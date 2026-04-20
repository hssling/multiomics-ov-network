# Title
Uncertainty-Aware Multi-Omics Integration Reveals Stable Cross-Layer Hubs and Perturbation-Sensitive Network Architecture in TCGA Ovarian Cancer

# Running Title
TCGA-OV Multi-Omics Network Hubs

# Structured Abstract
## Background
Ovarian cancer is biologically heterogeneous, and multi-omics integration is attractive because it can connect genomic and epigenomic inputs to transcriptomic, proteomic, and phenotypic outputs. However, many published analyses emphasize single-model performance while giving less attention to uncertainty, cross-method robustness, and perturbation behavior. We developed a reproducible public-data pipeline to identify the most defensible cross-layer signals in TCGA ovarian cancer (TCGA-OV).

## Methods
Public TCGA-OV mutation, copy-number alteration (CNA), DNA methylation, RNA expression, clinical, and optional protein data were harmonized at patient level. Core analyses used matched mutation, CNA, methylation, and RNA data; protein was analyzed in a fairness-restricted matched subset. We applied MOFA-like latent integration, DIABLO-like supervised multiblock modeling, multilayer network construction, hub ranking, and in silico hub perturbation. Additional evidence layers included DAG-style pathway orientation, perturbation-fraction sensitivity experiments, input-output ablation, and repeated stratified cross-validation confidence intervals for advanced machine learning (ML). A permutation test compared the best advanced-ML model against shuffled-label null performance.

## Results
The core matched cohort included 90 patients; the protein-matched subset included 57 patients. In all-available benchmarking, RNA modules achieved the highest AUC (0.613, 95% CI 0.489-0.737), whereas CNA achieved the highest Cox C-index (0.616, 95% CI 0.534-0.699). Mutation-only features showed poor discrimination (AUC 0.378). In protein-matched fair benchmarking, integrated-no-protein achieved the highest AUC (0.575, 95% CI 0.423-0.729). Across bootstrap centrality analyses, LF8, LF5, LF6, and LF7 were the most stable hubs, each with top-k frequencies of at least 0.995. Perturbation sensitivity slopes ranked LF7, LF8, LF6, and LF5 as the strongest monotonic high-impact hubs. DAG aggregation showed dominant RNA->Latent transitions (40 edges; mean absolute weight 0.441) followed by Latent->Protein transitions (16 edges; mean absolute weight 0.350). In advanced ML, XGBoost had the highest AUC (0.526, 95% repeated-CV CI 0.445-0.649), but permutation testing showed limited separation from null labels (p=0.2745). The strongest ablation result was the RNA-module plus protein-module combination (AUC 0.644).

## Conclusions
The most robust evidence in TCGA-OV arises from cross-layer network structure, hub stability, and perturbation response rather than from high predictive discrimination. This framework supports mechanistic hypothesis generation and translational prioritization while maintaining conservative claims about immediate clinical prediction.

# Keywords
Ovarian cancer; TCGA; multi-omics; systems oncology; network biology; perturbation analysis; reproducible research

# Key Points
- Question: Which omics signals in TCGA-OV remain convincing after uncertainty calibration, cross-method triangulation, and perturbation analysis?
- Findings: Stable latent hubs dominated centrality, bootstrap, and sensitivity analyses, while predictive discrimination remained modest and permutation-calibrated.
- Meaning: The paper’s strongest contribution is a reproducible network-centered evidence framework that prioritizes biologically coherent, perturbation-sensitive candidate hubs for downstream validation.

# Plain-Language Summary
1. We combined several public ovarian cancer data types from the same patients, including DNA changes, RNA patterns, and proteins where available.
2. We found a small group of signals, especially LF7, LF8, LF6, and LF5, that repeatedly acted as important hubs in the network.
3. When we simulated weakening those hubs, the network changed in a consistent and measurable way.
4. The prediction models were only moderately accurate, so the main value of this study is better biological understanding rather than a ready-to-use clinical test.
5. Because the workflow is reproducible, other groups can reuse it, challenge it, and extend it to new ovarian cancer cohorts.

