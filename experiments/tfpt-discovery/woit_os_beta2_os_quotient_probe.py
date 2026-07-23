"""woit_os_beta2_os_quotient_probe.py -- EXPLORATION ONLY (WOIT-beta2
sandbox).  Nothing in verification/, ledger, papers, changelog, website or
scorecard is touched; WOIT.OS.TWISTOR.01 stays [O] regardless of the
outcome below.  No files are written; standalone; deterministic.

=== PREREGISTRATION (frozen BEFORE the run; criteria not adjusted after) ===

Contract basis (tfpt_research_contracts.tex, WOIT.OS.TWISTOR.01):
  beta_2 milestone, verbatim: "The OS quotient of the *free* system made
  explicit --- success: (H, Omega) constructed from the v519 bond-cut form
  with the clock acting unitarily; kill: the quotient degenerates (zero or
  indefinite completion)."
  Precision (iii) (from v522, verbatim): "the clock is the euclidean
  rotation itself (timelike: all 16 seam mirror axes invert it, none
  commutes), and its equivariant statement moves to beta_2 --- OS quotient
  first, then the clock as reconstructed transfer operator."

[C] operationalisations (declared; contract wording prevails where it
exists, the attack-shape criteria (a)-(d) are [C]-refinements):
 [C-1] free system = the v519-pinned 16-Majorana chiral NS seam circle;
   both v519 levels: N = 16 at deg <= 2 (37 = 1 + 8 + 28 monomials on the
   half) AND the complete 2^4 = 16-monomial half algebra at N = 8.  OS
   reflection = the v519 bond cut (axis k = 15 resp. k = 7, NS spin
   signs, twist eta = +i as forced by v519 R3/R5.1).
 [C-2] H_phys := A_+ / N with N = {a : <theta(a) Omega, a Omega> = 0} =
   the kernel of the PSD OS Gram; "explicit" = basis + Gram + dimension.
   Nondegeneracy certificates: exact Hermiticity + 40-digit inertia
   (mp.mp.dps = 40, zero threshold 1e-25) with the minimum eigenvalue
   printed; exact 2x2 sub-determinants where cheap.  KILL branch
   (contract verbatim): a negative direction (indefinite completion) or
   rank <= 1 (zero completion beyond the vacuum).
 [C-3] transfer = the Klein-Landau LOCAL symmetric semigroup of the
   euclidean one-step rotation alpha_1 (2 pi / N): T(k)[b] := [alpha_k b]
   on the domain D_k := monomials supported in {cut+1, ..., far-cut - k}
   (the shifted support must stay in the half).  Success-checks:
   (a) tau_k(a,b) = omega(theta(a) alpha_k(b)) is EXACTLY Hermitian on
   D_k x D_k for all 1 <= k <= N/2 - 1 (self-adjointness via Theta on
   the good domain); (b) semigroup consistency <[alpha_j a],[alpha_k b]>
   = tau_{j+k}(a,b) exactly, and the vacuum is fixed exactly
   (tau_k(1,.) = Gram(1,.)); (c) positivity PATTERN (pre-derived, to be
   machine-confirmed): for EVEN k the exact A*A identity tau_k(a,b) =
   Gram(alpha_{k/2} a, alpha_{k/2} b) forces tau_k >= 0; for ODD k the
   effective reflection axis 15 - k is a SITE axis and the chiral
   checkerboard C(even) = 0 forces an exactly ZERO one-particle diagonal
   -> indefinite (or degenerate on too-small domains): the one-step
   transfer is NOT positive -- this is the v519 site/bond dichotomy
   resurfacing INSIDE the semigroup and is typed as the free chirality
   datum (kill-test-3 shadow), NOT as a beta_2 failure; (d) CONTRACTION
   (0 < T <= 1): PRE-DECLARED EXPECTED DEVIATION -- on the compact
   euclidean circle the reconstruction is THERMAL (KMS; H_phys at N = 8
   has dim 16 = 4^2, a doubled/two-sided space) and the local transfer
   need NOT be a contraction: exact witnesses derived pre-run: the norm
   drift ||[g_7]||^2 / ||[g_5]||^2 = C(1)/C(3) = 1 + sqrt(2) = the
   SILVER RATIO delta_S (exact) at N = 8, and at N = 16 the odd
   one-particle clock block has det(G - tau_4) < 0 exactly, so the
   compressed clock has an eigenvalue > 1 (predicted ~1.64).
   Contraction failure with EXACTLY these witnesses is a typed KMS
   finding and does NOT block success (the contract demands no
   contraction); any OTHER failure mode -> UNDECIDED.
 [C-4] the clock: quarter turn = alpha_{N/4} = T(N/4), an EVEN step ->
   positive by (c).  Success: tau_{N/4} on D_{N/4} exactly Hermitian AND
   positive definite (40-digit inertia; at the one-particle level EXACT
   PD certificates via 2x2 trace/det with the exact identities
   C(9) = C(7), C(11) = C(5) at N = 16); the exact form identity
   tau_{N/4}(a,b) = Gram(alpha_{N/8} a, alpha_{N/8} b) ("quarter turn =
   T^{N/4}, with square root A_{N/8}"); spectral projections of the
   compressed clock well-defined (eigendecomposition residuals < 1e-30
   at 40 digits) -- EXACTLY what failed pre-quotient in v522 (the
   non-Hermitian clock average has no spectral calculus); the
   reconstructed rotation one-parameter group U(s) := exp(i s H_c),
   H_c := -log(compressed clock) (PD required), unitary with the
   semigroup law (residuals < 1e-30) -- per precision (iii) this IS the
   [C]-operationalisation of the contract phrase "the clock acting
   unitarily".  PRE-DERIVED EXACT ANCHOR (to be machine-confirmed): at
   N = 8 the compressed clock spectrum is EXACTLY {1, sqrt(2) - 1} =
   {1, 1/delta_S} (each twice: even + odd sector) -- the silver ratio
   of the v519 silver-midpoint axes; at N = 16 the known free trig
   kernel gives the spectrum (40-digit certificates, vacuum eigenvalue
   exactly 1).
 [C-5] GSO / Theta on H_phys: (i) fermion parity descends to a
   G-unitary P with P^2 = 1 commuting with all transfer data (grading
   survives: H_phys = H_even (+) H_odd exactly orthogonal); (ii) the OS
   Theta itself maps A_+ -> A_- (support census) -- it does NOT act on
   H_phys (it IS the metric); the anti-unitary that DOES descend is the
   PERPENDICULAR torsor mirror theta_perp (axis k_cut - N/2, the other
   clock orbit of the v519 mu4 torsor W-S2.5): Theta_phys[a] :=
   [theta_perp(a)], anti-unitarity <Theta a, Theta b> = <b, a> checked
   exactly entrywise, eta_perp pinned inside mu4 by the census;
   Theta_phys^2 measured exactly per parity sector (Kramers question IN
   the quotient); theta_perp alpha_k = alpha_{-k} theta_perp exactly
   (Theta_phys time-reverses the semigroup); theta_cut o theta_perp =
   the deck/antipode lift exactly (the torsor closes onto the deck).
   Success (d): anti-unitary descent exists, GSO grading survives,
   Theta_phys^2 = +1 at least on H_even.
 [C-6] negative controls (all mandatory): (i) SITE cut -> the OS form is
   indefinite (contract kill branch fires for the site placement;
   negative directions counted at N = 16 one-particle (3,3,1) regression
   and N = 8 full site-half algebra); (ii) FAMILY A (clock-centralising
   antipode, alternating dressing) -> Hermitian only for a sub-torsor
   eta and INDEFINITE ((4,4,0) one-particle regression): no PSD form,
   no quotient; (iii) DECK candidate Theta_t = Utilde o K (Kramers class
   (-1)^F): support census shows it maps A_+ to A_- -> it does not act
   on H_phys at all; the descended real structure is the torsor partner
   with Theta_phys^2 measured (the Kramers dichotomy resolved in the
   quotient); (iv) WRONG semigroup direction (alpha_{-1} on the
   UNSHRUNK domain): Hermiticity must FAIL with wrap-overlap witnesses
   (the v522 mechanism localised: no-overlap entries must all match,
   anti-matching entries must all have overlap), while the mirrored
   domain is Hermitian with the mirror inertia; (v) ANTI-CHIRAL state
   (chi = -1): the odd block flips to negative definite -> the FULL
   half-algebra Gram is indefinite: the OS quotient EXISTS ONLY for the
   chirality matching the twist (the kill-test-3 shadow at quotient
   level, quantified).
 [C-7] verdict logic (frozen): KILL iff (K1) a bond-cut Gram at either
   level is indefinite or rank <= 1 [contract kill], or (K2) the clock
   step on its domain is non-Hermitian or has a negative direction
   [clock not implementable on H_phys].  SUCCESS iff no kill AND all of:
   S1 = H_phys explicit + nondegenerate (both levels); S2 = local
   transfer exactly Hermitian on all domains + semigroup identities +
   vacuum fixed; S3 = clock PD + spectral projections + T^{N/4} square
   identity + reconstructed unitary rotation group; S4 = GSO grading +
   anti-unitary Theta descent; S5 = all five controls behave as typed;
   the [C-3](d) contraction deviation counts as SUCCESS-compatible ONLY
   with exactly the pre-declared witnesses.  Otherwise UNDECIDED with
   the gap named.  Runtime target < 20 min.

=== FINDINGS (from the frozen-prereg run, 2026-07-23; 20/20) ===

VERDICT: SUCCESS (beta2, [C]-typed per contract precision (iii)); the
contract kill branch does NOT fire.  Headline numbers:
  * H_phys explicit and NONDEGENERATE: null space N = {0} at both
    levels -- N = 16 deg <= 2: 37 = 29 (+) 8, Gram PD (min eigenvalue
    1.7801e-6 at 40 digits); N = 8 complete half algebra: 16 = 8 (+) 8
    = 4^2, PD (min 3.3471e-3), with exact 2x2 certificates via
    sin^2(3pi/8) - sin(pi/8) sin(5pi/8) = 1/2.
  * Local transfer (Klein-Landau): tau_k exactly Hermitian on every
    domain D_k (k = 1..7 at N = 16, 1..3 at N = 8); semigroup chain
    identities exact; vacuum fixed exactly.  Positivity pattern exactly
    the site/bond dichotomy: even k PSD via the square identity
    T(2j) = A_j* A_j ((22,0,0)/(11,0,0)/(4,0,0)); odd k indefinite/
    degenerate with exactly zero one-particle diagonal ((10,12,7)/
    (5,6,5)/(2,2,3)/(1,0,1) at N = 16) -- the one-step transfer is NOT
    positive (staggering/chirality datum), its even powers are.
  * THE CLOCK: quarter turn = T^{N/4} positive self-adjoint on its
    domain -- N = 16: (11,0,0), min 6.6821e-5, one-particle blocks PD
    EXACTLY; N = 8: (4,0,0) and the compressed clock spectrum EXACTLY
    {1, sqrt(2)-1} = {1, 1/delta_S} in both parity sectors (SILVER
    ratio); compressed spectrum at N = 16: min 0.0194517, max 1.64144
    (vacuum eigenvalue exactly 1); spectral projections certified
    (residuals ~1e-40); reconstructed rotation group U(s) = exp(isH)
    unitary with group law (~1e-40).
  * v522 RESOLUTION: the clock-insertion census (745 match, 96 anti,
    0 violations) reproduced; EVERY anti-matching entry is a
    wrap-overlap entry and every overlap-free entry matches; the same
    insertion restricted to the quotient domain IS tau_4 entrywise.
    What dissolves in beta2: the ill-posedness of clock positivity
    (the clock now has a spectral calculus).  What remains time-like:
    the clock is a transfer step, not a symmetry of H_phys; its
    unitary avatar is the reconstructed rotation group.
  * KMS DEVIATION (pre-declared, confirmed with exactly the declared
    witnesses): NO contraction on the compact circle -- the local
    clock step expands the edge mode by exactly C(1)/C(3) = 1 +
    sqrt(2) = delta_S (N = 8), det(G - tau_4) < 0 on the odd
    one-particle block (N = 16, compressed lambda_max = 1.6414 > 1).
  * GSO/THETA: parity descends G-unitarily, H_even (+) H_odd exact;
    theta_cut and the deck candidate do NOT act on H_phys (support
    censuses); the PERPENDICULAR torsor mirror descends anti-unitarily
    (eta_perp in {+i, -i}), Theta_phys^2 = +1 on EVERY sector (the
    quotient is KRAMERS-FREE -- the (-1)^F class does not reach
    H_phys), time-reverses the semigroup, and theta_cut o theta_perp
    = alpha_{N/2} exactly (the torsor closes onto the deck).
  * CONTROLS: site cut indefinite ((3,3,1) / (2,2,4) with 2-3 negative
    directions -- kill branch fires for the site placement); family A
    indefinite (4,4,0); anti-chiral state (8,8,0) -- no quotient for
    the wrong chirality; wrong direction non-Hermitian off-domain
    (census (58,6,0), all mismatches wrap-overlap), mirrored domain
    Hermitian with mirror inertia.
  * KILL TESTS: (1), (2) strengthened, (3) shadow sharpened; none
    fires; (4)-(7) untouched; all seven stay live on A_hol.

TRANSPARENCY (tooling only; preregistration text unchanged): run 1
scored 18/20 -- the single substantive miss was a sympy simplify
failure on the exact product formula sin(7pi/16) - sin(5pi/16) =
2 cos(3pi/8) sin(pi/16) (true identity; simplify() does not close
pi/16 arguments), which cascaded into the verdict check.  Fixed by
certifying it as a Laurent-polynomial identity in z = e^{i pi/16}
(exact term-by-term cancellation, no trig simplification) plus a
40-digit numeric zero; an intermediate exp-rewrite attempt failed
because sympy auto-evaluates cos(3pi/8) to radicals.  No criterion,
tolerance or expectation was changed.

Construction base (READ-ONLY): verification/v519_woit_theta_rp_free.py
(kernel C(d), Pfaffian-Wick, dihedral machinery, theta_mono, Gram,
inertia certificates -- copied verbatim where possible),
verification/v522_woit_beta1_gso_gauge.py (tower maps, os_term,
Hermiticity census), experiments/tfpt-discovery/
woit_os_beta1_gauge_invariant_theta_probe.py.

Exact throughout (sympy trig-algebraic entries, Pfaffian-Wick, exact
signed-permutation towers); definiteness certificates are 40-digit
spectra of exact Hermitian matrices (mp.mp.dps = 40, threshold 1e-25).

Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/woit_os_beta2_os_quotient_probe.py
"""
import time
from itertools import combinations

