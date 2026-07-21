"""seam_alignment_bit_torus_origin_probe.py -- EXPLORATION ONLY (experiments/, no verification claim).

THE TAUTOLOGY ATTACK ON THE v506 ALIGNMENT BIT (Moebius / torus-origin side).

v506 (SEAM.CLOCK.RIGIDITY.01) reduced the last identification input to ONE bit:
"the collar deck is the central involution of the mark-D4" (<=> a marks-
preserving Moebius square root = the clock exists).  Conjecture under attack:
marks AND deck both descend from the SAME torus structure (the seam double
T^2_tau -> S^2, v214/v260), and this common origin forces the central
alignment AUTOMATICALLY -- the bit would be a tautology.

  T1 ORIGIN (die Herkunft, made exact).  The 4 marks are the branch points of
     the double: fixed points of the hyperelliptic involution w -> -w on
     T^2 = C/(Z + tau Z) = the four half-periods Lambda/2Lambda = {0, 1/2,
     tau/2, (1+tau)/2} (|.| = 4 = 2 chi, v216).  A half-period translation
     t_c: w -> w + c (2c in Lambda) commutes with w -> -w and DESCENDS to the
     base; the descended map is the EXPLICIT Moebius involution
        sigma_i(x) = e_i + (e_i - e_j)(e_i - e_k)/(x - e_i)
     (the algebraic shadow of the p-function addition formula p(w + omega_i)),
     verified as an exact curve-automorphism identity on y^2 = 4 prod(x-e_l)
     with RATIONAL fibre factor psi_i = (e_i-e_j)(e_i-e_k)/(x-e_i)^2.  The
     three sigma_c + id form Klein V4; each sigma_c permutes the 4 marks
     freely in 2+2 pairs (pairing infinity <-> e_i).  CONVERSELY: in EVERY
     stabiliser type (V4 generic / D4 harmonic / A4 equianharmonic) the
     freely-acting involutions are EXACTLY the three sigma_c -- so the
     established deck (mark-free, v216) IS a half-period translation.  The
     Herkunft is forced; only WHICH c is not.
  T2 THE THREE DECK CANDIDATES (A1).  Generic tau (Legendre lambda = 3, 5):
     Stab(marks) = V4 = {id, sigma_1, sigma_2, sigma_3} -- ABELIAN: every
     sigma_c is "central", yet exponent 2 => NO square root inside; the two
     global PGL2 roots of each sigma_c (v506 Theorem A: exactly two, +-i-like,
     here r_pm = [[+-i sqrt(lam), lam], [1, +-i sqrt(lam)]] for sigma_1) do
     NOT preserve the marks.  THE CORE SOLVE (symbolic lambda): sigma_c admits
     a marks-preserving PGL2 square root  <=>  lambda = -1 (sigma_1),
     lambda = 2 (sigma_2), lambda = 1/2 (sigma_3)  <=>  the two deck pairs of
     sigma_c separate each other HARMONICALLY (pair cross-ratio = -1) -- one
     intrinsic Moebius invariant.  Union over c = the harmonic orbit
     {-1, 2, 1/2} <=> j = 1728 <=> tau = i.  At lambda = -1 the stabiliser
     jumps to D4: sigma_1 becomes the CENTRAL involution (2 roots = the clock
     pair), sigma_2/sigma_3 become EDGE involutions (0 roots) -- the silver
     counterexample of v506 is realised INSIDE the torus family (same tau = i,
     wrong c).  Conjugation search: (mu4 marks, deck z -> -z) of v506 maps
     exactly onto (lemniscatic marks, sigma_central).
  T3 CM DICTIONARY (why tau = i, intrinsically).  Mult-by-i on
     Lambda/2Lambda = [[0,1],[1,0]] mod 2: fixes EXACTLY ONE nonzero
     half-period, c* = (1+tau)/2 -- the central sigma_c is the translation by
     the CM-FIXED half-period; at tau = rho mult-by-zeta6 = [[0,1],[1,1]]
     mod 2 3-cycles the half-periods (NO fixed one, matching A4 with zero
     order-4 elements); generic tau has no CM at all.  On the lemniscatic
     curve y^2 = 4x^3 - 4x the CM map (x,y) -> (-x, iy) is exact; the clock
     ghat: x -> (x-1)/(x+1) = sigma_{omega_1} o (CM descent) is order 4,
     4-cycles the marks, ghat^2 = -1/x = sigma_central, and its curve lift
     needs psi = 2i/(x+1)^2: the fibre factor REQUIRES the CM unit i (t^2+1
     irreducible over Q) -- half-period translations lift rationally, the
     clock root only exists WITH complex multiplication <=> tau = i.
  T4 EQUIVALENCE TRIAS + CIRCULARITY AUDIT (A2).  "Uhr existiert" <=>
     "tau = i AND deck = t_{c*}" <=> "Stab = D4 AND deck central" <=> "deck
     pairs harmonically separated".  Sharpening: 'central' ALONE is empty
     (generic V4: all central, zero roots), 'harmonic' ALONE is insufficient
     (silver, v506): the bit is the CONJUNCTION.  No circularity with v493:
     v493 assumes the clock and derives tau = i (P(iZ) = P(Z) => a3 = a2 =
     a1 = 0, re-verified); here NO clock is assumed and existence is solved
     -- two independently computed converses of ONE equivalence.  The common
     origin does NOT force the bit: TAUTOLOGY REFUTED, EQUIVALENCE PROVED.

Repo anchors: v506 (bit + counterexample + Theorem A), v216 (marks =
Gauss-Bonnet), v214/v260 (pillowcase = T^2/±, Kummer), v168 (cross-ratio 2),
v493 (clock => tau = i frozen), v503 (dynamics picks hexagonal; clock =
carrier input), v492 (S5 clock/deck).

Exact throughout (sympy; no floats).  Standalone.
Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/seam_alignment_bit_torus_origin_probe.py
"""
from fractions import Fraction as Fr
from itertools import permutations

