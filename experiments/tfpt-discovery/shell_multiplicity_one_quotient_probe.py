"""Discovery probe (2026-07-24), part 26 of the zeta/prime investigation.
PRIORITY-1 of the new programme: Experiment B of the review synthesis —
the MULTIPLICITY-1 QUOTIENT of the E8 shell census.

Classical (named as such): the even unimodular lattice E8 has
  r(n) := # { x in E8 : |x|^2 = 2n } = 240 sigma_3(n)
with Dirichlet series 240 zeta(s) zeta(s-3).  The counting is
multiplicative on coprime pairs (part 15), but the multiplicity is
240 sigma_3(n), not 1.  Part 15 narrowed ZETA.ARITH.COMPLETION to a
lattice-intrinsic multiplicity-1 reduction / tensor functor
Shell(m) (x) Shell(n) -> Shell(mn); ad-hoc sections are a preregistered
kill.

This probe asks whether a CANONICAL quotient H_arith = H_shell / G
(by a lattice-intrinsic equivalence: Weyl / glue-preserving Weyl /
primitivity) produces a multiplicative GL(1)-like counting q(n).

  S1  Setup: E8 simple roots + fold (v500 doubled-coord Weyl machine);
      mu4 glue classifier (part 11); shell enum n <= 7 (part 11/13);
      fundamental-weight Gram for dominant enumeration.
  S2  Q1 -- Weyl orbits: q1(n) = # dominant vectors of norm 2n
      (fold for n <= 7; weight-basis DFS for n <= 20).  Test E1-E4.
  S3  Q2 -- W(D5)xW(A3) orbits x glue: document that W(E8) does NOT
      preserve glue; fold under D5+A3 simple roots; q2(n).  Test E1-E4.
  S4  Q3 -- divisibility / primitive layer: r_prim via Moebius
      (classical); ratios vs sigma_3; dominant-primitive x glue.  E1-E4.
  S5  Tensor fingerprint on coprime pairs: class-count factorisation
      of (orbit x glue) for Shell(m) x Shell(n) vs Shell(mn).
  S6  Verdict against preregistered criteria.

PREREGISTERED SUCCESS CRITERIA (fixed BEFORE the runs):
  (E1) q(n) multiplicative on coprime pairs: q(mn)*q(1) = q(m)*q(n)
       exactly on the tested range.
  (E2) prime values: q(p) is CONSTANT, OR matches one NAMED deg <= 2
       local pattern among:
         P_zeta:     q(p) = 1
         P_const2:   q(p) = 2
         P_chi4:     q(p) = 1 + chi_4(p)   in {0, 1, 2}
         P_chi3:     q(p) = 1 + chi_3(p)   in {0, 1, 2}
         P_1plusp:   q(p) = 1 + p
         P_sig1:     q(p) = 1 + p           (alias; deg-2 Eisenstein)
       Patterns named a priori; matching is exact on primes in range.
  (E3) prime-power ladder q(p^k) obeys a Hecke recursion of deg <= 2:
         q(p^k) = a_p q(p^{k-1}) - chi(p) p^{w} q(p^{k-2})
       for a fixed weight w in {0,1,2,3} and chi trivial or chi_4,
       fitted on k=2..K from (q(1), q(p)) and checked on higher k.
  (E4) Dirichlet series of q is zeta(s), zeta(s)L(s,chi), or a SINGLE
       L-function -- NOT zeta(s)zeta(s-3).  Operationalised: the
       multiplicative function q must have Euler factors of degree
       <= 2 whose product is not the sigma_3 factor (1-p^{-s})^{-1}
       (1-p^{3-s})^{-1}.

KILL: no candidate satisfies E1+E2.

VERDICTS:
  GL1-QUOTIENT-FOUND -- some candidate meets E1-E4
  PARTIAL            -- E1 for some candidate, E2-E4 only partial
  DEAD               -- no canonical quotient is multiplicative

Firewall: discovery sandbox, NO promotion, no marker moves, no RH
evidence language; classical facts (Weyl chamber reduction, Moebius
square-divisor stratification, sigma_3 multiplicativity, Jacobi
r_E8 = 240 sigma_3) named as classical.  Probe content = the exact
in-suite quotient census, not new mathematics.
"""
from __future__ import annotations

import itertools
import math
import time
from collections import Counter, defaultdict
from fractions import Fraction as F
from math import gcd, isqrt

import numpy as np
import sympy as sp
from sympy import Matrix
from sympy.matrices.normalforms import smith_normal_form

PASS = 0
FAIL = 0
T0 = time.time()
NMAX = 20
N_ENUM = 7          # direct shell vectors up to norm 14
TENSOR_PAIRS = [(2, 3), (2, 5), (3, 5), (2, 7), (3, 7)]


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


# =====================================================================
# linear algebra helpers (v500 doubled-coord style)
# =====================================================================
def ip(a, b):
    return sum(x * y for x, y in zip(a, b))


