"""Discovery probe (2026-07-24), part 15 of the zeta/prime investigation.
Candidate research contract ZETA.ARITH.COMPLETION: construct, from the
finite compiler, a canonical infinite Hilbert space with basis |n>,
multiplication, and H = log n, WITHOUT writing N or the primes in by
hand.  Kill: if |n>, multiplication, or log n are merely DEFINITIONS,
nothing is explained.

  S1  OPERATOR-SIDE REACHABILITY CENSUS: starting from clock level 30
      (the E8 point of the clock family), close under suite-native
      operations -- divisors, products, lcm, power-semigroup level
      lowering sigma_m (m from existing levels), and tensor T_a (x) T_b
      (combined period = lcm).  Exact finite closure up to bound B:
      the reachable set equals the {2,3,5}-smooth integers <= B, and
      contains NO prime outside {2,3,5}.  Honest PARTIAL KILL of the
      naive reading "the compiler operators generate all of N".
  S2  LATTICE SIDE AS CANONICAL CANDIDATE: the E8 shell structure is
      lattice-intrinsic (no ad-hoc N).  Shell Hamiltonian on the
      counting space of E8 vectors: H|x> = log(|x|^2/2).  Exact shell
      multiplicities via direct enumeration (n <= 6, part-11 technique)
      equal 240 sigma3(n); numerical Tr e^{-s H} = 240 zeta(s) zeta(s-3)
      at s = 5, 6 against mpmath.  HONEST: multiplicities are
      240 sigma3(n), not 1 -- this is NOT the BC space l^2(N), but a
      different canonical all-primes object.  Missing (typed): a
      canonical factorisation of the shell space reducing multiplicity
      to 1, or Hecke structure as a multiplication substitute.
  S3  MULTIPLICATION-STRUCTURE TEST: weaker statement -- the counting
      function r(n) = 240 sigma3(n) satisfies the multiplicative law
      r(mn) * r(1) = r(m) * r(n) on coprime pairs (exact, m,n <= 50,
      mn <= 200, via sympy).  Multiplicativity (heart of the
      fundamental theorem) is already in the LATTICE COUNTING, not in
      the vectors.  Missing step (typed, not claimed): a tensor functor
      Shell(m) (x) Shell(n) -> Shell(mn).
  S4  VERDICT: ZETA.ARITH.COMPLETION is PARTIAL -- completion exists in
      TWO halves.  Operator side {2,3,5}-limited (S1 partial kill of
      naive all-N reading).  Counting side all-primes-canonical but
      multiplicity-laden ([O] narrowed to multiplicity-1 reduction /
      tensor functor).  Kill for the narrowed contract preregistered.

Firewall: discovery sandbox, NO promotion, no marker moves, no RH
evidence language; classical facts (Bost-Connes sigma_m, Hecke /
sigma3-multiplicativity, zeta(s)zeta(s-3) = Dirichlet series of
sigma3) named as classical -- probe content is the exact in-suite
typing of what the compiler already owns vs what it does not.
"""
import math
import time
from math import gcd

import numpy as np
import mpmath
import sympy as sp

PASS = 0
FAIL = 0
T0 = time.time()
mpmath.mp.dps = 40

BOUND = 10_000
SEED = 30
SMOOTH_PRIMES = (2, 3, 5)


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


def is_235_smooth(n):
    if n < 1:
        return False
    x = n
    for p in SMOOTH_PRIMES:
        while x % p == 0:
            x //= p
    return x == 1


def all_235_smooth_upto(B):
    out = []
    a = 1
    while a <= B:
        b = 1
        while a * b <= B:
            c = 1
            while a * b * c <= B:
                out.append(a * b * c)
                c *= 5
            b *= 3
        a *= 2
    return sorted(set(out))


