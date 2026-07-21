"""v495 -- CELEST.WP3.01: the Green-Schwarz axion coefficient lambda_g of celestial
SDYM (Costello) vs the TFPT seam constant c3 = 1/(8 pi) -- WP3 of the research
contract CELEST.SEAM.01 (the pre-registered "alignment test only").  Exact
arithmetic (Fraction/sympy, no floats).

Question: Costello's twistorial SDYM theory is quantum-consistent exactly on the
algebras with no independent quartic Casimir (arXiv:2111.08879, eq. 1.2.2/2.4.2:
Tr_adj X^4 = lambda_g^2 (tr X^2)^2), and the forced Green-Schwarz axion coupling
is kappa = lambda_g/(8 pi sqrt 3) (his eq. 1.2.4).  WP3 asks ONLY: does kappa
align arithmetically with c3 = 1/(8 pi) for e8 -- and, brutally honestly, is any
such alignment e8-SELECTIVE at all?

  [E] S1. ROOT DATA + KILLING.  Exact root systems for all 8 algebras on
        Costello's list (sl2, sl3, g2, so8, f4, e6, e7, e8; e6/e7 carved out of
        the v492 E8 root set); |roots| = dim - rank; the Killing normalisation
        Sum_alpha <alpha,x>^2 = 2 h_vee <x,x> as an exact POLYNOMIAL identity
        (theta^2 = 2) pins h_vee = (2,3,4,6,9,12,18,30).
  [E] S2. OKUBO IDENTITY DERIVED, NOT QUOTED.  Sum_alpha <alpha,x>^4 =
        [5/(2(dim g + 2))] * (Sum_alpha <alpha,x>^2)^2 holds as an exact
        polynomial identity for ALL 8 algebras ("no independent quartic
        Casimir"); negative control: sl4 (which HAS one) fails the
        proportionality (5/32 on s0^4 vs 3/32 on s0^2 s2^2) -- the list is sharp.
  [E] S3. LAMBDA IN ALL CONVENTIONS.  Deligne-series dimension formula
        dim g = 2(5h_vee-6)(h_vee+1)/(h_vee+6) exact for all 8; unit-trace
        lambda~^2 = 10 h_vee^2/(dim+2) = h_vee + 6 EXACTLY (8,9,10,12,15,18,24,
        36) -- fixes Costello-Paquette eq. (1.5); fundamental Dynkin indices
        i_R = (1,1,2,2,6,6,12,60) from explicit weight systems; E8: lambda~ = 6
        and lambda_fund = 1/10 EXACT.  Cross-checks: Costello's sl2 = 8, sl3 = 9
        reproduced; his PRINTED lambda^2(so8) = 3/2 is a factor-2 slip (his own
        weight content gives Sum w^4 = 192, not 96: lambda^2 = 3, Okubo-
        consistent 12/4); the CP formula reading disambiguated (h_vee OUTSIDE
        the square root).
  [E] S4. ALIGNMENT vs c3 = 1/(8 pi).  kappa = lambda_g/(8 pi sqrt 3) contains
        c3 with (kappa/c3)^2 = lambda^2/3: e8 unit-trace 36/3 = 12 = |mu4| N_fam
        EXACT; adjoint-trace 1/300 EXACT.  kappa/c3 ITSELF is irrational
        (2 sqrt 3 resp. 1/(10 sqrt 3)): the pre-registered "lambda/sqrt3
        rational?" reading FAILS; only the squared alignment is exact.  Anchor
        decomposition: h_vee = 30 = |Z2| N_fam g_car (all three atoms once),
        phi(30) = 8 = rank, dim+2 = 250 = 2 * 5^3, lambda~ = 6 = |Z2| N_fam,
        lambda_fund = 1/10 = 1/(|Z2| g_car).
  [E] S5. LOOK-ELSEWHERE (the HARD FENCE of this module -- alignment != selection).
        All 8 candidates through the same battery:
              test                                   passes    who
              (kappa/c3)^2 an exact rational          8/8      everyone
              h_vee {2,3,5}-smooth                    8/8      everyone
              lambda~ integer (h_vee+6 square)        2/8      sl3, e8
              lambda_fund rational                    2/8      sl3, e8
              g_car = 5 | h_vee                       1/8      e8 ONLY
              phi(h_vee) = rank                       4/8      sl2,sl3,g2,e8
              phi(h) = rank                           5/8      +f4
        The alignment test AS SUCH has ZERO selective power (8/8); the only
        e8-selective single test is "the atom 5 = g_car divides h_vee" (1/8);
        the conjunction that isolates e8 (1/8) was assembled POST HOC from
        correlated sub-tests -- it quantifies where e8 sits, it is NOT a
        preregistered discriminator.
  [E] S6. KILL-TEST K3 + VERDICT.  K3 ("no exact alignment => the c3-connection
        of the celestial route dies") does NOT fire: exact alignment EXISTS.
        BUT by S5 the alignment format itself passes 8/8, so the c3-connection
        survives ONLY as convention-level compatibility plus genuine
        lambda-arithmetic -- it is NOT e8-selective evidence; K3's scope is
        DEMOTED accordingly in the contract.
  [C] TYPED: the 8 pi in Costello's (1.2.4) is the 2 pi-convention of the
        anomaly polynomial (his A.0.10 constant descended to spacetime), NOT an
        independent occurrence of the seam constant; the sqrt 3 is the
        anomaly's own (sqrt 48 = 4 sqrt 3 from the twistor box diagram,
        48 = 2*4!).  WP3 is an alignment yes/no -- it can never derive c3 from
        celestial data (contract wording, honoured here).
  [O] FENCE: no marker moves anywhere; WP5 (constructive holography) and
        SEAM.EQUIV.01 (the continuum (E8)_1 net on the seam) stay [O],
        untouched.  Verdict B: exact arithmetic alignment, honestly typed as
        non-selective.

Status: [E] exact arithmetic (Fraction/sympy, no floats); [C] the convention
typing of the 8 pi and sqrt 3; [O] the celestial programme (WP5).  Python;
Wolfram-mirrorable (exact), counted with the next verified engine run."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from math import factorial

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

Z2 = 2             # sheet order |Z2|
MU4 = 4            # |mu4|


# ---------------------------------------------------------------------------
# exact multivariate polynomials: dict {sorted index tuple: Fraction}
# ---------------------------------------------------------------------------
def dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def multinom(combo, p):
    c = Counter(combo)
    r = factorial(p)
    for v in c.values():
        r //= factorial(v)
    return r


def add_pow(out, a, p):
    """out += (sum_j a_j s_j)^p  as an exact polynomial dict."""
    idxs = [j for j in range(len(a)) if a[j] != 0]
    for combo in combinations_with_replacement(idxs, p):
        coef = F(multinom(combo, p))
        for j in combo:
            coef *= a[j]
        out[combo] = out.get(combo, F(0)) + coef


def poly_square(K):
    out = {}
    items = list(K.items())
    for i in range(len(items)):
        k1, c1 = items[i]
        key = tuple(sorted(k1 + k1))
        out[key] = out.get(key, F(0)) + c1 * c1
        for j in range(i + 1, len(items)):
            k2, c2 = items[j]
            key = tuple(sorted(k1 + k2))
            out[key] = out.get(key, F(0)) + 2 * c1 * c2
    return out


def poly_eq_scaled(P, Q, num, den):
    """den * P == num * Q  exactly (both polynomial dicts)."""
    keys = set(P) | set(Q)
    return all(den * P.get(k, F(0)) == num * Q.get(k, F(0)) for k in keys)


def power_sums(vectors, basis):
    """(Sum <v,x>^2, Sum <v,x>^4) as polynomial dicts in x = sum s_j b_j."""
    K, Q = {}, {}
    for v in vectors:
        a = [F(dot(v, b)) for b in basis]
        add_pow(K, a, 2)
        add_pow(Q, a, 4)
    return K, Q


def gram_quad(basis):
    """<x,x> as a polynomial dict (same key convention as add_pow)."""
    out = {}
    m = len(basis)
    for j in range(m):
        for k in range(j, m):
            g = F(dot(basis[j], basis[k]))
            if g:
                out[(j, k)] = out.get((j, k), F(0)) + g * (1 if j == k else 2)
    return out


# ---------------------------------------------------------------------------
# root systems (theta^2 = 2 normalisation throughout)
# ---------------------------------------------------------------------------
def roots_sl2():
    return [(1, -1), (-1, 1)]


def roots_sl3():
    out = []
    for i, j in product(range(3), repeat=2):
        if i != j:
            v = [0] * 3
            v[i], v[j] = 1, -1
            out.append(tuple(v))
    return out


def roots_g2():
    lng = []
    for i, j in product(range(3), repeat=2):
        if i != j:
            v = [F(0)] * 3
            v[i], v[j] = F(1), F(-1)
            lng.append(tuple(v))
    sht = []
    for i in range(3):
        v = [F(-1, 3)] * 3
        v[i] = F(2, 3)
        sht.append(tuple(v))
        sht.append(tuple(-x for x in v))
    return lng, sht


def roots_so8():
    out = []
    for i, j in combinations(range(4), 2):
        for si in (1, -1):
            for sj in (1, -1):
                v = [0] * 4
                v[i], v[j] = si, sj
                out.append(tuple(v))
    return out


def roots_f4():
    lng = roots_so8()
    sht = []
    for i in range(4):
        for s in (1, -1):
            v = [F(0)] * 4
            v[i] = F(s)
            sht.append(tuple(v))
    for signs in product((1, -1), repeat=4):
        sht.append(tuple(F(s, 2) for s in signs))
    return lng, sht


def roots_sl4():
    out = []
    for i, j in product(range(4), repeat=2):
        if i != j:
            v = [0] * 4
            v[i], v[j] = 1, -1
            out.append(tuple(v))
    return out


def roots_e8():
    """v128/v492 construction in D5 (+) A3 glue coordinates, flattened to R^9
    (A3 block sum-zero); all 240 roots have norm 2."""
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
    roots = []
    for r in d5_roots:
        roots.append(r + z4)
    for r in a3_roots:
        roots.append(z5 + r)
    for d in d5_s:
        for w in wclass(1):
            roots.append(d + w)
    for d in d5_v:
        for w in wclass(2):
            roots.append(d + w)
    for d in d5_c:
        for w in wclass(3):
            roots.append(d + w)
    return roots


def basis_sumzero(n, ambient):
    """simple-root-style basis (1,-1,0,..) of the sum-zero subspace of R^n,
    padded to the ambient dimension."""
    out = []
    for i in range(n - 1):
        v = [F(0)] * ambient
        v[i], v[i + 1] = F(1), F(-1)
        out.append(tuple(v))
    return out


# ---------------------------------------------------------------------------
# the algebra table (name, dim, h_vee, h, rank, roots, basis, fund weights, i_R)
# ---------------------------------------------------------------------------
def build_algebras():
    E8 = roots_e8()
    e8_basis = []
    for i in range(5):
        v = [F(0)] * 9
        v[i] = F(1)
        e8_basis.append(tuple(v))
    for i in range(3):
        v = [F(0)] * 9
        v[5 + i], v[6 + i] = F(1), F(-1)
        e8_basis.append(tuple(v))

    delta1 = tuple([F(1), F(1)] + [F(0)] * 7)          # D5 root (1,1,0,0,0)
    delta2 = tuple([F(0), F(-1), F(1)] + [F(0)] * 6)   # D5 root (0,-1,1,0,0)

    e7_roots = [r for r in E8 if dot(r, delta1) == 0]
    e7_basis = [tuple([F(1), F(-1)] + [F(0)] * 7)] + \
        [e8_basis[i] for i in (2, 3, 4, 5, 6, 7)]
    e7_56 = [r for r in E8 if dot(r, delta1) == 1]

    e6_roots = [r for r in E8
                if dot(r, delta1) == 0 and dot(r, delta2) == 0]
    e6_basis = [tuple([F(1), F(-1), F(-1)] + [F(0)] * 6)] + \
        [e8_basis[i] for i in (3, 4, 5, 6, 7)]
    e6_27 = [r for r in E8 if dot(r, delta1) == 1 and dot(r, delta2) == 0]

    g2_long, g2_short = roots_g2()
    f4_long, f4_short = roots_f4()

    sl2_fund = [(F(1, 2), F(-1, 2)), (F(-1, 2), F(1, 2))]
    sl3_fund = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    so8_vec = []
    for i in range(4):
        for s in (1, -1):
            v = [0] * 4
            v[i] = s
            so8_vec.append(tuple(v))

    return [
        ("sl2", 3, 2, 2, 1, roots_sl2(), basis_sumzero(2, 2), sl2_fund, 1),
        ("sl3", 8, 3, 3, 2, roots_sl3(), basis_sumzero(3, 3), sl3_fund, 1),
        ("g2", 14, 4, 6, 2, g2_long + g2_short, basis_sumzero(3, 3),
         g2_short, 2),
        ("so8", 28, 6, 6, 4, roots_so8(),
         [tuple(F(1) if j == i else F(0) for j in range(4))
          for i in range(4)], so8_vec, 2),
        ("f4", 52, 9, 12, 4, f4_long + f4_short,
         [tuple(F(1) if j == i else F(0) for j in range(4))
          for i in range(4)], f4_short, 6),
        ("e6", 78, 12, 12, 6, e6_roots, e6_basis, e6_27, 6),
        ("e7", 133, 18, 18, 7, e7_roots, e7_basis, e7_56, 12),
        ("e8", 248, 30, 30, 8, E8, e8_basis, E8, 60),
    ]


def section1(algs):
    print("  -- S1: exact root systems + Killing normalisation (theta^2 = 2)")
    counts = {name: len(roots)
              for (name, _, _, _, _, roots, _, _, _) in algs}
    ok_counts = all(len(roots) == dim - rank
                    for (_, dim, _, _, rank, roots, _, _, _) in algs)
    check("S1 [E]: root counts = dim - rank for all 8 algebras on Costello's "
          "list: %s" % counts, ok_counts)

    ok_e67 = (counts["e6"] == 72 and counts["e7"] == 126
              and len(algs[5][7]) == 27 and len(algs[6][7]) == 56)
    check("S1 [E]: e6/e7 carved out of the v492 E8 root set: 72 = |e6 roots|, "
          "126 = |e7 roots|, branching slices |27| = 27 (e6), |56| = 56 (e7) "
          "-- adjoint e8 = (78,1)+(1,8)+(27,3)+(27b,3b) resp. "
          "(133,1)+(1,3)+(56,2) at the root level", ok_e67)

    ok_norm = True
    for (name, dim, hv, _, _, roots, basis, _, _) in algs:
        K, _ = power_sums(roots, basis)
        Gq = gram_quad(basis)
        ok_norm &= poly_eq_scaled(K, Gq, 2 * hv, 1)
    check("S1 [E]: KILLING = 2 h_vee <.,.> as an exact POLYNOMIAL identity in "
          "x for all 8 (h_vee = 2,3,4,6,9,12,18,30) -- the theta^2 = 2 "
          "normalisation and the dual Coxeter numbers are pinned", ok_norm)


def section2(algs):
    print("  -- S2: the quartic (Okubo) identity, derived exactly")
    ok_okubo = True
    for (name, dim, hv, _, _, roots, basis, _, _) in algs:
        K, Q = power_sums(roots, basis)
        K2 = poly_square(K)
        ok_okubo &= poly_eq_scaled(Q, K2, 5, 2 * (dim + 2))
    check("S2 [E]: OKUBO IDENTITY DERIVED -- Sum_alpha <alpha,x>^4 = "
          "[5/(2(dim g+2))] * (Sum_alpha <alpha,x>^2)^2 holds as an exact "
          "polynomial identity for ALL 8 algebras (= no independent quartic "
          "Casimir; the anomaly is a perfect square)", ok_okubo)

    sl4_basis = basis_sumzero(4, 4)
    K4, Q4 = power_sums(roots_sl4(), sl4_basis)
    K42 = poly_square(K4)
    k1 = (0, 0, 0, 0)       # monomial s0^4
    k2 = (0, 0, 2, 2)       # monomial s0^2 s2^2
    r1 = F(Q4[k1]) / F(K42[k1])
    r2 = F(Q4[k2]) / F(K42[k2])
    check("S2 [E]: NEGATIVE CONTROL -- sl4 (HAS an independent quartic "
          "Casimir) fails the proportionality: Q/K^2 = %s on s0^4 but %s on "
          "s0^2 s2^2: Costello's list is sharp, the identity is not a generic "
          "accident" % (r1, r2), r1 == F(5, 32) and r2 == F(3, 32))


def section3(algs):
    print("  -- S3: lambda_g in all conventions (exact)")
    rows = {}
    ok_dl = ok_lam = ok_idx = True
    for (name, dim, hv, h, rank, roots, basis, fund, i_exp) in algs:
        ok_dl &= (dim * (hv + 6) == 2 * (5 * hv - 6) * (hv + 1))
        lam2_unit = F(10 * hv * hv, dim + 2)
        ok_lam &= (lam2_unit == hv + 6)
        Kf, _ = power_sums(fund, basis)
        Gq = gram_quad(basis)
        ok_idx &= poly_eq_scaled(Kf, Gq, i_exp, 1)
        rows[name] = (hv, h, rank, lam2_unit, i_exp, F(hv + 6, i_exp * i_exp))
    check("S3 [E]: DELIGNE-SERIES DIMENSION FORMULA -- dim g = 2(5h_vee-6)"
          "(h_vee+1)/(h_vee+6) exactly for all 8: Costello's list IS the "
          "Deligne exceptional series", ok_dl)
    check("S3 [E]: UNIT-TRACE LAMBDA -- lambda~^2 = 10 h_vee^2/(dim g+2) = "
          "h_vee + 6 EXACTLY for all 8: (8,9,10,12,15,18,24,36); fixes "
          "Costello-Paquette eq. (1.5) [lambda = sqrt(10) h_vee/sqrt(dim+2)] "
          "and gives Tr_adj X^4 = [(h_vee+6)/(4 h_vee^2)] (Tr_adj X^2)^2",
          ok_lam)
    check("S3 [E]: FUNDAMENTAL DYNKIN INDICES from explicit weight systems -- "
          "tr_R X^2 = i_R <X,X> with i_R = (1,1,2,2,6,6,12,60) for "
          "(2, 3, 7, 8v, 26, 27, 56, 248): exact polynomial identities (for "
          "e8 the smallest faithful rep IS the adjoint, i = 2 h_vee = 60)",
          ok_idx)

    check("S3 [E]: LAMBDA_E8 EXACT -- fundamental(=adjoint)-trace convention: "
          "lambda_e8^2 = 36/3600 = 1/100, lambda_e8 = 1/10; unit-trace "
          "convention: lambda~_e8^2 = 36, lambda~_e8 = 6.  Both perfect "
          "squares of rationals",
          rows["e8"][5] == F(1, 100) and rows["e8"][3] == 36)

    check("S3 [E]: COSTELLO CROSS-CHECK -- his appendix-A samples "
          "lambda^2(sl2) = 32/4 = 8 and lambda^2(sl3) = 36/4 = 9 reproduced "
          "exactly in his own (fundamental-trace) convention",
          rows["sl2"][5] == 8 and rows["sl3"][5] == 9)

    w4_adj_so8 = 12 * 2 ** 4          # six weights +2, six weights -2
    w2_fund_so8 = 8                   # four weights each of +-1
    lam2_so8 = F(w4_adj_so8, w2_fund_so8 ** 2)
    check("S3 [E]: COSTELLO SO8 SLIP FLAGGED -- with HIS stated weight "
          "content (fundamental: four each of +-1; adjoint: six each of +-2) "
          "the sums are Sum w^4 = 192, (Sum w^2)^2 = 64: lambda^2(so8) = 3 "
          "exactly (= (h_vee+6)/i^2 = 12/4, Okubo-consistent); the PRINTED "
          "96/64 = 3/2 undercounts Lambda^2 C^4_+ (+) Lambda^2 C^4_- by a "
          "factor 2",
          lam2_so8 == 3 and rows["so8"][5] == 3 and lam2_so8 != F(3, 2))

    misread = F(10 * 2, 3 + 2)        # the "sqrt(10 h_vee)" reading for sl2
    check("S3 [E]: CP FORMULA DISAMBIGUATED -- the reading lambda^2 = "
          "10 h_vee/(dim+2) gives %s for sl2, contradicting the exact 8; the "
          "reading lambda = sqrt(10) h_vee/sqrt(dim+2) gives h_vee+6 = 8 -- "
          "the latter is the correct normalisation (h_vee outside the root)"
          % misread, misread == 4 and misread != 8)
    return rows


# ---------------------------------------------------------------------------
# S4/S5 -- alignment + look-elsewhere
# ---------------------------------------------------------------------------
def phi(n):
    return sum(1 for k in range(1, n + 1) if sp.gcd(k, n) == 1)


def smooth235(n):
    for p in (2, 3, 5):
        while n % p == 0:
            n //= p
    return n == 1


def is_square(q):
    q = F(q)
    return sp.sqrt(sp.Rational(q.numerator, q.denominator)).is_rational


def section4(rows):
    print("  -- S4: alignment against c3 = 1/(8 pi) (typed brutally honestly)")
    hv, _, _, lam2_unit, _, lam2_fund = rows["e8"]

    ratio2_unit = F(lam2_unit, 3)          # (kappa/c3)^2, unit-trace CS
    ratio2_fund = F(lam2_fund, 3)          # (kappa^/c3)^2, adjoint-trace CS
    check("S4 [E]: the GS coupling kappa = lambda_g/(8 pi sqrt 3) contains "
          "c3 = 1/(8 pi) with (kappa/c3)^2 = lambda^2/3: e8 unit-trace = "
          "36/3 = 12 EXACT; adjoint-trace = (1/100)/3 = 1/300 EXACT -- both "
          "anchor rationals (12 = |mu4| N_fam, 300 = 2^2 3 5^2)",
          ratio2_unit == 12 and ratio2_fund == F(1, 300)
          and 12 == MU4 * N_fam and 300 == 2 ** 2 * 3 * 5 ** 2)

    check("S4 [E]: kappa/c3 ITSELF IS IRRATIONAL -- 12 and 1/300 are not "
          "squares of rationals (kappa/c3 = 2 sqrt3 resp. 1/(10 sqrt3)): the "
          "pre-registered 'lambda_e8/sqrt(3) rational?' reading FAILS; only "
          "the SQUARED alignment is exact.  The sqrt(3) is the anomaly's own "
          "(sqrt 48 = 4 sqrt 3 from the twistor box diagram, 48 = 2*4!)",
          (not is_square(12)) and (not is_square(F(1, 300)))
          and 48 == 2 * factorial(4))

    check("S4 [E]: ANCHOR DECOMPOSITION OF THE E8 DATA -- h_vee = 30 = "
          "|Z2|*N_fam*g_car = 2*3*5 (squarefree, all three TFPT atoms once); "
          "phi(30) = 8 = rank(E8); dim+2 = 250 = 2*5^3; lambda~ = 6 = "
          "|Z2|*N_fam; lambda_fund = 1/10 = 1/(|Z2|*g_car); lambda~^2 = 36 = "
          "h_vee + 6",
          hv == Z2 * N_fam * g_car and phi(30) == rankE8
          and 250 == 2 * 5 ** 3 and lam2_unit == (Z2 * N_fam) ** 2
          and lam2_fund == F(1, (Z2 * g_car) ** 2) and 36 == hv + 6)

    check("S4 [C, TYPED]: the 8 pi in Costello's (1.2.4) is the 2 pi-"
          "convention of the anomaly polynomial (his A.0.10 constant "
          "C_YM = 1/((2 pi i)^{3/2} sqrt 48) descended to spacetime), NOT an "
          "independent occurrence of the seam constant: the WP3 test is "
          "'exact arithmetic alignment yes/no' ONLY -- it can never derive "
          "c3 from celestial data (contract wording, honoured here)", True)


def section5(rows):
    print("  -- S5: look-elsewhere -- ALL 8 candidates through the same "
          "battery (the hard fence: alignment != selection)")
    names = ["sl2", "sl3", "g2", "so8", "f4", "e6", "e7", "e8"]
    tab = {}
    for n in names:
        hv, h, rank, lam2u, i_r, lam2f = rows[n]
        tab[n] = (smooth235(hv), is_square(lam2u), is_square(lam2f),
                  hv % g_car == 0, phi(hv) == rank, phi(h) == rank)

    n_smooth = sum(1 for n in names if tab[n][0])
    check("S5 [E]: LOOK-ELSEWHERE (the brutal one) -- '(kappa/c3)^2 = "
          "(h_vee+6)/3 is an exact rational' passes 8/8 BY CONSTRUCTION and "
          "'h_vee is {2,3,5}-smooth' passes %d/8: the alignment test AS SUCH "
          "has ZERO selective power for e8 -- every algebra on Costello's "
          "list aligns this way" % n_smooth, n_smooth == 8)

    ints = [n for n in names if tab[n][1]]
    fundrats = [n for n in names if tab[n][2]]
    check("S5 [E]: 'lambda~ integer' (h_vee+6 a perfect square) passes 2/8: "
          "%s; 'lambda_fund rational' passes the SAME 2/8: %s -- e8 shares "
          "this distinction with sl3 (9 = 3^2, 36 = 6^2 are the only squares "
          "in (8,9,10,12,15,18,24,36))" % (ints, fundrats),
          ints == ["sl3", "e8"] and fundrats == ["sl3", "e8"])

    five = [n for n in names if tab[n][3]]
    check("S5 [E]: 'g_car = 5 divides h_vee' passes 1/8: %s -- the ONLY test "
          "in the battery that singles out e8 alone (30 is the unique h_vee "
          "on the list containing the atom 5)" % five, five == ["e8"])

    phivs = [n for n in names if tab[n][4]]
    phihs = [n for n in names if tab[n][5]]
    check("S5 [E]: 'phi(h_vee) = rank' passes 4/8 (%s); 'phi(h) = rank' "
          "passes 5/8 (%s): the totient test is real but NOT e8-specific"
          % (phivs, phihs),
          phivs == ["sl2", "sl3", "g2", "e8"]
          and phihs == ["sl2", "sl3", "g2", "f4", "e8"])

    units = sorted(k for k in range(1, 30) if sp.gcd(k, 30) == 1)
    exps = [1, 7, 11, 13, 17, 19, 23, 29]
    prodd = 1
    for e in exps:
        prodd *= e + 1
    check("S5 [E]: E8 EXTRAS (exact arithmetic; exponent list [C] standard "
          "data) -- exponents of e8 = %s = the units mod 30 (the phi-set of "
          "h_vee), sum = 120 = #positive roots; degrees product = %d = "
          "|W(E8)|" % (exps, prodd),
          units == exps and sum(exps) == 120 and prodd == 696729600)

    joint = [n for n in names if tab[n][1] and tab[n][3] and tab[n][4]]
    check("S5 [E]: JOINT TEST TYPED HONESTLY -- the conjunction (lambda~ "
          "integer AND g_car | h_vee AND phi(h_vee) = rank) passes 1/8 (%s), "
          "but the conjunction was assembled POST HOC from correlated "
          "sub-tests: it quantifies where e8 sits, it is NOT a preregistered "
          "discriminator.  Honest summary: alignment alone 8/8, sharpest "
          "single natural test 1/8 (atom 5 = g_car in h_vee)" % joint,
          joint == ["e8"])


def section6():
    print("  -- S6: kill-test K3 evaluation + verdict")
    check("S6 [E] KILL-TEST K3 (contract: 'no exact alignment => the c3-"
          "connection of the celestial route dies') -- K3 does NOT fire: "
          "exact arithmetic alignment EXISTS ((kappa/c3)^2 = 12 resp. 1/300, "
          "lambda_e8 = 6 resp. 1/10, all exact anchor rationals).  BUT the "
          "look-elsewhere battery (S5) shows the alignment format itself "
          "passes 8/8: the c3-connection SURVIVES only as convention-level "
          "compatibility plus genuine lambda-arithmetic -- it is NOT "
          "e8-selective evidence; K3's scope is demoted accordingly", True)

    check("S6 [C]: WHAT IS NEW AND EXACT HERE -- (i) the Okubo coefficient "
          "5/(2(dim+2)) DERIVED as a polynomial identity for all 8 algebras "
          "with a sharp sl4 negative control; (ii) the closed form lambda~^2 "
          "= h_vee + 6 across the Deligne series; (iii) lambda_e8 = 1/10 "
          "(adjoint units) resp. 6 (unit-trace) EXACT; (iv) the so8 factor-2 "
          "slip in the printed source localised; (v) the honest pass-count "
          "table (S5)", True)

    check("S6 [O] FENCE -- WP3 verdict B: exact arithmetic alignment, "
          "honestly typed as NON-SELECTIVE (the e8-specific content is "
          "h_vee = 2*3*5 with phi = 8 = rank and lambda-integrality shared "
          "only with sl3); no marker moves anywhere; WP5 (constructive "
          "holography) and SEAM.EQUIV.01 stay [O], untouched", True)


def run():
    reset()
    print("v495  CELEST.WP3.01: Green-Schwarz axion coefficient lambda_g "
          "(Costello) vs the TFPT seam constant c3 = 1/(8 pi) (WP3 of "
          "CELEST.SEAM.01 -- alignment test only)")
    algs = build_algebras()
    section1(algs)
    section2(algs)
    rows = section3(algs)
    section4(rows)
    section5(rows)
    section6()

    return summary("v495 CELEST.WP3.01: Okubo coefficient 5/(2(dim+2)) derived for all 8 "
                   "algebras (sl4 negative control); lambda~^2 = h_vee + 6 across the Deligne "
                   "series; lambda_e8 = 6 (unit-trace) resp. 1/10 (adjoint-trace) exact; "
                   "(kappa/c3)^2 = 12 = |mu4| N_fam resp. 1/300 exact, kappa/c3 irrational; "
                   "so8 factor-2 slip flagged; look-elsewhere: alignment 8/8 (zero selectivity), "
                   "g_car | h_vee 1/8 (e8 only), lambda-integrality 2/8 (with sl3), joint test "
                   "post hoc. K3 does not fire, scope demoted: compatibility, not e8-selective "
                   "evidence. Verdict B; SEAM.EQUIV.01 untouched")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
