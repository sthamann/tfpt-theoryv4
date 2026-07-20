"""probe_p2_retirement_partition.py -- EXPLORATION (experiments/tfpt-discovery, NOT load-bearing).

P2-retirement audit: can Axiom P2 (g_car = 5) become a THEOREM, conditional on
(i) #marks = 4  [E, v216 Gauss-Bonnet: flat sphere chi=2 + Z2 branch points -- P1-side
    premises only, NO g_car input], and
(ii) the weight typing "the anchor is a multiset of #marks-1 = 3 POSITIVE INTEGERS with
    |a|_1 = #marks = 4"?

Sharpening of v53: v53 pins (1,1,2) using ALL THREE targets e = (4,5,2).  The sharper
lemma: 3 positive integers summing to 4 already force the multiset {1,1,2} (the unique
partition of 4 into exactly 3 positive parts), so e2 = 5 = g_car and e3 = 2 = |Z2| are
COROLLARIES, not inputs.

Circularity audit (from reading v216/v23/v53/v137/v228/v115 + papers 1 and 3):
  * "#marks = 4": v216 check 1+3 derive it from {sphere chi=2, flat, Z2 branch} alone;
    N_fam = 3 appears only as one of three CONVERGENT selectors (check 4), not as input.
  * "3 weights": rank H^1(P^1 minus 4 marks) = #marks - 1 = 3 is pure topology
    (v137 explicit basis, v228 index gate) -- no g_car input.
  * "|a|_1 = 4": two routes, both g_car-free:
      (a) splitting type O(-2)+O(-1)^2 has deg = -4, and parabolic-degree-0
          (Mehta-Seshadri flatness/unitarity (U)) gives -deg = total parabolic weight
          = #marks * (per-mark weight sum) = 4 * 1;
      (b) mu4-average lemma (v115): a = |mu4| * diag(A0), so |a|_1 = 4 * tr(A0) = 4.
      The per-mark weight sum 1 = (0 + 1/3 + 2/3) is the equidistributed clock
      spectrum {0,1,...,N-1}/N at N = 3, and (N-1)/2 = 1 iff N = 3 -- consistent, not
      circular in g_car.
  * GEOMETRIC TYPING of the weights: the repo does NOT type (1,1,2) as Mehta-Seshadri
    weights (those are the RATIONALS {0,1/3,2/3} in [0,1), v115/v137 -- MS weights are
    rational, which would speak AGAINST integrality).  (1,1,2) is typed as the
    Birkhoff-Grothendieck SPLITTING TYPE / exponents-at-infinity: integrality is then a
    THEOREM (Grothendieck: every bundle on P^1 splits with integer degrees), and
    positivity a_i >= 1 is h^0(E) = 0 (no global sections; candidate geometric ground:
    the trivial mu4 character is ABSENT from H^1, v137 check 1).

This script machine-checks the arithmetic core and its negative controls (each
assumption is load-bearing).  Numbers only; no paper/ledger claims.
"""
from itertools import combinations_with_replacement

import sympy as sp


def esym(ms):
    x = list(ms)
    e1 = sum(x)
    e2 = sum(x[i] * x[j] for i in range(len(x)) for j in range(i + 1, len(x)))
    e3 = sp.prod(x) if len(x) == 3 else None
    return e1, e2, e3


def multisets(n_parts, lo, hi, total):
    return [m for m in combinations_with_replacement(range(lo, hi + 1), n_parts)
            if sum(m) == total]


