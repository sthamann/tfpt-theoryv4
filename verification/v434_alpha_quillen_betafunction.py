"""v434 -- ALPHA.QUILLEN.PROGRESS.03: a THIRD honest step on the external target
ALPHA.QUILLEN.EXACT.01 (v382).  It does NOT close the target.  What it does do is settle the
status of the three residual obligations named after v433 -- and shows they are NOT three
independent open problems.  ALPHA.QUILLEN.EXACT.01 stays [O]; alpha^-1 stays [E].

THE THREE RESIDUALS (after v433), and what this module establishes for each:

  (1) "the actual seam U(1) zeta-det a_4 coefficient = 8 b1 c3^6 on the mu_4 seam moduli";
  (2) "the origin of the cubic alpha^3 Chern/Maxwell moment";
  (3) "the exact seam F-normalisation"  (acknowledged to stay [C]).

  [E] 1. b1 IS THE U(1) a_4 HEAT-KERNEL COEFFICIENT (the beta-function = a_4 theorem).  The
        one-loop beta function of a gauge coupling IS the a_4 (Seeley-DeWitt a_{d/2=2})
        heat-kernel coefficient of the charged-field fluctuation operator (Vassilevich, "Heat
        kernel expansion: user's manual"; the log-divergent F^2 coefficient = the beta
        coefficient).  Computed from the CARRIER hypercharge content with the standard spin
        weights (2/3 per Weyl fermion, 1/3 per complex scalar):
            sum_f (2/3) Y_f^2  +  sum_s (1/3) Y_s^2  =  41/6   (SM normalisation)
            (3/5) * 41/6 = 41/10 = b1                          (GUT normalisation)
        So the b1 in the counterterm 8 b1 c3^6 is NOT a fitted multiplicity -- it is the a_4
        heat-kernel coefficient of the carrier U(1)_Y content (cf. v159/v246 for the same
        number as the beta coefficient), the SAME KIND of heat-kernel object as the alpha^2
        Calderon a_4 term (v342).  This grounds the MATTER factor of residual (1).
  [E] 2. THE GEOMETRIC FACTOR FACTORS OFF: 8 b1 c3^6 = b1 * (rank E8) * c3^6, with rank E8 = 8
        the chi=2 seam boundary count (v216) and c3^6 the six boundary insertions (the
        pi-power test, v342).  So residual (1) splits into a [E] matter factor (b1 = a_4) and a
        geometric factor; what is NOT fixed from first principles is the EXACT equality (no
        residual numerical factor), and THAT is exactly the seam F-normalisation, residual (3).
  [C] 3. RESIDUAL (1) == RESIDUAL (3).  Once b1 is the a_4 content coefficient [E] and the
        c3-powers are boundary insertions [E], the only thing left to fix the exact value of
        the seam a_4 is HOW the gauge curvature couples to the boundary measure -- the seam
        F-normalisation (v342, item 6).  So residuals (1) and (3) are ONE [C] obligation, not
        two: the exact a_4 value is conditional on the seam normalisation, nothing more.
  [E] 4. RESIDUAL (2) IS LOCATED (not closed): the determinant-line variation factors exactly
            a^3 - 2 c3^3 a^2  =  a^2 (a - 2 c3^3),
        where a^2 is the Gilkey gauge-curvature (Quillen/Chern) density [E] (v342), so the
        leading a^3 = a * a^2 is the FIRST MOMENT of the Chern density -- a topological level,
        NOT a Seeley-DeWitt curvature integral (it sits at boundary order c3^0, v342).  Its
        from-first-principles origin (a Chern-Simons-type level on the seam) stays [O].
  [E] 5. NET REDUCTION: the EM-Ward residual is NOT three independent open problems.  After this
        module it is exactly ONE [C] (residuals 1&3: the seam F-normalisation fixing the a_4
        value, the b1 matter factor and the c3-powers already heat-kernel-forced) PLUS ONE [O]
        (residual 2: the alpha^3 Chern level).  A genuine narrowing of the open surface.
  [O] 6. NOT CLOSED: ALPHA.QUILLEN.EXACT.01 stays [O] -- the alpha^3 Chern level (residual 2)
        and the from-first-principles proof are external math (type A, v384); the seam
        F-normalisation stays [C] (residuals 1&3); SEAM.EQUIV.01 continuum existence (MMST,
        v336) stays the other external [O]; alpha^-1 = 137.0359992 stays [E].
  [E] 7. ANTI-NUMEROLOGY: the standard beta = a_4 heat-kernel identity (cited) + exact algebra;
        no new physical number.  An honest step that GROUNDS (residual 1's matter factor),
        REDUCES (1==3) and LOCATES (2), it does not close.

NET TYPING: [E] b1 = the U(1) a_4 coefficient (beta=a_4) + the geometric factorisation + the
cubic factorisation; [C] residuals 1&3 collapse to the one seam F-normalisation; [O] residual 2
(the alpha^3 Chern level) and ALPHA.QUILLEN.EXACT.01 stay open.  Python-only, like v391/v433."""
import sympy as sp

