from pathlib import Path
import sys
import gzip
import re
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger, to_patient_id, write_flag


def read_table_auto(path: Path) -> pd.DataFrame:
    kwargs = {"sep": "\t", "low_memory": False, "comment": "#"}
    if path.suffix.lower() == ".gz":
        kwargs["compression"] = "gzip"
    try:
        return pd.read_csv(path, **kwargs)
    except Exception:
        return pd.read_csv(path, sep=",", low_memory=False)


def normalize_feature_name(x: str) -> str:
    if not isinstance(x, str):
        return str(x)
    x = x.strip()
    x = re.sub(r"\.[0-9]+$", "", x)
    return x


def choose_column(columns: List[str], candidates: List[str]) -> Optional[str]:
    lookup = {c.lower(): c for c in columns}
    for cand in candidates:
        if cand.lower() in lookup:
            return lookup[cand.lower()]
    return None


def parse_numeric_series(path: Path, layer: str) -> pd.Series:
    df = read_table_auto(path)
    if df.empty:
        raise ValueError(f"Empty file: {path}")

    feature_col = choose_column(
        list(df.columns),
        [
            "gene_name",
            "hugo_symbol",
            "gene",
            "gene_id",
            "ensembl_gene_id",
            "composite element ref",
            "composite_element_ref",
            "probe_id",
            "probe",
            "id",
        ],
    )

    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        for c in df.columns:
            converted = pd.to_numeric(df[c], errors="coerce")
            if converted.notna().sum() > 0:
                df[c] = converted
                numeric_cols.append(c)

    if layer == "rna":
        val_col = choose_column(
            list(df.columns),
            ["tpm_unstranded", "fpkm_uq_unstranded", "fpkm_unstranded", "unstranded", "normalized_count", "value"],
        )
    elif layer == "cna":
        val_col = choose_column(
            list(df.columns),
            ["copy_number", "gene_level_copy_number", "segment_mean", "cna", "value"],
        )
    elif layer == "methylation":
        val_col = choose_column(list(df.columns), ["beta_value", "beta", "value"])
    elif layer == "protein":
        val_col = choose_column(
            list(df.columns),
            ["protein_expression", "protein_abundance", "normalized_abundance", "value"],
        )
    else:
        val_col = None

    if val_col is None:
        if not numeric_cols:
            raise ValueError(f"No numeric columns found in {path}")
        val_col = numeric_cols[-1]

    if feature_col is None:
        feature_col = df.columns[0]

    sub = df[[feature_col, val_col]].copy()
    sub[feature_col] = sub[feature_col].map(normalize_feature_name)
    sub[val_col] = pd.to_numeric(sub[val_col], errors="coerce")
    sub = sub.dropna(subset=[feature_col, val_col])
    sub = sub[~sub[feature_col].astype(str).str.startswith("__")]

    if sub.empty:
        raise ValueError(f"No usable rows in {path}")

    return sub.groupby(feature_col)[val_col].mean()


def parse_mutation_file(path: Path) -> pd.Series:
    df = read_table_auto(path)
    if df.empty:
        raise ValueError(f"Empty mutation file: {path}")

    gene_col = choose_column(list(df.columns), ["hugo_symbol", "gene", "gene_name", "symbol"])
    if gene_col is None:
        raise ValueError(f"Mutation gene column not found in {path}")

    vc_col = choose_column(list(df.columns), ["variant_classification"])
    if vc_col is not None:
        drop_classes = {
            "Silent",
            "Synonymous_SNV",
            "3'UTR",
            "5'UTR",
            "IGR",
            "Intron",
            "RNA",
            "5'Flank",
            "3'Flank",
            "lincRNA",
        }
        df = df[~df[vc_col].astype(str).isin(drop_classes)]

    genes = (
        df[gene_col]
        .astype(str)
        .map(normalize_feature_name)
        .replace({"nan": np.nan, "": np.nan})
        .dropna()
        .unique()
        .tolist()
    )
    if not genes:
        raise ValueError(f"No mutated genes in {path}")

    return pd.Series(1, index=genes, dtype="int8")


def map_manifest_to_local_files(manifest: pd.DataFrame, raw_root: Path) -> pd.DataFrame:
    files = []
    for p in raw_root.rglob("*"):
        if p.is_file() and p.name not in {"gdc_download_manifest.tsv", "manifest_summary.json", "download_complete.flag"}:
            files.append(p)

    by_name: Dict[str, List[Path]] = {}
    for p in files:
        by_name.setdefault(p.name, []).append(p)

    out = manifest.copy()
    local_paths = []
    for _, row in out.iterrows():
        fname = str(row.get("file_name", ""))
        fid = str(row.get("file_id", ""))
        candidates = by_name.get(fname, [])
        chosen = None
        if candidates:
            chosen = next((c for c in candidates if fid and fid in str(c.parent)), candidates[0])
        local_paths.append(str(chosen) if chosen else None)

    out["local_path"] = local_paths
    return out


