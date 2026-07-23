"""seam_clock_silver_spectrum_probe.py -- EXPLORATION ONLY (sandbox).

Origin and readout-connection of the SILVER clock spectrum {1, sqrt(2)-1}
found by woit_os_beta2_os_quotient_probe.py (the compressed quarter-turn
transfer T^{N/4} on the OS quotient of the N = 8 seam circle).  Nothing in
verification/, ledger, papers, changelog, website or scorecard is touched;
no files are written; standalone; deterministic; runtime target < 15 min.

=== PREREGISTRATION (frozen BEFORE the run; criteria not adjusted after) ===

Two INDEPENDENT verdicts:
  VERDICT-STRUCTURE  (Part A): the closed-form origin of the silver
    spectrum.  SUCCESS iff every A-check passes (the chain below is
    machine-certified exactly / at 40 digits); otherwise UNDECIDED/KILL
    with the gap named.
  VERDICT-CONNECTION (Part B): a preregistered, look-elsewhere-counted
    scan of the frozen [E]-numbers for silver relations.  Logic frozen
    in [B-5] below.

Pre-derived exact anchors (declared BEFORE the run, to be machine-
confirmed; derived by hand from the beta2 Hankel structure):
 (a) the one-particle OS Gram at bond cut k = N-1 is the Hankel matrix
     G_ab = C(a+b-(N-1)), C(d) = (2/N)/sin(pi d/N) for odd d, else 0;
     the k-step transfer is the shifted Hankel T_ab = G_{a,b+k}.
 (b) at N = 8 the quarter-turn domain {4,5} makes both matrices
     DIAGONAL (C(2) = C(4) = 0), so the compressed clock spectrum is
     the pure kernel ratios {C(3)/C(1), C(5)/C(3)}
       = {sin(pi/8)/sin(3pi/8), sin(3pi/8)/sin(5pi/8)}
       = {tan(pi/8), 1}   with tan(pi/8) = sqrt(2)-1 = 1/delta_S.
 (c) the full domain-algebra clock is the SECOND QUANTISATION of the
     one-particle pencil: spectrum = all subset products of the
     one-particle eigenvalues -- this is the origin of the observed
     doubling {1, sqrt(2)-1} in BOTH parity sectors at N = 8.
 (d) scaling: the positive clock exists only for N == 0 mod 8 (for
     N == 4 mod 8 the shifted Hankel lands on the COMPLEMENTARY
     checkerboard: parity conjugation flips T -> -T, the pencil
     spectrum is symmetric +/-, indefinite -> contract-kill shape);
     for N = 16, 24, ... the silver value is NOT in the spectrum
     (exact certificates) and lambda_max(N) grows monotonically
     (numeric 40-digit): {1, 1/delta_S} is an N = 8 lattice datum,
     not a continuum limit.
 (e) controls N = 6 / 10 (no mu4: 4 does not divide N, the quarter
     turn is not a lattice step): the nearest even-step clocks give
     1/2 (N = 6, third turn) and the GOLDEN family {phi/2} u
     roots(lam^2 - phi lam + (phi-1)/2) (N = 10, fifth turn): the
     Dirichlet-kernel mechanism yields metallic trigonometry
     GENERICALLY; silver specifically = the mu4 quarter turn at N = 8.
 (f) gap: -ln(sqrt(2)-1) = ln(1+sqrt(2)) = ln delta_S = arcsinh(1)
     = gd^{-1}(pi/4) = ln tan(3pi/8); the beta2 KMS drift witness
     C(1)/C(3) = delta_S = e^{+DeltaK} exactly at N = 8 (and ONLY
     there: the N = 16 edge drift is a different number, exact
     inequality); arcsinh(1) != pi/4 = the naive continuum NS gap
     (theta r with theta = pi/2, r = 1/2).

[B] PREREGISTERED RELATION CLASS (Part B; frozen):
  candidate values  v = (p/q) * n * b * c3^f  with
    p, q coprime, 1 <= p, q <= 12          (small rationals)
    n in {1, 4, 8, 16, 1/4, 1/8, 1/16}     (|mu4| = 4 and N = 8, 16)
    b in {dS, dS^2, dS^-1, dS^-2, ln dS, 1/ln dS},  dS = 1+sqrt(2)
    f in {0, 1, 2}                          (c3 = 1/(8 pi))
  TARGETS (primary): the 16 "predictions" entries of
    verification/predictions_frozen.json (read-only); the two
    "assigned" integers and the bands/variants are EXCLUDED (rational
    targets trivialise the class).
  TARGETS (secondary, recorded separately, same discipline): phi0,
    lambda_C, and the v124 clock rates {6 ln(3/2), 6 ln 3}.
  HIT TIERS (relative |v/t - 1|):  T1 <= 1e-30 (exact candidate;
    must then be closed-form verified), T2 <= 1e-6, T3 <= 1e-3
    (calibration only).
  NULL EXPECTATION: analytic local-density estimate per target
    (candidates within a factor-2 log window / (2 ln 2), times 2 eps),
    summed; plus two placebo bases through the SAME class: golden
    phi_G = (1+sqrt(5))/2 and plastic rho (rho^3 = rho + 1), each with
    the analogous 6-element base set.
  [B-5] VERDICT-CONNECTION logic (frozen):
    ERFOLG   iff >= 1 T1 hit that survives closed-form verification;
    UNENTSCHIEDEN iff no T1 but T2_silver >= 3 AND
      T2_silver >= 3 * max(T2_golden, T2_plastic, E_T2);
    KILL otherwise (silver behaves like a placebo: no readout
      connection above the null expectation).
  Calibration sanity (must PASS): for every base with analytic
    E_T3 >= 3 the observed T3 count is within a factor 5 of E_T3.

=== FINDINGS (from the frozen-prereg run, 2026-07-23; 22/22) ===

VERDICT-STRUCTURE: SUCCESS -- the silver spectrum has a closed origin:
  * Hankel form G_ab = C(a+b-(N-1)), NS-Dirichlet carrier
    sum_{j<N/2} sin((2j+1)pi d/N) = 1/sin(pi d/N) certified as an
    exact Laurent-polynomial identity (all odd d, N = 8 and 16).
  * N = 8 quarter turn: domain {4,5} diagonalises the pencil exactly;
    spectrum = {C(3)/C(1), C(5)/C(3)} = {tan(pi/8), 1} = {1/delta_S, 1}
    exactly; even sector = {1, C(5)/C(1)} = {1, tan(pi/8)} exactly.
  * Second quantisation EXACT: N = 8 doubling = subset products of
    {tan(pi/8), 1}; N = 16 full 16-dim domain-algebra clock spectrum
    = all subset products of the 4 one-particle eigenvalues (40-digit,
    max deviation 2.8e-38); vacuum column fixed exactly (lambda = 1).
  * Geometric carrier: tan(pi/8) = tan((pi/4)/2) = the stereographic
    half-angle coordinate of the SILVER-MIDPOINT direction e^{i pi/4}
    (the mu = i cut points of the v519 torsor, e^{2 i theta} = i);
    pi/8 = 2pi/16 = the 16-Majorana bond angle = half the N = 8 site
    spacing; the quarter turn conjugates the OS cut axis into the
    perpendicular torsor mirror (axis k -> k + N/2: 15 -> 7 at N = 16,
    7 -> 3 at N = 8, exactly the beta2 theta_perp axes) up to the NS
    deck sign (S_{N/4} R_k S_{N/4}^{-1} = -R_{k+N/2} exactly, eps =
    -1 at both levels).
  * v512 tie: S_SILVER = 3 + 2 sqrt(2) = delta_S^2 = cot^2(pi/8)
    = e^{2 arcsinh(1)} exactly -- the SAME silver quantity (delta_S
    powers), but a different structural role (harmonic mark POSITION
    there, transfer EIGENVALUE here); no further identification.
  * Scaling: N == 4 mod 8 (12, 20): T lands on the complementary
    checkerboard, parity flips T -> -T, spectrum exactly symmetric
    +/- with a zero mode -- NO positive clock (mod-8 selection: the
    positive mu4 clock exists iff 8 | N).  N = 16: silver is NOT an
    eigenvalue (|det(T - (sqrt(2)-1)G)| = 8.7e-3, 9.1e-4 > 1e-30 on
    the two blocks); nor is 1; the tan(k pi/16) family all fail.
    N = 24: silver not an eigenvalue (3x3 blocks, dets 1.1e-5,
    2.0e-6 > 1e-30).  Numeric scan N = 8..40: lambda_max = 1 ->
    1.6414 -> 2.8055 -> 5.1033 -> 9.6447 (strictly increasing),
    lambda_min = 0.414 -> 0.0665 -> 0.00826 -> 9.5e-4 -> 1.0e-4 -> 0;
    nearest-to-silver distance does NOT converge to 0 (N = 40 false
    friend 0.4144378... vs 0.4142135...: differs at 2.24e-4 --
    40-digit discrimination).  {1, 1/delta_S} is a 16-Majorana/N = 8
    lattice datum, NOT a continuum datum.
  * Controls: N = 6 third turn = 1/2 exactly; N = 10 fifth turn =
    {phi/2} u roots(lam^2 - phi lam + (phi-1)/2) exactly (GOLDEN
    family, phi = (1+sqrt 5)/2): metallic trigonometry is generic,
    silver is the mu4-specific instance.
  * Gap: -ln(sqrt(2)-1) = ln delta_S = arcsinh(1) = gd^{-1}(pi/4)
    = ln tan(3pi/8) exactly; e^{-2 DeltaK} = 1/S_SILVER(v512); the
    beta2 KMS drift C(1)/C(3) = e^{+DeltaK} exactly at N = 8, while
    the N = 16 edge drift sin(7pi/16)/sin(pi/16) = 5.0273 matches
    neither 1/lambda_min = 15.04 nor any delta_S power (40-digit
    inequalities): the drift = gap coincidence is exclusive to
    N = 8; arcsinh(1) != pi/4 (naive continuum NS gap theta r at
    theta = pi/2, r = 1/2; separation 0.0960) at 40 digits.

VERDICT-CONNECTION: KILL -- no readout connection above null:
  * class size 91 coprime rationals x 7 x 6 x 3 = 11,466 candidates
    (5,598 distinct values), 16 primary + 4 secondary targets;
  * silver: T1 = 0, T2 = 0, T3 = 35 (primary); analytic null
    E_T3 = 24.9, E_T2 = 0.0249 -- observed T3 within the declared
    factor-5 calibration band of the null;
  * placebos: golden T3 = 23, plastic T3 = 20 (comparable: the class
    is calibrated, not silver-tuned); golden/plastic T2 = 0 = silver;
  * closest approach anywhere: MC_OVER_MS at rel. distance 1.03e-5
    (recorded; a factor 10 above the T2 threshold, and ~0.26 such
    approaches are expected by chance across the census -- no
    overshoot);
  * secondary targets (phi0, lambda_C, v124 rates 6 ln(3/2), 6 ln 3):
    T1 = T2 = 0 (T3 = 10);
  * per frozen [B-5] logic: KILL.  The silver ratio does not reach
    the frozen readout numbers through the declared narrow class.

TRANSPARENCY (tooling only; preregistration text unchanged): run 1
scored 20/22 -- the two misses were sympy simplification gaps, not
substantive: (i) log(3 + 2 sqrt(2)) - 2 asinh(1) and (ii)
sinh(ln(1 + sqrt(2))) - 1 do not close under plain simplify();
both are now certified via exact algebraic square/exp-rewrite
identities (S = delta_S^2 exactly, asinh(1).rewrite(log) =
log(delta_S) exactly, radsimp of the exp form) plus 40-digit zeros.
No criterion, tolerance or expectation was changed.

Construction base (READ-ONLY): experiments/tfpt-discovery/
woit_os_beta2_os_quotient_probe.py (kernel, Pfaffian-Wick, theta/tower
machinery -- copied verbatim where possible), verification/
v519_woit_theta_rp_free.py (torsor/silver-midpoint data),
verification/v512_seam_tau_flag.py (S_SILVER), verification/
v100_numerology_null_mc.py (null-census methodology), verification/
predictions_frozen.json + tfpt_constants.py (frozen inventories),
verification/v124_resummed_clock.py (clock-chain rates).

Exact throughout (sympy trig-algebraic entries, Pfaffian-Wick);
definiteness/membership certificates are 40-digit (mp.mp.dps = 40,
threshold 1e-30) on exact Hermitian matrices.

Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/seam_clock_silver_spectrum_probe.py
"""
import json
import os
import time
from bisect import bisect_left, bisect_right
from itertools import combinations
from math import gcd

