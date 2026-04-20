from pathlib import Path
import gzip
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


MOTIFS = {
    "wpre_core": "AATCAACCTCTGGAT",
    "cd3zeta_motif": "CAGCAGGACCTGAA",
    "cd8a_hinge_like": "GACGCCGCCACCATC",
    "fmc63_like_seed": "CAGGTGCAGCTGGTG",
}


def reverse_complement(seq: str) -> str:
    comp = str.maketrans("ACGTN", "TGCAN")
    return seq.translate(comp)[::-1]


def count_motifs(path: Path, max_reads: int = 150000) -> dict:
    counts = {k: 0 for k in MOTIFS}
    sampled_reads = 0
    with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as handle:
        while sampled_reads < max_reads:
            header = handle.readline()
            if not header:
                break
            seq = handle.readline().strip().upper()
            handle.readline()
            handle.readline()
            if not seq:
                break
            sampled_reads += 1
            rc = reverse_complement(seq)
            for label, motif in MOTIFS.items():
                if motif in seq or motif in rc:
                    counts[label] += 1
    out = {"file": str(path.relative_to(ROOT)), "sampled_reads": sampled_reads}
    out.update(counts)
    return out


def main() -> None:
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("cart_motif_benchmark")

    fastq_dir = ROOT / "data" / "raw" / "external_validation" / "car_benchmark" / "SRR31001810"
    tables = ROOT / cfg["paths"]["results_tables"]
    reports = ROOT / "results" / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    rows = [count_motifs(path) for path in sorted(fastq_dir.glob("*.fastq.gz"))]
    df = pd.DataFrame(rows)
    out_csv = tables / "cart_motif_benchmark.csv"
    df.to_csv(out_csv, index=False)

    md = f"""# CAR Motif Benchmark

Date: 2026-04-20
Project: multiomics-ov-network

## Purpose

This module provides a conservative intermediate benchmark between raw FASTQ QC and future full reference-panel alignment.

## Important limitation

These motif counts are heuristic and are **not** sufficient to claim CAR construct recovery.
They only test whether the direct CAR-product dataset contains sequence fragments compatible with commonly discussed CAR backbone motifs.

## Output

- `results/tables/cart_motif_benchmark.csv`
"""
    (reports / "cart_motif_benchmark.md").write_text(md, encoding="utf-8")
    log.info("Wrote %s", out_csv)


if __name__ == "__main__":
    main()

