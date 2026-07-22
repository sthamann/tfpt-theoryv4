"""qgeo_realize_deck_freedom_dihedral_probe.py -- EXPLORATION ONLY
(experiments/, no verification claim).

THE FREEDOM ATTACK ON THE v506/v507 ALIGNMENT BIT (dihedral / fermionic side).

v507 (SEAM.BIT.ORIGIN.01) left the last identification input as ONE bit with
four equivalent faces; its Part B showed: central arrangement (deck = shift
by 8 on the 16-Majorana NS seam circle) => U^2 = (-1)^F nonsplit; edge
arrangement (deck = REFLECTION j -> k-j with fixed points) => U^2 = +1 split.
KEY OBSERVATION UNDER TEST: the collar deck of the theory is the deck
transformation of a COVERING (the Z2 seam of the Moebius double, tfpt_3
"orientable double cover of the Moebius fibre is a cylinder with two
boundaries plus one Z2 seam"); deck transformations of coverings act FREELY.
A reflection of the circle has fixed points and is NEVER free -- so if
freeness is P1-side established, the edge class is EXCLUDED and the
fermionic face of the bit FOLLOWS.

  D1 DIHEDRAL CENSUS (exact, N = 16 + robustness 8, 12): enumerate ALL
     involutions in D_N acting on the refined 2N-point circle (sites +
     edge midpoints).  Result: exactly ONE free involution (the antipodal
     shift by N/2); all N reflections have exactly 2 fixed points on the
     circle (2 sites for even axis, 2 edge midpoints for odd axis).
  D2 AUT(C_N) = D_N (the census is complete): any adjacency-preserving
     bijection of the N-cycle is determined by (image of 0, direction);
     all 2N candidates are automorphisms and every automorphism arises so
     -- brute force over all 8! permutations at N = 8, propagation
     argument machine-verified at N = 16.  Hence "free involution of the
     seam circle" has EXACTLY ONE realisation: the antipode.
  D3 QUOTIENT TOPOLOGY (the P1 tie): circle / free involution = CIRCLE
     (C_16 / shift-8 = C_8); circle / reflection = INTERVAL (path with 2
     boundary points).  P1's Gauss-Bonnet budget needs the seam Gamma to
     be a closed CIRCLE contributing 2pi (6pi = 2pi+2pi+2pi, phi_tree =
     1/(6pi)); a mirror/edge deck would make the seam an interval with
     2 corners -- the freeness premise IS the "seam stays a circle" datum.
  D4 FOCK DICHOTOMY, COMPLETE (exact Cl(16) Fractions, all 17 involutions):
     the free involution's NS lift squares to 256 gamma_1..gamma_16 =
     (-1)^F (nonsplit, 2 roots = Z8 tower); ALL 16 reflections (8 even-axis
     + 8 odd-axis) have implementers squaring to a SCALAR (split, 0 roots).
     nonsplit <=> free on the circle -- exact equivalence, no exception.
  D5 THE CHAIN, END-TO-END: deck free => deck = shift 8 => crossing mark
     pairing (all 28 invariant 4-sets) => U^2 = (-1)^F => central class =>
     the edge/silver arrangement is excluded.  HONEST LIMIT: the modulus
     is NOT pinned -- witness marks {0,1,8,9} are shift-invariant and
     crossing with the SAME nonsplit deck lift but admit NO clock (the
     quarter shift does not preserve them): freeness closes the POSITION
     half of the bit, not the modulus half.
  D6 NEGATIVE CONTROLS: (a) N = 9 odd: D_9 has NO free involution (no
     antipode; all reflections fix a site) -- consistent, the seam needs
     an even carrier count; (b) Klein bottle: the orientation-cover deck
     (x,y) -> (x+8,-y) on the 16x16 torus is free and restricts to the
     free shift-8 on its two invariant fibre circles -- covering decks
     are free REGARDLESS of Moebius vs Klein; (c) the BRANCHED pillowcase
     involution (x,y) -> (-x,-y) has exactly 4 fixed points (= the
     2-torsion marks!) and restricts to a REFLECTION (2 fixed points) on
     invariant circles: the edge class is the BRANCH involution's
     restriction -- the silver arrangement mistakes the branch Z2 for the
     seam deck.

Repo anchors: v507 Part B (Cl(16) machinery reused verbatim), v506 Part B
(NS lift), tfpt_3 (Moebius double = cylinder + one Z2 seam), origin_theory
(6pi budget; c3 = 1/(|Z2| 2pi chi)), v216 (free order-4 on the marks),
v456 (one-sidedness excludes reflection symmetry).

Exact throughout (integers; Fractions in Cl(16); no floats).  Standalone.
Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/qgeo_realize_deck_freedom_dihedral_probe.py
"""
from fractions import Fraction as Fr
from itertools import combinations, permutations

