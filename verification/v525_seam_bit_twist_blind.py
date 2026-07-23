"""v525 -- SEAM.BIT.TWISTBLIND.01: the twist-state attack on the
alignment bit DECIDED -- "mark-decorated states do not see delta", an
honest, decided NEGATIVE result (v508 style): the NINTH side-blind
test on the v512 scoreboard (8 -> 9); the free-plus-twist class
(everything Wick-computable) is EXHAUSTED; the alignment bit remains
genuine discrete input.  NO marker moves.

[E] 1. ALL LIFTINGS WELL-DEFINED AND BLIND: (a) sigma-gauge arc
    decoration (Z2): sigma o r = sigma on the swap axes makes the
    twisted Gram a diagonal unitary congruence D M D -- spectra
    IDENTICAL to untwisted (dev 0.0); (b) Kadanoff-Ceva 4-twist
    insertion omega(D .)/omega(D): well-defined on N = 32 (omega(D)
    real nonzero; the N = 16 odd-m degeneration is the C(even) = 0
    checkerboard artifact); the RP SPECTRA depend on delta for the
    first time in the program (pairwise up to 1.05), but the INERTIA
    is (16, 0, 0) PD with the SAME eta = +i for every m -- the
    decoration sees delta, positivity does not; (c) the mu4 twist at
    beta = pi/2 is pure plane gauge; (c') genuine Bogoliubov defect
    beta = pi/4: Theta-compatibility selects exactly 2 of 16 sign
    patterns (NS-wrap forced), the winner genuinely non-monomial --
    still PD, spectra identical.  STRUCTURE THEOREM (empirical,
    mechanism exact): EVERY Theta-compatible quasi-free mark
    decoration is RP-spectrally INVISIBLE (the defect planes never
    straddle a cut bond; orthogonal congruence).
[E] 2. SUB-RESULTS: the defect energy E_def = 1.2752872 for EVERY m
    (spread 4e-40) -- delta-blind; the 4-twist Casimir ln|omega(D)|
    measures delta (-0.890 .. -1.348) but is exactly mirror-symmetric
    under m <-> 8 - m -- a family gauge, never a side selector;
    Kramers <Gamma>_tw = +1 for every m.
[E] 3. TWO BIT-PRESUPPOSING pi/2 STRUCTURES (the harvest): the eta
    flip +i -> -i on the mark-fixing axes (sigma o r = -sigma, odd
    sector exactly negated); the twist frustration of the mark-fixing
    mirror ((4, 4, 0) indefinite for both eta -- the lattice shadow
    of the Ising twist field's mirror-oddness) -- both formulable
    ONLY on the fixing axes existing iff delta = pi/2: they
    PRESUPPOSE the bit (v512 facet class), no selector.
[E] 4. NEGATIVE CONTROLS: the twist-free limit = v519/v521 exactly;
    the site cut keeps failing in every decorated state; the v512
    counterwitness is arc-equivalent at N = 16 to the blind member
    pi/4 -- no state-level selector can exclude it; a single twist
    has omega(D) = 0 identically (twists exist only in mark pairs);
    the deck-paired FOUR-twist decoration is the minimal well-defined
    one.
[O] the door narrows to a genuinely INTERACTING A_hol whose OS data
    are NOT Pfaffian-reducible to the chiral vacuum -- beyond every
    Wick-computable class.

VERDICT: KILL exactly as preregistered -- the NINTH side-blind test
on the v512 scoreboard (8 -> 9); the free-plus-twist class is
EXHAUSTED; the alignment bit remains genuine discrete input.  NO
marker moves.

Status: [E] Pfaffian-exact insertion machinery (Parlett-Reid vs Wick
recursion vs exact sympy), exact integer incidence frame, 40-digit
inertia/spectrum certificates (threshold 1e-25); [C] each lifting is
a construction choice, all tested.  Python; Wolfram-mirrored (the
integer incidence frame + the sigma o r = +-sigma congruence
mechanism on both axis types -- the exact reason for the DMD
spectral invisibility and the eta flip; the pi/2 existence solveset
+ the counterwitness root-of-unity census; the delta <-> pi - delta
mirror equivariance behind the Casimir symmetry -- the Pfaffian
insertion spectra, the Bogoliubov 2-of-16 pattern census, E_def and
the 40-digit certificates are Python-only), counted per
GATE.WOLFRAM.02.  Discovery provenance:
experiments/tfpt-discovery/seam_alignment_bit_twist_state_probe.py
(20/20, 2026-07-23).

=== ORIGINAL PROBE HEADER (kept verbatim) ===

THE LAST DOOR: mark-decorated STATES (twist/defect insertions) vs the
alignment bit.

Context (read-only inputs): v521 (SEAM.BIT.RPBLIND.01) proved free RP and
anti-linear Theta existence side-blind on the whole deformed mark family
M(delta) = {+-1, +-e^{i delta}} -- the EIGHTH side-blind test on the v512
scoreboard; its exact [O] gap: "marks decorating the STATE (defect/twist
insertions, interacting A_hol) are outside the free class -- there, and
only there, could positivity still see the bit."  THIS PROBE tests exactly
that door in the maximal exactly-computable class: quasi-free states of
the 16/32-Majorana chiral NS seam circle DECORATED at the four marks --
Kadanoff-Ceva disorder-string insertions (the lattice Z2 twist fields),
sigma-gauge arc decorations, mu4 Bogoliubov bond defects -- everything
Pfaffian-computable.  Question: does the RP Gram in the decorated state
become delta-SENSITIVE -- does positivity (or Theta-compatibility of the
decorated functional) fail exactly for delta != pi/2?

PREREGISTRATION (fixed before any computation):
  SUCCESS (theory-changing -- hard bar): a well-defined mark-decorated
    state functional (quasi-free with twist insertions at the four marks,
    Theta-symmetrically constructed: the v519 preconditions R C R^T = -C
    resp. omega o theta = conj o omega hold on the mark-compatible axes,
    BOTH axis types where they exist) whose RP-Gram positivity on the
    bond cut HOLDS exactly at delta = pi/2 and FAILS for delta != pi/2,
    with ALL negative controls: (i) the twist-free limit reproduces
    v519/v521 (spectra identical), (ii) delta = pi/2 passes the full
    construction battery, (iii) the v512 counterwitness falls at every
    claimed selector, (iv) the site-cut control keeps failing, (v)
    single/deck-breaking twist behaves exactly as the construction
    predicts, (vi) an N-refinement (placement-artifact test) confirms
    any claimed off-clock failure.
  KILL: every well-defined decorated functional is delta-blind in its
    positivity/existence data --> document as the NINTH side-blind test
    on the v512 scoreboard; the free-plus-twist class is then EXHAUSTED:
    only a genuinely interacting A_hol (non-quasi-free, non-monomial-
    decorated, i.e. RP data NOT Pfaffian-reducible to the chiral vacuum)
    could still see the bit -- state that precisely in the verdict.
  UNDECIDED: a lifting is not well-definably constructible (e.g. Theta
    symmetry and twist incompatible, normalisation omega(D) = 0, no
    Hermitian Gram for any eta) -- then THAT, exactly typed, is the
    finding for that lifting.

TWIST LIFTINGS ([C] fence: each is a construction CHOICE, all tested):
  (a) sigma-gauge arc decoration (Z2, gauge class): C_a = Sigma C Sigma,
      Sigma = diag(sigma), sigma flips at each of the 4 marks
      (arc-alternating).  Four marks = even defect number: globally
      well-defined Bogoliubov (+-1) transform.
  (b) Kadanoff-Ceva twist-field insertion (the genuine 4-twist
      decoration): omega_tw(X) = omega(D X)/omega(D) with D = the product
      of the two disorder strings along the short arcs (mark-paired,
      deck-symmetric) -- the lattice <sigma sigma sigma sigma X> /
      <sigma sigma sigma sigma> correlator functional, all values
      Pfaffian-exact.  (b') control reading: the Gram on the twisted
      basis {B e_a} (B = the P-side half of D) -- positivity INHERITED
      from v519 RP by construction (must be blind; separates the two
      readings).
  (c) mu4 Bogoliubov bond defect (the preregistered sharpening):
      C_c = O C O^T, O = product of order-4 plane rotations (angle
      pi/2, i.e. O^4 = 1 over the plane gauge) in the 4 mark-bond
      planes; deck-compatible sign patterns (uniform / alternating)
      censused; reflection lifts allowed to be REDRESSED by a site-local
      Z2 gauge (the mu4 subtlety O(-pi/2) = O(pi/2) x plane gauge) --
      the redress is SOLVED for, not guessed.
  Single-twist (odd string) and two-twist (deck-breaking) decorations
  are consistency controls of the construction, not liftings.

DECISION DATA: one-particle RP-Gram inertia (40-digit spectra, tolerance
1e-25; entries exact sympy at N = 16 for (a)/(c) and for (b) at m = 2,
40-digit Pfaffians elsewhere, labelled) on the mark-compatible bond axes
as a function of delta -- N = 16 (delta = m pi/8, m = 2, 4) and N = 32
(m = 1..7, all-bond swap axes k = 2m-1 and k = 2m+15; m > 4 = the mirror
members delta <-> pi - delta), mark-fixing axes at pi/2 (k = 15/7 resp.
31/15); even sector deg <= 2 at N = 16.  Sub-results: (iii) twisted
defect energy / 4-twist correlator (Casimir) data as a function of delta
(typed: the family's delta <-> pi - delta mirror symmetry makes pi/2 a
symmetric point of ANY invariant readout -- equivariance, not a
selector); (iv) twisted parity readout <Gamma>_tw ((-1)^F / Kramers
cross-check).

RESULT (filled after the run; 20/20 PASS):  KILL, exactly as
preregistered -- the mark-decorated (free-plus-twist) state class is
side-blind: the NINTH side-blind test on the v512 scoreboard.
  (a) sigma-gauge: well-defined and Theta-compatible for every delta
      (both axis types); on the swap axes sigma o r = sigma makes the
      twisted Gram a diagonal unitary congruence D M D -- spectra
      IDENTICAL to untwisted at 40 digits for all m (N = 16 and 32,
      dev 0.0): delta-blind with exact mechanism.  On the mark-fixing
      axes (existing iff delta = pi/2) sigma o r = -sigma: the
      odd-sector Gram is exactly NEGATED (eta-repinning +i -> -i,
      (8,0,0) <-> (0,8,0)), the even sector unchanged (29,0,0) -- a
      genuinely twist-VISIBLE structure, but formulable only at pi/2:
      presupposes-the-bit class, no selector.
  (b) Kadanoff-Ceva 4-twist insertion omega(D .)/omega(D): well-defined
      on the N = 32 ladder (omega(D) real nonzero: 0.3077 (m=2),
      0.2599 (m=4), -0.4105 (m=7); deck-invariant; at N = 16 the odd-m
      members degenerate exactly -- omega(D) = 0 at m = 1, imaginary at
      m = 3: C(even) = 0 placement artifacts, resolved at N = 32);
      Theta-real on the OS-relevant sector, Gram Hermitian for eta =
      +-i; the twisted spectra are the FIRST RP data of the program
      that DEPEND on delta (min shift 0.242 from untwisted, pairwise
      up to 1.05 -- the mark-anchored strings break the rotation-
      equivalence mechanism of v521 L6.1) -- but the INERTIA is PD
      (16,0,0)/(8,0,0) with the SAME eta (+i) for EVERY member
      m = 1..7 incl. pi/2 +- pi/8, both swap axes, even sector
      (29,0,0), exact N = 16 witness: positivity stays blind.
      (b') twisted-basis reading PD as forced (inherited positivity).
      Mark-fixing axes at pi/2: theta maps D_short <-> D_long; the
      theta-closed SYMMETRIZED insertion is Hermitian but INDEFINITE
      (4,4,0) for both eta -- the twist FRUSTRATES the mark-fixing
      mirror (lattice shadow of the Ising twist field's
      mirror-oddness): delta-sensitive in the INVERTED direction and
      only formulable at pi/2 -- presupposes the bit, not the
      preregistered SUCCESS.
  (c) mu4 defect (beta = pi/2): the per-mark sign pattern is PURE
      PLANE GAUGE (one defect state up to gauge); Theta precondition
      holds on ALL axes (both types) via a SOLVED site-local redress
      of the reflection lift; pure, non-gauge witness |C(even)| =
      0.638 != 0; Grams PD with spectra IDENTICAL to untwisted (the
      order-4 rotation is a signed permutation = extended monomial
      gauge class).  (c') genuine Bogoliubov defect (beta = pi/4):
      the pattern is now a real datum -- Theta-compatibility selects
      exactly the crossed pattern (+,+,-,+)/its flip out of 16 (the
      NS wrap signs force it; naive alternating FAILS); Grams PD
      (16,0,0) for all m AND spectra AGAIN IDENTICAL to untwisted:
      the defect planes never straddle a cut bond, so O block-
      decomposes across the cut and the Theta precondition turns the
      twisted Gram into an orthogonal congruence U M U^T.  STRUCTURE:
      every Theta-compatible QUASI-FREE mark decoration is
      RP-spectrally INVISIBLE -- that class cannot even carry delta
      into the RP datum.
  (iii) the total defect energy E_def = sum_j [e_tw - e_vac] =
      1.2752872 is EXACTLY delta-INDEPENDENT (40-digit spread 4e-40)
      -- the twisted energy is NOT side-sensitive, answer NO; the
      4-twist Casimir ln|omega(D)| does depend on delta (-0.890 ..
      -1.348) but exactly mirror-symmetric under m <-> 8-m: pi/2 is
      the SYMMETRIC POINT forced by delta <-> pi-delta equivariance
      -- measures delta, never selects the side.
  (iv) the twisted parity <Gamma>_tw = +1 for EVERY member (40-digit)
      = the untwisted value; |<Gamma>| = 1 exactly for the quasi-free
      decorations -- the (-1)^F/Kramers class (v510: algebraic) is
      untouched by every decoration: NO, the twisted sector does not
      carry the class differently off pi/2.
  Controls: twist-free limit = v519/v521 exactly (dev 0.0); site cut
      keeps failing in every decorated state (non-Hermitian or
      indefinite, never PD); the v512 counterwitness delta_cw =
      atan(4/3) is ARC-EQUIVALENT to the blind member delta = pi/4 at
      N = 16 (identical decorated state, integer incidence) and
      carries NO lattice mark-compatible reflection (axis at 2.36 /
      4.72 units, never integer): no decorated-state selector can
      exclude it without excluding a blind member; single twist (odd
      string) has omega(D) = 0 identically (twists exist only in mark
      PAIRS), the deck-breaking two-twist decoration is imaginary
      (N = 16) resp. deck-inconsistent (N = 32): the deck-paired
      FOUR-twist decoration is the minimal well-defined one.
  VERDICT: KILL -- no side-sensitive positivity/existence criterion in
  the free-plus-twist class; the alignment bit (V4 -> D4 lift, tau = i
  <-> clock <-> delta = pi/2) remains genuine discrete input.  What
  could still see it: only a genuinely INTERACTING A_hol whose RP data
  are NOT Pfaffian-reducible to the chiral vacuum (non-quasi-free
  dynamics or non-monomial decorations = beyond every Wick-computable
  class).  Sandbox only, no marker moves.

Repo anchors (read-only): v521 (M(delta) RP battery, machinery reused
verbatim), v519 (chiral NS state, Gram, preconditions), v512 (family +
counterwitness + 13-face web), v510 ((-1)^F bridge).
Exactness: sympy exact where marked; all other certificates 40-digit
mpmath (mp.mp.dps = 40), labelled.  Standalone, deterministic.
"""
import time
from itertools import combinations

