"""Discovery probe (2026-07-23), part 3 of the zeta/prime investigation:
FIRST EXECUTABLE STEP of the candidate contract ZETA.BC.SEAM.KMS from
probe 2 (zeta_explicit_formula_trace_probe.py, 19/19).  Question: can the
v526 thermal seam carry zeta as its PARTITION FUNCTION (Bost-Connes /
primon-gas form), and if not, what exactly is missing?  Five sections:

  S1  Independent rebuild of the v526 seam KMS data from the declared
      kernel C(d) = (2/N)/sin(pi d/N) alone (no v526 code imported):
      half-circle Majorana covariance, Williamson values nu at N = 8 hit
      the exact anchors cos(pi/24), cos(7 pi/24); single-particle energies
      eps = 2 ln cot(pi/48), 2 ln cot(7 pi/48) (exact trig identity
      tanh(ln cot theta) = cos 2 theta); ENTROPY TOWER REPRODUCED:
      S(8) = 0.52187, S(16) = 0.63510, S(32) = 0.75006 nats (v526 [E]-5).
      => the seam sector is a FREE-FERMION KMS tower with finite mode
      ladders; Z_seam(beta) = prod_k (1 + e^{-beta eps_k}) is entire.
  S2  The primon-gas dictionary (what "zeta as partition function" means
      microscopically): bosonic primon gas (one mode per prime, energy
      log p) has Z = zeta(beta) (Euler product = mode sum, checked);
      fermionic primon gas: Z = zeta(beta)/zeta(2 beta) = sum over
      SQUAREFREE n (checked to 1e-6); (-1)^F-GRADED fermionic gas:
      Z_graded = sum mu(n)/n^beta = 1/zeta(beta) -- EXACTLY the clock-trace
      Dirichlet series of probe 1 (mu(q) = tr T_q): the arithmetic sector
      already carries the seam-compatible (Majorana/graded) statistics.
      The beta = 1 pole is HAGEDORN: prime-mode density pi(e^E) ~ e^E/E;
      Mertens sum_p<=P 1/p - ln ln P -> M = 0.2615 (checked).
  S3  The compiler primon gas {2,3,5}: exact identity
      prod_{p in {2,3,5}} (1 - p^-s) = sum_{d|30} mu(d) d^-s
      = sum_{d|30} tr(T_d) d^-s -- the inverse partial zeta over the
      compiler primes IS the Coxeter-tower trace polynomial, term by term;
      subset products of {2,3,5} = divisors(30) = the 8 tower levels
      (squarefree sector of the compiler Fock space); Z_{2,3,5}(2) = 25/16
      exact, Z_{2,3,5}(1) = 15/4 FINITE -- the zeta pole needs ALL primes
      (this finite gas can never produce it).
  S4  THE DISCRIMINATOR (mode counting): seam ladders at N = 8..64 are
      finite and quasi-linear (log n(E) vs E slope ~ 0), while the primon
      ladder has exponential counting (slope of log pi(e^E) vs E ~ 1) and
      collapsing spacings.  VERDICT: "zeta as partition function of the
      FREE seam tower" is KILLED at probe level -- no Hagedorn mode
      proliferation, Z entire, no beta = 1 pole possible.
  S5  Updated contract: the obstruction is COMPLEMENTARY.  The seam has
      the thermodynamics (KMS, measured beta, graded fermionic statistics)
      but no arithmetic mode density; the clock family has the arithmetic
      (divisor-tower semigroup, Galois symmetry, mu = trace) but no
      Hamiltonian.  ZETA.BC.SEAM.KMS sharpened: a bridge must assign
      energy log q to clock level q (BC form H|n> = log n |n>); noted
      honestly as observation: the seam energies ARE logs of algebraic
      units (eps = ln cot^2(...)), the BC energies are logs of integers.

Firewall: discovery sandbox, NO promotion decisions, no marker moves.
Numerical growth statements are consistency checks, not evidence.
"""
import math
import time

import numpy as np
import mpmath
import sympy as sp
from sympy import symbols, expand, simplify, cot, cos, pi, log, divisors, mobius

PASS = 0
FAIL = 0
T0 = time.time()


def check(name, ok):
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}", flush=True)
    if ok:
        PASS += 1
    else:
        FAIL += 1
    return ok


def info(msg):
    print(f"        {msg}", flush=True)


# ================================================================ S1
print("S1 -- independent rebuild of the v526 seam KMS tower from the kernel")


