"""v508 -- CELEST.WP5E.GAMMA.01: WP5e-gamma of the research contract
CELEST.SEAM.01 -- "the sphere-axion pairing check", an honest, rigid
NEGATIVE result (v505 style).  Question: can the three twisted sphere
axions eta_m (m = 1, 2, 3; Coxeter eigencharacters {i, -1, -i} on
H^2(ALE), v505 S5.8) cancel the rigid 32 T3 residual of the Atiyah-Bott
anomaly ledger (v505 S3.7: A_fix = Q^{(1)}/2 + Q^{(2)}/4 + Q^{(3)}/2 =
9 P1 - 30 P2 - 15 P3 + 32 T3) by Green-Schwarz-type EXCHANGE with
sector-compatible quadratic vertices?  Answer: NO, with a certificate.
Exact linear algebra throughout (sympy / Fraction, no floats).

[E] S1. VERTEX-SPACE THEOREM (the structural backbone): the space of
      W(D5) x W(A3)-invariant polynomials on the 8-dim glue Cartan is
      computed EXACTLY by nullspace arithmetic over the Weyl generators
      across all bidegrees: quadratics dim 2 = span{s5, s3} (bidegree
      dims (1, 0, 1)); quartics dim 5 = span{P1, P2, P3, T5, T3}
      (bidegree dims (2, 0, 1, 0, 2)) -- the vertex basis is COMPLETE.
      PRODUCT THEOREM (the master kill): (a s5 + b s3)(c s5 + d s3) =
      ac P1 + (ad+bc) P2 + bd P3 identically -- the product of ANY two
      invariant quadratics has identically ZERO T5- and T3-content, so
      EVERY exchange image (any number of axions, any selection rule,
      any couplings) is annihilated by Phi_T3, while Phi_T3(A_fix) =
      32 != 0: the pairing is decided before enumeration.
[E] S2. SELECTION-RULE ENUMERATION (Z4 charge m + j + j' = 0 mod 4):
      the strict two-index reading COLLAPSES -- the class bilinears
      C_{j,j'} = sum_{alpha+beta=0} <alpha,x><beta,x> are nonzero ONLY
      for j' = -j (C_{j,-j} = -K_j), so the rule forces m = 0: the
      sphere axions have NO invariant bilinear Cartan vertex at all
      (16 raw triples, 4 nonzero, all m = 0).  Twist-insertion reading
      (the generous route): eta_1 <-> K^{(3)}, eta_2 <-> K^{(2)},
      eta_3 <-> K^{(1)}, eta_0 <-> K^{(0)}; exchange channels E13 =
      K^{(3)}K^{(1)} = (16, -96, 144, 0, 0), E22 = (K^{(2)})^2 =
      (16, 32, 16, 0, 0), bulk E00 = 225 E22.  SIDE DISCOVERY:
      K^{(0)} = -15 K^{(2)} -- the two even-sector quadratics are
      PARALLEL; this collapse drives the Phi_P obstruction below.
[E] S3. UNSOLVABILITY WITH CERTIFICATE (the core result): exchange
      matrix M is 5 x 2, rank 2, kernel 0 (a solution, if it existed,
      would be unique/rigid); rank([M | A_fix]) = 3 > 2: UNSOLVABLE.
      Annihilator certificate: im(M) is annihilated by Phi_T5, Phi_T3,
      Phi_P = 3[P1] - [P2] - [P3], with values (0, 32, 72) on A_fix =
      (9, -30, -15, 0, 32) -- TWO independent obstructions: 32 T3
      (structural, rule-independent, the S1 product theorem) and
      Phi_P = 72 (selection-rule-driven: even the factorised part
      9 P1 - 30 P2 - 15 P3 is unreachable through charge-0 channels,
      because K^{(0)} || K^{(2)} collapses the charge-0 product span to
      2 dims); Phi_P(Q^{(0)}) = 0 (the bulk Okubo square stays inside
      the reachable slice: the v505 sector-0 mechanism is undisturbed);
      ker M = 0 forces the unique non-disturbing coupling c = 0 -- the
      sphere axions are RIGIDLY SILENT in the exchange ansatz.  Relaxed
      control: dropping charge conservation makes the P-block fully
      reachable (rank 3, det -64) but T5 = T3 = 0 persists.
[E] S4. NATURALNESS RESOLUTION: ch2-natural couplings (f(1)f(3),
      f(2)^2) = (9/64, 1/4) give image (25/4, -11/2, 97/4, 0, 0) and
      AB-weight couplings (1/2, 1/4) give (12, -40, 76, 0, 0) -- BOTH
      have certificate values (0, 0) instead of the required (32, 72):
      the failure is scale- and coupling-INDEPENDENT (no "unnatural
      factor" -- the ansatz space misses the target identically).
[E] S5. NEGATIVE CONTROLS: (a) invariant axion only = v505 S3.9
      replicated + sharpened (A_fix not in span{(K^{(0)})^2});
      (b) flipped rule m + j - j': the Phi_T3 kill is flip-invariant,
      Phi_P is rule-dependent (the P-part becomes reachable, 32 T3
      stays dead); (c) SO(16) glue: odd classes EMPTY (no sphere
      partners) and the AB sum (15, -18, -15, -4, 40) does not even
      cancel T5 -- E8 is doubly special; (d) D8 native: quartic
      16 T8 + 12 s8^2, no A3 block, no T3 structure -- the pairing
      question cannot even be posed.
[C] Number fences (typed [C] only, look-elsewhere discipline):
      32 = (h,h) + (h',h') = 20 + 12; 72 = 2 * 36 = 2 lambda~^2_e8.
[O] SHARPENED O-FENCE (what stays open after gamma): the exchange
      sub-branch is DEAD; the 32 T3 residual MUST be carried by twisted
      BCOV contact terms -- binary criterion WP5e-delta-1: the one-loop
      coefficient on C^2/Z4 must come out exactly (9, -30, -15, 0, 32),
      COMPUTED (orbifold elliptic-genus / twisted-character arithmetic),
      not fitted; named escape WP5e-delta-2: the full-tensor ledger with
      non-Cartan external legs (the S2 collapse is a Cartan-restricted
      statement); plus WP5e-epsilon-1 (the O(-2) bulk-axion
      construction, lambda~ = 6) and WP5e-epsilon-2 (CPS level-from-
      flux, k = 1).  The slot bijection (v505 S5.8) is UNTOUCHED; the
      preregistered level-kill still does NOT fire; SEAM.EQUIV.01
      stays [O]; NO marker moves anywhere.

Status: [E] exact vertex-space/selection/certificate arithmetic (sympy
+ Fraction); [C] the number fences above; [O] the twisted BCOV contact
terms (delta-1) and the full-tensor ledger (delta-2).  Python;
Wolfram-mirrored (vertex-space dims 2/5, K^{(0)} = -15 K^{(2)}, product
theorem, rank-3 certificate (0, 32, 72), SO(16) AB sum, D8 quartic),
counted per GATE.WOLFRAM.02.  Discovery provenance: experiments/
tfpt-discovery/celestial_seam_wp5e_gamma_sphere_axion_pairing_probe.py
(2026-07-21, 27/27)."""
from fractions import Fraction as F
from itertools import combinations, product

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

