/-
  TFPT Carrier — Boundary Polarisation
  ------------------------------------

  v10 upstream layer for the Calderón interface.

  In Paper 1's analytic incarnation, the Calderón polarisation
  is the decomposition of a boundary spectral space into a
  positive and a negative chirality block,

      H = H_+ ⊕ H_-,

  where the two blocks are spanned by the eigenspaces of the
  boundary spectral operator above and below threshold. The
  Calderón projector is then the linear projection onto `H_+`
  along `H_-`. Its key algebraic property is idempotency.

  This module captures the *algebraic skeleton* of that
  construction: a `BoundaryPolarization` is a complementary
  pair of submodules of a `K`-module `H`. The projection onto
  the positive block (an endomorphism of `H`) is idempotent by
  the standard Mathlib lemma `IsCompl.projection_isIdempotentElem`.

  Composing the two bridges

      BoundaryPolarization  →  CalderonProjector  →
      CalderonCertificate   →  CarrierInvolution

  feeds the carrier-rigidity chain entirely from a polarisation
  datum, modulo `Invertible (2 : K)` (i.e.\ `char K ≠ 2`).

  --------------------------------------------------------------
  Scope discipline
  --------------------------------------------------------------

  This module formalises the *algebraic step* from a polarised
  module to a Calderón idempotent. The analytic content of
  Paper 1 — boundary elliptic theory producing the spectral
  decomposition `H = H_+ ⊕ H_-` from a Calderón operator on
  Sobolev spaces — remains upstream. The structure here is the
  Lean-side target for that analytic theorem: a future
  formalisation of Paper 1 would produce a
  `BoundaryPolarization` from the boundary spectral pair.
-/

import Mathlib.LinearAlgebra.Projection
import Mathlib.Algebra.Module.End
import Mathlib.Algebra.GroupWithZero.Invertible
import Mathlib.GroupTheory.Submonoid.Center

import TfptCarrier.CalderonProjector

set_option linter.dupNamespace false

open Submodule

namespace TFPT.Carrier.BoundaryPolarization

section InvertibleTwoInEnd

variable (R : Type*) [Semiring R] [Invertible (2 : R)]
variable (M : Type*) [AddCommMonoid M] [Module R M]

/-- **Helper instance**: if `2` is invertible in the scalar ring,
it is invertible in the endomorphism ring. This is the same
instance as in `Mathlib.LinearAlgebra.QuadraticForm.Basic`,
inlined here to avoid pulling in the full quadratic-form
infrastructure. -/
noncomputable instance invertibleTwoEnd :
    Invertible (2 : Module.End R M) where
  invOf := (⟨⅟2, Set.invOf_mem_center (Set.ofNat_mem_center _ _)⟩ :
    Submonoid.center R) • (1 : Module.End R M)
  invOf_mul_self := by
    ext m
    dsimp [Submonoid.smul_def]
    rw [← ofNat_smul_eq_nsmul R, invOf_smul_smul (2 : R) m]
  mul_invOf_self := by
    ext m
    dsimp [Submonoid.smul_def]
    rw [← ofNat_smul_eq_nsmul R, smul_invOf_smul (2 : R) m]

end InvertibleTwoInEnd

/--
**`BoundaryPolarization`** — algebraic skeleton of the
Paper 1 Calderón polarisation.

A complementary pair of `K`-submodules of `H`:
`Hplus` (the positive chirality block) and `Hminus` (the
negative chirality block), with `Hplus ⊕ Hminus = H` encoded
as the Mathlib predicate `IsCompl Hplus Hminus`.

In Paper 1's analytic incarnation, `Hplus` and `Hminus` are the
positive and negative spectral subspaces of the boundary Dirac
operator restricted to the doubled boundary. The Lean side
consumes only the direct-sum structure.
-/
structure BoundaryPolarization
    (K : Type*) [Field K]
    (H : Type*) [AddCommGroup H] [Module K H] where
  /-- The positive polarisation block. -/
  Hplus : Submodule K H
  /-- The negative polarisation block. -/
  Hminus : Submodule K H
  /-- The two blocks are complementary: `H = Hplus ⊕ Hminus`. -/
  isCompl : IsCompl Hplus Hminus

namespace BoundaryPolarization

variable {K : Type*} [Field K]
variable {H : Type*} [AddCommGroup H] [Module K H]

/--
**The Calderón projector of the polarisation.**

The linear endomorphism of `H` that projects onto `Hplus` along
`Hminus`. Concretely

    π(h_+ + h_-) = h_+    for h_+ ∈ Hplus, h_- ∈ Hminus.

By the standard Mathlib lemma `IsCompl.projection_isIdempotentElem`,
this endomorphism is idempotent.
-/
noncomputable def projector (P : BoundaryPolarization K H) :
    Module.End K H :=
  P.isCompl.projection

/--
**Algebraic core**: the Calderón projector is idempotent.

This is the algebraic content of "the boundary projector is a
projector": `π² = π` in the endomorphism algebra of `H`.
-/
theorem projector_isIdempotent (P : BoundaryPolarization K H) :
    P.projector * P.projector = P.projector :=
  P.isCompl.projection_isIdempotentElem

/--
**Bridge: BoundaryPolarization ⇒ CalderonProjector.**

