/-
  TFPT Carrier — Signature-Lock Audit Contract
  --------------------------------------------

  Companion of `AuditCheck.lean` (which only verifies that the
  headline names elaborate) and of `scripts/audit.sh` (which
  checks for deferred-proof placeholders, axioms, etc.).

  This module goes one step further: each headline theorem is
  used in an `example` whose type is the *exact intended Lean
  statement*. If a future refactor silently weakens the
  conclusion of a headline theorem (without renaming it), this
  file will fail to elaborate.

  ----------------------------------------------------------------
  Reading the file
  ----------------------------------------------------------------

  Every block has the form

      example : <exact intended type signature> :=
        <reference to the theorem>

  The `example` does not introduce a new name; it only verifies
  that the right-hand side has the left-hand side's type.

  ----------------------------------------------------------------
  Strictness
  ----------------------------------------------------------------

  This is strictly stronger than `#check`:

  * `#check theorem_name` succeeds as long as `theorem_name`
    elaborates *with any type*.
  * The patterns below succeed only if `theorem_name` elaborates
    with the *exact specified type* (up to definitional equality).
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

namespace TFPT.Carrier.AuditContract

/-! ## Layer 1 — Polarization (algebraic core) -/

example {A : Type*} [Ring A] [Algebra ℚ A]
    (p : TFPT.Carrier.Polarization A) :
    p.sixY * p.sixY - p.sixY - 6 = 0 :=
  p.sixY_carrier_polynomial

/-! ## Layer 2 — Boundary involution to projectors -/

noncomputable example {A : Type*} [Ring A] [Invertible (2 : A)]
    (c : TFPT.Carrier.InvolutionProjectors.CarrierInvolution A) :
    TFPT.Carrier.Polarization A :=
  c.toPolarization

example {A : Type*} [Ring A] [Invertible (2 : A)]
    (c : TFPT.Carrier.InvolutionProjectors.CarrierInvolution A) :
    c.Pminus * c.Pminus = c.Pminus :=
  c.Pminus_idem

example {A : Type*} [Ring A] [Invertible (2 : A)]
    (c : TFPT.Carrier.InvolutionProjectors.CarrierInvolution A) :
    c.Pminus + c.Pplus = 1 :=
  c.Pminus_add_Pplus

/-! ## Layer 3 — Discrete rigidity -/

example
    (m n : ℕ) (hm : 0 < m) (hn : 0 < n) (qm qp : ℤ)
    (htrace : (m : ℤ) * qm + (n : ℤ) * qp = 0)
    (hneg : qm < 0) (hpos : 0 < qp)
    (hgcd : Int.gcd qm qp = 1) :
    qm = -((n / Nat.gcd m n : ℕ) : ℤ) ∧
    qp = ((m / Nat.gcd m n : ℕ) : ℤ) :=
  TFPT.Carrier.LatticeRigidityGeneral.primitive_trace_free_pair_general
    m n hm hn qm qp htrace hneg hpos hgcd

example
    (qm qp : ℤ)
    (htrace : 3 * qm + 2 * qp = 0)
    (hneg : qm < 0) (hpos : 0 < qp)
    (hgcd : Int.gcd qm qp = 1) :
    qm = -2 ∧ qp = 3 :=
  TFPT.Carrier.Rigidity.unique_carrier_pair qm qp htrace hneg hpos hgcd

example (c : TFPT.Carrier.OrientedDeterminantCarrier.PrimitiveOrientedDeterminantCarrier 3 2) :
    c.q_minus = -2 ∧ c.q_plus = 3 :=
  c.sm_pair_eq

/-! ## Layer 4 — Structural trace -/

example
    {K M : Type*} [Field K] [AddCommGroup M] [Module K M]
    [FiniteDimensional K M]
    (Pm Pp : M →ₗ[K] M)
    (hm : IsIdempotentElem Pm) (hp : IsIdempotentElem Pp)
    (a b : K) :
    LinearMap.trace K M (a • Pm + b • Pp)
      = a * (Module.finrank K (LinearMap.range Pm) : K)
        + b * (Module.finrank K (LinearMap.range Pp) : K) :=
  TFPT.Carrier.TraceProjection.trace_linear_combination_of_idempotents Pm Pp hm hp a b

/-! ## Layer 5 — Determinant character -/

example
    {K : Type*} [Field K] {m n : ℕ}
    (lam : K) (qm qp : ℤ) (hlam : lam ≠ 0) :
    Matrix.det (TFPT.Carrier.DeterminantCharacter.torusMatrix K m n lam qm qp)
      = lam ^ ((m : ℤ) * qm + (n : ℤ) * qp) :=
  TFPT.Carrier.DeterminantCharacter.det_torusMatrix lam qm qp hlam

