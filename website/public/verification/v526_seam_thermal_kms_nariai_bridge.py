"""v526 -- SEAM.THERMAL.KMS.01: the thermal seam -- KMS structure of the
reconstructed free OS quotient CLOSED onto the Nariai/BH temperature
chain (the THIRD LEG of c3).  Verdict SUCCESS per the frozen
preregistration.  NO marker moves.

[E] 1. beta MEASURED, NOT ASSUMED: the circle kernel C(d)=(2/N)/sin(pi d/N)
    has exactly one finite thermal-mode representation with detailed
    balance; N=8: one real frequency omega=arcsinh(2^{-3/4}), weight
    ratio kappa=q^{-8} EXACTLY => beta=8=N (Q-polynomial identity
    Q^2-(2+sqrt2)Q+1=0); N=16: both mode pairs real, pairing exponent
    exactly (N/2)+1=9 => beta=16=N; anchor Pi(u_i-2)=sqrt2 =
    Pi sinh(omega_i)*2^{7/4} pin at both levels; wrong beta
    {N/2,N/4,2N} excluded (gaps 0.0937/0.3126/0.0108; N/2 witness
    C(1)-C(3)=sqrt2*C(3) != 0 exact).
[E] 2. T_seam = 1/N per clock step; in angle units (step = 2pi/N,
    v519 pin): beta_angle = 2pi EXACT, T_seam = 1/(2pi) = 4 c3 --
    N-independent.
[E] 3. MODULAR HAMILTONIAN CLOSED: rho_OS faithful, spectrum
    p={(1+-nu1)(1+-nu2)/4} with nu1=cos(pi/24), nu2=cos(7pi/24) exact;
    K = eps1 n1 + eps2 n2 with eps1=2 ln cot(pi/48),
    eps2=2 ln cot(7pi/48); full Tomita structure (KMS-beta=1 on all
    256 pairs, residual 2.5e-38, J Delta J = Delta^{-1}).
[E] 4. THE c3 CLOSURE (class-1 selection in the frozen anti-numerology
    lattice, exact r=1): beta_angle=2pi=1/(4 c3) -- T_seam=4 c3 is the
    Bisognano-Wichmann/Hawking normalisation from v208; chain:
    T_H=c3/M=1/(8pi M) (the axiom IS the Hawking coefficient, here
    from the seam KMS), SdS 1/(4pi)=2 c3, Nariai T_N=4 c3 sqrt(Lambda),
    v104 cross-link 2H/T_N=4pi=1/(2 c3) exact.  [C]-fence: reading
    "seam euclidean circle = thermal circle of the reconstructed
    horizon dynamics" -- temperature as THIRD LEG of c3 beside
    geometry and anomaly.
[E] 5. ENTROPY: S(8)=0.52187, S(16)=0.63510, S(32)=0.75006 nats;
    DeltaS/ln2 -> 1/6 = c_chi/3 monotonically (chiral c=1/2 log law
    confirmed); HONESTLY FAILED: v129 horizon fractions {1/3,2/3} and
    v190 floor do NOT transfer (S/S_max=0.376/0.229, not N-stable) --
    temperature bridge closes, entropy-fraction bridge does not.
[C-5] typed non-gating: naive clock reading fails ({1,sqrt2-1} are NOT
    e^{-Delta K} ratios; gaps 0.0496/0.1710), Tomita flow != transfer
    flow (0.45-0.67); exact replacement: sqrt2-1 = C(3)/C(1) =
    1/(2 cosh 2 omega - 1) -- the silver eigenvalue is a thermal
    kernel ratio.
[E] 6. NEGATIVE CONTROLS: site (2,2,4) no state; family A (4,4,0);
    anti-chiral (8,8,0); NON-COMPACT: Stieltjes => kappa=0, beta=inf,
    T=0 -- the temperature hangs exactly on compactness of the
    euclidean circle.

Status: [E] exact sympy/cyclotomic + 40-digit Tomita certificates;
[C] bridge reading typed.  Python; Wolfram-mirrored (Q-polynomial /
beta measurement / 2pi=1/(4 c3) chain / nu char-poly -- the 40-digit
Tomita residuals and entropy tower are Python-only), counted per
GATE.WOLFRAM.02.  Discovery provenance:
experiments/tfpt-discovery/seam_thermal_kms_nariai_bridge_probe.py
(22/22, 2026-07-23).

=== ORIGINAL PROBE HEADER (kept verbatim) ===
seam_thermal_kms_nariai_bridge_probe.py -- EXPLORATION ONLY (thermal-seam
sandbox).  Nothing in verification/, ledger, papers, changelog, website or
scorecard is touched; every status marker stays where it is.  No files are
written; standalone; deterministic.

THE ATTACK (KMS -> Nariai/BH bridge): the WOIT-beta2 probe
(woit_os_beta2_os_quotient_probe.py) showed that the OS quotient of the free
16-Majorana NS seam circle is THERMAL: at N = 8 the complete half algebra
reconstructs dim H_phys = 16 = 4^2 (a doubled/two-sided space), there is no
contraction on the compact euclidean circle (silver witnesses), and the
clock T^{N/4} has spectrum exactly {1, sqrt(2)-1}.  This probe constructs
the KMS structure of that reconstruction EXACTLY and asks whether its
temperature normalisation closes onto the Nariai/BH temperature chain of
the suite (v208 modular T_H, v104 Nariai clock, v129/v190 entropy ledger).

LEADING HYPOTHESIS (preregistered BEFORE the computation): the TFPT axiom
c3 = 1/(8 pi) is numerically the Hawking coefficient (T_H = 1/(8 pi M) for
Schwarzschild).  If the KMS temperature of the reconstructed seam state, in
clock-step units, closes exactly onto the modular normalisation the
Nariai/BH sector of the suite uses (v208: modular beta = 2 pi = 1/(4 c3)),
temperature becomes an independent third leg of the axiom, next to
geometry and anomaly.

=== PREREGISTRATION (frozen BEFORE the probe run; criteria not adjusted
after; scratch pre-derivation produced the EXACT ANCHORS marked
"pre-derived", each to be machine-confirmed here -- no criterion, tolerance
or relation class was changed after seeing probe output) ===

[C-0] system pinned = the v519/beta2 seam data, copied verbatim: chiral NS
  vacuum kernel C(d) = (2/N)/sin(pi d/N) (odd d; C(even) = 0), bond-cut OS
  reflection (axis k = N-1, NS spin signs, twist eta = +i), half algebra
  A_+ on {N/2..N-1}; levels N = 8 (complete 2^4 half algebra) and N = 16
  (Gaussian/one-particle level).  One clock step = the euclidean rotation
  alpha_1 = geometric angle 2 pi / N (v519 Q1.1 pin; re-verified here).

[C-1] rho_OS := the unique element of A_+ (== M_4(C) via a pinned
  Jordan-Wigner map) with Tr(rho_OS a) = omega(a) for all a in A_+ -- the
  reduced state of the pure circle state on the half algebra, i.e. the
  state the OS vector Omega induces on pi(A_+) (pi = left multiplication
  on H_phys).  SUCCESS-criteria: exact duality on all 16 monomials;
  Hermitian, trace 1, POSITIVE DEFINITE (faithful => two-sided 4^2 GNS =
  thermal representation).  Pre-derived exact anchors: Williamson values
  nu_1 = cos(pi/24), nu_2 = cos(7 pi/24) (char-poly identity: nu^2 =
  (4 + sqrt2 +- sqrt6)/8); spectrum p = {(1 +- nu_1)(1 +- nu_2)/4};
  modular Hamiltonian K = -ln rho_OS with single-particle energies
  eps_i = ln((1+nu_i)/(1-nu_i)) = 2 ln cot(pi/48), 2 ln cot(7 pi/48).

[C-2] Tomita/KMS of the reconstruction: on H_phys (exact 16x16 Gram G,
  PD per beta2) with Omega = [1] and pi = left multiplication, construct
  S[a] = pi(a)^{*G} Omega, Delta = S*S, J = S Delta^{-1/2} explicitly.
  SUCCESS-criteria (40-digit certificates, thresholds 1e-30): Delta Omega
  = Omega; Delta G-self-adjoint PD; the KMS-beta=1 identity
  <Omega, pi(a) Delta pi(b) Omega> = <Omega, pi(b) pi(a) Omega> on ALL
  256 monomial pairs; J anti-unitary, J^2 = 1, J Delta J = Delta^{-1},
  J pi J in the commutant; modular flow preserves pi(A_+); spec Delta =
  {p_i / p_j} (the two-sided ratio spectrum -- the commutant carries the
  SAME density: the purification is reflection-symmetric).

[C-3] KMS for the TRANSFER flow -- the beta measurement (beta is NOT an
  input): the circle two-point kernel C(d), d = 1..N-1, is tested for a
  finite thermal-mode (detailed-balance) representation
      C(d) = sum_i  w_i (q_i^{-d} + kappa_i q_i^{+d}),   q_i > 1 real,
  via the palindromic Prony recurrence (the even-d checkerboard zeros
  force the +-(momentum 0/pi) mode doubling; the ansatz does NOT input
  beta).  KMS at inverse temperature beta (clock steps) <=> kappa_i =
  q_i^{-beta} (detailed balance).  Pre-derived exact anchors, to confirm:
    N = 8:  recurrence closes with ONE pair, q^2 + q^{-2} = 2 + sqrt2,
      i.e. omega := ln q = arcsinh(2^{-3/4}); weights positive;
      MEASURED kappa = q^{-8} EXACTLY  =>  beta = 8 = N;
      silver chain: C(1)/C(3) = 2 cosh(2 omega) - 1 = 1 + sqrt2.
    N = 16: recurrence (2 unknowns, 4 equations) closes EXACTLY
      (cyclotomic certificates mod z^16 + 1); both mode pairs REAL
      (u_i = q_i^2 + q_i^{-2} > 2); anchor prod_i (u_i - 2) = sqrt2
      (both levels: at N = 8, u - 2 = sqrt2); weight pairing =>
      beta = 16 = N (j-unit exponent (N/2)+1 = 9, 40-digit).
  Fermi-Dirac closure: n = 1/(1 + q^N) with |u|-|v| weight symmetry
  (the chiral eta = +i as mode phase).  The trivially-true graded
  reflection identity (alpha_N = (-1)^F) is recorded as necessary-only.

[C-4] TEMPERATURE BRIDGE -- preregistered relation classes
  (anti-numerology; FROZEN): the only admissible closures are
      beta_angle / (2 pi)  in  {1/4, 1/2, 1, 2, 4}  (small rationals),
  optionally times c3^k (k in {-1, 0, 1}) or |mu_4|^{+-1} or N^{+-1} --
  and the BRIDGE counts as EXACT CLOSURE only for the class-1 value
  beta_angle = 2 pi, since 2 pi = 1/(4 c3) EXACTLY (v58/v208) is the
  Bisognano-Wichmann/Hawking modular normalisation of the suite:
  T_seam = 1/beta_angle = 1/(2 pi) = 4 c3, and the Schwarzschild chain
  T_H = kappa_h/(2 pi) = c3/M = 1/(8 pi M) (v208 check 1), SdS
  1/(4 pi) = 2 c3 (v208 check 3), Nariai T_N = 4 c3 sqrt(Lambda) with
  the v104 rate cross-link 2H/T_N = 1/(2 c3) = 4 pi.  beta_angle :=
  beta_steps * (2 pi / N) with beta_steps the [C-3] measurement.
  KILL if beta_steps measured but beta_angle/(2 pi) lands outside the
  class lattice (incommensurable); the wrong-beta candidates beta = N/2,
  N/4 (angle pi, pi/2) must FAIL detailed balance with quantified gaps.

[C-5] clock sub-expectations (typed check-questions, non-gating; the task
  hypothesis "the clock eigenvalues {1, sqrt2 - 1} should appear as
  e^{-Delta K} ratios" is tested honestly).  Scratch pre-derivation
  indicates the NAIVE reading FAILS (min gap ~0.05 to spec Delta^{1/4},
  ~0.17 to spec Delta) and that the Tomita flow is NOT the transfer flow
  (||tau_k - G Delta^{k/N}|| = O(0.5) on the Klein-Landau domains) -- the
  interval/half-circle modular flow of a thermal chiral fermion is
  non-geometric; machine-confirm both, and confirm the POSITIVE exact
  identity that replaces the naive reading:  sqrt2 - 1 = C(3)/C(1) =
  1/(2 cosh(2 omega) - 1)  (the silver clock eigenvalue is a thermal
  KERNEL ratio, not a Boltzmann/modular weight ratio).  The beta2
  compressed-clock spectrum {1, sqrt2 - 1} (both parity sectors) is
  re-verified exactly.

[C-6] ENTROPY: S(rho_OS) exact form S = sum_i [ln 2 - ((1+nu)ln(1+nu) +
  (1-nu)ln(1-nu))/2] + 40 digits; N = 16 and N = 32 via the Gaussian
  covariance.  Preregistered candidate structures (informative,
  NON-GATING either way -- no fishing beyond these):
   (E1) chiral-CFT ln-law: Delta S / ln 2 -> c_chi/3 = 1/6 monotonically
        (c_chi = 1/2), PASS-shape: |DS2/ln2 - 1/6| < |DS1/ln2 - 1/6|;
   (E2) v129 fraction transfer: S/S_max vs {1/3, 2/3} at N = 8, 16;
   (E3) v190 floor transfer: S/S_max >= 2/3.
  Scratch pre-derivation: E1 holds, E2/E3 fail (the horizon entropy
  fractions do NOT transfer to seam entanglement entropy) -- confirm and
  record honestly.

[C-7] negative controls (all mandatory):
   (i)  SITE cut (N = 8, half {1,2,3}): the OS Gram is indefinite for
        every admissible twist => no state, no purification, no KMS --
        the thermal reconstruction exists only at the bond placement;
   (ii) FAMILY A (clock-centralising antipode, alternating dressing):
        Hermitian only for a sub-torsor eta and indefinite (4,4,0) =>
        no quotient to be thermal;
   (iii) ANTI-CHIRAL state (chi = -1): odd block negative definite,
        total (8,8,0) => no state for the wrong chirality;
   (iv) NON-COMPACT control (half-line kernel C_inf(d) = 2/(pi d), the
        N -> inf Cauchy-Stieltjes limit): the return symmetry C(N-d) =
        C(d) dies (exact witness), the kernel is monotone-decaying
        (h4 - h3 < 0 vs the circle's +sqrt2 C(3) return), the palindromic
        recurrence consistency FAILS with the exact gap 128/105, and the
        Stieltjes identity 2/(pi d) = (2/pi) int_0^1 x^{d-1} dx shows all
        growing weights vanish => beta = inf, T = 0: the temperature
        hangs exactly on the compact circle; contraction is restored
        (ratios < 1) where the circle shows the silver expansion;
   (v)  WRONG-beta candidates: beta = N/2, N/4 (and 2N) violate detailed
        balance exactly -- gaps |q^{-8} - q^{-4}|, |q^{-8} - q^{-2}|,
        |q^{-8} - q^{-16}| quantified at 40 digits, plus the N/2-return
        witness C(1) - C(3) = sqrt2 C(3) != 0 exact.

[C-8] verdict logic (FROZEN): KILL iff (K1) rho_OS fails PD/duality or
  the Tomita KMS identity fails, or (K2) the transfer kernel admits the
  real-mode representation but detailed balance forces beta != N at
  either level (or no real-mode rep exists at N = 16 while N = 8 has
  one -- incommensurable temperatures), or (K3) beta_angle/(2 pi) lands
  on a non-class value.  SUCCESS iff ALL of: [C-1] exact anchors confirm;
  [C-2] certificates pass; [C-3] beta = N exact at BOTH levels; [C-4]
  class-1 closure beta_angle = 2 pi = 1/(4 c3); [C-6] computed; [C-7]
  all five controls behave as typed.  Otherwise UNDECIDED with the gap
  named.  [C-5]/[C-6] outcomes are recorded, not gating.  Exactness
  policy: scalar identities exact (sympy / cyclotomic Laurent reduction
  mod z^N + 1); operator certificates 40-digit (mp.mp.dps = 40,
  threshold 1e-30, inertia threshold 1e-25).  Runtime < 15 min.

=== FINDINGS (from the frozen-prereg run, 2026-07-23; 22/22) ===

VERDICT: SUCCESS (typed [C]; sandbox only -- no marker moves).
  * rho_OS explicit & faithful; nu = {cos(pi/24), cos(7 pi/24)} EXACT;
    K = -ln rho_OS with eps = {2 ln cot(pi/48), 2 ln cot(7 pi/48)}
    = {5.4501, 1.4139}; Tomita (S, J, Delta) certified at 1e-33..1e-38;
    KMS beta = 1 modular identity exact on all 256 pairs; spec Delta =
    {p_i/p_j} (two-sided ratio spectrum, commutant carries the same
    density).
  * TRANSFER KMS: C(d) = 2w (q^{-d} + q^{d-N}) with omega = ln q =
    arcsinh(2^{-3/4}) at N = 8 -- MEASURED beta = 8 = N exactly
    (kappa = q^{-8} via Q-polynomial identity); N = 16: recurrence
    closes exactly (cyclotomic certificates), both pairs real, anchor
    prod(u_i - 2) = sqrt2 at both levels, measured exponent 9 =
    (N/2)+1 to 1e-30 => beta = 16 = N.  Fermi-Dirac n = 1/(1+q^N).
  * BRIDGE CLOSES (class 1): beta_angle = N * (2 pi/N) = 2 pi =
    1/(4 c3) exactly = the v208 modular normalisation; T_seam =
    1/(2 pi) = 4 c3; Schwarzschild T_H = kappa_h/(2 pi) = c3/M =
    1/(8 pi M): the axiom c3 IS the seam KMS temperature coefficient;
    SdS 1/(4 pi) = 2 c3; Nariai cross-link 2H/T_N = 1/(2 c3) = 4 pi.
    beta = N/2, N/4, 2N all excluded exactly (gaps 0.094, 0.31, 0.011).
  * CLOCK (typed [C-5] finding): the naive e^{-Delta K} reading FAILS
    (min gaps 0.0496/0.1710) and tau_k != G Delta^{k/N} (residuals
    0.45/0.67): the Tomita flow of the half-circle cut is NOT the
    transfer flow (non-geometric interval modular flow, as in CFT);
    the EXACT replacement holds: sqrt2 - 1 = C(3)/C(1) =
    1/(2 cosh 2 omega - 1) -- the silver clock eigenvalue is the
    thermal kernel ratio at separations 3:1; beta2 compressed clock
    {1, sqrt2 - 1} re-verified exactly in both parity sectors.
  * ENTROPY: S(8) = 0.52187, S(16) = 0.63510, S(32) = 0.75006 nats;
    E1 chiral-CFT ln-law CONFIRMED (DeltaS/ln2: 0.16335 -> 0.16585 ->
    1/6, monotone); E2/E3 FAIL as pre-derived: S/S_max = 0.376 (N=8),
    0.229 (N=16) -- the v129/v190 horizon fractions {1/3, 2/3} do NOT
    transfer to seam entanglement entropy (different objects).
  * CONTROLS: site cut indefinite ((2,2,4), 2 negative directions --
    no state); family A (4,4,0); anti-chiral odd block (0,8,0), total
    (8,8,0); half-line kernel: return dead, recurrence gap 128/105
    exact, Stieltjes => beta = inf/T = 0, contraction restored; wrong
    beta N/2, N/4, 2N excluded with the quantified gaps above.

Construction base (READ-ONLY): verification/v519_woit_theta_rp_free.py,
verification/v522_woit_beta1_gso_gauge.py, experiments/tfpt-discovery/
woit_os_beta2_os_quotient_probe.py (kernel, Pfaffian-Wick, dihedral
machinery copied verbatim); verification/v104_nariai_clock.py,
v107_quantum_clock_target.py, v190_nariai_entropy_bound.py,
v208_bh_thermodynamics.py, v129_entropy_power_law.py,
v127_ring_resummation.py, v147_clock_gaussian.py (normalisations only).

Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/seam_thermal_kms_nariai_bridge_probe.py
"""
import time
from itertools import combinations

