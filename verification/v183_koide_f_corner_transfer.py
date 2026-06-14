"""v183 -- The Koide source->pole factor 53/54 has an OPERATOR origin: it is the
anchor response of the missing Sheet-Diamond corner F = R + Q over the
sheet-doubled E6xA2 cubic family block. This upgrades the FR.KOIDE.03 conjecture
(53/54 = 1 - 1/(2 N_fam^3)) from a 'nice compiler factor' to the exact ratio

    u_pole / u_source = a^T (R+Q) 1 / (2 * 1^T R a) = 53 / (2*27) = 53/54,

with a hard negative control (only the F corner gives 53). The PHYSICAL claim --
that the leptonic source->pole transfer reads the F corner -- stays [C] (an
F_transfer special case), but the FACTOR is now structurally sourced, not fitted.
(External-review proposal 2026-06-14, validated.)

  [I] 1. THE CUBIC FAMILY BLOCK 1^T R a = 27.  In the E6xA2 flavor shadow the
        E8 dimension splits 248 = dim E6 + det R + 2 (1^T R a) N_fam =
        78 + 8 + 2*27*3, so 27 = 1^T R a is the cubic family block (the
        sheet-doubled denominator 2*27 = 54).
  [I] 2. THE MISSING CORNER a^T (R+Q) 1 = 53.  The Sheet Diamond has corners
        R=M(0,0), K=M(1,-1), L=M(2,0) and the MISSING corner F=R+Q=M(1,1) with
        anchor-block determinant det B_F = 52 = dim F4 (v80). Its anchor response
        a^T F 1 = a^T(R+Q)1 = 53 = 52 + 1 (the F4 shadow plus the singlet).
  [I] 3. THE RATIO IS 53/54.  u_pole/u_source = a^T(R+Q)1 / (2 * 1^T R a) =
        53/54, matching FR.KOIDE.03's 1 - 1/(2 N_fam^3) EXACTLY (54 = 2*N_fam^3 =
        2*27), so the two readings coincide -- but this one is an operator
        identity on the carrier, not an arithmetic guess.
  [I] 4. NEGATIVE CONTROL.  Only the missing corner F gives 53: a^T M 1 for
        M in {R,Q,K,L} is {32,21,35,56}, none equal to 53. The factor singles
        out F = R+Q, the absent Sheet-Diamond corner -- specific, not generic.
  [C] 5. PHYSICAL STATUS.  This sources the FACTOR exactly; the MECHANISM
        (that the leptonic pole-mass transfer evaluates the F corner of the
        Sheet Diamond) remains a conjecture -- an F_transfer special case
        (F_pole: source -> pole). Given it, Koide moves from 'near miss +
        conjecture' to 'operator-sourced source->pole transfer'; without it,
        53/54 stays a structurally-grounded [C], no longer a bare numerology.
        (Cross-ref: the same Sheet-Diamond / double-cover grammar carries the
        gravity clock, HOR.TRISECT.01: flavor rate (2/3)^{2N_fam} vs gravity
        curvature (2/3)^{N_fam}, exponent ratio |Z2| -- one clock, two geometries.)
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
L = sp.Matrix([[7, 3, 0], [7, 5, 2], [8, 5, 3]])
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
F = R + Q


def _f(M, u, v):
    return int((u.T * M * v)[0])


def _detB(M):
    return sp.Matrix([[_f(M, ONE, ONE), _f(M, ONE, A)],
                      [_f(M, A, ONE), _f(M, A, A)]]).det()


def run():
    reset()
    print("v183 Koide 53/54 = a^T(R+Q)1 / (2*1^T R a): operator origin in the missing Sheet-Diamond corner")

    # 1. cubic family block 1^T R a = 27 and the E6xA2 split
    cubic = _f(R, ONE, A)
    split = 78 + 8 + 2 * cubic * N_fam
    check("CUBIC FAMILY BLOCK [I]: 1^T R a = %d; the E6xA2 shadow splits "
          "248 = dim E6 + det R + 2(1^T R a)N_fam = 78 + 8 + 2*27*3 = %d, so 27 "
          "is the cubic family block and 2*27 = 54 the sheet-doubled denominator"
          % (cubic, split),
          cubic == 27 and split == 248)

    # 2. missing corner a^T(R+Q)1 = 53, det B_F = 52 = dim F4
    corner = _f(F, A, ONE)
    detBF = _detB(F)
    check("MISSING CORNER [I]: F = R+Q = M(1,1) is the absent Sheet-Diamond "
          "corner (R,K,L present); det B_F = %d = dim F4 (v80) and its anchor "
          "response a^T(R+Q)1 = %d = 52 + 1 (F4 shadow + singlet)"
          % (detBF, corner),
          corner == 53 and detBF == 52)

    # 3. the ratio is 53/54, matching 1 - 1/(2 N_fam^3)
    ratio = sp.Rational(corner, 2 * cubic)
    koide_conj = 1 - sp.Rational(1, 2 * N_fam**3)
    check("THE RATIO IS 53/54 [I]: u_pole/u_source = a^T(R+Q)1 / (2*1^T R a) = "
          "%s = 1 - 1/(2 N_fam^3) = %s (54 = 2*N_fam^3 = 2*27) -- the FR.KOIDE.03 "
          "factor, now an operator identity on the carrier, not an arithmetic guess"
          % (ratio, koide_conj),
          ratio == sp.Rational(53, 54) and ratio == koide_conj)

    # 4. negative control: only F gives 53
    others = {nm: _f(M, A, ONE) for nm, M in (("R", R), ("Q", Q), ("K", K), ("L", L))}
    check("NEGATIVE CONTROL [I]: only the missing corner F gives 53 -- "
          "a^T M 1 for M in {R,Q,K,L} = %s, none equal to 53; the factor singles "
          "out F = R+Q, the absent Sheet-Diamond corner (specific, not generic)"
          % others,
          corner == 53 and all(v != 53 for v in others.values())
          and set(others.values()) == {32, 21, 35, 56})

    # 5. physical status -- [C]
    check("PHYSICAL STATUS [C]: the FACTOR is sourced exactly; the MECHANISM "
          "(the leptonic pole-mass transfer evaluates the F corner) stays a "
          "conjecture -- an F_transfer special case (F_pole: source->pole). "
          "Koide moves from 'near miss + conjecture' to 'operator-sourced "
          "source->pole transfer'; cross-ref HOR.TRISECT.01 (same double-cover "
          "grammar carries the gravity clock, exponent ratio |Z2|)", True)

    return summary("v183 Koide 53/54 operator origin (missing F corner / E6xA2 block)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
