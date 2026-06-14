"""C_E -- the energy-cascade (discreteness / log-periodicity) test.

This is the decisive TFPT test of ``problem_b.txt`` section 1: a phi-attractor
cascade ``Delta E_n ~ E_0 gamma(n)`` should make a single source's burst
energies **cluster into discrete, log-periodically spaced families**, whereas
the standard magnetar picture predicts a smooth (power-law / log-normal)
continuum.

Three orthogonal probes, all calibrated against the smooth null:

1. ``lognormal_baseline``  -- fit the boring continuum (the null hypothesis).
2. ``gmm_multimodality``   -- is a mixture of >1 log-Gaussian preferred (BIC)?
3. ``log_periodicity``     -- a Rayleigh test for equal log-spacing, with the
   p-value calibrated by smooth-null surrogates so the frequency scan is honest.

If a log-periodic spacing is found, its ratio is matched against the
TFPT-natural ``candidate_ratios`` (carrier 3/2, transfer gap, E8 cascade mean).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats
from sklearn.mixture import GaussianMixture

from .tfpt_ladder import RatioTarget, candidate_ratios


def _clean_log10(fluence: np.ndarray) -> np.ndarray:
    e = np.asarray(fluence, dtype=float)
    e = e[np.isfinite(e) & (e > 0)]
    return np.log10(e)


@dataclass
class LogNormalFit:
    n: int
    mu: float
    sigma: float
    ks_stat: float
    ks_pvalue: float  # high p => data consistent with a smooth log-normal continuum


def lognormal_baseline(fluence: np.ndarray) -> LogNormalFit:
    """Fit the smooth-continuum null (log-normal in energy) and KS-test it."""
    x = _clean_log10(fluence)
    mu, sigma = float(np.mean(x)), float(np.std(x, ddof=1))
    ks = stats.kstest(x, "norm", args=(mu, sigma))
    return LogNormalFit(len(x), mu, sigma, float(ks.statistic), float(ks.pvalue))


@dataclass
class GMMResult:
    best_k: int
    delta_bic: float          # BIC(k=1) - BIC(best_k); >0 favours multimodal
    weights: list[float]
    means_log10: list[float]


def gmm_multimodality(fluence: np.ndarray, max_k: int = 5, seed: int = 0) -> GMMResult:
    """BIC scan of Gaussian mixtures in log-energy (k = 1..max_k)."""
    x = _clean_log10(fluence).reshape(-1, 1)
    max_k = min(max_k, max(1, len(x) // 10))
    bics, models = [], []
    for k in range(1, max_k + 1):
        gm = GaussianMixture(n_components=k, covariance_type="full",
                             n_init=4, random_state=seed).fit(x)
        bics.append(gm.bic(x))
        models.append(gm)
    bics = np.array(bics)
    best = int(np.argmin(bics))
    gm = models[best]
    order = np.argsort(gm.means_.ravel())
    return GMMResult(
        best_k=best + 1,
        delta_bic=float(bics[0] - bics[best]),
        weights=[float(gm.weights_[i]) for i in order],
        means_log10=[float(gm.means_.ravel()[i]) for i in order],
    )


def _rayleigh_logperiodic(x: np.ndarray, freqs: np.ndarray) -> np.ndarray:
    """Rayleigh statistic z(f) = N * |<exp(2 pi i f x)>|^2 on the log-energy axis.

    ``x`` are log10(energy); ``freqs`` are in cycles per dex.  A pile-up of
    energies at spacing ratio r = 10^(1/f) makes the phases align -> large z.
    Under a smooth null the phases are diffuse -> small z.
    """
    n = len(x)
    phase = 2.0 * np.pi * np.outer(freqs, x)          # (F, N)
    c = np.cos(phase).mean(axis=1)
    s = np.sin(phase).mean(axis=1)
    return n * (c * c + s * s)


@dataclass
class LogPeriodicResult:
    n: int
    best_ratio: float          # 10^(1/f*)
    best_freq: float           # cycles per dex
    z_max: float               # Rayleigh power at f*
    p_value: float             # surrogate-calibrated (accounts for the scan)
    nearest: RatioTarget | None
    nearest_rel_err: float     # |ratio-target|/target of the closest TFPT ratio


def log_periodicity(
    fluence: np.ndarray,
    ratio_lo: float = 1.3,
    ratio_hi: float = 6.0,
    n_freq: int = 400,
    n_surrogate: int = 400,
    seed: int = 0,
) -> LogPeriodicResult:
    """Search for equal log-spacing and calibrate the detection with surrogates.

    The p-value is the fraction of smooth-null (log-normal) surrogates whose
    *scan-maximum* Rayleigh power exceeds the observed one, so it already pays
    the multiple-frequency penalty.  Small p => significant log-periodicity.
    """
    x = _clean_log10(fluence)
    n = len(x)
    # frequency grid in cycles/dex spans the requested spacing-ratio window
    f_lo, f_hi = 1.0 / np.log10(ratio_hi), 1.0 / np.log10(ratio_lo)
    freqs = np.linspace(f_lo, f_hi, n_freq)

    z = _rayleigh_logperiodic(x, freqs)
    k = int(np.argmax(z))
    z_max, f_star = float(z[k]), float(freqs[k])
    best_ratio = float(10.0 ** (1.0 / f_star))

    rng = np.random.default_rng(seed)
    mu, sigma = float(np.mean(x)), float(np.std(x, ddof=1))
    null_max = np.empty(n_surrogate)
    for i in range(n_surrogate):
        xs = rng.normal(mu, sigma, size=n)
        null_max[i] = _rayleigh_logperiodic(xs, freqs).max()
    p_value = float((1 + np.sum(null_max >= z_max)) / (n_surrogate + 1))

    nearest, rel = None, np.inf
    for t in candidate_ratios():
        r = abs(best_ratio - t.value) / t.value
        if r < rel:
            nearest, rel = t, r
    return LogPeriodicResult(n, best_ratio, f_star, z_max, p_value, nearest, float(rel))


@dataclass
class SpacingLadderResult:
    n: int
    best_k: int
    centers_log10: list[float]
    adjacent_spacings_dex: list[float]
    best_candidate: str | None
    best_candidate_dex: float
    match_rel_err: float          # worst adjacent-spacing rel-err to the best candidate
    p_value: float                # surrogate-calibrated (>=3 clusters with matching ladder)
    c_ladder: float
    verdict: str


# preregistered candidate spacings (energy ratio between adjacent families).
# Kernel ratios are primary; (3/2),(2),(5/3) are AUDIT ratios only (flagged).
def _candidate_spacings() -> dict[str, float]:
    return {
        "(3/2)^6=729/64": np.log10(729 / 64),    # kernel energy
        "(3/2)^3=27/8": np.log10(27 / 8),        # kernel field root
        "3/2[audit]": np.log10(3 / 2),
        "2[audit]": np.log10(2.0),
        "5/3[audit]": np.log10(5 / 3),
    }


def fit_spacing_ladder(fluence: np.ndarray, tol: float = 0.10, max_k: int = 6,
                       n_surrogate: int = 150, seed: int = 0) -> SpacingLadderResult:
    """Fit a GMM, and if >=3 clusters are preferred, test whether the adjacent
    log-energy spacings match a single preregistered ratio (surrogate-calibrated)."""
    x = _clean_log10(fluence)
    n = len(x)
    gm = gmm_multimodality(fluence, max_k=max_k, seed=seed)
    centers = np.array(sorted(gm.means_log10))
    if gm.best_k < 3:
        return SpacingLadderResult(n, gm.best_k, centers.tolist(), [], None, float("nan"),
                                   float("nan"), 1.0, 0.0,
                                   f"no cascade: best_k={gm.best_k} (<3 clusters)")
    spac = np.diff(centers)
    cands = _candidate_spacings()
    best_name, best_rel = None, np.inf
    for name, c in cands.items():
        rel = float(np.max(np.abs(spac - c) / c))
        if rel < best_rel:
            best_name, best_rel = name, rel

    rng = np.random.default_rng(seed)
    mu, sigma = float(np.mean(x)), float(np.std(x, ddof=1))
    hits = 0
    for _ in range(n_surrogate):
        xs = rng.normal(mu, sigma, n)
        g = gmm_multimodality(10.0 ** xs, max_k=max_k, seed=seed)
        if g.best_k < 3:
            continue
        sp = np.diff(np.array(sorted(g.means_log10)))
        if any(np.max(np.abs(sp - c) / c) <= tol for c in cands.values()):
            hits += 1
    p = float((1 + hits) / (n_surrogate + 1))
    matched = best_rel <= tol
    c_ladder = float(np.clip((matched and p < 0.05) * (1 - p / 0.05), 0, 1))
    verdict = (f"cascade ladder ~ {best_name} (worst {100*best_rel:.0f}%, p={p:.3f})"
               if matched else f"{gm.best_k} clusters but no uniform kernel spacing "
               f"(closest {best_name} at {100*best_rel:.0f}%)")
    return SpacingLadderResult(n, gm.best_k, centers.tolist(), spac.tolist(),
                               best_name, cands[best_name], best_rel, p, c_ladder, verdict)


def periodogram_curve(fluence: np.ndarray, ratio_lo: float = 1.3, ratio_hi: float = 6.0,
                      n_freq: int = 400, n_surrogate: int = 400, seed: int = 0):
    """Return (ratios, z, z95) for plotting the log-periodogram.

    ``ratios`` are spacing ratios (x-axis), ``z`` the Rayleigh power, ``z95`` the
    95th-percentile scan-maximum of smooth-null surrogates (the detection bar).
    """
    x = _clean_log10(fluence)
    f_lo, f_hi = 1.0 / np.log10(ratio_hi), 1.0 / np.log10(ratio_lo)
    freqs = np.linspace(f_lo, f_hi, n_freq)
    z = _rayleigh_logperiodic(x, freqs)
    ratios = 10.0 ** (1.0 / freqs)
    rng = np.random.default_rng(seed)
    mu, sigma = float(np.mean(x)), float(np.std(x, ddof=1))
    null_max = np.array([_rayleigh_logperiodic(rng.normal(mu, sigma, len(x)), freqs).max()
                         for _ in range(n_surrogate)])
    return ratios, z, float(np.percentile(null_max, 95))


@dataclass
class EnergyClusterReport:
    source: str
    lognormal: LogNormalFit
    gmm: GMMResult
    logperiodic: LogPeriodicResult
    c_e: float                 # combined TFPT energy-cascade score in [0, 1]
    verdict: str


def energy_cluster_score(source: str, fluence: np.ndarray, *,
                         alpha: float = 0.05, seed: int = 0) -> EnergyClusterReport:
    """Combine the three probes into C_E and a plain-language verdict."""
    ln = lognormal_baseline(fluence)
    gm = gmm_multimodality(fluence, seed=seed)
    lp = log_periodicity(fluence, seed=seed)

    s_multi = 1.0 / (1.0 + np.exp(-(gm.delta_bic - 6.0) / 3.0))   # ~0 below dBIC 6
    s_period = float(np.clip(1.0 - lp.p_value / alpha, 0.0, 1.0)) # 1 when p<<alpha
    s_ratio = float(np.exp(-(lp.nearest_rel_err / 0.05) ** 2))    # match within ~5%
    # the ratio only counts as corroboration if the periodicity itself is real
    c_e = float(np.clip(0.5 * s_multi + 0.5 * s_period * (0.5 + 0.5 * s_ratio), 0, 1))

    if lp.p_value < alpha and gm.best_k > 1 and gm.delta_bic > 6:
        verdict = (f"discrete log-periodic cascade (p={lp.p_value:.3f}, "
                   f"ratio {lp.best_ratio:.2f}~{lp.nearest.name} "
                   f"@ {100 * lp.nearest_rel_err:.0f}%)")
    elif lp.p_value < alpha:
        verdict = (f"marginal log-periodicity (p={lp.p_value:.3f}, "
                   f"ratio {lp.best_ratio:.2f}) but not strongly multimodal "
                   f"(dBIC={gm.delta_bic:.1f}); treat as tentative")
    elif gm.best_k > 1 and gm.delta_bic > 6:
        verdict = f"multimodal but not equal-spaced (best_k={gm.best_k})"
    else:
        verdict = "smooth continuum; no TFPT cascade signature"
    return EnergyClusterReport(source, ln, gm, lp, c_e, verdict)
