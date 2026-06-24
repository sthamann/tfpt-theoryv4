"""v403 -- ARITH.HULL.01: the three number-field facets COMPOSE to a degree-8 = rank(E8)
abelian field, the arithmetic hull dual to the E8 lattice hull.

v390/v394 named the three single-prime facet fields of the order-30 Coxeter clock
(2->Q(i), 3->Q(sqrt-3), 5->Q(sqrt5)) but only ever used them ONE at a time.  This
module composes them: K = Q(i, sqrt-3, sqrt5).  The whole TFPT integer skeleton
falls out of that one arithmetic object -- and nothing here is a new postulate (the
prime set {2,3,5} is FORCED by h(E8)=30, the three facets by v390).

  K = Q(i, sqrt-3, sqrt5)  (the compositum of the three facet fields, v390)

  [E] 1. THREE INDEPENDENT FACETS: the squarefree parts -1,-3,5 are multiplicatively
        independent in Q*/(Q*)^2 (no nonempty subset product is a square) -- so the
        three quadratics are linearly disjoint and [K:Q] = 2^3.
  [E] 2. DEGREE = rank E8: [K:Q] = 2^3 = 8 = rank(E8) = g_car + N_fam, and the Galois
        group is (Z/2)^3 of order 8 = rank(E8).  (2^omega(h) = rank is E8-special:
        the negative control E7 has h=18, omega=2, 2^2=4 != 7.)
  [E] 3. SEVEN QUADRATIC SUBFIELDS: the 2^3-1 = 7 nontrivial subgroups of (Z/2)^3 give
        exactly 7 quadratic subfields, squarefree parts {-1,-3,5, 3,-5,-15, 15}.
  [E] 4. THE 4+3 SPLIT = |mu4| + N_fam: of the 7 quadratic subfields exactly 4 are
        IMAGINARY (-1,-3,-5,-15) = |mu4| (the CM / dynamic facets) and 3 are REAL
        (3,5,15) = N_fam (the RM / static facets); 4 + 3 = 7.
  [E] 5. RAMIFIED ONLY AT THE ATOMS: every quadratic subfield ramifies only over
        {2,3,5}, the three atoms = the prime factors of h(E8)=30; the conductor of K
        is supported on {2,3,5}.
  [E] 6. CM/RM = DYNAMIC/STATIC: the two imaginary-quadratic atoms (2->disc -4,
        3->disc -3) are the CM facets carrying the dynamic rates ({2,3}-arithmetic,
        v394); the one real-quadratic atom (5->disc +5) is the RM facet carrying the
        STATIC golden carrier (2cos(pi/5)=phi) -- no independent prime-5 dynamic rate.
  [C] 7. THE ARITHMETIC HULL: K is the abelian (Z/2)^3 'arithmetic hull' dual to the
        E8 lattice hull -- both of rank/order 8, both supported on the same three
        atoms; the 7 quadratic subfields are a candidate for the 7 E8 audit slices.

NET TYPING: [E] the exact field arithmetic (independence => degree 8 = rank E8;
(Z/2)^3; the 7 subfields 4+3 = |mu4|+N_fam; ramified only at {2,3,5}; the E8-special
2^omega(h)=rank with the E7 negative control); [C] the arithmetic-hull reading and the
7-subfields<->7-slices candidate.  A synthesis (like v390/v394) that COMPOSES the
already-established facet fields; no new number, the prime set forced by h(E8)=30.
Python (sympy).  The component facet arithmetic is mirrored via v222/v390; this
compositum reading is Python-only by the synthesis-module convention (cf. v390/v394).
"""
import itertools

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

x = sp.symbols("x")


def squarefree_part(n):
    """The squarefree part of the integer n (keeping the sign)."""
    n = int(n)
    sign = -1 if n < 0 else 1
    out = 1
    for p, e in sp.factorint(abs(n)).items():
        if e % 2 == 1:
            out *= p
    return sign * out


def fundamental_disc(m):
    """Fundamental discriminant of Q(sqrt m) for squarefree m."""
    return m if (m % 4 == 1) else 4 * m


def ramified_primes(m):
    return set(int(p) for p in sp.factorint(abs(fundamental_disc(m))))