# Introduction
Ovarian cancer remains one of the most lethal gynecologic malignancies, largely because diagnosis is often delayed and biologic heterogeneity complicates prognosis and treatment stratification [1]. High-grade serous ovarian cancer in particular exhibits extensive chromosomal instability, widespread copy-number alteration, epigenomic deregulation, transcriptional reprogramming, and clinically relevant pathway diversity [1]. This makes ovarian cancer an appropriate setting for multi-omics integration, where the goal is not merely to aggregate many data types, but to reconstruct how upstream molecular alterations are transmitted across regulatory layers to produce downstream biological states and clinical phenotypes [2-11].

Several methodological frameworks already support this type of analysis. MOFA and related latent factor approaches are useful for identifying hidden sources of coordinated cross-omics variation [5,6], while DIABLO and related supervised multi-block methods aim to discriminate predefined groups while preserving covariance structure across data views [7,8]. These frameworks are powerful, but their application in the literature often leaves a practical gap between computational output and publication-grade evidence. In particular, many studies report one favored model, one performance estimate, or one network without systematically quantifying uncertainty, checking whether the same hubs remain important across methods, or testing whether perturbing those hubs produces stable downstream consequences.

That gap matters because ovarian cancer multi-omics cohorts are constrained by sample attrition, missing layers, and outcome ambiguity. When sample matching becomes strict, point estimates alone become fragile. A modest AUC can be mistakenly overinterpreted, while a reproducible network signal may be undervalued if it is not framed clearly enough. In translational oncology, these are different kinds of evidence and they should not be treated as interchangeable. A classifier with limited discrimination should not be promoted as clinically ready, but a stable cross-layer hub that survives centrality analysis, bootstrap resampling, perturbation experiments, and pathway-orientation checks may still represent a valuable mechanistic target.

This study was designed around that distinction. Using public TCGA-OV data, we built an end-to-end reproducible workflow to evaluate multi-omics evidence at three levels. First, we assessed predictive and survival-oriented performance across individual omics blocks and integrated representations. Second, we identified network hubs and quantified how stable they remained across bootstrap resampling and alternative graph-derived views. Third, we tested whether those hubs produced consistent downstream shifts under computational perturbation and whether the inferred architecture preserved biologically sensible directionality from RNA to latent and protein layers.

The objective was not to maximize a single headline metric. The objective was to identify which findings remain defensible when examined from multiple complementary angles. Accordingly, this manuscript is organized around a publication-level evidentiary question: what is genuinely strong in this TCGA-OV multi-omics analysis, what is only suggestive, and how should those findings be communicated in a scientifically disciplined way?

# Methods
## Study Design and Data Sources
This was a retrospective computational study using public de-identified datasets. TCGA-OV data were accessed programmatically through the Genomic Data Commons (GDC) [2,3]. Supporting context and optional extension resources included cBioPortal and the Proteomic Data Commons (PDC) [9-11]. No direct human-subject intervention occurred. The study focused on public data only and preserved raw source files as immutable artifacts within the workflow.

## Cohort Construction and Sample Matching
Sample matching was performed at the patient level using TCGA barcode harmonization. Five principal data domains were considered: RNA expression, gene-level CNA, DNA methylation, somatic mutation, and proteomic abundance. The available patient counts by layer were 99 for RNA, 99 for CNA, 100 for methylation, 92 for mutation, and 61 for protein. The core intersection across mutation, CNA, methylation, and RNA consisted of 90 patients. Protein-based analyses were performed on a fairness-restricted matched subset of 57 patients after downstream processing.

This matching strategy was chosen deliberately. Multi-omics studies can appear stronger than they are when different models are compared on different effective sample sets. To reduce that risk, all protein-related fair comparisons were performed on the same protein-matched cohort. All-available analyses were still retained because they describe the broader evidence landscape, but they were interpreted separately from the matched subset analyses.

## Data Processing and Feature Engineering
Layer-specific processing was implemented through scripted workflow stages. RNA data were normalized and later summarized into 50 RNA modules to reduce dimensionality while preserving coordinated biological variation. Gene-level CNA data were clipped and standardized, retaining 46,216 features in the matched cohort. DNA methylation data were filtered and summarized into 7,594 features. Mutation data were encoded into 292 binary or burden-like features. Protein abundance data were normalized and summarized into 20 protein modules in the matched protein subset. Additional burden features comprised three compact summaries intended to capture global alteration load.

