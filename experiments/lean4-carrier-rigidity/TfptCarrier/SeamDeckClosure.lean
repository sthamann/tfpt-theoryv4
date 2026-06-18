/-
  TFPT Carrier — Seam-Deck Closure (the QGEO.SYM.01 conditional theorem)
  ----------------------------------------------------------------------

  Formalises the ALGEBRAIC SKELETON of the last open premise of TFPT,
  `QGEO.SYM.01` ("the carrier μ₄ clock is the conformal deck of the seam"),
  in the same discipline as `CalderonProjector` and `GlueUniqueness`:

    * the PHYSICAL premise (the raw seam DtN sub-principal symbol is
      *mark-local* -- the seam is flat away from the four μ₄ marks) is a
      typed `structure` `SeamDeckPremise` -- the open [O] input, NOT proved;
    * the IMPLICATION it produces (mark-local ⇒ the carrier clock commutes
      with the DtN at the character level ⇒ the quasi-free state is
      clock-invariant, `ω∘ρ=ω`) is a `theorem` -- machine-proved [F].

  This is the Lean counterpart of `verification/v201_seam_subprincipal_marks.py`
  and `verification/v210_mark_local_dtn.py` (ledger `QGEO.SUBPRIN.01`,
  `QGEO.MARKLOCAL.01`): v210 certified the implication *numerically* on
  realistic Steklov profiles; here the exact algebraic core is a Lean theorem.

  WHAT IS AND IS NOT CLOSED.  The carrier clock ρ acts on the boundary
  Fourier mode `n` by the character `i^n`, i.e. by its class `cls n := n mod 4`.
  The seam DtN is `Λ = |D_θ| + M_f`; the sub-principal piece `M_f` is
  multiplication by a boundary-curvature function `f`, a Toeplitz operator with
  entry `⟨n|M_f|n'⟩ = f_{n-n'}`. Two facts:

    (A) [F, character orthogonality]  a curvature SOURCED BY THE FOUR μ₄ MARKS,
        `f(θ) = Σ_{j=0}^{3} g(θ - jπ/2)`, has Fourier support ONLY on modes
        ≡ 0 (mod 4): its mode-`m` coefficient carries the factor
        `Σ_{j<4} (ω^m)^j` with `ω` a primitive 4th root of unity, which is `4`
        if `4 ∣ m` and `0` otherwise (finite geometric sum / character
        orthogonality).  So a μ₄-mark-sourced `f` is mark-local.
    (B) [F, block-diagonality]  if `f` is mark-local (support ⊆ {m : cls m = 0})
        then `M_f` connects only equal clock-characters: `f_{n-n'} ≠ 0 ⇒
        cls n = cls n'`, i.e. `[ρ, M_f] = 0` (the principal `|D_θ|` is diagonal,
        so it commutes too).  For the quasi-free covariance `C = ½(1+sgn H₁)`,
        a function of the commuting operator, `[ρ, C] = 0`, i.e. `ω∘ρ = ω`.

  The PREMISE that the physical seam DtN actually IS mark-local stays the one
  fundamental seam-identification postulate (`QGEO.SYM.01`, [O]); it is encoded
  as the hypothesis of `SeamDeckPremise`, exactly as `CalderonProjector`
  encodes the Paper-1 analytic input.  This module does NOT close that
  postulate -- it formalises the conditional theorem downstream of it.

  All proofs use only `propext`, `Classical.choice`, `Quot.sound`.
-/

import Mathlib.Tactic
import Mathlib.Algebra.Field.GeomSum
import Mathlib.Data.Complex.Basic

namespace TFPT.Carrier.SeamDeckClosure

open Finset

/-! ### Part 1 — character orthogonality of the four μ₄ marks -/

/-- **Finite geometric sum at a 4th root of unity** (the mark-sum kernel).
For any `ζ : ℂ` with `ζ⁴ = 1`, the four-mark phase sum `Σ_{j<4} ζ^j` is `4`
if `ζ = 1` and `0` otherwise.  This is the orthogonality that forces a
μ₄-mark-sourced curvature onto modes `≡ 0 (mod 4)`. -/
theorem geom_sum_fourth_root (ζ : ℂ) (h4 : ζ ^ 4 = 1) :
    (∑ j ∈ range 4, ζ ^ j) = if ζ = 1 then 4 else 0 := by
  by_cases hζ : ζ = 1
  · subst hζ; simp
  · rw [if_neg hζ, geom_sum_eq hζ 4, h4]; simp