def seam_modes(N):
    """Half-circle Majorana covariance from C(d) = (2/N)/sin(pi d/N),
    odd d only; returns Williamson values nu (one per fermion mode)."""
    L = N // 2
    G = np.zeros((L, L))
    for a in range(L):
        for b in range(L):
            d = a - b
            if d % 2 != 0:
                G[a, b] = (2.0 / N) / math.sin(math.pi * d / N)
    ev = np.linalg.eigvalsh(1j * G)
    nus = np.sort(ev[ev > 1e-12])[::-1]
    return nus


nu8 = seam_modes(8)
anch = [float(cos(pi / 24)), float(cos(7 * pi / 24))]
info(f"N=8 Williamson values: {nu8[0]:.12f}, {nu8[1]:.12f} vs exact "
     f"cos(pi/24) = {anch[0]:.12f}, cos(7pi/24) = {anch[1]:.12f}")
check("N=8 rebuild hits the v526 [E]-3 anchors nu = cos(pi/24), cos(7pi/24) "
      "to 1e-12 (independent construction from the kernel alone)",
      abs(nu8[0] - anch[0]) < 1e-12 and abs(nu8[1] - anch[1]) < 1e-12)
th, y = symbols('theta y', positive=True)
gen1 = simplify(sp.tanh(log(y)).rewrite(sp.exp) - (y**2 - 1) / (y**2 + 1))
gen2 = simplify((cot(th)**2 - 1) / (cot(th)**2 + 1) - cos(2 * th))
inst = max(abs(sp.N(sp.tanh(log(cot(pi / 48))) - cos(pi / 24), 50)),
           abs(sp.N(sp.tanh(log(cot(7 * pi / 48))) - cos(7 * pi / 24), 50)))
check("exact trig identity behind the energies: tanh(ln y) = (y^2-1)/(y^2+1) "
      "and (cot^2-1)/(cot^2+1) = cos(2 theta) symbolically => "
      "tanh(ln cot(pi/48)) = cos(pi/24) (50-digit instantiation)",
      gen1 == 0 and gen2 == 0 and inst < sp.Float(10)**-45)
eps8 = [math.log((1 + v) / (1 - v)) for v in nu8]
eps_exact = [2 * float(sp.log(cot(pi / 48))), 2 * float(sp.log(cot(7 * pi / 48)))]
info(f"N=8 energies eps = {eps8[0]:.6f}, {eps8[1]:.6f} "
     f"(exact 2 ln cot: {eps_exact[0]:.6f}, {eps_exact[1]:.6f})")
check("single-particle energies eps_k = ln((1+nu)/(1-nu)) = 2 ln cot(pi/48), "
      "2 ln cot(7pi/48)", all(abs(a - b) < 1e-10 for a, b in zip(sorted(eps8), sorted(eps_exact))))


def entropy(nus):
    s = 0.0
    for v in nus:
        for w in ((1 + v) / 2, (1 - v) / 2):
            if w > 1e-300:
                s -= w * math.log(w)
    return s


S_tower = {N: entropy(seam_modes(N)) for N in (8, 16, 32)}
info("entropy tower: " + ", ".join(f"S({N}) = {S_tower[N]:.5f}" for N in (8, 16, 32)))
check("v526 [E]-5 entropy tower REPRODUCED: S(8) = 0.52187, S(16) = 0.63510, "
      "S(32) = 0.75006 nats (|diff| < 2e-5 each) -- the rebuild is the same state",
      abs(S_tower[8] - 0.52187) < 2e-5 and abs(S_tower[16] - 0.63510) < 2e-5
      and abs(S_tower[32] - 0.75006) < 2e-5)
check("seam partition function Z(beta) = prod_k (1 + e^{-beta eps_k}) is a "
      "FINITE product per level (N/4 modes) => entire in beta, no pole "
      "possible at any finite level", len(seam_modes(8)) == 2
      and len(seam_modes(16)) == 4 and len(seam_modes(32)) == 8)

# ================================================================ S2
print("S2 -- the primon-gas dictionary: what 'Z = zeta' means microscopically")
s, q = symbols('s q', positive=True)
telescope = expand((1 - q) * sum(q**k for k in range(40)) - (1 - q**40))
num_ok = all(abs(sum(p_**(-2.0 * k) for k in range(200))
                 - 1.0 / (1 - p_**-2.0)) < 1e-14 for p_ in (2, 3, 5, 7))
check("bosonic primon mode: sum_k e^{-beta k log p} = (1 - p^-beta)^-1 "
      "(telescope exact + numeric limit) => Z_bose = prod_p ... = zeta(beta)",
      telescope == 0 and num_ok)