def build_layer_matrix(mapped: pd.DataFrame, layer: str, log) -> pd.DataFrame:
    rows = mapped[(mapped["layer"] == layer) & mapped["local_path"].notna()].copy()
    if rows.empty:
        raise RuntimeError(f"No downloaded local files found for required layer '{layer}'.")

    rows = rows.drop_duplicates(subset=["sample_barcode", "file_name"])
    sample_to_series = {}
    failures = 0

    for _, r in rows.iterrows():
        sample_id = str(r.get("sample_barcode", ""))
        if not sample_id or sample_id == "nan":
            continue
        path = Path(r["local_path"])
        if sample_id in sample_to_series:
            continue
        try:
            s = parse_mutation_file(path) if layer == "mutation" else parse_numeric_series(path, layer=layer)
            sample_to_series[sample_id] = s
        except Exception as e:
            failures += 1
            log.warning("Failed parsing %s file %s: %s", layer, path.name, e)

    if not sample_to_series:
        raise RuntimeError(f"All parsers failed for required layer '{layer}'.")

    mat = pd.DataFrame(sample_to_series).T
    if layer == "mutation":
        mat = mat.fillna(0).astype("int8")
    mat.index.name = "sample_id"
    mat = mat.reset_index()
    mat["patient_id"] = mat["sample_id"].map(lambda x: to_patient_id(str(x), 3))

    # Keep deterministic column order
    id_cols = ["sample_id", "patient_id"]
    feat_cols = sorted([c for c in mat.columns if c not in id_cols])
    mat = mat[id_cols + feat_cols]

    log.info("Layer %s parsed samples=%s features=%s failures=%s", layer, mat.shape[0], len(feat_cols), failures)
    return mat


def apply_qc(df: pd.DataFrame, layer: str, max_feature_missing_frac=0.3, max_sample_missing_frac=0.3):
    id_cols = ["sample_id", "patient_id"]
    feat_cols = [c for c in df.columns if c not in id_cols]
    x = df[feat_cols]

    if layer == "mutation":
        out = pd.concat([df[id_cols], x.fillna(0)], axis=1)
        keep_cols = [c for c in out.columns if c not in id_cols]
    else:
        feat_keep = x.isna().mean(axis=0) <= max_feature_missing_frac
        keep_cols = [c for c in feat_cols if feat_keep.get(c, False)]
        out = pd.concat([df[id_cols], df[keep_cols]], axis=1)

    sample_missing = out[keep_cols].isna().mean(axis=1) if keep_cols else pd.Series(1.0, index=out.index)
    out = out.loc[sample_missing <= max_sample_missing_frac, :].reset_index(drop=True)
    return out


def fetch_clinical_from_gdc(project_id: str, retries: int = 4, timeout: int = 120) -> pd.DataFrame:
    endpoint = "https://api.gdc.cancer.gov/cases"
    payload = {
        "filters": {
            "op": "in",
            "content": {"field": "project.project_id", "value": [project_id]},
        },
        "format": "JSON",
        "size": 5000,
        "fields": ",".join(
            [
                "submitter_id",
                "diagnoses.days_to_death",
                "diagnoses.days_to_last_follow_up",
                "diagnoses.ajcc_pathologic_stage",
                "demographic.vital_status",
            ]
        ),
    }

    last = None
    for i in range(retries):
        try:
            r = requests.post(endpoint, json=payload, timeout=timeout)
            r.raise_for_status()
            hits = r.json().get("data", {}).get("hits", [])
            rows = []
            for h in hits:
                pid = h.get("submitter_id")
                diagnoses = h.get("diagnoses", []) or []
                d_death = [d.get("days_to_death") for d in diagnoses if d.get("days_to_death") is not None]
                d_lfu = [d.get("days_to_last_follow_up") for d in diagnoses if d.get("days_to_last_follow_up") is not None]
                stage = next((d.get("ajcc_pathologic_stage") for d in diagnoses if d.get("ajcc_pathologic_stage")), None)
                rows.append(
                    {
                        "patient_id": pid,
                        "days_to_death": max(d_death) if d_death else np.nan,
                        "days_to_last_follow_up": max(d_lfu) if d_lfu else np.nan,
                        "vital_status": h.get("demographic", {}).get("vital_status"),
                        "stage_group": stage,
                    }
                )
            return pd.DataFrame(rows).drop_duplicates("patient_id")
        except Exception as e:
            last = e
    raise RuntimeError(f"Failed fetching clinical data from GDC API: {last}")


