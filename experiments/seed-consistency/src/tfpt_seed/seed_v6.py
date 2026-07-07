"""Seed-consistency v6 -- RETARDED-TAIL ABLATION (tree seed vs retarded seed).

The seed is not one number but a sum of a tree part and the specific topological tail:

    u_tree = (4/3) c3           = 1/(6 pi)              = 0.05305165
    u_ret  = u_tree + 48 c3^4   = 1/(6 pi) + 3/(256 pi^4) = 0.05317246
    tail   = 3/(256 pi^4)       = 1.208e-4   (+0.23% of the seed)

v6 asks the ablation question the architecture reading must eventually win: do the data
prefer the RETARDED seed (with the tail) over the TREE seed (without it)?  Today the
tail shifts every channel by well under 1 sigma, so the honest output is (1) the current
Delta chi^2 preference, (2) the per-channel shift in units of today's sigma, and (3) the
DATED precision targets at which each channel decides the tail at 3 sigma -- the
prequential version of the test (future data score against both seeds, no refitting).

Channel shifts induced by the tail (exact link functions, v2 conventions):
    beta:        tail/(4 pi)                  = 5.51e-4 deg
    Omega_b h2:  tail * (4pi-1)/(4pi) * h^2   = 5.05e-5
    sin^2 th13:  tail * e^(-5/6)              = 5.25e-5
    |V_us|:      tail * (1-2u)/(2 lambda_C)   = 2.41e-4

Firewall: consistency architecture, never proof; a future preference for the TREE seed
at >=3 sigma in >=2 channels would be a genuine crack in the retarded reading (the
tail IS the topological correction), typed as such in advance.
"""

from __future__ import annotations

import json
import math

from tfpt_seed import seed_v2

C3 = 1.0 / (8.0 * math.pi)
U_TREE = (4.0 / 3.0) * C3                 # = 1/(6 pi)
TAIL = 48.0 * C3 ** 4                     # = 3/(256 pi^4)
U_RET = U_TREE + TAIL                     # = seed_v2.PHI0
DATA = seed_v2.DATA
RESULTS = seed_v2.RESULTS


def _chi2_at(u: float, legs: list[dict]) -> float:
    return sum((leg["phi0"] - u) ** 2 / leg["sigma"] ** 2 for leg in legs)


