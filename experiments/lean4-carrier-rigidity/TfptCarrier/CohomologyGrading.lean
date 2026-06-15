/-
  TFPT Carrier — Cohomology Grading (QGEO.COHOM.01, the character node)
  ---------------------------------------------------------------------

  Formalises the CONSTRUCTIVE content of `QGEO.COHOM.01`
  (`verification/v177_seam_marking_kernel.py`, node COHOM): the cohomology
  `H^1(P^1 \ mu4)` is spanned by the three eigenforms

      omega_k = z^(k-1) dz / (z^4 - 1),   k = 1, 2, 3,

  and the carrier clock `rho : z |-> i z` acts on them by the CHARACTER

      rho^* omega_k = i^k omega_k,

  so the H^1 character grading is `(i, -1, -i)` with exponents `(1, 2, 3)` = the
  `A_3` exponents = `Spec(Q_+)`, of rank `3 = N_fam`. This module proves the
  pullback-eigenvalue identities as exact rational-function identities in ℂ
  (the pullback `rho^*(g dz) = g(iz) d(iz) = g(iz) * i dz`), and adds the
  reflection parity `sigma^* omega_k = omega_{4-k}` (the MODULE node: the
  reflection `sigma : z |-> 1/z` swaps `omega_1 <-> omega_3` and fixes
  `omega_2`).

  SCOPE.  This is the geometric COHOM/MODULE-parity content GIVEN the marked
  curve `(P^1, mu4)` and the clock (the [E] middle nodes of the proof tree). It
  does NOT close the open obligations `QGEO.MARKS.01` (the raw seam producing
  the marked curve) or `QGEO.KERNEL.01`; the MODULE *uniqueness* (multiplicity-
  free + residue normalisation) stays the symbolic v177 reading. Together with
  `MobiusUniformisation` (UNIFORM) this puts the purely-geometric nodes on a
  formal footing.

  All proofs use only `propext`, `Classical.choice`, `Quot.sound`.
-/

import Mathlib.Tactic
import Mathlib.Data.Complex.Basic
import TfptCarrier.MobiusUniformisation

namespace TFPT.Carrier.CohomologyGrading

open TFPT.Carrier.MobiusUniformisation (I_pow_four)

/-- The three eigenform coefficients `omega_k(z) = z^(k-1)/(z^4-1)` of
`H^1(P^1 \ mu4)` (the `dz` is implicit). -/
noncomputable def omega1 (z : ℂ) : ℂ := 1 / (z ^ 4 - 1)
noncomputable def omega2 (z : ℂ) : ℂ := z / (z ^ 4 - 1)
noncomputable def omega3 (z : ℂ) : ℂ := z ^ 2 / (z ^ 4 - 1)

/-- The clock fixes the denominator: `(i z)^4 - 1 = z^4 - 1` (since `i^4 = 1`). -/
theorem denom_clock_invariant (z : ℂ) : (Complex.I * z) ^ 4 - 1 = z ^ 4 - 1 := by
  rw [mul_pow, I_pow_four, one_mul]

/-! ### COHOM — the pullback character `rho^* omega_k = i^k omega_k` -/

/-- `rho^* omega_1 = i^1 omega_1 = i omega_1` (character `i`). -/
theorem omega1_pullback (z : ℂ) :
    omega1 (Complex.I * z) * Complex.I = Complex.I * omega1 z := by
  unfold omega1
  rw [denom_clock_invariant]; ring

/-- `rho^* omega_2 = i^2 omega_2 = -omega_2` (character `-1`). -/
theorem omega2_pullback (z : ℂ) :
    omega2 (Complex.I * z) * Complex.I = (-1 : ℂ) * omega2 z := by
  unfold omega2
  rw [denom_clock_invariant]
  have h : (Complex.I * z) / (z ^ 4 - 1) * Complex.I
            = Complex.I ^ 2 * (z / (z ^ 4 - 1)) := by ring
  rw [h, Complex.I_sq]

/-- `rho^* omega_3 = i^3 omega_3 = -i omega_3` (character `-i`). -/
theorem omega3_pullback (z : ℂ) :
    omega3 (Complex.I * z) * Complex.I = (-Complex.I) * omega3 z := by
  unfold omega3
  rw [denom_clock_invariant]
  have h : (Complex.I * z) ^ 2 / (z ^ 4 - 1) * Complex.I
            = Complex.I ^ 3 * (z ^ 2 / (z ^ 4 - 1)) := by ring
  have h3 : (Complex.I : ℂ) ^ 3 = -Complex.I := by
    rw [pow_succ, Complex.I_sq]; ring
  rw [h, h3]

/-- **Character grading `(1,2,3)`.** The three pullback eigenvalues are
`i^1, i^2, i^3 = i, -1, -i`, i.e. the characters of weights `(1,2,3)` = the
`A_3` exponents = `Spec(Q_+)`, of rank `3 = N_fam`. -/
theorem character_grading :
    (Complex.I ^ 1, Complex.I ^ 2, Complex.I ^ 3)
      = (Complex.I, (-1 : ℂ), -Complex.I) := by
  refine Prod.ext ?_ (Prod.ext ?_ ?_) <;> simp [pow_succ]

