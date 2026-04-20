#!/usr/bin/env bash
set -euo pipefail

# Optional CAR raw-read screening skeleton.
REF_PANEL='D:/Ovarian cancer network analysis/multiomics-ov-network/references/car_t/public_car_panel.fasta'
READS_DIR='data/raw/gdc/files'
OUT_DIR='results/car_t_screen'
mkdir -p "$OUT_DIR"

# Uncomment after providing a validated CAR reference FASTA and raw BAM/CRAM/FASTQ files.
# bwa index "$REF_PANEL"
# bwa mem "$REF_PANEL" sample_R1.fastq.gz sample_R2.fastq.gz | samtools view -bS - > "$OUT_DIR/sample.cart.bam"
# samtools sort -o "$OUT_DIR/sample.cart.sorted.bam" "$OUT_DIR/sample.cart.bam"
# samtools index "$OUT_DIR/sample.cart.sorted.bam"
# samtools view "$OUT_DIR/sample.cart.sorted.bam" | awk '$6 ~ /S/' > "$OUT_DIR/sample.softclipped.sam"