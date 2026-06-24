/-
  TFPT Carrier — Spectral-Gap Attractor (the scalar core of v383)
  ----------------------------------------------------------------

  Door #4: a SCOPED, fully-proved Lean formalisation of the universal
  spectral-gap meta-theorem (verification scripts v303, v383, v387):

      a gapped operator  ⇒  a unique attractor (the physics)
                         ⇒  geometric convergence at the gap rate
                         ⇒  parameter-freeness (the start is forgotten).

  HONEST SCOPE.  This formalises the SCALAR / one-dimensional reduction —
  the affine contraction `x ↦ x* + r·(x − x*)` whose multiplier `r = λ₂/λ₁`
  is the spectral-gap ratio that v303/v383 iterate numerically.  The full
  multi-dimensional Perron–Frobenius statement (a primitive nonnegative
  operator has a unique dominant eigenvector) stays the cited theorem; this
  module proves the contraction CORE on which the meta-theorem rests, with
  no `sorry` and only the standard Lean kernel axioms.

  Results:

    iter_sub          — closed form: `iterₙ − x* = rⁿ · (x₀ − x*)`.
    iter_tendsto      — `0 ≤ r < 1` (the gap) ⇒ `iterₙ → x*` (the attractor).
    starts_agree      — two starts differ by `rⁿ·(a−b) → 0`: the attractor is
                        UNIQUE / independent of the initial state (= parameter-free).
    no_gap_no_forget  — `r = 1` (no gap) ⇒ `iterₙ − x* = x₀ − x*` is CONSTANT:
                        without a gap the initial condition is a free parameter.
    seam_rate_lt_one  — the seam rate `(2/3)⁶` (prime-3 / family facet) is in `[0,1)`.
    golden_rate_lt_one— the compiler rate `(φ+2)/4 = (5+√5)/8` (prime-5 / carrier
                        facet) is in `[0,1)`.

  See verification/v383_dynamics_universal.py and v387_corrections_gap.py.
-/

import Mathlib.Tactic
import Mathlib.Analysis.SpecificLimits.Basic

namespace TFPT.Carrier.SpectralGapAttractor

open Filter

/-- The affine gap contraction `x ↦ x* + r·(x − x*)`, iterated from `x₀`.
`r = λ₂/λ₁` is the spectral-gap ratio. -/
def iter (r xstar x0 : ℝ) : ℕ → ℝ
  | 0     => x0
  | n + 1 => xstar + r * (iter r xstar x0 n - xstar)

/-- **Closed form.** The deviation from the attractor decays as `rⁿ`:
`iterₙ − x* = rⁿ · (x₀ − x*)`. -/
theorem iter_sub (r xstar x0 : ℝ) (n : ℕ) :
    iter r xstar x0 n - xstar = r ^ n * (x0 - xstar) := by
  induction n with
  | zero => simp [iter]
  | succ k ih =>
      have hunfold : iter r xstar x0 (k + 1) = xstar + r * (iter r xstar x0 k - xstar) := by
        simp only [iter]
      rw [hunfold, pow_succ]
      linear_combination r * ih

/-- **The gap gives a unique attractor.** With a spectral gap `0 ≤ r < 1`, the
iteration converges to `x*` from any start — the physics is the dominant mode. -/
theorem iter_tendsto (r xstar x0 : ℝ) (hr0 : 0 ≤ r) (hr1 : r < 1) :
    Tendsto (iter r xstar x0) atTop (nhds xstar) := by
  have hpow : Tendsto (fun n : ℕ => r ^ n) atTop (nhds 0) :=
    tendsto_pow_atTop_nhds_zero_of_lt_one hr0 hr1
  have hdev : Tendsto (fun n : ℕ => r ^ n * (x0 - xstar)) atTop (nhds 0) := by
    simpa using hpow.mul_const (x0 - xstar)
  have hconst : Tendsto (fun _ : ℕ => xstar) atTop (nhds xstar) := tendsto_const_nhds
  have hsum : Tendsto (fun n : ℕ => xstar + r ^ n * (x0 - xstar)) atTop (nhds xstar) := by
    simpa using hconst.add hdev
  refine hsum.congr (fun n => ?_)
  have := iter_sub r xstar x0 n
  linarith

/-- **Parameter-freeness.** Two different initial states `a`, `b` stay within
`rⁿ·(a − b)`, which tends to `0`: the attractor is independent of the start, so
no free parameter survives. -/
theorem starts_agree (r xstar a b : ℝ) (n : ℕ) :
    iter r xstar a n - iter r xstar b n = r ^ n * (a - b) := by
  have ha := iter_sub r xstar a n
  have hb := iter_sub r xstar b n
  have h : iter r xstar a n - iter r xstar b n
      = r ^ n * (a - xstar) - r ^ n * (b - xstar) := by linarith
  rw [h]; ring

/-- **No gap, no forgetting.** If `r = 1` (the gap closes) the deviation is
constant: `iterₙ − x* = x₀ − x*` for all `n`, so the initial condition is
remembered forever — i.e. it is a free parameter.  The gap `r < 1` is exactly
what removes it. -/
theorem no_gap_no_forget (xstar x0 : ℝ) (n : ℕ) :
    iter 1 xstar x0 n - xstar = x0 - xstar := by
  rw [iter_sub]; simp

/-- The seam rate `(2/3)⁶` (the prime-3 / family-dynamic facet, v387) lies in
`[0,1)`, so the seam-gapped sectors contract to their attractor. -/
theorem seam_rate_lt_one : (0 : ℝ) ≤ (2 / 3) ^ 6 ∧ ((2 / 3 : ℝ)) ^ 6 < 1 := by
  constructor <;> norm_num

/-- The discrete-compiler rate `(φ+2)/4 = (5+√5)/8` (the prime-5 / carrier-static
facet, v387) lies in `[0,1)`. -/
theorem golden_rate_lt_one : (0 : ℝ) ≤ (5 + Real.sqrt 5) / 8 ∧ (5 + Real.sqrt 5) / 8 < 1 := by
  have hlt : Real.sqrt 5 < 3 := by
    have h9 : Real.sqrt 9 = 3 := by
      rw [show (9 : ℝ) = 3 ^ 2 by norm_num, Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ 3)]
    calc Real.sqrt 5 < Real.sqrt 9 := Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
      _ = 3 := h9
  refine ⟨by positivity, ?_⟩
  rw [div_lt_one (by norm_num : (0 : ℝ) < 8)]
  linarith [hlt]

end TFPT.Carrier.SpectralGapAttractor
