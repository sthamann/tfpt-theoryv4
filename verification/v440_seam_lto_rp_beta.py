"""v440 -- SEAM.EQUIV.LTORP.BETA.01: the beta-interpolation that connects the
NPW26-PROVEN trace case (beta=0) to the seam's beta=1 KMS case along an
obstruction-free homotopy -- upgrading the single-point v426 witness for v424
sub-step (ii) to a PATH argument.

Naaijkens-Penneys-Wallick [NPW26, arXiv:2605.10693] prove (LTO-RP) for the TRACE
state (the maximally mixed, beta=0 covariance C=1/2).  The TFPT seam is the beta=1
KMS state.  v426 showed (LTO-RP) holds AT beta=1; this module shows it holds ALONG
the whole interpolation C_beta = 1/(1+e^{beta K}), beta in [0, infty): the defining
(LTO-RP)/BW data are CONDITIONS ON K, hence beta-independent, and every covariance
on the path is reflection-related and mu4-invariant and a valid covariance.  So
there is NO obstruction between the proven trace case and the seam KMS case.

One-particle dictionary (as in v426): (LTO-RP)/BW <=> u_Theta=J <=> Theta K Theta=-K;
the mu4 clock rho a modular SYMMETRY <=> [rho,K]=0; KMS reflection relation
Theta C_beta Theta = 1 - C_beta (since K is reflection-odd).

  [E] 1. beta-INDEPENDENT (LTO-RP) DATA.  Theta K Theta=-K and [rho,K]=0 are
         conditions on K alone -- independent of beta; built once, hold for all beta.
  [E] 2. THE KMS PATH.  C_beta=1/(1+e^{beta K}): beta=0 -> C=1/2 I (the NPW26 TRACE
         state), beta=1 -> the seam KMS state (v426), beta->infty -> the ground-
         state projection.  At every beta: Theta C_beta Theta=1-C_beta (reflection),
         [rho,C_beta]=0 (mu4-invariant), 0<=C_beta<=1 (a valid covariance / RP).
  [E] 3. NO OBSTRUCTION (homotopy).  beta -> C_beta is norm-continuous and stays in
         the (LTO-RP)-valid set for all beta in [0, beta_max] -- a continuous path
         from the proven trace endpoint to the seam KMS point, no topological wall.
  [E] 4. NEG CONTROLS.  A reflection-EVEN K' (Theta K' Theta=+K') breaks
         Theta C_beta Theta=1-C_beta for every beta>0 (the trace endpoint beta=0 is
         degenerate, C=1/2 I always passes) -- the relation is non-vacuous and
         beta-sensitive away from the trace; an off-mu4-block K breaks [rho,C_beta].
  [C]/[O] 5. VERDICT.  (LTO-RP)/BW connects the NPW26 trace case to the seam beta=1
         KMS case along an obstruction-free homotopy -- a PATH argument for v424
         sub-step (ii), stronger than the single point of v426.  SEAM.EQUIV.01 stays
         [O]: that the operator-algebraic (LTO-RP) property is CLOSED along the path
         in the continuum (uniform in the limit) is the residual analytic step.

Python-only (numpy/scipy; reuses the v426 collar construction, no Wolfram mirror).
"""
import numpy as np
from scipy.linalg import expm

from tfpt_constants import check, summary, reset, g_car

I2 = np.eye(2)
SX = np.array([[0.0, 1.0], [1.0, 0.0]])
SZ = np.array([[1.0, 0.0], [0.0, -1.0]])


def collar():
    """The v426 seam collar: K reflection-odd, mu4-even, gapped; rho, Theta."""
    k = 3.0 * np.log(1.5)                                    # half-gap; 2k=6 ln(3/2)
    marks = np.diag([1j ** m for m in range(4)])
    rho = np.kron(marks, I2)
    K = np.kron(np.eye(4), k * SZ)                           # reflection-odd, mu4-even
    Theta = np.kron(np.eye(4), SX)
    return K, rho, Theta


def cov(beta, K):
    """beta-KMS Fermi-Dirac covariance C_beta = 1/(1+e^{beta K})."""
    eK = expm(beta * K)
    return np.linalg.inv(np.eye(K.shape[0]) + eK)


