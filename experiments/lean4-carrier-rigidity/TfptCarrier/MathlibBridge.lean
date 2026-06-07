/-
  TFPT Carrier — Mathlib Bridge
  -----------------------------

  The TFPT `Polarization` structure is a special case (the 2-element
  case) of Mathlib's `CompleteOrthogonalIdempotents`. Making this
  explicit in both directions has two benefits:

  * It positions the carrier algebra inside a standard Mathlib idiom
    rather than as a proprietary structure, which makes review and
    re-use cheaper.

  * It gives downstream consumers access to the existing Mathlib
    API for orthogonal-idempotent families (sum lemmas, ring-equiv
    factorisations, idempotent embeddings).

  We construct equivalences in both directions between `Polarization A`
  and the Mathlib statement
  `CompleteOrthogonalIdempotents (e : Fin 2 → A)` with
  `e 0 = Pm, e 1 = Pp`.
-/

import Mathlib.RingTheory.Idempotents
import Mathlib.Data.Fin.VecNotation

import TfptCarrier.Polarization

namespace TFPT.Carrier.MathlibBridge

open TFPT.Carrier

variable {A : Type*} [Ring A]

/-- A TFPT `Polarization` gives a Mathlib `CompleteOrthogonalIdempotents`
on the two-element family `(Pm, Pp)`. -/
theorem Polarization.toCompleteOrthogonalIdempotents (p : Polarization A) :
    CompleteOrthogonalIdempotents ![p.Pm, p.Pp] := by
  rw [CompleteOrthogonalIdempotents.pair_iff'ₛ]
  refine ⟨p.orth_mp, p.orth_pm, p.complete⟩

/-- Conversely: a 2-element family of complete orthogonal idempotents
gives a TFPT `Polarization`. -/
def Polarization.ofCompleteOrthogonalIdempotents
    (e : Fin 2 → A)
    (he : CompleteOrthogonalIdempotents e) :
    Polarization A where
  Pm := e 0
  Pp := e 1
  idem_m := (he.idem 0).eq
  idem_p := (he.idem 1).eq
  orth_mp := he.ortho (by decide : (0 : Fin 2) ≠ 1)
  orth_pm := he.ortho (by decide : (1 : Fin 2) ≠ 0)
  complete := by
    have := he.complete
    rw [Fin.sum_univ_two] at this
    exact this

end TFPT.Carrier.MathlibBridge
