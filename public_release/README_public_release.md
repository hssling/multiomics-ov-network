# Multiomics OV Public Release

This folder contains publication-ready derived outputs from the TCGA-OV multi-omics network analysis.

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
