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
  `(e_1, e_2, e_3) = (4, 5, 2) = (|mu4|, g_car, |Z2|)`.

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

end TFPT.Carrier.AnchorLadder