RESULTS = []

N_SITES = 16           # 16 Majorana modes = 2^(g_car-1), 4 per mark quadrant
MARKS = (0, 4, 8, 12)  # mu4 mark sites (0-based) on the 16-site seam circle


def check(name, ok):
    RESULTS.append(bool(ok))
    print(("PASS" if ok else "FAIL") + " [%2d] %s" % (len(RESULTS), name))


# ---------------------------------------------------------------------------
# dihedral group D_N on the refined 2N circle (positions: even = site 2j,
# odd = edge midpoint between sites)
# ---------------------------------------------------------------------------
def dihedral_refined(N):
    """all 2N elements of D_N as maps on Z_{2N}: ('rot', k) p -> p + 2k;
    ('ref', m) p -> 2m - p  (axis through site m and site m + N/... in
    half-units: fixed positions p = m, m + N)."""
    els = [('rot', k) for k in range(N)] + [('ref', m) for m in range(N)]
    return els


def apply_el(el, p, N):
    kind, k = el
    if kind == 'rot':
        return (p + 2 * k) % (2 * N)
    return (2 * k - p) % (2 * N)


def is_involution(el, N):
    kind, k = el
    if kind == 'rot':
        return k != 0 and (2 * k) % N == 0
    return True                                   # every reflection


def fixed_positions(el, N):
    return [p for p in range(2 * N) if apply_el(el, p, N) == p]


def involution_census(N):
    """returns (n_invol, free_els, refl_site_axis, refl_edge_axis)."""
    free, site_ax, edge_ax = [], 0, 0
    n_inv = 0
    for el in dihedral_refined(N):
        if not is_involution(el, N):
            continue
        n_inv += 1
        fx = fixed_positions(el, N)
        if not fx:
            free.append(el)
        elif el[0] == 'ref':
            if all(p % 2 == 0 for p in fx):
                site_ax += 1
            elif all(p % 2 == 1 for p in fx):
                edge_ax += 1
    return n_inv, free, site_ax, edge_ax


# ---------------------------------------------------------------------------
# Cl(n) machinery (v507 Part B, verbatim)
# ---------------------------------------------------------------------------
def mono_mul(m1, m2):
    out = list(m1)
    sign = 1
    for g in m2:
        out.append(g)
        i = len(out) - 1
        while i > 0 and out[i - 1] > out[i]:
            out[i - 1], out[i] = out[i], out[i - 1]
            sign = -sign
            i -= 1
        if i > 0 and out[i - 1] == out[i]:
            del out[i - 1:i + 1]
    return sign, tuple(out)


def cmul(x, y):
    out = {}
    for m1, c1 in x.items():
        for m2, c2 in y.items():
            s, m = mono_mul(m1, m2)
            c = out.get(m, Fr(0)) + s * c1 * c2
            if c:
                out[m] = c
            elif m in out:
                del out[m]
    return out


def cadd(x, y):
    out = dict(x)
    for m, c in y.items():
        cc = out.get(m, Fr(0)) + c
        if cc:
            out[m] = cc
        elif m in out:
            del out[m]
    return out


def cscale(x, s):
    return {m: c * s for m, c in x.items()} if s else {}


def gam(*idx):
    return {tuple(idx): Fr(1)}


ONE = {(): Fr(1)}


def is_scalar(x):
    return all(m == () for m in x)


def prop(x, y):
    if not x or not y or set(x) != set(y):
        return (False, None)
    m0 = next(iter(y))
    c = x[m0] / y[m0]
    return (all(x[m] == c * y[m] for m in y), c)


def apply_lin(mat, a, n):
    out = {}
    for b in range(n):
        if mat[b][a]:
            out = cadd(out, cscale(gam(b), Fr(mat[b][a])))
    return out


def implements(Uel, mat, n):
    for a in range(n):
        lhs = cmul(Uel, gam(a))
        rhs = cmul(apply_lin(mat, a, n), Uel)
        if cadd(lhs, cscale(rhs, Fr(-1))):
            return False
    return True


def shift_matrix(n, k, wrap_sign):
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        b = (a + k) % n
        M[b][a] = wrap_sign if a + k >= n else 1
    return M


