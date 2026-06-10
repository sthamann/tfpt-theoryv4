/-
  TFPT Carrier — Audit Check (Lean-side)
  --------------------------------------

  Companion of `scripts/audit.sh`. By going through Lean's
  `#check` rather than `grep`, this file enforces that every
  headline theorem actually *typechecks* — comments, dead code,
  and misspellings cannot fake a pass.

  If a headline theorem disappears, is renamed, or fails to
  elaborate, this file fails to build, and `scripts/audit.sh`
  catches it via the `lake build` step.

  Run:
      lake env lean TfptCarrier/AuditCheck.lean
-/

import TfptCarrier.Polarization
import TfptCarrier.InvolutionProjectors
import TfptCarrier.CalderonInterface
import TfptCarrier.CalderonProjector
import TfptCarrier.BoundaryPolarization
import TfptCarrier.MathlibBridge
import TfptCarrier.LatticeRigidityGeneral
import TfptCarrier.CarrierRankUniqueness
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

-- Layer 1: Polarization (algebraic core)
#check @TFPT.Carrier.Polarization.sixY_carrier_polynomial

-- Layer 2: Involution → Projectors
#check @TFPT.Carrier.InvolutionProjectors.CarrierInvolution.toPolarization
#check @TFPT.Carrier.InvolutionProjectors.CarrierInvolution.Pminus_idem
#check @TFPT.Carrier.InvolutionProjectors.CarrierInvolution.Pplus_idem
#check @TFPT.Carrier.InvolutionProjectors.CarrierInvolution.Pminus_mul_Pplus
#check @TFPT.Carrier.InvolutionProjectors.CarrierInvolution.Pplus_mul_Pminus
#check @TFPT.Carrier.InvolutionProjectors.CarrierInvolution.Pminus_add_Pplus

-- Layer 3: Rigidity
#check @TFPT.Carrier.LatticeRigidityGeneral.primitive_trace_free_pair_general
#check @TFPT.Carrier.LatticeRigidityGeneral.primitive_trace_free_pair_3_2
#check @TFPT.Carrier.Rigidity.unique_carrier_pair

-- Layer 3a: Theorem A — carrier rank uniqueness (g_car = 5)
#check @TFPT.Carrier.CarrierRankUniqueness.pascal_growth
#check @TFPT.Carrier.CarrierRankUniqueness.carrier_rank_pascal_unique
#check @TFPT.Carrier.CarrierRankUniqueness.g_car_unique
#check @TFPT.Carrier.CarrierRankUniqueness.carrier_closure_integers

-- Layer 3b: Primitive oriented determinant-preserving carrier bundle
#check @TFPT.Carrier.OrientedDeterminantCarrier.PrimitiveOrientedDeterminantCarrier.to_rigidity_pair_eq
#check @TFPT.Carrier.OrientedDeterminantCarrier.PrimitiveOrientedDeterminantCarrier.sm_pair_eq

-- Layer 4: Structural trace
#check @TFPT.Carrier.TraceProjection.trace_linear_combination_of_idempotents
#check @TFPT.Carrier.TraceProjection.trace_carrier_Y_eq_zero

-- Layer 5: Determinant character (universal-λ headline + at-two helper)
#check @TFPT.Carrier.DeterminantCharacter.det_torusMatrix
#check @TFPT.Carrier.DeterminantCharacter.trace_zero_of_det_one_forall_rat
#check @TFPT.Carrier.DeterminantCharacter.trace_zero_of_det_one_at_two

-- Layer 6: Stage-A rank certificates
#check @TFPT.Carrier.HiggsIndexShadow.finrank_degreeOneBinaryForms
#check @TFPT.Carrier.HiggsIndexShadow.HiggsIndexCertificate.finrank_Eplus_eq_two
#check @TFPT.Carrier.YukawaRank.finrank_negativeBlockShadow
#check @TFPT.Carrier.YukawaRank.YukawaRankCertificate.finrank_Eminus_eq_three

-- Layer 6b: Yukawa Stage-B (algebraic content via Λ³E)
#check @TFPT.Carrier.YukawaTopForm.YukawaTopForm.finrank_lambda3_eq_one
#check @TFPT.Carrier.YukawaTopForm.YukawaTopForm.finrank_E_eq_three
#check @TFPT.Carrier.YukawaTopForm.YukawaTopForm.toYukawaRankCertificate
#check @TFPT.Carrier.YukawaTopForm.YukawaTopForm.ofFinrankEqThree
#check @TFPT.Carrier.YukawaTopForm.YukawaTopForm.nonempty_iff_finrank_eq_three

-- Layer 6c: Yukawa Stage-C (primitive indecomposable coupling via contraction iso)
#check @TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling.finrank_E_eq_three
#check @TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling.toYukawaTopForm
#check @TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling.toYukawaRankCertificate
#check @TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling.ofFinrankEqThree
#check @TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling.nonempty_iff_finrank_eq_three

-- Layer 6d: Yukawa Stage-D (trilinear form with derived contraction map)
#check @TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.contraction
#check @TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.ContractionInjective
#check @TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.ContractionSurjective
#check @TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.PrimitiveIndecomposableYukawaCondition
#check @TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.contractionEquivOfBoth
#check @TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.toPrimitiveIndecomposableYukawaCoupling
#check @TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.finrank_E_eq_three
#check @TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.finrank_E_eq_three_of_condition
#check @TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.finrank_E_eq_zero_or_three

-- Layer 0 (interface): Calderon certificate from Paper 1
#check @TFPT.Carrier.CalderonInterface.CalderonCertificate.toCarrierInvolution
#check @TFPT.Carrier.CalderonInterface.CalderonCertificate.ofCarrierInvolution

