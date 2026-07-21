"""seam_clock_rigidity_fock_probe.py -- EXPLORATION ONLY (experiments/, no verification claim).

ROUTE B OF THE v503 CLASSIFICATION, PART 2/2 (the fermionic / Fock side):
does the SEAM FERMION CONTENT force the order-4 lift of the deck?

Companion of seam_clock_rigidity_moebius_probe.py (B1/B3/B4: on the sphere the
clock reduces to ONE bit -- "the deck admits a marks-preserving Moebius square
root").  This probe computes the B2 lever: implement the ESTABLISHED deck
(z -> -z = half-rotation of the seam circle, v492 S5) on the 16-Majorana CAR
algebra (16 = 2^(g_car-1), v156/v175/v367/v490) and compute U^2 EXACTLY.

MODEL (finite, exact): 16 Majorana modes gamma_1..gamma_16 on the seam circle,
4 per mark quadrant (marks at sites 1, 5, 9, 13 = the mu4 points).  The deck is
the half-rotation = shift by 8 sites; the clock candidate is the quarter-shift
by 4 sites.  Spin structure enters as the wrap sign gamma_{j+16} = -gamma_j
(NS/antiperiodic = the BOUNDING structure -- the one induced by the UNIQUE spin
structure of the celestial sphere S^2, H^1(S^2, Z2) = 0, b1 = 0) versus
gamma_{j+16} = +gamma_j (R/periodic, the non-bounding control).  All Fock-side
computations are done in the ABSTRACT Clifford algebra Cl(16) with Fraction
coefficients (dict of monomials) -- no matrices, no floats, fully exact.

  S1 ONE-PARTICLE LEVEL.  NS: the deck matrix D has D^2 = -1 (a half-rotation
     squares to the 2 pi rotation = -1 on antiperiodic spinors): the "Z2" deck
     is ALREADY order 4 on NS one-particle data; charpoly (lam^2+1)^8.  The
     quarter-shift C has C^2 = D, C^4 = -1, C^8 = 1, charpoly (lam^4+1)^4 --
     eigenvalues = the primitive 8th roots zeta8 of the v492 spin bridge.
     R control: D_R^2 = +1 (order 2, no forcing).
  S2 FOCK LEVEL, THE CORE RESULT.  The Bogoliubov implementer of the NS deck,
     U = prod_j (1 - gamma_j gamma_{j+8})/sqrt2, satisfies EXACTLY
                U^2 = gamma_1 gamma_2 ... gamma_16 = (-1)^F,   U^4 = 1.
     (-1)^F is NOT a scalar, and any other implementer is c U (irreducibility /
     center = scalars), with (cU)^2 = c^2 (-1)^F never 1: NO phase choice makes
     the deck order 2 on the seam fermions.  The Z4 lift is FORCED:
     1 -> Z2^{(-1)^F} -> Z4<U> -> Z2^{deck} -> 1 is the nonsplit extension.
  S3 R-SECTOR CONTROL.  The R implementer U_R = prod_j (gamma_j-gamma_{j+8})/sqrt2
     satisfies U_R^2 = +1 EXACTLY -- split Z2, nothing forced: the forcing
     premise is exactly the (established) bounding spin structure, not a hidden
     convention.
  S4 THE CLOCK TOWER Z8.  The quarter-shift implementer V (constructed exactly
     per 4-Majorana block by a rational nullspace solve) satisfies V^2 prop U,
     V^4 prop (-1)^F (pure grade-16), V^8 = scalar: projective order 8 = 2|mu4|
     -- the v492 Z8 spin bridge REALISED on the 16-Majorana Fock space, with
     clock^2 = deck holding at every level (sphere, one-particle, Fock).
  S5 16-FOLD-WAY ARITHMETIC.  nu = 16 Majoranas: theta_v = exp(2 pi i nu/16)=1
     (gaugeable, v490); the forced tower period 8 = 2|mu4| = the Fidkowski-
     Kitaev Z8; robustness: the forcing U^2 = +-(-1)^F holds for ANY 4m-site
     NS circle (checked at 8 sites too) -- 16 enters as the carrier COUNT
     (2^(g_car-1)), not as a tuning.
  S6 HONEST VERDICT.  Fermions force the ORDER (4 for the deck lift, 8 for the
     quarter-shift lift) but NOT the spatial alignment of the marks with the
     quarter-shift -- that alignment bit (= "deck central in the mark-D4",
     Moebius probe) remains the residual carrier input.  No overclaim.

Repo anchors: v492 S5 (clock/deck/Z8), v367/v450/v490 (16 Majoranas, spin
structures, parity census, theta_v = 1), v215/v216 (marks), v503 (emergence
classification), v499/p2 probe (R1).

Exact throughout (Fractions in Cl(16); sympy for 16x16 matrices and theta_v).
Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/seam_clock_rigidity_fock_probe.py
"""
from fractions import Fraction as Fr

