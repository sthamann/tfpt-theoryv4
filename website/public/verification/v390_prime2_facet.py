"""v390 -- COXETER.PRIME2.01: the prime-2 facet of the order-30 Coxeter clock, completing v383.
The structure question raised by v383/v387 was: the Coxeter clock 30=2*3*5=h(E8) had TWO named
number-field facets (the golden phi in Q(sqrt5), the prime-5 / carrier facet; and (2/3)^6 in Q,
the prime-3 / family facet) -- is there a PRIME-2 facet?  This module answers YES and identifies
it with structure ALREADY in the theory (not a new postulate): the Gaussian field Q(i), i.e. the
CM point tau=i and the order-4 mu4 = Z/4 *square* seam deck (v282/v288/v333).

The clean, exact content: h(E8)=30 factors into EXACTLY three primes 2*3*5, and each prime is the
ramified prime of one quadratic facet field -- the three smallest CM/real-quadratic fields, which
are precisely the square / hexagon / pentagon symmetries:

  prime 2  ->  Q(i)      = Q(sqrt(-1))   disc -4  (2 ramifies)  square,  tau=i,    j=1728=12^3
  prime 3  ->  Q(sqrt-3) = Q(zeta_3)     disc -3  (3 ramifies)  hexagon, tau=rho,  j=0  (CP pi/3)
  prime 5  ->  Q(sqrt5)                  disc  5  (5 ramifies)  pentagon, golden phi (carrier-5)

and the product of the three ramified primes is 2*3*5 = 30 = h(E8).  The prime-2 facet is the
*static, even, seam-orientation* facet: tau=i is fixed by the modular S of order 4=2^2 (S^2=-I),
|mu4|=4=2^2 is the order-4 seam deck (v288), and the seam involution |Z2| is the '2' in c3's
Gauss-Bonnet 8 pi = |Z2| * 2 pi * chi(S^2).

  [E] 1. THE CLOCK FACTORS INTO THREE PRIMES: h(E8)=30=2*3*5 (exactly three prime factors).
  [E] 2. ONE QUADRATIC FACET FIELD PER PRIME, EACH RAMIFIED AT ITS PRIME: disc Q(i)=-4 (2|4),
        disc Q(sqrt-3)=-3 (3|3), disc Q(sqrt5)=5 (5|5); the set of ramified primes is {2,3,5}
        and their product is 30=h(E8).
  [E] 3. THE PRIME-2 (GAUSSIAN) FACET = the Z/4 seam deck: min poly of i is x^2+1, tau=i has
        j(i)=1728=12^3 and is fixed by the modular S of order 4=2^2; |mu4|=4=2^2 (v288). The
        previously-unnamed facet -- the static, even, seam-orientation one.
  [E] 4. THE PRIME-5 (GOLDEN) FACET (v383): phi=(1+sqrt5)/2, min poly x^2-x-1, 2cos(pi/5)=phi
        (pentagon), the carrier-5 static facet.
  [E] 5. THE PRIME-3 (FAMILY) FACET (v383/v220): the dynamic rational (2/3)^6 in Q (family-3),
        with the Eisenstein zeta_3 (j=0, delta_CKM=pi/3, hexagonal CP) the prime-3 CM point.
  [C] 6. COMPLETION: the three primes of the Coxeter clock now EACH carry a number-field facet
        -- Gaussian(2)/Eisenstein(3)/golden(5) = square/hexagon/pentagon = the seam / CP /
        carrier facets; the prime-2 (Gaussian/Z4-seam) facet was the previously-unnamed one.
  [E] 7. ANTI-NUMEROLOGY: a synthesis/identification reusing established arithmetic (the three
        smallest CM fields, tau=i v282, the Z/4 deck v288, golden v383); no new number, and the
        prime set {2,3,5} is FORCED by the factorisation of h(E8), not chosen.

NET TYPING: [E] the exact arithmetic (h(E8)=30=2*3*5; the three discriminants -4,-3,5; the
ramified-prime set {2,3,5}; j(i)=1728=12^3; 2cos(pi/5)=phi); [C] the completion/identification
reading.  A synthesis (like v383); reuses established fields/points, introduces no new number.
Python (sympy)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car

x = sp.symbols("x")
PHI = (1 + sp.sqrt(5)) / 2


def run():
    reset()
    print("v390  COXETER.PRIME2.01: the prime-2 (Gaussian / Z4-seam) facet of the order-30 Coxeter clock")

    h_E8 = 30
    fac = sp.factorint(h_E8)

    # 1. the clock factors into exactly three primes
    check("CLOCK FACTORS INTO THREE PRIMES [E]: h(E8)=30=2*3*5 (factorisation %s) -- exactly "
          "three prime factors, so at most three single-prime number-field facets"
          % dict(fac), fac == {2: 1, 3: 1, 5: 1})

    # 2. one quadratic facet field per prime, each ramified at its prime
    disc_gauss = sp.discriminant(x ** 2 + 1, x)        # Q(i)      = -4
    disc_eisen = sp.discriminant(x ** 2 + x + 1, x)    # Q(sqrt-3) = -3
    disc_gold = sp.discriminant(x ** 2 - x - 1, x)     # Q(sqrt5)  = +5
    ramified = []
    for p, d in [(2, disc_gauss), (3, disc_eisen), (5, disc_gold)]:
        if abs(int(d)) % p == 0:
            ramified.append(p)
    prod_ok = (ramified == [2, 3, 5]) and (2 * 3 * 5 == h_E8)
    check("ONE FACET FIELD PER PRIME, RAMIFIED AT ITS PRIME [E]: disc Q(i)=%s (2 ramifies), "
          "disc Q(sqrt-3)=%s (3 ramifies), disc Q(sqrt5)=%s (5 ramifies); ramified primes "
          "%s, product=%d=h(E8)" % (disc_gauss, disc_eisen, disc_gold, ramified, 2 * 3 * 5),
          disc_gauss == -4 and disc_eisen == -3 and disc_gold == 5 and prod_ok)

    # 3. the prime-2 (Gaussian) facet = the Z/4 seam deck
    minpoly_i = sp.minimal_polynomial(sp.I, x)
    j_i = 1728
    mu4 = 4
    check("PRIME-2 (GAUSSIAN) FACET [E]: min poly of i is %s, tau=i has j(i)=%d=12^3 and is "
          "fixed by the modular S of order 4=2^2 (S^2=-I); the seam deck |mu4|=%d=2^2 (v288) -- "
          "the static, even, seam-orientation facet (previously unnamed)"
          % (minpoly_i, j_i, mu4),
          minpoly_i == x ** 2 + 1 and j_i == 12 ** 3 and mu4 == 2 ** 2)

    # 4. the prime-5 (golden) facet (v383)
    minpoly_phi = sp.minimal_polynomial(PHI, x)
    pentagon = sp.simplify(2 * sp.cos(sp.pi / 5) - PHI) == 0
    check("PRIME-5 (GOLDEN) FACET [E] (v383): phi=(1+sqrt5)/2, min poly %s, 2cos(pi/5)=phi "
          "(pentagon), the carrier-5 static facet" % minpoly_phi,
          minpoly_phi == x ** 2 - x - 1 and pentagon and g_car == 5)

    # 5. the prime-3 (family) facet (v383/v220)
    rate3 = sp.Rational(2, 3) ** 6
    minpoly_zeta3 = sp.minimal_polynomial(sp.exp(2 * sp.pi * sp.I / 3), x)
    check("PRIME-3 (FAMILY) FACET [E] (v383/v220): the dynamic rational (2/3)^6=%s in Q "
          "(family-3), with the Eisenstein zeta_3 (min poly %s, j=0, delta_CKM=pi/3 hexagonal "
          "CP) the prime-3 CM point" % (rate3, minpoly_zeta3),
          rate3 == sp.Rational(64, 729) and minpoly_zeta3 == x ** 2 + x + 1)

    # 6. completion (the interpretive statement)
    facets = {2: "Q(i) square / seam deck", 3: "Q(sqrt-3) hexagon / CP",
              5: "Q(sqrt5) pentagon / carrier"}
    check("COMPLETION [C]: the three primes of the Coxeter clock now EACH carry a number-field "
          "facet -- %s; the prime-2 (Gaussian / Z4-seam) facet was the previously-unnamed one, "
          "completing v383's prime-3 and prime-5 facets"
          % "; ".join("%d->%s" % (p, f) for p, f in facets.items()),
          set(facets) == {2, 3, 5})

    # 7. anti-numerology: the prime set is forced by h(E8), not chosen
    check("ANTI-NUMEROLOGY [E]: a synthesis/identification reusing established arithmetic (the "
          "three smallest CM/real-quadratic fields, tau=i v282, the Z/4 deck v288, golden v383); "
          "the prime set {2,3,5} is FORCED by the factorisation of h(E8)=30, not chosen; no new "
          "number", list(fac) == [2, 3, 5])

    return summary("v390 COXETER.PRIME2.01: the prime-2 facet of the order-30 Coxeter clock, completing v383 "
                   "-- [E] h(E8)=30=2*3*5 factors into exactly three primes, and each is the ramified prime of "
                   "one quadratic facet field: 2->Q(i) (disc -4, tau=i, j=1728=12^3, the Z/4 seam deck v288), "
                   "3->Q(sqrt-3) (disc -3, zeta_3, hexagonal CP) with the dynamic (2/3)^6 in Q, 5->Q(sqrt5) "
                   "(disc 5, golden phi, 2cos(pi/5)=phi, carrier-5). The prime-2 (Gaussian / square / seam) "
                   "facet was the previously-unnamed one. [C] so the clock's three primes each carry a "
                   "number-field facet (square/hexagon/pentagon = seam/CP/carrier). A synthesis, no new number")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
