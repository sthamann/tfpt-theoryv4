"""Sessionisation + per-session tau series (the preregistered observable frame).

A *session* is a contiguous observing block of one source (gap > 0.2 d opens a
new one; FAST blocks are 1-4 h separated by >= 1 d, CHIME 'sessions' are single
transits).  Within a session the activity-onset proxy is the FIRST burst t0;
the cascade observable is tau_i = (t_i - t0) in seconds for the later bursts,
gated at tau >= 30x the dataset time resolution (preregistered).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .constants import ONE_PERIOD_DLN_T
from .data_io import DAY_S, BurstSeries

SESSION_GAP_D = 0.2
TAU_GATE_FACTOR = 30.0


@dataclass
class Session:
    dataset_id: str
    source: str
    t0_mjd: float
    n_bursts: int                 # all bursts in the session (incl. the onset burst)
    duration_s: float
    tau_s: np.ndarray             # gated taus (s) of bursts after onset, ascending
    tau_gate_s: float

    @property
    def n_used(self) -> int:
        return len(self.tau_s)

    @property
    def reach_periods(self) -> float:
        """Achieved ln(t) reach in comb periods (the PG.06 gate currency)."""
        if len(self.tau_s) < 2:
            return 0.0
        return float((math.log(self.tau_s[-1]) - math.log(self.tau_s[0]))
                     / ONE_PERIOD_DLN_T)


def split_sessions(series: BurstSeries, *, gap_days: float = SESSION_GAP_D) -> list[Session]:
    mjd = series.mjd
    if len(mjd) == 0:
        return []
    edges = np.where(np.diff(mjd) > gap_days)[0] + 1
    gate = TAU_GATE_FACTOR * series.time_resolution_s
    out: list[Session] = []
    for block in np.split(mjd, edges):
        if len(block) < 2:
            continue
        t0 = float(block[0])
        tau = (block[1:] - t0) * DAY_S
        tau = np.sort(tau[tau >= gate])
        out.append(Session(series.dataset_id, series.source, t0, len(block),
                           float((block[-1] - block[0]) * DAY_S), tau, gate))
    return out


def waiting_time_sequences(series: BurstSeries, *, gap_days: float = SESSION_GAP_D,
                           min_bursts: int = 10) -> list[np.ndarray]:
    """Per-session raw consecutive waiting times (s), for the RC.03 ladder.
    Intervals below 2x the time resolution are dropped (quantisation floor)."""
    mjd = series.mjd
    if len(mjd) == 0:
        return []
    edges = np.where(np.diff(mjd) > gap_days)[0] + 1
    floor = 2.0 * series.time_resolution_s
    out = []
    for block in np.split(mjd, edges):
        if len(block) < min_bursts:
            continue
        dt = np.diff(block) * DAY_S
        dt = dt[dt >= floor]
        if len(dt) >= 3:
            out.append(dt)
    return out
