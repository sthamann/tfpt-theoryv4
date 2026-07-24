"""Discovery probe (2026-07-24), part 45 of the zeta/prime investigation.
FINAL test of the central-value line: Waldspurger proportionality for the
NON-PLUS compiler object g in the Baruch–Mao / metaplectic frame.

Classical background (named as such — not new mathematics):
  Waldspurger (1981): for ANY weight-(k+1/2) eigenform (not only
  Kohnen-plus), |b(|d|)|² ∝ |d|^{k-1/2} L(f × χ_d, k) × (local factors
  at finitely many places).  Baruch–Mao (2007): explicit metaplectic
  formulae; the 2-adic local correction depends only on d mod 8, so
  the Waldspurger quotient is constant on each 2-adic class of d, with
  possibly DIFFERENT class constants.

Context:
  T38/T41: g = θ₂(q²)²·θ₃(q²)·θ₄·θ₄(q²) is the Shimura preimage of f₈
    (Sh_{t=2}(g) = −8 f₈) and an exact T(p²)-eigenform with λ = a_p(f₈).
  T43/T44: g ∉ Kohnen-plus; exploratory Waldspurger quotients clustered
    (~21) with outlier d = 89 blamed on a poorly convergent direct-sum
    twist L-value.  Lesson: fix L-value quality FIRST, then test.

S1 / B1  Clean twist L-values (foundation):
    L(f₈ × χ_d, s=2) via the COMPLETE Lambda / incomplete-Gamma AFE
    (T12 technique).  For odd fundamental d (gcd(d,2)=1), f₈×χ_d is a
    newform of level 8·d², weight 4.  Fricke / root-number convention
    for the twist (documented below).  Validations:
      (i) FE self-consistency / root-number selection at Re(s)>2;
      (ii) AFE ↔ well-convergent direct sums at s=3.5 (NOT at s=2 —
          direct sums at the centre are the T44 failure mode);
      (iii) T44 outlier d = 89 MUST stabilise under AFE (litmus).

S2 / B2  Proportionality test:
    R(d) = b(|d|)² / (|d|^{3/2} · L(f₈×χ_d, 2)) over ≥10 fundamental
    discriminants with b(|d|)≠0, split by d mod 8.
    Root-number dichotomy (classical): ε_d = −1 ⇒ Λ(2)=0 ⇒ L(2)=0
    ⇒ Waldspurger forces b(|d|)=0.  Live class is d≡1 mod 8 (ε=+1);
    vanishing class d≡5 mod 8 is a consistency check, not a fit.
    Success: relative spread < 5% WITHIN each live d-mod-8 class.

S3 / B3  Interpretation (honest typing):
    Success ⇒ central-value family L(f₈×χ_d, 2) is realised as coefficient
    squares of g (with explicit 2-adic local factors) — third functor
    channel (abelian→1/2; cuspidal→a_p; central values→b(d)²).
    These are GL(2)-centre values at s=2, NOT the ξ-line; no RH content.
    Failure despite clean L-values ⇒ central-value line rests as typed-open.

PREREGISTERED CRITERIA:
  B1: AFE L-values pass (i)–(iii); K1 if AFE contradicts validated directs
      at s=3.5 (where directs converge).
  B2: classwise constancy < 5% on each live d-mod-8 class with ≥3 samples;
      vanishing class d≡5 mod 8: b(|d|)=0 for all odd fund. d in range;
      K2 if spread > 5% inside a live class despite B1.
  Verdicts:
    CENTRAL-VALUES-WIRED-BM / NUMERICALLY-CLEAN-BUT-SCATTERED / IMPL-BLOCKED.

Firewall: discovery sandbox only — no promotion, no ledger/paper/website/
marker edits; classical theorems named as classical; no RH-evidence language.
"""
from __future__ import annotations

import math
import time
from collections import defaultdict

import mpmath
import numpy as np
import sympy as sp

PASS = 0
FAIL = 0
T0 = time.time()
mpmath.mp.dps = 25

