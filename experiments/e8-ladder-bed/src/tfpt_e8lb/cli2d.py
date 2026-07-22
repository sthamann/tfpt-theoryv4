"""CLI: PYTHONPATH=src python -m tfpt_e8lb.cli2d analyze2d

Amendment-v2 (2DCS) runs, deterministic (fixed seeds). Writes
results/results2d.json, results/assignments2d.csv, results/map2d_fit.png.

Runs (preregistered in hypotheses/e8_ladder_bed_v1.yaml, amendment_v2):
  KA2D_synthetic_e8       known-answer synthetic E8 2D map (m7/m8 via F3)
  NEG2D_localized_limit   analytic arXiv:2512.16829 prediction -> must reject
  C2D_control_battery     scramble2d / offset2d / jitter2d / wrong-ladder2d
  REAL2D_conb2o6_e8point  BLOCKED (no experimental 2DCS data exists yet)
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

from .controls import CHI2_DOF_MAX, P_VALIDATED, R_MAX
from .controls2d import (N_REQ_2D, jitter2d_battery, offset2d_battery,
                         scramble2d_battery, wrong_ladder2d_battery)
from .ladder import E8_LADDER, pf_selftest
from .recover2d import Recovery2D, build_catalog, mc_pvalue2d, recover2d
from .synth2d import ka2d_map, neg2d_map

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"


def rec_to_dict(rec: Recovery2D, peaks, labels) -> dict:
    if not rec.ok:
        return {"ok": False}
    cat = build_catalog(E8_LADDER)
    return {
        "ok": True,
        "n_rungs": rec.n_rungs,
        "rungs_covered": rec.rungs_covered,
        "missing_rungs": rec.missing_rungs,
        "n_matched": rec.n_matched,
        "chi2": round(rec.chi2, 4),
        "chi2_dof": round(rec.chi2_dof, 4),
        "scale_m1_hat": round(rec.scale, 6),
        "matches": {
            cat.label[j]: {
                "peak": [float(x) for x in peaks[i]],
                "predicted": [round(float(rec.scale * v), 4) for v in cat.xy[j]],
                "pull_sigma": [round(p, 2) for p in rec.pulls[i]],
                "label_reporting_only": labels[i],
            } for i, j in rec.assignment.items()
        },
        "unmatched_peaks": [
            {"peak": [float(x) for x in peaks[i]],
             "label_reporting_only": labels[i]}
            for i in rec.unmatched_peaks
        ],
    }


def make_plot(ka, ka_rec: Recovery2D, neg, neg_rec: Recovery2D, path: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    cat = build_catalog(E8_LADDER)
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6))
    for ax, data, rec, title in [
        (axes[0], ka, ka_rec,
         "KA2D synthetic E8 map (m$_1$=0.16 THz, window 0.6 THz)\n"
         "m$_7$/m$_8$ only via F3 difference coordinates"),
        (axes[1], neg, neg_rec,
         "NEG2D localized-limit map (arXiv:2512.16829, non-E8)\n"
         "preregistered negative control"),
    ]:
        peaks = np.abs(np.asarray(data["peaks"], dtype=float))
        if rec.ok:
            pred = rec.scale * cat.xy
            fam_style = {"F1": ("s", "0.75"), "F2": ("^", "0.75"),
                         "F3": ("v", "0.75")}
            for fam, (mk, col) in fam_style.items():
                m = [k for k, f in enumerate(cat.family) if f == fam]
                ax.scatter(pred[m, 0], pred[m, 1], marker=mk, s=18,
                           facecolors="none", edgecolors=col, linewidths=0.7,
                           label=f"catalog {fam} @ $\\hat m_1$", zorder=1)
        matched = set(rec.assignment) if rec.ok else set()
        for i, (x, y) in enumerate(peaks):
            if i in matched:
                ax.plot(x, y, "o", color="tab:blue", ms=7, zorder=3)
            else:
                ax.plot(x, y, "x", color="tab:red", ms=8, mew=2, zorder=3)
        if rec.ok:
            for i, j in rec.assignment.items():
                ax.plot([peaks[i, 0], pred[j, 0]], [peaks[i, 1], pred[j, 1]],
                        "-", color="tab:blue", lw=0.6, zorder=2)
            stat = (f"n_rungs = {rec.n_rungs}/8\nn_matched = {rec.n_matched}"
                    f"\n$\\chi^2$/dof = {rec.chi2_dof:.2f}")
        else:
            stat = "no valid recovery"
        ax.annotate(stat, xy=(0.03, 0.83), xycoords="axes fraction", fontsize=9)
        ax.set_xlabel(f"$\\omega_\\tau$ [{data['unit']}] (folded)")
        ax.set_ylabel(f"$\\omega_t$ [{data['unit']}] (folded)")
        ax.set_title(title, fontsize=9)
        h = [plt.Line2D([], [], marker="o", ls="", color="tab:blue",
                        label="peak (matched)"),
             plt.Line2D([], [], marker="x", ls="", color="tab:red",
                        label="peak (unmatched)")]
        ax.legend(handles=h + ax.get_legend_handles_labels()[0][:3],
                  loc="lower right", fontsize=7)
    fig.suptitle("2DCS blind E8 recovery bed, amendment v2 -- synthetic runs "
                 "(detector level; no experimental 2DCS data exists yet)",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=140, bbox_inches="tight")


def write_assignments_csv(runs, path: Path):
    cat = build_catalog(E8_LADDER)
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["run", "peak_omega_tau", "peak_omega_t", "sigma", "unit",
                    "label_reporting_only", "status", "catalog_entry",
                    "pred_omega_tau", "pred_omega_t",
                    "pull_tau_sigma", "pull_t_sigma"])
        for run_name, data, rec in runs:
            peaks = np.abs(np.asarray(data["peaks"], dtype=float))
            labels = data["labels_reporting_only"]
            for i, (x, y) in enumerate(peaks):
                if rec.ok and i in rec.assignment:
                    j = rec.assignment[i]
                    w.writerow([run_name, x, y, data["sigmas"][i],
                                data["unit"], labels[i], "matched",
                                cat.label[j],
                                round(float(rec.scale * cat.xy[j, 0]), 5),
                                round(float(rec.scale * cat.xy[j, 1]), 5),
                                round(rec.pulls[i][0], 2),
                                round(rec.pulls[i][1], 2)])
                else:
                    w.writerow([run_name, x, y, data["sigmas"][i],
                                data["unit"], labels[i], "unmatched",
                                "", "", "", "", ""])


def verdict2d(res: dict) -> str:
    """Preregistered amendment_v2 logic: prepared_awaiting_data or kill_2d."""
    ka = res["KA2D_synthetic_e8"]
    ka_ok = (ka["recovery"].get("n_rungs", 0) == 8
             and ka["recovery"].get("chi2_dof", 99) <= CHI2_DOF_MAX
             and ka["mc_null"]["p_value"] < P_VALIDATED)
    neg_rejected = not res["NEG2D_localized_limit"]["detected_at_validated_level"]
    ctl = res["C2D_control_battery"]
    ctl_ok = all([
        ctl["scramble2d"]["rejected"],
        ctl["offset2d"]["rejected"],
        ctl["jitter2d"]["_rejected_at_destructive_level"],
        ctl["wrong_ladder2d"]["_all_beaten_by_e8"],
    ])
    if ka_ok and neg_rejected and ctl_ok:
        return "prepared_awaiting_data"
    return "kill_2d"


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] != "analyze2d":
        print(__doc__)
        return 1
    t0 = time.time()
    res: dict = {
        "experiment": "e8-ladder-bed",
        "version": "v2_amendment_2dcs",
        "firewall": ("detector validation, synthetic/analytic maps only; "
                     "confirms nothing about TFPT; no experimental 2DCS data "
                     "on CoNb2O6 exists as of 2026-07-21 (arXiv:2512.16829 "
                     "is a theory paper)"),
        "pf_selftest": pf_selftest(),
    }
    assert res["pf_selftest"]["pass"], "PF self-test failed -- aborting"

    # --- KA2D: known-answer synthetic E8 2D map ------------------------------
    ka = ka2d_map()
    ka_rec = recover2d(ka["peaks"], ka["sigmas"], E8_LADDER)
    ka_mc = mc_pvalue2d(ka["peaks"], ka["sigmas"], ka_rec, R_MAX,
                        n_ladders=5000, seed=0)
    res["KA2D_synthetic_e8"] = {
        "provenance": ka["provenance"],
        "n_peaks_input": len(ka["peaks"]),
        "m1_true": ka["m1_true"], "window": ka["window"], "unit": ka["unit"],
        "recovery": rec_to_dict(ka_rec, np.abs(ka["peaks"]),
                                ka["labels_reporting_only"]),
        "mc_null": ka_mc,
        "m7_m8_via_F3": {
            "rung_7_covered": 7 in ka_rec.rungs_covered if ka_rec.ok else False,
            "rung_8_covered": 8 in ka_rec.rungs_covered if ka_rec.ok else False,
        },
    }

    # --- NEG2D: localized-limit analytic map (must be rejected) --------------
    neg = neg2d_map()
    neg_rec = recover2d(neg["peaks"], neg["sigmas"], E8_LADDER)
    neg_mc = mc_pvalue2d(neg["peaks"], neg["sigmas"], neg_rec, R_MAX,
                         n_ladders=1000, seed=0)
    neg_detected = bool(neg_rec.ok and neg_rec.n_rungs >= N_REQ_2D
                        and neg_rec.chi2_dof <= CHI2_DOF_MAX
                        and neg_mc["p_value"] < P_VALIDATED)
    res["NEG2D_localized_limit"] = {
        "provenance": neg["provenance"],
        "n_peaks_input": len(neg["peaks"]),
        "unit": neg["unit"],
        "eps_minus_mev": round(neg["eps_minus_mev"], 4),
        "eps_plus_mev": round(neg["eps_plus_mev"], 4),
        "q_states_mev": {k: round(v, 4) for k, v in neg["q_states_mev"].items()},
        "recovery": rec_to_dict(neg_rec, np.abs(neg["peaks"]),
                                neg["labels_reporting_only"]),
        "mc_null_1000": neg_mc,
        "detected_at_validated_level": neg_detected,
        "rejected": not neg_detected,
    }

    # --- C2D control battery on the KA map ----------------------------------
    res["C2D_control_battery"] = {
        "note": "detection = n_rungs>=6 & chi2/dof<=2 & MC p<0.01 (500 null)",
        "scramble2d": scramble2d_battery(np.abs(ka["peaks"]), ka["sigmas"],
                                         n_obs=ka_rec.n_rungs),
        "offset2d": offset2d_battery(np.abs(ka["peaks"]), ka["sigmas"],
                                     m1_hat=ka_rec.scale),
        "jitter2d": jitter2d_battery(np.abs(ka["peaks"]), ka["sigmas"]),
        "wrong_ladder2d": wrong_ladder2d_battery(np.abs(ka["peaks"]),
                                                 ka["sigmas"], ka_rec),
    }

    # --- REAL2D: blocked -----------------------------------------------------
    res["REAL2D_conb2o6_e8point"] = {
        "status": "blocked_no_experimental_data",
        "note": ("no published experimental 2DCS measurement of CoNb2O6 "
                 "exists (web-checked 2026-07-21); arXiv:2512.16829 is "
                 "theory-only (four-kink/ED model, B_y = 0-3 T localized "
                 "regime, not the E8 point B ~ 4.7-5.5 T). CoNb2O6 leg "
                 "stays 6/8 (p = 0.0038) per the m7_m8_upgrade_rule."),
    }

    res["verdict_v2"] = verdict2d(res)
    res["v1_verdict_untouched"] = "validated (results.json)"
    res["runtime_s"] = round(time.time() - t0, 1)

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results2d.json").write_text(json.dumps(res, indent=2) + "\n")
    write_assignments_csv(
        [("KA2D_synthetic_e8", ka, ka_rec),
         ("NEG2D_localized_limit", neg, neg_rec)],
        RESULTS / "assignments2d.csv")
    make_plot(ka, ka_rec, neg, neg_rec, RESULTS / "map2d_fit.png")

    print(json.dumps({k: res[k] for k in ("verdict_v2", "runtime_s")}, indent=2))
    print(f"KA2D : n_rungs={ka_rec.n_rungs}/8 n_matched={ka_rec.n_matched} "
          f"chi2/dof={ka_rec.chi2_dof:.2f} p={ka_mc['p_value']:.4g} "
          f"m1_hat={ka_rec.scale:.4f} {ka['unit']}")
    if neg_rec.ok:
        print(f"NEG2D: n_rungs={neg_rec.n_rungs}/8 n_matched={neg_rec.n_matched} "
              f"chi2/dof={neg_rec.chi2_dof:.2f} p={neg_mc['p_value']:.4g} "
              f"detected={neg_detected} (must be False)")
    else:
        print("NEG2D: no valid recovery (rejected)")
    print(f"wrote {RESULTS/'results2d.json'}, assignments2d.csv, map2d_fit.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
