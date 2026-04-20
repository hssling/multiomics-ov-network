# CAR Reference Alignment Readiness

Date: 2026-04-20
Project: multiomics-ov-network

## Purpose

This report prepares the direct CAR benchmark branch for future alignment against a validated public reference panel.
It does not perform alignment unless the required panel and tools are available.

## Overall status

- Status: **blocked**

## Current checks

| component                | status   | detail                                                     |
|:-------------------------|:---------|:-----------------------------------------------------------|
| reference_panel_fasta    | missing  | references\car_t\public_car_panel.fasta not found          |
| reference_panel_readme   | ready    | references\car_t\README.md                                 |
| reference_panel_metadata | ready    | results\tables\car_t_architecture_metadata.csv             |
| raw_fastq_inventory      | ready    | 2 FASTQ files discovered across configured roots           |
| tool:bwa                 | ready    | /home/devcontainers/miniconda3/envs/cartalign/bin/bwa      |
| tool:samtools            | ready    | /home/devcontainers/miniconda3/envs/cartalign/bin/samtools |
| tool:minimap2            | ready    | /home/devcontainers/miniconda3/envs/cartalign/bin/minimap2 |

## Benchmarked raw-read inputs

- FASTQ files discovered: 2
- SRR31001810 paired FASTQ files discovered: 2

## Required next actions

1. Place a validated public reference panel at `references/car_t/public_car_panel.fasta`.
2. Confirm provenance for each reference entry in `results/tables/car_t_architecture_metadata.csv`.
3. Ensure the configured `bwa` and `samtools` executables are installed and executable.
4. Review the generated shell template at `results/reports/cart_reference_alignment_commands.sh` before execution.

## Interpretation boundary

No construct-level recovery claim should be made from this branch until a validated reference panel has been provided and an alignment-based analysis has been completed and audited.
