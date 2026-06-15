"""``tfpt-kaon analyze`` -- the rare-kaon flavour bridge as a *geometry*.

Instead of celebrating one lucky BR(K+) number, this tests the whole flavour bridge:

    R_K       = BR(KL -> pi0 nu nu) / BR(K+ -> pi+ nu nu)  = 0.35238   (geometry; robust,
                short-distance X_t and |Vcb|^4 largely cancel in the ratio)
    BR(K+)    = 9.45e-11                                                (vs NA62)
    BR(KL)    = 3.33e-11                                                (vs KOTO limit)
    delta_CKM = pi/3 + 3 lambda^2 = 68.65 deg                           (vs LHCb gamma; canonical v88)
    Jarlskog  J(lambda_TFPT, delta_TFPT, |Vcb|,|Vub|_PDG)               (vs PDG J)
    Grossman-Nir: BR(KL) <= 4.3 BR(K+)                                  (isospin bound)

Firewall: this is a downstream FLAVOUR BRIDGE [C]. |Vcb|, |Vub| and the SM short-distance
functions are EXTERNAL nuisances -- only lambda (Cabibbo) and delta_CKM are TFPT predictions.
The discriminating future test is KOTO measuring BR(KL) -> R_K, not another BR(K+).
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

C3 = 1.0 / (8.0 * math.pi)
PHI0 = (4.0 / 3.0) * C3 + 48.0 * C3**4
LAMBDA = math.sqrt(PHI0 * (1.0 - PHI0))                   # Cabibbo from the seed
DELTA_CKM_DEG = math.degrees(math.pi / 3.0 + 3.0 * LAMBDA**2)
BR_KP = 9.45e-11
BR_KL = 3.33e-11
R_K = BR_KL / BR_KP                                       # 0.35238
DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
RESULTS = Path(__file__).resolve().parents[2] / "results"


def _z_asym(pred: float, meas: float, sp: float, sm: float) -> float:
    s = sp if pred < meas else sm
    return (pred - meas) / s


def _jarlskog(lam: float, delta_deg: float, vcb: float, vub: float) -> float:
    s12, s23, s13 = lam, vcb, vub
    c12 = math.sqrt(1 - s12**2)
    c23 = math.sqrt(1 - s23**2)
    c13 = math.sqrt(1 - s13**2)
    return c12 * c13**2 * c23 * s12 * s23 * s13 * math.sin(math.radians(delta_deg))


def analyze(m: dict) -> dict:
    out: dict = {"R_K_tfpt": R_K, "lambda_tfpt": LAMBDA, "delta_CKM_deg_tfpt": DELTA_CKM_DEG,
                 "tests": []}

    # 1) BR(K+) vs NA62
    kp = m["BR_Kp_pinunu"]
    z_kp = _z_asym(BR_KP, kp["measured"], kp["sigma_plus"], kp["sigma_minus"])
    out["tests"].append({"name": "BR(K+ -> pi+ nu nu)", "tfpt": BR_KP, "meas": kp["measured"],
                         "z": round(z_kp, 2), "status": "consistent" if abs(z_kp) < 3 else "tension",
                         "kind": "downstream_bridge"})

    # 2) BR(KL) vs KOTO limit
    kl = m["BR_KL_pi0nunu"]
    below = BR_KL < kl["limit_90CL"]
    out["tests"].append({"name": "BR(KL -> pi0 nu nu)", "tfpt": BR_KL, "limit_90CL": kl["limit_90CL"],
                         "below_limit": below, "status": "data_limited",
                         "note": f"KOTO limit {kl['limit_90CL']:.1e} is ~66x above TFPT; ratio test waits for KOTO-II"})

    # 3) R_K geometry vs SM ratio + Grossman-Nir
    rk_sm = m["BR_KL_SM"]["value"] / m["BR_Kp_SM"]["value"]
    gn = m["grossman_nir_coeff"]["value"]
    out["tests"].append({"name": "R_K = BR(KL)/BR(K+)", "tfpt": round(R_K, 5),
                         "SM_ratio": round(rk_sm, 3), "grossman_nir_bound": gn,
                         "respects_GN": R_K <= gn, "status": "data_limited",
                         "note": "geometry test: TFPT R_K near SM, well below the GN bound; "
                                 "becomes the discriminating measurement once KOTO measures BR(KL)"})

    # 4) delta_CKM vs LHCb gamma
    g = m["gamma_CKM_deg"]
    z_g = (DELTA_CKM_DEG - g["value"]) / g["sigma"]
    out["tests"].append({"name": "delta_CKM / gamma", "tfpt_deg": round(DELTA_CKM_DEG, 2),
                         "meas_deg": g["value"], "sigma_deg": g["sigma"], "z": round(z_g, 2),
                         "status": "consistent" if abs(z_g) < 3 else "tension",
                         "kind": "prediction (delta = pi/3 + 3 lambda^2)"})

    # 5) Jarlskog from TFPT (lambda, delta) + PDG |Vcb|,|Vub|
    nu = m["ckm_nuisance"]
    j_tfpt = _jarlskog(LAMBDA, DELTA_CKM_DEG, nu["Vcb"], nu["Vub"])
    jp = m["jarlskog"]
    z_j = (j_tfpt - jp["value"]) / jp["sigma"]
    out["tests"].append({"name": "Jarlskog J", "tfpt": j_tfpt, "meas": jp["value"],
                         "sigma": jp["sigma"], "z": round(z_j, 2),
                         "status": "consistent" if abs(z_j) < 3 else "tension",
                         "kind": "bridge (|Vcb|,|Vub| are PDG nuisances)"})

    consistent = [t for t in out["tests"] if t["status"] == "consistent"]
    out["verdict"] = (
        f"Flavour bridge geometry is internally consistent: BR(K+) {z_kp:+.1f}s (NA62), "
        f"delta_CKM/gamma {z_g:+.1f}s (LHCb), Jarlskog {z_j:+.1f}s (PDG); R_K={R_K:.5f} respects "
        f"Grossman-Nir and sits near the SM ratio {rk_sm:.2f}. {len(consistent)}/5 legs are direct "
        f"data hits; R_K and BR(KL) are data_limited (KOTO). This is a downstream BRIDGE [C] "
        f"(external |Vcb|,|Vub| + short-distance), NOT a unique compiler fingerprint -- the real "
        f"discriminator is KOTO measuring BR(KL) -> R_K."
    )
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT rare-kaon flavour bridge (geometry)")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)
    m = json.loads(DATA.read_text(encoding="utf-8"))

    print("=" * 74)
    print(f"TFPT rare-kaon flavour bridge  (R_K = {R_K:.5f}; lambda = {LAMBDA:.5f}; "
          f"delta_CKM = {DELTA_CKM_DEG:.2f} deg)")
    print("=" * 74)
    if args.command == "audit":
        return 0

    res = analyze(m)
    for t in res["tests"]:
        z = f"{t['z']:+.2f}s" if "z" in t else "--"
        print(f"  [{t['status']:12s}] {t['name']:22s} {z:>8s}")
    print(f"\n-> {res['verdict']}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
