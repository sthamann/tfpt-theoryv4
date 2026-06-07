/-
  TFPT Carrier — Paper 1 Calderon Interface
  -----------------------------------------

  This module makes the Paper 1 input to the carrier-rigidity
  chain an explicit Lean *certificate*, rather than something
  silently consumed.

  --------------------------------------------------------------
  What Paper 1 contributes
  --------------------------------------------------------------

  TFPT Paper 1 (Boundary Polarization and the Primitive Kernel)
  constructs the carrier involution `ε := ι_C |_E` from the
  Calderón polarisation of an admissible one-sided boundary
  datum. The output of that construction, restricted to the
  finite essential carrier `E`, is an element ε of the
  endomorphism ring of `E` satisfying `ε² = id`.

  The carrier-rigidity chain consumes exactly this output. It
  does *not* attempt to reformalise Paper 1's analytic content:
  the Calderón polarisation, boundary elliptic regularity, and
  the operator-theoretic construction of the involution all
  live upstream of this project.

  --------------------------------------------------------------
  Why an explicit interface
  --------------------------------------------------------------

  In the v5 chain, `CarrierInvolution` (in
  `InvolutionProjectors.lean`) was the entry point of the
  algebraic chain. It is a clean structure but it does *not*
  document that ε is meant to come from Paper 1's Calderón
  polarisation.

  The reviewer's standing critique is that
  this hides an *upstream* dependency: the Lean chain works for
  *any* involution, but the TFPT claim is that the involution is
  produced by a specific boundary construction. Without an
  explicit interface, a reader cannot see at the type-theory
  level "this is the place where Paper 1 enters".

  `CalderonCertificate` below is exactly that interface: a thin
  structural wrapper around `CarrierInvolution` that names the
  Paper 1 origin in its docstring. Any future Lean
  formalisation of Paper 1's boundary elliptic theory would
  *produce* a `CalderonCertificate`; the present chain
  *consumes* it.
-/

import Mathlib.Algebra.GroupWithZero.Invertible
import Mathlib.Algebra.Ring.Basic

import TfptCarrier.InvolutionProjectors

namespace TFPT.Carrier.CalderonInterface

/--
**`CalderonCertificate`** — Paper 1 interface for the carrier
involution.

The certificate carries an element `ε` of a ring `A` (in
practice, `Module.End K E` for a finite-dimensional `K`-vector
space `E`) together with the involutive relation `ε² = 1`.

The intended reading is: ε is the Calderón-induced carrier
involution `ι_C |_E` of TFPT Paper 1, restricted to the finite
essential carrier `E`. The Lean structure does not formalise
the Calderón construction itself; it names where the construction
enters the carrier-rigidity chain.

The forgetful map
`CalderonCertificate A → CarrierInvolution A` then feeds the
algebraic chain in `InvolutionProjectors.lean`.
-/
structure CalderonCertificate (A : Type*) [Ring A] where
  /-- The Calderón-induced carrier involution element. -/
  eps : A
  /-- Involutive relation `ε² = 1`, the output of Paper 1's
      boundary polarisation argument. -/
  eps_sq : eps * eps = 1

namespace CalderonCertificate

variable {A : Type*} [Ring A]

/-- A Calderon certificate produces the algebraic carrier
involution consumed by `InvolutionProjectors`. -/
def toCarrierInvolution (c : CalderonCertificate A) :
    TFPT.Carrier.InvolutionProjectors.CarrierInvolution A where
  eps := c.eps
  eps_sq := c.eps_sq

end CalderonCertificate

/-- Conversely: a `CarrierInvolution` can be re-packaged as a
`CalderonCertificate`, with the understanding that its origin is
*not* certified by the wrapper — only that its algebraic content
is the same.

This is the converse direction. It is sometimes useful to wrap
a `CarrierInvolution` constructed by other means (e.g.\ from a
concrete matrix) into the Calderón-interface shape for
downstream uniformity. -/
def CalderonCertificate.ofCarrierInvolution
    {A : Type*} [Ring A]
    (c : TFPT.Carrier.InvolutionProjectors.CarrierInvolution A) :
    CalderonCertificate A where
  eps := c.eps
  eps_sq := c.eps_sq

end TFPT.Carrier.CalderonInterface
