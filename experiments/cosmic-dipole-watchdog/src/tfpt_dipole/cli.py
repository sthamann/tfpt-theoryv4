"""``tfpt-dipole analyze`` -- the cosmic number-count dipole (Ellis-Baldwin) watchdog.

THE OPEN QUESTION.  The dipole in the number counts of distant quasars/radio
sources (CatWISE2020, NVSS, MALS) is ~2x LARGER than the kinematic expectation
from the CMB dipole, aligned with it in direction.  Published significances
span 4.4-5.7 sigma (Secrest+2021/22, Dam+2023, Wagenveld+2025; the 2025 RMP
colloquium claims ">5 sigma"), while clustering/mask-aware reassessments
reduce it to 3.3-3.6 sigma (arXiv:2511.00822 S1-S3).  No model explains it:
if real, the matter and radiation rest frames disagree -- a direct strike at
FLRW and the cosmological principle.

THE TFPT READING.  TFPT's cosmology branch is built ON FLRW: the flat budget
closure (h = 0.6715, parameter-free), the Lambda/H0 engine, Omega_b via the
Macquart relation, the CMB seed line -- all assume an isotropic FLRW
background.  The mu4 clock / PSL(2,C) boundary orientation allows at most a
TINY global orientation remnant (the same expectation as the cosmic-handedness
watchdog).  TFPT has NO mechanism for a super-Hubble intrinsic matter dipole.

  =>  like steriles (N_fam=3), evolving DE (w=-1), Cabibbo, X17 and R_D(*),
      this is a DISSOLUTION prediction: the excess must resolve into
      selection/mask/clustering systematics.  A confirmed intrinsic dipole
      would strike the FLRW foundation of the TFPT cosmology branch (NOT the
      compiler core -- alpha, masses, mixings are local physics).

Deterministic: published values only (data/measurements.json), no fetching.
Verdict enums: consistent | tension | data_limited.

Firewall: standalone frontier watchdog; search surface, NOT a load-bearing
claim.  Nothing here upgrades any TFPT status.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
RESULTS = Path(__file__).resolve().parents[2] / "results"

KILL_SIGMA = 5.0


def analyze(m: dict) -> dict:
    kin = m["cmb_kinematic"]
    legs = [{"name": leg["name"], "significance_sigma": leg["significance_sigma"],
             "excess_over_kinematic": leg.get("excess_over_kinematic"),
             "reference": leg["reference"]} for leg in m["legs"]]
    reassessments = [{"name": r["name"], "significance_sigma": r["significance_sigma"],
                      "reference": r["reference"]} for r in m["reassessments"]]

    claimed = [leg["significance_sigma"] for leg in legs if leg["significance_sigma"]]
    reduced = [r["significance_sigma"] for r in reassessments if r["significance_sigma"]]
    spread_lo = min(reduced) if reduced else min(claimed)
    spread_hi = max(claimed)

    catwise = m["legs"][0]
    excess = catwise["D_obs"] / kin["catwise_kinematic_expectation_D"]

    # the honest state: the anomaly is real as a measurement (the dipole IS
    # ~2x kinematic in every catalog) but its SIGNIFICANCE as a violation of
    # FLRW is contested at the level of the clustering/mask error budget.
    verdict = "data_limited"
    return {
        "tfpt_expectation": {
            "statement": ("FLRW isotropy + at most a tiny mu4/PSL(2,C) orientation remnant; "
                          "no mechanism for an intrinsic super-Hubble matter dipole => the "
                          "number-count dipole excess MUST dissolve into clustering/mask/"
                          "selection systematics (dissolution watchdog, same family as "
                          "fixed-point-watchdog axes D-G)"),
            "allowed_intrinsic_dipole": "~0 (kinematic dipole only)"},
        "observed": {
            "catwise_D_obs": catwise["D_obs"],
            "kinematic_expectation_D": kin["catwise_kinematic_expectation_D"],
            "excess_factor": round(excess, 2),
            "direction": f"aligned with CMB dipole within ~{catwise['direction_offset_deg_from_cmb']} deg"},
        "claimed_legs": legs,
        "clustering_mask_reassessments": reassessments,
        "significance_spread_sigma": [spread_lo, spread_hi],
        "today": ("every catalog sees D ~ 2x kinematic aligned with the CMB dipole; claimed "
                  "significances 4.4-5.7 sigma (RMP 2025: '>5 sigma'), clustering/mask-aware "
                  "reassessments 3.3-3.6 sigma. The error budget -- not the excess -- is the "
                  "open question. TFPT requires the FLRW-violating reading to dissolve."),
        "deciders": m["deciders"],
        "kill_rule": ("a clustering-marginalized, mask-controlled NON-kinematic dipole at "
                      ">= 5 sigma, replicated in >= 2 independent selections (e.g. LSST/"
                      "Euclid + SKA-MALS), surviving the aligned-clustering scenario "
                      "=> strikes the FLRW foundation of the TFPT cosmology branch "
                      "(flat budget, Lambda/H0 engine) -- not the compiler core"),
        "kill_triggered": False,
        "verdict": verdict,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT cosmic number-count dipole watchdog")
    ap.add_argument("command", choices=["analyze"], nargs="?", default="analyze")
    ap.parse_args(argv)
    m = json.loads(DATA.read_text(encoding="utf-8"))

    print("=" * 78)
    print("TFPT cosmic-dipole watchdog -- Ellis-Baldwin number-count dipole vs FLRW "
          f"(retrieved {m['retrieved']})")
    print("=" * 78)

    res = analyze(m)
    obs = res["observed"]
    print(f"  TFPT expectation: {res['tfpt_expectation']['allowed_intrinsic_dipole']} "
          "(FLRW + tiny boundary remnant; dissolution predicted)\n")
    print(f"  CatWISE2020: D_obs = {obs['catwise_D_obs']} vs kinematic "
          f"{obs['kinematic_expectation_D']} -> excess x{obs['excess_factor']}, "
          f"{obs['direction']}\n")
    print("  claimed significances:")
    for leg in res["claimed_legs"]:
        sig = f"{leg['significance_sigma']:.1f}s" if leg["significance_sigma"] else "--"
        print(f"      {leg['name']:55s} {sig}")
    print("  clustering/mask-aware reassessments:")
    for r in res["clustering_mask_reassessments"]:
        sig = f"{r['significance_sigma']:.2f}s" if r["significance_sigma"] else "contested"
        print(f"      {r['name']:55s} {sig}")
    lo, hi = res["significance_spread_sigma"]
    print(f"\n  honest spread: {lo:.1f} - {hi:.1f} sigma depending on the "
          "clustering/mask error budget")
    print(f"  deciders: {res['deciders']}")
    print(f"  kill rule: {res['kill_rule']}")

    verdict_line = (f"DIPOLE WATCHDOG: excess x{obs['excess_factor']} real in every catalog; "
                    f"FLRW-violation significance contested ({lo:.1f}-{hi:.1f} sigma) -> "
                    f"{res['verdict']} (watch). TFPT requires dissolution; a confirmed "
                    f">=5 sigma intrinsic dipole would strike the FLRW-based cosmology branch.")
    print(f"\n-> {verdict_line}")
    res["verdict_line"] = verdict_line

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
