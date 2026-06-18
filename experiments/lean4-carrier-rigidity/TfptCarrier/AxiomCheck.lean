/-
  TFPT Carrier — Axiom Check
  --------------------------

  Prints the axioms each main theorem depends on. A clean Lean 4
  formalisation should only depend on the three standard axioms:

      Classical.choice
      Quot.sound
      propext

  Run with:

      lake env lean TfptCarrier/AxiomCheck.lean
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
import TfptCarrier.MobiusUniformisation
import TfptCarrier.CohomologyGrading

-- Layer 1: Polarization (algebraic core)
#print axioms TFPT.Carrier.Polarization.sixY_carrier_polynomial

-- Layer 2: Involution → Projectors
#print axioms TFPT.Carrier.InvolutionProjectors.CarrierInvolution.Pminus_idem
#print axioms TFPT.Carrier.InvolutionProjectors.CarrierInvolution.Pplus_idem
#print axioms TFPT.Carrier.InvolutionProjectors.CarrierInvolution.Pminus_mul_Pplus
#print axioms TFPT.Carrier.InvolutionProjectors.CarrierInvolution.Pplus_mul_Pminus

-- Layer 3: Rigidity (general + SM specialisation)
#print axioms TFPT.Carrier.LatticeRigidityGeneral.primitive_trace_free_pair_general
#print axioms TFPT.Carrier.LatticeRigidityGeneral.primitive_trace_free_pair_3_2
#print axioms TFPT.Carrier.Rigidity.unique_carrier_pair

-- Layer 4: Structural trace
#print axioms TFPT.Carrier.TraceProjection.trace_linear_combination_of_idempotents
#print axioms TFPT.Carrier.TraceProjection.trace_carrier_Y_eq_zero

-- Layer 5: Determinant character (forall-λ headline + at-two helper)
#print axioms TFPT.Carrier.DeterminantCharacter.det_torusMatrix
#print axioms TFPT.Carrier.DeterminantCharacter.trace_zero_of_det_one_forall_rat
#print axioms TFPT.Carrier.DeterminantCharacter.trace_zero_of_det_one_at_two

-- Layer 6: Higgs and Yukawa Stage-A rank certificates
#print axioms TFPT.Carrier.HiggsIndexShadow.finrank_degreeOneBinaryForms
#print axioms TFPT.Carrier.HiggsIndexShadow.HiggsIndexCertificate.finrank_Eplus_eq_two
#print axioms TFPT.Carrier.YukawaRank.finrank_negativeBlockShadow
#print axioms TFPT.Carrier.YukawaRank.YukawaRankCertificate.finrank_Eminus_eq_three

-- Layer 6b: Yukawa Stage-B (top form Λ³E = 1-dim ⟹ dim E = 3)
#print axioms TFPT.Carrier.YukawaTopForm.YukawaTopForm.finrank_lambda3_eq_one
#print axioms TFPT.Carrier.YukawaTopForm.YukawaTopForm.finrank_E_eq_three
#print axioms TFPT.Carrier.YukawaTopForm.YukawaTopForm.toYukawaRankCertificate
#print axioms TFPT.Carrier.YukawaTopForm.YukawaTopForm.ofFinrankEqThree
#print axioms TFPT.Carrier.YukawaTopForm.YukawaTopForm.nonempty_iff_finrank_eq_three

-- Layer 6c: Yukawa Stage-C (contraction iso ⟹ dim E = 3)
#print axioms TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling.finrank_E_eq_three
#print axioms TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling.toYukawaTopForm
#print axioms TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling.toYukawaRankCertificate
#print axioms TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling.ofFinrankEqThree
#print axioms TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling.nonempty_iff_finrank_eq_three

-- Layer 6d: Yukawa Stage-D (trilinear form with derived contraction)
#print axioms TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.contraction
#print axioms TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.contractionEquivOfBoth
#print axioms TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.toPrimitiveIndecomposableYukawaCoupling
#print axioms TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.finrank_E_eq_three
#print axioms TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.finrank_E_eq_three_of_condition
#print axioms TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.finrank_E_eq_zero_or_three

