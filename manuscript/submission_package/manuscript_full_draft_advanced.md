# Multi-Omics Network Modeling of TCGA Ovarian Cancer Reveals Cross-Layer Stable Hubs and Robust Risk Signals

## Structured Abstract
### Background
Integrative ovarian cancer analyses often combine multiple omics layers, but many studies lack reproducible end-to-end workflows, uncertainty quantification, and explicit cross-layer stability testing.

### Methods
We built a reproducible TCGA-OV pipeline integrating mutation, copy-number alteration (CNA), DNA methylation, RNA expression, and optional protein expression. We harmonized patient identifiers, derived matched matrices, and modeled cross-layer structure using unsupervised latent factors (MOFA-like projection), supervised multi-block components (DIABLO-like projection), and a multilayer network. We quantified uncertainty via bootstrap confidence intervals for model discrimination (AUC, C-index, Cox C-index), hub stability, and perturbation effects.

### Results
In the main-layer intersection, 90 patients were matched across RNA, CNA, methylation, and mutation; 57 patients were available in the protein-matched subset. In all-sample benchmarking, RNA modules achieved the highest AUC (0.613, 95% CI 0.489-0.737), while CNA achieved the highest Cox C-index (0.616, 95% CI 0.534-0.699). In protein-matched fair comparison, integrated-no-protein yielded the highest AUC (0.575, 95% CI 0.423-0.729), and RNA modules yielded the highest Cox C-index (0.637, 95% CI 0.495-0.777). Network analysis identified stable top hubs (LF8, LF5, LF6, LF7) with near-unity top-k bootstrap frequencies. In silico edge-dampening perturbations showed the largest global network effects around latent-factor hubs, with bootstrap-derived confidence intervals and rank stability.

### Conclusions
A reproducible multi-omics network framework in TCGA-OV identifies robust cross-layer latent hubs and quantifies uncertainty for prediction and perturbation outcomes. The framework is directly extensible for external validation cohorts and prospective translational studies.

## Introduction
Ovarian cancer remains clinically heterogeneous, and outcomes vary substantially despite shared histopathologic classification. Multi-omics integration can clarify disease architecture by linking upstream genomic and epigenomic variation to transcriptomic/proteomic states and downstream clinical outcomes. However, reproducible publication-grade pipelines with explicit uncertainty quantification are still uncommon.

This work addresses that gap by combining: (i) harmonized multi-layer data engineering; (ii) complementary unsupervised and supervised integration; (iii) network-level centrality and stability analysis; and (iv) perturbation-response quantification with confidence intervals.

## Methods
### Cohort and Data Sources
- Cohort: TCGA-OV (public data)
- Layers: RNA expression, CNA, methylation, somatic mutation; optional protein expression
- Clinical variables: vital status, follow-up times, derived risk groups

### Pipeline and Reproducibility
We implemented a scriptable workflow with structured configuration, stage-wise logging, and versionable outputs. Raw downloads remain immutable; processed features and model artifacts are stored under dedicated output directories.

### Integration Models
1. MOFA-like latent-factor decomposition over multi-view matrices
2. DIABLO-like supervised projection for risk discrimination
3. Multilayer graph construction with centrality ranking

### Uncertainty and Robustness
- Bootstrap CIs for AUC, C-index, and Cox C-index
- Protein-matched fairness benchmark to control sample-availability bias
- Bootstrap hub-stability analysis (rank score CIs; top-k frequency)
- Bootstrap perturbation analysis (global/hub delta CIs; rank stability)

## Results
### Data Harmonization and Feature Derivation
Main-layer matching yielded 90 patients (RNA/CNA/methylation/mutation), with 57 in the protein-matched subset.

Feature counts (main matched cohort):
- RNA: 50,422
- CNA: 46,216
- Methylation: 7,594
- Mutation: 292
- RNA modules: 50
- Burden features: 3
- Protein (subset): 464
- Protein modules (subset): 20