def main():
    args = parse_args(extra=True)
    cfg = read_yaml(args.config)
    log = setup_logger("qc")

    raw_gdc = Path(cfg["paths"]["raw_gdc"])
    interim = Path(cfg["paths"]["interim"])
    interim.mkdir(parents=True, exist_ok=True)

    manifest_path = raw_gdc / "gdc_download_manifest.tsv"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    manifest = pd.read_csv(manifest_path, sep="\t")
    if manifest.empty:
        raise RuntimeError("GDC manifest is empty. Download stage did not return files.")

    selected_manifest_path = Path(cfg["paths"]["manifests"]) / "selected_for_run.tsv"
    if selected_manifest_path.exists():
        selected = pd.read_csv(selected_manifest_path, sep="\t")
        if not selected.empty and "file_id" in selected.columns:
            keep_ids = set(selected["file_id"].astype(str))
            manifest = manifest[manifest["file_id"].astype(str).isin(keep_ids)].copy()

    mapped = map_manifest_to_local_files(manifest, raw_gdc)
    miss_cfg = cfg["qc"]["missingness"]

    layer_dfs = {}
    summaries = []
    required_layers = list(cfg.get("analysis", {}).get("main_layers", ["rna", "cna", "methylation", "mutation"]))
    optional_layers = []
    for layer in cfg.get("analysis", {}).get("optional_layers", []):
        if layer != "protein":
            continue
        has_layer_in_manifest = (manifest["layer"] == layer).any()
        has_local = ((mapped["layer"] == layer) & mapped["local_path"].notna()).any()
        if has_layer_in_manifest and has_local:
            optional_layers.append(layer)

    layers_to_parse = required_layers + optional_layers

    for layer in layers_to_parse:
        layer_df = build_layer_matrix(mapped, layer, log)
        layer_df = apply_qc(
            layer_df,
            layer=layer,
            max_feature_missing_frac=miss_cfg.get("max_feature_missing_frac", 0.3),
            max_sample_missing_frac=miss_cfg.get("max_sample_missing_frac", 0.3),
        )

        if layer == "methylation":
            feat_cols = [c for c in layer_df.columns if c not in ["sample_id", "patient_id"]]
            if feat_cols:
                v = layer_df[feat_cols].var(axis=0, skipna=True)
                keep = v[v >= float(cfg["qc"]["methylation"].get("min_probe_variance", 0.01))].index.tolist()
                layer_df = pd.concat([layer_df[["sample_id", "patient_id"]], layer_df[keep]], axis=1)

        if layer == "mutation":
            feat_cols = [c for c in layer_df.columns if c not in ["sample_id", "patient_id"]]
            if feat_cols:
                min_mut = int(cfg["qc"]["mutation"].get("min_mutated_samples", 5))
                keep = [c for c in feat_cols if layer_df[c].fillna(0).sum() >= min_mut]
                layer_df = pd.concat([layer_df[["sample_id", "patient_id"]], layer_df[keep]], axis=1)
                layer_df[keep] = layer_df[keep].fillna(0).astype("int8")

        out = interim / f"{layer}_matrix.parquet"
        layer_df.to_parquet(out, index=False)

        summaries.append(
            {
                "layer": layer,
                "n_samples": int(layer_df["sample_id"].nunique()),
                "n_features": int(len([c for c in layer_df.columns if c not in ["sample_id", "patient_id"]])),
                "n_manifest_files": int((manifest["layer"] == layer).sum()),
                "n_local_files": int(((mapped["layer"] == layer) & mapped["local_path"].notna()).sum()),
            }
        )

        layer_dfs[layer] = layer_df

    clinical = fetch_clinical_from_gdc(
        project_id=cfg["cohort_filters"]["project_id"],
        retries=int(cfg["download"].get("retry", 4)),
        timeout=int(cfg["download"].get("timeout_sec", 120)),
    )

    if clinical.empty:
        raise RuntimeError("Clinical table is empty from GDC API.")

    clinical.to_csv(interim / "clinical.csv", index=False)

    pd.DataFrame(summaries).to_csv("results/tables/pre_qc_layer_summary.csv", index=False)
    write_flag(str(interim / "qc_complete.flag"))
    log.info("QC complete using real GDC files only. Manifest rows: %s", len(manifest))


if __name__ == "__main__":
    main()
