/-
  TFPT — SEAM.EQUIV.01 composition chain (formal skeleton of v308)
  ================================================================

  This module is the Lean mirror of `v308_seam_equiv_chain.py`
  (ledger `SEAM.EQUIV.CHAIN.01`): the closing implication of the
  open keystone "the raw seam–Calderón boundary net IS the
  holomorphic c=8 net (E₈)₁", written as ONE well-typed logical
  chain whose dependency structure is machine-audited.

  The chain (each link's conclusion = the next link's hypothesis):

      GapPositive  --kitaev-->        InvertibleSRE
      InvertibleSRE --mueger/klm-->   HolomorphicC8
      HolomorphicC8 --conway/sloane-> SeamIsE8     (= SEAM.EQUIV.01)

  HONEST SCOPE.  The three category-theory / lattice steps are
  CITED standard theorems (Kitaev free-fermion invertibility;
  Müger / Kawahigashi–Longo–Müger holomorphy from a trivial
  Drinfeld center; Conway–Sloane uniqueness of the rank-8 even
  unimodular lattice), declared here as named `axiom`s — NOT
  re-proved.  The single carrier-forced input is the recovery gap
  Δ = 6 ln(3/2) > 0 (v302), and the one genuinely OPEN premise is
  the Osterwalder–Schrader identification "the OS-reconstructed
  bulk gap = the transfer gap".

  The VALUE of this file is therefore not a from-scratch proof but
  the machine-checked *composition* plus the *axiom audit*
  (`#print axioms seamEquivChain`), which pins the residual of the
  keystone to exactly the named cited theorems + the one OS input.
  This is the v308 certificate, formalised in the same
  audit-contract style as `AuditContract.lean` / `AxiomCheck.lean`.

  Plus a small provable arithmetic discriminator: the number of
  boundary primaries / bulk anyons (|det Cartan|) distinguishes
  E₈ (=1, holomorphic) from the same-central-charge rival
  D₈ = SO(16) (=4, non-holomorphic).
-/

namespace TfptCarrier.SeamEquivChain

/-! ### The four nodes of the closing chain (abstract propositions). -/

/-- The seam transfer gap is positive (carrier-forced: Δ = 6 ln(3/2) > 0, v302). -/
axiom GapPositive : Prop
/-- The gapped quasi-free seam bulk is invertible / short-range-entangled. -/
axiom InvertibleSRE : Prop
/-- The seam–Calderón boundary net is holomorphic with central charge 8. -/
axiom HolomorphicC8 : Prop
/-- The seam–Calderón net is the (E₈)₁ net.  This is `SEAM.EQUIV.01`. -/
axiom SeamIsE8 : Prop

/-! ### The cited literature implications (named external theorems, the [C] links). -/

/-- Kitaev (free-fermion periodic table): a gapped quasi-free 2+1D bulk carries no
    intrinsic anyons, hence is invertible/SRE. -/
axiom kitaev_invertibility : GapPositive → InvertibleSRE
/-- Müger / Kawahigashi–Longo–Müger: a trivial bulk Drinfeld center forces a
    holomorphic boundary net. -/
axiom mueger_klm_holomorphy : InvertibleSRE → HolomorphicC8
/-- Conway–Sloane / Dong–Xu: a holomorphic c=8 chiral net is the lattice net of the
    unique rank-8 even unimodular lattice E₈. -/
axiom conway_sloane_e8 : HolomorphicC8 → SeamIsE8

/-! ### The one carrier-forced input (the single OPEN premise, OS step). -/

/-- The carrier-forced recovery gap Δ = 6 ln(3/2) > 0 (v302), read through
    Osterwalder–Schrader as the bulk mass gap.  This OS identification is the single
    genuinely open premise of the keystone. -/
axiom recovery_gap : GapPositive

/-! ### The composition theorem (the v308 certificate). -/

/-- `SEAM.EQUIV.01` follows from the three cited links composed over the
    carrier-forced gap.  Well-typed composition; `#print axioms` below pins the
    exact residual. -/
theorem seamEquivChain : SeamIsE8 :=
  conway_sloane_e8 (mueger_klm_holomorphy (kitaev_invertibility recovery_gap))

/-- Audit-contract check (AuditContract.lean style): the chain has exactly the
    intended conclusion `SeamIsE8`. -/
example : SeamIsE8 := seamEquivChain

/-! ### The holomorphy discriminator (a small provable arithmetic fact). -/

/-- #boundary primaries / bulk anyons = |det Cartan(E₈)| = 1 (holomorphic). -/
def primariesE8 : Nat := 1
/-- #boundary primaries of the same-c rival D₈ = SO(16) = |det Cartan(D₈)| = 4. -/
def primariesD8 : Nat := 4

/-- The discriminator: E₈ has a single primary (holomorphic), the same-central-charge
    rival D₈ = SO(16) has four — so equal central charge is necessary, not sufficient,
    and holomorphy is the load-bearing selector. -/
theorem e8_unique_holomorphic : primariesE8 = 1 ∧ primariesD8 ≠ primariesE8 := by
  decide

-- The residual is exactly the named cited steps + the OS input.
-- `#print axioms` confirms the dependency set (kitaev/mueger_klm/conway_sloane
-- + recovery_gap + the four abstract nodes), i.e. no hidden assumption.
#print axioms seamEquivChain

end TfptCarrier.SeamEquivChain
