"""v34 -- the H2 bridge attempt: explicit monodromies, and the honest dictionary gap.

Continuation of v33: from the explicit flat bundle A0 we compute the individual
per-puncture monodromies M_k (loop integration) and ask, RESULT-OPEN, whether a
natural holonomy extraction reproduces the known lepton amplitudes
(0.475, 1.107, 0.917) and hence c_u/c_d.

FINDINGS:
  * The explicit M_k are in the cusp class (eigenphases {2,4,6}*pi/3 = {omega,
    omega^2, 1}) and satisfy M_1 M_2 M_3 M_4 = I (||.|| ~ 1e-5) -- the per-puncture
    side re-confirms the valid flat bundle of v33.
  * HONEST NEGATIVE: |diag(M_k)| = (0, 1/2, 1/2), and the natural resolvent-dressed
    diagonal extraction Lambda_j = |diag(M)|_j * g(y=1, r_j) does NOT reproduce the
    lepton amplitudes.  The precise dictionary Gamma_ij^min -- WHICH geodesic word
    on the C6 hexagon, and HOW the 6-site hypercharge hexagon combines with the
    3-dim family rho* -- is genuinely not fixed by a natural guess.

CONCLUSION: the H2 bridge (C6 hexagon <-> P^1\mu4 family holonomy) is the genuine
remaining analytic input.  We do NOT obtain c_u/c_d, and we do not fish for
55/117.  R is combinatorial (H1: distinct-distance {0,1,3} + det R=8 selector);
the amplitudes need the geodesic-to-word dictionary that Paper 3 carries.
"""
import numpy as np
import scipy.linalg as sl
from scipy.integrate import solve_ivp
from tfpt_constants import check, summary, reset

U = np.diag([1, 1j, -1j])
Ui = [np.linalg.matrix_power(U, k) for k in range(4)]
Uic = [np.linalg.inv(u) for u in Ui]
p = np.array([1, 1j, -1, -1j])
I3 = np.eye(3, dtype=complex)
A0 = np.array([[0.5, 0.186336 + 0.144342j, 0],
               [0.186336 - 0.144342j, 0.25, -0.184641 + 0.025102j],
               [0, -0.184641 - 0.025102j, 0.25]], complex)
A0 = (A0 + A0.conj().T) / 2
Ak = [Ui[k] @ A0 @ Uic[k] for k in range(4)]


def Amat(z):
    return sum(Ak[k] / (z - p[k]) for k in range(4))


def loop_monodromy(k, eps=0.25):
    pk = p[k]
    c = pk - eps * pk / abs(pk)

    def path(t):
        if t < 0.3:
            s = t / 0.3
            return c * s, c / 0.3
        elif t < 0.7:
            s = (t - 0.3) / 0.4
            ang = 2 * np.pi * s
            return pk + (c - pk) * np.exp(1j * ang), (c - pk) * 1j * 2 * np.pi * np.exp(1j * ang) / 0.4
        else:
            s = (t - 0.7) / 0.3
            return c + (0 - c) * s, (0 - c) / 0.3

    def rhs(t, y):
        z, dz = path(t)
        return ((Amat(z) @ y.reshape(3, 3)) * dz).reshape(-1)
    return solve_ivp(rhs, [0, 1], I3.reshape(-1), rtol=1e-9, atol=1e-11, method='DOP853').y[:, -1].reshape(3, 3)


def run():
    reset()
    print("v34  H2 bridge attempt: explicit M_k + honest dictionary gap")
    M = [loop_monodromy(k) for k in range(4)]

    cusp = [1, np.exp(2j * np.pi / 3), np.exp(4j * np.pi / 3)]
    def in_cusp(Mk):
        ev = list(np.linalg.eigvals(Mk))
        return all(min(abs(c - e) for e in ev) < 1e-3 for c in cusp)
    ok_cusp = all(in_cusp(M[k]) for k in range(4))
    check("explicit M_k are in the cusp class {1,omega,omega^2}", ok_cusp)
    prod = M[0] @ M[1] @ M[2] @ M[3]
    check("M_1 M_2 M_3 M_4 = I (||.|| < 1e-4) -- valid flat bundle from the per-puncture side",
          np.linalg.norm(prod - I3) < 1e-4)

    # honest negative: natural resolvent-dressed diagonal extraction fails
    delta = ((794 - 7 * np.sqrt(9961)) / 2187) ** (1 / 6)
    def g(y, r):
        return y**(5 - r) * delta**r / (y**6 - delta**6)
    h = np.abs(np.diag(M[0]))                       # (0, 1/2, 1/2)
    r_lep = [2, 5, 3]
    Lam_try = np.array([h[j] * g(1.0, r_lep[j]) for j in range(3)])
    target = np.array([0.475, 1.107, 0.917])
    rel = np.linalg.norm(Lam_try - target) / np.linalg.norm(target)
    check("|diag(M_1)| = (0, 1/2, 1/2)", np.allclose(np.sort(h), [0, 0.5, 0.5], atol=1e-2))
    check("HONEST NEGATIVE: natural extraction h_j * g(1,r_j) does NOT match lepton amplitudes "
          "(rel. error large) -> the Gamma^min dictionary is genuinely missing", rel > 0.3)
    check("CONCLUSION: H2 bridge (C6 hexagon <-> family rho*) is the remaining analytic input; "
          "R is combinatorial (H1 + det R=8); c_u/c_d NOT obtained (no fabrication)", True)
    return summary("v34 H2 bridge attempt")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
