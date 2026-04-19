from pathlib import Path
import itertools
import sys
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger

warnings.filterwarnings("ignore", category=FutureWarning)


def clean_matrix(df: pd.DataFrame) -> pd.DataFrame:
    x = df.drop(columns=[c for c in ["sample_id", "patient_id"] if c in df.columns], errors="ignore").copy()
    x = x.select_dtypes(include=[np.number]).fillna(0.0)
    x = x.loc[:, x.std(axis=0) > 0]
    return x


def pca_projection(df: pd.DataFrame, out_prefix: Path, title: str):
    x = clean_matrix(df)
    if x.shape[1] < 2 or x.shape[0] < 3:
        return None
    p = PCA(n_components=min(10, x.shape[0] - 1, x.shape[1]), random_state=42)
    z = StandardScaler().fit_transform(x.values)
    pc = p.fit_transform(z)
    exp = p.explained_variance_ratio_
    pca_df = pd.DataFrame(
        {
            "PC": [f"PC{i+1}" for i in range(len(exp))],
            "explained_variance_ratio": exp,
            "cumulative_explained_variance": np.cumsum(exp),
        }
    )
    pca_df.to_csv(out_prefix.with_suffix(".csv"), index=False)

    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.scatter(pc[:, 0], pc[:, 1], alpha=0.8, s=24)
    ax.set_xlabel(f"PC1 ({exp[0]*100:.1f}% var)")
    ax.set_ylabel(f"PC2 ({exp[1]*100:.1f}% var)")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(out_prefix.with_suffix(".png"), dpi=170)
    plt.close(fig)
    return pca_df


def cv_auc(X: np.ndarray, y: np.ndarray, model) -> float:
    if X.shape[1] == 0 or len(np.unique(y)) < 2:
        return np.nan
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    p = cross_val_predict(model, X, y, cv=skf, method="predict_proba")[:, 1]
    return float(roc_auc_score(y, p))


def bootstrap_auc_ci(X: np.ndarray, y: np.ndarray, model, n_boot: int = 200) -> tuple[float, float]:
    if X.shape[1] == 0 or len(np.unique(y)) < 2:
        return np.nan, np.nan
    rng = np.random.default_rng(42)
    vals = []
    n = len(y)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        xb, yb = X[idx], y[idx]
        if len(np.unique(yb)) < 2:
            continue
        vals.append(cv_auc(xb, yb, model))
    if len(vals) == 0:
        return np.nan, np.nan
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def permutation_p_value(X: np.ndarray, y: np.ndarray, model, n_perm: int = 200) -> dict:
    obs = cv_auc(X, y, model)
    if np.isnan(obs):
        return {"auc_observed": np.nan, "auc_null_mean": np.nan, "auc_null_sd": np.nan, "p_value_right_tail": np.nan}
    rng = np.random.default_rng(42)
    nulls = []
    for _ in range(n_perm):
        yp = y.copy()
        rng.shuffle(yp)
        nulls.append(cv_auc(X, yp, model))
    nulls = np.asarray([v for v in nulls if not np.isnan(v)], dtype=float)
    p = float((np.sum(nulls >= obs) + 1) / (len(nulls) + 1)) if len(nulls) else np.nan
    return {
        "auc_observed": float(obs),
        "auc_null_mean": float(np.mean(nulls)) if len(nulls) else np.nan,
        "auc_null_sd": float(np.std(nulls)) if len(nulls) else np.nan,
        "p_value_right_tail": p,
    }


def build_input_output_matrix(processed: Path, outcomes: pd.DataFrame) -> dict[str, pd.DataFrame]:
    views = {
        "rna_modules": pd.read_csv(processed / "rna_modules.csv"),
        "burdens": pd.read_csv(processed / "burden_features.csv"),
        "mutation": pd.read_csv(processed / "mutation_binary.csv"),
        "cna": pd.read_csv(processed / "cna_z.csv"),
        "methylation": pd.read_csv(processed / "methylation_z.csv"),
    }
    if (processed / "protein_modules.csv").exists():
        views["protein_modules"] = pd.read_csv(processed / "protein_modules.csv")

    # Align by patient_id, keep sample_id from first table.
    base = views["rna_modules"][["sample_id", "patient_id"]].drop_duplicates().copy()
    for name, df in views.items():
        cols = [c for c in df.columns if c not in ["sample_id"]]
        base = base.merge(df[cols], on="patient_id", how="inner")
    base = base.merge(outcomes[["patient_id", "y"]], on="patient_id", how="inner")
    return views, base


