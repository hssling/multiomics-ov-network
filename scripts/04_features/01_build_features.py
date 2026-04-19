from pathlib import Path
import sys

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger, write_flag


def safe_to_parquet(df: pd.DataFrame, path: Path, log) -> None:
    try:
        df.to_parquet(path, index=False)
    except Exception as e:
        log.warning("Parquet write failed for %s: %s. Continuing with CSV output.", path.name, e)


def zscore_df(df: pd.DataFrame, id_cols=("sample_id", "patient_id")) -> pd.DataFrame:
    features = [c for c in df.columns if c not in id_cols]
    scaler = StandardScaler(with_mean=True, with_std=True)
    arr = scaler.fit_transform(df[features].fillna(0.0))
    out = pd.concat(
        [
            df[list(id_cols)].reset_index(drop=True),
            pd.DataFrame(arr, columns=features, index=df.index).reset_index(drop=True),
        ],
        axis=1,
    )
    return out


def burden_features(mut_df: pd.DataFrame, cna_df: pd.DataFrame, meth_df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({"sample_id": mut_df["sample_id"], "patient_id": mut_df["patient_id"]})
    mut_feats = [c for c in mut_df.columns if c not in ["sample_id", "patient_id"]]
    cna_feats = [c for c in cna_df.columns if c not in ["sample_id", "patient_id"]]
    meth_feats = [c for c in meth_df.columns if c not in ["sample_id", "patient_id"]]
    out["mutation_burden"] = mut_df[mut_feats].sum(axis=1)
    out["cna_burden"] = cna_df[cna_feats].abs().sum(axis=1)
    out["methylation_burden"] = meth_df[meth_feats].mean(axis=1)
    return out


def module_scores(df: pd.DataFrame, prefix: str, n_components: int = 50) -> pd.DataFrame:
    feats = [c for c in df.columns if c not in ["sample_id", "patient_id"]]
    n_components = min(n_components, len(feats), max(2, len(df) - 1))
    pca = PCA(n_components=n_components, random_state=42)
    scores = pca.fit_transform(df[feats])
    cols = [f"{prefix}_module_{i+1:03d}" for i in range(scores.shape[1])]
    out = df[["sample_id", "patient_id"]].copy()
    out[cols] = scores
    return out


def main():
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("features")

    interim = Path(cfg["paths"]["interim"])
    processed = Path(cfg["paths"]["processed"])
    processed.mkdir(parents=True, exist_ok=True)

    master = pd.read_csv(Path(cfg["paths"]["sample_maps"]) / "master_sample_sheet.csv")
    matched = set(master.loc[master["matched_all_main_layers"] == 1, "patient_id"])

    rna = pd.read_parquet(interim / "rna_matrix.parquet")
    cna = pd.read_parquet(interim / "cna_matrix.parquet")
    meth = pd.read_parquet(interim / "methylation_matrix.parquet")
    mut = pd.read_parquet(interim / "mutation_matrix.parquet")

    protein_path = interim / "protein_matrix.parquet"
    protein = pd.read_parquet(protein_path) if protein_path.exists() else None

    def filt(df):
        return df[df["patient_id"].isin(matched)].reset_index(drop=True)

    rna, cna, meth, mut = map(filt, [rna, cna, meth, mut])
    if protein is not None:
        protein = filt(protein)

    rna_z = zscore_df(rna)
    cna_z = zscore_df(cna)
    meth_z = zscore_df(meth)
    mut_bin = mut.copy()

    rna_modules = module_scores(rna_z, prefix="rna", n_components=cfg["features"].get("module_n_components", 50))
    burdens = burden_features(mut_bin, cna_z, meth_z)

    clinical = pd.read_csv(interim / "clinical.csv")
    clinical2 = clinical.copy()
    t = clinical2["days_to_death"].fillna(clinical2["days_to_last_follow_up"]).fillna(0)
    thr = float(t.median())
    # Shorter observed time is treated as higher risk for benchmark supervision.
    clinical2["survival_risk_group"] = pd.Series(["high_risk" if x <= thr else "low_risk" for x in t], index=clinical2.index)
    outcome = master[["patient_id"]].merge(clinical2, on="patient_id", how="left")

    safe_to_parquet(rna_z, processed / "rna_z.parquet", log)
    rna_z.to_csv(processed / "rna_z.csv", index=False)
    safe_to_parquet(cna_z, processed / "cna_z.parquet", log)
    cna_z.to_csv(processed / "cna_z.csv", index=False)
    safe_to_parquet(meth_z, processed / "methylation_z.parquet", log)
    meth_z.to_csv(processed / "methylation_z.csv", index=False)
    safe_to_parquet(mut_bin, processed / "mutation_binary.parquet", log)
    mut_bin.to_csv(processed / "mutation_binary.csv", index=False)
    safe_to_parquet(rna_modules, processed / "rna_modules.parquet", log)
    rna_modules.to_csv(processed / "rna_modules.csv", index=False)
    safe_to_parquet(burdens, processed / "burden_features.parquet", log)
    burdens.to_csv(processed / "burden_features.csv", index=False)
    outcome.to_csv(processed / "outcomes.csv", index=False)

    summary_rows = [
        {"layer": "rna", "n_samples": len(rna_z), "n_features": rna_z.shape[1] - 2},
        {"layer": "cna", "n_samples": len(cna_z), "n_features": cna_z.shape[1] - 2},
        {"layer": "methylation", "n_samples": len(meth_z), "n_features": meth_z.shape[1] - 2},
        {"layer": "mutation", "n_samples": len(mut_bin), "n_features": mut_bin.shape[1] - 2},
        {"layer": "rna_modules", "n_samples": len(rna_modules), "n_features": rna_modules.shape[1] - 2},
        {"layer": "burdens", "n_samples": len(burdens), "n_features": burdens.shape[1] - 2},
    ]

    if protein is not None and not protein.empty:
        protein_z = zscore_df(protein)
        protein_modules = module_scores(
            protein_z,
            prefix="protein",
            n_components=min(20, cfg["features"].get("module_n_components", 50)),
        )
        safe_to_parquet(protein_z, processed / "protein_z.parquet", log)
        protein_z.to_csv(processed / "protein_z.csv", index=False)
        safe_to_parquet(protein_modules, processed / "protein_modules.parquet", log)
        protein_modules.to_csv(processed / "protein_modules.csv", index=False)
        summary_rows.append({"layer": "protein", "n_samples": len(protein_z), "n_features": protein_z.shape[1] - 2})
        summary_rows.append(
            {"layer": "protein_modules", "n_samples": len(protein_modules), "n_features": protein_modules.shape[1] - 2}
        )

    pd.DataFrame(summary_rows).to_csv("results/tables/feature_count_summary.csv", index=False)
    write_flag(str(processed / "features_complete.flag"))
    log.info("Feature engineering complete for %s matched patients", len(rna_z))


if __name__ == "__main__":
    main()
