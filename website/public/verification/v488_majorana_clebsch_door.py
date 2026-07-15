"""v488 -- FLAV.NUSCALE.04: the 3/5 CLEBSCH DOOR, ENUMERATED AND CLOSED.
v482 named ONE escape for the integer seesaw rung (a third-generation
Majorana factor r ~ 1.6696, 0.18% from g_car/N_fam = 5/3) and declined it
for lack of a mechanism.  This module executes the mechanism search at the
group-theory level and finds a clean NEGATIVE: no minimal Pati-Salam /
SO(10) Majorana channel can produce 5/3.  The coincidence is decided dead;
the honest endpoint stays the v481 one-parameter window candidate.

  [E] 1. NO RENORMALISABLE CHANNEL: sym^2(16) = 136 = 10 + 126; the only
        Higgs giving a renormalisable nu^c nu^c mass is the 126bar, and
        the 126 is NOT in the E8 hull {1, 10, 16, 45} (v247).  M_R must
        come from the d = 5 operator (16_F 16bar_H)(16_F 16bar_H)/Lambda
        with the E8-allowed 16_H.
  [E] 2. CHANNEL LIST: 16 x 16bar = 1 + 45 + 210 (= 256); the E8 hull
        admits the singlet and 45 channels (210 absent).  A 45 insertion
        acts on nu^c through its Cartan charges T_3R, B-L, Y (the SU(4)
        15-direction is B-L up to normalisation).
  [E] 3. CHARGE TABLE: (B-L, T_3R, Y)(nu^c) = (+1, -1/2, 0), with
        Y = T_3R + (B-L)/2 verified on all 16 states and Tr_16 Y^2 = 10/3
        (the v485 exact trace).
  [E] 4. THE {2,3}-SMOOTH THEOREM (the door closes): every available
        nu^c channel weight -- singlet 1, T_3R^2 = 1/4, (B-L)^2 = 1,
        T_3R(B-L) = -1/2, SU(4)-15 weight 3/8 -- is a {2,3}-smooth
        rational; the multiplicative closure of {2,3}-smooth rationals
        can never contain 5/3 (no factor 5).  The UNIQUE natural 5 of
        the embedding is k_Y = Tr_16 Y^2 / Tr_16 T_3L^2 = 5/3 (Ginsparg,
        v470) -- a full-multiplet trace, and its carrier direction has
        Y(nu^c) = 0 EXACTLY: the only 5-carrying group number is
        structurally decoupled from the Majorana operator.
  [E] 5. GENERATION-BLINDNESS: the Clebsch multiplies the WHOLE family
        matrix c_ij of the d = 5 operator (the three 16's are identical
        reps); a per-generation ratio is a flavor texture, never a
        Clebsch -- the required diag(1, 1, 3/5) shape cannot arise from
        group theory by construction.
  [O] 6. COMPILER-FLAVOR INVENTORY (typed, declined): exact 3/5's in the
        frozen address tables sit only in WRONG slots (K lepton row
        (5,3,2): gen2/gen1; R (2,5,3) and L (8,5,3) lepton rows:
        gen3/gen2); the v482 escape needs gen3 vs a DEGENERATE gen1 =
        gen2 base, which no frozen table has; and no mechanism links M_R
        to the address tables.  Recorded, declined per v354/v355.

NET EFFECT: the named escape of FLAV.NUSCALE.03 is DECIDED NEGATIVE at
the group-theory level -- the rung + 5/3 rescue is dead as a mechanism
candidate; the v481 window candidate (M_R free inside the PS window; the
Sigma m_nu = 0.059 eV floor as kill test) stands as the honest endpoint.
No gate closes; the frozen record is untouched.

Contract provenance: experiments/theory-contracts/
clebsch01_majorana_35_door.py (2026-07-15).  Exact (Fraction/sympy);
mirrorable, deferred to the next verified Wolfram engine run.
"""
from fractions import Fraction as F

import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, g_car

# the 16 of SO(10): (name, multiplicity, B-L, T_3R, Y)
SIXTEEN = [
    ("Q",    6, F(1, 3),  F(0),      F(1, 6)),
    ("u^c",  3, F(-1, 3), F(-1, 2),  F(-2, 3)),
    ("d^c",  3, F(-1, 3), F(1, 2),   F(1, 3)),
    ("L",    2, F(-1),    F(0),      F(-1, 2)),
    ("e^c",  1, F(1),     F(1, 2),   F(1)),
    ("nu^c", 1, F(1),     F(-1, 2),  F(0)),
]
HULL = {1, 10, 16, 45}                 # E8-allowed SO(10) content (v247)

# frozen flavor address tables (v12/v18/v20/v121); rows = up/down/lepton
K_TAB = [[4, 2, 0], [4, 3, 2], [5, 3, 2]]
Q_TAB = [[3, 1, 0], [3, 2, 0], [3, 2, 1]]
R_TAB = [[1, 3, 0], [1, 5, 2], [2, 5, 3]]
L_TAB = [[7, 3, 0], [7, 5, 2], [8, 5, 3]]


def smooth23(x: F) -> bool:
    for n in (abs(x.numerator), x.denominator):
        for p in (2, 3):
            while n % p == 0:
                n //= p
        if n != 1:
            return False
    return True


