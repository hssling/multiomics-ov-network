# GitHub Release Note: CAR Scaffold Refresh

Date: 2026-04-20
Project: multiomics-ov-network

## Summary

This release refreshes the public TCGA-OV evidence package and adds a safe CAR benchmarking scaffold without bundling engineered construct reference sequences.

## Included updates

- Journal of Biomedical Informatics submission package refresh
- CAR benchmark tooling readiness with `bwa`, `samtools`, and `minimap2`
- metadata-only CAR panel scaffold under `references/car_t/`
- updated public-release documentation for Hugging Face and Kaggle
- cleaned duplicate stale public-release copies created by an earlier copy-layout bug

## CAR scaffold scope

Included:
- metadata manifest template
- placeholder panel interface
- readiness audit outputs
- benchmark command template

Not included:
- engineered CAR FASTA content
- de novo construct panel generation
- construct-level recovery claims

## Public-use intent

- workflow experimentation
- metadata curation
- readiness validation
- approved future reference-panel integration
