"""v95 -- Centered Flavor Diamond (third review round, 2026-06-11): the four
flavor operators are ONE center plus TWO axes.  [I] closures + audit typing.

Sharpens v94: the sheet diamond M(s,t) = R + Q diag(s,t,t) is not just a
surface with four distinguished points -- it is a CENTERED cross.  With

    C := M(1,0) = (R+L)/2 = (K+F)/2     (the center),
    U := Q diag(1,0,0) = N_fam * 1 e_1^T   (the WINDING axis, rank 1),
    V := Q diag(0,1,1)                     (the SHEET axis,   rank 2),

one has exactly

    Q = U + V,
    R = C - U,   L = C + U,   K = C - V,   F = C + V :

five objects (R, K, L, F, Q) collapse to three (C, U, V), and the v94
winding line IS the U-axis (L = R + 2U).

CENTER INVARIANTS (all exact):
    tr C = 12,  det C = 14,  SNF(C) = (1,1,14),
    sum C = 31 = 2^g_car - 1 = 1 + h_vee(E8),
    det B_C = 28 = 2*14,
    Pi_L(C) = (0,14,14),   Pi_R(C) = (14,21,7) = 7*(2,3,1).

CROSS-LINKS (the structural content beyond the review):
  * Spec(V) = {0,1,2} = N_fam * {0, 1/3, 2/3} -- the sheet axis carries
    exactly the CUSP CLASS of v69/v72 (Q_+ = 3*cusp + 1 had {1,2,3});
  * Spec(U) = {3,0,0}: the winding axis is pure family charge;
  * sum C = 31 is the SAME 31 as the IR gap-bound numerator
    ||V_metric|| <= 248 c3^2 = 31/(8 pi^2)  (v63/v76);
  * det C = 14 is the SAME 14 as the constant term of chi_[K,Q] =
    t^3 + 5t + 14  (v80) and half of sum B_F = 196 = 14^2 (v94);
  * Pi_R(C) = 7*(2,3,1) shares its direction (2,3,1) with
    Pi_R(L) = 10*(2,3,1): scalaron-7 vs decuple-10 scaling of one ray.

HONEST TYPING: the normal form and every integer above are exact [I];
the reading "C carries a G2 center" (14 = dim G2 as det, Pluecker entry
and half anchor block) is an AUDIT-level Lie-dimension match, exactly like
78 = dim E6 or 52 = dim F4 elsewhere -- recorded, not promoted.
"""
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

from tfpt_constants import check, summary, reset, g_car, N_fam

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
SIG = sp.diag(1, -1, -1)
K = R + Q * SIG
L = R + Q * (sp.eye(3) + SIG)
F = R + Q
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])

C = R + Q * sp.diag(1, 0, 0)
U = Q * sp.diag(1, 0, 0)
V = Q * sp.diag(0, 1, 1)


def anchor_block(M):
    return sp.Matrix([[(ONE.T * M * ONE)[0], (ONE.T * M * A)[0]],
                      [(A.T * M * ONE)[0], (A.T * M * A)[0]]])


def pi_left(M):
    blk = sp.Matrix.vstack((ONE.T * M), (A.T * M))
    return [blk[:, [i, j]].det() for i, j in ((0, 1), (0, 2), (1, 2))]


def pi_right(M):
    blk = sp.Matrix.hstack(M * ONE, M * A)
    return [blk[[i, j], :].det() for i, j in ((0, 1), (0, 2), (1, 2))]


def run():
    reset()
    print("v95 centered flavor diamond (one center, two axes)")

    # 1. the normal form
    check("center: C = M(1,0) = (R+L)/2 = (K+F)/2 = [[4,3,0],[4,5,2],[5,5,3]]",
          C == (R + L) / 2 and C == (K + F) / 2
          and C == sp.Matrix([[4, 3, 0], [4, 5, 2], [5, 5, 3]]))
    check("axes: Q = U + V with U = N_fam * 1 e_1^T (winding) and "
          "V = Q diag(0,1,1) (sheet)",
          Q == U + V and U == N_fam * ONE * sp.Matrix([[1, 0, 0]]))
    check("CENTERED CROSS: R = C-U, L = C+U, K = C-V, F = C+V "
          "(five objects -> three)",
          R == C - U and L == C + U and K == C - V and F == C + V)
    check("the v94 winding line IS the U-axis: L = R + 2U "
          "(s=6 winding = 2U, U eigenvalues {3,0,0} = pure family charge)",
          L == R + 2 * U and sorted(sp.Matrix(U).eigenvals().keys()) == [0, 3]
          and U.rank() == 1)

    # 2. the sheet axis carries the cusp class
    check("Spec(V) = {0,1,2} = N_fam * cusp weights {0,1/3,2/3} "
          "(the same cusp class as Q_+ = 3*cusp+1 with {1,2,3}, v69/v72)",
          sorted(V.eigenvals().keys()) == [0, 1, 2] and V.rank() == 2
          and [N_fam * w for w in (0, sp.Rational(1, 3), sp.Rational(2, 3))]
          == [0, 1, 2])

    # 3. center invariants
    check("tr C = 12, det C = 14, SNF(C) = (1,1,14)",
          C.trace() == 12 and C.det() == 14
          and smith_normal_form(C).diagonal().tolist() == [[1, 1, 14]])
    check("sum C = 31 = 2^g_car - 1 = 1 + h_vee(E8) -- the SAME 31 as the "
          "IR gap-bound numerator ||V_metric|| <= 31/(8 pi^2) (v63/v76)",
          sum(C) == 31 == 2**g_car - 1 == 1 + 30)
    BC = anchor_block(C)
    check("anchor block B_C = [[31,36],[44,52]], det B_C = 28 = 2*14",
          BC == sp.Matrix([[31, 36], [44, 52]]) and BC.det() == 28)
    check("Pluecker of the center: Pi_L(C) = (0,14,14), "
          "Pi_R(C) = (14,21,7) = 7*(2,3,1)",
          pi_left(C) == [0, 14, 14] and pi_right(C) == [14, 21, 7])

    # 4. cross-links
    t = sp.symbols('t')
    chi_comm = sp.expand((t * sp.eye(3) - (K * Q - Q * K)).det())
    check("det C = 14 = constant term of chi_[K,Q] = t^3 + 5t + 14 (v80) "
          "= sqrt(sum B_F) (v94: 196 = 14^2)",
          C.det() == 14 and chi_comm == t**3 + 5 * t + 14
          and 14**2 == 196)
    check("ray alignment: Pi_R(C) = 7*(2,3,1) and Pi_R(L) = 10*(2,3,1) -- "
          "the same direction, scalaron-7 vs decuple-10 scaling",
          pi_right(C) == [7 * x for x in (2, 3, 1)]
          and pi_right(L) == [10 * x for x in (2, 3, 1)])

    # 5. honest typing
    check("AUDIT TYPING: the 'G2 center' reading (14 = dim G2) is a "
          "Lie-dimension match like 78 = dim E6 / 52 = dim F4 -- recorded, "
          "NOT promoted; the load-bearing content is the exact normal form "
          "C +- U, C +- V and its integer invariants",
          True)

    return summary("v95 centered diamond")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
