"""v415 -- The square CM-norm dictionary is operator-realised, and the mu4 deck
is an intrinsic diamond object.  The Gaussian arithmetic of v222/v230 (the
square seam: 13 = N_Z[i](3+2i) = Delta_Q, 41 = N_Z[i](5+4i) = 10 b1) is lifted
from NUMBERS to OPERATORS via the single complex structure born from the
commutator of the binary (V) and ternary (U) compilers (v410/v95).  [E] algebra,
[C] the geometric-deck identification (v140 residue, sharpened not closed).

  [E] 1. THE OPERATOR 'i'.  With U = Q diag(1,0,0) (winding, Spec {3,0,0}) and
         V = Q diag(0,1,1) (sheet, Spec {0,1,2}) the integer matrix
             J := [U,V]/3 = [[-1,1,0],[-2,1,0],[-3,1,0]]
         has Spec(J) = {i, -i, 0}, J^2 = -I on the rank-2 image and J^3 + J = 0
         (order 4 on the plane) -- a genuine mu4 quarter-turn complex structure,
         born from the non-commutativity of the two internal compilers.
  [E] 2. THE GAUSSIAN INTEGERS ARE EIGENVALUES.  3I + 2J has spectrum
         {3+2i, 3-2i, 3} and 5I + 4J has {5+4i, 5-4i, 5}: the abstract Gaussian
         integers 3+2i (norm 13 = Delta_Q) and 5+4i (norm 41 = 10 b1) are LITERAL
         eigenvalues of concrete diamond operators -- lifting v222/v230 from norm
         to spectrum.
  [E] 3. THE NORM DICTIONARY AS OPERATOR IDENTITIES.
             (3I+2J)(3I-2J) = 9I - 4J^2,  Spec = {13, 13, 9},
             (5I+4J)(5I-4J) = 25I - 16J^2, Spec = {41, 41, 25};
         on the mu4-plane these are 13*I = Delta_Q and 41*I = 10 b1, while the
         kernel slot reads the real part squared (9 = N_fam^2, 25 = g_car^2).
  [E] 4. THE INTRINSIC mu4 DECK.  Pi2 := I + J^2 is the projector onto ker J
         (the self-conjugate chi2 line), and
             D := J - Pi2 = -I + J - J^2 = [[-1,1,0],[-2,1,0],[-4,3,-1]]
         is a genuine order-4 deck: D^4 = I, chi_D = (x+1)(x^2+1), Spec(D) =
         {i, -1, -i} (the seam-deck spectrum of v146).  The diamond canonically
         singles out the self-conjugate line as
             ker[U,V] = (0,0,1) = a - 1 = the V-fixed line (Spec-1 eigenvector).
  [C] 5. DECK IDENTIFICATION (v140 residue, SHARPENED not closed).  D has the
         same characteristic polynomial as the geometric seam deck delta (v146,
         z->iz on H^1), and the diamond fixes the chi2 line internally as a-1.
         Whether a-1 is the GEOMETRIC self-conjugate line is exactly the one
         Z_3 family-rotation residue of v140 -- so this gives the deck as an
         intrinsic diamond object and reduces the residue to a single concrete
         identification, but does NOT by itself close it.

The exact identities (1-4) are mirrored in wolfram/tfpt_readouts_extension.wl;
the deck-identification (5) stays the v140 [C]/[P] residue.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
I3 = sp.eye(3)

U = Q * sp.diag(1, 0, 0)
V = Q * sp.diag(0, 1, 1)
J = (U * V - V * U) / 3

DELTA_Q = 13          # = N_fam^2 + |Z2|^2 = 3^2 + 2^2 (v14)
EM_INDEX = 41         # = 10 b1 = g_car^2 + |mu4|^2 = 5^2 + 4^2 (v222)
i = sp.I


def run():
    reset()
    print("v415 Gaussian operator: J=[U,V]/3 is the mu4 quarter-turn; "
          "3+2i, 5+4i are eigenvalues; the deck is intrinsic")

    # ---- 1. the operator i ----
    check("THE OPERATOR i [E]: J = [U,V]/3 = [[-1,1,0],[-2,1,0],[-3,1,0]] is "
          "integer, Spec(J)={i,-i,0}, J^2=-I on the rank-2 image, J^3+J=0 "
          "(order 4 on the plane) -- a complex structure from [binary V, "
          "ternary U]",
          J == sp.Matrix([[-1, 1, 0], [-2, 1, 0], [-3, 1, 0]])
          and set(J.eigenvals().keys()) == {i, -i, sp.Integer(0)}
          and sp.simplify(J**3 + J) == sp.zeros(3)
          and J.rank() == 2)

    # ---- 2. the Gaussian integers are eigenvalues ----
    check("GAUSSIAN INTEGERS ARE EIGENVALUES [E]: 3I+2J has spectrum "
          "{3+2i,3-2i,3} (|3+2i|^2=13=Delta_Q) and 5I+4J has {5+4i,5-4i,5} "
          "(|5+4i|^2=41=10 b1) -- the abstract Gaussian integers are literal "
          "operator eigenvalues",
          set((3 * I3 + 2 * J).eigenvals().keys())
          == {3 + 2 * i, 3 - 2 * i, sp.Integer(3)}
          and set((5 * I3 + 4 * J).eigenvals().keys())
          == {5 + 4 * i, 5 - 4 * i, sp.Integer(5)}
          and (3**2 + 2**2) == DELTA_Q and (5**2 + 4**2) == EM_INDEX)

    # ---- 3. the norm dictionary as operator identities ----
    N32 = sp.simplify((3 * I3 + 2 * J) * (3 * I3 - 2 * J))
    N54 = sp.simplify((5 * I3 + 4 * J) * (5 * I3 - 4 * J))
    check("NORM DICTIONARY AS OPERATORS [E]: (3I+2J)(3I-2J)=9I-4J^2 has Spec "
          "{13,13,9} (13=Delta_Q on the mu4-plane, 9=N_fam^2 on the kernel); "
          "(5I+4J)(5I-4J)=25I-16J^2 has Spec {41,41,25} (41=10 b1, "
          "25=g_car^2) -- the v222/v230 norms lifted to operators",
          N32 == sp.simplify(9 * I3 - 4 * J * J)
          and N32.eigenvals() == {DELTA_Q: 2, N_fam**2: 1}
          and N54 == sp.simplify(25 * I3 - 16 * J * J)
          and N54.eigenvals() == {EM_INDEX: 2, g_car**2: 1})

    # ---- 4. the intrinsic mu4 deck ----
    Pi2 = sp.simplify(I3 + J * J)
    D = sp.simplify(J - Pi2)
    x = sp.symbols('x')
    check("INTRINSIC mu4 DECK [E]: Pi2=I+J^2 projects onto ker J; "
          "D=J-Pi2=-I+J-J^2=[[-1,1,0],[-2,1,0],[-4,3,-1]] is order 4 (D^4=I), "
          "chi_D=(x+1)(x^2+1), Spec(D)={i,-1,-i} (the seam-deck spectrum); "
          "the chi2 line is canonically ker[U,V]=(0,0,1)=a-1=the V-fixed line",
          Pi2.eigenvals() == {0: 2, 1: 1}
          and D == sp.Matrix([[-1, 1, 0], [-2, 1, 0], [-4, 3, -1]])
          and sp.simplify(D**4) == I3
          and sp.factor(D.charpoly(x).as_expr()) == (x + 1) * (x**2 + 1)
          and set(D.eigenvals().keys()) == {i, -i, sp.Integer(-1)}
          and J.nullspace() == [A - ONE]
          and (A - ONE) == sp.Matrix([0, 0, 1]))

    # ---- 5. deck identification: SHARPENED, not closed (v140 residue) ----
    delta = sp.diag(i, -1, -i)                       # the v146 geometric deck
    check("DECK IDENTIFICATION [C] (v140 residue, sharpened): D and the "
          "geometric seam deck delta=diag(i,-1,-i) (v146) share chi=(x+1)"
          "(x^2+1) and order 4; the diamond fixes the chi2 line as a-1 "
          "INTERNALLY, reducing the v140 Z3 choice to the single concrete "
          "identification 'is a-1 the geometric self-conjugate line?' -- "
          "intrinsic deck [E], geometric match still [C]/[P]",
          sp.factor(delta.charpoly(x).as_expr())
          == sp.factor(D.charpoly(x).as_expr())
          and delta**4 == I3)

    return summary("v415 Gaussian operator (J=mu4 quarter-turn; 3+2i/5+4i "
                   "eigenvalues; intrinsic deck D)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
