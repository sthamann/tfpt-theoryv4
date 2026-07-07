"""FO.02 -- common two-rate operator in the nightly medium state of FRB 20240114A.

Ontology under test: the relaxing magneto-ionic medium is the state, bursts are
probe pulses, and the transduction is a KNOWN linear line integral (DM, RM).
If the medium relaxes under the transfer operator, ALL coupled observables share
one two-rate set with the frozen ratio r2/r1 = ln3/ln(3/2) = 2.7095. An AR(1)/OU
drift (the FRB.04b killer) has observable-specific single memories instead.

Method (preregistered, hypotheses/frb_ontology_v1.yaml):
  per-session medians of {RM, DM, log10 Weff, DOL} -> standardised series ->
  pairwise empirical ACF in 12 log-spaced lag bins (1-150 d) -> joint shared
  two-exponential fit on a frozen (r1, ratio) grid, amplitudes >= 0 per
  observable. Statistic Dstat = |ln(ratio_hat / 2.7095)|.
Nulls/controls: OU surrogates per observable on the same timestamps (full refit);
placebo ratio family; AIC gate shared-two-exp vs per-observable single-exp.
"""

from __future__ import annotations

import numpy as np

from . import constants as c
from .data import PolCatalog, sessions

LAG_MIN_D, LAG_MAX_D, N_BINS = 1.0, 150.0, 12
R1_GRID = np.logspace(np.log10(1.0 / 150.0), 0.0, 40)      # 1/d
RATIO_GRID = np.exp(np.linspace(0.0, np.log(8.0), 30))     # in [1, 8]
N_SURR = 500


def medium_state(cat: PolCatalog) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """Session timestamps (median MJD) + per-session medians of the 4 observables."""
    idxs = sessions(cat.mjd)
    t, obs = [], {"RM": [], "DM": [], "log10Weff": [], "DOL": []}
    for idx in idxs:
        t.append(np.median(cat.mjd[idx]))
        obs["RM"].append(np.nanmedian(cat.rm[idx]))
        obs["DM"].append(np.nanmedian(cat.dm[idx]))
        w = cat.weff_ms[idx]
        obs["log10Weff"].append(np.nanmedian(np.log10(w[w > 0])))
        obs["DOL"].append(np.nanmedian(cat.dol[idx]))
    t = np.array(t)
    return t, {k: np.array(v) for k, v in obs.items()}


def _standardise(x: np.ndarray) -> np.ndarray:
    return (x - np.nanmean(x)) / np.nanstd(x)


