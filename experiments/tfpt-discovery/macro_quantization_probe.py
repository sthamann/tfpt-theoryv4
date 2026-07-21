#!/usr/bin/env python3
"""
MACRO.QUANT.01 -- macroscopic-quantization / forbidden-window probe (discovery sandbox).

User question (2026-07-21 signature round): "if reality is a discrete fixed-point
process, macroscopic observables should show (a) preferred sizes, (b) forbidden
windows, (c) the frozen TFPT tones -- do tornado widths, sunspot group areas or
the DIB catalog carry any of that?"  This probe runs the EXISTING frozen S7
size-space detector (vendored stacked comb statistic from recovery-comb-domains,
same import route as signature_coverage_audit.py) on three macroscopic worlds
plus one deliberate rounding POSITIVE control:

  D1  SPC tornado path widths  (yards,   1995-2024 era, human-estimated)
  D2  SPC tornado path lengths (miles,   1995-2024 era, human-estimated)
  D3  RGO/USAF sunspot group PEAK areas (uHem, 1874-2016, measured)
  D4  HURDAT2 hurricane max winds (kt)  -- KNOWN 5-kt reporting quantization;
      the battery MUST classify this as a reporting comb (detector validation)
  D5  Fan+2019 APO DIB catalog (557 optical bands, HD 183143 sightline file):
      frozen-comb range check + exploratory pair-spacing scan in wavenumber

Per size dataset: frozen tones omega_1/2/3 (S7), the BASE-10 REPORTING comb
omega_dec = 2*pi/ln(10) = 2.7288 (dangerously close to omega_1 = 2.5827:
resolvable only if ln-range > ~43 e-folds -- so on macro catalogs any omega_1
hit is a priori degenerate with decimal reporting; printed explicitly), a
divisibility census (multiples of 5/10/25/50/100 vs smooth expectation), a
free omega scan, and an FO.08-style FORBIDDEN-WINDOW search (largest interior
empty gap in ln v vs a smoothed-density bootstrap null).

FIREWALL (mandatory): tornadoes, hurricanes, sunspots and DIBs are surface /
atmospheric / photospheric / ISM-chemistry systems -- NOT boundary or horizon
recoveries.  No S15 transduction B is named for any of them, so every channel
here is EXPLORATORY SURFACE LEAKAGE by construction (SIGNATURES.md 0b.1).  A
null constrains nothing about the core; a hit would be an escalate-candidate
for independent replication only, never a claim, never a scorecard row without
promotion, never [E].

Data sources (raw files cached in data_macro/, gitignored; refetch on demand):
  D1/D2  https://www.spc.noaa.gov/wcm/data/1950-2024_actual_tornadoes.csv
  D3     https://solarscience.msfc.nasa.gov/greenwch/gYYYY.txt  (1874-2016)
  D4     https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2024-040425.txt
  D5     https://cdsarc.cds.unistra.fr/ftp/J/ApJ/878/151/hd183143.dat

Run:  cd <repo root> && experiments/tfpt-discovery/.venv/bin/python \
          experiments/tfpt-discovery/macro_quantization_probe.py
"""
from __future__ import annotations

import csv
import io
import json
import math
import sys
import urllib.request
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
DATA = HERE / "data_macro"
sys.path.insert(0, str(EXP / "recovery-comb-domains" / "src"))

from tfpt_combdomains.quake import _stacked_at, rate_curve  # noqa: E402

A = 6 * math.log(1.5)
B = 6 * math.log(3.0)
TONES = {
    "omega_1 2.583": 2 * math.pi / A,
    "omega_2 0.953": 2 * math.pi / B,
    "omega_3 1.511": 2 * math.pi / (B - A),
}
OMEGA_DEC = 2 * math.pi / math.log(10)          # 2.7288 -- decimal reporting comb
SEED = 41

# ----------------------------------------------------------------------
# data loaders (cached raw files; sources in module docstring)
# ----------------------------------------------------------------------


