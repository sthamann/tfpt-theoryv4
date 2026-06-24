"""v394 -- COXETER.ATOMS.01: the clockwork coherence -- the three Coxeter primes ARE the three
anchor atoms ARE the three number-field facets, and the prime-2 seam is the common dynamical
factor.  A bird's-eye [E] re-reading that ties v390 (the prime facets) to the anchor a=(1,1,2)
and to v319 (the 5x6 translation clock); it also REGISTERS the residual-asymmetry research
question (RES.COXETER.SYMMETRY.01) as a tracked [O].  No new number.

The Coxeter clock 30 = 2*3*5 = h(E8) had its three primes facet-typed in v390.  Seen from the
anchor, those primes are not three coincidences -- they are the three atoms of a=(1,1,2):

    |Z2| = e3(a) = 2,    N_fam = p0(a) = 3,    g_car = e2(a) = 5,    product = 30 = h(E8).

So {atoms} = {Coxeter primes} = {facet fields}: 2->Q(i) (seam), 3->Q(sqrt-3) (family CP),
5->Q(sqrt5) (carrier golden).  And the dynamic rates are {2,3}-arithmetic with prime-2 as the
common factor (the seam involution drives every sector):

  [E] 1. ANCHOR ATOMS = COXETER PRIMES: a=(1,1,2) has e3=2=|Z2|, p0=3=N_fam, e2=5=g_car, and
        2*3*5 = 30 = h(E8); the clock's three primes ARE the anchor's three atoms.
  [E] 2. ATOMS = FACET FIELDS (v390): each atom-prime is the ramified prime of its facet field
        -- 2->Q(i) (disc -4), 3->Q(sqrt-3) (disc -3), 5->Q(sqrt5) (disc 5); {atoms}={primes}={fields}.
  [E] 3. QG SUSCEPTIBILITY IS PURE {2,3}: chi = 1/(1-(2/3)^6) = 729/665 = 3^6/(3^6-2^6), and
        (2/3)^6 = 2^6/3^6 -- both built from the prime-2 and prime-3 sixth powers; exponent
        6 = 2*N_fam.
  [E] 4. PRIME-2 IS THE COMMON DYNAMIC FACTOR: the seam rate 2/3 = |Z2|/N_fam (prime-2/prime-3),
        and the compiler rate (phi+2)/4 = (phi+2)/|mu4| with |mu4| = 4 = 2^2 (prime-2) -- so
        BOTH dynamic rates carry prime-2 (the seam involution), while prime-3 (family) and
        prime-5 (carrier golden) distinguish the two hands.
  [E] 5. THE 5x6 CLOCK (v319): 30 = 5 * 6 = g_car * (2*N_fam) = (static carrier, prime-5) *
        (dynamic, prime-2*prime-3) -- the translation clock, grounded in the prime split.
  [C] 6. THE READING: the prime-2 seam is the universal dynamical engine (present in every rate);
        prime-3 and prime-5 are the two distinguishable attractors (family / carrier).
  [O] 7. OPEN RESEARCH QUESTION (RES.COXETER.SYMMETRY.01): is the prime-2-as-common-factor
        reading FORCED -- i.e. does the seam involution provably appear in EVERY sector's gap,
        with no independent prime-2 attractor -- or is there a residual asymmetry?  A named,
        tracked open question (see tfpt_research_contracts), NOT closed here.

NET TYPING: [E] the exact arithmetic (atoms=primes=fields; chi=3^6/(3^6-2^6); 2/3=|Z2|/N_fam;
4=|mu4|=2^2; 30=5x6); [C] the seam-as-engine reading; [O] the registered symmetry question.
A bird's-eye re-reading; no new number.  Python (sympy)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

x = sp.symbols("x")
PHI = (1 + sp.sqrt(5)) / 2


def run():
    reset()
    print("v394  COXETER.ATOMS.01: the three Coxeter primes = the three anchor atoms = the three facet fields")

    # anchor a = (1,1,2): elementary symmetric + power sums
    a = (1, 1, 2)
    e1 = a[0] + a[1] + a[2]                                   # 4 = |mu4|
    e2 = a[0] * a[1] + a[0] * a[2] + a[1] * a[2]              # 5 = g_car
    e3 = a[0] * a[1] * a[2]                                   # 2 = |Z2|
    p0 = len(a)                                              # 3 = N_fam

    # 1. anchor atoms = coxeter primes
    atoms = {e3, p0, e2}
    check("ANCHOR ATOMS = COXETER PRIMES [E]: a=(1,1,2) has e3=%d=|Z2|, p0=%d=N_fam, e2=%d=g_car; "
          "{%d,%d,%d} product = %d = h(E8); the clock's three primes ARE the anchor's three atoms"
          % (e3, p0, e2, e3, p0, e2, e3 * p0 * e2),
          atoms == {2, 3, 5} and e3 * p0 * e2 == 30 and e2 == g_car and p0 == N_fam)

    # 2. atoms = facet fields (each ramified at its prime, v390)
    disc2 = sp.discriminant(x ** 2 + 1, x)                   # Q(i)      -4
    disc3 = sp.discriminant(x ** 2 + x + 1, x)               # Q(sqrt-3) -3
    disc5 = sp.discriminant(x ** 2 - x - 1, x)               # Q(sqrt5)   5
    facet_ok = (abs(int(disc2)) % 2 == 0 and abs(int(disc3)) % 3 == 0 and abs(int(disc5)) % 5 == 0)
    check("ATOMS = FACET FIELDS [E] (v390): 2->Q(i) (disc %s), 3->Q(sqrt-3) (disc %s), "
          "5->Q(sqrt5) (disc %s); each atom-prime is the ramified prime of its facet field -- "
          "{atoms}={primes}={fields}" % (disc2, disc3, disc5),
          facet_ok and disc2 == -4 and disc3 == -3 and disc5 == 5)

    # 3. QG susceptibility is pure {2,3}
    seam = sp.Rational(2, 3) ** 6
    chi = sp.simplify(1 / (1 - seam))
    check("QG SUSCEPTIBILITY IS PURE {2,3} [E]: chi = 1/(1-(2/3)^6) = %s = 3^6/(3^6-2^6), and "
          "(2/3)^6 = %s = 2^6/3^6 -- both built from 2^6,3^6; exponent 6 = 2*N_fam = %d"
          % (chi, seam, 2 * N_fam),
          chi == sp.Rational(3 ** 6, 3 ** 6 - 2 ** 6) and seam == sp.Rational(2 ** 6, 3 ** 6)
          and 6 == 2 * N_fam)

    # 4. prime-2 is the common dynamic factor
    seam_base = sp.Rational(e3, p0)                          # |Z2|/N_fam = 2/3
    mu4 = e1                                                 # 4 = 2^2
    compiler_rate = sp.simplify((PHI + 2) / mu4)             # (phi+2)/|mu4|
    check("PRIME-2 IS THE COMMON DYNAMIC FACTOR [E]: the seam rate 2/3 = |Z2|/N_fam = %s "
          "(prime-2/prime-3), and the compiler rate (phi+2)/4 = (phi+2)/|mu4| with |mu4|=%d=2^2 "
          "(prime-2) -- BOTH dynamic rates carry prime-2 (the seam involution); prime-3,prime-5 "
          "distinguish the two hands" % (seam_base, mu4),
          seam_base == sp.Rational(2, 3) and mu4 == 4 and mu4 == 2 ** 2
          and sp.simplify(compiler_rate - (PHI + 2) / 4) == 0)

    # 5. the 5x6 clock (v319)
    check("THE 5x6 CLOCK [E] (v319): 30 = 5 * 6 = g_car * (2*N_fam) = (static carrier prime-5) * "
          "(dynamic prime-2*prime-3) = %d * %d -- the translation clock, grounded in the prime "
          "split" % (g_car, 2 * N_fam),
          g_car * (2 * N_fam) == 30 and 2 * N_fam == 6)

    # 6. the reading (interpretation)
    check("THE READING [C]: the prime-2 seam is the universal dynamical engine (present in every "
          "rate via |Z2|=2 and |mu4|=4); prime-3 (family) and prime-5 (carrier golden) are the "
          "two distinguishable attractors", True)

    # 7. open research question (registered, NOT closed)
    check("OPEN QUESTION [O] (RES.COXETER.SYMMETRY.01): is the prime-2-as-common-factor reading "
          "FORCED (the seam involution provably in EVERY gap, no independent prime-2 attractor) "
          "or is there a residual asymmetry? A named tracked question (tfpt_research_contracts), "
          "NOT closed here", True)

    return summary("v394 COXETER.ATOMS.01: the clockwork coherence -- [E] the three Coxeter primes ARE the "
                   "three anchor atoms {|Z2|=2, N_fam=3, g_car=5} (a=(1,1,2): e3,p0,e2; product 30=h(E8)) ARE "
                   "the three facet fields (Q(i)/Q(sqrt-3)/Q(sqrt5), v390); chi=3^6/(3^6-2^6) and (2/3)^6=2^6/3^6 "
                   "are pure {2,3}; both dynamic rates carry prime-2 (2/3=|Z2|/N_fam, (phi+2)/4=(phi+2)/|mu4|, "
                   "|mu4|=2^2); 30=5x6=g_car*(2 N_fam) (v319). [C] the seam (prime-2) is the universal dynamic "
                   "engine. [O] RES.COXETER.SYMMETRY.01: is that forced? A bird's-eye re-reading, no new number")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
