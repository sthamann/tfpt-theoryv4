/-
  TFPT — the µ₄ mark-locality commutation, as real linear algebra (formalising v201/v323)
  =======================================================================================

  v201 (`QGEO.SUBPRIN.01`) / v309 / v323 establish, on the finite seam model, that the
  µ₄ clock ρ = diag(iⁿ) commutes with a DtN sub-principal coupling iff that coupling is
  "mark-local", i.e. couples only Fourier modes differing by a multiple of 4 (the Z₄
  Fourier fingerprint).  Those modules verify it numerically (numpy).  This file turns the
  load-bearing case into an EXACT, kernel-checked statement over the Gaussian integers ℤ[i]:

    * an offset-4 coupling COMMUTES with the µ₄ clock   (i⁰ = i⁴ = 1, invisible to ρ);
    * an offset-2 coupling does NOT                     (i² = −1 ≠ 1, ρ sees it).

  The scalar heart is `i⁴ = 1` vs `i² = −1`; the matrix statements are the v201
  block-diagonality criterion, proved by `decide` on concrete 6×6 matrices over ℤ[i].
-/

import Mathlib.NumberTheory.Zsqrtd.GaussianInt
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

namespace TfptCarrier.Mu4Commutation

/-- The imaginary unit `i ∈ ℤ[i]`. -/
def I : GaussianInt := ⟨0, 1⟩

/-- The seam clock order: `i⁴ = 1` — an offset-4 mode shift is invisible to the µ₄ clock. -/
theorem i_pow_four : I ^ 4 = 1 := by decide

/-- `i² = −1` — an offset-2 mode shift flips the sign, so the µ₄ clock SEES it. -/
theorem i_pow_two : I ^ 2 = -1 := by decide

/-- The µ₄ clock on 6 Fourier modes: `ρ = diag(iⁿ)`, n = 0..5. -/
def rho : Matrix (Fin 6) (Fin 6) GaussianInt :=
  Matrix.diagonal (fun n => I ^ (n : ℕ))

/-- An offset-4 coupling (modes 0 ↔ 4): the Z₄-invariant / mark-local case. -/
def M4 : Matrix (Fin 6) (Fin 6) GaussianInt :=
  fun i j => if (i = 0 ∧ j = 4) ∨ (i = 4 ∧ j = 0) then 1 else 0

/-- An offset-2 coupling (modes 0 ↔ 2): the non-mark-local (Z₂) case. -/
def M2 : Matrix (Fin 6) (Fin 6) GaussianInt :=
  fun i j => if (i = 0 ∧ j = 2) ∨ (i = 2 ∧ j = 0) then 1 else 0

set_option maxRecDepth 10000 in
/-- MARK-LOCAL ⇒ COMMUTES: an offset-4 (Z₄-invariant) coupling commutes with the µ₄ clock
    — the v201 block-diagonality criterion, exact over ℤ[i]. -/
theorem mu4_commutes_offset4 : rho * M4 = M4 * rho := by decide

set_option maxRecDepth 10000 in
/-- NON-MARK-LOCAL ⇒ DOES NOT COMMUTE: an offset-2 coupling fails to commute with the µ₄
    clock (ρ sees the sign flip i² = −1) — the v201/v309 negative control, exact. -/
theorem mu4_not_commutes_offset2 : rho * M2 ≠ M2 * rho := by decide

end TfptCarrier.Mu4Commutation
