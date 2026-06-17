"""PG.01 -- discreteness / log-periodicity of glitch sizes ``Delta nu / nu``.

The pulsar analogue of the FRB energy-cascade test (``frb_tfpt.energy_clusters``):
a phi-attractor / recovery cascade would make glitch sizes pile up into discrete,
*log-periodically* spaced families, whereas the standard two-population starquake /
superfluid picture predicts a smooth (broad, bimodal but comb-free) continuum.

Honesty about the known bimodality of glitch sizes (large Vela-type vs small
Crab-type) is built in: the log-periodicity p-value is calibrated against **two**
smooth nulls and the *more conservative* (larger) p is reported --

1. ``lognormal``  -- a single log-normal continuum (guards "any structure beyond
   unimodal smooth");
2. ``kde``        -- a shape-preserving smooth bootstrap (Gaussian-KDE resample,
   widened bandwidth) that *keeps* the real broad/bimodal shape and only destroys
   a fine log-periodic comb (guards "comb beyond the actual smooth shape").

A detection therefore has to beat the real, bimodal size distribution -- not just
a convenient unimodal straw man.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats

from .constants import RatioTarget, candidate_size_ratios


def _clean_log10(sizes: np.ndarray) -> np.ndarray:
    s = np.asarray(sizes, dtype=float)
    s = s[np.isfinite(s) & (s > 0)]
    return np.log10(s)


def _rayleigh_logperiodic(x: np.ndarray, freqs: np.ndarray) -> np.ndarray:
    """Rayleigh power ``z(f) = N |<exp(2 pi i f x)>|^2`` on the log-size axis.

    A pile-up at spacing ratio ``r = 10^(1/f)`` aligns the phases -> large z.
    """
    n = len(x)
    phase = 2.0 * np.pi * np.outer(freqs, x)
    c = np.cos(phase).mean(axis=1)
    s = np.sin(phase).mean(axis=1)
    return n * (c * c + s * s)


def _lognormal_surrogate(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    mu, sigma = float(np.mean(x)), float(np.std(x, ddof=1))
    return rng.normal(mu, sigma, size=len(x))


def _kde_surrogate(x: np.ndarray, rng: np.random.Generator,
                   bw_inflate: float = 1.3) -> np.ndarray:
    """Shape-preserving smooth bootstrap: resample from a (widened) Gaussian KDE.

    The widened bandwidth makes the null *conservative* -- it keeps the broad /
    bimodal shape of the real distribution while erasing any fine comb, so a
    detection must exceed structure already present in the smooth density.
    """
    kde = stats.gaussian_kde(x, bw_method="silverman")
    kde.set_bandwidth(kde.factor * bw_inflate)
    return kde.resample(len(x), seed=rng).ravel()


def _gmm_surrogate(params: tuple[np.ndarray, np.ndarray, np.ndarray], n: int,
                   rng: np.random.Generator) -> np.ndarray:
    """Parametric bootstrap from the BIC-selected Gaussian mixture.

    This is the *population-controlled* null: it reproduces the known broad,
    multi-population (Vela-type vs Crab-type) glitch-size structure exactly, so
    only a genuine finer log-periodic comb -- not the astrophysical bimodality --
    can beat it.  This is the primary, most conservative null for PG.01.
    """
    means, variances, weights = params
    comp = rng.choice(len(weights), size=n, p=weights / weights.sum())
    return means[comp] + rng.normal(0.0, 1.0, size=n) * np.sqrt(variances[comp])


@dataclass
class LogNormalFit:
    n: int
    mu: float
    sigma: float
    ks_stat: float
    ks_pvalue: float        # high p => consistent with a smooth log-normal


def lognormal_baseline(sizes: np.ndarray) -> LogNormalFit:
    x = _clean_log10(sizes)
    mu, sigma = float(np.mean(x)), float(np.std(x, ddof=1))
    ks = stats.kstest(x, "norm", args=(mu, sigma))
    return LogNormalFit(len(x), mu, sigma, float(ks.statistic), float(ks.pvalue))


@dataclass
class GMMResult:
    best_k: int
    delta_bic: float        # BIC(k=1) - BIC(best_k); >0 favours multimodal
    weights: list[float]
    means_log10: list[float]


def _fit_gmm_1d(x: np.ndarray, k: int, seed: int, n_iter: int = 200,
                tol: float = 1e-6) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Tiny 1-D Gaussian-mixture EM (no sklearn dependency).

    Returns (means, variances, weights, log-likelihood).  Variances are floored
    to avoid singular collapse onto a single point.
    """
    rng = np.random.default_rng(seed)
    n = len(x)
    var_floor = max(1e-6, np.var(x) / 1e4)
    means = np.quantile(x, np.linspace(0.1, 0.9, k)) if k > 1 else np.array([x.mean()])
    means = means + rng.normal(0, 1e-3, size=k)
    variances = np.full(k, max(np.var(x), var_floor))
    weights = np.full(k, 1.0 / k)
    prev_ll = -np.inf
    for _ in range(n_iter):
        # E-step: responsibilities
        comp = (weights / np.sqrt(2 * np.pi * variances)
                * np.exp(-0.5 * (x[:, None] - means) ** 2 / variances))  # (n,k)
        tot = comp.sum(axis=1, keepdims=True)
        tot = np.where(tot <= 0, 1e-300, tot)
        resp = comp / tot
        ll = float(np.sum(np.log(tot)))
        # M-step
        nk = resp.sum(axis=0) + 1e-12
        weights = nk / n
        means = (resp * x[:, None]).sum(axis=0) / nk
        variances = np.maximum((resp * (x[:, None] - means) ** 2).sum(axis=0) / nk,
                               var_floor)
        if abs(ll - prev_ll) < tol * max(1.0, abs(prev_ll)):
            break
        prev_ll = ll
    return means, variances, weights, ll


