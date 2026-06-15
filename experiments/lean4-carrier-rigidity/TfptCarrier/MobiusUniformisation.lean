/-
  TFPT Carrier — Möbius Uniformisation (QGEO.UNIFORM.01, the geometric half)
  --------------------------------------------------------------------------

  Formalises the CONSTRUCTIVE NORMAL FORM of `QGEO.UNIFORM.01`
  (`verification/v177_seam_marking_kernel.py`, node UNIFORM): a genus-0 curve
  with four reduced marks and a faithful order-4 conformal automorphism rotating
  them cyclically is Möbius-equivalent to `(ℙ¹, μ₄)`.  The constructive content
  is the explicit normal form, and that is what this module proves in Lean:

    * the order-4 clock is `ρ : z ↦ i z` (an elliptic Möbius map, fixed points
      `0, ∞`), with `ρ⁴ = id` and `ρ² ≠ id` (order exactly 4);
    * a non-fixed point `a ≠ 0` has orbit `{a, ia, -a, -ia}`, and the scaling
      `z ↦ z/a` sends it to `μ₄ = {1, i, -1, -i}`;
    * the reflection `σ : z ↦ 1/z` is an involution with
      `σ ∘ ρ ∘ σ = ρ⁻¹` (so `⟨ρ, σ⟩` is the dihedral group `D₄` of order 8),
      and `σ` permutes `μ₄` (fixes `1, -1`, swaps `i, -i`);
    * the multiplier classification: a multiplier map `z ↦ ζ z` has order
      exactly 4 iff `ζ = i` or `ζ = -i` (the two primitive 4th roots), and the
      inversion conjugates one to the other — so the canonical representative is
      `z ↦ i z`.

  SCOPE (honest, matching `CalderonProjector`/`SeamDeckClosure`).  The reduction
  "every order-4 elliptic Möbius map has two fixed points and is conjugate to a
  multiplier map" is the standard `PSL(2,ℂ)` elliptic-classification step; here
  the marks/clock are presented in the already-normalised coordinate (fixed
  points `0, ∞`), which is exactly the constructive `QGEO.UNIFORM.01` content
  of `v177`.  This module does NOT close `QGEO.MARKS.01` (the RAW seam producing
  a genus-0 four-marked `D₄` boundary) — that stays the open obligation.  What
  is formalised is the geometric normal form GIVEN the four marks and the clock.

  All proofs use only `propext`, `Classical.choice`, `Quot.sound` (elementary
  complex algebra; no analysis beyond `Complex.I_sq`).
-/

import Mathlib.Tactic
import Mathlib.Data.Complex.Basic

namespace TFPT.Carrier.MobiusUniformisation

/-- The order-4 clock Möbius map `ρ : z ↦ i z` (rotation of the square; fixed
points `0, ∞`). -/
def rho (z : ℂ) : ℂ := Complex.I * z

/-- Its inverse `ρ⁻¹ : z ↦ -i z`. -/
def rhoInv (z : ℂ) : ℂ := -Complex.I * z

/-- The reflection `σ : z ↦ 1/z` (the inversion swapping `0 ↔ ∞`). -/
noncomputable def sigma (z : ℂ) : ℂ := z⁻¹

/-- The four `μ₄` marks `{1, i, -1, -i}`. -/
def mu4 : List ℂ := [1, Complex.I, -1, -Complex.I]

/-! ### Powers of `i` -/

/-- `i⁴ = 1`. -/
theorem I_pow_four : (Complex.I) ^ 4 = 1 := by
  rw [show (4 : ℕ) = 2 * 2 from rfl, pow_mul, Complex.I_sq]; norm_num

/-- `i⁻¹ = -i`. -/
theorem inv_I' : (Complex.I)⁻¹ = -Complex.I := by
  have h : Complex.I * (-Complex.I) = 1 := by
    rw [mul_neg, Complex.I_mul_I]; ring
  exact inv_eq_of_mul_eq_one_right h

/-! ### The order-4 clock -/

/-- `ρ⁴ = id`: the clock has order dividing 4. -/
theorem rho_pow_four (z : ℂ) : rho (rho (rho (rho z))) = z := by
  simp only [rho]
  have h : Complex.I * (Complex.I * (Complex.I * (Complex.I * z))) = Complex.I ^ 4 * z := by
    ring
  rw [h, I_pow_four, one_mul]

/-- `ρ² ≠ id`: the clock has order EXACTLY 4 (`ρ²(1) = -1 ≠ 1`). -/
theorem rho_order_exactly_four : rho (rho 1) ≠ 1 := by
  simp only [rho, mul_one]
  rw [show Complex.I * Complex.I = Complex.I ^ 2 from by ring, Complex.I_sq]
  norm_num

/-! ### The reflection and the `D₄` relation -/

/-- `σ² = id`: the reflection is an involution. -/
theorem sigma_invol (z : ℂ) : sigma (sigma z) = z := by
  simp only [sigma, inv_inv]

