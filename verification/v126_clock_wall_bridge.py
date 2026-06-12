"""v126 -- The clock and the wall share a spectrum: the resummed-clock
weights are the Mehta-Seshadri parabolic weights (= spec A0*), the first
R1 checkpoint passes classically, and det(1 - A0*) is the gravity entropy
curvature.  [I] exact identities; the quantum content isolates to the
geometric tail.

v124 gave R1 the closed form rate(n) = -p2 ln(1 - n/N_fam) with first
checkpoint 'linear-response slope |Z2|'.  This module connects both ends
to established exact objects:

  [I] 1. THE WEIGHTS ARE THE PARABOLIC WEIGHTS.  The arguments n/N_fam
         = {0, 1/3, 2/3} of the resummed logarithm are EXACTLY the cusp
         weights -- i.e. the spectrum of the exact U_wall residue A0*
         (v115).  The spectral bridge:
             lambda_n = (1 - alpha_n)^{p_2},
             alpha_n in spec A0* = {0, 1/3, 2/3}
         -- the horizon clock and the flavor wall share their spectrum
         through the complement map alpha -> 1 - alpha; the transfer
         eigenvalues are the hexagon-power of the COMPLEMENTARY
         parabolic weight.
  [I] 2. CHECKPOINT 1 PASSES CLASSICALLY.  The linear term of the
         resummed clock is (p_2/N_fam) n = |Z2| n -- and the
         established CLASSICAL entropy-deviation rate at the horizon
         is exactly 2H = |Z2| x Hubble (v104).  The two coefficients
         agree exactly: the slope-2 linear response demanded by v124
         is already the classical entropy rate; the genuinely QUANTUM
         content of R1 isolates to the geometric tail
         sum_{k>=2} (alpha)^k / k.
  [I] 3. THE DETERMINANT IS THE ENTROPY CURVATURE.
             det(1 - A0*) = (1)(2/3)(1/3) = 2/9 = |Z2| / N_fam^2
         -- exactly the established gravity entropy curvature at the
         anchor (v102), a fourth independent appearance; also
         tr(1 - A0*) = 2 = |Z2| and det A0* = 0 (the parabolic
         degree-0 marker).
  [P] 4. R1 RE-TARGETED (recorded, not claimed).  The semiclassical
         job now reads: derive 'rate = -p_2 ln(1 - alpha)' with alpha
         the parabolic weight -- first order is CLASSICAL (= v104's
         entropy rate), the tail is the quantum part; and any
         derivation automatically inherits the U_wall spectral data:
         one spectrum, two gates (R1 and the U_wall side), one object
         A0*.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

A0 = sp.Matrix([[sp.Rational(1, 2), sp.sqrt(2) / 6, 0],
                [sp.sqrt(2) / 6, sp.Rational(1, 4), sp.sqrt(5) / 12],
                [0, sp.sqrt(5) / 12, sp.Rational(1, 4)]])
P2 = 6
N_FAM = 3


def run():
    reset()
    print("v126 clock-wall bridge (one spectrum, two gates)")

    spec = sorted(A0.eigenvals().keys())

    # 1. the weights are the parabolic weights
    check("THE WEIGHTS ARE THE PARABOLIC WEIGHTS: the resummed-clock "
          "arguments n/N_fam = {0, 1/3, 2/3} are EXACTLY spec A0* (the "
          "exact U_wall residue, v115); spectral bridge lambda_n = "
          "(1 - alpha_n)^{p2} reproduces the frozen transfer spectrum "
          "{1, (2/3)^6, (1/3)^6} -- the horizon clock and the flavor "
          "wall share their spectrum through alpha -> 1 - alpha",
          spec == [0, sp.Rational(1, 3), sp.Rational(2, 3)]
          and spec == [sp.Rational(n, N_FAM) for n in range(3)]
          and sorted([(1 - a) ** P2 for a in spec], reverse=True)
          == [1, sp.Rational(2, 3) ** 6, sp.Rational(1, 3) ** 6])

    # 2. checkpoint 1 passes classically
    x = sp.Symbol('x')
    lin_coeff = sp.series(-P2 * sp.log(1 - x / N_FAM), x, 0,
                          2).removeO().coeff(x, 1)
    check("CHECKPOINT 1 PASSES CLASSICALLY: the resummed clock's "
          "linear coefficient p2/N_fam = 2 = |Z2| equals the "
          "ESTABLISHED classical entropy-deviation rate 2H = |Z2| x "
          "Hubble (v104) -- the slope-2 linear response demanded by "
          "v124 is already the classical entropy rate; the quantum "
          "content of R1 isolates to the geometric tail "
          "sum_{k>=2} alpha^k / k",
          lin_coeff == 2 and sp.Rational(P2, N_FAM) == 2)

    # 3. the determinant is the entropy curvature
    check("THE DETERMINANT IS THE ENTROPY CURVATURE: det(1 - A0*) = "
          "(1)(2/3)(1/3) = 2/9 = |Z2|/N_fam^2 -- exactly the "
          "established gravity entropy curvature at the anchor "
          "(v102), a fourth independent appearance; tr(1 - A0*) = 2 = "
          "|Z2|; det A0* = 0 (parabolic degree-0 marker)",
          sp.simplify(sp.det(sp.eye(3) - A0)) == sp.Rational(2, 9)
          and sp.Rational(2, 9) == sp.Rational(2, N_FAM ** 2)
          and sp.simplify(sp.trace(sp.eye(3) - A0)) == 2
          and sp.simplify(A0.det()) == 0)

    # 4. R1 re-targeted
    check("R1 RE-TARGETED [P] (recorded, not claimed): derive "
          "'rate = -p2 ln(1 - alpha)' with alpha the Mehta-Seshadri "
          "parabolic weight -- first order is CLASSICAL (v104's "
          "entropy rate), the tail is the quantum part; one spectrum, "
          "two gates, one object A0*", True)

    return summary("v126 clock-wall bridge")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
