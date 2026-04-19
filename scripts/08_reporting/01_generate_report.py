from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Template

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


def render_km(outcomes: pd.DataFrame, out_png: Path):
    try:
        from lifelines import KaplanMeierFitter

        kmf = KaplanMeierFitter()
        fig, ax = plt.subplots(figsize=(7, 5))
        for grp, df in outcomes.groupby("survival_risk_group"):
            t = df["days_to_death"].fillna(df["days_to_last_follow_up"])
            e = (df["vital_status"].str.lower() == "dead").astype(int)
            kmf.fit(durations=t, event_observed=e, label=grp)
            kmf.plot_survival_function(ax=ax)
        ax.set_title("Survival by Derived Risk Group")
        ax.set_xlabel("Days")
        ax.set_ylabel("Survival probability")
        fig.tight_layout()
        fig.savefig(out_png, dpi=150)
        plt.close(fig)
    except Exception:
        fig, ax = plt.subplots(figsize=(7, 5))
        counts = outcomes["survival_risk_group"].value_counts()
        ax.bar(counts.index.tolist(), counts.values.tolist())
        ax.set_title("Risk Group Counts (KM fallback)")
        fig.tight_layout()
        fig.savefig(out_png, dpi=150)
        plt.close(fig)


def render_perturbation_ci(perturb: pd.DataFrame, out_png: Path):
    req = {"hub", "delta_global_boot_mean", "delta_global_ci_low", "delta_global_ci_high"}
    if not req.issubset(set(perturb.columns)):
        return
    p = perturb.dropna(subset=["delta_global_boot_mean"]).copy().head(10)
    if p.empty:
        return
    p = p.sort_values("delta_global_boot_mean", ascending=False)
    yerr = [
        p["delta_global_boot_mean"] - p["delta_global_ci_low"],
        p["delta_global_ci_high"] - p["delta_global_boot_mean"],
    ]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(p["hub"], p["delta_global_boot_mean"], yerr=yerr, capsize=3)
    ax.set_ylabel("Delta global PageRank L1")
    ax.set_title("Perturbation Effect (Bootstrap 95% CI)")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


