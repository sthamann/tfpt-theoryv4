"""Stage-2 DYNAMIC recovery-waveform matched filter on REAL GWOSC strain.

The catalogue census (echo_forecast.py) and the Stage-1 echo search (real_echo_search.py)
both test the recovery kernel as a STATIC amplitude ratio: consecutive echo amplitudes
bounded by (2/3)^6. The experiments/README §1.1 "Reconsideration" notes that this misses
the kernel's *dynamic* signature -- the exact discrete->dynamic transition (verification
v124/v126/v147, mirrored in quantum-testbed/clock.py QT.04) is a **walled two-mode clock**

    R(t) = w0 + w1 e^{-(6 ln 3/2) t/tau} + w2 e^{-(6 ln 3) t/tau}

with three sharp signatures that a static ratio cannot carry:

  1. BEND (det'-clean, v147): the two decay rates are LOCKED at the ratio
        rate(2)/rate(1) = ln 3 / ln(3/2) = log_{3/2} 3 = 2.7095        (frozen, exact)
     -- a ONE-parameter (tau) two-exponential template, not a free rate pair.
  2. PROTECTED FLOOR: a non-decaying w0 mode (lambda=1, the "law") -> the recovery
     saturates at a floor and never returns to zero.
  3. HARD WALL: NO third decay mode (pole at n = N_fam = 3) -> >= 3 robust decay
     timescales would be a tension, not a TFPT recovery.

This module turns that bend into a matched-filter run on REAL strain: for each event we
whiten once, subtract the dominant Kerr (l=m=2,n=0) ringdown, build the **post-merger
residual power envelope** (binned RMS), and fit the FIXED-RATIO (2.7095) walled-clock
template against the envelope. Significance comes from an OFF-SOURCE background (the same
fit on many noise-only windows), and a FREE two-rate control recovers the bend ratio
q_hat (anti-numerology, cf. FRB.02b / the Stage-1 echo q_hat).

Firewall / honest scope: TFPT does NOT claim ringdown recovery imprints are present --
the kernel ratio is an UPPER bound, so a null/data-limited result is consistent. A loud
single-exponential decay (leftover ringdown power from imperfect dominant-mode subtraction)
has q_hat far from the bend and is rejected by the free-ratio control -- it is NOT a kernel
recovery. No detection claim is made; this closes the "machinery only validated on
synthetic data" gap by running it on real, public strain. Python (numpy/scipy/h5py).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .strain_data import (
    apply_whitening,
    fit_and_subtract_qnm,
    qnm_220,
    read_hdf5,
    whitening_filter,
)

# --- frozen walled-clock constants (derived from the two axioms; mirror QT.04 clock.py) ---
N_FAM = 3
P2 = 6
RATE1 = P2 * math.log(1.5)          # 6 ln(3/2) = Delta = 2.4328   (slow mode)
RATE2 = P2 * math.log(3.0)          # 6 ln 3    = 6.5917           (fast mode)
BEND = math.log(3.0) / math.log(1.5)  # rate(2)/rate(1) = log_{3/2} 3 = 2.7095 (frozen)
BEND_LOG_TOL = math.log(1.15)       # free ratio counts as the bend within +-15% (QT.04 tol)

WIN_TAU = 40.0                      # analysis window length in QNM damping times tau
WIN_MAX_S = 0.30                    # but never longer than 0.3 s post-merger
N_BINS = 40                         # RMS-envelope bins across the window
N_BACKGROUND = 400                  # off-source windows for the noise background
P_THRESHOLD = 0.01


# --------------------------------------------------------------------------- the envelope
def power_envelope(series: np.ndarray, start: int, win_samp: int,
                   n_bins: int = N_BINS) -> tuple[np.ndarray, np.ndarray]:
    """Binned RMS power envelope of `series[start:start+win_samp]` -> (t_norm, env).

    `t_norm` is the bin-centre time in units of the window length (0..1); the envelope is
    the per-bin root-mean-square. Pure white noise gives a flat envelope; leftover ringdown
    or a recovery relaxation gives a decay toward a floor."""
    seg = series[start:start + win_samp]
    if len(seg) < win_samp or win_samp < n_bins:
        return np.array([]), np.array([])
    edges = np.linspace(0, win_samp, n_bins + 1).astype(int)
    env = np.array([math.sqrt(float(np.mean(seg[edges[i]:edges[i + 1]] ** 2)))
                    for i in range(n_bins)])
    centres = 0.5 * (edges[:-1] + edges[1:]) / win_samp
    return centres, env


# --------------------------------------------------------------------------- the fits
def _r2(y: np.ndarray, resid: np.ndarray) -> float:
    """Fraction of envelope variance explained vs a constant-only model."""
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return 0.0 if ss_tot == 0 else 1.0 - float(np.sum(resid ** 2)) / ss_tot


def fit_walled_clock(t: np.ndarray, env: np.ndarray, n_scan: int = 200) -> tuple[float, float]:
    """Fit floor + two LOCKED-ratio exponentials ``w0 + w1 e^{-r t} + w2 e^{-BEND r t}``.

    Scan the slow decay constant r, solve the 3 amplitudes by least squares (the bend ratio
    is fixed). Returns (best r, R^2-vs-constant) -- the matched-filter statistic."""
    if len(t) == 0:
        return 0.0, 0.0
    rs = np.logspace(math.log10(0.5), math.log10(60.0), n_scan)
    best_r, best_r2 = rs[0], -np.inf
    for r in rs:
        X = np.column_stack([np.ones_like(t), np.exp(-r * t), np.exp(-BEND * r * t)])
        beta, *_ = np.linalg.lstsq(X, env, rcond=None)
        r2 = _r2(env, X @ beta - env)
        if r2 > best_r2:
            best_r, best_r2 = r, r2
    return best_r, best_r2


def fit_free_ratio(t: np.ndarray, env: np.ndarray, n_scan: int = 90) -> tuple[float, float]:
    """Fit floor + two FREE exponential rates; return (recovered ratio r2/r1, R^2)."""
    if len(t) == 0:
        return 0.0, 0.0
    rs = np.logspace(math.log10(0.5), math.log10(60.0), n_scan)
    best_ratio, best_r2 = 1.0, -np.inf
    for i in range(n_scan):
        for j in range(i + 1, n_scan):
            X = np.column_stack([np.ones_like(t), np.exp(-rs[i] * t), np.exp(-rs[j] * t)])
            beta, *_ = np.linalg.lstsq(X, env, rcond=None)
            r2 = _r2(env, X @ beta - env)
            if r2 > best_r2:
                best_ratio, best_r2 = rs[j] / rs[i], r2
    return best_ratio, best_r2


# --------------------------------------------------------------------------- real-data search
@dataclass
class DynamicDetectorResult:
    detector: str
    r2_template: float          # fixed-bend walled-clock template R^2
    q_hat: float                # free-fit recovered rate ratio (the bend estimate)
    p_value: float              # off-source background p-value for r2_template
    kernel_consistent: bool     # p<thr AND q_hat ~ bend (a walled-clock recovery)


@dataclass
class DynamicEventResult:
    event: str
    mf_msun: float
    tau_ms: float
    detectors: list[DynamicDetectorResult] = field(default_factory=list)
    n_kernel_consistent: int = 0
    label: str = ""
    note: str = ""


def _envelope_statistic(series: np.ndarray, start: int, win_samp: int) -> tuple[float, float]:
    """(r2_template, q_hat) for the walled-clock fit of the envelope at `start`."""
    t, env = power_envelope(series, start, win_samp)
    if len(t) == 0:
        return -1.0, 0.0
    _, r2_tmpl = fit_walled_clock(t, env)
    q_hat, _ = fit_free_ratio(t, env)
    return r2_tmpl, q_hat


def search_event_dynamic(event: str, strain_dir, af: float = 0.69,
                         seed: int = 0) -> DynamicEventResult:
    """Run the dynamic walled-clock matched filter on the real strain of `event`."""
    meta = json.loads((Path(strain_dir) / f"{event}_meta.json").read_text(encoding="utf-8"))
    merger_gps, mf = float(meta["gps"]), float(meta["mf"])
    f0, tau = qnm_220(mf, af)
    res = DynamicEventResult(event, mf, round(tau * 1e3, 2))
    rng = np.random.default_rng(seed)

    for det, fname in meta["files"].items():
        s = read_hdf5(str(Path(strain_dir) / Path(fname).name))
        psd_i, scale = whitening_filter(s.data, s.dt)
        white = apply_whitening(s.data, psd_i, scale)
        merger = s.index_at(merger_gps)
        resid, _ = fit_and_subtract_qnm(white, merger, f0, tau, s.dt)

        win_samp = min(int(WIN_TAU * tau / s.dt), int(WIN_MAX_S / s.dt))
        r2_on, q_hat = _envelope_statistic(resid, merger, win_samp)

        guard = int(1.0 / s.dt)
        lo, hi = guard, len(resid) - win_samp - guard
        centres = rng.integers(lo, hi, size=N_BACKGROUND)
        bg = np.array([_envelope_statistic(resid, int(c), win_samp)[0]
                       for c in centres if abs(int(c) - merger) > win_samp])
        p_val = float((np.sum(bg >= r2_on) + 1) / (len(bg) + 1))
        on_bend = abs(math.log(q_hat / BEND)) < BEND_LOG_TOL if q_hat > 0 else False
        kc = bool(p_val < P_THRESHOLD and on_bend)
        res.detectors.append(DynamicDetectorResult(det, round(r2_on, 4), round(q_hat, 4),
                                                    round(p_val, 4), kc))

    res.n_kernel_consistent = sum(d.kernel_consistent for d in res.detectors)
    res.label = ("WALLED_CLOCK_RECOVERY_CANDIDATE" if res.n_kernel_consistent >= 2
                 else "NO_KERNEL_RECOVERY")
    loud = [d for d in res.detectors if d.p_value < P_THRESHOLD]
    if loud and res.n_kernel_consistent == 0:
        res.note = (f"low-p decaying envelope in {[d.detector for d in loud]} but q_hat="
                    f"{[d.q_hat for d in loud]} far from the bend {BEND:.3f} -> leftover "
                    "single-mode ringdown power, NOT a locked-ratio walled-clock recovery "
                    "(free-ratio control)")
    return res


# --------------------------------------------------------------------------- injection suite
def walled_clock_envelope(t: np.ndarray, tau: float, ratio: float = BEND) -> np.ndarray:
    """Synthetic recovery envelope: floor + two exponentials at rate-ratio `ratio`."""
    return 0.2 + 0.6 * np.exp(-RATE1 * t / tau) + 0.4 * np.exp(-ratio * RATE1 * t / tau)


@dataclass
class DynamicInjectionResult:
    case: str
    r2_template: float
    q_hat: float
    label: str           # KERNEL_RECOVERY / NULL / NON_KERNEL_RECOVERY
    expected: str
    correct: bool


def _classify(r2_tmpl: float, q_hat: float, *, r2_floor: float) -> str:
    if r2_tmpl < r2_floor:
        return "NULL"
    return ("KERNEL_RECOVERY" if (q_hat > 0 and abs(math.log(q_hat / BEND)) < BEND_LOG_TOL)
            else "NON_KERNEL_RECOVERY")


def inject_once(case: str, noise_series: np.ndarray, dt: float, *, f0: float = 250.0,
                tau_rec_s: float = 0.04, amp: float = 6.0, seed: int = 0) -> DynamicInjectionResult:
    """Inject a recovery-modulated narrowband burst into a REAL off-source noise segment,
    run the same envelope + walled-clock fit, and classify it."""
    rng = np.random.default_rng(seed)
    start = rng.integers(len(noise_series) // 4, len(noise_series) // 2)
    win_samp = min(int(WIN_TAU * 0.004 / dt), int(WIN_MAX_S / dt))
    k = np.arange(win_samp)
    t = k * dt
    carrier = np.cos(2.0 * np.pi * f0 * t)
    env_clock = {"kernel": walled_clock_envelope(t, tau_rec_s, BEND),
                 "null": np.zeros_like(t),
                 "wrong_ratio": walled_clock_envelope(t, tau_rec_s, 6.0)}[case]
    seg = noise_series[start:start + win_samp].copy()
    sigma = float(np.std(seg)) or 1.0
    injected = seg + amp * sigma * env_clock * carrier
    series = noise_series.copy()
    series[start:start + win_samp] = injected

    r2_tmpl, q_hat = _envelope_statistic(series, int(start), win_samp)
    label = _classify(r2_tmpl, q_hat, r2_floor=0.3)
    expected = {"kernel": "KERNEL_RECOVERY", "null": "NULL",
                "wrong_ratio": "NON_KERNEL_RECOVERY"}[case]
    return DynamicInjectionResult(case, round(r2_tmpl, 4), round(q_hat, 4),
                                  label, expected, label == expected)


@dataclass
class DynamicInjectionSuite:
    results: list[DynamicInjectionResult] = field(default_factory=list)
    n_correct: int = 0
    n_total: int = 0
    verdict: str = ""


def injection_suite_dynamic(noise_series: np.ndarray, dt: float,
                            seed: int = 0) -> DynamicInjectionSuite:
    """Validate the dynamic pipeline on real off-source noise: a kernel-bend recovery, a
    no-recovery null, and a wrong-ratio recovery must be separated."""
    suite = DynamicInjectionSuite()
    for i, case in enumerate(("kernel", "null", "wrong_ratio")):
        suite.results.append(inject_once(case, noise_series, dt, seed=seed + i))
    suite.n_total = len(suite.results)
    suite.n_correct = sum(r.correct for r in suite.results)
    ok = suite.n_correct == suite.n_total
    suite.verdict = (
        f"dynamic walled-clock matched filter validated on real off-source noise: "
        f"{suite.n_correct}/{suite.n_total} injections correctly classified -- the pipeline "
        f"(whiten + Kerr subtraction + RMS envelope + fixed-bend {BEND:.4f} template + "
        f"free-ratio control) separates a kernel-bend recovery, a no-recovery null and a "
        f"wrong-ratio recovery. No recovery claim on real data is made."
        if ok else
        f"FAIL: only {suite.n_correct}/{suite.n_total} injections classified correctly"
    )
    return suite
