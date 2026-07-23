"""WP5e-wm of CELEST.SEAM.01 (EXPLORATION ONLY -- experiments/, no
verification claim).

"THE CONSTRUCTIVE w_m DERIVATION" -- the residual [O] of v516/v520.
v516 (CELEST.WP5E.M2.01) DECLARED the completion contact term

    contact_j = (Q^{(0)} - Q^{(j)}) / det_j ,

with det_j = det(1 - g^j) on the twistor fibre (g = diag(i, i^{-1}):
det_1 = det_3 = 2, det_2 = 4), and from it the completion weights
w_m = sum_j (1 - i^{jm})/det_j = (0, 3/2, 2, 3/2) = 4 h_m = -4 ch2(T_m).
v520 (CELEST.WP5E.MEASURE.01) decided the measure question at probe
level (ERFOLG-A): single-valuedness of the one-loop lattice factor is
DERIVED, and the numerator of the completion loop is FORCED to the
unphased sector trace Q^{(0)}.  The residual [O] named by v520: the
constructive derivation of the NORMALISATION 1/det_j itself.

THE HYPOTHESIS this probe attacks: 1/det_j is exactly the standard
Atiyah-Bott/holomorphic-Lefschetz fixed-point weight of the
equivariant one-loop amplitude in the g^j-twisted sector -- the
regularised g^j-character of the fibre mode space -- and equally the
Quillen-factorised zeta-determinant of the twisted fibre Laplacian.
If both constructive routes deliver 1/det_j, and the v520-forced
unphased numerator rides on the SAME fibre factor, the chain closes:
nothing in w_m is declared any more (at probe level, under the typed
premises below).

===========================================================================
PREREGISTRATION (fixed BEFORE any computation below)
===========================================================================

WHAT COUNTS AS "CONSTRUCTIVE" (fixed now, before computing): the
normalisation must be COMPUTED from an object that is defined WITHOUT
any reference to the v516 contact declaration or its target numbers:
  (source-i)   the equivariant mode ledger of the fibre C^2: the exact
       g^j-character of the polynomial function space, truncation
       degree by truncation degree in Q(i), with Abel/Cesaro
       regularisation (TP-REG) -- the standard construction of the
       equivariant character = the holomorphic Lefschetz fixed-point
       weight 1/det(1 - g^{-j}|_{T_0});
  (source-ii)  the spectral zeta function of the g^j-twisted fibre
       Laplacian (circle model, eigenvalues (n + a)^2, a = j/4):
       det_zeta = exp(-zeta'(0)) via Hurwitz zeta and the Lerch
       formula, PLUS the Quillen factorisation of the determinant
       line, det Delta = |det dbar|^2 (TP-Q);
  (source-iii) the exact modular fibre blocks of the delta-1f/v520
       transport machinery (the f1f3 dressing at the (0, b) nodes):
       their exact lowest-order (zero-mode) coefficient in Q(i).
A bare rescaling declared to match v516 is NOT admissible.  All
derivation steps exact (Q(i) / Q(zeta_k) / cyclotomic modular
arithmetic) or 30+ digit mpmath with printed deviations.

TYPED PREMISES (named, carried into the verdict):
  TP-REG  Abel/Cesaro/zeta regularisation IS the definition of the
          equivariant character / determinant (standard, but named);
  TP-Q    BCOV F1 is Quillen/Ray-Singer: det Delta = |det dbar|^2 and
          the physical one-loop factor is the holomorphic section of
          the determinant line (= v520 TP-4);
  TP-NUM  the completion-loop numerator is the unphased sector trace
          (the v520 ERFOLG-A decision layer, under its TP-1..TP-4);
  TP-CH   the insertion-channel (0, j) ledger computes the box-channel
          j contact normalisation (the shared v516/v518 scaffold: the
          modular frame in which the AB skeleton was declared).

ERFOLG fires iff ALL of
  (R1) [AB ROUTE, source-i] the exact fibre mode ledger matches the
       closed form (1 - t_j q + q^2)^{-1}, t_j = i^j + i^{-j}, at
       EVERY computed order; the Abel value at q = 1 is EXACTLY
       1/det_j = (1/2, 1/4, 1/2) in Q(i) (no pole: i^j /= 1 for
       j = 1, 2, 3); the (C,2) Cesaro truncation means converge to
       1/det_j with shrinking deviation; and the fixed-point factor
       SPLITS OFF EXACTLY AT EVERY TRUNCATION LEVEL d, for the phased
       (skeleton) and the unphased (completion, TP-NUM) gauge trace
       alike: contact_j(d) = (Q^{(0)} - Q^{(j)}) x T_j(d), Abel limit
       (Q^{(0)} - Q^{(j)})/det_j -- the v516 contact vectors.
  (R2) [ZETA/QUILLEN ROUTE, source-ii/iii] det_zeta(twisted circle
       Laplacian, a = j/4) = 4 sin^2(pi j/4) = det_j EXACTLY
       (reflection formula exact; Hurwitz/Lerch numerics 30+ digits);
       the Quillen split gives det Delta_j(fibre C^2) = det_j^2 with
       the UNIQUE positive real holomorphic section det dbar = det_j
       (existence of the real section = the SU(2) conjugation
       pairing); and the delta-1f modular fibre blocks carry EXACTLY
       the constant term 1/det_b at the (0, b) nodes (exact series
       + stripped mpmath limit).
  (R3) [CONSISTENCY CHAIN] inserting the DERIVED weight reproduces
       the v516 chain NUMBER BY NUMBER: w_m = (0, 3/2, 2, 3/2) =
       4 h_m = |mu4| h_m = -4 ch2(T_m); T5 = 0 for ANY scale c; ratio
       h_2 : h_1 = 4 : 3; the T3 budget forces c = 4 = |mu4| uniquely;
       per-sector perfect Okubo squares (18, 9, 18) <x,x>^2; total
       45 <x,x>^2 = (5/4) x 36 <x,x>^2; certificates Phi_T3: 32 -> 0,
       Phi_P: 72 -> 0; psi(A_fix) = +64, psi(contact) = -64.
  plus ALL negative controls behave (below).
KILL fires iff a constructive route yields a normalisation DIFFERENT
  from 1/det_j for the SU(2) fibre (e.g. 1/det_j^2, 1/|1 - i^j|, or a
  complex/non-real weight), or the two routes disagree with each
  other, or the derived weight fails ANY of the v516 identities in R3.
UNENTSCHIEDEN otherwise, with the gap named precisely.

NEGATIVE CONTROLS (mandatory teeth, fixed now):
  (NC-1) WRONG WEIGHT 1/det_j^2: index-bridge ratio w_2 : w_1 = 8 : 5
         /= 4 : 3, w' = (0, 5/8, 1, 5/8) /= 4h; against the
         v505-forced AB skeleton the totals keep T5 = +2 and
         T3 = +12; the j = 1 sector sum keeps T5 = -2 (no square);
         and the zeta side CONTRADICTS it: det dbar = det^2 would
         demand det Delta = det^4 = (16, 256, 16) /= det^2 =
         (4, 16, 4) (exact).
  (NC-2) WRONG WEIGHT 1/|1 - i^j| = (1/sqrt2, 1/2, 1/sqrt2): weights
         leave Q (w''_1 = 1 + sqrt2), the index bridge w = 4h breaks;
         totals keep T5 = 8 sqrt2 - 16 /= 0 and T3 = 64 - 48 sqrt2
         /= 0 (exact in Q(sqrt2)).
  (NC-3) Z2/EGUCHI-HANSON ANCHOR: the SAME derivation on C^2/Z2
         (g = -1): AB = Abel = zeta = det(1-g) = 4 = 4 sin^2(pi/2);
         w^{Z2} = (0, 1/2) = |Z2| h^{A1} = -2 ch2(A1); contact = Q_1;
         A_2 + contact = 9 <x,x>^2 = (1/4) x 36 <x,x>^2; the scale
         teeth clear BOTH quartics only at c = 2 = |Z2|;
         psi(A_2) = -8.
  (NC-4) SO(16)/D8 GLUE: classes {0, 2} only, the completion supplies
         only w_2: total (5/4)(Q_0 + Q_2) = (15, 30, 45, 20, -40)
         keeps T5 = 20, T3 = -40 -- the KILL branch fires there
         (Okubo failure inherited, E8 doubly special).
  (NC-5) diag(i, i): AB denominators (2i, 4, -2i) COMPLEX; the
         zeta = AB identity FAILS (real 4 sin^2 vs complex (1-i^j)^2:
         the SU(2) conjugation pairing is exactly what made them
         agree); no real Quillen section (arg((1-i)^2) = -pi/2);
         fake weights (0, -1/2, 0, 3/2) with w_1 /= w_3 break the
         conjugation pairing; the skeleton degenerates to A_2
         (v516 S4.4 replication).
  (NC-6) k = 3, 5 ORBIFOLDS (weights must wander, cf. v517 S5.3):
         exact in Q[x]/Phi_k(x): det_j^{(k)} = (1-z^j)(1-z^{-j}),
         w_m^{(k)} = sum_j (1 - z^{jm})/det_j^{(k)} = m(k-m)/2 =
         k h_m^{(k)} = -k ch2(T_m^{(A_{k-1})}) (Cartan-inverse
         route); Dedekind sum_j 1/det_j = (k^2-1)/12; prod_j det_j =
         k^2; zeta dets 4 sin^2(pi j/k) match the AB dets per j --
         the constructive weight moves correctly with the geometry,
         and only k = 4 carries the E8-glue chain of R3.

Numerics: exact sympy/Fraction/cyclotomic arithmetic wherever
possible; mpmath at mp.dps = 40 for the Hurwitz/Lerch certificates
and the stripped block limits (printed deviations, thresholds 1e-30 /
1e-25).  Runtime target < 20 min (expected < 5 min).

Throwaway probe: standalone, prints tables + PASS/FAIL + verdict,
ends with a check count.  Nothing here is a claim; verification/,
ledger, papers, changelog, website, scorecard untouched; NO marker
moves.  Provenance (read-only): v505 (AB ledger, index bridge), v516
(declared completion measure), v520 (measure decision, TP-1..TP-4),
experiments/tfpt-discovery/celestial_seam_wp5e_delta1f_single_
valuedness_probe.py (block machinery), v517 (k-control pattern).
"""
from fractions import Fraction as F
from itertools import combinations, product