/-! ## Layer 6 — Stage A rank certificates -/

example
    {K : Type*} [Field K]
    {Eplus : Type*} [AddCommGroup Eplus] [Module K Eplus]
    (cert : TFPT.Carrier.HiggsIndexShadow.HiggsIndexCertificate K Eplus) :
    Module.finrank K Eplus = 2 :=
  cert.finrank_Eplus_eq_two

example
    {K : Type*} [Field K]
    {Eminus : Type*} [AddCommGroup Eminus] [Module K Eminus]
    (cert : TFPT.Carrier.YukawaRank.YukawaRankCertificate K Eminus) :
    Module.finrank K Eminus = 3 :=
  cert.finrank_Eminus_eq_three

/-! ## Layer 6b — Yukawa Stage B (top form) -/

example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E] [FiniteDimensional K E]
    (Y : TFPT.Carrier.YukawaTopForm.YukawaTopForm K E) :
    Module.finrank K E = 3 :=
  Y.finrank_E_eq_three

example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E] [FiniteDimensional K E] :
    Nonempty (TFPT.Carrier.YukawaTopForm.YukawaTopForm K E)
      ↔ Module.finrank K E = 3 :=
  TFPT.Carrier.YukawaTopForm.YukawaTopForm.nonempty_iff_finrank_eq_three

/-! ## Layer 6c — Yukawa Stage C (contraction iso) -/

example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E] [FiniteDimensional K E]
    (Y : TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling K E) :
    Module.finrank K E = 3 :=
  Y.finrank_E_eq_three

example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E] [FiniteDimensional K E] :
    Nonempty (TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling K E)
      ↔ Module.finrank K E = 3 :=
  TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling.nonempty_iff_finrank_eq_three

/-! ## Layer 6d — Yukawa Stage D (primary trilinear form) -/

example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E] [FiniteDimensional K E] [Nontrivial E]
    (Y : TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm K E)
    (hinj : Y.ContractionInjective)
    (hsurj : Y.ContractionSurjective) :
    Module.finrank K E = 3 :=
  Y.finrank_E_eq_three hinj hsurj

example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E] [FiniteDimensional K E] [Nontrivial E]
    (Y : TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm K E)
    (h : Y.PrimitiveIndecomposableYukawaCondition) :
    Module.finrank K E = 3 :=
  Y.finrank_E_eq_three_of_condition h

/-- Without `Nontrivial`, the correct statement is the disjunction
`dim E = 0 ∨ dim E = 3`. This signature lock verifies the
transparency theorem of v9. -/
example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E] [FiniteDimensional K E]
    (Y : TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm K E)
    (hinj : Y.ContractionInjective)
    (hsurj : Y.ContractionSurjective) :
    Module.finrank K E = 0 ∨ Module.finrank K E = 3 :=
  Y.finrank_E_eq_zero_or_three hinj hsurj

/-! ## Layer 0+ — Calderon projector (Paper 1 structural) -/

example {A : Type*} [Ring A] [Invertible (2 : A)]
    (c : TFPT.Carrier.CalderonProjector.CalderonProjector A) :
    c.eps * c.eps = 1 :=
  c.eps_sq

noncomputable example {A : Type*} [Ring A] [Invertible (2 : A)]
    (c : TFPT.Carrier.CalderonProjector.CalderonProjector A) :
    TFPT.Carrier.InvolutionProjectors.CarrierInvolution A :=
  c.toCarrierInvolution

noncomputable example {A : Type*} [Ring A] [Invertible (2 : A)]
    (c : TFPT.Carrier.CalderonProjector.CalderonProjector A) :
    TFPT.Carrier.CalderonInterface.CalderonCertificate A :=
  c.toCalderonCertificate

/-! ## Layer 0++ — Boundary polarisation (v10 upstream layer) -/

noncomputable example
    {K : Type*} [Field K]
    {H : Type*} [AddCommGroup H] [Module K H]
    (P : TFPT.Carrier.BoundaryPolarization.BoundaryPolarization K H) :
    Module.End K H := P.projector

example
    {K : Type*} [Field K]
    {H : Type*} [AddCommGroup H] [Module K H]
    (P : TFPT.Carrier.BoundaryPolarization.BoundaryPolarization K H) :
    P.projector * P.projector = P.projector :=
  P.projector_isIdempotent