MU4 = N_fam + 1             # 4 = |mu4|, the seam clock order
RANK = rankE8               # 8
H_VEE = 2 * N_fam * g_car   # 30 = |Z2| N_fam g_car (v495 anchor decomposition)
HALF = F(1, 2)


def fmt(xs):
    return "(" + ", ".join(str(x) for x in xs) + ")"


# ---------------------------------------------------------------------------
# E8 roots in D5 (+) A3 glue coordinates (v128/v492/v502/v505 construction)
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
# exact polynomial machinery on the D5 (+) A3 Cartan (8 parameters)
# ---------------------------------------------------------------------------
X5 = sp.symbols('x1:6')                      # D5 Cartan x1..x5
Y3 = sp.symbols('y1:4')                      # A3 Cartan (sum-zero coords)
Y4 = (*Y3, -sum(Y3))                         # y4 = -(y1+y2+y3)
ALLV = (*X5, *Y3)

S5 = sp.expand(sum(v ** 2 for v in X5))
S3 = sp.expand(sum(v ** 2 for v in Y4))
P1 = sp.expand(S5 ** 2)
P2 = sp.expand(S5 * S3)
P3 = sp.expand(S3 ** 2)
T5 = sp.expand(sum(v ** 4 for v in X5))
T3 = sp.expand(sum(v ** 4 for v in Y4))
BASIS4 = [("P1", P1), ("P2", P2), ("P3", P3), ("T5", T5), ("T3", T3)]

# Weyl generators as substitution maps on the 8 reduced coordinates:
# W(D5) = S5 permutations + one double sign flip; W(A3) = S4 permutations
# of (y1, y2, y3, y4) with y4 = -(y1+y2+y3) eliminated.
WEYL_D5 = [
    {X5[0]: X5[1], X5[1]: X5[0]},
    {X5[1]: X5[2], X5[2]: X5[1]},
    {X5[2]: X5[3], X5[3]: X5[2]},
    {X5[3]: X5[4], X5[4]: X5[3]},
    {X5[3]: -X5[4], X5[4]: -X5[3]},
]
WEYL_A3 = [
    {Y3[0]: Y3[1], Y3[1]: Y3[0]},
    {Y3[1]: Y3[2], Y3[2]: Y3[1]},
    {Y3[2]: -Y3[0] - Y3[1] - Y3[2]},
]
WEYL_ALL = WEYL_D5 + WEYL_A3


def lin_form(alpha):
    """<alpha, x> as a sympy linear form (A3 block in sum-zero coordinates)."""
    e = sum(sp.Rational(alpha[i].numerator, alpha[i].denominator) * X5[i]
            for i in range(5))
    e += sum(sp.Rational(alpha[5 + i].numerator, alpha[5 + i].denominator)
             * Y4[i] for i in range(4))
    return sp.expand(e)


def poly_dict(expr):
    return sp.Poly(sp.expand(expr), *ALLV, domain='QQ').as_dict()


def decompose(target, basis_exprs):
    """Exact coefficients of target in span(basis) or None if not in span."""
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


def in_span(target, basis_exprs):
    return decompose(target, basis_exprs) is not None


def power_sums_by_class(roots):
    """K_m, Q_m = sum over class-m roots of <alpha,x>^2 resp. ^4 (exact)."""
    K = {m: sp.Poly(0, *ALLV, domain='QQ') for m in range(4)}
    Q = {m: sp.Poly(0, *ALLV, domain='QQ') for m in range(4)}
    for alpha, c in roots.items():
        p = sp.Poly(lin_form(alpha), *ALLV, domain='QQ')
        p2 = p ** 2
        K[c] = K[c] + p2
        Q[c] = Q[c] + p2 ** 2
    return ({m: K[m].as_expr() for m in range(4)},
            {m: Q[m].as_expr() for m in range(4)})


