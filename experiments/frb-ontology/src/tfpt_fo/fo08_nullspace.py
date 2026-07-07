"""FO.08 -- polarimetric NULL-SPACE search: forbidden regions instead of peaks.

S15 hole search: if B projects character classes away, TFPT could appear as a
forbidden region of the polarization state space rather than a pile-up
(FRB.06/FO.04 searched peaks/classes; nobody searched holes). No forbidden set
is derived -> exploratory, with the look-elsewhere inside the statistic.

Statistic: largest empty disk in u = (DOL, DOC)/100 over grid centres inside
the physical domain and the populated envelope. Null: permute DOC against DOL
(preserves BOTH marginals exactly, destroys only the joint structure) -- a hole
counts only if it is a property of the JOINT distribution.
"""

from __future__ import annotations

import numpy as np
from scipy.spatial import cKDTree

from .data import PolCatalog

MIN_SNR = 20.0
GRID_L, GRID_C = 40, 80
ENVELOPE_R, ENVELOPE_MIN = 0.35, 5
N_PERM = 1000


def _points(cat: PolCatalog) -> np.ndarray:
    import csv
    from .data import POL_CSV, _f
    snr = {}
    with POL_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            m = _f(r, "MJD_topo")
            if np.isfinite(m):
                snr[round(m, 9)] = _f(r, "S/N")
    keep = np.array([snr.get(round(m, 9), np.nan) >= MIN_SNR for m in cat.mjd])
    ok = keep & np.isfinite(cat.dol) & np.isfinite(cat.doc)
    return np.column_stack([cat.dol[ok] / 100.0, cat.doc[ok] / 100.0])


def _grid(points: np.ndarray) -> np.ndarray:
    ls = np.linspace(0.0, 1.05, GRID_L)
    cs = np.linspace(-1.05, 1.05, GRID_C)
    G = np.array([(l, c) for l in ls for c in cs])
    G = G[G[:, 0] ** 2 + G[:, 1] ** 2 <= 1.05 ** 2]
    # populated-envelope gate: centre needs >= ENVELOPE_MIN points within 0.35
    tree = cKDTree(points)
    counts = np.array([len(tree.query_ball_point(g, ENVELOPE_R)) for g in G])
    return G[counts >= ENVELOPE_MIN]


def _max_empty_disk(points: np.ndarray, G: np.ndarray) -> tuple[float, np.ndarray]:
    tree = cKDTree(points)
    d, _ = tree.query(G)
    k = int(np.argmax(d))
    return float(d[k]), G[k]


def run(cat: PolCatalog, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    pts = _points(cat)
    G = _grid(pts)
    r_obs, centre = _max_empty_disk(pts, G)

    null = np.empty(N_PERM)
    for i in range(N_PERM):
        perm = pts.copy()
        perm[:, 1] = rng.permutation(perm[:, 1])
        null[i], _ = _max_empty_disk(perm, G)
    p = float((1 + np.sum(null >= r_obs)) / (N_PERM + 1))

    verdict = "hint_flag" if p < 0.05 else "null"
    return {"axis": "FO.08_polarimetric_null_space",
            "n_bursts_snr20": int(len(pts)),
            "n_grid_centres": int(len(G)),
            "largest_empty_disk_r": round(r_obs, 4),
            "at_DOL_DOC_pct": [round(100 * float(c), 1) for c in centre],
            "null_median_r": round(float(np.median(null)), 4),
            "p_joint_perm": p,
            "caveats": ["holes below the 2-4% measurement error are unresolvable",
                        "marginal-driven voids do not count (null preserves marginals)"],
            "verdict": verdict,
            "note": ("no joint forbidden region beyond the marginals in the only "
                     "full-Stokes catalog in hand" if verdict == "null"
                     else "escalate-only")}
