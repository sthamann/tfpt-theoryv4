"""PC.01-PC.03 -- the parity-resolved comb tests (v486 selection rule).

Odd channel (signed circular polarization): the signed Rayleigh power
    Z_s(w) = |sum_i s_i exp(i w ln tau_i)|^2 / n
with the WITHIN-SESSION SIGN-PERMUTATION null: every burst time (and hence the
entire rate envelope) is kept, only the sign-time coherence is destroyed --
the smooth envelope is parity-even and cancels from the signed statistic, so
this null is envelope-immune by construction.

Even channel: the unsigned Rayleigh with the rate-preserving log-density
surrogate of repeater-cascade (functions vendored verbatim from
repeater_cascade/comb.py -- surrogate_lntau, rayleigh_z).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.stats import chi2

from .constants import (MIN_BURSTS_USED, N_OFFTONE, N_SIGN_PERM, N_SURROGATE,
                        OFFTONE_HI, OFFTONE_LO, REACH_GATE_PERIODS,
                        RELAXED_GATE_PERIODS, RELAXED_MIN_BURSTS)

# ---- vendored verbatim from repeater_cascade/comb.py (frozen constructions) --
SURROGATE_POLY_DEG = 3
SURROGATE_BINS = 32


def rayleigh_z(u: np.ndarray, w: np.ndarray | float) -> np.ndarray:
    """Rayleigh power z(w) = |sum exp(i w u)|^2 / n for one or many frequencies."""
    w_arr = np.atleast_1d(np.asarray(w, dtype=float))
    ph = np.exp(1j * np.outer(w_arr, u))
    z = np.abs(ph.sum(axis=1)) ** 2 / len(u)
    return z if np.ndim(w) else float(z[0])


def surrogate_lntau(u: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    lo, hi = float(u.min()), float(u.max())
    edges = np.linspace(lo, hi, SURROGATE_BINS + 1)
    counts, _ = np.histogram(u, bins=edges)
    centers = 0.5 * (edges[:-1] + edges[1:])
    logc = np.log(counts + 0.5)
    coef = np.polyfit(centers, logc, SURROGATE_POLY_DEG, w=np.sqrt(counts + 0.5))
    weights = np.exp(np.polyval(coef, centers))
    weights = weights / weights.sum()
    picks = rng.choice(SURROGATE_BINS, size=len(u), p=weights)
    return edges[picks] + rng.uniform(0.0, 1.0, len(u)) * (edges[picks + 1] - edges[picks])
# ------------------------------------------------------------------------------


def signed_rayleigh(u: np.ndarray, s: np.ndarray, w: float) -> float:
    return float(np.abs(np.sum(s * np.exp(1j * w * u))) ** 2 / len(u))


def reach_periods(u: np.ndarray, omega: float) -> float:
    """ln-tau reach in periods of the tested tone (period = 2 pi / omega)."""
    return float((u.max() - u.min()) * omega / (2.0 * math.pi))


@dataclass
class OddSessionResult:
    n_used: int
    reach_periods: float
    gate: str                      # "primary" | "relaxed" | "fail"
    z_signed: float = float("nan")
    p_sign_perm: float = float("nan")
    p_offtone_rank: float = float("nan")


def odd_session_test(u: np.ndarray, s: np.ndarray, omega: float, *,
                     seed: int = 0, relaxed_ok: bool = False) -> OddSessionResult:
    n = len(u)
    rp = reach_periods(u, omega)
    if rp > REACH_GATE_PERIODS and n >= MIN_BURSTS_USED:
        gate = "primary"
    elif relaxed_ok and rp > RELAXED_GATE_PERIODS and n >= RELAXED_MIN_BURSTS:
        gate = "relaxed"
    else:
        return OddSessionResult(n, round(rp, 3), "fail")
    rng = np.random.default_rng(seed + n)
    z_obs = signed_rayleigh(u, s, omega)
    null = np.empty(N_SIGN_PERM)
    for k in range(N_SIGN_PERM):
        null[k] = signed_rayleigh(u, rng.permutation(s), omega)
    p = float((1 + np.sum(null >= z_obs)) / (N_SIGN_PERM + 1))
    # off-tone rank of the sign-permutation-standardised score
    tones = np.linspace(OFFTONE_LO, OFFTONE_HI, N_OFFTONE)
    tones = tones[np.abs(tones - omega) > 0.1 * omega]
    zeta = np.empty(len(tones) + 1)
    for j, w in enumerate(np.concatenate([[omega], tones])):
        zo = signed_rayleigh(u, s, w)
        zn = np.array([signed_rayleigh(u, rng.permutation(s), w)
                       for _ in range(60)])
        zeta[j] = (zo - zn.mean()) / (zn.std() + 1e-12)
    p_rank = float((1 + np.sum(zeta[1:] >= zeta[0])) / len(zeta))
    return OddSessionResult(n, round(rp, 3), gate, round(z_obs, 4),
                            round(p, 4), round(p_rank, 4))


def even_session_test(u: np.ndarray, omega: float, *, seed: int = 0) -> dict:
    n = len(u)
    rp = reach_periods(u, omega)
    if not (rp > REACH_GATE_PERIODS and n >= MIN_BURSTS_USED):
        return {"n_used": n, "reach_periods": round(rp, 3), "gate": "fail"}
    rng = np.random.default_rng(seed + n)
    z_obs = float(rayleigh_z(u, omega))
    z_sur = np.array([float(rayleigh_z(surrogate_lntau(u, rng), omega))
                      for _ in range(N_SURROGATE)])
    p = float((1 + np.sum(z_sur >= z_obs)) / (N_SURROGATE + 1))
    return {"n_used": n, "reach_periods": round(rp, 3), "gate": "primary",
            "z": round(z_obs, 4), "p_surrogate": round(p, 4)}


def fisher(pvals: list[float], floor: float) -> float:
    p = np.clip(np.asarray(pvals, dtype=float), floor, 1.0)
    if len(p) == 0:
        return float("nan")
    stat = -2.0 * np.sum(np.log(p))
    return float(chi2.sf(stat, df=2 * len(p)))


@dataclass
class InjectionResult:
    omega: float
    eps_grid: list = field(default_factory=list)
    detection_rate: list = field(default_factory=list)


def inject_odd(u_sessions: list[tuple[np.ndarray, np.ndarray]], omega: float,
               eps_grid=(0.05, 0.10, 0.20, 0.30, 0.50), n_trial: int = 100,
               seed: int = 1) -> InjectionResult:
    """Handedness-modulation injection ON THE REAL SESSION TIMES: draw fresh
    signs from the modulated law P(s_i = +1) = (1 + eps cos(omega ln tau_i +
    phi))/2 (the physical odd-channel comb model: the handedness follows the
    clock), then run the standard odd test; a trial 'detects' if the
    Fisher-combined sign-permutation p < 0.01.

    Calibration-bug record (2026-07-15): the first implementation multiplied
    the OBSERVED signs by modulated flips -- the random observed signs
    scramble the injected phase coherence, so the detector saw ~nothing even
    at eps = 0.5.  The physical model modulates the handedness itself."""
    rng = np.random.default_rng(seed)
    res = InjectionResult(omega)
    usable = [u for u, _ in u_sessions
              if reach_periods(u, omega) > REACH_GATE_PERIODS
              and len(u) >= MIN_BURSTS_USED]
    if not usable:
        usable = [u for u, _ in u_sessions
                  if reach_periods(u, omega) > RELAXED_GATE_PERIODS
                  and len(u) >= RELAXED_MIN_BURSTS]
    if not usable:
        return res
    for eps in eps_grid:
        hits = 0
        for _ in range(n_trial):
            ps = []
            for u in usable:
                phi = rng.uniform(0, 2 * math.pi)
                p_plus = 0.5 * (1 + eps * np.cos(omega * u + phi))
                si = np.where(rng.uniform(size=len(u)) < p_plus, 1.0, -1.0)
                z_obs = signed_rayleigh(u, si, omega)
                null = np.array([signed_rayleigh(u, rng.permutation(si), omega)
                                 for _ in range(200)])
                ps.append(float((1 + np.sum(null >= z_obs)) / 201))
            if fisher(ps, 1 / 201) < 0.01:
                hits += 1
        res.eps_grid.append(eps)
        res.detection_rate.append(hits / n_trial)
    return res
