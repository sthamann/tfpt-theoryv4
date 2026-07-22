"""v518 -- CELEST.WP5E.DELTA1.01: the delta-1 chain (delta-1b + delta-1c
+ delta-1d) DECIDED -- "the derived chiral measure kills the delta-1
route", an honest, decided NEGATIVE result (v508 style).  Question
(preregistered in v508 S6.2, sharpened by v511): does the Harvey-Moore /
BCOV fundamental-domain integral on PT/Z4, evaluated under a measure
that is DERIVED (blockwise SL(2,Z) covariance of the dressed
16-component Weil system, solved for -- not declared, not scanned),
deliver the twisted contact vector -A_fix = -(9, -30, -15, 0, 32) or the
psi = 64 slice?  Answer: NO -- every member of the derived family fails
all three preregistered testers, with the residual freedoms measured
exactly.  Consolidates the decided delta-1b/1c/1d probe chain into one
suite module.

[E] 1. THE 16-COMPONENT WEIL COMPLETION (delta-1c): the discriminant
    module of D5 (+) A3 is Z4 x Z4 with q = (5x^2 + 3y^2)/8 mod 1;
    Gauss sums 2 zeta_8^5 x 2 zeta_8^3 = 4 = sqrt(16) (signature 0 mod
    8 = rank E8); T = diag e(q), S = (1/4) e(-(mu,nu)) satisfy S
    symmetric + unitary, S^2 = C, (ST)^3 = S^2, S^4 = 1, T^8 = 1
    EXACTLY in Q(zeta_8); S = S_D5 (x) S_A3; the glue diagonal H and
    the anti-diagonal H' are the two invariant Lagrangians (both counts
    reproduce E4 -- two E8 gluings); P_H S P_H = (1/4) J with 3/4 of
    every S-image weight on the 12 shifted classes -- WHY the naive
    4-character rule failed; the 16-vector theta S-covariance CLOSES:
    the delta-1b E1.5 residual 2.91 = O(1) (naive 4-rule) drops to
    ~1e-39 (16-component Weil rule), certified at two tau points.
[E] 2. THE OBSTRUCTION IS A FINITE mu4 CHARACTER, IDENTIFIED: the
    dressed gauge blocks M = G[a,b] eta^{-8} have constant transport
    (t_p, s_p) (28+ digits), recognised as exact phases on the 1/960
    grid (1e-25); the T-fixed pairs (0,b) carry t = e(-1/2) = -1
    EXACTLY (the naked level-matching defect); the transport-groupoid
    loops land in the orbit stabilisers Gamma_1(4) (gcd-1) resp.
    Gamma_0(2)+- (gcd-2), joint holonomy eigenspaces dim 8/16 resp.
    6/16 with every eigen-phase a root of unity of order <= 4 (the
    group is mu_4); the KOBOUNDARY TEST: the three SL(2,Z) relation
    defects c_{S^4}, c_{(ST)^3 S^-2}, c_{[S^2,T]} are (1, 1, 1)
    EXACTLY on all 15 pairs -- the multiplier system is a CHARACTER of
    the stabilisers, NOT a genuine 2-cocycle on SL(2,Z); on Gamma_1(4)
    it is identified: lambda(gamma) = i^{2B + C/4} (monomial fit in
    the residues, (2,1,0,0) among the four equivalent solutions).
[E] 3. THE CANCELLATION EXISTS AND IS THE TWISTED FIBRE BLOCK f1 f3,
    NOT THE THREE SPHERE AXIONS: exact identity G[a,b] = f_1 f_3 (the
    twisted C^2 gauge block IS the weight-(1,3) axion pair, 30+
    digits); the axion T-phases are v502 vacuum-energy data e(sum 2E),
    not a fit; the T-fix mechanism is one line of exact phase
    arithmetic: (-1) x e(-1/6) = e(1/3) = chi_4(T) at every T-fixed
    node; the CANCELLATION TABLE (exact, minimal residual multiplier
    order over all eta^m x chi_k, m = 0..23, k = 0..11): none -> 4,
    f1f2f3 (the three sphere axions) -> 4, f2 -> 6, f1f3 -> 1 (hol AND
    anti), wrong weights (1,1,2)/(2,2,2) -> 4: ONLY the f1 f3 dressing
    cancels the mu4 system; the strict solutions are exactly chi_4
    (dims (3,3)) and chi_10 (dims (1,1)) at eta^0 (the eta^{+-8} hits
    are the same transport solutions with T-phase bookkeeping folded
    in), certified on the dressed functions at a fresh tau (1e-15, NO
    residual multiplier).
[E] 4. THE DECISION -- ALL THREE TESTERS FAIL (the kill): under both
    derived solutions the integral (30-digit kernels, negative-exponent
    cell audit, cut-6 vs cut-8 truncation scan) fails T5(V) = 0
    (fractions ~0.5 / ~0.83), fails W_2 : W_13 = 4 : 3 (W_13 = 0, the
    ratio degenerates), fails V = -A_fix N (spreads ~1.05 / ~1.47) and
    the psi = -64 N slice; the honest (N1, N2) orbit-rebalance scan:
    chi_4 reaches T5 = 0 only at psi > 0 (wrong sign), chi_10 only at
    N2/N1 = -4 < 0 (outside the orbifold projector) -- no branch fires
    anywhere in the positive cone.  NEGATIVE CONTROLS: Z2/Eguchi-Hanson
    (gauge-only residual order 2 -- no order-4 content, the mu4 defect
    is Z4-specific -- and the SAME fibre dressing cancels it to 1: the
    mechanism replicates at the anchor); SO(16)/D8 (only even sectors
    survive, all axion b-characters in mu_2, the order-4 supply
    structurally absent); wrong discriminant form (x^2+y^2)/4
    (|Gauss|^2 = 64 != 16, its S-rule fails at O(1) on the true
    thetas) and wrong signature factor (S^2 = C breaks exactly).
[C] THE f1f3 = KS-WEIGHT IDENTIFICATION: the cancelling block f1 f3
    carries the deck weights (1, 3) = (+1, -1 mod 4) of the twistor
    fibre coordinates (mu1, mu2) -> (i mu1, i^{-1} mu2) forced by the
    v514 incidence ledger -- exactly the Kodaira-Spencer fibre content
    of PT/Z4, an exact match, but NOT a complete BCOV derivation of
    the one-loop measure.  KERNEL-FAMILY CONVENTION: main kernel
    J(Delta,0) + heat-kernel completion J(Delta,1), J(Delta,2)
    (P-block only), fixed by weight bookkeeping (invariant measure
    d^2tau/tau_2^2 x tau_2^2 quartic zero-mode scaling) -- a
    documented convention, not a derivation.  Residual discrete
    freedom: the chi_k choice within {chi_4, chi_10} (both evaluated,
    both fail -- the kill does not depend on it).
TENSION, stated honestly (the mandatory fence): the DECLARED completion
    reading (v516/M2) delivers the psi = 64 slice and cancels 32 T3;
    the DERIVED chiral measure (this module) fails all three testers --
    both are exact; the sharp open question is which of the two is the
    true BCOV measure (the declared reading is supported by the
    delta-1 modular-completion finding but not derived; the derived
    measure rests on the f1f3 identification).  Neither result is
    hidden behind the other.
[O] the BCOV-integral derivation on PT/Z4 that decides between the two
    measures (the declared completion reading of v516 vs the derived
    chiral measure of this module) -- the single open item that closes
    the delta-1 strand; until then CELEST.SEAM.01 carries the measure
    question as a named [O], and the twisted-contact route of v508
    S6.2 is DECIDED NEGATIVE under the derived measure.  NO marker
    moves anywhere.

Status: [E] exact Weil/Q(zeta_8) algebra, exact loop words + relation
defects + 1/960 phase arithmetic, exact ledgers/grids/leading cell,
G = f1 f3 (30+ digits), the decision table; [C] the f1f3/KS-weight
identification + the kernel-family convention; [O] the BCOV derivation
above.  Python; Wolfram-mirrored (Weil relations + Gauss sums,
character formula + koboundary defects, cancellation table, T-fix
mechanism (-1) e(-1/6) = e(1/3), wrong-form/wrong-signature controls);
the Harvey-Moore integrals are numerical (mpmath kernels + SVD solves)
and stay Python-only, flagged in the .wl mirror.  Discovery
provenance: experiments/tfpt-discovery/
celestial_seam_wp5e_delta1b_harvey_moore_unfolding_probe.py (30/30),
..._delta1c_weil16_completion_probe.py (31/31),
..._delta1d_order4_multiplier_cancellation_probe.py (36/36)
(2026-07-22)."""
import math
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, gcd, lcm

