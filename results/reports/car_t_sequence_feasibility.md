# CAR-T Sequence Feasibility Assessment

Date: 2026-04-20
Project: multiomics-ov-network
Question: Can CAR-T sequences be identified from the current local TCGA-OV workspace and from public online resources?

## Summary

Conclusion:
- Public online CAR-related sequence resources do exist and can be curated into a reusable source catalog.
- The current local TCGA-OV workspace does not contain the raw sequencing file types needed for a defensible CAR/transgene read search.
- Endogenous immune-receptor inference and public construct curation are feasible, but true CAR-transgene recovery is not supported by the current downloaded data.

## Local Workspace Assessment

The current `data/raw/gdc/files` tree contains primarily:
- RNA STAR gene-count tables (`*.rna_seq.augmented_star_gene_counts.tsv`)
- methylation beta-value tables (`*.methylation_array.sesame.level3betas.txt`)
- masked mutation MAF files (`*.wxs.aliquot_ensemble_masked.maf.gz`)
- gene-level copy-number TSV files
- RPPA TSV files

Counts of raw-read or alignment files relevant for CAR-transgene detection:
- `*.bam`: 0
- `*.bai`: 0
- `*.cram`: 0
- `*.fastq`: 0
- `*.fastq.gz`: 0
- `*.fq`: 0
- `*.fq.gz`: 0

Interpretation:
- There are no local BAM/CRAM/FASTQ files to align against a custom CAR reference.
- Therefore, a sequence-level CAR/transgene search cannot be performed from the current workspace.
- The local data are suitable for expression-level, mutation-level, methylation-level, CNA-level, RPPA-level, and immune-context analyses, but not engineered transgene discovery.

## Public Online Resource Assessment

Public CAR-related sequence resources identified:
- Addgene plasmid entries with construct and sequence metadata
- Addgene developer portal for programmatic plasmid and sequence-data access
- FreeGenes construct pages with public GenBank-linked CAR designs
- Patent disclosures with explicit SEQ IDs, domain definitions, and architecture descriptions
- CAR-T papers and supplements describing construct architecture and source backbones

These sources can support:
- metadata cataloguing of public CAR constructs
- architecture-level annotation (target, hinge, TM, co-stimulatory domain, signaling domain)
- downstream manual or licensed retrieval of linked public sequence records where available

## Practical Recommendation

Feasible now:
1. Build and maintain a public CAR construct metadata compendium.
2. Add endogenous TCR/BCR repertoire inference as a separate analysis using the available RNA-derived data products only if appropriate upstream files exist in future runs.
3. If true CAR/transgene detection is desired, obtain raw BAM/CRAM or FASTQ files from a suitable CAR-T dataset and align reads to a custom CAR reference panel.

Not feasible now:
- Direct recovery of CAR-T construct sequences from the current TCGA-OV workspace.

## Output Produced

- `results/tables/car_t_public_sequence_catalog.csv`

## Sources Used

- Addgene plasmid page: https://www.addgene.org/135992/
- Addgene Developers Portal: https://developers.addgene.org/
- FreeGenes CD19CAR-CD28z page: https://freegenes.github.io/genes/BBF10K_000527.html
- Google Patents WO2020261231A1: https://patents.google.com/patent/WO2020261231A1/en
- Google Patents US20190106492A1: https://patents.google.com/patent/US20190106492A1/en
- Google Patents US20220324967A1: https://patents.google.com/patent/US20220324967A1/en
- EPO EP4190804A1 PDF: https://data.epo.org/publication-server/rest/v1.0/publication-dates/20230607/patents/EP4190804NWA1/document.pdf
- ARI-0001 paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC6319086/
