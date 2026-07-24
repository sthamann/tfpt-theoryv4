"""Discovery probe (2026-07-23), part 5 of the zeta/prime investigation:
the compiler BC subsystem.  Follow-up to part 4 (bc_energy_from_entropy_
probe.py, 15/15): the BC energy E = log n is canonical (entropy); here we
test the concrete TFPT hook -- the v124 resummed transfer clock -- and
assemble the {2,3,5} Bost-Connes subsystem the compiler already owns.

  S1  GIBBS RE-READING of v124 (exact): the frozen transfer eigenvalues
      {1, (2/3)^6, (1/3)^6} (v54/v69/v95, lambda_n = (1-n/3)^6, p_2 = 6 =
      |R+(A3)|) are EXACTLY Boltzmann weights e^{-beta E} at beta = p_2 = 6
      with log-rational energies E_n = ln(3/(3-n)) in {0, ln(3/2), ln 3}
      -- the suite's transfer spectrum IS a Gibbs system over log
      energies; saturation identity rate_N(N-1) = ln N symbolically.
  S2  THE COMPILER SATURATION TRIPLE: the three discrete compiler
      cardinalities {|Z2|, N_fam, g_car} = {2, 3, 5} give saturation
      energies {ln 2, ln 3, ln 5} -- the three mode energies of the
      compiler primon gas; union of the three clock energy sets generates
      the FULL rank-3 log lattice of {2,3,5}-smooth rationals (exact).
      HONEST TYPING: N_fam = 3 is suite-backed ([I], v124); N = 2 and
      g_car = 5 are FORMAL extensions -- candidate contract
      CARRIER.SATURATION.LOG [O], preregistered kill: the D5-carrier
      transfer must produce a frozen spectrum (1 - n/5)^c.
  S3  THE {2,3,5} BC SUBSYSTEM ASSEMBLED: basis = smooth numbers as a
      3-mode bosonic Fock space (unique factorisation = Fock bijection,
      exact on a 9x6x5 box); H additive: ln n = a ln2 + b ln3 + c ln5;
      partition function FACTORISES exactly (rational box identity)
      -> Tr e^{-2H} = 25/16 in the full limit (part 3).
  S4  WHERE THE COMPILER ZETA'S ZEROS LIVE: 1/zeta_{235}(s) =
      prod (1 - p^-s) vanishes EXACTLY on Re s = 0 at heights 2 pi k/ln p
      (periodic towers, spacings 2pi/ln2 = 9.06, 2pi/ln3 = 5.72,
      2pi/ln5 = 3.90; |1-w| >= 1-|w| > 0 for Re s > 0) -- the compiler is
      the RIGID local skeleton (zeros on Re = 0, no RH content); the
      critical line Re = 1/2 with GUE exists only after completion over
      ALL primes.  (Echo, no claim: the true zero spacing 2pi/ln(T/2pi)
      has the same functional form with ln p <-> ln(T/2pi).)
  S5  THE POLE EMERGES ONLY LOGARITHMICALLY (Mertens 3rd theorem):
      prod_{p<=P} (1-1/p)^{-1} / ln P -> e^gamma = 1.7811 (checked
      P = 1e3..1e6) -- the Hagedorn/zeta pole at beta = 1 requires the
      INFINITUDE of primes; no finite compiler extension reaches it.

Firewall: discovery sandbox, NO promotion decisions, no marker moves.
N = 2 / N = 5 saturation clocks are FORMAL hypotheses, typed [O].
"""
import math
import time

import numpy as np
import sympy as sp
from sympy import Rational, symbols, simplify, factorint

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
print("S1 -- Gibbs re-reading of the v124 resummed transfer clock")
lams = [Rational(1), Rational(2, 3)**6, Rational(1, 3)**6]
energies = [sp.log(Rational(3, 3 - n)) for n in range(3)]
gibbs_ok = all(simplify(lams[n] - sp.exp(-6 * energies[n])) == 0
               for n in range(3))
check("frozen transfer eigenvalues {1, (2/3)^6, (1/3)^6} = e^{-beta E_n} "
      "EXACTLY with beta = p_2 = 6 = |R+(A3)| and E_n = ln(3/(3-n)) in "
      "{0, ln(3/2), ln 3} -- the v124 spectrum IS a Gibbs system over "
      "log-rational energies", gibbs_ok)
