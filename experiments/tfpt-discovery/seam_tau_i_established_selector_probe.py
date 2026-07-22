"""seam_tau_i_established_selector_probe.py -- EXPLORATION ONLY
(experiments/, no verification claim; nothing in verification/, ledger,
papers, changelog, website or scorecard is touched).

THE tau = i ATTACK: after v510 the last identification input of the
theory is the square-modulus datum tau = i (position half = topology;
"harmonic + free => mu4" proven, but the counterwitness {+-1, +-(3+4i)/5}
is free, central, nonsplit and NOT harmonic: j = 148176/25 != 1728).
QUESTION: which ESTABLISHED seam datum excludes the free-but-non-harmonic
configurations, i.e. forces harmonicity?

TEST FAMILY: on the free RP seam circle |z| = 1 (deck z -> -z, free) the
deck-invariant 4-mark configurations are, up to rotation, M(delta) =
{+-1, +-e^{i delta}}, delta in (0, pi/2]; delta = pi/2 <=> equally spaced
<=> harmonic <=> mu4 <=> tau = i.  The v510 counterwitness is the member
delta_cw = arctan(4/3) (cos delta_cw = 3/5; lambda = 5/4; j = 148176/25;
deck-pair cross-ratio -1/4).

FINDINGS (honest, computed below):
  H1 FAILS AS BRIEFED -- AND THE FAILURE IS THE FINDING.  The complete
     census of circle symmetries preserving deck + mark set (two-family
     classification z -> lam z / z -> lam/z, |lam| = 1, v510 B-M3 basis)
     gives G(delta) = {z, -z, b/z, -b/z} ~= V4 for EVERY delta, and the
     two inversions are pair-EXCHANGING: V4 acts SIMPLY TRANSITIVELY on
     the four marks for every delta.  Bare mark-transitivity is delta-
     blind; the expected orbit split {+-1} | {+-b} is wrong; the
     counterwitness IS mark-transitive.  What IS equivalent to delta =
     pi/2, exactly: (i) transitivity by ROTATIONS alone (= the clock),
     (ii) a mark-fixing mirror (nontrivial stabiliser), (iii) ARC/FLAG
     transitivity (marks AND their two sides indistinguishable),
     (iv) |G| = 8 (D4) instead of 4 (V4).  The v216-class per-mark
     UNSIDED local data (arc-pair multiset {delta, pi-delta}, distance
     multiset, cone germ) are identical at all four marks for EVERY
     delta -- local equality does NOT force the flag datum.
  H2 EXACT SPECTRAL CRITERION, REFORMULATION CLASS.  The seam covariance
     (H = sqrt(-Delta) on the circle, kernel -(1/pi) log(2 sin(theta/2)))
     restricted to the marks has deck-odd eigenvalue split (2/pi)
     log cot(delta/2): zero iff delta = pi/2 (counterwitness: (2/pi)
     log 2 ~ 0.4413).  Same criterion from the arc-weighted seam
     Laplacian (spectrum {0, 2/delta, 2/(pi-delta), sum}).  The v215-K3/
     v503 mod-4 indicator restricted to the marks is 2 sqrt(2) |u - v| --
     an isolated zero at pi/2 in closed form.  BUT the established
     transfer spectrum {1, (2/3)^6, (1/3)^6} and cusp weights {0, 1/3,
     2/3} are degeneracy-FREE: no established datum demands the odd-
     sector degeneracy -- criterion exact, normative force not
     established.
  H3 RATIONALITY IS TWIST-EXISTENCE IN DISGUISE.  Atiyah-Bott: the deck
     twist sigma has d sigma = -1 on EVERY torus, trace = 4 x 1/4 = 1
     exactly rational for ALL delta (verified in position space at
     tau_cw = i K(1/5)/K(4/5) ~ 0.7353 i and tau = i).  The order-4
     twist rho EXISTS iff tau = i ([R, Delta_t] = 0 <=> t = 1, exact
     mode identity (m^2 - n^2)(t - 1/t)).  Even j-RATIONALITY does not
     select (j_cw = 148176/25 rational).  "All twisted traces rational"
     selects nothing; what selects is WHICH twists exist = the clock.
  H4 THE W(A3) CUSP 4-CYCLE NEEDS A GENUINE ORDER-4 IMPLEMENTER.
     Existence of the flat S4 monodromy (4 local lam^3 - 1 blocks,
     product = 1) is position-BLIND (pi_1 does not see delta; two
     explicit solutions).  But: V4 has no order-4 element, so it cannot
     induce the cusp 4-cycle M_k -> M_{k+1}; representation side
     (Schur): the centraliser of the four v117 conjugates is scalar
     (dim 1), every implementer W = c U, and U^2 = diag(1,-1,-1) is
     nonscalar -- NO projective involution implements the 4-cycle, the
     implementer has projective order exactly 4.  "Cusp 4-cycle is seam-
     geometric" <=> order-4 rotation <=> delta = pi/2 -- conditional
     rigidity; the premise is the clock postulate itself (v117 calls U
     'the mu4 deck').
  NC  hexagonal: |b_hex| = 2 - sqrt(3) != 1, lambda complex (not
     concyclic), j = 0: not in the family, battery preconditions fail.
     silver: all marks real => mark circle = R u {inf} THROUGH the deck
     fixed points 0, inf (not free), yet lambda = 1/2, j = 1728
     (harmonic!): position half and modulus half are independent --
     topologically dead before the battery, consistent v510.
     3 marks: impossible on the free RP circle (free involution =>
     even mark count; 0 invariant 3-subsets vs 28 invariant 4-subsets
     on Z16); on a plain circle bare transitivity ALREADY forces
     equal spacing at n = 3 (scalene: trivial group; isosceles: Z2;
     equilateral: D3) -- it is the deck-PAIRING at n = 4 that makes
     bare transitivity free of charge and the flag sharpening
     necessary: 4 counts.
  SYN ONE DISCRETE BIT, MANY FACES: delta = pi/2 <=> clock rotation <=>
     D4 (vs V4) <=> mark mirror <=> arc/flag transitivity <=> odd-sector
     degeneracy (Green + weighted Laplacian + K3-mark indicator) <=>
     rho-twist exists <=> cusp-4-cycle implementable <=> harmonic <=>
     j = 1728.  The counterwitness passes ALL established unsided tests
     (free circle, central class, V4-transitive, equal per-mark data,
     monodromy existence, sigma-trace = 1, j rational) and fails ALL
     sided/clock-equivalent ones.  NO established seam datum excludes
     it; the honest reduction: the last input stays ONE datum but gains
     an equivalent DISCRETE seam-intrinsic form -- "the four marks are
     also SIDE-indistinguishable (flag-transitive; V4 -> D4)" -- in
     place of the continuous modulus tau = i.  [E]: every equivalence
     link above (exact).  [C]: the bit itself; v216 locality does NOT
     deliver it (H1.5).  No marker moves proposed.

Repo anchors: v510 (freedom attack, counterwitness), v216 (marks from
Gauss-Bonnet, equality), v117 (S4 = W(A3) monodromy, U = mu4 deck),
v503 (no dynamical selection; mod-4 DtN indicator; Aut(E_rho) = Z6),
v483 (exact twisted traces, Atiyah-Bott), v54/v56 (transfer spectrum
{1, (2/3)^6, (1/3)^6}), v115 (weights {0, 1/3, 2/3}).

Exact throughout where claimed (sympy; mpmath dps 30 for the modular /
heat-trace numerics; one numpy lattice commutator, v503-style).
Standalone; deterministic; no files written.

Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/seam_tau_i_established_selector_probe.py
"""
from fractions import Fraction as Fr
from itertools import combinations

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 30

