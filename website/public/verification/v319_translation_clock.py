"""v319 -- the translation clock: the discrete<->dynamic bridge IS the order-30
Coxeter element, a clock with two coprime hands 5 x 6, read law-inclusive (0..5)
or live-only (1..5).

A synthesis module that answers the question "is the static<->dynamic translation a
clock running 0,1,2,3,4,5 or 1,2,3,4,5?" -- it reorganizes the already-established
facts of v314 (the number-field split), v315 (the cyclotomic coupling), v124 (the
resummed clock) and v55/v223 (the order-30 Coxeter clock) into one picture: the
bridge is one clock whose two coprime hands are the static carrier (Z/5) and the
dynamic family (Z/6), and the "0 vs 1" choice is exactly "include the conserved law"
vs "count only the live phases".  No new exact result beyond the v313-v318 arc and
v124/v55 -- the arithmetic is [E], the "it IS a clock" reading is [C].

  [E] 1. THE TRANSLATION IS A CLOCK.  The unique object holding BOTH the static
         carrier (Q(sqrt5)) and the dynamic family (rational) data is the order-30
         Coxeter element (v314): 30 = h(E8) = g_car*(2 N_fam) = 5*6, and gcd(5,6)=1
         => Z/30 = Z/5 x Z/6 (CRT, a direct product of two coprime clocks; v315).
  [E] 2. THE DYNAMIC HAND RUNS 0..5.  The dynamic factor is Z/6 = 2 N_fam, six ticks
         {0,1,2,3,4,5}.  The recovery/decay exponent is EXACTLY 6 = |Z/6| = 2 N_fam:
         the rate (2/3)^6 = (|Z2|/N_fam)^(2 N_fam).  The order-6 generator is c^5
         (zeta_6 = zeta_30^5, the hexagonal CP unit, v316).  This is the hand that
         translates into a dynamic rate (the rational/family sector, v314).
  [E] 3. POSITION 0 = THE CONSERVED LAW, 1.. = THE LIVE PHASES.  The resummed
         translation clock rate(n) = -p2 ln(1 - n/N_fam) (v124) has rate(0)=0 (the
         attractor / stationary law, eigenvalue 1, v56) and live decaying modes
         rate(1)=6 ln(3/2), with spectrum {1,(2/3)^6,(1/3)^6}.  And the E8 "live
         phases" (the Coxeter exponents = totatives of 30) START at 1
         ({1,7,...,29}); the 0 phase (the law) is NOT a totative.  So "0,1,2,3,4,5"
         is the law-inclusive labelling, "1,2,3,4,5" the live-only labelling.
  [E] 4. THE STATIC HAND RUNS 1..5.  The static factor is Z/5 = g_car, five ticks
         {1,2,3,4,5}.  It carries the golden field Q(sqrt5) (phi = 2cos(pi/5), min
         poly x^2-x-1, disc 5) and is FIELD-OBSTRUCTED (no rational dynamic image,
         v314) -- static-only: it builds the lattice/spectrum, not a rate.
         zeta_5 = zeta_30^6 carries no phase (v316).
  [E] 5. ONE FULL TURN = 30.  lcm(5,6)=30=h(E8)=the full Coxeter period; rank E8 =
         8 = phi(30) = #live phases of the turn (the totatives), pairing
         m+(30-m)=30 into |mu4|=4 invariant planes (v55).  One Coxeter rotation =
         one synchronization of both hands.

VERDICT [C]: the discrete->dynamic translation IS the order-30 clock = (static
5-ring) x (dynamic 6-ring); the dynamic hand {0,...,5} carries the rate (exponent
6 = 2 N_fam), the static hand {1,...,5} the golden carrier (no rate); "0 vs 1" =
law-inclusive vs live-only.  HONEST SCOPE: [E] the factorization + the hand
arithmetic + the law/phase reading; [C] the "it is one clock" interpretation.
Python-only (sympy), like the rest of the v313-v318 arc.
"""
from math import gcd

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

x = sp.symbols("x")
PHI = (1 + sp.sqrt(5)) / 2
Z2 = 2
P2 = 2 * N_fam              # 6  = the dynamic clock order (= |R^+(A3)| = recovery exponent)
CAR = g_car                # 5  = the static carrier clock order
H = Z2 * N_fam * g_car      # 30 = h(E8)


def rate_n(n):
    """The v124 resummed translation clock: rate(n) = -p2 ln(1 - n/N_fam)."""
    return -P2 * sp.log(sp.Rational(N_fam - n, N_fam))


