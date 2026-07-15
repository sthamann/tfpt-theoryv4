"""Loaders (committed sibling-experiment catalogs; nothing fetched) +
sessionisation -- same conventions as frb-kernel-couplings/repeater-cascade.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .constants import (SESSION_GAP_D, TAU_GATE_S, VSIGN_MIN_ABS_PCT,
                        VSIGN_MIN_SIGMA)

EXPS = Path(__file__).resolve().parents[3]
POL_CSV = EXPS / "frb-tfpt-signatures" / "data" / "FAST_FRB20240114A_pol_catalog_v5.csv"
ZHANG_CSV = EXPS / "repeater-cascade" / "data" / "frb20220912a_zhang2023.csv"
LI_TSV = EXPS / "frb-tfpt-signatures" / "data" / "frb20121102_fast_li2021_1652.tsv"

DAY_S = 86400.0


@dataclass
class Bursts:
    source: str
    mjd: np.ndarray                    # sorted
    vsign: np.ndarray | None = None    # +/-1 significant handedness, nan else


def load_pol_v5() -> Bursts:
    rows = []
    with POL_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                mjd = float(r["MJD_topo"])
                doc = float(r["DOC"])
                err = float(r["DOC_err"])
            except (ValueError, KeyError):
                continue
            sig = (np.sign(doc)
                   if abs(doc) >= max(VSIGN_MIN_SIGMA * err, VSIGN_MIN_ABS_PCT)
                   else np.nan)
            rows.append((mjd, sig))
    rows.sort()
    return Bursts("FRB20240114A", np.array([a for a, _ in rows]),
                  vsign=np.array([b for _, b in rows]))


def load_zhang2023() -> Bursts:
    rows = []
    with ZHANG_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                rows.append(float(r["mjd_bary"]))
            except (ValueError, KeyError):
                continue
    return Bursts("FRB20220912A", np.array(sorted(rows)))


def load_li2021() -> Bursts:
    rows = []
    for r in csv.reader(LI_TSV.open(encoding="utf-8"), delimiter="\t"):
        if not r:
            continue
        try:
            rows.append(float(r[2]))
        except (ValueError, IndexError):
            continue
    return Bursts("FRB20121102A", np.array(sorted(rows)))


def sessions(b: Bursts) -> list[np.ndarray]:
    edges = np.where(np.diff(b.mjd) > SESSION_GAP_D)[0] + 1
    return [idx for idx in np.split(np.arange(len(b.mjd)), edges) if len(idx) >= 2]


def session_taus(b: Bursts, idx: np.ndarray) -> np.ndarray:
    """tau (s) from session onset; the onset burst itself gets tau = 0."""
    tau = (b.mjd[idx] - b.mjd[idx[0]]) * DAY_S
    tau[0] = 0.0
    return tau


def odd_channel_sessions(b: Bursts) -> list[tuple[np.ndarray, np.ndarray]]:
    """(ln tau, sign) pairs per session: significant handedness AND tau >= gate."""
    out = []
    for idx in sessions(b):
        tau = session_taus(b, idx)
        s = b.vsign[idx]
        ok = ~np.isnan(s) & (tau >= TAU_GATE_S)
        if int(ok.sum()) >= 2:
            out.append((np.log(tau[ok]), s[ok].astype(float)))
    return out


def even_channel_sessions(b: Bursts) -> list[np.ndarray]:
    """ln tau per session (all bursts past the tau gate)."""
    out = []
    for idx in sessions(b):
        tau = session_taus(b, idx)
        ok = tau >= TAU_GATE_S
        if int(ok.sum()) >= 2:
            out.append(np.log(tau[ok]))
    return out
