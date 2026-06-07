/-
  TFPT Carrier — Seam-Winding Interface
  -------------------------------------

  v11 upstream layer for the lattice-rigidity input.

  In TFPT Paper 2, the conditions on the integer charges
  `(q_-, q_+)` — determinant trace-zero, orientation,
  primitivity — are not assumed: they are *derived* from the
  seam-class data `[u_Σ] ∈ H^1(\Sigma, \mathbb{Z})`. The TFPT
  Paper-2 statement reads, in slogan form:

      seam-winding `[u_Σ] = 1`
        ⟹  primitive oriented determinant-preserving carrier.

  The analytic / topological derivation of the seam-winding
  condition from the TFPT spectral data is upstream physics
  work (Paper 2 §3). The *Lean-side target* of that future
  derivation is to produce a
  `PrimitiveOrientedDeterminantCarrier`.

  This module provides a structural typed interface
  `SeamWindingData` capturing the abstract algebraic content
  of "seam class equals 1": a chirality sign on the negative
  block, a chirality sign on the positive block, a winding
  integer, and the algebraic primitivity condition. The
  forward bridge
  `SeamWindingData.toPrimitiveOrientedDeterminantCarrier`
  feeds the existing lattice-rigidity chain.

  --------------------------------------------------------------
  Scope discipline
  --------------------------------------------------------------

  This module formalises:

    SeamWindingData (m n)  ⟹  PrimitiveOrientedDeterminantCarrier (m n).

  It does *not* formalise:

    TFPT seam class `[u_Σ] = 1`  ⟹  SeamWindingData (m n).

  The latter is the boundary-topological content of Paper 2 §3,
  which lives outside the present algebraic Lean note.
-/

import Mathlib.Data.Int.GCD
import Mathlib.Tactic.Linarith

import TfptCarrier.OrientedDeterminantCarrier

set_option linter.dupNamespace false

namespace TFPT.Carrier.SeamWindingInterface

/--
**`SeamWindingData`** — the abstract algebraic content of the
TFPT seam-class condition `[u_Σ] = 1`.

Four fields:

  * `q_minus`, `q_plus` — the integer charges on the negative
    and positive polarisation blocks (the "winding integers").
  * `det_trace_zero` — `m · q_- + n · q_+ = 0`, the algebraic
    consequence of `[u_Σ]` being a class \emph{trivialised by
    the determinant character} of the carrier torus.
  * `orientation_neg`, `orientation_pos` — `q_- < 0 < q_+`,
    the chirality split: positive winding on the positive
    block, negative on the negative.
  * `primitive` — `gcd(|q_-|, q_+) = 1`, the primitivity of
    the seam class: it is a generator of its $\mathbb Z$-line,
    not a non-trivial multiple.

This structure is *isomorphic* (as a typed datum) to
`PrimitiveOrientedDeterminantCarrier`. It is supplied as a
separate name to make the TFPT-side interpretation explicit:
the Lean-side target of "seam winding 1" is precisely the
production of a `SeamWindingData`.
-/
structure SeamWindingData (m n : ℕ) where
  q_minus : ℤ
  q_plus  : ℤ
  det_trace_zero : (m : ℤ) * q_minus + (n : ℤ) * q_plus = 0
  orientation_neg : q_minus < 0
  orientation_pos : 0 < q_plus
  primitive : Int.gcd q_minus q_plus = 1

namespace SeamWindingData

variable {m n : ℕ}

/--
**Bridge: seam-winding data ⇒ primitive oriented determinant
carrier.**

The seam-winding interface forgets the topological
interpretation and exposes only the algebraic content needed
by lattice rigidity. -/
def toPrimitiveOrientedDeterminantCarrier
    (s : SeamWindingData m n) :
    TFPT.Carrier.OrientedDeterminantCarrier.PrimitiveOrientedDeterminantCarrier m n where
  q_minus := s.q_minus
  q_plus  := s.q_plus
  det_trace_zero := s.det_trace_zero
  orientation_neg := s.orientation_neg
  orientation_pos := s.orientation_pos
  primitive := s.primitive

/--
**Converse: every primitive oriented determinant carrier
arises from a seam-winding datum.**

This converse shows that the seam-winding interface is not
a new constraint: it is precisely the existing carrier
condition, named to make the upstream TFPT theorem visible.
The seam-winding bridge is therefore a typed renaming, not a
strengthening or weakening of the rigidity input. -/
def ofPrimitiveOrientedDeterminantCarrier
    (c : TFPT.Carrier.OrientedDeterminantCarrier.PrimitiveOrientedDeterminantCarrier m n) :
    SeamWindingData m n where
  q_minus := c.q_minus
  q_plus  := c.q_plus
  det_trace_zero := c.det_trace_zero
  orientation_neg := c.orientation_neg
  orientation_pos := c.orientation_pos
  primitive := c.primitive

/--
**SM specialisation.** A seam-winding datum on the rank-(3,2)
splitting forces $(q_-, q_+) = (-2, 3)$. This is the integer
content of the SM carrier theorem, presented through the
seam-winding interface. -/
theorem sm_pair_eq (s : SeamWindingData 3 2) :
    s.q_minus = -2 ∧ s.q_plus = 3 :=
  s.toPrimitiveOrientedDeterminantCarrier.sm_pair_eq

end SeamWindingData

end TFPT.Carrier.SeamWindingInterface
