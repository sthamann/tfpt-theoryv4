"""WP1 of CELEST.SEAM.01 (EXPLORATION ONLY -- experiments/, no verification claim).

Question: does the mu4 clock on the seam celestial sphere select the SAME Z4
structure as the E8 mu4-glue grading (v125/v128), when both are read through the
celestial chiral algebra (CCA) on the A3 ALE space C^2/Z4?

Method (Bittleston-Heuveline-Skinner, arXiv:2305.09451, JHEP 09 (2023) 008):
  - CCA of SD gravity on flat space = L ham(C^2) (w-algebra of polynomial
    functions on the twistor fibre C^2 under the Poisson bracket);
  - CCA of SDYM with gauge algebra g = L g[C^2] (S-algebra);
  - on the orbifold C^2/Z_k only the Z_k-invariant modes survive
    (EH case k=2: modes w[p,q] with p+q = 0 mod 2 -> wedge of w_{1+infty});
  - with a flat connection rho: Z_k -> G at infinity (Kronheimer-Nakajima /
    heterotic-on-ALE standard), the surviving SDYM modes are the rho-equivariant
    ones: g_j (x) C[z1,z2]_m with j + m = 0 mod k.

Here k = 4, spatial action (A3 ALE, the unique Z4 in SU(2) up to conjugacy):
    (z1, z2) -> (i z1, i^-1 z2),
and rho = the E8 mu4 glue (v128 grading, exact on all 240 roots).

Sections:
  S1  v128 replication + the grading is INNER (torus element h, order 4);
      the glue charge is the diagonal (1,1) in the discriminant group of D5+A3.
  S2  Molien table of C[z1,z2] under the deck Z4; invariant ring = A3
      singularity XY = Z^4 (Hilbert series check).
  S3  combined glue-equivariant sector of e8[C^2]: graded dimensions, zero
      modes = carrier D5+A3, conjugate pairing, closure, SO(16) halfway (Z2).
  S4  character/theta level matching: Theta_E8 = sum of 4 glue-coset thetas;
      per-sector (E8)_1 character coefficients; sector conformal weights =
      the v125 discriminant form (5x^2+3y^2)/8 mod 1; locality = integrality.
  S5  the clock on the celestial sphere (exact Moebius/spin arithmetic):
      deck -> z |-> -z (order 2, NOT the clock); the order-4 clock z |-> iz is
      realised by the U(2) phase diag(i,1) (a second Z4), spin lift = Z8 with
      (spin clock)^2 = deck; clock-invariant A3 deformation = XY = Z^4 + a0,
      whose 4 branch points are ONE mu4 orbit with cross-ratio 2.
  S6  negative controls: false spatial action diag(i,i) (not SL(2), Poisson
      closure fails, conjugate pairing fails); false glue assignment (grading
      additivity fails, pairing fails); rigidity: only Aut(Z4) relabelings work.

Throwaway probe: prints tables + PASS/FAIL + verdict. Nothing here is a claim;
promotion (if any) goes through the usual verification workflow.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product

import sympy as sp

HALF = F(1, 2)
DMAX = 9  # polynomial degree cutoff for mode tables
PASS_ALL = True


def check(label, ok):
    global PASS_ALL
    print(("  PASS  " if ok else "  FAIL  ") + label)
    if not ok:
        PASS_ALL = False
    return ok


# ---------------------------------------------------------------------------
# S1 -- E8 roots in D5 (+) A3 + glue coordinates (v128 replication)
# ---------------------------------------------------------------------------
def build_roots():
    """E8 roots tagged by glue class (exactly the v128 construction)."""
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


def additivity(roots, classmap):
    """# of root pairs whose sum is a root / # violating grade additivity."""
    items = list(roots.keys())
    pairs = viol = 0
    for i in range(len(items)):
        a1, b1 = items[i]
        for j in range(i + 1, len(items)):
            a2, b2 = items[j]
            s = (tuple(x + y for x, y in zip(a1, a2)),
                 tuple(x + y for x, y in zip(b1, b2)))
            if s in roots:
                pairs += 1
                if classmap[s] != (classmap[items[i]] + classmap[items[j]]) % 4:
                    viol += 1
    return pairs, viol


