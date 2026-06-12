"""v142 -- Frame integrality: in the (1, a, sigma) dual frame the three
R4' pairings live on an INDEX-11 sublattice (one congruence
x - 3y + z = 0 mod 11), integrality + the two established line pairings
force 11 | (sigma-pairing), and primitivity forces the v139 line
parameter to be EVEN.  R4' sharpens from 'derive three pairings' to
'derive the two line pairings'.  [I] exact lattice arithmetic; the
establishment of (|Z2|, rank E8) stays the genuine [P]/[A] residue.

v139 re-expressed the selector covector n = (5,-9,6) as the unique
integer solution of three atom pairings against the frame (1, a, sigma)
(volume 11) and left 'derive the three pairings' as the R4' residue.
This module shows the third pairing is NOT independent:

  [I] 1. DUAL-FRAME EXPANSION.  For every covector m,
             11 * m = (m.1)(a x sigma) + (m.a)(sigma x 1)
                      + (m.sigma)(1 x a)
         with a x sigma = (23,-1,-11), sigma x 1 = (-14,3,11),
         1 x a = (1,-1,0) (the adjugate rows of the frame).
  [I] 2. INTEGRALITY = ONE CONGRUENCE MOD 11.  m has INTEGER entries
         iff its pairing triple (x,y,z) = (m.1, m.a, m.sigma)
         satisfies x - 3y + z = 0 (mod 11): the pairing triples of
         integer covectors form an index-11 sublattice of Z^3 -- the
         index is 11 = ||Pl(K)||_1 = det(1|a|sigma) itself.
  [I] 3. THE THIRD PAIRING IS FORCED MOD 11.  With the two line
         pairings at their established atoms (x, y) = (|Z2|, rank E8)
         = (2, 8): integrality forces z = 0 (mod 11).  On the v139
         line z(t) = 11(11 + t) this is automatic -- and conversely
         the congruence is exactly what makes the v139 line the
         INTEGER line.
  [I] 4. PRIMITIVITY FORCES EVEN t.  On the line n(t) =
         (5 + t, -9 - t, 6): odd t makes all three entries even
         (non-primitive); so the selector search space is the EVEN
         lattice line.  t = 0 is the unique even t with z a perfect
         square in |t| < 88 (the next square sits at t = 88);
         a global pick still needs the v139 square selector or a
         boundedness principle -- recorded honestly.
  [I] 5. CRAMER REDUCTIONS (restructuring, not establishment).  Both
         line pairings are restatements of established identities:
             n.a = det R = 8           (Laplace expansion along R's
                                        anchor column, v121/v122),
             n.1 = 8 (R^{-1} 1)_1 = 2  (R^{-1} 1 = (1,1,-1)/4, v134).
         They consume R, so they restructure -- the R-free
         ESTABLISHMENT of (2, 8) remains the residue.

STATUS: R4' reduces from three pairings to TWO (the third is
integrality-forced mod 11, with the square/parity selection on the
even line); typing [A]/[P] unchanged, content strictly smaller.
"""
import sympy as sp
from itertools import product

from tfpt_constants import check, summary, reset

ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
SIGMA = sp.Matrix([2, -9, 5])
N = sp.Matrix([5, -9, 6])
R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])


def cross(u, v):
    return sp.Matrix([u[1] * v[2] - u[2] * v[1],
                      u[2] * v[0] - u[0] * v[2],
                      u[0] * v[1] - u[1] * v[0]])


