/-
  TFPT — the Kronheimer quiver input data, kernel-checked (v479)
  ==============================================================

  v479 (SEAM.KRONHEIMER.01) discharges the R3 "combinatorial-to-geometric
  bridge" of the det K = 1 keystone to Kronheimer's ALE theorems
  (J. Diff. Geom. 29 (1989) 665 and 685).  Kronheimer's INPUT datum is the
  affine McKay graph with its Kac marks (= dimension vector); this module
  kernel-checks that TFPT's compiler outputs ARE that datum, over ℤ:

    (i)   the Kac marks δ = (2,3,4,6,5,4,3,2,1) are the NULL vector of the
          affine-E₈ Cartan matrix:  C_aff · δ = 0;
    (ii)  equivalently they are the PERRON vector of the McKay adjacency:
          A · δ = 2 δ  (the v312 rewrite-attractor eigenvector);
    (iii) the regular-representation identity Σ δᵢ² = 120 = |2I| = |μ₄|·h(E₈)
          with h(E₈) = 30 = 2·3·5 the product of the seam atoms;
    (iv)  the hyper-Kähler quotient dimension count lands on 4:
          dim_ℝ M − 4 dim_ℝ G = 4(Σ_edges dᵢdⱼ − Σ dᵢ² + 1) = 4,
          with Σ_edges dᵢdⱼ = Σ dᵢ² = 120 forced by (i).

  The theorems (K-A construction / K-B Torelli) are CITED, not re-proved —
  same import class as the MMST/NPW26/AGT legs.  The open premise of
  SEAM.EQUIV.01 is untouched: this certifies only the finite input data.

  Node ordering: Bourbaki E₈ nodes 1..8, affine node 9 attached to node 8
  (the end of the long chain); marks in that ordering: (2,3,4,6,5,4,3,2,1).
-/

import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

namespace TfptCarrier.KronheimerMarks

/-- The affine-E₈ (McKay) adjacency matrix: Bourbaki chain 1–3–4–5–6–7–8,
    branch 2–4, affine node 9 on node 8. -/
def adjE8affine : Matrix (Fin 9) (Fin 9) ℤ :=
  !![0, 0, 1, 0, 0, 0, 0, 0, 0;
     0, 0, 0, 1, 0, 0, 0, 0, 0;
     1, 0, 0, 1, 0, 0, 0, 0, 0;
     0, 1, 1, 0, 1, 0, 0, 0, 0;
     0, 0, 0, 1, 0, 1, 0, 0, 0;
     0, 0, 0, 0, 1, 0, 1, 0, 0;
     0, 0, 0, 0, 0, 1, 0, 1, 0;
     0, 0, 0, 0, 0, 0, 1, 0, 1;
     0, 0, 0, 0, 0, 0, 0, 1, 0]

/-- The affine-E₈ Cartan matrix `C = 2·1 − A`. -/
def cartanE8affine : Matrix (Fin 9) (Fin 9) ℤ :=
  2 • (1 : Matrix (Fin 9) (Fin 9) ℤ) - adjE8affine

/-- The Kac marks (Bourbaki order + affine node) = the 2I irrep dimensions
    = the v312 rewrite-attractor Perron vector. -/
def marks : Fin 9 → ℤ := ![2, 3, 4, 6, 5, 4, 3, 2, 1]

set_option maxRecDepth 8000 in
/-- (i) The marks are the null vector of the affine Cartan matrix. -/
theorem marks_null : cartanE8affine.mulVec marks = 0 := by
  decide

set_option maxRecDepth 8000 in
/-- (ii) The marks are the Perron eigenvector of the McKay adjacency,
    `A · δ = 2 δ` — the graph-spectral form of the McKay tensor identity. -/
theorem marks_perron : adjE8affine.mulVec marks = fun i => 2 * marks i := by
  decide

/-- (iii) Regular representation: `Σ δᵢ² = 120 = |2I|`. -/
theorem marks_sq_sum : (∑ i, marks i ^ 2) = 120 := by
  decide

/-- (iii′) `120 = |μ₄| · h(E₈)` and `h(E₈) = 30 = 2·3·5` — the seam atoms. -/
theorem two_I_order : (120 : ℤ) = 4 * 30 ∧ (30 : ℤ) = 2 * 3 * 5 := by
  decide

/-- The edge sum `Σ_edges dᵢdⱼ = (1/2)·δᵀAδ`, computed here as `δᵀAδ = 240`. -/
theorem marks_adj_quadratic : (∑ i, marks i * adjE8affine.mulVec marks i) = 240 := by
  decide

/-- (iv) The Kronheimer hyper-Kähler dimension count: with
    `dim_ℝ M = 2·(δᵀAδ) = 480` (double quiver, quaternionic) and
    `dim_ℝ G = Σ δᵢ² − 1 = 119` (`Π U(δᵢ)/U(1)`), the quotient has
    `dim_ℝ X = 480 − 4·119 = 4` — the `ℂ²/Γ` geometry. -/
theorem kronheimer_dimension_count :
    2 * (∑ i, marks i * adjE8affine.mulVec marks i)
      - 4 * ((∑ i, marks i ^ 2) - 1) = 4 := by
  decide

/-- The combined Kronheimer-input certificate: the compiler marks are the
    null/Perron vector, carry `|2I| = 120 = 4·30` with `30 = 2·3·5`, and the
    hyper-Kähler quotient dimension is exactly `4`.  (The Kronheimer theorems
    themselves are cited, not re-proved; SEAM.EQUIV.01 stays open.) -/
theorem kronheimer_input_data :
    cartanE8affine.mulVec marks = 0
    ∧ adjE8affine.mulVec marks = (fun i => 2 * marks i)
    ∧ (∑ i, marks i ^ 2) = 120
    ∧ 2 * (∑ i, marks i * adjE8affine.mulVec marks i)
        - 4 * ((∑ i, marks i ^ 2) - 1) = 4 :=
  ⟨marks_null, marks_perron, marks_sq_sum, kronheimer_dimension_count⟩

end TfptCarrier.KronheimerMarks
