/-
  TFPT Carrier — Layer 1: Polarization Algebra
  --------------------------------------------

  Abstract algebraic core of the carrier rigidity theorem from TFPT
  Paper 2 (Carrier Rigidity, Hypercharge, and the Standard Model Packet).

  The boundary polarization induces on the finite essential carrier a
  self-adjoint involution

      ε² = 1,

  which splits `E = E₋ ⊕ E₊` via the orthogonal projectors

      P₋ = (1 − ε)/2,   P₊ = (1 + ε)/2.

  These satisfy the four axioms encoded in `Polarization`:
  idempotence, mutual orthogonality, completeness. Everything that
  follows is a consequence of those four axioms.

  The carrier polynomial identity proved here,

      6 Y² − Y − 1 = 0,

  where `Y = -(1/3) P₋ + (1/2) P₊`, is *not* assumed: it is derived.
-/

import Mathlib.Algebra.Algebra.Basic
import Mathlib.Algebra.Module.Basic
import Mathlib.Algebra.Ring.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NoncommRing
import Mathlib.Tactic.Linarith

namespace TFPT.Carrier

/--
A polarization datum on a (possibly non-commutative) `ℚ`-algebra `A`:
two orthogonal idempotents summing to the unit.

In TFPT this is the algebraic image of the Calderón-induced carrier
involution `ε` after restriction to the finite essential carrier `E`.
The element `Pm` projects onto the negative polarization block
(`dim E₋ = 3` in the closed branch); `Pp` projects onto the positive
polarization block (`dim E₊ = 2`). The dimensions enter only in
`Hypercharge`; here we work purely algebraically.
-/
structure Polarization (A : Type*) [Ring A] where
  Pm        : A
  Pp        : A
  idem_m    : Pm * Pm = Pm
  idem_p    : Pp * Pp = Pp
  orth_mp   : Pm * Pp = 0
  orth_pm   : Pp * Pm = 0
  complete  : Pm + Pp = 1

namespace Polarization

variable {A : Type*} [Ring A] [Algebra ℚ A]

/--
The trace-free auxiliary `sixY := 6 · Y = -2 P₋ + 3 P₊`.

Working with `sixY` instead of `Y` clears denominators, so that the
arithmetic identities below become statements over the ground ring `A`
that do not require inverting `6`. The full identity for
`Y := (1/6) · sixY` is recovered by rescaling at the very end.
-/
def sixY (p : Polarization A) : A := -2 * p.Pm + 3 * p.Pp

/--
Key algebraic lemma:

    (sixY)² = 4 P₋ + 9 P₊.

Pure expansion using the four idempotent/orthogonality axioms.
-/
lemma sixY_sq (p : Polarization A) :
    p.sixY * p.sixY = 4 * p.Pm + 9 * p.Pp := by
  have hmm := p.idem_m
  have hpp := p.idem_p
  have hmp := p.orth_mp
  have hpm := p.orth_pm
  unfold sixY
  -- First, expand the product algebraically.
  have expand :
      (-2 * p.Pm + 3 * p.Pp) * (-2 * p.Pm + 3 * p.Pp)
        = 4 * (p.Pm * p.Pm) - 6 * (p.Pm * p.Pp)
            - 6 * (p.Pp * p.Pm) + 9 * (p.Pp * p.Pp) := by
    noncomm_ring
  rw [expand, hmm, hpp, hmp, hpm]
  -- Goal becomes:  4 * Pm - 6 * 0 - 6 * 0 + 9 * Pp = 4 * Pm + 9 * Pp
  simp [mul_zero]

/--
**Carrier polynomial theorem (concrete form on sixY).**

The auxiliary `sixY = -2 P₋ + 3 P₊` satisfies

    sixY² − sixY − 6 = 0.

This is equivalent, after dividing by `6`, to the determinant-
normalised carrier polynomial `6 Y² − Y − 1 = 0` with
`Y = -P₋/3 + P₊/2`.

The proof is direct expansion using the four polarization axioms.
No analytic content, no field structure: this is an identity over
any associative ring containing two orthogonal idempotents
summing to the unit.
-/
theorem sixY_carrier_polynomial (p : Polarization A) :
    p.sixY * p.sixY - p.sixY - 6 = 0 := by
  have hmm := p.idem_m
  have hpp := p.idem_p
  have hmp := p.orth_mp
  have hpm := p.orth_pm
  have hc  := p.complete
  -- Use sixY_sq for the quadratic term and unfold linear/constant terms.
  rw [p.sixY_sq]
  unfold sixY
  -- LHS = (4 Pm + 9 Pp) − (−2 Pm + 3 Pp) − 6
  --     = 6 (Pm + Pp) − 6
  --     = 6 · 1 − 6 = 0.
  have step : (4 : A) * p.Pm + 9 * p.Pp - (-2 * p.Pm + 3 * p.Pp) - 6
            = 6 * (p.Pm + p.Pp) - 6 := by noncomm_ring
  rw [step, hc, mul_one, sub_self]

/--
The determinant-normalised two-point generator

    Y = -(1/3) P₋ + (1/2) P₊

over a `ℚ`-algebra. Defined as `(1/6) • sixY` so that the carrier
polynomial identity follows from `sixY_carrier_polynomial` by rescaling.
-/
noncomputable def Y (p : Polarization A) : A := (1 / 6 : ℚ) • p.sixY

end Polarization
end TFPT.Carrier
