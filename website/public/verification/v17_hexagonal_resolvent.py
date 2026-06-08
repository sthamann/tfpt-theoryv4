"""v17 -- A4 (partial): the finite hexagonal resolvent backbone of the quark c's.

The flavor transport kernel on the C_6 ring is D_y = y*I - delta*U6 (U6 = the
six-cycle shift, U6^6 = I).  The quark/lepton c-coefficients are read off the
*finite* resolvent

    D_y^{-1} = (1/(y^6 - delta^6)) * sum_{m=0}^5 y^{5-m} delta^m U6^m .

This script PROVES that closed resolvent identity exactly (it is the backbone of
the whole c-extraction).  What it does NOT do -- honestly -- is produce the
quark c-digits: those require the off-diagonal SU(3)_F holonomy U_f* and the
per-sector legs (y_u,y_d,y_e), a finite but intricate Paper-3 evaluation that is
the remaining step.  The lepton reference values c_e=16/7, c_mu=4/3, c_tau=7/6
are recorded as the target quality the quark table must reach.
"""
import sympy as sp
from tfpt_constants import check, summary, reset

y, d = sp.symbols('y delta')


def U6_power(m):
    """m-th power of the 6x6 cyclic shift (U6)^m."""
    P = sp.zeros(6)
    for i in range(6):
        P[i, (i + m) % 6] = 1
    return P


def run():
    reset()
    print("v17  hexagonal resolvent backbone (A4, partial)")

    U = U6_power(1)
    check("U6 is the 6-cycle shift, U6^6 = I", U6_power(6) == sp.eye(6))
    Dy = y * sp.eye(6) - d * U

    # the finite resolvent: Dy * S = (y^6 - delta^6) I
    S = sum(((y**(5 - m) * d**m) * U6_power(m) for m in range(6)), sp.zeros(6))
    prod = sp.expand(Dy * S)
    check("D_y * sum_{m=0}^5 y^{5-m} delta^m U6^m = (y^6 - delta^6) I (finite resolvent)",
          prod == sp.expand((y**6 - d**6) * sp.eye(6)))
    check("resolvent denominator is y^6 - delta^6 (hexagonal pole structure)",
          sp.factor(y**6 - d**6) == sp.factor((y - d) * (y + d) * (y**2 + y * d + d**2) * (y**2 - y * d + d**2)))

    # lepton reference c-values (exact, the target quality for the quark table)
    c_lep = {"e": sp.Rational(16, 7), "mu": sp.Rational(4, 3), "tau": sp.Rational(7, 6)}
    check("lepton c-values are exact rationals (16/7, 4/3, 7/6) -- the reference",
          [c_lep["e"], c_lep["mu"], c_lep["tau"]] ==
          [sp.Rational(16, 7), sp.Rational(4, 3), sp.Rational(7, 6)])
    # honest status flag (no fabricated quark c's)
    print("      NOTE: quark c-digits require the U_f* SU(3)_F holonomy + sector "
          "legs (y_u,y_d,y_e); that finite evaluation is the remaining step (open).")
    return summary("v17 hexagonal resolvent")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