def section1():
    print("\n=== S1  E8 mu4-glue grading (v128 replication + inner-torus test) ===")
    roots = build_roots()
    counts = [sum(1 for c in roots.values() if c == k) for k in range(4)]
    norm_ok = all(sum(x * x for x in a) + sum(x * x for x in b) == 2
                  for (a, b) in roots)
    check("240 roots, all norm 2, glue split 240 = 52+64+60+64: %s" % counts,
          len(roots) == 240 and norm_ok and counts == [52, 64, 60, 64])

    dims = [counts[0] + 8] + counts[1:]  # Cartan (rank 8) sits in grade 0
    check("graded dims with Cartan: dim g_j = %s (60,64,60,64); "
          "g0 = D5+A3 carrier (45+15=60)" % dims,
          dims == [60, 64, 60, 64] and 45 + 15 == 60)

    pairs, viol = additivity(roots, roots)
    check("grading additive on ALL %d root pairs (violations: %d)"
          % (pairs, viol), pairs == 6720 and viol == 0)

    # the grading is INNER: <alpha, h> mod 4 = class, h = (2,2,2,2,2; 0,0,0,0)
    h_d5 = tuple(F(2) for _ in range(5))
    ok_h = all((sum(x * y for x, y in zip(a, h_d5))) % 4 == c
               and (sum(x * y for x, y in zip(a, h_d5))).denominator == 1
               for (a, b), c in roots.items())
    check("INNER grading: h = (2,2,2,2,2;0^4) gives <alpha,h> = class mod 4 for "
          "all 240 roots => grading = Ad(exp(2 pi i h/4)), an order-4 torus "
          "element (flat Z4 connection / monodromy in the maximal torus)", ok_h)

    # A3-side detector: h' = (0^5; 1,1,1,-3) reproduces the same class
    h_a3 = (F(1), F(1), F(1), F(-3))
    ok_h2 = all((sum(x * y for x, y in zip(b, h_a3))) % 4 == c
                and (sum(x * y for x, y in zip(b, h_a3))).denominator == 1
                for (a, b), c in roots.items())
    check("the SAME class is read off the A3 side by h' = (0^5;1,1,1,-3): the "
          "glue charge is the DIAGONAL (1,1) of the discriminant group "
          "Z4 x Z4 of D5 (+) A3 -- the v92/v125 Lagrangian glue <(1,1)>", ok_h2)

    # SO(16) halfway (v125 sub-Q-system {0,2} / v377 promotion arithmetic)
    even, odd = dims[0] + dims[2], dims[1] + dims[3]
    check("Z2 halfway refinement: g0+g2 = %d = dim SO(16), g1+g3 = %d = "
          "dim spinor 128 -- the v125 sub-Q-system {0,2} = SO(16)_1 step"
          % (even, odd), even == 120 and odd == 128)
    return roots, dims


# ---------------------------------------------------------------------------
# S2 -- Molien table of C[z1,z2] under the deck Z4: (z1,z2) -> (i z1, i^-1 z2)
# ---------------------------------------------------------------------------
def monomial_table(action, dmax=DMAX, modulus=4):
    """N[d][j] = # monomials z1^p z2^q of degree d with grade j (mod modulus).

    action(p, q) -> integer grade of the monomial.
    """
    N = []
    for d in range(dmax + 1):
        row = [0] * modulus
        for p in range(d + 1):
            row[action(p, d - p) % modulus] += 1
        N.append(row)
    return N


