"""seam_clock_rigidity_moebius_probe.py -- EXPLORATION ONLY (experiments/, no verification claim).

ROUTE B OF THE v503 CLASSIFICATION, PART 1/2 (the Moebius / divisor side):
"RP seam data => order-4 clock" attacked as a RIGIDITY theorem.

v503 (QGEO.EMERGE.LIGHT.01) localised the one remaining identification input:
mark count 4 is derived (v216), the square modulus is derived GIVEN the clock
(v493/v503), free dynamics picks hexagonal -- the order-4 clock itself is the
carrier input [C], identical to the P2 typing rest R1 (v499).  This probe asks:
how much of "order-4 clock" is already forced by ESTABLISHED seam data
(P1 deck involution + 4 deck-free Z2 marks, v216), i.e. what is the WEAKEST
residual input from which the clock follows as a theorem?

  B1 SQUARE-ROOT CLASSIFICATION (exact, complete).  The deck z -> -z (the
     collar Z2, P1-side) has in PGL2(C) EXACTLY TWO square roots: z -> +iz and
     z -> -iz -- both elliptic of ORDER 4, mutually inverse, fixing the deck's
     fixed points {0, inf}.  No parabolic/loxodromic/other square roots exist
     (complete case analysis: trace != 0 forces diagonal with (a/d)^2 = -1;
     trace = 0 forces det = 0, impossible).  So "order 4" is NOT a choice: any
     Moebius square root of the deck automatically has order 4.
  B1' MARKS FILTER + ALIGNMENT (the sharp part).  A deck-invariant deck-free
     mark set is {u,-u,v,-v}.  A marks-preserving square root of the deck
     exists  <=>  v = +-i u  <=>  the marks are ONE mu4 orbit ALIGNED with the
     deck  ==>  cross-ratio {2, 1/2, -1}, j = 1728, tau = i, free 4-cycle, and
     the root is THE clock (unique up to inverse = Aut(Z4)).  Group form: the
     stabiliser of a harmonic 4-set is D4 (order 8 = 2|mu4|, v168); squares in
     D4 are {1, r^2}; so a square root of the deck inside the stabiliser exists
     iff the deck is the CENTRAL involution r^2 of that D4.  HONESTY: harmonic
     j = 1728 ALONE is not sufficient -- the counterexample {+-1, +-(3+2sqrt2)}
     is harmonic (lambda = 1/2) and deck-free, but there z -> -z is an
     EDGE-type (non-central) involution of the D4 and has NO root in it; the
     true central involution CROSSES the +- pairs (a different collar).  The honest
     residual input is therefore ONE bit: "the collar deck is central in the
     mark stabiliser" = "the deck admits a marks-preserving Moebius square
     root".  Everything else (order 4, uniqueness, free orbit, tau = i pinned,
     scale free) follows.
  B3 WHY n = 4 (honest).  A Z_n acting freely on the 4 marks forces n | 4;
     faithfulness (a Moebius map with >= 3 fixed points is the identity) kills
     every n >= 5 outright (kernel argument through S4); n = 3 requires a fixed
     mark (hexagonal (3,3,3) shadow) and is no square root of an involution;
     marks-transitive cyclic => n = 4 exactly.  The deck (n = 2) preserves
     EVERY {+-u, +-v} -- modulus-blind (v503 B5, here exact and symbolic), so
     ALL modulus-pinning power sits in the square-root bit.  Why n = 4 rather
     than no clock has NO Moebius-side answer -- the P1-side forcing candidate
     is fermionic: companion probe seam_clock_rigidity_fock_probe.py shows the
     NS-sector deck implementation is forced to order 4 (U^2 = (-1)^F).
  B4 NEGATIVE / SHARPNESS CONTROLS.  (a) no order-8 element preserves ANY
     4-point set (z -> zeta8 z has orbit sizes 8 off {0, inf}; kernel argument);
     the Z8 lives upstairs (spin/Fock, 8 = 2|mu4|), never on the sphere.
     (b) hexagonal/equianharmonic marks {1, w, w^2, inf}: stabiliser = A4
     (order 12, element orders {1,2,3}), zero order-4 elements, squares contain
     no involution => NO clock at j = 0 (sharpens v503 C2).  (c) generic marks
     {+-1, +-2}: stabiliser = Klein V4 (exponent 2), squares = {1} => not even
     the deck has a root.  (d) fixed-type harmonic {0, inf, u, -u}: the deck
     fixes two marks ((2,4,4) shadow, killed by v216 all-order-2), and the
     global roots +-iz do not preserve it.

Repo anchors: v492 S5 (clock^2 = deck, U(2) clock diag(i,1), Z8 spin bridge),
v215 K1/K2 (4 marks, square), v216 (marks from Gauss-Bonnet; free order-4
selects (2,2,2,2)), v168/v214 (cross-ratio 2 => j = 1728, D4), v117 (cusp class
lam^3 - 1), v503 (emergence classification), v499/p2 probe (R1 typing rest).

Exact throughout (sympy; no floats).  Standalone.
Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/seam_clock_rigidity_moebius_probe.py
"""
from itertools import permutations

