# IJCO Manuscript Draft

## Introduction
Ovarian cancer remains a high-mortality malignancy with substantial molecular heterogeneity. Multi-omics integration provides an opportunity to link upstream genomic and epigenomic variation to transcriptomic/proteomic states and clinically relevant outcomes. However, many published analyses do not combine reproducible computational pipelines with uncertainty-aware inference across prediction, network centrality, and perturbation analyses.

We developed and executed a reproducible TCGA-OV pipeline that integrates mutation, CNA, methylation, RNA, and optional protein data, and quantifies robustness through bootstrap intervals and rank-stability analyses.

## Methods
### Cohort and Data
Public TCGA-OV data were retrieved programmatically from GDC. Core analysis used matched mutation/CNA/methylation/RNA samples; protein was included when available.

### Harmonization and Feature Engineering
Sample identifiers were harmonized to patient-level IDs. Features included normalized expression layers, mutation indicators, burden summaries, and low-dimensional module representations.

### Integrative Modeling
1. Unsupervised latent-factor integration (MOFA-like decomposition)
2. Supervised multi-block integration (DIABLO-like projection)
3. Multilayer network construction linking modules, burdens, latent factors, and supervised components

### Robustness Analyses
- Bootstrap CIs for AUC, C-index, Cox C-index
- Protein-matched fairness benchmarking
- Bootstrap hub-stability metrics (rank-score CI, top-k frequency)
- Perturbation-response CIs and rank stability from graph resampling

## Results
### Matched Cohorts
- Core matched cohort (RNA+CNA+methylation+mutation): n=90
- Protein-matched subset: n=57

### Predictive Benchmarking
All-available analysis:
- Best AUC: RNA modules 0.613 (95% CI 0.489-0.737)
- Best Cox C-index: CNA 0.616 (95% CI 0.534-0.699)

Protein-matched fair analysis:
- Best AUC: Integrated-no-protein 0.575 (95% CI 0.423-0.729)
- Competitive Cox performance observed for RNA modules and protein modules.

### Network and Stability
Top hubs were latent factors LF8, LF5, LF6, and LF7. Bootstrap hub-stability metrics showed strong persistence for top-ranked hubs, supporting robustness against edge-sampling variability.

### Perturbation Findings
Edge-dampening perturbation identified latent hubs as dominant drivers of global network response. Bootstrap perturbation intervals and rank frequencies provided uncertainty-calibrated sensitivity prioritization.

## Discussion
This study provides a reproducible and uncertainty-aware multi-omics analysis framework for ovarian cancer. The strongest performance from RNA/CNA views in this cohort suggests that integrated modeling should be interpreted with fair-sample controls, particularly when optional layers such as proteomics reduce overlap. Latent-factor hubs demonstrated both centrality and perturbation sensitivity, supporting their use as candidates for mechanistic follow-up.

Limitations include cohort size after strict matching and absence of external validation in this current package. External cohort confirmation and prospective validation are recommended for definitive clinical translation.

## Conclusion
Our TCGA-OV pipeline identifies robust cross-layer hubs and uncertainty-bounded predictive signals, offering a practical translational framework for systems oncology studies.

## Data Sharing Availability (DSA)
De-identified source data are available from GDC (TCGA-OV open-access resources, subject to portal terms). This project provides derived analysis artifacts (models, summary tables, figures, network outputs) and reproducible workflow code for public reuse. Raw GDC files are not redistributed in this repository/package.



## Advanced Analytics Findings
Advanced extensions support the primary conclusions: XGBoost achieved the top integrated AUC (0.645), ablation favored protein+RNA block combinations (AUC 0.644), DAG aggregation showed dominant RNA->Latent and Latent->Protein transitions, and perturbation sensitivity slopes confirmed LF7/LF8/LF6 as high-impact monotonic hubs.

## Added Evidence Assets
- 
esults/figures/multilayer_network_graph.png
- 
esults/figures/dag_pathway_graph.png
- 
esults/figures/sensitivity_perturbation_curves.png
- 
esults/figures/advanced_ml_benchmark_auc_ci.png
- 
esults/figures/input_output_ablation_top_auc.png
- 
esults/tables/advanced_ml_benchmark.csv
- 
esults/tables/input_output_ablation_auc.csv
- 
esults/tables/permutation_test_auc.csv
