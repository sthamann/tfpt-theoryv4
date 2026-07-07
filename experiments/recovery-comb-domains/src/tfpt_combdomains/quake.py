"""Test the FULL TFPT log-periodic signature battery against real earthquake aftershock data.

Aftershock sequences (Omori decay, rate ~ t^-p) are the data-richest terrestrial relaxation with
the wide ln(t) range and high counts the faint (~2%) recovery comb needs -- and discrete scale
invariance is already a documented (Sornette) feature of seismicity. FIREWALL: earthquakes are a
crustal/critical relaxation, NOT a boundary/horizon recovery, so any hit here is a SHAPE-level
coincidence about universal DSI, never confirmation of TFPT physics. The value is the sharp,
falsifiable question TFPT alone asks: is the preferred log-period one of the TFPT ratios
(3/2, (3/2)^6, ...), and not the freely-fit value seismology usually reports (~2)?

Battery (reusing the injection-validated detector from ``comb.py``):
  1. comb at every TFPT log-period lambda -> omega = 2 pi / ln(lambda), stacked across sequences,
     with a PER-lambda ln-range + Nyquist gate and a Bonferroni look-elsewhere correction;
  2. a free-fit of the data's own dominant log-period (where is seismicity's DSI scale?);
  3. the Omori exponent p vs TFPT rational candidates (secondary, heavily caveated).
"""

from __future__ import annotations

import csv
import io
import json
import math
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from .comb import (MIN_COMB_PERIODS, P_THRESHOLD, _comb_gain, _matched_pool, comb_periods)

DATA = Path(__file__).resolve().parents[2] / "data" / "quake"
RESULTS = Path(__file__).resolve().parents[2] / "results"
UA = {"User-Agent": "tfpt-research/0.1 (recovery-comb-domains; mailto:test@example.com)"}
USGS = "https://earthquake.usgs.gov/fdsnws/event/1/query?"


@dataclass(frozen=True)
class Mainshock:
    name: str
    start: str
    end: str
    lat: float
    lon: float
    radius_km: float
    minmag: float


# Rich aftershock sequences: dense local networks (low completeness mag -> many cycles, great early
# sampling) plus great earthquakes (global coverage).
MAINSHOCKS: tuple[Mainshock, ...] = (
    Mainshock("Ridgecrest2019", "2019-07-06", "2022-07-06", 35.770, -117.599, 80, 2.0),
    Mainshock("Landers1992", "1992-06-28", "1995-06-28", 34.200, -116.437, 80, 2.5),
    Mainshock("HectorMine1999", "1999-10-16", "2002-10-16", 34.594, -116.271, 80, 2.5),
    Mainshock("Tohoku2011", "2011-03-11", "2014-03-11", 38.297, 142.373, 500, 4.5),
    Mainshock("Maule2010", "2010-02-27", "2013-02-27", -36.122, -72.898, 500, 4.5),
    Mainshock("Sumatra2004", "2004-12-26", "2007-12-26", 3.295, 95.982, 600, 4.7),
)

PHI = 0.5 * (1.0 + math.sqrt(5.0))
# TFPT log-period battery: lambda (the discrete-scale-invariance ratio) -> omega = 2 pi / ln lambda.
# FROZEN -- guarded bit-for-bit by strange-metal-comb/tests/test_frozen_kernel.py; the Z2/Moebius
# readings live in the separate Z2_LAMBDAS below.
TFPT_LAMBDAS: dict[str, float] = {
    "3/2 (1/Koide, fundamental)": 1.5,
    "phi (golden, g_car=5)": PHI,
    "2 (sheet doubling)": 2.0,
    "3 (N_fam)": 3.0,
    "4 (|mu4|)": 4.0,
    "5 (g_car)": 5.0,
    "8 (rank E8)": 8.0,
    "(3/2)^6 (recovery comb)": 1.5 ** 6,
    "30 (Coxeter h)": 30.0,
}
# The Z2/Moebius double-cover READINGS of the SAME kernel (added 2026-07-06, EXPLORATORY and
# UNFORCED -- no theory contract selects one; a hit is "escalate -> independent cross-check",
# never a claim): if the comb carries the Z2 sheet parity per kernel period (antiperiodic: sign
# flip each period, periodic only on the double cover), its Fourier power at the kernel
# omega=2.583 is exactly ZERO -- the fundamental moves to omega/2 <-> lambda=(3/2)^12 and the
# first odd harmonic to 3*omega/2 <-> lambda=(3/2)^4. If instead the base observable ticks the
# HALF period (the amplitude/sqrt-lambda reading per rung, cf. the energy-vs-amplitude
# semantics), the comb sits at 2*omega <-> lambda=(3/2)^3.
Z2_LAMBDAS: dict[str, float] = {
    "(3/2)^3 (Z2 half-period)": 1.5 ** 3,
    "(3/2)^4 (Z2 antiperiodic harmonic)": 1.5 ** 4,
    "(3/2)^12 (Z2 antiperiodic fundamental)": 1.5 ** 12,
}
# the full battery = frozen atoms/kernel + the Z2 readings
BATTERY_LAMBDAS: dict[str, float] = {**TFPT_LAMBDAS, **Z2_LAMBDAS}
# the structurally "deep" (idiosyncratic) TFPT ratios -- a hit here would matter more than the
# low-complexity atoms {2,3,4,5,8}, which are dense among any scaling story. (FROZEN, guarded
# bit-for-bit.) The Z2 readings are kernel-derived, hence idiosyncratic too (BATTERY_IDIO).
IDIO = {"3/2 (1/Koide, fundamental)", "phi (golden, g_car=5)", "(3/2)^6 (recovery comb)"}
BATTERY_IDIO = IDIO | set(Z2_LAMBDAS)