import mpmath as mp
import sympy as sp

mp.mp.dps = 40

N_PASS = 0
N_FAIL = 0

HALF = F(1, 2)
IPOW = [(1, 0), (0, 1), (-1, 0), (0, -1)]      # i^e as Gaussian ints
DETS = {1: 2, 2: 4, 3: 2}
NPROD = 120
CESARO_PTS = (100, 200, 400)
TRUNC_PTS = (7, 12, 25)


def check(label, ok):
    global N_PASS, N_FAIL
    print(("  PASS  " if ok else "  FAIL  ") + label)
    if ok:
        N_PASS += 1
    else:
        N_FAIL += 1
    return bool(ok)


def fmt(xs):
    return "(" + ", ".join(str(x) for x in xs) + ")"


# ---------------------------------------------------------------------------
# E8 roots in D5 (+) A3 glue coordinates (v128/v492/v505/v516 construction)
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
# exact polynomial machinery on the D5 (+) A3 Cartan (v505/v516)
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


def lin_form(alpha):
    e = sum(sp.Rational(alpha[i].numerator, alpha[i].denominator) * X5[i]
            for i in range(5))
    e += sum(sp.Rational(alpha[5 + i].numerator, alpha[5 + i].denominator)
             * Y4[i] for i in range(4))
    return sp.expand(e)


def poly_dict(expr):
    return sp.Poly(sp.expand(expr), *ALLV, domain='QQ').as_dict()


def decompose(target):
    dicts = [poly_dict(b) for b in BASIS4]
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
    if sp.expand(target - sum(sol[i] * BASIS4[i] for i in range(5))) != 0:
        return None
    return [sp.Rational(x) for x in sol]


def quartics_by_class(roots):
    Q = {m: sp.Poly(0, *ALLV, domain='QQ') for m in range(4)}
    for alpha, c in roots.items():
        p = sp.Poly(lin_form(alpha), *ALLV, domain='QQ')
        Q[c] = Q[c] + (p ** 2) ** 2
    return {m: Q[m].as_expr() for m in range(4)}


def vsum(*vecs):
    return [sp.nsimplify(sum(v[i] for v in vecs)) for i in range(5)]


def vscale(c, v):
    return [sp.nsimplify(sp.expand(c * v[i])) for i in range(5)]


PHI_P = lambda v: sp.nsimplify(3 * v[0] - v[1] - v[2])
PSI = lambda v: sp.nsimplify(3 * v[0] - v[1] - v[2]
                             - sp.Rational(1, 4) * v[4])


# ---------------------------------------------------------------------------
# exact fibre mode ledger on C^2 (source-i)
# ---------------------------------------------------------------------------
def ledger_cn(j, nmax):
    """c_n = sum_{a+b=n} i^{j(a-b)}, direct double-sum ledger
    (exact Gaussian integers)."""
    out = []
    for n in range(nmax + 1):
        re = im = 0
        for a in range(n + 1):
            r, i_ = IPOW[(j * (2 * a - n)) % 4]
            re += r
            im += i_
        out.append((re, im))
    return out


def recur_cn(j, nmax):
    """the same coefficients from the CLOSED FORM
    1/((1 - q i^j)(1 - q i^{-j})) = 1/(1 - t_j q + q^2),
    t_j = i^j + i^{-j}, via its characteristic recursion."""
    t = IPOW[j % 4]
    tc = IPOW[(-j) % 4]
    tre, tim = t[0] + tc[0], t[1] + tc[1]
    out = [(1, 0)]
    if nmax >= 1:
        out.append((tre, tim))
    for n in range(2, nmax + 1):
        pre, pim = out[n - 1]
        qre, qim = out[n - 2]
        out.append((tre * pre - tim * pim - qre,
                    tre * pim + tim * pre - qim))
    return out


def cesaro2_devs(j, checkpoints):
    """(C,2) Cesaro means of T_j(d) = sum_{a+b<=d} i^{j(a-b)},
    exact Fractions; returns {N: (M2_re - 1/det_j, M2_im)}."""
    cs = recur_cn(j, max(checkpoints))
    target = F(1, DETS[j])
    Tre = Tim = 0
    STre = STim = 0
    SM1re, SM1im = F(0), F(0)
    devs = {}
    for d in range(max(checkpoints) + 1):
        Tre += cs[d][0]
        Tim += cs[d][1]
        STre += Tre
        STim += Tim
        SM1re += F(STre, d + 1)
        SM1im += F(STim, d + 1)
        if d in checkpoints:
            devs[d] = (SM1re / (d + 1) - target, SM1im / (d + 1))
    return devs


