"""PG.04 — the post-glitch *recovery* channel (Yu+2013 Q / tau_d).

Two `problem_1.txt` tests, now data-backed by the Yu+2013 recovery table:

* **PG.04a (Q clustering, §A).** Does the healing fraction ``Q`` pile up at the
  ``phi0`` multiples ``{phi0, 2 phi0, 4 phi0, 8 phi0, 1-phi0}``?  Calibrated against
  a KDE bootstrap (population-controlled) **and** a uniform null (conservative max).
* **PG.04b (tau_d ladder / multi-timescale DSI, §B+§D).** For glitches resolved into
  several exponential components, do the decay timescales form a *geometric ladder*
  at a kernel ratio ``(3/2)^k``?  This is the **dynamical** reading of the kernel: a
  geometric rate ladder is exactly what produces log-periodic (discrete-scale-
  invariant) relaxation (see ``dsi.py``).  Null: shuffle ``tau_d`` across components.

Honest by construction: N is small and the fits are heterogeneous (literature
compilation), so the channel is typed conservatively.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .catalog import RecoveryRecord, recovery_by_glitch
from .constants import RECOVERY_BEND, RECOVERY_WALL, candidate_Q_clusters, kernel_log_ratios


@dataclass
class QClusterResult:
    n: int
    targets: dict[str, float]
    tol: float
    frac_on_target: float
    null_frac_kde: float
    null_frac_uniform: float
    p_value: float          # conservative max over the two nulls
    verdict: str


def _frac_near(values: np.ndarray, targets: np.ndarray, tol: float) -> float:
    if len(values) == 0:
        return 0.0
    d = np.abs(values[:, None] - targets[None, :]).min(axis=1)
    return float(np.mean(d <= tol))


def q_cluster_test(records: list[RecoveryRecord], *, tol: float = 0.025,
                   n_surrogate: int = 4000, seed: int = 0) -> QClusterResult:
    q = np.array([r.Q for r in records if r.Q is not None], dtype=float)
    q = q[(q > 0) & (q <= 1.1)]                 # physical recovery fractions
    targets = candidate_Q_clusters()
    tvals = np.array(list(targets.values()))
    obs = _frac_near(q, tvals, tol)

    rng = np.random.default_rng(seed)
    # KDE (population-controlled) null
    from scipy import stats
    kde = stats.gaussian_kde(q, bw_method="silverman")
    null_kde = np.empty(n_surrogate)
    null_uni = np.empty(n_surrogate)
    lo, hi = float(q.min()), float(q.max())
    for i in range(n_surrogate):
        s = np.clip(kde.resample(len(q), seed=rng).ravel(), 1e-4, 1.1)
        null_kde[i] = _frac_near(s, tvals, tol)
        u = rng.uniform(lo, hi, size=len(q))
        null_uni[i] = _frac_near(u, tvals, tol)
    p_kde = float((1 + np.sum(null_kde >= obs)) / (n_surrogate + 1))
    p_uni = float((1 + np.sum(null_uni >= obs)) / (n_surrogate + 1))
    p = max(p_kde, p_uni)
    verdict = (f"Q clusters at phi0-multiples (frac={obs:.2f}, p={p:.3f})" if p < 0.05
               else f"Q not clustered at phi0-multiples (frac={obs:.2f} vs null "
                    f"{null_kde.mean():.2f}/{null_uni.mean():.2f}, p={p:.3f})")
    return QClusterResult(len(q), targets, tol, obs, float(null_kde.mean()),
                          float(null_uni.mean()), p, verdict)


@dataclass
class TauLadderResult:
    n_glitches: int          # multi-component glitches used
    n_ratios: int
    teeth_dex: list[float]
    tol_dex: float
    frac_on_comb: float
    null_frac: float
    p_value: float
    ratios: list[float]      # the observed tau_{i+1}/tau_i ratios (for the record)
    verdict: str


def tau_component_ladder(records: list[RecoveryRecord], *, tol_dex: float = 0.05,
                         n_shuffle: int = 5000, seed: int = 0) -> TauLadderResult:
    groups = recovery_by_glitch(records)
    teeth = np.array(list(kernel_log_ratios().values()))
    per_glitch: list[list[float]] = []
    obs_ratios: list[float] = []
    for comps in groups.values():
        taus = [c.tau_d for c in comps if c.tau_d and c.tau_d > 0]
        if len(taus) < 2:
            continue
        taus = sorted(taus)
        lr = [abs(np.log10(taus[i + 1] / taus[i])) for i in range(len(taus) - 1)]
        per_glitch.append(lr)
        obs_ratios.extend([taus[i + 1] / taus[i] for i in range(len(taus) - 1)])
    pooled = np.array([v for lst in per_glitch for v in lst], dtype=float)
    obs = _frac_near(pooled, teeth, tol_dex) if len(pooled) else 0.0

    # null: pool ALL tau_d, reshuffle into the same per-glitch multiplicities
    all_logtau = np.log10(np.array([c.tau_d for c in records
                                    if c.tau_d and c.tau_d > 0]))
    sizes = [len(lst) + 1 for lst in per_glitch]   # n components per multi-glitch
    rng = np.random.default_rng(seed)
    null = np.empty(n_shuffle)
    for k in range(n_shuffle):
        draw = rng.choice(all_logtau, size=sum(sizes), replace=True)
        idx = 0
        shuffled: list[float] = []
        for s in sizes:
            chunk = np.sort(draw[idx:idx + s])
            idx += s
            shuffled.extend(np.abs(np.diff(chunk)).tolist())
        null[k] = _frac_near(np.array(shuffled), teeth, tol_dex)
    p = float((1 + np.sum(null >= obs)) / (n_shuffle + 1))
    verdict = (f"tau_d components form the kernel ladder (frac={obs:.2f}, p={p:.3f})"
               if p < 0.05 else
               f"tau_d component ratios consistent with shuffle (frac={obs:.2f} vs "
               f"null {null.mean():.2f}, p={p:.3f}) -- no kernel ladder")
    return TauLadderResult(len(per_glitch), len(pooled), teeth.tolist(), tol_dex,
                           obs, float(null.mean()), p,
                           [round(r, 3) for r in obs_ratios], verdict)


@dataclass
class BendWallResult:
    bend: float                  # ln3/ln(3/2) = 2.7095
    n_two_comp: int              # glitches resolved into exactly 2 decay modes
    ratios: list[float]          # tau_long/tau_short for those
    frac_near_bend: float        # fraction within 15% of the bend (log scale)
    null_frac: float
    p_value: float               # shuffle null
    comp_counts: dict[int, int]  # decay-component multiplicity per glitch (wall test)
    n_wall_exceed: int           # glitches needing >= N_fam decay modes
    verdict: str


def bend_wall_test(records: list[RecoveryRecord], *, tol_log: float = 0.061,
                   n_shuffle: int = 5000, seed: int = 0) -> BendWallResult:
    """PG.04c -- the *correct* discrete->dynamic candidates (v124): for 2-component
    recoveries, the decay-timescale ratio should equal the det'-clean **bend**
    ``ln3/ln(3/2)=2.7095`` (the two clock rates 6ln(3/2), 6ln3); and the **wall** at
    ``n=N_fam=3`` predicts at most 2 decaying modes.  ``tol_log`` ~ log10(1.15) = 15%."""
    groups = recovery_by_glitch(records)
    ratios: list[float] = []
    comp_counts: dict[int, int] = {}
    all_logtau = np.log10(np.array([c.tau_d for c in records if c.tau_d and c.tau_d > 0]))
    for comps in groups.values():
        taus = sorted([c.tau_d for c in comps if c.tau_d and c.tau_d > 0])
        comp_counts[len(taus)] = comp_counts.get(len(taus), 0) + 1
        if len(taus) == 2:
            ratios.append(taus[1] / taus[0])
    log_bend = np.log10(RECOVERY_BEND)
    obs = (float(np.mean(np.abs(np.log10(np.array(ratios)) - log_bend) <= tol_log))
           if ratios else 0.0)
    rng = np.random.default_rng(seed)
    null = np.empty(n_shuffle)
    for k in range(n_shuffle):
        draw = rng.choice(all_logtau, size=(len(ratios), 2))
        r = np.abs(np.diff(np.sort(draw, axis=1), axis=1).ravel())
        null[k] = float(np.mean(np.abs(r - log_bend) <= tol_log)) if len(r) else 0.0
    p = float((1 + np.sum(null >= obs)) / (n_shuffle + 1))
    n_exceed = sum(v for c, v in comp_counts.items() if c >= RECOVERY_WALL)
    verdict = (
        f"2-mode bend: {obs:.2f} of {len(ratios)} ratios near {RECOVERY_BEND:.3f} "
        f"(null {null.mean():.2f}, p={p:.3f}; {'on bend' if p < 0.05 else 'null'}); "
        f"wall: {n_exceed} glitch(es) need >= {RECOVERY_WALL} decay modes "
        f"({'tension' if n_exceed > 2 else 'consistent with <=2-mode wall'})")
    return BendWallResult(RECOVERY_BEND, len(ratios), [round(r, 3) for r in ratios],
                          obs, float(null.mean()), p, dict(sorted(comp_counts.items())),
                          n_exceed, verdict)