-- Layer 0+ (structural): Calderon projector ⟹ ε² = 1
#check @TFPT.Carrier.CalderonProjector.CalderonProjector.eps
#check @TFPT.Carrier.CalderonProjector.CalderonProjector.eps_sq
#check @TFPT.Carrier.CalderonProjector.CalderonProjector.toCarrierInvolution
#check @TFPT.Carrier.CalderonProjector.CalderonProjector.toCalderonCertificate

-- Layer 0++ (upstream, v10): BoundaryPolarization ⟹ CalderonProjector
#check @TFPT.Carrier.BoundaryPolarization.BoundaryPolarization.projector
#check @TFPT.Carrier.BoundaryPolarization.BoundaryPolarization.projector_isIdempotent
#check @TFPT.Carrier.BoundaryPolarization.BoundaryPolarization.toCalderonProjector
#check @TFPT.Carrier.BoundaryPolarization.BoundaryPolarization.toCalderonCertificate
#check @TFPT.Carrier.BoundaryPolarization.BoundaryPolarization.toCarrierInvolution

-- Layer 6+ (Higgs Stage B: degree-1 two-variable form ⟹ dim Eplus = 2)
#check @TFPT.Carrier.HiggsTopForm.DegreeOneTwoVarForm.toBinaryForms
#check @TFPT.Carrier.HiggsTopForm.DegreeOneTwoVarForm.finrank_eq_two
#check @TFPT.Carrier.HiggsTopForm.HiggsTopForm.finrank_Eplus_eq_two
#check @TFPT.Carrier.HiggsTopForm.HiggsTopForm.toHiggsIndexCertificate

-- Layer 6++ (Higgs scheme-cohomology shadow, v10): K[X,Y]_1 ≃ DegreeOneTwoVarForm
#check @TFPT.Carrier.HiggsSchemeCohomologyShadow.toDegreeOneTwoVarForm
#check @TFPT.Carrier.HiggsSchemeCohomologyShadow.finrank_O_one_eq_two
#check @TFPT.Carrier.HiggsSchemeCohomologyShadow.toHiggsTopForm

-- Layer 6d+ (Yukawa Stage D backward, v10): dim E = 3 ⟹ ∃ω with CI ∧ CS
#check @TFPT.Carrier.YukawaStageDExistence.ofBasis
#check @TFPT.Carrier.YukawaStageDExistence.ofFinrankEqThree
#check @TFPT.Carrier.YukawaStageDExistence.ofBasis_contractionInjective
#check @TFPT.Carrier.YukawaStageDExistence.ofBasis_contractionSurjective
#check @TFPT.Carrier.YukawaStageDExistence.ofBasis_satisfies_condition
#check @TFPT.Carrier.YukawaStageDExistence.exists_yukawaTrilinearForm_of_finrank_eq_three
#check @TFPT.Carrier.YukawaStageDExistence.stage_D_iff_finrank_eq_three

-- Layer 0++ (v11): CarrierInvolution → BoundaryPolarization (converse)
#check @TFPT.Carrier.BoundaryPolarization.BoundaryPolarization.ofCarrierInvolution

-- Layer 3b+ (v11): Seam-winding interface (upstream of OrientedDeterminantCarrier)
#check @TFPT.Carrier.SeamWindingInterface.SeamWindingData
#check @TFPT.Carrier.SeamWindingInterface.SeamWindingData.toPrimitiveOrientedDeterminantCarrier
#check @TFPT.Carrier.SeamWindingInterface.SeamWindingData.ofPrimitiveOrientedDeterminantCarrier
#check @TFPT.Carrier.SeamWindingInterface.SeamWindingData.sm_pair_eq

-- Layer 6d++ (v11): Boundary Yukawa Kernel interface (upstream typed target)
#check @TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel
#check @TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel.finrank_E_eq_three
#check @TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel.ofFinrankEqThree
#check @TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel.nonempty_iff_finrank_eq_three
#check @TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel.toYukawaRankCertificate

-- Layer 7: Mathlib bridge
#check @TFPT.Carrier.MathlibBridge.Polarization.toCompleteOrthogonalIdempotents
#check @TFPT.Carrier.MathlibBridge.Polarization.ofCompleteOrthogonalIdempotents

-- Layer 8: Bundled main theorems
#check @TFPT.Carrier.CarrierData.CarrierPremises.primitive_pair_eq_sm
#check @TFPT.Carrier.CarrierData.CarrierPremises.trace_Y_eq_zero
#check @TFPT.Carrier.CarrierData.CarrierPremises.carrier_polynomial_Y
#check @TFPT.Carrier.CarrierData.CarrierPremises.hypercharge_carrier_packet

-- Concrete 5×5 model
#check @TFPT.Carrier.Hypercharge.trace_Y
#check @TFPT.Carrier.Hypercharge.Y_carrier_polynomial

-- Glue uniqueness + carrier index (v89/v92 arithmetic cores)
#check @TFPT.Carrier.GlueUniqueness.isotropic_elements_classified
#check @TFPT.Carrier.GlueUniqueness.isotropic_order4_classified
#check @TFPT.Carrier.GlueUniqueness.orbit33_eq_H1
#check @TFPT.Carrier.GlueUniqueness.orbit31_eq_H2
#check @TFPT.Carrier.GlueUniqueness.glues_isotropic
#check @TFPT.Carrier.GlueUniqueness.klein_not_isotropic
#check @TFPT.Carrier.GlueUniqueness.spinor_swap_exchanges
#check @TFPT.Carrier.GlueUniqueness.unique_halfway_stage
#check @TFPT.Carrier.GlueUniqueness.carrier_index_lemma
#check @TFPT.Carrier.GlueUniqueness.glue_sectors_are_currents