def fiber_T_pair(j, d):
    """T_j(d) = sum_{a+b<=d} i^{j(a-b)} as Gaussian-int pair."""
    re = im = 0
    for n in range(d + 1):
        for a in range(n + 1):
            r, i_ = IPOW[(j * (2 * a - n)) % 4]
            re += r
            im += i_
    return (re, im)


def tensor_trace(j, d, Qv, phased):
    """direct (gauge x fibre) tensor trace at truncation d:
    sum_m sum_{a+b<=d} i^{j(m [phased] + a - b)} Q_m -- the group
    element acts on the FIBRE modes always (twisted sector) and on
    the gauge factor only in the phased (skeleton) trace."""
    out = [sp.Integer(0)] * 5
    for m in range(4):
        re = im = 0
        for n in range(d + 1):
            for a in range(n + 1):
                e = j * (a - (n - a)) + (j * m if phased else 0)
                r, i_ = IPOW[e % 4]
                re += r
                im += i_
        ph = sp.Integer(re) + sp.I * im
        for i in range(5):
            out[i] += ph * Qv[m][i]
    return [sp.expand(x) for x in out]


# ---------------------------------------------------------------------------
# delta-1f fibre block machinery (exact Gaussian-pair series + mpmath)
# ---------------------------------------------------------------------------
def gadd(z1, z2):
    return (z1[0] + z2[0], z1[1] + z2[1])


def gmul(z1, z2):
    return (z1[0] * z2[0] - z1[1] * z2[1], z1[0] * z2[1] + z1[1] * z2[0])


def fipow(b):
    return [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))][b % 4]


def uroot(N, k):
    if N == 2:
        return [(F(1), F(0)), (F(-1), F(0))][k % 2]
    return fipow(k)


def ser_mul(A, B, cut):
    out = {}
    for e1, v1 in A.items():
        for e2, v2 in B.items():
            e = e1 + e2
            if e > cut:
                continue
            out[e] = gadd(out.get(e, (F(0), F(0))), gmul(v1, v2))
    return {e: v for e, v in out.items() if v != (F(0), F(0))}


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


def qp(tau, e):
    return mp.exp(2j * mp.pi * tau * e)


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


# ---------------------------------------------------------------------------
# exact cyclotomic arithmetic in Q[x]/Phi_k(x) (NC-6)
# ---------------------------------------------------------------------------
def cyclo_data(k):
    x = sp.symbols('x')
    Phi = sp.expand(sp.cyclotomic_poly(k, x))

    def red(p):
        return sp.rem(sp.expand(p), Phi, x)

    dets = {j: red((1 - x ** j) * (1 - x ** (k - j)))
            for j in range(1, k)}
    invs = {j: red(sp.invert(dets[j], Phi, x)) for j in range(1, k)}
    wm = {}
    for m in range(1, k):
        acc = sp.Integer(0)
        for j in range(1, k):
            acc += red((1 - x ** ((j * m) % k)) * invs[j])
        wm[m] = red(acc)
    ded = red(sum(invs[j] for j in range(1, k)))
    prd = sp.Integer(1)
    for j in range(1, k):
        prd = red(prd * dets[j])
    n = k - 1
    C = sp.Matrix(n, n, lambda i, j2: 2 if i == j2
                  else (-1 if abs(i - j2) == 1 else 0))
    Ci = C.inv()
    ch2 = [-Ci[m, m] / 2 for m in range(n)]
    zeta_ok = True
    zk = sp.exp(2 * sp.pi * sp.I / k)
    for j in range(1, k):
        dv = sp.simplify(sp.expand_complex(
            dets[j].subs(x, zk)) - 4 * sp.sin(sp.pi * sp.Rational(j, k)) ** 2)
        if dv != 0:
            zeta_ok = False
    return dets, wm, ded, prd, ch2, zeta_ok


# ---------------------------------------------------------------------------
# S0 -- replication foundations: roots, class quartics, AB data
# ---------------------------------------------------------------------------
def section0():
    print("  -- S0: replication foundations (roots, quartics, AB data)")
    I = sp.I
    roots = build_glue_roots()
    counts = [sum(1 for c in roots.values() if c == m) for m in range(4)]
    check("S0.1 [ROOTS] 240 roots, all norm 2, class split %s = "
          "(52, 64, 60, 64) (v492/v505/v516 replication)" % fmt(counts),
          len(roots) == 240 and counts == [52, 64, 60, 64]
          and all(sum(x * x for x in r) == 2 for r in roots))

    Qpoly = quartics_by_class(roots)
    Qv = {m: decompose(Qpoly[m]) for m in range(4)}
    expect = {0: [12, 0, 6, 4, 8], 1: [12, 24, 0, -8, 16],
              2: [0, 24, 30, 12, -40], 3: [12, 24, 0, -8, 16]}
    print("     class quartics Q_m in (P1, P2, P3, T5, T3):")
    for m in range(4):
        print("       Q_%d = %s" % (m, fmt(Qv[m])))
    check("S0.2 [CLASS QUARTICS] Q_0 = (12,0,6,4,8), Q_1 = Q_3 = "
          "(12,24,0,-8,16), Q_2 = (0,24,30,12,-40) (v505 S3.1 "
          "replication)",
          all(Qv[m] == [sp.Rational(x) for x in expect[m]]
              for m in range(4)))

    dens = [sp.nsimplify(sp.expand((1 - I ** (-j)) * (1 - I ** j)))
            for j in (1, 2, 3)]
    dens_rev = [sp.nsimplify(sp.expand((1 - I ** j) * (1 - I ** (-j))))
                for j in (1, 2, 3)]
    recip = sum(sp.Rational(1, d) for d in dens)
    prd = dens[0] * dens[1] * dens[2]
    check("S0.3 [AB DENOMINATORS] det(1 - g^j|_{C^2}) = "
          "(1-i^j)(1-i^{-j}) = %s = (2, 4, 2), REAL POSITIVE (g in "
          "SU(2)); orientation-blind det(1-g^{-j}) identical; Dedekind "
          "sum %s = 5/4 = (|Z4|^2-1)/12; product %s = 16 = |Z4|^2 "
          "(v505 S1.1/S1.2 replication)" % (fmt(dens), recip, prd),
          dens == [2, 4, 2] and dens_rev == dens
          and recip == sp.Rational(5, 4) and prd == 16
          and sp.Rational(16 - 1, 12) == sp.Rational(5, 4))

    Qtw = {j: [sp.nsimplify(sp.expand(
        sum(I ** (j * m) * Qv[m][i] for m in range(4))))
        for i in range(5)] for j in range(4)}
    Afix = [sp.nsimplify(sum(Qtw[j][i] / DETS[j] for j in (1, 2, 3)))
            for i in range(5)]
    check("S0.4 [TWISTED QUARTICS + BULK] Q^{(0)} = %s = (36,72,36,0,0) "
          "= 36<x,x>^2 (bulk Okubo); Q^{(1)} = Q^{(3)} = %s, Q^{(2)} = "
          "%s; A_fix = sum_j Q^{(j)}/det_j = %s = (9,-30,-15,0,32) "
          "(v505 S3.7 replication: rigid +32 T3 residual)"
          % (fmt(Qtw[0]), fmt(Qtw[1]), fmt(Qtw[2]), fmt(Afix)),
          Qtw[0] == [36, 72, 36, 0, 0]
          and Qtw[1] == [12, -24, -24, -8, 48]
          and Qtw[3] == Qtw[1]
          and Qtw[2] == [-12, -24, 36, 32, -64]
          and Afix == [9, -30, -15, 0, 32])
    return Qv, Qtw, Afix


