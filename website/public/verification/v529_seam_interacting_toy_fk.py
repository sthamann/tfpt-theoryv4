"""v529 -- SEAM.INT.FKTOY.01: the minimal interacting Fidkowski-Kitaev
seam toy -- the FIRST firing Kill-Test-2 shadow (triple-verdicted).
F1 = KILL, F2 = KILL, F3 = ERFOLG.  NO marker moves --
WOIT.OS.TWISTOR.01 stays [O]; the contract MUST document the firing
toy shadow as a named threat (Kill-Test-2 paragraph + the straddle
law as a concrete hurdle for beta3/gamma).

[E] 1. F1 = KILL (THE MOST IMPORTANT PART -- honest and prominent):
    Theta exists exactly on the interacting model (U_r^2=2^8, Theta^2=+1,
    clock-tower inversion conj_V·V=4096, [Theta,H_g]=0 exact,
    Theta Omega_g = Omega_g) -- Kill-Test 1 does NOT fire; BUT Kill-Test 2
    FIRES AT TOY LEVEL: RP breaks in the interacting ground state for
    every g>0 -- inertia ladder (37,0,0) at g=0 -> (33,4,0) at g=1/4,1/2
    -> (31,6,0) at g=1 -> (29,8,0) at g=2 (most negative EW -4.5e-2);
    Gibbs beta=2 exact same ladder; g=-1: (19,18,0).  MECHANISM:
    interference (neither crossing nor half-local alone breaks -- each
    (37,0,0)); STRADDLE LAW (24/24): RP fails exactly on
    quartet-straddled cuts, stays PD on quartet-avoiding.  MANDATORY
    FENCE: ONE toy, ONE interaction class, [C] flat-band parent --
    narrows the Woit route (every A_hol must protect RP against exactly
    this mechanism), does not close it.
[E] 2. F2 = KILL: the TENTH side-blind test (9->10), the first with
    genuinely non-Wick-computable dynamics -- the interaction sees
    delta massively (spectral spread 1.32, gaps 0.31-1.66, overlaps
    0.869-0.962), but the mark-axis mirror Theta_15 maps H(m)->H(8-m)
    EXACTLY (Fraction identity); all side data mirror-equal; Theta_7
    for m=1<->7 obstructed by exactly two NS wrap signs; counterwitness
    anchors to identical dynamics as m=2.  Door narrows: only dynamics
    that break mirror covariance in BOTH torsor orbits.
[E] 3. F3 = ERFOLG: grading exact ([H_q,(-1)^F]=0, <Gamma>=+1 incl.
    g=100); Z8 backbone: Utilde^2=256 Gamma=(-1)^F nonsplit, V^2=256
    Utilde (the clock tower IS the root of the deck), Theta inverts the
    tower; FK anchor single quartet {-1,+1}x128, m=4 at g->inf binomial
    ladder {16,64,96,64,16}; OS quotient at g>0 constructive on the
    pi/2 model (Gram (37,0,0), tau_4 PD (11,0,0), vacuum fixed).
[E] 4. CONTROLS: Theta-incompatible quartic makes Gram non-Hermitian
    (0.46 vs 1e-16); site (3,3,1).

Status: [E] exact Fraction/Clifford + float-track certificates (tol
1e-9); [C] flat-band parent / one interaction class fence.  Python;
Wolfram-mirrored (straddle inertias exact-rational where possible /
Z8 identities V^2=256 Utilde -- 256-dim spectra Python-only), counted
per GATE.WOLFRAM.02.  Discovery provenance:
experiments/tfpt-discovery/seam_interacting_toy_fk_probe.py
(24/24, 2026-07-23).

=== ORIGINAL PROBE HEADER (kept verbatim) ===
seam_interacting_toy_fk_probe.py -- EXPLORATION ONLY (experiments/, no
verification claim, no marker moves, sandbox only).

THE FIRST INTERACTING SEAM MODEL: the Fidkowski-Kitaev (FK) quartic on the
16-Majorana NS seam circle, exactly diagonalisable (2^8 = 256-dim Fock
space).  All open core questions converge on the interacting algebra A_hol
on the seam: (a) WOIT kill tests 1+2 (Theta existence, RP) -- defused on
the FREE level only (v519/v522/v524); (b) the alignment bit -- NINE
side-blind tests prove the whole Wick-computable class blind (v512, v521,
v525 + probes); only non-quasi-free dynamics could see it; (c) SEAM.EQUIV.
No concrete interacting seam model was ever built.  This probe builds the
minimal one: v510 shows the central arrangement carries the nontrivial FK
class (U^2 = (-1)^F, Z8 clock tower) -- the FK quartic is THE canonical
interaction of the Z8 classification of Majorana chains.

=== PREREGISTRATION (frozen BEFORE the run; criteria not adjusted) ===

Three SEPARATELY verdicted questions:

F1 (WOIT kill tests 1+2 on the interacting toy):
  Does Theta exist with Theta^2 = +1 and clock-tower inversion on the
  INTERACTING seam, and does RP hold on the bond cut in the interacting
  ground/Gibbs state?
  ERFOLG iff ALL of:
    (a) Theta_Fock (v519, bond axis k = 15) with Theta^2 = +1 and
        Theta V Theta^-1 = 4096 V^-1 exists (exact Clifford certificates)
        AND commutes with H_g = H_free + g H_q for every g (exact for the
        quartic; R C R^T = -C + anti-linearity for the free part);
    (b) the interacting GROUND-state OS Gram on the bond cut k = 15
        (deg <= 2 basis, 37 = 1 + 8 + 28) is Hermitian with NO negative
        direction for all g in {0, 1/4, 1/2, 1, 2} (float track,
        Hermiticity tol 1e-8, eigenvalue zero threshold 1e-9), with the
        g = 0 column reproducing v519/v524 EXACTLY (max entry deviation
        vs the exact sympy Wick Gram < 1e-10; inertia (8,0,0) odd,
        (29,0,0) even, (37,0,0) full);
    (c) the Gibbs state (beta = 2, [C] choice) passes the same battery,
        judged RELATIVE to its own g = 0 baseline;
    (d) the negative controls have teeth: a Theta-INCOMPATIBLE quartic
        breaks Hermiticity/theta-invariance quantifiably; the site cut
        stays non-PD in the interacting state.
  KILL iff a Theta-compatible construction exists but a ground (or
    baseline-relative Gibbs) Gram at some g > 0 acquires a negative
    direction (kill test 2 fires in the toy -- first sharp ammunition
    against the Woit route), or no Theta-compatible FK quartic exists at
    all (kill test 1 fires).
  UNENTSCHIEDEN: a branch is not well-definably constructible (typed).

F2 (the alignment bit): does the interacting model on the M(delta) mark
  family become SIDE-sensitive?  The marks couple into the dynamics via
  mark-anchored quartics H_marks(delta) = g * sum over the four marks of
  the quartet gamma_{b-2} gamma_{b-1} gamma_b gamma_{b+1} centred on the
  mark bond b ([C] anchoring rule).  SIDE datum means: a canonical
  readout X, computed identically for every member, with
  X(delta) != X(pi - delta) -- i.e. m vs 8 - m at delta = m pi/8 (the
  v525 bar: "decoration sees delta, positivity does not"; mere
  delta-dependence is NOT side-sensitivity).  The side mirror is
  CONSTRUCTED EXPLICITLY: the anti-unitary axis-7 reflection
  Theta_7 = U_r7 o K maps M(delta) -> M(pi - delta); readouts:
  full 256-level spectra, E0, gap, ground parity, vacuum overlap
  |<Omega_0|Omega_g(m)>|, RP-Gram spectra/inertia on the mark-swap bond
  axes (existing at N = 16 iff m even -- m in {2,4,6}; odd m typed as
  the known placement artifact, v521/v525), each at several g.
  Ladder: delta = m pi/8, m = 1..7 (mirror pairs (1,7), (2,6), (3,5),
  self-mirror 4) plus the v512 counterwitness delta_cw = atan(4/3).
  ERFOLG iff some side datum differs beyond 1e-9 AND the exact mirror
    mechanism confirms genuine inequivalence (Theta_7-conjugation of
    H(m) is NOT gauge-equivalent to H(8-m)).
  KILL iff the exact equivariance Theta_7 H(m) Theta_7^-1 = H(8-m)
    (up to solvable site-local Z2 gauge) is certified AND all side data
    vanish -- the TENTH side-blind test on the v512 scoreboard.
  UNENTSCHIEDEN otherwise (typed).

F3 (FK class + OS quotient): does the interacting ground state carry the
  expected Z8/FK class, and does the v524 OS quotient survive g > 0?
  ERFOLG iff ALL of:
    (a) fermion parity survives: [H_g, (-1)^F] = 0, definite ground
        parity, parity-block-diagonal Grams;
    (b) the Z8 backbone survives the interaction EXACTLY: H_q is
        alpha_1-covariant (hence deck- and clock-invariant), the deck
        lift obeys Utilde^2 = 256 Gamma = (-1)^F (nonsplit), the clock
        lift V implements the quarter shift with V^2 prop Utilde (the
        tower = square roots of the deck), Theta inverts the tower
        (conj_V V = 4096, v519 route) -- all exact Fraction/Cl(16);
    (c) FK anchor: a single quartet has spectrum {-1, +1} x 128; the
        m = 4 mark-anchored model at g -> infinity is 4 disjoint
        quartets with the exact binomial ladder E in {-4,-2,0,2,4},
        multiplicities {16, 64, 96, 64, 16}; the large-g (g = 100)
        translation-invariant model keeps definite parity;
    (d) OS quotient at g > 0: the 37-Gram null space stays {0} (or its
        degeneration is typed), and the clock transfer step tau_4 on the
        Klein-Landau domain {8..11} (11 monomials) is Hermitian and PD
        in the interacting state at g in {1/2, 1}, with the vacuum row
        fixed (omega_g o alpha invariance witnessed).
  KILL iff the quartic breaks the tower/grading, or the quotient
    degenerates (indefinite/rank collapse), or the clock step is not
    implementable (non-Hermitian or negative direction) at g > 0.
  UNENTSCHIEDEN otherwise (typed).

[C] FENCES (model choices, declared): this is a TOY, not a construction
of A_hol -- every statement is about the 16-Majorana lattice seam with
deg <= 2 OS bases; NO extrapolation to the continuum interacting algebra
is claimed.  Choices: (i) H_free = (i/4) sum C_ab gamma_a gamma_b -- the
quadratic parent whose UNIQUE ground state is exactly the v519 chiral NS
vacuum (flat single-particle spectrum; the state is pinned, the parent is
[C]); (ii) H_q = the NS-shift-covariant FK quartic
sum_{p=0..15} alpha_1^p(gamma_0 gamma_1 gamma_2 gamma_3) (translation
invariance in the NS sense); (iii) the mark anchoring rule (quartet on
the 4 sites centred at each mark bond); (iv) Gibbs beta = 2; (v) g > 0
sign; g = -1 is run as a labelled mechanism diagnostic only; (vi) float
track (numpy 256-dim) with tolerances declared above, exact
sympy/Fraction certificates for the load-bearing algebraic identities
(Clifford relations, implementers, Theta compatibility, tower, class),
mpmath 40-digit inertia for the exact free Gram.  Runtime target
< 30 min.

READ-ONLY basis: verification/v519_woit_theta_rp_free.py (kernel,
theta_mono, gram, refl_implementer, clock_lift, inertia -- reused
verbatim where possible), v510 (deck census, (-1)^F), v521/v525 probes
(M(delta) frame, swap axes, counterwitness incidence),
experiments/tfpt-discovery/woit_os_beta2_os_quotient_probe.py (tower
maps, alpha_mono, Klein-Landau domain).

=== TRANSPARENCY (deviations after run 1; preregistration unchanged) ===

Run 1 (2026-07-23) surfaced four tooling items, fixed for run 2 with NO
criterion, tolerance or verdict-logic change: (i) a %-format crash in
the V2 check string; (ii) the bond-axis implementer normalisation:
U_r(k = 15)^2 = 2^8 (the v510 bond/edge-axis class; the site-axis
members square to 2^7) -- conj_V rescaled accordingly, the invariant
scalar conj_V V = 4096 is unchanged; (iii) the preregistered mirror
OPERATIONALISATION Theta_7 (midpoint axis) fails to assemble for the
single pair m = 1 <-> 7 by exactly two NS wrap signs (typed as torsor
structure in B2.1); the equally canonical MARK-axis mirror Theta_15 of
the same v519 torsor realises the preregistered side mirror EXACTLY
for all m and carries the mechanism certificate; (iv) two labelled
post-hoc mechanism controls added (A4.1 crossing/half-local
decomposition; C3.2 constructive m = 4 quotient witness),
verdict-neutral; assertions locked to the measured inertia ladders
(regression style).

=== RESULT (filled after the run, 2026-07-23; 24/24 PASS) ===

VERDICTS: F1 = KILL | F2 = KILL | F3 = ERFOLG.

F1 = KILL -- KILL TEST 2 FIRES ON THE FIRST INTERACTING SEAM MODEL
  (the first sharp ammunition against the Woit route, toy level).
  Kill test 1 does NOT fire: Theta_Fock exists on the interacting
  model (U_r^2 = 2^8 exact, Theta^2 = +1 matrix-exact dev 0.0,
  clock-tower inversion conj_V V = 4096 exact, [Theta, H_g] = 0 exact
  for every g, ground states Theta-invariant to 1e-8).  But the OS
  Gram on the bond cut k = 15 is INDEFINITE in the interacting ground
  state for EVERY g > 0: inertia (33,4,0) at g = 1/4 and 1/2,
  (31,6,0) at g = 1, (29,8,0) at g = 2 (most negative eigenvalue
  -4.5e-2, seven orders above threshold; the free even sector sits
  near the RP boundary at min eigenvalue 1.78e-6 and the interaction
  pushes through), IDENTICALLY in the Gibbs state (beta = 2, baseline
  (37,0,0) PD), and for g = -1 too ((19,18,0): no coupling-sign
  rescue).  g = 0 reproduces the exact v519/v524 Wick Gram to 8.9e-16
  with 40-digit inertia (37,0,0), min 1.7801e-6.  MECHANISM (typed):
  neither the 6 cut-crossing FK terms alone nor the 10 half-local
  terms alone break RP (each gives (37,0,0) at g = 1; mins 3.1e-3 /
  1.4e-5) -- the violation is an INTERFERENCE effect; on the
  mark-anchored family RP fails exactly on quartet-STRADDLED cuts and
  stays PD on every quartet-AVOIDING cut (the straddle law, 24/24
  entries): reflection positivity is a nontrivial SELECTOR on
  interacting seam dynamics, not an automatic property.  Controls:
  Theta-incompatible quartic g0 g1 g2 g4 -> Gram non-Hermitian (dev
  0.46 for both eta); site cut stays non-PD ((3,3,1) at g = 0 and 1).
  FENCE: one interaction class on one 16-Majorana toy with a [C]
  flat-band parent -- narrows the route, does not close it.
F2 = KILL -- the TENTH side-blind test on the v512 scoreboard, the
  FIRST with genuinely interacting (non-quasi-free, non-Wick-
  reducible) dynamics: the explicit anti-unitary side mirror (mark
  axis, Theta_15 = the OS Theta itself) maps H_marks(m) ->
  H_marks(8-m) EXACTLY for all m (Fraction identity, no gauge;
  matrix conjugation dev 0.0; R C R^T = -C exact for k = 15 and 7)
  => full equivariance; machine confirmation: 256-level spectra of
  m vs 8-m identical to 8e-15, vacuum overlaps to 7e-16, RP-Gram
  spectra across the mirror pairs (m=2, axis k) <-> (m=6, axis 14-k)
  identical to ~1e-14 -- EVERY canonical readout is mirror-equal.
  The decoration DOES see delta: spectral spread 1.32 across the
  ladder at g = 1, Gram spectra vary with (m, g) -- delta-dependence
  everywhere, side-sensitivity nowhere (the v525 bar, interacting
  edition).  Torsor structure: the midpoint-axis mirror Theta_7 is
  exact for m = 2, 3, 4 and obstructed for m = 1 <-> 7 by exactly
  two NS wrap signs (quartets (0,13,14,15), (5,6,7,8)); no
  C-preserving gauge removes them -- the side mirror is pinned to
  the mark-axis clock orbit.  The counterwitness delta_cw = atan(4/3)
  anchors to the IDENTICAL Hamiltonian as the blind member m = 2
  (exact dict equality; v525 N2.1 integer incidence at the dynamics
  level).  Odd m have no bond swap axis (best Hermiticity dev 0.75;
  typed placement artifact).  The alignment bit remains genuine
  discrete input even against FK-interacting dynamics.
F3 = ERFOLG -- the interacting ground state carries the Z8/FK class:
  grading survives ([H_q, (-1)^F] = 0 exact, all terms degree 4,
  ground parity <Gamma> = +1 at every g incl. g = 100, unique gapped
  grounds); the Z8 backbone survives EXACTLY (alpha_1(H_q) = H_q,
  deck- and clock-invariance, Utilde^2 = 256 Gamma = (-1)^F nonsplit,
  V^2 = 256 Utilde -- the clock tower IS a square root of the deck --
  conj_V V = 4096, all Fraction-exact); FK anchor: single quartet
  spectrum {-1, +1} x 128 exact, m = 4 at g -> infinity = 4 disjoint
  quartets with the exact binomial ladder E in {-4,-2,0,2,4}, mults
  {16,64,96,64,16}.  OS quotient at g > 0: CONSTRUCTIVE witness on
  the delta = pi/2 mark-anchored model, quartet-avoiding axis k = 3
  -- Gram PD (37,0,0) (min 4.4e-5), clock step tau_4 Hermitian PD
  (11,0,0) (min 8.4e-5 / 4.0e-5), vacuum row fixed, alpha_4-invariant
  -- H_phys exists and the clock stays implementable; the
  translation-invariant model's quotient DEGENERATES (Gram indefinite
  incl. the interior D4 block (9,2,0)) = exactly the F1 RP datum at
  quotient level (typed there, not double-counted).
  Bonus structure (not verdict-bearing): interacting RP, where it
  holds, keeps the site cut failing -- the v519 placement selection
  is interaction-stable.

Exactness: sympy/Fraction exact where marked; float track numpy
(deviations quoted); mpmath 40-digit for the exact free Gram inertia.
Standalone, deterministic.  Runtime ~ 100 s.

Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/seam_interacting_toy_fk_probe.py
"""
import time
from fractions import Fraction as Fr
from itertools import combinations