The feature design reflects a practical tradeoff between biological granularity and statistical stability. Extremely high-dimensional matrices can overwhelm a matched cohort of 90 patients, especially when several views are combined. Module-level representations were therefore emphasized for RNA and protein layers, whereas full or near-gene-level structure was retained where tractable for CNA and methylation.

## Latent and Supervised Multi-Omics Integration
An unsupervised MOFA-like procedure was used to derive latent factors summarizing coordinated structure across omics views [5,6]. These latent factors served both as mechanistic summaries and as intermediate states in the network model. A DIABLO-like supervised multi-block procedure was then used to derive components associated with the modeled outcome grouping [7,8]. In the context of this pipeline, latent and supervised representations were not treated as competing outputs; rather, they provided complementary views of cross-layer organization.

## Network Construction and Hub Ranking
A multilayer graph was assembled to represent relationships across input and intermediate blocks, linking DNA-level features, RNA modules, latent factors, protein modules, and outcome-related nodes. Hub importance was ranked using degree, betweenness, and PageRank-derived signals [13]. Because single centrality statistics can overemphasize one graph property, a combined rank score and bootstrap-based stability analysis were used to identify nodes that remained consistently prominent under resampling.

## Perturbation and Sensitivity Analysis
Top-ranked hubs were perturbed through edge-weight dampening. The primary perturbation summary was the change in global PageRank distribution measured as an L1 difference, along with hub-specific PageRank changes. Bootstrap estimates were used to generate confidence intervals for perturbation effect size and hub rank behavior. To move beyond one perturbation strength, a perturbation-fraction grid from 0.1 to 0.9 was used to estimate slope-based sensitivity and to check whether the response was monotonic. Monotonic high-impact hubs were interpreted as stronger intervention candidates than hubs that appeared important only at a single arbitrary perturbation fraction.

## Advanced Evidence Layer
Four additional analyses were used to test whether the core signal pattern persisted under different formulations.

1. Input-output ablation experiments assessed how combinations of omics blocks performed relative to individual blocks.
2. DAG-style pathway orientation summarized directional transition strength between layers.
3. Advanced ML benchmarking compared logistic regression, elastic net, random forest, and XGBoost in the matched integrated setting.
4. A label permutation test measured whether the best observed advanced-ML discrimination materially exceeded the null expectation generated by shuffled labels.

These analyses were not intended to create a second paper inside the first one. Their role was calibration: if a finding remained coherent across these orthogonal checks, it became more credible.

## Statistical Reporting and Interpretation
Discrimination and time-to-event performance were summarized with AUC, concordance index, and Cox C-index together with resampling-based uncertainty intervals. We prioritized effect sizes, confidence intervals, and internal consistency across analytic layers rather than threshold-only declarations. This was especially important because the sample size, while adequate for exploratory systems-level analysis, is modest for high-confidence predictive claims.

# Results
## Cohort Yield and Data Sufficiency
Strict matching retained 90 patients across the four core layers and 57 in the processed protein-matched subset. This is an analytically workable but not large cohort, and it defines the evidentiary ceiling for any supervised claim. The layer structure of the matched cohort was still informative. RNA retained 50,422 features before module compression, CNA retained 46,216 features, methylation retained 7,594 features, mutation retained 292 features, and the derived module/burden summaries created compact views suitable for integration. These counts indicate that the workflow preserved substantial biological detail while still allowing dimensional reduction where needed.

The attrition pattern itself is informative. RNA, CNA, and methylation were available in nearly all candidate cases, mutation was somewhat less complete, and protein availability was the main limiting factor. This justified the staged design of the study: first establish a strong four-layer core analysis, then examine whether protein augments or changes the signal pattern in a fairness-controlled subset.