def operator_closure(seed, B):
    """Finite closure under suite-native clock-level operations <= B.

    Operations (all TFPT-native / BC-native, parts 3-5):
      - divisors of a reachable level
      - products a*b of reachable levels (when <= B)
      - lcm(a,b) of reachable levels (tensor / combined period)
      - power-semigroup level-lowering: m|q with m,q reachable => q/m
        (already among divisors of q; kept explicit for typing)
    """
    reach = {seed}
    changed = True
    while changed:
        changed = False
        cur = list(reach)
        # divisors + sigma_m level-lowering
        for q in cur:
            for d in sp.divisors(q):
                if d not in reach and d <= B:
                    reach.add(d)
                    changed = True
            for m in cur:
                if m > 0 and q % m == 0:
                    q_over = q // m
                    if q_over not in reach and q_over <= B:
                        reach.add(q_over)
                        changed = True
        # products and lcm (= tensor period)
        for i, a in enumerate(cur):
            for b in cur[i:]:
                prod = a * b
                if prod <= B and prod not in reach:
                    reach.add(prod)
                    changed = True
                ell = math.lcm(a, b)
                if ell <= B and ell not in reach:
                    reach.add(ell)
                    changed = True
    return frozenset(reach)


# ================================================================ S1
print("S1 -- operator-side reachability census from level 30")
smooth = all_235_smooth_upto(BOUND)
reach = operator_closure(SEED, BOUND)
info(f"seed = {SEED}; bound = {BOUND}")
info(f"|reachable| = {len(reach)}; |{{2,3,5}}-smooth <= B| = {len(smooth)}")
info(f"reachable sample (first 20): {sorted(reach)[:20]}")
info(f"largest reachable: {max(reach)}")

check(f"closure equals the {{2,3,5}}-smooth integers <= {BOUND}: "
      f"|reach| = |smooth| = {len(smooth)}, set equality exact",
      reach == frozenset(smooth) and len(reach) == len(smooth))

outside_primes = [p for p in sp.primerange(2, min(BOUND, 200))
                  if p not in SMOOTH_PRIMES]
blocked = [p for p in outside_primes if p in reach]
info(f"outside primes <= 200 tested for membership: {outside_primes[:12]}..."
     f" ({len(outside_primes)} total); in closure: {blocked}")
check("PARTIAL KILL (naive all-N reading): NO prime outside {2,3,5} is "
      "reachable from level 30 by suite-native operations "
      "(divisors / products / lcm=tensor / sigma_m lowering) -- "
      "operator side produces only the {2,3,5}-adic completion "
      "(Z_2 x Z_3 x Z_5), not all of N",
      len(blocked) == 0 and all(is_235_smooth(n) for n in reach))

# concrete witnesses: powers and mixed smooths ARE generated
witnesses = [4, 8, 9, 12, 16, 18, 20, 24, 25, 27, 32, 36, 48, 50, 54, 75,
             81, 100, 125, 128, 243, 625, 1024, 3125, 7776]
wit_ok = all(w in reach for w in witnesses if w <= BOUND)
info(f"smooth witnesses present: {[w for w in witnesses if w <= BOUND][:10]}...")
check("constructive generation: products of {2,3,5} from divisors(30) "
      "build higher smooth levels (4,8,9,12,...,7776) -- the closure is "
      "not just the 8 squarefree divisors of 30, but the full "
      "{2,3,5}-smooth monoid truncated at B",
      wit_ok and 1 in reach and 7 not in reach and 11 not in reach)

# ================================================================ S2
print("S2 -- lattice side: shell Hamiltonian and 240 zeta(s) zeta(s-3)")