def compositions(total, parts):
    """All tuples of `parts` nonneg ints summing to `total`."""
    if parts == 1:
        yield (total,)
        return
    for head in range(total + 1):
        for tail in compositions(total - head, parts - 1):
            yield (head,) + tail


def monoms_bidegree(dx, dy):
    """Exponent tuples on ALLV with x-degree dx and y-degree dy."""
    return [xc + yc for xc in compositions(dx, 5)
            for yc in compositions(dy, 3)]


def mono_expr(t):
    e = sp.Integer(1)
    for v, p in zip(ALLV, t):
        e *= v ** p
    return e


def invariant_dim(monom_tuples, gens):
    """dim of the invariant subspace of span(monomials) under gens (exact)."""
    idx = {t: i for i, t in enumerate(monom_tuples)}
    n = len(monom_tuples)
    blocks = []
    for g in gens:
        A = sp.zeros(n, n)
        for i, t in enumerate(monom_tuples):
            d = sp.Poly(sp.expand(mono_expr(t).subs(g, simultaneous=True)),
                        *ALLV, domain='QQ').as_dict()
            for expo, coef in d.items():
                A[idx[expo], i] += coef
        blocks.append(A - sp.eye(n))
    M = sp.Matrix.vstack(*blocks)
    return n - M.rank()


def vec5(expr):
    """Exact coefficient vector of a quartic in the (P1,P2,P3,T5,T3) basis."""
    c = decompose(expr, [b for _, b in BASIS4])
    assert c is not None, "quartic not in the invariant 5-basis"
    return [sp.Rational(x) for x in c]


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


PHI_P = [3, -1, -1, 0, 0]    # 3[P1] - [P2] - [P3]: charge-0 annihilator
PHI_T5 = [0, 0, 0, 1, 0]
PHI_T3 = [0, 0, 0, 0, 1]


def phi(functional, vec):
    return sum(sp.Rational(a) * sp.Rational(b)
               for a, b in zip(functional, vec))


# ---------------------------------------------------------------------------
# S0 -- baseline replication (v505 anchors this module builds on)
# ---------------------------------------------------------------------------
def section0(roots, K, Q):
    print("  -- S0: v505 baseline replication (roots, K/Q ledger, residual)")
    I = sp.I

    counts = [sum(1 for c in roots.values() if c == m) for m in range(4)]
    norm_ok = all(sum(x * x for x in r) == 2 for r in roots)
    check("S0.1 [ROOTS] 240 roots, all norm 2, class split %s = "
          "(52, 64, 60, 64) (v492/v505 replication)" % fmt(counts),
          len(roots) == 240 and norm_ok and counts == [52, 64, 60, 64])

    Ktw = {j: sp.expand(sum(I ** (j * m) * K[m] for m in range(4)))
           for j in range(4)}
    check("S0.2 [TWISTED QUADRATICS] K^{(0)} = 60(s5+s3), K^{(1)} = K^{(3)} "
          "= 4 s5 - 12 s3, K^{(2)} = -4(s5+s3) (v505 S2.2 replication); "
          "NOTE K^{(0)} = -15 K^{(2)}: the two even-sector quadratics are "
          "PARALLEL -- this collapse drives S3",
          sp.expand(Ktw[0] - 60 * (S5 + S3)) == 0
          and sp.expand(Ktw[1] - (4 * S5 - 12 * S3)) == 0
          and sp.expand(Ktw[3] - Ktw[1]) == 0
          and sp.expand(Ktw[2] + 4 * (S5 + S3)) == 0
          and sp.expand(Ktw[0] + 15 * Ktw[2]) == 0)

    Qtw = {j: sp.expand(sum(I ** (j * m) * Q[m] for m in range(4)))
           for j in range(4)}
    Afix = sp.expand(Qtw[1] / 2 + Qtw[2] / 4 + Qtw[3] / 2)
    dA = vec5(Afix)
    print("     A_fix = Q^(1)/2 + Q^(2)/4 + Q^(3)/2 = %s in "
          "(P1, P2, P3, T5, T3)" % fmt(dA))
    check("S0.3 [THE TARGET] AB residual A_fix = (9, -30, -15, 0, 32): D5 "
          "quartic cancelled, A3 quartic 32 T3 rigid (v505 S3.7 "
          "replication) -- THIS is what the sphere axions must produce",
          dA == [9, -30, -15, 0, 32])

    dens = [sp.expand((1 - I ** (-j)) * (1 - I ** j)) for j in (1, 2, 3)]
    fvals = [sp.nsimplify(sp.expand(
        sp.Rational(1, 4) * sum((I ** (j * m) - 1) / dens[j - 1]
                                for j in (1, 2, 3)))) for m in range(4)]
    check("S0.4 [ch2 DATA] f(m) = (1/4) sum_j (i^{jm}-1)/det_j = %s = "
          "(0, -3/8, -1/2, -3/8) = ch2(T_m) (v505 S4.3 index bridge): the "
          "geometric coupling data for the naturalness anchor" % fmt(fvals),
          fvals == [0, sp.Rational(-3, 8), sp.Rational(-1, 2),
                    sp.Rational(-3, 8)])

    A = sp.Matrix([[0, 0, -1], [1, 0, -1], [0, 1, -1]])
    xs = sp.symbols('x')
    eigs = set(sp.roots(A.charpoly(xs).as_expr(), xs).keys())
    check("S0.5 [SLOT BIJECTION] the three H2(ALE) classes carry Coxeter "
          "eigencharacters {i, -1, -i} = the three twisted sectors "
          "(v505 S5.8): the axions eta_1, eta_2, eta_3 carry Z4 charges "
          "1, 2, 3 -- the charge assignment used below",
          eigs == {sp.I, -1, -sp.I}
          and (A - sp.eye(3)).det() == -4)
    return Ktw, Qtw, Afix, dA


