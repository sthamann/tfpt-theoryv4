"""Burst timing: waiting-time structure and periodic activity windows.

* ``waiting_time_structure`` -- consecutive inter-burst intervals of one source.
  A *bimodal* waiting-time distribution (a within-storm mode plus an
  inter-storm mode) is a real, well-known feature of FRB 20121102A and is the
  timing analogue of the cascade picture in ``problem_b.txt`` section 5.
* ``folded_rayleigh`` -- fold arrival times at a trial period and measure phase
  concentration (Rayleigh).  Used as a sanity check that the pipeline recovers
  the known 16.33 d activity period of FRB 20180916B.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .energy_clusters import gmm_multimodality


@dataclass
class WaitingTimeResult:
    n_intervals: int
    log10_seconds: list[float]
    best_k: int | None
    delta_bic: float | None
    bimodal: bool
    note: str


def waiting_time_structure(mjd: np.ndarray, seed: int = 0) -> WaitingTimeResult:
    t = np.sort(np.asarray(mjd, dtype=float))
    t = t[np.isfinite(t)]
    if len(t) < 6:
        return WaitingTimeResult(0, [], None, None, False, "too few bursts")
    dt = np.diff(t)
    dt = dt[dt > 0] * 86_400.0  # seconds
    logdt = np.log10(dt)
    gm = gmm_multimodality(dt, seed=seed)
    bimodal = gm.best_k >= 2 and gm.delta_bic > 6
    return WaitingTimeResult(
        len(dt), [float(v) for v in logdt], gm.best_k, gm.delta_bic, bimodal,
        f"GMM best_k={gm.best_k}, dBIC={gm.delta_bic:.1f}",
    )


@dataclass
class FoldResult:
    period_days: float
    rayleigh_z: float
    p_value: float
    note: str


def folded_rayleigh(mjd: np.ndarray, period_days: float) -> FoldResult:
    """Phase-fold arrival times and Rayleigh-test for phase concentration."""
    t = np.asarray(mjd, dtype=float)
    t = t[np.isfinite(t)]
    n = len(t)
    if n < 6:
        return FoldResult(period_days, float("nan"), float("nan"), "too few bursts")
    phase = 2.0 * np.pi * (t % period_days) / period_days
    c, s = np.cos(phase).mean(), np.sin(phase).mean()
    z = n * (c * c + s * s)
    p = float(np.exp(-z) * (1 + (2 * z - z * z) / (4 * n)))  # Rayleigh w/ correction
    return FoldResult(period_days, float(z), float(np.clip(p, 0, 1)),
                      f"folded {n} bursts at {period_days} d")
