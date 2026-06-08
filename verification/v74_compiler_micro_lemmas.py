"""v74 -- compiler micro-lemmas (review synthesis): the spine quotient ladder, the K+xQ pencil
DIFFERENCE chain 2->16->48, the anchor-quadratic-form reading EM = mass-volume + one generation,
and the solar dual-anchor rank-one invariance mechanism.

All four are exact identities that compress scattered factors into the anchor a=(1,1,2) / the
(R,Q,K,L) operators -- the "fewer admissible invariants" discipline:

(1) Spine quotient ladder: the recurring factors 2/3,3/4,4/5,5/4,4/3 are adjacent quotients of
    the spine (|Z2|,N_fam,|mu4|,g_car)=(2,3,4,5).
(2) Pencil P(x)=det(K+xQ)=3x^3+7x^2+6x+4; endpoints (2,4,20,68); the consecutive DIFFERENCES are
    (2,16,48) = (|Z2|, dim S+, Omega_adm) = sheet -> one generation -> three generations.
(3) Anchor quadratic form B_K: 1^T K 1 = 25 = g_car^2 (mass volume), a^T K a = 41 = 10 b1 (EM
    budget); a^T K a - 1^T K 1 = 16 = dim S+ => EM budget = mass volume + one generation.
(4) Solar dual anchor: L = R + 6*1*e1^T (rank-one winding) and a^T R^-1 . 1 = 0, so by
    Sherman-Morrison a^T L^-1 = a^T R^-1 = (-1/2,-1/2,1): the winding deformation is invisible to
    the dual anchor -> the TBM symmetry vector is stable (the mechanism behind eps=q(A3)*phi0).
"""
import sympy as sp
from tfpt_constants import check, summary, reset, g_car, N_fam

x = sp.symbols('x')


def run():
    reset()
    print("v74  compiler micro-lemmas (spine quotients, pencil differences, anchor QF, solar dual anchor)")

    Z2, mu4 = 2, 4
    # (1) spine quotient ladder
    check("spine quotient ladder: (2/3,3/4,4/5,5/4,4/3) = (Z2/Nf, Nf/mu4, mu4/gcar, gcar/mu4, mu4/Nf)",
          (sp.Rational(Z2, N_fam), sp.Rational(N_fam, mu4), sp.Rational(mu4, g_car),
           sp.Rational(g_car, mu4), sp.Rational(mu4, N_fam))
          == (sp.Rational(2, 3), sp.Rational(3, 4), sp.Rational(4, 5), sp.Rational(5, 4), sp.Rational(4, 3)))
    c3 = 1 / (8 * sp.pi)
    check("the ladder feeds the seed/transport/glue: (4/3)c3=1/(6pi) (phi0 lead), (2/3)^6 (gap), "
          "q(D5)+q(A3)=5/4+3/4=2",
          sp.simplify(sp.Rational(4, 3) * c3 - 1 / (6 * sp.pi)) == 0
          and sp.Rational(2, 3)**6 == sp.Rational(64, 729)
          and sp.Rational(5, 4) + sp.Rational(3, 4) == 2)

    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    L = sp.Matrix([[7, 3, 0], [7, 5, 2], [8, 5, 3]])

    # (2) pencil difference chain
    P = sp.expand((K + x * Q).det())
    vals = [P.subs(x, k) for k in (-1, 0, 1, 2)]
    diffs = [vals[i + 1] - vals[i] for i in range(3)]
    check("pencil P(x)=det(K+xQ)=3x^3+7x^2+6x+4; endpoints (2,4,20,68)",
          P == 3 * x**3 + 7 * x**2 + 6 * x + 4 and vals == [2, 4, 20, 68])
    check("pencil DIFFERENCES (2,16,48) = (|Z2|, dim S+, Omega_adm) = sheet -> 1 gen -> 3 gens",
          diffs == [2, 16, 48])

    # (3) anchor quadratic form
    one = sp.Matrix([1, 1, 1]); a = sp.Matrix([1, 1, 2])
    v11 = (one.T * K * one)[0]; vaa = (a.T * K * a)[0]
    check("B_K anchor quadratic form: 1^TK1=25=g_car^2 (mass vol); a^TKa=41=10*b1 (EM budget)",
          v11 == 25 == g_car**2 and vaa == 41)
    check("a^TKa - 1^TK1 = 41-25 = 16 = dim S+  =>  EM budget = mass volume + one generation",
          vaa - v11 == 16)

    # (4) solar dual anchor rank-one invariance
    check("L = R + 6*1*e1^T (rank-one winding deformation)",
          L - R == 6 * one * sp.Matrix([[1, 0, 0]]))
    aR = a.T * R.inv(); aL = a.T * L.inv()
    check("a^T R^-1 . 1 = 0  =>  (Sherman-Morrison)  a^T L^-1 = a^T R^-1 = (-1/2,-1/2,1): winding "
          "invisible to dual anchor, TBM vector stable (mechanism for eps=q(A3)*phi0)",
          (aR * one)[0] == 0 and aR == aL == sp.Matrix([[sp.Rational(-1, 2), sp.Rational(-1, 2), 1]]))
    return summary("v74 compiler micro-lemmas")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
