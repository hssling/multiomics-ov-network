from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


EXPECTED_COLUMNS = [
    "source_type",
    "title",
    "antigen_or_scope",
    "construct_or_identifier",
    "public_access_route",
    "sequence_availability",
    "notable_components_or_notes",
    "url",
]


def read_catalog(path: Path) -> pd.DataFrame:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        header = handle.readline().strip().split(",")
        if header != EXPECTED_COLUMNS:
            raise ValueError(f"Unexpected CAR catalog header in {path}")
        for line in handle:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split(",")
            if len(parts) < len(EXPECTED_COLUMNS):
                raise ValueError(f"Malformed CAR catalog line: {line}")
            fixed = parts[:6]
            url = parts[-1]
            notes = ",".join(parts[6:-1]).strip()
            rows.append(dict(zip(EXPECTED_COLUMNS, fixed + [notes, url])))
    return pd.DataFrame(rows, columns=EXPECTED_COLUMNS)


def extract_target(text: str) -> str:
    for token in ["CD19/CD22", "CD19", "CD22", "BCMA", "HER2", "EGFRvIII", "Mesothelin"]:
        if token.lower() in text.lower():
            return token
    return "general/unspecified"


def extract_costim(text: str) -> str:
    text_lower = text.lower()
    hits = []
    if any(tok in text_lower for tok in ["4-1bb", "cd137", "bbz", "h19bbz"]):
        hits.append("4-1BB")
    if any(tok in text_lower for tok in ["cd28", "28z"]):
        hits.append("CD28")
    return "+".join(hits) if hits else "not explicitly stated"


def extract_signaling(text: str) -> str:
    text_lower = text.lower()
    if any(tok in text_lower for tok in ["cd3 zeta", "cd3zeta", "zeta", "bbz", "28z"]):
        return "CD3-zeta"
    return "not explicitly stated"


def extract_hinge_tm(text: str) -> tuple[str, str]:
    text_lower = text.lower()
    hinge = "not explicitly stated"
    tm = "not explicitly stated"
    if "cd8 hinge" in text_lower:
        hinge = "CD8 hinge"
    if "cd8 tm" in text_lower or "cd8 transmembrane" in text_lower:
        tm = "CD8 transmembrane"
    elif "cd28" in text_lower and ("tm" in text_lower or "transmembrane" in text_lower):
        tm = "CD28 transmembrane"
    return hinge, tm


def extract_scfv(text: str) -> str:
    text_lower = text.lower()
    if "fmc63" in text_lower:
        return "FMC63-related"
    if "ltg2050" in text_lower:
        return "LTG2050"
    if "ari-0001" in text_lower:
        return "ARI-0001 academic construct"
    return "not explicitly stated"


def classify_sequence_access(value: str) -> str:
    v = value.lower()
    if "genbank" in v or "public plasmid" in v or "sequence metadata" in v:
        return "direct public construct/metadata access"
    if "seq id" in v or "patent" in v:
        return "patent-disclosed sequence identifiers"
    if "paper" in v:
        return "paper-level construct description"
    return "metadata only"


def sanitize_for_manuscript(df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for row in df.to_dict(orient="records"):
        evidence = " | ".join(
            [
                str(row.get("title", "")),
                str(row.get("construct_or_identifier", "")),
                str(row.get("sequence_availability", "")),
                str(row.get("notable_components_or_notes", "")),
            ]
        )
        hinge, tm = extract_hinge_tm(evidence)
        records.append(
            {
                "source_type": row.get("source_type", ""),
                "title": row.get("title", ""),
                "target_antigen": extract_target(evidence),
                "construct_identifier": row.get("construct_or_identifier", ""),
                "scfv_or_binding_domain": extract_scfv(evidence),
                "hinge_spacer": hinge,
                "transmembrane_domain": tm,
                "costimulatory_domain": extract_costim(evidence),
                "signaling_domain": extract_signaling(evidence),
                "sequence_access_level": classify_sequence_access(str(row.get("sequence_availability", ""))),
                "recommended_project_use": "cataloguing/reference design only",
                "public_access_route": row.get("public_access_route", ""),
                "source_url": row.get("url", ""),
            }
        )
    return pd.DataFrame.from_records(records)


def build_markdown_table(df: pd.DataFrame) -> str:
    cols = [
        "source_type",
        "target_antigen",
        "construct_identifier",
        "costimulatory_domain",
        "signaling_domain",
        "sequence_access_level",
    ]
    return df[cols].to_markdown(index=False)


def main() -> None:
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("car_t_assets")

    tables = Path(cfg["paths"]["results_tables"])
    reports = Path("results/reports")
    reports.mkdir(parents=True, exist_ok=True)

    src = tables / "car_t_public_sequence_catalog.csv"
    if not src.exists():
        raise FileNotFoundError(f"Missing CAR-T catalog: {src}")

    catalog = read_catalog(src)
    architecture = sanitize_for_manuscript(catalog)
    out_csv = tables / "car_t_architecture_metadata.csv"
    architecture.to_csv(out_csv, index=False)

    md = f"""# CAR-T Architecture Metadata Summary

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

{build_markdown_table(architecture)}

## Recommended Manuscript Use

1. Cite as a supplementary reference table for public CAR construct provenance.
2. Use the architecture columns to define any future custom CAR reference panel.
3. State clearly that TCGA-OV processed files do not permit direct CAR discovery from the present workspace.
"""
    out_md = reports / "car_t_architecture_summary.md"
    out_md.write_text(md, encoding="utf-8")
    log.info("Wrote %s and %s", out_csv, out_md)


if __name__ == "__main__":
    main()