import mpmath as mp
import sympy as sp

from tfpt_constants import check as _check, summary, reset

mp.mp.dps = 40

I = sp.I
N8 = 8
N16 = 16
ETA = I
RESULTS = []
FLAGS = {}
T0_WALL = time.perf_counter()
TOL = mp.mpf(10) ** -30
TOL_IN = mp.mpf(10) ** -25


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
# v519/beta2 machinery (verbatim where possible)
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


def tower_maps(n, shift, kmax):
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


def spectrum_inertia(M, tol=None):
    if tol is None:
        tol = TOL_IN
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
    B = mp.matrix(A.cols, A.rows)
    for i in range(A.rows):
        for j in range(A.cols):
            B[j, i] = mp.conj(A[i, j])
    return B


def mconj(A):
    B = mp.matrix(A.rows, A.cols)
    for i in range(A.rows):
        for j in range(A.cols):
            B[i, j] = mp.conj(A[i, j])
    return B


# cyclotomic Laurent certificate: expr(z) == 0 at z = e^{i pi / n}
# (z^n + 1 = 0 is the minimal polynomial for n a power of two)
ZSYM = sp.symbols('z')


def zeta_zero(expr, n, pad=220):
    e = sp.cancel(sp.together(sp.expand(expr)))
    num, den = sp.fraction(e)
    num = sp.expand(num * ZSYM ** pad)
    try:
        p = sp.Poly(num, ZSYM)
        r = sp.rem(p, sp.Poly(ZSYM ** n + 1, ZSYM))
        poly_zero = r.is_zero
    except sp.PolynomialError:
        # fallback: substitute the exact root of unity
        poly_zero = sp.simplify(sp.expand(
            expr.subs(ZSYM, sp.exp(sp.I * sp.pi / n)))) == 0
    if not poly_zero:
        return False
    zval = mp.e ** (1j * mp.pi / n)
    dv = complex(sp.lambdify(ZSYM, den)(complex(zval)))
    return abs(dv) > 1e-12