## Single-Block and Integrated Predictive Landscape
The all-available benchmarking results showed a clear pattern. RNA modules achieved the highest AUC at 0.613 (95% CI 0.489-0.737), suggesting that transcriptomic structure carried the strongest discriminative information among the tested blocks. CNA produced the highest Cox C-index at 0.616 (95% CI 0.534-0.699), indicating that copy-number structure may better preserve survival-related ranking information than the other individual views in this cohort. Integrated-no-protein features performed similarly on AUC at 0.579 (95% CI 0.468-0.702), but they did not decisively surpass RNA alone. Methylation showed near-chance discrimination, and mutation-only features performed poorly, with an AUC of 0.378.

This pattern matters for interpretation. It argues against a simplistic narrative in which "more omics automatically means better prediction." In this study, the predictive landscape was uneven. Some layers were clearly more informative than others, and the integrated representation did not dominate every endpoint. RNA modules emerged as the strongest discriminative single block, whereas CNA aligned better with survival-oriented ranking. Mutation-only modeling, in contrast, appeared too sparse or too weakly aligned with the selected outcome representation to serve as a strong stand-alone predictor here.

## Protein-Matched Fair Benchmarking
When the analysis was restricted to the protein-matched subset, the comparative picture shifted. Integrated-no-protein reached the highest AUC at 0.575 (95% CI 0.423-0.729), whereas integrated-with-protein and protein-modules alone remained near 0.48. The important point is not that protein lacked biological value. The important point is that under strict matched-sample comparison, inclusion of the available protein features did not immediately translate into stronger supervised discrimination. That is precisely why fairness-controlled analyses were necessary: without them, one might incorrectly conclude that protein-based integration added predictive value simply because of a different sample set.

The protein results also suggest a more nuanced interpretation. Protein may contribute more clearly at the network and pathway levels than as a direct driver of discrimination in this particular matched cohort. This view is reinforced by the ablation and DAG analyses discussed below.

## Stable Cross-Layer Hubs
The strongest and most internally consistent results emerged from hub analysis. LF8, LF5, LF6, and LF7 occupied the top positions in bootstrap centrality stability, with top-k frequencies of 1.0, 1.0, 0.995, and 1.0, respectively. Their bootstrap mean rank scores were high, and their confidence intervals remained well above those of lower-priority nodes. This is an unusually coherent signal for a public multi-omics analysis: the same latent nodes persisted as dominant hubs across repeated resampling.

The dominance of latent hubs rather than raw mutation or methylation features is biologically plausible. Latent factors are expected to capture shared variation propagated from multiple upstream sources, so they can act as convergence points where regulatory signals become coordinated and therefore network-visible. The ranking of RNA modules immediately below the top latent hubs strengthens this interpretation. The network is not dominated by arbitrary isolated features; it is structured around intermediate states that appear to organize broad transcriptomic and, secondarily, proteomic behavior.

## Perturbation Response Identifies High-Impact Nodes
Static centrality can identify influential nodes, but perturbation analysis tests whether those nodes actually matter dynamically within the graph structure. At the primary perturbation fraction of 0.5, LF7, LF6, LF8, and LF5 produced some of the largest global PageRank shifts, with delta-global values around 0.049 to 0.054. Bootstrap summaries showed that these signals were not artifacts of a single graph realization. LF5 showed the highest top-5 frequency under perturbation ranking (0.72), while LF6 and LF7 also remained prominent.

The sensitivity analysis across perturbation fractions strengthened this result. LF7 had the largest global sensitivity slope (0.127), followed closely by LF8 (0.123), LF6 (0.113), and LF5 (0.110). All four showed monotonic non-decreasing response across the perturbation gradient. This is a stronger evidentiary pattern than a single centrality score because it indicates that the system reacts to increasing perturbation of these hubs in a graded and directionally stable way. In practical terms, these nodes are the most convincing candidates for downstream intervention-focused validation.

## Directional Network Architecture
DAG-style aggregation revealed a concentrated pathway structure. The dominant transition was RNA->Latent, with 40 edges and a mean absolute weight of 0.441. The next strongest transition was Latent->Protein, with 16 edges and a mean absolute weight of 0.350. There was also a direct Latent->Outcome connection represented by a smaller number of edges but a substantial mean signed weight.