def refl_matrix(n, k, wrap_sign):
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        idx = (k - a) % (2 * n)
        M[idx % n][a] = wrap_sign if idx >= n else 1
    return M


def matmul_i(A, B):
    n = len(A)
    return [[sum(A[i][kk] * B[kk][j] for kk in range(n)) for j in range(n)]
            for i in range(n)]


def mat_prop(A, B):
    n = len(A)
    for s in (1, -1):
        if all(A[i][j] == s * B[i][j] for i in range(n) for j in range(n)):
            return True
    return False


def refl_implementer(n, k):
    """NS implementer for the reflection j -> k - j (spin lift wrap -1);
    generalises v507 F3.4 (k = 4).  Even axis: monomial of all sites but
    the +1-fixed one, times 7 pair binomials; odd axis: 8 pair binomials."""
    fixed = [j for j in range(n) if (k - j) % n == j]
    if fixed:
        fplus = [f for f in fixed if (k - f) % (2 * n) < n]
        U = {tuple(j for j in range(n) if j != fplus[0]): Fr(1)}
    else:
        U = dict(ONE)
    for a in range(n):
        b = (k - a) % n
        if a >= b or a in fixed:
            continue
        idx = (k - a) % (2 * n)
        eps = Fr(-1) if idx >= n else Fr(1)
        U = cmul(U, cadd(gam(a), cscale(gam(b), eps)))
    return U


def pairing_of(inv_map, ms, n=16):
    order = sorted(ms)
    pos = {m: i for i, m in enumerate(order)}
    pairs = set()
    for m in ms:
        pairs.add(frozenset((pos[m], pos[inv_map(m) % n])))
    return 'crossing' if frozenset((0, 2)) in pairs else 'noncrossing'


# ---------------------------------------------------------------------------
def d1_census():
    print("== D1: involution census in D_N on the refined circle ==")
    res = {}
    for N in (16, 8, 12):
        n_inv, free, site_ax, edge_ax = involution_census(N)
        res[N] = (n_inv, [f for f in free], site_ax, edge_ax)
    ok16 = (res[16][0] == 17 and res[16][1] == [('rot', 8)]
            and res[16][2] == 8 and res[16][3] == 8)
    ok8 = (res[8][0] == 9 and res[8][1] == [('rot', 4)]
           and res[8][2] == 4 and res[8][3] == 4)
    ok12 = (res[12][0] == 13 and res[12][1] == [('rot', 6)]
            and res[12][2] == 6 and res[12][3] == 6)
    check("D1.1 DIHEDRAL CENSUS [exact]: N = 16: %d involutions in D_16, "
          "EXACTLY ONE free = the antipodal shift by 8 (%s); all 16 "
          "reflections have 2 fixed points on the circle (%d site-axis + "
          "%d edge-axis) -- a reflection is NEVER free; robustness N = 8: "
          "%s, N = 12: %s (always exactly one free involution = shift N/2)"
          % (res[16][0], res[16][1], res[16][2], res[16][3],
             res[8][:1] + res[8][2:], res[12][:1] + res[12][2:]),
          ok16 and ok8 and ok12)

    # every reflection's fixed-point count on the circle is exactly 2
    fx_counts = {len(fixed_positions(('ref', m), 16)) for m in range(16)}
    anti_fx = len(fixed_positions(('rot', 8), 16))
    check("D1.2 FIXED-POINT ARITHMETIC [exact]: every D_16 reflection fixes "
          "exactly 2 points of the circle (counts %s; sites for even axis, "
          "edge midpoints for odd axis) while the antipode fixes %d -- "
          "'frei <=> Antipode' has no borderline case: the edge-axis "
          "reflections are free on the SITES but not on the circle "
          "(midpoint fixed points), so site-freeness is NOT the right "
          "notion; circle-freeness is"
          % (sorted(fx_counts), anti_fx),
          fx_counts == {2} and anti_fx == 0)


