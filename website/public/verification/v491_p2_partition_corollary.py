"""v491 -- P2.PARTITION.01: g_car = 5 as a COROLLARY of the four marks -- the partition
sharpening of v53.  Exact sympy enumeration, no floats.

The lemma: a multiset of exactly 3 POSITIVE INTEGERS summing to 4 is unique -- {1, 1, 2}
(the unique partition of 4 into exactly 3 positive parts).  Its elementary symmetric
functions are e = (e1, e2, e3) = (4, 5, 2), so

    g_car = e2 = 5,   |Z2| = e3 = 2,   N_fam = e2 - e3 = 3

are COROLLARIES, not inputs.  v53 pins (1,1,2) by demanding ALL THREE targets (4,5,2);
the sharper lemma needs only e1 = 4 (+ positivity + 3 parts) -- checked here side by side.

Independence chain for the three hypotheses (why this is not circular in g_car):
  * "#marks = 4": v216 Gauss-Bonnet (flat sphere chi = 2 + Z2 branch points) -- P1-side
    premises only, checks 1/3/5 of v216 use NO g_car input;
  * "3 weights": rank H^1(P^1 minus 4 marks) = #marks - 1 = 3 is pure topology (v137
    explicit basis / v228 index gate) -- no g_car input;
  * "|a|_1 = 4": two g_car-free routes -- (a) parabolic-degree-0 (Mehta-Seshadri
    flatness/unitarity (U), v115): -deg(O(-2)+O(-1)^2) = 4 = #marks x (per-mark weight
    sum 1); (b) the mu4-average lemma (v115): a = |mu4| diag(A0), |a|_1 = 4 tr(A0) = 4.

  [E] 1. THE PARTITION LEMMA.  4 into exactly 3 positive integer parts: the multiset
        {1,1,2} is the UNIQUE solution; e_k(1,1,2) = (4,5,2) exactly.
  [E] 2. COROLLARIES + CONSISTENCY CLOSURE.  g_car = e2 = 5, |Z2| = e3 = 2,
        N_fam = e2 - e3 = 3; the carrier formula closes as a FIXED POINT:
        (2^(g_car-1) - 1)/g_car = 3 = rank H^1 = #marks - 1.
  [E] 3. NEGATIVE CONTROL: POSITIVITY.  allowing 0 gives 4 solutions with e2 ambiguous
        {0, 3, 4, 5} -- positivity is load-bearing.
  [E] 4. NEGATIVE CONTROL: THE SUM.  sum 3 -> unique but e2 = 3 != 5; sum 5 -> NOT
        unique ({1,1,3}, {1,2,2}) -- the sum 4 = #marks is load-bearing.
  [E] 5. NEGATIVE CONTROL: THE PART COUNT.  2 parts -> e2 in {3, 4}; 4 parts -> e2 = 6
        -- exactly 3 parts (= rank H^1) is load-bearing.
  [E] 6. NEGATIVE CONTROL: INTEGRALITY.  Mehta-Seshadri-typed RATIONAL weights (scaled
        by 4) give e2 = 16/3 resp. 44/9 != 5 -- integrality is load-bearing, and it comes
        from the SPLITTING-TYPE typing (Birkhoff-Grothendieck), NOT from MS weights
        (which are rational).
  [E] 7. THE v53 SHARPENING.  v53-style search (all three targets (4,5,2)) and the
        sharper search (only e1 = 4 + positivity + 3 parts) return the SAME unique
        multiset {1,1,2} -- the partition needs only e1 = 4.
  [E] 8. THE SUM RULE |a|_1 = 4.  4 x (N-1)/2 = 4 iff N = 3 (the equidistributed clock
        spectrum {0,...,N-1}/N has per-mark weight sum (N-1)/2); the v115 route
        |a|_1 = |mu4| tr(A0) = 4 x (0 + 1/3 + 2/3) = 4 agrees.
  [C] 9. HONEST RESIDUAL: THE WEIGHT-TYPING POSTULATE.  P2 is NOT made axiom-free.  The
        residual is the TYPING of the anchor as a multiset of #marks - 1 = 3 POSITIVE
        INTEGERS with |a|_1 = #marks = 4: integrality = the Birkhoff-Grothendieck
        splitting-exponent reading (Grothendieck: every bundle on P^1 splits with integer
        degrees -- then a theorem); positivity a_i >= 1 = h^0(E) = 0 (no global sections;
        correlate: the trivial mu4 character is ABSENT from H^1, v137 check 1); the sum
        rule = parabolic-degree-0 "given (U)" (v115).  AX.P2.01 stays a declared axiom.
        DIRECTION-REVERSAL NOTE: tfpt_constants COMPUTES N_fam from g_car
        ((2^(g_car-1)-1)/g_car); here the arrow runs the other way (marks -> partition ->
        g_car) -- an OVER-DETERMINATION check, not a circle, and it must not be
        double-counted in witness tallies.

Status: [E] Formal/arithmetic (partition + corollaries + negative controls, sympy exact);
[C] the weight-typing postulate (splitting-type integrality, h^0 = 0 positivity, (U) sum
rule).  Sharpens v53; does NOT retire axiom P2.  Python (sympy); Wolfram-mirrored
(tfpt_readouts.wl)."""
from itertools import combinations_with_replacement

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam


