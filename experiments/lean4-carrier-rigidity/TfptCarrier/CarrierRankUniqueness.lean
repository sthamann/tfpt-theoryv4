/-
  TFPT Carrier — Carrier Rank Uniqueness (Theorem A, lattice core)
  ----------------------------------------------------------------

  The Selection / Bootstrap statement of TFPT (Papers 1, 3; verification
  scripts v6, v14, v47) singles out the carrier rank `g_car = 5` from the
  Pascal carrier condition

      2^(g-1) = C(g,0) + C(g,1) + C(g,2)   (the half-spinor exhaustion),

  which, after clearing the binomial division by `2`, is the integer
  (division-free) equation

      2^g = g^2 + g + 2.

  This module proves the **uniqueness** part of Theorem A rigorously:

      ∀ g : ℕ,  2^g = g^2 + g + 2  ↔  g = 5.

  The forward direction is the genuine content: every solution is `5`.
  It splits into a finite check `g ≤ 5` (`interval_cases`) and an
  exponential-vs-quadratic growth lemma for `g ≥ 6`.

  Two carrier corollaries are recorded: `g_car = 5` is the unique solution,
  and the family/closure integers `N_fam = (2^(g-1)-1)/g = 3`, `g + N_fam =
  rank E₈ = 8` follow by computation.

  No incomplete proofs and no domain axioms: only the standard Lean kernel axioms.
-/

import Mathlib.Tactic

namespace TFPT.Carrier.CarrierRankUniqueness

/--
**Growth lemma.** For `g ≥ 6` the quadratic carrier count is strictly
below the half-spinor exhaustion `2^g`. Proved by induction from `g = 6`:
the right side doubles each step while the left side grows only
quadratically (`n ≤ n²` carries the step).
-/
theorem pascal_growth : ∀ g : ℕ, 6 ≤ g → g ^ 2 + g + 2 < 2 ^ g := by
  intro g hg
  induction g, hg using Nat.le_induction with
  | base => decide
  | succ n hn ih =>
      have hnn : n ≤ n ^ 2 := by nlinarith [hn]
      have hexp : (n + 1) ^ 2 + (n + 1) + 2 = (n ^ 2 + n + 2) + (2 * n + 2) := by ring
      have hpow : 2 ^ (n + 1) = 2 * 2 ^ n := by rw [pow_succ]; ring
      calc (n + 1) ^ 2 + (n + 1) + 2
          = (n ^ 2 + n + 2) + (2 * n + 2) := hexp
        _ ≤ 2 * (n ^ 2 + n + 2) := by omega
        _ < 2 * 2 ^ n := by omega
        _ = 2 ^ (n + 1) := hpow.symm

/--
**Theorem A (lattice core).** The carrier-rank Pascal condition
`2^g = g^2 + g + 2` has the \emph{unique} solution `g = 5`.
-/
theorem carrier_rank_pascal_unique (g : ℕ) :
    2 ^ g = g ^ 2 + g + 2 ↔ g = 5 := by
  constructor
  · intro h
    by_contra hne
    rcases Nat.lt_or_ge g 6 with hlt | hge
    · interval_cases g
      all_goals first | exact absurd h (by decide) | exact hne rfl
    · have hgrow := pascal_growth g hge
      omega
  · intro h; subst h; decide

/--
**Carrier corollary.** `g_car = 5` is the unique carrier rank, and it is a
genuine solution.
-/
theorem g_car_unique : (∃! g : ℕ, 2 ^ g = g ^ 2 + g + 2) := by
  refine ⟨5, by decide, ?_⟩
  intro g hg
  exact (carrier_rank_pascal_unique g).mp hg

/--
**Closure integers.** From `g_car = 5` the family count and the `E₈` rank
follow by computation: `N_fam = (2^(g-1) - 1)/g = 3` and
`g_car + N_fam = rank E₈ = 8`.
-/
theorem carrier_closure_integers :
    (2 ^ (5 - 1) - 1) / 5 = 3 ∧ 5 + 3 = 8 := by decide

end TFPT.Carrier.CarrierRankUniqueness
