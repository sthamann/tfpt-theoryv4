"""EXPLORATION (experiments/ only -- the throwaway analysis behind v194).

Target: subclaim 2 of QGEO.ENERGY.02 -- "the raw RP-seam Dirichlet-to-Neumann
operator Lambda_Sigma is definable from the RP data alone (not the mu4 normal
form)". If it holds, [rho, Lambda_Sigma] = 0 is a genuine rigidity statement and
QGEO.SYM.01 would drop from postulate to theorem.

HONEST FINDING (this is a REDUCTION, NOT a closure):
  (A) The DtN / transfer operator IS RP-canonical: Osterwalder-Schrader
      reconstruction produces a canonical transfer operator T = e^{-H} from the
      RP state + reflection alone, no coordinates (v54; tfpt_2 (4)). The seam
      state is quasi-free (v155: the boundary marginal of a Gaussian bulk is the
      compression P Gamma P, a contraction). So Lambda_Sigma is RP-definable at
      the canonical level -- subclaim 2's HINGE is essentially met.
  (B) [rho, Lambda_Sigma] = 0 CLOSES on the finite cohomology H^1: rho: z->iz
      acts on H^1 = <w1,w2,w3>, wk = z^{k-1}dz/(z^4-1), as rho* wk = i^k wk
      (characters i, -1, -i -- DISTINCT). Distinct eigenvalues => any operator
      commuting with rho is diagonal there, and the harmonic structure IS
      rho-equivariant (v177/QGEO.COHOM.01). So the finite core is [E].
  (C) The RESIDUAL relocates (does NOT vanish): [rho, Lambda_Sigma] = 0 on the
      FULL boundary L^2 (beyond the 3-dim H^1) <=> the quasi-free seam state's
      modular flow is GEOMETRIC (Bisognano-Wichmann). This is a named, standard
      (hard) AQFT property -- sharper than "the seam is P^1\\mu4 (definitional)"
      -- but it stays [O].
  CIRCULARITY WATCH: BW normally PRESUPPOSES a conformal/Poincare-covariant net,
  which is part of what is being derived. So the BW step must be established
  INTRINSICALLY (modular geometricity from the RP + quasi-free data alone), or it
  re-circulates. That intrinsic-geometricity is the irreducible analytic content.

CONCLUSION: subclaim 2's hinge is met and the finite core is [E], so QGEO.SYM.01
REDUCES from a definitional postulate to "intrinsic BW geometric modular
covariance of the quasi-free seam state" -- one more notch sharper, still [O].
The last fog point SHARPENS; it does not close to [E].
"""
import sympy as sp


def main():
    z = sp.symbols("z")
    I = sp.I
    print("=== (B) finite core: rho: z->iz on wk = z^(k-1) dz/(z^4-1) ===")
    chars = []
    for k in (1, 2, 3):
        char = sp.simplify(I**(k - 1) * I)          # z^(k-1) gives i^(k-1); dz gives i
        den = sp.expand((I * z)**4 - 1)              # (iz)^4 - 1 = z^4 - 1 (invariant)
        chars.append(char)
        print(f"  k={k}: rho* wk = {char} wk   (char i^{k});  denom -> {den}")
    print(f"  characters {chars} are distinct: {len(set(chars)) == 3}")
    print("  => any operator commuting with rho is diagonal on H^1; the harmonic")
    print("     structure is rho-equivariant (v177) => [rho,Lambda]=0 on H^1 is [E].")
    print()
    print("=== (A) hinge: DtN is RP-canonical (OS, v54) on a quasi-free state (v155) ===")
    print("  => 'raw seam DtN RP-definable' holds at the canonical level.")
    print()
    print("=== (C) residual: full-L^2 commutation = Bisognano-Wichmann (intrinsic) -> [O] ===")
    print("  QGEO.SYM.01 reduces: definitional postulate -> intrinsic BW geometric")
    print("  modular covariance of the quasi-free seam state. SHARPER, still [O].")
    print("  (BW must be intrinsic, else it re-presupposes conformal covariance.)")


if __name__ == "__main__":
    main()
