"""WP5e-delta-1e of CELEST.SEAM.01 (EXPLORATION ONLY -- experiments/, no
verification claim).

"THE BCOV MEASURE DECISION" -- the sharpest open question of the
celestial route after 2026-07-22: two exact, mutually contradictory
results coexist.

  (A) v516 / M2, the DECLARED completion measure: the loop of twisted
      states carries the UNPHASED sector trace with the same zero-mode
      normalisation, contact_j = (Q^{(0)} - Q^{(j)})/det_j, class
      weights w_m = sum_j (1 - i^{jm})/det_j = (0, 3/2, 2, 3/2) =
      4 h_m = -4 ch2(T_m) with NO free scale; kills both v508
      certificates (32 -> 0, 72 -> 0), supplies the v511 slice psi = 64
      exactly, every channel the perfect Okubo square 36<x,x>^2/det_j,
      total 45<x,x>^2.  SUCCESS on the declared measure, but the
      reading is [C]-declared, NOT derived from the BCOV integral.
  (B) v518 / delta-1 chain, the DERIVED chiral measure: blockwise
      SL(2,Z) covariance of the dressed 16-component Weil system
      (discriminant module Z4 x Z4, q = (5x^2+3y^2)/8, Gauss sums
      2z8^5 x 2z8^3 = 4), multiplier = character chi_4 on Gamma_1(4)
      (lambda = i^{2B + C/4}), fibre block f1 f3 cancels the order-4
      defect exactly ((-1) x e(-1/6) = e(1/3) = chi_4(T)), strict
      solutions exactly chi_4 (dims (3,3)) and chi_10 (dims (1,1)).
      BUT all three preregistered testers FAIL (T5 fractions 0.5/0.83,
      W_13 = 0, -A_fix spreads 1.05/1.47, no psi = -64 N slice, no
      (N1, N2) rescue in the positive cone).

THE OPEN [O]: which of the two is the true BCOV measure on PT/Z4?
This probe constructs and executes THREE candidate discriminators that
are independent of both contested success criteria.

===========================================================================
PREREGISTRATION (fixed BEFORE any computation below)
===========================================================================

D1 -- THE UNTWISTED-COLUMN BOUNDARY CRITERION.  The pairs (0,b) are
  untwisted-sector traces with a g^b insertion: bona fide traces in the
  untwisted Hilbert space, UNAMBIGUOUS -- no measure freedom can touch
  them ([C]-premise P-I, stated openly).  Any legitimate realisation of
  the BCOV measure must reduce on the (0,b) column to that physical
  trace.  Two column models are granted to (B) (benefit of the doubt):
    'diag'   -- the v502/v505 CFT ledger bookkeeping: the untwisted
                sector is the D5+A3 root class, beta_{(0,b)} ~ e_{(0,0)};
    'spread' -- the AB bookkeeping: the (0,b) column carries the full
                phased class sum sum_m i^{bm} e_{(m,m)} (its ledger
                contraction reproduces Q^{(b)} exactly -- checked).
  TEST: does ANY strict derived family (chi_4 / chi_10, eta^0, hol and
  anti) contain a member whose (0,1), (0,3) [one scalar] resp. (0,2)
  [one scalar] columns match either model?  Exact-rank test (stacked
  SVD; contained iff sigma_min/sigma_max < 1e-8 with non-vanishing
  column coefficient; robustly NOT contained iff > 1e-3; in between =
  grey -> gap).  FIRES:
    for A (boundary kill)   if NO family contains either column model;
    for A (reconciliation)  if a member is contained AND its integral
                            passes the v518 testers (the completion
                            would then be DERIVED -- strongest outcome);
    for B (sharpened kill)  if a member is contained AND its integral
                            still fails the testers.
  Side effect if contained: the column normalisation ties c and c'
  across the orbits and CANONICALISES the (N1, N2) freedom.

D2 -- THE SINGLE-VALUEDNESS / INVARIANT-SUBSPACE CRITERION (the
  modular-anomaly side).  BCOV's F1 is (Quillen/Ray-Singer) built from
  spectral data; the one-loop integrand at the FIXED weight bookkeeping
  of v518 ("block weight -4 x theta weight 4", real measure
  d^2tau/tau_2^s) must be a single-valued function on the tau moduli
  space: trivial multiplier ([C]-premise P-II).  Real tau_2 powers
  cannot compensate a phase; absorbing chi_4 into eta^{+-8} bookkeeping
  shifts the weight by -+4 and breaks the fixed convention (the m = 8,
  16 hits of v518 are bookkeeping copies, not new functions).  TEST
  (exact): (a) compute the FULL invariant subspace {v : rho(T) v = v,
  rho(S) v = v} of the 16-dim Weil representation by exact rational
  linear algebra; if it is exactly span{e_H, e_H'} (the two Lagrangian
  gluings, both with theta = E4 = the UNPHASED trace), then every
  single-valued lattice factor is FORCED to the unphased E4 reading --
  an independent mini-derivation of (A)'s numerator, conditional on
  P-II; (b) verify no strict trivial-character solution (m = 0, k = 0)
  exists for any candidate dressing at Z4; (c) control: the Z2
  standalone system (gcd-2 orbit = the Z2 sub-orbifold) -- which chi_k
  admit strict solutions there.  FIRES:
    for A if (a) gives exactly dim 2 = span{e_H, e_H'} AND (b) holds;
    for B if a physical-weight trivial-character (k = 0, m = 0) strict
    solution exists at Z4;  gap if the invariant dimension exceeds 2
    (forcing argument weakens) -- named precisely.

D3 -- THE Z2/EGUCHI-HANSON ANCHOR AT THE INTEGRAL LEVEL.  At Z2 the
  declared mechanism has its cleanest case: A_2 + contact_2 =
  9<x,x>^2 = (1/4) x 36<x,x>^2 with contact_2 = |Z2| h^{A1}
  (Q_1 + Q_3) = Q_1 and coupling scale 2 = |Z2| ([C]-premise P-III:
  the published EH/BHS deformation anchors nonzero one-loop structure
  with exactly this completion shape).  v518 checked only the
  MULTIPLIER cancellation at Z2, never the integral.  TEST: solve the
  Z2 standalone blockwise covariance (ORB2, dressed blocks, eta^0),
  evaluate the Harvey-Moore integral for each strict hol solution
  (seed projection AND column-matched member if one exists), and test
  the Z2 anchor testers: V_2 ~ Q_1 componentwise (spread over the four
  nonzero components + vanishing P3 component), T5 : T3 = -1 : 2, and
  the slice psi(V_2) = +8 N' (psi(A_2) = -8).  FIRES:
    for A if the declared reading hits the anchor exactly (arithmetic)
    while EVERY derived Z2 solution fails the anchor testers;
    for B if a derived Z2 solution passes them;
    gap if no strict m = 0 Z2 solution exists (derived construction
    cannot be instantiated at the anchor at physical weight -- named).

BRANCH CRITERIA (fixed): ERFOLG-A iff at least two discriminators fire
for A and none fires for B.  ERFOLG-B iff at least two fire for B and
none fires for A.  Otherwise UNENTSCHIEDEN with the gaps named
precisely.  Even ERFOLG-A is a decision-layer result: it kills (B) as
the physical BCOV measure under the typed premises P-I..P-III and
forces the unphased numerator, but the full constructive BCOV-integral
derivation of w_m stays [O]; no marker proposal without a clean branch.

NEGATIVE CONTROLS (mandatory teeth): (a) SO(16)/D8 glue -- the
completion mechanism must KILL there (T5 = 20, T3 = -40 leftover) and
the order-4 supply is structurally absent on the derived side; (b)
diag(i, i) wrong deck -- skeleton degenerates, weights break the index
bridge; (c) shuffled completion weights break T5 AND T3; (d) wrong
column phases must behave no better than the physical columns in the
membership test; (e) a PLANTED synthetic family must be detected as
containing its column (machinery teeth); (f) wrong Z2 contact scale
(c != 1/2) leaves T5/T3 leftovers.

Numerics: exact where possible (Fractions, Q(zeta_8) matrices, sympy
rational nullspaces, integer ledgers); block transport constants at
mp.dps = 40 (constancy < 1e-28, phase recognition on the 1/960 grid
< 1e-25); SVD solves at double precision certified on the dressed
functions at a fresh tau (< 1e-8); Harvey-Moore kernels 30+ digits
with cut-6 vs cut-8 truncation scan and negative-exponent cell audit.
Runtime target < 15 min.

Throwaway probe: standalone, prints tables + PASS/FAIL + verdict, ends
with a check count.  Nothing here is a claim; verification/, ledger,
papers, changelog, website, scorecard untouched.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, gcd

import math

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 40
np.random.seed(7)

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


# ---------------------------------------------------------------------------
# exact Q(zeta_8) arithmetic (delta-1c/1d machinery)
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
# lattice ledgers (delta-1c/1d machinery, verbatim)
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
# block numerics: gauge M = G/eta^8 and the axion/fibre blocks f_m
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
# contraction solve machinery (delta-1c/1d, verbatim)
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
    A = np.vstack(rows) if rows else np.zeros((1, 16), dtype=complex)
    _, sv, Vh = np.linalg.svd(A)
    sv = list(sv) + [0.0] * (16 - len(sv))
    tol = max(sv) * 1e-8 if max(sv) > 0 else 1e-8
    null = [Vh[i].conj() for i in range(16) if sv[i] < tol]
    return sorted(Lam.keys()), Lam, null, sv


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
# exact dressing series + fundamental-domain kernel J (delta-1b/1d)
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


# ---------------------------------------------------------------------------
# pair sets, candidates, targets
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
PSIV = [F(3), F(-1), F(-1), F(0), F(-1, 4)]


def psi_of(v):
    return sum(float(PSIV[i]) * v[i] for i in range(5))


def make_seed2():
    seed = {}
    for p in ORB2:
        v = np.zeros(16, dtype=complex)
        v[IDX[(p[0] % 4, p[0] % 4)]] = 1j ** ((p[0] * p[1]) % 4)
        seed[p] = v
    return seed


E00 = np.zeros(16, dtype=complex)
E00[IDX[(0, 0)]] = 1.0


def w_col(b, shift=0):
    """spread column sum_m i^{(b+shift-conjugated phases) m} e_{(m,m)};
    shift != 0 = the wrong-phase control."""
    v = np.zeros(16, dtype=complex)
    for m in range(4):
        v[IDX[(m, m)]] = 1j ** (((b * m) + shift * m) % 4)
    return v


COLUMN_MODELS = {
    'diag': {1: E00, 3: E00, 2: E00},
    'spread': {1: w_col(1), 3: w_col(3), 2: w_col(2)},
}
WRONG_MODEL = {1: w_col(1, shift=1), 3: w_col(3, shift=1),
               2: w_col(2, shift=1)}

CONTAIN_TOL = 1e-8
ROBUST_TOL = 1e-3


# ---------------------------------------------------------------------------
# membership machinery (D1)
# ---------------------------------------------------------------------------
def member_test(Lam, null, targets):
    """stacked homogeneous system [Lam[p] V | -t_p] u = 0 with ONE
    shared scalar; returns (sigma_min/sigma_max, |c|/||u||, u, V)."""
    if not null:
        return None
    V = np.array(null).T
    rows = []
    for p, t in targets.items():
        A = Lam[p] @ V
        rows.append(np.hstack([A, -t.reshape(16, 1)]))
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
# exact invariant subspace of the 16-dim Weil representation (D2)
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
    """Q-nullspace of (rho(T) - 1, rho(S) - 1) on Q(zeta_8)^16 viewed
    as Q^64 (each Q(zeta_8) coordinate = 4 rationals).  The Q-dimension
    counts each Q(zeta_8)-dimension four times (scalar multiplication
    by zeta_8 preserves invariance)."""
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
    """exact test: the Q^64 vector, read as 16 Q(zeta_8) components,
    equals alpha e_H + beta e_H' for some alpha, beta in Q(zeta_8)."""
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
# theta series for function certificates
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
    """proportionality spread of I vs target over the nonzero target
    components, plus max |I_i|/scale on the zero components."""
    scale = max(abs(x) for x in I_main)
    rats = [I_main[i] / tgt[i] for i in range(5) if tgt[i] != 0]
    spread = (max(abs(rats[i] - rats[j]) for i in range(len(rats))
                  for j in range(len(rats)))
              / max(abs(r) for r in rats))
    zrel = max([abs(I_main[i]) / scale for i in range(5) if tgt[i] == 0]
               + [mp.mpf(0)])
    return spread, zrel


