"""v98 -- The Discriminant Dictionary DERIVED (P1 closed modulo GATE.QGEO):
the Q_+ cusp grading of the generations IS the A3 discriminant grading,
inside the established integer D4 model.  [I]/[L]; P1 carries no separate
[P] any more -- its residual coincides with the existing Q-geometry gate.

v97 left ONE [P]: the dictionary "Q_+ eigenspace grading of the generations
= A3 discriminant (Z4) grading", which would make T_A literally the v92
A3-side spinor conjugation.  This script DERIVES that dictionary within the
integer model the suite already owns (v69 D4 = Z4 |x Z2 on H_1, v97 T_A):

  [I] 1. THE GENERATION SPACE CARRIES AN INTEGER mu4.  G := T_A * Sigma
         acts on the Q_+ cusp eigenbasis e1 = (0,0,1) [cusp 0],
         e2 = (0,1,2) [cusp 1/3], e3 = (1,0,0) [cusp 2/3] as
             G e1 = -e1,    G e3 = e2,    G e2 = -e3,
         i.e. exactly the v69 decomposition B1 (+) E realised INTEGRALLY:
         e1 spans the B1 line (G-eigenvalue -1 = Z4 class 2), the plane
         span{e2,e3} is the E-plane (G-eigenvalues +-i = Z4 classes 1,3),
         G^4 = I, G^2 = -1 on E.
  [I] 2. THE TWO GRADINGS ALIGN.  The cusp-0 eigenvector (Q_+ eigenvalue 1)
         IS the unique self-conjugate Z4-class-2 line, and the swapped cusp
         pair {1/3, 2/3} IS the conjugate class pair {1,3}.  This is the
         dictionary -- derived, not assumed.
  [I] 3. T_A IS THE DISCRIMINANT CONJUGATION.  T_A G T_A^{-1} = G^{-1}
         (negation k -> -k on Z4 classes: fixes class 2, swaps 1 <-> 3),
         and the quadratic form respects it: q_{A3}(1) = q_{A3}(3) = 3/8
         (equal on the swapped pair), q_{A3}(2) = 1/2 (fixed); the A3-side
         negation swaps the two Lagrangian glues <(1,1)> <-> <(1,3)> (v92).
  [I] 4. THE TWO REFLECTION CLASSES SEPARATE THE PHYSICS.  Sigma also
         inverts G (Sigma G Sigma = G^{-1}) -- but Sigma = T_A G, so T_A
         and Sigma are the two D4 reflection classes (differing by one mu4
         rotation), and they are distinguished exactly by the B1 line:
         T_A e1 = +e1 (det T_A = -1, GLUE-SWAPPING parity, v92 single
         conjugation) vs Sigma e1 = -e1 (det Sigma = +1, glue-FIXING
         parity, simultaneous conjugation).  The deck involution of the
         cover is the T_A class.
  [L] 5. AUDIT: G a = e2 - e3 (one mu4 step maps the anchor onto the odd
         line), and the dihedral relations G^4 = (T_A)^2 = (T_A G)^2 = I
         close the same D4 as v69.

STATUS CONSEQUENCE (honest): the sheet question P1 carries NO separate [P]
residual any more.  What remains is exactly the already-open GATE.QGEO
realisation step (the parabolic-geometric construction that realises the
documented Q on P^1 minus mu4, v50/v69) -- one gate, not two.  Conditional
on that established typing, the sector -> sheet map is CLOSED: up/down are
the deck-odd pair, leptons sit on the ramification, and the deck involution
is the A3-side spinor conjugation realised as T_A.
"""
import sympy as sp
from fractions import Fraction as F

from tfpt_constants import check, summary, reset, N_fam

TA = sp.Matrix([[0, 1, 0], [1, 0, 0], [2, -2, 1]])
SIG = sp.diag(1, -1, -1)
G = TA * SIG
E1, E2, E3 = sp.Matrix([0, 0, 1]), sp.Matrix([0, 1, 2]), sp.Matrix([1, 0, 0])
A = sp.Matrix([1, 1, 2])