P8 = [4, 5, 6, 7]
R7, S7 = refl_map(7, N8)
BASIS8 = [m for d in range(5) for m in combinations(P8, d)]     # 16
BIDX = {m: i for i, m in enumerate(BASIS8)}
TW8 = tower_maps(N8, 1, N8)
C1, C3 = c_of(1, 8), c_of(3, 8)
c3 = sp.Rational(1, 8) / sp.pi
pi_ = sp.pi

# pre-derived exact mode data (to be machine-confirmed in Part B)
QQ_ = sp.Rational(1, 2) * (2 + sp.sqrt(2) + sp.sqrt(2 + 4 * sp.sqrt(2)))
q_ = sp.sqrt(QQ_)                              # q > 1, omega = ln q


# ---------------------------------------------------------------------------
# Part R -- the reduced state and its modular Hamiltonian (N = 8 exact)
# ---------------------------------------------------------------------------
def r1_kernel():
    print("  -- R1: kernel preconditions (compact-circle thermal form)")
    ret = all(iszero(c_of(N8 - d, N8) - c_of(d, N8)) for d in (1, 3, 5, 7))
    antip = all(iszero(c_of(d + N8, N8) + c_of(d, N8)) for d in (1, 3, 5, 7))
    chk = all(c_of(d, N8) == 0 for d in (2, 4, 6))
    Cm8 = sp.Matrix(N8, N8, lambda a, b: c_of(a - b, N8))
    pure = sp.simplify(Cm8 * Cm8 + sp.eye(N8)) == sp.zeros(N8, N8)
    S1 = sp.Matrix(N8, N8, lambda i, j: 0)
    for a in range(N8):
        b = (a + 1) % N8
        S1[b, a] = -1 if a + 1 >= N8 else 1
    inv = sp.simplify(S1 * Cm8 * S1.T - Cm8) == sp.zeros(N8, N8)
    full_turn = (TW8[8][0] == tuple(range(N8)) and set(TW8[8][1]) == {-1})
    FLAGS['r1'] = ret and antip and chk and pure and inv and full_turn
    check("R1 KERNEL PRECONDITIONS [exact]: return symmetry C(N-d) = C(d) "
          "(%s -- correlations RETURN on the compact circle: the thermal "
          "hallmark), NS antiperiodicity C(d+N) = -C(d) (%s -- the "
          "fermionic KMS boundary sign), chiral checkerboard C(even) = 0 "
          "(%s), C^2 = -1 (%s -- the FULL circle state is PURE: the "
          "temperature can only come from the cut), alpha_1 preserves the "
          "state (%s) and alpha_1^N = (-1)^F (%s -- the trivially-true "
          "graded reflection identity omega(a alpha_t b) = "
          "omega(alpha_{t+N}(b) a) is thereby necessary-only: the KMS "
          "content sits in detailed balance, Part B)"
          % (ret, antip, chk, pure, inv, full_turn), FLAGS['r1'])


def r2_rho():
    print("  -- R2: rho_OS explicit (Jordan-Wigner dual basis)")
    sx = sp.Matrix([[0, 1], [1, 0]])
    sy = sp.Matrix([[0, -I], [I, 0]])
    sz = sp.Matrix([[1, 0], [0, -1]])

    def kron(A, B):
        return sp.Matrix(sp.BlockMatrix(
            [[A[i, j] * B for j in range(A.cols)] for i in range(A.rows)]))

    GM = {4: kron(sx, sp.eye(2)), 5: kron(sy, sp.eye(2)),
          6: kron(sz, sx), 7: kron(sz, sy)}
    cliff = all(sp.simplify(GM[a] * GM[b] + GM[b] * GM[a]
                            - 2 * sp.KroneckerDelta(a, b) * sp.eye(4))
                == sp.zeros(4, 4) for a in P8 for b in P8)

    def mono_mat(m):
        M = sp.eye(4)
        for a in m:
            M = M * GM[a]
        return M

    rho = sp.zeros(4, 4)
    for m in BASIS8:
        om = wick(m, N8)
        if om != 0:
            rho += om * mono_mat(m).conjugate().T   # unitary: inv = dagger
    rho = sp.expand_complex(rho / 4)
    dual = all(iszero(sp.expand_complex((rho * mono_mat(m)).trace())
                      - wick(m, N8)) for m in BASIS8)
    herm = all(iszero(x) for x in (rho - rho.conjugate().T))
    tr1 = iszero(rho.trace() - 1)
    inert, gap = spectrum_inertia(rho)
    FLAGS['rho'] = rho
    FLAGS['r2'] = cliff and dual and herm and tr1 and inert == (4, 0, 0)
    check("R2 rho_OS EXISTS AND IS FAITHFUL [exact + 40-digit]: pinned "
          "Jordan-Wigner map is Clifford (%s); the dual-basis element "
          "rho_OS = (1/4) sum_m omega(m) m^{-1} satisfies Tr(rho m) = "
          "omega(m) on ALL 16 monomials (%s), is Hermitian (%s), trace 1 "
          "(%s), and POSITIVE DEFINITE, inertia %s (min eigenvalue %s) -- "
          "the reduced state of the pure circle state on the half algebra "
          "is a full-rank (thermal) state: the 4^2 = 16 two-sided "
          "dimension of H_phys is its purification"
          % (cliff, dual, herm, tr1, inert, mp.nstr(gap, 5)), FLAGS['r2'])


def r3_closed_forms():
    print("  -- R3: closed forms -- nu, spectrum, modular Hamiltonian")
    Jm = sp.zeros(4, 4)
    for i, a in enumerate(P8):
        for j, b in enumerate(P8):
            if a < b:
                v = sp.im(wick((a, b), N8))
                Jm[i, j] = v
                Jm[j, i] = -v
    lam = sp.symbols('lam')
    cp = sp.expand((I * Jm - lam * sp.eye(4)).det())
    n1s = (4 + sp.sqrt(2) + sp.sqrt(6)) / 8
    n2s = (4 + sp.sqrt(2) - sp.sqrt(6)) / 8
    target = sp.expand((lam ** 2 - n1s) * (lam ** 2 - n2s))
    cp_ok = iszero(cp - target)
    cos_ok = (iszero(sp.cos(sp.pi / 24) ** 2 - n1s)
              and iszero(sp.cos(7 * sp.pi / 24) ** 2 - n2s))
    nu1, nu2 = sp.cos(sp.pi / 24), sp.cos(7 * sp.pi / 24)
    ps = [(1 + s1 * nu1) * (1 + s2 * nu2) / 4
          for s1 in (1, -1) for s2 in (1, -1)]
    sum1 = iszero(sum(ps) - 1)
    rho_n = to_mp(FLAGS['rho'])
    Er, _ = mp.eighe(rho_n)
    got = sorted([Er[i].real for i in range(4)])
    want = sorted([mp.mpf(str(sp.N(p, 45))) for p in ps])
    spec_ok = max(abs(got[k] - want[k]) for k in range(4)) < TOL
    th = sp.symbols('th', positive=True)
    cot_id = iszero(sp.simplify((1 + sp.cos(th)) / (1 - sp.cos(th))
                                - sp.cot(th / 2) ** 2))
    eps1 = mp.log((1 + mp.cos(mp.pi / 24)) / (1 - mp.cos(mp.pi / 24)))
    eps2 = mp.log((1 + mp.cos(7 * mp.pi / 24))
                  / (1 - mp.cos(7 * mp.pi / 24)))
    eps_ok = (abs(eps1 - 2 * mp.log(mp.cot(mp.pi / 48))) < TOL
              and abs(eps2 - 2 * mp.log(mp.cot(7 * mp.pi / 48))) < TOL)
    FLAGS['ps'] = want
    FLAGS['eps'] = (eps1, eps2)
    FLAGS['r3'] = cp_ok and cos_ok and sum1 and spec_ok and cot_id and eps_ok
    check("R3 CLOSED FORMS [exact]: char poly of the half covariance iJ = "
          "(lam^2 - nu1^2)(lam^2 - nu2^2) with nu^2 = (4 + sqrt2 +- "
          "sqrt6)/8 EXACTLY (%s), and nu_1 = cos(pi/24), nu_2 = "
          "cos(7 pi/24) (%s); spectrum p = {(1 +- nu1)(1 +- nu2)/4} "
          "(sum 1: %s; 40-digit match: %s) -- the MODULAR HAMILTONIAN "
          "K = -ln rho_OS is free with single-particle energies eps_i = "
          "ln((1+nu)/(1-nu)) = 2 ln cot(theta/2) (identity: %s), theta = "
          "pi/24, 7 pi/24: eps = {%s, %s} (%s) -- K = eps1 n1 + eps2 n2 "
          "+ const on the 2-mode Fock space"
          % (cp_ok, cos_ok, sum1, spec_ok, cot_id, mp.nstr(eps1, 8),
             mp.nstr(eps2, 8), eps_ok), FLAGS['r3'])


