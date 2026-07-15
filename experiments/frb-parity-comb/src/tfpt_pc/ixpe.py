"""IX.01-IX.03 -- the IXPE leg (prereg v1.1 addendum, 2026-07-15): magnetar
1E 1841-045 post-outburst ToO (ObsID 03250499), EVEN-sector tests only (IXPE
is linear-only; the Z2-odd handedness channel does not exist in X-rays).

IX.01: omega_2 = 0.9532 FORBIDDEN even line on post-burst photon cascades.
IX.02: omega_1 = 2.5827 allowed even line (escalate-only).
IX.03: thinning-injection calibration on the real photon times.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from astropy.io import fits
from scipy.stats import poisson

from .constants import (N_SURROGATE, OMEGA_1, OMEGA_2, REACH_GATE_PERIODS,
                        RELAXED_GATE_PERIODS)
from .signed_comb import fisher, rayleigh_z, reach_periods, surrogate_lntau

DATA = Path(__file__).resolve().parents[2] / "data" / "ixpe"
FILES = [f"ixpe03250499_det{d}_evt2_v01.fits.gz" for d in (1, 2, 3)]

# preregistered (parity_comb_v1.1_ixpe.yaml)
PI_LO, PI_HI = 50, 200          # 2-8 keV (PI * 0.04 keV)
BIN_S = 0.1
LOCAL_WIN_S = 100.0
POISSON_TAIL = 1e-6
TAU_MIN_S = 0.1
GAP_END_S = 200.0
SESSION_MAX_S = 1.0e4
MIN_PHOTONS = 200


def load_events() -> np.ndarray:
    times = []
    for f in FILES:
        with fits.open(DATA / f) as h:
            ev = h["EVENTS"].data
            pi = ev["PI"]
            t = ev["TIME"][(pi >= PI_LO) & (pi <= PI_HI)]
            times.append(np.asarray(t, dtype=float))
    t = np.concatenate(times)
    t.sort()
    return t


@dataclass
class Burst:
    t_peak: float
    counts_peak: int
    local_rate: float
    tail_p: float


def find_bursts(t: np.ndarray) -> list[Burst]:
    """Preregistered finder: 0.1 s bins, local (+-50 s, burst bins excluded)
    Poisson mean, tail p < 1e-6; adjacent burst bins merged (peak bin kept)."""
    t0, t1 = t[0], t[-1]
    nbin = int(np.ceil((t1 - t0) / BIN_S))
    idx = np.minimum(((t - t0) / BIN_S).astype(np.int64), nbin - 1)
    counts = np.bincount(idx, minlength=nbin)
    w = int(LOCAL_WIN_S / BIN_S)
    bursts_bins: list[tuple[int, int, float, float]] = []
    hot = np.where(counts >= 5)[0]         # cheap pre-filter (mean ~ 0.6/bin)
    for b in hot:
        lo, hi = max(0, b - w), min(nbin, b + w + 1)
        local = np.delete(counts[lo:hi], np.arange(b - lo, b - lo + 1))
        mu = max(float(local.mean()), 1e-3)
        p = float(poisson.sf(counts[b] - 1, mu))
        if p < POISSON_TAIL:
            bursts_bins.append((b, int(counts[b]), mu, p))
    # merge adjacent bins (within 1 s), keep the peak
    merged: list[Burst] = []
    for b, c, mu, p in sorted(bursts_bins):
        tpk = t0 + (b + 0.5) * BIN_S
        if merged and tpk - merged[-1].t_peak < 1.0:
            if c > merged[-1].counts_peak:
                merged[-1] = Burst(tpk, c, mu, p)
        else:
            merged.append(Burst(tpk, c, mu, p))
    return merged


def burst_sessions(t: np.ndarray, bursts: list[Burst]) -> list[np.ndarray]:
    """ln(tau) arrays of post-burst photon cascades per the preregistered
    session rule (tau >= 0.1 s; end at next burst, arrival gap > 200 s, or
    1e4 s; >= 200 photons)."""
    out = []
    peaks = [b.t_peak for b in bursts]
    for i, tp in enumerate(peaks):
        t_end = tp + SESSION_MAX_S
        if i + 1 < len(peaks):
            t_end = min(t_end, peaks[i + 1])
        seg = t[(t > tp + TAU_MIN_S) & (t < t_end)]
        if len(seg) == 0:
            continue
        gaps = np.diff(seg)
        cut = np.where(gaps > GAP_END_S)[0]
        if len(cut):
            seg = seg[:cut[0] + 1]
        if len(seg) >= MIN_PHOTONS:
            out.append(np.log(seg - tp))
    return out


def even_comb_test(u: np.ndarray, omega: float, *, seed: int = 0) -> dict:
    n = len(u)
    rp = reach_periods(u, omega)
    if rp > REACH_GATE_PERIODS:
        gate = "primary"
    elif rp > RELAXED_GATE_PERIODS:
        gate = "relaxed"
    else:
        return {"n_photons": n, "reach_periods": round(rp, 3), "gate": "fail"}
    rng = np.random.default_rng(seed + n)
    z_obs = float(rayleigh_z(u, omega))
    z_sur = np.array([float(rayleigh_z(surrogate_lntau(u, rng), omega))
                      for _ in range(N_SURROGATE)])
    p = float((1 + np.sum(z_sur >= z_obs)) / (N_SURROGATE + 1))
    return {"n_photons": n, "reach_periods": round(rp, 3), "gate": gate,
            "z": round(z_obs, 4), "p_surrogate": round(p, 4)}


def inject_even(sessions: list[np.ndarray], omega: float,
                eps_grid=(0.05, 0.10, 0.20, 0.30), n_trial: int = 50,
                seed: int = 3) -> dict:
    """Thinning injection: keep each real photon with probability
    (1 + eps cos(omega ln tau + phi)) / (1 + eps), then the even test."""
    rng = np.random.default_rng(seed)
    usable = [u for u in sessions if reach_periods(u, omega) > RELAXED_GATE_PERIODS
              and len(u) >= MIN_PHOTONS]
    out = {"omega": omega, "eps_grid": list(eps_grid), "detection_rate": []}
    if not usable:
        return out
    for eps in eps_grid:
        hits = 0
        for _ in range(n_trial):
            ps = []
            for u in usable:
                phi = rng.uniform(0, 2 * np.pi)
                keep = rng.uniform(size=len(u)) < (
                    (1 + eps * np.cos(omega * u + phi)) / (1 + eps))
                ui = u[keep]
                if len(ui) < MIN_PHOTONS // 2:
                    continue
                z_obs = float(rayleigh_z(ui, omega))
                z_sur = np.array([float(rayleigh_z(surrogate_lntau(ui, rng), omega))
                                  for _ in range(200)])
                ps.append(float((1 + np.sum(z_sur >= z_obs)) / 201))
            if ps and fisher(ps, 1 / 201) < 0.01:
                hits += 1
        out["detection_rate"].append(hits / n_trial)
    return out
