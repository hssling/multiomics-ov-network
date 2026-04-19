---
language:
- en
license: cc-by-4.0
tags:
- ovarian-cancer
- multi-omics
- tcga
- systems-biology
- network-analysis
task_categories:
- tabular-classification
- tabular-regression
- text-classification
pretty_name: TCGA-OV Multiomics Network Derived Results
size_categories:
- 10K<n<100K
---

# TCGA-OV Multiomics Network Derived Results

This dataset contains **derived, publication-ready outputs** from a reproducible TCGA-OV multi-omics network analysis pipeline.

## Included
- `results/models/`: MOFA-like factors, DIABLO-like scores
- `results/tables/`: matching summary, feature counts, benchmark metrics with CIs, perturbation deltas
- `results/networks/`: multilayer edges and network centrality/stability
- `results/figures/`: manuscript/report figures
- `metadata/manifests/`: GDC query/manifests templates
- `manuscript/ijco/`: IJCO-targeted manuscript package markdown files

## Not included
- Raw GDC downloads are not redistributed.

## Reproducibility
Use the companion repository workflow and scripts to regenerate these artifacts from public TCGA-OV sources.
