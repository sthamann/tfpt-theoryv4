"""FRB.03 -- activity-window eigenwidths of periodic repeaters.

The headline new candidate of the user's note:

    W_broad / P  ~  sqrt(lambda2) = (2/3)^3 = 8/27 ~ 0.2963
    W_core  / P  ~  sqrt(lambda3) = (1/3)^3 = 1/27 ~ 0.0370

i.e. the *visibility/field-amplitude* roots of the recovery eigenvalues set the
phase widths of periodic-repeater activity windows.

Only a couple of FRB sources have a securely measured activity period, so this
is a *curated, cited* table -- not a population fit.  Values are published; the
core-window fractions are approximate (definitions differ between papers).  Add
more rows as new periodic repeaters are confirmed.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .recovery_kernel import SQRT_LAMBDA2, SQRT_LAMBDA3


@dataclass(frozen=True)
class PeriodicRepeater:
    name: str
    period_d: float
    w_broad_d: float            # full activity window (days)
    w_core_d: float             # window containing ~50% of bursts (days); NaN if undefined
    reference: str
    period_err_d: float = 0.0
    w_broad_err_d: float = 0.0
    w_core_err_d: float = float("nan")


# Curated from the literature (robustly periodic repeaters only).
PERIODIC_REPEATERS: tuple[PeriodicRepeater, ...] = (
    PeriodicRepeater(
        "FRB 20180916B", 16.35, 5.0, 0.6,
        "CHIME/FRB Collab. 2020 (Nature 582, 351; arXiv:2001.10275): "
        "P=16.35+/-0.15 d, ~5 d activity window, ~50% within ~0.6 d",
        period_err_d=0.15, w_broad_err_d=1.0, w_core_err_d=0.2,
    ),
    PeriodicRepeater(
        "FRB 20121102A", 157.0, 83.0, float("nan"),
        "Rajwade et al. 2020 (MNRAS 495, 3551): P~157 d, active duty cycle ~53% "
        "(=> W_broad ~ 0.53 P); no well-defined narrow core window",
        period_err_d=7.0, w_broad_err_d=15.0,
    ),
)


@dataclass
class WindowMatch:
    name: str
    period_d: float
    w_broad_over_p: float
    broad_target: float
    broad_rel_err: float        # |ratio - 8/27| / (8/27)
    w_core_over_p: float
    core_target: float
    core_rel_err: float
    reference: str


@dataclass
class ActivityWindowResult:
    matches: list[WindowMatch]
    c_window: float             # best broad-window match score in [0,1]
    note: str


def activity_window_test(repeaters=PERIODIC_REPEATERS, tol: float = 0.05) -> ActivityWindowResult:
    """Compare W_broad/P to 8/27 and W_core/P to 1/27 for each periodic source."""
    matches: list[WindowMatch] = []
    best = 0.0
    for r in repeaters:
        wb = r.w_broad_d / r.period_d
        be = abs(wb - SQRT_LAMBDA2) / SQRT_LAMBDA2
        wc = r.w_core_d / r.period_d
        ce = abs(wc - SQRT_LAMBDA3) / SQRT_LAMBDA3 if np.isfinite(wc) else float("nan")
        matches.append(WindowMatch(r.name, r.period_d, wb, SQRT_LAMBDA2, be,
                                   wc, SQRT_LAMBDA3, ce, r.reference))
        best = max(best, float(np.exp(-(be / tol) ** 2)))
    n_broad_match = sum(1 for m in matches if m.broad_rel_err < tol)
    note = (f"{len(matches)} periodic repeaters; {n_broad_match} match W_broad/P~8/27 "
            f"within {int(tol * 100)}%. n is too small for a population claim -- "
            f"a candidate match, not evidence.")
    return ActivityWindowResult(matches, best, note)
