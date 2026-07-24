"""v535 -- HECKE.GEOM.01: Hecke from geometry on the E8 census channels.
The Hecke structure of the mu4-glue census is lattice-native:
Kneser p-neighbour correspondence + affine neighbour-sum operator
+ 2-adic oldform recovery.  Consolidated from discovery T27/T31/T32.

[E] (A) KNESER CORRESPONDENCE CARRIES HECKE (T27 H1).  For the even
    unimodular E8, isotropic points/lines of (E8/pE8, q=|·|^2/2):
        #iso_pts  = p^7 + p^4 - p^3
        #iso_lines = sigma3(p) * #P^3(F_p) = (1+p^3)*(p^4-1)/(p-1)
    identically (symbolic) and by full enumeration at p = 2,3,5,7
    (135 / 1120 / 19656 / 137600 lines).  The Eisenstein eigenvalue
    sigma3(p) = 1+p^3 of the trivial census channel is an exact factor
    of a lattice-native correspondence count.
[E] (B) MARKED NEIGHBOUR-SUM IS AN AFFINE HECKE ELEMENT (T31).
    nu_p Theta_j(n) := sum_{isotropic lines ell} Th_j(L'_ell)(n)
    equals a(p) Id + b(p) T_p exactly (overdetermined, residual 0):
        b = sigma3(p) + a_p,   a = #lines - b*sigma3(p)
    with cusp rule a_p = b - sigma3(p).  Live orbit-reduced census
    at p = 3 (shell n = 1) recovers (a,b) = (448, 24) => a_3 = -4;
    p = 5 uses the T31-validated orbit-reduced S[1] block
    (25 orbits, lambda_odd = 3784) => (a,b) = (4032, 124) => a_5 = -2;
    p = 7 consistency via lambda_odd = #lines - sigma3^2 + a_p^2
    (= 19840) and #lines = 137600 (profiling, not full re-enumeration).
    Placebo (seed-falsified deg' permutation) fails the true (a,b).
[E] (C) CENSUS REDUNDANCY = 2-ADIC OLDFORM STRUCTURE (T32).
    dim_Q V = 7 = 5 (E4-copies at levels 1,2,4,8,16) + 2 (f8-copies
    at levels 8,16); every Th_j is an explicit Q-linear combination;
    recovery projectors pi_cusp = (28 - T_3)/32, pi_Eis = (T_3 + 4)/32,
    newform via (1 - V_2 U_2); new quotients each dim 1; level census
    purely 2-adic (no odd-prime level).

HONEST FENCES (load-bearing typing):
  * Classical theorems (Kneser neighbours, class number 1 of E8,
    weight-4 Hecke, Atkin-Lehner oldforms, multiplicity one) are
    classical -- the claim is the IN-SUITE MECHANICS: correspondence
    -> operator -> a_p as output; redundancy = mu4/2-adic glue.
  * NO RH statement; no archimedean / GL(1) claim.
  * p = 7 is consistency (lambda identity + line count), not full
    geometric re-enumeration; p = 5 geometric S[1] is frozen from
    the validated T31 orbit-reduced census (algebraic A1/A4 live).
  * Weight-4 restriction: both new systems are weight 4
    (L = zeta(s)zeta(s-3) and L(f8,s)); the GL(1)/weight-drop
    transport (ZETA.CENSUS.TO.GL1) stays OPEN -- named, not claimed.
  * NO marker upgrades of any pre-existing contract.

Status: [E] exact integer / Rational / sympy identities + live p=3
geometry; [C] p=5 geometric block as T31-validated freeze; [O] the
weight-4 -> GL(1) step.  Python; Wolfram-mirrored (exact count
identities, (a,b)/lambda laws, dim-7 / projector arithmetic -- the
p=3 FP census and q-series builds stay Python-only), counted per
GATE.WOLFRAM.02.  Discovery provenance:
  experiments/tfpt-discovery/e8_pneighbor_hecke_probe.py (T27)
  experiments/tfpt-discovery/e8_neighbor_operator_decomposition_probe.py (T31)
  experiments/tfpt-discovery/census_newform_recovery_probe.py (T32)
  (+ theta scaffolding from e8_glue_chi4_signed_theta_probe.py, T11)
"""
from __future__ import annotations

import itertools
import time
from fractions import Fraction

import numpy as np
import sympy as sp
from sympy import Matrix, Rational

from tfpt_constants import check, summary, reset

A_P = {3: -4, 5: -2, 7: 24, 11: -44, 13: 22}
H1_PRIMES = (2, 3, 5, 7)
PLACEBO_SEED = 20260731
QMAX = 200
# Coefficient window for Hecke identities: need p*CHK <= QMAX (p=3 => CHK<=66).
CHK = 60
TMAX = 8 * QMAX

