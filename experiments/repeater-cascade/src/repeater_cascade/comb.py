"""RC.02 -- the frozen log-periodic comb (omega = 2.583) in ln(t - t_onset).

The discriminating dynamic TFPT signature (GW Stage-2 result): a repeating
source relaxing through the geometric mode ladder does not fire as a smooth
point process but with a log-periodic rate ripple

    R(tau) = R_smooth(tau) * (1 + eps * cos(omega ln tau + phi)),
    omega = 2*pi/ln((3/2)^6) = 2.583,  eps_pred = exp(-pi^2/ln lambda) ~ 1.7%.

Statistic: the Rayleigh power z(w) = |sum_i exp(i w ln tau_i)|^2 / n of the
burst phases.  The raw Rayleigh null is invalid here (the smooth session
envelope leaks into every w), so all inference is surrogate-calibrated:

  * rate-preserving surrogates: redraw the taus from the session's SMOOTH rate
    profile (a cubic log-density fit in ln tau: keeps the envelope + N,
    destroys any phase coherence at omega);
  * off-kernel periodogram rank: the surrogate-standardised score
    zeta(w) = (z_obs(w) - mean z_sur(w)) / std z_sur(w) at the kernel omega,
    ranked against a grid of off-kernel log-frequencies;
  * off-kernel lambda battery (Bonferroni): omega must be the smallest-p member.

Gates (preregistered, enforced per session): reach > 2.8 comb periods in
ln(tau); tau >= 30x the dataset time resolution; n_used >= 30.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.stats import ks_2samp

from .constants import OMEGA, REACH_GATE_PERIODS
from .sessions import Session

MIN_BURSTS_USED = 30
N_SURROGATE = 200
N_FREQ = 150
FREQ_LO, FREQ_HI = 0.9, 6.5
# The three "Z2" members (2026-07-06) are the Moebius/double-cover READINGS of the same kernel
# (exploratory/unforced, mirroring recovery-comb-domains Z2_LAMBDAS): an antiperiodic
# (sheet-parity) comb has ZERO power at the kernel omega -- fundamental at omega/2 <-> (3/2)^12,
# first odd harmonic at 3*omega/2 <-> (3/2)^4; a half-period clock sits at 2*omega <-> (3/2)^3.
LAMBDA_BATTERY = {
    "(3/2)^6 [kernel]": 1.5**6,
    "(3/2)^5": 1.5**5, "(3/2)^7": 1.5**7, "(3/2)^8": 1.5**8,
    "lambda=2": 2.0, "lambda=3": 3.0, "lambda=e": float(np.e),
    "(3/2)^3 [Z2 half-period]": 1.5**3,
    "(3/2)^4 [Z2 antiperiodic harmonic]": 1.5**4,
    "(3/2)^12 [Z2 antiperiodic fundamental]": 1.5**12,
}


def rayleigh_z(u: np.ndarray, w: np.ndarray | float) -> np.ndarray:
    """Rayleigh power z(w) = |sum exp(i w u)|^2 / n for one or many frequencies."""
    w_arr = np.atleast_1d(np.asarray(w, dtype=float))
    ph = np.exp(1j * np.outer(w_arr, u))
    z = np.abs(ph.sum(axis=1)) ** 2 / len(u)
    return z if np.ndim(w) else float(z[0])


SURROGATE_POLY_DEG = 3            # smooth log-density fit; cannot follow >~1 comb cycle
SURROGATE_BINS = 32


def surrogate_lntau(u: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Rate-preserving surrogate (the preregistered construction): draw the same
    number of ln(tau) values from the session's SMOOTH rate profile.

    The profile is a degree-3 polynomial fit to the log binned density of the
    observed ln(tau) -- smooth enough to keep the true envelope (incl. its
    slope, whose spectral leakage at omega the piecewise-flat alternative
    misses) but far too stiff to follow the >~3 oscillation cycles of a genuine
    kernel comb, so any phase coherence at omega is erased.  Hard session-window
    edges are preserved exactly."""
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