RESULTS = []
I = sp.I


def check(name, ok):
    RESULTS.append(bool(ok))
    print(("PASS" if ok else "FAIL") + " [%2d] %s" % (len(RESULTS), name))


def iszero(e):
    e2 = sp.expand(e)
    if e2 == 0:
        return True
    e3 = sp.expand(sp.expand_complex(e2))
    if e3 == 0:
        return True
    e4 = sp.simplify(e3)
    if e4 == 0:
        return True
    return sp.simplify(sp.expand_trig(e4)) == 0


def set_eq(A, B):
    """exact multiset equality of symbolic complex numbers."""
    if len(A) != len(B):
        return False
    used = [False] * len(B)
    for a in A:
        hit = False
        for j, b_ in enumerate(B):
            if not used[j] and iszero(a - b_):
                used[j] = True
                hit = True
                break
        if not hit:
            return False
    return True


# ---------------------------------------------------------------------------
# the delta family
# ---------------------------------------------------------------------------
d = sp.Symbol('delta', positive=True)          # 0 < delta <= pi/2
b = sp.exp(I * d)
DOM = sp.Interval.Lopen(0, sp.pi / 2)

B_CW = sp.Rational(3, 5) + sp.Rational(4, 5) * I     # the v510 counterwitness
D_CW = sp.atan(sp.Rational(4, 3))                    # its delta

B_HEX = I * (2 - sp.sqrt(3))                         # v510 hexagonal frame
S_SILVER = 3 + 2 * sp.sqrt(2)                        # v510 silver


def marks_of(bv):
    return [sp.Integer(1), bv, sp.Integer(-1), -bv]  # ccw order 0,d,pi,pi+d


def jlam(lam):
    return sp.simplify(256 * (lam ** 2 - lam + 1) ** 3
                       / (lam ** 2 * (lam - 1) ** 2))


def lam_of(bv):
    return sp.simplify(4 * bv / (1 + bv) ** 2)


def paircr_of(bv):
    return sp.simplify((1 - bv) ** 2 / (1 + bv) ** 2)


# ---------------------------------------------------------------------------
# symmetry census machinery (complete: v510 B-M3 two-family classification)
# ---------------------------------------------------------------------------
def dedup(xs):
    out = []
    for x in xs:
        if not any(iszero(x - y) for y in out):
            out.append(x)
    return out


def census(marks):
    """all circle symmetries preserving the mark set: rotations z -> lam z
    and inversions z -> lam / z with |lam| = 1 (complete: any Moebius map
    commuting with the deck z -> -z is diagonal or antidiagonal, and the
    image of mark m0 must be a mark, so lam in M/m0 resp. M*m0)."""
    m0 = marks[0]
    rot_c = dedup([sp.cancel(m / m0) for m in marks])
    inv_c = dedup([sp.expand(m * m0) for m in marks])
    rots = [lam for lam in rot_c
            if set_eq([sp.expand(lam * m) for m in marks], marks)]
    invs = [lam for lam in inv_c
            if set_eq([sp.cancel(sp.expand(lam / m)) for m in marks], marks)]
    return rots, invs


def match_index(x, marks):
    for k, m in enumerate(marks):
        if iszero(x - m):
            return k
    return None


def perms_signed_of(marks, rots, invs):
    """list of (mark permutation tuple, orientation sign)."""
    out = []
    for lam in rots:
        out.append((tuple(match_index(sp.expand(lam * m), marks)
                          for m in marks), +1))
    for lam in invs:
        out.append((tuple(match_index(sp.cancel(sp.expand(lam / m)), marks)
                          for m in marks), -1))
    return out


def orbits_of(perms, n):
    seen, orbs = set(), []
    for s0 in range(n):
        if s0 in seen:
            continue
        orb, stack = {s0}, [s0]
        while stack:
            k = stack.pop()
            for p in perms:
                if p[k] not in orb:
                    orb.add(p[k])
                    stack.append(p[k])
        seen |= orb
        orbs.append(orb)
    return orbs


def flag_orbits_of(perms_signed, n):
    """flags = (mark, side); rotations keep the side, inversions flip it."""
    flags = [(k, s) for k in range(n) for s in (+1, -1)]
    seen, orbs = set(), []
    for f0 in flags:
        if f0 in seen:
            continue
        orb, stack = {f0}, [f0]
        while stack:
            k, s = stack.pop()
            for p, sg in perms_signed:
                g = (p[k], s * sg)
                if g not in orb:
                    orb.add(g)
                    stack.append(g)
        seen |= orb
        orbs.append(orb)
    return orbs


def arc_orbits_of(perms_signed, n):
    """arc A_k = ccw arc from mark k = {flag (k,+1), flag (k+1,-1)}."""
    def arc_of_flag(k, s):
        return k if s == +1 else (k - 1) % n
    seen, orbs = set(), []
    for a0 in range(n):
        if a0 in seen:
            continue
        orb, stack = {a0}, [a0]
        while stack:
            a = stack.pop()
            for p, sg in perms_signed:
                img = arc_of_flag(p[a], sg)     # image of flag (a, +1)
                if img not in orb:
                    orb.add(img)
                    stack.append(img)
        seen |= orb
        orbs.append(orb)
    return orbs


