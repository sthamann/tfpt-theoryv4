"""FO.03 -- log-comb in the medium-state clock tau_mod = cumsum |dRM| (S14).

The first FRB comb test with a NAMED clock: if the session cascade is a recovery,
it ticks in the medium's own state path (total-variation of RM within a session),
not in observer time. All previous S2b nulls ran on t_observer.

Per session (>= 30 finite-RM bursts): tau_mod_i = cumulative |RM_i - RM_{i-1}|;
noise floor = median per-burst RM error of the session; reach gate >= 2.8 comb
periods in ln tau_mod evaluated BEFORE the comb statistic. Rayleigh power at the
frozen omega = 2.5830; nulls: increment permutation (2000) + off-kernel rank
(120 omegas, surrogate-standardised). Session p = max of the two; Fisher combine.
"""

from __future__ import annotations

import numpy as np
from scipy import stats

from . import constants as c
from .data import PolCatalog, sessions

MIN_RM_BURSTS = 30
N_PERM = 2000
N_STD_SURR = 300
OMEGA_GRID = np.exp(np.linspace(np.log(0.6), np.log(6.0), 120))


def _rayleigh_z(ln_tau: np.ndarray, omega: float | np.ndarray) -> np.ndarray:
    ph = np.multiply.outer(np.atleast_1d(omega), ln_tau)
    r = np.abs(np.exp(1j * ph).mean(axis=-1))
    return ln_tau.size * r ** 2


def _session_clock(rm: np.ndarray, rm_err: np.ndarray
                   ) -> tuple[np.ndarray, float] | None:
    ok = np.isfinite(rm)
    if ok.sum() < MIN_RM_BURSTS:
        return None
    r = rm[ok]
    inc = np.abs(np.diff(r))
    floor = float(np.nanmedian(rm_err[ok]))
    return inc, floor


def _kept_ln_tau(inc: np.ndarray, floor: float) -> np.ndarray:
    tau = np.cumsum(inc)
    tau = tau[tau >= max(floor, 1e-9)]
    return np.log(tau)


def run(cat: PolCatalog, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    per_session, gated_out = [], 0
    for idx in sessions(cat.mjd):
        sc = _session_clock(cat.rm[idx], cat.rm_err[idx])
        if sc is None:
            continue
        inc, floor = sc
        ln_tau = _kept_ln_tau(inc, floor)
        if ln_tau.size < 10:
            continue
        reach = (ln_tau[-1] - ln_tau[0]) / c.LN_LAMBDA
        if reach < c.REACH_GATE_PERIODS:
            gated_out += 1
            continue

        z_obs = float(_rayleigh_z(ln_tau, c.OMEGA)[0])

        # permutation null on the increments (rebuild the clock, re-apply floor)
        z_null = np.empty(N_PERM)
        for i in range(N_PERM):
            lt = _kept_ln_tau(rng.permutation(inc), floor)
            z_null[i] = _rayleigh_z(lt, c.OMEGA)[0] if lt.size >= 5 else 0.0
        p_perm = float((1 + np.sum(z_null >= z_obs)) / (N_PERM + 1))

        # off-kernel rank: surrogate-standardised zeta across the omega grid
        z_grid_obs = _rayleigh_z(ln_tau, OMEGA_GRID)
        zg = np.empty((N_STD_SURR, OMEGA_GRID.size))
        for i in range(N_STD_SURR):
            lt = _kept_ln_tau(rng.permutation(inc), floor)
            zg[i] = _rayleigh_z(lt, OMEGA_GRID) if lt.size >= 5 else 0.0
        zeta = (z_grid_obs - zg.mean(0)) / np.where(zg.std(0) < 1e-12, 1.0, zg.std(0))
        k = int(np.argmin(np.abs(OMEGA_GRID - c.OMEGA)))
        p_rank = float((1 + np.sum(zeta >= zeta[k])) / (OMEGA_GRID.size + 1))

        per_session.append({
            "mjd0": round(float(cat.mjd[idx][0]), 3),
            "n_rm": int(np.isfinite(cat.rm[idx]).sum()),
            "n_phases": int(ln_tau.size),
            "reach_periods": round(float(reach), 2),
            "floor_rad_m2": round(floor, 2),
            "rayleigh_z": round(z_obs, 3),
            "p_perm": p_perm,
            "p_rank": p_rank,
            "p_session": max(p_perm, p_rank),
        })

    if per_session:
        ps = np.array([s["p_session"] for s in per_session])
        chi2 = float(-2 * np.log(np.clip(ps, 1e-12, 1)).sum())
        p_fisher = float(stats.chi2.sf(chi2, 2 * ps.size))
        verdict = "hint_flag" if p_fisher < 0.05 else "null"
        note = ("comb at detectable amplitude absent in the state clock; the "
                "predicted epsilon = 1.7% stays behind the amplitude wall (data_limited)"
                if verdict == "null" else "escalate-only")
    else:
        p_fisher, verdict = None, "data_limited"
        note = "no session passes the 2.8-period reach gate in ln tau_mod"

    return {
        "axis": "FO.03_state_clock_comb",
        "omega": round(c.OMEGA, 4),
        "n_gate_passing_sessions": len(per_session),
        "n_gated_out": gated_out,
        "sessions": per_session,
        "fisher_p": p_fisher,
        "verdict": verdict,
        "note": note,
    }