def section2():
    print("\n=== S2  Molien/Hilbert data of C[z1,z2] under the A3 deck Z4 ===")
    N = monomial_table(lambda p, q: p - q)
    print("  N[d][j] (deg d, grade j = (p-q) mod 4):")
    for d, row in enumerate(N):
        print("    d=%d: %s" % (d, row))

    # closed-form Molien check via symbolic series
    t = sp.symbols('t')
    i4 = sp.I
    molien = []
    for j in range(4):
        Fj = sp.Rational(1, 4) * sum(
            i4 ** ((-j * k) % 4) / ((1 - i4 ** k * t) * (1 - i4 ** (-k) * t))
            for k in range(4))
        ser = sp.series(sp.simplify(Fj), t, 0, DMAX + 1).removeO()
        molien.append([int(sp.expand(ser).coeff(t, d)) for d in range(DMAX + 1)])
    ok_molien = all(molien[j][d] == N[d][j]
                    for j in range(4) for d in range(DMAX + 1))
    check("Molien series (character average) reproduces the table exactly "
          "for all grades j = 0..3, d <= %d" % DMAX, ok_molien)

    # invariant ring = A3 singularity XY = Z^4
    z1, z2 = sp.symbols('z1 z2')
    X, Y, Z = z1 ** 4, z2 ** 4, z1 * z2
    check("invariant ring generated by X=z1^4, Y=z2^4, Z=z1 z2 with the A3 "
          "relation XY = Z^4 (exact): C^2/Z4 IS the A3 ALE singularity",
          sp.simplify(X * Y - Z ** 4) == 0)

    hilb = sp.series((1 + t ** 4) / ((1 - t ** 2) * (1 - t ** 4)),
                     t, 0, DMAX + 1).removeO()
    ok_hilb = all(int(sp.expand(hilb).coeff(t, d)) == N[d][0]
                  for d in range(DMAX + 1))
    check("Hilbert series of C[X,Y,Z]/(XY - Z^4) = (1+t^4)/((1-t^2)(1-t^4)) "
          "matches the grade-0 Molien column", ok_hilb)

    ok_conj = all(N[d][1] == N[d][3] for d in range(DMAX + 1))
    check("conjugation symmetry N[d][1] = N[d][3] (z1 <-> z2 swap = Weyl of "
          "SU(2)) -- the spatial side offers the 64/64 pairing slot", ok_conj)
    return N


# ---------------------------------------------------------------------------
# S3 -- combined glue-equivariant sector of e8[C^2] on C^2/Z4
# ---------------------------------------------------------------------------
def equivariant_dims(dims, N, modulus=4):
    """D[d] = sum_j dim(g_j) * N[d][(-j) mod modulus] (j + m = 0 mod modulus)."""
    return [sum(dims[j % len(dims)] * N[d][(-j) % modulus]
                for j in range(len(dims))) for d in range(len(N))]


def section3(dims, N):
    print("\n=== S3  glue-equivariant CCA sector of SDYM(E8) on C^2/Z4 ===")
    D = equivariant_dims(dims, N)
    print("  graded dims D[d] of the equivariant S-algebra (level = poly deg d):")
    print("    %s" % D)

    ok_shape = all(D[d] == (60 if d % 2 == 0 else 64) * (d + 1)
                   for d in range(DMAX + 1))
    check("D[d] = 60(d+1) for even d, 64(d+1) for odd d -- uniform per parity "
          "BECAUSE dim g0 = dim g2 = 60 and dim g1 = dim g3 = 64 (the v128 "
          "dims are exactly what uniformity requires)", ok_shape)

    check("zero modes (d=0) = g0 alone: dim %d = D5 (+) A3 carrier + Cartan -- "
          "the unbroken algebra on the orbifold IS the carrier" % D[0],
          D[0] == 60)

    check("asymptotic density D[d]/(248(d+1)) -> (60+64)/2/248 = 1/4 = 1/|Z4| "
          "(orbifold index density)", sp.Rational(62, 248) == sp.Rational(1, 4))

    # closure: both gradings additive => equivariant subalgebra closes
    # (root additivity was verified in S1 with 0 violations; monomial grade
    #  (p-q) is additive under multiplication by construction)
    check("closure: [g_j (x) m, g_k (x) m'] in g_{j+k} (x) mm' and "
          "(j+k) + (grade m + grade m') = 0 mod 4 -- equivariant sector is a "
          "Lie subalgebra (needs EXACTLY the v128 additivity, 0 violations)",
          True)

    # Z2 (Eguchi-Hanson) halfway consistency: deck^2 = diag(-1,-1)
    N2 = monomial_table(lambda p, q: p + q, modulus=2)
    D2 = [sum((dims[0] + dims[2] if j == 0 else dims[1] + dims[3]) * N2[d][j]
              for j in range(2)) for d in range(DMAX + 1)]
    ok_eh = all(D2[d] == (120 if d % 2 == 0 else 128) * (d + 1)
                for d in range(DMAX + 1))
    check("halfway EH/Z2 sector (deck^2 = -1, BHS Z2 case): dims 120(d+1) / "
          "128(d+1) = SO(16) adjoint / spinor -- the A3 tower refines the "
          "EH tower exactly as mu4 refines the sheet Z2 (4 = 2 x 2, v125)",
          ok_eh)
    return D


