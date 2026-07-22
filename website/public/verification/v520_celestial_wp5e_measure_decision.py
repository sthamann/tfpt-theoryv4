"""v520 -- CELEST.WP5E.MEASURE.01: the WP5e BCOV measure question DECIDED
at probe level -- "single-valuedness is derived, the completion reading
wins" (delta-1e + delta-1f consolidated, v518-consolidation style).
Question (the named [O] of v516/v518): which of the two exact, mutually
contradictory measures on PT/Z4 is the true BCOV measure -- (A) the
DECLARED completion reading (v516: unphased sector trace, w_m = 4 h_m,
supplies psi = 64) or (B) the DERIVED chiral measure (v518: multiplier
character chi_4 on Gamma_1(4); all three testers fail)?  Answer:
ERFOLG-A on the decision layer -- single-valuedness of the physical
one-loop lattice factor is DERIVED from two independent constructive
sources (F-independence of the moduli integral + the Quillen/BCOV
conjugate pairing), NOT postulated; with single-valuedness forced, the
exact invariant subspace of the 16-dim Weil system forces the unphased
E4 numerator, and the consistency circle to v516 closes levelwise.

[E] 1. THE INVARIANT SUBSPACE (delta-1e D2): dim_Q {v : rho(T) v = v,
    rho(S) v = v} = 8 = 4 x 2 in the dressed 16-component Weil system
    (exact rational nullspace); EVERY kernel vector lies in the
    Q(zeta_8)-span of {e_H, e_H'} -- the two Lagrangian gluings, both
    theta = E4, level-1 quartic = Q^{(0)} = the unphased trace; strict
    trivial-character solutions at physical weight (m, k) = (0, 0):
    ZERO for every dressing (11 combinations, both orientations).
[E] 2. SOURCE 1 -- THE F-LEMMA (delta-1f A1): the only strict chiral
    families are chi_4 (dims (3,3)) and chi_10 (dims (1,1)), both with
    nontrivial T-character EXACTLY (chi_4(T) = e(1/3), chi_10(T) =
    e(5/6)); the canonical column-matched chi_4 member's total block
    sum obeys G(gamma tau) = chi_4(gamma) G(tau) pointwise (certificate
    3.9e-16 over two fresh tau, nonvacuous |G| >= 59.6); EXACT change
    of variables: int_{gamma F} G dmu = chi_4(gamma) int_F G dmu --
    fundamental-domain independence forces int = 0 for EVERY chiral
    integrand: under TP-1 + TP-2 the chiral route can never source
    psi = 64 -- the v518 route was never a well-defined nonvanishing
    moduli integral (the kill is SHARPENED, its unfolded values are
    convention bookkeeping).
[E] 3. SOURCE 2 -- THE QUILLEN PAIRING (delta-1f A2): the doubled
    hol x antihol transports satisfy |t conj(t) - 1| < 8.3e-40 on all
    15 pairs and both generators (measured unitarity, not constructed);
    |chi_4|^2 = 1 exactly vs one-sided chi_4^2 = e(2/3) != 1 (T-fixed:
    640 != 0 mod 960, squared defects on 15/15 pairs); the doubled
    256-dim Weil system closes STRICTLY at trivial character and
    physical weight (nullspaces (28, 17) >= 11), contains the unphased
    diagonal (~2e-15) AND the physical columns w_b (x) conj(w_b)
    (sigma 4.9e-16 / 8.3e-16); negative control hol (x) hol: EMPTY
    nullspace (0, 0) -- only the conjugate pairing implements
    single-valuedness.
[E] 4. THE CONSISTENCY CLOSURE (delta-1f A3): the forced unphased
    numerator inside the v518 scaffold reproduces sum_m V prop
    (1, 2, 1, 0, 0) = <x,x>^2 EXACTLY on every level n <= 8 (levelwise
    Okubo / 4-design); J-weighted spreads ~5e-41, T5/T3 fractions
    ~7e-42, zero negative-exponent cells; psi(skeleton) = +0.2302 =
    -psi(contact) -- the J-weighted mirror image of psi(A_fix) = +64 /
    psi(contact) = -64; linearity skeleton + contact = unphased at
    4.6e-41: the circle to v516 is CLOSED.
[E] 5. D3 -- THE Z2/EH ANCHOR (delta-1e): only the declared reading
    hits the anchor (9<x,x>^2 = (1/4) x 36<x,x>^2, psi(A_2) = -8,
    scale tooth c = 1/2 = |Z2| h^{A1} unique); ALL THREE derived Z2
    instantiations fail the anchor testers (spreads 1.12 / 0.895 /
    0.516, psi sign wrong).
[E] 6. D1 -- COLUMN CANONICALISATION (delta-1e): the physical AB
    column sum_m i^{bm} e_{(m,m)} is contained EXACTLY in the chi_4
    family (sigma 1.8e-16 / 1.7e-16, one scalar per orbit --
    canonicalising the (N1, N2) freedom); the canonical member STILL
    fails every tester (sharpened kill, counted per the delta-1e
    preregistration).
[E] NEGATIVE CONTROLS: SO(16)/D8 (T5 = 20 / T3 = -40 exact, mu_2-only
    supply), wrong form (|Gauss|^2 = 64 != 16, S^2 = C breaks), wrong
    weight (transport dev 0.78 at exponent 2), shuffled weights
    (T5 = -14 / T3 = 36), planted family detected (1.5e-16), hol (x)
    hol empty.
[C] TYPED PREMISES (the mandatory fence): TP-1 (the twisted one-loop
    contribution is an F-independent moduli-space integral), TP-2
    (it is nonzero -- it must source psi = 64), TP-3 (the v518
    kernel-family weight convention), TP-4 (BCOV F1 is Quillen/
    Ray-Singer: the one-loop factor pairs hol x conj(hol)).
[O] the constructive BCOV derivation of the w_m normalisation itself
    (the residual open item); SEAM.EQUIV.TWISTOR.01 stays Open.

VERDICT: ERFOLG-A per the preregistered delta-1f criteria (both
constructive sources fire independently, the consistency closure
carries, all negative controls behave); the [O] question "which is
the true BCOV measure" is DECIDED at probe level in favour of (A)
under the typed premises TP-1..TP-4.  NO marker moves anywhere.

Status: [E] exact Weil/Q(zeta_8) algebra, exact invariant subspace
(rational nullspace), characters + 1/960 grid arithmetic, ledgers,
completion/contact/psi identities, levelwise 4-design, Z2 anchor
arithmetic, change-of-variables corollary, controls; numeric
(documented) = block transports (28+ digits, grid 25+), SVD solves
and memberships (double, thresholds 1e-8/1e-3), function certificates
at fresh tau (< 1e-8), HM kernels (30+ digits, cut-6 vs cut-8 scan,
negative-cell audit).  Python; Wolfram-mirrored (Weil relations,
invariant-subspace forcing, characters |chi_4|^2 = 1 vs chi_4^2 =
e(2/3), completion/contact/psi arithmetic, Z2 anchor + scale teeth,
levelwise Okubo, so16/wrong-form/shuffle controls); the Harvey-Moore
integrals and SVD memberships are numerical and stay Python-only,
flagged in the .wl mirror.  Discovery provenance:
experiments/tfpt-discovery/
celestial_seam_wp5e_delta1e_bcov_measure_decision_probe.py (28/28),
..._delta1f_single_valuedness_probe.py (23/23) (2026-07-22)."""
import math
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, gcd

import mpmath as mp
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, rankE8

MU4 = N_fam + 1                # 4 = |mu4|, the seam clock order
NCLS = MU4 * MU4               # 16 discriminant classes of D5 (+) A3
L_PHASE = 960
GRID_CUT = F(8)
GRID_CUT_LOW = F(6)
MAXN_LED = 16
MAXN_CERT = 20
BASES4 = {0: F(-1, 2), 1: F(-5, 16), 2: F(-1, 4), 3: F(-5, 16)}
SIGMA3 = [1, 9, 28, 73, 126, 252, 344, 585]
NPROD = 120
TAU_A = mp.mpc(mp.mpf(13) / 100, mp.mpf(51) / 50)
TAU_B = mp.mpc(mp.mpf(-31) / 100, mp.mpf(99) / 100)
TAU_C = mp.mpc(mp.mpf(7) / 100, mp.mpf(101) / 100)
TAU_D = mp.mpc(mp.mpf(-19) / 100, mp.mpf(103) / 100)


def fmt(xs):
    return "(" + ", ".join(str(x) for x in xs) + ")"


def fmtn(xs, nd=6):
    return "(" + ", ".join(mp.nstr(mp.mpf(x) if not isinstance(x, mp.mpc)
                                   else x, nd) for x in xs) + ")"


# ---------------------------------------------------------------------------
# exact Q(zeta_8) arithmetic (delta-1c/1d/1e machinery, verbatim)
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
DIAG_H = [(a, a) for a in range(4)]
ANTI_H = [(0, 0), (1, 3), (2, 2), (3, 1)]


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
# lattice ledgers (delta-1c/1d/1e machinery, verbatim)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# block numerics: gauge M = G/eta^8 and the fibre blocks f_m
# ---------------------------------------------------------------------------
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
    lm = mp.log(abs(z))
    ph = mp.arg(z) / (2 * mp.pi)
    k = int(mp.nint(ph * L_PHASE))
    dev = abs(ph - mp.mpf(k) / L_PHASE)
    return lm, k % L_PHASE, dev


