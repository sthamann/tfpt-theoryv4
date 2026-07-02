"""QT.04-mirror bend fitting for the circuit relaxation curve.

The observable is the combined two-mode relaxation over carrier substeps m:

    R(m) = w0 + w1 * exp(-r1 m) + w2 * exp(-r2 m),

with the walled-clock signature r2/r1 = ln3/ln(3/2) = 2.7095 (BEND), a protected
floor w0 (Perron mode) and no third decaying mode (hard wall).  Two fits mirror
``quantum-testbed`` QT.04:

    fixed-ratio template  -- r2/r1 FROZEN at the bend, one rate parameter (tau);
    free-ratio control    -- both rates free (the anti-numerology control): a kernel
                             relaxation must RECOVER 2.7095, anything else rejects it.

Grid scan (as in QT.04) + Nelder-Mead refinement on the log-rates; amplitudes are
always solved linearly (variable projection).
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import numpy as np
from scipy.optimize import minimize, minimize_scalar

from .constants import BEND

_RATIO_WINDOW = math.log(1.15)      # QT.04 acceptance: free ratio within 15% of the bend


def _weights_and_rms(t: np.ndarray, y: np.ndarray, r1: float, r2: float
                     ) -> tuple[np.ndarray, float]:
    X = np.column_stack([np.ones_like(t), np.exp(-r1 * t), np.exp(-r2 * t)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    rms = float(np.sqrt(np.mean((X @ beta - y) ** 2)))
    return beta, rms


@dataclass
class FixedRatioFit:
    rate1: float                 # slow rate per substep (tau^-1); rate2 = BEND * rate1
    weights: tuple[float, float, float]
    rms: float


@dataclass
class FreeRatioFit:
    rate1: float
    rate2: float
    ratio: float                 # recovered bend r2/r1
    weights: tuple[float, float, float]
    rms: float


@dataclass
class BendReport:
    fixed: FixedRatioFit
    free: FreeRatioFit
    bend_target: float
    bend_bias: float             # free ratio - 2.7095
    bend_bias_rel: float
    on_bend: bool                # free ratio within the 15% QT.04 window
    template_ok: bool            # fixed template rms <= 1.5x free rms
    is_kernel_relaxation: bool

    def to_dict(self) -> dict:
        return asdict(self)


def _rate_grid(t: np.ndarray, n: int) -> np.ndarray:
    span = t.max() - t.min()
    dt = t[1] - t[0]
    return np.logspace(math.log10(0.05 / span), math.log10(8.0 / dt), n)


def fit_fixed_ratio(t: np.ndarray, y: np.ndarray, ratio: float = BEND,
                    n_scan: int = 400) -> FixedRatioFit:
    """One-parameter template: scan + refine the slow rate, ratio frozen."""
    t = np.asarray(t, float)
    y = np.asarray(y, float)
    rs = _rate_grid(t, n_scan)
    rms_grid = [_weights_and_rms(t, y, r, ratio * r)[1] for r in rs]
    r0 = rs[int(np.argmin(rms_grid))]
    res = minimize_scalar(lambda lr: _weights_and_rms(t, y, math.exp(lr), ratio * math.exp(lr))[1],
                          bracket=(math.log(r0) - 0.3, math.log(r0), math.log(r0) + 0.3),
                          method="brent", options={"xtol": 1e-14})
    r = math.exp(float(res.x))
    beta, rms = _weights_and_rms(t, y, r, ratio * r)
    return FixedRatioFit(r, tuple(float(b) for b in beta), rms)


def fit_free_ratio(t: np.ndarray, y: np.ndarray, n_scan: int = 120) -> FreeRatioFit:
    """Two free rates (+ floor): grid over ordered pairs, Nelder-Mead refinement."""
    t = np.asarray(t, float)
    y = np.asarray(y, float)
    rs = _rate_grid(t, n_scan)
    best, best_rms = (rs[0], rs[1]), np.inf
    for i in range(n_scan):
        for j in range(i + 1, n_scan):
            rms = _weights_and_rms(t, y, rs[i], rs[j])[1]
            if rms < best_rms:
                best, best_rms = (rs[i], rs[j]), rms

    def objective(lr: np.ndarray) -> float:
        return _weights_and_rms(t, y, math.exp(lr[0]), math.exp(lr[1]))[1]

    res = minimize(objective, np.log(best), method="Nelder-Mead",
                   options={"xatol": 1e-13, "fatol": 1e-16, "maxiter": 4000})
    r1, r2 = sorted(math.exp(v) for v in res.x)
    beta, rms = _weights_and_rms(t, y, r1, r2)
    return FreeRatioFit(r1, r2, r2 / r1, tuple(float(b) for b in beta), rms)


def bend_report(t: np.ndarray, y: np.ndarray) -> BendReport:
    fixed = fit_fixed_ratio(t, y)
    free = fit_free_ratio(t, y)
    bias = free.ratio - BEND
    on_bend = abs(math.log(free.ratio / BEND)) < _RATIO_WINDOW
    template_ok = fixed.rms < 1.5 * free.rms + 1e-9
    return BendReport(fixed, free, BEND, bias, bias / BEND,
                      bool(on_bend), bool(template_ok), bool(on_bend and template_ok))


@dataclass
class SingleExpFit:
    rate: float
    amplitude: float
    floor: float
    rms: float


def fit_single_exp(t: np.ndarray, y: np.ndarray, n_scan: int = 400) -> SingleExpFit:
    """Per-mode circuit-native decode: y(t) = floor + a * exp(-r t) (floor absorbs
    the readout/noise offset that survives on hardware)."""
    t = np.asarray(t, float)
    y = np.asarray(y, float)

    def rms_at(r: float) -> float:
        X = np.column_stack([np.ones_like(t), np.exp(-r * t)])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        return float(np.sqrt(np.mean((X @ beta - y) ** 2)))

    rs = _rate_grid(t, n_scan)
    r0 = rs[int(np.argmin([rms_at(r) for r in rs]))]
    res = minimize_scalar(lambda lr: rms_at(math.exp(lr)),
                          bracket=(math.log(r0) - 0.3, math.log(r0), math.log(r0) + 0.3),
                          method="brent", options={"xtol": 1e-14})
    r = math.exp(float(res.x))
    X = np.column_stack([np.ones_like(t), np.exp(-r * t)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return SingleExpFit(r, float(beta[1]), float(beta[0]), rms_at(r))


def direct_bend(p2: np.ndarray, p3: np.ndarray, t: np.ndarray,
                tiny: float = 1e-12) -> float:
    """Exact-tier decode: per-mode log-linear slopes, bend = rate3/rate2.

    Only valid when the populations are floor-free (exact simulator); on noisy data
    use ``bend_report`` (the floor-aware template fit).
    """
    t = np.asarray(t, float)
    out = []
    for p in (np.asarray(p2, float), np.asarray(p3, float)):
        keep = p > tiny
        A = np.column_stack([np.ones(keep.sum()), t[keep]])
        slope = np.linalg.lstsq(A, np.log(p[keep]), rcond=None)[0][1]
        out.append(-slope)
    return out[1] / out[0]
