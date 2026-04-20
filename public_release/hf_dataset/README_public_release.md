# Multiomics OV Public Release

This Hugging Face package contains publication-ready derived outputs from the TCGA-OV multi-omics network analysis together with the current preferred Journal of Biomedical Informatics manuscript bundle.

## Current release notes

- Preferred manuscript bundle updated to the Journal of Biomedical Informatics package
- JBI main manuscript now includes the required statement-of-significance table
- JBI main manuscript reduced to a compliant `<=8` combined tables/figures in the main paper
- in-text table/figure callout order and reference first-appearance order were corrected
- graphical abstract refreshed
- CAR motif benchmark notes clarified to explain heuristic zero-count rows

## Contents
- results/models/*: latent and supervised model outputs
- results/tables/*: matched sample, benchmark, perturbation, external validation, and CAR benchmark summaries
- results/networks/*: network edges and centrality tables
- results/figures/*: manuscript/report figures
- metadata/manifests/*: reproducible GDC query templates
- manuscript/*: journal-specific submission bundles, with JBI as the preferred current package

## Data policy
- Public-source data only.
- Raw GDC downloads are not redistributed here.
- Release contains derived, analysis-ready artifacts and reproducibility metadata.
- No engineered CAR construct FASTA panel is included.

## License
For code/data licensing, see repository license and manuscript declarations.