def main():
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("report")

    processed = Path(cfg["paths"]["processed"])
    tables = Path(cfg["paths"]["results_tables"])
    figures = Path(cfg["paths"]["results_figures"])
    models = Path(cfg["paths"]["results_models"])
    networks = Path(cfg["paths"]["results_networks"])
    reports = Path("results/reports")
    manuscript_dir = Path("manuscript")

    for p in [figures, reports, manuscript_dir]:
        p.mkdir(parents=True, exist_ok=True)

    outcomes = pd.read_csv(processed / "outcomes.csv")
    km_path = figures / "survival_km.png"
    render_km(outcomes, km_path)

    sample_summary = pd.read_csv(tables / "sample_matching_summary.csv")
    feature_summary = pd.read_csv(tables / "feature_count_summary.csv")
    top_hubs = pd.read_csv(networks / "network_centrality.csv").head(20)
    hub_stab_path = networks / "network_centrality_stability.csv"
    hub_stab = pd.read_csv(hub_stab_path).head(20) if hub_stab_path.exists() else pd.DataFrame()
    perturb = pd.read_csv(tables / "perturbation_delta.csv").head(20)
    perturb_full = pd.read_csv(tables / "perturbation_delta.csv")
    benchmark_path = tables / "model_benchmark.csv"
    benchmark = pd.read_csv(benchmark_path) if benchmark_path.exists() else pd.DataFrame()
    benchmark_prot_path = tables / "model_benchmark_protein_matched.csv"
    benchmark_prot = pd.read_csv(benchmark_prot_path) if benchmark_prot_path.exists() else pd.DataFrame()
    protein_row = feature_summary[feature_summary["layer"] == "protein"]
    protein_status = (
        f"Protein layer included (n_samples={int(protein_row.iloc[0]['n_samples'])})"
        if not protein_row.empty
        else "Protein layer not available in current run"
    )
    top_model = benchmark.sort_values("auc", ascending=False).head(1)
    top_model_txt = (
        f"Top all-sample AUC model: {top_model.iloc[0]['model']} (AUC={top_model.iloc[0]['auc']:.3f})"
        if not top_model.empty and pd.notna(top_model.iloc[0]["auc"])
        else "Top all-sample AUC model: unavailable"
    )
    top_hub_txt = (
        f"Top central hub: {top_hubs.iloc[0]['node']} (rank_score={top_hubs.iloc[0]['rank_score']:.3f})"
        if not top_hubs.empty
        else "Top central hub: unavailable"
    )
    top_pert_txt = (
        f"Top perturbation-sensitive hub: {perturb.iloc[0]['hub']} (delta_global={perturb.iloc[0]['delta_global_pagerank_l1']:.3f})"
        if not perturb.empty and "delta_global_pagerank_l1" in perturb.columns
        else "Top perturbation-sensitive hub: unavailable"
    )
    render_perturbation_ci(perturb_full, figures / "perturbation_bootstrap_ci.png")

    html_tpl = Template("""
    <html><head><title>Multi-Omics OV Report</title></head>
    <body>
    <h1>TCGA-OV Multi-Omics Network Report</h1>
    <h2>Key Findings</h2>
    <ul>
      <li>{{ key_find_1 }}</li>
      <li>{{ key_find_2 }}</li>
      <li>{{ key_find_3 }}</li>
    </ul>
    <h2>Sample Matching Summary</h2>
    {{ sample_table }}
    <h2>Feature Count Summary</h2>
    {{ feature_table }}
    <h2>Top Network Hubs</h2>
    {{ hub_table }}
    <h2>Hub Stability (Bootstrap)</h2>
    {{ hub_stability_table }}
    <h2>Perturbation Delta (Top)</h2>
    {{ perturb_table }}
    <h2>Benchmark (Single-Omics vs Integrated)</h2>
    <p>{{ protein_status }}</p>
    {{ benchmark_table }}
    <h2>Benchmark (Protein-Matched Fair Comparison)</h2>
    {{ benchmark_protein_table }}
    <h2>Figures</h2>
    <p><img src="../figures/survival_km.png" width="500"></p>
    <p><img src="../figures/mofa_factors.png" width="500"></p>
    <p><img src="../figures/diablo_components.png" width="500"></p>
    <p><img src="../figures/model_benchmark_auc_ci.png" width="500"></p>
    <p><img src="../figures/model_benchmark_cox_cindex_ci.png" width="500"></p>
    <p><img src="../figures/model_benchmark_protein_matched_auc_ci.png" width="500"></p>
    <p><img src="../figures/model_benchmark_protein_matched_cox_cindex_ci.png" width="500"></p>
    <p><img src="../figures/perturbation_bootstrap_ci.png" width="500"></p>
    </body></html>
    """)

    html = html_tpl.render(
        sample_table=sample_summary.to_html(index=False),
        feature_table=feature_summary.to_html(index=False),
        hub_table=top_hubs.to_html(index=False),
        hub_stability_table=(hub_stab.to_html(index=False) if not hub_stab.empty else "<p>No hub stability table available.</p>"),
        perturb_table=perturb.to_html(index=False),
        benchmark_table=(benchmark.to_html(index=False) if not benchmark.empty else "<p>No benchmark table available.</p>"),
        benchmark_protein_table=(
            benchmark_prot.to_html(index=False) if not benchmark_prot.empty else "<p>No protein-matched benchmark table available.</p>"
        ),
        protein_status=protein_status,
        key_find_1=top_model_txt,
        key_find_2=top_hub_txt,
        key_find_3=top_pert_txt,
    )

    (reports / "final_report.html").write_text(html, encoding="utf-8")

    manuscript = f"""# Manuscript Skeleton: TCGA-OV Multi-Omics Network Analysis

## Methods
- Cohort: {cfg['cohort_filters']['project_id']}
- Main layers: {', '.join(cfg['analysis']['main_layers'])}
- Integration methods: MOFA2-like latent factors, DIABLO-like supervised components
- Network ranking: degree, betweenness, pagerank, stability score
- Perturbation: edge dampening around top hubs

## Results (Placeholders)
- Figure 1: Cohort flow and sample matching
- Figure 2: Latent factor landscape (MOFA)
- Figure 3: Supervised components (DIABLO)
- Figure 4: Integrated multi-layer network
- Figure 5: Survival curves by network-derived risk group
- Table 1: Matched-sample counts by layer
- Table 2: Top cross-layer hubs
- Table 3: Perturbation response summary

## Discussion
- Placeholder: biological interpretation, robustness checks, limitations, and future extension with proteomics.
"""
    (manuscript_dir / "manuscript_skeleton.md").write_text(manuscript, encoding="utf-8")
    log.info("Reporting artifacts generated")


if __name__ == "__main__":
    main()
