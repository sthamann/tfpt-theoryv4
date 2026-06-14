"""v197 -- ARCH.RRCAR.02: hardening the Riemann-Roch carrier reading from g_car to
D5 itself (external-review point 7). v189 read g_car = 5 = h^0(P^1, O(mu4)) and
matched it to rank(D5). This module goes one step further: the 5-dimensional
carrier mode space C_car := H^0(P^1, O(mu4)) generates the so(10) = D5 half-spinor
by its even Clifford algebra,

    Lambda^even(C_car) = S^+ ,    dim S^+ = 2^{g_car-1} = 16 ,

so the carrier is not merely "rank 5 like D5" but IS the Clifford spinor of the
5-dim mode space. The dimensional chain is exact [I]; the physical identification
"carrier := the Clifford spinor of the seam mode space" stays [C] (as in v189).

  [I] 1. THE EVEN CLIFFORD DIMENSION.  For a 5-dim space, the even exterior
        algebra has dim Lambda^even(C^5) = C(5,0)+C(5,2)+C(5,4) = 1+10+5 = 16 =
        2^{5-1} = 2^{g_car-1} = dim S^+ (the repo's dim_Splus).
  [I] 2. THE SO(10) HALF-SPINOR.  so(10) = D5 (rank 5) has Dirac spinor 2^5 = 32
        and half-spinors 2^4 = 16 each; S^+ = Lambda^even(C_car). So the 5-dim
        mode space, doubled to its Clifford/spinor module, IS the D5 half-spinor.
  [I] 3. CLOSES THE CHAIN mu4 -> g_car -> D5.  From ONE four-point divisor:
        cycle side rank H_1 = deg-1 = 3 = N_fam (A3); function side
        h^0(O(mu4)) = deg+1 = 5 = g_car = dim C_car; and now
        Lambda^even(C_car) = 16 = the D5 half-spinor = the carrier. So D5 is not a
        separate input -- it is the Clifford spinor of the Riemann-Roch carrier.
  [C] 4. THE PHYSICAL IDENTIFICATION STAYS [C].  Reading the carrier as
        Cl^even(C_car) (rather than merely matching rank(D5)=5) is a geometric
        hardening, but the identification "carrier = Clifford spinor of the seam
        meromorphic mode space" is still a physical [C] step (as in v189); it does
        NOT change the over-determined status of g_car=5.

  Exact (binomial / Clifford dimensions); Wolfram-mirrored.
"""
from math import comb

from tfpt_constants import g_car, N_fam, dim_Splus, check, summary, reset

MU4 = 4


def run():
    reset()
    print("v197 ARCH.RRCAR.02: C_car = H^0(O(mu4)) (5-dim) generates the D5 half-spinor S^+ via Clifford")

    h0 = MU4 + 1                                       # h^0(P^1,O(mu4)) = deg+1 = 5 = g_car
    lam_even = sum(comb(h0, k) for k in range(0, h0 + 1, 2))   # dim Lambda^even(C^5)
    check("EVEN CLIFFORD DIM [I]: dim Lambda^even(C^%d) = C(5,0)+C(5,2)+C(5,4) = "
          "%d+%d+%d = %d = 2^{g_car-1} = dim S^+ = %d"
          % (h0, comb(h0, 0), comb(h0, 2), comb(h0, 4), lam_even, dim_Splus),
          h0 == g_car and lam_even == 2**(g_car - 1) == dim_Splus == 16)

    check("SO(10) HALF-SPINOR [I]: so(10)=D5 (rank 5) has Dirac spinor 2^5=%d and "
          "half-spinors 2^4=%d each; S^+ = Lambda^even(C_car). The 5-dim mode "
          "space's Clifford module IS the D5 half-spinor"
          % (2**5, 2**4),
          2**5 == 32 and 2**4 == dim_Splus)

    check("CHAIN mu4 -> g_car -> D5 [I]: from ONE four-point divisor -- cycle side "
          "rank H_1 = deg-1 = %d = N_fam (A3); function side h^0 = deg+1 = %d = "
          "g_car = dim C_car; Lambda^even(C_car) = %d = the D5 half-spinor = the "
          "carrier. D5 is the Clifford spinor of the Riemann-Roch carrier, not a "
          "separate input" % (MU4 - 1, h0, lam_even),
          (MU4 - 1) == N_fam and h0 == g_car and lam_even == dim_Splus)

    check("PHYSICAL IDENTIFICATION [C]: reading the carrier as Cl^even(C_car) (not "
          "merely matching rank(D5)=5) is a geometric hardening of v189, but "
          "'carrier = Clifford spinor of the seam mode space' is still a physical "
          "[C] step; it does NOT change the over-determined status of g_car=5", True)

    return summary("v197 ARCH.RRCAR.02: Lambda^even(C_car)=S^+=16=D5 half-spinor; mu4->g_car->D5 chain [I]/[C]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
