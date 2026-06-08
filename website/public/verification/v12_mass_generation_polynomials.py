"""v12 -- Sector and generation polynomials of K, and the anchor-block ladder.

Backs the per-sector / per-generation reading of the mass-power matrix K: each
row (up/down/lepton) and each column (generation) of K is a clean integer
polynomial whose roots are compiler numbers, and the anchor bilinear blocks of
Q,K,R,L form the ladder det = (9,10,16,40).
"""
import sympy as sp
from tfpt_constants import check, summary, reset

t = sp.symbols('t')


def cpoly(vals):
    """Monic cubic with the given integer roots, expanded."""
    return sp.expand((t - vals[0]) * (t - vals[1]) * (t - vals[2]))


def run():
    reset()
    print("v12  sector / generation polynomials and anchor ladder")

    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    L = R + 6 * sp.Matrix([[1, 0, 0], [1, 0, 0], [1, 0, 0]])
    one, a = sp.Matrix([1, 1, 1]), sp.Matrix([1, 1, 2])

    # row sums (sector budget) and column sums (generation budget)
    check("K row sums (sector) = (6,9,10) = (|R^+(A3)|, N_fam^2, A_Lambda)",
          list(K * one), [6, 9, 10], exact=True)
    check("K col sums (generation) = (13,8,4) = (|R(A3)|+N_Phi, h(D5), |mu4|)",
          list((one.T * K).T), [13, 8, 4], exact=True)

    # sector polynomials (rows of K, as root sets)
    check("up sector (4,2,0): P_u = t(t-2)(t-4)  [6=|R^+(A3)|, 8=h(D5)]",
          cpoly([4, 2, 0]) == t**3 - 6 * t**2 + 8 * t)
    check("down sector (4,3,2): P_d = (t-2)(t-3)(t-4)  [9, 24=|W(A3)|, 26=dim26_F4]",
          cpoly([4, 3, 2]) == t**3 - 9 * t**2 + 26 * t - 24)
    check("lepton sector (5,3,2): P_l = (t-2)(t-3)(t-5)  [10=A_L, 30=h(E8), 31]",
          cpoly([5, 3, 2]) == t**3 - 10 * t**2 + 31 * t - 30)

    # generation polynomials (columns of K)
    check("gen-1 (4,4,5): (t-4)^2(t-5)  [13, 56=dim56_E7, 80=dim A8]",
          cpoly([4, 4, 5]) == t**3 - 13 * t**2 + 56 * t - 80)
    check("gen-2 (2,3,3): (t-2)(t-3)^2  [8=h(D5), 21=3*7, 18=N_fam|R^+(A3)|]",
          cpoly([2, 3, 3]) == t**3 - 8 * t**2 + 21 * t - 18)
    check("gen-3 (0,2,2): t(t-2)^2  [4=|mu4|]",
          cpoly([0, 2, 2]) == t**3 - 4 * t**2 + 4 * t)

    # anchor bilinear blocks: det ladder (9,10,16,40)
    def block(M):
        return sp.Matrix([[(one.T * M * one)[0], (one.T * M * a)[0]],
                          [(a.T * M * one)[0], (a.T * M * a)[0]]])
    dets = [int(block(Q).det()), int(block(K).det()),
            int(block(R).det()), int(block(L).det())]
    check("anchor-block det ladder (Q,K,R,L) = (9,10,16,40) "
          "= (N_fam^2, A_Lambda, dim S+, |R(D5)|)",
          dets, [9, 10, 16, 40], exact=True)
    return summary("v12 sector/generation polynomials")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
