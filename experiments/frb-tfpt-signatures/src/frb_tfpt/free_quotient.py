"""FRB.02b -- the free-quotient null (the central anti-numerology control).

FRB.02 asks "is there an excess of consecutive amplitude ratios near the FROZEN
kernel value 8/27?". That is necessary but not sufficient: a numerology critic rightly
demands that a model with a FREELY fitted quotient must NOT win somewhere else. So we
compare three models on the within-session consecutive amplitude ratios of a repeater:

    M0     : no echo  (flat null; surrogate baseline)
    Mfixed : echo at the frozen TFPT amplitude quotient q in {8/27, 1/27}
    Mfree  : echo at a free quotient q* in [0.01, 0.5]

scanning q over a grid and taking the look-elsewhere-corrected max. Decision rule:

  * if Mfree is significant (LEE-corrected) but q* is NOT at a kernel value
        -> the free template wins elsewhere => NOT a TFPT signal;
  * if Mfree is significant AND q* coincides with 8/27 (or 1/27)
        -> consistent with TFPT (the data prefer exactly the frozen quotient);
  * if nothing is significant
        -> M0: no echo structure (TFPT echo not required).

An injection-recovery check confirms the scan recovers q* ~ 8/27 when a real echo at
that quotient is injected. Surrogates: within-session energy shuffle (destroys
ordering, preserves the per-session energy distribution).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .data_io import RepeaterSeries
from .recovery_kernel import SQRT_LAMBDA2, SQRT_LAMBDA3  # 8/27, 1/27 (amplitude kernel)

KERNEL_AMP = {"8/27": SQRT_LAMBDA2, "1/27": SQRT_LAMBDA3}


def _within_session_amp_abslog(values: np.ndarray, sess: np.ndarray,
                               mjd: np.ndarray) -> np.ndarray:
    """|0.5 * log10(E_{n+1}/E_n)| for within-session consecutive pairs (amplitude,
    folded to magnitude so decay and its time-reverse both count)."""
    out = []
    for s in np.unique(sess):
        m = sess == s
        v, t = values[m], mjd[m]
        ok = np.isfinite(v) & (v > 0) & np.isfinite(t)
        v, t = v[ok], t[ok]
        if len(v) < 2:
            continue
        v = v[np.argsort(t)]
        out.append(np.abs(0.5 * np.log10(v[1:] / v[:-1])))
    return np.concatenate(out) if out else np.array([])


@dataclass
class FreeQuotientResult:
    source: str
    available: bool
    n_pairs: int = 0
    q_star: float = float("nan")          # best free amplitude quotient
    q_star_max_z: float = float("nan")    # scan-max z at q_star
    global_p: float = float("nan")        # look-elsewhere-corrected p of Mfree
    near_kernel: str | None = None        # which kernel value q_star matches (if any)
    fixed_enrichment: dict = field(default_factory=dict)  # kernel -> enrichment
    injection_recovered_q: float = float("nan")
    injection_ok: bool = False
    verdict: str = ""


def free_quotient_test(series: RepeaterSeries, q_lo: float = 0.01, q_hi: float = 0.5,
                       n_grid: int = 80, half_window_dex: float = 0.10,
                       n_surrogate: int = 800, kernel_tol_dex: float = 0.05,
                       seed: int = 0) -> FreeQuotientResult:
    if not series.available:
        return FreeQuotientResult(series.source, False, verdict="data-limited")
    val = series.energy if np.isfinite(series.energy).sum() else series.fluence
    if not np.isfinite(val).sum():
        return FreeQuotientResult(series.source, False, verdict="data-limited (no energy/fluence)")
    sess = series.session_id if series.session_id.size else np.zeros(len(series.mjd))
    mjd = series.mjd
    x = _within_session_amp_abslog(val, sess, mjd)
    n = len(x)
    if n < 30:
        return FreeQuotientResult(series.source, True, n, verdict=f"too few pairs ({n})")

    grid_q = np.logspace(math.log10(q_lo), math.log10(q_hi), n_grid)
    grid_t = np.abs(np.log10(grid_q))                       # target |log10 q|

    def counts(xv: np.ndarray) -> np.ndarray:
        return np.array([np.sum(np.abs(xv - t) <= half_window_dex) for t in grid_t])

    obs = counts(x)
    rng = np.random.default_rng(seed)
    surr = np.empty((n_surrogate, n_grid))
    for i in range(n_surrogate):
        v2 = val.copy()
        for s in np.unique(sess):
            idx = np.where(sess == s)[0]
            v2[idx] = rng.permutation(val[idx])
        surr[i] = counts(_within_session_amp_abslog(v2, sess, mjd))

    mean = surr.mean(0)
    std = surr.std(0) + 1e-9
    z = (obs - mean) / std
    surr_z = (surr - mean) / std
    obs_max_z = float(z.max())
    j_star = int(np.argmax(z))
    q_star = float(grid_q[j_star])
    surr_max_z = surr_z.max(axis=1)
    global_p = float((1 + np.sum(surr_max_z >= obs_max_z)) / (n_surrogate + 1))

    # which kernel value (if any) does q* coincide with?
    near = None
    for name, kv in KERNEL_AMP.items():
        if abs(math.log10(q_star) - math.log10(kv)) <= kernel_tol_dex:
            near = name
    fixed = {}
    for name, kv in KERNEL_AMP.items():
        t = abs(math.log10(kv))
        oc = int(np.sum(np.abs(x - t) <= half_window_dex))
        mc = float(mean[int(np.argmin(np.abs(grid_t - t)))])   # null at nearest grid node
        fixed[name] = oc / (mc or 1e-9)

    # injection-recovery: inject a real echo at 8/27 and confirm the scan finds it
    inj_q, inj_ok = _injection_recovery(val, sess, grid_q, grid_t, half_window_dex,
                                        kernel_tol_dex, rng)

    sig = global_p < 0.05
    if sig and near:
        verdict = (f"free quotient q*={q_star:.3f} is significant (LEE p={global_p:.3f}) AND "
                   f"coincides with the kernel value {near} -> consistent with TFPT")
    elif sig and not near:
        verdict = (f"free quotient q*={q_star:.3f} wins (LEE p={global_p:.3f}) but is NOT a "
                   f"kernel value -> NOT a TFPT signal (the free template prefers elsewhere)")
    else:
        verdict = (f"no significant echo at any quotient (LEE p={global_p:.3f}); best q*="
                   f"{q_star:.3f} -> M0 (no echo structure; TFPT echo not required)")
    return FreeQuotientResult(series.source, True, n, q_star, obs_max_z, global_p, near,
                              fixed, inj_q, inj_ok, verdict)


def _injection_recovery(val, sess, grid_q, grid_t, hw, tol, rng):
    """Inject a clean echo at q=8/27 (interleave each shuffled burst with an echo at
    energy*q^2) and confirm the scan recovers q* ~ 8/27 -- validates the method finds
    the kernel quotient when a real echo at that quotient is present."""
    q_inj = SQRT_LAMBDA2
    xs = []
    for s in np.unique(sess):
        idx = np.where(sess == s)[0]
        v = val[idx]
        v = v[np.isfinite(v) & (v > 0)]
        if len(v) < 2:
            continue
        v = rng.permutation(v)
        seq = np.empty(2 * len(v))
        seq[0::2] = v
        seq[1::2] = v * (q_inj ** 2)                 # echo energy = burst energy * q^2
        xs.append(np.abs(0.5 * np.log10(seq[1:] / seq[:-1])))
    if not xs:
        return float("nan"), False
    x = np.concatenate(xs)
    obs = np.array([np.sum(np.abs(x - t) <= hw) for t in grid_t])
    q_rec = float(grid_q[int(np.argmax(obs))])
    ok = abs(math.log10(q_rec) - math.log10(q_inj)) <= tol
    return q_rec, ok


@dataclass
class MultiSourceFreeQuotient:
    sources: list[str]
    per_source: dict = field(default_factory=dict)
    tfpt_consistent: list[str] = field(default_factory=list)
    nonkernel_wins: list[str] = field(default_factory=list)
    verdict: str = ""


def multi_source_free_quotient(series_list: list[RepeaterSeries], n_surrogate: int = 600,
                               seed: int = 0) -> MultiSourceFreeQuotient:
    per, names, tfpt_ok, nonkernel = {}, [], [], []
    for s in series_list:
        r = free_quotient_test(s, n_surrogate=n_surrogate, seed=seed)
        if not r.available or r.n_pairs < 30:
            continue
        names.append(r.source)
        per[r.source] = {"n_pairs": r.n_pairs, "q_star": r.q_star, "global_p": r.global_p,
                         "near_kernel": r.near_kernel, "injection_ok": r.injection_ok,
                         "injection_recovered_q": r.injection_recovered_q, "verdict": r.verdict}
        if r.global_p < 0.05 and r.near_kernel:
            tfpt_ok.append(r.source)
        elif r.global_p < 0.05 and not r.near_kernel:
            nonkernel.append(r.source)
    if tfpt_ok and not nonkernel:
        verdict = f"free quotient lands on a kernel value in {tfpt_ok} (TFPT-consistent)"
    elif nonkernel:
        verdict = f"free quotient wins at NON-kernel values in {nonkernel} -> not TFPT"
    else:
        verdict = f"no source shows a significant echo at any quotient ({len(names)} tested) -> M0"
    return MultiSourceFreeQuotient(names, per, tfpt_ok, nonkernel, verdict)
