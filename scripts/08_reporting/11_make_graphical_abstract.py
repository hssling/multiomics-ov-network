
from __future__ import annotations

from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "results" / "figures"
TABLE_DIR = ROOT / "results" / "tables"
NET_DIR = ROOT / "results" / "networks"
JBI_DIR = ROOT / "manuscript" / "submission_package" / "targets" / "journal_of_biomedical_informatics"
OUT_MAIN = FIG_DIR / "graphical_abstract_journal.png"
OUT_JBI = JBI_DIR / "JBI_Graphical_Abstract.png"

W = 2400
H = 1600
BG = "#f6f2ea"
INK = "#243746"
MUTED = "#5f6b75"
NAVY = "#163b57"
TEAL = "#2b7a86"
GOLD = "#d4882b"
BRICK = "#c55a3d"
OLIVE = "#667d32"
WHITE = "#fffdf9"
PALE_BLUE = "#e8f0f7"
PALE_GREEN = "#ebf5ef"
PALE_GOLD = "#fff4e2"
PALE_ROSE = "#f8ece8"
LINE = "#d8cdbc"


def load_font(size: int, bold: bool = False):
    candidates = [
        r"C:\Windows\Fonts\cambria.ttc" if bold else r"C:\Windows\Fonts\cambria.ttc",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for candidate in candidates:
        p = Path(candidate)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def round_box(draw, xy, fill, outline, radius=28, width=3):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def add_text(draw, box, text, font, fill=INK, line_gap=8):
    x1, y1, x2, _ = box
    max_width = x2 - x1
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        test = f"{cur} {word}".strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= max_width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    y = y1
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        h = bbox[3] - bbox[1]
        draw.text((x1, y), line, font=font, fill=fill)
        y += h + line_gap
    return y


def bullet_block(draw, box, bullets, font, bullet_color, text_color=INK, gap=16):
    x1, y1, x2, _ = box
    y = y1
    for bullet in bullets:
        draw.ellipse((x1, y + 8, x1 + 16, y + 24), fill=bullet_color)
        y = add_text(draw, (x1 + 30, y, x2, y + 120), bullet, font, fill=text_color, line_gap=6) + gap
    return y


def paste_panel(canvas, path: Path, xy, size):
    if not path.exists():
        return
    img = Image.open(path).convert("RGB")
    fitted = ImageOps.fit(img, size, method=Image.Resampling.LANCZOS)
    canvas.paste(fitted, xy)


def main():
    sample = pd.read_csv(TABLE_DIR / "sample_matching_summary.csv")
    bench = pd.read_csv(TABLE_DIR / "model_benchmark.csv")
    perm = pd.read_csv(TABLE_DIR / "permutation_test_auc.csv")
    hubs = pd.read_csv(NET_DIR / "network_centrality_stability.csv")
    cart_qc = pd.read_csv(TABLE_DIR / "cart_direct_benchmark_qc.csv")

    n_core = int(sample.loc[sample.metric == "n_patients_intersection_all_main_layers", "value"].iloc[0])
    n_prot = int(sample.loc[sample.metric == "n_patients_protein", "value"].iloc[0])
    best_auc = bench.sort_values("auc", ascending=False).iloc[0]
    best_c = bench.sort_values("cox_c_index", ascending=False).iloc[0]
    top_hubs = ", ".join(hubs.head(4)["node"].tolist())
    perm_p = float(perm["p_value_right_tail"].iloc[0])
    mean_len = cart_qc["mean_read_length"].mean()
    gc = cart_qc["gc_fraction"].mean()

    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    title_font = load_font(60, True)
    sub_font = load_font(25)
    section_font = load_font(28, True)
    body_font = load_font(21)
    small_font = load_font(18)

    draw.text((90, 40), "Uncertainty-Aware Multi-Omics Network Analysis of Ovarian Cancer", font=title_font, fill=NAVY)
    add_text(
        draw,
        (90, 118, 2280, 170),
        "Public TCGA-OV integration identified stable cross-layer hubs and linked them to perturbation response, external ovarian immune-context validation, and a real CAR-product sequencing benchmark.",
        sub_font,
        fill=MUTED,
        line_gap=4,
    )

    top_y1, top_y2 = 210, 840
    left = (80, top_y1, 700, top_y2)
    mid = (760, top_y1, 1540, top_y2)
    right = (1600, top_y1, 2320, top_y2)
    bottom = (80, 900, 2320, 1510)

    round_box(draw, left, PALE_BLUE, NAVY)
    round_box(draw, mid, PALE_GREEN, TEAL)
    round_box(draw, right, PALE_GOLD, GOLD)
    round_box(draw, bottom, WHITE, LINE, radius=30, width=3)

    draw.text((left[0] + 28, left[1] + 24), "Study cohort and inputs", font=section_font, fill=NAVY)
    add_text(draw, (left[0] + 28, left[1] + 86, left[2] - 28, left[1] + 180), f"Matched TCGA-OV cohort: n={n_core}. Protein-matched subset: n={n_prot}.", body_font)
    add_text(draw, (left[0] + 28, left[1] + 170, left[2] - 28, left[1] + 300), "Input layers: mutation, copy-number alteration, methylation, RNA, and optional protein.", body_font)
    add_text(draw, (left[0] + 28, left[1] + 300, left[2] - 28, left[1] + 470), "Primary outputs: latent factors, pathway modules, survival ordering, network hubs, and perturbation effects.", body_font)

    chip_y = left[1] + 490
    chip_x = left[0] + 28
    for label, width, color in [
        ("Mutation", 150, BRICK),
        ("CNA", 110, GOLD),
        ("Methylation", 170, TEAL),
        ("RNA", 110, NAVY),
    ]:
        draw.rounded_rectangle((chip_x, chip_y, chip_x + width, chip_y + 54), radius=16, fill=color)
        tw = draw.textbbox((0, 0), label, font=small_font)[2]
        draw.text((chip_x + (width - tw) / 2, chip_y + 15), label, font=small_font, fill=WHITE)
        chip_x += width + 14
    draw.rounded_rectangle((left[0] + 28, chip_y + 78, left[0] + 170, chip_y + 132), radius=16, fill=OLIVE)
    draw.text((left[0] + 57, chip_y + 93), "Protein", font=small_font, fill=WHITE)

    draw.text((mid[0] + 28, mid[1] + 24), "Analytical strategy", font=section_font, fill=TEAL)
    bullet_block(
        draw,
        (mid[0] + 28, mid[1] + 92, mid[2] - 28, mid[2]),
        [
            "MOFA-like latent integration summarized shared cross-layer structure.",
            f"RNA modules achieved the highest AUC ({best_auc['auc']:.3f}, 95% CI {best_auc['auc_ci_low']:.3f}-{best_auc['auc_ci_high']:.3f}).",
            f"CNA showed the strongest survival ordering with Cox C-index {best_c['cox_c_index']:.3f}.",
            f"Perturbation and bootstrap resampling preserved the central role of {top_hubs} (permutation p={perm_p:.3f}).",
        ],
        body_font,
        bullet_color=TEAL,
    )

    draw.text((right[0] + 28, right[1] + 24), "Main findings", font=section_font, fill=GOLD)
    bullet_block(
        draw,
        (right[0] + 28, right[1] + 92, right[2] - 32, right[3] - 32),
        [
            "Stable biology was concentrated in latent hub states rather than isolated single features.",
            "Integrated modelling improved interpretability more clearly than it improved predictive accuracy.",
            "External ovarian immune-state comparisons supported the direction of the immune-regulatory signal.",
            "Direct CAR-product raw-read benchmarking established a real public sequencing validation branch.",
        ],
        body_font,
        bullet_color=GOLD,
    )

    draw.text((bottom[0] + 28, bottom[1] + 22), "Key outputs and external support", font=section_font, fill=INK)

    panels = [
        ((110, 980), (500, 440), FIG_DIR / "multilayer_network_graph.png", NAVY, "Integrated network", f"Top stable hubs: {top_hubs}"),
        ((650, 980), (500, 440), FIG_DIR / "perturbation_bootstrap_ci.png", BRICK, "Perturbation response", "Bootstrap effect sizes showed reproducible downstream rewiring after hub dampening."),
        ((1190, 980), (500, 440), FIG_DIR / "external_ovarian_immune_scores.png", TEAL, "External ovarian validation", "Immune-state scores shifted coherently across GEO-defined CD8 T-cell groups."),
        ((1730, 980), (520, 440), None, GOLD, "Direct CAR benchmark", f"Public CD22 CAR-T FASTQ ingestion succeeded. Mean read length {mean_len:.1f} bp; mean GC fraction {gc:.3f}. QC supports future validated alignment-based screening."),
    ]

    for (px, py), (pw, ph), fig_path, color, title, caption in panels:
        round_box(draw, (px, py, px + pw, py + ph), "#fcfbf8", LINE, radius=22, width=2)
        draw.text((px + 18, py + 14), title, font=body_font, fill=color)
        if fig_path is not None:
            paste_panel(canvas, fig_path, (px + 16, py + 52), (pw - 32, 230))
            add_text(draw, (px + 18, py + 302, px + pw - 18, py + ph - 18), caption, body_font, fill=INK, line_gap=6)
        else:
            round_box(draw, (px + 18, py + 60, px + pw - 18, py + 170), PALE_GOLD, GOLD, radius=18, width=2)
            draw.text((px + 34, py + 88), "ENA/SRA paired FASTQ", font=body_font, fill=GOLD)
            draw.text((px + 34, py + 126), "QC -> motif screen -> alignment readiness", font=small_font, fill=INK)
            add_text(draw, (px + 18, py + 210, px + pw - 18, py + ph - 18), caption, body_font, fill=INK, line_gap=6)

    OUT_MAIN.parent.mkdir(parents=True, exist_ok=True)
    OUT_JBI.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_MAIN, dpi=(300, 300))
    canvas.save(OUT_JBI, dpi=(300, 300))
    print(f"saved {OUT_MAIN}")
    print(f"saved {OUT_JBI}")


if __name__ == "__main__":
    main()
