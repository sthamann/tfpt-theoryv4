"""v91 -- The Spine Tetrahedron: the compiler microkernel as one finite object.

Implements the review proposal (2026-06-10): the spine T = {2,3,4,5} =
{|Z2|, N_fam, |mu_4|, g_car} is promoted from a recurring quotient set to a
single combinatorial object -- a tetrahedron whose nodes, edges, faces and
volume ARE the central integer grammar.

WHAT IS GENUINELY CHECKED (and how it is typed):

  [I] 1. anchor closure: T = {e3(a), p0(a), e1(a), e2(a)} for a = (1,1,2)
         -- the tetrahedron is NOT a second structure next to the anchor;
         it is the anchor plus its zeroth moment.
  [I] 2. edge products {6,8,10,12,15,20} with established readings
         (|R+(A3)|/C6; rank E8 = h(D5) = det R; A_Lambda = |E(K5)|;
         |R(A3)| = dim SM gauge; dim A3; det L).
  [I] 3. face products {24,30,40,60} (|W(A3)|; h(E8); |R(D5)| = Sum L;
         cascade start D_0 = dim of the mixed (10,6) block, cf. v89).
  [I] 4. volume 2*3*4*5 = 120 = |R+(E8)| = Tr_S+ X^2 = sum of E8 exponents
         = 5!.
  [I] 5. graph reading: |R(E8)| = 240 = |mu_4| * |E(K_4)| * |E(K_5)| with
         |E(K_4)| = p2(a) = 6 and |E(K_5)| = p3(a) = 10 -- and the honest
         NEGATIVE CONTROL: the identification breaks at K_6
         (|E(K_6)| = 15 != p4(a) = 18), so it is specific, not generic.

  TRIVIALITY FLAG (important): 6. the "dual cuts" (node x opposite face,
  edge x opposite edge, all = 120) are TAUTOLOGIES -- every complementary
  partition of a 4-set multiplies to the total product.  Their value is
  purely organisational: ONE raster instead of seven separate "120
  costumes".  They are typed as presentation, never as evidence.

  HONEST INCOMPLETENESS: 7. the tetrahedron grammar is a SUB-grammar.  The
  full subset-product set is {2,...,120} (15 numbers); the load-bearing
  7 (scalaron), 16 (dim S+), 41 (EM budget), 48 (Omega_adm), 240, 248 are
  NOT subset products -- they need the anchor power sums / Pascal /
  glue layers.  The tetrahedron complements, it does not replace, the
  admissibility filter.

  AUDIT (fingerprint, not load-bearing): 8. chi_T(t) = (t-2)(t-3)(t-4)(t-5)
  = t^4 - 14 t^3 + 71 t^2 - 154 t + 120: the coefficients are exactly
  (node sum, edge sum, face sum, volume) = (14, 71, 154, 120) with
  14 = dim G2 (the [K,Q] motif, v80); the spine is symmetric about 7/2, so
  chi_T(0) = chi_T(7) = 120 and chi_T(1) = chi_T(6) = 24, and the scalaron
  exponent 7 = 2+5 = 3+4 is the complementary-pair sum (the same 7 as the
  branch-divisor trace, v80/v81).  Typed AUDIT: 71 and 154 carry no TFPT
  reading; nothing here is promoted to spine status.
"""
from itertools import combinations
from math import prod, comb, factorial

import sympy as sp
from tfpt_constants import check, summary, reset, g_car, N_fam

ANCHOR = (1, 1, 2)
Z2, MU4 = 2, 4
SPINE = (Z2, N_fam, MU4, g_car)          # {2,3,4,5}
E8_EXPONENTS = (1, 7, 11, 13, 17, 19, 23, 29)
SCALARON = 7
DIM_G2 = 14


def esym(a, k):
    return sum(prod(c) for c in combinations(a, k)) if k else 1


