"""Blind ladder recovery.

Input: a sorted list of peak positions with 1-sigma uncertainties. The detector
does NOT know which peak is m1 and does NOT see any single/multi-particle labels.

Procedure (preregistered in hypotheses/e8_ladder_bed_v1.yaml):
  * every peak is tried as the m1 anchor (initial scale s = p_j);
  * monotone injective DP matching of peaks to rungs with per-pair gate
    |p_i - s*r_k| <= GATE_SIGMA * sigma_i, lexicographic objective
    (max n_assigned, then min chi2);
  * physical gates, baked into the DP:
      - rung r1 (the lightest mass) must be assigned,
      - every peak below 2s - 2sigma must be assigned (no continua exist below
        the 2*m1 threshold in a pure one-particle ladder),
      - peaks above 2s may remain unassigned (multi-particle continua etc.);
  * two scale-refinement iterations (weighted LS on matched pairs, re-match);
  * score = chi2/dof with dof = n_assigned - 1 (scale fitted);
  * Monte-Carlo null: random 8-rung ladders with uniform-log ratios in the same
    dynamic range, identical detector; p = P[(n >= n_obs) & (chi2/dof <= obs)].

The DP uses a single float score n*SCORE_N - chi2 (chi2 is bounded by
n_rungs * GATE_SIGMA^2 = 72 << SCORE_N), which makes the lexicographic
(max n, min chi2) objective a plain max.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

GATE_SIGMA = 3.0          # per-pair pull gate
REFINE_ITERATIONS = 2
NULL_LADDERS = 5000
NULL_SEED = 0
SCORE_N = 1.0e4
NEG_INF = -1.0e18


@dataclass
class Recovery:
    ok: bool
    n_assigned: int = 0
    chi2: float = np.inf
    chi2_dof: float = np.inf
    scale: float = np.nan
    assignment: dict[int, int] = field(default_factory=dict)  # peak idx -> rung idx
    pulls: dict[int, float] = field(default_factory=dict)
    unassigned_peaks: list[int] = field(default_factory=list)
    missing_rungs: list[int] = field(default_factory=list)
    anchor_peak: int = -1


def _dp_match(peaks, sigmas, ladder, scale):
    """Gated monotone injective matching, maximizing (n_assigned, -chi2).

    Returns (n, chi2, assignment dict peak->rung) or (0, inf, {}) if infeasible."""
    n_p, n_r = len(peaks), len(ladder)
    pred = scale * ladder
    forced = peaks < 2.0 * scale - 2.0 * sigmas   # peaks that MUST be assigned
    pull = (peaks[:, None] - pred[None, :]) / sigmas[:, None]
    can = np.abs(pull) <= GATE_SIGMA
    chi = pull * pull

    dp = np.full((n_p + 1, n_r + 1), NEG_INF)
    par = np.zeros((n_p + 1, n_r + 1), dtype=np.int8)  # 0 none,1 skip_peak,2 skip_rung,3 match
    dp[0, 0] = 0.0
    for i in range(n_p + 1):
        for k in range(n_r + 1):
            best, op = dp[i, k], 0
            if i > 0 and not forced[i - 1] and dp[i - 1, k] > best:
                best, op = dp[i - 1, k], 1                       # skip peak
            if k >= 2 and dp[i, k - 1] > best:
                best, op = dp[i, k - 1], 2                       # skip rung (never rung 0)
            if i > 0 and k > 0 and can[i - 1, k - 1] and dp[i - 1, k - 1] > NEG_INF:
                cand = dp[i - 1, k - 1] + SCORE_N - chi[i - 1, k - 1]
                if cand > best:
                    best, op = cand, 3                           # match
            if op:
                dp[i, k], par[i, k] = best, op
    if dp[n_p, n_r] <= NEG_INF:
        return 0, np.inf, {}
    assignment = {}
    i, k = n_p, n_r
    while i > 0 or k > 0:
        op = par[i, k]
        if op == 3:
            assignment[i - 1] = k - 1
            i, k = i - 1, k - 1
        elif op == 1:
            i -= 1
        elif op == 2:
            k -= 1
        else:
            break
    n = len(assignment)
    chi2 = float(sum(chi[i, k] for i, k in assignment.items()))
    return n, chi2, assignment


def _refit_scale(peaks, sigmas, ladder, assignment):
    p = np.array([peaks[i] for i in assignment])
    s = np.array([sigmas[i] for i in assignment])
    r = np.array([ladder[k] for k in assignment.values()])
    return float(np.sum(p * r / s**2) / np.sum(r * r / s**2))


def recover(peaks, sigmas, ladder) -> Recovery:
    """Best blind recovery over all anchor hypotheses (deterministic)."""
    peaks = np.asarray(peaks, dtype=float)
    sigmas = np.asarray(sigmas, dtype=float)
    order = np.argsort(peaks)
    peaks, sigmas = peaks[order], sigmas[order]
    ladder = np.asarray(ladder, dtype=float)

    n_low_rungs = int(np.sum(ladder < 2.0 + GATE_SIGMA * np.max(sigmas) / peaks[0]))
    best = Recovery(ok=False)
    for j in range(len(peaks)):
        scale = peaks[j]
        # cheap anchor prefilter: more forced peaks below 2s than rungs below 2
        # can never be matched (monotone injective) -> skip
        if np.sum(peaks < 2.0 * scale - 2.0 * sigmas) > n_low_rungs:
            continue
        assignment = {}
        for _ in range(REFINE_ITERATIONS + 1):
            n, chi2, assignment = _dp_match(peaks, sigmas, ladder, scale)
            if not assignment:
                break
            new_scale = _refit_scale(peaks, sigmas, ladder, assignment)
            if not np.isfinite(new_scale) or abs(new_scale - scale) < 1e-12:
                break
            scale = new_scale
        if not assignment or 0 not in assignment.values():
            continue
        n = len(assignment)
        chi2 = float(sum(((peaks[i] - scale * ladder[k]) / sigmas[i]) ** 2
                         for i, k in assignment.items()))
        dof = max(n - 1, 1)
        cand = Recovery(
            ok=True, n_assigned=n, chi2=chi2, chi2_dof=chi2 / dof,
            scale=float(scale),
            assignment=dict(sorted(assignment.items())),
            pulls={i: float((peaks[i] - scale * ladder[k]) / sigmas[i])
                   for i, k in assignment.items()},
            unassigned_peaks=[i for i in range(len(peaks)) if i not in assignment],
            missing_rungs=[k for k in range(len(ladder))
                           if k not in assignment.values()],
            anchor_peak=j,
        )
        if (cand.n_assigned, -cand.chi2) > (best.n_assigned, -best.chi2):
            best = cand
    return best


def random_ladders(n_ladders: int, n_rungs: int, r_max: float,
                   seed: int = NULL_SEED) -> np.ndarray:
    """r1 = 1; remaining rungs i.i.d. uniform in log-space on [1, r_max], sorted."""
    rng = np.random.default_rng(seed)
    logs = rng.uniform(0.0, np.log(r_max), size=(n_ladders, n_rungs - 1))
    ladders = np.exp(np.sort(logs, axis=1))
    return np.hstack([np.ones((n_ladders, 1)), ladders])


def mc_pvalue(peaks, sigmas, observed: Recovery, r_max: float,
              n_ladders: int = NULL_LADDERS, seed: int = NULL_SEED) -> dict:
    """p = P[random ladder recovers (n >= n_obs) AND (chi2/dof <= obs)]."""
    if not observed.ok:
        return {"p_value": 1.0, "n_null": 0, "n_as_good": 0}
    ladders = random_ladders(n_ladders, 8, r_max, seed)
    n_good = 0
    for lad in ladders:
        rec = recover(peaks, sigmas, lad)
        if rec.ok and rec.n_assigned >= observed.n_assigned \
                and rec.chi2_dof <= observed.chi2_dof:
            n_good += 1
    # conservative (add-one) estimator
    p = (n_good + 1) / (n_ladders + 1)
    return {"p_value": float(p), "n_null": int(n_ladders), "n_as_good": int(n_good)}
