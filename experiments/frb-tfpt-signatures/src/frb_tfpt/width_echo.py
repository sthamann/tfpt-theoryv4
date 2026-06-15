"""FRB.07 (NEW, exploratory) -- width-relaxation echo.

A temporal-domain analogue of FRB.02: if a discharge relaxes, the *duration* of
consecutive bursts/sub-bursts in a session might step by the unpowered relaxation
ratio. Width is a timescale (neither energy nor amplitude), so it reads the
**sub-burst step channel {2/3, 1/3}** (and inverses) -- chosen up front to avoid
the channel-mismatch error that bit FRB.02.

Null: within-session and local-block shuffles of the widths (same machinery as
FRB.02); BH q-values across the 4 (target, sign) cells.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .data_io import RepeaterSeries
from .echo_ratio import _bh_qvalues, _session_logratios_indexed, _surrogate_logratios
from .recovery_kernel import ONE_THIRD, TWO_THIRDS

STEP_TARGETS = {"2/3": TWO_THIRDS, "1/3": ONE_THIRD}


@dataclass
class WidthEchoResult:
    source: str
    available: bool
    n_pairs: int
    n_sessions: int
    targets: dict
    significant: list
    verdict: str


def width_step_echo(series: RepeaterSeries, half_window_dex: float = 0.10,
                    n_surrogate: int = 800, q_threshold: float = 0.05,
                    seed: int = 0) -> WidthEchoResult:
    if not series.available or series.width.size == 0:
        return WidthEchoResult(series.source, False, 0, 0, {}, [], "data-limited: no widths")
    val = series.width
    sess = series.session_id if series.session_id.size else np.zeros(len(series.mjd))
    mjd = series.mjd
    lr, _ = _session_logratios_indexed(val, sess, mjd)
    n_pairs = len(lr)
    n_sessions = int(len(np.unique(sess)))
    if n_pairs < 20:
        return WidthEchoResult(series.source, False, n_pairs, n_sessions, {}, [],
                               f"too few within-session width pairs ({n_pairs})")

    rng = np.random.default_rng(seed)
    nulls = ["within_session", "local_block"]
    surr = {}
    for m in nulls:
        rows = [_surrogate_logratios(val, sess, mjd, m, rng) for _ in range(n_surrogate)]
        rows = [r for r in rows if len(r) == n_pairs]
        surr[m] = np.vstack(rows) if rows else np.empty((0, n_pairs))

    names, pvals, recs = [], [], {}
    for tname, tv in STEP_TARGETS.items():
        for sign, lt, label in ((+1, np.log10(tv), tname), (-1, -np.log10(tv), f"{tname}^-1")):
            obs = int(np.sum(np.abs(lr - lt) <= half_window_dex))
            pmax, enr = 0.0, 1.0
            for m in nulls:
                if surr[m].shape[0] == 0:
                    continue
                nh = (np.abs(surr[m] - lt) <= half_window_dex).sum(axis=1)
                p = float((1 + np.sum(nh >= obs)) / (len(nh) + 1))
                if p > pmax:
                    pmax, enr = p, obs / (float(nh.mean()) or 1e-9)
            recs[label] = {"ratio": tv if sign > 0 else 1.0 / tv,
                           "enrichment": round(enr, 2), "p": round(pmax, 4)}
            names.append(label); pvals.append(pmax)
    for label, q in zip(names, _bh_qvalues(pvals)):
        recs[label]["q"] = round(q, 4)
    sig = [n for n in names if recs[n]["q"] < q_threshold and recs[n]["enrichment"] > 1.2]
    verdict = (f"width-step excess at {sig}" if sig
               else f"clean null (no BH q<{q_threshold} width-step excess)")
    return WidthEchoResult(series.source, True, n_pairs, n_sessions, recs, sig, verdict)