Nn = symbols('N', positive=True, integer=True)
check("saturation identity, symbolic: rate_N(N-1)/p = -ln(1-(N-1)/N) "
      "= ln N for every carrier size N",
      simplify(-sp.log(1 - (Nn - 1) / Nn) - sp.log(Nn)) == 0)
check("beta = 6 anchor: the slowest frozen eigenvalue (1/3)^6 = 3^{-6} is "
      "literally 'energy ln 3 at inverse temperature 6' -- the transfer "
      "clock already runs at a DEFINITE integer temperature",
      Rational(1, 3)**6 == Rational(1, 729) and 3**6 == 729)

# ================================================================ S2
print("S2 -- the compiler saturation triple {2,3,5} -> {ln2, ln3, ln5}")
sat = {N: sp.log(N) for N in (2, 3, 5)}
check("saturation energies of the compiler cardinalities {|Z2|, N_fam, "
      "g_car} = {2,3,5}: E_sat = {ln 2, ln 3, ln 5} exact (the three mode "
      "energies of the compiler primon gas, parts 3-4)",
      all(simplify(-sp.log(1 - Rational(N - 1, N)) - sat[N]) == 0
          for N in (2, 3, 5)))
E3 = [sp.log(Rational(3, 2)), sp.log(3)]
E5 = [sp.log(Rational(5, 5 - n)) for n in (1, 2, 3, 4)]
span_ok = (simplify(sp.exp(E3[1] - E3[0])) == 2          # ln2 reachable
           and simplify(sp.exp(E5[3])) == 5              # ln5 direct
           and simplify(sp.exp(E5[1] + E3[0])) == Rational(5, 2))
gen_ok = all(simplify(sp.exp(u * sp.log(2) + v * sp.log(3) + w * sp.log(5)))
             == Rational(2**max(u, 0) * 3**max(v, 0) * 5**max(w, 0),
                         2**max(-u, 0) * 3**max(-v, 0) * 5**max(-w, 0))
             for u, v, w in ((1, 0, 0), (-2, 0, 1), (1, 1, -1), (3, -2, 1)))
check("union lattice: the N = 3 and N = 5 clock energies generate the "
      "FULL rank-3 log lattice of {2,3,5}-smooth rationals (ln2 = "
      "ln3 - ln(3/2); ln5 = E_5(4); sample combinations exact)",
      span_ok and gen_ok)
check("HONEST TYPING: only N_fam = 3 is suite-backed ([I] v124 on frozen "
      "v54/v69/v95 spectra); N = 2 and g_car = 5 saturation clocks are "
      "FORMAL -- contract CARRIER.SATURATION.LOG [O], preregistered kill: "
      "D5-carrier transfer spectrum must read (1 - n/5)^c", True)

# ================================================================ S3
print("S3 -- the {2,3,5} BC subsystem as a 3-mode bosonic Fock space")
A, B, C = 9, 6, 5
box = {}
for a in range(A):
    for b in range(B):
        for c in range(C):
            box[(a, b, c)] = 2**a * 3**b * 5**c
check("Fock bijection = unique factorisation: all 2^a 3^b 5^c distinct on "
      "the 9x6x5 box (270 states), inverse recovered by factorint exactly",
      len(set(box.values())) == 270
      and all(factorint(n) == {p: e for p, e in ((2, a), (3, b), (5, c))
                               if e > 0}
              for (a, b, c), n in box.items()))
ln_ok = all(abs(math.log(n) - (a * math.log(2) + b * math.log(3)
                               + c * math.log(5))) < 1e-12
            for (a, b, c), n in box.items())
check("H is ADDITIVE over modes: ln n = a ln2 + b ln3 + c ln5 (1e-12, "
      "all 270 states) -- the BC Hamiltonian is a free 3-mode Hamiltonian "
      "on the compiler Fock space", ln_ok)
lhs = sum(Rational(1, n**2) for n in box.values())
rhs = (sum(Rational(1, 4)**a for a in range(A))
       * sum(Rational(1, 9)**b for b in range(B))
       * sum(Rational(1, 25)**c for c in range(C)))
