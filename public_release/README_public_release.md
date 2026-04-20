# Multiomics OV Public Release

This folder contains publication-ready derived outputs from the TCGA-OV multi-omics network analysis, including the current Journal of Biomedical Informatics submission bundle and public benchmark assets.

## Current release notes

- JBI package is the preferred current manuscript bundle.
- JBI main manuscript now includes the required statement-of-significance table.
- JBI main manuscript was reduced to a compliant `<=8` combined tables/figures in the main paper while preserving detailed supporting material in the supplement.
- in-text citation order for main-manuscript tables and figures was corrected.
- reference first-appearance order was corrected in the JBI manuscript.
- graphical abstract was rebuilt in a cleaner journal-facing format.
- CAR motif benchmark notes now explain why heuristic all-zero rows do not imply construct absence.

## Preferred manuscript package
- `manuscript/journal_of_biomedical_informatics/`: primary current submission bundle
- `manuscript/ijco/` and `manuscript/british_journal_of_cancer/`: preserved prior packages

## Contents
- results/models/*: latent and supervised model outputs
- results/tables/*: matched sample, benchmark, perturbation, external validation, and CAR benchmark summaries
- results/networks/*: network edges and centrality tables
- results/figures/*: manuscript/report figures
- results/reports/*: external validation, benchmark, and audit narratives
- references/car_t/*: metadata-only scaffold for approved external CAR reference panels
- metadata/manifests/*: reproducible GDC query templates
- manuscript/*: journal-specific submission bundles

## Data policy
- Public-source data only.
- Raw GDC downloads are not redistributed here.
- Release contains derived, analysis-ready artifacts and reproducibility metadata.
- No engineered CAR construct FASTA panel is included.

## License
For code/data licensing, see repository license and manuscript declarations.