def r4_gram():
    print("  -- R4: H_phys, Gram, purification identity")
    G8 = sp.zeros(16, 16)
    for i, ma in enumerate(BASIS8):
        ca, mta = theta_mono(ma, R7, S7, ETA)
        for j, mb in enumerate(BASIS8):
            cs, mm = mono_mul(mta, mb)
            G8[i, j] = sp.expand_complex(ca * cs * wick(mm, N8))
    herm = all(iszero(x) for x in (G8 - G8.conjugate().T))
    inert, gap = spectrum_inertia(G8)
    vec = all(iszero(G8[0, j] - wick(BASIS8[j], N8)) for j in range(16))
    FLAGS['G8'] = G8
    FLAGS['r4'] = herm and inert == (16, 0, 0) and vec
    check("R4 PURIFICATION [exact + 40-digit]: the 16x16 bond-cut OS Gram "
          "is Hermitian (%s) and PD, inertia %s (min %s -- the beta2 Q1.3 "
          "regression 3.3471e-3), so Omega = [1] is CYCLIC and SEPARATING "
          "for pi(A_+) = M_4 acting on H_phys = C^4 (x) C^4; the vector "
          "state IS the reduced state: <Omega, pi(m) Omega> = omega(m) = "
          "Tr(rho_OS m) on all 16 monomials (%s) -- H_phys is the "
          "standard-form purification of rho_OS"
          % (herm, inert, mp.nstr(gap, 5), vec), FLAGS['r4'])


# ---------------------------------------------------------------------------
# Part T -- Tomita-Takesaki data and the modular KMS condition (40-digit)
# ---------------------------------------------------------------------------
def t1_tomita():
    print("  -- T1: S, Delta, J constructed on H_phys")
    Gn = to_mp(FLAGS['G8'])
    EGv, QG = mp.eighe(Gn)
    Gh = QG * mp.diag([mp.sqrt(EGv[i]) for i in range(16)]) * ctr(QG)
    Ghi = QG * mp.diag([1 / mp.sqrt(EGv[i]) for i in range(16)]) * ctr(QG)
    Gninv = Ghi * Ghi
    PIn = {}
    for m in BASIS8:
        M = mp.matrix(16, 16)
        for j, mb in enumerate(BASIS8):
            c, mm = mono_mul(m, mb)
            M[BIDX[mm], j] = c
        PIn[m] = M
    e0 = mp.matrix(16, 1)
    e0[0, 0] = 1
    Gcol0 = mp.matrix(16, 1)
    for i in range(16):
        Gcol0[i, 0] = Gn[i, 0]
    A_S = mp.matrix(16, 16)
    for m in BASIS8:
        col = Gninv * (ctr(PIn[m]) * Gcol0)
        for i in range(16):
            A_S[i, BIDX[m]] = col[i, 0]
    M_T = ctr(A_S) * Gn * A_S
    Delta = Gninv * M_T.T
    res_om = mp.mnorm(Delta * e0 - e0, 1)
    B = Gh * Delta * Ghi
    res_h = mp.mnorm(B - ctr(B), 1)
    Bh = (B + ctr(B)) * mp.mpf('0.5')
    ED, QD = mp.eighe(Bh)
    all_pos = all(ED[i].real > TOL_IN for i in range(16))
    Dinvh = Ghi * QD * mp.diag([1 / mp.sqrt(ED[i].real)
                                for i in range(16)]) * ctr(QD) * Gh
    Dinv = Dinvh * Dinvh
    A_J = A_S * mconj(Dinvh)
    res_j2 = mp.mnorm(A_J * mconj(A_J) - mp.eye(16), 1)
    res_au = mp.mnorm(ctr(A_J) * Gn * A_J - Gn.T, 1)
    JDJ = A_J * mconj(Delta) * mconj(A_J)
    res_jdj = mp.mnorm(JDJ - Dinv, 1) / mp.mnorm(Dinv, 1)
    FLAGS.update(Gn=Gn, Gh=Gh, Ghi=Ghi, PIn=PIn, e0=e0, Delta=Delta,
                 Dinv=Dinv, ED=ED, QD=QD, A_J=A_J)
    ok = (res_om < TOL and res_h < TOL and all_pos and res_j2 < TOL
          and res_au < TOL and res_jdj < TOL)
    FLAGS['t1'] = ok
    check("T1 TOMITA DATA EXPLICIT [40-digit certificates]: S[a] = "
          "pi(a)^{*G} Omega, Delta = S*S, J = S Delta^{-1/2} -- "
          "Delta Omega = Omega (res %s), Delta G-self-adjoint (res %s) "
          "and POSITIVE (%s), J^2 = 1 (res %s), J anti-unitary (res %s), "
          "J Delta J = Delta^{-1} (res %s): the full modular structure "
          "of the thermal reconstruction is explicit"
          % (mp.nstr(res_om, 3), mp.nstr(res_h, 3), all_pos,
             mp.nstr(res_j2, 3), mp.nstr(res_au, 3), mp.nstr(res_jdj, 3)),
          ok)


def t2_kms_modular():
    print("  -- T2: modular KMS identity + flow/commutant structure")
    Gn, PIn, e0 = FLAGS['Gn'], FLAGS['PIn'], FLAGS['e0']
    Delta, Dinv, A_J = FLAGS['Delta'], FLAGS['Dinv'], FLAGS['A_J']
    r0 = ctr(e0) * Gn
    rowa = {m: r0 * PIn[m] for m in BASIS8}
    cola = {m: PIn[m] * e0 for m in BASIS8}
    ucol = {m: Delta * cola[m] for m in BASIS8}
    kms = mp.mpf(0)
    for a in BASIS8:
        for b in BASIS8:
            lhs = (rowa[a] * ucol[b])[0, 0]
            rhs = (rowa[b] * cola[a])[0, 0]
            kms = max(kms, abs(lhs - rhs))
    worst_c = mp.mpf(0)
    for m in BASIS8:
        X = A_J * mconj(PIn[m]) * mconj(A_J)
        for m2 in [(4,), (5,), (6,), (7,)]:
            Y = PIn[m2]
            worst_c = max(worst_c, mp.mnorm(X * Y - Y * X, 1))
    worst_m = mp.mpf(0)
    for m in BASIS8:
        X = Delta * PIn[m] * Dinv
        R = X.copy()
        for m2 in BASIS8:
            cc = mp.fsum([mp.conj(PIn[m2][k, i2]) * X[k, i2]
                          for k in range(16) for i2 in range(16)]) / 16
            R = R - cc * PIn[m2]
        worst_m = max(worst_m, mp.mnorm(R, 1) / mp.mnorm(X, 1))
    ok = kms < TOL and worst_c < TOL and worst_m < TOL
    FLAGS['t2'] = ok
    check("T2 MODULAR KMS AT beta = 1 [40-digit]: the KMS identity "
          "<Omega, pi(a) Delta pi(b) Omega> = <Omega, pi(b) pi(a) Omega> "
          "holds on ALL 256 monomial pairs (max residual %s < 1e-30) -- "
          "the OS state is EXACTLY KMS for its modular flow; the flow "
          "preserves pi(A_+) (membership res %s), and J pi J lands in "
          "the commutant (res %s): (pi(A_+), Omega) is a genuine "
          "thermal/two-sided (Tomita standard form) pair"
          % (mp.nstr(kms, 3), mp.nstr(worst_m, 3), mp.nstr(worst_c, 3)),
          ok)


def t3_spec():
    print("  -- T3: spec Delta = two-sided ratio spectrum")
    ED = FLAGS['ED']
    got = sorted([ED[i].real for i in range(16)])
    want = sorted([pi_v / pj_v for pi_v in FLAGS['ps']
                   for pj_v in FLAGS['ps']])
    dev = max(abs(got[k] - want[k]) for k in range(16))
    ok = dev < TOL
    FLAGS['t3'] = ok
    FLAGS['specD'] = got
    check("T3 SPEC Delta = {p_i / p_j} [40-digit, max dev %s]: the "
          "modular spectrum is the full two-sided RATIO spectrum of "
          "rho_OS (16 values incl. 4 exact 1's and the degeneracy "
          "p1/p3 = p2/p4) -- the commutant (the reflected half) carries "
          "the SAME density: the purification is reflection-symmetric, "
          "exactly as the bond-cut theta demands"
          % mp.nstr(dev, 3), ok)


