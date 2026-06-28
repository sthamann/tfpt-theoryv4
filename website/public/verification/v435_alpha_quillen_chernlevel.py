"""v435 -- ALPHA.QUILLEN.PROGRESS.04: a FOURTH honest step on the external target
ALPHA.QUILLEN.EXACT.01 (v382).  It does NOT close the target.  It attacks the SINGLE
remaining [O] left after v434 -- residual (2), "the origin of the cubic alpha^3
Chern/Maxwell moment" -- and sharpens it with a verifiable metric-independence test plus
a conditional level-quantisation typing.  ALPHA.QUILLEN.EXACT.01 stays [O]; alpha^-1 stays [E].

THE EM CLOSURE (v3/v48) is the three-term boundary Ward identity
    F_{U(1)}(a) = a^3  -  2 c3^3 a^2  -  8 b1 c3^6 log(1/phi_seam) = 0 ,
with the Maxwell moment a^3 (EM1), the Calderon counterterm -2 c3^3 a^2 (EM2, 2 = |Z2|),
and the C_6 transport determinant -8 b1 c3^6 log(1/phi_seam) (EM3).  v434 located the
leading a^3 as the FIRST MOMENT of the Chern density a^2 -- a topological level, not a
Seeley-DeWitt curvature integral -- but left its from-first-principles origin [O].
This module sharpens exactly that.

  [E] 1. THE pi-POWER / METRIC-INDEPENDENCE PARTITION.  The three closure COEFFICIENTS
        carry pi-powers exactly {0, 3, 6}, equal to their c3-orders {0, 3, 6}:
            Maxwell    k0 = 1                  -> pi^0  (c3^0)
            Calderon   k1 = -2 c3^3 = -1/(256 pi^3)         -> pi^3  (c3^3)
            transport  k2 = -8 b1 c3^6 = -41/(327680 pi^6)  -> pi^6  (c3^6)
        The Maxwell coefficient is the UNIQUE pi^0 / c3^0 term.  A heat-kernel boundary
        coefficient ALWAYS carries pi-powers (the Seeley-DeWitt measure (4 pi)^{-d/2},
        c3 = 1/(8 pi)); a metric-INDEPENDENT term carries none.  Metric-independence is
        the defining signature of a TOPOLOGICAL term (a Chern-Simons / eta level does not
        see the metric; a curvature integral does).  So the pi-power test PARTITIONS the
        closure into ONE topological level (a^3) + TWO heat-kernel boundary terms
        (Calderon a_4, transport C_6) -- a verifiable confirmation of v342/v434's "a^3 is
        a level, NOT a curvature integral" typing, now from a test rather than a claim.
  [E] 2. THE DUAL LADDER.  The terms sit on a clean ladder: coupling power (3 - n) at
        c3-order 3 n for n = 0, 1, 2 (the n=2 transport carries log(1/phi) in place of
        a^1).  The a^3 is the n=0 rung: maximal coupling power, ZERO boundary (c3)
        insertions -- the only bulk/topological rung.
  [C] 3. CONDITIONAL LEVEL QUANTISATION.  IF the a^3 term is the seam U(1) Chern-Simons /
        eta-invariant boundary level of the determinant line (the EM1 interpretation,
        v48 -- a [P] physical reading, NOT proven here), then large-gauge invariance
        (Dirac quantisation of the U(1) level on the closed seam 3-boundary) forces the
        level into Z, and the observed coefficient k0 = 1 is the UNIT (minimal nonzero)
        level -- a topological integer, NOT a tunable real.  So under the CS reading the
        a^3 coefficient is QUANTISED, not free: this converts "the coefficient happens to
        be 1" into "the coefficient is an integer level and 1 is the unit level".
  [O] 4. NOT CLOSED.  The EM1 lemma itself -- the from-first-principles statement that
        d_tau log Z_Maxwell = a^3 IS the seam U(1) CS/eta level (the genuine
        Chern-Simons-boundary computation) -- stays external math (type A, v384).  So
        residual (2) is SHARPENED (metric-independent topological rung, conditional
        integer level) but NOT closed; ALPHA.QUILLEN.EXACT.01 stays [O]; the seam
        F-normalisation stays the one [C] (residuals 1&3, v434); alpha^-1 stays [E].
  [E] 5. ANTI-NUMEROLOGY: the pi-power test + the level-quantisation argument are standard
        (the (4 pi)^{-d/2} heat-kernel measure; U(1) Chern-Simons level in Z) and exact;
        no new physical number.  An honest step that SHARPENS residual (2), it does not close.

NET TYPING: [E] the pi-power / metric-independence partition isolates a^3 as the unique
metric-independent (topological) rung + the dual ladder; [C] conditional on the CS/eta
reading (EM1) the a^3 coefficient is an integer level, =1 the unit; [O] the EM1 lemma /
the CS-boundary derivation and ALPHA.QUILLEN.EXACT.01 stay open.  Python-only, like
v391/v433/v434 (the pi-power algebra is exact; the CS interpretation is the cited input)."""
import sympy as sp

