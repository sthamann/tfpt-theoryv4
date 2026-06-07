/-
  TFPT Carrier — Yukawa Stage D Backward Direction
  ------------------------------------------------

  v10 closes the standing Stage-D lemma gap: from `dim E = 3`
  we now exhibit a concrete alternating trilinear form
  `ω : ⋀³E →ₗ[K] K` whose contraction is both injective
  (`ContractionInjective`) and surjective
  (`ContractionSurjective`).

  This is the converse of `YukawaTrilinearForm.finrank_E_eq_three`:

      finrank K E = 3   ⟹   ∃ Y : YukawaTrilinearForm K E,
                              Y.ContractionInjective ∧
                              Y.ContractionSurjective.

  Combined with the forward direction this gives the
  characterisation theorem (under `Nontrivial E`):

      ∃ Y : YukawaTrilinearForm K E with CI + CS
      ⟺   finrank K E = 3.

  --------------------------------------------------------------
  Construction
  --------------------------------------------------------------

  Given a basis `b : Basis (Fin 3) K E`, Mathlib's
  `Module.Basis.det b` is an alternating multilinear form
  `E [⋀^Fin 3]→ₗ[K] K` (the determinant of vectors expressed in
  `b`). Transporting via `exteriorPower.alternatingMapLinearEquiv`
  produces a linear map `⋀³E →ₗ[K] K` — our Yukawa form `ω`.

  The contraction `C_ω : E →ₗ[K] ((⋀²E) →ₗ K)` is injective by
  basis-level computation: writing `v = ∑ aᵢ • bᵢ`, the
  evaluation of `C_ω(v)` on the dual basis of `Λ²E` extracts
  each `aᵢ` (up to sign), so `C_ω(v) = 0` forces `v = 0`.
  Surjectivity then follows from injectivity and the equal-
  dimensional finite-rank theorem
  (`LinearMap.injective_iff_surjective_of_finrank_eq_finrank`):
  `dim E = 3 = binom(3, 2) = dim (Λ²E) = dim (Λ²E)*`.

  --------------------------------------------------------------
  Scope discipline
  --------------------------------------------------------------

  This module formalises:

      finrank K E = 3   ⟹   ∃ Y, CI(Y) ∧ CS(Y).

  It does *not* formalise the TFPT-internal construction of `ω`
  from boundary kernel and representation data: that is the
  upstream physics question. The present construction is purely
  algebraic, demonstrating that the Stage D hypothesis is
  *equivalent* to the rank-3 condition under non-triviality.
-/

import Mathlib.LinearAlgebra.ExteriorPower.Basis
import Mathlib.LinearAlgebra.Determinant
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas

import TfptCarrier.YukawaTrilinearForm

set_option linter.dupNamespace false

namespace TFPT.Carrier.YukawaStageDExistence

open exteriorPower TFPT.Carrier.YukawaTrilinearForm

variable {K : Type*} [Field K]
variable {E : Type*} [AddCommGroup E] [Module K E]

/--
**Stage D form from a basis.**

Given a basis `b : Basis (Fin 3) K E`, the determinant form
`b.det` is an alternating multilinear form `E^3 →ₗ K`. Via
`exteriorPower.alternatingMapLinearEquiv` (the universal
property of the exterior power), this transports to a linear
form on `⋀³E`, giving a `YukawaTrilinearForm`.
-/
noncomputable def ofBasis (b : Module.Basis (Fin 3) K E) :
    TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm K E where
  ω := (alternatingMapLinearEquiv (R := K) (M := E) (N := K) (n := 3)) b.det

/--
**Stage D form from rank-3 hypothesis.**

