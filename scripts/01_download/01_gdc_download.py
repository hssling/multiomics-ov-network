import time
from pathlib import Path
import sys

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger, write_flag, save_json


def gdc_post(url, payload, retries=4, timeout=120):
    for i in range(retries):
        try:
            r = requests.post(url, json=payload, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(2 * (i + 1))


def main():
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("download_gdc")

    project = cfg["cohort_filters"]["project_id"]
    raw_gdc = Path(cfg["paths"]["raw_gdc"])
    raw_gdc.mkdir(parents=True, exist_ok=True)

    base = "https://api.gdc.cancer.gov/files"
    retries = int(cfg["download"].get("retry", 4))
    timeout = int(cfg["download"].get("timeout_sec", 120))

    rows = []
    for layer, data_type in cfg["cohort_filters"]["data_types"].items():
        filters = {
            "op": "and",
            "content": [
                {"op": "in", "content": {"field": "cases.project.project_id", "value": [project]}},
                {"op": "in", "content": {"field": "data_type", "value": [data_type]}},
                {"op": "in", "content": {"field": "access", "value": ["open"]}},
            ],
        }
        payload = {
            "filters": filters,
            "format": "JSON",
            "size": cfg["download"].get("request_size", 2000),
            "fields": "file_id,file_name,data_type,data_format,cases.case_id,cases.submitter_id",
        }

        log.info("Querying GDC for layer=%s data_type=%s", layer, data_type)
        try:
            data = gdc_post(base, payload, retries=retries, timeout=timeout)
            hits = data.get("data", {}).get("hits", [])
            for h in hits:
                cases = h.get("cases", [])
                submitter_id = cases[0].get("submitter_id") if cases else None
                rows.append(
                    {
                        "layer": layer,
                        "file_id": h.get("file_id"),
                        "file_name": h.get("file_name"),
                        "data_type": h.get("data_type"),
                        "data_format": h.get("data_format"),
                        "sample_barcode": submitter_id,
                    }
                )
            log.info("Found %s files for %s", len(hits), layer)
        except Exception as e:
            log.warning("Failed querying %s: %s", layer, e)

    manifest = pd.DataFrame(rows)
    manifest_path = raw_gdc / "gdc_download_manifest.tsv"
    manifest.to_csv(manifest_path, sep="\t", index=False)

    summary = manifest.groupby("layer").size().to_dict() if not manifest.empty else {}
    save_json(summary, str(raw_gdc / "manifest_summary.json"))

    # Note: this script captures a reproducible manifest and metadata only.
    # Use gdc-client with the manifest to perform full bulk transfer.
    write_flag(str(raw_gdc / "download_complete.flag"))
    log.info("Manifest saved: %s rows", len(manifest))


if __name__ == "__main__":
    main()
