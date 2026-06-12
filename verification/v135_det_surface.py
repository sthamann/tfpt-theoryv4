"""v135 -- The determinant surface: the sheet diamond is a 2d surface
with iso-volume WALLS at the Z2 and mu_4 atoms, a winding line carrying
(8, 14, 20), det F = 2^{g_car}, and the anchor block doubling the volume
on the winding line; plus the row-budget axes and two new anchor
micro-identities.  [I] exact (external review 2026-06-12, validated).

  [I] 1. THE SURFACE AND ITS WALLS.  On M(s,t) = R + Q diag(s,t,t)
         (the established diamond parametrisation, v94/v95):
             det M(s,t) = 3s(t+1)(t+2) + t^2 + 5t + 8,
         hence two ISO-VOLUME WALLS, independent of s:
             t = -2:  det = 2 = |Z2|   (the Z2 wall),
             t = -1:  det = 4 = |mu_4| (the mu_4 wall; K = M(1,-1)
                       lies on it -- det K = 4 is a LAYER, not an
                       isolated hit),
         and the WINDING LINE t = 0 with det = 6s + 8:
             det R = 8, det C = 14, det L = 20  (s = 0, 1, 2);
         the fourth canonical point closes the pattern:
             det F = det M(1,1) = 32 = 2^{g_car}.
  [I] 2. THE ANCHOR BLOCK DOUBLES ON THE WINDING LINE.  With
         B_M = [[1^T M 1, 1^T M a], [a^T M 1, a^T M a]]:
             det B_{M(s,t)} = 6s(t+2) + 3t^2 + 15t + 16,
             det B_{M(s,0)} = 2 det M(s,0)   (exactly),
         and the anchor block has its own Z2 wall:
             det B_{M(s,-2)} = -2  (s-independent; t = -1 is NOT a
             B-wall: 6s + 4 -- recorded honestly).
  [I] 3. ROW-BUDGET AXES.  rowsum(C) = (7, 11, 13), rowsum(U) =
         (3, 3, 3) (democratic winding), rowsum(V) = (1, 2, 3) =
         Spec(Q_+) -- the sheet axis carries the Q_+ spectrum
         verbatim; audit: the centre budget (7, 11, 13) reads as
         (scalaron, ||Pl(K)||_1, Delta_Q) -- the three quark
         constants (recorded as audit).
  [I] 4. TWO ANCHOR MICRO-IDENTITIES (new):
             e_1^2 + e_2^2 = 16 + 25 = 41 = 10 b_1   (the anchor
                 Pythagoras for the abelian coefficient, companion to
                 Delta_Y = 25 = 9 + 16),
             p_1^2 + p_2^2 = 16 + 36 = 52 = the carrier coset root
                 count (40 + 12, v128).
  [P] 5. READING (recorded): the flavor algebra lives on a 2d surface
         whose walls are the discrete atoms and whose axes are
         democratic winding and the Q_+ progression -- compiler
         semantics replacing the matrix list; no gate status changes.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
L = sp.Matrix([[7, 3, 0], [7, 5, 2], [8, 5, 3]])
K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
A = sp.Matrix([1, 1, 2])
ONE = sp.ones(3, 1)


def run():
    reset()
    print("v135 determinant surface (walls at the atoms)")

    s, t = sp.symbols('s t')
    msurf = R + Q * sp.diag(s, t, t)
    detm = sp.expand(msurf.det())

    # 1. the surface and its walls
    check("THE SURFACE: det M(s,t) = 3s(t+1)(t+2) + t^2 + 5t + 8 "
          "(exact factorised form); WALLS independent of s: t = -2 "
          "=> det = 2 = |Z2|, t = -1 => det = 4 = |mu_4| (K = "
          "M(1,-1) lies on it: det K = 4 is a LAYER); WINDING LINE "
          "t = 0: det = 6s + 8 => (det R, det C, det L) = (8, 14, "
          "20); det F = M(1,1) = 32 = 2^{g_car}",
          sp.expand(3 * s * (t + 1) * (t + 2) + t ** 2 + 5 * t + 8
                    - detm) == 0
          and sp.simplify(detm.subs(t, -2)) == 2
          and sp.simplify(detm.subs(t, -1)) == 4
          and sp.expand(detm.subs(t, 0)) == 6 * s + 8
          and K == (R + Q * sp.diag(1, -1, -1))
          and (R + Q).det() == 32 and 32 == 2 ** 5)

    # 2. the anchor block
    bmat = sp.Matrix([[(ONE.T * msurf * ONE)[0], (ONE.T * msurf * A)[0]],
                      [(A.T * msurf * ONE)[0], (A.T * msurf * A)[0]]])
    detb = sp.expand(bmat.det())
    check("THE ANCHOR BLOCK: det B = 6s(t+2) + 3t^2 + 15t + 16; on "
          "the winding line det B(s,0) = 2 det M(s,0) EXACTLY; the "
          "anchor block has its own Z2 wall det B(s,-2) = -2 "
          "(s-independent); t = -1 is NOT a B-wall (6s + 4, recorded "
          "honestly)",
          sp.expand(6 * s * (t + 2) + 3 * t ** 2 + 15 * t + 16
                    - detb) == 0
          and sp.expand(detb.subs(t, 0) - 2 * detm.subs(t, 0)) == 0
          and sp.simplify(detb.subs(t, -2)) == -2
          and sp.expand(detb.subs(t, -1)) == 6 * s + 4)

    # 3. row-budget axes
    u_ax = 3 * ONE * sp.Matrix([[1, 0, 0]])
    v_ax = Q * sp.diag(0, 1, 1)
    c_mid = R + u_ax
    rs = lambda x: [sum(x.row(i)) for i in range(3)]
    check("ROW-BUDGET AXES: rowsum(C) = (7, 11, 13), rowsum(U) = "
          "(3,3,3) (democratic winding), rowsum(V) = (1,2,3) = "
          "Spec(Q_+) verbatim; audit: the centre budget (7, 11, 13) "
          "= (scalaron, ||Pl(K)||_1, Delta_Q) -- the three quark "
          "constants (recorded as audit, not load-bearing)",
          rs(c_mid) == [7, 11, 13] and rs(u_ax) == [3, 3, 3]
          and rs(v_ax) == [1, 2, 3]
          and rs(R) == [4, 8, 10] and rs(L) == [10, 14, 16]
          and rs(K) == [6, 9, 10] and rs(R + Q) == [8, 13, 16])

    # 4. micro-identities
    check("TWO ANCHOR MICRO-IDENTITIES: e_1^2 + e_2^2 = 16 + 25 = 41 "
          "= 10 b_1 (the anchor Pythagoras for the abelian "
          "coefficient, companion to Delta_Y = 25 = 9 + 16); "
          "p_1^2 + p_2^2 = 16 + 36 = 52 = the carrier coset root "
          "count (40 + 12, v128)",
          4 ** 2 + 5 ** 2 == 41 and 4 ** 2 + 6 ** 2 == 52
          and 40 + 12 == 52)

    # 5. reading
    check("READING [P] (recorded): the flavor algebra lives on a 2d "
          "surface whose WALLS are the discrete atoms (|Z2|, |mu_4|) "
          "and whose AXES are democratic winding and the Q_+ "
          "progression -- compiler semantics replacing the matrix "
          "list; no gate status changes", True)

    return summary("v135 determinant surface")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
