# Title
Uncertainty-Aware Multi-Omics Integration and Multi-Layer Network Perturbation in TCGA Ovarian Cancer: A Reproducible Public-Data Study

# Running Title
TCGA-OV Multi-Omics Network Perturbation

# Structured Abstract
## Background
Integrated ovarian cancer multi-omics studies often report model performance without full uncertainty calibration for prediction, network stability, and perturbation response. We developed a reproducible end-to-end public-data framework to identify robust cross-layer hubs in TCGA ovarian cancer (TCGA-OV).

## Methods
Public TCGA-OV mutation, copy-number alteration (CNA), DNA methylation, RNA expression, clinical, and optional protein data were harmonized at patient level. We applied MOFA-like latent integration, DIABLO-like supervised multiblock integration, multilayer network analysis, and in silico hub perturbation. Additional evidence layers included DAG-style pathway orientation, perturbation-fraction sensitivity curves, input-output ablation experiments, and repeated stratified cross-validation confidence intervals for advanced machine learning (ML). A permutation test evaluated whether the best ML model outperformed shuffled-label null performance.

## Results
The core matched cohort (RNA+CNA+methylation+mutation) included 90 patients; the protein-matched subset included 57 patients. In all-available benchmarking, RNA modules achieved the highest AUC (0.613, 95% CI 0.489-0.737), while CNA achieved the highest Cox C-index (0.616, 95% CI 0.534-0.699). In protein-matched fair benchmarking, integrated-no-protein yielded the highest AUC (0.575, 95% CI 0.423-0.729). Stable top hubs were LF8, LF5, LF6, and LF7. Sensitivity slopes ranked LF7/LF8/LF6 as strongest monotonic high-impact hubs. DAG aggregation showed dominant RNA->Latent (40 edges) and Latent->Protein (16 edges) transitions. Advanced ML in integrated features showed modest discrimination (top XGBoost AUC 0.526, 95% repeated-CV CI 0.445-0.649), with non-significant permutation separation (p=0.2745).

## Conclusions
This reproducible framework identifies robust cross-layer network hubs and calibrated uncertainty in TCGA-OV. Current evidence is strongest for mechanistic, network-level biological insight and translational hypothesis generation rather than immediate clinical prediction deployment.

# Keywords
Ovarian cancer; TCGA; multi-omics; network biology; perturbation analysis; DAG; reproducible research

# Key Points
- Question: Which omics layers and network hubs remain robust when uncertainty is explicitly quantified?
- Findings: Stable latent hubs persisted across centrality, bootstrap, perturbation-fraction sensitivity, and pathway-orientation analyses, while predictive discrimination remained modest.
- Meaning: The strongest immediate contribution is robust mechanistic evidence for translational follow-up, not stand-alone bedside prediction.

# Plain-Language Summary
1. We combined several public ovarian cancer molecular data types from the same patients.
2. We found a small set of stable "hub" signals (LF7, LF8, LF6) that repeatedly influenced the network.
3. When we simulated perturbations, these hubs consistently caused the largest downstream changes.
4. Prediction models were only moderate, so the strongest message is biological insight and testable hypotheses.
5. The workflow is reproducible and shareable, allowing other teams to validate and extend the findings.

# Introduction
Ovarian cancer remains a high-mortality malignancy with substantial molecular heterogeneity [1]. Multi-omics integration offers a biologically coherent approach to link upstream DNA-level aberrations with transcriptomic and proteomic states and then to clinical outcomes [2-8]. However, many reports still rely on single-model point estimates without explicit calibration of uncertainty across prediction, network stability, and intervention-like perturbation behavior.

This study addresses that gap with an end-to-end reproducible public-data pipeline using TCGA-OV. We integrated mutation, CNA, methylation, RNA, and optional protein layers; learned cross-view latent structure; built supervised multi-block predictors; assembled a multilayer network; and quantified robustness using bootstrap- and repeated-CV-based uncertainty reporting. We then extended evidence with pathway orientation (DAG-style), perturbation-fraction sensitivity analysis, and block-wise input-output ablation.

To improve clarity for broad audiences, we report findings as answers to clinically intuitive questions: (1) what data remain after strict matching, (2) which views best predict outcomes, (3) which hubs are stable across methods, and (4) how strongly does the system respond when those hubs are perturbed.