def _omega(lam: float) -> float:
    return 2.0 * math.pi / math.log(lam)


def fetch_quake(ms: Mainshock, *, refresh: bool = False) -> np.ndarray:
    """Aftershock times in days since the first catalogued event (>0), from the USGS FDSN event
    service. Cached to data/quake/<name>.csv (gitignored)."""
    DATA.mkdir(parents=True, exist_ok=True)
    cache = DATA / f"{ms.name}.csv"
    if cache.exists() and not refresh:
        txt = cache.read_text(encoding="utf-8")
    else:
        url = USGS + urllib.parse.urlencode({
            "format": "csv", "starttime": ms.start, "endtime": ms.end,
            "latitude": ms.lat, "longitude": ms.lon, "maxradiuskm": ms.radius_km,
            "minmagnitude": ms.minmag, "orderby": "time-asc", "limit": 20000})
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=90) as r:  # noqa: S310
            txt = r.read().decode("utf-8", "replace")
        cache.write_text(txt, encoding="utf-8")
    times = []
    for row in csv.DictReader(io.StringIO(txt)):
        try:
            times.append(datetime.fromisoformat(row["time"].replace("Z", "+00:00")))
        except (KeyError, ValueError):
            continue
    if len(times) < 20:
        return np.array([])
    t0 = min(times)
    days = np.array([(t - t0).total_seconds() / 86400.0 for t in times])
    return np.sort(days[days > 0])


def rate_curve(days: np.ndarray, *, n_bins: int = 80, min_count: int = 2
               ) -> tuple[np.ndarray, np.ndarray]:
    """Equal-ln(t) bins of aftershock COUNTS -> (t_center, y=ln count). For Omori rate ~ t^-p the
    per-bin count ~ t^(1-p) (~flat at p~1), so equal-ln(t) bins give near-uniform weight in ln(t)
    -- the natural frame for a log-periodic comb. The comb survives as a residual on y(ln t)."""
    lt = np.log(days)
    edges = np.linspace(lt.min(), lt.max(), n_bins + 1)
    idx = np.clip(np.digitize(lt, edges) - 1, 0, n_bins - 1)
    tc, y = [], []
    for j in range(n_bins):
        c = int(np.sum(idx == j))
        if c >= min_count:
            tc.append(math.exp(0.5 * (edges[j] + edges[j + 1])))
            y.append(math.log(c))
    return np.array(tc), np.array(y)


def _stacked_at(curves: list[tuple[np.ndarray, np.ndarray]], omega: float, *,
                n_draws: int = 4000, n_pool: int = 160, seed: int = 0) -> dict:
    """Stacked permutation comb test at an ARBITRARY omega, with a PER-omega gate: each curve must
    span >= MIN_COMB_PERIODS cycles of THIS omega and sample it below Nyquist. Same statistic as
    comb.stacked_comb_test (sum of matched-band-ranked kernel gains)."""
    lam = math.exp(2.0 * math.pi / omega)
    prepared = []
    for t, y in curves:
        lt = np.log(np.asarray(t, float))
        yy = np.asarray(y, float)
        if len(lt) < 6:
            continue
        periods = (lt.max() - lt.min()) / math.log(lam)
        dln = float(np.median(np.diff(np.sort(lt))))
        nyq = math.pi / dln if dln > 0 else math.inf
        if periods >= MIN_COMB_PERIODS and omega <= nyq:
            prepared.append((lt, yy))
    k = len(prepared)
    if k == 0:
        return {"n_used": 0, "gain": 0.0, "p_value": 1.0, "comb_detected": False}
    rng = np.random.default_rng(seed)
    g_om, pools = [], []
    for lt, yy in prepared:
        g0, pool = _matched_pool(lt, yy, omega, rng, n_pool)
        g_om.append(g0)
        pools.append(pool)
    s_obs = float(sum(g_om))
    draws = np.zeros(n_draws)
    for pool in pools:
        draws += rng.choice(pool, size=n_draws)
    p = float((1 + np.sum(draws >= s_obs)) / (n_draws + 1))
    return {"n_used": k, "gain": round(float(np.mean(g_om)), 4), "p_value": round(p, 4),
            "comb_detected": bool(p < P_THRESHOLD)}