# ---------------------------------------------------------------------------
# contraction solve machinery (generalised to n dims for the doubled system)
# ---------------------------------------------------------------------------
def sl2z_char(k):
    return (np.exp(2j * np.pi * k / 12), np.exp(-2j * np.pi * k / 4))


def solve_orbit(pairs, N, tconst, sconst, rhoT_np, rhoS_np, base, k=0):
    n = rhoT_np.shape[0]
    chT, chS = sl2z_char(k)
    TT = rhoT_np.T
    ST = rhoS_np.T
    Lam = {base: np.eye(n, dtype=complex)}
    queue = [base]
    rows = []
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
    A = np.vstack(rows) if rows else np.zeros((1, n), dtype=complex)
    _, sv, Vh = np.linalg.svd(A)
    sv = list(sv) + [0.0] * (n - len(sv))
    tol = max(sv) * 1e-8 if max(sv) > 0 else 1e-8
    null = [Vh[i].conj() for i in range(n) if sv[i] < tol]
    return sorted(Lam.keys()), Lam, null, sv


def member_test(Lam, null, targets):
    """stacked homogeneous system [Lam[p] V | -t_p] u = 0 with ONE
    shared scalar; returns (sigma_min/sigma_max, |c|/||u||, u, V)."""
    if not null:
        return None
    V = np.array(null).T
    rows = []
    for p, t in targets.items():
        A = Lam[p] @ V
        rows.append(np.hstack([A, -t.reshape(len(t), 1)]))
    Mst = np.vstack(rows)
    _, svs, Vh = np.linalg.svd(Mst)
    ratio = svs[-1] / svs[0]
    u = Vh[-1].conj()
    c_rel = abs(u[-1]) / np.linalg.norm(u)
    return ratio, c_rel, u, V


def ray_residual(Lam, null, p, t):
    """per-pair least-squares containment residual of target t in the
    family column space at pair p."""
    if not null:
        return None
    V = np.array(null).T
    A = Lam[p] @ V
    x, *_ = np.linalg.lstsq(A, t, rcond=None)
    return float(np.linalg.norm(A @ x - t) / np.linalg.norm(t))


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


def dressed_consts(tg, sg, d, orient, pairs):
    if orient == 'hol':
        tt = {p: complex(tg[p]) * complex(d['t'][p]) for p in pairs}
        ss = {p: complex(sg[p]) * complex(d['s'][p]) for p in pairs}
    else:
        tt = {p: complex(tg[p]) * np.conj(complex(d['t'][p]))
              for p in pairs}
        ss = {p: complex(sg[p]) * np.conj(complex(d['s'][p]))
              for p in pairs}
    return tt, ss


# ---------------------------------------------------------------------------
# exact invariant subspace of the 16-dim Weil representation (delta-1e D2)
# ---------------------------------------------------------------------------
def mulmat_q8(u):
    M = [[F(0)] * 4 for _ in range(4)]
    for i in range(4):
        if u[i] == 0:
            continue
        for j in range(4):
            k = i + j
            if k < 4:
                M[k][j] += u[i]
            else:
                M[k - 4][j] -= u[i]
    return M


def invariant_subspace(Tx, Sx):
    rows = []
    for Op in (Tx, Sx):
        for i in range(16):
            block = [[sp.Rational(0)] * 64 for _ in range(4)]
            for j in range(16):
                Mm = mulmat_q8(Op[i][j])
                for r in range(4):
                    for cc in range(4):
                        if Mm[r][cc]:
                            block[r][4 * j + cc] += sp.Rational(
                                Mm[r][cc].numerator, Mm[r][cc].denominator)
            for r in range(4):
                block[r][4 * i + r] -= 1
            rows.extend(block)
    A = sp.Matrix(rows)
    return A.nullspace()


def in_lagrangian_span(vec64):
    comp = [tuple(F(sp.Rational(vec64[4 * j + c]).p,
                    sp.Rational(vec64[4 * j + c]).q) for c in range(4))
            for j in range(16)]
    alpha = comp[IDX[(1, 1)]]
    beta = comp[IDX[(1, 3)]]
    for mu in MU:
        j = IDX[mu]
        in_h = mu in DIAG_H
        in_hp = mu in ANTI_H
        if mu == (0, 0):
            want = z8_add(alpha, beta)
        elif in_h and in_hp:
            want = z8_add(alpha, beta)
        elif in_h:
            want = alpha
        elif in_hp:
            want = beta
        else:
            want = Z8_ZERO
        if comp[j] != want:
            return False
    return True


# ---------------------------------------------------------------------------
# exact dressing series + fundamental-domain kernel J (delta-1b/1d/1e)
# ---------------------------------------------------------------------------
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


def build_dress(beta_keys, ws):
    dm, basemap = {}, {}
    for p in beta_keys:
        a, b = p
        d = gauge_dress_series(4, a, b, GRID_CUT)
        shift = F(0)
        for m in ws:
            fs, sh = f_series(4, m, a, b, GRID_CUT)
            d = ser_mul(d, fs, GRID_CUT)
            shift += sh
        dm[p] = d
        basemap[p] = BASES4[a] + shift
    return dm, basemap


def run_integral(beta, ws, V4, V2, CNT, weight):
    dm, basemap = build_dress(list(beta.keys()), ws)
    I_main, I_hat, W, n_neg, wt_neg = hm_integral_pp(
        beta, dm, basemap, V4, V2, CNT, GRID_CUT, weight)
    dml = {p: {e: v for e, v in dm[p].items() if e <= GRID_CUT_LOW}
           for p in dm}
    I_lo, _, _, _, _ = hm_integral_pp(
        beta, dml, basemap, V4, V2, CNT, GRID_CUT_LOW, weight)
    scale = max(abs(x) for x in I_main)
    im_rel = max(abs(x.imag) for x in I_main) / scale if scale > 0 else 0
    eps_rel = (max(abs(I_main[i] - I_lo[i]) for i in range(5)) / scale
               if scale > 0 else 0)
    return I_main, W, n_neg, wt_neg, im_rel, eps_rel


def spread_vs(I_main, tgt):
    scale = max(abs(x) for x in I_main)
    rats = [I_main[i] / tgt[i] for i in range(5) if tgt[i] != 0]
    spread = (max(abs(rats[i] - rats[j]) for i in range(len(rats))
                  for j in range(len(rats)))
              / max(abs(r) for r in rats))
    zrel = max([abs(I_main[i]) / scale for i in range(5) if tgt[i] == 0]
               + [mp.mpf(0)])
    return spread, zrel


def function_certificate(beta, ws, k_chi, th):
    chT = mp.exp(2j * mp.pi * k_chi / 12)
    chS = mp.exp(-2j * mp.pi * k_chi / 4)

    def blockval(p, tau):
        v = (M_val(4, p[0], p[1], tau)
             * ax_val(4, ws, p[0], p[1], tau))
        return v * sum(complex(beta[p][i]) * th[tau][i]
                       for i in range(16))

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
    return max_dev


PSIV = [F(3), F(-1), F(-1), F(0), F(-1, 4)]


def psi_of(v):
    return sum(float(PSIV[i]) * v[i] for i in range(5))


# ---------------------------------------------------------------------------
# pair sets, candidates, columns, targets
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

QTAB = {0: [12, 0, 6, 4, 8], 1: [12, 24, 0, -8, 16],
        2: [0, 24, 30, 12, -40], 3: [12, 24, 0, -8, 16]}
DETS = {1: 2, 2: 4, 3: 2}
AFIX = [9, -30, -15, 0, 32]
A2VEC = [-3, -6, 9, 8, -16]
Q1VEC = QTAB[1]
CONTACT_A = [36, 120, 60, 0, -32]
OKUBO = [F(1), F(2), F(1), F(0), F(0)]
ZERO5 = [F(0)] * 5
CONTAIN_TOL = 1e-8
ROBUST_TOL = 1e-3

E00 = np.zeros(16, dtype=complex)
E00[IDX[(0, 0)]] = 1.0


def w_col(b, shift=0):
    v = np.zeros(16, dtype=complex)
    for m in range(4):
        v[IDX[(m, m)]] = 1j ** (((b * m) + shift * m) % 4)
    return v


def diag_unph():
    v = np.zeros(16, dtype=complex)
    for m in range(4):
        v[IDX[(m, m)]] = 1.0
    return v


def col_contact(j):
    v = np.zeros(16, dtype=complex)
    for m in range(4):
        v[IDX[(m, m)]] = 1.0 - 1j ** ((j * m) % 4)
    return v


COLUMN_MODELS = {
    'diag': {1: E00, 3: E00, 2: E00},
    'spread': {1: w_col(1), 3: w_col(3), 2: w_col(2)},
}
WRONG_MODEL = {1: w_col(1, shift=1), 3: w_col(3, shift=1),
               2: w_col(2, shift=1)}


def make_seed2():
    seed = {}
    for p in ORB2:
        v = np.zeros(16, dtype=complex)
        v[IDX[(p[0] % 4, p[0] % 4)]] = 1j ** ((p[0] * p[1]) % 4)
        seed[p] = v
    return seed