# Direct E8 enumeration for shells n = 1..6 (part-11 technique:
# integer + half-integer coordinate models in doubled coords)
rng7 = np.arange(-3, 4, dtype=np.int16)
gi = np.array(np.meshgrid(*[rng7] * 8, indexing="ij")).reshape(8, -1).T
ni = np.einsum("ij,ij->i", gi.astype(np.int32), gi.astype(np.int32))
mi = (gi.astype(np.int32).sum(axis=1) % 2 == 0) & (ni >= 2) & (ni <= 12)
n_i = ni[mi] // 2
rng6 = np.array([-5, -3, -1, 1, 3, 5], dtype=np.int16)
gh = np.array(np.meshgrid(*[rng6] * 8, indexing="ij")).reshape(8, -1).T
nh = np.einsum("ij,ij->i", gh.astype(np.int32), gh.astype(np.int32))
mh = (gh.astype(np.int32).sum(axis=1) % 4 == 0) & (nh <= 48)
n_h = nh[mh] // 8
nsh = np.concatenate([n_i, n_h])
shell_counts = {n: int(np.sum(nsh == n)) for n in range(1, 7)}
sig3 = {n: int(sp.divisor_sigma(n, 3)) for n in range(1, 7)}
expected = {n: 240 * sig3[n] for n in range(1, 7)}
info(f"enumerated N(2n) for n=1..6: "
     f"{[shell_counts[n] for n in range(1, 7)]}")
info(f"240*sigma3(n) for n=1..6: "
     f"{[expected[n] for n in range(1, 7)]}")
check("lattice-intrinsic shell multiplicities (direct E8 enumeration, "
      "n <= 6): N(2n) = 240 sigma3(n) EXACT -- shells know ALL primes "
      "via classical sigma3 (Jacobi), with NO ad-hoc writing of N; "
      f"counts = { [shell_counts[n] for n in range(1, 7)] }",
      all(shell_counts[n] == expected[n] for n in range(1, 7)))

# Shell Hamiltonian H|x> = log(|x|^2/2) = log n on shell n
# Tr e^{-s H} = sum_{n>=1} N(2n) n^{-s} = 240 zeta(s) zeta(s-3)
# Tail of sum sigma3(n) n^{-s} is O(N^{4-s}); s=5 needs N ~ 1e6 for 1e-6.
N_DIR = 2_000_000


def sigma3_sieve(N):
    s = np.zeros(N + 1, dtype=np.int64)
    for d in range(1, N + 1):
        d3 = d * d * d
        s[d::d] += d3
    return s


sig3_big = sigma3_sieve(N_DIR)
# sanity vs sympy on a sample
assert all(int(sig3_big[n]) == int(sp.divisor_sigma(n, 3))
           for n in (1, 2, 3, 6, 12, 30, 60, 210, 720, 5040))


def dirichlet_shell(s, N=N_DIR):
    # float64 is enough for the relative-error check at s >= 5
    n = np.arange(1, N + 1, dtype=np.float64)
    return float(np.sum(240.0 * sig3_big[1:].astype(np.float64) * n ** (-s)))


def closed_form(s):
    return 240 * mpmath.zeta(s) * mpmath.zeta(s - 3)


for s_val in (5, 6):
    direct = dirichlet_shell(s_val)
    closed = float(closed_form(s_val))
    rel = abs(direct - closed) / abs(closed)
    info(f"s = {s_val}: direct(N={N_DIR}) = {direct:.10f}; "
         f"240*zeta({s_val})*zeta({s_val - 3}) = {closed:.10f}; "
         f"rel err = {rel:.2e}")
    check(f"Tr e^{{-{s_val} H}} = sum_n 240 sigma3(n) n^{{-{s_val}}} "
          f"= 240 zeta({s_val}) zeta({s_val - 3}) (mpmath; relative "
          f"truncation error < 1e-6 at N = {N_DIR})",
          rel < 1e-6)

# Honest typing: NOT l^2(N)
r1, r2, r3 = expected[1], expected[2], expected[3]
check("HONEST GAP typed: shell multiplicities are 240*sigma3(n), NOT 1 "
      f"(r(1)={r1}, r(2)={r2}, r(3)={r3}) -- the shell space is NOT "
      "the BC space l^2(N); it is a DIFFERENT canonical all-primes "
      "object.  Missing for ZETA.ARITH.COMPLETION: a canonical "
      "factorisation reducing multiplicity to 1, OR Hecke structure "
      "as a multiplication substitute",
      r1 == 240 and r2 == 2160 and r3 == 6720 and r1 != 1)