# ---------------------------------------------------------------------------
# S1 -- the vertex-space theorem (exact Weyl-invariant arithmetic)
# ---------------------------------------------------------------------------
def section1(Ktw):
    print("  -- S1: the invariant vertex space and the master kill")

    d20 = invariant_dim(monoms_bidegree(2, 0), WEYL_D5)
    d11 = invariant_dim(monoms_bidegree(1, 1), WEYL_ALL)
    d02 = invariant_dim(monoms_bidegree(0, 2), WEYL_A3)
    kdec = [decompose(Ktw[j], [S5, S3]) is not None for j in range(4)]
    check("S1.1 [INVARIANT QUADRATICS] bidegree dims (x^2, xy, y^2) = "
          "(%d, %d, %d): the W(D5) x W(A3)-invariant quadratics on the "
          "8-dim Cartan are EXACTLY span{s5, s3} (dim 2, Schur on each "
          "simple block); all sector quadratics K^{(j)} lie inside -- the "
          "COMPLETE gauge-invariant quadratic vertex basis is 2-dim"
          % (d20, d11, d02),
          (d20, d11, d02) == (1, 0, 1) and all(kdec))

    d40 = invariant_dim(monoms_bidegree(4, 0), WEYL_D5)
    d31 = invariant_dim(monoms_bidegree(3, 1), WEYL_ALL)
    d22 = invariant_dim(monoms_bidegree(2, 2), WEYL_ALL)
    d13 = invariant_dim(monoms_bidegree(1, 3), WEYL_ALL)
    d04 = invariant_dim(monoms_bidegree(0, 4), WEYL_A3)
    basis_rank = sp.Matrix([[poly_dict(b).get(m, 0)
                             for _, b in BASIS4]
                            for m in sorted(set().union(
                                *[poly_dict(b).keys()
                                  for _, b in BASIS4]))]).rank()
    check("S1.2 [INVARIANT QUARTICS] bidegree dims (4,0)/(3,1)/(2,2)/(1,3)/"
          "(0,4) = (%d, %d, %d, %d, %d), total %d = 5; the exhibited basis "
          "{P1, P2, P3, T5, T3} has rank %d = 5: COMPLETE -- the anomaly "
          "bookkeeping space is exactly 5-dim"
          % (d40, d31, d22, d13, d04, d40 + d31 + d22 + d13 + d04,
             basis_rank),
          (d40, d31, d22, d13, d04) == (2, 0, 1, 0, 2) and basis_rank == 5)

    a, b, c, d = sp.symbols('a b c d')
    prod = sp.expand((a * S5 + b * S3) * (c * S5 + d * S3)
                     - (a * c * P1 + (a * d + b * c) * P2 + b * d * P3))
    check("S1.3 [PRODUCT THEOREM] (a s5 + b s3)(c s5 + d s3) = ac P1 + "
          "(ad+bc) P2 + bd P3 IDENTICALLY: the product of any two "
          "invariant quadratics has ZERO T5- and T3-content -- scalar "
          "exchange with gauge-invariant quadratic vertices lives entirely "
          "in span{P1, P2, P3}",
          prod == 0)

    check("S1.4 [MASTER KILL, rule-independent] Phi_T3 annihilates EVERY "
          "exchange image (S1.3) but Phi_T3(A_fix) = 32 != 0: no scalar-"
          "exchange mechanism with invariant quadratic vertices -- ANY "
          "number of axions, ANY selection rule, ANY couplings -- can "
          "cancel the 32 T3 residual; the pairing question is decided "
          "before enumeration, the enumeration below sharpens WHERE it "
          "fails", True)


