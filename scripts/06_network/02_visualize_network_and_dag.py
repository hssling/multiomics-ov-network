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


def node_layer(node: str) -> str:
    if str(node).startswith("rna_module_"):
        return "RNA"
    if str(node).startswith("protein_module_"):
        return "Protein"
    if str(node).startswith("LF"):
        return "Latent"
    if str(node).endswith("_burden"):
        return "Input"
    if str(node).startswith("comp"):
        return "Outcome"
    return "Other"


def layer_color(layer: str) -> str:
    return {
        "Input": "#B03A2E",
        "RNA": "#1F618D",
        "Latent": "#117A65",
        "Protein": "#7D3C98",
        "Outcome": "#AF601A",
        "Other": "#6C757D",
    }.get(layer, "#6C757D")


def draw_multilayer_network(edges: pd.DataFrame, out_png: Path):
    if edges.empty:
        return
    g = nx.Graph()
    for _, r in edges.iterrows():
        g.add_edge(r["source"], r["target"], weight=abs(float(r["weight"])))

    cent = nx.degree_centrality(g)
    pos = nx.spring_layout(g, k=0.7, seed=42, weight="weight")
    nodes = list(g.nodes())
    layers = [node_layer(n) for n in nodes]
    colors = [layer_color(l) for l in layers]
    sizes = [450 + 4500 * cent.get(n, 0.0) for n in nodes]
    widths = [0.5 + 2.0 * abs(g[u][v].get("weight", 0.0)) for u, v in g.edges()]

    fig, ax = plt.subplots(figsize=(12, 9))
    nx.draw_networkx_edges(g, pos, width=widths, alpha=0.20, edge_color="#444444", ax=ax)
    nx.draw_networkx_nodes(g, pos, node_size=sizes, node_color=colors, alpha=0.9, linewidths=0.4, edgecolors="black", ax=ax)

    # Label only major nodes to keep readability.
    major = sorted(nodes, key=lambda n: cent.get(n, 0.0), reverse=True)[:25]
    labels = {n: n for n in major}
    nx.draw_networkx_labels(g, pos, labels=labels, font_size=7, ax=ax)
    ax.set_title("Integrated Multi-Layer Network (TCGA-OV)")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out_png, dpi=180)
    plt.close(fig)


def build_dag(edges: pd.DataFrame, out_csv: Path) -> pd.DataFrame:
    if edges.empty:
        dag = pd.DataFrame(columns=["source", "target", "weight", "etype", "source_layer", "target_layer"])
        dag.to_csv(out_csv, index=False)
        return dag

    d = edges.copy()
    d["source_layer"] = d["source"].map(node_layer)
    d["target_layer"] = d["target"].map(node_layer)

    layer_rank = {"Input": 0, "RNA": 1, "Latent": 2, "Protein": 3, "Outcome": 4, "Other": 2}
    s_rank = d["source_layer"].map(layer_rank).fillna(2)
    t_rank = d["target_layer"].map(layer_rank).fillna(2)

    # Orient edges to preserve input -> output flow for a DAG-like interpretation.
    flip = s_rank > t_rank
    d.loc[flip, ["source", "target"]] = d.loc[flip, ["target", "source"]].to_numpy()
    d.loc[flip, ["source_layer", "target_layer"]] = d.loc[flip, ["target_layer", "source_layer"]].to_numpy()

    # Keep cross-layer and known directional edge types for causal pathway interpretation.
    keep_etypes = {"input_to_latent", "latent_to_outcome"}
    keep = (d["source_layer"] != d["target_layer"]) | d["etype"].isin(keep_etypes)
    dag = d.loc[keep, ["source", "target", "weight", "etype", "source_layer", "target_layer"]].copy()
    dag = dag.sort_values("weight", ascending=False).head(120).reset_index(drop=True)
    dag.to_csv(out_csv, index=False)
    return dag


def draw_dag(dag_edges: pd.DataFrame, out_png: Path):
    if dag_edges.empty:
        return
    g = nx.DiGraph()
    for _, r in dag_edges.iterrows():
        g.add_edge(r["source"], r["target"], weight=abs(float(r["weight"])))

    layers = {n: node_layer(n) for n in g.nodes()}
    x_map = {"Input": 0.0, "RNA": 1.0, "Latent": 2.0, "Protein": 3.0, "Outcome": 4.0, "Other": 2.0}
    pos = {}
    for layer in ["Input", "RNA", "Latent", "Protein", "Outcome", "Other"]:
        ln = [n for n, l in layers.items() if l == layer]
        for i, n in enumerate(sorted(ln)):
            y = 0.0 if len(ln) == 1 else (i / (len(ln) - 1)) * 2.0 - 1.0
            pos[n] = (x_map[layer], y)

    in_deg = dict(g.in_degree())
    out_deg = dict(g.out_degree())
    size = [400 + 130 * (in_deg.get(n, 0) + out_deg.get(n, 0)) for n in g.nodes()]
    color = [layer_color(layers[n]) for n in g.nodes()]

    fig, ax = plt.subplots(figsize=(14, 6.5))
    nx.draw_networkx_edges(
        g,
        pos,
        alpha=0.30,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=9,
        width=1.0,
        edge_color="#555555",
        ax=ax,
    )
    nx.draw_networkx_nodes(g, pos, node_size=size, node_color=color, alpha=0.92, linewidths=0.4, edgecolors="black", ax=ax)

    top_nodes = sorted(g.nodes(), key=lambda n: in_deg.get(n, 0) + out_deg.get(n, 0), reverse=True)[:30]
    nx.draw_networkx_labels(g, pos, labels={n: n for n in top_nodes}, font_size=7, ax=ax)
    ax.set_title("DAG-Style Input -> Output Pathway Map")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out_png, dpi=180)
    plt.close(fig)


def main():
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("network_viz")

    networks = Path(cfg["paths"]["results_networks"])
    figures = Path(cfg["paths"]["results_figures"])
    networks.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)

    edges_path = networks / "multilayer_network_edges.csv"
    edges = pd.read_csv(edges_path) if edges_path.exists() else pd.DataFrame()

    draw_multilayer_network(edges, figures / "multilayer_network_graph.png")
    dag = build_dag(edges, networks / "dag_pathways.csv")
    draw_dag(dag, figures / "dag_pathway_graph.png")
    log.info("Network visualization complete: %s edges, %s DAG edges", len(edges), len(dag))


if __name__ == "__main__":
    main()

