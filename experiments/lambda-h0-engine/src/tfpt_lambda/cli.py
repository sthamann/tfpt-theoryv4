"""``tfpt-lambda analyze`` -- the TFPT cosmological-constant / Hubble engine.

One EM fixed point alpha^-1 sets the cosmological constant and the de Sitter horizon
(origin_theory sec.alpha): the smallness of Lambda is e^{-2 alpha^-1}, not a tuning.

    rho_Lambda / M_pl^4   = (3 / 256 pi^4) e^{-2 ainv}      -> ~122.95 orders (unreduced)
    rho_Lambda / Mbar^4   = (3 / 4 pi^2)   e^{-2 ainv}      -> ~120.15 orders (reduced)
    S_dS * rho_Lambda     = 1/(128 c3^4) = 32 pi^4          (exact dimensionless identity)
    H0 / Mbar            ~ e^{-ainv}/(2 pi)                 (one engine: H0 ~ sqrt(Lambda))

Confronted with the measured Lambda (Omega_Lambda, H0). Consistency, not a parameter-free
prediction of Lambda itself (the absolute scale is the one anchor).
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

AINV = 137.035999          # EM fixed point (v3_em_alpha)
C3 = 1.0 / (8.0 * math.pi)
RESULTS = Path(__file__).resolve().parents[2] / "results"

# measured cosmology (Planck 2018)
OMEGA_LAMBDA = 0.6889
# 67.36 km/s/Mpc -> 1/s (x1e3 m/km / 3.086e22 m/Mpc) -> GeV (x hbar = 6.582e-25 GeV s)
H0_GEV = 67.36 * 1e3 / 3.0856775814913e22 * 6.582119569e-25
MBAR_GEV = 2.435e18        # reduced Planck mass


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT Lambda/H0 engine vs measured cosmology")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)

    # TFPT predicted orders of magnitude
    orders_unreduced = 2 * AINV / math.log(10) + math.log10(256 * math.pi**4 / 3)
    orders_reduced = 2 * AINV / math.log(10) + math.log10(4 * math.pi**2 / 3)
    sds_rho = 32 * math.pi**4
    inv_128c3_4 = 1.0 / (128 * C3**4)
    h0_over_mbar_tfpt = math.e ** (-AINV) / (2 * math.pi)

    print("=" * 72)
    print("TFPT cosmological-constant engine (one alpha^-1 -> Lambda, S_dS, H0)")
    print("=" * 72)
    print(f"  alpha^-1 = {AINV}")
    print(f"  rho_Lambda/M_pl^4  = (3/256pi^4) e^-2ainv -> {orders_unreduced:.3f} orders (unreduced)")
    print(f"  rho_Lambda/Mbar^4  = (3/4pi^2)  e^-2ainv -> {orders_reduced:.3f} orders (reduced)")
    print(f"  S_dS * rho_Lambda  = 1/(128 c3^4) = 32 pi^4 = {sds_rho:.3f} "
          f"(check 1/(128c3^4)={inv_128c3_4:.3f})")
    if args.command == "audit":
        return 0

    # measured orders from Omega_Lambda, H0, Mbar:
    # rho_Lambda/Mbar^4 = 3 Omega_Lambda (H0/Mbar)^2 ; unreduced divides by (8pi)^2/... = 64pi^2
    h0_over_mbar = H0_GEV / MBAR_GEV
    rho_over_mbar4 = 3 * OMEGA_LAMBDA * h0_over_mbar**2
    meas_reduced = -math.log10(rho_over_mbar4)
    meas_unreduced = -math.log10(rho_over_mbar4 / (64 * math.pi**2))

    print(f"\n  measured (Omega_Lambda={OMEGA_LAMBDA}, H0/Mbar={h0_over_mbar:.2e}):")
    print(f"    rho_Lambda/Mbar^4  -> {meas_reduced:.3f} orders   (TFPT {orders_reduced:.3f}, "
          f"dev {abs(meas_reduced-orders_reduced):.3f})")
    print(f"    rho_Lambda/M_pl^4  -> {meas_unreduced:.3f} orders  (TFPT {orders_unreduced:.3f}, "
          f"dev {abs(meas_unreduced-orders_unreduced):.3f})")
    print(f"    H0/Mbar measured {h0_over_mbar:.2e} (log10 {math.log10(h0_over_mbar):+.2f}) vs "
          f"TFPT e^-ainv/(2pi) {h0_over_mbar_tfpt:.2e} (log10 {math.log10(h0_over_mbar_tfpt):+.2f})")

    dev = abs(meas_unreduced - orders_unreduced)
    verdict = (f"consistency: the EM fixed point alpha^-1 reproduces the measured Lambda "
               f"hierarchy to {dev:.2f} orders (122.95 predicted vs {meas_unreduced:.2f} measured) "
               f"and H0/Mbar ~ e^-ainv/(2pi) to ~0.1 dex; the dimensionless identity "
               f"S_dS rho_Lambda = 32 pi^4 is exact. One engine for Lambda, S_dS and H0 -- "
               f"a consistency, not a parameter-free derivation of the absolute scale (the anchor).") \
        if dev < 1.0 else f"tension: predicted vs measured Lambda orders differ by {dev:.2f}"
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(
        {"alpha_inv": AINV, "orders_unreduced_tfpt": orders_unreduced,
         "orders_reduced_tfpt": orders_reduced, "orders_unreduced_meas": meas_unreduced,
         "orders_reduced_meas": meas_reduced, "S_dS_rho_Lambda": sds_rho,
         "H0_over_Mbar_tfpt": h0_over_mbar_tfpt, "H0_over_Mbar_meas": h0_over_mbar,
         "verdict": verdict}, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
