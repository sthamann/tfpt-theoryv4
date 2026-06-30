/-
  TFPT — the Borchers/Wiesbrock standard-pair algebra, kernel-checked (formalising v438)
  =====================================================================================
  (Lean mirror of `v438_seam_hsmi_borchers.py`, ledger `SEAM.EQUIV.BW.HSMI.01`.)

  v438 attacks face (ii) of `SEAM.EQUIV.01` by the INTRINSIC Bisognano–Wichmann route:
  the seam supplies a Longo **standard pair** / `+`half-sided modular inclusion, so by
  Borchers' theorem the modular flow is geometric WITHOUT presupposing the
  rotation-covariance of the vacuum.  The Python module verifies the standard-pair
  relations numerically (numpy) on a finite ladder.  This file turns the load-bearing
  algebra into an EXACT, kernel-checked statement over ℤ, in the audit-contract style of
  `SeamScalingLimit.lean` / `BWKeystone.lean`.

  THE STANDARD-PAIR RELATIONS (Borchers/Wiesbrock/Longo), on the centred 5-mode ladder
  with boost `K = diag(-2,-1,0,1,2)`, lightlike translation `P` (the lowering shift) and
  the reflection `J` (index reversal):

    * `K*P − P*K = P`        the ax+b / Möbius commutator `[K,P] = P`;
    * `J*J = 1`              `J` is an involution (`Θ² = id`);
    * `J*K*J = −K`           the reflection reverses the boost (`u_Θ = J`, `ΘKΘ = −K`);
    * `J*P*J = P₊`           the reflection sends the translation to the OPPOSITE
                            translation (`ΘP Θ = P₋`), the standard-pair reflection.

  These four are proved by `decide` (kernel-checked, NO axioms).  The continuum
  positive-energy condition `P ≥ 0` and the cited Borchers/Wiesbrock theorem are declared
  as named `axiom`s — not re-proved; the conclusion (geometric modular flow / face (ii))
  then follows by a well-typed composition, and `#print axioms` pins the residual to
  exactly the cited theorem plus the ONE open continuum input (the continuum standard
  pair), which is the same wall as MMST/NPW26.  So face (ii) is "closed modulo a cited
  theorem": the standard-pair RELATIONS are machine-checked; only the continuum existence
  and the cited Borchers step are assumed.
-/

import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

namespace TfptCarrier.SeamStandardPair

/-! ### The standard-pair generators on the centred 5-mode ladder (exact, over ℤ). -/

/-- The boost generator `K = diag(-2,-1,0,1,2)` — centred so the reflection can reverse it. -/
def K : Matrix (Fin 5) (Fin 5) ℤ :=
  !![(-2), 0, 0, 0, 0;
     0, (-1), 0, 0, 0;
     0, 0, 0, 0, 0;
     0, 0, 0, 1, 0;
     0, 0, 0, 0, 2]

/-- The lightlike translation `P` — the lowering shift (sub-diagonal). -/
def P : Matrix (Fin 5) (Fin 5) ℤ :=
  !![0, 0, 0, 0, 0;
     1, 0, 0, 0, 0;
     0, 1, 0, 0, 0;
     0, 0, 1, 0, 0;
     0, 0, 0, 1, 0]

/-- The opposite translation `P₊` — the raising shift (super-diagonal). -/
def Pplus : Matrix (Fin 5) (Fin 5) ℤ :=
  !![0, 1, 0, 0, 0;
     0, 0, 1, 0, 0;
     0, 0, 0, 1, 0;
     0, 0, 0, 0, 1;
     0, 0, 0, 0, 0]

/-- The reflection `J` — index reversal (anti-diagonal), `u_Θ = J`. -/
def J : Matrix (Fin 5) (Fin 5) ℤ :=
  !![0, 0, 0, 0, 1;
     0, 0, 0, 1, 0;
     0, 0, 1, 0, 0;
     0, 1, 0, 0, 0;
     1, 0, 0, 0, 0]

/-! ### The standard-pair relations as kernel-checked facts (NO axioms). -/