This architecture supports a coherent biologic narrative. The model is not implying that RNA literally causes latent factors in a mechanistic sense; rather, it indicates that transcript-level organization is strongly coupled to the latent space recovered by integration, and that this latent space then connects meaningfully to downstream protein variation. In publication terms, this is important because it converts what could have been a set of disconnected statistical outputs into a layered systems picture: upstream alterations are expressed through RNA-level organization, stabilized into latent states, and partially transmitted into the protein layer.

## Input-Output Ablation Clarifies Complementarity
Ablation analyses provided one of the clearest signals about what integration is and is not adding. The best-performing combination was the RNA-module plus protein-module set, with an AUC of 0.644 in the protein-matched cohort. This was meaningfully better than either RNA modules alone (0.417) or protein modules alone (0.489). By contrast, burden features contributed less when added to the RNA-protein pair, reducing AUC to 0.560.

This is a useful result because it distinguishes complementarity from generic accumulation of features. Not every additional block improved performance. The combination that helped most was specifically the transcript-protein pair, consistent with the DAG signal showing strong RNA-to-latent and latent-to-protein coupling. In other words, the ablation analysis and the pathway-orientation analysis point in the same direction.

## Advanced ML as a Calibration Layer
Advanced ML benchmarking showed modest discrimination overall. XGBoost performed best with an AUC of 0.526 (95% repeated-CV CI 0.445-0.649), followed closely by elastic net and random forest. Logistic regression underperformed relative to these methods. On its own, an AUC in this range would not support a strong predictive manuscript claim. The permutation test confirmed that caution. The observed XGBoost AUC of 0.526 was only modestly above the null mean of 0.466, and the right-tail permutation p-value was 0.2745.

That result does not invalidate the entire analysis. It clarifies its center of gravity. The advanced-ML layer functions here as a calibration device, showing that the dataset does not support aggressive claims about predictive readiness. This is scientifically valuable because it prevents a common failure mode in computational oncology, where modest predictive signals are promoted more strongly than the evidence permits.

# Discussion
The principal contribution of this study is not the identification of a high-accuracy predictor. It is the demonstration that a public, reproducible TCGA-OV workflow can generate a stable, interpretable, and uncertainty-aware network map in which a small set of latent hubs repeatedly emerge as dominant cross-layer control points. That distinction is important. In systems oncology, mechanistic robustness and predictive discrimination are related but not identical goals. A cohort can contain biologically meaningful structure even when classifier performance remains moderate.

Three features of the evidence make the hub-centric interpretation convincing. First, the dominant hubs remained stable across bootstrap centrality analysis rather than appearing in a single deterministic ranking. Second, those same hubs produced the largest and most monotonic perturbation responses across a range of intervention strengths. Third, the broader architecture around them was biologically coherent, with transcript-level structure feeding into latent organization and then into the protein layer. These are independent lines of support that converge on the same signal pattern.

The manuscript therefore supports a layered evidentiary model. At the weakest level are isolated predictive metrics that do not survive broader calibration. At an intermediate level are input-output associations that suggest potentially informative combinations, such as RNA modules plus protein modules. At the strongest level are latent hubs whose importance is reproduced by network ranking, bootstrap stability, perturbation response, and pathway-oriented aggregation. A publication-grade interpretation should weight these layers accordingly rather than presenting all results as equally mature.

The comparative performance results also help answer a practical question that frequently remains implicit in multi-omics studies: which layer is actually carrying the signal? In this dataset, RNA modules were the strongest discriminative block, whereas CNA appeared more informative for survival ranking. Methylation and mutation were weaker in direct supervised use, at least in the current representations. This does not imply that methylation and mutation are biologically unimportant. Rather, it suggests that their effect may be indirect, distributed, or more visible once transmitted into shared latent or transcriptomic states than when modeled as isolated high-dimensional predictors.

The protein results deserve similarly careful interpretation. Protein did not improve the fairness-restricted integrated benchmark when inserted naively into a supervised comparison. Yet the best ablation result was the RNA-protein pair, and the pathway summary showed strong latent-to-protein connectivity. Together, these findings suggest that protein contributes interpretively and relationally, even if it does not immediately improve every predictive model. In a translational context, this is still important, because protein-level confirmation can strengthen biological plausibility and sharpen candidate prioritization.

