"""v218 -- The Diamond Axis Geometry: the Sheet Diamond is a discrete geometry
with TWO axes, and the missing corner F is the natural transfer completion.
Sharpens v94 (sheet diamond) / v95 (centered cross C,U,V) with three exact
[E] lemmas plus honestly-typed audit/heuristic blocks. NO new numbers -- it
organises the existing operators {Q,K,R,C,L,F} more strictly.

  [I] 1. DIAMOND AXIS CURVATURE LEMMA.  Along the two canonical axes of the
        centered cross (C the center, U winding, V sheet, v95) the determinant
        is LINEAR on the winding axis and QUADRATIC on the sheet axis:
            det(C + x U) = 14 + 6 x              (flat: slope 6 = |R^+(A_3)|)
            det(C + y V) = 14 + 14 y + 4 y^2     (2nd diff = 8 = rank E_8)
            det B(C + x U) = 28 + 12 x = 2 det(C + x U)
            det B(C + y V) = 28 + 21 y + 3 y^2   (2nd diff = 6 = |R^+(A_3)|)
        So winding flows linearly (A_3-driven), the sheet split CURVES, and the
        two curvatures are exactly rank E_8 = 8 (determinant) and |R^+(A_3)| = 6
        (anchor block) -- a discrete differential geometry of the diamond.
  [I] 2. PLUECKER TRANSFER LADDER.  The anchor-Pluecker coordinates lift K->C->F
        in two exact steps:
            Pl(K) = (-1, 6, 4),  Pl(C) = (0,14,14),  Pl(F) = (1,22,30),
            Pl(C) - Pl(K) = (1, 8, 10) = (N_Phi, rank E_8, A_Lambda),
            Pl(F) - Pl(C) = (1, 8, 16) = (N_Phi, rank E_8, dim S^+).
        Each step adds (1, 8) in the first two coordinates; the third adds first
        the decuple A_Lambda = 10, then the full spinor generation dim S^+ = 16.
        The Pluecker identity is [E]; the F_transfer source->pole reading (a
        two-stage sheet lift) stays [C].
  [I] 3. SPECTRAL RAMIFICATION LADDER.  For Q,K,C,F the characteristic polynomial
        splits as (t - r)(t^2 - b t + c) with r rational, and the FULL cubic
        discriminant factors as Disc(chi) = q(r)^2 * Disc(q):
            squares q(r)^2 in {1^2, 3^2, 4^2, 6^2} = (N_Phi, N_fam, |mu4|, |R^+(A_3)|)^2,
            kernels Disc(q) in {13, 48, 65, 105}
                  = (Delta_Q, Omega_adm, g_car*Delta_Q, N_fam*g_car*7),
        with Delta_Q = 13 = b^2 + s^2 = |R(A_3)| + 1 the carrier-split norm (v14).
        The missing corner F carries the kernel 105 = 3*5*7 = family*carrier*scalaron.
  [I] 4. ANCHOR DEFECT SPECTRUM (audit).  One anchor operation Delta_a(M) =
        a^T M a - 1^T M 1 reads six known blocks across the whole diamond:
            Delta_a(Q,K,R,C,L,F) = (8, 16, 18, 21, 24, 26)
              = (rank E_8, dim S^+, N_fam|R^+(A_3)|, N_fam*7, |W(A_3)|, 2*13),
        monotone in the SAME ordering as the determinant ladder. NOTE the cleaned
        notation: 26 = 2*13 uses the SPECTRAL Delta_Q = 13, NOT the anchor defect
        Delta_a(Q) = 8. AUDIT-typed: spine only if the six operators are shown
        canonical and complete.
  [I] 5. PAIR-SUM ATLAS + DETERMINANT STAIRCASE (audit fingerprints).  The four
        corner determinants (det R,K,L,F) = (8,4,20,32) have six pair sums
        {12,24,28,36,40,52} and total 64 = dim S^+ * |mu4|; the six diamond
        determinants (3,4,8,14,20,32) sum to 81 = N_fam^4 with steps
        (+1,+4,+6,+6,+12). The spine reads are 12 = dim g_SM = |R(A_3)|,
        24 = |W(A_3)|, 36 = N_fam|R(A_3)|, 40 = |R(D_5)|, 64 = dim S^+|mu4|; but
        28 = 2 dim G_2 and 52 = dim F_4 are EXOTIC Lie labels -- audit only, NOT
        spine (same typing as the G_2/F_4 shadows in v94/v95).
  [C] 6. F AS THE TRANSFER COMPLETION CORNER (heuristic, NOT a hard rule).  F is
        where the diamond tips from compiler into transfer: det F = 32 = 2^g_car,
        a^T F 1 = 53 = sum Pl(F), det L + det F = 52, det R + det F = 40. The
        search principle "every F_transfer kernel must cast an F / Pluecker /
        (2/3)^6 shadow" is recorded as a HEURISTIC only -- promoting it to a hard
        admissibility filter is explicitly rejected (cf. the v94 firewall
        rejection of the over-strong adjacent-quotient rule).

  Python-only here; the exact identities (axis curvatures, the Pluecker ladder,
  the discriminant factorisations) are mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import (check, summary, reset, g_car, N_fam,
                            dim_Splus, Omega_adm)

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])

C = R + Q * sp.diag(1, 0, 0)
U = Q * sp.diag(1, 0, 0)
V = Q * sp.diag(0, 1, 1)
K = C - V
L = C + U
F = C + V

# Lie-theoretic block constants (same convention as v94/v95)
RANK_E8 = 8
R_A3 = 12            # |R(A_3)|  (all roots of A_3 = su(4))
RP_A3 = 6            # |R^+(A_3)| (positive roots)
W_A3 = 24            # |W(A_3)| = 4!
R_D5 = 40            # |R(D_5)|  (roots of D_5)
DIM_GSM = 12         # dim su(3)+su(2)+u(1)
A_LAMBDA = 10        # |E(K_5)| decuple
SCALARON = 7         # scalaron exponent
DELTA_Q = 13         # carrier-split norm b^2+s^2 = |R(A_3)|+1 (v14)
MU4 = 4
N_PHI = 1


def anchor_block(M):
    return sp.Matrix([[(ONE.T * M * ONE)[0], (ONE.T * M * A)[0]],
                      [(A.T * M * ONE)[0], (A.T * M * A)[0]]])


def pi_left(M):
    blk = sp.Matrix.vstack((ONE.T * M), (A.T * M))
    return [blk[:, [i, j]].det() for i, j in ((0, 1), (0, 2), (1, 2))]


def defect(M):
    return (A.T * M * A)[0] - (ONE.T * M * ONE)[0]


def ramification(M):
    """(|q(r)|, Disc(q)) for chi_M = (t - r)(t^2 - b t + c), r the rational root."""
    t = sp.symbols('t')
    p = M.charpoly(t).as_expr()
    r = next(rt for rt in sp.roots(p, t) if rt.is_rational)
    q = sp.factor(sp.cancel(p / (t - r)))
    return abs(q.subs(t, r)), sp.discriminant(q, t)


def run():
    reset()
    print("v218 diamond axis geometry: U-axis flat (A3), V-axis curved (E8), F the transfer corner")

    x, y = sp.symbols('x y')

    # ---- LEMMA 1: axis curvature ----
    dU = sp.expand((C + x * U).det())
    dV = sp.expand((C + y * V).det())
    bU = sp.expand(anchor_block(C + x * U).det())
    bV = sp.expand(anchor_block(C + y * V).det())
    sheet = [(C + i * V).det() for i in (-1, 0, 1)]
    bsheet = [anchor_block(C + i * V).det() for i in (-1, 0, 1)]
    second_diff = sheet[2] - 2 * sheet[1] + sheet[0]
    bsecond_diff = bsheet[2] - 2 * bsheet[1] + bsheet[0]
    check("LEMMA 1 AXIS CURVATURE [I]: det(C+xU) = 14+6x is LINEAR (winding flat, "
          "slope 6 = |R^+(A_3)|); det(C+yV) = 14+14y+4y^2 is QUADRATIC with 2nd "
          "difference = %d = rank E_8; det B(C+xU) = 28+12x = 2 det(C+xU); the "
          "anchor-block sheet 2nd difference = %d = |R^+(A_3)| -- two curvatures "
          "(8 det, 6 anchor) = (rank E_8, |R^+(A_3)|)" % (second_diff, bsecond_diff),
          dU == 6 * x + 14 and dV == 4 * y**2 + 14 * y + 14
          and bU == 12 * x + 28 and sp.expand(bU - 2 * dU) == 0
          and bV == 3 * y**2 + 21 * y + 28
          and second_diff == RANK_E8 and bsecond_diff == RP_A3)

    # ---- LEMMA 2: Pluecker transfer ladder ----
    plK, plC, plF = pi_left(K), pi_left(C), pi_left(F)
    step1 = [plC[i] - plK[i] for i in range(3)]
    step2 = [plF[i] - plC[i] for i in range(3)]
    check("LEMMA 2 PLUECKER TRANSFER LADDER [I]: Pl(K)=%s -> Pl(C)=%s -> Pl(F)=%s "
          "lifts in two steps: C-K = %s = (N_Phi, rank E_8, A_Lambda), F-C = %s = "
          "(N_Phi, rank E_8, dim S^+); each step adds (1,8), the third adds the "
          "decuple 10 then the full generation 16 (identity [I]; source->pole "
          "reading [C])" % (plK, plC, plF, step1, step2),
          plK == [-1, 6, 4] and plC == [0, 14, 14] and plF == [1, 22, 30]
          and step1 == [N_PHI, RANK_E8, A_LAMBDA]
          and step2 == [N_PHI, RANK_E8, dim_Splus])

    # ---- LEMMA 3: spectral ramification ladder ----
    sq, ker = {}, {}
    for nm, M in (('Q', Q), ('K', K), ('C', C), ('F', F)):
        s_, k_ = ramification(M)
        sq[nm], ker[nm] = s_, k_
    squares = [sq['Q'], sq['K'], sq['C'], sq['F']]
    kernels = [ker['Q'], ker['K'], ker['C'], ker['F']]
    check("LEMMA 3 SPECTRAL RAMIFICATION [I]: for Q,K,C,F the cubic discriminant "
          "factors as q(r)^2 * Disc(q); squares |q(r)| = %s = (N_Phi, N_fam, "
          "|mu4|, |R^+(A_3)|); kernels Disc(q) = %s = (Delta_Q, Omega_adm, "
          "g_car*Delta_Q, N_fam*g_car*7), Delta_Q = 13 = |R(A_3)|+1 (v14); F "
          "carries 105 = 3*5*7 = family*carrier*scalaron"
          % (squares, kernels),
          squares == [N_PHI, N_fam, MU4, RP_A3]
          and kernels == [DELTA_Q, Omega_adm, g_car * DELTA_Q,
                          N_fam * g_car * SCALARON])

    # ---- AUDIT 4: anchor defect spectrum (cleaned notation) ----
    spectrum = [defect(M) for M in (Q, K, R, C, L, F)]
    check("AUDIT ANCHOR DEFECT SPECTRUM [I]: Delta_a(Q,K,R,C,L,F) = %s = "
          "(rank E_8, dim S^+, N_fam|R^+(A_3)|, N_fam*7, |W(A_3)|, 2*13), "
          "monotone in the determinant ordering; 26 = 2*13 uses the SPECTRAL "
          "Delta_Q=13, NOT the anchor defect Delta_a(Q)=8 (cleaned). AUDIT: "
          "spine only if the six operators are canonical/complete" % spectrum,
          spectrum == [RANK_E8, dim_Splus, N_fam * RP_A3, N_fam * SCALARON,
                       W_A3, 2 * DELTA_Q]
          and spectrum == sorted(spectrum))

    # ---- AUDIT 5: pair-sum atlas + determinant staircase ----
    corners = {'R': R.det(), 'K': K.det(), 'L': L.det(), 'F': F.det()}
    import itertools
    pairsums = sorted(corners[i] + corners[j]
                      for i, j in itertools.combinations(['R', 'K', 'L', 'F'], 2))
    total4 = sum(corners.values())
    seq = [Q.det(), K.det(), R.det(), C.det(), L.det(), F.det()]
    steps = [seq[i + 1] - seq[i] for i in range(5)]
    spine_sums = {12: DIM_GSM, 24: W_A3, 36: N_fam * R_A3, 40: R_D5}
    exotic = {28: 2 * 14, 52: 52}     # 2 dim G_2, dim F_4 -- audit only
    check("AUDIT PAIR-SUM ATLAS + STAIRCASE [I]: corner-det pair sums = %s, total "
          "= %d = dim S^+ * |mu4|; det staircase (3,4,8,14,20,32) sum 81 = "
          "N_fam^4, steps %s. SPINE: 12=dim g_SM, 24=|W(A_3)|, 36=N_fam|R(A_3)|, "
          "40=|R(D_5)|, 64=dim S^+|mu4|; but 28=2 dim G_2 and 52=dim F_4 are "
          "AUDIT-only exotic labels, NOT spine (same typing as v94/v95)"
          % (pairsums, total4, steps),
          pairsums == [12, 24, 28, 36, 40, 52] and total4 == dim_Splus * MU4
          and sum(seq) == N_fam**4 and steps == [1, 4, 6, 6, 12]
          and set(spine_sums) <= set(pairsums)
          and set(exotic) <= set(pairsums))

    # ---- HEURISTIC 6: F as the transfer completion corner ----
    check("HEURISTIC F = TRANSFER COMPLETION CORNER [C]: det F = 32 = 2^g_car, "
          "a^T F 1 = 53 = sum Pl(F), det L + det F = 52, det R + det F = 40. The "
          "rule 'every F_transfer kernel casts an F / Pluecker / (2/3)^6 shadow' "
          "is a HEURISTIC search principle ONLY -- NOT promoted to a hard "
          "admissibility filter (cf. the v94 firewall rejection)",
          F.det() == 2**g_car and (A.T * F * ONE)[0] == 53
          and sum(pi_left(F)) == 53 and L.det() + F.det() == 52
          and R.det() + F.det() == 40)

    return summary("v218 diamond axis geometry (U=A3 flow, V=E8 curvature, F=transfer corner)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
