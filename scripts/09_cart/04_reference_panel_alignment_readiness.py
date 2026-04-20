from __future__ import annotations

import os
import subprocess
import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


def find_fastqs(root: Path) -> list[Path]:
    fastqs: list[Path] = []
    for pattern in ("*.fastq.gz", "*.fastq", "*.fq.gz", "*.fq"):
        fastqs.extend(sorted(root.rglob(pattern)))
    seen = set()
    unique = []
    for path in fastqs:
        key = str(path.resolve())
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


def tool_status(name: str) -> dict[str, str]:
    exe = shutil.which(name)
    return {"component": f"tool:{name}", "status": "ready" if exe else "missing", "detail": exe or "not found in PATH"}


def linux_executable_exists(path_str: str) -> bool:
    if os.name != "nt" or not path_str.startswith("/"):
        return False
    cmd = ["wsl", "-d", "Ubuntu", "bash", "-lc", f'test -x "{path_str}"']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def configured_tool_status(name: str, configured_path: str | None) -> dict[str, str]:
    if configured_path:
        path = Path(configured_path)
        if path.exists() or linux_executable_exists(configured_path):
            return {"component": f"tool:{name}", "status": "ready", "detail": configured_path}
        return {"component": f"tool:{name}", "status": "missing", "detail": f"{configured_path} not found"}
    return tool_status(name)


def file_status(label: str, path: Path) -> dict[str, str]:
    detail = str(path.relative_to(ROOT)) if path.exists() else f"{path.relative_to(ROOT)} not found"
    return {"component": label, "status": "ready" if path.exists() else "missing", "detail": detail}


def main() -> None:
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("cart_reference_alignment_readiness")

    cart_cfg = cfg["car_t"]
    tables_dir = ROOT / cfg["paths"]["results_tables"]
    reports_dir = ROOT / "results" / "reports"
    tables_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    panel_fasta = ROOT / cart_cfg["reference_panel_fasta"]
    panel_readme = ROOT / cart_cfg["reference_panel_readme"]
    panel_metadata = ROOT / cart_cfg["reference_panel_metadata"]
    readiness_csv = ROOT / cart_cfg["readiness_table"]
    readiness_md = ROOT / cart_cfg["readiness_report"]
    commands_sh = ROOT / cart_cfg["readiness_commands"]
    alignment_cfg = cart_cfg.get("alignment", {})
    bwa_path = alignment_cfg.get("bwa_path")
    samtools_path = alignment_cfg.get("samtools_path")
    minimap2_path = alignment_cfg.get("minimap2_path")

    fastqs: list[Path] = []
    for raw_root in [ROOT / p for p in cart_cfg["raw_read_roots"]]:
        if raw_root.exists():
            fastqs.extend(find_fastqs(raw_root))

    rows = [
        file_status("reference_panel_fasta", panel_fasta),
        file_status("reference_panel_readme", panel_readme),
        file_status("reference_panel_metadata", panel_metadata),
        {
            "component": "raw_fastq_inventory",
            "status": "ready" if fastqs else "missing",
            "detail": f"{len(fastqs)} FASTQ files discovered across configured roots" if fastqs else "no FASTQ inputs discovered",
        },
        configured_tool_status("bwa", bwa_path),
        configured_tool_status("samtools", samtools_path),
        configured_tool_status("minimap2", minimap2_path),
    ]
    df = pd.DataFrame(rows)
    df.to_csv(readiness_csv, index=False)

    benchmark_fastqs = [p for p in fastqs if "SRR31001810" in str(p)]
    bwa_cmd = bwa_path or "bwa"
    samtools_cmd = samtools_path or "samtools"
    command_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "# Fill in the validated reference panel before running alignment.",
        "REF=references/car_t/public_car_panel.fasta",
        "OUT=results/intermediate/car_reference_alignment",
        'mkdir -p "$OUT"',
        "",
        "# Example indexing commands",
        f'"{bwa_cmd}" index "$REF"',
        f'"{samtools_cmd}" faidx "$REF"',
        "",
    ]
    for fastq in sorted(benchmark_fastqs):
        if not fastq.name.endswith("_1.fastq.gz"):
            continue
        mate2 = fastq.with_name(fastq.name.replace("_1.fastq.gz", "_2.fastq.gz"))
        sample = fastq.name.replace("_1.fastq.gz", "")
        if mate2.exists():
            command_lines.extend([
                f"# {sample}",
                f'"{bwa_cmd}" mem "$REF" "{fastq.relative_to(ROOT).as_posix()}" "{mate2.relative_to(ROOT).as_posix()}" | "{samtools_cmd}" sort -o "$OUT/{sample}.bam"',
                f'"{samtools_cmd}" index "$OUT/{sample}.bam"',
                "",
            ])
    commands_sh.write_text("\n".join(command_lines) + "\n", encoding="utf-8")

    blockers = df[df["status"] != "ready"]
    overall = "ready" if blockers.empty else "blocked"
    report = f"""# CAR Reference Alignment Readiness

Date: 2026-04-20
Project: multiomics-ov-network

## Purpose

This report prepares the direct CAR benchmark branch for future alignment against a validated public reference panel.
It does not perform alignment unless the required panel and tools are available.

## Overall status

- Status: **{overall}**

## Current checks

{df.to_markdown(index=False)}

## Benchmarked raw-read inputs

- FASTQ files discovered: {len(fastqs)}
- SRR31001810 paired FASTQ files discovered: {len(benchmark_fastqs)}

## Required next actions

1. Place a validated public reference panel at `references/car_t/public_car_panel.fasta`.
2. Confirm provenance for each reference entry in `results/tables/car_t_architecture_metadata.csv`.
3. Ensure the configured `bwa` and `samtools` executables are installed and executable.
4. Review the generated shell template at `results/reports/cart_reference_alignment_commands.sh` before execution.

## Interpretation boundary

No construct-level recovery claim should be made from this branch until a validated reference panel has been provided and an alignment-based analysis has been completed and audited.
"""
    readiness_md.write_text(report, encoding="utf-8")
    log.info("Wrote %s", readiness_csv)
    log.info("Wrote %s", readiness_md)
    log.info("Wrote %s", commands_sh)


if __name__ == "__main__":
    main()