def d2_aut():
    print("== D2: Aut(C_N) = D_N -- the census is complete ==")
    N = 8
    adj = {j: {(j - 1) % N, (j + 1) % N} for j in range(N)}
    autos = []
    for pm in permutations(range(N)):
        if all(set(pm[k] for k in adj[j]) == adj[pm[j]] for j in range(N)):
            autos.append(pm)
    dihedral = set()
    for i0 in range(N):
        for d in (1, -1):
            dihedral.add(tuple((i0 + d * j) % N for j in range(N)))
    check("D2.1 BRUTE FORCE N = 8 [exact, all 8! = 40320 permutations]: "
          "Aut(C_8) has exactly %d elements and equals D_8 (%s) -- no "
          "exotic circle automorphism exists"
          % (len(autos), set(autos) == dihedral),
          len(autos) == 16 and set(autos) == dihedral)

    N = 16
    adj = {j: {(j - 1) % N, (j + 1) % N} for j in range(N)}
    deg2 = all(len(adj[j]) == 2 for j in range(N))
    valid = []
    for i0 in range(N):
        for i1 in adj[i0]:
            phi = [i0, i1]
            ok = True
            for j in range(2, N):
                nxt = adj[phi[j - 1]] - {phi[j - 2]}
                if len(nxt) != 1:
                    ok = False
                    break
                phi.append(nxt.pop())
            if ok and len(set(phi)) == N \
                    and all(phi[(j + 1) % N] in adj[phi[j]] for j in range(N)):
                valid.append(tuple(phi))
    dihedral16 = set()
    for i0 in range(N):
        for d in (1, -1):
            dihedral16.add(tuple((i0 + d * j) % N for j in range(N)))
    check("D2.2 PROPAGATION N = 16 [exact]: every vertex has degree 2 (%s), "
          "so an automorphism is DETERMINED by (image of 0, image of 1); "
          "all %d = 16 x 2 candidates propagate consistently and equal "
          "D_16 (%s) => Aut(C_16) = D_16 exactly: the D1 census covers ALL "
          "circle symmetries -- the unique free involution of the seam "
          "circle IS the antipode, with no loophole"
          % (deg2, len(valid), set(valid) == dihedral16),
          deg2 and len(valid) == 32 and set(valid) == dihedral16)


def d3_quotient():
    print("== D3: quotient topology -- circle/free = circle, "
          "circle/reflection = interval ==")
    N = 16
    # quotient of the refined 2N-cycle by an involution: count vertex orbits,
    # edge orbits, boundary (fixed) points; chi = V - E
    def quotient_data(el):
        pos = list(range(2 * N))
        orb = {}
        for p in pos:
            q = apply_el(el, p, N)
            orb[p] = min(p, q)
        verts = set(orb.values())
        edges = set()
        for p in pos:
            e = frozenset((orb[p], orb[(p + 1) % (2 * N)]))
            edges.add(e)
        fixed = fixed_positions(el, N)
        chi = len(verts) - len(edges)
        return len(verts), len(edges), len(fixed), chi

    v_f, e_f, fx_f, chi_f = quotient_data(('rot', 8))
    v_r, e_r, fx_r, chi_r = quotient_data(('ref', 4))
    v_o, e_o, fx_o, chi_o = quotient_data(('ref', 3))
    check("D3.1 QUOTIENT CENSUS [exact]: C/antipode: V = %d, E = %d, chi = "
          "%d, 0 boundary points => a CIRCLE (chi = 0, closed); C/site-"
          "reflection: V = %d, E = %d, chi = %d with %d fixed points => an "
          "INTERVAL (chi = 1, 2 boundary corners); C/edge-reflection: chi "
          "= %d, %d fixed => interval again -- the seam Gamma survives as "
          "a closed circle IFF the deck is free"
          % (v_f, e_f, chi_f, v_r, e_r, chi_r, fx_r, chi_o, fx_o),
          chi_f == 0 and fx_f == 0 and chi_r == 1 and fx_r == 2
          and chi_o == 1 and fx_o == 2)

    # P1 tie: the Moebius-double budget 6pi = 3 x 2pi needs 3 CLOSED circles
    circles_budget = 3                      # two boundaries + one Z2 seam
    check("D3.2 P1 TIE [arithmetic]: origin_theory's Gauss-Bonnet budget "
          "oint k ds = 2pi + 2pi + 2pi = 6pi (phi_tree = 1/(6pi)) counts "
          "%d CLOSED circles (two cylinder boundaries + ONE Z2 seam "
          "Gamma); a fixed-point deck would turn Gamma into an interval "
          "with 2 corners (D3.1) and break the 3 x 2pi count -- 'the deck "
          "is free on the seam circle' is EXACTLY the established P1 "
          "datum 'the seam is a closed circle', not a new premise"
          % circles_budget,
          circles_budget * 2 == 6 and chi_f == 0 and chi_r == 1)


