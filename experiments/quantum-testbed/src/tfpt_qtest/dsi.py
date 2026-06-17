"""Discrete scale invariance (DSI) — the dynamical TFPT signature.

A system relaxing to a fixed point through a *geometric ladder* of modes (rates
``gamma_k = gamma_0 * lambda^k``) relaxes not as a clean power law but as

    R(t) = power law * (1 + eps * cos(omega ln t + phi)),   omega = 2 pi / ln(lambda),

i.e. the critical exponent is **complex** (``alpha + i*omega``).  The frozen kernel
ratio reappears as a *log-frequency* in the dynamics.  The modulation amplitude is
exponentially suppressed for ratios near 1, ``eps ~ exp(-pi*omega/2) = exp(-pi^2/ln
lambda)`` — so only a *coarse* ladder leaves a detectable ripple (see ``quench.py``).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def log_frequency(lam: float) -> float:
    """DSI log-frequency ``omega = 2 pi / ln(lambda)`` (imag part of the exponent)."""
    return 2.0 * math.pi / math.log(lam)


def amplitude_suppression(lam: float) -> float:
    """The leading log-periodic Fourier amplitude scale ``exp(-pi*omega/2)`` — why
    fine ratios (lambda ~ 1) give an exponentially invisible DSI ripple."""
    return math.exp(-math.pi * log_frequency(lam) / 2.0)


def geometric_rate_relaxation(t: np.ndarray, lam: float, *, n_modes: int = 7,
                              gamma0: float = 10.0) -> np.ndarray:
    """Open-system recovery of a geometric ladder of decay rates ``gamma_k =
    gamma0 * lambda^{-k}``.  The equal-weight sum ``(1/N) sum_k exp(-gamma_k t)``
    is the textbook DSI result: a power-law envelope with a log-periodic ripple of
    period ``ln(lambda)`` in ``ln t``."""
    t = np.asarray(t, dtype=float)
    ks = np.arange(n_modes)
    rates = gamma0 * lam ** (-ks.astype(float))
    return np.exp(-np.outer(t, rates)).mean(axis=1)


@dataclass
class DSIFit:
    omega: float
    lam: float
    amplitude: float
    p_value: float
    detected: bool


def _design(logt: np.ndarray, omega: float) -> np.ndarray:
    return np.column_stack([np.ones_like(logt), logt,
                            np.cos(omega * logt), np.sin(omega * logt)])


def fit_log_periodic(t: np.ndarray, y: np.ndarray, omega: float) -> float:
    """Relative log-periodic amplitude at ``omega``: regress ``y`` on
    ``{1, ln t, cos(omega ln t), sin(omega ln t)}``."""
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

    Null: the smooth power-law fit ``{1, ln t}`` plus phase-randomised residuals —
    keeps the trend and residual amplitude, destroys a genuine log-periodic comb, so
    the detection is the phase coherence at ``omega``.
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