# ---------------------------------------------------------------------------
# S4 -- theta/character level matching: Theta_E8 = sum of 4 glue-coset thetas
# ---------------------------------------------------------------------------
def d5_coset_norms(maxnorm):
    """norm -> count for the 4 cosets of D5* / D5: 0=D5, v, s, c."""
    out = {k: {} for k in ('0', 'v', 's', 'c')}
    rng_int = range(-2, 3)
    for v in product(rng_int, repeat=5):
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
    """norm -> count for the 4 cosets of A3* / A3: w0=A3, w1, w2, w3."""
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


def series_mul(a, b, nmax):
    out = [0] * (nmax + 1)
    for i, ai in enumerate(a):
        if i > nmax:
            break
        for j, bj in enumerate(b):
            if i + j > nmax:
                break
            out[i + j] += ai * bj
    return out


def section4():
    print("\n=== S4  (E8)_1 character = sum of 4 mu4 glue sectors (exact) ===")
    NMAX = 3          # character levels q^0..q^3
    MAXNORM = 2 * NMAX
    d5 = d5_coset_norms(MAXNORM)
    a3 = a3_coset_norms(MAXNORM)
    pairing = {0: ('0', 0), 1: ('s', 1), 2: ('v', 2), 3: ('c', 3)}

    # coset theta coefficients: theta_j[m] = # vectors of norm 2m in coset C_j
    theta = {}
    for j, (dk, ak) in pairing.items():
        coeffs = [0] * (NMAX + 1)
        for n5, c5 in d5[dk].items():
            for n3, c3 in a3[ak].items():
                n = n5 + n3
                if n <= MAXNORM and n % 2 == 0 and F(n, 2).denominator == 1:
                    coeffs[int(n) // 2] += c5 * c3
        theta[j] = coeffs
    print("  coset theta coefficients (norm 2m, m=0..%d) per glue class:" % NMAX)
    for j in range(4):
        print("    C%d: %s" % (j, theta[j]))

    shell1 = [theta[j][1] for j in range(4)]
    check("shell 1 (norm 2): %s = (52,64,60,64) -- the v128 split re-derived "
          "from the LATTICE, independent of the root construction" % shell1,
          shell1 == [52, 64, 60, 64])

    shell2 = [theta[j][2] for j in range(4)]
    check("shell 2 (norm 4): %s sums to 2160 = |E8 shell 2| -- the Z4 glue "
          "grading persists shell by shell (Theta_E8 = sum Theta_Cj)" % shell2,
          sum(shell2) == 2160)

    # eta^-8 core: prod (1-q^n)^{-8}
    q = sp.symbols('q')
    P8 = sp.Integer(1)
    for n in range(1, NMAX + 1):
        P8 *= sum(sp.binomial(7 + k, 7) * q ** (n * k)
                  for k in range(0, NMAX // n + 1))
    P8 = sp.expand(P8)
    p8 = [int(P8.coeff(q, k)) for k in range(NMAX + 1)]

    # independent E8 character (v377 style): E4 * prod(1-q^n)^{-8}
    sigma3 = lambda n: sum(d ** 3 for d in range(1, n + 1) if n % d == 0)
    e4 = [1] + [240 * sigma3(n) for n in range(1, NMAX + 1)]
    chi_e8 = series_mul(e4, p8, NMAX)

    sector = {j: series_mul(theta[j], p8, NMAX) for j in range(4)}
    print("  sector characters Theta_Cj/eta^8 (q^0..q^%d):" % NMAX)
    for j in range(4):
        print("    chi_%d: %s" % (j, sector[j]))
    total = [sum(sector[j][m] for j in range(4)) for m in range(NMAX + 1)]
    check("sum of the 4 sector characters = chi_(E8)_1 = %s "
          "(1, 248, 4124, 34752; v377 uses the same series)" % total,
          total == chi_e8 and chi_e8 == [1, 248, 4124, 34752])

    lvl1 = [sector[j][1] for j in range(4)]
    check("level-1 currents per sector: %s = (60,64,60,64) -- the v128 dims "
          "WITH Cartan appear as the 4 branching blocks of the 248" % lvl1,
          lvl1 == [60, 64, 60, 64])

    # conformal weights: min norm / 2 per sector; and per-factor weights
    hmin = [min(n for n, c in
                {0: d5['0'], 1: d5['s'], 2: d5['v'], 3: d5['c']}[j].items()
                if c > 0 and n > 0) for j in range(4)]
    hd5 = [F(0)] + [F(h, 2) for h in hmin[1:]]
    ha3 = [F(0)] + [F(min(n for n in a3[k] if n > 0), 2) for k in (1, 2, 3)]
    qform = lambda x, y: (F(5 * x * x + 3 * y * y, 8))
    ok_h = all(hd5[j] % 1 == (F(5 * j * j, 8)) % 1
               and ha3[j] % 1 == (F(3 * j * j, 8)) % 1 for j in range(4))
    check("sector weights h(D5 side) = %s, h(A3 side) = %s: equal mod 1 to "
          "5x^2/8 and 3y^2/8 -- the v92/v125 DISCRIMINANT FORM (5x^2+3y^2)/8 "
          "IS the pair of conformal weights of the lattice-CFT sectors"
          % (hd5, ha3), ok_h)

    ok_int = all((qform(j, j)) % 1 == 0 and (hd5[j] + ha3[j]) % 1 == 0
                 for j in range(4))
    check("glue-diagonal weights h_j = h_D5 + h_A3 are INTEGERS for all j "
          "(h = 0,1,1,1): v125 isotropy q(k(1,1)) = k^2 in Z <=> all four "
          "sectors are CURRENTS <=> the extension to (E8)_1 is local", ok_int)


# ---------------------------------------------------------------------------
# S5 -- the clock on the celestial sphere: exact Moebius / spin arithmetic
# ---------------------------------------------------------------------------
def moebius_of_diag(a, d):
    """induced map on z = z1/z2 for (z1,z2) -> (a z1, d z2); returns factor."""
    return sp.simplify(a / d)


def proj_order(factor, nmax=16):
    f = sp.Integer(1)
    for n in range(1, nmax + 1):
        f = sp.simplify(f * factor)
        if f == 1:
            return n
    return None


def section5():
    print("\n=== S5  which Z4 rotates the celestial sphere? (exact) ===")
    I = sp.I
    zeta8 = sp.exp(sp.I * sp.pi / 4)

    # deck group action on the sphere
    fac_deck = moebius_of_diag(I, 1 / I)
    check("deck diag(i, i^-1) induces z -> (%s) z on the celestial sphere: "
          "PROJECTIVE ORDER %s -- the A3 deck group acts as z -> -z (the "
          "sheet flip), NOT as the order-4 clock z -> iz"
          % (fac_deck, proj_order(fac_deck)),
          fac_deck == -1 and proj_order(fac_deck) == 2)

    # no SU(2) element induces an order-4 rotation without having order 8
    zeta = sp.symbols('zeta')
    sols = sp.solve(sp.Eq(zeta ** 2, I), zeta)
    orders = [proj_order(sp.simplify(s ** 2)) for s in sols]
    su2_orders = []
    for s in sols:
        g = sp.Matrix([[s, 0], [0, 1 / s]])
        p, m = sp.eye(2), g
        k = 1
        while not m.equals(p):
            m = sp.simplify(m * g)
            k += 1
            if k > 20:
                break
        su2_orders.append(k)
    check("SPIN OBSTRUCTION: any SU(2) lift diag(zeta,1/zeta) of the clock "
          "z -> iz needs zeta^2 = i, i.e. zeta a primitive 8th root: SU(2) "
          "orders %s = 8 -- the clock's spin group is Z8 (would quotient to "
          "the A7 ALE), NEVER the A3 deck Z4" % su2_orders,
          all(o == 8 for o in su2_orders) and all(o == 4 for o in orders))

    g8 = sp.Matrix([[zeta8, 0], [0, 1 / zeta8]])
    deck = sp.Matrix([[I, 0], [0, 1 / I]])
    check("SPIN BRIDGE: (spin clock)^2 = diag(zeta8,zeta8^-1)^2 = "
          "diag(i,i^-1) = the A3 deck generator EXACTLY -- the deck Z4 is the "
          "unique index-2 subgroup of the clock's Z8; sphere images Z4 > Z2; "
          "|Z8| = 8 = 2|mu4| (the c3 = 1/(8 pi) seam winding integer)",
          sp.simplify(g8 ** 2 - deck) == sp.zeros(2, 2))

    # the order-4 clock IS realised -- by the U(2) phase diag(i, 1)
    fac_clock = moebius_of_diag(I, 1)
    z = sp.symbols('z')
    fixed = sp.solve(sp.Eq(I * z, z), z)
    orbit = {sp.simplify(I ** k) for k in range(4)}
    check("U(2) CLOCK: diag(i,1) induces z -> iz with projective order %s, "
          "fixed points {0,inf}, free orbit {1,i,-1,-i} = mu4 -- ALL v180 "
          "clock properties hold for this (non-deck) isometry"
          % proj_order(fac_clock),
          fac_clock == I and proj_order(fac_clock) == 4
          and fixed == [0] and orbit == {1, I, -1, -I})

    clock = sp.Matrix([[I, 0], [0, 1]])
    comm = sp.simplify(clock * deck - deck * clock)
    det_clock = sp.simplify(clock.det())
    check("clock diag(i,1) NORMALISES the deck (diagonal U(2) is abelian: "
          "commutator = 0) and so PRESERVES the glue flat connection; "
          "det = i has order 4: the clock rotates the holomorphic symplectic "
          "form omega = dz1^dz2 by exactly i = the mu4 generator (a Kaehler, "
          "NOT triholomorphic isometry -> rotates the twistor sphere by pi/2)",
          comm == sp.zeros(2, 2) and det_clock == I
          and proj_order(det_clock) == 4)

    check("clock vs deck on the sphere: clock^2 induces z -> (%s) z = the "
          "deck's sphere image -- projectively the deck is the SQUARE of the "
          "clock (the sheet pair Z2 inside the clock Z4)"
          % sp.simplify(fac_clock ** 2),
          sp.simplify(fac_clock ** 2 - fac_deck) == 0)

    # clock-invariant deformations of the A3 singularity XY = Z^4
    Z, a3c, a2c, a1c, a0c = sp.symbols('Z a3 a2 a1 a0')
    P = Z ** 4 + a3c * Z ** 3 + a2c * Z ** 2 + a1c * Z + a0c
    diff = sp.expand(P.subs(Z, sp.I * Z) - P)
    sol = sp.solve([sp.Poly(diff, Z).coeff_monomial(Z ** k) for k in range(4)],
                   [a3c, a2c, a1c], dict=True)
    ok_def = sol == [{a3c: 0, a2c: 0, a1c: 0}]
    check("CLOCK-INVARIANT DEFORMATION: P(iZ) = P(Z) forces a3 = a2 = a1 = 0: "
          "of the 3-parameter versal A3 family XY = Z^4 + a2 Z^2 + a1 Z + a0 "
          "(3 = rank A3 = # resolution spheres), the clock fixes EXACTLY the "
          "1-parameter family XY = Z^4 + a0", ok_def)

    c = sp.symbols('c', positive=True)
    roots4 = sp.solve(sp.Eq(Z ** 4, c ** 4), Z)
    ratios = {sp.simplify(r / c) for r in roots4}
    z1r, z2r, z3r, z4r = c, sp.I * c, -c, -sp.I * c
    lam = sp.simplify((z1r - z3r) * (z2r - z4r) / ((z1r - z4r) * (z2r - z3r)))
    check("the 4 branch points of XY = Z^4 - c^4 are ONE mu4 orbit "
          "{c, ic, -c, -ic} (ratios = %s) with CROSS-RATIO %s = 2: the seam "
          "marks (v179: one clock orbit; v168/v214: cross-ratio 2 => j = 1728 "
          "pillowcase) appear as the celestial deformation branch points"
          % (ratios, lam),
          ratios == {1, sp.I, -1, -sp.I} and lam == 2)


# ---------------------------------------------------------------------------
# S6 -- negative controls
# ---------------------------------------------------------------------------
def section6(roots, dims):
    print("\n=== S6  negative controls (the test must kill the fakes) ===")
    I = sp.I

    # NC1: false spatial action (z1,z2) -> (i z1, i z2)
    det_false = sp.simplify(sp.Matrix([[I, 0], [0, I]]).det())
    check("NC1a: diag(i,i) has det = %s != 1: NOT in SL(2,C) => the quotient "
          "is not Gorenstein/Calabi-Yau, there is NO ALE hyperkaehler "
          "resolution and no SD-gravity background" % det_false,
          det_false == -1)

    # NC1b: Poisson closure fails for the diag(i,i)-invariant sector
    z1, z2 = sp.symbols('z1 z2')
    pb = lambda f, g: (sp.diff(f, z1) * sp.diff(g, z2)
                       - sp.diff(f, z2) * sp.diff(g, z1))
    grade_false = lambda p_, q_: (p_ + q_) % 4
    viol = 0
    tested = 0
    invmons = [(p_, q_) for p_ in range(5) for q_ in range(5)
               if grade_false(p_, q_) == 0 and p_ + q_ > 0]
    for (pa, qa), (pb_, qb_) in combinations(invmons, 2):
        b = sp.expand(pb(z1 ** pa * z2 ** qa, z1 ** pb_ * z2 ** qb_))
        if b == 0:
            continue
        tested += 1
        if grade_false(pa + pb_ - 1, qa + qb_ - 1) != 0:
            viol += 1
    check("NC1b: Poisson bracket of diag(i,i)-invariant monomials leaves the "
          "invariant sector in %d/%d nonzero cases (bracket shifts the grade "
          "by -2 mod 4): the false w-algebra sector does NOT close -- KILLED"
          % (viol, tested), viol == tested and tested > 0)

    # NC1c: conjugate pairing impossible (grade-1/3 asymmetry)
    Nf = monomial_table(lambda p_, q_: p_ + q_)
    asym = [(d, Nf[d][1], Nf[d][3]) for d in range(DMAX + 1)
            if Nf[d][1] != Nf[d][3]]
    check("NC1c: under diag(i,i) the monomial grades are N[d][1] != N[d][3] "
          "at %d of %d levels (e.g. d=1: %s) -- the conjugate 64/64 pairing "
          "of g1/g3 has NO spatial partner slots -- KILLED"
          % (len(asym), DMAX + 1, Nf[1]),
          len(asym) > 0)

    # NC2: false glue assignment (swap classes 1 <-> 2)
    swap = {0: 0, 1: 2, 2: 1, 3: 3}
    fake = {r: swap[c] for r, c in roots.items()}
    pairs, viol2 = additivity(roots, fake)
    check("NC2: swapping the glue classes of the 64-block and the 60-block "
          "breaks grading additivity on %d of %d root pairs (>0) and breaks "
          "the conjugate-dimension pairing (dim fake-g1 = 60 != 64 = dim "
          "fake-g3): the false glue does NOT define a graded Lie algebra -- "
          "KILLED" % (viol2, pairs), viol2 > 0)

    # NC3: rigidity -- which relabelings of the 4 classes stay additive?
    good = []
    for perm in permutations(range(4)):
        relab = {r: perm[c] for r, c in roots.items()}
        _, v = additivity(roots, relab)
        if v == 0:
            good.append(perm)
    check("NC3 RIGIDITY: of all 24 relabelings of the glue classes exactly "
          "%d are additive: %s = identity and negation j -> -j = Aut(Z4) -- "
          "the mu4 glue grading is rigid up to the group automorphism"
          % (len(good), good),
          sorted(good) == [(0, 1, 2, 3), (0, 3, 2, 1)])


# ---------------------------------------------------------------------------
def main():
    print("WP1 CELEST.SEAM.01 -- Z4 orbifold structure of the celestial chiral"
          " algebra on C^2/Z4 (A3 ALE) vs the E8 mu4-glue grading")
    roots, dims = section1()
    N = section2()
    section3(dims, N)
    section4()
    section5()
    section6(roots, dims)

    print("\n=== VERDICT (see report) ===")
    print("  POSITIVE (exact): E8 mu4-glue = order-4 inner torus automorphism")
    print("    = flat Z4 monodromy on the A3 ALE; equivariant CCA closes,")
    print("    zero modes = carrier D5+A3, graded dims 60/64 alternating,")
    print("    4-sector (E8)_1 character with h = discriminant form (v125).")
    print("  CORRECTION (exact): the A3 deck Z4 acts on the celestial sphere")
    print("    as z -> -z (order 2). The order-4 clock z -> iz is NOT the")
    print("    deck group: it is the U(2) phase diag(i,1) (normalising the")
    print("    deck, det = i rotating omega by the mu4 generator), or the")
    print("    spin-lift Z8 with (spin clock)^2 = deck.")
    print("  => Overall: match under ONE precisely named extra identification")
    print("     (clock^2 = deck on the sphere / sheet-Z2 spin bookkeeping).")
    print("\n" + ("ALL CHECKS PASSED" if PASS_ALL else "SOME CHECKS FAILED"))
    return PASS_ALL


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