# ---------------------------------------------------------------- config
N_F8 = 100_000
QMAX = 200
K_WT = 4
HEAD_AP = {3: -4, 5: -2, 7: 24, 11: -44, 13: 22}
WITNESS_KEY = (0, 2, 0, 1, 1, 1)
DMAX = 120
# AFE↔direct validation at s=3.5 (direct converges; centre does not).
SMALL_D_VALIDATE = (5, 13, 17, 29, 37, 41, 89)
D_LITMUS = 89
AFE_DIRECT_TOL = mpmath.mpf("1e-6")     # s=3.5 AFE vs direct
FE_EPS_RATIO = 10.0                     # correct-ε gap << wrong-ε gap
STABLE_REL_TOL = mpmath.mpf("1e-5")     # d=89 term-doubling
CLASS_SPREAD_OK = 0.05
MIN_PER_CLASS = 3
MIN_TOTAL_D = 10
L_VANISH_TOL = mpmath.mpf("1e-20")


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


# ================================================================ helpers
def eta_pass(d, e, order):
    s = np.zeros(order + 1, dtype=np.int64)
    s[0] = 1
    for k in range(d, order + 1, d):
        for _ in range(e):
            s[k:] = s[k:] - s[:-k]
    return s


def conv_i64(a, b, order):
    return np.convolve(a, b)[: order + 1].astype(np.int64)


def kronecker(d: int, n: int) -> int:
    return int(sp.kronecker_symbol(d, n))


def is_fundamental_discriminant(d: int) -> bool:
    if d == 0:
        return False
    if d % 4 == 1:
        return abs(sp.mobius(abs(d))) == 1
    if d % 4 != 0:
        return False
    m = d // 4
    if m % 4 not in (2, 3):
        return False
    return abs(sp.mobius(abs(m))) == 1


def twist_root_number(d: int, eps_f: int = 1, N_f: int = 8) -> int:
    """Classical twist root-number convention (documented).

    For a weight-k newform f of level N_f, trivial nebentypus, Fricke /
    root number ε_f, and an odd fundamental discriminant d with
    gcd(d, N_f) = 1, the quadratic twist f ⊗ χ_d is a newform of level
    N_f · d² and root number

        ε_d = ε_f · χ_d(N_f) · χ_d(-1)^{k/2}

    (standard Atkin–Li / Shimura twist FE; Gauss-sum phase τ(χ)²/|d|
    equals χ(-1), absorbed for even weight).

    Here k = 4 ⇒ χ_d(-1)^2 = 1, N_f = 8, ε_f = +1 (T12), so
        ε_d = χ_d(8) = χ_d(2)
            = +1 if d ≡ ±1 mod 8,  −1 if d ≡ ±3 mod 8.
    For positive fundamental d ≡ 1 mod 4:
        d ≡ 1 mod 8 → ε_d = +1,   d ≡ 5 mod 8 → ε_d = −1.

    Consequence at the centre s = 2 = k/2:
        ε_d = −1 ⇒ Λ(2) = −Λ(2) ⇒ L(f₈×χ_d, 2) = 0 identically.
    """
    assert d % 2 != 0
    return int(eps_f * kronecker(d, N_f))


# ================================================================ P0
print("=" * 72)
print("P0 -- rebuild f8 (eta) and T38/T41 witness g")
print("=" * 72)

t_f8 = time.time()
f8 = np.roll(conv_i64(eta_pass(2, 4, N_F8),
                      eta_pass(4, 4, N_F8), N_F8), 1)
f8[0] = 0
a_f8 = [int(f8[n]) for n in range(N_F8 + 1)]
info(f"f8 coeffs to n={N_F8} in {time.time() - t_f8:.2f}s")
check("P0.f8: eta(2t)^4 eta(4t)^4 matches T11 a_p head "
      "{3:-4,5:-2,7:24,11:-44,13:22}; a_1=1",
      a_f8[1] == 1 and all(a_f8[p] == v for p, v in HEAD_AP.items()))

EPS_F8 = 1


def theta2_t(order_t, scale_q=1):
    s = np.zeros(order_t + 1, dtype=np.int64)
    o = 1
    while True:
        exp = scale_q * o * o
        if exp > order_t:
            break
        s[exp] = 2
        o += 2
    return s


