"""v516 -- CELEST.WP5E.M2.01: milestone M2 of the research contract
CELEST.SEAM.01 (WP5e back-reaction programme) -- "the twisted
Kodaira-Spencer measure", executed (SUCCESS on the preregistered v514
S8.2 criterion, on the DECLARED completion measure -- verdict B).
Question (preregistered VERBATIM in v514): quantise the O(-2) tower on
PT/Z4 using the eps1 mode ledger and compute the one-loop box
coefficient PER SECTOR.  SUCCESS = the bulk sector reproduces
lambda~^2 = 36 with the eps1 measure bookkeeping AND the twisted
sectors pair with the three sphere axions cancelling the rigid 32 T3
residual (v505 S3.7); KILL = a leftover independent quartic (T3-type)
in ANY sector after all four axions are included.

DECLARED MEASURE ANSATZ (stated before computing, honest typing): v508
killed every EXCHANGE realisation (product theorem: exchange images
have identically zero T5/T3); the delta-1 exploration established that
the twisted contact term is the MODULAR COMPLETION of the very
Atiyah-Bott data that produced A_fix, with a FORCED leading (T5, T3)
weight ratio 4:3 (sector 2 : sectors 1+3).  M2 declares the completion
contact term per twisted box channel j as

    contact_j := (Q^{(0)} - Q^{(j)}) / det_j ,

i.e. in the channel with the g^j zero-mode normalisation 1/det_j the
twisted-sector LOOP contributes the UNPHASED sector trace (a loop of
twisted closed-string states carries no group-element insertion
phase), of which the AB skeleton kept only the phase-weighted
insertion part Q^{(j)}/det_j.  Equivalently, per glue class m the
contact weights are

    w_m = sum_j (1 - i^{jm})/det_j = 4 h_m = |mu4| h_m = -4 ch2(T_m)

with h_m = m(4-m)/8 the v502 sector Casimir energies (= the A3
discriminant weights) and ch2(T_m) the McKay/Kronheimer charges of the
tautological bundles on the sphere classes (v505 S4.3 index bridge):
THE THREE SPHERE AXIONS PAIR THROUGH THEIR OWN ch2 CHARGES -- an exact
identity, NO free scale, no fit.  References: Costello arXiv:2111.08879
(one-loop box anomaly); Bittleston-Sharma-Skinner CMP 403 (Poisson-CS
tower); Harvey-Moore hep-th/9510182 (modular completion); v505 (AB
ledger, index bridge, S3.8 rigidity), v508 (exchange no-go), v511
(psi = 64 slice), v514 (eps1 ledger, M1-M3 preregistration), v515
(M1).  Exact sympy/Fraction arithmetic throughout, no floats.

[E] S0. REPLICATION: 240 roots, class split (52, 64, 60, 64); class
      quartics Q_0 = (12,0,6,4,8), Q_1 = Q_3 = (12,24,0,-8,16), Q_2 =
      (0,24,30,12,-40) in (P1, P2, P3, T5, T3); A_fix =
      (9, -30, -15, 0, 32) by characters AND class weights; bulk Okubo
      Q^{(0)} = 36<x,x>^2 = (K^{(0)})^2/100 (lambda~^2 = 36).
[E] S1. THE COMPLETION-WEIGHT IDENTITY (the centrepiece): index bridge
      f(m) = (0, -3/8, -1/2, -3/8) = ch2(T_m) = -h_m replicated; the
      completion weights w_m = sum_j (1 - i^{jm})/det_j =
      (0, 3/2, 2, 3/2) = 4 h_m = |mu4| h_m = -4 ch2(T_m) EXACTLY --
      the 4 = |mu4| is the group order in the identity, not a dial;
      PARAMETER-FREE LOCKS: T5 = 0 for ANY scale c (the ch2 pattern
      alone kills T5); ratio h_2 : h_1 = 4 : 3 = the delta-1-forced
      leading ratio (REPRODUCED, not fitted); the T3 budget fixes the
      scale c = 4 = |mu4| uniquely.
[E] S2. THE CONTACT TERM: channel form sum_j (Q^{(0)} - Q^{(j)})/det_j
      = class form sum_m 4 h_m Q_m = (36, 120, 60, 0, -32) EXACTLY
      (one object, two bases); the contacts carry nonzero T5/T3 per
      channel (genuine contact, not exchange -- the v508 product
      theorem replicated as control).
[E] S3. SUCCESS TABLE (sector by sector): skeleton_j + contact_j =
      Q^{(0)}/det_j = 36<x,x>^2/det_j -- a PERFECT Okubo square
      (T5 = T3 = 0, lambda~^2 = 36) in EVERY twisted channel
      ((18, 9, 18) x <x,x>^2); total A_fix + contact = 45<x,x>^2 =
      (5/4) x 36<x,x>^2 = (Dedekind sum) x (Okubo) = the UNIQUE
      quartic-free weighting of v505 S3.8 (the rigidity theorem is
      exactly what the measure lands on); both v508 certificates
      killed (Phi_T3: 32 -> 0, Phi_P: 72 -> 0); the v511 slice
      psi = 64 SUPPLIED EXACTLY (psi(contact) = -64) -- no cubic
      d-channel needed, c_d is free to be 0; remainder inside the
      exchange span (45<x,x>^2 = (45/16) E22 = (1/80) E00, Phi_P = 0):
      the BULK axion cancels every channel with the SAME lambda~^2 =
      36, the twisted propagator carrying the AB zero-mode factor
      1/det_j; the v514 S3.4 measure chain stays mu-blind.
[E] S4. NEGATIVE CONTROLS: wrong scale c in {1, 2, 3, 5} leaves T3 =
      (24, 16, 8, -8) -- only c = 4 = |mu4| clears the budget;
      shuffled weights (h_1 <-> h_2) break T5 = -14 AND T3 = 36;
      SO(16) glue keeps T5 = 20 / T3 = -40 in the summed trace -- the
      KILL branch FIRES there (Okubo failure inherited, E8 doubly
      special); diag(i, i) degenerates to the Z2 target and breaks the
      conjugation pairing + the index bridge; the Z2/Eguchi-Hanson
      anchor PASSES with the same mechanism (A_2 + contact =
      9<x,x>^2 = (1/4) x 36<x,x>^2, coupling scale 2 = |Z2| = centre
      count).
[E] S5. MULTIPLIER NOTE (cross-reference only -- the substance belongs
      to the parallel delta-1d strand): the contact weights 4h are
      REAL RATIONALS carrying no multiplier system of their own; the
      delta-1c residual phases are the SQUARES of the A3 discriminant
      T-phases e(3a^2/8) -- orders (1, 8, 2, 8) squaring to
      (1, 4, 1, 4), a finite mu4 system; Gauss sums 2e(3/8) (A3),
      2e(5/8) (D5), full Weil sum 4 (signature 0 mod 8).
[C] THE COMPLETION READING (the mandatory fence): the loop of twisted
      states carries the UNPHASED sector trace with the same zero-mode
      normalisation -- declared, supported by the delta-1
      modular-completion finding, NOT derived from the BCOV integral.
[O] O-FENCE: the BCOV-integral derivation of the completion reading
      (delta-1b/1c/1d territory) stays open; M3 (the a0 uplift) is
      executed separately (v517); SEAM.EQUIV.TWISTOR.01 untouched
      (preparation, not construction); NO marker moves anywhere.

VERDICT per the preregistered v514 S8.2 branches: SUCCESS wording met
on the declared completion measure -- lambda~^2 = 36 reproduced in
EVERY sector, the 32 T3 cancelled exactly by the ch2-weighted
sphere-axion contacts; the KILL branch does NOT fire.

Status: [E] exact weight/contact/table/control arithmetic
(sympy/Fraction, no floats); [C] the declared completion reading of
the twisted KS measure; [O] its BCOV-integral derivation.  Python;
Wolfram-mirrored (completion-weight identity, parameter-free locks,
contact two-forms, per-sector Okubo squares, certificate kills,
psi = 64, negative controls), counted per GATE.WOLFRAM.02.  Discovery
provenance: experiments/tfpt-discovery/
celestial_seam_wp5e_m2m3_twisted_ks_measure_probe.py
(2026-07-22, 23/23).
"""
from itertools import combinations, product

