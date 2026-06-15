"""Shared recovery-eigenvalue search across FRB observables.

The methodological shift the user asks for: not "does one plot show 8/27?" but
"do several independent observables of one source share the SAME recovery
eigenvalue?"  We model the per-burst observable memory as a lag-1 (AR(1))
process

    x_{n+1} = a * x_n + eps,

estimate the memory coefficient ``a`` for each available observable, and ask
whether several observables cluster on the SAME kernel eigenvalue
(``2/3`` step, ``8/27`` field, or ``64/729`` energy), with bootstrap CIs.

A coincidence in one channel is not stacked with others; the score only rises
when >= 2 channels share one kernel eigenvalue within their CIs.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .data_io import RepeaterSeries
from .recovery_kernel import LAMBDA2, ONE_THIRD, SQRT_LAMBDA2, TWO_THIRDS

KERNEL_MEMORY = {
    "step_2/3": TWO_THIRDS, "step_1/3": ONE_THIRD,
    "field_8/27": SQRT_LAMBDA2, "energy_64/729": LAMBDA2,
}


def _ar1(x: np.ndarray) -> float:
    """Lag-1 memory coefficient (regression slope of x_{n+1} on x_n)."""
    x = x[np.isfinite(x)]
    if len(x) < 8:
        return np.nan
    x = x - x.mean()
    a, b = x[:-1], x[1:]
    denom = float(a @ a)
    return float(a @ b / denom) if denom > 0 else np.nan


def _ar1_with_ci(x: np.ndarray, n_boot: int, rng) -> tuple[float, float, float]:
    """AR(1) coefficient with a *pair* (block) bootstrap CI.

    NB: IID-resampling the series and re-estimating AR(1) is wrong -- it scrambles
    the time order and collapses the CI toward 0. We instead resample the
    consecutive pairs (x_n, x_{n+1}) jointly, which preserves the lag-1 structure,
    so the CI is genuinely centred on the point estimate.
    """
    a = _ar1(x)
    xs = x[np.isfinite(x)]
    if not np.isfinite(a) or len(xs) < 8:
        return a, np.nan, np.nan
    A, B = xs[:-1], xs[1:]
    n = len(A)
    boot = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        aa, bb = A[idx], B[idx]
        aa = aa - aa.mean()
        bb = bb - bb.mean()
        d = float(aa @ aa)
        if d > 0:
            boot.append(float(aa @ bb / d))
    if not boot:
        return a, np.nan, np.nan
    boot = np.array(boot)
    return a, float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))


@dataclass
class ChannelMemory:
    name: str
    a: float                       # AR(1) lag-1 memory coefficient (point estimate)
    a_ci_lo: float                 # pair-bootstrap 2.5th percentile of a
    a_ci_hi: float                 # pair-bootstrap 97.5th percentile of a
    nearest_kernel: str | None
    nearest_value: float
    delta_to_nearest: float        # |a - nearest_value|
    kernel_in_a_ci: bool           # is the nearest kernel value inside the a-CI?


@dataclass
class SharedKernelResult:
    source: str
    available: bool
    channels: list[ChannelMemory] = field(default_factory=list)
    shared_kernel: str | None = None
    n_sharing: int = 0
    c_shared: float = 0.0
    verdict: str = ""


def _build_channels(series: RepeaterSeries) -> dict[str, np.ndarray]:
    ch: dict[str, np.ndarray] = {}
    if np.isfinite(series.energy).sum() > 8:
        ch["log_energy"] = np.log10(np.where(series.energy > 0, series.energy, np.nan))
    elif np.isfinite(series.fluence).sum() > 8:
        ch["log_fluence"] = np.log10(np.where(series.fluence > 0, series.fluence, np.nan))
    if np.isfinite(series.rm).sum() > 8:
        t, y = series.mjd, series.rm
        ok = np.isfinite(t) & np.isfinite(y)
        resid = np.full(len(y), np.nan)
        if ok.sum() > 4:
            resid[ok] = y[ok] - np.polyval(np.polyfit(t[ok], y[ok], 3), t[ok])
        ch["rm_residual"] = resid
    if np.isfinite(series.mjd).sum() > 8:
        t = np.sort(series.mjd[np.isfinite(series.mjd)])
        wt = np.full(len(series.mjd), np.nan)
        d = np.diff(t)
        wt[1:len(d) + 1] = np.log10(np.where(d > 0, d, np.nan))
        ch["log_waiting"] = wt
    return ch


def shared_kernel_search(series: RepeaterSeries, n_boot: int = 1000,
                         seed: int = 0) -> SharedKernelResult:
    if not series.available:
        return SharedKernelResult(series.source, False, verdict="data-limited")
    rng = np.random.default_rng(seed)
    channels = _build_channels(series)
    cms: list[ChannelMemory] = []
    for name, x in channels.items():
        a, lo, hi = _ar1_with_ci(x, n_boot, rng)
        if not np.isfinite(a):
            continue
        near, nd, nv = None, np.inf, np.nan
        for kname, kval in KERNEL_MEMORY.items():
            if abs(a - kval) < nd:
                near, nd, nv = kname, abs(a - kval), kval
        cms.append(ChannelMemory(name, a, lo, hi, near, nv, float(nd),
                                 bool(np.isfinite(lo) and lo <= nv <= hi)))
    # shared: a kernel value inside the a-CI of >=2 channels
    shared, n_share = None, 0
    for kname, kval in KERNEL_MEMORY.items():
        cnt = sum(1 for c in cms if np.isfinite(c.a_ci_lo) and c.a_ci_lo <= kval <= c.a_ci_hi)
        if cnt > n_share:
            shared, n_share = kname, cnt
    c = 1.0 if n_share >= 2 else 0.0
    verdict = (f"shared eigenvalue {shared} in {n_share} channels" if n_share >= 2
               else f"no shared kernel eigenvalue (max {n_share} channel); "
                    f"memory coefficients consistent with weak/no AR(1) recovery")
    return SharedKernelResult(series.source, True, cms, shared, n_share, c, verdict)


# --------------------------------------------------------------------------- #
# Package G -- a true multivariate VAR(1) over the available observables
# --------------------------------------------------------------------------- #
@dataclass
class VAR1Result:
    source: str
    available: bool
    channels: list[str]
    eigs_abs: list[float] = field(default_factory=list)        # |eig(A)| descending
    nearest_kernel: list[str] = field(default_factory=list)    # per-eig nearest kernel label
    nearest_rel_err: list[float] = field(default_factory=list)
    null_p_any_kernel: float = float("nan")
    note: str = ""


def _var1_matrix(series: RepeaterSeries):
    """Time-ordered, standardised multivariate observable matrix + channel names."""
    order = np.argsort(series.mjd)
    t = series.mjd[order]
    cols: dict[str, np.ndarray] = {}

    def detrend(y):
        ok = np.isfinite(t) & np.isfinite(y)
        out = np.full(len(y), np.nan)
        if ok.sum() > 5:
            out[ok] = y[ok] - np.polyval(np.polyfit(t[ok], y[ok], 3), t[ok])
        return out

    if np.isfinite(series.energy).sum() > 30:
        e = series.energy[order]
        cols["log_energy"] = np.log10(np.where(e > 0, e, np.nan))
    elif np.isfinite(series.fluence).sum() > 30:
        f = series.fluence[order]
        cols["log_fluence"] = np.log10(np.where(f > 0, f, np.nan))
    if np.isfinite(series.rm).sum() > 30:
        cols["rm_resid"] = detrend(series.rm[order])
    if np.isfinite(series.dm).sum() > 30:
        cols["dm_resid"] = detrend(series.dm[order])
    if np.isfinite(series.pa_deg).sum() > 30:
        pa = np.deg2rad(2.0 * series.pa_deg[order])
        cols["pa_sin"] = np.sin(pa)
        cols["pa_cos"] = np.cos(pa)
    if np.isfinite(series.linear_frac).sum() > 30:
        cols["linear_frac"] = series.linear_frac[order].astype(float)

    if len(cols) < 2:
        return None, []
    names = list(cols)
    M = np.column_stack([cols[n] for n in names])
    M = M[np.all(np.isfinite(M), axis=1)]
    if M.shape[0] < 30:
        return None, names
    M = (M - M.mean(axis=0)) / (M.std(axis=0) + 1e-12)
    return M, names


def var1_spectrum(series: RepeaterSeries, n_null: int = 500, tol: float = 0.05,
                  seed: int = 0) -> VAR1Result:
    """Fit X_{n+1} = A X_n on the standardised observable matrix and compare the
    |eigenvalues| of A to the kernel memory set, with a row-shuffle null."""
    if not series.available:
        return VAR1Result(series.source, False, [], note="data-limited")
    M, names = _var1_matrix(series)
    if M is None:
        return VAR1Result(series.source, False, names, note="data-limited: <2 usable channels or <30 rows")
    X0, X1 = M[:-1], M[1:]
    A = np.linalg.lstsq(X0, X1, rcond=None)[0].T     # X1 = X0 @ A.T  =>  A maps X_n -> X_{n+1}
    eigs = np.sort(np.abs(np.linalg.eigvals(A)))[::-1]

    near, rel = [], []
    for ev in eigs:
        kname, kd = min(((kn, abs(ev - kv) / kv) for kn, kv in KERNEL_MEMORY.items()),
                        key=lambda kv: kv[1])
        near.append(kname); rel.append(float(kd))
    obs_best = min(rel) if rel else np.inf

    rng = np.random.default_rng(seed)
    null_best = np.empty(n_null)
    for i in range(n_null):
        idx = rng.permutation(len(M))
        Ms = M[idx]
        An = np.linalg.lstsq(Ms[:-1], Ms[1:], rcond=None)[0].T
        ev = np.sort(np.abs(np.linalg.eigvals(An)))[::-1]
        null_best[i] = min((abs(e - kv) / kv for e in ev for kv in KERNEL_MEMORY.values()),
                           default=np.inf)
    p = float((1 + np.sum(null_best <= obs_best)) / (n_null + 1))
    return VAR1Result(series.source, True, names, [float(e) for e in eigs], near, rel, p,
                      f"VAR(1) on {names}: |eig(A)|={np.round(eigs, 3).tolist()}; "
                      f"nearest kernel rel-errs={[round(r, 2) for r in rel]}; row-shuffle p={p:.3f}")
