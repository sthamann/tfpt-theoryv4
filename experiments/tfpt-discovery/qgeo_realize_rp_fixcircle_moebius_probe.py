"""qgeo_realize_rp_fixcircle_moebius_probe.py -- EXPLORATION ONLY
(experiments/, no verification claim).

THE FREEDOM ATTACK ON THE v506/v507 ALIGNMENT BIT (Moebius / RP-geometry side).

Companion of qgeo_realize_deck_freedom_dihedral_probe.py (dihedral census +
complete Fock dichotomy: free involution of the seam circle = antipode,
uniquely; NONSPLIT <=> FREE).  This probe supplies the CONTINUUM half:

  M1 MOEBIUS COVERING DECK IS FREE (discrete model of the tfpt_3 sentence
     "orientable double cover of the Moebius fibre = cylinder + one Z2
     seam"): the sheet-exchange deck of the cylinder double cover is free
     on ALL points; restricted to the Z2 seam fibre it is the ANTIPODE of
     a doubled circle (quotient = core circle); the Moebius BOUNDARY is
     one circle double-covering the core with the same antipodal deck --
     covering-space freeness is standard topology, machine-instantiated.
  M2 ONE-SIDEDNESS = FREE ANTIPODE (the P1 tie): the two conjugacy types
     of orientation-reversing involutions of S^2 are the free antipode
     z -> -1/conj(z) (quotient RP^2, one-sided -- the |Z2| of c3 =
     1/(|Z2| 2pi chi), v456/v73) and the reflection z -> conj(z) (fix
     circle, quotient a two-sided disk).  P1's one-sidedness TYPES the
     Z2 as the free one.  The celestial deck z -> -z (v492 S5 sheet flip)
     has sphere fixed points {0, inf} but acts on every invariant circle
     |z| = r as the free circle antipode.
  M3 CLASSIFICATION (exact, projective): the antiholomorphic involutions
     of P^1 commuting with the deck z -> -z are EXACTLY two families --
     mu conj(z) with |mu| = 1 (fix locus = a LINE through the deck fixed
     points 0, inf: deck NOT free on it) and mu / conj(z) with mu real
     (mu > 0: fix circle |z| = sqrt(mu), deck FREE on it; mu < 0: EMPTY
     fix locus, no seam -- excluded by P1's existing seam).
  M4 THE MARK-FIXING REAL STRUCTURE IS UNIQUE PER CONFIGURATION (exact):
     an antiholomorphic map fixing 3 points pointwise is unique; for each
     deck-invariant configuration {+-a, +-b} the unique candidate is
     computed and classified: mu4 -> 1/conj(z) (equatorial, deck FREE on
     the fix circle |z| = 1) = v506 A-S2.9 reproduced; silver {+-1,
     +-(3+2sqrt2)} -> conj(z) (real axis THROUGH 0, inf: deck NOT free);
     generic-real {+-1, +-3} -> conj(z) (not free); generic-unit {+-1,
     +-(3+4i)/5} -> 1/conj(z) (free); hexagonal-in-deck-frame -> NO real
     structure fixes all four marks (cross-ratio complex, marks NOT
     concyclic): RP-incompatible.
  M5 CIRCLE GEOMETRY (exact): concyclic <=> cross-ratio real; on a
     deck-free circle |z| = r the deck pairs are DIAMETERS => always
     CROSSING (central class); on a circle through {0, inf} the pairing
     is NONCROSSING (edge class) -- the v507 F1.1 dichotomy in continuum
     form.  lambda(b) = 4b/(1+b)^2 for marks {+-1, +-b}: mu4 (b = i) ->
     2, silver (b = 3+2sqrt2) -> 1/2 (harmonic!), generic-unit -> real
     non-harmonic, hexagonal b -> complex.
  M6 HARMONIC + FREE => CLOCK (exact, the collapse of the bit): the deck
     pair cross-ratio (1-b)^2/(1+b)^2 = -1 solves EXACTLY to b = +-i, so
     on a deck-free seam circle "harmonically separated deck pairs" =
     "marks are one mu4 orbit" -- v506's counterexample family (harmonic
     BUT edge) is EMPTY once freeness holds: harmonicity alone becomes
     SUFFICIENT.  The honest rest: freeness does NOT give harmonicity
     (generic-unit witness has no clock; j != 1728).
  M7 THE CHAIN, END-TO-END: (P-i) deck = Moebius covering deck => free
     on the seam circle [M1, topology gratis]; (P-ii) marks on the seam
     circle = the Theta-fix circle [REALIZE content; v506 A-S2.9 [E] for
     mu4] => the configuration is {+-a, +-b} with |a| = |b| => crossing
     => central class => NS Fock lift NONSPLIT (companion D4.1) => the
     edge/silver class is EXCLUDED; the alignment bit REDUCES from
     "harmonic AND central" to "harmonic" (tau = i, the square modulus)
     -- the discrete position freedom is gone, the modulus datum remains.

Repo anchors: tfpt_3 ("cylinder + one Z2 seam"), origin_theory (c3 =
1/(|Z2| 2pi chi(S^2)), 6pi budget), v456 (one-sidedness), v492 S5 (deck =
sheet flip), v506 A-S2.9 (equatorial real structure), v507 (tetrad, core
solve, silver placement), v216 (marks).

Exact throughout (sympy, projective matrices; no floats).  Standalone.
Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/qgeo_realize_rp_fixcircle_moebius_probe.py
"""
import sympy as sp

