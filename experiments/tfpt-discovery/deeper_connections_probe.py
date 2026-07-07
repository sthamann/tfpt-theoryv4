#!/usr/bin/env python3
"""Deeper-connections discovery probe (2026-07-07, follow-up round).

Goal: push PAST the D11-D15 batch for *stronger* exact connections, with the
repo's anti-numerology discipline. Two genuinely new threads survive; the
small-integer temptations are quantified by a look-elsewhere census and
DECLINED in the same script.

FIREWALL / TYPING: discovery-sandbox probe (experiments/tfpt-discovery). Never
load-bearing, never a scorecard row, nothing promoted. FORCED identities are
exact [E]; every physical reading is [C]; declined coincidences print their
deviation and their census cost.

  N1  THE METALLIC-MEAN COMPACTNESS LAW (upgrades D15, links D1 + D7 + D15).
      The gravastar compactness function C(k) = (k^2-1)/(6k) evaluated at the
      n-th METALLIC MEAN mu_n = (n+sqrt(n^2+4))/2 (the root of x^2-nx-1, the
      continued fraction [n;n,n,...]) collapses to
          C(mu_n) = n/6           (exact, all n)
      so the "sheet index" is literally 6 x compactness. The two *classical*
      GR thresholds are the two carrier hands as metallic indices:
          photon sphere  C = 1/3 = 2/6  <->  n = |Z2| = 2  (SILVER mean 1+sqrt2)
          horizon        C = 1/2 = 3/6  <->  n = N_fam = 3  (BRONZE mean)
      The physical window C <= 1/2 is exactly n <= 3, capped at horizon=N_fam.
      Discovery 1's Markov boundary branches ARE mu_1 (golden/Fibonacci) and
      mu_2 (silver/Pell); the horizon index 3 is NOT a Markov number but IS the
      Markov COUPLING k=3 (exactly D1's "3 is the coupling, not a state").
      Buchdahl (4/9) and Nariai (3/8) are the NON-metallic sheets in between.

  N2  D11 SHARPENED: the eigenvalue and the comb are S-DUAL modular faces.
      tau = i ln(Lambda_DSI)/(2pi) has |tau| < 1 (OUTSIDE the fundamental
      domain); its nome is q = lambda_T = (2/3)^6. The S-dual tau~ = -1/tau =
      i*omega sits IN the fundamental domain (omega > 1), with nome
          q~ = e^{2 pi i tau~} = e^{-2 pi omega} = eps^4           (exact)
      i.e. the known amplitude/frequency lock eps = e^{-(pi/2) omega} is exactly
      "the comb nome is the S-image of the eigenvalue nome". HONEST NEGATIVE
      RESULT (corrects D11's proposed test): at the real point q=lambda_T the
      character chi = E4/eta^8 is a plain REAL number (prefactor q^{-1/3} = 9/4
      exact), so the comb is NOT arg chi(lambda_T); it lives on the S-dual face.

  DECLINED (LEE-quantified, NOT claims):
      D_a metallic discriminants n^2+4 for n=1..5 = {5,8,13,20,29} vs the TFPT
          named set -> census cost printed.
      D_b the D12 discriminant 7 "homes" (E8 exponent / rank-1 / |Z2|+g_car).

Run:  ./experiments/tfpt-discovery/.venv/bin/python \
        experiments/tfpt-discovery/deeper_connections_probe.py
"""
from __future__ import annotations

import math
from fractions import Fraction

import sympy as sp

FAILS: list[str] = []
DECLINED: list[str] = []


def check(label: str, ok: bool) -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        FAILS.append(label)


def info(label: str) -> None:
    print(f"  [INFO] {label}")


def declined(label: str) -> None:
    print(f"  [DECLINED] {label}")
    DECLINED.append(label)


# ----------------------------------------------------------------- constants
G_CAR, N_FAM, Z2 = 5, 3, 2
RANK_E8, H_E8, DELTA_Q, E_MAX = 8, 30, 13, 29
LN_LAMBDA = 6 * sp.log(sp.Rational(3, 2))
LAMBDA_T = sp.Rational(2, 3) ** 6
OMEGA = 2 * sp.pi / LN_LAMBDA
EPS = sp.exp(-sp.pi ** 2 / LN_LAMBDA)
# v418 frozen named-integer set (reused from markov_modular_prime_clock_probe.py)
TFPT_NAMED = {1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 20, 21, 24,
              25, 30, 31, 40, 41, 48, 52, 55, 56, 60, 78, 120, 128, 240, 248}


# ================================================================= N1
print("=" * 74)
print("N1  METALLIC-MEAN COMPACTNESS LAW  C(mu_n) = n/6  (upgrades D15)")
print("=" * 74)

n = sp.symbols("n", positive=True)
mu_n = (n + sp.sqrt(n ** 2 + 4)) / 2                 # n-th metallic mean
C_of = lambda k: (k ** 2 - 1) / (6 * k)              # gravastar compactness
check("FORCED [E, all n]: for the n-th metallic mean mu_n (root of x^2-nx-1), "
      "C(mu_n) = (mu_n^2-1)/(6 mu_n) = n/6 exactly  (since mu_n^2-1 = n*mu_n)",
      sp.simplify(C_of(mu_n) - n / 6) == 0)