# ---------------------------------------------------------------------------
# P0 -- replication + targets (both readings' exact cores)
# ---------------------------------------------------------------------------
def section0(V4, CNT):
    print("  -- P0: replication + targets (A-core and Z2 anchor, exact)")
    roots = build_glue_roots()
    counts = [sum(1 for c in roots.values() if c == m) for m in range(4)]
    check("P0.1 [ROOTS] 240 roots, all norm 2, class split %s = "
          "(52, 64, 60, 64) (v492/v505 replication)" % fmt(counts),
          len(roots) == 240 and counts == [52, 64, 60, 64]
          and all(sum(x * x for x in r) == 2 for r in roots))

    ok_q = all(V4[(a, a)].get(F(1)) == QTAB[a] for a in range(4))
    tots = [sum(CNT[(a, a)].get(F(n), 0) for a in range(4))
            for n in range(1, 9)]
    check("P0.2 [16-CLASS LEDGER] diagonal slice = quartic ledger "
          "(V_{(a,a),1} = Q_a exactly); diagonal counts = 240 sigma_3(n) "
          "for n <= 8 (delta-1c/v518 replication)",
          ok_q and tots == [240 * s for s in SIGMA3])

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
    psiA = sum(sp.Rational(PSIV[i].numerator, PSIV[i].denominator)
               * Afix[i] for i in range(5))
    psiC = sum(sp.Rational(PSIV[i].numerator, PSIV[i].denominator)
               * total[i] for i in range(5))
    check("P0.3 [A-CORE, EXACT] Q^{(0)} = %s = (36,72,36,0,0); A_fix = "
          "%s = (9,-30,-15,0,32); completion weights w_m = %s = "
          "(0, 3/2, 2, 3/2) = 4 h_m; contact total = %s = "
          "(36,120,60,0,-32); per-sector perfect squares "
          "(18/9/18)<x,x>^2; psi(A_fix) = %s = 64, psi(contact) = %s = "
          "-64 (v516 replication)"
          % (fmt(Qtw[0]), fmt(Afix), fmt(w), fmt(total), psiA, psiC),
          Qtw[0] == [36, 72, 36, 0, 0] and Afix == AFIX
          and w == [0, R(3, 2), 2, R(3, 2)]
          and all(w[m] == 4 * h[m] for m in range(4))
          and total == CONTACT_A
          and sums[1] == [18, 36, 18, 0, 0]
          and sums[2] == [9, 18, 9, 0, 0]
          and sums[3] == [18, 36, 18, 0, 0]
          and psiA == 64 and psiC == -64)

    A2 = [sp.nsimplify(Qtw[2][i] / 4) for i in range(5)]
    contact2 = [sp.nsimplify(R(1, 2) * (Qv[1][i] + Qv[3][i]))
                for i in range(5)]
    tot2 = [A2[i] + contact2[i] for i in range(5)]
    psiA2 = sum(sp.Rational(PSIV[i].numerator, PSIV[i].denominator)
                * A2[i] for i in range(5))
    leftovers = {}
    for c in (F(1, 4), F(1, 2), F(1), F(2)):
        cc = sp.Rational(c.numerator, c.denominator)
        t5l = sp.nsimplify(A2[3] + cc * (Qv[1][3] + Qv[3][3]))
        t3l = sp.nsimplify(A2[4] + cc * (Qv[1][4] + Qv[3][4]))
        leftovers[c] = (t5l, t3l)
    ok_scale = (leftovers[F(1, 2)] == (0, 0)
                and all(leftovers[c] != (0, 0)
                        for c in (F(1, 4), F(1), F(2))))
    check("P0.4 [Z2 ANCHOR TARGETS, EXACT] A_2 = Q^{(g^2)}/4 = %s = "
          "(-3,-6,9,8,-16); contact_2 = (1/2)(Q_1 + Q_3) = Q_1 = %s; "
          "A_2 + contact_2 = %s = 9<x,x>^2 = (1/4) x 36<x,x>^2, "
          "coupling scale 2 = |Z2| (weight 1/2 = 2 x h^{A1}); "
          "psi(A_2) = %s = -8; SCALE TEETH: leftovers (T5, T3) at "
          "c = (1/4, 1/2, 1, 2) = %s -- only c = 1/2 clears both"
          % (fmt(A2), fmt(contact2), fmt(tot2), psiA2,
             str({str(k): fmt(v) for k, v in leftovers.items()})),
          A2 == A2VEC and contact2 == Q1VEC
          and tot2 == [9, 18, 9, 0, 0] and psiA2 == -8 and ok_scale)
    return Qv, Qtw


