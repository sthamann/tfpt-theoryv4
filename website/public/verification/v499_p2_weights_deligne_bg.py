"""v499 -- P2.TYPING.01: the P2 weight-typing postulate HARDENED -- the anchor weights
a = (1,1,2) typed as the Birkhoff-Grothendieck splitting exponents of the DELIGNE
CANONICAL EXTENSION of the flavor connection.  Exact sympy/integer arithmetic, no floats.

v491 (P2.PARTITION.01) reduced g_car = 5 to "3 positive integers summing to 4"; its
check-9 residual was the TYPING: why integers, why positive, why sum 4?  This module
shows that, given already-established [E] anchors, all three become THEOREMS of standard
algebraic geometry:

    THE CONDITIONAL THEOREM (premises fenced below):
    Let V be the 3-dim generation module, identified with H^1(P^1 \\ mu4; C)
    (rank = #marks - 1 = 3; #marks = 4 by Gauss-Bonnet, v216), carrying a flat,
    irreducible, unitary (U) connection whose local monodromy at every mark is the
    cusp class (char poly lam^3 - 1, v117).  Then the Deligne canonical extension E
    (residue eigenvalues in [0,1)) satisfies
      (i)   rank E = 3                                   [rank of V]
      (ii)  deg E = -sum_marks tr Res = -4               [Deligne; trace 1 per mark]
      (iii) h^0(E) = 0                                   [Mehta-Seshadri stability]
      (iv)  E = O(-a1)+O(-a2)+O(-a3), a_i in Z           [Birkhoff-Grothendieck]
    hence a_i >= 1, sum a_i = 4, {a} = {1,1,2} UNIQUE (v491 lemma), g_car = e2 = 5.

  [E]  1-3.  PREMISE MAP.  H^1 basis omega_k = z^(k-1)dz/(z^4-1), k = 1,2,3 (residues
        zeta^k/4, regular at infinity, deck characters i^k; k = 4 = trivial character
        ABSENT, dlog pole at infinity -- rank = #marks - 1 = 3, v137); the SAME 3 as
        coherent cohomology of L = O(-D), D = mu4: h^1(L) = 3 = N_fam, h^0(L) = 0,
        H^0(Omega^1(log D)) = H^0(O(2)) = 3 = the v137 basis, h^0(O(4)) = 5 = g_car
        (v228 index gate); cusp class => canonical residue exponents {0, 1/3, 2/3}
        unique in [0,1) (distinct mod Z => Deligne extension exists, unique, no Jordan
        ambiguity; v117).
  [E]  4-6.  deg E = -4 AS A THEOREM.  mu4-average lemma sum_k U^k X U^-k = 4 diag(X)
        (v115); residue spectrum {0,1/3,2/3} has trace 1 per mark, 4 marks (v216) =>
        deg E = -4; par-deg = 0 (the v39 (U) consistency); infinity APPARENT (monodromy
        product = 1 exactly, (M0 U)^4 = 1, witness exponents diag(2,1,1) integer).
  [E]  7-9.  POSITIVITY AS A THEOREM.  Irreducibility EXACT from v117 (|<U,M0>| = 24 =
        |S4|, sum |chi|^2 = 24; S4 standard x sign -- replaces v38-type sampling); with
        (U) unitarity => Mehta-Seshadri stability => every section-saturation violates
        strict stability (all 324 cases par-deg >= 0) => h^0(E) = 0; BG dictionary
        h^0 = 0 <=> a_i >= 1 (exhaustive window) -- positivity IS h^0 = 0.
  [E] 10-11. UNIQUENESS + SELECTOR.  {a in Z^3 : a_i >= 1, sum = 4} = {(1,1,2)} unique,
        e2 = 5 = g_car, e3 = 2 = |Z2|, e2 - e3 = 3 = N_fam (v491); Schur-Horn
        permutohedron of 4*spec(A0) = (8/3, 4/3, 0) has integer points exactly
        {(2,2,0), (2,1,1)} (the tfpt_2 'Global computation' pair); h^0 = 0 kills
        {0,2,2} (O(0) summand => h^0 = 1) -- the paper's 'balanced' heuristic is now
        TYPED as stability/positivity, and the two routes converge on {1,1,2}.
  [E] 12-15. NEGATIVE CONTROLS.  Drop positivity -> 4 solutions (31 with negatives);
        deg -3 -> e2 = 3, deg -5 -> not unique; n-mark scan: {1,..,1,2} unique for
        EVERY n >= 3 but e2 = (n-2)(n+1)/2 = 5 ONLY at n = 4 -- the VALUE, not the
        uniqueness, is the n = 4 content; MS-rational weights as exponents -> e2 = 16/3
        resp. 44/9, non-integer -- integrality lives on the BUNDLE side.
  [E] 16-18. THE h^1 DISCREPANCY, REAL + RESOLVED.  h^1(O(-2)+O(-1)^2) = 1 != 3
        (chi = deg + rk = -1): the naive typing "generations = H^1 of the rank-3 E" is
        FALSE; forcing it demands deg -6 and loses uniqueness ({1,1,4},{1,2,3},{2,2,2},
        e2 never 5).  Correct TWO-OBJECT typing: generations = H^1(L) = C^3 for the
        LINE bundle L = O(-D) (= H^0(Omega^1(log D)), the v137 basis); E carries them
        as its FIBER (rank 3) with the anchor as splitting type; shared invariants
        rank E = 3 = h^1(L), deg E = -4 = deg L, h^0 = 0 both.  Three DIFFERENT H^1's
        coexist: 3 (generations, L-side), 1 (coherent h^1 of E), 6 = |R+(A3)|
        (local-system deformations); h^1(E(-D)) = 13 = Delta_Q recorded as curiosity.
  [E] 19-22. THE BISWAS COMPUTATION, EXPLICIT (independent convergence witness).  The
        weight denominator is 3 = N_fam, NOT 2 = |Z2|: the Biswas cover is the Z3 cusp
        cover y^3 = (z-1)(z-i)(z+1)^2(z+i)^2 (genus 2 by RH, unramified over infinity;
        an all-equal branch choice is impossible, 4c != 0 mod 3), NOT the pillowcase
        double w^2 = z^4-1 (genus 1, j = 1728 -- the deck side).  p_* O_Y = O + O(-2)^2
        (chi cross-check -1 = -1); the equivariant model W = (chi^0+chi^1+chi^2) x O_Y
        (regular rep at every mark, weights {0,1/3,2/3}) has parabolic partner with
        underlying bundle O + O(-2)^2: rank 3 OK, deg -4 OK, par-deg 0 OK -- integrality
        AND the sum rule COME OUT of the correspondence -- but splitting {0,2,2} with
        h^0 = 1: exactly the UNSTABLE Schur-Horn companion.  (1,1,2) is the Biswas image
        of the STABLE object; stability (irreducibility, v117) is the selector.
  [C]/[N]/[O] 23.  HONEST RESIDUALS (P2 stays an axiom; no marker moves):
        R1  the module identification "generation space = this H^1 with this
            connection" [C] (QGEO.SYM territory);
        R2  unitarity (U) of the flavor monodromy [C] (v33/v40 premise);
        R3  the identification of the ANALYTIC monodromy with the exact W(A3)
            representation [N] (v117 check 4, ODE matching 1e-7).
        NON-CIRCULAR: neither v23's splitting-type input nor v115's diag(A0) = a/4
        input is used; the chain is rank (topology) -> deg (residue trace) ->
        integrality (BG) -> positivity (stability) -> partition (v491); A0* appears
        only as the explicit consistency witness.  The weight postulate shrinks from
        "positive integers summing to 4 (why?)" to "Deligne + BG + stability, given
        the cohomological typing".  DIRECTION-REVERSAL NOTE (inherited from v491):
        tfpt_constants computes N_fam FROM g_car; here the arrow runs marks -> bundle
        -> partition -> g_car -- an over-determination check, not a circle, never
        double-counted in witness tallies.

Status: [E] Formal/Identity (AG arithmetic: Deligne degree, BG dictionary, stability
skeleton, Schur-Horn lattice points, Biswas cover -- sympy exact) + [C] R1/R2 (module
identification, unitarity) + [N] R3 (v117 check 4).  Sharpens v491 (types its check-9
residual); does NOT retire axiom P2; AX.P2.01 stays declared, QGEO.SYM stays [O].
Repo anchors: v216 (marks = 2chi), v137 (H^1 basis), v228 (RR index gate), v115
(mu4-average, A0*), v117 (exact monodromy, S4), v39/v33 (pardeg 0), v491 (partition),
tfpt_2 'Global computation'.  Python (sympy); Wolfram-mirrored (tfpt_readouts_extension.wl)."""
from itertools import combinations_with_replacement, product

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

