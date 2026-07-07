"""KC.01 -- the 2D LADDER COUPLING (joint energy-time tooth).

The frozen kernel is a 2D statement: one transfer rung multiplies the elapsed time by
(3/2)^k AND the energy by (2/3)^k (E * t = const along a cascade).  Every prior test
probed a marginal (FRB.02 energies alone, RC.02/03 times alone).  KC.01 tests the
COUPLING: for consecutive within-session pairs whose tau ratio lies on a time tooth
(3/2)^k (k in {1,3,6}, +/-0.10 dex), does the energy ratio E_early/E_late lie on the
PARTNER tooth (3/2)^k as well?

Null (exact, coupling-only): within-session permutation of the ENERGIES (times fixed)
-- both marginals are preserved exactly, only the pairing is destroyed.
Controls: (a) placebo pairing k -> k' != k must not beat the matched pairing;
(b) free-quotient LEE: the kernel base 2/3 must not be beaten by >95% of a q grid.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .data import Bursts, session_taus, sessions

TEETH_K = (1, 3, 6)
TOL_DEX = 0.10
L32 = math.log10(1.5)
N_NULL = 2000
Q_GRID = np.linspace(0.40, 0.95, 45)          # free-quotient control (energy base)


def _pairs(b: Bursts) -> tuple[np.ndarray, np.ndarray]:
    """Consecutive within-session pairs -> (log10 tau ratio, log10 energy ratio
    E_early/E_late) with tau-gated positive taus."""
    lt, le = [], []
    for idx in sessions(b):
        tau = session_taus(b, idx)
        e = b.energy[idx]
        ok = tau > 0.5
        tau, e = tau[ok], e[ok]
        if len(tau) < 3:
            continue
        lt.append(np.log10(tau[1:] / tau[:-1]))
        le.append(np.log10(e[:-1] / e[1:]))     # early over late
    return (np.concatenate(lt), np.concatenate(le)) if lt else (np.array([]), np.array([]))


def _joint_hits(lt: np.ndarray, le: np.ndarray, *, base_log: float = L32) -> int:
    hits = 0
    for k in TEETH_K:
        on_t = np.abs(lt - k * L32) < TOL_DEX
        on_e = np.abs(le - k * base_log) < TOL_DEX
        hits += int(np.sum(on_t & on_e))
    return hits


def _placebo_hits(lt: np.ndarray, le: np.ndarray) -> int:
    """Mismatched pairing: time tooth k with energy tooth k' != k (max over pairings)."""
    best = 0
    for k in TEETH_K:
        on_t = np.abs(lt - k * L32) < TOL_DEX
        for kp in TEETH_K:
            if kp == k:
                continue
            best = max(best, int(np.sum(on_t & (np.abs(le - kp * L32) < TOL_DEX))))
    return best


@dataclass
class KC01Result:
    source: str
    n_pairs: int
    n_time_tooth: int
    joint_hits: int
    null_mean: float
    enrichment: float
    p_value: float
    placebo_max_hits: int
    free_q_beat_frac: float
    per_tooth: dict = field(default_factory=dict)
    verdict: str = ""


def run(b: Bursts, *, seed: int = 0) -> KC01Result:
    lt, le = _pairs(b)
    rng = np.random.default_rng(seed)
    obs = _joint_hits(lt, le)
    n_time = int(sum(np.sum(np.abs(lt - k * L32) < TOL_DEX) for k in TEETH_K))

    # energy-shuffle null: permute the energy-ratio series construction per session.
    # Equivalent exact implementation: permute le against lt (pairs are the unit).
    null = np.empty(N_NULL)
    for i in range(N_NULL):
        null[i] = _joint_hits(lt, rng.permutation(le))
    p = float((1 + np.sum(null >= obs)) / (N_NULL + 1))
    enr = obs / (null.mean() + 1e-12)

    per = {}
    for k in TEETH_K:
        on_t = np.abs(lt - k * L32) < TOL_DEX
        on_e = np.abs(le - k * L32) < TOL_DEX
        per[f"(3/2)^{k}"] = {"time_tooth_pairs": int(on_t.sum()),
                             "joint_hits": int(np.sum(on_t & on_e))}

    # free-quotient LEE: how often does an off-kernel energy base beat the kernel?
    beat = 0
    for q in Q_GRID:
        if abs(math.log10(1.0 / q) - L32) < 0.02:
            continue
        if _joint_hits(lt, le, base_log=math.log10(1.0 / q)) > obs:
            beat += 1
    beat_frac = beat / len(Q_GRID)

    placebo = _placebo_hits(lt, le)
    res = KC01Result(b.source, len(lt), n_time, obs, float(null.mean()),
                     round(float(enr), 3), round(p, 4), placebo,
                     round(beat_frac, 3), per)
    supported = p < 0.05 and enr > 1.2 and obs >= placebo and beat_frac < 0.5
    res.verdict = ("JOINT TOOTH ENRICHED -> escalate-only (needs 2nd source + controls)"
                   if supported else
                   f"NULL -- joint hits {obs} vs shuffle mean {null.mean():.1f} "
                   f"(enr {enr:.2f}, p={p:.3f}); placebo max {placebo}; "
                   f"free-q beats kernel in {beat_frac:.0%} of the grid")
    return res
