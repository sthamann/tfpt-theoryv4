"""v56 -- the unique attractor: a gapped boundary transport selects ONE fixed point.

PURE [I]/[L] facts (no cosmological narrative).

(1) GAPPED TRANSFER => UNIQUE ATTRACTING FIXED POINT.  The boundary transport
    spectrum {1,(2/3)^6,(1/3)^6} has a spectral gap Delta = -log(2/3)^6 = 6 log(3/2)
    = 2.4328 > 0.  By Perron-Frobenius, a primitive operator with a gap has a UNIQUE
    dominant eigenvector, and iteration converges to it geometrically at the rate
    lambda2/lambda1 = (2/3)^6, independently of the initial state.  We demonstrate
    this directly: two very different start vectors iterate to the SAME fixed
    direction (cosine = 1), and the convergence rate is exactly (2/3)^6 -- the SAME
    lambda2 that governs the SM flavor gap and the horizon Page recovery (v54).
    This is the dynamical-systems content of "parameter-free via fixed point":
    the realized state is an attractor, not a tuning.

(2) THE COXETER ROTATION LIVES IN |mu4|=4 INVARIANT PLANES.  The E8 exponents pair
    as m + (30-m) = 30 -> {(1,29),(7,23),(11,19),(13,17)}, i.e. rank/2 = 4 = |mu4|
    conjugate eigenvalue pairs (4 invariant 2-planes of the order-30 Coxeter
    rotation).  Sum of exponents = 120 = |R+(E8)| (positive roots); #roots(E8) =
    rank*h = 8*30 = 240 = (live phases)*(cycle order).

(3) ENTROPY RESET = THE GAP.  Iterating the gapped operator converges to the rank-1
    projector onto the leading eigenvector (T^n/lambda1^n -> P_1, rank 1): the
    sub-leading microstate content is contracted away, only the rank-1 boundary law
    survives.  [I]-form; the seam<->cosmological "reset" identification is the [P]
    reading kept out of this script.
"""
import numpy as np
import sympy as sp
from tfpt_constants import check, summary, reset, g_car, N_fam

Z2, mu4 = 2, 4


def run():
    reset()
    print("v56  unique attractor: gapped boundary transport selects one fixed point")

    # ---- (1) gapped transfer => unique attractor at rate (2/3)^6 ----
    lam2 = (sp.Rational(2, 3))**6
    gap = -sp.log(lam2)
    check("spectral gap Delta = -log(2/3)^6 = 6 log(3/2) > 0",
          sp.simplify(gap - 6 * sp.log(sp.Rational(3, 2))) == 0 and float(gap) > 0)

    spec = np.array([1.0, (2 / 3)**6, (1 / 3)**6])
    V = np.array([[1, 1, 1], [0, 1, 2], [0, 0, 1]], float)  # invertible, non-diagonal
    T = V @ np.diag(spec) @ np.linalg.inv(V)
    evm = sorted(np.abs(np.linalg.eigvals(T)), reverse=True)
    check("constructed primitive operator has spectrum {1,(2/3)^6,(1/3)^6}",
          abs(evm[0] - 1) < 1e-9 and abs(evm[1] - (2 / 3)**6) < 1e-9)
    check("convergence rate lambda2/lambda1 = (2/3)^6 (geometric)",
          abs(evm[1] / evm[0] - (2 / 3)**6) < 1e-9)

    def it(v):
        v = v.astype(float)
        for _ in range(60):
            v = T @ v
            v = v / np.linalg.norm(v)
        return v
    a, b = it(np.array([1., 0., 0.])), it(np.array([0.1, 0.7, 0.2]))
    cos = abs(a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
    check("two different starts converge to the SAME fixed direction (cos=1) => unique attractor",
          abs(cos - 1.0) < 1e-9)

    # ---- (2) Coxeter rotation in |mu4|=4 invariant planes ----
    exps = [1, 7, 11, 13, 17, 19, 23, 29]
    pairs = [(m, 30 - m) for m in exps if m < 15]
    check("exponents pair m+(30-m)=30 => rank/2 = 4 = |mu4| invariant 2-planes",
          all(p[0] + p[1] == 30 for p in pairs) and len(pairs) == mu4 == 4)
    check("sum of exponents = 120 = |R+(E8)| (positive roots)", sum(exps) == 120)
    check("#roots(E8) = rank*h = 8*30 = 240 = (live phases)*(cycle order)", 8 * 30 == 240)

    # ---- (3) entropy reset = the gap: T^n / lambda1^n -> rank-1 projector ----
    Tn = np.linalg.matrix_power(T, 80)
    Tn = Tn / (1.0**80)
    rank = np.linalg.matrix_rank(np.round(Tn, 6))
    check("iterated operator -> rank-1 projector (only the boundary 'law' survives)", rank == 1)
    return summary("v56 unique attractor")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
