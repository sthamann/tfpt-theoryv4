"""v410 -- The sheet generator V is a binary internal compiler.  The centered
cross of the Sheet Diamond (v95/v218) has the rank-2 sheet axis
V = Q diag(0,1,1); its POWERS print the binary carrier spine and the recurring
flavor/audit integers as bilinear readouts of one operator.  [E] algebra,
[C]/audit readings (the spine is FORCED by Spec(V) = {0,1,2}).

  [E] 1. CLOSED FORM.  For all n >= 1 (proved by the inductive step
         F(n)*V = F(n+1), base case F(1) = V):
             V^n = [[0, 2^{n-1}, 0],
                    [0, 2^n,     0],
                    [0, 2^{n+1}-2, 1]],
         hence the binary carrier spine
             V^n 1 = (2^{n-1}, 2^n, 2^{n+1}-1),
             V^1..4 1 = (1,2,3), (2,4,7), (4,8,15), (8,16,31).
  [E] 2. BILINEAR FAMILIES (all exact in n, with 1 = (1,1,1), a = (1,1,2)):
             1^T V^n 1 = 7*2^{n-1} - 1,   1^T V^n a = 7*2^{n-1},
             a^T V^n a = 11*2^{n-1},      a^T V^n 1 = 11*2^{n-1} - 2.
         At n = 1 the four readouts are (6, 7, 9, 11) = (|R^+(A_3)|, scalaron,
         N_fam^2, the anchor amplitude); the higher levels give
             1^T V^2 1 = 13 = Delta_Q,   1^T V^3 1 = 27 = 1^T R a,
             1^T V^4 1 = 55 = quark numerator,  1^T V^4 a = 56 = dim 56_{E_7}.
  [C] 3. BINARY-SPINE READING (audit, NOT promoted).  The spine entries
         {2^{k-1}, 2^k, 2^{k+1}-1} are forced by Spec(V) = {0,1,2} (v95): the
         dominant eigenvalue 2 drives the doubling, the eigenvalue 1 fixes the
         third slot.  That these powers land on the carrier atoms
             (1,2,3) = A_3 exponents,
             (2,4,7) = (|Z2|, |mu4|, scalaron 7),
             (4,8,15) = (|mu4|, rank E_8, dim A_3),
             (8,16,31) = (rank E_8, dim S^+, 2^{g_car}-1 = 248/8)
         is an audit-level Lie/dimension match, exactly like the G_2 center
         reading of v95 -- recorded, not promoted.
  [C] 4. THETA CROSS-LINK (audit raster).  The E_8 theta shell degeneracies
         240*sigma_3(n) = 240, 2160, 6720, 17520 (tfpt_3) read the same V
         bilinears at prime shells:
             sigma_3(2) = 9  = a^T V 1 = N_fam^2,
             sigma_3(3) = 28 = 1^T V^3 a = det(I+R),
             sigma_3(5) = 126 = the local E_7 root shell (tfpt_3 lemma v).
         An audit raster, not a physics claim.

Mirrored in wolfram/tfpt_readouts_extension.wl (exact identities only).
"""
import sympy as sp

from tfpt_constants import (check, summary, reset, g_car, N_fam, dim_Splus,
                            rankE8)

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
V = Q * sp.diag(0, 1, 1)
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
I3 = sp.eye(3)

SCALARON = 7
DELTA_Q = 13
DIM_56_E7 = 56