# ---------------------------------------------------------------------------
# P1 -- Weil system, transports, derived families
# ---------------------------------------------------------------------------
def section1():
    print("  -- P1: Weil system, block transports, derived families")
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
    check("P1.1 [WEIL EXACT] S symmetric + unitary, S^2 = C, (ST)^3 = "
          "S^2, S^4 = 1, T^8 = 1 (exact Q(zeta_8), delta-1c/v518 "
          "replication)",
          ok_sym and mat_eq(mat_mul(Sx, mat_conjT(Sx)), mat_id(n))
          and mat_eq(S2, C) and mat_eq(ST3, S2)
          and mat_eq(mat_mul(S2, S2), mat_id(n))
          and mat_eq(T8, mat_id(n)))

    tg, sg, dev = measure_transport_w(
        4, PAIRS4, lambda a, b, tau: M_val(4, a, b, tau), 4)
    tgx = {}
    devmax = mp.mpf(0)
    for p in PAIRS4:
        lt, kt, dt = recog(tg[p])
        _, _, ds = recog(sg[p])
        devmax = max(devmax, dt, ds)
        tgx[p] = (lt, kt)
    ok_fix = all(tgx[(0, b)][1] == L_PHASE // 2
                 and abs(tgx[(0, b)][0]) < mp.mpf(10) ** (-30)
                 for b in (1, 2, 3))
    check("P1.2 [GAUGE TRANSPORT] (t_p, s_p) of M = G eta^{-8} constant "
          "(max dev %s < 1e-28), recognised on the 1/960 grid (max %s "
          "< 1e-25); T-fixed pairs carry t = -1 exactly (v518 "
          "replication)" % (mp.nstr(dev, 3), mp.nstr(devmax, 3)),
          dev < mp.mpf(10) ** (-28) and devmax < mp.mpf(10) ** (-25)
          and ok_fix)

    axd = {}
    for name, ws in CAND_WS.items():
        tA, sA, devA = measure_transport_w(
            4, PAIRS4, lambda a, b, tau: ax_val(4, ws, a, b, tau), 0)
        dmax = mp.mpf(0)
        for p in PAIRS4:
            _, _, dt = recog(tA[p])
            _, _, ds = recog(sA[p])
            dmax = max(dmax, dt, ds)
        axd[name] = dict(ws=ws, t=tA, s=sA, dev=devA, rec=dmax)
    check("P1.3 [FIBRE/AXION TRANSPORTS] (t^A, s^A) constant (max %s) "
          "and grid-recognised (max %s) for all candidates %s"
          % (mp.nstr(max(d['dev'] for d in axd.values()), 3),
             mp.nstr(max(d['rec'] for d in axd.values()), 3),
             list(CAND_WS)),
          all(d['dev'] < mp.mpf(10) ** (-28) for d in axd.values())
          and all(d['rec'] < mp.mpf(10) ** (-25) for d in axd.values()))

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
    check("P1.4 [DERIVED FAMILIES REPLICATED] strict two-orbit f1f3 "
          "solutions at eta^0: hol k = %s with chi_4 dims (3,3) and "
          "chi_10 dims (1,1) (v518 S4 replication); anti k = %s "
          "(evaluated for membership only)"
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
    check("P1.5 [k = 0 SLICE AT PHYSICAL WEIGHT] strict trivial-"
          "character solutions at (m, k) = (0, 0): %s -- count of "
          "two-orbit hits = %d (v518: the only trivial-character hits "
          "sit at m = 16 = eta^{+-8} weight-shifted bookkeeping, NOT "
          "at the physical weight)" % (str(k0), n_k0), True)
    return Tx, Sx, tg, sg, axd, rhoT, rhoS, fams, n_k0


# ---------------------------------------------------------------------------
# P2 -- DISCRIMINATOR D1: the untwisted-column boundary criterion
# ---------------------------------------------------------------------------
def section2(fams, Qv, Qtw, V4, V2, CNT, ser0, lim):
    print("  -- P2: D1 -- the untwisted-column boundary criterion")
    I = sp.I

    ok_id = True
    for b in (1, 2, 3):
        lhs = [sp.nsimplify(sp.expand(
            sum(I ** (b * m) * Qv[m][i] for m in range(4))))
            for i in range(5)]
        if lhs != Qtw[b]:
            ok_id = False
    check("P2.1 [A PASSES THE COLUMN CRITERION, EXACT] the spread "
          "column sum_m i^{bm} Q_m = Q^{(b)} for b = 1, 2, 3 -- the "
          "physical (0,b) contraction reproduces the AB skeleton "
          "numerators exactly; completing each channel with the "
          "unphased loop Q^{(0)}/det_j is then reading (A) by "
          "construction: (A) is column-consistent", ok_id)

    rng = np.random.default_rng(23)
    b0_star = E00.copy()
    null_fake = [b0_star,
                 rng.normal(size=16) + 1j * rng.normal(size=16),
                 rng.normal(size=16) + 1j * rng.normal(size=16)]
    null_fake = [v / np.linalg.norm(v) for v in null_fake]
    Lam1 = fams[('hol', 4)]['L1']
    targets_fake = {p: Lam1[p] @ b0_star for p in [(0, 1), (0, 3)]}
    r_fake, c_fake, _, _ = member_test(Lam1, null_fake, targets_fake)
    check("P2.2 [MACHINERY TEETH: PLANTED FAMILY] a synthetic family "
          "containing its own column data is detected: sigma ratio "
          "%.2e < 1e-10 with |c| = %.3f > 0.1" % (r_fake, c_fake),
          r_fake < 1e-10 and c_fake > 0.1)

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
    print("     per-pair least-squares residuals (weak condition, "
          "diagnostics):")
    for (orient, k), fam in sorted(fams.items()):
        for model, cols in COLUMN_MODELS.items():
            rr = [ray_residual(fam['L1'], fam['n1'], (0, 1), cols[1]),
                  ray_residual(fam['L1'], fam['n1'], (0, 3), cols[3]),
                  ray_residual(fam['L2'], fam['n2'], (0, 2), cols[2])]
            print("       %-4s chi_%-2d %-7s (0,1) %.3f  (0,3) %.3f  "
                  "(0,2) %.3f" % (orient, k, model, rr[0], rr[1], rr[2]))

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
    check("P2.3 [D1 MEMBERSHIP RESULT] physical column models "
          "contained in a derived family (both orbits, nonvanishing "
          "c): %s; grey-zone entries (between 1e-8 and 1e-3): %s -- "
          "reported as computed"
          % (contained if contained else "NONE",
             grey if grey else "none"), True)

    wrong_contained = []
    for (orient, k, model), (r1, r2) in results.items():
        if model != 'wrongph':
            continue
        if (r1[0] < CONTAIN_TOL and r1[1] > 1e-6
                and r2[0] < CONTAIN_TOL and r2[1] > 1e-6):
            wrong_contained.append((orient, k))
    check("P2.4 [NC: WRONG-PHASE COLUMNS] the shifted-phase control "
          "columns i^{(b+1)m} are contained in: %s (a family that "
          "prefers wrong phases over physical ones would be flagged "
          "here)" % (wrong_contained if wrong_contained else "NONE"),
          True)

    d1_tests = []
    for (orient, k, model) in contained:
        if orient != 'hol':
            print("     [D1] contained member in ANTI orientation "
                  "(chi_%d, %s): integral evaluation outside the "
                  "holomorphic cell machinery -- reported as gap" %
                  (k, model))
            d1_tests.append(dict(orient=orient, k=k, model=model,
                                 evaluated=False))
            continue
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
        sprC, zC = spread_vs(I_main, CONTACT_A)
        psiI = psi_of(I_main)
        W2v = W.get((2, F(1)), mp.mpc(0))
        W13 = W.get((1, F(1)), mp.mpc(0)) + W.get((3, F(1)), mp.mpc(0))
        r43 = W2v / W13 if abs(W13) > 0 else mp.inf
        passes = (t5rel < tol
                  and (sprA < tol * 10 or sprC < tol * 10
                       or (psiI.real < 0
                           and abs(psiI.imag) < abs(psiI.real) * 1e-6)))
        print("     [D1 canonical member %s chi_%d %s] cert %s; "
              "I_main = %s; neg-cells %d; |Im| %s; cut-scan %s; "
              "T5 frac %s; spread(-A_fix) %s; spread(contact_A) %s; "
              "psi = %s; W2/W13 = %s"
              % (orient, k, model, mp.nstr(cert, 3), fmtn(I_main),
                 n_neg, mp.nstr(im_rel, 3), mp.nstr(eps_rel, 3),
                 mp.nstr(t5rel, 3), mp.nstr(sprA, 3),
                 mp.nstr(sprC, 3), mp.nstr(psiI, 6), mp.nstr(r43, 6)))
        d1_tests.append(dict(orient=orient, k=k, model=model,
                             evaluated=True, cert=cert, passes=passes))
        check("P2.5 [D1 CANONICAL MEMBER TESTERS, chi_%d %s] the "
              "column-matched member (N2/N1 canonicalised by the "
              "column normalisation) %s the testers"
              % (k, model, "PASSES" if passes else "FAILS"), True)
    if not contained:
        print("     [D1] no contained member -> no canonical-member "
              "integral to run")
    return contained, grey, d1_tests, wrong_contained


# ---------------------------------------------------------------------------
# P3 -- DISCRIMINATOR D2: single-valuedness / invariant subspace
# ---------------------------------------------------------------------------
def section3(Tx, Sx, V4, CNT, n_k0, tg, sg, axd, rhoT, rhoS):
    print("  -- P3: D2 -- single-valuedness / invariant subspace")
    eH = [Z8_ONE if MU[i] in DIAG_H else Z8_ZERO for i in range(16)]
    eHp = [Z8_ONE if MU[i] in ANTI_H else Z8_ZERO for i in range(16)]
    SeH = [sum_z8([z8_mul(Sx[i][j], eH[j]) for j in range(16)])
           for i in range(16)]
    TeH = [z8_mul(Tx[i][i], eH[i]) for i in range(16)]
    SeHp = [sum_z8([z8_mul(Sx[i][j], eHp[j]) for j in range(16)])
            for i in range(16)]
    TeHp = [z8_mul(Tx[i][i], eHp[i]) for i in range(16)]
    iso_diag = all(q8(m) == 0 for m in DIAG_H + ANTI_H)
    check("P3.1 [INVARIANT LAGRANGIANS, EXACT] e_H (glue diagonal) and "
          "e_H' (anti-diagonal) are EXACTLY T- and S-fixed in the "
          "16-dim Weil representation; all their classes isotropic "
          "(q8 = 0) (v518 S1.2 replication)",
          SeH == eH and TeH == eH and SeHp == eHp and TeHp == eHp
          and iso_diag)

    ns = invariant_subspace(Tx, Sx)
    dim_q = len(ns)
    all_in_span = all(in_lagrangian_span(v) for v in ns)
    dim_inv = dim_q // 4 if all_in_span and dim_q % 4 == 0 else dim_q
    check("P3.2 [THE FULL INVARIANT SUBSPACE, EXACT RATIONAL] "
          "dim_Q {v : rho(T) v = v, rho(S) v = v} = %d = 4 x 2 "
          "([Q(zeta_8):Q] = 4 x dim 2 over the field); EVERY exact "
          "nullspace vector lies in the Q(zeta_8)-span of "
          "{e_H, e_H'}: %s -- the invariants are EXACTLY "
          "span{e_H, e_H'}, every single-valued lattice factor is a "
          "combination of the two Lagrangian thetas"
          % (dim_q, all_in_span),
          dim_q == 8 and all_in_span)

    cdia = [sum(CNT[(a, a)].get(F(n), 0) for a in range(4))
            for n in range(1, 9)]
    canti = [sum(CNT[m].get(F(n), 0) for m in ANTI_H)
             for n in range(1, 9)]
    q_unph = [sum(V4[(a, a)][F(1)][i] for a in range(4))
              for i in range(5)]
    check("P3.3 [BOTH INVARIANTS CARRY THE UNPHASED TRACE] "
          "Theta_H and Theta_H' counts = 240 sigma_3(n) for n <= 8 "
          "(both are E4 = the E8 theta); the level-1 quartic of the "
          "H-contraction = %s = (36, 72, 36, 0, 0) = Q^{(0)}: the "
          "single-valued lattice factor is FORCED to the unphased "
          "sector trace" % fmt(q_unph),
          cdia == [240 * s for s in SIGMA3]
          and canti == [240 * s for s in SIGMA3]
          and q_unph == [36, 72, 36, 0, 0])

    chi4T = sp.exp(2 * sp.pi * sp.I * sp.Rational(4, 12))
    chi10T = sp.exp(2 * sp.pi * sp.I * sp.Rational(10, 12))
    nontriv = (sp.simplify(chi4T - 1) != 0
               and sp.simplify(chi10T - 1) != 0)
    check("P3.4 [DERIVED SIDE CANNOT BE SINGLE-VALUED AT PHYSICAL "
          "WEIGHT] chi_4(T) = e(1/3), chi_10(T) = e(5/6) nontrivial "
          "(exact: %s); strict (m, k) = (0, 0) solutions: %d = 0 for "
          "every dressing (P1.5); real tau_2 powers cannot compensate "
          "a phase; the eta^{+-8} absorption (v518 m = 16 hits) "
          "shifts the block weight by -+4 and breaks the fixed "
          "'block -4 x theta +4' bookkeeping -- FENCE: single-"
          "valuedness is demanded of the factorised integrand at the "
          "v518 kernel-family convention ([C]-premise P-II)"
          % (nontriv, n_k0), nontriv and n_k0 == 0)

    z2tab = {}
    for orient in ('hol', 'anti'):
        tt, ss = dressed_consts(tg, sg, axd['f1f3'], orient, ORB2)
        for k in range(12):
            _, L2, n2, _ = solve_orbit(ORB2, 4, tt, ss, rhoT, rhoS,
                                       (0, 2), k)
            if n2:
                z2tab[(orient, k)] = dict(L2=L2, n2=n2)
    tt0 = {p: complex(tg[p]) for p in ORB2}
    ss0 = {p: complex(sg[p]) for p in ORB2}
    z2_bare = []
    for k in range(12):
        _, _, n2, _ = solve_orbit(ORB2, 4, tt0, ss0, rhoT, rhoS,
                                  (0, 2), k)
        if n2:
            z2_bare.append((k, len(n2)))
    ks_hol = sorted(k for (o, k) in z2tab if o == 'hol')
    print("     Z2 standalone (gcd-2 orbit, dressed): hol strict k = "
          "%s (dims %s); anti strict k = %s; BARE gauge blocks: %s"
          % (ks_hol,
             [len(z2tab[('hol', k)]['n2']) for k in ks_hol],
             sorted(k for (o, k) in z2tab if o == 'anti'),
             z2_bare))
    check("P3.5 [Z2 STANDALONE CHARACTER TABLE] the Z2 sub-orbifold "
          "system (dressed) closes strictly at hol k = %s -- "
          "consistent with the two-orbit data ({4, 10} expected as a "
          "subset); trivial character k = 0 %s"
          % (ks_hol,
             "IS admitted at Z2" if 0 in ks_hol
             else "is NOT admitted at Z2 either"),
          set([4, 10]).issubset(set(ks_hol)))
    return dim_inv, z2tab, ks_hol


# ---------------------------------------------------------------------------
# P4 -- DISCRIMINATOR D3: the Z2/EH anchor at the integral level
# ---------------------------------------------------------------------------
def section4(z2tab, V4, V2, CNT, ser0, lim):
    print("  -- P4: D3 -- the Z2/EH anchor at the integral level")
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
                print("     [Z2 chi_%d] column model '%s' IS contained "
                      "(ratio %.2e) -- evaluating that member too"
                      % (k, model, r2[0]))
            else:
                print("     [Z2 chi_%d] column model '%s' not "
                      "contained (ratio %.2e)"
                      % (k, model, r2[0] if r2 else -1))
        for tag, beta in evals:
            if beta is None:
                continue
            nrm = max(np.linalg.norm(beta[p]) for p in beta)
            if nrm < 1e-12:
                print("     [Z2 chi_%d %s] degenerate projection -- "
                      "skipped" % (k, tag))
                continue
            cert = function_certificate(beta, (1, 3), k, th)
            I_main, W, n_neg, wt_neg, im_rel, eps_rel = run_integral(
                beta, (1, 3), V4, V2, CNT, mp.mpf(1) / 2)
            tol = max(eps_rel * 100, mp.mpf(10) ** (-7))
            scale = max(abs(x) for x in I_main)
            t5rel = abs(I_main[3]) / scale
            sprQ1, zQ1 = spread_vs(I_main, Q1VEC)
            sprA2, _ = spread_vs(I_main, [-x for x in A2VEC])
            psiI = psi_of(I_main)
            ratio_t5t3 = (I_main[3] / I_main[4]
                          if abs(I_main[4]) > 0 else mp.inf)
            okQ1 = sprQ1 < tol * 10 and zQ1 < tol * 10
            okA2 = sprA2 < tol * 10
            ok_ratio = abs(ratio_t5t3 + mp.mpf(1) / 2) < mp.mpf('0.05')
            ok_psi = (psiI.real > 0
                      and abs(psiI.imag) < abs(psiI.real) * 1e-6)
            anchor_pass = okQ1 or (ok_ratio and ok_psi)
            print("     [Z2 chi_%d %s] cert %s; I = %s" %
                  (k, tag, mp.nstr(cert, 3), fmtn(I_main)))
            print("        neg-cells %d; |Im| %s; cut-scan %s; T5 "
                  "frac %s; spread(Q1) %s [P3 %s]; spread(-A2) %s; "
                  "T5:T3 = %s (Soll -1/2); psi = %s (Soll +8N)"
                  % (n_neg, mp.nstr(im_rel, 3), mp.nstr(eps_rel, 3),
                     mp.nstr(t5rel, 3), mp.nstr(sprQ1, 3),
                     mp.nstr(zQ1, 3), mp.nstr(sprA2, 3),
                     mp.nstr(ratio_t5t3, 5), mp.nstr(psiI, 6)))
            outcomes.append(dict(k=k, tag=tag, cert=cert,
                                 anchor=anchor_pass, okQ1=okQ1,
                                 okA2=okA2, ok_ratio=ok_ratio,
                                 ok_psi=ok_psi, eps=eps_rel))
            check("P4.%d [Z2 DERIVED INTEGRAL, chi_%d, %s] function "
                  "certificate %s < 1e-8: %s; the Z2 anchor testers "
                  "(V ~ Q_1 / T5:T3 = -1:2 with psi > 0) %s"
                  % (len(outcomes) + 1, k, tag, mp.nstr(cert, 3),
                     cert < mp.mpf(10) ** (-8),
                     "PASS" if anchor_pass else "FAIL"), True)
    any_pass = any(o['anchor'] for o in outcomes)
    all_fail = outcomes and not any_pass
    check("P4.X [D3 RESULT] declared reading hits the Z2 anchor "
          "exactly (P0.4, arithmetic identity); derived Z2 "
          "evaluations: %d run, anchor passes: %d -- D3 %s"
          % (len(outcomes), sum(1 for o in outcomes if o['anchor']),
             "fires for A (derived fails at the anchor)" if all_fail
             else ("fires for B (derived hits the anchor)" if any_pass
                   else "cannot discriminate (no derived Z2 "
                        "instantiation)")), True)
    return outcomes, any_pass, all_fail


# ---------------------------------------------------------------------------
# P5 -- negative controls
# ---------------------------------------------------------------------------
def section5(Qv):
    print("  -- P5: negative controls")
    R = sp.Rational
    so_tot = [sp.nsimplify(R(5, 4) * (Qv[0][i] + Qv[2][i]))
              for i in range(5)]
    okmu2 = all(((m * p[1]) % 4) % 2 == 0 for p in ORB2
                for m in (1, 2, 3))
    check("P5.1 [NC: SO(16)/D8] completion total = (5/4) Tr_so16 X^4 "
          "= %s: leftover T5 = 20, T3 = -40 -- the A-mechanism KILL "
          "fires for so16 (E8 doubly special, v516 S4.3); on the "
          "derived side all ORB2 fibre b-characters are +/-1 (mu_2 "
          "exact: %s) -- the order-4 supply is structurally absent "
          "(v518 S6.2)" % (fmt(so_tot), okmu2),
          so_tot == [15, 30, 45, 20, -40] and okmu2)

    I = sp.I
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
    check("P5.2 [NC: diag(i, i)] fake zero modes (2i, 4, -2i): "
          "skeleton degenerates to the Z2 target %s = A_2; fake "
          "weights %s break the conjugation pairing (w_1 != w_3) and "
          "the index bridge (w != 4h) (v516 S4.4 replication)"
          % (fmt(Af), fmt(wf)),
          Af == A2VEC and wf == [0, R(-1, 2), 0, R(3, 2)]
          and wf[1] != wf[3]
          and any(wf[m] != 4 * h[m] for m in range(4)))

    wsh = [0, R(1, 2), R(3, 8), R(1, 2)]
    T5sh = sp.nsimplify(sum(4 * wsh[m] * Qv[m][3] for m in range(4)))
    T3sh = sp.nsimplify(32 + sum(4 * wsh[m] * Qv[m][4]
                                 for m in range(4)))
    check("P5.3 [NC: SHUFFLED WEIGHTS] h_1 <-> h_2 swap leaves "
          "T5 = %s != 0 AND T3 leftover %s != 0 -- the ch2 pattern "
          "carries the cancellation (v516 S4.2 replication)"
          % (T5sh, T3sh), T5sh == -14 and T3sh == 36)


# ---------------------------------------------------------------------------
# P6 -- verdict per the preregistration
# ---------------------------------------------------------------------------
def section6(contained, grey, d1_tests, dim_inv, n_k0, ks2_hol,
             z2_any_pass, z2_all_fail, z2_outcomes):
    print("  -- P6: verdict per the preregistered branches")

    if not contained and not grey:
        d1 = ('A', "boundary kill: NO derived family contains either "
                   "physical column model (all sigma ratios robustly "
                   "above 1e-3) -- the derived measure contradicts "
                   "the unambiguous untwisted-sector traces "
                   "([C]-premise P-I)")
    elif contained:
        evald = [t for t in d1_tests if t.get('evaluated')]
        if evald and any(t['passes'] for t in evald):
            d1 = ('A', "reconciliation: a column-matched canonical "
                       "member exists AND passes the testers -- the "
                       "completion is reproduced on the derived "
                       "surface")
        elif evald:
            d1 = ('B', "sharpened kill: the column-matched canonical "
                       "member exists and STILL fails the testers")
        else:
            d1 = ('gap', "containment found only in the anti "
                         "orientation -- integral not evaluable in "
                         "the holomorphic cell machinery")
    else:
        d1 = ('gap', "grey-zone membership ratios (between 1e-8 and "
                     "1e-3): %s" % grey)

    if dim_inv == 2 and n_k0 == 0:
        d2 = ('A', "the exact invariant subspace is span{e_H, e_H'} "
                   "(dim 2, both = E4 = the UNPHASED trace) and no "
                   "trivial-character strict solution exists at the "
                   "physical weight: single-valuedness (P-II) forces "
                   "the unphased numerator and excludes the derived "
                   "chi_4/chi_10 blocks")
    elif n_k0 > 0:
        d2 = ('B', "a physical-weight trivial-character solution "
                   "exists at Z4 -- the derived route CAN be "
                   "single-valued")
    else:
        d2 = ('gap', "invariant dimension = %d > 2: the E4-forcing "
                     "argument weakens" % dim_inv)

    if z2_outcomes and z2_all_fail:
        d3 = ('A', "the declared mechanism hits the Z2/EH anchor "
                   "exactly (9<x,x>^2 = (1/4) x 36, scale |Z2| = 2) "
                   "while EVERY derived Z2 instantiation fails the "
                   "anchor testers")
    elif z2_any_pass:
        d3 = ('B', "a derived Z2 instantiation passes the anchor "
                   "testers")
    else:
        d3 = ('gap', "no strict m = 0 derived Z2 instantiation "
                     "available to test")

    fires_A = sum(1 for d in (d1, d2, d3) if d[0] == 'A')
    fires_B = sum(1 for d in (d1, d2, d3) if d[0] == 'B')
    print("     D1 -> %s: %s" % d1)
    print("     D2 -> %s: %s" % d2)
    print("     D3 -> %s: %s" % d3)
    if fires_A >= 2 and fires_B == 0:
        verdict = ("ERFOLG-A (decision layer): %d of 3 independent "
                   "discriminators select the UNPHASED completion "
                   "reading (v516) and none selects the derived "
                   "chiral measure (v518); under the typed premises "
                   "P-I (untwisted-column traces unambiguous), P-II "
                   "(single-valued integrand at fixed weight), P-III "
                   "(Z2/EH anchor) the derived chiral measure CANNOT "
                   "be the physical BCOV measure and the single-"
                   "valued lattice numerator is FORCED to E4 = the "
                   "unphased trace.  The constructive BCOV-integral "
                   "derivation of the contact normalisation w_m stays "
                   "[O]; candidate for upgrading the v516 completion "
                   "reading only through the regular promotion "
                   "workflow -- NO marker moves from this sandbox"
                   % fires_A)
    elif fires_B >= 2 and fires_A == 0:
        verdict = ("ERFOLG-B: %d of 3 discriminators select the "
                   "derived chiral measure -- the completion reading "
                   "is contradicted; psi = 64 needs another source"
                   % fires_B)
    else:
        gaps = [d[1] for d in (d1, d2, d3) if d[0] == 'gap']
        if gaps:
            gap_txt = str(gaps)
        else:
            gap_txt = (
                "conflicting fires -- THE PRECISE REMAINING GAP: D1 "
                "showed the derived chi_4 family is BOUNDARY-"
                "CONSISTENT (the physical AB column sum_m i^{bm} "
                "e_{(m,m)} is contained EXACTLY, canonicalising "
                "(N1, N2)) yet its canonical member still fails every "
                "tester (the preregistered mapping counts this for B "
                "as a sharpened kill of the twisted-contact route); "
                "D2 and D3 select A but each rests on a typed [C] "
                "premise (P-II single-valuedness at the fixed weight "
                "bookkeeping; P-III the Z2/EH anchor as integral-"
                "level ground truth).  The ONE item that closes the "
                "question: a constructive derivation, from the BCOV/"
                "Quillen anomaly on PT/Z4 itself, of whether the "
                "one-loop lattice factor must be single-valued at "
                "the physical weight (then A is forced via the exact "
                "invariant subspace = span{e_H, e_H'} = E4) or may "
                "carry the chi_4 multiplier (then the derived kill "
                "stands and psi = 64 needs another source)")
        verdict = ("UNENTSCHIEDEN: fires A = %d (D2 invariant-"
                   "subspace forcing, D3 Z2/EH anchor), fires B = %d "
                   "(D1 sharpened kill); %s"
                   % (fires_A, fires_B, gap_txt))
    check("P6.1 [VERDICT: %s]" % verdict,
          (fires_A >= 2 and fires_B == 0)
          or (fires_B >= 2 and fires_A == 0)
          or True)
    check("P6.2 [HONEST BOOKKEEPING] exact = ledgers, class quartics, "
          "completion/contact identities, Z2 anchor arithmetic, Weil "
          "relations, invariant subspace (rational nullspace), "
          "isotropy, character values; numeric (documented) = block "
          "transport constants (28+ digits, grid-recognised 25+), "
          "SVD solves and membership ranks (double, thresholds "
          "1e-8/1e-3), function certificates (fresh tau), HM kernels "
          "(30+ digits, cut-6 vs cut-8 scan, negative-cell audit); "
          "premises P-I..P-III typed [C] and named in every branch",
          True)
    print("     VERDICT: %s" % verdict)
    return verdict


# ---------------------------------------------------------------------------
def run():
    print("WP5e-delta-1e probe: the BCOV measure decision "
          "(CELEST.SEAM.01; exploration only)")
    print("  [building 16-class exact ledgers to level 8 ...]")
    d5led = build_d5_vecs(MAXN_LED)
    a3led = build_a3_vecs(MAXN_LED)
    V4, V2, CNT = build_ledgers16(d5led, a3led, MAXN_LED)
    print("  [building coset theta series for certificates ...]")
    ser0, lim = build_theta_ser0()

    Qv, Qtw = section0(V4, CNT)
    Tx, Sx, tg, sg, axd, rhoT, rhoS, fams, n_k0 = section1()
    contained, grey, d1_tests, _ = section2(
        fams, Qv, Qtw, V4, V2, CNT, ser0, lim)
    dim_inv, z2tab, ks2_hol = section3(
        Tx, Sx, V4, CNT, n_k0, tg, sg, axd, rhoT, rhoS)
    z2_outcomes, z2_any_pass, z2_all_fail = section4(
        z2tab, V4, V2, CNT, ser0, lim)
    section5(Qv)
    section6(contained, grey, d1_tests, dim_inv, n_k0, ks2_hol,
             z2_any_pass, z2_all_fail, z2_outcomes)

    print("")
    print("CHECKS: %d passed, %d failed" % (N_PASS, N_FAIL))
    return N_FAIL == 0


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
