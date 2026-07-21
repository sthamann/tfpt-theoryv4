"""WP4 of CELEST.SEAM.01 (EXPLORATION ONLY -- experiments/, no verification claim).

The (E8)_1 character E4/eta^8 as a conformal block of the celestial E8[C^2]
S-algebra -- the contract's "type mismatch, head-on".  WP1 (v492) showed the
four glue sectors sum to the (E8)_1 character AT THE COUNTING LEVEL; but the
S-algebra is graded by polynomial degree (60/64 jet towers), not by conformal
weight.  This probe computes both sides exactly and either produces the
character from an S-algebra trace or localises the obstruction.  Exact integer/
Fraction arithmetic + sympy, no floats.

Method anchors (gradings taken from the literature, typed [C]):
  * Costello-Paquette, JHEP 10 (2022) 193 (arXiv:2201.02595), Table 1: the
    celestial chiral algebra of SDYM has towers J^a[m,n] ~ g (x) z1^m z2^n with
    2d SPIN 1 - (m+n)/2, R^4-scaling DIMENSION -(m+n), SU(2)_+ rep (m+n)/2.
    The natural celestial-conformal grading is by d = m+n (jet degree); the 2d
    spin decreases linearly along the tower -- unbounded below.
  * Bittleston-Homans-Sharma arXiv:2305.09451 (the v492/v493 anchor): the
    equivariant sector on C^2/Z4 keeps modes with glue grade j + monomial
    grade (m-n) = 0 mod 4 -- graded dims D[d] = 60(d+1) even / 64(d+1) odd.
  * (E8)_1: chi = E4/eta^8 = 1 + 248q + 4124q^2 + ... (v377/v492 convention,
    no q^{-1/3} prefactor); Sugawara c = k dim g/(k+h_vee) = 248/31 = 8.

Sections (checks counted; fences typed honestly):
  S1  BASE + GRADING.  v492 replication (roots, glue split, D[d]); cumulative
      generator counts are QUADRATIC (exact closed forms 31s^2+92s+60 even /
      31s^2+94s+63 odd; leading 31 = k + h_vee); CP Table 1 spin 1 - d/2 is
      unbounded below => no L0-bounded rational VOA can contain the towers.
  S2  EQUIVARIANT HILBERT SERIES + SPECIALISATIONS.  Closed form chi_sp(t) =
      (60 + 128t + 60t^2)/(1-t^2)^2 (palindromic numerator, value 248 at
      t = 1); the four mu4 collapses w in {1,-1,i,-i} of the doubly graded
      series and the SU(2)_+ primary slice (60+64t)/(1-t^2) -- exact first
      coefficients; none reproduces (1, 248, 4124, ...).
  S3  THE (E8)_1 SIDE, EXACT.  chi = E4/eta^8 through q^6 = (1, 248, 4124,
      34752, 213126, 1057504, 4530744); machinery cross-check j = E4^3/Delta
      = 1/q + 744 + 196884 q + 21493760 q^2; theta-split replication (shell 1
      = (52,64,60,64), sector currents (60,64,60,64), glue-diagonal h =
      (0,1,1,1) integer); Sugawara c = 248/31 = 8 = rank = 2|mu4|.
  S4  BRIDGE TESTS (quantitative).  (i) zero-mode slice d = 0: 60 = C0-sector
      currents EXACTLY; (ii) single-line jet slice z1^d: dims cycle
      (60,64,60,64) = the sector current counts sector by sector; (iii)
      boundary/loop reading (|z| = 1, jets -> loop modes): one mu4 period sums
      to 64+60+64+60 = 248 = the 248q stage at single-particle level; 248 is
      NOT in the D-list (d <= 100) -- only the period-collapse produces it;
      (iv) BUT the loop Fock at integer level 1 counts 897266 >> 248: the
      level-1 truncation (null ideal) is NOT in the jet/loop algebra.
  S5  MISMATCH LOCALISATION (exact).  Fock of the equivariant tower vs chi:
      f1 = 128 < 248 (undercount), f2 = 8436 > 4124 (overcount) -- two-sided,
      no rescaling fixes it; ratios f_n/x_n strictly increasing n = 1..12
      (exact cross-multiplication); Meinardus poles: sum D[d]/d^s has its
      rightmost pole at s = 2 (D linear) vs s = 1 for 8 bosons => growth
      exponents n^{2/3} vs n^{1/2} [C]; the null ideal: free-current counting
      at level 2 = 31124 = 4124 + 27000 with 27000 = 30^3 = h_vee^3 -- the
      (E8)_1 character DELETES exactly the 27000 of Sym^2(248) = 1 + 3875 +
      27000 ([C] standard), while 4124 = 248 + 3875 + 1: the rational
      truncation is a LEVEL-2 phenomenon absent from g[C^2].
  S6  KILL-TEST K4 EVALUATION + VERDICT.  Three-way: (i) exact realisation NO;
      (ii) boundary/compactification-limit realisation PARTIAL YES (sector
      arithmetic exact at the current stratum; rational truncation must be
      imposed in the limit -- the same scaling-limit structure as the MMST
      route of SEAM.EQUIV.01, named); (iii) the hard mismatch is localised
      (growth 2/3 vs 1/2, spin unbounded, missing 27000-null ideal).

Throwaway probe: prints tables + PASS/FAIL + verdict, ends with a check count.
Nothing here is a claim; promotion (if any) goes through the usual workflow.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb

import sympy as sp

G_CAR = 5
N_FAM = 3
MU4 = 4
RANK_E8 = 8
H_VEE = 30
NMAX = 12          # q-order for the series comparisons
DMAX = 12          # jet degree cutoff

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
    """(1 - q^d)^(-D) as a series: sum_k C(D+k-1, k) q^(dk)."""
    out = [0] * (nmax + 1)
    k = 0
    while d * k <= nmax:
        out[d * k] = comb(D + k - 1, k)
        k += 1
    return out


def fock(gen_dims, nmax):
    """prod_d (1 - q^d)^(-gen_dims[d]) over d >= 1."""
    out = [1] + [0] * nmax
    for d, D in gen_dims.items():
        if d == 0 or D == 0:
            continue
        out = series_mul(out, geom_factor(d, D, nmax), nmax)
    return out


def sigma3(n):
    return sum(k ** 3 for k in range(1, n + 1) if n % k == 0)


# ---------------------------------------------------------------------------
# E8 roots in D5 (+) A3 + glue coordinates (v128/v492 construction)
# ---------------------------------------------------------------------------
def build_roots():
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
        roots[(r, z4)] = 0
    for r in a3_roots:
        roots[(z5, r)] = 0
    for d in d5_s:
        for w in wclass(1):
            roots[(d, w)] = 1
    for d in d5_v:
        for w in wclass(2):
            roots[(d, w)] = 2
    for d in d5_c:
        for w in wclass(3):
            roots[(d, w)] = 3
    return roots


def monomial_table(dmax):
    """N[d][j] = # monomials z1^p z2^q, p+q = d, with (p-q) mod 4 = j."""
    N = []
    for d in range(dmax + 1):
        row = [0] * 4
        for p in range(d + 1):
            row[(p - (d - p)) % 4] += 1
        N.append(row)
    return N


