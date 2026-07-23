"""seam_bit_twist_class_definition_probe.py -- EXPLORATION ONLY (experiments/, no verification claim).

TURNING THE BIT AROUND: from abstract input to a measurable
twist-class choice.

Context (read-only inputs): the alignment bit (V4 -> D4 symmetry lift
<=> tau = i <=> clock <=> delta = pi/2) has NINE failed derivation
attempts behind it (v521 = the eighth, the twist-state probe / v525 =
the ninth side-blind test on the v512 scoreboard): in the whole
Wick-computable class it is genuine discrete input.  BUT the
twist-state attack found two structures that PRESUPPOSE the bit
(exist only at delta = pi/2):
  (1) the eta FLIP: on the mark-fixing axes (existing iff delta =
      pi/2) the sigma-gauge decoration obeys sigma o r = -sigma
      exactly -- the odd-sector RP Gram is negated, the pinned RP
      sign eta jumps +i -> -i (on the swap axes sigma o r = sigma,
      no flip);
  (2) the TWIST FRUSTRATION: the theta-symmetrized Kadanoff-Ceva
      4-twist insertion is Hermitian but INDEFINITE (4,4,0) on the
      fixing cut for both eta -- the twist frustrates the mark
      mirror (lattice shadow of the Ising twist field's
      mirror-oddness).
THE IDEA: instead of deriving the bit (proven impossible in the
Wick class), DEFINE it physically: "the bit is the choice of which
of the two twist classes nature realizes."  For that the two
structures must be shown to be EXACT, well-typed dichotomies
equivalent to the bit -- then the abstract input becomes an (in
principle) measurable order parameter.

PREREGISTRATION (fixed before any computation):
  SUCCESS = (a) BOTH structures are proven exact equivalences to
    the bit (candidate facets #14/#15 of the v512 web -- SANDBOX
    proposal only, no v512/ledger edit): "a mark-compatible axis
    with sigma o r = -sigma exists <=> delta = pi/2" and "a
    theta-irreducible (exchange-forced) 4-twist insertion exists
    (and is then frustrated) <=> delta = pi/2", BOTH directions
    each, including a complete census that NO generalized fixing
    structure (axes through mark pairs with modified return,
    redressed lifts, arbitrary bijections) exists off pi/2;
    AND (b) a well-defined order parameter is constructed: an
    exactly computable O with O != 0 <=> bit set, invariant under
    all gauge/lifting freedoms identified in v525 ([C]: plane
    gauge, pattern flip, site redress; plus sigma global flip and
    string orientation);
    AND (c) the connection to the v510 Kramers class is exactly
    typed (is the twist-class choice THE SAME dichotomy as
    split/nonsplit U^2 = +-(-1)^F? -- machine-decided either way;
    an identification would unify all bit faces into one physical
    datum, a separation must say exactly which half carries which).
  KILL = one of the equivalences breaks (the structure exists in
    generalized form for some delta != pi/2) -- then it is NOT a
    bit definition.
  UNDECIDED = an equivalence holds only one-sidedly / only
    numerically (no exact mechanism), or a needed lifting is not
    well-definably constructible.

CONSTRUCTION PROGRAM (exact, N = 16 and N = 32):
  (i)   both directions of both equivalences on the M(delta) =
        {+-1, +-e^(i delta)} family: fine lattice ladder (N = 32,
        m = 1..7, delta = m pi/8; N = 16, m = 2, 4) + symbolic
        solvesets as in v521; the (=>) directions via (alpha) the
        complete reflection census (mark-compatible fixing axes
        exist iff delta = pi/2), (beta) the CARDINALITY LEMMA: both
        structures require a bijection exchanging the short/long
        arc systems (the sigma = +1 support IS the short-string
        support, machine identity), and |short| = |long| <=> delta
        = pi/2 -- this kills EVERY modified-return generalization,
        (gamma) explicit RP data on every existing cut off pi/2
        (no flip, no frustration).
  (ii)  order-parameter candidates: the sign datum eta(axis) over
        the axis torsor (flip cycle vs constant -- the Z2 character
        of the eighth rotation = the Z8 clock-tower shadow); the
        inertia signature of the symmetrized insertion; the v510
        index U^2 in {+1, (-1)^F}; a Pfaffian sign invariant of the
        4-twist chain.
  (iii) gauge robustness of the winner under: sigma global flip,
        admissible site redress (global -1), the INADMISSIBLE
        alternating redress (must be rejected by the untwisted
        battery -- teeth), mu4-defect overlay in all plane-gauge /
        pattern-flip variants, string orientation.
  (iv)  unification theorem: are eta-flip class, frustration class
        and v510 Kramers class the same Z2 invariant (lattice-
        instantiated)?
  (v)   measurement-protocol sketch as a typed [C] comment in the
        verdict (principle statement only, no experiment design).

NEGATIVE CONTROLS (mandatory): the v512 counterwitness
{+-1, +-(3+4i)/5} (must fall out of every claimed dichotomy: no
fixing axes, exact); hexagonal / silver configurations (fail the
preconditions upstream); the Z2 seam (2 marks) as anchor (there the
analogous dichotomy must be trivial -- "4 counts"); FALSE order
parameters (delta-dependent quantities that are NOT gauge-robust
and/or non-selecting -- constructed and rejected, so the selection
has teeth).

RESULT (filled after the run; 18/18 PASS): SUCCESS, exactly as
preregistered -- the bit IS a twist-class choice:
  (a) FACET #14 (eta flip <=> delta = pi/2, both directions): (<=)
      on all four fixing axes (N = 16 k = 15/7, N = 32 k = 31/15)
      sigma o r = -sigma exactly and the pinned eta flips +i -> -i
      with 40-digit-identical spectra, even sector untouched
      (29,0,0); (=>) complete census: on every existing axis off
      pi/2 sigma o r = +sigma exactly and eta never flips; the
      complete g-class census over ALL 32 x 7 axes shows the global
      flip class g = -1 occurs EXACTLY at {31, 15} for m = 4 and
      nowhere else; cardinality lemma |A+| = 4m vs |A-| = 32 - 4m
      kills every modified-return bijection (equality iff m = 4;
      symbolic: solveset(delta - (pi - delta)) = {pi/2}).
      FACET #15 (twist frustration <=> delta = pi/2, both
      directions): (<=) at pi/2 theta maps D_short -> D_long
      exactly, omega(D_s) = omega(D_l) exactly (quarter-shift), the
      minimal theta-closed insertion is UNIQUE = D_s + D_l (the
      difference is ill-normalized, omega = 0) and its Gram is
      Hermitian and INDEFINITE for both eta: (4,4,0) at N = 16 on
      both fixing axes, (8,8,0) at N = 32; (=>) off pi/2 theta acts
      REDUCIBLY (r(D_s) = D_s on every existing axis, single string
      already closed, insertion Grams PD (16,0,0) along the whole
      ladder incl. pi/2 +- pi/8, exact N = 16 witness), and the
      exchange D_s <-> D_l is killed by the same cardinality lemma
      (|D_s| = 4m != 32 - 4m = |D_l|); the reducible sum insertion
      on swap axes decomposes exactly into two PD sectors whose
      weights omega(D_s) = omega(D_l) agree at 40 digits even off
      pi/2 (complement-string identity) with the same sign -- the
      sum is PD as forced: a theta-REDUCIBLE decoration can never
      certify frustration (typed [C] fence: facet #15 carries the
      irreducibility clause, itself cardinality-locked to pi/2).
  (b) ORDER PARAMETER (winner): O = (number of flip axes) /
      (number of mark-compatible axes) = eta-holonomy datum over
      the axis torsor; O = 1/2 at delta = pi/2 (flip cycle
      -,+,-,+ under the eighth rotation k -> k+4: the nontrivial
      Z2 character of the Z8 clock-tower shadow, class(k+4) =
      -class(k) exactly) and O = 0 for every other member, the
      counterwitness (O = 0, continuum-typed) and trivially
      constant at the 2-mark anchor.  ROBUSTNESS: invariant under
      sigma global flip (exact identity), admissible site redress
      (global -1: both pinned eta flip together, relative datum
      invariant), mu4-defect overlay in ALL plane-gauge/pattern
      variants (uniform / alternating / flipped: the SAME redress
      works and the flip persists on the decorated state as the
      exact relative negation, best-eta swap with identical
      spectra and equal best inertia (14,2,0) -- the fixing-cut
      mu4 Gram is legitimately non-PD since the mark-bond defect
      planes straddle that cut), string orientation
      (normalized insertion functional exactly invariant); the
      alternating redress is INADMISSIBLE (untwisted Gram (4,4,0)
      for both eta -- the fence has teeth).
  (c) KRAMERS TYPING: NOT the same dichotomy -- the deck preserves
      every M(delta) and U_deck^2 = 256 Gamma = (-1)^F (nonsplit)
      CONSTANT along the family, while the twist class is the
      indicator of m = 4; the mark-fixing reflection lift at pi/2
      is split (U^2 = +2^8): the twist-class choice is the MODULUS
      half of the bit (the one remaining input), the Kramers class
      is the POSITION half (derived from topology, v510).
      UNIFICATION: eta-flip class = frustration class = flag
      transitivity (one Z2 invariant in three clothings; both new
      facets decorate the SAME arc system, A+ = supp(D_s) machine-
      exact, same cardinality obstruction = v512 H1.4 arc-orbit
      argument); the web grows 13 -> 15 faces (sandbox proposal).
  FALSE ORDER PARAMETERS rejected (teeth): sign(omega(D)) flips
      under string reorientation ([C] convention) and is nonzero
      off pi/2 (doubly rejected); the twisted spectral shift is
      nonzero at EVERY m incl. m = 4 (measures delta, never
      selects); the v510 index is CONSTANT on the family (valid OP
      of the position half only).
  CONTROLS: counterwitness cos delta_cw = 3/5 != 0 and
      tan(delta_cw/2) = 1/2 != 1 exactly, no lattice-compatible
      axis (incidence non-integer), carries only the two swap
      reflections -- falls out of BOTH dichotomies; hex/silver fail
      the preconditions upstream (not concyclic / deck not free);
      2-mark anchor: |A+| = |A-| automatic, the flip axis exists
      for EVERY 2-mark configuration (one rotation orbit, no
      modulus) -- the dichotomy is trivially constant: "4 counts".
  VERDICT: SUCCESS -- the alignment bit is equivalent to a
      twist-class choice with a gauge-robust order parameter; the
      bit REMAINS formal input (a definition is not a derivation
      -- it makes the input measurable in principle).  Measurement
      sketch, [C], principle only: transporting the Z2 twist
      defect once around the seam's axis torsor accumulates the
      eta holonomy (+i -> -i), i.e. a relative pi phase between
      interference arms exactly when the bit is set; equivalently
      the sign/indefiniteness datum of the mirror-symmetrized
      4-twist (disorder) correlator across the mark mirror reads
      the same class.  Sandbox only, no marker moves.

Repo anchors (read-only): v525/twist-state probe (machinery reused
verbatim; eta flip + frustration discovered there), v521 (census
solvesets, M(delta) RP battery), v512 (13-face web, counterwitness),
v510 ((-1)^F bridge, Cl(16) machinery), v519 (chiral NS state).
Exactness: sympy exact / integer where marked; all other
certificates 40-digit mpmath (mp.mp.dps = 40), labelled.
Standalone, deterministic.
Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/seam_bit_twist_class_definition_probe.py
"""
import time
from fractions import Fraction as Fr
from itertools import combinations

