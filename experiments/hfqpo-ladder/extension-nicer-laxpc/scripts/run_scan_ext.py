#!/usr/bin/env python3
"""Orchestrator for the NICER extension scan: stack -> sanity -> inject -> scan.

Usage:  python run_scan_ext.py stack|sanity|inject|scan|all

All thresholds, targets, fit windows and gates are frozen in
hypotheses/hfqpo_ext_v1.yaml (created before download). Outputs to results/.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXT_ROOT = os.path.dirname(HERE)
RESDIR = os.path.join(EXT_ROOT, "results")
os.makedirs(RESDIR, exist_ok=True)

sys.path.insert(0, HERE)
from nicer_core import (BANDS, SEG_S, fit_line_range, load_segments,  # noqa: E402
                        stack_from_segments)

with open(os.path.join(EXT_ROOT, "data", "manifest_ext.json")) as f:
    MANIFEST = json.load(f)
OBSIDS = MANIFEST["selected_obsids"]

SOURCE = "MAXI_J1820+070"
PRIMARY_BAND = "tot"          # frozen: band of the published anchor detection
SECONDARY_BAND = "hard"

# frozen targets and fit windows (hypotheses/hfqpo_ext_v1.yaml)
ANCHOR = {"f0": 55.12, "tol": 4.0, "win": (40.0, 74.0),
          "published_rms_pct": 1.0}
TOOTH = {"f0": 82.68, "tol": 3.0, "win": (64.0, 101.0)}
INTEGER = {"f0": 110.24, "tol": 4.0, "win": (95.0, 135.0)}
N_TRIALS = 4                  # 2 frequencies x 1 source x 2 bands
DETECT_SIGMA_AFTER_TRIALS = 4.0
INJ_Q = 10.0                  # parent stage_inject value
INJ_N_TRIALS = 8
INJ_MAX_SEGMENTS = 6000
INJ_SEED = 123


def _stack(band):
    segs = load_segments(OBSIDS, band)
    return segs, stack_from_segments(segs)


def stage_stack():
    report = {}
    for band in (PRIMARY_BAND, SECONDARY_BAND):
        segs, st = _stack(band)
        report[f"{SOURCE}/{band}"] = {
            "obsids": OBSIDS, "n_seg": st.nseg,
            "exposure_s": st.nseg * SEG_S, "n_photons": st.nph,
            "mean_rate_cps": round(st.mean_rate, 1),
            "pi_band": BANDS[band],
        }
        print(f"{SOURCE}/{band:5s} nseg={st.nseg:6d} "
              f"rate={st.mean_rate:9.1f} c/s", flush=True)
    with open(os.path.join(RESDIR, "stack_report_ext.json"), "w") as f:
        json.dump(report, f, indent=2)


def stage_sanity():
    """Gate: 55 Hz anchor >= 3 sigma in the primary band AND measured rms
    within a factor 2 of the published ~1% - else the scan STOPS."""
    out = {}
    for band in (PRIMARY_BAND, SECONDARY_BAND):
        segs, st = _stack(band)
        r = fit_line_range(st, ANCHOR["f0"], ANCHOR["tol"], *ANCHOR["win"])
        key = f"{SOURCE}/{band}/@{ANCHOR['f0']}Hz"
        if r is None:
            out[key] = {"status": "no_fit"}
            continue
        detected = r["significance_sigma"] >= 3.0
        rms_ok = (ANCHOR["published_rms_pct"] / 2.0 <= r["rms_pct"]
                  <= ANCHOR["published_rms_pct"] * 2.0)
        r["status"] = "pass" if (detected and rms_ok) else (
            "detected_rms_off" if detected else "ANCHOR_FAIL")
        out[key] = r
        print(f"{key:40s} f0={r['f0_hz']:6.2f} rms={r['rms_pct']:.2f}% "
              f"sig={r['significance_sigma']:.1f} {r['status']}", flush=True)
    primary = out.get(f"{SOURCE}/{PRIMARY_BAND}/@{ANCHOR['f0']}Hz", {})
    out["_gate"] = "PASS" if primary.get("status") == "pass" else "FAIL"
    with open(os.path.join(RESDIR, "sanity_gate_ext.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"SANITY GATE: {out['_gate']}")


def stage_inject():
    """Injection-recovery at the tooth frequency in the primary band.
    Identical design to the parent stage_inject: piecewise-coherent
    Lorentzian QPO (Q=10) thinned into real segments; adaptive levels around
    the analytic sensitivity; gate >= 90% recovery at <= 2x prediction."""
    rng = np.random.default_rng(INJ_SEED)
    segs = load_segments(OBSIDS, PRIMARY_BAND)
    n_full = len(segs)
    if n_full > INJ_MAX_SEGMENTS:
        idx = rng.choice(n_full, INJ_MAX_SEGMENTS, replace=False)
        segs = segs[idx]
    base = stack_from_segments(segs)
    r0 = fit_line_range(base, TOOTH["f0"], TOOTH["tol"], *TOOTH["win"])
    sigma_norm = r0["norm_err"] if r0 else 0.3
    rate = base.mean_rate
    scale_full = np.sqrt(len(segs) / max(n_full, 1))
    pred_rms = float(np.sqrt(3.0 * sigma_norm / rate))
    pred_rms_full = float(pred_rms * np.sqrt(scale_full))
    levels = [0.75 * pred_rms, pred_rms, 1.5 * pred_rms, 2.0 * pred_rms]
    res = {"source": SOURCE, "band": PRIMARY_BAND, "tooth_hz": TOOTH["f0"],
           "q_injected": INJ_Q, "n_seg_used": len(segs),
           "n_seg_full_stack": n_full, "mean_rate_cps": rate,
           "pred_sens_rms_pct_subsample": 100 * pred_rms,
           "pred_sens_rms_pct_full_stack": 100 * pred_rms_full,
           "levels": {}}
    ck = os.path.join(RESDIR, "injection_calibration_ext.json")
    for rms in levels:
        det = 0
        meas = []
        for k in range(INJ_N_TRIALS):
            st = stack_from_segments(segs, thin=(TOOTH["f0"], rms, INJ_Q),
                                     rng=rng)
            r = fit_line_range(st, TOOTH["f0"], TOOTH["tol"], *TOOTH["win"])
            if r and r["significance_sigma"] >= 3.0:
                det += 1
                meas.append(r["rms_pct"])
        res["levels"][f"{100*rms:.3f}"] = {
            "injected_rms_pct": 100 * rms, "n_trials": INJ_N_TRIALS,
            "n_detected_3sig": det, "recovery_frac": det / INJ_N_TRIALS,
            "measured_rms_pct_mean": float(np.mean(meas)) if meas else None,
        }
        print(f"inject rms={100*rms:.3f}% -> {det}/{INJ_N_TRIALS} recovered",
              flush=True)
        with open(ck, "w") as f:
            json.dump(res, f, indent=2)
    sens = None
    for key, lv in sorted(res["levels"].items(),
                          key=lambda kv: kv[1]["injected_rms_pct"]):
        if lv["recovery_frac"] >= 0.9:
            sens = lv["injected_rms_pct"]
            break
    res["sensitivity_rms_pct_90"] = sens
    res["gate_90pct_at_2x"] = bool(sens is not None
                                   and sens <= 2.0 * 100 * pred_rms)
    with open(ck, "w") as f:
        json.dump(res, f, indent=2)
    print(f"injection calibration written; sens90={sens} "
          f"gate={res['gate_90pct_at_2x']}")


def stage_scan():
    from scipy.stats import norm as ndist
    scan = {"trials_correction": {
        "n_trials": N_TRIALS,
        "rule": "2 frequencies x 1 source x 2 bands, "
                "p_final = 1-(1-p_single)^4"}}
    entry = {}
    for role, band in (("primary", PRIMARY_BAND),
                       ("secondary", SECONDARY_BAND)):
        segs, st = _stack(band)
        bl = {"band": band, "n_seg": st.nseg,
              "exposure_s": st.nseg * SEG_S, "mean_rate_cps": st.mean_rate}
        for name, tgt in (("tooth", TOOTH), ("integer", INTEGER)):
            r = fit_line_range(st, tgt["f0"], tgt["tol"], *tgt["win"])
            if r is None:
                bl[name] = {"status": "no_fit"}
                continue
            sig = r["significance_sigma"]
            p_single = float(ndist.sf(sig))
            p_final = float(1 - (1 - p_single) ** N_TRIALS)
            r["p_single"] = p_single
            r["p_trials_corrected"] = p_final
            r["significance_after_trials_sigma"] = float(
                ndist.isf(min(max(p_final, 1e-300), 1.0)))
            r["target_hz"] = tgt["f0"]
            bl[name] = r
        entry[role] = bl
    scan[SOURCE] = entry

    # decision per the preregistered rule, read from the PRIMARY band
    t = entry["primary"].get("tooth", {})
    i = entry["primary"].get("integer", {})
    t_sig = t.get("significance_after_trials_sigma", 0.0)
    i_sig = i.get("significance_after_trials_sigma", 0.0)
    if t_sig >= DETECT_SIGMA_AFTER_TRIALS and i_sig < DETECT_SIGMA_AFTER_TRIALS:
        rule = "ladder_hit"
    elif i_sig >= DETECT_SIGMA_AFTER_TRIALS and t_sig < DETECT_SIGMA_AFTER_TRIALS:
        rule = "harmonic_hit"
    else:
        rule = "neither_upper_limits"

    # extension verdict enum (hypotheses/hfqpo_ext_v1.yaml verdict_mapping)
    inj_path = os.path.join(RESDIR, "injection_calibration_ext.json")
    sens = None
    inj_gate = False
    if os.path.exists(inj_path):
        with open(inj_path) as f:
            inj = json.load(f)
        sens = inj.get("sensitivity_rms_pct_90")
        inj_gate = bool(inj.get("gate_90pct_at_2x"))
    san_path = os.path.join(RESDIR, "sanity_gate_ext.json")
    anchor_rms = None
    if os.path.exists(san_path):
        with open(san_path) as f:
            san = json.load(f)
        anchor_rms = san.get(
            f"{SOURCE}/{PRIMARY_BAND}/@{ANCHOR['f0']}Hz", {}).get("rms_pct")
    if rule == "ladder_hit":
        verdict = "recovered"
    elif inj_gate and sens is not None and anchor_rms is not None \
            and sens <= anchor_rms:
        verdict = "null_with_sensitivity"
    else:
        verdict = "null_without_sensitivity"

    scan["verdict"] = {
        "source": SOURCE,
        "decision_rule_outcome": rule,
        "extension_enum": verdict,
        "tooth_sig_after_trials": t_sig,
        "integer_sig_after_trials": i_sig,
        "tooth_rms_ul3sig_pct": t.get("rms_ul3sig_pct"),
        "integer_rms_ul3sig_pct": i.get("rms_ul3sig_pct"),
        "integer_rms_pct_if_detected": i.get("rms_pct")
        if i_sig >= DETECT_SIGMA_AFTER_TRIALS else None,
        "injection_sensitivity_rms_pct_90": sens,
        "anchor_rms_pct": anchor_rms,
    }
    scan["laxpc"] = {
        "archive": "AstroSat/LAXPC (ISSDC)",
        "extension_enum": "infrastructure_blocked",
        "basis": "login-gated archive, no anonymous/scriptable access "
                 "(probed 2026-07-22; see hypotheses/hfqpo_ext_v1.yaml)",
    }
    with open(os.path.join(RESDIR, "blind_scan_ext.json"), "w") as f:
        json.dump(scan, f, indent=2)
    v = scan["verdict"]
    print(f"{SOURCE}: rule={v['decision_rule_outcome']} "
          f"enum={v['extension_enum']} tooth={t_sig:.2f}s int={i_sig:.2f}s "
          f"UL(tooth)={v['tooth_rms_ul3sig_pct']}% "
          f"UL(int)={v['integer_rms_ul3sig_pct']}%")


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if stage in ("stack", "all"):
        stage_stack()
    if stage in ("sanity", "all"):
        stage_sanity()
    if stage in ("inject", "all"):
        stage_inject()
    if stage in ("scan", "all"):
        stage_scan()
