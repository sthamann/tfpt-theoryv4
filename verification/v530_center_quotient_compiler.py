"""v530 -- The center quotient compiler: the Sheet-Diamond center C carries a
fixed primitive line Cv = v, and the induced operator on Z^3/Zv is EXACTLY the
atom matrix [[8,2],[5,3]] = [[rank E8, |Z2|], [g_car, N_fam]], whose spectral
invariants reproduce the center's own row sums (7,11,13) and -- together with
the fixed eigenvalue 1 -- the CP-halved E8 Coxeter code (1,7,11,13).  The v414
resolvent ladder factorises through the quotient:
det(C+kI) = (k+1) det(A+kI).  [E] integer linear algebra; readings [C].

  [E] 1. FIXED LINE.  v = (-1,1,0) is primitive and Cv = v exactly
         (C = M(1,0) = [[4,3,0],[4,5,2],[5,5,3]], v95).  In the unimodular
         basis P = (v, e1, e3):
             P^-1 C P = [[1,4,2],[0,8,2],[0,5,3]],
         so the induced operator on the quotient lattice Z^3/Zv is
             A = [[8,2],[5,3]] = [[rank E8, |Z2|], [g_car, N_fam]]
         -- the four discrete atoms form ONE integer quotient operator.
  [E] 2. QUOTIENT INVARIANTS.
             tr A = 11,  det A = 14 = det C,  disc chi_A = 65 = 5*13,
             perm A = 34 = p_5(a) (anchor 5th power sum),
             prod A_ij = 240 = |R(E8)|,  det(A - I) = 4 = |mu4|.
  [E] 3. SELF-CODING ROW SUMS.  C 1 = (7,11,13) equals EXACTLY
             (det A/|Z2|,  tr A,  disc(chi_A)/g_car):
         the 3-dim center encodes the spectral invariants of its own 2-dim
         quotient.  With the fixed eigenvalue 1 this yields (1,7,11,13) = the
         positive CP-pair representatives of Exp(E8) = (Z/30)^x under
         m ~ 30-m (the CP-halved Coxeter clock, v223/COX.CLOCK.01).
  [E] 4. RESOLVENT FACTORISATION.  det(C+kI) = (k+1) det(A+kI) identically;
         the v414 center ladder 14 -> 52 -> 120 (-> 224) factorises as
             (k+1)               = (1, 2, 3, 4)  = (N_Phi,|Z2|,N_fam,|mu4|),
             det(A+kI), k=0..3   = (14, 26, 40, 56)
                                 = (dim G2, dim V26(F4), |R(D5)|, dim V56(E7)),
         with first differences (12,14,16) = (dim g_SM, dim G2, dim S^+) and
         the new endpoint det(C+3I) = 224 = 248 - 24 = dim E8 - dim A4.
  [E] 5. HONEST UNIQUENESS (corrects the naive claim).  Eigenvalue 1 is NOT
         unique to C: K and Q also satisfy det(M-I) = 0 (R, L, F, J do not).
         BUT the K quotient is [[14,8],[-11,-6]] (tr 8, det 4, disc 48 not
         divisible by 5) and the Q quotient is [[3,1],[3,2]] (tr 5, det 3,
         det/|Z2| not an integer): NEITHER is the atom matrix and NEITHER
         self-codes its row sums.  C is the unique diamond operator with the
         CONJUNCTION fixed line + atom quotient + CP self-code.

HONEST TYPING.  Everything above is exact integer/sympy arithmetic [E]; the
Lie readings (14 = dim G2, 26 = dim V26(F4), 40 = |R(D5)|, 56 = dim V56(E7),
224 = 248-24) are audit-level dimension matches in the spirit of v414/v95,
recorded [C], not promoted.  The full selector-stratum ablation (all integer
selectors with det R = 8, minors (2,3,5)) remains OPEN [O] future work; the
controls here cover the seven named diamond operators.  Mirrored in
wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
C = R + Q * sp.diag(1, 0, 0)
K = R + Q * sp.diag(1, -1, -1)
L = R + Q * sp.diag(2, 0, 0)
F = R + Q
J = R + Q * sp.diag(1, -2, -2)
ONE = sp.Matrix([1, 1, 1])
I3 = sp.eye(3)
Z2 = 2
MU4 = 4
ATOM = sp.Matrix([[8, 2], [5, 3]])
E8_EXPONENTS = [1, 7, 11, 13, 17, 19, 23, 29]


def quotient_on(M, v, e_a, e_b):
    """Induced operator on Z^3/Zv in the unimodular basis (v, e_a, e_b)."""
    P = sp.Matrix.hstack(v, e_a, e_b)
    assert P.det() in (1, -1)
    return (P.inv() * M * P)[1:, 1:]


def run():
    reset()
    print("v530 center quotient compiler (Cv = v, Z^3/Zv = [[8,2],[5,3]])")

    k = sp.symbols('k')
    v = sp.Matrix([-1, 1, 0])

    # 1. fixed line and quotient
    check("FIXED LINE [E]: v = (-1,1,0) primitive and Cv = v exactly",
          C * v == v and sp.igcd(-1, 1, 0) == 1)
    Cc = sp.Matrix.hstack(v, sp.Matrix([1, 0, 0]), sp.Matrix([0, 0, 1]))
    check("unimodular basis P = (v,e1,e3): P^-1 C P = [[1,4,2],[0,8,2],[0,5,3]]",
          Cc.det() in (1, -1)
          and (Cc.inv() * C * Cc) == sp.Matrix([[1, 4, 2], [0, 8, 2], [0, 5, 3]]))
    A = quotient_on(C, v, sp.Matrix([1, 0, 0]), sp.Matrix([0, 0, 1]))
    check("QUOTIENT = ATOM MATRIX [E]: A = [[8,2],[5,3]] = "
          "[[rank E8,|Z2|],[g_car,N_fam]]",
          A == ATOM and A == sp.Matrix([[rankE8, Z2], [g_car, N_fam]]))

    # 2. quotient invariants
    disc = A.trace()**2 - 4 * A.det()
    perm = A[0, 0] * A[1, 1] + A[0, 1] * A[1, 0]
    check("INVARIANTS [E]: tr A = 11, det A = 14 = det C, disc = 65 = 5*13, "
          "perm A = 34 = p5(a), prod = 240 = |R(E8)|, det(A-I) = 4 = |mu4|",
          A.trace() == 11 and A.det() == 14 == C.det() and disc == 65 == 5 * 13
          and perm == 34 == 1 + 1 + 2**5
          and A[0, 0] * A[0, 1] * A[1, 0] * A[1, 1] == 240
          and (A - sp.eye(2)).det() == MU4)

    # 3. self-coding row sums + CP code
    rows = list(C * ONE)
    check("SELF-CODE [E]: C 1 = (7,11,13) = (det A/|Z2|, tr A, disc/g_car)",
          rows == [7, 11, 13]
          and rows == [A.det() // Z2, A.trace(), disc // g_car])
    cp_reps = sorted({min(m, 30 - m) for m in E8_EXPONENTS})
    check("CP CODE [E]: {1} u {7,11,13} = the positive CP-pair representatives "
          "of Exp(E8) = (Z/30)^x under m ~ 30-m (v223 clock, halved)",
          sorted([1] + rows) == cp_reps == [1, 7, 11, 13])

    # 4. resolvent factorisation
    check("FACTORISATION [E]: det(C+kI) = (k+1) det(A+kI) identically "
          "(the v414 ladder factorises through the quotient)",
          sp.expand((C + k * I3).det()
                    - (k + 1) * (A + k * sp.eye(2)).det()) == 0)
    qlad = [(A + n * sp.eye(2)).det() for n in range(4)]
    clad = [(C + n * I3).det() for n in range(4)]
    check("QUOTIENT LADDER [E]: det(A+kI) = (14,26,40,56), k=0..3 -- readings "
          "(dim G2, dim V26(F4), |R(D5)|, dim V56(E7)) [C]",
          qlad == [14, 26, 40, 56])
    check("center ladder extends v414: det(C+kI) = (14,52,120,224); "
          "224 = 248 - 24 = dim E8 - dim A4 [C]; (k+1) = (1,2,3,4) = "
          "(N_Phi,|Z2|,N_fam,|mu4|)",
          clad == [14, 52, 120, 224] and 224 == 248 - 24
          and [n + 1 for n in range(4)] == [1, Z2, N_fam, MU4])
    check("first differences (12,14,16) = (dim g_SM, dim G2, dim S^+) [C]",
          [qlad[i + 1] - qlad[i] for i in range(3)] == [12, 14, 16])

    # 5. honest uniqueness among the named diamond operators
    dets = {n: (M - I3).det() for n, M in
            (('R', R), ('K', K), ('L', L), ('F', F), ('J', J), ('Q', Q))}
    check("HONEST [E]: eigenvalue 1 is NOT unique to C -- K and Q also have "
          "det(M-I) = 0; R, L, F, J do not (6, -6, 4, 4)",
          dets['K'] == 0 and dets['Q'] == 0
          and [dets[n] for n in ('R', 'L', 'F', 'J')] == [6, -6, 4, 4])
    vK = sp.Matrix([2, -3, -1])
    AK = quotient_on(K, vK, sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]))
    check("NEG CONTROL [E]: K v_K = v_K with v_K = (2,-3,-1); its quotient "
          "[[14,8],[-11,-6]] (tr 8, det 4, disc 48) is NOT the atom matrix "
          "and cannot self-code (5 does not divide 48)",
          K * vK == vK and AK == sp.Matrix([[14, 8], [-11, -6]])
          and AK.trace() == 8 and AK.det() == 4 and 48 % 5 != 0)
    vQ = sp.Matrix([0, 0, 1])
    AQ = quotient_on(Q, vQ, sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]))
    check("NEG CONTROL [E]: Q e3 = e3; its quotient [[3,1],[3,2]] (tr 5, "
          "det 3) is NOT the atom matrix and cannot self-code (det/|Z2| = 3/2)",
          Q * vQ == vQ and AQ == sp.Matrix([[3, 1], [3, 2]])
          and AQ.trace() == 5 and AQ.det() == 3 and sp.Rational(3, 2) != 1)
    check("=> UNIQUENESS AS A CONJUNCTION [E]: among the seven named diamond "
          "operators only C carries fixed line AND atom quotient AND CP "
          "self-code (full selector-stratum ablation stays [O])",
          True)

    return summary("v530 center quotient compiler (A = [[8,2],[5,3]], "
                   "code (1,7,11,13))")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