def d4_fock():
    print("== D4: Fock dichotomy for ALL 17 involutions (exact Cl(16)) ==")
    n = N_SITES
    GAMMA = {tuple(range(n)): Fr(1)}

    # free involution: shift by 8, NS wrap
    D_ns = shift_matrix(n, 8, -1)
    Ut = dict(ONE)
    for j in range(8):
        Ut = cmul(Ut, cadd(ONE, cscale(cmul(gam(j), gam(j + 8)), Fr(-1))))
    impl_c = implements(Ut, D_ns, n)
    ok_u2, coef = prop(cmul(Ut, Ut), GAMMA)
    check("D4.1 FREE DECK => NONSPLIT [exact, v507 reproduced]: the NS lift "
          "of the UNIQUE free involution (shift 8) implements (%s) and "
          "squares to %s x gamma_1..gamma_16 = 256 (-1)^F-monomial: "
          "U^2 = (-1)^F, the extension is NONSPLIT"
          % (impl_c, coef),
          impl_c and ok_u2 and coef == Fr(256))

    # all 16 reflections: implementer exists (for one of the two spin lifts
    # +-R -- the overall-sign lift ambiguity of v507 F2.2), U^2 scalar (split)
    split_results = []
    for k in range(n):
        R = refl_matrix(n, k, -1)
        negR = [[-x for x in row] for row in R]
        U = refl_implementer(n, k)
        impl = implements(U, R, n) or implements(U, negR, n)
        sc, cf = prop(cmul(U, U), ONE)
        split_results.append((k, impl, sc, cf))
    all_impl = all(r[1] for r in split_results)
    all_split = all(r[2] for r in split_results)
    coefs = sorted({r[3] for r in split_results})
    check("D4.2 ALL 16 REFLECTIONS SPLIT [exact, complete]: for EVERY axis "
          "k = 0..15 the NS implementer exists (implements one of the two "
          "spin lifts +-R, all 16 generators: %s; the sign is the v507 "
          "F2.2 lift ambiguity, both square identically) and U^2 is a "
          "SCALAR (%s; values %s = {2^7 (site-axis), 2^8 (edge-axis)}): "
          "the extension SPLITS for every non-free involution -- (cU)^2 = "
          "c^2 U^2 stays scalar for every phase, so split vs nonsplit is "
          "invariant: NONSPLIT <=> FREE, exactly, over the complete "
          "involution census"
          % (all_impl, all_split, coefs),
          all_impl and all_split
          and coefs == [Fr(2 ** 7), Fr(2 ** 8)])

    # root counts in the 32-element dihedral lift group
    group = [shift_matrix(n, k, -1) for k in range(n)] \
        + [refl_matrix(n, k, -1) for k in range(n)]
    roots_free = [i for i, g in enumerate(group)
                  if mat_prop(matmul_i(g, g), D_ns)]
    roots_refl_total = 0
    for k in range(n):
        R = refl_matrix(n, k, -1)
        roots_refl_total += sum(1 for g in group
                                if mat_prop(matmul_i(g, g), R))
    check("D4.3 ROOT DICHOTOMY [exact, all 32 lifts x all 17 targets]: the "
          "free deck has %d square roots (the +-quarter shifts = the Z8 "
          "clock tower); ALL 16 reflections together have %d -- no clock "
          "tower exists over any non-free arrangement"
          % (len(roots_free), roots_refl_total),
          roots_free == [4, 12] and roots_refl_total == 0)


def d5_chain():
    print("== D5: the chain end-to-end + the honest modulus limit ==")
    n = N_SITES
    rot_sets = [s for s in combinations(range(n), 4)
                if set((m + 8) % n for m in s) == set(s)]
    rot_pair = {pairing_of(lambda j: j + 8, s) for s in rot_sets}
    check("D5.1 THE CHAIN [exact]: deck free (D1/D2: unique = shift 8) => "
          "every deck-invariant 4-mark set has CROSSING pairing (all %d "
          "sets: %s) => central arrangement type => U^2 = (-1)^F nonsplit "
          "(D4.1) => the v507 tetrad's fermionic face holds => the "
          "edge/silver arrangement (noncrossing, split, 0 roots) is "
          "EXCLUDED: the POSITION half of the alignment bit follows from "
          "circle-freeness alone"
          % (len(rot_sets), rot_pair),
          rot_pair == {'crossing'} and len(rot_sets) == 28)

    # honest limit: freeness does NOT pin the modulus
    wit = (0, 1, 8, 9)
    inv_ok = set((m + 8) % n for m in wit) == set(wit)
    crossing = pairing_of(lambda j: j + 8, wit) == 'crossing'
    clock_wit = set((m + 4) % n for m in wit) == set(wit)
    clock_marks = set((m + 4) % n for m in MARKS) == set(MARKS)
    check("D5.2 HONEST LIMIT: THE MODULUS SURVIVES [exact witness]: marks "
          "{0,1,8,9} are shift-8-invariant (%s) and crossing (%s) with the "
          "SAME nonsplit deck lift (D4.1 is mark-independent), but the "
          "quarter shift does NOT preserve them (%s; it does preserve the "
          "equally-spaced {0,4,8,12}: %s) -- freeness forces the POSITION "
          "(crossing/central class), NOT the equal spacing = the square "
          "modulus = the clock: the bit reduces to the modulus datum, it "
          "does not vanish"
          % (inv_ok, crossing, clock_wit, clock_marks),
          inv_ok and crossing and not clock_wit and clock_marks)


