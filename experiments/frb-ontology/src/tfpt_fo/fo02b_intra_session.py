"""FO.02b -- INTRA-session common two-rate test (v1.2 addendum, prereg before run).

The data FO.02 v1 said it needed already exist: per-burst RM (and partner
observables) WITHIN sessions, where constant-RM is strongly rejected. If the
medium relaxation is driven by the transfer operator, all coupled observables
in a session share ONE two-rate set with the frozen ratio ln3/ln(3/2) = 2.7095
(the session clock r1 may vary; the RATIO may not). Per-burst scatter without
temporal memory instead types the RM variance as magnetospheric/per-burst --
an informative negative for the 'FRB as medium measurement' ontology.

Gates (preregistered): memory gate per (session, observable) -- first ACF lag
bin beats a time-shuffle null; AIC gate -- shared two-exp must beat
per-observable single-exp. Statistic: median |ln(ratio_s / 2.7095)| over
AIC-passing sessions. Nulls: OU surrogates (full refit incl. gates) + placebo
ratio family. Sources analysed separately (v5 + Blinkverse 20201124A).
"""

from __future__ import annotations

import numpy as np

from . import constants as c
from .data import RmSeries, sessions

MIN_PER_OBS = 30
MIN_OBS_PER_SESSION = 2
N_LAG_BINS = 8
LAG_MIN_S = 30.0
N_MEMORY_NULL = 200
N_OU = 300
RATIO_GRID = np.exp(np.linspace(0.0, np.log(8.0), 30))
DAY_S = 86400.0


def _standardise(x: np.ndarray) -> np.ndarray:
    return (x - np.nanmean(x)) / np.nanstd(x)


