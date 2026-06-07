/-
  TFPT Carrier — Yukawa Rank Stage-A Certificate
  ----------------------------------------------

  TFPT Paper 2 derives `dim E_- = 3` from the existence of a
  *primitive indecomposable Yukawa type*: a non-degenerate local
  trilinear coupling with two fermionic legs in `E_-` and one
  seam-even bosonic leg in `Λ²E_+`, subject to the carrier-closure
  identity

      E_- ⊗ Λ²E_- → Λ³E_- = det E_-.

  Once `dim E_+ = 2` is fixed (`HiggsIndexShadow`), the closure of
  the negative factor without a spectator forces `dim E_- = 3`.

  --------------------------------------------------------------
  STATUS OF THIS MODULE — DELIBERATELY *RANK WITNESS ONLY*
  --------------------------------------------------------------

  This module is **not** a formalisation of *primitive
  indecomposable Yukawa type*. It is a `YukawaRankCertificate`:
  a structured rank witness — a linear isomorphism
  `Eminus ≃ₗ[K] Fin 3 → K` — that downstream theorems consume as a
  *hypothesis*, not as a derived fact.

  Calling it a witness rather than a definition is deliberate:

  1. A bona-fide Lean formalisation would require a precise
     mathematical definition of "primitive indecomposable Yukawa
     type" that contains *no physics words*. See the *three
     candidate variants* discussed below — choosing among them is
     a mathematical, not engineering, decision.

  2. Once such a definition is fixed, the rank-3 corollary would
     be a *theorem* over that definition. The
     `YukawaRankCertificate` is the receiving interface for the
     conclusion of that future theorem: today it is provided as a
     hypothesis; tomorrow it should be produced as the output of a
     deeper Lean module.

  3. Naming the present object `PrimitiveYukawaTypeCertificate`
     would be misleading. It would invite the reader to believe
     that this module formalises the conceptual content of
     Paper 2 §2; it does not. It formalises the *rank conclusion*
     under the heading "an isomorphism with `K^3` is available".

  -----  CANDIDATE DEFINITIONS FOR FUTURE WORK  -----

  Variant 1 — quiver-theoretic
      A finite incidence graph with prescribed primitivity and
      indecomposability conditions, classified up to isomorphism.
      Best fit if Paper 2 ultimately rests on a combinatorial
      classification.

  Variant 2 — representation-theoretic
      An indecomposable `K`-module `Eminus` with a trilinear
      coupling `Eminus ⊗ Eminus ⊗ Eplusᵛ → K` that respects no
      proper submodule. Closest to the Yukawa-coupling language
      of Paper 2 itself.

  Variant 3 — finite enumeration
      A small `inductive` of admissible Yukawa shapes with the
      colour-triplet shape singled out by an `admissible`
      predicate. Ugly but maximally auditable.

  The decision between these is the principal open problem of
  this experiment.
-/

import Mathlib.LinearAlgebra.FiniteDimensional.Defs
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.FreeModule.Finite.Basic
import Mathlib.Data.Fin.VecNotation

namespace TFPT.Carrier.YukawaRank

variable (K : Type*) [Field K]

/--
The algebraic shadow of the negative polarization block: rank `3`
over `K`, in carrier-basis order `(d_R, d_G, d_B)` for the
down-type quark colour triplet.

This is *not* the definition of "primitive indecomposable Yukawa
type". It is the rank-3 target of the `YukawaRankCertificate`
hypothesis below.
-/
abbrev NegativeBlockShadow : Type _ := Fin 3 → K

/--
**Algebraic rank-3 shadow.**

The carrier-basis realisation of the negative block has dimension
`3` over the ground field. This is a pure rank statement.
-/
theorem finrank_negativeBlockShadow :
    Module.finrank K (NegativeBlockShadow K) = 3 := by
  show Module.finrank K (Fin 3 → K) = 3
  rw [Module.finrank_fintype_fun_eq_card]
  exact Fintype.card_fin 3

variable {K}

/--
**`YukawaRankCertificate`** — Stage-A interface for the rank-3
conclusion `dim E_- = 3`.

A `YukawaRankCertificate K Eminus` exhibits a *linear isomorphism*
`Eminus ≃ₗ[K] (Fin 3 → K)`. Producing such a certificate is
strictly weaker than proving the bona-fide Yukawa-type theorem of
Paper 2: the certificate carries only the rank conclusion of that
theorem, not its conceptual content.

Downstream theorems (`CarrierData.lean`) consume the certificate
as a *hypothesis*. The principal mathematical extension point of
this experiment is to replace the bare certificate with a
constructive Lean theorem deriving it from a future formal
definition of *primitive indecomposable Yukawa type*.
-/
structure YukawaRankCertificate
    (K : Type*) [Field K]
    (Eminus : Type*) [AddCommGroup Eminus] [Module K Eminus] where
  toShadow : Eminus ≃ₗ[K] NegativeBlockShadow K

variable {Eminus : Type*} [AddCommGroup Eminus] [Module K Eminus]

/-- A `YukawaRankCertificate` transfers finite-dimensionality. -/
instance (cert : YukawaRankCertificate K Eminus) :
    FiniteDimensional K Eminus :=
  Module.Finite.equiv cert.toShadow.symm

/--
**Rank corollary.**

A `YukawaRankCertificate` forces `dim Eminus = 3`.

This is a one-line composition: the certificate exhibits the
linear isomorphism, and `finrank_negativeBlockShadow` reads off
the dimension of the target. It does *not* close the gap to a
formal definition of primitive indecomposable Yukawa type.
-/
theorem YukawaRankCertificate.finrank_Eminus_eq_three
    (cert : YukawaRankCertificate K Eminus) :
    Module.finrank K Eminus = 3 := by
  rw [LinearEquiv.finrank_eq cert.toShadow]
  exact finrank_negativeBlockShadow K

end TFPT.Carrier.YukawaRank