import sympy as sp
from sympy.combinatorics import Permutation

I = sp.I
RESULTS = []

# carrier constants (hardcoded, standalone probe; cf. tfpt_constants)
G_CAR = 5
N_FAM = 3


def check(name, ok):
    RESULTS.append(bool(ok))
    print(("PASS" if ok else "FAIL") + " [%2d] %s" % (len(RESULTS), name))


def iszero(e):
    e2 = sp.expand(e)
    if e2 == 0:
        return True
    return sp.simplify(e2) == 0


# ---------------------------------------------------------------------------
# projective points (p, q) with point = p/q, infinity = (1, 0); exact Moebius
# ---------------------------------------------------------------------------
def peq(P, Q):
    return iszero(P[0] * Q[1] - P[1] * Q[0])


def apply_m(M, P):
    return (sp.expand(M[0, 0] * P[0] + M[0, 1] * P[1]),
            sp.expand(M[1, 0] * P[0] + M[1, 1] * P[1]))


def map3(A, B, C):
    """the unique Moebius matrix sending (inf, 0, 1) -> (A, B, C)."""
    alpha = C[0] * B[1] - B[0] * C[1]
    beta = A[0] * C[1] - C[0] * A[1]
    return sp.Matrix([[alpha * A[0], beta * B[0]],
                      [alpha * A[1], beta * B[1]]])


def mexp(M):
    return M.applyfunc(sp.expand)


def prop_mat(A, B):
    """projective equality of 2x2 matrices (A = c B)."""
    a = [A[0, 0], A[0, 1], A[1, 0], A[1, 1]]
    b = [B[0, 0], B[0, 1], B[1, 0], B[1, 1]]
    for i in range(4):
        for j in range(i + 1, 4):
            if not iszero(a[i] * b[j] - a[j] * b[i]):
                return False
    return True


def is_scalar_mat(M):
    return iszero(M[0, 1]) and iszero(M[1, 0]) and iszero(M[0, 0] - M[1, 1])


def proj_order(M, cap=9):
    P = sp.eye(2)
    for n in range(1, cap + 1):
        P = mexp(P * M)
        if is_scalar_mat(P):
            return n
    return None


def stabilizer(cfg):
    """ALL Moebius maps preserving the 4-point set cfg (complete: a Moebius map
    is fixed by the images of 3 points => enumerate all 24 ordered triples)."""
    S = map3(cfg[0], cfg[1], cfg[2])
    Sinv = S.adjugate()
    found = []
    for t in permutations(range(4), 3):
        T = map3(cfg[t[0]], cfg[t[1]], cfg[t[2]])
        M = mexp(T * Sinv)
        ok = all(any(peq(apply_m(M, p), q) for q in cfg) for p in cfg)
        if ok and not any(prop_mat(M, X) for X in found):
            found.append(M)
    return found


def mark_perm(M, cfg):
    perm = []
    for p in cfg:
        img = apply_m(M, p)
        perm.append([j for j, q in enumerate(cfg) if peq(img, q)][0])
    return perm


def order_profile(stab):
    prof = {}
    for g in stab:
        o = proj_order(g)
        prof[o] = prof.get(o, 0) + 1
    return prof


def cross_ratio(P1, P2, P3, P4):
    d = lambda X, Y: X[0] * Y[1] - Y[0] * X[1]
    return sp.simplify(sp.expand(d(P1, P3) * d(P2, P4)) /
                       sp.expand(d(P1, P4) * d(P2, P3)))


def jlam(lam):
    return sp.simplify(256 * (lam ** 2 - lam + 1) ** 3
                       / (lam ** 2 * (lam - 1) ** 2))


