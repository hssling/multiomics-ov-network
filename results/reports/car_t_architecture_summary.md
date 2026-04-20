# CAR-T Architecture Metadata Summary

Date: 2026-04-20
Project: multiomics-ov-network

## Purpose

This table converts the public CAR construct source catalog into a manuscript-ready architecture summary.
It is designed for supplementary reporting, reference design tracking, and future raw-read screening preparation.

## Scope

- Inputs: `results/tables/car_t_public_sequence_catalog.csv`
- Outputs: `results/tables/car_t_architecture_metadata.csv`
- Interpretation level: metadata and architecture only
- Deliberate limitation: this summary does not reproduce full engineered therapeutic sequences

## Main Observations

- The public sources are strongest for CD19-focused constructs, with both 4-1BB and CD28 costimulatory architectures represented.
- Patent entries provide domain-level architecture and SEQ-ID references rather than turnkey analytic panels.
- The current project can use these records for annotation and future screening design, not for direct TCGA-OV transgene recovery.

## Table Preview

| source_type   | target_antigen      | construct_identifier                       | costimulatory_domain   | signaling_domain      | sequence_access_level                   |
|:--------------|:--------------------|:-------------------------------------------|:-----------------------|:----------------------|:----------------------------------------|
| Addgene       | CD19                | pSLCAR-CD19-BBz / Addgene 135992           | 4-1BB                  | CD3-zeta              | direct public construct/metadata access |
| Addgene       | general/unspecified | API and sequence-data access portal        | not explicitly stated  | not explicitly stated | metadata only                           |
| FreeGenes     | CD19                | BBF10K_000527 / pOpen-CD19CAR-CD28z        | CD28                   | CD3-zeta              | direct public construct/metadata access |
| Patent        | general/unspecified | WO2020261231A1                             | 4-1BB                  | not explicitly stated | patent-disclosed sequence identifiers   |
| Patent        | CD19                | LTG2050 and related anti-CD19 CAR variants | not explicitly stated  | CD3-zeta              | patent-disclosed sequence identifiers   |
| Patent        | CD19/CD22           | CAR 22-19 / LTG2681 family                 | not explicitly stated  | not explicitly stated | patent-disclosed sequence identifiers   |
| Patent        | CD19                | h19BBz / FMC63-based CD19 CAR              | 4-1BB                  | CD3-zeta              | patent-disclosed sequence identifiers   |
| Paper         | CD19                | ARI-0001                                   | not explicitly stated  | not explicitly stated | paper-level construct description       |

## Recommended Manuscript Use

1. Cite as a supplementary reference table for public CAR construct provenance.
2. Use the architecture columns to define any future custom CAR reference panel.
3. State clearly that TCGA-OV processed files do not permit direct CAR discovery from the present workspace.