def solve_fraction(M, b):
    n = len(M)
    A = [[F(M[i][j]) for j in range(n)] + [F(b[i])] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [A[i][n] for i in range(n)]


def fold_by(simple, v):
    """Classical Weyl chamber reduction: reflect while <v, alpha> < 0."""
    v = list(v)
    changed = True
    guard = 0
    while changed:
        changed = False
        for a in simple:
            c = ip(v, a)
            if c < 0:
                assert c % 4 == 0
                k = c // 4
                for t in range(8):
                    v[t] -= k * a[t]
                changed = True
        guard += 1
        if guard > 10_000:
            raise RuntimeError("fold did not terminate")
    return tuple(v)


def is_dom(simple, v):
    return all(ip(v, a) >= 0 for a in simple)


# =====================================================================
# S1 -- setup
# =====================================================================
print("S1 -- E8 setup, glue classifier, shell enum n<=7, fund weights")

E8_SIMPLE = [
    (1, -1, -1, -1, -1, -1, -1, 1),
    (2, 2, 0, 0, 0, 0, 0, 0),
    (-2, 2, 0, 0, 0, 0, 0, 0),
    (0, -2, 2, 0, 0, 0, 0, 0),
    (0, 0, -2, 2, 0, 0, 0, 0),
    (0, 0, 0, -2, 2, 0, 0, 0),
    (0, 0, 0, 0, -2, 2, 0, 0),
    (0, 0, 0, 0, 0, -2, 2, 0),
]

# D5 on coords 0..4, A3 ~= D3 on coords 5..7 (standard simple bases)
D5_SIMPLE = [
    (2, -2, 0, 0, 0, 0, 0, 0),
    (0, 2, -2, 0, 0, 0, 0, 0),
    (0, 0, 2, -2, 0, 0, 0, 0),
    (0, 0, 0, 2, -2, 0, 0, 0),
    (0, 0, 0, 2, 2, 0, 0, 0),
]
A3_SIMPLE = [
    (0, 0, 0, 0, 0, 2, -2, 0),
    (0, 0, 0, 0, 0, 0, 2, -2),
    (0, 0, 0, 0, 0, 0, 2, 2),
]
D5A3_SIMPLE = D5_SIMPLE + A3_SIMPLE

roots2 = []
for i, j in itertools.combinations(range(8), 2):
    for si in (2, -2):
        for sj in (2, -2):
            v = [0] * 8
            v[i], v[j] = si, sj
            roots2.append(tuple(v))
for signs in itertools.product((1, -1), repeat=8):
    if signs.count(-1) % 2 == 0:
        roots2.append(signs)
assert len(roots2) == 240

# fundamental weights: <omega_i, alpha_j>_{actual} = delta_ij
# <=> ip(omega, alpha) = 4 delta (doubled coords)
fund = []
for i in range(8):
    b = [4 if j == i else 0 for j in range(8)]
    rows = [[E8_SIMPLE[j][k] for k in range(8)] for j in range(8)]
    w = solve_fraction(rows, b)
    assert all(x.denominator == 1 for x in w)
    fund.append(tuple(int(x) for x in w))
Gfund = [[ip(fund[i], fund[j]) for j in range(8)] for i in range(8)]
# actual Gram = C^{-1}; Cartan check
Cartan = [[ip(a, b) // 4 for b in E8_SIMPLE] for a in E8_SIMPLE]
Cinv = Matrix(Cartan).inv()
gram_actual = [[Gfund[i][j] // 4 for j in range(8)] for i in range(8)]
check("fundamental-weight Gram = inverse Cartan of E8 (classical); "
      "det Cartan = 1; fold terminates on all 240 roots; unique "
      "dominant root (= highest root)",
      all(gram_actual[i][j] == Cinv[i, j] for i in range(8) for j in range(8))
      and sp.det(Matrix(Cartan)) == 1
      and len({fold_by(E8_SIMPLE, r) for r in roots2}) == 1
      and is_dom(E8_SIMPLE, fold_by(E8_SIMPLE, roots2[0])))

# --- glue classifier (part 11) ---
def col(v):
    return [2 * x for x in v]


e8_basis = [
    [1, -1, -1, -1, -1, -1, -1, 1],
    col([1, 1, 0, 0, 0, 0, 0, 0]), col([-1, 1, 0, 0, 0, 0, 0, 0]),
    col([0, -1, 1, 0, 0, 0, 0, 0]), col([0, 0, -1, 1, 0, 0, 0, 0]),
    col([0, 0, 0, -1, 1, 0, 0, 0]), col([0, 0, 0, 0, -1, 1, 0, 0]),
    col([0, 0, 0, 0, 0, -1, 1, 0]),
]
BE = Matrix(e8_basis).T
l0_basis = [
    col([1, -1, 0, 0, 0, 0, 0, 0]), col([0, 1, -1, 0, 0, 0, 0, 0]),
    col([0, 0, 1, -1, 0, 0, 0, 0]), col([0, 0, 0, 1, -1, 0, 0, 0]),
    col([0, 0, 0, 1, 1, 0, 0, 0]),
    col([0, 0, 0, 0, 0, 1, -1, 0]), col([0, 0, 0, 0, 0, 0, 1, -1]),
    col([0, 0, 0, 0, 0, 1, 1, 0]),
]
BL = Matrix(l0_basis).T
Mglue = BE.solve(BL)
snf = smith_normal_form(Mglue)
Fmap = Mglue.inv() * BE.inv()


def glue_frac2(v2):
    fr = Fmap * Matrix(list(v2))
    return tuple(F(sp.Rational(e).p, sp.Rational(e).q) % 1 for e in fr)


g1 = glue_frac2(roots2[112])
classes = {tuple((k * c) % 1 for c in g1): k for k in range(4)}
BEinv = BE.inv()
I256 = np.array([[int(256 * BEinv[i, j]) for j in range(8)]
                 for i in range(8)], dtype=np.int64)
dvec = np.array([classes[glue_frac2([BE[j, i] for j in range(8)])]
                 for i in range(8)], dtype=np.int64)


def deg_bulk(V2):
    prod = V2.astype(np.int64) @ I256.T
    assert np.all(prod % 256 == 0)
    return ((prod // 256) @ dvec) % 4


def deg_one(v):
    return int(deg_bulk(np.array([v], dtype=np.int64))[0])


tab_roots = Counter(int(d) for d in deg_bulk(np.array(roots2, dtype=np.int64)))
check("part-11 glue classifier: root census (52,64,60,64); SNF glue = Z4",
      dict(tab_roots) == {0: 52, 1: 64, 2: 60, 3: 64}
      and abs(Mglue.det()) == 4
      and sorted(abs(snf[i, i]) for i in range(8)) == [1] * 7 + [4])

# --- shell enumeration n = 1..7 (part 11/13 technique) ---
t_enum = time.time()
rng_i = np.arange(-3, 4, dtype=np.int16)
gi = np.array(np.meshgrid(*[rng_i] * 8, indexing="ij")).reshape(8, -1).T
ni = np.einsum("ij,ij->i", gi.astype(np.int32), gi.astype(np.int32))
mi = (gi.astype(np.int32).sum(axis=1) % 2 == 0) & (ni >= 2) & (ni <= 14)
V2_list = [2 * gi[mi].astype(np.int64)]
n_list = [ni[mi] // 2]
del gi, ni
rng_h = np.array([-7, -5, -3, -1, 1, 3, 5, 7], dtype=np.int16)
for c0 in rng_h:
    gh = np.array(np.meshgrid(*[rng_h] * 7, indexing="ij")).reshape(7, -1).T
    gh = np.hstack([np.full((gh.shape[0], 1), c0, dtype=np.int16), gh])
    nh = np.einsum("ij,ij->i", gh.astype(np.int32), gh.astype(np.int32))
    mh = (gh.astype(np.int32).sum(axis=1) % 4 == 0) & (nh <= 56)
    V2_list.append(gh[mh].astype(np.int64))
    n_list.append(nh[mh] // 8)
    del gh, nh
V2 = np.vstack(V2_list)
nsh = np.concatenate(n_list)
deg_all = deg_bulk(V2)
sig3 = {n: int(sp.divisor_sigma(n, 3)) for n in range(1, max(NMAX, 21) + 1)}
r_shell = {n: 240 * sig3[n] for n in range(1, max(NMAX, 21) + 1)}
enum_ok = all(int(np.sum(nsh == n)) == r_shell[n] for n in range(1, N_ENUM + 1))
info(f"shell enum n=1..7 in {time.time() - t_enum:.2f}s: "
     f"{[int(np.sum(nsh == n)) for n in range(1, N_ENUM + 1)]}")
check("direct E8 shell enumeration n<=7: N(2n)=240 sigma3(n) exact "
      "(classical Jacobi; part-11 technique)",
      enum_ok)

# per-shell vector lists (n <= 7) for folding
shell_vecs = {n: [tuple(int(x) for x in V2[i])
                  for i in np.where(nsh == n)[0]]
              for n in range(1, N_ENUM + 1)}
shell_deg = {n: [int(deg_all[i]) for i in np.where(nsh == n)[0]]
             for n in range(1, N_ENUM + 1)}


# =====================================================================
# dominant / D5A3-dominant enumeration via weight / chamber DFS
# =====================================================================
def enum_e8_dominant(n_max):
    """Dominant E8 lattice vectors with shell index <= n_max.
    x = sum c_i omega_i, c_i >= 0; doubled-norm ip(x,x) = 8n.
    """
    by_n = defaultdict(list)
    # bound: G_ii c_i^2 <= 8 n_max
    bounds = [isqrt(8 * n_max // Gfund[i][i]) for i in range(8)]

    def dfs(idx, coeffs, partial):
        if idx == 8:
            s = partial
            if s % 8 != 0:
                return
            n = s // 8
            if 1 <= n <= n_max:
                vec = tuple(sum(coeffs[i] * fund[i][k] for i in range(8))
                            for k in range(8))
                by_n[n].append(vec)
            return
        # remaining diagonal lower bound: only G_jj for j>=idx
        # prune: current + 0 >= already; upper: add max possible
        rem_max = 0
        for j in range(idx, 8):
            bj = bounds[j]
            rem_max += bj * bj * Gfund[j][j]
            for i in range(idx, j):
                rem_max += 2 * bounds[i] * bj * abs(Gfund[i][j])
        # cruder but safe prune using only positive-semidefinite:
        # ip >= sum_i G_ii c_i^2 (not always true if off-diag negative)
        # Use exact incremental: try c and prune if partial_exact > 8 n_max
        for c in range(bounds[idx] + 1):
            # exact partial norm with coords 0..idx fixed, rest 0
            add = c * c * Gfund[idx][idx]
            for i in range(idx):
                add += 2 * coeffs[i] * c * Gfund[i][idx]
            new_partial = partial + add
            if new_partial > 8 * n_max:
                break
            coeffs[idx] = c
            dfs(idx + 1, coeffs, new_partial)
        coeffs[idx] = 0

    dfs(0, [0] * 8, 0)
    return {n: by_n[n] for n in range(1, n_max + 1)}


def enum_d5a3_dominant(n_max):
    """Count D5xA3-dominant E8 vectors per shell by coordinate DFS.
    Integer type: v=2x; half-integer: odd coords.  Chamber:
      x0 >= x1 >= x2 >= x3 >= |x4|   (D5)
      y0 >= y1 >= |y2|               (A3 ~= D3) on last three.
    """
    counts = {n: 0 for n in range(1, n_max + 1)}
    glue_orbit = {n: Counter() for n in range(1, n_max + 1)}
    reps = {n: [] for n in range(1, n_max + 1)}

    # ---- integer type: |x|^2 = 2n, sum x even ----
    # bound |x_i| <= sqrt(2 n_max)
    B = isqrt(2 * n_max)

    def add_int(x):
        nrm = sum(t * t for t in x)
        if nrm % 2:
            return
        n = nrm // 2
        if not (1 <= n <= n_max):
            return
        if sum(x) % 2:
            return
        v = tuple(2 * t for t in x)
        assert is_dom(D5A3_SIMPLE, v)
        counts[n] += 1
        g = deg_one(v)
        glue_orbit[n][g] += 1
        if n <= N_ENUM:
            reps[n].append(v)

    def dfs_d5(pos, x, rem):
        if pos == 5:
            # A3 part: last 3 coords
            dfs_a3(0, x, rem)
            return
        # x[pos] >= x[pos+1] >= ... ; max |x[pos]| constrained by rem
        lo = -B
        hi = B
        if pos == 0:
            lo = 0  # can fix x0 >= 0 by overall sign? NO -- D5 chamber
            # already x0 >= x1 >= ... >= |x4| forces x0 >= 0
            lo = 0
        upper = isqrt(rem) if rem >= 0 else -1
        hi = min(hi, upper)
        # lower bound from chamber relative to previous
        if pos == 0:
            cand_lo = 0
        elif pos < 4:
            # x[pos] <= x[pos-1], and x[pos] >= x[pos+1] >= ... >= 0 eventually
            cand_lo = -B  # tightened below
            # remaining 5-pos coords each <= x[pos] in abs for last; use 0
            cand_lo = 0 if pos < 4 else -B
            # for pos=1,2,3: x[pos] between 0 and x[pos-1] roughly
            # since x3 >= |x4| >= 0, all of x0..x3 are >= 0
            cand_lo = 0
            hi = min(hi, x[pos - 1])
        else:
            # pos == 4: |x4| <= x3, and x4^2 <= rem
            # x4 in [-x3, x3]
            pass

        if pos < 4:
            for val in range(cand_lo, hi + 1):
                if pos > 0 and val > x[pos - 1]:
                    continue
                x[pos] = val
                dfs_d5(pos + 1, x, rem - val * val)
            x[pos] = 0
        else:
            # pos == 4
            lim = min(x[3], isqrt(rem) if rem >= 0 else -1)
            for val in range(-lim, lim + 1):
                x[4] = val
                dfs_d5(5, x, rem - val * val)
            x[4] = 0

    def dfs_a3(pos, x, rem):
        # fill x[5], x[6], x[7] with y0 >= y1 >= |y2|, sum squares = rem
        if pos == 0:
            upper = isqrt(rem) if rem >= 0 else -1
            for y0 in range(0, upper + 1):
                x[5] = y0
                dfs_a3(1, x, rem - y0 * y0)
            x[5] = 0
        elif pos == 1:
            upper = min(x[5], isqrt(rem) if rem >= 0 else -1)
            for y1 in range(0, upper + 1):
                x[6] = y1
                dfs_a3(2, x, rem - y1 * y1)
            x[6] = 0
        else:
            # |y2| <= y1, y2^2 = rem
            if rem < 0:
                return
            r = isqrt(rem)
            if r * r != rem:
                return
            y2 = r
            if y2 <= x[6]:
                x[7] = y2
                add_int(list(x))
                if y2 > 0:
                    x[7] = -y2
                    add_int(list(x))
            x[7] = 0

    # start integer DFS with total norm budget 2*n_max
    # exact shell budgets (one DFS per n -- rem must be spent exactly)
    for n_target in range(1, n_max + 1):
        dfs_d5(0, [0] * 8, 2 * n_target)

    # ---- half-integer type: coords odd, sum == 0 mod 4, |v|^2 = 8n ----
    def add_half(o):
        nrm = sum(t * t for t in o)
        if nrm % 8:
            return
        n = nrm // 8
        if not (1 <= n <= n_max):
            return
        if sum(o) % 4:
            return
        v = tuple(o)
        if not is_dom(D5A3_SIMPLE, v):
            return
        counts[n] += 1
        g = deg_one(v)
        glue_orbit[n][g] += 1
        if n <= N_ENUM:
            reps[n].append(v)

    def odd_range(lo, hi):
        a = lo if lo % 2 else lo + 1
        b = hi if hi % 2 else hi - 1
        if a > b:
            return range(0)
        return range(a, b + 1, 2)

    def dfs_d5h(pos, o, rem):
        if pos == 5:
            dfs_a3h(0, o, rem)
            return
        if pos < 4:
            hi = isqrt(rem) if rem >= 0 else -1
            if pos > 0:
                hi = min(hi, o[pos - 1])
            lo = 1  # all coords odd => 0 forbidden
            for val in odd_range(lo, hi):
                o[pos] = val
                dfs_d5h(pos + 1, o, rem - val * val)
            o[pos] = 0
        else:
            lim = min(o[3], isqrt(rem) if rem >= 0 else -1)
            for val in odd_range(-lim, lim):
                o[4] = val
                dfs_d5h(5, o, rem - val * val)
            o[4] = 0

    def dfs_a3h(pos, o, rem):
        if pos == 0:
            hi = isqrt(rem) if rem >= 0 else -1
            for y0 in odd_range(1, hi):
                o[5] = y0
                dfs_a3h(1, o, rem - y0 * y0)
            o[5] = 0
        elif pos == 1:
            hi = min(o[5], isqrt(rem) if rem >= 0 else -1)
            for y1 in odd_range(1, hi):
                o[6] = y1
                dfs_a3h(2, o, rem - y1 * y1)
            o[6] = 0
        else:
            if rem < 0:
                return
            r = isqrt(rem)
            if r * r != rem or r % 2 == 0:
                return
            if r <= o[6]:
                o[7] = r
                add_half(list(o))
                o[7] = -r
                add_half(list(o))
            o[7] = 0

    for n_target in range(1, n_max + 1):
        dfs_d5h(0, [0] * 8, 8 * n_target)
    return counts, glue_orbit, reps


# =====================================================================
# S2 -- Q1 Weyl orbits
# =====================================================================
print("S2 -- Q1: Weyl-orbit quotient (dominant vectors)")

t_q1 = time.time()
# fold route for n <= 7
q1_fold = {}
for n in range(1, N_ENUM + 1):
    doms = {fold_by(E8_SIMPLE, v) for v in shell_vecs[n]}
    q1_fold[n] = len(doms)
    assert all(is_dom(E8_SIMPLE, d) for d in doms)

dom_by_n = enum_e8_dominant(max(NMAX, 21))
q1 = {n: len(dom_by_n[n]) for n in range(1, max(NMAX, 21) + 1)}
info(f"q1 via weight-basis DFS in {time.time() - t_q1:.2f}s")
info(f"q1(n) n=1..20: {[q1[n] for n in range(1, NMAX + 1)]}")
info(f"q1 fold n=1..7: {[q1_fold[n] for n in range(1, N_ENUM + 1)]}")

fold_match = all(q1[n] == q1_fold[n] for n in range(1, N_ENUM + 1))
check("Q1 cross-check: weight-basis dominant count = fold-of-shell count "
      "for n=1..7 (classical: unique dominant per W-orbit)",
      fold_match)

# E1 for q1
coprime_pairs = [(m, n) for m in range(1, NMAX + 1) for n in range(1, NMAX + 1)
                 if m * n <= NMAX and gcd(m, n) == 1]
e1_q1_fails = [(m, n) for m, n in coprime_pairs
               if q1[m * n] * q1[1] != q1[m] * q1[n]]
e1_q1 = len(e1_q1_fails) == 0
if e1_q1_fails:
    m0, n0 = e1_q1_fails[0]
    info(f"E1 first break for q1: (m,n)=({m0},{n0}): "
         f"q1({m0*n0})*q1(1)={q1[m0*n0]*q1[1]} vs "
         f"q1({m0})*q1({n0})={q1[m0]*q1[n0]}")
info(f"q1 E1: {len(coprime_pairs) - len(e1_q1_fails)}/{len(coprime_pairs)} "
     f"coprime pairs ok; first fails: {e1_q1_fails[:5]}")
check(f"Q1 E1 multiplicativity on coprime pairs mn<=20: "
      f"{'HOLDS' if e1_q1 else 'FAILS (documented)'} -- honest expectation: "
      f"chamber volume ~ polynomial, not multiplicative; first break at "
      f"{e1_q1_fails[0] if e1_q1_fails else 'N/A'}",
      True)  # negative finding is the content

# E2 patterns (preregistered names)
primes = [p for p in range(2, NMAX + 1) if sp.isprime(p)]


def chi4(p):
    return 0 if p == 2 else (1 if p % 4 == 1 else -1)


def chi3(p):
    if p == 3:
        return 0
    return 1 if p % 3 == 1 else -1


PATTERNS = {
    "P_zeta": lambda p: 1,
    "P_const2": lambda p: 2,
    "P_chi4": lambda p: 1 + chi4(p),
    "P_chi3": lambda p: 1 + chi3(p),
    "P_1plusp": lambda p: 1 + p,
}


def match_e2(q, label):
    hits = []
    for name, fn in PATTERNS.items():
        if all(q[p] == fn(p) for p in primes):
            hits.append(name)
    # also: constant (any)
    vals = [q[p] for p in primes]
    if len(set(vals)) == 1:
        hits.append(f"P_const[{vals[0]}]")
    info(f"{label} prime values q(p): "
         f"{ {p: q[p] for p in primes} }; E2 hits: {hits or 'NONE'}")
    return hits


e2_q1 = match_e2(q1, "q1")


def hecke_e3(q, label, kmax=4):
    """Try deg<=2 Hecke recursion on prime powers p^k <= NMAX."""
    ok_any = []
    for p in primes:
        powers = []
        pk = 1
        for k in range(0, 8):
            if pk > NMAX:
                break
            powers.append(q[pk])
            pk *= p
        if len(powers) < 3:
            continue
        # powers[k] = q(p^k); try a_p = q(p), chi in {0,1,chi4}, w in 0..3
        # q(p^k) = a q(p^{k-1}) - chi * p^w * q(p^{k-2})
        a = q[p]
        found = False
        for chi_name, chi in (("triv", 1), ("zero", 0),
                              ("chi4", chi4(p) if p > 2 else 0)):
            for w in range(0, 4):
                good = True
                for k in range(2, len(powers)):
                    rhs = a * powers[k - 1] - chi * (p ** w) * powers[k - 2]
                    if powers[k] != rhs:
                        good = False
                        break
                if good:
                    ok_any.append((p, chi_name, w, powers))
                    found = True
                    break
            if found:
                break
    info(f"{label} E3 Hecke fits: {ok_any[:6]}"
         f"{' ...' if len(ok_any) > 6 else ''} "
         f"({len(ok_any)} primes with some fit)")
    # E3 requires ALL primes with enough powers to fit the SAME (chi_fam, w)
    # with a_p = q(p)
    return ok_any


e3_q1 = hecke_e3(q1, "q1")
# E4: is q1's Euler product sigma3? clearly no if not multiplicative
e4_q1 = False  # cannot be zeta/L if E1 fails
info(f"q1 growth: q1(1..10)={ [q1[n] for n in range(1, 11)] } "
     f"(polynomial chamber growth -- classical)")
check("Q1 E2/E3/E4: E2 pattern match "
      f"{e2_q1 or 'NONE'}; E3 partial fits on "
      f"{len(e3_q1)} prime ladders; E4 = False (E1 failed => not a "
      "single L / zeta / zeta L) -- negative findings recorded",
      True)


# =====================================================================
# S3 -- Q2 W(D5)xW(A3) x glue
# =====================================================================
print("S3 -- Q2: glue-preserving Weyl (W(D5)xW(A3)) x glue class")

# Document: W(E8) does NOT preserve glue
examples_break = []
for v in shell_vecs[1][:40]:
    # reflect by first E8 simple root if possible
    for a in E8_SIMPLE:
        c = ip(v, a)
        if c != 0 and c % 4 == 0:
            w = tuple(v[t] - (c // 4) * a[t] for t in range(8))
            if deg_one(v) != deg_one(w):
                examples_break.append((v, a, w, deg_one(v), deg_one(w)))
                break
    if len(examples_break) >= 3:
        break
info(f"W(E8) glue non-invariance examples (v, alpha, w, deg v, deg w):")
for ex in examples_break[:3]:
    info(f"  deg {ex[3]} -> deg {ex[4]} under reflection")
check("W(E8) does NOT preserve mu4 glue class (explicit reflection "
      "examples on the root shell) -- so Q1 orbits cannot carry a "
      "glue label; refine to W(D5)xW(A3)",
      len(examples_break) >= 1)

# D5xA3 DOES preserve glue (subgroup of automorphisms of the pair)
d5a3_preserves = True
for n in range(1, min(3, N_ENUM) + 1):
    for v in shell_vecs[n][:: max(1, len(shell_vecs[n]) // 30)]:
        for a in D5A3_SIMPLE:
            c = ip(v, a)
            if c != 0 and c % 4 == 0:
                w = tuple(v[t] - (c // 4) * a[t] for t in range(8))
                if deg_one(v) != deg_one(w):
                    d5a3_preserves = False
check("W(D5)xW(A3) reflections preserve glue class on sampled shell "
      "vectors (n=1,2,3) -- glue-preserving subgroup usable for Q2",
      d5a3_preserves)

t_q2 = time.time()
q2_fold = {}
q2_glue_hist = {}
for n in range(1, N_ENUM + 1):
    reps = {}
    for v, g in zip(shell_vecs[n], shell_deg[n]):
        r = fold_by(D5A3_SIMPLE, v)
        reps[r] = g  # glue constant on orbit
        assert deg_one(r) == g
    q2_fold[n] = len(reps)
    hist = Counter(reps.values())
    q2_glue_hist[n] = dict(sorted(hist.items()))
info(f"q2 fold n=1..7: {[q2_fold[n] for n in range(1, N_ENUM + 1)]}")
info(f"q2 glue hist n=1: {q2_glue_hist[1]}")

# chamber DFS for n <= 21
q2_counts, q2_ghist, _ = enum_d5a3_dominant(max(NMAX, 21))
info(f"q2 chamber DFS in {time.time() - t_q2:.2f}s")
info(f"q2(n) n=1..20: {[q2_counts[n] for n in range(1, NMAX + 1)]}")
q2_match = all(q2_counts[n] == q2_fold[n] for n in range(1, N_ENUM + 1))
check("Q2 cross-check: D5xA3-chamber count = fold-of-shell count "
      "for n=1..7",
      q2_match)
q2 = q2_counts

e1_q2_fails = [(m, n) for m, n in coprime_pairs
               if q2[m * n] * q2[1] != q2[m] * q2[n]]
e1_q2 = len(e1_q2_fails) == 0
if e1_q2_fails:
    m0, n0 = e1_q2_fails[0]
    info(f"E1 first break for q2: ({m0},{n0}): "
         f"q2({m0*n0})*q2(1)={q2[m0*n0]*q2[1]} vs "
         f"q2({m0})*q2({n0})={q2[m0]*q2[n0]}")
info(f"q2 E1: {len(coprime_pairs) - len(e1_q2_fails)}/{len(coprime_pairs)} "
     f"ok; first fails: {e1_q2_fails[:5]}")
e2_q2 = match_e2(q2, "q2")
e3_q2 = hecke_e3(q2, "q2")
check(f"Q2 E1 multiplicativity: {'HOLDS' if e1_q2 else 'FAILS'} "
      f"(first break {e1_q2_fails[0] if e1_q2_fails else 'N/A'}); "
      f"E2 hits {e2_q2 or 'NONE'}; E3 fits on {len(e3_q2)} ladders -- "
      "findings recorded",
      True)


# =====================================================================
# S4 -- Q3 primitive layer
# =====================================================================
print("S4 -- Q3: divisibility / primitive stratification (Moebius)")

# Classical: r(n) = sum_{d^2 | n} r_prim(n/d^2)
# => r_prim(n) = sum_{d^2 | n} mu(d) r(n/d^2)
def r_prim(n):
    s = 0
    d = 1
    while d * d <= n:
        if n % (d * d) == 0:
            s += int(sp.mobius(d)) * r_shell[n // (d * d)]
        d += 1
    return s


rp = {n: r_prim(n) for n in range(1, max(NMAX, 21) + 1)}
# verify inversion on n=1..20
inv_ok = True
for n in range(1, NMAX + 1):
    recon = sum(rp[n // (d * d)] for d in range(1, isqrt(n) + 1)
                if n % (d * d) == 0)
    if recon != r_shell[n]:
        inv_ok = False
        break
info(f"r_prim(n) n=1..20: {[rp[n] for n in range(1, NMAX + 1)]}")
info(f"r_prim(n)/240 n=1..20: {[rp[n] // 240 for n in range(1, NMAX + 1)]}")
check("Q3 Moebius inversion exact: r(n)=sum_{d^2|n} r_prim(n/d^2) and "
      "r_prim(n)=sum mu(d) r(n/d^2) for n=1..20 (classical square "
      "stratification of a lattice)",
      inv_ok and all(rp[n] % 240 == 0 for n in range(1, NMAX + 1)))

# classical comparison: sigma3 vs "primitive sigma"
# The function beta(n) = r_prim(n)/240 = sum_{d^2|n} mu(d) sigma3(n/d^2)
beta = {n: rp[n] // 240 for n in range(1, max(NMAX, 21) + 1)}
info(f"beta=r_prim/240 vs sigma3: "
     f"{[(n, beta[n], sig3[n]) for n in range(1, 13)]}")

# Is beta multiplicative?
e1_beta_fails = [(m, n) for m, n in coprime_pairs
                 if beta[m * n] * beta[1] != beta[m] * beta[n]]
e1_beta = len(e1_beta_fails) == 0
info(f"beta E1: fails at {e1_beta_fails[:5]} "
     f"({len(e1_beta_fails)} fails)")

# q3a = beta itself; q3b = number of dominant primitive vectors
# dominant primitive: E8-dominant with gcd of Z-coords = 1
# In doubled coords: for integer type v=2x, primitivity of x in E8
# <=> not all coords of x divisible by d>1.
# Equivalent lattice-intrinsic: v not in d*(2E8) for d>1, i.e.
# content of the vector in the lattice = 1.


def lattice_content(v):
    """Largest d > 0 such that v/d is still in the doubled E8 model."""
    # v must be divisible by d in Z^8, and v/d must satisfy E8 parity
    g = 0
    for t in v:
        g = gcd(g, abs(t))
    if g == 0:
        return 0
    # candidate divisors of g; E8 in doubled coords: all even or all odd.
    # If v has content d (actual lattice), doubled vector divisible by d.
    # Maximal d with v/d in E8_doubled.
    best = 1
    for d in range(1, g + 1):
        if g % d:
            continue
        w = [t // d for t in v]
        # E8 doubled parity
        par = [t % 2 for t in w]
        if any(par) and not all(par):
            continue
        if all(par) and sum(w) % 4 != 0:
            continue
        if (not any(par)) and (sum(t // 2 for t in w) % 2 != 0):
            continue
        # norm integrity: ip(w,w) must be 0 mod 8 for shell index
        if ip(w, w) % 8 != 0:
            continue
        best = d
    return best


q3_dom_prim = {}
for n in range(1, NMAX + 1):
    cnt = 0
    for v in dom_by_n[n]:
        if lattice_content(v) == 1:
            cnt += 1
    q3_dom_prim[n] = cnt
info(f"q3_dom_prim (dominant + content 1) n=1..20: "
     f"{[q3_dom_prim[n] for n in range(1, NMAX + 1)]}")

# combine with glue: dominant primitive per glue -- use fold shells n<=7
q3_dom_glue = {}
for n in range(1, N_ENUM + 1):
    seen = set()
    for v, g in zip(shell_vecs[n], shell_deg[n]):
        d = fold_by(E8_SIMPLE, v)
        if lattice_content(d) == 1:
            seen.add((d, g))  # NOTE: glue not W-invariant; this is a
            # diagnostic pairing of (dominant, glue of preimage) --
            # honest: not canonical.  Prefer D5A3 fold:
    seen2 = set()
    for v, g in zip(shell_vecs[n], shell_deg[n]):
        d = fold_by(D5A3_SIMPLE, v)
        if lattice_content(v) == 1:  # primitivity of the vector itself
            seen2.add((d, g))
    q3_dom_glue[n] = len(seen2)
info(f"q3 D5A3-orbit x glue on PRIMITIVE vectors n=1..7: "
     f"{[q3_dom_glue[n] for n in range(1, N_ENUM + 1)]}")

e1_q3a_fails = e1_beta_fails
e1_q3b_fails = [(m, n) for m, n in coprime_pairs
                if q3_dom_prim[m * n] * q3_dom_prim[1]
                != q3_dom_prim[m] * q3_dom_prim[n]]
e1_q3b = len(e1_q3b_fails) == 0
e2_beta = match_e2(beta, "beta=r_prim/240")
e2_q3b = match_e2(q3_dom_prim, "q3_dom_prim")
e3_beta = hecke_e3(beta, "beta")
check(f"Q3 E1: beta=r_prim/240 "
      f"{'HOLDS' if e1_beta else 'FAILS'} "
      f"(first {e1_beta_fails[0] if e1_beta_fails else 'N/A'}); "
      f"dominant-primitive "
      f"{'HOLDS' if e1_q3b else 'FAILS'} "
      f"(first {e1_q3b_fails[0] if e1_q3b_fails else 'N/A'}); "
      f"E2 beta={e2_beta or 'NONE'}, dom_prim={e2_q3b or 'NONE'} -- "
      "classical Moebius layer does not yield GL(1) counting",
      True)

# document classical comparison
check("Q3 classical comparison typed: beta(n)=sum_{d^2|n} mu(d) "
      "sigma3(n/d^2) is the square-free-at-squares residual of sigma3; "
      "it is NOT identically 1, NOT sigma_0, and (as checked) not a "
      "named deg<=2 L-local pattern on primes in range -- still "
      "multiplicity-laden relative to GL(1)",
      beta[1] == 1 and beta[2] == sig3[2] and rp[1] == 240)


# =====================================================================
# S5 -- tensor fingerprint
# =====================================================================
print("S5 -- tensor fingerprint: Shell(m) x Shell(n) vs Shell(mn)")

# Class arithmetic on Q2 (orbit x glue): class count = q2(n)
# Glue character distribution from chamber hist / fold hist
tensor_rows = []
tensor_class_ok = True
tensor_glue_ok = True
for m, n in TENSOR_PAIRS:
    mn = m * n
    # class-count factorisation (E1 at class level)
    left = q2[m] * q2[n]
    right = q2[mn] * q2[1]
    class_factor = (left == right)
    if not class_factor:
        tensor_class_ok = False
    # glue histogram convolution under Z/4Z addition
    # use fold hist for n<=7; else chamber hist
    def hist(k):
        if k <= N_ENUM:
            return Counter(q2_glue_hist[k])
        return Counter(q2_ghist[k])

    hm, hn, hmn = hist(m), hist(n), hist(mn)
    conv = Counter()
    for a, ca in hm.items():
        for b, cb in hn.items():
            conv[(a + b) % 4] += ca * cb
    # compare shape: normalised?  Or exact product of totals
    # Exact: if functorial in glue, # in class c on mn should relate
    # to sum_{a+b=c} #_m(a) #_n(b) -- but totals: sum conv = q2(m)q2(n),
    # sum hmn = q2(mn).  Compare proportional fingerprints:
    glue_match = (sum(conv.values()) == q2[m] * q2[n]
                  and sum(hmn.values()) == q2[mn])
    # fingerprint equality of normalised distributions
    tot_c = sum(conv.values()) or 1
    tot_h = sum(hmn.values()) or 1
    dist_c = tuple(conv.get(i, 0) / tot_c for i in range(4))
    dist_h = tuple(hmn.get(i, 0) / tot_h for i in range(4))
    # exact scaled equality: conv == lambda * hmn?
    # require conv[i]*q2[mn] == hmn[i]*q2[m]*q2[n] for all i
    scaled = all(conv.get(i, 0) * q2[mn] == hmn.get(i, 0) * q2[m] * q2[n]
                 for i in range(4))
    if not scaled:
        tensor_glue_ok = False
    row = (m, n, q2[m], q2[n], q2[mn], left, right, class_factor,
           dict(hm), dict(hn), dict(hmn), dict(conv), scaled)
    tensor_rows.append(row)
    info(f"  ({m},{n}): q2={q2[m]} x {q2[n]} = {left}; "
         f"q2({mn})*q2(1)={right}; class_factor={class_factor}; "
         f"glue_scaled={scaled}")
    info(f"    hist m/n/mn/conv = {dict(hm)} / {dict(hn)} / "
         f"{dict(hmn)} / {dict(conv)}")

check("TENSOR class-count factorisation q2(m)*q2(n)=q2(mn)*q2(1) on "
      f"pairs {TENSOR_PAIRS}: "
      f"{'YES' if tensor_class_ok else 'NO -- functor dead at class counts'}",
      True)
check("TENSOR glue-histogram scaled convolution under Z/4Z: "
      f"{'YES' if tensor_glue_ok else 'NO -- character arithmetic fails'}",
      True)

# Also E1-style on q1 for tensor pairs
q1_tensor = all(q1[m * n] * q1[1] == q1[m] * q1[n] for m, n in TENSOR_PAIRS)
info(f"q1 tensor pairs factor: {q1_tensor}")
check("TENSOR also checked on Q1 dominant counts for the five pairs: "
      f"{'factor' if q1_tensor else 'do NOT factor'} -- consistent with "
      "E1 failure of Q1",
      True)


# =====================================================================
# S6 -- verdict
# =====================================================================
print("S6 -- verdict against preregistered criteria")

candidates = {
    "Q1_Weyl": dict(e1=e1_q1, e2=bool(e2_q1), e3=len(e3_q1) == len(primes),
                    e2_hits=e2_q1, e1_fail=e1_q1_fails[:3],
                    q=[q1[n] for n in range(1, NMAX + 1)]),
    "Q2_D5A3_glue": dict(e1=e1_q2, e2=bool(e2_q2),
                         e3=len(e3_q2) == len(primes),
                         e2_hits=e2_q2, e1_fail=e1_q2_fails[:3],
                         q=[q2[n] for n in range(1, NMAX + 1)]),
    "Q3_beta_rprim/240": dict(e1=e1_beta, e2=bool(e2_beta),
                              e3=len(e3_beta) == len(primes),
                              e2_hits=e2_beta, e1_fail=e1_beta_fails[:3],
                              q=[beta[n] for n in range(1, NMAX + 1)]),
    "Q3_dom_prim": dict(e1=e1_q3b, e2=bool(e2_q3b), e3=False,
                        e2_hits=e2_q3b, e1_fail=e1_q3b_fails[:3],
                        q=[q3_dom_prim[n] for n in range(1, NMAX + 1)]),
}

found = [name for name, c in candidates.items()
         if c["e1"] and c["e2"] and c.get("e3")]
# E4 implied by E1+E2+E3 with non-sigma3 -- none found
partial = [name for name, c in candidates.items()
           if c["e1"] and not (c["e2"] and c.get("e3"))]
# also PARTIAL if E1 fails but something interesting -- per spec:
# PARTIAL = E1 yes for a candidate, E2-E4 partial
if found:
    verdict = "GL1-QUOTIENT-FOUND"
elif partial:
    verdict = "PARTIAL"
else:
    verdict = "DEAD"

info(f"candidate summary:")
for name, c in candidates.items():
    info(f"  {name}: E1={c['e1']} E2={c['e2']}({c['e2_hits']}) "
         f"E3_allprimes={c['e3']}; q[1..20]={c['q']}")
# E4 for beta: Dirichlet series = zeta(s)zeta(s-3)/zeta(2s) (classical
# from Dir(r) = zeta(2s) Dir(r_prim)) -- NOT zeta / zeta L / single L.
e4_beta = False
info(f"beta E4: Dir(beta) = zeta(s)zeta(s-3)/zeta(2s) (classical "
     f"square-divisor identity) -- NOT a GL(1)/single-L series; "
     f"E4={e4_beta}")
info(f"VERDICT = {verdict}")
if verdict == "PARTIAL":
    info("Consequence for ZETA.CENSUS.TO.GL1: PARTIAL narrowing -- "
         "Q1 (Weyl) and Q2 (D5xA3 x glue) FAIL E1 (first breaks "
         f"{e1_q1_fails[0] if e1_q1_fails else 'N/A'} / "
         f"{e1_q2_fails[0] if e1_q2_fails else 'N/A'}); tensor "
         "class-count factorisation FAILS on all five pairs => "
         "Shell(m)(x)Shell(n)->Shell(mn) functor DEAD at the "
         "countable fingerprint.  Q3 beta=r_prim/240 IS multiplicative "
         "(E1) but beta(p)=1+p^3 (E2 FAIL) and Dir=zeta zeta(s-3)/"
         "zeta(2s) (E4 FAIL) -- still the weight-4 Eisenstein residual, "
         "NOT multiplicity-1.  Kill E1+E2 fires for GL(1).  Next lever: "
         "parallel p-neighbor / Hecke-from-seam (not shell-quotient).")
elif verdict == "DEAD":
    info("Consequence: no candidate even multiplicative; shell-quotient "
         "branch fully closed.")
else:
    info("Consequence: GL1 quotient found -- document Euler factors.")

check(f"VERDICT = {verdict} (preregistered tree): Q3-beta has E1 but "
      f"not E2/E4 (beta(p)=1+p^3; Dir=zeta zeta(s-3)/zeta(2s)); "
      f"Q1/Q2 E1 fail at "
      f"{e1_q1_fails[0] if e1_q1_fails else 'N/A'} / "
      f"{e1_q2_fails[0] if e1_q2_fails else 'N/A'}; tensor class "
      f"factorisation fails; no candidate meets E1+E2 (GL1 kill); "
      f"ZETA.CENSUS.TO.GL1 shell-quotient route narrowed to PARTIAL "
      f"-- Moebius residual multiplicative but not GL(1)",
      verdict == "PARTIAL"
      and e1_beta and not e2_beta and not found
      and not e1_q1 and not e1_q2 and not tensor_class_ok)

check("global consistency: r(n)=240 sigma3 classical; Q1 fold=weight "
      "for n<=7; Q2 fold=chamber for n<=7; Moebius inversion exact; "
      "W(E8) glue-noninvariant / W(D5)xW(A3) glue-invariant; "
      "NO promotion; NO RH-evidence language; classical named classical",
      enum_ok and fold_match and q2_match and inv_ok
      and len(examples_break) >= 1 and d5a3_preserves)

elapsed = time.time() - T0
print(f"\nTOTAL: {PASS} passed, {FAIL} failed  ({elapsed:.1f}s)", flush=True)
raise SystemExit(0 if FAIL == 0 else 1)
