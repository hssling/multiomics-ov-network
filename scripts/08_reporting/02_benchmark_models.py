from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


def prep_matrix(df: pd.DataFrame, max_components: int = 20) -> np.ndarray:
    id_cols = [c for c in ["sample_id", "patient_id"] if c in df.columns]
    x = df.drop(columns=id_cols, errors="ignore").fillna(0.0)
    x = x.loc[:, x.std(axis=0) > 0]
    if x.shape[1] == 0:
        return np.empty((len(df), 0))
    z = StandardScaler().fit_transform(x.values)
    k = min(max_components, z.shape[1], max(1, z.shape[0] - 1))
    if k < z.shape[1]:
        z = PCA(n_components=k, random_state=42).fit_transform(z)
    return z


def manual_c_index(times: np.ndarray, risks: np.ndarray, events: np.ndarray) -> float:
    concordant = 0.0
    permissible = 0.0
    n = len(times)
    for i in range(n):
        for j in range(i + 1, n):
            ti, tj = times[i], times[j]
            ei, ej = events[i], events[j]
            if ti == tj:
                continue
            if ti < tj and ei == 1:
                permissible += 1
                if risks[i] > risks[j]:
                    concordant += 1
                elif risks[i] == risks[j]:
                    concordant += 0.5
            elif tj < ti and ej == 1:
                permissible += 1
                if risks[j] > risks[i]:
                    concordant += 1
                elif risks[i] == risks[j]:
                    concordant += 0.5
    if permissible == 0:
        return np.nan
    return concordant / permissible


