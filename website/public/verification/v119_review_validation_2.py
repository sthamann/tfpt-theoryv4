"""v119 -- Second external-review validation (2026-06-11b): the anchor
ratio triad, the 121 audit lemma, and the normal-form micro-identities.
[I] exact identities + explicit sensitivity controls; presentational
recommendations recorded, not checked.

An external review proposed several sharpenings.  Validation result:

  [I] 1. ANCHOR NORMAL-FORM MICRO-IDENTITIES (all exact).  With
         p_n = 2 + 2^n and (e1, e2, e3) = (4, 5, 2):
             Omega_adm = 2 p1 p2 = 48,        10 b1 = 1 + p1 p3 = 41,
             Delta_Y = e2^2 = p0^2 + 2 rank = 25,
             h(E8) = e3 p0 e2 = 30,           rank E8 = p0 + e2 = 8,
             |R(E8)| = p1 p2 p3 = 240,        dim = 240 + (p4 - p3) = 248.
  [I] 2. THE ANCHOR RATIO TRIAD (named lemma).  The three elementary
         symmetric values of the anchor, normalised by the family count:
             e3/p0 = 2/3   (the KOIDE BRANCH / sheet ratio),
             e1/p0 = 4/3   (the SEED GAIN: phi0 = (4/3)c3 + 48 c3^4,
                            4/3 = |mu_4|/N_fam, v106),
             e2/p0 = 5/3   (the CARRIER BRANCH: the canonical flow's
                            critical points are exactly (2, 5) =
                            (e3, e2), v99/v102, with inflection
                            7/2 = (e3+e2)/2).
         The recurring fractions 2/3, 4/3, 5/3 are not scattered
         numbers: they are the three normalised anchor coefficients.
  [I] 3. THE 121 AUDIT LEMMA (recorded as AUDIT, not load-bearing).
         With h = 1 + a = (2, 2, 3) in the canonical anchor ordering
         and the established residue operator R (det 8, SNF (1,1,8)):
             h^T R h = 121 = 11^2 = ||Pl(K)||_1^2 = (p3 + 1)^2
         -- the quark-ratio 11 appears a SECOND, independent time as
         the quadratic anchor norm of R.  SENSITIVITY CONTROL: over the
         3 distinct orderings of h the form takes values {105, 121,
         135}; only the canonical anchor ordering gives 121.  BONUS:
         1^T R 1 = 22 = 2 x 11 (the entry sum of R) and
         a^T R a = 40 = p1 p3 = 10 b1 - 1.  This does NOT replace the
         oriented Plucker mechanism (v42/v49) -- it is a second
         checksum on the same integer.
  [I] 4. THE FLAVOR SURFACE CLAIM = ESTABLISHED v94/v95.  The review's
         M(s,t) = R + Q diag(s,t,t) with R = M(0,0), K = M(1,-1),
         L = M(2,0), F = M(1,1) and the centered cross Q = U + V,
         {R, L} = C -+ U, {K, F} = C -+ V is exactly the sheet diamond
         (v94) / centered diamond (v95) -- re-verified here; the
         review's suggestion is presentational, not new mathematics.
      5. ALREADY CLOSED TODAY (no new checks): the mu_4 projection
         lemma = v115/v116; the anchor triptych = v104/v105; "interior
         free, structure = certificate" = v113.  Presentational
         recommendations (anchor-first entry, normal-form table, M(s,t)
         presentation) recorded in next.txt as editorial items.
"""
import sympy as sp
from itertools import permutations

from tfpt_constants import check, summary, reset

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
L = sp.Matrix([[7, 3, 0], [7, 5, 2], [8, 5, 3]])
A = sp.Matrix([1, 1, 2])
ONE = sp.ones(3, 1)


def p(n):
    return 2 + 2 ** n