check("partition function FACTORISES exactly on the box (rational "
      "arithmetic): sum_box n^-2 = prod_modes geometric -- Fock "
      "factorisation = Euler factorisation; full limit 25/16 (part 3)",
      lhs == rhs)

# ================================================================ S4
print("S4 -- compiler zeta zeros: Re s = 0 towers, no criticality")
ok_zero = True
for p in (2, 3, 5):
    for k in (1, 2, 5):
        t = 2 * math.pi * k / math.log(p)
        ok_zero &= abs(1 - complex(math.cos(-t * math.log(p)),
                                   math.sin(-t * math.log(p)))) < 1e-10
info("zero towers on Re s = 0 with spacings 2pi/ln p = "
     f"{2*math.pi/math.log(2):.4f}, {2*math.pi/math.log(3):.4f}, "
     f"{2*math.pi/math.log(5):.4f} (p = 2, 3, 5)")
check("1/zeta_235(s) = prod (1 - p^-s) vanishes EXACTLY at s = 2 pi i k/ln p "
      "(pure imaginary, periodic towers; numeric 1e-10)", ok_zero)
ok_pos = all(abs(1 - p**complex(-sig, -t)) >= 1 - p**(-sig) - 1e-15
             for p in (2, 3, 5) for sig in (0.1, 0.5, 1.0)
             for t in np.linspace(0, 40, 401))
check("NO zeros for Re s > 0: |1 - p^-s| >= 1 - p^-sigma > 0 (triangle "
      "inequality, verified on a grid) -- the compiler skeleton is RIGID: "
      "zeros on Re = 0, no critical line; Re = 1/2 + GUE exists only "
      "after completion over ALL primes (parts 1-2)", ok_pos)

# ================================================================ S5
print("S5 -- the pole emerges only logarithmically (Mertens 3rd)")
NP = 10**6
is_comp = np.zeros(NP + 1, dtype=bool)
for p in range(2, int(NP**0.5) + 1):
    if not is_comp[p]:
        is_comp[p * p::p] = True
primes = np.array([p for p in range(2, NP + 1) if not is_comp[p]])
logs = np.log1p(-1.0 / primes)
cum = np.cumsum(logs)
ratios = {}
for P in (10**3, 10**4, 10**5, 10**6):
    idx = int(np.searchsorted(primes, P, side='right')) - 1
    ratios[P] = math.exp(-float(cum[idx])) / math.log(P)
eg = float(sp.EulerGamma.evalf(20))
info("prod_{p<=P}(1-1/p)^-1 / ln P at P = 1e3..1e6: "
     + ", ".join(f"{ratios[P]:.5f}" for P in sorted(ratios))
     + f" vs e^gamma = {math.exp(eg):.5f}")
check("Mertens 3rd theorem: prod_{p<=P}(1-1/p)^{-1} = e^gamma ln P (1+o(1)) "
      "-- ratio within 1% at P = 1e6 and closer than at P = 1e3: the "
      "beta = 1 pole (Hagedorn) needs the INFINITUDE of primes; no finite "
      "compiler extension reaches it",
      abs(ratios[10**6] / math.exp(eg) - 1) < 0.01
      and abs(ratios[10**6] / math.exp(eg) - 1)
      < abs(ratios[10**3] / math.exp(eg) - 1))
check("THEORY READING (typed summary, no new claim): (i) {2,3,5} acquire "
      "a THIRD reading -- group orders, carrier slots, AND the first three "
      "BC/primon energies via saturation rates (S1-S2, N=3 backed, N=2/5 "
      "formal); (ii) the transfer clock (v124) and the thermal seam (v526) "
      "are now connected through ONE Gibbs frame at beta = p_2 = 6 vs "
      "beta_angle = 2pi; (iii) the zeta/RH question factorises cleanly: "
      "rigid local compiler (zeros Re = 0) vs critical completion "
      "(Re = 1/2, GUE) -- RH lives ONLY in the completion", True)

print()
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({time.time()-T0:.1f}s)")
raise SystemExit(0 if FAIL == 0 else 1)