# ---------------------------------------------------------------------------
# S1 -- ROUTE (i): the Atiyah-Bott mode ledger, exact
# ---------------------------------------------------------------------------
def section1(Qv, Qtw):
    print("  -- S1: route (i) -- the equivariant fibre mode ledger")
    I = sp.I
    q = sp.symbols('q')

    NMAX = max(CESARO_PTS)
    ok_match = True
    for j in (1, 2, 3):
        led = ledger_cn(j, 120)
        rec = recur_cn(j, NMAX)
        if led != rec[:121]:
            ok_match = False
        Fq = 1 / ((1 - q * I ** j) * (1 - q * I ** (-j)))
        ser = sp.series(Fq, q, 0, 13).removeO()
        poly = sp.expand(sum((sp.Integer(rec[n][0]) + sp.I * rec[n][1])
                             * q ** n for n in range(13)))
        if sp.expand(ser - poly) != 0:
            ok_match = False
    check("S1.1 [MODE LEDGER = CLOSED FORM, EXACT] the direct fibre "
          "ledger c_n = sum_{a+b=n} i^{j(a-b)} equals the recursion of "
          "1/((1-q i^j)(1-q i^{-j})) = 1/(1 - t_j q + q^2) for all "
          "n <= 120 AND the sympy series to order 12, for j = 1, 2, 3 "
          "(t_j = i^j + i^{-j} = (0, -2, 0)): the generating function "
          "of the mode ledger IS the reciprocal characteristic "
          "polynomial of g^j -- no input from v516", ok_match)

    abel = [sp.nsimplify(
        (1 / ((1 - q * I ** j) * (1 - q * I ** (-j)))).subs(q, 1))
        for j in (1, 2, 3)]
    dens_at_1 = [sp.nsimplify(sp.expand(
        (1 - I ** j) * (1 - I ** (-j)))) for j in (1, 2, 3)]
    check("S1.2 [ABEL VALUE EXACT IN Q(i)] the closed form is REGULAR "
          "at q = 1 for j = 1, 2, 3 (denominator = %s /= 0; the "
          "untwisted j = 0 channel keeps its volume pole -- it carries "
          "no 1/det weight, its normalisation is the mu-blind v514 "
          "chain): Abel value F_j(1) = %s = (1/2, 1/4, 1/2) = 1/det_j "
          "EXACTLY -- the fixed-point weight is COMPUTED, not chosen"
          % (fmt(dens_at_1), fmt(abel)),
          dens_at_1 == [2, 4, 2]
          and abel == [sp.Rational(1, 2), sp.Rational(1, 4),
                       sp.Rational(1, 2)])

    ok_ces = True
    print("     (C,2) Cesaro deviations |M2(N) - 1/det_j| "
          "(exact Fractions):")
    for j in (1, 2, 3):
        devs = cesaro2_devs(j, CESARO_PTS)
        mags = {}
        for N, (dre, dim_) in devs.items():
            mags[N] = float(abs(complex(dre, dim_)))
            if dim_ != 0:
                ok_ces = False
        print("       j=%d : " % j
              + ", ".join("N=%d: %.5f" % (N, mags[N])
                          for N in CESARO_PTS))
        if not (mags[100] > mags[200] > mags[400]
                and mags[400] < 0.02):
            ok_ces = False
    check("S1.3 [CESARO CONVERGENCE, EXACT ARITHMETIC] the (C,2) "
          "means of the truncated ledger sums T_j(d) converge to "
          "1/det_j: imaginary parts exactly 0, deviations strictly "
          "shrinking over N = 100 -> 200 -> 400 and < 0.02 at N = 400 "
          "for all three sectors (TP-REG: Abel/Cesaro is the "
          "equivariant character)", ok_ces)

    ok_split = True
    for j in (1, 2, 3):
        for d in TRUNC_PTS:
            Tre, Tim = fiber_T_pair(j, d)
            Tph = sp.Integer(Tre) + sp.I * Tim
            lhs_ph = tensor_trace(j, d, Qv, phased=True)
            rhs_ph = [sp.expand(Qtw[j][i] * Tph) for i in range(5)]
            lhs_un = tensor_trace(j, d, Qv, phased=False)
            rhs_un = [sp.expand(Qtw[0][i] * Tph) for i in range(5)]
            if any(sp.expand(lhs_ph[i] - rhs_ph[i]) != 0
                   for i in range(5)):
                ok_split = False
            if any(sp.expand(lhs_un[i] - rhs_un[i]) != 0
                   for i in range(5)):
                ok_split = False
    contact = {j: [sp.nsimplify((Qtw[0][i] - Qtw[j][i])
                                * sp.Rational(1, DETS[j]))
                   for i in range(5)] for j in (1, 2, 3)}
    skel = {j: [sp.nsimplify(Qtw[j][i] * sp.Rational(1, DETS[j]))
                for i in range(5)] for j in (1, 2, 3)}
    print("     Abel-limit contact vectors (P1, P2, P3, T5, T3):")
    for j in (1, 2, 3):
        print("       j=%d : %s" % (j, fmt(contact[j])))
    check("S1.4 [FIXED-POINT SPLITTING AT EVERY LEVEL] at every "
          "truncation degree d in %s the direct (gauge x fibre) "
          "tensor trace factorises EXACTLY: phased (skeleton) trace = "
          "Q^{(j)} x T_j(d), unphased (completion, TP-NUM = the "
          "v520-forced numerator) trace = Q^{(0)} x T_j(d) -- the "
          "SAME fibre factor multiplies both; Abel limit: skeleton_j "
          "= Q^{(j)}/det_j = %s..., contact_j = (Q^{(0)} - Q^{(j)}) "
          "/det_j = (12,48,30,4,-24)/(12,24,0,-8,16)/(12,48,30,4,-24) "
          "-- the v516 contact term DERIVED from the mode ledger"
          % (str(TRUNC_PTS), fmt(skel[1])),
          ok_split
          and contact[1] == [12, 48, 30, 4, -24]
          and contact[2] == [12, 24, 0, -8, 16]
          and contact[3] == [12, 48, 30, 4, -24]
          and skel[1] == [6, -12, -12, -4, 24]
          and skel[2] == [-3, -6, 9, 8, -16]
          and skel[3] == skel[1])

    ok_lef = True
    for j in (1, 2, 3):
        f_plus = sp.nsimplify((1 / (1 - q * I ** j)).subs(q, 1))
        f_minus = sp.nsimplify((1 / (1 - q * I ** (-j))).subs(q, 1))
        prod = sp.nsimplify(sp.expand(f_plus * f_minus))
        if prod != sp.Rational(1, DETS[j]):
            ok_lef = False
        d_fwd = sp.nsimplify(sp.expand((1 - I ** j) * (1 - I ** (-j))))
        d_bwd = sp.nsimplify(sp.expand((1 - I ** (-j)) * (1 - I ** j)))
        if d_fwd != d_bwd or sp.im(d_fwd) != 0:
            ok_lef = False
    check("S1.5 [HOLOMORPHIC LEFSCHETZ FACTORISATION] each fibre "
          "direction contributes its own Abel-regularised geometric "
          "ledger 1/(1 - i^{+-j}); the product is 1/det_j; and "
          "det(1 - g^j) = det(1 - g^{-j}) real (the AB weight is "
          "orientation-blind exactly because g in SU(2) pairs each "
          "eigenvalue with its conjugate -- the ingredient the "
          "diag(i,i) control breaks)", ok_lef)
    R1 = bool(ok_match and ok_ces and ok_split and ok_lef
              and dens_at_1 == [2, 4, 2]
              and abel == [sp.Rational(1, 2), sp.Rational(1, 4),
                           sp.Rational(1, 2)]
              and contact[2] == [12, 24, 0, -8, 16])
    return R1, contact, skel


