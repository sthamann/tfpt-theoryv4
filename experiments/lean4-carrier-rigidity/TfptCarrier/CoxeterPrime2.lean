/-
  TFPT Carrier — Coxeter prime-2 structural lemma (v409 / RES.COXETER.SYMMETRY.01)
  --------------------------------------------------------------------------------

  Door: a fully-proved Lean formalisation of the falsifiable corollary of
  RES.COXETER.SYMMETRY.01 (verification script v409_coxeter_prime2_lemma.py):

      prime-2 (the seam sheet involution) is NECESSARY but NOT autonomous --
      there is NO prime-2-only attractor.

  THE ARGUMENT (machine-checked here).  A genuine dynamical attractor needs a
  CONTRACTION RATE `r` strictly inside the unit interval, `0 < r < 1` (so that
  `rⁿ → 0`, the gap-contraction core of `SpectralGapAttractor`).  But the
  spectrum of the prime-2 generator carries no such rate:

    * the sheet INVOLUTION `σ` (with `σ² = 1`, the |Z₂| = 2 generator) has
      eigenvalues in `{+1, -1}` (parity), and
    * its spectral PROJECTOR `(1 ± σ)/2` (idempotent) has eigenvalues in
      `{0, 1}` (projection),

  and none of `{-1, 0, 1}` lies in `(0,1)`.  Meanwhile the genuine seam family
  rate `2/3 = |Z₂|/N_fam` DOES lie in `(0,1)` (and `(2/3)⁶`, the recovery gap,
  is already `seam_rate_lt_one` in `SpectralGapAttractor`).  Hence prime-2
  supplies a parity / a projection, never a nonzero universal contraction rate:
  it is necessary (admissible boundary transport is sheet-paired) but cannot, by
  itself, drive an attractor.  Dynamics begins only after coupling to family
  prime-3 or carrier prime-5.

  This upgrades the v409 Python check to a Lean theorem (FORM.COXETER.PRIME2.01),
  closing the corollary at the machine-proof tier.  It reuses the gap-contraction
  core of `SpectralGapAttractor` for the dynamical reading: a parity eigenvalue
  `r = 1` REMEMBERS the start (no attractor), while `r = 2/3` CONVERGES.
-/

import Mathlib.Tactic
import TfptCarrier.SpectralGapAttractor

namespace TFPT.Carrier.CoxeterPrime2

open TFPT.Carrier.SpectralGapAttractor

/-- A genuine dynamical contraction rate: strictly inside the open unit
interval `(0,1)`, so that `rⁿ → 0` drives convergence to a nonzero attractor. -/
def IsContractionRate (r : ℝ) : Prop := 0 < r ∧ r < 1

/-- **Involution eigenvalues are `±1`.** Any root of `r² = 1` is `1` or `-1`. -/
theorem involution_eigenvalue {r : ℝ} (hr : r * r = 1) : r = 1 ∨ r = -1 := by
  have h : (r - 1) * (r + 1) = 0 := by
    have hexp : (r - 1) * (r + 1) = r * r - 1 := by ring
    rw [hexp, hr]; ring
  rcases mul_eq_zero.mp h with h1 | h2
  · exact Or.inl (by linear_combination h1)
  · exact Or.inr (by linear_combination h2)

/-- **Idempotent (projector) eigenvalues are `0` or `1`.** Any root of `r² = r`
is `0` or `1`. -/
theorem idempotent_eigenvalue {r : ℝ} (hr : r * r = r) : r = 0 ∨ r = 1 := by
  have h : r * (r - 1) = 0 := by
    have hexp : r * (r - 1) = r * r - r := by ring
    rw [hexp, hr]; ring
  rcases mul_eq_zero.mp h with h0 | h1
  · exact Or.inl h0
  · exact Or.inr (by linear_combination h1)