def cv_probs(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    probs = np.full(shape=(len(y),), fill_value=np.nan, dtype=float)
    if X.shape[1] == 0 or len(np.unique(y)) < 2:
        return probs
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for tr, te in skf.split(X, y):
        model = LogisticRegression(max_iter=2000, class_weight="balanced")
        model.fit(X[tr], y[tr])
        probs[te] = model.predict_proba(X[te])[:, 1]
    return probs


def cv_cox_risk(X: np.ndarray, y: np.ndarray, times: np.ndarray, events: np.ndarray) -> np.ndarray:
    risk = np.full(shape=(len(times),), fill_value=np.nan, dtype=float)
    if X.shape[1] == 0:
        return risk

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for tr, te in skf.split(X, y):
        xt, xv = X[tr], X[te]
        tt, et = times[tr], events[tr]
        pred = None
        # 1) Prefer penalized CoxPH for stability when available.
        try:
            from lifelines import CoxPHFitter

            cols = [f"x{i}" for i in range(xt.shape[1])]
            dtr = pd.DataFrame(xt, columns=cols)
            dtr["time"] = np.clip(tt, a_min=0.0, a_max=None) + 1e-6
            dtr["event"] = et.astype(int)
            cph = CoxPHFitter(penalizer=0.1)
            cph.fit(dtr, duration_col="time", event_col="event")
            dte = pd.DataFrame(xv, columns=cols)
            pred = np.log(cph.predict_partial_hazard(dte).values.reshape(-1))
        except Exception:
            pred = None

        # 2) Statsmodels PHReg fallback.
        if pred is None:
            try:
                from statsmodels.duration.hazard_regression import PHReg

                m = PHReg(endog=tt, exog=xt, status=et, ties="breslow")
                r = m.fit(disp=0)
                pred = xv @ r.params
            except Exception:
                pred = None

        # 3) Final regularized linear fallback on log-time proxy.
        if pred is None or np.all(~np.isfinite(pred)):
            lr = LinearRegression()
            lr.fit(xt, np.log1p(np.clip(tt, a_min=0, a_max=None)))
            pred = -lr.predict(xv)

        pred = np.asarray(pred, dtype=float).reshape(-1)
        bad = ~np.isfinite(pred)
        if bad.any():
            fill = np.nanmedian(pred[~bad]) if (~bad).any() else 0.0
            pred[bad] = fill
        risk[te] = pred
    return risk


def bootstrap_metric_ci(metric_values: np.ndarray) -> tuple[float, float]:
    vals = metric_values[~np.isnan(metric_values)]
    if len(vals) == 0:
        return np.nan, np.nan
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def bootstrap_all(
    y: np.ndarray,
    probs: np.ndarray,
    times: np.ndarray,
    events: np.ndarray,
    cox_risk: np.ndarray,
    n_boot: int = 300,
    seed: int = 42,
) -> dict:
    valid_cls = ~np.isnan(probs)
    y1, p1, t1, e1 = y[valid_cls], probs[valid_cls], times[valid_cls], events[valid_cls]
    valid_cox = ~np.isnan(cox_risk)
    t2, e2, r2 = times[valid_cox], events[valid_cox], cox_risk[valid_cox]

    auc = roc_auc_score(y1, p1) if len(y1) >= 20 and len(np.unique(y1)) >= 2 else np.nan
    cidx = manual_c_index(t1, p1, e1) if len(y1) >= 20 else np.nan
    cox_cidx = manual_c_index(t2, r2, e2) if len(t2) >= 20 else np.nan

    rng = np.random.default_rng(seed)
    auc_bs, cidx_bs, cox_bs = [], [], []
    if len(y1) >= 20:
        for _ in range(n_boot):
            idx = rng.integers(0, len(y1), len(y1))
            ys, ps, ts, es = y1[idx], p1[idx], t1[idx], e1[idx]
            if len(np.unique(ys)) >= 2:
                auc_bs.append(float(roc_auc_score(ys, ps)))
            c = manual_c_index(ts, ps, es)
            if not np.isnan(c):
                cidx_bs.append(float(c))
    if len(t2) >= 20:
        for _ in range(n_boot):
            idx = rng.integers(0, len(t2), len(t2))
            c = manual_c_index(t2[idx], r2[idx], e2[idx])
            if not np.isnan(c):
                cox_bs.append(float(c))

    auc_lo, auc_hi = bootstrap_metric_ci(np.array(auc_bs, dtype=float))
    c_lo, c_hi = bootstrap_metric_ci(np.array(cidx_bs, dtype=float))
    cx_lo, cx_hi = bootstrap_metric_ci(np.array(cox_bs, dtype=float))
    return {
        "auc": float(auc) if not np.isnan(auc) else np.nan,
        "auc_ci_low": auc_lo,
        "auc_ci_high": auc_hi,
        "c_index": float(cidx) if not np.isnan(cidx) else np.nan,
        "c_index_ci_low": c_lo,
        "c_index_ci_high": c_hi,
        "cox_c_index": float(cox_cidx) if not np.isnan(cox_cidx) else np.nan,
        "cox_c_index_ci_low": cx_lo,
        "cox_c_index_ci_high": cx_hi,
    }


def evaluate_view(name: str, df: pd.DataFrame, outcomes: pd.DataFrame, id_subset: set | None = None) -> dict:
    ids = set(df["patient_id"]).intersection(set(outcomes["patient_id"]))
    if id_subset is not None:
        ids = ids.intersection(id_subset)
    if len(ids) < 20:
        return {"model": name, "n_samples": len(ids)}

    common = sorted(ids)
    dfx = df[df["patient_id"].isin(common)].copy().sort_values("patient_id")
    dfo = outcomes[outcomes["patient_id"].isin(common)].copy().sort_values("patient_id")
    common2 = sorted(set(dfx["patient_id"]).intersection(set(dfo["patient_id"])))
    dfx = dfx[dfx["patient_id"].isin(common2)].sort_values("patient_id")
    dfo = dfo[dfo["patient_id"].isin(common2)].sort_values("patient_id")

    X = prep_matrix(dfx, max_components=20)
    y = dfo["y"].to_numpy()
    t = dfo["time"].to_numpy()
    e = dfo["event"].to_numpy()
    probs = cv_probs(X, y)
    cox_risk = cv_cox_risk(X, y, t, e)
    m = bootstrap_all(y, probs, t, e, cox_risk, n_boot=300, seed=42)
    return {"model": name, "n_samples": len(common2), **m}


def bar_ci(df: pd.DataFrame, metric: str, lo: str, hi: str, ylabel: str, title: str, out_png: Path):
    p = df.dropna(subset=[metric]).copy()
    if p.empty:
        return
    p = p.sort_values(metric, ascending=False)
    yerr = np.vstack([p[metric] - p[lo], p[hi] - p[metric]])
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(p["model"], p[metric], yerr=yerr, capsize=3)
    ax.set_ylim(0.0, 1.0)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


def main():
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("benchmark")

    processed = Path(cfg["paths"]["processed"])
    tables = Path(cfg["paths"]["results_tables"])
    figs = Path(cfg["paths"]["results_figures"])
    tables.mkdir(parents=True, exist_ok=True)
    figs.mkdir(parents=True, exist_ok=True)

    outcomes = pd.read_csv(processed / "outcomes.csv")
    outcomes["event"] = outcomes["vital_status"].astype(str).str.lower().eq("dead").astype(int)
    outcomes["time"] = outcomes["days_to_death"].fillna(outcomes["days_to_last_follow_up"]).fillna(0)
    outcomes = outcomes.dropna(subset=["patient_id", "survival_risk_group"]).copy()
    outcomes["y"] = outcomes["survival_risk_group"].astype(str).str.lower().eq("high_risk").astype(int)

    views = {
        "rna_modules": pd.read_csv(processed / "rna_modules.csv"),
        "cna": pd.read_csv(processed / "cna_z.csv"),
        "methylation": pd.read_csv(processed / "methylation_z.csv"),
        "mutation": pd.read_csv(processed / "mutation_binary.csv"),
    }
    views["integrated_no_protein"] = (
        views["rna_modules"][["sample_id", "patient_id"]]
        .merge(pd.read_csv(processed / "burden_features.csv"), on=["sample_id", "patient_id"], how="inner")
    )

    protein_mod = processed / "protein_modules.csv"
    if protein_mod.exists():
        views["protein_modules"] = pd.read_csv(protein_mod)
        views["integrated_with_protein"] = (
            views["integrated_no_protein"].merge(views["protein_modules"], on=["sample_id", "patient_id"], how="inner")
        )

    rows_all = [evaluate_view(name, df, outcomes, id_subset=None) for name, df in views.items()]
    all_df = pd.DataFrame(rows_all).sort_values(["auc", "c_index"], ascending=False, na_position="last")
    all_df.to_csv(tables / "model_benchmark.csv", index=False)

    protein_fair_models = ["rna_modules", "cna", "methylation", "mutation", "integrated_no_protein"]
    protein_ids = None
    if "protein_modules" in views:
        protein_fair_models.extend(["protein_modules", "integrated_with_protein"])
        protein_ids = set(views["protein_modules"]["patient_id"])
    rows_prot = [evaluate_view(m, views[m], outcomes, id_subset=protein_ids) for m in protein_fair_models if m in views]
    prot_df = pd.DataFrame(rows_prot).sort_values(["auc", "c_index"], ascending=False, na_position="last")
    prot_df.to_csv(tables / "model_benchmark_protein_matched.csv", index=False)

    bar_ci(
        all_df,
        metric="auc",
        lo="auc_ci_low",
        hi="auc_ci_high",
        ylabel="AUC (95% bootstrap CI)",
        title="Single-Omics vs Integrated (All Available Samples)",
        out_png=figs / "model_benchmark_auc_ci.png",
    )
    bar_ci(
        all_df,
        metric="cox_c_index",
        lo="cox_c_index_ci_low",
        hi="cox_c_index_ci_high",
        ylabel="Cox C-index (95% bootstrap CI)",
        title="Cox Benchmark (All Available Samples)",
        out_png=figs / "model_benchmark_cox_cindex_ci.png",
    )
    bar_ci(
        prot_df,
        metric="auc",
        lo="auc_ci_low",
        hi="auc_ci_high",
        ylabel="AUC (95% bootstrap CI)",
        title="Protein-Matched Fair Comparison (AUC)",
        out_png=figs / "model_benchmark_protein_matched_auc_ci.png",
    )
    bar_ci(
        prot_df,
        metric="cox_c_index",
        lo="cox_c_index_ci_low",
        hi="cox_c_index_ci_high",
        ylabel="Cox C-index (95% bootstrap CI)",
        title="Protein-Matched Fair Comparison (Cox C-index)",
        out_png=figs / "model_benchmark_protein_matched_cox_cindex_ci.png",
    )

    log.info("Benchmark complete: %s all-sample models, %s protein-matched models", len(all_df), len(prot_df))


if __name__ == "__main__":
    main()