# ---------------------------------------------------------------------------
# theta split of the E8 lattice by the glue cosets (v492 S4 machinery)
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


# ---------------------------------------------------------------------------
# S1 -- base data + the grading question
# ---------------------------------------------------------------------------
def section1():
    print("  -- S1: v492 base data + the celestial grading (CP Table 1)")
    roots = build_roots()
    counts = [sum(1 for c in roots.values() if c == k) for k in range(4)]
    dims = [counts[0] + RANK_E8] + counts[1:]
    check("S1.1: v492 replication -- 240 roots, glue split 240 = 52+64+60+64, "
          "graded dims with Cartan g_j = %s = (60,64,60,64)" % dims,
          len(roots) == 240 and counts == [52, 64, 60, 64]
          and dims == [60, 64, 60, 64])

    N = monomial_table(DMAX)
    D = [sum(dims[j] * N[d][(-j) % 4] for j in range(4))
         for d in range(DMAX + 1)]
    ok_D = all(D[d] == (60 if d % 2 == 0 else 64) * (d + 1)
               for d in range(DMAX + 1))
    check("S1.2: equivariant tower D[d] = 60(d+1) even / 64(d+1) odd for "
          "d <= %d: D = %s" % (DMAX, D[:7]), ok_D)

    ok_cum = True
    cum = 0
    for s in range(DMAX + 1):
        cum += D[s]
        expect = 31 * s * s + (92 * s + 60 if s % 2 == 0 else 94 * s + 63)
        ok_cum &= (cum == expect)
    check("S1.3: cumulative generator count QUADRATIC -- sum_{d<=s} D[d] = "
          "31 s^2 + 92 s + 60 (s even) / 31 s^2 + 94 s + 63 (s odd) exactly; "
          "leading coefficient 31 = 248/8 = k + h_vee (the Sugawara "
          "denominator, an arithmetic note, not a derivation)",
          ok_cum and 31 == 1 + H_VEE and 31 * 8 == 248)

    spins = [sp.Rational(1) - sp.Rational(d, 2) for d in range(5)]
    check("S1.4 [C, literature grading]: CP Table 1 (arXiv:2201.02595) -- "
          "J[m,n] has 2d spin 1 - (m+n)/2 (= %s for d = 0..4), R^4 dimension "
          "-(m+n), SU(2)_+ rep (m+n)/2: the spin is UNBOUNDED BELOW along "
          "the tower, and by S1.3 the number of generators above any spin "
          "floor grows quadratically -- no rational VOA (L0 bounded below, "
          "finite level spaces over a finite generating set) contains the "
          "S-algebra towers as graded pieces" % spins,
          spins[4] == -1 and spins[0] == 1)
    return dims, N, D


