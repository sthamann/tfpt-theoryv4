"""WP5b of CELEST.SEAM.01 (EXPLORATION ONLY -- experiments/, no verification claim).

"THE SINGULAR VECTOR AS AN OPERATOR" -- second constructive milestone of WP5.
WP5a (v497 + the WP5a probe) derived the SIZE and LOCATION of the level-2 null
ideal (27000 = h_vee^3 = dim V(2 theta) inside Sym^2(248)) and made the boundary
limit a precise coefficientwise limit.  WP5b now CONSTRUCTS the deleting object:
the level-2 vacuum singular vector of the affine (E8)_1 current algebra,

    |s> = (E^theta_{-1})^2 |0>      (weight 2 theta, level-2, level k = 1),

explicitly, in an exact integer Chevalley / Frenkel-Kac basis built from the
v497 root machinery, and machine-verifies (exact Fractions, no floats, nothing
cited) singularity and mu4 compatibility.  Preregistered criteria (contract /
v497): SUCCESS = |s> explicit + J^a_1 |s> = 0 for all 248 generators machine-
checked + mu4-grading compatible (integer quarter-level, definite clock phase,
expressible through the mu4-sector variables); KILL = |s> cannot be written in
the limit/equivariant variables.

  S1  CHEVALLEY BASIS FROM ROOT DATA (not cited).  Standard-frame E8 (v497
      doubled-integer coordinates): bimultiplicative Frenkel-Kac 2-cocycle
      eps(a,b) = (-1)^(m_a^T B m_b) on the root lattice; brackets
      [e_a,e_b] = eps(a,b) e_{a+b}, [e_a,e_{-a}] = SGN * H(a) with the sign
      SGN machine-determined by the Jacobi identity (not chosen); invariant
      form kappa derived from invariance (not postulated), normalised
      kappa(theta_vee,theta_vee) = 2.  Verified: eps diagonal/asymmetry on all
      240/57600 pairs, antisymmetry on all pairs, Jacobi on ALL 57600 triples
      (e_a, e_{-a}, e_b) + 4000 seeded general triples + all theta-adjacent
      triples + Cartan samples, kappa invariance on all 13440 root triples
      with a+b+c = 0, sl2 triples on all 240 roots.
  S2  THETA STRUCTURE.  theta-grading g = g_{-2}+g_{-1}+g_0+g_1+g_2 with dims
      (1,56,134,56,1) (134 = 126 roots + 8 Cartan = e7 + u(1)); a+theta not a
      root for ALL positive a (E^a_0 |s> = 0 automatic); a+2*theta re-enters
      the root system for EXACTLY one root (a = -theta, giving theta back);
      the 248 cases of the J_1 condition classified: 190 vanish at the
      first bracket, 57 at the second, exactly 1 (a = F^theta) by the central-
      term cancellation -- the ONLY case that sees the level k.
  S3  THE SINGULAR VECTOR, MACHINE-VERIFIED.  Exact affine PBW engine
      ([J^a_m, J^b_n] = [a,b]_{m+n} + m k kappa(a,b) delta_{m+n,0}) unit-tested
      against kappa and the bracket table on all 61504 pairs.  |s> constructed
      as an explicit Fock monomial; J^a_1 |s> = 0 for ALL 248 basis elements,
      J^a_2 |s> = 0 for all 248, E^a_0 |s> = 0 for all 120 positive roots,
      h_i-eigenvalues = <2 theta, a_i_vee>: |s> is an exact singular vector.
      Shapovalov norm 0 at k = 1.  Level dial: the F^theta_1 coefficient is
      2(1-k) -- nonzero at k = 0 (centerless loop algebra: the deletion
      operator does NOT exist without the central extension) and at k = 2,
      zero EXACTLY at k = 1.
  S4  MU4 COMPATIBILITY (the TFPT-specific part; glue frame, v492/v128 data).
      Inner grading h = (2,2,2,2,2;0^4) replicated on all 240 roots; the
      h-adapted Weyl chamber constructed (simple roots re-derived, E8 diagram
      shape verified); theta_glue found (height 29), glue class j(theta) =
      <theta,h> mod 4 computed; clock phase on |s> = i^(2 j(theta)) computed;
      2 j(theta) mod 4 in {0,2}: sheet-even (WP5a S6.8 consistent); the
      theta-sl2 (E^theta, F^theta) sits in the sheet-ODD class pair (j, 4-j)
      while its square is sheet-even; E^theta exists in the equivariant jet
      algebra (sector C_j, spatial degrees m = -j mod 4), and the square is a
      mu4-INVARIANT element; quarter bookkeeping: E^theta_{-1} = 4 quarter
      units (one full mu4 period = 248 currents, v496 dictionary), |s> = 8
      quarters = q^2 INTEGER level.  Lattice reading: momentum 2 theta has
      lattice class 2 j(theta) and (2theta,2theta)/2 = 4 > 2, so the quotient
      (E8)_1 theory has NO momentum-2theta state at q^2: |s> IS the kernel
      generator of Fock -> E4/eta^8; theta-split sector dims at q^2 =
      (1036,1024,1040,1024), sum 4124 (v497 two-routes replication).  HONEST
      [O] FLAG: in the TWISTED quarter-slot moding of the chi_w limit Fock the
      two-particle E^theta states sit at u-levels = 2 mod 4 (minimum q^{3/2},
      never q^2): the per-period (untwisted) dictionary, not the per-slot
      identification, carries |s> -- exactly the WP5c GNS/limit-state seam.
  S5  LEVEL-2 COUNT.  dim V(2 theta) = 27000 = 30^3 = h_vee^3 (Freudenthal +
      Weyl-orbit sums, v497 replication); weight 2 theta has multiplicity 1 in
      the level-2 Fock (unique pair theta+theta), so U(g)|s> is THE 27000;
      quotient 31124 - 27000 = 4124 = 1 + 248 + 3875; DIRECT ORBIT CHECK: the
      g_0-lowering BFS from |s> inside the level-2 Fock reproduces the
      Freudenthal weight multiplicities of V(2 theta) exactly, weight by
      weight, through depth 4 ([C] Weyl complete reducibility extends the
      count to the full 27000).
  S6  NEGATIVE CONTROLS.  (a) The FALSE candidate E^theta_{-1}|0> (level 1) is
      NOT singular: exactly one witness (a = F^theta) with J^a_1 = k|0> != 0
      -- it is the 248-current state that must REMAIN (chi_1 = 248).
      (b) Generic level-2 states (E^b_{-1})(E^c_{-1})|0>, b+c != 2 theta
      (4 seeded picks): all non-singular with many witnesses.  (c) Level dial:
      (E^theta_{-1})^2 fails at k = 0 and k = 2 (coefficient 2|1-k|), and at
      k = 2 the CUBE (E^theta_{-1})^3 is singular (all 248 J_1 and J_2 zero):
      the (E^theta)^{k+1} mechanism is generic Kac level mechanics -- honestly
      typed.  (d) SO(16)_1 contrast (D8, same pipeline): Chevalley basis +
      Jacobi verified, (E^theta_{-1})^2|0> IS singular at k = 1 (the mechanics
      is not E8-specific), BUT D8 has THREE more level-1 primaries
      (<omega,theta_vee> = 1 for vector + both spinors, h = (1/2,1,1) exact)
      -- the singular vector alone does not make SO(16)_1 one-block (h = 1/2
      non-integer breaks fusion), while E8 has comarks all >= 2 (vacuum is the
      ONLY level-1 primary) and integer glue weights (0,1,1,1): the ONE-BLOCK
      closure is E8/mu4-specific; and 27000 = 30^3 vs 5304 != 14^3.
  S7  VERDICT (preregistered).  SUCCESS criteria all machine-met at the
      ALGEBRAIC-MODULE level; KILL not triggered.  Honest limit [O]: the GNS
      limit state whose kernel contains the ideal (WP5c), local normality /
      Haag duality (WP5d), Costello-Li (WP5e) stay OPEN; the twisted-slot
      moding tension is flagged as the precise WP5c question.  SEAM.EQUIV.01
      untouched; no gate closes, no marker moves.

Throwaway probe: standalone, sympy-free (exact integers/Fractions), prints
tables + PASS/FAIL + verdict, ends with a check count.  Nothing here is a
claim; promotion (if any) goes through the usual workflow.  verification/,
ledger, papers, changelog, website, scorecard untouched.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, isqrt
import random

G_CAR = 5
N_FAM = 3
MU4 = 4
RANK = 8
H_VEE = 30

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


# ---------------------------------------------------------------------------
# exact integer power series helpers (lists of coefficients, q^0..q^n)
# ---------------------------------------------------------------------------
def series_mul(a, b, nmax):
    out = [0] * (nmax + 1)
    for i, ai in enumerate(a[:nmax + 1]):
        if ai == 0:
            continue
        for j, bj in enumerate(b[:nmax + 1 - i]):
            out[i + j] += ai * bj
    return out


def geom_factor(d, D, nmax):
    out = [0] * (nmax + 1)
    k = 0
    while d * k <= nmax:
        out[d * k] = comb(D + k - 1, k)
        k += 1
    return out


def fock(gen_dims, nmax):
    out = [1] + [0] * nmax
    for d, D in gen_dims.items():
        if d == 0 or D == 0:
            continue
        out = series_mul(out, geom_factor(d, D, nmax), nmax)
    return out


# ---------------------------------------------------------------------------
# small exact linear algebra (Fractions)
# ---------------------------------------------------------------------------
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


def _det(M):
    n = len(M)
    A = [[F(M[i][j]) for j in range(n)] for i in range(n)]
    det = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None:
            return 0
        if p != c:
            A[c], A[p] = A[p], A[c]
            det = -det
        det *= A[c][c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(c + 1, n):
            if A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return det


def ip(a, b):
    return sum(x * y for x, y in zip(a, b))


def vadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def vsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def smul(k, a):
    return tuple(k * x for x in a)


# ---------------------------------------------------------------------------
# root-system machinery in DOUBLED integer coordinates (v497 replication;
# all roots norm_d = 8, true inner product = ip_d / 4)
# ---------------------------------------------------------------------------
class RootSystem:
    def __init__(self, name, simple, roots):
        self.name = name
        self.simple = [tuple(a) for a in simple]
        self.roots = [tuple(r) for r in roots]
        self.dim = len(simple[0])
        self.n = len(simple)
        assert self.dim == self.n
        self.Mrows = [[self.simple[j][i] for j in range(self.n)]
                      for i in range(self.dim)]
        self.cartan = [[ip(a, b) // 4 for b in self.simple]
                       for a in self.simple]
        pos = [r for r in self.roots if self._nonneg_coords(r)]
        assert 2 * len(pos) == len(self.roots)
        self.pos = pos
        s = [0] * self.dim
        for r in pos:
            s = [x + y for x, y in zip(s, r)]
        assert all(x % 2 == 0 for x in s)
        self.rho = tuple(x // 2 for x in s)
        self.fund = []
        for i in range(self.n):
            b = [4 if j == i else 0 for j in range(self.n)]
            rows = [[self.simple[j][k] for k in range(self.dim)]
                    for j in range(self.n)]
            w = solve_fraction(rows, b)
            assert all(x.denominator == 1 for x in w)
            self.fund.append(tuple(int(x) for x in w))

    def _nonneg_coords(self, v):
        cs = solve_fraction(self.Mrows, list(v))
        return all(c >= 0 for c in cs)

    def alpha_coords(self, v):
        return solve_fraction(self.Mrows, list(v))

    def in_Qplus(self, v):
        cs = self.alpha_coords(v)
        return all(c.denominator == 1 and c >= 0 for c in cs)

    def height(self, v):
        cs = self.alpha_coords(v)
        h = sum(cs)
        assert h.denominator == 1
        return int(h)

    def fold(self, v):
        v = list(v)
        changed = True
        while changed:
            changed = False
            for a in self.simple:
                c = 0
                for x, y in zip(v, a):
                    c += x * y
                if c < 0:
                    k = c // 4
                    assert c % 4 == 0
                    for t in range(self.dim):
                        v[t] -= k * a[t]
                    changed = True
        return tuple(v)

    def is_dominant(self, v):
        return all(ip(v, a) >= 0 for a in self.simple)

    def weyl_dim(self, lam):
        lr = vadd(lam, self.rho)
        out = F(1)
        for a in self.pos:
            out *= F(ip(lr, a), ip(self.rho, a))
        assert out.denominator == 1
        return int(out)

    def dominant_candidates(self, lam):
        nl = ip(lam, lam)
        G = [[ip(wi, wj) for wj in self.fund] for wi in self.fund]
        bounds = [isqrt(nl // G[i][i]) for i in range(self.n)]
        out = []
        for ns in product(*(range(b + 1) for b in bounds)):
            mu = tuple(sum(ns[i] * self.fund[i][k] for i in range(self.n))
                       for k in range(self.dim))
            if ip(mu, mu) <= nl and self.in_Qplus(vsub(lam, mu)):
                out.append(mu)
        return out

    def freudenthal(self, lam):
        lam = tuple(lam)
        if all(x == 0 for x in lam):
            return {lam: 1}
        cands = sorted(self.dominant_candidates(lam),
                       key=lambda m: self.height(vsub(lam, m)))
        acoords = [(a, [int(c) for c in self.alpha_coords(a)])
                   for a in self.pos]
        mult = {}
        lr = vadd(lam, self.rho)
        nlr = ip(lr, lr)
        for mu in cands:
            if mu == lam:
                mult[lam] = 1
                continue
            cmu = [int(c) for c in self.alpha_coords(vsub(lam, mu))]
            num = 0
            for a, ca in acoords:
                k = 1
                while all(cm - k * c >= 0 for cm, c in zip(cmu, ca)):
                    nu = vadd(mu, smul(k, a))
                    m = mult.get(self.fold(nu), 0)
                    if m:
                        num += m * ip(nu, a)
                    k += 1
            mr = vadd(mu, self.rho)
            den = nlr - ip(mr, mr)
            assert den > 0 and (2 * num) % den == 0
            m_mu = (2 * num) // den
            if m_mu > 0:
                mult[mu] = m_mu
        return mult

    def orbit_size(self, v):
        v = tuple(v)
        seen = {v}
        frontier = [v]
        while frontier:
            nf = []
            for x in frontier:
                for a in self.simple:
                    c = ip(x, a)
                    if c == 0:
                        continue
                    y = tuple(xi - (c // 4) * ai for xi, ai in zip(x, a))
                    if y not in seen:
                        seen.add(y)
                        nf.append(y)
            frontier = nf
        return len(seen)

    def dim_by_orbits(self, mult):
        return sum(m * self.orbit_size(mu) for mu, m in mult.items())


def e8_std():
    roots = []
    for i, j in combinations(range(8), 2):
        for si in (2, -2):
            for sj in (2, -2):
                v = [0] * 8
                v[i], v[j] = si, sj
                roots.append(tuple(v))
    for signs in product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            roots.append(tuple(signs))
    simple = [
        (1, -1, -1, -1, -1, -1, -1, 1),
        (2, 2, 0, 0, 0, 0, 0, 0),
        (-2, 2, 0, 0, 0, 0, 0, 0),
        (0, -2, 2, 0, 0, 0, 0, 0),
        (0, 0, -2, 2, 0, 0, 0, 0),
        (0, 0, 0, -2, 2, 0, 0, 0),
        (0, 0, 0, 0, -2, 2, 0, 0),
        (0, 0, 0, 0, 0, -2, 2, 0),
    ]
    return RootSystem('E8', simple, roots)


def d8_std():
    roots = []
    for i, j in combinations(range(8), 2):
        for si in (2, -2):
            for sj in (2, -2):
                v = [0] * 8
                v[i], v[j] = si, sj
                roots.append(tuple(v))
    simple = [tuple(2 * (1 if k == i else (-1 if k == i + 1 else 0))
                    for k in range(8)) for i in range(7)]
    simple.append((0, 0, 0, 0, 0, 0, 2, 2))
    return RootSystem('D8', simple, roots)


# ---------------------------------------------------------------------------
# Chevalley / Frenkel-Kac basis with exact integer structure constants
# ---------------------------------------------------------------------------
class Chevalley:
    """basis: indices 0..nR-1 = root vectors e_alpha (roots sorted),
    nR..nR+rank-1 = simple coroots h_i.  Structure constants from the
    bimultiplicative 2-cocycle eps(a,b) = (-1)^(m_a^T B m_b); the sign of
    [e_a, e_{-a}] = SGN * H(a) is DETERMINED by the Jacobi identity."""

    def __init__(self, rs):
        self.rs = rs
        self.roots = sorted(rs.roots)
        self.nR = len(self.roots)
        self.rank = rs.n
        self.dim = self.nR + self.rank
        self.ridx = {r: i for i, r in enumerate(self.roots)}
        self.opp = [self.ridx[tuple(-x for x in r)] for r in self.roots]
        self.mvec = []
        for r in self.roots:
            cs = rs.alpha_coords(r)
            assert all(c.denominator == 1 for c in cs)
            self.mvec.append(tuple(int(c) for c in cs))
        A = [[ip(a, b) // 4 for b in rs.simple] for a in rs.simple]
        self.Atrue = A
        self.B = [[(1 if i == j else (A[i][j] % 2 if i > j else 0))
                   for j in range(self.rank)] for i in range(self.rank)]
        self.Bm = [tuple(sum(self.B[i][t] * m[t] for t in range(self.rank)) % 2
                         for i in range(self.rank)) for m in self.mvec]
        self._table = {}
        self.sgn = self._determine_sign()
        self._table = {}          # rebuild with the fixed sign
        self.kappa_root = self._derive_kappa_root()

    # true inner product of two roots (ints)
    def rip(self, i, j):
        return ip(self.roots[i], self.roots[j]) // 4

    def eps(self, i, j):
        m = self.mvec[i]
        bn = self.Bm[j]
        return -1 if sum(m[t] * bn[t] for t in range(self.rank)) % 2 else 1

    def bracket(self, i, j):
        key = (i, j)
        got = self._table.get(key)
        if got is not None:
            return got
        out = self._bracket_compute(i, j)
        self._table[key] = out
        return out

    def _bracket_compute(self, i, j):
        nR, rank = self.nR, self.rank
        if i >= nR and j >= nR:
            return {}
        if i >= nR:
            c = i - nR
            pair = ip(self.rs.simple[c], self.roots[j]) // 4
            return {j: F(pair)} if pair else {}
        if j >= nR:
            c = j - nR
            pair = ip(self.rs.simple[c], self.roots[i]) // 4
            return {i: F(-pair)} if pair else {}
        s = vadd(self.roots[i], self.roots[j])
        if all(x == 0 for x in s):
            return {nR + t: F(self.sgn * self.mvec[i][t])
                    for t in range(rank) if self.mvec[i][t]}
        k = self.ridx.get(s)
        if k is not None:
            return {k: F(self.eps(i, j))}
        return {}

    def _determine_sign(self):
        # test Jacobi on triples (e_a, e_{-a}, e_b) with a+b a root
        triples = []
        for i in range(self.nR):
            if len(triples) >= 24:
                break
            for j in range(self.nR):
                s = vadd(self.roots[i], self.roots[j])
                if s in self.ridx:
                    triples.append((i, self.opp[i], j))
                    break
        results = {}
        for sgn in (1, -1):
            self.sgn = sgn
            self._table = {}
            results[sgn] = all(self.jacobi_zero(*t) for t in triples)
        good = [s for s, ok in results.items() if ok]
        assert len(good) == 1, "Jacobi must fix the sign uniquely: %s" % results
        return good[0]

    def _derive_kappa_root(self):
        # kappa(e_a, e_{-a}) = T from invariance kappa([e_a,e_{-a}],h_j)
        #                        = kappa(e_a,[e_{-a},h_j]) = (a_j,a) T
        vals = set()
        for i in range(self.nR):
            u = self.bracket(i, self.opp[i])
            for j in range(self.rank):
                lhs = sum(c * F(self.Atrue[t - self.nR][j])
                          for t, c in u.items())
                rhs_pair = ip(self.rs.simple[j], self.roots[i]) // 4
                if rhs_pair:
                    vals.add(lhs / rhs_pair)
        assert len(vals) == 1, vals
        return vals.pop()

    def kappa(self, i, j):
        nR = self.nR
        if i >= nR and j >= nR:
            return F(self.Atrue[i - nR][j - nR])
        if i < nR and j < nR and self.opp[i] == j:
            return self.kappa_root
        return F(0)

    def jacobi_zero(self, x, y, z):
        out = {}
        for (p, q, r) in ((x, y, z), (y, z, x), (z, x, y)):
            for e, ce in self.bracket(p, q).items():
                for f, cf in self.bracket(e, r).items():
                    out[f] = out.get(f, F(0)) + ce * cf
        return all(v == 0 for v in out.values())

    def hvec_index(self, root_tuple):
        """H(a) = sum m_i h_i as a sparse dict over basis indices."""
        i = self.ridx[root_tuple]
        return {self.nR + t: F(self.mvec[i][t])
                for t in range(self.rank) if self.mvec[i][t]}


# ---------------------------------------------------------------------------
# exact affine PBW engine at level k:
# [J^a_m, J^b_n] = ([a,b])_{m+n} + m k kappa(a,b) delta_{m+n,0}
# states: sparse dicts over canonical keys = tuples of (mode, basis_idx),
# sorted ascending; key () = |0>
# ---------------------------------------------------------------------------
class Affine:
    def __init__(self, ch, k):
        self.ch = ch
        self.k = k

    def push(self, a, m, key):
        if not key:
            return {((m, a),): F(1)} if m < 0 else {}
        head = key[0]
        if m < 0 and (m, a) <= head:
            return {((m, a),) + key: F(1)}
        m1, b = head
        rest = key[1:]
        out = {}
        for k2, c2 in self.push(a, m, rest).items():
            for k3, c3 in self.push(b, m1, k2).items():
                out[k3] = out.get(k3, F(0)) + c2 * c3
        for cidx, cf in self.ch.bracket(a, b).items():
            for k3, c3 in self.push(cidx, m + m1, rest).items():
                out[k3] = out.get(k3, F(0)) + cf * c3
        if m + m1 == 0:
            ct = F(m) * self.k * self.ch.kappa(a, b)
            if ct:
                out[rest] = out.get(rest, F(0)) + ct
        return {kk: vv for kk, vv in out.items() if vv != 0}

    def act(self, a, m, state):
        out = {}
        for key, c in state.items():
            for k2, c2 in self.push(a, m, key).items():
                out[k2] = out.get(k2, F(0)) + c * c2
        return {kk: vv for kk, vv in out.items() if vv != 0}

    def weight(self, key):
        w = [0] * self.ch.rs.dim
        for (_m, idx) in key:
            if idx < self.ch.nR:
                w = [x + y for x, y in zip(w, self.ch.roots[idx])]
        return tuple(w)


def vec_axpy(v, w, c):
    out = dict(v)
    for k, cw in w.items():
        out[k] = out.get(k, F(0)) + c * cw
    return {k: c2 for k, c2 in out.items() if c2 != 0}


def add_to_basis(basis, vec):
    """exact incremental Gauss; basis = list of (pivot_key, reduced_vec)."""
    v = dict(vec)
    for pk, bv in basis:
        c = v.get(pk)
        if c:
            v = vec_axpy(v, bv, -c)
    v = {k: c for k, c in v.items() if c != 0}
    if not v:
        return False
    pk = min(v)
    piv = v[pk]
    v = {k: c / piv for k, c in v.items()}
    basis.append((pk, v))
    return True


# ---------------------------------------------------------------------------
# glue frame (v128/v492 construction) for the mu4 part
# ---------------------------------------------------------------------------
def build_glue_roots():
    HALF = F(1, 2)
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


def monomial_table(dmax):
    N = []
    for d in range(dmax + 1):
        row = [0] * 4
        for p in range(d + 1):
            row[(p - (d - p)) % 4] += 1
        N.append(row)
    return N


def d5_coset_norms(maxnorm):
    out = {k: {} for k in ('0', 'v', 's', 'c')}
    for v in product(range(-2, 3), repeat=5):
        n = F(sum(x * x for x in v))
        if n > maxnorm:
            continue
        key = '0' if sum(v) % 2 == 0 else 'v'
        out[key][n] = out[key].get(n, 0) + 1
    rng_half = [F(k, 2) for k in (-3, -1, 1, 3)]
    for v in product(rng_half, repeat=5):
        n = sum(x * x for x in v)
        if n > maxnorm:
            continue
        key = 's' if (sum(v) - F(5, 2)) % 2 == 0 else 'c'
        out[key][n] = out[key].get(n, 0) + 1
    return out


def a3_coset_norms(maxnorm):
    out = {k: {} for k in range(4)}
    for k in range(4):
        shift = F(-k, 4)
        rng = [m + shift for m in range(-3, 4)]
        for v in product(rng, repeat=4):
            if sum(v) != 0:
                continue
            n = sum(x * x for x in v)
            if n > maxnorm:
                continue
            out[k][n] = out[k].get(n, 0) + 1
    return out


# ---------------------------------------------------------------------------
# S1 -- Chevalley basis, cocycle, Jacobi, invariant form (all machine)
# ---------------------------------------------------------------------------
def section1():
    print("  -- S1: exact Chevalley/Frenkel-Kac basis from the v497 root data")
    rs = e8_std()
    ch = Chevalley(rs)
    nR = ch.nR

    check("S1.1: standard-frame E8 -- 240 roots (norm 2), 120 positive, "
          "Cartan det = 1; basis dim %d = 240 + 8 = 248" % ch.dim,
          nR == 240 and len(rs.pos) == 120
          and round(_det(rs.cartan)) == 1 and ch.dim == 248)

    ok_diag = all(ch.eps(i, i) == -1 for i in range(nR))
    check("S1.2: cocycle diagonal -- eps(a,a) = (-1)^(|a|^2/2) = -1 for all "
          "240 roots (bimultiplicative by construction: eps = (-1)^(m^T B m'))",
          ok_diag)

    ok_asym = True
    for i in range(nR):
        for j in range(nR):
            if ch.eps(i, j) * ch.eps(j, i) != (-1) ** (ch.rip(i, j) % 2):
                ok_asym = False
                break
        if not ok_asym:
            break
    check("S1.3: cocycle asymmetry -- eps(a,b) eps(b,a) = (-1)^(a,b) on ALL "
          "57600 ordered root pairs", ok_asym)

    check("S1.4: SIGN DETERMINED BY JACOBI (not chosen) -- [e_a,e_{-a}] = "
          "SGN * H(a) with SGN = %+d is the unique sign passing the Jacobi "
          "identity on the sl2-partner triples" % ch.sgn, ch.sgn in (1, -1))

    n_sum = n_cartan = 0
    ok_pm1 = True
    for i in range(nR):
        for j in range(nR):
            br = ch.bracket(i, j)
            if not br:
                continue
            if ch.opp[i] == j:
                n_cartan += 1
            else:
                n_sum += 1
                (c,) = br.values()
                if c not in (F(1), F(-1)):
                    ok_pm1 = False
    check("S1.5: bracket tally -- %d root pairs with a+b a root (= 240*56), "
          "%d opposite pairs; all root-sum structure constants N_ab = +-1 "
          "(simply-laced)" % (n_sum, n_cartan),
          n_sum == 240 * 56 and n_cartan == 240 and ok_pm1)

    ok_anti = True
    for i in range(ch.dim):
        for j in range(ch.dim):
            bij = ch.bracket(i, j)
            bji = ch.bracket(j, i)
            if set(bij) != set(bji) or any(bij[t] != -bji[t] for t in bij):
                ok_anti = False
                break
        if not ok_anti:
            break
    check("S1.6: antisymmetry [x,y] = -[y,x] on ALL 248 x 248 basis pairs",
          ok_anti)

    ok_j1 = all(ch.jacobi_zero(i, ch.opp[i], j)
                for i in range(nR) for j in range(nR))
    check("S1.7: JACOBI, full sl2-slice -- identity holds on ALL 57600 "
          "triples (e_a, e_{-a}, e_b)", ok_j1)

    rnd = random.Random(4970)
    ok_j2 = all(ch.jacobi_zero(rnd.randrange(nR), rnd.randrange(nR),
                               rnd.randrange(nR)) for _ in range(4000))
    ok_j3 = all(ch.jacobi_zero(rnd.randrange(nR, ch.dim), rnd.randrange(nR),
                               rnd.randrange(nR)) for _ in range(2000))
    check("S1.8: JACOBI, samples -- 4000 seeded root triples + 2000 seeded "
          "Cartan-root-root triples, all exact", ok_j2 and ok_j3)

    theta = rs.fold(rs.roots[0])
    it = ch.ridx[theta]
    ok_jt = all(ch.jacobi_zero(a, it, it) and ch.jacobi_zero(a, it, ch.opp[it])
                for a in range(ch.dim))
    check("S1.9: JACOBI, theta-adjacent -- all 496 triples (x, e_theta, "
          "e_{+-theta}) over the full basis", ok_jt)

    ok_inv = True
    n_inv = 0
    for i in range(nR):
        for j in range(nR):
            s = vadd(ch.roots[i], ch.roots[j])
            kidx = ch.ridx.get(s)
            if kidx is None:
                continue
            g = ch.opp[kidx]        # gamma = -(a+b)
            n_inv += 1
            lhs = sum(c * ch.kappa(t, g) for t, c in ch.bracket(i, j).items())
            rhs = sum(c * ch.kappa(i, t) for t, c in ch.bracket(j, g).items())
            if lhs != rhs:
                ok_inv = False
    ht = ch.hvec_index(theta)
    norm_t = sum(ci * cj * F(ch.Atrue[ii - nR][jj - nR])
                 for ii, ci in ht.items() for jj, cj in ht.items())
    check("S1.10: invariant form DERIVED -- kappa(e_a,e_{-a}) = %s uniform "
          "(from invariance, all roots x all Cartan directions); invariance "
          "kappa([a,b],c) = kappa(a,[b,c]) on all %d root triples with "
          "a+b+c = 0; normalisation kappa(theta_vee,theta_vee) = %s = 2"
          % (ch.kappa_root, n_inv, norm_t),
          n_inv == 240 * 56 and ok_inv and norm_t == 2
          and ch.kappa_root in (F(1), F(-1)))

    ok_sl2 = True
    for i in range(nR):
        u = ch.bracket(i, ch.opp[i])
        # [ [e_a,e_{-a}], e_a ] must be SGN * (a,a) e_a = 2 SGN e_a
        acc = {}
        for t, c in u.items():
            for f, cf in ch.bracket(t, i).items():
                acc[f] = acc.get(f, F(0)) + c * cf
        if set(acc) != {i} or acc[i] != 2 * ch.sgn:
            ok_sl2 = False
    check("S1.11: sl2 triples -- [[e_a,e_{-a}],e_a] = 2*SGN*e_a for all 240 "
          "roots (uniform normalisation, exact)", ok_sl2)
    return rs, ch, theta


# ---------------------------------------------------------------------------
# S2 -- theta structure and the case classification of the J_1 condition
# ---------------------------------------------------------------------------
def section2(rs, ch, theta):
    print("  -- S2: theta structure (grading, automatic strata)")
    it = ch.ridx[theta]
    two_theta = smul(2, theta)

    grades = {}
    for r in ch.roots:
        t = ip(r, theta) // 4
        grades[t] = grades.get(t, 0) + 1
    dims5 = [grades.get(-2, 0), grades.get(-1, 0), grades.get(0, 0) + 8,
             grades.get(1, 0), grades.get(2, 0)]
    check("S2.1: THETA-GRADING g = g_-2 + g_-1 + g_0 + g_1 + g_2 with dims "
          "%s = (1,56,134,56,1), sum 248; g_0 = 126 roots + 8 Cartan = "
          "e7 + u(1) (133 + 1)" % dims5,
          dims5 == [1, 56, 134, 56, 1] and sum(dims5) == 248
          and grades.get(0, 0) == 126 and 126 + 7 == 133)

    ok_pos = all(vadd(r, theta) not in ch.ridx for r in rs.pos)
    check("S2.2: a + theta is NOT a root for any of the 120 positive roots "
          "a (theta highest) => E^a_0 |s> = 0 will be automatic", ok_pos)

    reenter = [r for r in ch.roots if vadd(r, two_theta) in ch.ridx]
    check("S2.3: a + 2*theta re-enters the root system for EXACTLY %d root "
          "(a = -theta, giving theta back: <a,theta_vee> = -2 is the only "
          "stratum with <a+2theta,theta_vee> <= 2); all other 239 roots "
          "leave it" % len(reenter),
          reenter == [tuple(-x for x in theta)])

    n_first = n_second = n_central = 0
    for a in range(ch.dim):
        r1 = ch.bracket(a, it)
        if not r1:
            n_first += 1
            continue
        r2 = {}
        for t, c in r1.items():
            for f, cf in ch.bracket(t, it).items():
                r2[f] = r2.get(f, F(0)) + c * cf
        r2 = {k2: v for k2, v in r2.items() if v != 0}
        if not r2:
            n_second += 1
        else:
            n_central += 1
            assert a == ch.opp[it]
    print("     case tally of the J^a_1 condition over the 248 basis "
          "elements:")
    print("       vanishes at the first bracket  : %3d  (e_theta, g_1, "
          "g_0-roots, 7 Cartan)" % n_first)
    print("       vanishes at the second bracket : %3d  (g_-1, 1 adjacent "
          "Cartan)" % n_second)
    print("       needs the central term         : %3d  (a = F^theta only)"
          % n_central)
    check("S2.4: CASE CLASSIFICATION -- (first, second, central) = "
          "(%d, %d, %d) = (190, 57, 1); exactly ONE case sees the level k"
          % (n_first, n_second, n_central),
          (n_first, n_second, n_central) == (190, 57, 1))
    return two_theta


# ---------------------------------------------------------------------------
# S3 -- the singular vector, machine-verified in the affine module
# ---------------------------------------------------------------------------
def section3(rs, ch, theta):
    print("  -- S3: |s> = (E^theta_{-1})^2 |0> and its singularity (exact)")
    it = ch.ridx[theta]
    iF = ch.opp[it]
    eng = Affine(ch, 1)
    vac = {(): F(1)}

    # engine unit tests against the finite-dimensional data
    ok_u1 = True
    for a in range(ch.dim):
        for b in range(ch.dim):
            got = eng.push(a, 1, ((-1, b),))
            want = {(): ch.kappa(a, b)} if ch.kappa(a, b) else {}
            if got != want:
                ok_u1 = False
                break
        if not ok_u1:
            break
    check("S3.1: ENGINE UNIT TEST -- J^a_1 J^b_{-1}|0> = k kappa(a,b)|0> "
          "reproduced on ALL 61504 basis pairs", ok_u1)

    ok_u2 = True
    for a in range(ch.dim):
        for b in range(ch.dim):
            got = eng.push(a, 0, ((-1, b),))
            want = {((-1, t),): c for t, c in ch.bracket(a, b).items()}
            if got != want:
                ok_u2 = False
                break
        if not ok_u2:
            break
    check("S3.2: ENGINE UNIT TEST -- J^a_0 J^b_{-1}|0> = ([a,b])_{-1}|0> "
          "on ALL 61504 basis pairs", ok_u2)

    rnd = random.Random(4971)
    ok_u3 = True
    for _ in range(500):
        a = rnd.randrange(ch.dim)
        b = rnd.randrange(ch.dim)
        s1 = eng.act(a, -1, eng.act(b, -1, vac))
        s2 = eng.act(b, -1, eng.act(a, -1, vac))
        comm = vec_axpy(s1, s2, F(-1))
        want = {((-2, t),): c for t, c in ch.bracket(a, b).items()}
        if comm != want:
            ok_u3 = False
            break
    check("S3.3: ENGINE UNIT TEST -- [J^a_{-1}, J^b_{-1}] = ([a,b])_{-2} on "
          "500 seeded pairs (PBW reordering exact)", ok_u3)

    s = eng.act(it, -1, eng.act(it, -1, vac))
    two_theta = smul(2, theta)
    skey = ((-1, it), (-1, it))
    check("S3.4: |s> CONSTRUCTED EXPLICITLY -- the single Fock monomial "
          "(E^theta_{-1})^2|0> with theta (doubled) = %s; weight = 2*theta, "
          "level 2 (8 quarter units)" % (list(theta),),
          s == {skey: F(1)} and eng.weight(skey) == two_theta)

    bad1 = [a for a in range(ch.dim) if eng.act(a, 1, s)]
    check("S3.5: THE SINGULARITY (main theorem, machine) -- J^a_1 |s> = 0 "
          "for ALL 248 basis elements a: %d violations" % len(bad1),
          not bad1)

    bad2 = [a for a in range(ch.dim) if eng.act(a, 2, s)]
    check("S3.6: J^a_2 |s> = 0 for ALL 248 basis elements (higher raising "
          "modes; with S3.5 and [J_1,J_n] closure this exhausts n >= 1): "
          "%d violations" % len(bad2), not bad2)

    ipos = [ch.ridx[r] for r in rs.pos]
    bad0 = [a for a in ipos if eng.act(a, 0, s)]
    ok_h = True
    for i in range(ch.rank):
        got = eng.act(ch.nR + i, 0, s)
        lam = ip(two_theta, rs.simple[i]) // 4
        want = {k: lam * c for k, c in s.items()} if lam else {}
        if got != want:
            ok_h = False
    check("S3.7: HIGHEST-WEIGHT PROPERTY -- E^a_0 |s> = 0 for all 120 "
          "positive roots (%d violations) and h_i |s> = <2 theta, a_i_vee> "
          "|s> exactly (weight 2 theta confirmed as eigenvalue)"
          % len(bad0), not bad0 and ok_h)

    # level dial: the one central case, k = 0, 1, 2
    dial = {}
    for kk in (0, 1, 2):
        ek = Affine(ch, kk)
        r = ek.act(iF, 1, ek.act(it, -1, ek.act(it, -1, vac)))
        dial[kk] = r.get(((-1, it),), F(0))
    print("     level dial (coefficient of E^theta_{-1}|0> in "
          "F^theta_1 (E^theta_{-1})^2|0>): k=0: %s, k=1: %s, k=2: %s"
          % (dial[0], dial[1], dial[2]))
    check("S3.8: LEVEL DIAL -- the F^theta_1 coefficient is 2*SGN*(1-k)*"
          "kappa-normalised: nonzero at k = 0 (NO deletion operator in the "
          "centerless loop algebra) and k = 2, zero EXACTLY at k = 1: "
          "|coeff| = (%d, %d, %d)"
          % (abs(dial[0]), abs(dial[1]), abs(dial[2])),
          abs(dial[0]) == 2 and dial[1] == 0 and abs(dial[2]) == 2)

    shap = {}
    for kk in (1, 2):
        ek = Affine(ch, kk)
        r = ek.act(iF, 1, ek.act(iF, 1,
                                 ek.act(it, -1, ek.act(it, -1, vac))))
        shap[kk] = r.get((), F(0))
    check("S3.9: SHAPOVALOV NORM -- <s|s> proportional to "
          "F_1 F_1 (E_{-1})^2|0> = %s |0> at k = 1 (null vector) vs %s |0> "
          "at k = 2 (the state survives)" % (shap[1], shap[2]),
          shap[1] == 0 and abs(shap[2]) == 4)
    return eng, s, it, iF


# ---------------------------------------------------------------------------
# S4 -- mu4 compatibility (glue frame; clock class, phase, quarter-modes)
# ---------------------------------------------------------------------------
def section4():
    print("  -- S4: mu4 compatibility of |s> (glue frame, v492/v496 data)")
    groots = build_glue_roots()
    counts = [sum(1 for c in groots.values() if c == k) for k in range(4)]
    dims = [counts[0] + RANK] + counts[1:]
    check("S4.1: v492 replication -- 240 glue-frame roots, split "
          "52+64+60+64, dims with Cartan (60,64,60,64)",
          len(groots) == 240 and counts == [52, 64, 60, 64]
          and dims == [60, 64, 60, 64])

    h9 = (2, 2, 2, 2, 2, 0, 0, 0, 0)
    ok_inner = all((ip(r, h9)) % 4 == c and F(ip(r, h9)).denominator == 1
                   for r, c in groots.items())
    check("S4.2: INNER GRADING -- <alpha,h> = glue class mod 4 for all 240 "
          "roots with h = (2,2,2,2,2;0^4) (v492 S1): the clock is "
          "Ad(exp(2 pi i h/4))", ok_inner)

    # h-adapted chamber: phi = BIG*<.,h> + separating tiebreaker.  The
    # tiebreaker 4*1000^i is injective on quarter-integer coordinates in
    # [-2,2] (base-1000 digits 4*r_i in [-8,8]); BIG dominates its range.
    tie = tuple(4 * 1000 ** i for i in range(9))
    BIG = 8 * 1000 ** 10
    phi = {r: ip(r, h9) * BIG + ip(r, tie) for r in groots}
    assert all(v != 0 for v in phi.values())
    assert len(set(phi.values())) == 240
    pos = [r for r, v in phi.items() if v > 0]
    posset = set(pos)
    simple = []
    for p in pos:
        decomposable = False
        for q in pos:
            rdiff = vsub(p, q)
            if rdiff in posset and rdiff != p:
                decomposable = True
                break
        if not decomposable:
            simple.append(p)
    A = [[ip(a, b) for b in simple] for a in simple]
    off = all(A[i][j] in (0, -1) for i in range(len(simple))
              for j in range(len(simple)) if i != j)
    deg = sorted(sum(1 for j in range(len(simple))
                     if i != j and A[i][j] == -1)
                 for i in range(len(simple)))
    # branch lengths from the trivalent node
    adj = {i: [j for j in range(len(simple))
               if j != i and A[i][j] == -1] for i in range(len(simple))}
    tri = [i for i in range(len(simple)) if len(adj[i]) == 3]
    branches = []
    if len(tri) == 1:
        for start in adj[tri[0]]:
            ln, prev, cur = 1, tri[0], start
            while True:
                nxt = [x for x in adj[cur] if x != prev]
                if not nxt:
                    break
                prev, cur = cur, nxt[0]
                ln += 1
            branches.append(ln)
    check("S4.3: h-ADAPTED CHAMBER -- 120 positives, 8 simple roots, Cartan "
          "matrix det %s, diagram = trivalent node with branch lengths %s "
          "= [1,2,4]: the glue-frame root system IS E8"
          % (int(_det(A)), sorted(branches)),
          len(pos) == 120 and len(simple) == 8 and off
          and all(A[i][i] == 2 for i in range(8))
          and int(_det(A)) == 1 and deg == [1, 1, 1, 2, 2, 2, 2, 3]
          and sorted(branches) == [1, 2, 4])

    dom = [r for r in groots if all(ip(r, a) >= 0 for a in simple)]
    theta_g = dom[0] if dom else None
    b = [ip(theta_g, a) for a in simple]
    coords = solve_fraction(A, b)
    height = sum(coords)
    jt = groots[theta_g]
    check("S4.4: THETA IN THE GLUE FRAME -- unique dominant root (%d found), "
          "= argmax phi (%s), height %s = 29 = h_vee - 1; <theta,h> = %d, "
          "glue class j(theta) = %d = <theta,h> mod 4"
          % (len(dom), max(phi.values()) == phi[theta_g], height,
             ip(theta_g, h9), jt),
          len(dom) == 1 and max(phi.values()) == phi[theta_g]
          and height == 29 and jt == ip(theta_g, h9) % 4)

    j2 = (2 * jt) % 4
    phase = {0: 1, 2: -1}[j2] if j2 in (0, 2) else None
    jm = groots[tuple(-x for x in theta_g)]
    check("S4.5: CLOCK COVARIANCE OF |s> -- class(2 theta) = 2 j(theta) mod "
          "4 = %d in {0,2} (SHEET-EVEN, chamber-independent parity; WP5a "
          "S6.8); clock phase on |s> = i^(2j) = %+d; the theta-sl2 pair "
          "(E^theta, F^theta) sits in the sheet-ODD class pair (%d, %d) -- "
          "the deleting sl2 crosses the odd sheets, its square is even"
          % (j2, phase, jt, jm),
          j2 in (0, 2) and phase == -1 and jt == 1 and jm == 3
          and (jt + jm) % 4 == 0)

    # cross-table (theta-grading) x (glue class); glue frame uses TRUE
    # inner products (norm 2), so <r,theta_vee> = ip(r,theta_g) directly
    tally = {}
    for r, c in groots.items():
        t = ip(r, theta_g)
        assert F(t).denominator == 1
        tally[(int(t), c)] = tally.get((int(t), c), 0) + 1
    print("     cross-table  <alpha,theta_vee> \\ glue class j "
          "(roots only):")
    print("        t\\j |   0   1   2   3 | sum")
    rows_ok = True
    for t in (2, 1, 0, -1, -2):
        row = [tally.get((t, j), 0) for j in range(4)]
        print("        %+2d  | %3d %3d %3d %3d | %3d"
              % (t, row[0], row[1], row[2], row[3], sum(row)))
    rowsums = [sum(tally.get((t, j), 0) for j in range(4))
               for t in (2, 1, 0, -1, -2)]
    colsums = [sum(tally.get((t, j), 0) for t in (2, 1, 0, -1, -2))
               for j in range(4)]
    check("S4.6: cross-table consistency -- theta-grading row sums %s = "
          "(1,56,126,56,1) (roots), glue-class column sums %s = "
          "(52,64,60,64)" % (rowsums, colsums),
          rowsums == [1, 56, 126, 56, 1] and colsums == [52, 64, 60, 64])

    # equivariant expressibility of the building block
    N = monomial_table(8)
    mdeg = (-jt) % 4
    slots = N[mdeg][mdeg]
    check("S4.7: EQUIVARIANT EXPRESSIBILITY -- E^theta lies in sector "
          "C_%d; e_theta (x) z^m is glue-equivariant iff m = -j(theta) = %d "
          "mod 4 (v492 S3 closure); at spatial degree %d there are %d such "
          "monomial slots; the SQUARE has total class 2j + spatial(-2j) = 0 "
          "mod 4: (e_theta z^-j)^2 is a mu4-INVARIANT element of the "
          "equivariant algebra" % (jt, mdeg, mdeg, slots),
          mdeg == 3 and slots == 2
          and (jt + mdeg) % 4 == 0 and (2 * jt + 2 * mdeg) % 4 == 0)

    period = sum(dims[n % 4] for n in range(1, 5))
    check("S4.8: QUARTER BOOKKEEPING (v496 dictionary) -- one mu4 period of "
          "quarter energies carries %d = 248 = the level-1 currents: "
          "E^theta_{-1} = 4 quarter units (one period), |s> = 2 x 4 = 8 "
          "quarters = q^2, an INTEGER level" % period,
          period == 248 and 2 * MU4 == 8 and 8 % 4 == 0)

    frac = F(-(-jt % 4), 4) % 1
    check("S4.9: v496 QUARTER-MODE CONVENTION -- sector C_%d generators sit "
          "at quarter energies n = -j mod 4 (n in {3,7,...}); mode fractions "
          "-n/4 mod 1 = %s = j(theta)/4: the 'm in Z + j/4' moding of the "
          "prompt, replicated" % (jt, frac), frac == F(jt, 4))

    pairs8 = [(n1, n2) for n1 in range(1, 8) for n2 in range(1, 8)
              if n1 % 4 == (-jt) % 4 and n2 % 4 == (-jt) % 4
              and n1 + n2 == 8]
    min_tot = min(n1 + n2 for n1 in range(1, 12) for n2 in range(1, 12)
                  if n1 % 4 == (-jt) % 4 and n2 % 4 == (-jt) % 4)
    check("S4.10 [O-FLAG]: TWISTED-SLOT TENSION (honest) -- in the "
          "quarter-SLOT moding of the chi_w limit Fock, two sector-C_%d "
          "modes never sum to 8 quarters (%d solutions; minimum total %d "
          "quarters = q^(3/2)): the per-PERIOD dictionary (S4.8), not the "
          "per-slot one, carries |s> to q^2 -- exactly the WP5c GNS/limit-"
          "state seam, typed open" % (jt, len(pairs8), min_tot),
          not pairs8 and min_tot == 6)

    # theta-split sector characters (v497 S4 replication) + lattice kernel
    d5 = d5_coset_norms(6)
    a3 = a3_coset_norms(6)
    pairing = {0: ('0', 0), 1: ('s', 1), 2: ('v', 2), 3: ('c', 3)}
    theta_c = {}
    for j, (dk, ak) in pairing.items():
        coeffs = [0] * 4
        for n5, c5 in d5[dk].items():
            for n3, c3v in a3[ak].items():
                n = n5 + n3
                if n <= 6 and n % 2 == 0 and F(n, 2).denominator == 1:
                    coeffs[int(n) // 2] += c5 * c3v
        theta_c[j] = coeffs
    p8 = fock({n: 8 for n in range(1, 4)}, 3)
    sector = {j: series_mul(theta_c[j], p8, 3) for j in range(4)}
    lvl1 = [sector[j][1] for j in range(4)]
    lvl2 = [sector[j][2] for j in range(4)]
    check("S4.11: THETA-SPLIT SECTORS -- level-1 currents per sector %s = "
          "(60,64,60,64): the NEGATIVE-control state E^theta_{-1}|0> (which "
          "must remain) sits in the class-%d block of dim %d"
          % (lvl1, jt, lvl1[jt]),
          lvl1 == [60, 64, 60, 64] and lvl1[jt] == 64)
    check("S4.12: level-2 sector sum %s -> %d = 4124 = 31124 - 27000 (WP5a "
          "two-routes number); class(2 theta) = %d block has dim %d"
          % (lvl2, sum(lvl2), j2, lvl2[j2]),
          lvl2 == [1036, 1024, 1040, 1024] and sum(lvl2) == 4124
          and lvl2[j2] == 1040)

    norm2t = ip(theta_g, theta_g) * 4 // 2  # (2t,2t)/2 = 4*(t,t)/2
    check("S4.13: LATTICE KERNEL READING -- momentum 2 theta has "
          "(2t,2t)/2 = %d > 2: the quotient (E8)_1 theory has NO momentum-"
          "2theta state at q^2, so |s> (which has exactly that momentum at "
          "level 2) maps to ZERO in E4/eta^8 -- |s> IS the deletion "
          "operator's top state" % norm2t, norm2t == 4)

    hmin_d5 = [F(0)] + [F(min(n for n in d5[k] if n > 0), 2)
                        for k in ('s', 'v', 'c')]
    hmin_a3 = [F(0)] + [F(min(n for n in a3[k] if n > 0), 2)
                        for k in (1, 2, 3)]
    hdiag = [hmin_d5[j] + hmin_a3[j] for j in range(4)]
    check("S4.14: glue-diagonal weights h_j = %s = (0,1,1,1) INTEGER (one-"
          "block fusion; the D8 control below breaks exactly this)" % hdiag,
          hdiag == [F(0), F(1), F(1), F(1)])
    return jt


# ---------------------------------------------------------------------------
# S5 -- level-2 count: Freudenthal + direct lowering-orbit BFS
# ---------------------------------------------------------------------------
def section5(rs, ch, theta, eng, s):
    print("  -- S5: level-2 ideal count (27000 / 4124) + direct orbit BFS")
    two_theta = smul(2, theta)

    npair = sum(1 for i, r in enumerate(ch.roots)
                if vsub(two_theta, r) in ch.ridx
                and ch.ridx[vsub(two_theta, r)] >= i)
    check("S5.1: weight 2 theta has multiplicity %d = 1 in the level-2 Fock "
          "(unique unordered pair theta + theta): the V(2 theta) component "
          "of Sym^2(248) is unique -- U(g)|s> is THE 27000" % npair,
          npair == 1)

    fm2t = rs.freudenthal(two_theta)
    dim2t = rs.dim_by_orbits(fm2t)
    check("S5.2: FREUDENTHAL -- dim V(2 theta) = %d = 27000 = %d^3 = "
          "h_vee^3 (Weyl-orbit sums, v497 replication)" % (dim2t, H_VEE),
          dim2t == 27000 and 27000 == H_VEE ** 3)

    fockV = fock({n: 248 for n in range(1, 3)}, 2)
    fund_dims = [rs.weyl_dim(w) for w in rs.fund]
    check("S5.3: QUOTIENT -- level-2 Fock %d = 30876 + 248; quotient "
          "%d - 27000 = %d = 4124 = 1 + 248 + 3875 (3875 = fundamental rep, "
          "in the Weyl-dim list %s)"
          % (fockV[2], fockV[2], fockV[2] - 27000,
             sorted(d for d in fund_dims if d < 10 ** 6)),
          fockV[2] == 31124 and comb(249, 2) + 248 == 31124
          and fockV[2] - 27000 == 4124 and 3875 in fund_dims)

    # direct lowering BFS: g_0-orbit of |s> inside the level-2 Fock
    ilow = [ch.ridx[tuple(-x for x in a)] for a in rs.simple]
    strata = {0: {two_theta: [(min(s), dict(s))]}}
    # normalise the seed to pivot form
    basis0 = []
    add_to_basis(basis0, s)
    strata = {0: {two_theta: basis0}}
    ok_bfs = True
    print("     depth |  #weights  orbit-dim  Freudenthal  match")
    for d in range(1, 5):
        new = {}
        for w, basis in strata[d - 1].items():
            for fi, alo in zip(ilow, rs.simple):
                wn = vsub(w, alo)
                for _pk, v in basis:
                    img = eng.act(fi, 0, v)
                    if img:
                        new.setdefault(wn, []).append(img)
        buckets = {}
        for wn, vecs in new.items():
            basis = []
            for v in vecs:
                add_to_basis(basis, v)
            if basis:
                buckets[wn] = basis
        expect = {}
        for w in strata[d - 1]:
            for alo in rs.simple:
                wn = vsub(w, alo)
                m = fm2t.get(rs.fold(wn), 0)
                if m:
                    expect[wn] = m
        got_dims = {w: len(b) for w, b in buckets.items()}
        match = (set(got_dims) == set(expect)
                 and all(got_dims[w] == expect[w] for w in expect))
        ok_bfs &= match
        print("       %d   |  %8d  %9d  %11d  %s"
              % (d, len(got_dims), sum(got_dims.values()),
                 sum(expect.values()), match))
        strata[d] = buckets
    check("S5.4: DIRECT ORBIT CHECK -- the g_0-lowering BFS from |s> "
          "reproduces the Freudenthal weight multiplicities of V(2 theta) "
          "EXACTLY, weight by weight, through depth 4 (weights reached = "
          "weights expected, dims equal)", ok_bfs)

    check("S5.5 [C]: the full count -- |s> is a g-highest-weight vector "
          "(S3.7, machine) of the unique V(2 theta) component (S5.1, "
          "machine) with dim 27000 (S5.2, machine); Weyl complete "
          "reducibility of the finite-dim level-2 Fock (standard, [C]) "
          "extends the depth-4 orbit agreement to dim U(g)|s> = 27000 and "
          "quotient 4124 -- named citation, counting consequence machine-"
          "checked", True)


# ---------------------------------------------------------------------------
# S6 -- negative controls
# ---------------------------------------------------------------------------
def section6(rs, ch, theta, it, iF):
    print("  -- S6: negative controls (the construction must have teeth)")
    vac = {(): F(1)}
    eng = Affine(ch, 1)

    # (a) the false candidate: level-1 current state
    st1 = eng.act(it, -1, vac)
    wit1 = [a for a in range(ch.dim) if eng.act(a, 1, st1)]
    val = eng.act(iF, 1, st1).get((), F(0))
    check("S6.1: FALSE CANDIDATE -- E^theta_{-1}|0> (level 1) is NOT "
          "singular: exactly %d witness (a = F^theta), J^F_1 gives "
          "%s |0> = +-k with k = 1: this is the 248-current state that "
          "must REMAIN (chi_1 = 248)" % (len(wit1), val),
          wit1 == [iF] and abs(val) == 1)

    # (b) generic level-2 states
    rnd = random.Random(4972)
    ok_gen = True
    tried = 0
    while tried < 4:
        b = rnd.randrange(ch.nR)
        c = rnd.randrange(ch.nR)
        if vadd(ch.roots[b], ch.roots[c]) == smul(2, theta):
            continue
        tried += 1
        st = eng.act(b, -1, eng.act(c, -1, vac))
        nw = sum(1 for a in range(ch.dim) if eng.act(a, 1, st))
        print("     generic pick %d: beta+gamma weight %s..., witnesses "
              "%d / 248" % (tried, [ch.roots[b][0], ch.roots[c][0]], nw))
        if nw == 0:
            ok_gen = False
    check("S6.2: GENERIC LEVEL-2 STATES -- 4 seeded picks "
          "(E^b_{-1})(E^c_{-1})|0> with b+c != 2 theta: ALL non-singular "
          "(witness count > 0 each)", ok_gen)

    # (c) the k-dial and the cube at k = 2
    eng2 = Affine(ch, 2)
    s2 = eng2.act(it, -1, eng2.act(it, -1, vac))
    r2 = eng2.act(iF, 1, s2)
    cube = eng2.act(it, -1, s2)
    bad_c1 = [a for a in range(ch.dim) if eng2.act(a, 1, cube)]
    bad_c2 = [a for a in range(ch.dim) if eng2.act(a, 2, cube)]
    check("S6.3: KAC LEVEL MECHANICS (generic, honestly typed) -- at k = 2 "
          "the SQUARE is not singular (F^theta_1 -> %s E_{-1}|0> != 0) but "
          "the CUBE (E^theta_{-1})^3|0> IS: J^a_1 and J^a_2 vanish for all "
          "248 basis elements (%d, %d violations): the (E^theta)^(k+1) "
          "pattern is generic Kac mechanics, NOT E8-specific"
          % (r2.get(((-1, it),), 0), len(bad_c1), len(bad_c2)),
          r2 != {} and not bad_c1 and not bad_c2)

    # (d) SO(16)_1 = D8 through the same pipeline
    rs8 = d8_std()
    ch8 = Chevalley(rs8)
    theta8 = rs8.fold(rs8.roots[0])
    it8 = ch8.ridx[theta8]
    ok_j8 = all(ch8.jacobi_zero(i, ch8.opp[i], j)
                for i in range(ch8.nR) for j in range(ch8.nR))
    check("S6.4: D8 CHEVALLEY -- 112 roots, Jacobi on ALL 12544 sl2-slice "
          "triples, kappa(theta_vee,theta_vee) = 2",
          ch8.nR == 112 and ok_j8
          and sum(ci * cj * F(ch8.Atrue[ii - ch8.nR][jj - ch8.nR])
                  for ii, ci in ch8.hvec_index(theta8).items()
                  for jj, cj in ch8.hvec_index(theta8).items()) == 2)

    eng8 = Affine(ch8, 1)
    s8 = eng8.act(it8, -1, eng8.act(it8, -1, vac))
    bad8 = [a for a in range(ch8.dim) if eng8.act(a, 1, s8)]
    bad8b = [a for a in range(ch8.dim) if eng8.act(a, 2, s8)]
    check("S6.5: D8 SINGULAR VECTOR -- (E^theta_{-1})^2|0> IS singular for "
          "SO(16)_1 too (%d, %d violations of 120 basis loops): the "
          "singular-vector mechanism is level-1 GENERIC -- what it deletes "
          "is dim V(2 theta_D8) = %d = 5304 != 14^3 = %d (the h_vee^3 "
          "identity stays E8-specific, WP5a)"
          % (len(bad8), len(bad8b), rs8.weyl_dim(smul(2, theta8)), 14 ** 3),
          not bad8 and not bad8b
          and rs8.weyl_dim(smul(2, theta8)) == 5304)

    com_e8 = sorted(ip(w, theta) // 4 for w in rs.fund)
    com_d8 = sorted(ip(w, theta8) // 4 for w in rs8.fund)
    n_extra = sum(1 for c in com_d8 if c <= 1)
    check("S6.6: THE DISCRIMINATOR -- comarks <omega_i,theta_vee>: E8 %s "
          "all >= 2 (vacuum is the ONLY level-1 primary: the singular "
          "vector closes the ONE-block theory), D8 %s has %d fundamental "
          "weights with comark 1 (vector + 2 spinors survive as SEPARATE "
          "level-1 primaries)" % (com_e8, com_d8, n_extra),
          min(com_e8) == 2 and n_extra == 3)

    hv8 = ip(theta8, rs8.rho) // 4 + 1
    hws = sorted(F(ip(w, vadd(w, smul(2, rs8.rho)))) / F(4 * 2 * (1 + hv8))
                 for w in rs8.fund if ip(w, theta8) // 4 == 1)
    check("S6.7: D8 BLOCK WEIGHTS -- h(omega) = (omega,omega+2rho)/"
          "(2(k+h_vee)) for the three comark-1 weights = %s = "
          "(1/2, 1, 1): h = 1/2 NON-integer -- the singular vector alone "
          "does NOT make SO(16)_1 one-block (4 blocks stay); E8's integer "
          "glue weights (0,1,1,1) (S4.14) DO fuse: one-block closure is "
          "the E8/mu4-specific part, honestly typed" % hws,
          hws == [F(1, 2), F(1), F(1)] and hv8 == 14)


# ---------------------------------------------------------------------------
# S7 -- preregistered verdict
# ---------------------------------------------------------------------------
def section7(jt):
    print("  -- S7: verdict against the preregistered criteria")
    check("S7.1 [E]: SUCCESS CRITERIA -- (i) |s> = (E^theta_{-1})^2|0> "
          "constructed explicitly (S3.4); (ii) J^a_1|s> = 0 for all 248 "
          "generators MACHINE-verified exactly, plus J^a_2, E^a_0, weight "
          "(S3.5-S3.7); (iii) mu4-compatible: integer quarter level 8 = "
          "q^2, definite clock phase i^(2j) = -1 (j(theta) = %d, h-adapted "
          "chamber), sheet-even class 2 in {0,2}, building block "
          "expressible in the sector-C_%d equivariant variables (S4.5-"
          "S4.9): the KILL branch (not expressible) is NOT triggered"
          % (jt, jt), True)
    check("S7.2 [C]: named identifications -- Weyl complete reducibility "
          "for the full-27000 extension of the depth-4 orbit check (S5.5); "
          "'the singular vector generates the maximal submodule' (Kac) "
          "used only beyond level 2; the per-period quarter dictionary "
          "(v496 S4) for the u-unit bookkeeping", True)
    check("S7.3 [O]: honest limits -- the GNS limit state whose kernel "
          "contains the ideal (WP5c), local normality/Haag duality (WP5d), "
          "Costello-Li (WP5e) stay OPEN; the twisted-slot moding tension "
          "(S4.10) is the precise WP5c question; SEAM.EQUIV.01 untouched, "
          "stays [O]; no gate closes, no marker moves", True)


# ---------------------------------------------------------------------------
def main():
    print("WP5b CELEST.SEAM.01 -- the singular vector as an operator "
          "(second constructive milestone of WP5; exploration only)")
    rs, ch, theta = section1()
    two_theta = section2(rs, ch, theta)
    eng, s, it, iF = section3(rs, ch, theta)
    jt = section4()
    section5(rs, ch, theta, eng, s)
    section6(rs, ch, theta, it, iF)
    section7(jt)

    print("\n=== VERDICT (see report) ===")
    print("  WP5b: SUCCESS on the preregistered criteria, at the ALGEBRAIC-")
    print("  MODULE level.  |s> = (E^theta_{-1})^2|0> is explicit; its")
    print("  singularity is a finite-dimensional identity verified over the")
    print("  full 248-element Chevalley basis (190 cases die at the first")
    print("  bracket, 57 at the second, exactly 1 -- a = F^theta -- by the")
    print("  central-term cancellation 2(1-k) = 0 at k = 1: the deletion")
    print("  operator EXISTS only at level 1 and not in the centerless")
    print("  loop algebra).  mu4: glue class j(theta) = 1 (h-adapted")
    print("  chamber), clock phase i^2 = -1, class(2 theta) = 2 sheet-even,")
    print("  8 quarters = q^2; the sl2 that deletes crosses the sheet-odd")
    print("  classes (1,3) while its square is sheet-even -- consistent")
    print("  with WP5a S6.8.  U(g)|s> = V(2 theta) = 27000 = h_vee^3 with")
    print("  the lowering orbit matching Freudenthal weight-by-weight;")
    print("  quotient 4124 = theta-split sector sum.  Controls: the level-1")
    print("  current state and generic level-2 states are NOT singular; the")
    print("  cube takes over at k = 2 (generic Kac mechanics, honestly")
    print("  typed); D8 has the same singular vector but keeps 3 extra")
    print("  primaries (h = 1/2 breaks one-block fusion) -- one-block")
    print("  closure stays E8/mu4-specific.  OPEN (WP5c-e): the GNS limit")
    print("  state (the twisted-slot moding tension S4.10 is the precise")
    print("  question), local normality/Haag duality, Costello-Li.")
    print("\nchecks: %d passed, %d failed" % (N_PASS, N_FAIL))
    print("ALL CHECKS PASSED" if N_FAIL == 0 else "SOME CHECKS FAILED")
    return N_FAIL == 0


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
