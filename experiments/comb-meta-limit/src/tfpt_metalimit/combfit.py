"""Harmonised comb-amplitude estimator + red-noise-aware null band.

Every recovery channel in the repo runs the SAME log-periodic detector: it fits

    y(ln t) = poly_deg2(ln t)  +  A cos(omega ln t)  +  B sin(omega ln t)

and reports the *gain* g = fraction of the poly-detrended variance the cos/sin pair explains.
For an amplitude UPPER LIMIT we need the fitted comb amplitude itself, not just the gain:

    a_hat = sqrt(A^2 + B^2)   -- the comb amplitude at omega.

For the log-flux channels (magnetar / GRB / ENT) the recovery observable is ``y = ln(flux)`` and
the theory comb enters multiplicatively, ``R = powerlaw * (1 + eps cos(omega ln t + phi))``, so
``ln R ~ smooth + eps cos(...)`` and ``a_hat`` is DIRECTLY the fractional comb amplitude ``eps``
that TFPT predicts (``eps ~ 2%``). That is the whole reason these channels can yield an *absolute*
eps, while linear-intensity channels (FRB tails, pulsar nudot) only yield a normalised amplitude.

The honest, RED-NOISE-AWARE part: astrophysical recovery curves are correlated (red), so the naive
i.i.d. amplitude error massively understates the uncertainty (this is exactly why the sibling
detectors rank the kernel gain against an OFF-kernel periodogram instead of using an analytic
error). We do the same in amplitude/power space: fit ``a_hat`` at a bank of off-kernel
log-frequencies, and use that empirical distribution as the null. The comb POWER excess

    eps2_hat = a_hat(omega)^2 - mean_offkernel(a_hat(f)^2)

is an (approximately) unbiased estimate of ``eps^2`` (the off-kernel mean removes the noise +
generic-wiggle bias), with a variance taken from the off-kernel power scatter. Working in power
(eps^2) is the standard footing for a periodogram / matched-filter upper limit and lets a null
channel sit at eps^2 ~ 0 with a proper, red-noise-calibrated uncertainty.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import numpy as np

from .kernel import DETREND_DEG, LAMBDA, OMEGA


def comb_gain_amp(lt: np.ndarray, y: np.ndarray, omega: float,
                  deg: int = DETREND_DEG) -> tuple[float, float]:
    """(gain, a_hat) at ``omega``: gain = detrended-variance fraction the comb explains (identical
    to the sibling detectors), a_hat = sqrt(A^2 + B^2) the fitted comb amplitude."""
    P = np.vander(lt, deg + 1)
    b0, *_ = np.linalg.lstsq(P, y, rcond=None)
    ss0 = float(np.sum((y - P @ b0) ** 2))
    X = np.column_stack([P, np.cos(omega * lt), np.sin(omega * lt)])
    b1, *_ = np.linalg.lstsq(X, y, rcond=None)
    ss1 = float(np.sum((y - X @ b1) ** 2))
    gain = max(0.0, (ss0 - ss1) / (ss0 + 1e-12))
    a_hat = float(math.hypot(b1[-2], b1[-1]))
    return gain, a_hat


def comb_periods(t: np.ndarray) -> float:
    """Number of comb periods the curve spans in ln(t): ln(t_max/t_min) / ln(lambda)."""
    t = np.asarray(t, float)
    t = t[t > 0]
    return float(np.log(t.max() / t.min()) / math.log(LAMBDA)) if len(t) > 1 else 0.0


def _offkernel_freqs(ln_range: float, omega: float, n_freq: int,
                     seed: int) -> np.ndarray:
    """Off-kernel log-frequency bank (same regime as the sibling detectors' periodogram null):
    from >= one full cycle in the window up to ~2.5 omega, excluding a neighbourhood of omega."""
    f_lo = max(0.9, 2.0 * math.pi / (ln_range or 1.0))
    f_hi = max(6.0, 2.5 * omega)
    rng = np.random.default_rng(seed)
    fs = rng.uniform(f_lo, f_hi, n_freq)
    return fs[np.abs(fs - omega) > 0.1 * omega]


@dataclass
class CombEstimate:
    """One recovery curve's comb-amplitude estimate at the kernel omega."""

    n_points: int
    comb_periods: float
    range_sufficient: bool
    gain: float           # detrended-variance fraction at omega (matches sibling detectors)
    a_hat: float          # fitted comb amplitude sqrt(A^2+B^2) at omega
    a_null_mean: float    # mean off-kernel comb amplitude (the noise/wiggle floor)
    power: float          # a_hat^2 (comb power at omega)
    power_null_mean: float  # mean off-kernel power = the bias to subtract
    eps2: float           # debiased comb power a_hat^2 - <off-kernel power>  (~ eps^2)
    se_power: float       # 1 sigma of the power estimate from the off-kernel scatter
    eps_hat: float        # sqrt(max(0, eps2))  -- debiased amplitude point estimate
    p_value: float        # periodogram rank of the kernel gain (matches sibling detectors)

    def as_dict(self) -> dict:
        return {k: (round(v, 6) if isinstance(v, float) else v) for k, v in asdict(self).items()}


def estimate_comb(t: np.ndarray, y: np.ndarray, *, omega: float = OMEGA,
                  min_periods: float = 2.8, n_freq: int = 400, seed: int = 0) -> CombEstimate:
    """Estimate the comb amplitude at ``omega`` on one recovery curve, with a red-noise-aware
    null band from off-kernel log-frequencies. ``y`` is the recovery observable (for log-flux
    channels ``y = ln(flux)`` so the amplitude IS the fractional comb amplitude eps)."""
    t = np.asarray(t, float)
    y = np.asarray(y, float)
    m = t > 0
    lt, yy = np.log(t[m]), y[m]
    periods = comb_periods(t[m])
    if len(lt) < 6:
        return CombEstimate(int(m.sum()), round(periods, 3), False, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    gain, a_hat = comb_gain_amp(lt, yy, omega)
    ln_range = float(lt.max() - lt.min())
    fs = _offkernel_freqs(ln_range, omega, n_freq, seed)
    null_gain = np.empty(len(fs))
    null_amp = np.empty(len(fs))
    for i, f in enumerate(fs):
        null_gain[i], null_amp[i] = comb_gain_amp(lt, yy, float(f))
    null_power = null_amp**2
    power = a_hat**2
    power_null_mean = float(np.mean(null_power))
    eps2 = power - power_null_mean
    # red-noise-aware 1 sigma of the power estimate: the scatter of the off-kernel power floor.
    se_power = float(np.std(null_power, ddof=1)) if len(null_power) > 1 else power_null_mean
    p_value = float((1 + np.sum(null_gain >= gain)) / (len(null_gain) + 1))
    return CombEstimate(
        n_points=int(m.sum()),
        comb_periods=round(periods, 3),
        range_sufficient=bool(periods >= min_periods),
        gain=gain,
        a_hat=a_hat,
        a_null_mean=float(np.mean(null_amp)),
        power=power,
        power_null_mean=power_null_mean,
        eps2=eps2,
        se_power=se_power,
        eps_hat=math.sqrt(max(0.0, eps2)),
        p_value=p_value,
    )