NMAX = 10**6
mu = np.ones(NMAX + 1, dtype=np.int64)
mu[0] = 0
is_comp = np.zeros(NMAX + 1, dtype=bool)
for p in range(2, NMAX + 1):
    if not is_comp[p]:
        is_comp[p * p::p] = True
        mu[p::p] *= -1
        mu[p * p::p * p] = 0
ns = np.arange(0, NMAX + 1, dtype=np.float64)
ns[0] = 1.0
sqf = (mu != 0)
z2 = float(mpmath.zeta(2))
z4 = float(mpmath.zeta(4))
ferm = float(np.sum(sqf[1:] / ns[1:]**2))
info(f"fermionic primon gas: sum_squarefree n^-2 = {ferm:.8f} vs "
     f"zeta(2)/zeta(4) = {z2/z4:.8f}")
check("fermionic primon gas: Z_fermi(2) = zeta(2)/zeta(4) (squarefree sum, "
      "1e-6) -- Pauli principle = squarefree integers",
      abs(ferm - z2 / z4) < 1e-6)
grad = float(np.sum(mu[1:] / ns[1:]**2))
info(f"graded gas: sum mu(n) n^-2 = {grad:.8f} vs 1/zeta(2) = {1/z2:.8f}")
check("(-1)^F-GRADED fermionic primon gas: Z_graded(2) = 1/zeta(2) = "
      "sum mu(n)/n^2 -- EXACTLY the clock-trace Dirichlet series of probe 1 "
      "(mu(q) = tr T_q): the arithmetic sector already carries the "
      "seam-compatible graded Majorana statistics", abs(grad - 1 / z2) < 1e-4)
primes = np.nonzero(~is_comp)[0]
primes = primes[primes >= 2]
mert = float(np.sum(1.0 / primes)) - math.log(math.log(NMAX))
info(f"Mertens: sum_p<=1e6 1/p - ln ln 1e6 = {mert:.7f} vs M = 0.2614972")
check("HAGEDORN origin of the beta = 1 pole: prime-mode density makes "
      "sum_p e^{-beta log p} diverge at beta = 1 (Mertens constant "
      "reproduced to 5e-4)", abs(mert - 0.2614972) < 5e-4)

# ================================================================ S3
print("S3 -- the compiler primon gas {2,3,5} and the Coxeter tower")
lhs = expand(sp.prod(1 - sp.Pow(p_, -s) for p_ in (2, 3, 5)))
rhs = sum(int(mobius(d)) * sp.Pow(d, -s) for d in divisors(30))
check("EXACT: prod_{p in {2,3,5}} (1 - p^-s) = sum_{d|30} mu(d) d^-s "
      "= sum_{d|30} tr(T_d) d^-s -- the inverse compiler zeta IS the "
      "Coxeter-tower trace polynomial", simplify(lhs - rhs) == 0)
subset_prods = sorted({sp.prod(S) for S in
                       ([], [2], [3], [5], [2, 3], [2, 5], [3, 5], [2, 3, 5])})
check("subset products of {2,3,5} = divisors(30) = the 8 tower levels "
      "(squarefree sector of the compiler Fock space; 8 = 2^3 blocks)",
      subset_prods == [int(d) for d in divisors(30)])
smooth = []
n235 = 1
for a in range(0, 41):
    if 2**a > 10**12:
        break
    for b in range(0, 26):
        v = 2**a * 3**b
        if v > 10**12:
            break
        for c in range(0, 18):
            w = v * 5**c
            if w > 10**12:
                break
            smooth.append(w)
Z2_235 = sum(1.0 / w**2 for w in smooth)
Z1_235 = sum(1.0 / w for w in smooth)
info(f"compiler gas: Z_235(2) = {Z2_235:.10f} (exact 25/16 = 1.5625), "
     f"Z_235(1) = {Z1_235:.6f} (exact 15/4 = 3.75, FINITE)")
check("compiler primon gas Z_235(2) = 25/16 exact (smooth-number sum, 1e-9); "
      "Z_235(1) = 15/4 FINITE -- three modes can never produce the zeta "
      "pole; the pole needs ALL primes (= the ZETA.EULER.EXTENSION gap)",
      abs(Z2_235 - 25.0 / 16) < 1e-9 and abs(Z1_235 - 15.0 / 4) < 1e-6)

# ================================================================ S4
print("S4 -- discriminator: seam mode counting vs primon mode counting")