noncomputable example
    {K : Type*} [Field K] [Invertible (2 : K)]
    {H : Type*} [AddCommGroup H] [Module K H]
    (P : TFPT.Carrier.BoundaryPolarization.BoundaryPolarization K H) :
    TFPT.Carrier.CalderonProjector.CalderonProjector (Module.End K H) :=
  P.toCalderonProjector

/-! ## Layer 6+ — Higgs Stage B (degree-1 two-variable forms) -/

example {K : Type*} [Field K] :
    Module.finrank K (TFPT.Carrier.HiggsTopForm.DegreeOneTwoVarForm K) = 2 :=
  TFPT.Carrier.HiggsTopForm.DegreeOneTwoVarForm.finrank_eq_two K

example
    {K : Type*} [Field K]
    {Eplus : Type*} [AddCommGroup Eplus] [Module K Eplus]
    (h : TFPT.Carrier.HiggsTopForm.HiggsTopForm K Eplus) :
    Module.finrank K Eplus = 2 :=
  h.finrank_Eplus_eq_two

noncomputable example
    {K : Type*} [Field K]
    {Eplus : Type*} [AddCommGroup Eplus] [Module K Eplus]
    (h : TFPT.Carrier.HiggsTopForm.HiggsTopForm K Eplus) :
    TFPT.Carrier.HiggsIndexShadow.HiggsIndexCertificate K Eplus :=
  h.toHiggsIndexCertificate

/-! ## Layer 6++ — Higgs scheme-cohomology shadow (v10) -/

noncomputable example
    {K : Type*} [Field K] :
    TFPT.Carrier.HiggsTopForm.DegreeOneTwoVarForm K ≃ₗ[K]
      TFPT.Carrier.HiggsSchemeCohomologyShadow.O_one K :=
  TFPT.Carrier.HiggsSchemeCohomologyShadow.toDegreeOneTwoVarForm

example
    {K : Type*} [Field K] :
    Module.finrank K (TFPT.Carrier.HiggsSchemeCohomologyShadow.O_one K) = 2 :=
  TFPT.Carrier.HiggsSchemeCohomologyShadow.finrank_O_one_eq_two

noncomputable example
    {K : Type*} [Field K]
    {Eplus : Type*} [AddCommGroup Eplus] [Module K Eplus]
    (h : Eplus ≃ₗ[K] TFPT.Carrier.HiggsSchemeCohomologyShadow.O_one K) :
    TFPT.Carrier.HiggsTopForm.HiggsTopForm K Eplus :=
  TFPT.Carrier.HiggsSchemeCohomologyShadow.toHiggsTopForm h

/-! ## Layer 6d+ — Yukawa Stage D backward (v10) -/

noncomputable example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E]
    (b : Module.Basis (Fin 3) K E) :
    TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm K E :=
  TFPT.Carrier.YukawaStageDExistence.ofBasis b

example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E]
    (b : Module.Basis (Fin 3) K E) :
    (TFPT.Carrier.YukawaStageDExistence.ofBasis b).ContractionInjective :=
  TFPT.Carrier.YukawaStageDExistence.ofBasis_contractionInjective b

example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E] [FiniteDimensional K E]
    (b : Module.Basis (Fin 3) K E) :
    (TFPT.Carrier.YukawaStageDExistence.ofBasis b).ContractionSurjective :=
  TFPT.Carrier.YukawaStageDExistence.ofBasis_contractionSurjective b

example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E] [FiniteDimensional K E]
    (h : Module.finrank K E = 3) :
    ∃ Y : TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm K E,
      Y.ContractionInjective ∧ Y.ContractionSurjective :=
  TFPT.Carrier.YukawaStageDExistence.exists_yukawaTrilinearForm_of_finrank_eq_three h

example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E]
    [FiniteDimensional K E] [Nontrivial E] :
    (∃ Y : TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm K E,
        Y.ContractionInjective ∧ Y.ContractionSurjective) ↔
      Module.finrank K E = 3 :=
  TFPT.Carrier.YukawaStageDExistence.stage_D_iff_finrank_eq_three

/-! ## Layer 0++ — CarrierInvolution → BoundaryPolarization (v11 converse) -/

/-- The converse direction of `BoundaryPolarization.toCarrierInvolution`,
closing the equivalence between the polarisation picture and the
involution picture for `A = Module.End K H`. -/
noncomputable example
    {K : Type*} [Field K] [Invertible (2 : K)]
    {H : Type*} [AddCommGroup H] [Module K H]
    (c : TFPT.Carrier.InvolutionProjectors.CarrierInvolution
          (Module.End K H)) :
    TFPT.Carrier.BoundaryPolarization.BoundaryPolarization K H :=
  TFPT.Carrier.BoundaryPolarization.BoundaryPolarization.ofCarrierInvolution c