# ---------------------------------------------------------------------------
# S0 -- exact foundations: roots, ledgers, targets, Z2 anchor, Weil, chars
# ---------------------------------------------------------------------------
def section0(V4, CNT):
    print("  -- S0: exact foundations (roots, ledgers, targets, Weil)")
    roots = build_glue_roots()
    counts = [sum(1 for c in roots.values() if c == m) for m in range(4)]
    check("S0.1 [ROOTS] 240 roots, all norm 2, class split %s = "
          "(52, 64, 60, 64); 16 = |mu4|^2 discriminant classes "
          "(v492/v505 replication)" % fmt(counts),
          len(roots) == 240 and counts == [52, 64, 60, 64]
          and all(sum(x * x for x in r) == 2 for r in roots)
          and NCLS == 16 and MU4 == 4 and rankE8 == 8)

    ok_q = all(V4[(a, a)].get(F(1)) == QTAB[a] for a in range(4))
    tots = [sum(CNT[(a, a)].get(F(n), 0) for a in range(4))
            for n in range(1, 9)]
    tots_anti = [sum(CNT[m].get(F(n), 0) for m in ANTI_H)
                 for n in range(1, 9)]
    check("S0.2 [16-CLASS LEDGER] diagonal slice = quartic ledger "
          "(V_{(a,a),1} = Q_a exactly); diagonal AND anti-diagonal "
          "counts = 240 sigma_3(n) for n <= 8 (both Lagrangian "
          "gluings are E4; delta-1c/v518 replication)",
          ok_q and tots == [240 * s for s in SIGMA3]
          and tots_anti == [240 * s for s in SIGMA3])

    I = sp.I
    R = sp.Rational
    Qv = {m: [R(x) for x in QTAB[m]] for m in range(4)}
    Qtw = {j: [sp.nsimplify(sp.expand(
        sum(I ** (j * m) * Qv[m][i] for m in range(4))))
        for i in range(5)] for j in range(4)}
    h = [R(m * (4 - m), 8) for m in range(4)]
    w = [sp.nsimplify(sp.expand(
        sum((1 - I ** (j * m)) / DETS[j] for j in (1, 2, 3))))
        for m in range(4)]
    Afix = [sp.nsimplify(sum(Qtw[j][i] / DETS[j] for j in (1, 2, 3)))
            for i in range(5)]
    contact = {j: [sp.nsimplify((Qtw[0][i] - Qtw[j][i]) / DETS[j])
                   for i in range(5)] for j in (1, 2, 3)}
    total = [sum(contact[j][i] for j in (1, 2, 3)) for i in range(5)]
    sums = {j: [sp.nsimplify(Qtw[j][i] / DETS[j] + contact[j][i])
                for i in range(5)] for j in (1, 2, 3)}
    psiS = lambda v: sp.nsimplify(3 * v[0] - v[1] - v[2] - R(1, 4) * v[4])
    check("S0.3 [A-CORE, EXACT] Q^{(0)} = %s = (36,72,36,0,0); A_fix = "
          "%s = (9,-30,-15,0,32); completion weights w_m = %s = "
          "(0, 3/2, 2, 3/2) = 4 h_m, h_2 : h_1 = %s = 4:3; contact "
          "total = %s = (36,120,60,0,-32); per-sector perfect squares "
          "(18/9/18)<x,x>^2; psi(A_fix) = %s = +64, psi(contact) = %s "
          "= -64 (v516 replication)"
          % (fmt(Qtw[0]), fmt(Afix), fmt(w), h[2] / h[1], fmt(total),
             psiS(Afix), psiS(total)),
          Qtw[0] == [36, 72, 36, 0, 0] and Afix == AFIX
          and w == [0, R(3, 2), 2, R(3, 2)]
          and all(w[m] == 4 * h[m] for m in range(4))
          and h[2] / h[1] == R(4, 3)
          and total == CONTACT_A
          and sums[1] == [18, 36, 18, 0, 0]
          and sums[2] == [9, 18, 9, 0, 0]
          and sums[3] == [18, 36, 18, 0, 0]
          and psiS(Afix) == 64 and psiS(total) == -64)

    A2 = [sp.nsimplify(Qtw[2][i] / 4) for i in range(5)]
    contact2 = [sp.nsimplify(R(1, 2) * (Qv[1][i] + Qv[3][i]))
                for i in range(5)]
    tot2 = [A2[i] + contact2[i] for i in range(5)]
    psiA2 = psiS(A2)
    leftovers = {}
    for c in (F(1, 4), F(1, 2), F(1), F(2)):
        cc = sp.Rational(c.numerator, c.denominator)
        t5l = sp.nsimplify(A2[3] + cc * (Qv[1][3] + Qv[3][3]))
        t3l = sp.nsimplify(A2[4] + cc * (Qv[1][4] + Qv[3][4]))
        leftovers[c] = (t5l, t3l)
    ok_scale = (leftovers[F(1, 2)] == (0, 0)
                and all(leftovers[c] != (0, 0)
                        for c in (F(1, 4), F(1), F(2))))
    check("S0.4 [Z2 ANCHOR TARGETS, EXACT] A_2 = Q^{(g^2)}/4 = %s = "
          "(-3,-6,9,8,-16); contact_2 = (1/2)(Q_1 + Q_3) = Q_1; "
          "A_2 + contact_2 = %s = 9<x,x>^2 = (1/4) x 36<x,x>^2, "
          "coupling scale 2 = |Z2| (weight 1/2 = 2 x h^{A1}); "
          "psi(A_2) = %s = -8; SCALE TEETH: only c = 1/2 clears both "
          "leftovers %s"
          % (fmt(A2), fmt(tot2), psiA2,
             str({str(k): fmt(v) for k, v in leftovers.items()})),
          A2 == A2VEC and contact2 == Q1VEC
          and tot2 == [9, 18, 9, 0, 0] and psiA2 == -8 and ok_scale)

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
    eH = [Z8_ONE if MU[i] in DIAG_H else Z8_ZERO for i in range(n)]
    eHp = [Z8_ONE if MU[i] in ANTI_H else Z8_ZERO for i in range(n)]
    SeH = [sum_z8([z8_mul(Sx[i][j], eH[j]) for j in range(n)])
           for i in range(n)]
    TeH = [z8_mul(Tx[i][i], eH[i]) for i in range(n)]
    SeHp = [sum_z8([z8_mul(Sx[i][j], eHp[j]) for j in range(n)])
            for i in range(n)]
    TeHp = [z8_mul(Tx[i][i], eHp[i]) for i in range(n)]
    iso_diag = all(q8(m) == 0 for m in DIAG_H + ANTI_H)
    check("S0.5 [WEIL EXACT] S symmetric + unitary, S^2 = C, (ST)^3 = "
          "S^2, S^4 = 1, T^8 = 1 in Q(zeta_8); e_H (glue diagonal) and "
          "e_H' (anti-diagonal) exactly T- and S-fixed, all classes "
          "isotropic (v518/delta-1e replication)",
          ok_sym and mat_eq(mat_mul(Sx, mat_conjT(Sx)), mat_id(n))
          and mat_eq(S2, C) and mat_eq(ST3, S2)
          and mat_eq(mat_mul(S2, S2), mat_id(n))
          and mat_eq(T8, mat_id(n))
          and SeH == eH and TeH == eH and SeHp == eHp and TeHp == eHp
          and iso_diag)

    e = lambda x: sp.exp(2 * sp.pi * sp.I * x)
    chi4T = e(R(1, 3))
    chi10T = e(R(5, 6))
    ok_chars = (sp.simplify(chi4T - 1) != 0
                and sp.simplify(chi10T - 1) != 0
                and sp.simplify(chi4T * sp.conjugate(chi4T) - 1) == 0
                and sp.simplify(chi4T ** 2 - e(R(2, 3))) == 0
                and sp.simplify(chi4T ** 2 - 1) != 0
                and sp.simplify((-1) * e(R(-1, 6)) - chi4T) == 0)
    check("S0.6 [CHARACTERS, EXACT] chi_4(T) = e(1/3) and chi_10(T) = "
          "e(5/6) are NONTRIVIAL; |chi_4(T)|^2 = 1 exactly (conjugate "
          "pairing cancels) while chi_4(T)^2 = e(2/3) != 1 (one-sided "
          "squaring does NOT); T-fix mechanism (-1) x e(-1/6) = "
          "chi_4(T) replicated; real tau_2 powers carry no phase",
          ok_chars)
    return Qv, Qtw, Tx, Sx


