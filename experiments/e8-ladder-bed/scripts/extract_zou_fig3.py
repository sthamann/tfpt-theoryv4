#!/usr/bin/env python3
"""Digitize the BaCo2V2O8 INS peak positions from Zou et al., PRL 127, 077201 (2021).

Source: arXiv:2005.13302v3 e-print, Fig. 3 (fig3.pdf). The figure embeds three
raster panels (a: INS experiment at H = 4.7 T, b: analytic E8 DSF with m1 = 1.2 meV,
c: iTEBD) that share one x-axis (identical tick pixel positions, ticks every 0.2 meV,
labels 1..5 meV under panel (c)).

What is extracted:
  1. The eight red vertical markers in panel (a). These mark the eight
     single-E8-particle peaks in the MEASURED spectrum (per-panel positions:
     in panel (b) the same markers sit on the analytic positions 1.2*r_i meV,
     which validates both the calibration and the marker semantics).
  2. The local maxima of the black Gaussian-fit curve in panel (a) -> the
     multi-particle / zone-folding peaks (P-peaks and F-peaks of the paper).

Determinism: pure function of the committed arXiv source; no seeds.
Output: data/baco2v2o8_ins_peaks.csv (+ results/extraction_qa.png overlay).

Usage:  python scripts/extract_zou_fig3.py [--eprint /path/to/2005.13302v3.tar.gz]
        (downloads the e-print from arXiv if no path is given and none is cached)
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import tarfile
import urllib.request
import zlib
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter1d, median_filter
from scipy.signal import find_peaks

ROOT = Path(__file__).resolve().parents[1]
EPRINT_URL = "https://arxiv.org/e-print/2005.13302"
CACHE = ROOT / "data" / "arxiv_2005.13302v3_eprint.tar.gz"

# --- axis calibration (see module docstring; ticks every 0.2 meV) -----------
TICK_PX_1MEV = 152.5   # pixel column of the "1 meV" major tick (panels a/c identical)
PX_PER_MEV = 195.0     # major-tick spacing (152.5, 347.5, 542.5, 737.5, 932.5)

SIGMA_SINGLE = 0.10    # meV; instrument energy resolution (paper, Fig. 4 caption)
SIGMA_MULTI = 0.12     # meV; broader multi-particle/folding features (curve maxima)

ZAM = np.array([
    1.0, 1.6180339887498948, 1.9890437907365467, 2.4048671723720653,
    2.9562952014676113, 3.2183404585236658, 3.8911568233268538, 4.7833861167528131,
])


def px_to_mev(px):
    return (np.asarray(px, dtype=float) - TICK_PX_1MEV) / PX_PER_MEV + 1.0


def load_fig3(eprint: Path) -> dict[str, np.ndarray]:
    """Return the three RGB raster panels of fig3.pdf keyed 'a', 'b', 'c'."""
    with tarfile.open(eprint, "r:gz") as tf:
        raw = tf.extractfile("fig3.pdf").read()
    streams = re.findall(rb"stream\r?\n(.*?)endstream", raw, re.S)
    decoded = []
    for s in streams:
        try:
            decoded.append(zlib.decompress(s))
        except zlib.error:
            decoded.append(None)
    shapes = {"a": (410, 1112), "c": (447, 1112), "b": (409, 1112)}
    panels: dict[str, np.ndarray] = {}
    for key, (h, w) in shapes.items():
        for d in decoded:
            if d is not None and len(d) == h * w * 3:
                panels[key] = np.frombuffer(d, dtype=np.uint8).reshape(h, w, 3)
                break
        else:
            raise RuntimeError(f"panel {key} raster ({h}x{w}) not found in fig3.pdf")
    return panels


def red_vertical_lines(img: np.ndarray, row_lo=5, row_hi=395) -> np.ndarray:
    """Pixel centroids of the vertical red markers (>=30% column coverage)."""
    r, g, b = (img[..., k].astype(int) for k in range(3))
    red = (r - g > 40) & (r - b > 40) & (r > 120)
    frac = red[row_lo:row_hi].mean(axis=0)
    cols = np.where(frac > 0.3)[0]
    centroids, start, prev = [], None, -10
    for x in cols:
        if x - prev > 3:
            if start is not None:
                centroids.append((start + prev) / 2)
            start = x
        prev = x
    if start is not None:
        centroids.append((start + prev) / 2)
    return np.array(centroids)


# Rectangles (row_lo, row_hi, col_lo, col_hi) masked out of the dark-pixel field:
# the in-axes legend box (top right) and the "Q=(0,0,2)" axis text (top left).
MASK_RECTS = [(0, 224, 788, 1108), (10, 75, 150, 345)]


def curve_maxima(img: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Local maxima of the black Gaussian-fit curve in panel (a).

    The curve is traced by connectivity: per column, the centers of all dark
    runs are candidate curve positions; a dynamic program picks the row path
    with minimal total vertical jump. Isolated text glyphs, marker edges and
    error-bar whiskers are rejected because they are not vertically continuous
    with the curve across columns.
    """
    h, w, _ = img.shape
    r, g, b = (img[..., k].astype(int) for k in range(3))
    dark = (r < 80) & (g < 80) & (b < 80)
    blue = (b - r > 40) & (b > 100)
    dark &= ~blue
    for r0, r1, c0, c1 in MASK_RECTS:
        dark[r0:r1, c0:c1] = False

    col_range = range(116, 1096)
    cands: list[np.ndarray] = []
    for x in col_range:
        rows = np.where(dark[8:396, x])[0] + 8
        if len(rows) == 0:
            cands.append(np.array([]))
            continue
        # run centers
        splits = np.where(np.diff(rows) > 1)[0]
        runs = np.split(rows, splits + 1)
        cands.append(np.array([rr.mean() for rr in runs]))

    # DP over candidate runs, cost = |row jump| (curve is continuous)
    INF = 1e18
    prev_cost, prev_rows = None, None
    back: list[np.ndarray] = []
    for c in cands:
        if len(c) == 0:
            back.append(np.array([], dtype=int))
            continue
        if prev_cost is None:
            cost = np.zeros(len(c))
            back.append(np.full(len(c), -1, dtype=int))
        else:
            jump = np.abs(c[:, None] - prev_rows[None, :])
            jump[jump > 40] = INF  # forbid teleporting to detached objects
            tot = prev_cost[None, :] + jump
            back.append(np.argmin(tot, axis=1))
            cost = np.min(tot, axis=1)
        prev_cost, prev_rows = cost, c
    # backtrack
    idx = int(np.argmin(prev_cost))
    path_rows = np.full(len(cands), np.nan)
    for i in range(len(cands) - 1, -1, -1):
        if len(cands[i]) == 0:
            continue
        path_rows[i] = cands[i][idx]
        idx = back[i][idx]
        if idx < 0 and i > 0:  # start column reached
            idx = 0
    xs_all = np.array(list(col_range))
    valid = ~np.isnan(path_rows)
    xs = xs_all[valid]
    height = -path_rows[valid]  # larger = higher intensity
    height = gaussian_filter1d(median_filter(height, size=7), 3)
    peaks, props = find_peaks(height, prominence=6, distance=12)
    return xs[peaks], props["prominences"], (xs, height)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eprint", type=Path, default=None)
    args = ap.parse_args()

    eprint = args.eprint or CACHE
    if not eprint.exists():
        print(f"downloading {EPRINT_URL} -> {eprint}")
        eprint.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(EPRINT_URL, eprint)

    panels = load_fig3(eprint)

    # -- calibration validation on panel (b): markers must sit on 1.2*r_i ----
    e_b = px_to_mev(red_vertical_lines(panels["b"]))
    theory_b = 1.2 * ZAM
    rel = np.abs(e_b - theory_b) / theory_b
    assert len(e_b) == 8, f"panel b: expected 8 markers, got {len(e_b)}"
    assert rel.max() < 0.01, f"calibration check failed: max rel dev {rel.max():.4f}"
    print("panel (b) calibration check: markers vs 1.2*r_i, max rel dev "
          f"{rel.max()*100:.2f}% -> OK")

    # -- panel (a): measured single-particle peaks ---------------------------
    e_single = px_to_mev(red_vertical_lines(panels["a"]))
    assert len(e_single) == 8, f"panel a: expected 8 markers, got {len(e_single)}"
    print("panel (a) single-E8 peaks (meV):", np.round(e_single, 3))

    # -- panel (a): all fit-curve maxima (multi-particle + folding peaks) ----
    px_max, prom, (xs, height) = curve_maxima(panels["a"])
    e_max = px_to_mev(px_max)
    # drop maxima that duplicate a red single-particle marker (within 0.06 meV)
    is_single = np.array([np.min(np.abs(e_single - e)) < 0.06 for e in e_max])
    e_multi = e_max[~is_single]
    print("panel (a) additional curve maxima (meV):", np.round(e_multi, 3))

    # -- write CSV ------------------------------------------------------------
    out = ROOT / "data" / "baco2v2o8_ins_peaks.csv"
    lines = [
        "# BaCo2V2O8 INS peak positions at the 1D QCP (H = 4.7 T || [010], T = 0.4 K, Q = (002))",
        "# Source: Zou, Cui, Wang et al., PRL 127, 077201 (2021); arXiv:2005.13302v3, Fig. 3(a).",
        "# Extraction: scripts/extract_zou_fig3.py (deterministic digitization of the arXiv",
        "#   vector figure). Red vertical markers = the paper's single-E8-particle peaks;",
        "#   additional rows = maxima of the paper's Gaussian fit curve (multi-particle /",
        "#   zone-folding peaks P/F of the paper). Axis: ticks every 0.2 meV, 195 px/meV;",
        "#   calibration validated on Fig. 3(b) (analytic panel, m1 = 1.2 meV) to < 1%.",
        "# sigma: 0.10 meV singles / 0.12 meV broader features (instrument resolution",
        "#   0.1 meV per the paper; digitization adds ~0.01 meV).",
        "# 'kind' is REPORTING metadata only -- the blind detector never sees it.",
        "energy_mev,sigma_mev,kind,source",
    ]
    rows = [(e, SIGMA_SINGLE, "single_marker", "fig3a_red_marker") for e in e_single]
    rows += [(e, SIGMA_MULTI, "other_peak", "fig3a_curve_max") for e in e_multi]
    rows.sort()
    for e, s, kind, src in rows:
        lines.append(f"{e:.4f},{s:.2f},{kind},{src}")
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out} ({len(rows)} peaks)")

    # -- QA overlay ------------------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.plot(px_to_mev(xs), height - height.min(), "k-", lw=1, label="traced fit curve")
    for e in e_single:
        ax.axvline(e, color="r", lw=1, label="single-E8 marker" if e == e_single[0] else None)
    for e in e_multi:
        ax.axvline(e, color="b", lw=0.7, ls="--",
                   label="curve maximum" if e == e_multi[0] else None)
    ax.set_xlabel("Energy (meV)")
    ax.set_ylabel("traced curve height (px)")
    ax.set_title("extraction QA: Zou+ PRL 127, 077201 Fig. 3(a)")
    ax.legend(loc="upper right", fontsize=8)
    qa = ROOT / "results" / "extraction_qa.png"
    qa.parent.mkdir(exist_ok=True)
    fig.savefig(qa, dpi=120, bbox_inches="tight")
    print(f"wrote {qa}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