# ---------------------------------------------------------------------------
# S2 -- ROUTE (ii): zeta determinant + Quillen factorisation
# ---------------------------------------------------------------------------
def section2():
    print("  -- S2: route (ii) -- zeta determinant / Quillen split")
    I = sp.I
    R = sp.Rational

    dz = [sp.nsimplify(4 * sp.sin(sp.pi * R(j, 4)) ** 2)
          for j in (1, 2, 3)]
    ok_refl = True
    for j in (1, 2, 3):
        a = R(j, 4)
        refl = sp.simplify((2 * sp.pi / (sp.gamma(a)
                                         * sp.gamma(1 - a))) ** 2
                           - 4 * sp.sin(sp.pi * a) ** 2)
        if refl != 0:
            ok_refl = False
    check("S2.1 [ZETA CLOSED FORM, EXACT] eigenvalues (n + j/4)^2 on "
          "the twisted circle: det_zeta = exp(-zeta'(0)) = "
          "(2 pi / (Gamma(a) Gamma(1-a)))^2 = 4 sin^2(pi a) (Lerch + "
          "reflection, exact in sympy) = %s = (2, 4, 2) = det_j "
          "EXACTLY for a = j/4 -- the spectral determinant of the "
          "g^j-twisted fibre Laplacian IS the AB denominator"
          % fmt(dz),
          dz == [2, 4, 2] and ok_refl)

    ok_hur = True
    devs = []
    for j in (1, 2, 3):
        a = mp.mpf(j) / 4
        lerch_dev = abs(mp.zeta(0, a, 1)
                        - mp.log(mp.gamma(a) / mp.sqrt(2 * mp.pi)))
        zp = (mp.zeta(0, a, 1) + mp.zeta(0, 1 - a, 1))
        detz = mp.exp(-2 * zp)
        det_dev = abs(detz - DETS[j])
        devs.append((j, lerch_dev, det_dev))
        if lerch_dev > mp.mpf(10) ** (-30) or det_dev > mp.mpf(10) ** (-30):
            ok_hur = False
    print("     Hurwitz certificates: "
          + "; ".join("j=%d: Lerch dev %s, det dev %s"
                      % (j, mp.nstr(ld, 3), mp.nstr(dd, 3))
                      for j, ld, dd in devs))
    check("S2.2 [HURWITZ NUMERICS, 30+ DIGITS] zeta_H'(0, a) = "
          "ln(Gamma(a)/sqrt(2 pi)) verified directly (mpmath, dps 40, "
          "devs < 1e-30) and det_zeta(j) = exp(-2[zeta_H'(0,a) + "
          "zeta_H'(0,1-a)]) = (2, 4, 2) to 30+ digits: the classical "
          "Lerch input is machine-checked, not just cited", ok_hur)

    ok_quillen = True
    for j in (1, 2, 3):
        a = sp.Rational(j, 4)
        dz_a = sp.nsimplify(4 * sp.sin(sp.pi * a) ** 2)
        dz_b = sp.nsimplify(4 * sp.sin(sp.pi * (1 - a)) ** 2)
        detDelta = sp.nsimplify(dz_a * dz_b)
        hol = sp.nsimplify(sp.expand((1 - I ** j) * (1 - I ** (-j))))
        if detDelta != DETS[j] ** 2:
            ok_quillen = False
        if sp.im(hol) != 0 or hol <= 0 or hol ** 2 != detDelta:
            ok_quillen = False
        if sp.sqrt(detDelta) != DETS[j]:
            ok_quillen = False
    check("S2.3 [QUILLEN SPLIT OF THE DETERMINANT LINE] the two fibre "
          "directions carry twists a = j/4 and 1 - j/4: det "
          "Delta_j(fibre) = det_zeta(a) det_zeta(1-a) = det_j^2 = "
          "(4, 16, 4); TP-Q (det Delta = |det dbar|^2) gives "
          "|det dbar| = det_j; the AB holomorphic section "
          "(1-i^j)(1-i^{-j}) = det_j is REAL POSITIVE (SU(2) "
          "conjugation pairing), so the positive square root is "
          "unique and canonical: det dbar = det_j, one-loop "
          "normalisation 1/det dbar = 1/det_j -- the Quillen "
          "factorisation lands on the SAME weight as route (i)",
          ok_quillen)

    ok_const = True
    cut = F(3)
    for b in (1, 2, 3):
        s1, sh1 = f_series(4, 1, 0, b, cut)
        s3, sh3 = f_series(4, 3, 0, b, cut)
        prod = ser_mul(s1, s3, cut)
        emin = min(prod.keys())
        c0 = prod.get(F(0), (F(0), F(0)))
        if emin != 0 or c0 != (F(1, DETS[b]), F(0)):
            ok_const = False
        if sh1 != F(-1, 12) or sh3 != F(-1, 12):
            ok_const = False
    check("S2.4 [delta-1f BLOCK CONSTANT TERM, EXACT] the f1f3 fibre "
          "block of the v518/v520 transport machinery at the (0, b) "
          "nodes has lowest exponent 0 with EXACT coefficient "
          "1/((1-i^b)(1-i^{-b})) = 1/det_b = (1/2, 1/4, 1/2) in Q(i) "
          "(E-shift -1/12 per factor booked separately): the modular "
          "blocks that drove the v520 measure decision CARRY the AB "
          "zero-mode weight verbatim -- route (ii) meets the "
          "delta-1f transports", ok_const)

    ok_strip = True
    strip_devs = []
    for b in (1, 2, 3):
        for tau, thr in ((mp.mpc(0, 3), mp.mpf(10) ** (-6)),
                         (mp.mpc(0, 10), mp.mpf(10) ** (-25))):
            val = (f_val(4, 1, 0, b, tau) * f_val(4, 3, 0, b, tau)
                   * qp(tau, mp.mpf(1) / 6))
            dev = abs(val - mp.mpf(1) / DETS[b])
            if tau.imag == 10:
                strip_devs.append((b, dev))
            if dev > thr:
                ok_strip = False
    print("     stripped block limits at tau = 10i: "
          + "; ".join("b=%d: dev %s" % (b, mp.nstr(d, 3))
                      for b, d in strip_devs))
    check("S2.5 [NUMERIC STRIP LIMIT] the full mpmath fibre blocks "
          "f1 f3 (0, b), stripped of the E-shift prefactor q^{-1/6}, "
          "converge to 1/det_b in the degeneration limit: devs "
          "< 1e-6 at tau = 3i and < 1e-25 at tau = 10i (dps 40) -- "
          "the exact constant term is the zero-mode of the actual "
          "one-loop block, not a series artefact", ok_strip)
    R2 = bool(dz == [2, 4, 2] and ok_refl and ok_hur and ok_quillen
              and ok_const and ok_strip)
    return R2


