import argparse
import json
import logging
import os
from pathlib import Path
from typing import Dict, Any

import numpy as np
import pandas as pd
import yaml


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def parse_args(extra: bool = False):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    if extra:
        parser.add_argument("--thresholds", required=False)
    return parser.parse_args()


def read_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_dirs(paths):
    for p in paths:
        Path(p).mkdir(parents=True, exist_ok=True)


def to_patient_id(tcga_barcode: str, parts: int = 3) -> str:
    if not isinstance(tcga_barcode, str) or "-" not in tcga_barcode:
        return tcga_barcode
    return "-".join(tcga_barcode.split("-")[:parts])


def survival_group(df: pd.DataFrame, time_col: str, event_col: str) -> pd.Series:
    t = df[time_col].fillna(df[time_col].median())
    threshold = float(np.median(t))
    return np.where(t >= threshold, "high_risk", "low_risk")


def save_json(obj: Dict[str, Any], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def write_flag(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("ok\n")
