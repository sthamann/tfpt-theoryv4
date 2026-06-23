/-
  TFPT Carrier Rigidity — Lean 4 Formalization
  =============================================

  Top-level entry. Re-exports the dependency graph of carrier
  rigidity from the boundary involution up to the concrete
  hypercharge spectrum.

  Module map:

    Polarization           — orthogonal idempotents and carrier polynomial
    InvolutionProjectors   — ε² = id  ⇒  spectral projectors P_±
    MathlibBridge          — Polarization ↔ Mathlib's CompleteOrthogonalIdempotents
    LatticeRigidityGeneral — general (m,n) integer rigidity, then (3,2) corollary
    Rigidity               — SM specialisation (q₋,q₊) = (-2, 3)
    TraceProjection        — structural trace formula  tr(aP₋ + bP₊) = a·rank + b·rank
    DeterminantCharacter   — det T(λ) = λ^(m·qm + n·qp);  trace-zero from det-preserving
    HiggsIndexShadow       — algebraic shadow H^0(P^1, O(1)) ≅ K^2  ⇒  dim E_+ = 2
    YukawaType             — Stage-A interface for primitive indecomposable Yukawa type
    CarrierData            — main bundled theorem: tr Y = 0 from all premises
    Hypercharge            — concrete 5×5 model:  tr Y = 0 and 6 Y² − Y − 1 = 0
    GlueUniqueness         — v89/v92 cores: glue uniqueness up to the spinor
                             swap + carrier index 4 = |μ₄| (kernel decide)
    Sanity                 — #eval smoke tests
    AxiomCheck             — #print axioms for the main theorems

  See README.md and `note_carrier_rigidity_lean4.tex` for the
  proof walkthrough and the dependency-graph documentation.
-/

import TfptCarrier.Polarization
import TfptCarrier.InvolutionProjectors
import TfptCarrier.CalderonInterface
import TfptCarrier.CalderonProjector
import TfptCarrier.BoundaryPolarization
import TfptCarrier.MathlibBridge
import TfptCarrier.LatticeRigidityGeneral
import TfptCarrier.Rigidity
import TfptCarrier.OrientedDeterminantCarrier
import TfptCarrier.TraceProjection
import TfptCarrier.DeterminantCharacter
import TfptCarrier.HiggsIndexShadow
import TfptCarrier.HiggsTopForm
import TfptCarrier.HiggsSchemeCohomologyShadow
import TfptCarrier.YukawaRank
import TfptCarrier.YukawaTopForm
import TfptCarrier.YukawaPrimitive
import TfptCarrier.YukawaTrilinearForm
import TfptCarrier.YukawaStageDExistence
import TfptCarrier.BoundaryYukawaKernelInterface
import TfptCarrier.SeamWindingInterface
import TfptCarrier.CarrierData
import TfptCarrier.Hypercharge
import TfptCarrier.GlueUniqueness
import TfptCarrier.SeamDeckClosure
import TfptCarrier.SeamEquivChain
import TfptCarrier.SeamScalingLimit
import TfptCarrier.BWKeystone
import TfptCarrier.CartanDeterminants
import TfptCarrier.Mu4Commutation
import TfptCarrier.MobiusUniformisation
import TfptCarrier.CohomologyGrading
import TfptCarrier.AnchorLadder
import TfptCarrier.PascalLadder
import TfptCarrier.Sanity
import TfptCarrier.AxiomCheck
import TfptCarrier.AuditCheck
import TfptCarrier.AuditContract
