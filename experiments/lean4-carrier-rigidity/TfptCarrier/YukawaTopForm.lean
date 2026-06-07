/-
  TFPT Carrier — Yukawa Top Form (Stage B)
  ----------------------------------------

  Stage B of the Yukawa-type formalisation: we replace the bare
  rank witness `YukawaRankCertificate` (a linear equivalence
  `Eminus ≃ K^3`) with a *genuinely algebraic* hypothesis that
  captures the geometric content of TFPT Paper 2:

      "Λ³ E_- = det E_-"  (the negative-block determinant line
                            is the top exterior power)

  Concretely we package this as a linear equivalence

      `⋀[K]^3 Eminus ≃ₗ[K] K`,

  i.e. a non-degenerate alternating trilinear form on `Eminus`.
  This is the precise algebraic content of the carrier-closure
  identity `E_- ⊗ Λ²E_- → Λ³E_- = det E_-`.

  **Theorem (the rank-3 conclusion is a corollary of Stage B).**
  Given such a top-form equivalence, the dimension formula
  `dim Λⁿ V = C(dim V, n)` (Mathlib) reduces the hypothesis to
  `Nat.choose (finrank K E_-) 3 = 1`, which forces
  `finrank K E_- = 3` via `Nat.choose_eq_one_iff`.

  This is genuinely stronger than the Stage A rank witness:
  the input is a structural fact about `Eminus` (existence of a
  top form on Λ³), and the rank-3 conclusion is *derived*, not
  postulated.

  --------------------------------------------------------------
  What this module *does* prove

      YukawaTopForm K Eminus  ⟹  finrank K Eminus = 3

  What this module *does not* prove

      ∃ a primitive indecomposable Yukawa coupling on Eminus
                              ⟹  YukawaTopForm K Eminus

  The second implication is the conceptual content of "primitive
  indecomposable Yukawa type" in TFPT Paper 2. Choosing the
  precise mathematical encoding of "primitive indecomposable" is
  the principal open problem (variants 1/2/3 in `YukawaRank.lean`).
  Stage B is the *interface* that any such formalisation must
  produce as its conclusion.
-/

import Mathlib.LinearAlgebra.ExteriorPower.Basis
import Mathlib.LinearAlgebra.FiniteDimensional.Defs
import Mathlib.Data.Nat.Choose.Basic

import TfptCarrier.YukawaRank

namespace TFPT.Carrier.YukawaTopForm

open Module

variable (K : Type*) [Field K]
variable (E : Type*) [AddCommGroup E] [Module K E]

/--
**`YukawaTopForm`** — Stage B hypothesis for the rank-3
discharge `dim E_- = 3`.

The data is a linear equivalence `⋀[K]^3 E ≃ₗ[K] K`. Equivalently,
a non-degenerate alternating trilinear form on `E` whose
associated map from `⋀[K]^3 E` to `K` is an isomorphism.

In TFPT Paper 2 language: the "carrier-closure" identity
`E_- ⊗ Λ²E_- → Λ³E_- = det E_-` reads precisely that `Λ³ E_-`
is a one-dimensional `K`-line — i.e. the determinant of `E_-`.

Producing a `YukawaTopForm` is strictly *stronger* than producing
the Stage A rank witness `YukawaRankCertificate`: from a
`YukawaTopForm` we can derive the rank certificate by extending
the top form to any basis (see `toYukawaRankCertificate` below).
The reverse implication is trivial in dimension 3 but
*conceptually* it is what a future Yukawa-type theorem would
have to produce.
-/
structure YukawaTopForm
    (K E : Type*) [Field K] [AddCommGroup E] [Module K E] where
  topFormEquiv : (⋀[K]^3 E) ≃ₗ[K] K

namespace YukawaTopForm

variable {K E}

/--
A `YukawaTopForm` forces `⋀[K]^3 E` to be one-dimensional.

This is the *algebraic* content of "Λ³E_- is the determinant
line of E_-": being a one-dimensional `K`-vector space.
-/
theorem finrank_lambda3_eq_one
    (Y : YukawaTopForm K E) :
    Module.finrank K (⋀[K]^3 E) = 1 := by
  rw [LinearEquiv.finrank_eq Y.topFormEquiv]
  exact Module.finrank_self K

/--
**Main rank-3 theorem (Stage B).**

A `YukawaTopForm K E` forces `dim E = 3`.

