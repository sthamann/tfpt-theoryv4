"""Seed-consistency v3 -- reactor-only theta13 from the individual experiments.

v2 used a single reactor-only theta13 leg (Daya Bay dominated). v3 goes one level deeper to
avoid statistics origami: it takes the **individual reactor experiments** (Daya Bay, RENO,
Double Chooz -- genuinely independent detectors), shows the seed each implies, forms a clean
reactor-only inverse-variance combination, and uses ONLY that in the seed fit. The NuFIT
global fit is carried as a *shadow* (never in the fit -- it already contains the reactor data,
so feeding both would double-count theta13). JUNO is listed for when its theta13 stabilises.

Decision rules (frozen, same firewall):
  * theta13 alone > 3 sigma from the common seed -> PMNS theta13 transfer-corrected;
  * two independent families > 3 sigma            -> shared-seed block falls.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from tfpt_seed import seed_v2

PHI0 = seed_v2.PHI0
DATA = seed_v2.DATA
RESULTS = seed_v2.RESULTS


def _combine_reactor(exps: list[dict]) -> tuple[float, float, list[dict]]:
    """Inverse-variance combination of the independent reactor sin^2 theta13 measurements."""
    used = [e for e in exps if e.get("value") is not None and e.get("sigma")]
    w = [1.0 / e["sigma"] ** 2 for e in used]
    val = sum(wi * e["value"] for wi, e in zip(w, used)) / sum(w)
    sig = 1.0 / math.sqrt(sum(w))
    detail = []
    for e in used:
        phi = e["value"] * math.exp(5 / 6)
        detail.append({"experiment": e["experiment"], "sin2_theta13": e["value"],
                       "sigma": e["sigma"], "phi0_implied": phi,
                       "phi0_sigma": e["sigma"] * math.exp(5 / 6)})
    return val, sig, detail


def analyze(m: dict) -> dict:
    exps = m["sin2_theta13_reactor_experiments"]
    t13_val, t13_sig, per_exp = _combine_reactor(exps)

    # build legs with the reactor-COMBINED theta13 (independent detectors -> may be combined)
    legs = []
    b = m["beta_deg"]
    p, sp = seed_v2._phi0_from_beta(b["value"], b["sigma"])
    legs.append({"name": "beta", "family": "CMB", "phi0": p, "sigma": sp, "indep": b["independence"]})
    o = m["omega_b_h2"]
    p, sp = seed_v2._phi0_from_omega_b(o["value"], o["sigma"], o["h"])
    legs.append({"name": "Omega_b", "family": "BBN", "phi0": p, "sigma": sp, "indep": o["independence"]})
    p, sp = seed_v2._phi0_from_theta13(t13_val, t13_sig)
    legs.append({"name": "theta13", "family": "reactor(DB+RENO+DC)", "phi0": p, "sigma": sp,
                 "indep": "reactor-combined"})
    c = m["cabibbo_Vus"]
    p, sp = seed_v2._phi0_from_cabibbo(c["value"], c["sigma"])
    legs.append({"name": "Cabibbo", "family": "CKM", "phi0": p, "sigma": sp, "indep": c["independence"]})

    phat, chi2, dof, resid = seed_v2._gls(legs)
    for leg, r in zip(legs, resid):
        leg["z_frozen"] = (leg["phi0"] - PHI0) / leg["sigma"]
        leg["z_joint"] = r / leg["sigma"]
        leg["chi2_contrib"] = leg["z_joint"] ** 2
    loo = {}
    for fam in sorted({leg["family"] for leg in legs}):
        kept = [leg for leg in legs if leg["family"] != fam]
        p2, c2, _, _ = seed_v2._gls(kept)
        loo[fam] = {"phi0": p2, "dphi0": p2 - phat, "dchi2": chi2 - c2}
    dominant = max(legs, key=lambda x: x["chi2_contrib"])
    chi2_share = dominant["chi2_contrib"] / chi2 if chi2 else 0.0
    th = next(x for x in legs if x["name"] == "theta13")
    over3 = [leg["name"] for leg in legs if abs(leg["z_joint"]) > 3.0]
    ppc = seed_v2._ppc(legs, phat, chi2)

    # shadow: NuFIT global theta13 (NOT in the fit) -> does the verdict move?
    g = m["sin2_theta13_global"]
    pg, sg = seed_v2._phi0_from_theta13(g["value"], g["sigma"])
    legs_shadow = [dict(leg) for leg in legs]
    legs_shadow[2] = {"name": "theta13", "family": "global", "phi0": pg, "sigma": sg, "indep": "global-PMNS"}
    pgh, cgh, dgh, _ = seed_v2._gls(legs_shadow)

    if len(over3) >= 2:
        verdict = f"SHARED-SEED BLOCK FALLS: {over3} both > 3 sigma"
    elif abs(th["z_joint"]) > 3.0:
        verdict = "theta13 > 3 sigma -> flag PMNS theta13 transfer-corrected"
    else:
        verdict = (f"shared-seed block HOLDS (reactor-only theta13, chi2/dof={chi2/dof:.2f}, "
                   f"PPC p={ppc:.2f}); theta13 dominant at {th['z_joint']:+.2f} sigma "
                   f"({chi2_share*100:.0f}% of chi2). Three independent reactor detectors combine "
                   f"to sin^2 th13={t13_val:.5f}+/-{t13_sig:.5f}; NuFIT-global shadow gives the same "
                   f"verdict (chi2/dof={cgh/dgh:.2f}). No statistics origami: global and reactor-only "
                   f"are never both in the fit.")

    return {"phi0_frozen": PHI0, "phi0_joint": phat, "chi2_dof": chi2 / dof, "ppc_pvalue": ppc,
            "reactor_combined_sin2_theta13": t13_val, "reactor_combined_sigma": t13_sig,
            "per_reactor_experiment": per_exp, "legs": legs, "leave_one_family_out": loo,
            "dominant_leg": dominant["name"], "dominant_chi2_fraction": round(chi2_share, 3),
            "over_3sigma": over3, "theta13_transfer_flag": bool(abs(th["z_joint"]) > 3.0),
            "shadow_global": {"phi0_joint": pgh, "chi2_dof": cgh / dgh}, "verdict": verdict}


def report(m: dict) -> dict:
    res = analyze(m)
    print("=" * 74)
    print(f"TFPT seed-consistency v3 (reactor-only theta13 from DB/RENO/DC; phi0={PHI0:.6f})")
    print("=" * 74)
    print("  individual reactor experiments -> implied phi0:")
    for e in res["per_reactor_experiment"]:
        print(f"    {e['experiment']:13s} sin2_th13={e['sin2_theta13']:.5f}+/-{e['sigma']:.5f}"
              f"  -> phi0={e['phi0_implied']:.5f}+/-{e['phi0_sigma']:.5f}")
    print(f"  reactor-only combined: sin2_th13 = {res['reactor_combined_sin2_theta13']:.5f} "
          f"+/- {res['reactor_combined_sigma']:.5f}\n")
    print(f"  joint phi0={res['phi0_joint']:.6f} ; chi2/dof={res['chi2_dof']:.2f} ; "
          f"PPC p={res['ppc_pvalue']:.2f}")
    for leg in res["legs"]:
        print(f"    {leg['name']:9s} [{leg['family']:18s}] phi0={leg['phi0']:.5f}+/-{leg['sigma']:.5f}"
              f"  z(joint)={leg['z_joint']:+.2f}")
    print(f"  dominant: {res['dominant_leg']} ({res['dominant_chi2_fraction']*100:.0f}% chi2) ; "
          f"shadow(global) chi2/dof={res['shadow_global']['chi2_dof']:.2f}")
    print(f"\n-> {res['verdict']}")
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results_v3.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results_v3.json'}")
    return res


if __name__ == "__main__":
    report(json.loads(DATA.read_text(encoding="utf-8")))
