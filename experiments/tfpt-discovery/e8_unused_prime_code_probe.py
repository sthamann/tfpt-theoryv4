"""Discovery probe (2026-07-23), part 6 of the zeta/prime investigation.
User question: large parts of E8 seem unmapped by the theory -- nature is
not wasteful; does the 'unused' part correlate with the prime theme, and
could the primes be a kind of ERROR CODE?  Made falsifiable:

  S1  Exact inventory: 240 roots split under the compiler subalgebra
      D5 (+) A3 as 40 + 12 + 60 + 128 (= (10,6) + (16,4) + (16bar,4bar));
      248 = 45 + 15 + 60 + 64 + 64.  The 188 'unused' root directions are
      the coset -- tfpt_1 already assigns them (matter spinors x mu4,
      decuple x Z6); this probe adds the exact arithmetic function.
  S2  THE GLUE IS mu4, EXACTLY: index [E8 : D5(+)A3] = 4 with Smith
      normal form (1,...,1,4) => quotient is CYCLIC Z4 = mu4 (not
      Z2 x Z2).  Root grading under the glue map: grade 0 = 52 (D5+A3),
      grade 2 = 60 (10,6), grades 1/3 = 64/64 (the two spinor sheets) --
      the 'unused' 188 are exactly the nontrivial mu4-glue classes: the
      axiom 'D5 (+) A3 + mu4 => E8' read backwards.
  S3  ERROR CODE, LITERAL: the extended Hamming code [8,4,4] (= RM(1,3),
      the paradigmatic 1-error-correcting code): 16 codewords, self-dual,
      doubly even, weight enumerator 1 + 14 y^4 + y^8; Construction A
      lifts it to the E8 lattice: 240 roots = 16 (from 2Z^8) + 14 x 2^4
      (from the weight-4 codewords) -- E8 IS the lattice lift of an
      error-correcting code (theorem, verified constructively).
      Observation (typed, no claim): 14 weight-4 words = det A = dim G2.
  S4  WHERE THE PRIMES ENTER: the E8 theta counting N(2n) = 240 sigma3(n)
      (direct enumeration n = 1..6: 240, 2160, 6720, 17520, 30240, 60480);
      sigma3 is MULTIPLICATIVE (Euler product; sigma3(6) = 9*28 = 252 =
      the v532 dual product); Dirichlet series sum sigma3(n)/n^s =
      zeta(s) zeta(s-3) (numeric s = 5); exact multiplicativity identity
      N(4) N(6) = N(12) N(2) for E8.  KILL CONTRAST: the same identity
      FAILS for the D5(+)A3 sublattice alone -- without the 188 glue
      roots the prime/Euler structure of the counting BREAKS.  Answer to
      the user question: the 'unused' part is exactly (a) the mu4 glue
      and (b) the modular completion that couples E8 to the primes.
  S5  CARRIER.SATURATION.LOG census (the executable proxy of the D5 kill
      test): saturation-class candidates (p/q) * b^{+-1}, b in
      {(5/4)^20, (5/3)^20, (5/2)^20, 5^20, 20 ln(5/4), ..., 20 ln 5}
      (20 = |R+(D5)|), scanned against the frozen prediction registry
      (same T2/T3 discipline as v527); golden-ratio placebo through the
      same pipeline.  Expected/honest outcome: no T2 hits -> the contract
      stays [O]; the STRUCTURAL test (a frozen D5 transfer spectrum of
      the form (1-n/5)^c) remains the real kill.

Firewall: discovery sandbox, NO promotion decisions, no marker moves.
"""
import itertools
import json
import math
import time
from fractions import Fraction

import numpy as np
import mpmath
import sympy as sp
from sympy import Matrix, Rational
from sympy.matrices.normalforms import smith_normal_form

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
print("S1 -- root inventory under D5 (+) A3 (coords 0-4 | 5-7)")
roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = [0] * 8
                v[i], v[j] = si, sj
                roots.append(tuple(v))
for signs in itertools.product((1, -1), repeat=8):
    if signs.count(-1) % 2 == 0:
        roots.append(tuple(Fraction(s, 2) for s in signs))
check("240 = 112 integer + 128 half-integer roots (even minus count)",
      len(roots) == 240 and sum(1 for r in roots if isinstance(r[0], int)) == 112)