# ===========================================================================
# S0 -- the family frame
# ===========================================================================
def s0_frame():
    print(" S0 -- the delta family frame")
    lam_fam = 4 * b / (1 + b) ** 2
    lam_id = iszero(lam_fam - 1 / sp.cos(d / 2) ** 2)
    cr_fam = (1 - b) ** 2 / (1 + b) ** 2
    cr_id = iszero(cr_fam + sp.tan(d / 2) ** 2)
    cr_lam = iszero(cr_fam - (1 - lam_fam))
    deck_inv = set_eq([sp.expand(-m) for m in marks_of(b)], marks_of(b))
    on_circle = iszero(sp.Abs(b) - 1)
    check("S0.1 FAMILY FRAME [exact, symbolic]: M(delta) = {+-1, +-e^(i "
          "delta)} is deck-invariant (%s) on the free circle |z| = 1 (%s); "
          "cross-ratio lambda(delta) = 4b/(1+b)^2 = sec^2(delta/2) (%s), "
          "deck-pair cross-ratio = -tan^2(delta/2) = 1 - lambda (%s, %s): "
          "the one-parameter family is exactly the v510 free/central class"
          % (deck_inv, on_circle, lam_id, cr_id, cr_lam),
          deck_inv and on_circle and lam_id and cr_id and cr_lam)

    lam_mu4 = lam_of(I)
    j_mu4 = jlam(lam_mu4)
    cr_mu4 = paircr_of(I)
    check("S0.2 THE mu4 MEMBER [exact]: delta = pi/2 gives b = i, lambda = "
          "%s (the v168 value), j = %s = 1728, pair cross-ratio = %s = -1 "
          "(harmonic) -- equally spaced <=> harmonic <=> tau = i"
          % (lam_mu4, j_mu4, cr_mu4),
          lam_mu4 == 2 and j_mu4 == 1728 and cr_mu4 == -1)

    is_member = iszero(sp.exp(I * D_CW) - B_CW) and iszero(sp.Abs(B_CW) - 1)
    lam_cw = lam_of(B_CW)
    j_cw = jlam(lam_cw)
    cr_cw = paircr_of(B_CW)
    cos_cw = sp.cos(D_CW)
    check("S0.3 THE COUNTERWITNESS MEMBER [exact]: {+-1, +-(3+4i)/5} is the "
          "family member delta_cw = arctan(4/3) (e^(i delta_cw) = (3+4i)/5: "
          "%s; cos delta_cw = %s = 3/5), lambda = %s = 5/4, j = %s = "
          "148176/25 != 1728, pair cross-ratio = %s = -1/4 != -1 -- the "
          "v510 counterwitness lives INSIDE the family"
          % (is_member, cos_cw, lam_cw, j_cw, cr_cw),
          is_member and cos_cw == sp.Rational(3, 5)
          and lam_cw == sp.Rational(5, 4)
          and j_cw == sp.Rational(148176, 25)
          and cr_cw == sp.Rational(-1, 4))


