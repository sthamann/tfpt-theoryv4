"""Dynamic probes: walled-clock matched filter on Crab nu(t); FRB repeater inter-burst gaps."""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .constants import CLOCK_BEND, OMEGA_COMB

PULSAR_SRC = Path(__file__).resolve().parents[3] / "pulsar-glitch-recovery" / "src"
from .frb_minimal import load_fast_121102
CRAB_EPHEM = Path(__file__).resolve().parents[3] / "pulsar-glitch-recovery" / "data" / "crab2.txt"


@dataclass
class MatchedFilterResult:
    segment: str
    bend_ratio: float | None
    r2_gain: float
    wall_modes: int
    comb_p: float | None
    note: str


@dataclass
class DynamicResult:
    crab: list[MatchedFilterResult] = field(default_factory=list)
    frb_gaps: dict = field(default_factory=dict)
    verdict: str = ""


def _two_exp_template(tau: np.ndarray, ratio: float = CLOCK_BEND) -> np.ndarray:
    t = tau / tau.max()
    t1, t2 = 0.3, 1.0
    return 0.2 + 0.5 * np.exp(-t / t1) + 0.3 * np.exp(-t * ratio / t2)


def _fit_bend(y: np.ndarray, tau: np.ndarray) -> tuple[float, float, int]:
    """Fit 1-exp+floor vs 2-exp+floor; return best bend ratio, R2 gain, n modes used."""
    t = tau - tau.min() + 1.0
    lt = np.log(t)
    y = y - y.min()
    if y.max() > 0:
        y = y / y.max()
    # 1-mode
    X1 = np.column_stack([np.ones_like(lt), np.exp(-lt)])
    b1, _, _, _ = np.linalg.lstsq(X1, y, rcond=None)
    ss1 = np.sum((y - X1 @ b1) ** 2)
    # 2-mode fixed ratio
    r = CLOCK_BEND
    X2 = np.column_stack([np.ones_like(lt), np.exp(-lt), np.exp(-r * lt)])
    b2, _, _, _ = np.linalg.lstsq(X2, y, rcond=None)
    ss2 = np.sum((y - X2 @ b2) ** 2)
    gain = (ss1 - ss2) / (ss1 + 1e-12)
    return r, float(gain), 2


def _run_crab() -> list[MatchedFilterResult]:
    out: list[MatchedFilterResult] = []
    if str(PULSAR_SRC) not in sys.path:
        sys.path.insert(0, str(PULSAR_SRC))
    try:
        from tfpt_pulsar.catalog import load_crab_ephemeris
        from tfpt_pulsar.nu_recovery import detect_glitch_mjds, recovery_segments, segment_curves
    except ImportError:
        return out

    crab_csv = Path(__file__).resolve().parents[3] / "pulsar-glitch-recovery" / "data" / "crab_ephemeris.csv"
    if not crab_csv.exists():
        return out

    try:
        pts = load_crab_ephemeris()
        glitches = detect_glitch_mjds(pts)
        segs = recovery_segments(pts, glitches)
        curves = {g: (tau, rec) for g, tau, rec in segment_curves(pts, glitches)}
    except Exception:
        return out

    for seg in segs:
        tau, rec = curves.get(seg.glitch_mjd, (None, None))
        if tau is None or len(tau) < 14:
            continue
        bend, gain, nm = _fit_bend(np.asarray(rec), np.asarray(tau))
        out.append(MatchedFilterResult(
            f"glitch@{seg.glitch_mjd:.0f}", bend, round(gain, 5), nm,
            seg.p_value, f"n={seg.n_points} pts, comb={'Y' if seg.detected else 'N'}",
        ))
    return out


def _run_frb_gaps(seed: int = 0) -> dict:
    s = load_fast_121102()
    if not s.available or len(s) < 30:
        return {"available": False, "note": "FAST 1652 not on disk"}

    order = np.argsort(s.mjd)
    t = s.mjd[order]
    dt = np.diff(t)
    dt = dt[dt > 0]
    if len(dt) < 20:
        return {"available": True, "n_gaps": len(dt), "note": "too few gaps"}

    log_dt = np.log(dt)
    # gap ratio test at CLOCK_BEND
    ratios = log_dt[1:] / log_dt[:-1]
    near = np.sum(np.abs(ratios - CLOCK_BEND) / CLOCK_BEND < 0.1)
    rng = np.random.default_rng(seed)
    null = []
    for _ in range(2000):
        sh = rng.permutation(log_dt)
        r = sh[1:] / sh[:-1]
        null.append(np.sum(np.abs(r - CLOCK_BEND) / CLOCK_BEND < 0.1))
    p = float((1 + sum(n >= near for n in null)) / (len(null) + 1))
    return {
        "available": True,
        "source": s.source,
        "n_gaps": len(dt),
        "clock_ratio": CLOCK_BEND,
        "near_count": int(near),
        "p_value": round(p, 4),
        "verdict": "null" if p > 0.05 else "hint",
    }


def run_dynamic(seed: int = 0) -> DynamicResult:
    res = DynamicResult()
    res.crab = _run_crab()
    res.frb_gaps = _run_frb_gaps(seed)

    crab_note = "no Crab segments" if not res.crab else (
        f"{len(res.crab)} segments; max 2-mode R2 gain "
        f"{max(x.r2_gain for x in res.crab):.4f} (expect ~1e-3 if degenerate)"
    )
    frb_note = res.frb_gaps.get("verdict", "data_limited")
    res.verdict = (
        f"dynamic probes: Crab matched-filter -- {crab_note}; "
        f"FRB repeater gap clock -- {frb_note} "
        f"(p={res.frb_gaps.get('p_value', 'n/a')}). "
        f"Open lever: Vela daily nu(t) (>3 comb periods)."
    )
    return res
