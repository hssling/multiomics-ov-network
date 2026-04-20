from pathlib import Path
import gzip
import math
import re
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
    "exhaustion_regulatory_score": ["PDCD1", "LAG3", "TIGIT", "HAVCR2", "CTLA4", "TOX"],
    "bcr_plasma_score": ["CD79A", "MS4A1", "CD74", "MZB1", "JCHAIN", "CD27"],
}


def guess_sheet(sheet_map: dict[str, pd.DataFrame], keyword: str) -> pd.DataFrame:
    for name, df in sheet_map.items():
        if keyword.lower() in name.lower():
            return df
    return next(iter(sheet_map.values()))


def parse_geo_series_metadata(text: str) -> dict[str, str]:
    sample_titles = []
    characteristics = []
    for line in text.splitlines():
        if line.startswith("!Sample_title"):
            sample_titles = [token.strip('"') for token in line.split("\t")[1:]]
        if line.startswith("!Sample_characteristics_ch1"):
            vals = [token.strip('"') for token in line.split("\t")[1:]]
            if vals and vals[0].startswith("cell type:"):
                characteristics = vals
    mapping = {}
    for title, cell_type in zip(sample_titles, characteristics):
        ct = cell_type.replace("cell type: ", "").strip()
        if "88-1.R+C29:G301.fastq" in ct:
            ct = "CD137+ PD-1high CD39+ CD8 T cells"
        mapping[title] = ct
    return mapping


def load_geo_series_metadata() -> dict[str, str]:
    import gzip as _gzip
    import requests

    url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE160nnn/GSE160705/matrix/GSE160705_series_matrix.txt.gz"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    text = _gzip.decompress(response.content).decode("utf-8", errors="ignore")
    return parse_geo_series_metadata(text)


def parse_combined_workbook(df: pd.DataFrame) -> pd.DataFrame:
    section_row = df.iloc[0].tolist()
    sample_row = df.iloc[1].tolist()
    norm_start = section_row.index("Normalized read counts")
    sample_names = [str(x) for x in sample_row[norm_start: ] if pd.notna(x)]

    genes = df.iloc[2:, 1].astype(str).tolist()
    norm_block = df.iloc[2:, norm_start : norm_start + len(sample_names)].copy()
    norm_block.columns = sample_names
    norm_block.insert(0, "gene", genes)
    norm_block = norm_block.dropna(subset=["gene"])
    for col in sample_names:
        norm_block[col] = pd.to_numeric(norm_block[col], errors="coerce")
    norm_block = norm_block.drop_duplicates(subset=["gene"])
    return norm_block


def score_matrix(expr: pd.DataFrame) -> pd.DataFrame:
    value_cols = [c for c in expr.columns if c != "gene"]
    expr = expr.set_index("gene")
    rows = []
    for sample in value_cols:
        row = {"sample": sample}
        for score_name, genes in GENE_SETS.items():
            found = [g for g in genes if g in expr.index]
            row[f"{score_name}"] = float(expr.loc[found, sample].mean()) if found else math.nan
            row[f"{score_name}_genes_found"] = len(found)
        rows.append(row)
    return pd.DataFrame(rows)


def render_external_scores(scores: pd.DataFrame, out_png: Path) -> None:
    plot_cols = [c for c in scores.columns if c.endswith("_score") and not c.endswith("_genes_found")]
    fig, axes = plt.subplots(1, len(plot_cols), figsize=(3.5 * len(plot_cols), 4.0), sharey=False)
    if len(plot_cols) == 1:
        axes = [axes]
    for ax, col in zip(axes, plot_cols):
        groups = []
        labels = []
        for label, sub in scores.groupby("sample_group"):
            groups.append(sub[col].dropna())
            labels.append(label)
        ax.boxplot(groups, tick_labels=labels)
        ax.set_title(col.replace("_", " "))
        ax.tick_params(axis="x", rotation=25)
    fig.suptitle("External Ovarian TIL Immune-State Scores")
    fig.tight_layout()
    fig.savefig(out_png, dpi=160)
    plt.close(fig)


def render_external_heatmap(scores: pd.DataFrame, out_png: Path) -> None:
    plot_cols = [c for c in scores.columns if c.endswith("_score") and not c.endswith("_genes_found")]
    corr = scores[plot_cols].corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(6.5, 5.0))
    im = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=35, ha="right")
    ax.set_yticks(range(len(corr.index)))
    ax.set_yticklabels(corr.index)
    ax.set_title("External Ovarian TIL Score Correlation")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(out_png, dpi=160)
    plt.close(fig)


