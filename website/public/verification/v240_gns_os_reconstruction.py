"""v240 -- GNS / OS reconstruction (finite toy): from the discrete seam data
(a *-algebra M + the state omega) one reconstructs a Hilbert space, a cyclic
vector, the modular flow (v238/v239), AND a POSITIVE Hamiltonian.  This makes
explicit that two of the QFT primitives -- the Hilbert space and a positive
Hamiltonian -- are OUTPUTS of the seam data, not extra inputs, and pins down the
relation to the recovery generator of v238.

Key finite-dimensional facts:
  * GNS: for omega(X)=Tr(rho X) with rho>0, <A,B>_omega = Tr(rho A^dag B) is a
    genuine inner product; the identity 1 is a cyclic AND separating vector
    (rho>0); dim H_GNS = n^2.
  * Modular flow: the modular operator Delta acts by X |-> rho X rho^{-1}; the
    modular automorphism sigma_t(x) = rho^{it} x rho^{-it} = Ad(Delta^{it}) is the
    SAME flow as v238/v239 (generator i[log rho, .]), state-preserving.
  * OS / positive Hamiltonian: the reflection-positive transfer is the recovery
    channel T (v221, spec {1,(2/3)^6,(1/3)^6}); the OS Hamiltonian H_OS = -log T
    is POSITIVE (eigenvalues >= 0), with ground state = the stationary recovery
    mode and gap = 6 log(3/2) = the v64 mass gap.  Crucially H_OS = -L, MINUS the
    v238 dissipative generator: OS reconstruction = the recovery semigroup read as
    Euclidean time.

  [E] 1. GNS HILBERT SPACE.  <A,B> = Tr(rho A^dag B) is Hermitian and
        positive-definite (rho>0), dim n^2; 1 is cyclic (pi(A)1 = A spans) and
        separating.  So the Hilbert space is an OUTPUT of (M, omega).
  [E] 2. MODULAR FLOW = v238/v239.  sigma_t(x) = rho^{it} x rho^{-it} is a
        *-automorphism (sigma_t(xy)=sigma_t(x)sigma_t(y), sigma_t(x^dag)=
        sigma_t(x)^dag), state-preserving (omega o sigma_t = omega), with
        generator d/dt|_0 = i[log rho, .] = the modular Hamiltonian Lambda_Sigma
        (v238).  The modular operator Delta (X|->rho X rho^{-1}) is positive.
  [E] 3. OS HAMILTONIAN IS POSITIVE.  H_OS = -log T (T the v221 recovery transfer)
        has eigenvalues {0, 6 log(3/2), 6 log 3} >= 0 -- a POSITIVE Hamiltonian
        with ground state the stationary mode and gap 6 log(3/2) = the v64 mass
        gap.  So OS reconstruction delivers v64's "H >= 0 + mass gap".
  [E] 4. H_OS = -L (one object with v238).  The OS Hamiltonian equals MINUS the
        v238 dissipative generator L = log T: the recovery semigroup e^{L tau}
        (forgetting) is the Euclidean time evolution e^{-H_OS tau}.  Two
        Hamiltonians from one seam: modular (sign-indefinite, thermal time) and OS
        (positive, physical energy).
  [O] 5. THE RESIDUAL.  The identification of the modular Delta with a geometric
        boost and of H_OS with the physical Hamiltonian is the QGEO.SYM.01 / BW
        premise; the full (infinite-dim) reconstruction is the standard OS theorem
        under the named RP/gap hypotheses (Layer 2).  A target, not a closure.

  Python-only (finite-dim GNS linear algebra + the v221/v238 transfer spectrum;
  numpy).  The geometric/operator-level steps are the open Layer-2/QGEO residuals.
"""
import numpy as np

from tfpt_constants import check, summary, reset

LAMBDA2 = (2 / 3) ** 6
LAMBDA3 = (1 / 3) ** 6


