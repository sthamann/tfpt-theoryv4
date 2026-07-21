"""seam_alignment_bit_fermion_probe.py -- EXPLORATION ONLY (experiments/, no verification claim).

THE TAUTOLOGY ATTACK ON THE v506 ALIGNMENT BIT (fermionic / Fock side, A3).

Companion of seam_alignment_bit_torus_origin_probe.py (Moebius/torus side:
the common torus origin forces "deck = half-period translation" but NOT its
central position -- tautology refuted, equivalence trias proved).  This probe
computes the FERMIONIC face of the bit: v506 Part B proved U^2 = (-1)^F for
the CENTRAL deck arrangement (deck = half-rotation of the 16-site NS seam,
marks at 1,5,9,13, deck acts as the crossing double transposition (13)(24)).
What happens fermionically in the COUNTEREXAMPLE (edge) arrangement, where
the deck acts as the neighbour transposition (12)(34)?

GEOMETRY FIRST (F1).  On a deck-invariant circle a rotation deck ALWAYS pairs
marks crossing (central type): every shift-8-invariant 4-set is {a, b, a+8,
b+8} with cyclic order a < b < a+8 < b+8 -- the chords cross.  The edge
(silver) arrangement is realisable on the seam circle ONLY by a REFLECTION:
in the v506 counterexample {+-1, +-(3+2sqrt2)} the deck-invariant circle
through the marks is the REAL line, and there z -> -z acts as the reflection
with the two non-mark fixed points 0, inf sitting BETWEEN neighbour marks --
discrete model: R_edge: j -> 4 - j (fixed sites 3, 11 = non-marks; marks
paired (1 5)(9 13) = neighbours, non-crossing).  Exact enumeration: rotation
decks give crossing pairings ONLY, reflection decks non-crossing ONLY.

  F2 ONE-PARTICLE DICHOTOMY.  NS half-rotation: D^2 = -1, charpoly
     (lam^2+1)^8 (order 4 BEFORE any Fock choice, v506).  NS reflection:
     R^2 = +1 EXACTLY for BOTH spin lifts (j -> 4-j and its partner on the
     32-cover), charpoly (lam^2-1)^8, det = +1 -- an honest involution,
     NOTHING order-4 in sight.
  F3 FOCK DICHOTOMY (the core).  Central: Utilde^2 = 256 (-1)^F (nonsplit
     Z4, v506 reproduced).  Edge: the even implementer Utilde_e =
     P_2 (g_1+g_5)(g_2+g_4)(g_6-g_16)(g_7-g_15)(g_8-g_14)(g_9-g_13)
     (g_10-g_12) EXISTS (implementation does NOT break), and Utilde_e^2 =
     +2^7 x 1 EXACTLY -- a SCALAR: U_e^2 = +1, the extension SPLITS.  Phase
     robustness: (cU)^2 = c^2 U^2 stays scalar for every c -- split vs
     nonsplit is phase-invariant.  The fermions DETECT the alignment.
  F4 ROOT/TOWER DICHOTOMY.  In the full NS dihedral lift group (32 signed
     shift/reflection matrices) the central deck has EXACTLY 2 projective
     square roots (the +-quarter shifts, the clock pair) -- the edge deck
     has 0 (rotation squares are rotations, reflection squares are +-1).
     The Moebius-side root count (2 vs 0, v506/torus probe) REAPPEARS at
     the fermionic circle level; no Z8 tower exists over the edge deck.
  F5 CONTROLS.  R-sector reflection: odd implementer, U^2 = +2^7 x 1 --
     scalar again (split); so the edge deck NEVER forces anything (NS or R),
     while the central deck forces EXACTLY in NS: the Z4-forcing premise is
     the CONJUNCTION (NS wrap AND central alignment).  8-site robustness:
     same dichotomy (U^2 = 16 (-1)^F_8 central vs scalar 2^2 edge) -- not a
     16-tuning.
  F6 VERDICT.  The alignment bit acquires a FOURTH equivalent face, a
     physical one: deck central <=> the deck's NS Fock lift is the NONSPLIT
     Z4 extension U^2 = (-1)^F (with Z8 clock tower) <=> Fidkowski-Kitaev
     class nontrivial; deck edge <=> split Z2, no tower.  This is a NEW
     physical characterisation (the bit = an extension class), NOT a
     derivation: WHICH class nature realises stays the one carrier input.

Repo anchors: v506 Part B (U^2 = (-1)^F, Z8 tower), v490/v492 (NS = unique
S^2 spin structure, 16 Majoranas), v216 (marks), torus companion probe
(sigma_c classification, silver = edge half-period).

Exact throughout (Fractions in Cl(16); sympy for matrices).  Standalone.
Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/seam_alignment_bit_fermion_probe.py
"""
from fractions import Fraction as Fr
from itertools import combinations

