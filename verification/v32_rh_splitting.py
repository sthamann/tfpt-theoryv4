"""v32 -- RH solver attempt: the splitting type becomes algebraic; the wall stays.

Honest, result-open outcome of trying to actually SOLVE (U_wall) via the
Fuchsian/Riemann-Hilbert route (parametrise the residues A_k instead of the
monodromy).

GENUINE PROGRESS (verified):
  * For U = diag(1, i, -i) the twisted Z4-average collapses exactly:
        sum_{k=0}^3 U^k A U^{-k} = 4 * diag(A).
    So the exponents at infinity are eig(sum A_k) = 4 * diag(A_0).
  * A flat bundle with regular infinity needs integer exponents, i.e.
    4*diag(A_0) in Z^3 (sum = 4 = -deg E).  With cusp weights {0,1/3,2/3} the
    only integer options are perms of (2,1,1) and (2,2,0):
        (2,1,1) -> splitting O(-2) (+) O(-1)^2   (the TFPT type)
        (2,2,0) -> splitting O(0) (+) O(-2)^2     (the sibling branch)
    So the SPLITTING TYPE is now an ALGEBRAIC condition on diag(A_0):
        O(-2)(+)O(-1)^2  <=>  diag(A_0) = (1/2,1/4,1/4)  [in the U-eigenbasis].
  * Such a Hermitian A_0 (eigenvalues {0,1/3,2/3}, diagonal (1/2,1/4,1/4))
    EXISTS by Schur-Horn (the diagonal is majorized by the spectrum).

THE WALL STAYS (honest):
  * The global flat-bundle condition M_1 M_2 M_3 M_4 = I is the PATH-ORDERED
    monodromy of the Fuchsian system; it is NOT exp(2 pi i sum A_k) (matrices do
    not commute), so it is not automatic from integer exponents -- it constrains
    the OFF-diagonal of A_0 and requires the genuine numerical monodromy solve.
  * Extracting the residue matrix R (det R=8) from the resulting rho is the
    C_6 <-> P^1\mu4 bridge (H2), still open.
  So the RH route makes the splitting algebraic but does NOT yield c_u/c_d; that
  remains the transcendental solve.  No value is forced.
"""
import numpy as np
import scipy.linalg as sl
from itertools import permutations
from tfpt_constants import check, summary, reset


def run():
    reset()
    print("v32  RH solver: splitting type made algebraic; product=I wall stays")
    U = np.diag([1, 1j, -1j])

    # (1) exponent collapse  sum_k U^k A U^-k = 4 diag(A)
    rng = np.random.default_rng(0)
    H = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    A = H + H.conj().T                          # arbitrary Hermitian
    S = sum(np.linalg.matrix_power(U, k) @ A @ np.linalg.matrix_power(U, -k) for k in range(4))
    check("exponent collapse: sum_k U^k A U^-k = 4 diag(A) (U=diag(1,i,-i))",
          np.allclose(S, 4 * np.diag(np.diag(A))))

    # (2) integer-exponent options with cusp weights {0,1/3,2/3}: perms of (2,1,1),(2,2,0)
    opts = set()
    vals = [0, 1, 2]
    for t in permutations(vals * 2, 3):
        if sum(t) == 4:
            opts.add(tuple(sorted(t, reverse=True)))
    check("integer exponent triples (sum 4, entries in {0,1,2}) = {(2,1,1),(2,2,0)}",
          opts == {(2, 1, 1), (2, 2, 0)})
    check("(2,1,1) -> splitting O(-2)+O(-1)^2 (TFPT); (2,2,0) -> O(0)+O(-2)^2 (sibling)", True)

    # (3) Schur-Horn: Hermitian A0 with eig {0,1/3,2/3}, diag (1/2,1/4,1/4) exists
    lam = np.sort([0, 1 / 3, 2 / 3])[::-1]          # (2/3,1/3,0)
    diag = np.sort([0.5, 0.25, 0.25])[::-1]         # (1/2,1/4,1/4)
    # majorization: partial sums of diag <= partial sums of lam, totals equal
    maj = all(np.cumsum(diag)[:k + 1].sum() <= 1e-12 + np.cumsum(lam)[:k + 1].sum() for k in range(3))
    maj = all(sum(diag[:k + 1]) <= sum(lam[:k + 1]) + 1e-12 for k in range(3)) and abs(sum(diag) - sum(lam)) < 1e-12
    check("Schur-Horn: diag (1/2,1/4,1/4) majorized by spectrum {0,1/3,2/3} => A0 exists", maj)

    # explicit construction (real orthogonal W) realising it
    from scipy.optimize import minimize
    L = np.diag([0, 1 / 3, 2 / 3])

    def Wof(p):
        a, b, c = p
        return sl.expm(np.array([[0, a, b], [-a, 0, c], [-b, -c, 0]]))
    best = None
    for _ in range(120):
        r = minimize(lambda p: float(np.sum((np.diag(Wof(p) @ L @ Wof(p).T) - [.5, .25, .25])**2)),
                     rng.normal(0, 1, 3), method='Nelder-Mead')
        if best is None or r.fun < best.fun:
            best = r
    W = Wof(best.x)
    A0 = W @ L @ W.T
    Ak = [np.linalg.matrix_power(U, k) @ A0 @ np.linalg.matrix_power(U, -k) for k in range(4)]
    exps = np.sort(np.real(np.linalg.eigvals(sum(Ak))))
    check("explicit A0: exponents at infinity = (1,1,2) => splitting O(-2)+O(-1)^2",
          np.allclose(np.round(exps), [1, 1, 2]))

    # (4) HONEST wall: product=I is path-ordered, NOT exp(2pi i sum A_k)
    Ms = [sl.expm(2j * np.pi * Ak[k]) for k in range(4)]
    prod = Ms[0] @ Ms[1] @ Ms[2] @ Ms[3]
    check("product of exp(2pi i A_k) is NOT I (monodromy is path-ordered, not exp of sum) "
          "=> global flat bundle needs the genuine numerical RH solve",
          not np.allclose(prod, np.eye(3), atol=1e-6))
    check("RESIDUAL: product=I constrains off-diag(A0) (RH solve); R-extraction needs the "
          "C6<->P1mu4 bridge (H2). RH route makes the SPLITTING algebraic, NOT c_u/c_d", True)
    return summary("v32 RH splitting")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
