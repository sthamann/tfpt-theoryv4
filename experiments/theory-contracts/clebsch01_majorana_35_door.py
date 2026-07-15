"""clebsch01 -- theory contract: THE 3/5 CLEBSCH DOOR (v482's named escape),
ENUMERATED AND DECIDED AT THE GROUP-THEORY LEVEL (2026-07-15).

v482 excluded the integer rung M_R = c3^3 Mbar as an unstructured pin and
recorded the ONE named escape: a third-generation Majorana structure factor
r = M_R,base / M_R,3 ~ 1.6696, sitting 0.18% from g_car/N_fam = 5/3 --
declined because 'no mechanism forces a 3/5 Clebsch on M_R3 today'.  This
contract enumerates the minimal Pati-Salam/SO(10) Majorana channels and
decides whether such a Clebsch CAN exist:

  D1 [E] NO RENORMALISABLE CHANNEL: sym^2(16) = 10 + 126 -- the only Higgs
     giving a renormalisable nu^c nu^c mass is the 126bar, and the 126 is
     NOT in the E8 hull {1, 10, 16, 45} (v247).  M_R must come from the
     d=5 operator (16_F 16bar_H)(16_F 16bar_H)/Lambda with the E8-allowed
     16_H.
  D2 [E] CHANNEL LIST: 16 x 16bar = 1 + 45 + 210; the E8 hull admits the
     singlet and 45 channels (210 absent).  A 45-channel insertion acts on
     nu^c through its charges under the Cartan directions T_3R, B-L, Y
     (and the SU(4) 15-direction = B-L up to normalisation).
  D3 [E] THE nu^c CHARGE TABLE: (B-L, T_3R, Y)(nu^c) = (+1, -1/2, 0) with
     Y = T_3R + (B-L)/2 verified on all 16 states and Tr_16 Y^2 = 10/3
     (v485's exact trace).
  D4 [E] THE 2,3-SMOOTH THEOREM (the door closes): every available
     nu^c channel weight -- 1 (singlet), T_3R^2 = 1/4, (B-L)^2 = 1,
     T_3R(B-L) = -1/2, and the SU(4)-adjoint weight (T15^2 ~ 3/8) -- is a
     {2,3}-smooth rational (numerator and denominator products of 2's and
     3's).  The multiplicative closure of {2,3}-smooth rationals never
     contains 5/3 or 3/5 (a factor 5 cannot appear).  The ONLY natural 5
     in the embedding is k_Y = 5/3 = (Tr_16 Y^2)/(Tr_16 T_3L^2) -- a
     FULL-MULTIPLET trace, not a nu^c matrix element -- and its carrier
     direction Y has Y(nu^c) = 0 EXACTLY: the unique 5-carrying group
     number is structurally decoupled from the Majorana operator.
  D5 [E] GENERATION-BLINDNESS: Clebsch factors multiply the WHOLE family
     matrix c_ij of the d=5 operator; a per-generation ratio (gen-3
     suppressed by 3/5) is a FLAVOR texture, not a group Clebsch --
     group theory cannot produce it by construction.
  D6 [O] COMPILER-FLAVOR INVENTORY (typed, declined): exact 3/5's inside
     the frozen flavor tables exist only in WRONG slots -- K lepton row
     (5,3,2): gen2/gen1 = 3/5; R lepton row (2,5,3) and L lepton row
     (8,5,3): gen3/gen2 = 3/5 -- but the v482 escape needs gen3/base with
     a DEGENERATE gen1 = gen2 base, and no frozen table has that shape;
     no mechanism links M_R to these address tables.  Recorded as
     inventory, declined per v354/v355.

NET: the 3/5 Clebsch door CLOSES.  m_3 via the exact rung + 3/5 stays a
numerical coincidence with no group-theoretic mechanism; the honest
endpoint remains the v481 one-parameter window candidate (M_R free inside
the PS window).  This is the 'falls cleanly through' outcome -- itself a
result.
"""
import json
from fractions import Fraction as F
from pathlib import Path

import sympy as sp

results = {}

