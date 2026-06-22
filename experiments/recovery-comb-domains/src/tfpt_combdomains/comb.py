"""The shared, injection-validated log-periodic recovery-comb detector.

The "new" TFPT signature is not a number but a SHAPE: a system relaxing to a fixed point through
the frozen geometric mode ladder leaves a log-periodic (discrete-scale-invariance) comb on its
recovery curve,

    R(t) = (power law) * (1 + eps cos(omega ln t + phi)),
    omega = 2 pi / ln(lambda),  lambda = (3/2)^6,  -> omega = 2.583,
    eps  ~ exp(-pi^2 / ln lambda) ~ 0.02   (the QT.02 amplitude-suppression law).

Everything is DERIVED from the two axioms (c3 = 1/(8 pi), g_car = 5); no domain number enters.
The detector asks whether the comb at the KERNEL omega is SPECIAL in a recovery curve, by ranking
the comb gain at omega against a periodogram of off-kernel log-frequencies (a degree-2
polynomial-in-ln(t) baseline absorbs the smooth power-law/recovery trend, so a pure power law is
NOT flagged). Validated identically to PG.05/PG.06: it fires on a geometric-ladder comb and not on
a smooth decay, and ONLY when the curve spans >~2.8 comb periods in ln(t) (the hard ln-range
requirement that no amount of stacking can relax).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# --- frozen kernel (from the two axioms) ---
N_FAM = 3
P2 = 6
LAMBDA = 1.5 ** P2                       # (3/2)^6 = 11.39, the cascade scale
OMEGA = 2.0 * math.pi / math.log(LAMBDA)  # 2.583, the comb log-frequency
EPS_PREDICTED = math.exp(-math.pi ** 2 / math.log(LAMBDA))  # ~0.017, QT.02 suppression law
MIN_COMB_PERIODS = 2.8                   # ln(tau) range needed to localise omega (machine-checked)
DETREND_DEG = 2
P_THRESHOLD = 0.05


def _comb_gain(lt: np.ndarray, y: np.ndarray, omega: float, deg: int = DETREND_DEG) -> float:
    """Fractional variance explained by cos/sin(omega ln t) over a degree-`deg` poly-in-ln(t)
    baseline (which absorbs the smooth recovery trend)."""
    P = np.vander(lt, deg + 1)
    b0, *_ = np.linalg.lstsq(P, y, rcond=None)
    ss0 = float(np.sum((y - P @ b0) ** 2))
    X = np.column_stack([P, np.cos(omega * lt), np.sin(omega * lt)])
    b1, *_ = np.linalg.lstsq(X, y, rcond=None)
    return max(0.0, (ss0 - float(np.sum((y - X @ b1) ** 2))) / (ss0 + 1e-12))


def detect_comb(t: np.ndarray, rec: np.ndarray, *, omega: float = OMEGA,
                n_freq: int = 600, seed: int = 0) -> tuple[float, float]:
    """Is a log-periodic comb at `omega` SPECIAL in this recovery curve? Returns (gain, p) where
    p = fraction of off-kernel log-frequencies whose comb gain >= the kernel gain (periodogram
    rank). A smooth power-law recovery -> p ~ 0.5; a genuine geometric-ladder comb -> p << 0.05."""
    m = t > 0
    lt, y = np.log(np.asarray(t)[m]), np.asarray(rec)[m]
    if len(lt) < 6:
        return 0.0, 1.0
    g0 = _comb_gain(lt, y, omega)
    ln_range = float(lt.max() - lt.min()) or 1.0
    f_lo = max(0.9, 2.0 * math.pi / ln_range)
    rng = np.random.default_rng(seed)
    fs = rng.uniform(f_lo, max(6.0, 2.5 * omega), n_freq)
    fs = fs[np.abs(fs - omega) > 0.1 * omega]
    null = np.array([_comb_gain(lt, y, f) for f in fs])
    return g0, float((1 + np.sum(null >= g0)) / (len(null) + 1))


def comb_periods(t: np.ndarray) -> float:
    """Number of comb periods the curve spans in ln(t) = ln(t_max/t_min)/ln(lambda)."""
    t = np.asarray(t)
    t = t[t > 0]
    return float(np.log(t.max() / t.min()) / math.log(LAMBDA)) if len(t) > 1 else 0.0


# --------------------------------------------------------------------------- injection validation
def _power_law_comb(t: np.ndarray, eps: float, alpha: float = 0.5) -> np.ndarray:
    return t ** (-alpha) * (1.0 + eps * np.cos(OMEGA * np.log(t)))


def _detect_rate(periods: float, eps: float, noise: float, *, n_seeds: int = 25,
                 n_pts: int = 70) -> float:
    tmax = math.exp(periods * math.log(LAMBDA))
    t = np.logspace(0.0, math.log10(tmax), n_pts)
    base = _power_law_comb(t, eps)
    hits = 0
    for s in range(n_seeds):
        rng = np.random.default_rng(s)
        _, p = detect_comb(t, base * (1.0 + rng.normal(0.0, noise, n_pts)), seed=s)
        hits += int(p < P_THRESHOLD)
    return hits / n_seeds


@dataclass
class CombValidation:
    eps: float
    noise: float
    n_seeds: int
    sufficient_periods: float
    sufficient_comb_rate: float    # comb present, enough ln-range -> should be high
    sufficient_null_rate: float    # no comb (eps=0) -> false-positive, should be ~0
    short_periods: float
    short_comb_rate: float         # comb present but too few periods -> range-blind, ~0
    passed: bool


def validate_detector(*, eps: float = 0.30, noise: float = 0.10, n_seeds: int = 25,
                      short_periods: float = 1.9) -> CombValidation:
    """Reusable proof that the detector (a) fires on a comb when the ln-range is sufficient,
    (b) does not fire on a smooth decay, (c) is RANGE-BLIND below ~2.8 comb periods."""
    sc = _detect_rate(MIN_COMB_PERIODS, eps, noise, n_seeds=n_seeds)
    sn = _detect_rate(MIN_COMB_PERIODS, 0.0, noise, n_seeds=n_seeds)
    short = _detect_rate(short_periods, eps, noise, n_seeds=n_seeds)
    passed = bool(sc >= 0.6 and sn <= 0.12 and short < 0.2)
    return CombValidation(eps, noise, n_seeds, MIN_COMB_PERIODS, sc, sn,
                          short_periods, short, passed)


def run_comb(t: np.ndarray, rec: np.ndarray, *, seed: int = 0) -> dict:
    """Apply the detector to a real recovery curve and report with the ln-range gate."""
    periods = comb_periods(t)
    gain, p = detect_comb(t, rec, seed=seed)
    enough = periods >= MIN_COMB_PERIODS
    detected = bool(p < P_THRESHOLD and enough)
    return {"n_points": int(len(t)), "comb_periods": round(periods, 2),
            "range_sufficient": enough, "gain": round(gain, 4), "p_value": round(p, 4),
            "comb_detected": detected, "omega": OMEGA}