def free_fit(curves: list[tuple[np.ndarray, np.ndarray]], *, n_grid: int = 300) -> list[dict]:
    """Where is seismicity's OWN dominant log-period? Stacked comb gain over a dense omega grid;
    report the top peaks as lambda = exp(2 pi / omega) (a la Sornette's free DSI fit)."""
    lts = [np.log(np.asarray(t, float)) for t, _ in curves]
    ys = [np.asarray(y, float) for _, y in curves]
    rng_ln = min(lt.max() - lt.min() for lt in lts)
    dln = max(float(np.median(np.diff(np.sort(lt)))) for lt in lts)
    omega_lo = 2.0 * math.pi * MIN_COMB_PERIODS / rng_ln      # >= MIN periods over shortest curve
    omega_hi = min(0.9 * math.pi / dln, 18.0)                # below Nyquist of coarsest sampling
    grid = np.linspace(omega_lo, omega_hi, n_grid)
    spec = np.array([sum(_comb_gain(lt, y, w) for lt, y in zip(lts, ys)) for w in grid])
    peaks = []
    for i in range(1, len(grid) - 1):
        if spec[i] >= spec[i - 1] and spec[i] >= spec[i + 1]:
            peaks.append((float(spec[i]), float(grid[i])))
    peaks.sort(reverse=True)
    out = []
    for s, w in peaks[:3]:
        out.append({"omega": round(w, 3), "lambda": round(math.exp(2 * math.pi / w), 3),
                    "stacked_gain": round(s, 4)})
    return out


def omori_p(curves: list[tuple[np.ndarray, np.ndarray]]) -> list[float]:
    """p from y = ln(count) = (1-p) ln t + const (+ comb); slope = 1-p (equal-ln-t binning)."""
    ps = []
    for t, y in curves:
        lt = np.log(np.asarray(t, float))
        a = np.vstack([lt, np.ones_like(lt)]).T
        slope = float(np.linalg.lstsq(a, np.asarray(y, float), rcond=None)[0][0])
        ps.append(1.0 - slope)
    return ps


