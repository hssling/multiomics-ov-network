# Immune-Receptor Proxy Analysis

Date: 2026-04-20
Project: multiomics-ov-network

## Scope

This branch estimates immune-receptor and immune-context proxy scores from TCGA-OV RNA expression.
It does not reconstruct TCR or BCR clonotypes and does not claim sequence-level receptor discovery.

## Feasible With Current Data

- T-cell infiltration proxy scoring
- cytolytic activity proxy scoring
- interferon/antigen-presentation proxy scoring
- exhaustion/regulatory marker scoring
- B-cell/plasma-cell proxy scoring

## Not Feasible With Current Data

- clonotype reconstruction
- paired receptor chain recovery
- CAR transgene detection

## Output Files

- `results/tables/immune_receptor_proxy_scores.csv`
- `results/tables/immune_receptor_proxy_summary.csv`
- `results/figures/immune_receptor_proxy_heatmap.png`
- `results/figures/immune_receptor_proxy_by_risk.png`
