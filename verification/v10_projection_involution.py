"""v10 -- The Q,Sigma projection-involution algebra (masses and transport from
one operator).

Backs the new structural finding integrated into tfpt_2: the phi0-mass-power
matrix K and the transport word-length matrix L are two sheet-readouts of one
parabolic projection Q on the residue matrix R, via the generation involution
Sigma = diag(1,-1,-1):

    K = R + Q*Sigma ,    L = R + Q*(I + Sigma) ,    Q = L - K .

This script verifies the whole algebra exactly (SymPy): the defining identities,
the factored characteristic polynomials, the cokernel/determinant ladder
(3,4,8,20) with product 1920 = |W(D5)|, the sheet-even/odd decompositions
Q_+,Q_-,K_+,K_-, the [Q,Sigma] / {Q,Sigma} spectra, and the EM-budget anchor
a^T K a = 41 with det(anchor block) = 10.
"""
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from tfpt_constants import check, summary, reset

t = sp.symbols('t')


def snf_diag(M):
    S = smith_normal_form(M, domain=sp.ZZ)
    return sorted(abs(int(S[i, i])) for i in range(M.shape[0]))


def run():
    reset()
    print("v10  Q,Sigma projection-involution algebra")

    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    W = sp.Matrix([[1, 0, 0], [1, 0, 0], [1, 0, 0]])
    L = R + 6 * W
    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    Q = L - K
    Sig = sp.diag(1, -1, -1)
    I = sp.eye(3)

    # --- defining identities ---
    check("Q = L - K = [[3,1,0],[3,2,0],[3,2,1]]",
          Q == sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]]))
    check("Sigma^2 = I", Sig * Sig == I)
    check("K = R + Q*Sigma", R + Q * Sig == K)
    check("L = R + Q*(I + Sigma)", R + Q * (I + Sig) == L)
    check("Q*(I + Sigma) = 6 W (first-generation winding = 2*N_fam)",
          Q * (I + Sig) == 6 * W)

    # --- factored characteristic polynomials ---
    check("chi_Q = (t-1)(t^2-5t+3)  -> carries (g_car=5, N_fam=3)",
          sp.factor(Q.charpoly(t).as_expr()) == (t - 1) * (t**2 - 5 * t + 3))
    check("chi_K = (t-1)(t^2-8t+4)  -> carries (h(D5)=8, |mu4|=4)",
          sp.factor(K.charpoly(t).as_expr()) == (t - 1) * (t**2 - 8 * t + 4))
    check("discriminant of Q-quadratic = 13 = |R(A3)|+1",
          5**2 - 4 * 3, 13, exact=True)
    check("discriminant of K-quadratic = 48 = Omega_adm",
          8**2 - 4 * 4, 48, exact=True)

    # --- cokernel / determinant ladder ---
    check("det(Q,K,R,L) = (3,4,8,20)",
          [int(Q.det()), int(K.det()), int(R.det()), int(L.det())],
          [3, 4, 8, 20], exact=True)
    check("coker SNF: Q->Z3, K->Z4, R->Z8, L->Z20",
          [snf_diag(Q)[-1], snf_diag(K)[-1], snf_diag(R)[-1], snf_diag(L)[-1]],
          [3, 4, 8, 20], exact=True)
    check("det Q * det K * det R * det L = 1920 = |W(D5)|",
          int(Q.det() * K.det() * R.det() * L.det()), 1920, exact=True)

    # --- sheet-even / odd decompositions ---
    Qp = sp.Rational(1, 2) * (Q + Sig * Q * Sig)
    Qm = sp.Rational(1, 2) * (Q - Sig * Q * Sig)
    Kp = sp.Rational(1, 2) * (K + Sig * K * Sig)
    Km = sp.Rational(1, 2) * (K - Sig * K * Sig)
    check("Spec(Q_+) = {1,2,3} = A3 exponents", sorted(Qp.eigenvals().keys()) == [1, 2, 3])
    check("det Q_+ = 6 = |R^+(A3)|", int(Qp.det()), 6, exact=True)
    check("chi_{Q_-} = t(t^2-3)  -> Q_- is a sqrt of N_fam=3",
          sp.factor(Qm.charpoly(t).as_expr()) == t * (t**2 - 3))
    check("Spec(K_+) = {0,4,5} = {top anchor, |mu4|, g_car}",
          sorted(Kp.eigenvals().keys()) == [0, 4, 5])
    check("chi_{K_-} = t(t^2-8)  -> K_- is a sqrt of h(D5)=8",
          sp.factor(Km.charpoly(t).as_expr()) == t * (t**2 - 8))

    # --- commutator / anticommutator with the sheet involution ---
    comm = Q * Sig - Sig * Q
    anti = Q * Sig + Sig * Q
    check("chi_[Q,Sigma] = t(t^2+12)  -> 12 = |R(A3)| = dim g_SM",
          sp.factor(comm.charpoly(t).as_expr()) == t * (t**2 + 12))
    check("Spec{Q,Sigma} = {6,-4,-2} = (|R^+(A3)|, -|mu4|, -|Z2|)",
          sorted(anti.eigenvals().keys()) == [-4, -2, 6])
    check("det{Q,Sigma} = 48 = Omega_adm", int(anti.det()), 48, exact=True)
    check("tr{Q,Sigma} = 0", int(anti.trace()), 0, exact=True)

    # --- EM budget 41 sits in the K anchor block ---
    a = sp.Matrix([1, 1, 2])
    one = sp.Matrix([1, 1, 1])
    check("a^T K a = 41 = 10 b1 (EM transport budget)", int((a.T * K * a)[0]), 41, exact=True)
    BK = sp.Matrix([[(one.T * K * one)[0], (one.T * K * a)[0]],
                    [(a.T * K * one)[0], (a.T * K * a)[0]]])
    check("K anchor block = [[25,29],[35,41]] (g_car^2, E8 exp 29, 5*7, 10 b1)",
          BK == sp.Matrix([[25, 29], [35, 41]]))
    check("det(K anchor block) = 10 = A_Lambda", int(BK.det()), 10, exact=True)
    return summary("v10 Q,Sigma algebra")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
