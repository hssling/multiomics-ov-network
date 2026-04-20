#!/usr/bin/env bash
set -euo pipefail

# Fill in the validated reference panel before running alignment.
REF=references/car_t/public_car_panel.fasta
OUT=results/intermediate/car_reference_alignment
mkdir -p "$OUT"

# Example indexing commands
"/home/devcontainers/miniconda3/envs/cartalign/bin/bwa" index "$REF"
"/home/devcontainers/miniconda3/envs/cartalign/bin/samtools" faidx "$REF"

# SRR31001810
"/home/devcontainers/miniconda3/envs/cartalign/bin/bwa" mem "$REF" "data/raw/external_validation/car_benchmark/SRR31001810/SRR31001810_1.fastq.gz" "data/raw/external_validation/car_benchmark/SRR31001810/SRR31001810_2.fastq.gz" | "/home/devcontainers/miniconda3/envs/cartalign/bin/samtools" sort -o "$OUT/SRR31001810.bam"
"/home/devcontainers/miniconda3/envs/cartalign/bin/samtools" index "$OUT/SRR31001810.bam"

