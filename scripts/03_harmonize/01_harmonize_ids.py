from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


def load_layer(path: Path, layer: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    out = df[["sample_id", "patient_id"]].drop_duplicates()
    out["layer"] = layer
    return out


def main():
    args = parse_args(extra=True)
    cfg = read_yaml(args.config)
    thr = read_yaml(args.thresholds) if args.thresholds else {}
    log = setup_logger("harmonize")

    interim = Path(cfg["paths"]["interim"])
    out_map = Path(cfg["paths"]["sample_maps"])
    out_map.mkdir(parents=True, exist_ok=True)

    layers = list(cfg.get("analysis", {}).get("main_layers", ["rna", "cna", "methylation", "mutation"]))
    optional_layers = []
    for layer in cfg.get("analysis", {}).get("optional_layers", []):
        if (interim / f"{layer}_matrix.parquet").exists():
            optional_layers.append(layer)
    all_layers = layers + optional_layers
    sets = {}
    sample_rows = []

    for layer in all_layers:
        path = interim / f"{layer}_matrix.parquet"
        df = load_layer(path, layer)
        sets[layer] = set(df["patient_id"])
        sample_rows.append(df)

    merged = pd.concat(sample_rows, axis=0, ignore_index=True)
    all_intersection = set.intersection(*(sets[l] for l in layers))

    pivot = (
        merged.assign(present=1)
        .drop_duplicates(["patient_id", "layer"])
        .pivot(index="patient_id", columns="layer", values="present")
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    for layer in all_layers:
        if layer not in pivot.columns:
            pivot[layer] = 0
    pivot["matched_all_main_layers"] = (pivot[layers].sum(axis=1) == len(layers)).astype(int)

    clinical = pd.read_csv(interim / "clinical.csv")
    master = pivot.merge(clinical, on="patient_id", how="left")
    master.to_csv(out_map / "master_sample_sheet.csv", index=False)

    summary_rows = []
    for layer in all_layers:
        summary_rows.append({"metric": f"n_patients_{layer}", "value": len(sets[layer])})
    summary_rows.append({"metric": "n_patients_intersection_all_main_layers", "value": len(all_intersection)})
    summary = pd.DataFrame(summary_rows)

    min_intersection = int(thr.get("thresholds", {}).get("min_intersection_samples", 30))
    status = "pass" if len(all_intersection) >= min_intersection else "warn"
    summary = pd.concat(
        [
            summary,
            pd.DataFrame(
                {
                    "metric": ["intersection_threshold", "intersection_status"],
                    "value": [min_intersection, status],
                }
            ),
        ],
        ignore_index=True,
    )

    summary.to_csv("results/tables/sample_matching_summary.csv", index=False)
    log.info("Harmonization complete. Intersection: %s", len(all_intersection))


if __name__ == "__main__":
    main()
