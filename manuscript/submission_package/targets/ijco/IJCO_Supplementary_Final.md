# Supplementary Appendix (Final)

## S1. Reproducibility and Workflow
- Workflow orchestration: `workflow/Snakefile`
- Deterministic seed usage in config and scripts
- Stage-wise logging under `results/tables/log_*.txt`
- Public-release packaging for Kaggle and Hugging Face

## S2. Advanced Analytics Methods
### S2.1 Repeated-CV Advanced ML
Advanced ML benchmarking used repeated stratified cross-validation for AUC confidence intervals in a small matched cohort (`n=57`), with XGBoost configured for resource-aware RTX GPU usage and fallback behavior.

### S2.2 DAG Pathway Orientation
DAG-style pathways were derived from the integrated network by orienting edges according to layer order (Input -> RNA -> Latent -> Protein -> Outcome) and summarizing transition counts/weights.

### S2.3 Sensitivity Grid
Perturbation fractions from 0.1 to 0.9 were applied to top hubs; global-response slopes and monotonicity status were computed for each hub.

### S2.4 Input-Output Ablation
Ablation enumerated omics block combinations and assessed discrimination (AUC) to evaluate marginal and synergistic signal contribution.

## S3. Supplementary Figures
- S1: `results/figures/multilayer_network_graph.png`
- S2: `results/figures/dag_pathway_graph.png`
- S3: `results/figures/sensitivity_perturbation_curves.png`
- S4: `results/figures/advanced_ml_benchmark_auc_ci.png`
- S5: `results/figures/input_output_ablation_top_auc.png`
- S6-S10: PCA view plots in `results/tables/pca_*.png`

## S4. Supplementary Tables
- S1: `results/tables/model_benchmark.csv`
- S2: `results/tables/model_benchmark_protein_matched.csv`
- S3: `results/networks/network_centrality_stability.csv`
- S4: `results/tables/perturbation_delta.csv`
- S5: `results/tables/sensitivity_perturb_fraction_grid.csv`
- S6: `results/tables/sensitivity_hub_slope_summary.csv`
- S7: `results/tables/advanced_ml_benchmark.csv`
- S8: `results/tables/input_output_ablation_auc.csv`
- S9: `results/tables/permutation_test_auc.csv`
- S10: `results/tables/causal_pathway_strength_summary.csv`
- S11: `results/tables/pca_summary.csv`