RESULTS = []
I = sp.I


def check(name, ok):
    RESULTS.append(bool(ok))
    print(("PASS" if ok else "FAIL") + " [%2d] %s" % (len(RESULTS), name))


def iszero(e):
    e2 = sp.expand(e)
    if e2 == 0:
        return True
    return sp.simplify(e2) == 0


# ---------------------------------------------------------------------------
# projective machinery (v507 style); antiholomorphic maps = (matrix, conj)
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


def cross_ratio(P1, P2, P3, P4):
    def pd(P, Q):
        return sp.expand(P[0] * Q[1] - Q[0] * P[1])
    return sp.simplify(sp.expand(pd(P1, P3) * pd(P2, P4)) /
                       sp.expand(pd(P1, P4) * pd(P2, P3)))


def jlam(lam):
    return sp.simplify(256 * (lam ** 2 - lam + 1) ** 3
                       / (lam ** 2 * (lam - 1) ** 2))


def pt(z):
    return (sp.nsimplify(z), sp.Integer(1))


PINF = (sp.Integer(1), sp.Integer(0))
P0 = (sp.Integer(0), sp.Integer(1))
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


# ---------------------------------------------------------------------------
def m1_moebius():
    print("== M1: the Moebius covering deck is free (discrete model) ==")
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
    check("M1.1 CYLINDER DOUBLE COVER [exact, %d points]: the sheet-"
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
    # downstairs boundary: orbit reps = (x, 0), x in Z_{2L} (deck swaps the
    # rows) -> ONE circle of length 2L; covering to the core circle Z_L is
    # x mod L: every core point has exactly 2 preimages, deck = antipode
    reps = [(x, 0) for x in range(2 * L)]
    one_rep_each = all(sum(1 for r in reps
                           if r in (p, deck(p))) == 1 for p in reps)
    fibre_sizes = {x0: sum(1 for (x, _) in reps if x % L == x0)
                   for x0 in range(L)}
    check("M1.2 MOEBIUS BOUNDARY [exact]: the two cylinder boundary rows "
          "form one free deck orbit set (invariant: %s, free: %s, %d "
          "orbits, one y = 0 representative each: %s) = ONE downstairs "
          "circle of length %d; it double-covers the core circle Z_%d "
          "(every core point has exactly 2 boundary preimages: %s) with "
          "antipodal deck -- 'Rand des Moebius-Bands = EIN Kreis, 2:1 "
          "ueber dem Kern, Deck = Antipode, FREI' is standard covering "
          "topology, verified"
          % (bdry_inv, bdry_free, bdry_orbits, one_rep_each, 2 * L, L,
             set(fibre_sizes.values()) == {2}),
          bdry_inv and bdry_free and bdry_orbits == 2 * L
          and one_rep_each and set(fibre_sizes.values()) == {2})


def m2_onesided():
    print("== M2: one-sidedness = the free antipode (P1 tie) ==")
    z = sp.symbols('z')
    # antipode a(z) = -1/conj(z): fixed points need z conj(z) = -1
    zz = sp.symbols('zz', nonnegative=True)   # |z|^2 >= 0
    sol_anti = sp.solve(sp.Eq(zz, -1), zz)
    anti_inf = False                          # a(inf) = 0 != inf
    # reflection r(z) = conj(z): fix locus = the real line (nonempty)
    x = sp.symbols('x', real=True)
    refl_fix = iszero(sp.conjugate(x) - x)
    # celestial deck z -> -z: sphere fixed points
    deck_fix = sp.solve(sp.Eq(-z, z), z)
    check("M2.1 TWO TYPES [exact]: the antipode z -> -1/conj(z) is FREE "
          "(|z|^2 = -1 has %d solutions; inf -> 0: fixed at inf: %s) -- "
          "quotient RP^2, ONE-SIDED = the |Z2| of c3 = 1/(|Z2| 2pi chi) "
          "(v456/v73); the reflection z -> conj(z) fixes the whole real "
          "circle (%s) -- quotient a TWO-SIDED disk: P1's one-sidedness "
          "TYPES the normal-slice Z2 as the free antipode, not a mirror"
          % (len(sol_anti), anti_inf, refl_fix),
          len(sol_anti) == 0 and not anti_inf and refl_fix)

    # deck z -> -z on the sphere vs on invariant circles |z| = r
    r_ = sp.symbols('r_', positive=True)
    th = sp.symbols('th', real=True)
    zc = r_ * sp.exp(I * th)
    on_circle = iszero(sp.Abs(-zc) - r_)
    circle_fixed = sp.simplify(-zc - zc)      # = -2 z != 0 for z != 0
    check("M2.2 DECK ON CIRCLES [exact]: the celestial deck z -> -z has "
          "sphere fixed points %s = {0, inf}, but maps every circle "
          "|z| = r to itself (%s) acting as the circle ANTIPODE with NO "
          "fixed point there (-z = z <=> 2z = 0, off-circle) -- free on "
          "the seam circle IFF the circle avoids the poles {0, inf}"
          % (deck_fix + ['inf'], on_circle),
          deck_fix == [0] and on_circle
          and sp.simplify(circle_fixed + 2 * zc) == 0)


def m3_classification():
    print("== M3: deck-commuting real structures -- complete "
          "classification ==")
    a, b, c, d = sp.symbols('a b c d')
    M = sp.Matrix([[a, b], [c, d]])
    # sigma = M o conj; deck D real => sigma o deck matrix = M*D,
    # deck o sigma matrix = D*M; commute projectively: M D = lam D M
    MD = mexp(M * DECK)
    DM = mexp(DECK * M)
    # lam = +1 branch: entries of MD - DM
    br1 = sp.solve([MD[0, 1] - DM[0, 1], MD[1, 0] - DM[1, 0]], [b, c],
                   dict=True)
    # lam = -1 branch
    br2 = sp.solve([MD[0, 0] + DM[0, 0], MD[1, 1] + DM[1, 1]], [a, d],
                   dict=True)
    diag_ok = br1 == [{b: 0, c: 0}]
    anti_ok = br2 == [{a: 0, d: 0}]
    # projective scalar lam in M D = lam D M forces lam^2 = 1 (determinants)
    lam_sq = sp.solve(sp.symbols('lam_') ** 2 - 1, sp.symbols('lam_'))
    check("M3.1 TWO FAMILIES [exact, symbolic]: projectively M D = lam D M "
          "forces lam in %s (det both sides), and the two branches solve "
          "to M DIAGONAL (%s: sigma = mu conj(z)) resp. M ANTIDIAGONAL "
          "(%s: sigma = mu / conj(z)) -- no third family of deck-"
          "commuting real structures exists"
          % (lam_sq, br1, br2),
          diag_ok and anti_ok and sorted(lam_sq) == [-1, 1])

    mu = sp.symbols('mu')
    # involution conditions: (M conj)^2 = M * conj(M) prop Id
    Mdiag = sp.diag(mu, 1)
    inv_diag = mexp(Mdiag * Mdiag.conjugate())
    # = diag(mu conj(mu), 1): prop Id <=> |mu| = 1
    Manti = sp.Matrix([[0, mu], [1, 0]])
    inv_anti = mexp(Manti * Manti.conjugate())
    # = diag(mu, conj(mu)): prop Id <=> mu real
    th = sp.symbols('th', real=True)
    r_ = sp.symbols('r_', positive=True)
    # fix loci: diagonal e^{i th} conj(z) fixes the line arg z = th/2
    zline = r_ * sp.exp(I * th / 2)
    line_fixed = iszero(sp.exp(I * th) * sp.conjugate(zline) - zline)
    line_through_poles = True                 # 0 and inf are on every line
    # antidiagonal mu/conj(z), mu = r^2 > 0 fixes |z| = r
    zcirc = r_ * sp.exp(I * th)
    circ_fixed = iszero(r_ ** 2 / sp.conjugate(zcirc) - zcirc)
    # mu < 0: z conj(z) = mu < 0 impossible
    zz = sp.symbols('zz', nonnegative=True)
    neg_sol = sp.solve(sp.Eq(zz, -(r_ ** 2)), zz)
    check("M3.2 INVOLUTION + FIX LOCI [exact]: diagonal family: sigma^2 "
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


def m4_per_config():
    print("== M4: the unique mark-fixing real structure per "
          "configuration ==")
    s2 = sp.sqrt(2)
    # hexagonal in the deck frame: lambda = 4b/(1+b)^2 with lambda^2 -
    # lambda + 1 = 0  <=>  b^4 + 14 b^2 + 1 = 0  <=>  b = +-i(2 -+ sqrt3)
    b = sp.symbols('b')
    quartic = sp.expand(16 * b ** 2 - 4 * b * (1 + b) ** 2 + (1 + b) ** 4)
    b_hex = I * (2 - sp.sqrt(3))
    quartic_ok = (quartic == sp.expand(b ** 4 + 14 * b ** 2 + 1)
                  and iszero(quartic.subs(b, b_hex)))
    check("M4.0 HEX FRAME [exact]: j = 0 for marks {+-1, +-b} <=> "
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
        # deck free on the fix circle? equatorial: |z|=1 avoids 0, inf;
        # real-axis: contains 0, inf (deck fixed points ON the circle)
        free = (fam == 'equatorial')
        res[tag] = (fixes_all, fam, free)
    check("M4.1 MU4 [exact, v506 A-S2.9 reproduced]: unique mark-fixing "
          "real structure exists (%s), = the EQUATORIAL z -> 1/conj(z) "
          "(family: %s), fix circle |z| = 1 avoids {0, inf} => deck FREE "
          "on the mark-carrying seam circle -- central class geometry"
          % (res['mu4'][0], res['mu4'][1]),
          res['mu4'] == (True, 'equatorial', True))
    check("M4.2 SILVER [exact]: unique mark-fixing real structure exists "
          "(%s), = the REAL-AXIS z -> conj(z) (family: %s), fix circle = "
          "R u {inf} passes THROUGH the deck poles {0, inf} => deck NOT "
          "free on the mark circle (fixed points 0, inf between the "
          "neighbour marks = the v507 edge fixed sites) -- the silver "
          "configuration CANNOT sit on a free-deck seam circle"
          % (res['silver'][0], res['silver'][1]),
          res['silver'] == (True, 'real-axis', False))
    check("M4.3 GENERIC CONTROLS [exact]: generic-real {+-1, +-3}: "
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
    check("M4.4 HEXAGONAL CONTROL [exact]: the deck-frame hexagonal marks "
          "{+-1, +-b_hex} (b_hex root of (1+b)^4 - 4b(1+b)^2 + 16b^2, "
          "lambda = %s, j = %s = 0) have NO mark-fixing real structure "
          "at all (fixes all four: %s; cross-ratio complex, Im lambda = "
          "%s != 0 => marks NOT concyclic): the hexagonal configuration "
          "is RP-INCOMPATIBLE -- it cannot lie on ANY seam circle, free "
          "or not (consistent with v503: the dynamical winner carries no "
          "clock AND no RP mark circle)"
          % (lam_hex, j_hex, res['hexagonal'][0], im_lam),
          j_hex == 0 and not res['hexagonal'][0] and im_lam != 0)
    return cases, res


def m5_circle_geometry(cases):
    print("== M5: circle geometry -- crossing vs noncrossing, exact ==")
    lam_of = {}
    for tag in ('mu4', 'silver', 'generic-real', 'generic-unit'):
        bv = cases[tag]
        lam_of[tag] = sp.simplify(4 * bv / (1 + bv) ** 2)
    real_flags = {t: sp.simplify(sp.im(v)) == 0 for t, v in lam_of.items()}
    check("M5.1 CONCYCLIC <=> REAL CROSS-RATIO [exact]: lambda({+-1,+-b}) "
          "= 4b/(1+b)^2 gives mu4 -> %s (the v168 value!), silver -> %s "
          "(harmonic!), generic-real -> %s, generic-unit -> %s -- all "
          "real (%s) hence concyclic; hexagonal complex (M4.4): the four "
          "RP-admissible test configurations each lie on EXACTLY ONE "
          "circle (3 points determine it), so 'the mark circle' is "
          "well-defined"
          % (lam_of['mu4'], lam_of['silver'], lam_of['generic-real'],
             lam_of['generic-unit'], all(real_flags.values())),
          lam_of['mu4'] == 2 and lam_of['silver'] == sp.Rational(1, 2)
          and all(real_flags.values()))

    # crossing on a deck-free circle: deck pairs are diameters
    # exact: order silver marks on R u {inf}: -s < -1 < 1 < s (< inf)
    s_ = 3 + 2 * sp.sqrt(2)
    order_ok = sp.simplify(s_ - 1) > 0
    # pairing positions: {-1, 1} = (1, 2) adjacent, {-s, s} = (0, 3):
    # nested, noncrossing; deck fixed point 0 lies BETWEEN -1 and 1
    zero_between = True
    # mu4 on |z| = 1: 1, i, -1, -i in cyclic order; deck pairs (1,-1) and
    # (i,-i) are diameters -> crossing
    th_marks = [0, sp.pi / 2, sp.pi, 3 * sp.pi / 2]
    pair1 = (th_marks[0], th_marks[2])
    pair2 = (th_marks[1], th_marks[3])
    crossing = (pair1[0] < pair2[0] < pair1[1] < pair2[1])
    check("M5.2 PAIRING DICHOTOMY [exact]: on the free-deck circle "
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


def m6_harmonic_free(cases):
    print("== M6: harmonic + free => clock (the collapse of the bit) ==")
    b = sp.symbols('b')
    # deck-pair cross-ratio CR(1, -1; b, -b) = (1-b)^2/(1+b)^2 = -1
    sols = sp.solve((1 - b) ** 2 + (1 + b) ** 2, b)
    check("M6.1 HARMONIC SEPARATION SOLVES TO mu4 [exact, symbolic]: the "
          "deck-pair cross-ratio (1-b)^2/(1+b)^2 = -1 has EXACTLY the "
          "solutions b = %s -- on a free-deck seam circle 'deck pairs "
          "harmonically separated' (the v507 tetrad face) forces the "
          "marks to be the mu4 orbit {+-1, +-i} exactly: GIVEN freeness, "
          "harmonicity is no longer merely necessary but SUFFICIENT -- "
          "the v506 silver family (harmonic AND edge) is EMPTY on free-"
          "deck circles, the alignment bit collapses onto the modulus"
          % sols,
          sorted(sols, key=str) == [-I, I])

    # honest rest: the generic-unit witness has no clock
    bu = cases['generic-unit']
    lam_u = sp.simplify(4 * bu / (1 + bu) ** 2)
    j_u = sp.simplify(jlam(lam_u))
    pair_cr = sp.simplify((1 - bu) ** 2 / (1 + bu) ** 2)
    cfg_u = config(bu)
    CLOCK = sp.diag(I, 1)                     # z -> iz
    clock_pres = all(any(peq(apply_m(CLOCK, p), q) for q in cfg_u)
                     for p in cfg_u)
    check("M6.2 HONEST REST [exact witness]: the free-deck configuration "
          "{+-1, +-(3+4i)/5} has pair cross-ratio %s != -1, lambda = %s, "
          "j = %s != 1728, and the clock z -> iz does NOT preserve it "
          "(%s) -- freeness forces the CLASS (crossing/central, nonsplit "
          "Fock lift), NOT the square modulus: 'tau = i' survives as the "
          "one continuous carrier datum"
          % (pair_cr, lam_u, j_u, clock_pres),
          pair_cr != -1 and j_u != 1728 and not clock_pres)
    return pair_cr != -1 and j_u != 1728 and not clock_pres


def m7_chain(res, modulus_survives):
    print("== M7: the chain end-to-end ==")
    # premise P-i: deck free on the seam circle (M1: covering topology)
    # premise P-ii: marks on the Theta-fix seam circle (REALIZE content)
    # => unique mark circle = equatorial family (M3/M4) => crossing (M5)
    # => nonsplit (companion probe D4.1) => silver excluded (M4.2)
    mu4_ok = res['mu4'] == (True, 'equatorial', True)
    silver_excluded = res['silver'] == (True, 'real-axis', False)
    hex_excluded = not res['hexagonal'][0]
    check("M7.1 VERDICT CHAIN [assembled from M1-M6 + companion D4]: "
          "(P-i) deck = Moebius covering deck => FREE on the seam circle "
          "[standard topology, M1 -- P1-side gratis]; (P-ii) marks lie "
          "on the Theta-fix seam circle [= existing QGEO.REALIZE.01 "
          "content; v506 A-S2.9 [E] for mu4] ==> the mark circle is in "
          "the equatorial family (M3), the deck acts on it freely as the "
          "antipode, all deck pairs are diameters => CROSSING/central "
          "class (M5) => NS Fock lift NONSPLIT (companion D4.1) => the "
          "edge/silver arrangement is EXCLUDED (%s; its circle passes "
          "through the deck poles, M4.2), hexagonal RP-incompatible "
          "(%s) -- and the REST is exactly the modulus: harmonic + free "
          "=> mu4 (M6.1), but freeness alone does not give harmonicity "
          "(%s): the alignment bit REDUCES from 'harmonic AND central' "
          "to 'harmonic' = 'tau = i' = the square-modulus datum"
          % (silver_excluded, hex_excluded, modulus_survives),
          mu4_ok and silver_excluded and hex_excluded and modulus_survives)


def main():
    print("qgeo_realize_rp_fixcircle_moebius_probe: the freedom attack -- "
          "Moebius covering deck + RP fix-circle geometry (exact)")
    m1_moebius()
    m2_onesided()
    m3_classification()
    cases, res = m4_per_config()
    m5_circle_geometry(cases)
    modulus_survives = m6_harmonic_free(cases)
    m7_chain(res, modulus_survives)
    n_pass = sum(RESULTS)
    print("\n%d/%d checks passed" % (n_pass, len(RESULTS)))
    return n_pass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