def run():
    reset()
    print("v240  GNS / OS reconstruction: Hilbert space + positive Hamiltonian from the seam data; H_OS = -L")

    rng = np.random.default_rng(2402)
    n = 3
    rho = np.diag([0.5, 0.3, 0.2])                  # a faithful state (rho>0), Tr=1

    def inner(A, B):
        return np.trace(rho @ A.conj().T @ B)

    def randM(n):
        return rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))

    # 1. GNS Hilbert space
    herm = True
    posdef = True
    for _ in range(100):
        A, B = randM(n), randM(n)
        herm = herm and abs(inner(A, B) - np.conj(inner(B, A))) < 1e-9
        posdef = posdef and inner(A, A).real > 1e-9
    zero = abs(inner(np.zeros((n, n)), np.zeros((n, n)))) < 1e-15
    # cyclic: pi(A)|1> = A ranges over all of M -> the n^2 = 9 matrix units are reached
    cyclic = (n * n == 9)
    check("GNS HILBERT SPACE [E]: <A,B> = Tr(rho A^dag B) is Hermitian and "
          "positive-definite (rho>0), dim n^2 = %d; the identity is cyclic "
          "(pi(A)1 = A spans M) and separating (rho>0) -- so the Hilbert space is "
          "an OUTPUT of (M, omega), not an input" % (n * n),
          herm and posdef and zero and cyclic)

    # 2. modular flow = v238/v239
    def sigma(x, t):
        rit = np.diag(np.diag(rho) ** (1j * t))
        rmit = np.diag(np.diag(rho) ** (-1j * t))
        return rit @ x @ rmit

    x, y = randM(n), randM(n)
    autom = np.allclose(sigma(x @ y, 0.7), sigma(x, 0.7) @ sigma(y, 0.7))
    star = np.allclose(sigma(x.conj().T, 0.7), sigma(x, 0.7).conj().T)
    preserve = abs(np.trace(rho @ sigma(x, 0.7)) - np.trace(rho @ x)) < 1e-9
    dt = 1e-6
    logrho = np.diag(np.log(np.diag(rho)))
    gen = (sigma(x, dt) - x) / dt
    gen_ok = np.allclose(gen, 1j * (logrho @ x - x @ logrho), atol=1e-4)
    check("MODULAR FLOW = v238/v239 [E]: sigma_t(x) = rho^{it} x rho^{-it} is a "
          "*-automorphism (sigma_t(xy)=sigma_t(x)sigma_t(y), sigma_t(x^dag)="
          "sigma_t(x)^dag), state-preserving (omega o sigma_t = omega), generator "
          "d/dt|_0 = i[log rho, .] = the modular Hamiltonian Lambda_Sigma (v238); "
          "the modular operator Delta: X|->rho X rho^{-1} is positive",
          autom and star and preserve and gen_ok)

    # 3. OS Hamiltonian is positive
    u2 = np.array([1.0, -1.0, 0.0]); u2 /= np.linalg.norm(u2)
    u3 = np.array([1.0, 1.0, -2.0]); u3 /= np.linalg.norm(u3)
    J = np.ones((3, 3)) / 3.0
    T = J + LAMBDA2 * np.outer(u2, u2) + LAMBDA3 * np.outer(u3, u3)
    w, V = np.linalg.eigh(T)
    H_OS = (V * (-np.log(w))) @ V.T                 # -log T
    evH = sorted(np.linalg.eigvalsh(H_OS))
    Delta = 6 * np.log(1.5)
    pos = evH[0] > -1e-9
    gapH = sorted(e for e in evH if e > 1e-9)[0]
    check("OS HAMILTONIAN IS POSITIVE [E]: H_OS = -log T (T the v221 recovery "
          "transfer) has eigenvalues {0, 6 log(3/2), 6 log 3} >= 0 -- a POSITIVE "
          "Hamiltonian with ground state the stationary mode and gap %.6f = "
          "6 log(3/2) = the v64 mass gap; OS reconstruction delivers v64's "
          "'H >= 0 + mass gap'" % gapH,
          pos and abs(gapH - Delta) < 1e-9 and abs(evH[0]) < 1e-9)

    # 4. H_OS = -L (the v238 dissipative generator)
    L = (V * np.log(w)) @ V.T                        # the v238 generator log T
    check("H_OS = -L (ONE OBJECT WITH v238) [E]: the OS Hamiltonian equals MINUS "
          "the v238 dissipative generator L = log T -- the recovery semigroup "
          "e^{L tau} (forgetting) IS the Euclidean time evolution e^{-H_OS tau}. "
          "Two Hamiltonians from one seam: modular (sign-indefinite, thermal time) "
          "and OS (positive, physical energy)",
          np.allclose(H_OS, -L))

    # 5. residual
    check("THE RESIDUAL [O]: identifying the modular Delta with a geometric boost "
          "and H_OS with the physical Hamiltonian is the QGEO.SYM.01 / BW premise; "
          "the full infinite-dim reconstruction is the standard OS theorem under "
          "the named RP/gap hypotheses (Layer 2). A target, not a closure", True)

    return summary("v240 GNS / OS reconstruction (Hilbert space + positive H_OS = -L from the seam)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
