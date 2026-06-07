/-
  TFPT Carrier — Higgs Stage B: Degree-One Top Forms
  --------------------------------------------------

  v8 upgrade of the Higgs interface: a Stage-B refinement
  parallel to the Yukawa tower.

  TFPT Paper 2 derives `dim E_+ = 2` from the compact Higgs
  index, which in geometric form reads

      H^0(P^1, O(1)) ≅ K[X, Y]_1 ≅ K · X ⊕ K · Y.

  The full geometric statement requires scheme-theoretic
  cohomology of line bundles. v8 introduces a Stage-B Lean
  interface that captures the *algebraic content* of this
  identification: an element of `H^0(P^1, O(1))^{alg}` is a
  homogeneous degree-1 polynomial in two formal variables `X, Y`
  over `K`, i.e.\ a pair of coefficients `(α, β) ∈ K × K`
  representing `α · X + β · Y`.

  The Stage-B Higgs interface

      HiggsTopForm K Eplus := Eplus ≃ₗ[K] DegreeOneTwoVarForm K

  is a structural refinement of the Stage-A
  `HiggsIndexCertificate`: producing a `HiggsTopForm` exhibits
  `Eplus` as the algebraic incarnation of the line-bundle
  sections, not just as a vector space of rank 2.

  --------------------------------------------------------------
  Scope discipline
  --------------------------------------------------------------

  The `DegreeOneTwoVarForm K` structure here is the algebraic
  shadow only: a pair of coefficients with the natural module
  structure. It does *not* formalise scheme-theoretic
  `H^0(P^1, O(1))`. A future Lean module would build the
  scheme-cohomology object and exhibit an iso to
  `DegreeOneTwoVarForm`; that iso is the upstream content of
  the geometric Higgs derivation.

  From Stage B the rank-2 conclusion is mechanical:
  `DegreeOneTwoVarForm K` has K-rank 2 by direct construction,
  so any `Eplus ≃ DegreeOneTwoVarForm K` forces
  `dim Eplus = 2`.
-/

import Mathlib.LinearAlgebra.FiniteDimensional.Defs
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.Data.Fin.VecNotation

import TfptCarrier.HiggsIndexShadow

namespace TFPT.Carrier.HiggsTopForm

variable (K : Type*) [Field K]

/--
The space of homogeneous degree-1 polynomials in two formal
variables `X, Y` over `K`.

An element is a pair of coefficients `(α, β)` interpreted as
`α · X + β · Y`. The natural `K`-module structure makes this a
2-dimensional `K`-vector space.

This is the algebraic shadow of `H^0(P^1, O(1))`: under the
identification
`H^0(P^1_K, O(1)) ≅ K[X, Y]_1 = K · X ⊕ K · Y` the
right-hand side is exactly the type defined here.
-/
@[ext]
structure DegreeOneTwoVarForm (K : Type*) [Field K] where
  /-- The coefficient of the formal variable `X`. -/
  coeffX : K
  /-- The coefficient of the formal variable `Y`. -/
  coeffY : K

namespace DegreeOneTwoVarForm

variable {K}

instance : Add (DegreeOneTwoVarForm K) :=
  ⟨fun p q => ⟨p.coeffX + q.coeffX, p.coeffY + q.coeffY⟩⟩

instance : Zero (DegreeOneTwoVarForm K) := ⟨⟨0, 0⟩⟩

instance : Neg (DegreeOneTwoVarForm K) :=
  ⟨fun p => ⟨-p.coeffX, -p.coeffY⟩⟩

instance : SMul K (DegreeOneTwoVarForm K) :=
  ⟨fun c p => ⟨c * p.coeffX, c * p.coeffY⟩⟩

@[simp] lemma add_coeffX (p q : DegreeOneTwoVarForm K) :
    (p + q).coeffX = p.coeffX + q.coeffX := rfl
@[simp] lemma add_coeffY (p q : DegreeOneTwoVarForm K) :
    (p + q).coeffY = p.coeffY + q.coeffY := rfl
@[simp] lemma zero_coeffX : (0 : DegreeOneTwoVarForm K).coeffX = 0 := rfl
@[simp] lemma zero_coeffY : (0 : DegreeOneTwoVarForm K).coeffY = 0 := rfl
@[simp] lemma neg_coeffX (p : DegreeOneTwoVarForm K) :
    (-p).coeffX = -p.coeffX := rfl
@[simp] lemma neg_coeffY (p : DegreeOneTwoVarForm K) :
    (-p).coeffY = -p.coeffY := rfl
@[simp] lemma smul_coeffX (c : K) (p : DegreeOneTwoVarForm K) :
    (c • p).coeffX = c * p.coeffX := rfl
