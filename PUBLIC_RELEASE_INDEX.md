# Public Release Index

This file is the landing page for the currently published public assets.

## Repository

- GitHub: `https://github.com/hssling/multiomics-ov-network`

## Datasets

- Kaggle dataset: `https://www.kaggle.com/datasets/jkhospital/tcga-ov-multiomics-network-derived-results`
- Hugging Face dataset: `https://huggingface.co/datasets/hssling/tcga-ov-multiomics-network-derived-results`

## Kaggle notebooks

- Advanced evidence notebook package:
  - `public_release/kaggle_kernel/tcga_ov_multiomics_advanced.ipynb`
- CAR scaffold notebook package:
  - `public_release/kaggle_kernel/car_scaffold/kernel-metadata.json`
  - `public_release/kaggle_kernel/car_scaffold/tcga_ov_car_panel_scaffold.ipynb`
- Host-alignment CAR benchmark notebook package:
  - `public_release/kaggle_kernel/host_alignment_car/kernel-metadata.json`
  - `public_release/kaggle_kernel/host_alignment_car/tcga_ov_host_alignment_car_benchmark.ipynb`

## Safe CAR benchmark scope

Included:
- metadata-only CAR panel scaffold
- public benchmark QC and readiness outputs
- host-alignment-only notebook

Not included:
- engineered CAR construct FASTA
- de novo construct generation
- construct-level recovery workflows

## Core local reports

- `results/reports/github_release_note_car_scaffold.md`
- `results/reports/car_t_public_panel_scaffold.md`
- `results/reports/cart_reference_alignment_plan.md`
