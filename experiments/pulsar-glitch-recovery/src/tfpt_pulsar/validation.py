"""Injection-recovery self-check for the discreteness machinery.

Before trusting a *null* result on the real catalogue we prove the pipeline can
(a) recover a genuine log-periodic comb at the injected ratio and (b) reject a
smooth, realistically *bimodal* size distribution.  Same discipline as the FRB
``free_quotient`` injection-recovery and the GW matched-filter injection suite.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .discreteness import log_periodicity


def _bimodal_smooth(n: int, rng: np.random.Generator) -> np.ndarray:
    """A smooth two-population (Crab-like + Vela-like) log-normal mixture,
    mimicking the real glitch-size distribution -- the hard null."""
    small = rng.normal(0.5, 0.6, size=n // 2)        # ~ few x 1e-9
    large = rng.normal(2.7, 0.4, size=n - n // 2)    # ~ hundreds x 1e-9
    return 10.0 ** np.concatenate([small, large])


def _logperiodic_comb(n: int, ratio: float, rng: np.random.Generator,
                      jitter_dex: float = 0.06) -> np.ndarray:
    """Sizes drawn on a log-periodic comb of the given spacing ratio + jitter."""
    step = np.log10(ratio)
    teeth = np.arange(0, 5.2, step)                  # cover ~5 dex
    centers = rng.choice(teeth, size=n)
    return 10.0 ** (centers + rng.normal(0.0, jitter_dex, size=n))


@dataclass
class InjectionResult:
    smooth_p: float
    smooth_rejected: bool          # expect True (no false comb)
    comb_p: float
    comb_ratio_recovered: float
    comb_detected: bool            # expect True
    comb_ratio_ok: bool            # recovered ratio within 8% of injected
    passed: bool


def injection_recovery(n: int = 700, inject_ratio: float = 27 / 8,
                       alpha: float = 0.05, seed: int = 1) -> InjectionResult:
    rng = np.random.default_rng(seed)
    smooth = _bimodal_smooth(n, rng)
    comb = _logperiodic_comb(n, inject_ratio, rng)

    lp_s = log_periodicity(smooth, n_surrogate=300, seed=seed)
    lp_c = log_periodicity(comb, n_surrogate=300, seed=seed)

    smooth_rejected = lp_s.p_value >= alpha
    comb_detected = lp_c.p_value < alpha
    ratio_ok = abs(lp_c.best_ratio - inject_ratio) / inject_ratio < 0.08
    return InjectionResult(
        smooth_p=lp_s.p_value, smooth_rejected=smooth_rejected,
        comb_p=lp_c.p_value, comb_ratio_recovered=lp_c.best_ratio,
        comb_detected=comb_detected, comb_ratio_ok=ratio_ok,
        passed=smooth_rejected and comb_detected and ratio_ok,
    )