# the two classical GR thresholds are the two carrier hands as metallic indices
metallic = {
    1: ("golden  phi=(1+sqrt5)/2", (1 + sp.sqrt(5)) / 2, sp.Rational(1, 6)),
    2: ("silver  1+sqrt2        ", 1 + sp.sqrt(2), sp.Rational(1, 3)),
    3: ("bronze  (3+sqrt13)/2   ", (3 + sp.sqrt(13)) / 2, sp.Rational(1, 2)),
    5: ("g_car   (5+sqrt29)/2   ", (5 + sp.sqrt(29)) / 2, sp.Rational(5, 6)),
}
for idx, (name, mu, C) in metallic.items():
    ok = sp.simplify(mu ** 2 - idx * mu - 1) == 0 and sp.simplify(C_of(mu) - C) == 0
    check(f"n={idx} {name}: mu solves x^2-{idx}x-1, C = {C} = {idx}/6", ok)

check("PHYSICAL READING [C]: photon sphere C=1/3 <-> n=|Z2|=2 (silver); "
      "horizon C=1/2 <-> n=N_fam=3 (bronze); the two GR thresholds' metallic "
      "indices are exactly the two carrier hands (|Z2|, N_fam)",
      sp.simplify(C_of(1 + sp.sqrt(2)) - sp.Rational(1, 3)) == 0
      and sp.simplify(C_of((3 + sp.sqrt(13)) / 2) - sp.Rational(1, 2)) == 0)

check("PHYSICAL WINDOW [E]: C = n/6 <= 1/2 (horizon) iff n <= 3 = N_fam; the "
      "horizonless/physical metallic sheets are exactly n in {1,2,3} = "
      "{golden, silver, bronze}, capped at horizon = N_fam",
      all(Fraction(k, 6) <= Fraction(1, 2) for k in (1, 2, 3))
      and Fraction(4, 6) > Fraction(1, 2))

# link to Discovery 1: golden/silver ARE the Markov boundary branches; horizon
# index 3 is the Markov COUPLING, not a Markov number
markov_numbers = {1, 2, 5, 13, 29, 34, 89, 169, 194, 233, 433, 610, 985}
check("LINK to D1 [E]: photon-sphere index 2 IS a Markov number (silver/Pell "
      "branch exists); horizon index 3 is NOT a Markov number but IS the "
      "Markov coupling k=3=N_fam -- exactly D1's 'k=3 is the coupling, not a "
      "state'",
      Z2 in markov_numbers and N_FAM not in markov_numbers)

info("Buchdahl 4/9 and Nariai 3/8 are the NON-metallic sheets between silver "
     "(1/3) and bronze (1/2): 6*4/9 = 8/3 and 6*3/8 = 9/4 are not integers, "
     "so they are integer/algebraic (k=3, (9+sqrt145)/8) sheets, not "
     "continued-fraction [n;n,...] points.")
info("the shared 6 = 2*N_fam is the SAME exponent as in (3/2)^6 (the DSI/seam "
     "exponent): metallic index n = 6*C ties the seam exponent to the "
     "compactness->continued-fraction map.")


# ================================================================= N2
print("=" * 74)
print("N2  D11 SHARPENED: eigenvalue nome and comb nome are S-DUAL faces")
print("=" * 74)

tau = sp.I * LN_LAMBDA / (2 * sp.pi)
tau_tilde = -1 / tau
q = sp.exp(2 * sp.pi * sp.I * tau)
q_tilde = sp.exp(2 * sp.pi * sp.I * tau_tilde)

check("eigenvalue face: q = e^{2 pi i tau} = lambda_T = (2/3)^6 = 64/729 "
      "(tau = i ln Lambda/(2pi))",
      sp.simplify(q - LAMBDA_T) == 0)

check("S-dual: tau~ = -1/tau = i*omega  (omega = 2pi/ln Lambda)",
      sp.simplify(tau_tilde - sp.I * OMEGA) == 0)

check("comb face: nome q~ = e^{2 pi i tau~} = e^{-2 pi omega} = eps^4  "
      "(so eps = e^{-(pi/2) omega}: amplitude and frequency are ONE datum, "
      "= the S-image of the eigenvalue)",
      sp.simplify(q_tilde - EPS ** 4) == 0
      and sp.simplify(q_tilde - sp.exp(-2 * sp.pi * OMEGA)) == 0)

# fundamental-domain check: |tau| < 1 (eigenvalue face outside), |tau~| > 1 (in)
abs_tau = float(LN_LAMBDA / (2 * sp.pi))
abs_tau_tilde = float(OMEGA)
check("fundamental domain: |tau| = ln Lambda/(2pi) < 1 (eigenvalue face is "
      "OUTSIDE the fundamental domain), |tau~| = omega > 1 (the comb face is "
      "the fundamental-domain representative)",
      abs_tau < 1 < abs_tau_tilde)

