# multiomics-ov-network

Reproducible, end-to-end public TCGA ovarian cancer multi-omics pipeline for network modelling, uncertainty-aware benchmarking, external ovarian immune-context validation, and CAR-product benchmarking.

## Current public release

- Preferred manuscript package: `manuscript/submission_package/targets/journal_of_biomedical_informatics/`
- Current compliant main manuscript: JBI package with required statement-of-significance table and `<=8` combined main-manuscript tables/figures
- Public mirrors:
  - GitHub repository: workflow, source code, manuscript assets, and release notes
  - Hugging Face dataset: derived results, public manuscript bundles, and release documentation
  - Kaggle dataset: derived results and notebook-ready public package

## Release notes

Latest refresh highlights:

- JBI submission package rebuilt as the primary submission-grade manuscript bundle
- JBI main manuscript reduced to a compliant `7` combined figure/table objects while retaining the significance table
- in-text table and figure callouts corrected to appear sequentially before captions
- JBI reference first-appearance ordering corrected
- graphical abstract rebuilt in a cleaner, journal-facing layout
- CAR motif benchmark documentation clarified so all-zero heuristic motif rows are not misinterpreted as construct absence
- public release package refreshed to keep GitHub, Hugging Face, and Kaggle outputs aligned

## Scope (first runnable pass)
- Cohort: `TCGA-OV`
- Main layers: RNA + CNA + methylation + mutation
- Outcome: survival risk group (median split)
- Models: MOFA2-like latent factors, DIABLO-like supervised components
- Network: multi-layer graph with centrality ranking + in silico perturbation
- Data policy: real public GDC data only (no synthetic fallback)

## Repository Structure

```text
multiomics-ov-network/
+-- data/
+-- metadata/
+-- notebooks/
+-- scripts/
+-- results/
+-- configs/
+-- environment/
+-- workflow/
+-- manuscript/
+-- Snakefile
+-- Makefile
+-- README.md
```

## Environments

- Python: `environment/environment-python.yml`
- R: `environment/environment-r.yml`

Create envs:

```bash
conda env create -f environment/environment-python.yml
conda env create -f environment/environment-r.yml
```

## Run Order

Dry run:

```bash
snakemake -n --cores 1
```

Full run:

```bash
snakemake --cores 4 --rerun-incomplete
```

Make targets:

```bash
make dryrun
make run
make report
make immune
make car_t
```

## Workflow Stages and Scripts

1. Download
- `scripts/01_download/01_gdc_download.py`
- `scripts/01_download/03_fetch_gdc_files.py`
- `scripts/01_download/02_optional_imports.py`
- `scripts/01_download/04_prepare_external_sra_manifest.py` (optional external validation/CAR benchmark manifest)

2. QC / preprocessing
- `scripts/02_qc/01_qc_preprocess.py`

3. Harmonize IDs
- `scripts/03_harmonize/01_harmonize_ids.py`

4. Feature engineering
- `scripts/04_features/01_build_features.py`
- `scripts/04_features/02_immune_receptor_proxy.py` (optional immune-context branch)

5. Integration
- `scripts/05_integration/01_run_mofa.R`
- `scripts/05_integration/02_run_diablo.R`

6. Network
- `scripts/06_network/01_build_network.py`

7. Perturbation
- `scripts/07_perturbation/01_perturbation.py`

8. Reporting
- `scripts/08_reporting/01_generate_report.py`
- `scripts/08_reporting/09_external_validation_and_cart_benchmark.py` (optional external ovarian validation + direct CAR FASTQ benchmark)

9. Optional CAR-T extension
- `scripts/09_cart/01_build_car_t_assets.py`
- `scripts/09_cart/02_screen_car_raw_reads.py`
- `workflow/car_t_raw_read_screening.smk`

## Exact GDC Query Templates

Layer templates are in `metadata/manifests/`:
- `gdc_query_rna.json`
- `gdc_query_cna.json`
- `gdc_query_methylation.json`
- `gdc_query_mutation.json`

Each uses:
- `cases.project.project_id = TCGA-OV`
- layer-specific `data_type`
- `access = open`
- output fields: `file_id,file_name,data_type,data_format,cases.case_id,cases.submitter_id`

## Variable Contracts (key files)

- `data/interim/*_matrix.parquet`
  - required columns: `sample_id`, `patient_id`, feature columns
- `metadata/sample_maps/master_sample_sheet.csv`
  - per-patient layer presence + clinical labels
- `data/processed/outcomes.csv`
  - includes `patient_id`, `days_to_death`, `days_to_last_follow_up`, `vital_status`, `survival_risk_group`
- `results/models/mofa_factors.csv`
  - `patient_id`, `LF1..LFn`
- `results/models/diablo_scores.csv`
  - `patient_id`, `comp1`, `comp2`, `survival_risk_group`
- `results/networks/network_centrality.csv`
  - `node`, `degree`, `betweenness`, `pagerank`, `rank_score`
- `results/tables/perturbation_delta.csv`
  - perturbation impact metrics per hub

## Validation Checks Included

- file existence and stage flags
- per-layer dimensions tracked (`results/tables/feature_count_summary.csv`)
- matched-sample intersection summary (`results/tables/sample_matching_summary.csv`)
- missingness filtering in QC
- ID harmonization via TCGA barcode truncation rules

## Resumability and Reproducibility