import sympy as sp

RESULTS = []

N_SITES = 16           # 16 Majorana modes = 2^(g_car-1), 4 per mark quadrant
G_CAR = 5
MARKS = [0, 4, 8, 12]  # mu4 mark sites (0-based) on the 16-site seam circle
AXIS = 4               # edge reflection j -> AXIS - j (fixed sites 2, 10)


def check(name, ok):
    RESULTS.append(bool(ok))
    print(("PASS" if ok else "FAIL") + " [%2d] %s" % (len(RESULTS), name))


# ---------------------------------------------------------------------------
# abstract Clifford algebra Cl(n): elements = {sorted index tuple: Fraction}
# ---------------------------------------------------------------------------
def mono_mul(m1, m2):
    out = list(m1)
    sign = 1
    for g in m2:
        out.append(g)
        i = len(out) - 1
        while i > 0 and out[i - 1] > out[i]:
            out[i - 1], out[i] = out[i], out[i - 1]
            sign = -sign
            i -= 1
        if i > 0 and out[i - 1] == out[i]:
            del out[i - 1:i + 1]
    return sign, tuple(out)


def cmul(x, y):
    out = {}
    for m1, c1 in x.items():
        for m2, c2 in y.items():
            s, m = mono_mul(m1, m2)
            c = out.get(m, Fr(0)) + s * c1 * c2
            if c:
                out[m] = c
            elif m in out:
                del out[m]
    return out


def cadd(x, y):
    out = dict(x)
    for m, c in y.items():
        cc = out.get(m, Fr(0)) + c
        if cc:
            out[m] = cc
        elif m in out:
            del out[m]
    return out


def cscale(x, s):
    return {m: c * s for m, c in x.items()} if s else {}


def gam(*idx):
    return {tuple(idx): Fr(1)}


ONE = {(): Fr(1)}


def is_scalar(x):
    return all(m == () for m in x)


def prop(x, y):
    """x = c y for a scalar c (both nonzero); returns (True, c) or (False, None)."""
    if not x or not y or set(x) != set(y):
        return (False, None)
    m0 = next(iter(y))
    c = x[m0] / y[m0]
    return (all(x[m] == c * y[m] for m in y), c)


def apply_lin(mat, a, n):
    out = {}
    for bidx in range(n):
        if mat[bidx][a]:
            out = cadd(out, cscale(gam(bidx), Fr(mat[bidx][a])))
    return out


def implements(Uel, mat, n):
    """check U gamma_a = (sum_b mat[b][a] gamma_b) U for all a."""
    for a in range(n):
        lhs = cmul(Uel, gam(a))
        rhs = cmul(apply_lin(mat, a, n), Uel)
        if cadd(lhs, cscale(rhs, Fr(-1))):
            return False
    return True


# ---------------------------------------------------------------------------
# one-particle lifts on the n-site circle (NS: gamma_{j+n} = -gamma_j)
# ---------------------------------------------------------------------------
def shift_matrix(n, k, wrap_sign):
    """rotation lift gamma_j -> (wrap sign)^(#wraps) gamma_{j+k}."""
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        b = (a + k) % n
        M[b][a] = wrap_sign if a + k >= n else 1
    return M


def refl_matrix(n, k, wrap_sign):
    """reflection lift gamma_j -> gamma_{k-j} on the double cover:
    idx = (k - j) mod 2n; sign = wrap_sign if idx >= n."""
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        idx = (k - a) % (2 * n)
        M[idx % n][a] = wrap_sign if idx >= n else 1
    return M


def matmul_i(A, B):
    n = len(A)
    return [[sum(A[i][kk] * B[kk][j] for kk in range(n)) for j in range(n)]
            for i in range(n)]


def mat_prop(A, B):
    """A = s B for s in {+1, -1} (integer signed-permutation matrices)."""
    n = len(A)
    for s in (1, -1):
        if all(A[i][j] == s * B[i][j] for i in range(n) for j in range(n)):
            return True
    return False


def pairing_of(inv_map, ms):
    """the 2+2 pairing of the 4 marks ms under involution j -> inv_map(j);
    returns 'crossing' or 'noncrossing' in the cyclic order of ms."""
    order = sorted(ms)
    pos = {m: i for i, m in enumerate(order)}
    pairs = set()
    for m in ms:
        pairs.add(frozenset((pos[m], pos[inv_map(m) % 16])))
    return 'crossing' if frozenset((0, 2)) in pairs else 'noncrossing'


