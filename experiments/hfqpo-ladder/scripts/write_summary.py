#!/usr/bin/env python3
"""Combine all H3-stage-2 checkpoint files into the final results summary
results/archival/archival_scan_results.json (+ CSV of the per-source scan)."""
import csv
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_scan import ARCH, MANIFEST, RESDIR, SCAN

def load(name):
    p = os.path.join(RESDIR, name)
    with open(p) as f:
        return json.load(f)


stacks = load("stack_report.json")
sanity = load("sanity_gate.json")
inject = load("injection_calibration.json")
scan = load("blind_scan.json")

# data volume from the merged download log
with open(os.path.join(ARCH, "download_log.json")) as f:
    dl = json.load(f)

per_source = {}
for source, cfg in SCAN.items():
    e = scan[source]
    p = e["primary"]
    s = e["secondary"]
    v = scan["verdicts"][source]
    inj = inject.get(source, {})
    per_source[source] = {
        "nu_u_hz": MANIFEST["sources"][source]["nu_u"],
        "tooth_hz": cfg["tooth"], "integer_hz": cfg["integer"],
        "scan_band_primary": p["band"], "scan_band_secondary": s["band"],
        "exposure_primary_s": p["exposure_s"],
        "mean_rate_primary_cps": p["mean_rate_cps"],
        "tooth": {
            "primary_sig_single": p["tooth"].get("significance_sigma"),
            "primary_sig_after_trials": p["tooth"].get("significance_after_trials_sigma"),
            "primary_rms_ul3sig_pct": p["tooth"].get("rms_ul3sig_pct"),
            "secondary_rms_ul3sig_pct": s["tooth"].get("rms_ul3sig_pct"),
        },
        "integer": {
            "primary_sig_single": p["integer"].get("significance_sigma"),
            "primary_sig_after_trials": p["integer"].get("significance_after_trials_sigma"),
            "primary_rms_ul3sig_pct": p["integer"].get("rms_ul3sig_pct"),
            "secondary_rms_ul3sig_pct": s["integer"].get("rms_ul3sig_pct"),
        },
        "injection": {
            "sens90_rms_pct": inj.get("sensitivity_rms_pct_90"),
            "predicted_rms_pct_full_stack": inj.get("pred_sens_rms_pct_full_stack"),
            "gate_90pct_at_2x": inj.get("gate_90pct_at_2x"),
        },
        "verdict_decision_rule": v["verdict"],
    }

