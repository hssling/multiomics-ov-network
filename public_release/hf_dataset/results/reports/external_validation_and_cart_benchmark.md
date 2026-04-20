# External Validation and Direct CAR Benchmark

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