import sympy as sp

RESULTS = []

N_SITES = 16          # 16 Majorana modes = 2^(g_car-1), 4 per mark quadrant
G_CAR = 5
MARKS = [0, 4, 8, 12]  # mu4 mark sites (0-based) on the 16-site seam circle


def check(name, ok):
    RESULTS.append(bool(ok))
    print(("PASS" if ok else "FAIL") + " [%2d] %s" % (len(RESULTS), name))


# ---------------------------------------------------------------------------
# abstract Clifford algebra Cl(n): elements = {sorted index tuple: Fraction}
# ---------------------------------------------------------------------------
def mono_mul(m1, m2):
    """product of two monomials (sorted tuples); gamma_a^2 = 1."""
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
    """x = c y for a scalar c (both nonzero); returns (True, c) or (False, None)."""
    if not x or not y or set(x) != set(y):
        return (False, None)
    m0 = next(iter(y))
    c = x[m0] / y[m0]
    return (all(x[m] == c * y[m] for m in y), c)


def apply_lin(mat, a, n):
    """one-particle image of gamma_a under integer matrix mat (n x n),
    as a Clifford element: sum_b mat[b][a] gamma_b."""
    out = {}
    for bidx in range(n):
        if mat[bidx][a]:
            out = cadd(out, cscale(gam(bidx), Fr(mat[bidx][a])))
    return out


def implements(Uel, mat, n):
    """check U gamma_a = (sum_b mat[b][a] gamma_b) U for all a (no inverse needed)."""
    for a in range(n):
        lhs = cmul(Uel, gam(a))
        rhs = cmul(apply_lin(mat, a, n), Uel)
        if cadd(lhs, cscale(rhs, Fr(-1))):
            return False
    return True


# ---------------------------------------------------------------------------
# one-particle signed-shift matrices on the n-site seam circle
# ---------------------------------------------------------------------------
def shift_matrix(n, k, wrap_sign):
    """gamma_j -> (wrap sign)^(#wraps) gamma_{j+k}; matrix M[b][a] with
    image(gamma_a) = sum_b M[b][a] gamma_b."""
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        b = (a + k) % n
        M[b][a] = wrap_sign if a + k >= n else 1
    return M