/-! ## Layer 3b+ — Seam-winding interface (v11 upstream) -/

example {m n : ℕ}
    (s : TFPT.Carrier.SeamWindingInterface.SeamWindingData m n) :
    TFPT.Carrier.OrientedDeterminantCarrier.PrimitiveOrientedDeterminantCarrier m n :=
  s.toPrimitiveOrientedDeterminantCarrier

example {m n : ℕ}
    (c : TFPT.Carrier.OrientedDeterminantCarrier.PrimitiveOrientedDeterminantCarrier m n) :
    TFPT.Carrier.SeamWindingInterface.SeamWindingData m n :=
  TFPT.Carrier.SeamWindingInterface.SeamWindingData.ofPrimitiveOrientedDeterminantCarrier c

example (s : TFPT.Carrier.SeamWindingInterface.SeamWindingData 3 2) :
    s.q_minus = -2 ∧ s.q_plus = 3 :=
  s.sm_pair_eq

/-! ## Layer 6d++ — Boundary Yukawa Kernel interface (v11 upstream) -/

example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E] [FiniteDimensional K E]
    (b : TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel K E) :
    Module.finrank K E = 3 :=
  b.finrank_E_eq_three

noncomputable example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E]
    [FiniteDimensional K E] [Nontrivial E]
    (h : Module.finrank K E = 3) :
    TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel K E :=
  TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel.ofFinrankEqThree h

example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E]
    [FiniteDimensional K E] [Nontrivial E] :
    Nonempty (TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel K E) ↔
      Module.finrank K E = 3 :=
  TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel.nonempty_iff_finrank_eq_three

noncomputable example
    {K : Type*} [Field K]
    {E : Type*} [AddCommGroup E] [Module K E] [FiniteDimensional K E]
    (b : TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel K E) :
    TFPT.Carrier.YukawaRank.YukawaRankCertificate K E :=
  b.toYukawaRankCertificate

/-! ## Layer 7 — Mathlib bridge -/

example
    {A : Type*} [Ring A]
    (p : TFPT.Carrier.Polarization A) :
    CompleteOrthogonalIdempotents ![p.Pm, p.Pp] :=
  TFPT.Carrier.MathlibBridge.Polarization.toCompleteOrthogonalIdempotents p

/-! ## Layer 8 — Bundled main theorems -/

example
    {K M : Type*} [Field K] [CharZero K]
    [AddCommGroup M] [Module K M] [FiniteDimensional K M]
    (cp : TFPT.Carrier.CarrierData.CarrierPremises K M) :
    LinearMap.trace K M cp.Y = 0 :=
  cp.trace_Y_eq_zero

example
    {K M : Type*} [Field K] [CharZero K]
    [AddCommGroup M] [Module K M] [FiniteDimensional K M]
    (cp : TFPT.Carrier.CarrierData.CarrierPremises K M) :
    (6 : ℕ) • (cp.Y * cp.Y) - cp.Y - 1 = (0 : Module.End K M) :=
  cp.carrier_polynomial_Y

example
    {K M : Type*} [Field K] [CharZero K]
    [AddCommGroup M] [Module K M] [FiniteDimensional K M]
    (cp : TFPT.Carrier.CarrierData.CarrierPremises K M)
    (qm qp : ℤ)
    (htrace : 3 * qm + 2 * qp = 0)
    (hsign_m : qm < 0) (hsign_p : 0 < qp)
    (hgcd : Int.gcd qm qp = 1) :
    (qm = -2 ∧ qp = 3)
    ∧ LinearMap.trace K M cp.Y = 0
    ∧ (6 : ℕ) • (cp.Y * cp.Y) - cp.Y - 1 = (0 : Module.End K M) :=
  cp.hypercharge_carrier_packet qm qp htrace hsign_m hsign_p hgcd

/-! ## Concrete 5×5 model -/

example : (TFPT.Carrier.Hypercharge.Y).trace = 0 :=
  TFPT.Carrier.Hypercharge.trace_Y

example : (6 : ℚ) • (TFPT.Carrier.Hypercharge.Y * TFPT.Carrier.Hypercharge.Y)
            - TFPT.Carrier.Hypercharge.Y - 1 = 0 :=
  TFPT.Carrier.Hypercharge.Y_carrier_polynomial

end TFPT.Carrier.AuditContract