The advanced-ML analysis was intentionally included as a check on overreach. XGBoost, elastic net, and random forest all produced only modest AUC values, and the permutation test did not show strong separation from null labels. That is the correct place to stop the predictive claim. The paper becomes stronger, not weaker, by stating this clearly. Scientific credibility is improved when the manuscript distinguishes robust mechanistic findings from results that remain exploratory.

This point is particularly relevant for publication strategy. A manuscript aimed at a clinically oriented oncology journal must not oversell prediction if the uncertainty intervals and permutation analysis do not support it. What the present study can credibly claim is different and, in many ways, more interesting: it identifies a short list of cross-layer hubs that are stable under multiple analytical stress tests and that therefore warrant orthogonal validation in laboratory or external cohort settings.

## Scientific Interpretation of the Leading Hubs
Although the latent factors are abstract model-derived constructs rather than named genes, their persistent ranking is not a weakness. In integrated multi-omics analysis, latent factors often capture shared biology that is diffused across many measured variables. The recurrence of LF7, LF8, LF6, and LF5 indicates that a small number of integrated axes organize much of the downstream network behavior. From a publication standpoint, these axes should be treated as candidate regulatory states. The next translational step is to map their strongest contributing features and pathways, then validate whether perturbing those pathways produces concordant biologic effects.

This hub interpretation is more rigorous than elevating whichever gene happened to have the largest single coefficient in one predictive model. Coefficients can be unstable in matched multi-omics settings. By contrast, a node that repeatedly ranks highly under centrality analysis, remains prominent under bootstrap resampling, and drives monotonic network change when perturbed has passed a more meaningful robustness screen.

## Strengths
This work has several strengths. It uses public data only, allowing transparent reproducibility. It applies complementary unsupervised, supervised, network, perturbation, and calibration analyses rather than relying on a single analytic lens. It separates all-available analyses from fairness-restricted matched comparisons, reducing hidden sample-composition bias. Most importantly, it reports uncertainty in a way that materially changes interpretation rather than merely decorating point estimates.

## Limitations
The limitations are equally clear. This remains a single-cohort study. Strict matching reduced the effective cohort size, especially for protein analyses. The latent hubs are computational constructs and not yet experimentally anchored to specific causal pathways. DAG-style orientation is useful for systems interpretation but does not prove causality. Finally, the modeled outcome representation may not capture the full clinical complexity of ovarian cancer, and stronger predictive performance may require additional cohort depth, refined labels, or external validation datasets.

## Translational Implications
For clinicians, the immediate message is restrained: this study does not yield a bedside-ready predictor. For translational researchers, however, it produces a sharper asset: a prioritized set of cross-layer hubs and module relationships that are repeatedly supported by the available evidence. For computational oncology groups, it provides a practical reporting template in which prediction, network inference, and uncertainty calibration are integrated rather than treated as disconnected outputs.

## Future Directions
The next phase should focus on three things. First, the strongest latent hubs should be decomposed into their highest-loading genes, pathways, and molecular contributors so that wet-lab validation becomes feasible. Second, the full workflow should be applied to an external ovarian cancer cohort or proteogenomic companion dataset to assess reproducibility beyond TCGA-OV. Third, future manuscripts may separate the network-mechanism story from the predictive benchmarking story if external validation materially improves the latter.

# Conclusions
This TCGA-OV public-data study shows that the most compelling evidence in ovarian cancer multi-omics integration may come from stable cross-layer network architecture rather than from headline classifier performance. RNA modules carried the strongest discriminative signal, CNA carried the strongest survival-ranking signal, and a compact set of latent hubs dominated centrality, perturbation, and sensitivity analyses. The resulting evidence base supports publication as a mechanistic, uncertainty-aware systems oncology study and provides a disciplined foundation for downstream translational validation.

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
13. Hagberg AA, Schult DA, Swart PJ. Exploring network structure, dynamics, and function using NetworkX. In: Proceedings of the 7th Python in Science Conference; 2008. p. 11-15.
