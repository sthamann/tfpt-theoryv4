/-
  TFPT Carrier — Pascal Ladder (the closure solutions are g = 2K+1)
  ------------------------------------------------------------------

  The Pascal Ladder Theorem (verification script v108) states that the
  carrier closure condition

      2^(g-1) = C(g,0) + C(g,1) + ... + C(g,K)

  has, for every truncation degree `K`, exactly the solution `g = 2K+1`:
  the carrier selection `g = 5` is therefore *equivalent* to the degree
  bound `K = 2` (the Quadratic-Boundary-Locality reduction of red-team
  Target B).

  This module formalises:

    * `ladder_solves`   — the odd-`g` midpoint identity: `g = 2K+1`
                          always solves the closure (from Mathlib's
                          `Nat.sum_range_choose_halfway`);
    * `ladder_unique_K2`— bounded uniqueness for the carrier case
                          `K = 2`: on `1 ≤ g ≤ 40` the closure holds iff
                          `g = 5` (kernel-decidable finite check);
    * the neighbour-world data `K = 1 → (g,N_fam) = (3,1)` and
      `K = 3 → (7,9)`, and the rank-8 overdetermination
      `g + N_fam = 8` holding at `g = 5` alone among the low ladder.

  No incomplete proofs and no domain axioms — only the standard Lean
  kernel axioms.
-/

import Mathlib.Tactic
import Mathlib.Data.Nat.Choose.Sum

namespace TFPT.Carrier.PascalLadder

open Finset

/-- Truncated Pascal sum `Σ_{k ≤ K} C(g,k)`. -/
def pascalSum (g K : ℕ) : ℕ := ∑ k ∈ range (K + 1), g.choose k

/--
**Ladder identity (odd midpoint).** For every `K`, the odd rank
`g = 2K+1` solves the closure: `Σ_{k ≤ K} C(2K+1, k) = 2^(2K) = 2^(g-1)`.
This is the binomial midpoint identity, `Nat.sum_range_choose_halfway`.
-/
theorem ladder_solves (K : ℕ) : pascalSum (2 * K + 1) K = 2 ^ (2 * K) := by
  have h := Nat.sum_range_choose_halfway K
  simpa [pascalSum, Nat.pow_mul] using h

/--
**Carrier case, bounded uniqueness.** On the window `1 ≤ g ≤ 40` the
`K = 2` closure `2^(g-1) = 1 + g + C(g,2)` holds iff `g = 5`.
(Kernel-decidable finite check; the unbounded uniqueness follows from the
growth lemma of `CarrierRankUniqueness` for the division-free form.)
-/
theorem ladder_unique_K2 :
    ∀ g : ℕ, 1 ≤ g → g ≤ 40 → (2 ^ (g - 1) = pascalSum g 2 ↔ g = 5) := by
  decide

/-- The carrier world: `K = 2` gives `g = 5`, code `2^4 = 16`,
`N_fam = (16-1)/5 = 3`, and the rank closure `g + N_fam = 8`. -/
theorem carrier_world :
    2 * 2 + 1 = 5 ∧ 2 ^ 4 = 16 ∧ (2 ^ 4 - 1) / 5 = 3 ∧ 5 + 3 = 8 := by
  decide

/-- Neighbour worlds: `K = 1` is a one-family world `(g, N_fam) = (3, 1)`;
`K = 3` is a nine-family world `(7, 9)`; `K = 4` is inconsistent
(`9 ∤ 2^8 - 1`). Only the carrier world satisfies `g + N_fam = 8`. -/
theorem neighbour_worlds :
    ((2 ^ 2 - 1) / 3 = 1 ∧ 3 + 1 ≠ 8) ∧
    ((2 ^ 6 - 1) / 7 = 9 ∧ 7 + 9 ≠ 8) ∧
    ¬ (9 ∣ 2 ^ 8 - 1) := by
  decide

end TFPT.Carrier.PascalLadder