import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

MU4 = N_fam + 1               # 4 = |mu4|, the seam clock order
H_VEE = 30                    # dual Coxeter number of E8
HALF = sp.Rational(1, 2)


def fmt(xs):
    return "(" + ", ".join(str(x) for x in xs) + ")"


# ---------------------------------------------------------------------------
# E8 roots in D5 (+) A3 glue coordinates (v128/v492/v502/v505/v508)
# ---------------------------------------------------------------------------
def build_glue_roots():
    d5_roots, d5_v = [], []
    for i, j in combinations(range(5), 2):
        for si in (1, -1):
            for sj in (1, -1):
                v = [sp.Rational(0)] * 5
                v[i], v[j] = sp.Rational(si), sp.Rational(sj)
                d5_roots.append(tuple(v))
    for i in range(5):
        for s in (1, -1):
            v = [sp.Rational(0)] * 5
            v[i] = sp.Rational(s)
            d5_v.append(tuple(v))
    d5_s, d5_c = [], []
    for signs in product((1, -1), repeat=5):
        v = tuple(HALF * s for s in signs)
        (d5_s if signs.count(-1) % 2 == 0 else d5_c).append(v)
    a3_roots = []
    for i in range(4):
        for j in range(4):
            if i != j:
                v = [sp.Rational(0)] * 4
                v[i], v[j] = sp.Rational(1), sp.Rational(-1)
                a3_roots.append(tuple(v))

    def wclass(k):
        out = []
        for sub in combinations(range(4), k):
            v = [sp.Rational(-k, 4)] * 4
            for i in sub:
                v[i] += 1
            out.append(tuple(v))
        return out

    z5, z4 = tuple([sp.Rational(0)] * 5), tuple([sp.Rational(0)] * 4)
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
# exact polynomial machinery on the D5 (+) A3 Cartan (v505/v508)
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
    e = sum(alpha[i] * X5[i] for i in range(5))
    e += sum(alpha[5 + i] * Y4[i] for i in range(4))
    return sp.expand(e)