def best_gmm_params(sizes: np.ndarray, max_k: int = 5,
                    seed: int = 0) -> tuple[np.ndarray, np.ndarray, np.ndarray, int, float]:
    """BIC scan; return (means, variances, weights, best_k, delta_bic) of the
    BIC-selected mixture -- the population-controlled null's parameters."""
    x = _clean_log10(sizes)
    n = len(x)
    max_k = min(max_k, max(1, n // 10))
    bics, fits = [], []
    for k in range(1, max_k + 1):
        means, variances, weights, ll = _fit_gmm_1d(x, k, seed)
        n_params = 3 * k - 1                      # means + variances + (k-1) weights
        bics.append(-2.0 * ll + n_params * np.log(n))
        fits.append((means, variances, weights))
    bics = np.array(bics)
    best = int(np.argmin(bics))
    means, variances, weights = fits[best]
    return means, variances, weights, best + 1, float(bics[0] - bics[best])


def gmm_multimodality(sizes: np.ndarray, max_k: int = 5, seed: int = 0) -> GMMResult:
    """BIC scan of 1-D Gaussian mixtures in log10(size); k=1..max_k."""
    means, variances, weights, best_k, delta_bic = best_gmm_params(sizes, max_k, seed)
    order = np.argsort(means)
    return GMMResult(best_k, delta_bic,
                     [float(weights[i]) for i in order],
                     [float(means[i]) for i in order])


@dataclass
class LogPeriodicResult:
    n: int
    best_ratio: float       # 10^(1/f*)
    best_freq: float        # cycles per dex
    z_max: float
    p_lognormal: float      # vs a single log-normal continuum
    p_kde: float            # vs a shape-preserving smooth (KDE) bootstrap
    p_gmm: float            # vs the population-controlled GMM bootstrap (primary)
    p_value: float          # max of the three -- the conservative report
    nearest: RatioTarget | None
    nearest_rel_err: float


def log_periodicity(sizes: np.ndarray, ratio_lo: float = 1.3, ratio_hi: float = 30.0,
                    n_freq: int = 500, n_surrogate: int = 600,
                    seed: int = 0) -> LogPeriodicResult:
    """Scan for equal log-spacing; the p-value already pays the frequency-scan
    penalty (it compares the *scan maximum* to the surrogate scan maxima)."""
    x = _clean_log10(sizes)
    n = len(x)
    f_lo, f_hi = 1.0 / np.log10(ratio_hi), 1.0 / np.log10(ratio_lo)
    freqs = np.linspace(f_lo, f_hi, n_freq)

    z = _rayleigh_logperiodic(x, freqs)
    k = int(np.argmax(z))
    z_max, f_star = float(z[k]), float(freqs[k])
    best_ratio = float(10.0 ** (1.0 / f_star))

    rng = np.random.default_rng(seed)
    gmm = best_gmm_params(sizes, seed=seed)[:3]
    null_ln = np.array([_rayleigh_logperiodic(_lognormal_surrogate(x, rng), freqs).max()
                        for _ in range(n_surrogate)])
    null_kde = np.array([_rayleigh_logperiodic(_kde_surrogate(x, rng), freqs).max()
                         for _ in range(n_surrogate)])
    null_gmm = np.array([_rayleigh_logperiodic(_gmm_surrogate(gmm, n, rng), freqs).max()
                         for _ in range(n_surrogate)])
    p_ln = float((1 + np.sum(null_ln >= z_max)) / (n_surrogate + 1))
    p_kde = float((1 + np.sum(null_kde >= z_max)) / (n_surrogate + 1))
    p_gmm = float((1 + np.sum(null_gmm >= z_max)) / (n_surrogate + 1))

    nearest, rel = None, np.inf
    for t in candidate_size_ratios():
        r = abs(best_ratio - t.value) / t.value
        if r < rel:
            nearest, rel = t, r
    return LogPeriodicResult(n, best_ratio, f_star, z_max, p_ln, p_kde, p_gmm,
                             max(p_ln, p_kde, p_gmm), nearest, float(rel))


@dataclass
class TargetedRatioResult:
    name: str
    ratio: float
    kind: str
    z: float
    p_lognormal: float
    p_kde: float
    p_gmm: float            # population-controlled (primary)
    p_value: float          # conservative max over the three nulls


def targeted_ratio_tests(sizes: np.ndarray, n_surrogate: int = 600,
                         seed: int = 0) -> list[TargetedRatioResult]:
    """Test each *preregistered* candidate ratio at its own single frequency.

    This is the honest way to probe specific ratios (e.g. ``1+phi0``, ``8pi``)
    that a coarse scan window cannot resolve: fix ``f = 1/log10(r)`` and ask how
    often a null reaches the observed Rayleigh power at that exact f.  The
    population-controlled GMM null (``p_gmm``) is decisive -- it strips the
    coarse ratios (~8-11) that merely ride on the glitch-size bimodality.
    """
    x = _clean_log10(sizes)
    rng = np.random.default_rng(seed)
    gmm = best_gmm_params(sizes, seed=seed)[:3]
    out: list[TargetedRatioResult] = []
    for t in candidate_size_ratios():
        f = np.array([1.0 / np.log10(t.value)])
        z_obs = float(_rayleigh_logperiodic(x, f)[0])
        null_ln = np.array([_rayleigh_logperiodic(_lognormal_surrogate(x, rng), f)[0]
                            for _ in range(n_surrogate)])
        null_kde = np.array([_rayleigh_logperiodic(_kde_surrogate(x, rng), f)[0]
                             for _ in range(n_surrogate)])
        null_gmm = np.array([_rayleigh_logperiodic(_gmm_surrogate(gmm, len(x), rng), f)[0]
                             for _ in range(n_surrogate)])
        p_ln = float((1 + np.sum(null_ln >= z_obs)) / (n_surrogate + 1))
        p_kde = float((1 + np.sum(null_kde >= z_obs)) / (n_surrogate + 1))
        p_gmm = float((1 + np.sum(null_gmm >= z_obs)) / (n_surrogate + 1))
        out.append(TargetedRatioResult(t.name, t.value, t.kind, z_obs,
                                       p_ln, p_kde, p_gmm, max(p_ln, p_kde, p_gmm)))
    return out


def periodogram_curve(sizes: np.ndarray, ratio_lo: float = 1.3, ratio_hi: float = 30.0,
                      n_freq: int = 500, n_surrogate: int = 600, seed: int = 0):
    """Return (ratios, z, z95) for plotting the log-periodogram + the 95% bar."""
    x = _clean_log10(sizes)
    f_lo, f_hi = 1.0 / np.log10(ratio_hi), 1.0 / np.log10(ratio_lo)
    freqs = np.linspace(f_lo, f_hi, n_freq)
    z = _rayleigh_logperiodic(x, freqs)
    ratios = 10.0 ** (1.0 / freqs)
    rng = np.random.default_rng(seed)
    gmm = best_gmm_params(sizes, seed=seed)[:3]
    null_max = np.array([_rayleigh_logperiodic(_gmm_surrogate(gmm, len(x), rng), freqs).max()
                         for _ in range(n_surrogate)])
    return ratios, z, float(np.percentile(null_max, 95))


@dataclass
class DiscretenessReport:
    n: int
    lognormal: LogNormalFit
    gmm: GMMResult
    logperiodic: LogPeriodicResult
    targeted: list[TargetedRatioResult]
    verdict: str


def discreteness_report(sizes: np.ndarray, *, alpha: float = 0.05,
                        seed: int = 0) -> DiscretenessReport:
    ln = lognormal_baseline(sizes)
    gm = gmm_multimodality(sizes, seed=seed)
    lp = log_periodicity(sizes, seed=seed)
    tg = targeted_ratio_tests(sizes, seed=seed)

    # Decisive null is the population-controlled GMM bootstrap (p_gmm): it strips
    # any coarse ratio that merely tracks the glitch-size bimodality.  A single
    # targeted ratio must also beat a look-elsewhere (Bonferroni) correction for
    # the preregistered candidate family.
    n_cand = sum(1 for t in tg if t.kind != "audit")
    surviving = [t.name for t in tg
                 if t.kind != "audit" and min(1.0, t.p_gmm * n_cand) < alpha]
    kernel_match = lp.p_gmm < alpha and lp.nearest_rel_err < 0.05
    smooth_comb = min(lp.p_lognormal, lp.p_kde) < alpha  # beats the smooth nulls
    pop_comb = lp.p_gmm < alpha       # comb survives the population-controlled null
    if kernel_match and pop_comb:
        verdict = (f"TFPT-specific log-periodic comb (ratio {lp.best_ratio:.2f} ~ "
                   f"{lp.nearest.name}, p_gmm={lp.p_gmm:.3f}) survives the "
                   "population-controlled null")
    elif smooth_comb and not pop_comb:
        verdict = (f"log-periodicity at ratio {lp.best_ratio:.2f} (p_smooth="
                   f"{min(lp.p_lognormal, lp.p_kde):.3f}) is the known glitch-size "
                   f"BIMODALITY (best_k={gm.best_k}); it vanishes under the "
                   f"population-controlled null (p_gmm={lp.p_gmm:.3f}) and the best "
                   f"ratio is not preregistered (closest {lp.nearest.name}, "
                   f"{100*lp.nearest_rel_err:.0f}% off) -- NOT a kernel signature")
    elif smooth_comb:
        verdict = (f"log-periodic comb at ratio {lp.best_ratio:.2f} (p_gmm="
                   f"{lp.p_gmm:.3f}) but not a preregistered ratio "
                   f"(closest {lp.nearest.name}, {100*lp.nearest_rel_err:.0f}% off)")
    elif surviving:
        verdict = (f"no global comb; targeted ratio(s) {surviving} survive the "
                   "population-controlled null -- tentative")
    else:
        verdict = "smooth (broad/bimodal) continuum; no TFPT log-periodic cascade"
    return DiscretenessReport(lp.n, ln, gm, lp, tg, verdict)