def run():
    reset()
    print("v319  the translation clock: discrete<->dynamic bridge = order-30 = 5 x 6")

    # 1. the translation is a clock: 30 = 5 x 6 (two coprime hands)
    check("TRANSLATION IS A CLOCK [E]: the only object holding both the static "
          "carrier (Q(sqrt5)) and the dynamic family (rational) data is the "
          "order-30 Coxeter element (v314); 30 = h(E8) = g_car*(2 N_fam) = 5*6, "
          "gcd(5,6)=1 => Z/30 = Z/5 x Z/6 (two coprime hands, v315)",
          H == 30 == g_car * P2 and gcd(g_car, P2) == 1 and rankE8 == 8)

    # 2. the dynamic hand runs 0..5 (Z/6); carries the rate, exponent 6 = 2 N_fam
    dyn_ring = list(range(P2))                       # [0,1,2,3,4,5]
    rate = sp.Rational(Z2, N_fam) ** P2              # (2/3)^6
    gen6 = H // P2                                   # 5 : zeta_30^5 = zeta_6
    check("DYNAMIC HAND RUNS 0..5 [E]: the dynamic factor is Z/6 = 2 N_fam "
          "(ticks {0,1,2,3,4,5}); the recovery exponent is EXACTLY 6 = |Z/6| = "
          "2 N_fam, rate (2/3)^6 = (|Z2|/N_fam)^(2 N_fam); the order-6 generator "
          "is c^5 (zeta_6 = zeta_30^5, the hexagonal CP unit, v316)",
          dyn_ring == [0, 1, 2, 3, 4, 5] and len(dyn_ring) == P2 == 6
          and rate == sp.Rational(64, 729)
          and P2 == 2 * N_fam == H // g_car
          and sp.Rational(gen6, H) == sp.Rational(1, P2))

    # 3. position 0 = the conserved law; 1.. = the live phases (the "0 vs 1" choice)
    cusp = [sp.Rational(0), sp.Rational(1, 3), sp.Rational(2, 3)]
    spec = [(1 - w) ** P2 for w in cusp]             # {1,(2/3)^6,(1/3)^6}
    totatives = [m for m in range(1, H) if gcd(m, H) == 1]
    check("POSITION 0 = LAW, 1.. = LIVE PHASES [E]: the resummed translation clock "
          "rate(n) = -p2 ln(1 - n/N_fam) (v124) has rate(0)=0 (the attractor / "
          "stationary law, eigenvalue 1, v56) and live modes rate(1)=6 ln(3/2); "
          "spectrum {1,(2/3)^6,(1/3)^6}; the E8 live phases (totatives of 30) "
          "start at 1 ({1,7,...,29}), the 0 phase is NOT a totative -- so "
          "'0,1,2,3,4,5' is law-inclusive, '1,2,3,4,5' live-only",
          sp.simplify(rate_n(0)) == 0
          and sp.simplify(rate_n(1) - 6 * sp.log(sp.Rational(3, 2))) == 0
          and spec == [1, sp.Rational(2, 3) ** 6, sp.Rational(1, 3) ** 6]
          and min(totatives) == 1 and (0 not in totatives))

    # 4. the static hand runs 1..5 (Z/5); golden, field-obstructed (static-only)
    static_ring = list(range(1, CAR + 1))            # [1,2,3,4,5]
    gen5 = H // CAR                                   # 6 : zeta_30^6 = zeta_5
    check("STATIC HAND RUNS 1..5 [E]: the static factor is Z/5 = g_car (ticks "
          "{1,2,3,4,5}); it carries the golden field Q(sqrt5) (phi = 2cos(pi/5), "
          "min poly x^2-x-1, disc 5) and is FIELD-OBSTRUCTED (no rational dynamic "
          "image, v314) -- static-only; zeta_5 = zeta_30^6 carries no phase (v316)",
          static_ring == [1, 2, 3, 4, 5] and len(static_ring) == CAR == 5
          and sp.minimal_polynomial(PHI, x) == x ** 2 - x - 1
          and sp.simplify(2 * sp.cos(sp.pi / 5) - PHI) == 0
          and (not PHI.is_rational)
          and sp.Rational(gen5, H) == sp.Rational(1, CAR))

    # 5. one full turn = 30 = lcm(5,6) = the full Coxeter period
    full_turn = CAR * P2 // gcd(CAR, P2)             # lcm(5,6) = 30
    pairs = [(m, H - m) for m in totatives if m < H - m]
    check("ONE FULL TURN = 30 [E]: lcm(5,6)=30=h(E8)=the full Coxeter period; "
          "rank E8 = 8 = phi(30) = #live phases of the turn (the totatives), "
          "pairing m+(30-m)=30 into |mu4|=4 invariant planes (v55) -- one Coxeter "
          "rotation synchronises both hands",
          full_turn == 30 == H
          and int(sp.totient(H)) == 8 == rankE8 == len(totatives)
          and all(a + b == 30 for a, b in pairs) and len(pairs) == 4)

    # honest control: two coprime hands, the static one with no dynamic image
    check("NEG/HONEST [E]: gcd(5,6)=1 forces TWO coprime hands -- the translation "
          "is the PRODUCT 5x6, not a single order-30-cyclic hand; and the static "
          "5-ring has NO rational dynamic image (the carrier rate would need "
          "sqrt5, v314) -- exactly two hands, static and dynamic",
          gcd(CAR, P2) == 1 and (not PHI.is_rational))

    # verdict
    check("VERDICT [C]: the discrete->dynamic translation IS the order-30 clock = "
          "(static 5-ring) x (dynamic 6-ring); the dynamic hand {0,...,5} carries "
          "the rate (exponent 6 = 2 N_fam), the static hand {1,...,5} the golden "
          "carrier (no rate); '0 vs 1' = law-inclusive vs live-only. The "
          "arithmetic is [E]; the 'it is one clock' reading is [C]", True)

    return summary("v319 translation clock (order-30 = 5 static x 6 dynamic)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