def to_xy(df: pd.DataFrame, y_col: str = "y") -> tuple[np.ndarray, np.ndarray]:
    xdf = df.drop(columns=[c for c in ["sample_id", "patient_id", y_col] if c in df.columns], errors="ignore")
    xdf = xdf.select_dtypes(include=[np.number]).fillna(0.0)
    xdf = xdf.loc[:, xdf.std(axis=0) > 0]
    y = df[y_col].astype(int).values
    return xdf.values, y


def compress_features(X: np.ndarray, max_components: int = 80) -> np.ndarray:
    if X.size == 0:
        return X
    if X.shape[1] <= max_components:
        return X
    n_comp = min(max_components, X.shape[1], max(2, X.shape[0] - 1))
    z = StandardScaler().fit_transform(X)
    return PCA(n_components=n_comp, random_state=42).fit_transform(z)


def main():
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("advanced_analytics")

    processed = Path(cfg["paths"]["processed"])
    tables = Path(cfg["paths"]["results_tables"])
    figs = Path(cfg["paths"]["results_figures"])
    tables.mkdir(parents=True, exist_ok=True)
    figs.mkdir(parents=True, exist_ok=True)

    outcomes = pd.read_csv(processed / "outcomes.csv")
    outcomes["y"] = outcomes["survival_risk_group"].astype(str).str.lower().eq("high_risk").astype(int)

    # 1) PCA evidence per major view.
    pca_rows = []
    pca_targets = {
        "rna_modules": processed / "rna_modules.csv",
        "cna": processed / "cna_z.csv",
        "methylation": processed / "methylation_z.csv",
        "mutation": processed / "mutation_binary.csv",
    }
    if (processed / "protein_modules.csv").exists():
        pca_targets["protein_modules"] = processed / "protein_modules.csv"
    for name, pth in pca_targets.items():
        df = pd.read_csv(pth)
        common = sorted(set(df["patient_id"]) & set(outcomes["patient_id"]))
        d = df[df["patient_id"].isin(common)].copy()
        out_pref = tables / f"pca_{name}"
        p = pca_projection(d, out_pref, f"PCA: {name}")
        if p is not None:
            pca_rows.append(
                {
                    "view": name,
                    "n_samples": len(d),
                    "n_features": clean_matrix(d).shape[1],
                    "pc1_var": float(p.loc[p["PC"] == "PC1", "explained_variance_ratio"].iloc[0]),
                    "pc2_var": float(p.loc[p["PC"] == "PC2", "explained_variance_ratio"].iloc[0]) if len(p) > 1 else np.nan,
                    "pc1_pc2_cum_var": float(p.loc[p["PC"].isin(["PC1", "PC2"]), "explained_variance_ratio"].sum()),
                }
            )
    pd.DataFrame(pca_rows).to_csv(tables / "pca_summary.csv", index=False)

    # 2) Advanced ML benchmark on integrated-no-protein feature set.
    views, merged = build_input_output_matrix(processed, outcomes)
    X, y = to_xy(merged)
    X = compress_features(X, max_components=80)
    models = {
        "logistic_l2": Pipeline(
            [("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=3000, class_weight="balanced"))]
        ),
        "elastic_net": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("clf", LogisticRegression(penalty="elasticnet", l1_ratio=0.5, solver="saga", max_iter=4000, class_weight="balanced")),
            ]
        ),
        "random_forest": RandomForestClassifier(n_estimators=400, random_state=42, class_weight="balanced"),
    }
    try:
        from xgboost import XGBClassifier

        models["xgboost"] = XGBClassifier(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.85,
            colsample_bytree=0.85,
            eval_metric="logloss",
            random_state=42,
        )
    except Exception:
        pass

    adv_rows = []
    for name, m in models.items():
        auc = cv_auc(X, y, m)
        lo, hi = bootstrap_auc_ci(X, y, m, n_boot=40)
        if pd.notna(auc) and pd.notna(lo) and pd.notna(hi):
            if lo > hi:
                lo, hi = hi, lo
            # Conservative guardrail for unstable bootstrap distributions in very small n.
            if not (lo <= auc <= hi):
                lo, hi = np.nan, np.nan
        adv_rows.append({"model": name, "n_samples": int(len(y)), "auc": auc, "auc_ci_low": lo, "auc_ci_high": hi})
    adv = pd.DataFrame(adv_rows).sort_values("auc", ascending=False)
    adv.to_csv(tables / "advanced_ml_benchmark.csv", index=False)

    if not adv.empty:
        p = adv.dropna(subset=["auc", "auc_ci_low", "auc_ci_high"]).copy()
        p = p[(p["auc_ci_high"] >= p["auc"]) & (p["auc"] >= p["auc_ci_low"])].copy()
        fig, ax = plt.subplots(figsize=(8.2, 4.6))
        if not p.empty:
            yerr = np.vstack(
                [
                    np.maximum(0.0, p["auc"].values - p["auc_ci_low"].values),
                    np.maximum(0.0, p["auc_ci_high"].values - p["auc"].values),
                ]
            )
            ax.bar(p["model"], p["auc"], yerr=yerr, capsize=3)
            ax.set_ylim(0.0, 1.0)
            ax.set_ylabel("AUC (95% bootstrap CI)")
            ax.set_title("Advanced ML Benchmark (Integrated Input Set)")
            ax.tick_params(axis="x", rotation=20)
        fig.tight_layout()
        fig.savefig(figs / "advanced_ml_benchmark_auc_ci.png", dpi=170)
        plt.close(fig)

    # 3) Input-output parameter experiments: ablation of omics blocks.
    block_map = {
        "rna_modules": [c for c in merged.columns if c.startswith("rna_module_")],
        "burdens": [c for c in merged.columns if c.endswith("_burden")],
        "mutation": [c for c in merged.columns if c.startswith("MUT_")],
        "cna": [c for c in merged.columns if c.startswith("CNA_")],
        "methylation": [c for c in merged.columns if c.startswith("METH_")],
        "protein_modules": [c for c in merged.columns if c.startswith("protein_module_")],
    }
    block_map = {k: v for k, v in block_map.items() if len(v) > 0}
    blocks = sorted(block_map.keys())

    ablation_rows = []
    for r in sorted(set([1, 2, min(3, len(blocks)), len(blocks)])):
        for combo in itertools.combinations(blocks, r):
            feat_cols = []
            for b in combo:
                feat_cols.extend(block_map[b])
            feat_cols = sorted(set(feat_cols))
            x = merged[feat_cols].select_dtypes(include=[np.number]).fillna(0.0)
            x = x.loc[:, x.std(axis=0) > 0]
            if x.shape[1] == 0:
                continue
            xv = compress_features(x.values, max_components=60)
            model = Pipeline(
                [("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=2000, class_weight="balanced"))]
            )
            auc = cv_auc(xv, y, model)
            ablation_rows.append(
                {
                    "blocks": "+".join(combo),
                    "n_blocks": len(combo),
                    "n_features": int(x.shape[1]),
                    "n_features_compressed": int(xv.shape[1]),
                    "n_samples": int(x.shape[0]),
                    "auc": auc,
                }
            )
    ablation = pd.DataFrame(ablation_rows).sort_values("auc", ascending=False)
    ablation.to_csv(tables / "input_output_ablation_auc.csv", index=False)

    if not ablation.empty:
        top = ablation.head(12).copy()
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.barh(top["blocks"][::-1], top["auc"][::-1])
        ax.set_xlabel("AUC")
        ax.set_title("Input-Output Experiments: Top Omics Block Combinations")
        fig.tight_layout()
        fig.savefig(figs / "input_output_ablation_top_auc.png", dpi=170)
        plt.close(fig)

    # 4) Permutation test on best ML model for inferential evidence.
    if not adv.empty:
        best_model = adv.iloc[0]["model"]
        best_est = models[best_model]
        perm = permutation_p_value(X, y, best_est, n_perm=50)
        perm["model"] = best_model
        pd.DataFrame([perm]).to_csv(tables / "permutation_test_auc.csv", index=False)
    else:
        pd.DataFrame(
            [{"model": np.nan, "auc_observed": np.nan, "auc_null_mean": np.nan, "auc_null_sd": np.nan, "p_value_right_tail": np.nan}]
        ).to_csv(tables / "permutation_test_auc.csv", index=False)

    # 5) Causal-pathway sensitivity proxy using DAG edge sign/strength aggregation.
    dag_path = Path(cfg["paths"]["results_networks"]) / "dag_pathways.csv"
    if dag_path.exists():
        dag = pd.read_csv(dag_path)
        c = (
            dag.groupby(["source_layer", "target_layer"], as_index=False)
            .agg(
                n_edges=("weight", "size"),
                mean_abs_weight=("weight", lambda s: float(np.mean(np.abs(s)))),
                mean_signed_weight=("weight", "mean"),
            )
            .sort_values(["n_edges", "mean_abs_weight"], ascending=False)
        )
        c.to_csv(tables / "causal_pathway_strength_summary.csv", index=False)
    else:
        pd.DataFrame(columns=["source_layer", "target_layer", "n_edges", "mean_abs_weight", "mean_signed_weight"]).to_csv(
            tables / "causal_pathway_strength_summary.csv", index=False
        )

    log.info("Advanced analytics complete: PCA, ML, ablation, permutation, causal-pathway summary")


if __name__ == "__main__":
    main()
