from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


def inventory_files(roots: list[Path], patterns: list[str]) -> pd.DataFrame:
    rows = []
    for root in roots:
        for pattern in patterns:
            count = 0
            if root.exists():
                count = sum(1 for _ in root.rglob(pattern))
            rows.append({"root": str(root), "pattern": pattern, "count": count})
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    cfg = read_yaml(args.config)
    car_cfg = read_yaml("configs/car_t.yaml")
    log = setup_logger("car_t_raw_read_screen")

    tables = Path(cfg["paths"]["results_tables"])
    reports = Path("results/reports")
    reports.mkdir(parents=True, exist_ok=True)

    roots = [(ROOT / Path(p)) for p in car_cfg["car_t"]["raw_read_roots"]]
    patterns = list(car_cfg["car_t"]["raw_read_patterns"])
    inventory = inventory_files(roots, patterns)
    inventory_path = tables / "car_t_raw_read_inventory.csv"
    inventory.to_csv(inventory_path, index=False)

    reference_panel = ROOT / Path(car_cfg["car_t"]["reference_panel_fasta"])
    metadata_table = ROOT / Path(car_cfg["car_t"]["reference_panel_metadata"])
    total_raw_reads = int(inventory.loc[inventory["pattern"].isin(["*.bam", "*.cram", "*.fastq", "*.fastq.gz", "*.fq", "*.fq.gz"]), "count"].sum())
    reference_exists = reference_panel.exists()

    command_script = reports / "car_t_raw_read_commands.sh"
    command_script.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                "# Optional CAR raw-read screening skeleton.",
                f"REF_PANEL='{reference_panel.as_posix()}'",
                "READS_DIR='data/raw/gdc/files'",
                "OUT_DIR='results/car_t_screen'",
                "mkdir -p \"$OUT_DIR\"",
                "",
                "# Uncomment after providing a validated CAR reference FASTA and raw BAM/CRAM/FASTQ files.",
                "# bwa index \"$REF_PANEL\"",
                "# bwa mem \"$REF_PANEL\" sample_R1.fastq.gz sample_R2.fastq.gz | samtools view -bS - > \"$OUT_DIR/sample.cart.bam\"",
                "# samtools sort -o \"$OUT_DIR/sample.cart.sorted.bam\" \"$OUT_DIR/sample.cart.bam\"",
                "# samtools index \"$OUT_DIR/sample.cart.sorted.bam\"",
                "# samtools view \"$OUT_DIR/sample.cart.sorted.bam\" | awk '$6 ~ /S/' > \"$OUT_DIR/sample.softclipped.sam\"",
            ]
        ),
        encoding="utf-8",
    )

    md = f"""# CAR Raw-Read Screening Skeleton

Date: 2026-04-20
Project: multiomics-ov-network

## Current Status

- Raw-read/alignment file count across configured roots: {total_raw_reads}
- CAR reference FASTA present: {"yes" if reference_exists else "no"}
- CAR architecture metadata table present: {"yes" if metadata_table.exists() else "no"}

## Interpretation

The workflow skeleton is ready, but the current workspace remains blocked for direct CAR/transgene screening because sequence-level inputs are absent.

## Inventory Summary

{inventory.to_markdown(index=False)}

## Expected Inputs For Future Execution

1. A validated custom CAR reference FASTA assembled from approved public sources or user-supplied constructs.
2. Raw BAM, CRAM, or FASTQ files from a CAR-relevant sequencing dataset.
3. Alignment and junction-support criteria defined in `configs/car_t.yaml`.

## Recommended Screening Logic

1. Inventory raw files and verify read modality.
2. Align reads against the CAR reference panel.
3. Flag high-confidence CAR evidence using split/soft-clipped support, junction-spanning reads, and unique mapping quality.
4. Summarize sample-level detection with manual review of candidate alignments.

## Generated Assets

- `results/tables/car_t_raw_read_inventory.csv`
- `results/reports/car_t_raw_read_commands.sh`
- `results/reports/car_t_raw_read_screening_plan.md`
"""
    plan_path = reports / "car_t_raw_read_screening_plan.md"
    plan_path.write_text(md, encoding="utf-8")
    log.info("Wrote %s, %s, and %s", inventory_path, command_script, plan_path)


if __name__ == "__main__":
    main()
