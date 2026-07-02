"""``tfpt-ringdown analyze`` -- the black-hole-direct QNM family-count signature.

TFPT/Hod cross-link (v57, horizon_readouts): the asymptotic high-overtone Schwarzschild
QNM real frequency satisfies omega_R -> T_H ln 3, so

    omega_R / T_H -> ln 3 = ln N_fam        (the ringdown carries the family count)

and the Bekenstein-Mukhanov-Hod area quantum is Delta A = 4 ln3 l_p^2 = ln(N_fam^4) = ln 81
(= ln of the discriminant of the flavor cover). The numerical identity ln3 = ln N_fam is
exact; the black-hole identification is [C]/[P] (Hod's '3' is spin-dependent).

HONEST SCOPE: the asymptotic omega_R/T_H = ln3 lives in the n->inf overtone limit;
measured ringdowns see the n=0 fundamental, which sits in a different regime. So the
direct family-count test is DATA-LIMITED until high-overtone ringdown spectroscopy.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

N_FAM = 3
LN3 = math.log(3.0)
DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
RESULTS = Path(__file__).resolve().parents[2] / "results"

# Schwarzschild dimensionless real frequencies (geometric M*omega):
M_OMEGA_FUNDAMENTAL = 0.3737      # n=0 (l=m=2), measured regime
M_OMEGA_ASYMPTOTIC = LN3 / (8.0 * math.pi)   # Hod high-n limit: M omega_R -> ln3/(8pi)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT QNM family-count (ln3) ringdown signature")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)

    print("=" * 72)
    print("TFPT QNM family-count signature: omega_R/T_H -> ln3 = ln N_fam")
    print("=" * 72)
    print(f"  ln 3 = ln N_fam = {LN3:.6f}  (exact numerical identity, N_fam={N_FAM})")
    print(f"  area quantum 4 ln3 = ln(N_fam^4) = ln 81 = {4*LN3:.6f}")
    print(f"  Schwarzschild: M*omega fundamental(n=0) = {M_OMEGA_FUNDAMENTAL:.4f}; "
          f"Hod asymptotic(n->inf) M*omega = ln3/(8pi) = {M_OMEGA_ASYMPTOTIC:.4f}")
    if args.command == "audit":
        return 0

    m = json.loads(DATA.read_text(encoding="utf-8"))
    ratio = M_OMEGA_FUNDAMENTAL / M_OMEGA_ASYMPTOTIC
    print(f"\n  structural identity ln3 = ln N_fam: {abs(LN3 - math.log(N_FAM)) < 1e-12}")
    print(f"  fundamental / asymptotic real-frequency ratio = {ratio:.1f} "
          f"(the measured n=0 mode is NOT in the asymptotic ln3 regime)")
    print("\n  per-event (measured fundamental vs where the asymptotic ln3 mode sits;"
          " Hz from DETECTOR-frame mass M(1+z) -- omega_R/T_H itself is frame-immune):")
    rows = []
    for ev in m["events"]:
        m_det = ev["M_final_Msun"] * (1.0 + float(ev.get("redshift", 0.0)))
        Mgeo = m_det * 4.92549e-6                       # GM/c^3 in s, detector frame
        f_fund = M_OMEGA_FUNDAMENTAL / (2 * math.pi * Mgeo)
        f_asym = M_OMEGA_ASYMPTOTIC / (2 * math.pi * Mgeo)
        rows.append({"name": ev["name"], "f220_measured_Hz": ev["f220_Hz"],
                     "M_detector_Msun": m_det,
                     "f_fundamental_pred_Hz": f_fund, "f_asymptotic_ln3_Hz": f_asym})
        print(f"    {ev['name']:10s} f220(meas)={ev['f220_Hz']:.0f} Hz, "
              f"M_det={m_det:.1f} Msun, f_fund(Schw)~{f_fund:.0f} Hz, "
              f"f_asym(ln3)~{f_asym:.0f} Hz")

    verdict = ("structural: ln3 = ln N_fam exactly and the area quantum is 4 ln3 = ln 81 "
               "= ln(N_fam^4); but the asymptotic omega_R/T_H=ln3 lives in the high-overtone "
               "limit, while measured ringdowns see the n=0 fundamental -> the black-hole-direct "
               "family-count test is DATA-LIMITED (needs high-overtone spectroscopy). [C]/[P]: "
               "Hod's '3' is spin-dependent, the N_fam identification is suggestive, not forced.")
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(
        {"ln3": LN3, "area_quantum_4ln3": 4 * LN3, "N_fam": N_FAM,
         "M_omega_fundamental": M_OMEGA_FUNDAMENTAL, "M_omega_asymptotic": M_OMEGA_ASYMPTOTIC,
         "fundamental_over_asymptotic": ratio, "events": rows,
         "status": "data_limited", "verdict": verdict}, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
