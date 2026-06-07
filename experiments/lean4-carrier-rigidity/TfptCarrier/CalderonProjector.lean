/-
  TFPT Carrier — Calderón Structural Certificate
  ----------------------------------------------

  v8 upgrade of the Paper 1 interface from "documentary
  wrapper" to "structural derivation".

  In Paper 1's analytic construction, the Calder\'on
  polarisation produces an idempotent operator (the Calder\'on
  projector) on a suitable doubled boundary space. The carrier
  involution `ε_car` is then the spectral reflection associated
  with this projector:

      ε := 2 π − 1,     where  π² = π.

  An elementary algebraic computation gives `ε² = 1`. Concretely
  in any associative ring:

      (2 π − 1)² = 4 π² − 4 π + 1
                 = 4 π − 4 π + 1            [using π² = π]
                 = 1.

  This module formalises that step. A `CalderonProjector` is an
  idempotent ring element, and `toCalderonCertificate` produces
  the Paper 1 interface as a *theorem*, not as a documentary
  hypothesis.

  --------------------------------------------------------------
  Scope discipline
  --------------------------------------------------------------

  This module formalises the *algebraic skeleton* of the
  Calder\'on construction: idempotent in a ring with `2`
  invertible, plus the involutive identity it produces. The full
  analytic content of Paper 1 (boundary elliptic regularity,
  the Calder\'on operator on Sobolev spaces, the doubled
  manifold construction) remains upstream.

  The structure here is the *Lean-side typed target* for the
  Paper 1 analytic theorem. A future Paper 1 formalisation would
  produce a `CalderonProjector` as its conclusion.
-/

import Mathlib.Algebra.GroupWithZero.Invertible
import Mathlib.Algebra.Ring.Basic
import Mathlib.Tactic.NoncommRing

import TfptCarrier.InvolutionProjectors
import TfptCarrier.CalderonInterface

namespace TFPT.Carrier.CalderonProjector

/--
**`CalderonProjector`** — the algebraic skeleton of the
Paper 1 Calder\'on construction: an idempotent element `π` in a
ring with `2` invertible.

In Paper 1's analytic incarnation, `π` is the boundary
projector built from the Calder\'on operator; the ring is the
endomorphism algebra of a doubled boundary spectral space; and
the idempotent identity `π² = π` is the property that the
boundary projector is a true projector. Restricted to the
finite essential carrier, this projector produces the spectral
reflection `ε := 2π − 1` whose square is the identity.

The structure carries only the algebraic content needed by the
carrier-rigidity chain. Producing a `CalderonProjector` from
TFPT Paper 1 is the *target* of a future analytic
formalisation; the present chain consumes the structure.
-/
structure CalderonProjector (A : Type*) [Ring A] [Invertible (2 : A)] where
  /-- The Calderón-induced idempotent: in Paper 1, the boundary
      projector restricted to the finite essential carrier. -/
  π : A
  /-- The defining identity of an idempotent: `π² = π`. -/
  π_sq : π * π = π

namespace CalderonProjector

variable {A : Type*} [Ring A] [Invertible (2 : A)]

/-- The spectral reflection associated with the Calder\'on
projector: `ε := 2 π − 1`. -/
def eps (c : CalderonProjector A) : A := 2 * c.π - 1

/--
**Main algebraic step**: the spectral reflection of an
idempotent is an involution.

For any idempotent `π` in a ring with `2` invertible,
`ε := 2 π − 1` satisfies `ε² = 1`. The proof is the elementary
expansion
`(2π − 1)² = 4π² − 4π + 1 = 4π − 4π + 1 = 1`.
-/
theorem eps_sq (c : CalderonProjector A) : c.eps * c.eps = 1 := by
  unfold eps
  have hπ := c.π_sq
  calc
    (2 * c.π - 1) * (2 * c.π - 1)
        = 4 * (c.π * c.π) - 2 * c.π - 2 * c.π + 1 := by noncomm_ring
    _   = 4 * c.π - 2 * c.π - 2 * c.π + 1         := by rw [hπ]
    _   = 1 := by noncomm_ring

/--
**Bridge: Calderón projector ⇒ Carrier involution.**

A `CalderonProjector` produces a `CarrierInvolution` (the
algebraic-interface object consumed by `InvolutionProjectors`),
via `ε := 2 π − 1` and `ε² = 1`.
-/
def toCarrierInvolution (c : CalderonProjector A) :
    TFPT.Carrier.InvolutionProjectors.CarrierInvolution A where
  eps := c.eps
  eps_sq := c.eps_sq

/--
**Bridge: Calderón projector ⇒ Calderón certificate.**

A `CalderonProjector` produces the higher-level
`CalderonCertificate` of `CalderonInterface`. The Calderón
interface — the place where the Paper 1 input arrives — is now
*derived* from an idempotent projector, not just packaged.
-/
def toCalderonCertificate (c : CalderonProjector A) :
    TFPT.Carrier.CalderonInterface.CalderonCertificate A where
  eps := c.eps
  eps_sq := c.eps_sq

end CalderonProjector

end TFPT.Carrier.CalderonProjector