import mpmath as mp
import numpy as np
import sympy as sp

from tfpt_constants import check as _check, summary, reset

mp.mp.dps = 40

I = sp.I
N = 16
NH = 8
BETA = 2.0                       # [C] Gibbs inverse temperature
G_LADDER = (0.0, 0.25, 0.5, 1.0, 2.0)
TOL_HERM = 1e-8                  # float-track Gram Hermiticity
TOL_ZERO = 1e-9                  # float-track eigenvalue zero threshold
TOL_REG = 1e-10                  # exact-vs-float regression
TOL_DEG = 1e-8                   # ground-state degeneracy clustering

RESULTS = []
FLAGS = {}
T0 = time.perf_counter()


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
    return sp.simplify(e3) == 0


# ---------------------------------------------------------------------------
# exact Cl(16) machinery (v519/v510 verbatim)
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


def prop(x, y):
    if not x or not y or set(x) != set(y):
        return (False, None)
    m0 = next(iter(y))
    c = x[m0] / y[m0]
    return (all(x[m] == c * y[m] for m in y), c)


def dict_eq(x, y):
    return not cadd(x, cscale(y, Fr(-1)))


def apply_lin(mat, a, n):
    out = {}
    for b in range(n):
        if mat[b][a]:
            out = cadd(out, cscale(gam(b), Fr(mat[b][a])))
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
        b = (a + k) % n
        M[b][a] = wrap_sign if a + k >= n else 1
    return M


def refl_matrix(n, k, wrap_sign):
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        idx = (k - a) % (2 * n)
        M[idx % n][a] = wrap_sign if idx >= n else 1
    return M


def refl_factors(n, k):
    """the ordered binomial factors of the v519 NS reflection
    implementer for axis k (site pairs (a, k-a), NS wrap sign)."""
    fixed = [j for j in range(n) if (k - j) % n == j]
    fac = []
    for a in range(n):
        b = (k - a) % n
        if a >= b or a in fixed:
            continue
        idx = (k - a) % (2 * n)
        eps = Fr(-1) if idx >= n else Fr(1)
        fac.append((a, b, eps))
    return fixed, fac


def refl_implementer(n, k):
    fixed, fac = refl_factors(n, k)
    if fixed:
        fplus = [f for f in fixed if (k - f) % (2 * n) < n]
        U = {tuple(j for j in range(n) if j != fplus[0]): Fr(1)}
    else:
        U = dict(ONE)
    for a, b, eps in fac:
        U = cmul(U, cadd(gam(a), cscale(gam(b), eps)))
    return U


