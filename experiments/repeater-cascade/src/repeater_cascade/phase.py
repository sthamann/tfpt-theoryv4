"""RC.04 -- per-source comb-PHASE coherence at the frozen kernel omega (exploratory).

The RC.02 comb search is phase-INSENSITIVE: each session contributes only its Rayleigh
power at omega, so a comb whose phase differs per session is treated identically to a
persistent one.  TFPT's stronger "persistent boundary clock" reading says more: if the
seam marks are persistent properties of the source, the log-comb phase (relative to each
activity onset t0) should be STABLE per source across its sessions,

    R_k(t) = A_k [1 + eps cos(omega ln tau + phi_source)]   vs   phi_event,k free.

Test (frozen omega = 2.583, no free frequency): per gate-passing session the empirical
phase  phi_k = arg sum_i exp(i omega ln tau_i);  the cross-session concentration
R_obs = |mean_k exp(i phi_k)|  is ranked against surrogate sessions (the SAME
rate-preserving redraw as RC.02, which erases any true comb phase but keeps each
session's envelope/window -- so shared-window artefacts are calibrated away by
construction).

Verdict semantics: a small p would be escalate-only (never a claim); a null BOUNDS the
persistent-clock reading while leaving the transient (per-event phase) reading intact.
Note the complementary channels already run elsewhere: the PG.07 Vela 2016-2024 stack
and the crust-cooling superposed-epoch stack are t0-aligned = phase-COHERENT stacks
(both null, p = 0.53 / 0.45).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .comb import MIN_BURSTS_USED, surrogate_lntau
from .constants import OMEGA, REACH_GATE_PERIODS
from .data_io import load_all
from .sessions import Session, split_sessions

N_SURROGATE = 2000
RESULTS = Path(__file__).resolve().parents[2] / "results"


def session_phase(u: np.ndarray, omega: float = OMEGA) -> tuple[float, float]:
    """Empirical comb phase and resultant length of one session: the argument and
    modulus of (1/n) sum_i exp(i omega u_i), u = ln tau."""
    z = np.exp(1j * omega * u).mean()
    return float(np.angle(z)), float(np.abs(z))


def phase_concentration(phases: list[float]) -> float:
    """Cross-session resultant length R = |mean_k exp(i phi_k)| (unweighted)."""
    return float(np.abs(np.mean(np.exp(1j * np.array(phases)))))


@dataclass
class SourcePhaseResult:
    source: str
    n_sessions: int
    phases_deg: list[float]
    per_session_resultant: list[float]
    r_obs: float = float("nan")
    p_surrogate: float = float("nan")
    coherent: bool = False


@dataclass
class RC04Result:
    omega: float
    n_surrogate: int
    sources: list[SourcePhaseResult] = field(default_factory=list)
    verdict: str = ""


def _gate_passing_by_source() -> dict[str, list[Session]]:
    by_src: dict[str, list[Session]] = {}
    for series in load_all():
        for s in split_sessions(series):
            if s.n_used >= MIN_BURSTS_USED and s.reach_periods > REACH_GATE_PERIODS:
                by_src.setdefault(s.source, []).append(s)
    return {src: ss for src, ss in by_src.items() if len(ss) >= 2}


def analyze(*, seed: int = 0) -> RC04Result:
    res = RC04Result(OMEGA, N_SURROGATE)
    by_src = _gate_passing_by_source()
    for src, sessions in sorted(by_src.items()):
        us = [np.log(s.tau_s) for s in sessions]
        obs = [session_phase(u) for u in us]
        phases = [p for p, _ in obs]
        r_obs = phase_concentration(phases)

        # surrogate null: redraw each session from its smooth rate profile (erases any
        # true comb phase; keeps window/envelope), recompute the cross-session R
        rng = np.random.default_rng(seed)
        r_sur = np.empty(N_SURROGATE)
        for k in range(N_SURROGATE):
            ph_k = [session_phase(surrogate_lntau(u, rng))[0] for u in us]
            r_sur[k] = phase_concentration(ph_k)
        p = float((1 + np.sum(r_sur >= r_obs)) / (N_SURROGATE + 1))

        res.sources.append(SourcePhaseResult(
            src, len(sessions),
            [round(math.degrees(p_), 1) for p_ in phases],
            [round(r, 4) for _, r in obs],
            round(r_obs, 4), round(p, 4), bool(p < 0.05)))

    hits = [s for s in res.sources if s.coherent]
    if not res.sources:
        res.verdict = "no source has >= 2 gate-passing sessions -- not testable."
    elif hits:
        res.verdict = (
            f"PHASE COHERENCE candidate in {[s.source for s in hits]} -> ESCALATE ONLY "
            "(independent cross-check; a persistent per-source comb phase would still be a "
            "universal-DSI style coincidence in the magnetar engine, never TFPT confirmation).")
    else:
        detail = "; ".join(f"{s.source}: R={s.r_obs} over {s.n_sessions} sessions "
                           f"(p={s.p_surrogate})" for s in res.sources)
        res.verdict = (
            f"NULL -- the per-source comb phase at the frozen omega={OMEGA:.3f} is NOT more "
            f"concentrated across sessions than the rate-preserving surrogate null ({detail}). "
            "Honest power scope: a per-session phase estimate has noise resultant ~1/sqrt(n) "
            "(~0.07-0.15 here) vs a coherent comb contribution ~eps/2, so this bounds only "
            "PERSISTENT combs with eps >~ 2/sqrt(n) ~ 0.15-0.3 -- the same amplitude wall as "
            "RC.02; at the predicted eps~1.7% the phases are noise-dominated by construction. "
            "The transient per-event reading is untouched. Consistent with the t0-aligned "
            "(phase-coherent) stacks already run elsewhere: PG.07 Vela 2016-2024 p=0.53, "
            "crust-cooling superposed-epoch p=0.45.")
    return res


def report(*, seed: int = 0) -> RC04Result:
    print("=" * 78)
    print(f"RC.04 per-source comb-phase coherence (frozen omega = {OMEGA:.3f}; "
          f"{N_SURROGATE} surrogates)")
    print("=" * 78)
    res = analyze(seed=seed)
    for s in res.sources:
        print(f"\n  [{s.source}] {s.n_sessions} gate-passing sessions")
        print(f"    per-session phases (deg): {s.phases_deg}")
        print(f"    cross-session R = {s.r_obs}   surrogate p = {s.p_surrogate}   "
              f"coherent = {s.coherent}")
    print(f"\n-> {res.verdict}")
    RESULTS.mkdir(exist_ok=True)
    out = {"omega": res.omega, "n_surrogate": res.n_surrogate,
           "sources": [vars(s) for s in res.sources], "verdict": res.verdict}
    (RESULTS / "rc04_phase_coherence.json").write_text(json.dumps(out, indent=2),
                                                       encoding="utf-8")
    print(f"\nWrote {RESULTS / 'rc04_phase_coherence.json'}")
    return res


if __name__ == "__main__":
    report()
