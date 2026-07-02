"""RC.03 -- waiting-time ratio ladders on the kernel teeth (PG.02/PG.03 mirror).

Consecutive within-session waiting-time ratios |log10(dt_{i+1}/dt_i)| are tested
for pile-up near the frozen tooth set {log 3/2, log (3/2)^3, log (3/2)^6}; the
tooth set IS the step/amplitude/energy semantics battery (the FRB
energy<->amplitude lesson is built in, exactly as in the pulsar PG.02/PG.03).

Null: within-session shuffle of the RAW waiting intervals, then RECOMPUTE the
consecutive ratios (permuting precomputed ratios is a tautology -- the comb
fraction is order-invariant; see pulsar-glitch-recovery/ratios.py).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .constants import LADDER_TEETH_DEX, LADDER_TOL_DEX


def _log_ratios(dt: np.ndarray) -> np.ndarray:
    return np.abs(np.log10(dt[1:] / dt[:-1]))


def _tooth_frac(log_ratios: np.ndarray, teeth: np.ndarray, tol: float) -> float:
    if len(log_ratios) == 0:
        return 0.0
    d = np.abs(log_ratios[:, None] - teeth[None, :]).min(axis=1)
    return float(np.mean(d <= tol))


@dataclass
class LadderResult:
    source: str
    n_sessions: int
    n_ratios: int
    frac_on_comb: float
    null_mean: float
    p_value: float
    verdict: str


def ladder_test(source: str, sequences: list[np.ndarray], *, n_shuffle: int = 2000,
                seed: int = 0) -> LadderResult:
    """RC.03 for one source: pool sessions, shuffle within session."""
    teeth = np.asarray(LADDER_TEETH_DEX)
    pooled = np.concatenate([_log_ratios(dt) for dt in sequences]) if sequences \
        else np.array([])
    obs = _tooth_frac(pooled, teeth, LADDER_TOL_DEX)

    rng = np.random.default_rng(seed)
    null = np.empty(n_shuffle)
    for k in range(n_shuffle):
        shuf = [_log_ratios(rng.permutation(dt)) for dt in sequences]
        null[k] = _tooth_frac(np.concatenate(shuf) if shuf else np.array([]),
                              teeth, LADDER_TOL_DEX)
    null_mean = float(null.mean())
    p = float((1 + np.sum(null >= obs)) / (n_shuffle + 1))
    verdict = (f"waiting ladder ON kernel comb (frac={obs:.3f} vs null {null_mean:.3f}, "
               f"p={p:.3f})" if p < 0.05 else
               f"consistent with shuffle (frac={obs:.3f} vs null {null_mean:.3f}, "
               f"p={p:.3f}) -- no kernel comb")
    return LadderResult(source, len(sequences), int(len(pooled)), obs, null_mean, p,
                        verdict)
