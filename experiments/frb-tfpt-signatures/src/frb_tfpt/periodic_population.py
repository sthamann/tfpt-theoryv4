"""FRB.03 (hardened) -- population test of activity-window eigenwidths.

A single match (FRB 20180916B at 8/27 and 1/27) is a candidate, never evidence.
This module evaluates W_broad/P vs 8/27 and W_core/P vs 1/27 across *all*
available periodic repeaters with: per-source deviations (error-propagated),
a population statistic, leave-one-out stability, and null models.

Acceptance (from the preregistration): >= 5 periodic repeaters, median broad
deviation < 10 %, >= 3 sources with a core window near 1/27, leave-one-out does
not flip the verdict, and q < 0.01 against the random-window null.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .activity_windows import PERIODIC_REPEATERS, PeriodicRepeater
from .recovery_kernel import SQRT_LAMBDA2, SQRT_LAMBDA3


@dataclass
class SourceWindow:
    name: str
    broad_ratio: float
    broad_ratio_err: float
    broad_rel_err: float          # |ratio - 8/27| / (8/27)
    core_ratio: float
    core_rel_err: float


@dataclass
class PeriodicPopulationResult:
    n_sources: int
    per_source: list[SourceWindow]
    median_broad_rel_err: float
    n_broad_within_tol: int
    n_core_within_tol: int
    leave_one_out_stable: bool
    null_p: float
    enough_sources: bool
    verdict: str
    c_window_population: float


def _ratio_err(w, werr, p, perr):
    return abs(w / p) * np.hypot(werr / w if w else 0.0, perr / p if p else 0.0)


def evaluate_periodic_windows(sources: tuple[PeriodicRepeater, ...] = PERIODIC_REPEATERS,
                              tol: float = 0.10, min_sources: int = 5,
                              n_null: int = 5000, seed: int = 0) -> PeriodicPopulationResult:
    per: list[SourceWindow] = []
    for r in sources:
        br = r.w_broad_d / r.period_d
        bre = _ratio_err(r.w_broad_d, r.w_broad_err_d, r.period_d, r.period_err_d)
        cr = r.w_core_d / r.period_d
        cre = abs(cr - SQRT_LAMBDA3) / SQRT_LAMBDA3 if np.isfinite(cr) else float("nan")
        per.append(SourceWindow(r.name, br, bre, abs(br - SQRT_LAMBDA2) / SQRT_LAMBDA2,
                                cr, cre))

    broad_rel = np.array([s.broad_rel_err for s in per])
    median_rel = float(np.median(broad_rel))
    n_broad = int(np.sum(broad_rel < tol))
    n_core = int(np.sum([np.isfinite(s.core_rel_err) and s.core_rel_err < tol for s in per]))

    # leave-one-out: does removing any one source change "median < tol"?
    loo = []
    for i in range(len(per)):
        rest = np.delete(broad_rel, i)
        loo.append(np.median(rest) < tol if len(rest) else False)
    base = median_rel < tol
    loo_stable = bool(len(per) > 1 and all(v == base for v in loo))

    # null: random duty-cycle windows drawn uniformly in (0,1); how often does a
    # population of this size land as close (median rel err) to 8/27 as observed?
    rng = np.random.default_rng(seed)
    n = len(per)
    null_med = np.empty(n_null)
    for k in range(n_null):
        w = rng.uniform(0.0, 1.0, n)
        null_med[k] = np.median(np.abs(w - SQRT_LAMBDA2) / SQRT_LAMBDA2)
    null_p = float((1 + np.sum(null_med <= median_rel)) / (n_null + 1))

    enough = n >= min_sources
    passed = (enough and median_rel < tol and n_core >= 3 and loo_stable and null_p < 0.01)
    if passed:
        verdict = "population-level support"
    elif n_broad >= 1 and not enough:
        verdict = (f"candidate only: {n_broad}/{n} broad matches but n={n} < {min_sources} "
                   f"required periodic repeaters")
    else:
        verdict = "no population-level window signature"
    c = float(np.clip((n_broad / n) * (null_p < 0.05), 0, 1)) if n else 0.0
    return PeriodicPopulationResult(n, per, median_rel, n_broad, n_core, loo_stable,
                                    null_p, enough, verdict, c)
