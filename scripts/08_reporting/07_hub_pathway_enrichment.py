from __future__ import annotations

from pathlib import Path
import re
import sys

import pandas as pd
import gseapy as gp

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


TOP_HUBS = ["LF8", "LF5", "LF6", "LF7"]
GENE_RE = re.compile(r"^[A-Z0-9][A-Z0-9\-\.]{1,}$")
EXCLUDE_PREFIXES = ("AC", "AL", "AP", "LINC", "RN7", "RNU", "MTCO", "IG", "AGID", "MRPS", "RPL", "RPS")
LIBRARIES = ["MSigDB_Hallmark_2020", "KEGG_2021_Human", "GO_Biological_Process_2023"]


def parse_genes(feature_blob: str) -> list[str]:
    genes: list[str] = []
    if not isinstance(feature_blob, str) or not feature_blob.strip():
        return genes
    for part in feature_blob.split(";"):
        gene = part.strip().split(" (")[0]
        if not gene:
            continue
        if not GENE_RE.match(gene):
            continue
        if gene.startswith(EXCLUDE_PREFIXES):
            continue
        genes.append(gene)
    return genes


def main() -> None:
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("hub_enrichment")

    tables = Path(cfg["paths"]["results_tables"])
    ijco_dir = ROOT / "manuscript" / "submission_package" / "targets" / "ijco"
    bjc_dir = ROOT / "manuscript" / "submission_package" / "targets" / "british_journal_of_cancer"
    ijco_dir.mkdir(parents=True, exist_ok=True)
    bjc_dir.mkdir(parents=True, exist_ok=True)

    hub_summary = pd.read_csv(tables / "hub_biology_summary.csv")

    all_rows: list[dict] = []
    md_lines = [
        "# Hub Pathway Enrichment",
        "",
        "This note summarizes pathway enrichment for the strongest module-linked genes associated with the four leading latent hubs.",
        "Enrichment was performed with Enrichr libraries through gseapy and should be treated as hypothesis-generating support for the network interpretation.",
        "",
    ]

    for hub in TOP_HUBS:
        hub_df = hub_summary[(hub_summary["hub"] == hub) & (hub_summary["direction"] == "incoming")].copy()
        gene_pool: list[str] = []
        for blob in hub_df["top_module_features"].fillna(""):
            gene_pool.extend(parse_genes(blob))
        genes = sorted(set(gene_pool))
        if len(genes) < 5:
            log.warning("Skipping enrichment for %s: only %d usable genes", hub, len(genes))
            continue

        hub_results: list[pd.DataFrame] = []
        for lib in LIBRARIES:
            try:
                enr = gp.enrichr(
                    gene_list=genes,
                    gene_sets=lib,
                    organism="Human",
                    outdir=None,
                    cutoff=1.0,
                )
            except Exception as exc:
                log.warning("Enrichment failed for %s using %s: %s", hub, lib, exc)
                continue
            df = enr.results.copy()
            if df.empty:
                continue
            keep = ["Term", "Adjusted P-value", "P-value", "Combined Score", "Odds Ratio", "Genes"]
            present = [c for c in keep if c in df.columns]
            df = df[present].copy().head(8)
            df.insert(0, "library", lib)
            df.insert(0, "hub", hub)
            hub_results.append(df)

        if not hub_results:
            continue

        merged = pd.concat(hub_results, ignore_index=True)
        all_rows.append(merged)

        md_lines.append(f"## {hub}")
        md_lines.append(f"Usable enrichment genes: {', '.join(genes[:20])}" + (" ..." if len(genes) > 20 else ""))
        for lib in LIBRARIES:
            sub = merged[merged["library"] == lib].head(3)
            if sub.empty:
                continue
            md_lines.append(f"### {lib}")
            for _, row in sub.iterrows():
                term = row["Term"]
                adj = float(row["Adjusted P-value"])
                genes_hit = row["Genes"] if "Genes" in row else ""
                md_lines.append(f"- {term} | adjusted P={adj:.3g} | genes={genes_hit}")
        md_lines.append("")

    if all_rows:
        full = pd.concat(all_rows, ignore_index=True)
        full.to_csv(tables / "hub_pathway_enrichment.csv", index=False)
        (ijco_dir / "hub_pathway_enrichment.md").write_text("\n".join(md_lines), encoding="utf-8")
        (bjc_dir / "hub_pathway_enrichment.md").write_text("\n".join(md_lines), encoding="utf-8")
        log.info("Hub pathway enrichment written")
    else:
        log.warning("No enrichment output generated")


if __name__ == "__main__":
    main()
