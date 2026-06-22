/-
  TFPT — Cartan determinants as real Matrix.det computations (hardening v308/v281)
  ===============================================================================

  The holomorphy discriminator of the keystone chain (SeamEquivChain.lean) used
  the *hardcoded* constants `primariesE8 := 1`, `primariesD8 := 4` for the
  anyon/primary count |det Cartan|.  This module grounds the carrier piece of
  that arithmetic in ACTUAL determinants of the integer Cartan matrices, proved
  by Lean rather than asserted:

      |det Cartan(A₃)| = 4 = |μ₄|        (the family glue index)
      |det Cartan(D₅)| = 4               (the carrier glue index)
      => carrier |det Gram(D₅ ⊕ A₃)| = 4·4 = 16 = dim S⁺   (v281)

  This turns the carrier anyon count (16 → the condensation tower 16→4→1 of
  v281) into a theorem about real determinants, not a constant.  The rank-8
  E₈/D₈ determinants stay the decide-proven Nat discriminator in
  SeamEquivChain.lean: an 8×8 Leibniz determinant is not kernel-`decide`-able,
  and indeed Mathlib's own `Mathlib.Data.Matrix.Cartan` leaves `E₈_det = 1` as a
  `proof_wanted` ("prefer to wait for a more principled determinant tactic"),
  while it proves the smaller `G₂_det`/`F₄_det` by `decide`.  The carrier 3×3
  (A₃) and 5×5 (D₅) cases are in that decidable range, so we prove them here.
-/

import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

namespace TfptCarrier.CartanDeterminants

/-- The `A₃` Cartan matrix (the family glue lattice). -/
def cartanA3 : Matrix (Fin 3) (Fin 3) ℤ :=
  !![2, -1, 0; -1, 2, -1; 0, -1, 2]

/-- `|det Cartan(A₃)| = 4 = |μ₄|`, the family glue index — a real 3×3 determinant. -/
theorem cartanA3_det : cartanA3.det = 4 := by
  simp [cartanA3, Matrix.det_fin_three]

/-- The `D₅` Cartan matrix (the carrier half-spinor lattice). -/
def cartanD5 : Matrix (Fin 5) (Fin 5) ℤ :=
  !![ 2, -1,  0,  0,  0;
     -1,  2, -1,  0,  0;
      0, -1,  2, -1, -1;
      0,  0, -1,  2,  0;
      0,  0, -1,  0,  2]

set_option maxRecDepth 4000 in
/-- `|det Cartan(D₅)| = 4`, the carrier glue index — a real 5×5 determinant. -/
theorem cartanD5_det : cartanD5.det = 4 := by
  decide

/-- The carrier `|det Gram(D₅ ⊕ A₃)| = |det D₅|·|det A₃| = 4·4 = 16 = dim S⁺`
    (v281's anyon count, now from real determinants). -/
theorem carrier_index_from_dets :
    cartanD5.det * cartanA3.det = 16 := by
  rw [cartanA3_det, cartanD5_det]; norm_num

end TfptCarrier.CartanDeterminants
