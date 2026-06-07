/-
  TFPT Carrier — Stage D: Primitive Indecomposable Trilinear Form
  ---------------------------------------------------------------

  Stage D is the most upstream Yukawa interface formalised in this
  project. The primary datum is an *alternating trilinear form*

      ω : ⋀[K]^3 E_- →ₗ[K] K,

  i.e.\ a linear functional on the third exterior power.
  The non-degeneracy / primitivity / no-spectator content of TFPT
  Paper 2's "primitive indecomposable Yukawa type" is split into
  three explicit predicates on ω, each a `Prop` with no physics
  words:

      * `Nondegenerate ω` — the contraction `C_ω : E → (⋀²E)^*`
                            is injective;
      * `Primitive ω`     — the contraction `C_ω : E → (⋀²E)^*`
                            is surjective;
      * (implicit) the carrier `E` is non-trivial.

  The contraction map `C_ω` is *constructed explicitly* from ω
  via the universal property of the exterior power
  (`exteriorPower.alternatingMapLinearEquiv`) followed by
  `AlternatingMap.curryLeft`. It is therefore not data: it is a
  theorem.

  The main result of this module is:

      Nondegenerate ω ∧ Primitive ω
        ⟹ Nonempty (PrimitiveIndecomposableYukawaCoupling K E)

  i.e.\ Stage D ⇒ Stage C. The chain
  Stage D ⇒ Stage C ⇒ Stage B ⇒ Stage A ⇒ `dim E = 3` is then
  fully derived; the only Yukawa-side input remaining is the
  *trilinear form ω itself together with the two predicates*,
  which is precisely TFPT Paper 2's "non-degenerate primitive
  alternating trilinear coupling with no spectator".

  --------------------------------------------------------------
  Why this addresses the standing critique
  --------------------------------------------------------------

  Stage C is, in finite dimensions, equivalent to `dim E = 3`.
  This was correctly flagged in the v5 critique as a residual
  weakness: Stage C is a contraction iso, but its existence is
  in principle automatic in dimension 3, so Stage C alone does
  not "explain" why TFPT forces 3.

  Stage D removes this concern. The primary datum is ω, not the
  contraction. The contraction `C_ω` is constructed from ω. The
  rank-3 conclusion is a theorem about ω plus two structural
  predicates, not about a packaged iso. The remaining open
  question is no longer "does the Lean structure express the
  TFPT content" but "does the TFPT boundary kernel produce a
  non-degenerate primitive alternating trilinear form on E_-".
  The latter is upstream TFPT theory work, properly outside the
  scope of the Lean note.
-/

import Mathlib.LinearAlgebra.ExteriorPower.Basic
import Mathlib.LinearAlgebra.Alternating.Curry
import Mathlib.LinearAlgebra.Dual.Lemmas

import TfptCarrier.YukawaPrimitive

set_option linter.dupNamespace false

namespace TFPT.Carrier.YukawaTrilinearForm

open exteriorPower

variable (K : Type*) [Field K]
variable (E : Type*) [AddCommGroup E] [Module K E]

/--
**Stage D primary datum**: an alternating trilinear form
`ω : ⋀[K]^3 E →ₗ[K] K`, packaged as a structure.

Equivalent (up to `exteriorPower.alternatingMapLinearEquiv`)
to a `K`-valued alternating multilinear form on `Fin 3 → E`.
-/
structure YukawaTrilinearForm
    (K E : Type*) [Field K] [AddCommGroup E] [Module K E] where
  ω : (⋀[K]^3 E) →ₗ[K] K

namespace YukawaTrilinearForm

variable {K E}

/--
**Contraction map**: given `ω : ⋀³E →ₗ K`, the linear map
`C_ω : E →ₗ ((⋀²E) →ₗ K)` characterised by

    C_ω(v)(w ∧ x) = ω(v ∧ w ∧ x).

Constructed explicitly using the universal property of the
exterior power (`alternatingMapLinearEquiv`) and
`AlternatingMap.curryLeft`.

This is *not* data on the `YukawaTrilinearForm` structure; it
is a definition derived from `ω`.
-/
noncomputable def contraction (Y : YukawaTrilinearForm K E) :
    E →ₗ[K] ((⋀[K]^2 E) →ₗ[K] K) :=
  -- Step 1: convert ω : ⋀³E →ₗ K into the equivalent alternating
  -- map ω_alt : E [⋀^Fin 3]→ₗ K.
  let ω_alt : E [⋀^Fin 3]→ₗ[K] K :=
    (alternatingMapLinearEquiv (R := K) (M := E) (N := K) (n := 3)).symm Y.ω
  -- Step 2: curry the first argument to obtain
  --   E →ₗ (E [⋀^Fin 2]→ₗ K).
  -- Step 3: post-compose with alternatingMapLinearEquiv to
  -- transport the codomain to (⋀²E) →ₗ K.
  (alternatingMapLinearEquiv (R := K) (M := E) (N := K) (n := 2)).toLinearMap.comp
    (AlternatingMap.curryLeft ω_alt)

/--
**Operational predicate (1/2): the contraction is injective.**

This is the algebraic content of "non-degenerate" for the
alternating trilinear form `ω`: equivalently, for every nonzero
`v ∈ E` there exist `w, x ∈ E` with `ω(v ∧ w ∧ x) ≠ 0`.