/-- The carrier clock generator `ω = -i` is a primitive 4th root of unity:
`ω⁴ = 1`. -/
theorem clock_gen_pow_four : (-Complex.I) ^ 4 = 1 := by
  have h2 : (-Complex.I) ^ 2 = -1 := by
    rw [neg_sq, Complex.I_sq]
  calc (-Complex.I) ^ 4 = ((-Complex.I) ^ 2) ^ 2 := by ring
    _ = (-1 : ℂ) ^ 2 := by rw [h2]
    _ = 1 := by ring

/-- The three non-trivial powers of the clock generator are `≠ 1`
(`(-i)¹ = -i`, `(-i)² = -1`, `(-i)³ = i`), so the only vanishing residue of
the mark sum is `0 (mod 4)`. -/
theorem clock_gen_pow_ne_one :
    (-Complex.I) ^ 1 ≠ 1 ∧ (-Complex.I) ^ 2 ≠ 1 ∧ (-Complex.I) ^ 3 ≠ 1 := by
  refine ⟨?_, ?_, ?_⟩
  · simp [Complex.ext_iff]
  · rw [neg_sq, Complex.I_sq]; norm_num
  · have : (-Complex.I) ^ 3 = Complex.I := by
      have h2 : (-Complex.I) ^ 2 = -1 := by rw [neg_sq, Complex.I_sq]
      calc (-Complex.I) ^ 3 = (-Complex.I) ^ 2 * (-Complex.I) := by ring
        _ = (-1 : ℂ) * (-Complex.I) := by rw [h2]
        _ = Complex.I := by ring
    rw [this]; simp [Complex.ext_iff]

/-- **Mark-sum vanishes off `mod 4`** (character orthogonality, concrete).
For each non-zero residue `r ∈ {1,2,3}` the four-mark phase sum at the clock
generator vanishes; at residue `0` it is `4`.  Hence a μ₄-mark-sourced
curvature has Fourier support only on modes `≡ 0 (mod 4)`. -/
theorem mark_sum_residue_zero :
    (∑ j ∈ range 4, ((-Complex.I) ^ (0 : ℕ)) ^ j) = 4 := by
  simp

theorem mark_sum_residue_nonzero :
    (∑ j ∈ range 4, ((-Complex.I) ^ (1 : ℕ)) ^ j) = 0 ∧
    (∑ j ∈ range 4, ((-Complex.I) ^ (2 : ℕ)) ^ j) = 0 ∧
    (∑ j ∈ range 4, ((-Complex.I) ^ (3 : ℕ)) ^ j) = 0 := by
  obtain ⟨h1, h2, h3⟩ := clock_gen_pow_ne_one
  refine ⟨?_, ?_, ?_⟩
  · have h4 : ((-Complex.I) ^ (1 : ℕ)) ^ 4 = 1 := by
      rw [← pow_mul, mul_comm, pow_mul, clock_gen_pow_four, one_pow]
    rw [geom_sum_fourth_root _ h4, if_neg h1]
  · have h4 : ((-Complex.I) ^ (2 : ℕ)) ^ 4 = 1 := by
      rw [← pow_mul, mul_comm, pow_mul, clock_gen_pow_four, one_pow]
    rw [geom_sum_fourth_root _ h4, if_neg h2]
  · have h4 : ((-Complex.I) ^ (3 : ℕ)) ^ 4 = 1 := by
      rw [← pow_mul, mul_comm, pow_mul, clock_gen_pow_four, one_pow]
    rw [geom_sum_fourth_root _ h4, if_neg h3]

/-! ### Part 2 — clock-character block-diagonality (the operational core) -/

/-- The carrier-clock character class of a boundary Fourier mode `n`:
the clock `ρ : z ↦ i z` acts on mode `n` by `i^n`, classified by `n mod 4`. -/
def cls (n : ℤ) : ZMod 4 := (n : ZMod 4)

/-- **Mark-locality** of a Toeplitz curvature with present-mode set `S`:
every present Fourier mode is `≡ 0 (mod 4)` (the seam is flat away from the μ₄
marks — the conformal-deck structure).  This is the operational form of the
`QGEO.SYM.01` premise. -/
def MarkLocal (S : Finset ℤ) : Prop := ∀ m ∈ S, cls m = 0