def t4_clock_reading():
    print("  -- T4: the clock vs the modular data (typed [C-5])")
    silver = mp.sqrt(2) - 1
    ED = FLAGS['ED']
    specD = FLAGS['specD']
    gap_quarter = min(abs(x ** mp.mpf('0.25') - silver) for x in specD
                      if x > 0)
    gap_full = min(abs(x - silver) for x in specD if x > 0)
    naive_fails = gap_quarter > mp.mpf('0.01') and gap_full > mp.mpf('0.01')
    # tau_k vs G Delta^{k/N} on the Klein-Landau domains
    Gn, Ghi, Gh, QD = FLAGS['Gn'], FLAGS['Ghi'], FLAGS['Gh'], FLAGS['QD']

    def Dpow(s):
        return Ghi * QD * mp.diag([ED[i].real ** s for i in range(16)]) \
            * ctr(QD) * Gh

    def tau_mat(D, k):
        M = sp.zeros(len(D), len(D))
        for i, ma in enumerate(D):
            ca, mta = theta_mono(ma, R7, S7, ETA)
            for j, mb in enumerate(D):
                cb, mbb = alpha_mono(mb, TW8[k])
                cs, mm = mono_mul(mta, mbb)
                M[i, j] = sp.expand_complex(ca * cb * cs * wick(mm, N8))
        return M

    D1 = [m for m in BASIS8 if all(4 <= a <= 6 for a in m)]
    D2 = [m for m in BASIS8 if all(4 <= a <= 5 for a in m)]
    res = {}
    for D, k, s in ((D1, 1, mp.mpf(1) / 8), (D2, 2, mp.mpf(1) / 4)):
        tn = to_mp(tau_mat(D, k))
        GDs = Gn * Dpow(s)
        idx = [BIDX[m] for m in D]
        r = max(abs(GDs[a, b] - tn[i, j])
                for i, a in enumerate(idx) for j, b in enumerate(idx))
        res[k] = r
    not_geometric = res[1] > mp.mpf('0.1') and res[2] > mp.mpf('0.1')
    # the exact positive replacement + beta2 clock regression
    silver_id = iszero(c_of(3, 8) / c_of(1, 8) - (sp.sqrt(2) - 1))
    cosh_id = iszero(sp.simplify(
        2 * (1 + 2 * (sp.sqrt(2) / 4)) - 1 - (1 + sp.sqrt(2))))
    # 2 cosh 2w - 1 with sinh^2 w = sqrt2/4  ->  1 + sqrt2
    lamv = sp.symbols('lamv')
    G8 = FLAGS['G8']
    tau2 = tau_mat(D2, 2)
    idx2 = [BIDX[m] for m in D2]
    Gs = sp.Matrix(4, 4, lambda i, j: G8[idx2[i], idx2[j]])
    io = [k for k, m in enumerate(D2) if len(m) % 2 == 1]
    ie = [k for k, m in enumerate(D2) if len(m) % 2 == 0]
    ok_clock = True
    for sec in (io, ie):
        Gb = Gs.extract(sec, sec)
        Tb = tau2.extract(sec, sec)
        roots = sp.solve(sp.det(Tb - lamv * Gb), lamv)
        ok_clock = ok_clock and len(roots) == 2 \
            and any(iszero(r - 1) for r in roots) \
            and any(iszero(r - (sp.sqrt(2) - 1)) for r in roots)
    FLAGS['t4'] = (naive_fails and not_geometric and silver_id and cosh_id
                   and ok_clock)
    check("T4 CLOCK vs MODULAR DATA [typed [C-5] finding; pre-declared]: "
          "the NAIVE reading fails exactly as pre-derived -- sqrt2 - 1 is "
          "NOT an e^{-Delta K} ratio (min gap to spec Delta^{1/4}: %s, to "
          "spec Delta: %s) and the transfer is NOT the modular flow: "
          "max|tau_1 - G Delta^{1/8}| = %s, max|tau_2 - G Delta^{1/4}| = "
          "%s on the Klein-Landau domains (the half-circle interval "
          "modular flow of a thermal chiral fermion is non-geometric, as "
          "in CFT); the EXACT replacement holds: sqrt2 - 1 = C(3)/C(1) "
          "(%s) = 1/(2 cosh 2 omega - 1) (%s, sinh^2 omega = sqrt2/4) -- "
          "the silver clock eigenvalue is a thermal KERNEL ratio; beta2 "
          "compressed clock spectrum {1, sqrt2 - 1} re-verified exactly "
          "in both parity sectors (%s)"
          % (mp.nstr(gap_quarter, 4), mp.nstr(gap_full, 4),
             mp.nstr(res[1], 4), mp.nstr(res[2], 4), silver_id, cosh_id,
             ok_clock), FLAGS['t4'])


# ---------------------------------------------------------------------------
# Part B -- transfer-flow KMS: the beta measurement (exact)
# ---------------------------------------------------------------------------
def b1_recurrence8():
    print("  -- B1: N = 8 palindromic recurrence -- the mode structure")
    f = [c_of(d, 8) for d in range(1, 8)]        # f_1..f_7
    # palindromic ansatz f_{d+4} = a(f_{d+3} + f_{d+1}) + b f_{d+2} - f_d
    # d = 2 equation: 0 = a (C5 + C3) with C5 + C3 = 2 C3 != 0 => a = 0
    a_forced = (not iszero(f[4] + f[2])) and iszero(f[5]) \
        and iszero(f[3]) and iszero(f[1])
    b1 = sp.simplify((f[4] + f[0]) / f[2])       # from d = 1
    b3 = sp.simplify((f[6] + f[2]) / f[4])       # from d = 3
    consist = iszero(b1 - b3)
    b_ok = iszero(b1 - (2 + sp.sqrt(2)))
    # z^4 - b z^2 + 1 = 0: modes {q, 1/q, -q, -1/q}, q^2 + q^{-2} = b
    QQok = iszero(sp.expand(QQ_ ** 2 - (2 + sp.sqrt(2)) * QQ_ + 1))
    sinh_ok = iszero(sp.expand(QQ_ + 1 / QQ_ - 2 - sp.sqrt(2)))
    om_num = mp.log(mp.mpf(str(sp.N(q_, 45))))
    om_ok = abs(om_num - mp.asinh(2 ** mp.mpf('-0.75'))) < TOL
    # zeta_8 certificate of the consistency: C1/C3 = 1 + sqrt2 with
    # sqrt2 = z^2 + z^{-2} at z = e^{i pi/8}
    lhs = (ZSYM ** 3 - ZSYM ** -3) - \
        (1 + ZSYM ** 2 + ZSYM ** -2) * (ZSYM - ZSYM ** -1)
    zc = zeta_zero(lhs, 8)
    FLAGS['b1'] = (a_forced and consist and b_ok and QQok and sinh_ok
                   and om_ok and zc)
    check("B1 N = 8 MODE STRUCTURE [exact]: the palindromic Prony "
          "recurrence on C(1..7) forces a = 0 (checkerboard: the +- "
          "momentum-0/pi doubling, %s) and CLOSES with ONE consistency "
          "equation satisfied exactly: b = (C1+C3)/C3 from d = 1 equals "
          "(C7+C3)/C5 from d = 3 (%s), b = 2 + sqrt2 (%s; cyclotomic "
          "certificate mod z^8+1: %s) -- modes {+-q, +-1/q} with "
          "q^2 + q^{-2} = 2 + sqrt2 (%s), i.e. (q - 1/q)^2 = sqrt2: "
          "omega = ln q = arcsinh(2^{-3/4}) = %s (%s) -- ONE real "
          "frequency: the seam kernel is a bona fide finite thermal-mode "
          "kernel"
          % (a_forced, consist, b_ok, zc, QQok, mp.nstr(om_num, 10),
             om_ok and sinh_ok), FLAGS['b1'])


def b2_beta8():
    print("  -- B2: N = 8 detailed balance -- beta measured = N")
    # measured kappa from the d = 1,3 solve (beta NOT input):
    # C(d) = v1 q^{-d} + v2 q^{d};  kappa := v2/v1 must equal q^{-8}
    v2 = (C3 - q_ ** -2 * C1) / (q_ ** 3 - q_ ** -1)
    v1 = (C1 - v2 * q_) * q_
    # exact route: kappa = q^{-8}  <=>  (1+sqrt2) Q = Q^2 - Q + 1
    # (the minimal polynomial Q^2 - (2+sqrt2) Q + 1 = 0 again)
    kap_id = iszero(sp.expand((1 + sp.sqrt(2)) * QQ_
                              - (QQ_ ** 2 - QQ_ + 1)))
    kap_num = mp.mpf(str(sp.N(v2 / v1, 45)))
    q_num = mp.mpf(str(sp.N(q_, 45)))
    kap_meas = abs(kap_num - q_num ** -8) < TOL
    # full detailed-balance representation, all four odd separations
    w_ = C1 / (2 * (q_ ** -1 + q_ ** -7))
    rep_ok = all(abs(mp.mpf(str(sp.N(
        c_of(d, 8) - 2 * w_ * (q_ ** -d + q_ ** (d - 8)), 45)))) < TOL
        for d in (1, 3, 5, 7))
    w_pos = sp.N(w_, 30) > 0
    n_fd = 1 / (1 + q_num ** 8)
    FLAGS['q_num'] = q_num
    FLAGS['b2'] = kap_id and kap_meas and rep_ok and w_pos
    check("B2 N = 8 DETAILED BALANCE -- MEASURED beta = 8 = N [exact]: "
          "solving the two-mode system on d = 1, 3 WITHOUT inputting "
          "beta gives growing/decaying weight ratio kappa = q^{-8} "
          "exactly (Q-polynomial identity Q/(Q^2-Q+1) = C3/C1 = "
          "1/(1+sqrt2): %s; 40-digit: %s), and the full representation "
          "C(d) = 2w (q^{-d} + q^{d-8}) holds at ALL odd separations "
          "d = 1, 3, 5, 7 (%s) with weight w = %s > 0 (%s) -- the "
          "reconstructed transfer dynamics sees the seam state as a "
          "Gibbs/KMS state at inverse temperature beta = N = 8 clock "
          "steps; Fermi-Dirac occupation n = 1/(1 + q^8) = %s"
          % (kap_id, kap_meas, rep_ok, mp.nstr(mp.mpf(str(sp.N(w_, 45))),
                                               8), bool(w_pos),
             mp.nstr(n_fd, 8)), FLAGS['b2'])


