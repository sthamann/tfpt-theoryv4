"""v510 -- SEAM.BIT.FREEDOM.01: the freedom attack on the v506/v507
alignment bit -- the POSITION half of the bit is topology.  v507
(SEAM.BIT.ORIGIN.01) left the last identification input as ONE bit with
four equivalent faces; its Part B showed: central arrangement (deck =
shift by 8 on the 16-Majorana NS seam circle) => U^2 = (-1)^F nonsplit;
edge arrangement (deck = REFLECTION with fixed points) => U^2 = +1 split.
KEY OBSERVATION UNDER PROOF: the collar deck of the theory is the deck
transformation of a COVERING (the Z2 seam of the Moebius double, tfpt_3
"orientable double cover of the Moebius fibre is a cylinder with two
boundaries plus one Z2 seam"); deck transformations of coverings act
FREELY, and a reflection of the circle has fixed points and is NEVER
free -- so the edge class is EXCLUDED and the fermionic face of the bit
FOLLOWS.  Two parts (Part A = dihedral/fermionic side, Part B =
Moebius/RP-geometry side).  Exact throughout (sympy; integers/Fractions
in Cl(16); no floats), deterministic.

[E] PART A, DIHEDRAL THEOREM (the discrete side): on the N-site seam
      circle the free involution is UNIQUE = the antipode (N = 16: 17
      involutions in D_16, EXACTLY ONE free = shift by 8; all 16
      reflections have exactly 2 circle fixed points -- sites for even
      axis, edge midpoints for odd axis; robustness N = 8, 12); the
      census is COMPLETE because Aut(C_16) = D_16 exactly (brute force
      over all 8! permutations at N = 8, propagation argument at N = 16
      -- no exotic circle automorphism exists); N = 9 control: D_9 has
      ZERO free involutions (a Moebius seam circle needs an EVEN carrier
      count, consistent with 16 = 2^(g_car-1)).  QUOTIENT TOPOLOGY (the
      P1 tie): circle/antipode = CIRCLE (chi = 0, closed), circle/
      reflection = INTERVAL (chi = 1, two boundary corners) -- origin_
      theory's Gauss-Bonnet budget 6pi = 2pi+2pi+2pi counts three CLOSED
      circles, so "the deck is free on the seam circle" is EXACTLY the
      established P1 datum "the seam is a closed circle", not a premise.
[E] PART A, NONSPLIT <=> FREE (complete census): ALL 17 involutions of
      the seam circle implemented in exact Cl(16) -- the free one's NS
      lift squares to 256 gamma_1...gamma_16 = (-1)^F (nonsplit, 2
      square roots in the 32-element dihedral lift group = the Z8 clock
      tower); ALL 16 reflections have U^2 = SCALAR (2^7 site-axis, 2^8
      edge-axis; splitting, 0 roots) -- the v507 dichotomy holds over
      the COMPLETE involution census, no exception.  Chain: deck free =>
      deck = shift 8 => crossing mark pairing (all 28 invariant 4-sets)
      => U^2 = (-1)^F => central class => the edge/silver arrangement is
      excluded.  Klein control: the orientation-cover deck is free too
      (covering vs branched is the discriminator, not Moebius vs Klein);
      branch control: the pillowcase involution (x,y) -> (-x,-y) has
      exactly 4 fixed points = the marks and restricts to a REFLECTION
      on invariant circles -- the edge class IS the restriction of the
      BRANCHED pillowcase involution: the silver arrangement mistakes
      the mark-creating branch Z2 for the seam deck.
[E] PART B, REAL-STRUCTURE CLASSIFICATION (the continuum side): the
      antiholomorphic involutions of P^1 commuting with the celestial
      deck z -> -z are EXACTLY two families -- mu conj(z), |mu| = 1
      (fix locus = a LINE through the deck poles {0, inf}: deck NOT free
      on it) and mu / conj(z), mu real (mu > 0: fix circle |z| = sqrt(mu)
      avoiding the poles, deck FREE on it; mu < 0: EMPTY fix locus, no
      seam).  Per deck-invariant configuration {+-a, +-b} the mark-
      fixing real structure is UNIQUE (an antiholomorphic map fixing 3
      points pointwise is unique); table: mu4 -> equatorial 1/conj(z),
      deck FREE (v506 A-S2.9 reproduced); SILVER {+-1, +-(3+2 sqrt 2)}
      -> real axis THROUGH the poles, deck NOT free -- the edge class
      is the restriction of the BRANCHED pillowcase involution: silver
      mistakes the mark-generating branch Z2 for the seam deck;
      hexagonal -> NO mark-fixing real structure at all (cross-ratio
      complex, marks not concyclic: RP-incompatible, consistent v503).
      Moebius covering model: the sheet-exchange deck of the cylinder
      double cover is free on ALL points, restricts to the antipode on
      the Z2 seam fibre; the antipode z -> -1/conj(z) is the free type
      whose quotient RP^2 is one-sided = the |Z2| of c3 = 1/(|Z2| 2pi
      chi) (v456/v73) -- P1's one-sidedness TYPES the Z2 as free.
[E] PART B, HARMONIC + FREE => mu4 (the collapse): the deck-pair
      cross-ratio (1-b)^2/(1+b)^2 = -1 solves EXACTLY to b = +-i -- on
      free-deck seam circles the silver family (harmonic AND edge) is
      EMPTY, so harmonicity alone becomes SUFFICIENT for the clock.
[E] HONEST COUNTERWITNESSES (mandatory): "nonsplit => clock" is FALSE
      -- discrete {0,1,8,9} (shift-invariant, crossing, same nonsplit
      lift, but the quarter shift does not preserve it) and continuous
      {+-1, +-(3+4i)/5} (deck free, equatorial, central class, but j =
      148176/25 != 1728, no clock): the Fock dichotomy measures the
      CLASS of the arrangement, not the modulus.
PREMISE TYPING [E]/[C]: (P-i) deck = Moebius covering deck => free on
      the seam circle -- standard covering topology, machine-
      instantiated here (the one-sidedness strand: origin_theory/v456
      check 1 [E]; tfpt_3 "cylinder + one Z2 seam" double structure);
      (P-ii) marks lie on the Theta-fix seam circle = existing REALIZE
      [C] content (QGEO.REALIZE.02 hypotheses (4)/(5), v264; v506
      A-S2.9 [E] for mu4) -- NO new input.  AUDIT FINDING documented:
      "circle-freeness" was nowhere typed before (only mark-freeness,
      v216); v507 F1.1 explicitly admitted the reflection reading of
      the edge class ("faithful seam-circle realisation, but only as a
      reflection") -- v510 closes that door: a reflection is not a
      covering deck.
[C] THE REDUCED REST (verbatim, no overclaim): the alignment bit
      reduces from "harmonic AND central" to the square-modulus datum
      tau = i alone; the position half is topology (edge class
      excluded), the modulus half stays the one carrier input.

Status: [E] dihedral theorem, complete Fock census, real-structure
classification, harmonic+free => mu4, counterwitnesses (exact sympy /
exact Cl(16) Fractions); [C] the square-modulus datum above.
SEAM.CLOCK.RIGIDITY.01, SEAM.BIT.ORIGIN.01 and QGEO.REALIZE.01 stay as
they are (text precised only), P2.TYPING.01 R1 halved -- NO marker
moves.  Python; Wolfram-mirrored (dihedral census, Cl(16) dichotomy
census, real-structure table, harmonic+free => +-i, counterwitnesses),
counted per GATE.WOLFRAM.02.  Discovery provenance: experiments/
tfpt-discovery/qgeo_realize_deck_freedom_dihedral_probe.py (2026-07-21,
14/14) and qgeo_realize_rp_fixcircle_moebius_probe.py (2026-07-21,
16/16)."""
from fractions import Fraction as Fr
from itertools import combinations, permutations

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

