# External Dataset Suitability Note

Date: 2026-04-20

## User-specified accession checked

Dataset checked: `GSM4877937`

### What it is
- GEO sample `GSM4877937` links to SRA experiment `SRX9423612` under study `PRJNA674045`.
- It is **paired-end bulk RNA-seq** from **tumor-infiltrating CD8 T cells** in **metastatic ovarian cancer**.
- Raw reads are available through SRA.

### Why it matters
- This is relevant to the ovarian cancer project because it provides an **external ovarian immune-context dataset**.
- It can support **validation of T-cell exhaustion / immune-state signals** against our expression-derived immune proxy branch.

### Why it does not solve the CAR-sequence question
- The sample is **not a CAR-T product dataset**.
- It does **not** provide evidence of an engineered CAR construct.
- It is therefore **not suitable for direct CAR transgene detection or CAR construct recovery**.

## Best interpretation

Use `GSM4877937` as an **external ovarian T-cell-state validation dataset**, not as a CAR-sequence source.

## Additional public datasets already identified

See `results/tables/external_cart_dataset_candidates.csv` for a compact comparison of:
- `GSM4877937 / SRX9423612 / PRJNA674045`: ovarian TIL RNA-seq, indirect CAR relevance
- `SRX26389396 / PRJNA1173154`: CD22 CAR-T infusion product bulk RNA-seq, direct CAR relevance
- `SRX26517613 / PRJNA980643`: BCMA CAR-T single-cell multi-omic dataset, direct CAR relevance

## Sources
- GEO GSM4877937: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM4877937
- SRA SRX9423612: https://www.ncbi.nlm.nih.gov/sra?term=SRX9423612
- SRA SRX26389396: https://www.ncbi.nlm.nih.gov/sra/SRX26389396
- SRA SRX26517613: https://www.ncbi.nlm.nih.gov/sra/SRX26517613