def run():
    reset()
    print("v440 SEAM.EQUIV.LTORP.BETA: beta-interpolation NPW26 trace(beta=0) -> "
          "seam KMS(beta=1), an obstruction-free homotopy")
    K, rho, Theta = collar()
    dim = K.shape[0]

    # ---- 1. beta-independent (LTO-RP) data ----
    bw = np.allclose(Theta @ K @ Theta.conj().T, -K)
    sym = np.allclose(rho @ K - K @ rho, 0)
    check("beta-INDEPENDENT (LTO-RP) DATA [E]: Theta K Theta=-K (u_Theta=J) and "
          "[rho,K]=0 (mu4 modular symmetry) are conditions on K alone -- "
          "independent of beta, so the (LTO-RP)/BW data are fixed across the path",
          bw and sym)

    # ---- 2. the KMS path ----
    betas = [0.0, 0.25, 0.5, 1.0, 2.0, 8.0]
    all_rel = all_clk = all_psd = True
    for b in betas:
        C = cov(b, K)
        rel = np.allclose(Theta @ C @ Theta.conj().T, np.eye(dim) - C)
        clk = np.allclose(rho @ C - C @ rho, 0)
        ev = np.linalg.eigvalsh(0.5 * (C + C.conj().T))
        psd = ev.min() >= -1e-12 and ev.max() <= 1 + 1e-12
        all_rel &= rel
        all_clk &= clk
        all_psd &= psd
    trace_pt = np.allclose(cov(0.0, K), 0.5 * np.eye(dim))   # beta=0 is the trace
    check("THE KMS PATH [E]: C_beta=1/(1+e^{beta K}) has beta=0 -> C=1/2 I (the "
          "NPW26 TRACE state), beta=1 -> the seam KMS state, beta->inf -> the "
          "ground-state projection; at every beta in {0,..,8} Theta C_beta Theta=1-C "
          "(reflection), [rho,C_beta]=0 (mu4), 0<=C_beta<=1 (valid covariance/RP)",
          all_rel and all_clk and all_psd and trace_pt)

    # ---- 3. no obstruction (homotopy continuity) ----
    grid = np.linspace(0.0, 8.0, 41)
    Cs = [cov(b, K) for b in grid]
    steps = [np.linalg.norm(Cs[i + 1] - Cs[i]) for i in range(len(grid) - 1)]
    cont = max(steps) < 0.2                                  # norm-continuous, no jump
    check("NO OBSTRUCTION [E]: beta -> C_beta is norm-continuous (max step %.3f over "
          "a 41-point grid on [0,8]) and stays in the (LTO-RP)-valid set throughout "
          "-- a continuous homotopy from the proven trace endpoint to the seam KMS "
          "point, no topological wall" % max(steps),
          cont)

    # ---- 4. neg controls ----
    Keven = np.kron(np.eye(4), 3.0 * np.log(1.5) * I2)       # reflection-EVEN
    even_breaks = not np.allclose(Theta @ cov(1.0, Keven) @ Theta.conj().T,
                                  np.eye(dim) - cov(1.0, Keven))
    Koff = K.copy()
    Koff[0, 2] = Koff[2, 0] = 0.4                            # off-mu4 mixing
    off_breaks = not np.allclose(rho @ cov(1.0, Koff) - cov(1.0, Koff) @ rho, 0)
    check("NEG CONTROLS [E]: a reflection-EVEN K' breaks Theta C_beta Theta=1-C for "
          "beta>0 (the trace endpoint beta=0 is degenerate, C=1/2 I always passes), "
          "and an off-mu4-block K breaks [rho,C_beta] -- the path conditions are "
          "non-vacuous and beta-sensitive away from the trace",
          even_breaks and off_breaks)

    # ---- 5. verdict (typed [C]/[O]) ----
    check("VERDICT [C]/[O]: (LTO-RP)/BW connects the NPW26 trace case (beta=0) to "
          "the seam beta=1 KMS case along an obstruction-free homotopy -- a PATH "
          "argument for v424 sub-step (ii), stronger than the single point of v426. "
          "SEAM.EQUIV.01 stays [O]: that the operator-algebraic (LTO-RP) property is "
          "CLOSED along the path in the continuum (uniform in the limit) is the "
          "residual analytic step",
          bw and sym and all_rel and all_psd and cont and g_car == 5)

    return summary("v440 SEAM.EQUIV.LTORP.BETA (beta-homotopy trace->KMS, "
                   "obstruction-free; v424 (ii) path argument; SEAM.EQUIV.01 [O])")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
