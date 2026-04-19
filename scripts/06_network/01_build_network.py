from pathlib import Path
import sys

import networkx as nx
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


def corr_edges(df: pd.DataFrame, layer: str, threshold: float) -> pd.DataFrame:
    feats = [c for c in df.columns if c not in ["sample_id", "patient_id"]]
    X = df[feats]
    corr = X.corr().fillna(0.0)
    edges = []
    for i, a in enumerate(feats):
        for b in feats[i + 1 :]:
            w = float(corr.loc[a, b])
            if abs(w) >= threshold:
                edges.append({"source": a, "target": b, "weight": w, "etype": f"{layer}_co"})
    return pd.DataFrame(edges)


def centrality_table(G: nx.Graph) -> pd.DataFrame:
    deg = dict(G.degree())
    btw = nx.betweenness_centrality(G, normalized=True) if G.number_of_nodes() > 0 else {}
    pr = nx.pagerank(G, weight="weight") if G.number_of_nodes() > 0 else {}
    cent = pd.DataFrame(
        {
            "node": list(G.nodes()),
            "degree": [deg.get(n, 0) for n in G.nodes()],
            "betweenness": [btw.get(n, 0.0) for n in G.nodes()],
            "pagerank": [pr.get(n, 0.0) for n in G.nodes()],
        }
    )
    if not cent.empty:
        cent["rank_score"] = cent[["degree", "betweenness", "pagerank"]].rank(pct=True).mean(axis=1)
    else:
        cent["rank_score"] = []
    return cent


def bootstrap_stability(edges_df: pd.DataFrame, base_cent: pd.DataFrame, top_k: int, n_boot: int = 200, seed: int = 42) -> pd.DataFrame:
    if edges_df.empty or base_cent.empty:
        return pd.DataFrame(columns=["node", "rank_score_mean", "rank_score_ci_low", "rank_score_ci_high", "topk_freq"])

    rng = np.random.default_rng(seed)
    nodes = base_cent["node"].tolist()
    ranks = {n: [] for n in nodes}
    top_hits = {n: 0 for n in nodes}
    e = edges_df.reset_index(drop=True)

    for _ in range(n_boot):
        idx = rng.integers(0, len(e), len(e))
        samp = e.iloc[idx]
        G = nx.Graph()
        for _, r in samp.iterrows():
            s, t = r["source"], r["target"]
            w = abs(float(r["weight"]))
            if G.has_edge(s, t):
                G[s][t]["weight"] += w
            else:
                G.add_edge(s, t, weight=w, etype=r.get("etype", "boot"))

        c = centrality_table(G)
        c_map = dict(zip(c["node"], c["rank_score"])) if not c.empty else {}
        for n in nodes:
            ranks[n].append(float(c_map.get(n, 0.0)))

        if not c.empty:
            top_nodes = set(c.sort_values("rank_score", ascending=False).head(min(top_k, len(c)))["node"])
            for n in top_nodes:
                if n in top_hits:
                    top_hits[n] += 1

    rows = []
    for n in nodes:
        arr = np.asarray(ranks[n], dtype=float)
        rows.append(
            {
                "node": n,
                "rank_score_mean": float(np.mean(arr)),
                "rank_score_ci_low": float(np.percentile(arr, 2.5)),
                "rank_score_ci_high": float(np.percentile(arr, 97.5)),
                "topk_freq": float(top_hits[n] / n_boot),
            }
        )
    return pd.DataFrame(rows)


def main():
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("network")

    processed = Path(cfg["paths"]["processed"])
    out_dir = Path(cfg["paths"]["results_networks"])
    out_dir.mkdir(parents=True, exist_ok=True)

    rna = pd.read_parquet(processed / "rna_modules.parquet")
    burdens = pd.read_parquet(processed / "burden_features.parquet")
    protein_path = processed / "protein_modules.parquet"
    protein = pd.read_parquet(protein_path) if protein_path.exists() else None
    mofa = pd.read_csv(Path(cfg["paths"]["results_models"]) / "mofa_factors.csv")
    diablo = pd.read_csv(Path(cfg["paths"]["results_models"]) / "diablo_scores.csv")

    common = sorted(set(rna["patient_id"]) & set(burdens["patient_id"]) & set(mofa["patient_id"]) & set(diablo["patient_id"]))
    if protein is not None:
        common = sorted(set(common) & set(protein["patient_id"]))

    def keep(df):
        return df[df["patient_id"].isin(common)].reset_index(drop=True)

    rna = keep(rna)
    burdens = keep(burdens)
    mofa = keep(mofa)
    diablo = keep(diablo)
    if protein is not None:
        protein = keep(protein)

    thr = float(cfg["network"]["corr_threshold"])
    edges = []
    edges.append(corr_edges(rna, "rna", thr))
    edges.append(corr_edges(burdens, "burden", thr))
    if protein is not None and not protein.empty:
        edges.append(corr_edges(protein, "protein", thr))

    merged = rna.merge(burdens, on=["sample_id", "patient_id"], how="inner")
    if protein is not None and not protein.empty:
        merged = merged.merge(protein, on=["sample_id", "patient_id"], how="inner")
    merged = merged.merge(mofa, on="patient_id", how="inner")

    X_cols = [c for c in merged.columns if c.startswith("rna_module_") or c.endswith("_burden") or c.startswith("protein_module_")]
    Y_cols = [c for c in merged.columns if c.startswith("LF")]

    for x in X_cols:
        xv = merged[x]
        for y in Y_cols:
            w = float(np.corrcoef(xv, merged[y])[0, 1]) if merged[y].std() > 0 and xv.std() > 0 else 0.0
            if abs(w) >= thr:
                edges.append(pd.DataFrame([{"source": x, "target": y, "weight": w, "etype": "input_to_latent"}]))

    D = diablo[["patient_id", "comp1", "comp2"]]
    M = merged.merge(D, on="patient_id", how="inner")
    for y in Y_cols:
        for z in ["comp1", "comp2"]:
            w = float(np.corrcoef(M[y], M[z])[0, 1]) if M[y].std() > 0 and M[z].std() > 0 else 0.0
            if abs(w) >= thr:
                edges.append(pd.DataFrame([{"source": y, "target": z, "weight": w, "etype": "latent_to_outcome"}]))

    edges_df = pd.concat([e for e in edges if not e.empty], ignore_index=True)
    edges_df.to_csv(out_dir / "multilayer_network_edges.csv", index=False)

    G = nx.Graph()
    for _, row in edges_df.iterrows():
        G.add_edge(row["source"], row["target"], weight=abs(float(row["weight"])), etype=row["etype"])

    cent = centrality_table(G)
    cent = cent.sort_values("rank_score", ascending=False)
    cent.to_csv(out_dir / "network_centrality.csv", index=False)

    stab = bootstrap_stability(
        edges_df=edges_df,
        base_cent=cent,
        top_k=int(cfg["network"].get("top_hubs", 50)),
        n_boot=int(cfg["network"].get("bootstrap_iters", 200)),
        seed=int(cfg["project"].get("seed", 42)),
    )
    if not stab.empty:
        stab = cent[["node", "rank_score"]].merge(stab, on="node", how="left").sort_values("rank_score", ascending=False)
    stab.to_csv(out_dir / "network_centrality_stability.csv", index=False)

    log.info("Network built with %s nodes and %s edges", G.number_of_nodes(), G.number_of_edges())


if __name__ == "__main__":
    main()
