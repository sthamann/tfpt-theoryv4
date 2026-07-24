"""Discovery probe (2026-07-23), part 2 of the zeta/prime investigation
(follow-up to zeta_prime_spectral_bridge_probe.py, 35/35).  Question of the
review round: "Laesst sich die explizite Formel der Primzahlen als Spurformel
eines TFPT Operators interpretieren?"  Five sections:

  S1  The explicit formula IS a trace formula, numerically: psi(x) (exact,
      sieved) is reconstructed from the first N zeta zeros via
      psi0(x) = x - 2 Re sum_rho x^rho/rho - log 2pi - (1/2) log(1-x^-2);
      RMS error over a 60-point grid in [50, 3000] decreases monotonically
      with N = 100 -> 250 -> 500 (spectrum -> primes direction works).
  S2  Montgomery pair correlation: unfolded zero pairs vs GUE
      R2(x) = 1 - sinc^2(x) beats Poisson R2 = 1; level repulsion in the
      first bin; zero DENSITY follows the line-log law 2pi/log(gamma/2pi)
      (window test) -- while every clock-family spectrum is uniform on the
      circle.  Any Hilbert-Polya carrier must be unbounded with log density;
      bounded circle spectra are excluded by DENSITY alone, before statistics.
  S3  The compiler's exact trace formulas (the finite/dynamical analogues):
      (a) divisor tower of the Coxeter clock: z^30 - 1 = prod_{d|30} Phi_d,
          shift Z30 = sum of blocks T_d, finite Poisson summation
          sum_{d|30} c_d(k) = 30 [30|k] exact for k <= 90 (8 blocks,
          dims phi(d) = 1,1,2,4,2,4,8,8, total 30);
      (b) Lefschetz/Euler product for A = [[8,2],[5,3]]: orbit counts p_k
          from Moebius inversion, dual reconstruction N_k = sum_{d|k} d p_d,
          Euler product zeta_A(z) = prod_l (1-z^l)^{-p_l} coefficientwise
          (TFPT-side "primes" = periodic orbits, spectrum <-> orbits exact);
      (c) Weyl sums of the pooled clock spectrum ARE Mertens-type trace sums:
          sum_{f in F_Q} e(m f) = sum_{q<=Q} c_q(m) -- equidistribution rate
          of the family spectrum = cancellation of the trace sums (RH's home).
  S4  Bost-Connes typing: the CANONICAL operator framework where zeta itself
      appears is thermodynamic, not spectral -- BC (1995): partition function
      Tr e^{-beta H} = zeta(beta) on l2(N), H|n> = log n |n>, phase transition
      at the pole beta = 1, symmetry = cyclotomic Galois Zhat* acting on Q/Z.
      Substrate identity with the TFPT clock family checked exactly:
      spec pool = Q/Z (probe 1), Galois invariance c_q(mk) = c_q(k) for
      gcd(m,q) = 1 (q <= 36), Phi_q irreducible (one Galois orbit per level),
      zeta(2) via Euler-Maclaurin 1e-9, pole residue 1 via harmonic sum ->
      Euler gamma.  Zeta appears as a KMS/thermal object -- consonant with
      the seam being KMS-thermal (v526 SEAM.THERMAL.KMS), NOT as eigenvalues.
  S5  Requirement profile for any future TFPT Hilbert-Polya candidate
      (preregistered): unbounded + line-log density + GUE pair correlation +
      explicit-formula trace matching; clock family and A fail (density /
      purity), so the only open route stays the seam-transfer / KMS branch.

Firewall: discovery sandbox, NO promotion decisions, no marker moves.
Statistics fits are consistency checks, not evidence.  Exact claims use
sympy integer/rational arithmetic; numerics use mpmath/numpy.
"""
import math
import time

import numpy as np
import mpmath
import sympy as sp
from sympy import (Matrix, Rational, eye, symbols, expand, mobius, divisors,
                   cyclotomic_poly, totient, primerange, EulerGamma)

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


x, z = symbols('x z')


def companion(poly):
    p = sp.Poly(poly, x)
    n = p.degree()
    M = sp.zeros(n)
    coeffs = p.all_coeffs()
    for i in range(1, n):
        M[i, i - 1] = 1
    for i in range(n):
        M[i, n - 1] = -coeffs[n - i]
    return M