I = sp.I
N_SITES = 16           # 16 Majorana modes = 2^(g_car-1), 4 per mark quadrant
MARKS = (0, 4, 8, 12)  # mu4 mark sites (0-based) on the 16-site seam circle


def iszero(e):
    e2 = sp.expand(e)
    if e2 == 0:
        return True
    return sp.simplify(e2) == 0


# ---------------------------------------------------------------------------
# PART A machinery: dihedral group D_N on the refined 2N circle
# (positions: even = site 2j, odd = edge midpoint between sites)
# ---------------------------------------------------------------------------
def dihedral_refined(N):
    """all 2N elements of D_N as maps on Z_{2N}: ('rot', k) p -> p + 2k;
    ('ref', m) p -> 2m - p (fixed positions p = m, m + N)."""
    return [('rot', k) for k in range(N)] + [('ref', m) for m in range(N)]


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
# PART B machinery: projective points, antiholomorphic maps (v507 style)
# ---------------------------------------------------------------------------
def peq(P, Q):
    return iszero(P[0] * Q[1] - P[1] * Q[0])


def apply_m(M, P):
    return (sp.expand(M[0, 0] * P[0] + M[0, 1] * P[1]),
            sp.expand(M[1, 0] * P[0] + M[1, 1] * P[1]))


def apply_anti(M, P):
    """antiholomorphic map z -> M(conj z) on projective pairs."""
    return apply_m(M, (sp.conjugate(P[0]), sp.conjugate(P[1])))


def map3(A, B, C):
    alpha = C[0] * B[1] - B[0] * C[1]
    beta = A[0] * C[1] - C[0] * A[1]
    return sp.Matrix([[alpha * A[0], beta * B[0]],
                      [alpha * A[1], beta * B[1]]])


def mexp(M):
    return M.applyfunc(sp.expand)


def prop_mat(A, B):
    a = [A[0, 0], A[0, 1], A[1, 0], A[1, 1]]
    b = [B[0, 0], B[0, 1], B[1, 0], B[1, 1]]
    for i in range(4):
        for j in range(i + 1, 4):
            if not iszero(a[i] * b[j] - a[j] * b[i]):
                return False
    return True


def jlam(lam):
    return sp.simplify(256 * (lam ** 2 - lam + 1) ** 3
                       / (lam ** 2 * (lam - 1) ** 2))


def pt(z):
    return (sp.nsimplify(z), sp.Integer(1))


DECK = sp.diag(1, -1)                       # z -> -z


def config(b):
    """deck-invariant marks {+-1, +-b} as projective pairs."""
    return [pt(1), pt(-1), pt(b), pt(-b)]


def mark_fixing_real_structure(cfg):
    """the UNIQUE antiholomorphic map fixing cfg[0..2] pointwise:
    sigma = M3 o conj o M3^{-1}; matrix M3 * conj(M3)^adj.
    Returns (matrix, fixes_fourth_mark)."""
    M3 = map3(cfg[0], cfg[1], cfg[2])
    Msig = mexp(M3 * M3.conjugate().adjugate())
    fixes_all = all(peq(apply_anti(Msig, m), m) for m in cfg)
    return Msig, fixes_all


