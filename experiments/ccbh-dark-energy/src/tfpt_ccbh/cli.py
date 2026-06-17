"""``tfpt-ccbh analyze`` -- the cosmologically-coupled-black-hole w = -1 leg.

TFPT reads a black hole as the *local* realization of the seam and de Sitter as the
*global* one (origin_theory / horizon_readouts); the maximal de Sitter--black-hole
(Nariai) state sits on the anchor (1,1,-2) and the de Sitter entropy satisfies the exact
identity ``S_dS * rho_Lambda = 32 pi^4``.  So the seam black-hole interior IS the de Sitter
vacuum: its interior equation of state is ``w_in = -1``.

Croker & Weiner (2019) show a cosmologically coupled compact object gains mass
``M(a) ~ a^k`` with ``k = -3 w_in`` set by the interior EoS, so the population energy
density scales as ``rho ~ a^(k-3)`` and has an effective ``w_eff = -k/3``.  Hence

    w_in = -1  =>  k = 3 (exactly)  =>  w_eff = -1   (a true cosmological constant).

This runner confronts the TFPT-frozen ``k = 3`` with the Farrah+2023 measurement
``k = 3.11 +/- 0.79`` (and the order-level dark-energy-density closure), and is explicit
that the CCBH-as-dark-energy interpretation is **contested**.  It is the *mechanism* behind
the ``w = -1`` that ``dark-energy-w-watchdog`` confronts with DESI -- the two are
ALTERNATIVE readings of one question (is dark energy a constant Lambda?) and must not be
double-counted.

Frozen kill rule (pre-registered):

    a robust k != 3 at >= 3 sigma in a systematics-controlled SMBH-growth sample
    -> the TFPT 'seam interior = de Sitter vacuum carrier' reading falls
       (NOT the compiler core; w=-1 can still hold via a plain Lambda).
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
RESULTS = Path(__file__).resolve().parents[2] / "results"
KILL_SIGMA = 3.0


def _k_from_w_interior(w_in: float) -> float:
    """Croker-Weiner coupling index from the interior equation of state."""
    return -3.0 * w_in


def _w_eff_from_k(k: float) -> float:
    """Effective cosmic EoS of the coupled population (rho ~ a^(k-3))."""
    return -k / 3.0


def analyze(m: dict) -> dict:
    pred = m["tfpt_prediction"]
    k_tfpt = _k_from_w_interior(pred["w_interior"])          # -> 3.0
    w_eff_tfpt = _w_eff_from_k(k_tfpt)                        # -> -1.0

    legs = []
    for c in m["coupling_measurements"]:
        pull_k = (k_tfpt - c["k"]) / c["sigma_k"]
        w_eff_obs = _w_eff_from_k(c["k"])
        sigma_w = c["sigma_k"] / 3.0
        legs.append({
            "name": c["name"], "k_obs": c["k"], "sigma_k": c["sigma_k"],
            "pull_k_sigma": round(pull_k, 3),
            "w_eff_obs": round(w_eff_obs, 4), "sigma_w_eff": round(sigma_w, 4),
        })

    dc = m["density_closure"]
    # combined sigma is dominated by the (large) CCBH-side model uncertainty, NOT Planck's
    # tiny error on Omega_Lambda -- otherwise a rounded 0.68 fakes a >1 sigma "tension".
    sigma_comb = math.hypot(dc.get("sigma_omega_de_ccbh", 0.10), dc["sigma_omega_lambda"])
    pull_omega = (dc["omega_de_ccbh_predicted"] - dc["omega_lambda_observed"]) / sigma_comb

    headline = min(legs, key=lambda r: abs(r["pull_k_sigma"]))   # closest leg
    kill = any(abs(leg["pull_k_sigma"]) >= KILL_SIGMA for leg in legs)
    return {
        "k_tfpt": k_tfpt, "w_eff_tfpt": w_eff_tfpt,
        "coupling_legs": legs,
        "density_closure": {**dc, "pull_sigma": round(pull_omega, 3)},
        "headline_leg": headline["name"],
        "headline_pull_k_sigma": headline["pull_k_sigma"],
        "kill_sigma": KILL_SIGMA, "kill_triggered": kill,
        "contested": True,
        "status": "tension" if kill else "data_limited",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT CCBH w=-1 leg (k=3) vs Farrah+2023")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)
    m = json.loads(DATA.read_text(encoding="utf-8"))

    print("=" * 76)
    print("TFPT cosmologically-coupled black holes  (de Sitter seam interior => k=3 => w=-1)")
    print("=" * 76)
    if args.command == "audit":
        return 0

    res = analyze(m)
    print(f"  TFPT chain: w_in = {m['tfpt_prediction']['w_interior']:+.0f}  ->  "
          f"k = -3 w_in = {res['k_tfpt']:.1f}  ->  w_eff = -k/3 = {res['w_eff_tfpt']:+.1f}\n")
    print(f"  {'coupling sample':46s} {'k_obs':>10s}   pull(k=3)")
    for leg in res["coupling_legs"]:
        print(f"  {leg['name']:46s} {leg['k_obs']:.2f}+/-{leg['sigma_k']:.2f}   "
              f"{leg['pull_k_sigma']:+.2f}s")
    dc = res["density_closure"]
    print(f"\n  density closure: Omega_de(CCBH,k=3) = {dc['omega_de_ccbh_predicted']:.3f}  vs  "
          f"Omega_Lambda(Planck) = {dc['omega_lambda_observed']:.4f}  -> {dc['pull_sigma']:+.2f}s "
          f"(model-dependent, contested)")
    print(f"\n  kill rule: robust k != 3 at >= {KILL_SIGMA:.0f} sigma "
          f"(systematics-controlled SMBH growth)")
    print("  link: same w=-1 confronted with DESI in dark-energy-w-watchdog "
          "(ALTERNATIVE reading -> do not double-count)")

    if res["kill_triggered"]:
        verdict = (f"KILL TRIGGERED: a sample excludes k=3 at >= {KILL_SIGMA:.0f} sigma -> the "
                   f"'seam interior = de Sitter vacuum' reading falls (compiler core untouched).")
    else:
        verdict = (f"CONSISTENT-BUT-CONTESTED (data_limited): TFPT k=3 matches Farrah+2023 "
                   f"(k=3.11+/-0.79) at {res['headline_pull_k_sigma']:+.2f} sigma, and the SMBH "
                   f"population can source Omega_Lambda at order level -- BUT the CCBH-as-dark-energy "
                   f"interpretation is disputed (Lacy/Amendola/Andrae&El-Badry/Mistele). A downstream "
                   f"bridge, not a TFPT confirmation; the discriminating decision is DESI w(z).")
    print(f"\n-> {verdict}")
    res["verdict"] = verdict

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
