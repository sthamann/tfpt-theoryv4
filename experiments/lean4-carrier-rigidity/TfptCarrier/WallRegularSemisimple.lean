/-
  TFPT — the quark wall puncture is regular-semisimple, kernel-checked
  ================================================================================
  (Lean mirror of `flav04_wall_logahoric.py` + `flav03`, deep-step 4, 2026-07-10.)

  flav03/flav04 reduce González's wall residual to a boundary case and then IDENTIFY
  that boundary: the TFPT parabolic puncture is REGULAR SEMISIMPLE (its residue has
  distinct eigenvalues), so it is a tame/regular-singular point living in the
  ESTABLISHED logahoric/parahoric non-abelian Hodge framework (Biswas–Kydonakis–Majra;
  Baraglia–Kamgarpour–Varma).  This file certifies the finite arithmetic core of that
  identification, with NO axioms:

    * the cusp weights (×3) `{0,1,2}` are distinct (a regular flag);
    * the residue spectrum `Spec(Q₊) = 3·weight + 1 = {1,2,3}` is distinct
      (regular semisimple — the tame class);
    * an irregular control (coincident weights → `{1,1,3}`) correctly fails;
    * combined with `WallReducedMinuscule.wall_reduced`, the wall point is both
      regular-semisimple AND reduced/minuscule.

  NOT formalised (cited, not arithmetic): the logahoric/parahoric non-abelian Hodge
  correspondence and González's very-stable ⇔ reduced equivalence in that setting.
-/

import Mathlib.Tactic
import TfptCarrier.WallReducedMinuscule

namespace TfptCarrier.WallRegularSemisimple

/-- The parabolic cusp weights, scaled by 3 (GATE.UWALL cusp class `{0, 1/3, 2/3}`). -/
def cuspWeights3 : List Int := [0, 1, 2]

/-- The residue spectrum `Spec(Q₊) = 3·weight + 1`. -/
def residueSpec : List Int := cuspWeights3.map (· + 1)

/-- An irregular control: coincident weights give a repeated eigenvalue. -/
def irregularSpec : List Int := [1, 1, 3]

/-! ### Kernel-checked facts (no axioms). -/

/-- The cusp weights are pairwise distinct — a regular (full-flag) parabolic. -/
theorem cusp_distinct : cuspWeights3.Nodup := by decide

/-- The residue spectrum is exactly `{1, 2, 3}`. -/
theorem residue_spec : residueSpec = [1, 2, 3] := by decide

/-- The residue spectrum has three distinct eigenvalues — REGULAR SEMISIMPLE
    (the tame/regular-singular class). -/
theorem residue_regular_semisimple : residueSpec.Nodup := by decide

/-- The irregular control is NOT regular semisimple (repeated eigenvalue). -/
theorem irregular_control : ¬ irregularSpec.Nodup := by decide

/-- Combined wall certificate: the puncture is regular-semisimple (distinct residue
    spectrum `{1,2,3}`) AND the cocharacter is reduced/minuscule
    (`WallReducedMinuscule`). -/
theorem wall_regular_and_reduced :
    residueSpec.Nodup ∧
    residueSpec = [1, 2, 3] ∧
    cuspWeights3.Nodup ∧
    WallReducedMinuscule.reducedB WallReducedMinuscule.wallDegs = true :=
  ⟨residue_regular_semisimple, residue_spec, cusp_distinct,
   WallReducedMinuscule.wall_reduced⟩

-- The regular-semisimple + reduced arithmetic depends on NO axioms (pure kernel
-- `decide`); the cited residual (logahoric/parahoric nonabelian Hodge + González
-- reducedness ⇔ section) is not an arithmetic fact and is not asserted here.
#print axioms wall_regular_and_reduced

end TfptCarrier.WallRegularSemisimple