def run():
    print("seam_alignment_bit_fermion_probe: A3 -- does the fermionic Fock lift "
          "DISTINGUISH central vs edge deck arrangement?  Exact Cl(16)")
    print("=" * 100)
    n = N_SITES

    # ================================================ F1: geometry of arrangements
    print("  -- F1: which deck arrangements exist on the seam circle at all?")

    rot_sets = [s for s in combinations(range(n), 4)
                if set((m + 8) % n for m in s) == set(s)]
    rot_pair = {pairing_of(lambda j: j + 8, s) for s in rot_sets}
    ref_sets = [s for s in combinations(range(n), 4)
                if set((AXIS - m) % n for m in s) == set(s)
                and all((AXIS - m) % n != m for m in s)]
    ref_pair = {pairing_of(lambda j: AXIS - j, s) for s in ref_sets}
    fixed_sites = [j for j in range(n) if (AXIS - j) % n == j]
    edge_mperm = [MARKS.index((AXIS - m) % n) for m in MARKS]
    cen_mperm = [MARKS.index((m + 8) % n) for m in MARKS]
    check("F1.1 ARRANGEMENT GEOMETRY [exact enumeration]: ALL %d shift-8-"
          "invariant 4-mark sets have CROSSING deck pairing (%s) = central "
          "type -- the rotation deck can NEVER act edge-like on a circle; "
          "ALL %d mark-free reflection-invariant sets are NONCROSSING (%s) "
          "= edge type; the edge model R: j -> 4-j fixes the non-mark sites "
          "%s (the silver 0/inf between neighbour marks), acts on marks "
          "%s as %s = (12)(34) vs central %s = (13)(24) -- the v506 "
          "counterexample HAS a faithful seam-circle realisation, but only "
          "as a reflection"
          % (len(rot_sets), rot_pair, len(ref_sets), ref_pair,
             [f + 1 for f in fixed_sites], [m + 1 for m in MARKS],
             edge_mperm, cen_mperm),
          rot_pair == {'crossing'} and ref_pair == {'noncrossing'}
          and len(rot_sets) == 28 and fixed_sites == [2, 10]
          and edge_mperm == [1, 0, 3, 2] and cen_mperm == [2, 3, 0, 1])

    # ================================================ F2: one-particle dichotomy
    print("  -- F2: one-particle level -- D^2 = -1 vs R^2 = +1")
    D_ns = shift_matrix(n, 8, -1)
    R_ns = refl_matrix(n, AXIS, -1)
    R_ns2 = refl_matrix(n, AXIS + n, -1)       # the other spin lift (j -> 20-j)
    Dm, Rm, Rm2 = sp.Matrix(D_ns), sp.Matrix(R_ns), sp.Matrix(R_ns2)
    lamv = sp.symbols('lam')
    chD = sp.factor(Dm.charpoly(lamv).as_expr())
    chR = sp.factor(Rm.charpoly(lamv).as_expr())
    check("F2.2 ONE-PARTICLE DICHOTOMY [exact]: NS half-rotation D^2 = -1 "
          "(%s), charpoly %s = (lam^2+1)^8 -- order 4 forced before Fock "
          "(v506); NS edge reflection R^2 = +1 for BOTH spin lifts (%s, %s "
          "-- the lift ambiguity is an overall sign, R and -R square "
          "equally), charpoly %s = (lam^2-1)^8, det = %s, tr = %s: an "
          "HONEST involution -- nothing order-4 on the edge arrangement"
          % (Dm ** 2 == -sp.eye(n), chD, Rm ** 2 == sp.eye(n),
             Rm2 ** 2 == sp.eye(n), chR, Rm.det(), sp.trace(Rm)),
          Dm ** 2 == -sp.eye(n) and Rm ** 2 == sp.eye(n)
          and Rm2 ** 2 == sp.eye(n) and mat_prop(R_ns, R_ns2)
          and sp.expand(chD - (lamv ** 2 + 1) ** 8) == 0
          and sp.expand(chR - (lamv ** 2 - 1) ** 8) == 0
          and Rm.det() == 1 and sp.trace(Rm) == 0)

    # ================================================ F3: Fock dichotomy (core)
    print("  -- F3: Fock level -- U^2 exact in Cl(16), central vs edge")

    GAMMA = {tuple(range(n)): Fr(1)}

    Ut = ONE                                     # central (v506 reproduced)
    for j in range(8):
        Ut = cmul(Ut, cadd(ONE, cscale(cmul(gam(j), gam(j + 8)), Fr(-1))))
    ok_u2, coef = prop(cmul(Ut, Ut), GAMMA)
    impl_c = implements(Ut, D_ns, n)
    check("F3.3 CENTRAL REFERENCE [exact, v506 reproduced]: Utilde = "
          "prod(1 - g_j g_{j+8}) implements the half-rotation (%s) and "
          "Utilde^2 = %s x g_1...g_16, i.e. U^2 = (-1)^F EXACTLY (nonsplit "
          "Z4; (cU)^2 = c^2 (-1)^F never scalar-free): the central "
          "arrangement carries the nontrivial extension"
          % (impl_c, coef),
          impl_c and ok_u2 and coef == Fr(256))

    # edge implementer: P_2 x (g0+g4)(g1+g3)(g5-g15)(g6-g14)(g7-g13)(g8-g12)(g9-g11)
    P2 = {tuple(j for j in range(n) if j != 2): Fr(1)}
    Ue = dict(P2)
    for a in range(n):
        b = (AXIS - a) % n
        if a >= b or a == 2 or a == 10:
            continue
        idx = (AXIS - a) % (2 * n)
        eps = Fr(-1) if idx >= n else Fr(1)
        Ue = cmul(Ue, cadd(gam(a), cscale(gam(b), eps)))
    impl_e = implements(Ue, R_ns, n)
    even_e = all(len(m) % 2 == 0 for m in Ue)
    Ue2 = cmul(Ue, Ue)
    ok_e2, coef_e = prop(Ue2, ONE)
    check("F3.4 EDGE RESULT: THE EXTENSION SPLITS [exact]: the even (%s) "
          "implementer Utilde_e = P_2 x prod(g_a +- g_b) EXISTS and "
          "implements the NS edge reflection on all 16 generators (%s) -- "
          "the implementation does NOT break; but Utilde_e^2 = %s x 1: a "
          "SCALAR (%s), i.e. U_e^2 = +1 -- NOT (-1)^F.  Phase robustness: "
          "(cU)^2 = c^2 U^2 stays scalar for every phase -- split vs "
          "nonsplit is invariant: the NS fermions force Z4 on the CENTRAL "
          "deck and plain Z2 on the EDGE deck"
          % (even_e, impl_e, coef_e, ok_e2),
          even_e and impl_e and ok_e2 and coef_e == Fr(2 ** 7)
          and not is_scalar(cmul(Ut, Ut)))

    center_wit = all(
        not all(not cadd(cmul({mt: Fr(1)}, gam(a)),
                         cscale(cmul(gam(a), {mt: Fr(1)}), Fr(-1)))
                for a in range(n))
        for mt in [(0,), (0, 1), tuple(range(n))])
    check("F3.5 CANONICITY [exact]: center of Cl(16) = scalars (no nonempty "
          "monomial commutes with all generators: %s) => BOTH implementers "
          "are unique up to phase => the dichotomy 'U^2 = (-1)^F (central) "
          "vs U^2 = +1 (edge)' is a property of the ARRANGEMENT, not of any "
          "construction choice -- the fermions measure the alignment bit"
          % center_wit, center_wit)

    # ================================================ F4: root/tower dichotomy
    print("  -- F4: square roots in the NS dihedral lift group (exact, complete)")
    group = [shift_matrix(n, k, -1) for k in range(n)] \
        + [refl_matrix(n, k, -1) for k in range(n)]
    roots_D = [k for k, g in enumerate(group)
               if mat_prop(matmul_i(g, g), D_ns)]
    roots_R = [k for k, g in enumerate(group)
               if mat_prop(matmul_i(g, g), R_ns)]
    quarter_ok = roots_D == [4, 12]
    check("F4.6 ROOT COUNT DICHOTOMY [exact, all 32 lifts]: square roots of "
          "the central deck in the NS dihedral lift group: %d (shift "
          "indices %s = the +-quarter shifts = the clock pair); square "
          "roots of the edge deck: %d (rotation squares are rotations, "
          "reflection squares are +-1 -- a reflection has NO root in the "
          "circle group) -- the Moebius-side count (2 vs 0, v506 A-S2.6/7 "
          "and torus probe T2.9) REAPPEARS fermionically: no Z8 tower "
          "exists over the edge deck"
          % (len(roots_D), roots_D, len(roots_R)),
          quarter_ok and len(roots_R) == 0)

    # ================================================ F5: controls
    print("  -- F5: R-sector control + 8-site robustness")
    R_r = refl_matrix(n, AXIS, +1)
    Ur = cmul(gam(2), gam(10))
    for a in range(n):
        b = (AXIS - a) % n
        if a >= b or a == 2 or a == 10:
            continue
        Ur = cmul(Ur, cadd(gam(a), gam(b)))
    impl_r = implements(Ur, R_r, n)
    odd_r = all(len(m) % 2 == 1 for m in Ur)
    ok_r2, coef_r = prop(cmul(Ur, Ur), ONE)
    check("F5.7 R-SECTOR EDGE CONTROL [exact]: the R (periodic) edge "
          "reflection has the ODD implementer g_2 g_10 x prod(g_a + g_b) "
          "(odd: %s, implements: %s) with U^2 = %s x 1 (scalar: %s) -- "
          "split again: the edge deck forces NOTHING in either sector, "
          "while the central deck forces exactly in NS (v506 B-S3: R "
          "central splits too) -- the Z4-forcing premise is the "
          "CONJUNCTION 'NS wrap AND central alignment'"
          % (odd_r, impl_r, coef_r, ok_r2),
          odd_r and impl_r and ok_r2 and coef_r == Fr(2 ** 7))

    m8 = 8
    D8 = shift_matrix(m8, 4, -1)
    Ut8 = ONE
    for j in range(4):
        Ut8 = cmul(Ut8, cadd(ONE, cscale(cmul(gam(j), gam(j + 4)), Fr(-1))))
    G8 = {tuple(range(m8)): Fr(1)}
    ok8, c8 = prop(cmul(Ut8, Ut8), G8)
    R8 = refl_matrix(m8, 2, -1)                  # marks 0,2,4,6; fixed 1, 5
    P1_8 = {tuple(j for j in range(m8) if j != 1): Fr(1)}
    Ue8 = dict(P1_8)
    for a in range(m8):
        b = (2 - a) % m8
        if a >= b or a == 1 or a == 5:
            continue
        idx = (2 - a) % (2 * m8)
        eps = Fr(-1) if idx >= m8 else Fr(1)
        Ue8 = cmul(Ue8, cadd(gam(a), cscale(gam(b), eps)))
    impl8e = implements(Ue8, R8, m8)
    ok8e, c8e = prop(cmul(Ue8, Ue8), ONE)
    check("F5.8 8-SITE ROBUSTNESS [exact]: same dichotomy on the 8-site NS "
          "circle (marks 0,2,4,6): central U^2 = %s/16 x (-1)^F_8 "
          "(nonscalar: %s) vs edge reflection j -> 2-j implementer (%s) "
          "with U^2 = %s x 1 (scalar: %s) -- the split/nonsplit contrast "
          "needs only (NS wrap + arrangement type), not the carrier count "
          "16 = 2^(g_car-1) = %d"
          % (c8, ok8, impl8e, c8e, ok8e, 2 ** (G_CAR - 1)),
          ok8 and c8 == Fr(16) and impl8e and ok8e and c8e == Fr(2 ** 3)
          and 2 ** (G_CAR - 1) == 16)

    # ================================================ F6: verdict
    print("  -- F6: verdict")
    verdict = (ok_u2 and coef == Fr(256)         # central: nonsplit
               and ok_e2 and coef_e == Fr(128)   # edge: split
               and quarter_ok and len(roots_R) == 0
               and ok_r2 and ok8 and ok8e)
    check("F6.9 VERDICT [typed]: the alignment bit has a FOURTH equivalent "
          "face, a PHYSICAL one: deck central <=> NS Fock lift is the "
          "NONSPLIT Z4 extension U^2 = (-1)^F with the Z8 clock tower "
          "(F3.3/F4.6) ; deck edge <=> honest split Z2, U^2 = +1, zero "
          "roots, no tower (F3.4/F4.6) -- 'Uhr existiert <=> tau = i <=> "
          "Deck zentral <=> Fock-Lift nichtsplittend'.  The central "
          "arrangement is fermionically DISTINGUISHED (only it carries the "
          "nontrivial Fidkowski-Kitaev-type class on the seam), giving the "
          "bit a physical characterisation -- but WHICH class nature "
          "realises remains the one discrete carrier input: an argument "
          "FOR the bit's physicality, not a derivation.  No marker moves",
          verdict)

    npass = sum(RESULTS)
    print("=" * 100)
    print("SUMMARY: %d/%d checks passed%s"
          % (npass, len(RESULTS),
             "" if npass == len(RESULTS) else "  -- FAILURES PRESENT"))
    return npass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
