# Title
Stable Cross-Layer Hubs and Perturbation-Sensitive Multi-Omics Network Architecture in TCGA Ovarian Cancer

# Running Title
TCGA-OV Multi-Omics Network Hubs

# Structured Abstract
## Background
Multi-omics ovarian cancer studies often report integrated models without clarifying which findings are truly robust across methods and uncertainty analyses. We developed a reproducible public-data framework to identify the most stable cross-layer signals in TCGA ovarian cancer (TCGA-OV).

## Methods
Public TCGA-OV mutation, copy-number alteration (CNA), DNA methylation, RNA expression, clinical, and optional protein data were harmonized at patient level. Core analyses used matched mutation, CNA, methylation, and RNA data; protein was analyzed in a fairness-restricted subset. We applied MOFA-like latent integration, DIABLO-like supervised integration, multilayer network modeling, hub ranking, computational perturbation, DAG-style pathway aggregation, and repeated resampling for uncertainty calibration.

## Results
The core matched cohort included 90 patients; the protein-matched subset included 57. RNA modules achieved the highest all-available AUC (0.613, 95% CI 0.489-0.737), whereas CNA achieved the highest Cox C-index (0.616, 95% CI 0.534-0.699). In fair protein-matched benchmarking, integrated-no-protein achieved the highest AUC (0.575, 95% CI 0.423-0.729). The most stable hubs were LF8, LF5, LF6, and LF7, each with top-k bootstrap frequencies of at least 0.995. Sensitivity slopes ranked LF7, LF8, LF6, and LF5 as the strongest monotonic perturbation-response hubs. RNA->Latent and Latent->Protein transitions dominated DAG aggregation. Advanced ML remained modest; the top XGBoost AUC was 0.526 and was not clearly separated from shuffled-label null performance (p=0.2745).

## Conclusions
The strongest evidence in TCGA-OV lies in stable network architecture and perturbation-sensitive latent hubs rather than high-confidence clinical prediction. This framework prioritizes biologically coherent candidate control points for downstream validation.

# Keywords
Ovarian cancer; TCGA; multi-omics; network biology; perturbation analysis; reproducible research

# Introduction
Ovarian cancer remains a high-mortality malignancy with substantial molecular heterogeneity, making it a natural target for multi-omics integration [1]. Public resources such as TCGA-OV allow simultaneous analysis of genomic, epigenomic, transcriptomic, and proteomic data, but integrating these layers does not automatically produce reliable biological conclusions [2-11]. In matched multi-omics cohorts, a single strong-looking model can be unstable, and a modest predictive signal can be overstated if uncertainty is not reported carefully.

The central question in this study was therefore not simply whether integrated data could predict an outcome. The more important question was which results remain convincing when the same dataset is examined through complementary analytical views: unsupervised latent integration, supervised multiblock discrimination, multilayer network centrality, perturbation analysis, pathway-oriented aggregation, and calibration by resampling. From a clinical-oncology perspective, that distinction matters. A network hub that remains stable across several stress tests may be more valuable for translational follow-up than a weak classifier with a single favorable point estimate.

Using public TCGA-OV data, we constructed a reproducible pipeline to identify robust cross-layer hubs and to evaluate whether those hubs produce stable downstream changes under computational perturbation. We also compared individual and integrated omics blocks to determine which layers contributed the most to discrimination and survival ranking. The goal was to generate a concise, uncertainty-aware systems-oncology study suitable for clinical oncology readership.

# Patients and Methods
## Study Design and Data Sources
This was a retrospective computational study using public de-identified TCGA-OV data accessed through the GDC [2,3]. Supporting context and optional extension resources included cBioPortal and the Proteomic Data Commons [9-11]. Core analyses required matched RNA, CNA, methylation, and mutation data. Protein was evaluated in a fairness-restricted subset.

## Cohort Matching and Feature Construction
After harmonization of TCGA barcodes, the available patient counts were 99 for RNA, 99 for CNA, 100 for methylation, 92 for mutation, and 61 for protein. The strict intersection across the four core layers yielded 90 patients. After downstream processing, the protein-matched subset included 57 patients. Feature engineering retained 50,422 RNA features, 46,216 CNA features, 7,594 methylation features, and 292 mutation features in the matched cohort. To reduce dimensionality, RNA was summarized into 50 modules, protein into 20 modules, and three burden-style features were computed for mutation, CNA, and methylation.