import mpmath as mp
import sympy as sp

mp.mp.dps = 40

I = sp.I
ETA = I
RESULTS = []
T0_WALL = time.perf_counter()

SILVER = sp.sqrt(2) - 1                 # tan(pi/8) = 1/delta_S
DELTA_S = 1 + sp.sqrt(2)                # the silver ratio
S_SILVER_V512 = 3 + 2 * sp.sqrt(2)      # v512 silver mark position
PHI_G = (1 + sp.sqrt(5)) / 2            # golden (control)


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
# chiral NS kernel + Pfaffian-Wick + theta/shift machinery (beta2 verbatim)
# ---------------------------------------------------------------------------
def c_of(d, n):
    if d % 2 == 0:
        return sp.Integer(0)
    return sp.Rational(2, n) / sp.sin(sp.pi * sp.Rational(d, n))


def g2f(a, b, n):
    if a == b:
        return sp.Integer(1)
    return I * c_of(a - b, n)


_WICK = {}


def wick(idx, n):
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
        tot += (-1) ** j * g2f(head, b, n) * wick(sub, n)
    tot = sp.expand_complex(tot)
    _WICK[key] = tot
    return tot


def refl_map(k, n):
    def r(a):
        return (k - a) % n

    def s(a):
        return -1 if (k - a) % (2 * n) >= n else 1
    return r, s


def theta_mono(mono, r, s, eta):
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


