"""CLI: PYTHONPATH=src python -m tfpt_e8lb.cli analyze

Deterministic (fixed seeds). Writes results/results.json, results/assignments.csv
and results/ladder_fit.png.
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

from .controls import (CHI2_DOF_MAX, P_VALIDATED, R_MAX, airy_bed_control,
                       jitter_battery, offset_battery, scramble_battery,
                       wrong_ladder_battery)
from .ladder import E8_LADDER, pf_selftest
from .recover import NULL_LADDERS, Recovery, mc_pvalue, recover

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"

N_REQ = {"baco2v2o8": 6, "conb2o6": 5}   # preregistered validated-level rung counts


def load_csv(path: Path):
    peaks, sigmas, kinds = [], [], []
    with open(path) as fh:
        for row in csv.DictReader(r for r in fh if not r.startswith("#")):
            key = "energy_mev" if "energy_mev" in row else "freq_thz"
            peaks.append(float(row[key]))
            sigmas.append(float(row["sigma_mev" if "sigma_mev" in row else "sigma_thz"]))
            kinds.append(row["kind"])
    order = np.argsort(peaks)
    return (np.asarray(peaks)[order], np.asarray(sigmas)[order],
            [kinds[i] for i in order])


def rec_to_dict(rec: Recovery, peaks, kinds) -> dict:
    if not rec.ok:
        return {"ok": False}
    return {
        "ok": True,
        "n_assigned": rec.n_assigned,
        "chi2": round(rec.chi2, 4),
        "chi2_dof": round(rec.chi2_dof, 4),
        "scale_m1_hat": round(rec.scale, 5),
        "missing_rungs": [k + 1 for k in rec.missing_rungs],
        "assignment": {
            f"rung_{k+1}": {
                "peak": float(peaks[i]),
                "predicted": round(rec.scale * E8_LADDER[k], 4),
                "pull_sigma": round(rec.pulls[i], 2),
                "kind_reporting_only": kinds[i],
            } for i, k in rec.assignment.items()
        },
        "unassigned_peaks": [
            {"peak": float(peaks[i]), "kind_reporting_only": kinds[i]}
            for i in rec.unassigned_peaks
        ],
    }


def analyze_material(name: str, csv_path: Path) -> tuple[dict, Recovery, tuple]:
    peaks, sigmas, kinds = load_csv(csv_path)
    rec = recover(peaks, sigmas, E8_LADDER)
    mc = mc_pvalue(peaks, sigmas, rec, R_MAX, n_ladders=NULL_LADDERS, seed=0)
    out = {
        "data_file": csv_path.name,
        "n_peaks_input": len(peaks),
        "recovery": rec_to_dict(rec, peaks, kinds),
        "mc_null": mc,
    }
    return out, rec, (peaks, sigmas, kinds)


def controls_for(name: str, peaks, sigmas, rec: Recovery) -> dict:
    n_req = N_REQ[name]
    return {
        "scramble": scramble_battery(peaks, sigmas, n_req, rec.n_assigned),
        "offset": offset_battery(peaks, sigmas, n_req),
        "jitter": jitter_battery(peaks, sigmas, n_req),
        "wrong_ladder": wrong_ladder_battery(peaks, sigmas, rec),
    }


def make_plot(bcvo, conb, path: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, (title, (peaks, sigmas, kinds), rec, unit) in zip(axes, [
        ("BaCo$_2$V$_2$O$_8$  INS 4.7 T (Zou+ PRL 127, 077201)", bcvo[2], bcvo[1], "meV"),
        ("CoNb$_2$O$_6$  THz 4.75 T (Amelin+ PRB 102, 104431)", conb[2], conb[1], "THz"),
    ]):
        for k, r in enumerate(E8_LADDER):
            ax.axhline(r, color="0.85", lw=0.8, zorder=0)
            ax.text(1.02, r, f"$m_{k+1}$", transform=ax.get_yaxis_transform(),
                    fontsize=8, va="center", color="0.4")
        assigned = set(rec.assignment)
        lim = [0.8, max(5.2, (peaks.max() / rec.scale) * 1.08)]
        for i, p in enumerate(peaks):
            ratio = p / rec.scale
            err = sigmas[i] / rec.scale
            if i in assigned:
                ax.errorbar([E8_LADDER[rec.assignment[i]]], [ratio], yerr=[err],
                            fmt="o", color="tab:blue", ms=6, capsize=3, zorder=3)
            else:
                # unassigned peaks: y-rug at the left edge (no x position implied)
                ax.errorbar([lim[0] + 0.06], [ratio], yerr=[err], fmt="x",
                            color="tab:red", ms=7, capsize=2, zorder=3)
        ax.plot(lim, lim, "k--", lw=0.8, zorder=1)
        ax.set_xlim(lim); ax.set_ylim(lim)
        ax.set_xlabel("exact E8 rung  $m_i/m_1$   (unassigned: left-edge rug)")
        ax.set_ylabel(f"measured peak / $\\hat m_1$  [{unit} scale "
                      f"$\\hat m_1$={rec.scale:.3f}]")
        ax.set_title(title, fontsize=10)
        ax.annotate(f"n = {rec.n_assigned}/8 rungs\n$\\chi^2$/dof = {rec.chi2_dof:.2f}",
                    xy=(0.03, 0.86), xycoords="axes fraction", fontsize=10)
        handles = [plt.Line2D([], [], marker="o", ls="", color="tab:blue",
                              label="assigned rung"),
                   plt.Line2D([], [], marker="x", ls="", color="tab:red",
                              label="unassigned peak (rug)"),
                   plt.Line2D([], [], ls="--", color="k", label="exact ladder")]
        ax.legend(handles=handles, loc="lower right", fontsize=8)
    fig.suptitle("Blind E8 ladder recovery (detector validation; confirms "
                 "Zamolodchikov E8, not TFPT)", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=140, bbox_inches="tight")


def write_assignments_csv(rows, path: Path):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["material", "peak", "sigma", "unit", "kind_reporting_only",
                    "status", "rung", "exact_ratio", "predicted", "pull_sigma"])
        w.writerows(rows)


def verdict(res: dict) -> str:
    b = res["baco2v2o8"]; c = res["conb2o6"]
    b_ok = (b["recovery"].get("n_assigned", 0) >= N_REQ["baco2v2o8"]
            and b["recovery"].get("chi2_dof", 99) <= CHI2_DOF_MAX
            and b["mc_null"]["p_value"] < P_VALIDATED)
    c_ok = (c["recovery"].get("n_assigned", 0) >= N_REQ["conb2o6"]
            and c["recovery"].get("chi2_dof", 99) <= CHI2_DOF_MAX
            and c["mc_null"]["p_value"] < P_VALIDATED)
    ctl = res["controls"]
    ctl_ok = all([
        ctl["baco2v2o8"]["scramble"]["rejected"],
        ctl["baco2v2o8"]["offset"]["rejected"],
        ctl["baco2v2o8"]["jitter"]["_rejected_at_destructive_level"],
        ctl["baco2v2o8"]["wrong_ladder"]["_all_beaten_by_e8"],
        ctl["conb2o6"]["scramble"]["rejected"],
        ctl["conb2o6"]["offset"]["rejected"],
        ctl["conb2o6"]["jitter"]["_rejected_at_destructive_level"],
        ctl["conb2o6"]["wrong_ladder"]["_all_beaten_by_e8"],
        ctl["airy_bed"]["rejected"],
    ])
    if b_ok and c_ok and ctl_ok:
        return "validated"
    if (b_ok or c_ok) and ctl_ok:
        return "partially_validated"
    return "failed"


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] != "analyze":
        print(__doc__)
        return 1
    t0 = time.time()
    res: dict = {
        "experiment": "e8-ladder-bed",
        "version": "v1",
        "firewall": ("detector validation on published spectra; confirms "
                     "Zamolodchikov E8, not TFPT axioms; nothing load-bearing"),
        "pf_selftest": pf_selftest(),
        "e8_ladder_exact": [float(x) for x in E8_LADDER],
    }
    assert res["pf_selftest"]["pass"], "PF self-test failed -- aborting"

    bcvo_out, bcvo_rec, bcvo_data = analyze_material(
        "baco2v2o8", ROOT / "data" / "baco2v2o8_ins_peaks.csv")
    conb_out, conb_rec, conb_data = analyze_material(
        "conb2o6", ROOT / "data" / "conb2o6_thz_peaks.csv")
    res["baco2v2o8"] = bcvo_out
    res["conb2o6"] = conb_out

    # sigma sensitivity variant for BCVO (0.05 meV singles), reported not primary
    p, s, k = bcvo_data
    s_var = np.where(np.array(k) == "single_marker", 0.05, 0.08)
    rec_var = recover(p, s_var, E8_LADDER)
    mc_var = mc_pvalue(p, s_var, rec_var, R_MAX, n_ladders=NULL_LADDERS, seed=0)
    res["baco2v2o8"]["sigma_variant_0p05"] = {
        "recovery": rec_to_dict(rec_var, p, k), "mc_null": mc_var}

    # A2 secondary run: singles-only (paper's 8 single-particle markers), no
    # continuum contamination -> clean detector significance
    mask = np.array(k) == "single_marker"
    p1, s1 = p[mask], s[mask]
    k1 = [kk for kk, m in zip(k, mask) if m]
    rec_s = recover(p1, s1, E8_LADDER)
    mc_s = mc_pvalue(p1, s1, rec_s, R_MAX, n_ladders=NULL_LADDERS, seed=0)
    res["baco2v2o8"]["singles_only_run_A2"] = {
        "recovery": rec_to_dict(rec_s, p1, k1), "mc_null": mc_s}

    res["controls"] = {
        "baco2v2o6_note": "detection = n>=n_req & chi2/dof<=2 & MC p<0.01",
        "baco2v2o8": controls_for("baco2v2o8", *bcvo_data[:2], bcvo_rec),
        "conb2o6": controls_for("conb2o6", *conb_data[:2], conb_rec),
        "airy_bed": airy_bed_control(N_REQ["baco2v2o8"]),
    }
    res["verdict"] = verdict(res)
    res["runtime_s"] = round(time.time() - t0, 1)

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(res, indent=2) + "\n")

    rows = []
    for mat, (peaks, sigmas, kinds), rec, unit in [
            ("BaCo2V2O8", bcvo_data, bcvo_rec, "meV"),
            ("CoNb2O6", conb_data, conb_rec, "THz")]:
        for i, pk in enumerate(peaks):
            if i in rec.assignment:
                kk = rec.assignment[i]
                rows.append([mat, pk, sigmas[i], unit, kinds[i], "assigned",
                             kk + 1, round(float(E8_LADDER[kk]), 6),
                             round(rec.scale * E8_LADDER[kk], 4),
                             round(rec.pulls[i], 2)])
            else:
                rows.append([mat, pk, sigmas[i], unit, kinds[i], "unassigned",
                             "", "", "", ""])
    write_assignments_csv(rows, RESULTS / "assignments.csv")
    make_plot((bcvo_out, bcvo_rec, bcvo_data), (conb_out, conb_rec, conb_data),
              RESULTS / "ladder_fit.png")

    print(json.dumps({k: res[k] for k in
                      ("pf_selftest", "verdict", "runtime_s")}, indent=2))
    print(f"BCVO : n={bcvo_rec.n_assigned}/8 chi2/dof={bcvo_rec.chi2_dof:.2f} "
          f"p={res['baco2v2o8']['mc_null']['p_value']:.4g}")
    print(f"CoNb : n={conb_rec.n_assigned}/8 chi2/dof={conb_rec.chi2_dof:.2f} "
          f"p={res['conb2o6']['mc_null']['p_value']:.4g}")
    print(f"wrote {RESULTS/'results.json'}, assignments.csv, ladder_fit.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
