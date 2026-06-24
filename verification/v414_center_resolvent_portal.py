"""v414 -- The center C is a resolvent portal G_2 -> F_4 -> E_8.  The center of
the Sheet Diamond (C = M(1,0), v95) is the t = 0 evaluation of the sheet
generator V; its shifted determinants climb the exceptional resolvent ladder
14 -> 52 -> 120 = (dim G_2, dim F_4, |R^+(E_8)|).  [E] algebra, [C] reading.

  [E] 1. CENTER INVARIANTS (anchored to v95):
             tr C = 12 = dim g_SM = chi_{E_8}(i),
             det C = 14 = dim G_2,
             sum_{ij} C_{ij} = 31 = 2^{g_car} - 1 = 248/8.
  [E] 2. RESOLVENT LADDER.  The shifted determinants give
             det(C)      = 14  = dim G_2,
             det(I + C)  = 52  = dim F_4,
             det(2I + C) = 120 = |R^+(E_8)|,
         i.e. the exceptional shell ladder G_2 -> F_4 -> E_8^+ as the
         resolvent of one operator C at shifts 0, 1, 2.

HONEST TYPING.  tr C, det C and sum C are the v95 center invariants
(cross-cited, not re-claimed); the NEW content is the resolvent ladder
det(C + kI) for k = 0,1,2.  All values are exact [E]; the
"G_2 -> F_4 -> E_8 portal" reading is [C], audit-typed exactly like the G_2
center / F_4 shadow of v95/v218.  Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
C = R + Q * sp.diag(1, 0, 0)
ONE = sp.Matrix([1, 1, 1])
I3 = sp.eye(3)

DIM_GSM = 12
DIM_G2 = 14
DIM_F4 = 52
RP_E8 = 120


def run():
    reset()
    print("v414 center resolvent portal G_2 -> F_4 -> E_8")

    check("CENTER INVARIANTS [E] (v95): tr C = 12 = dim g_SM = chi_{E_8}(i), "
          "det C = 14 = dim G_2, sum C = 31 = 2^g_car - 1 = 248/8",
          C.trace() == DIM_GSM and C.det() == DIM_G2
          and (ONE.T * C * ONE)[0] == 31 == 2**g_car - 1 == 248 // 8)

    check("RESOLVENT LADDER [E]: det(C) = 14 = dim G_2, det(I+C) = 52 = "
          "dim F_4, det(2I+C) = 120 = |R^+(E_8)| -- the exceptional shell "
          "ladder G_2 -> F_4 -> E_8^+ as det(C + kI), k = 0,1,2 (reading [C], "
          "audit-typed)",
          C.det() == DIM_G2 and (I3 + C).det() == DIM_F4
          and (2 * I3 + C).det() == RP_E8)

    return summary("v414 center resolvent portal (14 -> 52 -> 120)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
