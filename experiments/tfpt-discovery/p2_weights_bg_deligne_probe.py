"""p2_weights_bg_deligne_probe.py -- EXPLORATION ONLY (experiments/, no verification claim).

HARDENING THE P2 WEIGHT-TYPING POSTULATE (the v491 check-9 residual).

v491 (P2.PARTITION.01) reduced g_car = 5 to a corollary of "3 positive integers summing
to 4"; the residual was the TYPING: why integers, why positive, why sum 4?  This probe
types the anchor weights as the Birkhoff-Grothendieck splitting exponents of the DELIGNE
CANONICAL EXTENSION E of the flavor connection and shows that, given already-established
[E] anchors, all three properties become THEOREMS of standard algebraic geometry:

    THE PROVABLE STATEMENT (conditional on the premise map below):
    Let V be the 3-dim generation module, identified with H^1(P^1 \\ mu4; C)
    (rank = #marks - 1 = 3; #marks = 4 by Gauss-Bonnet, v216), and let nabla be a
    flat, irreducible, unitary (U) connection on V over P^1 \\ mu4 whose local
    monodromy at every mark is the cusp class (char poly lam^3 - 1, v117).  Then the
    Deligne canonical extension E (residue eigenvalues in [0,1)) satisfies:
      (i)   rank E = 3                                   [rank of V]
      (ii)  deg E = -sum_marks tr Res = -4               [Deligne; trace 1 per mark]
      (iii) h^0(E) = 0                                   [Mehta-Seshadri stability]
      (iv)  E = O(-a1)+O(-a2)+O(-a3), a_i in Z           [Birkhoff-Grothendieck]
    hence a_i >= 1, sum a_i = 4, and {a} = {1,1,2} is UNIQUE (v491 partition lemma);
    g_car = e2 = 5.

NON-CIRCULARITY: v23 takes the splitting type as INPUT (generator reading) and v115
check 1 takes diag A0 = a/4 as INPUT (an IFF statement).  The chain here --
rank (topology) -> deg (residue trace) -> integrality (BG) -> positivity (stability)
-> partition (v491) -- uses NEITHER; A0* appears only as the explicit consistency
witness.  The paper's Schur-Horn theorem (tfpt_2 'Global computation' section) needs
the 'balanced / minimal-variance' selection to kill {0,2,2}; here that selection is
TYPED: {0,2,2} contains an O(0) summand, h^0 = 1 != 0 -- positivity IS the selection.

THE h^1 DISCREPANCY (resolved): the naive target shape "generation space = H^1 of the
rank-3 E" is FALSE: h^1(O(-2)+O(-1)^2) = sum(a_i - 1) = 1, not 3 (chi = deg + rk = -1,
Riemann-Roch).  The correct typing needs TWO objects sharing (deg, h^0) = (-4, 0):
    L = O(-D) (rank 1, D = mu4):  h^1(L) = 3  = the generation space
                                  (= H^0(Omega^1(log D)) = H^0(O(2)), v137 basis
                                  omega_k = z^{k-1}dz/(z^4-1));
    E = Deligne ext. (rank 3):    FIBER = the 3 generations, splitting = the anchor.
Duality pattern: rank E = 3 = h^1(L), deg E = deg L = -4, h^0(E) = h^0(L) = 0.
Negative control: demanding "generations = H^1(E')" for a rank-3 E' with h^0 = 0
forces deg = -6 (not -4) and loses uniqueness ({1,1,4},{1,2,3},{2,2,2}, e2 in
{9,11,12}, never 5) -- the two-object typing is load-bearing.

THE BISWAS COMPUTATION (explicit): the Mehta-Seshadri weights {0,1/3,2/3} live on the
PARABOLIC side; their denominator is 3 = N_fam, NOT 2 = |Z2| -- so the Biswas cover is
the Z3 cusp cover (genus 2, local monodromies (1,1,2,2) mod 3; an all-equal choice is
impossible since 4c != 0 mod 3), NOT the pillowcase double w^2 = z^4 - 1 (genus 1,
j = 1728, the deck-side cover).  For the explicit model W = (chi^0 + chi^1 + chi^2)
tensor O_Y (rank 3, deg 0, isotropy = regular rep = weights {0,1/3,2/3} at every mark)
the invariant pushforward gives the underlying bundle O + O(-2) + O(-2):
    rank 3 OK, deg -4 OK  -- integrality and the sum rule COME OUT of Biswas --
but splitting {0,2,2}: the weights alone do NOT fix the splitting type; the
decomposable (trivial-character) model lands exactly on the unstable Schur-Horn
companion (h^0 = 1).  (1,1,2) is the Biswas image of the STABLE object -- stability
(= irreducible unitary monodromy, exact via v117) is the selector.

HONEST RESIDUALS (stay open; P2 NOT axiom-free):
    R1  "generation space = H^1(P^1 \\ mu4) with cusp-class flavor connection"
        -- the module identification, [C] (tfpt_2: 'generation space IS H^1 of the
        seam curve with its parabolic weights' stays [C]; QGEO.SYM territory).
    R2  (U) unitarity of the flavor monodromy, [C] (v33/v40 premise).
    R3  the identification of the ANALYTIC monodromy with the exact W(A3)
        representation, [N] (v117 check 4, ODE matching 1e-7).

Repo anchors: v216 (marks = 2chi), v137 (H^1 basis/characters), v228 (RR index gate),
v115 (mu4-average, A0*), v117 (exact monodromy, S4), v39/v33 (pardeg 0, splitting on
the explicit point), v491 (partition lemma), tfpt_2_standard_model 'Global
computation' + stability-wall note, tfpt_research_contracts U_H2 block.

Exact sympy/integer arithmetic throughout; no floats; standalone (no tfpt_constants).
Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/p2_weights_bg_deligne_probe.py
"""
from fractions import Fraction as Fr
from itertools import combinations_with_replacement, product