# ---------------------------------------------------------------------------
# S2 -- selection-rule enumeration (both readings, exact)
# ---------------------------------------------------------------------------
def section2(roots, K, Ktw):
    print("  -- S2: Z4 selection rule m + j + j' = 0 mod 4 -- enumeration")

    cls = dict(roots)
    neg_ok = all(cls[tuple(-x for x in r)] == (4 - c) % 4 if c != 0
                 else cls[tuple(-x for x in r)] == 0
                 for r, c in roots.items())
    check("S2.1 [CHARGE OF -alpha] class(-alpha) = -class(alpha) mod 4 for "
          "all 240 roots: the Killing pairing g_j x g_{4-j} -> C is the "
          "only invariant bilinear pairing between class blocks", neg_ok)

    Cpair = {(j, jp): sp.Integer(0) for j in range(4) for jp in range(4)}
    for r, c in roots.items():
        cneg = cls[tuple(-x for x in r)]
        lf = lin_form(r)
        Cpair[(c, cneg)] = Cpair[(c, cneg)] + sp.expand(lf * (-lf))
    nonzero = sorted(k for k, v in Cpair.items() if sp.expand(v) != 0)
    diag_ok = all(sp.expand(Cpair[(j, (4 - j) % 4)] + K[j]) == 0
                  for j in range(4))
    raw = [(m, j, jp) for m in range(4) for j in range(4) for jp in range(4)
           if (m + j + jp) % 4 == 0]
    live = [(m, j, jp) for (m, j, jp) in raw if (j, jp) in nonzero]
    print("     raw rule-allowed triples (m; j, j'): %d; with nonzero "
          "bilinear V^{(j,j')}: %d -> %s"
          % (len(raw), len(live), fmt(live)))
    check("S2.2 [TWO-INDEX READING COLLAPSES] the class bilinears "
          "C_{j,j'} = sum_{alpha+beta=0} <alpha,x><beta,x> are nonzero "
          "ONLY for j' = -j (namely C_{j,-j} = -K_j); the rule m + j + j' "
          "= 0 then forces m = 0: of 16 raw triples only 4 survive, ALL "
          "with m = 0 -- under the strict two-index reading the sphere "
          "axions (m = 1, 2, 3) have NO invariant bilinear Cartan vertex "
          "at all (coupling-space collapse)",
          nonzero == [(0, 0), (1, 3), (2, 2), (3, 1)] and diag_ok
          and len(raw) == 16 and len(live) == 4
          and all(m == 0 for m, _, _ in live))

    allowed = [(m, (4 - m) % 4) for m in range(4)]
    tab = {m: decompose(Ktw[a], [S5, S3]) for m, a in allowed}
    print("     twist-insertion vertices eta_m K^{(a)}, a = -m mod 4 "
          "(coeffs in (s5, s3)):")
    for m, a in allowed:
        print("       m = %d -> a = %d: K^(%d) = %s" % (m, a, a,
                                                        fmt(tab[m])))
    check("S2.3 [TWIST-INSERTION READING] vertices eta_m tr(g^a X^2) = "
          "eta_m K^{(a)} with the rule m + a = 0 mod 4: allowed (m; a) = "
          "{(0;0), (1;3), (2;2), (3;1)} -- every axion couples through "
          "exactly ONE sector quadratic: eta_1 via K^{(3)} = (4, -12), "
          "eta_2 via K^{(2)} = (-4, -4), eta_3 via K^{(1)} = (4, -12), "
          "bulk eta_0 via K^{(0)} = (60, 60)",
          tab[1] == [4, -12] and tab[2] == [-4, -4]
          and tab[3] == [4, -12] and tab[0] == [60, 60])

    E13 = vec5(sp.expand(Ktw[3] * Ktw[1]))
    E22 = vec5(sp.expand(Ktw[2] ** 2))
    E00 = vec5(sp.expand(Ktw[0] ** 2))
    print("     exchange channels (m, 4-m), generated quartics:")
    print("       (1,3): E13 = %s" % fmt(E13))
    print("       (2,2): E22 = %s" % fmt(E22))
    print("       (0,0): E00 = %s (bulk, = 225 E22)" % fmt(E00))
    check("S2.4 [EXCHANGE CHANNELS] propagator <eta_m eta_{m'}> nonzero "
          "iff m + m' = 0 mod 4: sphere channels (1,3) and (2,2) generate "
          "E13 = K^{(3)}K^{(1)} = (16, -96, 144, 0, 0) and E22 = "
          "(K^{(2)})^2 = (16, 32, 16, 0, 0); the bulk channel E00 = "
          "(K^{(0)})^2 = 3600(1, 2, 1, 0, 0) = 225 E22 is PARALLEL to E22 "
          "(K^{(0)} || K^{(2)}): the total charge-0 product span is only "
          "2-dimensional",
          E13 == [16, -96, 144, 0, 0] and E22 == [16, 32, 16, 0, 0]
          and E00 == [3600, 7200, 3600, 0, 0]
          and [225 * x for x in E22] == E00)
    return E13, E22, E00