d5 = [r for r in roots if isinstance(r[0], int) and all(r[i] == 0 for i in (5, 6, 7))]
a3 = [r for r in roots if isinstance(r[0], int) and all(r[i] == 0 for i in range(5))]
mixed = [r for r in roots if isinstance(r[0], int) and r not in d5 and r not in a3]
halfs = [r for r in roots if not isinstance(r[0], int)]
even5 = [r for r in halfs if sum(1 for i in range(5) if r[i] < 0) % 2 == 0]
odd5 = [r for r in halfs if sum(1 for i in range(5) if r[i] < 0) % 2 == 1]
info(f"D5: {len(d5)}, A3: {len(a3)}, (10,6): {len(mixed)}, "
     f"(16,4): {len(even5)}, (16bar,4bar): {len(odd5)}")
check("split: 40 (D5) + 12 (A3) + 60 (10,6) + 64 + 64 (spinor sheets) "
      "= 240; coset = 188 root directions; dims 248 = 45+15+60+64+64",
      (len(d5), len(a3), len(mixed), len(even5), len(odd5))
      == (40, 12, 60, 64, 64) and 60 + 64 + 64 == 188
      and 45 + 15 + 60 + 64 + 64 == 248)

# ================================================================ S2
print("S2 -- the glue quotient E8/(D5 (+) A3) is CYCLIC Z4 = mu4")


def col(v):
    return [2 * x for x in v]      # work at doubled coordinates (integers)


e8_basis = [
    [1, -1, -1, -1, -1, -1, -1, 1],            # 2 * alpha1 (spinor root)
    col([1, 1, 0, 0, 0, 0, 0, 0]),
    col([-1, 1, 0, 0, 0, 0, 0, 0]),
    col([0, -1, 1, 0, 0, 0, 0, 0]),
    col([0, 0, -1, 1, 0, 0, 0, 0]),
    col([0, 0, 0, -1, 1, 0, 0, 0]),
    col([0, 0, 0, 0, -1, 1, 0, 0]),
    col([0, 0, 0, 0, 0, -1, 1, 0]),
]
BE = Matrix(e8_basis).T
gram = (BE.T * BE) / 4              # undo doubling: (2u).(2v)/4 = u.v
check("E8 basis valid: Gram determinant = 1 (even unimodular)",
      sp.det(gram) == 1)

l0_basis = [
    col([1, -1, 0, 0, 0, 0, 0, 0]), col([0, 1, -1, 0, 0, 0, 0, 0]),
    col([0, 0, 1, -1, 0, 0, 0, 0]), col([0, 0, 0, 1, -1, 0, 0, 0]),
    col([0, 0, 0, 1, 1, 0, 0, 0]),
    col([0, 0, 0, 0, 0, 1, -1, 0]), col([0, 0, 0, 0, 0, 0, 1, -1]),
    col([0, 0, 0, 0, 0, 1, 1, 0]),
]
BL = Matrix(l0_basis).T
M = BE.solve(BL)
check("L0 = D5 (+) A3 basis has INTEGER coordinates in the E8 basis "
      "(sublattice) and index |det| = 4 = |mu4|",
      all(e.is_Integer for e in M) and abs(M.det()) == 4)
snf = smith_normal_form(M)
divisors_ = [snf[i, i] for i in range(8)]
check("Smith normal form = diag(1,1,1,1,1,1,1,4): the glue group is "
      "CYCLIC Z4 = mu4, NOT Z2 x Z2 -- 'D5 (+) A3 + mu4 => E8' is "
      "literally the lattice glue", sorted(map(abs, divisors_)) == [1] * 7 + [4])

Fmap = M.inv() * BE.inv()


def glue_frac(r):
    fr = Fmap * Matrix([2 * x for x in r])
    return tuple(Fraction(sp.Rational(e).p, sp.Rational(e).q) % 1 for e in fr)


g1 = glue_frac(halfs[0])
classes = {}
for k in range(4):
    classes[tuple((k * c) % 1 for c in g1)] = k
grades = {}
for r in roots:
    grades[r] = classes[glue_frac(r)]
tab = {k: sum(1 for r in roots if grades[r] == k) for k in range(4)}
info(f"root counts by glue grade: {tab}")
g_even = {grades[r] for r in even5}
g_odd = {grades[r] for r in odd5}
check("mu4 grading of the 240 roots: grade 0 = 52 (D5+A3), grade 2 = 60 "
      "((10,6)), grades 1/3 = 64/64 (spinor sheets, each sheet ONE "
      "uniform glue class) -- the 'unused' 188 ARE the nontrivial mu4 "
      "glue classes",
      tab[0] == 52 and tab[2] == 60 and tab[1] == tab[3] == 64
      and all(grades[r] == 0 for r in d5 + a3)
      and all(grades[r] == 2 for r in mixed)
      and len(g_even) == 1 and len(g_odd) == 1 and g_even | g_odd == {1, 3})