Given `finrank K E = 3` over a finite-dimensional `K`-vector
space, choose a basis (Mathlib's `Module.finBasisOfFinrankEq`)
and apply `ofBasis`.
-/
noncomputable def ofFinrankEqThree
    [FiniteDimensional K E]
    (h : Module.finrank K E = 3) :
    TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm K E :=
  ofBasis (Module.finBasisOfFinrankEq K E h)

/--
**The Stage D form from a basis is non-trivial.**

Specifically, `ω(b 0 ∧ b 1 ∧ b 2) = 1`. This is the basis-level
witness of non-degeneracy of `ω` on the top wedge.
-/
theorem ofBasis_ω_apply_top
    (b : Module.Basis (Fin 3) K E) :
    (ofBasis b).ω (ιMulti K 3 ![b 0, b 1, b 2]) = 1 := by
  simp only [ofBasis, alternatingMapLinearEquiv_apply_ιMulti]
  have : (![b 0, b 1, b 2] : Fin 3 → E) = b := by
    funext i; fin_cases i <;> rfl
  rw [this]
  exact b.det_self

/-- **Key computational lemma**: the contraction of the
basis-constructed Yukawa form on a wedge product
`ιMulti K 2 w` equals `b.det` applied to the prepended tuple
`(v, w 0, w 1)`. -/
private lemma contraction_apply_ιMulti
    (b : Module.Basis (Fin 3) K E) (v : E) (w : Fin 2 → E) :
    (ofBasis b).contraction v (ιMulti K 2 w) =
      b.det (Matrix.vecCons v w) := by
  show ((alternatingMapLinearEquiv (R := K) (M := E) (N := K) (n := 2)).toLinearMap.comp
        (AlternatingMap.curryLeft
          ((alternatingMapLinearEquiv (R := K) (M := E) (N := K) (n := 3)).symm
            (ofBasis b).ω))) v (ιMulti K 2 w) =
      b.det (Matrix.vecCons v w)
  simp only [LinearMap.comp_apply, LinearEquiv.coe_coe,
    AlternatingMap.curryLeft_apply_apply,
    alternatingMapLinearEquiv_apply_ιMulti, ofBasis,
    LinearEquiv.symm_apply_apply]

/-- For the basis-prepended tuple `(v, b 1, b 2)`, the `b`-determinant
extracts the 0-coordinate of `v` in `b`. -/
private lemma det_basis_first_pair12
    (b : Module.Basis (Fin 3) K E) (v : E) :
    b.det (Matrix.vecCons v ![b 1, b 2]) = (b.repr v) 0 := by
  rw [Module.Basis.det_apply, Matrix.det_fin_three]
  -- Matrix entries (i, j): b.toMatrix m i j = (b.repr (m j)) i.
  -- m 0 = v, m 1 = b 1, m 2 = b 2.
  have hM00 : b.toMatrix (Matrix.vecCons v ![b 1, b 2]) 0 0 = (b.repr v) 0 := rfl
  have hM10 : b.toMatrix (Matrix.vecCons v ![b 1, b 2]) 1 0 = (b.repr v) 1 := rfl
  have hM20 : b.toMatrix (Matrix.vecCons v ![b 1, b 2]) 2 0 = (b.repr v) 2 := rfl
  have hM01 : b.toMatrix (Matrix.vecCons v ![b 1, b 2]) 0 1 = 0 := by
    show (b.repr (b 1)) 0 = 0
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM11 : b.toMatrix (Matrix.vecCons v ![b 1, b 2]) 1 1 = 1 := by
    show (b.repr (b 1)) 1 = 1
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM21 : b.toMatrix (Matrix.vecCons v ![b 1, b 2]) 2 1 = 0 := by
    show (b.repr (b 1)) 2 = 0
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM02 : b.toMatrix (Matrix.vecCons v ![b 1, b 2]) 0 2 = 0 := by
    show (b.repr (b 2)) 0 = 0
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM12 : b.toMatrix (Matrix.vecCons v ![b 1, b 2]) 1 2 = 0 := by
    show (b.repr (b 2)) 1 = 0
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM22 : b.toMatrix (Matrix.vecCons v ![b 1, b 2]) 2 2 = 1 := by
    show (b.repr (b 2)) 2 = 1
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  rw [hM00, hM10, hM20, hM01, hM11, hM21, hM02, hM12, hM22]
  ring

/-- For the basis-prepended tuple `(v, b 0, b 2)`, the `b`-determinant
extracts minus the 1-coordinate of `v` in `b`. -/
private lemma det_basis_first_pair02
    (b : Module.Basis (Fin 3) K E) (v : E) :
    b.det (Matrix.vecCons v ![b 0, b 2]) = -((b.repr v) 1) := by
  rw [Module.Basis.det_apply, Matrix.det_fin_three]
  have hM00 : b.toMatrix (Matrix.vecCons v ![b 0, b 2]) 0 0 = (b.repr v) 0 := rfl
  have hM10 : b.toMatrix (Matrix.vecCons v ![b 0, b 2]) 1 0 = (b.repr v) 1 := rfl
  have hM20 : b.toMatrix (Matrix.vecCons v ![b 0, b 2]) 2 0 = (b.repr v) 2 := rfl
  have hM01 : b.toMatrix (Matrix.vecCons v ![b 0, b 2]) 0 1 = 1 := by
    show (b.repr (b 0)) 0 = 1
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM11 : b.toMatrix (Matrix.vecCons v ![b 0, b 2]) 1 1 = 0 := by
    show (b.repr (b 0)) 1 = 0
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM21 : b.toMatrix (Matrix.vecCons v ![b 0, b 2]) 2 1 = 0 := by
    show (b.repr (b 0)) 2 = 0
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM02 : b.toMatrix (Matrix.vecCons v ![b 0, b 2]) 0 2 = 0 := by
    show (b.repr (b 2)) 0 = 0
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM12 : b.toMatrix (Matrix.vecCons v ![b 0, b 2]) 1 2 = 0 := by
    show (b.repr (b 2)) 1 = 0
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM22 : b.toMatrix (Matrix.vecCons v ![b 0, b 2]) 2 2 = 1 := by
    show (b.repr (b 2)) 2 = 1
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  rw [hM00, hM10, hM20, hM01, hM11, hM21, hM02, hM12, hM22]
  ring

/-- For the basis-prepended tuple `(v, b 0, b 1)`, the `b`-determinant
extracts the 2-coordinate of `v` in `b`. -/
private lemma det_basis_first_pair01
    (b : Module.Basis (Fin 3) K E) (v : E) :
    b.det (Matrix.vecCons v ![b 0, b 1]) = (b.repr v) 2 := by
  rw [Module.Basis.det_apply, Matrix.det_fin_three]
  have hM00 : b.toMatrix (Matrix.vecCons v ![b 0, b 1]) 0 0 = (b.repr v) 0 := rfl
  have hM10 : b.toMatrix (Matrix.vecCons v ![b 0, b 1]) 1 0 = (b.repr v) 1 := rfl
  have hM20 : b.toMatrix (Matrix.vecCons v ![b 0, b 1]) 2 0 = (b.repr v) 2 := rfl
  have hM01 : b.toMatrix (Matrix.vecCons v ![b 0, b 1]) 0 1 = 1 := by
    show (b.repr (b 0)) 0 = 1
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM11 : b.toMatrix (Matrix.vecCons v ![b 0, b 1]) 1 1 = 0 := by
    show (b.repr (b 0)) 1 = 0
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM21 : b.toMatrix (Matrix.vecCons v ![b 0, b 1]) 2 1 = 0 := by
    show (b.repr (b 0)) 2 = 0
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM02 : b.toMatrix (Matrix.vecCons v ![b 0, b 1]) 0 2 = 0 := by
    show (b.repr (b 1)) 0 = 0
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM12 : b.toMatrix (Matrix.vecCons v ![b 0, b 1]) 1 2 = 1 := by
    show (b.repr (b 1)) 1 = 1
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  have hM22 : b.toMatrix (Matrix.vecCons v ![b 0, b 1]) 2 2 = 0 := by
    show (b.repr (b 1)) 2 = 0
    simp [Module.Basis.repr_self, Finsupp.single_apply]
  rw [hM00, hM10, hM20, hM01, hM11, hM21, hM02, hM12, hM22]
  ring

/-- **Stage D contraction is injective for the basis form.**

If `v` lies in the kernel of `(ofBasis b).contraction`, then
its coordinates in `b` are all zero, so `v = 0`. -/
theorem ofBasis_contractionInjective
    (b : Module.Basis (Fin 3) K E) :
    (ofBasis b).ContractionInjective := by
  rw [TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm.ContractionInjective,
    injective_iff_map_eq_zero]
  intro v hv
  have h0 : (b.repr v) 0 = 0 := by
    have := LinearMap.congr_fun hv (ιMulti K 2 ![b 1, b 2])
    rw [contraction_apply_ιMulti, det_basis_first_pair12] at this
    simpa using this
  have h1 : (b.repr v) 1 = 0 := by
    have := LinearMap.congr_fun hv (ιMulti K 2 ![b 0, b 2])
    rw [contraction_apply_ιMulti, det_basis_first_pair02] at this
    simpa [neg_eq_zero] using this
  have h2 : (b.repr v) 2 = 0 := by
    have := LinearMap.congr_fun hv (ιMulti K 2 ![b 0, b 1])
    rw [contraction_apply_ιMulti, det_basis_first_pair01] at this
    simpa using this
  apply b.repr.injective
  ext i
  fin_cases i
  · simpa using h0
  · simpa using h1
  · simpa using h2

/-- **Stage D contraction is surjective for the basis form.**

Given a basis indexed by `Fin 3` (so `dim E = 3` and `Nontrivial E`),
the contraction is a linear map between two `K`-vector spaces of
equal finite dimension. Injectivity (proved above) implies
surjectivity by the standard finite-dimensional rank-nullity result. -/
theorem ofBasis_contractionSurjective
    [FiniteDimensional K E]
    (b : Module.Basis (Fin 3) K E) :
    (ofBasis b).ContractionSurjective := by
  have hE : Module.finrank K E = 3 := by
    have := b.linearIndependent.fintype_card_le_finrank
    have h2 := Module.finrank_eq_card_basis b
    simp [Fintype.card_fin] at h2
    exact h2
  have hΛ2 : Module.finrank K ((⋀[K]^2 E) →ₗ[K] K) = 3 := by
    have h1 : Module.finrank K ((⋀[K]^2 E) →ₗ[K] K)
            = Module.finrank K (⋀[K]^2 E) := Subspace.dual_finrank_eq
    have h2 : Module.finrank K (⋀[K]^2 E) = Nat.choose (Module.finrank K E) 2 :=
      exteriorPower.finrank_eq (R := K) (M := E) (n := 2)
    rw [h1, h2, hE]
    decide
  have hdim : Module.finrank K E = Module.finrank K ((⋀[K]^2 E) →ₗ[K] K) := by
    rw [hE, hΛ2]
  exact (LinearMap.injective_iff_surjective_of_finrank_eq_finrank hdim).mp
    (ofBasis_contractionInjective b)

/--
**Stage D backward (forward direction): from a basis, a witness.**

A basis indexed by `Fin 3` produces a Yukawa trilinear form whose
contraction is both injective and surjective. -/
theorem ofBasis_satisfies_condition
    [FiniteDimensional K E]
    (b : Module.Basis (Fin 3) K E) :
    (ofBasis b).PrimitiveIndecomposableYukawaCondition :=
  ⟨ofBasis_contractionInjective b, ofBasis_contractionSurjective b⟩

/--
**Stage D backward theorem.**

Given `finrank K E = 3` (and finite-dimensionality), there exists a
Yukawa trilinear form `ω : ⋀³E →ₗ[K] K` whose contraction is both
injective and surjective. This is the converse direction of
`YukawaTrilinearForm.finrank_E_eq_three` and closes the existence
gap documented in v9. -/
theorem exists_yukawaTrilinearForm_of_finrank_eq_three
    [FiniteDimensional K E]
    (h : Module.finrank K E = 3) :
    ∃ Y : TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm K E,
      Y.ContractionInjective ∧ Y.ContractionSurjective :=
  let b := Module.finBasisOfFinrankEq K E h
  ⟨ofBasis b, ofBasis_contractionInjective b, ofBasis_contractionSurjective b⟩

/--
**Stage D characterisation (under `Nontrivial`).**

For a finite-dimensional `K`-vector space `E`, the existence of a
Yukawa trilinear form on `E` with injective and surjective
contraction is *equivalent* to `dim E = 3`.

This is the Stage-D characterisation theorem requested by the v9
review: it shows that the operational Stage-D predicates are not
weaker than the rank-3 condition (apart from the `Nontrivial`
hypothesis required to rule out the trivial case `dim E = 0`). -/
theorem stage_D_iff_finrank_eq_three
    [FiniteDimensional K E] [Nontrivial E] :
    (∃ Y : TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm K E,
        Y.ContractionInjective ∧ Y.ContractionSurjective) ↔
      Module.finrank K E = 3 := by
  constructor
  · rintro ⟨Y, hinj, hsurj⟩
    exact Y.finrank_E_eq_three hinj hsurj
  · intro h
    exact exists_yukawaTrilinearForm_of_finrank_eq_three h

end TFPT.Carrier.YukawaStageDExistence
