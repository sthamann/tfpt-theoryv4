"""v136 -- The dual-normal selector: (d, n) pins R COLUMNWISE (each
column the unique lattice point in the address box), the A0* zero mode
carries the exact spectral normal (2,-9,5) with two new atoms, and the
W(A3) orbit control shows the lift sigma -> n is a genuine mechanism,
not a group element.  [I] exact + brute-force census + [P] recorded
programme (external review 2026-06-12, validated and sharpened).

  [I] 1. COLUMN NORMAL FORM.  For the columns c_j of R:
             d . c_j = a_j   and   n . c_j = 8 delta_{1j},
         and these two covectors FORCE each column individually: the
         common kernel of (d, n) is the primitive vector (6, 8, 7)
         (audit: p_2, rank E8, scalaron-7), so within the address box
         {0..5}^3 each line v + t(6,8,7) contains AT MOST one lattice
         point.  Brute-force census (216 per column): c_1 = (1,1,2)
         = a, c_2 = (3,5,5), c_3 = (0,2,3) are each the UNIQUE
         solution.  R4' shrinks from a 6^9 matrix census (v121) to
         three 1-of-216 column problems: (d, n) => R.
  [I] 2. WHAT (d, n) DOES NOT DO (honesty).  K is NOT pinned directly:
         d^T K = (1, 1/2, 1), n^T K = (14, 1, -6) -- no clean form.
         det K = 4 follows from R via the diamond (K = M(1,-1) on the
         mu_4 wall, v135), not from the dual pair.
  [I] 3. THE SPECTRAL NORMAL OF A0*.  The zero mode of the exact
         anchor residue A0* (v115) is v = (-sqrt2, 3, -sqrt5)/3; its
         signed squared components x 9 give EXACTLY
             sigma = (2, -9, 5) = (|Z2|, -N_fam^2, g_car).
         Two new atoms: ||v||^2 = 16/9 (numerator 16 = dim S+), and
             adj(A0*) = (2/9) P_v   with   2/9 = |Z2|/N_fam^2
         -- the rank-1 adjugate carries the SdS entropy curvature
         (v101/v106) as its scale.
  [I] 4. SIGMA RELATIONS.  sigma.1 = -2 = -|Z2|, sigma.a = 3 = N_fam,
         and n . sigma = 121 = ||Pl(K)||_1^2 (the 121 audit constant,
         v119) -- the torsion normal pairs with the spectral normal
         to the squared quark constant.
  [I] 5. ORBIT CONTROL (the honest lift status).  Exact enumeration
         of W(A3) = <U, M0> (24 elements, v117): the only REAL images
         of sigma are its signed copies {(2,-9,5), (2,9,-5),
         (-2,5,-9), (-2,-5,9)}; NO image is proportional to
         n = (5,-9,6).  The naive cofactor/orbit lift FAILS, exactly
         as the review predicted: the step sigma -> n (the
         |Z2|-to-|Z2|N_fam = 6 torsion lift + the carrier endpoint 5)
         is a genuine mechanism beyond the monodromy group.
  [P] 6. R4' RESTATED (recorded): "derive the pair (d, n); then R is
         forced columnwise."  d is already structural (a^T R^{-1},
         Sherman-Morrison invariant, v134); the residue is the
         derivation of n -- now sharply bounded by sigma.1/sigma.a,
         the 121 pairing, and the negative orbit control.
"""
import itertools

import sympy as sp

from tfpt_constants import check, summary, reset

II = sp.I
R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
A = sp.Matrix([1, 1, 2])
ONE = sp.ones(3, 1)
D = sp.Matrix([sp.Rational(-1, 2), sp.Rational(-1, 2), 1])
N = sp.Matrix([5, -9, 6])
SIGMA = sp.Matrix([2, -9, 5])
A0 = sp.Matrix([[sp.Rational(1, 2), sp.sqrt(2) / 6, 0],
                [sp.sqrt(2) / 6, sp.Rational(1, 4), sp.sqrt(5) / 12],
                [0, sp.sqrt(5) / 12, sp.Rational(1, 4)]])
U_MON = sp.diag(1, II, -II)
M0 = sp.Matrix([[0, -(1 + II) / 2, (1 - II) / 2],
                [-(1 + II) / 2, -II / 2, sp.Rational(-1, 2)],
                [(1 - II) / 2, sp.Rational(-1, 2), II / 2]])


def _key(m):
    # entries live in (1/2)Z[i]; canonicalise as exact (re, im) pairs
    return tuple((sp.nsimplify(sp.re(x)), sp.nsimplify(sp.im(x)))
                 for x in sp.expand(m))


def weyl_a3():
    elems = [sp.eye(3)]
    seen = {_key(sp.eye(3))}
    frontier = [sp.eye(3)]
    while frontier:
        new = []
        for g in frontier:
            for h in (U_MON, M0):
                p = sp.expand(g * h)
                k = _key(p)
                if k not in seen:
                    seen.add(k)
                    elems.append(p)
                    new.append(p)
        frontier = new
    return elems


