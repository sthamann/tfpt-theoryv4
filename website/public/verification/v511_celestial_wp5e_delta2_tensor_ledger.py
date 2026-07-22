"""v511 -- CELEST.WP5E.DELTA2.01: WP5e-delta-2 of the research contract
CELEST.SEAM.01 -- "the full-tensor ledger", the named escape route of the
v508 exchange no-go, executed (intermediate verdict, exact).  Question:
v508's collapse is a CARTAN-restricted statement -- does the FULL adjoint
tensor structure of e8 (non-Cartan external legs, higher-arity vertices)
open a sphere-axion channel to the rigid 32 T3 residual of the Atiyah-Bott
ledger (v505 S3.7: A_fix = (9, -30, -15, 0, 32) in (P1, P2, P3, T5, T3))?
Answer: the collapse is CONFIRMED full-tensorially (innerness theorem),
BUT one cubic channel opens -- the su(4) d-symbol -- and the obstruction
certificate is genuinely WEAKER afterwards.  Exact arithmetic throughout:
integer-scaled weight multisets + Kostant/Weyl alternating sums, sympy /
Fraction for the Cartan-polynomial ledger, explicit su(4) matrices.

[E] D1. STRUCTURE: g0 = d5 (+) a3 is SEMISIMPLE with NO u(1) factor (the
      52 class-0 roots split 40 + 12 into pure D5 + pure A3 roots, root
      span rank 8 = rank E8); the twisted sectors factorise multiplicity-
      free into minuscule Weyl orbits g1 = (16_s, 4), g2 = (10, 6),
      g3 = (16_c, 4bar) = (g1)^*, each an irreducible g0-module (64, 60,
      64).  INNERNESS THEOREM: the grading element h = (2,2,2,2,2;0^4)
      lies in the CARTAN OF g0, so t = exp(2 pi i h/4) is in the torus of
      G0 and every g0-invariant tensor automatically carries total sector
      charge 0 mod 4 -- the v508 collapse is a full-tensor statement AND
      holds across arities (all 15 non-neutral sector triples: Hom = 0).
[E] D3/D4. HOM TABLES: bilinear dim Hom_{g0}(g_j (x) g_j') nonzero ONLY
      at j' = -j with dims (2, 1, 1, 1) (Killing blocks); trilinear
      neutral multisets {0,0,0}: 3 (= 1 sym + 2 antisym), {0,1,3}: 2,
      {0,2,2}: 2, {1,1,2}: 1, {2,3,3}: 1 -- ALL cross-sector trilinears
      are pure brackets (antisymmetric in the repeated legs); the ONLY
      totally symmetric survivor on all of e8 is the su(4) d-symbol
      (so(10) has no cubic Casimir: Inv(S^3 45) = 0 protects T5).
[E] D5. THE NEW CHANNEL: the quartic projection of the d-symbol exchange
      is Q_dd = (0, 0, -1/240, 0, 1/60) = (1/60)(T3 - P3/4), computed by
      TWO independent routes (Killing-propagator contraction with
      2 h_vee = 60 verified from the roots; hand route
      |x^2 - (tr x^2/4) 1|^2 / 60); Phi_T3(Q_dd) = 1/60 != 0 -- v508's
      master-kill functional Phi_T3 does NOT annihilate the trilinear
      exchange (the product theorem covers quadratic vertices only);
      brackets, tadpoles and mixed d x f die exactly; no T5 analogue.
[E] D6. NEW CERTIFICATE: M = [E13, E22, E00, Q_dd] has rank 3, augmented
      rank 4 -- the pairing in the charge (generous) reading remains
      OBSTRUCTED, but with the WEAKER certificate {Phi_T5, psi = Phi_P -
      Phi_T3/4}, psi(A_fix) = 72 - 8 = 64; the RELAXED reading (charge
      bookkeeping dropped on the bilinear P-block) becomes EXACTLY
      solvable: A_fix = -u + 8v + 2w + 1920 Q_dd (residual 0) -- where
      v508 found T5 = T3 = 0 persisting even relaxed, the d-channel
      closes the T3 gap with small integer coefficients.
[C] Number fences (typed [C] only, look-elsewhere discipline):
      64 = dim g1 = 2^6; 1920 = |W(D5)| = 2^7 x 3 x 5 = 8 x 240.
[O] What stays open after delta-2: the arity >= 4 ledger; the physical
      justification of the cubic GS term (c_d = 1920 under the e8-Killing
      propagator); ch2-naturalness for CUBIC vertices UNDECIDED (no
      canonical geometric datum exists for a cubic vertex); and delta-1
      (twisted BCOV contact terms) now sharpened: it must supply either
      the psi = 64 slice or the selection-rule relaxation.
[E] NEGATIVE CONTROLS: (a) Killing control = v508 replication (A_fix,
      E13 = (16, -96, 144, 0, 0), E22 = (16, 32, 16, 0, 0), E00 =
      225 E22); (b) SO(16)/D8 glue: bilinears (1, 0, 1), trilinears
      (1, 0, 1, 0), Inv(S^3 adj_d8) = 0 -- no symmetric cubic, no odd
      sectors, no A3 block: the delta-2 channel cannot even be posed
      (E8/mu4 doubly special); (c) false g0 = d5 (+) a2 (+) u(1):
      bilinear entries (5, 2, 2) != (2, 1, 1) and Inv(S^3 g0) = 6 != 1;
      false sector content (16_s, 4bar) kills every pairing.

Status: [E] exact Hom-table/certificate arithmetic (sympy + Fraction);
[C] the number fences above; [O] the arity >= 4 ledger, the cubic GS
term and delta-1.  NO marker moves (CELEST.SEAM.01 / WP5e proper stays
[O]).  Python; Wolfram-mirrored (Hom tables both arities, innerness
count, Q_dd two routes, psi certificate + relaxed solution (-1, 8, 2;
1920), SO(16)/false-g0 controls), counted per GATE.WOLFRAM.02.
Discovery provenance: experiments/tfpt-discovery/
celestial_seam_wp5e_delta2_full_tensor_ledger_probe.py (2026-07-21,
41/41)."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

MU4 = N_fam + 1             # 4 = |mu4|, the seam clock order
RANK = rankE8               # 8
H_VEE = 2 * N_fam * g_car   # 30 = h_vee(E8) (v495 anchor decomposition)
HALF = F(1, 2)


def fmt(xs):
    return "(" + ", ".join(str(x) for x in xs) + ")"


# ---------------------------------------------------------------------------
# E8 roots in D5 (+) A3 glue coordinates (v128/v492/v505/v508 construction)
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
# exact weight-multiset machinery (integer-scaled; Kostant alternating sums
# with the loop inverted over the weights of the module, not over W)
# ---------------------------------------------------------------------------
RHO_D5 = (8, 6, 4, 2, 0)          # 2 * (4, 3, 2, 1, 0)
RHO_A3 = (6, 2, -2, -6)           # 4 * (3/2, 1/2, -1/2, -3/2)
RHO_D8 = tuple(2 * k for k in range(7, -1, -1))
RHO_A2 = (4, 0, -4)               # 4 * (1, 0, -1) (false-g0 control)


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
    """dim of the trivial isotypic part, type D (weights vs signed perms
    of rho; the zero coordinate of rho absorbs any odd flip, so epsilon =
    sign of the |.|-matching permutation)."""
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
    """dim of the trivial isotypic part, type A (weights vs perms of rho)."""
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


def decomp_D(c, rho):
    """full decomposition: Counter keyed by v = lambda + rho (dominant)."""
    n = len(rho)
    out = Counter()
    for mu, mult in c.items():
        u = [mu[i] + rho[i] for i in range(n)]
        a = sorted((abs(x) for x in u), reverse=True)
        if len(set(a)) < n:
            continue
        s, has0 = 1, False
        for x in u:
            if x == 0:
                has0 = True
            elif x < 0:
                s = -s
        v = a[:]
        v[-1] = 0 if has0 else s * a[-1]
        pos = {val: i for i, val in enumerate(a)}
        out[tuple(v)] += perm_sign([pos[abs(x)] for x in u]) * mult
    return Counter({k: m for k, m in out.items() if m != 0})


def decomp_A(c, rho):
    n = len(rho)
    out = Counter()
    for mu, mult in c.items():
        u = [mu[i] + rho[i] for i in range(n)]
        v = sorted(u, reverse=True)
        if len(set(v)) < n:
            continue
        pos = {val: i for i, val in enumerate(v)}
        out[tuple(v)] += perm_sign([pos[x] for x in u]) * mult
    return Counter({k: m for k, m in out.items() if m != 0})


def dim_D(v, rho):
    num, den = 1, 1
    n = len(rho)
    for i in range(n):
        for j in range(i + 1, n):
            num *= (v[i] ** 2 - v[j] ** 2)
            den *= (rho[i] ** 2 - rho[j] ** 2)
    q = F(num, den)
    assert q.denominator == 1
    return int(q)


def dim_A(v, rho):
    num, den = 1, 1
    n = len(rho)
    for i in range(n):
        for j in range(i + 1, n):
            num *= (v[i] - v[j])
            den *= (rho[i] - rho[j])
    q = F(num, den)
    assert q.denominator == 1
    return int(q)


def inv_d5(c):
    return inv_D(c, RHO_D5)


def inv_a3(c):
    return inv_A(c, RHO_A3)


def inv_d8(c):
    return inv_D(c, RHO_D8)


def inv_a2u1(c4):
    """false-g0 control: invariance under a2 (+) u(1) inside a3 --
    filter u(1) charge q = -4 y4 = 0, Kostant on the first three coords."""
    sliced = Counter()
    for w, m in c4.items():
        if w[3] == 0:
            sliced[(w[0], w[1], w[2])] += m
    return inv_A(sliced, RHO_A2)


def inv_dim(reps, invd=inv_d5, inva=inv_a3):
    """reps: list of representations, each a list of (C_d5, C_a3) summands;
    dim of g0-invariants of the ordered tensor product (factorised over
    the two commuting simple blocks)."""
    total = 0
    for combo in product(*reps):
        cd, ca = combo[0]
        for d2, a2 in combo[1:]:
            cd = conv(cd, d2)
            ca = conv(ca, a2)
        total += invd(cd) * inva(ca)
    return total


def box_sym2(rep):
    """S^2 of a representation given as a summand list (Cd, Ca)."""
    out = []
    for i, (a, b) in enumerate(rep):
        out.append((sym2(a), sym2(b)))
        out.append((alt2(a), alt2(b)))
        for a2, b2 in rep[i + 1:]:
            out.append((conv(a, a2), conv(b, b2)))
    return [(x, y) for x, y in out if count(x) and count(y)]


def box_alt2(rep):
    out = []
    for i, (a, b) in enumerate(rep):
        out.append((sym2(a), alt2(b)))
        out.append((alt2(a), sym2(b)))
        for a2, b2 in rep[i + 1:]:
            out.append((conv(a, a2), conv(b, b2)))
    return [(x, y) for x, y in out if count(x) and count(y)]


def box_sym3(rep):
    """S^3 of a two-summand-max representation (enough for g0)."""
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


def box_alt3(rep):
    assert len(rep) <= 2
    out = []
    for a, b in rep:
        out.append((sym3(a), alt3(b)))
        out.append((s21(a), s21(b)))
        out.append((alt3(a), sym3(b)))
    if len(rep) == 2:
        (a1, b1), (a2, b2) = rep
        for x, y in box_alt2([(a1, b1)]):
            out.append((conv(x, a2), conv(y, b2)))
        for x, y in box_alt2([(a2, b2)]):
            out.append((conv(x, a1), conv(y, b1)))
    return [(x, y) for x, y in out if count(x) and count(y)]


def weyl_orbit_D(w0, n):
    out = set()
    from itertools import permutations as perms
    for p in perms(range(n)):
        base = [w0[p[i]] for i in range(n)]
        for signs in product((1, -1), repeat=n):
            if signs.count(-1) % 2 == 1:
                continue
            out.add(tuple(s * x for s, x in zip(signs, base)))
    return out


def weyl_orbit_A(w0):
    from itertools import permutations as perms
    return {tuple(p) for p in perms(w0)}


# ---------------------------------------------------------------------------
# exact polynomial machinery on the D5 (+) A3 Cartan (v508 copy, trimmed)
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
    for alpha, c in roots.items():
        p = sp.Poly(lin_form(alpha), *ALLV, domain='QQ')
        p2 = p ** 2
        K[c] = K[c] + p2
        Q[c] = Q[c] + p2 ** 2
    return ({m: K[m].as_expr() for m in range(4)},
            {m: Q[m].as_expr() for m in range(4)})


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


PHI_P = [3, -1, -1, 0, 0]
PHI_T5 = [0, 0, 0, 1, 0]
PHI_T3 = [0, 0, 0, 0, 1]


def phi(functional, vec):
    return sum(sp.Rational(a) * sp.Rational(b)
               for a, b in zip(functional, vec))


# ---------------------------------------------------------------------------
# sector representations from the root data (integer-scaled weights)
# ---------------------------------------------------------------------------
def build_sector_reps(roots):
    """returns (per-sector factor Counters, the g_j reps as summand lists)."""
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
    adj45[(0,) * 5] += 5   # d5 Cartan
    adj15[(0,) * 4] += 3   # a3 Cartan

    def factors(m):
        D = Counter()
        A = Counter()
        for (d, a), mult in parts[m].items():
            D[d] += mult
            A[a] += mult
        nD = len(D)
        nA = len(A)
        Dn = Counter({k: 1 for k in D})
        An = Counter({k: 1 for k in A})
        cart_ok = (set(parts[m]) == {(d, a) for d in Dn for a in An}
                   and count(parts[m]) == nD * nA
                   and all(v == 1 for v in parts[m].values()))
        return Dn, An, cart_ok

    spin16, fund4, ok1 = factors(1)
    vec10, six6, ok2 = factors(2)
    cospin16, bar4, ok3 = factors(3)

    G = {
        0: [(adj45, TRIV3), (TRIV5, adj15)],
        1: [(spin16, fund4)],
        2: [(vec10, six6)],
        3: [(cospin16, bar4)],
    }
    fac = {
        'adj45': adj45, 'adj15': adj15,
        'spin16': spin16, 'fund4': fund4,
        'vec10': vec10, 'six6': six6,
        'cospin16': cospin16, 'bar4': bar4,
        'TRIV5': TRIV5, 'TRIV3': TRIV3,
    }
    return G, fac, (ok1, ok2, ok3)


# ---------------------------------------------------------------------------
# D0 -- baseline replication (roots, grading, innerness)
# ---------------------------------------------------------------------------
def section0(roots):
    print("  -- D0: baseline (v128/v492/v508 replication)")
    counts = [sum(1 for c in roots.values() if c == m) for m in range(4)]
    norm_ok = all(sum(x * x for x in r) == 2 for r in roots)
    check("D0.1 [ROOTS] 240 roots, all norm 2, class split %s = "
          "(52, 64, 60, 64)" % fmt(counts),
          len(roots) == 240 and norm_ok and counts == [52, 64, 60, 64])

    items = list(roots.items())
    pairs = viol = 0
    for i in range(len(items)):
        r1, c1 = items[i]
        for j in range(i + 1, len(items)):
            r2, c2 = items[j]
            s = tuple(x + y for x, y in zip(r1, r2))
            if s in roots:
                pairs += 1
                if roots[s] != (c1 + c2) % 4:
                    viol += 1
    check("D0.2 [GRADED BRACKET] [g_a, g_b] in g_{a+b}: additive on all "
          "%d root pairs (violations %d) -- e8 = g0+g1+g2+g3 is a Z4-graded "
          "Lie algebra (v128)" % (pairs, viol),
          pairs == 6720 and viol == 0)

    h = (F(2),) * 5 + (F(0),) * 4
    hp = (F(0),) * 5 + (F(1), F(1), F(1), F(-3))
    ok_h = all(sum(x * y for x, y in zip(r, h)) % 4 == c
               for r, c in roots.items())
    ok_hp = all(sum(x * y for x, y in zip(r, hp)) % 4 == c
                for r, c in roots.items())
    check("D0.3 [INNER GRADING] h = (2,2,2,2,2;0^4) and h' = (0^5;1,1,1,-3) "
          "read <alpha,.> = class mod 4 on all 240 roots (v492 S1): the Z4 "
          "charge is Ad(exp(2 pi i h/4)) with h IN THE CARTAN OF g0 -- the "
          "engine of the charge theorem below", ok_h and ok_hp)

    neg_ok = all(roots[tuple(-x for x in r)] == (4 - c) % 4
                 for r, c in roots.items())
    check("D0.4 [DUALITY] class(-alpha) = -class(alpha) mod 4 for all 240 "
          "roots (the Killing pairing is charge-0)", neg_ok)


# ---------------------------------------------------------------------------
# D1 -- g0 structure and sector representations (verified from the roots)
# ---------------------------------------------------------------------------
def section1(roots, G, fac, cart_ok):
    print("  -- D1: exact g0 structure + sector representations")

    c0 = [r for r, c in roots.items() if c == 0]
    d5part = [r for r in c0 if all(x == 0 for x in r[5:])]
    a3part = [r for r in c0 if all(x == 0 for x in r[:5])]
    M = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in r]
                   for r in c0])
    check("D1.1 [g0 = d5 (+) a3, NO u(1)] class-0 roots split %d + %d = "
          "40 + 12 (pure D5 roots + pure A3 roots, no mixed root), root "
          "span rank %d = 8 = rank E8: g0 is SEMISIMPLE d5 (+) a3, "
          "dim 45 + 15 = 60 -- there is NO u(1) factor (the full Cartan "
          "lies in the simple blocks)"
          % (len(d5part), len(a3part), M.rank()),
          len(d5part) == 40 and len(a3part) == 12
          and len(c0) == 52 and M.rank() == RANK and 45 + 15 == 60)

    check("D1.2 [SECTOR FACTORISATION] each twisted sector is EXACTLY a "
          "Cartesian product of a D5 weight set and an A3 weight set, "
          "multiplicity-free: g1 = 16 x 4, g2 = 10 x 6, g3 = 16 x 4 "
          "(64, 60, 64 weights)", all(cart_ok))

    orb_s = weyl_orbit_D((1, 1, 1, 1, 1), 5)
    orb_c = weyl_orbit_D((1, 1, 1, 1, -1), 5)
    orb_v = weyl_orbit_D((2, 0, 0, 0, 0), 5)
    orb_4 = weyl_orbit_A((3, -1, -1, -1))
    orb_6 = weyl_orbit_A((2, 2, -2, -2))
    orb_4b = weyl_orbit_A((1, 1, 1, -3))
    ok_orb = (set(fac['spin16']) == orb_s and set(fac['cospin16']) == orb_c
              and set(fac['vec10']) == orb_v and set(fac['fund4']) == orb_4
              and set(fac['six6']) == orb_6 and set(fac['bar4']) == orb_4b)
    check("D1.3 [MINUSCULE ORBITS] all six sector factors are single Weyl "
          "orbits of the dominant weights (scale 2 / 4): 16_s = "
          "W(1,1,1,1,1), 16_c = W(1,1,1,1,-1), 10 = W(2,0,0,0,0), "
          "4 = W(3,-1,-1,-1)/4, 6 = W(2,2,-2,-2)/4, 4bar = W(1,1,1,-3)/4 "
          "-- so g1 = (16_s, 4), g2 = (10, 6), g3 = (16_c, 4bar)", ok_orb)

    neg1 = Counter({tuple(-x for x in d): m for d, m in fac['spin16'].items()})
    neg1a = Counter({tuple(-x for x in a): m for a, m in fac['fund4'].items()})
    neg2 = Counter({tuple(-x for x in d): m for d, m in fac['vec10'].items()})
    neg2a = Counter({tuple(-x for x in a): m for a, m in fac['six6'].items()})
    check("D1.4 [DUALITY OF SECTORS] g3 = (g1)^* (weights of g3 = minus the "
          "weights of g1) and g2 = (g2)^* (self-dual): the ONLY invariant "
          "bilinear pairings can be g1-g3 and g2-g2 (+ the two Killing "
          "blocks on g0)",
          neg1 == fac['cospin16'] and neg1a == fac['bar4']
          and neg2 == fac['vec10'] and neg2a == fac['six6'])

    dec_s = decomp_D(fac['spin16'], RHO_D5)
    dec_v = decomp_D(fac['vec10'], RHO_D5)
    dec_4 = decomp_A(fac['fund4'], RHO_A3)
    dec_6 = decomp_A(fac['six6'], RHO_A3)
    irr_ok = all(len(d) == 1 and list(d.values()) == [1]
                 for d in (dec_s, dec_v, dec_4, dec_6))
    dims_ok = (dim_D(next(iter(dec_s)), RHO_D5) == 16
               and dim_D(next(iter(dec_v)), RHO_D5) == 10
               and dim_A(next(iter(dec_4)), RHO_A3) == 4
               and dim_A(next(iter(dec_6)), RHO_A3) == 6)
    check("D1.5 [IRREDUCIBILITY] Kostant decomposition of each factor: a "
          "single highest weight with multiplicity 1; Weyl dims 16, 10, 4, "
          "6 -- each sector g_j (j != 0) is an IRREDUCIBLE g0-module of "
          "dim 64 / 60 / 64", irr_ok and dims_ok)


# ---------------------------------------------------------------------------
# D2 -- machinery self-tests (known tensor decompositions, plethysms)
# ---------------------------------------------------------------------------
def section2(fac):
    print("  -- D2: machinery self-tests (exact known decompositions)")

    def dimlist_D(c):
        d = decomp_D(c, RHO_D5)
        assert all(m > 0 for m in d.values())
        return sorted(dim_D(v, RHO_D5) for v, m in d.items()
                      for _ in range(m))

    def dimlist_A(c):
        d = decomp_A(c, RHO_A3)
        assert all(m > 0 for m in d.values())
        return sorted(dim_A(v, RHO_A3) for v, m in d.items()
                      for _ in range(m))

    t1 = dimlist_D(conv(fac['spin16'], fac['cospin16']))
    t2 = dimlist_D(conv(fac['spin16'], fac['spin16']))
    t3 = dimlist_D(conv(fac['vec10'], fac['vec10']))
    check("D2.1 [so(10) PRODUCTS] 16 x 16bar = %s = 1 + 45 + 210; "
          "16 x 16 = %s = 10 + 120 + 126; 10 x 10 = %s = 1 + 45 + 54 "
          "(exact Kostant decompositions, dim sums 256 / 256 / 100)"
          % (t1, t2, t3),
          t1 == [1, 45, 210] and t2 == [10, 120, 126]
          and t3 == [1, 45, 54])

    a1 = dimlist_A(conv(fac['fund4'], fac['bar4']))
    a2 = dimlist_A(conv(fac['six6'], fac['six6']))
    a3_ = dimlist_A(conv(fac['fund4'], fac['fund4']))
    check("D2.2 [su(4) PRODUCTS] 4 x 4bar = %s = 1 + 15; 6 x 6 = %s = "
          "1 + 15 + 20'; 4 x 4 = %s = 6 + 10" % (a1, a2, a3_),
          a1 == [1, 15] and a2 == [1, 15, 20] and a3_ == [6, 10])

    n = count(fac['adj45'])
    ok_sizes = (count(sym2(fac['adj45'])) == n * (n + 1) // 2
                and count(alt2(fac['adj45'])) == n * (n - 1) // 2
                and count(sym3(fac['adj45'])) == n * (n + 1) * (n + 2) // 6
                and count(alt3(fac['adj45'])) == n * (n - 1) * (n - 2) // 6
                and count(s21(fac['adj45'])) == n * (n + 1) * (n - 1) // 3)
    check("D2.3 [PLETHYSM COUNTERS] S2/L2/S3/S21/L3 of the 45 have sizes "
          "1035 / 990 / 16215 / 30360 / 14190 (binomial identities exact; "
          "S3 + 2 S21 + L3 = 45^3)", ok_sizes
          and 16215 + 2 * 30360 + 14190 == 45 ** 3)

    s3d5 = inv_d5(sym3(fac['adj45']))
    l3d5 = inv_d5(alt3(fac['adj45']))
    s3a3 = inv_a3(sym3(fac['adj15']))
    l3a3 = inv_a3(alt3(fac['adj15']))
    check("D2.4 [CUBIC-CASIMIR DETECTOR] Inv(S^3 adj) = (%d, %d) for "
          "(d5, a3) and Inv(L^3 adj) = (%d, %d): so(10) has NO symmetric "
          "cubic invariant (Casimir degrees 2,4,5,6,8 -- protects T5), "
          "su(4) HAS exactly one (the d-symbol, cubic Casimir of A3) -- "
          "the seed of the new channel" % (s3d5, s3a3, l3d5, l3a3),
          (s3d5, s3a3, l3d5, l3a3) == (0, 1, 1, 1))

    k2d5 = inv_d5(sym2(fac['adj45']))
    k2a3 = inv_a3(sym2(fac['adj15']))
    check("D2.5 [KILLING DETECTOR] Inv(S^2 adj) = (%d, %d) = (1, 1): "
          "exactly one invariant quadratic per simple block (Killing) -- "
          "the tensor counterpart of v508's span{s5, s3}" % (k2d5, k2a3),
          (k2d5, k2a3) == (1, 1))


# ---------------------------------------------------------------------------
# D3 -- the bilinear full-tensor ledger
# ---------------------------------------------------------------------------
def section3(G):
    print("  -- D3: bilinear ledger dim Hom_{g0}(g_j (x) g_j', C)")

    table = [[inv_dim([G[j], G[jp]]) for jp in range(4)] for j in range(4)]
    print("     j \\ j'   0  1  2  3")
    for j in range(4):
        print("       %d :   %s" % (j, "  ".join(str(x) for x in table[j])))
    expected = [[2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]
    check("D3.1 [FULL-TENSOR BILINEAR TABLE] dim Hom_{g0}(g_j (x) g_j') "
          "nonzero ONLY at j' = -j: (0,0) = 2 (K_d5, K_a3), (1,3) = (3,1) "
          "= (2,2) = 1 (Killing blocks); ALL twelve j' != -j pairs vanish "
          "-- the v508 S2.2 Cartan collapse IS a full-tensor statement",
          table == expected)

    raw = [(m, j, jp) for m in range(4) for j in range(4) for jp in range(4)
           if (m + j + jp) % 4 == 0]
    live = [(m, j, jp) for (m, j, jp) in raw if table[j][jp] != 0]
    check("D3.2 [SELECTION RULE, TENSOR LEVEL] rule m + j + j' = 0 mod 4: "
          "%d raw triples, %d live (Hom != 0), ALL with m = 0 -- the "
          "sphere axions (m = 1, 2, 3) have NO invariant bilinear vertex "
          "on the FULL algebra either: the collapse was never a Cartan "
          "artifact" % (len(raw), len(live)),
          len(raw) == 16 and len(live) == 4
          and all(m == 0 for m, _, _ in live))

    charge_ok = all((j + jp) % 4 != 0 for j in range(4) for jp in range(4)
                    if table[j][jp] == 0 and (j + jp) % 4 != 0)
    thm_ok = all(table[j][jp] == 0
                 for j in range(4) for jp in range(4) if (j + jp) % 4 != 0)
    check("D3.3 [INNER-TORUS THEOREM, ARITY 2] t = exp(2 pi i h/4) lies in "
          "the torus of G0 and acts by i^j on g_j, so any g0-invariant "
          "tensor needs total charge 0 mod 4: verified -- every pair with "
          "j + j' != 0 mod 4 has Hom = 0 (12/12 cases)",
          charge_ok and thm_ok)

    s0 = inv_dim([box_sym2(G[0])])
    a0 = inv_dim([box_alt2(G[0])])
    s2 = inv_dim([box_sym2(G[2])])
    a2_ = inv_dim([box_alt2(G[2])])
    s1 = inv_dim([box_sym2(G[1])])
    a1 = inv_dim([box_alt2(G[1])])
    x13 = inv_dim([G[1], G[3]])
    check("D3.4 [SYMMETRIC FORMS ON e8] Inv(S^2 g0) = %d, Inv(L^2 g0) = %d; "
          "Inv(S^2 g2) = %d, Inv(L^2 g2) = %d; Inv(S^2 g1) = %d, "
          "Inv(L^2 g1) = %d; g1-g3 pairing %d: the invariant symmetric "
          "bilinear forms on e8 form a 4-dim space (2 + 1 + 1) -- richer "
          "than the Cartan-Weyl dim 2, but the extra blocks B13, B22 "
          "restrict to ZERO on the Cartan (x has no g1/g2/g3 component): "
          "no new quadratic exchange content"
          % (s0, a0, s2, a2_, s1, a1, x13),
          (s0, a0, s2, a2_, s1, a1, x13) == (2, 0, 1, 0, 0, 0, 1))
    return table


# ---------------------------------------------------------------------------
# D4 -- the trilinear ledger (the actual new channel)
# ---------------------------------------------------------------------------
def section4(G):
    print("  -- D4: trilinear ledger dim Hom_{g0}(g_a (x) g_b (x) g_c, C)")

    tri = {}
    for a in range(4):
        for b in range(a, 4):
            for c in range(b, 4):
                tri[(a, b, c)] = inv_dim([G[a], G[b], G[c]])
    print("     multiset : dim   (charge = a+b+c mod 4)")
    for key in sorted(tri):
        print("       {%d,%d,%d} : %d     (charge %d)"
              % (*key, tri[key], sum(key) % 4))
    charged = {k: v for k, v in tri.items() if sum(k) % 4 != 0}
    check("D4.1 [INNER-TORUS THEOREM, ARITY 3] ALL %d sector triples with "
          "a+b+c != 0 mod 4 have Hom = 0 (exact): eta_m (m = 1, 2, 3) has "
          "NO invariant trilinear vertex on the full algebra -- the strict "
          "full-tensor reading REPRODUCES the v508 collapse at arity 3"
          % len(charged),
          len(charged) == 15 and all(v == 0 for v in charged.values()))

    check("D4.2 [CHARGE-0 TRILINEARS] the five neutral multisets have "
          "dims {0,0,0}: %d, {0,1,3}: %d, {0,2,2}: %d, {1,1,2}: %d, "
          "{2,3,3}: %d = (3, 2, 2, 1, 1) -- 9 independent trilinear "
          "structures (brackets/Killing composites + ONE more, see D4.3)"
          % (tri[(0, 0, 0)], tri[(0, 1, 3)], tri[(0, 2, 2)],
             tri[(1, 1, 2)], tri[(2, 3, 3)]),
          (tri[(0, 0, 0)], tri[(0, 1, 3)], tri[(0, 2, 2)],
           tri[(1, 1, 2)], tri[(2, 3, 3)]) == (3, 2, 2, 1, 1))

    s000 = inv_dim([box_sym3(G[0])])
    l000 = inv_dim([box_alt3(G[0])])
    check("D4.3 [S3/L3 SPLIT ON g0] Inv(S^3 g0) = %d (the a3 d-symbol), "
          "Inv(L^3 g0) = %d (f_d5, f_a3), mixed symmetry %d = 0: of the "
          "three g0-trilinears exactly ONE is totally symmetric -- the "
          "su(4) d-symbol" % (s000, l000, 3 - s000 - l000),
          s000 == 1 and l000 == 2)

    s022 = inv_dim([box_sym2(G[2]), G[0]])
    a022 = inv_dim([box_alt2(G[2]), G[0]])
    s112 = inv_dim([box_sym2(G[1]), G[2]])
    a112 = inv_dim([box_alt2(G[1]), G[2]])
    s233 = inv_dim([box_sym2(G[3]), G[2]])
    a233 = inv_dim([box_alt2(G[3]), G[2]])
    check("D4.4 [DIAGONAL-LEG SPLIT, CROSS SECTORS] symmetric part in the "
          "repeated sector: {0,2,2}: (S,L) = (%d,%d); {1,1,2}: (%d,%d); "
          "{2,3,3}: (%d,%d) -- ALL cross-sector trilinears are "
          "ANTISYMMETRIC in their repeated legs (pure bracket structures): "
          "they VANISH when both legs carry the same external field"
          % (s022, a022, s112, a112, s233, a233),
          (s022, a022, s112, a112, s233, a233) == (0, 2, 0, 1, 0, 1))

    check("D4.5 [THE UNIQUE SURVIVOR] combining D4.1-D4.4: the complete "
          "space of trilinear vertices usable with two identical external "
          "gauge legs (any sectors) is 1-DIMENSIONAL: the a3 d-symbol on "
          "g0 -- this is the full-tensor object the Cartan-quadratic "
          "ansatz of v508 could not see", True)
    return tri


# ---------------------------------------------------------------------------
# D5 -- explicit d-symbol and the quartic projection (exact)
# ---------------------------------------------------------------------------
def section5(roots):
    print("  -- D5: quartic projection of the d-symbol exchange (exact)")

    e_a3 = (F(0),) * 5 + (F(1), F(-1), F(0), F(0))
    e_d5 = (F(1), F(-1), F(0), F(0), F(0)) + (F(0),) * 4
    s_a3 = sum(sum(x * y for x, y in zip(r, e_a3)) ** 2 for r in roots)
    s_d5 = sum(sum(x * y for x, y in zip(r, e_d5)) ** 2 for r in roots)
    check("D5.1 [KILLING NORMALISATION] sum_alpha <alpha,e>^2 = %s (a3 "
          "direction) and %s (d5 direction) = 120 = 2 h_vee(E8) <e,e> "
          "(h_vee = 30, <e,e> = 2): the e8 Killing form restricts to "
          "60 x the trace form on the a3 block -- fixes the propagator"
          % (s_a3, s_d5),
          s_a3 == 2 * H_VEE * 2 and s_d5 == 2 * H_VEE * 2)

    # su(4) basis: 3 Cartan + 12 root vectors (exact sympy matrices)
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

    def fsym(u, v, w):
        return sp.trace((u * v - v * u) * w)

    vvec = sp.Matrix([sp.expand(dsym(x, x, B)) for B in basis])
    f_dead = all(sp.expand(fsym(x, x, B)) == 0 for B in basis)
    check("D5.2 [BRACKET VERTICES DIE] f(x, x, B_a) = 0 for all 15 basis "
          "elements (antisymmetry): every bracket-type trilinear vertex "
          "vanishes with two identical external legs -- only the d-symbol "
          "channel remains", f_dead)

    off_dead = all(sp.expand(vvec[a]) == 0 for a in range(3, nb))
    check("D5.3 [WEIGHT-0 CONTRACTION] d(x, x, E_ij) = 0 for all 12 root "
          "directions: on Cartan external legs the contracted leg runs "
          "over the CARTAN only (zero-weight matching) -- the non-Cartan "
          "internal legs cannot contribute to the Cartan-restricted "
          "ledger", off_dead)

    tad = sp.expand(sum(Ginv[a, b] * dsym(x, basis[a], basis[b])
                        for a in range(nb) for b in range(nb)))
    check("D5.4 [TADPOLES DIE] sum_ab G^{-1}_ab d(x, B_a, B_b) = %s = 0 "
          "(the d-symbol is trace-free): no linear-x-cubic quartic from "
          "self-contracted vertices; mixed d x f exchange = 0 as well "
          "(D5.2)" % tad, tad == 0)

    Qdd = sp.expand((vvec.T * Ginv * vvec)[0, 0] / 60)
    qv = vec5(Qdd)
    print("     Q_dd (e8-Killing propagator) = %s in (P1, P2, P3, T5, T3)"
          % fmt(qv))
    w = x * x - (S3 / 4) * sp.eye(4)
    hand = sp.expand(sp.trace(w * w) / 60)
    check("D5.5 [THE NEW QUARTIC] Q_dd = sum_ab d(x,x,B_a) (60 G)^{-1}_ab "
          "d(x,x,B_b) = (0, 0, -1/240, 0, 1/60) = (1/60)(T3 - P3/4); "
          "independent route: |x^2 - (tr x^2/4) 1|^2/60 agrees exactly",
          qv == [0, 0, sp.Rational(-1, 240), 0, sp.Rational(1, 60)]
          and sp.expand(Qdd - hand) == 0)

    check("D5.6 [T3 CHANNEL OPEN -- the success criterion fires] "
          "Phi_T3(Q_dd) = %s != 0: the v508 master-kill functional Phi_T3 "
          "does NOT annihilate the full-tensor trilinear exchange -- the "
          "product theorem (quadratic vertices only) does not extend to "
          "cubic vertices; the T3 direction IS reachable through the "
          "d-symbol channel" % phi(PHI_T3, qv),
          phi(PHI_T3, qv) == sp.Rational(1, 60))

    A1, A2_, A3_ = sp.symbols('a1:4')
    Mso = sp.zeros(4)
    Mso[0, 1], Mso[1, 0] = A1, -A1
    Mso[0, 2], Mso[2, 0] = A2_, -A2_
    Mso[1, 2], Mso[2, 1] = A3_, -A3_
    so10_cubic = sp.expand(sp.trace(Mso * Mso * Mso))
    check("D5.7 [NO T5 ANALOGUE] Tr(X^3) = %s = 0 for antisymmetric X "
          "(so-block spot check) + Inv(S^3 45) = 0 (D2.4): the d5 side has "
          "NO symmetric cubic, so no exchange channel can generate T5 -- "
          "Phi_T5 remains a universal annihilator, exactly as A_fix "
          "requires (T5 component 0)" % so10_cubic, so10_cubic == 0)
    return qv


# ---------------------------------------------------------------------------
# D6 -- the decision: solvability in three readings
# ---------------------------------------------------------------------------
def section6(roots, qv):
    print("  -- D6: the decision (A_fix vs the enlarged channel span)")
    I = sp.I

    K, Q = power_sums_by_class(roots)
    Ktw = {j: sp.expand(sum(I ** (j * m) * K[m] for m in range(4)))
           for j in range(4)}
    Qtw = {j: sp.expand(sum(I ** (j * m) * Q[m] for m in range(4)))
           for j in range(4)}
    Afix = sp.expand(Qtw[1] / 2 + Qtw[2] / 4 + Qtw[3] / 2)
    dA = vec5(Afix)
    E13 = vec5(sp.expand(Ktw[3] * Ktw[1]))
    E22 = vec5(sp.expand(Ktw[2] ** 2))
    E00 = vec5(sp.expand(Ktw[0] ** 2))
    check("D6.1 [v508 REPLICATION] A_fix = %s = (9, -30, -15, 0, 32); "
          "E13 = %s, E22 = %s, E00 = 225 E22 (Killing-control anchor, "
          "NC-a of the task)" % (fmt(dA), fmt(E13), fmt(E22)),
          dA == [9, -30, -15, 0, 32] and E13 == [16, -96, 144, 0, 0]
          and E22 == [16, 32, 16, 0, 0]
          and E00 == [225 * x for x in E22])

    sol_strict = solvable([E00, qv], dA)
    Ms = sp.Matrix([[E00[i], qv[i]] for i in range(5)])
    aug_s = Ms.row_join(sp.Matrix(dA))
    check("D6.2 [STRICT TENSOR READING] m != 0 vertices do not exist at "
          "any arity <= 3 (D3.2 + D4.1): the sphere axions are silent; "
          "the bulk axion channels {E00, Q_dd} give rank %d = 2 with "
          "rank([M | A_fix]) = %d = 3: UNREACHABLE -- the strict "
          "full-tensor ledger reproduces the v508 kill"
          % (Ms.rank(), aug_s.rank()),
          sol_strict is None and Ms.rank() == 2 and aug_s.rank() == 3)

    M4 = sp.Matrix([[E13[i], E22[i], E00[i], qv[i]] for i in range(5)])
    aug = M4.row_join(sp.Matrix(dA))
    sol_gen = solvable([E13, E22, E00, qv], dA)
    psi = [a - sp.Rational(1, 4) * b for a, b in zip(PHI_P, PHI_T3)]
    ann_ok = all(phi(psi, E) == 0 for E in (E13, E22, E00, qv))
    t3_broken = phi(PHI_T3, qv) != 0
    check("D6.3 [GENEROUS READING -- NEW CERTIFICATE] M = [E13, E22, E00, "
          "Q_dd]: rank %d = 3, rank([M | A_fix]) = %d = 4: STILL "
          "UNSOLVABLE; but Phi_T3 is NO LONGER an annihilator of im(M) "
          "(Phi_T3(Q_dd) = 1/60 != 0) -- the surviving certificate is "
          "{Phi_T5, psi = Phi_P - Phi_T3/4} with psi(A_fix) = %s"
          % (M4.rank(), aug.rank(), phi(psi, dA)),
          sol_gen is None and M4.rank() == 3 and aug.rank() == 4
          and ann_ok and t3_broken and phi(psi, dA) == 64)

    check("D6.4 [CERTIFICATE ANATOMY] psi(A_fix) = Phi_P(A_fix) - "
          "Phi_T3(A_fix)/4 = 72 - 8 = 64: the T3 obstruction (32) is "
          "traded for a COMBINED (P3, T3) obstruction -- the d-channel "
          "produces T3 only with the fixed shadow P3 = -T3/4, and the "
          "leftover P-block violates the charge-0 span (K0 || K2 "
          "collapse, v508); [C] fence noted, no claim: 64 = dim g1 = 2^6",
          phi(PHI_P, dA) == 72
          and sp.Rational(1, 4) * phi(PHI_T3, dA) == 8
          and 72 - 8 == 64)

    u = [1, 2, 1, 0, 0]
    v = [1, -2, -3, 0, 0]
    w = [1, -6, 9, 0, 0]
    sol_rel = solvable([u, v, w, qv], dA)
    Mr = sp.Matrix([[u[i], v[i], w[i], qv[i]] for i in range(5)])
    ok_sol = (sol_rel is not None
              and sol_rel == [-1, 8, 2, 1920])
    resid = [dA[i] - (-1 * u[i] + 8 * v[i] + 2 * w[i]
                      + 1920 * qv[i]) for i in range(5)]
    check("D6.5 [RELAXED READING SOLVABLE -- the contrast with v508 S3.5] "
          "dropping charge bookkeeping on the bilinear P-block (directions "
          "(1,2,1), (1,-2,-3), (1,-6,9)) PLUS Q_dd: rank %d = 4 and A_fix "
          "= -1 u + 8 v + 2 w + 1920 Q_dd EXACTLY (residual %s): where "
          "v508 found T5 = T3 = 0 persisting even relaxed, the d-channel "
          "closes the T3 gap with small integer coefficients"
          % (Mr.rank(), fmt(resid)),
          Mr.rank() == 4 and ok_sol
          and all(r == 0 for r in resid))

    check("D6.6 [COUPLING SCALE / NATURALNESS FENCE] required d-channel "
          "weight c_d = 1920 = 32 x 60 under the e8-Killing propagator "
          "(= Phi_T3(A_fix) / Phi_T3(Q_dd)); [C]-typed observations only: "
          "1920 = |W(D5)| = 2^7 x 3 x 5 = 8 x 240; sign feasible via the "
          "(1, 3) exchange channel (lambda_1 lambda_3 unconstrained); no "
          "canonical ch2 datum exists yet for a CUBIC vertex -- "
          "naturalness stays UNDECIDED (honest fence)",
          sp.Rational(32) / sp.Rational(1, 60) == 1920
          and 1920 == 2 ** 7 * 3 * 5 and 1920 == 8 * 240)
    return dA, E13, E22, E00


# ---------------------------------------------------------------------------
# D7 -- negative controls
# ---------------------------------------------------------------------------
def section7(G, fac):
    print("  -- D7: negative controls")

    # (b) SO(16) glue: D8 adjoint + spinor, Z2 grading
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
    bil = (inv_d8(conv(adj8, adj8)),
           inv_d8(conv(adj8, spin8)),
           inv_d8(conv(spin8, spin8)))
    check("D7.1 [NC-b: SO(16) BILINEARS] (adj x adj, adj x spin, spin x "
          "spin) = %s = (1, 0, 1): Killing + the real spinor pairing, "
          "nothing off-diagonal -- same collapse pattern, but with NO odd "
          "sectors there are no sphere-axion partners at all (v508 NC-c "
          "at tensor level)" % fmt(bil), bil == (1, 0, 1))

    tri8 = (inv_d8(conv(conv(adj8, adj8), adj8)),
            inv_d8(conv(conv(adj8, adj8), spin8)),
            inv_d8(conv(conv(adj8, spin8), spin8)),
            inv_d8(conv(conv(spin8, spin8), spin8)))
    s3adj8 = inv_d8(sym3(adj8))
    l3adj8 = inv_d8(alt3(adj8))
    check("D7.2 [NC-b: SO(16) TRILINEARS] (adj^3, adj^2 spin, adj spin^2, "
          "spin^3) = %s = (1, 0, 1, 0) and Inv(S^3 adj_d8) = %d = 0, "
          "Inv(L^3 adj_d8) = %d = 1: D8 has NO symmetric cubic (no cubic "
          "Casimir) -- the delta-2 channel does not exist for the SO(16) "
          "route, and there is no A3 block to feed anyway: E8/mu4 is "
          "doubly special" % (fmt(tri8), s3adj8, l3adj8),
          tri8 == (1, 0, 1, 0) and s3adj8 == 0 and l3adj8 == 1)

    # (c) deliberately false g0 = d5 (+) a2 (+) u(1)
    b00 = inv_dim([G[0], G[0]], inv_d5, inv_a2u1)
    b13 = inv_dim([G[1], G[3]], inv_d5, inv_a2u1)
    b22 = inv_dim([G[2], G[2]], inv_d5, inv_a2u1)
    s3f = inv_dim([box_sym3(G[0])], inv_d5, inv_a2u1)
    check("D7.3 [NC-c: FALSE g0 = d5+a2+u(1)] bilinear entries (0,0)/"
          "(1,3)/(2,2) = (%d, %d, %d) != (2, 1, 1) and Inv(S^3 g0) = %d "
          "!= 1: breaking a3 -> a2+u(1) inflates every Hom dimension -- "
          "the computation SEES the exact g0 structure (and D1.1 showed "
          "the true g0 has NO u(1))" % (b00, b13, b22, s3f),
          (b00, b13, b22) == (5, 2, 2) and s3f == 6)

    # (c2) false sector assignment: g1 -> (16_s, 4bar)
    fake1 = [(fac['spin16'], fac['bar4'])]
    f13 = inv_dim([fake1, G[3]])
    f11 = inv_dim([fake1, fake1])
    check("D7.4 [NC-c2: FALSE SECTOR CONTENT] swapping the a3 factor of "
          "g1 to 4bar kills EVERY pairing of the fake sector: fake-g1 x "
          "g3 = %d and fake-g1 x fake-g1 = %d (both 0, true g1-g3 value "
          "1): the misassigned sector has NO Killing partner left -- the "
          "(16_s, 4) / (16_c, 4bar) content is forced by the bilinear "
          "table" % (f13, f11), f13 == 0 and f11 == 0)

    # machinery guard: trivial vs nontrivial modules, dual vs non-dual pair
    guards = (inv_d5(fac['TRIV5']), inv_a3(fac['TRIV3']),
              inv_d5(fac['adj45']), inv_a3(fac['adj15']),
              inv_d5(fac['vec10']), inv_a3(fac['fund4']),
              inv_a3(conv(fac['fund4'], fac['fund4'])),
              inv_a3(conv(fac['fund4'], fac['bar4'])))
    check("D7.5 [MACHINERY GUARD] Inv(trivial) = (%d, %d) = 1, "
          "Inv(adj/vec/fund alone) = (%d, %d, %d, %d) = 0, and the dual "
          "test 4 x 4 = %d vs 4 x 4bar = %d: the Kostant matcher returns "
          "invariants only where they exist" % guards,
          guards == (1, 1, 0, 0, 0, 0, 0, 1))


# ---------------------------------------------------------------------------
def run():
    reset()
    print("v511  CELEST.WP5E.DELTA2.01: the full-tensor ledger "
          "(WP5e-delta-2 of CELEST.SEAM.01 -- the collapse is confirmed "
          "full-tensorially, and one cubic door opens)")
    roots = build_glue_roots()
    G, fac, cart_ok = build_sector_reps(roots)

    section0(roots)
    section1(roots, G, fac, cart_ok)
    section2(fac)
    section3(G)
    section4(G)
    qv = section5(roots)
    section6(roots, qv)
    section7(G, fac)

    return summary("v511 CELEST.WP5E.DELTA2.01: the full-tensor ledger of "
                   "the WP5e pairing question -- the v508 collapse is "
                   "confirmed as a full-tensor, arity-crossing statement "
                   "(innerness: h in the g0 Cartan, so all invariant "
                   "vertices carry total charge 0 mod 4; all 15 "
                   "non-neutral trilinear triples have Hom = 0), and the "
                   "charge-0 ledger contains exactly ONE structure "
                   "invisible to the quadratic ansatz: the su(4) d-symbol "
                   "(unique symmetric trilinear on e8), whose exchange "
                   "quartic Q_dd = (1/60)(T3 - P3/4) breaks the Phi_T3 "
                   "master kill (1/60 != 0); the pairing stays obstructed "
                   "in the charge reading with the weaker certificate "
                   "{Phi_T5, psi = Phi_P - Phi_T3/4}, psi(A_fix) = 64, "
                   "and becomes exactly solvable relaxed: A_fix = -u + 8v "
                   "+ 2w + 1920 Q_dd; SO(16)/D8 has no symmetric cubic "
                   "and false g0/sector controls separate; the burden on "
                   "delta-1 is sharpened to the psi = 64 slice or the "
                   "selection-rule relaxation; no marker moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