# ---------------------------------------------------------------------------
# S3 -- ROUTE (iii): the consistency chain, number by number
# ---------------------------------------------------------------------------
def section3(Qv, Qtw, Afix, contact, skel):
    print("  -- S3: route (iii) -- the v516 chain with the DERIVED "
          "weight")
    I = sp.I
    R = sp.Rational

    f = [sp.nsimplify(sp.expand(
        R(1, 4) * sum((I ** (j * m) - 1) / DETS[j] for j in (1, 2, 3))))
        for m in range(4)]
    h = [R(m * (4 - m), 8) for m in range(4)]
    C = sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
    Cinv = C.inv()
    ch2 = [-Cinv[m, m] / 2 for m in range(3)]
    check("S3.1 [INDEX BRIDGE] f(m) = (1/4) sum_j (i^{jm}-1)/det_j = "
          "%s = (0, -3/8, -1/2, -3/8) = ch2(T_m) = -h_m with h_m = "
          "m(4-m)/8 (v505 S4.3 replication, det_j now DERIVED)"
          % fmt(f),
          f == [0, R(-3, 8), R(-1, 2), R(-3, 8)]
          and all(f[m + 1] == ch2[m] for m in range(3))
          and all(h[m] == -f[m] for m in range(4)))

    w = [sp.nsimplify(sp.expand(
        sum((1 - I ** (j * m)) / DETS[j] for j in (1, 2, 3))))
        for m in range(4)]
    c = sp.symbols('c')
    T5tot = sp.expand(c * sum(h[m] * Qv[m][3] for m in range(4)))
    T3tot = sp.expand(c * sum(h[m] * Qv[m][4] for m in range(4)))
    sol_c = sp.solve(sp.Eq(T3tot + 32, 0), c)
    leftovers = {cc: sp.nsimplify(32 + cc * sum(h[m] * Qv[m][4]
                                                for m in range(4)))
                 for cc in (1, 2, 3, 4, 5)}
    check("S3.2 [WEIGHTS + PARAMETER-FREE LOCKS] w_m = sum_j "
          "(1-i^{jm})/det_j = %s = (0, 3/2, 2, 3/2) = 4 h_m = "
          "|mu4| h_m = -4 ch2(T_m); ratio h_2 : h_1 = %s = 4 : 3; "
          "T5 total = %s = 0 for ANY scale c; T3 budget: leftover "
          "32 - 8c = %s -- only c = %s = 4 = |mu4| clears it (v516 "
          "S1.2/S1.3/S4.1 replicated with the DERIVED det_j)"
          % (fmt(w), h[2] / h[1], T5tot, str(leftovers), sol_c),
          w == [0, R(3, 2), 2, R(3, 2)]
          and all(w[m] == 4 * h[m] for m in range(4))
          and h[2] / h[1] == R(4, 3) and T5tot == 0
          and sol_c == [4]
          and leftovers == {1: 24, 2: 16, 3: 8, 4: 0, 5: -8})

    total = vsum(contact[1], contact[2], contact[3])
    classform = [sp.nsimplify(sum(4 * h[m] * Qv[m][i] for m in range(4)))
                 for i in range(5)]
    sums = {j: vsum(skel[j], contact[j]) for j in (1, 2, 3)}
    targets = {j: [sp.nsimplify(Qtw[0][i] * R(1, DETS[j]))
                   for i in range(5)] for j in (1, 2, 3)}
    tot = vsum(Afix, total)
    print("     SUCCESS TABLE (P1, P2, P3, T5, T3):")
    for j in (1, 2, 3):
        print("       ch %d: skeleton %s + contact %s = %s"
              % (j, fmt(skel[j]), fmt(contact[j]), fmt(sums[j])))
    print("       total: A_fix %s + contact %s = %s"
          % (fmt(Afix), fmt(total), fmt(tot)))
    check("S3.3 [CONTACT + PER-SECTOR SQUARES + TOTAL] channel form "
          "sum_j (Q^{(0)}-Q^{(j)})/det_j = class form sum_m 4 h_m Q_m "
          "= %s = (36, 120, 60, 0, -32); per sector skeleton_j + "
          "contact_j = Q^{(0)}/det_j: (18, 9, 18) x <x,x>^2 with "
          "T5 = T3 = 0 in EVERY channel; total = %s = 45<x,x>^2 = "
          "(5/4) x 36<x,x>^2 = (Dedekind) x (Okubo) (v516 S2.1/S3.1/"
          "S3.2 number by number)" % (fmt(total), fmt(tot)),
          total == [36, 120, 60, 0, -32] and total == classform
          and all(sums[j] == targets[j] for j in (1, 2, 3))
          and sums[1] == [18, 36, 18, 0, 0]
          and sums[2] == [9, 18, 9, 0, 0]
          and sums[3] == [18, 36, 18, 0, 0]
          and tot == [45, 90, 45, 0, 0])

    cert = (Afix[4], total[4], PHI_P(Afix), PHI_P(total),
            PSI(Afix), PSI(total))
    check("S3.4 [CERTIFICATES + psi SLICE] Phi_T3: A_fix %s + contact "
          "%s = 0; Phi_P: %s + %s = 0; psi = Phi_P - Phi_T3/4: "
          "%s + %s = 0 -- the v511 psi = 64 slice is SUPPLIED exactly "
          "by the derived-weight contact (v516 S3.3 replication)"
          % cert, cert == (32, -32, 72, -72, 64, -64))
    R3 = bool(f == [0, R(-3, 8), R(-1, 2), R(-3, 8)]
              and w == [0, R(3, 2), 2, R(3, 2)]
              and total == [36, 120, 60, 0, -32]
              and tot == [45, 90, 45, 0, 0]
              and cert == (32, -32, 72, -72, 64, -64))
    return R3, h


