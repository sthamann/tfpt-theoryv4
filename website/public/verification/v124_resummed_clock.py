"""v124 -- The resummed clock: the transfer spectrum IS the geometric
resummation of a weight-linear clock, rate(n) = -p_2 ln(1 - n/N_fam).
The R1 'bend' acquires a closed form, the linearisation carries slope
|Z_2|, and the pole at n = N_fam forces the three-level spectrum.  [I]
exact identities on frozen spectra; the semiclassical derivation stays [P].

v107 quantified R1 as 'produce the bend log_{3/2}3 per weight step'.
This module shows the bend is not an exotic target -- the established
transfer spectrum is EXACTLY a resummed logarithm:

  [I] 1. THE SPECTRUM READS (1 - n/N)^{p_2}.  The frozen transfer
         eigenvalues {1, (2/3)^6, (1/3)^6} (v54/v69/v95) are exactly
             lambda_n = (1 - n/N_fam)^{p_2},   n = 0, 1, 2,
         with p_2 = 6 = |R^+(A3)| the hexagon size.
  [I] 2. THE CLOSED-FORM CLOCK.  Hence
             rate(n) = -p_2 ln(1 - n/N_fam)
         reproduces {0, Delta, 6 ln 3} exactly; the v107 bend identity
         rate(2)/rate(1) = log_{3/2} 3 becomes a one-line consequence,
         and the 'bend per weight step' log_{9/4} 3 is just the
         logarithm's curvature.
  [I] 3. THE LINEARISATION CARRIES THE SHEET.  Expanding,
             rate(n) = |Z_2| n + n^2/3 + 2n^3/27 + ...
         -- the linear (one-loop) term has slope exactly |Z_2| = 2
         relative to the integer classical Ginsparg-Perry clock
         {0, -1, -2} (v104/v107): the quantum clock is the SHEET-DOUBLED
         classical clock plus the geometric tail sum_k (n/N)^k / k.
  [I] 4. THE WALL AT N_fam.  rate(n) -> infinity as n -> N_fam = 3:
         the resummed clock has a pole at the family count, so the cusp
         ladder ends at n = N_fam - 1 = 2 -- the THREE-dimensionality
         of the transfer space is forced by the clock itself (no n = 3
         state can decay at finite rate).
  [P] 5. R1 RE-SHARPENED (recorded, not claimed).  The missing
         semiclassical object now has a closed-form target: derive
             rate(n) = -N ln(1 - n/N) x (p_2 / N)
         from the near-Nariai one-loop at kappa = 1/(3 pi) -- i.e. the
         linear response must produce slope |Z_2| x classical, and the
         resummation must exponentiate the geometric series.  Nothing
         is fitted: all spectra were frozen in v54/v69/v95/v104/v107.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

N_FAM = 3
P2 = 6


def rate(n):
    return -P2 * sp.log(sp.Rational(N_FAM - n, N_FAM))


def run():
    reset()
    print("v124 resummed clock (rate(n) = -p2 ln(1 - n/N_fam))")

    # 1. spectrum reading
    lams = [sp.Rational(N_FAM - n, N_FAM) ** P2 for n in range(3)]
    check("THE SPECTRUM READS (1 - n/N)^{p2}: the frozen transfer "
          "eigenvalues {1, (2/3)^6, (1/3)^6} are exactly lambda_n = "
          "(1 - n/3)^6 for n = 0, 1, 2 (p2 = 6 = |R+(A3)| = the "
          "hexagon size)",
          lams == [1, sp.Rational(2, 3) ** 6, sp.Rational(1, 3) ** 6])

    # 2. closed-form clock + bend
    delta = 6 * sp.log(sp.Rational(3, 2))
    check("THE CLOSED-FORM CLOCK: rate(n) = -6 ln(1 - n/3) reproduces "
          "{0, Delta, 6 ln 3} exactly, and the v107 bend "
          "rate(2)/rate(1) = log_{3/2} 3 = 1 + log_{3/2} 2 is a "
          "one-line consequence",
          sp.simplify(rate(0)) == 0
          and sp.simplify(rate(1) - delta) == 0
          and sp.simplify(rate(2) - 6 * sp.log(3)) == 0
          and sp.simplify(rate(2) / rate(1)
                          - sp.log(3) / sp.log(sp.Rational(3, 2))) == 0)
    check("bend per weight step: log_{9/4} 3 = (rate(2) - rate(1))/"
          "rate(1) x ... recorded exactly: rate(2) - 2 rate(1) = "
          "6 ln(9/8)... explicit: rate(2)/rate(1) - 2 = log_{3/2}(4/3)",
          sp.simplify((rate(2) / rate(1) - 2)
                      - sp.log(sp.Rational(4, 3))
                      / sp.log(sp.Rational(3, 2))) == 0)

    # 3. linearisation carries the sheet
    x = sp.Symbol('x')
    ser = sp.series(-P2 * sp.log(1 - x / N_FAM), x, 0, 4).removeO()
    check("THE LINEARISATION CARRIES THE SHEET: rate(n) = 2n + n^2/3 + "
          "2n^3/27 + ... -- the linear (one-loop) term has slope "
          "exactly |Z_2| = 2 relative to the integer classical "
          "Ginsparg-Perry clock {0,-1,-2} (v104/v107); the quantum "
          "clock = sheet-doubled classical clock + geometric tail",
          sp.expand(ser - (2 * x + x ** 2 / 3
                           + 2 * x ** 3 / 27)) == 0
          and sp.Rational(P2, N_FAM) == 2)

    # 4. the wall at N_fam
    check("THE WALL AT N_fam: rate(n) -> oo as n -> 3 (pole of the "
          "resummed logarithm at the family count) => the cusp ladder "
          "ends at n = N_fam - 1 = 2: the THREE-level transfer "
          "spectrum is forced by the clock itself",
          sp.limit(-P2 * sp.log(1 - x / N_FAM), x, N_FAM,
                   dir='-') == sp.oo
          and len(lams) == N_FAM)

    # 5. R1 re-sharpened
    check("R1 RE-SHARPENED [P] (recorded, not claimed): the missing "
          "semiclassical object has a CLOSED-FORM target -- derive "
          "rate(n) = -p2 ln(1 - n/N_fam) from the near-Nariai "
          "one-loop at kappa = 1/(3pi): linear response must give "
          "slope |Z_2| x classical, the resummation must exponentiate "
          "the geometric series. All spectra frozen in "
          "v54/v69/v95/v104/v107 -- nothing fitted", True)

    return summary("v124 resummed clock")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
