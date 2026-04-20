from pathlib import Path
import hashlib
import sys

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


CHUNK_SIZE = 1024 * 1024


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, out_path: Path, log) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and out_path.stat().st_size > 0:
        log.info("Exists, skipping download: %s", out_path)
        return
    log.info("Downloading %s -> %s", url, out_path)
    with requests.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        with out_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    handle.write(chunk)


def main() -> None:
    args = parse_args()
    cfg = read_yaml(args.config)
    ext_cfg = read_yaml(ROOT / "configs" / "external_validation.yaml")
    log = setup_logger("fetch_external_validation")

    raw_root = ROOT / "data" / "raw" / "external_validation"
    raw_root.mkdir(parents=True, exist_ok=True)
    tables = ROOT / cfg["paths"]["results_tables"]

    ovarian_xlsx_url = (
        "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE160nnn/GSE160705/suppl/"
        "GSE160705_Raw_data_read_counts_and_normalized_read_counts.xlsx"
    )
    ovarian_xlsx = raw_root / "GSE160705" / "GSE160705_Raw_data_read_counts_and_normalized_read_counts.xlsx"
    download(ovarian_xlsx_url, ovarian_xlsx, log)

    run_map = {
        "SRR31001810": [
            "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR310/010/SRR31001810/SRR31001810_1.fastq.gz",
            "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR310/010/SRR31001810/SRR31001810_2.fastq.gz",
        ]
    }
    for run, urls in run_map.items():
        for url in urls:
            out_path = raw_root / "car_benchmark" / run / Path(url).name
            download(url, out_path, log)

    rows = []
    for path in [ovarian_xlsx] + sorted((raw_root / "car_benchmark").rglob("*.gz")):
        rows.append(
            {
                "path": str(path.relative_to(ROOT)),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    pd.DataFrame(rows).to_csv(tables / "external_validation_file_inventory.csv", index=False)
    log.info("Wrote external validation file inventory for %s files", len(rows))


if __name__ == "__main__":
    main()

