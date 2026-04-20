# External SRA Manifest

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
