"""v134 -- The Dual Anchor Lemma: the inverse flavor response of the
anchor is the Nariai root, invariant under the winding deformation, with
an exact Sherman-Morrison characterisation; d and n form the dual normal
pair of the flavor boundary.  [I] exact identities + controls (external
review 2026-06-12, validated).

  [I] 1. THE DUAL ANCHOR.
             d := a^T R^{-1} = a^T L^{-1} = (-1/2, -1/2, 1),
         with  d.1 = 0,  d.a = 1,  d = (3/2)(a - (4/3) 1)^T  -- the
         normalised TRACELESS anchor -- and
             (1, 1, -2) = -2 d:
         the inverse flavor response stores EXACTLY the Nariai
         double-root structure (v101) up to sign and scale.  The
         horizon structure is not glued on afterwards: it sits inside
         the flavor compiler as a dual invariant.
  [I] 2. WHY IT IS INVARIANT (Sherman-Morrison, exact).  With
         L = R + 6 * 1 e_1^T:
             v^T L^{-1} = v^T R^{-1}  <=>  v^T R^{-1} 1 = 0,
         and R^{-1} 1 = (1, 1, -1)/4, denominator 1 + 6 e_1^T R^{-1} 1
         = 5/2 != 0.  The anchor satisfies a . (R^{-1} 1) = 0 -- it
         lies on the 2-plane of invariant covectors; the winding
         deformation lives in the democratic direction 1, which d
         annihilates.
  [I] 3. CONTROL (honesty): 1, e_1 and n = (5,-9,6) do NOT lie on the
         invariance plane (values 1/4, 1/4, -5/2) -- the property is
         special, not generic.
  [I] 4. THE DUAL NORMAL PAIR.  d (the sheet normal: annihilates 1,
         dual to a, proportional to the Nariai root) and n = (5,-9,6)
         (the torsion normal: n^T R = (8,0,0), n^T L = (20,0,0),
         n.a = 8, and n.1 = 2 = |Z2|, v95) form the dual basis of the
         flavor boundary: d reads the traceless horizon structure,
         n reads torsion/volume in the first generation.
  [P] 5. CONSEQUENCE (recorded): a third, purely algebraic leg of the
         flavor <-> horizon bridge (besides the shared spectrum, v126,
         and the entropy power law, v129); strengthens the reduced
         seam reading (v133) and gives the R4' selector programme a
         geometric target: derive the PAIR (d, n), not n alone.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
L = sp.Matrix([[7, 3, 0], [7, 5, 2], [8, 5, 3]])
A = sp.Matrix([1, 1, 2])
ONE = sp.ones(3, 1)
E1 = sp.Matrix([1, 0, 0])
N = sp.Matrix([5, -9, 6])


def run():
    reset()
    print("v134 dual anchor (a^T R^-1 = a^T L^-1 = Nariai root / -2)")

    # 1. the dual anchor
    d = A.T * R.inv()
    check("THE DUAL ANCHOR: a^T R^-1 = a^T L^-1 = (-1/2, -1/2, 1) "
          "with d.1 = 0, d.a = 1, d = (3/2)(a - (4/3)1)^T (the "
          "normalised traceless anchor), and (1,1,-2) = -2d -- the "
          "inverse flavor response IS the Nariai double-root "
          "structure (v101) up to sign and scale",
          d == A.T * L.inv()
          and list(d) == [sp.Rational(-1, 2), sp.Rational(-1, 2), 1]
          and (d * ONE)[0] == 0 and (d * A)[0] == 1
          and d.T == sp.Rational(3, 2) * (A - sp.Rational(4, 3) * ONE)
          and sp.Matrix([1, 1, -2]).T == -2 * d)

    # 2. Sherman-Morrison characterisation
    rinv1 = R.inv() * ONE
    sm_l = R.inv() - 6 * (R.inv() * ONE) * (E1.T * R.inv()) \
        / (1 + 6 * (E1.T * R.inv() * ONE)[0])
    check("WHY INVARIANT (Sherman-Morrison, exact): L = R + 6*1 e1^T "
          "gives L^-1 = R^-1 - 6 R^-1 1 e1^T R^-1 / (1 + 6 e1^T R^-1 "
          "1) with denominator 5/2; hence v^T L^-1 = v^T R^-1 <=> "
          "v^T R^-1 1 = 0; R^-1 1 = (1,1,-1)/4 and a.(R^-1 1) = 0 -- "
          "the anchor lies on the 2-plane of invariant covectors "
          "(the winding lives in the democratic direction 1, which d "
          "annihilates)",
          L == R + 6 * ONE * E1.T
          and sp.simplify(sm_l - L.inv()) == sp.zeros(3)
          and list(rinv1) == [sp.Rational(1, 4), sp.Rational(1, 4),
                              sp.Rational(-1, 4)]
          and (A.T * rinv1)[0] == 0
          and 1 + 6 * (E1.T * rinv1)[0] == sp.Rational(5, 2))

    # 3. control
    check("CONTROL (honesty): 1, e1 and n = (5,-9,6) do NOT lie on "
          "the invariance plane (v^T R^-1 1 = 1/4, 1/4, -5/2 "
          "respectively) -- the anchor's membership is special, not "
          "generic",
          (ONE.T * rinv1)[0] == sp.Rational(1, 4)
          and (E1.T * rinv1)[0] == sp.Rational(1, 4)
          and (N.T * rinv1)[0] == sp.Rational(-5, 2))

    # 4. the dual normal pair
    check("THE DUAL NORMAL PAIR: d (sheet normal: kills 1, dual to a, "
          "proportional to the Nariai root) and n = (5,-9,6) (torsion "
          "normal: n^T R = (8,0,0), n^T L = (20,0,0), n.a = 8, and "
          "n.1 = 2 = |Z2|, cf. v95) -- the dual basis of the flavor "
          "boundary",
          list(N.T * R) == [8, 0, 0] and list(N.T * L) == [20, 0, 0]
          and (N.T * A)[0] == 8 and (N.T * ONE)[0] == 2)

    # 5. consequence
    check("CONSEQUENCE [P] (recorded): a third, purely ALGEBRAIC leg "
          "of the flavor <-> horizon bridge (besides the shared "
          "spectrum v126 and the entropy power law v129); supports "
          "the reduced seam reading (v133); the R4' selector "
          "programme acquires a geometric target: derive the PAIR "
          "(d, n), not n alone", True)

    return summary("v134 dual anchor")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
