from pathlib import Path
import sys

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger


def build_graph(edges: pd.DataFrame) -> nx.Graph:
    g = nx.Graph()
    for _, r in edges.iterrows():
        g.add_edge(r["source"], r["target"], weight=abs(float(r["weight"])))
    return g


def perturb_delta(g: nx.Graph, hub: str, frac: float) -> tuple[float, float]:
    base = nx.pagerank(g, weight="weight") if g.number_of_nodes() > 0 else {}
    h = g.copy()
    if hub in h:
        for n in list(h.neighbors(hub)):
            h[hub][n]["weight"] = max(0.0, h[hub][n].get("weight", 1.0) * (1.0 - frac))
    p2 = nx.pagerank(h, weight="weight") if h.number_of_nodes() > 0 else {}
    dh = p2.get(hub, 0.0) - base.get(hub, 0.0)
    dg = sum(abs(p2.get(k, 0.0) - base.get(k, 0.0)) for k in base)
    return float(dh), float(dg)


def main():
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("sensitivity")

    nets = Path(cfg["paths"]["results_networks"])
    tabs = Path(cfg["paths"]["results_tables"])
    figs = Path(cfg["paths"]["results_figures"])
    tabs.mkdir(parents=True, exist_ok=True)
    figs.mkdir(parents=True, exist_ok=True)

    edges = pd.read_csv(nets / "multilayer_network_edges.csv")
    cent = pd.read_csv(nets / "network_centrality.csv")
    hubs = cent.head(10)["node"].tolist()
    g = build_graph(edges)

    fractions = [0.1, 0.25, 0.5, 0.75, 0.9]
    rows = []
    for f in fractions:
        for h in hubs:
            dh, dg = perturb_delta(g, h, f)
            rows.append(
                {
                    "hub": h,
                    "perturb_fraction": f,
                    "delta_hub_pagerank": dh,
                    "delta_global_pagerank_l1": dg,
                }
            )
    sens = pd.DataFrame(rows)
    sens.to_csv(tabs / "sensitivity_perturb_fraction_grid.csv", index=False)

    # Aggregate robustness slope: does effect increase consistently as perturbation increases?
    slope_rows = []
    for h, d in sens.groupby("hub"):
        x = d["perturb_fraction"].values.astype(float)
        y = d["delta_global_pagerank_l1"].values.astype(float)
        slope = float(np.polyfit(x, y, deg=1)[0]) if len(x) >= 2 else np.nan
        monotonic = bool(np.all(np.diff(y[np.argsort(x)]) >= -1e-9))
        slope_rows.append({"hub": h, "delta_global_slope": slope, "monotonic_non_decreasing": monotonic})
    slope_df = pd.DataFrame(slope_rows).sort_values("delta_global_slope", ascending=False)
    slope_df.to_csv(tabs / "sensitivity_hub_slope_summary.csv", index=False)

    # Plot top hubs by global effect trajectory.
    fig, ax = plt.subplots(figsize=(8.5, 5))
    top = slope_df.head(6)["hub"].tolist()
    for h in top:
        d = sens[sens["hub"] == h].sort_values("perturb_fraction")
        ax.plot(d["perturb_fraction"], d["delta_global_pagerank_l1"], marker="o", label=h)
    ax.set_xlabel("Perturbation fraction")
    ax.set_ylabel("Delta global PageRank L1")
    ax.set_title("Sensitivity Curves: Hub Perturbation Strength vs Network Response")
    ax.legend(ncol=2, fontsize=8)
    fig.tight_layout()
    fig.savefig(figs / "sensitivity_perturbation_curves.png", dpi=170)
    plt.close(fig)
    log.info("Sensitivity experiments complete for %s hubs x %s fractions", len(hubs), len(fractions))


if __name__ == "__main__":
    main()