# T31-validated p=5 orbit-reduced S[1] (25 orbits; lambda_odd = 3784).
# Live re-enumeration of the FP shell at norm 25 is ~100 s; frozen here
# with algebraic A1/A4 checks live.  Provenance: T31 probe 2026-07-24.
S5_N1_FROZEN = (1085600, 1257984, 1115872, 1257984)
P7_PROFILE = {"nlines": 137600, "lam_odd": 19840}


# ---------------------------------------------------------------- helpers
def col(v):
    return [2 * x for x in v]


E8_BASIS = [
    [1, -1, -1, -1, -1, -1, -1, 1],
    col([1, 1, 0, 0, 0, 0, 0, 0]), col([-1, 1, 0, 0, 0, 0, 0, 0]),
    col([0, -1, 1, 0, 0, 0, 0, 0]), col([0, 0, -1, 1, 0, 0, 0, 0]),
    col([0, 0, 0, -1, 1, 0, 0, 0]), col([0, 0, 0, 0, -1, 1, 0, 0]),
    col([0, 0, 0, 0, 0, -1, 1, 0]),
]
L0_BASIS = [
    col([1, -1, 0, 0, 0, 0, 0, 0]), col([0, 1, -1, 0, 0, 0, 0, 0]),
    col([0, 0, 1, -1, 0, 0, 0, 0]), col([0, 0, 0, 1, -1, 0, 0, 0]),
    col([0, 0, 0, 1, 1, 0, 0, 0]),
    col([0, 0, 0, 0, 0, 1, -1, 0]), col([0, 0, 0, 0, 0, 0, 1, -1]),
    col([0, 0, 0, 0, 0, 1, 1, 0]),
]

BE = Matrix(E8_BASIS).T
GRAM_SYM = (BE.T * BE) / 4
G = np.array([[int(GRAM_SYM[i, j]) for j in range(8)] for i in range(8)],
             dtype=np.int64)
BE_np = np.array([[int(BE[i, j]) for j in range(8)] for i in range(8)],
                 dtype=np.int64)
detBE = int(sp.det(BE))
BEinv = BE.inv()
Adj = np.array(
    [[int(sp.Integer(sp.simplify(BEinv[i, j] * detBE))) for j in range(8)]
     for i in range(8)],
    dtype=np.int64,
)
BL = Matrix(L0_BASIS).T
FMAP = (BE.solve(BL)).inv() * BE.inv()

_roots2 = []
for i in range(8):
    for j in range(i + 1, 8):
        for si, sj in itertools.product((2, -2), repeat=2):
            v = [0] * 8
            v[i], v[j] = si, sj
            _roots2.append(tuple(v))
for signs in itertools.product((1, -1), repeat=8):
    if signs.count(-1) % 2 == 0:
        _roots2.append(signs)
assert len(_roots2) == 240


def _glue_frac2(v2):
    fr = FMAP * Matrix(list(v2))
    return tuple(Fraction(sp.Rational(e).p, sp.Rational(e).q) % 1
                 for e in fr)


_g1 = _glue_frac2(_roots2[112])
_classes = {tuple((k * c) % 1 for c in _g1): k for k in range(4)}
DVEC = np.array(
    [_classes[_glue_frac2([BE[j, i] for j in range(8)])] for i in range(8)],
    dtype=np.int64,
)


def sigma3(p):
    return 1 + p ** 3


def num_P3(p):
    return (p ** 4 - 1) // (p - 1)


def iso_points_formula(p):
    return p ** 7 + p ** 4 - p ** 3


def iso_lines_formula(p):
    return sigma3(p) * num_P3(p)


def predicted_law(p, ap=None):
    if ap is None:
        ap = A_P[p]
    sig = sigma3(p)
    L = iso_lines_formula(p)
    b = sig + ap
    a = L - b * sig
    lam = L - sig ** 2 + ap ** 2
    return {"L": L, "sig": sig, "ap": ap, "a": a, "b": b, "lam": lam,
            "a_blk": Rational(L + lam, 2), "b_blk": Rational(L - lam, 2)}


# ---------------------------------------------------------------- series
def zeros(order):
    return [0] * (order + 1)


def pmul(a, b, order):
    aa = np.array(a[: order + 1], dtype=object)
    bb = np.array(b[: order + 1], dtype=object)
    return list(np.convolve(aa, bb)[: order + 1])


def ppow(a, e, order):
    res = zeros(order)
    res[0] = 1
    for _ in range(e):
        res = pmul(res, a, order)
    return res


def padd(a, b):
    return [x + y for x, y in zip(a, b)]


def psub(a, b):
    return [x - y for x, y in zip(a, b)]


