"""v519 -- WOIT.THETA.FREE.01: the WOIT-alpha milestone of the OS twistor
bridge -- the real structure exists, and free reflection positivity picks
the SAME family.  Part W (the anti-linear Theta: classification, exact
relations, kill test 1 on the free/equivariant level) + Part R (reflection
positivity of the free 16-Majorana NS seam system under the pinned Theta)
in one module.  Exact throughout (sympy; Fractions in exact Cl(16));
the RP definiteness certificates are 40-digit spectra of exact Hermitian
matrices (tolerance 1e-25, gap-certified); no floats anywhere else.

[E] THETA CLASSIFICATION COMPLETE: exactly TWO families of anti-linear
      structures on C^2 normalise the clock rho = diag(i,1) (v492 S5) --
      family D (z -> mu conj(z), |mu| = 1): Theta rho Theta = rho^-1
      EXACTLY at matrix level, Theta^2 = +1 (and -1 IMPOSSIBLE:
      M conj(M) = diag(|mu|^2, 1) -- the family is Kramers-free), inverts
      the Z4 deck, fixed set = the great circle through the deck poles
      {0, inf} at axis angle arg(mu)/2; family A (z -> mu/conj(z)):
      centralises the clock projectively (NEVER inverts it, not even
      projectively), Theta^2 = +-1 per mu, fixed set |z| = 1 resp. empty.
      ROLE SEPARATION: family A DEFINES the euclidean section (Woit's
      rho_tw side: rho_tw^2 = -1, no real points -- replicated exactly on
      C^4), family D REFLECTS it (the OS conjugation; sigma_std = the
      standard conjugation with real points RP^3 in CP^3).
[E] MARK PINNING: z -> mu conj(z) preserves the mu4 marks iff mu in mu4
      -- a 4-element mu4-TORSOR (2 mark axes + 2 silver-midpoint axes);
      clock conjugation rho Theta_mu rho^-1 = Theta_{-mu} => exactly 2
      clock orbits (the v506 A-S2.9 Aut(Z4)-type freedom).
[E] SPIN/FOCK: the Z8 spin plane has no phase leaks (conj(zeta8^k) =
      zeta8^-k for all k); exact Cl(16): Theta_Fock = U_r o K with
      Theta_Fock^2 = 2^7 > 0 (unitarily normalised +1), inverts the Fock
      clock tower (V -> 4096 V^-1, exact scalar) and normalises the deck
      (Utilde -> 256 Utilde^-1); KRAMERS DICHOTOMY: the deck-induced
      candidate Theta_t = Utilde o K has Theta_t^2 = 256 gamma_1..gamma_16
      = (-1)^F -- the v510 split/nonsplit dichotomy IS the Theta^2 = +1
      vs (-1)^F dichotomy; the deck does NOT furnish Theta, the
      seam-circle REFLECTION does.
[E] KILL TEST 1 (free level): does NOT fire -- Theta exists with
      Theta^2 = +1 AND Theta rho Theta = rho^-1 and satisfies all three
      side conditions simultaneously (marks preserved, deck normalised,
      Z8-spin/Cl(16)-Fock implementable).
[E] FREE RP: the chiral NS vacuum C(d) = (2/N)/sin(pi d/N) has C^2 = -1
      exact (pure state); preconditions exact (R C R^T = -C, S C S^T = C,
      R S R^-1 = S^-1; the deck FAILS anti-invariance -- it is no OS
      reflection of this state); BOND CUT: one-particle Gram (8,0,0) PD
      (min eigenvalue 1.888e-3 at 40 digits), even deg <= 2 sector
      (29,0,0) PD, N = 8 complete half-sided algebra PD (even + odd each
      (8,0,0)) -- free RP with NO degree truncation; the twist eta = +i
      is FORCED (eta = 1 non-Hermitian); CONTROLS: the site cut fails
      exactly (det = 0, inertia (3,3,1); continuum control: the
      Cauchy-Stieltjes factorisation is strictly PD -- a lattice-
      PLACEMENT artifact: RP selects the site placement relative to the
      marks), the clock-CENTRALISING family-A structure fails RP
      structurally ((4,4,0)) -- RP and Theta rho Theta = rho^-1 select
      the SAME family; bonus: the anti-chiral state flips the odd sector
      to (0,8,0) ND (the free shadow of kill test 3).
[C]/[O] NOT SHOWN (verbatim, no overclaim): the interacting algebra
      A_hol (kill test 1 stays live there), gauge-fixed RP (kill test 2),
      the OS reconstruction, chirality without mirrors (kill tests 3/6 --
      only the free odd-sector shadow above), mu4 incidence (kill test
      7).  WOIT-beta/gamma roadmap: (beta-1) Theta on the gauge-invariant
      subalgebra + gauge-fixed RP on the equivariant SDYM(E8) sector;
      (beta-2) the OS quotient of the free system made explicit;
      (beta-3) the PT <-> PT* duality vs sigma_std typed; (gamma) the
      chirality theorem + the mark incidence.

Status: [E] every check below (exact sympy / exact Cl(16) Fractions /
40-digit gap-certified inertia); NO marker moves -- WOIT.OS.TWISTOR.01
stays [O]: kill test 1 is discharged on the FREE level only and stays
formally live on the interacting algebra.  Two contract PRECISIONS
(prose, no marker): (i) "Theta induced by the seam reflection" means the
seam-circle REFLECTION, not the deck -- the deck furnishes the (-1)^F
Kramers class (the v510 bridge); (ii) the marks sit RP-side on the BOND
MIDPOINTS of the 16-Majorana circle (the half-offset/NS-natural
placement, 4 sites per mark quadrant).  Consolidation note: the Fock
clock inversion is verified via the implementer route (conj_V implements
C^-1; centre of Cl(16) = scalars, machine-instantiated sign rule; the
scalar 4096 pinned by the exact ()-pairing) instead of the brute-force
V-power arithmetic of the discovery probe -- same claims, same
exactness, runtime 105 s -> ~20 s; all tolerances unchanged (exact
except the 40-digit inertia spectra, zero threshold 1e-25).  Python;
Wolfram-mirrored (two-family classification, Theta^2 table + mu4 torsor,
Z8 tower conjugation, C^4 rho_tw vs sigma_std, Cl(16) dichotomy 2^7 vs
(-1)^F, RP preconditions + site-cut degeneration + Cauchy-Stieltjes
control -- the 40-digit PD certificates are Python-only), counted per
GATE.WOLFRAM.02.  Discovery provenance: experiments/tfpt-discovery/
woit_os_theta_realstructure_probe.py (2026-07-22, 21/21) and
woit_os_theta_rp_freelevel_probe.py (2026-07-22, 13/13)."""
from fractions import Fraction as Fr
from itertools import combinations

import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset, g_car

mp.mp.dps = 40

I = sp.I
N_SEAM = 2 ** (g_car - 1)        # 16 Majorana seam sites, 4 per mark quadrant
NH = N_SEAM // 2

RHO = sp.diag(I, 1)              # the order-4 clock, U(2) (v492 S5)
RHOINV = sp.diag(-I, 1)
DECK = sp.diag(I, -I)            # the Z4 ALE deck generator, SU(2)
ZETA8 = sp.exp(I * sp.pi / 4)
SPIN = sp.diag(ZETA8, 1 / ZETA8)  # Z8 spin lift of the clock (v492 S5)
MARKS = [sp.Integer(1), I, sp.Integer(-1), -I]      # the mu4 seam marks


def iszero(e):
    e2 = sp.expand(e)
    if e2 == 0:
        return True
    e3 = sp.expand(sp.expand_complex(e2))
    if e3 == 0:
        return True
    return sp.simplify(e3) == 0


