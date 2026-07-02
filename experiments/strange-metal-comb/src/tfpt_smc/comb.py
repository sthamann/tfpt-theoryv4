"""The shared, injection-validated log-periodic recovery-comb detector (self-contained port).

Ported verbatim (kernel logic UNCHANGED) from
``experiments/recovery-comb-domains/src/tfpt_combdomains/comb.py`` (detector) and ``quake.py``
(lambda-battery constants) so this experiment stays self-contained; guarded bit-for-bit by
``tests/test_frozen_kernel.py``. The "new" TFPT signature is not a number but a SHAPE: a system
relaxing to a fixed point through the frozen geometric mode ladder leaves a log-periodic
(discrete-scale-invariance) comb,

    (smooth curve) * (1 + eps cos(omega * u + phi)),
    omega = 2 pi / ln(lambda),  lambda = (3/2)^6,  -> omega = 2.583,
    eps  ~ exp(-pi^2 / ln lambda) ~ 0.017   (the QT.02 amplitude-suppression law).

Everything is DERIVED from the two axioms (c3 = 1/(8 pi), g_car = 5); no condensed-matter number
enters. Here the log-variable u is ln(hbar*omega_opt / k_B T) -- the master-curve scaling variable
-- instead of ln(t); the detector is variable-agnostic (it sees only ``lt = ln(x)``), so nothing
in the kernel changes.

FIREWALL: strange metals have NO established boundary-recovery structure; a hit would be a
universal-DSI coincidence, NEVER TFPT confirmation. A null is expected and informative.
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
MIN_COMB_PERIODS = 2.8                   # ln range needed to localise omega (machine-checked)
DETREND_DEG = 2
P_THRESHOLD = 0.05

PHI = 0.5 * (1.0 + math.sqrt(5.0))
# TFPT log-period battery: lambda (the discrete-scale-invariance ratio) -> omega = 2 pi / ln lambda.
TFPT_LAMBDAS: dict[str, float] = {
    "3/2 (1/Koide, fundamental)": 1.5,
    "phi (golden, g_car=5)": PHI,
    "2 (sheet doubling)": 2.0,
    "3 (N_fam)": 3.0,
    "4 (|mu4|)": 4.0,
    "5 (g_car)": 5.0,
    "8 (rank E8)": 8.0,
    "(3/2)^6 (recovery comb)": 1.5 ** 6,
    "30 (Coxeter h)": 30.0,
}
# the structurally "deep" (idiosyncratic) TFPT ratios -- a hit here would matter more than the
# low-complexity atoms {2,3,4,5,8}, which are dense among any scaling story.
IDIO = {"3/2 (1/Koide, fundamental)", "phi (golden, g_car=5)", "(3/2)^6 (recovery comb)"}


def _omega(lam: float) -> float:
    return 2.0 * math.pi / math.log(lam)


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


# --------------------------------------------------------------------------- matched-pool p-value
def _matched_pool(lt: np.ndarray, y: np.ndarray, omega: float, rng: np.random.Generator,
                  n_pool: int = 160) -> tuple[float, np.ndarray]:
    """Comb gain at the kernel and a pool of gains at neighbouring off-kernel log-frequencies in a
    NARROW band [0.72,1.40]*omega that shares the kernel's gain regime under the null. Under H0
    (no comb) omega is exchangeable with this pool, which is what makes the permutation test exact."""
    g0 = _comb_gain(lt, y, omega)
    fs = rng.uniform(0.72 * omega, 1.40 * omega, n_pool)
    fs = fs[np.abs(fs - omega) > 0.06 * omega]
    return g0, np.array([_comb_gain(lt, y, f) for f in fs])


def kernel_pvalue(t: np.ndarray, rec: np.ndarray, *, omega: float = OMEGA, n_pool: int = 160,
                  seed: int = 0) -> tuple[float, float]:
    """Single-curve kernel test: permutation p = rank of the comb gain at omega within its matched
    off-kernel pool. Returns (p, gain). Coarse for a single short curve (few independent
    frequencies) -- the stack is what sharpens it."""
    m = np.asarray(t) > 0
    lt, y = np.log(np.asarray(t)[m]), np.asarray(rec)[m]
    if len(lt) < 6:
        return 1.0, 0.0
    g0, pool = _matched_pool(lt, y, omega, np.random.default_rng(seed), n_pool)
    return float((1 + np.sum(pool >= g0)) / (len(pool) + 1)), g0