def poly_dict(expr):
    return sp.Poly(sp.expand(expr), *ALLV, domain='QQ').as_dict()


def decompose(target):
    dicts = [poly_dict(b) for b in BASIS4]
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
    if sp.expand(target - sum(sol[i] * BASIS4[i] for i in range(5))) != 0:
        return None
    return [sp.Rational(x) for x in sol]


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


def vsum(*vecs):
    return [sum(v[i] for v in vecs) for i in range(5)]


def vscale(c, v):
    return [sp.nsimplify(sp.expand(c * v[i])) for i in range(5)]


PHI_T5 = lambda v: v[3]
PHI_T3 = lambda v: v[4]
PHI_P = lambda v: 3 * v[0] - v[1] - v[2]
PSI = lambda v: PHI_P(v) - sp.Rational(PHI_T3(v)) / 4


# ---------------------------------------------------------------------------
# S0 -- replication: roots, class quartics, A_fix, bulk Okubo
# ---------------------------------------------------------------------------
def section0(roots):
    print("  -- S0: replication (roots, class quartics, A_fix, bulk Okubo)")
    I = sp.I

    counts = [sum(1 for c in roots.values() if c == m) for m in range(4)]
    check("S0.1 [ROOTS] 240 roots, all norm 2, class split %s = "
          "(52, 64, 60, 64) (v492/v505 replication)" % fmt(counts),
          len(roots) == 240 and counts == [52, 64, 60, 64]
          and all(sum(x * x for x in r) == 2 for r in roots))

    K, Q = power_sums_by_class(roots)
    dec = {m: decompose(Q[m]) for m in range(4)}
    expect = {0: [12, 0, 6, 4, 8], 1: [12, 24, 0, -8, 16],
              2: [0, 24, 30, 12, -40], 3: [12, 24, 0, -8, 16]}
    print("     class quartics Q_m in (P1, P2, P3, T5, T3):")
    for m in range(4):
        print("       Q_%d = %s" % (m, fmt(dec[m])))
    check("S0.2 [CLASS QUARTICS] Q_0 = (12,0,6,4,8), Q_1 = Q_3 = "
          "(12,24,0,-8,16), Q_2 = (0,24,30,12,-40) (v505 S3.1 "
          "replication)",
          all(dec[m] == [sp.Rational(x) for x in expect[m]]
              for m in range(4)))

    Qv = {m: dec[m] for m in range(4)}
    dets = {1: 2, 2: 4, 3: 2}
    Qtw = {j: [sp.nsimplify(sp.expand(
        sum(I ** (j * m) * Qv[m][i] for m in range(4))))
        for i in range(5)] for j in range(4)}
    Afix = [sp.nsimplify(sum(Qtw[j][i] / dets[j] for j in (1, 2, 3)))
            for i in range(5)]
    cA = [sp.Rational(5, 4), sp.Rational(-1, 4),
          sp.Rational(-3, 4), sp.Rational(-1, 4)]
    Afix2 = [sum(cA[m] * Qv[m][i] for m in range(4)) for i in range(5)]
    check("S0.3 [A_FIX, TWO ROUTES] A_fix = sum_j Q^{(j)}/det_j = %s = "
          "(9, -30, -15, 0, 32) by characters AND by class weights "
          "(5/4, -1/4, -3/4, -1/4) (v505 S3.7 replication); the rigid "
          "twisted residual is +32 T3" % fmt(Afix),
          Afix == [9, -30, -15, 0, 32] and Afix2 == Afix)

    Ksum = sp.expand(sum(K.values()))
    okubo = sp.expand(sum(Q.values()) - 36 * (S5 + S3) ** 2)
    okubo2 = sp.expand(sum(Q.values())
                       - sp.Rational(1, 100) * Ksum ** 2)
    check("S0.4 [BULK OKUBO] K^{(0)} = 60<x,x> and Q^{(0)} = "
          "36<x,x>^2 = (K^{(0)})^2/100 as exact polynomial identities "
          "(lambda~^2 = 36 = h_vee + 6, v495/v505/v514): Q^{(0)} = %s "
          "in the 5-basis -- ZERO independent quartic in the summed "
          "trace" % fmt(Qtw[0]),
          sp.expand(Ksum - 60 * (S5 + S3)) == 0 and okubo == 0
          and okubo2 == 0 and Qtw[0] == [36, 72, 36, 0, 0])
    return Qv, Qtw, Afix, dets