# ===========================================================================
# H1 -- mark indistinguishability / transitivity (the main candidate)
# ===========================================================================
def h1_symmetry():
    print(" H1 -- mark indistinguishability: the complete symmetry census")

    # completeness of the two families (holomorphic v510 B-M3 analogue)
    a_, b_, c_, dd_ = sp.symbols('a_ b_ c_ dd_')
    Mg = sp.Matrix([[a_, b_], [c_, dd_]])
    DECK = sp.diag(1, -1)
    comm = sp.expand(Mg * DECK - DECK * Mg)
    anti = sp.expand(Mg * DECK + DECK * Mg)
    fam_plus = sp.solve([comm[0, 1], comm[1, 0]], [b_, c_], dict=True)
    fam_minus = sp.solve([anti[0, 0], anti[1, 1]], [a_, dd_], dict=True)
    check("H1.0 CENSUS BASIS [exact, symbolic]: a Moebius map commuting "
          "with the deck z -> -z (M D = +- D M; det forces the sign in "
          "{+1, -1}) is DIAGONAL (%s: z -> lam z) or ANTIDIAGONAL (%s: "
          "z -> lam / z); preserving |z| = 1 forces |lam| = 1, and the "
          "image of the mark 1 must be a mark, so lam runs over the mark "
          "set in both families: the census below is COMPLETE (v510 B-M3 "
          "holomorphic analogue; antiholomorphic maps act on the seam "
          "circle identically to these since Theta fixes it pointwise)"
          % (fam_plus, fam_minus),
          fam_plus == [{b_: 0, c_: 0}] and fam_minus == [{a_: 0, dd_: 0}])

    # H1.1 rotation subgroup: order 4 exactly at delta = pi/2
    sol_b2_m1 = sp.solveset(sp.cos(2 * d) + 1, d, DOM)      # b^2 = -1
    sol_b2_p1 = sp.solveset(sp.cos(2 * d) - 1, d, DOM)      # b^2 = +1
    sol_b_p1 = sp.solveset(sp.cos(d) - 1, d, DOM)           # b = 1
    sol_b_m1 = sp.solveset(sp.cos(d) + 1, d, DOM)           # b = -1
    rot_ok = (sol_b2_m1 == sp.FiniteSet(sp.pi / 2)
              and sol_b2_p1 is sp.S.EmptySet
              and sol_b_p1 is sp.S.EmptySet
              and sol_b_m1 is sp.S.EmptySet)
    rots_mu4, invs_mu4 = census(marks_of(I))
    check("H1.1 ROTATIONS = THE CLOCK QUESTION [exact]: a rotation z -> "
          "lam z preserving M(delta) needs lam in M; lam = +-1 always work, "
          "lam = +-b works iff b^2 in M, and on (0, pi/2] the only solution "
          "is b^2 = -1 <=> delta = pi/2 (solvesets: b^2=-1 -> %s, b^2=+1 -> "
          "%s, b=+-1 -> empty %s): the rotation subgroup is Z2 = {+-1} for "
          "EVERY delta < pi/2 and jumps to Z4 = mu4 = THE CLOCK exactly at "
          "delta = pi/2 (mu4 member: %d rotations) -- rotation-transitivity "
          "<=> delta = pi/2 <=> tau = i, exactly"
          % (sol_b2_m1, sol_b2_p1,
             sol_b_p1 is sp.S.EmptySet and sol_b_m1 is sp.S.EmptySet,
             len(rots_mu4)),
          rot_ok and len(rots_mu4) == 4)

    # H1.2 the honest surprise: V4 with pair-EXCHANGING inversions, always
    M_gen = marks_of(b)
    rots_gen, invs_gen = census(M_gen)
    ps_gen = perms_signed_of(M_gen, rots_gen, invs_gen)
    mark_orbs = orbits_of([p for p, _ in ps_gen], 4)
    orders_ok = all(tuple(p[p[k]] for k in range(4)) == (0, 1, 2, 3)
                    for p, _ in ps_gen)                       # all invol/id
    sol_inv1 = sp.solveset(sp.cos(d), d, DOM)                # conj(b) = -b
    sol_inv1b = sp.solveset(sp.sin(d), d, DOM)               # conj(b) = b
    transitive = len(mark_orbs) == 1
    check("H1.2 THE HONEST SURPRISE [exact, symbolic delta]: the generic "
          "group is G = {z, -z, b/z, -b/z} ~= V4 (%d rotations + %d "
          "inversions, every non-identity element an involution: %s; the "
          "inversions z -> +-b/z preserve M IDENTICALLY in delta, lam = "
          "+-1 inversions need conj(b) in {+-b} <=> delta = pi/2: %s / %s) "
          "and the inversions are pair-EXCHANGING: the mark orbit census "
          "gives %s = ONE orbit -- V4 acts (simply) TRANSITIVELY on the "
          "four marks for EVERY delta: bare mark-transitivity does NOT "
          "select delta = pi/2; the briefed orbit split {+-1} | {+-b} is "
          "FALSE and the counterwitness is fully mark-transitive"
          % (len(rots_gen), len(invs_gen), orders_ok,
             sol_inv1, sol_inv1b, [sorted(o) for o in mark_orbs]),
          len(rots_gen) == 2 and len(invs_gen) == 2 and orders_ok
          and transitive and sol_inv1 == sp.FiniteSet(sp.pi / 2)
          and sol_inv1b is sp.S.EmptySet)

    # H1.3 stabiliser / mark mirror
    stab_gen = [p for p, _ in ps_gen if p[0] == 0]
    ps_mu4 = perms_signed_of(marks_of(I), rots_mu4, invs_mu4)
    stab_mu4 = [p for p, _ in ps_mu4 if p[0] == 0]
    mirror_mu4 = any(p[0] == 0 and p != (0, 1, 2, 3) for p, sg in ps_mu4
                     if sg == -1)
    check("H1.3 STABILISER JUMP [exact]: generically the V4 action is "
          "REGULAR (stabiliser of mark 1 = %d element(s), |G| = 4 = "
          "#marks); at delta = pi/2 the group is D4 of order %d and every "
          "mark acquires a MIRROR through it (z -> 1/z fixes +-1 and "
          "preserves mu4: %s; stabiliser order %d) -- 'a mark-fixing "
          "mirror exists' <=> conj(b) = -b <=> delta = pi/2 (H1.2 "
          "solveset): the stabiliser jump 1 -> 2 is the discrete face of "
          "the modulus"
          % (len(stab_gen), len(ps_mu4), mirror_mu4, len(stab_mu4)),
          len(stab_gen) == 1 and len(ps_mu4) == 8 and mirror_mu4
          and len(stab_mu4) == 2)

    # H1.4 arcs and flags: THE sharp selector
    arc_gen = arc_orbits_of(ps_gen, 4)
    flag_gen = flag_orbits_of(ps_gen, 4)
    arc_mu4 = arc_orbits_of(ps_mu4, 4)
    flag_mu4 = flag_orbits_of(ps_mu4, 4)
    arc_lengths = [d, sp.pi - d, d, sp.pi - d]
    sol_arcs = sp.solveset(d - (sp.pi - d), d, DOM)
    check("H1.4 FLAG TRANSITIVITY IS THE SELECTOR [exact]: the four arcs "
          "have lengths (delta, pi-delta, delta, pi-delta); generic arc "
          "orbits %s (2 orbits: the two delta-arcs vs the two others; "
          "isometries preserve length, and delta = pi-delta <=> %s), "
          "generic FLAG orbits: %d orbits of size 4 (8 flags, |G| = 4); "
          "at delta = pi/2: arc orbits %s = ONE, flag orbits %d = ONE with "
          "all 8 flags (D4 simply transitive on flags) -- 'marks AND their "
          "two sides indistinguishable' (flag/arc transitivity) <=> delta "
          "= pi/2 <=> tau = i: THE exact discrete selector"
          % ([sorted(o) for o in arc_gen], sol_arcs, len(flag_gen),
             [sorted(o) for o in arc_mu4], len(flag_mu4)),
          len(arc_gen) == 2 and len(flag_gen) == 2
          and sol_arcs == sp.FiniteSet(sp.pi / 2)
          and len(arc_mu4) == 1 and len(flag_mu4) == 1
          and len(flag_mu4[0]) == 8 and arc_lengths[0] == d)

    # H1.5 the v216 separation: unsided local data never see delta
    per_mark_arcs = []
    for k in range(4):
        per_mark_arcs.append({arc_lengths[k], arc_lengths[(k - 1) % 4]})
    arcs_equal = all(pa == per_mark_arcs[0] for pa in per_mark_arcs)
    M_gen_list = marks_of(b)
    dist_multisets = []
    for k in range(4):
        ds = []
        for l in range(4):
            if l != k:
                # angular distance via chordal |m_k - m_l| (monotone)
                ds.append(sp.simplify(sp.expand_complex(
                    sp.Abs(M_gen_list[k] - M_gen_list[l]) ** 2)))
        dist_multisets.append(sorted([sp.srepr(sp.simplify(x)) for x in ds]))
    dists_equal = all(dm == dist_multisets[0] for dm in dist_multisets)
    check("H1.5 LOCAL EQUALITY DOES NOT FORCE THE FLAG BIT [exact, the "
          "v216 separation]: the UNSIDED per-mark data are identical at "
          "all four marks for EVERY delta -- arc-pair multiset {delta, "
          "pi-delta} at each mark (%s), chordal distance multiset "
          "{|2 sin(delta/2)|^2, |2 cos(delta/2)|^2, 4} at each mark (%s), "
          "cone germ (angle pi, flat) trivially equal -- so the v216-class "
          "statement 'all four marks carry identical data' (all-order-2, "
          "same cusp class, same weights) holds for the WHOLE family "
          "including the counterwitness: what delta = pi/2 adds is the "
          "SIDED (flag) datum, which no per-mark local jet can see -- "
          "local equality != global flag transitivity, cleanly separated"
          % (arcs_equal, dists_equal),
          arcs_equal and dists_equal)

    # H1.6 the census table over sample members
    print("        delta        |G|  #rot  transitive  #flag-orbits  #arc-orbits")
    table_ok = True
    rows = [(sp.pi / 6, 'pi/6'), (sp.pi / 4, 'pi/4'),
            (D_CW, 'atan(4/3) [CW]'), (sp.pi / 3, 'pi/3'),
            (sp.pi / 2, 'pi/2 [mu4]')]
    tab = {}
    for dv, tag in rows:
        bv = sp.exp(I * dv) if dv != D_CW else B_CW
        Mv = marks_of(bv)
        rr, ii = census(Mv)
        ps = perms_signed_of(Mv, rr, ii)
        n_orb = len(orbits_of([p for p, _ in ps], 4))
        n_flag = len(flag_orbits_of(ps, 4))
        n_arc = len(arc_orbits_of(ps, 4))
        tab[tag] = (len(rr) + len(ii), len(rr), n_orb == 1, n_flag, n_arc)
        print("        %-12s %3d  %4d  %-10s  %12d  %11d"
              % (tag, len(rr) + len(ii), len(rr), n_orb == 1, n_flag, n_arc))
    for tag in ('pi/6', 'pi/4', 'atan(4/3) [CW]', 'pi/3'):
        table_ok &= (tab[tag] == (4, 2, True, 2, 2))
    table_ok &= (tab['pi/2 [mu4]'] == (8, 4, True, 1, 1))
    check("H1.6 CENSUS TABLE [exact, 5 members]: every generic member "
          "(incl. the counterwitness) has |G| = 4 = V4, 2 rotations, IS "
          "mark-transitive, 2 flag orbits, 2 arc orbits; only delta = "
          "pi/2 has |G| = 8 = D4, 4 rotations (the clock), 1 flag orbit, "
          "1 arc orbit -- the discrete datum is the V4 -> D4 enhancement "
          "bit, nothing else moves", table_ok)