Z = sp.Symbol('z')
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


def _e2(ms):
    x = list(ms)
    return sum(x[i] * x[j] for i in range(len(x)) for j in range(i + 1, len(x)))


def _h0_line(d):
    """h^0(P^1, O(d))"""
    return d + 1 if d >= 0 else 0


def _h1_line(d):
    """h^1(P^1, O(d)) = h^0(O(-d-2)) (Serre)"""
    return -d - 1 if d <= -2 else 0


def _enumerate_group(gens):
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
    reset()
    print("v499  P2.TYPING.01: the anchor (1,1,2) typed as Deligne/Birkhoff-Grothendieck "
          "splitting data (hardening the v491 weight-typing residual)")

    # ================================================================ A. premise map
    # 1. the generation H^1: basis omega_k, mu4 characters, trivial character absent
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
    check("GENERATION H^1 [E, v137]: omega_k = z^(k-1)dz/(z^4-1), k = 1,2,3 span "
          "H^1(P^1 minus mu4) = C^3 (residues zeta^k/4, regular at infinity, deck "
          "characters i^k); k = 4 carries the TRIVIAL character and has res_inf = -1 "
          "(dlog pole) -- trivial character ABSENT, rank = #marks - 1 = 3",
          all(c == 0 for c in chars) and res_ok and reg_inf)

    # 2. the same 3 as coherent cohomology of the degree -4 line bundle L = O(-D)
    dims = (_h0_line(-4), _h1_line(-4), _h0_line(2), _h0_line(-2 + 4), _h0_line(4))
    check("LINE-BUNDLE CARRIER [E, v228-type RR]: L = O(-D), deg -4: h^0 = %d, "
          "h^1 = %d = N_fam (RR chi = deg+1 = -3; Serre h^1(O(-4)) = h^0(O(2)) = %d); "
          "Omega^1(log D) = O(-2+4) = O(2): h^0 = %d = 3 (the v137 basis IS this "
          "space); function side h^0(O(+4)) = %d = 5 = g_car (v228 index gate)"
          % dims, dims == (0, N_fam, 3, 3, g_car))

    # 3. the cusp class fixes the canonical residue exponents {0,1/3,2/3} in [0,1)
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
    check("CUSP CLASS => CANONICAL EXPONENTS [E, v117]: M0 unitary, M0^3 = 1, char "
          "poly lam^3 - 1; the unique residue eigenvalues in [0,1) with exp(2 pi i a) "
          "= spec M0 are {0, 1/3, 2/3} (distinct mod Z => the Deligne canonical "
          "extension exists and is unique, no Jordan ambiguity)",
          cusp_ok and spec_match and distinct)

    # ============================================== B. deg E = -4 is a THEOREM
    # 4. mu4-average lemma, generic X (v115 check 1, replicated)
    xsym = sp.Matrix(3, 3, lambda i, j: sp.Symbol('x%d%d' % (i, j), complex=True))
    ssum = sp.zeros(3)
    for k in range(4):
        uk = U ** k
        ssum += uk * xsym * uk.inv()
    check("MU4-AVERAGE LEMMA [E, v115]: sum_k U^k X U^-k = 4 diag(X) for generic 3x3 "
          "X (U = diag(1,i,-i)) -- the four residues A_k = U^k A0 U^-k are one mu4 "
          "orbit and their sum is diagonal",
          sp.simplify(sp.expand(ssum - 4 * sp.diag(xsym[0, 0], xsym[1, 1],
                                                   xsym[2, 2]))) == sp.zeros(3))

    # 5. Deligne degree bookkeeping on the explicit witness A0*
    char_ok = sp.simplify(A0STAR.charpoly(lam).as_expr()
                          - lam * (lam - sp.Rational(1, 3))
                          * (lam - sp.Rational(2, 3))) == 0
    traces = [sp.simplify((U ** k * A0STAR * (U ** k).inv()).trace())
              for k in range(4)]
    deg_E = -sum(traces)
    pardeg = deg_E + 4 * sum(WEIGHTS)
    check("deg E = -4 [THEOREM given the cusp class]: residue spec {0,1/3,2/3} has "
          "trace 1 per mark; 4 marks (v216 Gauss-Bonnet) => deg E = -sum_k tr(Res_k) "
          "= %s (Deligne: deg of the canonical extension = -sum of residue traces); "
          "par-deg = deg + 4*(0+1/3+2/3) = %s (the v39 'pardeg 0' (U) consistency); "
          "witness A0* has char poly lam(lam-1/3)(lam-2/3) exactly"
          % (deg_E, pardeg),
          char_ok and traces == [1, 1, 1, 1] and deg_E == -4 and pardeg == 0)

    # 6. flatness across infinity + the integer exponents there (consistency route)
    prod_flat = sp.eye(3)
    for k in range(4):
        uk = U ** k
        prod_flat = sp.expand(prod_flat * (uk * M0 * uk.inv()))
    sumA = sp.simplify(sum((U ** k * A0STAR * (U ** k).inv() for k in range(4)),
                           sp.zeros(3)))
    off_zero = all(sp.simplify(sumA[i, j]) == 0
                   for i in range(3) for j in range(3) if i != j)
    eig_inf = sorted([sumA[i, i] for i in range(3)], reverse=True)
    check("REGULAR INFINITY [E, v117/v115]: monodromy at infinity = "
          "prod_k U^k M0 U^-k = 1 exactly and (M0 U)^4 = 1 -- infinity is an "
          "APPARENT singularity (integer exponents); on the witness: sum_k A_k = "
          "4 diag(A0*) = diag(2,1,1), eigenvalues %s in Z^3, sum 4 -- consistent "
          "with BG integrality but NOT used for the uniqueness below"
          % (eig_inf,),
          sp.simplify(prod_flat) == sp.eye(3)
          and sp.simplify((M0 * U) ** 4) == sp.eye(3)
          and off_zero and eig_inf == [2, 1, 1])

    # ============================================== C. h^0(E) = 0 is a THEOREM
    # 7. irreducibility is EXACT: <U, M0> has order 24 and sum |chi|^2 = |G|
    elems = _enumerate_group([U, M0])
    chi2 = sp.Integer(0)
    for x in elems:
        tr = sp.expand(x.trace())
        chi2 += sp.expand(tr * sp.conjugate(tr))
    check("IRREDUCIBILITY EXACT [E, v117]: |<U, M0>| = %d = |W(A3)| = |S4| and "
          "sum_g |tr g|^2 = %s = |G| -- the 3-dim monodromy representation is "
          "IRREDUCIBLE (standard x sign of S4); with (U) unitarity this is the "
          "Mehta-Seshadri stability input (replaces v38-type sampling)"
          % (len(elems), sp.simplify(chi2)),
          len(elems) == 24 and sp.simplify(chi2 - 24) == 0)

    # 8. stability => h^0 = 0 (the inequality skeleton, exhaustively)
    # a nonzero section O -> E saturates to a line bundle with deg d >= 0; its
    # parabolic degree is d + (one induced weight per mark) >= 0 = par-slope(E);
    # STRICT stability demands par-deg < 0 -- contradiction in EVERY case:
    viol = []
    for d in range(0, 4):
        for wsel in product(WEIGHTS, repeat=4):
            pdeg = d + sum(wsel)
            if pdeg < 0:                      # would satisfy stability -> no clash
                viol.append((d, wsel))
    check("STABILITY => h^0(E) = 0 [THEOREM given irreducibility + (U)]: every "
          "candidate section-saturation (deg d >= 0, any induced weights from "
          "{0,1/3,2/3} at the 4 marks) has par-deg = d + sum w >= 0 = par-slope(E) "
          "-- checked all %d cases, 0 satisfy the strict-stability bound par-deg < 0 "
          "=> no global sections (the v137 'trivial character absent' correlate, "
          "now typed)" % (4 * 3 ** 4), viol == [])

    # 9. the BG dictionary: h^0 = 0 <=> all splitting exponents >= 1
    dict_ok = True
    for a in product(range(-3, 7), repeat=3):
        h0 = sum(_h0_line(-ai) for ai in a)
        if (h0 == 0) != all(ai >= 1 for ai in a):
            dict_ok = False
    check("BG DICTIONARY [E]: for E = O(-a1)+O(-a2)+O(-a3), h^0(E) = "
          "sum max(0, 1 - a_i) = 0 <=> a_i >= 1 for all i (window a_i in [-3,6], "
          "exhaustive) -- POSITIVITY of the anchor IS h^0 = 0; integrality itself is "
          "Birkhoff-Grothendieck (every holomorphic bundle on P^1 splits with integer "
          "degrees), automatic once E is typed as a bundle", dict_ok)

    # ==================================== D. uniqueness + convergence + controls
    # 10. the partition lemma under the full typing
    sols = [m for m in combinations_with_replacement(range(1, 11), 3) if sum(m) == 4]
    check("UNIQUENESS [E, v491]: {a in Z^3 : a_i >= 1 (h^0 = 0), sum a_i = 4 "
          "(deg E = -4), 3 parts (rank 3)} = %s -- unique; e2 = %d = g_car, "
          "e3 = %d = |Z2|, e2 - e3 = %d = N_fam"
          % (sols, _e2(sols[0]), sols[0][0] * sols[0][1] * sols[0][2],
             _e2(sols[0]) - 2),
          sols == [(1, 1, 2)] and _e2(sols[0]) == g_car
          and _e2(sols[0]) - sols[0][0] * sols[0][1] * sols[0][2] == N_fam)

    # 11. Schur-Horn route converges (the tfpt_2 theorem, with 'balance' TYPED)
    bound = [sp.Rational(8, 3), sp.Rational(4, 1)]      # partial sums of 4*(2/3,1/3)
    sh = []
    for a in product(range(0, 3), repeat=3):            # diag in [0, 2/3] => a_i in {0,1,2}
        s = sorted(a, reverse=True)
        if sum(s) == 4 and s[0] <= bound[0] and s[0] + s[1] <= bound[1]:
            if tuple(s) not in sh:
                sh.append(tuple(s))
    survivors = [s for s in sh if all(x >= 1 for x in s)]
    check("SCHUR-HORN CONVERGENCE [E, tfpt_2 'Global computation']: integer points "
          "of the permutohedron of 4*spec(A0) = (8/3, 4/3, 0) with sum 4 = %s "
          "(exactly the paper's two options); h^0 = 0 kills {2,2,0} (contains O(0), "
          "h^0 = 1) => %s -- the paper's 'balanced' selection is now TYPED as "
          "positivity/stability, and the two routes converge on {1,1,2}"
          % (sorted(sh), survivors),
          sorted(sh) == [(2, 1, 1), (2, 2, 0)] and survivors == [(2, 1, 1)])

    # 12. negative control: drop positivity
    nc0 = [m for m in combinations_with_replacement(range(0, 5), 3) if sum(m) == 4]
    ncz = [m for m in combinations_with_replacement(range(-5, 10), 3) if sum(m) == 4]
    e2s0 = sorted(set(_e2(m) for m in nc0))
    e2sz = set(_e2(m) for m in ncz)
    check("NEGATIVE CONTROL / POSITIVITY [E, v491]: allowing a_i = 0 gives %d "
          "solutions, e2 ambiguous %s; allowing negatives (window [-5,9]) gives %d "
          "solutions, %d distinct e2 values -- h^0 = 0 is load-bearing"
          % (len(nc0), e2s0, len(ncz), len(e2sz)),
          len(nc0) == 4 and e2s0 == [0, 3, 4, 5] and len(ncz) == 31
          and len(e2sz) == 29 and 5 in e2sz)

    # 13. negative control: drop the degree fixing
    nc3 = [m for m in combinations_with_replacement(range(1, 11), 3) if sum(m) == 3]
    nc5 = [m for m in combinations_with_replacement(range(1, 11), 3) if sum(m) == 5]
    check("NEGATIVE CONTROL / DEGREE [E, v491]: deg -3 -> unique but e2 = %d != 5; "
          "deg -5 -> %d solutions (not unique) -- deg E = -4 = -#marks is "
          "load-bearing" % (_e2(nc3[0]), len(nc5)),
          len(nc3) == 1 and _e2(nc3[0]) == 3 and len(nc5) == 2)

    # 14. negative control: the mark count (n marks => n-1 parts summing to n)
    marks_scan = {}
    for n in range(3, 9):
        s = [m for m in combinations_with_replacement(range(1, n + 1), n - 1)
             if sum(m) == n]
        marks_scan[n] = (len(s), _e2(s[0]))
    formula_ok = all(marks_scan[n][1] == (n - 2) * (n + 1) // 2 for n in marks_scan)
    check("NEGATIVE CONTROL / MARK COUNT [E]: n marks => n-1 positive parts summing "
          "to n; the partition {1,..,1,2} is unique for EVERY n >= 3 (uniqueness is "
          "generic!), but e2 = (n-2)(n+1)/2 = %s -- e2 = 5 = g_car picks out n = 4 "
          "alone: the VALUE, not the uniqueness, is the n = 4 content"
          % ({n: v[1] for n, v in marks_scan.items()}),
          all(v[0] == 1 for v in marks_scan.values()) and formula_ok
          and [n for n, v in marks_scan.items() if v[1] == 5] == [4])

    # 15. negative control: MS-rational weights typed directly as exponents
    w1 = [sp.Rational(1, 3)] * 3
    w2 = [sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)]
    e2w = [_e2([4 * x for x in w]) for w in (w1, w2)]
    check("NEGATIVE CONTROL / INTEGRALITY [E, v491]: typing the RATIONAL MS weights "
          "directly as exponents (scaled by 4) gives e2 = %s and %s, both != 5 and "
          "not integers -- integrality lives on the BUNDLE side (BG splitting of "
          "the Deligne extension), not on the parabolic side"
          % (e2w[0], e2w[1]),
          e2w == [sp.Rational(16, 3), sp.Rational(44, 9)])

    # ==================================== E. the h^1 discrepancy, resolved
    # 16. h^1 of the anchor bundle is 1, not 3; the carrier of the generations is L
    a_anchor = (1, 1, 2)
    h1E = sum(_h1_line(-ai) for ai in a_anchor)
    chiE = sum((-ai) + 1 for ai in a_anchor)            # RR: chi(O(d)) = d + 1
    check("THE h^1 DISCREPANCY [E, resolved]: h^1(O(-2)+O(-1)^2) = sum(a_i - 1) = "
          "%d != 3 and chi(E) = deg + rk = %d (RR) -- the naive typing 'generation "
          "space = H^1(E)' is FALSE.  Correct two-object typing: generations = "
          "H^1(L) = C^3 for L = O(-D); E carries them as its FIBER (rank 3) with "
          "the anchor as splitting type; shared invariants rank E = 3 = h^1(L), "
          "deg E = -4 = deg L, h^0(E) = 0 = h^0(L)"
          % (h1E, chiE),
          h1E == 1 and chiE == -1
          and 3 == _h1_line(-4) and -4 == sum(-ai for ai in a_anchor)
          and sum(_h0_line(-ai) for ai in a_anchor) == 0 == _h0_line(-4))

    # 17. negative control: forcing 'generations = H^1(rank-3 E)' breaks everything
    forced = [m for m in combinations_with_replacement(range(1, 8), 3)
              if sum(x - 1 for x in m) == 3]
    check("NEGATIVE CONTROL / NAIVE TYPING [E]: demanding h^1(E') = 3 with "
          "h^0(E') = 0 for a rank-3 E' forces sum a_i = 6, i.e. deg = -6 != -4, "
          "and the splitting is NOT unique: %s with e2 = %s -- never 5.  The "
          "two-object typing is load-bearing"
          % (forced, [_e2(m) for m in forced]),
          forced == [(1, 1, 4), (1, 2, 3), (2, 2, 2)]
          and [_e2(m) for m in forced] == [9, 11, 12]
          and all(sum(m) == 6 for m in forced))

    # 18. observations (exact, but NOT load-bearing -- recorded as curiosities)
    h1_EtwD = sum(_h1_line(-ai - 4) for ai in a_anchor)   # E(-D) = O(-6)+O(-5)^2
    h1_locsys = -3 * (2 - 4)                              # -chi = -rk*chi_top
    check("OBSERVATION [E arithmetic, curiosity, not load-bearing]: h^1(E(-D)) = "
          "5+4+4 = %d = Delta_Q (the 13 of v115's (8,0,5)/144 lemma), and h^1 of "
          "the rank-3 flavor LOCAL SYSTEM on P^1 minus mu4 is -chi = 3*(4-2) = %d "
          "= |R+(A3)| -- three DIFFERENT H^1's coexist: 3 (generations, L-side), "
          "1 (coherent h^1 of E), 6 (local-system deformations); the discrepancy "
          "came from conflating them"
          % (h1_EtwD, h1_locsys),
          h1_EtwD == 13 and h1_locsys == 6)

    # ==================================== F. the Biswas correspondence, explicit
    # 19. the pillowcase double (deck side): genus 1, j = 1728 -- NOT the weight cover
    g2 = sp.Rational(2 * 0 - 2) * 2 + 4 * (2 - 1)        # RH: 2g-2 = N(2g_X-2)+sum(e-1)
    genus_z2 = (g2 + 2) / 2
    lam_cr = sp.Rational(2)                              # cross-ratio of mu4 (v214)
    j_inv = 256 * (lam_cr ** 2 - lam_cr + 1) ** 3 / (lam_cr ** 2 * (lam_cr - 1) ** 2)
    check("DECK COVER [E, v214-type]: w^2 = z^4 - 1 (Z2, branched at mu4, deg 4 "
          "even => unramified over infinity): Riemann-Hurwitz genus = %s = 1, "
          "cross-ratio 2 => j = %s = 1728 (the tau = i pillowcase double) -- "
          "denominator 2 = |Z2|: this is the DECK-side cover, not the Biswas cover "
          "for the weights (denominator 3 = N_fam)" % (genus_z2, j_inv),
          genus_z2 == 1 and j_inv == 1728)

    # 20. the Z3 cusp cover exists only with asymmetric branch data (1,1,2,2)
    all_equal_bad = all((4 * c) % 3 != 0 for c in (1, 2))
    m_branch = (1, 1, 2, 2)
    branch_ok = sum(m_branch) % 3 == 0
    degq = sum(m_branch)                                 # q = (z-1)(z-i)(z+1)^2(z+i)^2
    unram_inf = degq % 3 == 0
    g3 = 3 * (2 * 0 - 2) + 4 * (3 - 1)                   # 4 totally ramified points
    genus_z3 = sp.Rational(g3 + 2, 2)
    check("BISWAS COVER [E, explicit]: a Z3 cover killing the weight denominator "
          "3 = N_fam cannot have equal local monodromies (4c mod 3 != 0 for "
          "c = 1,2); the choice m = (1,1,2,2) works (sum 6 = 0 mod 3, deg q = 6 => "
          "unramified over infinity); Riemann-Hurwitz genus = %s = 2 -- the cusp "
          "cover Y: y^3 = (z-1)(z-i)(z+1)^2(z+i)^2 is a genus-2 curve with Z3 "
          "action, NOT the pillowcase double" % genus_z3,
          all_equal_bad and branch_ok and unram_inf and genus_z3 == 2)

    # 21. eigensheaf degrees of p_* O_Y by explicit pole bookkeeping + chi cross-check
    deg_V = {}
    for j in (1, 2):
        # allowed pole of g at mark i: floor(j*m_i/3); at infinity ord(y^j) = -2j
        deg_V[j] = sum((j * mi) // 3 for mi in m_branch) - 2 * j
    chi_sum = (0 + 1) + (deg_V[1] + 1) + (deg_V[2] + 1)  # chi(O(d)) = d+1 on P^1
    chi_Y = 1 - 2                                        # 1 - g(Y)
    check("EIGENSHEAVES [E, explicit]: p_* O_Y = O + V_1 + V_2 with "
          "deg V_j = sum_i floor(j m_i / 3) - 2j = (%d, %d) => V_1 = V_2 = O(-2); "
          "cross-check chi(p_* O_Y) = 1 - 1 - 1 = %d = chi(O_Y) = 1 - g(Y) = %d "
          "(Riemann-Roch on both sides of the cover agrees)"
          % (deg_V[1], deg_V[2], chi_sum, chi_Y),
          deg_V == {1: -2, 2: -2} and chi_sum == chi_Y == -1)

    # 22. the Biswas partner of the decomposable model W = (chi^0+chi^1+chi^2) x O_Y
    wt_sets_ok = all(
        sorted(sp.Rational(j * mi, 3) % 1 for j in range(3))
        == sorted(WEIGHTS) for mi in m_branch)
    E_dec = (0, 2, 2)                                    # O + O(-2) + O(-2), exponents
    deg_dec = -sum(E_dec)
    h0_dec = sum(_h0_line(-ai) for ai in E_dec)
    pardeg_dec = deg_dec + 4 * sum(WEIGHTS)
    check("BISWAS IMAGE [E, the independent witness]: W = (chi^0+chi^1+chi^2) x O_Y "
          "has rank 3, deg 0, isotropy = REGULAR rep at every ramification point "
          "(fractional weights {j m_i/3} = {0,1/3,2/3} at every mark, both m_i = 1 "
          "and 2); its parabolic partner has underlying bundle O + O(-2)^2: rank 3 "
          "OK, deg %d = -4 OK, par-deg %d = 0 OK -- integrality AND the sum rule "
          "COME OUT of the correspondence; but the splitting is {0,2,2} with "
          "h^0 = %d != 0: the decomposable (trivial-character) model is exactly the "
          "unstable Schur-Horn companion -- (1,1,2) is the Biswas image of the "
          "STABLE object, and stability (irreducibility, v117) is the selector"
          % (deg_dec, pardeg_dec, h0_dec),
          wt_sets_ok and deg_dec == -4 and pardeg_dec == 0 and h0_dec == 1)

    # ==================================== G. honest verdict
    # 23. residual map (recorded; P2 stays an axiom, no marker moves)
    check("HONEST RESIDUALS [C/N recorded]: THE CONDITIONAL THEOREM (standard AG, "
          "given [E] anchors): 'Given 4 marks (v216), rank 3 (v137), cusp class "
          "(v117), irreducibility (v117) and (U): Deligne + BG + stability force "
          "E = O(-1)^2 + O(-2), so a = {1,1,2} and g_car = e2 = 5.'  RESIDUALS: R1 "
          "module identification 'generation space = this H^1 with this connection' "
          "[C] (QGEO.SYM territory, stays [O]); R2 unitarity (U) [C] (v33/v40); R3 "
          "analytic-monodromy identification [N] (v117 check 4).  NON-CIRCULAR: "
          "neither v23's splitting-type input nor v115's diag(A0) = a/4 input is "
          "used; the weight postulate shrinks from 'positive integers summing to 4 "
          "(why?)' to 'Deligne + BG + stability, given the cohomological typing'.  "
          "AX.P2.01 stays a declared axiom; direction reversal (marks -> bundle -> "
          "g_car) is an over-determination check, never double-counted", True)

    return summary("v499 P2.TYPING.01: the v491 weight-typing residual hardened -- rank 3 "
                   "(topology) + deg E = -4 (Deligne residue trace) + integrality (Birkhoff-"
                   "Grothendieck) + positivity (Mehta-Seshadri stability, h^0 = 0) type the anchor "
                   "as E = O(-1)^2 + O(-2), so {1,1,2} and g_car = 5 follow; h^1 discrepancy "
                   "resolved by the two-object typing (L = O(-D) carries the generations); Biswas "
                   "Z3-cover computed explicitly (independent convergence, stability the selector); "
                   "P2 stays an axiom (R1/R2 [C], R3 [N])")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
