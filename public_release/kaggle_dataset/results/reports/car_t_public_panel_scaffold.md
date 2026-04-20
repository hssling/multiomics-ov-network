# CAR-T Public Panel Scaffold

Date: 2026-04-20
Project: multiomics-ov-network

## Purpose

This project now includes a **public-facing scaffold** for future CAR alignment benchmarking without bundling engineered construct reference sequences.

## Included scaffold assets

- `references/car_t/README.md`
- `references/car_t/reference_panel_manifest_template.csv`
- `references/car_t/public_car_panel.placeholder.txt`
- `results/tables/car_t_architecture_metadata.csv`
- `results/tables/cart_reference_alignment_readiness.csv`
- `results/reports/cart_reference_alignment_plan.md`
- `results/reports/cart_reference_alignment_commands.sh`

## Current status

- Tooling: ready for `bwa`, `samtools`, and `minimap2`
- Raw benchmark reads: available for `SRR31001810`
- Public scaffold: ready
- Approved reference FASTA: not present

## Intended public use

- workflow experimentation
- metadata curation
- readiness validation
- benchmark documentation

## Not supported in this release

- bundled engineered CAR reference sequences
- de novo construct panel generation
- construct-level recovery claims without an approved external panel