/-- The defining dihedral relation `σ ρ σ = ρ⁻¹`: with `ρ⁴ = id`, `σ² = id` this
makes `⟨ρ, σ⟩` the dihedral group `D₄` of order 8 (the faithful `D₄` of v168). -/
theorem sigma_rho_sigma (z : ℂ) : sigma (rho (sigma z)) = rhoInv z := by
  simp only [sigma, rho, rhoInv]
  rw [mul_inv_rev, inv_inv, inv_I']
  ring

/-! ### Orbit of a non-fixed point scales to `μ₄` -/

/-- A non-fixed point `a ≠ 0` has orbit `{a, ia, -a, -ia}` under `ρ`, and the
scaling `z ↦ z/a` sends it exactly to `μ₄ = {1, i, -1, -i}`. -/
theorem orbit_scales_to_mu4 (a : ℂ) (ha : a ≠ 0) :
    a / a = 1 ∧
    (Complex.I * a) / a = Complex.I ∧
    (-a) / a = -1 ∧
    (-Complex.I * a) / a = -Complex.I := by
  refine ⟨div_self ha, ?_, ?_, ?_⟩
  · rw [mul_div_assoc, div_self ha, mul_one]
  · rw [neg_div, div_self ha]
  · rw [mul_div_assoc, div_self ha, mul_one]

/-! ### The reflection permutes `μ₄` -/

/-- `σ` permutes `μ₄`: it fixes `1, -1` and swaps `i ↔ -i` (the integer-model
parity `w₁ ↔ w₃`, `w₂` fixed; v141/v146/v177). -/
theorem sigma_perm_mu4 :
    sigma 1 = 1 ∧ sigma (-1) = -1 ∧
    sigma Complex.I = -Complex.I ∧ sigma (-Complex.I) = Complex.I := by
  refine ⟨by simp [sigma], by simp [sigma], ?_, ?_⟩
  · simp only [sigma]; exact inv_I'
  · simp only [sigma, inv_neg, inv_I']; ring

/-! ### Multiplier classification (the order-4 elliptic normal form) -/

/-- **Order-4 multiplier classification.** A multiplier Möbius map `z ↦ ζ z` has
order exactly 4 — `ζ⁴ = 1` and `ζ² ≠ 1` — iff `ζ` is a primitive 4th root of
unity, `ζ = i` or `ζ = -i`.  Together with `sigma_rho_sigma` (the inversion
conjugates `i ↦ -i`) this gives the canonical representative `ρ : z ↦ i z`. -/
theorem mult_order_four_iff (ζ : ℂ) :
    (ζ ^ 4 = 1 ∧ ζ ^ 2 ≠ 1) ↔ (ζ = Complex.I ∨ ζ = -Complex.I) := by
  constructor
  · rintro ⟨h4, h2⟩
    have hz : (ζ ^ 2 - 1) * (ζ ^ 2 + 1) = 0 := by linear_combination h4
    rcases mul_eq_zero.mp hz with h | h
    · exact absurd (by linear_combination h : ζ ^ 2 = 1) h2
    · have expand : (ζ - Complex.I) * (ζ + Complex.I) = ζ ^ 2 + 1 := by
        have e : (ζ - Complex.I) * (ζ + Complex.I) = ζ ^ 2 - Complex.I ^ 2 := by ring
        rw [e, Complex.I_sq]; ring
      have key : (ζ - Complex.I) * (ζ + Complex.I) = 0 := by rw [expand]; exact h
      rcases mul_eq_zero.mp key with h' | h'
      · exact Or.inl (sub_eq_zero.mp h')
      · exact Or.inr (add_eq_zero_iff_eq_neg.mp h')
  · rintro (h | h) <;> subst h
    · exact ⟨I_pow_four, by rw [Complex.I_sq]; norm_num⟩
    · refine ⟨?_, ?_⟩
      · have e : (-Complex.I) ^ 4 = Complex.I ^ 4 := by ring
        rw [e, I_pow_four]
      · have e : (-Complex.I) ^ 2 = Complex.I ^ 2 := by ring
        rw [e, Complex.I_sq]; norm_num

/-! ### Bundled normal form (for the signature lock) -/

/-- **`QGEO.UNIFORM.01` normal form, bundled.** The constructive uniformisation
content in one statement: the clock `ρ : z ↦ i z` has order exactly 4, the
reflection `σ : z ↦ 1/z` is an involution satisfying the `D₄` relation
`σρσ = ρ⁻¹` and permuting `μ₄`, a non-fixed orbit scales to `μ₄`, and the
order-4 multipliers are exactly `±i`.  This is the geometric half of the seam
realisation, formalised; the RAW-seam obligation `QGEO.MARKS.01` stays open. -/
theorem uniformisation_normal_form :
    (∀ z : ℂ, rho (rho (rho (rho z))) = z) ∧
    rho (rho 1) ≠ 1 ∧
    (∀ z : ℂ, sigma (sigma z) = z) ∧
    (∀ z : ℂ, sigma (rho (sigma z)) = rhoInv z) ∧
    (∀ ζ : ℂ, (ζ ^ 4 = 1 ∧ ζ ^ 2 ≠ 1) ↔ (ζ = Complex.I ∨ ζ = -Complex.I)) :=
  ⟨rho_pow_four, rho_order_exactly_four, sigma_invol, sigma_rho_sigma, mult_order_four_iff⟩

end TFPT.Carrier.MobiusUniformisation