- immutable raw data folders under `data/raw/`
- stage completion flags
- deterministic random seed in config (`project.seed`)
- workflow-managed dependencies in Snakemake

## Expected Outputs

Tables:
- `results/tables/sample_matching_summary.csv`
- `results/tables/feature_count_summary.csv`
- `results/tables/perturbation_delta.csv`
- `results/tables/sensitivity_perturb_fraction_grid.csv`
- `results/tables/sensitivity_hub_slope_summary.csv`
- `results/tables/model_benchmark.csv`
- `results/tables/model_benchmark_protein_matched.csv`
- `results/tables/pca_summary.csv`
- `results/tables/advanced_ml_benchmark.csv`
- `results/tables/input_output_ablation_auc.csv`
- `results/tables/permutation_test_auc.csv`
- `results/tables/causal_pathway_strength_summary.csv`

Models:
- `results/models/mofa_factors.csv`
- `results/models/diablo_scores.csv`

Network:
- `results/networks/multilayer_network_edges.csv`
- `results/networks/network_centrality.csv`
- `results/networks/network_centrality_stability.csv`
- `results/networks/dag_pathways.csv`

Figures:
- `results/figures/mofa_factors.png`
- `results/figures/diablo_components.png`
- `results/figures/survival_km.png`
- `results/figures/model_benchmark_auc_ci.png`
- `results/figures/model_benchmark_protein_matched_auc_ci.png`
- `results/figures/model_benchmark_cox_cindex_ci.png`
- `results/figures/model_benchmark_protein_matched_cox_cindex_ci.png`
- `results/figures/perturbation_bootstrap_ci.png`
- `results/figures/multilayer_network_graph.png`
- `results/figures/dag_pathway_graph.png`
- `results/figures/sensitivity_perturbation_curves.png`
- `results/figures/advanced_ml_benchmark_auc_ci.png`
- `results/figures/input_output_ablation_top_auc.png`

Reports:
- `results/reports/final_report.html`
- `manuscript/manuscript_skeleton.md`
- `results/reports/immune_receptor_proxy.md`
- `results/reports/car_t_architecture_summary.md`
- `results/reports/car_t_raw_read_screening_plan.md`

Optional extension outputs:
- `results/tables/car_t_architecture_metadata.csv`
- `results/tables/car_t_raw_read_inventory.csv`
- `results/tables/external_sra_manifest.csv`
- `results/tables/external_cart_dataset_candidates.csv`
- `results/tables/external_validation_file_inventory.csv`
- `results/tables/external_ovarian_immune_scores.csv`
- `results/tables/external_ovarian_immune_summary.csv`
- `results/tables/cart_direct_benchmark_qc.csv`
- `results/tables/immune_receptor_proxy_scores.csv`
- `results/tables/immune_receptor_proxy_summary.csv`
- `results/figures/immune_receptor_proxy_heatmap.png`
- `results/figures/immune_receptor_proxy_by_risk.png`
- `results/figures/external_ovarian_immune_scores.png`
- `results/figures/external_ovarian_immune_heatmap.png`
- `results/reports/external_sra_manifest.md`
- `results/reports/gsm4877937_suitability.md`
- `results/reports/external_validation_and_cart_benchmark.md`

## Notes

- `scripts/02_qc/01_qc_preprocess.py` is strict and parses only downloaded real GDC files; it fails fast when required layers are missing.
- Optional cBioPortal/PDC imports are enabled via `data/raw/cbioportal` and `data/raw/pdc`.
- The CAR-T extension is metadata-first. Direct CAR/transgene screening requires BAM/CRAM/FASTQ plus a validated custom reference FASTA.
- The immune-receptor branch provides expression-level proxy scores only. It is not a clonotype reconstruction workflow.

## CI/CD

- CI pipeline: `.github/workflows/ci.yml`
  - Python syntax smoke checks
  - R script parse checks
- Release pipeline: `.github/workflows/release.yml`
  - Packages `results/` + `manuscript/` as versioned artifacts on tag (`v*`)

## Public Release Targets

- Kaggle package folder: `public_release/kaggle_dataset/`
- Hugging Face package folder: `public_release/hf_dataset/`
- Both contain derived outputs only (no raw GDC redistribution).
- Landing page: `PUBLIC_RELEASE_INDEX.md`

## CAR Scaffold Release

- CAR-related public assets are scaffold-only and metadata-first.
- `references/car_t/` contains:
  - `README.md`
  - `reference_panel_manifest_template.csv`
  - `public_car_panel.placeholder.txt`
- The workflow can benchmark approved external reference panels when supplied later, but no engineered construct FASTA is bundled in this repository.
- Current readiness outputs are in:
  - `results/tables/cart_reference_alignment_readiness.csv`
  - `results/reports/cart_reference_alignment_plan.md`
  - `results/reports/car_t_public_panel_scaffold.md`
- Notebook entry point:
  - `notebooks/tcga_ov_car_panel_scaffold.ipynb`
  - `notebooks/tcga_ov_host_alignment_car_benchmark.ipynb`

## GitHub Release Note

Suggested release message for the current public package:

```text
TCGA-OV multi-omics public release refresh:
- JBI manuscript package added
- CAR benchmark workflow refreshed
- metadata-only CAR panel scaffold added for approved future reference validation
- WSL-backed bwa/samtools/minimap2 readiness audited
- duplicate stale public-release copies cleaned
```
