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
    a = _ar1(x)
    if not np.isfinite(a):
        return a, np.nan, np.nan
    xs = x[np.isfinite(x)]
    boot = np.array([_ar1(xs[rng.integers(0, len(xs), len(xs))]) for _ in range(n_boot)])
    boot = boot[np.isfinite(boot)]
    return a, float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))


@dataclass
class ChannelMemory:
    name: str
    a: float
    ci_lo: float
    ci_hi: float
    nearest_kernel: str | None
    nearest_value: float
    ci_contains_kernel: bool


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
        cms.append(ChannelMemory(name, a, lo, hi, near, nv,
                                 bool(np.isfinite(lo) and lo <= nv <= hi)))
    # shared: a kernel value whose CI is contained by >=2 channels
    shared, n_share = None, 0
    for kname, kval in KERNEL_MEMORY.items():
        cnt = sum(1 for c in cms if np.isfinite(c.ci_lo) and c.ci_lo <= kval <= c.ci_hi)
        if cnt > n_share:
            shared, n_share = kname, cnt
    c = 1.0 if n_share >= 2 else 0.0
    verdict = (f"shared eigenvalue {shared} in {n_share} channels" if n_share >= 2
               else f"no shared kernel eigenvalue (max {n_share} channel); "
                    f"memory coefficients consistent with weak/no AR(1) recovery")
    return SharedKernelResult(series.source, True, cms, shared, n_share, c, verdict)
