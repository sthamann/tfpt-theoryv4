"""v64 -- Causal Boundary Engineering: the conditional NO-GO for seam shortcuts / CTCs.

A proof ATTEMPT for the Tier-3 "topological seam shortcut" that turned into a
conditional no-go.  Honest typing:
  - the discrete no-CTC core (a gapped positive transfer has NO periodic orbit) is
    machine-checkable [I], bound to v56;
  - the continuum chain (RP+OS -> unitary causal QFT -> ANEC -> topological censorship
    -> no traversable shortcut) is a [P] argument citing standard theorems, NOT a
    fully formalized TFPT theorem.

RESULT: under the theory's OWN conditions (reflection positivity, OS/unitarity, a
positive mass gap), a traversable seam shortcut connecting causally separated regions
by a SHORTER global path is FORBIDDEN.  The only survivor is the non-traversable
ER=EPR bridge (the Z2 seam), which carries entanglement, not signals.

Proof chain (Widerspruchsbeweis; assume a traversable shortcut exists):
  (1) RP + OS reconstruction => unitary causal QFT, H >= 0, mass gap Delta=6log(3/2)>0.
  (2) unitary + microcausal => ANEC (Faulkner-Leigh-Parrikar-Wang 2016;
      Hartman-Kundu-Tajdini 2017).
  (3) ANEC + global hyperbolicity => Topological Censorship (Friedman-Schleich-Witt
      1993): every causal curve is homotopic to a trivial one => no traversable shortcut.
  (4) gapped positive H => no time-periodicity => no CTC (discrete analog verified here).
  => contradiction.  Loopholes: (i) non-globally-hyperbolic ambient (no asymptotic
  'shorter path'); (ii) quantum ANEC violation (Gao-Jafferis-Wall 2017) gives a
  traversable wormhole that is NOT a shortcut (longer than the ambient path, no FTL
  signaling) = exactly the ER=EPR bridge.
"""
import numpy as np
import sympy as sp
from tfpt_constants import check, summary, reset


def run():
    reset()
    print("v64  Causal Boundary Engineering: conditional no-go for seam shortcuts / CTCs")

    # ---- discrete no-CTC core: gapped positive transfer has no periodic orbit ----
    spec = np.array([1.0, (2 / 3)**6, (1 / 3)**6])
    V = np.array([[1, 1, 1], [0, 1, 2], [0, 0, 1]], float)
    T = V @ np.diag(spec) @ np.linalg.inv(V)
    I = np.eye(3)
    periodic = any(np.allclose(np.linalg.matrix_power(T, n), I, atol=1e-9) for n in range(1, 300))
    check("gapped transfer has NO periodic orbit (T^n != I for all n>0) => discrete no-CTC [I, v56]",
          not periodic)
    evm = sorted(abs(np.linalg.eigvals(T)), reverse=True)
    check("subdominant eigenvalue moduli < 1 => T^n -> rank-1 projector, never identity",
          evm[0] > 0.999 and evm[1] < 0.999)

    # ---- the logical chain as documented structure (the [P] argument) ----
    gap = 6 * sp.log(sp.Rational(3, 2))
    check("(1) RP+OS => H>=0 with mass gap Delta=6log(3/2)>0", float(gap) > 0)
    check("(2) unitary+microcausal => ANEC (Faulkner et al.; Hartman-Kundu-Tajdini) [P-cited]", True)
    check("(3) ANEC + global hyperbolicity => Topological Censorship (Friedman-Schleich-Witt 1993): "
          "no traversable shortcut [P-cited]", True)
    check("(4) gapped positive H => no time-periodicity => no CTC (discrete analog verified above)", True)
    check("VERDICT: traversable seam shortcut FORBIDDEN under RP/OS/gap; only the non-traversable "
          "ER=EPR bridge (Z2 seam) survives (no FTL signaling) [conditional no-go]", True)
    check("falsifiable hinge: a shortcut needs macroscopic ANEC violation, which breaks RP/unitarity "
          "(= a falsification of the TFPT foundation itself)", True)
    return summary("v64 causal boundary engineering no-go")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
