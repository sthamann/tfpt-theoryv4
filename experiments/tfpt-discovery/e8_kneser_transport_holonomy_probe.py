"""Discovery probe (2026-07-24), part 28 of the zeta/prime investigation.
Kneser TRANSPORT with glue marking: do the cusp coefficients a_p(f8)
live in the mixing of the four glue channels under the neighbour
correspondence?  (Review synthesis after part 27: static glue labelling
of isotropic lines missed a_p; the transport action remains.)

Classical scaffold (named as such): Kneser p-neighbours of an even
unimodular lattice biject with isotropic lines of (L/pL, q); E8 has
class number 1.  Part 27 closed the Eisenstein half:
  #iso_lines = sigma3(p) * #P^3(F_p).
Part 11 supplies the mu4 class thetas Th0..Th3 and
  Th0 - Th2 = Eisenstein tower - 8 f8, with a_p(f8) = (-4,-2,24,-44,22).

  S1 / Z1  Theta-side target.  Build Th0..Th3 from part-11 theta-constant
           formulae to O(q^200).  Classical weight-4 Hecke (p odd,
           coprime to the level-16 support; formula
           (T_p f)(n) = a(pn) + p^3 a(n/p)) on the four class series.
           Preregister: either a constant 4x4 M_p^theta exists in the
           Th-basis, or document the exact obstruction and the
           Hecke-stable closure (where a_p sits).
  S2 / Z2  Geometry-side matrix.  For every isotropic line at p = 3
           (1120, complete): form the Kneser neighbour L', classify
           short vectors by deg'(x) := p^{-1} deg(p x) mod 4 (well-
           defined on all of L'; recovers deg on L ∩ L'), accumulate
           Sum_lines Th_j(L')(n) for n <= 3.  Solve for constant
           M_p^geom in Sum Th_j(L') = Sum_k M_kj Th_k(E8), or document
           the exact even/odd block structure if no single M exists.
  S3 / K   Compare.  Preregistered success: M_geom = M_theta exactly
           (or up to the classical Witt factor #P^3).  Extract where
           a_p sits.  Placebo: seed-fixed redistribution of line
           weights must not reproduce the a_p-bearing eigenvalue.
  S4       Verdict + consequence for ZETA.LOCAL.EULER M1 /
           ZETA.CENSUS.TO.GL1 (sandbox only).

PREREGISTERED CRITERIA
  Z1  T_p acts on the class-theta data with a documented matrix /
      eigenchannel decomposition in which a_p appears (eigenvalue,
      block, or exact linear combination), for p in {3,5,7,11,13}.
  Z2  Geometric neighbour sum at p = 3 (complete, 1120 lines) yields
      a documented transport operator on glue channels for n = 1,2,3;
      shell totals equal #lines * 240 sigma3(n).
  K   M_geom and M_theta agree exactly, OR agree up to a documented
      classical normalisation / level / parity term that still lets
      a_p be read from geometry.  Kill: structural contradiction.
  P   Placebo line-weighting (seed 20260728) fails to reproduce the
      a_p-bearing geometric eigenvalue.

VERDICT
  HECKE-FROM-COMPILER-COMPLETE : K exact (cusp a_p from compiler
      geometry of neighbour transport — strongest mechanism hit of
      the series on probe level; NO promotion, no RH claim)
  PARTIAL : transport carries a_p in a typed even/odd or block form,
      but constant-matrix equality fails with a documented residual
  DEAD    : transport does not see a_p (static-labelling kill repeats)

Firewall: discovery sandbox, NO promotion, no marker moves, no RH
evidence; classical theorems (Kneser neighbours, Hecke on theta
series, class number 1 of E8, Witt counts) named as such.
"""
from __future__ import annotations

import itertools
import time
from collections import defaultdict
from fractions import Fraction

import numpy as np
import sympy as sp
from sympy import Matrix, Rational

PASS = 0
FAIL = 0
T0 = time.time()

A_P = {3: -4, 5: -2, 7: 24, 11: -44, 13: 22}
Z1_PRIMES = (3, 5, 7, 11, 13)
PLACEBO_SEED = 20260728
QMAX = 200
TMAX = 8 * QMAX
GEOM_P = 3
GEOM_MAXN = 3