def analyze(refresh: bool = False) -> dict:
    print("=" * 84)
    print("TFPT signature battery vs REAL earthquake aftershocks (USGS FDSN)")
    print("  FIREWALL: crustal/critical relaxation, NOT a horizon recovery -> any hit = universal-")
    print("  DSI shape coincidence, never TFPT confirmation. The sharp question: is the preferred")
    print("  log-period a TFPT ratio (3/2, (3/2)^6, phi, ...) rather than the usual free-fit ~2?")
    print("=" * 84)

    curves, meta = [], []
    for ms in MAINSHOCKS:
        days = fetch_quake(ms, refresh=refresh)
        if len(days) < 20:
            print(f"  {ms.name}: too few events ({len(days)})")
            continue
        t, y = rate_curve(days)
        per = comb_periods(t)
        curves.append((t, y))
        meta.append({"name": ms.name, "n_events": int(len(days)), "n_bins": int(len(t)),
                     "ln_range": round(float(np.log(t.max() / t.min())), 2),
                     "periods_3half6": round(per, 2)})
        print(f"  {ms.name}: {len(days)} events, {len(t)} bins, ln-range "
              f"{np.log(t.max()/t.min()):.1f} ({per:.1f} periods @ (3/2)^6)")
    if not curves:
        print("  no usable sequences."); return {}

    # (1) TFPT log-period battery (incl. the Z2/Moebius readings), stacked + Bonferroni
    print("\n  --- (1) comb at each TFPT log-period (stacked over sequences) ---")
    battery = {}
    for label, lam in BATTERY_LAMBDAS.items():
        res = _stacked_at(curves, _omega(lam), seed=17)
        battery[label] = {"lambda": round(lam, 4), "omega": round(_omega(lam), 3), **res}
        tag = "IDIO" if label in BATTERY_IDIO else "atom"
        print(f"    [{tag}] lambda={lam:7.3f} (omega={_omega(lam):5.2f})  "
              f"n_used={res['n_used']}  stacked p={res['p_value']:.4f}"
              f"{'  <-- nominally special' if res['comb_detected'] else ''}")
    tested = [v for v in battery.values() if v["n_used"] > 0]
    min_p = min((v["p_value"] for v in tested), default=1.0)
    m_eff = max(1, len(tested))
    global_p = min(1.0, min_p * m_eff)
    print(f"  best stacked p = {min_p:.4f} over {m_eff} gated TFPT log-periods; "
          f"Bonferroni global p = {global_p:.3f}")

    # (2) free-fit: the data's own preferred log-period(s)
    print("\n  --- (2) free-fit: seismicity's OWN dominant log-period (top peaks) ---")
    peaks = free_fit(curves)
    for pk in peaks:
        near = min(BATTERY_LAMBDAS.items(), key=lambda kv: abs(math.log(kv[1]) - math.log(pk["lambda"])))
        dev = abs(math.log(near[1]) - math.log(pk["lambda"])) / math.log(pk["lambda"]) * 100
        print(f"    lambda_fit={pk['lambda']:7.3f} (omega={pk['omega']:.2f}, gain={pk['stacked_gain']}) "
              f"-> nearest TFPT: {near[0]} ({dev:.0f}% off in ln)")

    # (3) Omori exponent vs TFPT rationals (secondary)
    ps = omori_p(curves)
    cands = {"2/3": 2/3, "3/4": 3/4, "5/6": 5/6, "1": 1.0, "6/5": 6/5, "5/4": 5/4, "4/3": 4/3}
    pbar = float(np.mean(ps))
    near = min(cands.items(), key=lambda kv: abs(kv[1] - pbar))
    # simple-rational look-elsewhere: low-denominator fractions are dense, so a noisy ~0.84 is
    # ALWAYS ~0% from some rational -- quantify that the 5/6 proximity carries no information.
    spread = max(ps) - min(ps)
    simples = sorted({a / b for b in range(1, 7) for a in range(1, 2 * b) if 0.5 < a / b < 1.5})
    n_in = sum(1 for s in simples if min(ps) <= s <= max(ps))
    tol = abs(near[1] - pbar)
    chance = min(1.0, n_in * 2 * tol / spread) if spread > 0 else 1.0
    print("\n  --- (3) Omori exponent (secondary, p~1 is generic) ---")
    print(f"    p per sequence: {[round(x,2) for x in ps]}  mean p={pbar:.3f} "
          f"-> nearest TFPT rational {near[0]}={near[1]:.3f} ({abs(near[1]-pbar)/pbar*100:.0f}% off)")
    print(f"    BUT per-seq scatter {min(ps):.2f}-{max(ps):.2f} (spread {spread:.2f}) already holds "
          f"{n_in} denom<=6 rationals; a noisy mean lands within {tol:.3f} of one ~{chance*100:.0f}% "
          f"of the time -> the 5/6 proximity is a 0-bit coincidence, not a signal.")

    verdict = (
        f"{len(curves)} aftershock sequences (up to ~5-6 comb periods, thousands of events). "
        + ("NO TFPT log-period is special after look-elsewhere (Bonferroni global p="
           f"{global_p:.2f} >= 0.05)" if global_p >= 0.05 else
           f"best TFPT log-period survives look-elsewhere (global p={global_p:.3f}) -> ESCALATE, "
           "independent cross-check (firewall: still only a universal-DSI shape match)")
        + f". Seismicity's own dominant log-period lambda_fit~{peaks[0]['lambda'] if peaks else '?'} "
        + "(seismology typically reports ~2). Firewall: earthquakes are not a horizon recovery, "
          "so this tests the SHAPE only, never TFPT physics.")
    print(f"\n==> {verdict}")

    out = {"mainshocks": meta, "battery": battery, "bonferroni_global_p": round(global_p, 4),
           "free_fit_peaks": peaks, "omori_p": [round(x, 3) for x in ps],
           "omori_p_mean": round(pbar, 3), "omori_nearest_rational": near[0],
           "omori_coincidence_chance": round(chance, 3), "verdict": verdict}
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "quake_tfpt_signatures.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'quake_tfpt_signatures.json'}")
    return out


if __name__ == "__main__":
    analyze()