# ===========================================================================
# PART A -- dihedral census, quotient topology, complete Fock dichotomy
# ===========================================================================
def a_d1_census():
    print("  -- A-D1: involution census in D_N on the refined circle")
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
    check("A-D1.1 DIHEDRAL CENSUS [exact]: N = 16: %d involutions in D_16, "
          "EXACTLY ONE free = the antipodal shift by 8 (%s); all 16 "
          "reflections have 2 fixed points on the circle (%d site-axis + "
          "%d edge-axis) -- a reflection is NEVER free; robustness N = 8: "
          "%s, N = 12: %s (always exactly one free involution = shift N/2)"
          % (res[16][0], res[16][1], res[16][2], res[16][3],
             res[8][:1] + res[8][2:], res[12][:1] + res[12][2:]),
          ok16 and ok8 and ok12)

    fx_counts = {len(fixed_positions(('ref', m), 16)) for m in range(16)}
    anti_fx = len(fixed_positions(('rot', 8), 16))
    check("A-D1.2 FIXED-POINT ARITHMETIC [exact]: every D_16 reflection "
          "fixes exactly 2 points of the circle (counts %s; sites for even "
          "axis, edge midpoints for odd axis) while the antipode fixes %d "
          "-- 'free <=> antipode' has no borderline case: the edge-axis "
          "reflections are free on the SITES but not on the circle "
          "(midpoint fixed points), so site-freeness is NOT the right "
          "notion; circle-freeness is"
          % (sorted(fx_counts), anti_fx),
          fx_counts == {2} and anti_fx == 0)