## Multi-Omics Integration and Network Analysis
Shared cross-layer structure was modeled with a MOFA-like latent-factor approach [5,6], and supervised multiblock integration was modeled using a DIABLO-like framework [7,8]. A multilayer graph was then constructed linking RNA modules, latent factors, protein modules, and outcome-related nodes. Hub importance was ranked using centrality-based measures combined into a bootstrap stability score.

## Perturbation, Pathway Orientation, and Predictive Calibration
Top hubs were perturbed through edge-weight dampening. The primary perturbation summary was the change in global PageRank distribution, together with bootstrap confidence intervals and rank stability measures. A perturbation-fraction grid from 0.1 to 0.9 was used to estimate monotonicity and sensitivity slopes. We further summarized directional pathway structure with DAG-style layer aggregation and assessed supervised performance using AUC, concordance-based metrics, repeated cross-validation, and permutation testing for the best advanced ML model.

# Results
## Matched Cohort and Layer Contribution
Strict matching retained a workable but selective cohort of 90 patients across the four core layers and 57 patients in the processed protein-matched subset. This cohort size is sufficient for exploratory systems analysis but imposes limits on predictive certainty. Among individual views, RNA modules carried the strongest discriminative information, achieving an AUC of 0.613 (95% CI 0.489-0.737). CNA carried the strongest survival-ranking signal, reaching a Cox C-index of 0.616 (95% CI 0.534-0.699). Mutation-only features performed poorly (AUC 0.378), whereas methylation remained near chance in direct discrimination.

This pattern indicates that more omics blocks do not automatically produce better performance. Instead, the predictive contribution of each layer was uneven. Transcript-level organization appeared most informative for discrimination, whereas copy-number structure appeared more informative for survival-oriented ordering.

## Fair Protein-Matched Benchmarking
In the protein-matched subset, integrated-no-protein achieved the highest AUC at 0.575 (95% CI 0.423-0.729). Protein alone and integrated-with-protein remained near 0.48. This fairness-restricted comparison was important because apparent gains from protein integration can otherwise be confounded by sample-composition changes. In the present cohort, protein did not strengthen supervised discrimination by itself, although later analyses suggested that it still contributed biologically meaningful relational information.

## Stable Network Hubs
The most coherent results arose from hub analysis. LF8, LF5, LF6, and LF7 were the dominant bootstrap-stable hubs, with top-k frequencies of 1.0, 1.0, 0.995, and 1.0, respectively. These factors remained prominent across repeated resampling, indicating that the centrality pattern was not driven by a single graph realization.

Because these hubs are latent factors rather than isolated measured genes, they are best interpreted as integrated regulatory states. Their persistence suggests that a small number of cross-layer axes organize much of the network behavior in this cohort.

## Perturbation and Sensitivity Evidence
At a perturbation fraction of 0.5, LF7, LF6, LF8, and LF5 produced the largest global PageRank shifts, with delta-global values around 0.049-0.054. Sensitivity analysis reinforced this result: LF7 had the highest global sensitivity slope (0.127), followed by LF8 (0.123), LF6 (0.113), and LF5 (0.110). All four demonstrated monotonic non-decreasing response across the perturbation gradient. These features make them stronger intervention candidates than nodes that appear influential only in one static ranking.

## Pathway Orientation and Hub Biology
DAG aggregation showed a dominant RNA->Latent transition layer, followed by Latent->Protein transitions. This directional structure supports a coherent systems interpretation in which transcript-level organization strongly feeds the latent space recovered by integration and is then transmitted into downstream protein variation.

Hub interpretation based on the linked module structure further sharpened this signal. LF6 was strongly connected to modules with stromal and extracellular-matrix-associated genes including ADAMTS4, ADAM12, COL12A1, TNC, and COLEC12. LF7 linked to modules containing AFAP1L2, APLP2, L1CAM, RDH10, and CTSV, suggesting an invasion- and adhesion-related program. LF8 was connected to modules containing ONECUT1, L1CAM, MAPT, and GFAP-like neural-lineage features, while LF5 linked to CCNDBP1-associated transcript modules and was the only top hub with a direct negative latent-to-outcome edge. These interpretations are module-derived and hypothesis-generating, but they provide a biologically meaningful bridge from abstract latent factors to candidate pathway content.

