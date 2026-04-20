#!/usr/bin/env bash
set -euo pipefail

# Optional public SRA retrieval plan for external validation and CAR benchmarking datasets.
# Requires NCBI SRA Toolkit in PATH.

mkdir -p data/raw/external_sra

# GSM4877937 | metastatic ovarian cancer TIL RNA-seq | external ovarian immune-context validation
prefetch SRR12971262 --output-directory data/raw/external_sra
fasterq-dump data/raw/external_sra/SRR12971262 -O data/raw/external_sra/SRR12971262

# SRX26389396 | CD22 CAR-T infusion product RNA-seq | direct CAR workflow benchmark
prefetch SRR31001810 --output-directory data/raw/external_sra
fasterq-dump data/raw/external_sra/SRR31001810 -O data/raw/external_sra/SRR31001810

# SRX26517613 | BCMA CAR-T single-cell multi-omics | future CAR/TCR/BCR-aware extension
prefetch SRR31135546 --output-directory data/raw/external_sra
fasterq-dump data/raw/external_sra/SRR31135546 -O data/raw/external_sra/SRR31135546
