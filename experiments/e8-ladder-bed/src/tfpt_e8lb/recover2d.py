"""Blind 2D (2DCS) ladder recovery -- amendment v2 of the e8-ladder-bed.

Input: a list of 2D peak coordinates (omega_tau, omega_t) with one isotropic
1-sigma uncertainty per peak, folded to the positive quadrant. The detector
does NOT know which frequency is m1 and sees no pathway labels.

Preregistered in hypotheses/e8_ladder_bed_v1.yaml, amendment_v2 block
(frozen 2026-07-21, BEFORE any 2D recovery run):

  * catalog for scale s over ladder rungs r_a (families; F4 sums NOT scored):
      F1 diagonal    (s*r_a, s*r_a)          rung set {a}
      F2 cross       (s*r_a, s*r_b), a != b  rung set {a, b}
      F3 difference  (s*r_a, s*|r_a - r_b|)  rung set {a, b}
    F3 is the channel by which rungs above a low-pass window (m7/m8 in the
    0.6 THz CoNb2O6 window) can appear inside the window.
  * scale hypotheses: every folded axis value of every peak tried as s*r_k
    for every rung k (deduplicated) -- blind analog of the v1 anchor scan;
  * matching: injective peaks -> catalog entries, two-axis gate
    |pull| <= 3 sigma on BOTH axes, chi2_peak = pull_tau^2 + pull_t^2,
    lexicographic objective (max n_matched, then min chi2) via a padded
    linear-sum assignment; two scale-refinement iterations;
  * physical gates: rung 1 must be covered; every peak with BOTH folded
    coordinates below 2s - 2sigma must be matched;
  * PRIMARY score: n_rungs = |union of rungs of matched entries|; secondary
    n_matched, chi2/dof with dof = 2*n_matched - 1 (scale fitted); selection
    over hypotheses lexicographic (n_rungs, n_matched, -chi2);
  * MC null: random 8-rung ladders (identical generator to v1), identical
    catalog machinery; p = P[(n_rungs >= n_obs) & (chi2/dof <= obs)], add-one.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import linear_sum_assignment

from .recover import NULL_SEED, random_ladders

GATE_SIGMA = 3.0
REFINE_ITERATIONS = 2
NULL_LADDERS_2D = 5000
SCORE_N = 1.0e4          # match bonus (chi2 per peak bounded by 2*GATE^2 = 18)
BIG = 1.0e9              # forbidden-assignment cost


@dataclass
class Catalog2D:
    xy: np.ndarray                # (M, 2) unit-scale coordinates
    rungs: list[frozenset]        # rung indices (0-based) referenced per entry
    family: list[str]             # F1 / F2 / F3
    label: list[str]              # human-readable, e.g. "F3(6,|6-7|)"


def build_catalog(ladder) -> Catalog2D:
    """F1 u F2 u F3 catalog (120 entries for an 8-rung ladder)."""
    r = np.asarray(ladder, dtype=float)
    n = len(r)
    xy, rungs, family, label = [], [], [], []
    for a in range(n):
        xy.append((r[a], r[a]))
        rungs.append(frozenset({a}))
        family.append("F1")
        label.append(f"F1({a+1},{a+1})")
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            xy.append((r[a], r[b]))
            rungs.append(frozenset({a, b}))
            family.append("F2")
            label.append(f"F2({a+1},{b+1})")
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            xy.append((r[a], abs(r[a] - r[b])))
            rungs.append(frozenset({a, b}))
            family.append("F3")
            label.append(f"F3({a+1},|{a+1}-{b+1}|)")
    return Catalog2D(np.asarray(xy), rungs, family, label)


@dataclass
class Recovery2D:
    ok: bool
    n_rungs: int = 0
    rungs_covered: list[int] = field(default_factory=list)   # 1-based
    n_matched: int = 0
    chi2: float = np.inf
    chi2_dof: float = np.inf
    scale: float = np.nan
    assignment: dict[int, int] = field(default_factory=dict)  # peak -> cat idx
    pulls: dict[int, tuple[float, float]] = field(default_factory=dict)
    unmatched_peaks: list[int] = field(default_factory=list)
    missing_rungs: list[int] = field(default_factory=list)    # 1-based


def _match(peaks, sigmas, cat: Catalog2D, scale):
    """Gated injective peak->catalog matching, maximizing (n_matched, -chi2).

    Returns (assignment dict, chi2) or None if a forced peak cannot be
    matched (hypothesis rejected). Catalog entries with no peak inside the
    gate are dropped before the assignment solve (exact: they can never be
    matched), which keeps the linear-sum problem small."""
    n_p = len(peaks)
    pred = scale * cat.xy                                        # (M, 2)
    pull = (peaks[:, None, :] - pred[None, :, :]) / sigmas[:, None, None]
    ok = np.all(np.abs(pull) <= GATE_SIGMA, axis=2)              # (N, M)
    forced = np.all(peaks < 2.0 * scale - 2.0 * sigmas[:, None], axis=1)

    if np.any(forced & ~ok.any(axis=1)):
        return None                           # forced peak unmatchable
    active = np.flatnonzero(ok.any(axis=0))   # catalog entries in reach
    if len(active) == 0:
        return {}, 0.0
    chi = np.sum(pull[:, active, :] ** 2, axis=2)                # (N, A)

    cost = np.where(ok[:, active], chi - SCORE_N, BIG)
    pad = np.where(forced[:, None], BIG, 0.0) * np.ones((1, n_p))
    C = np.hstack([cost, pad])
    rows, cols = linear_sum_assignment(C)

    assignment: dict[int, int] = {}
    chi2 = 0.0
    for i, j in zip(rows, cols):
        if C[i, j] >= BIG / 2:
            return None                       # forced peak left unmatched
        if j < len(active):
            assignment[i] = int(active[j])
            chi2 += float(chi[i, j])
    if any(forced[i] and i not in assignment for i in range(n_p)):
        return None
    return assignment, chi2


def _refit_scale(peaks, sigmas, cat: Catalog2D, assignment):
    """Weighted LS scale over BOTH axes of all matched pairs."""
    num = den = 0.0
    for i, j in assignment.items():
        w = 1.0 / sigmas[i] ** 2
        for ax in (0, 1):
            num += w * peaks[i, ax] * cat.xy[j, ax]
            den += w * cat.xy[j, ax] ** 2
    return num / den if den > 0 else np.nan


def _coverage(cat: Catalog2D, assignment) -> set:
    cov: set = set()
    for j in assignment.values():
        cov |= cat.rungs[j]
    return cov


# Pruning gate for the coverage upper bound, deliberately 2x looser than the
# matching gate so that scale drift during the (small) refinement steps cannot
# push a hypothesis past a bound computed at the initial scale -- pruning can
# only skip hypotheses whose 6-sigma-gated rung-coverage union is already
# below the requested minimum (conservative direction; used for the MC null
# scan only, the observed recovery always runs unpruned with min_n_rungs=0).
BOUND_GATE_FACTOR = 2.0


def _coverage_bound(peaks, sigmas, cat: Catalog2D, scale) -> int | None:
    """Upper bound on reachable rung coverage; None if a forced peak is dead."""
    pred = scale * cat.xy
    pull = (peaks[:, None, :] - pred[None, :, :]) / sigmas[:, None, None]
    ok = np.all(np.abs(pull) <= BOUND_GATE_FACTOR * GATE_SIGMA, axis=2)
    forced = np.all(peaks < 2.0 * scale - 2.0 * sigmas[:, None], axis=1)
    if np.any(forced & ~ok.any(axis=1)):
        return None
    cov: set = set()
    for j in np.flatnonzero(ok.any(axis=0)):
        cov |= cat.rungs[j]
    return len(cov)


def recover2d(peaks_xy, sigmas, ladder, min_n_rungs: int = 0) -> Recovery2D:
    """Best blind 2D recovery over all scale hypotheses (deterministic).

    min_n_rungs > 0 (MC-null scans only): hypotheses whose loose-gated
    coverage upper bound is below the target are skipped."""
    peaks = np.abs(np.asarray(peaks_xy, dtype=float)).reshape(-1, 2)  # fold
    sigmas = np.asarray(sigmas, dtype=float)
    ladder = np.asarray(ladder, dtype=float)
    cat = build_catalog(ladder)
    n_rungs_total = len(ladder)

    hyps: set = set()
    for v in np.unique(peaks.ravel()):
        for r in ladder:
            s = v / r
            if s > 0:
                hyps.add(round(s, 12))

    best = Recovery2D(ok=False)
    best_key = (-1, -1, -np.inf)
    for s0 in sorted(hyps):
        if min_n_rungs > 0:
            bound = _coverage_bound(peaks, sigmas, cat, s0)
            if bound is None or bound < min_n_rungs:
                continue
        scale = s0
        m = None
        for _ in range(REFINE_ITERATIONS + 1):
            m = _match(peaks, sigmas, cat, scale)
            if m is None:
                break
            new_scale = _refit_scale(peaks, sigmas, cat, m[0])
            if not np.isfinite(new_scale) or abs(new_scale - scale) < 1e-12:
                break
            scale = new_scale
        if m is None:
            continue
        assignment, _ = m
        if not assignment:
            continue
        cov = _coverage(cat, assignment)
        if 0 not in cov:                      # rung-1 gate
            continue
        chi2 = float(sum(
            np.sum(((peaks[i] - scale * cat.xy[j]) / sigmas[i]) ** 2)
            for i, j in assignment.items()))
        n_m = len(assignment)
        key = (len(cov), n_m, -chi2)
        if key > best_key:
            best_key = key
            dof = max(2 * n_m - 1, 1)
            best = Recovery2D(
                ok=True, n_rungs=len(cov),
                rungs_covered=sorted(k + 1 for k in cov),
                n_matched=n_m, chi2=chi2, chi2_dof=chi2 / dof,
                scale=float(scale),
                assignment=dict(sorted(assignment.items())),
                pulls={i: tuple(
                    float(x) for x in (peaks[i] - scale * cat.xy[j]) / sigmas[i])
                    for i, j in assignment.items()},
                unmatched_peaks=[i for i in range(len(peaks))
                                 if i not in assignment],
                missing_rungs=[k + 1 for k in range(n_rungs_total)
                               if k not in cov],
            )
    return best


def mc_pvalue2d(peaks_xy, sigmas, observed: Recovery2D, r_max: float,
                n_ladders: int = NULL_LADDERS_2D, seed: int = NULL_SEED,
                early_stop_threshold: int | None = None) -> dict:
    """v2.1 corrected null region (see hypotheses YAML amendment_v2_1):

        p = P[(n_rungs >= obs) AND (n_matched >= obs) AND (chi2/dof <= obs)]

    i.e. a null ladder counts only if it is as good as the observed recovery
    in EVERY component of the detector's lexicographic objective. The v2
    coverage-only count is reported alongside (n_as_good_coverage_only).

    Null recoveries use the coverage-bound pruning (min_n_rungs = observed
    coverage): a null ladder whose loose-gated bound cannot reach the observed
    coverage can never count as 'as good' (machine-checked in tests).

    early_stop_threshold (control batteries only): stop once n_good reaches
    the threshold -- the binary decision 'p < P_VALIDATED' is then already
    False; the returned p_value is a valid >= threshold value, NOT the
    full-scan estimate (flagged early_stopped)."""
    if not observed.ok:
        return {"p_value": 1.0, "n_null": 0, "n_as_good": 0,
                "n_as_good_coverage_only": 0, "early_stopped": False}
    ladders = random_ladders(n_ladders, 8, r_max, seed)
    n_good = n_good_cov = 0
    n_scanned = 0
    early = False
    for lad in ladders:
        n_scanned += 1
        rec = recover2d(peaks_xy, sigmas, lad, min_n_rungs=observed.n_rungs)
        if rec.ok and rec.n_rungs >= observed.n_rungs \
                and rec.chi2_dof <= observed.chi2_dof:
            n_good_cov += 1
            if rec.n_matched >= observed.n_matched:
                n_good += 1
                if early_stop_threshold is not None \
                        and n_good >= early_stop_threshold:
                    early = True
                    break
    p = (n_good + 1) / (n_scanned + 1)
    return {"p_value": float(p), "n_null": int(n_scanned),
            "n_as_good": int(n_good),
            "n_as_good_coverage_only": int(n_good_cov),
            "early_stopped": early}
