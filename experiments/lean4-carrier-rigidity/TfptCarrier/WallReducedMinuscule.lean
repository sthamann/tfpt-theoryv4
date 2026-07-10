/-
  TFPT — the quark wall cocharacter is minuscule/reduced, kernel-checked
  ================================================================================
  (Lean mirror of the experiment `flav02_wall_bruhat_gonzalez.py` / `flav03`,
   next-step 5, 2026-07-10.)

  The absolute quark holonomy normalisation reduces to selecting the polystable TFPT
  wall point (GATE.UWALL).  González (arXiv:2606.16880) gives: a parabolic G-Higgs
  bundle at a Borel-type fixed point is VERY STABLE iff its weight is REDUCED in the
  affine Bruhat sense, and then the upward flow is a Hitchin SECTION (unique
  selection).  The Python contract shows the TFPT wall splitting type
  `O(-2) ⊕ O(-1)²` (exponents-at-infinity `{2,1,1}` = the anchor `a = (1,1,2)`)
  gives a cocharacter whose A₂ root pairings all lie in `{0, ±1}` — i.e. it is the
  MINUSCULE fundamental coweight `ω₁`, so the divisor is multiplicity-free = REDUCED.

  This file turns that arithmetic into a kernel-checked FACT (no axioms):
  the pairings of the wall cocharacter with the A₂ roots are exactly `{0, ±1}`
  (reduced), its affine length is `2`, and the wobbly controls fail — all by
  `decide`.  Only differences of the splitting degrees enter, so everything is
  integer arithmetic.

  The one thing NOT formalised (it is a cited theorem, not arithmetic): González's
  very-stable ⇔ reduced equivalence, extended to the Φ=0 polystable boundary
  (flav03).  This file certifies only the combinatorial input to that theorem.
-/

import Mathlib.Tactic

namespace TfptCarrier.WallReducedMinuscule

/-- The wall splitting `O(-2) ⊕ O(-1)²` as its exponents-at-infinity, the anchor
    multiset `a = (1,1,2)` written high-to-low.  Only differences matter, so we use
    the integer gap vector directly. -/
def wallDegs : List Int := [2, 1, 1]

/-- A wobbly control splitting `O(-3) ⊕ O(0)²`. -/
def wobblyDegs : List Int := [3, 0, 0]

/-- The A₂ positive-root pairings `⟨λ, α_ij⟩ = d_i − d_j` for `i < j`
    (roots `α₁₂, α₂₃, α₁₃`). -/
def posPairings : List Int → List Int
  | [a, b, c] => [a - b, b - c, a - c]
  | _ => []

/-- All A₂ root pairings: the positive ones together with their negatives. -/
def allPairings (d : List Int) : List Int :=
  posPairings d ++ (posPairings d).map (fun p => -p)

/-- Reduced/minuscule test: every root pairing lies in `{-1, 0, 1}`
    (multiplicity-free divisor). -/
def reducedB (d : List Int) : Bool :=
  (allPairings d).all (fun p => Nat.ble p.natAbs 1)

/-- The affine-Weyl translation length `ℓ(t_λ) = Σ_{α>0} |⟨λ, α⟩|`. -/
def affineLength (d : List Int) : Nat :=
  ((posPairings d).map Int.natAbs).sum

/-! ### The wall cocharacter is reduced/minuscule (kernel-checked, no axioms). -/

/-- The wall pairings with the positive A₂ roots are exactly `{1, 0, 1}`
    (the middle `0` is the stability wall: `λ` is non-regular). -/
theorem wall_pos_pairings : posPairings wallDegs = [1, 0, 1] := by decide

/-- Every root pairing of the wall cocharacter lies in `{-1, 0, 1}` — the divisor is
    MULTIPLICITY-FREE = REDUCED (González's very-stable arithmetic criterion). -/
theorem wall_reduced : reducedB wallDegs = true := by decide

/-- The affine length is `ℓ(t_λ) = 2`. -/
theorem wall_length : affineLength wallDegs = 2 := by decide

/-- The exponents sum to `4 = |μ₄|` (deg E = −4), an anchor consistency check. -/
theorem wall_sum : wallDegs.sum = 4 := by decide

/-! ### Discriminating controls: the wobbly splitting is NOT reduced. -/

/-- The wobbly control `O(-3) ⊕ O(0)²` has a pairing of `3`, so it is NOT reduced —
    the arithmetic criterion genuinely separates reduced (section) from wobbly. -/
theorem wobbly_not_reduced : reducedB wobblyDegs = false := by decide

/-- Its affine length is `6 ≠ 2`, confirming it is a different (wobbly) stratum. -/
theorem wobbly_length : affineLength wobblyDegs = 6 := by decide

/-- The full wall certificate at once: reduced, length 2, anchor sum 4, and the
    wobbly control fails. -/
theorem wall_certificate :
    reducedB wallDegs = true ∧
    affineLength wallDegs = 2 ∧
    wallDegs.sum = 4 ∧
    reducedB wobblyDegs = false :=
  ⟨wall_reduced, wall_length, wall_sum, wobbly_not_reduced⟩

-- The wall reducedness arithmetic depends on NO axioms (pure kernel `decide`);
-- the cited residual (González very-stable ⇔ reduced, extended to the Φ=0
-- polystable boundary, flav03) is NOT an arithmetic fact and is not asserted here.
#print axioms wall_certificate

end TfptCarrier.WallReducedMinuscule
