# Title
Uncertainty-Aware Multi-Omics Integration Reveals Stable Cross-Layer Hubs and Perturbation-Sensitive Network Architecture in TCGA Ovarian Cancer

# Structured Abstract
## Background
Integrated ovarian cancer multi-omics studies often report model performance without showing which signals remain stable across analytic methods and uncertainty checks. We developed a reproducible public-data framework to identify the most defensible cross-layer findings in TCGA ovarian cancer (TCGA-OV).

## Methods
Public TCGA-OV mutation, copy-number alteration (CNA), DNA methylation, RNA expression, clinical, and optional protein data were harmonized at patient level. Core analyses used matched mutation, CNA, methylation, and RNA data; protein was analyzed in a fairness-restricted subset. We applied MOFA-like latent integration, DIABLO-like supervised multiblock modeling, multilayer network analysis, computational perturbation, DAG-style pathway aggregation, input-output ablation, and repeated resampling for uncertainty calibration.

## Results
The core matched cohort included 90 patients; the protein-matched subset included 57. RNA modules achieved the highest all-available AUC (0.613, 95% CI 0.489-0.737), whereas CNA achieved the highest Cox C-index (0.616, 95% CI 0.534-0.699). In protein-matched fair benchmarking, integrated-no-protein achieved the highest AUC (0.575, 95% CI 0.423-0.729). Stable top hubs were LF8, LF5, LF6, and LF7, each with top-k frequencies of at least 0.995. Sensitivity slopes ranked LF7, LF8, LF6, and LF5 as the strongest monotonic perturbation-response hubs. RNA->Latent and Latent->Protein transitions dominated pathway aggregation. Advanced ML discrimination remained modest; the best XGBoost AUC was 0.526 and was not clearly separated from shuffled-label null performance (p=0.2745). Hub-linked module summaries implicated extracellular-matrix and stromal programs around LF6, adhesion and invasion-related signals around LF7, lineage-like transcript-protein signals around LF8, and a negative latent-to-outcome edge centered on LF5.

## Conclusions
The most robust evidence in TCGA-OV lies in stable cross-layer network architecture and perturbation-sensitive latent hubs rather than in high-confidence clinical prediction. This framework prioritizes biologically coherent candidate control points for downstream validation.

# Introduction
Ovarian cancer remains one of the most lethal gynecologic malignancies, in large part because clinically relevant heterogeneity is embedded across multiple molecular layers [1]. The ovarian tumors profiled by TCGA are characterized by extensive copy-number abnormality, epigenetic deregulation, coordinated transcriptional change, and downstream proteomic heterogeneity [1]. These features make ovarian cancer a strong candidate disease for multi-omics systems analysis. Yet the central challenge is not the availability of many data types; it is determining which conclusions are sufficiently robust to justify translational interpretation.

That challenge becomes more acute when strict patient matching is imposed. The effective cohort size falls, some molecular layers become incomplete, and predictive point estimates can become unstable. In this setting, a publication-grade multi-omics paper should not be built around a single favorable classifier result. Instead, it should distinguish clearly between evidence for prediction and evidence for mechanism. A modest predictive signal may still be useful, but a network hub that remains stable across centrality analysis, bootstrap resampling, pathway summarization, and perturbation stress testing may represent a more reproducible biological finding.

The present study was designed around that principle. Using public TCGA-OV data, we built a reproducible workflow that combines latent integration, supervised multiblock discrimination, multilayer network analysis, perturbation modeling, input-output ablation, and advanced ML calibration. Rather than asking only whether integrated omics can predict an outcome, we asked which layers contribute signal, which hubs remain stable, how the network responds when those hubs are perturbed, and whether the resulting structure is biologically coherent across RNA, latent, and protein levels.

For a broad oncology readership, the goal is twofold. First, to identify high-priority molecular control points that warrant validation. Second, to show how uncertainty-aware reporting changes interpretation in a realistic public multi-omics cohort.

# Methods
## Study design and data sources
This was a retrospective computational study based on public de-identified datasets. TCGA-OV data were accessed through the Genomic Data Commons [2,3], with contextual support from cBioPortal and the Proteomic Data Commons where relevant [9-11]. No direct human-subject intervention was performed. Raw files were retained as immutable artifacts in the workflow, and all processed matrices were generated in scripted stages.

## Cohort construction and feature engineering
TCGA barcodes were harmonized at patient level. Available patient counts by layer were 99 for RNA, 99 for CNA, 100 for methylation, 92 for mutation, and 61 for protein. The strict four-layer intersection across RNA, CNA, methylation, and mutation yielded 90 patients. After processing, the protein-matched subset contained 57 patients.