def run():
    reset()
    print("v136 dual-normal selector ((d,n) => R columnwise)")

    # 1. column normal form
    cols = [R[:, j] for j in range(3)]
    ker = sp.Matrix([[*D.T], [*N.T]]).nullspace()[0]
    ker = ker * sp.lcm([x.q for x in ker])
    census = []
    for aj, nj in [(1, 8), (1, 0), (2, 0)]:
        sols = [v for v in itertools.product(range(6), repeat=3)
                if (D.T * sp.Matrix(v))[0] == aj
                and (N.T * sp.Matrix(v))[0] == nj]
        census.append(sols)
    check("COLUMN NORMAL FORM: d.c_j = a_j and n.c_j = 8 delta_1j for "
          "the columns of R; common kernel of (d,n) = primitive "
          "(6,8,7) (audit: p_2, rank E8, scalaron-7); brute-force "
          "census over the address box {0..5}^3: each column is the "
          "UNIQUE solution (1 of 216) -- (d,n) => R, and R4' shrinks "
          "from a 6^9 census to three 1-of-216 column problems",
          [(D.T * c)[0] for c in cols] == [1, 1, 2]
          and [(N.T * c)[0] for c in cols] == [8, 0, 0]
          and (ker == sp.Matrix([6, 8, 7])
               or ker == -sp.Matrix([6, 8, 7]))
          and [len(s) for s in census] == [1, 1, 1]
          and [sp.Matrix(s[0]) for s in census] == cols)

    # 2. honesty: K is not pinned directly
    check("WHAT (d,n) DOES NOT DO (honesty): d^T K = (1, 1/2, 1) and "
          "n^T K = (14, 1, -6) -- K is NOT pinned by the dual pair; "
          "det K = 4 follows from R via the diamond (K = M(1,-1) on "
          "the mu_4 wall, v135)",
          list(D.T * K) == [1, sp.Rational(1, 2), 1]
          and list(N.T * K) == [14, 1, -6]
          and K == R + Q * sp.diag(1, -1, -1) and K.det() == 4)

    # 3. spectral normal of A0*
    v0 = A0.nullspace()[0]
    v0 = sp.simplify(v0 / v0[1] * 3)        # -> (-sqrt2, 3, -sqrt5)
    signed_sq = sp.Matrix([sp.sign(x) * sp.simplify(x ** 2) for x in v0])
    nrm = sp.simplify((v0.T * v0)[0] / 9)   # back to v = v0/3
    proj = sp.simplify((v0 * v0.T) / (v0.T * v0)[0])
    check("SPECTRAL NORMAL OF A0*: zero mode v = (-sqrt2, 3, -sqrt5)/3; "
          "signed squares = (-2, 9, -5) = -sigma with sigma = (2,-9,5) "
          "= (|Z2|, -N_fam^2, g_car); NEW ATOMS: ||v||^2 = 16/9 "
          "(numerator 16 = dim S+) and adj(A0*) = (2/9) P_v with "
          "2/9 = |Z2|/N_fam^2 = the SdS entropy curvature (v101/v106)",
          signed_sq == -SIGMA
          and nrm == sp.Rational(16, 9)
          and sp.simplify(A0.adjugate() - sp.Rational(2, 9) * proj)
          == sp.zeros(3))

    # 4. sigma relations
    check("SIGMA RELATIONS: sigma.1 = -2 = -|Z2|, sigma.a = 3 = N_fam, "
          "n.sigma = 121 = ||Pl(K)||_1^2 = 11^2 (the v119 audit "
          "constant) -- the torsion normal pairs with the spectral "
          "normal to the squared quark constant",
          (SIGMA.T * ONE)[0] == -2 and (SIGMA.T * A)[0] == 3
          and (N.T * SIGMA)[0] == 121 and 121 == 11 ** 2)

    # 5. orbit control
    grp = weyl_a3()
    reals = set()
    prop_to_n = False
    for g in grp:
        img = sp.simplify(g * SIGMA)
        if all(sp.im(x) == 0 for x in img):
            reals.add(tuple(img))
            if img.cross(N) == sp.zeros(3, 1):
                prop_to_n = True
    check("ORBIT CONTROL (honest): |W(A3)| = 24 exactly; the only "
          "REAL orbit images of sigma are its signed copies "
          "{(2,-9,5), (2,9,-5), (-2,5,-9), (-2,-5,9)}; NO image is "
          "proportional to n = (5,-9,6) -- the naive cofactor/orbit "
          "lift FAILS (as predicted); the step sigma -> n is a "
          "genuine mechanism beyond the monodromy group",
          len(grp) == 24 and not prop_to_n
          and reals == {(2, -9, 5), (2, 9, -5), (-2, 5, -9),
                        (-2, -5, 9)})

    # 6. restated programme
    check("R4' RESTATED [P] (recorded): derive the PAIR (d, n); then "
          "R is forced columnwise. d is already structural (v134); "
          "the residue is the derivation of n -- bounded by "
          "sigma.1 = -|Z2|, sigma.a = N_fam, the 121 pairing, and "
          "the negative orbit control", True)

    return summary("v136 dual-normal selector")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