/-! ### MODULE — the reflection parity `sigma^* omega_k = omega_{4-k}` -/

/-- The pullback of `g dz` under the reflection `sigma : z |-> 1/z` is
`g(1/z) * d(1/z) = g(1/z) * (-(1/z^2))`. -/
noncomputable def sigmaPull (g : ℂ → ℂ) (z : ℂ) : ℂ := g z⁻¹ * (-(z ^ 2)⁻¹)

/-- `sigma^* omega_1 = omega_3`: the reflection sends `omega_1` to `omega_3`. -/
theorem omega1_reflection (z : ℂ) (hz : z ≠ 0) (hz4 : z ^ 4 - 1 ≠ 0) :
    sigmaPull omega1 z = omega3 z := by
  unfold sigmaPull omega1 omega3
  have h2 : z ^ 2 ≠ 0 := pow_ne_zero 2 hz
  have h4 : z ^ 4 ≠ 0 := pow_ne_zero 4 hz
  have hinv : (z⁻¹) ^ 4 - 1 ≠ 0 := by
    rw [inv_pow]; intro hcontra; apply hz4
    rw [sub_eq_zero]; exact inv_eq_one.mp (sub_eq_zero.mp hcontra)
  have hz4' : (1 : ℂ) - z ^ 4 ≠ 0 := by
    have e : (1 : ℂ) - z ^ 4 = -(z ^ 4 - 1) := by ring
    rw [e, neg_ne_zero]; exact hz4
  field_simp
  ring

/-- `sigma^* omega_2 = omega_2`: the reflection fixes `omega_2`. -/
theorem omega2_reflection (z : ℂ) (hz : z ≠ 0) (hz4 : z ^ 4 - 1 ≠ 0) :
    sigmaPull omega2 z = omega2 z := by
  unfold sigmaPull omega2
  have h2 : z ^ 2 ≠ 0 := pow_ne_zero 2 hz
  have h4 : z ^ 4 ≠ 0 := pow_ne_zero 4 hz
  have hinv : (z⁻¹) ^ 4 - 1 ≠ 0 := by
    rw [inv_pow]; intro hcontra; apply hz4
    rw [sub_eq_zero]; exact inv_eq_one.mp (sub_eq_zero.mp hcontra)
  have hz4' : (1 : ℂ) - z ^ 4 ≠ 0 := by
    have e : (1 : ℂ) - z ^ 4 = -(z ^ 4 - 1) := by ring
    rw [e, neg_ne_zero]; exact hz4
  field_simp
  ring

/-- `sigma^* omega_3 = omega_1`: the reflection sends `omega_3` to `omega_1`
(so `sigma` swaps `omega_1 <-> omega_3` and fixes `omega_2` -- the integer-model
parity of v141/v146/v177). -/
theorem omega3_reflection (z : ℂ) (hz : z ≠ 0) (hz4 : z ^ 4 - 1 ≠ 0) :
    sigmaPull omega3 z = omega1 z := by
  unfold sigmaPull omega3 omega1
  have h2 : z ^ 2 ≠ 0 := pow_ne_zero 2 hz
  have h4 : z ^ 4 ≠ 0 := pow_ne_zero 4 hz
  have hinv : (z⁻¹) ^ 4 - 1 ≠ 0 := by
    rw [inv_pow]; intro hcontra; apply hz4
    rw [sub_eq_zero]; exact inv_eq_one.mp (sub_eq_zero.mp hcontra)
  have hz4' : (1 : ℂ) - z ^ 4 ≠ 0 := by
    have e : (1 : ℂ) - z ^ 4 = -(z ^ 4 - 1) := by ring
    rw [e, neg_ne_zero]; exact hz4
  field_simp
  ring

/-! ### Bundled (for the signature lock) -/

/-- **`QGEO.COHOM.01` + MODULE parity, bundled.** The pullback character grading
`(i, -1, -i)` (weights `(1,2,3)` = `A_3` exponents) and the reflection parity
`omega_1 <-> omega_3`, `omega_2` fixed. The geometric COHOM/MODULE-parity nodes,
formalised; the MARKS/KERNEL obligations and the MODULE uniqueness stay open. -/
theorem cohom_grading :
    (∀ z : ℂ, omega1 (Complex.I * z) * Complex.I = Complex.I * omega1 z) ∧
    (∀ z : ℂ, omega2 (Complex.I * z) * Complex.I = (-1 : ℂ) * omega2 z) ∧
    (∀ z : ℂ, omega3 (Complex.I * z) * Complex.I = (-Complex.I) * omega3 z) ∧
    (∀ z : ℂ, z ≠ 0 → z ^ 4 - 1 ≠ 0 → sigmaPull omega1 z = omega3 z) ∧
    (∀ z : ℂ, z ≠ 0 → z ^ 4 - 1 ≠ 0 → sigmaPull omega2 z = omega2 z) ∧
    (∀ z : ℂ, z ≠ 0 → z ^ 4 - 1 ≠ 0 → sigmaPull omega3 z = omega1 z) :=
  ⟨omega1_pullback, omega2_pullback, omega3_pullback,
   omega1_reflection, omega2_reflection, omega3_reflection⟩

end TFPT.Carrier.CohomologyGrading