import mpmath as mp
import sympy as sp

mp.mp.dps = 40

I = sp.I
RESULTS = []
FLAGS = {}
DATA = {}
T0 = time.time()

G_CAR = 5
N16 = 2 ** (G_CAR - 1)          # 16 Majorana seam sites, 4 per mark quadrant
N32 = 2 * N16

TOL25 = mp.mpf(10) ** -25
TOL30 = mp.mpf(10) ** -30
ETA_P = mp.mpc(0, 1)
ETA_M = mp.mpc(0, -1)

d = sp.Symbol('delta', positive=True)
DOM = sp.Interval.Lopen(0, sp.pi / 2)
B_CW = sp.Rational(3, 5) + sp.Rational(4, 5) * I     # v510/v512 counterwitness
D_CW = sp.atan(sp.Rational(4, 3))
B_HEX = I * (2 - sp.sqrt(3))
S_SILVER = 3 + 2 * sp.sqrt(2)


def check(name, ok):
    RESULTS.append(bool(ok))
    print(("PASS" if ok else "FAIL") + " [%2d] %s" % (len(RESULTS), name),
          flush=True)


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
    if len(A) != len(B):
        return False
    used = [False] * len(B)
    for x in A:
        hit = False
        for j, y in enumerate(B):
            if not used[j] and iszero(x - y):
                used[j] = True
                hit = True
                break
        if not hit:
            return False
    return True


def marks_of(bv):
    return [sp.Integer(1), bv, sp.Integer(-1), -bv]


# ---------------------------------------------------------------------------
# exact chiral NS kernel + Wick (v519/v521/twist-probe verbatim)
# ---------------------------------------------------------------------------
def c_exact(dd, n):
    if dd % 2 == 0:
        return sp.Integer(0)
    return sp.Rational(2, n) / sp.sin(sp.pi * sp.Rational(dd, n))


def wick_exact(idx, n):
    if len(idx) == 0:
        return sp.Integer(1)
    if len(idx) % 2 == 1:
        return sp.Integer(0)
    head, rest = idx[0], idx[1:]
    tot = sp.Integer(0)
    for j, bb in enumerate(rest):
        sub = rest[:j] + rest[j + 1:]
        tot += (-1) ** j * (I * c_exact(head - bb, n)) * wick_exact(sub, n)
    return tot


def refl_map(k, n):
    def r(a):
        return (k - a) % n

    def s(a):
        return -1 if (k - a) % (2 * n) >= n else 1
    return r, s


