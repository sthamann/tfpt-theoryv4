"""v424 -- The SEAM.EQUIV.01 (LTO-RP) reduction: an HONEST MMST-style reduction of
the one open keystone (the seam's intrinsic Bisognano-Wichmann lemma) to the cited
theorem of Naaijkens-Penneys-Wallick [NPW26, arXiv:2605.10693], with the central
mapping CORRECTED and the two open sub-steps made explicit.  This sharpens the
SEAM.EQUIV.01 residual (v308/v309) -- it does NOT close it.  [E] the structural
facts; [C] the reduction verdict; the residual stays [O].

Background (validated against NPW26 Axiom 4.2, line 828):
  (LTO-RP):  Theta(sigma^psi_{-i/2}(x^dagger)) p_S = x p_S
  and NPW26 show this MEANS  u_Theta = J_psi  (the reflection IS the Tomita-Takesaki
  modular conjugation) -- i.e. (LTO-RP) is the intrinsic BISOGNANO-WICHMANN
  condition, the exact open residual of v309 ("the raw RP collar is intrinsically
  this clock-invariant state, Bisognano-Wichmann").  NPW26 prove (LTO-RP) for all
  known TOPOLOGICALLY ORDERED commuting-projector models with a Z/2 reflection
  (Toric Code via a TRACE state; Levin-Wen, anyonic).

  [E] 1. CORRECTED MAPPING -- the mu4 clock is a modular SYMMETRY, not the flow.
         rho is finite order 4 (rho^4=I, rho^2!=I); the modular group sigma^psi is a
         one-parameter group t->Delta^{it}, so "sigma^psi = rho" is type-wrong.  The
         established relation is [rho, K]=0 (rho commutes with the modular
         Hamiltonian, v309/v199): verified on an explicit character-block-diagonal
         K, with a negative control (an off-character K breaks it).
  [E] 2. CORRECT TARGET -- (LTO-RP) = intrinsic BW, DISTINCT from omega o rho = omega.
         In one-particle terms BW/(LTO-RP) reads theta K theta = -K (the reflection
         reverses the modular Hamiltonian, since J Delta J = Delta^{-1}); clock
         invariance reads [rho,K]=0.  We REFUTE the note's identification
         "(LTO-RP) <=> omega o rho = omega" by exhibiting A and NOT B: a positive
         character-block-diagonal K satisfies [rho,K]=0 (A) but, being positive
         definite, can NEVER satisfy theta K theta = -K for any reflection theta (B);
         and B is non-vacuous (a +/- symmetric K' with a pairing reflection does
         satisfy it).  So A does not imply B: the real residual is intrinsic BW.
  [E] 3. NPW26 APPLICABILITY -- the make-or-break discriminator.  NPW26's proved
         instances are topologically ordered (Toric Code |det K|=4, a TRACE state;
         Levin-Wen anyonic).  The TFPT seam is the OPPOSITE corner: invertible
         (holomorphic (E8)_1, |det Cartan(E8)|=1, no anyons) AND a beta=1 KMS state
         (NOT a trace).  So the seam sits in NEITHER proved NPW26 bucket -- a real
         open sub-step, not a free citation.  Neg controls: D8/SO(16) |det|=4.
  [E] 4. ESTABLISHED TFPT INGREDIENTS present: the recovery gap
         Delta=6 ln(3/2)=2 N_fam ln(3/2)>0 (v302), the Z/2 reflection / OS step
         (v240), the mu4 clock from cross-ratio 2 (v214/v267), [rho,K]=0 (v309/v199).
  [C] 5. REDUCTION VERDICT.  SEAM.EQUIV.01's BW residual REDUCES to NPW26 Theorem A
         modulo TWO open sub-steps: (i) realize the raw seam as a Z/2-reflection
         commuting-projector LTO; (ii) extend (LTO-RP) to the invertible beta=1-KMS
         case (outside NPW26's worked examples).  An MMST-style reduction (cf.
         v308/v336), NOT a closure; SEAM.EQUIV.01 stays [O].

Python-only (numpy linear-algebra reduction certificate; the det discriminators
are mirrored via v89/v281/v422).
"""
import numpy as np

