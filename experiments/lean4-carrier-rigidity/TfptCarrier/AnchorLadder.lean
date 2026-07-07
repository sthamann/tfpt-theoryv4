/-
  TFPT Carrier — Anchor Ladder (power sums of a = (1,1,2))
  ---------------------------------------------------------

  The anchor-first refinement (Paper 1; verification scripts v23, v53,
  v106) reduces the discrete inputs to the single parabolic anchor
  `a = (1,1,2)`.  This module formalises the arithmetic ladder:

      p_n(a) = 1^n + 1^n + 2^n = 2 + 2^n      (for every n),

  hence

      (p_0, p_1, p_2, p_3) = (3, 4, 6, 10)
                           = (N_fam, |mu4|, |R+(A3)|, A_Lambda),
      p_1 * p_2 * p_3      = 240  = |R(E8)|,
      p_4 - p_3            = 8    = rank E8,
      240 + 8              = 248  = dim E8,
      p_{n+1} - p_n        = 2^n              (the binary ladder),

  together with the elementary symmetric values
  `(e_1, e_2, e_3) = (4, 5, 2) = (|mu4|, g_car, |Z2|)`,

  and the CONVERSE (`rankgap_uniqueness`, ANCHOR.RANKGAP.UNIQUENESS):
  among positive integer triples, the single rank-gap equation

      p_4(x) - p_3(x) = 8

  already forces `x = (1,1,2)` up to permutation — the contribution
  `x^3 (x-1)` is `0` at `x = 1`, `8` at `x = 2`, and `>= 54` for
  `x >= 3`, so exactly one entry is `2` and the others are `1`.

  Everything is decidable arithmetic over ℕ; no incomplete proofs and no
  domain axioms — only the standard Lean kernel axioms.
-/

import Mathlib.Tactic

namespace TFPT.Carrier.AnchorLadder

/-- Power sums of the anchor `a = (1,1,2)`. -/
def p (n : ℕ) : ℕ := 1 ^ n + 1 ^ n + 2 ^ n

/-- **Anchor ladder.** `p_n(a) = 2 + 2^n` for every `n`. -/
theorem p_eq (n : ℕ) : p n = 2 + 2 ^ n := by
  simp [p]

/-- The four ladder atoms `(N_fam, |μ₄|, |R⁺(A₃)|, A_Λ) = (3,4,6,10)`. -/
theorem ladder_atoms : p 0 = 3 ∧ p 1 = 4 ∧ p 2 = 6 ∧ p 3 = 10 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide

/-- **E₈ root count.** `p₁ p₂ p₃ = 240 = |R(E₈)|`. -/
theorem root_count : p 1 * p 2 * p 3 = 240 := by decide

/-- **E₈ rank.** `p₄ − p₃ = 8 = rank E₈`. -/
theorem rank_step : p 4 - p 3 = 8 := by decide

/-- **E₈ dimension.** `p₁ p₂ p₃ + (p₄ − p₃) = 248 = dim E₈`. -/
theorem dim_e8 : p 1 * p 2 * p 3 + (p 4 - p 3) = 248 := by decide

/-- **Binary ladder.** `p_{n+1} − p_n = 2^n` for every `n`. -/
theorem binary_ladder (n : ℕ) : p (n + 1) - p n = 2 ^ n := by
  rw [p_eq, p_eq, pow_succ]
  omega

/-- Elementary symmetric values of the anchor:
`(e₁, e₂, e₃) = (1+1+2, 1·1+1·2+1·2, 1·1·2) = (4, 5, 2)
= (|μ₄|, g_car, |Z₂|)`. -/
theorem elementary_symmetric :
    (1 + 1 + 2 = 4) ∧ (1 * 1 + 1 * 2 + 1 * 2 = 5) ∧ (1 * 1 * 2 = 2) := by
  decide

/-! ### The rank-gap converse (ANCHOR.RANKGAP.UNIQUENESS)

`rank_step` above reads the value `p₄ − p₃ = 8` *off* the anchor.
The converse below shows the equation *selects* the anchor: among all
positive integer triples, `p₄(x) − p₃(x) = 8 = rank E₈` holds only for
permutations of `(1,1,2)`.  Scope note: this forces the anchor within
positive integer triples of length 3; that the anchor is such a triple,
and that the rank gap is the right normalisation, remain the axiom-side
inputs (Paper 1). -/

