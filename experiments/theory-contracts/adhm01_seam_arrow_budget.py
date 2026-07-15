"""adhm01 -- theory contract: THE SEAM-SIDE ARROW BUDGET of the Kronheimer
bridge (first concrete step feeding SEAM.KRONHEIMER.01 / v479 from the seam
side; 2026-07-15).

v479 discharged the graph->geometry bridge to Kronheimer's theorems and left
ONE [O] premise: 'the raw seam supplies ALE hyper-Kaehler data asymptotic to
the (2,3,5) cone'.  This probe makes the FIRST layer of that premise concrete
by computing exactly WHAT the seam has to supply -- the arrow datum of the
marks quiver -- and showing its budget is made of already-frozen seam
structures.  Dictionary + exact counts; NO new physics claim; nothing
promoted.

  A1 [E] THE ARROW BUDGET IS THE ROOT COUNT: the double-quiver rep space of
     the marks quiver has dim_C M = 2 sum_edges delta_i delta_j = 240 =
     |R(E8)| -- ONE complex arrow dimension per E8 root (= 248 - 8).
     Equivalently dim_C M = |Z2| |2I| = 2 x 120: the regular representation,
     sheet-doubled (M = (C^2 (x) End R)^Gamma, the C^2 = the Z2 sheet
     doublet of the quaternionic structure).
  A2 [E] THE BUDGET BRANCHES LIKE THE CARRIER: under E8 -> SO(10) x SU(4)
     (v247) the 240 roots split as 40 + 12 + 60 + 128 (adjoint-coset roots
     of D5, of A3, the (10,6) block, the two spinor blocks) -- the SAME
     52 = 40 + 12 carrier coset root count already frozen in v128/v135.
  A3 [E] GAUGE + MOMENT-MAP BOOKKEEPING: dim_R G = sum delta_i^2 - 1 = 119;
     moment-map target dim = 3 x 119 = 357; dim_R mu^-1(0) = 480 - 357 =
     123 = dim G + 4 -- the 4 of the ALE geometry (v479's count, redone
     from the arrow side).
  A4 [E] THE mu4 x 30 SPLIT OF THE GAUGE DATUM: the regular rep restricted
     to the seam's binary clock mu4 subgroup has EXACTLY multiplicity 30 =
     h(E8) in each of the 4 characters (chi_R(g) = 0 off the identity, so
     m_k = 120/4 = 30) -- i.e. the 120-dim quiver gauge datum is |mu4| x
     h(E8) = (the four seam marks) x (the seam's Coxeter totative cycle,
     v223/v315): both factors are frozen seam structures.  Also the
     deformation/period datum dim(h (x) R^3) = 3 x 8 = 24 = |R+(A3)| x
     h(A3) = 6 x 4 -- the hexagon hand times the mark count.
  A5 [O] HONEST RESIDUAL (typed, the actual research step): what the seam
     has NOT yet supplied is the ALE metric datum itself -- a
     2I-equivariant identification of the v155/v160 covariance sector with
     a point of mu^-1(0) (three real moment-map levels from the family
     3-block x rank-8 Cartan = the 24-dim period datum).  This stays the
     SEAM.EQUIV.01-class premise; recorded as the named next extraction,
     not claimed.

Firewall: experiments/theory-contracts probe -- inventory/dictionary only,
not load-bearing, no ledger/marker change; feeds a future v-module only if
the A5 extraction ever lands.
"""
import json
from pathlib import Path

import sympy as sp

results = {}