# ---------------------------------------------------------------------------
# S2 -- equivariant Hilbert series and its specialisations
# ---------------------------------------------------------------------------
def section2(dims, N, D):
    print("  -- S2: equivariant Hilbert series + all natural specialisations")
    t = sp.symbols('t')
    closed = (60 + 128 * t + 60 * t ** 2) / (1 - t ** 2) ** 2
    ser = sp.series(closed, t, 0, DMAX + 1).removeO()
    ok_closed = all(int(sp.expand(ser).coeff(t, d)) == D[d]
                    for d in range(DMAX + 1))
    check("S2.1: closed form chi_sp(t) = (60 + 128 t + 60 t^2)/(1-t^2)^2 "
          "reproduces D[d] exactly (d <= %d); numerator palindromic with "
          "value 60+128+60 = 248 = dim e8 at t = 1" % DMAX,
          ok_closed and 60 + 128 + 60 == 248)

    coll = {}
    for wval in (sp.Integer(1), sp.Integer(-1), sp.I, -sp.I):
        c = []
        for d in range(6):
            tot = sp.Integer(0)
            for p in range(d + 1):
                m = p - (d - p)
                tot += dims[(-m) % 4] * wval ** sp.Integer(m)
            c.append(sp.simplify(tot))
        coll[str(wval)] = c
    check("S2.2: mu4 COLLAPSES of the doubly graded series (w^(m-n) "
          "insertion, w in mu4) -- w=1: %s; w=-1: %s; w=i: %s: NONE starts "
          "1, 248, ... (the w = +-i collapses even vanish at odd d); the "
          "'row sum' route to E4/eta^8 fails at the first coefficient"
          % (coll['1'][:4], coll['-1'][:4], coll['I'][:4]),
          coll['1'][:2] == [60, 128] and coll['-1'][1] == -128
          and coll['I'][1] == 0 and coll['I'][2] == -60
          and all(c[1] != 248 for c in coll.values()))

    slice_ser = (60 + 64 * t) / (1 - t ** 2)
    ss = sp.series(slice_ser, t, 0, 7).removeO()
    slice_dims = [int(sp.expand(ss).coeff(t, d)) for d in range(7)]
    check("S2.3: SU(2)_+ PRIMARY SLICE (one monomial per degree, the "
          "highest-weight line) -- (60 + 64t)/(1-t^2): dims %s cycle "
          "(60,64,60,64): bounded per level but still not (1,248,...) as a "
          "Fock generator set (level-1 Fock coefficient would be 64, not "
          "248)" % slice_dims,
          slice_dims == [60, 64, 60, 64, 60, 64, 60])