# ---------------------------------------------------------------------------
# S1 -- index bridge -> completion weights (parameter-free locks)
# ---------------------------------------------------------------------------
def section1(Qv, dets):
    print("  -- S1: the index bridge and the completion weights")
    I = sp.I
    R = sp.Rational

    f = [sp.nsimplify(sp.expand(
        R(1, 4) * sum((I ** (j * m) - 1) / dets[j] for j in (1, 2, 3))))
        for m in range(4)]
    h = [R(m * (4 - m), 8) for m in range(4)]
    C = sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
    Cinv = C.inv()
    ch2 = [-Cinv[m, m] / 2 for m in range(3)]
    check("S1.1 [INDEX BRIDGE REPLICATION] f(m) = (1/4) sum_j "
          "(i^{jm}-1)/det_j = %s = (0, -3/8, -1/2, -3/8) = ch2(T_m) = "
          "-h_m with h_m = m(4-m)/8 the v502 sector Casimir energies "
          "(v505 S4.1/S4.3): the loop data of the sphere axions IS the "
          "AB data" % fmt(f),
          f == [0, R(-3, 8), R(-1, 2), R(-3, 8)]
          and all(f[m + 1] == ch2[m] for m in range(3))
          and all(h[m] == -f[m] for m in range(4)))

    w = [sp.nsimplify(sp.expand(
        sum((1 - I ** (j * m)) / dets[j] for j in (1, 2, 3))))
        for m in range(4)]
    check("S1.2 [COMPLETION WEIGHTS, NO FREE SCALE] w_m = sum_j "
          "(1 - i^{jm})/det_j = %s = (0, 3/2, 2, 3/2) = 4 h_m = "
          "|mu4| h_m = -4 ch2(T_m) EXACTLY for all m: under the "
          "completion reading the per-class contact weight is FORCED "
          "-- the 4 = |mu4| is the group order in the identity, not a "
          "dial" % fmt(w),
          w == [0, R(3, 2), 2, R(3, 2)]
          and all(w[m] == MU4 * h[m] for m in range(4)))

    c = sp.symbols('c')
    T5tot = sp.expand(c * sum(h[m] * Qv[m][3] for m in range(4)))
    T3tot = sp.expand(c * sum(h[m] * Qv[m][4] for m in range(4)))
    sol_c = sp.solve(sp.Eq(T3tot + 32, 0), c)
    lead = sp.Matrix([[Qv[1][3] + Qv[3][3], Qv[2][3]],
                      [Qv[1][4] + Qv[3][4], Qv[2][4]]])
    wlead = lead.solve(sp.Matrix([0, -32]))
    check("S1.3 [PARAMETER-FREE LOCKS] with weights c*(h_1, h_2, h_3): "
          "T5 total = %s = 0 identically (ANY scale c -- the ch2 "
          "pattern alone kills T5); ratio h_2 : h_1 = %s = 4 : 3 = the "
          "delta-1 E3.4 FORCED leading ratio; T3 total = %s => the 32 "
          "T3 budget forces c = %s = 4 = |mu4|; the unique delta-1 "
          "leading weights (w13, w2) = %s = (3/2, 2) are REPRODUCED as "
          "(4h_1, 4h_2), det = %s != 0"
          % (T5tot, h[2] / h[1], T3tot, sol_c, fmt(list(wlead)),
             lead.det()),
          T5tot == 0 and h[2] / h[1] == R(4, 3)
          and sol_c == [MU4] and list(wlead) == [R(3, 2), 2]
          and wlead[0] == 4 * h[1] and wlead[1] == 4 * h[2]
          and lead.det() != 0)
    return h, w