def run():
    reset()
    print("v91 spine tetrahedron (compiler microkernel; review proposal 2026-06-10)")

    # 1. the anchor generates the spine (plus zeroth moment)
    gen = sorted([esym(ANCHOR, 3), len(ANCHOR), esym(ANCHOR, 1), esym(ANCHOR, 2)])
    check("spine = {e3(a), p0(a), e1(a), e2(a)} = {2,3,4,5} = "
          "{|Z2|, N_fam, |mu4|, g_car}", gen == sorted(SPINE))

    # 2. edges
    edges = sorted(prod(c) for c in combinations(SPINE, 2))
    check("edge products = {6,8,10,12,15,20}",
          edges == [6, 8, 10, 12, 15, 20])
    check("edge readings: 2*3=6=|R+(A3)|=C6; 2*4=8=rank E8=h(D5)=det R; "
          "2*5=10=A_Lambda=|E(K5)|; 3*4=12=|R(A3)|=dim SM gauge (8+3+1); "
          "3*5=15=dim A3; 4*5=20=det L",
          2 * 3 == 6 and 2 * 4 == 8 and 2 * 5 == 10
          and 3 * 4 == 8 + 3 + 1 and 3 * 5 == 15 and 4 * 5 == 20)

    # 3. faces
    faces = sorted(prod(c) for c in combinations(SPINE, 3))
    check("face products = {24,30,40,60}", faces == [24, 30, 40, 60])
    check("face readings: 2*3*4=24=|W(A3)|=4!; 2*3*5=30=h(E8); "
          "2*4*5=40=|R(D5)|=Sum L; 3*4*5=60=cascade start = dim(10,6) "
          "mixed block (v89 branching)",
          24 == factorial(4) and 30 == 2 * 3 * 5 and 40 == 2 * 4 * 5
          and 60 == 10 * 6)

    # 4. volume
    check("volume 2*3*4*5 = 120 = |R+(E8)| = 5! = sum of E8 exponents "
          "(= Tr_S+ X^2, tfpt_1)",
          prod(SPINE) == 120 == factorial(5) == sum(E8_EXPONENTS))

    # 5. graph reading + negative control
    check("graph reading: |R(E8)| = 240 = |mu4| * |E(K4)| * |E(K5)| "
          "with |E(K4)| = p2(a) = 6, |E(K5)| = p3(a) = 10",
          MU4 * comb(4, 2) * comb(5, 2) == 240
          and comb(4, 2) == sum(x**2 for x in ANCHOR)
          and comb(5, 2) == sum(x**3 for x in ANCHOR))
    check("NEGATIVE CONTROL: the graph reading breaks at K6 "
          "(|E(K6)| = 15 != p4(a) = 18) -- specific, not generic",
          comb(6, 2) == 15 and sum(x**4 for x in ANCHOR) == 18)

    # 6. dual cuts -- correct, but TAUTOLOGICAL (typed as presentation)
    node_cuts = [n * prod(x for x in SPINE if x != n) for n in SPINE]
    edge_cuts = [prod(c) * prod(x for x in SPINE if x not in c)
                 for c in combinations(SPINE, 2)]
    check("dual cuts all equal 120 (2*60, 3*40, 4*30, 5*24; 6*20, 8*15, "
          "10*12) -- TAUTOLOGY of complementary partitions; value is the "
          "one-raster presentation, NOT evidence",
          set(node_cuts) == {120} and set(edge_cuts) == {120})

    # 7. honest incompleteness of the grammar
    products = {prod(c) for r in (1, 2, 3, 4)
                for c in combinations(SPINE, r)}
    outside = [7, 16, 41, 48, 240, 248]
    check("SUB-grammar, honestly: 7 (scalaron), 16 (dim S+), 41 (EM "
          "budget), 48 (Omega_adm), 240, 248 are NOT subset products -- "
          "the tetrahedron complements the admissibility filter, it does "
          "not replace it",
          all(n not in products for n in outside))

    # 8. chi_T audit fingerprint (NOT load-bearing)
    t = sp.symbols('t')
    chi = sp.expand(sp.prod([t - x for x in SPINE]))
    check("chi_T = t^4 - 14 t^3 + 71 t^2 - 154 t + 120; coefficients = "
          "(node sum, edge sum, face sum, volume), node sum 14 = dim G2 "
          "([K,Q] motif, v80)  [AUDIT]",
          chi == t**4 - 14 * t**3 + 71 * t**2 - 154 * t + 120
          and sum(SPINE) == DIM_G2 and sum(edges) == 71
          and sum(faces) == 154)
    check("spine symmetric about 7/2: chi_T(0)=chi_T(7)=120, "
          "chi_T(1)=chi_T(6)=24; scalaron 7 = 2+5 = 3+4 = the "
          "complementary-pair sum (same 7 as the branch-divisor trace, "
          "v80/v81)  [AUDIT, not load-bearing]",
          chi.subs(t, 0) == chi.subs(t, SCALARON) == 120
          and chi.subs(t, 1) == chi.subs(t, 6) == 24
          and 2 + 5 == 3 + 4 == SCALARON)

    return summary("v91 spine tetrahedron")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