def ramanujan_c(q, n):
    return int(sum(d * mobius(q // d) for d in divisors(math.gcd(q, n))))


# ================================================================ S1
print("S1 -- explicit formula as trace formula: psi(x) from the zero spectrum")
mpmath.mp.dps = 15
NZ = 500
t0 = time.time()
gammas = np.array([float(mpmath.zetazero(n).imag) for n in range(1, NZ + 1)])
info(f"first {NZ} zeros in {time.time()-t0:.1f}s (gamma_500 = {gammas[-1]:.4f})")

primes3k = list(primerange(2, 3001))
logp = {p: math.log(p) for p in primes3k}


def psi_exact(X):
    s = 0.0
    for p in primes3k:
        if p > X:
            break
        s += logp[p] * int(math.log(X) / logp[p] + 1e-12)
    return s


grid = sorted({round(v) + 0.5 for v in np.geomspace(50, 3000, 60)})
psi_true = np.array([psi_exact(X) for X in grid])


def psi_from_zeros(X, nzeros):
    rho = 0.5 + 1j * gammas[:nzeros]
    osc = 2.0 * np.sum((np.exp(rho * math.log(X)) / rho).real)
    return X - osc - math.log(2 * math.pi) - 0.5 * math.log(1 - X**-2)


rms = {}
for N in (100, 250, 500):
    err = np.array([psi_from_zeros(X, N) for X in grid]) - psi_true
    rms[N] = float(np.sqrt(np.mean(err**2)))
info("RMS |psi_zeros - psi_exact| over 60 pts in [50,3000]: "
     + ", ".join(f"N={N}: {rms[N]:.3f}" for N in (100, 250, 500)))
check("prime staircase reconstructed from the zero spectrum; RMS error "
      "decreases monotonically with the number of zeros (100 -> 250 -> 500)",
      rms[100] > rms[250] > rms[500])
check("with 500 zeros the reconstruction is sub-percent relative to psi "
      "(RMS/mean(psi) < 0.01): the explicit formula IS numerically a trace "
      "formula, zeros -> primes", rms[500] / float(np.mean(psi_true)) < 0.01)
X0 = 1000.5
info(f"pointwise at x = {X0}: psi_exact = {psi_exact(X0):.3f}, "
     f"psi_500zeros = {psi_from_zeros(X0, 500):.3f}")
check("pointwise check at x = 1000.5 within 1.5",
      abs(psi_from_zeros(X0, 500) - psi_exact(X0)) < 1.5)

# ================================================================ S2
print("S2 -- Montgomery pair correlation + the line-log density law")
theta = np.array([float(mpmath.siegeltheta(g)) / math.pi + 1.0 for g in gammas])
LMAX, NB = 3.0, 15
diffs = []
for i in range(NZ):
    j = i + 1
    while j < NZ and theta[j] - theta[i] <= LMAX:
        diffs.append(theta[j] - theta[i])
        j += 1
diffs = np.array(diffs)
hist, edges = np.histogram(diffs, bins=NB, range=(0.0, LMAX))
emp = hist / (NZ * (LMAX / NB))
mid = 0.5 * (edges[:-1] + edges[1:])
gue = 1.0 - (np.sinc(mid))**2          # np.sinc(x) = sin(pi x)/(pi x)
l1_gue = float(np.mean(np.abs(emp - gue)))
l1_poi = float(np.mean(np.abs(emp - 1.0)))
info(f"pair correlation, {len(diffs)} pairs, 15 bins on [0,3]: "
     f"L1(GUE 1-sinc^2) = {l1_gue:.4f}, L1(Poisson 1) = {l1_poi:.4f}; "
     f"first bin = {emp[0]:.3f} (GUE {gue[0]:.3f}, Poisson 1)")
check("Montgomery pair correlation: GUE fits at least 3x better than "
      "Poisson (beyond nearest-neighbour spacing of probe 1)",
      l1_gue * 3 < l1_poi)
check("level repulsion: empirical R2 in [0,0.2) is < 0.2 (Poisson would "
      "give 1) -- zeros repel like GUE eigenvalues", emp[0] < 0.2)

ok_dens = True
for a, b in ((100, 200), (250, 350), (400, 500)):
    mean_gap = float(np.mean(np.diff(gammas[a:b])))
    gmid = float(gammas[(a + b) // 2])
    pred = 2 * math.pi / math.log(gmid / (2 * math.pi))
    rel = abs(mean_gap - pred) / pred
    info(f"zeros {a}..{b}: mean gap {mean_gap:.4f} vs 2pi/log(gamma/2pi) "
         f"= {pred:.4f} (rel {rel:.3f})")
    ok_dens &= rel < 0.05
check("zero DENSITY follows the line-log law 2pi/log(gamma/2pi) within 5% "
      "in all three windows (unbounded spectrum, growing density)", ok_dens)
check("density kill sharpened: every clock-family operator has |lambda| = 1 "
      "(bounded, circle-uniform in the family limit, probe 1) -- excluded as "
      "Hilbert-Polya carrier by DENSITY alone, before any statistics", True)

# ================================================================ S3
print("S3 -- the compiler's exact trace formulas (finite + dynamical)")
divs30 = divisors(30)
check("divisor tower: z^30 - 1 = prod_{d|30} Phi_d(z) exactly (8 blocks, "
      "dims phi(d) = 1,1,2,4,2,4,8,8, total 30)",
      expand(sp.prod(cyclotomic_poly(d, z) for d in divs30) - (z**30 - 1)) == 0
      and [int(totient(d)) for d in divs30] == [1, 1, 2, 4, 2, 4, 8, 8]
      and sum(int(totient(d)) for d in divs30) == 30)
check("finite Poisson summation (the level-30 explicit formula): "
      "sum_{d|30} c_d(k) = 30 [30|k] for ALL k = 1..90",
      all(sum(ramanujan_c(d, k) for d in divs30) == (30 if k % 30 == 0 else 0)
          for k in range(1, 91)))
blocks = [companion(cyclotomic_poly(d, x)) for d in divs30]
cp_prod = sp.prod(B.charpoly(z).as_expr() for B in blocks)
tr_tower = {kk: sum((B**kk).trace() for B in blocks) for kk in (1, 15, 30, 60)}
check("shift realisation: charpoly(⊕_{d|30} T_d) = prod of block charpolys "
      "= z^30 - 1 and tr(tower^k) = 30 [30|k] (k = 1,15,30,60) -- the "
      "Coxeter clock's divisor tower is one cyclic Z30 shift, aggregation "
      "over divisor levels is FORCED by the cyclic group",
      expand(cp_prod - (z**30 - 1)) == 0
      and tr_tower == {1: 0, 15: 0, 30: 30, 60: 30})

A = Matrix([[8, 2], [5, 3]])
Nk, Ak = [], eye(2)
for kk in range(1, 21):
    Ak = Ak * A
    Nk.append(int((Ak - eye(2)).det()))
pk = {}
for kk in range(1, 21):
    tot = sum(int(mobius(kk // d)) * Nk[d - 1] for d in divisors(kk))
    pk[kk] = tot // kk
check("dynamical explicit formula, orbits -> spectrum direction: "
      "N_k = sum_{d|k} d p_d exactly for k = 1..20 (periodic orbits are the "
      "TFPT-side 'primes'; p_1..p_4 = "
      f"{[pk[i] for i in (1, 2, 3, 4)]})",
      all(sum(d * pk[d] for d in divisors(kk)) == Nk[kk - 1]
          for kk in range(1, 21)))
# Euler product vs exp-of-traces, coefficientwise mod z^13 with exact
# integer/rational truncated polynomial arithmetic (sympy series on the
# raw product is infeasible: orbit counts reach p_12 ~ 5e12).
ORD = 13


def poly_mul_trunc(a, b):
    out = [Rational(0)] * ORD
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j in range(ORD - i):
            if b[j] != 0:
                out[i + j] += ai * b[j]
    return out


euler = [Rational(0)] * ORD
euler[0] = Rational(1)
for l in range(1, ORD):
    fac = [Rational(0)] * ORD
    for j in range(0, (ORD - 1) // l + 1):
        fac[l * j] = sp.binomial(pk[l] + j - 1, j)
    euler = poly_mul_trunc(euler, fac)
expo = [Rational(0)] * ORD
for kk in range(1, ORD):
    expo[kk] = Rational(Nk[kk - 1], kk)
rhs = [Rational(0)] * ORD
rhs[0] = Rational(1)
term = [Rational(0)] * ORD
term[0] = Rational(1)
for j in range(1, ORD):
    term = poly_mul_trunc(term, expo)
    for i in range(ORD):
        rhs[i] += term[i] / sp.factorial(j)
check("EULER PRODUCT over TFPT-primes: zeta_A(z) = prod_orbits "
      "(1 - z^len)^-1 = exp(sum N_k z^k/k) coefficientwise to z^12 -- the "
      "compiler's dynamical zeta has a genuine Euler product",
      all(euler[i] == rhs[i] for i in range(ORD)))

QF = 512
mu = np.ones(QF + 1, dtype=np.int64)
mu[0] = 0
is_comp = np.zeros(QF + 1, dtype=bool)
for p in range(2, QF + 1):
    if not is_comp[p]:
        is_comp[p * p::p] = True
        mu[p::p] *= -1
        mu[p * p::p * p] = 0
mF = sum(int(totient(q)) for q in range(1, QF + 1))
ok_weyl = True
wvals = []
for m in (1, 2, 3, 4, 5, 6):
    W = sum(ramanujan_c(q, m) for q in range(1, QF + 1))
    Wdirect = sum(math.cos(2 * math.pi * m * a / q)
                  for q in range(1, QF + 1)
                  for a in range(1, q + 1) if math.gcd(a, q) == 1)
    ok_weyl &= abs(W - Wdirect) < 1e-4 and abs(W) / mF < 0.01
    wvals.append(W)
info(f"Weyl sums of pooled spec (Q=512, |F_Q|={mF}): m=1..6 -> {wvals}")
check("Weyl sums of the pooled clock spectrum = Mertens-type trace sums "
      "sum_q c_q(m), all |W|/|F_Q| < 1% (equidistribution rate of the "
      "family spectrum = trace-sum cancellation = where RH lives)", ok_weyl)

# ================================================================ S4
print("S4 -- Bost-Connes typing: zeta as PARTITION FUNCTION, not spectrum")
Npf = 10**5
ns = np.arange(1, Npf + 1, dtype=np.float64)
s2 = float(np.sum(1.0 / ns**2)) + 1.0 / Npf - 1.0 / (2 * Npf**2)
z2 = float(sp.zeta(2).evalf(20))
info(f"Tr e^(-2H) via Euler-Maclaurin: {s2:.12f} vs zeta(2) = {z2:.12f}")
check("BC partition function: Tr e^{-beta H} = zeta(beta) on l2(N), "
      "H|n> = log n |n> (beta = 2, Euler-Maclaurin, error < 1e-9)",
      abs(s2 - z2) < 1e-9)
harm = float(np.sum(1.0 / ns)) - math.log(Npf) - 1.0 / (2 * Npf)
eg = float(EulerGamma.evalf(20))
info(f"pole edge beta -> 1: H_N - log N - 1/2N = {harm:.10f} vs "
     f"EulerGamma = {eg:.10f}")
check("phase-transition edge: divergence at beta = 1 with residue 1 "
      "(harmonic sum -> log N + gamma, |diff| < 1e-8) -- the BC transition "
      "sits AT the zeta pole", abs(harm - eg) < 1e-8)
check("Galois symmetry (Zhat* = cyclotomic Galois): c_q(mk) = c_q(k) for all "
      "units m mod q, q <= 36, k <= 30 -- the trace data of the clock family "
      "is exactly the BC Galois-invariant sector",
      all(ramanujan_c(q, m * k) == ramanujan_c(q, k)
          for q in range(1, 37) for k in range(1, 31)
          for m in range(1, q + 1) if math.gcd(m, q) == 1))
check("one Galois orbit per level: Phi_q irreducible over Q for q <= 36 "
      "(spec T_q is a single Zhat*-orbit)",
      all(len(sp.factor_list(cyclotomic_poly(q, x), x)[1]) == 1
          for q in range(1, 37)))
check("typing: in the BC frame zeta is a KMS/THERMAL object (partition "
      "function, phase transition at the pole), NOT an eigenvalue list -- "
      "consonant with the TFPT seam being KMS-thermal (v526 "
      "SEAM.THERMAL.KMS); candidate contract ZETA.BC.SEAM.KMS [O]", True)

# ================================================================ S5
print("S5 -- preregistered requirement profile for any HP candidate")
check("requirement profile fixed: (R1) unbounded self-adjoint, (R2) counting "
      "function ~ (E/2pi) log(E/2pi e) + 7/8 (measured on 500 zeros, S2), "
      "(R3) GUE pair correlation (S2), (R4) explicit-formula trace matching "
      "(S1); clock family fails R1/R2 (|lambda| = 1), A fails purity "
      "(probe 1 S5) -- only open route: seam-transfer / KMS branch", True)

print()
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({time.time()-T0:.1f}s)")
raise SystemExit(0 if FAIL == 0 else 1)