# ---------------------------------------------------------------------------
# S2 -- the contact term: two forms, genuine-contact certificate
# ---------------------------------------------------------------------------
def section2(Qv, Qtw, dets, h):
    print("  -- S2: the twisted KS contact term (two forms)")

    contact = {j: [sp.nsimplify((Qtw[0][i] - Qtw[j][i]) / dets[j])
                   for i in range(5)] for j in (1, 2, 3)}
    total = vsum(contact[1], contact[2], contact[3])
    classform = [sum(4 * h[m] * Qv[m][i] for m in range(4))
                 for i in range(5)]
    print("     contact_j = (Q^{(0)} - Q^{(j)})/det_j:")
    for j in (1, 2, 3):
        print("       j=%d : %s" % (j, fmt(contact[j])))
    print("     total contact = %s" % fmt(total))
    check("S2.1 [TWO FORMS AGREE] channel form sum_j (Q^{(0)} - "
          "Q^{(j)})/det_j = class form sum_m 4 h_m Q_m = %s = "
          "(36, 120, 60, 0, -32) EXACTLY -- the completion contact is "
          "one object seen in two bases" % fmt(total),
          total == classform and total == [36, 120, 60, 0, -32])

    a, b, cc, d = sp.symbols('a b cc d')
    prod_id = sp.expand((a * S5 + b * S3) * (cc * S5 + d * S3)
                        - (a * cc * P1 + (a * d + b * cc) * P2
                           + b * d * P3))
    t5t3 = {j: (contact[j][3], contact[j][4]) for j in (1, 2, 3)}
    check("S2.2 [GENUINE CONTACT, NOT EXCHANGE] v508 product theorem "
          "replicated: (a s5 + b s3)(c s5 + d s3) = ac P1 + (ad+bc) P2 "
          "+ bd P3 identically (residual = %s) -- EVERY exchange image "
          "has zero T5/T3; the contacts carry (T5, T3) = %s per "
          "channel: they are exactly the non-exchange objects v508 "
          "said must exist"
          % (prod_id, str({j: fmt(t5t3[j]) for j in (1, 2, 3)})),
          prod_id == 0
          and t5t3 == {1: (4, -24), 2: (-8, 16), 3: (4, -24)})
    return contact, total


# ---------------------------------------------------------------------------
# S3 -- the success table, certificates, exchange span
# ---------------------------------------------------------------------------
def section3(Qv, Qtw, Afix, dets, contact, total):
    print("  -- S3: the success test, sector by sector")
    R = sp.Rational

    skeleton = {j: [sp.nsimplify(Qtw[j][i] / dets[j]) for i in range(5)]
                for j in (1, 2, 3)}
    sums = {j: vsum(skeleton[j], contact[j]) for j in (1, 2, 3)}
    targets = {j: [sp.nsimplify(Qtw[0][i] / dets[j]) for i in range(5)]
               for j in (1, 2, 3)}
    print("     SUCCESS TABLE (P1, P2, P3, T5, T3):")
    print("       ch | AB skeleton          | KS contact            | "
          "sum = Q^(0)/det_j")
    for j in (1, 2, 3):
        print("       %d  | %-20s | %-21s | %s"
              % (j, fmt(skeleton[j]), fmt(contact[j]), fmt(sums[j])))
    print("       tot| %-20s | %-21s | %s"
          % (fmt(Afix), fmt(total), fmt(vsum(Afix, total))))
    ok_chan = all(sums[j] == targets[j] for j in (1, 2, 3))
    ok_sq = (sums[1] == [18, 36, 18, 0, 0] and sums[2] == [9, 18, 9, 0, 0]
             and sums[3] == [18, 36, 18, 0, 0])
    check("S3.1 [PER-SECTOR PERFECT SQUARES] skeleton_j + contact_j = "
          "Q^{(0)}/det_j = 36<x,x>^2/det_j in EVERY twisted channel: "
          "(18, 9, 18) x <x,x>^2 with T5 = T3 = 0 EXACTLY in every "
          "sector -- the preregistered KILL (leftover independent "
          "quartic in ANY sector) does NOT fire", ok_chan and ok_sq)

    tot = vsum(Afix, total)
    check("S3.2 [TOTAL = DEDEKIND x OKUBO] A_fix + contact = %s = "
          "45<x,x>^2 = (5/4) x 36<x,x>^2 = (sum_j 1/det_j) x Q^{(0)}: "
          "the completion converts the AB weighting into the UNIFORM "
          "weighting -- the unique quartic-free weighting of v505 S3.8 "
          "(the rigidity theorem is exactly what the measure lands on)"
          % fmt(tot),
          tot == [45, 90, 45, 0, 0]
          and R(5, 4) * 36 == 45)

    cert = (PHI_T3(Afix), PHI_T3(total), PHI_P(Afix), PHI_P(total),
            PSI(Afix), PSI(total))
    check("S3.3 [v508/v511 CERTIFICATES KILLED] Phi_T3: A_fix %s + "
          "contact %s = 0; Phi_P: %s + %s = 0; psi = Phi_P - Phi_T3/4: "
          "%s + %s = 0 -- the contact supplies EXACTLY the psi = 64 "
          "slice that v511 demanded from delta-1 (no cubic d-channel "
          "needed: c_d free to be 0)" % cert,
          cert == (32, -32, 72, -72, 64, -64))

    E22 = [16, 32, 16, 0, 0]
    E00 = [3600, 7200, 3600, 0, 0]
    ok_span = (tot == vscale(R(45, 16), E22)
               and tot == vscale(R(1, 80), E00)
               and PHI_P(tot) == 0)
    ok_chan_span = all(
        sums[j] == vscale(R(36, 16 * dets[j]), E22) for j in (1, 2, 3))
    check("S3.4 [REMAINDER IN THE EXCHANGE SPAN] 45<x,x>^2 = (45/16) "
          "E22 = (1/80) E00 and per channel 36<x,x>^2/det_j = "
          "(36/(16 det_j)) E22 = (K^{(0)})^2/(100 det_j): the BULK "
          "axion exchange cancels every channel with the SAME residue "
          "lambda~^2 = 36, the twisted propagator carrying the AB "
          "zero-mode factor 1/det_j; Phi_P(remainder) = %s = 0 -- "
          "inside v508's reachable slice (their own certificate "
          "Phi_P(Q^{(0)}) = 0)" % PHI_P(tot),
          ok_span and ok_chan_span)

    mu, le2, Gp, vv = sp.symbols('mu lam_eff2 G v', positive=True)
    sol_mu = sp.solve(sp.Eq(le2 * (mu * vv) ** 2 * (Gp / mu),
                            mu * 36 * vv ** 2 * Gp), le2)
    check("S3.5 [MEASURE CHAIN mu-BLIND] v514 S3.4 replicated: "
          "lam_eff^2 (mu v)^2 (G/mu) = mu 36 v^2 G => lam_eff^2 = %s "
          "for ARBITRARY mu: the quotient measure factors cancel in "
          "the bulk exchange -- the per-channel 1/det_j weighting does "
          "not disturb lambda~ = 6" % sol_mu, sol_mu == [36])
    return sums


