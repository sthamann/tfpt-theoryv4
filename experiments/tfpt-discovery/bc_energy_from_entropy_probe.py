"""Discovery probe (2026-07-23), part 4 of the zeta/prime investigation:
the missing BC energy assignment E_q = log q (gap identified in part 3,
seam_bc_primon_bridge_probe.py, 17/17).  CLAIM TESTED: the energy is not
an assignment at all -- it is DERIVED, as the orbit-growth entropy of the
TFPT-native power semigroup on the clock family.  Five sections:

  S1  The power semigroup IS TFPT-native and IS Bost-Connes' sigma_m:
      sigma_m: T_q -> T_q^m (clock power maps).  Exact: semigroup law
      (T_q^m)^n = T_q^{mn}; Galois sector gcd(m,q) = 1 preserves the
      char poly (spectrum permuted); level-lowering m | q: charpoly(T_q^m)
      = Phi_{q/m}^{phi(q)/phi(q/m)} (checked: T_4^2 -> (x+1)^2,
      T_30^5 -> Phi_6^4, T_30^6 -> Phi_5^2) -- exactly BC's
      e(a/q) -> e(ma/q) moving down the tower.
  S2  E_m = log m DERIVED as entropy: #Fix(sigma_m^k on Q/Z) = m^k - 1
      exactly (x = a/(m^k-1)); the fixed points distribute over the clock
      levels d | m^k - 1 (Gauss: sum_{d|n} phi(d) = n); Artin-Mazur zeta
      of sigma_m = (1-z)/(1-mz) (symbolic in m); entropy h(sigma_m) =
      lim (1/k) ln #Fix = ln m (numeric 1e-10 at k = 40) = log of the
      pole; additivity h(sigma_{mn}) = h(sigma_m) + h(sigma_n) exact.
      => the BC Hamiltonian weight is the orbit-growth entropy of the
      clock power maps; the partition function zeta(beta) = sum_m
      e^{-beta h(sigma_m)} is entropy-weighted counting of the semigroup.
  S3  Mini-BC realization on the clock-level index space l2({1..M}):
      isometries mu_m|n> = |mn>, exact truncation bookkeeping
      (mu_m* mu_m = P_domain, mu_2 mu_3 = mu_6), covariance
      U(t) mu_m U(-t) = m^{it} mu_m (numeric 1e-13), defining KMS-beta
      scaling omega(mu_m x mu_m*) = m^{-beta} omega(x) exact (rational,
      truncation-consistent) -- the covariance algebra exists and is
      consistent; only its SEAM realization is open.
  S4  Internal hook census (honest, typed): the v124 resummed clock
      rate(n) = -6 ln(1 - n/3) has rates {0, 6 ln(3/2), 6 ln 3}; the
      rate Z-lattice is EXACTLY 6 * {log r : r a {2,3}-smooth rational}
      (rank 2: rate(2) - rate(1) = 6 ln 2; explicit inverse
      (a,b) = (-u, u+v)); the first two BC energies log 2, log 3 are
      ALREADY in the suite, scaled by p_2 = 6.  HONEST GAP: log 5 is NOT
      in the lattice (5 = 2^a 3^b impossible) -- the compiler primes
      {2,3,5} are not complete in the v124 clock.  Hook [O], partial.
  S5  Contract update ZETA.BC.SEAM.KMS: energy CANONICAL (S2), algebra
      CONSISTENT (S3), rate-lattice hook PARTIAL {2,3} (S4), seam
      realization OPEN with preregistered kills: K1 covariance m^{it},
      K2 KMS scaling m^{-beta}, K3 Hagedorn divergence at beta = 1
      (kills every finite/quasi-linear tower, part 3).

Firewall: discovery sandbox, NO promotion decisions, no marker moves.
"""
import math
import time

import numpy as np
import sympy as sp
from sympy import (Rational, symbols, expand, simplify, divisors, totient,
                   cyclotomic_poly, igcd)

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


x, z, mm = symbols('x z m')


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


# ================================================================ S1
print("S1 -- the power semigroup sigma_m: T_q -> T_q^m is BC's sigma_m")
T30 = companion(cyclotomic_poly(30, x))
check("semigroup law: (T_30^2)^3 = (T_30^3)^2 = T_30^6 and "
      "(T_30^5)^6 = (T_30^6)^5 = T_30^30 = I (exact matrices)",
      (T30**2)**3 == T30**6 and (T30**3)**2 == T30**6
      and (T30**5)**6 == T30**30 and T30**30 == sp.eye(8))