/-- Any entry `x ≥ 3` alone overshoots the rank gap:
`x³(x−1) ≥ 54 > 8`. -/
theorem cube_step_ge_54 (x : ℕ) (hx : 3 ≤ x) : 54 ≤ x ^ 3 * (x - 1) := by
  calc 54 = 3 ^ 3 * (3 - 1) := by norm_num
  _ ≤ x ^ 3 * (x - 1) :=
      Nat.mul_le_mul (Nat.pow_le_pow_left hx 3) (by omega)

/-- Any entry `w ≥ 3` overshoots the whole gap even before subtracting:
`w³ + 54 ≤ w⁴`. -/
theorem overshoot_ge_three (w : ℕ) (hw : 3 ≤ w) : w ^ 3 + 54 ≤ w ^ 4 := by
  have h27 : (27 : ℕ) ≤ w ^ 3 :=
    calc (27 : ℕ) = 3 ^ 3 := by norm_num
    _ ≤ w ^ 3 := Nat.pow_le_pow_left hw 3
  calc w ^ 3 + 54 ≤ w ^ 3 + 2 * w ^ 3 :=
        Nat.add_le_add_left
          (calc (54 : ℕ) = 2 * 27 := by norm_num
           _ ≤ 2 * w ^ 3 := Nat.mul_le_mul (Nat.le_refl 2) h27) _
  _ = 3 * w ^ 3 := by ring
  _ ≤ w * w ^ 3 := Nat.mul_le_mul hw (Nat.le_refl _)
  _ = w ^ 4 := by ring

/-- **Rank-gap uniqueness (ANCHOR.RANKGAP.UNIQUENESS).**
A positive integer triple with `p₄(x) − p₃(x) = 8` (stated
subtraction-free as `p₄ = p₃ + 8`) is `(1,1,2)` up to permutation. -/
theorem rankgap_uniqueness (x y z : ℕ)
    (hx : 1 ≤ x) (hy : 1 ≤ y) (hz : 1 ≤ z)
    (h : x ^ 4 + y ^ 4 + z ^ 4 = x ^ 3 + y ^ 3 + z ^ 3 + 8) :
    (x = 1 ∧ y = 1 ∧ z = 2) ∨ (x = 1 ∧ y = 2 ∧ z = 1) ∨
    (x = 2 ∧ y = 1 ∧ z = 1) := by
  -- each entry is ≤ 2: an entry ≥ 3 contributes ≥ 54 > 8 to the gap,
  -- while every entry w ≥ 1 has w³ ≤ w⁴, so nothing can compensate
  have cube_le_pow4 : ∀ w : ℕ, 1 ≤ w → w ^ 3 ≤ w ^ 4 := fun w hw =>
    Nat.pow_le_pow_right hw (by norm_num)
  have hxb : x ≤ 2 := by
    by_contra hgt
    have h1 := overshoot_ge_three x (by omega)
    have h2 := cube_le_pow4 y hy
    have h3 := cube_le_pow4 z hz
    linarith
  have hyb : y ≤ 2 := by
    by_contra hgt
    have h1 := overshoot_ge_three y (by omega)
    have h2 := cube_le_pow4 x hx
    have h3 := cube_le_pow4 z hz
    linarith
  have hzb : z ≤ 2 := by
    by_contra hgt
    have h1 := overshoot_ge_three z (by omega)
    have h2 := cube_le_pow4 x hx
    have h3 := cube_le_pow4 y hy
    linarith
  -- finite check on {1,2}³
  revert h
  interval_cases x <;> interval_cases y <;> interval_cases z <;> decide

/-- The anchor satisfies the rank-gap equation (soundness companion of
`rankgap_uniqueness`; matches `rank_step`). -/
theorem rankgap_anchor :
    1 ^ 4 + 1 ^ 4 + 2 ^ 4 = 1 ^ 3 + 1 ^ 3 + 2 ^ 3 + 8 := by
  decide

end TFPT.Carrier.AnchorLadder