def summarize_cart_fastq(path: Path, max_reads: int = 50000) -> dict:
    reads = 0
    total_bases = 0
    gc_bases = 0
    n_bases = 0
    lengths = []
    with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as handle:
        while reads < max_reads:
            header = handle.readline()
            if not header:
                break
            seq = handle.readline().strip()
            handle.readline()
            qual = handle.readline().strip()
            if not qual:
                break
            reads += 1
            total_bases += len(seq)
            gc_bases += seq.count("G") + seq.count("C")
            n_bases += seq.count("N")
            lengths.append(len(seq))
    return {
        "file": str(path.relative_to(ROOT)),
        "sampled_reads": reads,
        "mean_read_length": float(np.mean(lengths)) if lengths else math.nan,
        "sd_read_length": float(np.std(lengths)) if lengths else math.nan,
        "gc_fraction": (gc_bases / total_bases) if total_bases else math.nan,
        "n_fraction": (n_bases / total_bases) if total_bases else math.nan,
        "compressed_size_bytes": path.stat().st_size,
    }


def main() -> None:
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("external_validation_and_cart")

    raw_root = ROOT / "data" / "raw" / "external_validation"
    tables = ROOT / cfg["paths"]["results_tables"]
    figures = ROOT / cfg["paths"]["results_figures"]
    reports = ROOT / "results" / "reports"
    for path in [tables, figures, reports]:
        path.mkdir(parents=True, exist_ok=True)

    xlsx_path = raw_root / "GSE160705" / "GSE160705_Raw_data_read_counts_and_normalized_read_counts.xlsx"
    sheets = pd.read_excel(xlsx_path, sheet_name=None, header=None)
    norm_df = parse_combined_workbook(guess_sheet(sheets, "sheet"))
    scores = score_matrix(norm_df)
    sample_meta = load_geo_series_metadata()
    scores["sample_group"] = scores["sample"].map(sample_meta).fillna("unannotated")
    ext_scores_path = tables / "external_ovarian_immune_scores.csv"
    scores.to_csv(ext_scores_path, index=False)

    summary_rows = []
    score_cols = [c for c in scores.columns if c.endswith("_score") and not c.endswith("_genes_found")]
    for col in score_cols:
        for grp, sub in scores.groupby("sample_group"):
            summary_rows.append(
                {
                    "score": col,
                    "sample_group": grp,
                    "n_samples": int(sub.shape[0]),
                    "mean_score": float(sub[col].mean()),
                    "sd_score": float(sub[col].std()),
                }
            )
    summary = pd.DataFrame(summary_rows)
    summary_path = tables / "external_ovarian_immune_summary.csv"
    summary.to_csv(summary_path, index=False)
    render_external_scores(scores, figures / "external_ovarian_immune_scores.png")
    render_external_heatmap(scores, figures / "external_ovarian_immune_heatmap.png")

    cart_fastqs = sorted((raw_root / "car_benchmark" / "SRR31001810").glob("*.fastq.gz"))
    cart_qc = pd.DataFrame([summarize_cart_fastq(path) for path in cart_fastqs])
    cart_qc_path = tables / "cart_direct_benchmark_qc.csv"
    cart_qc.to_csv(cart_qc_path, index=False)

    report = f"""# External Validation and Direct CAR Benchmark

Date: 2026-04-20
Project: multiomics-ov-network

## External Ovarian Immune-Context Validation

- Dataset: `GSE160705` / `GSM4877937` family / `SRX9423612`
- Data used: processed read-count and normalized-count workbook from GEO
- Scope: external ovarian tumor-infiltrating CD8 T-cell immune-state comparison
- Output tables:
  - `results/tables/external_ovarian_immune_scores.csv`
  - `results/tables/external_ovarian_immune_summary.csv`

## Direct CAR Workflow Benchmark

- Dataset: `SRX26389396` / `SRR31001810`
- Data used: raw paired FASTQ files from ENA mirror of SRA
- Scope: ingestion and lightweight sequence QC on a true CAR-product RNA-seq run
- Important boundary: this benchmark validates external raw-read handling and dataset suitability, but does not claim CAR construct recovery without a validated reference panel and alignment stage.
- Output table:
  - `results/tables/cart_direct_benchmark_qc.csv`

## Main Result

The project now contains:
1. a real external ovarian immune-context dataset analyzed at expression level
2. a real direct CAR-product raw-read dataset downloaded and QC-profiled for workflow benchmarking
3. manuscript-ready outputs that separate ovarian external biology validation from direct CAR benchmarking
"""
    (reports / "external_validation_and_cart_benchmark.md").write_text(report, encoding="utf-8")
    log.info("Wrote external immune validation and CAR benchmark outputs")


if __name__ == "__main__":
    main()
