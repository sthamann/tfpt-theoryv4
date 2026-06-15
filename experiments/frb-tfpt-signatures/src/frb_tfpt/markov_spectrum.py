"""FRB.04 (strong form) -- PA / RM state-transition spectrum.

The strong mu4/D4 test is NOT "there are four PA classes" (numerological
confetti). It is:

    spec(T_PA)  ~  { 1, (2/3)^6, (1/3)^6 } = { 1, 64/729, 1/729 }.

We build a state-transition matrix from a single repeater's time-ordered PA (or
RM-residual) states, compare its non-trivial eigenvalues to the frozen kernel
with a moving-block bootstrap CI, and calibrate against the **four preregistered
nulls** (same-stationary-distribution Markov, time-shuffle, block-shuffle,
AR(1)-drift). The conservative overall p is the max over those four; the v2
exploratory variant passes ``kernel=(2/3,1/3)``.

The AR(1)-drift null is decisive for RM: if a smooth autocorrelated drift
reproduces the observed proximity to a kernel, the "match" is just environmental
relaxation, not a discrete boundary spectrum.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.signal import lfilter

from .data_io import RepeaterSeries
from .recovery_kernel import LAMBDA2, LAMBDA3

YAML_NULLS = ("stationary_markov", "time_shuffle", "block_shuffle", "ar1_drift")


def pa_states(pa_deg: np.ndarray, mjd: np.ndarray | None = None,
              session_id: np.ndarray | None = None, detrend: bool = False) -> np.ndarray:
    """Map PA (mod 180 deg) to four D4 sectors 0..3 (each 45 deg wide)."""
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
    """Detrend RM(t) with a low-order polynomial and quantise the residual into
    ``n_states`` equal-occupancy states."""
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
    """Row-stochastic transition matrix from a time-ordered integer state list
    (vectorised via ``np.add.at``)."""
    s = np.asarray(states, int)
    s = s[s >= 0]
    P = np.zeros((n_states, n_states))
    if len(s) >= 2:
        np.add.at(P, (s[:-1], s[1:]), 1.0)
    row = P.sum(axis=1, keepdims=True)
    row[row == 0] = 1
    return P / row


def _nontrivial_abs_eigs(P: np.ndarray, k: int) -> np.ndarray:
    ev = np.sort(np.abs(np.linalg.eigvals(P)))[::-1]   # descending; ev[0] ~ 1
    return ev[1:1 + k]


def _ordered_channel(series: RepeaterSeries, channel: str, n_states: int):
    """Return the time-ordered, finite (states, continuous) arrays for a channel."""
    order = np.argsort(series.mjd)
    mjd = series.mjd[order]
    if channel == "pa":
        if series.pa_deg.size == 0:
            return np.array([], int), np.array([])
        pa = series.pa_deg[order]
        sess = series.session_id[order] if series.session_id.size else np.zeros_like(pa)
        ok = np.isfinite(pa)
        pa, sess = pa[ok] % 180.0, sess[ok]
        for s in np.unique(sess):
            m = sess == s
            ang = np.deg2rad(2 * pa[m])
            mean = np.rad2deg(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean())) / 2.0
            pa[m] = (pa[m] - mean) % 180.0
        return np.clip((pa // 45.0).astype(int), 0, n_states - 1), pa
    if series.rm.size == 0:
        return np.array([], int), np.array([])
    rm = series.rm[order]
    ok = np.isfinite(mjd) & np.isfinite(rm)
    t, y = mjd[ok], rm[ok]
    resid = (y - np.polyval(np.polyfit(t, y, 3), t)) if len(y) > 5 else (y - y.mean())
    edges = np.quantile(resid, np.linspace(0, 1, n_states + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    return np.clip(np.digitize(resid, edges[1:-1]), 0, n_states - 1), resid


# --- null generators -------------------------------------------------------
def _block_shuffle(states, block, rng):
    n = len(states)
    nb = int(np.ceil(n / block))
    blocks = [states[i * block:(i + 1) * block] for i in range(nb)]
    rng.shuffle(blocks)
    return np.concatenate(blocks)[:n]


def _reversible_chain(pi, rng):
    """A random reversible Markov chain with the given stationary distribution
    (Metropolis construction with a random symmetric proposal)."""
    n = len(pi)
    g = rng.uniform(0, 1, (n, n))
    g = (g + g.T) / (4.0 * n)         # symmetric, small enough to keep P_ii > 0
    np.fill_diagonal(g, 0.0)
    P = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j and pi[i] > 0:
                P[i, j] = g[i, j] * min(1.0, pi[j] / pi[i])
        P[i, i] = 1.0 - P[i].sum()
    return P


def _ar1_states(cont, n_states, rng):
    x = cont[np.isfinite(cont)]
    n = len(x)
    rho = 0.0
    if n >= 8:
        xc = x - x.mean()
        d = float(xc[:-1] @ xc[:-1])
        rho = float(xc[:-1] @ xc[1:] / d) if d > 0 else 0.0
    rho = float(np.clip(rho, -0.99, 0.99))
    sim = lfilter([np.sqrt(1.0 - rho**2)], [1.0, -rho], rng.standard_normal(n))
    edges = np.quantile(sim, np.linspace(0, 1, n_states + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    return np.clip(np.digitize(sim, edges[1:-1]), 0, n_states - 1)


def _null_pvalue(mode, states, cont, n_states, kernel, dist_obs, n_null, rng, block):
    k = len(kernel)
    pi = np.bincount(states, minlength=n_states).astype(float)
    pi /= pi.sum()
    nd = np.empty(n_null)
    for i in range(n_null):
        if mode == "stationary_markov":
            Q = _reversible_chain(pi, rng)
        elif mode == "time_shuffle":
            Q = transition_matrix_from_states(rng.permutation(states), n_states)
        elif mode == "block_shuffle":
            Q = transition_matrix_from_states(_block_shuffle(states, block, rng), n_states)
        elif mode == "ar1_drift":
            Q = transition_matrix_from_states(_ar1_states(cont, n_states, rng), n_states)
        elif mode == "dirichlet":
            Q = rng.dirichlet(np.ones(n_states) * 2.0, size=n_states)
        else:
            raise ValueError(mode)
        nd[i] = np.linalg.norm(_nontrivial_abs_eigs(Q, k) - kernel)
    return float((1 + np.sum(nd <= dist_obs)) / (n_null + 1))


@dataclass
class MarkovSpectrumResult:
    source: str
    channel: str
    available: bool
    n: int
    eigs: list[float]
    kernel: list[float]
    distance: float
    ci_lo: list[float] = field(default_factory=list)
    ci_hi: list[float] = field(default_factory=list)
    ci_contains_kernel: bool = False
    null_pvals: dict = field(default_factory=dict)   # per-null p-values
    null_p: float = float("nan")                     # conservative overall (max over YAML nulls)
    c_markov: float = 0.0
    note: str = ""


def markov_spectrum_test(series: RepeaterSeries, channel: str = "pa",
                         n_states: int = 4, n_boot: int = 800,
                         n_null: int = 1000, seed: int = 0, block: int = 25,
                         kernel: tuple[float, float] | None = None) -> MarkovSpectrumResult:
    """PA/RM transition spectrum vs the kernel, with a moving-block bootstrap CI
    and the four preregistered nulls (+ a Dirichlet diagnostic)."""
    kernel = np.array(kernel if kernel is not None else (LAMBDA2, LAMBDA3))
    if not series.available:
        return MarkovSpectrumResult(series.source, channel, False, 0, [], kernel.tolist(),
                                    float("nan"), note="data-limited: no PA/RM sequence loaded")
    st, cont = _ordered_channel(series, channel, n_states)
    if st.size < 4 * n_states:
        return MarkovSpectrumResult(series.source, channel, False, int(st.size), [],
                                    kernel.tolist(), float("nan"),
                                    note=f"data-limited: only {st.size} {channel} states")

    P = transition_matrix_from_states(st, n_states)
    eigs = _nontrivial_abs_eigs(P, len(kernel))
    dist = float(np.linalg.norm(eigs - kernel))

    rng = np.random.default_rng(seed)
    # moving-block bootstrap on the STATE sequence (preserves local transitions;
    # IID resampling would scramble order and collapse the eigenvalue CI to 0)
    n = len(st)
    nb = int(np.ceil(n / block))
    boot = np.empty((n_boot, len(kernel)))
    for i in range(n_boot):
        starts = rng.integers(0, max(1, n - block + 1), nb)
        idx = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        boot[i] = _nontrivial_abs_eigs(transition_matrix_from_states(st[idx], n_states), len(kernel))
    lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
    ci_ok = bool(np.all(kernel >= lo) and np.all(kernel <= hi))

    pvals = {m: _null_pvalue(m, st, cont, n_states, kernel, dist, n_null, rng, block)
             for m in (*YAML_NULLS, "dirichlet")}
    overall_p = max(pvals[m] for m in YAML_NULLS)   # conservative: most permissive null

    c = float((ci_ok and overall_p < 0.01) * np.exp(-(dist / 0.05) ** 2))
    worst = max(YAML_NULLS, key=lambda m: pvals[m])
    note = (f"eigs={np.round(eigs, 4).tolist()} vs kernel {np.round(kernel, 4).tolist()}; "
            f"CI_contains_kernel={ci_ok}; overall null p={overall_p:.3f} "
            f"(worst null: {worst})")
    return MarkovSpectrumResult(series.source, channel, True, int(n), eigs.tolist(),
                                kernel.tolist(), dist, lo.tolist(), hi.tolist(), ci_ok,
                                pvals, overall_p, c, note)
