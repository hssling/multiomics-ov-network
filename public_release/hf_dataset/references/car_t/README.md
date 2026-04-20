# CAR-T Reference Panel Staging Area

This directory is a **scaffold only** for a user-supplied, validated CAR reference panel used for alignment readiness and benchmarking.

## What is included

- `README.md`: usage and scope notes
- `reference_panel_manifest_template.csv`: metadata template for approved reference entries
- `public_car_panel.placeholder.txt`: placeholder instructions instead of sequence content

## What is not included

- No engineered therapeutic construct FASTA is bundled here
- No automatically generated construct reference panel is bundled here
- No claim is made that the repository can recover or reconstruct CAR designs without an approved external panel

## Expected user-supplied file

- `public_car_panel.fasta`

This file is expected only when an approved reference panel is available through the user's own governance and provenance process.

## Scope boundary

- Do not treat this repository as a source of engineered therapeutic construct sequences.
- Do not place unvalidated or proprietary constructs here.
- Only use references that are already approved for your intended benchmark.
- Sequence-level alignment claims should be made only after the panel metadata and provenance have been reviewed.

## Expected companion metadata

The pipeline expects summary metadata in:

- `results/tables/car_t_architecture_metadata.csv`
- `references/car_t/reference_panel_manifest_template.csv`

These files should describe provenance, access level, intended benchmark use, and review status for each externally supplied reference entry.
