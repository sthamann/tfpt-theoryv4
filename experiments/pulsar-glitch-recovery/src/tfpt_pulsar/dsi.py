"""Discrete scale invariance (DSI) — the *dynamical* TFPT signature.

The FRB/pulsar size searches (FRB.02-09, PG.01-03) all tested the frozen kernel as
a **static ratio** in a histogram and came back null.  `problem_1.txt` §D points at
a richer, *dynamical* fingerprint: the recovery **curve** should carry a small
log-periodic modulation

    R(t) = 1 + eps * cos(omega * ln t + phi)        with   omega = 2*pi / ln(lambda).

This is **discrete scale invariance**: a system relaxing to a fixed point through a
*geometric ladder* of modes (rates ``gamma_k = gamma_0 * lambda^k``, exactly the
``(3/2)^k`` / E8-cascade structure) does **not** relax as a clean power law but as a
power law times a log-periodic oscillation.  Equivalently the critical exponent is
**complex**, ``alpha + i*omega``, with the imaginary part set by the kernel ratio.

So the discrete kernel reappears not as a number you read off a ruler, but as a
*log-frequency* in how things recover — the "übergang diskret -> dynamisch".  This
module is the shared, falsifiable predictor; PG.04 tests it on real glitch-recovery
timescales, the quantum-testbed exhibits it in a quench.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def log_frequency(lam: float) -> float:
    """The DSI log-frequency ``omega = 2*pi / ln(lambda)`` (imag part of the
    complex exponent), i.e. the period in ``ln t`` is ``ln(lambda)``."""
    return 2.0 * math.pi / math.log(lam)


def complex_exponent(alpha: float, lam: float) -> complex:
    """The complex critical exponent ``alpha + i*omega(lambda)``."""
    return complex(alpha, log_frequency(lam))


def log_periodic_relaxation(t: np.ndarray, lam: float, *, alpha: float = 0.0,
                            eps: float = 0.1, phi: float = 0.0,
                            c: float = 1.0) -> np.ndarray:
    """``c * t^{-alpha} * (1 + eps cos(omega ln t + phi))`` — the DSI recovery curve."""
    t = np.asarray(t, dtype=float)
    om = log_frequency(lam)
    return c * t ** (-alpha) * (1.0 + eps * np.cos(om * np.log(t) + phi))


def geometric_rate_relaxation(t: np.ndarray, lam: float, *, n_modes: int = 8,
                              gamma0: float = 1.0) -> np.ndarray:
    """Relaxation of a *geometric ladder* of modes with rates ``gamma_k = gamma0
    * lambda^{-k}`` (each rung slower by ``lambda``).  The equal-weight sum

        S(t) = (1/N) Σ_k exp(-gamma_k t)

    is the textbook DSI result: a power-law envelope with a log-periodic ripple of
    period ``ln(lambda)`` in ``ln t``.  This is the mechanism by which the frozen
    kernel ladder becomes a dynamical log-frequency."""
    t = np.asarray(t, dtype=float)
    ks = np.arange(n_modes)
    rates = gamma0 * lam ** (-ks.astype(float))
    return np.exp(-np.outer(t, rates)).mean(axis=1)


@dataclass
class DSIFit:
    omega: float            # tested log-frequency
    lam: float              # corresponding ratio 10^(2pi/omega in dex)... = e^{2pi/omega}
    amplitude: float        # fitted log-periodic amplitude (relative)
    p_value: float          # vs phase-randomised / smooth-detrended surrogates
    detected: bool


def _design(logt: np.ndarray, omega: float) -> np.ndarray:
    return np.column_stack([np.ones_like(logt), logt,
                            np.cos(omega * logt), np.sin(omega * logt)])


def fit_log_periodic(t: np.ndarray, y: np.ndarray, omega: float) -> float:
    """Relative log-periodic amplitude at ``omega``: regress ``y`` on
    ``{1, ln t, cos(omega ln t), sin(omega ln t)}`` and return
    ``sqrt(b_cos^2+b_sin^2)`` normalised by the smooth (1, ln t) level."""
    t = np.asarray(t, float)
    y = np.asarray(y, float)
    m = np.isfinite(t) & np.isfinite(y) & (t > 0)
    logt, yy = np.log(t[m]), y[m]
    X = _design(logt, omega)
    beta, *_ = np.linalg.lstsq(X, yy, rcond=None)
    amp = math.hypot(beta[2], beta[3])
    base = abs(beta[0]) + abs(beta[1]) * np.mean(np.abs(logt)) + 1e-12
    return float(amp / base)


def detect_dsi(t: np.ndarray, y: np.ndarray, lam: float, *, n_surrogate: int = 500,
               alpha: float = 0.05, seed: int = 0) -> DSIFit:
    """Test for a log-periodic ripple at the kernel log-frequency ``omega(lambda)``.

    Null: the smooth power-law part (the ``{1, ln t}`` fit) plus phase-randomised
    residuals — destroys a genuine log-periodic comb while keeping the trend and
    the residual amplitude, so a detection is the *phase coherence* at ``omega``.
    """
    om = log_frequency(lam)
    amp = fit_log_periodic(t, y, om)

    t = np.asarray(t, float)
    y = np.asarray(y, float)
    m = np.isfinite(t) & np.isfinite(y) & (t > 0)
    logt, yy = np.log(t[m]), y[m]
    X0 = np.column_stack([np.ones_like(logt), logt])
    b0, *_ = np.linalg.lstsq(X0, yy, rcond=None)
    resid = yy - X0 @ b0
    rng = np.random.default_rng(seed)
    null = np.empty(n_surrogate)
    for i in range(n_surrogate):
        ys = X0 @ b0 + rng.permutation(resid)
        null[i] = fit_log_periodic(t[m], ys, om)
    p = float((1 + np.sum(null >= amp)) / (n_surrogate + 1))
    return DSIFit(om, lam, amp, p, p < alpha)