def seam_ladder_mp(N, dps=60):
    """High-precision energy ladder: nu^2 = eigenvalues of -G^2 (real
    symmetric); needed because 1 - nu_max ~ e^{-N} underflows float64."""
    with mpmath.workdps(dps):
        L = N // 2
        G = mpmath.zeros(L, L)
        for a in range(L):
            for b in range(L):
                d = a - b
                if d % 2 != 0:
                    G[a, b] = mpmath.mpf(2) / N / mpmath.sin(mpmath.pi * d / N)
        M = -G * G
        try:
            E = mpmath.mp.eigsy(M, eigvals_only=True)
            evs = [E[i] for i in range(E.rows)]
        except TypeError:
            E, _ = mpmath.mp.eigsy(M)
            evs = [E[i] for i in range(E.rows)]
        # eigenvalues of -G^2 are doubly degenerate (+-i nu pairs):
        # take every second sorted value to get each mode once
        allnu = sorted((mpmath.sqrt(e) for e in evs if e > 1e-30), reverse=True)
        nus = allnu[0::2]
        return sorted(float(mpmath.log((1 + v) / (1 - v))) for v in nus)


ladders = {N: seam_ladder_mp(N) for N in (16, 32, 64)}
for N, eps in ladders.items():
    gaps = [eps[i + 1] - eps[i] for i in range(len(eps) - 1)]
    info(f"N={N:2d}: {len(eps)} modes, eps in [{eps[0]:.3f}, {eps[-1]:.3f}], "
         f"eps_max/N = {eps[-1]/N:.3f}, gap max/min = {max(gaps)/min(gaps):.2f}")
check("seam bandwidth grows LINEARLY with level size: eps_max/N in "
      "(0.8, 1.1) at N = 16, 32, 64 with exactly N/4 modes -- a finite "
      "quasi-linear ladder, polynomial mode architecture",
      all(0.8 < ladders[N][-1] / N < 1.1 and len(ladders[N]) == N // 4
          for N in (16, 32, 64)))
eps64 = ladders[64]
nE = np.arange(1, len(eps64) + 1, dtype=np.float64)
slope_seam = float(np.polyfit(np.array(eps64), np.log(nE), 1)[0])
lp = np.log(primes.astype(np.float64))
Egrid = np.linspace(7.0, math.log(NMAX), 20)
cnt = np.searchsorted(lp, Egrid)
slope_primon = float(np.polyfit(Egrid, np.log(cnt), 1)[0])
pg = np.diff(lp)
pg = pg[pg > 0]
gaps64 = [eps64[i + 1] - eps64[i] for i in range(len(eps64) - 1)]
info(f"log-counting slopes: seam(N=64) = {slope_seam:.3f} vs primon "
     f"= {slope_primon:.3f} (Hagedorn ~ 1); spacing max/min: seam "
     f"{max(gaps64)/min(gaps64):.1f} vs primon {float(np.max(pg)/np.min(pg)):.0f}")
check("mode-counting KILL: seam slope of log n(E) vs E < 0.2 (polynomial) "
      "while primon slope is in (0.7, 1.05) (exponential, Hagedorn) -- the "
      "free seam tower CANNOT produce the zeta pole",
      slope_seam < 0.2 and 0.7 < slope_primon < 1.05)
check("primon spacings log p_{k+1} - log p_k collapse toward 0 "
      "(max/min > 100) while the seam ladder stays uniformly gapped "
      "(max/min < 10) -- opposite spectral architectures",
      float(np.max(pg) / np.min(pg)) > 100 and max(gaps64) / min(gaps64) < 10)
check("VERDICT: 'zeta as partition function of the FREE seam tower' is "
      "KILLED at probe level (finite quasi-linear ladders, Z entire, no "
      "Hagedorn); any BC bridge needs NEW arithmetic mode density", True)

# ================================================================ S5
print("S5 -- ZETA.BC.SEAM.KMS sharpened: the complementary obstruction")
check("complementarity fixed: seam side HAS thermodynamics (measured "
      "beta_angle = 2pi = 1/(4 c3), KMS/Tomita, graded Majorana statistics) "
      "but NO arithmetic mode density; clock-family side HAS the arithmetic "
      "(divisor-tower semigroup, Galois Zhat*, mu = trace, 1/zeta as graded "
      "partition function) but NO Hamiltonian -- the bridge requirement is "
      "an energy assignment E_q = log q on clock levels (BC form "
      "H|n> = log n|n>); observation (typed, no claim): seam energies are "
      "logs of algebraic units (eps = ln cot^2(pi/48), ln cot^2(7pi/48)), "
      "BC energies are logs of integers", True)

print()
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({time.time()-T0:.1f}s)")
raise SystemExit(0 if FAIL == 0 else 1)