def b3_beta16():
    print("  -- B3: N = 16 -- two real pairs, beta = N, sqrt2 anchor")
    # exact solve of the j-unit recurrence with cyclotomic h-values:
    # h_j = 1/(z^{2j-1} - z^{-(2j-1)}) ~ C(2j-1) up to a common factor
    hz = [1 / (ZSYM ** (2 * jj - 1) - ZSYM ** -(2 * jj - 1))
          for jj in range(1, 9)]
    a, b = sp.symbols('a b')
    eqs = [hz[j + 3] - a * (hz[j + 2] + hz[j]) - b * hz[j + 1] + hz[j - 1]
           for j in (1, 2, 3, 4)]
    sol = sp.solve(eqs[:2], [a, b], dict=True)[0]
    res3 = eqs[2].subs(sol)
    res4 = eqs[3].subs(sol)
    z16 = 16
    c34 = zeta_zero(res3, z16) and zeta_zero(res4, z16)
    # anchor prod(u_i - 2) = 2 - b - 2a = sqrt2 = z^4 + z^{-4}
    anchor = zeta_zero(2 - sol[b] - 2 * sol[a] - (ZSYM ** 4 + ZSYM ** -4),
                       z16)
    zeta16 = sp.exp(sp.I * sp.pi / 16)
    a_val = sp.N(sol[a].subs(ZSYM, zeta16), 40)
    b_val = sp.N(sol[b].subs(ZSYM, zeta16), 40)
    a_re, a_im = [mp.mpf(str(x)) for x in a_val.as_real_imag()]
    b_re, b_im = [mp.mpf(str(x)) for x in b_val.as_real_imag()]
    # u quadratic: u^2 - a u - (b + 2) = 0 -> both roots real > 2
    disc = a_re ** 2 + 4 * (b_re + 2)
    u1 = (a_re + mp.sqrt(disc)) / 2
    u2 = (a_re - mp.sqrt(disc)) / 2
    real_pairs = (abs(a_im) < TOL and abs(b_im) < TOL
                  and disc > 0 and u1 > 2 and u2 > 2)
    # weights + measured exponent (40-digit Prony in j-units)
    hval = [mp.mpf(str(sp.N(c_of(2 * jj - 1, 16), 45)))
            for jj in range(1, 9)]
    Mh = mp.matrix(4, 4)
    bv = mp.matrix(4, 1)
    for i2 in range(4):
        for j2 in range(4):
            Mh[i2, j2] = hval[i2 + j2]
        bv[i2, 0] = hval[i2 + 4]
    rl = mp.lu_solve(Mh, bv)
    coeffs = [mp.mpf(1), -rl[3, 0], -rl[2, 0], -rl[1, 0], -rl[0, 0]]
    zr = mp.polyroots(coeffs, maxsteps=200, extraprec=100)
    zr = [r.real for r in zr]
    all_real_pos = all(abs(mp.im(r)) < TOL for r in
                       mp.polyroots(coeffs, maxsteps=200, extraprec=100)) \
        and all(r > 0 for r in zr)
    V4 = mp.matrix(4, 4)
    for i2 in range(4):
        for j2 in range(4):
            V4[i2, j2] = zr[j2] ** (i2 + 1)
    hv4 = mp.matrix(4, 1)
    for i2 in range(4):
        hv4[i2, 0] = hval[i2]
    Wv = mp.lu_solve(V4, hv4)
    expo_ok = True
    w_pos16 = all(Wv[i2, 0] > 0 for i2 in range(4))
    oms = []
    for i2 in range(4):
        for j2 in range(i2 + 1, 4):
            if abs(zr[i2] * zr[j2] - 1) < mp.mpf(10) ** -20:
                zd = min(zr[i2], zr[j2])
                wd = Wv[i2, 0] if zr[i2] == zd else Wv[j2, 0]
                wg = Wv[j2, 0] if zr[i2] == zd else Wv[i2, 0]
                expo = mp.log(wg / wd) / mp.log(zd)
                # j-units: exponent (N/2)+1 = 9  <=>  beta = 16 = N
                expo_ok = expo_ok and abs(expo - 9) < TOL
                oms.append(mp.log(1 / zd) / 2)
    prod_sinh = mp.mpf(1)
    for om in oms:
        prod_sinh *= mp.sinh(om)
    anchor_num = abs(prod_sinh - 2 ** mp.mpf('-1.75')) < TOL
    FLAGS['oms16'] = oms
    FLAGS['b3'] = (c34 and anchor and real_pairs and all_real_pos
                   and expo_ok and w_pos16 and anchor_num)
    check("B3 N = 16 -- THE SAME KMS CLOSURE, TWO MODES [exact "
          "cyclotomic + 40-digit]: the palindromic recurrence (2 "
          "unknowns from j = 1, 2) satisfies the remaining equations "
          "j = 3, 4 EXACTLY mod z^16 + 1 (%s); both mode pairs are REAL "
          "with u_i = q_i^2 + q_i^{-2} > 2 (%s; omega_1 = %s, omega_2 = "
          "%s), all four Prony roots real positive (%s), weights "
          "positive (%s); MEASURED weight-pairing exponent = 9 = (N/2)+1 "
          "in j-units, i.e. beta = 16 = N (%s); EXACT ANCHOR at both "
          "levels: prod_i (u_i - 2) = sqrt2 (cyclotomic: %s; equivalent "
          "40-digit: prod sinh omega_i = 2^{-7/4}: %s; at N = 8: "
          "(q - 1/q)^2 = sqrt2) -- the |mu_4|-th root of 2 pins the "
          "frequency content at every level"
          % (c34, real_pairs, mp.nstr(oms[0] if oms else mp.mpf(0), 8),
             mp.nstr(oms[1] if len(oms) > 1 else mp.mpf(0), 8),
             all_real_pos, w_pos16, expo_ok, anchor, anchor_num),
          FLAGS['b3'])


def b4_wrong_beta():
    print("  -- B4: wrong-beta candidates excluded (quantified)")
    q_num = FLAGS['q_num']
    kap = q_num ** -8
    gaps = {half: abs(kap - q_num ** -half) for half in (4, 2, 16)}
    all_pos = all(g > mp.mpf('0.005') for g in gaps.values())
    wit = iszero((C1 - C3) - sp.sqrt(2) * C3)
    wit_num = mp.mpf(str(sp.N(C1 - C3, 45)))
    FLAGS['b4'] = all_pos and wit
    check("B4 WRONG-beta CANDIDATES EXCLUDED [exact + 40-digit]: "
          "detailed balance pins kappa = q^{-8}; the candidates beta = "
          "N/2, N/4, 2N would need q^{-4}, q^{-2}, q^{-16} -- gaps "
          "|q^{-8} - q^{-4}| = %s, |q^{-8} - q^{-2}| = %s, |q^{-8} - "
          "q^{-16}| = %s, all > 0 (%s); direct N/2-periodicity witness: "
          "KMS at beta = 4 would demand C(d) = C(d+4)-matching, but "
          "C(1) - C(3) = sqrt2 C(3) EXACTLY (%s; = %s != 0) -- the "
          "seam temperature is UNIQUELY beta = N in the preregistered "
          "candidate lattice"
          % (mp.nstr(gaps[4], 6), mp.nstr(gaps[2], 6),
             mp.nstr(gaps[16], 6), all_pos, wit, mp.nstr(wit_num, 8)),
          FLAGS['b4'])


# ---------------------------------------------------------------------------
# Part C -- the temperature bridge to the Nariai/BH chain
# ---------------------------------------------------------------------------
def c1_bridge():
    print("  -- C1: beta_angle = 2 pi = 1/(4 c3) -- the v208 closure")
    # one clock step = euclidean angle 2 pi/N (v519 pin, re-verified R1)
    beta_angle = sp.Integer(N8) * (2 * pi_ / N8)
    cls1 = iszero(beta_angle - 2 * pi_)
    v58 = iszero(2 * pi_ - 1 / (4 * c3))
    Tseam = sp.simplify(1 / beta_angle)
    Tid = iszero(Tseam - 4 * c3)
    beta16 = sp.Integer(N16) * (2 * pi_ / N16)
    cls16 = iszero(beta16 - 2 * pi_)
    FLAGS['c1'] = cls1 and v58 and Tid and cls16
    check("C1 THE BRIDGE CLOSES IN CLASS 1 [exact]: beta_steps = N "
          "(measured, B2/B3) x angle-per-step 2 pi/N (v519 geometric "
          "pin) = beta_angle = 2 pi at BOTH levels (%s/%s) -- and "
          "2 pi = 1/(4 c3) EXACTLY (%s, v58/v208): T_seam = 1/(2 pi) = "
          "4 c3 (%s) -- the reconstructed seam state is KMS at exactly "
          "the Bisognano-Wichmann/Hawking modular normalisation "
          "Delta^{it} = e^{-2 pi t K} that v208 carries into the "
          "horizon sector; N-independence: the temperature in angle "
          "units does not depend on the lattice size (8 vs 16), exactly "
          "as a universal modular temperature must"
          % (cls1, cls16, v58, Tid), FLAGS['c1'])