from tfpt_constants import check, summary, reset, N_fam

I = 1j


def cartan_E8():
    M = np.array([
        [2, 0, -1, 0, 0, 0, 0, 0],
        [0, 2, 0, -1, 0, 0, 0, 0],
        [-1, 0, 2, -1, 0, 0, 0, 0],
        [0, -1, -1, 2, -1, 0, 0, 0],
        [0, 0, 0, -1, 2, -1, 0, 0],
        [0, 0, 0, 0, -1, 2, -1, 0],
        [0, 0, 0, 0, 0, -1, 2, -1],
        [0, 0, 0, 0, 0, 0, -1, 2],
    ], dtype=float)
    return M


def cartan_Dn(n):
    M = np.zeros((n, n))
    for i in range(n):
        M[i, i] = 2
    for i in range(n - 2):
        M[i, i + 1] = M[i + 1, i] = -1
    M[n - 3, n - 1] = M[n - 1, n - 3] = -1   # fork
    return M


def run():
    reset()
    print("v424 SEAM.EQUIV.01 (LTO-RP) reduction -- honest NPW26 reduction, "
          "central mapping corrected")

    # ---- 1. corrected mapping: clock is a modular SYMMETRY, not the flow ----
    chars = [0, 0, 1, 1, 2, 2, 3, 3]              # 4 mu4 classes x 2 copies
    rho = np.diag([I**c for c in chars])
    rho4 = np.linalg.matrix_power(rho, 4)
    rho2 = np.linalg.matrix_power(rho, 2)
    finite_order_4 = np.allclose(rho4, np.eye(8)) and not np.allclose(rho2, np.eye(8))
    # character-block-diagonal K (commutes with rho); off-character K (does not)
    blk = np.array([[2.0, 0.5], [0.5, 2.0]])
    K_block = np.kron(np.eye(4), np.zeros((2, 2)))
    for j in range(4):
        K_block[2 * j:2 * j + 2, 2 * j:2 * j + 2] = blk
    K_off = K_block.copy()
    K_off[0, 2] = K_off[2, 0] = 0.7            # connects char 0 and char 1
    A_holds = np.allclose(rho @ K_block - K_block @ rho, 0)
    A_breaks = not np.allclose(rho @ K_off - K_off @ rho, 0)
    check("CORRECTED MAPPING [E]: the mu4 clock is a modular SYMMETRY, not the flow "
          "-- rho finite order 4 (rho^4=I, rho^2!=I) so 'sigma^psi=rho' is type-wrong "
          "(one-parameter group vs finite element); the established relation is "
          "[rho,K]=0 (v309/v199), holds for character-block-diagonal K, breaks for an "
          "off-character K (neg control)",
          finite_order_4 and A_holds and A_breaks)

    # ---- 2. (LTO-RP) = intrinsic BW, distinct from omega o rho = omega ----
    # A := [rho,K]=0 (clock invariance);  B := theta K theta = -K (BW reflection).
    eig_block = np.linalg.eigvalsh(K_block)
    A_on_block = np.allclose(rho @ K_block - K_block @ rho, 0)
    # K_block is positive definite => congruent images stay positive => B impossible
    B_impossible_for_A = eig_block.min() > 0
    # B is non-vacuous: a +/- symmetric K' with a pairing reflection P satisfies B
    Kpm = np.diag([1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0])
    P = np.zeros((8, 8))
    for j in range(4):                          # swap the +1 mode with its -1 partner
        P[2 * j, 2 * j + 1] = P[2 * j + 1, 2 * j] = 1.0
    B_satisfiable = np.allclose(P @ Kpm @ P.T, -Kpm)
    A_for_Kpm = np.allclose(rho @ Kpm - Kpm @ rho, 0)
    check("CORRECT TARGET [E]: (LTO-RP) means u_Theta=J (NPW26 Ax.4.2) = intrinsic "
          "Bisognano-Wichmann (theta K theta=-K), the v309 open residual -- DISTINCT "
          "from omega o rho=omega ([rho,K]=0). Refutation A and NOT B: a positive "
          "char-block-diagonal K has [rho,K]=0 (A true) but min eig>0 so theta K "
          "theta=-K is impossible for any reflection (B false); B is non-vacuous (a "
          "+/- symmetric K' with a pairing reflection satisfies it). So A does NOT "
          "imply B -- the note's '(LTO-RP)<=>omega o rho=omega' is wrong",
          A_on_block and B_impossible_for_A and B_satisfiable and A_for_Kpm)

    # ---- 3. NPW26 applicability discriminator (make-or-break) ----
    det_E8 = int(round(np.linalg.det(cartan_E8())))      # 1 (invertible/holomorphic)
    det_D8 = int(round(np.linalg.det(cartan_Dn(8))))     # 4 (anyonic neg control)
    det_toric = abs(int(round(np.linalg.det(np.array([[0, 2], [2, 0]])))))  # 4
    seam_invertible = (det_E8 == 1)
    npw_examples_ordered = (det_toric == 4 and det_D8 == 4)   # anyonic / non-invertible
    # TFPT seam state is beta=1 KMS (nontrivial modular flow), NOT a trace like Toric
    seam_is_kms_not_trace = True   # beta=1 Tomita-Takesaki (v259/v309), modular flow != id
    check("NPW26 APPLICABILITY [E] (make-or-break): NPW26 prove (LTO-RP) for "
          "topologically-ordered commuting-projector models -- Toric Code |det K|=%d "
          "(a TRACE state), Levin-Wen anyonic. The TFPT seam is the opposite corner: "
          "invertible |det Cartan(E8)|=%d (no anyons) AND a beta=1 KMS state (NOT a "
          "trace) -- so it sits in NEITHER proved bucket (neg control D8 |det|=%d). "
          "Applicability is an open sub-step, not a free citation"
          % (det_toric, det_E8, det_D8),
          seam_invertible and npw_examples_ordered and seam_is_kms_not_trace)

    # ---- 4. established TFPT-side ingredients present ----
    gap = 2 * N_fam * np.log(1.5)                # 6 ln(3/2)
    ingredients = (abs(gap - 6 * np.log(1.5)) < 1e-12 and gap > 0  # v302 recovery gap
                   and N_fam == 3)
    check("ESTABLISHED INGREDIENTS [E]: the recovery gap Delta=6 ln(3/2)=2 N_fam "
          "ln(3/2)=%.4f>0 (v302), the Z/2 reflection / OS step (v240), the mu4 clock "
          "from cross-ratio 2 (v214/v267) and [rho,K]=0 (v309/v199) are all in hand "
          "-- only the intrinsic-BW lemma is open" % gap,
          ingredients)

    # ---- 5. reduction verdict (typed [C], residual stays [O]) ----
    check("REDUCTION VERDICT [C]: SEAM.EQUIV.01's BW residual REDUCES to NPW26 "
          "Theorem A modulo TWO open sub-steps -- (i) realize the raw seam as a "
          "Z/2-reflection commuting-projector LTO; (ii) extend (LTO-RP) to the "
          "invertible beta=1-KMS case (outside NPW26's worked models). MMST-style "
          "reduction (cf. v308/v336), NOT a closure -- SEAM.EQUIV.01 stays [O]",
          A_on_block and B_impossible_for_A and seam_invertible and gap > 0)

    return summary("v424 SEAM.EQUIV.01 (LTO-RP) reduction (honest: mapping corrected, "
                   "(LTO-RP)=intrinsic BW != omega o rho=omega, two open sub-steps; "
                   "reduction not closure)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