# ================================================================ S3
print("S3 -- multiplicativity of the shell counting function")
pairs = [(m, n) for m in range(1, 51) for n in range(1, 51)
         if m * n <= 200 and gcd(m, n) == 1]
r = {k: 240 * int(sp.divisor_sigma(k, 3)) for k in range(1, 201)}
mult_ok = all(r[m * n] * r[1] == r[m] * r[n] for m, n in pairs)
# classical control: sigma3 itself is multiplicative (sigma3(1)=1)
s3_ok = all(int(sp.divisor_sigma(m * n, 3))
            == int(sp.divisor_sigma(m, 3)) * int(sp.divisor_sigma(n, 3))
            for m, n in pairs)
info(f"coprime pairs tested: {len(pairs)} (m,n <= 50, mn <= 200)")
info(f"law checked: r(mn)*r(1) = r(m)*r(n) with r(1) = {r[1]} "
     f"(equivalently sigma3 multiplicative -- classical)")
# sample
samples = [(1, 1), (2, 3), (4, 5), (8, 9), (7, 11), (15, 8), (25, 7)]
for m, n in samples:
    if gcd(m, n) == 1 and m * n <= 200:
        info(f"  r({m})*r({n})/r(1) = {r[m] * r[n] // r[1]} = r({m * n})")
check(f"shell counting r(n) = 240 sigma3(n) obeys r(mn)*r(1) = r(m)*r(n) "
      f"on ALL {len(pairs)} coprime pairs with m,n <= 50, mn <= 200 "
      "(exact sympy) -- multiplicativity of the FUNDAMENTAL THEOREM is "
      "already present in the lattice COUNTING (classical sigma3), "
      "not as a vector-space tensor on shells",
      mult_ok and s3_ok and r[1] == 240)

check("MISSING STEP typed (not claimed): a tensor functor "
      "Shell(m) (x) Shell(n) -> Shell(mn) that realises the counting "
      "multiplicativity on the VECTOR space -- counting alone does not "
      "supply the BC multiplication operators mu_k |n> = |kn|",
      True)

# ================================================================ S4
print("S4 -- verdict typing for ZETA.ARITH.COMPLETION")
check("VERDICT = PARTIAL: completion exists in TWO halves -- "
      "(i) operator side {2,3,5}-limited (S1 partial kill of naive "
      "all-N reading); (ii) lattice counting side all-primes-canonical "
      "via E8 shells but multiplicity-laden.  Contract [O] NARROWED to: "
      "multiplicity-1 reduction of the shell space / tensor functor "
      "Shell(m)(x)Shell(n)->Shell(mn) (or Hecke multiplication "
      "substitute)",
      reach == frozenset(smooth) and r1 == 240 and mult_ok)

check("preregistered KILL for the narrowed contract: if the only "
      "multiplicity-1 model is obtained by QUOTIENTING the shell space "
      "by an ad-hoc 'pick one vector per shell' section that writes N "
      "in by hand, OR if the tensor functor requires an external "
      "identification Shell(n) ~= C^{240 sigma3(n)} with no "
      "lattice-intrinsic factorisation, then the narrowed "
      "ZETA.ARITH.COMPLETION is KILLED -- no explanation gained "
      "(same kill spirit as the original contract)",
      True)

check("global consistency: operator closure = {2,3,5}-smooth; "
      "shell N(2n) = 240 sigma3(n) for n <= 6; Dirichlet = "
      "240 zeta zeta at s = 5,6; counting multiplicativity holds; "
      "NO claim that |n> / mu_k / log n have been derived -- "
      "classical Bost-Connes / Hecke / sigma3 facts named as such",
      reach == frozenset(smooth)
      and all(shell_counts[n] == expected[n] for n in range(1, 7))
      and mult_ok)

print()
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({time.time() - T0:.1f}s)")
raise SystemExit(0 if FAIL == 0 else 1)
