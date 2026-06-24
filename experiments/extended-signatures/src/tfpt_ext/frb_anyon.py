"""FRB.11 -- anyon MTC pi/4 comb on linear polarisation (QT.05 reinterpretation).

The carrier Z4 x Z4 MTC predicts statistical phase quanta pi/4 (spin) and pi/2 (braiding).
FRB.08 found fundamental m=2 in PA classes -- QT.05 reads that as the predicted fermion
sector, not a null. This test searches for pi/4-quantised EVPA structure:

    chi in {theta0 + k * 45 deg}  <=>  |<exp(8 i chi)>| concentrated

Preregistered: kernel spacing 45 deg (pi/4 in the 180-deg EVPA period).
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .frb_minimal import all_series, load_fast_20240114A_pol, blinkverse_series
PI4_SPACING_DEG = 45.0
M_PI4 = 4  # 180/4 = 45 deg = pi/4 quanta on EVPA period


@dataclass
class AnyonCombResult:
    source: str
    n: int
    rayleigh_z_m8: float
    p_value: float
    theta0_deg: float
    m2_also_sig: bool
    verdict: str


@dataclass
class FrbAnyonResult:
    results: list[AnyonCombResult] = field(default_factory=list)
    injection_validated: bool = False
    verdict: str = ""
    data_limited: bool = False


def _order_param(pa_deg: np.ndarray, m: int) -> tuple[float, float]:
    pa = np.asarray(pa_deg, float)
    pa = pa[np.isfinite(pa)] % 180.0
    n = len(pa)
    if n < 8:
        return 0.0, 1.0
    th = np.deg2rad(2.0 * m * pa)
    c, s = np.cos(th).mean(), np.sin(th).mean()
    z = n * (c * c + s * s)
    return float(z), float(np.rad2deg(np.arctan2(s, c)) / (2.0 * m) % (180.0 / m))


def _surrogate_p(z: float, n: int, m: int, n_null: int = 2000, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    null = np.empty(n_null)
    for i in range(n_null):
        th = np.deg2rad(2.0 * m * (rng.uniform(0, 180, n) % 180.0))
        null[i] = n * (np.cos(th).mean() ** 2 + np.sin(th).mean() ** 2)
    return float((1 + np.sum(null >= z)) / (n_null + 1))


def validate_injection(seed: int = 0) -> bool:
    rng = np.random.default_rng(seed)
    n = 200
    theta0 = 12.0
    pa = (theta0 + PI4_SPACING_DEG * rng.integers(0, 4, n) + rng.normal(0, 3, n)) % 180.0
    z8, _ = _order_param(pa, M_PI4)
    p8 = _surrogate_p(z8, n, M_PI4, seed=seed)
    pa_u = rng.uniform(0, 180, n)
    z_u, _ = _order_param(pa_u, M_PI4)
    p_u = _surrogate_p(z_u, n, M_PI4, seed=seed + 1)
    return bool(p8 < 0.05 and p_u > 0.05)


def run_frb_anyon(seed: int = 0) -> FrbAnyonResult:
    res = FrbAnyonResult()
    res.injection_validated = validate_injection(seed)

    series_list: list = []
    pol = load_fast_20240114A_pol()
    if pol.available and pol.pa_deg.size:
        series_list.append(pol)
    for s in blinkverse_series():
        if s.pa_deg.size and np.sum(np.isfinite(s.pa_deg)) >= 10:
            series_list.append(s)

    if not series_list:
        res.data_limited = True
        res.verdict = (
            f"data_limited: no PA arrays on disk; pi/4 detector injection_validated="
            f"{res.injection_validated}"
        )
        return res

    for s in series_list:
        if not getattr(s, "available", True):
            continue
        pa = getattr(s, "pa_deg", np.array([]))
        if pa.size == 0 or np.sum(np.isfinite(pa)) < 10:
            continue
        pa = pa[np.isfinite(pa)]
        z8, t0 = _order_param(pa, M_PI4)
        p8 = _surrogate_p(z8, len(pa), M_PI4, seed=seed)
        z2, _ = _order_param(pa, 2)
        p2 = _surrogate_p(z2, len(pa), 2, seed=seed + 1)
        res.results.append(AnyonCombResult(
            source=s.source, n=len(pa),
            rayleigh_z_m8=round(z8, 2), p_value=round(p8, 4),
            theta0_deg=round(t0, 1),
            m2_also_sig=p2 < 0.05,
            verdict="pi/4 comb candidate" if p8 < 0.05 else "null",
        ))

    if not res.results:
        res.data_limited = True
        res.verdict = (
            f"data_limited: no PA arrays on disk; pi/4 detector injection_validated="
            f"{res.injection_validated}"
        )
        return res

    sig8 = [r for r in res.results if r.p_value < 0.05]
    m2_dom = sum(1 for r in res.results if r.m2_also_sig and r.p_value >= 0.05)
    if sig8:
        res.verdict = (
            f"pi/4 (m=4) comb significant in {len(sig8)} source(s) -- "
            f"QT.05 reinterpretation candidate (not replicated unless >=2 sources)"
        )
    elif m2_dom:
        res.verdict = (
            f"consistent with QT.05 fermion-sector (m=2) dominance in {m2_dom} source(s); "
            f"no pi/4 comb excess -- matches FRB.08 reading"
        )
    else:
        res.verdict = "clean NULL on pi/4 comb across available PA data"
    return res