def shift_mono(m, k, n):
    """alpha_k on a sorted monomial with NS wrap sign -1 per crossing."""
    c = 1
    imgs = []
    for a in m:
        q = a + k
        c *= (-1 if q >= n else 1)
        imgs.append(q % n)
    lst = list(imgs)
    sgn = 1
    for i in range(len(lst)):
        for j in range(len(lst) - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                sgn = -sgn
    assert len(set(lst)) == len(lst)
    return c * sgn, tuple(lst)


def os_entry(ea, eb, k, r, s, n):
    """omega(theta(e_a) alpha_k(e_b)), exact (eta = +i pinned by v519)."""
    ca, ma = theta_mono(ea, r, s, ETA)
    cb, mb = shift_mono(eb, k, n)
    cs, mm = mono_mul(ma, mb)
    return sp.expand_complex(ca * cb * cs * wick(mm, n))


def os_matrix(basis, k, r, s, n):
    d = len(basis)
    return sp.Matrix(d, d, lambda i, j: os_entry(basis[i], basis[j],
                                                 k, r, s, n))


def hermitian_exact(M):
    d = M - M.conjugate().T
    return all(iszero(x) for x in d)


def to_mp(M):
    A = mp.matrix(M.rows, M.cols)
    for i in range(M.rows):
        for j in range(M.cols):
            re_, im_ = M[i, j].evalf(45).as_real_imag()
            A[i, j] = mp.mpc(mp.mpf(str(re_)), mp.mpf(str(im_)))
    return A


def ctr(A):
    B = mp.matrix(A.cols, A.rows)
    for i in range(A.rows):
        for j in range(A.cols):
            B[j, i] = mp.conj(A[i, j])
    return B


def frame_spec(Gs, Ts):
    """spectrum of the G-compressed pencil (exact input, 40-digit out)."""
    G, T = to_mp(Gs), to_mp(Ts)
    n = G.rows
    EG, QG = mp.eighe(G)
    Gis = QG * mp.diag([1 / mp.sqrt(EG[i]) for i in range(n)]) * ctr(QG)
    B = Gis * T * Gis
    B = (B + ctr(B)) * mp.mpf('0.5')
    EB, _ = mp.eighe(B)
    return sorted([EB[i].real for i in range(n)])


def one_particle_pencil_mp(N):
    """pure-mpmath quarter-turn pencil on {N/2 .. 3N/4-1} (Hankel form)."""
    def Cmp(d):
        if d % 2 == 0:
            return mp.mpf(0)
        return (mp.mpf(2) / N) / mp.sin(mp.pi * d / N)
    dom = list(range(N // 2, 3 * N // 4))
    m = len(dom)
    G = mp.matrix(m, m)
    T = mp.matrix(m, m)
    for i, a in enumerate(dom):
        for j, b in enumerate(dom):
            G[i, j] = Cmp(a + b - (N - 1))
            T[i, j] = Cmp(a + b - (N - 1) + N // 4)
    return G, T


def pencil_spec_mp(G, T):
    n = G.rows
    EG, QG = mp.eighe(G)
    Gis = QG * mp.diag([1 / mp.sqrt(EG[i]) for i in range(n)]) * QG.T
    B = Gis * T * Gis
    B = (B + B.T) * mp.mpf('0.5')
    EB, _ = mp.eighe(B)
    return sorted([EB[i] for i in range(n)])


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


def hankel_pencil_exact(N, dom, k):
    m = len(dom)
    G = sp.Matrix(m, m, lambda i, j: c_of(dom[i] + dom[j] - (N - 1), N))
    T = sp.Matrix(m, m, lambda i, j: c_of(dom[i] + dom[j] - (N - 1) + k, N))
    return G, T


def det40(M):
    """40-digit |det| of an exact matrix (nonzero-certificate helper)."""
    v = sp.det(M).evalf(45)
    re_, im_ = v.as_real_imag()
    return mp.sqrt(mp.mpf(str(re_)) ** 2 + mp.mpf(str(im_)) ** 2)


TOL30 = mp.mpf(10) ** (-30)


# ---------------------------------------------------------------------------
# Part A1 -- closed-form origin
# ---------------------------------------------------------------------------
def a1_1_hankel():
    print("  -- A1.1: the one-particle OS Gram is the Hankel kernel")
    ok = True
    for N in (8, 16):
        r, s = refl_map(N - 1, N)
        half = list(range(N // 2, N))
        for a in half:
            for b in half:
                lhs = os_entry((a,), (b,), 0, r, s, N)
                if not iszero(lhs - c_of(a + b - (N - 1), N)):
                    ok = False
        # checkerboard: C(even) = 0
        for d in range(0, N, 2):
            if c_of(d, N) != 0:
                ok = False
    # PD certificates (40-digit)
    pd = True
    for N in (8, 16):
        G, _ = one_particle_pencil_mp(N)
        # extend to the full half for the PD statement
        def Cmp(d):
            return (mp.mpf(2) / N) / mp.sin(mp.pi * d / N) if d % 2 else \
                mp.mpf(0)
        half = list(range(N // 2, N))
        m = len(half)
        Gh = mp.matrix(m, m)
        for i, a in enumerate(half):
            for j, b in enumerate(half):
                Gh[i, j] = Cmp(a + b - (N - 1))
        E, _ = mp.eighe(Gh)
        if min(E[i] for i in range(m)) <= TOL30:
            pd = False
    check("A1.1 HANKEL FORM OF THE QUOTIENT [exact + 40-digit]: at the "
          "v519 bond cut k = N-1 the one-particle OS Gram is EXACTLY the "
          "Hankel matrix G_ab = C(a+b-(N-1)) with the chiral NS kernel "
          "C(d) = (2/N)/sin(pi d/N) (odd d; C(even) = 0 checkerboard), "
          "certified entrywise through the full theta/Wick machinery at "
          "N = 8 and N = 16 (%s), and the half-circle Gram is PD (%s) -- "
          "the k-step transfer is the SHIFTED Hankel T_ab = G_{a,b+k}: "
          "the whole clock question is a Hankel-pencil question about "
          "the kernel 1/sin" % (ok, pd), ok and pd)


def a1_2_dirichlet():
    print("  -- A1.2: NS-Dirichlet carrier of the kernel")
    z = sp.symbols('z')
    ok_laurent = True
    for N in (8, 16):
        M = N // 2
        S = sum(z ** (2 * j + 1) - z ** (-(2 * j + 1)) for j in range(M))
        # (z - 1/z) * S telescopes to z^N + z^-N - 2 identically
        if sp.expand((z - 1 / z) * S - (z ** N + z ** (-N) - 2)) != 0:
            ok_laurent = False
    # at z = e^{i pi d / N} with d odd: z^N = -1 -> (z-1/z) S = -4
    # -> sum_j sin((2j+1) pi d/N) * sin(pi d/N) = 1 exactly
    ok_num = True
    for N in (8, 16):
        for d in range(1, 2 * N, 2):
            sd = mp.sin(mp.pi * d / N)
            tot = mp.fsum(mp.sin((2 * j + 1) * mp.pi * d / N)
                          for j in range(N // 2))
            if abs(tot * sd - 1) > TOL30:
                ok_num = False
    check("A1.2 NS-DIRICHLET CARRIER [exact Laurent identity]: "
          "(z - 1/z) sum_{j<N/2} (z^{2j+1} - z^{-(2j+1)}) = z^N + z^{-N} "
          "- 2 identically (%s), so at z = e^{i pi d/N}, d odd (z^N = -1) "
          "the geometric NS-momentum sum sum_j sin((2j+1) pi d/N) equals "
          "1/sin(pi d/N) EXACTLY (40-digit spot check all odd d, N = 8 "
          "and 16: %s) -- the kernel C(d) IS the Dirichlet sum over the "
          "N/2 positive NS momenta: the clock eigenvalues below are "
          "ratios of these Dirichlet kernels" % (ok_laurent, ok_num),
          ok_laurent and ok_num)


def a1_3_n8_odd():
    print("  -- A1.3: N = 8 quarter turn, odd sector -- the exact chain")
    N = 8
    G, T = hankel_pencil_exact(N, [4, 5], 2)
    diag_ok = iszero(G[0, 1]) and iszero(G[1, 0]) and iszero(T[0, 1]) \
        and iszero(T[1, 0])
    lam_a = sp.simplify(T[0, 0] / G[0, 0])     # C(3)/C(1)
    lam_b = sp.simplify(T[1, 1] / G[1, 1])     # C(5)/C(3)
    chain = [
        iszero(lam_a - sp.sin(sp.pi / 8) / sp.sin(3 * sp.pi / 8)),
        iszero(sp.sin(3 * sp.pi / 8) - sp.cos(sp.pi / 8)),
        iszero(lam_a - sp.tan(sp.pi / 8)),
        iszero(sp.tan(sp.pi / 8) - SILVER),
        iszero(sp.sin(5 * sp.pi / 8) - sp.sin(3 * sp.pi / 8)),
        iszero(lam_b - 1),
        iszero(SILVER - 1 / DELTA_S),
    ]
    check("A1.3 THE CLOSED CHAIN, ODD SECTOR [exact]: on the quarter-"
          "turn domain {4,5} the pencil is DIAGONAL (C(2) = C(4) = 0: "
          "%s), so the compressed clock spectrum is the pure kernel "
          "ratio pair {C(3)/C(1), C(5)/C(3)} = {sin(pi/8)/sin(3pi/8), "
          "sin(3pi/8)/sin(5pi/8)}; the chain sin(3pi/8) = cos(pi/8) => "
          "C(3)/C(1) = tan(pi/8) = sqrt(2)-1 = 1/delta_S and sin(5pi/8) "
          "= sin(3pi/8) => C(5)/C(3) = 1 closes EXACTLY (%s) -- the "
          "silver eigenvalue is the half-angle tangent forced by the "
          "complementary bond distances d = 1, 3 (1 + 3 = N/2) under "
          "the quarter-turn shift N/4 = 2"
          % (diag_ok, all(chain)), diag_ok and all(chain))


def a1_4_even_and_secondquant():
    print("  -- A1.4: even sector + second quantisation (the doubling)")
    N = 8
    r, s = refl_map(7, N)
    # even sector on the domain algebra {4,5}: basis {1, g4 g5}
    be = [(), (4, 5)]
    Ge = os_matrix(be, 0, r, s, N)
    Te = os_matrix(be, 2, r, s, N)
    herm = hermitian_exact(Ge) and hermitian_exact(Te)
    tr_ok = iszero(sp.simplify((Ge.inv() * Te).trace()) - (1 + SILVER))
    det_ok = iszero(sp.simplify(sp.det(Te) / sp.det(Ge)) - SILVER)
    mem1 = iszero(sp.det(Te - Ge))
    mem_s = iszero(sp.det(Te - SILVER * Ge))
    prod_id = iszero(sp.simplify(c_of(5, N) / c_of(1, N)) - SILVER)
    # second quantisation at N = 16: full 2^4 domain algebra on {8..11}
    N2 = 16
    r2, s2 = refl_map(15, N2)
    dom = [8, 9, 10, 11]
    basis = [m for d in range(5) for m in combinations(dom, d)]
    Gf = os_matrix(basis, 0, r2, s2, N2)
    Tf = os_matrix(basis, 4, r2, s2, N2)
    spec_full = frame_spec(Gf, Tf)
    b1 = [(a,) for a in dom]
    G1 = os_matrix(b1, 0, r2, s2, N2)
    T1 = os_matrix(b1, 4, r2, s2, N2)
    spec1 = frame_spec(G1, T1)
    prods = sorted(mp.mpf(1) if not S else
                   mp.fprod([spec1[i] for i in S])
                   for dd in range(5) for S in combinations(range(4), dd))
    dev = max(abs(a - b) for a, b in zip(prods, spec_full))
    sq_ok = dev < TOL30
    # vacuum fixed: tau(a, ()) = Gram(a, ()) for every a (lambda = 1)
    vac_ok = all(iszero(Tf[i, 0] - Gf[i, 0]) for i in range(len(basis)))
    check("A1.4 SECOND QUANTISATION = THE DOUBLING [exact + 40-digit]: "
          "the N = 8 EVEN sector {1, g4 g5} has generalized spectrum "
          "{1, C(5)/C(1)} with C(5)/C(1) = tan(pi/8) exactly (Vieta "
          "trace/det %s/%s, membership dets zero for lambda = 1 and "
          "sqrt(2)-1: %s/%s; telescoped product C(5)/C(1) = "
          "(C(3)/C(1))(C(5)/C(3)): %s) -- so BOTH parity sectors carry "
          "{1, 1/delta_S}: the doubling is the fermionic second "
          "quantisation of the one-particle pair {tan(pi/8), 1}; at "
          "N = 16 the FULL 16-dim domain-algebra clock spectrum equals "
          "all subset products of the 4 one-particle eigenvalues "
          "(max deviation %s < 1e-30: %s) and the vacuum column is "
          "fixed exactly (lambda = 1: %s)"
          % (tr_ok, det_ok, mem1, mem_s, prod_id, mp.nstr(dev, 3),
             sq_ok, vac_ok),
          herm and tr_ok and det_ok and mem1 and mem_s and prod_id
          and sq_ok and vac_ok)


def a1_5_geometry():
    print("  -- A1.5: the geometric carrier (torsor / bond angle)")
    # silver-midpoint cut points of the v519 mu = i axis: e^{2 i th} = i
    cut_ok = all(iszero(sp.exp(2 * I * t) - I)
                 for t in (sp.pi / 4, 5 * sp.pi / 4))
    # tan(pi/8) = tan(theta_cut / 2): stereographic half-angle coordinate
    stereo = iszero(sp.tan((sp.pi / 4) / 2) - SILVER)
    # pi/8 = 2 pi/16 = 16-Majorana bond angle = half the N = 8 spacing
    bond = iszero(sp.pi / 8 - 2 * sp.pi / 16) \
        and iszero(sp.pi / 8 - (2 * sp.pi / 8) / 2)
    # quarter turn conjugates the cut axis into the perpendicular
    # torsor mirror: S_{N/4} R_k S_{N/4}^{-1} = +- R_{k+N/2}
    conj = {}
    for N, kcut in ((16, 15), (8, 7)):
        S = sp.Matrix(shift_matrix(N, N // 4, -1))
        Rk = sp.Matrix(refl_matrix(N, kcut, -1))
        Rp = sp.Matrix(refl_matrix(N, (kcut + N // 2) % N, -1))
        M = S * Rk * S.inv()
        if M == Rp:
            conj[N] = '+1'
        elif M == -Rp:
            conj[N] = '-1'
        else:
            conj[N] = 'FAIL'
    conj_ok = all(v in ('+1', '-1') for v in conj.values())
    check("A1.5 GEOMETRIC CARRIER [exact]: the clock eigenvalue is the "
          "HALF-ANGLE TANGENT OF THE SILVER MIDPOINT -- the mu = i "
          "torsor axis of v519 W-S2.4 cuts the seam at e^{i pi/4}, "
          "e^{i 5pi/4} (e^{2 i theta} = i: %s), and tan((pi/4)/2) = "
          "sqrt(2)-1 exactly (%s): the eigenvalue is the stereographic "
          "coordinate of the silver-midpoint direction; equivalently "
          "pi/8 = 2pi/16 = the 16-Majorana BOND ANGLE = half the N = 8 "
          "site spacing (%s); and the quarter turn maps the OS cut "
          "axis to the PERPENDICULAR torsor mirror, axis k -> k + N/2 "
          "(15 -> 7 at N = 16, 7 -> 3 at N = 8; signed-permutation "
          "identity S_{N/4} R_k S_{N/4}^{-1} = eps R_{k+N/2} with eps "
          "= %s) -- exactly the beta2 theta_perp axes: the clock's own "
          "quarter step interchanges the two clock-orbits of the mu4 "
          "torsor" % (cut_ok, stereo, bond, conj),
          cut_ok and stereo and bond and conj_ok)


def a1_6_v512():
    print("  -- A1.6: the v512 silver configuration -- same quantity?")
    # log(3 + 2 sqrt(2)) = 2 arcsinh(1): certified via the exact
    # algebraic square identity + asinh -> log rewrite + exp transport
    # (sympy's plain simplify does not close nested log/asinh forms)
    log_id = (iszero(S_SILVER_V512 - DELTA_S ** 2)
              and iszero(sp.asinh(1).rewrite(sp.log) - sp.log(DELTA_S))
              and iszero(sp.radsimp(S_SILVER_V512 / DELTA_S ** 2) - 1))
    num0 = abs(mp.log(3 + 2 * mp.sqrt(2)) - 2 * mp.asinh(1)) < TOL30
    ids = [
        iszero(S_SILVER_V512 - DELTA_S ** 2),
        iszero(S_SILVER_V512 - sp.cot(sp.pi / 8) ** 2),
        log_id and num0,
        iszero(DELTA_S - sp.cot(sp.pi / 8)),
        iszero(DELTA_S - sp.tan(3 * sp.pi / 8)),
    ]
    check("A1.6 v512 TIE [exact]: the v512 'silver' mark position "
          "S_SILVER = 3 + 2 sqrt(2) is EXACTLY delta_S^2 = cot^2(pi/8) "
          "= e^{2 arcsinh(1)} (%s) -- the SAME silver quantity (powers "
          "of delta_S = cot(pi/8) = tan(3pi/8)) as the clock eigenvalue "
          "1/delta_S = tan(pi/8), NOT a name coincidence; role typing "
          "stays separate: in v512 it is a harmonic mark POSITION on a "
          "topologically dead configuration (negative control there), "
          "here it is the transfer EIGENVALUE of the pinned mu4 clock "
          "-- common exact source: the pi/8 half-angle family of the "
          "16-Majorana circle" % ids, all(ids))


# ---------------------------------------------------------------------------
# Part A2 -- scaling in N
# ---------------------------------------------------------------------------
def a2_mod8(N, num):
    dom = list(range(N // 2, 3 * N // 4))
    G, T = hankel_pencil_exact(N, dom, N // 4)
    m = len(dom)
    # complementary checkerboard: G odd a+b support, T even a+b support
    comp = all(iszero(G[i, j] * T[i, j]) for i in range(m)
               for j in range(m))
    # parity conjugation P = diag((-1)^a): P G P = G, P T P = -T
    P = sp.diag(*[sp.Integer(-1) ** a for a in dom])
    par = (sp.expand(P * G * P - G) == sp.zeros(m, m)
           and sp.expand(P * T * P + T) == sp.zeros(m, m))
    tr0 = iszero(sp.simplify((G.inv() * T).trace()))
    spec = frame_spec(G, T)
    paired = all(abs(spec[i] + spec[m - 1 - i]) < TOL30
                 for i in range(m // 2))
    zero_mode = (m % 2 == 1) and abs(spec[m // 2]) < TOL30
    indef = spec[0] < -mp.mpf('1e-3')
    check("A2.%d N = %d (N/4 = %d ODD) -> NO CLOCK [exact mechanism + "
          "40-digit]: the quarter-turn shift lands on the COMPLEMENTARY "
          "checkerboard (G_ij T_ij = 0 entrywise: %s); the site-parity "
          "conjugation P = diag((-1)^a) fixes G and FLIPS T (P G P = G, "
          "P T P = -T: %s), so the compressed clock anticommutes with a "
          "unitary involution: spectrum exactly symmetric +/- (paired "
          "at 40 digits: %s; trace(G^-1 T) = 0 exactly: %s) with a "
          "zero mode (%s) -- indefinite (%s), no positive transfer "
          "step, no spectral calculus: the POSITIVE mu4 clock exists "
          "only for N == 0 mod 8"
          % (num, N, N // 4, comp, par, paired, tr0, zero_mode, indef),
          comp and par and tr0 and paired and zero_mode and indef)


def a2_3_n16_membership():
    print("  -- A2.3: N = 16 -- silver is NOT in the spectrum (exact)")
    N = 16
    # checkerboard blocks {8,10} and {9,11}
    dets_s, dets_1 = [], []
    for blk in ([8, 10], [9, 11]):
        G, T = hankel_pencil_exact(N, blk, 4)
        dets_s.append(det40(T - SILVER * G))
        dets_1.append(det40(T - G))
    non_silver = all(d > TOL30 for d in dets_s)
    non_one = all(d > TOL30 for d in dets_1)
    # tan-family hypothesis: tan(k pi/16), k = 1..7 -- all fail
    fam_fail = True
    for k in range(1, 8):
        lam = sp.tan(k * sp.pi / 16)
        for blk in ([8, 10], [9, 11]):
            G, T = hankel_pencil_exact(N, blk, 4)
            if det40(T - lam * G) <= TOL30:
                fam_fail = False
    check("A2.3 N = 16: THE SILVER VALUE DOES NOT SURVIVE [exact "
          "entries, 40-digit nonzero certificates]: det(T - (sqrt(2)-1) "
          "G) = %s, %s on the two checkerboard blocks (both > 1e-30) -- "
          "sqrt(2)-1 is NOT an eigenvalue of the N = 16 one-particle "
          "clock; neither is 1 (dets %s, %s; the vacuum lambda = 1 "
          "lives at the ALGEBRA level as the empty product, A1.4); the "
          "naive family guess lambda in {tan(k pi/16)} fails for ALL "
          "k = 1..7 (%s): no tan(pi/N) family"
          % (mp.nstr(dets_s[0], 3), mp.nstr(dets_s[1], 3),
             mp.nstr(dets_1[0], 3), mp.nstr(dets_1[1], 3), fam_fail),
          non_silver and non_one and fam_fail)


def a2_4_n24_membership():
    print("  -- A2.4: N = 24 -- silver is NOT in the spectrum")
    N = 24
    dets = []
    pd_ok = True
    for blk in ([12, 14, 16], [13, 15, 17]):
        G, T = hankel_pencil_exact(N, blk, 6)
        dets.append(det40(T - SILVER * G))
        E, _ = mp.eighe(to_mp(G))
        if min(E[i].real for i in range(3)) <= TOL30:
            pd_ok = False
    check("A2.4 N = 24: SILVER ABSENT AGAIN [exact entries, 40-digit]: "
          "det(T - (sqrt(2)-1) G) = %s, %s on the two 3x3 checkerboard "
          "blocks (both > 1e-30), with PD Gram blocks (%s) -- the exact "
          "silver eigenvalue does not recur at the next mod-8 level "
          "either" % (mp.nstr(dets[0], 3), mp.nstr(dets[1], 3), pd_ok),
          all(d > TOL30 for d in dets) and pd_ok)


def a2_5_scan():
    print("  -- A2.5: numeric N-scan -- artefact vs continuum datum")
    silver = mp.sqrt(2) - 1
    lam_max, lam_min, nearest = [], [], []
    Ns = [8, 16, 24, 32, 40]
    for N in Ns:
        G, T = one_particle_pencil_mp(N)
        spec = pencil_spec_mp(G, T)
        lam_max.append(spec[-1])
        lam_min.append(spec[0])
        nearest.append(min(abs(s - silver) for s in spec))
    mono_up = all(lam_max[i] < lam_max[i + 1] for i in range(len(Ns) - 1))
    mono_dn = all(lam_min[i] > lam_min[i + 1] for i in range(len(Ns) - 1))
    exact_at_8 = nearest[0] < TOL30
    absent_after = all(d > mp.mpf('1e-4') for d in nearest[1:])
    false_friend = abs(nearest[-1] - mp.mpf('2.242736e-4')) \
        < mp.mpf('1e-9')
    check("A2.5 SCALING VERDICT: N = 8 DATUM, NOT A CONTINUUM LIMIT "
          "[40-digit scan N = 8..40]: lambda_max = %s strictly "
          "increasing (%s; no bounded limit -- the thermal/KMS "
          "non-contraction escalates), lambda_min = %s strictly "
          "decreasing to 0 (%s); distance of the spectrum to sqrt(2)-1: "
          "%s -- EXACTLY zero only at N = 8 (%s), bounded away (> 1e-4) "
          "for all larger N (%s) incl. the N = 40 FALSE FRIEND "
          "0.4144378... vs 0.4142135... (gap 2.24e-4: %s, a "
          "look-elsewhere lesson at 40 digits): the silver spectrum is "
          "a 16-Majorana/N = 8 lattice datum, not a continuum datum"
          % ([mp.nstr(x, 6) for x in lam_max], mono_up,
             [mp.nstr(x, 3) for x in lam_min], mono_dn,
             [mp.nstr(x, 3) for x in nearest], exact_at_8, absent_after,
             false_friend),
          mono_up and mono_dn and exact_at_8 and absent_after
          and false_friend)


def a2_6_n6():
    print("  -- A2.6: control N = 6 (no mu4)")
    N = 6
    quarter_not_lattice = (N % 4 != 0)
    G, T = hankel_pencil_exact(N, [3], 2)
    lam = sp.simplify(T[0, 0] / G[0, 0])
    ok = iszero(lam - sp.Rational(1, 2))
    check("A2.6 CONTROL N = 6 [exact]: 4 does not divide 6 -- the "
          "quarter turn is NOT a lattice step (%s), there is no mu4 "
          "clock; the nearest even-step clock (third turn, k = 2, "
          "domain {3}) has the single eigenvalue C(3)/C(1) = "
          "sin(pi/6)/sin(pi/2) = 1/2 EXACTLY (%s) -- a plain rational, "
          "no silver" % (quarter_not_lattice, ok),
          quarter_not_lattice and ok)


def a2_7_n10():
    print("  -- A2.7: control N = 10 (no mu4) -- the GOLDEN family")
    N = 10
    quarter_not_lattice = (N % 4 != 0)
    # fifth turn k = 2 on domain {5,6,7}; checkerboard {5,7} (+) {6}
    G2, T2 = hankel_pencil_exact(N, [5, 7], 2)
    tr = sp.simplify((G2.inv() * T2).trace())
    dt = sp.simplify(sp.det(T2) / sp.det(G2))
    ok_tr = iszero(tr - PHI_G)
    ok_dt = iszero(dt - (PHI_G - 1) / 2)
    lam6 = sp.simplify(c_of(5, N) / c_of(3, N))
    ok_6 = iszero(lam6 - PHI_G / 2) and iszero(lam6 - sp.cos(sp.pi / 5))
    check("A2.7 CONTROL N = 10 [exact]: 4 does not divide 10 (%s) -- no "
          "mu4 clock; the fifth-turn clock (k = 2, domain {5,6,7}) has "
          "the GOLDEN spectrum: block {6} eigenvalue C(5)/C(3) = "
          "sin(3pi/10) = cos(pi/5) = phi/2 exactly (%s); block {5,7} "
          "satisfies lambda^2 - phi lambda + (phi-1)/2 = 0 exactly "
          "(Vieta: trace = phi: %s, det ratio = (phi-1)/2: %s) -- the "
          "Dirichlet-kernel mechanism yields METALLIC trigonometry for "
          "every small N (1/2 at N = 6, golden at N = 10, SILVER at "
          "N = 8): what singles out silver is not the mechanism but the "
          "mu4 quarter turn itself, which exists exactly at the "
          "16-Majorana levels N == 0 mod 8"
          % (quarter_not_lattice, ok_6, ok_tr, ok_dt),
          quarter_not_lattice and ok_tr and ok_dt and ok_6)


# ---------------------------------------------------------------------------
# Part A4 -- the gap and the KMS structure
# ---------------------------------------------------------------------------
def a4_1_gap():
    print("  -- A4.1: the spectral gap in closed form")
    # sinh(ln delta_S) = (delta_S - 1/delta_S)/2 = 1: exp-rewrite +
    # radsimp (plain simplify does not close it), plus 40-digit zero
    sinh_id = (iszero(sp.radsimp(sp.expand(
        sp.sinh(sp.log(DELTA_S)).rewrite(sp.exp))) - 1)
        and abs(mp.sinh(mp.log(1 + mp.sqrt(2))) - 1) < TOL30)
    ids = [
        iszero(-sp.log(SILVER) - sp.log(DELTA_S)),
        iszero(sp.log(DELTA_S) - sp.asinh(1)),
        sinh_id,
        iszero(sp.exp(-2 * sp.asinh(1)) - 1 / S_SILVER_V512),
    ]
    check("A4.1 GAP CLOSED FORM [exact]: the modular generator K = "
          "-ln(compressed clock) has per-sector spectrum {0, DeltaK} "
          "with DeltaK = -ln(sqrt(2)-1) = ln(1+sqrt(2)) = ln delta_S = "
          "arcsinh(1) (%s; sinh(DeltaK) = 1 exactly: %s); the doubled "
          "algebra spectrum is the additive second quantisation "
          "{0, DeltaK} per sector (A1.4); and e^{-2 DeltaK} = "
          "1/S_SILVER(v512) exactly (%s) -- the v512 silver position is "
          "the two-quantum Boltzmann factor of the clock gap"
          % (ids[0] and ids[1], ids[2], ids[3]), all(ids))


def a4_2_kms():
    print("  -- A4.2: the beta2 KMS drift vs the gap")
    N = 8
    drift8 = sp.simplify(c_of(1, N) / c_of(3, N))
    ok8 = iszero(drift8 - DELTA_S) \
        and iszero(drift8 - sp.exp(sp.asinh(1)))
    # N = 16 edge drift ||T(4)[g_11]||^2/||[g_11]||^2 = C(15)/C(7)
    N2 = 16
    drift16 = sp.simplify(c_of(15, N2) / c_of(7, N2))
    d16 = mp.mpf(str(drift16.evalf(45)))
    G1, T1 = one_particle_pencil_mp(16)
    spec16 = pencil_spec_mp(G1, T1)
    neq_min = abs(d16 - 1 / spec16[0]) > mp.mpf('1e-3')
    neq_ds = min(abs(d16 - (mp.mpf(1) + mp.sqrt(2)) ** k)
                 for k in (1, 2, 3)) > mp.mpf('1e-3')
    check("A4.2 DRIFT = e^{+DeltaK} EXACTLY AT N = 8, AND ONLY THERE "
          "[exact + 40-digit]: the pre-declared beta2 KMS witness "
          "C(1)/C(3) = 1 + sqrt(2) IS e^{+DeltaK} (%s) -- the edge-mode "
          "norm expansion and the clock gap are the same number "
          "(2-site exactness: the drift ratio is the inverse of the "
          "eigenvalue ratio); at N = 16 the analogous edge drift "
          "C(15)/C(7) = sin(7pi/16)/sin(pi/16) = %s matches neither "
          "1/lambda_min = %s (%s) nor any delta_S power (%s): the "
          "drift/gap coincidence is EXCLUSIVE to the N = 8 level"
          % (ok8, mp.nstr(d16, 8), mp.nstr(1 / spec16[0], 8),
             neq_min, neq_ds), ok8 and neq_min and neq_ds)


def a4_3_gudermann():
    print("  -- A4.3: Gudermannian form of the gap; continuum contrast")
    gd_ok = iszero(sp.asinh(1) - sp.log(sp.tan(3 * sp.pi / 8))) \
        and iszero(sp.log(sp.tan(sp.pi / 8 + sp.pi / 4))
                   - sp.log(sp.tan(3 * sp.pi / 8)))
    # arcsinh(1) != pi/4 (naive continuum NS gap theta*r, theta = pi/2,
    # r = 1/2) -- 40-digit separation
    sep = abs(mp.asinh(1) - mp.pi / 4)
    sep_ok = sep > mp.mpf('0.09')
    check("A4.3 THE GAP IS THE INVERSE GUDERMANNIAN OF THE SILVER-"
          "MIDPOINT ANGLE [exact]: DeltaK = arcsinh(1) = ln tan(pi/8 + "
          "pi/4) = gd^{-1}(pi/4) (%s) -- the rapidity whose Gudermann "
          "angle is pi/4 = half the quarter-turn euclidean angle = the "
          "silver-midpoint axis angle (A1.5): the Wick bridge circle-"
          "angle <-> rapidity evaluated at the mu4 half-angle; it is "
          "NOT the naive continuum NS mode gap theta r = pi/4 (lowest "
          "NS momentum r = 1/2 under the quarter turn theta = pi/2): "
          "|arcsinh(1) - pi/4| = %s > 0.09 (%s) -- consistent with "
          "A2.5: the gap is lattice data, its closed form lives in the "
          "half-angle geometry, not in a continuum mode sum"
          % (gd_ok, mp.nstr(sep, 6), sep_ok), gd_ok and sep_ok)


# ---------------------------------------------------------------------------
# Part B -- preregistered readout census
# ---------------------------------------------------------------------------
def load_targets():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, '..', '..', 'verification',
                        'predictions_frozen.json')
    with open(path) as fh:
        reg = json.load(fh)
    primary = [(e['id'], mp.mpf(e['frozen_value']))
               for e in reg['predictions']]
    c3 = 1 / (8 * mp.pi)
    phi0 = 1 / (6 * mp.pi) + 48 * c3 ** 4
    lamC = mp.sqrt(phi0 * (1 - phi0))
    secondary = [('PHI0', phi0), ('LAMBDA_C_SEED', lamC),
                 ('V124_RATE1', 6 * mp.log(mp.mpf(3) / 2)),
                 ('V124_RATE2', 6 * mp.log(3))]
    return primary, secondary


def class_values(base):
    """the frozen class: (p/q) * n * b * c3^f (base = 6-element b-set)."""
    c3 = 1 / (8 * mp.pi)
    rats = [mp.mpf(p) / q for p in range(1, 13) for q in range(1, 13)
            if gcd(p, q) == 1]
    ns = [mp.mpf(1), mp.mpf(4), mp.mpf(8), mp.mpf(16),
          mp.mpf(1) / 4, mp.mpf(1) / 8, mp.mpf(1) / 16]
    fs = [mp.mpf(1), c3, c3 ** 2]
    vals = []
    for r in rats:
        for n in ns:
            for b in base:
                for f in fs:
                    vals.append(r * n * b * f)
    return len(rats), vals


def census(vals_sorted, targets, tiers):
    """hit counts per tier + nearest relative distance per target."""
    counts = {t: 0 for t in tiers}
    nearest = []
    for tid, t in targets:
        lo_all = bisect_left(vals_sorted, t * (1 - max(tiers)))
        hi_all = bisect_right(vals_sorted, t * (1 + max(tiers)))
        best = None
        for tier in tiers:
            lo = bisect_left(vals_sorted, t * (1 - tier))
            hi = bisect_right(vals_sorted, t * (1 + tier))
            counts[tier] += hi - lo
        i = bisect_left(vals_sorted, t)
        cands = [vals_sorted[j] for j in (i - 1, i, i + 1)
                 if 0 <= j < len(vals_sorted)]
        if cands:
            best = min(abs(v / t - 1) for v in cands)
        nearest.append((tid, best))
        _ = (lo_all, hi_all)
    return counts, nearest


def null_expectation(vals_sorted, targets, tiers):
    """analytic local-density null: E = sum_t D_t * 2 eps."""
    ln2 = mp.log(2)
    out = {t: mp.mpf(0) for t in tiers}
    for _, t in targets:
        lo = bisect_left(vals_sorted, t / 2)
        hi = bisect_right(vals_sorted, t * 2)
        dens = (hi - lo) / (2 * ln2)
        for tier in tiers:
            out[tier] += dens * 2 * tier
    return out


def b_census():
    print("  -- B: preregistered silver-relation census on the frozen "
          "registry")
    primary, secondary = load_targets()
    dS = mp.mpf(1) + mp.sqrt(2)
    gold = (1 + mp.sqrt(5)) / 2
    disc = mp.sqrt(mp.mpf(23) / 108)
    plast = mp.cbrt(mp.mpf(1) / 2 + disc) + mp.cbrt(mp.mpf(1) / 2 - disc)

    def base6(x):
        return [x, x ** 2, 1 / x, 1 / x ** 2, mp.log(x), 1 / mp.log(x)]

    tiers = [mp.mpf('1e-30'), mp.mpf('1e-6'), mp.mpf('1e-3')]
    T1, T2, T3 = tiers
    n_rat, vals_s = class_values(base6(dS))
    _, vals_g = class_values(base6(gold))
    _, vals_p = class_values(base6(plast))
    for v in (vals_s, vals_g, vals_p):
        v.sort()
    n_raw = len(vals_s)
    n_distinct = len({mp.nstr(v, 32) for v in vals_s})

    # fairness: the declared generators reconstruct inside the class
    fair = all(any(abs(v - w) < mp.mpf('1e-35') for v in vals_s)
               for w in (dS, dS ** 2, 1 / dS, 1 / dS ** 2, mp.log(dS),
                         4 * dS, 16 / dS ** 2,
                         mp.log(dS) / (8 * mp.pi) ** 2 * 64))
    ok_inv = (len(primary) == 16 and abs(plast ** 3 - plast - 1)
              < mp.mpf('1e-35'))
    check("B.1 INVENTORY + CLASS [frozen]: 16 primary targets loaded "
          "from predictions_frozen.json (read-only), 4 secondary "
          "(phi0, lambda_C, v124 rates); class = %d coprime rationals "
          "x 7 (mu4/N powers) x 6 (delta_S branch) x 3 (c3 powers) = "
          "%d candidates (%d distinct values); plastic root certified "
          "(rho^3 - rho - 1 = 0 at 40 digits: %s); fairness: all "
          "declared generators reconstruct inside the class (%s)"
          % (n_rat, n_raw, n_distinct, ok_inv, fair),
          ok_inv and fair and n_raw == n_rat * 7 * 6 * 3)

    cs, near_s = census(vals_s, primary, tiers)
    cg, _ = census(vals_g, primary, tiers)
    cp, _ = census(vals_p, primary, tiers)
    E = null_expectation(vals_s, primary, tiers)
    print("      silver  T1/T2/T3 = %d/%d/%d   (null E: %s/%s/%s)"
          % (cs[T1], cs[T2], cs[T3], mp.nstr(E[T1], 3),
             mp.nstr(E[T2], 3), mp.nstr(E[T3], 3)))
    print("      golden  T1/T2/T3 = %d/%d/%d ; plastic T1/T2/T3 = "
          "%d/%d/%d" % (cg[T1], cg[T2], cg[T3], cp[T1], cp[T2], cp[T3]))
    for tid, d in near_s:
        print("        nearest silver-class candidate to %-18s : "
              "rel dist %s" % (tid, "n/a" if d is None else
                               mp.nstr(d, 4)))

    check("B.2 SILVER CENSUS RECORDED [frozen tiers]: exact tier T1 "
          "(1e-30) = %d, tight tier T2 (1e-6) = %d, calibration tier "
          "T3 (1e-3) = %d over 16 frozen targets x %d candidates -- "
          "every T1 hit would require closed-form verification; none "
          "to verify iff T1 = 0 (observed: %s)"
          % (cs[T1], cs[T2], cs[T3], n_raw, cs[T1] == 0), True)

    plc_ok = (cg[T3] + cp[T3]) >= cs[T3] // 2
    check("B.3 PLACEBO CONTROLS [same class, same targets]: golden "
          "T3 = %d and plastic T3 = %d vs silver T3 = %d -- the "
          "placebos deliver comparable chance hits (%s): the class is "
          "calibrated, not silver-tuned; placebo T2 = %d/%d vs silver "
          "T2 = %d" % (cg[T3], cp[T3], cs[T3], plc_ok, cg[T2],
                       cp[T2], cs[T2]), plc_ok)

    cal_ok = True
    for tag, c in (('silver', cs), ('golden', cg), ('plastic', cp)):
        if E[T3] >= 3 and not (E[T3] / 5 <= c[T3] <= E[T3] * 5):
            cal_ok = False
    check("B.4 NULL CALIBRATION [analytic density]: expected T3 hits "
          "under the log-local-density null = %s; observed %d "
          "(silver), %d (golden), %d (plastic) -- all within the "
          "declared factor 5 (%s); expected T2 = %s: any T2 hit is "
          "individually interesting, none is expected by chance"
          % (mp.nstr(E[T3], 4), cs[T3], cg[T3], cp[T3], cal_ok,
             mp.nstr(E[T2], 3)), cal_ok)

    cs2, near2 = census(vals_s, secondary, tiers)
    for tid, d in near2:
        print("        nearest silver-class candidate to %-18s : "
              "rel dist %s" % (tid, "n/a" if d is None else
                               mp.nstr(d, 4)))
    check("B.5 SECONDARY TARGETS (phi0, lambda_C, v124 clock rates "
          "6 ln(3/2), 6 ln 3) [recorded separately]: T1 = %d, T2 = %d, "
          "T3 = %d -- the silver/arcsinh(1) family does not land on "
          "the resummed-clock chain either (closest approach printed "
          "above)" % (cs2[T1], cs2[T2], cs2[T3]), True)

    # frozen verdict logic [B-5]
    t1_verified = 0        # no T1 hits -> nothing to verify
    if cs[T1] > 0:
        t1_verified = -1   # would require closed-form work: flag only
    if cs[T1] > 0 and t1_verified > 0:
        verdict = "ERFOLG-ANSCHLUSS"
    elif cs[T1] == 0 and cs[T2] >= 3 and \
            cs[T2] >= 3 * max(cg[T2], cp[T2], 1):
        verdict = "UNENTSCHIEDEN"
    else:
        verdict = "KILL"
    consistent = (verdict == "KILL") == (cs[T1] == 0 and not
                                         (cs[T2] >= 3 and cs[T2] >= 3 *
                                          max(cg[T2], cp[T2], 1)))
    check("B.6 VERDICT-CONNECTION PER FROZEN [B-5] LOGIC = %s "
          "[assembled]: T1 = %d (verified exact: %d), T2 silver/golden/"
          "plastic = %d/%d/%d, null E_T2 = %s -- the decision follows "
          "the preregistered branch exactly (consistency: %s)"
          % (verdict, cs[T1], max(t1_verified, 0), cs[T2], cg[T2],
             cp[T2], mp.nstr(E[T2], 3), consistent), consistent)
    return verdict


# ---------------------------------------------------------------------------
def run():
    print("seam_clock_silver_spectrum_probe -- origin and readout-"
          "connection of the silver clock spectrum (EXPLORATION ONLY)")
    a1_1_hankel()
    a1_2_dirichlet()
    a1_3_n8_odd()
    a1_4_even_and_secondquant()
    a1_5_geometry()
    a1_6_v512()
    a2_mod8(12, 1)
    a2_mod8(20, 2)
    a2_3_n16_membership()
    a2_4_n24_membership()
    a2_5_scan()
    a2_6_n6()
    a2_7_n10()
    a4_1_gap()
    a4_2_kms()
    a4_3_gudermann()
    n_a = len(RESULTS)
    verdict_structure = "SUCCESS" if all(RESULTS) else "UNDECIDED"
    verdict_connection = b_census()
    npass = sum(RESULTS)
    print("\n%d/%d checks passed  (runtime %.1f s)"
          % (npass, len(RESULTS), time.perf_counter() - T0_WALL))
    if not all(RESULTS[:n_a]):
        verdict_structure = "UNDECIDED"
    print("VERDICT-STRUCTURE : %s  (closed-form origin of {1, "
          "sqrt(2)-1})" % verdict_structure)
    print("VERDICT-CONNECTION: %s  (frozen-registry readout census)"
          % verdict_connection)
    return npass == len(RESULTS)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
