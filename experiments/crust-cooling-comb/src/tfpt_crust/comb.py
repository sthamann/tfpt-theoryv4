"""The shared, injection-validated log-periodic recovery-comb detector (self-contained port).

Ported verbatim (kernel logic UNCHANGED) from
``experiments/recovery-comb-domains/src/tfpt_combdomains/comb.py`` and ``quake.py`` so this
experiment stays self-contained. The "new" TFPT signature is not a number but a SHAPE: a system
relaxing to a fixed point through the frozen geometric mode ladder leaves a log-periodic
(discrete-scale-invariance) comb on its recovery curve,

    R(t) = (power law) * (1 + eps cos(omega ln t + phi)),
    omega = 2 pi / ln(lambda),  lambda = (3/2)^6,  -> omega = 2.583,
    eps  ~ exp(-pi^2 / ln lambda) ~ 0.017   (the QT.02 amplitude-suppression law).

Everything is DERIVED from the two axioms (c3 = 1/(8 pi), g_car = 5); NO neutron-star number enters.
The detector asks whether the comb at the KERNEL omega is SPECIAL in a recovery curve, by ranking
the comb gain at omega against a periodogram of off-kernel log-frequencies (a degree-2
polynomial-in-ln(t) baseline absorbs the smooth exponential-to-floor cooling trend, so a pure
smooth decay is NOT flagged). It fires on a geometric-ladder comb and not on a smooth decay, and
ONLY when the curve spans >~2.8 comb periods in ln(t) (the hard ln-range requirement that no amount
of stacking can relax).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# --- frozen kernel (from the two axioms; identical to recovery-comb-domains / pulsar-glitch) ---
N_FAM = 3
P2 = 6
LAMBDA = 1.5 ** P2                        # (3/2)^6 = 11.39, the cascade scale
OMEGA = 2.0 * math.pi / math.log(LAMBDA)  # 2.583, the comb log-frequency
EPS_PREDICTED = math.exp(-math.pi ** 2 / math.log(LAMBDA))  # ~0.017, QT.02 suppression law
MIN_COMB_PERIODS = 2.8                    # ln(tau) range needed to localise omega (machine-checked)
DETREND_DEG = 2
P_THRESHOLD = 0.05

PHI = 0.5 * (1.0 + math.sqrt(5.0))
# The full TFPT log-period battery: lambda (the discrete-scale-invariance ratio) -> omega.
# The single (3/2)^6 kernel is the DISCRIMINATING signature; the small-lambda entries are dense
# among any scaling story (low complexity) and serve as the look-elsewhere control.
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
IDIO = {"3/2 (1/Koide, fundamental)", "phi (golden, g_car=5)", "(3/2)^6 (recovery comb)"}
# The Z2/Moebius double-cover READINGS of the same kernel (2026-07-06, exploratory/unforced;
# mirrors recovery-comb-domains quake.Z2_LAMBDAS): an antiperiodic (sheet-parity) comb has zero
# power at the kernel omega -- fundamental at omega/2 <-> (3/2)^12, first odd harmonic at
# 3*omega/2 <-> (3/2)^4; a half-period (sqrt-lambda per rung) clock sits at 2*omega <-> (3/2)^3.
Z2_LAMBDAS: dict[str, float] = {
    "(3/2)^3 (Z2 half-period)": 1.5 ** 3,
    "(3/2)^4 (Z2 antiperiodic harmonic)": 1.5 ** 4,
    "(3/2)^12 (Z2 antiperiodic fundamental)": 1.5 ** 12,
}
BATTERY_LAMBDAS: dict[str, float] = {**TFPT_LAMBDAS, **Z2_LAMBDAS}
BATTERY_IDIO = IDIO | set(Z2_LAMBDAS)


def _omega(lam: float) -> float:
    return 2.0 * math.pi / math.log(lam)


def _comb_gain(lt: np.ndarray, y: np.ndarray, omega: float, deg: int = DETREND_DEG) -> float:
    """Fractional variance explained by cos/sin(omega ln t) over a degree-`deg` poly-in-ln(t)
    baseline (which absorbs the smooth exponential-to-floor cooling trend)."""
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
    rank). A smooth cooling recovery -> p ~ 0.5; a genuine geometric-ladder comb -> p << 0.05."""
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