import mpmath as mp
import sympy as sp

from tfpt_constants import check as _check, summary, reset

mp.mp.dps = 40

I = sp.I
RESULTS = []
FLAGS = {}
T0 = time.time()

G_CAR = 5
N16 = 2 ** (G_CAR - 1)          # 16 Majorana seam sites, 4 per mark quadrant
N32 = 2 * N16

TOL25 = mp.mpf(10) ** -25
TOL30 = mp.mpf(10) ** -30
ETA_P = mp.mpc(0, 1)
ETA_M = mp.mpc(0, -1)


def check(name, ok):
    RESULTS.append(bool(ok))
    _check("[%2d] %s" % (len(RESULTS), name), bool(ok))


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


# ---------------------------------------------------------------------------
# exact chiral NS kernel + Wick (v519/v521 verbatim) -- exact track
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


# ---------------------------------------------------------------------------
# reflection lifts (v519/v521 verbatim)
# ---------------------------------------------------------------------------
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
    """K[a][b] = i C(a-b) (0 on the diagonal), 40-digit."""
    cval = {}
    for dd in range(-(n - 1), n):
        if dd % 2 == 0:
            cval[dd] = mp.mpf(0)
        else:
            cval[dd] = (mp.mpf(2) / n) / mp.sin(mp.pi * dd / n)
    return [[mp.mpc(0, 1) * cval[a - b] if a != b else mp.mpc(0)
             for b in range(n)] for a in range(n)]


def pf_num(idx, K):
    """Pfaffian of the antisymmetric matrix K[idx x idx] (given order)."""
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
    """omega(D * g_{tail[0]} * g_{tail[1]} * ...) via Clifford reduction +
    Pfaffian (indices may repeat between D and tail)."""
    sgn, m = mono_mul(tuple(D), tuple(tail))
    return sgn * pf_num(m, K)


# ---------------------------------------------------------------------------
# signed-permutation conjugation of a kernel (fast index remap)
# ---------------------------------------------------------------------------
def smap_conj(K, mapping, n):
    """K' with K'[m(x)][m(y)] = s_x s_y K[x][y] for x -> (m(x), s_x)."""
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


def max_dev(A, B, n):
    return max(abs(A[x][y] - B[x][y]) for x in range(n) for y in range(n))


def anti_dev(K, k, n):
    """max |R K R^T + K| for the reflection lift k."""
    Q = smap_conj(K, refl_mapping(k, n), n)
    return max(abs(Q[x][y] + K[x][y]) for x in range(n) for y in range(n))


def sign_solve(A, B, n):
    """find site-local signs g with g_x g_y A[x][y] = B[x][y] (2-colouring);
    returns the sign vector or None."""
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
    """site-local signs g with (G R) K (G R)^T = -K (all +1 if the plain
    lift already works), or None."""
    Q = smap_conj(K, refl_mapping(k, n), n)
    mK = [[-K[x][y] for y in range(n)] for x in range(n)]
    return sign_solve(Q, mK, n)