def run():
    reset()
    print("v410 sheet generator V: a binary internal compiler (V^n prints the spine)")

    n = sp.symbols('n', positive=True, integer=True)

    # ---- 0. anchor to the established cross ----
    check("V = Q diag(0,1,1) = [[0,1,0],[0,2,0],[0,2,1]] is the rank-2 sheet "
          "axis with Spec(V) = {0,1,2} (the cusp class, v95/v135)",
          V == sp.Matrix([[0, 1, 0], [0, 2, 0], [0, 2, 1]])
          and sorted(V.eigenvals().keys()) == [0, 1, 2] and V.rank() == 2)

    # ---- 1. closed form V^n + binary spine ----
    def Vn(k):
        return sp.Matrix([[0, 2**(k - 1), 0],
                          [0, 2**k, 0],
                          [0, 2**(k + 1) - 2, 1]])
    Fn = sp.Matrix([[0, 2**(n - 1), 0],
                    [0, 2**n, 0],
                    [0, 2**(n + 1) - 2, 1]])
    Fn1 = Fn.subs(n, n + 1)
    spine = [list(Vn(k) * ONE) for k in range(1, 5)]
    check("CLOSED FORM [E]: V^n = [[0,2^{n-1},0],[0,2^n,0],[0,2^{n+1}-2,1]] "
          "(numeric n=1..16 AND symbolic induction F(n)*V = F(n+1), base "
          "F(1)=V); binary spine V^n 1 = (2^{n-1}, 2^n, 2^{n+1}-1) = "
          "(1,2,3),(2,4,7),(4,8,15),(8,16,31)",
          all(V**k == Vn(k) for k in range(1, 17))
          and sp.simplify(Fn * V - Fn1) == sp.zeros(3)
          and V == Vn(1)
          and sp.simplify(Fn * ONE
                          - sp.Matrix([2**(n - 1), 2**n, 2**(n + 1) - 1]))
          == sp.zeros(3, 1)
          and spine == [[1, 2, 3], [2, 4, 7], [4, 8, 15], [8, 16, 31]])

    # ---- 2. bilinear families ----
    o1Vn1 = sp.simplify((ONE.T * Fn * ONE)[0])
    o1Vna = sp.simplify((ONE.T * Fn * A)[0])
    aVna = sp.simplify((A.T * Fn * A)[0])
    aVn1 = sp.simplify((A.T * Fn * ONE)[0])
    check("BILINEAR FAMILIES [E]: 1^T V^n 1 = 7*2^{n-1}-1, 1^T V^n a = "
          "7*2^{n-1}, a^T V^n a = 11*2^{n-1}, a^T V^n 1 = 11*2^{n-1}-2 "
          "(all exact in n); at n=1 the four readouts = (6,7,9,11) = "
          "(|R^+(A_3)|, scalaron, N_fam^2, anchor amplitude)",
          o1Vn1 == 7 * 2**(n - 1) - 1 and o1Vna == 7 * 2**(n - 1)
          and aVna == 11 * 2**(n - 1) and aVn1 == 11 * 2**(n - 1) - 2
          and [(ONE.T * V * ONE)[0], (ONE.T * V * A)[0],
               (A.T * V * ONE)[0], (A.T * V * A)[0]] == [6, 7, 9, 11])

    # ---- 3. the recurring integers as V-power readouts ----
    check("GENERATOR READOUT [E]: 1^T V^2 1 = 13 = Delta_Q, 1^T V^3 1 = 27 = "
          "1^T R a, 1^T V^4 1 = 55 = quark numerator, 1^T V^4 a = 56 = "
          "dim 56_{E_7}; 11 = a^T V a is the anchor amplitude one level "
          "below the quark Pluecker norm",
          (ONE.T * V**2 * ONE)[0] == DELTA_Q
          and (ONE.T * V**3 * ONE)[0] == 27 == (ONE.T * R * A)[0]
          and (ONE.T * V**4 * ONE)[0] == 55
          and (ONE.T * V**4 * A)[0] == DIM_56_E7
          and (A.T * V * A)[0] == 11)

    # ---- 3b. binary spine reading (audit) ----
    s1 = list(V * ONE)
    s2 = list(V**2 * ONE)
    s3 = list(V**3 * ONE)
    s4 = list(V**4 * ONE)
    check("SPINE READING [C, audit]: the spine is FORCED by Spec(V)={0,1,2} "
          "(eigenvalue 2 doubles, eigenvalue 1 fixes slot 3); the carrier "
          "matches (1,2,3)=A_3 exponents, (2,4,7)=(|Z2|,|mu4|,7), "
          "(4,8,15)=(|mu4|,rank E_8,dim A_3), (8,16,31)=(rank E_8,dim S^+,"
          "2^g_car-1=248/8) are audit Lie/dimension matches (v95 typing)",
          s1 == [1, 2, 3] and s2 == [2, 4, 7]
          and s3 == [4, rankE8, 15]
          and s4 == [rankE8, dim_Splus, 2**g_car - 1]
          and 2**g_car - 1 == 248 // 8)

    # ---- 4. theta cross-link (audit raster) ----
    sig3 = lambda m: sum(d**3 for d in sp.divisors(m))
    check("THETA CROSS-LINK [C, audit]: E_8 shell degeneracies 240*sigma_3(n) "
          "= 240,2160,6720,17520; sigma_3(2)=9 = a^T V 1 = N_fam^2, "
          "sigma_3(3)=28 = 1^T V^3 a = det(I+R), sigma_3(5)=126 = local E_7 "
          "root shell (tfpt_3 lemma v) -- an audit raster, not a claim",
          [240 * sig3(k) for k in range(1, 5)] == [240, 2160, 6720, 17520]
          and sig3(2) == 9 == (A.T * V * ONE)[0] == N_fam**2
          and sig3(3) == 28 == (ONE.T * V**3 * A)[0] == (I3 + R).det()
          and sig3(5) == 126)

    return summary("v410 sheet generator V (binary compiler: V^n prints the spine)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