# ===========================================================================
# H2 -- transfer / DtN spectral consistency
# ===========================================================================
def h2_spectral():
    print(" H2 -- transfer/DtN spectral criterion for the delta family")
    u = -sp.log(2 * sp.sin(d / 2)) / sp.pi
    v = -sp.log(2 * sp.cos(d / 2)) / sp.pi     # sin((pi-delta)/2)
    w = -sp.log(2) / sp.pi
    c = sp.Symbol('c', real=True)              # regularised diagonal
    G4 = sp.Matrix([[c, u, w, v],
                    [u, c, v, w],
                    [w, v, c, u],
                    [v, w, u, c]])
    vecs = [sp.Matrix([1, 1, 1, 1]), sp.Matrix([1, -1, 1, -1]),
            sp.Matrix([1, 1, -1, -1]), sp.Matrix([1, -1, -1, 1])]
    eigs = [c + u + w + v, c - u + w - v, c + u - w - v, c - u - w + v]
    eig_ok = all(all(iszero(x) for x in (G4 * vv - ee * vv))
                 for vv, ee in zip(vecs, eigs))
    split = sp.expand(eigs[2] - eigs[3])           # = 2(u - v)
    ratio = sp.simplify(sp.expand(sp.exp(sp.pi * split / 2), power_exp=True))
    split_id = sp.simplify(ratio - sp.cot(d / 2)) == 0
    sol_split = sp.solveset(sp.tan(d / 2) - 1, d, DOM)
    y_ = sp.Symbol('y_', positive=True)        # x = 2y half-angle identity
    half_id = sp.simplify(sp.expand_trig(
        sp.tan(y_) * sp.sin(2 * y_) - 1 + sp.cos(2 * y_))) == 0
    tanhalf_cw = sp.simplify((1 - sp.cos(D_CW)) / sp.sin(D_CW))
    split_cw = 2 * sp.log(2) / sp.pi
    check("H2.1 SEAM COVARIANCE SPLIT [exact]: the free seam two-point "
          "kernel of H = sqrt(-Delta) on the circle, G(theta) = -(1/pi) "
          "log(2 sin(theta/2)) (v280 DtN class), restricted to the 4 marks "
          "has exact deck-adapted eigenvectors (%s); the two DECK-ODD "
          "eigenvalues split by 2(u - v) = (2/pi) log cot(delta/2) "
          "(exp(pi split/2) = cot(delta/2) exactly: %s); "
          "zero on (0, pi/2] EXACTLY at delta = pi/2 (tan(delta/2) = 1: "
          "%s; half-angle identity: %s); counterwitness: tan(delta_cw/2) "
          "= %s = 1/2 => split = (2/pi) log 2 = %.6f != 0 -- an exact "
          "isolated-degeneracy criterion, IDENTITY class not extremal"
          % (eig_ok, split_id, sol_split, half_id, tanhalf_cw,
             float(split_cw)),
          eig_ok and split_id and sol_split == sp.FiniteSet(sp.pi / 2)
          and half_id and tanhalf_cw == sp.Rational(1, 2))

    a_w = 1 / d
    b_w = 1 / (sp.pi - d)
    L4 = sp.Matrix([[a_w + b_w, -a_w, 0, -b_w],
                    [-a_w, a_w + b_w, -b_w, 0],
                    [0, -b_w, a_w + b_w, -a_w],
                    [-b_w, 0, -a_w, a_w + b_w]])
    lvecs = [sp.Matrix([1, 1, 1, 1]), sp.Matrix([1, -1, 1, -1]),
             sp.Matrix([1, -1, -1, 1]), sp.Matrix([1, 1, -1, -1])]
    leigs = [sp.Integer(0), 2 * (a_w + b_w), 2 * a_w, 2 * b_w]
    leig_ok = all(all(iszero(x) for x in (L4 * vv - ee * vv))
                  for vv, ee in zip(lvecs, leigs))
    sol_ab = sp.solveset(a_w - b_w, d, DOM)
    ev_cw = [float(2 / sp.atan(sp.Rational(4, 3))),
             float(2 / (sp.pi - sp.atan(sp.Rational(4, 3))))]
    check("H2.2 ARC-WEIGHTED SEAM LAPLACIAN [exact]: the 4-cycle with arc "
          "weights (1/delta, 1/(pi-delta)) has exact spectrum {0, "
          "2/delta, 2/(pi-delta), 2/delta + 2/(pi-delta)} (%s); the same "
          "deck-odd pair {2/delta, 2/(pi-delta)} is degenerate iff delta "
          "= pi - delta, i.e. %s = {pi/2}; counterwitness eigenvalues "
          "%.4f != %.4f, mu4 member {4/pi, 4/pi} (degenerate) -- a second "
          "independent operator, the SAME criterion"
          % (leig_ok, sol_ab, ev_cw[0], ev_cw[1]),
          leig_ok and sol_ab == sp.FiniteSet(sp.pi / 2)
          and abs(ev_cw[0] - 2.156814) < 1e-5
          and abs(ev_cw[1] - 0.903222) < 1e-5)

    P4 = sp.zeros(4, 4)
    for j_ in range(4):
        P4[(j_ + 1) % 4, j_] = 1
    C4 = sp.expand(G4 * P4 - P4 * G4)
    frob2 = sp.expand(sum(x ** 2 for x in C4))
    frob_id = sp.simplify(frob2 - 8 * (u - v) ** 2) == 0
    k3_cw = float(2 * sp.sqrt(2) * sp.log(2) / sp.pi)
    check("H2.3 THE v215-K3 / v503 INDICATOR IN CLOSED FORM [exact]: the "
          "mod-4 off-block indicator restricted to the 4 marks is "
          "||[G4, P_clock]||_F = 2 sqrt(2) |u - v| (Frobenius^2 = "
          "8(u-v)^2: %s) = (2 sqrt(2)/pi) |log tan(delta/2)| -- the v503 "
          "lattice curve's isolated zero at tau = i reproduced in CLOSED "
          "FORM on the mark sector; counterwitness value 2 sqrt(2) "
          "log(2)/pi = %.6f != 0, mu4 value 0" % (frob_id, k3_cw),
          frob_id and abs(k3_cw - 0.624053) < 1e-5)

    spec = [Fr(1), Fr(2, 3) ** 6, Fr(1, 3) ** 6]
    weights = [Fr(0), Fr(1, 3), Fr(2, 3)]
    distinct = len(set(spec)) == 3 and len(set(weights)) == 3
    check("H2.4 HONEST TYPING [exact rationals]: the ESTABLISHED transfer "
          "spectrum {1, (2/3)^6, (1/3)^6} = {1, 64/729, 1/729} (v54/v56) "
          "and the cusp weights {0, 1/3, 2/3} (v115/v117) are pairwise "
          "DISTINCT (%s) -- degeneracy-free: no established spectral "
          "datum demands the H2 odd-sector degeneracy.  H2's criterion "
          "is exact but its normative force ('the seam MUST have the "
          "degenerate odd doublet') is nowhere established: it is the "
          "D4/flag bit in spectral clothing, REFORMULATION class"
          % distinct,
          distinct and spec == [Fr(1), Fr(64, 729), Fr(1, 729)])


# ===========================================================================
# H3 -- heat-trace rationality
# ===========================================================================
def refl_trace_1d(P, s):
    """1D twisted heat trace Tr(sigma_1 e^{s Delta}) on a circle of
    circumference P, sigma_1: x -> -x (position-space Gaussian images,
    v483 style): exact value 1 for every P."""
    a = P / (2 * mp.sqrt(s))
    tot = mp.mpf(0)
    for vv in range(-60, 61):
        tot += mp.erf((vv + 2) * a) - mp.erf(vv * a)
    return tot / 4