# ---------------------------------------------------------------------------
# S3 -- solvability of the pairing (the core result)
# ---------------------------------------------------------------------------
def section3(E13, E22, E00, dA, Qtw):
    print("  -- S3: exchange matrix, rank/kernel, solvability")

    M = sp.Matrix([[E13[i], E22[i]] for i in range(5)])
    Mb = sp.Matrix([[E13[i], E22[i], E00[i]] for i in range(5)])
    t = sp.Matrix([dA[i] for i in range(5)])
    ker = M.nullspace()
    check("S3.1 [MATRIX] sphere exchange matrix M: 5 x 2, rank %d = 2, "
          "kernel dim %d = 0 (a solution, if any, would be UNIQUE -- the "
          "ansatz is rigid); adding the bulk column keeps rank %d = 2 "
          "(parallelism E00 = 225 E22)"
          % (M.rank(), len(ker), Mb.rank()),
          M.rank() == 2 and len(ker) == 0 and Mb.rank() == 2)

    aug = M.row_join(t)
    sol = solvable([E13, E22], dA)
    solb = solvable([E13, E22, E00], dA)
    ann_ok = all(phi(f, E) == 0 for f in (PHI_P, PHI_T5, PHI_T3)
                 for E in (E13, E22, E00))
    vals = [phi(f, dA) for f in (PHI_T5, PHI_T3, PHI_P)]
    print("     certificate values on A_fix: Phi_T5 = %s, Phi_T3 = %s, "
          "Phi_P = %s" % tuple(vals))
    check("S3.2 [UNSOLVABLE -- THE CORE RESULT] rank([M | A_fix]) = %d > 2: "
          "NO coupling assignment of the three sphere axions (nor adding "
          "the bulk axion) cancels the residual; obstruction certificate: "
          "Phi_T5, Phi_T3, Phi_P = 3[P1]-[P2]-[P3] all annihilate im(M), "
          "with values (0, 32, 72) on A_fix -- the unreachable directions "
          "are EXACTLY the A3 quartic (32 T3) and the Phi_P = 72 slice of "
          "the factorised part" % aug.rank(),
          aug.rank() == 3 and sol is None and solb is None and ann_ok
          and vals == [0, 32, 72])

    solP = solvable([E13[:3] + [0, 0], E22[:3] + [0, 0]],
                    dA[:3] + [0, 0])
    check("S3.3 [TWO-LAYER OBSTRUCTION] even the FACTORISED part "
          "(9, -30, -15, 0, 0) alone is unreachable through the charge-0 "
          "channels (Phi_P = 72 != 0; root cause: K^{(0)} || K^{(2)} "
          "collapses the charge-0 span to 2 dims): obstruction 1 = 32 T3 "
          "(structural, S1.4), obstruction 2 = Phi_P = 72 (selection-rule-"
          "driven, see NC-b for the contrast)",
          solP is None and phi(PHI_P, dA) == 72)

    q0 = vec5(Qtw[0])
    homo = solvable([E13, E22], [0, 0, 0, 0, 0])
    check("S3.4 [RIGID SILENCE + SECTOR-0 SAFETY] ker M = 0: the only "
          "coupling choice adding NO new uncancelled quartic is c = 0 -- "
          "since the target is unreachable, the sphere axions are FORCED "
          "SILENT in the exchange ansatz; consistency: Phi_P(Q^{(0)}) = "
          "%s = 0 (the bulk Okubo square 36<x,x>^2 = (36, 72, 36) lies in "
          "the Phi_P = 0 slice: the v505 sector-0 mechanism is not "
          "disturbed at c = 0)" % phi(PHI_P, q0),
          homo == [0, 0] and phi(PHI_P, q0) == 0
          and q0 == [36, 72, 36, 0, 0])

    u = [1, 2, 1, 0, 0]
    v = [1, -2, -3, 0, 0]
    w = [1, -6, 9, 0, 0]
    det3 = sp.Matrix([u[:3], v[:3], w[:3]]).det()
    sol_relaxed = solvable([u, v, w], dA[:3] + [0, 0])
    still_dead = solvable([u, v, w], dA)
    check("S3.5 [RELAXED CONTROL: DROP CHARGE CONSERVATION] allowing ALL "
          "graded products K^{(a)}K^{(b)} gives the P-directions "
          "{(1,2,1), (1,-2,-3), (1,-6,9)} with det %s = -64 != 0: the "
          "factorised part becomes fully reachable -- but T5 = T3 = 0 "
          "identically persists and A_fix stays unreachable: the DEEP "
          "obstruction is 32 T3, the Phi_P block is what the selection "
          "rule adds on top" % det3,
          det3 == -64 and sol_relaxed is not None and still_dead is None)


# ---------------------------------------------------------------------------
# S4 -- naturalness anchors (ch2 data, Coxeter characters)
# ---------------------------------------------------------------------------
def section4(E13, E22, dA):
    print("  -- S4: naturalness anchors -- what natural couplings "
          "would produce")

    f1, f2, f3 = (sp.Rational(-3, 8), sp.Rational(-1, 2),
                  sp.Rational(-3, 8))
    img_f = [f1 * f3 * sp.Rational(E13[i]) + f2 ** 2 * sp.Rational(E22[i])
             for i in range(5)]
    print("     ch2-natural couplings (c13, c22) = (f(1)f(3), f(2)^2) = "
          "(9/64, 1/4): image = %s" % fmt(img_f))
    check("S4.1 [ch2-NATURAL COUPLINGS] c13 = f(1)f(3) = 9/64, c22 = "
          "f(2)^2 = 1/4 give image (25/4, -11/2, 97/4, 0, 0); certificate "
          "values (Phi_T3, Phi_P) = (0, 0) vs required (32, 72): the "
          "mismatch is INDEPENDENT of any overall scale kappa -- no "
          "normalisation of the geometric data rescues the exchange "
          "ansatz",
          img_f == [sp.Rational(25, 4), sp.Rational(-11, 2),
                    sp.Rational(97, 4), 0, 0]
          and phi(PHI_T3, img_f) == 0 and phi(PHI_P, img_f) == 0)

    img_ab = [sp.Rational(1, 2) * sp.Rational(E13[i])
              + sp.Rational(1, 4) * sp.Rational(E22[i]) for i in range(5)]
    print("     AB-weight couplings (c13, c22) = (1/det_1, 1/det_2) = "
          "(1/2, 1/4): image = %s" % fmt(img_ab))
    check("S4.2 [AB-WEIGHT COUPLINGS] c13 = 1/2, c22 = 1/4 (the Atiyah-"
          "Bott weights themselves) give image (12, -40, 76, 0, 0): same "
          "certificate mismatch (0, 0) vs (32, 72) -- the naturalness "
          "question DISSOLVES: the ansatz space misses the target "
          "identically, not by an unnatural factor",
          img_ab == [12, -40, 76, 0, 0]
          and phi(PHI_T3, img_ab) == 0 and phi(PHI_P, img_ab) == 0)

    hh = 5 * 4          # (h,h) = 20, h = (2,2,2,2,2;0^4)
    hph = 12            # (h',h') with h' the A3-side inner element (v505)
    check("S4.3 [NUMEROLOGY FENCES, typed [C] only] 32 = (h,h) + (h',h') "
          "= 20 + 12 (v505 S3.7) and Phi_P(A_fix) = 72 = 2 * 36 = "
          "2 lambda~^2_e8 (v495 Okubo coefficient): arithmetic holds, "
          "flagged as coincidence-level observations -- NO claim is "
          "attached (look-elsewhere discipline)",
          hh + hph == 32 and 2 * 36 == 72 and phi(PHI_P, dA) == 72)


