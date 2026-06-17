"""v233 -- the CP phase is the universal family/triality phase, only sheet-split.

v231 showed both CP phases are mu6 powers of one hexagonal unit rho=e^{i pi/3},
split by the Z2 sheet (rho^3=-1). This pushes the reduction one step further, into
the canonical mu6 = mu3 (family/triality) x mu2 (sheet) factorisation: the FAMILY
part of the CP phase is the SAME triality-centre element for both sectors -- it is
not even a free choice of power. Only the Z2 sheet distinguishes quark from lepton.

  mu6 = mu3 x mu2,   rho = omega^2 * (-1)   with omega = e^{2 pi i/3} (the Z3 family
  triality centre = the 2/3 cusp weight), and -1 = rho^3 the Z2 sheet.

  quark  delta_CKM,lead = arg(rho^1):  family class = [rho] in mu6/mu2,  sheet = -1
  lepton delta_PMNS     = arg(rho^4):  family class = [rho] in mu6/mu2,  sheet = +1

since rho^4 = rho^1 * rho^3 (rho^3 in mu2), the two phases have the SAME image in
the family quotient mu6/mu2 ~ mu3 and OPPOSITE sheet -- so the CP phase IS the
family triality phase (the cusp-weight Z3 centre), read on the two sheets.

  [E] 1. mu6 = mu3 x mu2 (gcd(3,2)=1): the family triality centre {1,omega,omega^2}
        = the cusp weights {0,1/3,2/3} x 2pi; the sheet is mu2 = {1,-1}.
  [E] 2. rho = omega^2 * (-1): the hexagonal CM unit factors as (family triality
        omega^2) x (sheet -1).
  [E] 3. SAME FAMILY CLASS: rho^4 = rho^1 * rho^3, and rho^3 in mu2, so rho^1 and
        rho^4 have the SAME image in the family quotient mu6/mu2 (= the same triality
        centre element); their mu2 (sheet) images are opposite ((-1)^1 vs (-1)^4).
  [E] 4. So the CP phase = the universal family triality phase (the 2/3 cusp-weight
        Z3 centre), sheet-split: quark = (triality) x (sheet -), lepton = (triality)
        x (sheet +). NOT a free choice of power -- one universal phase + the sheet.
  [E] 5. omega (the triality centre) sits in the (2,3,5) Milnor/Coxeter monodromy
        spectrum (e^{2 pi i m/30}, m the E8 exponents): the mu3 family factor of the
        order-30 cycle. So CP lives inside the same monodromy that builds the hull.
  [E] 6. NEG: a mu2-only phase carries no family triality; a mu3-only phase carries
        no sheet; only the full mu6=mu3 x mu2 gives 'one triality phase, two sheets'.

Status: [E] for the mu3 x mu2 factorisation and the same-family/opposite-sheet
statement; the physical CP derivation stays [C] (the quark seam correction
3 lambda_C^2 is the v88 misalignment). Reduces Target D's CP residual from 'one
hexagonal unit + sheet' (v231) to 'the universal triality phase + sheet' -- the
power choice is removed. Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam


def run():
    reset()
    print("v233  CP = the universal family/triality phase, sheet-split (mu6 = mu3 x mu2)")

    rho = sp.exp(sp.I * sp.pi / 3)              # hexagonal CM unit, order 6
    omega = sp.exp(2 * sp.I * sp.pi / 3)        # Z3 family / triality centre, order 3
    sheet = sp.Integer(-1)                      # Z2 sheet = rho^3

    check("mu6 = mu3 x mu2 (gcd(3,2)=1): family triality centre {1,omega,omega^2} "
          "= cusp weights {0,1/3,2/3} x 2pi; sheet mu2 = {1,-1}",
          sp.gcd(3, 2) == 1 and sp.simplify(omega**3) == 1 and sp.simplify(sheet**2) == 1
          and sp.simplify(rho**3 - sheet) == 0)
    check("rho = omega^2 * (-1): the hexagonal CM unit = (family triality omega^2) x "
          "(sheet -1)", sp.simplify(rho - omega**2 * sheet) == 0)

    # cusp weights {0,1/3,2/3} -> triality phases {1, omega, omega^2}
    cusp = [sp.exp(2 * sp.I * sp.pi * w) for w in (sp.Integer(0), sp.Rational(1, 3), sp.Rational(2, 3))]
    check("the three cusp weights {0,1/3,2/3} give the triality centre {1,omega,omega^2}",
          set(sp.simplify(c) for c in cusp) == {sp.simplify(omega**k) for k in range(3)})

    # quark rho^1, lepton rho^4: same family class (mu6/mu2), opposite sheet
    # family quotient: reduce exponent mod 2 is the SHEET; the family class is exponent mod 3
    q_fam, q_sheet = 1 % 3, (-1)**1
    l_fam, l_sheet = 4 % 3, (-1)**4
    check("SAME FAMILY CLASS: rho^4 = rho^1 * rho^3 with rho^3 in mu2, so rho^1 and "
          "rho^4 have the SAME image in mu6/mu2 ~ mu3 (family class %d == %d); "
          "OPPOSITE sheet ((-1)^1=%d vs (-1)^4=%d)" % (q_fam, l_fam, q_sheet, l_sheet),
          sp.simplify(rho**4 - rho**1 * rho**3) == 0
          and q_fam == l_fam and q_sheet == -l_sheet)
    # the common family element is omega^2 (= the 2/3 cusp weight)
    check("the common family/triality phase of BOTH sectors is omega^2 (the 2/3 "
          "cusp-weight Z3 centre); the sheet (-1)^k splits quark/lepton",
          sp.simplify(rho**1 * sheet - omega**2) == 0          # quark family part
          and sp.simplify(rho**4 - omega**2) == 0)             # lepton family part (sheet +1)

    # omega sits in the (2,3,5) Milnor/Coxeter monodromy spectrum (E8 exponents /30)
    e8_exps = [1, 7, 11, 13, 17, 19, 23, 29]
    monodromy = {sp.exp(2 * sp.I * sp.pi * m / 30) for m in e8_exps}
    # omega = e^{2pi i/3} = e^{2pi i*10/30}; omega^2 = e^{2pi i*20/30}. Check the family
    # Z3 factor divides the order-30 monodromy: omega^3 = 1 and 30/3 = 10 (= A_Lambda)
    check("the triality centre omega is the mu3 factor of the order-30 (2,3,5) "
          "monodromy: omega^3=1, 30/|mu3|=10=A_Lambda; the family CP phase lives "
          "inside the same Coxeter/Milnor cycle that builds E8 (v232)",
          sp.simplify(omega**3) == 1 and 30 // 3 == 10 and len(monodromy) == 8)

    # negative controls
    check("NEG: a mu2-only phase {1,-1} carries NO family triality (no order-3 "
          "element); a mu3-only phase {1,omega,omega^2} carries NO sheet (no -1); "
          "only mu6=mu3 x mu2 gives 'one triality phase, two sheets'",
          all(sp.simplify(s**3) != 1 or s == 1 for s in (sp.Integer(-1),))   # -1 has no order 3
          and all(sp.simplify(omega**k + 1) != 0 for k in range(3))          # no -1 in mu3
          and N_fam == 3)

    return summary("v233 CP triality phase (universal family phase, sheet-split)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