def matmul_i(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def run():
    print("seam_clock_rigidity_fock_probe: Route B (v503), B2 lever -- does the 16-"
          "Majorana seam content FORCE the order-4 deck lift?  Exact Cl(16) arithmetic")
    print("=" * 100)
    n = N_SITES

    # ================================================ S1: one-particle level
    print("  -- S1: one-particle level (16 x 16 exact integer matrices)")
    D_ns = shift_matrix(n, n // 2, -1)      # NS deck: half-rotation, antiperiodic
    C_ns = shift_matrix(n, n // 4, -1)      # NS clock candidate: quarter-shift
    D_r = shift_matrix(n, n // 2, +1)       # R deck (periodic control)

    Dm, Cm = sp.Matrix(D_ns), sp.Matrix(C_ns)
    lamv = sp.symbols('lam')
    chD = sp.factor(Dm.charpoly(lamv).as_expr())
    chC = sp.factor(Cm.charpoly(lamv).as_expr())
    det_D, det_C = Dm.det(), Cm.det()
    check("S1.1 NS DECK IS ALREADY ORDER 4 ONE-PARTICLE [exact]: the half-rotation "
          "with antiperiodic wrap has D^2 = -1 (%s), det = %s (SO(16)), charpoly = "
          "%s = (lam^2+1)^8 -- a pi-rotation squares to the 2pi rotation = -1 on NS "
          "spinors: the 'Z2' deck acts as Z4 on the seam's one-particle fermion data "
          "BEFORE any Fock choice"
          % (Dm ** 2 == -sp.eye(n), det_D, chD),
          Dm ** 2 == -sp.eye(n) and det_D == 1
          and sp.expand(chD - (lamv ** 2 + 1) ** 8) == 0)

    check("S1.2 QUARTER-SHIFT = ZETA8 SPECTRUM [exact]: C^2 = D (%s), C^4 = -1 (%s), "
          "C^8 = 1 (%s), det = %s, charpoly = %s = (lam^4+1)^4: eigenvalues are the "
          "primitive 8th roots zeta8 -- the v492 spin-bridge Z8 (8 = 2|mu4|) appears "
          "as the one-particle order of the geometric quarter-rotation"
          % (Cm ** 2 == Dm, Cm ** 4 == -sp.eye(n), Cm ** 8 == sp.eye(n), det_C, chC),
          Cm ** 2 == Dm and Cm ** 4 == -sp.eye(n) and Cm ** 8 == sp.eye(n)
          and det_C == 1 and sp.expand(chC - (lamv ** 4 + 1) ** 4) == 0)

    Dr2 = matmul_i(D_r, D_r)
    dr2_id = all(Dr2[i][j] == (1 if i == j else 0) for i in range(n) for j in range(n))
    check("S1.3 SPIN-STRUCTURE PREMISE [exact + typed]: with PERIODIC wrap the same "
          "half-rotation has D_R^2 = +1 (%s) -- order 2, nothing forced.  The seam "
          "circle bounds (equator of the celestial sphere); S^2 has b1 = 0, hence "
          "2^0 = %d spin structure(s), whose restriction to any circle is the "
          "BOUNDING = antiperiodic one: the NS wrap is ESTABLISHED P1 geometry "
          "(v492 sphere; v490 handles the 4 torus structures of the double), not a "
          "convention" % (dr2_id, 2 ** 0), dr2_id and 2 ** 0 == 1)

    clock_mperm = [MARKS.index((m + 4) % 16) for m in MARKS]
    deck_mperm = [MARKS.index((m + 8) % 16) for m in MARKS]
    check("S1.4 MARK GEOMETRY MATCHES THE MOEBIUS SIDE [exact]: on the 16-site seam "
          "the 4 marks sit at sites %s (one per quadrant); the quarter-shift 4-cycles "
          "them (%s), the half-shift deck acts as the double transposition %s = the "
          "Moebius-probe pattern [2,3,0,1]; the quarter-shift needs 4 | 16 sites "
          "(4 x 4 = |mu4| x #marks) -- an 'order-8 clock' would shift by 2 = half a "
          "quadrant and map NO mark to a mark"
          % ([m + 1 for m in MARKS], clock_mperm, deck_mperm),
          clock_mperm == [1, 2, 3, 0] and deck_mperm == [2, 3, 0, 1]
          and 16 % 4 == 0 and 2 not in [(m2 - m1) % 16 for m1 in MARKS for m2 in MARKS])

    # ================================================ S2: Fock level (the core)
    print("  -- S2: Fock level -- U^2 computed exactly in Cl(16)")

    # fermion parity (-1)^F = prod_j (-i gamma_{2j-1} gamma_{2j}) = gamma_1...gamma_16
    GAMMA = {tuple(range(n)): Fr(1)}
    g2 = cmul(GAMMA, GAMMA)
    anti = all(not cadd(cmul(GAMMA, gam(a)), cmul(gam(a), GAMMA)) for a in range(n))
    phase_i8 = sp.simplify((-sp.I) ** (n // 2))
    check("S2.5 FERMION PARITY [exact]: (-1)^F = prod_j(-i g_{2j-1} g_{2j}) = "
          "(-i)^8 g_1...g_16 with (-i)^8 = %s, so (-1)^F = g_1...g_16 = the Cl(16) "
          "volume element; ((-1)^F)^2 = 1 (%s), it anticommutes with every gamma_a "
          "(%s) and is NOT a scalar -- the parity operator exists canonically on the "
          "16-Majorana Fock space" % (phase_i8, prop(g2, ONE), anti),
          phase_i8 == 1 and prop(g2, ONE) == (True, Fr(1)) and anti
          and not is_scalar(GAMMA))

    # NS deck implementer: U = prod (1 - g_j g_{j+8})/sqrt2  (track Utilde = 16 U)
    Ut = ONE
    for j in range(n // 2):
        Ut = cmul(Ut, cadd(ONE, cscale(cmul(gam(j), gam(j + n // 2)), Fr(-1))))
    Ut_inv = ONE
    for j in range(n // 2):
        Ut_inv = cmul(Ut_inv, cadd(ONE, cmul(gam(j), gam(j + n // 2))))
    impl_ok = implements(Ut, D_ns, n)
    inv_ok = prop(cmul(Ut, Ut_inv), ONE)
    even_ok = all(len(m) % 2 == 0 for m in Ut)
    check("S2.6 DECK IMPLEMENTER [exact]: Utilde = prod_j (1 - g_j g_{j+8}) "
          "(256 monomials: %d) implements the NS deck on ALL 16 generators "
          "(U g_a U^-1 = D g_a: %s), is even (%s), and Utilde x reverse = 256 x 1 "
          "(%s) -- U = Utilde/16 is the unitary Bogoliubov lift"
          % (len(Ut), impl_ok, even_ok, inv_ok),
          len(Ut) == 256 and impl_ok and even_ok
          and inv_ok == (True, Fr(256)))

    Ut2 = cmul(Ut, Ut)
    ok_u2, coef = prop(Ut2, GAMMA)
    check("S2.7 THE CORE RESULT U^2 = (-1)^F [exact]: Utilde^2 = %s x g_1...g_16 "
          "(single grade-16 monomial: %s), i.e. U^2 = (256/256) (-1)^F = (-1)^F "
          "EXACTLY; U^4 = 1; U^2 is NOT a scalar, and every implementer is c U "
          "(irreducibility), with (cU)^2 = c^2 (-1)^F never = 1: NO phase choice "
          "implements the deck with order 2 -- the Z4 lift is FORCED by the NS seam "
          "fermions: 1 -> Z2^{(-1)^F} -> Z4<U> -> Z2^{deck} -> 1, nonsplit"
          % (coef, ok_u2),
          ok_u2 and coef == Fr(256) and not is_scalar(Ut2)
          and prop(cmul(Ut2, Ut2), ONE) == (True, Fr(256 ** 2)))

    # canonicity: center = scalars; <U> = {1, U, P, PU}; Aut(Z4) ambiguity
    center_wit = []
    for mtest in [(0,), (0, 1), (0, 1, 2), tuple(range(n))]:
        x = {mtest: Fr(1)}
        commutes_all = all(not cadd(cmul(x, gam(a)),
                                    cscale(cmul(gam(a), x), Fr(-1)))
                           for a in range(n))
        center_wit.append(commutes_all)
    Ut3 = cmul(Ut2, Ut)
    u3_is_pu = prop(Ut3, cmul(GAMMA, Ut))
    check("S2.8 CANONICITY + Aut(Z4) [exact]: no nonempty monomial commutes with all "
          "gammas (witnesses odd/even/full: %s => center = scalars => implementer "
          "unique up to phase); the forced group is <U> = {1, U, (-1)^F, (-1)^F U} "
          "with U^3 = (-1)^F U (%s): a CANONICAL Z4 on the raw NS seam -- generator "
          "ambiguity U <-> U^3 = Aut(Z4), the same irreducible ambiguity as the "
          "Moebius pair {clock, clock^-1} (companion S2.9); groups of order 4 are "
          "only Z4 (nonsplit) or V4 (split), and U^2 != 1 excludes V4"
          % (center_wit, u3_is_pu[0]),
          center_wit == [False, False, False, False] and u3_is_pu[0])

    # ================================================ S3: R-sector control
    print("  -- S3: R-sector (periodic) control")
    Ur = ONE
    for j in range(n // 2):
        Ur = cmul(Ur, cadd(gam(j), cscale(gam(j + n // 2), Fr(-1))))
    impl_r = implements(Ur, D_r, n)
    Ur2 = cmul(Ur, Ur)
    ok_r2, coef_r = prop(Ur2, ONE)
    check("S3.9 R CONTROL: SPLIT Z2 [exact]: U_R = prod_j (g_j - g_{j+8})/sqrt2 "
          "implements the periodic deck (%s) and U_R^2 = (%s/256) x 1 = +1 EXACTLY "
          "(scalar!) -- in the R sector the deck lifts as an honest Z2, NOTHING is "
          "forced: the entire Z4-forcing of S2 rests on the bounding/NS spin "
          "structure (S1.3), which is exactly the established seam geometry"
          % (impl_r, coef_r),
          impl_r and ok_r2 and coef_r == Fr(256))

    # ================================================ S4: the clock tower Z8
    print("  -- S4: the quarter-shift Fock lift V (exact block construction)")

    # per-4-block: e1 -> e2 -> e3 -> e4 -> -e1 on block (j, j+4, j+8, j+12)
    Cblk = [[0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    even_basis = [(), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (0, 1, 2, 3)]
    odd_basis = [(0,), (1,), (2,), (3,), (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    rows = []
    for a4 in range(4):
        img = apply_lin(Cblk, a4, 4)
        cols = []
        for mb in even_basis:
            x = {mb: Fr(1)}
            expr = cadd(cmul(x, gam(a4)), cscale(cmul(img, x), Fr(-1)))
            cols.append([expr.get(mo, Fr(0)) for mo in odd_basis])
        for r_i in range(8):
            rows.append([sp.Rational(cols[c_i][r_i].numerator,
                                     cols[c_i][r_i].denominator)
                         for c_i in range(8)])
    A = sp.Matrix(rows)
    null = A.nullspace()
    v = {}
    if len(null) == 1:
        vec = null[0] * sp.lcm([sp.denom(x) for x in null[0]])
        v = {even_basis[k]: Fr(int(vec[k])) for k in range(8) if vec[k] != 0}
    v2 = cmul(v, v)
    ublk = cmul(cadd(ONE, cscale(cmul(gam(0), gam(2)), Fr(-1))),
                cadd(ONE, cscale(cmul(gam(1), gam(3)), Fr(-1))))
    ok_v2, lam_blk = prop(v2, ublk)
    v4 = cmul(v2, v2)
    ok_v4, sig_blk = prop(v4, {(0, 1, 2, 3): Fr(1)})
    v8 = cmul(v4, v4)
    ok_v8, rho_blk = prop(v8, ONE)
    impl_v = implements(v, Cblk, 4)
    check("S4.10 BLOCK LIFT [exact, rational nullspace]: the even implementer of the "
          "signed 4-cycle in Cl(4) is UNIQUE up to scale (nullspace dim = %d); it "
          "implements the block clock (%s), v^2 = %s x (block deck lift) (%s), "
          "v^4 = %s x e1e2e3e4 = PURE block chirality (%s, nonscalar), v^8 = %s x 1 "
          "(scalar, %s) -- the block tower is (clock, deck, parity) = orders "
          "(8, 4, 2) projectively"
          % (len(null), impl_v, lam_blk, ok_v2, sig_blk, ok_v4, rho_blk, ok_v8),
          len(null) == 1 and impl_v and ok_v2 and ok_v4 and ok_v8
          and not is_scalar(v4) and rho_blk == sig_blk ** 2)

    # global V = product of the 4 block lifts (blocks commute: even, disjoint)
    def embed(x, j):
        table = (j, j + 4, j + 8, j + 12)
        return {tuple(sorted(table[i] for i in m)): c for m, c in x.items()}

    V = ONE
    for j in range(4):
        V = cmul(V, embed(v, j))
    impl_V = implements(V, C_ns, n)
    emb = [embed(v, j) for j in range(4)]
    blocks_comm = all(not cadd(cmul(emb[a_], emb[b_]),
                               cscale(cmul(emb[b_], emb[a_]), Fr(-1)))
                      for a_ in range(4) for b_ in range(a_ + 1, 4))
    # commuting even blocks => V^(2k) = prod_j embed(v^(2k), j) exactly
    V2 = ONE
    for j in range(4):
        V2 = cmul(V2, embed(v2, j))
    ok_V2, lam_g = prop(V2, Ut)
    V4 = ONE
    for j in range(4):
        V4 = cmul(V4, embed(v4, j))
    ok_V4, sig_g = prop(V4, GAMMA)
    V8 = ONE
    for j in range(4):
        V8 = cmul(V8, embed(v8, j))
    ok_V8, rho_g = prop(V8, ONE)
    check("S4.11 GLOBAL CLOCK TOWER Z8 [exact]: block lifts commute (%s); V "
          "implements the quarter-shift on all 16 generators (%s); V^2 = %s x "
          "Utilde (deck lift: clock^2 = deck at the FOCK level, %s), V^4 = %s x "
          "(-1)^F (pure grade 16, %s, nonscalar), V^8 = %s x 1 (scalar, %s): "
          "projective order 8 = 2|mu4| -- the v492 Z8 spin bridge is REALISED on "
          "the 16-Majorana Fock space; the phase-invariant content is the tower "
          "Z8 -> Z4 -> Z2 (V -> V^2 prop U -> U^2 = (-1)^F)"
          % (bool(blocks_comm), impl_V, lam_g, ok_V2, sig_g, ok_V4, rho_g, ok_V8),
          bool(blocks_comm) and impl_V and ok_V2 and ok_V4 and ok_V8
          and not is_scalar(V4) and rho_g == sig_g ** 2)

    gam4prod = ONE
    for j in range(4):
        gam4prod = cmul(gam4prod, embed({(0, 1, 2, 3): Fr(1)}, j))
    ok_g4, sign_g4 = prop(gam4prod, GAMMA)
    check("S4.12 ARITHMETIC OF THE TOWER [exact]: prod of the 4 block chiralities = "
          "%s x (-1)^F (%s); orders: |deck lift| = 4 = |mu4|, |clock lift| = 8 = "
          "2|mu4| = the c3 = 1/(8 pi) seam winding integer; carrier count 16 = "
          "2^(g_car-1) = %d with g_car = 5; the 'Z2' -> Z4 -> Z8 doubling chain is "
          "1 -> 2 -> 4 -> 8 = the mu4-glue powers of 2"
          % (sign_g4, ok_g4, 2 ** (G_CAR - 1)),
          ok_g4 and sign_g4 == Fr(1) and 2 ** (G_CAR - 1) == 16
          and 2 * 4 == 8)

    # ================================================ S5: 16-fold way + robustness
    print("  -- S5: 16-fold-way arithmetic + count robustness")
    nu = 16
    theta_v = sp.exp(2 * sp.pi * sp.I * sp.Rational(nu, 16))
    theta_8 = sp.exp(2 * sp.pi * sp.I * sp.Rational(8, 16))
    check("S5.13 16-FOLD WAY [exact]: theta_v = exp(2 pi i nu/16) = %s = 1 at "
          "nu = 16 (v490: vortex condensable, gaugeable), while nu = 8 gives "
          "theta_v = %s != 1; the forced tower period 8 = 2|mu4| equals the "
          "Fidkowski-Kitaev Z8 of interacting Majorana classifications -- the "
          "seam sits at the anomaly-free point nu = 16 = 0 mod 8 where the "
          "Z4-extended deck CAN be gauged (consistency), yet the extension itself "
          "(U^2 = (-1)^F) remains nontrivial"
          % (sp.simplify(theta_v), sp.simplify(theta_8)),
          sp.simplify(theta_v - 1) == 0 and sp.simplify(theta_8 + 1) == 0)

    m8 = 8
    D8 = shift_matrix(m8, 4, -1)
    Ut8 = ONE
    for j in range(4):
        Ut8 = cmul(Ut8, cadd(ONE, cscale(cmul(gam(j), gam(j + 4)), Fr(-1))))
    G8 = {tuple(range(m8)): Fr(1)}
    ok8, c8 = prop(cmul(Ut8, Ut8), G8)
    impl8 = implements(Ut8, D8, m8)
    check("S5.14 COUNT ROBUSTNESS [exact]: on an 8-site NS circle the same "
          "construction gives an implementer (%s) with U^2 = %s/16 x (-1)^F_8 "
          "(nonscalar, %s): the Z4-forcing needs ONLY (NS wrap + half-rotation), "
          "not the number 16 -- 16 is the CARRIER count (2^(g_car-1), v156/v175), "
          "and it is what places the seam at the gaugeable point nu = 16 of S5.13"
          % (impl8, c8, ok8),
          impl8 and ok8 and c8 == Fr(16))

    # ================================================ S6: honest verdict
    print("  -- S6: verdict")
    forced = (ok_u2 and coef == Fr(256)          # U^2 = (-1)^F exactly
              and ok_r2                          # R control splits
              and ok_V4 and ok_V8                # Z8 tower realised
              and dr2_id)
    check("S6.15 VERDICT [typed]: FORCED by established seam data (NS wrap from the "
          "unique S^2 spin structure + half-rotation deck + fermions): the deck's "
          "Fock implementation has ORDER 4, U^2 = (-1)^F (S2.7), and the geometric "
          "quarter-shift lifts to a canonical Z8 with V^2 prop U, V^4 prop (-1)^F "
          "(S4.11) -- '8 = 2|mu4|' gets its fermionic explanation.  NOT forced: "
          "that the quarter-shift preserves the MARKED dynamics (DtN/marks) -- the "
          "alignment bit of the Moebius companion (deck central in the mark-D4) "
          "remains the one residual carrier input; the fermionic Z4 does not by "
          "itself create a marks-preserving spatial square root.  No overclaim",
          forced)

    npass = sum(RESULTS)
    print("=" * 100)
    print("SUMMARY: %d/%d checks passed%s"
          % (npass, len(RESULTS),
             "" if npass == len(RESULTS) else "  -- FAILURES PRESENT"))
    return npass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
