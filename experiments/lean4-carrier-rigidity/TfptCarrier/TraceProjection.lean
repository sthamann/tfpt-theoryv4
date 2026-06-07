/-
  TFPT Carrier — Structural Trace Theorem
  ---------------------------------------

  The abelian-trace identity `tr Y = 0` for the carrier hypercharge
  was proved in `Hypercharge.lean` by direct rational arithmetic on a
  concrete 5×5 diagonal. That is correct but unilluminating: it does
  not separate the structural content (linearity of trace; trace of a
  projector equals its rank) from the numerical content (the specific
  ranks 3 and 2).

  This module proves the *structural* theorem:

      tr (a • P₋ + b • P₊) = a · rank(P₋) + b · rank(P₊)

  for any pair of idempotent endomorphisms `P₋, P₊` of a finite-
  dimensional vector space.  The carrier-level statement
  `tr Y = 0` then follows from this by substituting the numerical
  values `a = -1/3, b = 1/2` and the rank discharge
  `rank(P₋) = 3, rank(P₊) = 2`.

  The proof rests on two Mathlib facts:

  1. `IsIdempotentElem.isProj_range`: an idempotent linear map is a
     projection onto its range.
  2. `IsProj.trace`: the trace of a projection equals the dimension
     of its range (in a finite-dimensional setting).

  See `Mathlib.LinearAlgebra.Trace` and `Mathlib.LinearAlgebra.Projection`.
-/

import Mathlib.LinearAlgebra.Trace
import Mathlib.LinearAlgebra.Projection
import Mathlib.LinearAlgebra.FiniteDimensional.Defs

namespace TFPT.Carrier.TraceProjection

open LinearMap Module

variable {K M : Type*}
variable [Field K] [AddCommGroup M] [Module K M] [FiniteDimensional K M]

/--
**Structural trace theorem.**

For any pair of idempotent endomorphisms `P₋, P₊` of a finite-
dimensional `K`-vector space `M`, and any scalars `a, b ∈ K`,

    tr (a • P₋ + b • P₊) = a · finrank(range P₋) + b · finrank(range P₊).

This is the structural statement underpinning `tr Y = 0` on the
carrier: linearity of trace plus the trace-equals-rank identity for
projectors.

No completeness or orthogonality hypothesis on `(P₋, P₊)` is needed —
the identity is purely about linearity of trace and trace-of-projector.
-/
theorem trace_linear_combination_of_idempotents
    (Pm Pp : M →ₗ[K] M)
    (hm : IsIdempotentElem Pm)
    (hp : IsIdempotentElem Pp)
    (a b : K) :
    LinearMap.trace K M (a • Pm + b • Pp)
      = a * (Module.finrank K (LinearMap.range Pm) : K)
        + b * (Module.finrank K (LinearMap.range Pp) : K) := by
  rw [map_add, map_smul, map_smul]
  rw [hm.isProj_range.trace, hp.isProj_range.trace]
  simp [smul_eq_mul]

/--
**Carrier corollary**: the trace of the determinant-normalised
hypercharge generator vanishes once the ranks are discharged.

Given two complementary orthogonal idempotents `P₋, P₊` with
`rank(P₋) = 3` and `rank(P₊) = 2`, the generator
`Y := -(1/3) • P₋ + (1/2) • P₊` satisfies `tr Y = 0`.

This is the abstract analogue of the per-entry computation in
`Hypercharge.trace_Y`. It works for *any* concrete realisation of
the carrier on a finite-dimensional vector space, not just the
diagonal 5×5 model.

The `[CharZero K]` assumption is genuinely needed: in characteristic
`2` or `3` the rationals `1/3, 1/2` are not defined, and the carrier
polynomial degenerates.
-/
theorem trace_carrier_Y_eq_zero
    [CharZero K]
    (Pm Pp : M →ₗ[K] M)
    (hm : IsIdempotentElem Pm)
    (hp : IsIdempotentElem Pp)
    (hrank_m : Module.finrank K (LinearMap.range Pm) = 3)
    (hrank_p : Module.finrank K (LinearMap.range Pp) = 2) :
    LinearMap.trace K M (-((1 : K)/3) • Pm + ((1 : K)/2) • Pp) = 0 := by
  rw [trace_linear_combination_of_idempotents Pm Pp hm hp]
  rw [hrank_m, hrank_p]
  push_cast
  field_simp
  norm_num

end TFPT.Carrier.TraceProjection
