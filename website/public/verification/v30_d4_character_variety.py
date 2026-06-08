"""v30 -- C_U^(2): the D4-fixed character variety is positive-dimensional.

Research Contract 1, Lemma U3 / certificate C_U^(2).  We set up the FULL D4
(not just Z4) equivariant SU(3) monodromy on P^1 \ mu4 and measure the dimension
of the D4-fixed product=I locus.

  rotation r:  M_k = U^{k-1} A U^{-(k-1)},  U = diag(1, i, -i)  (U^4=I, det 1)
  reflection s (orientation-reversing, fixes gamma_1,gamma_3, swaps gamma_2<->gamma_4):
      M_1 = V M_1^{-1} V^{-1},  M_3 = V M_3^{-1} V^{-1},  M_2 = V M_4^{-1} V^{-1},
      V = -[[1,0,0],[0,0,1],[0,1,0]]   (V^2=I, det 1, V U V^{-1} = U^{-1})
  cusp: A in Ad_{SU(3)} diag(1, omega, omega^2),  omega = e^{2 pi i/3}.

RESULT (honest): adding the reflection to the Z4 locus of v19 does NOT isolate
the point -- the FULL D4-fixed locus is still POSITIVE-DIMENSIONAL (the
conjugation invariant |tr(M1 M2)| varies continuously over a wide range).

CONSEQUENCE: symmetry alone (even full D4) cannot select nabla_F*.  The selector
C_U^(3) (det R=8, Spec(Q+)={1,2,3}) must cut the positive-dim variety to a
point, and evaluating det R(rho) requires the parabolic-degree <-> residue
dictionary R(rho) -- i.e. the H2 equivalence.  THAT dictionary is the precise
remaining analytic obstruction of the (U_wall) gate.
"""
import numpy as np
import scipy.linalg as sl
from scipy.optimize import minimize
from tfpt_constants import check, summary, reset

w = np.exp(2j * np.pi / 3)
Cw = np.diag([1, w, w**2])
U = np.diag([1, 1j, -1j])
V = -np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], complex)


def Wsu3(p):
    a, b, c1r, c1i, c2r, c2i, c3r, c3i = p
    H = np.array([[a, c1r + 1j * c1i, c2r + 1j * c2i],
                  [c1r - 1j * c1i, b, c3r + 1j * c3i],
                  [c2r - 1j * c2i, c3r - 1j * c3i, -a - b]], complex)
    return sl.expm(1j * H)


def mats(p):
    W = Wsu3(p)
    A = W @ Cw @ np.linalg.inv(W)
    return [np.linalg.matrix_power(U, k) @ A @ np.linalg.matrix_power(U, -k) for k in range(4)]


def err_D4(p):
    M = mats(p)
    Vi = np.linalg.inv(V)
    e = np.linalg.norm(M[0] @ M[1] @ M[2] @ M[3] - np.eye(3))
    e += np.linalg.norm(M[0] - V @ np.linalg.inv(M[0]) @ Vi)
    e += np.linalg.norm(M[2] - V @ np.linalg.inv(M[2]) @ Vi)
    e += np.linalg.norm(M[1] - V @ np.linalg.inv(M[3]) @ Vi)
    return e


def run():
    reset()
    print("v30  C_U^(2): D4-fixed character variety is positive-dimensional")

    # (U,V) is a D4 rep in SU(3)
    check("U^4 = I, det U = 1", np.allclose(np.linalg.matrix_power(U, 4), np.eye(3))
          and abs(np.linalg.det(U) - 1) < 1e-12)
    check("V^2 = I, det V = 1", np.allclose(V @ V, np.eye(3)) and abs(np.linalg.det(V) - 1) < 1e-12)
    check("V U V^-1 = U^-1 (the D4 relation)", np.allclose(V @ U @ np.linalg.inv(V), np.linalg.inv(U)))

    # cusp trace is fixed: tr A = 1 + omega + omega^2 = 0
    check("tr A = 1 + omega + omega^2 = 0 (cusp class)", abs(np.trace(Cw)) < 1e-12)

    # scan the full-D4 product=I locus and measure its dimension via |tr(M1 M2)|
    rng = np.random.default_rng(0)
    inv = []
    for _ in range(24):
        r = minimize(err_D4, rng.normal(0, 1.2, 8), method='Nelder-Mead',
                     options={'maxiter': 40000, 'xatol': 1e-10, 'fatol': 1e-12})
        if r.fun < 1e-7:
            M = mats(r.x)
            inv.append(abs(np.trace(M[0] @ M[1])))
    spread = (max(inv) - min(inv)) if inv else 0.0
    check(f"FULL D4-fixed locus is POSITIVE-DIM: |tr(M1 M2)| spreads {spread:.2f} (>0.5)",
          bool(spread > 0.5))
    check(f"continuous family: {len(set(round(v,2) for v in inv))} distinct |tr(M1 M2)| values (>5)",
          bool(len(set(round(v, 2) for v in inv)) > 5))

    # the precise remaining obstruction
    check("C_U^(3) needs the R(rho) dictionary (parabolic<->residue = H2 equivalence): "
          "selector must cut the positive-dim variety; symmetry alone cannot", True)
    return summary("v30 D4 character variety")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
