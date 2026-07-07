"""Loaders for the three committed FRB catalogs + sessionisation.

All data files live in SIBLING experiments (committed there); nothing is fetched:
  * Li+2021  FRB 20121102A -- frb-tfpt-signatures/data/frb20121102_fast_li2021_1652.tsv
  * Zhang+2023 FRB 20220912A -- repeater-cascade/data/frb20220912a_zhang2023.csv
  * FAST pol v5 FRB 20240114A -- frb-tfpt-signatures/data/FAST_FRB20240114A_pol_catalog_v5.csv
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np

EXPS = Path(__file__).resolve().parents[3]
LI_TSV = EXPS / "frb-tfpt-signatures" / "data" / "frb20121102_fast_li2021_1652.tsv"
ZHANG_CSV = EXPS / "repeater-cascade" / "data" / "frb20220912a_zhang2023.csv"
POL_CSV = EXPS / "frb-tfpt-signatures" / "data" / "FAST_FRB20240114A_pol_catalog_v5.csv"

SESSION_GAP_D = 0.2
DAY_S = 86400.0
TAU_GATE_S = 0.5


@dataclass
class Bursts:
    source: str
    mjd: np.ndarray                  # sorted
    energy: np.ndarray | None        # same order (None for pol-only catalog)
    vsign: np.ndarray | None = None  # +/-1 where handedness significant, nan else
    pa_deg: np.ndarray | None = None  # mean linear-pol angle (deg, mod 180)
    li_pct: np.ndarray | None = None  # linear polarization fraction L/I (%)


def load_li2021() -> Bursts:
    rows = []
    for r in csv.reader(LI_TSV.open(encoding="utf-8"), delimiter="\t"):
        if not r or r[0].lstrip().startswith(("#", "recno", "-", "d", " ")) and not \
           r[0].strip().isdigit():
            continue
        try:
            rows.append((float(r[2]), float(r[12])))
        except (ValueError, IndexError):
            continue
    rows.sort()
    mjd = np.array([a for a, _ in rows])
    e = np.array([b for _, b in rows])
    keep = e > 0
    return Bursts("FRB20121102A", mjd[keep], e[keep])


def load_zhang2023() -> Bursts:
    rows = []
    with ZHANG_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                rows.append((float(r["mjd_bary"]), float(r["energy_1e36erg"])))
            except (ValueError, KeyError):
                continue
    rows.sort()
    mjd = np.array([a for a, _ in rows])
    e = np.array([b for _, b in rows])
    keep = e > 0
    return Bursts("FRB20220912A", mjd[keep], e[keep])


def load_pol_v5(*, min_abs_pct: float = 5.0, min_sigma: float = 2.0) -> Bursts:
    """FRB 20240114A with SIGNED circular polarization; vsign = +/-1 where the
    handedness is significant (|DOC| >= max(min_sigma * DOC_err, min_abs_pct)), nan else."""
    rows = []
    with POL_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                mjd = float(r["MJD_topo"])
                doc = float(r["DOC"])
                err = float(r["DOC_err"])
            except (ValueError, KeyError):
                continue
            sig = np.sign(doc) if abs(doc) >= max(min_sigma * err, min_abs_pct) else np.nan
            try:
                pa = float(r["PA_mean(deg)"])
            except (ValueError, KeyError):
                pa = np.nan
            try:
                li = float(r["DOL"])
            except (ValueError, KeyError):
                li = np.nan
            rows.append((mjd, sig, pa, li))
    rows.sort()
    return Bursts("FRB20240114A", np.array([a for a, *_ in rows]), None,
                  vsign=np.array([b for _, b, *_ in rows]),
                  pa_deg=np.array([c for *_, c, _ in rows]),
                  li_pct=np.array([d for *_, d in rows]))


def sessions(b: Bursts) -> list[np.ndarray]:
    """Index arrays of the per-session bursts (gap > SESSION_GAP_D opens a session)."""
    edges = np.where(np.diff(b.mjd) > SESSION_GAP_D)[0] + 1
    return [idx for idx in np.split(np.arange(len(b.mjd)), edges) if len(idx) >= 2]


def session_taus(b: Bursts, idx: np.ndarray) -> np.ndarray:
    """tau (s) from the session onset (first burst), gated at TAU_GATE_S."""
    tau = (b.mjd[idx] - b.mjd[idx[0]]) * DAY_S
    tau[0] = 0.0
    return tau
