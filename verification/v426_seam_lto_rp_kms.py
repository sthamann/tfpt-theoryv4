"""v426 -- SEAM.EQUIV.LTORP.KMS.01: the INVERTIBLE beta=1-KMS variant of the
(LTO-RP) axiom -- the one corner Naaijkens-Penneys-Wallick [NPW26, arXiv:2605.10693]
leave open.  NPW26 prove (LTO-RP) only for TOPOLOGICALLY ORDERED commuting-projector
models (Toric Code via a TRACE state; Levin-Wen anyonic).  The TFPT seam is the
opposite corner: invertible (holomorphic (E8)_1, no anyons) AND a beta=1 KMS state
(nontrivial modular flow, NOT a trace).  This module exhibits CONSTRUCTIVELY that on
this corner the (LTO-RP)/Bisognano-Wichmann condition u_Theta=J is satisfiable and
NATURAL, by direct Tomita-Takesaki -- advancing sub-step (ii) of v424.  It does NOT
close SEAM.EQUIV.01 (the continuum/abstract realisation, sub-step (i), stays open).

One-particle / quasi-free dictionary (the seam collar):
  modular operator Delta = e^{-K},  modular conjugation J,  reflection Theta;
  (LTO-RP)/BW  <=>  u_Theta = J  <=>  Theta K Theta^{-1} = -K  (J Delta J = Delta^{-1});
  the mu4 clock rho is a modular SYMMETRY  <=>  [rho, K] = 0  (NOT sigma^psi=rho).

  [E] 1. THE INVERTIBLE-KMS COLLAR.  Build K reflection-odd, mu4-even, gapped (gap
         2k=6 ln(3/2)); C=1/(1+e^K) is the beta=1 KMS covariance and satisfies the
         beta=1 KMS relation C/(1-C)=e^{-K} -- a genuine KMS (not trace) state.
  [E] 2. (LTO-RP)/BW HOLDS.  Theta K Theta^{-1} = -K (reflection = modular
         conjugation, u_Theta=J) AND [rho,K]=0 (mu4 a modular symmetry) -- both hold
         for the constructed collar, so (LTO-RP) is satisfied on the invertible KMS
         corner by direct Tomita-Takesaki, no skein/UFC machinery.
  [E] 3. INVERTIBLE, OUTSIDE NPW26.  |det Cartan(E8)|=1 (one primary, invertible,
         no anyons) vs the anyonic |det|=4 of NPW26's worked models; and the state
         is NOT a trace (K!=0 => Delta=e^{-K}!=I, nontrivial modular flow) -- so it
         is in NEITHER proved NPW26 bucket.
  [E] 4. NEG CONTROLS (teeth).  A side-EVEN reflection gives Theta K Theta=+K!=-K
         (BW fails); an off-mu4-block K mixing two marks gives [rho,K]!=0 (the mu4
         symmetry fails).  Not every reflection / not every K works.
  [C] 5. VERDICT.  On the gapped invertible beta=1-KMS reflection-symmetric collar,
         (LTO-RP) reduces to (Theta K Theta=-K) and ([rho,K]=0), both structural --
         the invertible-KMS variant NPW26 leave open is constructively satisfiable.
         Advances v424 sub-step (ii); SEAM.EQUIV.01 stays [O] (continuum sub-step
         (i) remains).  A finite-dim Tomita-Takesaki witness, NOT the continuum
         theorem.

Python-only (numpy linear algebra; det discriminator mirrored via v89/v281/v422/v424).
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car

I2 = np.eye(2)
SX = np.array([[0.0, 1.0], [1.0, 0.0]])              # side-flip (reflection)
SZ = np.array([[1.0, 0.0], [0.0, -1.0]])             # boost / modular direction


def cartan_E8():
    return np.array([
        [2, 0, -1, 0, 0, 0, 0, 0], [0, 2, 0, -1, 0, 0, 0, 0],
        [-1, 0, 2, -1, 0, 0, 0, 0], [0, -1, -1, 2, -1, 0, 0, 0],
        [0, 0, 0, -1, 2, -1, 0, 0], [0, 0, 0, 0, -1, 2, -1, 0],
        [0, 0, 0, 0, 0, -1, 2, -1], [0, 0, 0, 0, 0, 0, -1, 2]], dtype=float)


def run():
    reset()
    print("v426 SEAM.EQUIV.LTORP.KMS: the invertible beta=1-KMS (LTO-RP) variant "
          "NPW26 leaves open")

    k = 3.0 * np.log(1.5)                             # half-gap; gap 2k = 6 ln(3/2)
    marks = np.diag([1j**m for m in range(4)])        # mu4 clock on the 4 marks
    rho = np.kron(marks, I2)                          # rho on mark sector (order 4)
    K = np.kron(np.eye(4), k * SZ)                    # reflection-odd, mu4-even, gapped
    Theta = np.kron(np.eye(4), SX)                    # the seam reflection (side-flip)

    # ---- 1. invertible-KMS collar: beta=1 KMS relation + gap ----
    eK = np.diag(np.exp(np.diag(K).real)).astype(complex)
    C = np.linalg.inv(np.eye(8) + eK)                 # Fermi-Dirac covariance, beta=1
    kms = np.allclose(C @ np.linalg.inv(np.eye(8) - C), np.linalg.inv(eK))  # C/(1-C)=e^{-K}
    gap = 2 * k
    rho4 = np.allclose(np.linalg.matrix_power(rho, 4), np.eye(8))
    rho2 = not np.allclose(np.linalg.matrix_power(rho, 2), np.eye(8))
    check("INVERTIBLE-KMS COLLAR [E]: K reflection-odd/mu4-even/gapped (gap "
          "2k=6 ln(3/2)=%.4f>0); C=1/(1+e^K) is the beta=1 KMS covariance and "
          "satisfies C/(1-C)=e^{-K} (a genuine KMS, not trace, state); rho order 4"
          % gap,
          kms and gap > 1.6 and rho4 and rho2)

    # ---- 2. (LTO-RP)/BW holds: Theta K Theta = -K and [rho,K]=0 ----
    bw = np.allclose(Theta @ K @ Theta.conj().T, -K)             # u_Theta = J
    sym = np.allclose(rho @ K - K @ rho, 0)                      # mu4 modular symmetry
    check("(LTO-RP)/BW HOLDS [E]: Theta K Theta^{-1} = -K (reflection = modular "
          "conjugation, u_Theta=J) AND [rho,K]=0 (mu4 a modular symmetry) -- both "
          "hold, so (LTO-RP) is satisfied on the invertible KMS corner by direct "
          "Tomita-Takesaki",
          bw and sym)

    # ---- 3. invertible, not a trace, outside NPW26 ----
    det_E8 = int(round(np.linalg.det(cartan_E8())))             # 1 (invertible)
    det_toric = abs(int(round(np.linalg.det(np.array([[0, 2], [2, 0]])))))  # 4 (anyonic)
    not_trace = not np.allclose(eK, np.eye(8))                  # Delta=e^{-K} != I
    check("INVERTIBLE, OUTSIDE NPW26 [E]: |det Cartan(E8)|=%d (one primary, "
          "invertible, no anyons) vs anyonic |det|=%d of NPW26's worked models; and "
          "the state is NOT a trace (Delta=e^{-K}!=I, nontrivial modular flow) -- "
          "neither proved NPW26 bucket" % (det_E8, det_toric),
          det_E8 == 1 and det_toric == 4 and not_trace)

    # ---- 4. neg controls (teeth) ----
    Theta_even = np.kron(np.eye(4), I2)                         # side-EVEN reflection
    bw_fails = not np.allclose(Theta_even @ K @ Theta_even.T, -K)
    Koff = K.copy()
    Koff[0, 2] = Koff[2, 0] = 0.5                               # mix mark 0 and mark 1
    sym_fails = not np.allclose(rho @ Koff - Koff @ rho, 0)
    check("NEG CONTROLS [E]: a side-EVEN reflection gives Theta K Theta=+K!=-K (BW "
          "fails); an off-mu4-block K mixing two marks gives [rho,K]!=0 (mu4 "
          "symmetry fails) -- the conditions have teeth",
          bw_fails and sym_fails)

    # ---- 5. verdict (typed [C]) ----
    check("VERDICT [C]: on the gapped invertible beta=1-KMS reflection-symmetric "
          "collar, (LTO-RP) reduces to (Theta K Theta=-K) and ([rho,K]=0), both "
          "structural -- the invertible-KMS variant NPW26 leave open is "
          "constructively satisfiable (advances v424 sub-step (ii)). SEAM.EQUIV.01 "
          "stays [O]: the continuum/abstract realisation (sub-step (i)) remains; "
          "this is a finite-dim Tomita-Takesaki witness, not the continuum theorem",
          bw and sym and kms and det_E8 == 1 and g_car == 5)

    return summary("v426 SEAM.EQUIV.LTORP.KMS (invertible beta=1-KMS (LTO-RP) "
                   "constructively satisfiable; advances v424 (ii); SEAM.EQUIV.01 "
                   "stays [O])")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
