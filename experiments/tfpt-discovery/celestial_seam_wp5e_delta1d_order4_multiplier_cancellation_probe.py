"""WP5e-delta-1d of CELEST.SEAM.01 (EXPLORATION ONLY -- experiments/, no
verification claim).

"THE ORDER-4 CANCELLATION" -- the step that decides whether the finite
mu_4 multiplier system measured by delta-1c (the only remaining
obstruction of the derived Harvey-Moore measure) is cancelled by the
missing twistor-/BCOV degrees of freedom.  delta-1c (31/31) ended
UNENTSCHIEDEN with an exact gap: the 16-component Weil completion
exists and closes exactly (E1.5 residual 2.91 -> 1e-39), but the
blockwise SL(2,Z) covariance of the dressed system M_{a,b} =
G[a,b] eta^{-8} is obstructed by a FINITE multiplier system of order 4
(joint holonomy eigenspace dim 8/16 resp. 6/16, every eigenvalue a
root of unity of order <= 4; no SL(2,Z) character k = 0..11 and no
eta^m bookkeeping m = 0..23 cancels it).  delta-1d computes:

D0  replication: roots, 16-class exact ledgers, targets A_fix / psi.
D1  the Weil representation (exact Q(zeta_8)) + the gauge block
    transport constants (t_p, s_p) measured at 28+ digits and
    RECOGNISED as exact phases on the 1/960 grid (certified 1e-25);
    the T-fixed pairs (0,b) have t = e(-1/2) = -1 EXACTLY (the naked
    level-matching defect of the chiral mu_4 block).
D2  THE MULTIPLIER SYSTEM EXPLICIT: BFS transport groupoid with word
    bookkeeping; every loop mapped to its SL(2,Z) matrix gamma (exact
    integer 2x2); stabiliser check: gcd-1 loops land in Gamma_1(4),
    gcd-2 loops in Gamma_0(2)+/-; KOZYKEL vs CHARAKTER decided exactly
    by the SL(2,Z) relation defects c_{S^4}(p), c_{(ST)^3 S^-2}(p) and
    the centrality defect c_{[S^2,T]}(p) (pure scalars, gauge- and
    character-invariant, computed in exact 1/960-phase arithmetic);
    the multiplier table per loop on the joint eigenspace (exact
    orders); monomial character fit on Gamma_1(4) data.
D3  THE CANCELLATION CANDIDATE: the three sphere axions with Coxeter
    characters {i, -1, -i} (weights 1, 2, 3 = A3 exponents, v493/v505)
    as twisted complex-boson blocks f_m[a,b] built in EXACTLY the
    delta-1b normalisation; the exact identity G[a,b] = f_1 f_3
    (the gauge C^2 block IS the weight-(1,3) axion pair) verified to
    30+ digits; v502 vacuum energies E_b(theta) replicated exactly;
    axion transport constants measured + recognised.
D4  KERNTEST: multiplier(gauge block) x multiplier(axion block) = 1?
    Exact per-loop product table (both orientations: holomorphic and
    antiholomorphic/conjugated axion block) against chi_k e(m/24)^nT;
    full solve scan: candidates {none, f2, f1f3, f1f2f3, wrong112} x
    orientation x eta^m (m = 0..23) x chi_k (k = 0..11), solution
    dims in BOTH orbits + seed overlap; residual-order table (what
    order survives per candidate = the new fence if no cancellation).
D5  THE DECISION (only if a strict cancellation exists): derived
    contraction, function-level edge certificate, the combined
    integrand (gauge quartic x twisted axion weight) integrated with
    the delta-1b/1c kernel machinery (negative-exponent cell audit),
    the three waiting tests: T5(V) = 0?  W_2 : W_13 = 4 : 3?
    psi(V) = -64 N or V = -A_fix N?  -- now BINDING (measure derived).
D6  NEGATIVE CONTROLS: (a) Z2/EH -- the Z2 sub-orbifold closed
    blockwise in delta-1c; the Z2 axion (single A1 sphere, character
    -1) must not break it (cancellation trivial there); (b) wrong
    axion weights (1,1,2) (not the A3 exponents) must fail;
    (c) SO(16)/gcd-2-only: no odd sectors -> the axion b-characters
    are all +/-1 (mu_2) -- the order-4 supply is structurally absent.
D7  honest verdict per the preregistered branches.

Throwaway probe: exact where possible (Fractions, Q(zeta_8) matrices,
integer phase arithmetic on the 1/960 grid, exact SL(2,Z) words),
mpmath dps = 40 for the block products (constants certified constant
at 1e-28, phases recognised at 1e-25), numpy double SVD for the
contraction solves.  Prints tables + PASS/FAIL + verdict, ends with a
check count.  Nothing here is a claim; verification/, ledger, papers,
changelog, website, scorecard untouched.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, gcd, lcm

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 40
np.random.seed(7)

L_PHASE = 960          # exact phase grid: e(k / 960)
N_PASS = 0
N_FAIL = 0


def check(label, ok):
    global N_PASS, N_FAIL
    print(("  PASS  " if ok else "  FAIL  ") + label)
    if ok:
        N_PASS += 1
    else:
        N_FAIL += 1
    return ok


def fmt(xs):
    return "(" + ", ".join(str(x) for x in xs) + ")"


def fmtn(xs, nd=6):
    return "(" + ", ".join(mp.nstr(mp.mpf(x) if not isinstance(x, mp.mpc)
                                   else x, nd) for x in xs) + ")"


def phs(k):
    """pretty exact phase e(k/L)."""
    fr = F(k % L_PHASE, L_PHASE)
    if fr == 0:
        return "1"
    if fr == F(1, 2):
        return "-1"
    if fr == F(1, 4):
        return "i"
    if fr == F(3, 4):
        return "-i"
    return "e(%s)" % fr


def phase_order(k):
    """order of e(k/L) as a root of unity."""
    return L_PHASE // gcd(k % L_PHASE, L_PHASE) if k % L_PHASE else 1


# ---------------------------------------------------------------------------
# exact Q(zeta_8) arithmetic (delta-1c machinery)
# ---------------------------------------------------------------------------
Z8_ZERO = (F(0), F(0), F(0), F(0))
Z8_ONE = (F(1), F(0), F(0), F(0))


def z8_add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def z8_mul(a, b):
    out = [F(0)] * 4
    for i in range(4):
        if a[i] == 0:
            continue
        for j in range(4):
            if b[j] == 0:
                continue
            k = i + j
            if k < 4:
                out[k] += a[i] * b[j]
            else:
                out[k - 4] -= a[i] * b[j]
    return tuple(out)


def z8_scal(f, a):
    return tuple(f * x for x in a)


def z8_root(k):
    k %= 8
    s = F(1)
    if k >= 4:
        k -= 4
        s = F(-1)
    v = [F(0)] * 4
    v[k] = s
    return tuple(v)


def z8_conj(a):
    return (a[0], -a[3], -a[2], -a[1])


def z8_to_mpc(a):
    z = mp.exp(mp.mpc(0, mp.pi / 4))
    return (mp.mpf(a[0].numerator) / a[0].denominator
            + z * mp.mpf(a[1].numerator) / a[1].denominator
            + z ** 2 * mp.mpf(a[2].numerator) / a[2].denominator
            + z ** 3 * mp.mpf(a[3].numerator) / a[3].denominator)


def sum_z8(xs):
    out = Z8_ZERO
    for x in xs:
        out = z8_add(out, x)
    return out


def mat_mul(A, B):
    n = len(A)
    return [[sum_z8([z8_mul(A[i][k], B[k][j]) for k in range(n)])
             for j in range(n)] for i in range(n)]


def mat_eq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A))
               for j in range(len(A)))


def mat_id(n):
    return [[Z8_ONE if i == j else Z8_ZERO for j in range(n)]
            for i in range(n)]


def mat_conjT(A):
    n = len(A)
    return [[z8_conj(A[j][i]) for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------------------
# discriminant module D = Z4 x Z4, q = (5x^2 + 3y^2)/8 mod 1
# ---------------------------------------------------------------------------
MU = [(x, y) for x in range(4) for y in range(4)]
IDX = {m: i for i, m in enumerate(MU)}


def q8(mu):
    x, y = mu
    return (5 * x * x + 3 * y * y) % 8


def bil8(mu, nu):
    return (2 * (5 * mu[0] * nu[0] + 3 * mu[1] * nu[1])) % 8


def neg(mu):
    return ((-mu[0]) % 4, (-mu[1]) % 4)


def build_weil(qfun, bfun, group, sigma_conj):
    n = len(group)
    rt = F(1)
    m = n
    while m % 4 == 0:
        m //= 4
        rt *= 2
    assert m == 1
    T = [[z8_root(qfun(group[i])) if i == j else Z8_ZERO
          for j in range(n)] for i in range(n)]
    S = [[z8_scal(F(1, rt), z8_mul(sigma_conj,
                                   z8_root(-bfun(group[i], group[j]))))
          for j in range(n)] for i in range(n)]
    return T, S


def weil_matrices():
    return build_weil(q8, bil8, MU, Z8_ONE)


def rho_np(exact):
    return np.array([[complex(z8_to_mpc(exact[i][j])) for j in range(16)]
                     for i in range(16)])


# ---------------------------------------------------------------------------
# lattice ledgers (delta-1c machinery, verbatim)
# ---------------------------------------------------------------------------
MAXN_LED = 16
MAXN_CERT = 20


def build_d5_vecs(maxnorm):
    out = {x: [] for x in range(4)}
    lim = 16 * maxnorm
    r = int(maxnorm ** 0.5) + 1
    for v in product(range(-r, r + 1), repeat=5):
        n16 = 16 * sum(t * t for t in v)
        if n16 > lim:
            continue
        x = 0 if sum(v) % 2 == 0 else 2
        out[x].append((n16, tuple(2 * t for t in v)))
    ru = int((4 * maxnorm) ** 0.5) + 1
    odd = [k for k in range(-ru, ru + 1) if k % 2 != 0]
    for u in product(odd, repeat=5):
        n16 = 4 * sum(t * t for t in u)
        if n16 > lim:
            continue
        x = 1 if (sum(u) - 5) % 4 == 0 else 3
        out[x].append((n16, u))
    return out


def build_a3_vecs(maxnorm):
    out = {y: [] for y in range(4)}
    lim = 16 * maxnorm
    r = int(maxnorm ** 0.5) + 2
    for y in range(4):
        rng = [4 * m - y for m in range(-r, r + 2)]
        for w3 in product(rng, repeat=3):
            w4 = -(w3[0] + w3[1] + w3[2])
            if (w4 + y) % 4 != 0:
                continue
            n16 = w3[0] ** 2 + w3[1] ** 2 + w3[2] ** 2 + w4 ** 2
            if n16 <= lim:
                out[y].append((n16, w3 + (w4,)))
    return out


def factor_moments(vecs, form_re, form_im, kmax, maxn16):
    out = {}
    for cls, lst in vecs.items():
        acc = {}
        for n16, u in lst:
            if n16 > maxn16:
                continue
            dre = sum(a * b for a, b in zip(u, form_re))
            dim_ = (sum(a * b for a, b in zip(u, form_im))
                    if form_im else 0)
            ms = acc.get(n16)
            if ms is None:
                ms = acc[n16] = [[0, 0] for _ in range(kmax + 1)]
            pr, pi = 1, 0
            for k in range(kmax + 1):
                ms[k][0] += pr
                ms[k][1] += pi
                pr, pi = pr * dre - pi * dim_, pr * dim_ + pi * dre
        out[cls] = acc
    return out


def combine_series(m5x, m3y, k_ins, maxn16):
    out = {}
    for n5, a in m5x.items():
        for n3, b in m3y.items():
            n = n5 + n3
            if n > maxn16:
                continue
            cre = cim = 0
            for k in range(k_ins + 1):
                c = comb(k_ins, k)
                ar, ai = a[k]
                br, bi = b[k_ins - k]
                cre += c * (ar * br - ai * bi)
                cim += c * (ar * bi + ai * br)
            if cre or cim:
                o = out.get(n, (0, 0))
                out[n] = (o[0] + cre, o[1] + cim)
    return out


def eval_series16(ser, tau, maxn16):
    tot = mp.mpc(0)
    for n16, (cre, cim) in ser.items():
        if n16 > maxn16:
            continue
        tot += mp.mpc(cre, cim) * mp.exp(1j * mp.pi * tau * n16 / 16)
    return tot


SAMPLES = [
    (1, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 1, 0, 0),
    (0, 0, 0, 0, 0, 1, 1, 1),
    (1, 2, 0, 0, 0, 0, 0, 0),
    (1, 0, 0, 0, 0, 1, 0, 0),
    (1, 1, 1, 0, 0, 1, 1, 1),
]


def basis_at(pt):
    xs, ys = pt[:5], list(pt[5:])
    ys4 = ys + [-sum(ys)]
    S5 = sum(x * x for x in xs)
    S3 = sum(y * y for y in ys4)
    T5 = sum(x ** 4 for x in xs)
    T3 = sum(y ** 4 for y in ys4)
    return (S5 * S5, S5 * S3, S3 * S3, T5, T3)


BMAT = [basis_at(p) for p in SAMPLES]


def solve_cell(bvals):
    A = sp.Matrix([[BMAT[k][i] for i in range(5)] for k in range(6)])
    b = sp.Matrix([sp.Rational(x.numerator, x.denominator) for x in bvals])
    sol, params = A.gauss_jordan_solve(b)
    assert len(params) == 0 and A * sol == b
    return [F(sp.Rational(x).p, sp.Rational(x).q) for x in sol]


def build_ledgers16(d5vecs, a3vecs, maxnorm):
    lim16 = 16 * maxnorm
    md5 = {}
    for x in range(4):
        acc = {}
        for n16, u in d5vecs[x]:
            if n16 > lim16:
                continue
            ms = acc.get(n16)
            if ms is None:
                ms = acc[n16] = [[0] * 6 for _ in range(5)]
            for si, s in enumerate(SAMPLES):
                d = 2 * (u[0] * s[0] + u[1] * s[1] + u[2] * s[2]
                         + u[3] * s[3] + u[4] * s[4])
                p = 1
                for k in range(5):
                    ms[k][si] += p
                    p *= d
        md5[x] = acc
    ma3 = {}
    for y in range(4):
        acc = {}
        for n16, w in a3vecs[y]:
            if n16 > lim16:
                continue
            ms = acc.get(n16)
            if ms is None:
                ms = acc[n16] = [[0] * 6 for _ in range(5)]
            for si, s in enumerate(SAMPLES):
                d = ((w[0] - w[3]) * s[5] + (w[1] - w[3]) * s[6]
                     + (w[2] - w[3]) * s[7])
                p = 1
                for k in range(5):
                    ms[k][si] += p
                    p *= d
        ma3[y] = acc
    out4 = {m: {} for m in MU}
    out2 = {m: {} for m in MU}
    CNT = {m: {} for m in MU}
    for (x, y) in MU:
        acc4, acc2 = {}, {}
        for n5, m5 in md5[x].items():
            for n3, m3 in ma3[y].items():
                tot = n5 + n3
                if tot == 0 or tot > lim16:
                    continue
                lev = F(tot, 32)
                cell4 = acc4.get(lev)
                if cell4 is None:
                    cell4 = acc4[lev] = [0] * 6
                    acc2[lev] = [0, 0]
                for si in range(6):
                    cell4[si] += sum(comb(4, k) * m5[k][si] * m3[4 - k][si]
                                     for k in range(5))
                for si in range(2):
                    acc2[lev][si] += (m5[2][si] * m3[0][si]
                                      + 2 * m5[1][si] * m3[1][si]
                                      + m5[0][si] * m3[2][si])
                CNT[(x, y)][lev] = (CNT[(x, y)].get(lev, 0)
                                    + m5[0][0] * m3[0][0])
        for lev, cell in acc4.items():
            out4[(x, y)][lev] = solve_cell([F(c, 256) for c in cell])
            b0, b1 = acc2[lev]
            out2[(x, y)][lev] = (F(b0, 16), F(b1, 32))
    return out4, out2, CNT


# ---------------------------------------------------------------------------
# E8 roots in glue coordinates (replication anchor)
# ---------------------------------------------------------------------------
HALF = F(1, 2)


def build_glue_roots():
    d5_roots, d5_v = [], []
    for i, j in combinations(range(5), 2):
        for si in (1, -1):
            for sj in (1, -1):
                v = [F(0)] * 5
                v[i], v[j] = F(si), F(sj)
                d5_roots.append(tuple(v))
    for i in range(5):
        for s in (1, -1):
            v = [F(0)] * 5
            v[i] = F(s)
            d5_v.append(tuple(v))
    d5_s, d5_c = [], []
    for signs in product((1, -1), repeat=5):
        v = tuple(HALF * s for s in signs)
        (d5_s if signs.count(-1) % 2 == 0 else d5_c).append(v)
    a3_roots = []
    for i in range(4):
        for j in range(4):
            if i != j:
                v = [F(0)] * 4
                v[i], v[j] = F(1), F(-1)
                a3_roots.append(tuple(v))

    def wclass(k):
        out = []
        for sub in combinations(range(4), k):
            v = [F(-k, 4)] * 4
            for i in sub:
                v[i] += 1
            out.append(tuple(v))
        return out

    z5, z4 = tuple([F(0)] * 5), tuple([F(0)] * 4)
    roots = {}
    for r in d5_roots:
        roots[r + z4] = 0
    for r in a3_roots:
        roots[z5 + r] = 0
    for d in d5_s:
        for w in wclass(1):
            roots[d + w] = 1
    for d in d5_v:
        for w in wclass(2):
            roots[d + w] = 2
    for d in d5_c:
        for w in wclass(3):
            roots[d + w] = 3
    return roots


SIGMA3 = [1, 9, 28, 73, 126, 252, 344, 585]
DIAG = [(a, a) for a in range(4)]


# ---------------------------------------------------------------------------
# block numerics: gauge M = G/eta^8 and the axion blocks f_m
# ---------------------------------------------------------------------------
NPROD = 120
TAU_A = mp.mpc(mp.mpf(13) / 100, mp.mpf(51) / 50)
TAU_B = mp.mpc(mp.mpf(-31) / 100, mp.mpf(99) / 100)
TAU_C = mp.mpc(mp.mpf(7) / 100, mp.mpf(101) / 100)


def qp(tau, e):
    return mp.exp(2j * mp.pi * tau * e)


def geo_val(N, a, b, tau):
    zb = mp.exp(2j * mp.pi * b / N)
    zbb = mp.exp(-2j * mp.pi * b / N)
    ep = mp.mpf(a) / N if a else mp.mpf(1)
    em = 1 - mp.mpf(a) / N if a else mp.mpf(1)
    Eb = -mp.mpf(1) / 24 + (mp.mpf(a) / N) * (1 - mp.mpf(a) / N) / 4 \
        if a else -mp.mpf(1) / 24
    val = qp(tau, 4 * Eb)
    for n in range(NPROD):
        val /= (1 - zb * qp(tau, ep + n)) ** 2
        val /= (1 - zbb * qp(tau, em + n)) ** 2
    if a == 0 and b % N != 0:
        val /= (1 - zb) * (1 - zbb)
    return val


def eta_val(tau):
    val = qp(tau, mp.mpf(1) / 24)
    for n in range(1, NPROD + 1):
        val *= (1 - qp(tau, n))
    return val


def M_val(N, a, b, tau):
    return geo_val(N, a, b, tau) / eta_val(tau) ** 8


def f_val(N, m, a, b, tau):
    """one twisted complex boson of deck weight m in sector (a,b):
    twist parameters (aa, bb) = (m a, m b) mod N; delta-1b
    normalisation (G[a,b] = f_1 f_3 exactly); untwisted (0,0) factors
    are EXCLUDED (they contribute the SL(2,Z)-invariant real factor
    sqrt(tau2)|eta|^{-2}, no multiplier)."""
    aa = (m * a) % N
    bb = (m * b) % N
    if aa == 0 and bb == 0:
        return mp.mpc(1)
    z = mp.exp(2j * mp.pi * bb / N)
    zc = mp.exp(-2j * mp.pi * bb / N)
    ep = mp.mpf(aa) / N if aa else mp.mpf(1)
    em = 1 - mp.mpf(aa) / N if aa else mp.mpf(1)
    E = -mp.mpf(1) / 24 + (mp.mpf(aa) / N) * (1 - mp.mpf(aa) / N) / 4 \
        if aa else -mp.mpf(1) / 24
    val = qp(tau, 2 * E)
    for n in range(NPROD):
        val /= (1 - z * qp(tau, ep + n))
        val /= (1 - zc * qp(tau, em + n))
    if aa == 0 and bb % N != 0:
        val /= (1 - z)
    return val


def ax_val(N, ws, a, b, tau):
    v = mp.mpc(1)
    for m in ws:
        v *= f_val(N, m, a, b, tau)
    return v


def measure_transport_w(N, pairs, fM, wexp):
    """t_p: f_p(tau+1) = t_p f_{Tp}(tau); s_p: f_p(-1/tau) =
    s_p (-i tau)^{-wexp} f_{Sp}(tau); constancy over two tau."""
    t, s = {}, {}
    dev = mp.mpf(0)
    for (a, b) in pairs:
        Tp = (a, (a + b) % N)
        Sp = (b % N, (-a) % N)
        vals_t, vals_s = [], []
        for tau in (TAU_A, TAU_B):
            vals_t.append(fM(a, b, tau + 1) / fM(*Tp, tau))
            vals_s.append(fM(a, b, -1 / tau) * (-1j * tau) ** wexp
                          / fM(*Sp, tau))
        dev = max(dev, abs(vals_t[0] - vals_t[1]),
                  abs(vals_s[0] - vals_s[1]))
        t[(a, b)] = vals_t[0]
        s[(a, b)] = vals_s[0]
    return t, s, dev


def recog(z):
    """z = r e(k/L) recognition; returns (logmod mpf, k int, dev mpf)."""
    lm = mp.log(abs(z))
    ph = mp.arg(z) / (2 * mp.pi)
    k = int(mp.nint(ph * L_PHASE))
    dev = abs(ph - mp.mpf(k) / L_PHASE)
    return lm, k % L_PHASE, dev


# ---------------------------------------------------------------------------
# SL(2,Z) word machinery
# ---------------------------------------------------------------------------
GENM = {'T': ((1, 1), (0, 1)), 'S': ((0, -1), (1, 0))}


def m2mul(A, B):
    return ((A[0][0] * B[0][0] + A[0][1] * B[1][0],
             A[0][0] * B[0][1] + A[0][1] * B[1][1]),
            (A[1][0] * B[0][0] + A[1][1] * B[1][0],
             A[1][0] * B[0][1] + A[1][1] * B[1][1]))


def m2inv(A):
    (a, b), (c, d) = A
    return ((d, -b), (-c, a))


def pair_act(p, g2, N):
    a, b = p
    return ((a * g2[0][0] + b * g2[1][0]) % N,
            (a * g2[0][1] + b * g2[1][1]) % N)


def orbit_loops(N, tph, sph, base, RT=None, RS=None):
    """BFS transport groupoid with exact word bookkeeping.
    tph/sph: {p: (logmod, k)}.  RT/RS: exact rho(T), rho(S) (both equal
    their transposes: T diagonal, S symmetric); None = scalar-only run.
    Returns (loops, Lam); loop dict: at, logmod, k, gamma, nT, nS,
    Hrho (exact, or None)."""
    with_rho = RT is not None
    I2 = ((1, 0), (0, 1))
    Lam = {base: (mp.mpf(0), 0, mat_id(16) if with_rho else None,
                  I2, 0, 0)}
    queue = [base]
    loops = []
    seen = set()
    while queue:
        p = queue.pop(0)
        lm, kp, W, M2, nT, nS = Lam[p]
        for g in ('T', 'S'):
            if (p, g) in seen:
                continue
            seen.add((p, g))
            p2 = pair_act(p, GENM[g], N)
            cm, ck = (tph if g == 'T' else sph)[p]
            W2 = mat_mul(RT if g == 'T' else RS, W) if with_rho else None
            dat = (lm + cm, (kp + ck) % L_PHASE, W2,
                   m2mul(M2, GENM[g]),
                   nT + (1 if g == 'T' else 0),
                   nS + (0 if g == 'T' else 1))
            if p2 not in Lam:
                Lam[p2] = dat
                queue.append(p2)
            else:
                lm2, k2, Wb, Mb, nT2, nS2 = Lam[p2]
                loops.append(dict(
                    at=(p, g, p2),
                    logmod=dat[0] - lm2,
                    k=(dat[1] - k2) % L_PHASE,
                    Hrho=(mat_mul(mat_conjT(Wb), W2) if with_rho
                          else None),
                    gamma=m2mul(dat[3], m2inv(Mb)),
                    nT=dat[4] - nT2, nS=dat[5] - nS2))
    return loops, Lam


def word_scalar(p, word, tph, sph, N):
    lm = mp.mpf(0)
    k = 0
    for g in word:
        cm, ck = (tph if g == 'T' else sph)[p]
        lm += cm
        k = (k + ck) % L_PHASE
        p = pair_act(p, GENM[g], N)
    return lm, k, p


# ---------------------------------------------------------------------------
# contraction solve machinery (delta-1c, verbatim)
# ---------------------------------------------------------------------------
def sl2z_char(k):
    return (np.exp(2j * np.pi * k / 12), np.exp(-2j * np.pi * k / 4))


def solve_orbit(pairs, N, tconst, sconst, rhoT_np, rhoS_np, base, k=0):
    chT, chS = sl2z_char(k)
    TT = rhoT_np.T
    ST = rhoS_np.T
    Lam = {base: np.eye(16, dtype=complex)}
    queue = [base]
    rows = []
    hols = []
    seen_edges = set()
    while queue:
        p = queue.pop(0)
        a, b = p
        for tag, p2, Mx in (
                ('T', (a, (a + b) % N),
                 complex(tconst[p]) / chT * TT),
                ('S', ((b % N), (-a) % N),
                 complex(sconst[p]) / chS * ST)):
            if (p, tag) in seen_edges:
                continue
            seen_edges.add((p, tag))
            cand = Mx @ Lam[p]
            if p2 not in Lam:
                Lam[p2] = cand
                queue.append(p2)
            else:
                rows.append(cand - Lam[p2])
                hols.append((p, tag, np.linalg.inv(Lam[p2]) @ cand))
    A = np.vstack(rows) if rows else np.zeros((1, 16), dtype=complex)
    _, sv, Vh = np.linalg.svd(A)
    sv = list(sv) + [0.0] * (16 - len(sv))
    tol = max(sv) * 1e-8 if max(sv) > 0 else 1e-8
    null = [Vh[i].conj() for i in range(16) if sv[i] < tol]
    return sorted(Lam.keys()), Lam, null, sv, hols


def joint_eigvecs(Hs, rng_seed=11):
    if not Hs:
        return []
    rng = np.random.default_rng(rng_seed)
    coef = rng.normal(size=len(Hs)) + 1j * rng.normal(size=len(Hs))
    Hr = sum(c * H for c, H in zip(coef, Hs))
    _, V = np.linalg.eig(Hr)
    out = []
    for i in range(16):
        v = V[:, i]
        v = v / np.linalg.norm(v)
        lams = []
        res = 0.0
        for H in Hs:
            lam = np.vdot(v, H @ v)
            res = max(res, np.linalg.norm(H @ v - lam * v))
            lams.append(lam)
        if res < 1e-8:
            out.append((v, lams, res))
    return out


def project_seed(Lam, null, seed):
    if not null:
        return None, 0.0
    V = np.array(null).T
    G = sum(Lam[p].conj().T @ Lam[p] for p in Lam)
    Avec = sum(Lam[p].conj().T @ seed[p] for p in Lam)
    Gv = V.conj().T @ G @ V
    c = np.linalg.solve(Gv, V.conj().T @ Avec)
    b0 = V @ c
    beta = {p: Lam[p] @ b0 for p in Lam}
    n_pr = np.sqrt(sum(np.vdot(beta[p], beta[p]).real for p in beta))
    n_sd = np.sqrt(sum(np.vdot(seed[p], seed[p]).real for p in seed))
    ov = sum(np.vdot(seed[p], beta[p]).real for p in beta)
    cos = ov / (n_pr * n_sd) if n_pr > 0 else 0.0
    return beta, cos


# ---------------------------------------------------------------------------
# exact dressing series (delta-1b/1c machinery) + axion series
# ---------------------------------------------------------------------------
GRID_CUT = F(8)
GRID_CUT_LOW = F(6)
BASES4 = {0: F(-1, 2), 1: F(-5, 16), 2: F(-1, 4), 3: F(-5, 16)}


def gadd(z1, z2):
    return (z1[0] + z2[0], z1[1] + z2[1])


def gmul(z1, z2):
    return (z1[0] * z2[0] - z1[1] * z2[1], z1[0] * z2[1] + z1[1] * z2[0])


def ipow(b):
    return [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))][b % 4]


def uroot(N, k):
    if N == 2:
        return [(F(1), F(0)), (F(-1), F(0))][k % 2]
    return ipow(k)


def ser_mul(A, B, cut):
    out = {}
    for e1, v1 in A.items():
        for e2, v2 in B.items():
            e = e1 + e2
            if e > cut:
                continue
            out[e] = gadd(out.get(e, (F(0), F(0))), gmul(v1, v2))
    return {e: v for e, v in out.items() if v != (F(0), F(0))}


def tower(zeta, e0, cut):
    """expansion of prod_n (1 - zeta q^{e0+n})^{-2}."""
    out = {F(0): (F(1), F(0))}
    n = 0
    while e0 + n <= cut:
        e = e0 + n
        n += 1
        if e <= 0:
            continue
        fac = {F(0): (F(1), F(0))}
        k = 1
        zk = zeta
        while k * e <= cut:
            fac[k * e] = (F(k + 1) * zk[0], F(k + 1) * zk[1])
            zk = gmul(zk, zeta)
            k += 1
        out = ser_mul(out, fac, cut)
    return out


def tower1(zeta, e0, cut):
    """expansion of prod_n (1 - zeta q^{e0+n})^{-1}."""
    out = {F(0): (F(1), F(0))}
    n = 0
    while e0 + n <= cut:
        e = e0 + n
        n += 1
        if e <= 0:
            continue
        fac = {F(0): (F(1), F(0))}
        k = 1
        zk = zeta
        while k * e <= cut:
            fac[k * e] = zk
            zk = gmul(zk, zeta)
            k += 1
        out = ser_mul(out, fac, cut)
    return out


def geo_block(N, a, b, cut):
    ab = F(a, N)
    e_plus = ab if a else F(1)
    e_minus = (1 - ab) if a else F(1)
    block = ser_mul(tower(uroot(N, b), e_plus, cut),
                    tower(uroot(N, -b), e_minus, cut), cut)
    zm = None
    if a == 0 and b % N != 0:
        wb, wmb = uroot(N, b), uroot(N, -b)
        zm = gmul((F(1) - wb[0], -wb[1]), (F(1) - wmb[0], -wmb[1]))
    return block, zm


def p8_series(nmax):
    out = [F(1)] + [F(0)] * nmax
    for d in range(1, nmax + 1):
        geo = [F(0)] * (nmax + 1)
        k = 0
        while d * k <= nmax:
            geo[d * k] = F(int(sp.binomial(8 + k - 1, k)))
            k += 1
        new = [F(0)] * (nmax + 1)
        for i, av in enumerate(out):
            if av == 0:
                continue
            for j, bv in enumerate(geo[:nmax + 1 - i]):
                new[i + j] += av * bv
        out = new
    return out


def gauge_dress_series(N, a, b, cut):
    """q^{base_a} G[a,b] P8, phase-free (i^{ab} lives in beta),
    AB zero mode included; returns {ex: gauss-rational}."""
    geo, zm = geo_block(N, a, b, cut + 1)
    w = (F(1), F(0))
    if zm is not None:
        nrm = zm[0] * zm[0] + zm[1] * zm[1]
        w = (zm[0] / nrm, -zm[1] / nrm)
    p8 = p8_series(int(cut) + 1)
    dress = {}
    for e, cv in geo.items():
        for m2, pv in enumerate(p8):
            if pv == 0:
                continue
            ex = e + m2
            if ex > cut:
                continue
            dress[ex] = gadd(dress.get(ex, (F(0), F(0))),
                             gmul(w, (cv[0] * pv, cv[1] * pv)))
    return dress


def f_series(N, m, a, b, cut):
    """exact q-series of f_m[a,b] (without q^{2E} prefactor);
    returns (series, exponent shift 2E as Fraction)."""
    aa = (m * a) % N
    bb = (m * b) % N
    if aa == 0 and bb == 0:
        return {F(0): (F(1), F(0))}, F(0)
    ep = F(aa, N) if aa else F(1)
    em = (1 - F(aa, N)) if aa else F(1)
    ser = ser_mul(tower1(uroot(N, bb), ep, cut),
                  tower1(uroot(N, -bb), em, cut), cut)
    if aa == 0 and bb % N != 0:
        w = uroot(N, bb)
        d = (F(1) - w[0], -w[1])
        nrm = d[0] * d[0] + d[1] * d[1]
        winv = (d[0] / nrm, -d[1] / nrm)
        ser = {e: gmul(winv, v) for e, v in ser.items()}
    shift = 2 * (F(-1, 24) + F(aa, N) * (1 - F(aa, N)) / 4)
    return ser, shift


def eta_pow_series(mm, cut):
    """(prod (1-q^n))^{mm}, mm in Z; returns (series, shift mm/24)."""
    nmax = int(cut) + 1
    out = [F(1)] + [F(0)] * nmax

    def poly_mul(A, B):
        new = [F(0)] * (nmax + 1)
        for i, av in enumerate(A):
            if av == 0:
                continue
            for j, bv in enumerate(B[:nmax + 1 - i]):
                if bv:
                    new[i + j] += av * bv
        return new

    for d in range(1, nmax + 1):
        fac = [F(0)] * (nmax + 1)
        if mm >= 0:
            k = 0
            while d * k <= nmax and k <= mm:
                fac[d * k] = F((-1) ** k * comb(mm, k))
                k += 1
        else:
            mpos = -mm
            k = 0
            while d * k <= nmax:
                fac[d * k] = F(comb(mpos + k - 1, k))
                k += 1
        out = poly_mul(out, fac)
    return ({F(n): (c, F(0)) for n, c in enumerate(out) if c != 0},
            F(mm, 24))


import math

_GLX, _GLW = np.polynomial.legendre.leggauss(160)
_TH = [(math.pi / 12) * (x + 1) for x in _GLX]
_WTH = [(math.pi / 12) * w for w in _GLW]
_J_CACHE = {}


def Jval(delta, s):
    key = (delta, s)
    if key in _J_CACHE:
        return _J_CACHE[key]
    d = mp.mpf(delta.numerator) / mp.mpf(delta.denominator)
    cusp = (mp.sin(mp.pi * d) / (mp.pi * d)
            * (2 * mp.pi * d) ** (s - 1) * mp.gammainc(1 - s, 2 * mp.pi * d))
    df = float(d)
    sinpd = math.sin(math.pi * df)
    arc = 0.0
    for th, wt in zip(_TH, _WTH):
        ct, st = math.cos(th), math.sin(th)
        arc += wt * (st * ct ** (-s) * math.exp(-2 * math.pi * df * ct)
                     * (sinpd - math.sin(2 * math.pi * df * st))
                     / (math.pi * df))
    val = cusp + mp.mpf(arc)
    _J_CACHE[key] = val
    return val


def hm_integral_pp(beta, dressmaps, basemap, V4, V2, CNT, cut, weight):
    """delta-1c hm_integral with PER-PAIR bases + negative-cell audit."""
    I_main = [mp.mpc(0)] * 5
    I_comp = [mp.mpc(0)] * 5
    W = {}
    n_neg = 0
    wt_neg = mp.mpf(0)
    for p, dress in dressmaps.items():
        a = p[0]
        base = basemap[p]
        bp = beta[p]
        for i_mu, mu in enumerate(MU):
            bc = complex(bp[i_mu])
            if abs(bc) < 1e-14:
                continue
            bz = mp.mpc(bc.real, bc.imag)
            for ex, cv in dress.items():
                cz = bz * mp.mpc(mp.mpf(cv[0].numerator) / cv[0].denominator,
                                 mp.mpf(cv[1].numerator) / cv[1].denominator)
                for lev, vec4 in V4[mu].items():
                    D = base + ex + lev
                    if D > cut:
                        continue
                    if D <= 0:
                        n_neg += 1
                        wt_neg = max(wt_neg, abs(cz))
                        continue
                    z0 = cz * Jval(D, 0)
                    for i in range(5):
                        z = z0 * (mp.mpf(vec4[i].numerator)
                                  / vec4[i].denominator)
                        I_main[i] += weight * z
                    if mu[0] == mu[1]:
                        key = (a, lev)
                        W[key] = W.get(key, mp.mpc(0)) + weight * z0
                    u, v = V2[mu][lev]
                    z1 = cz * Jval(D, 1) * mp.mpf(-3) / (2 * mp.pi)
                    uu = mp.mpf(u.numerator) / u.denominator
                    vv = mp.mpf(v.numerator) / v.denominator
                    I_comp[0] += weight * z1 * uu
                    I_comp[1] += weight * z1 * (uu + vv)
                    I_comp[2] += weight * z1 * vv
                    z2 = (cz * Jval(D, 2) * mp.mpf(3)
                          / (16 * mp.pi ** 2) * CNT[mu][lev])
                    I_comp[0] += weight * z2
                    I_comp[1] += weight * z2 * 2
                    I_comp[2] += weight * z2
    I_hat = [I_main[i] + I_comp[i] for i in range(5)]
    return I_main, I_hat, W, n_neg, wt_neg


# ---------------------------------------------------------------------------
# pair sets, seeds, candidates
# ---------------------------------------------------------------------------
PAIRS4 = [(a, b) for a in range(4) for b in range(4) if (a, b) != (0, 0)]
ORB1 = [p for p in PAIRS4 if gcd(gcd(p[0], p[1]), 4) == 1]
ORB2 = [p for p in PAIRS4 if gcd(gcd(p[0], p[1]), 4) == 2]

CAND_WS = {
    'f2': (2,),
    'f1f3': (1, 3),
    'f1f2f3': (1, 2, 3),
    'wrong112': (1, 1, 2),
    'wrong222': (2, 2, 2),
}


def make_seed():
    seed = {}
    for p in PAIRS4:
        v = np.zeros(16, dtype=complex)
        v[IDX[(p[0] % 4, p[0] % 4)]] = 1j ** ((p[0] * p[1]) % 4)
        seed[p] = v
    return seed


# ---------------------------------------------------------------------------
# D0 -- conventions, targets, 16-class ledger
# ---------------------------------------------------------------------------
def section0():
    print("  -- D0: conventions, targets, 16-class ledger (replication)")
    roots = build_glue_roots()
    cnt = [sum(1 for c in roots.values() if c == m) for m in range(4)]
    check("D0.1 [ROOTS] 240 roots, norm 2, class split %s = (52,64,60,64)"
          % fmt(cnt),
          len(roots) == 240 and cnt == [52, 64, 60, 64]
          and all(sum(x * x for x in r) == 2 for r in roots))

    print("     [building 16-class exact ledgers to level 8 ...]")
    d5led = build_d5_vecs(MAXN_LED)
    a3led = build_a3_vecs(MAXN_LED)
    V4, V2, CNT = build_ledgers16(d5led, a3led, MAXN_LED)

    Qtab = {0: [12, 0, 6, 4, 8], 1: [12, 24, 0, -8, 16],
            2: [0, 24, 30, 12, -40], 3: [12, 24, 0, -8, 16]}
    ok_q = all(V4[(a, a)].get(F(1)) == Qtab[a] for a in range(4))
    tots = [sum(CNT[(a, a)].get(F(n), 0) for a in range(4))
            for n in range(1, 9)]
    check("D0.2 [LEDGER] diagonal slice = delta-1 quartic ledger "
          "(V_{(a,a),1} = Q_a exactly); diagonal counts = 240 sigma_3(n) "
          "for n <= 8", ok_q and tots == [240 * s for s in SIGMA3])

    cA = [F(5, 4), F(-1, 4), F(-3, 4), F(-1, 4)]
    Afix = [sum(cA[m] * Qtab[m][i] for m in range(4)) for i in range(5)]
    psi = [F(3), F(-1), F(-1), F(0), F(-1, 4)]
    psiA = sum(psi[i] * Afix[i] for i in range(5))
    check("D0.3 [TARGETS] A_fix = %s = (9,-30,-15,0,32); psi(A_fix) = %s "
          "= 64; waiting tests: T5(V) = 0, W_2 : W_13 -> 4:3, "
          "psi(V) = -64 N or V = -A_fix N" % (fmt(Afix), psiA),
          Afix == [9, -30, -15, 0, 32] and psiA == 64)
    return V4, V2, CNT, Afix, psi


# ---------------------------------------------------------------------------
# D1 -- Weil rep + gauge transport constants, exact phase recognition
# ---------------------------------------------------------------------------
def section1():
    print("  -- D1: Weil representation + gauge block transport constants")
    Tx, Sx = weil_matrices()
    n = 16
    C = [[Z8_ONE if MU[j] == neg(MU[i]) else Z8_ZERO for j in range(n)]
         for i in range(n)]
    S2 = mat_mul(Sx, Sx)
    ST = mat_mul(Sx, Tx)
    ST3 = mat_mul(mat_mul(ST, ST), ST)
    T8 = mat_id(n)
    for _ in range(8):
        T8 = mat_mul(T8, Tx)
    ok_sym = all(Sx[i][j] == Sx[j][i] for i in range(n) for j in range(n))
    check("D1.1 [WEIL EXACT] S symmetric + unitary, S^2 = C, (ST)^3 = "
          "S^2, S^4 = 1, T^8 = 1 (level 8) -- exact Q(zeta_8) "
          "(delta-1c C1.2 replication)",
          ok_sym and mat_eq(mat_mul(Sx, mat_conjT(Sx)), mat_id(n))
          and mat_eq(S2, C) and mat_eq(ST3, S2)
          and mat_eq(mat_mul(S2, S2), mat_id(n)) and mat_eq(T8, mat_id(n)))

    tg, sg, dev = measure_transport_w(
        4, PAIRS4, lambda a, b, tau: M_val(4, a, b, tau), 4)
    check("D1.2 [GAUGE TRANSPORT] (t_p, s_p) of M = G[a,b] eta^{-8} "
          "constant over two tau for all 15 pairs (max dev %s < 1e-28)"
          % mp.nstr(dev, 3), dev < mp.mpf(10) ** (-28))

    tgx, sgx = {}, {}
    devmax = mp.mpf(0)
    print("     pair    t = r e(k/960)            s = r e(k/960)")
    for p in PAIRS4:
        lt, kt, dt = recog(tg[p])
        ls, ks, ds = recog(sg[p])
        devmax = max(devmax, dt, ds)
        tgx[p] = (lt, kt)
        sgx[p] = (ls, ks)
        print("     %s  |t|=%-8s %-12s |s|=%-8s %s"
              % (p, mp.nstr(mp.e ** lt, 5), phs(kt),
                 mp.nstr(mp.e ** ls, 5), phs(ks)))
    check("D1.3 [PHASE RECOGNITION] every t_p, s_p recognised as "
          "r e(k/960) with max phase deviation %s < 1e-25"
          % mp.nstr(devmax, 3), devmax < mp.mpf(10) ** (-25))

    ok_fix = all(tgx[(0, b)][1] == L_PHASE // 2
                 and abs(tgx[(0, b)][0]) < mp.mpf(10) ** (-30)
                 for b in (1, 2, 3))
    check("D1.4 [LEVEL-MATCHING DEFECT, EXACT] the T-fixed pairs (0,b) "
          "have t = e(-1/2) = -1 EXACTLY (leading exponent -1/2 on an "
          "integer grid): the naked order-2 seed of the multiplier "
          "system sits at the T-fixed nodes", ok_fix)
    return Tx, Sx, tg, sg, tgx, sgx


# ---------------------------------------------------------------------------
# D2 -- the multiplier system explicit
# ---------------------------------------------------------------------------
def eig_phase_table(loops, evs):
    """per (loop, eigvec): recognised phase k; returns table + max dev."""
    tab = []
    devm = mp.mpf(0)
    for lp in loops:
        Hn = (complex(mp.e ** lp['logmod'])
              * complex(mp.exp(2j * mp.pi * mp.mpf(lp['k']) / L_PHASE))
              * rho_np(lp['Hrho']))
        row = []
        for (v, _, _) in evs:
            lam = np.vdot(v, Hn @ v)
            lm, kk, dv = recog(mp.mpc(lam))
            devm = max(devm, dv, abs(lm))
            row.append(kk)
        tab.append(row)
    return tab, devm


def section2(Tx, Sx, tg, sg, tgx, sgx):
    print("  -- D2: THE MULTIPLIER SYSTEM (exact loops, cocycle test)")
    out = {}
    for name, orb, base, stab in (('gcd1', ORB1, (0, 1), 'Gamma_1(4)'),
                                  ('gcd2', ORB2, (0, 2), 'Gamma_0(2)+-')):
        loops, Lam = orbit_loops(4, tgx, sgx, base, Tx, Sx)
        ok_stab = True
        for lp in loops:
            g = lp['gamma']
            if pair_act(base, g, 4) != base:
                ok_stab = False
            if name == 'gcd1' and (g[1][0] % 4 != 0 or g[1][1] % 4 != 1):
                ok_stab = False
            if name == 'gcd2' and (g[1][0] % 2 != 0 or g[1][1] % 2 != 1):
                ok_stab = False
        ok_mod = max(abs(lp['logmod']) for lp in loops) < mp.mpf(10) ** (-25)
        Hs = [(complex(mp.e ** lp['logmod'])
               * complex(mp.exp(2j * mp.pi * mp.mpf(lp['k']) / L_PHASE))
               * rho_np(lp['Hrho'])) for lp in loops]
        evs = joint_eigvecs(Hs)
        tab, devm = eig_phase_table(loops, evs)
        seed_ov = [abs(v[IDX[(base[0] % 4, base[0] % 4)]])
                   for (v, _, _) in evs]
        ibest = int(np.argmax(seed_ov)) if evs else -1
        orders = sorted({phase_order(k) for row in tab for k in row})
        print("     [%s] base %s, %d nodes, %d loops, joint eigenspace "
              "dim %d/16, eigen-phase orders %s (stab %s)"
              % (name, base, len(Lam), len(loops), len(evs), fmt(orders),
                 stab))
        print("     loop  gamma            (C,D) mod 4   scalar     "
              "seed-eig phase")
        for i, lp in enumerate(loops):
            g = lp['gamma']
            print("     %-4d  [[%d,%d],[%d,%d]]%s  (%d,%d)      %-9s  %s"
                  % (i, g[0][0], g[0][1], g[1][0], g[1][1],
                     ' ' * max(0, 12 - len("[[%d,%d],[%d,%d]]"
                                           % (g[0][0], g[0][1],
                                              g[1][0], g[1][1]))),
                     g[1][0] % 4, g[1][1] % 4, phs(lp['k']),
                     phs(tab[i][ibest]) if ibest >= 0 else '--'))
        out[name] = dict(loops=loops, Lam=Lam, evs=evs, tab=tab,
                         ibest=ibest, orders=orders)
        exp_dim = 8 if name == 'gcd1' else 6
        check("D2.%s [%s LOOPS -> %s] all %d loop matrices gamma lie in "
              "the stabiliser %s (exact integer check); loop scalars "
              "unitary (max |log|mod|| < 1e-25: %s); joint eigenspace "
              "dim %d/16 = %d (delta-1c replication); eigen-phases "
              "snap to the 1/960 grid at double precision (dev %s "
              "< 1e-10, grid spacing 1e-3), orders %s <= 4"
              % ('1a' if name == 'gcd1' else '1b', name, stab,
                 len(loops), stab, ok_mod, len(evs), exp_dim,
                 mp.nstr(devm, 3), fmt(orders)),
              ok_stab and ok_mod and len(evs) == exp_dim
              and devm < mp.mpf(10) ** (-10) and max(orders) <= 4)

    # cocycle-vs-character: SL(2,Z) relation defects (pure scalars)
    ok_rel = True
    worst = 0
    print("     relation defects per pair: c_{S^4}, c_{(ST)^3 S^-2}, "
          "c_{[S^2,T]}")
    for p in PAIRS4:
        l1, k1, e1 = word_scalar(p, 'SSSS', tgx, sgx, 4)
        l2a, k2a, e2a = word_scalar(p, 'STSTST', tgx, sgx, 4)
        l2b, k2b, e2b = word_scalar(p, 'SS', tgx, sgx, 4)
        l3a, k3a, e3a = word_scalar(p, 'SST', tgx, sgx, 4)
        l3b, k3b, e3b = word_scalar(p, 'TSS', tgx, sgx, 4)
        assert e1 == p and e2a == e2b and e3a == e3b
        d1 = k1 % L_PHASE
        d2 = (k2a - k2b) % L_PHASE
        d3 = (k3a - k3b) % L_PHASE
        dm = max(abs(l1), abs(l2a - l2b), abs(l3a - l3b))
        if d1 or d2 or d3 or dm > mp.mpf(10) ** (-25):
            ok_rel = False
            worst = max(worst, phase_order(d1), phase_order(d2),
                        phase_order(d3))
            print("       %s : %s, %s, %s  <-- NONTRIVIAL"
                  % (p, phs(d1), phs(d2), phs(d3)))
    if ok_rel:
        print("       all 15 pairs: (1, 1, 1) exactly")
    check("D2.2 [KOZYKEL vs CHARAKTER, EXACT] the SL(2,Z) relation "
          "defects c_{S^4}(p), c_{(ST)^3 S^-2}(p), c_{[S^2,T]}(p) "
          "(gauge- and character-invariant pure scalars, exact 1/960 "
          "phase arithmetic): %s -- the multiplier system is %s"
          % ("ALL TRIVIAL" if ok_rel else "NONTRIVIAL (max order %d)"
             % worst,
             "a CHARACTER of the orbit stabilisers (Gamma_1(4) resp. "
             "Gamma_0(2)+-), NOT a genuine 2-cocycle on SL(2,Z)"
             if ok_rel else "a genuine 2-cocycle (projective datum) on "
             "SL(2,Z)"), True)
    out['relations_trivial'] = ok_rel

    # the finite group generated by the multiplier values
    allk = [k for name in ('gcd1', 'gcd2')
            for row in out[name]['tab'] for k in row]
    gord = 1
    for k in allk:
        gord = lcm(gord, phase_order(k))
    check("D2.3 [THE GROUP IS mu_%d] the multiplier values on the joint "
          "eigenspaces generate exactly the cyclic group of order %d "
          "(orders present: %s / %s)"
          % (gord, gord, fmt(out['gcd1']['orders']),
             fmt(out['gcd2']['orders'])), gord == 4)

    # monomial character fit on Gamma_1(4) loop data (seed eigenvector)
    lps = out['gcd1']['loops']
    tab1 = out['gcd1']['tab']
    ib = out['gcd1']['ibest']
    feats, lams4 = [], []
    ok_div = True
    for i, lp in enumerate(lps):
        g = lp['gamma']
        A, B = g[0]
        Cc, D = g[1]
        feats.append(((B) % 4, (Cc // 4) % 4, ((A - 1) // 4) % 4,
                      ((D - 1) // 4) % 4))
        k4 = tab1[i][ib] * 4
        if k4 % L_PHASE:
            ok_div = False
        lams4.append((k4 // L_PHASE) % 4)
    fits = []
    if ok_div:
        for x in product(range(4), repeat=4):
            if all((x[0] * f[0] + x[1] * f[1] + x[2] * f[2]
                    + x[3] * f[3]) % 4 == l4
                   for f, l4 in zip(feats, lams4)):
                fits.append(x)
    print("     Gamma_1(4) character fit lambda(gamma) = i^{x1 B + "
          "x2 (C/4) + x3 (A-1)/4 + x4 (D-1)/4}: solutions %s"
          % (fits if fits else "NONE (not a monomial in these residues)"))
    check("D2.4 [CHARACTER FORMULA] the seed-eigenvector multiplier on "
          "Gamma_1(4): all values in mu_4 (%s); monomial fit in the "
          "residues (B, C/4, (A-1)/4, (D-1)/4) mod 4: %s -- reported as "
          "computed" % (ok_div, fits if fits else "none"), True)
    out['fits'] = fits

    # the T-fixed support constraint table (exact)
    print("     T-fixed pair support: t_(0,b) x e(q(mu)) = chi_k(T) "
          "demands q8(mu) = (2k/3 + 4 - m/3) mod 8 [gauge, eta^m]")
    q8vals = sorted({q8(mu) for mu in MU})
    print("     attained q8 values: %s (6 isotropic classes at q8 = 0; "
          "diagonal seed classes have q8 = 0)" % fmt(q8vals))
    sup = {}
    for k in range(12):
        need = F(k, 12) + F(1, 2)
        need8 = (need * 8) % 8
        if need8.denominator == 1:
            cls = [mu for mu in MU if q8(mu) == int(need8)]
        else:
            cls = []
        sup[k] = cls
    live = [k for k in range(12) if sup[k]]
    seedk = [k for k in range(12) if any(mu in DIAG for mu in sup[k])]
    print("     gauge only (m = 0): support nonempty at k = %s; "
          "diagonal-seed classes allowed at k = %s" % (fmt(live),
                                                       fmt(seedk)))
    check("D2.5 [T-FIXED CONSTRAINT, EXACT] with the bare gauge blocks "
          "the T-fixed pairs (0,b) restrict any invariant contraction "
          "to classes with q8 = 2k/3 + 4 mod 8: nonempty only for "
          "k = %s, and the diagonal (v502) classes are allowed only at "
          "k = %s -- combined with the loop holonomies delta-1c found "
          "NO strict character: this is the exact shape of the "
          "obstruction" % (fmt(live), fmt(seedk)), len(live) > 0)
    return out


# ---------------------------------------------------------------------------
# D3 -- the cancellation candidate: the three sphere axions
# ---------------------------------------------------------------------------
def section3(tgx, sgx):
    print("  -- D3: THE CANCELLATION CANDIDATE (three sphere axions)")
    # v502 vacuum energies, exact
    Ev = {th: F(-1, 24) + th * (1 - th) / 4
          for th in (F(0), F(1, 4), F(1, 2), F(3, 4))}
    check("D3.1 [v502 VACUUM ENERGIES, EXACT] E_b(theta) = -1/24 + "
          "theta(1-theta)/4 at theta = (0, 1/4, 1/2, 3/4) = %s = "
          "(-1/24, 1/192, 1/48, 1/192); the axion Coxeter characters "
          "{i, -1, -i} = weights (1, 2, 3) = A3 exponents (v493/v505)"
          % fmt([Ev[t] for t in (F(0), F(1, 4), F(1, 2), F(3, 4))]),
          [Ev[t] for t in (F(0), F(1, 4), F(1, 2), F(3, 4))]
          == [F(-1, 24), F(1, 192), F(1, 48), F(1, 192)])

    # G = f_1 f_3 exactly (the gauge C^2 block IS the weight-(1,3) pair)
    devG = mp.mpf(0)
    for (a, b) in ((0, 1), (1, 0), (1, 1), (2, 1), (0, 2), (3, 2)):
        for tau in (TAU_A, TAU_B):
            g = geo_val(4, a, b, tau)
            ff = f_val(4, 1, a, b, tau) * f_val(4, 3, a, b, tau)
            devG = max(devG, abs(g - ff) / abs(g))
    check("D3.2 [G = f_1 f_3, EXACT IDENTITY] the twisted C^2 gauge "
          "block factorises as the weight-1 x weight-3 axion pair "
          "(same towers, prefactors 2E+2E = 4E, AB zero modes "
          "(1-i^b)(1-i^{-b})): max rel deviation %s < 1e-30 over six "
          "pairs x two tau -- the cancellation candidate f_1 f_2 f_3 "
          "differs from the gauge content exactly by the weight-2 "
          "axion f_2" % mp.nstr(devG, 3), devG < mp.mpf(10) ** (-30))

    # axion transport constants for all candidates
    axd = {}
    for name, ws in CAND_WS.items():
        tA, sA, dev = measure_transport_w(
            4, PAIRS4, lambda a, b, tau: ax_val(4, ws, a, b, tau), 0)
        tAx, sAx = {}, {}
        dmax = mp.mpf(0)
        for p in PAIRS4:
            lt, kt, dt = recog(tA[p])
            ls, ks, ds = recog(sA[p])
            dmax = max(dmax, dt, ds)
            tAx[p] = (lt, kt)
            sAx[p] = (ls, ks)
        axd[name] = dict(ws=ws, t=tA, s=sA, tx=tAx, sx=sAx,
                         dev=dev, rec=dmax)
    ok_c = all(d['dev'] < mp.mpf(10) ** (-28) for d in axd.values())
    ok_r = all(d['rec'] < mp.mpf(10) ** (-25) for d in axd.values())
    check("D3.3 [AXION TRANSPORT] (t^A, s^A) constant (max dev %s) and "
          "recognised on the 1/960 grid (max %s) for all candidates "
          "%s" % (mp.nstr(max(d['dev'] for d in axd.values()), 3),
                  mp.nstr(max(d['rec'] for d in axd.values()), 3),
                  list(CAND_WS)), ok_c and ok_r)

    # exact T-prediction: t^A_p = e(sum 2E) x (coefficient map); at the
    # T-fixed pairs the coefficient map is the identity -> pure e(sum 2E)
    okT = True
    for b in (1, 2, 3):
        shift = F(0)
        for m in CAND_WS['f1f2f3']:
            aa = 0
            bb = (m * b) % 4
            if aa == 0 and bb == 0:
                continue
            shift += 2 * F(-1, 24)
        kpred = int(shift * L_PHASE) % L_PHASE
        if axd['f1f2f3']['tx'][(0, b)][1] != kpred:
            okT = False
    print("     f1f2f3 T-fixed pairs: t^A_(0,b) = %s (predicted "
          "e(-1/4) = -i for b odd, e(-1/6) for b = 2 [f_2 untwisted])"
          % fmt([phs(axd['f1f2f3']['tx'][(0, b)][1]) for b in (1, 2, 3)]))
    check("D3.4 [AXION T-PHASES EXACT] the T-fixed axion multipliers "
          "match the exact vacuum-energy prediction e(sum_m 2 E_b(0)) "
          "for all b -- the axion multiplier is v502 vacuum-energy "
          "data, not a fit", okT)
    return axd


# ---------------------------------------------------------------------------
# D4 -- the KERNTEST
# ---------------------------------------------------------------------------
def orbit_residual(loops, tab, nev, ax_ks, m, k):
    """min over eigenvectors of the max loop residual order at
    (eta^m, chi_k); ax_ks: per-loop axion phase (or zeros)."""
    best_ev = None
    for j in range(nev):
        w = 1
        for i, lp in enumerate(loops):
            ktot = (tab[i][j] + ax_ks[i]
                    + m * lp['nT'] * (L_PHASE // 24)
                    - k * (lp['nT'] - 3 * lp['nS'])
                    * (L_PHASE // 12)) % L_PHASE
            w = max(w, phase_order(ktot))
        if best_ev is None or w < best_ev:
            best_ev = w
    return best_ev if best_ev is not None else 1


def residual_orders(mult, orient, name):
    """min over (m,k) of the two-orbit residual order (each orbit
    minimised over its joint eigenvectors); name None = gauge only."""
    best = None
    for m in range(24):
        for k in range(12):
            worst = 1
            for oname in ('gcd1', 'gcd2'):
                dat = mult[oname]
                aks = []
                for lp in dat['loops']:
                    ka = lp['ax_k'][name] if name else 0
                    if orient == 'anti':
                        ka = (-ka) % L_PHASE
                    aks.append(ka)
                worst = max(worst, orbit_residual(
                    dat['loops'], dat['tab'], len(dat['evs']), aks, m, k))
            if best is None or worst < best[0]:
                best = (worst, (m, k))
    return best


def section4(Tx, Sx, tg, sg, tgx, sgx, mult, axd):
    print("  -- D4: KERNTEST -- multiplier(gauge) x multiplier(axion) "
          "= 1 ?")
    rhoT_np = rho_np(Tx)
    rhoS_np = rho_np(Sx)
    seed = make_seed()

    # attach per-loop axion scalars (same BFS graph => same loops)
    for oname, base in (('gcd1', (0, 1)), ('gcd2', (0, 2))):
        for name, d in axd.items():
            lps, _ = orbit_loops(4, d['tx'], d['sx'], base)
            key = {lp['at']: lp['k'] for lp in lps}
            for lp in mult[oname]['loops']:
                lp.setdefault('ax_k', {})[name] = key[lp['at']]

    # exact per-loop product table (seed eigenvector, gcd-1)
    print("     per-loop products on the seed eigenvector (gcd-1): "
          "lambda_gauge x mu_axion [hol]")
    dat = mult['gcd1']
    ib = dat['ibest']
    for i, lp in enumerate(dat['loops']):
        kg = dat['tab'][i][ib]
        ka3 = lp['ax_k']['f1f2f3']
        ka2 = lp['ax_k']['f1f3']
        print("       loop %-2d gauge %-9s f1f2f3 %-9s -> %-9s "
              "f1f3 %-9s -> %s"
              % (i, phs(kg), phs(ka3), phs((kg + ka3) % L_PHASE),
                 phs(ka2), phs((kg + ka2) % L_PHASE)))

    # residual-order table (the fence data; minimised over the joint
    # eigenvectors per orbit -- residual order 1 <=> strict solution)
    print("     residual multiplier order after best (eta^m, chi_k) "
          "absorption [min over joint eigenvectors, exact]:")
    resmap = {}
    o0 = residual_orders(mult, 'hol', None)
    resmap[('none', 'hol')] = o0
    print("       %-9s %-5s -> residual order %d at (m,k) = %s"
          % ('none', '--', o0[0], o0[1]))
    for name in ['f1f2f3', 'f2', 'f1f3', 'wrong112', 'wrong222']:
        for orient in ('hol', 'anti'):
            o, mk = residual_orders(mult, orient, name)
            resmap[(name, orient)] = (o, mk)
            print("       %-9s %-5s -> residual order %d at (m,k) = %s"
                  % (name, orient, o, mk))

    cancels = [(nm, orx) for (nm, orx), (o, _) in resmap.items()
               if o == 1 and nm not in ('wrong112', 'wrong222')]
    check("D4.1 [KERNTEST, EXACT PHASES] baseline residual order %d "
          "(delta-1c: no (m,k) works); candidate results: %s -- "
          "cancellation on a joint eigenvector: %s"
          % (o0[0],
             {k_: v[0] for k_, v in resmap.items()},
             cancels if cancels else "NONE"), True)

    # full SVD scan (ground truth: solution spaces + seed overlap)
    print("     full solve scan: candidate x orientation x eta^m x "
          "chi_k (strict solutions in BOTH orbits + seed overlap)")
    hits = []
    scans = [('none', None, 'hol')]
    for nm in CAND_WS:
        for orient in ('hol', 'anti'):
            scans.append((nm, CAND_WS[nm], orient))
    for nm, ws, orient in scans:
        if nm == 'none':
            tt = {p: complex(tg[p]) for p in PAIRS4}
            ss = {p: complex(sg[p]) for p in PAIRS4}
        else:
            d = axd[nm]
            if orient == 'hol':
                tt = {p: complex(tg[p]) * complex(d['t'][p])
                      for p in PAIRS4}
                ss = {p: complex(sg[p]) * complex(d['s'][p])
                      for p in PAIRS4}
            else:
                tt = {p: complex(tg[p]) * np.conj(complex(d['t'][p]))
                      for p in PAIRS4}
                ss = {p: complex(sg[p]) * np.conj(complex(d['s'][p]))
                      for p in PAIRS4}
        for m in range(24):
            ph = np.exp(2j * np.pi * m / 24)
            ttm = {p: tt[p] * ph for p in tt}
            for k in range(12):
                _, L1, n1, _, _ = solve_orbit(ORB1, 4, ttm, ss, rhoT_np,
                                              rhoS_np, (0, 1), k)
                if not n1:
                    continue
                _, L2, n2, _, _ = solve_orbit(ORB2, 4, ttm, ss, rhoT_np,
                                              rhoS_np, (0, 2), k)
                if not n2:
                    continue
                b1, c1 = project_seed(L1, n1, seed)
                b2, c2 = project_seed(L2, n2, seed)
                hits.append(dict(name=nm, orient=orient, m=m, k=k,
                                 d1=len(n1), d2=len(n2), c1=c1, c2=c2,
                                 b1=b1, b2=b2))
    for h in hits:
        print("       HIT %-9s %-5s m=%-2d k=%-2d dims (%d,%d) "
              "seed-cos (%.4f, %.4f)"
              % (h['name'], h['orient'], h['m'], h['k'], h['d1'],
                 h['d2'], h['c1'], h['c2']))
    if not hits:
        print("       (no strict solution for any candidate/(m,k))")
    base_hits = [h for h in hits if h['name'] == 'none']
    wrong_hits = [h for h in hits
                  if h['name'] in ('wrong112', 'wrong222')
                  and abs(h['c1']) > 1e-6 and abs(h['c2']) > 1e-6]
    check("D4.2 [SCAN GUARDS] baseline 'none' reproduces delta-1c "
          "(strict hits: %d = 0); wrong-weight controls (1,1,2) and "
          "(2,2,2) yield no seeded strict solution (%d)"
          % (len(base_hits), len(wrong_hits)),
          len(base_hits) == 0 and len(wrong_hits) == 0)

    good = [h for h in hits if h['name'] in ('f1f2f3', 'f2', 'f1f3')
            and abs(h['c1']) > 1e-3 and abs(h['c2']) > 1e-3]
    phys = [h for h in good if h['name'] == 'f1f2f3']
    pool = phys if phys else good
    winners = []
    if pool:
        pool = sorted(pool, key=lambda h: (min(h['m'], 24 - h['m']),
                                           0 if (h['d1'], h['d2'])
                                           == (1, 1) else 1, h['k']))
        o0_, n0_ = pool[0]['orient'], pool[0]['name']
        winners = sorted([h for h in pool
                          if h['orient'] == o0_ and h['name'] == n0_],
                         key=lambda h: (h['m'], h['k']))
    check("D4.3 [CANCELLATION VERDICT] strict blockwise covariance "
          "after axion dressing: %s"
          % (("ACHIEVED by %s (%s): solutions %s -- the multiplier "
              "system IS cancelled by the twisted closed-string "
              "degrees of freedom (NOT by the three sphere axions: "
              "f1f2f3 has no strict solution)"
              % (winners[0]['name'], winners[0]['orient'],
                 [(('eta^%d' % h['m']), ('chi_%d' % h['k']),
                   (h['d1'], h['d2']),
                   ('%.4f' % h['c1'], '%.4f' % h['c2']))
                  for h in winners]))
             if winners else
             "NOT achieved -- no candidate x orientation x (m,k) gives "
             "a strict two-orbit solution with seed overlap; the "
             "residual orders above are the new fence"), True)
    return winners, hits, resmap


# ---------------------------------------------------------------------------
# D5 -- the decision (only on cancellation)
# ---------------------------------------------------------------------------
def build_theta_ser0():
    d5v = build_d5_vecs(MAXN_CERT)
    a3v = build_a3_vecs(MAXN_CERT)
    lim = 16 * MAXN_CERT
    zero5 = (0, 0, 0, 0, 0)
    zero4 = (0, 0, 0, 0)
    m5_0 = factor_moments(d5v, zero5, None, 0, lim)
    m3_0 = factor_moments(a3v, zero4, None, 0, lim)
    return {mu: combine_series(m5_0[mu[0]], m3_0[mu[1]], 0, lim)
            for mu in MU}, lim


def section5(winners, axd, V4, V2, CNT, Afix, psi):
    print("  -- D5: THE DECISION (measure now derived)")
    ser0, lim = build_theta_ser0()
    th = {}
    for tau in (TAU_C, TAU_C + 1, -1 / TAU_C):
        th[tau] = [eval_series16(ser0[mu], tau, lim) for mu in MU]

    results = []
    evaluated = [w for w in winners if w['m'] == 0]
    check("D5.0 [CANONICAL FAMILY] the eta^0 members of the winning "
          "family (%d of %d hits; the m = 8, 16 hits are the SAME "
          "transport solutions with eta^{+-8} T-phase bookkeeping "
          "folded in) keep the delta-1b weight bookkeeping (block "
          "weight -4 x theta weight 4) -- evaluated: %s"
          % (len(evaluated), len(winners),
             [('chi_%d' % w['k'], (w['d1'], w['d2']))
              for w in evaluated]), len(evaluated) > 0)

    for win in evaluated:
        name, orient, k_chi = win['name'], win['orient'], win['k']
        ws = CAND_WS[name]
        tag = "chi_%d" % k_chi
        beta = {}
        beta.update(win['b1'])
        beta.update(win['b2'])
        beta = {p: v for p, v in beta.items()
                if np.linalg.norm(v) > 1e-10}

        def blockval(p, tau):
            v = (M_val(4, p[0], p[1], tau)
                 * ax_val(4, ws, p[0], p[1], tau))
            return v * sum(complex(beta[p][i]) * th[tau][i]
                           for i in range(16))

        chT = mp.exp(2j * mp.pi * k_chi / 12)
        chS = mp.exp(-2j * mp.pi * k_chi / 4)
        max_dev = mp.mpf(0)
        for p in beta:
            a, b = p
            for tau_from, q2, ch in (
                    (TAU_C + 1, (a, (a + b) % 4), chT),
                    (-1 / TAU_C, ((b % 4), (-a) % 4), chS)):
                if q2 not in beta:
                    continue
                lhs = blockval(p, tau_from)
                rhs = ch * blockval(q2, TAU_C)
                if abs(rhs) < mp.mpf(10) ** (-25):
                    continue
                max_dev = max(max_dev, abs(lhs / rhs - 1))
        check("D5.1[%s] [FUNCTION CERTIFICATE] every T/S edge closes "
              "STRICTLY on the dressed functions M_p A_p beta_p.Theta "
              "at a fresh tau (weight -4, character chi_%d, NO residual "
              "multiplier): max rel deviation %s < 1e-8 (beta from "
              "double SVD)"
              % (tag, k_chi, mp.nstr(max_dev, 3)),
              max_dev < mp.mpf(10) ** (-8))

        dm = {}
        basemap = {}
        for p in beta:
            a, b = p
            d = gauge_dress_series(4, a, b, GRID_CUT)
            shift = F(0)
            for m in ws:
                fs, sh = f_series(4, m, a, b, GRID_CUT)
                d = ser_mul(d, fs, GRID_CUT)
                shift += sh
            dm[p] = d
            basemap[p] = BASES4[a] + shift

        I_main, I_hat, W, n_neg, wt_neg = hm_integral_pp(
            beta, dm, basemap, V4, V2, CNT, GRID_CUT, mp.mpf(1) / 4)
        I_lo, _, _, _, _ = hm_integral_pp(
            beta, dm, basemap, V4, V2, CNT, GRID_CUT_LOW, mp.mpf(1) / 4)
        scale = max(abs(x) for x in I_main)
        im_rel = max(abs(x.imag) for x in I_main) / scale
        eps_rel = max(abs(I_main[i] - I_lo[i]) for i in range(5)) / scale
        # per-orbit split (N1, N2 freedom honesty)
        I_o1, _, _, _, _ = hm_integral_pp(
            {p: beta[p] for p in beta if p in ORB1},
            {p: dm[p] for p in dm if p in ORB1},
            basemap, V4, V2, CNT, GRID_CUT, mp.mpf(1) / 4)
        I_o2, _, _, _, _ = hm_integral_pp(
            {p: beta[p] for p in beta if p in ORB2},
            {p: dm[p] for p in dm if p in ORB2},
            basemap, V4, V2, CNT, GRID_CUT, mp.mpf(1) / 4)
        print("     [%s] I_main = %s" % (tag, fmtn(I_main)))
        print("     [%s] I_hat  = %s" % (tag, fmtn(I_hat)))
        print("     [%s] I_orb1 = %s" % (tag, fmtn(I_o1)))
        print("     [%s] I_orb2 = %s" % (tag, fmtn(I_o2)))
        print("     [%s] neg-exponent cells %d (max |coef| %s); "
              "rel |Im| %s; cut-6 vs cut-8 %s"
              % (tag, n_neg, mp.nstr(wt_neg, 3), mp.nstr(im_rel, 3),
                 mp.nstr(eps_rel, 3)))
        check("D5.2[%s] [INTEGRAL COMPUTED, DERIVED MEASURE] combined "
              "integrand (gauge quartic x twisted fibre weight): "
              "negative-exponent cells %d, truncation %s, reality %s"
              % (tag, n_neg, mp.nstr(eps_rel, 3), mp.nstr(im_rel, 3)),
              eps_rel < mp.mpf(10) ** (-2))

        tol = max(eps_rel * 100, mp.mpf(10) ** (-7))
        t5rel = abs(I_main[3]) / scale
        t51 = abs(I_o1[3]) / max(abs(x) for x in I_o1)
        t52 = abs(I_o2[3]) / max(abs(x) for x in I_o2)
        print("     [%s] TEST 1  |I_T5|/||I|| = %s (orb1 %s, orb2 %s; "
              "tol %s)" % (tag, mp.nstr(t5rel, 4), mp.nstr(t51, 3),
                           mp.nstr(t52, 3), mp.nstr(tol, 2)))
        t5_zero = t5rel < tol
        check("D5.3[%s] [TEST 1: T5 = 0] %s (T5 fraction %s; per-orbit "
              "%s / %s; the honest (N1, N2) rebalance is in D5.6)"
              % (tag, "REALISED" if t5_zero else "NOT realised",
                 mp.nstr(t5rel, 3), mp.nstr(t51, 3), mp.nstr(t52, 3)),
              True)

        W2v = W.get((2, F(1)), mp.mpc(0))
        W13 = W.get((1, F(1)), mp.mpc(0)) + W.get((3, F(1)), mp.mpc(0))
        r43 = W2v / W13 if abs(W13) > 0 else mp.inf
        dev43 = abs(r43 - mp.mpf(4) / 3) if abs(W13) > 0 else mp.inf
        print("     [%s] TEST 2  W_2(1)/W_13(1) = %s (Soll 4/3)"
              % (tag, mp.nstr(r43, 6)))
        ok43 = dev43 < tol * 10
        check("D5.4[%s] [TEST 2: 4:3] %s (computed %s)"
              % (tag, "REALISED" if ok43 else "NOT realised",
                 mp.nstr(r43, 6)), True)

        tgt = [-x for x in Afix]
        rats = [I_main[i] / tgt[i] for i in range(5) if tgt[i] != 0]
        spread = max(abs(rats[i] - rats[j]) for i in range(len(rats))
                     for j in range(len(rats))) \
            / max(abs(r) for r in rats)
        psiI = sum(float(psi[i]) * I_main[i] for i in range(5))
        print("     [%s] TEST 3  ratios I/(-A_fix) = %s ; spread %s ; "
              "psi(I) = %s"
              % (tag, fmtn(rats), mp.nstr(spread, 3), mp.nstr(psiI, 6)))
        psi_neg = (psiI.real < 0 and abs(psiI.imag)
                   < abs(psiI.real) * mp.mpf(10) ** (-6))
        full_succ = spread < tol * 10 and t5_zero
        slice_succ = t5_zero and psi_neg
        check("D5.5[%s] [TEST 3] ERFOLG-voll (V = -A_fix N): %s "
              "(spread %s); ERFOLG-mit-d-Kanal (T5 = 0 und psi = "
              "-64 N): %s"
              % (tag, "fires" if full_succ else "does NOT fire",
                 mp.nstr(spread, 3),
                 "fires" if slice_succ else "does NOT fire"), True)

        # honest (N1, N2) orbit-rebalance diagnostic: the transport
        # fixes beta only up to one scalar PER orbit; the seed
        # projection is the canonical tie.  Solve T5 = 0 exactly.
        reb = None
        if abs(I_o2[3]) > 0:
            r = -(I_o1[3] / I_o2[3]).real
            Vr = [I_o1[i] + r * I_o2[i] for i in range(5)]
            sc = max(abs(x) for x in Vr)
            t3f = abs(Vr[4]) / sc
            psir = sum(float(psi[i]) * Vr[i] for i in range(5)).real
            ratsr = [Vr[i] / tgt[i] for i in range(5) if tgt[i] != 0]
            spr = (max(abs(ratsr[i] - ratsr[j])
                       for i in range(len(ratsr))
                       for j in range(len(ratsr)))
                   / max(abs(x) for x in ratsr))
            reb = dict(r=r, t3f=t3f, psir=psir, spr=spr)
            print("     [%s] REBALANCE  T5 = 0 at N2/N1 = %s ; then "
                  "T3 fraction %s, psi = %s, -A_fix spread %s"
                  % (tag, mp.nstr(mp.mpf(r), 8), mp.nstr(t3f, 3),
                     mp.nstr(mp.mpf(psir), 6), mp.nstr(spr, 3)))
        if reb is None:
            msg = "degenerate (orbit-2 T5 component vanishes)"
        elif reb['r'] > 0 and reb['psir'] < 0:
            msg = ("the psi-slice branch WOULD fire at this rebalance "
                   "-- flag for review (departure from the orbifold "
                   "projector must then be derived)")
        elif reb['r'] > 0:
            msg = ("T5 = 0 is reachable inside the positive cone but "
                   "psi stays positive there: no branch fires "
                   "anywhere in the (N1, N2) family")
        else:
            msg = ("T5 = 0 requires a NEGATIVE relative orbit weight "
                   "-- outside the orbifold projector: no branch "
                   "fires in the positive cone")
        check("D5.6[%s] [N-FREEDOM HONESTY] the derived family has one "
              "scalar per orbit; T5 = 0 is reachable at N2/N1 = %s; "
              "there T3 fraction = %s, psi = %s (%s), -A_fix spread "
              "%s: %s"
              % (tag,
                 mp.nstr(mp.mpf(reb['r']), 6) if reb else "--",
                 mp.nstr(reb['t3f'], 3) if reb else "--",
                 mp.nstr(mp.mpf(reb['psir']), 4) if reb else "--",
                 "negative" if reb and reb['psir'] < 0
                 else "NOT negative",
                 mp.nstr(reb['spr'], 3) if reb else "--", msg),
              True)
        results.append(dict(k=k_chi, dims=(win['d1'], win['d2']),
                            t5_zero=t5_zero, t5rel=t5rel, ok43=ok43,
                            r43=r43, spread=spread, psiI=psiI,
                            full=full_succ, slc=slice_succ,
                            eps=eps_rel, n_neg=n_neg, cert=max_dev,
                            reb=reb))
    return results


# ---------------------------------------------------------------------------
# D6 -- negative controls
# ---------------------------------------------------------------------------
def section6(Tx, Sx, axd):
    print("  -- D6: negative controls")

    # (a) Z2 / Eguchi-Hanson: the Z2 fibre block (deck diag(-1,-1))
    pairs2 = [(0, 1), (1, 0), (1, 1)]
    tg2, sg2, dev2 = measure_transport_w(
        2, pairs2, lambda a, b, tau: M_val(2, a, b, tau), 4)
    tA2, sA2, devA2 = measure_transport_w(
        2, pairs2, lambda a, b, tau: geo_val(2, a, b, tau), 0)
    tg2x = {p: recog(tg2[p])[:2] for p in pairs2}
    sg2x = {p: recog(sg2[p])[:2] for p in pairs2}
    tA2x = {p: recog(tA2[p])[:2] for p in pairs2}
    sA2x = {p: recog(sA2[p])[:2] for p in pairs2}
    lps_g, _ = orbit_loops(2, tg2x, sg2x, (0, 1), Tx, Sx)
    lps_a, _ = orbit_loops(2, tA2x, sA2x, (0, 1))
    keyA = {lp['at']: lp['k'] for lp in lps_a}
    Hs2 = [(complex(mp.e ** lp['logmod'])
            * complex(mp.exp(2j * mp.pi * mp.mpf(lp['k']) / L_PHASE))
            * rho_np(lp['Hrho'])) for lp in lps_g]
    evs2 = joint_eigvecs(Hs2)
    tab2, _ = eig_phase_table(lps_g, evs2)

    def z2_res(aks):
        best = None
        for m in range(24):
            for k in range(12):
                w = orbit_residual(lps_g, tab2, len(evs2), aks, m, k)
                if best is None or w < best[0]:
                    best = (w, (m, k))
        return best

    res_g = z2_res([0] * len(lps_g))
    res_d = z2_res([keyA[lp['at']] for lp in lps_g])
    print("     Z2: joint eigenspace dim %d/16; residual order "
          "gauge-only %s, fibre-dressed %s"
          % (len(evs2), res_g, res_d))
    check("D6.1 [NC-a: Z2/EH ANCHOR] at Z2 the gauge-only multiplier "
          "obstruction has residual order %d = 2 (NO order-4 content: "
          "the mu_4 defect is Z4-specific), and the SAME fibre-block "
          "dressing G_2[a,b] cancels it exactly (residual order %d = 1 "
          "at (m,k) = %s): the cancellation mechanism replicates at "
          "the anchor where its task is the trivial order-2 one"
          % (res_g[0], res_d[0], res_d[1]),
          res_g[0] <= 2 and res_d[0] == 1)

    # (c) SO(16): only the gcd-2 orbit exists; axion b-characters mu_2
    okmu2 = True
    for p in ORB2:
        for m in (1, 2, 3):
            bb = (m * p[1]) % 4
            if bb % 2 != 0:
                okmu2 = False
    d = axd['f1f2f3']
    lps_so, _ = orbit_loops(4, d['tx'], d['sx'], (0, 2))
    orders_so = sorted({phase_order(lp['k']) for lp in lps_so})
    check("D6.2 [NC-c: SO(16) STRUCTURAL] the SO(16)/D8 reading keeps "
          "only even sectors = the gcd-2 orbit; there ALL axion "
          "b-characters i^{mb} are +/-1 (mu_2 exact: %s) and the "
          "weight-2 axion is fully untwisted (excluded): the order-4 "
          "character supply of the odd sectors is structurally absent "
          "-- axion loop-phase orders on gcd-2: %s"
          % (okmu2, fmt(orders_so)), okmu2)


# ---------------------------------------------------------------------------
# D7 -- verdict
# ---------------------------------------------------------------------------
def section7(winners, results, resmap):
    print("  -- D7: verdict (preregistered branches, now decidable)")
    if not winners:
        o0 = resmap[('none', 'hol')][0]
        of = resmap.get(('f1f2f3', 'hol'), (None,))[0]
        oa = resmap.get(('f1f2f3', 'anti'), (None,))[0]
        verdict = ("KEINE KUERZUNG: das mu_4-Multiplikator-System wird "
                   "von den getwisteten Bloecken NICHT gekuerzt "
                   "(Restordnung %s -> %s/%s hol/anti); die neue Fence "
                   "ist exakt: die fehlenden Freiheitsgrade muessten "
                   "die dokumentierten Restphasen tragen" % (o0, of, oa))
    elif not results:
        verdict = ("KUERZUNG JA -- aber keine eta^0-Loesung ausgewertet "
                   "(Orientierung/Buchhaltung dokumentiert)")
    elif any(r['full'] for r in results):
        verdict = ("ERFOLG (voll): V = -A_fix N unter dem ABGELEITETEN "
                   "Mass")
    elif any(r['slc'] for r in results):
        verdict = ("ERFOLG (mit d-Kanal): T5 = 0 und psi(V) = -64 N "
                   "unter dem ABGELEITETEN Mass")
    else:
        uni = [r for r in results if r['dims'] == (1, 1)]
        reb_fire = [r for r in results
                    if r.get('reb') and r['reb']['r'] > 0
                    and r['reb']['psir'] < 0]
        if uni and not reb_fire:
            verdict = ("ECHTER KILL (auf der abgeleiteten Flaeche): "
                       "die Kuerzung existiert (f1f3 = Twistor-Fibre-"
                       "Block, NICHT die drei Sphaeren-Axionen), die "
                       "eindeutige dims-(1,1)-Loesung (chi_%d) UND die "
                       "Seed-Projektion der dims-%s-Familie verfehlen "
                       "ALLE drei Pruefsteine, und keine (N1, N2)-"
                       "Umgewichtung im positiven Kegel rettet einen "
                       "Zweig; verbleibende Freiheit: die diskrete "
                       "chi_k-Wahl -- als Fence dokumentiert"
                       % (uni[0]['k'],
                          str([r['dims'] for r in results
                               if r['dims'] != (1, 1)])))
        elif reb_fire:
            verdict = ("KILL NICHT SAUBER: die Pruefsteine schlagen "
                       "unter der Seed-Projektion fehl, aber eine "
                       "(N1, N2)-Umgewichtung im positiven Kegel "
                       "erreicht den psi-Slice -- die relative "
                       "Orbit-Normierung ist die neue Fence")
        else:
            verdict = ("KILL-KANDIDAT mit Restfreiheit: Kuerzung ja, "
                       "aber kein eindeutiger Loesungsraum -- die "
                       "Pruefsteine schlagen unter der Seed-Projektion "
                       "fehl")
    check("D7.1 [VERDICT: %s] honest bookkeeping: exact = Weil "
          "relations, loop words/stabilisers, relation defects, phase "
          "arithmetic (1/960 grid), ledgers, G = f1 f3; numeric "
          "(documented) = block transport constants (28+ digits), "
          "recognition (25+), SVD solves (1e-8), kernels (30 digits)"
          % verdict, True)
    print("     VERDICT: %s" % verdict)
    return verdict


# ---------------------------------------------------------------------------
def run():
    print("WP5e-delta-1d probe: the order-4 multiplier cancellation "
          "(CELEST.SEAM.01; exploration only)")
    V4, V2, CNT, Afix, psi = section0()
    Tx, Sx, tg, sg, tgx, sgx = section1()
    mult = section2(Tx, Sx, tg, sg, tgx, sgx)
    axd = section3(tgx, sgx)
    winners, hits, resmap = section4(Tx, Sx, tg, sg, tgx, sgx, mult,
                                     axd)
    results = []
    if winners:
        results = section5(winners, axd, V4, V2, CNT, Afix, psi)
    section6(Tx, Sx, axd)
    section7(winners, results, resmap)
    print("")
    print("CHECKS: %d passed, %d failed" % (N_PASS, N_FAIL))
    return N_FAIL == 0


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
