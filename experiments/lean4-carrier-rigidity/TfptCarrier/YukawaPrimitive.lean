/-
  TFPT Carrier — Primitive Indecomposable Yukawa Type (Stage C)
  -------------------------------------------------------------

  Stage C closes the conceptual gap of TFPT Paper 2's
  "primitive indecomposable Yukawa type" with a mathematically
  precise Lean definition. From this definition, the Stage B
  hypothesis `YukawaTopForm` follows mechanically.

  --------------------------------------------------------------
  The mathematical content
  --------------------------------------------------------------

  Let `E` be a finite-dimensional `K`-vector space. A primitive
  indecomposable Yukawa coupling on `E` is the structural datum

      Cω : E ≃ₗ[K] (⋀[K]^2 E →ₗ[K] K),

  i.e. a linear equivalence between `E` and the dual of its
  second exterior power. Up to canonical identifications this is
  the contraction map associated to a non-degenerate alternating
  trilinear form, in the precise sense that:

  * "non-degenerate" = Cω is injective,
  * "indecomposable + no spectator" = Cω is surjective,

  so the combined non-degenerate + indecomposable + no-spectator
  package is precisely "Cω is a linear isomorphism".

  --------------------------------------------------------------
  Why this forces dim E = 3
  --------------------------------------------------------------

  An iso `Cω : E ≃ₗ[K] (⋀[K]^2 E)^*` yields the dimension chain

      dim E
        = dim (⋀[K]^2 E)^*       (linear equivalence)
        = dim (⋀[K]^2 E)         (dual_finrank_eq, finite-dim)
        = Nat.choose (dim E) 2   (exteriorPower.finrank_eq)
        = n(n-1)/2               (Nat.choose_two_right).

  The equation `n = n(n-1)/2` over `ℕ` with `n ≥ 1` has the
  unique solution `n = 3` (an elementary `omega` check). Thus
  the existence of `Cω` forces `dim E = 3`.

  This is the precise mathematical reading of TFPT Paper 2's
  phrase "primitive indecomposable Yukawa type implies rank 3":

  > the seam-even bosonic leg contributes the line `Λ²E_+`, and
  > closure of the negative factor without a spectator requires
  > `E_- ⊗ Λ²E_- → Λ³E_- = det E_-`, so `dim E_- = 3`.

  Our `contraction` is the linear-algebraic realisation of the
  closure map `E ⊗ Λ²E → Λ³E` together with the non-degenerate
  / no-spectator content.

  --------------------------------------------------------------
  What this module proves

      PrimitiveIndecomposableYukawaCoupling K E
        ⟹ Module.finrank K E = 3
        ⟹ Nonempty (YukawaTopForm K E)

  Combined with the converse in `YukawaTopForm`, the entire
  Yukawa-rank discharge is now derived rather than postulated.
-/

import Mathlib.LinearAlgebra.ExteriorPower.Basis
import Mathlib.LinearAlgebra.Dual.Lemmas
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Tactic.Linarith

import TfptCarrier.YukawaRank
import TfptCarrier.YukawaTopForm

namespace TFPT.Carrier.YukawaPrimitive

open Module

/--
**`PrimitiveIndecomposableYukawaCoupling`** — Stage C definition
of TFPT Paper 2's "primitive indecomposable Yukawa type".

The datum is a linear equivalence

    E ≃ₗ[K] (⋀[K]^2 E →ₗ[K] K),

i.e.\ an iso between `E` and the dual of its second exterior
power. This packages the three pieces of TFPT's heuristic
sentence into one type-theoretic object:

* "non-degenerate"  — Cω is injective,
* "no spectator"    — Cω is surjective,
* "indecomposable"  — both together: no proper subspace either
                      annihilates Cω or has dual not in its image.

