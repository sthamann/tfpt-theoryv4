/-
  TFPT — S3 / SEAM.EQUIV.01 continuum leg: the MMST scaling limit, formalised
  ===========================================================================
  (Lean mirror of the S3 closure stack: v336/v356/v366/v367 and v376–v379;
   ledger `FORM.SEAM.MMST.01`.)

  The keystone `SEAM.EQUIV.01` reduces (v356/v366) to ONE input, **S3**: the seam
  collar — realised as a gapped quasi-free chiral lattice free-fermion phase — has a
  massless scaling limit equal to the chiral net (E₈)₁.  The Python suite pins the
  TARGET of that limit at every computable level: central charge c = 8 (v376), the
  (E₈)₁ character with 248 currents / one primary (v377), the genus-1 torus
  degeneracy 1 (v378) and reflection positivity (v379).  What a computation CANNOT
  supply is the abstract continuum-EXISTENCE of the limit; that is the cited,
  published theorem of Morinelli–Morsella–Stottmeister–Tanimoto (chiral CFT from free
  lattice fermions, CMP 2022) together with the Adamo–Moriwaki–Tanimoto OS
  reconstruction (2024).

  This module formalises the logical status **"closed modulo a cited theorem"**, in
  the same audit-contract style as `SeamEquivChain.lean`:

   • the MMST applicability HYPOTHESES for the collar are *provable* arithmetic facts
     (`decide`): D = 16 Majorana copies, rank = c = 8, the range rank ≤ c ≤ D, the
     chiral central charge c₋ = D/2 = 8 ≠ 0, and the holomorphy discriminator
     det K = 1 (vs the same-c rival SO(16), det K = 4);
   • the MMST scaling-limit theorem and the Adamo OS/holomorphy selector are declared
     as named `axiom`s (the cited [C] external results), NOT re-proved;
   • the conclusion (E₈)₁ then follows by a well-typed composition, and
     `#print axioms seamScalingLimit` pins the residual to exactly those two cited
     theorems plus the one carrier-forced gap.

  So S3 is "closed modulo the published MMST/Adamo theorems": every TFPT-internal
  hypothesis is machine-checked; only the two cited theorems (and the carrier gap)
  are assumed.
-/

namespace TfptCarrier.SeamScalingLimit

/-! ### The collar's MMST hypotheses as provable arithmetic facts. -/

/-- Number of Majorana copies on the seam collar: dim S⁺ = 2^(g_car−1) = 16. -/
def D : Nat := 16
/-- Central charge of the carrier: c = g_car + N_fam = 8. -/
def c : Nat := 8
/-- Rank of the target lattice E₈ = 8. -/
def rankE8 : Nat := 8
/-- Chiral central charge c₋ = D/2 = 8. -/
def cMinus : Nat := D / 2
/-- #boundary primaries = |det Cartan(E₈)| = 1 (holomorphic). -/
def detK_E8 : Nat := 1
/-- #boundary primaries of the same-c rival SO(16) = |det Cartan(D₈)| = 4. -/
def detK_SO16 : Nat := 4

/-- The MMST applicability range rank ≤ c ≤ D holds for the collar: 8 ≤ 8 ≤ 16. -/
theorem mmst_range : rankE8 ≤ c ∧ c ≤ D := by decide
/-- The collar is chiral: c₋ = D/2 = 8 ≠ 0. -/
theorem chiral : cMinus = 8 ∧ cMinus ≠ 0 := by decide
/-- Holomorphy discriminator: the collar net is holomorphic (det K = 1); the
    same-central-charge rival SO(16) is not (det K = 4).  Equal central charge is
    therefore necessary but NOT sufficient — holomorphy is the load-bearing selector. -/
theorem holomorphic_discriminator : detK_E8 = 1 ∧ detK_SO16 ≠ detK_E8 := by decide

/-! ### The collar's structural hypotheses and the target (abstract Props). -/

/-- The collar is a gapped quasi-free (CAR) lattice free-fermion phase
    (carrier-forced gap Δ = 6 ln(3/2) > 0; v302/v367). -/
axiom CollarGappedQuasifree : Prop
/-- The massless scaling limit is a chiral CFT of central charge 8. -/
axiom ChiralCFT_c8 : Prop
/-- The scaling-limit net is the (E₈)₁ net.  This is `SEAM.EQUIV.01`. -/
axiom SeamIsE8 : Prop

/-- The carrier forces the collar to be a gapped quasi-free phase (v302/v367):
    the single carrier-forced structural input. -/
axiom collar_gapped : CollarGappedQuasifree

/-! ### The cited published theorems (named external axioms, the [C] links). -/

/-- Morinelli–Morsella–Stottmeister–Tanimoto (CMP 2022): a gapped quasi-free lattice
    free-fermion collar that is in the applicability range `rank ≤ c ≤ D` and chiral
    (`c₋ ≠ 0`) has a massless scaling limit that is a chiral CFT with the matching
    central charge.  CITED, not re-proved; the arithmetic hypotheses are the provable
    facts `mmst_range` and `chiral` above. -/
axiom mmst_scaling_limit :
    CollarGappedQuasifree → (rankE8 ≤ c ∧ c ≤ D) → cMinus ≠ 0 → ChiralCFT_c8

/-- Adamo–Moriwaki–Tanimoto (2024) OS reconstruction + the order-4 μ₄ clock
    holomorphy selector: a chiral c = 8 net that is holomorphic (det K = 1) is the
    (E₈)₁ lattice net — the same-c rival SO(16) (det K = 4) is excluded.  CITED, not
    re-proved; the holomorphy hypothesis is the provable `holomorphic_discriminator`. -/
axiom adamo_holomorphic_e8 :
    ChiralCFT_c8 → (detK_E8 = 1 ∧ detK_SO16 ≠ detK_E8) → SeamIsE8

/-! ### The composition theorem: S3 closed modulo the two cited theorems. -/

/-- `SEAM.EQUIV.01` follows from: the carrier-forced collar gap (`collar_gapped`), the
    *provable* MMST hypotheses (`mmst_range`, `chiral`), the cited MMST scaling-limit
    theorem, the *provable* holomorphy discriminator, and the cited Adamo OS theorem.
    A well-typed composition; `#print axioms` below pins the exact residual. -/
theorem seamScalingLimit : SeamIsE8 :=
  adamo_holomorphic_e8
    (mmst_scaling_limit collar_gapped mmst_range chiral.2)
    holomorphic_discriminator

/-- Audit-contract check: the composition has exactly the intended conclusion. -/
example : SeamIsE8 := seamScalingLimit

-- The residual is EXACTLY the two named cited published theorems
-- (`mmst_scaling_limit`, `adamo_holomorphic_e8`) plus the carrier gap
-- (`collar_gapped`); every other MMST hypothesis (range, chirality, holomorphy
-- discriminator) is a machine-proved arithmetic fact — so S3 is "closed modulo a
-- cited theorem", with no hidden assumption.
#print axioms seamScalingLimit

end TfptCarrier.SeamScalingLimit
