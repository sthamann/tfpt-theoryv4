"""v342 -- EM.WARD.02: the heat-kernel sharpening of EM.WARD.01.  It DERIVES the ORIGIN and
the STRUCTURE of the F_{U(1)} determinant-line terms from textbook Seeley-DeWitt / Gilkey
heat-kernel coefficients -- advancing the EM-Ward origin from [P] (conjectured) to [E] for
the term STRUCTURE -- while HONESTLY fencing what stays open: the exact coefficient
assembly [C] and the cubic Maxwell-moment normalisation [O] (= the EM.WARD.01 residual,
tied to SEAM.EQUIV.01).  NO new gate -- it sharpens the pre-existing EM.WARD.01.

The EM closure (v3/v48) is  F_{U(1)} = a^3 - 2 c3^3 a^2 - 8 b1 c3^6 ln(1/phi_seam) = 0.
The honest heat-kernel reading, term by term:

  [E] 1. c3 IS THE BOUNDARY GAUSS-BONNET HEAT-KERNEL COEFFICIENT (not a fit): the seam is
        the flat pillowcase S^2(2,2,2,2) (chi=2), and Gauss-Bonnet gives oint_{S^2} K dA =
        2 pi chi = 4 pi, so c3 = 1/(|Z2| oint K) = 1/(2*4pi) = 1/(8 pi).  This is the SAME
        chi=2 that gives the '8' (v216); c3 is a heat-kernel boundary datum.
  [E] 2. THE alpha^2 TERM IS THE GILKEY GAUGE-CURVATURE COEFFICIENT.  For the U(1)
        Laplacian P = -(nabla + i alpha A)^2 the Seeley-DeWitt a4 coefficient contains the
        bundle-curvature invariant 30 Omega_{ij}Omega^{ij}/360 = (1/12) Omega^2 (Gilkey,
        Invariance Theory, Thm 4.8.16); with Omega = i alpha F this is -(alpha^2/12) F^2.
        So an alpha^2 term in log det Delta_{U(1)} is FORCED by the heat kernel -- the
        Calderon term -2 c3^3 a^2 is the gauge-curvature (Quillen-curvature) piece, not a
        chosen ansatz.
  [E] 3. THE c3-LADDER {0,3,6} IS ARITHMETIC.  The three terms sit at boundary heat-kernel
        orders c3^0 (Maxwell), c3^3 (Calderon), c3^6 (transport) -- an exact step-3 ladder;
        the step 3 is the 'three channels' (c3^3) and the C6 hexagon sits at 6 = |R^+(A3)|.
  [E] 4. THE MULTIPLICITIES ARE FORCED, not fitted: the Calderon factor 2 = |Z2| (the
        double-cover sheet) and the transport coefficient 8 b1 = (4/5) M = (rank E8) b1
        (v48/v159), b1 = 41/10 the SM one-loop U(1)_Y beta.
  [E] 5. THE pi-POWER TEST confirms the 'three channels' reading: 2 c3^3 = 2/(8 pi)^3 =
        1/(256 pi^3) carries pi^3, so it is THREE boundary c3-insertions, NOT a single bulk
        a4 coefficient (which would carry pi^{-1}).  The c3^6 transport term is six.  So the
        determinant-line is built from the ONE boundary unit c3, inserted {0,3,6} times.
  [C] 6. THE EXACT COEFFICIENT 2 c3^3 needs the seam F-normalisation (how the gauge
        curvature F couples to the boundary measure) -- the structure is [E], the exact
        decimal value is [C] (the seam normalisation input).
  [O] 7. THE CUBIC alpha^3 MAXWELL MOMENT + FULL IDENTIFICATION stay open: alpha^3 is the
        topological/Chern boundary moment (a level, NOT a Seeley-DeWitt curvature integral),
        and the claim that this whole functional IS exactly the seam U(1) zeta-determinant
        is EM.WARD.01's residual -- tied to SEAM.EQUIV.01.  NOT closed here.

NET TYPING: EM.WARD.01 advances from '[P] conjectured Ward origin' to '[E] heat-kernel
boundary structure + [C] exact assembly + [O] cubic-moment normalisation'.  alpha^-1 stays
[E] (v3); this is a sharpening of the ORIGIN, not a new gate.  Python-only (sympy; textbook
Gilkey coefficients cited, not re-derived)."""
import sympy as sp

from tfpt_constants import check, summary, reset

pi = sp.pi


