/-
  TFPT Carrier — Boundary Involution → Complete Orthogonal Idempotents
  --------------------------------------------------------------------

  This is the missing algebraic bridge between

      Paper 1 (boundary polarization gives an involution ε with ε² = 1)

  and

      Polarization.Polarization (two orthogonal idempotents summing to 1).

  Given an involution `ε` in a ring `A` where `2` is invertible, the
  spectral projectors

      P₋ = (1 - ε) · ⅟2,    P₊ = (1 + ε) · ⅟2

  satisfy the four polarization axioms.

  We work in an abstract ring `A` with `Invertible (2 : A)` so the
  construction applies uniformly to `Module.End K E` (for `K` of
  characteristic ≠ 2) and to any other concrete carrier algebra.
-/

import Mathlib.Algebra.GroupWithZero.Invertible
import Mathlib.Algebra.Ring.Basic
import Mathlib.Tactic.NoncommRing

import TfptCarrier.Polarization

namespace TFPT.Carrier.InvolutionProjectors

/--
The data of a carrier involution: an element `ε` of a ring squaring
to the identity.

In the intended application `A = Module.End K E` and `ε` is the
Calderón-induced carrier involution `ε := iota_C |_E` of Paper 1.
The constraint `ε * ε = 1` is the only piece imported from the
analytic content of the boundary polarization.
-/
structure CarrierInvolution (A : Type*) [Ring A] where
  eps : A
  eps_sq : eps * eps = 1

namespace CarrierInvolution

variable {A : Type*} [Ring A] [Invertible (2 : A)]

/-- The numeral `(2 : A)` commutes with every ring element. -/
private lemma two_commute (x : A) : Commute (2 : A) x := by
  rw [show (2 : A) = 1 + 1 by norm_num]
  exact (Commute.one_left x).add_left (Commute.one_left x)

/-- `⅟(2 : A)` commutes with every ring element. -/
private lemma invOf_two_commute (x : A) : Commute (⅟(2 : A)) x :=
  (two_commute x).invOf_left

/-- Generic idempotency from the self-double identity `x · x = 2 · x`. -/
private lemma idem_of_self_double {x : A} (hx : x * x = 2 * x) :
    (x * ⅟(2 : A)) * (x * ⅟(2 : A)) = x * ⅟(2 : A) := by
  have hc : Commute (⅟(2 : A)) x := invOf_two_commute x
  have hc2 : Commute (2 : A) x := two_commute x
  calc (x * ⅟(2 : A)) * (x * ⅟(2 : A))
      = (x * x) * (⅟(2 : A) * ⅟(2 : A)) := hc.mul_mul_mul_comm x ⅟(2 : A)
    _ = (2 * x) * (⅟(2 : A) * ⅟(2 : A)) := by rw [hx]
    _ = (x * 2) * (⅟(2 : A) * ⅟(2 : A)) := by rw [hc2.eq]
    _ = x * (2 * ⅟(2 : A)) * ⅟(2 : A) := by
        rw [mul_assoc x (2 : A) _,
            ← mul_assoc (2 : A) (⅟(2 : A)) (⅟(2 : A)),
            ← mul_assoc x (2 * ⅟(2 : A)) _]
    _ = x * 1 * ⅟(2 : A) := by rw [mul_invOf_self]
    _ = x * ⅟(2 : A) := by rw [mul_one]

/-- Generic orthogonality from the annihilation identity `x · y = 0`. -/
private lemma orth_of_annihilate {x y : A} (hxy : x * y = 0) :
    (x * ⅟(2 : A)) * (y * ⅟(2 : A)) = 0 := by
  have hc : Commute (⅟(2 : A)) y := invOf_two_commute y
  calc (x * ⅟(2 : A)) * (y * ⅟(2 : A))
      = (x * y) * (⅟(2 : A) * ⅟(2 : A)) := hc.mul_mul_mul_comm x ⅟(2 : A)
    _ = 0 * (⅟(2 : A) * ⅟(2 : A)) := by rw [hxy]
    _ = 0 := zero_mul _

variable (c : CarrierInvolution A)

/-- The negative polarization projector `P₋ = (1 - ε) · ⅟2`. -/
noncomputable def Pminus : A := (1 - c.eps) * ⅟(2 : A)

/-- The positive polarization projector `P₊ = (1 + ε) · ⅟2`. -/
noncomputable def Pplus : A := (1 + c.eps) * ⅟(2 : A)