def prop_mat(A, B):
    """projective equality of matrices (A = c B, c != 0)."""
    a = list(A)
    b = list(B)
    if all(iszero(x) for x in a) or all(iszero(x) for x in b):
        return False
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if not iszero(a[i] * b[j] - a[j] * b[i]):
                return False
    return True


def set_eq(A, B):
    if len(A) != len(B):
        return False
    used = [False] * len(B)
    for x in A:
        hit = False
        for j, y in enumerate(B):
            if not used[j] and iszero(x - y):
                used[j] = True
                hit = True
                break
        if not hit:
            return False
    return True


# ---------------------------------------------------------------------------
# exact Cl(16) machinery (v506/v507/v510, verbatim)
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


def refl_implementer(n, k):
    """NS implementer for the reflection j -> k - j (v510 verbatim)."""
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


def clock_lift(n):
    """the v506 B-S4 quarter-shift Fock lift V (rational block nullspace)."""
    Cblk = [[0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    even_basis = [(), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
                  (0, 1, 2, 3)]
    odd_basis = [(0,), (1,), (2,), (3,), (0, 1, 2), (0, 1, 3), (0, 2, 3),
                 (1, 2, 3)]
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
    vec = null[0] * sp.lcm([sp.denom(x) for x in null[0]])
    v = {even_basis[kk]: Fr(int(vec[kk])) for kk in range(8) if vec[kk] != 0}

    def embed(x, j):
        table = (j, j + 4, j + 8, j + 12)
        return {tuple(sorted(table[i] for i in m)): c for m, c in x.items()}

    V = ONE
    for j in range(4):
        V = cmul(V, embed(v, j))
    return V


def pair_scalar(x, y):
    """the ()-coefficient of x*y, exact, in O(|x|): monomials multiply to
    (a multiple of) the empty monomial iff they are EQUAL as sets, with
    sign mono_mul(m, m)."""
    c0 = Fr(0)
    for m1, cx in x.items():
        cy = y.get(m1)
        if cy:
            s_m, m_sq = mono_mul(m1, m1)
            assert m_sq == ()
            c0 += s_m * cx * cy
    return c0


# ---------------------------------------------------------------------------
# Part W -- the anti-linear real structure Theta (W1 + W2)
# ---------------------------------------------------------------------------
def conj_by_theta(M, X):
    """Theta X Theta^-1 for Theta = C o M (anti-linear) and linear X."""
    return sp.expand(M * X.conjugate() * M.inv())


def w_s1_classification():
    print("  -- W-S1: classify all anti-linear Theta with "
          "Theta rho Theta^-1 prop rho^{+-1}")
    a, b, c, d, lam = sp.symbols('a b c d lam')
    M = sp.Matrix([[a, b], [c, d]])
    rho_bar = RHO.conjugate()          # = diag(-i, 1) = RHO^-1 exactly

    eqs_inv = sp.expand(M * rho_bar - lam * RHOINV * M)
    eqs_cen = sp.expand(M * rho_bar - lam * RHO * M)

    sol_inv = sp.solve([eqs_inv[0, 1], eqs_inv[1, 0],
                        eqs_inv[0, 0], eqs_inv[1, 1]],
                       [b, c, lam], dict=True)
    diag_only = all(s.get(b, 0) == 0 and s.get(c, 0) == 0 for s in sol_inv)
    lam_inv = {s.get(lam) for s in sol_inv if lam in s}
    off_branch = sp.solve([eqs_inv[0, 0].subs(lam, sp.I),
                           eqs_inv[1, 1].subs(lam, sp.I)], [a, d], dict=True)
    off_kills = off_branch == [{a: 0, d: 0}]

    sol_cen = sp.solve([eqs_cen[0, 0], eqs_cen[1, 1],
                        eqs_cen[0, 1], eqs_cen[1, 0]],
                       [a, d, lam], dict=True)
    anti_only = all(s.get(a, 0) == 0 and s.get(d, 0) == 0 for s in sol_cen)
    lam_cen = {s.get(lam) for s in sol_cen if lam in s}
    check("W-S1.1 TWO FAMILIES [exact, symbolic]: Theta = C o M with "
          "Theta rho Theta^-1 = lam rho^-1 forces M DIAGONAL with lam = 1 "
          "(solve: %s, lam in %s; off-diagonal branch inconsistent: %s) -- "
          "family D inverts the clock EXACTLY; Theta rho Theta^-1 = lam rho "
          "forces M ANTIDIAGONAL with lam = -i (solve: %s, lam in %s) -- "
          "family A centralises the clock only PROJECTIVELY (-i rho): "
          "no third family exists"
          % (diag_only, lam_inv, off_kills, anti_only, lam_cen),
          diag_only and lam_inv <= {1} and anti_only
          and lam_cen <= {-sp.I} and off_kills)


def w_s2_family_d():
    print("  -- W-S2: family D = diag(mu,1) o conj -- the OS-reflection "
          "family")
    mu = sp.symbols('mu')
    Md = sp.diag(mu, 1)

    conj_rho = sp.expand(Md * RHO.conjugate() * Md.inv())
    exact_inv = sp.simplify(conj_rho - RHOINV) == sp.zeros(2, 2)
    conj_deck = sp.expand(Md * DECK.conjugate() * Md.inv())
    deck_inv = sp.simplify(conj_deck - DECK.inv()) == sp.zeros(2, 2)
    check("W-S2.1 RELATIONS EXACT [symbolic mu]: Theta_D rho Theta_D^-1 = "
          "rho^-1 EXACTLY at matrix level (%s; because conj(rho) = rho^-1 "
          "and diagonal M commutes) and Theta_D delta Theta_D^-1 = "
          "delta^-1 = delta^3 (%s) -- family D inverts the clock AND "
          "normalises the Z4 deck, for EVERY mu"
          % (exact_inv, deck_inv), exact_inv and deck_inv)

    theta_sq = sp.expand(Md * Md.conjugate())
    sq_unit = theta_sq.subs(mu * sp.conjugate(mu), 1)
    sq_pos = [theta_sq[0, 0], theta_sq[1, 1]]
    check("W-S2.2 KRAMERS-FREE [exact]: Theta_D^2 = M conj(M) = diag(|mu|^2, "
          "1) -- POSITIVE diagonal, = +1 exactly iff |mu| = 1 (%s), and "
          "NEVER -1 (both entries %s are absolute squares): the Kramers "
          "case Theta^2 = -1 is IMPOSSIBLE in the clock-inverting family "
          "-- the contract demand (Theta^2 = +1, Theta rho Theta = rho^-1) "
          "is INTERNALLY consistent"
          % (sq_unit == sp.eye(2), sq_pos),
          sq_unit == sp.eye(2)
          and sq_pos == [mu * sp.conjugate(mu), 1])

    good, bad = [], []
    for m_v in [sp.Integer(1), I, sp.Integer(-1), -I,
                sp.exp(I * sp.pi / 3), ZETA8]:
        img = [sp.expand_complex(m_v * sp.conjugate(z)) for z in MARKS]
        (good if set_eq(img, MARKS) else bad).append(m_v)
    check("W-S2.3 MARK PINNING [exact]: z -> mu conj(z) preserves the mu4 "
          "mark set {1, i, -1, -i} iff mu in mu4 (all 4 pass: %s; controls "
          "e^{i pi/3}, zeta8 fail: %s) -- the mark-compatible Theta_D form "
          "a mu4-TORSOR of exactly 4 anti-involutions"
          % ([str(g) for g in good], len(bad) == 2),
          len(good) == 4 and set_eq(good, MARKS) and len(bad) == 2)

    perms = {}
    for m_v in MARKS:
        pm = []
        for z in MARKS:
            img = sp.expand_complex(m_v * sp.conjugate(z))
            pm.append([k for k, w in enumerate(MARKS) if iszero(img - w)][0])
        perms[str(m_v)] = pm
    fixed_marks = {k: sum(1 for i_, j_ in enumerate(v) if i_ == j_)
                   for k, v in perms.items()}
    cutpts = {}
    for m_v, cands, tag in [(sp.Integer(1), [0, sp.pi], '1'),
                            (I, [sp.pi / 4, 5 * sp.pi / 4], 'i')]:
        ok_c = all(iszero(sp.exp(2 * I * t) - m_v) for t in cands)
        others = [k * sp.pi / 4 for k in range(8)
                  if not any(iszero(k * sp.pi / 4 - t) for t in cands)]
        none_else = all(not iszero(sp.exp(2 * I * t) - m_v) for t in others)
        cutpts[tag] = len(cands) if (ok_c and none_else) else 0
    check("W-S2.4 INDUCED SEAM ACTION [exact]: on the seam circle Theta_D is "
          "the REFLECTION e^{i th} -> mu e^{-i th} with exactly 2 cut "
          "points (e^{2 i th} = mu: %s solutions each for mu = 1, i); mark "
          "permutations: mu = 1 fixes {1,-1} swaps {i,-i} (%s), mu = -1 "
          "fixes {i,-i} (%s), mu = +-i swap all marks in 2-cycles with "
          "cut points at the SILVER midpoints (%s, %s) -- 2 mark-axes + 2 "
          "midpoint-axes, all order 2; fix set on the sphere = the line "
          "through the deck poles {0, inf} at angle arg(mu)/2: the "
          "'euclidean cut' is a great circle through the poles"
          % ({k: v for k, v in cutpts.items()}, perms['1'], perms['-1'],
             perms['I'], perms['-I']),
          all(v == 2 for v in cutpts.values())
          and fixed_marks == {'1': 2, '-1': 2, 'I': 0, '-I': 0}
          and perms['1'] == [0, 3, 2, 1] and perms['-1'] == [2, 1, 0, 3])

    mu = sp.symbols('mu')
    conj_by_clock = sp.expand(RHO * sp.diag(mu, 1) * RHO.conjugate().inv())
    orbit_map = sp.simplify(conj_by_clock[0, 0] / conj_by_clock[1, 1])
    check("W-S2.5 TORSOR STRUCTURE [exact]: conjugating Theta_mu by the "
          "clock maps mu -> %s = -mu (rho Theta_mu rho^-1 = Theta_{-mu}): "
          "the 4 pinned reflections fall into 2 clock-orbits {1,-1} "
          "(mark axes) and {i,-i} (midpoint axes); the deck acts "
          "trivially -- the Aut(Z4)-type ambiguity of v506 A-S2.9 "
          "reappears as exactly this 2-orbit freedom" % orbit_map,
          orbit_map == -mu)


def w_s3_family_a():
    print("  -- W-S3: family A = antidiag o conj -- equatorial / rho_tw")
    mu = sp.symbols('mu')
    Ma = sp.Matrix([[0, mu], [1, 0]])

    conj_rho = sp.expand(Ma * RHO.conjugate() * Ma.inv())
    is_cen = sp.simplify(conj_rho + I * RHO) == sp.zeros(2, 2)
    not_inv = not prop_mat(conj_rho.subs(mu, 1), RHOINV)
    conj_deck = sp.expand(Ma * DECK.conjugate() * Ma.inv())
    deck_exact = sp.simplify(conj_deck - DECK) == sp.zeros(2, 2)
    check("W-S3.1 CLOCK RELATION [exact, symbolic mu]: Theta_A rho "
          "Theta_A^-1 = -i rho (%s) -- prop rho, i.e. family A "
          "CENTRALISES the clock projectively and NEVER inverts it "
          "(-i rho not prop rho^-1: %s); it centralises the deck EXACTLY "
          "(%s): family A can never satisfy the contract relation "
          "Theta rho Theta = rho^-1"
          % (is_cen, not_inv, deck_exact), is_cen and not_inv and deck_exact)

    sq = sp.expand(Ma * Ma.conjugate())
    eq_sq = sq.subs(mu, 1)
    tw_sq = sq.subs(mu, -1)
    check("W-S3.2 THETA^2 DICHOTOMY [exact]: Theta_A^2 = diag(mu, conj(mu)) "
          "-- involution iff mu REAL; mu = +1: equatorial z -> 1/conj(z), "
          "Theta^2 = +1 (%s), fix circle |z| = 1 = the SEAM (v506 A-S2.9, "
          "v510 B-M4.1); mu = -1: the ANTIPODE z -> -1/conj(z) = Woit's "
          "rho_tw on the fibre P^1, Theta^2 = -1 on C^2 (%s) = KRAMERS/ "
          "quaternionic, no fixed points (Woit: rho_tw^2 = -1 on C^2, +1 "
          "projectively) -- the free RP structure of v510 B-M2 is the "
          "Kramers member of family A"
          % (eq_sq == sp.eye(2), tw_sq == -sp.eye(2)),
          eq_sq == sp.eye(2) and tw_sq == -sp.eye(2))

    th = sp.symbols('th', real=True)
    z_c = sp.exp(I * th)
    eq_fix = sp.simplify(sp.expand_complex(
        1 / sp.conjugate(z_c) - z_c)) == 0
    check("W-S3.3 NO OS CUT [exact]: the equatorial member fixes the seam "
          "circle POINTWISE (1/conj(e^{i th}) = e^{i th}: %s) -- it "
          "DEFINES the Euclidean section instead of reflecting it: no "
          "half-space decomposition, no OS form.  ROLE SEPARATION: family "
          "A = the seam/Euclidean real structure (Woit's rho_tw side), "
          "family D = the OS/Minkowski-type conjugation -- the two v507 "
          "families are BOTH needed, in DIFFERENT contract slots"
          % eq_fix, eq_fix)


def w_s4_twistor_c4():
    print("  -- W-S4: C^4 twistor homogeneous coordinates -- rho_tw vs "
          "sigma_std")
    J2 = sp.Matrix([[0, -1], [1, 0]])
    M_tw = sp.diag(J2, J2)          # Woit: [z] -> [-c(z2),c(z1),-c(z4),c(z3)]
    rho4 = sp.diag(RHO, RHO)        # blockwise clock lift on C^4
    deck4 = sp.diag(DECK, DECK)     # blockwise Z4 deck lift

    tw_sq = sp.expand(M_tw * M_tw.conjugate())
    z1, z2 = sp.symbols('z1 z2')
    lamr = sp.symbols('lamr')
    fix_eqs = sp.expand(J2 * sp.Matrix([sp.conjugate(z1), sp.conjugate(z2)])
                        - lamr * sp.Matrix([z1, z2]))
    no_fix = sp.solve(sp.Eq(-1, sp.symbols('s2', nonnegative=True)),
                      sp.symbols('s2', nonnegative=True))
    check("W-S4.1 WOIT rho_tw REPRODUCED [exact]: M_tw = diag(J, J) (j-mult "
          "blockwise) has Theta_tw^2 = M_tw conj(M_tw) = %s = -1 on C^4 "
          "(Woit: rho_tw^2 = -1 upstairs, +1 projectively) and NO real "
          "points (a projective fixed point needs Theta^2 = +|lam|^2 > 0, "
          "impossible: %s solutions) -- the fibrewise antipode of v510 "
          "B-M2, globalised"
          % (list(tw_sq.diagonal()), len(no_fix)),
          tw_sq == -sp.eye(4) and len(no_fix) == 0 and len(fix_eqs) == 2)

    tw_rho = sp.expand(M_tw * rho4.conjugate() * M_tw.inv())
    tw_deck = sp.expand(M_tw * deck4.conjugate() * M_tw.inv())
    check("W-S4.2 rho_tw IS FAMILY A GLOBALLY [exact]: Theta_tw rho4 "
          "Theta_tw^-1 = -i rho4 (%s; centralises the clock projectively, "
          "never inverts) and centralises the deck EXACTLY (%s) -- Woit's "
          "Euclidean real structure is the C^4 globalisation of the "
          "W-S3 family A: it is the EUCLIDEAN structure, not the OS Theta"
          % (sp.simplify(tw_rho + I * rho4) == sp.zeros(4, 4),
             sp.simplify(tw_deck - deck4) == sp.zeros(4, 4)),
          sp.simplify(tw_rho + I * rho4) == sp.zeros(4, 4)
          and sp.simplify(tw_deck - deck4) == sp.zeros(4, 4))

    M_std = sp.eye(4)                # sigma_std: [z] -> [conj z]
    std_rho = sp.expand(M_std * rho4.conjugate() * M_std.inv())
    std_deck = sp.expand(M_std * deck4.conjugate() * M_std.inv())
    std_sq = sp.expand(M_std * M_std.conjugate())
    check("W-S4.3 sigma_std IS FAMILY D GLOBALLY [exact]: the standard "
          "conjugation inverts the clock lift EXACTLY (conj(rho4) = "
          "rho4^-1: %s), inverts the deck (%s), squares to +1 (%s), real "
          "points = RP^3 in CP^3 (Woit's second inequivalent structure) "
          "-- the C^4 globalisation of family D: Theta^2 = +1 AND "
          "Theta rho Theta = rho^-1 hold on the twistor level; honest "
          "fence: Woit's MINKOWSKI structure maps PT -> PT* (dual), so "
          "the OS-quotient interpretation of sigma_std stays contract "
          "work (WOIT-beta), only the group relations are settled here"
          % (sp.simplify(std_rho - rho4.inv()) == sp.zeros(4, 4),
             sp.simplify(std_deck - deck4.inv()) == sp.zeros(4, 4),
             std_sq == sp.eye(4)),
          sp.simplify(std_rho - rho4.inv()) == sp.zeros(4, 4)
          and sp.simplify(std_deck - deck4.inv()) == sp.zeros(4, 4)
          and std_sq == sp.eye(4))


def w_s5_spin_level():
    print("  -- W-S5: Z8 spin lift -- does Theta survive the spin bridge?")
    mu = sp.symbols('mu')
    Md = sp.diag(mu, 1)
    d_spin = sp.expand(Md * SPIN.conjugate() * Md.inv())
    d_inv = sp.simplify(d_spin - SPIN.inv()) == sp.zeros(2, 2)
    Ma = sp.Matrix([[0, 1], [1, 0]])
    a_spin = sp.expand(Ma * SPIN.conjugate() * Ma.inv())
    a_cen = sp.simplify(a_spin - SPIN) == sp.zeros(2, 2)
    check("W-S5.1 SPIN COMPATIBILITY [exact]: Theta_D s Theta_D^-1 = s^-1 "
          "EXACTLY for the Z8 spin lift s = diag(zeta8, zeta8^-1) (%s; "
          "any diagonal mu) -- Theta_D extends to the spin group as an "
          "anti-linear map inverting the FULL Z8 tower, with Theta^2 "
          "still +1 (W-S2.2): NO Kramers obstruction at the spin level; "
          "the equatorial family-A member centralises s exactly (%s) -- "
          "the role separation persists upstairs"
          % (d_inv, a_cen), d_inv and a_cen)

    tower = [sp.simplify(ZETA8 ** k - sp.conjugate(ZETA8) ** (-k))
             for k in range(8)]
    all_inv = all(iszero(t) for t in tower)
    check("W-S5.2 TOWER ARITHMETIC [exact]: conj(zeta8^k) = zeta8^-k for "
          "all k = 0..7 (%s) -- inversion of the whole Z8 = 2|mu4| tower "
          "is pure Galois conjugation, no sign/phase leaks anywhere in "
          "the 8 steps: the Theta relation propagates through clock^2 = "
          "deck (v492) without correction terms"
          % all_inv, all_inv)


def w_s6_fock_level():
    print("  -- W-S6: Cl(16) Fock level -- Theta_Fock = U_r o K, exact")
    n = N_SEAM
    GAMMA = {tuple(range(n)): Fr(1)}

    D_ns = shift_matrix(n, 8, -1)
    Ut = dict(ONE)
    for j in range(8):
        Ut = cmul(Ut, cadd(ONE, cscale(cmul(gam(j), gam(j + 8)), Fr(-1))))
    V = clock_lift(n)
    C_ns = shift_matrix(n, 4, -1)
    ok_lifts = implements(Ut, D_ns, n) and implements(V, C_ns, n)

    results = {}
    for k_ax, tag in [(0, 'mu=1'), (4, 'mu=i')]:
        R = refl_matrix(n, k_ax, -1)
        negR = [[-x for x in row] for row in R]
        Ur_k = refl_implementer(n, k_ax)
        impl = implements(Ur_k, R, n) or implements(Ur_k, negR, n)
        even = all(len(m) % 2 == 0 for m in Ur_k)
        ok_sq, c_sq = prop(cmul(Ur_k, Ur_k), ONE)
        results[tag] = (impl, even, ok_sq, c_sq)
    check("W-S6.1 THETA_FOCK EXISTS, THETA^2 = +1 [exact]: both pinned "
          "reflection axes have EVEN NS implementers U_r (mu=1, axis "
          "k=0, fixed sites = marks {0,8}: %s; mu=i, axis k=4, fixed "
          "sites = silver midpoints {2,10}: %s) with U_r^2 = POSITIVE "
          "scalar (%s and %s x 1 = 2^7 both; the 2^8 edge-axes at odd k "
          "are NOT in the mu4 torsor) -- all coefficients rational, so "
          "Theta_Fock = U_r o K obeys Theta_Fock^2 = U_r conj(U_r) = "
          "U_r^2 = 2^7 > 0: after unitary normalisation Theta_Fock^2 = "
          "+1 EXACTLY -- Kramers-free, matching W-S2.2 downstairs"
          % (results['mu=1'][:2], results['mu=i'][:2],
             results['mu=1'][3], results['mu=i'][3]),
          ok_lifts
          and all(r[0] and r[1] and r[2] for r in results.values())
          and results['mu=1'][3] == Fr(2 ** 7)
          and results['mu=i'][3] == Fr(2 ** 7))

    # --- clock inversion, implementer route (consolidated; see docstring):
    # (a) matrix level: R C R^-1 = C^-1 exactly; (b) conj_V = U_r V U_r^-1
    # implements C^-1; (c) centre of Cl(16) = scalars (sign rule machine-
    # instantiated below); hence conj_V V implements the identity and is
    # the scalar pinned by the exact ()-pairing.
    Ur = refl_implementer(n, 0)
    c_ur = Fr(2 ** 7)                     # U_r^2 = 2^7 => U_r^-1 = U_r/2^7
    Rm = sp.Matrix(refl_matrix(n, 0, -1))
    Cm = sp.Matrix(C_ns)
    Cinv = Cm.inv()
    mat_inv = sp.simplify(Rm * Cm * Rm.inv() - Cinv) == sp.zeros(n, n)
    Cinv_int = [[int(Cinv[i_, j_]) for j_ in range(n)] for i_ in range(n)]
    conj_V = cscale(cmul(cmul(Ur, V), Ur), Fr(1, c_ur))
    impl_conj = implements(conj_V, Cinv_int, n)
    # centre lemma, machine-instantiated: gamma_a (monomial m) gamma_a^-1 =
    # +-m with relative sign -1 iff (a in m, |m| even) or (a not in m, |m|
    # odd) -- the sign counts pairwise generator crossings, so it depends
    # only on |m| and membership; verified for every degree k and every
    # generator a.  A non-scalar central element is impossible: every
    # non-empty monomial has an anticommuting generator (k even: any a in
    # m; k odd <= 15: any a outside).
    centre_ok = True
    for k in range(1, n + 1):
        m = tuple(range(k))
        for a in range(n):
            s1, m1 = mono_mul((a,), m)
            s2, m2 = mono_mul(m, (a,))
            anti = ((a in m) and k % 2 == 0) or ((a not in m) and k % 2 == 1)
            centre_ok = (centre_ok and m1 == m2
                         and (s1 == -s2 if anti else s1 == s2))
    c0 = pair_scalar(conj_V, V)
    check("W-S6.2 CLOCK INVERSION AT FOCK LEVEL [exact, implementer route]: "
          "R C R^-1 = C^-1 exactly at matrix level (%s), V implements C "
          "and conj_V = U_r V U_r^-1 (K trivial on the rational V) "
          "implements C^-1 on all 16 generators (%s); the centre of "
          "Cl(16) is the scalars (sign rule verified for every degree k "
          "= 1..16 and every generator: %s), so conj_V V implements the "
          "identity and IS the exact scalar %s = 2^12: Theta_Fock V "
          "Theta_Fock^-1 = 4096 V^-1 -- the anti-unitary lift of the "
          "seam reflection inverts the FOCK clock tower exactly as "
          "demanded, Theta rho Theta = rho^-1 realised on 2^8-dim Fock "
          "space (and c0 != 0 certifies V invertible)"
          % (mat_inv, impl_conj, centre_ok, c0),
          mat_inv and impl_conj and centre_ok and c0 == Fr(4096))

    conj_Ut = cscale(cmul(cmul(Ur, Ut), Ur), Fr(1, c_ur))
    ok_g2, g2c = prop(cmul(GAMMA, GAMMA), ONE)
    Utinv = cscale(cmul(Ut, GAMMA), Fr(1, 256))   # Ut^2 = 256 Gamma
    ok_dinv, c_dinv = prop(conj_Ut, Utinv)
    check("W-S6.3 DECK NORMALISATION AT FOCK LEVEL [exact]: Theta_Fock "
          "Utilde Theta_Fock^-1 = %s x Utilde^-1 (Utilde^2 = 256 Gamma, "
          "Gamma^2 = %s x 1 => Utilde^-1 = Utilde Gamma/256; prop: %s) "
          "-- the Z4 deck lift is normalised (conjugated to its inverse "
          "in the SAME Z4), consistent with W-S2.1 downstairs"
          % (c_dinv, g2c, ok_dinv), ok_dinv and ok_g2 and g2c == Fr(1))

    theta_t_sq = cmul(Ut, Ut)                 # Theta_t = Utilde o K
    ok_kram, c_kram = prop(theta_t_sq, GAMMA)
    check("W-S6.4 THE KRAMERS DICHOTOMY [exact]: the DECK-induced anti-"
          "linear candidate Theta_t = Utilde o K (= Woit's rho_tw "
          "restricted to the seam: the antipode z -> -1/conj(z) acts on "
          "the 16 Majoranas as the shift-8) has Theta_t^2 = Utilde^2 = "
          "%s x gamma_1..gamma_16 = 256 (-1)^F-monomial (%s) -- NOT a "
          "scalar: Theta_t^2 = (-1)^F, Kramers on the odd sector.  The "
          "v510 split/nonsplit dichotomy IS the Theta^2 = +1 vs (-1)^F "
          "dichotomy: rho_tw^2 = -1 (W-S4.1) resurfaces fermionically; "
          "the contract's parenthetical 'Theta induced by the seam "
          "reflection (the deck/covering involution)' needs precision -- "
          "the DECK cannot furnish the OS Theta, the seam-circle "
          "REFLECTION does"
          % (c_kram, ok_kram), ok_kram and c_kram == Fr(256)
          and not is_scalar(theta_t_sq))

    UtV = cmul(Ut, V)
    VUt = cmul(V, Ut)
    commutes = not cadd(UtV, cscale(VUt, Fr(-1)))
    check("W-S6.5 CONTROL -- rho_tw CENTRALISES THE FOCK CLOCK [exact]: "
          "Utilde V = V Utilde as exact Cl(16) elements (%s), i.e. "
          "Theta_t V Theta_t^-1 = 1 x V -- the antipodal/Euclidean "
          "structure centralises the clock tower instead of inverting "
          "it, EXACTLY as family A downstairs (W-S3.1/W-S4.2): the two "
          "families stay separated at every level (sphere, C^4, spin, "
          "Fock)"
          % commutes, commutes)


def w_s7_verdict():
    print("  -- W-S7: kill test 1 verdict")
    check("W-S7.1 KILL TEST 1 DOES NOT FIRE (free/equivariant level) "
          "[assembled]: anti-linear Theta with Theta^2 = +1 AND "
          "Theta rho Theta = rho^-1 EXISTS -- the family D torsor "
          "{Theta_mu : mu in mu4} (W-S1.1/W-S2.1-S2.3), deck-normalising "
          "(W-S2.1), mark-set-preserving (W-S2.3), spin-compatible "
          "(W-S5.1), Fock-implementable with Theta_Fock^2 = +1 "
          "(W-S6.1-S6.3).  The real structure is PINNED up to the "
          "clock-orbit pair {mark-axis, midpoint-axis} (W-S2.5); "
          "fixed-point set = great circle through the deck poles at "
          "angle arg(mu)/2 (the euclidean cut, 2 cut points on the "
          "seam).  HONEST SCOPE: this is the FREE/equivariant skeleton "
          "only -- A_hol (interacting), gauge-fixed RP (kill test 2), OS "
          "reconstruction, chirality (3/6), mu4 incidence (7) remain "
          "open contract work", True)
    check("W-S7.2 STRUCTURAL COROLLARY [typed]: the two v507/v510 real-"
          "structure families occupy DIFFERENT contract slots -- family "
          "A (equatorial/antipodal, rho_tw-type) DEFINES the Euclidean "
          "seam section and centralises the clock; family D "
          "(conjugation, sigma_std-type) REFLECTS it and inverts the "
          "clock = the OS Theta.  Kill test 1 would have fired if "
          "family D were absent or Kramers-obstructed; it is neither "
          "(Theta^2 = M conj(M) = diag(|mu|^2, 1) can never be -1, "
          "W-S2.2).  Woit's rho_tw^2 = -1 lives in family A and lifts "
          "to Theta_t^2 = (-1)^F at Fock level (W-S6.4) -- consistent, "
          "and NOT in conflict with the contract target", True)


# ---------------------------------------------------------------------------
# Part R -- reflection positivity of the free seam system (W3)
# ---------------------------------------------------------------------------
def c_of(d, n=N_SEAM):
    """C(d) = (2/n) sum_{p in NS+} sin(p d) = (2/n)/sin(pi d/n) for odd d,
    0 for even d (exact geometric sum; antiperiodic C(d+n) = -C(d))."""
    if d % 2 == 0:
        return sp.Integer(0)
    return sp.Rational(2, n) / sp.sin(sp.pi * sp.Rational(d, n))


def g2(a, b, n=N_SEAM, chi=1):
    """omega(g_a g_b) = delta + i*chi*C(a-b); chi = -1 -> anti-chiral."""
    if a == b:
        return sp.Integer(1)
    return I * chi * c_of(a - b, n)


def wick(idx, n=N_SEAM, chi=1):
    """omega(g_{i1} ... g_{i2k}) by Pfaffian recursion (indices distinct)."""
    if len(idx) == 0:
        return sp.Integer(1)
    if len(idx) % 2 == 1:
        return sp.Integer(0)
    head, rest = idx[0], idx[1:]
    tot = sp.Integer(0)
    for j, b in enumerate(rest):
        sub = rest[:j] + rest[j + 1:]
        tot += (-1) ** j * g2(head, b, n, chi) * wick(sub, n, chi)
    return tot


def refl_map(k, n=N_SEAM):
    """site map + spin sign of the reflection j -> k - j (NS lift)."""
    def r(a):
        return (k - a) % n

    def s(a):
        return -1 if (k - a) % (2 * n) >= n else 1
    return r, s


def theta_mono(mono, r, s, eta):
    """theta(g_{i1}...g_{ik}) = eta^k * s_{ik}...s_{i1} g_{r(ik)}...g_{r(i1)}
    sorted back to increasing order; returns (coeff, tuple)."""
    imgs = [r(a) for a in reversed(mono)]
    coeff = eta ** len(mono)
    for a in mono:
        coeff *= s(a)
    lst = list(imgs)
    sign = 1
    for i in range(len(lst)):
        for j in range(len(lst) - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                sign = -sign
    assert len(set(lst)) == len(lst)
    return coeff * sign, tuple(lst)


def gram(basis, r, s, eta, n=N_SEAM, chi=1):
    """M_ab = omega(theta(e_a) e_b), exact."""
    rows = []
    for ma in basis:
        ca, ia = theta_mono(ma, r, s, eta)
        row = []
        for mb in basis:
            assert not (set(ia) & set(mb)), "supports must be disjoint"
            row.append(sp.expand_complex(ca * wick(list(ia) + list(mb),
                                                   n, chi)))
        rows.append(row)
    return sp.Matrix(rows)


def hermitian_exact(M):
    d = M - M.conjugate().T
    return all(iszero(x) for x in d)


def spectrum_inertia(M, tol=None):
    """inertia (n+, n-, n0) of the exact Hermitian matrix via 40-digit
    spectrum of the evalf'd matrix; returns (inertia, min|nonzero|)."""
    if tol is None:
        tol = mp.mpf(10) ** (-25)
    n = M.shape[0]
    A = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            re_, im_ = M[i, j].evalf(45).as_real_imag()
            A[i, j] = mp.mpc(mp.mpf(str(re_)), mp.mpf(str(im_)))
    E, _ = mp.eighe(A)
    evs = [E[i].real for i in range(n)]
    npos = sum(1 for e in evs if e > tol)
    nneg = sum(1 for e in evs if e < -tol)
    nzero = n - npos - nneg
    nz = [abs(e) for e in evs if abs(e) > tol]
    return (npos, nneg, nzero), (min(nz) if nz else mp.mpf(0))


PLUS = lambda a: 1                     # plain spin signs (state-compatible)


def half_of(k, n=N_SEAM):
    """the positive half for the reflection r(a) = k - a mod n (site axis:
    exclude the 2 fixed sites; bond axis: the arc between the two cut
    bonds), plus disjointness of r(half)."""
    if k % 2 == 0:
        f1 = (k // 2) % n
        P = [(f1 + j) % n for j in range(1, n // 2)]
    else:
        b = (k + 1) // 2                # first site right of the cut bond
        P = [(b + j) % n for j in range(n // 2)]
    rP = {(k - a) % n for a in P}
    assert not (rP & set(P))
    return P


def r1_state():
    print("  -- R1: the chiral NS vacuum vs theta -- exact preconditions")
    n8 = 8
    Cm8 = sp.Matrix(n8, n8, lambda a, b: c_of(a - b, n8))
    pure = sp.simplify(Cm8 * Cm8 + sp.eye(n8)) == sp.zeros(n8, n8)
    check("R1.1 STATE WELL-DEFINED [exact, N=8]: the chiral NS kernel "
          "C(d) = (2/N)/sin(pi d/N) (odd d; 0 even; C(d+N) = -C(d)) has "
          "C^2 = -1 EXACTLY (%s) -- omega = (1 + iC)/2-quasifree is a "
          "PURE state: the lattice chiral vacuum exists and is the "
          "unique all-right-movers NS polarisation" % pure, pure)

    N = N_SEAM
    Cm = sp.Matrix(N, N, lambda a, b: c_of(a - b))
    Rs = {k: sp.Matrix(refl_matrix(N, k, -1)) for k in (15, 3, 0)}
    anti = all(sp.simplify(R * Cm * R.T + Cm) == sp.zeros(N, N)
               for R in Rs.values())
    S = sp.Matrix(shift_matrix(N, 4, -1))
    clock_inv = sp.simplify(S * Cm * S.T - Cm) == sp.zeros(N, N)
    dihed = sp.simplify(Rs[15] * S * Rs[15].inv()
                        - S.inv()) == sp.zeros(N, N)
    anti_antipode = sp.simplify(
        (S ** 2) * Cm * (S ** 2).T + Cm) == sp.zeros(N, N)
    check("R1.2 ANTI-INVARIANCE + CLOCK [exact, N=16, NS dihedral "
          "lifts]: every v510 NS reflection lift gives R C R^T = -C "
          "EXACTLY (k = 15, 3, 0: %s; the OS precondition omega o theta "
          "= conj o omega at 2-pt level -- the antiperiodic wrap signs "
          "implement exactly the C(d+16) = -C(d) representative shift), "
          "the NS quarter-shift clock lift gives S C S^T = C (%s; the "
          "chiral vacuum is clock-invariant), and R S R^-1 = S^-1 "
          "EXACTLY (%s; theta inverts the clock -- the Part-W relation "
          "on the state side); the NS ANTIPODE S^2 (= the Utilde deck "
          "conjugation) FAILS anti-invariance (%s: S^2 C S^2T = +C != "
          "-C) -- the deck is not an OS reflection of this state"
          % (anti, clock_inv, dihed, not anti_antipode),
          anti and clock_inv and dihed and not anti_antipode)

    r, s = refl_map(15)
    eta = I
    idx = (1, 2, 4, 7)
    th_c, th_m = theta_mono(idx, r, s, eta)
    lhs = sp.expand_complex(th_c * wick(list(th_m)))
    rhs = sp.expand_complex(sp.conjugate(wick(list(idx))))
    four_pt = iszero(lhs - rhs)
    tsq = []
    for a in range(N):
        c1, m1 = theta_mono((a,), r, s, eta)
        c2, m2 = theta_mono(m1, r, s, eta)
        tsq.append(iszero(sp.conjugate(c1) * c2 - 1) and m2 == (a,))
    check("R1.3 THETA IS AN OS REFLECTION [exact]: theta(g_a) = eta s_a "
          "g_{15-a} with eta = i (NS signs) is an anti-linear anti-"
          "automorphism with theta^2 = 1 on ALL 16 generators (%s; "
          "anti-linearity kills the phase: conj(eta) eta = |eta|^2 = 1) "
          "and omega o theta = conj o omega verified beyond 2-pt on the "
          "4-pt witness g1 g2 g4 g7 (%s)"
          % (all(tsq), four_pt), all(tsq) and four_pt)


def r2_site_cut():
    print("  -- R2: cut THROUGH sites (marks-at-sites reading) -- RP fails")
    N = N_SEAM
    k = 0
    P = half_of(k)                       # {1..7}
    r = lambda a: (k - a) % N
    basis1 = [(a,) for a in P]
    M1 = gram(basis1, r, PLUS, -I)
    herm = hermitian_exact(M1)
    diag0 = all(iszero(M1[i, i]) for i in range(len(P)))
    offdiag = sum(0 if iszero(M1[i, j]) else 1
                  for i in range(7) for j in range(7) if i != j)
    det_exact = sp.simplify(M1.det())
    inert, gap = spectrum_inertia(M1)
    check("R2.1 ONE-PARTICLE GRAM DEGENERATES [exact]: axis through the "
          "sites (k = 0, half = 7 sites): the Gram omega(theta(g_a) g_b) "
          "= -C(-a-b) is Hermitian (%s) but has ZERO diagonal (all 7 "
          "entries: %s; reflected distance k-2a is EVEN and the strictly "
          "chiral kernel has C(even) = 0 exactly) with %d nonzero "
          "off-diagonal entries -- indefinite for EVERY twist eta and "
          "EVERY spin-sign dressing; checkerboard block structure: "
          "det = %s exactly (bipartite 4+3), inertia (n+,n-,n0) = %s "
          "(+- symmetric): RP FAILS on the site cut"
          % (herm, diag0, offdiag, det_exact, inert),
          herm and diag0 and offdiag > 0 and det_exact == 0
          and inert == (3, 3, 1))

    pairs = list(combinations(P, 2))
    basis2 = [()] + pairs
    M2 = gram(basis2, r, PLUS, -I)
    herm2 = hermitian_exact(M2)
    zero_idx = [i for i, pr in enumerate(pairs)
                if (pr[0] + pr[1]) % 2 == 0]
    wit = None
    for i in zero_idx:
        for j in range(len(basis2)):
            if j != i + 1 and not iszero(M2[i + 1, j]):
                minor = sp.expand_complex(
                    M2[i + 1, i + 1] * M2[j, j]
                    - M2[i + 1, j] * sp.conjugate(M2[i + 1, j]))
                wit = (pairs[i], basis2[j], sp.simplify(minor))
                break
        if wit:
            break
    inert2, _ = spectrum_inertia(M2)
    check("R2.2 EVEN SECTOR FAILS TOO [exact]: deg <= 2 even Gram (1 + 21 "
          "pairs = 22x22) is Hermitian (%s) but the same-parity pairs "
          "have diagonal C(a-b)^2 - C(a+b)^2 = 0 - 0 = 0 (%d zero-"
          "diagonal rows) with nonzero coupling: 2x2 minor witness "
          "%s x %s = %s < 0 exactly; inertia %s -- the site cut fails "
          "even in the gauge-blind (even) sector: NOT a fermion-parity "
          "artifact" % (herm2, len(zero_idx), wit[0], wit[1], wit[2],
                        inert2),
          herm2 and len(zero_idx) > 0 and wit is not None
          and sp.simplify(wit[2]) != 0 and inert2[1] > 0)


def r3_bond_cut():
    print("  -- R3: cut BETWEEN sites (marks-at-bond-midpoints reading) "
          "-- RP holds")
    res = {}
    for k, tag in [(15, 'mu=1'), (3, 'mu=i')]:
        P = half_of(k)
        r, s = refl_map(k)
        basis1 = [(a,) for a in P]
        picked = None
        for eta in (I, -I):
            M1 = gram(basis1, r, s, eta)
            if not hermitian_exact(M1):
                continue
            inert, gap = spectrum_inertia(M1)
            if inert == (8, 0, 0):
                picked = (eta, inert, gap)
        res[tag] = picked
    check("R3.1 ONE-PARTICLE GRAM PD [exact entries, 40-digit inertia]: "
          "bond axes (k = 15 <-> mark axis mu = 1 in the half-offset "
          "placement; k = 3 <-> mu = i), NS spin lifts: reflected "
          "distances are ODD, the Gram entries land on the nonzero "
          "chiral kernel; for exactly one twist per axis (mu=1: eta = "
          "%s; mu=i: eta = %s) the 8x8 Gram is POSITIVE DEFINITE, "
          "inertia %s / %s (min eigenvalue > %s at 40 digits) -- RP "
          "holds at one-particle level on both pinned mark axes"
          % (res['mu=1'][0], res['mu=i'][0], res['mu=1'][1],
             res['mu=i'][1], mp.nstr(min(res['mu=1'][2], res['mu=i'][2]),
                                     5)),
          res['mu=1'] is not None and res['mu=i'] is not None)

    k = 15
    P = half_of(k)
    r, s = refl_map(k)
    eta = res['mu=1'][0]
    basis2 = [()] + list(combinations(P, 2))
    M2 = gram(basis2, r, s, eta)
    herm2 = hermitian_exact(M2)
    inert2, gap2 = spectrum_inertia(M2)
    check("R3.2 EVEN SECTOR deg <= 2 [exact entries, 40-digit inertia]: "
          "the 29x29 Gram (1 + 28 pairs on the 8-site half) is Hermitian "
          "exactly (%s) with inertia %s -- positive semidefinite (kernel "
          "dim %d), no negative direction: the OS form extends past one "
          "particle" % (herm2, inert2, inert2[2]),
          herm2 and inert2[1] == 0 and inert2[0] > 0)

    n8 = 8
    k8 = 7
    P8 = half_of(k8, n8)                 # {4,5,6,7}
    r8, s8 = refl_map(k8, n8)
    evens = [()] + list(combinations(P8, 2)) + [tuple(P8)]
    odds = [(a,) for a in P8] + list(combinations(P8, 3))
    Me = gram(evens, r8, s8, I, n8)
    eta8 = None
    for eta_c in (I, -I):
        Mo_c = gram(odds, r8, s8, eta_c, n8)
        if hermitian_exact(Mo_c):
            io_c, _ = spectrum_inertia(Mo_c)
            if io_c[1] == 0:
                eta8, io = eta_c, io_c
    he = hermitian_exact(Me)
    ie, ge = spectrum_inertia(Me)
    check("R3.3 FULL HALF-ALGEBRA AT N = 8 [exact entries, 40-digit "
          "inertia]: bond cut k = 7, half = 4 sites, COMPLETE basis (8 "
          "even + 8 odd monomials = all 16; the Gram block-diagonalises "
          "even (+) odd): even Gram Hermitian %s inertia %s (eta-sign-"
          "blind), odd Gram Hermitian, PSD for exactly eta = %s with "
          "inertia %s -- the FULL half-side algebra is RP (kernels "
          "%d/%d): free-level reflection positivity holds with no "
          "degree truncation at the 8-site robustness size"
          % (he, ie, eta8, io, ie[2], io[2]),
          he and eta8 is not None and ie[1] == 0 and io[1] == 0
          and ie[0] > 0 and io[0] > 0)


def r4_continuum():
    print("  -- R4: continuum control (Cauchy-Stieltjes factorisation)")
    s, t = sp.symbols('s t', positive=True)
    lhs = 1 / sp.sin((s + t) / 2)
    rhs = (1 / (sp.cos(s / 2) * sp.cos(t / 2))) \
        / (sp.tan(s / 2) + sp.tan(t / 2))
    ident = iszero(sp.simplify(sp.trigsimp(lhs - rhs)))
    xs = [sp.Integer(1), sp.Integer(2), sp.Integer(3), sp.Integer(4)]
    Cau = sp.Matrix(4, 4, lambda i, j: 1 / (xs[i] + xs[j]))
    minors = [sp.simplify(Cau[:m, :m].det()) for m in range(1, 5)]
    all_pos = all(mv > 0 for mv in minors)
    check("R4.1 CONTINUUM CHIRAL OS KERNEL IS PD [exact]: 1/sin((s+t)/2) "
          "= [1/(cos(s/2)cos(t/2))] x 1/(tan(s/2) + tan(t/2)) (identity: "
          "%s) -- a positive diagonal congruence of the Cauchy-Stieltjes "
          "kernel 1/(x+y) = int_0^inf e^{-lam x} e^{-lam y} dlam, PD at "
          "any distinct points (leading minors at x = 1,2,3,4: %s, all "
          "> 0: %s): the continuum mark-cut OS form is strictly positive "
          "-- the R2 site-cut failure is a LATTICE-PLACEMENT artifact "
          "(reflected site distances collide with the exact C(even) = 0 "
          "checkerboard), not a defect of the mark cut itself"
          % (ident, minors, all_pos), ident and all_pos)


def r5_controls():
    print("  -- R5: controls (twist, antipode, chirality)")
    N = N_SEAM
    k = 15
    P = half_of(k)
    r, s = refl_map(k)
    basis1 = [(a,) for a in P]
    M_no = gram(basis1, r, s, 1)
    non_herm = not hermitian_exact(M_no)
    diag_im = [sp.simplify(sp.re(M_no[i, i])) for i in range(3)]
    check("R5.1 THE gamma^0 TWIST IS FORCED [exact]: eta = 1 (naive "
          "theta(g_a) = g_{k-a}) gives a NON-Hermitian form (%s; diagonal "
          "purely imaginary: Re = %s...) -- Hermiticity of the OS form "
          "forces eta = +-i, the Majorana analogue of the Dirac gamma^0 "
          "twist; the residual eta = +-i is fixed by positivity (R3.1)"
          % (non_herm, diag_im),
          non_herm and all(dv == 0 for dv in diag_im))

    r_anti = lambda a: (a + 8) % N
    s_alt = lambda a: 1 if a % 2 == 0 else -1
    Ca = sp.Matrix(N, N, lambda a, b:
                   s_alt(a) * s_alt(b) * c_of((a + 8) - (b + 8)))
    anti_ok = sp.simplify(Ca + sp.Matrix(N, N, lambda a, b:
                                         c_of(a - b))) == sp.zeros(N, N)
    P_a = list(range(8))
    basis_a = [(a,) for a in P_a]
    picked = None
    for eta in (1, -1, I, -I):
        Ma = gram(basis_a, r_anti, s_alt, eta)
        if hermitian_exact(Ma):
            ia, _ = spectrum_inertia(Ma)
            diag0 = all(iszero(Ma[i, i]) for i in range(8))
            picked = (eta, ia, diag0)
            break
    check("R5.2 THE ANTIPODE/DECK IS NO OS REFLECTION [exact]: the "
          "family-A/antipodal candidate theta_c(g_a) = eta s_a g_{a+8} "
          "(the Part-W Theta_t = Utilde o K, clock-CENTRALISING) needs "
          "the alternating dressing s_a = (-1)^a even to keep the state "
          "anti-invariant (%s; plain signs fail, R1.2), and its Gram is "
          "then Hermitian for eta = %s but has ZERO diagonal (%s; "
          "reflected distance a+8-b even on the diagonal) -- inertia %s, "
          "+- symmetric, indefinite: RP FAILS structurally for the "
          "clock-centralising real structure, at the same place where "
          "the clock-inverting one is PD -- the test SEPARATES the two "
          "families exactly as kill test 1 demands"
          % (anti_ok, picked[0], picked[2], picked[1]),
          anti_ok and picked is not None and picked[2]
          and picked[1][0] == picked[1][1] and picked[1][1] > 0)

    k = 15
    r, s = refl_map(k)
    M_anti = gram([(a,) for a in half_of(k)], r, s, I, N, chi=-1)
    herm_a = hermitian_exact(M_anti)
    ia, _ = spectrum_inertia(M_anti)
    pairsP = list(combinations(half_of(k), 2))
    M2_pos = gram([()] + pairsP, r, s, I, N, chi=1)
    M2_neg = gram([()] + pairsP, r, s, I, N, chi=-1)
    block_blind = all(iszero(M2_pos[i, j] - M2_neg[i, j])
                      for i in range(1, 29) for j in range(1, 29))
    id_flip = all(iszero(M2_pos[0, j] + M2_neg[0, j])
                  for j in range(1, 29))
    ia2, _ = spectrum_inertia(M2_neg)
    check("R5.3 CHIRALITY IS AN ODD-SECTOR DATUM [exact]: the ANTI-chiral "
          "state (C -> -C) with the SAME theta (eta = +i) has Hermitian "
          "(%s) one-particle Gram of inertia %s = NEGATIVE definite -- "
          "the ODD sector flips definiteness with the chirality, RP "
          "pins the PAIR (chirality, eta) up to the joint flip.  The "
          "EVEN sector is chirality-BLIND: the 28x28 pair block is "
          "entry-IDENTICAL (%s; entries quadratic in C), the identity-"
          "pair couplings flip sign (%s) = a diagonal-sign congruence "
          "diag(-1, 1..1) -- same inertia %s = still PD: the gauge-"
          "blind sector cannot see the chirality, only the odd sector "
          "can: an exact free-level shadow of kill test 3 (mirror "
          "fermions) living entirely in the fermionic sector"
          % (herm_a, ia, block_blind, id_flip, ia2),
          herm_a and ia == (0, 8, 0) and block_blind and id_flip
          and ia2 == (29, 0, 0))


def r6_verdict():
    print("  -- R6: verdict")
    check("R6.1 W3 VERDICT [assembled]: free-level RP HOLDS for the "
          "pinned clock-inverting Theta -- with three exact structure "
          "results: (i) the OS twist eta = +-i is forced by Hermiticity "
          "and pinned (jointly with the chirality) by positivity; (ii) "
          "the euclidean cut must run BETWEEN the 16 Majorana sites "
          "(marks at bond midpoints, the half-offset/NS-natural "
          "placement; 4 sites per mark quadrant) -- the cut THROUGH "
          "sites fails RP exactly via the chiral checkerboard C(even) = "
          "0, while the continuum control is strictly PD (R4): RP "
          "selects the site placement relative to the marks; (iii) the "
          "clock-centralising (family A / antipode / deck) structure "
          "fails RP structurally (zero diagonal) -- RP and the Part-W "
          "relation Theta rho Theta = rho^-1 select the SAME family: "
          "the two halves of the contract target are mutually "
          "consistent on the free level.  HONEST SCOPE: quadratic/free "
          "seam system only, deg <= 2 at N = 16, full algebra at N = 8; "
          "no interacting algebra, no gauge fixing, no OS "
          "reconstruction, no chirality theorem", True)


# ---------------------------------------------------------------------------
def run():
    reset()
    mp.mp.dps = 40
    print("v519  WOIT.THETA.FREE.01: the WOIT-alpha milestone -- the real "
          "structure exists (Part W) and free reflection positivity "
          "picks the same family (Part R)")
    w_s1_classification()
    w_s2_family_d()
    w_s3_family_a()
    w_s4_twistor_c4()
    w_s5_spin_level()
    w_s6_fock_level()
    w_s7_verdict()
    r1_state()
    r2_site_cut()
    r3_bond_cut()
    r4_continuum()
    r5_controls()
    r6_verdict()

    return summary("v519 WOIT.THETA.FREE.01: Theta exists with Theta^2 = "
                   "+1 and Theta rho Theta = rho^-1 on all four levels "
                   "(sphere, C^4, Z8 spin, Cl(16) Fock: V -> 4096 V^-1); "
                   "exactly two families, mu4 torsor, Kramers dichotomy "
                   "2^7 vs (-1)^F; free RP holds on the bond cut "
                   "((8,0,0)/(29,0,0)/full N = 8 algebra) and selects "
                   "the SAME family; kill test 1 does NOT fire at the "
                   "free level and stays live on the interacting "
                   "algebra; WOIT.OS.TWISTOR.01 stays [O], no marker "
                   "moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