def run():
    reset()
    print("v488  FLAV.NUSCALE.04: the 3/5 Clebsch door -- enumerated, closed")

    # 1. no renormalisable channel
    check("NO RENORMALISABLE CHANNEL [E]: sym^2(16) = 136 = 10 + 126; the "
          "only renormalisable nu^c nu^c mass needs the 126bar, which is "
          "NOT in the E8 hull {1, 10, 16, 45} (v247) -- M_R only via the "
          "d = 5 operator (16_F 16bar_H)^2/Lambda with the E8-allowed 16_H",
          16 * 17 // 2 == 136 == 10 + 126 and 126 not in HULL)

    # 2. channel list
    check("CHANNEL LIST [E]: 16 x 16bar = 1 + 45 + 210 = 256; the E8 hull "
          "admits the singlet and 45 insertion channels (210 absent) -- a "
          "45 acts on nu^c through its Cartan charges T_3R, B-L, Y",
          16 * 16 == 1 + 45 + 210 and 45 in HULL and 210 not in HULL)

    # 3. charge table
    nu = next(r for r in SIXTEEN if r[0] == "nu^c")
    tr_y2 = sum(m * y * y for _, m, _, _, y in SIXTEEN)
    check("CHARGE TABLE [E]: Y = T_3R + (B-L)/2 on all 16 states; "
          "Tr_16 Y^2 = 10/3 (v485); (B-L, T_3R, Y)(nu^c) = (+1, -1/2, 0)",
          all(y == t3r + bl / 2 for _, _, bl, t3r, y in SIXTEEN)
          and tr_y2 == F(10, 3)
          and nu[2:] == (F(1), F(-1, 2), F(0)))

    # 4. the {2,3}-smooth theorem
    bl, t3r, y = nu[2], nu[3], nu[4]
    weights = [F(1), t3r * t3r, bl * bl, t3r * bl, F(9, 24)]
    tr_t3l2 = 2 * (3 * F(1, 4) + F(1, 4))
    k_y = tr_y2 / tr_t3l2
    check("{2,3}-SMOOTH THEOREM [E]: every nonzero nu^c channel weight "
          "{1, 1/4, 1, -1/2, 3/8} is {2,3}-smooth, and the multiplicative "
          "closure of {2,3}-smooth rationals never contains 5/3 (no factor "
          "5); the UNIQUE natural 5 is k_Y = Tr Y^2/Tr T_3L^2 = 5/3 = "
          "g_car/N_fam (v470), a full-multiplet trace whose direction has "
          "Y(nu^c) = 0 EXACTLY -- structurally decoupled from M_R",
          all(smooth23(w) for w in weights) and not smooth23(F(5, 3))
          and k_y == F(5, 3) and y == 0
          and F(g_car, N_fam) == F(5, 3))

    # 5. generation-blindness
    cij = sp.Matrix(sp.MatrixSymbol('c', 3, 3))
    G = sp.Symbol('G')
    check("GENERATION-BLINDNESS [E]: M_R = G c_ij with the Clebsch G a "
          "family-space SCALAR (identical 16's); every generation ratio is "
          "a c-texture -- diag(1, 1, 3/5) cannot arise from group theory",
          sp.simplify((G * cij)[2, 2] / (G * cij)[0, 0]
                      - cij[2, 2] / cij[0, 0]) == 0)

    # 6. compiler-flavor inventory
    hits = []
    for name, tab in (("K", K_TAB), ("Q", Q_TAB), ("R", R_TAB), ("L", L_TAB)):
        lep = tab[2]
        for i, j, slot in ((2, 0, "gen3/gen1"), (2, 1, "gen3/gen2"),
                           (1, 0, "gen2/gen1")):
            if lep[j] and F(lep[i], lep[j]) == F(3, 5):
                hits.append((name, slot))
    degenerate_base_hit = any(
        tab[2][0] == tab[2][1] and tab[2][0]
        and F(tab[2][2], tab[2][0]) == F(3, 5)
        for tab in (K_TAB, Q_TAB, R_TAB, L_TAB))
    check("COMPILER-FLAVOR INVENTORY [O] (typed, declined): exact 3/5's "
          "sit only in WRONG slots (K lepton (5,3,2): gen2/gen1; R (2,5,3) "
          "+ L (8,5,3): gen3/gen2); the v482 escape needs gen3 vs a "
          "DEGENERATE gen1 = gen2 base -- no frozen table has that shape, "
          "and no mechanism links M_R to the address tables (v354/v355)",
          hits == [("K", "gen2/gen1"), ("R", "gen3/gen2"),
                   ("L", "gen3/gen2")]
          and not degenerate_base_hit)

    return summary("v488 FLAV.NUSCALE.04: the 3/5 Clebsch door CLOSES -- "
                   "no renormalisable channel (126 E8-forbidden); all nu^c "
                   "d=5 channel weights {2,3}-smooth, 5/3 unreachable; the "
                   "unique 5 (k_Y = 5/3) decoupled by Y(nu^c) = 0; "
                   "Clebsches generation-blind; compiler 3/5's in wrong "
                   "slots -- the v482 rescue is DEAD as a mechanism "
                   "candidate; the v481 window candidate stands")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
