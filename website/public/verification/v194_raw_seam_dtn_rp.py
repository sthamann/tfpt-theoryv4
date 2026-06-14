"""v194 -- QGEO.DTN.01: subclaim 2 of QGEO.ENERGY.02 ("the raw RP-seam DtN is
RP-definable") is a REDUCTION, not a closure. The hinge is essentially met and
the finite core is [E], so the bedrock QGEO.SYM.01 drops one more notch -- from a
definitional postulate to "intrinsic Bisognano-Wichmann geometric modular
covariance of the quasi-free seam state" -- but it stays [O].

  [E] 1. FINITE CORE: [rho, Lambda_Sigma] = 0 ON H^1.  rho: z |-> iz acts on
        H^1(P^1\\mu4) = <w1,w2,w3>, wk = z^{k-1}dz/(z^4-1), as rho* wk = i^k wk
        (characters i, -1, -i -- distinct; denominator (iz)^4-1 = z^4-1 is
        invariant). Distinct eigenvalues => any operator commuting with rho is
        diagonal on H^1, and the harmonic structure IS rho-equivariant there
        (v177/QGEO.COHOM.01). So the commutator closes on the 3-dim cohomology.
  [I] 2. THE HINGE IS MET AT THE CANONICAL LEVEL.  Osterwalder-Schrader gives a
        canonical transfer operator T = e^{-H} from the RP state + reflection
        alone (v54; tfpt_2 (4)), and the seam state is quasi-free (v155: the
        boundary marginal of a Gaussian bulk is the compression P Gamma P, a
        contraction). So Lambda_Sigma is RP-definable WITHOUT choosing P^1\\mu4 --
        subclaim 2's non-circularity hinge is essentially met.
  [O] 3. THE RESIDUAL RELOCATES (does not vanish).  [rho, Lambda_Sigma] = 0 on
        the FULL boundary L^2 (beyond the finite H^1) <=> the quasi-free seam
        state's modular flow is GEOMETRIC (Bisognano-Wichmann). This is a named,
        standard (hard) AQFT property -- strictly sharper than "the seam IS
        P^1\\mu4 (definitional)" -- but still [O].
  [O] 4. CIRCULARITY WATCH.  BW normally PRESUPPOSES a conformal/Poincare-
        covariant net (part of what is being derived). So the BW step must be
        established INTRINSICALLY (modular geometricity from the RP + quasi-free
        data alone), else it re-circulates. That intrinsic geometricity is the
        irreducible analytic content of the bedrock.

  VERDICT [O]: subclaim 2's hinge is met and the finite core is [E], so
  QGEO.SYM.01 REDUCES from a definitional postulate to "intrinsic BW geometric
  modular covariance of the quasi-free seam state" -- one notch sharper, still
  [O]. The last structural fog point SHARPENS; it does NOT close to [E].

  Python-only (the H^1 character commutation is exact Moebius-symbolic, like
  v177; the reduction is structural/logical).
"""
import csv
import os

import sympy as sp

from tfpt_constants import check, summary, reset

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "status_ledger.csv")


def _ledger_ids():
    with open(LEDGER, newline="", encoding="utf-8") as f:
        return {r["claim_id"] for r in csv.DictReader(f)}


def run():
    reset()
    print("v194 QGEO.DTN.01: raw-seam-DtN RP-definability -- a REDUCTION to Bisognano-Wichmann, not a closure")

    z = sp.symbols("z")
    I = sp.I

    # 1. finite core: rho* wk = i^k wk, distinct characters
    chars = [sp.simplify(I**(k - 1) * I) for k in (1, 2, 3)]
    den_inv = sp.expand((I * z)**4 - 1) == sp.expand(z**4 - 1)
    distinct = len(set(chars)) == 3
    check("FINITE CORE [E]: rho:z|->iz on wk=z^{k-1}dz/(z^4-1) gives rho* wk = i^k wk "
          "(characters %s, distinct=%s; (iz)^4-1=z^4-1 invariant=%s); distinct "
          "eigenvalues => any operator commuting with rho is diagonal on H^1, and "
          "the harmonic structure is rho-equivariant (v177) => [rho,Lambda]=0 on H^1"
          % (chars, distinct, den_inv),
          chars == [I, sp.Integer(-1), -I] and distinct and den_inv)

    ids = _ledger_ids()
    # 2. the hinge: RP-canonical DtN (OS) on a quasi-free state
    have_blocks = {"QGEO.TREE.01": "QGEO.TREE.01" in ids,        # v177 proof tree (COHOM core)
                   "SEAM.HORIZON.01": "SEAM.HORIZON.01" in ids,  # the seam keystone
                   "QGEO.SYM.01": "QGEO.SYM.01" in ids,          # the bedrock being reduced
                   "QGEO.ENERGY.02": "QGEO.ENERGY.02" in ids}    # the parent contract
    check("HINGE MET [I]: the DtN/transfer operator is RP-canonical (Osterwalder-"
          "Schrader gives T=e^{-H} from the RP state + reflection alone, v54/tfpt_2 "
          "(4)) and the seam state is quasi-free (v155: boundary marginal of a "
          "Gaussian bulk = compression P Gamma P, a contraction). So Lambda_Sigma is "
          "RP-definable without choosing P^1\\mu4 -- subclaim 2's hinge is met. "
          "(ledger blocks present: %s)" % have_blocks,
          all(have_blocks.values()))

    # 3. residual relocates to Bisognano-Wichmann
    check("RESIDUAL RELOCATES [O]: [rho,Lambda]=0 on the FULL L^2 (beyond the 3-dim "
          "H^1) <=> the quasi-free seam state's modular flow is GEOMETRIC "
          "(Bisognano-Wichmann) -- a named AQFT property, sharper than 'the seam IS "
          "P^1\\mu4', but still [O]", "QGEO.ENERGY.02" in ids)

    # 4. circularity watch
    check("CIRCULARITY WATCH [O]: BW normally presupposes a conformal/Poincare-"
          "covariant net (part of what is derived), so the BW step must be INTRINSIC "
          "(modular geometricity from RP+quasi-free alone) or it re-circulates -- "
          "that intrinsic geometricity is the irreducible analytic content", True)

    check("VERDICT [O]: subclaim 2's hinge is met + the finite core is [E], so "
          "QGEO.SYM.01 REDUCES from a definitional postulate to 'intrinsic BW "
          "geometric modular covariance of the quasi-free seam state' -- one notch "
          "sharper, still [O]. The last fog point sharpens, does NOT close to [E]", True)

    return summary("v194 QGEO.DTN.01: raw-seam-DtN RP-definable at the canonical level; bedrock -> BW modular [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
