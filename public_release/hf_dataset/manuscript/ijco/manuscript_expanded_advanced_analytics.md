# Expanded Manuscript Draft: Advanced Evidence Layer

## Scope Fit
This expanded version stays within the current TCGA-OV manuscript scope by adding formal PCA structure evidence, advanced ML benchmarking, DAG-style pathway analysis, perturbation sensitivity curves, and input-output ablation experiments.

## New Results to Add
1. PCA evidence:
- Summarize layer-wise variance concentration from `results/tables/pca_summary.csv`.
- Add PCA plots generated under `results/tables/pca_*.png`.

2. Advanced ML evidence:
- Include `results/tables/advanced_ml_benchmark.csv`.
- Add `results/figures/advanced_ml_benchmark_auc_ci.png`.

3. Input-output experiments:
- Include `results/tables/input_output_ablation_auc.csv`.
- Add `results/figures/input_output_ablation_top_auc.png`.

4. Causal pathway and DAG interpretation:
- Include DAG table `results/networks/dag_pathways.csv`.
- Include pathway strength summary `results/tables/causal_pathway_strength_summary.csv`.
- Add `results/figures/dag_pathway_graph.png`.

5. Sensitivity analysis:
- Include perturbation fraction grid `results/tables/sensitivity_perturb_fraction_grid.csv`.
- Include slope robustness table `results/tables/sensitivity_hub_slope_summary.csv`.
- Add `results/figures/sensitivity_perturbation_curves.png`.

6. Inferential support:
- Include permutation test `results/tables/permutation_test_auc.csv`.

## Suggested Figure Additions
- Figure 7: Multilayer network map (`results/figures/multilayer_network_graph.png`)
- Figure 8: DAG pathway map (`results/figures/dag_pathway_graph.png`)
- Figure 9: Sensitivity curves (`results/figures/sensitivity_perturbation_curves.png`)
- Figure 10: Advanced ML benchmark (`results/figures/advanced_ml_benchmark_auc_ci.png`)
- Figure 11: Input-output ablation top combinations (`results/figures/input_output_ablation_top_auc.png`)

## Suggested Table Additions
- Table 6: Advanced ML benchmark with bootstrap CIs
- Table 7: Input-output ablation combinations and AUC
- Table 8: Causal pathway layer transition strengths
- Table 9: Perturbation sensitivity slope summary
- Table 10: Permutation test for best model