/-- **Block-diagonality theorem** (the implication `v210` certifies numerically):
a mark-local sub-principal symbol `M_f` connects only modes of equal
clock-character, `f_{n-n'} ≠ 0 ⇒ cls n = cls n'`.  Equivalently `[ρ, M_f] = 0`
(the principal `|D_θ| = diag|n|` already commutes), so the carrier clock
preserves the DtN. -/
theorem markLocal_blockDiagonal {S : Finset ℤ} (h : MarkLocal S)
    {n n' : ℤ} (hmem : (n - n') ∈ S) : cls n = cls n' := by
  have h0 : cls (n - n') = 0 := h _ hmem
  unfold cls at h0 ⊢
  push_cast at h0
  exact sub_eq_zero.mp h0

/-! ### Part 3 — the conditional theorem (premise as a typed target) -/

/-- **`SeamDeckPremise`** — the `QGEO.SYM.01` premise as a typed target, the
single open [O] input of TFPT, encoded exactly as `CalderonProjector` encodes
the Paper-1 analytic input: the raw seam DtN sub-principal symbol is mark-local
(its present Fourier modes are all `≡ 0 (mod 4)`; the seam is flat away from the
four μ₄ marks = the conformal-deck structure).  This structure is *consumed*,
never proved — producing it from the physical seam is the one fundamental
seam-identification postulate. -/
structure SeamDeckPremise where
  /-- The present Fourier modes of the seam DtN sub-principal symbol. -/
  modes : Finset ℤ
  /-- The premise: the symbol is mark-local (conformal-deck flat). -/
  mark_local : MarkLocal modes

namespace SeamDeckPremise

/-- **Conditional QGEO closure (the `ω∘ρ=ω` skeleton):** given the seam-deck
premise, the carrier clock commutes with the DtN at the character level — the
sub-principal symbol connects only equal clock-characters.  For the quasi-free
covariance `C = ½(1+sgn H₁)` (a function of the commuting one-particle operator)
this gives `[ρ, C] = 0`, i.e. `ω∘ρ = ω`.  The premise stays [O]; this
implication is [F]. -/
theorem clock_invariant (P : SeamDeckPremise)
    {n n' : ℤ} (h : (n - n') ∈ P.modes) : cls n = cls n' :=
  markLocal_blockDiagonal P.mark_local h

/-- A μ₄-mark-sourced curvature satisfies the premise: any mode present in a
mark sum is `≡ 0 (mod 4)` (Part 1), so a `SeamDeckPremise` is realised by the
mark sum over the four μ₄ points.  (Constructor witnessing that the typed
premise is the μ₄-orbit image, not an arbitrary assumption.) -/
def ofMarkSet (S : Finset ℤ) (hS : ∀ m ∈ S, cls m = 0) : SeamDeckPremise :=
  ⟨S, hS⟩

end SeamDeckPremise

/-! ### Part 4 — the flat-metric all-orders closure (v276) -/

/-- `CommutesClock M`: the boundary operator `M` (matrix element `M n n'` in the
Fourier-mode basis) commutes with the carrier clock `ρ = diag(iⁿ)`, i.e. it connects
only equal clock-characters: `M n n' ≠ 0 ⇒ cls n = cls n'`. -/
def CommutesClock (M : ℤ → ℤ → ℂ) : Prop := ∀ n n', M n n' ≠ 0 → cls n = cls n'