# ---- the 16 of SO(10): (name, multiplicity, B-L, T_3R, Y) ------------------
SIXTEEN = [
    ("Q",    6, F(1, 3),  F(0),      F(1, 6)),
    ("u^c",  3, F(-1, 3), F(-1, 2),  F(-2, 3)),
    ("d^c",  3, F(-1, 3), F(1, 2),   F(1, 3)),
    ("L",    2, F(-1),    F(0),      F(-1, 2)),
    ("e^c",  1, F(1),     F(1, 2),   F(1)),
    ("nu^c", 1, F(1),     F(-1, 2),  F(0)),
]

# frozen compiler flavor tables (v12/v121; rows = sector up/down/lepton,
# columns = generation 1/2/3)
K = [[4, 2, 0], [4, 3, 2], [5, 3, 2]]
Q_TAB = [[3, 1, 0], [3, 2, 0], [3, 2, 1]]
R_TAB = [[1, 3, 0], [1, 5, 2], [2, 5, 3]]
L_TAB = [[7, 3, 0], [7, 5, 2], [8, 5, 3]]


def smooth23(x: F) -> bool:
    """True iff numerator and denominator factor over {2, 3} only."""
    for n in (abs(x.numerator), x.denominator):
        for p in (2, 3):
            while n % p == 0:
                n //= p
        if n != 1:
            return False
    return True


