"""v189 -- The Riemann-Roch carrier reading (external-review proposal, point 1):
the five-slot carrier and the three families are the two canonical invariants of
ONE object, the four-point seam divisor D = mu4 on P^1. The arithmetic is exact
[E]; the *identification* 'carrier = the meromorphic mode space H^0(P^1, O(mu4))'
is a [C] geometric reading (it does NOT replace the over-determined g_car=5 of the
Pascal/bootstrap/Lean route -- it adds a fourth, geometric reading, and it is
matched by rank(D5)=5).

  [E] 1. THE DIVISOR HAS TWO CANONICAL INVARIANTS.  For D = mu4 (degree
        |mu4| = 4) on P^1, Riemann-Roch gives the function side
        h^0(P^1, O(D)) = deg D + 1 = 5, and the cycle side is
        rank H_1(P^1 \\ D) = deg D - 1 = 3.  So from ONE four-point object:
        g_car = |mu4| + 1 = 5  and  N_fam = |mu4| - 1 = 3.
  [E] 2. BOTH MATCH THE COMPILER PRIMITIVES.  g_car = 5 = rank(D5) (the carrier
        is the so(10) half-spinor, rank D5 + rank A3 = 5 + 3 = 8 = rank E8, v1),
        and N_fam = 3 is the homology side already closed as QGEO.COHOM.01
        (n(P^1\\mu4) = C.w1 + C.w2 + C.w3, the eigenforms z^{k-1}dz/(z^4-1), v177).
  [C] 3. THE CARRIER READING (geometric, conjectural identification).  Under
        QGEO.SYM.01 the carrier is read as the space of meromorphic seam-boundary
        modes with at most simple poles on the mu4 divisor: C_car ~= H^0(P^1,
        O(mu4)), dim = 5.  This is more natural than 'five slots' (less number,
        more geometry), BUT the identification 'carrier = this mode space' is a
        physical [C] step, not derived.  It does NOT weaken P2: g_car=5 stays
        OVER-determined (Pascal 2*5=C(5,2)=10 v2; bootstrap forced three ways v6;
        Lean FORM.LADDER.01).  Honest scope: h^0 and rank H_1 are BOTH fixed by
        deg=4, so this is ONE object read two ways (a unification), not two
        independent confirmations.

  Exact (integer Riemann-Roch / homology); Wolfram-mirrored.
"""
from tfpt_constants import g_car, N_fam, dim_Splus, check, summary, reset

MU4 = 4                       # |mu4| = deg D = number of seam marks
RANK_D5 = 5                   # carrier = so(10) half-spinor, rank 5 (v1)


def h0_P1(deg):
    """h^0(P^1, O(deg)) = deg+1 for deg >= 0 (Riemann-Roch on P^1, h^1=0)."""
    return deg + 1 if deg >= 0 else 0


def rank_H1_punctured_P1(n_points):
    """rank H_1(P^1 minus n points) = n - 1 (pi_1 free on n-1 generators)."""
    return n_points - 1


def run():
    reset()
    print("v189 Riemann-Roch carrier: (g_car, N_fam) = (5,3) are the two invariants of the mu4 divisor")

    h0 = h0_P1(MU4)
    rkH1 = rank_H1_punctured_P1(MU4)
    check("DIVISOR INVARIANTS [E]: for D=mu4 (deg %d) on P^1, h^0(P^1,O(D)) = "
          "deg+1 = %d (function side) and rank H_1(P^1\\D) = deg-1 = %d (cycle "
          "side); so g_car = |mu4|+1 and N_fam = |mu4|-1 from ONE object"
          % (MU4, h0, rkH1),
          h0 == 5 and rkH1 == 3)

    check("FUNCTION SIDE = CARRIER [E]: h^0(P^1,O(mu4)) = %d = g_car = rank(D5) "
          "(the carrier is the so(10) half-spinor, rank D5 + rank A3 = 5+3 = 8 = "
          "rank E8, v1)" % h0,
          h0 == g_car == RANK_D5)

    check("CYCLE SIDE = FAMILIES [E]: rank H_1(P^1\\mu4) = %d = N_fam, the "
          "homology side already closed as QGEO.COHOM.01 (n = C.w1+C.w2+C.w3, "
          "eigenforms z^{k-1}dz/(z^4-1), v177)" % rkH1,
          rkH1 == N_fam == 3)

    # consistency: same object, deg fixes both; N_fam = (dim S+ - 1)/g_car cross-check
    check("ONE OBJECT, TWO INVARIANTS [E]: both h^0 and rank H_1 are fixed by "
          "deg=|mu4|=4 (a unification, not two independent checks); cross-check "
          "N_fam = (dim S+ - 1)/g_car = (%d-1)/%d = %d agrees"
          % (dim_Splus, g_car, (dim_Splus - 1) // g_car),
          (dim_Splus - 1) // g_car == rkH1 == N_fam)

    check("CARRIER READING [C]: 'C_car ~= H^0(P^1,O(mu4)), dim 5' is a geometric "
          "reading (less number, more geometry), matched by rank(D5)=5; the "
          "identification 'carrier = this mode space' is a physical [C] step, NOT "
          "derived, and does NOT replace the over-determined g_car=5 (Pascal v2, "
          "bootstrap v6, Lean) -- it is a fourth, geometric reading", True)

    return summary("v189 Riemann-Roch carrier: (g_car,N_fam)=(5,3) as the two invariants of the mu4 divisor")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
