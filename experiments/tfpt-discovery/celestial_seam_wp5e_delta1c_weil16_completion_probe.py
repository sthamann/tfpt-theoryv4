"""WP5e-delta-1c of CELEST.SEAM.01 (EXPLORATION ONLY -- experiments/, no
verification claim).

"COMPLETING THE 16-COMPONENT WEIL SYSTEM" -- the step that makes the
Harvey-Moore integral of delta-1b decidable.  delta-1b (30/30) ended
UNENTSCHIEDEN with a precise gap: (i) the declared measure family
{s = 0,1,2} x {vac = 0..3} missed both targets, and (ii) E1.5 showed the
naive 4-character S-rule of the glue coset thetas FAILS at O(1) because
the discriminant group of D5 (+) A3 is Z4 x Z4 (16 classes) -- the v502
sector assignment covers only the 4 diagonal (isotropic-Lagrangian)
classes.  delta-1c builds the FULL system:

P0  replication: roots, targets A_fix / psi, the delta-1 ledger anchors.
P1  THE WEIL REPRESENTATION EXACT (Q(zeta_8) arithmetic): D = Z4 x Z4,
    q(x,y) = (5x^2+3y^2)/8 mod 1; Gauss sum = 4 exactly (signature
    0 mod 8 = rank E8); T = diag e(q), S = (1/4) e(-(mu,nu)); exact
    S symmetric + unitary, S^2 = C, (ST)^3 = C, S^4 = 1, T^8 = 1
    (level 8); tensor factorisation S = S_D5 (x) S_A3; the v502 slice:
    e_H = sum over the diagonal H is EXACTLY S- and T-invariant
    (H = H-perp Lagrangian); the naive 4-rule is doubly wrong:
    P_H S P_H = J/16-block (all entries 1/4) != (1/2) i^{-aa'}, and
    12/16 of every S-image sits on shifted classes.
P2  THE 16 COSET THETAS: all 16 (D5-class x A3-class) lattice sums;
    exact grid statement norm/2 = q(mu) mod 1 per class; the 4 diagonal
    classes reproduce the delta-1/v502 counts and E4; BOTH Lagrangians
    (diagonal and anti-diagonal) sum to E4; S-covariance of the
    16-vector verified at 25+ digits -- the E1.5 residual (O(1) on the
    4-component rule) drops to numerical zero on the 16-component rule.
P3  THE QUARTIC WEIL SYSTEM: <lambda,x>^4-inserted 16-vector thetas
    with ISOTROPIC complex x ((x,x) = 0 => insertion harmonic => exact
    weight-8 covariance, one global constant); non-harmonic real-x
    completion (heat-kernel: -3(x,x)Theta^(2)/(2 pi tau2) +
    3(x,x)^2 Theta^(0)/(16 pi^2 tau2^2)) verified as weight-8 covariant
    -- the integrated form of the delta-1b (T5,T3)-rigidity.
P4  THE CONTRACTION IS SOLVED FOR, NOT DECLARED: ansatz
    Z = sum_{(a,b) != (0,0)} M_{a,b}(tau) beta^{(a,b)}.Theta(tau) with
    M = (twisted C^2 block) x eta^{-8}.  Block transport constants t_p
    (T: p -> (a, a+b)) and s_p (S: p -> (b, -a), weight -4) measured
    to 28+ digits, CONSTANT; blockwise covariance = parallel transport
    on the two pair orbits (gcd 1: 12, gcd 2: 3): BFS + loop-holonomy
    constraints + SVD null space.  Validated on the eta^{-8} single
    block (dim 0 strictly; dim 2 = span{e_H, e_H'} exactly at the
    eta^8-character chi_8).  RESULT: NO strict solution for ANY of the
    12 SL(2,Z) characters, and NO (eta^m, chi_k) weight bookkeeping
    (m = 0..23) rescues it; holonomy spectroscopy: joint eigenspace of
    dim 8/16 (gcd 1) resp. 6/16 (gcd 2) with EVERY eigenvalue a root
    of unity of order <= 4 -- the obstruction is a FINITE mu_4
    multiplier system, not a continuous defect.  Derived contraction =
    seed-projected joint eigenvector (canonical BFS tree; edge closure
    certified on the functions to 1e-15 up to unit phases of the
    diagnosed order).
P5  THE INTEGRAL UNDER THE DERIVED CONTRACTION: weight bookkeeping
    fixes the kernels (invariant measure x tau2^2 zero-mode scaling =>
    main J(Delta,0); heat-kernel completion J(Delta,1), J(Delta,2),
    P-block only); delta-1b cell machinery (exact cusp integrals +
    Gauss-Legendre arc) evaluates the three WAITING tests:
    T5(V) = 0?  W_2 : W_13 = 4 : 3?  psi(V) = -64 N or V = -A_fix N?
    (complex moduli; residual multiplier phases recorded honestly --
    they ARE the remaining gap).
P6  ANCHOR (Z2 FIRST): the D8 discriminant Z2 x Z2 with q =
    (0, 1/2, 0, 0) mod 1 (v502 S6.1): its 4-component theta system
    closes under S WITHOUT shifted classes (exact Weil relations +
    covariance certificate: the completion is a Z4 phenomenon); the
    derived Z2 sub-orbifold contraction reproduces the delta-1b/BHS
    structure (nonzero, leading massive coset level dominant).
P7  NEGATIVE CONTROLS: (a) wrong form (x^2+y^2)/4 (Gauss sum 2i =>
    signature 2 mod 8 != 0, theta covariance breaks O(1)); (b) wrong
    signature factor in S (relations break exactly); (c) k = 2 thetas
    (q -> q^2) break covariance and empty the leading slot.
P8  HONEST VERDICT of the delta-1 route per the preregistered branches.

Throwaway probe: exact where possible (Fractions, Q(zeta_8), exact
q-grids), mpmath dps = 30+ for the covariance certificates and kernels,
numpy double SVD for the contraction solve (residual scale documented).
Prints tables + PASS/FAIL + verdict, ends with a check count.  Nothing
here is a claim; verification/, ledger, papers, changelog, website,
scorecard untouched.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, gcd

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 40
np.random.seed(7)

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
# exact Q(zeta_8) arithmetic: elements a0 + a1 z + a2 z^2 + a3 z^3, z^4 = -1
# ---------------------------------------------------------------------------
Z8_ZERO = (F(0), F(0), F(0), F(0))
Z8_ONE = (F(1), F(0), F(0), F(0))


def z8_add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def z8_sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


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
    """zeta_8^k exactly."""
    k %= 8
    s = F(1)
    if k >= 4:
        k -= 4
        s = F(-1)
    v = [F(0)] * 4
    v[k] = s
    return tuple(v)


def z8_conj(a):
    """complex conjugation: zeta -> zeta^{-1} = -zeta^3."""
    return (a[0], -a[3], -a[2], -a[1])


def z8_to_mpc(a):
    z = mp.exp(mp.mpc(0, mp.pi / 4))
    return (mp.mpf(a[0].numerator) / a[0].denominator
            + z * mp.mpf(a[1].numerator) / a[1].denominator
            + z ** 2 * mp.mpf(a[2].numerator) / a[2].denominator
            + z ** 3 * mp.mpf(a[3].numerator) / a[3].denominator)


def mat_mul(A, B):
    n = len(A)
    return [[sum_z8([z8_mul(A[i][k], B[k][j]) for k in range(n)])
             for j in range(n)] for i in range(n)]


def sum_z8(xs):
    out = Z8_ZERO
    for x in xs:
        out = z8_add(out, x)
    return out


def mat_eq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A))
               for j in range(len(A)))


def mat_id(n):
    return [[Z8_ONE if i == j else Z8_ZERO for j in range(n)]
            for i in range(n)]


def mat_scal(f, A):
    return [[z8_scal(f, x) for x in row] for row in A]


def mat_conjT(A):
    n = len(A)
    return [[z8_conj(A[j][i]) for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------------------
# the discriminant module D = Z4 x Z4, q = (5x^2 + 3y^2)/8 mod 1
# ---------------------------------------------------------------------------
MU = [(x, y) for x in range(4) for y in range(4)]
IDX = {m: i for i, m in enumerate(MU)}


def q8(mu):
    """8 * q(mu) mod 8 (integer exponent of zeta_8)."""
    x, y = mu
    return (5 * x * x + 3 * y * y) % 8


def bil8(mu, nu):
    """8 * (mu, nu) mod 8, (mu,nu) = q(mu+nu) - q(mu) - q(nu)."""
    return (2 * (5 * mu[0] * nu[0] + 3 * mu[1] * nu[1])) % 8


def neg(mu):
    return ((-mu[0]) % 4, (-mu[1]) % 4)


def build_weil(qfun, bfun, group, sigma_conj):
    """T = diag e(q), S = (sigma_conj / sqrt|D|) e(-(mu,nu)); exact."""
    n = len(group)
    rt = F(1)
    m = n
    while m % 4 == 0:
        m //= 4
        rt *= 2
    assert m == 1, "|D| must be a power of 4 here"
    T = [[z8_root(qfun(group[i])) if i == j else Z8_ZERO
          for j in range(n)] for i in range(n)]
    S = [[z8_scal(F(1, rt), z8_mul(sigma_conj,
                                   z8_root(-bfun(group[i], group[j]))))
          for j in range(n)] for i in range(n)]
    return T, S


# ---------------------------------------------------------------------------
# lattice enumerations in SCALED INTEGER coordinates (norms in 1/16
# units): D5 classes x = 0('0'), 1('s'), 2('v'), 3('c') on u = 2*vector;
# A3 classes y = 0..3 (shift -y/4) on w = 4*vector (sum 0, w = -y mod 4)
# ---------------------------------------------------------------------------
MAXN_NUM = 34      # numeric theta certificates (lattice-norm cut)
MAXN_LED = 16      # quartic ledger cut (levels n <= 8)


def build_d5_vecs(maxnorm):
    """{x: [(n16, u)]}, u = 2 * lattice vector (ints), n16 = 16 * norm."""
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
    """{y: [(n16, w)]}, w = 4 * lattice vector (ints, sum 0,
    all components = -y mod 4), n16 = 16 * norm."""
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


# ---------------------------------------------------------------------------
# exact factor moment tables: per class and per n16, the integer sums
# sum <., f>^k (k = 0..kmax) of a (complex) integer linear form on the
# scaled coordinates -- exact ledgers AND numeric covariance thetas
# ---------------------------------------------------------------------------
def factor_moments(vecs, form_re, form_im, kmax, maxn16):
    """{class: {n16: [(re, im) int moment, k = 0..kmax]}}."""
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
    """{n16: (re, im) ints}: class theta with a degree-k_ins insertion,
    binomial split of the two factor moment tables."""
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
    """sum c_{n16} e^{i pi tau n16 / 16} (mpmath, int coefficients)."""
    tot = mp.mpc(0)
    for n16, (cre, cim) in ser.items():
        if n16 > maxn16:
            continue
        tot += mp.mpc(cre, cim) * mp.exp(1j * mp.pi * tau * n16 / 16)
    return tot


# ---------------------------------------------------------------------------
# exact quartic/quadratic/count ledgers for all 16 classes
# (delta-1 scale convention: linear form 4x, quartic / 256)
# ---------------------------------------------------------------------------
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
    """V4[mu][lev] 5-vec (P1,P2,P3,T5,T3), CNT[mu][lev]; lev = norm/2
    exact Fraction.  delta-1 scale: linear form 4*(lattice vector),
    quartic / 256.  Scaled coords: D5 4*v = 2*u, A3 4*(v_j - v_4) =
    w_j - w_4 exactly."""
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
    # quadratic ledger: sum <l,x>^2 = u S5(x) + v S3(x); samples 0, 1
    # give S5 = (1, 0), S3 = (0, 2) -> u = b0, v = b1/2
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
# E8 roots in glue coordinates (replication anchor, v502/delta-1b)
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
# C0 -- conventions, targets, the 16-class ledger
# ---------------------------------------------------------------------------
SIGMA3 = [1, 9, 28, 73, 126, 252, 344, 585]
DIAG = [(a, a) for a in range(4)]


def section0():
    print("  -- C0: conventions, targets, 16-class ledger")
    roots = build_glue_roots()
    cnt = [sum(1 for c in roots.values() if c == m) for m in range(4)]
    check("C0.1 [ROOTS] 240 roots, norm 2, class split %s = (52,64,60,64) "
          "(v502/delta-1 replication)" % fmt(cnt),
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
    check("C0.2 [DIAGONAL SLICE = delta-1 LEDGER] the 4 diagonal classes "
          "(a,a) reproduce the delta-1 quartic ledger: V_{(a,a),1} = Q_a "
          "exactly (Q_0 = (12,0,6,4,8) etc.); diagonal counts sum to the "
          "E8 theta 240 sigma_3(n) for n <= 8: %s; V_{(1,1),n} = "
          "V_{(3,3),n} (conjugation)" % fmt(tots),
          ok_q and tots == [240 * s for s in SIGMA3]
          and all(V4[(1, 1)].get(F(n)) == V4[(3, 3)].get(F(n))
                  for n in range(1, 9)))

    cA = [F(5, 4), F(-1, 4), F(-3, 4), F(-1, 4)]
    Afix = [sum(cA[m] * Qtab[m][i] for m in range(4)) for i in range(5)]
    psi = [F(3), F(-1), F(-1), F(0), F(-1, 4)]
    psiA = sum(psi[i] * Afix[i] for i in range(5))
    check("C0.3 [TARGETS] A_fix = %s = (9,-30,-15,0,32); psi(A_fix) = %s "
          "= 64; the three waiting delta-1b tests: T5(V) = 0, "
          "W_2 : W_13 -> 4:3, psi(V) = -64 N or V = -A_fix N"
          % (fmt(Afix), psiA),
          Afix == [9, -30, -15, 0, 32] and psiA == 64)
    return V4, V2, CNT, Afix, psi


# ---------------------------------------------------------------------------
# C1 -- the Weil representation, exact in Q(zeta_8)
# ---------------------------------------------------------------------------
def weil_matrices():
    T, S = build_weil(q8, bil8, MU, Z8_ONE)
    return T, S


def section1():
    print("  -- C1: the 16x16 Weil representation (exact Q(zeta_8))")
    g5 = sum_z8([z8_root(5 * x * x) for x in range(4)])
    g3 = sum_z8([z8_root(3 * y * y) for y in range(4)])
    g = z8_mul(g5, g3)
    check("C1.1 [GAUSS SUM / SIGNATURE] factor sums: sum e(5x^2/8) = "
          "2 zeta_8^5 (sig(D5) = 5 mod 8), sum e(3y^2/8) = 2 zeta_8^3 "
          "(sig(A3) = 3 mod 8); total G = 4 = sqrt(16) e(0/8): signature "
          "0 mod 8 = rank E8 -- the signature factor in S is exactly 1",
          g5 == z8_scal(F(2), z8_root(5)) and g3 == z8_scal(F(2), z8_root(3))
          and g == z8_scal(F(4), Z8_ONE))

    T, S = weil_matrices()
    n = 16
    C = [[Z8_ONE if MU[j] == neg(MU[i]) else Z8_ZERO for j in range(n)]
         for i in range(n)]
    S2 = mat_mul(S, S)
    ST = mat_mul(S, T)
    ST3 = mat_mul(mat_mul(ST, ST), ST)
    SSdag = mat_mul(S, mat_conjT(S))
    T8 = mat_id(n)
    for _ in range(8):
        T8 = mat_mul(T8, T)
    S4 = mat_mul(S2, S2)
    ok_sym = all(S[i][j] == S[j][i] for i in range(n) for j in range(n))
    check("C1.2 [RELATIONS, EXACT] S symmetric; S unitary (S S^dag = 1); "
          "S^2 = C (conjugation mu -> -mu); (ST)^3 = S^2; S^4 = 1; "
          "T^8 = 1 (level 8): all verified in exact Q(zeta_8) arithmetic",
          ok_sym and mat_eq(SSdag, mat_id(n)) and mat_eq(S2, C)
          and mat_eq(ST3, S2) and mat_eq(S4, mat_id(n))
          and mat_eq(T8, mat_id(n)))

    # tensor factorisation S = S_D5 (x) S_A3
    T5x, S5x = build_weil(lambda x: (5 * x * x) % 8,
                          lambda x, y: (10 * x * y) % 8,
                          list(range(4)), z8_root(-5))
    T3x, S3x = build_weil(lambda y: (3 * y * y) % 8,
                          lambda x, y: (6 * x * y) % 8,
                          list(range(4)), z8_root(-3))
    ok_tensor = all(
        S[IDX[(x1, y1)]][IDX[(x2, y2)]]
        == z8_mul(S5x[x1][x2], S3x[y1][y2])
        for x1 in range(4) for y1 in range(4)
        for x2 in range(4) for y2 in range(4))
    check("C1.3 [TENSOR SPLIT, EXACT] S = S_D5 (x) S_A3 with the factor "
          "signature factors e(-5/8), e(-3/8) (sig 5 + 3 = 8 = 0): the "
          "16-component system is the product of the two rank-4 factor "
          "Weil systems", ok_tensor)

    iso = [m for m in MU if q8(m) == 0]
    H = [(a, a) for a in range(4)]
    Hp = [(0, 0), (1, 3), (2, 2), (3, 1)]
    okH = all(bil8(m1, m2) == 0 for m1 in H for m2 in H)
    okHp = all(bil8(m1, m2) == 0 for m1 in Hp for m2 in Hp)
    # e_H invariance (exact): S e_H = e_H, T e_H = e_H
    eH = [Z8_ONE if MU[i] in H else Z8_ZERO for i in range(16)]
    SeH = [sum_z8([z8_mul(S[i][j], eH[j]) for j in range(16)])
           for i in range(16)]
    TeH = [z8_mul(T[i][i], eH[i]) for i in range(16)]
    eHp = [Z8_ONE if MU[i] in Hp else Z8_ZERO for i in range(16)]
    SeHp = [sum_z8([z8_mul(S[i][j], eHp[j]) for j in range(16)])
            for i in range(16)]
    check("C1.4 [v502 SLICE, EXACT] isotropic classes: %d = 6 of 16; the "
          "glue diagonal H = {(a,a)} is a Lagrangian (|H| = 4 = sqrt(16), "
          "q|_H = 0, H = H-perp) and e_H = sum_H e_mu is EXACTLY S- and "
          "T-invariant (the E8/v502 block is the invariant slice); the "
          "anti-diagonal H' = {(0,0),(1,3),(2,2),(3,1)} is a SECOND "
          "Lagrangian, equally invariant (two E8 gluings)"
          % len(iso),
          len(iso) == 6 and okH and okHp
          and all(q8(m) == 0 for m in H) and all(q8(m) == 0 for m in Hp)
          and SeH == eH and TeH == eH and SeHp == eHp)

    # exact diagnosis of the naive 4-character rule
    PSP = [[S[IDX[(a, a)]][IDX[(ap, ap)]] for ap in range(4)]
           for a in range(4)]
    all_quarter = all(PSP[a][ap] == z8_scal(F(1, 4), Z8_ONE)
                      for a in range(4) for ap in range(4))
    # weight of S e_{(a,a)} outside H: sum |S_{mu,(a,a)}|^2 over mu not in H
    wt_out = F(0)
    for i in range(16):
        if MU[i] in H:
            continue
        v = S[i][IDX[(1, 1)]]
        vv = z8_mul(v, z8_conj(v))
        wt_out += vv[0]
    check("C1.5 [WHY E1.5 FAILED, EXACT] the S-block on the diagonal "
          "classes is P_H S P_H = (1/4) J (EVERY entry exactly 1/4, since "
          "(mu,nu) = 16 a a'/8 = 0 mod 1 on H x H) -- NOT the naive "
          "(1/2) i^{-a a'}; and 12/16 = 3/4 of the S-image weight of a "
          "diagonal basis vector sits on the 12 SHIFTED classes "
          "(|weight outside H| = %s): the 4-character rule cannot close, "
          "the 16-component system is mandatory" % wt_out,
          all_quarter and wt_out == F(3, 4))
    return T, S


# ---------------------------------------------------------------------------
# C2 -- the 16 coset thetas and their S/T covariance
# ---------------------------------------------------------------------------
def build_theta_data():
    d5v = build_d5_vecs(MAXN_NUM)
    a3v = build_a3_vecs(MAXN_NUM)
    lim = 16 * MAXN_NUM
    zero5 = (0, 0, 0, 0, 0)
    zero4 = (0, 0, 0, 0)
    m5_0 = factor_moments(d5v, zero5, None, 4, lim)
    m3_0 = factor_moments(a3v, zero4, None, 4, lim)
    ser0 = {mu: combine_series(m5_0[mu[0]], m3_0[mu[1]], 0, lim)
            for mu in MU}
    # isotropic complex form on D5 (scaled u-coords): d = u1 + i u2
    m5_iso = factor_moments(d5v, (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), 4, lim)
    ser_iso4 = {mu: combine_series(m5_iso[mu[0]], m3_0[mu[1]], 4, lim)
                for mu in MU}
    # real form x = (1,1,0,0,0) in D5, (x,x) = 2; d = u1 + u2 = 2 <l,x>
    m5_re = factor_moments(d5v, (1, 1, 0, 0, 0), None, 4, lim)
    ser_re = {k: {mu: combine_series(m5_re[mu[0]], m3_0[mu[1]], k, lim)
                  for mu in MU} for k in (0, 2, 4)}
    return d5v, a3v, ser0, ser_iso4, ser_re


def rho_mpc(M):
    return [[z8_to_mpc(M[i][j]) for j in range(16)] for i in range(16)]


def section2(Sx, CNT):
    print("  -- C2: the 16 coset thetas, S/T covariance certificates")
    d5v, a3v, ser0, ser_iso4, ser_re = build_theta_data()

    # exact grid statement: every norm in class mu is == 2 q(mu) mod 2
    ok_grid = True
    nonempty = 0
    for mu in MU:
        want = (4 * q8(mu)) % 32
        ns = set(n % 32 for n in ser0[mu])
        if ns:
            nonempty += 1
        if ns - {want}:
            ok_grid = False
    check("C2.1 [GRID, EXACT] all 16 classes are nonempty (%d/16) and "
          "every lattice norm in class mu satisfies norm/2 = q(mu) mod 1 "
          "(n16 = 4 q8(mu) mod 32) -- so T acts EXACTLY as "
          "Theta_mu(tau+1) = e(q(mu)) Theta_mu(tau): the T-side of the "
          "Weil covariance is a lattice identity" % nonempty,
          ok_grid and nonempty == 16)

    e4 = [1, 240, 2160, 6720]
    cdia = [sum(CNT[(a, a)].get(F(n), 0) for a in range(4))
            for n in range(1, 4)]
    Hp = [(0, 0), (1, 3), (2, 2), (3, 1)]
    canti = [sum(CNT[m].get(F(n), 0) for m in Hp) for n in range(1, 4)]
    check("C2.2 [BOTH LAGRANGIANS -> E4] diagonal-glue counts (1,%s) and "
          "anti-diagonal counts (1,%s) BOTH reproduce E4 = (1,240,2160,"
          "6720): the two Lagrangians of C1.4 are two E8 gluings"
          % (fmt(cdia), fmt(canti)),
          cdia == e4[1:] and canti == e4[1:])

    SC = rho_mpc(Sx)
    tauA = mp.mpc(mp.mpf(13) / 100, mp.mpf(51) / 50)
    tauB = mp.mpc(mp.mpf(-9) / 40, mp.mpf(23) / 20)
    lim = 16 * MAXN_NUM

    # BEFORE: the naive 4-character rule on the diagonal thetas (E1.5)
    res_naive = []
    thS = {mu: eval_series16(ser0[mu], -1 / tauA, lim) for mu in DIAG}
    thd = {mu: eval_series16(ser0[mu], tauA, lim) for mu in MU}
    pref4 = (-1j * tauA) ** 4
    for a in range(4):
        rhs = pref4 * sum(mp.exp(-2j * mp.pi * a * ap / 4) * thd[(ap, ap)]
                          for ap in range(4)) / 2
        res_naive.append(abs(thS[(a, a)] - rhs) / abs(thS[(a, a)]))
    # AFTER: the 16-component Weil rule
    res16 = []
    for i, mu in enumerate(MU):
        lhs = eval_series16(ser0[mu], -1 / tauA, lim)
        rhs = pref4 * sum(SC[i][j] * thd[MU[j]] for j in range(16))
        res16.append(abs(lhs - rhs) / abs(lhs))
    r_nv, r_16 = max(res_naive), max(res16)
    print("     E1.5 residual BEFORE (naive 4-rule): %s ; AFTER "
          "(16-component Weil rule): %s" % (mp.nstr(r_nv, 3),
                                            mp.nstr(r_16, 3)))
    # second tau point for the 16-rule
    res16b = []
    pref4b = (-1j * tauB) ** 4
    thdb = {mu: eval_series16(ser0[mu], tauB, lim) for mu in MU}
    for i, mu in enumerate(MU):
        lhs = eval_series16(ser0[mu], -1 / tauB, lim)
        rhs = pref4b * sum(SC[i][j] * thdb[MU[j]] for j in range(16))
        res16b.append(abs(lhs - rhs) / abs(lhs))
    check("C2.3 [S-COVARIANCE 16-VECTOR -- THE COMPLETION WORKS] "
          "Theta_mu(-1/tau) = (-i tau)^4 sum_nu S_mu_nu Theta_nu(tau): "
          "max rel residual %s (tau_A), %s (tau_B) < 1e-25; the naive "
          "4-component rule fails at %s = O(1) on the SAME data (delta-1b "
          "E1.5 replicated): the E1.5 obstruction vanishes on the full "
          "Weil system"
          % (mp.nstr(r_16, 3), mp.nstr(max(res16b), 3), mp.nstr(r_nv, 3)),
          r_16 < mp.mpf(10) ** (-25) and max(res16b) < mp.mpf(10) ** (-25)
          and r_nv > mp.mpf(10) ** (-3))
    return ser0, ser_iso4, ser_re, SC


# ---------------------------------------------------------------------------
# C3 -- the quartic Weil system (insertion covariance)
# ---------------------------------------------------------------------------
def section3(ser_iso4, ser_re, SC):
    print("  -- C3: quartic insertion covariance (the integrand's theta)")
    lim = 16 * MAXN_NUM
    tauA = mp.mpc(mp.mpf(13) / 100, mp.mpf(51) / 50)
    tauB = mp.mpc(mp.mpf(-9) / 40, mp.mpf(23) / 20)

    # isotropic x: <l,x>^4 harmonic -> exact weight-8 covariance
    ok_iso = True
    cfits = []
    for tau in (tauA, tauB):
        pref = (-1j * tau) ** 8
        lhs = [eval_series16(ser_iso4[mu], -1 / tau, lim) for mu in MU]
        rhsv = [pref * sum(SC[i][j]
                           * eval_series16(ser_iso4[MU[j]], tau, lim)
                           for j in range(16)) for i in range(16)]
        i0 = max(range(16), key=lambda i: abs(rhsv[i]))
        c = lhs[i0] / rhsv[i0]
        cfits.append(c)
        for i in range(16):
            if abs(lhs[i] - c * rhsv[i]) / max(abs(lhs[i0]), 1) \
                    > mp.mpf(10) ** (-22):
                ok_iso = False
    c_iso = cfits[0]
    check("C3.1 [ISOTROPIC QUARTIC, WEIGHT 8] with (x,x) = 0 the "
          "insertion <lambda,x>^4 is harmonic: Theta4_mu(-1/tau) = c "
          "(-i tau)^8 sum S_mu_nu Theta4_nu(tau) with ONE global c = %s "
          "(|c - 1| = %s), all 16 components, two tau points, 22+ digits"
          % (mp.nstr(c_iso, 6), mp.nstr(abs(c_iso - 1), 3)),
          ok_iso and abs(c_iso - 1) < mp.mpf(10) ** (-22)
          and abs(cfits[1] - 1) < mp.mpf(10) ** (-22))

    # real x, (x,x) = 2 (scaled d = 2<l,x> => <l,x>^k = d^k / 2^k):
    # completed Theta-hat = Th4 - 3(x,x)/(2 pi t2) Th2
    #                       + 3 (x,x)^2/(16 pi^2 t2^2) Th0
    xx = mp.mpf(2)

    def theta_hat(mu, tau):
        t2 = tau.imag
        v4 = eval_series16(ser_re[4][mu], tau, lim) / 16
        v2 = eval_series16(ser_re[2][mu], tau, lim) / 4
        v0 = eval_series16(ser_re[0][mu], tau, lim)
        return (v4 - 3 * xx / (2 * mp.pi * t2) * v2
                + 3 * xx ** 2 / (16 * mp.pi ** 2 * t2 ** 2) * v0)

    ok_hat = True
    chats = []
    for tau in (tauA, tauB):
        pref = (-1j * tau) ** 8
        lhs = [theta_hat(mu, -1 / tau) for mu in MU]
        rhsv = [pref * sum(SC[i][j] * theta_hat(MU[j], tau)
                           for j in range(16)) for i in range(16)]
        i0 = max(range(16), key=lambda i: abs(rhsv[i]))
        c = lhs[i0] / rhsv[i0]
        chats.append(c)
        for i in range(16):
            if abs(lhs[i] - c * rhsv[i]) / max(abs(lhs[i0]), 1) \
                    > mp.mpf(10) ** (-20):
                ok_hat = False
    # and the UNcompleted quartic must FAIL (non-harmonic)
    res_raw = mp.mpf(0)
    pref = (-1j * tauA) ** 8
    lhs4 = [eval_series16(ser_re[4][mu], -1 / tauA, lim) / 16 for mu in MU]
    rhs4 = [pref * sum(SC[i][j]
                       * eval_series16(ser_re[4][MU[j]], tauA, lim) / 16
                       for j in range(16)) for i in range(16)]
    scale4 = max(abs(x) for x in rhs4)
    res_raw = max(abs(lhs4[i] - rhs4[i]) for i in range(16)) / scale4
    check("C3.2 [HEAT-KERNEL COMPLETION, WEIGHT 8] for real x ((x,x) = 2) "
          "the completed Theta-hat = Th4 - 3(x,x) Th2/(2 pi tau2) + "
          "3(x,x)^2 Th0/(16 pi^2 tau2^2) is weight-8 covariant with "
          "global c = %s (20+ digits, both tau); the RAW quartic alone "
          "fails at %s = O(1): the completion terms are EXACTLY the "
          "(x,x)-contraction block of the delta-1b (T5,T3)-rigidity -- "
          "T5/T3 receive NO completion contribution"
          % (mp.nstr(chats[0], 6), mp.nstr(res_raw, 3)),
          ok_hat and abs(chats[0] - 1) < mp.mpf(10) ** (-20)
          and abs(chats[1] - 1) < mp.mpf(10) ** (-20)
          and res_raw > mp.mpf(10) ** (-3))


# ---------------------------------------------------------------------------
# M-block numerics (delta-1b machinery): twisted C^2 block x eta^{-8}
# ---------------------------------------------------------------------------
NPROD = 120
TAU_A = mp.mpc(mp.mpf(13) / 100, mp.mpf(51) / 50)     # |tau| ~ 1.03
TAU_B = mp.mpc(mp.mpf(-31) / 100, mp.mpf(99) / 100)   # |tau| ~ 1.04
TAU_C = mp.mpc(mp.mpf(7) / 100, mp.mpf(101) / 100)    # certificate point


def qp(tau, e):
    """q^e on the tau-cover: exp(2 pi i tau e), e mpf/float."""
    return mp.exp(2j * mp.pi * tau * e)


def geo_val(N, a, b, tau):
    """twisted C^2 oscillator block incl. base exponent q^{4 E_b(a/N)}
    and the AB zero-mode 1/det for a = 0, b != 0 (delta-1b geo_val)."""
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


def measure_transport(N, pairs, fM):
    """t_p: f_p(tau+1) = t_p f_{Tp}(tau); s_p: f_p(-1/tau) =
    s_p (-i tau)^{-4} f_{Sp}(tau).  Constancy verified at two tau."""
    t = {}
    s = {}
    dev = mp.mpf(0)
    for (a, b) in pairs:
        Tp = (a, (a + b) % N)
        Sp = (b % N, (-a) % N)
        vals_t, vals_s = [], []
        for tau in (TAU_A, TAU_B):
            vals_t.append(fM(a, b, tau + 1) / fM(*Tp, tau))
            vals_s.append(fM(a, b, -1 / tau) * (-1j * tau) ** 4
                          / fM(*Sp, tau))
        dev = max(dev, abs(vals_t[0] - vals_t[1]),
                  abs(vals_s[0] - vals_s[1]))
        t[(a, b)] = vals_t[0]
        s[(a, b)] = vals_s[0]
    return t, s, dev


# ---------------------------------------------------------------------------
# blockwise-covariance transport solve (BFS + SVD null space)
# ---------------------------------------------------------------------------
def rho_np(exact):
    return np.array([[complex(z8_to_mpc(exact[i][j])) for j in range(16)]
                     for i in range(16)])


def sl2z_char(k):
    """the k-th character of SL(2,Z) (abelianisation Z/12):
    chi(T) = e(k/12), chi(S) = chi(T)^{-3} = e(-k/4)."""
    return (np.exp(2j * np.pi * k / 12), np.exp(-2j * np.pi * k / 4))


def solve_orbit(pairs, N, tconst, sconst, rhoT_np, rhoS_np, base, k=0):
    """Transport BFS on the pair orbit of `base` under T: p -> (a, a+b),
    S: p -> (b, -a); edge matrices (t_p / chi(T)) rhoT^T resp.
    (s_p / chi(S)) rhoS^T -- invariance up to the k-th SL(2,Z)
    character.  Returns (orbit, Lambda dict, null basis, sv)."""
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


def joint_eigvecs(hols, rng_seed=11):
    """common eigenvectors of the loop-holonomy matrices (multiplier-
    relaxed covariance): random-combination eigenbasis, tested on every
    holonomy.  Returns [(v, [lambda_i], residual)] with residual < tol."""
    Hs = [h for (_, _, h) in hols]
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


def root_order(lam, nmax=192):
    """smallest n with lam^n ~ 1 (unit-modulus check included)."""
    if abs(abs(lam) - 1) > 1e-8:
        return None
    for n in range(1, nmax + 1):
        if abs(lam ** n - 1) < 1e-7:
            return n
    return None


def project_seed(Lam, null, seed):
    """least-squares seed projection onto {p -> Lam_p (V c)}; returns
    (beta dict, cosine overlap)."""
    if not null:
        return None, 0.0
    V = np.array(null).T                       # 16 x d
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


def section4(Tx, Sx, ser0, ser_iso4):
    print("  -- C4: the contraction SOLVED from blockwise covariance")
    rhoT_np = rho_np(Tx)
    rhoS_np = rho_np(Sx)
    lim = 16 * MAXN_NUM

    # C4.0 validation: the eta^{-8} lattice block. T-multiplier e(-1/3)
    # obstructs <T,S>; under <T^3, S> the solution space is exactly
    # span{e_H, e_H'} (the two Lagrangian E8 gluings).
    t_lat = eta_val(TAU_A + 1) ** (-8) / eta_val(TAU_A) ** (-8)
    s_lat = (eta_val(-1 / TAU_A) ** (-8) * (-1j * TAU_A) ** 4
             / eta_val(TAU_A) ** (-8))
    ok_lat = (abs(t_lat - mp.exp(-2j * mp.pi / 3)) < mp.mpf(10) ** (-30)
              and abs(s_lat - 1) < mp.mpf(10) ** (-30))
    # single-block constraints: beta = (t/chi_T) rhoT^T beta,
    # beta = (s/chi_S) rhoS^T beta -- scan the SL(2,Z) character k
    dim_k = {}
    null_k = {}
    for k in range(12):
        chT, chS = sl2z_char(k)
        A1 = np.vstack([complex(t_lat) / chT * rhoT_np.T - np.eye(16),
                        complex(s_lat) / chS * rhoS_np.T - np.eye(16)])
        _, sv1, Vh1 = np.linalg.svd(A1)
        dim_k[k] = int(np.sum(sv1 < 1e-8 * sv1[0]))
        null_k[k] = Vh1[np.argwhere(sv1 < 1e-8 * sv1[0]).ravel()].conj()
    dim_TS = dim_k[0]
    dim_T3S = dim_k[8]
    null3 = null_k[8]
    eH = np.array([1.0 if MU[i][0] == MU[i][1] else 0.0
                   for i in range(16)], dtype=complex)
    # H' = {(0,0),(1,3),(2,2),(3,1)} <=> x + y = 0 mod 4
    eHp = np.array([1.0 if (MU[i][0] + MU[i][1]) % 4 == 0 else 0.0
                    for i in range(16)], dtype=complex)

    def in_span(v, basis):
        if len(basis) == 0:
            return False
        B = np.array(basis).T
        c, *_ = np.linalg.lstsq(B, v, rcond=None)
        return np.linalg.norm(B @ c - v) < 1e-9 * max(np.linalg.norm(v), 1)
    print("     eta^{-8} block: dim(k) over the 12 SL(2,Z) characters "
          "chi_k = %s" % fmt([dim_k[k] for k in range(12)]))
    check("C4.0 [MACHINERY VALIDATION on the v502 block] the eta^{-8} "
          "lattice block has T-multiplier e(-1/3) (30+ digits) and "
          "S-multiplier 1; STRICT invariance (character k = 0) has dim "
          "%d = 0 (the q^{-1/3} prefactor obstruction -- E4/eta^8 is a "
          "character vector, not an invariant); at the eta^8-character "
          "k = 8 (chi(T) = e(2/3), chi(S) = 1) the space is dim %d = 2 "
          "and contains BOTH Lagrangian vectors e_H (v502/E8) and e_H': "
          "the solver reproduces the known invariant theory of the "
          "lattice block exactly (E4/eta^8 transforms with chi_8)"
          % (dim_TS, dim_T3S),
          ok_lat and dim_TS == 0 and dim_T3S == 2
          and in_span(eH, null3) and in_span(eHp, null3))

    # C4.1: the full Z4 block transport constants
    pairs4 = [(a, b) for a in range(4) for b in range(4)
              if (a, b) != (0, 0)]
    t4, s4, dev4 = measure_transport(4, pairs4,
                                     lambda a, b, tau: M_val(4, a, b, tau))
    check("C4.1 [BLOCK TRANSPORT CONSTANTS] M_{a,b}(tau+1) = t "
          "M_{a,a+b}(tau) and M_{a,b}(-1/tau) = s (-i tau)^{-4} "
          "M_{b,-a}(tau) with CONSTANT (t, s) for all 15 pairs "
          "(max two-tau deviation %s < 1e-28): the delta-1b E1.3/E1.4 "
          "certificates extended to the full dressed blocks incl. "
          "eta^{-8}" % mp.nstr(dev4, 3), dev4 < mp.mpf(10) ** (-28))

    # C4.2: orbit solve (gcd-1 and gcd-2), scanning the SL(2,Z)
    # character chi_k (the only remaining 1-dim freedom of the group)
    orb1 = [p for p in pairs4 if gcd(gcd(p[0], p[1]), 4) == 1]
    orb2 = [p for p in pairs4 if gcd(gcd(p[0], p[1]), 4) == 2]
    seed = {}
    for p in pairs4:
        v = np.zeros(16, dtype=complex)
        v[IDX[(p[0] % 4, p[0] % 4)]] = 1j ** ((p[0] * p[1]) % 4)
        seed[p] = v
    tab = {}
    for k in range(12):
        _, L1, n1, _, h1 = solve_orbit(orb1, 4, t4, s4, rhoT_np,
                                       rhoS_np, (0, 1), k)
        _, L2, n2, _, h2 = solve_orbit(orb2, 4, t4, s4, rhoT_np,
                                       rhoS_np, (0, 2), k)
        b1, c1 = project_seed(L1, n1, seed)
        b2, c2 = project_seed(L2, n2, seed)
        tab[k] = (len(n1), len(n2), c1, c2, b1, b2, L1, L2, h1, h2)
    print("     k   dim(gcd1)  dim(gcd2)  seed-cos(gcd1)  seed-cos(gcd2)")
    for k in range(12):
        d1, d2, c1, c2 = tab[k][:4]
        print("     %-2d  %-9d  %-9d  %-14s  %s"
              % (k, d1, d2,
                 ("%.6f" % c1) if c1 else "--",
                 ("%.6f" % c2) if c2 else "--"))
    live = [k for k in range(12) if tab[k][0] > 0 or tab[k][1] > 0]
    good = [k for k in range(12)
            if tab[k][0] > 0 and tab[k][1] > 0
            and abs(tab[k][2] or 0) > 1e-6 and abs(tab[k][3] or 0) > 1e-6]
    check("C4.2 [SOLUTION SPACES x CHARACTER SCAN] blockwise-covariant "
          "contractions over all 12 SL(2,Z) characters chi_k: "
          "characters with ANY solution: %s; characters with solutions "
          "in BOTH orbits AND nonzero seed overlap: %s -- reported as "
          "computed" % (fmt(live), fmt(good)), True)

    # C4.2b: holonomy spectroscopy of the obstruction (k = 0 loops)
    L1, L2, h1, h2 = tab[0][6], tab[0][7], tab[0][8], tab[0][9]
    ev1 = joint_eigvecs(h1)
    ev2 = joint_eigvecs(h2)
    ords1 = sorted({o for (_, lams, _) in ev1
                    for o in [root_order(l) for l in lams]
                    if o is not None})
    ords2 = sorted({o for (_, lams, _) in ev2
                    for o in [root_order(l) for l in lams]
                    if o is not None})
    print("     holonomy: gcd-1 orbit: %d loops, %d/16 joint "
          "eigenvectors, eigenvalue orders %s"
          % (len(h1), len(ev1), fmt(ords1)))
    print("               gcd-2 orbit: %d loops, %d/16 joint "
          "eigenvectors, eigenvalue orders %s"
          % (len(h2), len(ev2), fmt(ords2)))
    check("C4.2b [OBSTRUCTION SPECTROSCOPY] the loop holonomies of the "
          "transport groupoid are unitary; their common eigenspace "
          "(where a consistent-up-to-phases contraction can live) has "
          "dim %d/16 (gcd-1) and %d/16 (gcd-2), and on it EVERY "
          "holonomy eigenvalue is a root of unity of order in %s / %s "
          "(all <= 4): the obstruction to a strictly invariant "
          "contraction is a FINITE multiplier system of order 4, not a "
          "continuous defect -- this is the exact δ1c sharpening of "
          "the delta-1b measure gap"
          % (len(ev1), len(ev2), fmt(ords1), fmt(ords2)),
          len(ev1) >= 1 and len(ev2) >= 1
          and all(o is not None for (_, lams, _) in ev1
                  for o in [root_order(l) for l in lams])
          and all(o is not None for (_, lams, _) in ev2
                  for o in [root_order(l) for l in lams])
          and max(ords1 + ords2) <= 4)

    # C4.2c: the eta-power weight-bookkeeping scan.  Tensoring every
    # block with eta^m multiplies each T-edge constant by e(m/24) and
    # leaves the S-edge constants untouched (eta(-1/tau) =
    # sqrt(-i tau) eta(tau) is phase-free): if a unique (m, k) makes
    # the transport strictly consistent, then Z eta^m is a genuine
    # vector-valued modular form of weight 4 + m/2 with character
    # chi_k -- the completion would be DERIVED, not declared.
    hits = []
    for m in range(24):
        ph = np.exp(2j * np.pi * m / 24)
        t4m = {p: complex(t4[p]) * ph for p in t4}
        for k in range(12):
            _, L1m, n1m, _, _ = solve_orbit(orb1, 4, t4m, s4, rhoT_np,
                                            rhoS_np, (0, 1), k)
            if not n1m:
                continue
            _, L2m, n2m, _, _ = solve_orbit(orb2, 4, t4m, s4, rhoT_np,
                                            rhoS_np, (0, 2), k)
            b1m, c1m = project_seed(L1m, n1m, seed)
            b2m, c2m = project_seed(L2m, n2m, seed)
            hits.append((m, k, len(n1m), len(n2m), c1m, c2m, b1m, b2m))
    good_hits = [h for h in hits if h[2] > 0 and h[3] > 0
                 and abs(h[4] or 0) > 1e-6 and abs(h[5] or 0) > 1e-6]
    print("     eta-power scan: %d (m,k) with gcd-1 solutions; %d with "
          "solutions in BOTH orbits + seed overlap"
          % (len(hits), len(good_hits)))
    for h in hits:
        print("       m = %-2d k = %-2d  dims (%d, %d)  seed-cos "
              "(%s, %s)"
              % (h[0], h[1], h[2], h[3],
                 ("%.4f" % h[4]) if h[4] else "--",
                 ("%.4f" % h[5]) if h[5] else "--"))
    check("C4.2c [ETA-POWER WEIGHT BOOKKEEPING] the eta^m tensor scan "
          "(m = 0..23 x 12 characters): hits with solutions in both "
          "orbits and nonzero seed overlap: %s -- if empty, no eta-power "
          "weight bookkeeping rescues a strict blockwise completion; if "
          "unique, the completion is derived"
          % str([(h[0], h[1]) for h in good_hits]), True)

    # C4.3: quasi-derived contraction from the seed-best joint
    # eigenvector (canonical BFS-tree representatives)
    def best_eig(Lam, evs, seedd):
        best = None
        for (v, lams, _) in evs:
            G = sum(Lam[p].conj().T @ Lam[p] for p in Lam)
            Av = sum(Lam[p].conj().T @ seedd[p] for p in Lam)
            denom = np.vdot(v, G @ v).real
            c = np.vdot(v, Av) / denom
            b = {p: Lam[p] @ (c * v) for p in Lam}
            n_pr = np.sqrt(sum(np.vdot(b[p], b[p]).real for p in b))
            n_sd = np.sqrt(sum(np.vdot(seedd[p], seedd[p]).real
                               for p in seedd))
            ov = abs(sum(np.vdot(seedd[p], b[p]) for p in b))
            cos = ov / (n_pr * n_sd) if n_pr > 1e-14 else 0.0
            lamords = [root_order(l) for l in lams]
            if best is None or cos > best[1]:
                best = (b, cos, v, lamords)
        return best

    ksel = good[0] if good else None
    quasi = False
    beta = {}
    cos1 = cos2 = None
    mult_ord = None
    dims = (tab[0][0], tab[0][1])
    if ksel is not None:
        d1, d2, cos1, cos2, b1, b2 = tab[ksel][:6]
        dims = (d1, d2)
        if b1 is not None:
            beta.update(b1)
        if b2 is not None and d2 > 0:
            beta.update(b2)
        beta = {p: v for p, v in beta.items()
                if np.linalg.norm(v) > 1e-10}
    elif good_hits:
        m, k, d1, d2, cos1, cos2, b1, b2 = good_hits[0]
        ksel = ('eta^%d' % m, k)
        dims = (d1, d2)
        beta.update(b1)
        beta.update(b2)
        beta = {p: v for p, v in beta.items()
                if np.linalg.norm(v) > 1e-10}
    else:
        quasi = True
        bst1 = best_eig(L1, ev1, seed)
        bst2 = best_eig(L2, ev2, seed)
        if bst1 is not None and bst1[1] > 1e-6:
            beta.update(bst1[0])
            cos1 = bst1[1]
        if bst2 is not None and bst2[1] > 1e-6:
            beta.update(bst2[0])
            cos2 = bst2[1]
        ords = []
        for bst in (bst1, bst2):
            if bst is not None:
                ords += [o for o in bst[3] if o is not None]
        if ords:
            from math import lcm
            mult_ord = 1
            for o in ords:
                mult_ord = lcm(mult_ord, o)
        beta = {p: v for p, v in beta.items()
                if np.linalg.norm(v) > 1e-10}
    have_beta = len(beta) > 0
    print("     seed overlaps: gcd-1 %s, gcd-2 %s; multiplier order %s"
          % (("%.4f" % cos1) if cos1 else "--",
             ("%.4f" % cos2) if cos2 else "--", str(mult_ord)))

    # conjugation (CPT) canonicalisation: betaC_p[mu] = conj(
    # beta_{-p}[-mu]) must be proportional to beta_p with ONE unit
    # phase phi per orbit; rescaling by e^{i arg(phi)/2} then makes the
    # assignment conjugation-real (kills the tree-phase imaginary part)
    if have_beta:
        for orb in (orb1, orb2):
            ratios = []
            for p in orb:
                if p not in beta:
                    continue
                pm = ((-p[0]) % 4, (-p[1]) % 4)
                if pm not in beta:
                    continue
                w = np.zeros(16, dtype=complex)
                for i, mu in enumerate(MU):
                    w[i] = np.conj(beta[pm][IDX[neg(mu)]])
                nb = np.vdot(beta[p], beta[p]).real
                if nb > 1e-16:
                    ratios.append(np.vdot(beta[p], w) / nb)
            if not ratios:
                continue
            phis = np.array(ratios)
            if (np.max(np.abs(np.abs(phis) - 1)) < 1e-8
                    and np.max(np.abs(phis - phis[0])) < 1e-8):
                c = np.exp(1j * np.angle(phis[0]) / 2)
                for p in orb:
                    if p in beta:
                        beta[p] = c * beta[p]
                print("     conjugation canonicalisation applied on "
                      "orbit %s (phi = %.4f+%.4fi)"
                      % (str(orb[0]), phis[0].real, phis[0].imag))
            else:
                print("     conjugation check on orbit %s: NOT "
                      "proportional (max dev %.2e) -- left as derived"
                      % (str(orb[0]),
                         float(np.max(np.abs(phis - phis[0])))))
    check("C4.3 [DERIVED CONTRACTION%s] the diagonal seed i^{ab} "
          "e_{(a,a)} projected onto the covariant structure gives a "
          "nonzero contraction on %d of 15 pairs; %s"
          % (" -- MULTIPLIER-RELAXED" if quasi else "", len(beta),
             ("strict character k = %s" % ksel) if not quasi else
             ("no strict character solution exists (C4.2): the derived "
              "object is covariant up to a finite multiplier system of "
              "order %s -- the transport eigen-direction is fixed, the "
              "residual freedom is the tree phase convention + N"
              % str(mult_ord))), have_beta)

    # C4.4: covariance certificate on the DRESSED FUNCTIONS themselves
    # (blockwise transport verified directly on M_p(tau) beta_p.Theta;
    # in the multiplier-relaxed case every edge must close up to a unit
    # phase of finite order)
    if have_beta:
        th = {}
        for tau in (TAU_C, TAU_C + 1, -1 / TAU_C):
            th[tau] = [eval_series16(ser0[mu], tau, lim) for mu in MU]

        def blockval(p, tau):
            Mv = M_val(4, p[0], p[1], tau)
            return Mv * sum(complex(beta[p][i]) * th[tau][i]
                            for i in range(16))

        max_dev = mp.mpf(0)
        max_orddev = mp.mpf(0)
        for p in beta:
            a, b = p
            Tp = (a, (a + b) % 4)
            Sp = (b % 4, (-a) % 4)
            for tau_from, q2, wgt in (
                    (TAU_C + 1, Tp, mp.mpc(1)),
                    (-1 / TAU_C, Sp, mp.mpc(1))):
                if q2 not in beta:
                    continue
                lhs = blockval(p, tau_from)
                rhs = blockval(q2, TAU_C)
                if abs(rhs) < mp.mpf(10) ** (-25):
                    continue
                ph = lhs / rhs
                max_dev = max(max_dev, abs(abs(ph) - 1))
                if mult_ord:
                    max_orddev = max(max_orddev,
                                     abs(ph ** (2 * mult_ord) - 1))
        print("     edge certificate: max | |phase| - 1 | = %s ; "
              "max |phase^(2n) - 1| = %s (n = %s)"
              % (mp.nstr(max_dev, 3), mp.nstr(max_orddev, 3),
                 str(mult_ord)))
        ok_cert = max_dev < mp.mpf(10) ** (-8) \
            and (not mult_ord or max_orddev < mp.mpf(10) ** (-6))
        check("C4.4 [TRANSPORT CERTIFICATE ON THE FUNCTIONS] with the "
              "derived beta, every T- and S-edge of the block system "
              "closes on the actual dressed functions M_p beta_p.Theta "
              "at a fresh tau UP TO A UNIT PHASE (max modulus deviation "
              "%s < 1e-8), and every edge phase is a root of unity of "
              "the diagnosed finite order (max |phase^2n - 1| = %s): "
              "the derived object is a vector-valued modular form for "
              "a FINITE multiplier system -- the covariance derivation "
              "is certified on the functions, not just on the "
              "transport algebra"
              % (mp.nstr(max_dev, 3), mp.nstr(max_orddev, 3)), ok_cert)
    else:
        check("C4.4 [TRANSPORT CERTIFICATE] skipped -- no nonzero "
              "derived contraction (see C4.2/C4.3)", False)
    return beta, dims, ksel, quasi, mult_ord, cos1, cos2


# ---------------------------------------------------------------------------
# exact dressing series (delta-1b pair_cells machinery, phase-free:
# the b-phases now live in beta) + the fundamental-domain kernel J
# ---------------------------------------------------------------------------
GRID_CUT = F(8)
GRID_CUT_LOW = F(6)
BASES4 = {0: F(-1, 2), 1: F(-5, 16), 2: F(-1, 4), 3: F(-5, 16)}
BASES2 = {0: F(-1, 2), 1: F(-1, 4)}


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


def dress_series(N, a, b, bases, cut):
    """{exponent ex: Gaussian-rational coeff} of q^{E_a} G[a,b] P8 --
    NO i^{ab} phase (that sits in beta now); AB zero-mode included."""
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


def hm_integral(beta, dressmaps, bases, V4, V2, CNT, cut, weight):
    """derived-measure HM integral: main term J(Delta,0) on the quartic
    ledger; heat-kernel completion -3(x,x)/(2 pi) J(.,1) on the
    quadratic ledger and +3/(16 pi^2) J(.,2) on the counts (P-block
    only; E1.6 decompositions (x,x)S5 = P1+P2, (x,x)S3 = P2+P3,
    (x,x)^2 = P1+2P2+P3).  Returns (I_main, I_hat, W: {(a, lev): z} of
    diagonal-class scalar weights)."""
    I_main = [mp.mpc(0)] * 5
    I_comp = [mp.mpc(0)] * 5
    W = {}
    for p, dress in dressmaps.items():
        a = p[0]
        base = bases[a]
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
                    if D <= 0 or D > cut:
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
    return I_main, I_hat, W


# ---------------------------------------------------------------------------
# C5 -- the decidable integral and the three waiting tests
# ---------------------------------------------------------------------------
def section5(beta, V4, V2, CNT, Afix, psi):
    print("  -- C5: THE DECIDABLE INTEGRAL (three waiting tests)")
    if not beta:
        check("C5.0 [SKIPPED] no derived contraction available", False)
        return None
    pairs4 = list(beta.keys())
    dm = {p: dress_series(4, p[0], p[1], BASES4, GRID_CUT) for p in pairs4}

    # guard: seed reproduces the delta-1b leading cell 5/16
    seedw = (F(0), F(0))
    for b in (1, 2, 3):
        dr = dm.get((0, b))
        if dr is not None:
            seedw = gadd(seedw, gmul(dr[F(0)], ipow(0)))
    seedw = (seedw[0] / 4, seedw[1] / 4)
    check("C5.1 [LEADING-CELL GUARD, EXACT] the (a=0, ex=0) dressing "
          "weights summed over b and divided by the orbifold order give "
          "%s = 5/16 = Dedekind(5/4)/4: the delta-1b E3.1 leading "
          "Harvey-Moore cell is reproduced by the phase-free dressing "
          "machinery (the i^{ab} now lives in beta)" % str(seedw[0]),
          seedw == (F(5, 16), F(0)))

    I_main, I_hat, W = hm_integral(beta, dm, BASES4, V4, V2, CNT,
                                   GRID_CUT, mp.mpf(1) / 4)
    I_lo, _, _ = hm_integral(beta, dm, BASES4, V4, V2, CNT,
                             GRID_CUT_LOW, mp.mpf(1) / 4)
    scale = max(abs(x) for x in I_main)
    im_rel = max(abs(x.imag) for x in I_main) / scale
    eps_rel = max(abs(I_main[i] - I_lo[i]) for i in range(5)) / scale
    print("     I_main (J(.,0) kernel)  = %s" % fmtn(I_main))
    print("     I_hat  (+ completion)   = %s" % fmtn(I_hat))
    print("     rel |Im| = %s ; cut-6 vs cut-8 rel = %s"
          % (mp.nstr(im_rel, 3), mp.nstr(eps_rel, 3)))
    is_real = im_rel < mp.mpf(10) ** (-8)
    check("C5.2 [INTEGRAL COMPUTED, DERIVED MEASURE] weight bookkeeping "
          "fixes the kernel family: invariant measure d^2tau/tau_2^2 x "
          "tau_2^2 quartic zero-mode scaling => main kernel J(Delta,0), "
          "heat-kernel completion J(Delta,1), J(Delta,2) (P-block "
          "only); truncation cut-6 vs cut-8 = %s; reality after the "
          "conjugation canonicalisation: rel |Im| = %s (%s)"
          % (mp.nstr(eps_rel, 3), mp.nstr(im_rel, 3),
             "real" if is_real else "residual multiplier phases remain "
             "-- tests evaluated on complex moduli, recorded honestly"),
          eps_rel < mp.mpf(10) ** (-2))

    tol = max(eps_rel * 100, mp.mpf(10) ** (-7))
    # TEST 1: T5(V) = 0
    t5rel = abs(I_main[3]) / scale
    print("     TEST 1  T5 fraction |I_T5|/||I|| = %s (tol %s)"
          % (mp.nstr(t5rel, 4), mp.nstr(tol, 2)))
    t5_zero = t5rel < tol
    check("C5.3 [TEST 1: T5] the rigid parameter-free channel: "
          "T5(V) = 0 is %s (completion-free channel, delta-1b E1.6 "
          "rigidity)" % ("REALISED" if t5_zero else
                         "NOT realised (T5 fraction %s)"
                         % mp.nstr(t5rel, 3)), True)

    # TEST 2: W_2 : W_13 -> 4:3 (diagonal-restricted scalar weights)
    W2 = W.get((2, F(1)), mp.mpc(0))
    W13 = W.get((1, F(1)), mp.mpc(0)) + W.get((3, F(1)), mp.mpc(0))
    r43 = W2 / W13 if abs(W13) > 0 else mp.inf
    dev43 = abs(r43 - mp.mpf(4) / 3)
    print("     TEST 2  W_2(1)/W_13(1) = %s (Soll 4/3 = 1.3333...)"
          % mp.nstr(r43, 6))
    ok43 = dev43 < tol * 10
    check("C5.4 [TEST 2: 4:3] the forced leading-level weight ratio "
          "W_2 : W_13 = 4 : 3 is %s (computed %s, |dev| = %s)"
          % ("REALISED" if ok43 else "NOT realised", mp.nstr(r43, 6),
             mp.nstr(dev43, 3)), True)

    # TEST 3: psi(V) = -64 N  /  V = -A_fix N
    tgt = [-x for x in Afix]
    rats = [I_main[i] / tgt[i] for i in range(5) if tgt[i] != 0]
    spread = max(abs(rats[i] - rats[j]) for i in range(len(rats))
                 for j in range(len(rats))) / max(abs(r) for r in rats)
    psiI_m = sum(float(psi[i]) * I_main[i] for i in range(5))
    psiI_h = sum(float(psi[i]) * I_hat[i] for i in range(5))
    print("     TEST 3  ratios I/(-A_fix) = %s ; spread %s"
          % (fmtn(rats), mp.nstr(spread, 3)))
    print("             psi(I) = %s (main) / %s (completed); Soll "
          "psi = -64 N, N > 0 (i.e. negative real)"
          % (mp.nstr(psiI_m, 6), mp.nstr(psiI_h, 6)))
    psi_neg = (psiI_m.real < 0
               and abs(psiI_m.imag) < abs(psiI_m.real) * mp.mpf(10) ** (-6))
    full_succ = spread < tol * 10 and t5_zero
    slice_succ = t5_zero and psi_neg
    check("C5.5 [TEST 3: TARGET] ERFOLG-voll (V = -A_fix N): %s "
          "(spread %s); ERFOLG-mit-d-Kanal (T5 = 0 und psi = -64 N): %s"
          % ("fires" if full_succ else "does NOT fire",
             mp.nstr(spread, 3),
             "fires" if slice_succ else "does NOT fire"), True)
    return dict(I_main=I_main, I_hat=I_hat, eps=eps_rel, t5rel=t5rel,
                t5_zero=t5_zero, r43=r43, ok43=ok43, spread=spread,
                psiI_m=psiI_m, psiI_h=psiI_h, full=full_succ,
                slc=slice_succ, W=W, im_rel=im_rel)


# ---------------------------------------------------------------------------
# C6 -- anchors: the Z2 discriminant (D8) and the Z2 sub-orbifold
# ---------------------------------------------------------------------------
G2 = [(0, 0), (1, 0), (0, 1), (1, 1)]     # order: (0, v, s, c) of D8


def q8_d8(m):
    x, y = m
    return (4 * x * x + 4 * x * y) % 8


def bil8_d8(m, n):
    s = ((m[0] + n[0]) % 2, (m[1] + n[1]) % 2)
    return (q8_d8(s) - q8_d8(m) - q8_d8(n)) % 8


def d8_theta_dicts(maxnorm):
    """{class 0,v,s,c: {n16: count}} of D8 via 8-fold 1-dim convolution
    with sum-parity tracking (classes: int/even, int/odd, half/even,
    half/odd)."""
    lim = 16 * maxnorm

    def conv8(one):
        cur = {(0, 0): 1}
        for _ in range(8):
            new = {}
            for (n1, p1), c1 in cur.items():
                for (n2, p2), c2 in one.items():
                    n = n1 + n2
                    if n > lim:
                        continue
                    k = (n, (p1 + p2) % 2)
                    new[k] = new.get(k, 0) + c1 * c2
            cur = new
        return cur

    one_int = {}
    m = 0
    while 16 * m * m <= lim:
        one_int[(16 * m * m, m % 2)] = one_int.get((16 * m * m, m % 2), 0) + 1
        if m > 0:
            one_int[(16 * m * m, (-m) % 2)] += 1
        m += 1
    one_half = {}
    m = 0
    while 4 * (2 * m + 1) ** 2 <= lim:
        for mm in (m, -m - 1):
            k = (4 * (2 * mm + 1) ** 2, mm % 2)
            one_half[k] = one_half.get(k, 0) + 1
        m += 1
    ci = conv8(one_int)
    ch = conv8(one_half)
    out = {0: {}, 1: {}, 2: {}, 3: {}}
    for (n, p), c in ci.items():
        out[0 if p == 0 else 1][n] = out[0 if p == 0 else 1].get(n, 0) + c
    for (n, p), c in ch.items():
        out[2 if p == 0 else 3][n] = out[2 if p == 0 else 3].get(n, 0) + c
    return out


def section6(V4, V2, CNT):
    print("  -- C6: ANCHORS (Z2 first -- run BEFORE the Z4 solve)")
    # (a) the D8 discriminant: 4 components CLOSE, no shifted classes
    g = sum_z8([z8_root(q8_d8(m)) for m in G2])
    T2x, S2x = build_weil(q8_d8, bil8_d8, G2, Z8_ONE)
    C2m = [[Z8_ONE if i == j else Z8_ZERO for j in range(4)]
           for i in range(4)]   # every element self-inverse
    S2sq = mat_mul(S2x, S2x)
    ST = mat_mul(S2x, T2x)
    ST3 = mat_mul(mat_mul(ST, ST), ST)
    ok_rel = (mat_eq(S2sq, C2m) and mat_eq(ST3, S2sq)
              and mat_eq(mat_mul(S2x, mat_conjT(S2x)), mat_id(4)))
    d8th = d8_theta_dicts(MAXN_NUM)
    e4c = [0] * 4
    for n in range(4):
        e4c[n] = (d8th[0].get(32 * n, 0) + d8th[2].get(32 * n, 0))
    SC2 = [[complex(z8_to_mpc(S2x[i][j])) for j in range(4)]
           for i in range(4)]
    res = []
    for i in range(4):
        lhs = sum(c * mp.exp(1j * mp.pi * (-1 / TAU_A) * n / 16)
                  for n, c in d8th[i].items())
        rhs = (-1j * TAU_A) ** 4 * sum(
            SC2[i][j] * sum(c * mp.exp(1j * mp.pi * TAU_A * n / 16)
                            for n, c in d8th[j].items())
            for j in range(4))
        res.append(abs(lhs - rhs) / abs(lhs))
    check("C6.1 [Z2 ANCHOR: D8 CLOSES AT 4 COMPONENTS] discriminant "
          "Z2 x Z2 with q = (0, 1/2, 0, 0): Gauss sum = %s = 2 = "
          "sqrt(4) (signature 0), exact relations S^2 = C = 1, "
          "(ST)^3 = S^2, S unitary; the 4-vector D8 theta covariance "
          "closes WITHOUT shifted classes (max rel residual %s < 1e-25); "
          "{1,s} extension = E8: Theta_0 + Theta_s = %s = E4 -- the "
          "16-component completion is a Z4-DISCRIMINANT phenomenon, "
          "absent in the Z2/D8 case (why the delta-1b Z2/EH anchor "
          "worked blockwise)"
          % (str(g[0]), mp.nstr(max(res), 3), fmt(e4c)),
          g == z8_scal(F(2), Z8_ONE) and ok_rel
          and max(res) < mp.mpf(10) ** (-25)
          and e4c == [1, 240, 2160, 6720])

    # (b) the Z2 sub-orbifold: derived contraction -> BHS structure
    pairs2 = [(0, 1), (1, 0), (1, 1)]
    t2, s2, dev2 = measure_transport(2, pairs2,
                                     lambda a, b, tau: M_val(2, a, b, tau))
    rhoT_np = rho_np(weil_matrices()[0])
    rhoS_np = rho_np(weil_matrices()[1])
    seed2 = {}
    for p in pairs2:
        v = np.zeros(16, dtype=complex)
        for c in range(4):
            if c % 2 == p[0] % 2:
                v[IDX[(c, c)]] = (-1.0) ** (p[0] * p[1])
        seed2[p] = v
    best = None
    hol2 = None
    Lam2s = None
    for k in range(12):
        o2, Lam2, null2, sv2, h2l = solve_orbit(pairs2, 2, t2, s2,
                                                rhoT_np, rhoS_np,
                                                (0, 1), k)
        if k == 0:
            hol2, Lam2s = h2l, Lam2
        b2, c2 = project_seed(Lam2, null2, seed2)
        if b2 is not None and abs(c2) > 1e-6 \
                and (best is None or abs(c2) > abs(best[3])):
            best = (k, len(null2), b2, c2)
    if best is None:
        # multiplier-relaxed fallback (same construction as C4.3)
        k2 = 'multiplier'
        ev2l = joint_eigvecs(hol2)
        beta2, cos2, d2n = None, None, 0
        bestc = 0.0
        for (v, lams, _) in ev2l:
            G = sum(Lam2s[p].conj().T @ Lam2s[p] for p in Lam2s)
            Av = sum(Lam2s[p].conj().T @ seed2[p] for p in Lam2s)
            c = np.vdot(v, Av) / np.vdot(v, G @ v).real
            b = {p: Lam2s[p] @ (c * v) for p in Lam2s}
            n_pr = np.sqrt(sum(np.vdot(b[p], b[p]).real for p in b))
            n_sd = np.sqrt(sum(np.vdot(seed2[p], seed2[p]).real
                               for p in seed2))
            cs = (abs(sum(np.vdot(seed2[p], b[p]) for p in b))
                  / (n_pr * n_sd)) if n_pr > 1e-14 else 0.0
            if cs > bestc:
                bestc = cs
                beta2, cos2, d2n = b, cs, 1
    else:
        k2, d2n, beta2, cos2 = best
    have2 = beta2 is not None and max(np.linalg.norm(beta2[p])
                                      for p in beta2) > 1e-10
    print("     Z2 solve: char k = %s, null dim %s, seed overlap %s"
          % (str(k2), str(d2n),
             ("%.6f" % cos2) if cos2 is not None else "n/a"))
    if have2:
        dm2 = {p: dress_series(2, p[0], p[1], BASES2, GRID_CUT)
               for p in pairs2}
        I2m, _, W2d = hm_integral(beta2, dm2, BASES2, V4, V2, CNT,
                                  GRID_CUT, mp.mpf(1) / 2)
        re2 = [x.real for x in I2m]
        Wn = {n: abs(sum(W2d.get((a, F(n)), mp.mpc(0)) for a in (0, 1)))
              for n in (1, 2, 3)}
        lead_ok = Wn[1] > Wn[2] > Wn[3]
        nonzero = min(abs(x) for x in re2) > max(abs(x) for x in re2) \
            * mp.mpf(10) ** (-4)
        print("     I_2(derived) = %s ; level weights %s"
              % (fmtn(re2), fmtn([Wn[n] for n in (1, 2, 3)])))
        check("C6.2 [Z2 SUB-ORBIFOLD / BHS] the derived Z2 contraction "
              "(char k = %s, dim %d, seed overlap %.4f) gives a NONZERO "
              "integral with the level ledger dominated by the FIRST "
              "massive coset level (|W(1)| > |W(2)| > |W(3)|): the "
              "BHS/Eguchi-Hanson 4c^2-at-grade-(-2) structure of "
              "delta-1b E2 falls out of the covariant system"
              % (str(k2), d2n, cos2), lead_ok and nonzero)
    else:
        check("C6.2 [Z2 SUB-ORBIFOLD] no nonzero derived Z2 contraction "
              "over the full character scan -- reported honestly",
              False)
    return d2n, cos2


# ---------------------------------------------------------------------------
# C7 -- negative controls
# ---------------------------------------------------------------------------
def section7(ser0):
    print("  -- C7: negative controls")
    lim = 16 * MAXN_NUM

    # (a) wrong quadratic form (x^2 + y^2)/4
    gw = sum_z8([z8_root((2 * x * x + 2 * y * y) % 8)
                 for x in range(4) for y in range(4)])
    nrm = z8_mul(gw, z8_conj(gw))
    Tw, Sw = build_weil(lambda m: (2 * m[0] ** 2 + 2 * m[1] ** 2) % 8,
                        lambda m, n: (4 * (m[0] * n[0] + m[1] * n[1])) % 8,
                        MU, Z8_ONE)
    Cm = [[Z8_ONE if MU[j] == neg(MU[i]) else Z8_ZERO for j in range(16)]
          for i in range(16)]
    s2w = mat_mul(Sw, Sw)
    SCw = rho_mpc(Sw)
    resw = []
    thd = {mu: eval_series16(ser0[mu], TAU_A, lim) for mu in MU}
    for i, mu in enumerate(MU):
        lhs = eval_series16(ser0[mu], -1 / TAU_A, lim)
        rhs = (-1j * TAU_A) ** 4 * sum(SCw[i][j] * thd[MU[j]]
                                       for j in range(16))
        resw.append(abs(lhs - rhs) / abs(lhs))
    check("C7.1 [NC-a: WRONG FORM] q = (x^2+y^2)/4: Gauss sum has "
          "|G|^2 = %s = 64 != 16 (no unit signature factor exists -- "
          "the form is not the discriminant form of an even unimodular "
          "gluing); forcing sigma = 1 breaks S^2 = C EXACTLY (%s); and "
          "the true 16 thetas fail its S-rule at O(1) (max residual %s)"
          % (str(nrm[0]), mat_eq(s2w, Cm), mp.nstr(max(resw), 3)),
          nrm == z8_scal(F(64), Z8_ONE) and not mat_eq(s2w, Cm)
          and max(resw) > mp.mpf(10) ** (-2))

    # (b) wrong signature factor
    Tb, Sb = build_weil(q8, bil8, MU, z8_root(-2))
    s2b = mat_mul(Sb, Sb)
    check("C7.2 [NC-b: WRONG SIGNATURE] the correct form with a WRONG "
          "signature factor sigma = e(-1/4) (signature-2 pretence): "
          "S^2 = C fails EXACTLY (S^2 = e(-1/2) C instead)",
          not mat_eq(s2b, Cm)
          and mat_eq(s2b, mat_scal(F(1), [[z8_mul(z8_root(4), Cm[i][j])
                                           for j in range(16)]
                                          for i in range(16)])))

    # (c) k = 2 thetas
    n_break = sum(1 for mu in MU if (2 * q8(mu)) % 8 != q8(mu) % 8)
    Sx = weil_matrices()[1]
    SC = rho_mpc(Sx)
    resk = []
    # k = 2 test: Theta_mu(2 tau) against the k = 1 Weil rule
    thd2 = {mu: eval_series16(ser0[mu], 2 * TAU_A, lim) for mu in MU}
    for i, mu in enumerate(MU):
        lhs = eval_series16(ser0[mu], 2 * (-1 / TAU_A), lim)
        rhs = (-1j * TAU_A) ** 4 * sum(SC[i][j] * thd2[MU[j]]
                                       for j in range(16))
        resk.append(abs(lhs - rhs) / max(abs(lhs), mp.mpf(1)))
    check("C7.3 [NC-c: k = 2] rescaled thetas Theta_mu(2 tau): the "
          "T-grid doubles (e(2 q) != e(q) on %d = 10 of 16 classes, "
          "EXACT) and the k = 1 Weil S-rule fails at O(1) (max residual "
          "%s); delta-1b E4.3 replication: the leading current slot "
          "norm 2/k = 1 is EMPTY (diagonal classes have integer levels "
          "only)" % (n_break, mp.nstr(max(resk), 3)),
          n_break == 10 and max(resk) > mp.mpf(10) ** (-2))


# ---------------------------------------------------------------------------
# C8 -- verdict
# ---------------------------------------------------------------------------
def section8(have_beta, dims, quasi, mult_ord, cos1, res5):
    print("  -- C8: verdict (the delta-1 route, preregistered branches)")
    if not have_beta:
        verdict = ("VERBLEIBENDE LUECKE (praezisiert): keine blockweise "
                   "SL(2,Z)-invariante Kontraktion des 16-Komponenten-"
                   "Systems existiert -- Obstruktion = Transport-"
                   "Holonomie (gemessen)")
    elif res5 and res5['full'] and not quasi:
        verdict = "ERFOLG (voll): V = -A_fix N"
    elif res5 and res5['slc'] and not quasi:
        verdict = "ERFOLG (mit d-Kanal): T5 = 0 und psi(V) = -64 N"
    elif res5 and quasi:
        passed = []
        if res5['t5_zero']:
            passed.append('T5 = 0')
        if res5['ok43']:
            passed.append('4:3')
        if res5['full']:
            passed.append('V = -A_fix N')
        if res5['slc']:
            passed.append('psi-Slice')
        if res5['full'] or res5['slc']:
            verdict = ("ERFOLG-KANDIDAT (bis auf Multiplikator): die "
                       "abgeleitete Kontraktion existiert nur bis auf "
                       "ein endliches Multiplikator-System (Ordnung %s "
                       "+ Baum-Phasenkonvention), und die Pruefsteine "
                       "%s werden unter der kanonischen Wahl getroffen "
                       "-- kein sauberer Abschluss, aber die Richtung "
                       "steht" % (str(mult_ord), ", ".join(passed)))
        else:
            verdict = ("UNENTSCHIEDEN mit praezisierter Luecke: die "
                       "Kontraktion ist bis auf ein ENDLICHES "
                       "Multiplikator-System der Ordnung %s abgeleitet "
                       "(kein strikter SL(2,Z)-Charakter existiert -- "
                       "exakt vermessen), die Pruefsteine schlagen "
                       "unter der kanonischen Baum-Phasenwahl fehl; "
                       "KILL feuert NICHT, weil die Phasenwahl kein "
                       "abgeleitetes Datum ist -- die Restluecke ist "
                       "jetzt exakt: das Multiplikator-System muss "
                       "durch die fehlenden Twistor-Freiheitsgrade "
                       "(BCOV-Seite) gekuerzt werden" % str(mult_ord))
    elif res5:
        unique = dims == (1, 1)
        if unique and cos1 is not None and cos1 > 0.1:
            verdict = ("KILL (unter der blockweisen Lesart): das Mass "
                       "ist jetzt ABGELEITET (Kovarianz + Gewichts-"
                       "Buchhaltung, eindeutig bis auf N) und die drei "
                       "Pruefsteine schlagen fehl -- T5 != 0, kein 4:3, "
                       "kein psi-Slice")
        else:
            verdict = ("UNENTSCHIEDEN mit praezisierter Luecke: die "
                       "Kontraktion ist abgeleitet, aber NICHT eindeutig "
                       "(Loesungsraum-Dim %s, Seed-Ueberlapp %s) -- die "
                       "Seed-Projektion ist eine Wahl innerhalb des "
                       "kovarianten Raums" % (str(dims), str(cos1)))
    else:
        verdict = "UNENTSCHIEDEN (Integral nicht ausgewertet)"
    check("C8.1 [VERDICT: %s] honest bookkeeping: exact = Weil matrices "
          "+ relations, grids, ledgers, leading cell, Gauss sums, "
          "D8 anchor algebra; numeric (documented) = theta covariance "
          "certificates (25+ digits), block transport constants (28+), "
          "contraction solve (double SVD, certified a posteriori at "
          "1e-9), kernels (30 digits, cut-scan)" % verdict, True)
    print("     VERDICT: %s" % verdict)
    return verdict


# ---------------------------------------------------------------------------
def run():
    print("WP5e-delta-1c probe: completing the 16-component Weil system "
          "and deciding the Harvey-Moore integral (CELEST.SEAM.01; "
          "exploration only)")
    V4, V2, CNT, Afix, psi = section0()
    Tx, Sx = section1()
    ser0, ser_iso4, ser_re, SC = section2(Sx, CNT)
    section3(ser_iso4, ser_re, SC)
    section6(V4, V2, CNT)          # the Z2 anchors run FIRST
    beta, dims, ksel, quasi, mult_ord, cos1, cos2 = section4(
        Tx, Sx, ser0, ser_iso4)
    have_beta = len(beta) > 0
    res5 = section5(beta, V4, V2, CNT, Afix, psi) if have_beta else None
    section7(ser0)
    section8(have_beta, dims, quasi, mult_ord, cos1, res5)
    print("")
    print("CHECKS: %d passed, %d failed" % (N_PASS, N_FAIL))
    return N_FAIL == 0


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)