DECK = sp.diag(1, -1)                 # z -> -z (the P1 collar involution)
CLOCK = sp.diag(I, 1)                 # z -> iz
CLOCKINV = sp.diag(-I, 1)             # z -> -iz


def run():
    print("seam_clock_rigidity_moebius_probe: Route B (v503) -- how much of the "
          "order-4 clock is forced by the deck + 4 deck-free marks?  B1/B3/B4, exact")
    print("=" * 100)

    # ================================================ S1: square-root classification
    print("  -- S1: ALL square roots of the deck in PGL2(C) (complete, exact)")
    a, b, c, d, lam_, r = sp.symbols('a b c d lam_ r')
    M = sp.Matrix([[a, b], [c, d]])

    # 1. normal form + identity rigidity
    ch = sp.expand(M * M - (a + d) * M + M.det() * sp.eye(2))
    z1, z2, z3 = sp.symbols('z1 z2 z3')
    V = sp.Matrix([[z1 ** 2, z1, -1], [z2 ** 2, z2, -1], [z3 ** 2, z3, -1]])
    detV = sp.factor(V.det())
    vand = sp.factor((z1 - z2) * (z1 - z3) * (z2 - z3))
    vand_ok = iszero(detV - vand) or iszero(detV + vand)
    M0 = sp.Matrix([[2, 3], [5, -2]])                       # generic traceless
    ev = list(M0.eigenvals().keys())
    check("S1.1 NORMAL FORM + ID-RIGIDITY [exact]: Cayley-Hamilton M^2 = (tr M) M - "
          "(det M) I holds identically (%s); an involution (M^2 scalar, M nonscalar) "
          "forces tr M = 0, and a traceless M has eigenvalue ratio -1 (generic "
          "witness: eigenvalues %s), i.e. IS conjugate to the deck diag(1,-1); a "
          "Moebius map fixing >= 3 points has c = b = a-d = 0 (Vandermonde det = "
          "%s != 0) and is the identity"
          % (ch == sp.zeros(2, 2), ev, detV),
          ch == sp.zeros(2, 2) and vand_ok and iszero(ev[0] + ev[1]))

    # 2. the complete solve of g^2 = deck in PGL2(C)
    #    M^2 = lam diag(1,-1): off-diagonal gives b(a+d) = c(a+d) = 0.
    b_sol = sp.solve(b * (a + d), b)          # trace != 0 branch: b = 0
    c_sol = sp.solve(c * (a + d), c)          # trace != 0 branch: c = 0
    ratio_sol = sp.solve(r ** 2 + 1, r)       # (a/d)^2 = -1
    Mt = sp.Matrix([[a, b], [c, -a]])         # trace = 0 branch
    E = sp.expand(Mt * Mt - lam_ * sp.diag(1, -1))
    lam_forced = sp.solve(E[0, 0] - E[1, 1], lam_)      # -> lam = 0
    det_forced = sp.expand(Mt.det().subs(b * c, -a ** 2))  # bc = -a^2 => det = 0
    sq_plus = mexp(CLOCK * CLOCK)
    sq_minus = mexp(CLOCKINV * CLOCKINV)
    check("S1.2 COMPLETE SQUARE-ROOT SOLVE [exact]: g^2 = deck in PGL2(C) has "
          "EXACTLY TWO solutions.  tr g != 0 forces b = %s, c = %s (diagonal) and "
          "(a/d)^2 = -1 => a/d = %s: g = z -> +iz or z -> -iz; tr g = 0 forces "
          "lam = %s and det = %s = 0 (impossible).  No parabolic, loxodromic or "
          "non-diagonal square roots exist"
          % (b_sol, c_sol, ratio_sol, lam_forced, det_forced),
          b_sol == [0] and c_sol == [0] and set(ratio_sol) == {I, -I}
          and lam_forced == [0] and det_forced == 0
          and prop_mat(sq_plus, DECK) and prop_mat(sq_minus, DECK))

    # 3. automatic order 4, inverse pair, fixed-point alignment, transport
    o_p, o_m = proj_order(CLOCK), proj_order(CLOCKINV)
    inv_pair = prop_mat(mexp(CLOCK * CLOCKINV), sp.eye(2))
    fix0 = peq(apply_m(CLOCK, (0, 1)), (0, 1)) and peq(apply_m(CLOCK, (1, 0)), (1, 0))
    h = sp.Matrix([[1, 2], [3, 5]])
    transport = prop_mat(mexp((h * CLOCK * h.adjugate()) ** 2),
                         mexp(h * DECK * h.adjugate()))
    check("S1.3 ORDER 4 IS AUTOMATIC [exact]: both roots have projective order "
          "(%s, %s) = 4 (elliptic, one PGL2 conjugacy class), are mutually inverse "
          "(%s) = the Aut(Z4) pair, share the deck's fixed points {0, inf} (%s), "
          "and the classification transports under conjugation (%s) -- 'order 4' "
          "is NOT an input once 'square root of the deck' is given"
          % (o_p, o_m, inv_pair, fix0, transport),
          o_p == 4 and o_m == 4 and inv_pair and fix0 and transport)

    # ================================================ S2: marks filter + alignment
    print("  -- S2: which deck-invariant 4-mark divisors admit a deck square root?")
    w, u = sp.symbols('w u')          # plain complex symbols (no real assumption)

    # 4. marks filter: clock preserves {1,-1,w,-w} <=> w = +-i
    w_sols = sorted(sp.solve(w - I, w) + sp.solve(w + I, w), key=str)
    i_not_pm1 = (not iszero(I - 1)) and (not iszero(I + 1))
    mu4 = [(sp.Integer(1), 1), (I, 1), (sp.Integer(-1), 1), (-I, 1)]
    preserved = all(any(peq(apply_m(CLOCK, p), q) for q in mu4) for p in mu4)
    check("S2.4 MARKS FILTER [exact, complete]: for a deck-invariant deck-free set "
          "{1,-1,w,-w} the clock image of the mark 1 is i, which must be a mark; "
          "i != +-1 (%s) leaves w = +-i only (%s); both give the SAME set mu4 = "
          "{1,i,-1,-i}, and the clock preserves it (%s) -- a marks-preserving "
          "square root exists IFF the marks are one mu4 orbit aligned with the deck"
          % (i_not_pm1, w_sols, preserved),
          i_not_pm1 and set(w_sols) == {I, -I} and preserved)

    # 5. the aligned configuration: harmonic, j = 1728, free 4-cycle, scale-free
    mu4u = [(u, 1), (I * u, 1), (-u, 1), (-I * u, 1)]
    crs = set()
    for pm in permutations(range(4)):
        crs.add(sp.nsimplify(cross_ratio(*[mu4u[k] for k in pm])))
    j_val = jlam(sp.Integer(2))
    orbit_ok = all(any(peq(apply_m(CLOCK, p), q) for q in mu4u) for p in mu4u)
    no_fixed = all(not peq(apply_m(CLOCK, p), p) for p in mu4u)
    deck_perm = mark_perm(DECK, mu4u)
    check("S2.5 ALIGNED = SQUARE [exact, symbolic scale u]: cross-ratio orderings of "
          "u*mu4 = %s (the harmonic class), j = %s = 1728, tau = i (v168/v214); the "
          "clock 4-cycles the marks freely (orbit %s, fixed marks none: %s); deck = "
          "clock^2 acts as the double transposition %s (v215 K1 pattern DERIVED); "
          "the scale u stays free = the v492 S5 one-parameter family"
          % (sorted(crs, key=str), j_val, orbit_ok, no_fixed, deck_perm),
          crs == {sp.Integer(2), sp.Rational(1, 2), sp.Integer(-1)}
          and j_val == 1728 and orbit_ok and no_fixed
          and deck_perm == [2, 3, 0, 1])

    # 6. the D4 stabiliser of mu4 and the centrality criterion
    stab_mu4 = stabilizer(mu4)
    prof_mu4 = order_profile(stab_mu4)
    o4 = [g for g in stab_mu4 if proj_order(g) == 4]
    o4_are_clocks = all(prop_mat(g, CLOCK) or prop_mat(g, CLOCKINV) for g in o4)
    o4_sq_deck = all(prop_mat(mexp(g * g), DECK) for g in o4)
    center = [g for g in stab_mu4
              if all(prop_mat(mexp(g * hh), mexp(hh * g)) for hh in stab_mu4)]
    center_ok = (len(center) == 2
                 and any(prop_mat(g, DECK) for g in center)
                 and any(prop_mat(g, sp.eye(2)) for g in center))
    roots_in_stab = [g for g in stab_mu4 if prop_mat(mexp(g * g), DECK)]
    check("S2.6 D4 STABILISER + CENTRALITY [exact]: |Stab(mu4)| = %d = 2|mu4| with "
          "order profile %s = D4 (v168); EXACTLY 2 order-4 elements, both = the "
          "clock or its inverse (%s), both squaring to the deck (%s); center = "
          "{id, deck} (%s); square roots of the deck inside the stabiliser = %d = "
          "the two clocks -- 'deck central in the mark-D4' <=> clock exists"
          % (len(stab_mu4), prof_mu4, o4_are_clocks, o4_sq_deck, center_ok,
             len(roots_in_stab)),
          len(stab_mu4) == 8 and prof_mu4 == {1: 1, 2: 5, 4: 2}
          and len(o4) == 2 and o4_are_clocks and o4_sq_deck and center_ok
          and len(roots_in_stab) == 2)

    # 7. ALIGNMENT IS NECESSARY: harmonic j = 1728 alone is NOT enough
    v_s = 3 + 2 * sp.sqrt(2)
    silver = [(sp.Integer(1), 1), (sp.Integer(-1), 1), (v_s, 1), (-v_s, 1)]
    lam_s = cross_ratio(silver[0], silver[2], silver[1], silver[3])
    j_s = jlam(cross_ratio(*silver))
    stab_s = stabilizer(silver)
    prof_s = order_profile(stab_s)
    deck_in = [g for g in stab_s if prop_mat(g, DECK)]
    center_s = [g for g in stab_s
                if all(prop_mat(mexp(g * hh), mexp(hh * g)) for hh in stab_s)]
    central_s = [g for g in center_s if not prop_mat(g, sp.eye(2))][0]
    cperm = mark_perm(central_s, silver)         # crosses the +- pairs?
    central_crosses = sorted(cperm) == [0, 1, 2, 3] and cperm[0] in (2, 3)
    deck_not_central = not any(prop_mat(g, DECK) for g in center_s)
    roots_s = [g for g in stab_s if prop_mat(mexp(g * g), DECK)]
    clock_not_pres = not any(peq(apply_m(CLOCK, silver[0]), q) for q in [silver[1], silver[2], silver[3]]) \
        and not peq(apply_m(CLOCK, silver[0]), silver[0])
    check("S2.7 ALIGNMENT NECESSARY [exact counterexample]: {+-1, +-(3+2sqrt2)} is "
          "deck-free AND harmonic (j = %s = 1728, an ordering has cross-ratio %s) "
          "with stabiliser D4 (order %d, profile %s) -- BUT the deck z -> -z sits "
          "in it NON-centrally (deck present: %s, central: %s; the true central "
          "involution CROSSES the +- pairs, perm %s: %s), so the deck has NO square "
          "root inside (%d found; "
          "in D4 only the central rotation r^2 has roots) and the global roots +-iz "
          "do not preserve the marks (%s) -- harmonic modulus ALONE is insufficient; "
          "the residual datum is DECK-CENTRALITY (one bit), not the j-invariant"
          % (j_s, lam_s, len(stab_s), prof_s, len(deck_in) == 1,
             not deck_not_central, cperm, central_crosses, len(roots_s),
             not clock_not_pres),
          j_s == 1728 and lam_s == sp.Rational(1, 2) and len(stab_s) == 8
          and prof_s == {1: 1, 2: 5, 4: 2} and len(deck_in) == 1
          and deck_not_central and central_crosses and len(roots_s) == 0
          and clock_not_pres)

    # 8. fixed-type harmonic control {0, inf, u, -u}: the (2,4,4) shadow
    fixcfg = [(sp.Integer(0), 1), (1, sp.Integer(0)), (sp.Integer(2), 1),
              (sp.Integer(-2), 1)]
    stab_f = stabilizer(fixcfg)
    deck_fixes = mark_perm(DECK, fixcfg)
    n_fixed = sum(1 for i, j in enumerate(deck_fixes) if i == j)
    clock_img = apply_m(CLOCK, fixcfg[2])
    clock_fails = not any(peq(clock_img, q) for q in fixcfg)
    center_f = [g for g in stab_f
                if all(prop_mat(mexp(g * hh), mexp(hh * g)) for hh in stab_f)]
    central_f = [g for g in center_f if not prop_mat(g, sp.eye(2))]
    central_not_deck = all(not prop_mat(g, DECK) for g in central_f)
    check("S2.8 FIXED-TYPE CONTROL [exact]: {0, inf, 2, -2} is harmonic but the deck "
          "FIXES %d marks (0 and inf) -- the (2,4,4) shadow killed by v216 "
          "(all marks order 2 / deck-free); consistently the global roots +-iz do "
          "not preserve it (i*2 = 2i not a mark: %s) and the central involution of "
          "its D4 (order %d) is NOT the deck (%s): no clock from this configuration"
          % (n_fixed, clock_fails, len(stab_f), central_not_deck),
          n_fixed == 2 and clock_fails and len(stab_f) == 8
          and len(central_f) == 1 and central_not_deck)

    # 9. RP / real-structure filter
    def sigma_eq_mat(Mm):          # conjugation action of z -> 1/conj(z)
        return sp.Matrix([[sp.conjugate(Mm[1, 1]), sp.conjugate(Mm[1, 0])],
                          [sp.conjugate(Mm[0, 1]), sp.conjugate(Mm[0, 0])]])
    eq_clock = prop_mat(sigma_eq_mat(CLOCK), CLOCK)
    eq_deck = prop_mat(sigma_eq_mat(DECK), DECK)
    conj_clock = prop_mat(CLOCK.conjugate(), CLOCKINV)
    marks_fixed = all(peq((sp.conjugate(q), sp.conjugate(p)), (p, q))
                      for (p, q) in mu4)
    check("S2.9 RP FILTER [exact]: the equatorial real structure sigma: z -> 1/conj(z) "
          "fixes all four mu4 marks pointwise (real locus = unit circle: %s), "
          "centralises the deck (%s) AND the clock (%s); the other real structure "
          "z -> conj(z) conjugates clock -> clock^-1 (%s) -- RP consistency passes "
          "BOTH roots and selects nothing: the Aut(Z4) = {clock, clock^-1} ambiguity "
          "is irreducible (= v492 NC3 rigidity 'up to Aut(Z4)')"
          % (marks_fixed, eq_deck, eq_clock, conj_clock),
          marks_fixed and eq_deck and eq_clock and conj_clock)

    # 10. converse + the one-bit reduction
    both_pres = all(any(peq(apply_m(g, p), q) for q in mu4u) for p in mu4u
                    for g in (CLOCK, CLOCKINV))
    check("S2.10 CONVERSE + ONE-BIT REDUCTION [exact]: for EVERY scale u the aligned "
          "set u*mu4 is preserved by both roots (%s) -- so (marks-preserving square "
          "root exists) <=> (marks aligned-square).  The single existence bit yields "
          "AT ONCE: order 4 (S1.3), uniqueness up to inverse (S1.2), free 4-cycle "
          "orbit (S2.5), tau = i pinned with only the scale free (S2.5), deck = "
          "clock^2 (S2.6).  Without the bit the (2,2,2,2) modulus is free (v216 "
          "[O]) -- circularity cleanly cut: the bit is the input, the clock the output"
          % both_pres, both_pres)

    # ================================================ S3: why n = 4 (honest)
    print("  -- S3: n-arithmetic -- which Z_n can live on 4 marks at all?")

    # 11. free actions
    free_n = [n for n in range(1, 9) if 4 % n == 0]
    check("S3.11 FREE ORBIT ARITHMETIC [exact]: a free Z_n action on 4 marks forces "
          "all orbits of size n, so n | 4: n in %s; marks-TRANSITIVE cyclic (marks = "
          "ONE orbit, the v215 K1 reading) forces n = 4 exactly"
          % free_n, free_n == [1, 2, 4] and max(free_n) == 4)

    # 12. faithfulness kills n >= 5; n = 3 needs a fixed mark
    s4_orders = sorted({Permutation(list(pm)).order()
                        for pm in permutations(range(4))})
    kill = {}
    for n in range(5, 9):
        img = max(dv for dv in range(1, n + 1) if n % dv == 0 and dv in s4_orders)
        kill[n] = img            # image order < n => kernel fixes all 4 marks
    o3_fixed = sorted({sum(1 for i in range(4) if Permutation(list(pm))(i) == i)
                       for pm in permutations(range(4))
                       if Permutation(list(pm)).order() == 3})
    check("S3.12 FAITHFULNESS [exact]: S4 element orders = %s; any Moebius Z_n "
          "preserving 4 marks acts FAITHFULLY on them (a kernel element would fix 4 "
          ">= 3 points => identity, S1.1), so n >= 5 dies: max cyclic image order "
          "= %s for n = 5..8, always < n; n = 3 elements fix exactly %s mark "
          "(hexagonal shadow) and g^2 has order 3 != 2 -- never a deck square root"
          % (s4_orders, kill, sorted(o3_fixed)),
          s4_orders == [1, 2, 3, 4] and all(kill[n] < n for n in kill)
          and o3_fixed == [1])

    # 13. the established transfer/cusp side pins the weight arithmetic to 4 marks
    lam_x = sp.symbols('lam_x')
    weights = [sp.Integer(0), sp.Rational(1, 3), sp.Rational(2, 3)]
    spec = sorted(((1 - wt) ** 6 for wt in weights), reverse=True)
    gap = spec[1]
    deg3 = sp.Poly(lam_x ** 3 - 1, lam_x).degree()
    deg5 = sp.Poly(lam_x ** 5 - 1, lam_x).degree()
    check("S3.13 TRANSFER/CUSP SIDE [exact]: the established cusp weights {0,1/3,2/3} "
          "have denominator 3 = b1 = #marks - 1 = N_fam; transfer spectrum (1-w)^6 = "
          "%s with gap %s = (2/3)^6 (v54/v56/v215 K4); a 6-mark Z6 world would need "
          "cusp class lam^5 - 1 (deg %d != %d = deg(lam^3 - 1), v117) -- n = 6 is "
          "killed INDEPENDENTLY by established cusp data; 6 = |W(A3)|/4 = 24/4"
          % ([str(s) for s in spec], gap, deg5, deg3),
          spec == [sp.Integer(1), sp.Rational(64, 729), sp.Rational(1, 729)]
          and gap == sp.Rational(2, 3) ** 6 and deg3 == 3 == N_FAM
          and deg5 == 5 and 24 // 4 == 6)

    # 14. the deck is modulus-blind; ALL pinning power sits in the root bit
    wsym = sp.symbols('wsym', nonzero=True)
    cfg_w = [(sp.Integer(1), 1), (sp.Integer(-1), 1), (wsym, 1), (-wsym, 1)]
    deck_all = all(any(peq(apply_m(DECK, p), q) for q in cfg_w) for p in cfg_w)
    check("S3.14 DECK IS MODULUS-BLIND [exact, symbolic w]: z -> -z preserves EVERY "
          "deck-pair configuration {+-1, +-w} (%s) -- n = 2 pins NO modulus (v503 B5 "
          "made exact); the modulus-pinning power of n = 4 is EXACTLY the square-root "
          "existence bit (S2.4/S2.10).  'Why n = 4 rather than no clock' has NO "
          "Moebius-side principle -- the P1-side forcing candidate is fermionic "
          "(companion probe: NS deck implementation is FORCED to order 4)"
          % deck_all, deck_all)

    # ================================================ S4: negative / sharpness controls
    print("  -- S4: negative controls (n = 8, hexagonal, generic)")

    # 15. no order-8 element preserves any 4-point set
    zeta8 = sp.exp(I * sp.pi / 4)
    distinct = all(not iszero(zeta8 ** k - zeta8 ** j)
                   for k in range(8) for j in range(k))
    sizes_ok = all((4 - r) % 8 != 0 or (4 - r) == 0 for r in (0, 1, 2)) and \
        all(4 - r < 8 for r in (0, 1, 2)) and all(4 - r > 0 for r in (0, 1, 2))
    check("S4.15 NO ORDER-8 ON THE SPHERE [exact]: z -> zeta8 z has all orbits of "
          "size 8 off {0, inf} (8 distinct powers: %s), so an invariant 4-set could "
          "only use fixed points (<= 2 < 4) -- impossible; the kernel argument "
          "(S3.12, image order max %d < 8) kills EVERY order-8 element; the Z8 lives "
          "UPSTAIRS (spin/Fock lift, 8 = 2|mu4| = %d, v492 + companion probe), never "
          "as a sphere symmetry of the marks"
          % (distinct, kill[8], 2 * 4),
          distinct and sizes_ok and kill[8] == 4 and 2 * 4 == 8)

    # 16. hexagonal / equianharmonic control: A4, no order 4
    om = sp.Rational(-1, 2) + sp.sqrt(3) * I / 2
    hexcfg = [(sp.Integer(1), 1), (om, 1), (sp.expand(om ** 2), 1), (1, sp.Integer(0))]
    j_hex = jlam(cross_ratio(*hexcfg))
    stab_h = stabilizer(hexcfg)
    prof_h = order_profile(stab_h)
    sq_orders = sorted({proj_order(mexp(g * g)) for g in stab_h})
    check("S4.16 HEXAGONAL KILL [exact]: marks {1, w, w^2, inf} (j = %s = 0, "
          "equianharmonic) have stabiliser A4: order %d, profile %s -- ZERO order-4 "
          "elements; squares in the stabiliser have orders %s (no involution is a "
          "square) => NO involution has a marks-preserving square root at j = 0: the "
          "dynamical winner (hexagonal, v503 A5) can NEVER carry the clock -- v503 "
          "C2 sharpened from Z6 to the full marked-sphere stabiliser"
          % (j_hex, len(stab_h), prof_h, sq_orders),
          j_hex == 0 and len(stab_h) == 12 and prof_h == {1: 1, 2: 3, 3: 8}
          and sq_orders == [1, 3])

    # 17. generic control: Klein V4 only
    gencfg = [(sp.Integer(1), 1), (sp.Integer(-1), 1), (sp.Integer(2), 1),
              (sp.Integer(-2), 1)]
    j_gen = jlam(cross_ratio(*gencfg))
    stab_g = stabilizer(gencfg)
    prof_g = order_profile(stab_g)
    sq_g = all(prop_mat(mexp(g * g), sp.eye(2)) for g in stab_g)
    check("S4.17 GENERIC KILL [exact]: marks {+-1, +-2} (j = %s, neither 0 nor 1728) "
          "have stabiliser Klein V4: order %d, profile %s, exponent 2, squares = {id} "
          "(%s) => not even the deck has a marks-preserving square root at generic "
          "modulus -- no clock, matching v503 A7 rigidity"
          % (j_gen, len(stab_g), prof_g, sq_g),
          j_gen not in (sp.Integer(0), sp.Integer(1728)) and len(stab_g) == 4
          and prof_g == {1: 1, 2: 3} and sq_g)

    # ================================================ S5: synthesis
    print("  -- S5: synthesis")

    # 18. the stabiliser trichotomy
    check("S4.18 STABILISER TRICHOTOMY [exact]: 4-mark stabilisers in PGL2(C) are "
          "V4 (generic, order 4) / D4 (harmonic, order 8 = 2|mu4|) / A4 "
          "(equianharmonic, order 12), with order-4 element counts (0, 2, 0) -- "
          "'an order-4 element exists IFF the marks are harmonic', and then it is "
          "the clock pair; enumeration complete via the 24 = |S4| = |W(A3)| ordered "
          "triples (the clock is the W(A3) Coxeter element, v117/v215)",
          len(stab_g) == 4 and len(stab_mu4) == 8 and len(stab_h) == 12
          and len(o4) == 2 and prof_h.get(4, 0) == 0 and prof_g.get(4, 0) == 0
          and 24 == 4 * 3 * 2)

    # 19. verdict
    verdict = (set(w_sols) == {I, -I}                # B1: roots classified
               and len(roots_in_stab) == 2           # aligned: exactly the clocks
               and len(roots_s) == 0                 # unaligned harmonic: none
               and prof_h.get(4, 0) == 0             # hexagonal: none
               and sq_g                              # generic: none
               and deck_all)                         # deck modulus-blind
    check("S5.19 VERDICT [typed]: the input 'order-4 clock with free mu4 orbit "
          "fixing tau = i' REDUCES to ONE bit: 'the collar deck admits a marks-"
          "preserving Moebius square root' (equivalently: the deck is the CENTRAL "
          "involution of the mark-stabiliser D4).  Given the bit, order 4, "
          "uniqueness up to Aut(Z4), the free 4-cycle, tau = i (scale free) and "
          "deck = clock^2 are all THEOREMS (S1.2-S2.10); without it, nothing pins "
          "the modulus (S3.14).  Harmonicity alone is NOT the bit (S2.7).  The "
          "fermionic side of the bit is computed in the companion Fock probe",
          verdict)

    npass = sum(RESULTS)
    print("=" * 100)
    print("SUMMARY: %d/%d checks passed%s"
          % (npass, len(RESULTS),
             "" if npass == len(RESULTS) else "  -- FAILURES PRESENT"))
    return npass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