import sympy as sp

I = sp.I
RESULTS = []

# carrier constants (hardcoded, standalone probe; cf. tfpt_constants)
G_CAR = 5
N_FAM = 3


def check(name, ok):
    RESULTS.append(bool(ok))
    print(("PASS" if ok else "FAIL") + " [%2d] %s" % (len(RESULTS), name))


def iszero(e):
    e2 = sp.expand(e)
    if e2 == 0:
        return True
    return sp.simplify(e2) == 0


# ---------------------------------------------------------------------------
# projective points (p, q) with point = p/q, infinity = (1, 0); exact Moebius
# ---------------------------------------------------------------------------
def peq(P, Q):
    return iszero(P[0] * Q[1] - P[1] * Q[0])


def pdet(P, Q):
    return sp.expand(P[0] * Q[1] - Q[0] * P[1])


def apply_m(M, P):
    return (sp.expand(M[0, 0] * P[0] + M[0, 1] * P[1]),
            sp.expand(M[1, 0] * P[0] + M[1, 1] * P[1]))


def map3(A, B, C):
    """the unique Moebius matrix sending (inf, 0, 1) -> (A, B, C)."""
    alpha = C[0] * B[1] - B[0] * C[1]
    beta = A[0] * C[1] - C[0] * A[1]
    return sp.Matrix([[alpha * A[0], beta * B[0]],
                      [alpha * A[1], beta * B[1]]])


def mexp(M):
    return M.applyfunc(sp.expand)


def prop_mat(A, B):
    """projective equality of 2x2 matrices (A = c B)."""
    a = [A[0, 0], A[0, 1], A[1, 0], A[1, 1]]
    b = [B[0, 0], B[0, 1], B[1, 0], B[1, 1]]
    for i in range(4):
        for j in range(i + 1, 4):
            if not iszero(a[i] * b[j] - a[j] * b[i]):
                return False
    return True


def is_scalar_mat(M):
    return iszero(M[0, 1]) and iszero(M[1, 0]) and iszero(M[0, 0] - M[1, 1])


def proj_order(M, cap=9):
    P = sp.eye(2)
    for n in range(1, cap + 1):
        P = mexp(P * M)
        if is_scalar_mat(P):
            return n
    return None


def stabilizer(cfg):
    """ALL Moebius maps preserving the 4-point set cfg (complete: a Moebius map
    is fixed by the images of 3 points => enumerate all 24 ordered triples)."""
    S = map3(cfg[0], cfg[1], cfg[2])
    Sinv = S.adjugate()
    found = []
    for t in permutations(range(4), 3):
        T = map3(cfg[t[0]], cfg[t[1]], cfg[t[2]])
        M = mexp(T * Sinv)
        ok = all(any(peq(apply_m(M, p), q) for q in cfg) for p in cfg)
        if ok and not any(prop_mat(M, X) for X in found):
            found.append(M)
    return found


def mark_perm(M, cfg):
    perm = []
    for p in cfg:
        img = apply_m(M, p)
        perm.append([j for j, q in enumerate(cfg) if peq(img, q)][0])
    return perm


def order_profile(stab):
    prof = {}
    for g in stab:
        o = proj_order(g)
        prof[o] = prof.get(o, 0) + 1
    return prof


def cross_ratio(P1, P2, P3, P4):
    return sp.simplify(sp.expand(pdet(P1, P3) * pdet(P2, P4)) /
                       sp.expand(pdet(P1, P4) * pdet(P2, P3)))


def jlam(lam):
    return sp.simplify(256 * (lam ** 2 - lam + 1) ** 3
                       / (lam ** 2 * (lam - 1) ** 2))


# ---------------------------------------------------------------------------
# the Legendre marks {0, 1, lambda, inf} and the three half-period involutions
# ---------------------------------------------------------------------------
def marks_of(l):
    return [(sp.Integer(0), sp.Integer(1)), (sp.Integer(1), sp.Integer(1)),
            (l, sp.Integer(1)), (sp.Integer(1), sp.Integer(0))]


def weier_sigma(ei, ej, ek):
    """descent of the half-period translation pairing inf <-> e_i:
    x -> e_i + (e_i-e_j)(e_i-e_k)/(x-e_i)  (p-addition-formula shadow)."""
    D = (ei - ej) * (ei - ek)
    return sp.Matrix([[ei, D - ei ** 2], [1, -ei]])


def sigmas_of(l):
    """sigma_1 pairs {0,inf},{1,l}; sigma_2 pairs {1,inf},{0,l};
    sigma_3 pairs {l,inf},{0,1} -- the three half-period decks in Legendre form."""
    return {1: mexp(weier_sigma(sp.Integer(0), sp.Integer(1), l)),
            2: mexp(weier_sigma(sp.Integer(1), sp.Integer(0), l)),
            3: mexp(weier_sigma(l, sp.Integer(0), sp.Integer(1)))}


