# Multiomics OV Public Release

This Kaggle package contains publication-ready derived outputs from the TCGA-OV multi-omics network analysis together with the current preferred Journal of Biomedical Informatics manuscript bundle.

## Current release notes

- Preferred manuscript bundle updated to the Journal of Biomedical Informatics package
- JBI main manuscript now includes the required statement-of-significance table
- JBI main manuscript reduced to a compliant `<=8` combined tables/figures in the main paper
- in-text table/figure callout order and reference first-appearance order were corrected
- graphical abstract refreshed
- CAR motif benchmark notes clarified to explain heuristic zero-count rows

## Preferred manuscript package
- `manuscript/journal_of_biomedical_informatics/`: primary current submission package
- `manuscript/ijco/` and `manuscript/british_journal_of_cancer/`: archived journal-specific variants

## Contents
- results/models/*: latent and supervised model outputs
- results/tables/*: matched sample, benchmark, perturbation, external validation, and CAR benchmark summaries
- results/networks/*: network edges and centrality tables
- results/figures/*: manuscript and report figures
- results/reports/*: external validation and CAR benchmark narrative outputs
- references/car_t/*: metadata-only scaffold for approved external CAR reference panels
- metadata/manifests/*: reproducible GDC query templates
- manuscript/journal_of_biomedical_informatics/*: JBI manuscript package and graphical abstract
- `public_release/kaggle_kernel/tcga_ov_car_panel_scaffold.ipynb`: notebook demonstrating the CAR scaffold workflow
- `public_release/kaggle_kernel/tcga_ov_host_alignment_car_benchmark.ipynb`: notebook demonstrating the host-alignment-only CAR benchmark workflow

## Data policy
- Public-source data only.
- Raw GDC downloads are not redistributed here.
- Release contains derived, analysis-ready artifacts and reproducibility metadata.
- No engineered CAR construct FASTA panel is included.

## License
For code/data licensing, see repository license and manuscript declarations.