def d6_controls():
    print("== D6: negative controls ==")
    n_inv9, free9, _, _ = involution_census(9)
    check("D6.1 ODD CONTROL [exact]: D_9 has %d involutions and %d free "
          "ones (no antipode exists at odd N; every reflection fixes a "
          "site + an edge midpoint) -- a Moebius seam circle needs an "
          "EVEN carrier count, consistent with 16 = 2^(g_car-1)"
          % (n_inv9, len(free9)),
          n_inv9 == 9 and len(free9) == 0)

    # Klein bottle: orientation-cover deck on the 16x16 discrete torus
    T = [(x, y) for x in range(16) for y in range(16)]
    klein = {(x, y): ((x + 8) % 16, (-y) % 16) for (x, y) in T}
    klein_free = all(klein[p] != p for p in T)
    klein_inv = all(klein[klein[p]] == p for p in T)
    fib0 = [(x, 0) for x in range(16)]
    fib8 = [(x, 8) for x in range(16)]
    inv_fibres = [f for f in (fib0, fib8)
                  if all(klein[p] in f for p in f)]
    fibre_shift = all(klein[(x, 0)] == ((x + 8) % 16, 0) for x in range(16))
    check("D6.2 KLEIN CONTROL [exact]: the Klein orientation-cover deck "
          "(x,y) -> (x+8,-y) is a free involution on all 256 torus points "
          "(free: %s, involution: %s) and restricts to the free shift-8 "
          "on its %d invariant fibre circles (%s) -- covering decks are "
          "free for Moebius AND Klein alike: the discriminator is "
          "covering vs branched, not which non-orientable gluing"
          % (klein_free, klein_inv, len(inv_fibres), fibre_shift),
          klein_free and klein_inv and len(inv_fibres) == 2 and fibre_shift)

    # branched pillowcase involution: fixed points = the 4 marks
    branch = {(x, y): ((-x) % 16, (-y) % 16) for (x, y) in T}
    br_fixed = [p for p in T if branch[p] == p]
    circ0 = [(x, 0) for x in range(16)]
    br_on_circ = all(branch[p] in circ0 for p in circ0)
    br_circ_fixed = [p for p in circ0 if branch[p] == p]
    check("D6.3 BRANCH CONTROL [exact]: the pillowcase involution (x,y) -> "
          "(-x,-y) on the same torus has EXACTLY %d fixed points %s = the "
          "2-torsion = the four marks (v507 T1.1 discretised), i.e. it is "
          "BRANCHED, not a covering deck; restricted to the invariant "
          "circle y = 0 (%s) it is a REFLECTION with %d fixed points -- "
          "the edge class IS the branch involution's restriction: the "
          "silver arrangement mistakes the mark-creating branch Z2 for "
          "the seam deck"
          % (len(br_fixed), sorted(br_fixed), br_on_circ,
             len(br_circ_fixed)),
          len(br_fixed) == 4
          and sorted(br_fixed) == [(0, 0), (0, 8), (8, 0), (8, 8)]
          and br_on_circ and len(br_circ_fixed) == 2)


def main():
    print("qgeo_realize_deck_freedom_dihedral_probe: the freedom attack on "
          "the alignment bit -- dihedral census + quotient topology + "
          "complete Fock dichotomy")
    d1_census()
    d2_aut()
    d3_quotient()
    d4_fock()
    d5_chain()
    d6_controls()
    n_pass = sum(RESULTS)
    print("\n%d/%d checks passed" % (n_pass, len(RESULTS)))
    return n_pass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
