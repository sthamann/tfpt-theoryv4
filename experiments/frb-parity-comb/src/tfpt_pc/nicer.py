"""NI.01-NI.03 -- the NICER burst-storm leg (prereg v1.2 addendum,
2026-07-15): SGR 1935+2154, ObsID 3020560101 (the 2020-04-28 storm;
Younes et al. 2020, ApJL 904 L21).  EVEN-sector arrival-time tests only.

Family A: storm-cascade sessions (burst PEAK times, u = ln(t_peak - t_storm)).
Family B: post-burst photon cascades (IXPE v1.1 machinery, band 1-10 keV).
Fallback rule (preregistered): if the cl file's GTI coverage of the storm
cluster is < 50% of the ufa coverage, the ufa file replaces it (recorded).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from astropy.io import fits
from scipy.stats import poisson

from .constants import (N_SURROGATE, REACH_GATE_PERIODS, RELAXED_GATE_PERIODS)
from .signed_comb import rayleigh_z, reach_periods, surrogate_lntau

DATA = Path(__file__).resolve().parents[2] / "data" / "nicer"
FILE_CL = "ni3020560101_0mpu7_cl.evt.gz"
FILE_UFA = "ni3020560101_0mpu7_ufa.evt.gz"

# preregistered (parity_comb_v1.2_nicer.yaml)
PI_LO, PI_HI = 100, 1000        # 1-10 keV (PI * 0.01 keV)
BIN_S = 0.05
LOCAL_WIN_S = 100.0
POISSON_TAIL = 1e-6
MERGE_S = 0.5
TAU_MIN_A = 0.5                 # family A (burst-time cascade)
MIN_BURSTS_A = 30
TAU_MIN_B = 0.1                 # family B (photon cascade)
GAP_END_S = 200.0
SESSION_MAX_S = 1.0e4
MIN_PHOTONS_B = 200
CLUSTER_GAP_S = 500.0           # bursts closer than this belong to one cluster


def _load(fname: str) -> tuple[np.ndarray, np.ndarray]:
    """(event times in band, GTI array [start, stop])."""
    with fits.open(DATA / fname) as h:
        ev = h["EVENTS"].data
        pi = ev["PI"]
        t = np.asarray(ev["TIME"][(pi >= PI_LO) & (pi <= PI_HI)], dtype=float)
        gti = np.array([(row[0], row[1]) for row in h["GTI"].data], dtype=float)
    t.sort()
    return t, gti


@dataclass
class Burst:
    t_peak: float
    counts_peak: int
    local_rate: float
    tail_p: float


def find_bursts(t: np.ndarray) -> list[Burst]:
    """Preregistered finder: 0.05 s bins, local +-50 s Poisson mean (burst
    bins excluded via one-pass exclusion of the candidate bin), tail
    p < 1e-6; adjacent burst bins within 0.5 s merged (peak kept)."""
    if len(t) == 0:
        return []
    t0, t1 = t[0], t[-1]
    nbin = int(np.ceil((t1 - t0) / BIN_S))
    idx = np.minimum(((t - t0) / BIN_S).astype(np.int64), nbin - 1)
    counts = np.bincount(idx, minlength=nbin)
    w = int(LOCAL_WIN_S / BIN_S)
    med = max(float(np.median(counts[counts > 0])), 0.05)
    hot = np.where(counts >= max(5, int(6 * med)))[0]
    cands: list[tuple[int, int, float, float]] = []
    for b in hot:
        lo, hi = max(0, b - w), min(nbin, b + w + 1)
        local = np.delete(counts[lo:hi], b - lo)
        mu = max(float(np.median(local)), 1e-3)   # median: storm-robust
        p = float(poisson.sf(int(counts[b]) - 1, mu))
        if p < POISSON_TAIL:
            cands.append((b, int(counts[b]), mu, p))
    merged: list[Burst] = []
    for b, c, mu, p in sorted(cands):
        tpk = t0 + (b + 0.5) * BIN_S
        if merged and tpk - merged[-1].t_peak < MERGE_S:
            if c > merged[-1].counts_peak:
                merged[-1] = Burst(tpk, c, mu, p)
        else:
            merged.append(Burst(tpk, c, mu, p))
    return merged


def clusters(bursts: list[Burst]) -> list[list[Burst]]:
    out: list[list[Burst]] = []
    for b in bursts:
        if out and b.t_peak - out[-1][-1].t_peak < CLUSTER_GAP_S:
            out[-1].append(b)
        else:
            out.append([b])
    return out


def gti_coverage(gti: np.ndarray, t_lo: float, t_hi: float) -> float:
    if len(gti) == 0:
        return 0.0
    lo = np.maximum(gti[:, 0], t_lo)
    hi = np.minimum(gti[:, 1], t_hi)
    return float(np.sum(np.maximum(hi - lo, 0.0)))


def choose_file() -> dict:
    """Apply the preregistered cl-vs-ufa fallback rule; returns the choice
    plus the recorded coverage numbers."""
    t_ufa, gti_ufa = _load(FILE_UFA)
    bursts_ufa = find_bursts(t_ufa)
    cls_ufa = clusters(bursts_ufa)
    if cls_ufa:
        storm = max(cls_ufa, key=len)
        lo = storm[0].t_peak - 100.0
        hi = storm[-1].t_peak + 100.0
    else:                                   # no storm anywhere: keep cl
        lo, hi = t_ufa[0], t_ufa[-1]
    _, gti_cl = _load(FILE_CL)
    cov_cl = gti_coverage(gti_cl, lo, hi)
    cov_ufa = gti_coverage(gti_ufa, lo, hi)
    use_ufa = cov_cl < 0.5 * cov_ufa
    return {"storm_window_met": [round(lo, 1), round(hi, 1)],
            "n_bursts_ufa_total": len(bursts_ufa),
            "coverage_cl_s": round(cov_cl, 1),
            "coverage_ufa_s": round(cov_ufa, 1),
            "use_ufa": bool(use_ufa),
            "file": FILE_UFA if use_ufa else FILE_CL}


def storm_sessions(bursts: list[Burst]) -> list[np.ndarray]:
    """Family A: one ln(tau) array per burst cluster with >= 30 bursts;
    t_storm = first peak of the cluster, tau >= 0.5 s."""
    out = []
    for cl in clusters(bursts):
        if len(cl) < MIN_BURSTS_A:
            continue
        t_storm = cl[0].t_peak
        tau = np.array([b.t_peak - t_storm for b in cl[1:]])
        tau = tau[tau >= TAU_MIN_A]
        if len(tau) + 1 >= MIN_BURSTS_A:
            out.append(np.log(tau))
    return out


def photon_sessions(t: np.ndarray, bursts: list[Burst]) -> list[np.ndarray]:
    """Family B: post-burst photon cascades (v1.1 rule, NICER band)."""
    out = []
    peaks = [b.t_peak for b in bursts]
    for i, tp in enumerate(peaks):
        t_end = tp + SESSION_MAX_S
        if i + 1 < len(peaks):
            t_end = min(t_end, peaks[i + 1])
        seg = t[(t > tp + TAU_MIN_B) & (t < t_end)]
        if len(seg) == 0:
            continue
        gaps = np.diff(seg)
        cut = np.where(gaps > GAP_END_S)[0]
        if len(cut):
            seg = seg[:cut[0] + 1]
        if len(seg) >= MIN_PHOTONS_B:
            out.append(np.log(seg - tp))
    return out


def even_comb_test(u: np.ndarray, omega: float, *, min_n: int,
                   seed: int = 0) -> dict:
    n = len(u)
    rp = reach_periods(u, omega)
    if n < min_n:
        return {"n": n, "reach_periods": round(rp, 3), "gate": "fail"}
    if rp > REACH_GATE_PERIODS:
        gate = "primary"
    elif rp > RELAXED_GATE_PERIODS:
        gate = "relaxed"
    else:
        return {"n": n, "reach_periods": round(rp, 3), "gate": "fail"}
    rng = np.random.default_rng(seed + n)
    z_obs = float(rayleigh_z(u, omega))
    z_sur = np.array([float(rayleigh_z(surrogate_lntau(u, rng), omega))
                      for _ in range(N_SURROGATE)])
    p = float((1 + np.sum(z_sur >= z_obs)) / (N_SURROGATE + 1))
    return {"n": n, "reach_periods": round(rp, 3), "gate": gate,
            "z": round(z_obs, 4), "p_surrogate": round(p, 4)}


def inject_thinning(sessions: list[np.ndarray], omega: float, *, min_n: int,
                    eps_grid=(0.0, 0.05, 0.10, 0.20, 0.30, 0.50),
                    n_trial: int = 50, seed: int = 5) -> dict:
    """NI.03: comb-modulated thinning of the real times (family A: burst
    peaks; family B: photons), then the even test; a trial detects when the
    FISHER-combined surrogate p across sessions is < 0.01 (the same
    criterion as NI.01/NI.02 -- a per-session threshold would be badly
    anti-conservative with O(100) sessions).  eps = 0 is the recorded
    false-positive baseline: with clustered burst-time sessions the smooth
    log-density surrogate is anti-conservative, and the baseline QUANTIFIES
    that."""
    from .signed_comb import fisher

    rng = np.random.default_rng(seed)
    usable = [u for u in sessions
              if reach_periods(u, omega) > RELAXED_GATE_PERIODS
              and len(u) >= min_n]
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
                if len(ui) < max(10, min_n // 2):
                    continue
                z_obs = float(rayleigh_z(ui, omega))
                z_sur = np.array([float(rayleigh_z(surrogate_lntau(ui, rng),
                                                   omega))
                                  for _ in range(200)])
                ps.append(float((1 + np.sum(z_sur >= z_obs)) / 201))
            if ps and fisher(ps, 1 / 201) < 0.01:
                hits += 1
        out["detection_rate"].append(hits / n_trial)
    return out


def load_chosen() -> tuple[np.ndarray, np.ndarray, dict]:
    choice = choose_file()
    t, gti = _load(choice["file"])
    return t, gti, choice