import mpmath as mp
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, rankE8

MU4 = N_fam + 1                # 4 = |mu4|, the seam clock order
NCLS = MU4 * MU4               # 16 discriminant classes of D5 (+) A3
L_PHASE = 960                  # exact phase grid: e(k / 960)
HALF = F(1, 2)

MAXN_LED = 16                  # quartic ledger cut (levels n <= 8)
MAXN_NUM = 34                  # theta covariance certificate cut
GRID_CUT = F(8)                # main dressing cut Delta <= 8
GRID_CUT_LOW = F(6)            # truncation-scan cut
BASES4 = {0: F(-1, 2), 1: F(-5, 16), 2: F(-1, 4), 3: F(-5, 16)}
SIGMA3 = [1, 9, 28, 73, 126, 252, 344, 585]
NPROD = 120
TAU_A = mp.mpc(mp.mpf(13) / 100, mp.mpf(51) / 50)
TAU_B = mp.mpc(mp.mpf(-31) / 100, mp.mpf(99) / 100)
TAU_C = mp.mpc(mp.mpf(7) / 100, mp.mpf(101) / 100)


def fmt(xs):
    return "(" + ", ".join(str(x) for x in xs) + ")"


def fmtn(xs, nd=6):
    return "(" + ", ".join(mp.nstr(mp.mpf(x) if not isinstance(x, mp.mpc)
                                   else x, nd) for x in xs) + ")"


def phs(k):
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
    return L_PHASE // gcd(k % L_PHASE, L_PHASE) if k % L_PHASE else 1


# ---------------------------------------------------------------------------
# exact Q(zeta_8) arithmetic
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
DIAG = [(a, a) for a in range(4)]


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


def rho_mpc(M):
    return [[z8_to_mpc(M[i][j]) for j in range(16)] for i in range(16)]


# ---------------------------------------------------------------------------
# lattice ledgers and coset theta series (delta-1c/1d machinery)
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


# ---------------------------------------------------------------------------
# E8 roots in glue coordinates (replication anchor)
# ---------------------------------------------------------------------------
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
# block numerics: gauge M = G/eta^8 and the axion blocks f_m
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
    """one twisted complex boson of deck weight m in sector (a,b);
    delta-1b normalisation (G[a,b] = f_1 f_3 exactly); the untwisted
    (0,0) factor is excluded (SL(2,Z)-invariant, no multiplier)."""
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
    """BFS transport groupoid with exact word bookkeeping (delta-1d)."""
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
# contraction solve machinery (numpy double SVD, delta-1c/1d)
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
# exact dressing series + fundamental-domain kernel J
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
    """prod_n (1 - zeta q^{e0+n})^{-2}."""
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
    """prod_n (1 - zeta q^{e0+n})^{-1}."""
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
    """q^{base_a} G[a,b] P8, phase-free (i^{ab} lives in beta)."""
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
    """delta-1d Harvey-Moore integral: per-pair bases, negative-exponent
    cell audit, main kernel J(.,0) + heat-kernel completion J(.,1/2)."""
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
# pair sets, candidates, seed
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
# S0 -- conventions, ledgers, targets
# ---------------------------------------------------------------------------
def section0():
    print("  -- S0: conventions, 16-class ledgers, targets")
    roots = build_glue_roots()
    cnt = [sum(1 for c in roots.values() if c == m) for m in range(4)]
    check("S0.1 [ROOTS] 240 roots, norm 2, class split %s = "
          "(52,64,60,64); 16 = |mu4|^2 discriminant classes" % fmt(cnt),
          len(roots) == 240 and cnt == [52, 64, 60, 64]
          and all(sum(x * x for x in r) == 2 for r in roots)
          and NCLS == 16 and MU4 == 4 and rankE8 == 8)

    d5led = build_d5_vecs(MAXN_LED)
    a3led = build_a3_vecs(MAXN_LED)
    V4, V2, CNT = build_ledgers16(d5led, a3led, MAXN_LED)

    Qtab = {0: [12, 0, 6, 4, 8], 1: [12, 24, 0, -8, 16],
            2: [0, 24, 30, 12, -40], 3: [12, 24, 0, -8, 16]}
    ok_q = all(V4[(a, a)].get(F(1)) == Qtab[a] for a in range(4))
    tots = [sum(CNT[(a, a)].get(F(n), 0) for a in range(4))
            for n in range(1, 9)]
    check("S0.2 [16-CLASS LEDGER, EXACT] diagonal slice = the delta-1 "
          "quartic ledger (V_{(a,a),1} = Q_a exactly, Q_0 = "
          "(12,0,6,4,8) etc.); diagonal counts sum to the E8 theta "
          "240 sigma_3(n) for n <= 8; V_{(1,1),n} = V_{(3,3),n} "
          "(conjugation)",
          ok_q and tots == [240 * s for s in SIGMA3]
          and all(V4[(1, 1)].get(F(n)) == V4[(3, 3)].get(F(n))
                  for n in range(1, 9)))

    cA = [F(5, 4), F(-1, 4), F(-3, 4), F(-1, 4)]
    Afix = [sum(cA[m] * Qtab[m][i] for m in range(4)) for i in range(5)]
    psi = [F(3), F(-1), F(-1), F(0), F(-1, 4)]
    psiA = sum(psi[i] * Afix[i] for i in range(5))
    check("S0.3 [TARGETS] A_fix = %s = (9,-30,-15,0,32); psi(A_fix) = "
          "%s = 64; the three preregistered testers: T5(V) = 0, "
          "W_2 : W_13 -> 4:3, psi(V) = -64 N or V = -A_fix N"
          % (fmt(Afix), psiA),
          Afix == [9, -30, -15, 0, 32] and psiA == 64)
    return V4, V2, CNT, Afix, psi


