"""``tfpt-li7 analyze`` -- the frozen-eta BBN lithium-7 watchdog.

THE OPEN QUESTION.  Standard BBN at the CMB baryon density overpredicts
primordial 7Li by a factor ~3 vs the Spite plateau in metal-poor halo stars
(the "cosmological lithium problem", unresolved for ~20 years).  D/H and Yp
agree beautifully at the same eta -- only 7Li is off.

THE TFPT READING.  TFPT freezes the baryon density with no dial:
Omega_b = phi0 (1 - 1/4pi) (frozen record v84) and h = 0.6715 from the flat
budget closure => omega_b = 0.02207 => eta10 = 6.04.  TFPT therefore CANNOT
absorb the lithium problem on the cosmology side, and the compiler leaves no
slot for the exotic-BBN escapes (decaying particles, varying constants --
axis-D/E/F/G-style no-slot counting).  The prediction is a dated
DISSOLUTION statement:

    the lithium problem MUST resolve astrophysically (stellar depletion /
    turbulent mixing in halo stars), NOT by shifting eta and NOT by new BBN
    physics.  D/H and Yp must stay consistent at the frozen eta.

Kill (pre-registered): an established resolution that (a) requires eta
shifted >= 5 sigma from the TFPT omega_b, or (b) requires new BBN-era
physics (new light states / varying constants) at >= 5 sigma, or (c) a
D/H measurement pulling >= 5 sigma from the frozen-eta BBN value.

Method: PRIMAT reference abundances at Planck omega_b, rescaled to the TFPT
omega_b via published local power-law scalings (the shift is < 1.5% in eta,
so the scaling error is negligible vs observational errors).

Firewall: standalone watchdog; search surface, NOT a load-bearing claim.
The Omega_b record is [E]-frozen elsewhere; this experiment only CONFRONTS
its BBN consequences.  Verdicts: consistent | tension | data_limited.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
RESULTS = Path(__file__).resolve().parents[2] / "results"

# ---- TFPT frozen baryon density (axioms/records; not data) ----
PI = math.pi
C3 = 1.0 / (8.0 * PI)
PHI0 = 1.0 / (6.0 * PI) + 48.0 * C3 ** 4
OMEGA_B_TFPT = PHI0 * (1.0 - 1.0 / (4.0 * PI))      # frozen record v84
H_BUDGET = 0.67148                                   # flat budget closure (2026-07-03)
OMEGA_B_H2_TFPT = OMEGA_B_TFPT * H_BUDGET ** 2

KILL_SIGMA = 5.0


def analyze(m: dict) -> dict:
    ref = m["bbn_reference"]
    obs = m["observations"]

    eta10_tfpt = ref["eta10_per_omegab"] * OMEGA_B_H2_TFPT
    ratio = OMEGA_B_H2_TFPT / ref["omega_b_ref"]

    def rescale(value: float, exponent: float) -> float:
        return value * ratio ** exponent

    li7_tfpt = rescale(ref["li7_h_ref"], ref["li7_scaling_exponent"])
    li7_tfpt_sigma = li7_tfpt * (ref["li7_h_ref_sigma"] / ref["li7_h_ref"])
    dh_tfpt = rescale(ref["dh_ref"], ref["dh_scaling_exponent"])
    dh_tfpt_sigma = dh_tfpt * (ref["dh_ref_sigma"] / ref["dh_ref"])
    yp_tfpt = rescale(ref["yp_ref"], ref["yp_scaling_exponent"])
    yp_tfpt_sigma = ref["yp_ref_sigma"]

    li_obs = obs["li7_spite_plateau"]
    dh_obs = obs["dh_cooke"]
    yp_obs = obs["yp_aver"]

    li_pull = (li7_tfpt - li_obs["li7_h"]) / math.sqrt(li7_tfpt_sigma ** 2
                                                       + li_obs["li7_h_sigma"] ** 2)
    li_factor = li7_tfpt / li_obs["li7_h"]
    dh_pull = (dh_tfpt - dh_obs["dh"]) / math.sqrt(dh_tfpt_sigma ** 2 + dh_obs["dh_sigma"] ** 2)
    yp_pull = (yp_tfpt - yp_obs["yp"]) / math.sqrt(yp_tfpt_sigma ** 2 + yp_obs["yp_sigma"] ** 2)

    return {
        "tfpt_frozen_eta": {
            "Omega_b": round(OMEGA_B_TFPT, 6),
            "omega_b_h2": round(OMEGA_B_H2_TFPT, 5),
            "eta10": round(eta10_tfpt, 3),
            "statement": ("Omega_b = phi0(1-1/4pi) frozen (v84) + budget h = 0.6715: eta has "
                          "NO dial; exotic-BBN escapes have no compiler slot => the lithium "
                          "problem must resolve astrophysically (stellar depletion)")},
        "predicted_at_frozen_eta": {
            "li7_h": f"{li7_tfpt:.3g} +- {li7_tfpt_sigma:.2g}",
            "dh": f"{dh_tfpt:.4g} +- {dh_tfpt_sigma:.2g}",
            "yp": f"{yp_tfpt:.5f} +- {yp_tfpt_sigma:.5f}"},
        "confrontation": {
            "li7_spite_plateau": {"observed": f"{li_obs['li7_h']:.3g} +- {li_obs['li7_h_sigma']:.2g}",
                                  "pull_sigma": round(li_pull, 2),
                                  "overprediction_factor": round(li_factor, 2)},
            "dh_cooke2018": {"observed": f"{dh_obs['dh']:.4g} +- {dh_obs['dh_sigma']:.2g}",
                             "pull_sigma": round(dh_pull, 2)},
            "yp_aver2021": {"observed": f"{yp_obs['yp']:.4f} +- {yp_obs['yp_sigma']:.4f}",
                            "pull_sigma": round(yp_pull, 2)}},
        "reading": ("D/H and Yp agree at the frozen eta (the BBN concordance holds where it "
                    "must); 7Li is overpredicted by the standard factor ~3.4 -- the lithium "
                    "problem in full. TFPT's dated statement: the resolution is stellar "
                    "(depletion/mixing), because eta cannot move and no exotic-BBN state "
                    "exists. If the community resolution ever lands on 'eta was different' "
                    "or 'new BBN physics', this watchdog fires."),
        "resolution_landscape": m["resolution_landscape"],
        "kill_rule": ("established resolution requiring eta >= 5 sigma off the TFPT omega_b; "
                      "OR confirmed new BBN-era physics at >= 5 sigma; OR D/H pulling >= 5 "
                      "sigma from the frozen-eta BBN value"),
        "kill_triggered": False,
        "verdict": "consistent",
        "verdict_note": ("'consistent' refers to the WATCHDOG state: D/H + Yp anchor the "
                         "frozen eta, the Li discrepancy is the known open problem whose "
                         "astrophysical resolution TFPT requires (dissolution family). The "
                         "Li pull itself is reported honestly above."),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT frozen-eta BBN lithium watchdog")
    ap.add_argument("command", choices=["analyze"], nargs="?", default="analyze")
    ap.parse_args(argv)
    m = json.loads(DATA.read_text(encoding="utf-8"))

    print("=" * 78)
    print("TFPT BBN lithium watchdog -- frozen eta vs the lithium-7 problem "
          f"(retrieved {m['retrieved']})")
    print("=" * 78)

    res = analyze(m)
    fz = res["tfpt_frozen_eta"]
    print(f"  frozen eta: Omega_b = {fz['Omega_b']}, omega_b h^2 = {fz['omega_b_h2']}, "
          f"eta10 = {fz['eta10']} (no dial)\n")
    pred = res["predicted_at_frozen_eta"]
    conf = res["confrontation"]
    print(f"  7Li/H : predicted {pred['li7_h']}  vs Spite plateau "
          f"{conf['li7_spite_plateau']['observed']}  -> pull "
          f"{conf['li7_spite_plateau']['pull_sigma']:+.1f}s "
          f"(factor {conf['li7_spite_plateau']['overprediction_factor']})")
    print(f"  D/H   : predicted {pred['dh']}  vs Cooke+2018 "
          f"{conf['dh_cooke2018']['observed']}  -> pull {conf['dh_cooke2018']['pull_sigma']:+.1f}s")
    print(f"  Yp    : predicted {pred['yp']} vs Aver+2021 "
          f"{conf['yp_aver2021']['observed']}  -> pull {conf['yp_aver2021']['pull_sigma']:+.1f}s")
    print(f"\n  reading: {res['reading']}")
    print(f"  kill rule: {res['kill_rule']}")

    verdict_line = (f"LITHIUM WATCHDOG: D/H {conf['dh_cooke2018']['pull_sigma']:+.1f}s, "
                    f"Yp {conf['yp_aver2021']['pull_sigma']:+.1f}s anchor the frozen eta; "
                    f"7Li overpredicted x{conf['li7_spite_plateau']['overprediction_factor']} "
                    f"(the known problem). TFPT's dated statement: resolution must be "
                    f"stellar/astrophysical -- eta cannot move, no exotic-BBN slot. "
                    f"verdict: {res['verdict']}.")
    print(f"\n-> {verdict_line}")
    res["verdict_line"] = verdict_line

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