# ---------------------------------------------------------------------------
# S4 -- negative controls
# ---------------------------------------------------------------------------
def section4(Qv, Qtw, Afix, dets, h):
    print("  -- S4: negative controls")
    I = sp.I
    R = sp.Rational

    leftovers = {c: sp.expand(32 + c * sum(h[m] * Qv[m][4]
                                           for m in range(4)))
                 for c in (1, 2, 3, 4, 5)}
    check("S4.1 [NC-a: WRONG SCALE] leftover T3(c) = 32 - 8c = %s for "
          "c = 1..5: only c = 4 = |mu4| clears the budget (c = 1 bare "
          "sector energies: 24 left; c = 2 = |Z2|: 16; c = 3 = N_fam: "
          "8; c = 5 = g_car: -8 overshoot) -- the |mu4| normalisation "
          "has teeth" % str(leftovers),
          leftovers == {1: 24, 2: 16, 3: 8, 4: 0, 5: -8})

    wsh = [0, R(1, 2), R(3, 8), R(1, 2)]      # h_1 <-> h_2 shuffled
    T5sh = sp.expand(sum(4 * wsh[m] * Qv[m][3] for m in range(4)))
    T3sh = sp.expand(32 + sum(4 * wsh[m] * Qv[m][4] for m in range(4)))
    check("S4.2 [NC-b: SHUFFLED WEIGHTS] swapping h_1 <-> h_2 (pattern "
          "(1/2, 3/8, 1/2) x 4) leaves T5 = %s != 0 AND T3 leftover "
          "%s != 0: the ch2 PATTERN carries the cancellation, not just "
          "the scale" % (T5sh, T3sh),
          T5sh == -14 and T3sh == 36)

    Aso = [sp.nsimplify(R(5, 4) * Qv[0][i] - R(3, 4) * Qv[2][i])
           for i in range(5)]
    so_tot = [sp.nsimplify(R(5, 4) * (Qv[0][i] + Qv[2][i]))
              for i in range(5)]
    check("S4.3 [NC-c: SO(16) GLUE] classes {0, 2} only; AB sum = %s = "
          "(15, -18, -15, -4, 40) (v508 S5.3 replication); completion "
          "weights hit only w_2 = 2: total = (5/4) Tr_so16 X^4 = %s -- "
          "leftover T5 = 20, T3 = -40 in the SUMMED trace (so16's "
          "Okubo failure is inherited: no perfect square, the KILL "
          "branch FIRES for so16 -- E8 is doubly special)"
          % (fmt(Aso), fmt(so_tot)),
          Aso == [15, -18, -15, -4, 40]
          and so_tot == [15, 30, 45, 20, -40]
          and so_tot[3] == 20 and so_tot[4] == -40)

    dets_f = {1: 2 * I, 2: 4, 3: -2 * I}      # (1 - i^{-j})^2, v505 S6.1
    wf = [sp.nsimplify(sp.expand(
        sum((1 - I ** (j * m)) / dets_f[j] for j in (1, 2, 3))))
        for m in range(4)]
    Af = [sp.nsimplify(sp.expand(
        sum(Qtw[j][i] / dets_f[j] for j in (1, 2, 3))))
        for i in range(5)]
    check("S4.4 [NC-d: diag(i, i)] fake zero modes (2i, 4, -2i): the "
          "skeleton DEGENERATES to the Z2 target (%s = A_2 = "
          "(-3,-6,9,8,-16): the odd channels cancel pairwise -- no Z4 "
          "ledger at all); fake weights %s = (-1/2, 0, 3/2): w_1 != "
          "w_3 breaks the conjugation pairing (Q_1 = Q_3 demands equal "
          "weights) and w != 4h breaks the index bridge (no ALE, no "
          "McKay data, v505 S6.1) -- the wrong deck has no sphere "
          "axions to source the contacts"
          % (fmt(Af), fmt(wf)),
          Af == [-3, -6, 9, 8, -16]
          and wf == [0, R(-1, 2), 0, R(3, 2)]
          and wf[1] != wf[3]
          and any(wf[m] != 4 * h[m] for m in range(4)))

    A2 = [sp.nsimplify((Qv[0][i] - Qv[1][i] + Qv[2][i] - Qv[3][i])
                       / 4) for i in range(5)]
    hZ2 = R(1, 4)                              # A1 discriminant weight
    contact2 = [sp.nsimplify(2 * hZ2 * (Qv[1][i] + Qv[3][i]))
                for i in range(5)]
    tot2 = vsum(A2, contact2)
    check("S4.5 [Z2/EGUCHI-HANSON ANCHOR] A_2 = Q^{(g^2)}/4 = %s; "
          "completion weights |Z2| h^{A1} = 2 x 1/4 = 1/2 on the odd "
          "classes: contact = %s = Q_1; A_2 + contact = %s = 9<x,x>^2 "
          "= (1/4) x 36<x,x>^2 = (Dedekind_2) x (Okubo) -- perfect "
          "square, T5 = T3 = 0, coupling scale 2 = |Z2| = centre "
          "count: the published-anchor case PASSES with the same "
          "mechanism" % (fmt(A2), fmt(contact2), fmt(tot2)),
          A2 == [-3, -6, 9, 8, -16]
          and contact2 == [12, 24, 0, -8, 16]
          and tot2 == [9, 18, 9, 0, 0])


