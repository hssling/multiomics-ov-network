# Title
Uncertainty-Aware Multi-Omics Integration and Multi-Layer Network Perturbation in TCGA Ovarian Cancer: A Reproducible Public-Data Study

# Running Title
TCGA-OV Multi-Omics Network Perturbation

# Structured Abstract
## Background
Integrated ovarian cancer analyses frequently report single-model results without uncertainty calibration across model performance, network stability, and perturbation sensitivity. We developed a reproducible public-data pipeline to quantify robust cross-layer signals in TCGA ovarian cancer (TCGA-OV).

## Methods
Public TCGA-OV mutation, copy-number alteration (CNA), DNA methylation, RNA, clinical, and optional protein data were harmonized at patient level. We applied unsupervised latent integration (MOFA-like factors), supervised multiblock integration (DIABLO-like components), multilayer network construction, and in silico hub perturbation. Evidence was expanded using DAG-style pathway orientation, perturbation-fraction sensitivity experiments, input-output ablation, and advanced machine-learning (ML) benchmarking with repeated stratified cross-validation confidence intervals. A permutation test assessed whether the best advanced-ML discrimination exceeded shuffled-label null performance.

## Results
The core matched cohort (RNA+CNA+methylation+mutation) comprised 90 patients; the protein-matched subset comprised 57 patients. In all-available benchmarking, RNA modules achieved the highest AUC (0.613, 95% CI 0.489-0.737), and CNA achieved the highest Cox C-index (0.616, 95% CI 0.534-0.699). In protein-matched fair benchmarking, integrated-no-protein achieved the highest AUC (0.575, 95% CI 0.423-0.729). Network analysis identified stable top hubs (LF8, LF5, LF6, LF7). Sensitivity slopes across perturbation fractions ranked LF7/LF8/LF6 as strongest monotonic global-response hubs. DAG aggregation showed dominant RNA->Latent transitions (40 edges) and Latent->Protein transitions (16 edges). In advanced ML on integrated features, XGBoost showed top AUC (0.526, 95% repeated-CV CI 0.445-0.649); permutation testing did not show strong statistical separation from null (p=0.2745).

## Conclusions
This reproducible framework identifies robust cross-layer network hubs and calibrated uncertainty for perturbation and prediction in TCGA-OV. Core network findings are stronger than current advanced-ML discrimination, emphasizing mechanistic network evidence over claims of immediate clinical predictive utility.

# Keywords
Ovarian cancer; TCGA; multi-omics; network biology; perturbation analysis; DAG; reproducible research

# Introduction
Ovarian cancer remains a high-mortality disease with clinically important molecular heterogeneity [1]. Multi-omics integration can connect upstream DNA-layer variation to downstream transcriptomic and proteomic states and then to patient-level outcomes [2-8]. However, many analyses still rely on point-estimate performance reporting without uncertainty-aware interpretation across model discrimination, network robustness, and perturbation sensitivity.

This study addresses that gap using a full reproducible public-data workflow. We integrated mutation, CNA, methylation, RNA, and optional protein layers from TCGA-OV; modeled shared structure with unsupervised and supervised multi-omics approaches; and quantified robustness using bootstrap-based hub/perturbation stability plus repeated cross-validation confidence intervals for advanced ML. We further introduced DAG-style pathway orientation and block-level input-output ablation to characterize layer-to-layer signal transfer.

# Methods
## Study Design and Data Sources
Public de-identified TCGA-OV data were accessed through GDC programmatic retrieval [2,3]. Optional context/extension sources included cBioPortal and PDC resources [9-11]. The primary analysis required matched RNA, CNA, methylation, and mutation; protein was analyzed when matched.

## Harmonization, Preprocessing, and Feature Engineering
Patient IDs were harmonized from TCGA barcodes. Layer-specific preprocessing included expression normalization, CNA clipping/z-scoring, methylation filtering/summarization, and mutation binary/burden feature derivation. Module-level representations were generated for RNA/protein to reduce high-dimensional noise.

## Integrative Modeling
1. MOFA-like latent-factor integration to capture cross-view structure [5,6].
2. DIABLO-like supervised multiblock integration for risk-group discrimination [7,8].
3. Multilayer graph assembly with centrality-based hub ranking (degree, betweenness, PageRank) [12,13].