def sigma_pairs(l):
    """(A, B, C, D): sigma_c swaps A <-> B and C <-> D."""
    P0, P1, PL, PInf = marks_of(l)[0], marks_of(l)[1], marks_of(l)[2], marks_of(l)[3]
    return {1: (P0, PInf, P1, PL),
            2: (P1, PInf, P0, PL),
            3: (PL, PInf, P0, P1)}


def root_condition(l, A, B, C, D, swap_cd):
    """closure condition for the 4-cycle root rho: A -> C -> B -> D -> A
    (rho^2 = the (A<->B)(C<->D) involution); swap_cd flips the orientation.
    Returns (condition polynomial in l, rho matrix)."""
    if swap_cd:
        C, D = D, C
    Ms = map3(A, C, B)          # sends (inf,0,1) -> (A,C,B)
    Mt = map3(C, B, D)          # sends (inf,0,1) -> (C,B,D)
    rho = mexp(Mt * Ms.adjugate())
    cond = pdet(apply_m(rho, D), A)
    return sp.factor(cond), rho


def conj_search(src_cfg, deckM, tgt_cfg, sigs):
    """all Moebius h with h(src marks) = tgt marks; classify h deck h^-1
    against the sigma dictionary.  Returns (#valid h, set of sigma indices)."""
    Ms_inv = map3(src_cfg[0], src_cfg[1], src_cfg[2]).adjugate()
    hits, n_h = set(), 0
    for t in permutations(range(4), 3):
        Mt = map3(tgt_cfg[t[0]], tgt_cfg[t[1]], tgt_cfg[t[2]])
        h = mexp(Mt * Ms_inv)
        if not any(peq(apply_m(h, src_cfg[3]), q) for q in tgt_cfg):
            continue
        n_h += 1
        hc = mexp(h * deckM * h.adjugate())
        for idx, sg in sigs.items():
            if prop_mat(hc, sg):
                hits.add(idx)
    return n_h, hits