# ================================================================ S3
print("S3 -- literal error code: E8 = Construction A of Hamming [8,4,4]")
G = [(1, 1, 1, 1, 1, 1, 1, 1), (0, 1, 0, 1, 0, 1, 0, 1),
     (0, 0, 1, 1, 0, 0, 1, 1), (0, 0, 0, 0, 1, 1, 1, 1)]
code = set()
for coeffs in itertools.product((0, 1), repeat=4):
    w = tuple(sum(c * g[i] for c, g in zip(coeffs, G)) % 2 for i in range(8))
    code.add(w)
weights = sorted(sum(w) for w in code)
selfdual = all(sum(a * b for a, b in zip(u, v)) % 2 == 0
               for u in code for v in code)
check("extended Hamming [8,4,4] = RM(1,3): 16 codewords, SELF-DUAL, "
      "doubly even, weight enumerator 1 + 14 y^4 + y^8",
      len(code) == 16 and selfdual
      and weights == [0] + [4] * 14 + [8]
      and all(w % 4 == 0 for w in weights))
grid = np.array(np.meshgrid(*[[-2, -1, 0, 1, 2]] * 8,
                            indexing='ij')).reshape(8, -1).T.astype(np.int8)
norms = np.einsum('ij,ij->i', grid.astype(np.int32), grid.astype(np.int32))
cand = grid[norms == 4]
lut = np.zeros(256, dtype=bool)
for w in code:
    lut[int(sum(b << i for i, b in enumerate(w)))] = True
keys = ((cand.astype(np.int32) % 2)
        * (2 ** np.arange(8, dtype=np.int32))).sum(axis=1)
inA = lut[keys]
n16 = int(np.sum(inA & (np.abs(cand).max(axis=1) == 2)))
n224 = int(np.sum(inA & (np.abs(cand).max(axis=1) == 1)))
check("Construction A root count: 240 = 16 [(+-2,0^7), zero word] + "
      "14 x 2^4 [weight-4 codewords with signs] -- the E8 roots are "
      "ENUMERATED by the error-correcting code",
      n16 == 16 and n224 == 224 and n16 + n224 == 240)
check("observation (typed, no claim): 14 weight-4 codewords = det A = "
      "dim G2 = quotient-ladder start (v530)", weights.count(4) == 14)

# ================================================================ S4
print("S4 -- primes enter through the counting: N(2n) = 240 sigma3(n)")
rng7 = np.arange(-3, 4, dtype=np.int16)
gi = np.array(np.meshgrid(*[rng7] * 8, indexing='ij')).reshape(8, -1).T
ni = np.sum(gi * gi, axis=1, dtype=np.int16)
si = np.sum(gi, axis=1, dtype=np.int16)
int_ok = (si % 2 == 0)
rng6 = np.array([-5, -3, -1, 1, 3, 5], dtype=np.int16)
gh = np.array(np.meshgrid(*[rng6] * 8, indexing='ij')).reshape(8, -1).T
nh = np.sum(gh * gh, axis=1, dtype=np.int16)
sh = np.sum(gh, axis=1, dtype=np.int16)
half_ok = (sh % 4 == 0)
NE8 = {}
for n in range(1, 7):
    NE8[n] = int(np.sum(int_ok & (ni == 2 * n))) \
        + int(np.sum(half_ok & (nh == 8 * n)))
sig3 = [int(sp.divisor_sigma(n, 3)) for n in range(1, 7)]
info(f"E8 counts N(2n), n=1..6: {[NE8[n] for n in range(1, 7)]} "
     f"= 240 * {sig3}")
check("theta counting EXACT: N(2n) = 240 sigma3(n) for n = 1..6 "
      "(direct lattice enumeration: 240, 2160, 6720, 17520, 30240, 60480)",
      all(NE8[n] == 240 * sig3[n - 1] for n in range(1, 7)))
check("sigma3 is MULTIPLICATIVE: sigma3(6) = sigma3(2) sigma3(3) = 9*28 "
      "= 252 (= the v532 dual product); Euler factor sigma3(p^k) = "
      "(p^{3(k+1)}-1)/(p^3-1) exact (p = 2,3,5; k <= 4)",
      sig3[5] == sig3[1] * sig3[2] == 252
      and all(int(sp.divisor_sigma(p**k, 3))
              == (p**(3 * (k + 1)) - 1) // (p**3 - 1)
              for p in (2, 3, 5) for k in range(5)))
NS = 200000
sieve = np.zeros(NS + 1, dtype=np.float64)
for d in range(1, NS + 1):
    sieve[d::d] += float(d)**3
