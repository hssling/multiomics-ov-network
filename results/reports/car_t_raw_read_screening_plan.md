# CAR Raw-Read Screening Skeleton

Date: 2026-04-20
Project: multiomics-ov-network

## Current Status

- Raw-read/alignment file count across configured roots: 0
- CAR reference FASTA present: no
- CAR architecture metadata table present: yes

## Interpretation

The workflow skeleton is ready, but the current workspace remains blocked for direct CAR/transgene screening because sequence-level inputs are absent.

## Inventory Summary

| root                                                                        | pattern    |   count |
|:----------------------------------------------------------------------------|:-----------|--------:|
| D:\Ovarian cancer network analysis\multiomics-ov-network\data\raw\gdc\files | *.bam      |       0 |
| D:\Ovarian cancer network analysis\multiomics-ov-network\data\raw\gdc\files | *.cram     |       0 |
| D:\Ovarian cancer network analysis\multiomics-ov-network\data\raw\gdc\files | *.fastq    |       0 |
| D:\Ovarian cancer network analysis\multiomics-ov-network\data\raw\gdc\files | *.fastq.gz |       0 |
| D:\Ovarian cancer network analysis\multiomics-ov-network\data\raw\gdc\files | *.fq       |       0 |
| D:\Ovarian cancer network analysis\multiomics-ov-network\data\raw\gdc\files | *.fq.gz    |       0 |

## Expected Inputs For Future Execution

1. A validated custom CAR reference FASTA assembled from approved public sources or user-supplied constructs.
2. Raw BAM, CRAM, or FASTQ files from a CAR-relevant sequencing dataset.
3. Alignment and junction-support criteria defined in `configs/car_t.yaml`.

## Recommended Screening Logic

1. Inventory raw files and verify read modality.
2. Align reads against the CAR reference panel.
3. Flag high-confidence CAR evidence using split/soft-clipped support, junction-spanning reads, and unique mapping quality.
4. Summarize sample-level detection with manual review of candidate alignments.

## Generated Assets

- `results/tables/car_t_raw_read_inventory.csv`
- `results/reports/car_t_raw_read_commands.sh`
- `results/reports/car_t_raw_read_screening_plan.md`