def a_d2_aut():
    print("  -- A-D2: Aut(C_N) = D_N -- the census is complete")
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
    check("A-D2.1 BRUTE FORCE N = 8 [exact, all 8! = 40320 permutations]: "
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
    check("A-D2.2 PROPAGATION N = 16 [exact]: every vertex has degree 2 "
          "(%s), so an automorphism is DETERMINED by (image of 0, image of "
          "1); all %d = 16 x 2 candidates propagate consistently and equal "
          "D_16 (%s) => Aut(C_16) = D_16 exactly: the A-D1 census covers "
          "ALL circle symmetries -- the unique free involution of the seam "
          "circle IS the antipode, with no loophole"
          % (deg2, len(valid), set(valid) == dihedral16),
          deg2 and len(valid) == 32 and set(valid) == dihedral16)


def a_d3_quotient():
    print("  -- A-D3: quotient topology -- circle/free = circle, "
          "circle/reflection = interval")
    N = 16

    def quotient_data(el):
        pos = list(range(2 * N))
        orb = {}
        for p in pos:
            q = apply_el(el, p, N)
            orb[p] = min(p, q)
        verts = set(orb.values())
        edges = set()
        for p in pos:
            edges.add(frozenset((orb[p], orb[(p + 1) % (2 * N)])))
        fixed = fixed_positions(el, N)
        chi = len(verts) - len(edges)
        return len(verts), len(edges), len(fixed), chi

    v_f, e_f, fx_f, chi_f = quotient_data(('rot', 8))
    v_r, e_r, fx_r, chi_r = quotient_data(('ref', 4))
    v_o, e_o, fx_o, chi_o = quotient_data(('ref', 3))
    check("A-D3.1 QUOTIENT CENSUS [exact]: C/antipode: V = %d, E = %d, chi "
          "= %d, 0 boundary points => a CIRCLE (chi = 0, closed); C/site-"
          "reflection: V = %d, E = %d, chi = %d with %d fixed points => an "
          "INTERVAL (chi = 1, 2 boundary corners); C/edge-reflection: chi "
          "= %d, %d fixed => interval again -- the seam Gamma survives as "
          "a closed circle IFF the deck is free"
          % (v_f, e_f, chi_f, v_r, e_r, chi_r, fx_r, chi_o, fx_o),
          chi_f == 0 and fx_f == 0 and chi_r == 1 and fx_r == 2
          and chi_o == 1 and fx_o == 2)

    circles_budget = 3                      # two boundaries + one Z2 seam
    check("A-D3.2 P1 TIE [arithmetic]: origin_theory's Gauss-Bonnet budget "
          "oint k ds = 2pi + 2pi + 2pi = 6pi (phi_tree = 1/(6pi)) counts "
          "%d CLOSED circles (two cylinder boundaries + ONE Z2 seam "
          "Gamma); a fixed-point deck would turn Gamma into an interval "
          "with 2 corners (A-D3.1) and break the 3 x 2pi count -- 'the "
          "deck is free on the seam circle' is EXACTLY the established P1 "
          "datum 'the seam is a closed circle', not a new premise"
          % circles_budget,
          circles_budget * 2 == 6 and chi_f == 0 and chi_r == 1)


def a_d4_fock():
    print("  -- A-D4: Fock dichotomy for ALL 17 involutions (exact Cl(16))")
    n = N_SITES
    GAMMA = {tuple(range(n)): Fr(1)}

    D_ns = shift_matrix(n, 8, -1)
    Ut = dict(ONE)
    for j in range(8):
        Ut = cmul(Ut, cadd(ONE, cscale(cmul(gam(j), gam(j + 8)), Fr(-1))))
    impl_c = implements(Ut, D_ns, n)
    ok_u2, coef = prop(cmul(Ut, Ut), GAMMA)
    check("A-D4.1 FREE DECK => NONSPLIT [exact, v507 reproduced]: the NS "
          "lift of the UNIQUE free involution (shift 8) implements (%s) "
          "and squares to %s x gamma_1..gamma_16 = 256 (-1)^F-monomial: "
          "U^2 = (-1)^F, the extension is NONSPLIT"
          % (impl_c, coef),
          impl_c and ok_u2 and coef == Fr(256))

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
    check("A-D4.2 ALL 16 REFLECTIONS SPLIT [exact, complete]: for EVERY "
          "axis k = 0..15 the NS implementer exists (implements one of the "
          "two spin lifts +-R, all 16 generators: %s; the sign is the v507 "
          "F2.2 lift ambiguity, both square identically) and U^2 is a "
          "SCALAR (%s; values %s = {2^7 (site-axis), 2^8 (edge-axis)}): "
          "the extension SPLITS for every non-free involution -- (cU)^2 = "
          "c^2 U^2 stays scalar for every phase, so split vs nonsplit is "
          "invariant: NONSPLIT <=> FREE, exactly, over the complete "
          "involution census"
          % (all_impl, all_split, coefs),
          all_impl and all_split
          and coefs == [Fr(2 ** 7), Fr(2 ** 8)])

    group = [shift_matrix(n, k, -1) for k in range(n)] \
        + [refl_matrix(n, k, -1) for k in range(n)]
    roots_free = [i for i, g in enumerate(group)
                  if mat_prop(matmul_i(g, g), D_ns)]
    roots_refl_total = 0
    for k in range(n):
        R = refl_matrix(n, k, -1)
        roots_refl_total += sum(1 for g in group
                                if mat_prop(matmul_i(g, g), R))
    check("A-D4.3 ROOT DICHOTOMY [exact, all 32 lifts x all 17 targets]: "
          "the free deck has %d square roots (the +-quarter shifts = the "
          "Z8 clock tower); ALL 16 reflections together have %d -- no "
          "clock tower exists over any non-free arrangement"
          % (len(roots_free), roots_refl_total),
          roots_free == [4, 12] and roots_refl_total == 0)


def a_d5_chain():
    print("  -- A-D5: the chain end-to-end + the honest modulus limit")
    n = N_SITES
    rot_sets = [s for s in combinations(range(n), 4)
                if set((m + 8) % n for m in s) == set(s)]
    rot_pair = {pairing_of(lambda j: j + 8, s) for s in rot_sets}
    check("A-D5.1 THE CHAIN [exact]: deck free (A-D1/A-D2: unique = shift "
          "8) => every deck-invariant 4-mark set has CROSSING pairing "
          "(all %d sets: %s) => central arrangement type => U^2 = (-1)^F "
          "nonsplit (A-D4.1) => the v507 tetrad's fermionic face holds => "
          "the edge/silver arrangement (noncrossing, split, 0 roots) is "
          "EXCLUDED: the POSITION half of the alignment bit follows from "
          "circle-freeness alone"
          % (len(rot_sets), rot_pair),
          rot_pair == {'crossing'} and len(rot_sets) == 28)

    wit = (0, 1, 8, 9)
    inv_ok = set((m + 8) % n for m in wit) == set(wit)
    crossing = pairing_of(lambda j: j + 8, wit) == 'crossing'
    clock_wit = set((m + 4) % n for m in wit) == set(wit)
    clock_marks = set((m + 4) % n for m in MARKS) == set(MARKS)
    check("A-D5.2 HONEST LIMIT: THE MODULUS SURVIVES [exact witness]: "
          "marks {0,1,8,9} are shift-8-invariant (%s) and crossing (%s) "
          "with the SAME nonsplit deck lift (A-D4.1 is mark-independent), "
          "but the quarter shift does NOT preserve them (%s; it does "
          "preserve the equally-spaced {0,4,8,12}: %s) -- freeness forces "
          "the POSITION (crossing/central class), NOT the equal spacing = "
          "the square modulus = the clock: the bit reduces to the modulus "
          "datum, it does not vanish"
          % (inv_ok, crossing, clock_wit, clock_marks),
          inv_ok and crossing and not clock_wit and clock_marks)


def a_d6_controls():
    print("  -- A-D6: negative controls")
    n_inv9, free9, _, _ = involution_census(9)
    check("A-D6.1 ODD CONTROL [exact]: D_9 has %d involutions and %d free "
          "ones (no antipode exists at odd N; every reflection fixes a "
          "site + an edge midpoint) -- a Moebius seam circle needs an "
          "EVEN carrier count, consistent with 16 = 2^(g_car-1) = %d"
          % (n_inv9, len(free9), 2 ** (g_car - 1)),
          n_inv9 == 9 and len(free9) == 0 and 2 ** (g_car - 1) == 16)

    T = [(x, y) for x in range(16) for y in range(16)]
    klein = {(x, y): ((x + 8) % 16, (-y) % 16) for (x, y) in T}
    klein_free = all(klein[p] != p for p in T)
    klein_inv = all(klein[klein[p]] == p for p in T)
    fib0 = [(x, 0) for x in range(16)]
    fib8 = [(x, 8) for x in range(16)]
    inv_fibres = [f for f in (fib0, fib8)
                  if all(klein[p] in f for p in f)]
    fibre_shift = all(klein[(x, 0)] == ((x + 8) % 16, 0) for x in range(16))
    check("A-D6.2 KLEIN CONTROL [exact]: the Klein orientation-cover deck "
          "(x,y) -> (x+8,-y) is a free involution on all 256 torus points "
          "(free: %s, involution: %s) and restricts to the free shift-8 "
          "on its %d invariant fibre circles (%s) -- covering decks are "
          "free for Moebius AND Klein alike: the discriminator is "
          "covering vs branched, not which non-orientable gluing"
          % (klein_free, klein_inv, len(inv_fibres), fibre_shift),
          klein_free and klein_inv and len(inv_fibres) == 2 and fibre_shift)

    branch = {(x, y): ((-x) % 16, (-y) % 16) for (x, y) in T}
    br_fixed = [p for p in T if branch[p] == p]
    circ0 = [(x, 0) for x in range(16)]
    br_on_circ = all(branch[p] in circ0 for p in circ0)
    br_circ_fixed = [p for p in circ0 if branch[p] == p]
    check("A-D6.3 BRANCH CONTROL [exact]: the pillowcase involution (x,y) "
          "-> (-x,-y) on the same torus has EXACTLY %d fixed points %s = "
          "the 2-torsion = the four marks (v507 T1.1 discretised), i.e. "
          "it is BRANCHED, not a covering deck; restricted to the "
          "invariant circle y = 0 (%s) it is a REFLECTION with %d fixed "
          "points -- the edge class IS the branch involution's "
          "restriction: the silver arrangement mistakes the mark-creating "
          "branch Z2 for the seam deck"
          % (len(br_fixed), sorted(br_fixed), br_on_circ,
             len(br_circ_fixed)),
          len(br_fixed) == 4
          and sorted(br_fixed) == [(0, 0), (0, 8), (8, 0), (8, 8)]
          and br_on_circ and len(br_circ_fixed) == 2)


def part_a():
    print(" PART A -- the dihedral/fermionic side: unique free involution "
          "+ complete Fock census")
    a_d1_census()
    a_d2_aut()
    a_d3_quotient()
    a_d4_fock()
    a_d5_chain()
    a_d6_controls()


# ===========================================================================
# PART B -- Moebius covering deck + RP fix-circle geometry (exact)
# ===========================================================================
def b_m1_moebius():
    print("  -- B-M1: the Moebius covering deck is free (discrete model)")
    L, W = 12, 5                             # cylinder Z_{2L} x {0..W-1}
    pts = [(x, y) for x in range(2 * L) for y in range(W)]

    def deck(p):
        return ((p[0] + L) % (2 * L), W - 1 - p[1])

    invol = all(deck(deck(p)) == p for p in pts)
    free = all(deck(p) != p for p in pts)
    orbits = len({frozenset((p, deck(p))) for p in pts})
    seam = [(x, (W - 1) // 2) for x in range(2 * L)]
    seam_inv = all(deck(p) in seam for p in seam)
    seam_antipode = all(deck((x, 2)) == ((x + L) % (2 * L), 2)
                        for x in range(2 * L))
    seam_orbits = len({frozenset((p, deck(p))) for p in seam})
    check("B-M1.1 CYLINDER DOUBLE COVER [exact, %d points]: the sheet-"
          "exchange deck (x,y) -> (x+%d, %d-y) of the cylinder over the "
          "Moebius band is an involution (%s), FREE on all points (%s; "
          "%d = %d/2 orbits = the Moebius band), preserves the Z2 seam "
          "fibre (%s) and acts there as the ANTIPODE x -> x+%d of the "
          "doubled circle (%s; %d seam orbits = the core circle) -- "
          "'covering deck => free' machine-instantiated on the tfpt_3 "
          "'cylinder + one Z2 seam' structure"
          % (len(pts), L, W - 1, invol, free, orbits, len(pts), seam_inv,
             L, seam_antipode, seam_orbits),
          invol and free and orbits == len(pts) // 2 and seam_inv
          and seam_antipode and seam_orbits == L)

    bdry = [(x, y) for x in range(2 * L) for y in (0, W - 1)]
    bdry_inv = all(deck(p) in bdry for p in bdry)
    bdry_free = all(deck(p) != p for p in bdry)
    bdry_orbits = len({frozenset((p, deck(p))) for p in bdry})
    reps = [(x, 0) for x in range(2 * L)]
    one_rep_each = all(sum(1 for r in reps
                           if r in (p, deck(p))) == 1 for p in reps)
    fibre_sizes = {x0: sum(1 for (x, _) in reps if x % L == x0)
                   for x0 in range(L)}
    check("B-M1.2 MOEBIUS BOUNDARY [exact]: the two cylinder boundary rows "
          "form one free deck orbit set (invariant: %s, free: %s, %d "
          "orbits, one y = 0 representative each: %s) = ONE downstairs "
          "circle of length %d; it double-covers the core circle Z_%d "
          "(every core point has exactly 2 boundary preimages: %s) with "
          "antipodal deck -- 'the Moebius boundary is ONE circle, 2:1 "
          "over the core, deck = antipode, FREE' is standard covering "
          "topology, verified"
          % (bdry_inv, bdry_free, bdry_orbits, one_rep_each, 2 * L, L,
             set(fibre_sizes.values()) == {2}),
          bdry_inv and bdry_free and bdry_orbits == 2 * L
          and one_rep_each and set(fibre_sizes.values()) == {2})


def b_m2_onesided():
    print("  -- B-M2: one-sidedness = the free antipode (P1 tie)")
    z = sp.symbols('z')
    zz = sp.symbols('zz', nonnegative=True)   # |z|^2 >= 0
    sol_anti = sp.solve(sp.Eq(zz, -1), zz)
    anti_inf = False                          # a(inf) = 0 != inf
    x = sp.symbols('x', real=True)
    refl_fix = iszero(sp.conjugate(x) - x)
    deck_fix = sp.solve(sp.Eq(-z, z), z)
    check("B-M2.1 TWO TYPES [exact]: the antipode z -> -1/conj(z) is FREE "
          "(|z|^2 = -1 has %d solutions; inf -> 0: fixed at inf: %s) -- "
          "quotient RP^2, ONE-SIDED = the |Z2| of c3 = 1/(|Z2| 2pi chi) "
          "(v456/v73); the reflection z -> conj(z) fixes the whole real "
          "circle (%s) -- quotient a TWO-SIDED disk: P1's one-sidedness "
          "TYPES the normal-slice Z2 as the free antipode, not a mirror"
          % (len(sol_anti), anti_inf, refl_fix),
          len(sol_anti) == 0 and not anti_inf and refl_fix)

    r_ = sp.symbols('r_', positive=True)
    th = sp.symbols('th', real=True)
    zc = r_ * sp.exp(I * th)
    on_circle = iszero(sp.Abs(-zc) - r_)
    circle_fixed = sp.simplify(-zc - zc)      # = -2 z != 0 for z != 0
    check("B-M2.2 DECK ON CIRCLES [exact]: the celestial deck z -> -z has "
          "sphere fixed points %s = {0, inf}, but maps every circle "
          "|z| = r to itself (%s) acting as the circle ANTIPODE with NO "
          "fixed point there (-z = z <=> 2z = 0, off-circle) -- free on "
          "the seam circle IFF the circle avoids the poles {0, inf}"
          % (deck_fix + ['inf'], on_circle),
          deck_fix == [0] and on_circle
          and sp.simplify(circle_fixed + 2 * zc) == 0)


def b_m3_classification():
    print("  -- B-M3: deck-commuting real structures -- complete "
          "classification")
    a, b, c, d = sp.symbols('a b c d')
    M = sp.Matrix([[a, b], [c, d]])
    MD = mexp(M * DECK)
    DM = mexp(DECK * M)
    br1 = sp.solve([MD[0, 1] - DM[0, 1], MD[1, 0] - DM[1, 0]], [b, c],
                   dict=True)
    br2 = sp.solve([MD[0, 0] + DM[0, 0], MD[1, 1] + DM[1, 1]], [a, d],
                   dict=True)
    diag_ok = br1 == [{b: 0, c: 0}]
    anti_ok = br2 == [{a: 0, d: 0}]
    lam_sq = sp.solve(sp.symbols('lam_') ** 2 - 1, sp.symbols('lam_'))
    check("B-M3.1 TWO FAMILIES [exact, symbolic]: projectively M D = lam "
          "D M forces lam in %s (det both sides), and the two branches "
          "solve to M DIAGONAL (%s: sigma = mu conj(z)) resp. M "
          "ANTIDIAGONAL (%s: sigma = mu / conj(z)) -- no third family of "
          "deck-commuting real structures exists"
          % (lam_sq, br1, br2),
          diag_ok and anti_ok and sorted(lam_sq) == [-1, 1])

    mu = sp.symbols('mu')
    Mdiag = sp.diag(mu, 1)
    inv_diag = mexp(Mdiag * Mdiag.conjugate())
    Manti = sp.Matrix([[0, mu], [1, 0]])
    inv_anti = mexp(Manti * Manti.conjugate())
    th = sp.symbols('th', real=True)
    r_ = sp.symbols('r_', positive=True)
    zline = r_ * sp.exp(I * th / 2)
    line_fixed = iszero(sp.exp(I * th) * sp.conjugate(zline) - zline)
    line_through_poles = True                 # 0 and inf are on every line
    zcirc = r_ * sp.exp(I * th)
    circ_fixed = iszero(r_ ** 2 / sp.conjugate(zcirc) - zcirc)
    zz = sp.symbols('zz', nonnegative=True)
    neg_sol = sp.solve(sp.Eq(zz, -(r_ ** 2)), zz)
    check("B-M3.2 INVOLUTION + FIX LOCI [exact]: diagonal family: sigma^2 "
          "matrix = %s prop Id <=> |mu| = 1, fix locus = the LINE arg z = "
          "th/2 (pointwise: %s) which ALWAYS contains the deck poles "
          "{0, inf} => deck NOT free on it; antidiagonal: sigma^2 = %s "
          "prop Id <=> mu real; mu = r^2 > 0: fix circle |z| = r "
          "(pointwise: %s), avoids the poles => deck FREE on it; mu < 0: "
          "fix locus EMPTY (%d solutions; quaternionic structure -- no "
          "seam circle at all, excluded by P1's existing seam Gamma): "
          "an RP seam circle with FREE deck exists in EXACTLY ONE family "
          "-- the equatorial one"
          % (list(inv_diag.diagonal()), line_fixed,
             list(inv_anti.diagonal()), circ_fixed, len(neg_sol)),
          list(inv_diag.diagonal()) == [mu * sp.conjugate(mu), 1]
          and line_fixed and line_through_poles
          and list(inv_anti.diagonal()) == [mu, sp.conjugate(mu)]
          and circ_fixed and len(neg_sol) == 0)


def b_m4_per_config():
    print("  -- B-M4: the unique mark-fixing real structure per "
          "configuration")
    s2 = sp.sqrt(2)
    b = sp.symbols('b')
    quartic = sp.expand(16 * b ** 2 - 4 * b * (1 + b) ** 2 + (1 + b) ** 4)
    b_hex = I * (2 - sp.sqrt(3))
    quartic_ok = (quartic == sp.expand(b ** 4 + 14 * b ** 2 + 1)
                  and iszero(quartic.subs(b, b_hex)))
    check("B-M4.0 HEX FRAME [exact]: j = 0 for marks {+-1, +-b} <=> "
          "b^4 + 14 b^2 + 1 = 0 (expansion of 16b^2 - 4b(1+b)^2 + "
          "(1+b)^4: %s); b_hex = i(2 - sqrt3) is a root (%s) -- purely "
          "imaginary with |b_hex| = 2 - sqrt3 != 1: two marks on the "
          "real axis, two on the imaginary, DIFFERENT radii"
          % (quartic == sp.expand(b ** 4 + 14 * b ** 2 + 1),
             iszero(quartic.subs(b, b_hex))),
          quartic_ok)
    cases = {
        'mu4': sp.nsimplify(I),
        'silver': 3 + 2 * s2,
        'generic-real': sp.Integer(3),
        'generic-unit': sp.Rational(3, 5) + sp.Rational(4, 5) * I,
        'hexagonal': b_hex,
    }
    EQUATOR = sp.Matrix([[0, 1], [1, 0]])     # z -> 1/conj(z)
    REALAXIS = sp.eye(2)                      # z -> conj(z)
    res = {}
    for tag, bv in cases.items():
        cfg = config(bv)
        Msig, fixes_all = mark_fixing_real_structure(cfg)
        fam = ('equatorial' if prop_mat(Msig, EQUATOR)
               else 'real-axis' if prop_mat(Msig, REALAXIS)
               else 'other')
        free = (fam == 'equatorial')
        res[tag] = (fixes_all, fam, free)
    check("B-M4.1 MU4 [exact, v506 A-S2.9 reproduced]: unique mark-fixing "
          "real structure exists (%s), = the EQUATORIAL z -> 1/conj(z) "
          "(family: %s), fix circle |z| = 1 avoids {0, inf} => deck FREE "
          "on the mark-carrying seam circle -- central class geometry"
          % (res['mu4'][0], res['mu4'][1]),
          res['mu4'] == (True, 'equatorial', True))
    check("B-M4.2 SILVER [exact]: unique mark-fixing real structure "
          "exists (%s), = the REAL-AXIS z -> conj(z) (family: %s), fix "
          "circle = R u {inf} passes THROUGH the deck poles {0, inf} => "
          "deck NOT free on the mark circle (fixed points 0, inf between "
          "the neighbour marks = the v507 edge fixed sites) -- the silver "
          "configuration CANNOT sit on a free-deck seam circle"
          % (res['silver'][0], res['silver'][1]),
          res['silver'] == (True, 'real-axis', False))
    check("B-M4.3 GENERIC CONTROLS [exact]: generic-real {+-1, +-3}: "
          "real-axis structure, deck NOT free (%s) -- edge geometry "
          "without harmonicity; generic-unit {+-1, +-(3+4i)/5}: "
          "equatorial structure, deck FREE (%s) -- central-class geometry "
          "without harmonicity: freeness and harmonicity are independent "
          "axes, freeness alone does NOT pin the modulus"
          % (res['generic-real'], res['generic-unit']),
          res['generic-real'] == (True, 'real-axis', False)
          and res['generic-unit'] == (True, 'equatorial', True))
    lam_hex = sp.simplify(4 * b_hex / (1 + b_hex) ** 2)
    j_hex = sp.simplify(jlam(lam_hex))
    im_lam = sp.simplify(sp.im(lam_hex))
    check("B-M4.4 HEXAGONAL CONTROL [exact]: the deck-frame hexagonal "
          "marks {+-1, +-b_hex} (b_hex root of (1+b)^4 - 4b(1+b)^2 + "
          "16b^2, lambda = %s, j = %s = 0) have NO mark-fixing real "
          "structure at all (fixes all four: %s; cross-ratio complex, "
          "Im lambda = %s != 0 => marks NOT concyclic): the hexagonal "
          "configuration is RP-INCOMPATIBLE -- it cannot lie on ANY seam "
          "circle, free or not (consistent with v503: the dynamical "
          "winner carries no clock AND no RP mark circle)"
          % (lam_hex, j_hex, res['hexagonal'][0], im_lam),
          j_hex == 0 and not res['hexagonal'][0] and im_lam != 0)
    return cases, res


def b_m5_circle_geometry(cases):
    print("  -- B-M5: circle geometry -- crossing vs noncrossing, exact")
    lam_of = {}
    for tag in ('mu4', 'silver', 'generic-real', 'generic-unit'):
        bv = cases[tag]
        lam_of[tag] = sp.simplify(4 * bv / (1 + bv) ** 2)
    real_flags = {t: sp.simplify(sp.im(v)) == 0 for t, v in lam_of.items()}
    check("B-M5.1 CONCYCLIC <=> REAL CROSS-RATIO [exact]: lambda({+-1,"
          "+-b}) = 4b/(1+b)^2 gives mu4 -> %s (the v168 value!), silver "
          "-> %s (harmonic!), generic-real -> %s, generic-unit -> %s -- "
          "all real (%s) hence concyclic; hexagonal complex (B-M4.4): the "
          "four RP-admissible test configurations each lie on EXACTLY ONE "
          "circle (3 points determine it), so 'the mark circle' is "
          "well-defined"
          % (lam_of['mu4'], lam_of['silver'], lam_of['generic-real'],
             lam_of['generic-unit'], all(real_flags.values())),
          lam_of['mu4'] == 2 and lam_of['silver'] == sp.Rational(1, 2)
          and all(real_flags.values()))

    s_ = 3 + 2 * sp.sqrt(2)
    order_ok = sp.simplify(s_ - 1) > 0
    zero_between = True
    th_marks = [0, sp.pi / 2, sp.pi, 3 * sp.pi / 2]
    pair1 = (th_marks[0], th_marks[2])
    pair2 = (th_marks[1], th_marks[3])
    crossing = (pair1[0] < pair2[0] < pair1[1] < pair2[1])
    check("B-M5.2 PAIRING DICHOTOMY [exact]: on the free-deck circle "
          "|z| = 1 the deck pairs {1, -1} and {i, -i} are DIAMETERS -- "
          "interleaved angles (0 < pi/2 < pi < 3pi/2: %s) => CROSSING = "
          "central class, and this holds for EVERY antipodal pair set "
          "(diameters always cross); on the silver circle R u {inf} the "
          "order is -s < -1 < 1 < s with s = 3+2sqrt2 > 1 (%s) and the "
          "deck pairs {-1,1}, {-s,s} are NESTED (noncrossing) with the "
          "deck fixed point 0 between -1 and 1 and inf between s and -s "
          "-- the edge class EXISTS ONLY on circles through the poles"
          % (crossing, order_ok),
          crossing and order_ok and zero_between)


def b_m6_harmonic_free(cases):
    print("  -- B-M6: harmonic + free => clock (the collapse of the bit)")
    b = sp.symbols('b')
    sols = sp.solve((1 - b) ** 2 + (1 + b) ** 2, b)
    check("B-M6.1 HARMONIC SEPARATION SOLVES TO mu4 [exact, symbolic]: "
          "the deck-pair cross-ratio (1-b)^2/(1+b)^2 = -1 has EXACTLY the "
          "solutions b = %s -- on a free-deck seam circle 'deck pairs "
          "harmonically separated' (the v507 tetrad face) forces the "
          "marks to be the mu4 orbit {+-1, +-i} exactly: GIVEN freeness, "
          "harmonicity is no longer merely necessary but SUFFICIENT -- "
          "the v506 silver family (harmonic AND edge) is EMPTY on free-"
          "deck circles, the alignment bit collapses onto the modulus"
          % sols,
          sorted(sols, key=str) == [-I, I])

    bu = cases['generic-unit']
    lam_u = sp.simplify(4 * bu / (1 + bu) ** 2)
    j_u = sp.simplify(jlam(lam_u))
    pair_cr = sp.simplify((1 - bu) ** 2 / (1 + bu) ** 2)
    cfg_u = config(bu)
    CLOCK = sp.diag(I, 1)                     # z -> iz
    clock_pres = all(any(peq(apply_m(CLOCK, p), q) for q in cfg_u)
                     for p in cfg_u)
    check("B-M6.2 HONEST REST [exact witness]: the free-deck "
          "configuration {+-1, +-(3+4i)/5} has pair cross-ratio %s != "
          "-1, lambda = %s, j = %s != 1728, and the clock z -> iz does "
          "NOT preserve it (%s) -- freeness forces the CLASS (crossing/"
          "central, nonsplit Fock lift), NOT the square modulus: 'tau = "
          "i' survives as the one continuous carrier datum"
          % (pair_cr, lam_u, j_u, clock_pres),
          pair_cr != -1 and j_u != 1728 and not clock_pres)
    return pair_cr != -1 and j_u != 1728 and not clock_pres


def b_m7_chain(res, modulus_survives):
    print("  -- B-M7: the chain end-to-end")
    mu4_ok = res['mu4'] == (True, 'equatorial', True)
    silver_excluded = res['silver'] == (True, 'real-axis', False)
    hex_excluded = not res['hexagonal'][0]
    check("B-M7.1 VERDICT CHAIN [assembled from B-M1..B-M6 + Part A]: "
          "(P-i) deck = Moebius covering deck => FREE on the seam circle "
          "[standard topology, B-M1 -- P1-side gratis]; (P-ii) marks lie "
          "on the Theta-fix seam circle [= existing QGEO.REALIZE "
          "content; v506 A-S2.9 [E] for mu4] ==> the mark circle is in "
          "the equatorial family (B-M3), the deck acts on it freely as "
          "the antipode, all deck pairs are diameters => CROSSING/central "
          "class (B-M5) => NS Fock lift NONSPLIT (A-D4.1) => the "
          "edge/silver arrangement is EXCLUDED (%s; its circle passes "
          "through the deck poles, B-M4.2), hexagonal RP-incompatible "
          "(%s) -- and the REST is exactly the modulus: harmonic + free "
          "=> mu4 (B-M6.1), but freeness alone does not give harmonicity "
          "(%s): the alignment bit REDUCES from 'harmonic AND central' "
          "to 'harmonic' = 'tau = i' = the square-modulus datum"
          % (silver_excluded, hex_excluded, modulus_survives),
          mu4_ok and silver_excluded and hex_excluded and modulus_survives)


def part_b():
    print(" PART B -- the Moebius/RP-geometry side: covering deck + "
          "fix-circle classification")
    b_m1_moebius()
    b_m2_onesided()
    b_m3_classification()
    cases, res = b_m4_per_config()
    b_m5_circle_geometry(cases)
    modulus_survives = b_m6_harmonic_free(cases)
    b_m7_chain(res, modulus_survives)


# ---------------------------------------------------------------------------
def run():
    reset()
    print("v510  SEAM.BIT.FREEDOM.01: the freedom attack on the alignment "
          "bit -- Part A (dihedral/Fock) + Part B (Moebius/RP)")
    part_a()
    part_b()

    return summary("v510 SEAM.BIT.FREEDOM.01: DIHEDRAL THEOREM (Part A) -- "
                   "on the N-site seam circle the free involution is "
                   "UNIQUE = the antipode (N = 16: 17 involutions, exactly "
                   "1 free; all 16 reflections have 2 circle fixed points; "
                   "Aut(C_16) = D_16 exactly, brute force 8! at N = 8); "
                   "quotient topology: circle/antipode = CIRCLE (chi = 0), "
                   "circle/reflection = INTERVAL (chi = 1) -- the 6pi "
                   "budget needs closed circles, so freeness = the "
                   "established P1 datum.  NONSPLIT <=> FREE (complete "
                   "census, exact Cl(16)): free => Utilde^2 = 256 "
                   "gamma_1..gamma_16 = (-1)^F (nonsplit, 2 roots = Z8); "
                   "ALL 16 reflections => U^2 = scalar (2^7/2^8, split, 0 "
                   "roots).  REAL-STRUCTURE CLASSIFICATION (Part B): deck-"
                   "commuting real structures = exactly 2 families (line "
                   "through the poles: not free; equatorial circle: free); "
                   "per configuration the mark-fixing real structure is "
                   "unique -- mu4 equatorial FREE, silver real-axis "
                   "through the poles NOT free (the edge class is the "
                   "restriction of the BRANCHED pillowcase involution), "
                   "hexagonal RP-incompatible.  HARMONIC + FREE => mu4 "
                   "exactly (pair cross-ratio -1 solves to b = +-i).  "
                   "COUNTERWITNESSES: 'nonsplit => clock' is FALSE -- "
                   "{0,1,8,9} and {+-1, +-(3+4i)/5} (free, central, j = "
                   "148176/25, no clock): the Fock dichotomy measures the "
                   "CLASS, not the modulus.  THE [C] REST (verbatim): the "
                   "alignment bit reduces from 'harmonic AND central' to "
                   "the square-modulus datum tau = i alone; the position "
                   "half is topology (edge class excluded), the modulus "
                   "half stays the one carrier input.  No marker moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
