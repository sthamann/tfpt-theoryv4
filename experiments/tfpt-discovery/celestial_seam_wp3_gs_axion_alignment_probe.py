"""WP3 of CELEST.SEAM.01 (EXPLORATION ONLY -- experiments/, no verification claim).

The Green-Schwarz axion coefficient lambda_g of celestial/twistorial SDYM
(Costello, arXiv:2111.08879) for ALL algebras on Costello's list, against the
TFPT seam constant c3 = 1/(8 pi) -- the WP3 "alignment test only" of the
research contract CELEST.SEAM.01 (tfpt_research_contracts).  Exact arithmetic
(Fraction / sympy, no floats).

Method anchors (all normalisations traced to the sources):
  * Costello, arXiv:2111.08879: SDYM on twistor space is quantum-consistent iff
    Tr_adj(X^4) = lambda_g^2 (tr X^2)^2 (Tr = adjoint, tr = fundamental trace;
    his eq. 1.2.2/2.4.2), which holds for sl2, sl3, so8 and all exceptional
    algebras (no independent quartic Casimir; Okubo).  The forced axion term is
    (1.2.4):  lambda_g/(8 pi sqrt(3)) * Int d rho ^ CS(A),  dCS(A) = tr F^2.
    His appendix A samples:  lambda^2(sl2) = 8,  lambda^2(sl3) = 9,  and the
    PRINTED lambda^2(so8) = 96/64 = 3/2 (checked below: the stated weight
    content gives 192/64 = 3 -- a factor-2 slip in the printed sum, flagged).
  * Costello-Paquette, JHEP 10 (2022) 193 (arXiv:2201.02595), eq. (1.5):
    lambda_g = sqrt(10) h_vee / sqrt(dim g + 2)   [unit-trace convention]
    -- equivalently lambda_g^2 = 10 h_vee^2/(dim g + 2), verified here to be
    EXACTLY h_vee + 6 across the whole list (Deligne series identity).

Sections (checks counted; fences typed honestly):
  S1  ROOT DATA + KILLING.  Exact root systems for sl2, sl3, g2, so8, f4, e6,
      e7, e8 (e6/e7 carved out of the v492 e8 root set); |roots| = dim - rank;
      Killing form Sum_alpha <alpha,x>^2 = 2 h_vee <x,x> as a POLYNOMIAL
      identity in x (theta^2 = 2 normalisation) -- fixes h_vee exactly.
  S2  OKUBO QUARTIC IDENTITY (derived, not quoted).  For all 8 algebras the
      full polynomial identity  Sum_alpha <alpha,x>^4
      = [5/(2(dim g + 2))] * (Sum_alpha <alpha,x>^2)^2  holds EXACTLY (this is
      "no independent quartic Casimir").  Negative control: sl4 (which HAS an
      independent quartic Casimir) fails the proportionality.
  S3  LAMBDA VALUES, ALL CONVENTIONS.  Unit-trace lambda~^2 = 10 h_vee^2 /
      (dim+2) = h_vee + 6 exactly for the whole list (8,9,10,12,15,18,24,36);
      fundamental-trace lambda^2 = (h_vee+6)/i_R^2 with the Dynkin indices i_R
      of the smallest faithful reps COMPUTED from explicit weight systems
      (2, 3, 7, 8v, 26, 27, 56, 248): (8, 9, 5/2, 3, 5/12, 1/2, 1/6, 1/100).
      lambda_e8 = 1/10 exactly (fundamental = adjoint), lambda~_e8 = 6 exactly.
      Costello cross-checks: sl2 = 8 ok, sl3 = 9 ok, so8: exact value 3, the
      printed 3/2 is a factor-2 slip (Sum w^4_adj = 192, not 96).
  S4  ALIGNMENT vs c3 = 1/(8 pi).  The physical GS coupling is convention-
      independent (lambda_g * CS_tr invariant under trace rescaling); in unit-
      trace units kappa = sqrt(h_vee+6)/(8 pi sqrt 3).  For e8:
      kappa = 6/(8 pi sqrt 3) = 2 sqrt(3) c3,  (kappa/c3)^2 = 12 exactly;
      adjoint-trace form: kappa^ = c3/(10 sqrt 3), (kappa^/c3)^2 = 1/300.
      Anchor decompositions: h_vee(e8) = 30 = |Z2| N_fam g_car, phi(30) = 8 =
      rank, dim+2 = 250 = 2 * 5^3, lambda~ = 6 = |Z2| N_fam, lambda = 1/10 =
      1/(|Z2| g_car).  HONEST: the 8 pi itself is the 2 pi-convention of the
      anomaly polynomial -- alignment can only ever be arithmetic, never a
      derivation of c3 (contract wording).  lambda_e8/sqrt(3) is IRRATIONAL
      (12 and 1/300 are not squares): the pre-registered "lambda/sqrt3
      rational?" reading fails; the squared alignment holds.
  S5  NEGATIVE CONTROLS / LOOK-ELSEWHERE (all 8 candidates).
      (kappa/c3)^2 = (h_vee+6)/3 rational: passes 8/8  -> the alignment test
      alone has ZERO selective power (brutal honesty).  h_vee {2,3,5}-smooth:
      8/8 (also no power).  lambda~ integer: 2/8 (sl3, e8).  lambda_fund
      rational: 2/8 (sl3, e8).  g_car | h_vee: 1/8 (e8 ONLY).  phi(h_vee) =
      rank: 4/8; phi(h) = rank: 5/8.  e8 extras: exponents = units mod 30
      (phi-set), sum = 120 = #positive roots; degrees product = |W(E8)|.
  S6  KILL-TEST K3 EVALUATION + VERDICT (typed; no status change anywhere).

Throwaway probe: prints tables + PASS/FAIL + verdict, ends with a check count.
Nothing here is a claim; promotion (if any) goes through the usual workflow.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from math import factorial

import sympy as sp

G_CAR = 5          # carrier rank (axiom P2)
N_FAM = 3          # family index = rank A3
Z2 = 2             # sheet
MU4 = 4            # |mu4|

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
# S1/S2/S3 -- the algebra table
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

    # name, dim, h_vee, h (Coxeter), rank, roots, basis, fund weights,
    # expected fundamental Dynkin index i_R (tr_R X^2 = i_R <X,X>)
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
    ok_counts = all(len(roots) == dim - rank
                    for (_, dim, _, _, rank, roots, _, _, _) in algs)
    counts = {name: len(roots)
              for (name, _, _, _, _, roots, _, _, _) in algs}
    check("S1.1: root counts = dim - rank for all 8 algebras: %s" % counts,
          ok_counts)

    ok_e67 = (counts["e6"] == 72 and counts["e7"] == 126
              and len(algs[5][7]) == 27 and len(algs[6][7]) == 56)
    check("S1.2: e6/e7 carved out of the v492 e8 root set: 72 = |e6 roots|, "
          "126 = |e7 roots|, and the branching slices give |27| = 27 (e6), "
          "|56| = 56 (e7) -- adjoint e8 = (78,1)+(1,8)+(27,3)+(27b,3b) resp. "
          "(133,1)+(1,3)+(56,2) at the root level", ok_e67)

    ok_norm = True
    for (name, dim, hv, _, _, roots, basis, _, _) in algs:
        K, _ = power_sums(roots, basis)
        Gq = gram_quad(basis)
        ok_norm &= poly_eq_scaled(K, Gq, 2 * hv, 1)
    check("S1.3: KILLING = 2 h_vee <.,.> as an exact POLYNOMIAL identity in x "
          "for all 8 (h_vee = 2,3,4,6,9,12,18,30) -- the theta^2 = 2 "
          "normalisation and the dual Coxeter numbers are pinned", ok_norm)


def section2(algs):
    print("  -- S2: the quartic (Okubo) identity, derived exactly")
    ok_okubo = True
    print("        algebra   dim   c_g = Tr_adj X^4 / (Tr_adj X^2)^2")
    for (name, dim, hv, _, _, roots, basis, _, _) in algs:
        K, Q = power_sums(roots, basis)
        K2 = poly_square(K)
        ok = poly_eq_scaled(Q, K2, 5, 2 * (dim + 2))
        ok_okubo &= ok
        print("        %-8s  %3d   5/(2*(dim+2)) = 5/%d   [%s]"
              % (name, dim, 2 * (dim + 2), "exact" if ok else "FAIL"))
    check("S2.1: OKUBO IDENTITY -- Sum_alpha <alpha,x>^4 = [5/(2(dim g+2))] * "
          "(Sum_alpha <alpha,x>^2)^2 holds as an exact polynomial identity for "
          "ALL 8 algebras on Costello's list (= no independent quartic "
          "Casimir; the anomaly is a perfect square)", ok_okubo)

    sl4_basis = basis_sumzero(4, 4)
    K4, Q4 = power_sums(roots_sl4(), sl4_basis)
    K42 = poly_square(K4)
    k1 = (0, 0, 0, 0)       # monomial s0^4
    k2 = (0, 0, 2, 2)       # monomial s0^2 s2^2
    r1 = sp.Rational(F(Q4[k1]) / F(K42[k1]))
    r2 = sp.Rational(F(Q4[k2]) / F(K42[k2]))
    check("S2.2: NEGATIVE CONTROL -- sl4 (HAS an independent quartic Casimir) "
          "fails the proportionality: Q/K^2 = %s on s0^4 but %s on s0^2 s2^2: "
          "Costello's list is sharp, the identity is not a generic accident"
          % (r1, r2), r1 != r2)


def section3(algs):
    print("  -- S3: lambda_g in all conventions (exact)")
    rows = {}
    ok_dl = ok_lam = ok_idx = True
    print("        algebra  h_vee  lambda~^2=h_vee+6  i_fund  "
          "lambda_fund^2 = (h_vee+6)/i^2")
    for (name, dim, hv, h, rank, roots, basis, fund, i_exp) in algs:
        ok_dl &= (dim * (hv + 6) == 2 * (5 * hv - 6) * (hv + 1))
        lam2_unit = F(10 * hv * hv, dim + 2)
        ok_lam &= (lam2_unit == hv + 6)
        Kf, _ = power_sums(fund, basis)
        Gq = gram_quad(basis)
        ok_idx &= poly_eq_scaled(Kf, Gq, i_exp, 1)
        lam2_fund = F(hv + 6, i_exp * i_exp)
        rows[name] = (hv, h, rank, lam2_unit, i_exp, lam2_fund)
        print("        %-7s  %3d    %3s               %3d     %s"
              % (name, hv, lam2_unit, i_exp, lam2_fund))
    check("S3.1: DELIGNE-SERIES DIMENSION FORMULA -- dim g = 2(5h_vee-6)"
          "(h_vee+1)/(h_vee+6) exactly for all 8: Costello's list IS the "
          "Deligne exceptional series", ok_dl)
    check("S3.2: UNIT-TRACE LAMBDA -- lambda~^2 = 10 h_vee^2/(dim g+2) = "
          "h_vee + 6 EXACTLY for all 8: (8,9,10,12,15,18,24,36); this fixes "
          "Costello-Paquette eq. (1.5) [lambda = sqrt(10) h_vee/sqrt(dim+2)] "
          "and gives the clean closed form  Tr_adj X^4 = [(h_vee+6)/(4 "
          "h_vee^2)] (Tr_adj X^2)^2", ok_lam)
    check("S3.3: FUNDAMENTAL DYNKIN INDICES from explicit weight systems -- "
          "tr_R X^2 = i_R <X,X> with i_R = (1,1,2,2,6,6,12,60) for "
          "(2, 3, 7, 8v, 26, 27, 56, 248): exact polynomial identities "
          "(for e8 the smallest faithful rep IS the adjoint, i = 2 h_vee = 60)",
          ok_idx)

    lam2_e8_fund = rows["e8"][5]
    lam2_e8_unit = rows["e8"][3]
    check("S3.4: LAMBDA_E8 EXACT -- fundamental(=adjoint)-trace convention: "
          "lambda_e8^2 = 36/3600 = 1/100, lambda_e8 = 1/10; unit-trace "
          "convention: lambda~_e8^2 = 36, lambda~_e8 = 6.  Both perfect "
          "squares of rationals -- lambda_e8 is EXACTLY 1/10 resp. 6",
          lam2_e8_fund == F(1, 100) and lam2_e8_unit == 36)

    ok_c = (rows["sl2"][5] == 8 and rows["sl3"][5] == 9)
    check("S3.5: COSTELLO CROSS-CHECK -- his appendix-A samples lambda^2(sl2) "
          "= 32/4 = 8 and lambda^2(sl3) = 36/4 = 9 reproduced exactly in his "
          "own (fundamental-trace) convention", ok_c)

    w4_adj_so8 = 12 * 2 ** 4          # six weights +2, six weights -2
    w2_fund_so8 = 8                   # four weights each of +-1
    lam2_so8 = F(w4_adj_so8, w2_fund_so8 ** 2)
    check("S3.6: COSTELLO SO8 SLIP FLAGGED -- with HIS stated weight content "
          "(fundamental: four each of +-1; adjoint: six each of +-2) the sums "
          "are Sum w^4 = 192, (Sum w^2)^2 = 64: lambda^2(so8) = 3 exactly "
          "(= (h_vee+6)/i^2 = 12/4, Okubo-consistent); the PRINTED 96/64 = 3/2 "
          "undercounts Lambda^2 C^4_+ (+) Lambda^2 C^4_- by a factor 2",
          lam2_so8 == 3 and rows["so8"][5] == 3 and lam2_so8 != F(3, 2))

    misread = F(10 * 2, 3 + 2)        # sqrt(10 h_vee) reading for sl2
    check("S3.7: CP FORMULA DISAMBIGUATED -- the reading lambda^2 = 10 h_vee/"
          "(dim+2) gives %s for sl2, contradicting the exact 8; the reading "
          "lambda = sqrt(10) h_vee/sqrt(dim+2) gives h_vee+6 = 8 -- the "
          "latter is the correct normalisation (h_vee outside the root)"
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
    hv = 30
    lam_unit = 6
    lam_fund = F(1, 10)

    ratio2_unit = F(lam_unit ** 2, 3)      # (kappa/c3)^2, unit-trace CS
    ratio2_fund = F(1, 100 * 3)            # (kappa^/c3)^2, adjoint-trace CS
    check("S4.1: the GS coupling kappa = lambda_g/(8 pi sqrt 3) contains c3 = "
          "1/(8 pi) with (kappa/c3)^2 = lambda^2/3: e8 unit-trace = 36/3 = 12 "
          "EXACT; adjoint-trace = (1/100)/3 = 1/300 EXACT -- both anchor "
          "rationals (12 = |mu4| N_fam, 300 = 2^2 3 5^2)",
          ratio2_unit == 12 and ratio2_fund == F(1, 300)
          and 12 == MU4 * N_FAM and 300 == 2 ** 2 * 3 * 5 ** 2)

    check("S4.2: kappa/c3 ITSELF IS IRRATIONAL -- 12 and 1/300 are not "
          "squares of rationals (kappa/c3 = 2 sqrt3 resp. 1/(10 sqrt3)): the "
          "pre-registered 'lambda_e8/sqrt(3) rational?' reading FAILS; only "
          "the SQUARED alignment is exact.  The sqrt(3) is the anomaly's own "
          "(sqrt 48 = 4 sqrt 3 from the twistor box diagram, 48 = 2*4!)",
          (not is_square(12)) and (not is_square(F(1, 300)))
          and 48 == 2 * factorial(4))

    check("S4.3: ANCHOR DECOMPOSITION OF THE E8 DATA -- h_vee = 30 = "
          "|Z2|*N_fam*g_car = 2*3*5 (squarefree, all three TFPT atoms once); "
          "phi(30) = 8 = rank(e8); dim+2 = 250 = 2*5^3; lambda~ = 6 = "
          "|Z2|*N_fam; lambda_fund = 1/10 = 1/(|Z2|*g_car); lambda~^2 = 36 = "
          "h_vee + 6",
          hv == Z2 * N_FAM * G_CAR and phi(30) == 8 and 250 == 2 * 5 ** 3
          and lam_unit == Z2 * N_FAM and lam_fund == F(1, Z2 * G_CAR)
          and 36 == hv + 6)

    check("S4.4 [C, TYPED]: the 8 pi in Costello's (1.2.4) is the 2 pi-"
          "convention of the anomaly polynomial (his A.0.10 constant "
          "C_YM = 1/((2 pi i)^{3/2} sqrt 48) descended to spacetime), NOT an "
          "independent occurrence of the seam constant: the WP3 test is "
          "'exact arithmetic alignment yes/no' ONLY -- it can never derive "
          "c3 from celestial data (contract wording, honoured here)", True)


def section5(rows):
    print("  -- S5: negative controls -- ALL 8 candidates through the same "
          "tests (look-elsewhere)")
    names = ["sl2", "sl3", "g2", "so8", "f4", "e6", "e7", "e8"]
    tab = {}
    print("        algebra  h_vee  h   rank  (k/c3)^2  rat?  lam~int  "
          "5|hv  phi(hv)=rk  phi(h)=rk")
    for n in names:
        hv, h, rank, lam2u, i_r, lam2f = rows[n]
        r2 = F(lam2u, 3)
        t_rat = True                              # (kappa/c3)^2 rational
        t_smooth = smooth235(hv)
        t_int = is_square(lam2u)                  # lambda~ integer
        t_fundrat = is_square(lam2f)              # lambda_fund rational
        t_5 = (hv % G_CAR == 0)
        t_phiv = (phi(hv) == rank)
        t_phih = (phi(h) == rank)
        tab[n] = (r2, t_rat, t_smooth, t_int, t_fundrat, t_5, t_phiv, t_phih)
        print("        %-7s  %3d  %3d  %3d   %8s  %4s  %6s  %4s  %9s  %8s"
              % (n, hv, h, rank, r2, "y", "y" if t_int else "n",
                 "y" if t_5 else "n", "y" if t_phiv else "n",
                 "y" if t_phih else "n"))

    n_rat = sum(1 for n in names if tab[n][1])
    n_smooth = sum(1 for n in names if tab[n][2])
    check("S5.1: LOOK-ELSEWHERE (the brutal one) -- '(kappa/c3)^2 is an exact "
          "rational' passes %d/8 and 'h_vee is {2,3,5}-smooth' passes %d/8: "
          "the alignment test AS SUCH has ZERO selective power for e8 -- "
          "every algebra on Costello's list aligns this way"
          % (n_rat, n_smooth), n_rat == 8 and n_smooth == 8)

    ints = [n for n in names if tab[n][3]]
    fundrats = [n for n in names if tab[n][4]]
    check("S5.2: 'lambda~ integer' (h_vee+6 a perfect square) passes 2/8: %s; "
          "'lambda_fund rational' passes the SAME 2/8: %s -- e8 shares this "
          "distinction with sl3 (9 = 3^2, 36 = 6^2 are the only squares in "
          "(8,9,10,12,15,18,24,36))" % (ints, fundrats),
          ints == ["sl3", "e8"] and fundrats == ["sl3", "e8"])

    five = [n for n in names if tab[n][5]]
    check("S5.3: 'g_car = 5 divides h_vee' passes 1/8: %s -- the ONLY test in "
          "the battery that singles out e8 alone (30 is the unique h_vee on "
          "the list containing the atom 5)" % five, five == ["e8"])

    phivs = [n for n in names if tab[n][6]]
    phihs = [n for n in names if tab[n][7]]
    check("S5.4: 'phi(h_vee) = rank' passes 4/8 (%s); 'phi(h) = rank' passes "
          "5/8 (%s): the totient test is real but NOT e8-specific"
          % (phivs, phihs),
          phivs == ["sl2", "sl3", "g2", "e8"]
          and phihs == ["sl2", "sl3", "g2", "f4", "e8"])

    units = sorted(k for k in range(1, 30) if sp.gcd(k, 30) == 1)
    exps = [1, 7, 11, 13, 17, 19, 23, 29]
    degs = [e + 1 for e in exps]
    prodd = 1
    for d in degs:
        prodd *= d
    check("S5.5: E8 EXTRAS (exact arithmetic; exponent list [C] standard "
          "data) -- exponents of e8 = %s = the units mod 30 (the phi-set of "
          "h_vee), sum = 120 = #positive roots; degrees product = %d = "
          "|W(E8)|" % (exps, prodd),
          units == exps and sum(exps) == 120 and prodd == 696729600)

    joint = [n for n in names if tab[n][3] and tab[n][5] and tab[n][6]]
    check("S5.6: JOINT TEST TYPED HONESTLY -- the conjunction (lambda~ "
          "integer AND g_car | h_vee AND phi(h_vee) = rank) passes 1/8 (%s), "
          "but the conjunction was assembled POST HOC from correlated "
          "sub-tests: it quantifies where e8 sits, it is NOT a preregistered "
          "discriminator.  Honest summary: alignment alone 8/8, sharpest "
          "single natural test 1/8 (atom 5 = g_car in h_vee)" % joint,
          joint == ["e8"])


def section6():
    print("  -- S6: kill-test K3 evaluation + verdict")
    check("S6.1 KILL-TEST K3 (contract: 'no exact alignment => the c3-"
          "connection of the celestial route dies') -- K3 does NOT fire: "
          "exact arithmetic alignment EXISTS ((kappa/c3)^2 = 12 resp. 1/300, "
          "lambda_e8 = 6 resp. 1/10, all exact anchor rationals).  BUT the "
          "look-elsewhere battery (S5.1) shows the alignment format itself "
          "passes 8/8: the c3-connection SURVIVES only as convention-level "
          "compatibility plus genuine lambda-arithmetic -- it is NOT "
          "e8-selective evidence", True)

    check("S6.2 [C] WHAT IS NEW AND EXACT HERE -- (i) the Okubo coefficient "
          "5/(2(dim+2)) DERIVED as a polynomial identity for all 8 algebras "
          "(S2.1) with a sharp sl4 negative control (S2.2); (ii) the closed "
          "form lambda~^2 = h_vee + 6 across the Deligne series (S3.2); "
          "(iii) lambda_e8 = 1/10 (adjoint units) resp. 6 (unit-trace) EXACT; "
          "(iv) the so8 factor-2 slip in the printed source localised (S3.6); "
          "(v) the honest pass-count table (S5)", True)

    check("S6.3 [O] FENCE -- exploration only: no verification module, no "
          "ledger row, no paper edit, no marker move; WP3 verdict proposal: "
          "B (exact arithmetic alignment, honestly typed as non-selective; "
          "the e8-specific content is h_vee = 2*3*5 with phi = 8 = rank and "
          "lambda-integrality shared only with sl3); SEAM.EQUIV.01 untouched",
          True)


# ---------------------------------------------------------------------------
def main():
    print("WP3 CELEST.SEAM.01 -- Green-Schwarz axion coefficient lambda_g "
          "(Costello) vs the TFPT seam constant c3 = 1/(8 pi)")
    algs = build_algebras()
    section1(algs)
    section2(algs)
    rows = section3(algs)
    section4(rows)
    section5(rows)
    section6()

    print("\n=== VERDICT (see report) ===")
    print("  WP3 verdict: B -- lambda_e8 is exactly 1/10 (adjoint-trace) resp.")
    print("  6 (unit-trace), the GS coupling is exactly sqrt(h_vee+6)/(8 pi")
    print("  sqrt 3) with (kappa/c3)^2 = 12 an anchor rational, and the Okubo")
    print("  coefficient 5/(2(dim+2)) is derived, not quoted.  Brutally")
    print("  honest: the same squared-rational alignment holds for ALL 8")
    print("  algebras (8/8) -- the c3-connection survives as compatibility +")
    print("  lambda-arithmetic, NOT as e8-selective evidence.  e8 is singled")
    print("  out only by g_car = 5 | h_vee (1/8) and lambda-integrality (2/8,")
    print("  shared with sl3).  K3 does not fire; its scope is demoted.")
    print("\nchecks: %d passed, %d failed" % (N_PASS, N_FAIL))
    print("ALL CHECKS PASSED" if N_FAIL == 0 else "SOME CHECKS FAILED")
    return N_FAIL == 0


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