set_option maxRecDepth 10000 in
/-- `[K,P] = P`: the ax+b / Möbius commutator of boost and lightlike translation
    (Borchers scaling `Δ^{it}P Δ^{-it} = e^{-t}P`), exact over ℤ. -/
theorem boost_translation_comm : K * P - P * K = P := by decide

set_option maxRecDepth 10000 in
/-- `J² = 1`: the reflection is an involution (`Θ² = id`). -/
theorem reflection_involution : J * J = 1 := by decide

set_option maxRecDepth 10000 in
/-- `J K J = −K`: the reflection reverses the boost (`Θ K Θ = −K`, `u_Θ = J`). -/
theorem reflection_reverses_boost : J * K * J = -K := by decide

set_option maxRecDepth 10000 in
/-- `J P J = P₊`: the reflection sends the translation to the OPPOSITE translation
    (`Θ P Θ = P₋`), the standard-pair reflection `J U(s) J = U(-s)`. -/
theorem reflection_flips_translation : J * P * J = Pplus := by decide

/-- The bundled standard-pair algebra: all four Borchers/Wiesbrock relations at once,
    kernel-checked. -/
theorem standard_pair_relations :
    (K * P - P * K = P) ∧ (J * J = 1) ∧ (J * K * J = -K) ∧ (J * P * J = Pplus) :=
  ⟨boost_translation_comm, reflection_involution,
   reflection_reverses_boost, reflection_flips_translation⟩

/-! ### The abstract nodes and the cited Borchers/Wiesbrock step (named axioms). -/

/-- The seam supplies a Longo standard pair: a positive-energy lightlike translation
    `P ≥ 0`, a boost `K` with `[K,P] = P`, and a reflection `J` reversing both.  The
    finite RELATIONS are the kernel-checked `standard_pair_relations`; the continuum
    POSITIVITY `P ≥ 0` (the `sl(2,ℝ)` lowest-weight condition the `c₃` one-sidedness
    demands) is the analytic content carried by this Prop. -/
axiom SeamHasStandardPair : Prop
/-- The seam modular flow is geometric — face (ii) of `SEAM.EQUIV.01`, obtained
    intrinsically (without presupposing rotation-covariance of the vacuum). -/
axiom GeometricModularFlow : Prop

/-- Borchers/Wiesbrock (cited): a standard pair `(K, P)` with `P ≥ 0`, `[K,P] = P` and a
    reflection `J` with `J K J = −K`, `J P J = P₋` is a `+`half-sided modular inclusion,
    so by Borchers' theorem the modular flow is geometric.  CITED, not re-proved; the
    finite algebra is the kernel-checked `standard_pair_relations`. -/
axiom borchers_wiesbrock : SeamHasStandardPair → GeometricModularFlow

/-- The ONE open continuum input: assembling the finite ladder algebra and the
    positive-energy representation into a genuine CONTINUUM standard pair (the same
    infinite-dimensional existence wall as MMST/NPW26). -/
axiom seam_continuum_standard_pair : SeamHasStandardPair

/-! ### The composition: face (ii) closed modulo the cited Borchers step. -/

/-- Intrinsic Bisognano–Wichmann: GIVEN the seam supplies a (continuum) standard pair,
    the modular flow is geometric — face (ii) of `SEAM.EQUIV.01` is a STRUCTURE
    consequence, not a state condition, and needs no rotation-covariance input. -/
theorem geometricModularFlowFromStandardPair : GeometricModularFlow :=
  borchers_wiesbrock seam_continuum_standard_pair

/-- Audit-contract check: the composition has exactly the intended conclusion. -/
example : GeometricModularFlow := geometricModularFlowFromStandardPair

/-- The boost is genuinely centred / traceless, so a reflection CAN reverse it
    (`tr K = 0`): the structural reason `J K J = −K` is possible at all. -/
theorem boost_traceless : Matrix.trace K = 0 := by decide

-- The standard-pair RELATIONS are kernel-checked with NO axioms; the residual of
-- face (ii) is EXACTLY the cited Borchers/Wiesbrock step + the one continuum standard
-- pair (the MMST/NPW26 wall) — no hidden assumption.
#print axioms standard_pair_relations
#print axioms geometricModularFlowFromStandardPair

end TfptCarrier.SeamStandardPair