@[simp] lemma smul_coeffY (c : K) (p : DegreeOneTwoVarForm K) :
    (c • p).coeffY = c * p.coeffY := rfl

instance : AddCommGroup (DegreeOneTwoVarForm K) where
  add_assoc p q r := by ext <;> simp [add_assoc]
  zero_add p := by ext <;> simp
  add_zero p := by ext <;> simp
  add_comm p q := by ext <;> simp [add_comm]
  neg_add_cancel p := by ext <;> simp
  nsmul := nsmulRec
  zsmul := zsmulRec

instance : Module K (DegreeOneTwoVarForm K) where
  one_smul p := by ext <;> simp
  mul_smul c d p := by ext <;> simp [mul_assoc]
  smul_zero c := by ext <;> simp
  smul_add c p q := by ext <;> simp [mul_add]
  add_smul c d p := by ext <;> simp [add_mul]
  zero_smul p := by ext <;> simp

variable (K) in
/--
The canonical linear equivalence between the homogeneous
degree-1 polynomial space and its algebraic shadow
`DegreeOneBinaryForms K = Fin 2 → K`.

`X ↦ ![1, 0]`,  `Y ↦ ![0, 1]`.
-/
def toBinaryForms :
    DegreeOneTwoVarForm K ≃ₗ[K] TFPT.Carrier.HiggsIndexShadow.DegreeOneBinaryForms K where
  toFun p := ![p.coeffX, p.coeffY]
  invFun v := ⟨v 0, v 1⟩
  left_inv p := by ext <;> simp [Matrix.cons_val_zero, Matrix.cons_val_one]
  right_inv v := by
    funext i
    fin_cases i <;> simp [Matrix.cons_val_zero, Matrix.cons_val_one]
  map_add' p q := by ext i; fin_cases i <;> simp
  map_smul' c p := by ext i; fin_cases i <;> simp

variable (K) in
/--
**Stage-B rank theorem.**

`DegreeOneTwoVarForm K` has `K`-rank `2`. This is the algebraic
content of `dim H^0(P^1, O(1)) = 2`.
-/
theorem finrank_eq_two :
    Module.finrank K (DegreeOneTwoVarForm K) = 2 := by
  rw [LinearEquiv.finrank_eq (toBinaryForms K)]
  exact TFPT.Carrier.HiggsIndexShadow.finrank_degreeOneBinaryForms K

instance : FiniteDimensional K (DegreeOneTwoVarForm K) :=
  Module.Finite.equiv (toBinaryForms K).symm

end DegreeOneTwoVarForm

/--
**`HiggsTopForm`** — Stage-B Higgs interface.

A linear equivalence between the positive polarisation block
`Eplus` and the algebraic shadow of `H^0(P^1, O(1))`. Producing
a `HiggsTopForm` exhibits `Eplus` not merely as a 2-dimensional
vector space (Stage A) but as the homogeneous-degree-1
polynomial space (algebraic Stage B).

The Stage B → Stage A bridge `toHiggsIndexCertificate` is just
composition with the algebraic-shadow iso.
-/
structure HiggsTopForm
    (K : Type*) [Field K]
    (Eplus : Type*) [AddCommGroup Eplus] [Module K Eplus] where
  toDegreeOneForm : Eplus ≃ₗ[K] DegreeOneTwoVarForm K

namespace HiggsTopForm

variable {K}
variable {Eplus : Type*} [AddCommGroup Eplus] [Module K Eplus]

/-- A `HiggsTopForm` transfers finite-dimensionality. -/
instance (h : HiggsTopForm K Eplus) : FiniteDimensional K Eplus :=
  Module.Finite.equiv h.toDegreeOneForm.symm

/--
**Stage-B rank discharge.**

A `HiggsTopForm K Eplus` forces `dim Eplus = 2`. The proof is
the composition of `LinearEquiv.finrank_eq` with the algebraic
shadow's rank-2 theorem.
-/
theorem finrank_Eplus_eq_two (h : HiggsTopForm K Eplus) :
    Module.finrank K Eplus = 2 := by
  rw [LinearEquiv.finrank_eq h.toDegreeOneForm]
  exact DegreeOneTwoVarForm.finrank_eq_two K

/--
**Stage B ⇒ Stage A bridge.**

A `HiggsTopForm` produces a Stage A `HiggsIndexCertificate` via
the algebraic shadow.
-/
def toHiggsIndexCertificate (h : HiggsTopForm K Eplus) :
    TFPT.Carrier.HiggsIndexShadow.HiggsIndexCertificate K Eplus where
  toForms := h.toDegreeOneForm.trans (DegreeOneTwoVarForm.toBinaryForms K)

end HiggsTopForm

end TFPT.Carrier.HiggsTopForm
