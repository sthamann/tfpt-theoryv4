"""KC.02 -- circular-polarization HANDEDNESS alternation (the deck-visible observable).

Topological motivation (exploratory, unforced): the Z2 deck is an ORIENTATION FLIP.
Linear polarization angle is defined mod pi (deck-invariant) and |V|/I is even -- every
polarization test run so far (FRB.04/06/08) was structurally blind to the flip.  The
only deck-visible polarization observable is the SIGN of the circular polarization.
Deck reading: consecutive kernel steps flip the handedness.

Primary: alternation fraction A = P(s_i != s_{i+1}) over consecutive significant-
handedness pairs within sessions, vs within-session sign permutation (one-sided,
excess alternation).  Secondary: tooth-gated pairs (tau ratio on (3/2)^6 +/- 0.10 dex).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .data import Bursts, session_taus, sessions

N_NULL = 2000
TOL_DEX = 0.10
L326 = 6 * math.log10(1.5)


@dataclass
class KC02Result:
    source: str
    n_significant: int
    n_pairs: int
    alternation: float
    null_mean: float
    p_value: float
    net_handedness: float          # mean sign (balance check)
    n_tooth_pairs: int
    tooth_alternation: float
    tooth_p: float
    verdict: str = ""


def _alt_frac(signs: list[np.ndarray]) -> tuple[float, int]:
    """(alternation fraction over consecutive pairs, number of pairs)."""
    flips = tot = 0
    for s in signs:
        if len(s) >= 2:
            flips += int(np.sum(s[:-1] != s[1:]))
            tot += len(s) - 1
    return (flips / tot if tot else float("nan"), tot)


def run(b: Bursts, *, seed: int = 0) -> KC02Result:
    rng = np.random.default_rng(seed)
    per_session_signs: list[np.ndarray] = []
    tooth_pairs: list[tuple[float, float]] = []
    all_signs: list[float] = []
    for idx in sessions(b):
        s = b.vsign[idx]
        tau = session_taus(b, idx)
        ok = ~np.isnan(s) & (tau >= 0)
        s_ok, tau_ok = s[ok], tau[ok]
        if len(s_ok) >= 2:
            per_session_signs.append(s_ok)
            all_signs.extend(s_ok)
            pos = tau_ok > 0.5
            ts, ss = tau_ok[pos], s_ok[pos]
            for i in range(len(ts) - 1):
                if abs(math.log10(ts[i + 1] / ts[i]) - L326) < TOL_DEX:
                    tooth_pairs.append((ss[i], ss[i + 1]))

    a_obs, n_pairs = _alt_frac(per_session_signs)
    null = np.empty(N_NULL)
    for k in range(N_NULL):
        null[k] = _alt_frac([rng.permutation(s) for s in per_session_signs])[0]
    p = float((1 + np.sum(null >= a_obs)) / (N_NULL + 1))

    # tooth-gated secondary (binomial-style permutation on the gated pairs)
    n_tooth = len(tooth_pairs)
    if n_tooth >= 5:
        flips = sum(1 for a, c in tooth_pairs if a != c)
        t_obs = flips / n_tooth
        base = np.array([a for a, _ in tooth_pairs] + [c for _, c in tooth_pairs])
        tn = np.empty(N_NULL)
        for k in range(N_NULL):
            pick = rng.choice(base, size=2 * n_tooth)
            tn[k] = np.mean(pick[:n_tooth] != pick[n_tooth:])
        t_p = float((1 + np.sum(tn >= t_obs)) / (N_NULL + 1))
    else:
        t_obs, t_p = float("nan"), 1.0

    res = KC02Result(b.source, len(all_signs), n_pairs, round(float(a_obs), 4),
                     round(float(null.mean()), 4), round(p, 4),
                     round(float(np.mean(all_signs)), 3), n_tooth,
                     round(float(t_obs), 4) if n_tooth >= 5 else float("nan"),
                     round(t_p, 4))
    res.verdict = ("HANDEDNESS ALTERNATION EXCESS -> escalate-only"
                   if (p < 0.05 and a_obs > null.mean()) else
                   f"NULL -- alternation {a_obs:.3f} vs shuffle {null.mean():.3f} "
                   f"(p={p:.3f}); tooth-gated ({n_tooth} pairs) p={t_p:.3f}")
    return res
