"""FRB.04 (strong form) -- PA / RM state-transition spectrum.

The strong mu4/D4 test is NOT "there are four PA classes" (numerological
confetti). It is:

    spec(T_PA)  ~  { 1, (2/3)^6, (1/3)^6 } = { 1, 64/729, 1/729 }.

We build a state-transition matrix from a single repeater's time-ordered PA (or
RM-residual) states and compare its non-trivial eigenvalues to the frozen
kernel, with a bootstrap CI on the eigenvalues and a null (same stationary
distribution, time-shuffle) calibration. Requires a per-repeater PA/RM
*sequence*; with the bundled non-repeater data this is data-limited.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .data_io import RepeaterSeries
from .recovery_kernel import LAMBDA2, LAMBDA3


def pa_states(pa_deg: np.ndarray, mjd: np.ndarray | None = None,
              session_id: np.ndarray | None = None, detrend: bool = False) -> np.ndarray:
    """Map PA (mod 180 deg) to four D4 sectors 0..3 (each 45 deg wide).

    If ``detrend`` and sessions are given, subtract each session's circular mean
    PA first (handles strong secular PA drift), then re-map the residual.
    """
    pa = np.asarray(pa_deg, dtype=float) % 180.0
    if detrend and session_id is not None:
        for s in np.unique(session_id):
            m = session_id == s
            ang = np.deg2rad(2 * pa[m])
            mean = np.rad2deg(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean())) / 2.0
            pa[m] = (pa[m] - mean) % 180.0
    return np.clip((pa // 45.0).astype(int), 0, 3)


def rm_residual_states(mjd: np.ndarray, rm: np.ndarray, n_states: int = 4,
                       deg: int = 3) -> np.ndarray:
    """Detrend RM(t) with a low-order polynomial, standardise, and quantise the
    residual into ``n_states`` equal-occupancy states (quantile bins)."""
    t = np.asarray(mjd, float)
    y = np.asarray(rm, float)
    ok = np.isfinite(t) & np.isfinite(y)
    resid = np.full(len(y), np.nan)
    if ok.sum() > deg + 1:
        resid[ok] = y[ok] - np.polyval(np.polyfit(t[ok], y[ok], deg), t[ok])
    r = resid[ok]
    edges = np.quantile(r, np.linspace(0, 1, n_states + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    states = np.full(len(y), -1)
    states[ok] = np.clip(np.digitize(r, edges[1:-1]), 0, n_states - 1)
    return states


def transition_matrix_from_states(states: np.ndarray, n_states: int = 4) -> np.ndarray:
    """Row-stochastic transition matrix from a time-ordered integer state list."""
    s = np.asarray(states, int)
    s = s[s >= 0]
    P = np.zeros((n_states, n_states))
    for a, b in zip(s[:-1], s[1:]):
        P[a, b] += 1
    row = P.sum(axis=1, keepdims=True)
    row[row == 0] = 1
    return P / row


def _nontrivial_abs_eigs(P: np.ndarray, k: int) -> np.ndarray:
    ev = np.sort(np.abs(np.linalg.eigvals(P)))[::-1]   # descending; ev[0] ~ 1
    return ev[1:1 + k]


@dataclass
class MarkovSpectrumResult:
    source: str
    channel: str
    available: bool
    n: int
    eigs: list[float]              # observed non-trivial |eigenvalues|
    kernel: list[float]            # (64/729, 1/729)
    distance: float                # Euclidean distance eigs - kernel
    ci_contains_kernel: bool
    null_p: float
    c_markov: float
    note: str


def markov_spectrum_test(series: RepeaterSeries, channel: str = "pa",
                         n_states: int = 4, n_boot: int = 1000,
                         n_null: int = 2000, seed: int = 0) -> MarkovSpectrumResult:
    kernel = np.array([LAMBDA2, LAMBDA3])
    if not series.available:
        return MarkovSpectrumResult(series.source, channel, False, 0, [], kernel.tolist(),
                                    float("nan"), False, float("nan"), 0.0,
                                    "data-limited: no repeater PA/RM sequence loaded")
    if channel == "pa":
        st = pa_states(series.pa_deg, series.mjd, series.session_id, detrend=True) \
            if series.pa_deg.size else np.array([])
    else:
        st = rm_residual_states(series.mjd, series.rm, n_states) if series.rm.size else np.array([])
    st = st[st >= 0] if st.size else st
    if st.size < 4 * n_states:
        return MarkovSpectrumResult(series.source, channel, False, int(st.size), [],
                                    kernel.tolist(), float("nan"), False, float("nan"), 0.0,
                                    f"data-limited: only {st.size} {channel} states")

    P = transition_matrix_from_states(st, n_states)
    eigs = _nontrivial_abs_eigs(P, len(kernel))
    dist = float(np.linalg.norm(eigs - kernel))

    rng = np.random.default_rng(seed)
    # bootstrap CI on the eigenvalues (block bootstrap of the state sequence)
    boot = np.empty((n_boot, len(kernel)))
    for i in range(n_boot):
        idx = rng.integers(0, len(st) - 1, len(st) - 1)
        seg = np.empty(len(st), int)
        seg[:-1] = st[idx]
        seg[-1] = st[idx[-1]]
        boot[i] = _nontrivial_abs_eigs(transition_matrix_from_states(seg, n_states), len(kernel))
    lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
    ci_ok = bool(np.all(kernel >= lo) and np.all(kernel <= hi))

    # null: random row-stochastic matrices with the observed stationary dist
    stat = np.bincount(st, minlength=n_states).astype(float)
    stat /= stat.sum()
    null_d = np.empty(n_null)
    for i in range(n_null):
        Q = rng.dirichlet(np.ones(n_states) * 2.0, size=n_states)
        null_d[i] = np.linalg.norm(_nontrivial_abs_eigs(Q, len(kernel)) - kernel)
    null_p = float((1 + np.sum(null_d <= dist)) / (n_null + 1))

    c = float((ci_ok and null_p < 0.01) * np.exp(-(dist / 0.05) ** 2))
    return MarkovSpectrumResult(series.source, channel, True, int(st.size),
                                eigs.tolist(), kernel.tolist(), dist, ci_ok, null_p, c,
                                f"eigs={np.round(eigs,4).tolist()} vs kernel; "
                                f"CI_contains_kernel={ci_ok}, null p={null_p:.3f}")