def comb_periods(t: np.ndarray, *, lam: float = LAMBDA) -> float:
    """Number of comb periods the curve spans in ln(t) = ln(t_max/t_min)/ln(lambda)."""
    t = np.asarray(t)
    t = t[t > 0]
    return float(np.log(t.max() / t.min()) / math.log(lam)) if len(t) > 1 else 0.0


def run_comb(t: np.ndarray, rec: np.ndarray, *, seed: int = 0) -> dict:
    """Apply the detector to a real recovery curve and report with the ln-range gate."""
    periods = comb_periods(t)
    gain, p = detect_comb(t, rec, seed=seed)
    enough = periods >= MIN_COMB_PERIODS
    detected = bool(p < P_THRESHOLD and enough)
    return {"n_points": int(len(t)), "comb_periods": round(periods, 2),
            "range_sufficient": enough, "gain": round(gain, 4), "p_value": round(p, 4),
            "comb_detected": detected, "omega": OMEGA}


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


# --------------------------------------------------------------------------- stacked meta-test
def _prepare(curves: list[tuple[np.ndarray, np.ndarray]]) -> list[tuple[np.ndarray, np.ndarray]]:
    """Keep only curves that individually clear the hard ln-range gate (>= MIN_COMB_PERIODS).
    Stacking raises amplitude SNR, never ln-range, so the gate stays PER CURVE (honest)."""
    out = []
    for t, rec in curves:
        t = np.asarray(t, float)
        rec = np.asarray(rec, float)
        m = t > 0
        if int(m.sum()) >= 6 and comb_periods(t[m]) >= MIN_COMB_PERIODS:
            out.append((t[m], rec[m]))
    return out


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
    off-kernel pool. Returns (p, gain)."""
    m = np.asarray(t) > 0
    lt, y = np.log(np.asarray(t)[m]), np.asarray(rec)[m]
    if len(lt) < 6:
        return 1.0, 0.0
    g0, pool = _matched_pool(lt, y, omega, np.random.default_rng(seed), n_pool)
    return float((1 + np.sum(pool >= g0)) / (len(pool) + 1)), g0


def stacked_comb_test(curves: list[tuple[np.ndarray, np.ndarray]], *, omega: float = OMEGA,
                      n_draws: int = 4000, n_pool: int = 160, seed: int = 0) -> dict:
    """Phase-incoherent stack of the kernel comb gain across many recovery curves with a
    PERMUTATION null (the same statistic as recovery-comb-domains). The TFPT comb sits at the SAME
    kernel omega in every relaxation (fixed by the axioms) with a source-dependent phase; per-curve
    comb gains are phase-insensitive, so they add. The hard per-curve ln-range gate (``_prepare``)
    stays -- stacking beats the intrinsic ~2% amplitude but NEVER buys ln-range."""
    prepared = _prepare(curves)
    k = len(prepared)
    if k == 0:
        return {"n_used": 0, "n_total": len(curves), "gain": 0.0, "p_value": 1.0,
                "comb_detected": False, "omega": omega, "ps": []}
    rng = np.random.default_rng(seed)
    g_om, pools, ps = [], [], []
    for t, rec in prepared:
        g0, pool = _matched_pool(np.log(t), rec, omega, rng, n_pool)
        g_om.append(g0)
        pools.append(pool)
        ps.append(float((1 + np.sum(pool >= g0)) / (len(pool) + 1)))
    s_obs = float(sum(g_om))
    draws = np.zeros(n_draws)
    for pool in pools:
        draws += rng.choice(pool, size=n_draws)
    p_comb = float((1 + np.sum(draws >= s_obs)) / (n_draws + 1))
    return {"n_used": k, "n_total": len(curves), "gain": round(float(np.mean(g_om)), 4),
            "p_value": round(p_comb, 4), "comb_detected": bool(p_comb < P_THRESHOLD),
            "omega": omega, "ps": [round(p, 4) for p in ps]}


def _stacked_at(curves: list[tuple[np.ndarray, np.ndarray]], omega: float, *,
                n_draws: int = 4000, n_pool: int = 160, seed: int = 0) -> dict:
    """Stacked permutation comb test at an ARBITRARY omega, with a PER-omega gate: each curve must
    span >= MIN_COMB_PERIODS cycles of THIS omega and sample it below Nyquist. Small-lambda entries
    (large omega) need LESS ln-range, so they are testable where the (3/2)^6 kernel is range-blind
    -- exactly the recovery-comb-domains quake/A5 look-elsewhere pattern."""
    lam = math.exp(2.0 * math.pi / omega)
    prepared = []
    for t, y in curves:
        lt = np.log(np.asarray(t, float))
        yy = np.asarray(y, float)
        if len(lt) < 6:
            continue
        periods = (lt.max() - lt.min()) / math.log(lam)
        dln = float(np.median(np.diff(np.sort(lt))))
        nyq = math.pi / dln if dln > 0 else math.inf
        if periods >= MIN_COMB_PERIODS and omega <= nyq:
            prepared.append((lt, yy))
    k = len(prepared)
    if k == 0:
        return {"n_used": 0, "gain": 0.0, "p_value": 1.0, "comb_detected": False}
    rng = np.random.default_rng(seed)
    g_om, pools = [], []
    for lt, yy in prepared:
        g0, pool = _matched_pool(lt, yy, omega, rng, n_pool)
        g_om.append(g0)
        pools.append(pool)
    s_obs = float(sum(g_om))
    draws = np.zeros(n_draws)
    for pool in pools:
        draws += rng.choice(pool, size=n_draws)
    p = float((1 + np.sum(draws >= s_obs)) / (n_draws + 1))
    return {"n_used": k, "gain": round(float(np.mean(g_om)), 4), "p_value": round(p, 4),
            "comb_detected": bool(p < P_THRESHOLD)}


def _make_log_curve(periods: float, eps: float, noise: float, rng: np.random.Generator,
                    alpha: float = 0.5, n_pts: int = 60) -> tuple[np.ndarray, np.ndarray]:
    """A synthetic recovery curve flux=t^-alpha (1+eps cos(omega ln t + phi)); returns
    (t, ln flux + noise)."""
    tmax = math.exp(periods * math.log(LAMBDA))
    t = np.logspace(0.0, math.log10(tmax), n_pts)
    phi = rng.uniform(0.0, 2.0 * math.pi)
    flux = t ** (-alpha) * (1.0 + eps * np.cos(OMEGA * np.log(t) + phi))
    return t, np.log(flux) + rng.normal(0.0, noise, n_pts)


@dataclass
class StackValidation:
    eps: float
    noise: float
    n_curves: int
    periods: float
    single_rate: float    # one ~3-period curve at this faint eps -> usually MISSED
    stacked_rate: float   # the stack of n_curves -> recovered (the sharpening)
    null_rate: float      # n_curves with NO comb -> false-positive, must be ~0
    passed: bool


def validate_stack(*, eps: float = 0.05, noise: float = 0.10, n_curves: int = 12,
                   periods: float = 3.0, n_seeds: int = 20) -> StackValidation:
    """Prove the phase-incoherent stack recovers a faint (eps=5%) common comb that a single curve
    misses, while staying null on comb-free data (the operational meaning of 'sharp')."""
    single = stack = nul = 0
    for s in range(n_seeds):
        rng = np.random.default_rng(1000 + s)
        curves = [_make_log_curve(periods, eps, noise, rng) for _ in range(n_curves)]
        p1, _ = kernel_pvalue(*curves[0], seed=s)
        single += int(p1 < P_THRESHOLD)
        stack += int(stacked_comb_test(curves, seed=s)["comb_detected"])
        nul += int(stacked_comb_test([_make_log_curve(periods, 0.0, noise, rng)
                                      for _ in range(n_curves)], seed=100 + s)["comb_detected"])
    single_rate, stacked_rate, null_rate = single / n_seeds, stack / n_seeds, nul / n_seeds
    passed = bool(stacked_rate >= 0.70 and stacked_rate >= single_rate + 0.20
                  and null_rate <= 0.15)
    return StackValidation(eps, noise, n_curves, periods, single_rate, stacked_rate,
                           null_rate, passed)
