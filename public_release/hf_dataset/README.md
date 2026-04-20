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

## Current status

- Primary manuscript target: Journal of Biomedical Informatics
- Preferred bundle: `manuscript/journal_of_biomedical_informatics/`
- Current JBI main manuscript status:
  - required statement-of-significance table included
  - main-paper combined tables/figures reduced to a compliant `<=8`
  - sequential in-text callouts and corrected reference-order audit completed

## Release notes

- Refreshed JBI submission bundle with compliant main manuscript, declarations, title page, cover letter, checklist, supplement, and graphical abstract
- Clarified CAR motif benchmark interpretation so heuristic all-zero motif rows are not misread as construct absence
- Preserved prior IJCO and BJC bundles for provenance while marking JBI as the active preferred package
- Kept the release derived-only: no raw GDC redistribution and no engineered CAR construct FASTA

## Preferred manuscript package
- `manuscript/journal_of_biomedical_informatics/`: primary current submission-grade package with main manuscript, cover letter, declarations, supplementary appendix, graphical abstract, and submission metadata
- `manuscript/ijco/` and `manuscript/british_journal_of_cancer/`: prior journal-tailored packages retained for provenance

## Included
- `results/models/`: MOFA-like factors, DIABLO-like scores
- `results/tables/`: matching summary, feature counts, benchmark metrics with CIs, perturbation deltas, external validation tables, and CAR benchmark audits
- `results/networks/`: multilayer edges and network centrality/stability
- `results/figures/`: manuscript/report figures
- `results/reports/`: external validation, CAR benchmark, and workflow audit reports
- `references/car_t/`: metadata-only scaffold for user-supplied approved CAR reference panels
- `metadata/manifests/`: GDC query/manifests templates
- `manuscript/journal_of_biomedical_informatics/`: JBI-targeted manuscript and submission bundle
- `public_release/kaggle_kernel/tcga_ov_car_panel_scaffold.ipynb`: notebook demonstrating the CAR scaffold workflow
- `public_release/kaggle_kernel/tcga_ov_host_alignment_car_benchmark.ipynb`: notebook demonstrating the host-alignment-only CAR benchmark workflow

## Not included
- Raw GDC downloads are not redistributed.
- No engineered CAR construct FASTA panel is redistributed.

## Reproducibility
Use the companion repository workflow and scripts to regenerate these artifacts from public TCGA-OV sources.
