# Multiomics OV Public Release

This folder contains publication-ready derived outputs from the TCGA-OV multi-omics network analysis.

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
