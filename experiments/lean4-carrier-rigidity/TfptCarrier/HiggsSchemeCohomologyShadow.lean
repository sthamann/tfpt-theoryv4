/-
  TFPT Carrier — Higgs Stage B+: Scheme-Cohomology Shadow
  --------------------------------------------------------

  v10 upstream layer for the Higgs Stage-B interface.

  In algebraic geometry, the projective line over `K` is defined
  as `ℙ¹_K = Proj K[X, Y]`, and the line bundle `O(n)` has
  global sections

      H^0(ℙ¹_K, O(n)) ≅ K[X, Y]_n

  where `K[X, Y]_n` is the degree-`n` homogeneous part of the
  graded ring `K[X, Y]`. In particular,

      H^0(ℙ¹_K, O(1)) ≅ K[X, Y]_1 = {α X + β Y : α, β ∈ K}.

  This module formalises the *algebraic identification of the
  Stage-B shadow with the graded-ring degree-1 piece*. Mathlib's
  `MvPolynomial.homogeneousSubmodule (Fin 2) K 1` is precisely
  the degree-1 part of `K[X₀, X₁]` (two-variable polynomials),
  and we exhibit a linear equivalence

      DegreeOneTwoVarForm K  ≃ₗ[K]
        MvPolynomial.homogeneousSubmodule (Fin 2) K 1.

  This pins the Stage-B Higgs interface to a Mathlib-native
  algebraic-geometry object, narrowing the remaining upstream
  gap to the Proj construction itself (the identification of
  `H^0(Proj K[X, Y], O(1))` with the graded-ring degree-1
  piece, which is a *general* algebraic-geometry theorem, not
  a Higgs-specific input).

  --------------------------------------------------------------
  Scope discipline
  --------------------------------------------------------------

  This module formalises:

    DegreeOneTwoVarForm K  ≃  K[X₀, X₁]_1
                                = MvPolynomial.homogeneousSubmodule (Fin 2) K 1.

  It does *not* formalise:

    K[X₀, X₁]_1  ≃  H^0(Proj K[X, Y], O(1)).

  The latter is the standard `Proj`-construction theorem in
  algebraic geometry, which lives in
  `Mathlib.AlgebraicGeometry.*` and is independent of TFPT.
  When that identification is formalised in Mathlib, this
  module's `LinearEquiv` composes with it to produce the full
  scheme-cohomology bridge.
-/

import Mathlib.RingTheory.MvPolynomial.Homogeneous
import Mathlib.RingTheory.MvPolynomial.Basic
import Mathlib.LinearAlgebra.Finsupp.LinearCombination
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.FiniteDimensional.Defs

import TfptCarrier.HiggsTopForm

set_option linter.dupNamespace false

namespace TFPT.Carrier.HiggsSchemeCohomologyShadow

open MvPolynomial Submodule

variable (K : Type*) [Field K]

/-- Abbreviation for the degree-1 homogeneous submodule of
`K[X₀, X₁]`. This is the algebraic-geometry "graded ring
degree-1 piece" `K[X, Y]_1`, which standardly identifies with
`H^0(ℙ¹_K, O(1))`. -/
noncomputable abbrev O_one : Submodule K (MvPolynomial (Fin 2) K) :=
  MvPolynomial.homogeneousSubmodule (Fin 2) K 1

namespace O_one

/-- The element `X i` lives in `O_one K` for any `i : Fin 2`. -/
theorem X_mem (i : Fin 2) : (MvPolynomial.X i : MvPolynomial (Fin 2) K) ∈ O_one K :=
  isHomogeneous_X K i

/-- `X 0, X 1` as elements of the homogeneous submodule. -/
noncomputable def Xsub (i : Fin 2) : O_one K :=
  ⟨MvPolynomial.X i, X_mem K i⟩

end O_one

variable {K}

/-- The forward map: a pair `(α, β)` becomes the homogeneous
degree-1 polynomial `α · X₀ + β · X₁`. -/
noncomputable def fromBinaryForm
    (p : TFPT.Carrier.HiggsTopForm.DegreeOneTwoVarForm K) :
    O_one K :=
  p.coeffX • O_one.Xsub K 0 + p.coeffY • O_one.Xsub K 1

/-- The forward map as a `K`-linear map. -/
noncomputable def fromBinaryFormLinear :
    TFPT.Carrier.HiggsTopForm.DegreeOneTwoVarForm K →ₗ[K] O_one K where
  toFun := fromBinaryForm
  map_add' p q := by
    show (p.coeffX + q.coeffX) • O_one.Xsub K 0 +
        (p.coeffY + q.coeffY) • O_one.Xsub K 1 =
        (p.coeffX • O_one.Xsub K 0 + p.coeffY • O_one.Xsub K 1) +
        (q.coeffX • O_one.Xsub K 0 + q.coeffY • O_one.Xsub K 1)
    rw [add_smul, add_smul]; abel
  map_smul' c p := by
    show (c * p.coeffX) • O_one.Xsub K 0 +
        (c * p.coeffY) • O_one.Xsub K 1 =
        c • (p.coeffX • O_one.Xsub K 0 + p.coeffY • O_one.Xsub K 1)
    rw [smul_add, ← mul_smul, ← mul_smul]

/-- Concrete formula for the value of the forward map (after
forgetting the subtype): `(α, β) ↦ α X₀ + β X₁`. -/
private theorem fromBinaryForm_val
    (p : TFPT.Carrier.HiggsTopForm.DegreeOneTwoVarForm K) :
    (fromBinaryForm p : MvPolynomial (Fin 2) K) =
      p.coeffX • MvPolynomial.X (0 : Fin 2) +
      p.coeffY • MvPolynomial.X (1 : Fin 2) := rfl

