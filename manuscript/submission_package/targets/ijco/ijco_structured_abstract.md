# Structured Abstract (IJCO Draft)

## Background
Integrative ovarian cancer studies frequently combine multi-omics layers but often lack complete reproducibility and uncertainty quantification for network and predictive outputs.

## Methods
We developed a reproducible TCGA-OV pipeline integrating somatic mutation, copy-number alteration, DNA methylation, RNA expression, and optional protein expression. Cross-layer structure was modeled with unsupervised latent-factor integration and supervised multi-block projection. We built a multilayer graph and quantified hub importance, bootstrap hub stability, and perturbation responses. Predictive benchmarking included AUC, C-index, and Cox C-index with bootstrap confidence intervals, plus protein-matched fairness comparisons.

## Results
In the core intersection, 90 patients were matched across RNA/CNA/methylation/mutation; 57 were available in the protein-matched subset. In all-available benchmarking, RNA modules achieved the highest AUC (0.613, 95% CI 0.489-0.737), while CNA achieved the highest Cox C-index (0.616, 95% CI 0.534-0.699). In protein-matched fair comparison, integrated-no-protein had the highest AUC (0.575, 95% CI 0.423-0.729). Top network hubs were latent factors LF8, LF5, LF6, and LF7, with high bootstrap persistence. Perturbation analysis identified latent-factor hubs as highest-impact nodes with uncertainty-bounded effect sizes and rank stability.

## Conclusions
A reproducible multi-omics network framework in TCGA ovarian cancer identifies robust cross-layer hubs and uncertainty-calibrated predictive signals, supporting translational hypothesis generation and future external validation.