Matched feature counts were 50,422 for RNA, 46,216 for CNA, 7,594 for methylation, and 292 for mutation. RNA was compressed into 50 module scores, protein into 20 module scores, and three burden-like summaries were derived from mutation, CNA, and methylation. This representation was chosen to balance biological detail against statistical tractability in a matched cohort of modest size.

## Integration, network construction, and perturbation
Shared cross-omics structure was modeled using a MOFA-like latent-factor approach [5,6]. A DIABLO-like supervised multiblock model was used to recover components associated with the outcome grouping [7,8]. A multilayer graph was then assembled linking RNA modules, latent factors, protein modules, and outcome-related nodes. Hub importance was ranked using combined centrality measures, followed by bootstrap stability analysis.

Top hubs were perturbed by edge-weight dampening. Network response was summarized by the change in global PageRank distribution together with hub-specific changes, bootstrap confidence intervals, and rank-stability statistics. A perturbation-fraction grid from 0.1 to 0.9 was used to evaluate whether hub effects increased monotonically with perturbation strength.

## Additional evidence layers
To test whether the principal network findings remained coherent under orthogonal formulations, we added four analyses: (1) DAG-style layer aggregation, (2) input-output ablation across omics block combinations, (3) advanced ML benchmarking using logistic regression, elastic net, random forest, and XGBoost, and (4) permutation testing of the best advanced-ML model.

## Statistical interpretation
Performance was summarized with AUC, concordance measures, and Cox C-index together with resampling-based uncertainty intervals. Because the matched cohort is not large enough to justify strong predictive claims without calibration, we emphasized effect sizes, confidence intervals, and cross-method consistency rather than threshold-only significance language.

# Results
## Layer contribution and predictive landscape
The direct predictive landscape was uneven. RNA modules achieved the highest all-available AUC at 0.613 (95% CI 0.489-0.737), indicating that transcript-level structure carried the clearest discriminative information in this dataset. CNA yielded the highest Cox C-index at 0.616 (95% CI 0.534-0.699), suggesting stronger alignment with survival-related ranking. Integrated-no-protein features performed similarly on AUC but did not decisively outperform RNA alone. Mutation-only features performed poorly (AUC 0.378), and methylation was near chance in direct discrimination.

These results argue against the common assumption that adding more omics blocks automatically strengthens supervised modeling. Instead, the contribution of each layer was distinct: transcript-level organization best supported classification, whereas copy-number structure best supported survival ordering.

## Fair protein-matched comparison
When all compared models were restricted to the same protein-matched subset, integrated-no-protein achieved the highest AUC at 0.575 (95% CI 0.423-0.729). Protein alone and integrated-with-protein remained near 0.48. This does not imply that protein is biologically uninformative. It shows that, in this cohort, the available protein representation did not translate directly into stronger supervised discrimination once sample-composition bias was controlled.

## Stable latent hubs define the network core
The strongest evidence in the study emerged from hub analysis. LF8, LF5, LF6, and LF7 were the top network hubs, with bootstrap top-k frequencies of 1.0, 1.0, 0.995, and 1.0, respectively. Their bootstrap mean rank scores remained high and clearly separated from lower-priority nodes. This pattern indicates that a small set of latent factors formed the central organizing structure of the integrated network.

The fact that the dominant hubs were latent factors rather than individual raw features is biologically plausible. Integrated latent states are expected to act as convergence points where diverse upstream molecular alterations are translated into coordinated downstream behavior.

## Perturbation identifies high-impact control points
At the primary perturbation fraction of 0.5, LF7, LF6, LF8, and LF5 produced the largest global network shifts, with delta-global values around 0.049-0.054. Bootstrap summaries showed that these effects were not artifacts of a single graph fit. LF5 had the highest top-5 perturbation ranking frequency, while LF6 and LF7 remained similarly prominent.

Sensitivity analysis across the perturbation grid strengthened this interpretation. LF7 had the highest sensitivity slope (0.127), followed by LF8 (0.123), LF6 (0.113), and LF5 (0.110), and all four showed monotonic non-decreasing response. The network therefore reacted to increasing perturbation of these hubs in a graded and stable fashion. From a translational perspective, such nodes are better candidates for downstream intervention-focused validation than hubs that appear influential only in one static centrality ranking.

## Cross-layer architecture and biologic interpretation
DAG-style aggregation showed that RNA->Latent transitions dominated the directed network summary, with Latent->Protein transitions second. This supports a coherent cross-layer model in which transcript-level organization strongly shapes the integrated latent space and is then transmitted into downstream protein-level variation.