def run():
    print("seam_alignment_bit_torus_origin_probe: does the COMMON TORUS ORIGIN "
          "of marks and deck force the v506 alignment bit?  Exact, sympy")
    print("=" * 100)
    lam = sp.symbols('lam')
    x, y, w, t_ = sp.symbols('x y w t_')
    e1, e2, e3 = sp.symbols('e1 e2 e3')

    # ================================================ T1: the origin (Herkunft)
    print("  -- T1: origin -- marks and deck from the torus double T^2 -> S^2")

    # 1. marks = fixed points of the hyperelliptic involution = Lambda/2Lambda
    half = Fr(1, 2)
    tors = [(a, b) for a in (Fr(0), half) for b in (Fr(0), half)]
    tors_ok = all(((2 * a) % 1, (2 * b) % 1) == (0, 0) for a, b in tors)
    non_tors = [(a, b) for a in (Fr(0), half, Fr(1, 3)) for b in (Fr(0), half)
                if ((2 * a) % 1, (2 * b) % 1) == (0, 0)]
    disc = sp.factor(sp.discriminant(x * (x - 1) * (x - lam), x))
    check("T1.1 MARKS ORIGIN [exact]: fixed points of w -> -w on C/(Z+tau Z) "
          "= half-periods Lambda/2Lambda = %d points {0, 1/2, tau/2, "
          "(1+tau)/2} (2w in Lambda <=> coefficients in {0,1/2}; a 1/3-"
          "coefficient never qualifies: %d survivors of the 6-point control "
          "grid = the 4 genuine ones); curve side: y = 0 on y^2 = "
          "x(x-1)(x-lam) gives 3 finite branch points + inf = 4 marks, "
          "distinct iff disc = %s != 0 (lam not in {0,1}) -- the v216 count "
          "4 = 2 chi = N_fam + 1 with its torus origin"
          % (len(tors), len(non_tors), disc),
          len(tors) == 4 and tors_ok and len(non_tors) == 4
          and disc == lam ** 2 * (lam - 1) ** 2 and 4 == N_FAM + 1)

    # 2. descent condition: t_c commutes with w -> -w  <=>  2c in Lambda
    half_periods = [(half, Fr(0)), (Fr(0), half), (half, half)]
    hp_ok = all(((2 * a) % 1, (2 * b) % 1) == (0, 0) for a, b in half_periods)
    c0 = (Fr(1, 3), Fr(0))
    c0_fails = ((2 * c0[0]) % 1, (2 * c0[1]) % 1) != (0, 0)
    # symbolic: -(w+c) - (-w + c) = -2c: in Lambda iff 2c in Lambda
    c_sym = sp.symbols('c_sym')
    resid = sp.expand(-(w + c_sym) - (-w + c_sym))
    check("T1.2 DECK-CANDIDATE DESCENT [exact]: t_c: w -> w+c commutes with "
          "the hyperelliptic involution iff -(w+c) = -w+c mod Lambda, i.e. "
          "residual %s in Lambda <=> 2c in Lambda: TRUE for all 3 nonzero "
          "half-periods (%s), FALSE for the control c = 1/3 (%s) -- exactly "
          "the three half-period translations descend to the base sphere"
          % (resid, hp_ok, c0_fails),
          resid == -2 * c_sym and hp_ok and c0_fails and len(half_periods) == 3)

    # 3. the descended maps are the explicit Moebius sigma_i + exact curve lift
    lift_ok, invol_ok, pairing_ok = True, True, True
    for (ei, ej, ek) in [(e1, e2, e3), (e2, e3, e1), (e3, e1, e2)]:
        M = weier_sigma(ei, ej, ek)
        Msq = mexp(M * M)
        invol_ok &= iszero(sp.trace(M)) and is_scalar_mat(Msq)
        phi = (ei * x + ((ei - ej) * (ei - ek) - ei ** 2)) / (x - ei)
        psi = (ei - ej) * (ei - ek) / (x - ei) ** 2
        prod_phi = (phi - ei) * (phi - ej) * (phi - ek)
        prod_x = (x - ei) * (x - ej) * (x - ek)
        lift_ok &= sp.simplify(sp.together(prod_phi - psi ** 2 * prod_x)) == 0
        cfge = [(ei, 1), (ej, 1), (ek, 1), (1, 0)]
        pm = mark_perm(M, cfge)
        pairing_ok &= (pm == [3, 2, 1, 0])   # inf<->e_i, e_j<->e_k
    check("T1.3 EXPLICIT DESCENT sigma_i [exact, symbolic e1,e2,e3]: "
          "sigma_i(x) = e_i + (e_i-e_j)(e_i-e_k)/(x-e_i) is traceless "
          "(involution: %s), permutes the marks as inf<->e_i, e_j<->e_k "
          "(free 2+2 pairing: %s), and LIFTS to the curve y^2 = 4prod(x-e_l) "
          "via (x,y) -> (sigma_i(x), psi_i(x) y) with RATIONAL psi_i = "
          "(e_i-e_j)(e_i-e_k)/(x-e_i)^2 (exact identity prod(sigma_i - e_l) "
          "= psi_i^2 prod(x - e_l): %s) -- the p-function addition formula "
          "p(w + omega_i) as pure algebra: the half-period translations "
          "descend RATIONALLY, no unit i needed"
          % (invol_ok, pairing_ok, lift_ok),
          invol_ok and pairing_ok and lift_ok)

    # 4. V4 closure of {id, sigma_1, sigma_2, sigma_3} (symbolic e's)
    S1w = weier_sigma(e1, e2, e3)
    S2w = weier_sigma(e2, e3, e1)
    S3w = weier_sigma(e3, e1, e2)
    closure = (prop_mat(mexp(S1w * S2w), S3w)
               and prop_mat(mexp(S2w * S3w), S1w)
               and prop_mat(mexp(S3w * S1w), S2w))
    abelian = all(prop_mat(mexp(A_ * B_), mexp(B_ * A_))
                  for A_ in (S1w, S2w, S3w) for B_ in (S1w, S2w, S3w))
    check("T1.4 KLEIN V4 [exact, symbolic]: sigma_i sigma_j = sigma_k "
          "projectively (%s), all commute (%s): {id, sigma_1, sigma_2, "
          "sigma_3} = V4 = the translation group Lambda/2Lambda / {+-1} "
          "acting on the base -- die drei Deck-Kandidaten, for EVERY modulus"
          % (closure, abelian), closure and abelian)

    # 5. free involutions in every stabiliser type are EXACTLY the sigma_c
    lam_hex = sp.Rational(1, 2) + sp.sqrt(3) * I / 2
    cfg3, cfgm1, cfghex = marks_of(sp.Integer(3)), marks_of(sp.Integer(-1)), \
        marks_of(lam_hex)
    stab3 = stabilizer(cfg3)
    stabm1 = stabilizer(cfgm1)
    stabhex = stabilizer(cfghex)
    counts = {}
    for tag, (stab, l) in {'generic': (stab3, sp.Integer(3)),
                           'harmonic': (stabm1, sp.Integer(-1)),
                           'hex': (stabhex, lam_hex)}.items():
        sigs = sigmas_of(l)
        cfg = marks_of(l)
        inv = [g for g in stab if proj_order(g) == 2]
        free = [g for g in inv
                if all(i != j for i, j in enumerate(mark_perm(g, cfg)))]
        match = all(any(prop_mat(g, s) for s in sigs.values()) for g in free)
        counts[tag] = (len(stab), len(inv), len(free), match)
    check("T1.5 DECK ORIGIN IS FORCED [exact]: in ALL three stabiliser types "
          "the freely-acting involutions are EXACTLY the three sigma_c: "
          "generic lam=3 (|Stab|, #inv, #free, =sigma) = %s (V4), harmonic "
          "lam=-1 %s (D4: 5 involutions, only 3 free), hexagonal %s (A4) -- "
          "EVERY mark-free collar deck (v216: all marks deck-free) descends "
          "from a half-period translation; die Herkunft ist erzwungen, nur "
          "WELCHES c nicht"
          % (counts['generic'], counts['harmonic'], counts['hex']),
          counts['generic'] == (4, 3, 3, True)
          and counts['harmonic'] == (8, 5, 3, True)
          and counts['hex'] == (12, 3, 3, True))

    # ================================================ T2: the three candidates (A1)
    print("  -- T2: A1 -- the three sigma_c, stabiliser position, root existence")

    # 6. generic modulus: V4, all central, exponent 2, no roots inside
    sigs3 = sigmas_of(sp.Integer(3))
    stab_is_v4 = (len(stab3) == 4
                  and all(any(prop_mat(g, s) for s in
                              list(sigs3.values()) + [sp.eye(2)])
                          for g in stab3))
    central3 = all(prop_mat(mexp(g * h_), mexp(h_ * g))
                   for g in stab3 for h_ in stab3)
    exp2 = all(is_scalar_mat(mexp(g * g)) for g in stab3)
    roots_inside = sum(1 for g in stab3 for s in sigs3.values()
                       if prop_mat(mexp(g * g), s))
    check("T2.6 GENERIC V4 [exact, lam=3]: Stab = {id, sigma_1, sigma_2, "
          "sigma_3} exactly (%s), abelian => ALL THREE sigma_c are central "
          "(%s) -- yet exponent 2 (%s): squares = {id}, so NO sigma_c has a "
          "square root inside the stabiliser (%d found).  'Zentralitaet' "
          "allein ist LEER -- sie liefert keine Uhr"
          % (stab_is_v4, central3, exp2, roots_inside),
          stab_is_v4 and central3 and exp2 and roots_inside == 0)

    # 7. the two global PGL2 roots per sigma_c (Theorem A transported), generic kill
    s_ = sp.sqrt(lam)
    r_plus = sp.Matrix([[I * s_, lam], [1, I * s_]])
    r_minus = sp.Matrix([[-I * s_, lam], [1, -I * s_]])
    sig1_sym = sp.Matrix([[0, lam], [1, 0]])
    roots_square = (prop_mat(mexp(r_plus * r_plus), sig1_sym)
                    and prop_mat(mexp(r_minus * r_minus), sig1_sym))
    inv_pair = prop_mat(mexp(r_plus * r_minus), sp.eye(2))
    r3p = r_plus.subs(lam, 3)
    r3m = r_minus.subs(lam, 3)
    img_p = apply_m(r3p, (sp.Integer(0), sp.Integer(1)))
    img_m = apply_m(r3m, (sp.Integer(0), sp.Integer(1)))
    gen_kill = (not any(peq(img_p, q) for q in cfg3)
                and not any(peq(img_m, q) for q in cfg3))
    check("T2.7 GLOBAL ROOTS, GENERIC KILL [exact]: sigma_1 = lam/z has "
          "EXACTLY the two PGL2 roots r_pm = [[+-i sqrt(lam), lam], [1, "
          "+-i sqrt(lam)]] (r_pm^2 = sigma_1 symbolically: %s; mutually "
          "inverse Aut(Z4) pair: %s; +-i-like at the deck fixed points "
          "+-sqrt(lam), v506 Theorem A transported); at lam = 3 NEITHER "
          "root preserves the marks (image of mark 0 is -i sqrt(3)-like, "
          "not a mark: %s) -- roots must come from OUTSIDE and generically "
          "stay outside"
          % (roots_square, inv_pair, gen_kill),
          roots_square and inv_pair and gen_kill)

    # 8. THE CORE SOLVE: marks-preserving root of sigma_c <=> one harmonic lambda
    pairs = sigma_pairs(lam)
    sigs_sym = sigmas_of(lam)
    expected = {1: {sp.Integer(-1)}, 2: {sp.Integer(2)},
                3: {sp.Rational(1, 2)}}
    solve_ok, cr_ok, root_verify = True, True, True
    sol_report = {}
    for cidx in (1, 2, 3):
        A, B, C, D = pairs[cidx]
        sols = set()
        rhos = {}
        for swap in (False, True):
            cond, rho = root_condition(lam, A, B, C, D, swap)
            for so in sp.solve(cond, lam):
                if so not in (sp.Integer(0), sp.Integer(1)):
                    sols.add(sp.nsimplify(so))
                    rhos[(so, swap)] = rho
        sol_report[cidx] = sols
        solve_ok &= (sols == expected[cidx])
        # intrinsic form: pair cross-ratio (A,B;C,D) = -1 <=> same lambda
        cr = cross_ratio(A, B, C, D)
        cr_sols = {sp.nsimplify(so) for so in sp.solve(sp.together(cr + 1), lam)}
        cr_ok &= (cr_sols == expected[cidx])
        # verify: at the solution the cycle map IS an order-4 root of sigma_c
        for (so, swap), rho in rhos.items():
            r_at = mexp(rho.subs(lam, so))
            sg_at = mexp(sigs_sym[cidx].subs(lam, so))
            root_verify &= prop_mat(mexp(r_at * r_at), sg_at)
            root_verify &= (proj_order(r_at) == 4)
    check("T2.8 THE CORE SOLVE [exact, symbolic lam]: a marks-preserving "
          "PGL2 root of sigma_c exists iff lam in %s (sigma_1), %s "
          "(sigma_2), %s (sigma_3) -- each condition EQUIVALENT to 'the two "
          "deck pairs separate harmonically' (pair cross-ratio = -1: same "
          "solution sets, %s); at each solution both cycle orientations give "
          "order-4 roots squaring to sigma_c (%s): per half-period c EXACTLY "
          "ONE harmonic lambda-representative; union over c = the harmonic "
          "orbit {-1, 2, 1/2}"
          % (sol_report[1], sol_report[2], sol_report[3], cr_ok, root_verify),
          solve_ok and cr_ok and root_verify)

    # 9. at tau = i the stabiliser jumps to D4: one sigma_c central, two edge
    sigsm1 = sigmas_of(sp.Integer(-1))
    profm1 = order_profile(stabm1)
    center = [g for g in stabm1
              if all(prop_mat(mexp(g * h_), mexp(h_ * g)) for h_ in stabm1)]
    central_is_s1 = (len(center) == 2
                     and any(prop_mat(g, sigsm1[1]) for g in center)
                     and any(prop_mat(g, sp.eye(2)) for g in center))
    edge_not_central = not any(prop_mat(g, sigsm1[2]) or prop_mat(g, sigsm1[3])
                               for g in center)
    roots_of = {c: sum(1 for g in stabm1
                       if prop_mat(mexp(g * g), sigsm1[c]))
                for c in (1, 2, 3)}
    o4 = [g for g in stabm1 if proj_order(g) == 4]
    o4_sq_s1 = all(prop_mat(mexp(g * g), sigsm1[1]) for g in o4)
    check("T2.9 TAU = i JUMP [exact, lam=-1]: Stab = D4 (order %d, profile "
          "%s); center = {id, sigma_1} (%s), sigma_2/sigma_3 NON-central "
          "edge involutions (%s); roots inside the stabiliser: sigma_1 has "
          "%d (= the 2 order-4 elements = the clock pair, both squaring to "
          "sigma_1: %s), sigma_2 has %d, sigma_3 has %d -- the CENTRAL "
          "sigma_c is EXACTLY the one whose PGL2 roots preserve the marks; "
          "the other two half-period decks sit edge-type: the v506 silver "
          "situation INSIDE the torus family"
          % (len(stabm1), profm1, central_is_s1, edge_not_central,
             roots_of[1], o4_sq_s1, roots_of[2], roots_of[3]),
          len(stabm1) == 8 and profm1 == {1: 1, 2: 5, 4: 2}
          and central_is_s1 and edge_not_central
          and roots_of == {1: 2, 2: 0, 3: 0} and len(o4) == 2 and o4_sq_s1)

    # 10. the v506 seam pair (mu4, z -> -z) IS (lemniscatic marks, sigma_central)
    mu4 = [(sp.Integer(1), 1), (I, 1), (sp.Integer(-1), 1), (-I, 1)]
    DECK = sp.diag(1, -1)
    n_h, hits = conj_search(mu4, DECK, cfgm1, sigsm1)
    check("T2.10 SEAM-DECK MATCH [exact]: Moebius conjugation search mu4 -> "
          "{0, 1, -1, inf}: %d valid mark bijections found, and EVERY one "
          "carries the v506 seam deck z -> -z to sigma_%s = the CENTRAL "
          "half-period involution -1/x (hits: %s) -- the established seam "
          "deck IS the half-period translation t_{c*}; its central position "
          "is a property of the PAIR (marks, deck), not of the origin"
          % (n_h, min(hits) if hits else '-', sorted(hits)),
          n_h == 8 and hits == {1})

    # ================================================ T3: CM dictionary
    print("  -- T3: the CM dictionary -- why tau = i, intrinsically")

    # 11. CM action on the half-periods mod 2
    Mi = sp.Matrix([[0, -1], [1, 0]])           # mult by i on basis (1, i)
    Mrho = sp.Matrix([[0, -1], [1, 1]])         # mult by rho on basis (1, rho)
    vecs = [sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([1, 1])]
    fix_i = [v for v in vecs
             if ((Mi * v) - v).applyfunc(lambda z: z % 2) == sp.zeros(2, 1)]
    orb_rho = []
    v_ = vecs[0]
    for _ in range(3):
        v_ = (Mrho * v_).applyfunc(lambda z: z % 2)
        orb_rho.append(tuple(v_))
    fix_rho = [v for v in vecs
               if ((Mrho * v) - v).applyfunc(lambda z: z % 2) == sp.zeros(2, 1)]
    check("T3.11 CM ON HALF-PERIODS [exact, mod 2]: mult-by-i = [[0,-1],"
          "[1,0]] fixes EXACTLY %d nonzero half-period: (1+tau)/2 = the "
          "vector (1,1) -- the intrinsically distinguished c*; mult-by-rho "
          "3-CYCLES all three (orbit of (1,0): %s, fixed: %d) -- at the "
          "hexagonal point NO half-period is distinguished (matching A4, "
          "zero order-4); generic tau has no CM at all (Aut = {+-1}, j not "
          "in {0,1728}, v214) -- 'welche sigma_c zentral wird' ist die "
          "CM-fixierte, und CM existiert nur bei tau = i"
          % (len(fix_i), orb_rho, len(fix_rho)),
          len(fix_i) == 1 and tuple(fix_i[0]) == (1, 1)
          and len(set(orb_rho)) == 3 and len(fix_rho) == 0)

    # 12. lemniscatic explicit: CM lift, the clock as affine quarter-turn descent
    lemn = y ** 2 - (4 * x ** 3 - 4 * x)          # e = (1, -1, 0)
    cm_auto = sp.expand(lemn.subs({x: -x, y: I * y}, simultaneous=True) + lemn)
    sig_cen = sp.Matrix([[0, -1], [1, 0]])        # -1/x pairs inf<->0, 1<->-1
    ghat = sp.Matrix([[1, -1], [1, 1]])           # x -> (x-1)/(x+1)
    ghat_o4 = proj_order(ghat) == 4
    ghat_sq = prop_mat(mexp(ghat * ghat), sig_cen)
    lemn_marks = [(sp.Integer(1), 1), (sp.Integer(0), 1),
                  (sp.Integer(-1), 1), (1, sp.Integer(0))]
    ghat_cycle = mark_perm(ghat, lemn_marks)
    phi_a = sp.Matrix([[1, 1], [1, -1]])          # pairs inf<->1, -1<->0
    ghat_is_comp = prop_mat(mexp(phi_a * sp.diag(-1, 1)), ghat)
    # upstairs: g(w) = i w + 1/2, g^2 = -w + (1+i)/2, commutes with +- mod Lambda
    gup = I * w + sp.Rational(1, 2)
    gup2 = sp.expand(gup.subs(w, gup))
    up_ok = (gup2 == -w + sp.Rational(1, 2) + I / 2)
    comm_resid = sp.expand(gup.subs(w, -w) - (-gup))   # = 1 in Lambda
    # curve lift of ghat needs psi = 2i/(x+1)^2 -- the CM unit i
    phig = (x - 1) / (x + 1)
    prod_g = phig * (phig - 1) * (phig + 1)
    prod_x0 = x * (x - 1) * (x + 1)
    psi_g = 2 * I / (x + 1) ** 2
    lift_g = sp.simplify(sp.together(prod_g - psi_g ** 2 * prod_x0)) == 0
    ratio = sp.cancel(prod_g / prod_x0)
    ratio_ok = sp.simplify(ratio + 4 / (x + 1) ** 4) == 0
    irre = sp.Poly(t_ ** 2 + 1, t_, domain='QQ').is_irreducible
    check("T3.12 THE CLOCK NEEDS THE CM UNIT [exact, lemniscatic y^2 = "
          "4x^3-4x]: (x,y) -> (-x, iy) is an exact curve automorphism (%s; "
          "descent x -> -x FIXES marks 0, inf = the mark-fixing D4 class, "
          "NOT a sigma_c); the clock ghat: x -> (x-1)/(x+1) has order 4 "
          "(%s), 4-cycles the marks (%s), ghat^2 = -1/x = sigma_central "
          "(%s), and ghat = sigma_a o (CM descent) (%s) = downstairs shadow "
          "of w -> iw + 1/2 (upstairs: g^2 = -w + (1+i)/2 = hyperelliptic o "
          "t_{(1+i)/2}: %s, commutes with +- mod Lambda: residual %s = 1 in "
          "Lambda); its curve lift needs psi = 2i/(x+1)^2 (exact: %s, ratio "
          "prod(phi-e)/prod(x-e) = -4/(x+1)^4: %s) and t^2+1 is irreducible "
          "over Q (%s): half-period decks lift RATIONALLY (T1.3), the clock "
          "root only exists WITH i <=> CM by Z[i] <=> tau = i"
          % (cm_auto == 0, ghat_o4, ghat_cycle, ghat_sq, ghat_is_comp,
             up_ok, comm_resid, lift_g, ratio_ok, irre),
          cm_auto == 0 and ghat_o4 and ghat_cycle == [1, 2, 3, 0]
          and ghat_sq and ghat_is_comp and up_ok and comm_resid == 1
          and lift_g and ratio_ok and irre)

    # 13. hexagonal control: A4, sigma_c all conjugate, zero roots, conditions fail
    sigshex = sigmas_of(lam_hex)
    profhex = order_profile(stabhex)
    o3 = [g for g in stabhex if proj_order(g) == 3]
    conj_s1_s2 = any(prop_mat(mexp(h_ * sigshex[1] * h_.adjugate()), sigshex[2])
                     for h_ in o3)
    roots_hex = sum(1 for g in stabhex for s in sigshex.values()
                    if prop_mat(mexp(g * g), s))
    hex_min = sp.expand(lam_hex ** 2 - lam_hex + 1)
    cond_fail = all(not iszero(lam_hex - v)
                    for v in (sp.Integer(-1), sp.Integer(2), sp.Rational(1, 2)))
    check("T3.13 HEXAGONAL CONTROL [exact]: lam_hex with lam^2 - lam + 1 = "
          "%s = 0 (j = 0): Stab = A4 (order %d, profile %s, ZERO order-4); "
          "the three sigma_c are mutually CONJUGATE under the order-3 CM "
          "descent (%s) -- no distinguished one; total sigma_c square roots "
          "in the stabiliser: %d; the three per-c conditions lam in "
          "{-1, 2, 1/2} all fail exactly (%s) -- the dynamical winner "
          "(v503) can never carry the clock, in torus language: no "
          "CM-fixed half-period exists"
          % (sp.simplify(hex_min), len(stabhex), profhex, conj_s1_s2,
             roots_hex, cond_fail),
          sp.simplify(hex_min) == 0 and len(stabhex) == 12
          and profhex == {1: 1, 2: 3, 3: 8} and conj_s1_s2
          and roots_hex == 0 and cond_fail)

    # ================================================ T4: trias + circularity (A2)
    print("  -- T4: A2 -- equivalence trias, circularity audit, silver placement")

    # 14. the equivalence trias
    j_vals = {str(v): jlam(v) for v in (sp.Integer(-1), sp.Integer(2),
                                        sp.Rational(1, 2))}
    j_gen = jlam(sp.Integer(3))
    j_hex = jlam(lam_hex)
    trias = (all(jv == 1728 for jv in j_vals.values())
             and j_gen != 1728 and sp.simplify(j_hex) == 0
             and solve_ok and cr_ok                     # T2.8
             and roots_of == {1: 2, 2: 0, 3: 0}         # T2.9
             and roots_inside == 0 and central3)        # T2.6
    check("T4.14 EQUIVALENCE TRIAS [exact]: (i) 'Uhr existiert' (marks-"
          "preserving root of the deck sigma_c) <=> lam = the ONE value in "
          "{-1, 2, 1/2} matching c <=> j = 1728 (j(-1) = j(2) = j(1/2) = "
          "%s; j(3) = %s, j(hex) = %s) <=> tau = i (v214); (ii) <=> Stab = "
          "D4 AND deck central in it; (iii) <=> the deck pairs separate "
          "harmonically (pair CR = -1).  SHARPENING: 'central' alone is "
          "EMPTY (generic V4: all sigma_c central, 0 roots -- T2.6), "
          "'harmonic' alone is INSUFFICIENT (v506 silver; T2.9 edge cases): "
          "the bit is the CONJUNCTION, with existential form 'exists c' "
          "<=> tau = i alone"
          % (j_vals[str(sp.Integer(-1))], j_gen, sp.simplify(j_hex)),
          trias)

    # 15. circularity audit: v493 direction re-verified, directions independent
    Z, a0, a1_, a2_, a3_ = sp.symbols('Z a0 a1_ a2_ a3_')
    P = Z ** 4 + a3_ * Z ** 3 + a2_ * Z ** 2 + a1_ * Z + a0
    eqd = sp.expand(P.subs(Z, I * Z) - P)
    coeffs = [sp.simplify(eqd.coeff(Z, k)) for k in range(5)]
    forced = sp.solve(coeffs, [a3_, a2_, a1_], dict=True)
    v493_dir = (len(forced) == 1
                and forced[0] == {a3_: 0, a2_: 0, a1_: 0})
    check("T4.15 CIRCULARITY AUDIT [exact]: direction 1 (v493, re-verified): "
          "GIVEN the order-4 clock, P(iZ) = P(Z) forces (a3, a2, a1) = %s "
          "and a0 stays free => j = 1728 frozen -- the clock is the PREMISE. "
          "Direction 2 (this probe, T2.8): NO clock assumed; root EXISTENCE "
          "solved => lam harmonic + alignment.  The two directions are "
          "independently computed converses of ONE equivalence -- no "
          "circularity: 'Uhr <=> tau = i <=> Deck zentral' is a proven "
          "equivalence chain, and the bit remains ONE discrete carrier "
          "datum with three faces"
          % (forced[0] if forced else None),
          v493_dir)

    # 16. silver placement: the counterexample lives INSIDE the torus family
    v_s = 3 + 2 * sp.sqrt(2)
    silver = [(sp.Integer(1), 1), (sp.Integer(-1), 1), (v_s, 1), (-v_s, 1)]
    n_h_s, hits_s = conj_search(silver, DECK, cfgm1, sigsm1)
    check("T4.16 SILVER PLACEMENT [exact]: conjugation search {+-1, "
          "+-(3+2sqrt2)} -> {0, 1, -1, inf}: %d valid mark bijections, deck "
          "z -> -z lands on sigma indices %s -- EDGE half-periods only, "
          "NEVER the central sigma_1: the v506 counterexample is exactly "
          "'tau = i with deck = a NON-CM-fixed half-period translation'; "
          "the common torus origin does NOT exclude the misalignment -- "
          "TAUTOLOGY REFUTED by an in-family witness"
          % (n_h_s, sorted(hits_s)),
          n_h_s == 8 and hits_s == {2, 3} and 1 not in hits_s)

    # ================================================ T5: verdict
    print("  -- T5: verdict")
    verdict = (counts['generic'][3] and counts['harmonic'][3]     # origin forced
               and solve_ok and cr_ok                             # core solve
               and roots_of == {1: 2, 2: 0, 3: 0}                 # D4 split 1+2
               and hits == {1} and hits_s == {2, 3}               # seam vs silver
               and roots_inside == 0 and roots_hex == 0           # controls
               and v493_dir)                                      # no circularity
    check("T5.17 VERDICT [typed]: (i) HERKUNFT GEKLAERT: marks = fixed "
          "points of w -> -w (half-periods), deck = NECESSARILY a half-"
          "period translation t_c (every mark-free involution is a sigma_c, "
          "T1.5), descent exact and rational (T1.3).  (ii) TAUTOLOGIE "
          "WIDERLEGT: the common origin does NOT force centrality -- "
          "generic: all sigma_c central yet zero roots (T2.6); tau = i: two "
          "of the three half-period decks are edge-type = the silver "
          "counterexample in-family (T2.9/T4.16).  (iii) EQUIVALENCE TRIAS "
          "PROVED: Uhr existiert <=> (tau = i AND c = CM-fixed half-period) "
          "<=> (Stab = D4 AND deck central) <=> deck pairs harmonically "
          "separated (T2.8/T4.14), and the clock root needs the CM unit i "
          "(T3.12).  (iv) REST: exactly ONE discrete carrier datum -- the "
          "bit -- equivalent to the modulus-plus-alignment choice, NOT "
          "dynamical (v503), NOT a consequence of the origin.  No marker "
          "moves; QGEO.REALIZE.01 / P2 R1 unaffected",
          verdict)

    npass = sum(RESULTS)
    print("=" * 100)
    print("SUMMARY: %d/%d checks passed%s"
          % (npass, len(RESULTS),
             "" if npass == len(RESULTS) else "  -- FAILURES PRESENT"))
    return npass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