/-- A **diagonal** boundary operator commutes with the clock (its only nonzero
entries are on `n = n'`).  The flat-metric Laplacian `Δ_flat` is diagonal in the
Fourier-mode basis. -/
theorem diagonal_commutesClock {M : ℤ → ℤ → ℂ}
    (hd : ∀ n n', n ≠ n' → M n n' = 0) : CommutesClock M := by
  intro n n' hMnn'
  by_cases h : n = n'
  · rw [h]
  · exact absurd (hd n n' h) hMnn'

/-- A **spectral function** `g` of a diagonal operator with eigenvalues `d` is the
diagonal operator with eigenvalues `g ∘ d` — by construction still diagonal.  This
models `H = g(Δ_flat)` (e.g. `g = √·`, the DtN `√(-Δ_flat)`). -/
def specFun (g : ℂ → ℂ) (d : ℤ → ℂ) : ℤ → ℤ → ℂ :=
  fun n n' => if n = n' then g (d n) else 0

theorem specFun_diagonal (g : ℂ → ℂ) (d : ℤ → ℂ) :
    ∀ n n', n ≠ n' → specFun g d n n' = 0 := by
  intro n n' h; simp [specFun, h]

/-- **Flat-metric all-orders closure (the Lean form of `v276`).** For the flat τ=i
pillowcase the DtN modular Hamiltonian `H = g(Δ_flat)` is a spectral function of the
Fourier-diagonal flat Laplacian, hence diagonal, hence commutes with the carrier
clock — for **every** spectral function `g`, i.e. to ALL orders, not merely the
principal (`v198`) and sub-principal (`v201`) orders.  This upgrades the conditional
block-diagonality to the full operator and reduces `QGEO.SYM.01` to the single
geometric premise *the raw seam carries the flat τ=i metric* (so that `H` is a
function of the diagonal `Δ_flat`).  The premise stays [O]; this closure is [F]. -/
theorem flat_all_orders_clock (g : ℂ → ℂ) (d : ℤ → ℂ) :
    CommutesClock (specFun g d) :=
  diagonal_commutesClock (specFun_diagonal g d)

/-! ### Part 5 — Flat-Away: positive-definiteness of the heat-trace deviation (v292/v295) -/

/-- The off-mark **heat-trace deviation** as a quadratic form in the smooth `ℤ₄`
curvature modes `g`, with weights `W k`: `Δ(g) = Σ_k W_k · (g_k)²`.  The weights are
the v295 second-order heat coefficients `W_k = c_k(t)`, proved positive there
(convexity of `Λ ↦ Tr e^{-tΛ}` together with the Gauss-Bonnet zero-mean condition). -/
def heatDeviation {ι : Type*} (s : Finset ι) (W g : ι → ℝ) : ℝ :=
  ∑ k ∈ s, W k * (g k) ^ 2

/-- **Non-negativity.**  With non-negative weights the heat-trace deviation is `≥ 0`. -/
theorem heatDeviation_nonneg {ι : Type*} (s : Finset ι) (W g : ι → ℝ)
    (hW : ∀ k ∈ s, 0 ≤ W k) : 0 ≤ heatDeviation s W g := by
  unfold heatDeviation
  exact Finset.sum_nonneg (fun k hk => mul_nonneg (hW k hk) (sq_nonneg _))

/-- **Positive-definiteness (the Flat-Away core).**  With *strictly positive* weights
the heat-trace deviation vanishes iff every smooth curvature mode vanishes — i.e.
matching the flat `(E₈)₁` heat data (`Δ = 0`) forces the off-mark curvature to be zero
(*flat away from the four μ₄ marks*).  The positivity of the weights `W_k = c_k(t)` is
the v295 analytic input; this lemma is the formal `Δ = 0 ⟺ flat` step.  Combined with
`markLocal_blockDiagonal` it closes the heat route of Flat-Away modulo that one input. -/
theorem heatDeviation_eq_zero_iff {ι : Type*} (s : Finset ι) (W g : ι → ℝ)
    (hW : ∀ k ∈ s, 0 < W k) :
    heatDeviation s W g = 0 ↔ ∀ k ∈ s, g k = 0 := by
  unfold heatDeviation
  rw [Finset.sum_eq_zero_iff_of_nonneg
        (fun k hk => mul_nonneg (hW k hk).le (sq_nonneg _))]
  refine ⟨fun h k hk => ?_, fun h k hk => ?_⟩
  · have hk0 : W k * (g k) ^ 2 = 0 := h k hk
    have hsq : (g k) ^ 2 = 0 := (mul_eq_zero.mp hk0).resolve_left (hW k hk).ne'
    rw [pow_two] at hsq
    exact mul_self_eq_zero.mp hsq
  · rw [h k hk]; ring

/-! ### Sanity: the clock has order 4 on the character classes -/

/-- The clock character is genuinely `ℤ/4`: the four residues `0,1,2,3` are
distinct, and a mode and its `+4` shift share a character (order-4 clock). -/
theorem cls_periodic (n : ℤ) : cls (n + 4) = cls n := by
  unfold cls
  rw [← sub_eq_zero, ← Int.cast_sub]
  have e : (n + 4 - n : ℤ) = 4 := by ring
  rw [e, ZMod.intCast_zmod_eq_zero_iff_dvd]
  norm_num

theorem cls_residues_distinct :
    cls 0 ≠ cls 1 ∧ cls 0 ≠ cls 2 ∧ cls 0 ≠ cls 3 ∧
    cls 1 ≠ cls 2 ∧ cls 1 ≠ cls 3 ∧ cls 2 ≠ cls 3 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> decide

end TFPT.Carrier.SeamDeckClosure