def main():
    print("== P2-retirement: partition lemma + negative controls ==")

    # ---- the core lemma: 3 positive integers, sum 4 -> unique {1,1,2} ----
    core = multisets(3, 1, 10, 4)
    e1, e2, e3 = esym(core[0])
    print(f"   partitions of 4 into exactly 3 positive parts: {core}")
    print(f"   -> unique: {len(core) == 1};  e_k({core[0]}) = ({e1},{e2},{e3})")
    print(f"   -> g_car = e2 = {e2}  (P2 as corollary),  |Z2| = e3 = {e3},"
          f"  N_fam = e2 - e3 = {e2 - e3}")
    assert core == [(1, 1, 2)] and (e1, e2, e3) == (4, 5, 2)

    # ---- consistency closure (fixed point, not input) ----
    g = e2
    nfam_carrier = (2 ** (g - 1) - 1) // g          # tfpt_constants formula
    nfam_topo = 4 - 1                               # rank H^1 = #marks - 1
    print(f"   consistency: N_fam(carrier formula) = (2^{g-1}-1)/{g} = {nfam_carrier}"
          f" = rank H^1 = {nfam_topo}: {nfam_carrier == nfam_topo}")

    # ---- negative controls: every assumption is load-bearing ----
    print("\n== negative controls ==")
    nc0 = multisets(3, 0, 10, 4)                    # drop positivity
    print(f"   drop positivity (allow 0): {nc0}  -> {len(nc0)} solutions, "
          f"e2 ambiguous {sorted(set(esym(m)[1] for m in nc0))}")
    assert len(nc0) == 4

    for tot in (3, 5):                              # wrong sum
        nc = multisets(3, 1, 10, tot)
        print(f"   sum {tot} instead of 4: {nc} -> "
              f"{'unique but e2 = %d != 5' % esym(nc[0])[1] if len(nc) == 1 else 'NOT unique'}")

    for np_ in (2, 4):                              # wrong part count
        nc = multisets(np_, 1, 10, 4)
        e2s = [sum(m[i] * m[j] for i in range(len(m)) for j in range(i + 1, len(m)))
               for m in nc]
        print(f"   {np_} parts instead of 3: {nc} -> e2 values {e2s} (not (unique and 5))")

    # drop integrality (Mehta-Seshadri typing: rationals in [0,1), scaled by 4):
    # a/4 must be 3 rationals in (0,1) summing to 1 -- infinitely many; two witnesses
    w1 = [sp.Rational(1, 3)] * 3
    w2 = [sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)]
    for w in (w1, w2):
        a = [4 * x for x in w]
        e2w = sum(a[i] * a[j] for i in range(3) for j in range(i + 1, 3))
        print(f"   drop integrality (MS-rational weights {w}): a = {a}, "
              f"e2 = {e2w} != 5")
        assert sum(w) == 1 and e2w != 5
    print("   -> integrality is load-bearing; it comes from the SPLITTING-TYPE typing "
          "(Birkhoff-Grothendieck), NOT from MS weights (which are rational).")

    # ---- v53 comparison: the sharper lemma needs only e1 (not e2, e3) ----
    print("\n== v53 sharpening ==")
    v53_style = [m for m in combinations_with_replacement(range(0, 7), 3)
                 if esym(m) == (4, 5, 2)]
    sharper = [m for m in combinations_with_replacement(range(1, 11), 3)
               if sum(m) == 4]
    print(f"   v53 (all three targets e=(4,5,2), range 0..6): {v53_style}")
    print(f"   sharper (only e1=4 + positivity + 3 parts):     {sharper}")
    assert v53_style == sharper == [(1, 1, 2)]

    # ---- the sum rule |a|_1 = #marks: clock-weight arithmetic ----
    print("\n== sum rule |a|_1 = 4: par-deg 0 + equidistributed clock weights ==")
    marks = 4
    for N in range(2, 7):
        per_mark = sp.Rational(sum(range(N)), N)     # (0+1+...+(N-1))/N = (N-1)/2
        total = marks * per_mark
        tag = "  <-- N = rank H^1 = 3: total = 4 = |a|_1 = -deg O(-2)+O(-1)^2"
        print(f"   N={N}: per-mark weight sum (N-1)/2 = {per_mark}, "
              f"total = 4 x {per_mark} = {total}{tag if N == 3 else ''}")
    assert marks * sp.Rational(sum(range(3)), 3) == 4

    # mu4-average route (v115): a = 4 * diag(A0), tr(A0) = 0 + 1/3 + 2/3 = 1
    trA0 = sp.Rational(0) + sp.Rational(1, 3) + sp.Rational(2, 3)
    print(f"   v115 route: |a|_1 = |mu4| * tr(A0) = 4 * {trA0} = {4 * trA0}")
    assert 4 * trA0 == 4

    print("\n== verdict (exploration only) ==")
    print("   P2-as-corollary chain: [#marks=4, E(v216, P1-side)] + [rank H^1 = 3, E]")
    print("   + [weight typing: positive integers, |a|_1 = 4]  ==>  {1,1,2} unique")
    print("   ==> g_car = e2 = 5 [E arithmetic], |Z2| = e3 = 2, N_fam = 3.")
    print("   Residual postulate: the weight TYPING -- integrality (= splitting-type")
    print("   reading, Grothendieck), positivity (= h^0 = 0 / no trivial mu4 character")
    print("   in H^1, v137), sum rule (= par-deg 0 / unitarity (U), v115 [I]/[N]).")


if __name__ == "__main__":
    main()