def clock_lift(n):
    """the v506/v519 quarter-shift Fock lift V (rational nullspace)."""
    Cblk = [[0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    even_basis = [(), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
                  (0, 1, 2, 3)]
    odd_basis = [(0,), (1,), (2,), (3,), (0, 1, 2), (0, 1, 3), (0, 2, 3),
                 (1, 2, 3)]
    rows = []
    for a4 in range(4):
        img = apply_lin(Cblk, a4, 4)
        cols = []
        for mb in even_basis:
            x = {mb: Fr(1)}
            expr = cadd(cmul(x, gam(a4)), cscale(cmul(img, x), Fr(-1)))
            cols.append([expr.get(mo, Fr(0)) for mo in odd_basis])
        for r_i in range(8):
            rows.append([sp.Rational(cols[c_i][r_i].numerator,
                                     cols[c_i][r_i].denominator)
                         for c_i in range(8)])
    A = sp.Matrix(rows)
    null = A.nullspace()
    vec = null[0] * sp.lcm([sp.denom(x) for x in null[0]])
    v = {even_basis[kk]: Fr(int(vec[kk])) for kk in range(8) if vec[kk] != 0}

    def embed(x, j):
        table = (j, j + 4, j + 8, j + 12)
        return {tuple(sorted(table[i] for i in m)): c for m, c in x.items()}

    V = ONE
    for j in range(4):
        V = cmul(V, embed(v, j))
    return V


def pair_scalar(x, y):
    c0 = Fr(0)
    for m1, cx in x.items():
        cy = y.get(m1)
        if cy:
            s_m, m_sq = mono_mul(m1, m1)
            assert m_sq == ()
            c0 += s_m * cx * cy
    return c0


# ---------------------------------------------------------------------------
# reflections, halves, theta, towers (v519/v524 verbatim)
# ---------------------------------------------------------------------------
def refl_map(k, n=N):
    def r(a):
        return (k - a) % n

    def s(a):
        return -1 if (k - a) % (2 * n) >= n else 1
    return r, s


def half_of(k, n=N):
    if k % 2 == 0:
        f1 = (k // 2) % n
        P = [(f1 + j) % n for j in range(1, n // 2)]
    else:
        b = (k + 1) // 2
        P = [(b + j) % n for j in range(n // 2)]
    rP = {(k - a) % n for a in P}
    assert not (rP & set(P))
    return P


def theta_mono_exact(mono, r, s, eta):
    """v519 theta_mono verbatim (sympy coefficient)."""
    imgs = [r(a) for a in reversed(mono)]
    coeff = eta ** len(mono)
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


def theta_mono_num(mono, r, s, eta):
    imgs = [r(a) for a in reversed(mono)]
    coeff = complex(eta) ** len(mono)
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


def tower_maps(n, shift, kmax):
    """(perm, sign) for alpha^k, NS wrap sign (v524 verbatim)."""
    maps = [(tuple(range(n)), (1,) * n)]
    for _ in range(kmax):
        perm, sign = maps[-1]
        np_, ns_ = [], []
        for a in range(n):
            p, s0 = perm[a], sign[a]
            q = p + shift
            np_.append(q % n)
            ns_.append(s0 * (-1 if (q >= n or q < 0) else 1))
        maps.append((tuple(np_), tuple(ns_)))
    return maps


def alpha_mono(m, pm):
    """signed-permutation automorphism on a sorted monomial (v524)."""
    perm, sign = pm
    c = 1
    imgs = []
    for a in m:
        c *= sign[a]
        imgs.append(perm[a])
    lst = list(imgs)
    sgn = 1
    for i in range(len(lst)):
        for j in range(len(lst) - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                sgn = -sgn
    assert len(set(lst)) == len(lst)
    return c * sgn, tuple(lst)


def sperm_dict(H, pm):
    """apply a signed permutation (as anti-/linear automorphism with
    trivial coefficient action -- valid for REAL coefficient dicts)."""
    out = {}
    for m, c in H.items():
        c2, m2 = alpha_mono(m, pm)
        cc = out.get(m2, Fr(0)) + c * c2
        if cc:
            out[m2] = cc
        elif m2 in out:
            del out[m2]
    return out


def refl_pm(k, n=N):
    r, s = refl_map(k, n)
    return (tuple(r(a) for a in range(n)), tuple(s(a) for a in range(n)))


TW = tower_maps(N, 1, N)
DECK_PM = TW[8]
CLOCK_PM = TW[4]


# ---------------------------------------------------------------------------
# exact chiral NS kernel + Wick (v519 verbatim, memoised)
# ---------------------------------------------------------------------------
def c_of(d, n=N):
    if d % 2 == 0:
        return sp.Integer(0)
    return sp.Rational(2, n) / sp.sin(sp.pi * sp.Rational(d, n))


_WICK = {}


def wick(idx, n=N):
    idx = tuple(idx)
    if len(idx) == 0:
        return sp.Integer(1)
    if len(idx) % 2 == 1:
        return sp.Integer(0)
    key = (idx, n)
    if key in _WICK:
        return _WICK[key]
    head, rest = idx[0], idx[1:]
    tot = sp.Integer(0)
    for j, b in enumerate(rest):
        sub = rest[:j] + rest[j + 1:]
        g2 = sp.Integer(1) if head == b else I * c_of(head - b, n)
        tot += (-1) ** j * g2 * wick(sub, n)
    tot = sp.expand_complex(tot)
    _WICK[key] = tot
    return tot


def spectrum_inertia_exact(Msym, tol=None):
    """40-digit inertia of an exact Hermitian sympy matrix (v519)."""
    if tol is None:
        tol = mp.mpf(10) ** (-25)
    n = Msym.shape[0]
    A = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            re_, im_ = Msym[i, j].evalf(45).as_real_imag()
            A[i, j] = mp.mpc(mp.mpf(str(re_)), mp.mpf(str(im_)))
    E, _ = mp.eighe(A)
    evs = [E[i].real for i in range(n)]
    npos = sum(1 for e in evs if e > tol)
    nneg = sum(1 for e in evs if e < -tol)
    nz = [abs(e) for e in evs if abs(e) > tol]
    return (npos, nneg, n - npos - nneg), (min(nz) if nz else mp.mpf(0))


# ---------------------------------------------------------------------------
# Jordan-Wigner Fock representation (float track, 256-dim)
# ---------------------------------------------------------------------------
def build_gammas():
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    E = np.eye(2, dtype=complex)
    gams = []
    for l in range(8):
        for P in (X, Y):
            ops = [Z] * l + [P] + [E] * (7 - l)
            M = ops[0]
            for o in ops[1:]:
                M = np.kron(M, o)
            gams.append(M)
    return gams


GAM = build_gammas()
DIM = 256
_MONO_MAT = {(): np.eye(DIM, dtype=complex)}


def mono_mat(m):
    if m not in _MONO_MAT:
        M = GAM[m[0]]
        for a in m[1:]:
            M = M @ GAM[a]
        _MONO_MAT[m] = M
    return _MONO_MAT[m]


def dict_to_mat(H):
    M = np.zeros((DIM, DIM), dtype=complex)
    for m, c in H.items():
        M += float(c) * mono_mat(m)
    return M


def herm_dev_mat(M):
    return float(np.max(np.abs(M - M.conj().T)))


def gibbs_rho(Hm, beta):
    w, Q = np.linalg.eigh(Hm)
    e = np.exp(-beta * (w - w[0]))
    e /= e.sum()
    return (Q * e) @ Q.conj().T


def ground_state(Hm):
    """returns (state, gap, degeneracy, w).  state = ('pure', vec) or
    ('mix', projector-average rho) for degenerate ground spaces."""
    w, Q = np.linalg.eigh(Hm)
    deg = int(np.sum(w < w[0] + TOL_DEG))
    if deg == 1:
        return ('pure', Q[:, 0]), float(w[1] - w[0]), 1, w
    rho = Q[:, :deg] @ Q[:, :deg].conj().T / deg
    return ('mix', rho), float(w[deg] - w[0]), deg, w


def expec(state, A):
    kind, x = state
    if kind == 'pure':
        return complex(np.vdot(x, A @ x))
    return complex(np.sum(x * A.T))


def levels(w, tol=1e-7):
    out = []
    for e in w:
        if out and abs(e - out[-1][0]) < tol:
            out[-1] = (out[-1][0], out[-1][1] + 1)
        else:
            out.append((float(e), 1))
    return out


# ---------------------------------------------------------------------------
# OS Gram in an arbitrary state (float track)
# ---------------------------------------------------------------------------
def basis_of(k):
    P = half_of(k)
    return [()] + [(a,) for a in P] + list(combinations(P, 2))


def gram_state(state, k, eta, basis, sfun=None):
    r, s0 = refl_map(k)
    s = sfun if sfun is not None else s0
    nb = len(basis)
    th = [theta_mono_num(m, r, s, eta) for m in basis]
    G = np.zeros((nb, nb), dtype=complex)
    kind, x = state
    if kind == 'pure':
        vb = [mono_mat(m) @ x for m in basis]
        for a, (ca, ta) in enumerate(th):
            wa = mono_mat(ta).conj().T @ x
            for b in range(nb):
                G[a, b] = ca * np.vdot(wa, vb[b])
    else:
        Mb = [mono_mat(m) for m in basis]
        for a, (ca, ta) in enumerate(th):
            Pa = x @ mono_mat(ta)
            for b in range(nb):
                G[a, b] = ca * np.sum(Pa * Mb[b].T)
    return G


def inertia_num(evs, tol=TOL_ZERO):
    npos = int(np.sum(evs > tol))
    nneg = int(np.sum(evs < -tol))
    return (npos, nneg, len(evs) - npos - nneg)


def gram_report(state, k, basis, sfun=None):
    """scan eta in {+i, -i}; return list of Hermitian picks sorted by
    fewest negative directions: (etastr, hermdev, full/odd/even inertia,
    min |nonzero| eig, sorted spectrum)."""
    odd_idx = [i for i, m in enumerate(basis) if len(m) % 2 == 1]
    ev_idx = [i for i, m in enumerate(basis) if len(m) % 2 == 0]
    out = []
    for eta, tag in ((1j, '+i'), (-1j, '-i')):
        G = gram_state(state, k, eta, basis, sfun)
        dev = herm_dev_mat(G)
        if dev > TOL_HERM:
            continue
        Gh = (G + G.conj().T) / 2
        evs = np.linalg.eigvalsh(Gh)
        io = inertia_num(np.linalg.eigvalsh(
            Gh[np.ix_(odd_idx, odd_idx)])) if odd_idx else (0, 0, 0)
        ie = inertia_num(np.linalg.eigvalsh(Gh[np.ix_(ev_idx, ev_idx)]))
        nz = np.abs(evs)[np.abs(evs) > TOL_ZERO]
        out.append((tag, dev, inertia_num(evs), io, ie,
                    float(nz.min()) if len(nz) else 0.0, np.sort(evs)))
    out.sort(key=lambda t: t[2][1])
    return out


# ---------------------------------------------------------------------------
# Hamiltonians
# ---------------------------------------------------------------------------
CNUM = np.zeros((N, N))
for _a in range(N):
    for _b in range(N):
        if _a != _b:
            CNUM[_a, _b] = float(sp.N(c_of(_a - _b), 20))


def build_hfree():
    M = np.zeros((DIM, DIM), dtype=complex)
    for a in range(N):
        for b in range(a + 1, N):
            if CNUM[a, b]:
                M += 0.5j * CNUM[a, b] * (GAM[a] @ GAM[b])
    return M


def fk_quartic_ns():
    """H_q = sum_{p=0..15} alpha_1^p(g0 g1 g2 g3) -- NS-shift covariant."""
    H = {}
    Qp = {(0, 1, 2, 3): Fr(1)}
    for _ in range(N):
        H = cadd(H, Qp)
        Qp = sperm_dict(Qp, TW[1])
    return H


def quartet(b):
    q = ONE
    for j in (b - 2, b - 1, b, b + 1):
        q = cmul(q, gam(j % N))
    return q


def h_marks(m):
    """mark-anchored FK quartic: one quartet centred on each mark bond
    b in {0, m, 8, 8+m} of M(delta = m pi/8)."""
    H = {}
    for b in (0, m, 8, 8 + m):
        H = cadd(H, quartet(b % N))
    return H


HQ = fk_quartic_ns()
HQ_MAT = dict_to_mat(HQ)
HBAD = {}
HBAD = cadd(HBAD, cmul(cmul(cmul(gam(0), gam(1)), gam(2)), gam(4)))
HBAD_MAT = dict_to_mat(HBAD)


# ===========================================================================
# MACH -- representation, Theta, tower (exact + float cross-anchored)
# ===========================================================================
def mach():
    print("  -- MACH: JW representation, Theta_Fock, clock tower")
    dev_ac = 0.0
    for a in range(N):
        for b in range(a, N):
            tgt = 2.0 * np.eye(DIM) if a == b else np.zeros((DIM, DIM))
            dev_ac = max(dev_ac, float(np.max(np.abs(
                GAM[a] @ GAM[b] + GAM[b] @ GAM[a] - tgt))))
    dev_h = max(herm_dev_mat(GAM[a]) for a in range(N))
    Gamma_mat = mono_mat(tuple(range(N)))
    dev_par = float(np.max(np.abs(Gamma_mat @ Gamma_mat - np.eye(DIM))))
    par_herm = herm_dev_mat(Gamma_mat)
    check("M1.1 JW CLIFFORD EXACT [float track, integer entries]: all "
          "136 anticommutators {g_a, g_b} = 2 delta_ab (max dev %.1e), "
          "all 16 generators Hermitian (max dev %.1e), parity Gamma = "
          "g_0..g_15 Hermitian (dev %.1e) with Gamma^2 = 1 (dev %.1e) "
          "-- the 256-dim Fock representation is faithful"
          % (dev_ac, dev_h, par_herm, dev_par),
          dev_ac < 1e-12 and dev_h < 1e-12 and dev_par < 1e-12
          and par_herm < 1e-12)

    # Theta_Fock = U_r o K, axis k = 15 (v519); exact + matrix
    Ur = refl_implementer(N, 15)
    ok_sq, c_sq = prop(cmul(Ur, Ur), ONE)
    R15m = refl_matrix(N, 15, -1)
    negR = [[-x for x in row] for row in R15m]
    impl_p = implements(Ur, R15m, N)
    impl_m = implements(Ur, negR, N)
    fixed, fac = refl_factors(N, 15)
    Urmat = np.eye(DIM, dtype=complex)
    for a, b, eps in fac:
        Urmat = Urmat @ (GAM[a] + float(eps) * GAM[b])
    Urmat /= np.sqrt(float(c_sq))
    Wmat = mono_mat(tuple(range(1, N, 2)))
    Mth = Urmat @ Wmat
    FLAGS['Mth'] = Mth
    dev_th2 = float(np.max(np.abs(Mth @ Mth.conj() - np.eye(DIM))))
    r15, s15 = refl_map(15)
    Minv = Mth.conj()
    eps_glob = None
    dev_gen = 1e9
    for e_try in (1.0, -1.0):
        d = max(float(np.max(np.abs(
            Mth @ GAM[a].conj() @ Minv - e_try * s15(a) * GAM[r15(a)])))
            for a in range(N))
        if d < dev_gen:
            dev_gen, eps_glob = d, e_try
    check("M2.1 THETA_FOCK EXISTS, THETA^2 = +1 [exact Fraction + "
          "matrix]: U_r (bond axis k = 15 = the mu = 1 mark axis in "
          "the half-offset placement) implements the NS reflection "
          "(+R %s / -R %s; the v507/v510 lift ambiguity, global sign) "
          "with U_r^2 = %s = 2^8 EXACTLY (the v510 bond/edge-axis "
          "class; the site-axis torsor members square to 2^7, v519); "
          "matrix anti-unitary Theta = U_r o K (K = W o K_0 with W = "
          "odd-JW monomial fixing all gammas): Theta^2 = +1 (dev "
          "%.1e), Theta g_a Theta^-1 = %+d * s_a g_{15-a} on all 16 "
          "generators (dev %.1e) -- kill test 1's object exists on "
          "the interacting-capable representation"
          % (impl_p, impl_m, c_sq, dev_th2, int(eps_glob), dev_gen),
          ok_sq and c_sq == Fr(2 ** 8) and (impl_p or impl_m)
          and dev_th2 < 1e-10 and dev_gen < 1e-10)

    # clock tower: V implements the quarter shift; Theta inverts it;
    # V^2 prop Utilde; Utilde^2 = 256 Gamma (v519 W-S6.2 / v510 A-D4.1)
    V = clock_lift(N)
    C_ns = shift_matrix(N, 4, -1)
    ok_V = implements(V, C_ns, N)
    Ut = dict(ONE)
    for j in range(8):
        Ut = cmul(Ut, cadd(ONE, cscale(cmul(gam(j), gam(j + 8)), Fr(-1))))
    GAMMA_CL = {tuple(range(N)): Fr(1)}
    ok_ut2, c_ut2 = prop(cmul(Ut, Ut), GAMMA_CL)
    Cm = sp.Matrix(N, N, lambda a, b: c_of(a - b))
    Rm = sp.Matrix(refl_matrix(N, 15, -1))
    Cinv = sp.Matrix(C_ns).inv()
    mat_inv = sp.simplify(Rm * sp.Matrix(C_ns) * Rm.inv()
                          - Cinv) == sp.zeros(N, N)
    Cinv_int = [[int(Cinv[i_, j_]) for j_ in range(N)] for i_ in range(N)]
    conj_V = cscale(cmul(cmul(Ur, V), Ur), Fr(1, 2 ** 8))
    impl_conj = implements(conj_V, Cinv_int, N)
    c0 = pair_scalar(conj_V, V)
    V2 = cmul(V, V)
    ok_v2a, c_v2a = prop(V2, Ut)
    ok_v2b, c_v2b = prop(V2, cmul(Ut, GAMMA_CL))
    tower = ('V^2 = %s Utilde' % c_v2a) if ok_v2a else \
        ('V^2 = %s Utilde Gamma' % c_v2b if ok_v2b else 'NO')
    FLAGS['tower_ok'] = ok_V and impl_conj and c0 == Fr(4096) \
        and ok_ut2 and c_ut2 == Fr(256) and ok_v2a and c_v2a == Fr(256)
    check("M3.1 THE Z8 CLOCK TOWER + THETA INVERSION [exact Fraction]: "
          "V implements the NS quarter shift (%s); R C_ns R^-1 = "
          "C_ns^-1 at matrix level (%s) and conj_V = U_r V U_r^-1 "
          "implements C_ns^-1 with conj_V V = %s = 4096: Theta V "
          "Theta^-1 = 4096 V^-1 (the clock-tower INVERSION, v519 "
          "W-S6.2 route); Utilde^2 = %s Gamma = 256 (-1)^F (nonsplit "
          "class, v510) and %s (the tower IS a square root of the "
          "deck) -- the full Z8/Theta backbone is machine-instantiated "
          "on the interacting-capable algebra"
          % (ok_V, mat_inv, c0, c_ut2, tower),
          FLAGS['tower_ok'] and mat_inv)

    # H_free: the v519 chiral NS vacuum as a quadratic parent
    Hf = build_hfree()
    dev_hh = herm_dev_mat(Hf)
    pick = None
    for sgn in (1.0, -1.0):
        st, gap, deg, w = ground_state(sgn * Hf)
        M2 = np.zeros((N, N), dtype=complex)
        for a in range(N):
            for b in range(N):
                M2[a, b] = expec(st, GAM[a] @ GAM[b])
        dev2 = float(np.max(np.abs(
            M2 - (np.eye(N) + 1j * CNUM))))
        if dev2 < 1e-9:
            pick = (sgn, gap, deg, dev2)
    FLAGS['hfree_sign'] = pick[0] if pick else None
    FLAGS['HF_MAT'] = (pick[0] if pick else 1.0) * Hf
    check("M4.1 H_free RECONSTRUCTED [float, anchored to the exact "
          "kernel]: H_free = (i/4) sum C_ab g_a g_b is Hermitian (dev "
          "%.1e); the sign %s branch has a UNIQUE ground state (deg "
          "%d, gap %.3f -- flat single-particle spectrum, [C] parent "
          "choice) whose 2-point function equals the exact v519 "
          "chiral NS vacuum delta_ab + i C(a-b) to %.1e -- the free "
          "seam state is reproduced from a Hamiltonian, as the "
          "interacting deformation requires"
          % (dev_hh, '+' if pick and pick[0] > 0 else '-',
             pick[2] if pick else -1, pick[1] if pick else -1,
             pick[3] if pick else -1),
          dev_hh < 1e-12 and pick is not None and pick[2] == 1)


# ===========================================================================
# R -- g = 0 regression against the exact v519/v524 Wick Gram
# ===========================================================================
def regression():
    print("  -- R: g = 0 regression (exact Wick Gram, k = 15)")
    basis = basis_of(15)
    r, s = refl_map(15)
    rows = []
    for ma in basis:
        ca, ia = theta_mono_exact(ma, r, s, I)
        row = []
        for mb in basis:
            assert not (set(ia) & set(mb))
            row.append(sp.expand_complex(ca * wick(list(ia) + list(mb))))
        rows.append(row)
    Gex = sp.Matrix(rows)
    in_ex, gap_ex = spectrum_inertia_exact(Gex)
    Gex_num = np.array([[complex(sp.N(Gex[i, j], 20))
                         for j in range(37)] for i in range(37)])
    st0, gap0, deg0, w0 = ground_state(FLAGS['HF_MAT'])
    FLAGS['state0'] = st0
    G0 = gram_state(st0, 15, 1j, basis)
    dev_reg = float(np.max(np.abs(G0 - Gex_num)))
    picks = gram_report(st0, 15, basis)
    p0 = picks[0]
    FLAGS['free_ok'] = (in_ex == (37, 0, 0) and dev_reg < TOL_REG
                        and p0[2] == (37, 0, 0) and p0[3] == (8, 0, 0)
                        and p0[4] == (29, 0, 0))
    FLAGS['free_min'] = p0[5]
    check("R1.1 g = 0 REPRODUCES v519/v524 EXACTLY [exact entries, "
          "40-digit inertia + float track]: the exact 37x37 bond-cut "
          "Wick Gram has inertia %s (min eigenvalue %s at 40 digits, "
          "= the v524 H_phys); the float-track Gram in the H_free "
          "ground state matches it entrywise to %.1e (< 1e-10) with "
          "eta = %s, inertias full %s / odd %s / even %s -- the "
          "interacting machinery reduces EXACTLY to the pinned free "
          "system at g = 0"
          % (in_ex, mp.nstr(gap_ex, 5), dev_reg, p0[0], p0[2], p0[3],
             p0[4]),
          FLAGS['free_ok'])

    rho0 = gibbs_rho(FLAGS['HF_MAT'], BETA)
    K2 = np.zeros((N, N), dtype=complex)
    for a in range(N):
        for b in range(N):
            K2[a, b] = expec(('mix', rho0), GAM[a] @ GAM[b])
    Kdev = K2 - np.eye(N)
    lam = float(np.real(Kdev[0, 1] / (1j * CNUM[0, 1])))
    dev_prop = float(np.max(np.abs(Kdev - 1j * lam * CNUM)))
    picks_g = gram_report(('mix', rho0), 15, basis_of(15))
    pg = picks_g[0] if picks_g else None
    FLAGS['gibbs0'] = pg
    check("R2.1 g = 0 GIBBS BASELINE [float, beta = %.1f]: the thermal "
          "2-point kernel stays in the chiral ray, K = delta + i "
          "lambda C with lambda = %.6f (= tanh(beta/2) = %.6f; "
          "proportionality dev %.1e) -- flat-band KMS; the thermal OS "
          "Gram on the bond cut is Hermitian (dev %.1e) for eta = %s "
          "with inertia %s (min %.3e): the free GIBBS baseline for "
          "the F1 comparison is PD"
          % (BETA, lam, np.tanh(BETA / 2), dev_prop,
             pg[1] if pg else -1, pg[0] if pg else '--',
             pg[2] if pg else (0, 0, 0), pg[5] if pg else -1),
          dev_prop < 1e-9 and pg is not None and pg[2] == (37, 0, 0))


# ===========================================================================
# T -- Theta compatibility of the quartics (exact Fraction certificates)
# ===========================================================================
def theta_compat():
    print("  -- T: Theta compatibility of the quartics (exact)")
    # Hermiticity of a real-coefficient monomial dict: monomial adjoint
    # = reversal = (-1)^{k(k-1)/2}; for k = 4 that is +1:
    herm_q = all(len(m) == 4 for m in HQ)
    cov = dict_eq(sperm_dict(HQ, TW[1]), HQ)
    deck_inv = dict_eq(sperm_dict(HQ, DECK_PM), HQ)
    clock_inv = dict_eq(sperm_dict(HQ, CLOCK_PM), HQ)
    th_inv = dict_eq(sperm_dict(HQ, refl_pm(15)), HQ)
    nterms = len(HQ)
    cross = [m for m in HQ
             if (set(m) & set(range(8))) and (set(m) & set(range(8, 16)))]
    FLAGS['hq_ok'] = herm_q and cov and deck_inv and clock_inv and th_inv
    check("T1.1 H_q IS THE THETA-COMPATIBLE FK QUARTIC [exact "
          "Fraction]: H_q = sum_p alpha_1^p(g0 g1 g2 g3) has %d "
          "degree-4 terms (Hermitian: reversal sign +1: %s), is "
          "alpha_1-COVARIANT exactly (%s) hence deck- (%s) and "
          "clock-invariant (%s), and Theta_15-INVARIANT exactly (%s; "
          "K trivial on the rational coefficients, theta-conjugation "
          "= NS signed permutation) with %d cut-crossing terms -- the "
          "canonical Z8 interaction is compatible with the pinned "
          "real structure: kill test 1 does NOT fire at the "
          "Hamiltonian level"
          % (nterms, herm_q, cov, deck_inv, clock_inv, th_inv,
             len(cross)),
          FLAGS['hq_ok'])

    # mark-anchored variants: swap-axis Theta compatibility (m even)
    tab = {}
    for m in (2, 4, 6):
        Hm = h_marks(m)
        row = {}
        for k in (m - 1, m + 7):
            row[k] = dict_eq(sperm_dict(Hm, refl_pm(k)), Hm)
        tab[m] = (row, dict_eq(sperm_dict(Hm, DECK_PM), Hm))
    cw_eq = dict_eq(h_marks(2), h_cw_dict())
    odd_axis_site = all(((mm - 1) % 2 == 0) for mm in (1, 3, 5, 7))
    FLAGS['marks_ok'] = all(all(r.values()) and d for r, d in tab.values())
    FLAGS['cw_eq'] = cw_eq
    check("T2.1 MARK-ANCHORED QUARTICS: THETA-COMPATIBLE ON THE SWAP "
          "AXES [exact Fraction]: H_marks(m) (quartets on the 4 mark "
          "bonds) is invariant under BOTH mark-swap reflection lifts "
          "and the deck for every even member (m = 2: %s, m = 4: %s, "
          "m = 6: %s) -- no symmetrisation needed, the NS wrap signs "
          "assemble to +1; the v512 counterwitness delta_cw = "
          "atan(4/3) anchors to the IDENTICAL Hamiltonian as the "
          "blind member m = 2 (exact dict equality: %s -- the v525 "
          "N2.1 integer incidence, now at the DYNAMICS level); odd m "
          "have site-type swap axes only (k = m-1 even: %s) -- the "
          "known N = 16 placement artifact, typed"
          % (tab[2], tab[4], tab[6], cw_eq, odd_axis_site),
          FLAGS['marks_ok'] and cw_eq and odd_axis_site)

    th_bad = sperm_dict(HBAD, refl_pm(15))
    same = dict_eq(th_bad, HBAD)
    anti = dict_eq(th_bad, cscale(HBAD, Fr(-1)))
    disj = not (set(next(iter(HBAD))) & set(next(iter(th_bad))))
    FLAGS['hbad_incompat'] = (not same) and (not anti)
    check("T3.1 THE THETA-INCOMPATIBLE CONTROL QUARTIC [exact]: "
          "H_bad = g0 g1 g2 g4 is Hermitian but maps under Theta_15 "
          "to the DISJOINT quartet %s (equal: %s, anti: %s, disjoint "
          "supports: %s) -- [Theta, H_bad] != 0 exactly: the control "
          "that gives F1's RP battery teeth"
          % (list(th_bad), same, anti, disj),
          FLAGS['hbad_incompat'] and disj)


def h_cw_dict():
    u = 16.0 * np.arctan(4.0 / 3.0) / np.pi
    b_cw = int(round(u / 2.0))
    H = {}
    for b in (0, b_cw, 8, 8 + b_cw):
        H = cadd(H, quartet(b % N))
    return H


# ===========================================================================
# A -- F1 battery: interacting RP on the bond cut (ground + Gibbs)
# ===========================================================================
def f1_battery():
    print("  -- A: F1 -- interacting RP on the bond cut k = 15")
    basis = basis_of(15)
    Mth = FLAGS['Mth']
    tab = {}
    print("        ground-state ladder:")
    for g in G_LADDER + (-1.0,):
        Hm = FLAGS['HF_MAT'] + g * HQ_MAT
        st, gap, deg, w = ground_state(Hm)
        picks = gram_report(st, 15, basis)
        p = picks[0] if picks else None
        if st[0] == 'pure':
            ov = abs(complex(np.vdot(Mth @ st[1].conj(), st[1])))
        else:
            ov = float('nan')
        tab[g] = (gap, deg, p, ov)
        tagd = '  [diagnostic]' if g < 0 else ''
        print("          g=%-5s gap %.4f deg %d  eta %s herm %.1e  "
              "inertia %s odd %s even %s  min %.3e  |<ThOm,Om>| %.6f%s"
              % (g, gap, deg, p[0] if p else '--',
                 p[1] if p else -1, p[2] if p else '?',
                 p[3] if p else '?', p[4] if p else '?',
                 p[5] if p else -1, ov, tagd), flush=True)
    herm_all = all(tab[g][2] is not None for g in G_LADDER)
    ok_theta_inv = all(abs(tab[g][3] - 1) < 1e-8 for g in G_LADDER
                       if tab[g][1] == 1)
    unique_all = all(tab[g][1] == 1 for g in G_LADDER)
    pd0 = tab[0.0][2] is not None and tab[0.0][2][2] == (37, 0, 0)
    LOCK_G = {0.25: (33, 4, 0), 0.5: (33, 4, 0),
              1.0: (31, 6, 0), 2.0: (29, 8, 0)}
    fail_match = all(tab[g][2][2] == LOCK_G[g] for g in LOCK_G)
    worst = min(float(tab[g][2][6][0]) for g in LOCK_G)
    diag_neg = tab[-1.0][2] is not None and tab[-1.0][2][2][1] > 0
    FLAGS['f1_rp_fails'] = (herm_all and ok_theta_inv and unique_all
                            and pd0 and fail_match)
    FLAGS['f1_tab'] = tab
    check("A1.1 THE CENTRAL F1 DATUM -- INTERACTING RP FAILS ON THE "
          "BOND CUT [float, tol 1e-9; regression-locked]: the OS form "
          "is perfectly WELL-POSED at every g (Gram Hermitian to "
          "1e-15: %s; unique gapped ground states: %s; Theta Omega_g "
          "= Omega_g to 1e-8: %s; g = 0 PD (37,0,0): %s) -- but for "
          "EVERY g > 0 the interacting ground Gram is INDEFINITE: "
          "inertia (33,4,0) at g = 1/4, 1/2, (31,6,0) at g = 1, "
          "(29,8,0) at g = 2 (locked: %s; most negative eigenvalue "
          "%.3e, four orders above the 1e-9 threshold; the free even "
          "sector sits near the RP boundary at 1.78e-6 and the FK "
          "interference pushes through it); the g = -1 diagnostic "
          "fails too (%s: no coupling-sign rescue) -- KILL TEST 2 "
          "FIRES in the toy: reflection positivity is NOT automatic "
          "for Theta-compatible interacting seam dynamics"
          % (herm_all, unique_all, ok_theta_inv, pd0, fail_match,
             worst, tab[-1.0][2][2]),
          FLAGS['f1_rp_fails'] and worst < -1e-5 and diag_neg)

    print("        Gibbs ladder (beta = %.1f):" % BETA)
    gtab = {}
    for g in G_LADDER:
        Hm = FLAGS['HF_MAT'] + g * HQ_MAT
        rho = gibbs_rho(Hm, BETA)
        picks = gram_report(('mix', rho), 15, basis)
        p = picks[0] if picks else None
        gtab[g] = p
        print("          g=%-5s eta %s herm %.1e  inertia %s  min %.3e"
              % (g, p[0] if p else '--', p[1] if p else -1,
                 p[2] if p else '?', p[5] if p else -1), flush=True)
    base_pd = gtab[0.0] is not None and gtab[0.0][2] == (37, 0, 0)
    gibbs_match = all(gtab[g] is not None and gtab[g][2] == LOCK_G[g]
                      for g in LOCK_G)
    FLAGS['f1_gibbs_fails'] = base_pd and gibbs_match
    check("A2.1 THE GIBBS STATE MIRRORS THE FAILURE [float, beta = "
          "%.1f; regression-locked]: the g = 0 thermal baseline is PD "
          "(37,0,0) (%s), and for every g > 0 the KMS Gram carries "
          "EXACTLY the ground-state inertia ladder (33,4,0)/(33,4,0)/"
          "(31,6,0)/(29,8,0) (%s) -- the RP violation is a property "
          "of the INTERACTION, not of the ground-state projection or "
          "the flat-band degeneracy structure ([C] beta choice)"
          % (BETA, base_pd, gibbs_match),
          FLAGS['f1_gibbs_fails'])

    # A4: mechanism decomposition [POST-HOC control, added after run 1,
    # labelled per transparency note; verdict-neutral]
    cross = {mm: c for mm, c in HQ.items()
             if (set(mm) & set(range(8))) and (set(mm) & set(range(8, 16)))}
    hnc = {mm: c for mm, c in HQ.items() if mm not in cross}
    inv_nc = dict_eq(sperm_dict(hnc, refl_pm(15)), hnc)
    inv_cx = dict_eq(sperm_dict(cross, refl_pm(15)), cross)
    res_mech = {}
    for tag, hd in (('half-local', hnc), ('crossing', cross)):
        st_m, gap_m, deg_m, _ = ground_state(
            FLAGS['HF_MAT'] + 1.0 * dict_to_mat(hd))
        picks = gram_report(st_m, 15, basis)
        res_mech[tag] = picks[0] if picks else None
    both_pd = all(p is not None and p[2] == (37, 0, 0)
                  for p in res_mech.values())
    check("A4.1 MECHANISM DECOMPOSITION [float; post-hoc control, "
          "verdict-neutral]: split H_q = half-local (10 terms) + "
          "cut-crossing (6 terms), both Theta_15-invariant exactly "
          "(%s/%s) -- at g = 1 EACH PART ALONE keeps the Gram PD "
          "(37,0,0) (half-local min %.3e, crossing min %.3e) while "
          "the SUM is (31,6,0): the RP violation is an INTERFERENCE "
          "effect between crossing and half-local FK terms, not a "
          "property of either class -- consistent with the "
          "mark-anchored finding (B3.1) that RP fails exactly on "
          "quartet-straddled cuts and survives on quartet-avoiding "
          "ones: RP acts as a nontrivial selector on interacting "
          "seam dynamics"
          % (inv_nc, inv_cx, res_mech['half-local'][5],
             res_mech['crossing'][5]),
          inv_nc and inv_cx and both_pd)

    # negative controls: Theta-incompatible quartic + site cut
    Hm_bad = FLAGS['HF_MAT'] + 1.0 * HBAD_MAT
    st_b, gap_b, deg_b, w_b = ground_state(Hm_bad)
    devs_bad = []
    for eta in (1j, -1j):
        Gb = gram_state(st_b, 15, eta, basis)
        devs_bad.append(herm_dev_mat(Gb))
    site_res = {}
    for g in (0.0, 1.0):
        Hm = FLAGS['HF_MAT'] + g * HQ_MAT
        st, _, _, _ = ground_state(Hm)
        P0 = half_of(0)
        b1 = [(a,) for a in P0]
        best = None
        for eta in (1, -1, 1j, -1j):
            Gs = gram_state(st, 0, eta, b1, sfun=lambda a: 1)
            dev = herm_dev_mat(Gs)
            if dev < TOL_HERM:
                evs = np.linalg.eigvalsh((Gs + Gs.conj().T) / 2)
                it = inertia_num(evs)
                if best is None or it[1] < best[1][1]:
                    best = (eta, it, float(evs.min()))
        site_res[g] = best
    FLAGS['f1_teeth'] = (min(devs_bad) > 1e-3
                         and all(v is not None and (v[1][1] > 0
                                                    or v[1][2] > 0)
                                 for v in site_res.values()))
    check("A3.1 NEGATIVE CONTROLS HAVE TEETH [float]: the "
          "Theta-INCOMPATIBLE quartic g0 g1 g2 g4 destroys "
          "theta-invariance of the ground state -- the OS Gram is "
          "NON-Hermitian for BOTH eta (devs %s vs < 1e-14 for the FK "
          "model): RP is not even well-posed there, quantified; the "
          "SITE cut (k = 0, plain signs) stays non-PD in the "
          "interacting state (g = 0: eta %s inertia %s min %.3f; "
          "g = 1: eta %s inertia %s min %.3f) -- the v519 placement "
          "selection survives the interaction"
          % (['%.3e' % d for d in devs_bad],
             site_res[0.0][0], site_res[0.0][1], site_res[0.0][2],
             site_res[1.0][0], site_res[1.0][1], site_res[1.0][2]),
          FLAGS['f1_teeth'])


# ===========================================================================
# B -- F2 battery: the delta ladder, the explicit side mirror
# ===========================================================================
def cut_bonds(k):
    x = ((k - 1) // 2) % N
    return ((x, (x + 1) % N), ((x + 8) % N, (x + 9) % N))


def straddles(m, k):
    """does any mark quartet of member m contain both endpoints of a
    cut bond of axis k?"""
    for b in (0, m, 8, 8 + m):
        sites = {(b - 2) % N, (b - 1) % N, b % N, (b + 1) % N}
        for (x, y) in cut_bonds(k):
            if x in sites and y in sites:
                return True
    return False


def f2_battery():
    print("  -- B: F2 -- mark-anchored ladder + explicit side mirror")
    # B1: spectra / overlaps ladder, m = 1..7, g in {1/2, 1}
    st0 = FLAGS['state0']
    v0 = st0[1]
    data = {}
    for g in (0.5, 1.0):
        for m in range(1, 8):
            Hm_mat = FLAGS['HF_MAT'] + g * dict_to_mat(h_marks(m))
            st, gap, deg, w = ground_state(Hm_mat)
            par = expec(st, mono_mat(tuple(range(N)))).real
            if st[0] == 'pure':
                ov = abs(complex(np.vdot(v0, st[1])))
            else:
                # degenerate ground space: |P_0 Omega_0| projector norm
                ov = float(np.sqrt(max(
                    np.real(np.vdot(v0, st[1] @ v0)) * deg, 0.0)))
            data[(g, m)] = (np.sort(w), gap, deg, par, ov, float(w[0]))
    print("        delta ladder (g = 1):")
    for m in range(1, 8):
        w0_, gap, deg, par, ov, e0 = data[(1.0, m)]
        print("          m=%d (delta=%dpi/8): E0 %.6f gap %.4f deg %d "
              "<Gamma> %+.4f  |<Om0|Om>| %.6f"
              % (m, m, e0, gap, deg, par, ov), flush=True)
    spread = max(float(np.max(np.abs(data[(1.0, m)][0]
                                     - data[(1.0, mm)][0])))
                 for m in range(1, 8) for mm in range(m + 1, 8))
    FLAGS['f2_sees_delta'] = spread > 1e-3
    side_spec = {(g, m): float(np.max(np.abs(
        data[(g, m)][0] - data[(g, 8 - m)][0])))
        for g in (0.5, 1.0) for m in (1, 2, 3)}
    side_ov = {(g, m): abs(data[(g, m)][4] - data[(g, 8 - m)][4])
               for g in (0.5, 1.0) for m in (1, 2, 3)}
    side_e0 = {(g, m): abs(data[(g, m)][5] - data[(g, 8 - m)][5])
               for g in (0.5, 1.0) for m in (1, 2, 3)}
    check("B1.1 THE DECORATION SEES delta -- SPECTRA/OVERLAPS LADDER "
          "[float, g = 1/2 and 1]: the 256-level spectra genuinely "
          "depend on the member (max pairwise spread %.4f > 1e-3 at "
          "g = 1: %s -- the mark-anchored quartic carries delta into "
          "the DYNAMICS, beyond every Wick-computable decoration); "
          "side comparison m vs 8-m over both g: spectra agree to "
          "%.1e, vacuum overlaps to %.1e, ground energies to %.1e -- "
          "delta-dependence everywhere, side-difference nowhere (the "
          "v525 bar, interacting edition)"
          % (spread, FLAGS['f2_sees_delta'],
             max(side_spec.values()), max(side_ov.values()),
             max(side_e0.values())),
          FLAGS['f2_sees_delta']
          and max(side_spec.values()) < TOL_ZERO
          and max(side_ov.values()) < 1e-8)
    FLAGS['f2_side_specs'] = (max(side_spec.values()),
                              max(side_ov.values()))

    # B2: the EXPLICIT side mirror (anti-unitary).  The exact carrier
    # is the MARK-AXIS reflection Theta_15 (z -> conj(z), fixing the
    # marks +-1, mapping delta -> -delta ~ pi - delta); the midpoint
    # axis Theta_7 is checked as the secondary torsor member.
    pm15 = refl_pm(15)
    mir15 = all(dict_eq(sperm_dict(h_marks(m), pm15), h_marks(8 - m))
                for m in (1, 2, 3, 4))
    Cm = sp.Matrix(N, N, lambda a, b: c_of(a - b))
    anti_ok = True
    for kax in (15, 7):
        Rk = sp.Matrix(refl_matrix(N, kax, -1))
        anti_ok &= sp.simplify(Rk * Cm * Rk.T + Cm) == sp.zeros(N, N)
    Mth = FLAGS['Mth']
    Mthinv = Mth.conj()
    dev_free = float(np.max(np.abs(
        Mth @ FLAGS['HF_MAT'].conj() @ Mthinv - FLAGS['HF_MAT'])))
    dev_mark = max(float(np.max(np.abs(
        Mth @ dict_to_mat(h_marks(m)).conj() @ Mthinv
        - dict_to_mat(h_marks(8 - m))))) for m in (1, 2, 3, 4))
    pm7 = refl_pm(7)
    diff7 = {m: sorted(cadd(sperm_dict(h_marks(m), pm7),
                            cscale(h_marks(8 - m), Fr(-1))).keys())
             for m in (1, 2, 3, 4)}
    ok7 = (diff7[2] == [] and diff7[3] == [] and diff7[4] == []
           and diff7[1] == [(0, 13, 14, 15), (5, 6, 7, 8)])
    FLAGS['f2_equivariance'] = (mir15 and anti_ok and dev_free < 1e-10
                                and dev_mark < 1e-10)
    check("B2.1 THE SIDE MIRROR, CONSTRUCTED EXPLICITLY [exact "
          "Fraction + sympy + matrix]: the anti-unitary MARK-AXIS "
          "reflection Theta_15 = U_r15 o K (the OS Theta itself; "
          "z -> conj(z) maps M(delta) -> M(pi - delta)) carries "
          "H_marks(m) -> H_marks(8-m) EXACTLY for ALL m = 1..4 "
          "(signed-permutation dict identity, no gauge needed: %s), "
          "preserves H_free (R C R^T = -C exact for k = 15 and 7: "
          "%s + anti-linearity; matrix dev %.1e) and the matrix "
          "conjugation reproduces the mirror Hamiltonians to %.1e "
          "-- the two sides of every mark configuration are "
          "ANTI-UNITARILY EQUIVALENT in the interacting model: "
          "every invariant readout is forced mirror-equal (the "
          "exact blindness mechanism).  Torsor structure: the "
          "MIDPOINT-axis mirror Theta_7 is exact for m = 2, 3, 4 "
          "but obstructed for the tightest pair m = 1 <-> 7 by "
          "exactly two NS wrap signs (flipped quartets %s; no "
          "C-preserving site gauge can remove them -- C(d) != 0 for "
          "every odd d forces a uniform gauge): the side mirror is "
          "PINNED to the mark-axis clock orbit of the v519 torsor"
          % (mir15, anti_ok, dev_free, dev_mark, diff7[1]),
          FLAGS['f2_equivariance'] and ok7)

    # B3: RP Gram ladder on the swap axes (m even): the straddle law
    print("        Gram ladder (swap axes, ground states):")
    gram_tab = {}
    law_ok = True
    for m in (2, 4, 6):
        for g in (0.25, 0.5, 1.0, 2.0):
            Hm_mat = FLAGS['HF_MAT'] + g * dict_to_mat(h_marks(m))
            st, gap, deg, w = ground_state(Hm_mat)
            for k in ((m - 1) % N, (m + 7) % N):
                picks = gram_report(st, k, basis_of(k))
                p = picks[0] if picks else None
                gram_tab[(m, g, k)] = p
                if p is None:
                    law_ok = False
                elif straddles(m, k):
                    law_ok &= p[2][1] > 0
                else:
                    law_ok &= p[2][1] == 0 and p[2][2] == 0
        for k in ((m - 1) % N, (m + 7) % N):
            seq = " ".join(str(gram_tab[(m, g, k)][2])
                           for g in (0.25, 0.5, 1.0, 2.0))
            print("          m=%d axis %2d [%s]: %s"
                  % (m, k, 'straddled' if straddles(m, k)
                     else 'avoiding ', seq), flush=True)
    pd_mins = [p[5] for (mm, g, k), p in gram_tab.items()
               if p and not straddles(mm, k)]
    # mirror pairing under Theta_15: axis k -> (14 - k) mod 16
    mdev = []
    for g in (0.25, 0.5, 1.0, 2.0):
        for (k2, k6) in ((1, 13), (9, 5)):
            a = gram_tab[(2, g, k2)]
            b = gram_tab[(6, g, k6)]
            if a and b:
                mdev.append(float(np.max(np.abs(a[6] - b[6]))))
    # delta-dependence among the WELL-POSED (quartet-avoiding) members
    gdev = []
    for g in (0.25, 0.5, 1.0, 2.0):
        a = gram_tab[(2, g, 9)]
        b = gram_tab[(4, g, 3)]
        if a and b:
            gdev.append(float(np.max(np.abs(a[6] - b[6]))))
    # odd members: no bond swap axis -- the Gram is not well-posed
    Hm1 = FLAGS['HF_MAT'] + 1.0 * dict_to_mat(h_marks(1))
    st1, _, _, _ = ground_state(Hm1)
    dev_odd = min(herm_dev_mat(gram_state(st1, 0, eta, basis_of(0),
                                          sfun=lambda a: 1))
                  for eta in (1, -1, 1j, -1j))
    FLAGS['f2_gram_law'] = law_ok
    FLAGS['f2_gram_mirror'] = max(mdev) if mdev else float('nan')
    check("B3.1 INTERACTING RP-GRAM LADDER: THE STRADDLE LAW [float]: "
          "over ALL (m, g, axis) in {2,4,6} x {1/4,1/2,1,2} x both "
          "swap axes, the Gram is PD exactly on the QUARTET-AVOIDING "
          "cuts (min eigenvalues %.3e .. %.3e) and INDEFINITE exactly "
          "on the quartet-STRADDLED cuts (law holds on all 24 "
          "entries: %s) -- the interacting RP datum depends on (m, g) "
          "(max spectral dev between PD members m = 2 and m = 4: "
          "%.3e), and the Theta_15 mirror pairs (m=2, axis k) vs "
          "(m=6, axis 14-k) have IDENTICAL spectra (max dev %.1e -- "
          "equivariance confirmed on the RP data, straddled and "
          "avoiding alike); the odd members have no bond swap axis "
          "(best Hermiticity dev %.2f -- the typed v521/v525 "
          "placement artifact); the counterwitness = m = 2 "
          "identically (T2.1) -- positivity becomes delta-dependent "
          "and cut-dependent but NEVER side-sensitive"
          % (min(pd_mins), max(pd_mins), law_ok,
             max(gdev) if gdev else -1,
             max(mdev) if mdev else -1, dev_odd),
          law_ok and (max(mdev) if mdev else 1) < 1e-8
          and (max(gdev) if gdev else 0) > 1e-6 and dev_odd > 1e-3)


# ===========================================================================
# C -- F3 battery: parity, tower, FK anchor, OS quotient at g > 0
# ===========================================================================
def f3_battery():
    print("  -- C: F3 -- FK class + OS quotient at g > 0")
    Gm = mono_mat(tuple(range(N)))
    tab = FLAGS['f1_tab']
    pars = {}
    for g in G_LADDER:
        Hm = FLAGS['HF_MAT'] + g * HQ_MAT
        st, gap, deg, w = ground_state(Hm)
        pars[g] = (expec(st, Gm).real, deg)
    Hm100 = FLAGS['HF_MAT'] + 100.0 * HQ_MAT
    st100, gap100, deg100, w100 = ground_state(Hm100)
    par100 = expec(st100, Gm).real
    comm_dev = float(np.max(np.abs(HQ_MAT @ Gm - Gm @ HQ_MAT)))
    even_ok = all(len(m) % 2 == 0 for m in HQ)
    lv1 = levels(np.linalg.eigvalsh(FLAGS['HF_MAT'] + HQ_MAT)[:20])
    FLAGS['f3_grading'] = (even_ok and comm_dev < 1e-10
                           and all(abs(abs(p[0]) - 1) < 1e-8
                                   for p in pars.values()))
    check("C1.1 GRADING + CLASS SURVIVE THE INTERACTION [exact + "
          "float]: H_q is even (all terms degree 4: %s, [H_q, "
          "(-1)^F] dev %.1e), the ground state has DEFINITE parity "
          "<Gamma> at every g (%s; g = 100: %+.4f, deg %d) -- the "
          "GSO grading survives; combined with M3.1 (Utilde^2 = 256 "
          "Gamma exact, V^2 prop Utilde, conj_V V = 4096): the "
          "NONSPLIT U^2 = (-1)^F class and the full Z8 clock tower "
          "are carried UNCHANGED by the interacting model -- the "
          "v510 central-arrangement class is interaction-stable "
          "(low levels at g = 1: %s)"
          % (even_ok, comm_dev,
             {g: '%+.3f/deg%d' % (pars[g][0], pars[g][1])
              for g in (0.5, 1.0, 2.0)},
             par100, deg100,
             [(round(e, 4), d) for e, d in lv1[:4]]),
          FLAGS['f3_grading'] and abs(abs(par100) - 1) < 1e-6)

    # FK anchor: single quartet; m = 4 disjoint quartets at g -> inf
    wq = np.linalg.eigvalsh(dict_to_mat(quartet(2)))
    lq = levels(wq)
    ok_q = (len(lq) == 2 and abs(lq[0][0] + 1) < 1e-12
            and abs(lq[1][0] - 1) < 1e-12
            and lq[0][1] == 128 and lq[1][1] == 128)
    w4 = np.linalg.eigvalsh(dict_to_mat(h_marks(4)))
    l4 = levels(w4)
    tgt = [(-4.0, 16), (-2.0, 64), (0.0, 96), (2.0, 64), (4.0, 16)]
    ok_4 = (len(l4) == 5
            and all(abs(l4[i][0] - tgt[i][0]) < 1e-10
                    and l4[i][1] == tgt[i][1] for i in range(5)))
    FLAGS['f3_anchor'] = ok_q and ok_4
    check("C2.1 FK ANCHOR [float, exact targets]: a single quartet "
          "g_a g_b g_c g_d has spectrum {-1, +1} x 128 exactly (%s); "
          "the m = 4 (delta = pi/2) mark-anchored interaction alone "
          "is 4 DISJOINT commuting quartets with the exact binomial "
          "ladder E in {-4,-2,0,2,4}, multiplicities {16,64,96,64,"
          "16} (%s: %s) -- the g -> infinity limit is the FK "
          "fixed-point structure, qualitatively confirmed"
          % (ok_q, ok_4, [(round(e, 6), d) for e, d in l4]),
          FLAGS['f3_anchor'])

    # OS quotient at g > 0 -- (i) translation-invariant model: typed
    # degeneration; (ii) constructive witness on the delta = pi/2
    # mark-anchored model [C3.2 POST-HOC, labelled; verdict logic per
    # the frozen F3(d) letter]
    basis = basis_of(15)
    null_ok = all(tab[g][2][2][2] == 0 for g in G_LADDER if tab[g][2])
    indef = all(tab[g][2][2][1] > 0 for g in (0.25, 0.5, 1.0, 2.0))
    D4 = [m for m in basis if all(8 <= a <= 11 for a in m)]
    r15, s15 = refl_map(15)
    res4 = {}
    sub_in = {}
    for g in (0.5, 1.0):
        Hm = FLAGS['HF_MAT'] + g * HQ_MAT
        st, _, _, _ = ground_state(Hm)
        inv_dev = 0.0
        for mwit in ((8, 9), (9,), (8, 11)):
            cb, mb = alpha_mono(mwit, TW[1])
            inv_dev = max(inv_dev, abs(
                expec(st, mono_mat(mwit))
                - cb * expec(st, mono_mat(mb))))
        T4 = np.zeros((len(D4), len(D4)), dtype=complex)
        for a, ma in enumerate(D4):
            ca, ta = theta_mono_num(ma, r15, s15, 1j)
            Ma = mono_mat(ta)
            for b, mb_ in enumerate(D4):
                cb, mb4 = alpha_mono(mb_, TW[4])
                T4[a, b] = ca * cb * expec(st, Ma @ mono_mat(mb4))
        dev4 = herm_dev_mat(T4)
        evs4 = np.linalg.eigvalsh((T4 + T4.conj().T) / 2)
        G15 = gram_state(st, 15, 1j, basis)
        idxmap = [basis.index(m) for m in D4]
        vac_dev = float(np.max(np.abs(T4[0, :] - G15[0, idxmap])))
        Gh = (G15 + G15.conj().T) / 2
        sub_in[g] = inertia_num(np.linalg.eigvalsh(
            Gh[np.ix_(idxmap, idxmap)]))
        res4[g] = (inv_dev, dev4, inertia_num(evs4),
                   float(evs4.min()), vac_dev)
        print("          trans-inv tau_4 g=%.1f: alpha-inv %.1e herm "
              "%.1e inertia %s min %.3e vac-row %.1e | D4 sub-Gram %s"
              % (g, inv_dev, dev4, res4[g][2], res4[g][3], vac_dev,
                 sub_in[g]), flush=True)
    ok_t4 = all(v[0] < 1e-8 and v[1] < 1e-8 and v[2] == (11, 0, 0)
                and v[4] < 1e-8 for v in res4.values())
    sub_indef = all(v == (9, 2, 0) for v in sub_in.values())
    FLAGS['f3_transinv_typed'] = null_ok and indef and ok_t4 \
        and sub_indef
    check("C3.1 TRANS-INVARIANT MODEL: THE QUOTIENT DEGENERATION IS "
          "THE F1 DATUM [float, typed]: the 37-Gram has null space "
          "{0} at every g (%s) but is INDEFINITE for g > 0 (A1.1: "
          "%s), and the indefiniteness reaches the deep-interior "
          "Klein-Landau domain (D4 sub-Gram (9,2,0) at g = 1/2 and "
          "1: %s) -- NO pre-Hilbert quotient exists for the "
          "translation-invariant FK model on the (always straddled) "
          "bond cut; the clock-step FORM data nonetheless stay "
          "exactly Hermitian, PD and vacuum-fixed on the domain "
          "(tau_4: %s / %s, alpha-invariance to %.1e) -- the "
          "degeneration is exactly the F1 RP finding at quotient "
          "level, typed here, NOT a second kill"
          % (null_ok, indef, sub_indef, res4[0.5][2], res4[1.0][2],
             max(v[0] for v in res4.values())),
          FLAGS['f3_transinv_typed'])

    # C3.2: constructive witness -- delta = pi/2 mark-anchored model,
    # quartet-avoiding swap axis k = 3
    h4 = h_marks(4)
    clock4 = dict_eq(sperm_dict(h4, CLOCK_PM), h4)
    deck4 = dict_eq(sperm_dict(h4, DECK_PM), h4)
    H4_MAT = dict_to_mat(h4)
    r3, s3 = refl_map(3)
    basis3 = basis_of(3)
    D43 = [m for m in basis3 if all(2 <= a <= 5 for a in m)]
    res_w = {}
    for g in (0.5, 1.0):
        st, gap, deg, _ = ground_state(FLAGS['HF_MAT'] + g * H4_MAT)
        picks = gram_report(st, 3, basis3)
        p = picks[0] if picks else None
        inv_dev = 0.0
        for mwit in ((2, 3), (3,), (2, 5)):
            cb, mb = alpha_mono(mwit, TW[4])
            inv_dev = max(inv_dev, abs(
                expec(st, mono_mat(mwit))
                - cb * expec(st, mono_mat(mb))))
        T4 = np.zeros((len(D43), len(D43)), dtype=complex)
        for a, ma in enumerate(D43):
            ca, ta = theta_mono_num(ma, r3, s3, 1j)
            Ma = mono_mat(ta)
            for b, mb_ in enumerate(D43):
                cb, mb4 = alpha_mono(mb_, TW[4])
                T4[a, b] = ca * cb * expec(st, Ma @ mono_mat(mb4))
        dev4 = herm_dev_mat(T4)
        evs4 = np.linalg.eigvalsh((T4 + T4.conj().T) / 2)
        G3 = gram_state(st, 3, 1j, basis3)
        idx3 = [basis3.index(m) for m in D43]
        vac_dev = float(np.max(np.abs(T4[0, :] - G3[0, idx3])))
        res_w[g] = (p, inv_dev, dev4, inertia_num(evs4),
                    float(evs4.min()), vac_dev)
        print("          m=4 witness g=%.1f: Gram %s min %.3e | tau_4 "
              "herm %.1e inertia %s min %.3e vac-row %.1e "
              "alpha4-inv %.1e"
              % (g, p[2] if p else '?', p[5] if p else -1, dev4,
                 res_w[g][3], res_w[g][4], vac_dev, inv_dev),
              flush=True)
    ok_w = all(v[0] is not None and v[0][2] == (37, 0, 0)
               and v[1] < 1e-8 and v[2] < 1e-8 and v[3] == (11, 0, 0)
               and v[5] < 1e-8 for v in res_w.values())
    FLAGS['f3_quotient'] = FLAGS['f3_transinv_typed'] and clock4 \
        and deck4 and ok_w
    check("C3.2 CONSTRUCTIVE QUOTIENT WITNESS AT g > 0 [float; "
          "post-hoc, labelled]: the delta = pi/2 mark-anchored FK "
          "model (the pinned physical member) is clock- and "
          "deck-invariant EXACTLY (%s/%s), its ground Gram on the "
          "quartet-avoiding swap axis k = 3 is PD (37,0,0) at g = "
          "1/2 and 1 (min %.3e / %.3e) -- H_phys EXISTS, dim 37, "
          "null space {0} -- and the interacting clock transfer "
          "step tau_4 on the domain {2..5} (11 monomials) is "
          "Hermitian and PD (11,0,0) (min %.3e / %.3e; vacuum row "
          "fixed to %.1e; omega_g alpha_4-invariant to %.1e): the "
          "v524 OS quotient + implementable clock SURVIVE the "
          "interaction in the quartet-compatible geometry"
          % (clock4, deck4, res_w[0.5][0][5], res_w[1.0][0][5],
             res_w[0.5][4], res_w[1.0][4],
             max(v[5] for v in res_w.values()),
             max(v[1] for v in res_w.values())),
          clock4 and deck4 and ok_w)


# ===========================================================================
# V -- the three frozen verdicts
# ===========================================================================
def verdicts():
    print("  -- V: preregistered verdicts")
    theta_ok = FLAGS['tower_ok'] and FLAGS['hq_ok']
    rp_fails = FLAGS['f1_rp_fails'] and FLAGS['f1_gibbs_fails']
    teeth = FLAGS['f1_teeth'] and FLAGS['free_ok']
    if not theta_ok:
        v1 = 'KILL'
    elif rp_fails and teeth:
        v1 = 'KILL'
    elif teeth:
        v1 = 'ERFOLG'
    else:
        v1 = 'UNENTSCHIEDEN'
    FLAGS['V1'] = v1
    check("V1.1 F1 VERDICT = %s [frozen logic]: KILL TEST 1 does NOT "
          "fire -- Theta exists with Theta^2 = +1 and clock-tower "
          "inversion ON the interacting model (M2.1/M3.1 exact, "
          "[Theta, H_g] = 0 exact, Theta-invariant ground states); "
          "but KILL TEST 2 FIRES: reflection positivity FAILS on the "
          "bond cut in the interacting ground state for every g > 0 "
          "((33,4,0) -> (29,8,0)) and identically in the Gibbs state "
          "(A1.1/A2.1), with exact g = 0 regression (R1.1) and "
          "toothed controls (A3.1/A4.1) -- THE FIRST SHARP AMMUNITION "
          "AGAINST THE WOIT ROUTE: on the first genuinely interacting "
          "seam model, RP is NOT automatic; it fails by an "
          "interference mechanism (A4.1) and survives only on "
          "quartet-avoiding cuts (B3.1).  FENCE: one interaction "
          "class on one 16-Majorana toy with a [C] flat-band parent "
          "-- this NARROWS the route (any A_hol must protect RP "
          "against exactly this mechanism; RP becomes a nontrivial "
          "selector on the interaction), it does not close it; the "
          "contract kill test on the continuum A_hol stays formally "
          "open" % v1,
          v1 == 'KILL' and theta_ok and rp_fails)

    side_max = max(FLAGS['f2_side_specs'][0], FLAGS['f2_side_specs'][1],
                   FLAGS['f2_gram_mirror'])
    equiv = FLAGS['f2_equivariance'] and FLAGS['f2_gram_law']
    if equiv and side_max < TOL_ZERO * 10:
        v2 = 'KILL'
    elif (not FLAGS['f2_equivariance']) and side_max > 1e-6:
        v2 = 'ERFOLG'
    else:
        v2 = 'UNENTSCHIEDEN'
    FLAGS['V2'] = v2
    check("V2.1 F2 VERDICT = %s [frozen logic; mirror "
          "operationalisation deviation documented -- the exact "
          "carrier is the mark-axis Theta_15, see B2.1]: the "
          "explicit anti-unitary side mirror maps H(m) -> H(8-m) "
          "EXACTLY (Fraction identity, all m, no gauge) -- "
          "equivariance; machine-confirmed: ALL canonical side data "
          "(256-level spectra, vacuum overlaps, RP-Gram spectra "
          "across the mirror pairs) agree to %.1e.  The interaction "
          "DOES carry delta into spectra and RP data (B1.1/B3.1 -- "
          "beyond every Wick-computable class, past the v525 bar), "
          "but NO datum distinguishes the sides: the TENTH "
          "side-blind test on the v512 scoreboard, the FIRST with "
          "genuinely interacting (non-quasi-free) dynamics.  The "
          "alignment bit (tau = i <-> delta = pi/2) remains genuine "
          "discrete input; the door narrows to: interacting seam "
          "dynamics whose mirror covariance is broken in BOTH "
          "torsor orbits (the FK class breaks only the midpoint "
          "orbit, and only for m = 1 <-> 7)"
          % (v2, side_max), v2 == 'KILL')

    ok3 = (FLAGS['f3_grading'] and FLAGS['tower_ok']
           and FLAGS['f3_anchor'] and FLAGS['f3_quotient'])
    v3 = 'ERFOLG' if ok3 else ('KILL' if not FLAGS['f3_quotient']
                               else 'UNENTSCHIEDEN')
    FLAGS['V3'] = v3
    check("V3.1 F3 VERDICT = %s [frozen logic]: the interacting "
          "ground state carries the expected Z8/FK class -- grading "
          "+ definite parity at every g incl. g = 100 (C1.1), the "
          "exact tower backbone Utilde^2 = 256 Gamma = (-1)^F "
          "(nonsplit), V^2 = 256 Utilde, conj_V V = 4096 (M3.1), "
          "the FK fixed-point anchor (C2.1); the v524 OS quotient "
          "survives g > 0 CONSTRUCTIVELY on the delta = pi/2 "
          "mark-anchored model (H_phys PD dim 37, clock step "
          "(11,0,0), C3.2), while the translation-invariant model's "
          "quotient degeneration is exactly the F1 RP datum (C3.1, "
          "typed there, not double-counted) -- the toy is in the "
          "nontrivial FK class AND OS-reconstructible where RP "
          "holds: SEAM.EQUIV gains its first interacting data "
          "point.  [C] fence: lattice toy, qualitative quotient "
          "checks only" % v3, v3 == 'ERFOLG')

    check("V4.1 HONEST FENCES [typed]: every model choice ([C]): "
          "quartic form (NS-covariant FK), mark anchoring rule, "
          "flat-band parent H_free, beta = 2, float-track "
          "tolerances; the F1 KILL is TOY-LEVEL ammunition -- it "
          "shows RP is a nontrivial constraint on interacting seam "
          "dynamics, NOT a theorem about the continuum A_hol; "
          "NOTHING here constructs A_hol -- the seven contract kill "
          "tests stay formally live there; no extrapolation "
          "claimed; sandbox only, no marker moves", True)


# ---------------------------------------------------------------------------
def run():
    reset()
    print("v529 SEAM.INT.FKTOY.01 -- the minimal interacting Fidkowski-Kitaev seam toy"
          "model -- Fidkowski-Kitaev quartic on the 16-Majorana NS "
          "seam circle (256-dim, exact)")
    print("  F1 WOIT kill tests 1+2 | F2 alignment-bit side test | "
          "F3 FK class + OS quotient")
    print("=" * 100)
    mach()
    regression()
    theta_compat()
    f1_battery()
    f2_battery()
    f3_battery()
    verdicts()
    npass = sum(RESULTS)
    print("=" * 100)
    print("SUMMARY: %d/%d checks passed%s   [runtime %.1f s]"
          % (npass, len(RESULTS),
             "" if npass == len(RESULTS) else "  -- FAILURES PRESENT",
             time.perf_counter() - T0))
    print("VERDICTS: F1 = %s | F2 = %s | F3 = %s"
          % (FLAGS.get('V1', '?'), FLAGS.get('V2', '?'),
             FLAGS.get('V3', '?')))
    return summary("v529 SEAM.INT.FKTOY.01: F1=KILL (RP breaks for every g>0 on the bond cut -- first firing Kill-Test-2 toy shadow; straddle law 24/24; Theta exists so Kill-Test-1 does NOT fire); F2=KILL (TENTH side-blind test 9->10: Theta_15 mirrors H(m)->H(8-m) EXACTLY despite delta-seeing spectra); F3=ERFOLG (grading + Z8 tower + FK anchor + constructive OS quotient at pi/2); [C] fence one toy / one interaction class -- narrows WOIT route, does NOT close it; WOIT.OS.TWISTOR.01 stays Open; no marker moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
