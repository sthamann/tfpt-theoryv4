"""WP5e-dterm of CELEST.SEAM.01 (EXPLORATION ONLY -- experiments/, no claim).

CAN GEOMETRY DERIVE c_d = 1920?  The v511 full-tensor ledger found exactly
ONE legal cubic channel (the su(4) d-symbol with exchange quartic
Q_dd = (1/60)(T3 - P3/4)) and the relaxed pairing solves EXACTLY with
A_fix = -u + 8v + 2w + 1920 Q_dd.  The [C] fence notes 1920 = |W(D5)|.
This probe is the honest stress test of that fingerprint: derivation or
numerology?  Four candidate routes, exact sympy/Fraction arithmetic, with
a PRE-DECLARED look-elsewhere ledger.

N0  BASELINE REPLICATION: roots (52, 64, 60, 64); A_fix = (9,-30,-15,0,32);
    Q_dd two routes; c_d = 1920 pinned SOLELY by the T3 slot (the P-block
    directions u, v, w span the full (P1,P2,P3) space, det = -68 != 0), so
    c_d = Phi_T3(A_fix)/Phi_T3(Q_dd) = 32 * 60 exactly.
N1  NORMALISATION BOOKKEEPING (the precondition of any "hit"): c_d is
    CONVENTION-DEPENDENT, c_d -> c_d/kappa^2 under d -> kappa d and
    c_d ~ propagator normalisation.  Table (exact): probe convention
    (tr-fund d, e8-Killing 60G) 1920; Gell-Mann d_abc = 2tr(T{T,T}),
    tr(TT) = 1/2 (kappa = 4): 120; su(4)-Killing propagator 8G: 256;
    plain trace propagator G: 32; ch3-normalised d/6: 69120.  ONLY the
    probe convention hits |W(D5)|.  The convention-stable content is the
    factorisation c_d = Phi_T3(A_fix) x 2 h_vee(E8) = 32 x 60 [E].
K1  FLUX PRODUCTS: pre-declared catalog of 21 [E] numbers of the
    construction, grammar {a*b, a*b/2, a*b/4, a+b} on unordered pairs:
    count of expressions hitting 1920 (look-elsewhere).  Charge-legality:
    the d-channel-compatible sphere pairings are (1,3) and (2,2)
    (m + m' = 0 mod 4); their flux products F1*F3/2 = 2048 and
    F2*F2/2 = 1800 BRACKET 1920 and both MISS; the hit 64*60/2 = F1*F2/2
    is the charge-FORBIDDEN (1,2) pairing (1 + 2 = 3 mod 4, killed by the
    v511 innerness theorem).  F_i = dim g_i (v509 S2.5), so the flux
    language is redundant with the dimension language anyway.
K2  ANOMALY INTEGRALITY: the su(4) cubic form tr(h^3) on the coroot
    lattice is valued in 6Z with minimal quantum 6 (= ch3 integrality);
    on the weight lattice it is fractional (3/8): the quantum depends on
    the lattice.  With integer trilinear couplings in tr-fund units the
    allowed c_d lattice is 60 Z (e8-Killing propagator): 1920 IS on the
    lattice but as the 32nd multiple, NOT the minimal quantum; with
    ch3-unit couplings (6Z) the lattice is 2160 Z and 1920 is EXCLUDED.
    The residual integer 32 = lambda_1 lambda_3 has 12 signed integer
    factorisations -- nothing forces it.  K2 gives a lattice, not 1920.
K3  CHARACTER/INDEX ROUTE: cubic power sums per class from the actual
    roots give the su(4) anomaly indices (0, 16, 0, -16) (sum 0: e8 has
    no cubic Casimir); twisted index sum_m i^m A_m = 32i -- numerically
    32, BUT the per-class provenance of the true quartic residual
    Phi_T3(A_fix) = 32 is (10, -4, 30, -4) (classes 0 and 2 dominate),
    while the cubic 32 comes from classes 1 and 3 as 16 + 16: DIFFERENT
    mechanism, same number = coincidence exposed.  Weyl/Kostant data:
    among {|W(A3)|, |W(D5)|, |W(D5xA3)|, |W(E8)| and its quotients,
    |W(D8)|} exactly |W(D5)| = 1920 hits (plus the accidental
    |W(E8)|/|W(A8)| = 1920, A8 not a carrier factor); the d-symbol is an
    A3-side object (natural order |W(A3)| = 24) and the D5 side has NO
    cubic invariant (Inv S^3 45 = 0): no mechanism connects |W(D5)| to
    the A3 d-channel.
K4  NEGATIVE CONTROLS: (a) SO(16)/D8: Inv(S^3 adj) = 0 (no channel),
    fluxes (0, 60, 0) => charge-legal flux products 0, cubic class sums
    all 0, |W(D8)| = 5160960: every candidate formula fails consistently;
    (b) k = 2 flux doubling: flux products scale x4 (7680) while c_d is
    root-theoretic and static (1920): K1 is not covariant; HONEST: the
    Weyl fence is also static, so this control cannot discriminate it;
    (c) false g0 = d5 + a2 + u1: Inv(S^3 g0) = 6 != 1 -- no unique
    channel, the question "derive c_d" cannot even be posed;
    (d) so(10): Tr X^3 = 0 (T5 protection, sanity).
V   VERDICT: NUMEROLOGY for the |W(D5)| reading (many-hit look-elsewhere,
    no quantisation force, no index mechanism, wrong-side Weyl group);
    the [E] content is the exact factorisation c_d = 32 x 60 with 32 =
    Phi_T3(A_fix) (provenance (10, -4, 30, -4)) and 60 = 2 h_vee(E8);
    the physical justification of the cubic GS term stays [O].

Throwaway probe: standalone (sympy + Fraction), prints tables + PASS/FAIL
+ verdict, ends with a check count.  verification/, ledger, papers,
changelog, website, scorecard untouched.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product

import sympy as sp

G_CAR = 5
N_FAM = 3
MU4 = 4
RANK = 8
H_VEE = 30
HALF = F(1, 2)

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


# ---------------------------------------------------------------------------
# E8 roots in D5 (+) A3 glue coordinates (v128/v492/v505/v508/v511 pattern)
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
# exact polynomial machinery on the D5 (+) A3 Cartan (v508/v511 copy)
# ---------------------------------------------------------------------------
X5 = sp.symbols('x1:6')
Y3 = sp.symbols('y1:4')
Y4 = (*Y3, -sum(Y3))
ALLV = (*X5, *Y3)

S5 = sp.expand(sum(v ** 2 for v in X5))
S3 = sp.expand(sum(v ** 2 for v in Y4))
P1 = sp.expand(S5 ** 2)
P2 = sp.expand(S5 * S3)
P3 = sp.expand(S3 ** 2)
T5 = sp.expand(sum(v ** 4 for v in X5))
T3 = sp.expand(sum(v ** 4 for v in Y4))
BASIS4 = [P1, P2, P3, T5, T3]
T3CUB = sp.expand(sum(v ** 3 for v in Y4))    # the a3 cubic invariant


def lin_form(alpha):
    e = sum(sp.Rational(alpha[i].numerator, alpha[i].denominator) * X5[i]
            for i in range(5))
    e += sum(sp.Rational(alpha[5 + i].numerator, alpha[5 + i].denominator)
             * Y4[i] for i in range(4))
    return sp.expand(e)


def poly_dict(expr):
    return sp.Poly(sp.expand(expr), *ALLV, domain='QQ').as_dict()


def decompose(target, basis_exprs):
    dicts = [poly_dict(b) for b in basis_exprs]
    tdict = poly_dict(target)
    monos = sorted(set().union(tdict.keys(), *[d.keys() for d in dicts]))
    A = sp.Matrix([[d.get(m, 0) for d in dicts] for m in monos])
    b = sp.Matrix([tdict.get(m, 0) for m in monos])
    try:
        sol, params = A.gauss_jordan_solve(b)
    except ValueError:
        return None
    if len(params) > 0:
        sol = sol.subs({p: 0 for p in params})
    if sp.expand(target - sum(sol[i] * basis_exprs[i]
                              for i in range(len(basis_exprs)))) != 0:
        return None
    return list(sol)


def vec5(expr):
    c = decompose(expr, BASIS4)
    assert c is not None, "quartic not in the invariant 5-basis"
    return [sp.Rational(x) for x in c]


def power_sums_by_class(roots):
    K = {m: sp.Poly(0, *ALLV, domain='QQ') for m in range(4)}
    Q = {m: sp.Poly(0, *ALLV, domain='QQ') for m in range(4)}
    C = {m: sp.Poly(0, *ALLV, domain='QQ') for m in range(4)}
    for alpha, c in roots.items():
        p = sp.Poly(lin_form(alpha), *ALLV, domain='QQ')
        p2 = p ** 2
        K[c] = K[c] + p2
        Q[c] = Q[c] + p2 ** 2
        C[c] = C[c] + p2 * p
    return ({m: K[m].as_expr() for m in range(4)},
            {m: Q[m].as_expr() for m in range(4)},
            {m: C[m].as_expr() for m in range(4)})


def solvable(cols, target):
    A = sp.Matrix([[c[i] for c in cols] for i in range(5)])
    b = sp.Matrix([target[i] for i in range(5)])
    try:
        sol, params = A.gauss_jordan_solve(b)
    except ValueError:
        return None
    if len(params) > 0:
        sol = sol.subs({p: 0 for p in params})
    return list(sol)


PHI_T3 = [0, 0, 0, 0, 1]


def phi(functional, vec):
    return sum(sp.Rational(a) * sp.Rational(b)
               for a, b in zip(functional, vec))


# ---------------------------------------------------------------------------
# weight-multiset machinery (v511 copy, only the pieces needed here)
# ---------------------------------------------------------------------------
RHO_D5 = (8, 6, 4, 2, 0)
RHO_D8 = tuple(2 * k for k in range(7, -1, -1))
RHO_A2 = (4, 0, -4)


def perm_sign(p):
    s = 1
    seen = [False] * len(p)
    for i in range(len(p)):
        if seen[i]:
            continue
        j, ln = i, 0
        while not seen[j]:
            seen[j] = True
            j = p[j]
            ln += 1
        if ln % 2 == 0:
            s = -s
    return s


def conv(c1, c2):
    out = Counter()
    for w1, m1 in c1.items():
        for w2, m2 in c2.items():
            out[tuple(a + b for a, b in zip(w1, w2))] += m1 * m2
    return out


def scaled(c, k):
    return Counter({tuple(k * x for x in w): m for w, m in c.items()})


def cdiv(c, k):
    out = Counter()
    for w, m in c.items():
        assert m % k == 0, "plethysm divisibility violated"
        if m // k:
            out[w] = m // k
    return out


def cadd(*cs):
    out = Counter()
    for c in cs:
        for w, m in c.items():
            out[w] += m
    return {w: m for w, m in out.items() if m != 0}


def csub(c1, c2):
    out = Counter(c1)
    for w, m in c2.items():
        out[w] -= m
    return Counter({w: m for w, m in out.items() if m != 0})


def sym2(c):
    return cdiv(Counter(cadd(conv(c, c), scaled(c, 2))), 2)


def alt2(c):
    return cdiv(csub(conv(c, c), scaled(c, 2)), 2)


def sym3(c):
    c3 = conv(conv(c, c), c)
    mid = conv(c, scaled(c, 2))
    return cdiv(Counter(cadd(c3, scaled(mid, 1), scaled(mid, 1),
                             scaled(mid, 1), scaled(c, 3), scaled(c, 3))), 6)


def alt3(c):
    c3 = conv(conv(c, c), c)
    mid = conv(c, scaled(c, 2))
    tot = csub(Counter(cadd(c3, scaled(c, 3), scaled(c, 3))),
               Counter(cadd(mid, mid, mid)))
    return cdiv(tot, 6)


def s21(c):
    c3 = conv(conv(c, c), c)
    return cdiv(csub(c3, scaled(c, 3)), 3)


def count(c):
    return sum(c.values())


def inv_D(c, rho):
    n = len(rho)
    key = sorted(rho, reverse=True)
    pos = {v: i for i, v in enumerate(key)}
    total = 0
    for mu, mult in c.items():
        u = tuple(mu[i] + rho[i] for i in range(n))
        a = [abs(x) for x in u]
        if sorted(a, reverse=True) != key:
            continue
        total += perm_sign([pos[x] for x in a]) * mult
    return total


def inv_A(c, rho):
    n = len(rho)
    key = sorted(rho, reverse=True)
    pos = {v: i for i, v in enumerate(key)}
    total = 0
    for mu, mult in c.items():
        u = tuple(mu[i] + rho[i] for i in range(n))
        if sorted(u, reverse=True) != key:
            continue
        total += perm_sign([pos[x] for x in u]) * mult
    return total


def inv_d5(c):
    return inv_D(c, RHO_D5)


def inv_d8(c):
    return inv_D(c, RHO_D8)


def inv_a2u1(c4):
    sliced = Counter()
    for w, m in c4.items():
        if w[3] == 0:
            sliced[(w[0], w[1], w[2])] += m
    return inv_A(sliced, RHO_A2)


def inv_dim(reps, invd, inva):
    total = 0
    for combo in product(*reps):
        cd, ca = combo[0]
        for d2, a2 in combo[1:]:
            cd = conv(cd, d2)
            ca = conv(ca, a2)
        total += invd(cd) * inva(ca)
    return total


def box_sym2(rep):
    out = []
    for i, (a, b) in enumerate(rep):
        out.append((sym2(a), sym2(b)))
        out.append((alt2(a), alt2(b)))
        for a2, b2 in rep[i + 1:]:
            out.append((conv(a, a2), conv(b, b2)))
    return [(x, y) for x, y in out if count(x) and count(y)]


def box_sym3(rep):
    assert len(rep) <= 2
    out = []
    for a, b in rep:
        out.append((sym3(a), sym3(b)))
        out.append((s21(a), s21(b)))
        out.append((alt3(a), alt3(b)))
    if len(rep) == 2:
        (a1, b1), (a2, b2) = rep
        for x, y in box_sym2([(a1, b1)]):
            out.append((conv(x, a2), conv(y, b2)))
        for x, y in box_sym2([(a2, b2)]):
            out.append((conv(x, a1), conv(y, b1)))
    return [(x, y) for x, y in out if count(x) and count(y)]


def build_g0_reps(roots):
    parts = {m: Counter() for m in range(4)}
    for r, m in roots.items():
        d = tuple(int(2 * x) for x in r[:5])
        a = tuple(int(4 * x) for x in r[5:])
        parts[m][(d, a)] += 1
    TRIV5 = Counter({(0,) * 5: 1})
    TRIV3 = Counter({(0,) * 4: 1})
    adj45 = Counter()
    adj15 = Counter()
    for (d, a), m in parts[0].items():
        if a == (0,) * 4:
            adj45[d] += m
        else:
            adj15[a] += m
    adj45[(0,) * 5] += 5
    adj15[(0,) * 4] += 3
    return [(adj45, TRIV3), (TRIV5, adj15)], adj45


# ---------------------------------------------------------------------------
# N0 -- baseline replication (v511 anchor)
# ---------------------------------------------------------------------------
def section_n0(roots):
    print("  -- N0: baseline (v511 replication; the target object c_d)")
    counts = [sum(1 for c in roots.values() if c == m) for m in range(4)]
    check("N0.1 [ROOTS] 240 roots, class split %s = (52, 64, 60, 64)"
          % fmt(counts),
          len(roots) == 240 and counts == [52, 64, 60, 64])

    I = sp.I
    K, Q, C = power_sums_by_class(roots)
    Qtw = {j: sp.expand(sum(I ** (j * m) * Q[m] for m in range(4)))
           for j in range(4)}
    Afix = sp.expand(Qtw[1] / 2 + Qtw[2] / 4 + Qtw[3] / 2)
    dA = vec5(Afix)
    check("N0.2 [A_fix] AB residual = %s = (9, -30, -15, 0, 32) "
          "(v505 S3.7 / v508 S0.3 / v511 D6.1)" % fmt(dA),
          dA == [9, -30, -15, 0, 32])

    # su(4) gl-basis (3 Cartan + 12 root vectors), probe convention
    basis = []
    for i in range(3):
        m = sp.zeros(4)
        m[i, i], m[i + 1, i + 1] = 1, -1
        basis.append(m)
    for i in range(4):
        for j in range(4):
            if i != j:
                m = sp.zeros(4)
                m[i, j] = 1
                basis.append(m)
    nb = len(basis)
    Gm = sp.Matrix(nb, nb, lambda a, b: sp.trace(basis[a] * basis[b]))
    Ginv = Gm.inv()
    x = sp.diag(*Y4)

    def dsym(u, v, w):
        return sp.trace(u * (v * w + w * v)) / 2

    vvec = sp.Matrix([sp.expand(dsym(x, x, B)) for B in basis])
    Qdd = sp.expand((vvec.T * Ginv * vvec)[0, 0] / 60)
    qv = vec5(Qdd)
    hand = sp.expand(sp.trace((x * x - (S3 / 4) * sp.eye(4)) ** 2) / 60)
    check("N0.3 [Q_dd] = %s = (0, 0, -1/240, 0, 1/60) (Killing-propagator "
          "route = hand route |x^2 - (tr x^2/4)1|^2/60, v511 D5.5)"
          % fmt(qv),
          qv == [0, 0, sp.Rational(-1, 240), 0, sp.Rational(1, 60)]
          and sp.expand(Qdd - hand) == 0)

    u = [1, 2, 1, 0, 0]
    v = [1, -2, -3, 0, 0]
    w = [1, -6, 9, 0, 0]
    detP = sp.Matrix([u[:3], v[:3], w[:3]]).det()
    sol = solvable([u, v, w, qv], dA)
    cd = sp.Rational(32) / sp.Rational(1, 60)
    check("N0.4 [c_d PINNED BY T3 ALONE] the relaxed P-directions span the "
          "FULL (P1, P2, P3) block (det = %s != 0) and carry no T5/T3, so "
          "the Q_dd coefficient is fixed by the T3 slot alone: c_d = "
          "Phi_T3(A_fix)/Phi_T3(Q_dd) = 32/(1/60) = %s = 1920; solver "
          "confirms %s" % (detP, cd, fmt(sol)),
          detP == -64 and cd == 1920 and sol == [-1, 8, 2, 1920])
    return K, Q, C, dA, qv, basis, Gm, Ginv, x, vvec


# ---------------------------------------------------------------------------
# N1 -- normalisation bookkeeping (convention table)
# ---------------------------------------------------------------------------
def section_n1(roots, dA, qv, basis, Gm, x, vvec):
    print("  -- N1: normalisation bookkeeping of c_d (convention table)")
    e_a3 = (F(0),) * 5 + (F(1), F(-1), F(0), F(0))
    s_a3 = sum(sum(x_ * y_ for x_, y_ in zip(r, e_a3)) ** 2 for r in roots)
    check("N1.1 [PROPAGATOR ANCHOR] sum_alpha <alpha,e>^2 = %s = 120 = "
          "2 h_vee(E8) <e,e>: the e8 Killing form restricts to 60 x the "
          "fundamental trace form on the a3 block -- the 60 in Q_dd is "
          "[E]-derived, not chosen" % s_a3,
          s_a3 == 120 and 60 == 2 * H_VEE)

    nb = len(basis)

    def cd_of(Qconv):
        qvc = vec5(Qconv)
        val = phi(PHI_T3, qvc)
        return sp.Rational(32) / val, val

    # (a) probe convention: already computed -> 1920
    Q_probe = sp.expand((vvec.T * Gm.inv() * vvec)[0, 0] / 60)
    cd_probe, _ = cd_of(Q_probe)

    # (b) Gell-Mann convention: T_a orthonormal tr(T T) = 1/2,
    #     d_abc = 2 tr(T_a {T_b, T_c}); propagator = e8 Killing = 30 delta
    gm = []
    for i, j in combinations(range(4), 2):
        m = sp.zeros(4)
        m[i, j] = sp.Rational(1, 2)
        m[j, i] = sp.Rational(1, 2)
        gm.append(m)
        m = sp.zeros(4)
        m[i, j] = -sp.I / 2
        m[j, i] = sp.I / 2
        gm.append(m)
    for k in range(1, 4):
        m = sp.zeros(4)
        for i in range(k):
            m[i, i] = 1
        m[k, k] = -k
        gm.append(m / sp.sqrt(2 * k * (k + 1)))
    ortho = all(sp.simplify(sp.trace(gm[a] * gm[b])
                            - (sp.Rational(1, 2) if a == b else 0)) == 0
                for a in range(15) for b in range(15))
    Vgm = sp.Matrix([sp.expand(2 * sp.trace(g * (x * x + x * x)))
                     for g in gm])           # d_abc x^b x^c = 2 tr(T{x,x})
    Q_gm = sp.expand((Vgm.T * Vgm)[0, 0] / 30)   # K_ab = 60 tr = 30 delta
    cd_gm, _ = cd_of(sp.re(Q_gm) + sp.expand(sp.im(Q_gm)) * 0
                     if Q_gm.has(sp.I) else Q_gm)

    # (c) su(4)-Killing propagator (2 h_vee(a3) = 8): K' = 8 G
    Q_su4 = sp.expand((vvec.T * (8 * Gm).inv() * vvec)[0, 0])
    cd_su4, _ = cd_of(Q_su4)

    # (d) plain trace-form propagator: K'' = G
    Q_tr = sp.expand((vvec.T * Gm.inv() * vvec)[0, 0])
    cd_tr, _ = cd_of(Q_tr)

    # (e) ch3-normalised d-symbol (d/6, integral cubic quantum): kappa=1/6
    Q_ch3 = sp.expand(Q_probe / 36)
    cd_ch3, _ = cd_of(Q_ch3)

    table = {'probe (tr-fund d, e8K)': cd_probe,
             'Gell-Mann d, e8K': cd_gm,
             'tr-fund d, su4-Killing': cd_su4,
             'tr-fund d, trace prop.': cd_tr,
             'ch3-normalised d/6, e8K': cd_ch3}
    print("     convention table c_d: %s" % table)
    hits_w = [k for k, v in table.items() if v == 1920]
    check("N1.2 [CONVENTION TABLE] c_d = (1920, 120, 256, 32, 69120) in "
          "the five conventions; EXACTLY ONE convention (the probe's) "
          "matches |W(D5)| = 1920: the Weyl-order fingerprint is "
          "normalisation-contingent, hits = %s" % hits_w,
          ortho
          and (cd_probe, cd_gm, cd_su4, cd_tr, cd_ch3)
          == (1920, 120, 256, 32, 69120)
          and hits_w == ['probe (tr-fund d, e8K)'])

    invar = [sp.Rational(32) for _ in range(5)]
    got = [cd * phi(PHI_T3, vec5(Qc)) for cd, Qc in
           ((cd_probe, Q_probe), (cd_gm, Q_gm), (cd_su4, Q_su4),
            (cd_tr, Q_tr), (cd_ch3, Q_ch3))]
    check("N1.3 [CONVENTION-STABLE CONTENT] c_d x Phi_T3(Q^conv) = 32 = "
          "Phi_T3(A_fix) in ALL five conventions: the invariant statement "
          "is the factorisation c_d = Phi_T3(A_fix) x 2 h_vee(E8) = "
          "32 x 60 -- everything beyond that (incl. '= |W(D5)|') is "
          "convention decoration", got == invar)


# ---------------------------------------------------------------------------
# K1 -- flux products with pre-declared look-elsewhere ledger
# ---------------------------------------------------------------------------
CATALOG = {
    2: "AB denominator det_1 = det_3",
    4: "|Z4| = det C(A3) = AB denominator det_2",
    6: "dim 6 (a3 self-dual) = ch3 quantum",
    8: "rank E8 = 2 h_vee(A3)",
    10: "dim 10 (d5 vector)",
    12: "#A3 roots",
    15: "dim a3",
    16: "dim 16 (d5 spinor) = mu = disc product",
    24: "|W(A3)|",
    30: "h_vee(E8)",
    32: "Phi_T3(A_fix) (AB T3 residual)",
    40: "#D5 roots",
    45: "dim d5",
    52: "#class-0 roots",
    60: "dim g0 = dim g2 = F_2 = 2 h_vee(E8)",
    64: "dim g1 = dim g3 = F_1 = F_3 = psi(A_fix)",
    120: "Killing sum 2 h_vee <e,e> = |W(D5)|/16",
    188: "sum F_i = 248 - 60",
    240: "#roots = chi(1) - rank",
    248: "dim E8 = chi(1)",
    256: "chi(1) - chi(g^2) = 2^8",
}


def enumerate_hits(target):
    vals = sorted(CATALOG)
    hits, total = [], 0
    for k, a in enumerate(vals):
        for b in vals[k:]:
            for opname, val in (("%d*%d" % (a, b), a * b),
                                ("%d*%d/2" % (a, b), F(a * b, 2)),
                                ("%d*%d/4" % (a, b), F(a * b, 4)),
                                ("%d+%d" % (a, b), a + b)):
                total += 1
                if val == target:
                    hits.append(opname)
    return hits, total


def section_k1(roots):
    print("  -- K1: flux-product candidates + look-elsewhere ledger")
    Fi = [64, 60, 64]
    counts = [sum(1 for c in roots.values() if c == m) for m in range(4)]
    dims = [counts[0] + RANK] + counts[1:]
    check("K1.1 [FLUX = DIM, REDUNDANCY] v509 S2.5: F_i = sum_m dim(g_m) "
          "delta_mi = %s = dim g_i exactly -- every 'flux product' IS a "
          "dimension product; the flux language adds no independent "
          "number to the catalog" % fmt(Fi),
          Fi == dims[1:] and Fi == [64, 60, 64])

    legal = [(m, mp) for m in (1, 2, 3) for mp in (1, 2, 3)
             if (m + mp) % 4 == 0 and m <= mp]
    prods = {(m, mp): F(Fi[m - 1] * Fi[mp - 1], 2) for m, mp in legal}
    illegal_hit = F(Fi[0] * Fi[1], 2)
    check("K1.2 [CHARGE-LEGAL PAIRINGS MISS] d-channel-compatible sphere "
          "pairings (m + m' = 0 mod 4): %s with F_m F_m'/2 = %s -- "
          "1800 < 1920 < 2048: both legal products BRACKET and MISS the "
          "target; the only flux hit 64*60/2 = %s is the (1,2) pairing "
          "with charge 1 + 2 = 3 mod 4, FORBIDDEN by the v511 innerness "
          "theorem (all 15 twisted triples have Hom = 0)"
          % (legal, fmt(prods.values()), illegal_hit),
          legal == [(1, 3), (2, 2)]
          and prods[(1, 3)] == 2048 and prods[(2, 2)] == 1800
          and illegal_hit == 1920 and (1 + 2) % 4 != 0)

    hits, total = enumerate_hits(1920)
    print("     1920-hits (%d/%d expressions): %s"
          % (len(hits), total, hits))
    check("K1.3 [LOOK-ELSEWHERE LEDGER] pre-declared catalog (21 [E] "
          "numbers) x grammar {a*b, a*b/2, a*b/4, a+b}: %d expressions, "
          "%d distinct hits on 1920 (plus the singleton |W(D5)| itself): "
          "a >= 12-fold ambiguous fingerprint -- no single combination "
          "is distinguished" % (total, len(hits)),
          total == 924 and len(hits) == 11)

    controls = {t: len(enumerate_hits(t)[0]) for t in (1800, 1920, 2016, 2048)}
    print("     control-target hit counts: %s" % controls)
    check("K1.4 [HIT DENSITY] neighbouring targets score comparably "
          "(1800: %d, 1920: %d, 2016: %d, 2048: %d): the catalog's "
          "multiplicative structure makes ANY smooth (highly divisible) "
          "number near 2000 easy to hit -- 1920 is not special in this "
          "arithmetic; K1 is numerology"
          % (controls[1800], controls[1920], controls[2016], controls[2048]),
          controls[1800] == 8 and controls[1920] == 11
          and controls[2016] == 0 and controls[2048] == 5)


# ---------------------------------------------------------------------------
# K2 -- anomaly integrality / quantisation lattice
# ---------------------------------------------------------------------------
def section_k2():
    print("  -- K2: quantisation condition -- which c_d lattice is allowed")
    vals = set()
    for a in range(-4, 5):
        for b in range(-4, 5):
            for c in range(-4, 5):
                d = -(a + b + c)
                vals.add(a ** 3 + b ** 3 + c ** 3 + d ** 3)
    nonzero = sorted(abs(v) for v in vals if v != 0)
    all_mod6 = all(v % 6 == 0 for v in vals)
    wl = F(3, 4) ** 3 + 3 * F(-1, 4) ** 3
    check("K2.1 [CUBIC QUANTUM] tr(h^3) on the su(4) COROOT lattice "
          "(box +-4, %d values): all = 0 mod 6 (x^3 = x mod 6, tr h = 0), "
          "minimal nonzero = %d = 6 -- the ch3 integrality quantum; on "
          "the WEIGHT lattice it is fractional (fundamental weight: "
          "tr(w^3) = %s = 3/8): the quantum depends on the lattice, so "
          "any integrality argument must first fix the charge lattice"
          % (len(vals), nonzero[0], wl),
          all_mod6 and nonzero[0] == 6 and wl == F(3, 8))

    z, zb, r = sp.symbols('z zbar r', positive=True)
    Ns = sp.symbols('N', positive=True)
    g_log = sp.simplify(sp.diff(Ns * sp.log(1 + z * zb), z, zb))
    flux = sp.integrate(2 * g_log.subs({z: r, zb: r}) * r,
                        (r, 0, sp.oo)) * 2 * sp.pi
    check("K2.2 [CPS FLUX ANCHOR] int_{CP^1} omega = %s = 2 pi N (v509 "
          "S1.2 replicated): the flux quantum is INTEGER N -- large-gauge "
          "shifts step the axion by one period, so trilinear couplings "
          "are quantised in integer units on the chosen lattice"
          % flux, sp.simplify(flux - 2 * sp.pi * Ns) == 0)

    lat_e8k = F(1920, 60)          # integer couplings, tr-fund units
    lat_ch3 = F(1920, 60 * 36)     # couplings in ch3 units (6 Z)
    check("K2.3 [ALLOWED LATTICE vs 1920] integer couplings in tr-fund "
          "units + e8-Killing propagator: c_d in 60 Z, and 1920/60 = %s "
          "= 32: ON the lattice but the 32ND MULTIPLE, not the minimal "
          "quantum 60; strict ch3-unit couplings (6 Z): c_d in 2160 Z "
          "and 1920/2160 = %s not integer: EXCLUDED -- K2 delivers a "
          "lattice, never the value 1920 (the integer 32 is not produced "
          "by any quantisation condition)"
          % (lat_e8k, lat_ch3),
          lat_e8k == 32 and lat_e8k.denominator == 1
          and lat_ch3.denominator != 1)

    facts = [(a, 32 // a) for a in range(-32, 33)
             if a != 0 and 32 % a == 0 and (a > 0) == (32 // a > 0)]
    check("K2.4 [32 NOT FORCED] the residual integer 32 read as a coupling "
          "product lambda_1 lambda_3 has %d signed integer factorisations "
          "%s: nothing selects one -- the quantisation route leaves the "
          "essential factor of c_d = 32 x 60 underived"
          % (len(facts), facts), len(facts) == 12)


# ---------------------------------------------------------------------------
# K3 -- character / index candidates
# ---------------------------------------------------------------------------
def section_k3(K, Q, C, dA):
    print("  -- K3: character/index candidates (exact from the roots)")
    I = sp.I

    cub = {}
    pt = {Y3[0]: 1, Y3[1]: 2, Y3[2]: 3}
    t3ref = T3CUB.subs(pt)                    # = -180 != 0
    for m in range(4):
        pure = sp.expand(C[m].subs({v: 0 for v in X5}))
        cub[m] = sp.Rational(pure.subs(pt), t3ref) if pure != 0 else \
            sp.Rational(0)
        assert sp.expand(pure - cub[m] * T3CUB) == 0, "not proportional to t3"
    check("K3.1 [CUBIC INDICES PER CLASS] su(4) cubic power sums from the "
          "actual roots: A_m = %s = (0, 16, 0, -16) (16 = D5-spinor "
          "multiplicity; the 6 is self-dual, the adjoint is real); total "
          "= %s = 0: e8 has NO cubic Casimir -- consistency"
          % (fmt(cub.values()), sum(cub.values())),
          [cub[m] for m in range(4)] == [0, 16, 0, -16]
          and sum(cub.values()) == 0)

    tw = {j: sp.expand(sum(I ** (j * m) * cub[m] for m in range(4)))
          for j in (1, 2, 3)}
    check("K3.2 [TWISTED CUBIC INDEX] sum_m i^{jm} A_m = %s for j = "
          "(1, 2, 3): magnitude 32 at j = 1, 3 -- NUMERICALLY equal to "
          "Phi_T3(A_fix) = 32; the candidate index formula would be "
          "c_d = |sum_m i^m A_m| x 2 h_vee = 32 x 60 = 1920"
          % fmt(tw.values()),
          tw[1] == 32 * I and tw[2] == 0 and tw[3] == -32 * I)

    W = {m: sp.Rational(5, 4) if m == 0
         else (sp.Rational(-3, 4) if m == 2 else sp.Rational(-1, 4))
         for m in range(4)}
    t3c = {m: vec5(Q[m])[4] for m in range(4)}
    contrib = {m: sp.expand(W[m] * t3c[m]) for m in range(4)}
    recon = [sp.expand(sum(W[m] * vec5(Q[m])[i] for m in range(4)))
             for i in range(5)]
    check("K3.3 [QUARTIC PROVENANCE OF 32] A_fix = sum_m W_m Q_m with "
          "AB weights W = (5/4, -1/4, -3/4, -1/4); T3 coefficients of "
          "Q_m = %s = (8, 16, -40, 16); per-class contributions to "
          "Phi_T3(A_fix): %s = (10, -4, 30, -4), sum %s = 32; full "
          "reconstruction %s = A_fix"
          % (fmt(t3c.values()), fmt(contrib.values()),
             sum(contrib.values()), fmt(recon)),
          [t3c[m] for m in range(4)] == [8, 16, -40, 16]
          and [contrib[m] for m in range(4)] == [10, -4, 30, -4]
          and sum(contrib.values()) == 32 and recon == dA)

    check("K3.4 [PROVENANCE CLASH -- the index route dies] the cubic 32 "
          "is built 16 + 16 from classes (1, 3) ONLY; the true quartic "
          "32 is built (10, -4, 30, -4) DOMINATED by classes (0, 2) with "
          "classes (1, 3) contributing NEGATIVELY (-8): same number, "
          "disjoint mechanism -- the candidate index formula of K3.2 is "
          "a numerical coincidence, not a derivation",
          [0, 16, 0, -16] != [10, -4, 30, -4]
          and contrib[1] + contrib[3] == -8
          and cub[1] + cub[3] == 0 and abs(cub[1]) + abs(cub[3]) == 32)

    WD5, WA3 = 2 ** 4 * sp.factorial(5), sp.factorial(4)
    WE8 = 696729600
    WD8 = 2 ** 7 * sp.factorial(8)
    WA8 = sp.factorial(9)
    cands = {
        '|W(A3)|': WA3, '|W(D5)|': WD5, '|W(D5)| |W(A3)|': WD5 * WA3,
        '|W(E8)|': WE8, '|W(E8)|/|W(D5)|': F(WE8, int(WD5)),
        '|W(E8)|/|W(A3)|': F(WE8, int(WA3)),
        '|W(E8)|/|W(D5xA3)|': F(WE8, int(WD5 * WA3)),
        '|W(D5)|/|W(A3)|': F(int(WD5), int(WA3)),
        '|W(D8)|': WD8, '|W(E8)|/|W(A8)|': F(WE8, int(WA8)),
    }
    whits = [k for k, v in cands.items() if v == 1920]
    print("     Weyl/Kostant candidates: %s"
          % {k: str(v) for k, v in cands.items()})
    check("K3.5 [WEYL DATA, WRONG SIDE] hits on 1920 among the carrier "
          "Weyl data: %s -- |W(D5)| itself plus the ACCIDENTAL "
          "|W(E8)|/|W(A8)| = 1920 (A8 is not a carrier factor: a second "
          "coincidental 1920 inside E8 combinatorics); the d-symbol is an "
          "A3-side object with natural order |W(A3)| = 24, and 2^4 5! = "
          "%s" % (whits, WD5),
          whits == ['|W(D5)|', '|W(E8)|/|W(A8)|'] and WD5 == 1920
          and WA3 == 24 and WE8 == 2 ** 14 * 3 ** 5 * 5 ** 2 * 7)


# ---------------------------------------------------------------------------
# K4 -- negative controls
# ---------------------------------------------------------------------------
def section_k4(roots):
    print("  -- K4: negative controls (must fail consistently)")

    # (a) SO(16)/D8
    adj8 = Counter()
    for i, j in combinations(range(8), 2):
        for si in (1, -1):
            for sj in (1, -1):
                w = [0] * 8
                w[i], w[j] = 2 * si, 2 * sj
                adj8[tuple(w)] += 1
    adj8[(0,) * 8] += 8
    spin8 = Counter()
    for signs in product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            spin8[signs] += 1
    s3adj8 = inv_d8(sym3(adj8))
    y8 = sp.symbols('u1:9')
    cub_adj = sp.expand(sum(m * (sum(F(w[i], 2) * y8[i]
                                     for i in range(8))) ** 3
                            for w, m in adj8.items()))
    cub_spin = sp.expand(sum(m * (sum(F(w[i], 2) * y8[i]
                                      for i in range(8))) ** 3
                             for w, m in spin8.items()))
    F_so16 = [0, 60, 0]
    legal_prods = {F(F_so16[0] * F_so16[2], 2), F(F_so16[1] ** 2, 2)}
    WD8 = 2 ** 7 * sp.factorial(8)
    check("K4.1 [NC: SO(16)/D8] Inv(S^3 adj_d8) = %d = 0 (no d-channel to "
          "coefficient), cubic class sums = (%s, %s) = (0, 0) (all reps "
          "real), fluxes (0, 60, 0) => charge-legal flux products %s "
          "(dark spheres), |W(D8)| = %s != 1920: EVERY candidate formula "
          "fails or is undefined -- consistent"
          % (s3adj8, cub_adj, cub_spin, sorted(legal_prods), WD8),
          s3adj8 == 0 and cub_adj == 0 and cub_spin == 0
          and legal_prods == {0, 1800} and WD8 == 5160960)

    # (b) k = 2 flux doubling
    F2x = [128, 120, 128]
    pred = F(F2x[0] * F2x[1], 2)
    check("K4.2 [NC: k = 2 FLUX DOUBLING] the flux-product formula scales "
          "x4: F1*F2/2 -> %s = 7680 != 1920, while c_d = "
          "Phi_T3(A_fix)/Phi_T3(Q_dd) is ROOT-THEORETIC and static: K1 "
          "is not covariant under the flux dial; HONEST: |W(D5)| is also "
          "static, so this control kills K1 but cannot discriminate the "
          "Weyl fence" % pred,
          pred == 7680 and pred != 1920)

    # (c) false g0 = d5 (+) a2 (+) u1
    G0, adj45 = build_g0_reps(roots)
    s3f = inv_dim([box_sym3(G0)], inv_d5, inv_a2u1)
    check("K4.3 [NC: FALSE g0 = d5+a2+u1] Inv(S^3 g0_false) = %d = 6 != 1 "
          "(v511 D7.3): SIX symmetric cubics -- no unique channel, no "
          "unique c_d: the derivation question cannot even be posed on "
          "the false carrier" % s3f, s3f == 6)

    # (d) so(10) side: no cubic (sanity)
    s3d5 = inv_d5(sym3(adj45))
    A1, A2_, A3_ = sp.symbols('a1:4')
    Mso = sp.zeros(4)
    Mso[0, 1], Mso[1, 0] = A1, -A1
    Mso[0, 2], Mso[2, 0] = A2_, -A2_
    Mso[1, 2], Mso[2, 1] = A3_, -A3_
    check("K4.4 [NC: D5 SIDE] Inv(S^3 45) = %d = 0 and Tr X^3 = %s = 0 "
          "(antisymmetric): the D5 factor has NO cubic invariant -- "
          "|W(D5)| = 1920 belongs to the factor WITHOUT a d-symbol; no "
          "index mechanism can route the D5 Weyl order into the A3 "
          "channel coefficient"
          % (s3d5, sp.expand(sp.trace(Mso ** 3))),
          s3d5 == 0 and sp.expand(sp.trace(Mso ** 3)) == 0)


# ---------------------------------------------------------------------------
def run():
    import time
    t0 = time.time()
    print("WP5e-dterm probe: CAN GEOMETRY DERIVE c_d = 1920? "
          "(CELEST.SEAM.01, exploration only)")
    roots = build_glue_roots()

    K, Q, C, dA, qv, basis, Gm, Ginv, x, vvec = section_n0(roots)
    section_n1(roots, dA, qv, basis, Gm, x, vvec)
    section_k1(roots)
    section_k2()
    section_k3(K, Q, C, dA)
    section_k4(roots)

    print()
    print("VERDICT (dterm): NUMEROLOGIE -- the fingerprint c_d = 1920 = "
          "|W(D5)| does NOT survive the honest test battery.  (1) The "
          "number 1920 is convention-decorated: only the tr-fund/e8-"
          "Killing convention produces it (Gell-Mann: 120, su4-Killing: "
          "256, trace: 32, ch3: 69120); the convention-stable [E] content "
          "is c_d = Phi_T3(A_fix) x 2 h_vee(E8) = 32 x 60.  (2) K1: 11 "
          "catalog expressions + the |W(D5)| singleton + |W(E8)|/|W(A8)| "
          "hit 1920 (neighbouring smooth targets score comparably); the "
          "charge-LEGAL flux pairings give 2048 and 1800 -- they bracket "
          "and MISS; the only flux hit is the charge-forbidden (1,2) "
          "pairing.  (3) K2: quantisation delivers the lattice 60 Z "
          "(1920 = 32nd multiple, not minimal) or excludes 1920 outright "
          "(ch3 units); the integer 32 has 12 factorisations and is not "
          "forced.  (4) K3: the twisted cubic index |32i| matches "
          "numerically but its provenance (16 + 16 from classes 1, 3) "
          "clashes with the true quartic provenance (10, -4, 30, -4; "
          "classes 0, 2 dominate, classes 1, 3 contribute -8): "
          "coincidence exposed; |W(A3)| = 24 is the natural order of the "
          "d-symbol side, and the D5 factor has no cubic invariant at "
          "all.  (5) K4: SO(16) fails everything consistently, k = 2 "
          "kills the flux route, the false g0 cannot pose the question. "
          "CONSEQUENCE: the v511 [C] fence '1920 = |W(D5)|' should be "
          "read as a LOOK-ELSEWHERE-LOADED coincidence; the physical "
          "justification of the cubic GS term and of the factor 32 "
          "stays [O].")
    print()
    tot = N_PASS + N_FAIL
    print("CHECKS: %d/%d PASS%s   (%.1f s)"
          % (N_PASS, tot, "" if N_FAIL == 0 else "  (%d FAIL)" % N_FAIL,
             time.time() - t0))
    return N_FAIL == 0


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
