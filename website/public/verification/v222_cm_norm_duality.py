"""v222 -- CM-norm duality: the two exceptional moduli give 41 (square) and 7 (hex).

The seam carries the SQUARE modulus (mu4 = {1,i,-1,-i}, cross-ratio 2 => j=1728,
CM by the Gaussian integers Z[i]; v214/v216).  Its hexagonal partner is the
modulus j=0 (tau=rho=e^{i pi/3}, CM by the Eisenstein integers Z[omega]).  This
script shows that the two CM rings are the two metric readings of the SAME carrier
split (3,2)=(colour,weak) and the anchor (e1,e2)=(|mu4|,g_car)=(4,5), and that they
deliver two central TFPT integers as ideal NORMS, not as loose sums:

  [E] SQUARE (Z[i], j=1728):  N(g_car + i|mu4|) = 5^2 + 4^2 = 41 = 10 b1   (EM index)
                              N(3 + 2i)          = 3^2 + 2^2 = 13 = Delta_Q (carrier-split norm)
  [E] HEX    (Z[omega], j=0): N(3 + 2 omega)     = 3^2-3*2+2^2 = 7 = scalaron exponent

So 10 b1 = 41 stops being "e1^2+e2^2" and becomes the Gaussian norm of the
carrier-glue vector g_car + i|mu4| on the square seam; and the scalaron 7 is the
Eisenstein norm of the same (3,2) split on the hexagonal partner.  The single
split (3,2) generates (5,6,7,13) by elementary ring operations:

  3 + 2 = 5 = g_car,   3 * 2 = 6 = |R^+(A3)|,   3 - 2 = 1 = N_Phi,
  N_omega(3,2) = 7 = scalaron,   N_i(3,2) = 13 = Delta_Q.

Negative controls (the assignment is rigid, not a coincidence):
  the Eisenstein norm of (5,4) is 21 (not 41); the Gaussian norm of (3,2) is 13
  (not 7); generic splits b+s=5 do not reproduce the whole (5,6,7,13) table.

Status: [E] as ring arithmetic; [C] as the architecture bridge
"square<->EM/mu4-clock, hex<->scalaron/CP-phase".  Mirrored in
wolfram/tfpt_readouts_extension.wl.
"""
from tfpt_constants import (check, summary, reset, g_car, N_fam, b1)

MU4 = 4            # |mu4| = e1(a)
N_PHI = 1
SCALARON = 7
DELTA_Q = 13
RP_A3 = 6          # |R^+(A3)|


def N_gauss(a, b):
    """Norm in the Gaussian integers Z[i]:  |a + b i|^2 = a^2 + b^2."""
    return a * a + b * b


def N_eisen(a, b):
    """Norm in the Eisenstein integers Z[omega], omega = e^{2 pi i/3}:
       |a + b omega|^2 = a^2 - a b + b^2."""
    return a * a - a * b + b * b


def run():
    reset()
    print("v222  CM-norm duality: square gives 41 & 13, hexagon gives 7")

    # ---- the square seam (Gaussian Z[i], j = 1728) ----
    check("SQUARE [E]: N_Z[i](g_car + i|mu4|) = 5^2 + 4^2 = 41 = 10 b1 (EM index); "
          "the EM index 41 IS the Gaussian norm of the carrier-glue vector on the "
          "square seam, not merely e1(a)^2 + e2(a)^2",
          N_gauss(g_car, MU4) == 41 == int(10 * b1) == MU4**2 + g_car**2)
    check("SQUARE [E]: N_Z[i](3 + 2 i) = 3^2 + 2^2 = 13 = Delta_Q (carrier-split norm)",
          N_gauss(N_fam, 2) == DELTA_Q == 13)

    # ---- the hexagonal partner (Eisenstein Z[omega], j = 0) ----
    check("HEX [E]: N_Z[omega](3 + 2 omega) = 3^2 - 3*2 + 2^2 = 7 = scalaron "
          "exponent; the same (3,2) split read on the hexagonal CM ring",
          N_eisen(N_fam, 2) == SCALARON == 7)

    # ---- the (3,2) split is a small generator ----
    check("(3,2) split generator: 3+2 = 5 = g_car", N_fam + 2 == g_car)
    check("(3,2) split generator: 3*2 = 6 = |R^+(A3)|", N_fam * 2 == RP_A3)
    check("(3,2) split generator: 3-2 = 1 = N_Phi", N_fam - 2 == N_PHI)
    check("(3,2) -> (5, 6, 7, 13) = (g_car, |R^+(A3)|, scalaron, Delta_Q) by "
          "sum / product / Eisenstein-norm / Gaussian-norm",
          [N_fam + 2, N_fam * 2, N_eisen(N_fam, 2), N_gauss(N_fam, 2)]
          == [g_car, RP_A3, SCALARON, DELTA_Q])

    # ---- negative controls: the ring assignment is RIGID ----
    check("NEG: Eisenstein norm of (5,4) = 21, NOT 41 (the square needs Z[i])",
          N_eisen(g_car, MU4) == 21 and N_eisen(g_car, MU4) != 41)
    check("NEG: Gaussian norm of (3,2) = 13, NOT 7 (the scalaron needs Z[omega])",
          N_gauss(N_fam, 2) != SCALARON)
    check("NEG: the two norms of (3,2) differ -- 7 (hex) vs 13 (square)",
          N_eisen(N_fam, 2) != N_gauss(N_fam, 2))
    # generic splits {b,s} (b<=s) with b+s=5 do not give the whole table;
    # the norms are symmetric, so {1,4} and {2,3} are the only two multisets.
    splits = {(b, 5 - b): (N_eisen(b, 5 - b), N_gauss(b, 5 - b))
              for b in range(1, 3)}            # {1,4} and {2,3}
    hits = [bs for bs, pair in splits.items() if pair == (SCALARON, DELTA_Q)]
    check("NEG: among the splits {1,4},{2,3} only {2,3} gives (N_omega,N_i)=(7,13) "
          "-- {1,4} gives (13,17); the carrier split (colour 3, weak 2) is rigid",
          hits == [(2, 3)] and splits[(1, 4)] == (13, 17))

    return summary("v222 CM-norm duality (square 41/13, hexagon 7)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