/-- Sum: `P₋ + P₊ = 1`. -/
theorem Pminus_add_Pplus : c.Pminus + c.Pplus = 1 := by
  unfold Pminus Pplus
  rw [← add_mul]
  have hsum : (1 - c.eps + (1 + c.eps) : A) = 2 := by
    rw [show ((2 : A)) = 1 + 1 by norm_num]
    abel
  rw [hsum]
  exact mul_invOf_self _

/-- Algebraic core: `(1 - ε)² = 2 · (1 - ε)` whenever `ε² = 1`. -/
private lemma sq_minus :
    (1 - c.eps) * (1 - c.eps) = 2 * (1 - c.eps) := by
  have he : c.eps * c.eps = 1 := c.eps_sq
  calc
    (1 - c.eps) * (1 - c.eps)
        = 1 - c.eps - c.eps + c.eps * c.eps := by noncomm_ring
    _   = 1 - c.eps - c.eps + 1 := by rw [he]
    _   = 2 * (1 - c.eps) := by
          rw [show (2 : A) = 1 + 1 by norm_num]
          noncomm_ring

/-- Algebraic core: `(1 + ε)² = 2 · (1 + ε)` whenever `ε² = 1`. -/
private lemma sq_plus :
    (1 + c.eps) * (1 + c.eps) = 2 * (1 + c.eps) := by
  have he : c.eps * c.eps = 1 := c.eps_sq
  calc
    (1 + c.eps) * (1 + c.eps)
        = 1 + c.eps + c.eps + c.eps * c.eps := by noncomm_ring
    _   = 1 + c.eps + c.eps + 1 := by rw [he]
    _   = 2 * (1 + c.eps) := by
          rw [show (2 : A) = 1 + 1 by norm_num]
          noncomm_ring

/-- Algebraic core: `(1 - ε)(1 + ε) = 0` whenever `ε² = 1`. -/
private lemma mul_pm :
    (1 - c.eps) * (1 + c.eps) = 0 := by
  have he : c.eps * c.eps = 1 := c.eps_sq
  calc
    (1 - c.eps) * (1 + c.eps) = 1 - c.eps * c.eps := by noncomm_ring
    _                          = 1 - 1            := by rw [he]
    _                          = 0                := sub_self 1

/-- Algebraic core: `(1 + ε)(1 - ε) = 0` whenever `ε² = 1`. -/
private lemma mul_mp :
    (1 + c.eps) * (1 - c.eps) = 0 := by
  have he : c.eps * c.eps = 1 := c.eps_sq
  calc
    (1 + c.eps) * (1 - c.eps) = 1 - c.eps * c.eps := by noncomm_ring
    _                          = 1 - 1            := by rw [he]
    _                          = 0                := sub_self 1

/-- `P₋` is idempotent: `P₋ * P₋ = P₋`. -/
theorem Pminus_idem : c.Pminus * c.Pminus = c.Pminus :=
  idem_of_self_double c.sq_minus

/-- `P₊` is idempotent: `P₊ * P₊ = P₊`. -/
theorem Pplus_idem : c.Pplus * c.Pplus = c.Pplus :=
  idem_of_self_double c.sq_plus

/-- `P₋` and `P₊` are orthogonal: `P₋ * P₊ = 0`. -/
theorem Pminus_mul_Pplus : c.Pminus * c.Pplus = 0 :=
  orth_of_annihilate c.mul_pm

/-- `P₊` and `P₋` are orthogonal: `P₊ * P₋ = 0`. -/
theorem Pplus_mul_Pminus : c.Pplus * c.Pminus = 0 :=
  orth_of_annihilate c.mul_mp

/--
**Main bridge theorem.**

The projectors `P₋, P₊` built from a carrier involution `ε` in a
ring with `Invertible (2 : A)` form a polarization in the sense of
`TFPT.Carrier.Polarization`. The four axioms — idempotence of both
projectors, mutual orthogonality, and completeness — all follow from
`ε² = 1` by elementary algebra.

Specialising to `A = Module.End K E` for a field `K` of
characteristic ≠ 2 recovers the projector construction
`P₋ = (id - ε)/2`, `P₊ = (id + ε)/2` used throughout TFPT Paper 1
and Paper 2.
-/
noncomputable def toPolarization : TFPT.Carrier.Polarization A where
  Pm := c.Pminus
  Pp := c.Pplus
  idem_m := c.Pminus_idem
  idem_p := c.Pplus_idem
  orth_mp := c.Pminus_mul_Pplus
  orth_pm := c.Pplus_mul_Pminus
  complete := c.Pminus_add_Pplus

end CarrierInvolution

end TFPT.Carrier.InvolutionProjectors