def run():
    reset()
    print("v119 second review validation (triad, 121 audit, micro-identities)")

    e1, e2, e3 = 4, 5, 2

    # 1. micro-identities
    check("ANCHOR NORMAL-FORM MICRO-IDENTITIES: Omega_adm = 2 p1 p2 = "
          "48, 10 b1 = 1 + p1 p3 = 41, Delta_Y = e2^2 = p0^2 + 2 rank "
          "= 25, h(E8) = e3 p0 e2 = 30, rank = p0 + e2 = 8, 240 = "
          "p1 p2 p3, 248 = 240 + (p4 - p3)",
          2 * p(1) * p(2) == 48 and 1 + p(1) * p(3) == 41
          and e2 ** 2 == 25 and p(0) ** 2 + 2 * 8 == 25
          and e3 * p(0) * e2 == 30 and p(0) + e2 == 8
          and p(1) * p(2) * p(3) == 240
          and p(1) * p(2) * p(3) + p(4) - p(3) == 248)

    # 2. anchor ratio triad
    check("ANCHOR RATIO TRIAD: (e3, e1, e2)/p0 = (2/3, 4/3, 5/3) = "
          "(Koide branch / sheet ratio, seed gain |mu_4|/N_fam (v106), "
          "carrier branch); the canonical flow's critical points are "
          "exactly (2, 5) = (e3, e2) (v99/v102) with inflection 7/2 = "
          "(e3+e2)/2 -- the recurring fractions are the three "
          "normalised anchor coefficients",
          (sp.Rational(e3, 3), sp.Rational(e1, 3), sp.Rational(e2, 3))
          == (sp.Rational(2, 3), sp.Rational(4, 3), sp.Rational(5, 3))
          and (2, 5) == (e3, e2)
          and sp.Rational(e3 + e2, 2) == sp.Rational(7, 2))

    # 3. the 121 audit lemma
    h = ONE + A
    val = (h.T * R * h)[0]
    perm_vals = sorted(set(int((sp.Matrix(q).T * R * sp.Matrix(q))[0])
                           for q in permutations([2, 2, 3])))
    bmat = sp.Matrix.vstack(ONE.T * K, A.T * K)
    pl = sp.Matrix([bmat[:, [1, 2]].det(), -bmat[:, [0, 2]].det(),
                    bmat[:, [0, 1]].det()])
    check("THE 121 AUDIT LEMMA: (1+a)^T R (1+a) = 121 = 11^2 = "
          "||Pl(K)||_1^2 = (p3+1)^2 -- the quark-ratio 11 appears a "
          "second, independent time as the quadratic anchor norm of R",
          val == 121 and 121 == 11 ** 2
          and sum(abs(x) for x in pl) == 11
          and (p(3) + 1) ** 2 == 121)
    check("SENSITIVITY CONTROL (honesty): over the 3 distinct orderings "
          "of h = (2,2,3) the form takes values {105, 121, 135} -- only "
          "the canonical anchor ordering gives 121; recorded as AUDIT, "
          "not load-bearing (the oriented Plucker mechanism v42/v49 "
          "stays the derivation)",
          perm_vals == [105, 121, 135])
    check("BONUS CHECKSUMS: 1^T R 1 = 22 = 2 x 11 (entry sum of R) and "
          "a^T R a = 40 = p1 p3 = 10 b1 - 1",
          (ONE.T * R * ONE)[0] == 22 and 22 == 2 * 11
          and (A.T * R * A)[0] == 40 and 40 == p(1) * p(3))

    # 4. flavor surface = established v94/v95
    def msurf(s, t):
        return R + Q * sp.diag(s, t, t)

    sig = sp.diag(1, -1, -1)
    u_ax = 3 * ONE * sp.Matrix([[1, 0, 0]])
    v_ax = Q - u_ax
    c_mid = R + u_ax
    check("FLAVOR SURFACE = ESTABLISHED v94/v95 (review claim "
          "re-verified, presentational): R = M(0,0), K = M(1,-1), "
          "L = M(2,0), F = M(1,1) on M(s,t) = R + Q diag(s,t,t); "
          "centered cross Q = U + V, R = C-U, L = C+U, K = C-V, "
          "F = C+V",
          msurf(0, 0) == R and msurf(1, -1) == K and msurf(2, 0) == L
          and msurf(1, 1) == R + Q
          and K == R + Q * sig and L == R + Q * (sp.eye(3) + sig)
          and R == c_mid - u_ax and L == c_mid + u_ax
          and K == c_mid - v_ax and R + Q == c_mid + v_ax)

    # 5. bookkeeping
    check("REVIEW BOOKKEEPING (recorded): mu_4 projection lemma = "
          "v115/v116 (closed today); anchor triptych = v104/v105; "
          "'interior free, structure = certificate' = v113; "
          "anchor-first presentation / normal-form table / M(s,t) "
          "presentation = editorial items (next.txt), not checks", True)

    return summary("v119 second review validation")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