# ---------------------------------------------------------------------------
# S4 -- negative controls
# ---------------------------------------------------------------------------
def section4(Qv, Qtw, Afix, h):
    print("  -- S4: negative controls")
    I = sp.I
    R = sp.Rational

    d2 = {j: DETS[j] ** 2 for j in (1, 2, 3)}
    w1 = [sp.nsimplify(sp.expand(
        sum((1 - I ** (j * m)) / d2[j] for j in (1, 2, 3))))
        for m in range(4)]
    ct1 = {j: [sp.nsimplify((Qtw[0][i] - Qtw[j][i]) * R(1, d2[j]))
               for i in range(5)] for j in (1, 2, 3)}
    tot1 = vsum(Afix, ct1[1], ct1[2], ct1[3])
    sec1 = vsum([sp.nsimplify(Qtw[1][i] * R(1, 2)) for i in range(5)],
                ct1[1])
    quillen_clash = [(DETS[j] ** 2) ** 2 != DETS[j] ** 2
                     for j in (1, 2, 3)]
    check("S4.1 [NC-1: WRONG WEIGHT 1/det^2] w' = %s = (0, 5/8, 1, "
          "5/8): ratio %s = 8:5 /= 4:3, w' /= 4h; against the v505-"
          "forced skeleton the totals keep (T5, T3) = (%s, %s) = "
          "(2, 12) /= (0, 0); sector-1 sum %s keeps T5 = -2 (no "
          "square); zeta contradiction: det dbar = det^2 would demand "
          "det Delta = det^4 = (16, 256, 16) /= measured det^2 = "
          "(4, 16, 4): %s -- the chain BREAKS, quantified"
          % (fmt(w1), w1[2] / w1[1], tot1[3], tot1[4], fmt(sec1),
             all(quillen_clash)),
          w1 == [0, R(5, 8), 1, R(5, 8)] and w1[2] / w1[1] == R(8, 5)
          and any(w1[m] != 4 * h[m] for m in range(4))
          and tot1[3] == 2 and tot1[4] == 12
          and sec1[3] == -2 and all(quillen_clash))

    dabs = {1: sp.sqrt(2), 2: sp.Integer(2), 3: sp.sqrt(2)}
    w2 = [sp.simplify(sp.expand_complex(
        sum((1 - I ** (j * m)) / dabs[j] for j in (1, 2, 3))))
        for m in range(4)]
    ct2_t5 = sp.simplify(sum((Qtw[0][3] - Qtw[j][3]) / dabs[j]
                             for j in (1, 2, 3)))
    ct2_t3 = sp.simplify(sum((Qtw[0][4] - Qtw[j][4]) / dabs[j]
                             for j in (1, 2, 3)))
    tot2_t3 = sp.simplify(32 + ct2_t3)
    check("S4.2 [NC-2: WRONG WEIGHT 1/|1-i^j|] w'' = %s leaves Q "
          "(w''_1 = 1 + sqrt2 is irrational -- the index bridge "
          "w = 4h and the exact Q-rational ledger are UNREACHABLE); "
          "contact T5 = %s = 8 sqrt2 - 16 /= 0; total T3 = %s = "
          "64 - 48 sqrt2 /= 0 (exact in Q(sqrt2)) -- the |.|-weight "
          "breaks the chain"
          % (fmt(w2), ct2_t5, tot2_t3),
          sp.simplify(w2[1] - (1 + sp.sqrt(2))) == 0
          and not w2[1].is_rational
          and sp.simplify(ct2_t5 - (8 * sp.sqrt(2) - 16)) == 0
          and ct2_t5 != 0
          and sp.simplify(tot2_t3 - (64 - 48 * sp.sqrt(2))) == 0
          and tot2_t3 != 0)

    q = sp.symbols('q')
    abel_z2 = sp.nsimplify((1 / ((1 + q) * (1 + q))).subs(q, 1))
    detz_z2 = sp.nsimplify(4 * sp.sin(sp.pi * R(1, 2)) ** 2)
    ab_z2 = sp.nsimplify(sp.expand((1 - (-1)) * (1 - (-1))))
    wz2 = [sp.nsimplify(sp.expand((1 - (-1) ** m) / ab_z2))
           for m in range(2)]
    hA1 = R(1, 4)
    A2 = [sp.nsimplify((Qv[0][i] - Qv[1][i] + Qv[2][i] - Qv[3][i])
                       / 4) for i in range(5)]
    contact2 = [sp.nsimplify(R(1, 2) * (Qv[1][i] + Qv[3][i]))
                for i in range(5)]
    tot2 = vsum(A2, contact2)
    teeth = {cc: (sp.nsimplify(A2[3] + cc * hA1 * (Qv[1][3] + Qv[3][3])),
                  sp.nsimplify(A2[4] + cc * hA1 * (Qv[1][4] + Qv[3][4])))
             for cc in (1, 2, 3, 4)}
    check("S4.3 [NC-3: Z2/EGUCHI-HANSON ANCHOR] the SAME derivation "
          "on C^2/Z2 (g = -1): Abel value %s = zeta det reciprocal "
          "1/%s = 1/det(1-g) = 1/%s = 1/4 = 1/|Z2|^2; derived weights "
          "w^{Z2} = %s = (0, 1/2) = |Z2| h^{A1} = -2 ch2(A1); contact "
          "= (1/2)(Q_1 + Q_3) = Q_1 = %s; A_2 + contact = %s = "
          "9<x,x>^2 = (1/4) x 36<x,x>^2, psi(A_2) = %s = -8; scale "
          "teeth (T5, T3) leftovers %s: BOTH clear only at c = 2 = "
          "|Z2| -- the published-anchor case PASSES with the same "
          "constructive weight"
          % (abel_z2, detz_z2, ab_z2, fmt(wz2), fmt(contact2),
             fmt(tot2), PSI(A2), str(teeth)),
          abel_z2 == R(1, 4) and detz_z2 == 4 and ab_z2 == 4
          and wz2 == [0, R(1, 2)] and wz2[1] == 2 * hA1
          and A2 == [-3, -6, 9, 8, -16]
          and contact2 == [12, 24, 0, -8, 16]
          and tot2 == [9, 18, 9, 0, 0] and PSI(A2) == -8
          and teeth == {1: (4, -8), 2: (0, 0), 3: (-4, 8),
                        4: (-8, 16)})

    so_tot = [sp.nsimplify(R(5, 4) * (Qv[0][i] + Qv[2][i]))
              for i in range(5)]
    check("S4.4 [NC-4: SO(16)/D8 GLUE] classes {0, 2} only, the "
          "completion supplies only w_2 = 2: total = (5/4) Tr_so16 "
          "X^4 = %s keeps T5 = 20, T3 = -40 (exact) -- no Okubo "
          "square, the KILL branch fires for so16 (E8 doubly "
          "special; v516 S4.3 replication)" % fmt(so_tot),
          so_tot == [15, 30, 45, 20, -40]
          and so_tot[3] == 20 and so_tot[4] == -40)

    dets_f = {1: 2 * I, 2: sp.Integer(4), 3: -2 * I}
    ab_f = [sp.nsimplify(sp.expand((1 - I ** (-j)) ** 2))
            for j in (1, 2, 3)]
    zeta_f = [sp.nsimplify(4 * sp.sin(sp.pi * R(j, 4)) ** 2)
              for j in (1, 2, 3)]
    mismatch = [ab_f[idx] != zeta_f[idx] for idx in (0, 2)]
    arg_bad = sp.arg(sp.expand((1 - I) ** 2))
    wf = [sp.nsimplify(sp.expand(
        sum((1 - I ** (j * m)) / dets_f[j] for j in (1, 2, 3))))
        for m in range(4)]
    Af = [sp.nsimplify(sp.expand(
        sum(Qtw[j][i] / dets_f[j] for j in (1, 2, 3))))
        for i in range(5)]
    check("S4.5 [NC-5: diag(i, i)] AB denominators %s = (2i, 4, -2i) "
          "COMPLEX; the zeta = AB identity FAILS in the odd sectors "
          "(real %s vs complex): %s -- the agreement of routes (i) "
          "and (ii) REQUIRES the SU(2) conjugation pairing; no real "
          "Quillen section (arg((1-i)^2) = %s = -pi/2 /= 0); fake "
          "weights %s = (0, -1/2, 0, 3/2) with w_1 /= w_3 (pairing "
          "broken, Q_1 = Q_3 demands equal weights); skeleton "
          "degenerates to %s = A_2 (v516 S4.4 replication)"
          % (fmt(ab_f), fmt(zeta_f), all(mismatch), arg_bad,
             fmt(wf), fmt(Af)),
          ab_f == [2 * I, 4, -2 * I] and all(mismatch)
          and arg_bad == -sp.pi / 2
          and wf == [0, R(-1, 2), 0, R(3, 2)] and wf[1] != wf[3]
          and Af == [-3, -6, 9, 8, -16])

    ok_k = True
    rows = {}
    for k in (3, 5):
        dets_k, wm, ded, prd, ch2k, zeta_ok = cyclo_data(k)
        wexp = {m: R(m * (k - m), 2) for m in range(1, k)}
        hk = {m: R(m * (k - m), 2 * k) for m in range(1, k)}
        ok_w = all(sp.expand(wm[m] - wexp[m]) == 0 for m in range(1, k))
        ok_h = all(wexp[m] == k * hk[m]
                   and wexp[m] == -k * ch2k[m - 1] for m in range(1, k))
        ok_ded = sp.expand(ded - R(k * k - 1, 12)) == 0
        ok_prd = sp.expand(prd - k * k) == 0
        rows[k] = (fmt([wexp[m] for m in range(1, k)]), ok_w, ok_h,
                   ok_ded, ok_prd, zeta_ok)
        if not (ok_w and ok_h and ok_ded and ok_prd and zeta_ok):
            ok_k = False
    check("S4.6 [NC-6: k = 3, 5 ORBIFOLDS -- WEIGHTS WANDER] exact in "
          "Q[x]/Phi_k: w_m^{(k)} = sum_j (1-z^{jm})/det_j^{(k)} = "
          "m(k-m)/2 = k h_m^{(k)} = -k ch2(T_m^{(A_{k-1})}) (k = 3: "
          "w = %s; k = 5: w = %s); Dedekind sum = (k^2-1)/12 and "
          "prod det_j = k^2 both exact; zeta dets 4 sin^2(pi j/k) = "
          "AB dets per j: the constructive weight moves correctly "
          "with the centre count (cf. v517 S5.3) -- only k = 4 = "
          "|mu4| carries the E8-glue chain of S3"
          % (rows[3][0], rows[5][0]), ok_k)
    NC = bool(w1 == [0, R(5, 8), 1, R(5, 8)] and tot1[3] == 2
              and not w2[1].is_rational and tot2_t3 != 0
              and tot2 == [9, 18, 9, 0, 0]
              and so_tot == [15, 30, 45, 20, -40]
              and all(mismatch) and wf[1] != wf[3] and ok_k)
    return NC