import mpmath as mp
import sympy as sp

mp.mp.dps = 40

I = sp.I
N16 = 16
N8 = 8
ETA = I
RESULTS = []
FLAGS = {}
T0_WALL = time.perf_counter()


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
    return sp.simplify(e3) == 0


# ---------------------------------------------------------------------------
# chiral NS vacuum kernel + Pfaffian-Wick (v519/v522 verbatim, memoised)
# ---------------------------------------------------------------------------
def c_of(d, n):
    if d % 2 == 0:
        return sp.Integer(0)
    return sp.Rational(2, n) / sp.sin(sp.pi * sp.Rational(d, n))


def g2f(a, b, n, chi):
    if a == b:
        return sp.Integer(1)
    return I * chi * c_of(a - b, n)


_WICK = {}


def wick(idx, n, chi=1):
    idx = tuple(idx)
    if len(idx) == 0:
        return sp.Integer(1)
    if len(idx) % 2 == 1:
        return sp.Integer(0)
    key = (idx, n, chi)
    if key in _WICK:
        return _WICK[key]
    head, rest = idx[0], idx[1:]
    tot = sp.Integer(0)
    for j, b in enumerate(rest):
        sub = rest[:j] + rest[j + 1:]
        tot += (-1) ** j * g2f(head, b, n, chi) * wick(sub, n, chi)
    tot = sp.expand_complex(tot)
    _WICK[key] = tot
    return tot