Hub-linked module interpretation sharpened this systems picture. LF6 was strongly connected to transcript modules enriched for ADAMTS4, ADAM12, COL12A1, TNC, FOXF1, and COLEC12, consistent with extracellular-matrix remodeling and stromal-like programs. LF7 was linked to modules containing AFAP1L2, APLP2, L1CAM, RDH10, CTSV, and related features consistent with adhesion, invasion, and epithelial plasticity. LF8 was connected to modules containing ONECUT1, L1CAM, MAPT, GFAP, and related lineage-like signals, suggesting a distinct transcriptional state that bridges transcript and protein layers. LF5 was linked to CCNDBP1-associated transcript modules and was the only leading hub with a direct negative latent-to-outcome edge, making it particularly notable as a candidate regulatory bottleneck.

These associations are module-derived and hypothesis-generating rather than experimentally validated pathway assignments. Their value lies in converting abstract latent hubs into tractable biologic candidates.

## Complementarity and advanced ML calibration
The strongest ablation result was the RNA-module plus protein-module combination, which reached an AUC of 0.644. This exceeded RNA modules or protein modules alone and suggests real complementarity between these two representations. Notably, adding burden features to the RNA-protein pair reduced performance, indicating that integration is beneficial only when the added block contributes coherent signal.

Advanced ML played a different role. XGBoost achieved the highest AUC at 0.526 (95% repeated-CV CI 0.445-0.649), followed closely by elastic net and random forest. However, the observed XGBoost AUC was not clearly separated from shuffled-label null performance (p=0.2745). This result usefully constrains interpretation: the dataset supports mechanistic inference more strongly than aggressive predictive claims.

# Discussion
This study supports a clear evidentiary conclusion: the strongest findings in TCGA-OV multi-omics integration are stable cross-layer hubs and perturbation-sensitive network architecture, not high-confidence prediction. That distinction is often blurred in computational oncology, where a modest classifier can receive more attention than a reproducible mechanistic signal. The present data argue for the opposite emphasis.

The four leading latent hubs, LF8, LF5, LF6, and LF7, were supported by several independent analyses. They remained top-ranked under bootstrap centrality, produced the largest and most monotonic perturbation responses, and occupied the center of a biologically coherent RNA->Latent->Protein network structure. These are not interchangeable pieces of evidence; they are complementary stress tests, and the same hubs passed all of them.

The comparative modeling results further clarify where the signal sits. RNA modules were the strongest direct discriminators, while CNA best preserved survival-ranking information. Methylation and mutation did not perform as strong stand-alone supervised layers in the present formulation, but that should not be interpreted as biologic irrelevance. Their effect may be more diffuse, indirect, or visible only once propagated into transcriptomic and latent states. This is precisely why the network formulation is informative: it reveals how signal is organized across layers even when direct classification is weak.

Protein deserves similar nuance. Protein did not improve fairness-restricted integrated benchmarking in a simple one-step way, but protein modules helped the best ablation combination and occupied the strongest downstream position in pathway aggregation. This suggests that protein may contribute more clearly as a relational and interpretive layer than as an isolated predictive block in this cohort.

The advanced-ML results are useful precisely because they do not support overreach. XGBoost, elastic net, and random forest remained modest, and the permutation result was not strongly persuasive. A less disciplined manuscript might still foreground such models. A stronger manuscript uses them as calibration and places the scientific center of gravity where the data are most reproducible: the hub and pathway structure.

The study has limitations. It remains a single-cohort analysis, and strict matching reduced the effective sample size, especially for protein-based comparisons. The latent factors are computational constructs and require downstream biological anchoring. The hub-interpretation layer is module-based and therefore hypothesis-generating. Even so, the study provides a credible translational starting point because it prioritizes findings that remain stable under multiple analytical views.

For the oncology community, the practical output is a short list of candidate control points and associated pathway contexts for follow-up. LF6-linked extracellular-matrix remodeling, LF7-linked adhesion and invasion programs, LF8-linked lineage-like transcript-protein states, and LF5-linked negative outcome association together define a biologically plausible set of targets for orthogonal validation.

# Additional Information
## Acknowledgements
This study used public de-identified resources from the Genomic Data Commons, cBioPortal, and the Proteomic Data Commons.

## Authors' contributions
Dr Siddalingaiah H S conceived the study, oversaw the computational analysis, interpreted the results, and prepared the manuscript.

## Ethics approval and consent to participate
This study analyzed publicly available de-identified human data and did not involve direct patient contact or new biospecimen collection. Formal institutional ethics approval and participant consent were not required for this secondary analysis. The work was conducted in accordance with the ethical principles of the Declaration of Helsinki as applicable to secondary analysis of public de-identified datasets.

## Consent for publication
Not applicable.

## Data availability
Source data are available from the GDC, cBioPortal, and PDC under their respective access terms. Derived artifacts, scripts, and reproducibility metadata are available in the project workspace and public release bundles.

## Competing interests
The author declares no competing interests.

## Funding information
The author received no specific funding for this work.

# References
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
