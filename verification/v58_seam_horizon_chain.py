"""v58 -- the seam-horizon chain (precise version) and the open Seam-Horizon Theorem.

PRECISE FRAMING (replaces the loose "seam = horizon"):
  The seam is NOT identical to an event horizon.  It is the abstract boundary
  normaliser whose local gravitational realisation is a horizon.  A black hole is a
  local instance of the seam grammar; de Sitter is its global instance.

This script records the EXACT arithmetic of the chain (all [I]) and the honest status
of each link.  The strong thesis (seam = holographic horizon in the mathematical
sense) stays OPEN [A]; the missing step is an analytic area-law from the seam/Calderon
kernel, not another numerical match.

Chain:  Mobius/double cover -> Z2 one-sidedness -> c3 = 1/(8pi) (Gauss-Bonnet of the
compactified normal slice) -> KMS thermality T = 4 c3 kappa -> [OPEN: area entropy
S = A/(4 G_Sigma) from the seam determinant] -> Jacobson: Einstein normalisation 8pi G.
"""
import sympy as sp
from tfpt_constants import check, summary, reset, g_car, N_fam

mu4 = 4
Z2 = 2
pi = sp.pi


def run():
    reset()
    print("v58  seam-horizon chain (precise) + open Seam-Horizon Theorem")

    c3 = sp.Rational(1, 8) / pi

    # ---- (1) geometric origin: one-sided Gauss-Bonnet of the compactified normal slice ----
    GB = 2 * pi * 2  # oint_{S^2} K dA = 2 pi chi(S^2), chi(S^2)=2
    check("Gauss-Bonnet of S^2: oint K dA = 2 pi chi(S^2) = 4 pi (chi=2)", GB == 4 * pi)
    check("one-sided (Z2/Mobius): c3 = 1/(|Z2| * oint K dA) = 1/(2*4pi) = 1/(8pi)",
          sp.simplify(sp.Rational(1, 1) / (Z2 * GB) - c3) == 0)
    check("=> 8pi = |Z2| * 2 pi chi(S^2); the '8' = |Z2|*chi*2 = 8 (geometric reading of the seam '8')",
          Z2 * 2 * 2 == 8)

    # ---- (2) KMS / Killing-horizon thermality ----
    check("KMS: T = kappa/(2pi) = 4 c3 kappa  (1/(2pi) = 4 c3)",
          sp.simplify(sp.Rational(1, 2) / pi - 4 * c3) == 0)

    # ---- (3) Schwarzschild local realisation ----
    check("Schwarzschild: T_H = 1/(8 pi M) = c3/M  (kappa = 1/(4M))",
          sp.simplify(sp.Rational(1, 1) / (8 * pi) - c3) == 0)
    check("Schwarzschild: S_BH = A/4 = 4 pi M^2 = M^2/(2 c3)  (1/(2c3) = 4 pi)",
          sp.simplify(1 / (2 * c3) - 4 * pi) == 0)

    # ---- (4) de Sitter global realisation ----
    check("de Sitter: T_dS = H/(2pi) = 4 c3 H  (same 1/(2pi)=4c3 structure)",
          sp.simplify(sp.Rational(1, 2) / pi - 4 * c3) == 0)

    # ---- (5) Ryu-Takayanagi / holographic area in seam units ----
    check("RT: 1/(4G) = 2 pi Mbar^2 = Mbar^2/(4 c3)  (reduced Planck Mbar^2 = 1/(8 pi G); 1/(4c3)=2pi)",
          sp.simplify(1 / (4 * c3) - 2 * pi) == 0)

    # ---- the three realisations + the open theorem (status, not a pass/fail of the proof) ----
    check("three realisations: BH (local horizon), de Sitter (global horizon), seam (abstract normaliser)", True)
    check("Seam-Horizon Theorem is OPEN [A]: links 1-3,5 are [I]; the area-law S=A/(4G_Sigma) from the "
          "seam/Calderon determinant (replica variation) is the missing analytic step, then Jacobson closes it",
          True)
    return summary("v58 seam-horizon chain")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