# ---------------------------------------------------------------------------
# S1 -- transports, derived families, the k = 0 slice
# ---------------------------------------------------------------------------
def section1(Tx, Sx):
    print("  -- S1: block transports + derived families")
    tg, sg, dev = measure_transport_w(
        4, PAIRS4, lambda a, b, tau: M_val(4, a, b, tau), 4)
    tgx = {}
    devmax = mp.mpf(0)
    for p in PAIRS4:
        lt, kt, dt = recog(tg[p])
        _, _, ds = recog(sg[p])
        devmax = max(devmax, dt, ds)
        tgx[p] = (lt, kt)
    axd = {}
    for name, ws in CAND_WS.items():
        tA, sA, devA = measure_transport_w(
            4, PAIRS4, lambda a, b, tau: ax_val(4, ws, a, b, tau), 0)
        tAx = {}
        dmax = mp.mpf(0)
        for p in PAIRS4:
            lt, kt, dt = recog(tA[p])
            _, _, ds = recog(sA[p])
            dmax = max(dmax, dt, ds)
            tAx[p] = (lt, kt)
        axd[name] = dict(ws=ws, t=tA, s=sA, tx=tAx, dev=devA, rec=dmax)
    ok_fix = all(tgx[(0, b)][1] == L_PHASE // 2
                 and abs(tgx[(0, b)][0]) < mp.mpf(10) ** (-30)
                 and axd['f1f3']['tx'][(0, b)][1]
                 == (-L_PHASE // 6) % L_PHASE for b in (1, 2, 3))
    check("S1.1 [TRANSPORTS] gauge + fibre transport constants constant "
          "over two tau (max dev %s < 1e-28) and recognised on the "
          "1/960 grid (max %s < 1e-25); T-fixed nodes: gauge k = 480 "
          "(= -1), fibre f1f3 k = 800 (= e(-1/6)) exactly (v518 "
          "replication)"
          % (mp.nstr(max(dev, max(d['dev'] for d in axd.values())), 3),
             mp.nstr(max(devmax, max(d['rec'] for d in axd.values())),
                     3)),
          dev < mp.mpf(10) ** (-28) and devmax < mp.mpf(10) ** (-25)
          and all(d['dev'] < mp.mpf(10) ** (-28) for d in axd.values())
          and all(d['rec'] < mp.mpf(10) ** (-25) for d in axd.values())
          and ok_fix)

    rhoT = rho_np(Tx)
    rhoS = rho_np(Sx)

    fams = {}
    for orient in ('hol', 'anti'):
        tt, ss = dressed_consts(tg, sg, axd['f1f3'], orient, PAIRS4)
        for k in range(12):
            _, L1, n1, _ = solve_orbit(ORB1, 4, tt, ss, rhoT, rhoS,
                                       (0, 1), k)
            if not n1:
                continue
            _, L2, n2, _ = solve_orbit(ORB2, 4, tt, ss, rhoT, rhoS,
                                       (0, 2), k)
            if not n2:
                continue
            fams[(orient, k)] = dict(L1=L1, n1=n1, L2=L2, n2=n2)
    for (orient, k), d in sorted(fams.items()):
        print("     family %-4s chi_%-2d dims (%d, %d)"
              % (orient, k, len(d['n1']), len(d['n2'])))
    hol_ks = sorted(k for (o, k) in fams if o == 'hol')
    dims_ok = (('hol', 4) in fams and ('hol', 10) in fams
               and len(fams[('hol', 4)]['n1']) == 3
               and len(fams[('hol', 4)]['n2']) == 3
               and len(fams[('hol', 10)]['n1']) == 1
               and len(fams[('hol', 10)]['n2']) == 1)
    check("S1.2 [THE ONLY STRICT CHIRAL FAMILIES] hol f1f3 closes "
          "exactly at k = %s with chi_4 dims (3,3) and chi_10 dims "
          "(1,1), both characters nontrivial (S0.6); anti k = %s "
          "(membership only) -- every strict chiral closure at "
          "physical weight carries a NONTRIVIAL multiplier (v518 S4 "
          "replication)"
          % (str(hol_ks), str(sorted(k for (o, k) in fams
                                     if o == 'anti'))),
          hol_ks == [4, 10] and dims_ok)

    k0 = {}
    scans = [('none', 'hol')] + [(nm, o) for nm in CAND_WS
                                 for o in ('hol', 'anti')]
    for nm, orient in scans:
        if nm == 'none':
            tt = {p: complex(tg[p]) for p in PAIRS4}
            ss = {p: complex(sg[p]) for p in PAIRS4}
        else:
            tt, ss = dressed_consts(tg, sg, axd[nm], orient, PAIRS4)
        _, _, n1, _ = solve_orbit(ORB1, 4, tt, ss, rhoT, rhoS, (0, 1), 0)
        _, _, n2, _ = solve_orbit(ORB2, 4, tt, ss, rhoT, rhoS, (0, 2), 0)
        k0[(nm, orient)] = (len(n1), len(n2))
    n_k0 = sum(1 for v in k0.values() if v[0] > 0 and v[1] > 0)
    check("S1.3 [NO SINGLE-VALUED CHIRAL OPTION, THE CORE FACT] strict "
          "trivial-character two-orbit solutions at physical weight "
          "(m, k) = (0, 0): count %d = 0 across the bare gauge blocks "
          "and ALL five dressings in BOTH orientations (the eta^{+-8} "
          "hits of v518 are weight-shifted bookkeeping, NOT the "
          "physical weight): the one-sided chiral combination KEEPS "
          "its multiplier, always" % n_k0, n_k0 == 0)
    return tg, sg, tgx, axd, rhoT, rhoS, fams, n_k0


# ---------------------------------------------------------------------------
# S2 -- D1: the untwisted-column boundary criterion (canonicalisation)
# ---------------------------------------------------------------------------
def section2(fams, Qv, Qtw, V4, V2, CNT, ser0, lim):
    print("  -- S2: D1 -- column canonicalisation + sharpened kill")
    I = sp.I
    ok_id = True
    for b in (1, 2, 3):
        lhs = [sp.nsimplify(sp.expand(
            sum(I ** (b * m) * Qv[m][i] for m in range(4))))
            for i in range(5)]
        if lhs != Qtw[b]:
            ok_id = False
    check("S2.1 [A PASSES THE COLUMN CRITERION, EXACT] the spread "
          "column sum_m i^{bm} Q_m = Q^{(b)} for b = 1, 2, 3 -- the "
          "physical (0,b) contraction reproduces the AB skeleton "
          "numerators exactly; completing each channel with the "
          "unphased loop Q^{(0)}/det_j is reading (A) by construction",
          ok_id)

    rng = np.random.default_rng(23)
    b0_star = E00.copy()
    null_fake = [b0_star,
                 rng.normal(size=16) + 1j * rng.normal(size=16),
                 rng.normal(size=16) + 1j * rng.normal(size=16)]
    null_fake = [v / np.linalg.norm(v) for v in null_fake]
    Lam1 = fams[('hol', 4)]['L1']
    targets_fake = {p: Lam1[p] @ b0_star for p in [(0, 1), (0, 3)]}
    r_fake, c_fake, _, _ = member_test(Lam1, null_fake, targets_fake)
    check("S2.2 [NC: PLANTED FAMILY] a synthetic family containing its "
          "own column data is detected: sigma ratio %.2e < 1e-10 with "
          "|c| = %.3f > 0.1 (membership machinery teeth)"
          % (r_fake, c_fake), r_fake < 1e-10 and c_fake > 0.1)

    print("     membership table (strong condition, one scalar per "
          "orbit): sigma_min/sigma_max [|c| rel]")
    results = {}
    for (orient, k), fam in sorted(fams.items()):
        for model, cols in list(COLUMN_MODELS.items()) + [
                ('wrongph', WRONG_MODEL)]:
            t1 = {(0, 1): cols[1], (0, 3): cols[3]}
            r1 = member_test(fam['L1'], fam['n1'], t1)
            t2 = {(0, 2): cols[2]}
            r2 = member_test(fam['L2'], fam['n2'], t2)
            results[(orient, k, model)] = (r1, r2)
            print("       %-4s chi_%-2d %-7s orb1 %.2e [%.3f]   "
                  "orb2 %.2e [%.3f]"
                  % (orient, k, model, r1[0], r1[1], r2[0], r2[1]))

    contained = []
    grey = []
    for (orient, k, model), (r1, r2) in results.items():
        if model == 'wrongph':
            continue
        ok1 = r1[0] < CONTAIN_TOL and r1[1] > 1e-6
        ok2 = r2[0] < CONTAIN_TOL and r2[1] > 1e-6
        if ok1 and ok2:
            contained.append((orient, k, model))
        elif (r1[0] < ROBUST_TOL or r2[0] < ROBUST_TOL) \
                and not (ok1 and ok2):
            grey.append((orient, k, model, r1[0], r2[0]))
    check("S2.3 [D1 MEMBERSHIP RESULT] the physical AB spread column "
          "sum_m i^{bm} e_{(m,m)} is contained in exactly ONE derived "
          "family (both orbits, one scalar each -- CANONICALISING the "
          "(N1, N2) freedom): %s = [('hol', 4, 'spread')]; grey-zone "
          "entries: %s"
          % (contained, [(g[0], g[1], g[2]) for g in grey]),
          contained == [('hol', 4, 'spread')]
          and [(g[0], g[1], g[2]) for g in grey]
          == [('anti', 8, 'spread')])

    wrong_contained = []
    for (orient, k, model), (r1, r2) in results.items():
        if model != 'wrongph':
            continue
        if (r1[0] < CONTAIN_TOL and r1[1] > 1e-6
                and r2[0] < CONTAIN_TOL and r2[1] > 1e-6):
            wrong_contained.append((orient, k))
    check("S2.4 [NC: WRONG-PHASE COLUMNS] the shifted-phase control "
          "columns i^{(b+1)m} are contained in NO family: %s"
          % (wrong_contained if wrong_contained else "NONE"),
          not wrong_contained)

    orient, k, model = contained[0]
    fam = fams[(orient, k)]
    cols = COLUMN_MODELS[model]
    _, _, u1, V1 = member_test(
        fam['L1'], fam['n1'], {(0, 1): cols[1], (0, 3): cols[3]})
    _, _, u2, V2m = member_test(
        fam['L2'], fam['n2'], {(0, 2): cols[2]})
    b01 = V1 @ (u1[:-1] / u1[-1])
    b02 = V2m @ (u2[:-1] / u2[-1])
    beta = {}
    for p in ORB1:
        beta[p] = fam['L1'][p] @ b01
    for p in ORB2:
        beta[p] = fam['L2'][p] @ b02
    th = {}
    for tau in (TAU_C, TAU_C + 1, -1 / TAU_C):
        th[tau] = [eval_series16(ser0[mu], tau, lim) for mu in MU]
    cert = function_certificate(beta, (1, 3), k, th)
    I_main, W, n_neg, wt_neg, im_rel, eps_rel = run_integral(
        beta, (1, 3), V4, V2, CNT, mp.mpf(1) / 4)
    tol = max(eps_rel * 100, mp.mpf(10) ** (-7))
    scale = max(abs(x) for x in I_main)
    t5rel = abs(I_main[3]) / scale
    sprA, _ = spread_vs(I_main, [-x for x in AFIX])
    sprC, _ = spread_vs(I_main, CONTACT_A)
    psiI = psi_of(I_main)
    passes = (t5rel < tol
              and (sprA < tol * 10 or sprC < tol * 10
                   or (psiI.real < 0
                       and abs(psiI.imag) < abs(psiI.real) * 1e-6)))
    print("     [D1 canonical member %s chi_%d %s] cert %s; I_main = "
          "%s; neg-cells %d; T5 frac %s; spread(-A_fix) %s; "
          "spread(contact_A) %s; psi = %s"
          % (orient, k, model, mp.nstr(cert, 3), fmtn(I_main), n_neg,
             mp.nstr(t5rel, 3), mp.nstr(sprA, 3), mp.nstr(sprC, 3),
             mp.nstr(psiI, 6)))
    check("S2.5 [D1 SHARPENED KILL] the column-matched canonical chi_4 "
          "member (function certificate %s < 1e-8) STILL FAILS all "
          "testers (T5 frac %s > 0.1, spreads %s / %s > 0.5, psi > 0): "
          "the (N1, N2)-canonicalised derived route is boundary-"
          "consistent yet tester-dead -- the v518 kill is sharpened"
          % (mp.nstr(cert, 3), mp.nstr(t5rel, 3), mp.nstr(sprA, 3),
             mp.nstr(sprC, 3)),
          cert < mp.mpf(10) ** (-8) and not passes
          and t5rel > mp.mpf('0.1'))
    return contained, grey


# ---------------------------------------------------------------------------
# S3 -- D2: the exact invariant subspace / single-valuedness forcing
# ---------------------------------------------------------------------------
def section3(Tx, Sx, V4, CNT, n_k0, tg, sg, axd, rhoT, rhoS):
    print("  -- S3: D2 -- invariant subspace / single-valuedness")
    ns = invariant_subspace(Tx, Sx)
    dim_q = len(ns)
    all_in_span = all(in_lagrangian_span(v) for v in ns)
    check("S3.1 [THE FULL INVARIANT SUBSPACE, EXACT RATIONAL] "
          "dim_Q {v : rho(T) v = v, rho(S) v = v} = %d = 4 x 2 "
          "([Q(zeta_8):Q] = 4 x dim 2 over the field); EVERY exact "
          "nullspace vector lies in the Q(zeta_8)-span of {e_H, e_H'}: "
          "%s -- the invariants are EXACTLY span{e_H, e_H'}, every "
          "single-valued lattice factor is a combination of the two "
          "Lagrangian thetas" % (dim_q, all_in_span),
          dim_q == 8 and all_in_span)

    q_unph = [sum(V4[(a, a)][F(1)][i] for a in range(4))
              for i in range(5)]
    check("S3.2 [BOTH INVARIANTS CARRY THE UNPHASED TRACE] Theta_H and "
          "Theta_H' = E4 (S0.2); the level-1 quartic of the "
          "H-contraction = %s = (36, 72, 36, 0, 0) = Q^{(0)}: the "
          "single-valued lattice factor is FORCED to the unphased "
          "sector trace" % fmt(q_unph),
          q_unph == [36, 72, 36, 0, 0])

    check("S3.3 [DERIVED SIDE CANNOT BE SINGLE-VALUED AT PHYSICAL "
          "WEIGHT] chi_4(T), chi_10(T) nontrivial (S0.6); strict "
          "(m, k) = (0, 0) solutions: %d = 0 for every dressing "
          "(S1.3); real tau_2 powers cannot compensate a phase; the "
          "eta^{+-8} absorption shifts the block weight by -+4 and "
          "breaks the fixed 'block -4 x theta +4' bookkeeping (TP-3)"
          % n_k0, n_k0 == 0)

    z2tab = {}
    for orient in ('hol', 'anti'):
        tt, ss = dressed_consts(tg, sg, axd['f1f3'], orient, ORB2)
        for k in range(12):
            _, L2, n2, _ = solve_orbit(ORB2, 4, tt, ss, rhoT, rhoS,
                                       (0, 2), k)
            if n2:
                z2tab[(orient, k)] = dict(L2=L2, n2=n2)
    ks_hol = sorted(k for (o, k) in z2tab if o == 'hol')
    check("S3.4 [Z2 STANDALONE CHARACTER TABLE] the Z2 sub-orbifold "
          "system (dressed) closes strictly at hol k = %s ({4, 10} "
          "expected as a subset); trivial character k = 0 is NOT "
          "admitted at Z2 either" % ks_hol,
          set([4, 10]).issubset(set(ks_hol)) and 0 not in ks_hol)
    return dim_q, z2tab, ks_hol


# ---------------------------------------------------------------------------
# S4 -- D3: the Z2/EH anchor at the integral level
# ---------------------------------------------------------------------------
def section4(z2tab, V4, V2, CNT, ser0, lim):
    print("  -- S4: D3 -- the Z2/EH anchor at the integral level")
    th = {}
    for tau in (TAU_C, TAU_C + 1, -1 / TAU_C):
        th[tau] = [eval_series16(ser0[mu], tau, lim) for mu in MU]
    seed2 = make_seed2()

    hol_ks = sorted(k for (o, k) in z2tab if o == 'hol')
    outcomes = []
    for k in hol_ks:
        dat = z2tab[('hol', k)]
        evals = [('seed-proj', project_seed(dat['L2'], dat['n2'],
                                            seed2)[0])]
        for model, cols in COLUMN_MODELS.items():
            r2 = member_test(dat['L2'], dat['n2'], {(0, 2): cols[2]})
            if r2 is not None and r2[0] < CONTAIN_TOL and r2[1] > 1e-6:
                b0 = np.array(dat['n2']).T @ (r2[2][:-1] / r2[2][-1])
                beta_m = {p: dat['L2'][p] @ b0 for p in ORB2}
                evals.append(('column-' + model, beta_m))
        for tag, beta in evals:
            if beta is None:
                continue
            nrm = max(np.linalg.norm(beta[p]) for p in beta)
            if nrm < 1e-12:
                continue
            cert = function_certificate(beta, (1, 3), k, th)
            I_main, W, n_neg, wt_neg, im_rel, eps_rel = run_integral(
                beta, (1, 3), V4, V2, CNT, mp.mpf(1) / 2)
            tol = max(eps_rel * 100, mp.mpf(10) ** (-7))
            sprQ1, zQ1 = spread_vs(I_main, Q1VEC)
            psiI = psi_of(I_main)
            ratio_t5t3 = (I_main[3] / I_main[4]
                          if abs(I_main[4]) > 0 else mp.inf)
            okQ1 = sprQ1 < tol * 10 and zQ1 < tol * 10
            ok_ratio = abs(ratio_t5t3 + mp.mpf(1) / 2) < mp.mpf('0.05')
            ok_psi = (psiI.real > 0
                      and abs(psiI.imag) < abs(psiI.real) * 1e-6)
            anchor_pass = okQ1 or (ok_ratio and ok_psi)
            print("     [Z2 chi_%d %s] cert %s; I = %s; spread(Q1) %s; "
                  "psi = %s (Soll +8N)"
                  % (k, tag, mp.nstr(cert, 3), fmtn(I_main),
                     mp.nstr(sprQ1, 3), mp.nstr(psiI, 6)))
            outcomes.append(dict(k=k, tag=tag, cert=cert,
                                 anchor=anchor_pass))
            check("S4.%d [Z2 DERIVED INTEGRAL, chi_%d, %s] function "
                  "certificate %s < 1e-8; the Z2 anchor testers "
                  "(V ~ Q_1 / T5:T3 = -1:2 with psi > 0) FAIL "
                  "(spread(Q1) %s, psi < 0)"
                  % (len(outcomes), k, tag, mp.nstr(cert, 3),
                     mp.nstr(sprQ1, 3)),
                  cert < mp.mpf(10) ** (-8) and not anchor_pass)
    all_fail = bool(outcomes) and not any(o['anchor'] for o in outcomes)
    check("S4.X [D3 RESULT] declared reading hits the Z2 anchor "
          "exactly (S0.4, arithmetic identity); derived Z2 "
          "evaluations: %d run, anchor passes: %d = 0 -- D3 fires "
          "for A (every derived instantiation fails at the anchor)"
          % (len(outcomes), sum(1 for o in outcomes if o['anchor'])),
          len(outcomes) == 3 and all_fail)
    return outcomes, all_fail


# ---------------------------------------------------------------------------
# S5 -- SOURCE 1: the F-lemma (fundamental-domain independence)
# ---------------------------------------------------------------------------
def section5(fams, ser0, lim):
    print("  -- S5: source-1 -- the fundamental-domain lemma")
    r1 = member_test(fams[('hol', 4)]['L1'], fams[('hol', 4)]['n1'],
                     {(0, 1): w_col(1), (0, 3): w_col(3)})
    r2 = member_test(fams[('hol', 4)]['L2'], fams[('hol', 4)]['n2'],
                     {(0, 2): w_col(2)})
    contained = (r1[0] < CONTAIN_TOL and r1[1] > 1e-6
                 and r2[0] < CONTAIN_TOL and r2[1] > 1e-6)
    b01 = np.array(fams[('hol', 4)]['n1']).T @ (r1[2][:-1] / r1[2][-1])
    b02 = np.array(fams[('hol', 4)]['n2']).T @ (r2[2][:-1] / r2[2][-1])
    beta = {}
    for p in ORB1:
        beta[p] = fams[('hol', 4)]['L1'][p] @ b01
    for p in ORB2:
        beta[p] = fams[('hol', 4)]['L2'][p] @ b02
    taus = []
    for t0 in (TAU_C, TAU_D):
        taus += [t0, t0 + 1, -1 / t0]
    th = {tau: [eval_series16(ser0[mu], tau, lim) for mu in MU]
          for tau in taus}

    def G_total(tau):
        tot = mp.mpc(0)
        for p, bp in beta.items():
            v = (M_val(4, p[0], p[1], tau)
                 * ax_val(4, (1, 3), p[0], p[1], tau))
            tot += v * sum(complex(bp[i]) * th[tau][i] for i in range(16))
        return tot

    chT = mp.exp(2j * mp.pi * mp.mpf(4) / 12)
    chS = mp.exp(-2j * mp.pi * mp.mpf(4) / 4)
    cert = mp.mpf(0)
    gmin = mp.inf
    for t0 in (TAU_C, TAU_D):
        g0 = G_total(t0)
        gmin = min(gmin, abs(g0))
        cert = max(cert, abs(G_total(t0 + 1) / (chT * g0) - 1))
        cert = max(cert, abs(G_total(-1 / t0) / (chS * g0) - 1))
    print("     canonical chi_4 column member: sigma ratios orb1 "
          "%.2e / orb2 %.2e; |G(tau)| >= %s; total-sum certificate "
          "max dev %s over two fresh tau"
          % (r1[0], r2[0], mp.nstr(gmin, 3), mp.nstr(cert, 3)))
    ok = bool(contained and cert < mp.mpf(10) ** (-8)
              and gmin > mp.mpf(10) ** (-10))
    check("S5.1 [F-LEMMA CERTIFICATE + COROLLARY] the canonical "
          "member's TOTAL block sum obeys G(tau+1) = chi_4(T) G(tau), "
          "G(-1/tau) = chi_4(S) G(tau) pointwise (cert %s < 1e-8, "
          "nonvacuous |G| > 1e-10).  EXACT CHANGE OF VARIABLES: "
          "int_{gamma F} G dmu = chi_4(gamma) int_F G dmu with "
          "chi_4(T) = e(1/3) != 1 -- an F-independent value forces "
          "int = 0: under TP-1 + TP-2 NO chiral integrand at physical "
          "weight can source psi = 64; single-valuedness is FORCED "
          "for any nonzero one-loop lattice contribution"
          % mp.nstr(cert, 3), ok)
    return ok


# ---------------------------------------------------------------------------
# S6 -- SOURCE 2: the Quillen pairing
# ---------------------------------------------------------------------------
def section6(tg, sg, axd, rhoT, rhoS):
    print("  -- S6: source-2 -- the Quillen pairing")
    ttH, ssH = dressed_consts(tg, sg, axd['f1f3'], 'hol', PAIRS4)
    ktot = {}
    dbl_dev = mp.mpf(0)
    for p in PAIRS4:
        _, kt, _ = recog(mp.mpc(ttH[p]))
        ktot[p] = kt
        tf = mp.mpc(tg[p]) * mp.mpc(axd['f1f3']['t'][p])
        sf = mp.mpc(sg[p]) * mp.mpc(axd['f1f3']['s'][p])
        dbl_dev = max(dbl_dev, abs(tf * mp.conj(tf) - 1),
                      abs(sf * mp.conj(sf) - 1))
    sq_def_T = {p: (2 * ktot[p]) % L_PHASE for p in PAIRS4}
    fib_sq = (2 * ((-L_PHASE // 6) % L_PHASE)) % L_PHASE
    check("S6.1 [CONJUGATE PAIRING CANCELS -- MEASURED UNITARITY] the "
          "doubled hol x antihol transports t conj(t) = |t|^2 equal 1 "
          "to %s < 1e-30 on all 15 pairs and both generators; the "
          "one-sided SQUARED combination keeps defects: T-fixed fibre "
          "2 x 800 = %d = e(2/3) != 0 on the exact grid, squared-"
          "defect table nonzero on %d of 15 pairs -- the phase dies "
          "ONLY in the conjugate pairing (|chi_4|^2 = 1 vs chi_4^2 = "
          "e(2/3), S0.6)"
          % (mp.nstr(dbl_dev, 3), fib_sq,
             sum(1 for p in PAIRS4 if sq_def_T[p] != 0)),
          dbl_dev < mp.mpf(10) ** (-30) and fib_sq == 640
          and any(v != 0 for v in sq_def_T.values()))

    rhoT2 = np.kron(rhoT, rhoT.conj())
    rhoS2 = np.kron(rhoS, rhoS.conj())
    tt2 = {p: ttH[p] * np.conj(ttH[p]) for p in PAIRS4}
    ss2 = {p: ssH[p] * np.conj(ssH[p]) for p in PAIRS4}
    _, L1d, n1d, _ = solve_orbit(ORB1, 4, tt2, ss2, rhoT2, rhoS2,
                                 (0, 1), 0)
    _, L2d, n2d, _ = solve_orbit(ORB2, 4, tt2, ss2, rhoT2, rhoS2,
                                 (0, 2), 0)
    d1, d2 = len(n1d), len(n2d)
    vecI = np.zeros(256, dtype=complex)
    for i in range(16):
        vecI[16 * i + i] = 1.0
    vecI /= np.linalg.norm(vecI)
    resI = []
    for nd in (n1d, n2d):
        V = np.array(nd).T
        proj = V @ np.linalg.solve(V.conj().T @ V, V.conj().T @ vecI)
        resI.append(float(np.linalg.norm(vecI - proj)))
    check("S6.2 [DOUBLED SYSTEM CLOSES SINGLE-VALUEDLY] the 256-dim "
          "hol x antihol Weil system (rho (x) conj(rho), transports "
          "t conj(t)) closes STRICTLY at trivial character and "
          "physical weight: nullspace dims (%d, %d) >= 11 = 3^2 + 1^2 "
          "+ 1; the unphased diagonal sum_mu e_mu (x) conj(e_mu) lies "
          "inside (residuals %.2e / %.2e < 1e-8): single-valuedness "
          "is IMPLEMENTED by the pairing, not postulated"
          % (d1, d2, resI[0], resI[1]),
          d1 >= 11 and d2 >= 11 and max(resI) < 1e-8)

    W1 = np.kron(w_col(1), w_col(1).conj())
    W3 = np.kron(w_col(3), w_col(3).conj())
    W2 = np.kron(w_col(2), w_col(2).conj())
    rd1 = member_test(L1d, n1d, {(0, 1): W1, (0, 3): W3})
    rd2 = member_test(L2d, n2d, {(0, 2): W2})
    check("S6.3 [PHYSICAL DOUBLED COLUMNS CONTAINED] the physical "
          "untwisted-column data w_b (x) conj(w_b) is contained in "
          "the doubled single-valued family with ONE scalar per orbit "
          "(sigma %.2e / %.2e < 1e-8, coefficient nonvanishing): the "
          "physical |.|^2 object lives entirely inside the single-"
          "valued surface" % (rd1[0], rd2[0]),
          rd1[0] < CONTAIN_TOL and rd1[1] > 1e-6
          and rd2[0] < CONTAIN_TOL and rd2[1] > 1e-6)

    rhoT2w = np.kron(rhoT, rhoT)
    rhoS2w = np.kron(rhoS, rhoS)
    tt2w = {p: ttH[p] * ttH[p] for p in PAIRS4}
    ss2w = {p: ssH[p] * ssH[p] for p in PAIRS4}
    _, _, n1w, sv1w = solve_orbit(ORB1, 4, tt2w, ss2w, rhoT2w, rhoS2w,
                                  (0, 1), 0)
    _, _, n2w, sv2w = solve_orbit(ORB2, 4, tt2w, ss2w, rhoT2w, rhoS2w,
                                  (0, 2), 0)
    check("S6.4 [NC: WRONG PAIRING EMPTY] the hol (x) hol doubled "
          "system (squared transports, characters chi^2 != 1) has NO "
          "trivial-character closure: nullspace dims (%d, %d) = "
          "(0, 0), min sv ratios %.2e / %.2e -- only the CONJUGATE "
          "pairing implements single-valuedness"
          % (len(n1w), len(n2w),
             min(sv1w) / max(sv1w), min(sv2w) / max(sv2w)),
          len(n1w) == 0 and len(n2w) == 0)

    _, _, devw = measure_transport_w(
        4, [(0, 1), (1, 0), (1, 1), (2, 1)],
        lambda a, b, tau: M_val(4, a, b, tau), 2)
    check("S6.5 [NC: WRONG WEIGHT] the gauge transport measured at "
          "weight exponent 2 instead of 4 is NOT constant over tau "
          "(dev %s > 1e-3): the physical weight bookkeeping (TP-3) "
          "has teeth" % mp.nstr(devw, 3),
          devw > mp.mpf(10) ** (-3))

    rng = np.random.default_rng(23)
    bstar = n1d[0]
    fake_null = [bstar,
                 rng.normal(size=256) + 1j * rng.normal(size=256),
                 rng.normal(size=256) + 1j * rng.normal(size=256)]
    fake_null = [v / np.linalg.norm(v) for v in fake_null]
    targets_fake = {p: L1d[p] @ bstar for p in [(0, 1), (0, 3)]}
    rf = member_test(L1d, fake_null, targets_fake)
    check("S6.6 [NC: PLANTED DOUBLED FAMILY] a synthetic doubled "
          "family containing its own column data is detected: sigma "
          "%.2e < 1e-10 with |c| = %.3f > 0.1 (machinery teeth at "
          "256 dims)" % (rf[0], rf[1]),
          rf[0] < 1e-10 and rf[1] > 0.1)
    A2ok = bool(dbl_dev < mp.mpf(10) ** (-30) and d1 >= 11 and d2 >= 11
                and max(resI) < 1e-8
                and rd1[0] < CONTAIN_TOL and rd2[0] < CONTAIN_TOL
                and len(n1w) == 0 and len(n2w) == 0)
    return A2ok


# ---------------------------------------------------------------------------
# S7 -- the point-4 consistency closure
# ---------------------------------------------------------------------------
def section7(V4, V2, CNT):
    print("  -- S7: the point-4 consistency closure")
    levels_H = sorted(set().union(*[set(V4[(m, m)].keys())
                                    for m in range(4)]))
    levels_Hp = sorted(set().union(*[set(V4[m].keys()) for m in ANTI_H]))
    ok_H = True
    ok_Hp = True
    c_samples = []
    for lev in levels_H:
        s = [sum(V4[(m, m)].get(lev, ZERO5)[i] for m in range(4))
             for i in range(5)]
        c = s[0]
        if s != [c, 2 * c, c, 0, 0]:
            ok_H = False
        if lev <= 3:
            c_samples.append((lev, c))
    for lev in levels_Hp:
        s = [sum(V4[m].get(lev, ZERO5)[i] for m in ANTI_H)
             for i in range(5)]
        c = s[0]
        if s != [c, 2 * c, c, 0, 0]:
            ok_Hp = False
    check("S7.1 [EXACT LEVELWISE OKUBO / 4-DESIGN] the unphased "
          "diagonal ledger sum_m V_{(m,m),lev} AND the anti-diagonal "
          "(H') sum are EXACTLY proportional to <x,x>^2 = (1, 2, 1, "
          "0, 0) at EVERY level (H: %d levels, H': %d levels, n <= 8; "
          "samples (lev, c): %s): the forced E4 numerator is a "
          "perfect Okubo square LEVEL BY LEVEL"
          % (len(levels_H), len(levels_Hp), str(c_samples[:4])),
          ok_H and ok_Hp)

    pairs_col = [(0, 1), (0, 2), (0, 3)]
    dets = {1: 2.0, 2: 4.0, 3: 2.0}
    dm, basemap = build_dress(pairs_col, (1, 3))
    beta_unph = {p: diag_unph() / dets[p[1]] for p in pairs_col}
    beta_ph = {p: w_col(p[1]) / dets[p[1]] for p in pairs_col}
    beta_ct = {p: col_contact(p[1]) / dets[p[1]] for p in pairs_col}

    def run_cols(beta, cut):
        dml = {p: {e: v for e, v in dm[p].items() if e <= cut}
               for p in beta}
        return hm_integral_pp(beta, dml, basemap, V4, V2, CNT, cut,
                              mp.mpf(1) / 4)

    I_tot, _, _, nneg_t, _ = run_cols(beta_unph, GRID_CUT)
    I_lo, _, _, _, _ = run_cols(beta_unph, GRID_CUT_LOW)
    scale = max(abs(x) for x in I_tot)
    eps_rel = max(abs(I_tot[i] - I_lo[i]) for i in range(5)) / scale
    im_rel = max(abs(x.imag) for x in I_tot) / scale
    spr_tot, z_tot = spread_vs(I_tot, OKUBO)
    ch_dat = []
    for p in pairs_col:
        I_ch, _, _, _, _ = run_cols({p: beta_unph[p]}, GRID_CUT)
        spr, zz = spread_vs(I_ch, OKUBO)
        ch_dat.append((p[1], spr, zz))
    print("     I(unphased columns) = %s; cut-6 vs cut-8 %s; |Im| %s"
          % (fmtn(I_tot), mp.nstr(eps_rel, 3), mp.nstr(im_rel, 3)))
    check("S7.2 [UNPHASED NUMERATOR x v518 SCAFFOLD = OKUBO] the "
          "J-weighted unphased column integral is proportional to "
          "<x,x>^2 PER CHANNEL and in TOTAL (total spread %s, T5/T3 "
          "fraction %s, channel spreads all < 1e-8), with ZERO "
          "negative-exponent cells (%d): the v516 per-sector perfect "
          "squares are REPRODUCED inside the v518 integral machinery"
          % (mp.nstr(spr_tot, 3), mp.nstr(z_tot, 3), nneg_t),
          spr_tot < mp.mpf(10) ** (-8) and z_tot < mp.mpf(10) ** (-8)
          and all(spr < mp.mpf(10) ** (-8)
                  and zz < mp.mpf(10) ** (-8) for _, spr, zz in ch_dat)
          and nneg_t == 0 and im_rel < mp.mpf(10) ** (-8))

    I_ct, _, _, _, _ = run_cols(beta_ct, GRID_CUT)
    psi_ct = psi_of(I_ct)
    V4_1 = {mu: ({F(1): V4[mu][F(1)]} if F(1) in V4[mu] else {})
            for mu in MU}
    I_ct1, _, _, _, _ = hm_integral_pp(
        beta_ct, dm, basemap, V4_1, V2, CNT, GRID_CUT, mp.mpf(1) / 4)
    psi_ct1 = psi_of(I_ct1)
    print("     I(contact columns) = %s; psi = %s; level-1 slice psi "
          "= %s  [arithmetic contact psi = -64]"
          % (fmtn(I_ct), mp.nstr(psi_ct, 6), mp.nstr(psi_ct1, 6)))
    ok_psi = (psi_ct.real < 0
              and abs(psi_ct.imag) < abs(psi_ct.real) * 1e-6
              and psi_ct1.real < 0)
    check("S7.3 [CONTACT SUPPLIES THE psi SLICE, RIGHT SIGN] the "
          "J-weighted contact (unphased minus phased columns) carries "
          "psi = %s < 0 (full) and %s < 0 (level-1 slice) -- the "
          "-64-slice sign of v511/v516 is reproduced by the FORCED "
          "numerator inside the scaffold"
          % (mp.nstr(psi_ct, 6), mp.nstr(psi_ct1, 6)), ok_psi)

    I_ph, _, _, _, _ = run_cols(beta_ph, GRID_CUT)
    psi_ph = psi_of(I_ph)
    print("     I(skeleton/phased columns) = %s; psi = %s  "
          "[arithmetic A_fix psi = +64]"
          % (fmtn(I_ph), mp.nstr(psi_ph, 6)))
    lin = max(abs(I_ph[i] + I_ct[i] - I_tot[i]) for i in range(5)) / scale
    check("S7.4 [THE CIRCLE CLOSES LINEARLY] skeleton (phased, psi = "
          "%s > 0) + contact (completion, psi < 0) = unphased columns "
          "inside the integral machinery (rel residual %s < 1e-12): "
          "the v516 identity skeleton_j + contact_j = Q^(0)/det_j "
          "holds cellwise in the v518 scaffold -- the circle to v516 "
          "is closed" % (mp.nstr(psi_ph, 6), mp.nstr(lin, 3)),
          lin < mp.mpf(10) ** (-12) and psi_ph.real > 0)
    A3ok = bool(ok_H and ok_Hp and spr_tot < mp.mpf(10) ** (-8)
                and z_tot < mp.mpf(10) ** (-8) and nneg_t == 0
                and ok_psi and lin < mp.mpf(10) ** (-12))
    return A3ok


# ---------------------------------------------------------------------------
# S8 -- remaining negative controls (exact)
# ---------------------------------------------------------------------------
def section8(Qv):
    print("  -- S8: negative controls (exact)")
    R = sp.Rational
    I = sp.I
    so_tot = [sp.nsimplify(R(5, 4) * (Qv[0][i] + Qv[2][i]))
              for i in range(5)]
    okmu2 = all(((m * p[1]) % 4) % 2 == 0 for p in ORB2
                for m in (1, 2, 3))
    ok_so = (so_tot == [15, 30, 45, 20, -40])
    check("S8.1 [NC: SO(16)/D8] even with single-valuedness granted "
          "the so16 unphased trace is NO Okubo square: completion "
          "total = %s leaves T5 = 20, T3 = -40 (exact) -- the KILL "
          "fires for so16, E8 stays doubly special; the order-4 "
          "supply is structurally absent on the derived side (all "
          "ORB2 fibre b-characters in mu_2: %s)"
          % (fmt(so_tot), okmu2), ok_so and okmu2)

    dets_f = {1: 2 * I, 2: 4, 3: -2 * I}
    Qtw = {j: [sp.nsimplify(sp.expand(
        sum(I ** (j * m) * Qv[m][i] for m in range(4))))
        for i in range(5)] for j in range(4)}
    wf = [sp.nsimplify(sp.expand(
        sum((1 - I ** (j * m)) / dets_f[j] for j in (1, 2, 3))))
        for m in range(4)]
    Af = [sp.nsimplify(sp.expand(
        sum(Qtw[j][i] / dets_f[j] for j in (1, 2, 3))))
        for i in range(5)]
    h = [R(m * (4 - m), 8) for m in range(4)]
    check("S8.2 [NC: diag(i, i)] fake zero modes (2i, 4, -2i): "
          "skeleton degenerates to the Z2 target %s = A_2; fake "
          "weights %s break the conjugation pairing (w_1 != w_3) and "
          "the index bridge (w != 4h) (v516 S4.4 replication)"
          % (fmt(Af), fmt(wf)),
          Af == A2VEC and wf == [0, R(-1, 2), 0, R(3, 2)]
          and wf[1] != wf[3]
          and any(wf[m] != 4 * h[m] for m in range(4)))

    gw = sum_z8([z8_root((2 * x * x + 2 * y * y) % 8)
                 for x in range(4) for y in range(4)])
    nrm = z8_mul(gw, z8_conj(gw))
    Tw, Sw = build_weil(lambda m: (2 * m[0] ** 2 + 2 * m[1] ** 2) % 8,
                        lambda m, n2: (4 * (m[0] * n2[0]
                                            + m[1] * n2[1])) % 8,
                        MU, Z8_ONE)
    Cm = [[Z8_ONE if MU[j] == neg(MU[i]) else Z8_ZERO
           for j in range(16)] for i in range(16)]
    s2w = mat_mul(Sw, Sw)
    ok_wf = (nrm == z8_scal(F(64), Z8_ONE) and not mat_eq(s2w, Cm))
    check("S8.3 [NC: WRONG FORM] q = (x^2+y^2)/4: |Gauss|^2 = %s = "
          "64 != 16 and S^2 = C breaks EXACTLY -- no invariant-"
          "subspace forcing is available for the wrong discriminant "
          "form (the E4 forcing is form-specific)" % str(nrm[0]),
          ok_wf)

    wsh = [0, R(1, 2), R(3, 8), R(1, 2)]
    T5sh = sp.nsimplify(sum(4 * wsh[m] * Qv[m][3] for m in range(4)))
    T3sh = sp.nsimplify(32 + sum(4 * wsh[m] * Qv[m][4]
                                 for m in range(4)))
    check("S8.4 [NC: SHUFFLED WEIGHTS] h_1 <-> h_2 swap leaves "
          "T5 = %s != 0 AND T3 leftover %s != 0 (exact): the ch2 "
          "pattern carries the levelwise cancellation (v516 S4.2 "
          "replication)" % (T5sh, T3sh), T5sh == -14 and T3sh == 36)
    return bool(ok_so and okmu2 and ok_wf and T5sh == -14)


# ---------------------------------------------------------------------------
# S9 -- verdict per the preregistered branches
# ---------------------------------------------------------------------------
def section9(d1_sharpened, dim_q, n_k0, z2_all_fail, A1, A2, A3, NC_ok):
    print("  -- S9: verdict per the preregistered branches")
    d2_fires = (dim_q == 8 and n_k0 == 0)
    erfolg_a = bool(A1 and A2 and A3 and NC_ok and d2_fires
                    and z2_all_fail and d1_sharpened)
    check("S9.1 [VERDICT: ERFOLG-A (decision layer)] single-valuedness "
          "of the physical one-loop lattice factor on PT/Z4 is DERIVED "
          "from two independent constructive sources, not postulated "
          "-- (source-1) F-independence: every strict chiral option at "
          "physical weight carries a nontrivial character, and a "
          "character-covariant integrand has NO F-independent nonzero "
          "moduli integral (exact change of variables); (source-2) the "
          "Quillen/BCOV pairing hol x conj(hol) cancels the multiplier "
          "identically and the doubled system closes single-valuedly "
          "with the physical columns contained.  With single-"
          "valuedness forced, the invariant subspace (exact: "
          "span{e_H, e_H'} = E4 = the unphased trace) FORCES the v516 "
          "numerator, and the point-4 circle closes levelwise.  "
          "Consequences: the WP5e measure question is DECIDED at probe "
          "level in favour of reading (A) (v516) under the typed "
          "premises TP-1..TP-4; the v518 kill is SHARPENED (the chi_4 "
          "route was never a well-defined nonzero moduli integral: its "
          "unfolded values are convention bookkeeping; the column-"
          "canonicalised member is boundary-consistent yet tester-"
          "dead); psi = 64 is sourced by the now-forced unphased "
          "completion; D3 confirms at the Z2/EH anchor.  NO marker "
          "moves -- any status upgrade goes through the regular "
          "promotion workflow", erfolg_a)
    check("S9.2 [HONEST BOOKKEEPING + TYPED PREMISES] exact = Weil "
          "relations, invariant subspace (rational nullspace), "
          "characters and 1/960 grid arithmetic, completion/contact/"
          "psi identities, levelwise 4-design ledgers, Z2 anchor "
          "arithmetic, controls, change-of-variables corollary; "
          "numeric (documented) = block transports (28+ digits, grid "
          "25+), SVD solves and memberships (double, thresholds "
          "1e-8/1e-3), total-sum certificates at two fresh tau "
          "(< 1e-8), HM kernels (30+ digits, cut-6 vs cut-8, "
          "negative-cell audit); typed premises TP-1 (F-independent "
          "moduli integral), TP-2 (nonvanishing -- must source "
          "psi = 64), TP-3 (v518 kernel convention), TP-4 (Quillen "
          "structure of BCOV F1) named in the verdict; the residual "
          "[O] is the constructive BCOV derivation of the w_m "
          "normalisation itself", True)


# ---------------------------------------------------------------------------
def run():
    reset()
    # the transport/recognition certificates need 40 digits; restore the
    # working precision in case an earlier suite module lowered it
    mp.mp.dps = 40
    _J_CACHE.clear()
    print("v520  CELEST.WP5E.MEASURE.01: the WP5e BCOV measure question "
          "decided at probe level -- single-valuedness derived from two "
          "constructive sources, the completion reading (A) wins "
          "(delta-1e + delta-1f consolidated)")
    print("  [building 16-class exact ledgers to level 8 ...]")
    d5led = build_d5_vecs(MAXN_LED)
    a3led = build_a3_vecs(MAXN_LED)
    V4, V2, CNT = build_ledgers16(d5led, a3led, MAXN_LED)
    print("  [building coset theta series for certificates ...]")
    ser0, lim = build_theta_ser0()

    Qv, Qtw, Tx, Sx = section0(V4, CNT)
    tg, sg, tgx, axd, rhoT, rhoS, fams, n_k0 = section1(Tx, Sx)
    contained, grey = section2(fams, Qv, Qtw, V4, V2, CNT, ser0, lim)
    dim_q, z2tab, ks_hol = section3(Tx, Sx, V4, CNT, n_k0, tg, sg, axd,
                                    rhoT, rhoS)
    z2_outcomes, z2_all_fail = section4(z2tab, V4, V2, CNT, ser0, lim)
    A1 = section5(fams, ser0, lim)
    A2 = section6(tg, sg, axd, rhoT, rhoS)
    A3 = section7(V4, V2, CNT)
    NC_ok = section8(Qv)
    d1_sharpened = (contained == [('hol', 4, 'spread')])
    section9(d1_sharpened, dim_q, n_k0, z2_all_fail, A1, A2, A3, NC_ok)

    return summary("v520 CELEST.WP5E.MEASURE.01: the WP5e measure "
                   "question is DECIDED at probe level -- the invariant "
                   "subspace of the 16-dim Weil system is exactly "
                   "span{e_H, e_H'} (dim_Q = 8 = 4 x 2, both = E4 = "
                   "the unphased trace); single-valuedness is DERIVED "
                   "from two independent constructive sources "
                   "(F-independence of the moduli integral kills every "
                   "chiral option: exact change of variables with "
                   "chi_4(T) = e(1/3) != 1; the Quillen pairing "
                   "cancels the multiplier: |t conj(t) - 1| < 8.3e-40 "
                   "on all 15 pairs, the doubled 256-dim system closes "
                   "at trivial character with the physical columns "
                   "contained, hol (x) hol empty); the forced unphased "
                   "numerator reproduces the v516 Okubo squares "
                   "levelwise inside the v518 scaffold and supplies "
                   "the psi < 0 contact slice (circle closed); the "
                   "declared reading also wins D1 (column "
                   "canonicalisation: the chi_4 member is boundary-"
                   "consistent yet fails every tester -- kill "
                   "sharpened) and D3 (Z2/EH anchor: all three derived "
                   "instantiations fail); ERFOLG-A under the typed "
                   "premises TP-1..TP-4; residual [O] = the "
                   "constructive BCOV derivation of w_m; no marker "
                   "moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