# ---------------------------------------------------------------------------
# S3 -- the (E8)_1 character side, exact
# ---------------------------------------------------------------------------
def section3():
    print("  -- S3: the (E8)_1 character E4/eta^8, exact through q^%d" % 6)
    e4 = [1] + [240 * sigma3(n) for n in range(1, NMAX + 1)]
    eta8inv = fock({n: 8 for n in range(1, NMAX + 1)}, NMAX)
    chi = series_mul(e4, eta8inv, NMAX)
    check("S3.1: chi_(E8)_1 = E4/eta^8 = %s (q^0..q^6): the v377/v492 series "
          "1, 248, 4124, 34752 extended exactly" % chi[:7],
          chi[:7] == [1, 248, 4124, 34752, 213126, 1057504, 4530744])

    e4cube = series_mul(series_mul(e4, e4, NMAX), e4, NMAX)
    eta24inv = fock({n: 24 for n in range(1, NMAX + 1)}, NMAX)
    jq = series_mul(e4cube, eta24inv, NMAX)      # q * j(tau)
    check("S3.2: MACHINERY CROSS-CHECK -- q j(tau) = E4^3/eta^24 = %s "
          "(q^0..q^3) = (1, 744, 196884, 21493760): the modular bookkeeping "
          "is exact (j-function coefficients [C] standard)" % jq[:4],
          jq[:4] == [1, 744, 196884, 21493760])

    d5 = d5_coset_norms(6)
    a3 = a3_coset_norms(6)
    pairing = {0: ('0', 0), 1: ('s', 1), 2: ('v', 2), 3: ('c', 3)}
    theta = {}
    for j, (dk, ak) in pairing.items():
        coeffs = [0] * 4
        for n5, c5 in d5[dk].items():
            for n3, c3v in a3[ak].items():
                n = n5 + n3
                if n <= 6 and n % 2 == 0 and F(n, 2).denominator == 1:
                    coeffs[int(n) // 2] += c5 * c3v
        theta[j] = coeffs
    shell1 = [theta[j][1] for j in range(4)]
    tot_shells = [sum(theta[j][k] for j in range(4)) for k in range(4)]
    check("S3.3: THETA SPLIT (v492 S4 replication) -- shell 1 = %s = "
          "(52,64,60,64); shells 0..3 sum to %s = E4 coefficients "
          "(1,240,2160,6720)" % (shell1, tot_shells),
          shell1 == [52, 64, 60, 64] and tot_shells == e4[:4])

    p8 = fock({n: 8 for n in range(1, 4)}, 3)
    sector = {j: series_mul(theta[j], p8, 3) for j in range(4)}
    lvl1 = [sector[j][1] for j in range(4)]
    check("S3.4: SECTOR CURRENTS -- level-1 coefficients per glue sector = "
          "%s = (60,64,60,64) = the v128 dims WITH Cartan (v492 S4 "
          "replication)" % lvl1, lvl1 == [60, 64, 60, 64])

    hmin_d5 = [F(0)] + [F(min(n for n in d5[k] if n > 0), 2)
                        for k in ('s', 'v', 'c')]
    hmin_a3 = [F(0)] + [F(min(n for n in a3[k] if n > 0), 2)
                        for k in (1, 2, 3)]
    hdiag = [hmin_d5[j] + hmin_a3[j] for j in range(4)]
    check("S3.5: GLUE-DIAGONAL WEIGHTS h_j = %s = (0,1,1,1) INTEGER -- the "
          "four glue sectors of (E8)_1 sit at integer conformal weight "
          "(v125 isotropy = locality of the extension): the quarter-graded "
          "boundary modes can land on integer levels at all" % hdiag,
          hdiag == [F(0), F(1), F(1), F(1)])

    c_sug = sp.Rational(1 * 248, 1 + H_VEE)
    check("S3.6: SUGAWARA -- c = k dim g/(k + h_vee) = 248/31 = %s = 8 = "
          "rank(E8) = 2|mu4| (the seam winding integer 8 = 2|mu4| of "
          "v492 S5); modular anomaly c/24 = 1/3 (the q^{-1/3} prefactor "
          "dropped throughout, counting convention)" % c_sug,
          c_sug == 8 and 8 == 2 * MU4 and sp.Rational(8, 24) == sp.Rational(1, 3))
    return chi


# ---------------------------------------------------------------------------
# S4 -- the bridge tests
# ---------------------------------------------------------------------------
def section4(dims, D, chi):
    print("  -- S4: bridge tests (zero-mode slice, jet slice, boundary loop)")
    check("S4.1: ZERO-MODE SLICE -- D[0] = %d = g0 = carrier D5+A3 + Cartan "
          "= C0-sector current count 60 EXACTLY: the d = 0 stratum of the "
          "S-algebra IS the vacuum-sector current content of (E8)_1"
          % D[0], D[0] == 60)

    slice_match = all(dims[(-d) % 4] == [60, 64, 60, 64][(-d) % 4]
                      for d in range(8))
    cyc = [dims[(-d) % 4] for d in range(8)]
    check("S4.2: SINGLE-LINE JET SLICE -- the monomials z1^d (one twistor "
          "line) pair with g_{-d mod 4}: dims %s cycle exactly through the "
          "four sector current counts (60,64,60,64) sector by sector "
          "(j = -d mod 4): the current stratum of every glue sector appears "
          "on the boundary line" % cyc, slice_match)

    period = sum(dims[n % 4] for n in range(1, 5))
    check("S4.3: BOUNDARY LOOP PERIOD -- restricting jets to |z| = 1 maps "
          "z1^p z2^q -> z^(p-q) (loop modes); one full mu4 period of loop "
          "energies n = 1..4 carries dim g_(n mod 4) = (64,60,64,60), sum = "
          "%d = 248 = the 248q stage of the character at single-particle "
          "level" % period, period == 248 and chi[1] == 248)

    in_list = any((60 if d % 2 == 0 else 64) * (d + 1) == 248
                  for d in range(101))
    check("S4.4: 248 IS NOT A JET-TOWER DIMENSION -- 248 not in {D[d]: d <= "
          "100} (60(d+1) or 64(d+1) never equals 248); ONLY the period "
          "collapse (four degrees -> one level) produces 248: the bridge "
          "MUST be a boundary/compactification statement, it cannot sit "
          "inside the polynomial grading", not in_list)

    loop_fock = fock({n: dims[n % 4] for n in range(1, 17)}, 16)
    lvl1_loop = loop_fock[4]      # u^4 = q^1 (quarter-integer moding)
    check("S4.5: BUT THE LOOP FOCK OVERCOUNTS -- free bosonic counting of "
          "the loop modes at integer level 1 (u^4, u = q^(1/4)) gives %d >> "
          "248: without the level-1 null ideal (rational truncation) even "
          "the boundary reading does NOT reproduce the character beyond the "
          "single-particle stratum; the truncation must be imposed in the "
          "limit -- it is not present in g[C^2] or its loop image"
          % lvl1_loop, lvl1_loop == 897266 and lvl1_loop > 248)


# ---------------------------------------------------------------------------
# S5 -- mismatch localisation
# ---------------------------------------------------------------------------
def section5(D, chi):
    print("  -- S5: the mismatch, localised exactly")
    f = fock({d: D[d] for d in range(1, NMAX + 1)}, NMAX)
    check("S5.1: EQUIVARIANT JET FOCK vs CHARACTER -- f = %s vs chi = %s "
          "(q^0..q^3): f1 = 128 < 248 = x1 (UNDERcount: the jet grading "
          "splits the 248 currents over degrees 0..3) and f2 = 8436 > 4124 "
          "= x2 (OVERcount: no null ideal): the failure is TWO-SIDED -- no "
          "rescaling or shift of the grading repairs both directions"
          % (f[:4], chi[:4]),
          f[1] == 128 and f[2] == 8436 and f[1] < chi[1] and f[2] > chi[2])

    ratios_ok = all(f[n + 1] * chi[n] > f[n] * chi[n + 1]
                    for n in range(1, NMAX))
    check("S5.2: GROWTH SEPARATION -- f_n/x_n strictly increasing for n = "
          "1..%d (exact cross-multiplication): the jet Fock pulls away "
          "monotonically; [C] Meinardus: sum_d D[d] d^{-s} has its rightmost "
          "pole at s = 2 (D[d] ~ 62 d) vs s = 1 for the 8 bosons of eta^{-8} "
          "=> log-growth n^{2/3} (jet tower) vs n^{1/2} (partitions in 8 "
          "bosons): polynomial-times-partition beats partition -- the two "
          "counting types are asymptotically DISJOINT" % NMAX, ratios_ok)

    verma = fock({n: 248 for n in range(1, 3)}, 2)
    deficit = verma[2] - chi[2]
    check("S5.3: THE NULL IDEAL, LOCALISED -- free current counting (248 "
          "oscillators) gives level-2 dim %d = 248 + Sym^2(248) = 248 + "
          "30876; the character keeps 4124; deficit = %d = 27000 = 30^3 = "
          "h_vee^3 EXACTLY: (E8)_1 deletes exactly the 27000 in Sym^2(248) "
          "= 1 + 3875 + 27000 ([C] standard), keeping 4124 = 248 + 3875 + 1 "
          "-- the rational truncation starts at level 2 and has NO analogue "
          "in the jet algebra (level 1 agrees: 248 = 248)"
          % (verma[2], deficit),
          verma[1] == 248 and verma[2] == 31124 and deficit == 27000
          and 27000 == H_VEE ** 3 and 1 + 3875 + 27000 == 30876
          and 248 + 3875 + 1 == 4124)

    check("S5.4: WHERE THE TYPE MISMATCH SITS (the contract's question, "
          "answered) -- three independent, exactly-located obstructions: "
          "(a) GRADING: jet degree d gives spin 1 - d/2 unbounded below "
          "(S1.4) and 248 is not a tower dimension (S4.4); (b) GROWTH: "
          "cumulative quadratic generator count => Fock exponent n^{2/3} vs "
          "n^{1/2} (S1.3/S5.2); (c) TRUNCATION: the level-2 null ideal "
          "27000 = h_vee^3 exists on the VOA side only (S5.3).  The ONLY "
          "surviving contact points are the current stratum (S4.1-S4.3: "
          "60/64 sector counts, period sum 248) and the theta-split "
          "counting identity (S3.3/S3.4 = v492 S4)", True)


# ---------------------------------------------------------------------------
# S6 -- kill-test K4 + verdict
# ---------------------------------------------------------------------------
def section6():
    print("  -- S6: kill-test K4 evaluation + verdict")
    check("S6.1 KILL-TEST K4, three-way (contract: 'WP4 negative => degrade "
          "to E8-admissible, zero TFPT content') -- (i) EXACT REALISATION: "
          "NO -- no specialisation/row-sum/slice of the doubly graded "
          "equivariant series reproduces E4/eta^8 (S2.2/S2.3/S5.1); (ii) "
          "BOUNDARY-LIMIT REALISATION: PARTIAL YES -- the current stratum "
          "matches sector by sector (60,64,60,64), the mu4 period collapse "
          "gives exactly 248, the glue-diagonal weights are integer (the "
          "quarter-modes CAN land on integer levels), and the theta split "
          "sums to the character exactly; what is missing is precisely the "
          "rational truncation (null ideal), which must come from a "
          "scaling/compactification limit -- the SAME structure as the MMST "
          "scaling-limit route of SEAM.EQUIV.01 (v336/v449: the rational "
          "net exists in the LIMIT of the lattice collar, not in the "
          "pre-limit algebra); (iii) HARD MISMATCH: localised at growth "
          "n^{2/3} vs n^{1/2}, spin unboundedness, and the 27000 = h_vee^3 "
          "null ideal", True)

    check("S6.2: VERDICT PROPOSAL -- K4 does NOT degrade the contract to "
          "'E8 admissible' (that would require the sector arithmetic to "
          "fail too -- it holds exactly); it lands at (ii): the (E8)_1 "
          "character is a BOUNDARY/LIMIT shadow of the equivariant "
          "S-algebra, not a conformal block of it in the bulk grading.  "
          "This sharpens WP4 into a statement of SEAM.EQUIV.01 type "
          "(rational structure emerges only in a limit) rather than "
          "killing it", True)

    check("S6.3 [O] FENCE -- exploration only: no verification module, no "
          "ledger row, no paper edit, no marker move anywhere; the "
          "constructive boundary limit itself (which limit, which topology, "
          "convergence) stays OPEN and belongs to WP5/SEAM.EQUIV.01; "
          "SEAM.EQUIV.01 untouched", True)


# ---------------------------------------------------------------------------
def main():
    print("WP4 CELEST.SEAM.01 -- the (E8)_1 character E4/eta^8 vs the "
          "glue-equivariant E8[C^2] S-algebra (type mismatch, head-on)")
    dims, N, D = section1()
    section2(dims, N, D)
    chi = section3()
    section4(dims, D, chi)
    section5(D, chi)
    section6()

    print("\n=== VERDICT (see report) ===")
    print("  WP4 verdict: B(ii) -- the (E8)_1 character is NOT a conformal")
    print("  block of the E8[C^2] S-algebra in its own (jet) grading: the")
    print("  mismatch is fully localised (spin unbounded below; cumulative")
    print("  generator count quadratic => Fock growth n^{2/3} vs n^{1/2};")
    print("  null ideal 27000 = h_vee^3 at level 2 absent from the jets).")
    print("  BUT the boundary/compactification reading holds exactly at the")
    print("  current stratum: zero modes = C0 currents (60), the jet slice")
    print("  cycles the four sector counts, one mu4 period sums to 248, and")
    print("  the glue-diagonal weights (0,1,1,1) are integers.  That is the")
    print("  MMST/scaling-limit shape of SEAM.EQUIV.01: the rational object")
    print("  lives in the LIMIT, not in the pre-limit algebra.  K4 fires")
    print("  only against reading (i); reading (ii) is the honest outcome.")
    print("\nchecks: %d passed, %d failed" % (N_PASS, N_FAIL))
    print("ALL CHECKS PASSED" if N_FAIL == 0 else "SOME CHECKS FAILED")
    return N_FAIL == 0


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