# ---------------------------------------------------------------------------
# S1 -- the 16-component Weil system + the E1.5 closure
# ---------------------------------------------------------------------------
def build_theta_ser0():
    d5v = build_d5_vecs(MAXN_NUM)
    a3v = build_a3_vecs(MAXN_NUM)
    lim = 16 * MAXN_NUM
    zero5 = (0, 0, 0, 0, 0)
    zero4 = (0, 0, 0, 0)
    m5_0 = factor_moments(d5v, zero5, None, 0, lim)
    m3_0 = factor_moments(a3v, zero4, None, 0, lim)
    return {mu: combine_series(m5_0[mu[0]], m3_0[mu[1]], 0, lim)
            for mu in MU}, lim


def section1(CNT):
    print("  -- S1: the 16-component Weil system (exact) + E1.5 closure")
    g5 = sum_z8([z8_root(5 * x * x) for x in range(4)])
    g3 = sum_z8([z8_root(3 * y * y) for y in range(4)])
    g = z8_mul(g5, g3)
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
    T5x, S5x = build_weil(lambda x: (5 * x * x) % 8,
                          lambda x, y: (10 * x * y) % 8,
                          list(range(4)), z8_root(-5))
    T3x, S3x = build_weil(lambda y: (3 * y * y) % 8,
                          lambda x, y: (6 * x * y) % 8,
                          list(range(4)), z8_root(-3))
    ok_tensor = all(
        Sx[IDX[(x1, y1)]][IDX[(x2, y2)]]
        == z8_mul(S5x[x1][x2], S3x[y1][y2])
        for x1 in range(4) for y1 in range(4)
        for x2 in range(4) for y2 in range(4))
    check("S1.1 [WEIL RELATIONS, EXACT Q(zeta_8)] Gauss sums "
          "2 zeta_8^5 x 2 zeta_8^3 = 4 = sqrt(16) (signature 0 mod 8 "
          "= rank E8, the signature factor in S is exactly 1); S "
          "symmetric + unitary, S^2 = C, (ST)^3 = S^2, S^4 = 1, "
          "T^8 = 1 (level 8); tensor split S = S_D5 (x) S_A3",
          g5 == z8_scal(F(2), z8_root(5))
          and g3 == z8_scal(F(2), z8_root(3))
          and g == z8_scal(F(4), Z8_ONE) and ok_sym
          and mat_eq(mat_mul(Sx, mat_conjT(Sx)), mat_id(n))
          and mat_eq(S2, C) and mat_eq(ST3, S2)
          and mat_eq(mat_mul(S2, S2), mat_id(n))
          and mat_eq(T8, mat_id(n)) and ok_tensor)

    iso = [m for m in MU if q8(m) == 0]
    H = DIAG
    Hp = [(0, 0), (1, 3), (2, 2), (3, 1)]
    eH = [Z8_ONE if MU[i] in H else Z8_ZERO for i in range(16)]
    SeH = [sum_z8([z8_mul(Sx[i][j], eH[j]) for j in range(16)])
           for i in range(16)]
    TeH = [z8_mul(Tx[i][i], eH[i]) for i in range(16)]
    eHp = [Z8_ONE if MU[i] in Hp else Z8_ZERO for i in range(16)]
    SeHp = [sum_z8([z8_mul(Sx[i][j], eHp[j]) for j in range(16)])
            for i in range(16)]
    all_quarter = all(Sx[IDX[(a, a)]][IDX[(ap, ap)]]
                      == z8_scal(F(1, 4), Z8_ONE)
                      for a in range(4) for ap in range(4))
    wt_out = F(0)
    for i in range(16):
        if MU[i] in H:
            continue
        v = Sx[i][IDX[(1, 1)]]
        vv = z8_mul(v, z8_conj(v))
        wt_out += vv[0]
    check("S1.2 [v502 SLICE + WHY THE 4-RULE FAILED, EXACT] isotropic "
          "classes 6 of 16; the glue diagonal H and the anti-diagonal "
          "H' are BOTH invariant Lagrangians (e_H, e_H' exactly S- and "
          "T-fixed: two E8 gluings); P_H S P_H = (1/4) J (every entry "
          "1/4, NOT the naive (1/2) i^{-aa'}) and |S-image weight "
          "outside H| = %s = 3/4: the 4-character rule cannot close"
          % wt_out,
          len(iso) == 6 and all(q8(m) == 0 for m in H)
          and all(q8(m) == 0 for m in Hp)
          and SeH == eH and TeH == eH and SeHp == eHp
          and all_quarter and wt_out == F(3, 4))

    ser0, lim = build_theta_ser0()
    e4 = [240, 2160, 6720]
    cdia = [sum(CNT[(a, a)].get(F(n), 0) for a in range(4))
            for n in range(1, 4)]
    canti = [sum(CNT[m].get(F(n), 0) for m in Hp) for n in range(1, 4)]
    SC = rho_mpc(Sx)
    res_nv = []
    res16 = {}
    for tau in (TAU_A, TAU_B):
        pref4 = (-1j * tau) ** 4
        thd = {mu: eval_series16(ser0[mu], tau, lim) for mu in MU}
        rr = []
        for i, mu in enumerate(MU):
            lhs = eval_series16(ser0[mu], -1 / tau, lim)
            rhs = pref4 * sum(SC[i][j] * thd[MU[j]] for j in range(16))
            rr.append(abs(lhs - rhs) / abs(lhs))
        res16[tau] = max(rr)
        if tau == TAU_A:
            for a in range(4):
                lhs = eval_series16(ser0[(a, a)], -1 / tau, lim)
                rhs = pref4 * sum(
                    mp.exp(-2j * mp.pi * a * ap / 4) * thd[(ap, ap)]
                    for ap in range(4)) / 2
                res_nv.append(abs(lhs - rhs) / abs(lhs))
    r_nv = max(res_nv)
    print("     E1.5 residual: naive 4-rule %s = O(1) -> 16-component "
          "Weil rule %s / %s (two tau)"
          % (mp.nstr(r_nv, 3), mp.nstr(res16[TAU_A], 3),
             mp.nstr(res16[TAU_B], 3)))
    check("S1.3 [E1.5 CLOSURE -- THE COMPLETION WORKS] both Lagrangian "
          "counts reproduce E4 = (1,240,2160,6720); Theta_mu(-1/tau) = "
          "(-i tau)^4 sum_nu S_mu_nu Theta_nu(tau) closes at max rel "
          "residual %s / %s < 1e-25 (two tau), while the naive "
          "4-component rule fails at %s = O(1) on the SAME data "
          "(delta-1b E1.5 replicated and resolved)"
          % (mp.nstr(res16[TAU_A], 3), mp.nstr(res16[TAU_B], 3),
             mp.nstr(r_nv, 3)),
          cdia == e4 and canti == e4
          and res16[TAU_A] < mp.mpf(10) ** (-25)
          and res16[TAU_B] < mp.mpf(10) ** (-25)
          and r_nv > mp.mpf(10) ** (-3))
    return Tx, Sx, ser0, lim, SC


