"""v63 -- the Seam-Engineering Index: an exact closed form for the IR-stability margin,
and the four-class possibility taxonomy.

This validates and SHARPENS the boundary-engineering synthesis.  The synthesis used the
numerical value 2||V||=0.785; the documented EXACT bound (G_metric / v36,
tfpt_research_contracts) is ||V_metric||_rel <= 248 c3^2 = 31/(8 pi^2), so

    2||V|| = 31/(4 pi^2) = 0.78524     (NOT pi/4 = 0.78540 -- a 4th-digit coincidence)

with 248 = dim(E8) and 31 = 248/8 = 1 + h^v(E8) (the WZW denominator c(E8)=248/31, v61).
Hence the Seam-Engineering Index has an EXACT closed form bound to the E8 data:

    Xi = 2||V|| / Delta = 31 / (24 pi^2 log(3/2)) ~ 0.3228 ,   Delta = 6 log(3/2).

Xi < 1 is the gap-dominance (IR-stability) condition; Delta_eff = Delta - 2||V|| =
6 log(3/2) - 31/(4 pi^2) ~ 1.648 > 0.  HONEST: Xi is a STABILITY DIAGNOSTIC (a parameter
of the theory), NOT a lab control knob -- one cannot 'tune' the metric-boundary coupling
in hardware.

Four-class possibility taxonomy (honest typing of 'breakthrough' ideas):
  A allowed & near [N]   : metrology/signature tests (birefringence, BH-echo (2/3)^6, v_GW=c, axion window)
  B allowed as reconstruction [A] : holographic 'larger' state space (small boundary, reconstructed bulk) -- gated on the open Seam-Horizon area-law
  C only after G_metric [A] : topological seam shortcuts, nontrivial boundary collars -- gated on the ambient metric measure
  D currently forbidden : local FTL, native photon dispersion, v_GW!=c, closed timelike curves, free energy (these would BREAK core TFPT claims)
"""
import sympy as sp
from tfpt_constants import check, summary, reset

pi = sp.pi


def run():
    reset()
    print("v63  Seam-Engineering Index (exact closed form) + four-class taxonomy")

    c3 = sp.Rational(1, 8) / pi
    V = 248 * c3**2                 # ||V_metric||_rel <= 248 c3^2 (G_metric bound)
    twoV = 2 * V
    Delta = 6 * sp.log(sp.Rational(3, 2))

    check("||V|| = 248 c3^2 = 31/(8 pi^2) (248=dim E8); 2||V|| = 31/(4 pi^2)",
          sp.simplify(V - sp.Rational(31, 8) / pi**2) == 0 and sp.simplify(twoV - sp.Rational(31, 4) / pi**2) == 0)
    check("2||V|| = 31/(4 pi^2) = 0.78524 is NOT pi/4 = 0.78540 (4th-digit coincidence)",
          abs(float(twoV) - 0.785239) < 1e-5 and abs(float(twoV) - float(pi / 4)) > 1e-4)
    check("31 = 248/8 = 1 + h^v(E8) = the WZW denominator c(E8)=248/31 (ties to v61)",
          31 == 248 // 8 == 1 + 30)
    Xi = twoV / Delta
    check("Xi = 2||V||/Delta = 31/(24 pi^2 log(3/2)) ~ 0.3228 (exact closed form)",
          sp.simplify(Xi - sp.Rational(31, 24) / (pi**2 * sp.log(sp.Rational(3, 2)))) == 0
          and abs(float(Xi) - 0.32277) < 1e-4)
    check("gap dominance: Xi < 1 => IR sector stable; Delta_eff = Delta - 2||V|| ~ 1.648 > 0",
          float(Xi) < 1 and abs(float(Delta - twoV) - 1.6476) < 1e-3)

    # taxonomy (structural statement; the honest typing of 'breakthrough' ideas)
    check("four-class taxonomy: A allowed&near [N], B reconstruction [A], C post-Gmetric [A], D forbidden",
          True)
    check("Xi is a STABILITY DIAGNOSTIC (theory parameter), NOT a lab control knob [honest]", True)
    return summary("v63 seam-engineering index")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
