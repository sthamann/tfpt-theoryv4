/-
  TFPT Carrier — Determinant Character of the Torus Action
  --------------------------------------------------------

  The Diophantine constraint `m · q₋ + n · q₊ = 0` is *not* an external
  input to the carrier rigidity proof. It is the trace-zero condition
  of the determinant character on the carrier torus.

  Concretely: let `T(λ)` denote the block diagonal endomorphism

      T(λ) := diag(λ^{q₋}, ..., λ^{q₋}, λ^{q₊}, ..., λ^{q₊})

  with `m` copies of `λ^{q₋}` and `n` copies of `λ^{q₊}`. Then

      det T(λ) = λ^{m · q₋ + n · q₊}.

  The carrier datum imposes the *determinant-preserving* condition
  `det T(λ) = 1` for all `λ`, which is equivalent to the integer
  equation `m · q₋ + n · q₊ = 0`.

  This module proves both halves of that equivalence using only the
  determinant of a diagonal matrix and an elementary argument over
  `ℚˣ`.

  No representation-theoretic machinery is required: this lives
  entirely in `Mathlib.LinearAlgebra.Matrix.Determinant`.
-/

import Mathlib.Data.Matrix.Diagonal
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic.Linarith

namespace TFPT.Carrier.DeterminantCharacter

open Matrix

variable (K : Type*) [Field K]
variable (m n : ℕ)

/-- The diagonal torus action on the carrier `K^{m+n}`:
the first `m` coordinates scale by `λ^{q₋}`, the last `n` by `λ^{q₊}`. -/
def torusMatrix (lam : K) (qm qp : ℤ) :
    Matrix (Fin (m + n)) (Fin (m + n)) K :=
  Matrix.diagonal fun i => if i.val < m then lam ^ qm else lam ^ qp

variable {K m n}

/-- For nonzero `λ` and integer exponents `qm, qp`,

    det T(λ) = λ^{m · qm + n · qp}.

The proof is direct: the determinant of a diagonal matrix is the
product of its diagonal entries, and the sum of `m` copies of `qm`
plus `n` copies of `qp` is `m · qm + n · qp`. -/
theorem det_torusMatrix
    (lam : K) (qm qp : ℤ) (hlam : lam ≠ 0) :
    Matrix.det (torusMatrix K m n lam qm qp) = lam ^ ((m : ℤ) * qm + (n : ℤ) * qp) := by
  unfold torusMatrix
  rw [Matrix.det_diagonal, Fin.prod_univ_add]
  -- Two pieces:
  --   ∏ i : Fin m, (if (castAdd n i).val < m then λ^qm else λ^qp)
  --   ∏ i : Fin n, (if (natAdd m i).val < m then λ^qm else λ^qp)
  have h1 : ∀ i : Fin m, (Fin.castAdd n i : ℕ) < m := fun i => by
    simp [Fin.castAdd]
  have h2 : ∀ i : Fin n, ¬ ((Fin.natAdd m i : ℕ) < m) := fun i => by
    simp [Fin.natAdd]
  rw [Finset.prod_congr rfl (fun i _ => if_pos (h1 i)),
      Finset.prod_congr rfl (fun i _ => if_neg (h2 i))]
  rw [Finset.prod_const, Finset.prod_const,
      Finset.card_univ, Finset.card_univ,
      Fintype.card_fin, Fintype.card_fin]
  -- Goal: (λ^qm)^m * (λ^qp)^n = λ^(m·qm + n·qp)
  rw [← zpow_natCast (lam ^ qm) m, ← zpow_natCast (lam ^ qp) n,
      ← zpow_mul, ← zpow_mul,
      ← zpow_add₀ hlam]
  congr 1
  push_cast
  ring

/--
**Determinant-preserving condition as a Diophantine constraint.**

For nonzero `λ : K`, the torus matrix `T(λ)` has determinant `1` iff
`λ^{m · qm + n · qp} = 1`. The integer equation
`m · qm + n · qp = 0` then follows from any choice of `λ` of
infinite multiplicative order.
-/
theorem det_torusMatrix_eq_one_iff
    (lam : K) (qm qp : ℤ) (hlam : lam ≠ 0) :
    Matrix.det (torusMatrix K m n lam qm qp) = 1
      ↔ lam ^ ((m : ℤ) * qm + (n : ℤ) * qp) = 1 := by
  rw [det_torusMatrix lam qm qp hlam]

/--
**Headline: determinant-preserving on all positive rationals
implies the trace-zero lattice condition.**

If `det T(λ) = 1` for *every* positive rational `λ ≠ 1`, then
`m · qm + n · qp = 0`.

This is the proper logical content of "the carrier torus is
determinant-preserving": a universal statement over the torus
parameter `λ`, not a single-point check. Specialising to a single
`λ = 2 ∈ ℚˣ` with infinite multiplicative order suffices, which is
recorded as the helper lemma `trace_zero_of_det_one_at_two`.
-/
theorem trace_zero_of_det_one_forall_rat
    (qm qp : ℤ)
    (hdet : ∀ lam : ℚ, 0 < lam → lam ≠ 1
              → Matrix.det (torusMatrix ℚ m n lam qm qp) = 1) :
    (m : ℤ) * qm + (n : ℤ) * qp = 0 := by
  have h := hdet 2 (by norm_num) (by norm_num)
  have h2 : (2 : ℚ) ≠ 0 := by norm_num
  rw [det_torusMatrix (2 : ℚ) qm qp h2] at h
  exact (zpow_eq_one_iff_right₀ (by norm_num : (0 : ℚ) ≤ 2)
                                 (by norm_num : (2 : ℚ) ≠ 1)).mp h

/--
**Single-point helper.**

Specialised statement: if `det T(2) = 1` over `ℚ`, then
`m · qm + n · qp = 0`. The witness `λ = 2` has infinite
multiplicative order in `ℚˣ`, which is the only fact used.

Kept as a separate lemma because audit pipelines occasionally need
a single concrete value rather than a universal quantifier.
-/
theorem trace_zero_of_det_one_at_two
    (qm qp : ℤ)
    (hdet : Matrix.det (torusMatrix ℚ m n (2 : ℚ) qm qp) = 1) :
    (m : ℤ) * qm + (n : ℤ) * qp = 0 := by
  have h2 : (2 : ℚ) ≠ 0 := by norm_num
  rw [det_torusMatrix (2 : ℚ) qm qp h2] at hdet
  exact (zpow_eq_one_iff_right₀ (by norm_num : (0 : ℚ) ≤ 2)
                                 (by norm_num : (2 : ℚ) ≠ 1)).mp hdet

end TFPT.Carrier.DeterminantCharacter
