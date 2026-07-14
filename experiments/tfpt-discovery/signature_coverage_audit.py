#!/usr/bin/env python3
"""
FRACTAL.HUNT.05 -- signature COVERAGE AUDIT after the fractal-string round.

Question (user): "are all signatures tested everywhere, and did the new
insights create signatures nobody has tested yet?"

Part 1: census matrix signature x channel-domain, statuses sourced from
        SIGNATURES.md, the experiment results JSONs and
        new_tone_posthoc_results.json (2026-07-13). Prints the gap list.
Part 2: CLOSES the closable gaps immediately -- the new tones have only been
        scanned in TIME-recovery curves (new_tone_posthoc_scan.py); the
        SIZE/ENERGY-distribution channels (S7 family) were never scanned at
        the new tones. Runs the frozen stacked detector on:
          * UHECR Auger open data, ln(E) distribution (3 detector streams)
          * pulsar glitch SIZES df_f (JBO catalog)
          * pulsar glitch recovery TIMESCALES tau_d (Yu+2013)
          * FRB 20201124A burst fluences (FAST)
        All post-hoc, exploration only; any p < 0.05 = escalate_candidate.

Firewall: discovery sandbox; distributions are S7-type search targets ("size-
space DSI"), not horizon recoveries; nothing here is a claim or scorecard row.

Run:  cd experiments/tfpt-discovery && .venv/bin/python signature_coverage_audit.py
"""
from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "recovery-comb-domains" / "src"))

from tfpt_combdomains.quake import _stacked_at, rate_curve  # noqa: E402

A = 6 * math.log(1.5)
B = 6 * math.log(3.0)
TONES = {
    "omega_1 2.583 (ref)": 2 * math.pi / A,
    "omega_2 0.953": 2 * math.pi / B,
    "omega_3 1.511": 2 * math.pi / (B - A),
    "res 2.749": 2.749026,
    "res 3.796": 3.796156,
    "res 4.911": 4.911247,
    "res 5.559": 5.558893,
}

# ======================================================================
# PART 1 -- census (statuses sourced; "UNTESTED*" = closable with repo data)
# ======================================================================
# channel-domain buckets actually used across the experiments
CHANNELS = [
    "time: GW ringdown envelope", "time: FRB burst tails", "time: magnetar",
    "time: GRB afterglow", "time: quake rate", "time: ENT fade",
    "time: crust cooling", "time: LSCO ln(w/T)", "time: Vela nudot",
    "dist: UHECR ln E", "dist: glitch sizes", "dist: FRB energy/fluence",
    "dist: glitch tau_d", "internal: quantum sim",
]
S = {}  # (signature, channel) -> status; default "n/a or untested-by-design"


def set_row(sig, mapping):
    for ch, st in mapping.items():
        S[(sig, ch)] = st


# classic signatures (source: SIGNATURES.md 2026-07-06 + experiment READMEs)
set_row("S1 static teeth (2/3)^k", {
    "time: FRB burst tails": "null", "time: GRB afterglow": "n/t",
    "time: quake rate": "null", "dist: FRB energy/fluence": "null",
    "time: GW ringdown envelope": "null(UL)", "dist: glitch sizes": "null",
    "internal: quantum sim": "exact"})
set_row("S2b omega_1 comb", {
    "time: GW ringdown envelope": "range_blind", "time: FRB burst tails": "null",
    "time: magnetar": "null", "time: GRB afterglow": "null",
    "time: quake rate": "null", "time: ENT fade": "null",
    "time: crust cooling": "null(stack)", "time: LSCO ln(w/T)": "null",
    "time: Vela nudot": "range_blind", "dist: UHECR ln E": "null",
    "dist: glitch sizes": "null", "internal: quantum sim": "exact"})
set_row("S4 Moebius (3/2)^{3,4,12}", {
    "time: FRB burst tails": "null", "time: magnetar": "null",
    "time: GRB afterglow": "null", "time: quake rate": "null",
    "dist: UHECR ln E": "null/range_blind"})
set_row("S7 size-space DSI @ omega_1", {
    "dist: UHECR ln E": "null", "dist: glitch sizes": "null",
    "dist: FRB energy/fluence": "null"})