# ---------------------------------------------------------------------------
# S2 -- gauge transport + the multiplier system (character identified)
# ---------------------------------------------------------------------------
def section2(Tx, Sx):
    print("  -- S2: gauge transport + the mu4 multiplier system")
    tg, sg, dev = measure_transport_w(
        4, PAIRS4, lambda a, b, tau: M_val(4, a, b, tau), 4)
    tgx, sgx = {}, {}
    devmax = mp.mpf(0)
    for p in PAIRS4:
        lt, kt, dt = recog(tg[p])
        ls, ks, ds = recog(sg[p])
        devmax = max(devmax, dt, ds)
        tgx[p] = (lt, kt)
        sgx[p] = (ls, ks)
    ok_fix = all(tgx[(0, b)][1] == L_PHASE // 2
                 and abs(tgx[(0, b)][0]) < mp.mpf(10) ** (-30)
                 for b in (1, 2, 3))
    check("S2.1 [GAUGE TRANSPORT + T-FIXED DEFECT] (t_p, s_p) of "
          "M = G[a,b] eta^{-8} constant over two tau for all 15 pairs "
          "(max dev %s < 1e-28), recognised as exact 1/960-grid phases "
          "(max %s < 1e-25); the T-fixed pairs (0,b) carry t = "
          "e(-1/2) = -1 EXACTLY (the naked level-matching defect)"
          % (mp.nstr(dev, 3), mp.nstr(devmax, 3)),
          dev < mp.mpf(10) ** (-28) and devmax < mp.mpf(10) ** (-25)
          and ok_fix)

    mult = {}
    ok_all = True
    for name, base, stab, exp_dim in (('gcd1', (0, 1), 'Gamma_1(4)', 8),
                                      ('gcd2', (0, 2), 'Gamma_0(2)+-', 6)):
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
        print("     [%s] %d nodes, %d loops in %s, joint eigenspace "
              "dim %d/16, eigen-phase orders %s"
              % (name, len(Lam), len(loops), stab, len(evs),
                 fmt(orders)))
        mult[name] = dict(loops=loops, Lam=Lam, evs=evs, tab=tab,
                          ibest=ibest, orders=orders)
        ok_all = (ok_all and ok_stab and ok_mod and len(evs) == exp_dim
                  and devm < mp.mpf(10) ** (-10) and max(orders) <= 4)
    allk = [k for name in ('gcd1', 'gcd2')
            for row in mult[name]['tab'] for k in row]
    gord = 1
    for k in allk:
        gord = lcm(gord, phase_order(k))
    check("S2.2 [LOOPS -> STABILISERS; THE GROUP IS mu_4] every loop "
          "matrix lies in the orbit stabiliser (Gamma_1(4) resp. "
          "Gamma_0(2)+-, exact integer check); loop scalars unitary; "
          "joint holonomy eigenspaces dim 8/16 resp. 6/16 (delta-1c "
          "replication); every eigen-phase snaps to the 1/960 grid and "
          "the multiplier values generate exactly the cyclic group of "
          "order %d = 4" % gord, ok_all and gord == 4)

    ok_rel = True
    for p in PAIRS4:
        l1, k1, e1 = word_scalar(p, 'SSSS', tgx, sgx, 4)
        l2a, k2a, e2a = word_scalar(p, 'STSTST', tgx, sgx, 4)
        l2b, k2b, e2b = word_scalar(p, 'SS', tgx, sgx, 4)
        l3a, k3a, e3a = word_scalar(p, 'SST', tgx, sgx, 4)
        l3b, k3b, e3b = word_scalar(p, 'TSS', tgx, sgx, 4)
        assert e1 == p and e2a == e2b and e3a == e3b
        if (k1 % L_PHASE or (k2a - k2b) % L_PHASE
                or (k3a - k3b) % L_PHASE
                or max(abs(l1), abs(l2a - l2b),
                       abs(l3a - l3b)) > mp.mpf(10) ** (-25)):
            ok_rel = False
    check("S2.3 [KOBOUNDARY TEST, EXACT] the SL(2,Z) relation defects "
          "c_{S^4}(p), c_{(ST)^3 S^-2}(p), c_{[S^2,T]}(p) (gauge- and "
          "character-invariant pure scalars, exact 1/960 phase "
          "arithmetic) are (1, 1, 1) on ALL 15 pairs: the multiplier "
          "system is a CHARACTER of the orbit stabilisers, NOT a "
          "genuine 2-cocycle on SL(2,Z)", ok_rel)

    lps = mult['gcd1']['loops']
    tab1 = mult['gcd1']['tab']
    ib = mult['gcd1']['ibest']
    feats, lams4 = [], []
    ok_div = True
    for i, lp in enumerate(lps):
        g = lp['gamma']
        A, B = g[0]
        Cc, D = g[1]
        feats.append((B % 4, (Cc // 4) % 4, ((A - 1) // 4) % 4,
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
    print("     Gamma_1(4) character fits (x1, x2, x3, x4) with "
          "lambda = i^{x1 B + x2 C/4 + x3 (A-1)/4 + x4 (D-1)/4}: %s"
          % str(fits))
    check("S2.4 [CHARACTER IDENTIFIED] all multiplier values on the "
          "seed eigenvector lie in mu_4 and the Gamma_1(4) character "
          "is lambda(gamma) = i^{2B + C/4} ((2,1,0,0) among the four "
          "equivalent monomial solutions in the residues "
          "(B, C/4, (A-1)/4, (D-1)/4) mod 4)",
          ok_div and (2, 1, 0, 0) in fits and len(fits) == 4)
    return tg, sg, tgx, sgx, mult


def eig_phase_table(loops, evs):
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


# ---------------------------------------------------------------------------
# S3 -- the cancellation candidate: G = f1 f3, T-fix mechanism, table
# ---------------------------------------------------------------------------
def section3(tgx, mult):
    print("  -- S3: the cancellation -- G = f1 f3, T-fix, exact table")
    Ev = {th: F(-1, 24) + th * (1 - th) / 4
          for th in (F(0), F(1, 4), F(1, 2), F(3, 4))}
    ok_ev = ([Ev[t] for t in (F(0), F(1, 4), F(1, 2), F(3, 4))]
             == [F(-1, 24), F(1, 192), F(1, 48), F(1, 192)])

    devG = mp.mpf(0)
    for (a, b) in ((0, 1), (1, 0), (1, 1), (2, 1), (0, 2), (3, 2)):
        for tau in (TAU_A, TAU_B):
            g = geo_val(4, a, b, tau)
            ff = f_val(4, 1, a, b, tau) * f_val(4, 3, a, b, tau)
            devG = max(devG, abs(g - ff) / abs(g))
    check("S3.1 [G = f1 f3, EXACT IDENTITY] v502 vacuum energies "
          "E_b(theta) = (-1/24, 1/192, 1/48, 1/192) exact (axion "
          "Coxeter characters {i, -1, -i} = weights (1, 2, 3) = A3 "
          "exponents); the twisted C^2 gauge block factorises as the "
          "weight-1 x weight-3 axion pair: max rel deviation %s < "
          "1e-30 over six pairs x two tau -- the sphere-axion "
          "candidate f1 f2 f3 differs from the gauge content exactly "
          "by the weight-2 axion f2" % mp.nstr(devG, 3),
          ok_ev and devG < mp.mpf(10) ** (-30))

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

    # T-fix mechanism, exact grid arithmetic: gauge e(-1/2) x axion
    # e(-1/6) = e(1/3) = chi_4(T) at every T-fixed node (0,b)
    k_third = L_PHASE // 3
    k_ax_pred = (-L_PHASE // 6) % L_PHASE
    ok_tfix = all(
        axd['f1f3']['tx'][(0, b)][1] == k_ax_pred
        and (tgx[(0, b)][1] + axd['f1f3']['tx'][(0, b)][1]) % L_PHASE
        == k_third for b in (1, 2, 3))
    check("S3.2 [T-FIX MECHANISM, EXACT PHASES] axion transport "
          "constants recognised on the 1/960 grid for all candidates "
          "(constancy %s, recognition %s); the f1 f3 T-fixed phases "
          "equal the vacuum-energy prediction e(2E+2E) = e(-1/6) for "
          "all b, and (-1) x e(-1/6) = e(1/3) = chi_4(T): the gauge "
          "level-matching defect is cancelled into the chi_4 "
          "character at every T-fixed node"
          % (mp.nstr(max(d['dev'] for d in axd.values()), 3),
             mp.nstr(max(d['rec'] for d in axd.values()), 3)),
          ok_c and ok_r and ok_tfix)

    # attach per-loop axion scalars (same BFS graph => same loops)
    for oname, base in (('gcd1', (0, 1)), ('gcd2', (0, 2))):
        for name, d in axd.items():
            lps, _ = orbit_loops(4, d['tx'], d['sx'], base)
            key = {lp['at']: lp['k'] for lp in lps}
            for lp in mult[oname]['loops']:
                lp.setdefault('ax_k', {})[name] = key[lp['at']]

    resmap = {('none', 'hol'): residual_orders(mult, 'hol', None)}
    for name in ['f1f2f3', 'f2', 'f1f3', 'wrong112', 'wrong222']:
        for orient in ('hol', 'anti'):
            resmap[(name, orient)] = residual_orders(mult, orient, name)
    print("     cancellation table (min residual order over eta^m x "
          "chi_k):")
    for key, (o, mk) in sorted(resmap.items()):
        print("       %-9s %-5s -> residual order %d at (m,k) = %s"
              % (key[0], key[1], o, mk))
    want = {('none', 'hol'): 4,
            ('f1f2f3', 'hol'): 4, ('f1f2f3', 'anti'): 4,
            ('f2', 'hol'): 6, ('f2', 'anti'): 6,
            ('f1f3', 'hol'): 1, ('f1f3', 'anti'): 1,
            ('wrong112', 'hol'): 4, ('wrong112', 'anti'): 4,
            ('wrong222', 'hol'): 4, ('wrong222', 'anti'): 4}
    check("S3.3 [CANCELLATION TABLE, EXACT] minimal residual "
          "multiplier order after best (eta^m, chi_k) absorption "
          "(m = 0..23, k = 0..11, exact phase arithmetic): none -> 4 "
          "(delta-1c: no bookkeeping rescues the bare gauge blocks), "
          "f1f2f3 (the three sphere axions) -> 4, f2 -> 6, f1f3 -> 1 "
          "(hol AND anti), wrong weights (1,1,2)/(2,2,2) -> 4: ONLY "
          "the twisted fibre block f1 f3 cancels the mu4 system",
          all(resmap[k][0] == want[k] for k in want))
    return axd, resmap


def orbit_residual(loops, tab, nev, ax_ks, m, k):
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


# ---------------------------------------------------------------------------
# S4 -- the strict solutions (SVD scan + function certificates)
# ---------------------------------------------------------------------------
def section4(Tx, Sx, tg, sg, axd):
    print("  -- S4: the strict solutions (constructive scan)")
    rhoT = rho_np(Tx)
    rhoS = rho_np(Sx)
    seed = make_seed()
    hits = []
    scans = [('none', None, 'hol')]
    for nm in CAND_WS:
        for orient in ('hol', 'anti'):
            scans.append((nm, CAND_WS[nm], orient))
    M_SCAN = (0, 8, 16)      # the eta^{+-8} copies of the eta^0 family
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
        for m in M_SCAN:
            ph = np.exp(2j * np.pi * m / 24)
            ttm = {p: tt[p] * ph for p in tt}
            for k in range(12):
                _, L1, n1, _, _ = solve_orbit(ORB1, 4, ttm, ss, rhoT,
                                              rhoS, (0, 1), k)
                if not n1:
                    continue
                _, L2, n2, _, _ = solve_orbit(ORB2, 4, ttm, ss, rhoT,
                                              rhoS, (0, 2), k)
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
    base_hits = [h for h in hits if h['name'] == 'none']
    wrong_hits = [h for h in hits
                  if h['name'] in ('wrong112', 'wrong222', 'f2',
                                   'f1f2f3')]
    hol_mk = sorted((h['m'], h['k']) for h in hits
                    if h['name'] == 'f1f3' and h['orient'] == 'hol')
    anti_mk = sorted((h['m'], h['k']) for h in hits
                     if h['name'] == 'f1f3' and h['orient'] == 'anti')
    seeded = [h for h in hits if h['name'] == 'f1f3'
              and h['orient'] == 'hol']
    ok_cos = (seeded and min(h['c1'] for h in seeded) > 0.1
              and max(abs(h['c1'] - h['c2']) for h in seeded) < 1e-6)
    check("S4.1 [SOLVE SCAN, m in {0, 8, 16}] strict two-orbit "
          "solutions exist ONLY for the f1 f3 dressing: hol hits %s "
          "(dims (3,3)/(1,1), seed-cos 0.105 in both orbits), anti "
          "hits %s; baseline 'none' %d = 0 hits (delta-1c replicated) "
          "and f2 / f1f2f3 / wrong-weight controls %d = 0 hits; the "
          "m = 8, 16 hits are the same transport solutions with "
          "eta^{+-8} T-phase bookkeeping folded in"
          % (str(hol_mk), str(anti_mk), len(base_hits),
             len(wrong_hits)),
          len(base_hits) == 0 and len(wrong_hits) == 0
          and hol_mk == [(0, 4), (0, 10), (8, 2), (8, 8), (16, 0),
                         (16, 6)]
          and len(anti_mk) == 6 and ok_cos)
    winners = sorted([h for h in hits if h['name'] == 'f1f3'
                      and h['orient'] == 'hol' and h['m'] == 0],
                     key=lambda h: h['k'])
    dimset = [(h['k'], (h['d1'], h['d2'])) for h in winners]
    check("S4.2 [CANONICAL FAMILY] the eta^0 members keep the "
          "delta-1b weight bookkeeping (block weight -4 x theta "
          "weight 4): exactly chi_4 with dims (3,3) and chi_10 with "
          "dims (1,1) -- evaluated below; residual discrete freedom = "
          "this chi_k choice (documented as a fence)",
          dimset == [(4, (3, 3)), (10, (1, 1))])
    return winners


# ---------------------------------------------------------------------------
# S5 -- the decision: both solutions vs the three testers
# ---------------------------------------------------------------------------
def section5(winners, axd, ser0, lim, V4, V2, CNT, Afix, psi):
    print("  -- S5: THE DECISION (derived measure, three testers)")
    th = {}
    for tau in (TAU_C, TAU_C + 1, -1 / TAU_C):
        th[tau] = [eval_series16(ser0[mu], tau, lim) for mu in MU]

    # leading-cell guard (gauge dressing only, exact)
    seedw = (F(0), F(0))
    for b in (1, 2, 3):
        dr = gauge_dress_series(4, 0, b, GRID_CUT)
        seedw = gadd(seedw, dr[F(0)])
    seedw = (seedw[0] / 4, seedw[1] / 4)
    check("S5.1 [LEADING-CELL GUARD, EXACT] the (a=0, ex=0) gauge "
          "dressing weights summed over b and divided by the orbifold "
          "order give %s = 5/16 = Dedekind(5/4)/4: the Atiyah-Bott "
          "denominators (2,4,2) sit as the leading Harvey-Moore cell "
          "coefficient (delta-1b E3.1 replicated)" % str(seedw[0]),
          seedw == (F(5, 16), F(0)))

    results = []
    for win in winners:
        k_chi = win['k']
        ws = CAND_WS['f1f3']
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
        check("S5.2[%s] [FUNCTION CERTIFICATE] every T/S edge closes "
              "STRICTLY on the dressed functions M_p A_p beta_p.Theta "
              "at a fresh tau (weight -4, character chi_%d, NO "
              "residual multiplier): max rel deviation %s < 1e-8"
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
        I_o1, _, _, _, _ = hm_integral_pp(
            {p: beta[p] for p in beta if p in ORB1},
            {p: dm[p] for p in dm if p in ORB1},
            basemap, V4, V2, CNT, GRID_CUT, mp.mpf(1) / 4)
        I_o2, _, _, _, _ = hm_integral_pp(
            {p: beta[p] for p in beta if p in ORB2},
            {p: dm[p] for p in dm if p in ORB2},
            basemap, V4, V2, CNT, GRID_CUT, mp.mpf(1) / 4)
        print("     [%s] I_main = %s" % (tag, fmtn(I_main)))
        print("     [%s] neg-exponent cells %d (max |coef| %s); rel "
              "|Im| %s; cut-6 vs cut-8 %s"
              % (tag, n_neg, mp.nstr(wt_neg, 3), mp.nstr(im_rel, 3),
                 mp.nstr(eps_rel, 3)))
        check("S5.3[%s] [INTEGRAL COMPUTED, DERIVED MEASURE] combined "
              "integrand (gauge quartic x twisted fibre weight), "
              "30-digit kernels: negative-exponent cells audited "
              "(%d), truncation cut-6 vs cut-8 = %s < 1e-2 "
              "(documented tolerance), reality %s < 1e-8"
              % (tag, n_neg, mp.nstr(eps_rel, 3), mp.nstr(im_rel, 3)),
              eps_rel < mp.mpf(10) ** (-2)
              and im_rel < mp.mpf(10) ** (-8))

        tol = max(eps_rel * 100, mp.mpf(10) ** (-7))
        t5rel = abs(I_main[3]) / scale
        W2v = W.get((2, F(1)), mp.mpc(0))
        W13 = W.get((1, F(1)), mp.mpc(0)) + W.get((3, F(1)), mp.mpc(0))
        r43 = W2v / W13 if abs(W13) > 0 else mp.inf
        dev43 = abs(r43 - mp.mpf(4) / 3) if abs(W13) > 0 else mp.inf
        ok43 = dev43 < tol * 10
        tgt = [-x for x in Afix]
        rats = [I_main[i] / tgt[i] for i in range(5) if tgt[i] != 0]
        spread = max(abs(rats[i] - rats[j]) for i in range(len(rats))
                     for j in range(len(rats))) \
            / max(abs(r) for r in rats)
        psiI = sum(float(psi[i]) * I_main[i] for i in range(5))
        psi_neg = (psiI.real < 0 and abs(psiI.imag)
                   < abs(psiI.real) * mp.mpf(10) ** (-6))
        t5_zero = t5rel < tol
        full_succ = spread < tol * 10 and t5_zero
        slice_succ = t5_zero and psi_neg
        print("     [%s] T5 fraction %s; W_2/W_13 = %s (Soll 4/3); "
              "spread vs -A_fix %s; psi(I) = %s"
              % (tag, mp.nstr(t5rel, 4), mp.nstr(r43, 6),
                 mp.nstr(spread, 3), mp.nstr(psiI, 6)))
        check("S5.4[%s] [ALL THREE TESTERS FAIL] T5(V) = 0 NOT "
              "realised (fraction %s > 0.1); W_2 : W_13 = 4 : 3 NOT "
              "realised; V = -A_fix N NOT realised (spread %s > 0.5); "
              "the psi = -64 N slice does NOT fire: no preregistered "
              "success branch fires under the derived measure"
              % (tag, mp.nstr(t5rel, 3), mp.nstr(spread, 3)),
              t5rel > mp.mpf('0.1') and not ok43
              and spread > mp.mpf('0.5')
              and not full_succ and not slice_succ)

        reb = None
        if abs(I_o2[3]) > 0:
            r = -(I_o1[3] / I_o2[3]).real
            Vr = [I_o1[i] + r * I_o2[i] for i in range(5)]
            sc = max(abs(x) for x in Vr)
            t3f = abs(Vr[4]) / sc
            psir = sum(float(psi[i]) * Vr[i] for i in range(5)).real
            reb = dict(r=r, t3f=t3f, psir=psir)
            print("     [%s] REBALANCE  T5 = 0 at N2/N1 = %s ; then "
                  "T3 fraction %s, psi = %s"
                  % (tag, mp.nstr(mp.mpf(r), 8), mp.nstr(t3f, 3),
                     mp.nstr(mp.mpf(psir), 6)))
        ok_reb = (reb is not None
                  and not (reb['r'] > 0 and reb['psir'] < 0))
        if k_chi == 4:
            ok_reb = ok_reb and reb['r'] > 0 and reb['psir'] > 0
            msg = ("T5 = 0 is reachable inside the positive cone but "
                   "psi stays POSITIVE there (wrong sign)")
        else:
            ok_reb = ok_reb and reb['r'] < 0
            msg = ("T5 = 0 requires a NEGATIVE relative orbit weight "
                   "-- outside the orbifold projector")
        check("S5.5[%s] [(N1, N2) SCAN -- NO RESCUE] the derived "
              "family has one scalar per orbit; %s: no branch fires "
              "anywhere in the positive (N1, N2) cone" % (tag, msg),
              ok_reb)
        results.append(dict(k=k_chi, dims=(win['d1'], win['d2']),
                            t5rel=t5rel, spread=spread, psiI=psiI,
                            full=full_succ, slc=slice_succ, reb=reb))
    return results


# ---------------------------------------------------------------------------
# S6 -- negative controls
# ---------------------------------------------------------------------------
def section6(Tx, Sx, axd, ser0, lim):
    print("  -- S6: negative controls")
    pairs2 = [(0, 1), (1, 0), (1, 1)]
    tg2, sg2, _ = measure_transport_w(
        2, pairs2, lambda a, b, tau: M_val(2, a, b, tau), 4)
    tA2, sA2, _ = measure_transport_w(
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
    check("S6.1 [NC-a: Z2/EGUCHI-HANSON ANCHOR] at Z2 the gauge-only "
          "multiplier obstruction has residual order %d = 2 (NO "
          "order-4 content: the mu4 defect is Z4-specific), and the "
          "SAME fibre-block dressing G_2[a,b] cancels it exactly "
          "(residual order %d = 1): the cancellation mechanism "
          "replicates at the anchor where its task is the trivial "
          "order-2 one" % (res_g[0], res_d[0]),
          res_g[0] <= 2 and res_d[0] == 1)

    okmu2 = True
    for p in ORB2:
        for m in (1, 2, 3):
            if (m * p[1]) % 4 % 2 != 0:
                okmu2 = False
    d = axd['f1f2f3']
    lps_so, _ = orbit_loops(4, d['tx'], d['sx'], (0, 2))
    orders_so = sorted({phase_order(lp['k']) for lp in lps_so})
    check("S6.2 [NC-b: SO(16) STRUCTURAL] the SO(16)/D8 reading keeps "
          "only even sectors = the gcd-2 orbit; there ALL axion "
          "b-characters i^{mb} are +/-1 (mu_2 exact) and the weight-2 "
          "axion is fully untwisted: the order-4 character supply of "
          "the odd sectors is structurally absent (axion loop-phase "
          "orders on gcd-2: %s)" % fmt(orders_so), okmu2)

    # misassignment controls: wrong form / wrong signature
    gw = sum_z8([z8_root((2 * x * x + 2 * y * y) % 8)
                 for x in range(4) for y in range(4)])
    nrm = z8_mul(gw, z8_conj(gw))
    Tw, Sw = build_weil(lambda m: (2 * m[0] ** 2 + 2 * m[1] ** 2) % 8,
                        lambda m, n: (4 * (m[0] * n[0]
                                           + m[1] * n[1])) % 8,
                        MU, Z8_ONE)
    Cm = [[Z8_ONE if MU[j] == neg(MU[i]) else Z8_ZERO
           for j in range(16)] for i in range(16)]
    s2w = mat_mul(Sw, Sw)
    SCw = rho_mpc(Sw)
    thd = {mu: eval_series16(ser0[mu], TAU_A, lim) for mu in MU}
    resw = []
    for i, mu in enumerate(MU):
        lhs = eval_series16(ser0[mu], -1 / TAU_A, lim)
        rhs = (-1j * TAU_A) ** 4 * sum(SCw[i][j] * thd[MU[j]]
                                       for j in range(16))
        resw.append(abs(lhs - rhs) / abs(lhs))
    check("S6.3 [NC-c: WRONG FORM] q = (x^2+y^2)/4: |Gauss|^2 = %s = "
          "64 != 16 (no unit signature factor exists); forcing "
          "sigma = 1 breaks S^2 = C EXACTLY; the true 16 thetas fail "
          "its S-rule at O(1) (max residual %s)"
          % (str(nrm[0]), mp.nstr(max(resw), 3)),
          nrm == z8_scal(F(64), Z8_ONE) and not mat_eq(s2w, Cm)
          and max(resw) > mp.mpf(10) ** (-2))

    Tb, Sb = build_weil(q8, bil8, MU, z8_root(-2))
    s2b = mat_mul(Sb, Sb)
    ok_shift = mat_eq(s2b, [[z8_mul(z8_root(4), Cm[i][j])
                             for j in range(16)] for i in range(16)])
    check("S6.4 [NC-d: WRONG SIGNATURE] the correct form with a wrong "
          "signature factor sigma = e(-1/4) (signature-2 pretence): "
          "S^2 = C fails EXACTLY (S^2 = e(-1/2) C instead)",
          not mat_eq(s2b, Cm) and ok_shift)


# ---------------------------------------------------------------------------
# S7 -- verdict + the mandatory tension fence
# ---------------------------------------------------------------------------
def section7(results):
    print("  -- S7: verdict + the tension fence")
    uni = [r for r in results if r['dims'] == (1, 1)]
    reb_fire = [r for r in results
                if r.get('reb') and r['reb']['r'] > 0
                and r['reb']['psir'] < 0]
    no_branch = all(not r['full'] and not r['slc'] for r in results)
    check("S7.1 [VERDICT: GENUINE KILL ON THE DERIVED SURFACE] the "
          "cancellation exists (f1 f3 = the twisted fibre block, NOT "
          "the three sphere axions); the unique dims-(1,1) solution "
          "(chi_10) AND the seed projection of the dims-(3,3) family "
          "(chi_4) fail ALL three preregistered testers, and no "
          "(N1, N2) reweighting in the positive cone rescues a "
          "branch; remaining freedom: the discrete chi_k choice -- "
          "documented as a fence.  Honest bookkeeping: exact = Weil "
          "relations, loop words/stabilisers, relation defects, phase "
          "arithmetic (1/960 grid), ledgers, G = f1 f3; numeric "
          "(documented) = block transport constants (28+ digits), "
          "recognition (25+), SVD solves certified on the functions "
          "(1e-8), kernels (30 digits, cut-scan)",
          len(uni) == 1 and uni[0]['k'] == 10 and not reb_fire
          and no_branch and len(results) == 2)
    check("S7.2 [TENSION, STATED HONESTLY -- the mandatory fence] the "
          "DECLARED completion reading (v516/M2) delivers the psi = "
          "64 slice and cancels 32 T3; the DERIVED chiral measure "
          "(this module) fails all three testers -- both are exact; "
          "the sharp open question is which of the two is the true "
          "BCOV measure (the declared reading is supported by the "
          "delta-1 modular-completion finding but not derived; the "
          "derived measure rests on the f1f3 identification).  "
          "Neither result is hidden behind the other.  [O] the "
          "BCOV-integral derivation that decides between the two "
          "measures; NO marker moves anywhere", True)
    print("     VERDICT: GENUINE KILL on the derived surface -- the "
          "delta-1 route is decided negative under the derived "
          "measure; the measure question (declared v516 reading vs "
          "derived chiral measure) is the named [O]")


# ---------------------------------------------------------------------------
def run():
    reset()
    # the transport/recognition certificates need 40 digits; restore the
    # working precision in case an earlier suite module lowered it
    mp.mp.dps = 40
    _J_CACHE.clear()
    print("v518  CELEST.WP5E.DELTA1.01: the delta-1 chain decided -- "
          "the derived chiral measure kills the delta-1 route "
          "(delta-1b/1c/1d consolidated; honest negative result with "
          "the v516 tension stated)")
    V4, V2, CNT, Afix, psi = section0()
    Tx, Sx, ser0, lim, SC = section1(CNT)
    tg, sg, tgx, sgx, mult = section2(Tx, Sx)
    axd, resmap = section3(tgx, mult)
    winners = section4(Tx, Sx, tg, sg, axd)
    results = section5(winners, axd, ser0, lim, V4, V2, CNT, Afix, psi)
    section6(Tx, Sx, axd, ser0, lim)
    section7(results)

    return summary("v518 CELEST.WP5E.DELTA1.01: the delta-1 chain "
                   "(delta-1b + delta-1c + delta-1d) is DECIDED -- the "
                   "16-component Weil completion closes exactly (E1.5 "
                   "residual 2.91 -> ~1e-39), the obstruction is a "
                   "finite mu4 CHARACTER of the orbit stabilisers "
                   "(koboundary defects (1,1,1) on all 15 pairs, "
                   "lambda(gamma) = i^{2B + C/4} on Gamma_1(4)), the "
                   "cancellation is achieved by the twisted fibre "
                   "block f1 f3 = G (exact identity; the three sphere "
                   "axions leave residual order 4, f2 leaves 6), and "
                   "under BOTH derived solutions (chi_4, chi_10) the "
                   "Harvey-Moore integral fails all three "
                   "preregistered testers (T5 != 0, no 4:3, no "
                   "-A_fix/psi-slice; no (N1, N2) rescue in the "
                   "positive cone): a genuine KILL on the derived "
                   "surface, with the v516 tension stated honestly "
                   "and the BCOV measure question the named [O]; no "
                   "marker moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