def analyze(m: dict) -> dict:
    legs = seed_v2._legs(m, "sin2_theta13_reactor")
    chi2_tree = _chi2_at(U_TREE, legs)
    chi2_ret = _chi2_at(U_RET, legs)
    dchi2 = chi2_tree - chi2_ret           # > 0 => data prefer the retarded seed

    per = {}
    for leg in legs:
        # today's discrimination power of this channel alone (in sigma of the leg)
        z_shift = TAIL / leg["sigma"]
        # dated 3-sigma decision target on the SEED scale
        per[leg["name"]] = {
            "phi0_implied": round(leg["phi0"], 6), "sigma_phi0": round(leg["sigma"], 6),
            "pull_tree": round((leg["phi0"] - U_TREE) / leg["sigma"], 2),
            "pull_ret": round((leg["phi0"] - U_RET) / leg["sigma"], 2),
            "tail_shift_sigma_today": round(z_shift, 3),
            "sigma_phi0_needed_3sigma": TAIL / 3.0,
        }

    # observable-space decision targets (what an experiment must reach)
    o = m["omega_b_h2"]
    lam_c = m["cabibbo_Vus"]["value"]
    targets = {
        "beta_deg": {"tail_shift": TAIL / (4 * math.pi) / seed_v2.DEG2RAD,
                     "sigma_today": m["beta_deg"]["sigma"],
                     "decider": "LiteBIRD/SO sigma~0.02 deg CANNOT decide the tail "
                                "(needs 1.8e-4 deg) -- beta tests the SEED, not the tail"},
        "Vus": {"tail_shift": TAIL * (1 - 2 * U_RET) / (2 * lam_c),
                "sigma_today": m["cabibbo_Vus"]["sigma"],
                "decider": "sharpest channel: needs sigma(V_us) ~ 8.0e-5 (~10x better "
                           "than PDG today) -- kaon/lattice programme scale"},
        "sin2_theta13": {"tail_shift": TAIL * math.exp(-5.0 / 6.0),
                         "sigma_today": m["sin2_theta13_reactor"]["sigma"],
                         "decider": "needs sigma ~ 1.75e-5 (~37x better than Daya Bay)"},
        "omega_b_h2": {"tail_shift": TAIL * seed_v2.SEED_SLOPE / (4 * math.pi) * o["h"] ** 2,
                       "sigma_today": o["sigma"],
                       "decider": "needs sigma ~ 1.7e-5 (~33x better than BBN D/H today)"},
    }
    for t in targets.values():
        t["tail_shift"] = float(f"{t['tail_shift']:.4g}")
        t["shift_over_sigma_today"] = round(t["tail_shift"] / t["sigma_today"], 3)

    pref = "RETARDED" if dchi2 > 0 else "TREE"
    verdict = (
        f"TAIL ABLATION (today): the four channels mildly prefer the {pref} seed "
        f"(chi2 tree {chi2_tree:.2f} vs retarded {chi2_ret:.2f}, dof 4 each; "
        f"|Delta chi^2| = {abs(dchi2):.2f} -- entirely insignificant"
        + (", driven by the known theta13 crack candidate pulling low" if pref == "TREE"
           else "")
        + f"). HONEST STATE: the data cannot yet see the tail (3/(256 pi^4) = +0.23%) "
        f"-- it shifts every channel by < 0.3 sigma today (best: Cabibbo "
        f"{per['Cabibbo']['tail_shift_sigma_today']:.2f} sigma). Prequential targets "
        f"are now DATED: the tail becomes a 3-sigma question only at sigma(V_us) ~ "
        f"8e-5 (kaon/lattice programme), sigma(sin2th13) ~ 1.8e-5, or sigma(omega_b "
        f"h2) ~ 1.7e-5; LiteBIRD's beta band tests the SEED, never the tail. Frozen "
        f"crack condition: >= 2 channels preferring the TREE seed at >= 3 sigma kills "
        f"the retarded reading.")
    return {"u_tree": U_TREE, "u_retarded": U_RET, "tail": TAIL,
            "chi2_tree_dof4": round(chi2_tree, 3), "chi2_retarded_dof4": round(chi2_ret, 3),
            "delta_chi2_pref_retarded": round(dchi2, 3),
            "per_channel": per, "observable_targets": targets, "verdict": verdict}


def report(m: dict) -> dict:
    res = analyze(m)
    print("=" * 78)
    print("TFPT seed-consistency v6 -- retarded-tail ablation "
          f"(u_tree = {U_TREE:.6f}, u_ret = {U_RET:.6f}, tail = {TAIL:.3e})")
    print("=" * 78)
    print(f"  chi2(tree) = {res['chi2_tree_dof4']:.2f}   chi2(retarded) = "
          f"{res['chi2_retarded_dof4']:.2f}   Delta chi2 = "
          f"{res['delta_chi2_pref_retarded']:+.2f} (pro retarded)\n")
    for name, d in res["per_channel"].items():
        print(f"  {name:9s} pull(tree) {d['pull_tree']:+.2f} | pull(ret) "
              f"{d['pull_ret']:+.2f} | tail = {d['tail_shift_sigma_today']:.3f} sigma today")
    print("\n  observable-space decision targets (3 sigma on the tail):")
    for name, t in res["observable_targets"].items():
        print(f"    {name:13s} tail shift {t['tail_shift']:.3g} "
              f"({t['shift_over_sigma_today']:.3f} sigma today) -- {t['decider']}")
    print(f"\n-> {res['verdict']}")
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results_v6.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results_v6.json'}")
    return res


if __name__ == "__main__":
    report(json.loads(DATA.read_text(encoding="utf-8")))