# ---------------------------------------------------------------------------
# S5 -- verdict per the preregistration
# ---------------------------------------------------------------------------
def section5(R1, R2, R3, NC):
    print("  -- S5: verdict per the preregistered branches")
    erfolg = bool(R1 and R2 and R3 and NC)
    if erfolg:
        verdict = (
            "ERFOLG: the w_m normalisation is DERIVED constructively "
            "at probe level -- (route i) the 1/det_j contact weight "
            "is the Abel/Cesaro-regularised g^j-character of the "
            "fibre mode ledger (exact in Q(i): closed form matched "
            "at every order, Abel value (1/2, 1/4, 1/2), fixed-point "
            "factor split off EXACTLY at every truncation level for "
            "the phased AND the v520-forced unphased trace, so "
            "contact_j = (Q^{(0)} - Q^{(j)})/det_j is COMPUTED); "
            "(route ii) the zeta determinant of the twisted fibre "
            "Laplacian is det_j exactly (Lerch/reflection exact + "
            "30-digit Hurwitz certificates), the Quillen split "
            "det Delta = det_j^2 has the unique real positive "
            "holomorphic section det_j (SU(2) conjugation pairing), "
            "and the delta-1f modular blocks carry the constant term "
            "1/det_b verbatim; (route iii) the derived weight "
            "reproduces the v516 chain number by number (w = "
            "(0, 3/2, 2, 3/2) = 4h = -4ch2, T5 = 0 for any c, 4:3, "
            "c = 4 = |mu4|, per-sector Okubo squares (18, 9, 18), "
            "total 45<x,x>^2, Phi/psi certificates +-64).  All "
            "negative controls behave (1/det^2 and 1/|1-i^j| break "
            "the chain quantifiably, Z2/EH anchor passes with scale "
            "2 = |Z2|, so16 kill fires, diag(i,i) breaks the "
            "zeta = AB identity itself, k = 3/5 weights wander "
            "correctly).  The v516 [C] 'completion reading' plus "
            "this derivation leaves NOTHING in w_m declared at probe "
            "level -- under the typed premises TP-REG, TP-Q, TP-NUM, "
            "TP-CH.  NO marker moves from this sandbox; any upgrade "
            "goes through the regular promotion workflow.")
    elif R1 and R2 and not R3:
        verdict = (
            "UNENTSCHIEDEN (named gap): both constructive routes "
            "deliver 1/det_j but the v516 chain is not reproduced -- "
            "the gap sits in the chain bookkeeping, not the weight.")
    elif not (R1 and R2):
        verdict = (
            "KILL-CANDIDATE / UNENTSCHIEDEN: a constructive route "
            "failed to deliver 1/det_j (R1 = %s, R2 = %s) -- see the "
            "failed checks above; if a route delivered a DIFFERENT "
            "normalisation, the preregistered KILL fires."
            % (R1, R2))
    else:
        verdict = (
            "UNENTSCHIEDEN: fires R1 = %s, R2 = %s, R3 = %s, "
            "controls = %s -- see the failed checks above."
            % (R1, R2, R3, NC))
    check("S5.1 [VERDICT: %s]" % verdict, True)
    check("S5.2 [HONEST BOOKKEEPING + FENCES] exact = mode ledgers "
          "and closed forms in Q(i), Abel values, tensor-trace "
          "splitting, reflection-formula zeta determinants, Quillen "
          "arithmetic, delta-1f block constant terms (Gaussian-"
          "rational series), the full v516 chain, all controls "
          "(Q(sqrt2)/Q(i)/cyclotomic Q[x]/Phi_k); numeric "
          "(documented) = Hurwitz/Lerch certificates and stripped "
          "block limits (mpmath dps 40, devs printed).  TYPED "
          "PREMISES carried: TP-REG (Abel/Cesaro/zeta regularisation "
          "= the equivariant character), TP-Q (Quillen structure of "
          "BCOV F1, = v520 TP-4), TP-NUM (unphased numerator = the "
          "v520 ERFOLG-A decision layer under its TP-1..TP-4), TP-CH "
          "(insertion channel computes the box-channel weight, the "
          "shared v516/v518 scaffold).  WHAT STAYS OPEN: the GLOBAL "
          "BCOV integral on PT/Z4 beyond the fibre zero-mode factor "
          "(the tau-integrated dressing lives in the v518/v520 "
          "scaffold and is not re-derived here); the resolved-ALE "
          "(v514/v517) instanton route not built; SEAM.EQUIV."
          "TWISTOR.01 untouched; v516's ledger markers move ONLY "
          "through the regular promotion workflow", True)
    print("     VERDICT: %s" % verdict)
    return erfolg


# ---------------------------------------------------------------------------
def run():
    print("WP5e-wm probe: the constructive BCOV derivation of the w_m "
          "normalisation (CELEST.SEAM.01; exploration only)")
    print("  [building E8 glue roots + exact class quartics ...]")
    Qv, Qtw, Afix = section0()
    R1, contact, skel = section1(Qv, Qtw)
    R2 = section2()
    R3, h = section3(Qv, Qtw, Afix, contact, skel)
    NC = section4(Qv, Qtw, Afix, h)
    section5(R1, R2, R3, NC)

    print("")
    print("CHECKS: %d passed, %d failed" % (N_PASS, N_FAIL))
    return N_FAIL == 0


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
