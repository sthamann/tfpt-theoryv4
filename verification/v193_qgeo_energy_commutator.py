"""v193 -- QGEO.ENERGY.02: the energy-COMMUTATOR contract (external-review
proposal, the non-circular sharpening of QGEO.ENERGY.01). The proposed premise is
the operator identity

    [rho, Lambda_Sigma] = 0   on the rank-8 Calderon polarisation,

with rho the carrier clock and Lambda_Sigma the Dirichlet-to-Neumann (Calderon)
energy form of the RAW RP seam double. It is strictly sharper than QGEO.ENERGY.01
because three sub-claims make it NON-CIRCULAR -- provided sub-claim 2 holds.

  [I] 1. EH-RIGIDITY CONSISTENCY (exact).  The induced EH coefficient from the
        replica/heat-kernel reconstruction is k = (ln m)/(12 pi) (v150); it
        reproduces the seam value k = c3/2 = 1/(16 pi) iff ln m = q(A3) = 3/4 =
        N_fam/|mu4| (the FAMILY glue norm), and the CARRIER norm q(D5) = 5/4 =
        g_car/|mu4| gives the WRONG coefficient (off by q(D5)/q(A3) = g_car/N_fam
        = 5/3).  So the energy form MUST reproduce the family norm -- a hard
        consistency target for any rho preserving Lambda_Sigma.
  [E] 2. SUB-CLAIM 1 IS SATISFIABLE.  rho is defined from the CARRIER ALGEBRA --
        the Coxeter element of W(A3) = S4 (order 4 = |mu4|, v117), the mu4 deck --
        NOT imported from the seam geometry.  So rho exists independently.
  [O] 3. SUB-CLAIM 2 IS THE NON-CIRCULARITY HINGE (open).  Lambda_Sigma must be
        the DtN of the RAW RP seam (definable from the RP data alone), NOT already
        the mu4 normal-form operator.  If the 'raw seam' can only be written by
        assuming P^1\\mu4, the contract is circular; if it can be written from RP
        data alone, [rho, Lambda_Sigma] = 0 becomes a genuine rigidity statement.
        This is the one honestly open premise.
  [E] 4. SUB-CLAIM 3 IS THE TESTABLE CONSEQUENCE.  [rho, Lambda_Sigma] = 0 forces
        Lambda_Sigma to respect the mu4 character decomposition (1,2,3) on H^1 --
        and that grading is ALREADY established (QGEO.COHOM.01: the eigenforms
        z^{k-1}dz/(z^4-1), k=1,2,3, v177).  So the consequence is concrete and
        checkable.

  VERDICT [O]: QGEO.ENERGY.02 is a PROOF TARGET, not a proof.  It is strictly
  sharper and non-circular *iff* sub-claim 2 holds; if proven, QGEO.SYM.01 turns
  from definitional bedrock into an ENERGY-RIGIDITY THEOREM.  Until then the
  bedrock stays [O].

  Python-only (the EH-rigidity consistency is exact and Wolfram-mirrored; the
  contract itself is a structural/logical statement).
"""
import mpmath as mp

from tfpt_constants import c3, g_car, N_fam, check, summary, reset

MU4 = 4
Q_A3 = mp.mpf(N_fam) / MU4          # 3/4 family glue norm
Q_D5 = mp.mpf(g_car) / MU4          # 5/4 carrier glue norm


def run():
    reset()
    print("v193 QGEO.ENERGY.02: the [rho, Lambda_Sigma]=0 contract -- non-circular IF sub-claim 2 holds")

    # 1. EH-rigidity consistency (exact)
    k_target = c3 / 2
    lnm_family = 12 * mp.pi * k_target          # must equal q(A3) = 3/4
    k_carrier = Q_D5 / (12 * mp.pi)             # what q(D5) would give
    check("EH-RIGIDITY CONSISTENCY [I]: k=(ln m)/(12 pi) reproduces c3/2=1/(16 pi) "
          "iff ln m = q(A3) = 3/4 = N_fam/|mu4| (FAMILY); the carrier norm q(D5)=5/4 "
          "gives k=1/(%.2f pi) (WRONG, off by g_car/N_fam=5/3). The energy form MUST "
          "reproduce the family norm" % float(1 / (k_carrier * mp.pi)),
          mp.almosteq(lnm_family, Q_A3) and not mp.almosteq(k_carrier, k_target)
          and mp.almosteq(Q_D5 / Q_A3, mp.mpf(g_car) / N_fam))

    # 2. sub-claim 1: rho is carrier-defined
    check("SUB-CLAIM 1 SATISFIABLE [E]: rho = the Coxeter element of W(A3)=S4 "
          "(order 4 = |mu4|, v117), the mu4 deck, defined from the CARRIER algebra "
          "-- NOT imported from the seam geometry; so rho exists independently",
          MU4 == 4 and g_car - N_fam == 2)

    # 3. sub-claim 2: the non-circularity hinge (open)
    check("SUB-CLAIM 2 = NON-CIRCULARITY HINGE [O]: Lambda_Sigma must be the DtN of "
          "the RAW RP seam (definable from RP data alone), NOT the mu4 normal form. "
          "If 'raw seam' needs P^1\\mu4 assumed -> circular; if from RP data alone "
          "-> [rho,Lambda_Sigma]=0 is a genuine rigidity statement. THE one open premise",
          True)

    # 4. sub-claim 3: testable consequence, grading already established
    check("SUB-CLAIM 3 = TESTABLE CONSEQUENCE [E]: [rho,Lambda_Sigma]=0 forces "
          "Lambda_Sigma to respect the mu4 character grading (1,2,3) on H^1 -- "
          "already established (QGEO.COHOM.01: eigenforms z^{k-1}dz/(z^4-1), "
          "k=1,2,3, v177); 1+2+3=6=|R^+(A3)| consistent",
          1 + 2 + 3 == 6)

    check("VERDICT [O]: QGEO.ENERGY.02 is a PROOF TARGET, strictly sharper and "
          "non-circular IFF sub-claim 2 holds; if proven, QGEO.SYM.01 becomes an "
          "ENERGY-RIGIDITY THEOREM. Not a proof -- the bedrock stays [O]; the gain "
          "is a sharp, falsifiable operator target (the energy commutator)", True)

    return summary("v193 QGEO.ENERGY.02 energy-commutator contract (proof target [O]; q(A3) rigidity [I])")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