/-- The forward map is injective. Proof: extract the coefficient
of `X i` (which is `Finsupp.single i 1`). For `α X₀ + β X₁ =
α' X₀ + β' X₁` this gives `α = α'` and `β = β'`. -/
private theorem fromBinaryFormLinear_injective :
    Function.Injective (fromBinaryFormLinear (K := K)) := by
  intro p q hpq
  have hval : (fromBinaryForm p : MvPolynomial (Fin 2) K) =
      (fromBinaryForm q : MvPolynomial (Fin 2) K) :=
    congrArg Subtype.val hpq
  rw [fromBinaryForm_val, fromBinaryForm_val] at hval
  let X0 : MvPolynomial (Fin 2) K := MvPolynomial.X (0 : Fin 2)
  let X1 : MvPolynomial (Fin 2) K := MvPolynomial.X (1 : Fin 2)
  have hX :
      MvPolynomial.coeff (Finsupp.single (0 : Fin 2) 1)
        (p.coeffX • X0 + p.coeffY • X1) =
      MvPolynomial.coeff (Finsupp.single (0 : Fin 2) 1)
        (q.coeffX • X0 + q.coeffY • X1) := by
    rw [hval]
  have hY :
      MvPolynomial.coeff (Finsupp.single (1 : Fin 2) 1)
        (p.coeffX • X0 + p.coeffY • X1) =
      MvPolynomial.coeff (Finsupp.single (1 : Fin 2) 1)
        (q.coeffX • X0 + q.coeffY • X1) := by
    rw [hval]
  have hne01 : (Finsupp.single (0 : Fin 2) 1 : (Fin 2) →₀ ℕ) ≠
      Finsupp.single 1 1 := by
    intro h
    have := DFunLike.congr_fun h 0
    simp at this
  have hne10 : (Finsupp.single (1 : Fin 2) 1 : (Fin 2) →₀ ℕ) ≠
      Finsupp.single 0 1 := fun h => hne01 h.symm
  simp [X0, X1, MvPolynomial.coeff_add, MvPolynomial.coeff_smul,
        MvPolynomial.coeff_X', hne01, hne10] at hX hY
  exact TFPT.Carrier.HiggsTopForm.DegreeOneTwoVarForm.ext hX hY

/-- The forward map is surjective. Proof: every element of
`O_one K` is in `span K (range X)` by
`MvPolynomial.homogeneousSubmodule_one_eq_span_X`, so there
exists `c : Fin 2 → K` with `c 0 • X 0 + c 1 • X 1` equal to
the polynomial. The preimage is `⟨c 0, c 1⟩`. -/
private theorem fromBinaryFormLinear_surjective :
    Function.Surjective (fromBinaryFormLinear (K := K)) := by
  rintro ⟨q, hq⟩
  have hspan : (O_one K : Submodule K (MvPolynomial (Fin 2) K)) =
      Submodule.span K (Set.range (MvPolynomial.X (R := K) (σ := Fin 2))) :=
    MvPolynomial.homogeneousSubmodule_one_eq_span_X
  rw [hspan] at hq
  obtain ⟨c, hc⟩ := (Submodule.mem_span_range_iff_exists_fun _).mp hq
  refine ⟨⟨c 0, c 1⟩, ?_⟩
  apply Subtype.ext
  show c 0 • MvPolynomial.X (0 : Fin 2) +
       c 1 • MvPolynomial.X (1 : Fin 2) = q
  rw [← hc, Fin.sum_univ_two]

/-- **Main result: the algebraic shadow of `H^0(ℙ¹, O(1))`
agrees with `DegreeOneTwoVarForm`.**

The Stage-B Higgs shadow `DegreeOneTwoVarForm K` is canonically
linearly equivalent to the degree-1 homogeneous submodule of
`K[X₀, X₁]`. -/
noncomputable def toDegreeOneTwoVarForm :
    TFPT.Carrier.HiggsTopForm.DegreeOneTwoVarForm K ≃ₗ[K] O_one K :=
  LinearEquiv.ofBijective fromBinaryFormLinear
    ⟨fromBinaryFormLinear_injective, fromBinaryFormLinear_surjective⟩

/--
**Stage-B rank discharge via scheme-cohomology shadow.**

The degree-1 homogeneous submodule
`MvPolynomial.homogeneousSubmodule (Fin 2) K 1` has `K`-rank 2.
This is the "scheme-cohomology shadow" form of `dim H^0(ℙ¹, O(1)) = 2`.
-/
theorem finrank_O_one_eq_two : Module.finrank K (O_one K) = 2 := by
  rw [← LinearEquiv.finrank_eq toDegreeOneTwoVarForm]
  exact TFPT.Carrier.HiggsTopForm.DegreeOneTwoVarForm.finrank_eq_two K

/--
**Bridge: scheme-cohomology shadow ⇒ Higgs Stage B.**

Given an `Eplus ≃ₗ K[X₀, X₁]_1` linear equivalence, produce a
`HiggsTopForm K Eplus`. This is the upstream-most Higgs interface
in v10: the rank-2 conclusion is now derivable from a
*Mathlib-native algebraic-geometry object* (the degree-1
homogeneous submodule of a bivariate polynomial ring).
-/
noncomputable def toHiggsTopForm
    {Eplus : Type*} [AddCommGroup Eplus] [Module K Eplus]
    (h : Eplus ≃ₗ[K] O_one K) :
    TFPT.Carrier.HiggsTopForm.HiggsTopForm K Eplus where
  toDegreeOneForm := h.trans toDegreeOneTwoVarForm.symm

end TFPT.Carrier.HiggsSchemeCohomologyShadow