# Methods
## Study Design and Data Sources
Public de-identified TCGA-OV data were accessed through GDC programmatic retrieval [2,3]. Context and extension sources included cBioPortal and PDC where relevant [9-11]. Core analyses required matched RNA, CNA, methylation, and mutation; protein was included when matched.

## Data Lineage and Reproducibility
Raw downloads were retained as immutable artifacts. Harmonized and processed matrices were generated via scripted stages with explicit logging and configuration control. This design supports reproducibility audits and traceability from source files to final figures/tables.

## Harmonization and Preprocessing
Patient-level harmonization used TCGA barcodes and strict intersection logic for core multi-layer analyses. Layer-specific processing included expression normalization, CNA clipping/z-scoring, methylation filtering and summarization, and mutation encoding as binary and burden-style features. Module-level summaries were generated for RNA/protein to reduce high-dimensional noise and improve interpretability.

## Core Integration Models
1. MOFA-like latent-factor integration to capture shared and view-specific variation [5,6].
2. DIABLO-like supervised N-integration for risk-group discrimination [7,8].
3. Multilayer graph construction with centrality-based hub ranking (degree, betweenness, PageRank) [12,13].

## Perturbation and Sensitivity Framework
Top hubs were perturbed by edge-weight dampening. Outputs included hub-specific and global PageRank deltas with bootstrap confidence intervals. A perturbation-fraction grid (0.1 to 0.9) produced slope-based sensitivity rankings and monotonicity checks.

## Extended Evidence Layer
1. DAG-style pathway orientation from multilayer edges.
2. Input-output ablation across omics block combinations.
3. Advanced ML benchmarking (logistic, elastic net, random forest, XGBoost).
4. Repeated stratified CV AUC confidence intervals.
5. Permutation testing for top advanced-ML model discrimination versus shuffled-label null.

## Statistical Interpretation Principles
Performance was summarized with AUC/C-index/Cox C-index and uncertainty intervals. Because strict matching reduces sample size, effect sizes and uncertainty were prioritized over dichotomous significance-only claims. Protein analyses used fairness-restricted comparisons on the same matched subset.

# Results
## Objective 1: Cohort Matching and Feature Sufficiency
The main matched cohort included 90 patients; the protein-matched subset included 57 patients (Table 1). Feature availability was highest for RNA/CNA, with expected dimensional and coverage constraints in methylation/mutation/protein layers (Table 2). This attrition profile is typical for deep multi-omics matching and was handled prospectively by design.

## Objective 2: Predictive and Survival Benchmarking
In all-available benchmarking, RNA modules yielded the highest AUC (0.613, 95% CI 0.489-0.737), while CNA yielded the highest Cox C-index (0.616, 95% CI 0.534-0.699) (Table 3; Figures 4-5). In protein-matched fair benchmarking, integrated-no-protein showed top AUC (0.575, 95% CI 0.423-0.729) (Table 4; Figures 6-7).

These patterns suggest that model ranking depends on sampling context and matching constraints. Accordingly, we avoid overstatement and emphasize uncertainty-aware comparison.

## Objective 3: Stable Hubs Across Methods
Network analysis identified LF8, LF5, LF6, and LF7 as top hubs with high bootstrap persistence (Tables 5-6; Figure 10). Stability across multiple centrality metrics reduced the likelihood that rankings were metric artifacts. These latent hubs represent cross-layer convergence points and were therefore prioritized for perturbation analysis.

## Objective 4: Perturbation and Sensitivity Evidence
Hub perturbation produced concentrated downstream effects around latent nodes, with stable rank behavior under bootstrap (Table 7; Figure 8). Sensitivity slopes across perturbation fractions identified LF7/LF8/LF6 as strongest monotonic high-impact hubs (Table 8; Figure 12). This monotonic response strengthens their suitability as intervention candidates for downstream biological validation.

## Objective 5: Pathway Orientation and Input-Output Experiments
DAG aggregation showed dominant RNA->Latent transitions (40 edges; mean absolute weight 0.441) and Latent->Protein transitions (16 edges; mean absolute weight 0.350), consistent with coherent cross-layer information flow (Table 13; Figure 11).

Ablation analysis identified protein modules + RNA modules as the highest-AUC combination among tested sets (AUC 0.644), suggesting potential complementarity between transcript and protein module representations (Table 10; Figure 14).