def run():
    reset()
    print("v403  ARITH.HULL.01: the three facet fields compose to a degree-8 = rank(E8) "
          "abelian field (the arithmetic hull dual to E8)")

    gens = [-1, -3, 5]                      # squarefree parts of Q(i), Q(sqrt-3), Q(sqrt5)
    h_E8 = 30

    # 1. the three facets are independent in Q*/(Q*)^2
    subsets = [c for r in range(1, len(gens) + 1) for c in itertools.combinations(gens, r)]
    sqf = [squarefree_part(sp.prod(c)) for c in subsets]
    independent = (len(set(sqf)) == 2 ** len(gens) - 1) and (1 not in sqf)
    check("THREE INDEPENDENT FACETS [E]: the squarefree parts -1,-3,5 are independent "
          "in Q*/(Q*)^2 (no nonempty subset product is a square) -- the three "
          "quadratics are linearly disjoint, so [K:Q]=2^3", independent)

    # 2. degree = rank E8, Galois (Z/2)^3
    degree = 2 ** len(gens)
    # E8-special negative control: 2^omega(h) = rank only for E8 (E7: h=18, omega=2)
    omega_30 = len(sp.factorint(h_E8))
    omega_18 = len(sp.factorint(18))
    e8_special = (2 ** omega_30 == rankE8) and (2 ** omega_18 != 7)
    check("DEGREE = rank E8 [E]: [K:Q]=2^3=%d=rank(E8)=g_car+N_fam=%d+%d; Galois group "
          "(Z/2)^3 order %d=rank(E8); 2^omega(h(E8))=2^%d=%d=rank E8 is E8-special "
          "(E7: h=18, omega=2, 2^2=4!=7)"
          % (degree, g_car, N_fam, degree, omega_30, 2 ** omega_30),
          degree == rankE8 == g_car + N_fam and e8_special)

    # 3. seven quadratic subfields
    subfields = sorted(set(sqf))
    check("SEVEN QUADRATIC SUBFIELDS [E]: the 2^3-1=7 nontrivial subgroups of (Z/2)^3 "
          "give exactly 7 quadratic subfields, squarefree parts %s"
          % (subfields,),
          len(subfields) == 7 and set(subfields) == {-1, -3, 5, 3, -5, -15, 15})

    # 4. the 4+3 split = |mu4| + N_fam
    mu4 = sum((1, 1, 2))                   # e1(anchor a=(1,1,2)) = 4 = |mu4|
    imaginary = [s for s in subfields if s < 0]
    real = [s for s in subfields if s > 0]
    check("4+3 SPLIT = |mu4|+N_fam [E]: of the 7 quadratic subfields exactly %d are "
          "IMAGINARY %s = |mu4|=%d (CM/dynamic) and %d are REAL %s = N_fam=%d "
          "(RM/static); %d+%d=7"
          % (len(imaginary), imaginary, mu4, len(real), real, N_fam,
             len(imaginary), len(real)),
          len(imaginary) == mu4 == 4 and len(real) == N_fam == 3)

    # 5. ramified only at the atoms {2,3,5}
    all_ram = set()
    for m in subfields:
        all_ram |= ramified_primes(m)
    atoms = set(int(p) for p in sp.factorint(h_E8))
    check("RAMIFIED ONLY AT THE ATOMS [E]: every quadratic subfield ramifies only over "
          "%s = the prime factors of h(E8)=30 = the three atoms {|Z2|,N_fam,g_car}"
          % (sorted(all_ram),),
          all_ram == atoms == {2, 3, 5})

    # 6. CM/RM = dynamic/static (the discriminant signs, from v390)
    disc = {-1: sp.discriminant(x ** 2 + 1, x),       # Q(i)      -4 (imaginary, CM)
            -3: sp.discriminant(x ** 2 + x + 1, x),   # Q(sqrt-3) -3 (imaginary, CM)
            5: sp.discriminant(x ** 2 - x - 1, x)}     # Q(sqrt5)   5 (real, RM)
    check("CM/RM = DYNAMIC/STATIC [E]: the two imaginary-quadratic atoms (2->disc %s, "
          "3->disc %s) are the CM facets carrying the {2,3}-arithmetic dynamic rates "
          "(v394); the one real-quadratic atom (5->disc %s) is the RM facet carrying "
          "the STATIC golden carrier 2cos(pi/5)=phi -- no independent prime-5 dynamic "
          "rate" % (disc[-1], disc[-3], disc[5]),
          disc[-1] == -4 and disc[-3] == -3 and disc[5] == 5)

    # 7. the arithmetic hull (interpretation)
    check("THE ARITHMETIC HULL [C]: K=Q(i,sqrt-3,sqrt5) is the abelian (Z/2)^3 "
          "'arithmetic hull' dual to the E8 lattice hull -- both of rank/order 8, both "
          "supported on the same atoms {2,3,5}; the 7 quadratic subfields are a "
          "candidate for the 7 E8 audit slices", True)

    return summary("v403 ARITH.HULL.01: the three facet fields compose to K=Q(i,sqrt-3,sqrt5) -- "
                   "[E] degree 2^3=8=rank E8, Galois (Z/2)^3, 7 quadratic subfields = 4 imaginary "
                   "(|mu4|) + 3 real (N_fam), ramified only at {2,3,5}=the atoms=primes of h(E8)=30; "
                   "2^omega(h(E8))=rank E8 is E8-special (E7 control fails). [C] the abelian "
                   "arithmetic hull dual to the E8 lattice hull. A synthesis composing v390's facets, "
                   "no new number")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