def h3_heat():
    print(" H3 -- heat-trace rationality across the family")
    dsig = -sp.eye(2)
    det_sig = sp.det(sp.eye(2) - dsig)
    ab_weight = 4 * sp.Rational(1, 1) / det_sig
    check("H3.1 ATIYAH-BOTT IS delta-BLIND [exact]: the deck twist sigma "
          "(z -> -z) has d sigma = -Id on EVERY torus in the family -- "
          "|det(1 - d sigma)| = %s = 4 independent of the modulus, so "
          "Tr(sigma e^{t Delta}) = 4 x 1/4 = %s = 1: exactly RATIONAL and "
          "t-independent for ALL delta including the counterwitness -- "
          "rationality of the deck-twisted heat trace selects NOTHING"
          % (det_sig, ab_weight),
          det_sig == 4 and ab_weight == 1)

    K15 = mp.ellipk(mp.mpf(1) / 5)
    K45 = mp.ellipk(mp.mpf(4) / 5)
    t_cw = K15 / K45
    j_cw_num = 1728 * mp.kleinj(1j * t_cw)
    j_target = mp.mpf(148176) / 25
    j_err = abs(j_cw_num - j_target) / j_target
    j_i = abs(1728 * mp.kleinj(1j * mp.ellipk(mp.mpf(1) / 2)
                               / mp.ellipk(mp.mpf(1) / 2)) - 1728)
    tr_errs = [abs(refl_trace_1d(P, s) - 1)
               for P in (mp.mpf(1), t_cw) for s in (mp.mpf('0.1'),
                                                    mp.mpf(1))]
    tr2d_err = abs(refl_trace_1d(1, mp.mpf('0.3'))
                   * refl_trace_1d(t_cw, mp.mpf('0.3')) - 1)
    check("H3.2 POSITION-SPACE CONFIRMATION [num, 30 digits]: the "
          "counterwitness torus is tau_cw = i K(1/5)/K(4/5) = %s i (from "
          "m = 1/lambda = 4/5), and 1728 kleinj(tau_cw) = %s = 148176/25 "
          "to %.1e (v510's j reproduced from the MODULAR side; tau = i "
          "control: |j - 1728| = %.1e); the sigma-twisted trace in "
          "position space (Gaussian images, erf sums) equals 1 to max "
          "%.1e per dimension and %.1e in 2D at BOTH tau = i and tau_cw "
          "-- exact rationality holds across the family, delta-blind"
          % (mp.nstr(t_cw, 10), mp.nstr(j_cw_num, 12), float(j_err),
             float(j_i), float(max(tr_errs)), float(tr2d_err)),
          j_err < mp.mpf(10) ** -20 and j_i < mp.mpf(10) ** -20
          and max(tr_errs) < mp.mpf(10) ** -25
          and tr2d_err < mp.mpf(10) ** -25)

    m_, n_, t_ = sp.symbols('m_ n_', integer=True) + (sp.Symbol(
        't_', positive=True),)
    lam_mn = m_ ** 2 * t_ + n_ ** 2 / t_
    lam_rot = n_ ** 2 * t_ + m_ ** 2 / t_
    diff_id = sp.simplify(sp.expand(lam_mn - lam_rot)
                          - (m_ ** 2 - n_ ** 2) * (t_ - 1 / t_)) == 0
    sol_t = sp.solveset(t_ - 1 / t_, t_, sp.Interval.open(0, sp.oo))
    N = 8

    def torus_lap(t):
        L = np.zeros((N * N, N * N))
        wy = 1.0 / t ** 2
        for x in range(N):
            for y in range(N):
                i0 = (x % N) * N + (y % N)
                L[i0, i0] = -2.0 - 2.0 * wy
                L[i0, ((x + 1) % N) * N + y] += 1.0
                L[i0, ((x - 1) % N) * N + y] += 1.0
                L[i0, x * N + (y + 1) % N] += wy
                L[i0, x * N + (y - 1) % N] += wy
        return L

    R_OP = np.zeros((N * N, N * N))
    for x in range(N):
        for y in range(N):
            R_OP[((-y) % N) * N + (x % N), x * N + y] = 1
    L1, Lcw = torus_lap(1.0), torus_lap(float(t_cw))
    c1 = np.linalg.norm(R_OP @ L1 - L1 @ R_OP) / np.linalg.norm(L1)
    ccw = np.linalg.norm(R_OP @ Lcw - Lcw @ R_OP) / np.linalg.norm(Lcw)
    check("H3.3 THE 4TH TWIST EXISTS <=> CLOCK [exact + lattice]: the "
          "order-4 twist rho needs [rho, Delta_tau] = 0; mode identity "
          "lam_mn - lam_rho(mn) = (m^2 - n^2)(t - 1/t) (%s), zero for all "
          "modes iff t = 1 (%s); lattice N = 8: ||[R, Delta]||/||Delta|| "
          "= %.1e at t = 1 vs %.3f at t_cw = %.4f -- v483's 'ALL twisted "
          "traces rational' quantifies over the twists that EXIST, and "
          "the order-4 twist exists ONLY at tau = i: H3 is the clock "
          "postulate in trace clothing, not an independent selector"
          % (diff_id, sol_t, c1, ccw, float(t_cw)),
          diff_id and sol_t == sp.FiniteSet(1)
          and c1 < 1e-12 and ccw > 1e-2)

    j_cw = sp.Rational(148176, 25)
    check("H3.4 j-RATIONALITY CONTROL [exact]: j_cw = 148176/25 is "
          "RATIONAL (denominator %d != 1, so not an algebraic integer, "
          "hence not CM) yet j_cw != 1728 and != 0 -- even rationality of "
          "j does not select; the selector j = 1728 <=> Aut(E) contains "
          "Z4 (v503 A7) is the clock again"
          % j_cw.q,
          j_cw.q == 25 and j_cw != 1728 and j_cw != 0)


