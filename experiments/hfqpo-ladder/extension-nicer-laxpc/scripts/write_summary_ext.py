#!/usr/bin/env python3
"""Combine the extension stage outputs into one deterministic summary JSON."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EXT_ROOT = os.path.dirname(HERE)
RESDIR = os.path.join(EXT_ROOT, "results")


def load(name):
    p = os.path.join(RESDIR, name)
    with open(p) as f:
        return json.load(f)


def main():
    stack = load("stack_report_ext.json")
    sanity = load("sanity_gate_ext.json")
    inject = load("injection_calibration_ext.json")
    scan = load("blind_scan_ext.json")
    with open(os.path.join(EXT_ROOT, "data", "manifest_ext.json")) as f:
        manifest = json.load(f)

    v = scan["verdict"]
    anchor = sanity.get("MAXI_J1820+070/tot/@55.12Hz", {})
    summary = {
        "experiment": "hfqpo-ladder / extension-nicer-laxpc",
        "prereg": "hypotheses/hfqpo_ext_v1.yaml (frozen 2026-07-22 before download)",
        "verdicts": {
            "NICER_MAXI_J1820+070": {
                "extension_enum": v["extension_enum"],
                "decision_rule_outcome": v["decision_rule_outcome"],
            },
            "AstroSat_LAXPC": {
                "extension_enum": "infrastructure_blocked",
                "basis": scan["laxpc"]["basis"],
            },
            "NICER_GRS_1915+105": {
                "extension_enum": "not_selected",
                "basis": "no published NICER anchor line; see prereg "
                         "archive_selection",
            },
            "NICER_MAXI_J1535-571": {
                "extension_enum": "not_selected",
                "basis": "no published HFQPO -> no frozen target",
            },
            "NuSTAR": {
                "extension_enum": "not_selected",
                "basis": "dead-time-capped sensitivity an order of magnitude "
                         "below NICER on the same source",
            },
        },
        "data": {
            "obsids_selected": manifest["selected_obsids"],
            "bytes_downloaded": manifest["selected_bytes_total"],
            "budget_gb": manifest["budget_gb"],
            "n_seg_primary": stack["MAXI_J1820+070/tot"]["n_seg"],
            "exposure_s_primary": stack["MAXI_J1820+070/tot"]["exposure_s"],
            "mean_rate_cps_primary":
                stack["MAXI_J1820+070/tot"]["mean_rate_cps"],
        },
        "sanity_gate": {
            "gate": sanity["_gate"],
            "anchor_f0_hz": anchor.get("f0_hz"),
            "anchor_rms_pct": anchor.get("rms_pct"),
            "anchor_sig": anchor.get("significance_sigma"),
        },
        "injection": {
            "gate_90pct_at_2x": inject["gate_90pct_at_2x"],
            "sensitivity_rms_pct_90": inject["sensitivity_rms_pct_90"],
            "pred_sens_rms_pct": inject["pred_sens_rms_pct_full_stack"],
            "tooth_hz": inject["tooth_hz"],
            "q_injected": inject["q_injected"],
        },
        "blind_scan": {
            "tooth": {
                "target_hz": 82.68,
                "sig_after_trials": v["tooth_sig_after_trials"],
                "rms_ul3sig_pct": v["tooth_rms_ul3sig_pct"],
            },
            "integer": {
                "target_hz": 110.24,
                "sig_single_trial":
                    scan["MAXI_J1820+070"]["primary"]["integer"]
                    ["significance_sigma"],
                "sig_after_trials": v["integer_sig_after_trials"],
                "rms_pct_at_fit":
                    scan["MAXI_J1820+070"]["primary"]["integer"]["rms_pct"],
                "rms_ul3sig_pct": v["integer_rms_ul3sig_pct"],
                "note": "3.82 sigma after trials - BELOW the preregistered "
                        "4 sigma threshold; consistent with the weak second "
                        "harmonic reported in ATel #11951; reported as a "
                        "sub-threshold excess, not a detection",
            },
        },
    }
    out = os.path.join(RESDIR, "results_ext.json")
    with open(out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"summary written: {out}")


if __name__ == "__main__":
    main()