# NEW tones (source: new_tone_posthoc_results.json, 2026-07-13 -- TIME domain)
set_row("F omega_2 0.953", {
    "time: GW ringdown envelope": "range_blind", "time: FRB burst tails": "range_blind",
    "time: magnetar": "range_blind", "time: GRB afterglow": "range_blind",
    "time: quake rate": "range_blind", "time: ENT fade": "range_blind",
    "time: crust cooling": "range_blind", "time: LSCO ln(w/T)": "range_blind",
    "time: Vela nudot": "range_blind",
    "dist: UHECR ln E": "UNTESTED*", "dist: glitch sizes": "UNTESTED*",
    "dist: FRB energy/fluence": "UNTESTED*", "dist: glitch tau_d": "UNTESTED*"})
set_row("F omega_3 1.511", {
    "time: quake rate": "null", "time: GW ringdown envelope": "range_blind",
    "time: FRB burst tails": "range_blind", "time: GRB afterglow": "range_blind",
    "dist: UHECR ln E": "UNTESTED*", "dist: glitch sizes": "UNTESTED*",
    "dist: FRB energy/fluence": "UNTESTED*", "dist: glitch tau_d": "UNTESTED*"})
set_row("F res-tones 2.75/3.80/4.91/5.56", {
    "time: GW ringdown envelope": "null", "time: FRB burst tails": "null",
    "time: magnetar": "null", "time: GRB afterglow": "null(prereg!)",
    "time: quake rate": "null", "time: ENT fade": "null",
    "time: crust cooling": "null", "time: LSCO ln(w/T)": "null",
    "time: Vela nudot": "null",
    "dist: UHECR ln E": "UNTESTED*", "dist: glitch sizes": "UNTESTED*",
    "dist: FRB energy/fluence": "UNTESTED*", "dist: glitch tau_d": "UNTESTED*"})

# structurally NEW signature concepts with NO detector yet (open)
NO_DETECTOR = [
    ("F two-tone JOINT comb (omega_1+omega_2 coherent, weight (1/3)^6)",
     "needs a 2-frequency matched filter with fixed amplitude ratio; "
     "eps_2 visibility ~ 3e-4 -> likely quantum-sim / stacked-only"),
    ("F rank-2 module fit (2D (k,l) grid instead of 1D comb)",
     "fit peaks at {k*a+m*b} jointly; distinguishes true two-ratio string "
     "from single-tone DSI -- no detector exists in any experiment"),
    ("F nonlattice amplitude damping (tooth decays like t^{sigma-D})",
     "the comb amplitude should DECAY across ln t if the string is "
     "nonlattice; all current detectors assume constant eps -- reanalysis "
     "hook for future wide-ln(t) data"),
]

SIGS = ["S1 static teeth (2/3)^k", "S2b omega_1 comb", "S4 Moebius (3/2)^{3,4,12}",
        "S7 size-space DSI @ omega_1", "F omega_2 0.953", "F omega_3 1.511",
        "F res-tones 2.75/3.80/4.91/5.56"]


def print_census():
    print("=" * 100)
    print("PART 1 -- signature x channel census (sources: SIGNATURES.md, results "
          "JSONs, new_tone_posthoc_results.json)")
    print("=" * 100)
    w0 = max(len(s) for s in SIGS) + 2
    print(" " * w0 + " | ".join(f"{c.split(': ')[1][:12]:12s}" for c in CHANNELS))
    for sig in SIGS:
        row = [S.get((sig, ch), "-") for ch in CHANNELS]
        print(f"{sig:{w0}s}" + " | ".join(f"{st[:12]:12s}" for st in row))
    gaps = [(sig, ch) for sig in SIGS for ch in CHANNELS
            if S.get((sig, ch), "") == "UNTESTED*"]
    print(f"\nclosable gaps (UNTESTED* with data in repo): {len(gaps)}")
    print("open concepts WITHOUT a detector anywhere:")
    for name, why in NO_DETECTOR:
        print(f"  - {name}\n      {why}")
    return gaps