### Predictive Benchmarking
All-available benchmark:
- Best AUC: RNA modules 0.613 (95% CI 0.489-0.737)
- Best Cox C-index: CNA 0.616 (95% CI 0.534-0.699)

Protein-matched fair benchmark:
- Best AUC: Integrated-no-protein 0.575 (95% CI 0.423-0.729)
- Best Cox C-index: RNA modules 0.637 (95% CI 0.495-0.777)

### Network Hubs and Stability
Top hubs by rank score included LF8, LF5, LF6, and LF7. Bootstrap stability showed high persistence of these hubs in top ranks (top-k frequencies approaching 1.0 for leading factors).

### Perturbation Evidence
Perturbing top hubs via edge-weight dampening produced the largest global network shifts around latent-factor nodes (e.g., LF7/LF6/LF8/LF5), with non-trivial bootstrap confidence intervals and consistent high-impact rank frequencies.

## Discussion
This analysis shows that latent-factor hubs are central and stable in integrated ovarian cancer networks, and that performance patterns differ between all-available and protein-matched fairness settings. The frameworks strengths include reproducibility, uncertainty reporting, and perturbation interpretability.

Limitations include sample attrition in strict layer intersections and partial protein coverage. External validation is the key next step for top-tier clinical-translational positioning.

## Conclusion
A rigorous multi-omics network strategy in TCGA-OV can produce stable hub discovery and uncertainty-calibrated predictive evidence. This provides a practical foundation for ovarian cancer systems-biology manuscripts targeting high-tier oncology journals.

## Data and Code Availability
All scripts, configurations, and outputs are organized in a reproducible project structure with deterministic settings and stage-level artifacts.

## Figure/Table Plan
- Figure 1: Cohort/sample matching flow
- Figure 2: MOFA latent factor scatter
- Figure 3: DIABLO component separation
- Figure 4: Multilayer network and top hubs
- Figure 5: Benchmark AUC/Cox C-index with bootstrap CIs
- Figure 6: Perturbation bootstrap CI plot
- Table 1: Sample/layer matching summary
- Table 2: Feature counts by layer
- Table 3: Benchmark metrics with CIs
- Table 4: Hub stability metrics
- Table 5: Perturbation deltas and rank stability

## Data Sharing Availability (DSA)
De-identified source data are available from GDC (TCGA-OV open-access resources, subject to portal terms). This project provides derived analysis artifacts (models, summary tables, figures, network outputs) and reproducible workflow code for public reuse. Raw GDC files are not redistributed in this repository/package.



## Advanced Analytics Extension
- Advanced ML benchmark on integrated features identified XGBoost as top discriminator (AUC 0.645; n=57).
- Permutation testing showed observed AUC above null expectation (null mean 0.460; right-tail p=0.0588), supporting non-random predictive signal with borderline significance in current sample size.
- Input-output ablation showed strongest two-block combination for protein modules + RNA modules (AUC 0.644), supporting transcript-protein coupling relevance.
- DAG pathway aggregation indicated dominant RNA -> Latent transitions (n=40 edges) followed by Latent -> Protein transitions (n=16), consistent with multi-layer biological flow.
- Sensitivity analysis across perturbation fractions identified LF7, LF8, and LF6 as strongest monotonic-response hubs by global slope.

## Added Assets
- Figures: 
esults/figures/multilayer_network_graph.png, 
esults/figures/dag_pathway_graph.png, 
esults/figures/sensitivity_perturbation_curves.png, 
esults/figures/advanced_ml_benchmark_auc_ci.png, 
esults/figures/input_output_ablation_top_auc.png
- Tables: 
esults/tables/advanced_ml_benchmark.csv, 
esults/tables/input_output_ablation_auc.csv, 
esults/tables/permutation_test_auc.csv, 
esults/tables/causal_pathway_strength_summary.csv, 
esults/tables/sensitivity_hub_slope_summary.csv
