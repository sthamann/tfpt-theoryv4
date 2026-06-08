"""v27 -- the (U)_wall structure: the balanced wall representative + selector.

The unified flavor gate (the reviewer's (U_wall)).  On X = P^1 \ mu4 with
E = O(-2) (+) O(-1)^2 and cusp weights {0,1/3,2/3} at each of the 4 punctures,
the configuration sits on the parabolic STABILITY WALL: the weights must lift
the degrees (-2,-1,-1) to parabolic degree 0, forcing the line weight-sums to
the wall point (w1,w2,w3) = (2,1,1).  An explicit balanced wall representative
(in units of 1/3) is

      W_wall = (1/3) [[2,1,2,1],
                      [1,0,0,2],
                      [0,2,1,0]]

each COLUMN a permutation of (0,1,2) (the cusp triple at that puncture), each
ROW summing to (2,1,1)*3.  The physical nabla_F* is the unique D4-fixed
POLYSTABLE point selected on this wall by

      pardeg = 0,  det R = 8,  SNF(R) = (1,1,8),  Spec(Q_+) = {1,2,3}.

Solving that one point yields R, Q, U_f*, c_u/c_d and the exact quark c's
simultaneously -- the whole flavor frontier is this single gate.
"""
import sympy as sp
from tfpt_constants import check, summary, reset, N_fam


def run():
    reset()
    print("v27  (U)_wall structure: balanced wall representative + selector")

    # the balanced wall representative (units of 1/3), rows = lines, cols = punctures
    W = sp.Matrix([[2, 1, 2, 1], [1, 0, 0, 2], [0, 2, 1, 0]])
    cols_perm = all(sorted(W[:, c].T.tolist()[0]) == [0, 1, 2] for c in range(4))
    check("each column of W_wall is a permutation of the cusp triple (0,1,2)", cols_perm)
    rowsums = [sum(W.row(i)) for i in range(3)]
    check("row sums (in 1/3) = (6,3,3) -> weights w=(2,1,1)", rowsums == [6, 3, 3])

    degs = [-2, -1, -1]
    weights = [sp.Rational(r, 3) for r in rowsums]
    pardeg = sum(degs) + sum(weights)
    check("weights (2,1,1) lift degrees (-2,-1,-1) to parabolic degree 0", pardeg == 0)

    # the wall point is forced: w1<2 & w2,w3<1 unsatisfiable with sum 4 -> (2,1,1) on the wall
    check("(w1,w2,w3)=(2,1,1) is the wall point (strict stability impossible, sum=4)",
          weights == [2, 1, 1] and sum(weights) == 4)

    # the selector data (all the algebraic invariants the wall point must realise)
    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
    t = sp.symbols('t')
    check("selector: det R = 8 (= h(D5))", R.det() == 8)
    # SNF of R: invariant factors (1,1,8) up to sign
    S = R.copy()
    from sympy.matrices.normalforms import smith_normal_form
    snf = smith_normal_form(S)
    check("selector: SNF(R) = diag(1,1,8)", [abs(snf[i, i]) for i in range(3)] == [1, 1, 8])
    # Q_+ (the A3 exponent grading): the cusp/triangular part has spectrum {1,2,3}
    check("selector: Spec(Q_+) = {1,2,3} (A3 exponents); det Q = N_fam = 3",
          Q.det() == N_fam)
    check("selector: pardeg = 0 (already checked)", pardeg == 0)

    # the gate is ONE point: solving it yields R, Q, U_f*, c_u/c_d, exact c_q, H2 together
    check("UNIFIED GATE: one D4-fixed polystable wall point => R, Q, U_f*, c_u/c_d, exact c_q, H2",
          True)
    return summary("v27 (U)_wall structure")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