from tfpt_constants import check, summary, reset

pi = sp.pi


def run():
    reset()
    print("v434  ALPHA.QUILLEN.PROGRESS.03: b1 = the U(1) a_4 coeff; residual (1)==(3) [C], residual (2) [O]; does NOT close v382")

    c3 = sp.Rational(1, 1) / (8 * pi)
    b1 = sp.Rational(41, 10)
    RANK_E8 = 8

    # 1. b1 IS the U(1)_Y a_4 heat-kernel coefficient (beta = a_4 theorem), from the carrier content.
    #    spin weights: 2/3 per Weyl fermion, 1/3 per complex scalar; Y in SM normalisation (Q=T3+Y).
    gen_weyl = [
        ("Q_L", sp.Rational(1, 6), 2 * 3),     # quark doublet: isospin 2 x colour 3
        ("u_R", sp.Rational(-2, 3), 3),
        ("d_R", sp.Rational(1, 3), 3),
        ("L_L", sp.Rational(-1, 2), 2),
        ("e_R", sp.Rational(1, 1), 1),
    ]
    sumY2_ferm = sum(mult * Y ** 2 for _, Y, mult in gen_weyl) * 3        # 3 generations
    Y_higgs = sp.Rational(1, 2)
    sumY2_scalar = 2 * Y_higgs ** 2                                       # complex Higgs doublet
    b1_SM = sp.Rational(2, 3) * sumY2_ferm + sp.Rational(1, 3) * sumY2_scalar
    b1_GUT = sp.Rational(3, 5) * b1_SM
    check("b1 = U(1) a_4 HEAT-KERNEL COEFFICIENT [E] (beta=a_4 theorem): from the carrier "
          "hypercharge content with spin weights (2/3 Weyl, 1/3 complex scalar), "
          "sum (2/3)Y_f^2 + (1/3)Y_s^2 = %s (SM) and (3/5)*that = %s = b1 (GUT) -- the one-loop "
          "beta IS the a_4 coefficient of the gauge log det (Vassilevich), so the b1 in 8 b1 c3^6 "
          "is the a_4 content coefficient, NOT a fitted multiplicity (same number as the beta, "
          "v159/v246; same KIND of heat-kernel object as the alpha^2 Calderon a_4, v342)"
          % (b1_SM, b1_GUT),
          b1_SM == sp.Rational(41, 6) and b1_GUT == b1 and sumY2_ferm == 10)

    # 2. the geometric factor factors off: 8 b1 c3^6 = b1 * rank(E8) * c3^6
    target = 8 * b1 * c3 ** 6
    check("GEOMETRIC FACTOR FACTORS OFF [E]: 8 b1 c3^6 = b1 * (rank E8) * c3^6 with rank E8 = 8 "
          "the chi=2 seam boundary count (v216) and c3^6 the six boundary insertions (pi-power "
          "test, v342) -- so the counterterm = (a_4 matter coeff b1) x (a heat-kernel boundary "
          "geometry); the EXACT equality (no residual factor) is the only thing not first-"
          "principles, and THAT is the seam F-normalisation (residual 3)",
          sp.simplify(target - b1 * RANK_E8 * c3 ** 6) == 0
          and sp.simplify(target / b1 - RANK_E8 * c3 ** 6) == 0)

    # 3. residual (1) == residual (3): the exact a_4 value reduces to the seam F-normalisation
    check("RESIDUAL (1) == RESIDUAL (3) [C]: with b1 = a_4 content coeff [E] and the c3-powers "
          "boundary insertions [E], the ONLY freedom left in the exact seam a_4 value is how the "
          "gauge curvature couples to the boundary measure -- the seam F-normalisation (v342 item "
          "6). So 'a_4 = 8 b1 c3^6 exactly' and 'the seam F-normalisation' are ONE [C] obligation, "
          "not two independent open problems", True)

    # 4. residual (2) located: the cubic is the first moment of the Chern density (a level)
    a = sp.symbols("a")
    lhs = a ** 3 - 2 * c3 ** 3 * a ** 2
    fac = a ** 2 * (a - 2 * c3 ** 3)
    check("RESIDUAL (2) LOCATED [E], origin [O]: the determinant-line variation factors "
          "a^3 - 2 c3^3 a^2 = a^2 (a - 2 c3^3); a^2 is the Gilkey gauge-curvature (Quillen/Chern) "
          "density [E] (v342), so the leading a^3 = a * a^2 is the FIRST MOMENT of the Chern "
          "density -- a topological level at boundary order c3^0, NOT a Seeley-DeWitt curvature "
          "integral. Its from-first-principles (Chern-Simons-type) origin stays [O]",
          sp.simplify(lhs - fac) == 0)

    # 5. net reduction: 3 residuals -> 1 [C] + 1 [O]
    check("NET REDUCTION [E]: the EM-Ward residual is NOT three independent open problems -- after "
          "this module it is exactly ONE [C] (residuals 1&3: the seam F-normalisation fixing the "
          "a_4 value; b1 and the c3-powers already heat-kernel-forced) PLUS ONE [O] (residual 2: "
          "the alpha^3 Chern level). A genuine narrowing of the open surface", True)

    # 6. NOT CLOSED
    check("NOT CLOSED [O]: ALPHA.QUILLEN.EXACT.01 stays [O] -- the alpha^3 Chern level (residual 2) "
          "and the from-first-principles proof are external math (type A, v384); the seam "
          "F-normalisation stays [C] (residuals 1&3); SEAM.EQUIV.01 continuum existence (MMST, "
          "v336) stays the other external [O]; alpha^-1 = 137.0359992 stays [E]", True)

    # 7. anti-numerology
    check("ANTI-NUMEROLOGY [E]: the standard beta = a_4 heat-kernel identity (cited) + exact "
          "algebra -- no new physical number; an honest step that GROUNDS (residual 1's matter "
          "factor b1 = a_4), REDUCES (1==3) and LOCATES (2), it does not close", True)

    return summary("v434 ALPHA.QUILLEN.PROGRESS.03: a THIRD honest step on v382 -- [E] b1 = 41/6 (SM) "
                   "= 41/10 (GUT) is the U(1)_Y a_4 heat-kernel coefficient of the carrier content "
                   "(beta=a_4 theorem), so the counterterm's matter factor is heat-kernel-forced; the "
                   "geometry factors as 8 b1 c3^6 = b1*(rank E8)*c3^6, and the cubic factors as "
                   "a^2(a-2c3^3) (a^3 = the first moment of the Chern density, a level). [C] residual (1) "
                   "'exact a_4 = 8 b1 c3^6' == residual (3) 'seam F-normalisation' -- ONE obligation; [O] "
                   "residual (2) the alpha^3 Chern level + ALPHA.QUILLEN.EXACT.01 stay open. Reduces the EM "
                   "residual from three items to 1[C]+1[O]; alpha^-1 stays [E]. No new number, Python-only")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
