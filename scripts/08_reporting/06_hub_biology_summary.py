from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


TOP_HUBS = ["LF8", "LF5", "LF6", "LF7"]


def fit_aligned_pca(z_path: Path, module_path: Path, prefix: str, n_components: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    z_df = pd.read_csv(z_path)
    score_df = pd.read_csv(module_path)
    feats = [c for c in z_df.columns if c not in ["sample_id", "patient_id"]]
    mod_cols = [c for c in score_df.columns if c.startswith(f"{prefix}_module_")]
    n_components = min(n_components, len(mod_cols), len(feats), max(2, len(z_df) - 1))

    pca = PCA(n_components=n_components, random_state=42)
    scores = pca.fit_transform(z_df[feats])
    loadings = pca.components_.copy()

    aligned_scores = scores.copy()
    aligned_loadings = loadings.copy()
    for idx, col in enumerate(mod_cols[:n_components]):
        corr = np.corrcoef(scores[:, idx], score_df[col].to_numpy())[0, 1]
        if np.isnan(corr):
            corr = 1.0
        if corr < 0:
            aligned_scores[:, idx] *= -1
            aligned_loadings[idx, :] *= -1

    loading_rows = []
    for idx, col in enumerate(mod_cols[:n_components]):
        comp = aligned_loadings[idx, :]
        order = np.argsort(np.abs(comp))[::-1]
        for rank, feat_idx in enumerate(order[:25], start=1):
            loading_rows.append(
                {
                    "module": col,
                    "feature": feats[feat_idx],
                    "loading": float(comp[feat_idx]),
                    "abs_loading": float(abs(comp[feat_idx])),
                    "rank_abs": rank,
                }
            )
    return pd.DataFrame(loading_rows), pd.DataFrame(aligned_scores, columns=mod_cols[:n_components])


def summarize_hub_edges(edges: pd.DataFrame, loadings_map: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    subset = edges[edges["target"].isin(TOP_HUBS) | edges["source"].isin(TOP_HUBS)].copy()

    for hub in TOP_HUBS:
        incoming = subset[subset["target"] == hub].copy()
        incoming["abs_weight"] = incoming["weight"].abs()
        incoming = incoming.sort_values("abs_weight", ascending=False)

        for _, edge in incoming.head(6).iterrows():
            src = edge["source"]
            layer = "rna" if str(src).startswith("rna_module_") else "protein" if str(src).startswith("protein_module_") else "other"
            top_features = ""
            if layer in loadings_map:
                mod_loadings = loadings_map[layer]
                sub = mod_loadings[mod_loadings["module"] == src].head(8)
                if not sub.empty:
                    top_features = "; ".join(f"{r.feature} ({r.loading:.3f})" for r in sub.itertuples())
            rows.append(
                {
                    "hub": hub,
                    "edge_source": src,
                    "edge_target": edge["target"],
                    "edge_type": edge["etype"],
                    "edge_weight": float(edge["weight"]),
                    "direction": "incoming",
                    "module_layer": layer,
                    "top_module_features": top_features,
                }
            )

        outgoing = subset[subset["source"] == hub].copy()
        outgoing["abs_weight"] = outgoing["weight"].abs()
        outgoing = outgoing.sort_values("abs_weight", ascending=False)
        for _, edge in outgoing.head(4).iterrows():
            rows.append(
                {
                    "hub": hub,
                    "edge_source": edge["source"],
                    "edge_target": edge["target"],
                    "edge_type": edge["etype"],
                    "edge_weight": float(edge["weight"]),
                    "direction": "outgoing",
                    "module_layer": "outcome_or_protein",
                    "top_module_features": "",
                }
            )

    return pd.DataFrame(rows)


def build_markdown(summary: pd.DataFrame, out_path: Path) -> None:
    lines = [
        "# Hub Interpretation",
        "",
        "This note summarizes the strongest network-linked biological signals for the four leading latent hubs (LF8, LF5, LF6, LF7).",
        "Interpretation is based on the signed edge structure of the integrated network and on PCA-derived feature loadings for the linked RNA and protein modules.",
        "",
    ]
    for hub in TOP_HUBS:
        lines.append(f"## {hub}")
        hub_df = summary[summary["hub"] == hub]
        if hub_df.empty:
            lines.append("No hub-specific summary available.")
            lines.append("")
            continue
        incoming = hub_df[hub_df["direction"] == "incoming"].head(4)
        outgoing = hub_df[hub_df["direction"] == "outgoing"].head(3)

        if not incoming.empty:
            lines.append("Key incoming signals:")
            for row in incoming.itertuples():
                feat_text = row.top_module_features if row.top_module_features else "No module feature summary available."
                lines.append(
                    f"- {row.edge_source} -> {row.edge_target} ({row.edge_weight:.3f}, {row.edge_type}): {feat_text}"
                )
        if not outgoing.empty:
            lines.append("Key outgoing signals:")
            for row in outgoing.itertuples():
                lines.append(f"- {row.edge_source} -> {row.edge_target} ({row.edge_weight:.3f}, {row.edge_type})")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("hub_biology")

    processed = Path(cfg["paths"]["processed"])
    networks = Path(cfg["paths"]["results_networks"])
    tables = Path(cfg["paths"]["results_tables"])
    ijco_dir = ROOT / "manuscript" / "submission_package" / "targets" / "ijco"
    bjc_dir = ROOT / "manuscript" / "submission_package" / "targets" / "british_journal_of_cancer"
    ijco_dir.mkdir(parents=True, exist_ok=True)
    bjc_dir.mkdir(parents=True, exist_ok=True)

    rna_loadings, _ = fit_aligned_pca(
        processed / "rna_z.csv",
        processed / "rna_modules.csv",
        prefix="rna",
        n_components=50,
    )
    rna_loadings.to_csv(tables / "rna_module_top_loadings.csv", index=False)

    loadings_map: dict[str, pd.DataFrame] = {"rna": rna_loadings}
    protein_z = processed / "protein_z.csv"
    protein_modules = processed / "protein_modules.csv"
    if protein_z.exists() and protein_modules.exists():
        protein_loadings, _ = fit_aligned_pca(
            protein_z,
            protein_modules,
            prefix="protein",
            n_components=20,
        )
        protein_loadings.to_csv(tables / "protein_module_top_loadings.csv", index=False)
        loadings_map["protein"] = protein_loadings

    edges = pd.read_csv(networks / "multilayer_network_edges.csv")
    summary = summarize_hub_edges(edges, loadings_map)
    summary.to_csv(tables / "hub_biology_summary.csv", index=False)

    build_markdown(summary, ijco_dir / "hub_interpretation.md")
    build_markdown(summary, bjc_dir / "hub_interpretation.md")
    log.info("Hub biology summaries written for IJCO and BJC targets")


if __name__ == "__main__":
    main()
