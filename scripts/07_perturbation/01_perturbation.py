from pathlib import Path
import sys

import networkx as nx
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


def build_graph(edges: pd.DataFrame) -> nx.Graph:
    G = nx.Graph()
    for _, r in edges.iterrows():
        G.add_edge(r["source"], r["target"], weight=abs(float(r["weight"])))
    return G


def perturb_delta(G: nx.Graph, hub: str, frac: float) -> tuple[float, float]:
    base_pr = nx.pagerank(G, weight="weight") if G.number_of_nodes() > 0 else {}
    H = G.copy()
    if hub in H:
        for n in list(H.neighbors(hub)):
            w = H[hub][n].get("weight", 1.0)
            H[hub][n]["weight"] = max(0.0, w * (1.0 - frac))
    pr2 = nx.pagerank(H, weight="weight") if H.number_of_nodes() > 0 else {}
    delta_hub = pr2.get(hub, 0.0) - base_pr.get(hub, 0.0)
    delta_global = sum(abs(pr2.get(k, 0.0) - base_pr.get(k, 0.0)) for k in base_pr.keys())
    return float(delta_hub), float(delta_global)


def main():
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("perturbation")

    net_dir = Path(cfg["paths"]["results_networks"])
    table_dir = Path(cfg["paths"]["results_tables"])
    table_dir.mkdir(parents=True, exist_ok=True)

    edges = pd.read_csv(net_dir / "multilayer_network_edges.csv")
    centrality = pd.read_csv(net_dir / "network_centrality.csv")

    top_n = int(cfg["perturbation"].get("top_hubs_to_test", 20))
    frac = float(cfg["perturbation"].get("perturb_fraction", 0.5))
    n_boot = int(cfg["perturbation"].get("bootstrap_iters", 200))
    seed = int(cfg.get("project", {}).get("seed", 42))

    hubs = centrality.head(top_n)["node"].tolist()

    G = build_graph(edges)

    rows = []
    for hub in hubs:
        delta_hub, delta_global = perturb_delta(G, hub, frac)
        rows.append(
            {
                "hub": hub,
                "perturb_type": "edge_weight_dampening",
                "perturb_fraction": frac,
                "delta_hub_pagerank": delta_hub,
                "delta_global_pagerank_l1": delta_global,
            }
        )

    out = pd.DataFrame(rows).sort_values("delta_global_pagerank_l1", ascending=False)

    # Bootstrap perturbation ranking/stability
    rng = np.random.default_rng(seed)
    hub_to_global = {h: [] for h in hubs}
    hub_to_hubdelta = {h: [] for h in hubs}
    hub_to_rank = {h: [] for h in hubs}
    hub_to_top5 = {h: 0 for h in hubs}

    if len(edges) > 0:
        for _ in range(n_boot):
            idx = rng.integers(0, len(edges), len(edges))
            e = edges.iloc[idx].reset_index(drop=True)
            Gb = build_graph(e)
            vals = []
            for h in hubs:
                dh, dg = perturb_delta(Gb, h, frac)
                hub_to_hubdelta[h].append(dh)
                hub_to_global[h].append(dg)
                vals.append((h, dg))

            vals_df = pd.DataFrame(vals, columns=["hub", "delta_global"])
            vals_df["rank"] = vals_df["delta_global"].rank(method="average", ascending=False)
            top5 = set(vals_df.sort_values("delta_global", ascending=False).head(5)["hub"])
            for _, r in vals_df.iterrows():
                h = r["hub"]
                hub_to_rank[h].append(float(r["rank"]))
                if h in top5:
                    hub_to_top5[h] += 1

    ci_rows = []
    for h in hubs:
        g = np.asarray(hub_to_global[h], dtype=float)
        d = np.asarray(hub_to_hubdelta[h], dtype=float)
        r = np.asarray(hub_to_rank[h], dtype=float)
        if len(g) == 0:
            ci_rows.append({"hub": h})
            continue
        ci_rows.append(
            {
                "hub": h,
                "delta_global_boot_mean": float(np.mean(g)),
                "delta_global_ci_low": float(np.percentile(g, 2.5)),
                "delta_global_ci_high": float(np.percentile(g, 97.5)),
                "delta_hub_boot_mean": float(np.mean(d)),
                "delta_hub_ci_low": float(np.percentile(d, 2.5)),
                "delta_hub_ci_high": float(np.percentile(d, 97.5)),
                "rank_boot_mean": float(np.mean(r)),
                "rank_ci_low": float(np.percentile(r, 2.5)),
                "rank_ci_high": float(np.percentile(r, 97.5)),
                "top5_freq": float(hub_to_top5[h] / n_boot),
            }
        )

    if ci_rows:
        out = out.merge(pd.DataFrame(ci_rows), on="hub", how="left")
    out.to_csv(table_dir / "perturbation_delta.csv", index=False)
    log.info("Perturbation complete for %s hubs", len(rows))


if __name__ == "__main__":
    main()