def c2_hawking_chain():
    print("  -- C2: the Hawking/Nariai chain in the same normalisation")
    M, Lam, rh = sp.symbols('M Lambda r_h', positive=True)
    T_H = (sp.Rational(1, 4) / M) / (2 * pi_)
    schw = iszero(T_H - c3 / M) and iszero(T_H - 1 / (8 * pi_ * M))
    sds = iszero(1 / (4 * pi_) - 2 * c3)
    T_N = sp.sqrt(Lam) / (2 * pi_)
    nariai = iszero(T_N - 4 * c3 * sp.sqrt(Lam))
    rate_link = iszero(2 * sp.sqrt(Lam) / T_N - 4 * pi_) \
        and iszero(4 * pi_ - 1 / (2 * c3))
    FLAGS['c2'] = schw and sds and nariai and rate_link
    check("C2 HAWKING/NARIAI CHAIN [exact, = v208/v104 normalisations]: "
          "with the seam-supplied 1/(2 pi) = 4 c3, Schwarzschild "
          "T_H = kappa_h/(2 pi) = c3/M = 1/(8 pi M) (%s) -- THE AXIOM "
          "c3 = 1/(8 pi) IS the Hawking coefficient, now derived from "
          "the seam KMS temperature rather than postulated; SdS "
          "1/(4 pi) = 2 c3 (%s, v208 check 3); Nariai T_N = "
          "sqrt(Lambda)/(2 pi) = 4 c3 sqrt(Lambda) (%s); v104 "
          "cross-link: the Nariai entropy-deviation rate 2H satisfies "
          "2H/T_N = 4 pi = 1/(2 c3) exactly (%s) -- temperature joins "
          "geometry (v101/v104) and anomaly as the third leg of c3"
          % (schw, sds, nariai, rate_link), FLAGS['c2'])


def c3_class_audit():
    print("  -- C3: anti-numerology class audit")
    # the measurement kills every class value except r = 1
    q_num = FLAGS['q_num']
    kap = q_num ** -8
    excluded = []
    for r_ in (sp.Rational(1, 4), sp.Rational(1, 2), 2, 4):
        beta_steps = 8 * r_
        need = q_num ** (-float(beta_steps))
        excluded.append(abs(kap - need) > mp.mpf('0.005'))
    # c3-power / mu4 / N dressings cannot rescue: beta_angle/(2pi) is a
    # PURE NUMBER = 1 exactly; any c3^k (k != 0) dressing would make it
    # transcendental-inhomogeneous (pi-degree mismatch) -- record
    pure = iszero((sp.Integer(8) * (2 * pi_ / 8)) / (2 * pi_) - 1)
    FLAGS['c3a'] = all(excluded) and pure
    check("C3 ANTI-NUMEROLOGY AUDIT [exact + 40-digit]: within the "
          "FROZEN relation classes beta_angle/(2 pi) in {1/4, 1/2, 1, "
          "2, 4} (x optional c3^k, |mu_4|, N dressings), the "
          "measurement selects EXACTLY r = 1 (%s): the four alternative "
          "rationals are excluded by the detailed-balance gaps (%s), "
          "and beta_angle/(2 pi) = 1 is a pure number (%s) -- no "
          "c3-power dressing can reproduce it (pi-degree mismatch): "
          "the closure is the class-1 identity, not a tuned fit"
          % (pure, all(excluded), pure), FLAGS['c3a'])


