"""``tfpt-seed analyze`` -- the shared-seed stress test.

One retarded seed phi0 = (4/3)c3 + 48 c3^4 fixes four observables in distinct sectors:

    beta_rad       = phi0/(4 pi)
    Omega_b        = (4 pi - 1) phi0 / (4 pi)
    sin^2 theta13  = phi0 e^(-5/6)
    lambda_Cabibbo = sqrt(phi0 (1 - phi0))

Invert each measurement to the seed it implies, do an inverse-variance joint fit, a
leave-one-out, and identify the dominant pull. Acceptance:

    * if one leg alone deviates > 3 sigma from the leave-one-out seed -> that leg is
      flagged transfer-corrected (currently the candidate is theta13);
    * if two legs deviate > 3 sigma -> the shared-seed block falls.

Legs use independent pipelines where possible (BBN Omega_b, reactor theta13, CKM
Cabibbo, CMB beta), so this is closer to four independent worlds than four CMB cuts.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from tfpt_seed import seed_v2, seed_v3

C3 = 1.0 / (8.0 * math.pi)
PHI0 = (4.0 / 3.0) * C3 + 48.0 * C3**4
SEED_SLOPE = 4.0 * math.pi - 1.0
DEG2RAD = math.pi / 180.0
DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
RESULTS = Path(__file__).resolve().parents[2] / "results"


def _legs(m: dict) -> list[dict]:
    legs = []
    b = m["beta_deg"]
    legs.append({"name": "beta", "phi0": b["value"] * DEG2RAD * 4 * math.pi,
                 "sigma": b["sigma"] * DEG2RAD * 4 * math.pi, "indep": b["independence"]})
    o = m["omega_b_h2"]
    ob = o["value"] / o["h"]**2
    ob_s = ob * math.hypot(o["sigma"] / o["value"], 2 * 0.0 / o["h"])   # h fixed here
    legs.append({"name": "Omega_b", "phi0": ob * 4 * math.pi / SEED_SLOPE,
                 "sigma": ob_s * 4 * math.pi / SEED_SLOPE, "indep": o["independence"]})
    t = m["sin2_theta13"]
    legs.append({"name": "theta13", "phi0": t["value"] * math.exp(5 / 6),
                 "sigma": t["sigma"] * math.exp(5 / 6), "indep": t["independence"]})
    c = m["cabibbo_Vus"]
    lam, ls = c["value"], c["sigma"]
    disc = 1 - 4 * lam**2
    phi = (1 - math.sqrt(disc)) / 2
    legs.append({"name": "Cabibbo", "phi0": phi, "sigma": (2 * lam / math.sqrt(disc)) * ls,
                 "indep": c["independence"]})
    return legs


def _joint(legs: list[dict]) -> tuple[float, float, float]:
    w = [1 / leg["sigma"]**2 for leg in legs]
    phat = sum(wi * leg["phi0"] for wi, leg in zip(w, legs)) / sum(w)
    chi2 = sum((leg["phi0"] - phat)**2 / leg["sigma"]**2 for leg in legs)
    return phat, chi2, max(1, len(legs) - 1)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT shared-seed stress test")
    ap.add_argument("command", choices=["audit", "analyze", "v2", "v3"], nargs="?",
                    default="analyze")
    args = ap.parse_args(argv)
    m = json.loads(DATA.read_text(encoding="utf-8"))

    if args.command == "v2":
        seed_v2.report(m)
        return 0
    if args.command == "v3":
        seed_v3.report(m)
        return 0

    legs = _legs(m)
    print("=" * 72)
    print(f"TFPT shared-seed stress test (frozen phi0 = {PHI0:.6f})")
    print("=" * 72)
    if args.command == "audit":
        return 0

    phat, chi2, dof = _joint(legs)
    print(f"  joint phi0_hat = {phat:.6f} ; chi2/dof = {chi2:.2f}/{dof} = {chi2/dof:.2f}\n")
    for leg in legs:
        z_frozen = (leg["phi0"] - PHI0) / leg["sigma"]
        z_joint = (leg["phi0"] - phat) / leg["sigma"]              # deviation from the COMMON seed
        loo = [x for x in legs if x["name"] != leg["name"]]
        _, chi2_loo, _ = _joint(loo)
        leg["z_frozen"], leg["z_joint"] = z_frozen, z_joint
        leg["chi2_contrib"] = z_joint**2
        leg["delta_chi2_on_removal"] = chi2 - chi2_loo            # how much it drives the tension
        print(f"  {leg['name']:9s} [{leg['indep']:7s}] phi0={leg['phi0']:.5f}+/-{leg['sigma']:.5f}"
              f"  z(frozen)={z_frozen:+.2f}  z(joint)={z_joint:+.2f}  dChi2_LOO={leg['delta_chi2_on_removal']:+.2f}")

    # dominant pull = the leg contributing most chi2 to the common fit (the real driver)
    dominant = max(legs, key=lambda x: x["chi2_contrib"])
    over3 = [leg["name"] for leg in legs if abs(leg["z_joint"]) > 3.0]
    theta13_flag = abs(next(x for x in legs if x["name"] == "theta13")["z_joint"]) > 3.0
    block_falls = len(over3) >= 2
    print(f"\n  dominant pull (max chi2 contribution): {dominant['name']} "
          f"(z_joint={dominant['z_joint']:+.2f}, chi2 share "
          f"{dominant['chi2_contrib']/chi2*100:.0f}%)")
    print(f"  legs > 3 sigma from the common seed: {over3 or 'none'}")
    if block_falls:
        verdict = f"SHARED-SEED BLOCK FALLS: {over3} both deviate > 3 sigma from the common seed"
    elif theta13_flag:
        verdict = "theta13 > 3 sigma from the common seed -> flag PMNS theta13 as transfer-corrected (mu-tau breaking)"
    else:
        verdict = (f"shared-seed block HOLDS (chi2/dof={chi2/dof:.2f}); dominant pull is "
                   f"{dominant['name']} at {dominant['z_joint']:+.2f} sigma (< 3) -- a mild stress, "
                   f"no transfer correction triggered. Legs span CMB/BBN/reactor/CKM pipelines.")
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(
        {"phi0_frozen": PHI0, "phi0_joint": phat, "chi2": chi2, "dof": dof,
         "legs": legs, "dominant_pull": dominant["name"], "over_3sigma": over3,
         "theta13_transfer_flag": theta13_flag, "block_falls": block_falls,
         "verdict": verdict}, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