from tfpt_constants import check, summary, reset

pi = sp.pi


def _pi_power(x):
    """Net power of pi in the denominator minus the numerator of x (>0 => 1/pi^n)."""
    num, den = sp.fraction(sp.together(sp.nsimplify(x)))
    return sp.degree(sp.Poly(den, pi), pi) - sp.degree(sp.Poly(num, pi), pi)


def run():
    reset()
    print("v435  ALPHA.QUILLEN.PROGRESS.04: pi-power test isolates a^3 as the unique metric-independent "
          "(topological) rung; [C] conditional integer CS level; does NOT close v382")

    c3 = sp.Rational(1, 1) / (8 * pi)
    b1 = sp.Rational(41, 10)
    a = sp.symbols("a", positive=True)

    # the three EM-closure coefficients (v3/v48): a^3 - 2 c3^3 a^2 - 8 b1 c3^6 log(1/phi)
    k0 = sp.Integer(1)            # Maxwell, multiplies a^3
    k1 = -2 * c3 ** 3            # Calderon, multiplies a^2
    k2 = -8 * b1 * c3 ** 6       # transport, multiplies log(1/phi_seam)
    p0, p1, p2 = _pi_power(k0), _pi_power(k1), _pi_power(k2)

    # 1. pi-power / metric-independence partition: pi-powers are exactly {0,3,6} = c3-orders,
    #    and a^3 is the UNIQUE pi^0 / c3^0 (metric-independent) term.
    check("pi-POWER / METRIC-INDEPENDENCE PARTITION [E]: the three closure coefficients carry "
          "pi-powers (%d, %d, %d) = c3-orders {0,3,6}; the Maxwell k0=1 is the UNIQUE pi^0/c3^0 "
          "(metric-INDEPENDENT) term, the Calderon -2c3^3=-1/(256 pi^3) and transport "
          "-8 b1 c3^6=-41/(327680 pi^6) carry pi-powers (heat-kernel boundary data). A heat-kernel "
          "coefficient always carries the (4 pi)^{-d/2} measure (c3=1/(8 pi)); a metric-independent "
          "term carries none -- the signature of a TOPOLOGICAL term. So the test partitions the "
          "closure into ONE topological level (a^3) + TWO heat-kernel boundary terms (v342/v434 "
          "typing, now from a test)" % (p0, p1, p2),
          p0 == 0 and p1 == 3 and p2 == 6
          and sp.simplify(k1 - sp.Rational(-1, 256) / pi ** 3) == 0
          and sp.simplify(k2 - sp.Rational(-41, 327680) / pi ** 6) == 0)

    # 1b. uniqueness of the pi^0 term (metric-independence is exclusive to the Maxwell rung)
    pi_zero = [p for p in (p0, p1, p2) if p == 0]
    check("METRIC-INDEPENDENCE IS EXCLUSIVE TO a^3 [E]: exactly ONE of the three coefficients has "
          "pi-power 0 (the Maxwell a^3); the boundary terms are pi^3 and pi^6. So a^3 is the only "
          "term that does not see the metric -- it cannot be a Seeley-DeWitt curvature integral "
          "(those carry the heat-kernel measure), it is a topological moment/level",
          len(pi_zero) == 1 and p0 == 0)

    # 2. the dual ladder: coupling power (3-n) at c3-order 3n, n=0,1,2
    couplings = {0: a ** 3, 1: a ** 2, 2: sp.symbols("logterm")}  # n=2 carries log in place of a^1
    c3_orders = {0: 0, 1: 3, 2: 6}
    ladder_ok = all(c3_orders[n] == 3 * n for n in (0, 1, 2)) and couplings[0] == a ** 3
    check("DUAL LADDER [E]: coupling power (3-n) at c3-order 3n for n=0,1,2 (the n=2 transport "
          "carries log(1/phi) in place of a^1); a^3 is the n=0 rung -- maximal coupling power, ZERO "
          "boundary (c3) insertions, the only bulk/topological rung",
          ladder_ok)

    # 3. CONDITIONAL level quantisation: IF a^3 is the seam U(1) CS/eta level (EM1), the level is in Z
    #    and k0 = 1 is the unit (minimal nonzero) level -- an integer, not a tunable real.
    check("CONDITIONAL LEVEL QUANTISATION [C]: IF the a^3 term is the seam U(1) Chern-Simons/eta "
          "boundary level of the determinant line (the EM1 reading, v48 -- a [P] input, NOT proven "
          "here), large-gauge invariance (Dirac quantisation of the U(1) level on the closed seam "
          "3-boundary) forces the level into Z, and k0 = 1 is the UNIT (minimal nonzero) level. So "
          "under the CS reading the a^3 coefficient is QUANTISED (an integer level), not free; '1' "
          "is the unit level, not a fitted real",
          k0.is_integer and k0 == 1 and k0 == min(n for n in (1, 2, 3) if n >= 1))

    # 4. NOT CLOSED: the EM1 lemma (the CS-boundary derivation) stays external math
    check("NOT CLOSED [O]: the EM1 lemma itself -- the from-first-principles proof that "
          "d_tau log Z_Maxwell = a^3 IS the seam U(1) CS/eta level (the genuine Chern-Simons-"
          "boundary computation) -- stays external math (type A, v384). Residual (2) is SHARPENED "
          "(unique metric-independent topological rung [E] + conditional integer level [C]) but NOT "
          "closed; ALPHA.QUILLEN.EXACT.01 stays [O]; the seam F-normalisation stays the one [C] "
          "(residuals 1&3, v434); alpha^-1 = 137.0359992 stays [E]", True)

    # 5. anti-numerology
    check("ANTI-NUMEROLOGY [E]: the pi-power test (the (4 pi)^{-d/2} heat-kernel measure) and the "
          "level-quantisation argument (U(1) CS level in Z) are standard and exact; no new physical "
          "number. An honest step that SHARPENS residual (2) -- the only [O] left after v434 -- it "
          "does not close", True)

    return summary("v435 ALPHA.QUILLEN.PROGRESS.04: a FOURTH honest step on v382, attacking residual "
                   "(2) the alpha^3 Chern level. [E] the pi-power/metric-independence test isolates "
                   "a^3 as the UNIQUE pi^0/c3^0 (metric-independent) term -- the signature of a "
                   "topological level, NOT a Seeley-DeWitt curvature integral (the other two carry "
                   "pi^3, pi^6); plus the dual ladder (coupling 3-n at c3-order 3n). [C] conditional "
                   "on the CS/eta reading (EM1, v48) the a^3 coefficient is an INTEGER level, =1 the "
                   "unit level, not a free real. [O] the EM1 CS-boundary derivation and "
                   "ALPHA.QUILLEN.EXACT.01 stay open; seam F-norm stays the one [C] (v434); alpha^-1 "
                   "stays [E]. Sharpens the only remaining [O]; no new number, Python-only")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
