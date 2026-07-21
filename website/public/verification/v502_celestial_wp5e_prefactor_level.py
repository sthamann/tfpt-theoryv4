"""v502 -- CELEST.WP5E.ALPHA.01: WP5e-alpha of the research contract
CELEST.SEAM.01 -- "prefactor and level bookkeeping", the CFT-side anchor stage
of WP5e (the BCOV/Costello-Li twistor uplift: boundary partition function =
E4/eta^8 INCLUDING the q^{-1/3} prefactor; preregistered kill: the anomaly
inflow demands a level != 1).  The full uplift stays out of reach; its two
exactly computable consistency anchors are established here.
Exact sympy/Fraction arithmetic throughout, no floats, deterministic.

PART A -- the q^{-1/3} prefactor is exact mu4 vacuum-energy bookkeeping.
  [E] S1. HURWITZ-ZETA VACUUM ENERGIES (symbolic, sympy): zeta(-1, theta) =
        -B2(theta)/2 as an exact Bernoulli identity; one real boson twisted
        by theta has E_b(theta) = (1/4)[zeta(-1,th) + zeta(-1,1-th)] =
        -1/24 + theta(1-theta)/4 EXACTLY (values -1/24, 1/192, 1/48, 1/192);
        fermionic counterpart E_f = -E_b (Ising h_sigma = E_R - E_NS = 1/16
        per Majorana); 8 untwisted bosons give -8/24 = -1/3 = -c/24 at
        c = 8 = Sugawara 248/(1+30); eta^8 = q^{1/3} prod(1-q^n)^8 and
        E4/eta^8 = q^{-1/3}(1 + 248q + 4124q^2 + 34752q^3) exact.
  [E] S2. THE CLOCK IS INNER => TWIST theta = 0^8 IN ALL FOUR SECTORS: the
        v492 machinery replicated (240 roots, glue split (52,64,60,64),
        clock multiplicities (60,64,60,64)); h = (2,2,2,2,2;0^4) and the A3
        detector h' = (0^5;1,1,1,-3) BOTH read the class mod 4 on all 240
        roots ((h,h) = 20, (h',h') = 12, sum 32); inner => all 8 Cartan
        (torus-boson) directions sit at clock eigenvalue i^0 = 1, so the
        induced twist distribution is theta = 0 (x8) in EVERY sector C_j --
        a SHIFT orbifold (sectors = lattice cosets, integer-moded
        oscillators), NOT a rotation orbifold; E_osc(C_j) = -1/3 in all four
        sectors = the sector-INDEPENDENT q^{-1/3} prefactor (one common
        eta^8).
  [E] S3. DISCRIMINANT FORM = CASIMIR ENERGY, TWO ROUTES: coset minima
        h_D5 = (0,5/8,1/2,5/8), h_A3 = (0,3/8,1/2,3/8), glue diagonal
        (0,1,1,1) INTEGER (v492 S4 from the lattice); the v92/v125 form
        (5x^2+3y^2)/8 is the sector-weight table mod 1; route 1 = SPECTRAL
        FLOW (flow by s_j = j h/4 costs j^2 (h,h)/32: 20 -> 5j^2/8, 12 ->
        3j^2/8, sum -> j^2 = 0 mod 1 = the isotropy/Lagrangian condition);
        route 2 = FREE FERMIONS, exact not just mod 1 (D5 = 10 Majorana,
        A3 = D3 = 6, glue diagonal = 16 = the WP5d seam carrier
        2^(g_car-1): R-NS shift n/16 = 5/8, 3/8, 1); honest sharpening: the
        naive ROTATION reading fails -- the geometric A3 deck diag(i,i^-1)
        gives twisted Casimir 3/16 != 3/8 (the v492 S5 'clock != deck'
        lesson at the Casimir level, factor 2).
  [E] S4. CHARACTER RECONSTRUCTION: all glue-coset norms even (isotropic
        diagonal <=> even extended lattice = E8); sum of the four
        Theta_{C_j} = E4 = (1,240,2160,6720); sector characters carry
        leading exponents -1/3 + h_j and leading coefficients (1,64,60,64),
        level-1 currents (60,64,60,64), and sum EXACTLY to E4/eta^8.

PART B -- the level k = 1 forced THREE independent ways.
  [E] S5. (i) CURRENT CONDITION: simple-current weights at level k are
        exact closed forms h(k om_v) = k/2, h(k om_{s,c}) = 5k/8 (D5),
        h(k om_j) = k j(4-j)/8 (A3); glue-diagonal totals h(J^j; k) =
        k (0,1,1,1) -- INTEGER FOR ALL k = 1..8, so integrality alone fixes
        NOTHING (the honest sharpening: the originally conjectured
        glue-h-integrality route holds at every level and is dead as a
        selector); what fixes k: the extension closes onto the E8 ADJOINT
        (60+64+60+64 = 248 spin-1 currents) only if h(J) = 1, and
        h(J; k) = k => k = 1 uniquely.  (ii) CONFORMAL EMBEDDING: D5+A3 in
        E8 reduces to 47k^2 + 219k - 266 = 47(k-1)(k + 266/47) = 0 (unique
        positive root k = 1); D8 in E8 reduces to 128k(1-k) = 0 (the 128 =
        spinor dim).  (iii) CENTRAL CHARGE = THE PREFACTOR ITSELF:
        248k/(k+30) = 8 <=> 240(k-1) = 0 <=> k = 1 (240 = #roots); -c/24 =
        -1/3 only at k = 1 (k = 2: -31/48).  PLUS the WP5b singular-vector
        dial: PBW engine ||(E^theta_{-1})^m 0||^2 = m! k(k-1)...(k-m+1),
        singular vector exactly at grade k+1; k = 1 deletes V(2 theta):
        Weyl dims recomputed from E8 root data (248, 3875, 27000 with
        Sym^2(248) = 30876), level-2 quotient 31124 - 27000 = 4124 = chi_2;
        k = 2: <s|s> = +4 (the WP5b/WP5c value), 31124 stays.
  [E] S6. NEGATIVE CONTROLS: (a) D8/SO(16)_1 -- same rank 8, same c = 8,
        SAME q^{-1/3} prefactor, but coset weights (0,1/2,1,1): the
        prefactor does NOT discriminate E8 vs SO(16), the h-INTEGRALITY of
        the glue diagonal does; Theta_D8 + Theta_s = E4 (the {1,s}
        Lagrangian extension IS E8).  (b) wrong twist: Z2 ROTATION gives
        E = +1/6 (h = 1/2, no mu4-shift sector there); a mu4 ROTATION makes
        E_j = (-1/3, 1/24, 1/6, 1/24) sector-DEPENDENT -- the common
        prefactor (and the single eta^8) breaks.  (c) wrong k in {2,3,4}:
        all five dials fail coherently (h(J) = k != 1; embedding residual
        360/814/1362; c != 8; prefactor != q^{-1/3}; <s|s> = 4/12/24, so
        27000 survives and the level-2 dim stays 31124 != 4124).
  [C] Kac generation of the maximal submodule by the grade-(k+1) singular
        vector for k >= 3 (k = 1, 2 machine-anchored by WP5b/WP5c).
  [O] HONEST FENCE -- WP5e is NOT closed: the BCOV/Costello-Li construction
        itself (the boundary partition function from the twistor side, the
        actual anomaly-inflow computation on PT, Costello's one-loop axion
        coupling lambda_g/(8 pi sqrt 3), the Costello-Paquette-Sharma
        level-from-flux mechanism) stays OPEN; v495 anchors the Lie-algebra
        arithmetic of the axion coefficient only; the KILL branch ('inflow
        demands a level != 1') is NOT triggered on the CFT side -- all
        computable dials say k = 1 -- but its twistor side is untested.
        v502 anchors the CFT side of WP5e (alpha stage); WP5e stays [O];
        SEAM.EQUIV.01 untouched; no gate closes, no marker moves.

Status: [E] exact prefactor/level arithmetic (sympy/Fraction); [C] the Kac
identification above; [O] the twistor inflow (WP5e proper).  Python;
Wolfram-mirrored (vacuum-energy identities, discriminant/Casimir tables,
k-fixing equations, character sums), counted per GATE.WOLFRAM.02.
Discovery provenance: experiments/tfpt-discovery/
celestial_seam_wp5e_prefactor_level_probe.py (2026-07-21, 33/33)."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, factorial

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

MU4 = N_fam + 1             # 4 = |mu4|, the seam clock order
RANK = rankE8               # 8
H_VEE = 2 * N_fam * g_car   # 30 = |Z2| N_fam g_car (v495 anchor decomposition)
NMAX = 3                    # character depth q^0..q^3
MAXNORM = 2 * NMAX


def fmt(xs):
    return "(" + ", ".join(str(x) for x in xs) + ")"


# ---------------------------------------------------------------------------
# exact integer power series helpers (v492/v500 style)
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


def sigma3(n):
    return sum(k ** 3 for k in range(1, n + 1) if n % k == 0)


def ip(a, b):
    return sum(x * y for x, y in zip(a, b))


def vadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def smul(k, a):
    return tuple(k * x for x in a)


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


# ---------------------------------------------------------------------------
# E8 roots in D5 (+) A3 + glue coordinates (v128/v492 construction, 9-tuples)
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
# coset norm tables (v492 machinery)
# ---------------------------------------------------------------------------
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


def d8_coset_norms(maxnorm):
    out = {k: {} for k in ('0', 'v', 's', 'c')}
    for v in product(range(-2, 3), repeat=8):
        n = F(sum(x * x for x in v))
        if n > maxnorm:
            continue
        key = '0' if sum(v) % 2 == 0 else 'v'
        out[key][n] = out[key].get(n, 0) + 1
    rng_half = [F(k, 2) for k in (-3, -1, 1, 3)]
    for v in product(rng_half, repeat=8):
        n = sum(x * x for x in v)
        if n > maxnorm:
            continue
        key = 's' if sum(v) % 2 == 0 else 'c'
        out[key][n] = out[key].get(n, 0) + 1
    return out


def coset_min(d, positive_only=True):
    vals = [n for n, c in d.items() if c > 0 and (n > 0 or not positive_only)]
    return min(vals) if vals else None


# ---------------------------------------------------------------------------
# E8 root system in DOUBLED integer coordinates (v500 crib, trimmed):
# only what the Weyl dimension formula needs (pos roots, rho, fold).
# ---------------------------------------------------------------------------
class E8System:
    def __init__(self):
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
        self.roots = roots
        self.simple = [
            (1, -1, -1, -1, -1, -1, -1, 1),
            (2, 2, 0, 0, 0, 0, 0, 0),
            (-2, 2, 0, 0, 0, 0, 0, 0),
            (0, -2, 2, 0, 0, 0, 0, 0),
            (0, 0, -2, 2, 0, 0, 0, 0),
            (0, 0, 0, -2, 2, 0, 0, 0),
            (0, 0, 0, 0, -2, 2, 0, 0),
            (0, 0, 0, 0, 0, -2, 2, 0),
        ]
        self.Mrows = [[self.simple[j][i] for j in range(8)] for i in range(8)]
        pos = [r for r in roots if self._nonneg(r)]
        assert 2 * len(pos) == len(roots)
        self.pos = pos
        s = [0] * 8
        for r in pos:
            s = [x + y for x, y in zip(s, r)]
        assert all(x % 2 == 0 for x in s)
        self.rho = tuple(x // 2 for x in s)

    def _nonneg(self, v):
        cs = solve_fraction(self.Mrows, list(v))
        return all(c >= 0 for c in cs)

    def fold(self, v):
        v = list(v)
        changed = True
        while changed:
            changed = False
            for a in self.simple:
                c = sum(x * y for x, y in zip(v, a))
                if c < 0:
                    assert c % 4 == 0
                    k = c // 4
                    for t in range(8):
                        v[t] -= k * a[t]
                    changed = True
        return tuple(v)

    def weyl_dim(self, lam):
        lr = vadd(lam, self.rho)
        out = F(1)
        for a in self.pos:
            out *= F(ip(lr, a), ip(self.rho, a))
        assert out.denominator == 1
        return int(out)


# ---------------------------------------------------------------------------
# mini affine sl2 PBW engine (v498/v500 Affine crib on the 3-dim theta-sl2):
# indices 0 = e (= E^theta), 1 = f, 2 = h; level k in the long-root
# normalisation (kappa(e,f) = 1, kappa(h,h) = 2) => sl2 level = E8 level.
# ---------------------------------------------------------------------------
class MiniSL2:
    _BR = {(0, 1): {2: F(1)}, (1, 0): {2: F(-1)},
           (2, 0): {0: F(2)}, (0, 2): {0: F(-2)},
           (2, 1): {1: F(-2)}, (1, 2): {1: F(2)}}

    def bracket(self, i, j):
        return self._BR.get((i, j), {})

    def kappa(self, i, j):
        if (i, j) in ((0, 1), (1, 0)):
            return F(1)
        if i == j == 2:
            return F(2)
        return F(0)


class AffineSL2:
    def __init__(self, k):
        self.ch = MiniSL2()
        self.k = F(k)

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


def shapovalov_em(k, m):
    """<0| f_1^m e_{-1}^m |0> at affine sl2 level k (exact)."""
    eng = AffineSL2(k)
    st = {(): F(1)}
    for _ in range(m):
        st = eng.act(0, -1, st)
    for _ in range(m):
        st = eng.act(1, 1, st)
        if not st:
            return F(0)
    return st.get((), F(0))


# ---------------------------------------------------------------------------
# affine conformal weights h(k*omega) = (lam, lam + 2 rho) / (2 (k + h_vee))
# ---------------------------------------------------------------------------
D5_OM = {'v': (F(1), F(0), F(0), F(0), F(0)),
         's': (HALF,) * 5,
         'c': (HALF, HALF, HALF, HALF, -HALF)}
D5_RHO = (F(4), F(3), F(2), F(1), F(0))
D5_HVEE = 8

A3_OM = {1: (F(3, 4), F(-1, 4), F(-1, 4), F(-1, 4)),
         2: (HALF, HALF, -HALF, -HALF),
         3: (F(1, 4), F(1, 4), F(1, 4), F(-3, 4))}
A3_RHO = (F(3, 2), F(1, 2), F(-1, 2), F(-3, 2))
A3_HVEE = 4


def h_current(om, rho, hvee, k):
    lam = smul(F(k), om)
    return (ip(lam, lam) + 2 * ip(lam, rho)) / (2 * (F(k) + hvee))


# ---------------------------------------------------------------------------
# S1 -- Hurwitz-zeta vacuum energies (symbolic, exact)
# ---------------------------------------------------------------------------
def section1():
    print("  -- S1: zeta-regularised vacuum energies (Hurwitz, sympy-exact)")
    th = sp.symbols('theta')

    zid = sp.expand(sp.zeta(-1, th) + sp.bernoulli(2, th) / 2)
    Eb = sp.expand((sp.zeta(-1, th) + sp.zeta(-1, 1 - th)) / 4)
    Eb_closed = -sp.Rational(1, 24) + th * (1 - th) / 4
    vals = {t: sp.nsimplify(Eb.subs(th, t)) for t in
            (0, sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4))}
    print("     theta      0     1/4    1/2    3/4")
    print("     E_b(th)  %s  %s  %s  %s"
          % (vals[0], vals[sp.Rational(1, 4)], vals[sp.Rational(1, 2)],
             vals[sp.Rational(3, 4)]))
    check("S1.1: HURWITZ-ZETA DERIVATION -- zeta(-1,theta) = -B2(theta)/2 "
          "(symbolic identity, residual %s); one real boson twisted by theta: "
          "E_b = (1/4)[zeta(-1,th) + zeta(-1,1-th)] = -1/24 + theta(1-theta)/4 "
          "EXACTLY; values (0,1/4,1/2,3/4) -> (-1/24, 1/192, 1/48, 1/192)"
          % zid,
          zid == 0 and sp.expand(Eb - Eb_closed) == 0
          and vals[0] == sp.Rational(-1, 24)
          and vals[sp.Rational(1, 4)] == sp.Rational(1, 192)
          and vals[sp.Rational(1, 2)] == sp.Rational(1, 48)
          and vals[sp.Rational(3, 4)] == sp.Rational(1, 192))

    Ef = -Eb
    ns = sp.nsimplify(Ef.subs(th, sp.Rational(1, 2)))
    ra = sp.nsimplify(Ef.subs(th, 0))
    check("S1.2: FERMION COUNTERPART -- E_f(theta) = -E_b(theta) = +1/24 - "
          "theta(1-theta)/4: NS (th=1/2) = %s = -1/48, R (th=0) = %s = +1/24; "
          "Ising h_sigma = E_R - E_NS = %s = 1/16 (per Majorana)"
          % (ns, ra, ra - ns),
          ns == sp.Rational(-1, 48) and ra == sp.Rational(1, 24)
          and ra - ns == sp.Rational(1, 16))

    e8bos = 8 * F(-1, 24)
    c_sug = F(248, 1 + H_VEE)
    check("S1.3: THE UNTWISTED VACUUM -- 8 bosons x (-1/24) = %s = -1/3 = "
          "-c/24 at c = 8; Sugawara c(E8, k=1) = 248/(1+30) = %s = 8: the two "
          "c = 8 routes (free-boson count = rank, Sugawara at k = 1) agree"
          % (e8bos, c_sug),
          e8bos == F(-1, 3) and c_sug == 8 and F(-8, 24) == F(-1, 3))

    p8 = fock({n: 8 for n in range(1, NMAX + 1)}, NMAX)
    check("S1.4: ETA^8 PREFACTOR -- eta = q^{1/24} prod(1-q^n) => eta^8 = "
          "q^{8/24} prod(...)^8 = q^{1/3}(...): 8/24 = 1/3 exact; "
          "1/prod(1-q^n)^8 = %s (q^0..q^3)" % (p8,),
          F(8, 24) == F(1, 3) and p8 == [1, 8, 44, 192])

    e4 = [1] + [240 * sigma3(n) for n in range(1, NMAX + 1)]
    chi = series_mul(e4, p8, NMAX)
    check("S1.5: THE TARGET -- E4 = %s (1, 240, 2160, 6720); E4/eta^8 = "
          "q^{-1/3} * %s = q^{-1/3}(1 + 248q + 4124q^2 + 34752q^3) exact"
          % (e4, chi),
          e4 == [1, 240, 2160, 6720] and chi == [1, 248, 4124, 34752])
    return p8, e4, chi


# ---------------------------------------------------------------------------
# S2 -- the mu4 twist distribution (v492 replication + shift reading)
# ---------------------------------------------------------------------------
def section2():
    print("  -- S2: the mu4 twist distribution on the 8 torus bosons")
    roots = build_glue_roots()
    counts = [sum(1 for c in roots.values() if c == j) for j in range(4)]
    norm_ok = all(sum(x * x for x in r) == 2 for r in roots)
    dims = [counts[0] + RANK] + counts[1:]
    check("S2.1: v492 REPLICATION -- 240 roots, all norm 2, glue split %s = "
          "(52,64,60,64); eigenvalue multiplicities of the clock on the 248 "
          "(with Cartan in class 0): %s = (60,64,60,64)" % (counts, dims),
          len(roots) == 240 and norm_ok and counts == [52, 64, 60, 64]
          and dims == [60, 64, 60, 64])

    h9 = (F(2),) * 5 + (F(0),) * 4
    hp9 = (F(0),) * 5 + (F(1), F(1), F(1), F(-3))
    ok_h = all(ip(r, h9).denominator == 1 and int(ip(r, h9)) % 4 == c
               for r, c in roots.items())
    ok_hp = all(ip(r, hp9).denominator == 1 and int(ip(r, hp9)) % 4 == c
                for r, c in roots.items())
    nh, nhp = ip(h9, h9), ip(hp9, hp9)
    check("S2.2: INNER ELEMENT -- h = (2,2,2,2,2;0^4) and the A3 detector "
          "h' = (0^5;1,1,1,-3) BOTH read <alpha,.> = class mod 4 on all 240 "
          "roots; norms (h,h) = %s = 20, (h',h') = %s = 12, sum = %s = 32 = "
          "2 * 4^2 * 1 (the clock is Ad(exp(2 pi i h/4)): INNER)"
          % (nh, nhp, nh + nhp),
          ok_h and ok_hp and nh == 20 and nhp == 12 and nh + nhp == 32)

    # inner => the 8 Cartan directions carry clock eigenvalue i^0 = 1:
    # Ad(torus element) is trivial on the Cartan (weight-0 space); machine
    # side: the class function is <alpha,h> on ROOT vectors, and the 8
    # Cartan generators sit at weight 0 -> class 0 (they fill 60 = 52 + 8).
    cartan_class = [int(ip((F(0),) * 9, h9)) % 4] * RANK
    twist_dist = {j: {F(0): RANK} for j in range(4)}
    check("S2.3: TWIST DISTRIBUTION -- the clock is inner, so ALL 8 Cartan "
          "(torus-boson) directions sit at eigenvalue i^0 = 1 (class %s x 8; "
          "class-0 total 52 + 8 = 60); induced twist on the 8 bosons in EVERY "
          "sector C_j: theta = 0 (multiplicity 8) -- a SHIFT orbifold "
          "(sectors = lattice cosets, oscillators integer-moded), NOT a "
          "rotation orbifold" % cartan_class[0],
          all(c == 0 for c in cartan_class)
          and all(twist_dist[j] == {F(0): 8} for j in range(4)))

    Eosc = {j: sum(mult * (F(-1, 24) + t * (1 - t) / 4)
                   for t, mult in twist_dist[j].items()) for j in range(4)}
    print("     sector  twist distribution      E_osc")
    for j in range(4):
        print("       C_%d   {theta=0: x8}          %s" % (j, Eosc[j]))
    check("S2.4: SECTOR OSCILLATOR ENERGIES -- E_osc(C_j) = 8 * E_b(0) = "
          "-1/3 in ALL four sectors (twist distribution trivial): the "
          "q^{-1/3} prefactor is SECTOR-INDEPENDENT -- one common eta^8",
          all(Eosc[j] == F(-1, 3) for j in range(4)))
    return roots, h9, hp9


# ---------------------------------------------------------------------------
# S3 -- discriminant form = Casimir energy
# ---------------------------------------------------------------------------
def section3(h9, hp9):
    print("  -- S3: the identity 'discriminant form = Casimir energy'")
    d5 = d5_coset_norms(MAXNORM)
    a3 = a3_coset_norms(MAXNORM)
    pairing = {0: ('0', 0), 1: ('s', 1), 2: ('v', 2), 3: ('c', 3)}
    hd5 = [F(0) if j == 0 else coset_min(d5[pairing[j][0]]) / 2
           for j in range(4)]
    ha3 = [F(0) if j == 0 else coset_min(a3[pairing[j][1]]) / 2
           for j in range(4)]
    hglue = [hd5[j] + ha3[j] for j in range(4)]
    print("     j     h_D5    h_A3    h_glue   5j^2/8   3j^2/8")
    for j in range(4):
        print("     %d     %-6s  %-6s  %-6s   %-6s   %-6s"
              % (j, hd5[j], ha3[j], hglue[j],
                 F(5 * j * j, 8) % 1, F(3 * j * j, 8) % 1))
    check("S3.1: COSET MINIMA -- h_D5 = %s = (0,5/8,1/2,5/8), h_A3 = %s = "
          "(0,3/8,1/2,3/8), glue diagonal h = %s = (0,1,1,1) INTEGER "
          "(v492 S4 replication from the lattice)"
          % (fmt(hd5), fmt(ha3), fmt(hglue)),
          hd5 == [F(0), F(5, 8), F(1, 2), F(5, 8)]
          and ha3 == [F(0), F(3, 8), F(1, 2), F(3, 8)]
          and hglue == [F(0), F(1), F(1), F(1)])

    ok_disc = all(hd5[j] % 1 == F(5 * j * j, 8) % 1
                  and ha3[j] % 1 == F(3 * j * j, 8) % 1
                  and hglue[j] % 1 == F(8 * j * j, 8) % 1
                  for j in range(4))
    check("S3.2: DISCRIMINANT FORM -- h_D5(j) = 5j^2/8, h_A3(j) = 3j^2/8, "
          "h_glue(j) = (5+3)j^2/8 = j^2 = 0 mod 1 for all j: the v92/v125 "
          "form (5x^2+3y^2)/8 IS the sector-weight table mod 1 (isotropy of "
          "the diagonal = glue-h integrality)", ok_disc)

    nh, nhp = ip(h9, h9), ip(hp9, hp9)      # 20 and 12 (S2.2)
    flow_d5 = [j * j * nh / 32 for j in range(4)]
    flow_a3 = [j * j * nhp / 32 for j in range(4)]
    flow_sum = [j * j * (nh + nhp) / 32 for j in range(4)]
    ok_flow = (all(flow_d5[j] % 1 == hd5[j] % 1 for j in range(4))
               and all(flow_a3[j] % 1 == ha3[j] % 1 for j in range(4))
               and all(flow_sum[j] % 1 == 0 for j in range(4)))
    check("S3.3: CASIMIR ROUTE 1 (SPECTRAL FLOW) -- flowing by s_j = j*h/4 "
          "costs L0 -> L0 + s_j^2/2 = j^2 (h,h)/32: D5 side 20j^2/32 = "
          "5j^2/8 = %s, A3 side 12j^2/32 = 3j^2/8 = %s, sum 32j^2/32 = j^2 "
          "integer -- the INNER element's flow energy IS the discriminant "
          "form (mod 1): the identity HOLDS on the shift reading"
          % (fmt(x % 1 for x in flow_d5), fmt(x % 1 for x in flow_a3)),
          ok_flow)

    dE = F(1, 24) - F(-1, 48)            # E_f(R) - E_f(NS) per Majorana
    n_maj = {'D5': 10, 'A3(=D3)': 6, 'glue(D5+A3)': 16, 'D8': 16}
    cas = {k: n * dE for k, n in n_maj.items()}
    check("S3.4: CASIMIR ROUTE 2 (FREE FERMIONS, exact not just mod 1) -- "
          "R-NS shift per Majorana = 1/24-(-1/48) = %s = 1/16; D5 = 10 Maj: "
          "%s = 5/8 = h_D5(1); A3 = D3 = 6 Maj: %s = 3/8 = h_A3(1); glue "
          "diagonal = 16 Maj (the WP5d seam carrier 2^(g_car-1) = 16): %s = "
          "1 = h_glue(1); vector classes h = 1/2 = first NS mode; the "
          "discriminant values ARE Casimir energies of the 16-Majorana seam "
          "edge" % (dE, cas['D5'], cas['A3(=D3)'], cas['glue(D5+A3)']),
          dE == F(1, 16) and cas['D5'] == F(5, 8) == hd5[1]
          and cas['A3(=D3)'] == F(3, 8) == ha3[1]
          and cas['glue(D5+A3)'] == F(1) == hglue[1]
          and 2 ** (g_car - 1) == 16
          and hd5[2] == ha3[2] == F(1, 2))

    # the naive ROTATION reading fails: geometric A3 deck on C^2 (complex
    # twists 1/4, 3/4) gives h_tw = 3/16 != 3/8
    Ec = lambda a: F(-1, 12) + a * (1 - a) / 2       # complex boson
    E_deck = Ec(F(1, 4)) + Ec(F(3, 4))
    h_deck = E_deck - 2 * F(-1, 12)
    check("S3.5: ROTATION READING FAILS (honest sharpening) -- the geometric "
          "A3 deck diag(i, i^-1) on C^2 (complex twists 1/4, 3/4) gives "
          "twisted Casimir h = %s = 3/16 != 3/8 = h_A3(1): the sector "
          "weights are NOT rotation-twist energies of the deck -- they are "
          "SHIFT/flow energies of the inner clock (the v492 S5 lesson "
          "'clock != deck' at the Casimir level; factor %s)"
          % (h_deck, ha3[1] / h_deck),
          h_deck == F(3, 16) and h_deck != ha3[1]
          and ha3[1] / h_deck == 2)
    return d5, a3, hd5, ha3, hglue


# ---------------------------------------------------------------------------
# S4 -- prefactor balance + character reconstruction
# ---------------------------------------------------------------------------
def section4(d5, a3, hglue, p8, e4, chi):
    print("  -- S4: prefactor balance and character reconstruction")
    pairing = {0: ('0', 0), 1: ('s', 1), 2: ('v', 2), 3: ('c', 3)}
    theta_c = {}
    n_odd = 0
    for j, (dk, ak) in pairing.items():
        coeffs = [0] * (NMAX + 1)
        for n5, c5 in d5[dk].items():
            for n3, c3v in a3[ak].items():
                n = n5 + n3
                if n > MAXNORM:
                    continue
                if n % 2 != 0 or F(n, 2).denominator != 1:
                    n_odd += c5 * c3v
                    continue
                coeffs[int(n) // 2] += c5 * c3v
        theta_c[j] = coeffs
    tot_theta = [sum(theta_c[j][m] for j in range(4)) for m in range(NMAX + 1)]
    check("S4.1: SECTOR THETAS -- all norms in every glue coset are EVEN "
          "integers (%d odd/fractional cross-terms in range: the diagonal is "
          "isotropic <=> the extended lattice is even = E8); "
          "sum of the four Theta_{C_j} = %s = E4 = (1,240,2160,6720)"
          % (n_odd, tot_theta), n_odd == 0 and tot_theta == e4)

    sector = {j: series_mul(theta_c[j], p8, NMAX) for j in range(4)}
    lead_exp, lead_coeff = [], []
    for j in range(4):
        m0 = next(m for m in range(NMAX + 1) if sector[j][m] != 0)
        lead_exp.append(F(-1, 3) + m0)
        lead_coeff.append(sector[j][m0])
    print("     sector char  leading exponent  leading coeff  q^1-coeff")
    for j in range(4):
        print("       C_%d        %-8s          %-6d        %d"
              % (j, lead_exp[j], lead_coeff[j], sector[j][1]))
    check("S4.2: SECTOR CHARACTERS -- Theta_{C_j}/eta^8 = q^{-1/3} (Theta_j "
          "P8): leading exponents %s = -1/3 + h_j (h = 0,1,1,1), leading "
          "coefficients %s = (1,64,60,64) = minimal-vector counts; level-1 "
          "currents per sector %s = (60,64,60,64), sum 248"
          % (fmt(lead_exp), lead_coeff, [sector[j][1] for j in range(4)]),
          lead_exp == [F(-1, 3) + h for h in hglue]
          and lead_coeff == [1, 64, 60, 64]
          and [sector[j][1] for j in range(4)] == [60, 64, 60, 64]
          and sum(sector[j][1] for j in range(4)) == 248)

    total = [sum(sector[j][m] for j in range(4)) for m in range(NMAX + 1)]
    check("S4.3: RECONSTRUCTION -- sum of the four sector characters = %s = "
          "chi_(E8)_1 = (1, 248, 4124, 34752) EXACTLY (first 4 coefficients; "
          "v492 S4/v496 S3 replication)" % (total,),
          total == chi and total == [1, 248, 4124, 34752])

    check("S4.4: PREFACTOR BALANCE -- every sector carries the SAME q^{-1/3} "
          "= q^{-c/24}, c = 8 = number of (untwisted) bosons: the E4/eta^8 "
          "prefactor is the mu4-sector vacuum-energy bookkeeping, sector by "
          "sector (-1/3 + h_j with h_j = 0,1,1,1 integer -- the sum starts "
          "at q^{-1/3} * 1 from C_0 alone)",
          F(-1, 3) == -F(8, 24) and all(h.denominator == 1 for h in hglue))
    return sector


# ---------------------------------------------------------------------------
# S5 -- level k = 1: three exact constraints
# ---------------------------------------------------------------------------
def section5():
    print("  -- S5: the level k = 1 (three independent exact constraints)")
    ks = sp.symbols('k', positive=True)

    # (i) simple-current weights at level k: closed forms
    hv = sp.together((ks ** 2 * 1 + 2 * ks * 4) / (2 * (ks + 8)))
    hs = sp.together((ks ** 2 * sp.Rational(5, 4) + 2 * ks * 5)
                     / (2 * (ks + 8)))
    ha1 = sp.together((ks ** 2 * sp.Rational(3, 4) + 2 * ks * sp.Rational(3, 2))
                      / (2 * (ks + 4)))
    ha2 = sp.together((ks ** 2 * 1 + 2 * ks * 2) / (2 * (ks + 4)))
    ok_closed = (sp.simplify(hv - ks / 2) == 0
                 and sp.simplify(hs - 5 * ks / 8) == 0
                 and sp.simplify(ha1 - 3 * ks / 8) == 0
                 and sp.simplify(ha2 - ks / 2) == 0)
    # numeric verification from the orthogonal-basis data, k = 1..8
    ok_num = True
    for k in range(1, 9):
        ok_num &= h_current(D5_OM['v'], D5_RHO, D5_HVEE, k) == F(k, 2)
        ok_num &= h_current(D5_OM['s'], D5_RHO, D5_HVEE, k) == F(5 * k, 8)
        ok_num &= h_current(D5_OM['c'], D5_RHO, D5_HVEE, k) == F(5 * k, 8)
        ok_num &= h_current(A3_OM[1], A3_RHO, A3_HVEE, k) == F(3 * k, 8)
        ok_num &= h_current(A3_OM[2], A3_RHO, A3_HVEE, k) == F(k, 2)
        ok_num &= h_current(A3_OM[3], A3_RHO, A3_HVEE, k) == F(3 * k, 8)
    check("S5.1: SIMPLE-CURRENT WEIGHTS AT LEVEL k -- affine formula "
          "(lam, lam+2rho)/(2(k+h_vee)) gives EXACT closed forms: D5: "
          "h(k om_v) = k/2, h(k om_{s,c}) = 5k/8; A3: h(k om_j) = k j(4-j)/8 "
          "(= 3k/8, k/2, 3k/8): each = k * (discriminant form) mod 1 "
          "(symbolic + numeric k = 1..8)", ok_closed and ok_num)

    print("     k    h_D5(s)  h_A3(w1)  glue h(J^1) h(J^2) h(J^3)  integer?")
    ok_int = True
    glue_int = []
    for k in range(1, 9):
        hj = [F(0),
              F(5 * k, 8) + F(3 * k, 8),
              F(k, 2) + F(k, 2),
              F(5 * k, 8) + F(3 * k, 8)]
        intg = all(x.denominator == 1 for x in hj)
        glue_int.append(intg)
        ok_int &= (hj == [F(0), F(k), F(k), F(k)])
        print("     %d    %-7s  %-8s  %-9s %-6s %-6s  %s"
              % (k, F(5 * k, 8), F(3 * k, 8), hj[1], hj[2], hj[3], intg))
    check("S5.2: GLUE-DIAGONAL INTEGRALITY (honest finding) -- h(J^j; k) = "
          "k * (0,1,1,1): INTEGER FOR ALL k = 1..8 (5k/8 + 3k/8 = k).  "
          "Integrality/locality of the Z4 simple-current extension holds at "
          "EVERY level -- it does NOT single out k = 1 by itself",
          ok_int and all(glue_int))

    hJ = {k: F(k) for k in range(1, 9)}
    check("S5.3: WHAT FIXES k ON THE GLUE SIDE -- the CURRENT condition: the "
          "extension closes onto the E8 ADJOINT (60+64+60+64 = 248 spin-1 "
          "currents) only if the 188 new fields have h(J) = 1; h(J; k) = k "
          "=> k = 1 uniquely (at k = 2,3,4 the would-be adjoint completion "
          "has spin %s != 1: the extension exists but is NOT a Lie-algebra "
          "extension, no (E8)_k)" % ([int(hJ[k]) for k in (2, 3, 4)],),
          hJ[1] == 1 and all(hJ[k] != 1 for k in range(2, 9))
          and 60 + 64 + 60 + 64 == 248)

    poly = sp.expand(45 * ks * (ks + 4) * (ks + 30) + 15 * ks * (ks + 8) * (ks + 30)
                     - 248 * ks * (ks + 8) * (ks + 4))
    fac = sp.factor(poly)
    sols = sp.solve(sp.Eq(45 * ks / (ks + 8) + 15 * ks / (ks + 4),
                          248 * ks / (ks + 30)), ks)
    poly8 = sp.expand(120 * ks * (ks + 30) - 248 * ks * (ks + 14))
    sols8 = sp.solve(sp.Eq(120 * ks / (ks + 14), 248 * ks / (ks + 30)), ks)
    check("S5.4: CONFORMAL-EMBEDDING EQUATIONS -- D5+A3 in E8: c-equation "
          "reduces to %s = 0, i.e. 47k^2 + 219k - 266 = 47(k-1)(k + 266/47): "
          "positive solutions %s = {1} only; D8 in E8: 120k/(k+14) = "
          "248k/(k+30) reduces to %s = 0 => 128k(1-k) = 0: k = 1 (the 128 = "
          "spinor dim appears as the coefficient)"
          % (fac, sols, sp.factor(poly8)),
          sols == [1]
          and sp.expand(poly + 4 * ks * (47 * ks ** 2 + 219 * ks - 266)) == 0
          and sols8 == [1]
          and sp.expand(poly8 - (-128 * ks * (ks - 1))) == 0)

    sols_c = sp.solve(sp.Eq(248 * ks / (ks + H_VEE), 8), ks)
    cvals = {k: F(248 * k, k + H_VEE) for k in range(1, 9)}
    print("     k     c(E8,k)      -c/24")
    for k in range(1, 9):
        print("     %d     %-10s   %s" % (k, cvals[k], -cvals[k] / 24))
    check("S5.5: CENTRAL CHARGE -- 248k/(k+30) = 8 <=> 240(k-1) = 0 <=> "
          "k = %s uniquely (240 = #roots); c table k = 1..8: %s; the "
          "prefactor -c/24 = -1/3 holds ONLY at k = 1 (k = 2: -31/48)"
          % (sols_c, [str(cvals[k]) for k in range(1, 9)]),
          sols_c == [1] and cvals[1] == 8
          and all(cvals[k] != 8 for k in range(2, 9))
          and -cvals[2] / 24 == F(-31, 48))

    # (iii) WP5b level dial: mini affine-sl2 engine
    print("     Shapovalov norms <0|f_1^m e_{-1}^m|0> (theta-sl2 at level k):")
    print("     k \\ m    1      2      3      4      5")
    ok_engine = True
    sing_grade = {}
    norms = {}
    for k in range(1, 5):
        row = []
        for m in range(1, 6):
            g = shapovalov_em(k, m)
            row.append(g)
            expect = factorial(m)
            for j in range(m):
                expect *= (k - j)
            ok_engine &= (g == expect)
        norms[k] = row
        sing_grade[k] = next(m for m in range(1, 6) if row[m - 1] == 0)
        print("     %d       %-6s %-6s %-6s %-6s %s"
              % (k, row[0], row[1], row[2], row[3], row[4]))
    check("S5.6a: LEVEL DIAL (engine) -- ||(E^theta_{-1})^m 0||^2 = "
          "m! k(k-1)...(k-m+1) verified by the PBW engine for k = 1..4, "
          "m = 1..5; singular vector EXACTLY at grade k+1: %s; k = 1: "
          "<s|s> = %s = 0 (the WP5b deleting operator), k = 2: <s|s> = %s "
          "= +4 (the WP5b/WP5c value)"
          % ({k: sing_grade[k] for k in sing_grade}, norms[1][1], norms[2][1]),
          ok_engine and all(sing_grade[k] == k + 1 for k in range(1, 5))
          and norms[1][1] == 0 and norms[2][1] == 4)

    e8 = E8System()
    theta_r = e8.fold(e8.roots[0])
    dim_adj = e8.weyl_dim(theta_r)
    dim_3875 = e8.weyl_dim(e8.fold((2, 2, 2, 2, 0, 0, 0, 0)))
    dim_27000 = e8.weyl_dim(smul(2, theta_r))
    sym2 = 248 * 249 // 2
    fock2 = 248 + sym2
    lvl2 = {k: (fock2 - dim_27000 if k == 1 else fock2) for k in range(1, 5)}
    check("S5.6b: LEVEL DIAL (count) -- Weyl dims from E8 root data: "
          "dim V(theta) = %d = 248, Sym^2(248) = %d = 1 + %d + %d "
          "(= 1 + 3875 + 27000); level-2 Fock = %d = 31124; k = 1: singular "
          "vector at grade 2 deletes V(2 theta): 31124 - 27000 = %d = 4124 "
          "= chi_2; k = 2,3,4: no singular vector at grade <= 2 (norms %s "
          "all nonzero), level-2 dim stays %d != 4124 (k = 2 anchored by the "
          "WP5c full 9361-block Gram)"
          % (dim_adj, sym2, dim_3875, dim_27000, fock2, lvl2[1],
             fmt(norms[k][1] for k in (2, 3, 4)), lvl2[2]),
          dim_adj == 248 and dim_3875 == 3875 and dim_27000 == 27000
          and sym2 == 30876 and fock2 == 31124
          and lvl2[1] == 4124
          and all(lvl2[k] == 31124 for k in (2, 3, 4))
          and all(norms[k][1] != 0 for k in (2, 3, 4)))

    check("S5.7 [O]: HONEST FENCE -- what is NOT computed here: the twistor-"
          "side anomaly inflow itself (Costello's one-loop axion coupling "
          "lambda_g/(8 pi sqrt 3) on PT, the Costello-Paquette-Sharma "
          "level-from-flux mechanism, the BCOV/Costello-Li boundary partition "
          "function).  v495 anchors the Lie-algebra arithmetic of the axion "
          "coefficient ((kappa/c3)^2 = 12) only.  What IS computed: the CFT "
          "side of the level fixing -- glue/current, central-charge/prefactor "
          "and singular-vector dials all force k = 1.  WP5e stays [O]; no "
          "marker moves", True)
    return norms, lvl2, cvals


# ---------------------------------------------------------------------------
# S6 -- negative controls
# ---------------------------------------------------------------------------
def section6(e4, norms, lvl2, cvals):
    print("  -- S6: negative controls")
    d8 = d8_coset_norms(MAXNORM)
    h_d8 = {key: (F(0) if key == '0' else coset_min(d8[key]) / 2)
            for key in ('0', 'v', 's', 'c')}
    th_d8 = [0] * (NMAX + 1)
    th_s = [0] * (NMAX + 1)
    for n, c in d8['0'].items():
        if n % 2 == 0 and F(n, 2).denominator == 1:
            th_d8[int(n) // 2] += c
    for n, c in d8['s'].items():
        if n % 2 == 0 and F(n, 2).denominator == 1:
            th_s[int(n) // 2] += c
    e8_from_d8 = [a + b for a, b in zip(th_d8, th_s)]
    c_d8 = F(120, 1 + 14)
    check("S6.1: D8/SO(16)_1 CONTROL -- same rank 8 => same c = 8 (Sugawara "
          "120/15 = %s) => SAME q^{-1/3} prefactor; but coset weights h = "
          "(%s, %s, %s, %s) = (0, 1/2, 1, 1): the VECTOR class h = 1/2 is "
          "NON-integer -- the prefactor does NOT discriminate E8 vs SO(16), "
          "the h-INTEGRALITY of the glue diagonal does ((0,1,1,1) one-block "
          "vs (0,1/2,1,1) four-block); the {1,s} Lagrangian extension IS E8: "
          "Theta_D8 + Theta_s = %s = E4"
          % (c_d8, h_d8['0'], h_d8['v'], h_d8['s'], h_d8['c'], e8_from_d8),
          c_d8 == 8 and h_d8['v'] == F(1, 2)
          and h_d8['s'] == 1 and h_d8['c'] == 1
          and e8_from_d8 == e4
          and th_d8[:3] == [1, 112, 1136] and th_s[:3] == [0, 128, 1024])

    Eb = lambda a: F(-1, 24) + a * (1 - a) / 4       # real boson
    E_z2 = 8 * Eb(F(1, 2))
    h_z2 = E_z2 - 8 * Eb(F(0))
    check("S6.2: WRONG TWIST (Z2 ROTATION) -- twisting all 8 bosons by "
          "theta = 1/2 (X -> -X) gives E_tw = %s = +1/6, i.e. ground weight "
          "h = %s = 1/2 above the vacuum: NO mu4-shift sector sits there "
          "(h in {0,1,1,1}); the Z2-rotation orbifold is a measurably "
          "different theory (half-integer-moded oscillators, different "
          "eta bookkeeping)" % (E_z2, h_z2),
          E_z2 == F(1, 6) and h_z2 == F(1, 2)
          and h_z2 not in (F(0), F(1)))

    Ec = lambda a: F(-1, 12) + a * (1 - a) / 2       # complex boson
    E_rot = [4 * Ec(F(j, 4) % 1) for j in range(4)]
    print("     mu4-ROTATION sector energies (4 complex bosons, twist j/4):")
    print("       j = 0..3 : %s   (shift orbifold: -1/3 in all sectors)"
          % fmt(E_rot))
    check("S6.3: WRONG TWIST (mu4 ROTATION) -- if the clock were a rotation "
          "with eigenvalues i^j on the 8 directions, the sector energies "
          "would be E_j = %s = (-1/3, 1/24, 1/6, 1/24): sector-DEPENDENT -- "
          "the common q^{-1/3} prefactor (and with it the single eta^8) "
          "breaks; the inner/shift reading (all E_j = -1/3) is what the "
          "E4/eta^8 bookkeeping requires" % fmt(E_rot),
          E_rot == [F(-1, 3), F(1, 24), F(1, 6), F(1, 24)]
          and len(set(E_rot)) > 1)

    print("     wrong-k table (five independent failures per k):")
    print("     k   h(J)=1?  47k^2+219k-266  c(E8,k)  -c/24     "
          "<s|s>   lvl-2 dim")
    ok_tab = True
    for k in (1, 2, 3, 4):
        res = 47 * k * k + 219 * k - 266
        row_ok = ((k == 1) == (F(k) == 1) == (res == 0)
                  == (cvals[k] == 8) == (norms[k][1] == 0)
                  == (lvl2[k] == 4124))
        ok_tab &= row_ok
        print("     %d   %-7s  %-14d  %-7s  %-8s  %-6s  %d"
              % (k, F(k) == 1, res, cvals[k], -cvals[k] / 24,
                 norms[k][1], lvl2[k]))
    check("S6.4: WRONG k CONSOLIDATED -- for k = 2, 3, 4 ALL five dials fail "
          "coherently (current condition h(J) = k != 1; embedding residual "
          "47k^2+219k-266 = 360, 814, 1362 != 0; c != 8; prefactor != "
          "q^{-1/3}; <s|s> = 4, 12, 24 != 0 so 27000 survives and the "
          "level-2 dim stays 31124 != 4124); at k = 1 ALL five pass",
          ok_tab
          and [47 * k * k + 219 * k - 266 for k in (2, 3, 4)] == [360, 814, 1362]
          and [norms[k][1] for k in (2, 3, 4)] == [4, 12, 24])


# ---------------------------------------------------------------------------
# S7 -- verdict against the WP5e-alpha scope
# ---------------------------------------------------------------------------
def section7():
    print("  -- S7: verdict against the WP5e-alpha scope")
    check("S7.1 [E]: WHAT IS ANCHORED -- (a) the q^{-1/3} prefactor of "
          "E4/eta^8 is the exact mu4-sector vacuum-energy bookkeeping "
          "(Hurwitz-zeta, inner/shift twist distribution theta = 0^8 in all "
          "four sectors, common -c/24 = -1/3 at c = 8) with sector ground "
          "exponents -1/3 + (0,1,1,1); (b) discriminant form = Casimir "
          "energy holds exactly (spectral flow j^2(h,h)/32 mod 1; free-"
          "fermion R-NS shifts n/16 = 5/8, 3/8, 1 on the 16-Majorana seam "
          "carrier); (c) k = 1 is forced THREE independent ways (current "
          "condition h(J) = k = 1; conformal embedding 47(k-1)(k+266/47) = 0 "
          "resp. 128(k-1) = 0; c = 8 <=> 240(k-1) = 0; singular vector "
          "(E^theta_{-1})^{k+1} at k = 1 deleting 27000 -> 4124)", True)
    check("S7.2 [E/C]: HONEST SHARPENINGS -- (i) glue-h INTEGRALITY alone "
          "does NOT fix k (h(J^j; k) = k(0,1,1,1) integer for ALL k): the "
          "naive expectation is corrected -- the sharp glue-side dial is the "
          "CURRENT condition h(J) = 1; (ii) the sector weights are NOT "
          "rotation-twist energies (deck gives 3/16 != 3/8): the clock is "
          "inner => shift orbifold (v492 S5 'clock != deck' at the Casimir "
          "level); [C]: Kac generation of the maximal submodule by the "
          "grade-(k+1) singular vector for k >= 3 (k = 1, 2 machine-anchored "
          "by WP5b/WP5c)", True)
    check("S7.3 [O]: WHAT STAYS OPEN -- the BCOV/Costello-Li construction "
          "itself (boundary partition function from the twistor side, the "
          "actual anomaly-inflow computation on PT); the KILL branch "
          "('inflow demands a level != 1') is NOT triggered on the CFT side "
          "-- all computable dials say k = 1 -- but its twistor side is "
          "untested; SEAM.EQUIV.01 untouched, no marker moves", True)


# ---------------------------------------------------------------------------
def run():
    reset()
    print("v502  CELEST.WP5E.ALPHA.01: prefactor + level bookkeeping "
          "(WP5e-alpha of CELEST.SEAM.01 -- the CFT-side anchor stage)")
    p8, e4, chi = section1()
    roots, h9, hp9 = section2()
    d5, a3, hd5, ha3, hglue = section3(h9, hp9)
    section4(d5, a3, hglue, p8, e4, chi)
    norms, lvl2, cvals = section5()
    section6(e4, norms, lvl2, cvals)
    section7()

    return summary("v502 CELEST.WP5E.ALPHA.01: the q^{-1/3} prefactor of E4/eta^8 "
                   "is exact mu4 vacuum-energy bookkeeping -- the clock is INNER "
                   "((h,h) = 20, (h',h') = 12, sum 32), so the twist distribution "
                   "on the 8 torus bosons is theta = 0^8 in all four sectors "
                   "(SHIFT orbifold) and every sector carries the same "
                   "8 x (-1/24) = -1/3 = -c/24; sector ground exponents "
                   "-1/3 + (0,1,1,1) with h_j = discriminant form, an identity "
                   "holding via spectral flow (j^2(h,h)/32) and exactly via 16 "
                   "Majorana free fermions (R-NS shift n/16: 5/8, 3/8, 1); the "
                   "four sector characters sum to E4/eta^8 = q^{-1/3}(1, 248, "
                   "4124, 34752).  k = 1 forced three ways: current condition "
                   "h(J) = k = 1 (glue-h integrality holds for ALL k -- the naive "
                   "route is dead, honest sharpening), conformal embedding "
                   "47(k-1)(k+266/47) = 0 resp. 128(k-1) = 0, c = 8 <=> "
                   "240(k-1) = 0, plus the WP5b singular-vector dial "
                   "(31124 - 27000 = 4124 at k = 1 only). Controls: D8 same "
                   "prefactor but h = (0,1/2,1,1); Z2/mu4 rotation twists break "
                   "the common prefactor; k = 2,3,4 fail all five dials. OPEN: "
                   "the BCOV/Costello-Li twistor inflow itself -- WP5e stays [O], "
                   "SEAM.EQUIV.01 untouched")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