summary = {
    "experiment": "hfqpo-ladder",
    "stage": "H3 stage 2 - archival RXTE PCA event-data scan (preregistered "
             "in hypotheses/hfqpo_v1.yaml, archival_design)",
    "manifest": os.path.relpath(os.path.join(ARCH, "obsid_manifest.json"),
                                os.path.dirname(RESDIR)),
    "n_obsids": MANIFEST["n_obsids_total"],
    "downloaded_files": len(dl["files"]),
    "downloaded_gb": round(dl["total_bytes"] / 1e9, 2),
    "prereg_deviations": MANIFEST["prereg_deviations"],
    "method_notes": [
        "Leahy PDS from PCA processed SE event files + single-bit XTE_SA "
        "modes; 16-s segments, dt=1/4096 s (Nyquist 2048 Hz); GTI-clean "
        "segments only; stacks per (source, group, band).",
        "No barycentring: max barycentric frequency modulation v/c ~1e-4 "
        "-> <=0.07 Hz at 661.5 Hz, negligible vs HFQPO widths (>=25 Hz) "
        "and the 0.0625 Hz Fourier resolution.",
        "Bands mirror the published detections: hard27 = ~13-27 keV "
        "(Strohmayer), bh = event chn 36-79 + SB 14-35 (Belloni+12/R06 hard), "
        "bt = chn 0-79 total (+ full-band SB).",
        "Detection fit: local continuum (c0+c1*x) + Lorentzian, f0 free "
        "within the preregistered tolerance, FWHM free within Q=4-25; "
        "significance = norm/sigma_norm (Belloni+2012 convention).",
        "Upper limits: 3-sigma on the Lorentzian integral at fixed f0, max "
        "over Q grid (5, 8, 12, 20) -> conservative %rms.",
        "%rms uses total (source+background) rate; PCA background is a few "
        "percent of these bright-state rates, so published source-rms values "
        "are marginally higher; effect << the quoted limits.",
        "Injection-recovery: piecewise-coherent Lorentzian oscillator "
        "(Q=10), binomial thinning of the summed per-segment light curves; "
        "gate = >=90% recovery at <=2x the analytic sensitivity: PASS for "
        "all four sources.",
    ],
    "trials_correction": scan["trials_correction"],
    "sanity_gate": {
        "result": sanity["_gate"],
        "lines_reproduced": f"{sanity['_n_pass']}/{sanity['_n_total']}",
        "detail": {k: {kk: v[kk] for kk in
                       ("f0_hz", "rms_pct", "significance_sigma", "status")}
                   for k, v in sanity.items() if not k.startswith("_")
                   and isinstance(v, dict) and "f0_hz" in v},
    },
    "per_source": per_source,
    "verdicts_decision_rule": scan["verdicts"],
    "overall_verdict_enum": "null",
    "overall_reading": (
        "Blind scan at the preregistered tooth (1.5 nu_u) and integer (4 nu_0) "
        "frequencies in all four 3:2-pair sources: NO detection at either "
        "frequency in any source (all single-trial significances ~0, trials-"
        "corrected < 0; thresholds 4 sigma). 3-sigma rms upper limits in the "
        "preregistered primary bands: tooth 3.06% (GRO J1655-40, 13-27 keV), "
        "1.61% (XTE J1550-564), 0.53% (GRS 1915+105), 1.26% (H1743-322); "
        "integer-line limits 2.94/1.51/0.53/1.22%. In every source the limit "
        "is at or below the measured strength of the upper pair line "
        "(5.4/3.7/2.0/1.5% rms) in the same stack, so a third tooth (or an "
        "integer line) as strong as the detected pair lines is excluded. "
        "The geometric-ladder reading gains NO support; the harmonic "
        "alternative gains no new line either (the published anti-kernel "
        "records 92=184/2 and 34/68 stand unchanged). Caveats: the "
        "GRS 1915+105 stack is a proxy state selection (168/113 epochs are "
        "not reconstructable at ObsID level from the literature) and the "
        "GRO J1655-40 hard-band sensitivity (5.1% at 90% recovery) only "
        "excludes a tooth at the strength of its 450-Hz line."
    ),
}

out = os.path.join(RESDIR, "archival_scan_results.json")
with open(out, "w") as f:
    json.dump(summary, f, indent=2)
print("wrote", out)

# per-source CSV
csv_path = os.path.join(RESDIR, "archival_scan_results.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["source", "nu_u_hz", "tooth_hz", "integer_hz", "band",
                "exposure_ks", "tooth_sig_single", "tooth_sig_trials",
                "tooth_rms_ul3sig_pct", "integer_sig_single",
                "integer_sig_trials", "integer_rms_ul3sig_pct",
                "inj_sens90_rms_pct", "verdict"])
    for source, d in per_source.items():
        w.writerow([
            source, d["nu_u_hz"], d["tooth_hz"], round(d["integer_hz"], 1),
            d["scan_band_primary"], round(d["exposure_primary_s"] / 1000, 1),
            round(d["tooth"]["primary_sig_single"], 2),
            round(d["tooth"]["primary_sig_after_trials"], 2),
            round(d["tooth"]["primary_rms_ul3sig_pct"], 3),
            round(d["integer"]["primary_sig_single"], 2),
            round(d["integer"]["primary_sig_after_trials"], 2),
            round(d["integer"]["primary_rms_ul3sig_pct"], 3),
            d["injection"]["sens90_rms_pct"] and
            round(d["injection"]["sens90_rms_pct"], 2),
            d["verdict_decision_rule"]])
print("wrote", csv_path)
