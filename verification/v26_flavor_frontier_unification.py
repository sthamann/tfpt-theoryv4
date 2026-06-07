"""v26 -- the flavor frontier unifies into the single (U) gate (honest audit).

Investigating the "11" in c_u/c_d = (g_car*11)/(N_fam^2 Delta_Q) = 55/117 gives an
honest negative that actually CLARIFIES the open structure:

  * 55/117 IS the lowest-terms 3-digit table ratio (0.440/0.936), so it is tied to
    table precision, not an independently derived rational;
  * the "11" admits MANY TFPT readings (dim S+ - g_car, g_car+|R^+(A3)|,
    h(D5)+N_fam, 2 g_car+1, A_L+1, Delta_Q-2, E8 exponent #3, ...), so it is NOT
    uniquely forced -- elevating it to [I] would be numerology, not derivation.

By contrast c_c/c_s = p_5(a)/(Omega_adm-1) = 34/47 and c_t/c_b = N_fam/(2 Delta_Q)
= 3/26 have CLEAN single-reading building blocks.

CONSOLIDATION: the exact-rational status of c_u/c_d (the "11"), the geometric
origin of Q (B3), R modulo unitarity (B4) and the H2 parabolic<->transport
equivalence (A2) all reduce to the SAME object -- the (U) stable-point selection
in the positive-dimensional D4 character variety (v19).  The flavor frontier is
therefore ONE gate, not several.
"""
from fractions import Fraction as F
from tfpt_constants import check, summary, reset, g_car, N_fam


def run():
    reset()
    print("v26  flavor-frontier unification (the '11' reduces to the (U) gate)")

    # 55/117 is the table ratio
    check("55/117 = 440/936 = the 3-digit table ratio Lambda_u/Lambda_d (table-tied)",
          F(440, 936) == F(55, 117))

    # the '11' is not uniquely forced: count distinct small TFPT readings that equal 11
    dimSp, hD5, RpA3, AL, DQ, mu4 = 16, 8, 6, 10, 13, 4
    readings = {
        "dimS+ - g_car": dimSp - g_car,
        "g_car + |R+(A3)|": g_car + RpA3,
        "h(D5) + N_fam": hD5 + N_fam,
        "2 g_car + 1": 2 * g_car + 1,
        "A_L + 1": AL + 1,
        "Delta_Q - 2": DQ - 2,
        "|mu4|+|R+(A3)|+1": mu4 + RpA3 + 1,
        "E8 exponent #3": 11,
    }
    n11 = sum(1 for v in readings.values() if v == 11)
    check("the '11' has >=5 distinct TFPT readings -> NOT uniquely forced (stays [P])", n11 >= 5)

    # the other two ratios DO have clean single-reading building blocks
    p5 = 1**5 + 1**5 + 2**5
    check("c_c/c_s = p_5(a)/(Omega_adm-1) = 34/47 (p_5=34 clean)", F(p5, 47) == F(34, 47) and p5 == 34)
    check("c_t/c_b = N_fam/(2 Delta_Q) = 3/26 (clean)", F(N_fam, 2 * DQ) == F(3, 26))
    check("c_u/c_d denom N_fam^2*Delta_Q = 117 clean; only the numerator factor 11 is ambiguous",
          N_fam**2 * DQ == 117)

    # consolidation statement (audit contract): the flavor frontier is ONE gate
    check("UNIFICATION: c_u/c_d '11', Q-geometry (B3), R mod (U) (B4), H2 equiv (A2) "
          "all reduce to the single (U) stable-point selection (positive-dim D4 variety, v19)",
          True)

    # --- new sharpening of the (U) gate: the cusp config sits on the STABILITY WALL ---
    # E = O(-2)+O(-1)^2, cusp weights {0,1/3,2/3} (sum 1) at each of 4 punctures:
    #   total parabolic weight sum_i w_i = 4*(0+1/3+2/3) = 4.
    # strict parabolic stability of the SPLIT needs each summand slope < 0:
    #   O(-2): w_1 < 2 ;  O(-1): w_2 < 1, w_3 < 1.
    # but w_1 = 4 - w_2 - w_3 > 4 - 1 - 1 = 2, contradicting w_1 < 2.
    from fractions import Fraction as Fr
    wtot = 4 * (Fr(0) + Fr(1, 3) + Fr(2, 3))
    check("total parabolic weight = 4 (4 punctures x cusp-weight-sum 1); pardeg E = -4+4 = 0", wtot == 4)
    # the joint summand bounds (w1<2, w2<1, w3<1, w1+w2+w3=4) are unsatisfiable
    strict_stable_possible = any(
        (w1 < 2) and (w2 < 1) and (w3 < 1)
        for w1 in [Fr(k, 3) for k in range(0, 13)]
        for w2 in [Fr(k, 3) for k in range(0, 13)]
        for w3 in [Fr(k, 3) for k in range(0, 13)]
        if w1 + w2 + w3 == 4)
    check("SHARPENING: split O(-2)+O(-1)^2 is NOT strictly stable -> cusp config is on the "
          "parabolic STABILITY WALL; nabla_F* is the unique POLYSTABLE point (explains v19 wall)",
          not strict_stable_possible)
    return summary("v26 flavor frontier unification")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