def phalf(a):
    assert all(int(x) % 2 == 0 for x in a)
    return [int(x) // 2 for x in a]


def eta_pow(d, e, order):
    s = zeros(order)
    s[0] = 1
    for n in range(1, order // d + 1):
        f = [0] * (d * n + 1)
        f[0], f[d * n] = 1, -1
        for _ in range(e):
            s = pmul(s, f, order)
    return s


def shift(a, k, order):
    return ([0] * k + list(a))[: order + 1]


def V_d(f, d, order=None):
    N = order if order is not None else len(f) - 1
    out = zeros(N)
    for n, c in enumerate(f):
        if n * d <= N:
            out[n * d] = c
    return out


def U_p(f, p, order=None):
    N = order if order is not None else len(f) - 1
    out = zeros(N)
    for n in range(N // p + 1):
        out[n] = f[p * n]
    return out


def hecke_Tp(f, p, k=4, out_order=None):
    N = len(f) - 1
    M = out_order if out_order is not None else N // p
    out = zeros(M)
    pk = p ** (k - 1)
    for n in range(M + 1):
        term = f[p * n] if p * n <= N else 0
        if n % p == 0:
            term = term + pk * f[n // p]
        out[n] = term
    return out


def series_eq(a, b, upto):
    return all(Rational(a[n]) == Rational(b[n]) for n in range(upto + 1))


def scale(c, f):
    return [Rational(c) * Rational(x) for x in f]


def sadd(*fs):
    N = min(len(f) for f in fs) - 1
    out = [Rational(0)] * (N + 1)
    for f in fs:
        for n in range(N + 1):
            out[n] += Rational(f[n])
    return out


def qentry(x):
    if isinstance(x, Rational):
        return x
    if isinstance(x, Fraction):
        return Rational(x.numerator, x.denominator)
    return Rational(sp.nsimplify(x))


# ---------------------------------------------------------------- geometry
def count_isotropic_points(p, batch_prefix=None):
    if batch_prefix is None:
        batch_prefix = 8 if p <= 3 else 5
    inv2 = pow(2, -1, p) if p > 2 else None
    bp = batch_prefix
    mesh = np.array(
        np.meshgrid(*[np.arange(p)] * bp, indexing="ij")
    ).reshape(bp, -1).T.astype(np.int64)
    n_iso = 0
    outers = (itertools.product(range(p), repeat=8 - bp)
              if bp < 8 else [()])
    for outer in outers:
        X = np.empty((mesh.shape[0], 8), dtype=np.int64)
        X[:, :bp] = mesh
        if bp < 8:
            X[:, bp:] = outer
        q2 = np.einsum("ij,jk,ik->i", X, G, X)
        if p == 2:
            n_iso += int(np.sum((q2 // 2) % 2 == 0))
        else:
            n_iso += int(np.sum((q2 * inv2) % p == 0))
    return n_iso


def signed_perms_Dn(n):
    out = []
    for perm in itertools.permutations(range(n)):
        for bits in range(2 ** n):
            signs = [1 if ((bits >> i) & 1) == 0 else -1 for i in range(n)]
            if signs.count(-1) % 2 != 0:
                continue
            out.append((perm, tuple(signs)))
    return out


WD5 = signed_perms_Dn(5)
WA3 = signed_perms_Dn(3)


def apply_weyl_ambient(v, d5, a3):
    perm5, s5 = d5
    perm3, s3 = a3
    out = np.zeros(8, dtype=np.int64)
    for i in range(5):
        out[i] = s5[i] * v[perm5[i]]
    for i in range(3):
        out[5 + i] = s3[i] * v[5 + perm3[i]]
    return out


def canon_line(c, p):
    c = np.asarray(c, dtype=np.int64) % p
    for i in range(8):
        if int(c[i]) % p != 0:
            inv = pow(int(c[i]) % p, -1, p)
            return tuple((int(x) * inv) % p for x in c)
    return tuple(0 for _ in range(8))


def coeff_from_ambient(amb, p):
    return ((Adj @ amb) * pow(detBE % p, -1, p)) % p


def ambient_from_coeff(c, p):
    return (BE_np @ c) % p


def weyl_mats(p):
    eye = np.eye(8, dtype=np.int64)
    mats = []
    for d5 in WD5:
        for a3 in WA3:
            cols = [
                coeff_from_ambient(
                    apply_weyl_ambient(ambient_from_coeff(eye[:, j], p),
                                       d5, a3), p
                )
                for j in range(8)
            ]
            mats.append(np.stack(cols, axis=1) % p)
    return np.stack(mats, axis=0)


def isotropic_lines(p):
    inv2 = pow(2, -1, p)
    mesh = np.array(
        np.meshgrid(*[np.arange(p)] * 8, indexing="ij")
    ).reshape(8, -1).T.astype(np.int64)
    q2 = np.einsum("ij,jk,ik->i", mesh, G, mesh)
    iso = mesh[(q2 * inv2) % p == 0]
    iso = iso[np.any(iso != 0, axis=1)]
    first = (iso != 0).argmax(axis=1)
    return iso[iso[np.arange(len(iso)), first] == 1]


def orbit_reps(p, mats):
    can = isotropic_lines(p)
    unvis = {canon_line(c, p): c.copy() for c in can}
    keys = set(unvis)
    orbs = []
    while keys:
        k0 = next(iter(keys))
        c0 = unvis[k0]
        orb = {canon_line(img, p) for img in (mats @ c0) % p}
        for kk in orb:
            keys.discard(kk)
        orbs.append((c0, len(orb)))
    return orbs, len(can)


def adjust_isotropic_lift(g, p):
    v = g.astype(np.int64).copy()
    q = int(v @ G @ v) // 2
    assert q % p == 0
    t = q // p
    if t % p == 0:
        return v
    Gv = G @ v
    i0 = next(i for i in range(8) if int(Gv[i]) % p != 0)
    s = (t * pow(int(Gv[i0]) % p, -1, p)) % p
    w = np.zeros(8, dtype=np.int64)
    w[i0] = 1
    v_new = v - p * s * w
    assert int(v_new @ G @ v_new) // 2 % (p * p) == 0
    return v_new


def fp_e8_shells(max_q, keep):
    U = np.linalg.cholesky(G.astype(np.float64)).T
    bound = float(2 * max_q)
    n = 8
    x = np.zeros(n)
    out_q = []
    out_c = []

    def go(k, right):
        if k < 0:
            ci = np.rint(x).astype(np.int64)
            qn = int(ci @ G @ ci) // 2
            if qn in keep:
                out_q.append(qn)
                out_c.append(ci.copy())
            return
        s = 0.0
        for j in range(k + 1, n):
            s += U[k, j] * x[j]
        ukk = U[k, k]
        thr = np.sqrt(max(0.0, right))
        lo = (-thr - s) / ukk
        hi = (thr - s) / ukk
        if lo > hi:
            lo, hi = hi, lo
        for xk in range(int(np.floor(lo)), int(np.ceil(hi)) + 1):
            x[k] = xk
            term = ukk * xk + s
            go(k - 1, right - term * term)
        x[k] = 0

    go(n - 1, bound)
    return np.array(out_q, dtype=np.int32), np.array(out_c, dtype=np.int64)


def build_buckets(W, p):
    Wp = (W % p).astype(np.int64)
    key = np.zeros(len(W), dtype=np.int64)
    mul = 1
    for j in range(8):
        key += Wp[:, j] * mul
        mul *= p
    order = np.argsort(key, kind="mergesort")
    key_s = key[order]
    breaks = np.flatnonzero(np.diff(key_s)) + 1
    starts = np.concatenate(([0], breaks))
    ends = np.concatenate((breaks, [len(key_s)]))
    buckets = {}
    for s, e in zip(starts.tolist(), ends.tolist()):
        idxs = order[s:e].astype(np.int32)
        rep = tuple(Wp[idxs[0]].tolist())
        buckets[rep] = idxs
    return buckets


def census_orbit(p, maxn, orbs, deg_perm=None):
    p2 = p * p
    keep = {m * p2 for m in range(1, maxn + 1)}
    Wq, W = fp_e8_shells(maxn * p2, keep)
    buckets = build_buckets(W, p)
    inv_p = pow(p % 4, -1, 4)
    S = np.zeros((maxn + 1, 4), dtype=np.int64)
    root_ok = 0
    for g, osz in orbs:
        v = adjust_isotropic_lift(np.asarray(g, dtype=np.int64), p)
        Gv = (G @ v).astype(np.int64)
        counts = np.zeros((maxn + 1, 4), dtype=np.int64)
        for a in range(p):
            key = tuple(((a * v) % p).tolist())
            idxs = buckets.get(key)
            if idxs is None:
                continue
            ws = W[idxs]
            ok = (ws @ Gv) % p2 == 0
            ws = ws[ok]
            qs = Wq[idxs[ok]]
            ns = qs // p2
            deg_p = (inv_p * ((ws @ DVEC) % 4)) % 4
            if deg_perm is not None:
                deg_p = np.array([deg_perm[int(d)] for d in deg_p],
                                 dtype=np.int64)
            for n_val in range(1, maxn + 1):
                mask = ns == n_val
                if not np.any(mask):
                    continue
                bc = np.bincount(deg_p[mask], minlength=4)
                counts[n_val] += bc[:4]
        S += osz * counts
        if int(counts[1].sum()) == 240:
            root_ok += 1
    return S, root_ok


def solve_ab_from_two(r1, r2):
    _, _, th1, tp1, rhs1 = r1
    _, _, th2, tp2, rhs2 = r2
    M = Matrix([[th1, tp1], [th2, tp2]])
    if M.det() == 0:
        return None
    sol = M.solve(Matrix([rhs1, rhs2]))
    return Rational(sol[0]), Rational(sol[1])


def verify_ab(rows, a, b):
    fails = []
    for n, j, th, tp, rhs in rows:
        if a * th + b * tp - rhs != 0:
            fails.append((n, j))
    return len(fails) == 0, len(fails)


def fit_ab_overdetermined(rows):
    for i in range(len(rows)):
        for k in range(i + 1, len(rows)):
            sol = solve_ab_from_two(rows[i], rows[k])
            if sol is None:
                continue
            a, b = sol
            ok, n_fail = verify_ab(rows, a, b)
            return {"a": a, "b": b, "ok": ok, "n_fail": n_fail,
                    "n_eq": len(rows)}
    return {"a": None, "b": None, "ok": False, "n_fail": len(rows),
            "n_eq": len(rows)}


def collect_eqs(p, S, Thetas, ns):
    Tp = [hecke_Tp(Thetas[j], p, out_order=QMAX) for j in range(4)]
    rows = []
    for n in ns:
        for j in range(4):
            rows.append((n, j, int(Thetas[j][n]), int(Tp[j][n]),
                         int(S[n, j])))
    return rows


# ======================================================================
def run():
    reset()
    t0 = time.time()
    print("v535 HECKE.GEOM.01 -- Hecke from geometry (Kneser + affine "
          "neighbour-sum + 2-adic oldform recovery)")

    # ============================================================ S0
    print("S0 -- E8 Gram, glue dvec, class thetas, f8")
    check("E8 Gram: det = 1, even diagonal (classical even unimodular)",
          sp.det(GRAM_SYM) == 1 and all(int(G[i, i]) == 2 for i in range(8)))
    check(f"part-11 glue dvec = {list(map(int, DVEC))}",
          list(map(int, DVEC)) == [1, 0, 0, 0, 0, 0, 2, 0])

    def theta3_t(step):
        s = zeros(TMAX)
        s[0] = 1
        n = 1
        while step * 4 * n * n <= TMAX:
            s[step * 4 * n * n] += 2
            n += 1
        return s

    def theta4_t(step):
        s = zeros(TMAX)
        s[0] = 1
        n = 1
        while step * 4 * n * n <= TMAX:
            s[step * 4 * n * n] += 2 * ((-1) ** n)
            n += 1
        return s

    def theta2_t(step):
        s = zeros(TMAX)
        o = 1
        while step * o * o <= TMAX:
            s[step * o * o] += 2
            o += 2
        return s

    def t_to_q(ts):
        return [int(ts[8 * n]) for n in range(QMAX + 1)]

    th3, th4, th2 = theta3_t(1), theta4_t(1), theta2_t(1)
    D5p = phalf(padd(ppow(th3, 5, TMAX), ppow(th4, 5, TMAX)))
    D5m = phalf(psub(ppow(th3, 5, TMAX), ppow(th4, 5, TMAX)))
    A3p = phalf(padd(ppow(th3, 3, TMAX), ppow(th4, 3, TMAX)))
    A3m = phalf(psub(ppow(th3, 3, TMAX), ppow(th4, 3, TMAX)))
    Th0 = t_to_q(pmul(D5p, A3p, TMAX))
    Th2 = t_to_q(pmul(D5m, A3m, TMAX))
    Th1 = t_to_q([x // 4 for x in ppow(th2, 8, TMAX)])
    Th3 = list(Th1)
    Thetas = [Th0, Th1, Th2, Th3]
    Tot = [Th0[n] + Th1[n] + Th2[n] + Th3[n] for n in range(QMAX + 1)]
    Sig = [Th0[n] - Th2[n] for n in range(QMAX + 1)]
    sig3 = [0] + [int(sp.divisor_sigma(n, 3)) for n in range(1, QMAX + 1)]
    E4 = [1] + [240 * sig3[n] for n in range(1, QMAX + 1)]
    f8 = shift(pmul(eta_pow(2, 4, QMAX), eta_pow(4, 4, QMAX), QMAX), 1, QMAX)
    check("class thetas: Th1 = Th3; Tot = E4; head (52,64,60,64); "
          "f8 a_p = (-4,-2,24) at p = 3,5,7",
          Th1 == Th3 and Tot == E4
          and (Th0[1], Th1[1], Th2[1], Th3[1]) == (52, 64, 60, 64)
          and all(int(f8[p]) == A_P[p] for p in (3, 5, 7)))

    # ============================================================ A
    print("A -- Kneser correspondence carries Hecke (T27 H1)")
    p_sym = sp.symbols("p", integer=True, positive=True)
    Npts_sym = p_sym ** 7 + p_sym ** 4 - p_sym ** 3
    Nlines_sym = sp.simplify((Npts_sym - 1) / (p_sym - 1))
    factor_id = sp.simplify(
        Nlines_sym - (1 + p_sym ** 3) * (p_sym ** 4 - 1) / (p_sym - 1)
    )
    factored = sp.factor(Nlines_sym)
    check("H1 symbolic: #iso_lines = (1+p^3)*(p^4-1)/(p-1) identically "
          "(= (p+1)^2 (p^2+1)(p^2-p+1))",
          factor_id == 0
          and factored == (p_sym + 1) ** 2 * (p_sym ** 2 + 1)
          * (p_sym ** 2 - p_sym + 1))

    iso_pts = {}
    iso_lines = {}
    for p in H1_PRIMES:
        n = count_isotropic_points(p)
        lines = (n - 1) // (p - 1)
        iso_pts[p] = n
        iso_lines[p] = lines
        print(f"        p = {p}: #iso_pts = {n}, #iso_lines = {lines}")
    check("H1 enumeration: #iso_pts = p^7+p^4-p^3 at p = 2,3,5,7 "
          f"(got {[iso_pts[p] for p in H1_PRIMES]})",
          all(iso_pts[p] == iso_points_formula(p) for p in H1_PRIMES))
    check("H1 enumeration: #iso_lines = sigma3(p)*#P^3 = "
          "(135,1120,19656,137600) at p = 2,3,5,7",
          all(iso_lines[p] == iso_lines_formula(p) for p in H1_PRIMES)
          and [iso_lines[p] for p in H1_PRIMES]
          == [135, 1120, 19656, 137600])

    # ============================================================ B
    print("B -- marked neighbour-sum = affine Hecke element (T31)")
    mats3 = weyl_mats(3)
    orbs3, nlines3 = orbit_reps(3, mats3)
    check(f"p=3 orbit partition: {len(orbs3)} orbits, sum sizes = "
          f"#lines = {nlines3} = 1120",
          sum(s for _, s in orbs3) == nlines3 == iso_lines_formula(3) == 1120)

    S3, root_ok3 = census_orbit(3, 1, orbs3)
    csig1 = Sig[1]
    lam3 = Rational(int(S3[1, 0] - S3[1, 2]), csig1)
    a_blk3 = Rational(nlines3 + lam3, 2)
    b_blk3 = Rational(nlines3 - lam3, 2)
    print(f"        p=3 S[1]={list(map(int, S3[1]))}; "
          f"lambda_odd={lam3}; block [[{a_blk3},{b_blk3}],...]")
    check("p=3 census: all orbit reps have 240 roots at n=1; "
          "Sum_j S_j(1) = #lines * E4(1)",
          root_ok3 == len(orbs3)
          and int(S3[1].sum()) == nlines3 * int(E4[1]))
    check("p=3 V3 anchors: lambda_odd = 352; odd (0,2)-block "
          "[[736,384],[384,736]]; spinor S1 = S3 = 1120*64",
          lam3 == 352 and a_blk3 == 736 and b_blk3 == 384
          and int(S3[1, 1]) == nlines3 * 64
          and int(S3[1, 3]) == nlines3 * 64)

    rows3 = collect_eqs(3, S3, Thetas, [1])
    fit3 = fit_ab_overdetermined(rows3)
    law3 = predicted_law(3)
    print(f"        p=3 A1 fit: a={fit3['a']}, b={fit3['b']} "
          f"(law {law3['a']},{law3['b']})")
    check("A1 p=3: nu_3 = a Id + b T_3 with (a,b)=(448,24) exactly "
          "(4 eqs, residual 0)",
          fit3["ok"] and fit3["a"] == 448 and fit3["b"] == 24
          and fit3["a"] == law3["a"] and fit3["b"] == law3["b"])
    check("A4 p=3: cusp rule a_3 = b - sigma3(3) = 24 - 28 = -4",
          fit3["b"] - sigma3(3) == -4 == A_P[3])

    # p=5: frozen geometric S[1], live algebraic fit
    S5 = np.zeros((2, 4), dtype=np.int64)
    S5[1] = S5_N1_FROZEN
    nlines5 = iso_lines_formula(5)
    lam5 = Rational(int(S5[1, 0] - S5[1, 2]), csig1)
    law5 = predicted_law(5)
    rows5 = collect_eqs(5, S5, Thetas, [1])
    fit5 = fit_ab_overdetermined(rows5)
    print(f"        p=5 (frozen S[1]) lambda={lam5}; "
          f"fit a={fit5['a']}, b={fit5['b']}")
    check("A1 p=5 (T31-validated freeze): lambda_odd = 3784; "
          "(a,b)=(4032,124) exactly on n=1 x 4 classes",
          lam5 == 3784 and fit5["ok"]
          and fit5["a"] == 4032 and fit5["b"] == 124
          and fit5["a"] == law5["a"] and fit5["b"] == law5["b"])
    check("A4 p=5: a_5 = b - sigma3(5) = 124 - 126 = -2",
          fit5["b"] - sigma3(5) == -2 == A_P[5])

    # closed-form lambda identity + p=7 consistency
    check("C: lambda_odd = L - sigma3^2 + a_p^2 at p=3,5 "
          f"(352, 3784)",
          lam3 == law3["lam"] and lam5 == law5["lam"]
          and law3["lam"] == 352 and law5["lam"] == 3784)
    law7 = predicted_law(7)
    check("C p=7 consistency (not full enum): #lines = 137600; "
          "lambda_odd = L - sigma3^2 + a_7^2 = 19840; "
          "|a_7| = 24 from disc",
          law7["L"] == P7_PROFILE["nlines"]
          and law7["lam"] == P7_PROFILE["lam_odd"] == 19840
          and sp.integer_nthroot(
              int(sigma3(7) ** 2 - (law7["L"] - law7["lam"])), 2
          ) == (24, True))

    # Eisenstein normalisation a + b sigma3 = L
    check("A1 normalisation: a + b*sigma3 = #lines at p=3,5 "
          "(Tot/Sp eigenchannel)",
          fit3["a"] + fit3["b"] * sigma3(3) == nlines3
          and fit5["a"] + fit5["b"] * sigma3(5) == nlines5)

    # placebo
    rng = np.random.default_rng(PLACEBO_SEED)
    perm = list(range(4))
    while perm == list(range(4)):
        rng.shuffle(perm)
    S3_fake, _ = census_orbit(3, 1, orbs3, deg_perm=perm)
    fit_fake = fit_ab_overdetermined(collect_eqs(3, S3_fake, Thetas, [1]))
    ap_fake = (fit_fake["b"] - sigma3(3)
               if fit_fake["b"] is not None else None)
    placebo_bad = (
        (not fit_fake["ok"])
        or (fit_fake["a"], fit_fake["b"]) != (fit3["a"], fit3["b"])
        or ap_fake != A_P[3]
    )
    print(f"        placebo perm={perm}: a={fit_fake['a']}, "
          f"b={fit_fake['b']}, ap={ap_fake}")
    check("P placebo: falsified deg' does NOT reproduce "
          "(a,b)=(448,24) with a_3=-4",
          placebo_bad)

    # ============================================================ C
    print("C -- census redundancy = 2-adic oldform structure (T32)")
    E4_LEVELS = (1, 2, 4, 8, 16)
    F8_LEVELS = (1, 2)

    def E4d(d):
        return [1] + [
            240 * sig3[n // d] if n % d == 0 else 0
            for n in range(1, QMAX + 1)
        ]

    f8_q2 = V_d(f8, 2)
    basis_names = [f"E4(q^{d})" for d in E4_LEVELS] + [
        f"f8(q^{e})" for e in F8_LEVELS
    ]
    basis = [E4d(d) for d in E4_LEVELS] + [V_d(f8, e) for e in F8_LEVELS]
    N_BASIS = 7

    def rank_of(series_list, upto=CHK):
        A = Matrix([[qentry(s[n]) for s in series_list]
                    for n in range(upto + 1)])
        return int(A.rank())

    def expand_in_basis(f, upto=CHK):
        A = Matrix([[qentry(basis[j][n]) for j in range(N_BASIS)]
                    for n in range(upto + 1)])
        b = Matrix([qentry(f[n]) for n in range(upto + 1)])
        sol, params = A.gauss_jordan_solve(b)
        if params:
            sol = sol.subs({p: 0 for p in params})
        coords = [qentry(sol[j]) for j in range(N_BASIS)]
        recon = [
            sum(coords[j] * qentry(basis[j][n]) for j in range(N_BASIS))
            for n in range(QMAX + 1)
        ]
        ok = all(qentry(f[n]) == recon[n] for n in range(QMAX + 1))
        return coords, ok

    EXPECTED = {
        "Th0": [Rational(7, 30), Rational(3, 10), Rational(-3, 5),
                Rational(16, 15), Rational(0), Rational(-4), Rational(0)],
        "Th1": [Rational(4, 15), Rational(-4, 15), Rational(0),
                Rational(0), Rational(0), Rational(0), Rational(0)],
        "Th2": [Rational(7, 30), Rational(7, 30), Rational(3, 5),
                Rational(-16, 15), Rational(0), Rational(4), Rational(0)],
        "Th3": [Rational(4, 15), Rational(-4, 15), Rational(0),
                Rational(0), Rational(0), Rational(0), Rational(0)],
    }
    th_ok = True
    for name, series in (("Th0", Th0), ("Th1", Th1),
                         ("Th2", Th2), ("Th3", Th3)):
        coords, ok = expand_in_basis(series)
        th_ok = th_ok and ok and coords == EXPECTED[name]
    dim_gens = rank_of(basis)
    dim_V = rank_of([Th0, Th1, Th2, Th3] + basis)
    check("N1: dim_Q V = 7; Th_j = exact Q-linear combos of "
          "E4(q^d)_{d|16} + f8(q^e)_{e|2} "
          "(Th1 = (4/15)(E4 - E4(q^2)); generators independent)",
          th_ok and dim_V == 7 == dim_gens)

    dim_eis = rank_of([E4d(d) for d in E4_LEVELS])
    dim_cusp = rank_of([V_d(f8, e) for e in F8_LEVELS])
    check("N2: V = direct sum of E4-oldclass (5 copies, levels 1..16) "
          "+ f8-oldclass (2 copies, levels 8,16); no collisions",
          dim_eis == 5 and dim_cusp == 2
          and rank_of(basis) == 7)

    def is_eigen(f, p, lam, upto):
        Tf = hecke_Tp(f, p, out_order=upto)
        return all(Rational(Tf[n]) == Rational(lam) * Rational(f[n])
                   for n in range(upto + 1))

    eig_ok = (all(is_eigen(E4d(d), 3, 28, CHK) for d in E4_LEVELS)
              and all(is_eigen(V_d(f8, e), 3, -4, CHK) for e in F8_LEVELS))
    T3 = Matrix.diag(28, 28, 28, 28, 28, -4, -4)
    dim28 = len((T3 - 28 * sp.eye(7)).nullspace())
    dim_m4 = len((T3 + 4 * sp.eye(7)).nullspace())
    check("N3: T_3 = diag(28 x5, -4 x2); ker(T_3-28) dim 5; "
          "ker(T_3+4) dim 2; new quotients each dim 1",
          eig_ok and dim28 == 5 and dim_m4 == 2
          and (dim_eis - rank_of([E4d(d) for d in E4_LEVELS if d > 1])
               == 1)
          and (dim_cusp - rank_of([V_d(f8, e) for e in F8_LEVELS if e > 1])
               == 1))

    pi_eis = (T3 + 4 * sp.eye(7)) / 32
    pi_cusp = (28 * sp.eye(7) - T3) / 32
    check("N4a: recovery projectors pi_Eis = (T_3+4)/32, "
          "pi_cusp = (28-T_3)/32 are complementary idempotents",
          pi_eis ** 2 == pi_eis and pi_cusp ** 2 == pi_cusp
          and pi_eis + pi_cusp == sp.eye(7)
          and pi_eis * pi_cusp == sp.zeros(7))

    # V2U2 matrix (exact oldform formulae, verified on basis)
    VU_cols = [
        [0, 9, -8, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
    ]
    VUmat = Matrix(N_BASIS, N_BASIS,
                   lambda r, c: Rational(VU_cols[c][r]))
    vu_ok = True
    for j, b in enumerate(basis):
        w = V_d(U_p(b, 2), 2)
        c, ok = expand_in_basis(w, upto=CHK)
        if (not ok) or [qentry(x) for x in c] != [
                qentry(x) for x in VU_cols[j]]:
            vu_ok = False
    pi_f8 = (sp.eye(7) - VUmat) * pi_cusp
    check("N4b: pi_f8 = (1 - V_2 U_2) o pi_cusp is idempotent rank 1 "
          "(image = Q·f8); V2U2 formulae exact on the 7-basis",
          vu_ok and pi_f8 ** 2 == pi_f8 and pi_f8.rank() == 1)

    def coords_of(f):
        c, ok = expand_in_basis(f, upto=CHK)
        assert ok
        return [qentry(x) for x in c]

    def apply_coords(M, coords):
        v = M * Matrix([qentry(c) for c in coords])
        return [qentry(v[j]) for j in range(N_BASIS)]

    def reconstruct(coords):
        return [
            sum(qentry(coords[j]) * qentry(basis[j][n])
                for j in range(N_BASIS))
            for n in range(QMAX + 1)
        ]

    def pi_E4_series(f):
        c_eis = apply_coords(pi_eis, coords_of(f))
        f_eis = reconstruct(c_eis)
        return scale(Rational(f_eis[1], 240), E4)

    def pi_f8_series(f):
        return reconstruct(apply_coords(pi_f8, coords_of(f)))

    check("N4c: recovery — pi_E4(Tot) = E4; pi_f8(Sig) = -8 f8; "
          "cross terms vanish (multiplicity 1 on each new system)",
          series_eq(pi_E4_series(Tot), E4, QMAX)
          and series_eq(pi_f8_series(Tot), zeros(QMAX), QMAX)
          and series_eq(pi_E4_series(Sig), zeros(QMAX), QMAX)
          and series_eq(pi_f8_series(Sig), scale(-8, f8), QMAX))

    levels_eis = list(E4_LEVELS)
    levels_cusp = [8 * e for e in F8_LEVELS]
    check("N4e: level census PURELY 2-ADIC — E4-levels {1,2,4,8,16}, "
          "f8-levels {8,16}; no odd-prime level "
          "(redundancy = mu4/glue-sided)",
          set(levels_eis) == {1, 2, 4, 8, 16}
          and set(levels_cusp) == {8, 16}
          and all((L & (L - 1)) == 0 for L in levels_eis + levels_cusp))

    # Weight-4 fence (named open, not a failure): systems stay wt-4 eigenforms.
    check("FENCE [O named]: both new systems are weight 4 "
          "(E4 ~ zeta(s)zeta(s-3); f8 = eta(2)^4 eta(4)^4, level 8); "
          "GL(1)/weight-drop transport stays OPEN — no RH claim",
          is_eigen(E4, 3, 28, CHK) and is_eigen(f8, 3, -4, CHK)
          and f8[1] == 1 and E4[0] == 1
          and all(f8[n] == 0 for n in range(0, min(CHK, QMAX) + 1, 2)))

    elapsed = time.time() - t0
    print(f"        walltime {elapsed:.1f}s")
    return summary("HECKE.GEOM.01 Hecke from geometry")


if __name__ == "__main__":
    raise SystemExit(run())