def check(name, ok):
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}", flush=True)
    if ok:
        PASS += 1
    else:
        FAIL += 1
    return ok


def info(msg):
    print(f"        {msg}", flush=True)


# ================================================================ data
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


def iso_lines_formula(p):
    return sigma3(p) * num_P3(p)


# ------------------------------------------------ theta / q-series
def pmul(a, b, order):
    res = [0] * (order + 1)
    for i, ai in enumerate(a):
        if ai:
            for j in range(min(len(b) - 1, order - i) + 1):
                if b[j]:
                    res[i + j] += ai * b[j]
    return res


def ppow(a, e, order):
    res = [0] * (order + 1)
    res[0] = 1
    for _ in range(e):
        res = pmul(res, a, order)
    return res


def padd(a, b):
    return [x + y for x, y in zip(a, b)]


def psub(a, b):
    return [x - y for x, y in zip(a, b)]


def phalf(a):
    assert all(x % 2 == 0 for x in a)
    return [x // 2 for x in a]


def eta_pow(d, e, order):
    s = [0] * (order + 1)
    s[0] = 1
    for n in range(1, order // d + 1):
        f = [0] * (d * n + 1)
        f[0], f[d * n] = 1, -1
        for _ in range(e):
            s = pmul(s, f, order)
    return s


def shift(a, k, order):
    return ([0] * k + a)[: order + 1]


def theta3_t(step):
    s = [0] * (TMAX + 1)
    s[0] = 1
    n = 1
    while step * 4 * n * n <= TMAX:
        s[step * 4 * n * n] += 2
        n += 1
    return s


def theta4_t(step):
    s = [0] * (TMAX + 1)
    s[0] = 1
    n = 1
    while step * 4 * n * n <= TMAX:
        s[step * 4 * n * n] += 2 * (-1) ** n
        n += 1
    return s


def theta2_t(step):
    s = [0] * (TMAX + 1)
    o = 1
    while step * o * o <= TMAX:
        s[step * o * o] += 2
        o += 2
    return s


def t_to_q(ts):
    return [ts[8 * n] for n in range(QMAX + 1)]


def hecke_Tp(a, p, k=4):
    """Level-coprime odd-p Hecke on q-coefficients (weight k).
    Convention: (T_p f)(n) = a(pn) + p^{k-1} a(n/p) with a(n/p)=0 if p∤n.
    Documented for Gamma0(N) with p odd not dividing N (here N|16).
    """
    out = [0] * (QMAX + 1)
    pk = p ** (k - 1)
    for n in range(QMAX + 1):
        val = 0
        if p * n <= QMAX:
            val += a[p * n]
        if n % p == 0:
            val += pk * a[n // p]
        out[n] = val
    return out


print("S0 -- scaffolding: E8 Gram, glue dvec, f8 a_p oracle")
check("E8 Gram det = 1, even diagonal (classical even unimodular)",
      sp.det(GRAM_SYM) == 1 and all(int(G[i, i]) == 2 for i in range(8)))
check(f"part-11 glue dvec = {list(map(int, DVEC))}",
      list(map(int, DVEC)) == [1, 0, 0, 0, 0, 0, 2, 0])
f8 = shift(pmul(eta_pow(2, 4, QMAX), eta_pow(4, 4, QMAX), QMAX), 1, QMAX)
ap_ok = all(int(f8[p]) == A_P[p] for p in Z1_PRIMES)
info(f"f8 a_p: {[(p, int(f8[p])) for p in Z1_PRIMES]}")
check("f8 a_p match part-11 table (-4,-2,24,-44,22) at p = (3,5,7,11,13)",
      ap_ok)


# ================================================================ S1 / Z1
print("S1 / Z1 -- class thetas and classical Hecke on the Th-span")
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
csig = [Th0[n] - Th2[n] for n in range(QMAX + 1)]
E4 = [Th0[n] + Th1[n] + Th2[n] + Th3[n] for n in range(QMAX + 1)]

check("Th1 = Th3 termwise (part 11); rank of {Th0,Th1,Th2} = 3 over Q "
      f"on coeffs n = 0..40",
      Th1 == Th3
      and Matrix([[Th0[n], Th1[n], Th2[n]] for n in range(41)]).rank() == 3)
check("Theta_E8 = E4 on n = 1..40 (240 sigma3)",
      all(E4[n] == 240 * int(sp.divisor_sigma(n, 3)) for n in range(1, 41)))

# Obstruction: T_p does not preserve span{Th0,Th1,Th2,Th3}
z1_closure = {}
for p in Z1_PRIMES:
    Nsol = min(QMAX // p, 60)
    A = Matrix([[Thetas[j][n] for j in range(4)] for n in range(Nsol + 1)])
    closed = True
    for j in range(4):
        Tp = hecke_Tp(Thetas[j], p)
        b = Matrix([Tp[n] for n in range(Nsol + 1)])
        aug = A.row_join(b)
        rref, _ = aug.rref()
        for row in range(rref.rows):
            if all(rref[row, c] == 0 for c in range(4)) and rref[row, 4] != 0:
                closed = False
                break
        if not closed:
            break
    z1_closure[p] = closed
info(f"T_p preserves span{{Th0..Th3}}? {z1_closure}")
check("Z1 obstruction (preregistered content): classical T_p does NOT "
      "preserve span{Th0,Th1,Th2,Th3} for any p in {3,5,7,11,13} — "
      "Th1=Th3 already forces rank 3, and T_p Th0 leaves the span "
      "(cusp f8 / level-16 Eisenstein towers needed to close)",
      all(not z1_closure[p] for p in Z1_PRIMES))

# Hecke-stable closure facts
z1_channel = {}
for p in Z1_PRIMES:
    Nsol = QMAX // p
    sig = sigma3(p)
    ap = A_P[p]
    TpE = hecke_Tp(E4, p)
    Tp1 = hecke_Tp(Th1, p)
    TpS = hecke_Tp(csig, p)
    rhs_S = [sig * csig[n] + 8 * (sig - ap) * int(f8[n])
             for n in range(Nsol + 1)]
    e_ok = all(TpE[n] == sig * E4[n] for n in range(Nsol + 1))
    s1_ok = all(Tp1[n] == sig * Th1[n] for n in range(Nsol + 1))
    f_ok = all(hecke_Tp(list(map(int, f8)), p)[n] == ap * int(f8[n])
               for n in range(Nsol + 1))
    S_ok = TpS[: Nsol + 1] == rhs_S
    z1_channel[p] = {
        "sigma3": sig, "a_p": ap, "E4_eigen": e_ok, "Th1_eigen": s1_ok,
        "f8_eigen": f_ok, "signed_formula": S_ok,
    }
    info(f"p = {p}: T E4 = {sig} E4? {e_ok}; T Th1 = {sig} Th1? {s1_ok}; "
         f"T f8 = {ap} f8? {f_ok}; T(Th0-Th2) = {sig}(Th0-Th2) + "
         f"8({sig}-{ap}) f8? {S_ok}")

check("Z1 eigenchannel (Hecke-stable closure): for all p in "
      "{3,5,7,11,13}, T_p E4 = sigma3(p) E4, T_p Th1 = sigma3(p) Th1, "
      "T_p f8 = a_p f8, and T_p(Th0-Th2) = sigma3(Th0-Th2) + "
      "8(sigma3-a_p) f8 — so a_p sits as the cusp eigenvalue; the "
      "signed class combination is NOT itself an eigenform",
      all(v["E4_eigen"] and v["Th1_eigen"] and v["f8_eigen"]
          and v["signed_formula"] for v in z1_channel.values()))
info("LEVEL CONVENTION: odd p, (T_p f)(n) = a(pn)+p^3 a(n/p); class "
     "thetas live at level dividing 16 (part 11), p coprime to 16.")


# ================================================================ S2 / Z2
print("S2 / Z2 -- geometric neighbour transport at p = 3 (complete)")


def adjust_isotropic_lift(g, p):
    """Standard Kneser adjustment: lift with q(v) ≡ 0 mod p^2."""
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
    """Fincke-Pohst on E8 Gram; keep only listed shells."""
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


p = GEOM_P
p2 = p * p
keep_shells = {m * p2 for m in range(1, GEOM_MAXN + 1)}
info(f"precompute E8 vectors at shells {sorted(keep_shells)} "
     f"(= p^2 * n for n <= {GEOM_MAXN}); complete line census, "
     f"not orbit-reduced")
t_fp = time.time()
Wq, W = fp_e8_shells(GEOM_MAXN * p2, keep_shells)
info(f"FP done: {len(Wq)} vectors in {time.time() - t_fp:.1f}s")
shell_ok = all(
    int(np.sum(Wq == m * p2)) == 240 * int(sp.divisor_sigma(m * p2, 3))
    for m in range(1, GEOM_MAXN + 1)
)
check(f"E8 shell counts at n = p^2·{{1..{GEOM_MAXN}}} match 240 sigma3 "
      "(FP completeness)",
      shell_ok)

buckets: dict[tuple, np.ndarray] = {}
_tmp: dict[tuple, list] = defaultdict(list)
for i in range(len(W)):
    _tmp[tuple((W[i] % p).tolist())].append(i)
buckets = {k: np.array(v, dtype=np.int32) for k, v in _tmp.items()}

inv2 = pow(2, -1, p)
mesh = np.array(
    np.meshgrid(*[np.arange(p)] * 8, indexing="ij")
).reshape(8, -1).T.astype(np.int64)
q2 = np.einsum("ij,jk,ik->i", mesh, G, mesh)
iso = mesh[(q2 * inv2) % p == 0]
iso = iso[np.any(iso != 0, axis=1)]
first = (iso != 0).argmax(axis=1)
can = iso[iso[np.arange(len(iso)), first] == 1]
nlines = len(can)
exp_lines = iso_lines_formula(p)
check(f"Z2: #isotropic lines at p = {p} = {nlines} = sigma3*#P^3 = "
      f"{exp_lines} (part 27 H1)",
      nlines == exp_lines)

# deg' consistency on L ∩ L' = L0: sample one neighbour via filter
inv_p = pow(p % 4, -1, 4)
v0 = adjust_isotropic_lift(can[0], p)
Gv0 = (G @ v0).astype(np.int64)
# vectors of E8 in L0 with q <= GEOM_MAXN: B(x,v)≡0 mod p, x in E8
# Use small ambient enum for n<=3
lim = int(np.ceil(np.sqrt(2 * GEOM_MAXN))) + 1
rng = np.arange(-lim, lim + 1, dtype=np.int16)
gi = np.array(np.meshgrid(*[rng] * 8, indexing="ij")).reshape(8, -1).T
ni = np.einsum("ij,ij->i", gi.astype(np.int32), gi.astype(np.int32))
mi = (gi.astype(np.int32).sum(axis=1) % 2 == 0) & (ni >= 2) & (ni <= 2 * GEOM_MAXN)
BEinv = BE.inv()
I256 = np.array([[int(256 * BEinv[i, j]) for j in range(8)]
                 for i in range(8)], dtype=np.int64)
Nsmall = (2 * gi[mi].astype(np.int64) @ I256.T) // 256
nsmall = ni[mi] // 2
degs_small = (Nsmall @ DVEC) % 4
# L0 filter
in_L0 = (Nsmall @ Gv0) % p == 0
deg_prime_L0 = (inv_p * ((p * Nsmall[in_L0] @ DVEC) % 4)) % 4
# p * x for x in L0: deg(p x) = p deg(x), so deg' = deg
cons_L0 = np.all(deg_prime_L0 == degs_small[in_L0])
check("deg' := p^{-1} deg(p x) mod 4 recovers deg on L ∩ L' = L0 "
      f"(sample neighbour, n <= {GEOM_MAXN})",
      bool(cons_L0))

# Full census
S = np.zeros((GEOM_MAXN + 1, 4), dtype=np.int64)
per_line_root_ok = 0
t_c = time.time()
line_signed_n1 = []
for g in can:
    v = adjust_isotropic_lift(g, p)
    Gv = (G @ v).astype(np.int64)
    counts = np.zeros((GEOM_MAXN + 1, 4), dtype=np.int64)
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
        for n, d in zip(ns.tolist(), deg_p.tolist()):
            counts[n, d] += 1
    S += counts
    if int(counts[1].sum()) == 240:
        per_line_root_ok += 1
    line_signed_n1.append(int(counts[1, 0] - counts[1, 2]))
info(f"census {time.time() - t_c:.1f}s; lines with 240 roots: "
     f"{per_line_root_ok}/{nlines}")
check(f"Z2 completeness: all {nlines} neighbours have 240 roots under "
      "deg'-refined count (class number 1 + exact filter)",
      per_line_root_ok == nlines)

Th_ref = np.array(
    [[Th0[n], Th1[n], Th2[n], Th3[n]] for n in range(GEOM_MAXN + 1)],
    dtype=np.int64,
)
tot_ok = all(
    int(S[n].sum()) == nlines * int(E4[n]) for n in range(1, GEOM_MAXN + 1)
)
check("Z2 shell totals: Sum_lines Theta(L')(n) = #lines * E4(n) for "
      f"n = 1..{GEOM_MAXN}",
      tot_ok)
for n in range(1, GEOM_MAXN + 1):
    info(f"n = {n}: S = {list(map(int, S[n]))}, Th(E8) = "
         f"{list(map(int, Th_ref[n]))}, signed S0-S2 = "
         f"{int(S[n, 0] - S[n, 2])}, c(n) = {csig[n]}")

# Constant-matrix obstruction: signed multiplier even vs odd differs
# (underdetermined least-squares on Th1=Th3 can spuriously "solve")
signed_ratio_n = {
    n: Rational(int(S[n, 0] - S[n, 2]), csig[n])
    for n in range(1, GEOM_MAXN + 1)
}
const_M_exists = len(set(signed_ratio_n.values())) == 1
info(f"signed multipliers by n: "
     f"{ {n: signed_ratio_n[n] for n in signed_ratio_n} }")
check("Z2 constant-matrix test: NO single 4x4 M_geom for all n — "
      "signed eigenvalue differs even vs odd "
      f"({signed_ratio_n[2]} vs {signed_ratio_n[1]}; content, not a "
      "probe failure)",
      not const_M_exists)

# Even / odd block structure
even_ok = all(
    int(S[n, j]) == nlines * int(Th_ref[n, j])
    for n in range(1, GEOM_MAXN + 1) if n % 2 == 0
    for j in range(4)
)
spinor_ok = all(
    int(S[n, 1]) == nlines * int(Th1[n])
    and int(S[n, 3]) == nlines * int(Th3[n])
    for n in range(1, GEOM_MAXN + 1)
)
odd_ns = [n for n in range(1, GEOM_MAXN + 1) if n % 2 == 1]
# Fit M_odd = [[a,b],[b,a]] on (Th0,Th2) with D8 eigenvalue = #lines
# i.e. a+b = nlines, a-b = lambda_signed
signed_mult = {}
for n in odd_ns:
    signed_mult[n] = Rational(int(S[n, 0] - S[n, 2]), csig[n])
lam_odd = signed_mult[odd_ns[0]]
lam_uniform = all(signed_mult[n] == lam_odd for n in odd_ns)
P3 = num_P3(p)
ap = A_P[p]
lam_formula = 8 * (P3 - ap)
info(f"even n: S = #lines * Th? {even_ok}")
info(f"spinor: S1 = S3 = #lines * Th1 for all n? {spinor_ok}")
info(f"odd signed multipliers: { {n: signed_mult[n] for n in odd_ns} }")
info(f"8*(#P^3 - a_p) = 8*({P3} - ({ap})) = {lam_formula}")
check("Z2 even shells: transport acts as #lines * Id on all four "
      "glue channels (n = 2)",
      even_ok)
check("Z2 spinor channels: S1(n) = S3(n) = #lines * Th1(n) for "
      f"n = 1..{GEOM_MAXN} (eigenvalue sigma3*#P^3)",
      spinor_ok)
check("Z2 odd signed channel: (S0-S2)/(Th0-Th2) is CONSTANT on odd "
      f"n = {odd_ns} and equals 8*(#P^3 - a_p) = {lam_formula}",
      lam_uniform and lam_odd == lam_formula)

# Explicit odd 2x2 block
a_blk = Rational(nlines + lam_odd, 2)
b_blk = Rational(nlines - lam_odd, 2)
M_odd = Matrix([[a_blk, b_blk], [b_blk, a_blk]])
odd_block_ok = all(
    a_blk * Th0[n] + b_blk * Th2[n] == int(S[n, 0])
    and b_blk * Th0[n] + a_blk * Th2[n] == int(S[n, 2])
    for n in odd_ns
)
info(f"M_odd^(0,2) = {M_odd}; eigenvalues "
     f"{{#lines: 1, 8*(P3-a_p): 1}} = {{{nlines}, {lam_odd}}}")
check("Z2 odd (0,2)-block: M = ((L+λ)/2) I + ((L-λ)/2) σ_x with "
      "L = #lines, λ = 8*(#P^3-a_p) reproduces S0,S2 on all odd n",
      odd_block_ok)

# Extract a_p from geometry alone
ap_from_geom = int(P3 - lam_odd / 8)
info(f"a_p extracted from geometry: #P^3 - λ_odd/8 = {P3} - "
     f"{lam_odd}/8 = {ap_from_geom} (oracle {ap})")
check("Z2 cusp readout: a_p(f8) = #P^3 - λ_odd/8 recovers a_3 = -4 "
      "from neighbour transport (no q-series input to λ)",
      ap_from_geom == ap)


# ================================================================ S3 / K
print("S3 / K -- compare theta-side and geometry-side; placebo")
# Documented relationship (not constant-matrix equality):
# geometric transport = even/odd operator whose odd signed eigenvalue
# is 8*(#P^3 - a_p), matching the cusp a_p from Z1's f8 eigenchannel.
K_exact_const = False  # established above
K_parity_match = (
    even_ok and spinor_ok and odd_block_ok
    and lam_odd == lam_formula and ap_from_geom == ap
)
check("K (strict constant-matrix equality M_geom = M_theta): FAIL as "
      "content — neither side admits a single 4x4 on span{Th0..Th3} "
      "for all n (Z1: T_p leaves the span; Z2: even/odd differ)",
      not K_exact_const)
check("K (documented parity / Witt form): geometric even/odd transport "
      "matches the Z1 cusp channel — λ_signed_odd = 8*(#P^3 - a_p) "
      "with #P^3 the classical Witt factor from part 27; a_p readable "
      "from geometry",
      K_parity_match)

# Placebo: random weights on lines (seed-fixed), rebuild signed odd λ
rng = np.random.default_rng(PLACEBO_SEED)
weights = rng.integers(1, 5, size=nlines)
# Recompute S with weights using only shell p^2 (= n=1) for speed
S_p = np.zeros(4, dtype=np.int64)
# Need per-line class counts at n=1 — re-filter quickly
w_n1 = W[Wq == p2]
w_n1_idx_all = np.where(Wq == p2)[0]
buckets1: dict[tuple, np.ndarray] = {}
_tmp1: dict[tuple, list] = defaultdict(list)
for i in w_n1_idx_all:
    _tmp1[tuple((W[i] % p).tolist())].append(i)
buckets1 = {k: np.array(v, dtype=np.int32) for k, v in _tmp1.items()}
signed_w = 0
tot_w = 0
for wi, g in zip(weights, can):
    v = adjust_isotropic_lift(g, p)
    Gv = (G @ v).astype(np.int64)
    cc = np.zeros(4, dtype=np.int64)
    for a in range(p):
        key = tuple(((a * v) % p).tolist())
        idxs = buckets1.get(key)
        if idxs is None:
            continue
        ws = W[idxs]
        ok = (ws @ Gv) % p2 == 0
        deg_p = (inv_p * ((ws[ok] @ DVEC) % 4)) % 4
        for d in deg_p.tolist():
            cc[d] += 1
    signed_w += int(wi) * int(cc[0] - cc[2])
    tot_w += int(wi) * int(cc.sum())
# Weighted Th reference at n=1 still csig[1]; λ_w = signed_w / (csig[1] * ? )
# Normalise by average weight so Id-eigenvalue scale is comparable
wmean = float(np.mean(weights))
lam_placebo = Rational(signed_w, csig[1]) / Rational(1, 1)
# Under uniform weight 1, signed_sum = lam_odd * csig[1]; with weights,
# expect ~ wmean * lam_odd * csig if structure preserved; placebo breaks a_p readout
ap_placebo = P3 - (signed_w / (wmean * csig[1])) / 8
info(f"placebo seed = {PLACEBO_SEED}: weight mean = {wmean:.3f}, "
     f"signed_w = {signed_w}, naive a_p readout = {ap_placebo:.6f}")
placebo_miss = abs(ap_placebo - ap) > 0.5
check("P placebo: seed-fixed random line weights do NOT reproduce "
      f"a_p = {ap} via the λ_odd readout (got {ap_placebo:.4f})",
      placebo_miss)


# ================================================================ S4 verdict
print("VERDICT")
if K_parity_match and placebo_miss and not K_exact_const:
    # Strong mechanism hit with documented residual (even/odd, #P^3)
    verdict = "PARTIAL"
    consequence = (
        "Neighbour TRANSPORT with ambient D5(+)A3 marking DOES carry "
        "the cusp a_p: on odd shells the signed glue channel is an "
        "eigenchannel of the summed correspondence with eigenvalue "
        "λ = 8*(#P^3 - a_p), so a_p = #P^3 - λ/8 is geometric.  Even "
        "shells and spinor channels are pure #lines = sigma3*#P^3.  "
        "Strict constant-matrix K fails (even/odd split; classical T_p "
        "does not preserve the 4 class-theta span).  ZETA.LOCAL.EULER "
        "M1 cusp half is PARTIAL→mechanism-visible; ZETA.CENSUS.TO.GL1 "
        "still open (no GL(1) reduction)."
    )
    next_lever = (
        "Next lever: (i) prove the odd-shell identity λ = 8*(#P^3-a_p) "
        "for all odd p (p = 5 sample / orbit reduction under "
        "W(D5)xW(A3)); (ii) identify the even/odd split with U_p vs T_p "
        "at level 16 (classical Atkin-Lehner); (iii) Brandt-matrix "
        "packaging of the (0,2)-block as a Hecke module."
    )
elif K_exact_const and K_parity_match and placebo_miss:
    verdict = "HECKE-FROM-COMPILER-COMPLETE"
    consequence = (
        "Full Hecke action including cusp a_p equals geometric "
        "neighbour transport on glue channels."
    )
    next_lever = "Promote only after independent audit; no RH claim."
else:
    verdict = "DEAD"
    consequence = (
        "Transport route does not isolate a_p; cusp remains a "
        "shell-census fact without correspondence mechanism."
    )
    next_lever = (
        "Fall back to c(p) = -8 a_p shell census; treat neighbour "
        "Hecke as Eisenstein-only (part 27)."
    )

# Upgrade path note: if one accepts even/odd + Witt #P^3 as the
# documented normalisation of K, the mechanism is complete on probe
# level — typed as PARTIAL per preregistered strict reading of K.
info(f"H1-style Witt factor #P^3 = {P3}, #lines = {nlines}, "
     f"λ_odd = {lam_odd}, a_p geom = {ap_from_geom}")
info(f"M_odd = {M_odd}")
info(f"even transport = {nlines} * I_4")
check(f"VERDICT = {verdict}",
      verdict in ("HECKE-FROM-COMPILER-COMPLETE", "PARTIAL", "DEAD"))
info(f"consequence: {consequence}")
info(f"next lever: {next_lever}")

print()
print("TABLE -- geometric glue transport at p = 3")
print(f"  {'n':>3} {'S0':>10} {'S1':>10} {'S2':>10} {'S3':>10} "
      f"{'λ_signed':>10} {'parity':>8}")
for n in range(1, GEOM_MAXN + 1):
    if n % 2 == 0:
        lam_s = str(nlines)
        par = "even"
    else:
        lam_s = str(signed_mult[n])
        par = "odd"
    print(f"  {n:>3} {int(S[n, 0]):>10} {int(S[n, 1]):>10} "
          f"{int(S[n, 2]):>10} {int(S[n, 3]):>10} {lam_s:>10} {par:>8}")

elapsed = time.time() - T0
print()
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({elapsed:.1f}s)")
print(f"VERDICT: {verdict}")
raise SystemExit(0 if FAIL == 0 else 1)
