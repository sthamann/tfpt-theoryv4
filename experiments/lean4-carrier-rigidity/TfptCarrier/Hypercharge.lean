/-
  TFPT Carrier — Layer 2: Hypercharge Spectrum
  --------------------------------------------

  Concrete 5×5 model that realises the SM hypercharge multiplet from
  the carrier polarization. The carrier `E = E₋ ⊕ E₊` with
  `dim E₋ = 3, dim E₊ = 2` is represented as `Fin 5` with the first
  three indices in `E₋` and the last two in `E₊`.

  This file discharges three concrete numerical facts:

    * `Y = diag(-1/3, -1/3, -1/3, 1/2, 1/2)`  — the SM hypercharge vector
    * `tr Y = 0`                              — abelian index closure
    * `6 Y² − Y − 1 = 0`                      — carrier polynomial,
                                                here on the concrete model

  All three are proved by direct rational arithmetic on a 5×5 matrix.
-/

import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Diagonal
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FinCases

namespace TFPT.Carrier.Hypercharge

open Matrix

/-- Carrier index set: 3 indices of `E₋` followed by 2 of `E₊`. -/
abbrev I := Fin 5

/--
The hypercharge matrix in the carrier basis:

    Y = diag(-1/3, -1/3, -1/3, 1/2, 1/2).

These are the hypercharges of the down-type quark colour-triplet
(`Y = -1/3`) and the lepton-doublet weak-isodoublet (`Y = 1/2`),
in TFPT's representation-theoretic order.
-/
def Y : Matrix I I ℚ := Matrix.diagonal ![-1/3, -1/3, -1/3, 1/2, 1/2]

/-- The diagonal entries of `Y` are the SM hypercharges. -/
lemma Y_diag_entries (i : I) : Y i i =
    (![(-1/3 : ℚ), -1/3, -1/3, 1/2, 1/2]) i := by
  unfold Y
  simp [Matrix.diagonal_apply_eq]

/-- Off-diagonal entries of `Y` vanish. -/
lemma Y_off_diag_zero (i j : I) (h : i ≠ j) : Y i j = 0 := by
  unfold Y
  exact Matrix.diagonal_apply_ne _ h

/--
**Trace identity.**

`tr Y = 0`. The abelian anomaly trace of the determinant-normalised
hypercharge generator on the first chiral family vanishes, which is the
carrier-level shadow of the Standard-Model abelian gauge-anomaly
cancellation.
-/
theorem trace_Y : Y.trace = 0 := by
  unfold Y
  rw [Matrix.trace_diagonal]
  simp [Fin.sum_univ_five]
  norm_num

/--
**Carrier polynomial identity, concrete form.**

The hypercharge matrix satisfies

    6 · (Y * Y) − Y − 1 = 0.

Proved per-entry: each of the 25 matrix entries reduces to a rational
equation between explicit numerals.
-/
theorem Y_carrier_polynomial : (6 : ℚ) • (Y * Y) - Y - 1 = 0 := by
  ext i j
  unfold Y
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Matrix.smul_apply, Matrix.sub_apply,
          Matrix.one_apply, Matrix.zero_apply, Matrix.diagonal_apply,
          Fin.sum_univ_five] <;>
    norm_num

end TFPT.Carrier.Hypercharge