# ---------------------------------------------------------------------------
# dihedral / tower machinery (v510/v519/v522 verbatim, tower generalised)
# ---------------------------------------------------------------------------
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
        b = (k + 1) // 2
        P = [(b + j) % n for j in range(n // 2)]
    rP = {(k - a) % n for a in P}
    assert not (rP & set(P))
    return P


PLUS = lambda a: 1


def tower_maps(n, shift, kmax):
    """(perm, sign) for alpha^k, k = 0..kmax; NS wrap sign -1 per crossing
    (v522 verbatim, generalised to arbitrary step count and shift sign)."""
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
    """apply the Bogoliubov automorphism (perm, sign) to a sorted monomial;
    returns (int coeff, sorted tuple).  (v522 verbatim)"""
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


def theta_mono(mono, r, s, eta):
    """theta(g_{i1}...g_{ik}) = eta^k s_{ik}..s_{i1} g_{r(ik)}..g_{r(i1)},
    sorted back; returns (sympy coeff, tuple).  (v519 verbatim)"""
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


def mono_mul(m1, m2):
    """exact Clifford product of sorted monomials (g_a^2 = 1); handles
    overlapping supports.  (v506/v519 verbatim)"""
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


def os_term(ea, eb, pm, r, s, eta, n, chi=1):
    """omega(theta(e_a) alpha^k(e_b)), exact.  (v522 verbatim)"""
    ca, ma = theta_mono(ea, r, s, eta)
    cb, mb = alpha_mono(eb, pm)
    cs, mm = mono_mul(ma, mb)
    return sp.expand_complex(ca * cb * cs * wick(mm, n, chi))


def os_lr(ea, eb, pmj, pmk, r, s, eta, n, chi=1):
    """omega(theta(alpha^j(e_a)) alpha^k(e_b)), exact (theta anti-linear;
    the alpha coefficients are +-1, so no conjugation subtlety)."""
    cj, mj = alpha_mono(ea, pmj)
    ct, mt = theta_mono(mj, r, s, eta)
    ck, mk = alpha_mono(eb, pmk)
    cs, mm = mono_mul(mt, mk)
    return sp.expand_complex(cj * ct * ck * cs * wick(mm, n, chi))


def term_matrix(basis, pm, r, s, eta, n, chi=1):
    d = len(basis)
    return sp.Matrix(d, d, lambda i, j: os_term(basis[i], basis[j], pm,
                                                r, s, eta, n, chi))


def hermitian_exact(M):
    d = M - M.conjugate().T
    return all(iszero(x) for x in d)


def spectrum_inertia(M, tol=None):
    """inertia (n+, n-, n0) of the exact Hermitian matrix via 40-digit
    spectrum; returns (inertia, min|nonzero|).  (v519 verbatim)"""
    if tol is None:
        tol = mp.mpf(10) ** (-25)
    n = M.shape[0]
    A = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            re_, im_ = M[i, j].evalf(45).as_real_imag()
            A[i, j] = mp.mpc(mp.mpf(str(re_)), mp.mpf(str(im_)))
    E, _ = mp.eighe(A)
    evs = [E[i].real for i in range(n)]
    npos = sum(1 for e in evs if e > tol)
    nneg = sum(1 for e in evs if e < -tol)
    nzero = n - npos - nneg
    nz = [abs(e) for e in evs if abs(e) > tol]
    return (npos, nneg, nzero), (min(nz) if nz else mp.mpf(0))


def to_mp(M):
    n, m = M.shape
    A = mp.matrix(n, m)
    for i in range(n):
        for j in range(m):
            re_, im_ = M[i, j].evalf(45).as_real_imag()
            A[i, j] = mp.mpc(mp.mpf(str(re_)), mp.mpf(str(im_)))
    return A


def ctr(A):
    """conjugate transpose of an mp.matrix."""
    B = mp.matrix(A.cols, A.rows)
    for i in range(A.rows):
        for j in range(A.cols):
            B[j, i] = mp.conj(A[i, j])
    return B


def eig_frame(Gm, Tm):
    """spectrum of the G-compressed operator G^{-1/2} T G^{-1/2} (exact
    inputs, 40-digit output); returns (sorted eigenvalues, B, QB)."""
    n = Gm.shape[0]
    G = to_mp(Gm)
    T = to_mp(Tm)
    EG, QG = mp.eighe(G)
    Gis = QG * mp.diag([1 / mp.sqrt(EG[i]) for i in range(n)]) * ctr(QG)
    B = Gis * T * Gis
    B = (B + ctr(B)) * mp.mpf('0.5')
    EB, QB = mp.eighe(B)
    return sorted([EB[i].real for i in range(n)]), B, QB


def dom_monos(basis, lo, hi):
    return [m for m in basis if all(lo <= a <= hi for a in m)]


# ---------------------------------------------------------------------------
# bases and pinned data
# ---------------------------------------------------------------------------
P16 = half_of(15, N16)                      # {8..15}
P8 = half_of(7, N8)                         # {4,5,6,7}
R15, S15 = refl_map(15, N16)
R7, S7 = refl_map(7, N8)

BASIS16 = [()] + [(a,) for a in P16] + list(combinations(P16, 2))   # 37
EVENS8 = [()] + list(combinations(P8, 2)) + [tuple(P8)]             # 8
ODDS8 = [(a,) for a in P8] + list(combinations(P8, 3))              # 8
BASIS8 = EVENS8 + ODDS8                                             # 16

TW16 = tower_maps(N16, 1, N16)
TW8 = tower_maps(N8, 1, N8)
TW16N = tower_maps(N16, -1, N16)
TW8N = tower_maps(N8, -1, N8)

C1_8, C3_8 = c_of(1, 8), c_of(3, 8)
C_16 = {d: c_of(d, 16) for d in range(1, 16, 2)}


def gram_of(basis, r, s, n, chi=1):
    tw0 = (tuple(range(n)), (1,) * n)
    return term_matrix(basis, tw0, r, s, ETA, n, chi)


def block_inertia(M, idx):
    return spectrum_inertia(M.extract(idx, idx))


# ---------------------------------------------------------------------------
# Part Q -- the OS quotient (H_phys, Omega) made explicit
# ---------------------------------------------------------------------------
def q1_preconditions():
    print("  -- Q1.1: one-step euclidean rotation -- exact preconditions")
    ok_full16 = (TW16[16][0] == tuple(range(N16))
                 and set(TW16[16][1]) == {-1})
    ok_full8 = (TW8[8][0] == tuple(range(N8)) and set(TW8[8][1]) == {-1})
    S1_16 = sp.Matrix(shift_matrix(N16, 1, -1))
    Cm16 = sp.Matrix(N16, N16, lambda a, b: c_of(a - b, N16))
    inv16 = sp.simplify(S1_16 * Cm16 * S1_16.T - Cm16) == sp.zeros(N16, N16)
    S1_8 = sp.Matrix(shift_matrix(N8, 1, -1))
    Cm8 = sp.Matrix(N8, N8, lambda a, b: c_of(a - b, N8))
    inv8 = sp.simplify(S1_8 * Cm8 * S1_8.T - Cm8) == sp.zeros(N8, N8)
    pure8 = sp.simplify(Cm8 * Cm8 + sp.eye(N8)) == sp.zeros(N8, N8)
    Rm = sp.Matrix(refl_matrix(N16, 15, -1))
    dihed = sp.simplify(Rm * S1_16 * Rm.inv()
                        - S1_16.inv()) == sp.zeros(N16, N16)
    # full state anti-invariance census at N = 8: omega(theta(m)) =
    # conj(omega(m)) for ALL 256 Cl(8) monomials (v519 R1.3 was 2-pt +
    # one 4-pt witness; here the complete census)
    anti_all = True
    for d in range(N8 + 1):
        for m in combinations(range(N8), d):
            ct_, mt_ = theta_mono(m, R7, S7, ETA)
            lhs = sp.expand_complex(ct_ * wick(mt_, N8))
            rhs = sp.expand_complex(sp.conjugate(wick(m, N8)))
            if not iszero(lhs - rhs):
                anti_all = False
                break
        if not anti_all:
            break
    FLAGS['q11'] = (ok_full16 and ok_full8 and inv16 and inv8 and pure8
                    and dihed and anti_all)
    check("Q1.1 PRECONDITIONS EXACT: the one-step NS rotation alpha_1 "
          "(2 pi/N) preserves the chiral vacuum (S1 C S1^T = C at N = 16: "
          "%s, N = 8: %s; C^2 = -1: %s), theta inverts it (R S1 R^-1 = "
          "S1^-1: %s), the FULL turn is fermion parity (alpha_1^N = "
          "(-1)^F as signed permutation, N = 16: %s, N = 8: %s -- lattice "
          "spin-statistics: the 2 pi seam rotation is the GSO element), "
          "and omega o theta = conj o omega on ALL 256 Cl(8) monomials "
          "(%s; full census, beyond the v519 witness)"
          % (inv16, inv8, pure8, dihed, ok_full16, ok_full8, anti_all),
          FLAGS['q11'])


def q2_gram16():
    print("  -- Q1.2: N = 16 deg <= 2 -- Gram, null space, H_phys")
    G16 = gram_of(BASIS16, R15, S15, N16)
    FLAGS['G16'] = G16
    ev_idx = [i for i, m in enumerate(BASIS16) if len(m) % 2 == 0]
    od_idx = [i for i, m in enumerate(BASIS16) if len(m) % 2 == 1]
    blocks0 = all(iszero(G16[i, j]) for i in ev_idx for j in od_idx)
    herm = hermitian_exact(G16)
    in_all, gap_all = spectrum_inertia(G16)
    in_odd, gap_odd = block_inertia(G16, od_idx)
    in_ev, gap_ev = block_inertia(G16, ev_idx)
    reg_odd = in_odd == (8, 0, 0) and mp.mpf('1.7e-3') < gap_odd \
        < mp.mpf('2.0e-3')
    reg_ev = in_ev == (29, 0, 0) and mp.mpf('1.5e-6') < gap_ev \
        < mp.mpf('2.1e-6')
    FLAGS['q12'] = (blocks0 and herm and in_all == (37, 0, 0)
                    and reg_odd and reg_ev)
    FLAGS['q_pd16'] = in_all == (37, 0, 0)
    check("Q1.2 H_phys EXPLICIT AT N = 16 (deg <= 2) [exact entries, "
          "40-digit inertia]: the 37x37 bond-cut OS Gram (1 + 8 + 28 "
          "monomials on the half {8..15}) is Hermitian exactly (%s), "
          "parity-block-diagonal exactly (%s), inertia %s = POSITIVE "
          "DEFINITE (min eigenvalue %s) -- NULL SPACE N = {0}: "
          "H_phys = A_+/N has dimension 37 = 29 (+) 8 at this level, "
          "with the v519/v522 sub-block regressions (one-particle %s "
          "min %s ~ 1.888e-3, even 29-basis %s min %s ~ 1.78e-6)"
          % (herm, blocks0, in_all, mp.nstr(gap_all, 5), in_odd,
             mp.nstr(gap_odd, 5), in_ev, mp.nstr(gap_ev, 5)),
          FLAGS['q12'])


def q3_gram8():
    print("  -- Q1.3: N = 8 complete half algebra -- Gram, null space")
    G8 = gram_of(BASIS8, R7, S7, N8)
    FLAGS['G8'] = G8
    blocks0 = all(iszero(G8[i, j]) for i in range(8) for j in range(8, 16))
    herm = hermitian_exact(G8)
    in_all, gap_all = spectrum_inertia(G8)
    # exact garnish: the one-particle block is checkerboard {4,6}(+){5,7};
    # 2x2 determinants exactly = (1/32)/(s1 s5 s3^2)-type via
    # sin^2(3pi/8) - sin(pi/8) sin(5pi/8) = 1/2 EXACTLY
    s1, s3, s5 = (sp.sin(sp.pi / 8), sp.sin(3 * sp.pi / 8),
                  sp.sin(5 * sp.pi / 8))
    half_id = iszero(s3 ** 2 - s1 * s5 - sp.Rational(1, 2))
    det_a = sp.simplify(c_of(1, 8) * c_of(5, 8) - c_of(3, 8) ** 2)
    det_ok = iszero(det_a * 32 * s1 * s5 * s3 ** 2 - 1)
    FLAGS['q13'] = (blocks0 and herm and in_all == (16, 0, 0) and half_id
                    and det_ok)
    FLAGS['q_pd8'] = in_all == (16, 0, 0)
    check("Q1.3 H_phys EXPLICIT AT N = 8 (COMPLETE half algebra) [exact "
          "entries, 40-digit inertia + exact 2x2 dets]: the 16x16 Gram "
          "(all 2^4 monomials on {4,5,6,7}) is Hermitian (%s), parity-"
          "block-diagonal (%s), inertia %s = PD (min eigenvalue %s) -- "
          "NULL SPACE N = {0} with NO degree truncation: dim H_phys = "
          "16 = 8 (+) 8 = 4^2 (the DOUBLED/two-sided dimension: compact "
          "euclidean time reconstructs a THERMAL representation, the "
          "KMS typing of [C-3](d)); exact certificates: sin^2(3pi/8) - "
          "sin(pi/8) sin(5pi/8) = 1/2 (%s) makes the one-particle "
          "checkerboard dets exactly positive (%s)"
          % (herm, blocks0, in_all, mp.nstr(gap_all, 5), half_id, det_ok),
          FLAGS['q13'])


def q4_kill_branch():
    print("  -- Q1.4: contract kill branch")
    fired = not (FLAGS['q_pd16'] and FLAGS['q_pd8'])
    FLAGS['q14'] = not fired
    check("Q1.4 CONTRACT KILL BRANCH ('the quotient degenerates: zero or "
          "indefinite completion') does NOT fire [assembled]: both "
          "completions are positive definite with rank 37 resp. 16 >> 1 "
          "(Q1.2/Q1.3) -- no negative direction, no collapse to the "
          "vacuum line: the OS quotient of the free system EXISTS and "
          "is explicit (basis + Gram + dimension)", not fired)


# ---------------------------------------------------------------------------
# Part T -- the reconstructed transfer operator (Klein-Landau local
# symmetric semigroup) and the clock
# ---------------------------------------------------------------------------
def t1_domain_hermiticity():
    print("  -- T2.1: local-domain Hermiticity of the transfer forms")
    # disjoint-support anti-multiplicativity lemma + overlap failure seed
    lem_ok = True
    for dx in range(3):
        for x in combinations(range(4), dx):        # negative half N=8
            for dy in range(3):
                for y in combinations(P8, dy):      # positive half
                    cs, mm = mono_mul(x, y)
                    ct1, mt1 = theta_mono(mm, R7, S7, ETA)
                    lhs = (sp.expand_complex(cs * ct1), mt1)
                    cy, my = theta_mono(y, R7, S7, ETA)
                    cx, mx = theta_mono(x, R7, S7, ETA)
                    cr, mr = mono_mul(my, mx)
                    rhs = (sp.expand_complex(cy * cx * cr), mr)
                    if lhs[1] != rhs[1] or not iszero(lhs[0] - rhs[0]):
                        lem_ok = False
    seed = not iszero(ETA ** 2 - 1)   # theta(g a g a)=1 vs theta(ga)^2=-1
    taus16, herm16 = {}, {}
    for k in range(1, 8):
        D = dom_monos(BASIS16, 8, 15 - k)
        M = term_matrix(D, TW16[k], R15, S15, ETA, N16)
        taus16[k] = (D, M)
        herm16[k] = hermitian_exact(M)
    taus8, herm8 = {}, {}
    for k in range(1, 4):
        D = dom_monos(BASIS8, 4, 7 - k)
        M = term_matrix(D, TW8[k], R7, S7, ETA, N8)
        taus8[k] = (D, M)
        herm8[k] = hermitian_exact(M)
    FLAGS['taus16'], FLAGS['taus8'] = taus16, taus8
    dims16 = {k: len(taus16[k][0]) for k in taus16}
    FLAGS['t21'] = (lem_ok and seed and all(herm16.values())
                    and all(herm8.values())
                    and dims16 == {1: 29, 2: 22, 3: 16, 4: 11, 5: 7,
                                   6: 4, 7: 2})
    check("T2.1 SELF-ADJOINTNESS VIA THETA ON THE KLEIN-LANDAU DOMAINS "
          "[exact]: theta is anti-multiplicative on DISJOINT supports "
          "(full census across the N = 8 cut, deg <= 2 x deg <= 2: %s) "
          "but NOT on overlapping ones (seed eta^2 = -1: theta(g_a g_a) "
          "= 1 vs theta(g_a)theta(g_a) = -1: %s -- the exact v522 "
          "mechanism); on the shrinking domains D_k (dims %s at N = 16) "
          "every insertion tau_k = omega(theta(a) alpha_k(b)) is "
          "Hermitian EXACTLY, k = 1..7 at N = 16 (%s) and k = 1..3 at "
          "N = 8 (%s): the local transfer T(k)[b] = [alpha_k b] is "
          "G-symmetric on its domain -- the OS-quotient cure of the "
          "v522 Hermiticity failure"
          % (lem_ok, seed, dims16, {k: herm16[k] for k in sorted(herm16)},
             {k: herm8[k] for k in sorted(herm8)}),
          FLAGS['t21'])


def t2_semigroup():
    print("  -- T2.2: semigroup structure + vacuum fixed")
    ok_sg8 = True
    for (j, k) in [(1, 1), (1, 2), (2, 1), (2, 2)]:
        for ea in BASIS8:
            for eb in BASIS8:
                lhs = os_lr(ea, eb, TW8[j], TW8[k], R7, S7, ETA, N8)
                rhs = os_term(ea, eb, TW8[j + k], R7, S7, ETA, N8)
                if not iszero(lhs - rhs):
                    ok_sg8 = False
                    break
            if not ok_sg8:
                break
        if not ok_sg8:
            break
    sub16 = dom_monos(BASIS16, 8, 11)
    ok_sg16 = True
    for (j, k) in [(1, 1), (2, 2), (1, 3)]:
        for ea in sub16:
            for eb in sub16:
                lhs = os_lr(ea, eb, TW16[j], TW16[k], R15, S15, ETA, N16)
                rhs = os_term(ea, eb, TW16[j + k], R15, S15, ETA, N16)
                if not iszero(lhs - rhs):
                    ok_sg16 = False
                    break
            if not ok_sg16:
                break
        if not ok_sg16:
            break
    vac_ok = True
    G16, G8 = FLAGS['G16'], FLAGS['G8']
    for k in range(1, 8):
        D, M = FLAGS['taus16'][k]
        i1 = D.index(())
        for j, m in enumerate(D):
            gi = BASIS16.index(m)
            if not iszero(M[i1, j] - G16[0, gi]):
                vac_ok = False
    for k in range(1, 4):
        D, M = FLAGS['taus8'][k]
        i1 = D.index(())
        for j, m in enumerate(D):
            gi = BASIS8.index(m)
            if not iszero(M[i1, j] - G8[0, gi]):
                vac_ok = False
    FLAGS['t22'] = ok_sg8 and ok_sg16 and vac_ok
    check("T2.2 TRANSLATION SEMIGROUP T^k [exact]: the chain identity "
          "<[alpha_j a], [alpha_k b]> = tau_{j+k}(a, b) holds EXACTLY -- "
          "N = 8: all 16x16 monomial pairs for (j,k) = (1,1), (1,2), "
          "(2,1), (2,2) (%s); N = 16: the 11-element sub-half {8..11} "
          "for (j,k) = (1,1), (2,2), (1,3) (%s) -- Klein-Landau local "
          "semigroup structure T(j)T(k) = T(j+k) on nested domains; the "
          "vacuum is FIXED exactly: tau_k(1, b) = <Omega, [b]> for every "
          "k and b (%s; omega o alpha = omega), so T(k)Omega = Omega"
          % (ok_sg8, ok_sg16, vac_ok), FLAGS['t22'])


def t3_positivity_pattern():
    print("  -- T2.3: positivity pattern of the local semigroup")
    inert16 = {}
    for k in range(1, 8):
        D, M = FLAGS['taus16'][k]
        inert16[k], _ = spectrum_inertia(M)
    inert8 = {}
    for k in range(1, 4):
        D, M = FLAGS['taus8'][k]
        inert8[k], _ = spectrum_inertia(M)
    # exact mechanism: odd k -> one-particle diagonal identically zero
    diag0 = True
    for k in (1, 3, 5):
        D, M = FLAGS['taus16'][k]
        for i, m in enumerate(D):
            if len(m) == 1 and not iszero(M[i, i]):
                diag0 = False
    D1_8, M1_8 = FLAGS['taus8'][1]
    for i, m in enumerate(D1_8):
        if len(m) == 1 and not iszero(M1_8[i, i]):
            diag0 = False
    # exact A*A identity for even k: tau_k = Gram(alpha_{k/2}., alpha_{k/2}.)
    G16 = FLAGS['G16']
    bidx16 = {m: i for i, m in enumerate(BASIS16)}
    aa_ok = True
    for k in (2, 4, 6):
        D, M = FLAGS['taus16'][k]
        for i, ma in enumerate(D):
            ca, ia = alpha_mono(ma, TW16[k // 2])
            for j, mb in enumerate(D):
                cb, ib = alpha_mono(mb, TW16[k // 2])
                if not iszero(M[i, j] - ca * cb * G16[bidx16[ia],
                                                      bidx16[ib]]):
                    aa_ok = False
    odd_indef = all(inert16[k][1] > 0 for k in (1, 3, 5)) \
        and inert16[7] == (1, 0, 1) and inert8[1][1] > 0 \
        and inert8[3] == (1, 0, 1)
    even_psd = all(inert16[k][1] == 0 for k in (2, 4, 6)) \
        and inert8[2][1] == 0
    FLAGS['inert16'], FLAGS['inert8'] = inert16, inert8
    FLAGS['t23'] = diag0 and aa_ok and odd_indef and even_psd
    check("T2.3 THE SITE/BOND DICHOTOMY BECOMES THE SEMIGROUP POSITIVITY "
          "PATTERN [exact mechanism + 40-digit inertia]: EVEN steps obey "
          "the exact square identity tau_2j(a,b) = <[alpha_j a], "
          "[alpha_j b]> (T(2j) = A_j* A_j: %s) and are PSD (N = 16 "
          "inertias k = 2, 4, 6: %s, %s, %s; N = 8 k = 2: %s); ODD steps "
          "land on SITE axes (axis 15 - k even): the chiral checkerboard "
          "C(even) = 0 kills the one-particle diagonal EXACTLY (%s) and "
          "they are indefinite or degenerate (N = 16 k = 1, 3, 5, 7: "
          "%s, %s, %s, %s; N = 8 k = 1, 3: %s, %s) -- the one-step "
          "transfer is NOT positive (the free chirality/staggering "
          "datum, kill-test-3 shadow), its even powers ARE: exactly the "
          "v519 bond-vs-site RP dichotomy resurfacing INSIDE the "
          "reconstructed semigroup"
          % (aa_ok, inert16[2], inert16[4], inert16[6], inert8[2],
             diag0, inert16[1], inert16[3], inert16[5], inert16[7],
             inert8[1], inert8[3]),
          FLAGS['t23'])


def t4_clock():
    print("  -- T2.4: the mu4 clock as positive transfer step T^{N/4}")
    D4, M4 = FLAGS['taus16'][4]
    herm4 = hermitian_exact(M4)
    in4, gap4 = spectrum_inertia(M4)
    # exact one-particle PD certificates (2x2 trace/det with C9=C7, C11=C5)
    c5, c7, c9, c11 = C_16[5], C_16[7], C_16[9], C_16[11]
    ids = iszero(c9 - c7) and iszero(c11 - c5)
    det_blk = sp.simplify(c5 * c9 - c7 ** 2)
    fact_ok = iszero(det_blk - c7 * (c5 - c7))
    s5, s7 = sp.sin(5 * sp.pi / 16), sp.sin(7 * sp.pi / 16)
    prod_expr = s7 - s5 - 2 * sp.cos(3 * sp.pi / 8) * sp.sin(sp.pi / 16)
    # exact certificate as a Laurent identity in z = e^{i pi/16}:
    # 2i [sin(7pi/16) - sin(5pi/16) - 2 cos(6pi/16) sin(pi/16)]
    #   = (z^7 - z^-7) - (z^5 - z^-5) - (z^6 + z^-6)(z - z^-1) = 0
    z = sp.symbols('z')
    laurent = sp.expand((z ** 7 - z ** -7) - (z ** 5 - z ** -5)
                        - (z ** 6 + z ** -6) * (z - 1 / z)) == 0
    re_p, im_p = prod_expr.evalf(40).as_real_imag()
    num0 = (abs(mp.mpf(str(re_p))) < mp.mpf(10) ** (-35)
            and abs(mp.mpf(str(im_p))) < mp.mpf(10) ** (-35))
    prodform = laurent and num0
    pos_factors = (sp.cos(3 * sp.pi / 8).is_positive
                   and sp.sin(sp.pi / 16).is_positive
                   and sp.sin(5 * sp.pi / 16).is_positive
                   and sp.sin(7 * sp.pi / 16).is_positive)
    D2_8, M2_8 = FLAGS['taus8'][2]
    herm2_8 = hermitian_exact(M2_8)
    in2_8, gap2_8 = spectrum_inertia(M2_8)
    # exact N = 8 anchor: compressed clock spectrum {1, sqrt(2)-1} exactly
    idx_o = [i for i, m in enumerate(D2_8) if len(m) == 1]
    idx_e = [i for i, m in enumerate(D2_8) if len(m) % 2 == 0]
    G8 = FLAGS['G8']
    bidx8 = {m: i for i, m in enumerate(BASIS8)}
    Go = sp.Matrix(2, 2, lambda i, j: G8[bidx8[D2_8[idx_o[i]]],
                                         bidx8[D2_8[idx_o[j]]]])
    To = M2_8.extract(idx_o, idx_o)
    lam = sp.symbols('lam')
    roots_o = sp.solve(sp.det(To - lam * Go), lam)
    Ge = sp.Matrix(2, 2, lambda i, j: G8[bidx8[D2_8[idx_e[i]]],
                                         bidx8[D2_8[idx_e[j]]]])
    Te = M2_8.extract(idx_e, idx_e)
    roots_e = sp.solve(sp.det(Te - lam * Ge), lam)
    silver = sp.sqrt(2) - 1
    ok_o = (len(roots_o) == 2
            and any(iszero(rt - 1) for rt in roots_o)
            and any(iszero(rt - silver) for rt in roots_o))
    ok_e = (len(roots_e) == 2
            and any(iszero(rt - 1) for rt in roots_e)
            and any(iszero(rt - silver) for rt in roots_e))
    silver_id = iszero(sp.sin(sp.pi / 8) / sp.sin(3 * sp.pi / 8) - silver)
    FLAGS['t24'] = (herm4 and in4 == (11, 0, 0) and ids and fact_ok
                    and prodform and bool(pos_factors) and herm2_8
                    and in2_8 == (4, 0, 0) and ok_o and ok_e and silver_id)
    FLAGS['clock_herm_pd'] = herm4 and in4[1] == 0 and herm2_8 \
        and in2_8[1] == 0
    check("T2.4 THE CLOCK IS IMPLEMENTED ON H_phys AS A POSITIVE "
          "SELF-ADJOINT TRANSFER STEP [exact + 40-digit]: the quarter "
          "turn alpha_{N/4} is an EVEN step -- at N = 16 tau_4 on the "
          "11-dim domain {8..11} is Hermitian (%s) and PD, inertia %s "
          "(min eigenvalue %s), with the one-particle blocks EXACTLY PD "
          "(C(9) = C(7), C(11) = C(5): %s; det = C7 (C5 - C7): %s; "
          "sin(7pi/16) - sin(5pi/16) = 2 cos(3pi/8) sin(pi/16) > 0: "
          "%s/%s); at N = 8 tau_2 on {4,5} is Hermitian (%s), PD %s "
          "(min %s), and the COMPRESSED clock spectrum is EXACTLY "
          "{1, sqrt(2) - 1} = {1, 1/delta_silver} in BOTH parity "
          "sectors (odd: %s, even: %s; sin(pi/8)/sin(3pi/8) = sqrt(2) "
          "- 1: %s) -- the SILVER-midpoint axes of the v519 mu4 torsor "
          "return as the exact clock-transfer eigenvalue"
          % (herm4, in4, mp.nstr(gap4, 5), ids, fact_ok, prodform,
             bool(pos_factors), herm2_8, in2_8, mp.nstr(gap2_8, 5),
             ok_o, ok_e, silver_id),
          FLAGS['t24'])


def t5_spectral_rotation():
    print("  -- T2.5: spectral projections + reconstructed rotation group")
    D4, M4 = FLAGS['taus16'][4]
    bidx16 = {m: i for i, m in enumerate(BASIS16)}
    idx = [bidx16[m] for m in D4]
    G4 = FLAGS['G16'].extract(idx, idx)
    spec, B, QB = eig_frame(G4, M4)
    n = len(spec)
    tol = mp.mpf(10) ** (-30)
    all_pos = all(e > mp.mpf(10) ** (-25) for e in spec)
    EB, QB2 = mp.eighe(B)
    res_eig = mp.mnorm(B - QB2 * mp.diag([EB[i] for i in range(n)])
                       * ctr(QB2), 1)
    res_orth = mp.mnorm(ctr(QB2) * QB2 - mp.eye(n), 1)
    lamH = [-mp.log(EB[i].real) for i in range(n)]

    def U(sv):
        return QB2 * mp.diag([mp.exp(1j * sv * h) for h in lamH]) \
            * ctr(QB2)

    Ua, Ub, Uc = U(mp.mpf('0.3')), U(mp.mpf('0.4')), U(mp.mpf('0.7'))
    res_uni = mp.mnorm(ctr(Ua) * Ua - mp.eye(n), 1)
    res_grp = mp.mnorm(Ua * Ub - Uc, 1)
    specs = sorted([float(e) for e in spec])
    D2_8, M2_8 = FLAGS['taus8'][2]
    bidx8 = {m: i for i, m in enumerate(BASIS8)}
    idx8 = [bidx8[m] for m in D2_8]
    G28 = FLAGS['G8'].extract(idx8, idx8)
    spec8, _, _ = eig_frame(G28, M2_8)
    FLAGS['spec_clock16'] = spec
    FLAGS['spec_clock8'] = spec8
    ok = (all_pos and res_eig < tol and res_orth < tol and res_uni < tol
          and res_grp < tol)
    FLAGS['t25'] = ok
    check("T2.5 SPECTRAL PROJECTIONS + RECONSTRUCTED ROTATION GROUP "
          "[40-digit certificates]: the compressed clock G^{-1/2} tau_4 "
          "G^{-1/2} at N = 16 (11-dim) is strictly positive (%s; "
          "spectrum min %.6g, max %.6g, vacuum eigenvalue 1), its "
          "eigendecomposition is certified (residual %s, orthonormality "
          "%s < 1e-30) -- SPECTRAL PROJECTIONS ARE WELL-DEFINED on "
          "H_phys, exactly the calculus that the non-Hermitian "
          "pre-quotient clock average of v522 could not have; the "
          "reconstructed rotation one-parameter group U(s) = exp(is H), "
          "H = -log(compressed clock), is unitary with the group law "
          "(residuals %s, %s < 1e-30) -- per contract precision (iii) "
          "this is the [C]-operationalisation of 'the clock acting "
          "unitarily' (N = 8 compressed clock spectrum: %s)"
          % (all_pos, specs[0], specs[-1], mp.nstr(res_eig, 3),
             mp.nstr(res_orth, 3), mp.nstr(res_uni, 3),
             mp.nstr(res_grp, 3),
             [mp.nstr(e, 8) for e in FLAGS['spec_clock8']]),
          FLAGS['t25'])


def t6_kms():
    print("  -- T2.6: contraction fails with the pre-declared KMS "
          "witnesses")
    # N = 8 exact: ||T(2)[g_5]||^2 / ||[g_5]||^2 = C(1)/C(3) = 1 + sqrt(2)
    G8 = FLAGS['G8']
    bidx8 = {m: i for i, m in enumerate(BASIS8)}
    n57 = G8[bidx8[(7,)], bidx8[(7,)]] / G8[bidx8[(5,)], bidx8[(5,)]]
    silver_exp = iszero(sp.simplify(n57) - (1 + sp.sqrt(2)))
    drift = iszero(sp.simplify(C1_8 / C3_8) - (1 + sp.sqrt(2)))
    # N = 16 exact: det(G - tau_4) < 0 on the odd one-particle clock block
    c3, c5, c7 = C_16[3], C_16[5], C_16[7]
    Gb = sp.Matrix([[c3, c5], [c5, c7]])
    Tb = sp.Matrix([[c7, c7], [c7, c5]])
    det_gt = sp.simplify(sp.det(Gb - Tb))
    fact = iszero(det_gt + (c5 - c7) * ((c3 - c7) + (c5 - c7)))
    re_, im_ = det_gt.evalf(40).as_real_imag()
    sign40 = (mp.mpf(str(re_)) < 0
              and abs(mp.mpf(str(im_))) < mp.mpf(10) ** (-30))
    spec16 = FLAGS['spec_clock16']
    lam_max16 = max(spec16)
    exceeds = lam_max16 > 1 + mp.mpf(10) ** (-25)
    spec8 = FLAGS['spec_clock8']
    lam_max8 = max(spec8)
    at_one8 = abs(lam_max8 - 1) < mp.mpf(10) ** (-30)
    FLAGS['t26'] = (silver_exp and drift and fact and sign40 and exceeds
                    and at_one8)
    FLAGS['kms_witnessed'] = FLAGS['t26']
    check("T2.6 NO CONTRACTION ON THE COMPACT CIRCLE -- THE PRE-DECLARED "
          "KMS DEVIATION [exact witnesses + 40-digit]: the local clock "
          "step EXPANDS the edge mode by exactly the silver ratio: "
          "||T(2)[g_5]||^2/||[g_5]||^2 = C(1)/C(3) = 1 + sqrt(2) = "
          "delta_S at N = 8 (%s/%s -- while the COMPRESSED spectrum is "
          "{1, 1/delta_S}); at N = 16 the odd one-particle clock block "
          "has det(G - tau_4) = -(C5-C7)((C3-C7)+(C5-C7)) < 0 EXACTLY "
          "(%s, 40-digit sign %s), so the compressed clock exceeds 1: "
          "lambda_max = %s > 1 (vs %s = 1 exactly at N = 8) -- the "
          "finite seam circle is compact euclidean TIME: the "
          "reconstruction is thermal (dim H_phys = 4^2), T(k) is a "
          "positive self-adjoint LOCAL semigroup but NOT a contraction "
          "(contraction = the ground-state/infinite-volume property); "
          "0 < T <= 1 fails exactly as pre-registered in [C-3](d), "
          "with exactly these witnesses -- typed KMS finding, not a "
          "beta2 failure"
          % (silver_exp, drift, fact, sign40, mp.nstr(lam_max16, 8),
             mp.nstr(lam_max8, 8)),
          FLAGS['t26'])


def t7_v522_resolution():
    print("  -- T2.7: the v522 non-Hermiticity localised and resolved")
    tw4 = tower_maps(N16, 4, 8)
    same_map = tw4[1] == TW16[4]
    basis29 = [()] + list(combinations(P16, 2))
    T1v = term_matrix(basis29, tw4[1], R15, S15, ETA, N16)
    d = len(basis29)
    n_match = n_anti = n_viol = 0
    impl_ok = True
    for i in range(d):
        ci, mi = theta_mono(basis29[i], R15, S15, ETA)
        for j in range(d):
            cj, mj = alpha_mono(basis29[j], tw4[1])
            dij = T1v[i, j] - sp.conjugate(T1v[j, i])
            if iszero(dij):
                n_match += 1
                matched = True
            elif iszero(T1v[i, j] + sp.conjugate(T1v[j, i])):
                n_anti += 1
                matched = False
            else:
                n_viol += 1
                matched = False
            # overlap census: does either product wrap into the other half?
            cjt, mjt = theta_mono(basis29[j], R15, S15, ETA)
            cit, mit = alpha_mono(basis29[i], tw4[1])
            ov = (set(mi) & set(mj)) or (set(mjt) & set(mit))
            if not ov and not matched:
                impl_ok = False
    reg = (n_match, n_anti, n_viol) == (745, 96, 0)
    # restriction to the quotient domain D_4: the SAME insertion is the
    # positive transfer step tau_4 (entrywise identity)
    D4, M4 = FLAGS['taus16'][4]
    sub = [i for i, m in enumerate(basis29)
           if all(8 <= a <= 11 for a in m)]
    restr_ok = True
    for ii, i in enumerate(sub):
        for jj, j in enumerate(sub):
            i4 = D4.index(basis29[i])
            j4 = D4.index(basis29[j])
            if not iszero(T1v[i, j] - M4[i4, j4]):
                restr_ok = False
    FLAGS['t27'] = same_map and reg and impl_ok and restr_ok
    check("T2.7 WHICH PART OF THE v522 'TIME-LIKENESS' DISSOLVES IN THE "
          "QUOTIENT [exact]: the v522 clock insertion (shift-4 tower, "
          "full even 29-basis) is reproduced with census (match, anti, "
          "viol) = (%d, %d, %d) = the v522 numbers (%s; alpha_S = "
          "alpha_1^4 as signed permutations: %s); EVERY "
          "Hermiticity-anti-matching entry has a WRAP OVERLAP (the "
          "shifted support crosses into the reflected half) and every "
          "overlap-free entry matches (%s) -- the pre-quotient "
          "non-Hermiticity is EXACTLY the domain/wrap artifact; "
          "restricted to the Klein-Landau domain {8..11} the SAME "
          "insertion IS the positive transfer step tau_4 entrywise "
          "(%s): what dissolves in beta2 is the ILL-POSEDNESS of clock "
          "positivity -- the clock becomes a positive self-adjoint "
          "operator with spectral calculus (T2.4/T2.5); what REMAINS "
          "time-like is the euclidean-rotation character itself (the "
          "clock is a transfer step, not a symmetry of H_phys -- its "
          "unitary avatar is the RECONSTRUCTED group of T2.5)"
          % (n_match, n_anti, n_viol, reg, same_map, impl_ok, restr_ok),
          FLAGS['t27'])


# ---------------------------------------------------------------------------
# Part G -- GSO grading and the descended anti-unitary on H_phys
# ---------------------------------------------------------------------------
def g1_gso():
    print("  -- G3.1: the GSO grading survives on H_phys")
    par16 = (tuple(range(N16)), (-1,) * N16)
    par8 = (tuple(range(N8)), (-1,) * N8)
    comm_ok = True
    for n, tw, par, kmax in ((N16, TW16, par16, 8), (N8, TW8, par8, 4)):
        for k in range(1, kmax):
            for a in range(n):
                c1 = par[1][tw[k][0][a]] * tw[k][1][a]     # P o alpha
                c2 = tw[k][1][a] * par[1][a]               # alpha o P
                if c1 != c2:
                    comm_ok = False
    dims16 = (sum(1 for m in BASIS16 if len(m) % 2 == 0),
              sum(1 for m in BASIS16 if len(m) % 2 == 1))
    dims8 = (len(EVENS8), len(ODDS8))
    FLAGS['g31'] = comm_ok and dims16 == (29, 8) and dims8 == (8, 8)
    check("G3.1 GSO GRADING SURVIVES [exact]: fermion parity descends to "
          "the G-unitary P[m] = (-1)^{|m|}[m] (the Gram is parity-block-"
          "diagonal EXACTLY, Q1.2/Q1.3: %s/%s), P^2 = 1, and P commutes "
          "with every translation alpha_k as signed permutation maps "
          "(%s) hence with all transfer data -- H_phys = H_even (+) "
          "H_odd orthogonally, dims %s at N = 16 (deg <= 2) and %s at "
          "N = 8; the mu4 gauge datum of v522 (the GSO Z2) acts on the "
          "quotient exactly"
          % (FLAGS['q12'], FLAGS['q13'], comm_ok, dims16, dims8),
          FLAGS['g31'])


def theta_perp_data(n):
    if n == N16:
        kp = 7
        return refl_map(kp, N16)
    kp = 3
    return refl_map(kp, N8)


def g2_theta_perp():
    print("  -- G3.2: the perpendicular torsor mirror descends "
          "anti-unitarily")
    rp16, sp16_ = theta_perp_data(N16)
    rp8, sp8_ = theta_perp_data(N8)
    G16, G8 = FLAGS['G16'], FLAGS['G8']
    bidx16 = {m: i for i, m in enumerate(BASIS16)}
    bidx8 = {m: i for i, m in enumerate(BASIS8)}
    good_eta = []
    for etap in (sp.Integer(1), sp.Integer(-1), I, -I):
        ok = True
        for basis, bidx, G, rp, sp_ in ((BASIS16, bidx16, G16, rp16, sp16_),
                                        (BASIS8, bidx8, G8, rp8, sp8_)):
            for i, ma in enumerate(basis):
                ca, ia = theta_mono(ma, rp, sp_, etap)
                if ia not in bidx:
                    ok = False
                    break
                for j, mb in enumerate(basis):
                    cb, ib = theta_mono(mb, rp, sp_, etap)
                    lhs = sp.conjugate(ca) * cb * G[bidx[ia], bidx[ib]]
                    if not iszero(lhs - G[j, i]):
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            good_eta.append(etap)
    FLAGS['eta_perp'] = good_eta
    etap = good_eta[0] if good_eta else I
    sq_plus = True
    for basis, rp, sp_ in ((BASIS16, rp16, sp16_), (BASIS8, rp8, sp8_)):
        for m in basis:
            c1, m1 = theta_mono(m, rp, sp_, etap)
            c2, m2 = theta_mono(m1, rp, sp_, etap)
            if m2 != m or not iszero(sp.conjugate(c1) * c2 - 1):
                sq_plus = False
    trev = True
    for n, tw, twn, rp, sp_, basis in ((N16, TW16, TW16N, rp16, sp16_,
                                        BASIS16),
                                       (N8, TW8, TW8N, rp8, sp8_, BASIS8)):
        for k in (1, 2):
            for m in basis:
                cb, mb = alpha_mono(m, tw[k])
                ct1, mt1 = theta_mono(mb, rp, sp_, etap)
                ct2, mt2 = theta_mono(m, rp, sp_, etap)
                cb2, mb2 = alpha_mono(mt2, twn[k])
                if mt1 != mb2 or not iszero(cb * ct1 - ct2 * cb2):
                    trev = False
    deck_eta = None
    for etad in good_eta:
        ok_d = True
        for n, tw, rc, sc, rp, sp_, basis in ((N16, TW16, R15, S15, rp16,
                                               sp16_, BASIS16),
                                              (N8, TW8, R7, S7, rp8, sp8_,
                                               BASIS8)):
            for m in basis:
                cp, mp_ = theta_mono(m, rp, sp_, etad)
                cc, mc = theta_mono(mp_, rc, sc, ETA)
                ca, ma = alpha_mono(m, tw[n // 2])
                if mc != ma or not iszero(sp.conjugate(cp) * cc - ca):
                    ok_d = False
                    break
            if not ok_d:
                break
        if ok_d:
            deck_eta = etad
            break
    deck_ok = deck_eta is not None
    FLAGS['g32'] = (set(map(str, good_eta)) == {'I', '-I'} and sq_plus
                    and trev and deck_ok)
    check("G3.2 THETA DESCENDS TO H_phys AS THE PERPENDICULAR TORSOR "
          "MIRROR [exact]: Theta_phys[a] := [theta_perp(a)] (axis "
          "k_cut - N/2 = 7 resp. 3, the OTHER clock orbit of the v519 "
          "mu4 torsor) is ANTI-UNITARY, <Theta a, Theta b> = <b, a> "
          "entrywise on all 37^2 + 16^2 pairs, exactly for the twist "
          "sub-torsor eta_perp in %s (mu4-pinned, like the cut twist); "
          "Theta_phys^2 = +1 on EVERY basis class incl. the ODD sector "
          "(%s) -- the quotient is KRAMERS-FREE: the (-1)^F dichotomy "
          "does not reach H_phys; Theta_phys time-reverses the local "
          "semigroup (theta_perp alpha_k = alpha_{-k} theta_perp: %s) "
          "and the torsor closes onto the deck: theta_cut o theta_perp "
          "= alpha_{N/2} EXACTLY including coefficients (%s) -- the "
          "product of the two pinned mirrors IS the antipode lift"
          % ([str(e) for e in good_eta], sq_plus, trev, deck_ok),
          FLAGS['g32'])


def g3_non_descent():
    print("  -- G3.3: what does NOT act on H_phys (typed)")
    cut_out = True
    for m in BASIS16[1:]:
        c_, mi = theta_mono(m, R15, S15, ETA)
        if set(mi) & set(P16):
            cut_out = False
    for m in BASIS8[1:]:
        if m == ():
            continue
        c_, mi = theta_mono(m, R7, S7, ETA)
        if set(mi) & set(P8):
            cut_out = False
    deck_out = True
    for m in BASIS16[1:]:
        c_, mi = alpha_mono(m, TW16[8])
        if set(mi) & set(P16):
            deck_out = False
    for m in BASIS8[1:]:
        if m == ():
            continue
        c_, mi = alpha_mono(m, TW8[4])
        if set(mi) & set(P8):
            deck_out = False
    FLAGS['g33'] = cut_out and deck_out
    check("G3.3 NON-DESCENT CENSUSES [exact]: the OS reflection "
          "theta_cut maps every non-scalar element of A_+ ENTIRELY into "
          "the opposite half (%s) -- it does not act on H_phys, it IS "
          "the metric; the deck/antipode candidate Theta_t = Utilde o K "
          "(Kramers class (-1)^F, v519 W-S6.4) likewise maps A_+ off "
          "itself (%s) -- the Kramers class CANNOT obstruct the "
          "quotient, and indeed the descended real structure has "
          "Theta_phys^2 = +1 (G3.2): the v510/v519 dichotomy resolves "
          "on H_phys in favour of +1, extending v522 G3.1 (invisible "
          "on A^G) to the FULL quotient including the odd sector"
          % (cut_out, deck_out), FLAGS['g33'])


# ---------------------------------------------------------------------------
# Part C -- negative controls
# ---------------------------------------------------------------------------
def c1_site_cut():
    print("  -- C4.1: site cut -- the kill branch fires for the site "
          "placement")
    k = 0
    P = half_of(k, N16)
    r_ = lambda a: (k - a) % N16
    basis1 = [(a,) for a in P]
    tw0 = (tuple(range(N16)), (1,) * N16)
    M1 = term_matrix(basis1, tw0, r_, PLUS, -I, N16)
    herm1 = hermitian_exact(M1)
    in1, _ = spectrum_inertia(M1)
    P8s = half_of(0, N8)                    # {1,2,3}
    basis8s = [m for d in range(4) for m in combinations(P8s, d)]
    tw08 = (tuple(range(N8)), (1,) * N8)
    r8_ = lambda a: (-a) % N8
    picked = None
    for etac in (sp.Integer(1), sp.Integer(-1), I, -I):
        M8s = term_matrix(basis8s, tw08, r8_, PLUS, etac, N8)
        if hermitian_exact(M8s):
            in8s, _ = spectrum_inertia(M8s)
            picked = (etac, in8s)
            break
    FLAGS['c41'] = (herm1 and in1 == (3, 3, 1) and picked is not None
                    and picked[1][1] > 0)
    check("C4.1 SITE CUT -> INDEFINITE COMPLETION [exact + 40-digit]: "
          "the marks-at-sites reading fails the beta2 kill branch "
          "exactly -- N = 16 one-particle Gram Hermitian %s with "
          "inertia %s (v519 R2.1 regression, 3 NEGATIVE directions + "
          "kernel); N = 8 complete site-half algebra {1,2,3} (8 "
          "monomials): Hermitian for eta = %s with inertia %s, %d "
          "negative directions -- for the site placement the OS "
          "quotient DEGENERATES (indefinite completion): the contract "
          "kill branch fires there, i.e. RP again SELECTS the bond "
          "placement (contract precision (ii)) at quotient level"
          % (herm1, in1, picked[0], picked[1], picked[1][1]),
          FLAGS['c41'])


def c2_family_a():
    print("  -- C4.2: family A -- no PSD form, no quotient")
    r_anti = lambda a: (a + 8) % N16
    s_alt = lambda a: 1 if a % 2 == 0 else -1
    basis_a = [(a,) for a in range(8)]
    tw0 = (tuple(range(N16)), (1,) * N16)
    picked = None
    for etac in (sp.Integer(1), sp.Integer(-1), I, -I):
        Ma = term_matrix(basis_a, tw0, r_anti, s_alt, etac, N16)
        if hermitian_exact(Ma):
            ia, _ = spectrum_inertia(Ma)
            diag0 = all(iszero(Ma[i, i]) for i in range(8))
            picked = (etac, ia, diag0)
            break
    FLAGS['c42'] = (picked is not None and picked[1] == (4, 4, 0)
                    and picked[2])
    check("C4.2 FAMILY A (CLOCK-CENTRALISING ANTIPODE) -> NO QUOTIENT "
          "[exact + 40-digit]: the alternating-dressed antipode "
          "candidate (v519 R5.2) has a Hermitian OS form only for eta "
          "= %s, with ZERO diagonal (%s) and inertia %s -- INDEFINITE "
          "with 4 negative directions at the one-particle level "
          "already: no PSD form, no H_phys, no transfer -- the "
          "clock-centralising family cannot even ENTER the beta2 "
          "construction: RP and Theta rho Theta = rho^-1 keep "
          "selecting the SAME family in the quotient"
          % (picked[0], picked[2], picked[1]), FLAGS['c42'])


def c3_antichiral():
    print("  -- C4.3: anti-chiral state -- quotient exists only for the "
          "matching chirality")
    G8a = gram_of(BASIS8, R7, S7, N8, chi=-1)
    herm = hermitian_exact(G8a)
    in_all, _ = spectrum_inertia(G8a)
    in_ev, _ = block_inertia(G8a, list(range(8)))
    in_od, _ = block_inertia(G8a, list(range(8, 16)))
    FLAGS['c43'] = (herm and in_od == (0, 8, 0) and in_ev == (8, 0, 0)
                    and in_all == (8, 8, 0))
    check("C4.3 ANTI-CHIRAL STATE -> INDEFINITE COMPLETION [exact + "
          "40-digit]: with C -> -C and the SAME theta (eta = +i) the "
          "N = 8 full half-algebra Gram is Hermitian (%s) but its odd "
          "block flips to NEGATIVE definite %s while the even block "
          "stays PD %s: total inertia %s -- the OS quotient EXISTS "
          "ONLY for the chirality matching the twist (the v519 R5.3 "
          "kill-test-3 shadow upgraded to quotient level: quotient "
          "existence itself selects the chiral orientation)"
          % (herm, in_od, in_ev, in_all), FLAGS['c43'])


def c4_wrong_direction():
    print("  -- C4.4: wrong semigroup direction -- breaks off-domain, "
          "mirrors on-domain")
    D1w = dom_monos(BASIS8, 4, 6)
    Mw = term_matrix(D1w, TW8N[1], R7, S7, ETA, N8)
    herm_w = hermitian_exact(Mw)
    i4 = D1w.index((4,))
    wit = sp.simplify(Mw[i4, i4])
    n_match = n_anti = n_viol = 0
    impl_ok = True
    d = len(D1w)
    for i in range(d):
        ci, mi = theta_mono(D1w[i], R7, S7, ETA)
        for j in range(d):
            cj, mj = alpha_mono(D1w[j], TW8N[1])
            dij = Mw[i, j] - sp.conjugate(Mw[j, i])
            if iszero(dij):
                n_match += 1
                matched = True
            else:
                matched = False
                if iszero(Mw[i, j] + sp.conjugate(Mw[j, i])):
                    n_anti += 1
                else:
                    n_viol += 1
            cjt, mjt = theta_mono(D1w[j], R7, S7, ETA)
            cit, mit = alpha_mono(D1w[i], TW8N[1])
            ov = (set(mi) & set(mj)) or (set(mjt) & set(mit))
            if not ov and not matched:
                impl_ok = False
    D1m = dom_monos(BASIS8, 5, 7)
    Mm = term_matrix(D1m, TW8N[1], R7, S7, ETA, N8)
    herm_m = hermitian_exact(Mm)
    in_m, _ = spectrum_inertia(Mm) if herm_m else ((0, 0, 0), 0)
    in_f, _ = spectrum_inertia(FLAGS['taus8'][1][1])
    FLAGS['c44'] = (not herm_w and iszero(wit - I) and impl_ok
                    and herm_m and in_m == in_f)
    check("C4.4 WRONG SEMIGROUP DIRECTION [exact]: alpha_{-1} on the "
          "UNSHRUNK domain algebra{4,5,6} is NOT Hermitian (%s; exact "
          "diagonal witness omega(theta(g_4) alpha_{-1}(g_4)) = "
          "omega(i g_3 g_3) = %s, purely imaginary -- the shifted "
          "support crosses the cut INTO the reflected half), census "
          "(match, anti, viol) = (%d, %d, %d) with every mismatch a "
          "wrap-overlap entry (%s) -- the v522 mechanism reproduced in "
          "miniature; on the MIRRORED domain algebra{5,6,7} the same "
          "backward step is Hermitian (%s) with the mirror inertia %s "
          "= forward %s: the semigroup exists exactly INTO the half, "
          "in both theta-conjugate directions, and nowhere else"
          % (not herm_w, wit, n_match, n_anti, n_viol, impl_ok,
             herm_m, in_m, in_f),
          FLAGS['c44'])


# ---------------------------------------------------------------------------
# Part V -- kill-test bookkeeping and the frozen verdict
# ---------------------------------------------------------------------------
def v1_killtests():
    print("  -- V5.1: contract kill-test bookkeeping under beta2")
    touched = {
        1: FLAGS['g32'] and FLAGS['g33'],
        2: FLAGS['q_pd16'] and FLAGS['q_pd8'] and FLAGS['clock_herm_pd'],
        3: FLAGS['c43'] and FLAGS['t23'],
    }
    FLAGS['v51'] = all(touched.values())
    check("V5.1 KILL-TEST BOOKKEEPING [assembled]: beta2 touches three "
          "of the seven contract kill tests, none fires -- (1) Theta/"
          "clock compatibility: STRENGTHENED (the real structure "
          "descends anti-unitarily to H_phys, Kramers-free even on the "
          "odd sector: %s); (2) RP after gauge fixing: STRENGTHENED "
          "(positivity survives INTO the quotient -- H_phys PD and the "
          "clock transfer step PD; the GSO Z2 acts exactly: %s); (3) "
          "mirror generation: free shadow SHARPENED (the anti-chiral "
          "state admits NO quotient, and the odd-step transfer "
          "indefiniteness is the staggering/chirality datum: %s).  "
          "Kill tests (4) interacting Penrose grade, (5) net/OPE "
          "equivalence, (6) internal SU(2), (7) mark incidence: "
          "UNTOUCHED at the free level.  All seven stay formally live "
          "on the interacting algebra A_hol; the beta2 contract kill "
          "branch itself (quotient degenerates) does NOT fire (Q1.4)"
          % (touched[1], touched[2], touched[3]),
          FLAGS['v51'])


def v2_verdict():
    print("  -- V5.2: verdict per the frozen preregistration")
    kill = (not (FLAGS['q_pd16'] and FLAGS['q_pd8'])) \
        or (not FLAGS['clock_herm_pd'])
    s1 = FLAGS['q11'] and FLAGS['q12'] and FLAGS['q13'] and FLAGS['q14']
    s2 = FLAGS['t21'] and FLAGS['t22']
    s3 = FLAGS['t23'] and FLAGS['t24'] and FLAGS['t25'] and FLAGS['t27']
    s4 = FLAGS['g31'] and FLAGS['g32'] and FLAGS['g33']
    s5 = (FLAGS['c41'] and FLAGS['c42'] and FLAGS['c43']
          and FLAGS['c44'])
    kms_ok = FLAGS['kms_witnessed']
    if kill:
        verdict = "KILL"
    elif s1 and s2 and s3 and s4 and s5 and kms_ok:
        verdict = "SUCCESS"
    else:
        verdict = "UNDECIDED"
    FLAGS['verdict'] = verdict
    print("VERDICT: %s" % verdict)
    check("V5.2 BETA2 VERDICT = %s [frozen C-7 logic]: no kill (H_phys "
          "PD at both levels, the clock step Hermitian + PD on its "
          "domain); S1 quotient explicit (%s), S2 local transfer "
          "self-adjoint + semigroup + vacuum fixed (%s), S3 clock = "
          "T^{N/4} positive with spectral projections + reconstructed "
          "unitary rotation group (%s), S4 GSO grading + anti-unitary "
          "Theta descent (%s), S5 all five negative controls behave "
          "(%s); the single deviation from naive expectations -- NO "
          "contraction on the compact circle -- carries EXACTLY the "
          "pre-declared KMS witnesses (%s: silver-ratio norm drift "
          "C(1)/C(3) = 1 + sqrt(2), det(G - tau_4) < 0).  Scope fence: "
          "free/quadratic seam system only, deg <= 2 at N = 16, "
          "complete algebra at N = 8; no interacting algebra, no "
          "chirality theorem, no net equivalence.  WOIT.OS.TWISTOR.01 "
          "stays [O]; no marker moves; sandbox only"
          % (verdict, s1, s2, s3, s4, s5, kms_ok),
          verdict == "SUCCESS")


def run():
    print("woit_os_beta2_os_quotient_probe -- WOIT-beta2: the OS "
          "quotient of the free system made explicit (EXPLORATION "
          "ONLY)")
    q1_preconditions()
    q2_gram16()
    q3_gram8()
    q4_kill_branch()
    t1_domain_hermiticity()
    t2_semigroup()
    t3_positivity_pattern()
    t4_clock()
    t5_spectral_rotation()
    t6_kms()
    t7_v522_resolution()
    g1_gso()
    g2_theta_perp()
    g3_non_descent()
    c1_site_cut()
    c2_family_a()
    c3_antichiral()
    c4_wrong_direction()
    v1_killtests()
    v2_verdict()
    npass = sum(RESULTS)
    print("\n%d/%d checks passed  (runtime %.1f s)"
          % (npass, len(RESULTS), time.perf_counter() - T0_WALL))
    print("FINAL VERDICT: %s" % FLAGS.get('verdict', 'UNDECIDED'))
    return npass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