## Objective 6: Advanced ML Calibration
Advanced ML showed modest discrimination on integrated features: XGBoost AUC 0.526 (95% repeated-CV CI 0.445-0.649), elastic net 0.525, random forest 0.523, and logistic 0.458 (Table 9; Figure 13). Permutation testing for XGBoost gave p=0.2745 (Table 12), indicating limited inferential separation from null labels in this cohort.

The overall evidence profile therefore favors robust mechanistic inference over aggressive predictive claims.

# Discussion
This study delivers a reproducible uncertainty-aware systems-oncology framework for TCGA-OV and provides convergent evidence across unsupervised integration, supervised integration, network centrality, perturbation sensitivity, and pathway-orientation analyses. The strongest signals are stable latent hubs and coherent cross-layer transitions rather than high predictive discrimination.

From a translational perspective, this is a meaningful result. In multi-omics oncology, robust mechanism discovery is often a prerequisite for valid predictive translation. Here, hub stability and monotonic perturbation sensitivity provide a defensible shortlist for orthogonal laboratory validation.

The advanced-ML findings are still informative. They show that after strict matching, prediction gains are constrained, and permutation testing discourages overinterpretation. This calibrated reporting is critical to prevent inflation of claims in small-to-moderate matched cohorts.

Objective-wise synthesis supports this interpretation:
1. Layer contribution: RNA modules showed strongest discrimination; CNA showed strongest survival ranking.
2. Cross-method robustness: LF8/LF5/LF6/LF7 remained top hubs with bootstrap support.
3. Perturbation sensitivity: LF7/LF8/LF6 exhibited strongest monotonic system response.
4. Pathway structure: RNA->Latent and Latent->Protein transitions dominated directional flow.
5. Predictive calibration: advanced ML remained moderate and not strongly separated from null in permutation testing.

## Clinical and Translational Interpretation
For clinicians, the immediate value is not a replacement for existing risk tools. Instead, this work provides a conservative, ranked list of molecular control points for future validation. For translational teams, the identified hubs and module-level interactions provide direct candidates for perturbation experiments, expression assays, and pathway-focused follow-up studies.

## Strengths
1. Reproducible, scriptable end-to-end public-data pipeline.
2. Multi-level uncertainty reporting for model performance, hub stability, and perturbation effects.
3. Fairness-restricted protein benchmarking to reduce hidden sample-overlap bias.
4. Cross-method triangulation across latent, supervised, network, and ablation views.

## Limitations
1. Sample attrition under strict multi-layer matching.
2. Single-cohort design without external independent validation.
3. Moderate predictive discrimination in current feature/sampling setting.
4. DAG orientation is computational and hypothesis-generating, not definitive causal proof.

## Future Directions
Priority next steps are external validation in independent ovarian cohorts, standardized proteomic augmentation, and wet-lab follow-up of LF7/LF8/LF6-centered pathways. Prospective evaluation should determine whether these robust mechanistic signals can be translated into clinically meaningful prediction or treatment stratification.

# Conclusions
A reproducible uncertainty-calibrated TCGA-OV multi-omics framework identified stable latent hubs, coherent cross-layer transitions, and high-impact perturbation targets. The current evidence is strongest for biologically grounded hypothesis generation and translational prioritization, with external validation required before clinical deployment claims.

# Declarations
## Ethics Approval and Consent to Participate
Public de-identified datasets were analyzed; no direct human-subject intervention was performed.

## Consent for Publication
Not applicable.

## Competing Interests
The author declares no competing interests.

## Funding
No dedicated project-specific funding declared for this analysis.

## Author Information
Dr Siddalingaiah H S, Professor, Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur.  
Email: hssling@yahoo.com; Phone: 8941087719.  
ORCID: 0000-0002-4771-8285.

## Data Sharing Availability
Source data are available from GDC (TCGA-OV) under portal terms. This project redistributes derived artifacts, scripts, and reproducibility metadata only; raw GDC data are not redistributed in this repository.