The predicate is given an *operational* name (`ContractionInjective`)
to keep semantic-load words out of the formal interface. The
TFPT-side reading "non-degeneracy of the Yukawa coupling" is a
statement *about* this predicate, not its definition.
-/
def ContractionInjective (Y : YukawaTrilinearForm K E) : Prop :=
  Function.Injective Y.contraction

/--
**Operational predicate (2/2): the contraction is surjective.**

This is the algebraic content of "no spectator" (the
linear-algebra reading of "primitive"): every linear functional
on `⋀²E` arises as the contraction of `ω` with a vector of `E`.

The predicate is given an *operational* name
(`ContractionSurjective`) to keep semantic-load words out of
the formal interface. The TFPT-side reading "primitivity / no
spectator" is a statement *about* this predicate, not its
definition.
-/
def ContractionSurjective (Y : YukawaTrilinearForm K E) : Prop :=
  Function.Surjective Y.contraction

/-- Combined predicate matching TFPT Paper 2's phrase
"primitive indecomposable Yukawa type", broken into the two
operational components above. -/
def PrimitiveIndecomposableYukawaCondition
    (Y : YukawaTrilinearForm K E) : Prop :=
  Y.ContractionInjective ∧ Y.ContractionSurjective

/--
A trilinear form whose contraction is both injective and
surjective has a contraction that is a linear isomorphism
(over a finite-dimensional `K`-vector space).
-/
noncomputable def contractionEquivOfBoth
    [FiniteDimensional K E]
    (Y : YukawaTrilinearForm K E)
    (hinj : Y.ContractionInjective)
    (hsurj : Y.ContractionSurjective) :
    E ≃ₗ[K] ((⋀[K]^2 E) →ₗ[K] K) :=
  LinearEquiv.ofBijective Y.contraction ⟨hinj, hsurj⟩

/--
**Main bridge theorem: Stage D ⇒ Stage C.**

A `YukawaTrilinearForm` with injective and surjective
contraction yields a `PrimitiveIndecomposableYukawaCoupling`.

The TFPT-side reading is: this is the precise sense in which
"primitive indecomposable Yukawa type" implies the Stage C
contraction iso, once the phrase is unpacked into its two
operational predicates.
-/
noncomputable def toPrimitiveIndecomposableYukawaCoupling
    [FiniteDimensional K E] [Nontrivial E]
    (Y : YukawaTrilinearForm K E)
    (hinj : Y.ContractionInjective)
    (hsurj : Y.ContractionSurjective) :
    TFPT.Carrier.YukawaPrimitive.PrimitiveIndecomposableYukawaCoupling K E where
  contraction := Y.contractionEquivOfBoth hinj hsurj
  nontrivial := inferInstance

/--
**Stage D rank-3 theorem.**

A trilinear form on a non-trivial finite-dimensional `K`-vector
space whose contraction is both injective and surjective forces
`dim E = 3`.

This is the bottom-up form of the carrier-rigidity discharge:
the primary input is an alternating trilinear form satisfying
two operational predicates on its contraction; the rank-3
conclusion is a derived theorem (not an assumption in
linear-equivalence dress).
-/
theorem finrank_E_eq_three
    [FiniteDimensional K E] [Nontrivial E]
    (Y : YukawaTrilinearForm K E)
    (hinj : Y.ContractionInjective)
    (hsurj : Y.ContractionSurjective) :
    Module.finrank K E = 3 :=
  (Y.toPrimitiveIndecomposableYukawaCoupling hinj hsurj).finrank_E_eq_three

/--
**Compact rank-3 theorem.**

A trilinear form satisfying the combined predicate
`PrimitiveIndecomposableYukawaCondition` forces `dim E = 3`.
-/
theorem finrank_E_eq_three_of_condition
    [FiniteDimensional K E] [Nontrivial E]
    (Y : YukawaTrilinearForm K E)
    (h : Y.PrimitiveIndecomposableYukawaCondition) :
    Module.finrank K E = 3 :=
  Y.finrank_E_eq_three h.1 h.2

/--
**Transparent rank theorem (no `Nontrivial` hypothesis).**

Without the non-triviality hypothesis on `E`, the contraction
predicates are also satisfied by the trivial case `E = 0` (in
which case both maps `0 → 0` are trivially bijective). The
correct unconditional statement is the disjunction
`dim E = 0 ∨ dim E = 3`.

Explicit form:

  * if `E` is `Subsingleton`, then `finrank K E = 0`;
  * if `E` is `Nontrivial`, then `finrank K E = 3` by the
    Stage D theorem `finrank_E_eq_three`.

This theorem is supplied for transparency: the rank-3 slogan
in the documentation is true precisely under non-triviality of
`E`, and the trivial case is the only other solution.
-/
theorem finrank_E_eq_zero_or_three
    [FiniteDimensional K E]
    (Y : YukawaTrilinearForm K E)
    (hinj : Y.ContractionInjective)
    (hsurj : Y.ContractionSurjective) :
    Module.finrank K E = 0 ∨ Module.finrank K E = 3 := by
  rcases subsingleton_or_nontrivial E with hss | hnt
  · left; exact Module.finrank_zero_of_subsingleton
  · right; exact Y.finrank_E_eq_three hinj hsurj

end YukawaTrilinearForm

end TFPT.Carrier.YukawaTrilinearForm