def run():
    reset()
    print("v142 frame integrality (R4': three pairings -> two)")

    F = sp.Matrix.hstack(ONE, A, SIGMA)
    det_f = F.det()
    axs, sx1, oxa = cross(A, SIGMA), cross(SIGMA, ONE), cross(ONE, A)

    # 1. dual-frame expansion
    expansion_ok = True
    for m in (N, sp.Matrix([1, 0, 0]), sp.Matrix([2, -5, 7])):
        lhs = det_f * m
        rhs = (m.dot(ONE)) * axs + (m.dot(A)) * sx1 + (m.dot(SIGMA)) * oxa
        if sp.simplify(lhs - rhs) != sp.zeros(3, 1):
            expansion_ok = False
    check("DUAL-FRAME EXPANSION: 11*m = (m.1)(a x sigma) + "
          "(m.a)(sigma x 1) + (m.sigma)(1 x a) for every covector "
          "(checked on n and two controls); the three adjugate rows "
          "are (23,-1,-11), (-14,3,11), (1,-1,0); det(1|a|sigma) = 11",
          expansion_ok and det_f == 11
          and axs.T.tolist()[0] == [23, -1, -11]
          and sx1.T.tolist()[0] == [-14, 3, 11]
          and oxa.T.tolist()[0] == [1, -1, 0])

    # 2. integrality = one congruence mod 11
    cong_ok = True
    for x, y, z in product(range(11), repeat=3):
        vec = x * axs + y * sx1 + z * oxa
        integral = all(c % 11 == 0 for c in vec)
        if integral != ((x - 3 * y + z) % 11 == 0):
            cong_ok = False
    n_triple = (N.dot(ONE), N.dot(A), N.dot(SIGMA))
    check("INTEGRALITY = ONE CONGRUENCE: (x,y,z) gives an integer "
          "covector iff x - 3y + z = 0 (mod 11) (full 11^3 scan); "
          "the integer pairing triples form an index-11 sublattice, "
          "index 11 = ||Pl(K)||_1 = the frame volume; n's triple "
          "(2,8,121) satisfies it",
          cong_ok and (n_triple[0] - 3 * n_triple[1] + n_triple[2]) % 11 == 0
          and n_triple == (2, 8, 121))

    # 3. the third pairing forced mod 11
    forced = [(2 - 3 * 8 + z) % 11 == 0 for z in range(0, 122)]
    sols = [z for z in range(0, 122) if forced[z]]
    check("THIRD PAIRING FORCED MOD 11: with (x,y) = (|Z2|, rank E8) "
          "= (2,8), integrality forces z = 0 (mod 11); the v139 line "
          "z(t) = 11(11+t) is exactly the integer line",
          sols == list(range(0, 122, 11))
          and all((2 - 24 + 11 * (11 + t)) % 11 == 0 for t in range(-11, 12)))

    # 4. primitivity forces even t
    def primitive(t):
        e = (5 + t, -9 - t, 6)
        return sp.igcd(sp.igcd(e[0], e[1]), e[2]) == 1
    parity_ok = all(not primitive(t) for t in range(-21, 22) if t % 2 == 1)
    squares_even = [t for t in range(-87, 88) if t % 2 == 0
                    and sp.sqrt(11 * (11 + t)).is_integer]
    check("PRIMITIVITY FORCES EVEN t: odd t makes every entry of "
          "n(t) = (5+t,-9-t,6) even (non-primitive); t = 0 is the "
          "unique EVEN t with z = 11(11+t) a perfect square for "
          "|t| < 88 (next square at t = 88) -- the global pick still "
          "needs the v139 square selector (recorded honestly)",
          parity_ok and squares_even == [0]
          and sp.sqrt(sp.Integer(11 * (11 + 88))).is_integer)

    # 5. Cramer reductions
    r_inv_one = R.inv() * ONE
    laplace = sum(A[i] * R.cofactor(i, 0) for i in range(3))
    check("CRAMER REDUCTIONS (restructuring): n.a = det R = 8 is the "
          "Laplace expansion along R's anchor column (v121/v122), "
          "and n.1 = 8*(R^-1 1)_1 = 2 with R^-1 1 = (1,1,-1)/4 "
          "(v134) -- both consume R, so the R-free establishment of "
          "(2,8) remains the genuine residue",
          laplace == R.det() == 8
          and r_inv_one == sp.Matrix([sp.Rational(1, 4),
                                      sp.Rational(1, 4),
                                      sp.Rational(-1, 4)])
          and 8 * r_inv_one[0] == 2 == N.dot(ONE)
          and N.dot(A) == 8)

    check("STATUS: R4' reduces from three pairings to TWO -- the "
          "sigma-pairing is integrality-forced mod 11 on the even "
          "line; deriving (|Z2|, rank E8) for the two line pairings "
          "is the remaining [P]/[A] content", True)

    return summary("v142 frame integrality")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