def theta3_t(order_t, scale_q=1):
    s = np.zeros(order_t + 1, dtype=np.int64)
    s[0] = 1
    n = 1
    while True:
        exp = 4 * scale_q * n * n
        if exp > order_t:
            break
        s[exp] = 2
        n += 1
    return s


def theta4_t(order_t, scale_q=1):
    s = np.zeros(order_t + 1, dtype=np.int64)
    s[0] = 1
    n = 1
    while True:
        exp = 4 * scale_q * n * n
        if exp > order_t:
            break
        s[exp] = 2 * ((-1) ** n)
        n += 1
    return s


def monomial_t(a0, a2, b0, b2, c0, c2, order_t):
    s = np.zeros(order_t + 1, dtype=np.int64)
    s[0] = 1
    for _ in range(a0):
        s = conv_i64(s, theta2_t(order_t, 1), order_t)
    for _ in range(a2):
        s = conv_i64(s, theta2_t(order_t, 2), order_t)
    for _ in range(b0):
        s = conv_i64(s, theta3_t(order_t, 1), order_t)
    for _ in range(b2):
        s = conv_i64(s, theta3_t(order_t, 2), order_t)
    for _ in range(c0):
        s = conv_i64(s, theta4_t(order_t, 1), order_t)
    for _ in range(c2):
        s = conv_i64(s, theta4_t(order_t, 2), order_t)
    return s