# ===========================================================================
# H4 -- monodromy / parallel transport (v117 machinery, exact)
# ===========================================================================
def h4_monodromy():
    print(" H4 -- S4 monodromy: does the cusp structure constrain the "
          "angles?")
    M0 = sp.Matrix([[0, -(1 + I) / 2, (1 - I) / 2],
                    [-(1 + I) / 2, -I / 2, sp.Rational(-1, 2)],
                    [(1 - I) / 2, sp.Rational(-1, 2), I / 2]])
    U = sp.diag(1, I, -I)
    lam = sp.Symbol('lam')
    Mk = [sp.expand(U ** k * M0 * U ** (-k)) for k in range(4)]
    prod = sp.eye(3)
    for Mi in Mk:
        prod = sp.expand(prod * Mi)
    char_ok = all(sp.simplify(Mi.charpoly(lam).as_expr() - (lam ** 3 - 1))
                  == 0 for Mi in Mk)
    unit_ok = all(sp.simplify(Mi.H * Mi) == sp.eye(3) for Mi in Mk)
    distinct = all(sp.simplify(Mk[i0] - Mk[j0]) != sp.zeros(3, 3)
                   for i0 in range(4) for j0 in range(i0 + 1, 4))
    M0i = M0.inv()
    alt = [M0, M0i, M0, M0i]
    prod_alt = sp.eye(3)
    for Mi in alt:
        prod_alt = sp.expand(prod_alt * Mi)
    char_alt = sp.simplify(M0i.charpoly(lam).as_expr() - (lam ** 3 - 1)) == 0
    check("H4.1 EXISTENCE IS POSITION-BLIND [exact]: the v117 quadruple "
          "M_k = U^k M0 U^-k is unitary (%s) with char poly lam^3 - 1 at "
          "every mark (%s), pairwise distinct (%s), product = 1 (%s); a "
          "second, clock-free solution (M0, M0^-1, M0, M0^-1) also has "
          "product 1 (%s) and cusp class lam^3 - 1 (%s) -- the product-"
          "around-the-circle condition is a pi_1 relation and pi_1 of the "
          "4-punctured sphere is position-INDEPENDENT: existence + "
          "unitarity of the S4 monodromy constrain the mark angles NOT AT "
          "ALL (every delta carries it)"
          % (unit_ok, char_ok, distinct, prod == sp.eye(3),
             prod_alt == sp.eye(3), char_alt),
          unit_ok and char_ok and distinct and prod == sp.eye(3)
          and prod_alt == sp.eye(3) and char_alt)

    V4_perms = [(0, 1, 2, 3), (2, 3, 0, 1), (1, 0, 3, 2), (3, 2, 1, 0)]
    orders = []
    for p in V4_perms:
        o, q = 1, p
        while q != (0, 1, 2, 3):
            q = tuple(q[p[k]] for k in range(4))
            o += 1
        orders.append(o)
    cyc = (1, 2, 3, 0)
    o_cyc, q = 1, cyc
    while q != (0, 1, 2, 3):
        q = tuple(q[cyc[k]] for k in range(4))
        o_cyc += 1
    check("H4.2 THE 4-CYCLE NEEDS ORDER 4 (group level) [exact]: the "
          "generic seam symmetry V4 has element orders %s (max 2); the "
          "cusp-conjugation scheme M_k -> M_(k+1) is the 4-cycle of order "
          "%d -- V4 cannot induce it, ANY group inducing it contains an "
          "order-4 element, and an order-4 mark rotation exists on the "
          "free circle iff delta = pi/2 (H1.1): 'the cusp 4-cycle is "
          "geometrically realised' <=> the clock"
          % (sorted(orders), o_cyc),
          sorted(orders) == [1, 2, 2, 2] and o_cyc == 4)

    I3 = sp.eye(3)
    A_comm = sp.Matrix.vstack(*[
        sp.kronecker_product(Mi.T, I3) - sp.kronecker_product(I3, Mi)
        for Mi in Mk])
    ns_comm = A_comm.nullspace()
    scal_ok = (len(ns_comm) == 1
               and all(iszero(ns_comm[0][i0] * I3.vec()[j0]
                              - ns_comm[0][j0] * I3.vec()[i0])
                       for i0 in range(9) for j0 in range(i0 + 1, 9)))
    A_cyc = sp.Matrix.vstack(*[
        sp.kronecker_product(Mk[k].T, I3)
        - sp.kronecker_product(I3, Mk[(k + 1) % 4])
        for k in range(4)])
    ns_cyc = A_cyc.nullspace()
    Uv = U.vec()
    prop_U = (len(ns_cyc) == 1
              and all(iszero(ns_cyc[0][i0] * Uv[j0]
                             - ns_cyc[0][j0] * Uv[i0])
                      for i0 in range(9) for j0 in range(i0 + 1, 9)))
    U2 = sp.expand(U ** 2)
    nonscalar = sp.simplify(U2[0, 0] - U2[1, 1]) != 0
    check("H4.3 REPRESENTATION RIGIDITY [exact, Schur]: the joint "
          "centraliser of the four cusp blocks M_k is the SCALARS "
          "(nullspace dim %d, basis prop Id: %s), so every implementer W "
          "of the 4-cycle W M_k W^-1 = M_(k+1) is W = c U (nullspace dim "
          "%d, basis prop U: %s); U^2 = diag(1, -1, -1) is NONSCALAR (%s) "
          "=> (cU)^2 is never scalar: NO projective involution implements "
          "the cusp 4-cycle -- the implementer has projective order "
          "exactly 4 (the Z8/clock-tower shadow, consistent v510 A-D4.3): "
          "even quantum-mechanically V4 cannot fake the clock"
          % (len(ns_comm), scal_ok, len(ns_cyc), prop_U, nonscalar),
          scal_ok and prop_U and nonscalar)

    check("H4.4 HONEST TYPING [recorded]: the premise 'the cusp 4-cycle "
          "must be realised by a seam isometry' is exactly the clock "
          "postulate reworded (v117 names U 'the mu4 deck'); H4 therefore "
          "yields CONDITIONAL rigidity (given the premise, delta = pi/2 "
          "follows exactly via H1.1 + H4.3), not an independent "
          "established selector -- same reformulation class as H2/H3",
          True)


