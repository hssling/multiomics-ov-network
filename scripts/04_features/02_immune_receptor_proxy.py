from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


GENE_SETS = {
    "tcr_core_score": ["PTPRC", "CD3D", "CD3E", "CD3G", "TRAC", "TRBC1", "TRBC2", "LCK", "LAT", "ZAP70"],
    "cytolytic_score": ["NKG7", "PRF1", "GZMB", "GNLY", "CTSW", "CCL5"],
    "ifn_antigen_presentation_score": ["IFNG", "CXCL9", "CXCL10", "STAT1", "IRF1", "B2M", "HLA-A", "HLA-B", "HLA-C"],
    "exhaustion_regulatory_score": ["PDCD1", "LAG3", "TIGIT", "HAVCR2", "CTLA4"],
    "bcr_plasma_score": ["CD79A", "MS4A1", "CD74", "MZB1", "JCHAIN", "CD27"],
}


def score_gene_set(df: pd.DataFrame, genes: list[str]) -> tuple[pd.Series, list[str]]:
    found = [gene for gene in genes if gene in df.columns]
    if not found:
        return pd.Series(np.nan, index=df.index), found
    return df[found].mean(axis=1), found


def mann_whitney_like(series_a: pd.Series, series_b: pd.Series) -> float:
    try:
        from scipy.stats import mannwhitneyu

        return float(mannwhitneyu(series_a, series_b, alternative="two-sided").pvalue)
    except Exception:
        return float("nan")


def render_heatmap(df: pd.DataFrame, out_png: Path) -> None:
    corr = df.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(7, 5.5))
    im = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=35, ha="right")
    ax.set_yticks(range(len(corr.index)))
    ax.set_yticklabels(corr.index)
    ax.set_title("Immune-Receptor Proxy Score Correlation")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(out_png, dpi=160)
    plt.close(fig)


def render_risk_boxplot(df: pd.DataFrame, out_png: Path) -> None:
    score_cols = [c for c in df.columns if c.endswith("_score")]
    fig, axes = plt.subplots(1, len(score_cols), figsize=(3.5 * len(score_cols), 4.2), sharey=False)
    if len(score_cols) == 1:
        axes = [axes]
    for ax, col in zip(axes, score_cols):
        groups = []
        labels = []
        for label, sub in df.groupby("survival_risk_group"):
            groups.append(sub[col].dropna())
            labels.append(label)
        ax.boxplot(groups, tick_labels=labels)
        ax.set_title(col.replace("_", " "))
        ax.tick_params(axis="x", rotation=25)
    fig.suptitle("Immune-Receptor Proxy Scores by Risk Group")
    fig.tight_layout()
    fig.savefig(out_png, dpi=160)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("immune_proxy")

    processed = Path(cfg["paths"]["processed"])
    tables = Path(cfg["paths"]["results_tables"])
    figures = Path(cfg["paths"]["results_figures"])
    reports = Path("results/reports")
    for path in [tables, figures, reports]:
        path.mkdir(parents=True, exist_ok=True)

    rna = pd.read_csv(processed / "rna_z.csv")
    outcomes = pd.read_csv(processed / "outcomes.csv")

    scores = rna[["sample_id", "patient_id"]].copy()
    summary_rows = []
    for name, genes in GENE_SETS.items():
        values, found = score_gene_set(rna, genes)
        scores[name] = values
        low = values[outcomes.set_index("patient_id").reindex(scores["patient_id"])["survival_risk_group"].values == "low_risk"]
        high = values[outcomes.set_index("patient_id").reindex(scores["patient_id"])["survival_risk_group"].values == "high_risk"]
        summary_rows.append(
            {
                "score": name,
                "genes_requested": len(genes),
                "genes_found": len(found),
                "genes_found_list": ";".join(found),
                "mean_score": float(pd.Series(values).mean()),
                "sd_score": float(pd.Series(values).std()),
                "high_minus_low_mean": float(pd.Series(high).mean() - pd.Series(low).mean()),
                "p_value_mannwhitney": mann_whitney_like(pd.Series(high).dropna(), pd.Series(low).dropna()),
            }
        )

    merged = scores.merge(outcomes[["patient_id", "survival_risk_group", "vital_status"]], on="patient_id", how="left")
    merged["immune_proxy_composite"] = merged[[c for c in merged.columns if c.endswith("_score")]].mean(axis=1)

    score_path = tables / "immune_receptor_proxy_scores.csv"
    summary_path = tables / "immune_receptor_proxy_summary.csv"
    merged.to_csv(score_path, index=False)
    pd.DataFrame(summary_rows).to_csv(summary_path, index=False)

    render_heatmap(merged[[c for c in merged.columns if c.endswith("_score")]], figures / "immune_receptor_proxy_heatmap.png")
    render_risk_boxplot(merged, figures / "immune_receptor_proxy_by_risk.png")

    report = f"""# Immune-Receptor Proxy Analysis

Date: 2026-04-20
Project: multiomics-ov-network

## Scope

This branch estimates immune-receptor and immune-context proxy scores from TCGA-OV RNA expression.
It does not reconstruct TCR or BCR clonotypes and does not claim sequence-level receptor discovery.

## Feasible With Current Data

- T-cell infiltration proxy scoring
- cytolytic activity proxy scoring
- interferon/antigen-presentation proxy scoring
- exhaustion/regulatory marker scoring
- B-cell/plasma-cell proxy scoring

## Not Feasible With Current Data

- clonotype reconstruction
- paired receptor chain recovery
- CAR transgene detection

## Output Files

- `results/tables/immune_receptor_proxy_scores.csv`
- `results/tables/immune_receptor_proxy_summary.csv`
- `results/figures/immune_receptor_proxy_heatmap.png`
- `results/figures/immune_receptor_proxy_by_risk.png`
"""
    (reports / "immune_receptor_proxy.md").write_text(report, encoding="utf-8")
    log.info("Wrote immune proxy outputs for %s patients", merged["patient_id"].nunique())


if __name__ == "__main__":
    main()