## Perturbation and Sensitivity
Top hubs were perturbed by edge-weight dampening; outcomes included hub-specific and global PageRank deltas with bootstrap uncertainty. A perturbation-fraction grid (0.1 to 0.9) generated slope-based sensitivity rankings and monotonicity checks.

## Advanced Evidence Layer
1. DAG-style pathway orientation from multilayer edges (input->RNA->latent->protein/outcome).
2. Input-output ablation across omics block combinations.
3. Advanced ML benchmarking (logistic, elastic net, random forest, XGBoost).
4. Repeated stratified CV AUC confidence intervals.
5. Label permutation test for the top advanced-ML model.

## Statistical Reporting
Model discrimination is reported as AUC/C-index/Cox C-index with confidence intervals from resampling methods used by each module. Given limited sample size in protein-matched analyses, effect sizes and uncertainty were prioritized over strict dichotomous significance claims.

# Results
## Cohort and Feature Coverage
Main matched cohort size was 90 and protein-matched size was 57 (Table 1). Feature coverage remained high for RNA and CNA with reduced but substantial methylation/mutation coverage (Table 2).

## Core Predictive and Survival Benchmarks
In all-available analysis, RNA modules produced the highest AUC (0.613, 95% CI 0.489-0.737), while CNA produced the highest Cox C-index (0.616, 95% CI 0.534-0.699) (Table 3, Figure 4-5). In protein-matched fair comparison, integrated-no-protein produced the highest AUC (0.575, 95% CI 0.423-0.729) (Table 4, Figure 6-7).

## Network Hub Robustness
Top hubs were LF8, LF5, LF6, and LF7 with high bootstrap persistence (Table 5-6). Perturbation effects concentrated around latent hubs with stable rank behavior (Table 7, Figure 8).

## Sensitivity and DAG Pathway Evidence
Sensitivity slopes across perturbation fractions identified LF7, LF8, and LF6 as strongest monotonic response hubs (Table 8, Figure 12). DAG aggregation indicated dominant RNA->Latent transitions (40 edges; mean absolute weight 0.441) followed by Latent->Protein transitions (16 edges; mean absolute weight 0.350), supporting biologically coherent cross-layer flow (Table 13, Figure 11).

## Advanced ML and Input-Output Experiments
Advanced ML on integrated features showed modest discrimination: XGBoost AUC 0.526 (95% repeated-CV CI 0.445-0.649), elastic net 0.525, random forest 0.523, logistic 0.458 (Table 9, Figure 13). The best ablation combination was protein modules + RNA modules (AUC 0.644) (Table 10, Figure 14). Permutation testing for XGBoost yielded p=0.2745, indicating limited inferential separation from shuffled null labels at current sample size (Table 12).

# Discussion
This study provides a reproducible uncertainty-aware TCGA-OV systems-oncology framework integrating unsupervised structure learning, supervised multi-block integration, network centrality, perturbation stability, and pathway-oriented sensitivity analysis. The strongest evidence in this cohort arises from network-level robustness and perturbation behavior rather than high clinical discrimination from advanced ML.

The advanced-ML results are scientifically informative despite modest AUC values. They show that with strict sample matching and current features, predictive gains are constrained; however, the ablation and DAG analyses still reveal interpretable cross-layer signal architecture, particularly RNA-latent-protein transitions and stable latent hubs. This supports a mechanistic, hypothesis-generating interpretation.

## Strengths
1. Fully scriptable and reproducible public-data pipeline.
2. Multi-level uncertainty reporting (performance, hub stability, perturbation sensitivity).
3. Explicit fairness comparison for protein-matched subsets.
4. Cross-method triangulation: latent integration, supervised integration, graph evidence, and ablation.

## Limitations
1. Sample attrition under strict multi-layer matching.
2. Single-cohort design without external validation.
3. Modest advanced-ML discrimination and non-significant permutation test in current setting.
4. DAG orientation is computationally inferred and not proof of biological causality.

## Translational Implications
The most defensible near-term outputs are robust hub/module candidates for downstream validation rather than direct clinical deployment. LF7/LF8/LF6-centered pathways and RNA-protein module interactions are priority candidates for mechanistic laboratory follow-up.

# Conclusions
A reproducible uncertainty-calibrated TCGA-OV multi-omics framework identifies robust latent hubs and cross-layer pathway architecture. Current evidence supports strong network-level biological insights and moderated claims for clinical prediction, with external validation as the critical next step.

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