def _fetch(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists() or dest.stat().st_size == 0:
        req = urllib.request.Request(url, headers={"User-Agent": "tfpt-research/0.1"})
        with urllib.request.urlopen(req, timeout=120) as r:  # noqa: S310
            dest.write_bytes(r.read())
    return dest


def load_tornadoes() -> tuple[np.ndarray, np.ndarray]:
    """(widths_yd, lengths_mi) for 1995-2024 (modern reporting era), values > 0."""
    f = _fetch("https://www.spc.noaa.gov/wcm/data/1950-2024_actual_tornadoes.csv",
               DATA / "spc_tornadoes_1950_2024.csv")
    wid, length = [], []
    with f.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                yr = int(row["yr"])
                w = float(row["wid"])
                ln = float(row["len"])
            except (KeyError, ValueError):
                continue
            if yr >= 1995:
                if w > 0:
                    wid.append(w)
                if ln > 0:
                    length.append(ln)
    return np.array(wid), np.array(length)


def load_sunspot_peak_areas() -> np.ndarray:
    """Per-group PEAK corrected whole-spot area (uHem) from the RGO/USAF daily
    group records, 1874-2016 (14-field rows; field 3 = group number, field 8 =
    corrected whole-spot area; mapping validated on the April-1947 great spot)."""
    d = DATA / "rgo_groups"
    peak: dict[str, float] = {}
    for y in range(1874, 2017):
        f = _fetch(f"https://solarscience.msfc.nasa.gov/greenwch/g{y}.txt",
                   d / f"g{y}.txt")
        for line in f.read_text(errors="replace").splitlines():
            p = line.split()
            if len(p) != 14:
                continue
            try:
                area = float(p[8])
            except ValueError:
                continue
            # group key: number + decade disambiguates recycled NOAA numbers
            key = f"{p[3]}_{p[0][:3]}"
            if area > peak.get(key, 0.0):
                peak[key] = area
    vals = np.array([v for v in peak.values() if v > 0])
    return vals


def load_hurdat_winds() -> np.ndarray:
    """All 6-hourly max sustained winds (kt) from HURDAT2 Atlantic 1851-2024 --
    the deliberate reporting-quantization POSITIVE control (5-kt steps)."""
    f = _fetch("https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2024-040425.txt",
               DATA / "hurdat2_atl.txt")
    winds = []
    for line in f.read_text().splitlines():
        p = [x.strip() for x in line.split(",")]
        if len(p) > 7 and len(p[0]) == 8 and p[0].isdigit():
            try:
                w = float(p[6])
            except ValueError:
                continue
            if w > 0:
                winds.append(w)
    return np.array(winds)


def load_dib_wavelengths() -> np.ndarray:
    """cWav (Angstrom) of the 557 measured rows of the Fan+2019 APO DIB catalog
    (HD 183143 sightline file carries the full catalog wavelength column)."""
    f = _fetch("https://cdsarc.cds.unistra.fr/ftp/J/ApJ/878/151/hd183143.dat",
               DATA / "fan2019_hd183143.dat")
    wl = []
    for line in f.read_text().splitlines():
        try:
            wl.append(float(line[4:11]))
        except ValueError:
            continue
    return np.array(sorted(wl))


# ----------------------------------------------------------------------
# battery pieces
# ----------------------------------------------------------------------


def divisibility_census(vals: np.ndarray) -> dict:
    """Fraction of (near-)integer values divisible by k, vs the 1/k smooth
    expectation.  Excess factor >> 1 = human reporting quantization."""
    iv = vals[np.abs(vals - np.round(vals)) < 1e-9].astype(int)
    out = {"n_integer": int(len(iv)), "frac_integer": round(len(iv) / len(vals), 3)}
    if len(iv) < 50:
        return out
    for k in (5, 10, 25, 50, 100):
        frac = float(np.mean(iv % k == 0))
        out[f"div_{k}"] = {"frac": round(frac, 3), "excess": round(frac * k, 1)}
    return out


def _decade_quanta(vals: np.ndarray) -> dict[int, float]:
    """EFFECTIVE reporting quantum PER DECADE of magnitude = max(native grid,
    preferred human rounding step).  Native grid: min positive spacing of the
    unique values in the decade.  Preferred step: the largest k in {2,5,10,25,
    50,100,250,500} (scaled into the decade) whose decade-local divisibility
    excess is >= 2 -- e.g. tornado widths carry a 25/50-yd preference (16-25x
    excess), so 56-59 yd being absent between 55 and 60 is REPORTING, not
    physics (exactly the artefact class the first two probe iterations flagged:
    single empty fine cells and preferred-step holes; both recorded and killed
    here)."""
    quanta: dict[int, float] = {}
    dec = np.floor(np.log10(vals)).astype(int)
    for d in np.unique(dec):
        sel = vals[dec == d]
        u = np.unique(sel)
        df = np.diff(u)
        df = df[df > 0]
        if not len(df):
            continue
        q0 = float(np.min(df))
        best_k = 1
        # decade-local preferred rounding step (only meaningful on near-integer grids)
        scaled = sel / q0
        near_int = scaled[np.abs(scaled - np.round(scaled)) < 1e-6].astype(int)
        if len(near_int) >= 50:
            for k in (2, 5, 10, 25, 50, 100, 250, 500):
                if k * q0 >= 10.0 ** (d + 1):
                    break
                if float(np.mean(near_int % k == 0)) * k >= 2.0:
                    best_k = k
        quanta[int(d)] = best_k * q0
    return quanta


MIN_EMPTY_CELLS = 3          # a forbidden window must be RESOLVABLE: >= 3 empty
#                              admissible reporting cells between its edges


def _resolvable_gaps(uvals: np.ndarray, quanta: dict[int, float]) -> list[tuple[float, float, float, int]]:
    """(ln_gap, left_edge, right_edge, n_empty_cells) for consecutive unique
    values whose interval contains >= MIN_EMPTY_CELLS unoccupied grid values of
    the LOCAL reporting quantum.  Kills both first-round artefact classes: the
    'humans never report 11 yd' single-cell hole (1 empty cell) and the coarse-
    grid-edge ln(2) spacing between adjacent occupied cells (0 empty cells)."""
    decs = sorted(quanta)
    out = []
    for a, b in zip(uvals[:-1], uvals[1:]):
        d = int(np.clip(math.floor(math.log10(max(a, 1e-12))), decs[0], decs[-1]))
        q = quanta.get(d, quanta[decs[-1]])
        n_empty = max(0, int(math.floor((b - a) / q + 1e-9)) - 1)
        if n_empty >= MIN_EMPTY_CELLS:
            out.append((math.log(b / a), float(a), float(b), n_empty))
    return out


def forbidden_window(vals: np.ndarray, *, n_boot: int = 1000, seed: int = SEED) -> dict:
    """FO.08-style largest RESOLVABLE interior empty window in ln(v), against a
    decade-local grid-aware bootstrap null: samples come from a smooth
    (Gaussian-KDE) fit of the ln-density, snapped to the catalog's per-decade
    reporting grid, and the SAME resolvability rule (>= MIN_EMPTY_CELLS empty
    grid values) is applied.  Interior = central 98% of support."""
    lv = np.sort(np.log(vals))
    lo, hi = np.quantile(lv, [0.01, 0.99])
    core = np.exp(lv[(lv >= lo) & (lv <= hi)])
    if len(core) < 100:
        return {"n": int(len(core)), "p_value": 1.0}
    quanta = _decade_quanta(vals)
    decs = sorted(quanta)
    gaps = _resolvable_gaps(np.unique(core), quanta)
    if not gaps:
        return {"n": int(len(core)), "largest_gap_ln": 0.0, "gap_edges": None,
                "note": f"no interior window with >= {MIN_EMPTY_CELLS} empty reporting cells",
                "p_value": 1.0}
    gap_obs, a, b, n_empty = max(gaps)

    def snap(v: np.ndarray) -> np.ndarray:
        d = np.clip(np.floor(np.log10(np.maximum(v, 1e-12))).astype(int),
                    decs[0], decs[-1])
        q = np.array([quanta.get(int(x), quanta[decs[-1]]) for x in d])
        return np.maximum(q, np.round(v / q) * q)

    lcore = np.log(core)
    rng = np.random.default_rng(seed)
    bw = 1.06 * np.std(lcore) * len(lcore) ** (-1 / 5)
    hits = 0
    for _ in range(n_boot):
        s = rng.choice(lcore, size=len(lcore), replace=True) + rng.normal(0, bw, len(lcore))
        v = snap(np.exp(s))
        v = v[(np.log(v) >= lo) & (np.log(v) <= hi)]
        g = _resolvable_gaps(np.unique(v), quanta)
        if g and max(g)[0] >= gap_obs:
            hits += 1
    return {"n": int(len(core)), "decade_quanta": {str(k): v for k, v in quanta.items()},
            "largest_gap_ln": round(gap_obs, 4),
            "gap_edges": (round(a, 4), round(b, 4)), "n_empty_cells": n_empty,
            "p_value": round((1 + hits) / (n_boot + 1), 4)}


def robustness_battery(vals: np.ndarray, om: float) -> dict:
    """Anti-artefact battery for a nominal tone hit (same design as
    signature_coverage_audit.py): (a) binning battery -- the equal-ln histogram
    is an analysis CHOICE, a real comb must survive it; (b) event bootstrap;
    (c) detuned tones +-12% -- a sharp comb dies, broad-band structure does not.
    'robust' requires >= 4/6 binnings p < 0.05 AND bootstrap fraction >= 0.5
    AND both detuned p > 0.10."""
    binnings = [(60, 2), (80, 2), (100, 2), (80, 1), (80, 5), (64, 3)]
    bin_ps = []
    for nb, mc in binnings:
        t, y = rate_curve(vals, n_bins=nb, min_count=mc)
        bin_ps.append(_stacked_at([(t, y)], om, seed=SEED)["p_value"])
    rng = np.random.default_rng(3)
    boot_ps = []
    for _ in range(20):
        bs = rng.choice(vals, size=len(vals), replace=True)
        t, y = rate_curve(bs)
        boot_ps.append(_stacked_at([(t, y)], om, seed=SEED)["p_value"])
    t, y = rate_curve(vals)
    detuned = [_stacked_at([(t, y)], om * f, seed=SEED)["p_value"] for f in (0.88, 1.12)]
    robust = (sum(p < 0.05 for p in bin_ps) >= 4
              and float(np.mean(np.array(boot_ps) < 0.05)) >= 0.5
              and all(p > 0.10 for p in detuned))
    return {"binning_ps": [round(p, 4) for p in bin_ps],
            "bootstrap_frac_below_05": round(float(np.mean(np.array(boot_ps) < 0.05)), 2),
            "detuned_ps": [round(p, 4) for p in detuned],
            "robust": bool(robust)}


def free_scan(t: np.ndarray, y: np.ndarray, *, n_grid: int = 60) -> dict:
    """Data's own best omega in [0.6, 8] under the same stacked statistic."""
    grid = np.linspace(0.6, 8.0, n_grid)
    best = {"omega": None, "p": 1.0}
    for om in grid:
        r = _stacked_at([(t, y)], float(om), seed=SEED)
        if r["n_used"] and r["p_value"] < best["p"]:
            best = {"omega": round(float(om), 3), "p": r["p_value"],
                    "lambda": round(math.exp(2 * math.pi / om), 2)}
    return best


def run_size_channel(name: str, vals: np.ndarray, results: dict) -> None:
    span = float(np.log(vals.max() / vals.min()))
    f_res = 2 * math.pi / span
    t, y = rate_curve(vals)
    print(f"\n### {name}: n={len(vals)}, ln-range {span:.2f}, {len(t)} bins, "
          f"freq resolution ~{f_res:.3f}")
    ch: dict = {"n": int(len(vals)), "ln_range": round(span, 2), "tones": {}}
    deg = abs(TONES["omega_1 2.583"] - OMEGA_DEC) < f_res
    print(f"    |omega_1 - omega_dec| = {abs(TONES['omega_1 2.583'] - OMEGA_DEC):.3f}"
          f" vs resolution {f_res:.3f} -> omega_1 {'DEGENERATE with' if deg else 'resolvable from'}"
          " the base-10 reporting comb")
    ch["omega1_base10_degenerate"] = bool(deg)
    for label, om in TONES.items():
        r = _stacked_at([(t, y)], om, seed=SEED)
        ch["tones"][label] = r
        status = "range_blind" if r["n_used"] == 0 else (
            "NOMINAL" if r["p_value"] < 0.05 else "null")
        print(f"    {label:16s} n_used={r['n_used']} p={r['p_value']:.4f}  {status}")
        if status == "NOMINAL":
            rb = robustness_battery(vals, om)
            ch["tones"][label]["robustness"] = rb
            print(f"      anti-artefact battery: binning {rb['binning_ps']}, "
                  f"bootstrap frac<0.05 {rb['bootstrap_frac_below_05']}, "
                  f"detuned {rb['detuned_ps']} -> "
                  f"{'ROBUST (escalate: prereg on independent data)' if rb['robust'] else 'NOT robust, dropped'}")
    r_dec = _stacked_at([(t, y)], OMEGA_DEC, seed=SEED)
    ch["decade_comb"] = r_dec
    print(f"    base-10 comb     n_used={r_dec['n_used']} p={r_dec['p_value']:.4f}"
          f"  ({'REPORTING COMB PRESENT' if r_dec['p_value'] < 0.05 else 'quiet'})")
    cen = divisibility_census(vals)
    ch["divisibility"] = cen
    div_str = ", ".join(f"x{k}:{cen[f'div_{k}']['excess']}x"
                        for k in (5, 10, 25, 50, 100) if f"div_{k}" in cen)
    print(f"    divisibility census (excess over smooth): {div_str or 'n/a (non-integer)'}")
    fw = forbidden_window(vals)
    ch["forbidden_window"] = fw
    print(f"    forbidden-window: largest interior ln-gap "
          f"{fw.get('largest_gap_ln', 0)} between {fw.get('gap_edges')} "
          f"p={fw['p_value']:.3f}"
          f"  ({'GAP CANDIDATE' if fw['p_value'] < 0.05 else 'no forbidden zone'})")
    fs = free_scan(t, y)
    ch["free_scan"] = fs
    if fs["omega"] is not None:
        near_dec = abs(fs["omega"] - OMEGA_DEC) < f_res
        print(f"    free scan best: omega={fs['omega']} (lambda={fs['lambda']}) "
              f"p={fs['p']:.4f}{'  <- within resolution of base-10 comb' if near_dec else ''}")
        if fs["p"] < 0.05:
            rb = robustness_battery(vals, fs["omega"])
            ch["free_scan"]["robustness"] = rb
            print(f"      anti-artefact battery on the free peak: binning {rb['binning_ps']}, "
                  f"bootstrap frac<0.05 {rb['bootstrap_frac_below_05']}, "
                  f"detuned {rb['detuned_ps']} -> "
                  f"{'ROBUST' if rb['robust'] else 'NOT robust, dropped'}")
    results[name] = ch


def run_dib_channel(results: dict) -> None:
    wl = load_dib_wavelengths()
    nu = np.sort(1e8 / wl)                      # wavenumber cm^-1
    span = float(np.log(wl.max() / wl.min()))
    periods = span / math.log(1.5 ** 6)
    print(f"\n### D5 DIB catalog (Fan+2019, 557 bands {wl.min():.0f}-{wl.max():.0f} A)")
    print(f"    frozen-comb range check: ln-range {span:.3f} = {periods:.2f} periods of"
          f" (3/2)^6  ->  RANGE-BLIND by construction (gate 2.8): the optical DIB window"
          " can never carry the omega_1 comb.")
    # exploratory pair-spacing scan: preferred wavenumber differences?
    dmat = nu[None, :] - nu[:, None]
    d = dmat[(dmat > 2.0) & (dmat < 300.0)]
    bins = np.arange(2.0, 300.0, 2.0)
    h_obs, _ = np.histogram(d, bins=bins)
    stat_obs = float(h_obs.max() / max(1.0, np.median(h_obs)))
    rng = np.random.default_rng(SEED)
    bw = 1.06 * np.std(nu) * len(nu) ** (-1 / 5) * 0.5
    null_stats = []
    for _ in range(500):
        s = np.sort(rng.choice(nu, size=len(nu), replace=True)
                    + rng.normal(0, bw, len(nu)))
        dm = s[None, :] - s[:, None]
        dd = dm[(dm > 2.0) & (dm < 300.0)]
        h, _ = np.histogram(dd, bins=bins)
        null_stats.append(float(h.max() / max(1.0, np.median(h))))
    p = float((1 + np.sum(np.array(null_stats) >= stat_obs)) / 501)
    peak_at = float(bins[int(np.argmax(h_obs))])
    print(f"    exploratory pair-spacing scan (2-300 cm^-1, 2 cm^-1 bins): peak at"
          f" ~{peak_at:.0f} cm^-1, max/median = {stat_obs:.2f}, smooth-null p = {p:.3f}"
          f"  ({'PREFERRED SPACING candidate' if p < 0.05 else 'no preferred spacing'})")
    print("    (S15: no transduction B is named for ISM chemistry -- exploratory only)")
    results["D5_dib_catalog"] = {
        "n_bands": int(len(wl)), "ln_range": round(span, 3),
        "comb_periods": round(periods, 2), "range_blind": True,
        "pair_spacing": {"peak_cm1": peak_at, "stat": round(stat_obs, 2),
                         "p_value": round(p, 3)}}


def main() -> int:
    print("=" * 88)
    print("MACRO.QUANT.01 -- macroscopic quantization / forbidden windows / frozen tones")
    print("  FIREWALL: surface/atmospheric/photospheric/ISM channels, no named B ->")
    print("  exploratory surface leakage only; nulls constrain nothing about the core;")
    print("  any hit = escalate-candidate for independent replication, never a claim.")
    print("=" * 88)
    results: dict = {}

    wid, length = load_tornadoes()
    run_size_channel("D1_tornado_width_yd", wid, results)
    run_size_channel("D2_tornado_length_mi", length, results)

    areas = load_sunspot_peak_areas()
    run_size_channel("D3_sunspot_peak_area_uHem", areas, results)

    winds = load_hurdat_winds()
    print(f"\n### D4 HURDAT2 max winds (positive rounding control): n={len(winds)}")
    cen = divisibility_census(winds)
    results["D4_hurdat_winds_control"] = cen
    frac5 = cen.get("div_5", {}).get("frac", 0.0)
    ok = frac5 > 0.95
    print(f"    divisible by 5 kt: {frac5:.3f} (excess {cen.get('div_5', {}).get('excess')}x)"
          f"  -> control {'PASS (reporting quantization detected)' if ok else 'FAIL'}")
    results["D4_control_pass"] = bool(ok)

    run_dib_channel(results)

    out = HERE / "macro_quantization_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
