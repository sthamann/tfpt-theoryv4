"""RC.01 -- the walled two-mode clock template on the per-session burst RATE.

The resummed recovery clock (v124) says a single recovery is a two-mode +
protected-floor curve with the FROZEN bend

    R(t) = w0 + w1 exp(-r t) + w2 exp(-BEND * r t),   BEND = ln3/ln(3/2) = 2.7095,

(weights >= 0, r > 0 profiled).  This is the cascade version of quantum-testbed
QT.04 applied to a repeater's burst-rate decay after activity onset.

HONEST FRAME: the GW Stage-2 identifiability analysis machine-checked that this
bend is DEGENERATE within one monotone recovery (two-mode R^2 gain ~1e-3 even
noise-free), so RC.01 is a consistency channel, not the discriminating axis --
it is run because the preregistration demands the template be confronted, and
because the free-bend placebo quantifies exactly how non-special the frozen
bend is in this data.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import nnls

from .comb import surrogate_lntau
from .constants import BEND
from .sessions import Session

MIN_BURSTS_RATE = 60
BIN_COUNT = 10                    # equal-count bins -> stable Poisson rate points
N_SURROGATE = 150
R_GRID_N = 36
PLACEBO_BENDS = np.linspace(1.5, 6.0, 19)


def rate_curve(tau_s: np.ndarray, *, k: int = BIN_COUNT
               ) -> tuple[np.ndarray, np.ndarray]:
    """Equal-count binned rate estimate: t_mid (geometric), rate = k/dt (s^-1)."""
    n_bins = len(tau_s) // k
    if n_bins < 4:
        return np.array([]), np.array([])
    edges = tau_s[:: k][: n_bins + 1]
    if len(edges) < n_bins + 1:
        edges = np.append(edges, tau_s[-1])
    t_mid, rate = [], []
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        if hi <= lo:
            continue
        t_mid.append(float(np.sqrt(lo * hi)))
        rate.append(k / (hi - lo))
    return np.array(t_mid), np.array(rate)


def _fit_template(t: np.ndarray, y: np.ndarray, bend: float | None
                  ) -> tuple[float, float]:
    """Profile r on a log grid; NNLS the weights. bend=None -> single-exp null
    model M0 (w0 + w1 e^{-rt}); else two-mode M1 with the given bend.
    Returns (best SSE, best r)."""
    r_grid = np.geomspace(0.3 / t.max(), 30.0 / t.min(), R_GRID_N)
    best, best_r = np.inf, float("nan")
    for r in r_grid:
        cols = [np.ones_like(t), np.exp(-r * t)]
        if bend is not None:
            cols.append(np.exp(-bend * r * t))
        X = np.column_stack(cols)
        w, _ = nnls(X, y)
        sse = float(np.sum((y - X @ w) ** 2))
        if sse < best:
            best, best_r = sse, float(r)
    return best, best_r


def delta_r2(t: np.ndarray, y: np.ndarray, bend: float = BEND) -> float:
    """R^2 gain of the frozen two-mode template over the single-exp+floor null."""
    sst = float(np.sum((y - y.mean()) ** 2)) or 1e-12
    sse0, _ = _fit_template(t, y, None)
    sse1, _ = _fit_template(t, y, bend)
    return max(0.0, (sse0 - sse1) / sst)


@dataclass
class ClockSessionResult:
    dataset_id: str
    source: str
    t0_mjd: float
    n_used: int
    applicable: bool
    delta_r2_frozen: float = float("nan")
    p_surrogate: float = float("nan")       # P(surrogate delta_r2 >= observed)
    placebo_max_delta_r2: float = float("nan")
    frozen_beats_placebos: bool = False


def clock_test_session(sess: Session, *, n_surrogate: int = N_SURROGATE,
                       seed: int = 0) -> ClockSessionResult:
    res = ClockSessionResult(sess.dataset_id, sess.source, sess.t0_mjd,
                             sess.n_used, sess.n_used >= MIN_BURSTS_RATE)
    if not res.applicable:
        return res
    t, y = rate_curve(sess.tau_s)
    if len(t) < 5:
        res.applicable = False
        return res
    obs = delta_r2(t, y)
    res.delta_r2_frozen = obs

    placebo = [delta_r2(t, y, bend=b) for b in PLACEBO_BENDS
               if abs(b - BEND) > 0.15]
    res.placebo_max_delta_r2 = float(max(placebo))
    res.frozen_beats_placebos = bool(obs > res.placebo_max_delta_r2)

    rng = np.random.default_rng(seed + int(sess.t0_mjd))
    u = np.log(sess.tau_s)
    null = []
    for _ in range(n_surrogate):
        ts = np.sort(np.exp(surrogate_lntau(u, rng)))
        tt, yy = rate_curve(ts)
        if len(tt) >= 5:
            null.append(delta_r2(tt, yy))
    null_arr = np.asarray(null)
    res.p_surrogate = float((1 + np.sum(null_arr >= obs)) / (len(null_arr) + 1))
    return res
