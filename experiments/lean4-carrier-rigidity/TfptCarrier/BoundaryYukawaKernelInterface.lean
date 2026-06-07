/-
  TFPT Carrier — Boundary Yukawa Kernel Interface
  -----------------------------------------------

  v11 upstream layer for the Yukawa Stage D input.

  In TFPT Paper 2, the alternating trilinear form
  $\omega : \Lambda^3 E_- \to K$ together with its
  non-degeneracy / no-spectator properties is not assumed: it
  is produced by the TFPT boundary kernel together with the
  representation-theoretic content of the negative chirality
  block. The slogan, in Paper 2's wording, reads:

      TFPT boundary kernel
        ⟹ canonical $\omega : \Lambda^3 E_- \to K$
          with CI and CS.

  Whether the TFPT boundary kernel produces \emph{the same}
  $\omega$ as the basis-constructed witness of
  `YukawaStageDExistence` is the upstream physics question; the
  existence is closed by the present note
  (`YukawaStageDExistence.exists_yukawaTrilinearForm_of_finrank_eq_three`).

  This module provides a structural typed interface
  `BoundaryYukawaKernel`: a Yukawa Stage-D form $\omega$
  packaged with the two operational predicates plus
  non-triviality of `E_-`. It is the *Lean-side target* of the
  future TFPT theorem.

  **What this module is**: a typed renaming / packaging of the
  Stage D condition, supplying a named Lean conclusion for the
  future TFPT derivation.

  **What this module is not**: a new physical derivation. The
  existence of an $\omega$ with CI + CS is closed in v10 by
  `YukawaStageDExistence`; the *canonicity* of $\omega$ from
  TFPT boundary data --- whether the TFPT-internal
  construction picks out the same form as the basis-built
  witness, up to carrier symmetries --- remains the upstream
  physics question.

  --------------------------------------------------------------
  Scope discipline
  --------------------------------------------------------------

  This module formalises:

    BoundaryYukawaKernel K E_-
      ⟹ ∃ Y : YukawaTrilinearForm K E_-,
          Y.ContractionInjective ∧ Y.ContractionSurjective.

  It does *not* formalise:

    TFPT boundary kernel  ⟹  BoundaryYukawaKernel K E_-.

  The latter is the TFPT-internal representation-theoretic
  derivation that lives outside the present algebraic Lean note.
-/

import Mathlib.LinearAlgebra.FiniteDimensional.Defs

import TfptCarrier.YukawaTrilinearForm
import TfptCarrier.YukawaStageDExistence

set_option linter.dupNamespace false

namespace TFPT.Carrier.BoundaryYukawaKernelInterface

/--
**`BoundaryYukawaKernel`** — the abstract typed target of TFPT
Paper 2's "the boundary kernel produces a canonical
alternating trilinear coupling on the negative block".

Four fields:

  * `ω` — a Yukawa Stage-D form on `E`.
  * `injective` — `ω.ContractionInjective` (non-degeneracy).
  * `surjective` — `ω.ContractionSurjective` (no spectator).
  * `nontrivial` — `Nontrivial E` (necessary to exclude the
    vacuous `dim E = 0` case).

The combined content is exactly what
`YukawaStageDExistence.stage_D_iff_finrank_eq_three` requires
to force $\dim E = 3$.
-/
structure BoundaryYukawaKernel
    (K : Type*) [Field K]
    (E : Type*) [AddCommGroup E] [Module K E]
    [FiniteDimensional K E] where
  ω : TFPT.Carrier.YukawaTrilinearForm.YukawaTrilinearForm K E
  injective : ω.ContractionInjective
  surjective : ω.ContractionSurjective
  nontrivial : Nontrivial E

namespace BoundaryYukawaKernel

variable {K : Type*} [Field K]
variable {E : Type*} [AddCommGroup E] [Module K E] [FiniteDimensional K E]

/--
**Rank-3 discharge.** Any `BoundaryYukawaKernel` forces
`finrank K E = 3`. -/
theorem finrank_E_eq_three (b : BoundaryYukawaKernel K E) :
    Module.finrank K E = 3 :=
  haveI := b.nontrivial
  b.ω.finrank_E_eq_three b.injective b.surjective

/--
**Existence from rank-3 (and non-triviality).** Conversely, any
finite-dimensional `K`-vector space of dimension 3 admits a
`BoundaryYukawaKernel`. The construction uses the basis-built
Yukawa form of `YukawaStageDExistence`.

This shows that the boundary-Yukawa-kernel interface is
\emph{characterised} (under `Nontrivial`) by the rank-3
condition: -/
noncomputable def ofFinrankEqThree
    [Nontrivial E] (h : Module.finrank K E = 3) :
    BoundaryYukawaKernel K E :=
  let b : Module.Basis (Fin 3) K E := Module.finBasisOfFinrankEq K E h
  { ω := TFPT.Carrier.YukawaStageDExistence.ofBasis b
    injective :=
      TFPT.Carrier.YukawaStageDExistence.ofBasis_contractionInjective b
    surjective :=
      TFPT.Carrier.YukawaStageDExistence.ofBasis_contractionSurjective b
    nontrivial := inferInstance }

/--
**Characterisation.** The boundary Yukawa kernel interface is,
under `Nontrivial`, equivalent to the rank-3 condition. -/
theorem nonempty_iff_finrank_eq_three [Nontrivial E] :
    Nonempty (BoundaryYukawaKernel K E) ↔ Module.finrank K E = 3 :=
  ⟨fun ⟨b⟩ => b.finrank_E_eq_three,
   fun h => ⟨ofFinrankEqThree h⟩⟩

/--
**Bridge to the Yukawa rank witness.** A boundary-Yukawa-kernel
datum produces a Stage-A `YukawaRankCertificate` via the full
Stage D ⇒ C ⇒ B ⇒ A chain. -/
noncomputable def toYukawaRankCertificate (b : BoundaryYukawaKernel K E) :
    TFPT.Carrier.YukawaRank.YukawaRankCertificate K E :=
  haveI := b.nontrivial
  (b.ω.toPrimitiveIndecomposableYukawaCoupling b.injective b.surjective).toYukawaRankCertificate

end BoundaryYukawaKernel

end TFPT.Carrier.BoundaryYukawaKernelInterface