# ======================================================================
# PART 2 -- close the closable gaps: new tones on the DISTRIBUTION channels
# ======================================================================
def load_uhecr() -> list[tuple[str, np.ndarray]]:
    d = EXP / "uhecr-energy-dsi" / "data" / "summary"
    out = []
    for f in sorted(d.glob("dataSummary*.csv")):
        es = []
        with f.open(encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            for row in rd:
                try:
                    e = float(row.get("sd_energy", "") or 0)
                except ValueError:
                    continue
                if e > 0:
                    es.append(e)
        if len(es) >= 100:
            out.append((f.stem.replace("dataSummary", "UHECR_"), np.array(es)))
    return out


def load_glitch_sizes() -> list[tuple[str, np.ndarray]]:
    f = EXP / "pulsar-glitch-recovery" / "data" / "jbo_glitches.csv"
    if not f.exists():
        return []
    vals = []
    with f.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                v = float(row.get("df_f", "") or 0)
            except ValueError:
                continue
            if v > 0:
                vals.append(v)
    return [("JBO_glitch_sizes_df_f", np.array(vals))] if len(vals) >= 100 else []


def load_glitch_taud() -> list[tuple[str, np.ndarray]]:
    f = EXP / "pulsar-glitch-recovery" / "data" / "yu2013_recovery.csv"
    if not f.exists():
        return []
    vals = []
    with f.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                v = float(row.get("tau_d", "") or 0)
            except ValueError:
                continue
            if v > 0:
                vals.append(v)
    return [("Yu2013_recovery_tau_d", np.array(vals))] if len(vals) >= 50 else []


def load_frb_fluence() -> list[tuple[str, np.ndarray]]:
    f = EXP / "repeater-cascade" / "data" / "frb20201124a_fast.csv"
    if not f.exists():
        return []
    by_ep: dict[str, list[float]] = {}
    with f.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                v = float(row.get("fluence_jyms", "") or 0)
            except ValueError:
                continue
            if v > 0:
                by_ep.setdefault(row.get("episode", "?"), []).append(v)
    return [(f"FRB20201124A_{ep}", np.array(vs)) for ep, vs in sorted(by_ep.items())
            if len(vs) >= 200]


def robustness_battery(vals: np.ndarray, om: float) -> dict:
    """Anti-artefact battery for a nominal distribution-channel hit: (a) binning
    battery (the equal-ln histogram is an analysis CHOICE -- a real comb must
    survive it), (b) event bootstrap, (c) detuned tones +-12% (a sharp comb dies,
    broad-band structure does not). Verdict 'robust' requires: >= 4/6 binnings
    p < 0.05 AND bootstrap fraction < 0.05 of at least 0.5 AND both detuned p > 0.1."""
    binnings = [(60, 2), (80, 2), (100, 2), (80, 1), (80, 5), (64, 3)]
    bin_ps = []
    for nb, mc in binnings:
        t, y = rate_curve(vals, n_bins=nb, min_count=mc)
        bin_ps.append(_stacked_at([(t, y)], om, seed=41)["p_value"])
    rng = np.random.default_rng(3)
    boot_ps = []
    for _ in range(20):
        bs = rng.choice(vals, size=len(vals), replace=True)
        t, y = rate_curve(bs)
        boot_ps.append(_stacked_at([(t, y)], om, seed=41)["p_value"])
    t, y = rate_curve(vals)
    detuned = [_stacked_at([(t, y)], om * f, seed=41)["p_value"] for f in (0.88, 1.12)]
    robust = (sum(p < 0.05 for p in bin_ps) >= 4
              and float(np.mean(np.array(boot_ps) < 0.05)) >= 0.5
              and all(p > 0.10 for p in detuned))
    return {"binning_ps": [round(p, 4) for p in bin_ps],
            "bootstrap_median_p": round(float(np.median(boot_ps)), 4),
            "bootstrap_frac_below_05": round(float(np.mean(np.array(boot_ps) < 0.05)), 2),
            "detuned_ps": [round(p, 4) for p in detuned],
            "robust": bool(robust)}


def scan_distributions() -> dict:
    print("\n" + "=" * 100)
    print("PART 2 -- close the gaps: NEW tones on the size/energy DISTRIBUTIONS "
          "(post-hoc, exploration only)")
    print("=" * 100)
    datasets = load_uhecr() + load_glitch_sizes() + load_glitch_taud() + load_frb_fluence()
    data_by_name = {n: v for n, v in datasets}
    results: dict = {}
    escal = []
    for name, vals in datasets:
        t, y = rate_curve(vals)          # equal-ln bins -> (center, ln count)
        span = float(np.log(vals.max() / vals.min()))
        print(f"\n### {name}: {len(vals)} events, ln-range {span:.1f}, "
              f"{len(t)} bins")
        results[name] = {"n_events": int(len(vals)), "ln_range": round(span, 2),
                         "tones": {}}
        gated = []
        for label, om in TONES.items():
            r = _stacked_at([(t, y)], om, seed=41)
            results[name]["tones"][label] = {"omega": round(om, 4), **r}
            is_new = "ref" not in label
            status = ("range_blind" if r["n_used"] == 0 else
                      ("ESCALATE_CANDIDATE" if (r["p_value"] < 0.05 and is_new)
                       else ("nominal (ref)" if r["p_value"] < 0.05 else "null")))
            if is_new and r["n_used"] > 0:
                gated.append((label, r["p_value"]))
            if status == "ESCALATE_CANDIDATE":
                escal.append((name, label, r["p_value"]))
            print(f"  {label:22s} n_used={r['n_used']}  p={r['p_value']:.4f}  {status}")
        if gated:
            m = len(gated)
            best = min(gated, key=lambda kv: kv[1])
            gp = min(1.0, best[1] * m)
            results[name]["bonferroni_new_tones"] = {
                "n_gated": m, "best": best[0], "best_p": best[1], "global_p": round(gp, 4)}
            print(f"  -> Bonferroni over {m} gated new tones: best {best[0]} "
                  f"p={best[1]:.4f}, global p={gp:.3f}"
                  + ("  <-- survives, ESCALATE" if gp < 0.05 else ""))
    print("\n" + "-" * 100)
    if escal:
        print("nominal distribution-channel candidates -> running the anti-artefact "
              "battery (binning / bootstrap / detuning / base-10 degeneracy) on each:")
        om_decade = 2 * math.pi / math.log(10)      # 2.7288: DECIMAL-reporting comb
        for n, l, p in escal:
            om = TONES[l]
            vals = data_by_name[n]
            rb = robustness_battery(vals, om)
            # base-10 degeneracy: catalogs with rounded/human-reported values carry
            # a mantissa (decade) comb at 2pi/ln10; if the tested tone is within the
            # frequency resolution of it AND the decade comb fits as well, the hit
            # is a reporting artefact, not physics.
            span = float(np.log(vals.max() / vals.min()))
            f_res = 2 * math.pi / span
            t, y = rate_curve(vals)
            r_dec = _stacked_at([(t, y)], om_decade, seed=41)
            base10_degenerate = (abs(om - om_decade) < f_res
                                 and r_dec["p_value"] <= max(0.05, p))
            rb["decade_comb_p"] = r_dec["p_value"]
            rb["decade_comb_gain"] = r_dec["gain"]
            rb["base10_degenerate"] = bool(base10_degenerate)
            results[n]["tones"][l]["robustness"] = rb
            if rb["robust"] and base10_degenerate:
                verdict = ("statistically robust BUT indistinguishable from the "
                           "base-10 reporting comb 2pi/ln10 = 2.7288 (decade comb "
                           f"p={r_dec['p_value']:.4f}, gain {r_dec['gain']}) -> "
                           "DECIMAL-ROUNDING ARTEFACT, dropped")
            elif rb["robust"]:
                verdict = "ROBUST -> escalate (needs prereg on independent data)"
            else:
                verdict = "NOT robust -> binning/fluctuation artefact, dropped"
            print(f"  {n} :: {l} (nominal p={p:.4f})")
            print(f"    binning p = {rb['binning_ps']}")
            print(f"    bootstrap: median p = {rb['bootstrap_median_p']}, "
                  f"frac<0.05 = {rb['bootstrap_frac_below_05']}")
            print(f"    detuned +-12%: p = {rb['detuned_ps']}")
            print(f"    decade-comb control: p = {r_dec['p_value']:.4f} "
                  f"(|om - 2pi/ln10| = {abs(om - om_decade):.4f} vs resolution {f_res:.3f})")
            print(f"    -> {verdict}")
    else:
        print("NO new tone is nominally special in any gated distribution channel -> "
              "clean post-hoc NULL; the S7 size-space coverage of the new tones is "
              "now COMPLETE on in-repo data.")
    return results


def main() -> int:
    gaps = print_census()
    results = scan_distributions()
    out = HERE / "signature_coverage_results.json"
    out.write_text(json.dumps({"closable_gaps_before": len(gaps),
                               "no_detector_concepts": [n for n, _ in NO_DETECTOR],
                               "distribution_scan": results}, indent=2),
                   encoding="utf-8")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