import sympy as sp

RESULTS = []


def check(name, ok):
    RESULTS.append(bool(ok))
    print(("PASS" if ok else "FAIL") + " [%2d] %s" % (len(RESULTS), name))


def e2(ms):
    x = list(ms)
    return sum(x[i] * x[j] for i in range(len(x)) for j in range(i + 1, len(x)))


def h0_line(d):
    """h^0(P^1, O(d))"""
    return d + 1 if d >= 0 else 0


def h1_line(d):
    """h^1(P^1, O(d)) = h^0(O(-d-2)) (Serre)"""
    return -d - 1 if d <= -2 else 0


Z, W, T = sp.symbols('z w t')
I = sp.I

# exact objects from the repo (v115 / v117)
A0STAR = sp.Matrix([[sp.Rational(1, 2), sp.sqrt(2) / 6, 0],
                    [sp.sqrt(2) / 6, sp.Rational(1, 4), sp.sqrt(5) / 12],
                    [0, sp.sqrt(5) / 12, sp.Rational(1, 4)]])
M0 = sp.Matrix([[0, -(1 + I) / 2, (1 - I) / 2],
                [-(1 + I) / 2, -I / 2, sp.Rational(-1, 2)],
                [(1 - I) / 2, sp.Rational(-1, 2), I / 2]])
U = sp.diag(1, I, -I)
MARKS = [sp.Integer(1), I, sp.Integer(-1), -I]
WEIGHTS = [sp.Integer(0), sp.Rational(1, 3), sp.Rational(2, 3)]   # cusp / MS weights


def enumerate_group(gens):
    """BFS closure of <gens> (exact 3x3 sympy matrices, Gaussian-rational entries)."""
    def freeze(m):
        return tuple(sp.expand(x) for x in m)

    elems = {freeze(sp.eye(3)): sp.eye(3)}
    frontier = [sp.eye(3)]
    while frontier:
        new = []
        for e in frontier:
            for g in gens:
                x = sp.expand(g * e)
                kx = freeze(x)
                if kx not in elems:
                    elems[kx] = x
                    new.append(x)
        frontier = new
    return list(elems.values())


