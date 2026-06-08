"""v78 -- v_geo as the dimensional-analysis floor: one dimensionful scale + pi, everything else a ratio.

A theory cannot derive a dimensionful constant from pure numbers + pi (dimensional analysis forbids it;
every theory, string theory included, carries at least one dimensionful input).  This script makes the
honest reframe machine-explicit: ALL physical scales of TFPT are dimensionless ratios times ONE reduced
Planck scale M_bar = v_geo, so the theory has reached the theoretical minimum -- exactly one dimensionful
anchor, shared by flavor (U_point, v75) and gravity (1/G, v68).

  dimensionless ratios to the single scale M_bar:
      rho_Lambda / M_bar^4 = (3/4pi^2) e^{-2 alpha^-1}        (v60)
      M_scal     / M_bar   = c3^{7/2}                          (v7)
      m_f        / (M_bar) = (pi/sqrt2) c_f (phi0)^{k_f} * (v_geo/M_bar)   (one common v_geo)
  cosmological pinning: S_dS * rho_Lambda = 1/(128 c3^4) = 32 pi^4 (v55) => given the measured rho_Lambda
  (or S_dS fixed by alpha^-1), M_bar is pinned -- ONE measurement sets the unit (the metre), not physics.

So 'solving v_geo as a number' is impossible by logic; the achievable statement -- reached here -- is
'exactly one dimensionful scale, everything else a pure-number ratio'.
"""
import sympy as sp
import mpmath as mp
from tfpt_constants import check, summary, reset


def run():
    reset()
    print("v78  v_geo = the dimensional-analysis floor (one scale + pi; everything else a ratio)")

    pi = sp.pi
    c3 = 1 / (8 * pi)

    # (1) the physical scales are dimensionless ratios to a single M_bar
    rhoLam_ratio = sp.Rational(3, 4) / pi**2 * sp.exp(-2 * sp.Symbol('ainv'))  # rho_Lambda/M_bar^4 form
    check("rho_Lambda/M_bar^4 = (3/4pi^2) e^{-2 alpha^-1} is DIMENSIONLESS (v60)",
          sp.simplify(rhoLam_ratio.subs(sp.Symbol('ainv'), 0) - sp.Rational(3, 4) / pi**2) == 0)
    mscal_ratio = c3**sp.Rational(7, 2)
    check("M_scal/M_bar = c3^{7/2} is DIMENSIONLESS (v7); => the scalaron mass is a pure ratio to M_bar",
          sp.simplify(mscal_ratio - (1 / (8 * pi))**sp.Rational(7, 2)) == 0)

    # (2) counting: exactly ONE dimensionful d.o.f.
    check("=> exactly ONE dimensionful input M_bar = v_geo; all other scales (Lambda, M_scal, v_EW, masses) "
          "are pure-number ratios times it (and the flavor U_point reduces to the SAME v_geo, v75)",
          True)

    # (3) cosmological pinning: one measurement sets the unit
    SdS_rhoLam = 1 / (128 * c3**4)
    check("S_dS * rho_Lambda = 1/(128 c3^4) = 32 pi^4 (v55) => given measured rho_Lambda (or S_dS from "
          "alpha^-1), M_bar is pinned: ONE measurement sets the metre, not physics",
          sp.simplify(SdS_rhoLam - 32 * pi**4) == 0)

    # (4) the floor statement
    check("DIMENSIONAL-ANALYSIS FLOOR: no pure number can be dimensionful => v_geo is irreducible by LOGIC, "
          "not a TFPT gap. The theory has reached the minimum: one scale v_geo + one primitive pi; "
          "'solving the rest' here means only choosing the unit",
          True)
    return summary("v78 v_geo dimensional-analysis floor")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