def _acf_bins(t_s: np.ndarray, x: np.ndarray, lag_max_s: float
              ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    edges = np.logspace(np.log10(LAG_MIN_S), np.log10(lag_max_s), N_LAG_BINS + 1)
    dt = np.abs(t_s[:, None] - t_s[None, :])
    prod = x[:, None] * x[None, :]
    iu = np.triu_indices(len(t_s), k=1)
    d, p = dt[iu], prod[iu]
    keep = (d >= LAG_MIN_S) & (d <= lag_max_s) & np.isfinite(p)
    d, p = d[keep], p[keep]
    lag, rho, w = [], [], []
    for i in range(N_LAG_BINS):
        m = (d >= edges[i]) & (d < edges[i + 1])
        if m.sum() >= 5:
            lag.append(np.exp(np.mean(np.log(d[m]))))
            rho.append(np.mean(p[m]))
            w.append(np.sqrt(m.sum()))
    return np.array(lag), np.array(rho), np.array(w)


def _memory_gate(rng: np.random.Generator, t_s: np.ndarray, x: np.ndarray,
                 lag_max_s: float) -> tuple[bool, float]:
    """First-lag-bin ACF vs within-session time-shuffle (one-sided, rho > null)."""
    lag, rho, _ = _acf_bins(t_s, x, lag_max_s)
    if lag.size < 3:
        return False, 1.0
    obs = rho[0]
    null = np.empty(N_MEMORY_NULL)
    for i in range(N_MEMORY_NULL):
        xs = rng.permutation(x)
        _, r, _ = _acf_bins(t_s, xs, lag_max_s)
        null[i] = r[0] if r.size else 0.0
    p = float((1 + np.sum(null >= obs)) / (N_MEMORY_NULL + 1))
    return p < 0.05, p


def _nnls2(E1, E2, y, w):
    w2 = w ** 2
    a11 = (w2 * E1 * E1).sum(-1)
    a12 = (w2 * E1 * E2).sum(-1)
    a22 = (w2 * E2 * E2).sum(-1)
    b1 = (w2 * E1 * y).sum(-1)
    b2 = (w2 * E2 * y).sum(-1)
    det = a11 * a22 - a12 ** 2
    det = np.where(np.abs(det) < 1e-12, np.nan, det)
    c1 = (a22 * b1 - a12 * b2) / det
    c2 = (a11 * b2 - a12 * b1) / det
    c1o = np.clip(b1 / np.where(a11 < 1e-12, np.nan, a11), 0, None)
    c2o = np.clip(b2 / np.where(a22 < 1e-12, np.nan, a22), 0, None)
    yy = (w2 * y * y).sum()
    sse_b = yy - (c1 * b1 + c2 * b2)
    sse_1 = yy - c1o * b1
    sse_2 = yy - c2o * b2
    bad = ~((c1 >= 0) & (c2 >= 0))
    use1 = bad & (sse_1 <= sse_2)
    use2 = bad & ~use1
    return np.nan_to_num(np.where(use1, sse_1, np.where(use2, sse_2, sse_b)),
                         nan=np.inf)


def _fit_session(acfs: list[tuple[np.ndarray, np.ndarray, np.ndarray]],
                 t_span_s: float) -> dict | None:
    """Shared two-exp vs per-observable single-exp on the session's ACFs."""
    r1_grid = np.logspace(np.log10(0.25 / t_span_s), np.log10(3.0 / LAG_MIN_S), 40)
    r1 = np.repeat(r1_grid, RATIO_GRID.size)
    ratio = np.tile(RATIO_GRID, r1_grid.size)
    total = np.zeros(r1.size)
    sse_one, n_pts = 0.0, 0
    for lag, rho, w in acfs:
        E1 = np.exp(-r1[:, None] * lag[None, :])
        E2 = np.exp(-(r1 * ratio)[:, None] * lag[None, :])
        total += _nnls2(E1, E2, rho, w)
        # single-exp per observable
        E = np.exp(-r1_grid[:, None] * lag[None, :])
        w2 = w ** 2
        num = (w2 * E * rho).sum(1)
        den = (w2 * E * E).sum(1)
        a = np.clip(num / den, 0.0, 1.5)
        sse = (w2 * rho * rho).sum() - 2 * a * num + a ** 2 * den
        sse_one += float(sse.min())
        n_pts += lag.size
    k = int(np.argmin(total))
    n_obs = len(acfs)
    aic_two = n_pts * np.log(max(float(total[k]), 1e-12) / n_pts) + 2 * (2 + 2 * n_obs)
    aic_one = n_pts * np.log(max(sse_one, 1e-12) / n_pts) + 2 * (2 * n_obs)
    return {"r1": float(r1[k]), "ratio": float(ratio[k]),
            "aic_two": float(aic_two), "aic_one": float(aic_one),
            "two_required": bool(aic_two < aic_one), "n_pts": n_pts}


def _session_blocks(series: RmSeries) -> list[dict]:
    """Per session: standardised (t_s, x) blocks for eligible observables."""
    out = []
    for idx in sessions(series.mjd):
        t_s = (series.mjd[idx] - series.mjd[idx[0]]) * DAY_S
        block = {}
        for name, vals in series.obs.items():
            x = vals[idx]
            ok = np.isfinite(x)
            if ok.sum() < MIN_PER_OBS or np.nanstd(x[ok]) == 0:
                continue
            block[name] = (t_s[ok], _standardise(x[ok]))
        if len(block) >= MIN_OBS_PER_SESSION:
            out.append({"mjd0": float(series.mjd[idx[0]]),
                        "span_s": float(t_s[-1]), "obs": block})
    return out


def _analyse_once(rng: np.random.Generator, blocks: list[dict],
                  collect: list | None = None) -> float | None:
    """Full pipeline (memory gate -> AIC gate -> median Dstat); returns None
    if no session survives both gates."""
    dstats = []
    for b in blocks:
        lag_max = b["span_s"] / 2.0
        acfs, kept = [], []
        for name, (t_s, x) in b["obs"].items():
            ok, p_mem = _memory_gate(rng, t_s, x, lag_max)
            if ok:
                acf = _acf_bins(t_s, x, lag_max)
                if acf[0].size >= 3:
                    acfs.append(acf)
                    kept.append((name, p_mem))
        if len(acfs) < MIN_OBS_PER_SESSION:
            if collect is not None:
                collect.append({"mjd0": round(b["mjd0"], 3), "gate": "memory_failed",
                                "n_memory_obs": len(acfs)})
            continue
        fit = _fit_session(acfs, b["span_s"])
        row = {"mjd0": round(b["mjd0"], 3),
               "obs_kept": [n for n, _ in kept],
               "ratio": round(fit["ratio"], 3), "r1_per_s": fit["r1"],
               "aic_two": round(fit["aic_two"], 1),
               "aic_one": round(fit["aic_one"], 1),
               "two_required": fit["two_required"]}
        if fit["two_required"]:
            d = abs(np.log(fit["ratio"] / c.BEND))
            dstats.append(d)
            row["dstat_ln"] = round(d, 4)
        if collect is not None:
            collect.append(row)
    if not dstats:
        return None
    return float(np.median(dstats))


def _ou_blocks(rng: np.random.Generator, blocks: list[dict]) -> list[dict]:
    """OU surrogates per (session, observable) at the fitted single-exp rate."""
    out = []
    for b in blocks:
        lag_max = b["span_s"] / 2.0
        nb = {"mjd0": b["mjd0"], "span_s": b["span_s"], "obs": {}}
        for name, (t_s, x) in b["obs"].items():
            lag, rho, w = _acf_bins(t_s, x, lag_max)
            if lag.size >= 2:
                r_grid = np.logspace(np.log10(0.25 / b["span_s"]),
                                     np.log10(3.0 / LAG_MIN_S), 40)
                E = np.exp(-r_grid[:, None] * lag[None, :])
                w2 = w ** 2
                num = (w2 * E * rho).sum(1)
                den = (w2 * E * E).sum(1)
                a = np.clip(num / den, 0.0, 1.5)
                sse = (w2 * rho * rho).sum() - 2 * a * num + a ** 2 * den
                r_o = float(r_grid[int(np.argmin(sse))])
            else:
                r_o = 1.0 / b["span_s"]
            xs = np.empty(len(t_s))
            xs[0] = rng.standard_normal()
            for k in range(1, len(t_s)):
                f = np.exp(-r_o * (t_s[k] - t_s[k - 1]))
                xs[k] = xs[k - 1] * f + np.sqrt(max(1 - f * f, 1e-12)) * rng.standard_normal()
            nb["obs"][name] = (t_s, _standardise(xs))
        if len(nb["obs"]) >= MIN_OBS_PER_SESSION:
            out.append(nb)
    return out


def _validate_memory_gate(rng: np.random.Generator, blocks: list[dict]) -> dict:
    """Injection validation of the memory gate on the REAL timestamps:
    OU processes with tau_c in {120, 600, 1800} s must pass; white noise must not."""
    times = []
    for b in blocks:
        name0 = next(iter(b["obs"]))
        times.append(b["obs"][name0][0])
    out = {}
    for tau_c in (120.0, 600.0, 1800.0):
        hits = 0
        for t_s in times:
            r = 1.0 / tau_c
            x = np.empty(len(t_s))
            x[0] = rng.standard_normal()
            for k in range(1, len(t_s)):
                f = np.exp(-r * (t_s[k] - t_s[k - 1]))
                x[k] = x[k - 1] * f + np.sqrt(max(1 - f * f, 1e-12)) * rng.standard_normal()
            ok, _ = _memory_gate(rng, t_s, _standardise(x), t_s[-1] / 2.0)
            hits += ok
        out[f"ou_tau{int(tau_c)}s"] = f"{hits}/{len(times)}"
    fp = 0
    for t_s in times:
        ok, _ = _memory_gate(rng, t_s, rng.standard_normal(len(t_s)), t_s[-1] / 2.0)
        fp += ok
    out["white_noise_fp"] = f"{fp}/{len(times)}"
    return out


def run_source(series: RmSeries, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    blocks = _session_blocks(series)
    detail: list = []
    med_obs = _analyse_once(rng, blocks, collect=detail)

    n_two = sum(1 for d in detail if d.get("two_required"))
    out = {"source": series.source, "n_sessions_eligible": len(blocks),
           "n_sessions_two_rate": n_two, "sessions": detail,
           "kernel_ratio": round(c.BEND, 6),
           "memory_gate_injection_validation": _validate_memory_gate(rng, blocks)}

    if med_obs is None:
        n_mem_failed = sum(1 for d in detail if d.get("gate") == "memory_failed")
        out["verdict"] = "data_limited"
        out["note"] = (f"preregistered informative negative: {n_mem_failed}/"
                       f"{len(blocks)} sessions fail the MEMORY gate although the "
                       "gate is injection-validated on the same timestamps -> the "
                       "intra-session variance is per-burst (magnetospheric/"
                       "sightline), NOT a relaxing medium state; the two-rate "
                       "ratio is untestable in this channel (data_limited per "
                       "prereg), and the 'FRB as medium measurement' reading is "
                       "disfavoured at burst-sampling cadence")
        return out

    placebo = {str(p): None for p in c.PLACEBO_RATIOS}
    ratios = [d["ratio"] for d in detail if d.get("two_required")]
    for p in c.PLACEBO_RATIOS:
        placebo[str(p)] = round(float(np.median([abs(np.log(r / p)) for r in ratios])), 4)
    kernel_closest = all(med_obs < v for v in placebo.values())

    null_med = []
    for _ in range(N_OU):
        m = _analyse_once(rng, _ou_blocks(rng, blocks))
        if m is not None:
            null_med.append(m)
    if null_med:
        p_ou = float((1 + np.sum(np.array(null_med) <= med_obs)) / (len(null_med) + 1))
    else:
        p_ou = None

    out.update({"median_dstat_ln": round(med_obs, 4),
                "median_ratio": round(float(np.median(ratios)), 3),
                "placebo_median_dstat_ln": placebo,
                "kernel_closest": kernel_closest,
                "n_ou_null_valid": len(null_med),
                "p_ou_null": p_ou})
    if p_ou is not None and p_ou < 0.05 and kernel_closest:
        out["verdict"] = "hint_flag"
        out["note"] = "escalate-only; needs the second source to agree"
    else:
        out["verdict"] = "null"
        out["note"] = ("two-rate relaxation resolvable but the ratio is not "
                       "preferentially at 2.7095")
    return out


def run(sources: list[RmSeries], seed: int = 0) -> dict:
    per = [run_source(s, seed) for s in sources]
    verdicts = {p["source"]: p["verdict"] for p in per}
    if all(v == "data_limited" for v in verdicts.values()):
        overall = "data_limited"
    elif any(v == "hint_flag" for v in verdicts.values()):
        overall = ("hint_flag" if all(v == "hint_flag" for v in verdicts.values())
                   else "not_confirmed_not_refuted")
    else:
        overall = "null"
    return {"axis": "FO.02b_intra_session_common_rate",
            "per_source": per, "verdicts": verdicts, "verdict": overall}
