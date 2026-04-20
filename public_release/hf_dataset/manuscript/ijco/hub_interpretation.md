# Hub Interpretation

This note summarizes the strongest network-linked biological signals for the four leading latent hubs (LF8, LF5, LF6, LF7).
Interpretation is based on the signed edge structure of the integrated network and on PCA-derived feature loadings for the linked RNA and protein modules.

## LF8
Key incoming signals:
- rna_module_010 -> LF8 (-0.649, input_to_latent): MZT1 (0.020); OR4K3 (0.019); AL158847 (0.019); IGHV3-41 (0.019); ONECUT1 (0.018); RPL14P6 (0.018); OOEPP1 (0.018); AL445604 (0.018)
- rna_module_012 -> LF8 (-0.373, input_to_latent): AFAP1L2 (0.019); APLP2 (0.019); LMX1B (0.017); MTCO1P2 (0.017); HMGB1P32 (0.017); LINC02384 (-0.017); TRUB2 (-0.017); L1CAM (0.016)
- protein_module_016 -> LF8 (-0.357, input_to_latent): AGID00303 (0.145); AGID00039 (-0.133); AGID00445 (0.125); AGID00201 (-0.118); AGID00165 (-0.116); AGID00189 (-0.115); AGID00484 (-0.113); AGID00376 (0.111)
- rna_module_011 -> LF8 (-0.339, input_to_latent): AC103564 (0.024); AC008805 (0.024); SLC35F3 (0.023); GFAP (0.023); TDRD12 (0.023); MAPT (0.022); SLC35F3-AS1 (0.022); ADRA2B (0.022)

## LF5
Key incoming signals:
- rna_module_005 -> LF5 (-0.503, input_to_latent): AC010300 (0.018); AC008731 (0.017); AC092620 (0.017); MRPS21P8 (0.017); AC002094 (0.017); SLC25A5 (-0.016); AC126773 (0.016); RPL9P2 (0.016)
- rna_module_007 -> LF5 (0.464, input_to_latent): CCNDBP1 (0.019); PTPRVP (0.018); AL139260 (0.017); CASC20 (-0.017); AL358134 (0.017); AC244102 (-0.017); AL442644 (0.017); KCNQ4 (0.017)
- rna_module_011 -> LF5 (-0.379, input_to_latent): AC103564 (0.024); AC008805 (0.024); SLC35F3 (0.023); GFAP (0.023); TDRD12 (0.023); MAPT (0.022); SLC35F3-AS1 (0.022); ADRA2B (0.022)
- protein_module_007 -> LF5 (-0.371, input_to_latent): AGID00002 (0.145); AGID00350 (-0.119); AGID00387 (-0.115); AGID00003 (0.113); AGID00050 (-0.112); AGID00177 (-0.106); AGID00208 (-0.103); AGID00396 (-0.100)
Key outgoing signals:
- LF5 -> comp2 (-0.381, latent_to_outcome)

## LF6
Key incoming signals:
- rna_module_003 -> LF6 (-0.527, input_to_latent): ADAMTS4 (0.018); ADAM12 (0.018); GALNT5 (0.018); COL12A1 (0.018); GUCY1A1 (0.017); TNC (0.017); FOXF1 (0.017); COLEC12 (0.017)
- rna_module_013 -> LF6 (0.443, input_to_latent): AC073614 (0.022); PIK3AP1 (0.021); RNU6-752P (0.021); KSR1P1 (0.020); FAM183DP (0.020); RTBDN (0.020); RPL19P18 (0.020); AL596214 (0.020)
- rna_module_005 -> LF6 (0.423, input_to_latent): AC010300 (0.018); AC008731 (0.017); AC092620 (0.017); MRPS21P8 (0.017); AC002094 (0.017); SLC25A5 (-0.016); AC126773 (0.016); RPL9P2 (0.016)
- rna_module_008 -> LF6 (0.413, input_to_latent): MANEAL (0.019); UNC13A (0.019); AC008761 (0.018); AL031658 (0.018); HIGD1AP2 (0.017); ONECUT2 (0.017); KRT127P (0.017); AP3B2 (0.017)

## LF7
Key incoming signals:
- rna_module_006 -> LF7 (-0.543, input_to_latent): PPP1R37 (0.019); BICRA (0.019); PPP1R12C (0.019); SCAF1 (0.018); CALM3 (0.017); FKRP (0.017); HIC1 (0.017); MRPS30-DT (-0.017)
- rna_module_012 -> LF7 (-0.500, input_to_latent): AFAP1L2 (0.019); APLP2 (0.019); LMX1B (0.017); MTCO1P2 (0.017); HMGB1P32 (0.017); LINC02384 (-0.017); TRUB2 (-0.017); L1CAM (0.016)
- rna_module_024 -> LF7 (0.361, input_to_latent): RDH10 (0.022); AK1 (0.021); ALPP (0.021); GCNT1P4 (0.021); GLRXP1 (0.020); AC117372 (0.020); CTSV (0.020); LINC00330 (0.020)
- rna_module_025 -> LF7 (-0.338, input_to_latent): AC127894 (0.028); AL929288 (0.028); AL591034 (0.028); MTCO3P28 (0.028); AC078974 (0.028); DPRXP7 (0.028); RDM1P1 (0.028); RN7SL584P (0.028)