# affine E8 (Bourbaki; node 9 = affine node attached to node 8)
EDGES = [(1, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (2, 4), (8, 9)]
MARKS = {1: 2, 2: 3, 3: 4, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1}

Z2, MU4, N_FAM, G_CAR = 2, 4, 3, 5
H_E8, RANK_E8 = 30, 8
H_A3, HEX = 4, 6


def main():
    ok = True

    # ---- A1: arrow budget = root count = sheet-doubled |2I| ----
    e_sum = sum(MARKS[a] * MARKS[b] for a, b in EDGES)
    dimC_M = 2 * e_sum
    roots_e8 = 248 - RANK_E8
    order_2I = sum(d * d for d in MARKS.values())
    a1 = dimC_M == 240 == roots_e8 == Z2 * order_2I
    results["A1_arrow_budget"] = {
        "sum_edges_didj": e_sum, "dimC_double_quiver": dimC_M,
        "roots_E8": roots_e8, "Z2_x_|2I|": Z2 * order_2I,
        "reading": "one complex arrow dimension per E8 root; the C^2 "
                   "factor = the Z2 sheet doublet",
        "pass": bool(a1)}
    ok &= a1

    # ---- A2: the budget branches like the carrier ----
    # E8 -> SO(10) x SU(4): 248 = (45,1)+(1,15)+(10,6)+(16,4)+(16b,4b) (v247)
    d5_coset = 45 - 5          # D5 adjoint roots
    a3_coset = 15 - 3          # A3 adjoint roots
    vector_block = 10 * 6
    spinor_block = 2 * 16 * 4
    a2 = (d5_coset + a3_coset + vector_block + spinor_block == 240
          and d5_coset + a3_coset == 52)   # v128/v135 carrier coset count
    results["A2_carrier_branching"] = {
        "split": {"D5_roots": d5_coset, "A3_roots": a3_coset,
                  "(10,6)": vector_block, "spinors": spinor_block},
        "total": d5_coset + a3_coset + vector_block + spinor_block,
        "carrier_coset_52_40_12": d5_coset + a3_coset,
        "pass": bool(a2)}
    ok &= a2

    # ---- A3: gauge + moment map bookkeeping ----
    dimR_G = order_2I - 1
    mm_target = 3 * dimR_G
    dimR_mu0 = 2 * dimC_M - mm_target
    a3 = dimR_G == 119 and dimR_mu0 == dimR_G + 4
    results["A3_moment_map"] = {
        "dimR_G": dimR_G, "moment_map_target": mm_target,
        "dimR_mu_inv_0": dimR_mu0, "ALE_dimension": dimR_mu0 - dimR_G,
        "pass": bool(a3)}
    ok &= a3

    # ---- A4: the mu4 x 30 split + the period datum ----
    # regular rep characters: chi_R(e) = |2I|, chi_R(g != e) = 0
    zeta = sp.exp(2 * sp.pi * sp.I / MU4)
    mults = [sp.simplify(sp.Rational(1, MU4) * sum(
        (order_2I if j == 0 else 0) * zeta ** (-j * k) for j in range(MU4)))
        for k in range(MU4)]
    period_dim = 3 * RANK_E8
    a4 = (all(m == H_E8 for m in mults)
          and MU4 * H_E8 == order_2I
          and H_E8 == Z2 * N_FAM * G_CAR
          and period_dim == 24 == HEX * H_A3)
    results["A4_mu4_x_30_split"] = {
        "mu4_character_multiplicities_in_regular_rep": [str(m) for m in mults],
        "|2I| = |mu4| x h(E8)": f"{order_2I} = {MU4} x {H_E8}",
        "h(E8) = |Z2| N_fam g_car": f"{H_E8} = {Z2}*{N_FAM}*{G_CAR}",
        "period_datum": f"dim(h x R^3) = 3 x {RANK_E8} = {period_dim} "
                        f"= |R+(A3)| x h(A3) = {HEX} x {H_A3}",
        "pass": bool(a4)}
    ok &= a4

    # ---- A5: honest residual (typed) ----
    results["A5_honest_residual"] = {
        "named_next_extraction": "a 2I-equivariant identification of the "
                                 "v155/v160 seam covariance sector with a "
                                 "point of mu^-1(0); the three moment-map "
                                 "levels from the family 3-block x rank-8 "
                                 "Cartan (the 24-dim period datum)",
        "class": "SEAM.EQUIV.01 face; recorded, not claimed",
        "pass": True}

    results["NET"] = ("the arrow datum the seam must supply is exactly the "
                      "E8 root budget 240 = 2x120, whose factors (|Z2| "
                      "sheet, |mu4| marks, h(E8) = 30 Coxeter cycle, family "
                      "3-block, hexagon hand) are ALL frozen seam "
                      "structures -- the bridge's input side is fully "
                      "budgeted; the metric identification (A5) is the "
                      "remaining research step")
    results["ALL_PASS"] = bool(ok)
    out = Path(__file__).with_name("adhm01_seam_arrow_results.json")
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