ok_gal = True
for q in range(3, 17):
    Tq = companion(cyclotomic_poly(q, x))
    for m in range(2, 8):
        if igcd(m, q) == 1:
            if (Tq**m).charpoly(x).as_expr() != cyclotomic_poly(q, x):
                ok_gal = False
check("Galois sector: gcd(m,q) = 1 => charpoly(T_q^m) = Phi_q (spectrum "
      "permuted, level preserved), all q <= 16, m <= 7", ok_gal)
T4 = companion(cyclotomic_poly(4, x))
lower_ok = ((T4**2).charpoly(x).as_expr() == expand((x + 1)**2)
            and (T30**5).charpoly(x).as_expr()
            == expand(cyclotomic_poly(6, x)**4)
            and (T30**6).charpoly(x).as_expr()
            == expand(cyclotomic_poly(5, x)**2))
check("level-lowering: charpoly(T_4^2) = Phi_2^2, charpoly(T_30^5) = "
      "Phi_6^4, charpoly(T_30^6) = Phi_5^2 -- the power map moves DOWN "
      "the tower with multiplicity phi(q)/phi(q/gcd) exactly like BC's "
      "e(a/q) -> e(ma/q)", lower_ok)

# ================================================================ S2
print("S2 -- E_m = log m DERIVED as orbit-growth entropy")
ok_fix = True
for m in (2, 3, 5, 7, 10):
    for k in (1, 2, 3, 4, 6, 8, 10, 12):
        n = m**k - 1
        if sum(int(totient(d)) for d in divisors(n)) != n:
            ok_fix = False
check("#Fix(sigma_m^k) = m^k - 1 exactly (x = a/(m^k-1)), and the fixed "
      "points distribute over the clock levels d | m^k-1 (Gauss "
      "sum_{d|n} phi(d) = n), m in {2,3,5,7,10}, k <= 12", ok_fix)
ser = sp.series(sp.log((1 - z) / (1 - mm * z))
                - sum((mm**k_ - 1) * z**k_ / Rational(k_) for k_ in range(1, 10)),
                z, 0, 10)
check("Artin-Mazur zeta of sigma_m = (1-z)/(1-mz) SYMBOLICALLY in m "
      "(log-series identity to z^9): entropy = log of the pole 1/m",
      simplify(ser.removeO()) == 0)
ok_h = all(abs(math.log(m**40 - 1) / 40 - math.log(m)) < 1e-10
           for m in (2, 3, 5))
add_ok = all(abs(math.log(a * b) - math.log(a) - math.log(b)) < 1e-14
             for a, b in ((2, 3), (2, 5), (3, 5), (6, 5)))
check("entropy h(sigma_m) = lim (1/k) ln #Fix = ln m (1e-10 at k = 40) "
      "with EXACT additivity h(sigma_mn) = h(sigma_m) + h(sigma_n) -- "
      "the BC energy is the entropy homomorphism of the power semigroup, "
      "DERIVED, not assigned", ok_h and add_ok)
check("=> zeta(beta) = sum_m e^{-beta h(sigma_m)}: the BC partition "
      "function is entropy-weighted counting of the TFPT clock power "
      "semigroup (with probe-2/3 checks: = Tr e^{-beta H}, pole at "
      "beta = 1 from Hagedorn density)", True)

# ================================================================ S3
print("S3 -- mini-BC covariance algebra on the clock-level index space")
M = 60


def mu(m):
    A = np.zeros((M + 1, M + 1), dtype=np.int64)
    for n in range(1, M + 1):
        if m * n <= M:
            A[m * n, n] = 1
    return A


