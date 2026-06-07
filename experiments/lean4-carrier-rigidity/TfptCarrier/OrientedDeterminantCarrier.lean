/-
  TFPT Carrier — Primitive Oriented Determinant-Preserving Condition
  ------------------------------------------------------------------

  TFPT Paper 2 combines three conditions on the integer charges
  `(q_-, q_+)` to fix the carrier:

  1. **Determinant trace-zero**:  `m·q_- + n·q_+ = 0`.
     This is the determinant-character condition on the carrier
     torus (`DeterminantCharacter`).

  2. **Orientation**:  `q_- < 0 < q_+`.
     This is the polarisation orientation (the negative block
     carries negative charges, the positive block positive ones).

  3. **Primitivity**:  `gcd(|q_-|, q_+) = 1`.
     This is the primitive-lattice content: the pair is not a
     non-trivial multiple of another pair.

  Lattice rigidity (`LatticeRigidityGeneral`) requires all three.

  This module packages the three conditions into a single Lean
  structure `PrimitiveOrientedDeterminantCarrier`, so that the
  TFPT-side claim "the seam-winding number determines a primitive
  oriented determinant-preserving carrier" becomes a single Lean
  target: producing a `PrimitiveOrientedDeterminantCarrier`.

  The bridge `toRigidityHypotheses` extracts the three components
  in the form consumed by `LatticeRigidityGeneral`.
-/

import Mathlib.Data.Int.GCD
import Mathlib.Tactic.Linarith

import TfptCarrier.LatticeRigidityGeneral
import TfptCarrier.Rigidity

namespace TFPT.Carrier.OrientedDeterminantCarrier

/--
**`PrimitiveOrientedDeterminantCarrier`** — the carrier-rigidity
input bundling the three integer conditions of TFPT Paper 2.

The fields correspond directly to the three hypotheses of
`LatticeRigidityGeneral.primitive_trace_free_pair_general`:
trace-zero, orientation, primitivity.

In a future TFPT formalisation, the *target* of the
seam-winding-class theorem `[u_Σ] = 1` would be to produce a
`PrimitiveOrientedDeterminantCarrier`.
-/
structure PrimitiveOrientedDeterminantCarrier (m n : ℕ) where
  /-- The integer charge on the negative polarisation block. -/
  q_minus : ℤ
  /-- The integer charge on the positive polarisation block. -/
  q_plus  : ℤ
  /-- Determinant trace-zero: `m · q_- + n · q_+ = 0`.
      Derived from the determinant character of the carrier torus. -/
  det_trace_zero : (m : ℤ) * q_minus + (n : ℤ) * q_plus = 0
  /-- Orientation: `q_- < 0 < q_+`. The negative block carries
      negative charge, the positive block positive charge. -/
  orientation_neg : q_minus < 0
  orientation_pos : 0 < q_plus
  /-- Primitivity: the pair is not a non-trivial integer multiple
      of another pair. -/
  primitive : Int.gcd q_minus q_plus = 1

namespace PrimitiveOrientedDeterminantCarrier

variable {m n : ℕ}

/--
The carrier hypotheses extracted from a
`PrimitiveOrientedDeterminantCarrier`, ready for consumption
by `LatticeRigidityGeneral`.
-/
theorem to_rigidity_pair_eq
    (hm : 0 < m) (hn : 0 < n)
    (c : PrimitiveOrientedDeterminantCarrier m n) :
    c.q_minus = -((n / Nat.gcd m n : ℕ) : ℤ) ∧
    c.q_plus = ((m / Nat.gcd m n : ℕ) : ℤ) :=
  TFPT.Carrier.LatticeRigidityGeneral.primitive_trace_free_pair_general
    m n hm hn c.q_minus c.q_plus
    c.det_trace_zero c.orientation_neg c.orientation_pos c.primitive

/--
**SM specialisation `(m, n) = (3, 2)`**: a primitive oriented
determinant-preserving carrier on the `(3, 2)` rank data fixes
`(q_-, q_+) = (-2, 3)`. This is the integer-rigidity content of
the carrier theorem.
-/
theorem sm_pair_eq
    (c : PrimitiveOrientedDeterminantCarrier 3 2) :
    c.q_minus = -2 ∧ c.q_plus = 3 :=
  TFPT.Carrier.Rigidity.unique_carrier_pair
    c.q_minus c.q_plus
    c.det_trace_zero c.orientation_neg c.orientation_pos c.primitive

end PrimitiveOrientedDeterminantCarrier

end TFPT.Carrier.OrientedDeterminantCarrier