Given a polarisation `H = Hplus ⊕ Hminus` and `2` invertible in
`K`, the projector `π` produces a
`CalderonProjector` in the endomorphism algebra
`Module.End K H`. The idempotent identity `π² = π` is exactly
the Calderón-projector axiom.
-/
noncomputable def toCalderonProjector
    [Invertible (2 : K)]
    (P : BoundaryPolarization K H) :
    TFPT.Carrier.CalderonProjector.CalderonProjector
      (Module.End K H) where
  π := P.projector
  π_sq := P.projector_isIdempotent

/--
**Convenience bridge: BoundaryPolarization ⇒ CarrierInvolution**

Composes the two bridges
`BoundaryPolarization → CalderonProjector → CarrierInvolution`.
The resulting carrier involution is `ε := 2π − 1` where `π` is
the projection onto `Hplus` along `Hminus`.
-/
noncomputable def toCarrierInvolution
    [Invertible (2 : K)]
    (P : BoundaryPolarization K H) :
    TFPT.Carrier.InvolutionProjectors.CarrierInvolution
      (Module.End K H) :=
  P.toCalderonProjector.toCarrierInvolution

/--
**Convenience bridge: BoundaryPolarization ⇒ CalderonCertificate**

Composes the two bridges
`BoundaryPolarization → CalderonProjector → CalderonCertificate`.
-/
noncomputable def toCalderonCertificate
    [Invertible (2 : K)]
    (P : BoundaryPolarization K H) :
    TFPT.Carrier.CalderonInterface.CalderonCertificate
      (Module.End K H) :=
  P.toCalderonProjector.toCalderonCertificate

end BoundaryPolarization

/-- **Converse construction**: any carrier involution on
`Module.End K H` produces a `BoundaryPolarization` of `H`.

In other words, the two algebraic-side presentations of the
Paper-1 input are \emph{equivalent} once `2` is invertible
in `K`:

  * `BoundaryPolarization K H`   (direct-sum picture)
  * `CarrierInvolution (Module.End K H)`   (involution picture)

The forward direction is `BoundaryPolarization.toCarrierInvolution`,
and this converse closes the equivalence. The remaining open
content of Paper 1 is therefore precisely the analytic
construction of \emph{either} presentation from the boundary
elliptic theory.

Construction: given `ε : End K H` with `ε² = 1` and
`2` invertible in `K`, define the +1 and -1 eigenspaces

    H_+ := range ((1 + ε) ⋅ ⅟2),
    H_- := range ((1 - ε) ⋅ ⅟2).

These are complementary by the elementary identities
`P_+ + P_- = 1`, `P_+² = P_+`, `P_-² = P_-`,
`P_+ * P_- = 0`, `P_- * P_+ = 0` of `InvolutionProjectors`.
-/
noncomputable def BoundaryPolarization.ofCarrierInvolution
    {K : Type*} [Field K] [Invertible (2 : K)]
    {H : Type*} [AddCommGroup H] [Module K H]
    (c : TFPT.Carrier.InvolutionProjectors.CarrierInvolution
          (Module.End K H)) :
    BoundaryPolarization K H where
  Hplus := LinearMap.range c.Pplus
  Hminus := LinearMap.range c.Pminus
  isCompl := by
    -- Cross-annihilation: for any h, Pplus (Pminus h) = 0 and Pminus (Pplus h) = 0.
    have hpm : ∀ h : H, c.Pplus (c.Pminus h) = 0 := fun h =>
      congrArg (fun φ : Module.End K H => φ h) c.Pplus_mul_Pminus
    have hmp : ∀ h : H, c.Pminus (c.Pplus h) = 0 := fun h =>
      congrArg (fun φ : Module.End K H => φ h) c.Pminus_mul_Pplus
    -- Idempotency at the pointwise level.
    have hpp : ∀ h : H, c.Pplus (c.Pplus h) = c.Pplus h := fun h =>
      congrArg (fun φ : Module.End K H => φ h) c.Pplus_idem
    have hmm : ∀ h : H, c.Pminus (c.Pminus h) = c.Pminus h := fun h =>
      congrArg (fun φ : Module.End K H => φ h) c.Pminus_idem
    -- Sum identity at pointwise level.
    have hsum : ∀ h : H, c.Pminus h + c.Pplus h = h := fun h => by
      have := congrArg (fun φ : Module.End K H => φ h) c.Pminus_add_Pplus
      simpa [LinearMap.add_apply] using this
    refine ⟨?_, ?_⟩
    · -- Disjoint.
      rw [disjoint_iff_inf_le]
      rintro v ⟨⟨a, ha⟩, ⟨b, hb⟩⟩
      -- v = Pplus a = Pminus b.
      -- Then Pplus v = Pplus (Pminus b) = 0 and Pminus v = Pminus (Pplus a) = 0.
      -- Hence v = Pminus v + Pplus v = 0.
      have hPplus_v : c.Pplus v = 0 := by rw [← hb]; exact hpm b
      have hPminus_v : c.Pminus v = 0 := by rw [← ha]; exact hmp a
      have hv_zero : v = 0 := by
        have := hsum v
        rw [hPminus_v, hPplus_v, zero_add] at this
        exact this.symm
      simp [hv_zero]
    · -- Codisjoint.
      rw [codisjoint_iff_le_sup]
      intro v _
      have hdec : v = c.Pplus v + c.Pminus v := by
        have h := hsum v
        rw [add_comm] at h
        exact h.symm
      rw [hdec]
      exact Submodule.add_mem_sup
        (LinearMap.mem_range_self _ v)
        (LinearMap.mem_range_self _ v)

end TFPT.Carrier.BoundaryPolarization