@dataclass
class CombSessionResult:
    dataset_id: str
    source: str
    t0_mjd: float
    n_used: int
    reach_periods: float
    gate_passed: bool
    z_omega: float = float("nan")
    p_surrogate: float = float("nan")     # P(z_sur >= z_obs) at omega
    p_rank: float = float("nan")          # off-kernel periodogram rank of zeta(omega)
    ks_p: float = float("nan")            # two-sample KS phases vs pooled surrogate phases
    battery: list[tuple[str, float, float]] = field(default_factory=list)
    kernel_smallest_p: bool = False


def comb_test_session(sess: Session, *, n_surrogate: int = N_SURROGATE,
                      seed: int = 0) -> CombSessionResult:
    reach = sess.reach_periods
    gate = bool(reach > REACH_GATE_PERIODS and sess.n_used >= MIN_BURSTS_USED)
    res = CombSessionResult(sess.dataset_id, sess.source, sess.t0_mjd,
                            sess.n_used, reach, gate)
    if not gate:
        return res
    rng = np.random.default_rng(seed + int(sess.t0_mjd))
    u = np.log(sess.tau_s)
    freqs = np.linspace(FREQ_LO, FREQ_HI, N_FREQ)
    freqs = freqs[np.abs(freqs - OMEGA) > 0.1 * OMEGA]
    all_w = np.concatenate([[OMEGA], freqs])

    z_obs = rayleigh_z(u, all_w)
    z_sur = np.empty((n_surrogate, len(all_w)))
    pooled_phases = []
    for k in range(n_surrogate):
        us = surrogate_lntau(u, rng)
        z_sur[k] = rayleigh_z(us, all_w)
        if k < 20:
            pooled_phases.append(np.mod(OMEGA * us, 2 * np.pi))
    mu, sd = z_sur.mean(axis=0), z_sur.std(axis=0) + 1e-12
    zeta = (z_obs - mu) / sd

    res.z_omega = float(z_obs[0])
    res.p_surrogate = float((1 + np.sum(z_sur[:, 0] >= z_obs[0])) / (n_surrogate + 1))
    res.p_rank = float((1 + np.sum(zeta[1:] >= zeta[0])) / (len(zeta)))
    res.ks_p = float(ks_2samp(np.mod(OMEGA * u, 2 * np.pi),
                              np.concatenate(pooled_phases)).pvalue)

    battery = []
    for label, lam in LAMBDA_BATTERY.items():
        w = 2.0 * np.pi / np.log(lam)
        zb = rayleigh_z(u, w)
        sb = np.array([rayleigh_z(surrogate_lntau(u, rng), w) for _ in range(60)])
        battery.append((label, float(w),
                        float((1 + np.sum(sb >= zb)) / 61)))
    res.battery = battery
    kernel_p = battery[0][2]
    res.kernel_smallest_p = bool(kernel_p <= min(p for _, _, p in battery))
    return res


def fisher_combine(pvals: list[float]) -> float:
    """Fisher's method over per-session surrogate p-values (guarded for the
    discrete floor p >= 1/(n_sur+1))."""
    from scipy.stats import chi2

    p = np.clip(np.asarray(pvals, dtype=float), 1.0 / (N_SURROGATE + 1), 1.0)
    if len(p) == 0:
        return float("nan")
    stat = -2.0 * np.sum(np.log(p))
    return float(chi2.sf(stat, df=2 * len(p)))


def benjamini_hochberg(pvals: dict[str, float]) -> dict[str, float]:
    """BH q-values across sources."""
    items = [(k, v) for k, v in pvals.items() if np.isfinite(v)]
    items.sort(key=lambda kv: kv[1])
    m = len(items)
    q: dict[str, float] = {}
    prev = 1.0
    for rank in range(m, 0, -1):
        k, p = items[rank - 1]
        val = min(prev, p * m / rank)
        q[k] = val
        prev = val
    return q
