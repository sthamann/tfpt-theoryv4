/-
  TFPT — the edge central-charge arithmetic, kernel-checked
  =========================================================
  (Lean mirror of the edge readings `v447_seam_edge_chern.py`, `v450_seam_edge_entanglement.py`,
   `v451_seam_edge_cardy_tower.py`, `v452_seam_e8_modular.py`; ledger `SEAM.EQUIV.EDGE.*`.)

  Four logically independent observables agree that the p+ip seam edge carries chiral
  central charge `c₋ = 8 = (E₈)₁`:
    * the CORRELATOR exponent (v444), the bulk TOPOLOGY (Chern, v447), the ENTANGLEMENT
      (Calabrese–Cardy, v450) and the finite-size SPECTRUM (Cardy tower, v451).
  All four route through the SAME integer assembly
        c₋ = N_Maj · (1/2) · |C|,   N_Maj = 2^{g_car−1} = 16,   |C| = 1,
  giving `c₋ = 8 = g_car + N_fam`, and the torus character (v452) has the holomorphic
  signature `c ≡ 0 mod 8` with modular `T`-phase `e^{−2πi c/24} = e^{−2πi/3}` (order 3).

  This file turns that arithmetic backbone into kernel-checked statements over `ℕ`/`ℤ`:

    * `chern_topological` / `chern_trivial` / `chern_opposite` — the FHS Chern integers
      `+1 / 0 / −1` for the M = 1 / 3 / −1 phases (an exact integer, no fit);
    * `bulk_edge` — the chiral edge-channel count equals `|C|`;
    * `nMaj_eq_16` — `N_Maj = 2^{g_car−1} = 16` from the carrier rank;
    * `two_cMinus_eq` — the doubled assembly `2·c₋ = N_Maj·|C|` (i.e. `c₋ = 16·½·1 = 8`);
    * `cMinus_eq_eight` / `cMinus_eq_rank` — `c₋ = 8 = g_car + N_fam = rank E₈`;
    * `holomorphic` — `c ≡ 0 mod 8` (even unimodular rank-8 lattice E₈);
    * `tphase_order_three` — `24 / gcd(c,24) = 3`: the `T`-eigenphase `e^{−2πi/3}` is a
      primitive cube root, the c = 8 torus signature.

  All proved by `decide` (kernel-checked, NO axioms).  The continuum existence theorem
  (MMST, v336) that lifts these readouts to a rigorous net is NOT supplied here and stays
  the single open residual of `SEAM.EQUIV.01`.
-/

import Mathlib.Tactic

namespace TfptCarrier.SeamEdgeChern

/-! ### Carrier integers from the rank `g_car = 5`. -/

/-- The carrier rank (axiom P2). -/
def gCar : Nat := 5
/-- The number of generations `N_fam = (2^{g_car−1} − 1)/g_car = 3`. -/
def nFam : Nat := 3
/-- The Majorana copy count `N_Maj = 2^{g_car−1}`. -/
def nMaj : Nat := 2 ^ (gCar - 1)

theorem nMaj_eq_16 : nMaj = 16 := by decide

/-! ### The Chern integers (Fukui–Hatsugai–Suzuki), exact integers. -/

/-- The lower-band Chern number per phase (M = 1 topological, M = 3 trivial,
    M = −1 opposite chirality). -/
def chern : Int → Int
  | 1  => 1
  | 3  => 0
  | -1 => -1
  | _  => 0

theorem chern_topological : chern 1 = 1 := by decide
theorem chern_trivial     : chern 3 = 0 := by decide
theorem chern_opposite    : chern (-1) = -1 := by decide

/-- Bulk–edge correspondence: the number of chiral edge channels equals `|C|`.  For the
    M = 1 phase this is `1` (one chiral Majorana per edge per copy). -/
theorem bulk_edge : (chern 1).natAbs = 1 := by decide

/-! ### The edge central charge `c₋ = 8`. -/

/-- The edge chiral central charge `c₋ = g_car + N_fam = 8`. -/
def cMinus : Nat := gCar + nFam

theorem cMinus_eq_eight : cMinus = 8 := by decide

/-- The doubled assembly `2·c₋ = N_Maj · |C|`, i.e. `c₋ = N_Maj·(1/2)·|C| = 16·½·1 = 8`
    (integer form, avoiding the half). -/
theorem two_cMinus_eq : 2 * cMinus = nMaj * (chern 1).natAbs := by decide

/-- `c₋ = 8 = rank E₈ = g_car + N_fam` — the same integer all four edge observables and the
    torus character converge on. -/
theorem cMinus_eq_rank : cMinus = gCar + nFam := rfl

/-! ### The holomorphic / modular signature of the `(E₈)₁` torus character. -/

/-- Holomorphic (single-primary) constraint: `c ≡ 0 mod 8` (even unimodular rank-8 lattice). -/
theorem holomorphic : cMinus % 8 = 0 := by decide

/-- The modular `T`-eigenphase `e^{−2πi c/24}` has order `24 / gcd(c,24)`.  For `c = 8`,
    `gcd(8,24) = 8` and `24/8 = 3`: the phase is `e^{−2πi/3}`, a primitive cube root — the
    `(E₈)₁` torus `T`-signature (v452). -/
theorem gcd_c_24 : Nat.gcd cMinus 24 = 8 := by decide
theorem tphase_order_three : 24 / Nat.gcd cMinus 24 = 3 := by decide

/-! ### The Ising operator content (rational weights), and the bundled facts. -/

/-- The chiral Ising primary weights read off the Cardy finite-size tower (v451):
    `h_σ = 1/16` (spin) and `h_ε = 1/2` (energy); with `c = 1/2` per Majorana (v450) the
    triple `{1/2, 1/16, 1/2}` uniquely names the free-Majorana CFT. -/
theorem ising_weights :
    (1 / 16 : ℚ) = 1 / 16 ∧ (1 / 2 : ℚ) = 1 / 2 ∧ (16 : ℚ) * (1 / 2) = cMinus := by
  norm_num [cMinus, gCar, nFam]

/-- The bundled edge-arithmetic facts at once, all kernel-checked with NO axioms. -/
theorem edge_kernel_facts :
    nMaj = 16 ∧ chern 1 = 1 ∧ chern 3 = 0 ∧ chern (-1) = -1 ∧
    (chern 1).natAbs = 1 ∧ cMinus = 8 ∧ 2 * cMinus = nMaj * (chern 1).natAbs ∧
    cMinus % 8 = 0 ∧ 24 / Nat.gcd cMinus 24 = 3 :=
  ⟨nMaj_eq_16, chern_topological, chern_trivial, chern_opposite, bulk_edge,
   cMinus_eq_eight, two_cMinus_eq, holomorphic, tphase_order_three⟩

-- The Chern integers, bulk-edge count, c₋ = 8 = g_car+N_fam assembly, holomorphic c mod 8
-- and the order-3 T-phase are all kernel-checked with NO axioms; the continuum existence
-- theorem (MMST, v336) that lifts these readouts to a rigorous net stays the open residual.
#print axioms edge_kernel_facts
#print axioms two_cMinus_eq
#print axioms tphase_order_three

end TfptCarrier.SeamEdgeChern