## Integrated Block Complementarity and Advanced ML
Input-output ablation showed that the strongest matched-subset combination was the RNA-module plus protein-module block, with an AUC of 0.644. This exceeded either RNA or protein modules alone, suggesting complementarity between transcript and protein summaries even though protein did not improve every direct benchmark.

Advanced ML added calibration rather than stronger prediction. XGBoost had the highest AUC at 0.526 (95% repeated-CV CI 0.445-0.649), followed closely by elastic net and random forest. Permutation testing gave a p-value of 0.2745, indicating that the observed discrimination was not clearly separated from a shuffled-label null. The predictive evidence should therefore be interpreted conservatively.

# Discussion
This study shows that the strongest signal in TCGA-OV multi-omics integration is not a high-accuracy classifier but a stable network architecture centered on a small set of perturbation-sensitive latent hubs. That distinction is essential for a clinical oncology audience. Predictive utility and mechanistic robustness are related but different forms of evidence, and the present dataset supports the latter more strongly than the former.

The robustness of LF8, LF5, LF6, and LF7 was supported in three ways. First, the hubs persisted across bootstrap centrality analyses. Second, they produced the largest and most monotonic network changes under computational perturbation. Third, the layer structure around them was biologically coherent, with strong RNA-to-latent and latent-to-protein transitions and interpretable module-level pathway content. Together, these findings argue that the dominant latent factors are not statistical artifacts but plausible regulatory states that deserve downstream validation.

The comparative modeling results are also informative. RNA modules contributed the strongest discrimination, whereas CNA contributed the strongest survival-ranking signal. Mutation and methylation were weaker in direct supervised modeling, which suggests that their influence may be more distributed and more visible after propagation into shared latent or transcriptomic states. Protein offered its clearest value at the level of cross-layer complementarity and pathway continuity rather than as a stand-alone predictive block.

The advanced-ML analysis usefully limits overinterpretation. Moderate AUC values and a non-significant permutation result do not support aggressive claims about clinical readiness. Instead, the paper’s main translational output is a ranked shortlist of cross-layer candidate hubs and associated module programs for orthogonal testing. In particular, LF6-associated stromal modules and LF7/LF8-associated adhesion or lineage-like signals appear reasonable starting points for functional follow-up.

This study has limitations. It is based on a single public cohort, and strict matching reduced the effective sample size, especially for protein analyses. The latent factors are model-derived constructs rather than experimentally validated pathways. DAG-style orientation is useful for biological organization but does not prove causality. Nevertheless, the study remains valuable because it demonstrates a disciplined way to distinguish strong mechanistic evidence from weaker predictive evidence in a realistic public multi-omics cohort.

# Conclusions
A reproducible TCGA-OV pipeline identified stable cross-layer hubs and perturbation-sensitive network architecture, with the strongest evidence centered on LF8, LF5, LF6, and LF7. RNA modules carried the strongest discriminative signal, CNA carried the strongest survival-ranking signal, and transcript-protein complementarity was supported by ablation analysis. These findings support the use of uncertainty-aware network biology as a translational prioritization strategy in ovarian cancer.

# Acknowledgements
The study used public de-identified resources from the Genomic Data Commons, cBioPortal, and the Proteomic Data Commons.

# Declarations
## Conflict of Interests
The author declares no competing interests.

## Data availability statement
The raw source data are available from the GDC and related public portals under their respective access terms. This repository redistributes derived artifacts, scripts, and reproducibility metadata only. Derived analysis outputs supporting the present manuscript are available in the project workspace and public release bundles.

## Ethics approval, informed consent, and authors’ contribution statements
This study analyzed publicly available de-identified human data and did not involve direct patient contact or new biospecimen collection. Formal institutional ethics approval and participant informed consent were not required for this secondary analysis. The work was conducted in accordance with the ethical principles of the Declaration of Helsinki as applicable to secondary analysis of public de-identified datasets. Author contribution: Dr Siddalingaiah H S conceived the study, oversaw analysis, interpreted results, and prepared the manuscript.

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
13. Hagberg AA, Schult DA, Swart PJ. Exploring network structure, dynamics, and function using NetworkX. In: Proceedings of the 7th Python in Science Conference; 2008. p. 11-15.