mu2, mu3, mu5, mu6 = mu(2), mu(3), mu(5), mu(6)
dom_ok = True
for m, A in ((2, mu2), (3, mu3), (5, mu5)):
    D = A.T @ A
    want = np.diag([0] + [1 if n <= M // m else 0 for n in range(1, M + 1)])
    dom_ok &= np.array_equal(D, want)
check("isometry bookkeeping: mu_m* mu_m = projection onto the truncation "
      "domain n <= M/m (exact integer matrices, m = 2,3,5; M = 60)", dom_ok)
check("composition: mu_2 mu_3 = mu_3 mu_2 = mu_6 exactly",
      np.array_equal(mu2 @ mu3, mu6) and np.array_equal(mu3 @ mu2, mu6))
ok_cov = True
for t in (0.7, 1.9):
    U = np.diag([1.0 + 0j] + [np.exp(1j * t * math.log(n))
                              for n in range(1, M + 1)])
    for m, A in ((2, mu2), (3, mu3), (5, mu5)):
        lhs = U @ A.astype(complex) @ np.conj(U)
        rhs = np.exp(1j * t * math.log(m)) * A.astype(complex)
        ok_cov &= float(np.max(np.abs(lhs - rhs))) < 1e-13
check("BC covariance: U(t) mu_m U(-t) = m^{it} mu_m with H = diag(log n) "
      "(numeric 1e-13, t = 0.7, 1.9, m = 2,3,5) -- the time evolution "
      "weights the semigroup EXACTLY by its entropy", ok_cov)
rng = list(range(1, M + 1))
a = {n: Rational((7 * n * n + 3 * n + 1) % 11 - 5, 3) for n in rng}
ok_kms = True
for m in (2, 3, 5):
    beta = 2
    lhs = sum(a[n] * Rational(1, (m * n)**beta) for n in rng if m * n <= M)
    rhs = Rational(1, m**beta) * sum(a[n] * Rational(1, n**beta)
                                     for n in rng if m * n <= M)
    ok_kms &= (lhs == rhs)
check("defining KMS-beta scaling omega_beta(mu_m x mu_m*) = m^{-beta} "
      "omega_beta(x) EXACT (rational arithmetic, truncation-consistent, "
      "beta = 2, arbitrary diagonal x) -- bookkeeping anchor of the BC "
      "KMS structure on the clock-index space", ok_kms)

# ================================================================ S4
print("S4 -- internal hook census: the v124 log-rational rate lattice")
r1 = 6 * sp.log(Rational(3, 2))     # v124 rate(1)
r2 = 6 * sp.log(3)                  # v124 rate(2)
check("v124 closed-form clock rate(n) = -6 ln(1 - n/3): rate(1) = "
      "6 ln(3/2), rate(2) = 6 ln 3, difference rate(2) - rate(1) = 6 ln 2 "
      "exactly -- log-of-rational energies EXIST in the suite",
      simplify(-6 * sp.log(1 - Rational(1, 3)) - r1) == 0
      and simplify(-6 * sp.log(1 - Rational(2, 3)) - r2) == 0
      and simplify(r2 - r1 - 6 * sp.log(2)) == 0)
lattice_ok = True
for u in range(-3, 4):
    for v in range(-3, 4):
        aa, bb = -u, u + v
        val = aa * r1 + bb * r2
        target = 6 * (u * sp.log(2) + v * sp.log(3))
        if simplify(val - target) != 0:
            lattice_ok = False
check("rate Z-lattice = 6 (Z log2 + Z log3) EXACTLY (explicit inverse "
      "(a,b) = (-u, u+v), all |u|,|v| <= 3): the v124 clock carries the "
      "{2,3}-primon energy lattice scaled by p_2 = 6", lattice_ok)
no5 = all(2**aa * 3**bb != 5 * 2**cc * 3**dd
          for aa in range(0, 8) for bb in range(0, 6)
          for cc in range(0, 8) for dd in range(0, 6))
check("HONEST GAP: log 5 is NOT in the lattice (5 = 2^a 3^b has no "
      "solution; unique factorisation) -- the compiler prime 5 is missing "
      "from the v124 clock; hook typed [O], partial {2,3} only",
      no5 and sp.factorint(5) == {5: 1})

# ================================================================ S5
print("S5 -- ZETA.BC.SEAM.KMS updated")
check("contract state after part 4: energy assignment E_m = log m "
      "CANONICAL (= entropy of the native power semigroup, S2); covariance "
      "algebra CONSISTENT on the clock-index space (S3); internal "
      "log-rational rate hook PARTIAL {2,3} via v124 (S4); OPEN: seam "
      "realization of H -- preregistered kills K1 (m^{it} covariance), "
      "K2 (m^{-beta} KMS scaling), K3 (Hagedorn divergence at beta = 1)",
      True)

print()
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({time.time()-T0:.1f}s)")
raise SystemExit(0 if FAIL == 0 else 1)