def _acf_bins(t: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(bin-centre lag, rho, weight=sqrt(n_pairs)) from all pairs in [1,150] d."""
    edges = np.logspace(np.log10(LAG_MIN_D), np.log10(LAG_MAX_D), N_BINS + 1)
    dt = np.abs(t[:, None] - t[None, :])
    prod = x[:, None] * x[None, :]
    iu = np.triu_indices(len(t), k=1)
    d, p = dt[iu], prod[iu]
    keep = (d >= LAG_MIN_D) & (d <= LAG_MAX_D) & np.isfinite(p)
    d, p = d[keep], p[keep]
    lag, rho, w = [], [], []
    for i in range(N_BINS):
        m = (d >= edges[i]) & (d < edges[i + 1])
        if m.sum() >= 3:
            lag.append(np.exp(np.mean(np.log(d[m]))))
            rho.append(np.mean(p[m]))
            w.append(np.sqrt(m.sum()))
    return np.array(lag), np.array(rho), np.array(w)


def _nnls2_vec(E1: np.ndarray, E2: np.ndarray, y: np.ndarray, w: np.ndarray
               ) -> tuple[np.ndarray, np.ndarray]:
    """Vectorised weighted 2-column NNLS over a grid.

    E1, E2: (G, n) basis; y, w: (n,). Returns (SSE (G,), ratio-usable flag is
    left to the caller via the c2 amplitudes (G, 2)).
    """
    w2 = w ** 2
    a11 = (w2 * E1 * E1).sum(1)
    a12 = (w2 * E1 * E2).sum(1)
    a22 = (w2 * E2 * E2).sum(1)
    b1 = (w2 * E1 * y).sum(1)
    b2 = (w2 * E2 * y).sum(1)
    det = a11 * a22 - a12 ** 2
    det = np.where(np.abs(det) < 1e-12, np.nan, det)
    c1 = (a22 * b1 - a12 * b2) / det
    c2 = (a11 * b2 - a12 * b1) / det
    # clip to the non-negative orthant (KKT for 2 variables)
    c1_only = np.clip(b1 / np.where(a11 < 1e-12, np.nan, a11), 0, None)
    c2_only = np.clip(b2 / np.where(a22 < 1e-12, np.nan, a22), 0, None)
    yy = (w2 * y * y).sum()
    sse_both = yy - (c1 * b1 + c2 * b2)
    sse_1 = yy - c1_only * b1
    sse_2 = yy - c2_only * b2
    bad = ~((c1 >= 0) & (c2 >= 0))
    use1 = bad & (sse_1 <= sse_2)
    use2 = bad & ~use1
    sse = np.where(use1, sse_1, np.where(use2, sse_2, sse_both))
    c1f = np.where(use1, c1_only, np.where(use2, 0.0, c1))
    c2f = np.where(use1, 0.0, np.where(use2, c2_only, c2))
    return np.nan_to_num(sse, nan=np.inf), np.stack([c1f, c2f], 1)


def _fit_shared(acfs: list[tuple[np.ndarray, np.ndarray, np.ndarray]]
                ) -> tuple[float, float, float, np.ndarray]:
    """Joint shared-two-exp fit. Returns (SSE, r1_hat, ratio_hat, amps (n_obs,2))."""
    G = len(R1_GRID) * len(RATIO_GRID)
    r1 = np.repeat(R1_GRID, len(RATIO_GRID))
    ratio = np.tile(RATIO_GRID, len(R1_GRID))
    total = np.zeros(G)
    amps = []
    for lag, rho, w in acfs:
        E1 = np.exp(-r1[:, None] * lag[None, :])
        E2 = np.exp(-(r1 * ratio)[:, None] * lag[None, :])
        sse, cf = _nnls2_vec(E1, E2, rho, w)
        total += sse
        amps.append(cf)
    k = int(np.argmin(total))
    return float(total[k]), float(r1[k]), float(ratio[k]), \
        np.array([a[k] for a in amps])


def _fit_single(lag, rho, w) -> tuple[float, float]:
    """Best single-exp (rate, SSE) on the frozen r grid, amplitude >= 0."""
    E = np.exp(-R1_GRID[:, None] * lag[None, :])
    w2 = w ** 2
    num = (w2 * E * rho).sum(1)
    den = (w2 * E * E).sum(1)
    a = np.clip(num / den, 0.0, 1.5)
    sse = (w2 * rho * rho).sum() - 2 * a * num + a ** 2 * den
    k = int(np.argmin(sse))
    return float(R1_GRID[k]), float(sse[k])


def _ou_surrogate(rng: np.random.Generator, t: np.ndarray, r: float) -> np.ndarray:
    x = np.empty(len(t))
    x[0] = rng.standard_normal()
    for k in range(1, len(t)):
        f = np.exp(-r * (t[k] - t[k - 1]))
        x[k] = x[k - 1] * f + np.sqrt(max(1.0 - f * f, 1e-12)) * rng.standard_normal()
    return _standardise(x)


def run(cat: PolCatalog, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    t, obs = medium_state(cat)
    series = {k: _standardise(v) for k, v in obs.items()}
    acfs = [_acf_bins(t, series[k]) for k in series]
    names = list(series)

    sse_two, r1_hat, ratio_hat, amps = _fit_shared(acfs)
    singles = {n: _fit_single(*a) for n, a in zip(names, acfs)}
    sse_one = sum(s for _, s in singles.values())
    n_pts = sum(len(a[0]) for a in acfs)
    aic_two = n_pts * np.log(max(sse_two, 1e-12) / n_pts) + 2 * (2 + 2 * len(names))
    aic_one = n_pts * np.log(max(sse_one, 1e-12) / n_pts) + 2 * (2 * len(names))
    two_rate_required = bool(aic_two < aic_one)

    dstat = abs(np.log(ratio_hat / c.BEND))
    placebo_d = {str(p): abs(np.log(ratio_hat / p)) for p in c.PLACEBO_RATIOS}
    kernel_closest = bool(all(dstat < v for v in placebo_d.values()))

    # OU null: per-observable surrogates with the fitted single rates, full refit
    null_d = np.empty(N_SURR)
    for i in range(N_SURR):
        sur = []
        for n in names:
            x = _ou_surrogate(rng, t, singles[n][0])
            sur.append(_acf_bins(t, x))
        _, _, ratio_n, _ = _fit_shared(sur)
        null_d[i] = abs(np.log(ratio_n / c.BEND))
    p_ou = float((1 + np.sum(null_d <= dstat)) / (N_SURR + 1))

    if not two_rate_required:
        verdict = "data_limited"
        note = "AIC prefers per-observable single rates -> the data do not require a second rate"
    elif p_ou < 0.05 and kernel_closest:
        verdict = "hint_flag"
        note = "kernel-close common ratio beats OU null and placebos -> escalate-only"
    else:
        verdict = "null"
        note = "no common two-rate set preferentially at the kernel ratio"

    return {
        "axis": "FO.02_common_rate_medium",
        "n_sessions": int(len(t)),
        "n_acf_points": int(n_pts),
        "single_rates_per_day": {n: round(r, 5) for n, (r, _) in singles.items()},
        "shared_fit": {"r1_per_day": round(r1_hat, 5), "ratio": round(ratio_hat, 4),
                       "amps": {n: [round(float(a), 4) for a in amps[i]]
                                for i, n in enumerate(names)},
                       "sse_two": round(sse_two, 4), "sse_one": round(sse_one, 4),
                       "aic_two": round(float(aic_two), 2),
                       "aic_one": round(float(aic_one), 2)},
        "two_rate_required_by_aic": two_rate_required,
        "kernel_ratio": round(c.BEND, 6),
        "dstat_ln": round(dstat, 4),
        "placebo_dstat_ln": {k: round(v, 4) for k, v in placebo_d.items()},
        "kernel_closest": kernel_closest,
        "p_ou_null": p_ou,
        "verdict": verdict,
        "note": note,
    }