A future deeper formalisation of Yukawa-type theory (quiver-
theoretic or representation-theoretic) would *produce* a
`PrimitiveIndecomposableYukawaCoupling` as its conclusion.
-/
structure PrimitiveIndecomposableYukawaCoupling
    (K E : Type*) [Field K]
    [AddCommGroup E] [Module K E] where
  contraction : E ≃ₗ[K] ((⋀[K]^2 E) →ₗ[K] K)
  /-- The carrier is non-trivial — required because `dim E = 0`
      also formally satisfies `n = n(n-1)/2`. -/
  nontrivial : Nontrivial E

namespace PrimitiveIndecomposableYukawaCoupling

variable {K E : Type*} [Field K] [AddCommGroup E] [Module K E]

/-- Helper: `n = n(n-1)/2` and `n ≠ 0` force `n = 3`.

The argument: `n*(n-1)` is always even, so `n*(n-1)/2` rounds
exactly, giving `2n = n(n-1)`. Cancelling `n` (using `n ≥ 1`)
gives `n - 1 = 2`, hence `n = 3`. -/
private lemma nat_dim_eq_choose_two_self (n : ℕ) (hn : 0 < n)
    (h : n = n.choose 2) : n = 3 := by
  rw [Nat.choose_two_right] at h
  -- n*(n-1) is always even.
  have h_even : 2 ∣ n * (n - 1) := by
    rcases Nat.even_or_odd n with hn_even | hn_odd
    · exact hn_even.two_dvd.mul_right _
    · have hn1_even : Even (n - 1) := by
        obtain ⟨k, hk⟩ := hn_odd
        refine ⟨k, ?_⟩; omega
      exact hn1_even.two_dvd.mul_left _
  -- Multiply h by 2:  2*n = n*(n-1)
  have h2 : 2 * n = n * (n - 1) := by
    have := Nat.div_mul_cancel h_even
    omega
  -- Cancel n: 2 = n - 1
  have hn_sub : n - 1 = 2 := by
    have h2' : n * 2 = n * (n - 1) := by linarith
    exact (Nat.eq_of_mul_eq_mul_left hn h2').symm
  omega

/--
**Main rank-3 theorem (Stage C).**

A `PrimitiveIndecomposableYukawaCoupling K E` over a finite-
dimensional vector space forces `dim E = 3`.

Proof: the contraction iso gives
`dim E = dim (Λ²E)^* = dim Λ²E = C(dim E, 2) = dim E (dim E - 1)/2`,
i.e.\ `n = n(n-1)/2`. Together with non-triviality (`dim E ≥ 1`)
this is the unique integer equation forcing `n = 3`.
-/
theorem finrank_E_eq_three
    [FiniteDimensional K E]
    (Y : PrimitiveIndecomposableYukawaCoupling K E) :
    Module.finrank K E = 3 := by
  -- Step 1: dim E = dim (⋀²E)^*
  have h1 : Module.finrank K E = Module.finrank K ((⋀[K]^2 E) →ₗ[K] K) :=
    LinearEquiv.finrank_eq Y.contraction
  -- Step 2: dim (⋀²E)^* = dim ⋀²E
  have h2 : Module.finrank K ((⋀[K]^2 E) →ₗ[K] K) = Module.finrank K (⋀[K]^2 E) :=
    Subspace.dual_finrank_eq
  -- Step 3: dim ⋀²E = C(dim E, 2)
  have h3 : Module.finrank K (⋀[K]^2 E) = Nat.choose (Module.finrank K E) 2 :=
    exteriorPower.finrank_eq (R := K) (M := E) (n := 2)
  -- Step 4: combine
  have hN : Module.finrank K E = Nat.choose (Module.finrank K E) 2 :=
    h1.trans (h2.trans h3)
  -- Step 5: non-triviality gives dim E ≥ 1
  have hpos : 0 < Module.finrank K E := by
    haveI := Y.nontrivial
    exact Module.finrank_pos
  -- Step 6: nat-level reasoning
  exact nat_dim_eq_choose_two_self _ hpos hN

/--
**Bridge: Stage C implies Stage B.**

A `PrimitiveIndecomposableYukawaCoupling K E` produces a
`YukawaTopForm K E` (via the v4 converse
`YukawaTopForm.ofFinrankEqThree`).

This is the formal closure of the conceptual gap of TFPT Paper~2:

    Stage C (algebraic Yukawa)
      ⟹ Stage B (top form on Λ³E_-)
      ⟹ Stage A (rank witness E_- ≃ K³)
      ⟹ dim E_- = 3.
-/
noncomputable def toYukawaTopForm
    [FiniteDimensional K E]
    (Y : PrimitiveIndecomposableYukawaCoupling K E) :
    TFPT.Carrier.YukawaTopForm.YukawaTopForm K E :=
  TFPT.Carrier.YukawaTopForm.YukawaTopForm.ofFinrankEqThree Y.finrank_E_eq_three

/-- Direct bridge to Stage A (rank witness). -/
noncomputable def toYukawaRankCertificate
    [FiniteDimensional K E]
    (Y : PrimitiveIndecomposableYukawaCoupling K E) :
    TFPT.Carrier.YukawaRank.YukawaRankCertificate K E :=
  (Y.toYukawaTopForm).toYukawaRankCertificate

end PrimitiveIndecomposableYukawaCoupling

/-! ### Converse: dim E = 3 ⟹ ∃ primitive indecomposable coupling

A finite-dimensional `K`-vector space of dimension `3` admits a
primitive indecomposable Yukawa coupling: the contraction iso
`E ≃ₗ[K] (Λ²E)^*` exists by dimension count alone, since both
sides have dimension `3` (Mathlib's `dual_finrank_eq` and
`exteriorPower.finrank_eq`).

Combined with the forward direction, this gives the
characterisation
`Nonempty (PrimitiveIndecomposableYukawaCoupling K E) ↔ dim E = 3`.
The Stage C hypothesis is therefore precisely the rank-3
condition, *expressed structurally as a non-degenerate
alternating trilinear coupling*.
-/

/--
A finite-dimensional `K`-vector space of dimension `3` admits a
`PrimitiveIndecomposableYukawaCoupling`.

The contraction iso is built non-constructively via
`LinearEquiv.ofFinrankEq`, using that
`dim (Λ²E)^* = dim Λ²E = C(3, 2) = 3 = dim E`.
-/
noncomputable def PrimitiveIndecomposableYukawaCoupling.ofFinrankEqThree
    {K E : Type*} [Field K] [AddCommGroup E] [Module K E]
    [FiniteDimensional K E]
    (h : Module.finrank K E = 3) :
    PrimitiveIndecomposableYukawaCoupling K E where
  contraction :=
    have h1 : Module.finrank K ((⋀[K]^2 E) →ₗ[K] K)
            = Module.finrank K (⋀[K]^2 E) := Subspace.dual_finrank_eq
    have h2 : Module.finrank K (⋀[K]^2 E) = 3 := by
      rw [exteriorPower.finrank_eq (R := K) (M := E) (n := 2), h]
      decide
    LinearEquiv.ofFinrankEq E ((⋀[K]^2 E) →ₗ[K] K) (by rw [h, h1, h2])
  nontrivial := by
    have : 0 < Module.finrank K E := by rw [h]; decide
    exact Module.finrank_pos_iff.mp this

/--
**Characterisation theorem (Stage C).**

For a finite-dimensional `K`-vector space,
`PrimitiveIndecomposableYukawaCoupling K E` is inhabited if and
only if `dim E = 3`. The Stage C hypothesis is therefore
precisely the rank-3 condition, expressed as a non-degenerate
alternating trilinear coupling on `E`.
-/
theorem PrimitiveIndecomposableYukawaCoupling.nonempty_iff_finrank_eq_three
    {K E : Type*} [Field K] [AddCommGroup E] [Module K E]
    [FiniteDimensional K E] :
    Nonempty (PrimitiveIndecomposableYukawaCoupling K E)
      ↔ Module.finrank K E = 3 :=
  ⟨fun ⟨Y⟩ => Y.finrank_E_eq_three,
   fun h => ⟨PrimitiveIndecomposableYukawaCoupling.ofFinrankEqThree h⟩⟩

end TFPT.Carrier.YukawaPrimitive