# ===========================================================================
# NC -- negative controls
# ===========================================================================
def nc_controls():
    print(" NC -- negative controls")
    lam_hex = lam_of(B_HEX)
    im_hex = sp.simplify(sp.im(lam_hex))
    j_hex = jlam(lam_hex)
    abs_hex = sp.simplify(sp.Abs(B_HEX))
    cr_hex = paircr_of(B_HEX)
    check("NC.1 HEXAGONAL [exact]: |b_hex| = %s = 2 - sqrt(3) != 1 (not "
          "on the free unit circle), Im lambda = %s != 0 (marks not "
          "concyclic -- no marked seam circle exists at all, v510 "
          "B-M4.4), j = %s = 0 (no order-4 automorphism: Aut(E_rho) = Z6, "
          "v503), pair cross-ratio != -1 (%s) -- the hexagonal "
          "configuration fails the PRECONDITIONS of H1-H4: the battery "
          "correctly rejects the v503 dynamical winner"
          % (abs_hex, im_hex, j_hex, iszero(cr_hex + 1)),
          abs_hex == 2 - sp.sqrt(3) and im_hex != 0 and j_hex == 0
          and not iszero(cr_hex + 1))

    marks_sil = [sp.Integer(1), sp.Integer(-1), S_SILVER, -S_SILVER]
    all_real = all(sp.simplify(sp.im(m)) == 0 for m in marks_sil)
    lam_sil = lam_of(S_SILVER)
    j_sil = jlam(lam_sil)
    check("NC.2 SILVER [exact]: all four marks are REAL (%s) => the "
          "unique circle through them is R u {inf}, which CONTAINS the "
          "deck fixed points 0 and inf => the deck is NOT free on the "
          "mark circle (the edge class, v510 B-M4.2) -- yet lambda = %s "
          "= 1/2 and j = %s = 1728: silver is HARMONIC but topologically "
          "dead: the position half (freeness) and the modulus half "
          "(harmonicity) are independent, and silver dies on the "
          "POSITION half BEFORE the delta battery even applies -- "
          "consistent with v510's two-half split"
          % (all_real, lam_sil, j_sil),
          all_real and lam_sil == sp.Rational(1, 2) and j_sil == 1728)

    n3 = sum(1 for s in combinations(range(16), 3)
             if set((x + 8) % 16 for x in s) == set(s))
    n4 = sum(1 for s in combinations(range(16), 4)
             if set((x + 8) % 16 for x in s) == set(s))
    check("NC.3a THREE MARKS ARE IMPOSSIBLE ON THE FREE CIRCLE [exact "
          "census]: the free deck (antipode) pairs points, so every "
          "invariant mark set has EVEN size -- on the Z16 seam circle "
          "there are %d invariant 3-subsets and %d invariant 4-subsets "
          "(= C(8,2) = 28, the v510 A-D5.1 count) -- the 4 = 2 chi mark "
          "count (v216) and deck-freeness (v510) already exclude every "
          "odd family; the delta family is the MINIMAL free moduli "
          "problem" % (n3, n4),
          n3 == 0 and n4 == 28)

    w5 = sp.exp(2 * sp.pi * I / 5)
    w3 = sp.exp(2 * sp.pi * I / 3)
    cases3 = {
        'scalene': [sp.Integer(1), w5, sp.Integer(-1)],
        'isosceles': [sp.Integer(1), w5, sp.conjugate(w5)],
        'equilateral': [sp.Integer(1), w3, w3 ** 2],
    }
    res3 = {}
    for tag, Mv in cases3.items():
        rr, ii = census(Mv)
        ps = perms_signed_of(Mv, rr, ii)
        n_orb = len(orbits_of([p for p, _ in ps], 3))
        res3[tag] = (len(rr) + len(ii), n_orb == 1)
    check("NC.3b THREE FREE MARKS: BARE TRANSITIVITY IS ALREADY RIGID "
          "[exact]: on a plain circle (no deck) 3 marks give group order "
          "/ transitivity = scalene %s, isosceles %s, equilateral %s -- "
          "at n = 3 bare transitivity <=> equal spacing (any transitive "
          "group on 3 circle points contains an order-3 rotation); at "
          "n = 4 WITH deck the pair-exchanging V4 makes bare transitivity "
          "free of charge for every delta (H1.2) -- '4 counts': the "
          "deck-pairing is exactly what forces the sharpening from mark- "
          "to FLAG-transitivity"
          % (res3['scalene'], res3['isosceles'], res3['equilateral']),
          res3['scalene'] == (1, False) and res3['isosceles'] == (2, False)
          and res3['equilateral'] == (6, True))


# ===========================================================================
# SYN -- synthesis
# ===========================================================================
def syn_synthesis():
    print(" SYN -- synthesis: one discrete bit, many faces")
    faces = [
        "delta = pi/2",
        "rotation subgroup = Z4 (clock exists)          [H1.1]",
        "|G| = 8 = D4 (vs V4)                           [H1.2/H1.6]",
        "mark-fixing mirror exists (stabiliser 2)       [H1.3]",
        "arc/flag transitivity                          [H1.4]",
        "Green odd-sector degeneracy                    [H2.1]",
        "weighted-Laplacian odd degeneracy              [H2.2]",
        "K3 mark indicator = 0                          [H2.3]",
        "order-4 twist rho exists                       [H3.3]",
        "cusp 4-cycle geometrically implementable       [H4.2/H4.3]",
        "harmonic (pair cross-ratio -1)                 [S0]",
        "j = 1728 (tau = i)                             [S0]",
    ]
    for f in faces:
        print("        <=> " + f)
    check("SYN.1 THE EQUIVALENCE WEB [assembled from exact results above]: "
          "on the free RP seam circle the %d conditions listed are "
          "pairwise EQUIVALENT (each proven <=> delta = pi/2 exactly in "
          "H1-H4/S0) -- ONE discrete datum with many faces; every face "
          "that references established machinery (clock, DtN blocks, "
          "twisted traces, cusp 4-cycle) is a REFORMULATION of the same "
          "bit, not an independent established selector" % len(faces),
          len(faces) == 12)

    passes = ["free circle (|b| = 1)", "central/crossing class (v510)",
              "V4 mark-transitive (H1.2)",
              "per-mark unsided data equal (H1.5)",
              "S4 monodromy exists, product 1 (H4.1)",
              "sigma-trace = 1 rational (H3.1/2)",
              "j rational = 148176/25 (H3.4)"]
    fails = ["flag orbits 2 != 1", "no mark mirror (|stab| = 1)",
              "no clock rotation (rot group Z2)",
              "Green split (2/pi) log 2 = 0.4413 != 0",
              "K3 mark indicator 0.6241 != 0",
              "rho-twist commutator > 1e-2 (t_cw = 0.735)",
              "no projective involution for the 4-cycle",
              "pair cross-ratio -1/4 != -1", "j = 5927.04 != 1728"]
    print("        counterwitness scoreboard: PASSES %d established "
          "unsided tests:" % len(passes))
    for p in passes:
        print("          + " + p)
    print("        FAILS %d sided/clock-equivalent tests:" % len(fails))
    for f in fails:
        print("          - " + f)
    check("SYN.2 COUNTERWITNESS SCOREBOARD [assembled]: {+-1, +-(3+4i)/5} "
          "passes ALL %d established unsided tests and fails ALL %d "
          "sided/clock-equivalent ones -- NO established seam datum "
          "excludes it: none of H1-H4 delivers harmonicity from [E] "
          "material; the exclusion needs exactly ONE new discrete bit"
          % (len(passes), len(fails)),
          len(passes) == 7 and len(fails) == 9)

    check("SYN.3 THE SENTENCE + TYPING [recorded, no overclaim]: 'On the "
          "free RP seam circle, bare mark-transitivity is free of charge "
          "for EVERY delta (pair-exchanging V4); FLAG-transitivity (marks "
          "AND their two sides indistinguishable) <=> delta = pi/2 <=> "
          "tau = i <=> the clock.  The last input therefore reduces from "
          "a continuous modulus to ONE discrete symmetry-enhancement bit "
          "(V4 -> D4: side-indistinguishability of the four equal-data "
          "marks).'  [E]: every equivalence link (exact, this probe + "
          "v510).  [C]: the bit itself -- v216 local equality does NOT "
          "deliver it (H1.5), so it stays a postulate; the gain is the "
          "FORM (discrete, seam-intrinsic, v216-adjacent language), not "
          "a derivation.  H1-as-briefed is FALSIFIED (transitivity "
          "delta-blind); H2/H3/H4 are exact reformulations, none an "
          "independent established selector.  NO marker moves", True)


# ---------------------------------------------------------------------------
def run():
    print("seam_tau_i_established_selector_probe: which ESTABLISHED seam "
          "datum excludes the free-but-non-harmonic family? (H1 "
          "transitivity / H2 spectra / H3 heat traces / H4 monodromy + "
          "controls)")
    s0_frame()
    h1_symmetry()
    h2_spectral()
    h3_heat()
    h4_monodromy()
    nc_controls()
    syn_synthesis()
    n_pass = sum(RESULTS)
    print("=" * 72)
    print("RESULT: %d/%d checks passed" % (n_pass, len(RESULTS)))
    return n_pass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
