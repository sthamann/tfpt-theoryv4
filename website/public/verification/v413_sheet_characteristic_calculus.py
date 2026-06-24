"""v413 -- The sheet axis is a discrete characteristic-difference calculator.
On the sheet axis M_t = C + tV (v95/v218) the three elementary-symmetric
coefficients of the characteristic polynomial encode the carrier atoms not as
VALUES but as DIFFERENCE ORDERS, and the anchor energy advances in steps of
the amplitude 11 = a^T V a (v410).  [E] algebra, [C] reading.

  [E] 1. ELEMENTARY-SYMMETRIC CALCULUS.  chi_{M_t} = lambda^3 - e_1 lambda^2 +
         e_2 lambda - e_3 with
             e_1(t) = 3t + 12,
             e_2(t) = 2t^2 + 15t + 25,
             e_3(t) = det M_t = 4t^2 + 14t + 14,
         so the carrier atoms appear as difference orders:
             Delta e_1   = 3 = N_fam        (first difference, linear trace),
             Delta^2 e_2 = 4 = |mu4|        (second difference of the
                                             surface coefficient),
             Delta^2 e_3 = 8 = rank E_8     (second difference of the volume;
                                             the curvature already in v218/v224).
         The NEW content here is the full triple (e_1, e_2, e_3) calculus:
         N_fam -> |mu4| -> rank E_8 as a discrete derivative ladder.
  [E] 2. ANCHOR-ENERGY LADDER.  The anchor energy is exactly linear with the
         amplitude 11 = a^T V a (v410):
             a^T M_t a = 52 + 11 t,
             30 --(+11)--> 41 --(+11)--> 52 --(+11)--> 63,
         the four steps reading (h(E_8), 10 b_1, dim F_4, 7 N_fam^2): the 11 is
         the STEP of the anchor energy along the sheet axis, not just the quark
         Pluecker norm.
  [E] 3. THE FOUR-ROW SHEET AXIS J,K,C,F = M(1, -2..1):
             t=-2 J: (tr,e_2,det)=(6,3,2),  a^T M a = 30
             t=-1 K: (9,12,4),              41
             t= 0 C: (12,25,14),            52
             t=+1 F: (15,42,32),            63

HONEST TYPING.  All coefficients/differences are exact [E]; Delta^2 e_3 = 8
overlaps the v218/v224 sheet-axis curvature and is cross-cited, not re-claimed.
The atom/Lie readings (10 b_1 = 41, dim F_4 = 52, 7 N_fam^2 = 63) are [C],
audit-typed.  Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, rankE8, b1

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
C = R + Q * sp.diag(1, 0, 0)
V = Q * sp.diag(0, 1, 1)
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])

MU4 = 4
H_E8 = 30
DIM_F4 = 52


def run():
    reset()
    print("v413 sheet axis as a characteristic-difference calculator")

    t, lam = sp.symbols('t lambda')
    Mt = C + t * V
    chi = sp.Poly((lam * sp.eye(3) - Mt).det(), lam)
    e1 = sp.expand(-chi.nth(2))
    e2 = sp.expand(chi.nth(1))
    e3 = sp.expand(-chi.nth(0))
    d1 = lambda f: sp.expand(f.subs(t, t + 1) - f)

    check("ELEMENTARY-SYMMETRIC CALCULUS [E]: e_1(t)=3t+12, e_2(t)=2t^2+15t+25, "
          "e_3(t)=det M_t=4t^2+14t+14 => Delta e_1 = 3 = N_fam, Delta^2 e_2 = "
          "4 = |mu4|, Delta^2 e_3 = 8 = rank E_8 (the e_3 curvature cross-cited "
          "to v218/v224; the full (e_1,e_2,e_3) ladder is the new content)",
          e1 == 3 * t + 12 and e2 == 2 * t**2 + 15 * t + 25
          and e3 == 4 * t**2 + 14 * t + 14
          and d1(e1) == N_fam and d1(d1(e2)) == MU4 and d1(d1(e3)) == rankE8)

    energy = sp.expand((A.T * Mt * A)[0])
    check("ANCHOR-ENERGY LADDER [E]: a^T M_t a = 52 + 11 t (step = 11 = "
          "a^T V a, v410); 30 -> 41 -> 52 -> 63 reads (h(E_8), 10 b_1, "
          "dim F_4, 7 N_fam^2) -- the 11 is the STEP of the anchor energy "
          "along the sheet axis",
          energy == 52 + 11 * t
          and [int(energy.subs(t, tv)) for tv in (-2, -1, 0, 1)]
          == [H_E8, int(10 * b1), DIM_F4, 7 * N_fam**2]
          and int(10 * b1) == 41 and 7 * N_fam**2 == 63)

    rows = {}
    for tv, name in [(-2, 'J'), (-1, 'K'), (0, 'C'), (1, 'F')]:
        Mv = C + tv * V
        rows[name] = (Mv.trace(), int(e2.subs(t, tv)), Mv.det(),
                      int((A.T * Mv * A)[0]))
    check("FOUR-ROW SHEET AXIS J,K,C,F = M(1,-2..1): (tr,e_2,det)/a^TMa = "
          "(6,3,2)/30, (9,12,4)/41, (12,25,14)/52, (15,42,32)/63",
          rows['J'] == (6, 3, 2, 30) and rows['K'] == (9, 12, 4, 41)
          and rows['C'] == (12, 25, 14, 52) and rows['F'] == (15, 42, 32, 63))

    return summary("v413 sheet characteristic calculus (3->4->8 differences, "
                   "anchor energy 52+11t)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