# ---------------------------------------------------------------------------
# S5 -- negative controls
# ---------------------------------------------------------------------------
def section5(K, Q, Ktw, Qtw, dA):
    print("  -- S5: negative controls")

    ok_span0 = in_span(Qtw[0], [sp.expand(Ktw[0] ** 2),
                                sp.expand(Ktw[1] * Ktw[3]),
                                sp.expand(Ktw[2] ** 2)])
    span1 = [sp.expand(Ktw[0] * Ktw[1]), sp.expand(Ktw[2] * Ktw[3])]
    span2 = [sp.expand(Ktw[0] * Ktw[2]), sp.expand(Ktw[1] ** 2),
             sp.expand(Ktw[3] ** 2)]
    inv_only = solvable([vec5(sp.expand(Ktw[0] ** 2))], dA)
    check("S5.1 [NC-a: INVARIANT AXION ONLY] v505 S3.9 replicated: sector "
          "0 lies in its graded span, sectors 1 and 2 do NOT (rank "
          "obstruction), and A_fix is not in span{(K^{(0)})^2} -- the "
          "single-axion mechanism fails exactly as before (the gamma "
          "enumeration adds: the three sphere axions do not repair it)",
          ok_span0 and (not in_span(Qtw[1], span1))
          and (not in_span(Qtw[2], span2)) and inv_only is None)

    allowed_flip = [(m, m % 4) for m in range(4)]
    pairs_strict = sorted({tuple(sorted(((4 - m) % 4, (4 - (4 - m)) % 4)))
                           for m in range(1, 4)})
    pairs_flip = sorted({tuple(sorted((m % 4, (4 - m) % 4)))
                         for m in range(1, 4)})
    live_flip = [(m, j, jp) for m in range(4) for j in range(4)
                 for jp in range(4)
                 if (m + j - jp) % 4 == 0 and jp == (4 - j) % 4]
    m_coupled = sorted({m for m, _, _ in live_flip})
    bulk_v = [decompose(K[0], [S5, S3]), decompose(K[2], [S5, S3])]
    det_bulk = sp.Matrix(bulk_v).det()
    prods_flip = [vec5(sp.expand(K[0] ** 2)), vec5(sp.expand(K[0] * K[2])),
                  vec5(sp.expand(K[2] ** 2))]
    solP_flip = solvable(prods_flip, dA[:3] + [0, 0])
    dead_flip = solvable(prods_flip + [vec5(sp.expand(K[1] ** 2))], dA)
    print("     flipped rule m + j - j' = 0: coupled charges (two-index "
          "reading) = %s; bulk vertex space span{K_0, K_2}, det %s"
          % (fmt(m_coupled), det_bulk))
    check("S5.2 [NC-b: FLIPPED RULE m + j - j'] twist-insertion reading: "
          "channel pair set %s unchanged vs strict %s -- IDENTICAL image, "
          "the kill is rule-flip invariant there; two-index reading "
          "CHANGES: now only eta_2 couples (charges %s, via C_{1,3} = "
          "-K_1) and the bulk axion gets the full 2-dim space span{K_0, "
          "K_2} (det 224 != 0), so the P-part becomes reachable -- but "
          "32 T3 stays unreachable (S1.4): a DIFFERENT enumeration, the "
          "same deep kill"
          % (fmt(pairs_flip), fmt(pairs_strict), fmt(m_coupled)),
          pairs_flip == pairs_strict and m_coupled == [0, 2]
          and det_bulk == 224 and solP_flip is not None
          and dead_flip is None and allowed_flip[2] == (2, 2))

    Qso = {0: Q[0], 2: Q[2]}
    Qso_tw = {j: sp.expand(sum(sp.I ** (j * m) * Qso[m] for m in (0, 2)))
              for j in (1, 2, 3)}
    Aso = vec5(sp.expand(Qso_tw[1] / 2 + Qso_tw[2] / 4 + Qso_tw[3] / 2))
    print("     SO(16) AB residual: %s" % fmt(Aso))
    check("S5.3 [NC-c: SO(16) GLUE] classes {0, 2} only: the odd McKay "
          "nodes are EMPTY -- there are NO twisted sphere-axion partners "
          "at all; the so16 AB sum = (15, -18, -15, -4, 40): T5 = -4 does "
          "NOT even cancel (unlike E8's exact T5 = 0) and T3 = 40 stands "
          "with zero axions available: the mechanism is structurally "
          "BROKEN, not merely obstructed -- the E8 mu4 glue is special "
          "on both counts",
          Aso == [15, -18, -15, -4, 40])

    Z8 = sp.symbols('z1:9')
    s8 = sp.expand(sum(z ** 2 for z in Z8))
    t8 = sp.expand(sum(z ** 4 for z in Z8))
    quad = sp.Integer(0)
    quart = sp.Integer(0)
    for i, j in combinations(range(8), 2):
        for si in (1, -1):
            for sj in (1, -1):
                lf = si * Z8[i] + sj * Z8[j]
                quad += lf ** 2
                quart += lf ** 4
    quad = sp.expand(quad)
    quart = sp.expand(quart)
    check("S5.4 [NC-d: D8 NATIVE VARIANT] on the D8 Cartan the 112 so16 "
          "roots give sum <alpha,z>^2 = 28 s8 (2 h_vee(D8) = 28) and "
          "sum <alpha,z>^4 = 16 T8 + 12 s8^2: the independent quartic "
          "coefficient 16 != 0 (no Okubo, matching v505 S6.3 in native "
          "coordinates) and there is NO A3 block at all -- no T3 "
          "structure, no sphere classes, nothing to pair: the gamma "
          "mechanism question cannot even be posed for the D8 route",
          sp.expand(quad - 28 * s8) == 0
          and sp.expand(quart - (16 * t8 + 12 * s8 ** 2)) == 0)