-- Layer 3b: Primitive oriented determinant carrier (carrier-rigidity bundle)
#print axioms TFPT.Carrier.OrientedDeterminantCarrier.PrimitiveOrientedDeterminantCarrier.to_rigidity_pair_eq
#print axioms TFPT.Carrier.OrientedDeterminantCarrier.PrimitiveOrientedDeterminantCarrier.sm_pair_eq

-- Layer 0 (interface): Calderon certificate from Paper 1
#print axioms TFPT.Carrier.CalderonInterface.CalderonCertificate.toCarrierInvolution
#print axioms TFPT.Carrier.CalderonInterface.CalderonCertificate.ofCarrierInvolution

-- Layer 0+ (structural): Calderon projector (idempotent π ⟹ ε² = 1)
#print axioms TFPT.Carrier.CalderonProjector.CalderonProjector.eps_sq
#print axioms TFPT.Carrier.CalderonProjector.CalderonProjector.toCarrierInvolution
#print axioms TFPT.Carrier.CalderonProjector.CalderonProjector.toCalderonCertificate

-- Layer 0++ (upstream, v10): BoundaryPolarization ⟹ CalderonProjector
#print axioms TFPT.Carrier.BoundaryPolarization.BoundaryPolarization.projector_isIdempotent
#print axioms TFPT.Carrier.BoundaryPolarization.BoundaryPolarization.toCalderonProjector
#print axioms TFPT.Carrier.BoundaryPolarization.BoundaryPolarization.toCalderonCertificate
#print axioms TFPT.Carrier.BoundaryPolarization.BoundaryPolarization.toCarrierInvolution

-- Layer 6+ (Higgs Stage B: degree-1 two-variable form ⟹ dim E = 2)
#print axioms TFPT.Carrier.HiggsTopForm.DegreeOneTwoVarForm.finrank_eq_two
#print axioms TFPT.Carrier.HiggsTopForm.HiggsTopForm.finrank_Eplus_eq_two
#print axioms TFPT.Carrier.HiggsTopForm.HiggsTopForm.toHiggsIndexCertificate

-- Layer 6++ (Higgs scheme-cohomology shadow, v10): K[X,Y]_1 ≃ DegreeOneTwoVarForm
#print axioms TFPT.Carrier.HiggsSchemeCohomologyShadow.toDegreeOneTwoVarForm
#print axioms TFPT.Carrier.HiggsSchemeCohomologyShadow.finrank_O_one_eq_two
#print axioms TFPT.Carrier.HiggsSchemeCohomologyShadow.toHiggsTopForm

-- Layer 6d+ (Yukawa Stage D backward, v10): dim E = 3 ⟹ ∃ω with CI ∧ CS
#print axioms TFPT.Carrier.YukawaStageDExistence.ofBasis
#print axioms TFPT.Carrier.YukawaStageDExistence.ofFinrankEqThree
#print axioms TFPT.Carrier.YukawaStageDExistence.ofBasis_contractionInjective
#print axioms TFPT.Carrier.YukawaStageDExistence.ofBasis_contractionSurjective
#print axioms TFPT.Carrier.YukawaStageDExistence.exists_yukawaTrilinearForm_of_finrank_eq_three
#print axioms TFPT.Carrier.YukawaStageDExistence.stage_D_iff_finrank_eq_three

-- Layer 0++ (v11): CarrierInvolution → BoundaryPolarization (converse)
#print axioms TFPT.Carrier.BoundaryPolarization.BoundaryPolarization.ofCarrierInvolution

-- Layer 3b+ (v11): Seam-winding interface (upstream of OrientedDeterminantCarrier)
#print axioms TFPT.Carrier.SeamWindingInterface.SeamWindingData.toPrimitiveOrientedDeterminantCarrier
#print axioms TFPT.Carrier.SeamWindingInterface.SeamWindingData.ofPrimitiveOrientedDeterminantCarrier
#print axioms TFPT.Carrier.SeamWindingInterface.SeamWindingData.sm_pair_eq