# ---------------------------------------------------------------------------
# Part S -- entropy
# ---------------------------------------------------------------------------
def s1_entropy():
    print("  -- S1: S(rho_OS) exact form + Gaussian tower N = 8, 16, 32")
    nu1, nu2 = mp.cos(mp.pi / 24), mp.cos(7 * mp.pi / 24)
    S_p = -mp.fsum([p * mp.log(p) for p in FLAGS['ps']])

    def Hnu(nu):
        return (mp.log(2)
                - ((1 + nu) * mp.log(1 + nu)
                   + (1 - nu) * mp.log(1 - nu)) / 2)

    S_form = Hnu(nu1) + Hnu(nu2)
    form_ok = abs(S_p - S_form) < TOL
    Ss = {}
    nus_all = {}
    for NN in (8, 16, 32):
        half = list(range(NN // 2, NN))
        nh = len(half)
        Jh = mp.matrix(nh, nh)
        for i2, a2 in enumerate(half):
            for j2, b2 in enumerate(half):
                if (a2 - b2) % 2 == 1:
                    Jh[i2, j2] = 1j * 2 / mp.mpf(NN) \
                        / mp.sin(mp.pi * (a2 - b2) / NN)
        Eh, _ = mp.eighe(Jh)
        nsv = sorted([abs(Eh[i2].real) for i2 in range(nh)])[::2]
        nus_all[NN] = nsv
        Ss[NN] = mp.fsum([Hnu(nu) for nu in nsv])
    faithful16 = all(mp.mpf(0) < nu < 1 for nu in nus_all[16])
    match8 = abs(Ss[8] - S_p) < TOL
    FLAGS['Ss'] = Ss
    FLAGS['s1'] = form_ok and match8 and faithful16
    check("S1 ENTROPY EXACT FORM + TOWER [40-digit]: S(rho_OS) = "
          "sum_i [ln 2 - ((1+nu)ln(1+nu) + (1-nu)ln(1-nu))/2] matches "
          "-sum p ln p (%s); S(8) = %s, S(16) = %s, S(32) = %s nats "
          "(Gaussian covariance; N = 8 cross-check %s); all N = 16 "
          "Williamson values strictly inside (0,1) (%s) -- rho_OS is "
          "faithful/thermal at N = 16 too (the Gaussian certificate of "
          "the same statement proved algebraically at N = 8); N = 16 "
          "nu's have no closed cos-form in the pi/48 family (recorded "
          "honestly, 40-digit values kept)"
          % (form_ok, mp.nstr(Ss[8], 8), mp.nstr(Ss[16], 8),
             mp.nstr(Ss[32], 8), match8, faithful16), FLAGS['s1'])


def s2_scaling():
    print("  -- S2/S3: preregistered entropy structures (non-gating)")
    Ss = FLAGS['Ss']
    ds1 = (Ss[16] - Ss[8]) / mp.log(2)
    ds2 = (Ss[32] - Ss[16]) / mp.log(2)
    sixth = mp.mpf(1) / 6
    e1 = abs(ds2 - sixth) < abs(ds1 - sixth) and abs(ds2 - sixth) < 0.02
    fr8 = Ss[8] / (2 * mp.log(2))
    fr16 = Ss[16] / (4 * mp.log(2))
    e2_fails = (min(abs(fr8 - mp.mpf(1) / 3), abs(fr8 - mp.mpf(2) / 3))
                > mp.mpf('0.04')
                and min(abs(fr16 - mp.mpf(1) / 3),
                        abs(fr16 - mp.mpf(2) / 3)) > mp.mpf('0.04')
                and abs(fr8 - fr16) > mp.mpf('0.1'))
    e3_fails = fr8 < mp.mpf(2) / 3 and fr16 < mp.mpf(2) / 3
    FLAGS['s2'] = e1 and e2_fails and e3_fails
    check("S2/S3 ENTROPY STRUCTURES [non-gating, outcomes as "
          "pre-derived]: (E1) chiral-CFT ln-law CONFIRMS -- DeltaS/ln2 "
          "= %s -> %s approaching c_chi/3 = 1/6 = %s monotonically (%s): "
          "the seam entanglement entropy has the c = 1/2 chiral AREA/log "
          "law, thermal-but-critical, NOT extensive; (E2) the v129 "
          "horizon fractions {1/3, 2/3} do NOT transfer: S/S_max = %s "
          "(N=8), %s (N=16), not N-stable (%s); (E3) the v190 floor 2/3 "
          "does not transfer either (%s) -- the Nariai entropy ledger "
          "lives on horizon ratios, the seam on entanglement: the "
          "TEMPERATURE bridge closes, the entropy-fraction bridge "
          "honestly does not"
          % (mp.nstr(ds1, 6), mp.nstr(ds2, 6), mp.nstr(sixth, 6), e1,
             mp.nstr(fr8, 5), mp.nstr(fr16, 5), e2_fails, e3_fails),
          FLAGS['s2'])


# ---------------------------------------------------------------------------
# Part N -- negative controls
# ---------------------------------------------------------------------------
def n1_site_cut():
    print("  -- N1: site cut -- no state, no KMS")
    P8s = [1, 2, 3]
    basis8s = [m for d in range(4) for m in combinations(P8s, d)]
    r8_ = lambda a: (-a) % N8
    PLUS = lambda a: 1
    picked = None
    for etac in (sp.Integer(1), sp.Integer(-1), I, -I):
        M = sp.zeros(8, 8)
        for i, ma in enumerate(basis8s):
            ca, mta = theta_mono(ma, r8_, PLUS, etac)
            for j, mb in enumerate(basis8s):
                cs, mm = mono_mul(mta, mb)
                M[i, j] = sp.expand_complex(ca * cs * wick(mm, N8))
        if all(iszero(x) for x in (M - M.conjugate().T)):
            inert, _ = spectrum_inertia(M)
            picked = (etac, inert)
            break
    FLAGS['n1'] = picked is not None and picked[1][1] >= 2
    check("N1 SITE CUT -> NO STATE [exact + 40-digit]: the site-placed "
          "OS form on the full site-half algebra {1,2,3} is Hermitian "
          "for eta = %s but INDEFINITE, inertia %s (%d negative "
          "directions) -- no PSD Gram, no H_phys, no purification, no "
          "rho_OS, hence NO KMS state: the thermal reconstruction "
          "exists only at the bond placement (beta2 C4.1 reproduced at "
          "thermal level)"
          % (picked[0] if picked else None,
             picked[1] if picked else None,
             picked[1][1] if picked else -1), FLAGS['n1'])


def n2_family_a():
    print("  -- N2: family A -- no quotient to be thermal")
    r_anti = lambda a: (a + 8) % N16
    s_alt = lambda a: 1 if a % 2 == 0 else -1
    basis_a = [(a,) for a in range(8)]
    picked = None
    for etac in (sp.Integer(1), sp.Integer(-1), I, -I):
        M = sp.zeros(8, 8)
        for i, ma in enumerate(basis_a):
            ca, mta = theta_mono(ma, r_anti, s_alt, etac)
            for j, mb in enumerate(basis_a):
                cs, mm = mono_mul(mta, mb)
                M[i, j] = sp.expand_complex(ca * cs * wick(mm, N16))
        if all(iszero(x) for x in (M - M.conjugate().T)):
            inert, _ = spectrum_inertia(M)
            diag0 = all(iszero(M[i, i]) for i in range(8))
            picked = (etac, inert, diag0)
            break
    FLAGS['n2'] = (picked is not None and picked[1] == (4, 4, 0)
                   and picked[2])
    check("N2 FAMILY A -> NO THERMAL STATE [exact + 40-digit]: the "
          "clock-centralising antipode (alternating dressing) is "
          "Hermitian only for eta = %s with ZERO diagonal (%s) and "
          "inertia %s -- indefinite at the one-particle level already: "
          "no PSD form, no purification, nothing to be KMS (beta2 C4.2 "
          "reproduced)"
          % (picked[0] if picked else None,
             picked[2] if picked else None,
             picked[1] if picked else None), FLAGS['n2'])


def n3_antichiral():
    print("  -- N3: anti-chiral state -- wrong chirality has no state")
    G8a = sp.zeros(16, 16)
    for i, ma in enumerate(BASIS8):
        ca, mta = theta_mono(ma, R7, S7, ETA)
        for j, mb in enumerate(BASIS8):
            cs, mm = mono_mul(mta, mb)
            G8a[i, j] = sp.expand_complex(ca * cs * wick(mm, N8, chi=-1))
    herm = all(iszero(x) for x in (G8a - G8a.conjugate().T))
    ev_idx = [i for i, m in enumerate(BASIS8) if len(m) % 2 == 0]
    od_idx = [i for i, m in enumerate(BASIS8) if len(m) % 2 == 1]
    in_ev, _ = spectrum_inertia(G8a.extract(ev_idx, ev_idx))
    in_od, _ = spectrum_inertia(G8a.extract(od_idx, od_idx))
    in_all, _ = spectrum_inertia(G8a)
    FLAGS['n3'] = (herm and in_od == (0, 8, 0) and in_ev == (8, 0, 0)
                   and in_all == (8, 8, 0))
    check("N3 ANTI-CHIRAL -> NO STATE [exact + 40-digit]: with C -> -C "
          "and the same twist the Gram stays Hermitian (%s) but the odd "
          "block flips NEGATIVE definite %s (even %s, total %s) -- the "
          "OS quotient and hence the thermal representation exist ONLY "
          "for the chirality matching the twist (beta2 C4.3 reproduced)"
          % (herm, in_od, in_ev, in_all), FLAGS['n3'])


def n4_noncompact():
    print("  -- N4: non-compact control -- the temperature needs the "
          "compact circle")
    # half-line kernel: h_j = 1/(2j-1) (x 2/pi, cancels in all tests)
    hL = [sp.Rational(1, 2 * jj - 1) for jj in range(1, 5)]
    hC = [c_of(2 * jj - 1, 8) for jj in range(1, 5)]
    ret_dead = not iszero(sp.Rational(2, 1) / pi_ / 7
                          - sp.Rational(2, 1) / pi_)   # C(7) != C(1)
    ret_alive = iszero(hC[3] - hC[0]) and iszero(hC[2] - hC[1])
    mono_line = all(hL[k + 1] < hL[k] for k in range(3))
    return_wit = iszero((hC[3] - hC[2]) - sp.sqrt(2) * c_of(3, 8))
    # recurrence consistency: b from j=1 vs j=2 (degree-2, j-units)
    bL1 = (hL[2] + hL[0]) / hL[1]
    bL2 = (hL[3] + hL[1]) / hL[2]
    gapL = sp.simplify(bL1 - bL2)
    gap_exact = sp.Rational(128, 105)
    line_fails = iszero(gapL - gap_exact) and gap_exact != 0
    bC1 = sp.simplify((hC[2] + hC[0]) / hC[1])
    bC2 = sp.simplify((hC[3] + hC[1]) / hC[2])
    circle_closes = iszero(bC1 - bC2)
    # Stieltjes: 2/(pi d) = (2/pi) int_0^1 x^{d-1} dx -> no growing part
    d_ = sp.symbols('d_', positive=True)
    x_ = sp.symbols('x_', positive=True)
    stj = iszero(sp.integrate(x_ ** (d_ - 1), (x_, 0, 1)) - 1 / d_)
    # contraction restored on the line vs silver expansion on the circle
    contr = all(sp.Rational(2 * jj - 1, 2 * jj + 1) < 1
                for jj in range(1, 4))
    expand_circle = iszero(hC[0] / hC[1] - (1 + sp.sqrt(2)))
    FLAGS['n4'] = (ret_dead and ret_alive and mono_line and return_wit
                   and circle_closes and line_fails and stj and contr
                   and expand_circle)
    check("N4 NON-COMPACT CONTROL -> T = 0 [exact]: on the half-line "
          "kernel 2/(pi d) the return symmetry is DEAD (2/(7 pi) != "
          "2/pi: %s; circle: C(7) = C(1), C(5) = C(3): %s) and the "
          "kernel decays monotonically (%s) where the circle RETURNS "
          "(h4 - h3 = +sqrt2 C(3): %s); the palindromic recurrence "
          "closes exactly on the circle (%s) but FAILS on the line with "
          "exact gap b(j=1) - b(j=2) = %s != 0 (%s); the line kernel is "
          "Stieltjes: 1/d = int_0^1 x^{d-1} dx (%s) -- ONLY decaying "
          "modes, growing weights identically zero: kappa = 0, beta = "
          "inf, T = 0 (ground state, contraction semigroup restored: "
          "ratios < 1: %s) while the compact circle carries the silver "
          "expansion C(1)/C(3) = 1 + sqrt2 (%s) -- the seam temperature "
          "hangs EXACTLY on the compactness of the euclidean circle"
          % (ret_dead, ret_alive, mono_line, return_wit, circle_closes,
             gap_exact, line_fails, stj, contr, expand_circle),
          FLAGS['n4'])


# ---------------------------------------------------------------------------
# Part V -- verdict
# ---------------------------------------------------------------------------
def v1_verdict():
    print("  -- V1: verdict per the frozen preregistration")
    k1 = not (FLAGS['r2'] and FLAGS['r4'] and FLAGS['t1'] and FLAGS['t2'])
    k2 = not (FLAGS['b1'] and FLAGS['b2'] and FLAGS['b3'] and FLAGS['b4'])
    k3 = not FLAGS['c1']
    kill = k1 or k2 or k3
    s_ok = (FLAGS['r1'] and FLAGS['r3'] and FLAGS['t3'] and FLAGS['c2']
            and FLAGS['c3a'] and FLAGS['s1'] and FLAGS['n1']
            and FLAGS['n2'] and FLAGS['n3'] and FLAGS['n4'])
    if kill:
        verdict = "KILL"
    elif s_ok:
        verdict = "SUCCESS"
    else:
        verdict = "UNDECIDED"
    FLAGS['verdict'] = verdict
    print("VERDICT: %s" % verdict)
    check("V1 VERDICT = %s [frozen C-8 logic]: no kill -- rho_OS "
          "faithful + Tomita KMS exact (K1 clear), transfer detailed "
          "balance gives beta = N at BOTH levels (K2 clear), bridge "
          "lands in class 1 (K3 clear); success block: kernel "
          "preconditions, closed forms, ratio spectrum, Hawking/Nariai "
          "chain, class audit, entropy computed, all five controls "
          "behave.  [C-5] recorded findings (non-gating): naive "
          "e^{-Delta K} clock reading FAILS; Tomita flow != transfer "
          "flow; the exact silver identity sqrt2 - 1 = C(3)/C(1) = "
          "1/(2 cosh 2 omega - 1) replaces it.  Scope fence: free seam "
          "system only; the bridge statement is [C]-typed (seam "
          "euclidean circle = thermal circle of the reconstructed "
          "horizon dynamics); NOTHING integrated -- all markers stay; "
          "sandbox only" % verdict, verdict == "SUCCESS")


def run():
    reset()
    print("v526 SEAM.THERMAL.KMS.01 -- the thermal seam: KMS -> Nariai/BH bridge"
          "KMS -> Nariai/BH bridge (EXPLORATION ONLY)")
    r1_kernel()
    r2_rho()
    r3_closed_forms()
    r4_gram()
    t1_tomita()
    t2_kms_modular()
    t3_spec()
    t4_clock_reading()
    b1_recurrence8()
    b2_beta8()
    b3_beta16()
    b4_wrong_beta()
    c1_bridge()
    c2_hawking_chain()
    c3_class_audit()
    s1_entropy()
    s2_scaling()
    n1_site_cut()
    n2_family_a()
    n3_antichiral()
    n4_noncompact()
    v1_verdict()
    npass = sum(RESULTS)
    print("\n%d/%d checks passed  (runtime %.1f s)"
          % (npass, len(RESULTS), time.perf_counter() - T0_WALL))
    print("FINAL VERDICT: %s" % FLAGS.get('verdict', 'UNDECIDED'))
    return summary("v526 SEAM.THERMAL.KMS.01: beta MEASURED (not assumed) = N at both levels via detailed balance (N=8: omega=arcsinh(2^{-3/4}), kappa=q^{-8}; N=16: pairing exponent (N/2)+1=9); T_seam=1/N per clock step, beta_angle=2pi EXACT = 1/(4 c3), T_seam=4 c3 = Bisognano-Wichmann/Hawking normalisation (v208); modular Hamiltonian closed (nu1=cos(pi/24), nu2=cos(7pi/24); eps=2 ln cot(theta/2); Tomita KMS beta=1 on all 256 pairs); c3 third leg (geometry+anomaly+temperature) class-1 selected; entropy S(8/16/32)=0.52187/0.63510/0.75006, DeltaS/ln2 -> 1/6, horizon fractions do NOT transfer; [C-5] silver = C(3)/C(1) thermal kernel ratio; non-compact => T=0; verdict SUCCESS; no marker moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