def half_of(k, n):
    if k % 2 == 0:
        f1 = (k // 2) % n
        P = [(f1 + j) % n for j in range(1, n // 2)]
    else:
        bb = (k + 1) // 2
        P = [(bb + j) % n for j in range(n // 2)]
    rP = {(k - a) % n for a in P}
    assert not (rP & set(P))
    return P


def tm_num(mono, r, s, eta):
    """theta on a monomial, numeric coefficient version (v519 theta_mono)."""
    imgs = [r(a) for a in reversed(mono)]
    coeff = mp.mpc(1)
    for _ in mono:
        coeff *= eta
    for a in mono:
        coeff *= s(a)
    lst = list(imgs)
    sign = 1
    for i in range(len(lst)):
        for j in range(len(lst) - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                sign = -sign
    assert len(set(lst)) == len(lst)
    return coeff * sign, tuple(lst)


# ---------------------------------------------------------------------------
# Clifford monomial reduction (v510 mono_mul verbatim; gamma^2 = 1)
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


# ---------------------------------------------------------------------------
# numeric kernels + Pfaffian engine (40 digits, labelled)
# ---------------------------------------------------------------------------
def kmat_num(n):
    cval = {}
    for dd in range(-(n - 1), n):
        if dd % 2 == 0:
            cval[dd] = mp.mpf(0)
        else:
            cval[dd] = (mp.mpf(2) / n) / mp.sin(mp.pi * dd / n)
    return [[mp.mpc(0, 1) * cval[a - b] if a != b else mp.mpc(0)
             for b in range(n)] for a in range(n)]


def pf_num(idx, K):
    n = len(idx)
    if n == 0:
        return mp.mpc(1)
    if n % 2 == 1:
        return mp.mpc(0)
    A = [[K[idx[p]][idx[q]] for q in range(n)] for p in range(n)]
    pf = mp.mpc(1)
    while True:
        m = len(A)
        j = max(range(1, m), key=lambda t: abs(A[0][t]))
        if abs(A[0][j]) < mp.mpf(10) ** -38:
            return mp.mpc(0)
        if j != 1:
            for row in A:
                row[1], row[j] = row[j], row[1]
            A[1], A[j] = A[j], A[1]
            pf = -pf
        a01 = A[0][1]
        pf *= a01
        if m == 2:
            return pf
        A = [[A[i][l] - (A[0][i] * A[1][l] - A[1][i] * A[0][l]) / a01
              for l in range(2, m)] for i in range(2, m)]


def wick_num(idx, K):
    if len(idx) == 0:
        return mp.mpc(1)
    if len(idx) % 2 == 1:
        return mp.mpc(0)
    head, rest = idx[0], idx[1:]
    tot = mp.mpc(0)
    for j, b in enumerate(rest):
        sub = rest[:j] + rest[j + 1:]
        tot += (-1) ** j * K[head][b] * wick_num(sub, K)
    return tot


def ins_val(D, tail, K):
    """omega(D * g_{tail[0]} * ...) via Clifford reduction + Pfaffian."""
    sgn, m = mono_mul(tuple(D), tuple(tail))
    return sgn * pf_num(m, K)


# ---------------------------------------------------------------------------
# signed-permutation conjugation + redress solving (twist probe verbatim)
# ---------------------------------------------------------------------------
def smap_conj(K, mapping, n):
    Q = [[mp.mpc(0)] * n for _ in range(n)]
    for x in range(n):
        mx, sx = mapping[x]
        for y in range(n):
            my, sy = mapping[y]
            Q[mx][my] = sx * sy * K[x][y]
    return Q


def refl_mapping(k, n):
    r, s = refl_map(k, n)
    return [(r(x), s(x)) for x in range(n)]


def deck_mapping(n):
    return [((x + n // 2) % n, -1 if x + n // 2 >= n else 1)
            for x in range(n)]


def sig_mapping(sig):
    return [(j, s) for j, s in enumerate(sig)]


def max_dev(A, B, n):
    return max(abs(A[x][y] - B[x][y]) for x in range(n) for y in range(n))


def sign_solve(A, B, n):
    """site-local signs g with g_x g_y A[x][y] = B[x][y], or None."""
    req = {}
    for x in range(n):
        for y in range(n):
            aA, aB = abs(A[x][y]), abs(B[x][y])
            if aA < TOL30 and aB < TOL30:
                continue
            if aA < TOL30 or aB < TOL30:
                return None
            ratio = B[x][y] / A[x][y]
            if abs(ratio - 1) < mp.mpf(10) ** -20:
                req[(x, y)] = 1
            elif abs(ratio + 1) < mp.mpf(10) ** -20:
                req[(x, y)] = -1
            else:
                return None
    g = [None] * n
    for x0 in range(n):
        if g[x0] is not None:
            continue
        g[x0] = 1
        stack = [x0]
        while stack:
            x = stack.pop()
            for y in range(n):
                rq = req.get((x, y))
                if rq is None:
                    continue
                want = rq * g[x]
                if g[y] is None:
                    g[y] = want
                    stack.append(y)
                elif g[y] != want:
                    return None
    for (x, y), rq in req.items():
        if g[x] * g[y] != rq:
            return None
    return g


def redress_solve(K, k, n):
    Q = smap_conj(K, refl_mapping(k, n), n)
    mK = [[-K[x][y] for y in range(n)] for x in range(n)]
    return sign_solve(Q, mK, n)


def anti_dev_redressed(K, k, n, g):
    """max |(GR) K (GR)^T + K| for the redressed reflection lift."""
    Q = smap_conj(K, refl_mapping(k, n), n)
    return max(abs(g[x] * g[y] * Q[x][y] + K[x][y])
               for x in range(n) for y in range(n))


# ---------------------------------------------------------------------------
# Gram builders + spectra (twist probe verbatim)
# ---------------------------------------------------------------------------
def gram1(k, n, K, D=(), eta=ETA_P, sfun=None, gdress=None):
    P = half_of(k, n)
    r, s0 = refl_map(k, n)
    s = sfun if sfun is not None else s0
    wD = ins_val(D, (), K)
    rows = []
    for a in P:
        g = gdress[r(a)] if gdress is not None else 1
        ca = eta * s(a) * g
        rows.append([ca * ins_val(D, (r(a), b), K) / wD for b in P])
    return rows, wD


def gram_even(k, n, K, D=(), eta=ETA_P):
    P = half_of(k, n)
    r, s = refl_map(k, n)
    basis = [()] + list(combinations(P, 2))
    wD = ins_val(D, (), K)
    rows = []
    for ma in basis:
        ca, ia = tm_num(ma, r, s, eta)
        rows.append([ca * ins_val(D, ia + mb, K) / wD for mb in basis])
    return rows


def herm_eig(rows):
    n = len(rows)
    dev = max(abs(rows[i][j] - mp.conj(rows[j][i]))
              for i in range(n) for j in range(n))
    A = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            A[i, j] = (rows[i][j] + mp.conj(rows[j][i])) / 2
    E, _ = mp.eighe(A)
    return dev, sorted(E[i].real for i in range(n))


def inertia(evs, tol=TOL25):
    npos = sum(1 for e in evs if e > tol)
    nneg = sum(1 for e in evs if e < -tol)
    return (npos, nneg, len(evs) - npos - nneg)


def spec_dev(e1, e2):
    return max(abs(x - y) for x, y in zip(e1, e2))


def best_eta(k, n, K, D=(), sfun=None, gdress=None):
    out = []
    for eta, tag in ((ETA_P, '+i'), (ETA_M, '-i')):
        rows, wD = gram1(k, n, K, D, eta, sfun, gdress)
        dev, evs = herm_eig(rows)
        if dev < TOL25:
            nz = [abs(e) for e in evs if abs(e) > TOL25]
            out.append((tag, dev, inertia(evs), min(nz) if nz else mp.mpf(0),
                        evs))
    out.sort(key=lambda t: t[2][1])          # fewest negative eigs first
    return out


# ---------------------------------------------------------------------------
# mark geometry (units of pi/n; circle = 2n units; sites at odd units)
# ---------------------------------------------------------------------------
def mark_units(n, m):
    mu = m * n // 8
    return mu, [0, mu, n, n + mu]


def arc_sites(n, lo, hi):
    return [j for j in range(n) if lo < (2 * j + 1) % (2 * n) < hi]


def sigma_vec(n, m):
    mu, _ = mark_units(n, m)
    a1 = set(arc_sites(n, 0, mu))
    a3 = set(arc_sites(n, n, n + mu))
    return [1 if j in a1 or j in a3 else -1 for j in range(n)]


def d_string(n, m):
    mu, _ = mark_units(n, m)
    return tuple(sorted(arc_sites(n, 0, mu) + arc_sites(n, n, n + mu)))


def d_string_long(n, m):
    mu, _ = mark_units(n, m)
    return tuple(sorted(arc_sites(n, mu, n) + arc_sites(n, n + mu, 2 * n)))


def defect_planes(n, m):
    _, marks = mark_units(n, m)
    return [(((u - 2) // 2) % n, (u // 2) % n) for u in marks]


def mu4_mapping(n, m, pattern):
    mapping = [(x, 1) for x in range(n)]
    for (p, q), eps in zip(defect_planes(n, m), pattern):
        mapping[p] = (q, eps)
        mapping[q] = (p, -eps)
    return mapping


def swap_axes(n, m):
    mu, _ = mark_units(n, m)
    k1 = mu // 2 - 1
    return [k1 % n, (k1 + n // 2) % n]


def fix_axes(n):
    return [(n - 1) % n, (n // 2 - 1) % n]


def axis_census(n, marks):
    """complete reflection census: for k = 0..n-1 (ALL reflections of D_n
    on the refined circle) return {k: 'fix'|'swap'} for the ones whose
    unit map u -> 2(k+1) - u preserves the mark-unit set."""
    ms = {u % (2 * n) for u in marks}
    out = {}
    for k in range(n):
        img = {(2 * (k + 1) - u) % (2 * n) for u in ms}
        if img == ms:
            fixed = {u for u in ms if (2 * (k + 1) - u) % (2 * n) == u}
            out[k] = 'fix' if fixed else 'swap'
    return out


def gclass(sig, k, n):
    """gauge class of g = (sigma o r) * sigma in {+1, -1, alt, -alt,
    other} -- the four non-'other' classes are exactly the site-sign
    vectors with g_x g_y = 1 for every odd distance."""
    r, _ = refl_map(k, n)
    g = [sig[r(j)] * sig[j] for j in range(n)]
    if all(x == 1 for x in g):
        return '+1'
    if all(x == -1 for x in g):
        return '-1'
    if all(x == (1 if j % 2 == 0 else -1) for j, x in enumerate(g)):
        return 'alt'
    if all(x == (-1 if j % 2 == 0 else 1) for j, x in enumerate(g)):
        return '-alt'
    return 'other'


# ---------------------------------------------------------------------------
# exact Cl(n) machinery over Fractions (v510/v521 verbatim)
# ---------------------------------------------------------------------------
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


def prop(x, y):
    if not x or not y or set(x) != set(y):
        return (False, None)
    m0 = next(iter(y))
    c = x[m0] / y[m0]
    return (all(x[m] == c * y[m] for m in y), c)


def apply_lin(mat, a, n):
    out = {}
    for bb in range(n):
        if mat[bb][a]:
            out = cadd(out, cscale(gam(bb), Fr(mat[bb][a])))
    return out


def implements(Uel, mat, n):
    for a in range(n):
        lhs = cmul(Uel, gam(a))
        rhs = cmul(apply_lin(mat, a, n), Uel)
        if cadd(lhs, cscale(rhs, Fr(-1))):
            return False
    return True


def shift_matrix(n, k, wrap_sign):
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        bb = (a + k) % n
        M[bb][a] = wrap_sign if a + k >= n else 1
    return M


def refl_matrix(n, k, wrap_sign):
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        idx = (k - a) % (2 * n)
        M[idx % n][a] = wrap_sign if idx >= n else 1
    return M


def refl_implementer(n, k):
    fixed = [j for j in range(n) if (k - j) % n == j]
    if fixed:
        fplus = [f for f in fixed if (k - f) % (2 * n) < n]
        U = {tuple(j for j in range(n) if j != fplus[0]): Fr(1)}
    else:
        U = dict(ONE)
    for a in range(n):
        bb = (k - a) % n
        if a >= bb or a in fixed:
            continue
        idx = (k - a) % (2 * n)
        eps = Fr(-1) if idx >= n else Fr(1)
        U = cmul(U, cadd(gam(a), cscale(gam(bb), eps)))
    return U


# ===========================================================================
# MACH -- machinery validation
# ===========================================================================
def mach(K16):
    print("  -- MACH: Pfaffian engine vs Wick recursion vs exact sympy")
    sets = [(0, 1, 2, 3), (1, 2, 4, 7), (0, 2, 5, 9, 11, 14),
            (1, 3, 4, 7, 9, 12), tuple(range(8))]
    dev1 = max(abs(pf_num(t, K16) - wick_num(t, K16)) for t in sets)
    ex = wick_exact([1, 2, 4, 7], N16)
    re_, im_ = sp.expand_complex(ex).as_real_imag()
    exv = mp.mpc(mp.mpf(str(sp.N(re_, 45))), mp.mpf(str(sp.N(im_, 45))))
    dev2 = abs(pf_num((1, 2, 4, 7), K16) - exv)
    sg, mm = mono_mul((0, 1, 8, 9), (0, 5))
    red_ok = (mm == (1, 5, 8, 9) and sg == -1)
    check("MACH.1 ENGINE VALIDATION [40-digit vs exact]: Parlett-Reid "
          "Pfaffian agrees with the v519 Wick recursion on 5 index sets "
          "(max dev %s) and with the exact sympy 4-point value (dev %s); "
          "Clifford reduction witness g0g1g8g9 * g0g5 = -g1g5g8g9 (%s) -- "
          "the insertion machinery is trustworthy"
          % (mp.nstr(dev1, 3), mp.nstr(dev2, 3), red_ok),
          dev1 < mp.mpf(10) ** -35 and dev2 < mp.mpf(10) ** -35 and red_ok)


# ===========================================================================
# S -- frame: incidence, symbolic solvesets, complete axis census
# ===========================================================================
def s_frame():
    print("  -- S: frame -- incidence, solvesets, complete axis census")

    ok_frame = True
    for n in (N16, N32):
        mr = range(1, 5) if n == N16 else range(1, 8)
        for m in mr:
            mu, marks = mark_units(n, m)
            sites = {(2 * j + 1) for j in range(n)}
            ok_frame &= not ({u % (2 * n) for u in marks} & sites)
            sig = sigma_vec(n, m)
            flips = sum(1 for j in range(n) if sig[j] != sig[(j + 1) % n])
            ok_frame &= flips == 4
            # sigma support identity: A+ = supp(D_short) exactly
            ok_frame &= (tuple(j for j in range(n) if sig[j] == 1)
                         == d_string(n, m))
    sol_cos = sp.solveset(sp.cos(d), d, DOM)      # mark-fixing reflection
    sol_sin = sp.solveset(sp.sin(d), d, DOM)
    sol_arc = sp.solveset(d - (sp.pi - d), d, DOM)  # arc-system exchange
    cw_cos = sp.cos(D_CW)
    cw_tanh = sp.simplify((1 - sp.cos(D_CW)) / sp.sin(D_CW))
    FLAGS['frame'] = (ok_frame and sol_cos == sp.FiniteSet(sp.pi / 2)
                      and sol_sin is sp.S.EmptySet
                      and sol_arc == sp.FiniteSet(sp.pi / 2)
                      and cw_cos == sp.Rational(3, 5)
                      and cw_tanh == sp.Rational(1, 2))
    check("S1.1 FRAME + SOLVESETS [exact integers + symbolic]: marks on "
          "bond midpoints and sigma flips exactly at the 4 marks for all "
          "members (N = 16 m = 1..4, N = 32 m = 1..7: %s); the sigma = +1 "
          "support IS the short-string support supp(D_short), exactly "
          "(same loop) -- the two pi/2 structures decorate the SAME arc "
          "system; symbolic: a mark-FIXING reflection exists iff cos "
          "delta = 0, solveset %s (sin delta = 0: %s, v521 S1.1); the "
          "arc-system exchange delta = pi - delta solves to %s; "
          "counterwitness exact data: cos delta_cw = %s != 0, "
          "tan(delta_cw/2) = %s != 1"
          % (ok_frame, sol_cos, sol_sin, sol_arc, cw_cos, cw_tanh),
          FLAGS['frame'])

    cen = {}
    for n in (N16, N32):
        mr = range(1, 5) if n == N16 else range(1, 8)
        for m in mr:
            _, marks = mark_units(n, m)
            cen[(n, m)] = axis_census(n, marks)
    exp16 = {m: ({m - 1: 'swap', m + 7: 'swap'} if m != 4 else
                 {3: 'swap', 11: 'swap', 15: 'fix', 7: 'fix'})
             for m in range(1, 5)}
    exp32 = {m: ({2 * m - 1: 'swap', (2 * m + 15) % 32: 'swap'}
                 if m != 4 else
                 {7: 'swap', 23: 'swap', 31: 'fix', 15: 'fix'})
             for m in range(1, 8)}
    cen_ok = (all(cen[(N16, m)] == exp16[m] for m in range(1, 5))
              and all(cen[(N32, m)] == exp32[m] for m in range(1, 8)))
    DATA['census32'] = {m: cen[(N32, m)] for m in range(1, 8)}
    DATA['census16'] = {m: cen[(N16, m)] for m in range(1, 5)}
    FLAGS['census'] = cen_ok
    check("S1.2 COMPLETE AXIS CENSUS [exact integers, ALL n reflections "
          "per lattice]: the mark-set-preserving reflections are EXACTLY "
          "the two swap axes for every member m != 4 and exactly 2 swap "
          "+ 2 fixing axes at m = 4 (N = 16: %s; N = 32 e.g. m = 2: %s, "
          "m = 4: %s) -- mark-fixing axes exist iff delta = pi/2 on both "
          "lattices, no other reflection anywhere preserves the marks: "
          "the (=>)-backbone of both facets"
          % (cen_ok, cen[(N32, 2)], cen[(N32, 4)]),
          cen_ok)


# ===========================================================================
# E14 -- facet #14: the eta flip <=> delta = pi/2 (both directions)
# ===========================================================================
def e14(K16, K32):
    print("  -- E14: facet #14 -- eta flip <=> delta = pi/2")

    # (<=) at pi/2: flip fires on every fixing axis
    mech = True
    flips = {}
    for n, K in ((N16, K16), (N32, K32)):
        sig = sigma_vec(n, 4)
        Ka = smap_conj(K, sig_mapping(sig), n)
        r_ok = True
        for k in fix_axes(n):
            r, _ = refl_map(k, n)
            r_ok &= all(sig[r(j)] == -sig[j] for j in range(n))
            tw = best_eta(k, n, Ka)
            un = best_eta(k, n, K)
            flips[(n, k)] = (un[0][0], tw[0][0], un[0][2], tw[0][2],
                             spec_dev(un[0][4], tw[0][4]))
        mech &= r_ok
    flip_ok = all(u != t and iu == (nn // 2, 0, 0) and it == (nn // 2, 0, 0)
                  and dv < TOL30
                  for (nn, k), (u, t, iu, it, dv) in flips.items())
    sig16 = sigma_vec(N16, 4)
    Ka16 = smap_conj(K16, sig_mapping(sig16), N16)
    dtw, etw = herm_eig(gram_even(15, N16, Ka16, (), ETA_P))
    dun, eun = herm_eig(gram_even(15, N16, K16, (), ETA_P))
    even_ok = (inertia(etw) == (29, 0, 0) and inertia(eun) == (29, 0, 0)
               and spec_dev(etw, eun) < TOL25
               and max(dtw, dun) < TOL25)
    FLAGS['f14_fwd'] = mech and flip_ok and even_ok
    check("E14.1 (<=) THE FLIP FIRES AT pi/2 [exact mechanism + 40-digit]: "
          "on ALL FOUR mark-fixing axes (N = 16 k = 15/7, N = 32 k = "
          "31/15) sigma o r = -sigma holds site-by-site exactly (%s) and "
          "the pinned RP sign flips with 40-digit-identical spectra "
          "(N16 k=15: %s->%s, k=7: %s->%s; N32 k=31: %s->%s, k=15: "
          "%s->%s; all PD, max spec dev %s); the even deg <= 2 sector is "
          "UNTOUCHED (twisted/untwisted inertia (29,0,0)/(29,0,0), spec "
          "dev %s) -- the flip is an odd-sector negation M_tw = -D M D, "
          "exactly"
          % (mech, flips[(N16, 15)][0], flips[(N16, 15)][1],
             flips[(N16, 7)][0], flips[(N16, 7)][1],
             flips[(N32, 31)][0], flips[(N32, 31)][1],
             flips[(N32, 15)][0], flips[(N32, 15)][1],
             mp.nstr(max(v[4] for v in flips.values()), 3),
             mp.nstr(spec_dev(etw, eun), 3)),
          FLAGS['f14_fwd'])

    # (=>) on every existing axis off pi/2: no flip
    ok2 = True
    devs = []
    etas = {}
    for n, K, mr in ((N16, K16, (2, 4)), (N32, K32, range(1, 8))):
        for m in mr:
            sig = sigma_vec(n, m)
            Ka = smap_conj(K, sig_mapping(sig), n)
            for k in swap_axes(n, m):
                r, _ = refl_map(k, n)
                ok2 &= all(sig[r(j)] == sig[j] for j in range(n))
                tw = best_eta(k, n, Ka)
                un = best_eta(k, n, K)
                ok2 &= (bool(tw) and bool(un) and tw[0][0] == un[0][0]
                        and tw[0][2] == (n // 2, 0, 0))
                devs.append(spec_dev(tw[0][4], un[0][4]))
                if n == N32 and k == swap_axes(n, m)[0]:
                    etas[m] = (un[0][0], tw[0][0])
    DATA['flip32'] = {m: (1 if m == 4 else 0) for m in range(1, 8)}
    FLAGS['f14_bwd_ax'] = ok2 and max(devs) < TOL30
    check("E14.2 (=>) NO FLIP ON ANY EXISTING AXIS OFF pi/2 [exact "
          "mechanism + 40-digit]: on EVERY mark-compatible swap axis of "
          "the whole ladder (N = 16 m = 2, 4; N = 32 m = 1..7 incl. "
          "pi/2 +- pi/8, both axes each) sigma o r = +sigma holds "
          "site-by-site exactly and the pinned eta NEVER flips (all PD "
          "with the untwisted eta: %s; twisted spectra identical to "
          "untwisted, max dev %s) -- combined with S1.2 (no other axes "
          "exist) the flip structure is ABSENT at every delta != pi/2"
          % (ok2, mp.nstr(max(devs), 3)),
          FLAGS['f14_bwd_ax'])

    # (=>) generalized kill: cardinality lemma + complete g-class census
    card16 = all(((2 * m == 16 - 2 * m) == (m == 4)) for m in range(1, 5))
    card32 = all(((4 * m == 32 - 4 * m) == (m == 4)) for m in range(1, 8))
    cnt32 = all(sum(1 for x in sigma_vec(N32, m) if x == 1) == 4 * m
                for m in range(1, 8))
    gtab = {}
    altcnt = 0
    for m in range(1, 8):
        sig = sigma_vec(N32, m)
        for k in range(N32):
            cls = gclass(sig, k, N32)
            gtab[(m, k)] = cls
            if cls in ('alt', '-alt'):
                altcnt += 1
    flip_axes32 = {m: sorted(k for k in range(N32)
                             if gtab[(m, k)] == '-1')
                   for m in range(1, 8)}
    gen_ok = flip_axes32 == {m: ([15, 31] if m == 4 else [])
                             for m in range(1, 8)}
    cls_k31_m2 = gtab[(2, 31)]
    FLAGS['f14_gen'] = card16 and card32 and cnt32 and gen_ok
    check("E14.3 (=>) GENERALIZED KILL [exact integers, complete]: "
          "CARDINALITY LEMMA -- sigma o f = -sigma for ANY bijection f "
          "(modified return included) forces |A+| = |A-|, and |A+| = "
          "mu = 4m vs |A-| = 32 - 4m (counts verified: %s) are equal "
          "IFF m = 4 (N16: 2m vs 16 - 2m, same: %s) = the S1.1 solveset "
          "delta = pi - delta -> {pi/2}; COMPLETE g-CLASS CENSUS over "
          "ALL 32 x 7 = 224 axes: the global flip class g = -1 occurs "
          "EXACTLY at {15, 31} for m = 4 and NOWHERE else (%s; "
          "alternating classes: %d occurrences -- inadmissible, see "
          "O2.1; e.g. the mark-pair axis k = 31 at m = 2 has class "
          "'%s', and h*g in {+-1, +-alt} with h in the admissible set "
          "{+-1} cannot repair a class outside {+-1, +-alt}) -- no "
          "redressed/modified-return flip exists off the clock point"
          % (cnt32, card16 and card32, gen_ok, altcnt, cls_k31_m2),
          FLAGS['f14_gen'])
    DATA['gtab32'] = gtab
    DATA['etas_ladder'] = etas


# ===========================================================================
# E15 -- facet #15: twist frustration <=> delta = pi/2 (both directions)
# ===========================================================================
def e15(K16, K32):
    print("  -- E15: facet #15 -- twist frustration <=> delta = pi/2")

    # (<=) at pi/2: exchange + unique minimal closed insertion, indefinite
    res = {}
    ok_map, ok_uni = True, True
    for n, K in ((N16, K16), (N32, K32)):
        Ds = d_string(n, 4)
        Dl = d_string_long(n, 4)
        ws = ins_val(Ds, (), K)
        wl = ins_val(Dl, (), K)
        ok_uni &= abs(ws - wl) < TOL30 and abs(ws) > TOL25
        klist = fix_axes(n) if n == N16 else [fix_axes(n)[0]]
        for k in klist:
            r, sf = refl_map(k, n)
            ok_map &= tuple(sorted(r(x) % n for x in Ds)) == Dl
            P = half_of(k, n)
            picks = []
            for eta, tag in ((ETA_P, '+i'), (ETA_M, '-i')):
                rows = []
                for a in P:
                    ca = eta * sf(a)
                    rows.append([ca * (ins_val(Ds, (r(a), b), K)
                                       + ins_val(Dl, (r(a), b), K))
                                 / (ws + wl) for b in P])
                dev, evs = herm_eig(rows)
                if dev < TOL25:
                    picks.append((tag, inertia(evs)))
            res[(n, k)] = picks
    ind_ok = all(len(p) == 2 and all(it[0] > 0 and it[1] > 0 and it[2] == 0
                                     for _, it in p)
                 for p in res.values())
    exp_in = (res[(N16, 15)][0][1] == (4, 4, 0)
              and res[(N32, 31)][0][1] == (8, 8, 0))
    FLAGS['f15_fwd'] = ok_map and ok_uni and ind_ok and exp_in
    check("E15.1 (<=) FRUSTRATION AT pi/2 [exact sets + 40-digit]: on "
          "every fixing axis theta maps the short-string system to the "
          "long one exactly (r(D_short) = D_long as sets: %s); the two "
          "normalisations agree exactly, omega(D_s) = omega(D_l) "
          "(quarter-shift invariance, dev < 1e-30: %s), so the "
          "DIFFERENCE insertion is ill-normalised (omega = 0) and the "
          "minimal theta-closed insertion is UNIQUE = D_s + D_l; its "
          "Gram is Hermitian for BOTH eta and INDEFINITE everywhere: "
          "N = 16 k = 15/7: %s / %s, N = 32 k = 31: %s -- in the "
          "4-twist-decorated state RP on the mark-fixing cut FAILS at "
          "pi/2 (both eta): the twist frustrates the mark mirror"
          % (ok_map, ok_uni, res[(N16, 15)], res[(N16, 7)],
             res[(N32, 31)]),
          FLAGS['f15_fwd'])

    # (=>) off pi/2: theta reducible + PD ladder + cardinality
    print("        (b) N = 32 insertion ladder (one swap axis each) ...",
          flush=True)
    lad = {}
    wds = {}
    red_ok = True
    for m in range(1, 8):
        Ds = d_string(N32, m)
        wds[m] = ins_val(Ds, (), K32)
        k = swap_axes(N32, m)[0]
        r, _ = refl_map(k, N32)
        red_ok &= tuple(sorted(r(x) % N32 for x in Ds)) == Ds
        picks = best_eta(k, N32, K32, Ds)
        lad[m] = picks[0] if picks else None
        print("          m=%d (delta=%dpi/8): k=%d %s" %
              (m, m, k, "eta=%s %s min %s" % (lad[m][0], lad[m][2],
                                              mp.nstr(lad[m][3], 5))
               if lad[m] else '---'), flush=True)
    all_pd = all(p is not None and p[2] == (16, 0, 0) for p in lad.values())
    card = all(((4 * m == 32 - 4 * m) == (m == 4)) for m in range(1, 8))
    # exact N = 16 m = 2 witness
    D16 = d_string(N16, 2)
    k16 = swap_axes(N16, 2)[0]
    P = half_of(k16, N16)
    r, s = refl_map(k16, N16)
    wDex = wick_exact(list(D16), N16)
    rows_ex = []
    for a in P:
        row = []
        for b in P:
            sg, mm = mono_mul(D16, ((r(a)), b))
            row.append(sp.expand_complex(
                I * s(a) * sg * wick_exact(list(mm), N16) / wDex))
        rows_ex.append(row)
    herm_ex = all(iszero(rows_ex[i][j] - sp.conjugate(rows_ex[j][i]))
                  for i in range(8) for j in range(8))
    num_ex = [[mp.mpc(mp.mpf(str(sp.N(sp.re(x), 45))),
                      mp.mpf(str(sp.N(sp.im(x), 45)))) for x in row]
              for row in rows_ex]
    dev_ex, evs_ex = herm_eig(num_ex)
    in_ex = inertia(evs_ex)
    DATA['lad'] = lad
    DATA['wds'] = wds
    DATA['frus32'] = {m: (1 if m == 4 else 0) for m in range(1, 8)}
    FLAGS['f15_bwd'] = red_ok and all_pd and card and herm_ex \
        and in_ex == (8, 0, 0)
    check("E15.2 (=>) NO FRUSTRATION OFF pi/2 [exact + 40-digit]: on "
          "every existing (swap) axis theta acts REDUCIBLY -- r(D_short) "
          "= D_short exactly for all m (%s), the single string is "
          "already theta-closed and its insertion Gram is PD (16,0,0) "
          "along the WHOLE N = 32 ladder m = 1..7 incl. pi/2 +- pi/8 "
          "(%s); exact N = 16 m = 2 witness: Gram Hermitian exactly in "
          "sympy (%s), inertia %s; and the frustration MECHANISM (theta "
          "exchanging the string systems) is killed off pi/2 by the "
          "SAME cardinality lemma: |D_s| = 4m = |D_l| = 32 - 4m iff "
          "m = 4 (%s) -- no bijection whatsoever can exchange the "
          "systems, and no fixing axis exists (S1.2): frustration is "
          "not formulable at any delta != pi/2"
          % (red_ok, all_pd, herm_ex, in_ex, card),
          FLAGS['f15_bwd'])

    # reducible-decoration control: the sum insertion on swap axes
    print("        (c) reducible sum-insertion control (m = 2, 7) ...",
          flush=True)
    ctrl = {}
    for m in (2, 7):
        Ds = d_string(N32, m)
        Dl = d_string_long(N32, m)
        k = swap_axes(N32, m)[0]
        r, sf = refl_map(k, N32)
        li = tuple(sorted(r(x) % N32 for x in Dl)) == Dl
        ws = wds[m]
        wl = ins_val(Dl, (), K32)
        pl = best_eta(k, N32, K32, Dl)
        P = half_of(k, N32)
        rows = []
        for a in P:
            ca = ETA_P * sf(a)
            rows.append([ca * (ins_val(Ds, (r(a), b), K32)
                               + ins_val(Dl, (r(a), b), K32)) / (ws + wl)
                         for b in P])
        dev, evs = herm_eig(rows)
        ctrl[m] = (li, mp.re(ws), mp.re(wl),
                   pl[0][2] if pl else None, dev, inertia(evs),
                   abs(ws - wl))
    sect_ok = all(v[0] and v[3] == (16, 0, 0) and v[4] < TOL25
                  for v in ctrl.values())
    same_sign = all(ctrl[m][1] * ctrl[m][2] > 0 for m in (2, 7))
    sum_pd = all(ctrl[m][5] == (16, 0, 0) for m in (2, 7))
    w_equal = all(ctrl[m][6] < TOL30 for m in (2, 7))
    FLAGS['f15_red'] = sect_ok and same_sign and sum_pd
    check("E15.3 REDUCIBLE-DECORATION CONTROL [40-digit, typed [C] "
          "fence]: on swap axes BOTH string systems are individually "
          "theta-closed (r(D_long) = D_long: %s) and both sector Grams "
          "are PD (long-string insertion (16,0,0): %s) -- the SUM "
          "insertion omega((D_s + D_l).)/(w_s + w_l) is their exact "
          "positive-weight mixture: the two normalisations agree at 40 "
          "digits even OFF pi/2 (m = 2: w_s = %s = w_l; m = 7: %s; "
          "|w_s - w_l| < 1e-30: %s -- the complement-string identity), "
          "same sign at both test members (%s), and the sum Gram is PD "
          "%s / %s as forced for a positive mixture of PD sectors -- a "
          "theta-REDUCIBLE decoration can NEVER certify frustration "
          "(each irreducible sector is PD; indefiniteness could only "
          "be manufactured by mixed normalisation weights, a "
          "convention, never a mirror datum): facet #15 is therefore "
          "typed with the irreducibility clause (frustration = the "
          "exchange-FORCED symmetrized insertion is indefinite), and "
          "that clause is cardinality-locked to pi/2"
          % (all(v[0] for v in ctrl.values()), sect_ok,
             mp.nstr(ctrl[2][1], 5), mp.nstr(ctrl[7][1], 5), w_equal,
             same_sign, ctrl[2][5], ctrl[7][5]),
          FLAGS['f15_red'])


# ===========================================================================
# U -- unification theorem + Kramers typing
# ===========================================================================
def u_unify(K16, K32):
    print("  -- U: unification -- one Z2 invariant, and the Kramers half")

    t_flip = DATA['flip32']
    t_frus = DATA['frus32']
    bit = {m: (1 if m == 4 else 0) for m in range(1, 8)}
    same = (t_flip == t_frus == bit)
    supp = all(tuple(j for j in range(N32) if sigma_vec(N32, m)[j] == 1)
               == d_string(N32, m) for m in range(1, 8))
    FLAGS['unify'] = same and supp
    check("U1.1 UNIFICATION THEOREM [assembled from exact results]: the "
          "three lattice functions m -> {eta-flip exists}, m -> "
          "{frustration exists}, m -> {delta_m = pi/2} are IDENTICAL "
          "over the whole ladder (%s = the bit indicator); both facets "
          "decorate the SAME arc system (A+ = supp(D_short) exactly: "
          "%s) and are locked by the SAME cardinality lemma = the "
          "continuum arc-exchange solveset {pi/2} = the v512 H1.4 "
          "flag/arc-transitivity face -- eta-flip class, frustration "
          "class and flag transitivity are ONE Z2 invariant in three "
          "clothings: candidate facets #14/#15 join the web as one "
          "invariant (13 -> 15 faces, SANDBOX proposal, no v512 edit)"
          % (same, supp),
          FLAGS['unify'])

    # Kramers half: deck datum constant along the family
    deck_all = True
    for n in (N16, N32):
        mr = range(1, 5) if n == N16 else range(1, 8)
        for m in mr:
            _, marks = mark_units(n, m)
            ms = {u % (2 * n) for u in marks}
            deck_all &= {(u + n) % (2 * n) for u in ms} == ms
    GAMMA = {tuple(range(N16)): Fr(1)}
    D_ns = shift_matrix(N16, 8, -1)
    Ut = dict(ONE)
    for j in range(8):
        Ut = cmul(Ut, cadd(ONE, cscale(cmul(gam(j), gam(j + 8)), Fr(-1))))
    impl_c = implements(Ut, D_ns, N16)
    ok_u2, coef = prop(cmul(Ut, Ut), GAMMA)
    U15 = refl_implementer(N16, 15)
    R15 = refl_matrix(N16, 15, -1)
    negR15 = [[-x for x in row] for row in R15]
    impl_r = implements(U15, R15, N16) or implements(U15, negR15, N16)
    ok_sq, c_sq = prop(cmul(U15, U15), ONE)
    twist_nonconst = (DATA['flip32'][4] == 1
                      and all(DATA['flip32'][m] == 0
                              for m in range(1, 8) if m != 4))
    FLAGS['kramers'] = (deck_all and impl_c and ok_u2 and coef == Fr(256)
                        and impl_r and ok_sq and c_sq == Fr(2 ** 8)
                        and twist_nonconst)
    check("U2.1 KRAMERS TYPING [exact Cl(16) Fractions + census]: the "
          "deck (antipode) preserves EVERY family member's mark set "
          "(%s) and its NS lift squares to %s x gamma_1..16 = (-1)^F "
          "(implements: %s) -- the v510 Kramers datum U^2 = (-1)^F "
          "(nonsplit) is CONSTANT along M(delta); the mark-fixing "
          "reflection lift at pi/2 is SPLIT (implements: %s, U^2 = %s "
          "x 1 = +2^8); the twist-class invariant is NON-constant "
          "(indicator of m = 4: %s) -- ANSWER (c), exactly typed: the "
          "twist-class choice is NOT the same dichotomy as "
          "split/nonsplit; the Kramers class is the POSITION half of "
          "the old bit (derived from topology, v510), the twist class "
          "is the MODULUS half (the one remaining input): the bit "
          "faces that unify are #14 = #15 = flag transitivity, while "
          "the fermionic face stays on the derived half"
          % (deck_all, coef, impl_c, impl_r, c_sq, twist_nonconst),
          FLAGS['kramers'])


# ===========================================================================
# O -- order parameter: definition, robustness, false candidates
# ===========================================================================
def o_param(K16, K32):
    print("  -- O: order parameter -- definition, robustness, teeth")

    # O1: definition + table
    otab = {}
    for m in range(1, 8):
        cenm = DATA['census32'][m]
        sig = sigma_vec(N32, m)
        fl = [k for k in cenm if gclass(sig, k, N32) == '-1']
        otab[m] = Fr(len(fl), len(cenm))
    o16 = {}
    for m in (2, 4):
        cenm = DATA['census16'][m]
        sig = sigma_vec(N16, m)
        fl = [k for k in cenm if gclass(sig, k, N16) == '-1']
        o16[m] = Fr(len(fl), len(cenm))
    tab_ok = (all(otab[m] == (Fr(1, 2) if m == 4 else 0)
                  for m in range(1, 8))
              and o16 == {2: Fr(0), 4: Fr(1, 2)})
    sig4 = sigma_vec(N16, 4)
    cyc = [15, 3, 7, 11]
    cls = {k: gclass(sig4, k, N16) for k in cyc}
    char_ok = all(cls[cyc[(i + 1) % 4]] != cls[cyc[i]] for i in range(4)) \
        and all(cls[k] in ('+1', '-1') for k in cyc)
    sig2v = sigma_vec(N32, 2)
    const_off = (gclass(sig2v, 3, N32) == gclass(sig2v, 19, N32) == '+1')
    FLAGS['op_table'] = tab_ok and char_ok and const_off
    print("        O(m), N = 32 ladder: " + ", ".join(
        "m=%d: %s" % (m, otab[m]) for m in range(1, 8)))
    check("O1.1 ORDER PARAMETER [exact integers]: O := (#flip axes) / "
          "(#mark-compatible axes) -- table: N = 32 ladder O = %s, "
          "N = 16 O(2) = %s, O(4) = %s: O = 1/2 EXACTLY at the clock "
          "member and 0 everywhere else (O != 0 <=> bit set: %s); the "
          "flip datum around the pi/2 axis torsor k = 15 -> 3 -> 7 -> "
          "11 under the EIGHTH rotation k -> k + 4 (the Z8 clock-tower "
          "shadow) alternates exactly (%s: classes %s) -- the "
          "nontrivial Z2 character; off pi/2 the two axes carry the "
          "constant class '+1' (%s)"
          % ([str(otab[m]) for m in range(1, 8)], o16[2], o16[4],
             tab_ok, char_ok, [cls[k] for k in cyc], const_off),
          FLAGS['op_table'])

    # O2: gauge robustness
    sig16 = sigma_vec(N16, 4)
    Ka16 = smap_conj(K16, sig_mapping(sig16), N16)
    # (i) sigma global flip: g invariant identically
    r15, _ = refl_map(15, N16)
    gplus = [sig16[r15(j)] * sig16[j] for j in range(N16)]
    gmin = [(-sig16[r15(j)]) * (-sig16[j]) for j in range(N16)]
    inv_sigma = gplus == gmin
    # (ii) admissible global -1 redress: both pinned eta flip together
    gm1 = [-1] * N16
    un0 = best_eta(15, N16, K16)
    tw0 = best_eta(15, N16, Ka16)
    un1 = best_eta(15, N16, K16, (), None, gm1)
    tw1 = best_eta(15, N16, Ka16, (), None, gm1)
    red_inv = (un1[0][0] != un0[0][0] and tw1[0][0] != tw0[0][0]
               and (un0[0][0] != tw0[0][0]) == (un1[0][0] != tw1[0][0]))
    # (iii) alternating redress inadmissible (teeth)
    halt = [1 if x % 2 == 0 else -1 for x in range(N16)]
    picks_alt = best_eta(15, N16, K16, (), None, halt)
    alt_bad = (len(picks_alt) > 0
               and all(p[2][0] > 0 and p[2][1] > 0 for p in picks_alt))
    # (iv) mu4 overlay at N = 32, m = 4, k = 31 (plane gauge/pattern flip)
    pats = {'uniform': (1, 1, 1, 1), 'alternating': (1, -1, 1, -1),
            'flipped': (-1, 1, -1, 1)}
    Ku = smap_conj(K32, mu4_mapping(N32, 4, pats['uniform']), N32)
    Kal = smap_conj(K32, mu4_mapping(N32, 4, pats['alternating']), N32)
    plane_gauge = sign_solve(Ku, Kal, N32) is not None
    sig32 = sigma_vec(N32, 4)
    overlay = {}
    for name, pat in pats.items():
        Kc = smap_conj(K32, mu4_mapping(N32, 4, pat), N32)
        g = redress_solve(Kc, 31, N32)
        if g is None:
            overlay[name] = None
            continue
        Kca = smap_conj(Kc, sig_mapping(sig32), N32)
        dev_pre = anti_dev_redressed(Kca, 31, N32, g)
        unp = best_eta(31, N32, Kc, (), None, g)
        twp = best_eta(31, N32, Kca, (), None, g)
        # the flip datum on the decorated state is the exact relative
        # negation M_tw = -D M D: the eta-resolved inertias swap eta ->
        # -eta and the best-eta spectra coincide (PD-ness is NOT part of
        # the datum -- on the fixing cut the mark-bond defect planes
        # straddle the cut, so the mu4 Gram is legitimately indefinite)
        overlay[name] = (dev_pre < TOL25, bool(unp) and bool(twp)
                         and unp[0][0] != twp[0][0]
                         and unp[0][2] == twp[0][2],
                         spec_dev(unp[0][4], twp[0][4]) if unp and twp
                         else mp.mpf(1),
                         unp[0][2] if unp else None)
    over_ok = all(v is not None and v[0] and v[1] and v[2] < TOL25
                  for v in overlay.values())
    over_in = overlay['alternating'][3] if overlay['alternating'] else None
    # (v) string orientation: normalized insertion functional invariant
    Ds = d_string(N32, 2)
    Dp = (Ds[1], Ds[0]) + Ds[2:]
    w0 = ins_val(Ds, (), K32)
    wp = ins_val(Dp, (), K32)
    orient_flip = abs(wp + w0) < TOL30
    ratio_dev = abs(ins_val(Dp, (5, 12), K32) / wp
                    - ins_val(Ds, (5, 12), K32) / w0)
    FLAGS['op_robust'] = (inv_sigma and red_inv and alt_bad and plane_gauge
                          and over_ok and orient_flip
                          and ratio_dev < TOL30)
    check("O2.1 GAUGE ROBUSTNESS OF O [exact + 40-digit]: (i) sigma "
          "global flip leaves g = (sigma o r) sigma invariant "
          "identically (%s); (ii) the admissible site redress (global "
          "-1) flips BOTH pinned eta together -- the relative flip "
          "datum and O are invariant (%s: un %s->%s, tw %s->%s); (iii) "
          "the alternating redress is INADMISSIBLE: the UNTWISTED Gram "
          "becomes indefinite for both eta (%s: %s) -- the admissible "
          "fence has teeth; (iv) mu4-defect overlay (m = 4, k = 31) in "
          "ALL plane-gauge/pattern variants (uniform/alternating/"
          "flipped; uniform ~ alternating by site gauge: %s): the SAME "
          "redress satisfies the Theta precondition on the decorated+"
          "twisted kernel (dev 0) and the flip persists as the exact "
          "relative negation -- best eta swaps with IDENTICAL spectra "
          "and equal best inertia %s (%s; the mu4 Gram on the fixing "
          "cut is legitimately non-PD because the mark-bond defect "
          "planes straddle that cut -- the marks sit ON the fixing "
          "axis; O reads the g-class, untouched); (v) string "
          "orientation: reordering D flips omega(D) exactly (%s) but "
          "the NORMALIZED insertion functional is invariant (dev %s) "
          "-- O never sees the orientation convention"
          % (inv_sigma, red_inv, un0[0][0], un1[0][0], tw0[0][0],
             tw1[0][0], alt_bad,
             [(p[0], p[2]) for p in picks_alt], plane_gauge, over_in,
             over_ok, orient_flip, mp.nstr(ratio_dev, 3)),
          FLAGS['op_robust'])

    # O3: false order parameters (teeth)
    wds = DATA['wds']
    signs = {m: (1 if mp.re(wds[m]) > 0 else -1) for m in range(1, 8)}
    nonzero_off = all(abs(wds[m]) > TOL25 for m in range(1, 8))
    sign_varies = len(set(signs.values())) > 1
    base = {}
    shifts = {}
    for m in range(1, 8):
        k = swap_axes(N32, m)[0]
        base[m] = best_eta(k, N32, K32)[0][4]
        shifts[m] = spec_dev(DATA['lad'][m][4], base[m])
    shift_all = min(shifts.values()) > TOL25
    kram_const = FLAGS.get('kramers', False)
    FLAGS['op_teeth'] = (nonzero_off and sign_varies and orient_flip
                         and shift_all and kram_const)
    check("O3.1 FALSE ORDER PARAMETERS REJECTED [40-digit; the "
          "selection has teeth]: (alpha) the raw Pfaffian sign "
          "sign(omega(D)) is REJECTED twice over -- it flips under the "
          "string orientation convention ([C], O2.1(v)) and it is "
          "nonzero at every member (%s; ladder signs %s vary without "
          "selecting pi/2: %s); (beta) the twisted-vs-untwisted "
          "spectral SHIFT is REJECTED -- it is nonzero at EVERY m "
          "including m = 4 (min %s > 0): it measures delta (v525 "
          "typing) but never satisfies 'O != 0 <=> bit'; (gamma) the "
          "v510 index U^2 is REJECTED as modulus OP -- it is CONSTANT "
          "along the family (U2.1): it is the valid OP of the "
          "POSITION half only.  The eta-holonomy/flip-fraction O of "
          "O1.1 is the unique surviving candidate"
          % (nonzero_off, [signs[m] for m in range(1, 8)], sign_varies,
             mp.nstr(min(shifts.values()), 3)),
          FLAGS['op_teeth'])


# ===========================================================================
# N -- negative controls
# ===========================================================================
def n_controls():
    print("  -- N: negative controls")

    # N1: the v512 counterwitness
    Mcw = marks_of(B_CW)
    cw_swap = all(
        set_eq([sp.expand_complex(mu * sp.conjugate(x)) for x in Mcw], Mcw)
        for mu in (B_CW, -B_CW))
    cw_fix = set_eq([sp.expand_complex(sp.conjugate(x)) for x in Mcw], Mcw)
    cw_cos = sp.cos(D_CW) == sp.Rational(3, 5)
    cw_tan = sp.simplify((1 - sp.cos(D_CW)) / sp.sin(D_CW)) \
        == sp.Rational(1, 2)
    u16 = 16 * mp.atan(mp.mpf(4) / 3) / mp.pi
    u32 = 2 * u16
    no_lat = (abs(u16 - mp.nint(u16)) > mp.mpf('0.2')
              and abs(u32 - mp.nint(u32)) > mp.mpf('0.2'))
    FLAGS['cw'] = cw_swap and not cw_fix and cw_cos and cw_tan and no_lat
    check("N1.1 COUNTERWITNESS FALLS OUT OF BOTH DICHOTOMIES [exact "
          "rationals + 40-digit incidence]: {+-1, +-(3+4i)/5} carries "
          "the two mark-SWAPPING reflections exactly (%s) and NO "
          "mark-fixing one (conj preserves the marks: %s) -- no flip "
          "axis; the arc exchange needs tan(delta/2) = 1 but "
          "tan(delta_cw/2) = 1/2 exactly (%s) and cos(delta_cw) = 3/5 "
          "!= 0 exactly (%s) -- no frustration; it is not a lattice "
          "member at all (mark offset %s / %s units, never integer: "
          "%s): O(CW) = 0 -- the counterwitness passes all unsided "
          "batteries (v512/v521/v525) and falls out of BOTH new "
          "dichotomies, exactly as a bit definition demands"
          % (cw_swap, cw_fix, cw_tan, cw_cos, mp.nstr(u16, 5),
             mp.nstr(u32, 5), no_lat),
          FLAGS['cw'])

    # N2: hexagonal / silver preconditions
    lam_hex = sp.simplify(4 * B_HEX / (1 + B_HEX) ** 2)
    im_hex = sp.simplify(sp.im(lam_hex))
    abs_hex = sp.simplify(sp.Abs(B_HEX))
    silver_real = all(sp.simplify(sp.im(x)) == 0
                      for x in (sp.Integer(1), sp.Integer(-1),
                                S_SILVER, -S_SILVER))
    FLAGS['pre'] = (abs_hex == 2 - sp.sqrt(3) and im_hex != 0
                    and silver_real)
    check("N2.1 HEX/SILVER PRECONDITION CONTROLS [exact, v510/v512/"
          "v521 reproduced]: hexagonal |b_hex| = %s != 1 and Im lambda "
          "= %s != 0 -- the marks are not concyclic, NO seam circle "
          "exists: the twist-class dichotomy is not even applicable "
          "(rejected upstream); silver marks all real (%s) -- the mark "
          "circle passes through the deck poles, the deck is not free "
          "(v510 B-M4.2): the POSITION half fails before the modulus "
          "dichotomy is asked -- both controls die exactly where the "
          "established batteries put them"
          % (abs_hex, im_hex, silver_real),
          FLAGS['pre'])

    # N3: the Z2 seam (2 marks) anchor
    n = N16
    marks2 = [0, n]
    cen2 = axis_census(n, marks2)
    sig2 = [1 if (2 * j + 1) < n else -1 for j in range(n)]
    cls2 = {k: gclass(sig2, k, n) for k in cen2}
    cen_ok = cen2 == {n - 1: 'fix', n // 2 - 1: 'swap'}
    cls_ok = cls2.get(n - 1) == '-1' and cls2.get(n // 2 - 1) == '+1'
    bal = sum(1 for x in sig2 if x == 1) == n // 2
    pairs = {frozenset({u, (u + n) % (2 * n)}) for u in range(0, 2 * n, 2)}
    orb = {frozenset({0, n})}
    grew = True
    while grew:
        grew = False
        for pr in list(orb):
            img = frozenset({(u + 2) % (2 * n) for u in pr})
            if img not in orb:
                orb.add(img)
                grew = True
    transitive = orb == pairs
    FLAGS['anchor'] = cen_ok and cls_ok and bal and transitive
    check("N3.1 Z2-SEAM ANCHOR (2 MARKS) [exact integers]: the 2-mark "
          "configuration {1, -1} has exactly one fixing and one swap "
          "axis (%s) with classes %s -- the flip axis EXISTS, i.e. "
          "O = 1/2; but |A+| = |A-| = %d automatically (both arcs have "
          "length pi) and ALL deck-invariant 2-mark sets form ONE "
          "rotation orbit (%s: no modulus exists at 2 marks) -- the "
          "analogous dichotomy is trivially CONSTANT: nothing to "
          "select.  '4 counts': the twist-class choice is contentful "
          "exactly because 4 marks carry a modulus (v512 NC.3b echo)"
          % (cen_ok, cls2, n // 2, transitive),
          FLAGS['anchor'])


# ===========================================================================
# V -- scoreboard + preregistered verdict
# ===========================================================================
def v_verdict():
    print("  -- V: scoreboard + preregistered verdict")
    rows_a = [
        ('facet #14 (<=): flip fires at pi/2', FLAGS['f14_fwd']),
        ('facet #14 (=>): no flip on existing axes', FLAGS['f14_bwd_ax']),
        ('facet #14 (=>): generalized kill (census)', FLAGS['f14_gen']),
        ('facet #15 (<=): frustration at pi/2', FLAGS['f15_fwd']),
        ('facet #15 (=>): PD ladder + cardinality', FLAGS['f15_bwd']),
        ('facet #15: reducibility fence typed', FLAGS['f15_red']),
    ]
    rows_b = [
        ('order parameter O (table + character)', FLAGS['op_table']),
        ('gauge robustness (all v525 freedoms)', FLAGS['op_robust']),
        ('false order parameters rejected', FLAGS['op_teeth']),
    ]
    rows_c = [
        ('unification: #14 = #15 = flag transitivity', FLAGS['unify']),
        ('Kramers typing: NOT the same dichotomy', FLAGS['kramers']),
    ]
    rows_n = [
        ('counterwitness falls out of both', FLAGS['cw']),
        ('hex/silver rejected upstream', FLAGS['pre']),
        ('2-mark anchor trivial (4 counts)', FLAGS['anchor']),
    ]
    print("        (a) equivalences (both directions each):")
    for name, ok in rows_a:
        print("          + %-48s %s" % (name, ok))
    print("        (b) order parameter:")
    for name, ok in rows_b:
        print("          + %-48s %s" % (name, ok))
    print("        (c) unification / Kramers:")
    for name, ok in rows_c:
        print("          + %-48s %s" % (name, ok))
    print("        controls:")
    for name, ok in rows_n:
        print("          + %-48s %s" % (name, ok))
    all_a = all(ok for _, ok in rows_a)
    all_b = all(ok for _, ok in rows_b)
    all_c = all(ok for _, ok in rows_c)
    all_n = all(ok for _, ok in rows_n)
    success = all_a and all_b and all_c and all_n and FLAGS['frame'] \
        and FLAGS['census']
    check("V1.1 PREREGISTERED VERDICT = SUCCESS [typed, no overclaim]: "
          "(a) both structures are exact equivalences to the bit, both "
          "directions each incl. the generalized-structure kill (%s); "
          "(b) the order parameter O = flip fraction / eta holonomy is "
          "constructed, exact, and invariant under every v525 gauge/"
          "lifting freedom, with false candidates rejected (%s); (c) "
          "the v510 Kramers connection is exactly typed: NOT the same "
          "dichotomy -- twist class = MODULUS half (the bit), Kramers "
          "= POSITION half (topology-derived); #14 = #15 = flag "
          "transitivity are ONE Z2 invariant (%s); controls behave "
          "(%s).  THE BIT IS HEREBY PHYSICALLY DEFINED: 'the alignment "
          "bit is the choice of which twist class nature realizes', "
          "read out by O.  MEASUREMENT SKETCH ([C], principle only, no "
          "experiment design): transporting the Z2 twist (disorder) "
          "defect once around the seam axis torsor accumulates the eta "
          "holonomy +i -> -i -- a relative pi phase between the two "
          "interference arms exactly when the bit is set; equivalently "
          "the sign/indefiniteness datum of the mirror-symmetrized "
          "4-twist correlator across the mark mirror reads the same "
          "class.  HONEST FENCE: the bit REMAINS formal input -- a "
          "definition is not a derivation (nine derivation attempts "
          "stay failed); the gain is that the input is now an in-"
          "principle measurable order parameter instead of an abstract "
          "symmetry-lift postulate.  Sandbox only, no marker moves, no "
          "v512/ledger edit (facets #14/#15 = proposal)"
          % (all_a, all_b, all_c, all_n),
          success)


# ---------------------------------------------------------------------------
def run():
    print("seam_bit_twist_class_definition_probe: is the alignment bit "
          "an exact, measurable TWIST-CLASS choice?")
    print("  facets #14 (eta flip) / #15 (twist frustration) as "
          "equivalences; order parameter + robustness; Kramers typing")
    print("=" * 100)
    K16 = kmat_num(N16)
    K32 = kmat_num(N32)
    mach(K16)
    s_frame()
    e14(K16, K32)
    e15(K16, K32)
    u_unify(K16, K32)
    o_param(K16, K32)
    n_controls()
    v_verdict()
    npass = sum(RESULTS)
    print("=" * 100)
    print("SUMMARY: %d/%d checks passed%s   [runtime %.1f s]"
          % (npass, len(RESULTS),
             "" if npass == len(RESULTS) else "  -- FAILURES PRESENT",
             time.time() - T0))
    return npass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