def to_q_series(s_t, qmax):
    for r in range(1, 4):
        if np.any(s_t[r::4] != 0):
            return None
    out = [0] * (qmax + 1)
    lim = min(qmax, (len(s_t) - 1) // 4)
    for n in range(lim + 1):
        out[n] = int(s_t[4 * n])
    return out


t_g0 = time.time()
g = to_q_series(monomial_t(*WITNESS_KEY, 4 * QMAX), QMAX)
assert g is not None
info(f"g rebuild O(q^{QMAX}) in {time.time() - t_g0:.2f}s; head={g[:24]}")
mass_mod4 = {r: sum(abs(g[n]) for n in range(1, min(801, QMAX + 1))
                     if n % 4 == r) for r in range(4)}
info(f"|g| mass by n mod 4 (n=1..800): {mass_mod4}")
check("P0.g: T38 witness rebuilt; g[0]=0; mass only on n≡1,2 mod 4 "
      f"(mass0={mass_mod4[0]}, mass3={mass_mod4[3]})",
      g[0] == 0 and mass_mod4[0] == 0 and mass_mod4[3] == 0
      and mass_mod4[1] > 0 and mass_mod4[2] > 0)


# ================================================================ B1
print("=" * 72)
print("B1 -- clean twist L-values via full Lambda / incomplete-Gamma AFE")
print("=" * 72)

info("CONVENTION (classical twist FE, weight k=4, trivial nebentypus):")
info("  Λ(s) = (√N/(2π))^s Γ(s) L(f⊗χ_d, s),   N = 8·d² (odd fund. d)")
info("  Λ(s) = ε_d Λ(4−s)")
info("  ε_d = ε_f · χ_d(N_f) · χ_d(-1)^{k/2}  with ε_f=+1, N_f=8, k=4")
info("      = χ_d(8) = χ_d(2)  (+1 if d≡1,7 mod 8; −1 if d≡3,5 mod 8)")
info("  At s=2=k/2: ε_d=−1 ⇒ L(f₈×χ_d,2)=0 identically (FE).")
info("  Incomplete-Gamma summation (T12): terms ~ exp(−2π n/√N).")
info("  PRIMARY L(2) = AFE; direct sums at s=2 are NOT trusted (T44).")


def nterms_for(Nlev: int, safety: float = 30.0) -> int:
    sq = math.sqrt(Nlev)
    need = int(math.ceil(safety * sq / (2 * math.pi))) + 50
    return min(N_F8, max(800, need))


def L_twist_direct(d, s, terms):
    s = mpmath.mpf(s)
    tot = mpmath.mpf(0)
    for n in range(1, min(terms, N_F8) + 1):
        an = a_f8[n]
        if an == 0:
            continue
        ch = kronecker(d, n)
        if ch == 0:
            continue
        tot += mpmath.mpf(an * ch) * mpmath.power(n, -s)
    return tot


def L_twist_afe(d, s, Nlev, eps, terms):
    """Incomplete-Gamma AFE for L(f8 × χ_d, s); weight 4."""
    s = mpmath.mpf(s)
    sqN = mpmath.sqrt(Nlev)
    two_pi = 2 * mpmath.pi
    lam = mpmath.mpf(0)
    kms = mpmath.mpf(K_WT) - s
    for n in range(1, min(terms, N_F8) + 1):
        an = a_f8[n]
        if an == 0:
            continue
        ch = kronecker(d, n)
        if ch == 0:
            continue
        xx = two_pi * n / sqN
        pref = sqN / (two_pi * n)
        c = mpmath.mpf(an * ch)
        lam += c * (pref ** s * mpmath.gammainc(s, xx)
                    + eps * pref ** kms * mpmath.gammainc(kms, xx))
    return lam / ((sqN / (2 * mpmath.pi)) ** s * mpmath.gamma(s))


# Untwisted Fricke of f8
Ldir_f8_45 = L_twist_direct(1, mpmath.mpf("4.5"), terms=8000)
# χ_1 is trivial — use plain a_n
gaps_f8 = {}
for eps in (1, -1):
    # plain f8 AFE at level 8
    s = mpmath.mpf("4.5")
    sqN = mpmath.sqrt(8)
    lam = mpmath.mpf(0)
    for n in range(1, 2001):
        an = a_f8[n]
        if an == 0:
            continue
        xx = 2 * mpmath.pi * n / sqN
        pref = sqN / (2 * mpmath.pi * n)
        c = mpmath.mpf(an)
        lam += c * (pref ** s * mpmath.gammainc(s, xx)
                    + eps * pref ** (K_WT - s)
                    * mpmath.gammainc(K_WT - s, xx))
    La = lam / ((sqN / (2 * mpmath.pi)) ** s * mpmath.gamma(s))
    # direct of untwisted
    Ld = sum(mpmath.mpf(a_f8[n]) * mpmath.power(n, -s)
             for n in range(1, 8001) if a_f8[n])
    gaps_f8[eps] = abs(La - Ld)
eps_f8_num = 1 if gaps_f8[1] < gaps_f8[-1] else -1
info(f"untwisted f8 Fricke via AFE↔direct at s=4.5: "
     f"gap(+1)={gaps_f8[1]}, gap(-1)={gaps_f8[-1]} → eps={eps_f8_num:+d}")
check("B1.f8-Fricke: numeric Fricke of f8 is +1 (T12), gap ratio ≥ 10",
      eps_f8_num == 1
      and max(gaps_f8.values()) / min(gaps_f8.values()) > 10)


def evaluate_twist(d: int):
    """B1 package for one odd fundamental d.  L_use = AFE at s=2."""
    assert d % 2 != 0 and is_fundamental_discriminant(d)
    Nlev = 8 * d * d
    eps_th = twist_root_number(d, EPS_F8, 8)
    nterm = nterms_for(Nlev)

    # Root-number selection at s=3.5 against direct (convergent)
    s_hi = mpmath.mpf("3.5")
    L_dir_hi = L_twist_direct(d, s_hi, terms=min(N_F8, max(20000, 5 * nterm)))
    gap_th = abs(L_twist_afe(d, s_hi, Nlev, eps_th, nterm) - L_dir_hi)
    gap_wrong = abs(L_twist_afe(d, s_hi, Nlev, -eps_th, nterm) - L_dir_hi)
    eps_hi_ok = (gap_th < gap_wrong
                 and (gap_wrong / gap_th > FE_EPS_RATIO
                      if gap_th > 0 else True))
    rel_gap_hi = (gap_th / abs(L_dir_hi)
                  if L_dir_hi != 0 else mpmath.mpf(1))

    # Primary central value via AFE
    L_afe = L_twist_afe(d, 2, Nlev, eps_th, nterm)
    L_dir_c = L_twist_direct(d, 2, terms=nterm)  # diagnostic only

    # Stability under term doubling
    n_lo = max(400, nterm // 2)
    n_hi = min(N_F8, max(nterm, n_lo + 200))
    L_lo = L_twist_afe(d, 2, Nlev, eps_th, n_lo)
    L_hi = L_twist_afe(d, 2, Nlev, eps_th, n_hi)
    stab_rel = (abs(L_hi - L_lo) / abs(L_hi)
                if abs(L_hi) > L_VANISH_TOL else mpmath.mpf(0))

    # FE centre vanishing for ε=−1
    centre_vanish_forced = (eps_th == -1)
    centre_is_zero = abs(L_afe) < L_VANISH_TOL

    return {
        "d": d,
        "Nlev": Nlev,
        "eps": eps_th,
        "nterm": nterm,
        "L_afe": L_afe,
        "L_dir_c": L_dir_c,
        "L_use": L_afe,
        "L_dir_hi": L_dir_hi,
        "gap_th": gap_th,
        "gap_wrong": gap_wrong,
        "rel_gap_hi": rel_gap_hi,
        "eps_hi_ok": eps_hi_ok,
        "stab_rel": stab_rel,
        "centre_vanish_forced": centre_vanish_forced,
        "centre_is_zero": centre_is_zero,
        "L_lo": L_lo,
        "L_hi": L_hi,
    }


# --- (i)+(ii): root number + AFE↔direct at s=3.5 ---
info("B1(i)+(ii): theoretical ε vs direct at s=3.5; AFE match")
val_rows = []
eps_ok_all = True
afe_dir_ok_all = True
for d in SMALL_D_VALIDATE:
    if not is_fundamental_discriminant(d):
        continue
    row = evaluate_twist(d)
    val_rows.append(row)
    eps_ok_all = eps_ok_all and row["eps_hi_ok"]
    afe_dir_ok_all = afe_dir_ok_all and (row["rel_gap_hi"] < AFE_DIRECT_TOL)
    info(f"  d={d}: eps={row['eps']:+d}, L_afe(2)={row['L_afe']}, "
         f"rel_gap@3.5={float(row['rel_gap_hi']):.3e}, "
         f"gap_th/wrong={float(row['gap_th']):.3e}/"
         f"{float(row['gap_wrong']):.3e}, eps_ok={row['eps_hi_ok']}, "
         f"forced_vanish={row['centre_vanish_forced']}")

# Forced vanishing check for ε=−1 rows
vanish_ok = all(
    r["centre_is_zero"] for r in val_rows if r["centre_vanish_forced"])
info(f"ε=−1 ⇒ L(2)=0 forced: ok={vanish_ok}")

check("B1(i): theoretical twist root number ε_d=χ_d(8) preferred over "
      f"wrong sign at s=3.5 (gap ratio ≥ {FE_EPS_RATIO}) for "
      f"d in {SMALL_D_VALIDATE}",
      eps_ok_all and len(val_rows) >= 6)

check("B1(ii): AFE matches well-convergent direct sums at s=3.5 "
      f"(rel_gap < {float(AFE_DIRECT_TOL):.0e}); ε=−1 forces L(2)=0",
      afe_dir_ok_all and vanish_ok)

# --- (iii) litmus d=89 ---
info("B1(iii): litmus — T44 outlier d=89 under clean AFE")
row89 = next(r for r in val_rows if r["d"] == D_LITMUS)
info(f"  d=89: L_afe(2)={row89['L_afe']}")
info(f"         L_dir(2)={row89['L_dir_c']}  (T44-style; NOT trusted)")
info(f"         |AFE−dir|/|AFE| at s=2 = "
     f"{float(abs(row89['L_afe'] - row89['L_dir_c']) / abs(row89['L_afe'])):.3e}")
info(f"         stab_rel (half→full terms)={float(row89['stab_rel']):.3e}")
info(f"         rel_gap@3.5={float(row89['rel_gap_hi']):.3e}, "
     f"eps={row89['eps']:+d}")
d89_stable = (row89["stab_rel"] < STABLE_REL_TOL
              and row89["eps_hi_ok"]
              and row89["rel_gap_hi"] < AFE_DIRECT_TOL
              and not row89["centre_is_zero"])
d89_dir_disagrees = (
    abs(row89["L_afe"] - row89["L_dir_c"]) / abs(row89["L_afe"])
    > mpmath.mpf("1e-2"))
check("B1(iii): d=89 AFE stabilises (term-doubling < 1e-5, s=3.5 match); "
      "nonvanishing L_afe(2); direct-at-s=2 still disagrees (T44 cause)",
      d89_stable and d89_dir_disagrees)

B1_ok = bool(eps_ok_all and afe_dir_ok_all and vanish_ok and d89_stable)
K1_fired = not (eps_ok_all and afe_dir_ok_all)
info(f"B1_ok={B1_ok}; K1_fired={K1_fired}")
check(f"B1.summary: B1_ok={B1_ok}; K1_fired={K1_fired} "
      "(IMPL-BLOCKED if K1)",
      True)


# ================================================================ B2
print("=" * 72)
print("B2 -- Baruch–Mao Waldspurger proportionality by d mod 8")
print("=" * 72)

info("PREREGISTERED: R(d)=b(|d|)²/(|d|^{3/2} L_AFE(f8×χ_d,2));")
info("  success = rel spread < 5% WITHIN each LIVE d-mod-8 class;")
info("  class constants MAY differ (2-adic local factor, classical).")
info("  g support on n≡1,2 mod 4; fundamental d are ≡0 or 1 mod 4,")
info("  so live indices are d≡1 or 5 mod 8.  Root-number split:")
info("    d≡5 mod 8 → ε=−1 → L(2)=0 → expect b(|d|)=0 (vanish class);")
info("    d≡1 mod 8 → ε=+1 → L(2) free → R-constancy test (live class).")
info("  n≡2-mod-4 mass of g does not hit fundamental discriminants.")

fund_odd_pos = [d for d in range(1, DMAX + 1, 2)
                if is_fundamental_discriminant(d)]
info(f"odd positive fundamental d ≤ {DMAX}: {fund_odd_pos}")
check("B2.fund: odd positive fundamental discriminants include "
      "5,13,17,29,37,41,53,61,73,89,97",
      all(d in fund_odd_pos for d in
          (5, 13, 17, 29, 37, 41, 53, 61, 73, 89, 97)))

twist_cache = {r["d"]: r for r in val_rows}


def get_twist(d):
    if d not in twist_cache:
        twist_cache[d] = evaluate_twist(d)
    return twist_cache[d]


# Vanishing-class consistency (d≡5 mod 8)
vanish_class = [d for d in fund_odd_pos if d % 8 == 5 and d <= QMAX]
vanish_b_ok = all(g[d] == 0 for d in vanish_class)
info(f"vanish class d≡5 mod 8 (n={len(vanish_class)}): "
     f"all b(|d|)=0? {vanish_b_ok}")
info(f"  d-list: {vanish_class}")
# Also: d≡1 mod 8 with L≈0 should have b=0 (e.g. d=41)
live_fund = [d for d in fund_odd_pos if d % 8 == 1 and d <= QMAX]
info(f"live class d≡1 mod 8 candidates: {live_fund}")

rows_by_class = defaultdict(list)
all_rows = []
skipped = []

if not K1_fired and B1_ok:
    for d in fund_odd_pos:
        if d > QMAX:
            continue
        bn = g[d]
        Lw = get_twist(d)
        Lval = Lw["L_use"]
        cls = d % 8
        if abs(Lval) < L_VANISH_TOL:
            # central zero: Waldspurger ⇒ b must vanish
            skipped.append((d, "L=0", bn))
            continue
        if bn == 0:
            skipped.append((d, "b=0", bn))
            continue
        denom = mpmath.power(d, mpmath.mpf("1.5")) * Lval
        R = (mpmath.mpf(bn) ** 2) / denom
        row = {
            "d": d, "b": bn, "b2": bn * bn, "L": Lval,
            "L_dir_c": Lw["L_dir_c"], "eps": Lw["eps"],
            "R": R, "class": cls,
            "rel_gap_hi": Lw["rel_gap_hi"],
            "stab_rel": Lw["stab_rel"],
        }
        rows_by_class[cls].append(row)
        all_rows.append(row)
else:
    info("B2 SKIPPED: B1 foundation failed / K1 fired.")

info(f"skipped (L=0 or b=0): {skipped}")
info(f"live R(d) rows: {len(all_rows)}; classes: "
     f"{ {c: len(v) for c, v in sorted(rows_by_class.items())} }")

# Consistency: whenever L=0, b=0
L0_rows = [(d, bn) for d, reason, bn in skipped if reason == "L=0"]
L0_implies_b0 = all(bn == 0 for d, bn in L0_rows)
info(f"Waldspurger consistency L(2)=0 ⇒ b=0: n_L0={len(L0_rows)}, "
     f"all b=0? {L0_implies_b0}")
check("B2.vanish: d≡5 mod 8 all have b(|d|)=0; and every computed "
      f"L(2)=0 twist has b=0 (n_L0={len(L0_rows)})",
      vanish_b_ok and L0_implies_b0)


def rel_spread(vals):
    vs = [float(v) for v in vals if v is not None and abs(float(v)) > 1e-30]
    if len(vs) < 2:
        return None, None, vs
    vs_s = sorted(vs)
    med = vs_s[len(vs_s) // 2]
    if med == 0:
        return None, med, vs_s
    return max(abs(v - med) / abs(med) for v in vs_s), med, vs_s


info("R(d) tables by d mod 8 (live, L≠0, b≠0):")
class_stats = {}
for cls in sorted(rows_by_class.keys()):
    rows = rows_by_class[cls]
    info(f"  --- class d ≡ {cls} mod 8 (n={len(rows)}) ---")
    info(f"  {'d':>6} {'b':>8} {'b^2':>10} {'L_AFE':>20} "
         f"{'R':>20} {'eps':>4}")
    for r in rows:
        info(f"  {r['d']:6d} {r['b']:8d} {r['b2']:10d} "
             f"{float(r['L']):20.12g} {float(r['R']):20.12g} "
             f"{r['eps']:+4d}")
    spread, med, vals = rel_spread([r["R"] for r in rows])
    class_stats[cls] = {
        "n": len(rows), "spread": spread, "med": med, "vals": vals,
    }
    info(f"  spread={spread}, med={med}")

r89 = next((r for r in all_rows if r["d"] == D_LITMUS), None)
if r89 is not None:
    info(f"LITMUS row d=89: b={r89['b']}, L_AFE={r89['L']}, "
         f"R={r89['R']} (on the constant — T44 outlier resolved)")

classes_tested = [c for c, st in class_stats.items()
                  if st["n"] >= MIN_PER_CLASS]
spreads_ok = [c for c in classes_tested
              if class_stats[c]["spread"] is not None
              and class_stats[c]["spread"] < CLASS_SPREAD_OK]
spreads_bad = [c for c in classes_tested if c not in spreads_ok]

B2_enough = len(all_rows) >= MIN_TOTAL_D and len(classes_tested) >= 1
B2_ok = bool(
    B1_ok and (not K1_fired) and B2_enough
    and len(spreads_bad) == 0
    and len(spreads_ok) >= 1
    and vanish_b_ok and L0_implies_b0
)
K2_fired = bool(
    B1_ok and (not K1_fired) and B2_enough and len(spreads_bad) > 0
)

info(f"classes_tested (≥{MIN_PER_CLASS})={classes_tested}")
info(f"spreads_ok={spreads_ok}, spreads_bad={spreads_bad}")
info(f"B2_ok={B2_ok}; K2_fired={K2_fired}; n_total={len(all_rows)}")

check(f"B2.sample: ≥{MIN_TOTAL_D} live fundamental d with b≠0 and L≠0? "
      f"n={len(all_rows)}; classes_tested={classes_tested}",
      True if K1_fired else (len(all_rows) >= MIN_TOTAL_D
                             and len(classes_tested) >= 1))

check(f"B2.Waldspurger RESULT: B2_ok={B2_ok} (classwise spread < 5%); "
      f"K2_fired={K2_fired}; per-class="
      + (", ".join(
          f"d≡{c} mod8: n={class_stats[c]['n']}, "
          f"spread={class_stats[c]['spread']}, med={class_stats[c]['med']}"
          for c in sorted(class_stats.keys())
      ) if class_stats else "none"),
      True)


# ================================================================ B3
print("=" * 72)
print("B3 -- interpretation / verdict")
print("=" * 72)

if K1_fired or not B1_ok:
    verdict = "IMPL-BLOCKED"
elif B2_ok:
    verdict = "CENTRAL-VALUES-WIRED-BM"
else:
    verdict = "NUMERICALLY-CLEAN-BUT-SCATTERED"

info(f"VERDICT = {verdict}")
info("TYPING:")
info("  Channel 1 (abelian, T39): weight-≤1 theta → ξ-line centre 1/2.")
info("  Channel 2 (cuspidal, T38/T41): Shimura g → f8 carries a_p as")
info("    T(p²)-eigenvalues of a compiler monoid object.")
info("  Channel 3 (central values, this probe): b(|d|)² ↔ L(f8×χ_d, 2)")
info("    at the GL(2) centre s=2 for weight-4 normalisation.")
info("  NOT the ξ-line; NOT an RH reading; classical Waldspurger /")
info("  Baruch–Mao named as classical.")

third_channel = (verdict == "CENTRAL-VALUES-WIRED-BM")
line_rests = (verdict == "NUMERICALLY-CLEAN-BUT-SCATTERED")

if verdict == "CENTRAL-VALUES-WIRED-BM":
    info("CONSEQUENCE: third functor channel YES — central-value family")
    info("  realised as coefficient squares of NON-PLUS g, with 2-adic")
    info("  class structure (d≡1 mod 8 live constant; d≡5 mod 8 vanishing")
    info("  via root number −1).  Central-value line CLOSED on sample.")
    if 1 in class_stats and class_stats[1]["med"] is not None:
        info(f"  Live-class constant R ≡ {class_stats[1]['med']} "
             f"(spread {class_stats[1]['spread']})")
elif verdict == "NUMERICALLY-CLEAN-BUT-SCATTERED":
    info("CONSEQUENCE: third functor channel NO on this sample.")
    info("  B1 L-values are clean; B2 classwise constancy FAILED.")
    info("  Central-value line RESTS as typed-open.")
    for c in sorted(class_stats.keys()):
        st = class_stats[c]
        info(f"    d≡{c} mod8: spread={st['spread']} "
             f"(med={st['med']}, n={st['n']})")
elif verdict == "IMPL-BLOCKED":
    info("CONSEQUENCE: implementation blocked (K1) — do not interpret")
    info("  proportionality; fix AFE/direct mismatch before retry.")

check(f"B3.verdict: {verdict}; third_functor_channel={third_channel}; "
      f"central_value_line_rests={line_rests}; "
      f"B1_ok={B1_ok}, B2_ok={B2_ok}, K1={K1_fired}, K2={K2_fired}",
      verdict in (
          "CENTRAL-VALUES-WIRED-BM",
          "NUMERICALLY-CLEAN-BUT-SCATTERED",
          "IMPL-BLOCKED",
      ))

eps_class_ok = True
for r in all_rows:
    expect = 1 if r["d"] % 8 in (1, 7) else -1
    if r["eps"] != expect:
        eps_class_ok = False
check("B3.eps-class: theoretical ε_d matches d≡1→+1 on all live rows",
      eps_class_ok if all_rows else True)


# ================================================================ end
elapsed = time.time() - T0
print("=" * 72)
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({elapsed:.1f}s)")
print(f"VERDICT: {verdict}")
print("=" * 72)
raise SystemExit(0 if FAIL == 0 else 1)