S5v = float(np.sum(sieve[1:] / np.arange(1, NS + 1, dtype=np.float64)**5))
target = float(mpmath.zeta(5) * mpmath.zeta(2))
info(f"Dirichlet: sum sigma3(n)/n^5 = {S5v:.9f} vs zeta(5) zeta(2) "
     f"= {target:.9f}")
check("the E8 theta L-series IS zeta(s) zeta(s-3): sum sigma3(n)/n^s = "
      "zeta(s) zeta(s-3) at s = 5 (2e-5) -- the Riemann zeta enters E8 "
      "through its own counting function", abs(S5v - target) < 2e-5)
check("multiplicativity identity for E8: N(4) N(6) = N(12) N(2) "
      f"({NE8[2]}*{NE8[3]} = {NE8[6]}*{NE8[1]} = {NE8[2]*NE8[3]})",
      NE8[2] * NE8[3] == NE8[6] * NE8[1])
sub_ok = ((si % 2 == 0)
          & (gi[:, :5].astype(np.int32).sum(axis=1) % 2 == 0)
          & (gi[:, 5:].astype(np.int32).sum(axis=1) % 2 == 0))
NL0 = {n: int(np.sum(sub_ok & (ni == 2 * n))) for n in (1, 2, 3, 6)}
info(f"D5(+)A3 sublattice counts N(2n), n=1,2,3,6: "
     f"{[NL0[n] for n in (1, 2, 3, 6)]}")
check("KILL CONTRAST: the same identity FAILS for the D5 (+) A3 "
      "sublattice alone (N(4) N(6) != N(12) N(2)) -- WITHOUT the 188 "
      "glue roots the prime/Euler structure of the counting BREAKS: the "
      "'unused' part is exactly the modular completion",
      NL0[1] == 52 and NL0[2] * NL0[3] != NL0[6] * NL0[1])

# ================================================================ S5
print("S5 -- CARRIER.SATURATION.LOG census against the frozen registry")
with open('verification/predictions_frozen.json') as fh:
    reg = json.load(fh)
targets = []
for e in reg['predictions']:
    try:
        v = float(e['frozen_value'])
    except (KeyError, ValueError):
        continue
    if e.get('layer') == 'assigned' or v == round(v):
        continue
    targets.append((e['id'], v))
info(f"targets: {len(targets)} frozen non-assigned, non-integer values")
P2_D5 = 20      # |R+(D5)|
bases = {}
for n in (1, 2, 3, 4):
    bases[f"(5/{5-n})^20"] = (5.0 / (5 - n))**P2_D5
    bases[f"20ln(5/{5-n})"] = P2_D5 * math.log(5.0 / (5 - n))
placebo = {}
phi_g = (1 + math.sqrt(5)) / 2
for lab, b in (("phi^20", phi_g**P2_D5), ("20lnphi", P2_D5 * math.log(phi_g)),
               ("phi^10", phi_g**10), ("10lnphi", 10 * math.log(phi_g)),
               ("phi^5", phi_g**5), ("5lnphi", 5 * math.log(phi_g)),
               ("phi^2", phi_g**2), ("2lnphi", 2 * math.log(phi_g))):
    placebo[lab] = b
fracs = [(p, q) for p in range(1, 13) for q in range(1, 13)
         if math.gcd(p, q) == 1]


def census(basedict):
    t2, t3 = [], []
    for lab, b in basedict.items():
        for f in (1.0, -1.0):
            bb = b**f
            for p, q in fracs:
                v = bb * p / q
                for tid, t in targets:
                    rel = abs(v / t - 1)
                    if rel < 1e-6:
                        t2.append((lab, f, p, q, tid, rel))
                    elif rel < 1e-3:
                        t3.append((lab, f, p, q, tid, rel))
    return t2, t3


t2_sat, t3_sat = census(bases)
t2_pla, t3_pla = census(placebo)
info(f"saturation class: T2 hits = {len(t2_sat)}, T3 hits = {len(t3_sat)}; "
     f"golden placebo: T2 = {len(t2_pla)}, T3 = {len(t3_pla)}")
if t2_sat:
    for h in t2_sat:
        info(f"  T2 HIT: {h}")
check("census verdict: NO T2 hit of the D5 saturation class on the frozen "
      "registry (and T3 rate comparable to the golden placebo => "
      "calibration noise) -- CARRIER.SATURATION.LOG stays [O]; the REAL "
      "kill remains a frozen D5 transfer spectrum of the form (1-n/5)^c",
      len(t2_sat) == 0 and len(t3_sat) <= max(3 * max(len(t3_pla), 1), 6))

print()
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({time.time()-T0:.1f}s)")
raise SystemExit(0 if FAIL == 0 else 1)