# HONEST NEGATIVE RESULT: q^{-1/3} = 9/4 exact; chi(lambda_T) is a real number
check("prefactor is exact: q^{-1/3} = lambda_T^{-1/3} = (9/4) since "
      "lambda_T = (4/9)^3  (and 9/4 = (N_fam/|Z2|)^2)",
      sp.simplify(LAMBDA_T ** sp.Rational(-1, 3) - sp.Rational(9, 4)) == 0)


def sigma3(m: int) -> int:
    return sum(d ** 3 for d in range(1, m + 1) if m % d == 0)


def chi_bracket_at(qval: float, terms: int = 40) -> tuple[float, float]:
    """[E4/prod(1-q^k)^8] at real qval; returns (value, last-term size)."""
    e4 = [1.0] + [240.0 * sigma3(k) for k in range(1, terms)]
    # prod(1-q^k) as truncated series
    prod = [1.0] + [0.0] * (terms - 1)
    for k in range(1, terms):
        fac = [0.0] * terms
        fac[0] = 1.0
        fac[k] = -1.0
        prod = [sum(prod[i] * fac[j - i] for i in range(j + 1)) for j in range(terms)]
    inv = [1.0] + [0.0] * (terms - 1)
    for k in range(1, terms):
        inv[k] = -sum(prod[i] * inv[k - i] for i in range(1, k + 1))
    inv8 = [1.0] + [0.0] * (terms - 1)
    for _ in range(8):
        inv8 = [sum(inv8[i] * inv[j - i] for i in range(j + 1)) for j in range(terms)]
    coeffs = [sum(e4[i] * inv8[j - i] for i in range(j + 1)) for j in range(terms)]
    powers = [qval ** j for j in range(terms)]
    val = sum(c * p for c, p in zip(coeffs, powers))
    last = abs(coeffs[-1] * powers[-1])
    return val, last


qf = 64.0 / 729.0
bracket, tail = chi_bracket_at(qf)
chi_val = (9.0 / 4.0) * bracket
check("HONEST NEGATIVE [E, numeric]: chi(lambda_T) = (9/4)*E4/eta^8 at the "
      "REAL nome q=64/729 is a plain real number (series converges: last term "
      f"~ {tail:.1e}) -- NO phase, so the comb is NOT arg chi(lambda_T); the "
      "comb lives on the S-dual face tau~=i*omega. This CORRECTS D11's "
      "proposed test.",
      tail < 1e-6)
info(f"chi(lambda_T) = {chi_val:.6f}  (real; bracket E4/eta^8 = {bracket:.6f}, "
     f"prefactor 9/4). The E4/eta^8 -> comb map stays OPEN [O]; what is new is "
     f"the correct S-dual geometry and the disproof of the naive real-point test.")


# ================================================================= DECLINED
print("=" * 74)
print("DECLINED (look-elsewhere quantified; NOT claims)")
print("=" * 74)

# D_a: metallic discriminants n^2+4
disc = {k: k ** 2 + 4 for k in range(1, 6)}
named_le30 = sorted(x for x in TFPT_NAMED if x <= 30)
p_named = len(named_le30) / 30.0
hits = [d for d in disc.values() if d in TFPT_NAMED]
census = p_named ** len(disc)
info(f"metallic discriminants n^2+4, n=1..5 = {list(disc.values())} "
     f"= {{g_car=5, rank=8, Delta_Q=13, deg=20, e_max=29}}")
declined(f"n^2+4 pattern: {len(hits)}/5 land in the {len(named_le30)}-of-30 "
         f"TFPT named set; a random small integer hits with p~{p_named:.2f}, so "
         f"all-5 costs p~{census:.2f} -- NOT significant; only C(mu_n)=n/6 (a "
         f"functional identity for ALL n) carries load, not the integer list")

# D_b: the D12 discriminant 7
homes = {"smallest E8 exponent (7, mu4-forbidden like the 17-crack)": 7 in
         [1, 7, 11, 13, 17, 19, 23, 29],
         "rank(E8)-1 = b0(QCD n_f=6)": 7 == RANK_E8 - 1,
         "|Z2|+g_car = 2+5": 7 == Z2 + G_CAR}
info(f"D12 discriminant 7 candidate 'homes': "
     f"{[h for h, ok in homes.items() if ok]}")
declined("the D12 '7' has three arithmetic homes but no forced route; typed as "
         "OPEN, not resolved -- three small-integer coincidences do not pin a "
         "carrier without a derivation")


# ================================================================= summary
print("=" * 74)
n_fail = len(FAILS)
print(f"SUMMARY: {'ALL EXACT CHECKS PASSED' if not n_fail else f'{n_fail} FAILURES'}"
      f"  |  survivors: N1 (metallic law C=n/6, [E] + [C] reading), "
      f"N2 (S-dual D11 + honest negative)  |  {len(DECLINED)} temptations "
      f"declined  |  exploration only, nothing promoted")
for f in FAILS:
    print("   FAIL:", f)
raise SystemExit(1 if n_fail else 0)