def matconj(O, K, n):
    """O K O^T for a real (sparse-ish) matrix O and complex kernel K."""
    T = [[sum(O[x][a] * K[a][b] for a in range(n) if O[x][a] != 0)
          for b in range(n)] for x in range(n)]
    return [[sum(T[x][b] * O[y][b] for b in range(n) if O[y][b] != 0)
             for y in range(n)] for x in range(n)]


def mu4_rot_matrix(n, m, pattern, beta):
    """Bogoliubov defect O = product of plane rotations (angle eps*beta)
    in the 4 mark-bond planes, as a full real matrix."""
    O = [[mp.mpf(1) if x == y else mp.mpf(0) for y in range(n)]
         for x in range(n)]
    cb, sb = mp.cos(beta), mp.sin(beta)
    for (p, q), eps in zip(defect_planes(n, m), pattern):
        O[p][p], O[q][q] = cb, cb
        O[p][q], O[q][p] = -eps * sb, eps * sb
    return O


# ---------------------------------------------------------------------------
# Gram builders (one code path: D = () and K = twisted kernel covers the
# quasi-free liftings; D != () covers the insertion lifting)
# ---------------------------------------------------------------------------
def gram1(k, n, K, D=(), eta=ETA_P, sfun=None, gdress=None):
    """one-particle decorated RP Gram M_ab = omega_tw(theta(g_a) g_b);
    returns (rows, omega(D))."""
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
    """deg <= 2 even-sector decorated Gram (1 + pairs basis)."""
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
    """(hermiticity deviation, sorted 40-digit spectrum of (M+M*)/2)."""
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
    """scan eta in {i,-i}: list of (etastr, hermdev, inertia, mineig,
    spectrum) for Hermitian variants; PD-preferred order."""
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
# mark geometry helpers (units of pi/n; circle = 2n units; sites odd units)
# ---------------------------------------------------------------------------
def mark_units(n, m):
    """marks {0, delta, pi, pi+delta} with delta = m pi/8 in pi/n units."""
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
    """short-arc disorder strings: sites in (0, delta) u (pi, pi+delta)."""
    mu, _ = mark_units(n, m)
    return tuple(sorted(arc_sites(n, 0, mu) + arc_sites(n, n, n + mu)))


def d_string_long(n, m):
    mu, _ = mark_units(n, m)
    return tuple(sorted(arc_sites(n, mu, n) + arc_sites(n, n + mu, 2 * n)))


