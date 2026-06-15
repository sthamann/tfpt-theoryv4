"""Package E -- data-derived activity windows from folded burst phases.

FRB 20180916B must not *define* "broad" and "core" (a tape measure calibrated on
the first fish). This module folds raw arrival times at a period and computes the
windows as preregistered **highest-density intervals (HDIs)**:

    W_broad / P = minimal phase arc containing 90% of bursts,
    W_core  / P = minimal phase arc containing 50% of bursts,

directly in units of the period, so they can be compared to 8/27 and 1/27
without any per-source tuning. With CHIME this can be applied to FRB 20180916B
(folded at 16.33 d); other periodic repeaters need their own folded arrival times.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .recovery_kernel import SQRT_LAMBDA2, SQRT_LAMBDA3


def fold_phases(mjd: np.ndarray, period_days: float, ref_mjd: float | None = None) -> np.ndarray:
    t = np.asarray(mjd, float)
    t = t[np.isfinite(t)]
    ref = ref_mjd if ref_mjd is not None else 0.0
    return ((t - ref) / period_days) % 1.0


def hdi_width(phases: np.ndarray, frac: float) -> float:
    """Minimal circular arc (in phase fraction) containing ``frac`` of the points."""
    p = np.sort(np.asarray(phases, float) % 1.0)
    n = len(p)
    if n < 2:
        return float("nan")
    k = max(2, int(np.ceil(frac * n)))
    pp = np.concatenate([p, p + 1.0])          # wrap-around
    widths = pp[k - 1:k - 1 + n] - pp[0:n]     # arc spanned by k consecutive points
    return float(np.min(widths))


@dataclass
class ExtractedWindow:
    source: str
    n_bursts: int
    period_days: float
    w_broad_over_p: float
    w_core_over_p: float
    broad_rel_err: float          # |W_broad/P - 8/27| / (8/27)
    core_rel_err: float           # |W_core/P  - 1/27| / (1/27)
    note: str


def extract_windows(source: str, mjd: np.ndarray, period_days: float) -> ExtractedWindow:
    ph = fold_phases(mjd, period_days)
    n = int(np.isfinite(ph).sum())
    wb = hdi_width(ph, 0.90)
    wc = hdi_width(ph, 0.50)
    be = abs(wb - SQRT_LAMBDA2) / SQRT_LAMBDA2 if np.isfinite(wb) else float("nan")
    ce = abs(wc - SQRT_LAMBDA3) / SQRT_LAMBDA3 if np.isfinite(wc) else float("nan")
    return ExtractedWindow(source, n, period_days, wb, wc, be, ce,
                           f"data-derived HDI windows from {n} folded bursts "
                           f"(90%/50% phase arcs); vs 8/27 ({100*be:.0f}%), 1/27 ({100*ce:.0f}%)")