# ---------------------------------------------------------------------------
# S6 -- verdict and honest fences
# ---------------------------------------------------------------------------
def section6():
    print("  -- S6: verdict and honest fences")
    check("S6.1 [VERDICT: EXCHANGE ROUTE KILLED, INFLOW NOT DEAD] the "
          "pairing 'three sphere axions cancel 32 T3 by quadratic-vertex "
          "exchange' is REFUTED with a three-functional certificate "
          "(Phi_T5, Phi_T3, Phi_P) = (0, 32, 72), rule- and coupling-"
          "independent in the T3 direction; the slot bijection (three "
          "sphere classes <-> three twisted sectors, v505 S5.8) is "
          "UNTOUCHED -- what dies is the exchange REALISATION of the "
          "pairing, not the slot count; the burden moves to twisted "
          "closed-string CONTACT terms: the 5-dim quartic space trivially "
          "contains A_fix, but the coefficient must be COMPUTED from the "
          "BCOV one-loop measure on C^2/Z4, not fitted", True)
    check("S6.2 [O-FENCE + ROADMAP HOOKS] open after gamma: (delta-1) the "
          "twisted BCOV one-loop contact terms on C^2/Z4 (orbifold "
          "elliptic-genus / twisted-character arithmetic; success = "
          "coefficient exactly -(9, -30, -15, 0, 32), kill = any other "
          "exact value); (delta-2) the full-tensor ledger with non-Cartan "
          "external legs (the collapse S2.2 is a Cartan-restricted "
          "statement; the V^{(j,j')} with j' != -j are nonzero as "
          "TENSORS); (epsilon-1) the O(-2) bulk-axion construction "
          "(lambda~ = 6); (epsilon-2) CPS level-from-flux (k = 1 from "
          "flux quantisation on the lockstep spheres); SEAM.EQUIV.01 "
          "untouched; the preregistered level-kill still does NOT fire; "
          "NO marker moves anywhere", True)


# ---------------------------------------------------------------------------
def run():
    reset()
    print("v508  CELEST.WP5E.GAMMA.01: the sphere-axion pairing check "
          "(WP5e-gamma of CELEST.SEAM.01 -- a rigid negative result "
          "with certificate)")
    roots = build_glue_roots()
    K, Q = power_sums_by_class(roots)
    Ktw, Qtw, Afix, dA = section0(roots, K, Q)
    section1(Ktw)
    E13, E22, E00 = section2(roots, K, Ktw)
    section3(E13, E22, E00, dA, Qtw)
    section4(E13, E22, dA)
    section5(K, Q, Ktw, Qtw, dA)
    section6()

    return summary("v508 CELEST.WP5E.GAMMA.01: the exchange route for the "
                   "sphere-axion pairing is killed with a certificate -- "
                   "the W(D5) x W(A3)-invariant quadratics on the glue "
                   "Cartan are exactly span{s5, s3} (dim 2) and the "
                   "quartics exactly span{P1, P2, P3, T5, T3} (dim 5); "
                   "the product of any two invariant quadratics has zero "
                   "T5/T3 content, so every exchange image is annihilated "
                   "by Phi_T3 while Phi_T3(A_fix) = 32 != 0; the strict "
                   "two-index selection rule collapses the sphere "
                   "couplings entirely (only m = 0 survives), the twist-"
                   "insertion channels E13 = (16, -96, 144, 0, 0) and "
                   "E22 = (16, 32, 16, 0, 0) give a rank-2 exchange "
                   "matrix with rank([M | A_fix]) = 3 and certificate "
                   "(Phi_T5, Phi_T3, Phi_P) = (0, 32, 72); ch2-natural "
                   "and AB-weight couplings miss the target scale-"
                   "independently; SO(16) has no sphere partners and "
                   "uncancelled T5, D8 has no T3 structure at all; the "
                   "32 T3 burden moves to the twisted BCOV contact terms "
                   "(delta-1, binary) and the full-tensor ledger "
                   "(delta-2); slot bijection untouched, no marker moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