def run():
    print("p2_weights_bg_deligne_probe: typing the (1,1,2) anchor as Birkhoff-"
          "Grothendieck/Deligne data (exploration)")
    print("=" * 100)

    # ================================================================ A. premise map
    # A1. the generation H^1: basis omega_k, mu4 characters, trivial character absent
    chars, res_ok, reg_inf = [], True, True
    for k in (1, 2, 3, 4):
        om = Z ** (k - 1) / (Z ** 4 - 1)
        # character under the deck z -> iz (1-form transforms with the extra i from dz)
        rot = sp.simplify((I * Z) ** (k - 1) / ((I * Z) ** 4 - 1) * I / om)
        chars.append(sp.simplify(rot - I ** k))
        ressum = sum(sp.residue(om, Z, zeta) for zeta in MARKS)
        for zeta in MARKS:
            if sp.simplify(sp.residue(om, Z, zeta) - zeta ** k / 4) != 0:
                res_ok = False
        if k <= 3 and sp.simplify(ressum) != 0:
            reg_inf = False          # residue theorem: regular at infinity
        if k == 4 and sp.simplify(ressum + (-1)) != 0:
            reg_inf = False          # res_infty(omega_4) = -1 != 0: dlog pole
    check("A1 GENERATION H^1 [E, v137]: omega_k = z^(k-1)dz/(z^4-1), k=1,2,3 span "
          "H^1(P^1 minus mu4) = C^3 (residues zeta^k/4, regular at infinity, deck "
          "characters i^k); k=4 carries the TRIVIAL character and has res_inf = -1 "
          "(dlog pole) -- trivial character ABSENT, rank = #marks - 1 = 3",
          all(c == 0 for c in chars) and res_ok and reg_inf)

    # A2. the same 3 as coherent cohomology of the degree -4 line bundle L = O(-D)
    dims = (h0_line(-4), h1_line(-4), h0_line(2), h0_line(-2 + 4), h0_line(4))
    check("A2 LINE-BUNDLE CARRIER [E, v228-type RR]: L = O(-D), deg -4: h^0 = %d, "
          "h^1 = %d = N_fam (RR chi = deg+1 = -3; Serre h^1(O(-4)) = h^0(O(2)) = %d); "
          "Omega^1(log D) = O(-2+4) = O(2): h^0 = %d = 3 (the v137 basis IS this "
          "space); function side h^0(O(+4)) = %d = 5 = g_car (v228 index gate)"
          % dims, dims == (0, 3, 3, 3, 5))

    # A3. the cusp class fixes the canonical residue exponents {0,1/3,2/3} in [0,1)
    lam = sp.Symbol('lam')
    cusp_ok = (sp.simplify(M0.H * M0) == sp.eye(3)
               and sp.simplify(M0 ** 3) == sp.eye(3)
               and sp.expand(M0.charpoly(lam).as_expr() - (lam ** 3 - 1)) == 0)
    expo = [sp.exp(2 * sp.pi * I * a) for a in WEIGHTS]
    spec_match = (all(sp.simplify(x ** 3 - 1) == 0 for x in expo)
                  and len({sp.nsimplify(sp.expand_complex(x))
                           for x in expo}) == 3)
    distinct = all(sp.simplify(WEIGHTS[i] - WEIGHTS[j]) not in (0,)
                   and not (WEIGHTS[i] - WEIGHTS[j]).is_integer
                   for i in range(3) for j in range(3) if i != j)
    check("A3 CUSP CLASS => CANONICAL EXPONENTS [E, v117]: M0 unitary, M0^3 = 1, "
          "char poly lam^3 - 1; the unique residue eigenvalues in [0,1) with "
          "exp(2 pi i a) = spec M0 are {0, 1/3, 2/3} (distinct mod Z => the Deligne "
          "canonical extension exists and is unique, no Jordan ambiguity)",
          cusp_ok and spec_match and distinct)

    # ============================================== B. deg E = -4 is a THEOREM
    # B1. mu4-average lemma, generic X (v115 check 1, replicated)
    xsym = sp.Matrix(3, 3, lambda i, j: sp.Symbol('x%d%d' % (i, j), complex=True))
    ssum = sp.zeros(3)
    for k in range(4):
        uk = U ** k
        ssum += uk * xsym * uk.inv()
    check("B1 MU4-AVERAGE LEMMA [E, v115]: sum_k U^k X U^-k = 4 diag(X) for generic "
          "3x3 X (U = diag(1,i,-i)) -- the four residues A_k = U^k A0 U^-k are one "
          "mu4 orbit and their sum is diagonal",
          sp.simplify(sp.expand(ssum - 4 * sp.diag(xsym[0, 0], xsym[1, 1],
                                                   xsym[2, 2]))) == sp.zeros(3))

    # B2. Deligne degree bookkeeping on the explicit witness A0*
    char_ok = sp.simplify(A0STAR.charpoly(lam).as_expr()
                          - lam * (lam - sp.Rational(1, 3))
                          * (lam - sp.Rational(2, 3))) == 0
    traces = [sp.simplify((U ** k * A0STAR * (U ** k).inv()).trace())
              for k in range(4)]
    deg_E = -sum(traces)
    pardeg = deg_E + 4 * sum(WEIGHTS)
    check("B2 deg E = -4 [THEOREM given A3]: residue spec {0,1/3,2/3} has trace 1 "
          "per mark; 4 marks (v216 Gauss-Bonnet) => deg E = -sum_k tr(Res_k) = %s "
          "(Deligne: deg of the canonical extension = -sum of residue traces); "
          "par-deg = deg + 4*(0+1/3+2/3) = %s (the v39 'pardeg 0' (U) consistency); "
          "witness A0* has char poly lam(lam-1/3)(lam-2/3) exactly"
          % (deg_E, pardeg),
          char_ok and traces == [1, 1, 1, 1] and deg_E == -4 and pardeg == 0)

    # B3. flatness across infinity + the integer exponents there (consistency route)
    prod_flat = sp.eye(3)
    for k in range(4):
        uk = U ** k
        prod_flat = sp.expand(prod_flat * (uk * M0 * uk.inv()))
    sumA = sp.simplify(sum((U ** k * A0STAR * (U ** k).inv() for k in range(4)),
                           sp.zeros(3)))
    off_zero = all(sp.simplify(sumA[i, j]) == 0
                   for i in range(3) for j in range(3) if i != j)
    eig_inf = sorted([sumA[i, i] for i in range(3)], reverse=True)
    check("B3 REGULAR INFINITY [E, v117/v115]: monodromy at infinity = "
          "prod_k U^k M0 U^-k = 1 exactly and (M0 U)^4 = 1 -- infinity is an "
          "APPARENT singularity (integer exponents); on the witness: sum_k A_k = "
          "4 diag(A0*) = diag(2,1,1), eigenvalues %s in Z^3, sum 4 -- consistent "
          "with BG integrality but NOT used for the uniqueness below"
          % (eig_inf,),
          sp.simplify(prod_flat) == sp.eye(3)
          and sp.simplify((M0 * U) ** 4) == sp.eye(3)
          and off_zero and eig_inf == [2, 1, 1])

    # ============================================== C. h^0(E) = 0 is a THEOREM
    # C1. irreducibility is EXACT: <U, M0> has order 24 and sum |chi|^2 = |G|
    elems = enumerate_group([U, M0])
    chi2 = sp.Integer(0)
    for x in elems:
        tr = sp.expand(x.trace())
        chi2 += sp.expand(tr * sp.conjugate(tr))
    check("C1 IRREDUCIBILITY EXACT [E, v117]: |<U, M0>| = %d = |W(A3)| = |S4| and "
          "sum_g |tr g|^2 = %s = |G| -- the 3-dim monodromy representation is "
          "IRREDUCIBLE (standard x sign of S4); with (U) unitarity this is the "
          "Mehta-Seshadri stability input" % (len(elems), sp.simplify(chi2)),
          len(elems) == 24 and sp.simplify(chi2 - 24) == 0)

    # C2. stability => h^0 = 0 (the inequality skeleton, exhaustively)
    # a nonzero section O -> E saturates to a line bundle L with deg L = d >= 0;
    # its parabolic degree is d + (one induced weight per mark) >= 0 = par-slope(E);
    # STRICT stability demands par-deg(L) < 0 -- contradiction for EVERY case:
    viol = []
    for d in range(0, 4):
        for wsel in product(WEIGHTS, repeat=4):
            pdeg = d + sum(wsel)
            if pdeg < 0:                      # would satisfy stability -> no clash
                viol.append((d, wsel))
    check("C2 STABILITY => h^0(E) = 0 [THEOREM given C1 + (U)]: every candidate "
          "section-saturation (deg d >= 0, any induced weights from {0,1/3,2/3} at "
          "the 4 marks) has par-deg = d + sum w >= 0 = par-slope(E) -- checked all "
          "%d cases, 0 satisfy the strict-stability bound par-deg < 0 => no global "
          "sections (the v137 'trivial character absent' correlate, now typed)"
          % (4 * 3 ** 4), viol == [])

    # C3. the BG dictionary: h^0 = 0 <=> all splitting exponents >= 1
    dict_ok = True
    for a in product(range(-3, 7), repeat=3):
        h0 = sum(h0_line(-ai) for ai in a)
        if (h0 == 0) != all(ai >= 1 for ai in a):
            dict_ok = False
    check("C3 BG DICTIONARY [E]: for E = O(-a1)+O(-a2)+O(-a3), h^0(E) = "
          "sum max(0, 1 - a_i) = 0 <=> a_i >= 1 for all i (window a_i in [-3,6]) "
          "-- POSITIVITY of the anchor IS h^0 = 0", dict_ok)

    # ==================================== D. uniqueness + convergence + controls
    # D1. the partition lemma under the full typing
    sols = [m for m in combinations_with_replacement(range(1, 11), 3) if sum(m) == 4]
    check("D1 UNIQUENESS [E, v491]: {a in Z^3 : a_i >= 1 (h^0 = 0), sum a_i = 4 "
          "(deg E = -4), 3 parts (rank 3)} = %s -- unique; e2 = %d = g_car, "
          "e3 = %d = |Z2|, e2 - e3 = %d = N_fam"
          % (sols, e2(sols[0]), sols[0][0] * sols[0][1] * sols[0][2],
             e2(sols[0]) - 2),
          sols == [(1, 1, 2)] and e2(sols[0]) == 5)

    # D2. Schur-Horn route converges (the paper's theorem, with 'balance' TYPED)
    bound = [sp.Rational(8, 3), sp.Rational(4, 1)]      # partial sums of 4*(2/3,1/3)
    sh = []
    for a in product(range(0, 3), repeat=3):            # diag in [0, 2/3] => a_i in {0,1,2}
        s = sorted(a, reverse=True)
        if sum(s) == 4 and s[0] <= bound[0] and s[0] + s[1] <= bound[1]:
            if tuple(s) not in sh:
                sh.append(tuple(s))
    survivors = [s for s in sh if all(x >= 1 for x in s)]
    check("D2 SCHUR-HORN CONVERGENCE [E, tfpt_2 'Global computation']: integer "
          "points of the permutohedron of 4*spec(A0) = (8/3, 4/3, 0) with sum 4 = "
          "%s (exactly the paper's two options); h^0 = 0 kills {2,2,0} (contains "
          "O(0), h^0 = 1) => %s -- the paper's 'balanced' selection is now TYPED "
          "as positivity, and the two routes converge on {1,1,2}"
          % (sorted(sh), survivors),
          sorted(sh) == [(2, 1, 1), (2, 2, 0)] and survivors == [(2, 1, 1)])

    # D3. negative control: drop positivity
    nc0 = [m for m in combinations_with_replacement(range(0, 5), 3) if sum(m) == 4]
    ncz = [m for m in combinations_with_replacement(range(-5, 10), 3) if sum(m) == 4]
    e2s0 = sorted(set(e2(m) for m in nc0))
    e2sz = set(e2(m) for m in ncz)
    check("D3 NEGATIVE CONTROL / POSITIVITY [E, v491]: allowing a_i = 0 gives %d "
          "solutions, e2 ambiguous %s; allowing negatives (window [-5,9]) gives %d "
          "solutions, %d distinct e2 values -- h^0 = 0 is load-bearing"
          % (len(nc0), e2s0, len(ncz), len(e2sz)),
          len(nc0) == 4 and e2s0 == [0, 3, 4, 5] and len(ncz) > 10
          and len(e2sz) > 5 and 5 in e2sz)

    # D4. negative control: drop the degree fixing
    nc3 = [m for m in combinations_with_replacement(range(1, 11), 3) if sum(m) == 3]
    nc5 = [m for m in combinations_with_replacement(range(1, 11), 3) if sum(m) == 5]
    check("D4 NEGATIVE CONTROL / DEGREE [E, v491]: deg -3 -> unique but e2 = %d != 5; "
          "deg -5 -> %d solutions (not unique) -- deg E = -4 = -#marks is "
          "load-bearing" % (e2(nc3[0]), len(nc5)),
          len(nc3) == 1 and e2(nc3[0]) == 3 and len(nc5) == 2)

    # D5. negative control: the mark count (n marks => n-1 parts summing to n)
    marks_scan = {}
    for n in range(3, 9):
        s = [m for m in combinations_with_replacement(range(1, n + 1), n - 1)
             if sum(m) == n]
        marks_scan[n] = (len(s), e2(s[0]))
    formula_ok = all(marks_scan[n][1] == (n - 2) * (n + 1) // 2 for n in marks_scan)
    check("D5 NEGATIVE CONTROL / MARK COUNT [new]: n marks => n-1 positive parts "
          "summing to n; the partition {1,..,1,2} is unique for EVERY n >= 3 "
          "(uniqueness is generic!), but e2 = (n-2)(n+1)/2 = %s -- e2 = 5 = g_car "
          "picks out n = 4 alone: the VALUE, not the uniqueness, is the n = 4 "
          "content" % ({n: v[1] for n, v in marks_scan.items()}),
          all(v[0] == 1 for v in marks_scan.values()) and formula_ok
          and [n for n, v in marks_scan.items() if v[1] == 5] == [4])

    # D6. negative control: MS-rational weights typed directly as exponents
    w1 = [sp.Rational(1, 3)] * 3
    w2 = [sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)]
    e2w = [e2([4 * x for x in w]) for w in (w1, w2)]
    check("D6 NEGATIVE CONTROL / INTEGRALITY [E, v491]: typing the RATIONAL MS "
          "weights directly as exponents (scaled by 4) gives e2 = %s and %s, "
          "both != 5 and not integers -- integrality lives on the BUNDLE side "
          "(BG splitting of the Deligne extension), not on the parabolic side"
          % (e2w[0], e2w[1]),
          e2w == [sp.Rational(16, 3), sp.Rational(44, 9)])

    # ==================================== E. the h^1 discrepancy, resolved
    # E1. h^1 of the anchor bundle is 1, not 3; the carrier of the generations is L
    a_anchor = (1, 1, 2)
    h1E = sum(h1_line(-ai) for ai in a_anchor)
    chiE = sum((-ai) + 1 for ai in a_anchor)            # RR: chi(O(d)) = d + 1
    check("E1 THE h^1 DISCREPANCY [resolved]: h^1(O(-2)+O(-1)^2) = sum(a_i - 1) = "
          "%d != 3 and chi(E) = deg + rk = %d (RR) -- the naive typing 'generation "
          "space = H^1(E)' is FALSE.  Correct two-object typing: generations = "
          "H^1(L) = C^3 for L = O(-D) (A1/A2); E carries them as its FIBER (rank 3) "
          "with the anchor as splitting type; shared invariants rank E = 3 = "
          "h^1(L), deg E = -4 = deg L, h^0(E) = 0 = h^0(L)"
          % (h1E, chiE),
          h1E == 1 and chiE == -1
          and 3 == h1_line(-4) and -4 == sum(-ai for ai in a_anchor)
          and sum(h0_line(-ai) for ai in a_anchor) == 0 == h0_line(-4))

    # E2. negative control: forcing 'generations = H^1(rank-3 E)' breaks everything
    forced = [m for m in combinations_with_replacement(range(1, 8), 3)
              if sum(x - 1 for x in m) == 3]
    check("E2 NEGATIVE CONTROL / NAIVE TYPING [new]: demanding h^1(E') = 3 with "
          "h^0(E') = 0 for a rank-3 E' forces sum a_i = 6, i.e. deg = -6 != -4, "
          "and the splitting is NOT unique: %s with e2 = %s -- never 5.  The "
          "target shape 'generation space = H^1 of the rank-3 bundle' fails "
          "exactly as flagged; the two-object typing (E1) is the correct one"
          % (forced, [e2(m) for m in forced]),
          forced == [(1, 1, 4), (1, 2, 3), (2, 2, 2)]
          and [e2(m) for m in forced] == [9, 11, 12]
          and all(sum(m) == 6 for m in forced))

    # E3. observations (exact, but NOT load-bearing -- recorded as curiosities)
    h1_EtwD = sum(h1_line(-ai - 4) for ai in a_anchor)   # E(-D) = O(-6)+O(-5)^2
    h1_locsys = -3 * (2 - 4)                             # -chi = -rk*chi_top(P^1 minus 4)
    check("E3 OBSERVATION [curiosity, not load-bearing]: h^1(E(-D)) = 5+4+4 = %d "
          "= Delta_Q (the 13 of v115's (8,0,5)/144 lemma), and h^1 of the rank-3 "
          "flavor LOCAL SYSTEM on P^1 minus mu4 is -chi = 3*(4-2) = %d = |R+(A3)| "
          "= p2 (hexagon sites) -- three DIFFERENT H^1's coexist: 3 (generations, "
          "L-side), 1 (coherent h^1 of E), 6 (local-system deformations); the "
          "discrepancy came from conflating them"
          % (h1_EtwD, h1_locsys),
          h1_EtwD == 13 and h1_locsys == 6)

    # ==================================== F. the Biswas correspondence, explicit
    # F1. the pillowcase double (deck side): genus 1, j = 1728 -- NOT the weight cover
    g2 = Fr(2 * 0 - 2) * 2 + 4 * (2 - 1)                 # RH: 2g-2 = N(2g_X-2)+sum(e-1)
    genus_z2 = (g2 + 2) / 2
    lam_cr = sp.Rational(2)                              # cross-ratio of mu4 (v214)
    j_inv = 256 * (lam_cr ** 2 - lam_cr + 1) ** 3 / (lam_cr ** 2 * (lam_cr - 1) ** 2)
    check("F1 DECK COVER [E, v214-type]: w^2 = z^4 - 1 (Z2, branched at mu4, deg 4 "
          "even => unramified over infinity): Riemann-Hurwitz genus = %s = 1, "
          "cross-ratio 2 => j = %s = 1728 (the tau = i pillowcase double) -- "
          "denominator 2 = |Z2|: this is the DECK-side cover, not the Biswas cover "
          "for the weights (denominator 3 = N_fam)" % (genus_z2, j_inv),
          genus_z2 == 1 and j_inv == 1728)

    # F2. the Z3 cusp cover exists only with asymmetric branch data (1,1,2,2)
    all_equal_bad = all((4 * c) % 3 != 0 for c in (1, 2))
    m_branch = (1, 1, 2, 2)
    branch_ok = sum(m_branch) % 3 == 0
    degq = sum(m_branch)                                 # q = (z-1)(z-i)(z+1)^2(z+i)^2, deg 6
    unram_inf = degq % 3 == 0
    g3 = 3 * (2 * 0 - 2) + 4 * (3 - 1)                   # 4 totally ramified points
    genus_z3 = Fr(g3 + 2, 2)
    check("F2 BISWAS COVER [new, explicit]: a Z3 cover killing the weight "
          "denominator 3 cannot have equal local monodromies (4c mod 3 != 0 for "
          "c = 1,2); the choice m = (1,1,2,2) works (sum 6 = 0 mod 3, deg q = 6 => "
          "unramified over infinity); Riemann-Hurwitz genus = %s = 2 -- the cusp "
          "cover Y is a genus-2 curve with Z3 action" % genus_z3,
          all_equal_bad and branch_ok and unram_inf and genus_z3 == 2)

    # F3. eigensheaf degrees of p_* O_Y by explicit pole bookkeeping + chi cross-check
    deg_V = {}
    for j in (1, 2):
        # allowed pole of g at mark i: floor(j*m_i/3); at infinity ord(y^j) = -2j
        deg_V[j] = sum((j * mi) // 3 for mi in m_branch) - 2 * j
    chi_sum = (0 + 1) + (deg_V[1] + 1) + (deg_V[2] + 1)  # chi(O(d)) = d+1 on P^1
    chi_Y = 1 - 2                                        # 1 - g(Y)
    check("F3 EIGENSHEAVES [new, explicit]: p_* O_Y = O + V_1 + V_2 with "
          "deg V_j = sum_i floor(j m_i / 3) - 2j = (%d, %d) => V_1 = V_2 = O(-2); "
          "cross-check chi(p_* O_Y) = 1 - 1 - 1 = %d = chi(O_Y) = 1 - g(Y) = %d "
          "(Riemann-Roch on both sides of the cover agrees)"
          % (deg_V[1], deg_V[2], chi_sum, chi_Y),
          deg_V == {1: -2, 2: -2} and chi_sum == chi_Y == -1)

    # F4. the Biswas partner of the decomposable model W = (chi^0+chi^1+chi^2) x O_Y
    wt_sets_ok = all(
        sorted(sp.Rational(j * mi, 3) % 1 for j in range(3))
        == sorted(WEIGHTS) for mi in m_branch)
    E_dec = (0, 2, 2)                                    # O + O(-2) + O(-2), exponents
    deg_dec = -sum(E_dec)
    h0_dec = sum(h0_line(-ai) for ai in E_dec)
    pardeg_dec = deg_dec + 4 * sum(WEIGHTS)
    check("F4 BISWAS IMAGE [new, the answer]: W = (chi^0+chi^1+chi^2) x O_Y has "
          "rank 3, deg 0, isotropy = REGULAR rep at every ramification point "
          "(fractional weights {j m_i/3} = {0,1/3,2/3} at every mark -- verified "
          "for both m_i = 1 and 2); its parabolic partner has underlying bundle "
          "O + O(-2)^2: rank 3 OK, deg %d = -4 OK, par-deg %d = 0 OK -- "
          "integrality AND the sum rule COME OUT of the correspondence; but the "
          "splitting is {0,2,2} with h^0 = %d != 0: the decomposable (trivial-"
          "character) model is exactly the unstable Schur-Horn companion of D2 -- "
          "(1,1,2) is the Biswas image of the STABLE object, and stability "
          "(irreducibility, C1) is the selector"
          % (deg_dec, pardeg_dec, h0_dec),
          wt_sets_ok and deg_dec == -4 and pardeg_dec == 0 and h0_dec == 1)

    # ==================================== G. honest verdict
    check("G1 HONEST VERDICT [recorded]: PROVABLE NOW (standard AG, given [E] "
          "anchors): 'Let V = H^1(P^1 minus mu4; C) (3-dim; 4 marks by v216) carry "
          "a flat irreducible unitary connection with cusp-class local monodromy "
          "(v117); then its Deligne canonical extension E has rank 3, deg -4, "
          "h^0 = 0, and BG forces E = O(-1)^2 + O(-2) -- so g_car = e2 = 5.' "
          "RESIDUALS (P2 stays an axiom): R1 the module identification 'generation "
          "space = this H^1 with this connection' [C] (QGEO.SYM territory); R2 "
          "unitarity (U) [C]; R3 the analytic-monodromy identification [N] (v117 "
          "check 4). NON-CIRCULAR: neither v23's splitting-type input nor v115's "
          "diag(A0) = a/4 input is used; the weight postulate shrinks from "
          "'positive integers summing to 4 (why?)' to 'Deligne + BG + stability, "
          "given the cohomological typing'", True)

    npass = sum(RESULTS)
    print("=" * 100)
    print("SUMMARY: %d/%d checks passed%s"
          % (npass, len(RESULTS),
             "" if npass == len(RESULTS) else "  -- FAILURES PRESENT"))
    return npass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