def main():
    ok = True

    # ---- D1: no renormalisable channel (needs 126bar, E8-forbidden) ----
    dim_sym2_16 = 16 * 17 // 2
    hull = {1, 10, 16, 45}
    d1 = dim_sym2_16 == 136 == 10 + 126 and 126 not in hull
    results["D1_no_renormalisable_channel"] = {
        "sym2_16": dim_sym2_16, "decomposition": "10 + 126",
        "E8_hull_SO10_content": sorted(hull), "contains_126": 126 in hull,
        "conclusion": "M_R only via d=5 (16 16bar_H)^2/Lambda (16_H is "
                      "E8-allowed; v247)",
        "pass": bool(d1)}
    ok &= d1

    # ---- D2: channel list for the d=5 operator ----
    d2 = 16 * 16 == 1 + 45 + 210
    results["D2_channel_list"] = {
        "16_x_16bar": "1 + 45 + 210 (256 total)",
        "E8_admissible_channels": ["singlet", "45"],
        "210_in_hull": 210 in hull,
        "pass": bool(d2)}
    ok &= d2

    # ---- D3: charge table exact ----
    y_ok = all(y == t3r + bl / 2 for _, _, bl, t3r, y in SIXTEEN)
    tr_y2 = sum(m * y * y for _, m, _, _, y in SIXTEEN)
    nu = next(r for r in SIXTEEN if r[0] == "nu^c")
    d3 = y_ok and tr_y2 == F(10, 3) and nu[2:] == (F(1), F(-1, 2), F(0))
    results["D3_nu_c_charges"] = {
        "Y_equals_T3R_plus_half_BL_on_all_16": y_ok,
        "Tr16_Y2": str(tr_y2),
        "nu_c_(B-L,T3R,Y)": [str(x) for x in nu[2:]],
        "pass": bool(d3)}
    ok &= d3

    # ---- D4: the 2,3-smooth theorem ----
    bl, t3r, y = nu[2], nu[3], nu[4]
    # available nu^c channel weights (relative to the singlet channel):
    weights = {
        "singlet": F(1),
        "T3R^2": t3r * t3r,
        "(B-L)^2": bl * bl,
        "T3R*(B-L)": t3r * bl,
        "SU4_15^2 (lepton: 9/24)": F(9, 24),
        "Y^2": y * y,            # = 0: the hypercharge channel is DEAD
        "Y*(B-L)": y * bl,       # = 0
    }
    all_smooth = all(smooth23(w) for w in weights.values() if w != 0)
    # closure argument: products of {2,3}-smooth rationals are {2,3}-smooth;
    # 5/3 is not {2,3}-smooth
    target_smooth = smooth23(F(5, 3))
    # the unique natural 5: k_Y = Tr Y^2 / Tr T3L^2 over the 16
    tr_t3l2 = 2 * (3 * F(1, 4) + F(1, 4))   # Q doublets (3 colors) + L doublet
    k_y = tr_y2 / tr_t3l2
    d4 = (all_smooth and not target_smooth and k_y == F(5, 3)
          and weights["Y^2"] == 0 and weights["Y*(B-L)"] == 0)
    results["D4_23smooth_theorem"] = {
        "nu_c_channel_weights": {k: str(v) for k, v in weights.items()},
        "all_nonzero_weights_23smooth": all_smooth,
        "5/3_is_23smooth": target_smooth,
        "closure": "products/quotients of {2,3}-smooth rationals stay "
                   "{2,3}-smooth -> 5/3 unreachable from any channel "
                   "combination",
        "unique_natural_5": f"k_Y = Tr16 Y^2 / Tr16 T3L^2 = {k_y} "
                            "(full-multiplet trace, v470)",
        "k_Y_decoupled_from_nu_c": "Y(nu^c) = 0 exactly -> the only "
                                   "5-carrying direction cannot touch M_R",
        "pass": bool(d4)}
    ok &= d4

    # ---- D5: generation-blindness of Clebsches (structural) ----
    # d=5 operator: c_ij (16_i 16bar_H)(16_j 16bar_H) -> M_R = Clebsch * c_ij:
    # the Clebsch is a SCALAR on family space (16's are identical reps).
    cij = sp.MatrixSymbol('c', 3, 3)
    clebsch = sp.Symbol('G')
    MR = clebsch * sp.Matrix(cij)
    ratios_generation_free = sp.simplify(MR[2, 2] / MR[0, 0]) == sp.Matrix(cij)[2, 2] / sp.Matrix(cij)[0, 0]
    results["D5_generation_blindness"] = {
        "statement": "M_R = G * c_ij with G a family-space scalar; any "
                     "generation ratio is c-texture, never Clebsch",
        "symbolic_check_G_cancels": bool(ratios_generation_free),
        "pass": bool(ratios_generation_free)}
    ok &= ratios_generation_free

    # ---- D6: compiler-flavor inventory (typed, declined) ----
    inventory = []
    for name, tab in (("K", K), ("Q", Q_TAB), ("R", R_TAB), ("L", L_TAB)):
        lep = tab[2]
        for (i, j, slot) in ((2, 0, "gen3/gen1"), (2, 1, "gen3/gen2"),
                             (1, 0, "gen2/gen1")):
            if lep[j] and F(lep[i], lep[j]) == F(3, 5):
                inventory.append(f"{name} lepton row {tuple(lep)}: "
                                 f"{slot} = 3/5")
    # the needed slot: gen3 suppressed by 3/5 against a DEGENERATE base
    # (v482 uses M_R = c3^3 Mbar * diag(1, 1, 3/5)) -- i.e. a lepton row
    # with gen1 = gen2 = base and gen3/base = 3/5.  Check all four tables:
    needed_slot_found = any(
        tab[2][0] == tab[2][1] and tab[2][0]
        and F(tab[2][2], tab[2][0]) == F(3, 5)
        for tab in (K, Q_TAB, R_TAB, L_TAB))
    d6 = (len(inventory) == 3 and not needed_slot_found
          and all(("gen2/gen1" in h) or ("gen3/gen2" in h)
                  for h in inventory))
    results["D6_compiler_flavor_inventory"] = {
        "exact_35_hits": inventory,
        "needed_slot": "gen3 vs unstructured base (v482: M_R3 = (3/5) "
                       "c3^3 Mbar with gen1 = gen2 = base)",
        "needed_slot_found": needed_slot_found,
        "typing": "wrong-slot hits recorded as inventory; no mechanism "
                  "links M_R to address tables; declined per v354/v355",
        "pass": bool(d6)}
    ok &= d6

    results["VERDICT"] = (
        "THE 3/5 CLEBSCH DOOR CLOSES: no renormalisable channel (126 "
        "E8-forbidden); all nu^c d=5 channel weights are {2,3}-smooth, so "
        "no channel combination reaches 5/3; the unique 5-carrying group "
        "number k_Y = 5/3 is decoupled (Y(nu^c) = 0); Clebsches are "
        "generation-blind by construction; compiler-flavor 3/5's sit in "
        "wrong slots.  The r ~ 5/3 rescue stays a numerical coincidence "
        "without mechanism -- the honest endpoint remains the v481 window "
        "candidate.")
    results["ALL_PASS"] = bool(ok)
    out = Path(__file__).with_name("clebsch01_majorana_35_results.json")
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
