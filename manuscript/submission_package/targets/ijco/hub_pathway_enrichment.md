# Hub Pathway Enrichment

This note summarizes pathway enrichment for the strongest module-linked genes associated with the four leading latent hubs.
Enrichment was performed with Enrichr libraries through gseapy and should be treated as hypothesis-generating support for the network interpretation.

## LF8
Usable enrichment genes: ADRA2B, AFAP1L2, GDF6, GFAP, HMGB1P32, L1CAM, LMX1B, MAPT, MZT1, ONECUT1, OOEPP1, OR4K3, PKP1, PRPH, SLC35F3, SLC35F3-AS1, TDRD12, TRUB2
### MSigDB_Hallmark_2020
- Hedgehog Signaling | adjusted P=0.156 | genes=L1CAM
- Apical Surface | adjusted P=0.156 | genes=AFAP1L2
- UV Response Up | adjusted P=0.166 | genes=ONECUT1
### KEGG_2021_Human
- Maturity onset diabetes of the young | adjusted P=0.27 | genes=ONECUT1
- Pathways of neurodegeneration | adjusted P=0.27 | genes=MAPT;PRPH
- TGF-beta signaling pathway | adjusted P=0.27 | genes=GDF6
### GO_Biological_Process_2023
- Positive Regulation Of Axon Extension (GO:0045773) | adjusted P=0.0253 | genes=MAPT;L1CAM
- Regulation Of Axon Extension (GO:0030516) | adjusted P=0.0343 | genes=MAPT;L1CAM
- Positive Regulation Of Axonogenesis (GO:0050772) | adjusted P=0.0343 | genes=MAPT;L1CAM

## LF5
Usable enrichment genes: ADRA2B, CASC20, CCNDBP1, GAPDHP21, GAPDHP66, GFAP, KCNQ4, MAPT, MZT1, ONECUT1, OOEPP1, OR4K3, PTPRVP, RANP1, SLC25A5, SLC35F3, SLC35F3-AS1, TDRD12
### MSigDB_Hallmark_2020
- UV Response Up | adjusted P=0.166 | genes=ONECUT1
- Oxidative Phosphorylation | adjusted P=0.166 | genes=SLC25A5
- Complement | adjusted P=0.166 | genes=ADRA2B
### KEGG_2021_Human
- cGMP-PKG signaling pathway | adjusted P=0.162 | genes=SLC25A5;ADRA2B
- Parkinson disease | adjusted P=0.162 | genes=MAPT;SLC25A5
- Maturity onset diabetes of the young | adjusted P=0.162 | genes=ONECUT1
### GO_Biological_Process_2023
- Negative Regulation Of Mitochondrion Organization (GO:0010823) | adjusted P=0.0691 | genes=MAPT;SLC25A5
- Inclusion Body Assembly (GO:0070841) | adjusted P=0.0691 | genes=MAPT
- Regulation Of Epinephrine Secretion (GO:0014060) | adjusted P=0.0691 | genes=ADRA2B

## LF6
Usable enrichment genes: ADAM12, ADAMTS4, COL12A1, COLEC12, FAM183DP, FOXF1, GALNT5, GUCY1A1, HIGD1AP2, KRT127P, KSR1P1, MANEAL, ONECUT2, PIK3AP1, RTBDN, SLC25A5, TNC, UNC13A
### MSigDB_Hallmark_2020
- Epithelial Mesenchymal Transition | adjusted P=0.00432 | genes=COL12A1;ADAM12;TNC
- Androgen Response | adjusted P=0.166 | genes=GUCY1A1
- Myogenesis | adjusted P=0.166 | genes=ADAM12
### KEGG_2021_Human
- cGMP-PKG signaling pathway | adjusted P=0.217 | genes=GUCY1A1;SLC25A5
- Mucin type O-glycan biosynthesis | adjusted P=0.217 | genes=GALNT5
- PI3K-Akt signaling pathway | adjusted P=0.217 | genes=TNC;PIK3AP1
### GO_Biological_Process_2023
- Neuromuscular Junction Development (GO:0007528) | adjusted P=0.0246 | genes=UNC13A;TNC
- Regulation Of Defense Response (GO:0031347) | adjusted P=0.0513 | genes=TNC;PIK3AP1
- Toll-Like Receptor 9 Signaling Pathway (GO:0034162) | adjusted P=0.0513 | genes=PIK3AP1

## LF7
Usable enrichment genes: AFAP1L2, AK1, BICRA, CALM3, CTSV, DPRXP7, FKRP, GCNT1P4, GLRXP1, HIC1, HMGB1P32, L1CAM, LMX1B, MIR4425, PMCHL2, PPP1R12C, PPP1R37, RDH10, RDM1P1, RMRPP5 ...
### MSigDB_Hallmark_2020
- Complement | adjusted P=0.137 | genes=CALM3;CTSV
- Hedgehog Signaling | adjusted P=0.137 | genes=L1CAM
- Apical Surface | adjusted P=0.137 | genes=AFAP1L2
### KEGG_2021_Human
- Vascular smooth muscle contraction | adjusted P=0.271 | genes=CALM3;PPP1R12C
- Oxytocin signaling pathway | adjusted P=0.271 | genes=CALM3;PPP1R12C
- Thiamine metabolism | adjusted P=0.271 | genes=AK1
### GO_Biological_Process_2023
- Regulation Of Cyclic-Nucleotide Phosphodiesterase Activity (GO:0051342) | adjusted P=0.11 | genes=CALM3
- Positive Regulation Of Ryanodine-Sensitive Calcium-Release Channel Activity (GO:0060316) | adjusted P=0.11 | genes=CALM3
- mRNA Pseudouridine Synthesis (GO:1990481) | adjusted P=0.11 | genes=TRUB2
