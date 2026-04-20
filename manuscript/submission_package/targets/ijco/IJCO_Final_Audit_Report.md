# IJCO Final Audit Report

Date: 2026-04-20  
Project: `multiomics-ov-network`  
Target journal package: IJCO

## 1. Scope-to-Results Traceability
- Objective: multi-omics integration (mutation/CNA/methylation/RNA/protein optional) -> Implemented and reported.
- Objective: MOFA-like + DIABLO-like integration -> Implemented and reported.
- Objective: multi-layer network hub detection -> Implemented and reported.
- Objective: perturbation and sensitivity analyses -> Implemented and reported.
- Objective: input-output experiments and advanced ML evidence -> Implemented and reported.

Status: PASS

## 2. Core Quantitative Consistency Checks
- Core matched cohort: 90
- Protein-matched cohort: 57
- All-sample top AUC: RNA modules 0.613 (95% CI 0.489-0.737)
- All-sample top Cox C-index: CNA 0.616 (95% CI 0.534-0.699)
- Protein-matched top AUC: integrated-no-protein 0.575 (95% CI 0.423-0.729)
- Advanced ML top AUC: XGBoost 0.526 (95% repeated-CV CI 0.445-0.649)
- Permutation p-value (XGBoost): 0.2745

Status: PASS

## 3. Figure/Table Asset Integrity
Required core and advanced figures/tables verified in `results/` and referenced in manuscript.

Status: PASS

## 4. Scientific Claims Audit
- Strong claims restricted to robust network/sensitivity evidence.
- Predictive discrimination interpreted conservatively due to modest advanced ML and non-significant permutation result.
- Causality language constrained to DAG-style computational orientation, not biological proof.

Status: PASS

## 5. Reproducibility and Public Availability
- GitHub repository updated.
- Kaggle dataset and kernel updated.
- Hugging Face dataset updated.

Status: PASS

## 6. Residual Risks
1. Single-cohort design without external cohort validation.
2. Matched-sample attrition limits power for some subgroup analyses.
3. Final journal formatting checks (word count/figure limits) still needed before upload.

Overall audit decision: READY FOR FINAL SUBMISSION PACKAGE FINALIZATION.

