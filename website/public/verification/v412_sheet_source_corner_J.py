"""v412 -- The sheet source corner J.  The determinant surface has two
s-independent iso-volume walls (v135): t = -1 (det = 4 = |mu4|, carries K)
and t = -2 (det = 2 = |Z2|).  The operator that sits on the Z2 wall of the
sheet axis, J := M(1,-2) = C - 2V, was so far unnamed; it is a fourth
distinguished corner that carries sheet, family, A_3, E_8 Coxeter, the SM
dimension and the D_5 root budget at once.  [E] algebra, [C] reading.

  [E] 1. THE Z2 WALL CARRIES J.  On M(s,t) = R + Q diag(s,t,t) (v94/v95) the
         t = -2 wall is det M(s,-2) = 2 = |Z2| for ALL s (v135).  The sheet
         axis s = 1 meets it at
             J := M(1,-2) = C - 2V = [[4,1,0],[4,1,2],[5,1,1]],
         completing the four-point sheet axis J, K, C, F = M(1, -2..1).
  [E] 2. CLEAN CHARACTERISTIC POLYNOMIAL.
             chi_J = lambda^3 - 6 lambda^2 + 3 lambda - 2
                  => (tr, e_2, det) = (6, 3, 2)
                   = (|R^+(A_3)|, N_fam, |Z2|).
  [E] 3. RESOLVENT / ANCHOR READOUTS.
             a^T J a   = 30  = h(E_8),
             det(I + J) = 12 = dim g_SM = chi_{E_8}(i),
             det(2I + J) = 40 = |R(D_5)|.

HONEST TYPING.  The wall is v135; the NEW content is the named operator J and
its exact invariants -- all [E].  The Lie readings (6,3,2)=(A_3^+, family, Z2),
30=h(E_8), 12=dim g_SM, 40=|R(D_5)| are audit-level matches in the same spirit
as the G_2/F_4 shadows of v95/v218 -- recorded as [C], not promoted.
Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
C = R + Q * sp.diag(1, 0, 0)
V = Q * sp.diag(0, 1, 1)
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
I3 = sp.eye(3)

H_E8 = 30
DIM_GSM = 12
R_D5 = 40
RP_A3 = 6


def run():
    reset()
    print("v412 sheet source corner J = M(1,-2) on the Z2 wall")

    s, t, lam = sp.symbols('s t lambda')
    detM = sp.expand((R + Q * sp.diag(s, t, t)).det())
    J = C - 2 * V

    check("THE Z2 WALL CARRIES J [E]: det M(s,-2) = 2 = |Z2| for ALL s "
          "(v135); the sheet axis s=1 meets it at J := M(1,-2) = C - 2V = "
          "[[4,1,0],[4,1,2],[5,1,1]], completing the sheet axis J,K,C,F = "
          "M(1,-2..1)",
          sp.expand(detM.subs(t, -2)) == 2
          and J == (R + Q * sp.diag(1, -2, -2))
          and J == sp.Matrix([[4, 1, 0], [4, 1, 2], [5, 1, 1]]))

    chiJ = sp.expand((lam * I3 - J).det())
    check("CLEAN CHARACTERISTIC POLY [E]: chi_J = lambda^3 - 6 lambda^2 + "
          "3 lambda - 2 => (tr, e_2, det) = (6, 3, 2) = (|R^+(A_3)|, N_fam, "
          "|Z2|)",
          chiJ == lam**3 - 6 * lam**2 + 3 * lam - 2
          and J.trace() == RP_A3 and J.det() == 2
          and chiJ.coeff(lam, 1) == N_fam)

    check("RESOLVENT / ANCHOR READOUTS [E]: a^T J a = 30 = h(E_8), "
          "det(I+J) = 12 = dim g_SM = chi_{E_8}(i), det(2I+J) = 40 = "
          "|R(D_5)| (readings [C], audit-typed like the G_2/F_4 shadows)",
          (A.T * J * A)[0] == H_E8
          and (I3 + J).det() == DIM_GSM
          and (2 * I3 + J).det() == R_D5)

    return summary("v412 source corner J (chi_J=(6,3,2), a^TJa=30, "
                   "det(I+J)=12, det(2I+J)=40)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