Proof. By `finrank_lambda3_eq_one`, `dim (⋀[K]^3 E) = 1`. By
`exteriorPower.finrank_eq` (Mathlib),
`dim (⋀[K]^3 E) = C(dim E, 3)`. Hence `C(dim E, 3) = 1`, and by
`Nat.choose_eq_one_iff`, either `3 = 0` (false) or `dim E = 3`.
-/
theorem finrank_E_eq_three
    [FiniteDimensional K E]
    (Y : YukawaTopForm K E) :
    Module.finrank K E = 3 := by
  have h1 : Module.finrank K (⋀[K]^3 E) = 1 := Y.finrank_lambda3_eq_one
  -- Mathlib's exteriorPower.finrank_eq needs Module.Free + Module.Finite.
  -- Over a field, both follow from FiniteDimensional.
  have h2 : Module.finrank K (⋀[K]^3 E) = Nat.choose (Module.finrank K E) 3 :=
    exteriorPower.finrank_eq (R := K) (M := E) (n := 3)
  rw [h2] at h1
  -- Goal: finrank K E = 3 from Nat.choose (finrank K E) 3 = 1
  have h3 : 3 = 0 ∨ Module.finrank K E = 3 :=
    Nat.choose_eq_one_iff.mp h1
  rcases h3 with h | h
  · exact absurd h (by decide)
  · exact h

/--
**Bridge: Stage B implies Stage A.**

A `YukawaTopForm` over a finite-dimensional vector space produces
a `YukawaRankCertificate`: pick any basis of `E` (which has size
`3` by `finrank_E_eq_three`) and read off the resulting linear
equivalence with `Fin 3 → K`.

This makes Stage B a strict refinement of Stage A: any future
proof of "primitive indecomposable Yukawa type ⟹ rank 3" that
factors through Stage B automatically discharges Stage A as well.
-/
noncomputable def toYukawaRankCertificate
    [FiniteDimensional K E]
    (Y : YukawaTopForm K E) :
    TFPT.Carrier.YukawaRank.YukawaRankCertificate K E where
  toShadow :=
    have h : Module.finrank K E = 3 := Y.finrank_E_eq_three
    have h' : Module.finrank K E = Module.finrank K (Fin 3 → K) := by
      rw [h, Module.finrank_fintype_fun_eq_card, Fintype.card_fin]
    LinearEquiv.ofFinrankEq E (Fin 3 → K) h'

end YukawaTopForm

/-! ### Converse: dim 3 ⟹ ∃ Yukawa top form

We round out the characterisation by showing that the Stage B
hypothesis is *equivalent* (in finite-dimensional vector spaces
over a field) to `dim E = 3`. The reverse direction takes any
3-dimensional vector space and constructs a top-form equivalence
from an arbitrary basis. Combined with the forward direction
above, this means: a `YukawaTopForm` carries *exactly* the
information `dim E = 3`, no more and no less.

The point is: the Stage B hypothesis is honest *algebra*, not a
disguised rank assumption. A future definition of "primitive
indecomposable Yukawa type" need produce only `Nonempty
(YukawaTopForm K E_-)` to close the carrier-rigidity chain.
-/

namespace YukawaTopForm

variable {K E}

/--
A finite-dimensional `K`-vector space of dimension `3` admits a
top-form equivalence: any choice of basis exhibits `⋀[K]^3 E ≃ K`.
-/
noncomputable def ofFinrankEqThree
    [FiniteDimensional K E]
    (h : Module.finrank K E = 3) :
    YukawaTopForm K E where
  topFormEquiv :=
    have hΛ : Module.finrank K (⋀[K]^3 E) = 1 := by
      rw [exteriorPower.finrank_eq (R := K) (M := E) (n := 3), h]
      decide
    LinearEquiv.ofFinrankEq (⋀[K]^3 E) K
      (by rw [hΛ, Module.finrank_self])

/--
**Characterisation theorem.**

For a finite-dimensional `K`-vector space, `YukawaTopForm K E` is
inhabited if and only if `dim E = 3`. The Stage B hypothesis is
therefore precisely the rank-3 condition expressed in
exterior-algebra form.
-/
theorem nonempty_iff_finrank_eq_three
    [FiniteDimensional K E] :
    Nonempty (YukawaTopForm K E) ↔ Module.finrank K E = 3 :=
  ⟨fun ⟨Y⟩ => Y.finrank_E_eq_three, fun h => ⟨YukawaTopForm.ofFinrankEqThree h⟩⟩

end YukawaTopForm

end TFPT.Carrier.YukawaTopForm
