"""QT.04 -- the EXACT discrete->dynamic clock and its recovery-waveform signature.

The verification suite reconstructs the discrete->dynamic transition exactly
(v124/v126/v147): the frozen transfer spectrum is

    lambda_n = (1 - n/N_fam)^{p2} = (1 - n/3)^6 ,   n = 0,1,2     (alpha_n = n/3 = spec A0*)

and the continuous clock is the resummed logarithm

    rate(n) = -p2 ln(1 - n/N_fam) = -6 ln(1 - n/3)  ->  {0, 6 ln(3/2), 6 ln 3},

a *Born-squared Gaussian zero-mode* partition ratio (v147) with a **pole (wall) at
n = N_fam = 3**.  So -- contrary to a naive infinite geometric ladder (which would give
sustained discrete scale invariance) -- the TFPT single-event recovery is a **walled,
two-mode clock**:

    R(t) = w0  +  w1 e^{-(6 ln 3/2) t/tau}  +  w2 e^{-(6 ln 3) t/tau}

with three sharp, *new* signatures that are different from a static ratio:

  1. BEND (det'-clean, v147): the two decay rates are locked at the ratio
         rate(2)/rate(1) = ln 3 / ln(3/2) = log_{3/2} 3 = 2.7095          (exact)
     -- a ONE-parameter (tau) two-exponential template, not two free rates.
  2. PROTECTED FLOOR: a non-decaying w0 mode (lambda=1, the "law") -> recovery saturates
     at a floor, it never returns to zero.
  3. HARD WALL: NO third decay mode (pole at n=3) -> >=3 robust decay timescales is a
     tension, not a TFPT recovery.

This module exhibits the exact identities and turns the bend into a **matched-filter
waveform discriminator**: fit the fixed-ratio (2.7095) two-exponential template vs a
free two-exponential; a kernel recovery is fit by the template and recovers 2.7095, a
non-kernel recovery is not.  (DSI / log-periodicity returns only across a *cascade* of
events, never within one walled recovery -- see ``quench.py``.)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

N_FAM = 3
P2 = 6
BEND = math.log(3.0) / math.log(1.5)            # rate(2)/rate(1) = log_{3/2} 3 = 2.7095
RATE1 = P2 * math.log(1.5)                       # 6 ln(3/2) = Delta = 2.4328
RATE2 = P2 * math.log(3.0)                       # 6 ln 3 = 6.5917


def clock_rate(n: float) -> float:
    """The resummed clock ``rate(n) = -6 ln(1 - n/3)`` (pole/wall at n=3)."""
    return -P2 * math.log(1.0 - n / N_FAM)


@dataclass
class ClockIdentities:
    spectrum: list[float]          # {1,(2/3)^6,(1/3)^6}
    rates: list[float]             # {0, 6ln(3/2), 6ln3}
    bend: float                    # rate(2)/rate(1)
    bend_is_log32_3: bool
    bend_curvature: float          # rate(2)/rate(1) - 2 = log_{3/2}(4/3)
    sheet_slope: float             # linear term p2/N_fam = |Z2|
    wall_at_nfam: bool             # rate(n) -> inf at n=3
    verdict: str


def clock_identities() -> ClockIdentities:
    spec = [(1 - n / N_FAM) ** P2 for n in range(3)]
    rates = [clock_rate(0), clock_rate(1), clock_rate(2)]
    bend = rates[2] / rates[1]
    bend_ok = abs(bend - BEND) < 1e-12
    curvature = bend - 2.0                                  # = log_{3/2}(4/3)
    curvature_ok = abs(curvature - math.log(4 / 3) / math.log(1.5)) < 1e-12
    sheet = P2 / N_FAM                                      # = 2 = |Z2|
    wall = clock_rate(3 - 1e-9) > 50.0                      # diverges at n->3
    ok = bend_ok and curvature_ok and sheet == 2 and wall
    verdict = (f"walled two-mode clock: rates {{0, {RATE1:.4f}, {RATE2:.4f}}}, "
               f"det'-clean bend {bend:.4f}=ln3/ln(3/2), sheet slope {sheet:.0f}=|Z2|, "
               "hard wall at n=N_fam=3 (no 3rd mode)" if ok
               else "FAIL: a clock identity did not hold")
    return ClockIdentities(spec, rates, bend, bend_ok, curvature, sheet, wall, verdict)


def recovery_curve(t: np.ndarray, tau: float, w0: float, w1: float, w2: float) -> np.ndarray:
    """The exact TFPT recovery waveform: floor + two locked-ratio exponentials."""
    t = np.asarray(t, dtype=float)
    return w0 + w1 * np.exp(-RATE1 * t / tau) + w2 * np.exp(-RATE2 * t / tau)


# --------------------------------------------------------------------------- matched filter
def _fit_fixed_ratio(t: np.ndarray, y: np.ndarray, ratio: float,
                     n_scan: int = 400) -> tuple[float, float]:
    """Fit ``w0 + w1 e^{-r t} + w2 e^{-ratio r t}`` (rate ratio FIXED): scan the slow
    rate r, solve the 3 linear amplitudes by least squares.  Returns (best r, rms)."""
    span = t.max() - t.min()
    rs = np.logspace(math.log10(0.3 / span), math.log10(30.0 / (t[1] - t[0] + 1e-9)), n_scan)
    best_r, best_rms = rs[0], np.inf
    for r in rs:
        X = np.column_stack([np.ones_like(t), np.exp(-r * t), np.exp(-ratio * r * t)])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        rms = float(np.sqrt(np.mean((X @ beta - y) ** 2)))
        if rms < best_rms:
            best_r, best_rms = r, rms
    return best_r, best_rms


def _fit_free_ratio(t: np.ndarray, y: np.ndarray, n_scan: int = 120) -> tuple[float, float]:
    """Fit two FREE exponential rates (+ floor); return (recovered ratio r2/r1, rms)."""
    span = t.max() - t.min()
    lo = math.log10(0.3 / span)
    hi = math.log10(30.0 / (t[1] - t[0] + 1e-9))
    rs = np.logspace(lo, hi, n_scan)
    best, best_rms = (rs[0], rs[1]), np.inf
    for i in range(n_scan):
        for j in range(i + 1, n_scan):
            X = np.column_stack([np.ones_like(t), np.exp(-rs[i] * t), np.exp(-rs[j] * t)])
            beta, *_ = np.linalg.lstsq(X, y, rcond=None)
            rms = float(np.sqrt(np.mean((X @ beta - y) ** 2)))
            if rms < best_rms:
                best, best_rms = (rs[i], rs[j]), rms
    return best[1] / best[0], best_rms


@dataclass
class MatchedFilterResult:
    injected_ratio: float
    template_rms: float           # fixed-ratio (2.7095) template residual
    free_ratio_recovered: float   # ratio from the free 2-exp fit
    is_kernel_recovery: bool      # free ratio lands on the bend AND template fits well


def matched_filter_discriminate(injected_ratio: float, *, n_t: int = 200, t_max: float = 6.0,
                                noise: float = 0.01, seed: int = 0) -> MatchedFilterResult:
    """Build a synthetic recovery with two decay rates in ``injected_ratio`` and test
    the fixed-ratio (2.7095) template against a free 2-exp fit -- the waveform
    discriminator for the bend signature."""
    rng = np.random.default_rng(seed)
    t = np.linspace(0.0, t_max, n_t)
    r1 = RATE1
    y = 0.3 + 0.5 * np.exp(-r1 * t) + 0.4 * np.exp(-injected_ratio * r1 * t)
    y = y + rng.normal(0.0, noise * y.max(), size=n_t)
    _, tmpl_rms = _fit_fixed_ratio(t, y, BEND)
    free_ratio, free_rms = _fit_free_ratio(t, y)
    on_bend = abs(math.log(free_ratio / BEND)) < math.log(1.15)      # within 15%
    template_ok = tmpl_rms < 1.5 * free_rms + 1e-6
    return MatchedFilterResult(injected_ratio, tmpl_rms, free_ratio,
                               bool(on_bend and template_ok))