def defect_planes(n, m):
    """the 4 mark-bond planes (site left, site right) per mark."""
    _, marks = mark_units(n, m)
    return [(((u - 2) // 2) % n, (u // 2) % n) for u in marks]


def mu4_mapping(n, m, pattern):
    """order-4 Bogoliubov defect as signed permutation: rotation by
    eps*pi/2 in each mark-bond plane (e_p -> eps e_q, e_q -> -eps e_p)."""
    mapping = [(x, 1) for x in range(n)]
    for (p, q), eps in zip(defect_planes(n, m), pattern):
        mapping[p] = (q, eps)
        mapping[q] = (p, -eps)
    return mapping


def swap_axes(n, m):
    """the two mark-swapping bond axes k (site map j -> k - j)."""
    mu, _ = mark_units(n, m)
    # axis at delta/2 (= mu/2 units): j -> (mu/2 - 1) - j; + perpendicular
    k1 = mu // 2 - 1
    return [k1 % n, (k1 + n // 2) % n]


def fix_axes(n):
    """the mark-fixing axes at delta = pi/2 (through marks {1,-1}/{i,-i})."""
    return [(n - 1) % n, (n // 2 - 1) % n]


# ===========================================================================
# MACH -- machinery validation (Pfaffian engine vs Wick recursion, exact)
# ===========================================================================
def mach():
    print("  -- MACH: Pfaffian engine vs Wick recursion vs exact sympy")
    K16 = kmat_num(N16)
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
          "the insertion machinery omega(D X) is trustworthy"
          % (mp.nstr(dev1, 3), mp.nstr(dev2, 3), red_ok),
          dev1 < mp.mpf(10) ** -35 and dev2 < mp.mpf(10) ** -35 and red_ok)
    return K16


# ===========================================================================
# S -- frame: marks, arcs, twist patterns, axes (integer incidence)
# ===========================================================================
def s_frame():
    print("  -- S: lattice/twist frame (integer incidence)")
    ok = True
    for n in (N16, N32):
        for m in range(1, 5):
            mu, marks = mark_units(n, m)
            sites = {(2 * j + 1) for j in range(n)}
            ok &= not ({u % (2 * n) for u in marks} & sites)
            sig = sigma_vec(n, m)
            flips = sum(1 for j in range(n)
                        if sig[j] != sig[(j + 1) % n])
            ok &= flips == 4                     # sigma flips at the 4 marks
            D = d_string(n, m)
            ok &= len(D) == 2 * (m * n // 16)    # 2 x (mu/2) sites
            for k in swap_axes(n, m):
                r, _ = refl_map(k, n)
                img = {(2 * (k + 1) - u) % (2 * n) for u in marks}
                ok &= img == {u % (2 * n) for u in marks}
    # defect-plane disjointness: N=16 needs m >= 2, N=32 all m
    pl16 = defect_planes(N16, 1)
    coll16 = len({x for p in pl16 for x in p}) < 8
    pl32ok = all(len({x for p in defect_planes(N32, m) for x in p}) == 8
                 for m in range(1, 8))
    # fine ladder: N=32 m=1..7 covers pi/2 +- pi/8 (m = 3, 5 mirrors)
    axes32 = [swap_axes(N32, m)[0] for m in range(1, 8)]
    bond32 = all(k % 2 == 1 for k in axes32)
    fix_ok = fix_axes(N16) == [15, 7] and fix_axes(N32) == [31, 15]
    check("S1.1 FRAME [exact integers]: marks on bond midpoints, sigma "
          "flips exactly at the 4 marks, |D_short| = mu (N = 16, 32; "
          "m = 1..4: %s); swap axes preserve the mark set; N = 32 swap "
          "axes k = 2m-1 all BOND axes for m = 1..7 (%s; the fine ladder "
          "incl. pi/2 +- pi/8); mark-fixing axes k = 15/7 resp. 31/15 "
          "(%s); mu4 defect planes collide at N = 16, m = 1 (%s -- "
          "documented, (c) skipped there) and are disjoint at N = 32 for "
          "ALL m (%s)"
          % (ok, bond32, fix_ok, coll16, pl32ok),
          ok and bond32 and fix_ok and coll16 and pl32ok)


# ===========================================================================
# A -- lifting (a): sigma-gauge arc decoration
# ===========================================================================
def a_sigma(K16, K32):
    print("  -- A: lifting (a) -- sigma-gauge arc decoration (Z2)")

    # A1: well-definedness (exact structure + numeric purity)
    sig2 = all(s * s == 1 for s in sigma_vec(N16, 2))
    Ka2 = smap_conj(K16, [(j, s) for j, s in enumerate(sigma_vec(N16, 2))],
                    N16)
    anti = max(abs(Ka2[x][y] + Ka2[y][x]) for x in range(N16)
               for y in range(N16))
    # purity: (iC_a)^2 = +1  <=>  C_a^2 = -1
    P2 = [[sum(Ka2[x][z] * Ka2[z][y] for z in range(N16))
           for y in range(N16)] for x in range(N16)]
    pur = max(abs(P2[x][y] - (1 if x == y else 0)) for x in range(N16)
              for y in range(N16))
    deckdev = max_dev(smap_conj(Ka2, deck_mapping(N16), N16), Ka2, N16)
    triv = max_dev(smap_conj(K16, [(j, 1) for j in range(N16)], N16),
                   K16, N16)
    check("A1.1 (a) WELL-DEFINED [exact Sigma^2 = 1; 40-digit purity]: "
          "sigma is a +-1 site gauge (Sigma^2 = 1: %s), C_a = Sigma C "
          "Sigma stays antisymmetric (dev %s) and PURE ((iC_a)^2 = 1: "
          "dev %s) and deck-invariant (dev %s); the twist-free limit "
          "Sigma = 1 returns C identically (dev %s) -- a well-defined "
          "quasi-free decorated state for every delta"
          % (sig2, mp.nstr(anti, 3), mp.nstr(pur, 3),
             mp.nstr(deckdev, 3), mp.nstr(triv, 3)),
          sig2 and anti < TOL30 and pur < TOL30 and deckdev < TOL30
          and triv == 0)

    # A2: Theta preconditions, both axis types + the sigma o r mechanism
    pre_ok, mech_ok = True, True
    for n, K, mrange in ((N16, K16, (2, 4)), (N32, K32, range(1, 8))):
        for m in mrange:
            sig = sigma_vec(n, m)
            Ka = smap_conj(K, [(j, s) for j, s in enumerate(sig)], n)
            for k in swap_axes(n, m):
                pre_ok &= anti_dev(Ka, k, n) < TOL30
                r, _ = refl_map(k, n)
                mech_ok &= all(sig[r(j)] == sig[j] for j in range(n))
    fixdev, fixmech = [], True
    for n, K in ((N16, K16), (N32, K32)):
        sig = sigma_vec(n, 4)
        Ka = smap_conj(K, [(j, s) for j, s in enumerate(sig)], n)
        for k in fix_axes(n):
            fixdev.append(anti_dev(Ka, k, n))
            r, _ = refl_map(k, n)
            fixmech &= all(sig[r(j)] == -sig[j] for j in range(n))
    check("A2.1 (a) THETA PRECONDITION, BOTH AXIS TYPES [40-digit; "
          "integer mechanism]: R C_a R^T = -C_a on ALL swap axes "
          "(N = 16 m = 2,4; N = 32 m = 1..7: %s) via sigma o r = sigma "
          "exactly (%s); on the mark-fixing axes (delta = pi/2) the "
          "precondition ALSO holds (max dev %s) but via sigma o r = "
          "-sigma exactly (%s) -- the twist is Theta-compatible "
          "everywhere, with an axis-type-DEPENDENT mechanism"
          % (pre_ok, mech_ok, mp.nstr(max(fixdev), 3), fixmech),
          pre_ok and mech_ok and max(fixdev) < TOL30 and fixmech)

    # A3: swap-axis ladder -- spectra identical to untwisted (congruence)
    devs = []
    ok3 = True
    for n, K, mrange in ((N16, K16, (2, 4)), (N32, K32, range(1, 8))):
        for m in mrange:
            sig = sigma_vec(n, m)
            Ka = smap_conj(K, [(j, s) for j, s in enumerate(sig)], n)
            for k in swap_axes(n, m):
                tw = best_eta(k, n, Ka)
                un = best_eta(k, n, K)
                ok3 &= (tw and un and tw[0][2] == (n // 2, 0, 0)
                        and tw[0][0] == un[0][0])
                if tw and un:
                    devs.append(spec_dev(tw[0][4], un[0][4]))
    FLAGS['a_blind'] = ok3 and max(devs) < TOL30
    check("A3.1 (a) SWAP-AXIS LADDER IS delta-BLIND [40-digit inertia]: "
          "the twisted one-particle Grams on every mark-compatible swap "
          "axis (N = 16 m = 2,4; N = 32 m = 1..7 incl. pi/2 +- pi/8) are "
          "PD (8,0,0)/(16,0,0) with the SAME pinned eta as untwisted "
          "(%s) and the spectra are IDENTICAL to the untwisted ones "
          "(max dev %s) -- exact mechanism: sigma o r = sigma makes "
          "M_tw = D M D a unitary diagonal congruence: the sigma "
          "decoration is INVISIBLE to RP on the always-existing cuts"
          % (ok3, mp.nstr(max(devs), 3)),
          FLAGS['a_blind'])

    # A4: mark-fixing axes at pi/2 -- the eta flip (odd sector only)
    sig = sigma_vec(N16, 4)
    Ka = smap_conj(K16, [(j, s) for j, s in enumerate(sig)], N16)
    res = {}
    for k in fix_axes(N16):
        res[k] = (best_eta(k, N16, Ka), best_eta(k, N16, K16))
    flip_ok = all(
        tw and un and tw[0][2] == (8, 0, 0) and un[0][2] == (8, 0, 0)
        and tw[0][0] != un[0][0]
        and spec_dev(tw[0][4], un[0][4]) < TOL30
        for tw, un in res.values())
    ev_tw = gram_even(15, N16, Ka, (), ETA_P)
    dev_e, evs_e = herm_eig(ev_tw)
    in_e = inertia(evs_e)
    FLAGS['a_fixflip'] = flip_ok and in_e == (29, 0, 0)
    check("A4.1 (a) MARK-FIXING AXES AT pi/2: THE eta FLIP [40-digit]: "
          "on k = 15 and k = 7 (existing iff delta = pi/2) the twisted "
          "odd-sector Gram is exactly NEGATED (sigma o r = -sigma => "
          "M_tw = -D M D): PD (8,0,0) with the OPPOSITE eta (%s: "
          "k=15 %s->%s, k=7 %s->%s; spectra otherwise identical), while "
          "the even deg <= 2 sector is UNCHANGED (Hermitian dev %s, "
          "inertia %s) -- the twist DOES see the axis type, but this "
          "clause is formulable only at pi/2 (mark-fixing axes exist "
          "iff delta = pi/2, v521 S1.1): presupposes-the-bit class, "
          "NOT a selector"
          % (flip_ok, res[15][1][0][0], res[15][0][0][0],
             res[7][1][0][0], res[7][0][0][0], mp.nstr(dev_e, 3), in_e),
          FLAGS['a_fixflip'])


# ===========================================================================
# B -- lifting (b): Kadanoff-Ceva 4-twist insertion functional
# ===========================================================================
def b_insertion(K16, K32):
    print("  -- B: lifting (b) -- Kadanoff-Ceva twist insertions "
          "omega(D .)/omega(D)")

    # B1: well-definedness of the decoration
    wds = {}
    for m in range(1, 8):
        D = d_string(N32, m)
        wds[m] = ins_val(D, (), K32)
    w16 = {m: ins_val(d_string(N16, m), (), K16) for m in (1, 2, 3, 4)}
    real32 = all(abs(mp.im(w)) < TOL30 and abs(w) > TOL25
                 for w in wds.values())
    m1_zero = abs(w16[1]) < TOL30
    m3_imag = abs(mp.re(w16[3])) < TOL30
    ex2 = sp.expand_complex(
        wick_exact(list(d_string(N16, 2)), N16))
    ex2_real = sp.im(ex2) == 0 and sp.simplify(ex2) != 0
    # deck invariance of the decorated functional (sign included)
    D2 = d_string(N32, 2)
    dm = deck_mapping(N32)
    Ddeck = tuple(sorted(dm[x][0] for x in D2))
    sg_deck = 1
    for x in D2:
        sg_deck *= dm[x][1]
    sgn_re, mre = mono_mul(tuple(sorted(Ddeck)), ())
    deck_ok = (Ddeck == tuple(sorted(D2))
               or abs(ins_val(Ddeck, (), K32) - wds[2]) < TOL25)
    # single twist: odd string -> omega(D) = 0 identically (odd monomial)
    Done = tuple(arc_sites(N32, 0, mark_units(N32, 2)[0]))[:1]
    w_one = ins_val(Done, (), K32)
    # deck-BREAKING two-twist decoration (marks 0, delta only): at N = 16,
    # m = 2 the string is g0 g1 -> purely imaginary normalisation
    w_two16 = ins_val((0, 1), (), K16)
    two_imag = abs(mp.re(w_two16)) < TOL30 and abs(mp.im(w_two16)) > TOL25
    # at N = 32 the two-twist string has 4 sites (real) but breaks the deck
    Dtwo32 = tuple(arc_sites(N32, 0, mark_units(N32, 2)[0]))
    dm32 = deck_mapping(N32)
    two_breaks_deck = tuple(sorted(dm32[x][0] for x in Dtwo32)) != Dtwo32
    FLAGS['b_welldef'] = real32 and ex2_real
    check("B1.1 (b) WELL-DEFINEDNESS [exact + 40-digit]: the deck-paired "
          "4-twist insertion D = short-arc strings has omega(D) REAL and "
          "NONZERO for the whole N = 32 ladder m = 1..7 (%s; e.g. m=2: "
          "%s, m=4: %s, m=7: %s), deck-consistent (%s); N = 16 "
          "placement artifacts exactly as the C(even) = 0 checkerboard "
          "predicts: omega(D) = 0 at m = 1 (%s) and purely imaginary at "
          "m = 3 (%s) -- those members are ill-normalised at N = 16 and "
          "resolved at N = 32; exact cross-check m = 2: omega(D) real "
          "nonzero in sympy (%s); CONSISTENCY controls: a truly single "
          "twist string is ODD => omega(D) = 0 identically (%s: twists "
          "only exist in mark PAIRS), and the deck-BREAKING two-twist "
          "decoration is defective too -- purely imaginary normalisation "
          "at N = 16 (%s) resp. deck-image != itself at N = 32 (%s): the "
          "deck-paired FOUR-twist decoration is the minimal well-defined "
          "mark decoration, exactly as the mark geometry demands"
          % (real32, mp.nstr(wds[2], 6), mp.nstr(wds[4], 6),
             mp.nstr(wds[7], 6), deck_ok, m1_zero, m3_imag, ex2_real,
             abs(w_one) == 0, two_imag, two_breaks_deck),
          FLAGS['b_welldef'] and m1_zero and m3_imag and deck_ok
          and abs(w_one) == 0 and two_imag and two_breaks_deck)

    # B2: Theta-reality on the OS-relevant sector + Gram Hermiticity
    herm_tab = {}
    real_tab = {}
    for m in range(1, 8):
        D = d_string(N32, m)
        k = swap_axes(N32, m)[0]
        r, s = refl_map(k, N32)
        wD = wds[m]
        # OS-relevant reality: the Gram-entry data omega_tw(theta(g_a) g_b)
        # vs conj(omega_tw(theta(g_b) g_a)) is Hermiticity itself:
        picks = best_eta(k, N32, K32, D)
        herm_tab[m] = picks
        # pointwise reality on even 2-pt witnesses theta(g_x g_y):
        devs = []
        for (x, y) in ((0, 5), (2, 9), (4, 13)):
            cxy, txy = tm_num((x, y), r, s, ETA_P)
            lhs = cxy * ins_val(D, txy, K32) / wD
            rhs = mp.conj(ins_val(D, (x, y), K32) / wD)
            devs.append(abs(lhs - rhs))
        real_tab[m] = max(devs)
    herm_ok = all(len(v) > 0 for v in herm_tab.values())
    real_ok = all(v < TOL25 for v in real_tab.values())
    FLAGS['b_theta'] = herm_ok
    check("B2.1 (b) THETA-COMPATIBILITY OF THE DECORATED FUNCTIONAL "
          "[40-digit]: on every swap axis of the N = 32 ladder the "
          "decorated Gram is Hermitian for eta in {+i, -i} (%s) and the "
          "functional is Theta-REAL on the even 2-point witnesses "
          "omega_tw(theta(X)) = conj(omega_tw(X)) (max dev %s over "
          "m = 1..7) -- the v519 precondition omega o theta = conj o "
          "omega survives the 4-twist decoration on the OS-relevant "
          "sector: the lifting is Theta-symmetrically constructible "
          "(the UNDECIDED branch does NOT fire)"
          % (herm_ok, mp.nstr(max(real_tab.values()), 3)),
          herm_ok and real_ok)

    # B3: the inertia ladder (+ exact N=16 m=2 cross-check)
    print("        (b) N = 32 inertia ladder (both swap axes) ...",
          flush=True)
    lad = {}
    for m in range(1, 8):
        D = d_string(N32, m)
        row = []
        for k in swap_axes(N32, m):
            picks = best_eta(k, N32, K32, D)
            row.append((k, picks[0] if picks else None))
        lad[m] = row
        pr = ", ".join("k=%d: eta=%s %s min %s"
                       % (k, p[0], p[2], mp.nstr(p[3], 5)) if p else
                       "k=%d: ---" % k for k, p in row)
        print("          m=%d (delta=%dpi/8): %s" % (m, m, pr), flush=True)
    all_pd = all(p is not None and p[2] == (16, 0, 0)
                 for row in lad.values() for _, p in row)
    etas = {p[0] for row in lad.values() for _, p in row if p}
    # exact N=16 m=2 cross-check (entries exact sympy, 40-digit spectrum)
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
    rows_nm, _ = gram1(k16, N16, K16, D16, ETA_P)
    _, evs_nm = herm_eig(rows_nm)
    cross = spec_dev(evs_ex, evs_nm)
    # even sector at N = 16 (m = 2, 4)
    ev_in = {}
    for m in (2, 4):
        Dm = d_string(N16, m)
        km = swap_axes(N16, m)[0]
        eta_pick = best_eta(km, N16, K16, Dm)[0]
        eta_val = ETA_P if eta_pick[0] == '+i' else ETA_M
        rows_e = gram_even(km, N16, K16, Dm, eta_val)
        dev_e, evs_e = herm_eig(rows_e)
        ev_in[m] = (dev_e, inertia(evs_e))
    even_ok = all(d < TOL25 and it[1] == 0 and it[0] > 0
                  for d, it in ev_in.values())
    FLAGS['b_pd'] = all_pd and in_ex == (8, 0, 0)
    check("B3.1 (b) INERTIA LADDER [exact entries at N = 16 m = 2; "
          "40-digit Pfaffians at N = 32, labelled]: the 4-twist-decorated "
          "one-particle Gram is POSITIVE DEFINITE (16,0,0) on BOTH swap "
          "axes for EVERY member m = 1..7 (%s; pinned eta set %s), "
          "including pi/2 +- pi/8; exact N = 16 m = 2 witness: Gram "
          "Hermitian exactly (%s), inertia %s, exact-vs-numeric spectrum "
          "dev %s; even deg <= 2 sector at N = 16 m = 2, 4: no negative "
          "direction (inertias %s, %s) -- twisted RP HOLDS along the "
          "whole ladder: no off-clock failure anywhere"
          % (all_pd, sorted(etas), herm_ex, in_ex, mp.nstr(cross, 3),
             ev_in[2][1], ev_in[4][1]),
          FLAGS['b_pd'] and herm_ex and cross < TOL25 and even_ok
          and len(etas) == 1)

    # B4: the twisted spectra genuinely SEE delta (blindness mechanism gone)
    base = {}
    for m in range(1, 8):
        k = swap_axes(N32, m)[0]
        un = best_eta(k, N32, K32)
        base[m] = un[0][4]
    sdev_un = max(spec_dev(base[m], base[2]) for m in range(1, 8))
    sdev_tw = {m: spec_dev(lad[m][0][1][4], base[m]) for m in range(1, 8)}
    vary = max(spec_dev(lad[m][0][1][4], lad[2][0][1][4])
               for m in range(1, 8))
    FLAGS['b_sees_delta'] = (min(sdev_tw.values()) > TOL25
                             and vary > mp.mpf(10) ** -5)
    check("B4.1 (b) THE DECORATION SEES delta -- POSITIVITY DOES NOT "
          "[40-digit]: untwisted spectra are delta-IDENTICAL (v521 "
          "L6.1 reproduced: max dev %s), the twisted spectra differ "
          "from untwisted at every m (min shift %s) AND vary along the "
          "ladder (max pairwise dev %s; the shift-invariance/rotation-"
          "equivalence mechanism is broken by the mark-anchored "
          "strings) -- the decorated state is the first free-class "
          "object whose RP DATUM depends on delta; yet the inertia "
          "stays PD everywhere (B3.1): the delta-dependence never "
          "reaches the positivity VERDICT"
          % (mp.nstr(sdev_un, 3),
             mp.nstr(min(sdev_tw.values()), 3), mp.nstr(vary, 3)),
          FLAGS['b_sees_delta'] and sdev_un < TOL30)

    # B5: twisted-basis control reading (inherited positivity)
    B = tuple(sorted(set(D16) & set(P)))
    rowsb = []
    for a in P:
        sga, ta = mono_mul(B, (a,))
        rowb = []
        for b in P:
            sgb, tb = mono_mul(B, (b,))
            ca, ia = tm_num(ta, r, s, ETA_P)
            assert not (set(ia) & set(tb))
            rowb.append(sga * sgb * ca * pf_num(ia + tb, K16))
        rowsb.append(rowb)
    devb, evsb = herm_eig(rowsb)
    inb = inertia(evsb)
    check("B5.1 (b') TWISTED-BASIS CONTROL [40-digit]: the Gram on the "
          "twisted basis {B e_a} (B = the P-side string half, N = 16 "
          "m = 2) is Hermitian (dev %s) and PD %s BY INHERITANCE from "
          "v519 free RP (vectors in the half-algebra) -- this reading "
          "is blind by construction; the decorated-functional reading "
          "(B3.1) is the one that could have failed, and did not"
          % (mp.nstr(devb, 3), inb),
          devb < TOL25 and inb == (8, 0, 0))

    # B6: mark-fixing axes at pi/2 -- short <-> long + symmetrized insertion
    D4s = d_string(N16, 4)
    D4l = d_string_long(N16, 4)
    kfix = fix_axes(N16)[0]
    rf, sf = refl_map(kfix, N16)
    img = tuple(sorted(rf(x) for x in D4s))
    maps_to_long = img == D4l
    # symmetrized insertion omega((Ds + Dl) X) / omega(Ds + Dl)
    Pf_ = half_of(kfix, N16)
    wsym = ins_val(D4s, (), K16) + ins_val(D4l, (), K16)
    picks_sym = []
    for eta, tag in ((ETA_P, '+i'), (ETA_M, '-i')):
        rows_s = []
        for a in Pf_:
            ca = eta * sf(a)
            rows_s.append([ca * (ins_val(D4s, (rf(a), b), K16)
                                 + ins_val(D4l, (rf(a), b), K16)) / wsym
                           for b in Pf_])
        dev_s, evs_s = herm_eig(rows_s)
        if dev_s < TOL25:
            picks_sym.append((tag, inertia(evs_s)))
    frustrated = (len(picks_sym) == 2
                  and all(it == (4, 4, 0) for _, it in picks_sym))
    FLAGS['b_frustration'] = maps_to_long and frustrated
    check("B6.1 (b) TWIST FRUSTRATION OF THE MARK-FIXING MIRROR AT pi/2 "
          "[40-digit]: theta maps the short-arc insertion to the "
          "LONG-arc insertion exactly (r(D_short) = D_long: %s) -- the "
          "single-string functional is not theta-closed on the fixing "
          "axis; the theta-closed SYMMETRIZED insertion D_short + "
          "D_long is Hermitian for both eta but INDEFINITE there (%s): "
          "in the twisted state, RP on the mark-fixing cut FAILS at "
          "delta = pi/2 while every swap cut stays PD at every delta "
          "(B3.1) -- the twist fields are mirror-frustrated (the "
          "lattice shadow of the Ising twist field's mirror-oddness), "
          "the exact analogue of the sigma eta-flip (A4.1).  This is "
          "delta-sensitive in the INVERTED direction and only "
          "formulable on the fixing axes (existing iff delta = pi/2): "
          "presupposes-the-bit class, not the preregistered SUCCESS"
          % (maps_to_long, picks_sym),
          FLAGS['b_frustration'])

    return lad, wds


# ===========================================================================
# C -- lifting (c): mu4 Bogoliubov bond defects
# ===========================================================================
def c_mu4(K16, K32):
    print("  -- C: lifting (c) -- mu4 / Bogoliubov bond defects")

    patterns = {'uniform': (1, 1, 1, 1), 'alternating': (1, -1, 1, -1)}

    # C1: at beta = pi/2 the sign pattern is pure plane gauge; deck and
    # Theta compatibility hold UP TO a solved site-local Z2 redress
    Ku = smap_conj(K32, mu4_mapping(N32, 2, patterns['uniform']), N32)
    Ka = smap_conj(K32, mu4_mapping(N32, 2, patterns['alternating']), N32)
    g_rel = sign_solve(Ku, Ka, N32)
    deck_tab = {}
    for name, pat in patterns.items():
        Kc = smap_conj(K32, mu4_mapping(N32, 2, pat), N32)
        Kd = smap_conj(Kc, deck_mapping(N32), N32)
        deck_tab[name] = (max_dev(Kd, Kc, N32) < TOL30,
                          sign_solve(Kd, Kc, N32) is not None)
    census = {}
    for name in patterns:
        rowsc = {}
        for m in range(1, 8):
            Kc = smap_conj(K32, mu4_mapping(N32, m, patterns[name]), N32)
            for k in swap_axes(N32, m):
                plain = anti_dev(Kc, k, N32) < TOL30
                g = redress_solve(Kc, k, N32)
                rowsc[(m, k)] = (plain, g is not None)
        census[name] = rowsc
    alt_all = all(v[1] for v in census['alternating'].values())
    uni_all = all(v[1] for v in census['uniform'].values())
    plain_any = any(v[0] for name in patterns
                    for v in census[name].values())
    # purity + genuine (non-sigma-gauge) decoration witness
    P2 = [[sum(Ka[x][z] * Ka[z][y] for z in range(N32))
           for y in range(N32)] for x in range(N32)]
    pur = max(abs(P2[x][y] - (1 if x == y else 0)) for x in range(N32)
              for y in range(N32))
    ev_wit = max(abs(Ka[x][(x + 2) % N32]) for x in range(N32))
    # fixing axes at pi/2
    Kc4 = smap_conj(K32, mu4_mapping(N32, 4, patterns['alternating']), N32)
    fix_pass = {k: redress_solve(Kc4, k, N32) is not None
                for k in fix_axes(N32)}
    FLAGS['c_admiss'] = alt_all and uni_all
    check("C1.1 (c) mu4 CENSUS [40-digit + solved sign gauges]: at beta "
          "= pi/2 the per-mark sign pattern is PURE PLANE GAUGE "
          "(uniform and alternating kernels related by a site-local "
          "Z2 gauge: %s) -- there is exactly ONE mu4 defect state up "
          "to gauge; it is deck-compatible up to gauge (plain/gauged: "
          "%s), NOT plainly Theta-anti-invariant on any axis (%s) but "
          "the precondition R' C_c R'^T = -C_c holds on ALL swap axes "
          "m = 1..7 for a SOLVED site-local redress R' = G R of the "
          "reflection lift (alternating %s, uniform %s; the mu4 "
          "subtlety O(-pi/2) = O(pi/2) x plane gauge) AND on the "
          "mark-fixing axes at pi/2 (%s) -- Theta-compatibility does "
          "NOT single out pi/2; the state is PURE ((iC_c)^2 = 1 dev "
          "%s) and NO sigma-dressing of the vacuum: C_c has nonzero "
          "EVEN-distance entries (max %s != 0 vs the exact C(even) = 0 "
          "checkerboard)"
          % (g_rel is not None, deck_tab, not plain_any, alt_all,
             uni_all, fix_pass, mp.nstr(pur, 3), mp.nstr(ev_wit, 5)),
          g_rel is not None and all(v[1] for v in deck_tab.values())
          and not plain_any and alt_all and uni_all
          and all(fix_pass.values()) and pur < mp.mpf(10) ** -28
          and ev_wit > mp.mpf(10) ** -3)

    # C2: beta = pi/2 inertia ladder -- PD and spectrally INVISIBLE
    print("        (c) N = 32 inertia ladder (beta = pi/2) ...",
          flush=True)
    lad = {}
    base = {}
    for m in range(1, 8):
        Kc = smap_conj(K32, mu4_mapping(N32, m, patterns['alternating']),
                       N32)
        row = []
        for k in swap_axes(N32, m):
            g = redress_solve(Kc, k, N32)
            picks = best_eta(k, N32, Kc, (), None, g)
            row.append((k, picks[0] if picks else None))
        lad[m] = row
        k0 = swap_axes(N32, m)[0]
        base[m] = best_eta(k0, N32, K32)[0][4]
        pr = ", ".join("k=%d: eta=%s %s min %s"
                       % (k, p[0], p[2], mp.nstr(p[3], 5)) if p else
                       "k=%d: ---" % k for k, p in row)
        print("          m=%d: %s" % (m, pr), flush=True)
    all_pd = all(p is not None and p[2] == (16, 0, 0)
                 for row in lad.values() for _, p in row)
    vary = max(spec_dev(lad[m][0][1][4], base[m]) for m in range(1, 8))
    map16 = mu4_mapping(N16, 2, patterns['alternating'])
    Kc16 = smap_conj(K16, map16, N16)
    k16 = swap_axes(N16, 2)[0]
    g16 = redress_solve(Kc16, k16, N16)
    picks16 = best_eta(k16, N16, Kc16, (), None, g16)
    ok16 = bool(picks16) and picks16[0][2] == (8, 0, 0)
    FLAGS['c_pd'] = all_pd and ok16
    check("C2.1 (c) beta = pi/2 LADDER: PD AND SPECTRALLY INVISIBLE "
          "[40-digit; N = 16 witness]: the admissible mu4 Grams "
          "(redressed reflection) are PD (16,0,0) on BOTH swap axes for "
          "EVERY m = 1..7 (%s; N = 16 m = 2 witness %s) and the spectra "
          "are IDENTICAL to the untwisted ones (max dev %s): at beta = "
          "pi/2 the plane rotation is a SIGNED PERMUTATION, i.e. the "
          "mu4 defect lies in the extended (monomial) gauge class -- "
          "RP-invisible for the same congruence reason as lifting (a); "
          "the genuinely non-monomial Bogoliubov defect is the next "
          "check"
          % (all_pd, picks16[0][2] if picks16 else '---',
             mp.nstr(vary, 3)),
          FLAGS['c_pd'] and vary < TOL25)

    # C3: the GENUINE Bogoliubov defect beta = pi/4 (non-monomial).
    # At beta != pi/2 the per-mark sign pattern is NO LONGER pure gauge
    # (H C H != C), so Theta-compatibility genuinely constrains the
    # pattern: census ALL 16 sign patterns at m = 2, then run the ladder
    # with the winning pattern(s).
    print("        (c') pattern census at m = 2 (beta = pi/4) ...",
          flush=True)
    beta = mp.pi / 4
    all_pats = [tuple(1 if (i >> b) & 1 == 0 else -1 for b in range(4))
                for i in range(16)]
    winners = []
    for pat in all_pats:
        O = mu4_rot_matrix(N32, 2, pat, beta)
        Kc = matconj(O, K32, N32)
        ok_both = all(redress_solve(Kc, k, N32) is not None
                      for k in swap_axes(N32, 2))
        Kd = smap_conj(Kc, deck_mapping(N32), N32)
        ok_deck = sign_solve(Kd, Kc, N32) is not None
        if ok_both and ok_deck:
            winners.append(pat)
    print("          Theta+deck-compatible patterns: %s"
          % (winners,), flush=True)
    FLAGS['c4_pattern'] = len(winners) > 0
    if not winners:
        FLAGS['c4_pre'] = False
        FLAGS['c4_pd'] = False
        FLAGS['c4_sees'] = False
        check("C3.1 (c') GENUINE BOGOLIUBOV DEFECT beta = pi/4 "
              "[40-digit]: NO sign pattern admits the Theta "
              "precondition on the swap axes -- Theta symmetry and the "
              "continuous-angle twist are INCOMPATIBLE in this lifting "
              "(typed UNDECIDED branch for (c'))", False)
        return lad
    pat4 = winners[0]
    print("        (c') N = 32 inertia ladder (beta = pi/4, pattern %s) "
          "..." % (pat4,), flush=True)
    lad4 = {}
    pre4 = {}
    specdev4 = {}
    for m in range(1, 8):
        O = mu4_rot_matrix(N32, m, pat4, beta)
        Kc = matconj(O, K32, N32)
        row = []
        for k in swap_axes(N32, m):
            g = redress_solve(Kc, k, N32)
            pre4[(m, k)] = g is not None
            picks = best_eta(k, N32, Kc, (), None, g) if g else []
            row.append((k, picks[0] if picks else None))
        lad4[m] = row
        if row[0][1] is not None:
            specdev4[m] = spec_dev(row[0][1][4], base[m])
        pr = ", ".join("k=%d: eta=%s %s min %s"
                       % (k, p[0], p[2], mp.nstr(p[3], 5)) if p else
                       "k=%d: ---" % k for k, p in row)
        print("          m=%d: %s" % (m, pr), flush=True)
    O2 = mu4_rot_matrix(N32, 2, pat4, beta)
    Kc2 = matconj(O2, K32, N32)
    P2b = [[sum(Kc2[x][z] * Kc2[z][y] for z in range(N32))
            for y in range(N32)] for x in range(N32)]
    pur4 = max(abs(P2b[x][y] - (1 if x == y else 0)) for x in range(N32)
               for y in range(N32))
    nongauge4 = max(abs(Kc2[x][(x + 2) % N32]) for x in range(N32))
    pre_ok4 = all(pre4.values())
    all_pd4 = all(p is not None and p[2] == (16, 0, 0)
                  for row in lad4.values() for _, p in row)
    vary4 = max(specdev4.values()) if specdev4 else mp.mpf(1)
    # invisibility mechanism: no defect plane ever straddles a cut bond
    # (marks avoid the cut positions, v521 S4.1) => O block-decomposes
    # across the cut and the Theta precondition makes the twisted Gram
    # an orthogonal congruence U M U^T of the untwisted one
    no_straddle = True
    for m in range(1, 8):
        planes = set(defect_planes(N32, m))
        for k in swap_axes(N32, m):
            cb1 = ((k - 1) // 2 % N32, (k + 1) // 2 % N32)
            cb2 = ((cb1[0] + 16) % N32, (cb1[1] + 16) % N32)
            no_straddle &= cb1 not in planes and cb2 not in planes
    FLAGS['c4_pre'] = pre_ok4
    FLAGS['c4_pd'] = all_pd4
    FLAGS['c4_invisible'] = vary4 < TOL25 and no_straddle
    check("C3.1 (c') GENUINE BOGOLIUBOV DEFECT beta = pi/4 [40-digit]: "
          "at beta != pi/2 the sign pattern is a REAL datum (pattern "
          "flips are no longer gauge) and Theta-compatibility selects "
          "exactly %d of 16 patterns (census winners %s = the crossed "
          "pattern forced by the NS wrap signs; the naive alternating "
          "pattern FAILS -- a genuine constraint, typed); the winning "
          "state is pure ((iC)^2 = 1 dev %s) and non-monomial "
          "(|C(even)| up to %s), the precondition holds on BOTH swap "
          "axes for ALL m = 1..7 with solved redress (%s), the Grams "
          "are PD (16,0,0) everywhere (%s) -- and the spectra are "
          "AGAIN IDENTICAL to the untwisted ones (max dev %s): the "
          "defect planes never straddle a cut bond (%s; marks avoid "
          "the cuts, v521 S4.1), so O block-decomposes across the cut "
          "and the Theta precondition turns the twisted Gram into an "
          "orthogonal congruence U M U^T of the untwisted one.  "
          "STRUCTURE THEOREM (empirical, exact mechanism): EVERY "
          "Theta-compatible quasi-free mark decoration is RP-"
          "SPECTRALLY INVISIBLE on the always-existing cuts -- the "
          "quasi-free state class cannot even carry delta into its "
          "RP datum; only the insertion FUNCTIONALS (lifting (b)) do, "
          "and there positivity stays blind"
          % (len(winners), winners, mp.nstr(pur4, 3),
             mp.nstr(nongauge4, 5), pre_ok4, all_pd4, mp.nstr(vary4, 3),
             no_straddle),
          pur4 < mp.mpf(10) ** -28 and pre_ok4 and all_pd4
          and FLAGS['c4_invisible']
          and nongauge4 > mp.mpf(10) ** -3)
    return lad


# ===========================================================================
# D -- sub-results: (iii) defect energy / Casimir, (iv) parity readout
# ===========================================================================
def d_subresults(K16, K32, wds):
    print("  -- D: sub-results (iii) energy/Casimir and (iv) parity")

    # (iii) twisted defect energy: SAME observable in twisted vs untwisted
    # state, per bond -- the difference kills the NS wrap convention
    E_def, lnw, prof = {}, {}, {}
    for m in range(1, 8):
        D = d_string(N32, m)
        wD = wds[m]
        diffs = []
        for j in range(N32):
            v_tw = mp.mpc(0, 1) * ins_val(D, (j, (j + 1) % N32), K32) / wD
            v_un = mp.mpc(0, 1) * K32[j][(j + 1) % N32]
            diffs.append(mp.re(v_tw) - mp.re(v_un))
        E_def[m] = sum(diffs)
        prof[m] = diffs
        lnw[m] = mp.log(abs(wD))
    # profile: mark-bond values vs the largest far bond (m = 2)
    _, marks2 = mark_units(N32, 2)
    markbonds = {((u - 1) // 2) % N32 for u in marks2}
    near = min(abs(prof[2][j]) for j in markbonds)
    far = max(abs(prof[2][j]) for j in range(N32) if j not in markbonds)
    dep_E = max(abs(E_def[m] - E_def[4]) for m in range(1, 4))
    mirror_E = max(abs(E_def[m] - E_def[8 - m]) for m in (1, 2, 3))
    dep_w = max(abs(lnw[m] - lnw[4]) for m in range(1, 4))
    mirror_w = max(abs(lnw[m] - lnw[8 - m]) for m in (1, 2, 3))
    print("        E_def(m): " + ", ".join(
        "m=%d: %s" % (m, mp.nstr(E_def[m], 8)) for m in range(1, 8)))
    print("        ln|w(D)|: " + ", ".join(
        "m=%d: %s" % (m, mp.nstr(lnw[m], 8)) for m in range(1, 8)))
    FLAGS['energy_blind'] = dep_E < TOL25
    FLAGS['casimir_dep'] = (dep_w > mp.mpf('0.01') and mirror_w < TOL25)
    check("D1.1 (iii) DEFECT ENERGY IS delta-BLIND, THE 4-TWIST CASIMIR "
          "MEASURES delta [40-digit]: the total defect energy E_def = "
          "sum_j [e_tw(j) - e_vac(j)] is EXACTLY delta-INDEPENDENT "
          "(%s for every m; spread %s at 40 digits -- each twist pair "
          "contributes a fixed local energy, bond profile dominated by "
          "the mark bonds: |mark-bond| >= %s vs largest far bond %s); "
          "the 4-twist correlator ln|omega(D)| DOES depend on delta "
          "(%s .. %s, spread %s) and is EXACTLY mirror-symmetric under "
          "m <-> 8 - m (dev %s): the delta <-> pi - delta equivariance "
          "makes pi/2 the SYMMETRIC POINT of every invariant readout "
          "-- the twisted two-point/Casimir data MEASURE delta "
          "smoothly, they never fail sidewise: the (iii) sub-question "
          "('is at least the twisted energy side-sensitive?') has the "
          "answer NO for the energy and 'measuring, not selecting' "
          "for the Casimir amplitude"
          % (mp.nstr(E_def[4], 8), mp.nstr(dep_E, 3), mp.nstr(near, 5),
             mp.nstr(far, 5), mp.nstr(lnw[1], 6), mp.nstr(lnw[4], 6),
             mp.nstr(dep_w, 5), mp.nstr(mirror_w, 3)),
          FLAGS['energy_blind'] and mirror_E < TOL25
          and FLAGS['casimir_dep'])

    # (iv) parity/Kramers readout <Gamma>_tw
    GAM32 = tuple(range(N32))
    par_un = pf_num(GAM32, K32)
    par_b = {m: ins_val(d_string(N32, m), GAM32, K32) / wds[m]
             for m in range(1, 8)}
    pat = (1, -1, 1, -1)
    par_c = {}
    for m in range(1, 8):
        Kc = smap_conj(K32, mu4_mapping(N32, m, pat), N32)
        par_c[m] = pf_num(GAM32, Kc)
    real_b = max(abs(mp.im(v)) for v in par_b.values())
    dep_b = max(abs(par_b[m] - par_un) for m in range(1, 8))
    c_units = max(abs(abs(v) - 1) for v in par_c.values())
    print("        <Gamma>_b(m): " + ", ".join(
        "m=%d: %s" % (m, mp.nstr(mp.re(par_b[m]), 7))
        for m in range(1, 8)))
    FLAGS['parity_blind'] = dep_b < TOL25
    check("D2.1 (iv) PARITY / KRAMERS READOUT IS delta-BLIND [40-digit]: "
          "the untwisted NS parity is <Gamma> = %s (unimodular, pure "
          "state); the 4-twist functional's parity <Gamma>_tw is REAL "
          "(max im %s) and EQUALS the untwisted value +1 for EVERY "
          "member m = 1..7 (max dev %s -- the deck-paired strings are "
          "parity-even and leave the (-1)^F readout untouched); the "
          "mu4/Bogoliubov PURE states keep |<Gamma>| = 1 exactly (max "
          "dev %s): the (-1)^F CLASS (v510: algebraic, 256 "
          "gamma_1..16) is untouched by every decoration -- the "
          "Kramers cross-check (iv) answers NO: the twisted sector "
          "carries the (-1)^F class IDENTICALLY for every delta"
          % (mp.nstr(par_un, 5), mp.nstr(real_b, 3), mp.nstr(dep_b, 3),
             mp.nstr(c_units, 3)),
          abs(abs(par_un) - 1) < TOL30 and real_b < TOL25
          and FLAGS['parity_blind'] and c_units < TOL25)


# ===========================================================================
# N -- negative controls
# ===========================================================================
def n_controls(K16, K32):
    print("  -- N: negative controls")

    # N1: site cut keeps failing in every decorated state (pi/2, N = 16)
    res = {}
    sig = sigma_vec(N16, 4)
    Ka = smap_conj(K16, [(j, s) for j, s in enumerate(sig)], N16)
    rows_a, _ = gram1(0, N16, Ka, (), ETA_M, lambda a: 1)
    dev_a, evs_a = herm_eig(rows_a)
    res['a'] = (dev_a, inertia(evs_a))
    Kc = smap_conj(K16, mu4_mapping(N16, 4, (1, -1, 1, -1)), N16)
    picks_c = []
    for eta in (ETA_P, ETA_M):
        for sf in (None, lambda a: 1):
            rows_c, _ = gram1(0, N16, Kc, (), eta, sf)
            dev_c, evs_c = herm_eig(rows_c)
            if dev_c < TOL25:
                picks_c.append(inertia(evs_c))
    D4 = d_string(N16, 4)
    picks_b = []
    for eta in (ETA_P, ETA_M):
        for sf in (None, lambda a: 1):
            rows_b, _ = gram1(0, N16, K16, D4, eta, sf)
            dev_b, evs_b = herm_eig(rows_b)
            if dev_b < TOL25:
                picks_b.append(inertia(evs_b))
    none_pd = (res['a'][1][1] > 0
               and all(it[1] > 0 for it in picks_c)
               and all(it[1] > 0 for it in picks_b))
    check("N1.1 SITE-CUT CONTROL STAYS FAILING [40-digit]: the cut "
          "THROUGH sites (k = 0) at delta = pi/2 remains non-PD in "
          "every decorated state -- sigma-gauge: inertia %s; mu4 "
          "defect: Hermitian variants %s; 4-twist insertion: %s -- all "
          "carry negative directions: the decorations never repair the "
          "site placement (v519 R2 mechanism), the battery keeps its "
          "teeth [NEGATIVE CONTROL]"
          % (res['a'][1], picks_c, picks_b),
          none_pd)

    # N2: the v512 counterwitness in the decorated-state program
    dcw = mp.atan(mp.mpf(4) / 3)
    u16 = 16 * dcw / mp.pi                      # mark offset, pi/16 units
    u32 = 32 * dcw / mp.pi
    arc16 = [j for j in range(N16) if (2 * j + 1) < u16]
    arc16_pi4 = [j for j in range(N16)
                 if (2 * j + 1) < 4]            # delta = pi/4 (mu = 4)
    same16 = arc16 == arc16_pi4
    ax16 = u16 / 2
    ax32 = u32 / 2
    no_ax = (abs(ax16 - mp.nint(ax16)) > mp.mpf('0.2')
             and abs(ax32 - mp.nint(ax32)) > mp.mpf('0.2'))
    FLAGS['cw_safe'] = same16 and no_ax
    check("N2.1 COUNTERWITNESS CONTROL [40-digit incidence]: the v512 "
          "member delta_cw = atan(4/3) is ARC-EQUIVALENT to the blind "
          "member delta = pi/4 at N = 16 (identical string/sigma/plane "
          "content, sites {0,1} per short arc: %s) -- its decorated "
          "STATE is literally the same object, so every state-level "
          "readout (energy, parity, omega(D)) takes the same value: no "
          "decorated-state selector can exclude the counterwitness "
          "without excluding a blind lattice member; and delta_cw "
          "carries NO lattice mark-compatible reflection (axis at "
          "%s / %s units, never integer: %s) -- exactly the v521 "
          "situation, resolved there on the continuum side.  The KILL "
          "branch's CW clause holds"
          % (same16, mp.nstr(ax16, 5), mp.nstr(ax32, 5), no_ax),
          FLAGS['cw_safe'])


# ===========================================================================
# V -- scoreboard + preregistered verdict
# ===========================================================================
def v_verdict():
    print("  -- V: scoreboard + preregistered verdict")
    rows = [
        ('(a) sigma-gauge RP on swap axes', FLAGS['a_blind']),
        ('(b) 4-twist insertion RP (whole ladder)', FLAGS['b_pd']),
        ('(c) mu4 (beta = pi/2) RP', FLAGS['c_pd']),
        ("(c') Bogoliubov (beta = pi/4) RP", FLAGS['c4_pd']),
        ('defect energy delta-blind (exact)', FLAGS['energy_blind']),
        ('parity <Gamma>_tw delta-blind', FLAGS['parity_blind']),
        ('site-cut fails in every decorated state', True),
        ('counterwitness arc-equivalent to blind member',
         FLAGS['cw_safe']),
    ]
    sided = [
        ('(a) eta flip on mark-fixing axes', FLAGS['a_fixflip']),
        ('(b) fixing-cut frustration (4,4,0)', FLAGS['b_frustration']),
    ]
    seen = [
        ('(b) insertion spectra depend on delta',
         FLAGS['b_sees_delta']),
        ('4-twist Casimir ln|w(D)| measures delta',
         FLAGS['casimir_dep']),
        ("(a)/(c)/(c') quasi-free spectra INVISIBLE",
         FLAGS['a_blind'] and FLAGS['c4_invisible']),
    ]
    print("        delta-BLIND positivity/existence rows (every member):")
    for name, ok in rows:
        print("          + %-48s %s" % (name, ok))
    print("        pi/2-ONLY twist structures (need the fixing axes = "
          "the bit):")
    for name, ok in sided:
        print("          - %-48s %s" % (name, ok))
    print("        delta-dependence structure of the decorated data:")
    for name, ok in seen:
        print("          ~ %-48s %s" % (name, ok))
    all_blind = all(ok for _, ok in rows)
    all_side = all(ok for _, ok in sided)
    all_seen = all(ok for _, ok in seen)
    # SUCCESS would need: PD at pi/2 AND failure off pi/2 on an
    # always-existing cut -- the ladders show PD everywhere instead
    selector = not (FLAGS['b_pd'] and FLAGS['c_pd'] and FLAGS['c4_pd']
                    and FLAGS['a_blind'])
    check("V1.1 PREREGISTERED VERDICT = KILL [typed, no overclaim]: the "
          "SUCCESS branch does NOT fire (%s) -- every well-defined "
          "mark-decorated state functional in the free-plus-twist class "
          "(sigma gauge, Kadanoff-Ceva 4-twist insertion, mu4 and "
          "genuine Bogoliubov bond defects) keeps RP POSITIVE on the "
          "always-existing mark-compatible cuts along the whole "
          "M(delta) ladder (%s).  Structure gained (%s): (i) "
          "Theta-compatible QUASI-FREE decorations are RP-spectrally "
          "INVISIBLE (orthogonal-congruence mechanism) -- that class "
          "cannot even carry delta into the RP datum; (ii) the "
          "insertion FUNCTIONALS are the first objects whose RP "
          "spectra and Casimir amplitude DO measure delta -- smoothly, "
          "delta <-> pi - delta equivariantly, never reaching the "
          "positivity verdict; (iii) the only twist-visible "
          "pi/2-EXCLUSIVE structures (sigma eta-flip, 4-twist "
          "fixing-cut frustration (4,4,0)) live on the mark-FIXING "
          "axes, which exist iff delta = pi/2 -- they presuppose the "
          "bit and even point in the INVERTED direction (%s).  The "
          "free-plus-twist class is EXHAUSTED: the NINTH side-blind "
          "test on the v512 scoreboard.  What could still see the "
          "bit: only a genuinely INTERACTING A_hol whose OS data are "
          "NOT Pfaffian-reducible to the chiral vacuum "
          "(non-quasi-free dynamics / non-monomial mark decorations "
          "-- beyond every Wick-computable class).  The alignment bit "
          "remains genuine discrete input.  Sandbox only, no marker "
          "moves"
          % (not selector, all_blind, all_seen, all_side),
          not selector and all_blind and all_side and all_seen)


# ---------------------------------------------------------------------------
def run():
    reset()
    RESULTS.clear()
    FLAGS.clear()
    print("v525 SEAM.BIT.TWISTBLIND.01: do mark-decorated STATES "
          "(twist/defect insertions) make RP side-sensitive on M(delta)?")
    print("  liftings: (a) sigma gauge, (b) Kadanoff-Ceva 4-twist "
          "insertion, (c) mu4 Bogoliubov defect -- Pfaffian-exact, "
          "40-digit certificates")
    print("=" * 100)
    K16 = mach()
    K32 = kmat_num(N32)
    s_frame()
    a_sigma(K16, K32)
    lad_b, wds = b_insertion(K16, K32)
    c_mu4(K16, K32)
    d_subresults(K16, K32, wds)
    n_controls(K16, K32)
    v_verdict()
    npass = sum(RESULTS)
    print("=" * 100)
    print("SUMMARY: %d/%d checks passed%s   [runtime %.1f s]"
          % (npass, len(RESULTS),
             "" if npass == len(RESULTS) else "  -- FAILURES PRESENT",
             time.time() - T0))
    return summary("v525 SEAM.BIT.TWISTBLIND.01: every well-defined "
                   "mark-decorated state functional in the "
                   "free-plus-twist class (sigma gauge, Kadanoff-Ceva "
                   "4-twist insertion, mu4 and genuine Bogoliubov "
                   "defects) keeps RP positive on the always-existing "
                   "cuts along the whole M(delta) ladder; quasi-free "
                   "decorations are RP-spectrally invisible (exact "
                   "congruence mechanism); the insertion spectra and "
                   "the 4-twist Casimir measure delta but never reach "
                   "the positivity verdict; the only pi/2-exclusive "
                   "structures (eta flip, fixing-cut frustration "
                   "(4,4,0)) presuppose the bit; E_def and <Gamma>_tw "
                   "delta-blind; the NINTH side-blind test (8 -> 9); "
                   "the free-plus-twist class is EXHAUSTED; the bit "
                   "remains genuine discrete input; no marker moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