/-- **An involution eigenvalue is never a contraction rate.** `±1 ∉ (0,1)`. -/
theorem involution_not_contraction {r : ℝ} (hr : r * r = 1) :
    ¬ IsContractionRate r := by
  rintro ⟨hpos, hlt⟩
  rcases involution_eigenvalue hr with h | h
  · rw [h] at hlt; exact lt_irrefl (1 : ℝ) hlt
  · rw [h] at hpos; exact absurd hpos (by norm_num)

/-- **A projector eigenvalue is never a contraction rate.** `{0,1} ∩ (0,1) = ∅`. -/
theorem idempotent_not_contraction {r : ℝ} (hr : r * r = r) :
    ¬ IsContractionRate r := by
  rintro ⟨hpos, hlt⟩
  rcases idempotent_eigenvalue hr with h | h
  · rw [h] at hpos; exact lt_irrefl (0 : ℝ) hpos
  · rw [h] at hlt; exact lt_irrefl (1 : ℝ) hlt

/-- **The seam family rate `2/3 = |Z₂|/N_fam` IS a contraction rate.** -/
theorem seam_rate_is_contraction : IsContractionRate ((2 : ℝ) / 3) :=
  ⟨by norm_num, by norm_num⟩

/-- The concrete sheet-involution eigenvalues `{+1, -1}` (the distinct entries of
`σ = diag(1,-1,-1)`, v409) are each not a contraction rate. -/
theorem sheet_eigenvalues_not_contraction :
    (¬ IsContractionRate (1 : ℝ)) ∧ (¬ IsContractionRate (-1 : ℝ)) :=
  ⟨involution_not_contraction (by norm_num),
   involution_not_contraction (by norm_num)⟩

/-- The concrete sheet-projector eigenvalues `{0, 1}` are each not a contraction
rate. -/
theorem projector_eigenvalues_not_contraction :
    (¬ IsContractionRate (0 : ℝ)) ∧ (¬ IsContractionRate (1 : ℝ)) :=
  ⟨idempotent_not_contraction (by norm_num),
   idempotent_not_contraction (by norm_num)⟩

/--
**RES.COXETER.SYMMETRY.01 — the falsifiable corollary, machine-proved.**

No prime-2-only attractor exists: every involution eigenvalue (`r² = 1`) and
every projector eigenvalue (`r² = r`) fails to be a contraction rate, while the
genuine seam family rate `2/3` is one. So prime-2 supplies parity / projection,
never a nonzero universal contraction rate.
-/
theorem no_prime2_only_attractor :
    (∀ r : ℝ, r * r = 1 → ¬ IsContractionRate r) ∧
    (∀ r : ℝ, r * r = r → ¬ IsContractionRate r) ∧
    IsContractionRate ((2 : ℝ) / 3) :=
  ⟨fun _ h => involution_not_contraction h,
   fun _ h => idempotent_not_contraction h,
   seam_rate_is_contraction⟩

/-- **Dynamical reading (necessary, not autonomous), via the gap-contraction
core.** At the parity eigenvalue `r = 1` the iteration REMEMBERS the start
(`iterₙ − x* = x₀ − x*` for all `n`): prime-2 alone drives no attractor. -/
theorem parity_eigenvalue_remembers_start (xstar x0 : ℝ) (n : ℕ) :
    iter 1 xstar x0 n - xstar = x0 - xstar :=
  no_gap_no_forget xstar x0 n

/-- **Dynamical reading (the genuine rate converges).** At the seam family rate
`r = 2/3 ∈ (0,1)` the iteration CONVERGES to the attractor `x*` from any start —
the contraction that prime-2 alone cannot supply, recovered once coupled to the
family `3`. -/
theorem seam_rate_has_attractor (xstar x0 : ℝ) :
    Filter.Tendsto (iter (2 / 3) xstar x0) Filter.atTop (nhds xstar) :=
  iter_tendsto (2 / 3) xstar x0 (by norm_num) (by norm_num)

end TFPT.Carrier.CoxeterPrime2
