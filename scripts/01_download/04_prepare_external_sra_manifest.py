from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


def main() -> None:
    args = parse_args()
    cfg = read_yaml(args.config)
    ext_cfg = read_yaml(ROOT / "configs" / "external_validation.yaml")
    log = setup_logger("external_sra_manifest")

    tables = Path(cfg["paths"]["results_tables"])
    reports = ROOT / "results" / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(ext_cfg["external_validation"]["sra_datasets"])
    out_csv = tables / "external_sra_manifest.csv"
    df.to_csv(out_csv, index=False)

    shell_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "# Optional public SRA retrieval plan for external validation and CAR benchmarking datasets.",
        "# Requires NCBI SRA Toolkit in PATH.",
        "",
        "mkdir -p data/raw/external_sra",
    ]
    for row in df.to_dict(orient="records"):
        run = row["linked_run"]
        shell_lines.extend(
            [
                "",
                f"# {row['accession']} | {row['context']} | {row['use_case']}",
                f"prefetch {run} --output-directory data/raw/external_sra",
                f"fasterq-dump data/raw/external_sra/{run} -O data/raw/external_sra/{run}",
            ]
        )
    cmd_path = reports / "external_sra_download_commands.sh"
    cmd_path.write_text("\n".join(shell_lines) + "\n", encoding="utf-8")

    md = f"""# External SRA Manifest

Date: 2026-04-20
Project: multiomics-ov-network

## Purpose

This manifest defines three public external datasets selected to strengthen the project in complementary ways:

1. ovarian immune-context validation (`GSM4877937 / SRX9423612 / PRJNA674045`)
2. direct CAR-workflow benchmark (`SRX26389396 / PRJNA1173154`)
3. future single-cell CAR/TCR/BCR extension (`SRX26517613 / PRJNA980643`)

## Output Files

- `results/tables/external_sra_manifest.csv`
- `results/reports/external_sra_download_commands.sh`

## Recommended Priority

1. Validate immune-state interpretations using the ovarian TIL bulk RNA-seq dataset.
2. Benchmark the CAR-alignment workflow on the true CAR-product bulk RNA-seq dataset.
3. Reserve the single-cell CAR multi-omic dataset for a second-stage extension because analysis complexity is substantially higher.
"""
    report_path = reports / "external_sra_manifest.md"
    report_path.write_text(md, encoding="utf-8")
    log.info("Wrote %s, %s, and %s", out_csv, cmd_path, report_path)


if __name__ == "__main__":
    main()