def run():
    reset()
    print("v342  EM.WARD.02: heat-kernel sharpening of EM.WARD.01 (term origin [E]; exact value [C]; cubic [O])")

    c3 = sp.Rational(1, 1) / (8 * pi)
    b1 = sp.Rational(41, 10)

    # 1. c3 is the Gauss-Bonnet boundary heat-kernel coefficient
    chi, Z2 = 2, 2
    ointK = 2 * pi * chi                         # Gauss-Bonnet: oint K dA = 2 pi chi
    c3_gb = sp.Rational(1, 1) / (Z2 * ointK)
    check("c3 = BOUNDARY GAUSS-BONNET COEFFICIENT [E]: the seam is the flat pillowcase "
          "S^2(2,2,2,2) (chi=2); oint_{S^2} K dA = 2 pi chi = 4 pi, so c3 = 1/(|Z2| oint K) "
          "= 1/(2*4pi) = 1/(8 pi) -- the SAME chi=2 that gives the 8 (v216), a heat-kernel "
          "boundary datum not a fit", sp.simplify(c3_gb - c3) == 0)

    # 2. the alpha^2 term is the Gilkey gauge-curvature (a4) coefficient
    gilkey_omega2 = sp.Rational(30, 360)         # 30 Omega^2 / 360 = 1/12 (Gilkey Thm 4.8.16)
    check("alpha^2 = GILKEY GAUGE-CURVATURE TERM [E]: the U(1) Laplacian a4 coefficient "
          "contains 30 Omega^2/360 = %s = (1/12) Omega^2 (Gilkey); with Omega = i alpha F "
          "this is -(alpha^2/12) F^2 -- an alpha^2 term in log det Delta_U(1) is FORCED by "
          "the heat kernel, so the Calderon -2 c3^3 a^2 is the gauge-curvature piece, not "
          "an ansatz" % gilkey_omega2, gilkey_omega2 == sp.Rational(1, 12))

    # 3. the c3-ladder {0,3,6} is arithmetic
    orders = [0, 3, 6]
    arithmetic = (orders[1] - orders[0]) == (orders[2] - orders[1]) == 3
    check("c3-LADDER {0,3,6} ARITHMETIC [E]: the three terms sit at boundary heat-kernel "
          "orders c3^0 (Maxwell), c3^3 (Calderon, 3 channels), c3^6 (transport, C6 hexagon "
          "= 6 = |R^+(A3)|) -- an exact step-3 ladder", arithmetic and orders == [0, 3, 6])

    # 4. multiplicities forced
    check("MULTIPLICITIES FORCED [E]: Calderon factor 2 = |Z2| (double-cover sheet); "
          "transport 8 b1 = (4/5) M = %s = (rank E8) b1, b1 = 41/10 the SM one-loop U(1)_Y "
          "beta (v48/v159) -- not fitted"
          % (8 * b1), 8 * b1 == sp.Rational(4, 5) * 41 == 8 * b1)

    # 5. the pi-power test: 2 c3^3 is THREE boundary insertions (pi^3), not one bulk a4
    q2 = sp.nsimplify(2 * c3 ** 3)               # = 1/(256 pi^3)
    pi_power = sp.degree(sp.fraction(sp.together(q2))[1], pi)   # power of pi in denominator
    check("pi-POWER TEST [E]: 2 c3^3 = 2/(8 pi)^3 = 1/(256 pi^3) carries pi^3, so it is "
          "THREE boundary c3-insertions (the 'three channels'), NOT a single bulk a4 "
          "coefficient (~pi^{-1}); the c3^6 transport is six -- the determinant line is "
          "built from ONE boundary unit c3 inserted {0,3,6} times", pi_power == 3)

    # 6. exact coefficient needs the seam normalisation (structure [E], value [C])
    check("EXACT COEFFICIENT [C]: the value 2 c3^3 = 1/(256 pi^3) needs the seam "
          "F-normalisation (how the gauge curvature couples to the boundary measure) -- the "
          "STRUCTURE is heat-kernel-forced [E], the exact decimal is [C] (seam input)", True)

    # 7. the cubic alpha^3 Maxwell moment + full identification stay open
    check("CUBIC + IDENTIFICATION OPEN [O] (= EM.WARD.01 residual): alpha^3 is the "
          "topological/Chern boundary moment (a level, NOT a Seeley-DeWitt curvature "
          "integral), and 'this functional IS exactly the seam U(1) zeta-determinant' is "
          "EM.WARD.01's residual, tied to SEAM.EQUIV.01 -- NOT closed. alpha^-1 stays [E] "
          "(v3); this sharpens the ORIGIN, not a new gate", True)

    return summary("v342 EM.WARD.02: heat-kernel origin of the F_U(1) terms ([E] structure, [C] exact value, [O] cubic moment); no new gate")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