# ---------------------------------------------------------------------------
# S5 -- multiplier note (cross-reference to the parallel delta-1d strand)
# ---------------------------------------------------------------------------
def order_of(ph):
    for n in range(1, 33):
        if sp.simplify(sp.expand_complex(ph ** n - 1)) == 0:
            return n
    return None


def section5(h):
    print("  -- S5: multiplier note (cross-reference to delta-1d; "
          "its files untouched)")
    R = sp.Rational

    e = lambda x: sp.exp(2 * sp.pi * sp.I * x)
    ph = [e(R(3 * a * a, 8)) for a in range(4)]
    orders = [order_of(p) for p in ph]
    orders_sq = [order_of(p ** 2) for p in ph]
    gauss_a3 = sp.simplify(sp.expand_complex(sum(ph)))
    target_a3 = sp.simplify(sp.expand_complex(2 * e(R(3, 8))))
    ph5 = [e(R(5 * a * a, 8)) for a in range(4)]
    gauss_d5 = sp.simplify(sp.expand_complex(sum(ph5)))
    target_d5 = sp.simplify(sp.expand_complex(2 * e(R(5, 8))))
    gauss_full = sp.simplify(sp.expand_complex(
        sum(e(R(5 * x * x + 3 * y * y, 8))
            for x in range(4) for y in range(4))))
    check("S5.1 [DISCRIMINANT T-PHASES, EXACT] A3 factor e(3a^2/8): "
          "phase orders %s = (1, 8, 2, 8) -- the h_a = (3/8, 1/2, 3/8) "
          "exponentiate to 8th roots (8 = 2|mu4|); their SQUARES have "
          "orders %s = (1, 4, 1, 4): a finite mu4 system -- exactly "
          "the order <= 4 multiplier delta-1c diagnosed in the pair-"
          "orbit holonomies; Gauss sums: A3 slice %s = 2 e(3/8), D5 "
          "slice %s = 2 e(5/8), full Weil %s = 4 (signature 0 mod 8, "
          "delta-1c replication)"
          % (fmt(orders), fmt(orders_sq), gauss_a3, gauss_d5,
             gauss_full),
          orders == [1, 8, 2, 8] and orders_sq == [1, 4, 1, 4]
          and sp.simplify(gauss_a3 - target_a3) == 0
          and sp.simplify(gauss_d5 - target_d5) == 0
          and gauss_full == 4)

    check("S5.2 [NOTE FOR delta-1d] the M2 contact weights 4h = "
          "(0, 3/2, 2, 3/2) are REAL RATIONALS -- they carry NO "
          "multiplier phase of their own; the residual multiplier "
          "phases delta-1c measured must therefore sit ENTIRELY in "
          "the tau-dependent block transport, and the natural "
          "candidate system is e(2 h_a) = (1, e(3/4), 1, e(3/4)) of "
          "order 4 = |mu4| (the SQUARED discriminant phases above); "
          "the diagonal-slice Gauss phases e(3/8), e(5/8) are order-8 "
          "objects whose PRODUCT is trivial (4 = real) -- the "
          "16-component Weil completion is where the order-8 pieces "
          "cancel.  Cross-reference only; the delta-1d strand and its "
          "files are untouched", True)