def _esym(ms):
    x = list(ms)
    e1 = sum(x)
    e2 = sum(x[i] * x[j] for i in range(len(x)) for j in range(i + 1, len(x)))
    e3 = sp.prod(x) if len(x) == 3 else None
    return e1, e2, e3


def _multisets(n_parts, lo, hi, total):
    return [m for m in combinations_with_replacement(range(lo, hi + 1), n_parts)
            if sum(m) == total]


def run():
    reset()
    print("v491  P2.PARTITION.01: g_car = 5 as a corollary of the four marks (partition of 4 into 3 positive parts)")

    # 1. the partition lemma: unique {1,1,2}, e = (4,5,2)
    core = _multisets(3, 1, 10, 4)
    e1, e2, e3 = _esym(core[0])
    check("THE PARTITION LEMMA [E]: 4 into exactly 3 positive integer parts has the UNIQUE "
          "solution %s; e_k = (%d, %d, %d) = (4, 5, 2) exactly"
          % (list(core[0]), e1, e2, e3),
          core == [(1, 1, 2)] and (e1, e2, e3) == (4, 5, 2))

    # 2. corollaries + consistency closure (fixed point, not input)
    nfam_carrier = (2 ** (e2 - 1) - 1) // e2
    check("COROLLARIES + CONSISTENCY CLOSURE [E]: g_car = e2 = %d (= axiom value %d), "
          "|Z2| = e3 = %d, N_fam = e2 - e3 = %d (= %d); carrier formula closes as a fixed "
          "point: (2^(g_car-1)-1)/g_car = %d = rank H^1 = #marks - 1 = 3"
          % (e2, g_car, e3, e2 - e3, N_fam, nfam_carrier),
          e2 == g_car == 5 and e3 == 2 and e2 - e3 == N_fam == 3 and nfam_carrier == 3)

    # 3. negative control: positivity
    nc0 = _multisets(3, 0, 10, 4)
    e2s0 = sorted(set(_esym(m)[1] for m in nc0))
    check("NEGATIVE CONTROL / POSITIVITY [E]: allowing 0 gives %d solutions with e2 "
          "ambiguous %s -- positivity is load-bearing" % (len(nc0), e2s0),
          len(nc0) == 4 and e2s0 == [0, 3, 4, 5])

    # 4. negative control: the sum
    nc3 = _multisets(3, 1, 10, 3)
    nc5 = _multisets(3, 1, 10, 5)
    check("NEGATIVE CONTROL / SUM [E]: sum 3 -> unique but e2 = %d != 5; sum 5 -> %d "
          "solutions (NOT unique) -- the sum 4 = #marks is load-bearing"
          % (_esym(nc3[0])[1], len(nc5)),
          len(nc3) == 1 and _esym(nc3[0])[1] == 3 and len(nc5) == 2)

    # 5. negative control: the part count
    nc2p = _multisets(2, 1, 10, 4)
    nc4p = _multisets(4, 1, 10, 4)
    e2_2p = sorted(sum(m[i] * m[j] for i in range(len(m)) for j in range(i + 1, len(m)))
                   for m in nc2p)
    e2_4p = sorted(sum(m[i] * m[j] for i in range(len(m)) for j in range(i + 1, len(m)))
                   for m in nc4p)
    check("NEGATIVE CONTROL / PART COUNT [E]: 2 parts -> e2 in %s; 4 parts -> e2 = %s -- "
          "exactly 3 parts (= rank H^1) is load-bearing" % (e2_2p, e2_4p),
          e2_2p == [3, 4] and e2_4p == [6])

    # 6. negative control: integrality (Mehta-Seshadri rational weights, scaled by 4)
    w1 = [sp.Rational(1, 3)] * 3
    w2 = [sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)]
    e2w = []
    for w in (w1, w2):
        a = [4 * x for x in w]
        e2w.append(sum(a[i] * a[j] for i in range(3) for j in range(i + 1, 3)))
    check("NEGATIVE CONTROL / INTEGRALITY [E]: MS-rational weight triples (sum 1, scaled by "
          "4) give e2 = %s and %s != 5 -- integrality is load-bearing; it comes from the "
          "SPLITTING-TYPE typing (Birkhoff-Grothendieck), NOT from MS weights (rational)"
          % (e2w[0], e2w[1]),
          all(sum(w) == 1 for w in (w1, w2)) and e2w == [sp.Rational(16, 3), sp.Rational(44, 9)]
          and all(v != 5 for v in e2w))

    # 7. the v53 sharpening: same unique multiset from strictly fewer targets
    v53_style = [m for m in combinations_with_replacement(range(0, 7), 3)
                 if _esym(m) == (4, 5, 2)]
    sharper = [m for m in combinations_with_replacement(range(1, 11), 3) if sum(m) == 4]
    check("THE v53 SHARPENING [E]: v53-style (all three targets e = (4,5,2)) and the sharper "
          "search (only e1 = 4 + positivity + 3 parts) BOTH return exactly {1,1,2} -- the "
          "partition needs only e1 = 4, so e2 = 5 and e3 = 2 are corollaries",
          v53_style == sharper == [(1, 1, 2)])

    # 8. the sum rule |a|_1 = 4: clock arithmetic + the v115 mu4-average route
    marks = 4
    totals = {N: marks * sp.Rational(sum(range(N)), N) for N in range(2, 7)}
    trA0 = sp.Rational(0) + sp.Rational(1, 3) + sp.Rational(2, 3)
    check("THE SUM RULE |a|_1 = 4 [E]: 4 x (N-1)/2 = 4 iff N = 3 (equidistributed clock "
          "spectrum {0,...,N-1}/N; totals %s); the v115 route |a|_1 = |mu4| tr(A0) = "
          "4 x (0 + 1/3 + 2/3) = %s agrees"
          % ({N: str(t) for N, t in totals.items()}, 4 * trA0),
          totals[3] == 4 and all(t != 4 for N, t in totals.items() if N != 3)
          and 4 * trA0 == 4)

    # 9. honest residual: the weight-typing postulate (P2 NOT axiom-free)
    check("HONEST RESIDUAL [C]: P2 is NOT made axiom-free -- the residual is the weight "
          "TYPING (integrality = Birkhoff-Grothendieck splitting exponents; positivity = "
          "h^0 = 0, correlate v137 check 1; sum rule = par-deg 0 'given (U)', v115); "
          "AX.P2.01 stays a declared axiom. Direction-reversal typed: tfpt_constants "
          "computes N_fam FROM g_car, here the arrow runs marks -> partition -> g_car -- "
          "an over-determination check, not a circle, never double-counted", True)

    return summary("v491 P2.PARTITION.01: 4 into exactly 3 positive parts = uniquely {1,1,2} => "
                   "e = (4,5,2) => g_car = 5, |Z2| = 2, N_fam = 3 as corollaries (sympy exact); every "
                   "assumption load-bearing (positivity/sum/part-count/integrality negative controls); "
                   "sharpens v53 (needs only e1 = 4); residual = the weight-typing postulate -- "
                   "AX.P2.01 stays a declared axiom")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