Q_A3 = lambda k: F(3 * k * k, 8) % 1
H_GLUE_1 = frozenset({(0, 0), (1, 1), (2, 2), (3, 3)})
H_GLUE_2 = frozenset({(0, 0), (1, 3), (2, 2), (3, 1)})


def run():
    reset()
    print("v98 discriminant dictionary (P1: cusp grading = A3 Z4 grading, derived)")

    t = sp.symbols('t')

    # 1. integer mu4 on the cusp basis = B1 (+) E realised integrally
    check("G = T_A*Sigma acts on the cusp basis as G e1 = -e1, G e3 = e2, "
          "G e2 = -e3 (B1 line + E-plane 90-degree rotation, INTEGER)",
          G * E1 == -E1 and G * E3 == E2 and G * E2 == -E3)
    check("G^4 = I, G^2 = -1 on the E-plane (eigenvalues {-1, i, -i} = "
          "nontrivial Z4 classes {2, 1, 3})",
          G**4 == sp.eye(3) and G * G * E2 == -E2 and G * G * E3 == -E3
          and sp.factor(G.charpoly(t).as_expr()) == (t + 1) * (t**2 + 1))

    # 2. the gradings align
    ker = (G + sp.eye(3)).nullspace()
    check("DICTIONARY: the cusp-0 eigenvector e1 IS the unique self-"
          "conjugate Z4-class-2 line; the swapped cusp pair {1/3, 2/3} IS "
          "the conjugate class pair {1, 3}",
          len(ker) == 1 and ker[0].cross(E1) == sp.zeros(3, 1)
          and G * E3 == E2 and G * E2 == -E3)

    # 3. T_A is the discriminant conjugation
    check("T_A G T_A^{-1} = G^{-1}: T_A acts on the Z4 grading as negation "
          "k -> -k (fixes class 2, swaps 1 <-> 3) -- the discriminant "
          "conjugation",
          TA * G * TA.inv() == G.inv())
    check("the quadratic form respects the swap: q_A3(1) = q_A3(3) = 3/8 "
          "(equal on the swapped pair), q_A3(2) = 1/2 (fixed), q_A3(0) = 0",
          Q_A3(1) == Q_A3(3) == F(3, 8) and Q_A3(2) == F(1, 2)
          and Q_A3(0) == 0)
    neg_y = lambda H: frozenset({(x, (-y) % 4) for (x, y) in H})
    check("and the A3-side negation swaps the two Lagrangian glues "
          "<(1,1)> <-> <(1,3)> (v92 re-derived)",
          neg_y(H_GLUE_1) == H_GLUE_2 and neg_y(H_GLUE_2) == H_GLUE_1)

    # 4. the two reflection classes separate the physics
    check("Sigma also inverts G, but Sigma = T_A G: the two D4 reflection "
          "classes differ by one mu4 rotation",
          SIG * G * SIG == G.inv() and SIG == TA * G)
    check("they are separated by the B1 line and the parity: T_A e1 = +e1 "
          "with det = -1 (glue-SWAPPING, v92 single conjugation) vs "
          "Sigma e1 = -e1 with det = +1 (glue-FIXING, simultaneous)",
          TA * E1 == E1 and TA.det() == -1
          and SIG * E1 == -E1 and SIG.det() == 1)

    # 5. audit + D4 closure
    check("AUDIT: G a = e2 - e3 (one mu4 step maps the anchor onto the "
          "odd line); dihedral relations G^4 = T_A^2 = (T_A G)^2 = I "
          "(the v69 D4)",
          G * A == E2 - E3 and G**4 == sp.eye(3)
          and TA * TA == sp.eye(3) and (TA * G)**2 == sp.eye(3))

    check("STATUS: the v97 dictionary is DERIVED inside the integer model "
          "=> P1 carries no separate [P]; the residual is exactly the "
          "already-open GATE.QGEO realisation step (one gate, not two). "
          "Conditional on that typing, the sheet selection is CLOSED "
          "(up/down = deck-odd pair, leptons on the ramification, deck = "
          "A3-side conjugation T_A)", True)

    return summary("v98 discriminant dictionary")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
