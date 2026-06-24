"""FRB.10 -- joint intensity x polarisation per source (search.txt §2 cross-correlation).

A strong TFPT hit would show BOTH:
  (A) echo / recovery quotient pile-up at 64/729 or 8/27 in consecutive energies, AND
  (B) mu4 / Z4 phase structure in PA or |exp(4 i chi)| after RM correction.

Each axis is tested separately elsewhere (FRB.02, FRB.04/08); this module asks whether
sources that score on one axis also score on the other beyond chance (Fisher / permutation).
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .constants import LAMBDA3, LAMBDA6

from .frb_minimal import all_series, echo_ratio_test, pa_angle_classes


def _echo_p(result) -> float:
    if not result.hits:
        return 1.0
    return min(h.p_value for h in result.hits)


def _pa_p(result) -> float:
    return result.p_value if result else 1.0


@dataclass
class SourceJoint:
    source: str
    n_bursts: int
    echo_p: float
    pa_p: float
    pa_m: int
    fisher_p: float
    joint_score: float
    note: str


@dataclass
class FrbJointResult:
    sources: list[SourceJoint] = field(default_factory=list)
    permutation_p: float = 1.0
    n_with_both: int = 0
    verdict: str = ""
    data_limited: bool = False


def _fisher(p1: float, p2: float) -> float:
    p1, p2 = max(p1, 1e-300), max(p2, 1e-300)
    stat = -2.0 * (math.log(p1) + math.log(p2))
    from scipy.stats import chi2 as chi2_dist

    return float(chi2_dist.sf(stat, 4))


def run_frb_joint(seed: int = 0) -> FrbJointResult:
    res = FrbJointResult()
    series_list = all_series()

    if not series_list:
        res.data_limited = True
        res.verdict = "data_limited: no repeater series on disk (download FAST/Blinkverse per frb README)"
        return res

    rng = np.random.default_rng(seed)
    for s in series_list:
        if not s.available or len(s) < 20:
            continue
        fluence = s.energy if s.energy.size else s.fluence
        if fluence.size == 0 or not np.any(fluence > 0):
            continue
        echo = echo_ratio_test(s.source, fluence, s.mjd, cluster_dt_days=1.0, seed=seed)
        pa_res = None
        if s.pa_deg.size and np.sum(np.isfinite(s.pa_deg)) >= 10:
            pa_res = pa_angle_classes(s.pa_deg, m_values=(2, 4, 8), seed=seed)
        ep, pp = _echo_p(echo), _pa_p(pa_res)
        fisher = _fisher(ep, pp) if pa_res else 1.0
        res.sources.append(SourceJoint(
            source=s.source, n_bursts=len(s),
            echo_p=round(ep, 4), pa_p=round(pp, 4),
            pa_m=pa_res.best_m if pa_res else 0,
            fisher_p=round(fisher, 4),
            joint_score=round(-math.log10(max(fisher, 1e-300)), 2),
            note=echo.note if echo.n_pairs < 10 else "",
        ))

    if not res.sources:
        res.data_limited = True
        res.verdict = "data_limited: repeater files absent or too few bursts"
        return res

    # permutation: shuffle PA labels within sources, recompute Fisher
    both_sig = [x for x in res.sources if x.echo_p < 0.05 and x.pa_p < 0.05]
    res.n_with_both = len(both_sig)
    obs = sum(-math.log10(max(x.fisher_p, 1e-300)) for x in res.sources)
    null = []
    for _ in range(500):
        perm = 0.0
        for x in res.sources:
            ep = rng.uniform(0, 1)
            pp = rng.uniform(0, 1)
            perm += -math.log10(max(_fisher(ep, pp), 1e-300))
        null.append(perm)
    res.permutation_p = float((1 + sum(n >= obs for n in null)) / (len(null) + 1))

    if res.n_with_both >= 2 and res.permutation_p < 0.05:
        res.verdict = (
            f"JOINT HINT: {res.n_with_both} sources with echo+PA both p<0.05; "
            f"stacked Fisher permutation p={res.permutation_p:.3f} -- escalate, not a claim"
        )
    elif res.n_with_both >= 1:
        res.verdict = (
            f"single-source joint hint only ({res.n_with_both} source); "
            f"permutation p={res.permutation_p:.2f} -- not replicated"
        )
    else:
        res.verdict = (
            f"clean joint NULL: no source with simultaneous echo+PA excess "
            f"({len(res.sources)} sources tested, perm p={res.permutation_p:.2f})"
        )
    return res