-- Layer 6d++ (v11): Boundary Yukawa Kernel interface (upstream typed target)
#print axioms TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel.finrank_E_eq_three
#print axioms TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel.ofFinrankEqThree
#print axioms TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel.nonempty_iff_finrank_eq_three
#print axioms TFPT.Carrier.BoundaryYukawaKernelInterface.BoundaryYukawaKernel.toYukawaRankCertificate

-- Layer 7: Mathlib bridge
#print axioms TFPT.Carrier.MathlibBridge.Polarization.toCompleteOrthogonalIdempotents

-- Layer 8: Bundled main theorems
#print axioms TFPT.Carrier.CarrierData.CarrierPremises.primitive_pair_eq_sm
#print axioms TFPT.Carrier.CarrierData.CarrierPremises.trace_Y_eq_zero
#print axioms TFPT.Carrier.CarrierData.CarrierPremises.carrier_polynomial_Y
#print axioms TFPT.Carrier.CarrierData.CarrierPremises.hypercharge_carrier_packet

-- Concrete 5×5 model
#print axioms TFPT.Carrier.Hypercharge.trace_Y
#print axioms TFPT.Carrier.Hypercharge.Y_carrier_polynomial

-- Glue uniqueness + carrier index (v89/v92 arithmetic cores)
#print axioms TFPT.Carrier.GlueUniqueness.isotropic_elements_classified
#print axioms TFPT.Carrier.GlueUniqueness.isotropic_order4_classified
#print axioms TFPT.Carrier.GlueUniqueness.orbit33_eq_H1
#print axioms TFPT.Carrier.GlueUniqueness.orbit31_eq_H2
#print axioms TFPT.Carrier.GlueUniqueness.glues_isotropic
#print axioms TFPT.Carrier.GlueUniqueness.klein_not_isotropic
#print axioms TFPT.Carrier.GlueUniqueness.spinor_swap_exchanges
#print axioms TFPT.Carrier.GlueUniqueness.unique_halfway_stage
#print axioms TFPT.Carrier.GlueUniqueness.carrier_index_lemma
#print axioms TFPT.Carrier.GlueUniqueness.glue_sectors_are_currents

-- Seam-deck closure (QGEO.SYM.01 conditional theorem; v201/v210 algebraic core)
#print axioms TFPT.Carrier.SeamDeckClosure.geom_sum_fourth_root
#print axioms TFPT.Carrier.SeamDeckClosure.clock_gen_pow_four
#print axioms TFPT.Carrier.SeamDeckClosure.mark_sum_residue_nonzero
#print axioms TFPT.Carrier.SeamDeckClosure.markLocal_blockDiagonal
#print axioms TFPT.Carrier.SeamDeckClosure.SeamDeckPremise.clock_invariant
#print axioms TFPT.Carrier.SeamDeckClosure.diagonal_commutesClock
#print axioms TFPT.Carrier.SeamDeckClosure.flat_all_orders_clock

-- Möbius uniformisation (QGEO.UNIFORM.01 geometric normal form; v177)
#print axioms TFPT.Carrier.MobiusUniformisation.rho_pow_four
#print axioms TFPT.Carrier.MobiusUniformisation.sigma_rho_sigma
#print axioms TFPT.Carrier.MobiusUniformisation.orbit_scales_to_mu4
#print axioms TFPT.Carrier.MobiusUniformisation.sigma_perm_mu4
#print axioms TFPT.Carrier.MobiusUniformisation.mult_order_four_iff
#print axioms TFPT.Carrier.MobiusUniformisation.uniformisation_normal_form

-- Cohomology grading (QGEO.COHOM.01 character node + MODULE parity; v177)
#print axioms TFPT.Carrier.CohomologyGrading.omega1_pullback
#print axioms TFPT.Carrier.CohomologyGrading.omega2_pullback
#print axioms TFPT.Carrier.CohomologyGrading.omega3_pullback
#print axioms TFPT.Carrier.CohomologyGrading.omega1_reflection
#print axioms TFPT.Carrier.CohomologyGrading.cohom_grading
