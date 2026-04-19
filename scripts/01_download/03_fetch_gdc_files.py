from pathlib import Path
import sys
import tarfile
import time
from typing import Dict, List

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


def chunked(items: List[str], n: int):
    for i in range(0, len(items), n):
        yield items[i : i + n]


def post_data(ids: List[str], timeout: int = 600, retries: int = 4):
    url = "https://api.gdc.cancer.gov/data"
    payload = {"ids": ids}
    last = None
    for i in range(retries):
        try:
            resp = requests.post(url, json=payload, stream=True, timeout=timeout)
            resp.raise_for_status()
            return resp
        except Exception as e:
            last = e
            if i < retries - 1:
                time.sleep(2 * (i + 1))
    raise RuntimeError(f"Failed downloading ids batch: {last}")


def save_single_file_payload(payload_path: Path, file_id: str, file_name: str, files_root: Path) -> None:
    out_dir = files_root / file_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (file_name if file_name else f"{file_id}.dat")
    payload_path.replace(out_path)


def main():
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("fetch_gdc_files")

    raw_gdc = Path(cfg["paths"]["raw_gdc"])
    manifest_path = raw_gdc / "gdc_download_manifest.tsv"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    manifest = pd.read_csv(manifest_path, sep="\t")
    manifest = manifest[manifest["layer"].isin(["rna", "cna", "methylation", "mutation", "protein"])].copy()

    max_per_layer = int(cfg["download"].get("max_files_per_type", 200))
    chunk_size = int(cfg["download"].get("download_chunk_size", 6))
    timeout = int(cfg["download"].get("timeout_sec", 120)) * 5
    retries = int(cfg["download"].get("retry", 4))

    files_root = raw_gdc / "files"
    bundles_root = raw_gdc / "bundles"
    files_root.mkdir(parents=True, exist_ok=True)
    bundles_root.mkdir(parents=True, exist_ok=True)

    required_layers = list(cfg.get("analysis", {}).get("main_layers", ["rna", "cna", "methylation", "mutation"]))
    optional_layers = list(cfg.get("analysis", {}).get("optional_layers", []))
    include_protein = bool(cfg.get("download", {}).get("include_proteome_if_available", True))
    if include_protein and "protein" in optional_layers and (manifest["layer"] == "protein").any():
        target_layers = required_layers + ["protein"]
    else:
        target_layers = required_layers

    pats = {}
    for layer in required_layers:
        s = (
            manifest.loc[manifest["layer"] == layer, "sample_barcode"]
            .dropna()
            .astype(str)
            .replace({"": pd.NA, "nan": pd.NA})
            .dropna()
            .unique()
            .tolist()
        )
        pats[layer] = set(s)

    common_patients = set.intersection(*(pats[l] for l in required_layers))
    if not common_patients:
        raise RuntimeError("No common patients across required layers in manifest.")

    selected_patients = sorted(common_patients)[:max_per_layer]
    selected_ids: List[str] = []
    for layer in target_layers:
        sub = manifest[
            (manifest["layer"] == layer)
            & (manifest["sample_barcode"].astype(str).isin(selected_patients))
        ].copy()
        sub = sub.dropna(subset=["file_id", "sample_barcode"])
        sub = sub.drop_duplicates(subset=["sample_barcode"], keep="first")
        ids = sub["file_id"].astype(str).tolist()
        selected_ids.extend(ids)

    run_manifest = manifest[manifest["file_id"].astype(str).isin(set(selected_ids))].copy()
    run_manifest = run_manifest.drop_duplicates(subset=["layer", "sample_barcode", "file_id"])
    run_manifest_out = Path(cfg["paths"]["manifests"]) / "selected_for_run.tsv"
    run_manifest_out.parent.mkdir(parents=True, exist_ok=True)
    run_manifest.to_csv(run_manifest_out, sep="\t", index=False)
    id_to_name: Dict[str, str] = (
        run_manifest.dropna(subset=["file_id", "file_name"])
        .drop_duplicates(subset=["file_id"])
        .assign(file_id=lambda d: d["file_id"].astype(str))
        .set_index("file_id")["file_name"]
        .to_dict()
    )

    # Skip ids that already exist locally
    existing_ids = {p.name for p in files_root.iterdir() if p.is_dir()}
    pending_ids = [fid for fid in selected_ids if fid not in existing_ids]

    log.info(
        "Selected patients=%s ids=%s, already_present=%s, pending=%s",
        len(selected_patients),
        len(selected_ids),
        len(existing_ids & set(selected_ids)),
        len(pending_ids),
    )

    for idx, batch in enumerate(chunked(pending_ids, max(1, chunk_size)), start=1):
        log.info("Downloading batch %s with %s files", idx, len(batch))
        resp = post_data(batch, timeout=timeout, retries=retries)
        bundle_path = bundles_root / f"bundle_{idx:04d}.tar.gz"
        with open(bundle_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        extracted = False
        try:
            with tarfile.open(bundle_path, "r:gz") as tar:
                tar.extractall(path=files_root)
            extracted = True
            log.info("Extracted %s", bundle_path.name)
        except Exception as e:
            log.warning("Batch %s extraction failed (%s). Retrying ids one-by-one.", idx, e)

        if not extracted:
            for j, fid in enumerate(batch, start=1):
                try:
                    r2 = post_data([fid], timeout=timeout, retries=retries)
                    b2 = bundles_root / f"bundle_{idx:04d}_{j:03d}_{fid}.tar.gz"
                    with open(b2, "wb") as f2:
                        for c2 in r2.iter_content(chunk_size=1024 * 1024):
                            if c2:
                                f2.write(c2)
                    try:
                        with tarfile.open(b2, "r:gz") as t2:
                            t2.extractall(path=files_root)
                    except Exception:
                        save_single_file_payload(
                            payload_path=b2,
                            file_id=fid,
                            file_name=id_to_name.get(fid, f"{fid}.dat"),
                            files_root=files_root,
                        )
                except Exception as e2:
                    log.warning("Single-id retry failed for %s: %s", fid, e2)

    # Report local coverage
    local_dirs = {p.name for p in files_root.iterdir() if p.is_dir()}
    got = len(local_dirs & set(selected_ids))
    log.info("Download complete. Local file-id directories matched=%s / %s", got, len(selected_ids))


if __name__ == "__main__":
    main()