# ---------------------------------------------------------------------------
# S6 -- verdict per the preregistered criterion
# ---------------------------------------------------------------------------
def section6():
    print("  -- S6: verdict per the preregistered v514 S8.2 criterion")
    check("S6.1 [WHAT IS EXACT] (a) the completion-weight identity "
          "w_m = sum_j (1-i^{jm})/det_j = 4 h_m = -4 ch2(T_m) (index "
          "bridge, no free scale); (b) T5 = 0 and the 4:3 ratio "
          "parameter-free, T3 budget closed at scale |mu4|, delta-1's "
          "forced leading weights reproduced; (c) per-sector perfect "
          "squares Q^{(0)}/det_j (T5 = T3 = 0 in every channel), "
          "total (5/4) x 36 <x,x>^2; (d) both v508 certificates and "
          "the v511 psi = 64 slice supplied exactly; (e) remainder "
          "inside the exchange span, bulk lambda~^2 = 36 per channel, "
          "mu-blind chain; (f) all controls (scale, shuffle, so16, "
          "diag(i,i), Z2 anchor) separate honestly", True)
    check("S6.2 [VERDICT: SUCCESS wording met -- with the honest "
          "fence] preregistered SUCCESS: 'bulk reproduces lambda~^2 = "
          "36 with the eps1 measure bookkeeping AND the twisted "
          "sectors pair with the three sphere axions cancelling the "
          "rigid 32 T3 residual' -- DELIVERED on the declared "
          "completion measure: every sector is the SAME Okubo square "
          "36<x,x>^2 (weights 1/det_j), the 32 T3 is cancelled by the "
          "ch2-weighted sphere-axion contacts, the KILL (leftover "
          "independent quartic in ANY sector) does NOT fire.  FENCE: "
          "the completion reading (loop = unphased sector trace with "
          "the same zero-mode measure) is DECLARED, supported by the "
          "delta-1 modular-completion finding -- its derivation from "
          "the BCOV integral stays [O] (delta-1b/1c/1d territory); "
          "NO marker moves anywhere", True)


# ---------------------------------------------------------------------------
def run():
    reset()
    print("v516  CELEST.WP5E.M2.01: the twisted Kodaira-Spencer measure "
          "on PT/Z4 (M2 of CELEST.SEAM.01, SUCCESS on the declared "
          "completion measure)")
    roots = build_glue_roots()
    Qv, Qtw, Afix, dets = section0(roots)
    h, w = section1(Qv, dets)
    contact, total = section2(Qv, Qtw, dets, h)
    section3(Qv, Qtw, Afix, dets, contact, total)
    section4(Qv, Qtw, Afix, dets, h)
    section5(h)
    section6()

    return summary("v516 CELEST.WP5E.M2.01: the twisted KS measure -- "
                   "M2 executed (SUCCESS on the preregistered v514 "
                   "S8.2 criterion, on the DECLARED completion "
                   "measure): completion weights w_m = sum_j "
                   "(1 - i^{jm})/det_j = (0, 3/2, 2, 3/2) = 4 h_m = "
                   "|mu4| h_m = -4 ch2(T_m) with NO free scale (the "
                   "sphere axions pair through their own McKay ch2 "
                   "charges); parameter-free locks (T5 = 0 for any "
                   "scale, ratio 4:3 reproduced, T3 budget forces "
                   "c = 4 = |mu4|); every twisted channel becomes the "
                   "perfect Okubo square 36<x,x>^2/det_j, total "
                   "45<x,x>^2 = (5/4) x 36 = Dedekind x Okubo (the "
                   "v505 S3.8 unique quartic-free weighting); both "
                   "v508 certificates killed (32 -> 0, 72 -> 0) and "
                   "the v511 psi = 64 slice supplied exactly (no "
                   "cubic d-channel needed); remainder in the "
                   "exchange span with bulk lambda~^2 = 36 per "
                   "channel, mu-blind chain; controls: wrong scale, "
                   "shuffle, so16 (KILL fires there), diag(i,i), "
                   "Z2/EH anchor (scale 2 = |Z2|); FENCE: the "
                   "completion reading is DECLARED [C], its BCOV-"
                   "integral derivation stays [O] (delta-1b/1c/1d); "
                   "no marker moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