# Figure Legends
Figure 1. Graphical abstract and overall study flow.  
Figure 2. MOFA-like latent factor projection.  
Figure 3. DIABLO-like supervised components.  
Figure 4. All-sample AUC benchmark with uncertainty.  
Figure 5. All-sample Cox C-index benchmark with uncertainty.  
Figure 6. Protein-matched AUC benchmark.  
Figure 7. Protein-matched Cox C-index benchmark.  
Figure 8. Perturbation delta-global bootstrap confidence intervals.  
Figure 9. Survival curves for derived risk groups.  
Figure 10. Integrated multilayer network graph.  
Figure 11. DAG-style pathway graph.  
Figure 12. Perturbation-fraction sensitivity curves.  
Figure 13. Advanced ML AUC comparison with repeated-CV confidence intervals.  
Figure 14. Input-output ablation top combinations.

# Table Legends
Table 1. Sample matching summary.  
Table 2. Per-layer feature count summary.  
Table 3. All-sample benchmarking metrics.  
Table 4. Protein-matched fair benchmarking metrics.  
Table 5. Top network centrality hubs.  
Table 6. Hub stability summary.  
Table 7. Perturbation delta and rank stability metrics.  
Table 8. Hub sensitivity slope summary.  
Table 9. Advanced ML benchmark metrics.  
Table 10. Input-output ablation combinations.  
Table 11. PCA variance summary by omics view.  
Table 12. Permutation-test result for top advanced ML model.  
Table 13. DAG pathway transition strength summary.

# References (Vancouver)
1. The Cancer Genome Atlas Research Network. Integrated genomic analyses of ovarian carcinoma. Nature. 2011;474(7353):609-615. doi:10.1038/nature10166.  
2. National Cancer Institute. Genomic Data Commons (GDC) Data Portal [Internet]. Available from: https://portal.gdc.cancer.gov/  
3. National Cancer Institute. GDC API Users Guide: Downloading Files [Internet]. Available from: https://docs.gdc.cancer.gov/API/Users_Guide/Downloading_Files/  
4. Colaprico A, Silva TC, Olsen C, Garofano L, Cava C, Garolini D, et al. TCGAbiolinks: an R/Bioconductor package for integrative analysis of TCGA data. Nucleic Acids Res. 2016;44(8):e71. doi:10.1093/nar/gkv1507.  
5. Argelaguet R, Velten B, Arnol D, Dietrich S, Zenz T, Marioni JC, et al. Multi-Omics Factor Analysis-a framework for unsupervised integration of multi-omics data sets. Mol Syst Biol. 2018;14(6):e8124. doi:10.15252/msb.20178124.  
6. Argelaguet R, Arnol D, Bredikhin D, Deloro Y, Velten B, Marioni JC, et al. MOFA+: a statistical framework for comprehensive integration of multi-modal single-cell data. Genome Biol. 2020;21(1):111. doi:10.1186/s13059-020-02015-1.  
7. Rohart F, Gautier B, Singh A, Le Cao KA. mixOmics: an R package for omics feature selection and multiple data integration. PLoS Comput Biol. 2017;13(11):e1005752. doi:10.1371/journal.pcbi.1005752.  
8. Singh A, Shannon CP, Gautier B, Rohart F, Vacher M, Tebbutt SJ, et al. DIABLO: an integrative approach for identifying key molecular drivers from multi-omics assays. Bioinformatics. 2019;35(17):3055-3062. doi:10.1093/bioinformatics/bty1054.  
9. Cerami E, Gao J, Dogrusoz U, Gross BE, Sumer SO, Aksoy BA, et al. The cBio cancer genomics portal: an open platform for exploring multidimensional cancer genomics data. Cancer Discov. 2012;2(5):401-404. doi:10.1158/2159-8290.CD-12-0095.  
10. Gao J, Aksoy BA, Dogrusoz U, Dresdner G, Gross B, Sumer SO, et al. Integrative analysis of complex cancer genomics and clinical profiles using the cBioPortal. Sci Signal. 2013;6(269):pl1. doi:10.1126/scisignal.2004088.  
11. National Cancer Institute. Proteomic Data Commons (PDC) [Internet]. Available from: https://pdc.cancer.gov/  
12. Cox DR. Regression models and life-tables. J R Stat Soc Series B Stat Methodol. 1972;34(2):187-220.  
13. Hagberg A, Swart P, Chult DS. Exploring network structure, dynamics, and function using NetworkX. In: Proceedings of the 7th Python in Science Conference; 2008. p. 11-15.
