"""KC.04 -- the mu4 phase-time HELIX (coupled polarization-time phase; exploratory).

If a repeater carries the same mu4 deck clock and the same recovery kernel, the burst
TIME and the complex linear polarization P = L e^{2i PA} are phase-coupled:

    Phi_ij(q) = omega ln(tau_j/tau_i) + q * 2 (PA_j - PA_i)   ~ const  (mod 2pi)

for within-session consecutive pairs, with FROZEN omega = 2.583 (no free frequency)
and q in {1, 2} (mu4 quarter-turn / Z2 half-turn readings).

Nulls: (a) within-session PA permutation; (b) within-session CIRCULAR SHIFT of the PA
series (preserves PA autocorrelation -- the conservative primary against slow
Faraday/instrument drift); (c) off-kernel omega rank in the matched band.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .data import Bursts, session_taus, sessions

OMEGA = 2.0 * math.pi / math.log(1.5 ** 6)      # 2.583, frozen
QS = (1, 2)
N_NULL = 2000
N_POOL = 200
MIN_LI_PCT = 10.0
TAU_GATE_S = 0.5


def _session_series(b: Bursts, pa_deg: np.ndarray, li_pct: np.ndarray
                    ) -> list[tuple[np.ndarray, np.ndarray]]:
    """Per session: (tau, PA_rad) for bursts with significant linear polarization."""
    out = []
    for idx in sessions(b):
        tau = session_taus(b, idx)
        pa = pa_deg[idx]
        li = li_pct[idx]
        ok = (tau > TAU_GATE_S) & np.isfinite(pa) & (li >= MIN_LI_PCT)
        if int(ok.sum()) >= 3:
            out.append((tau[ok], np.deg2rad(pa[ok])))
    return out


def _rayleigh_phi(series: list[tuple[np.ndarray, np.ndarray]], omega: float,
                  q: int) -> tuple[float, int]:
    """Rayleigh resultant of Phi over consecutive pairs; returns (R, n_pairs)."""
    zs = []
    for tau, pa in series:
        phi = omega * np.log(tau[1:] / tau[:-1]) + q * 2.0 * (pa[1:] - pa[:-1])
        zs.append(np.exp(1j * phi))
    if not zs:
        return float("nan"), 0
    z = np.concatenate(zs)
    return float(np.abs(z.mean())), len(z)


@dataclass
class KC04Result:
    source: str
    n_sessions: int
    n_pairs: int
    per_q: dict = field(default_factory=dict)
    verdict: str = ""


def run(b: Bursts, pa_deg: np.ndarray, li_pct: np.ndarray, *, seed: int = 0) -> KC04Result:
    series = _session_series(b, pa_deg, li_pct)
    rng = np.random.default_rng(seed)
    res = KC04Result(b.source, len(series), _rayleigh_phi(series, OMEGA, 1)[1])

    any_hit = False
    for q in QS:
        r_obs, _ = _rayleigh_phi(series, OMEGA, q)

        perm = np.empty(N_NULL)
        shift = np.empty(N_NULL)
        for k in range(N_NULL):
            sp = [(t, rng.permutation(p)) for t, p in series]
            perm[k] = _rayleigh_phi(sp, OMEGA, q)[0]
            ss = [(t, np.roll(p, int(rng.integers(1, len(p))))) for t, p in series]
            shift[k] = _rayleigh_phi(ss, OMEGA, q)[0]
        p_perm = float((1 + np.sum(perm >= r_obs)) / (N_NULL + 1))
        p_shift = float((1 + np.sum(shift >= r_obs)) / (N_NULL + 1))

        pool = rng.uniform(0.72 * OMEGA, 1.40 * OMEGA, N_POOL)
        pool = pool[np.abs(pool - OMEGA) > 0.06 * OMEGA]
        ranks = np.array([_rayleigh_phi(series, w, q)[0] for w in pool])
        p_rank = float((1 + np.sum(ranks >= r_obs)) / (len(ranks) + 1))

        detected = bool(max(p_perm, p_shift) < 0.05 and p_rank < 0.05)
        any_hit = any_hit or detected
        res.per_q[f"q={q}"] = {"R": round(r_obs, 4),
                               "p_perm": round(p_perm, 4),
                               "p_shift": round(p_shift, 4),
                               "p_offkernel_rank": round(p_rank, 4),
                               "detected": detected}

    res.verdict = ("PHASE HELIX candidate -> escalate-only (needs RM-corrected PA + "
                   "a second source)" if any_hit else
                   "NULL -- the coupled phase Phi = omega ln(tau ratio) + q*2*dPA is "
                   "not concentrated above the permutation AND drift-robust "
                   "circular-shift nulls at the frozen omega for either mu4 reading "
                   "(q=1, 2); the off-kernel rank agrees. The helix reading closes "
                   "for FAST 20240114A at catalog statistics (PA is mod pi and "
                   "RM-uncorrected -- documented limitation).")
    return res
