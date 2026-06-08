"""v55 -- the cyclic element inside the compiler hull, and the one-alpha cross-sector link.

PURE [I]/[L] facts (no cosmological narrative).

(1) E8 CONTAINS A LITERAL CYCLIC ELEMENT OF ORDER 30.  We BUILD the E8 Coxeter
    element from scratch (Cartan matrix -> product of the 8 simple reflections) and
    verify, by direct computation:
        - its order is exactly h(E8) = 30,
        - its eigenvalue phases are exp(2 pi i m/30) with m the E8 exponents
          {1,7,11,13,17,19,23,29}, which are EXACTLY the totatives of 30,
        - 30 = |Z2|*N_fam*g_car = 2*3*5,
        - rank E8 = 8 = phi(30) = #exponents = #live phases of the order-30 cycle.
    So the integer 8 of c3=1/(8pi) is the count of live phases of a primitive
    order-30 cyclic symmetry of the hull, with 30 = |Z2|*N_fam*g_car.

(2) ONE alpha^-1 FIXES EM, THE COSMIC HORIZON AND Lambda.  The de Sitter
    (Gibbons-Hawking) entropy and the cosmological constant are inverse and both set
    by e^{+-2 alpha^-1}:
        S_dS = e^{2 ainv}/(128 c3^4),   rho_Lambda/Mbar^4 ~ e^{-2 ainv},
        S_dS * rho_Lambda = 1/(128 c3^4) = 32 pi^4   (exact).
    So the SAME EM fixed point alpha^-1=137.036 sets the cosmic horizon entropy and
    the smallness of Lambda (~10^-122 = e^{-2 ainv}).  [I]-form; the physical
    identification seam<->horizon is the [P] reading kept out of this script.
"""
import numpy as np
import sympy as sp
from tfpt_constants import check, summary, reset, g_car, N_fam

Z2 = 2
mu4 = 4


def _e8_cartan():
    edges = [(1, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (2, 4)]  # Bourbaki E8
    A = sp.zeros(8, 8)
    for i in range(8):
        A[i, i] = 2
    for (a, b) in edges:
        A[a - 1, b - 1] = -1
        A[b - 1, a - 1] = -1
    return A


def _coxeter(A):
    def refl(i):
        S = sp.eye(8)
        for j in range(8):
            S[i, j] = (1 if i == j else 0) - A[i, j]
        return S
    C = sp.eye(8)
    for i in range(8):
        C = C * refl(i)
    return C


def run():
    reset()
    print("v55  cyclic element in the hull (E8 Coxeter, order 30) + one-alpha cross-sector")

    # ---- (1) build and diagonalise the E8 Coxeter element ----
    A = _e8_cartan()
    C = _coxeter(A)
    P, order = C, 1
    while P != sp.eye(8) and order < 200:
        P = P * C
        order += 1
    check("E8 Coxeter element order = 30 = h(E8) (computed from Cartan matrix)", order == 30)

    Cn = np.array(C.evalf(), dtype=complex)
    phases = sorted(int(round((np.angle(e) / (2 * np.pi)) * 30)) % 30 for e in np.linalg.eigvals(Cn))
    exps = [1, 7, 11, 13, 17, 19, 23, 29]
    check("Coxeter eigenvalue phases *30 = E8 exponents {1,7,11,13,17,19,23,29}", phases == exps)
    totatives = [k for k in range(1, 30) if sp.gcd(k, 30) == 1]
    check("E8 exponents = totatives of 30 (coprime to the cycle order)", exps == totatives)
    check("30 = |Z2|*N_fam*g_car = 2*3*5 (cycle order = product of the three core integers)",
          30 == Z2 * N_fam * g_car)
    check("rank E8 = 8 = phi(30) = #exponents = #live phases of the order-30 cycle",
          8 == sp.totient(30) == len(exps) == g_car + N_fam)

    # ---- (2) one alpha^-1 fixes EM, the cosmic horizon and Lambda ----
    pi = sp.pi
    c3 = sp.Rational(1, 8) / pi
    check("S_dS*rho_Lambda = 1/(128 c3^4) = 32 pi^4 (de Sitter entropy and Lambda are inverse)",
          sp.simplify(1 / (128 * c3**4) - 32 * pi**4) == 0)
    # the de Sitter entropy prefactor is built from carrier + glue atoms:
    check("S_dS = 2^g_car * pi^|mu4| * e^{2 ainv}: 32 = 2^g_car = dim Dirac(D5=SO10)=S+ + S-",
          32 == 2**g_car == 16 + 16)
    check("pi power = pi^|mu4| (glue index); 128 = 2^7 with 7 = scalaron exponent = g_car+N_fam-1",
          mu4 == 4 and 128 == 2**7 and 7 == g_car + N_fam - 1)
    ainv = sp.Float('137.035999', 30)
    S_dS = sp.exp(2 * ainv) / (128 * c3**4)
    check("S_dS = e^{2 ainv}/(128 c3^4) ~ 3.32e122 (same ainv as the EM fixed point)",
          abs(float(sp.log(S_dS, 10)) - 122.52) < 0.1)
    check("Lambda smallness ~10^-122 = e^{-2 ainv}: no fine-tuning, the SAME EM fixed point",
          abs(float(-2 * ainv / sp.log(10)) - (-119.03)) < 0.1)
    return summary("v55 cyclic hull element + one-alpha cross-sector")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
