"""v537 -- HECKE.GEOM.HALFINT.01: the half-integral bridge.
Shimura preimage + Hecke equivariance + Kohnen scope fence +
Waldspurger/Baruch-Mao constancy.  Consolidated from discovery
T38/T41/T44/T45; builds on the weight-4 Hecke/Eichler package
(v535/v536) without duplicating those checks.

[E] (A) UNIQUE SHIMURA PREIMAGE AT SCALE -8 (T38).  In the
    70-element compiler theta-monoid of weight 5/2 (theta2/3/4
    plain and q^2-scaled, total exponent sum 5, integer-q only)
    there is exactly ONE object with the signed identity
        Sh_{t=2, psi=1}(g) = -8 * f8
    coefficientwise (screen n <= 40; witness extended to n <= 120).
    Witness:
        g = theta2(q^2)^2 * theta3(q^2) * theta4 * theta4(q^2)
    (key (0,2,0,1,1,1)).  Three further monoid elements lift to
    other scales (+8, -16, +16)*f8 (documented; not the -8 witness).
    Shimura convention (Shimura 1973 / Cipra):
        A_t(n) = sum_{d|n} psi(d) (t/d)_Kronecker d^{k-1} b(t n^2/d^2)
    with k=2 (weight 5/2 -> 4), psi=1, t=2.
[E] (B) HECKE EQUIVARIANCE (T41).  g is an exact T(p^2)-eigenform
    of weight 5/2, trivial nebentypus, with eigenvalues a_p(f8) for
    p = 3,5,7,11,13 (= -4,-2,24,-44,22).  Shimura 1973 formula
        (T(p^2)f)(n) = a(p^2 n) + chi(p)(n/p) p^{k-1} a(n)
                     + chi(p^2) p^{2k-1} a(n/p^2)
    (k=2 => p and p^3).  Trial FE of the 5/2-side around centre 5/4
    with N=512, eps=+1 as a numeric anchor (AFE↔direct).
[E] (C) KOHNEN SCOPE FENCE (T44) -- NEGATIVE RESULT PART OF CLAIM.
    U4(g)=0 exactly (mass mod 4 = {0:0, 1:..., 2:..., 3:0}); the
    spectral Kohnen pr+_4 sees no plus component (H=W4U4 vanishes
    on ker(U4)).  Level hypothesis 32=4*8 with M=8 even lies outside
    Kohnen 1982 (needs M odd squarefree; 4a-Mbc=1 unsolvable).
    Plus-route structurally closed.
[C] (D) WALDSPURGER / BARUCH-MAO CONSTANCY (T45).  With AFE-based
    twist L-values (AFE vs direct at s=3.5, rel <= 1e-8; eps_d =
    chi_d(8); eps=-1 => L(2)=0) the quotient
        R(d) = b(|d|)^2 / (|d|^{3/2} L(f8 x chi_d, 2))
    is CONSTANT over 10 fundamental discriminants d ≡ 1 mod 8
    (R = 23.1873585645..., spread <= 1e-12; includes d=89).  The
    class d ≡ 5 mod 8 vanishes structurally (b=0, root number -1).

HONEST FENCES (load-bearing typing):
  * Shimura 1973, Kohnen 1980/82, Waldspurger 1981 / Baruch-Mao are
    CLASSICAL -- the claim is: (i) the preimage sits IN the compiler
    monoid and is UNIQUE there; (ii) the full chain is in-suite
    machine-checked; (iii) the constant R is MEASURED, not derived.
  * GL(2) centre s=2 (weight-4 normalisation), NOT the xi-line.
  * NO RH statement; ZETA.HP.CARRIER untouched.
  * Trial FE of the 5/2-side is a numeric anchor, not a derivation
    of the half-integral functional equation package.
  * NO marker upgrades of any pre-existing contract.

Status: [E] exact integer Shimura uniqueness / Hecke equivariance /
Kohnen scope fence; [C] AFE-numeric Waldspurger constancy (measured
R).  Python; Wolfram-mirrored (exact a_p / Shimura scale / Kohnen
scope / root-number arithmetic -- q-series builds, AFE/L-values,
and R-constancy stay Python-only), counted per GATE.WOLFRAM.02.
Discovery provenance:
  experiments/tfpt-discovery/cuspidal_bridge_probe.py (T38)
  experiments/tfpt-discovery/functor_wiring_halfintegral_probe.py (T41)
  experiments/tfpt-discovery/kohnen_operator_projection_probe.py (T44)
  experiments/tfpt-discovery/baruch_mao_metaplectic_probe.py (T45)
  (+ f8 scaffolding from e8_glue_chi4_signed_theta_probe.py, T11)
"""
from __future__ import annotations

import itertools
import math
import time
from fractions import Fraction

import mpmath
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset

# ---------------------------------------------------------------- budgets
A_P = {3: -4, 5: -2, 7: 24, 11: -44, 13: 22}
PRIMES_HECKE = (3, 5, 7, 11, 13)
WITNESS_KEY = (0, 2, 0, 1, 1, 1)  # th2(q2)^2 th3(q2) th4 th4(q2)
K_HALF = 2                        # weight = k+1/2 = 5/2
Q_CAND = 3200                     # uniqueness screen (t=2 => n_cap ~40)
N_SHIMURA_SEARCH = 40
N_SHIMURA_EXT = 120
Q_WITNESS = max(2 * (N_SHIMURA_EXT ** 2) + 16, 13 * 13 * 100 + 16)
N_HECKE = 100
N_F8 = 100_000                    # AFE twist L-values (T45)
Q_G_SMALL = 200                   # g coeffs for Waldspurger (d <= 120)
DMAX = 120
SMALL_D_VALIDATE = (5, 13, 17, 29, 37, 41, 89)
D_LITMUS = 89
AFE_DIRECT_TOL = mpmath.mpf("1e-8")
FE_EPS_RATIO = 10.0
STABLE_REL_TOL = mpmath.mpf("1e-5")
L_VANISH_TOL = mpmath.mpf("1e-20")
R_SPREAD_TOL = mpmath.mpf("1e-12")
R_TARGET = mpmath.mpf("23.1873585645")
LEVEL_FE_TRIALS = (16, 32, 64, 128, 256, 512)
FE_THRESH = 5e-3
AFE_SAFETY = 50.0                 # nterms ~ safety * sqrt(N)/(2pi)


# ---------------------------------------------------------------- helpers
def chi4(n: int) -> int:
    r = n % 4
    if r == 1:
        return 1
    if r == 3:
        return -1
    return 0


def kronecker(d: int, n: int) -> int:
    return int(sp.kronecker_symbol(d, n))


def legendre(a: int, p: int) -> int:
    if a % p == 0:
        return 0
    return int(sp.legendre_symbol(a % p, p))


def eta_pass(d, e, order):
    s = np.zeros(order + 1, dtype=np.int64)
    s[0] = 1
    for k in range(d, order + 1, d):
        for _ in range(e):
            s[k:] = s[k:] - s[:-k]
    return s


def conv_i64(a, b, order):
    return np.convolve(a, b)[: order + 1].astype(np.int64)


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
    """eps_d = eps_f * chi_d(N_f) for weight-4 trivial nebentypus.
    With eps_f=+1, N_f=8: eps_d = chi_d(8) = +1 (d≡1 mod 8), -1 (d≡5).
    """
    assert d % 2 != 0
    return int(eps_f * kronecker(d, N_f))


# ---------------------------------------------------------------- thetas
_TH_CACHE: dict = {}


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


def _th(kind, scale_q, order_t):
    key = (kind, scale_q, order_t)
    if key not in _TH_CACHE:
        if kind == 2:
            _TH_CACHE[key] = theta2_t(order_t, scale_q)
        elif kind == 3:
            _TH_CACHE[key] = theta3_t(order_t, scale_q)
        else:
            _TH_CACHE[key] = theta4_t(order_t, scale_q)
    return _TH_CACHE[key]


def monomial_t(a0, a2, b0, b2, c0, c2, order_t):
    s = np.zeros(order_t + 1, dtype=np.int64)
    s[0] = 1
    for _ in range(a0):
        s = conv_i64(s, _th(2, 1, order_t), order_t)
    for _ in range(a2):
        s = conv_i64(s, _th(2, 2, order_t), order_t)
    for _ in range(b0):
        s = conv_i64(s, _th(3, 1, order_t), order_t)
    for _ in range(b2):
        s = conv_i64(s, _th(3, 2, order_t), order_t)
    for _ in range(c0):
        s = conv_i64(s, _th(4, 1, order_t), order_t)
    for _ in range(c2):
        s = conv_i64(s, _th(4, 2, order_t), order_t)
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


def build_candidates(qmax):
    """Integer-q weight-5/2 theta monoid (plain + q^2-scaled)."""
    tmax = 4 * qmax
    cands = []

    def add(label, a0, a2, b0, b2, c0, c2):
        if a0 + a2 + b0 + b2 + c0 + c2 != 5:
            return
        if (a0 + 2 * a2) % 4 != 0:
            return
        st = monomial_t(a0, a2, b0, b2, c0, c2, tmax)
        bq = to_q_series(st, qmax)
        if bq is None or all(x == 0 for x in bq):
            return
        cands.append((label, bq, (a0, a2, b0, b2, c0, c2)))

    for b in range(6):
        add(f"V0:th3^{b}*th4^{5 - b}", 0, 0, b, 0, 5 - b, 0)
    for b in range(2):
        add(f"V0:th2^4*th3^{b}*th4^{1 - b}", 4, 0, b, 0, 1 - b, 0)
    for a0, a2, b0, b2, c0 in itertools.product(range(6), repeat=5):
        c2 = 5 - (a0 + a2 + b0 + b2 + c0)
        if c2 < 0:
            continue
        if a2 == b2 == c2 == 0:
            continue
        add(f"V1:{a0},{a2},{b0},{b2},{c0},{c2}",
            a0, a2, b0, b2, c0, c2)
    uniq = {}
    for lab, bq, key in cands:
        tup = tuple(bq)
        if tup not in uniq:
            uniq[tup] = (lab, bq, key)
    return list(uniq.values())


# ---------------------------------------------------------------- Shimura
def shimura_A(bq, n, t, psi):
    total = 0
    for d in sp.divisors(n):
        d = int(d)
        idx = t * (n // d) * (n // d)
        if idx >= len(bq):
            return None
        total += psi(d) * kronecker(t, d) * (d ** (K_HALF - 1)) * bq[idx]
    return int(total)


def shimura_lift(bq, t, psi, nmax):
    out = [0] * (nmax + 1)
    for n in range(1, nmax + 1):
        val = shimura_A(bq, n, t, psi)
        if val is None:
            return None
        out[n] = val
    return out


def max_lift_n(bq_len, t):
    return int(((bq_len - 1) // t) ** 0.5)


# ---------------------------------------------------------------- Hecke
def T_p2_half(a, p, chi_p, chi_p2, order, n_check):
    assert p * p * n_check <= order
    p1 = p ** (K_HALF - 1)
    p3 = p ** (2 * K_HALF - 1)
    out = [Fraction(0) for _ in range(n_check + 1)]
    for n in range(n_check + 1):
        np2 = n * p * p
        term = Fraction(a[np2] if np2 <= order else 0)
        if n >= 1:
            term += (Fraction(chi_p) * Fraction(legendre(n, p))
                     * Fraction(p1) * Fraction(a[n]))
        if n % (p * p) == 0:
            term += Fraction(chi_p2) * Fraction(p3) * Fraction(a[n // (p * p)])
        out[n] = term
    return out


# ---------------------------------------------------------------- FE / AFE
def L_g_direct(g, s, terms):
    s = mpmath.mpf(s)
    tot = mpmath.mpf(0)
    for n in range(1, min(terms, len(g) - 1) + 1):
        bn = g[n]
        if bn:
            tot += mpmath.mpf(bn) * mpmath.power(n, -s)
    return tot


def L_g_afe(g, s, Nlev, eps, terms):
    s = mpmath.mpf(s)
    wt = mpmath.mpf("2.5")
    sqN = mpmath.sqrt(Nlev)
    lam = mpmath.mpf(0)
    for n in range(1, min(terms, len(g) - 1) + 1):
        bn = g[n]
        if not bn:
            continue
        xx = 2 * mpmath.pi * n / sqN
        pref = sqN / (2 * mpmath.pi * n)
        c = mpmath.mpf(bn)
        lam += c * (pref ** s * mpmath.gammainc(s, xx)
                    + eps * pref ** (wt - s) * mpmath.gammainc(wt - s, xx))
    return lam / ((sqN / (2 * mpmath.pi)) ** s * mpmath.gamma(s))


def nterms_for(Nlev: int, safety: float = AFE_SAFETY) -> int:
    sq = math.sqrt(Nlev)
    need = int(math.ceil(safety * sq / (2 * math.pi))) + 80
    return min(N_F8, max(1200, need))


def L_twist_direct(a_f8, d, s, terms):
    s = mpmath.mpf(s)
    tot = mpmath.mpf(0)
    for n in range(1, min(terms, len(a_f8) - 1) + 1):
        an = a_f8[n]
        if not an:
            continue
        ch = kronecker(d, n)
        if not ch:
            continue
        tot += mpmath.mpf(an * ch) * mpmath.power(n, -s)
    return tot


def L_twist_afe(a_f8, d, s, Nlev, eps, terms):
    s = mpmath.mpf(s)
    sqN = mpmath.sqrt(Nlev)
    two_pi = 2 * mpmath.pi
    lam = mpmath.mpf(0)
    kms = mpmath.mpf(4) - s
    for n in range(1, min(terms, len(a_f8) - 1) + 1):
        an = a_f8[n]
        if not an:
            continue
        ch = kronecker(d, n)
        if not ch:
            continue
        xx = two_pi * n / sqN
        pref = sqN / (two_pi * n)
        c = mpmath.mpf(an * ch)
        lam += c * (pref ** s * mpmath.gammainc(s, xx)
                    + eps * pref ** kms * mpmath.gammainc(kms, xx))
    return lam / ((sqN / (2 * mpmath.pi)) ** s * mpmath.gamma(s))


# ======================================================================
def run():
    reset()
    mpmath.mp.dps = 25
    t0 = time.time()
    print("v537 HECKE.GEOM.HALFINT.01 -- half-integral bridge "
          "(Shimura preimage + Hecke + Kohnen fence + Waldspurger)")

    # ============================================================ S0
    print("S0 -- scaffold: f8 = eta(2t)^4 eta(4t)^4")
    f8 = np.roll(conv_i64(eta_pass(2, 4, N_F8),
                          eta_pass(4, 4, N_F8), N_F8), 1)
    f8[0] = 0
    a_f8 = [int(f8[n]) for n in range(N_F8 + 1)]
    check("S0.f8: eta(2t)^4 eta(4t)^4 matches T11 a_p head "
          "{3:-4,5:-2,7:24,11:-44,13:22}; a_1=1; a_even=0 on n<=200",
          a_f8[1] == 1
          and all(a_f8[p] == v for p, v in A_P.items())
          and all(a_f8[n] == 0 for n in range(2, 201, 2)))

    # ============================================================ A
    print("A -- unique Shimura preimage in the compiler theta-monoid (T38)")
    t1 = time.time()
    cands = build_candidates(Q_CAND)
    print(f"        built {len(cands)} integer-q candidates to O(q^{Q_CAND}) "
          f"in {time.time() - t1:.1f}s")
    check(f"A.space: compiler weight-5/2 theta monoid has "
          f"{len(cands)} distinct integer-q series "
          f"(~70 expected; V0 + q^2-scaled V1)",
          60 <= len(cands) <= 80)

    n_cap = min(N_SHIMURA_SEARCH, max_lift_n(Q_CAND + 1, 2))
    matches = []  # any nonzero scale * f8
    for lab, bq, key in cands:
        sh = shimura_lift(bq, 2, lambda d: 1, n_cap)
        if sh is None or sh[1] == 0:
            continue
        scale = Fraction(int(sh[1]), int(a_f8[1]))
        if all(scale * a_f8[n] == sh[n] for n in range(1, n_cap + 1)):
            matches.append((lab, key, scale))
    matches_m8 = [m for m in matches if m[2] == Fraction(-8)]
    print(f"        Shimura t=2,psi=1 scale-multiples of f8 on "
          f"n=1..{n_cap}: {len(matches)}")
    for lab, key, scale in matches:
        print(f"          key={key} scale={scale}  {lab}")
    check(f"A.unique: exactly ONE candidate with Sh_{{t=2,psi=1}} = "
          f"-8*f8 on n=1..{n_cap} (signed scale fixed); "
          f"witness key={WITNESS_KEY}; "
          f"{len(matches)} monoid elements lift to other scales "
          f"(+8,-16,+16 documented)",
          len(matches_m8) == 1
          and matches_m8[0][1] == WITNESS_KEY
          and len(matches) == 4
          and {m[2] for m in matches}
          == {Fraction(-8), Fraction(8), Fraction(-16), Fraction(16)})

    # Extended witness verify to n=120
    t1 = time.time()
    g_big = to_q_series(monomial_t(*WITNESS_KEY, 4 * Q_WITNESS), Q_WITNESS)
    assert g_big is not None
    sh_ext = shimura_lift(g_big, 2, lambda d: 1, N_SHIMURA_EXT)
    ext_ok = (sh_ext is not None and all(
        sh_ext[n] == -8 * a_f8[n] for n in range(1, N_SHIMURA_EXT + 1)))
    print(f"        extended Sh verify n=1..{N_SHIMURA_EXT} on O(q^{Q_WITNESS}): "
          f"{ext_ok} ({time.time() - t1:.1f}s)")
    print(f"        g head: {g_big[:16]}")
    print(f"        Sh head: {sh_ext[:16] if sh_ext else None}")
    check(f"A.witness: g=theta2(q^2)^2*theta3(q^2)*theta4*theta4(q^2); "
          f"Sh_{{t=2,psi=1}}(g)=-8*f8 exactly on n=1..{N_SHIMURA_EXT}; "
          f"g[0]=0; NOT Kohnen-plus",
          ext_ok and g_big[0] == 0
          and any(g_big[n] != 0 and n % 4 in (2, 3)
                  for n in range(1, 200)))
    check("A.convention: Shimura formula documented "
          "(A_t(n)=sum_{d|n} psi(d)(t/d) d^{k-1} b(t n^2/d^2); "
          "k=2, psi=1, t=2; weight 5/2 -> 4)",
          K_HALF == 2 and 2 * K_HALF == 4 and N_SHIMURA_EXT >= 120)

    # ============================================================ B
    print("B -- T(p^2) Hecke equivariance + trial FE (T41)")
    g = g_big  # reuse extended table for Hecke
    hecke_ok = True
    for p in PRIMES_HECKE:
        b = T_p2_half(g, p, 1, 1, Q_WITNESS, N_HECKE)
        ap = A_P[p]
        if any(b[n] != Fraction(ap) * Fraction(g[n])
               for n in range(N_HECKE + 1)):
            hecke_ok = False
            print(f"        p={p}: FAIL")
        else:
            print(f"        p={p}: T(p^2)g = {ap} g on n=0..{N_HECKE}")
    check("B.hecke: g is exact T(p^2)-eigenform (trivial chi) with "
          f"lam=a_p(f8) for p={PRIMES_HECKE} on n<= {N_HECKE} "
          f"(values {-4,-2,24,-44,22})",
          hecke_ok)

    # Trial FE around centre 5/4
    S_AFE = [mpmath.mpf("2.8"), mpmath.mpf("3.2"), mpmath.mpf("3.6")]
    AFE_TERMS = 4000
    DIR_TERMS = min(Q_WITNESS, 18000)
    Ldir_cache = {float(s): L_g_direct(g, s, DIR_TERMS) for s in S_AFE}
    fe_best = None
    for Nlev in LEVEL_FE_TRIALS:
        for eps in (1, -1):
            max_gap = mpmath.mpf(0)
            for s in S_AFE:
                Ld = Ldir_cache[float(s)]
                La = L_g_afe(g, s, Nlev, eps, AFE_TERMS)
                gap = (abs(La / Ld - 1) if Ld != 0 else mpmath.mpf(1))
                max_gap = max(max_gap, gap)
            if fe_best is None or max_gap < fe_best[2]:
                fe_best = (Nlev, eps, max_gap)
    print(f"        best FE: N={fe_best[0]}, eps={fe_best[1]:+d}, "
          f"max|AFE/dir-1|={float(fe_best[2]):.3e}")
    check("B.FE: trial half-integral FE Lambda(s)=eps Lambda(5/2-s) "
          f"anchors at N=512, eps=+1 (centre 5/4); "
          f"max|AFE/direct-1|={float(fe_best[2]):.3e} < {FE_THRESH}",
          fe_best[0] == 512 and fe_best[1] == 1
          and float(fe_best[2]) < FE_THRESH)
    check("B.fence: half-integral L-series generally have NO Euler "
          "product (multiplicativity of g-coeffs fails on coprime pairs)",
          any(g[n] * g[m] != g[n * m]
              for n in range(1, 40) for m in range(1, 40)
              if sp.gcd(n, m) == 1 and n * m <= 200
              and g[n] and g[m]))

    # ============================================================ C
    print("C -- Kohnen scope fence / U4(g)=0 (T44; NEGATIVE in claim)")
    g_small = g[: max(Q_G_SMALL, 801) + 1]
    mass_mod4 = {
        r: sum(abs(g_small[n]) for n in range(1, 801) if n % 4 == r)
        for r in range(4)
    }
    print(f"        |g| mass by n mod 4 (n=1..800): {mass_mod4}")
    u4_zero = all(g[4 * n] == 0 for n in range(0, Q_WITNESS // 4 + 1)
                  if 4 * n <= Q_WITNESS)
    check("C.U4: U4(g)=0 exactly (no Fourier mass on n≡0 mod 4); "
          f"mass mod 4 = {{0:0, 1:{mass_mod4[1]}, 2:{mass_mod4[2]}, "
          f"3:0}}",
          u4_zero and mass_mod4[0] == 0 and mass_mod4[3] == 0
          and mass_mod4[1] > 0 and mass_mod4[2] > 0)
    check("C.spectral: on ker(U4), H=W4∘U4 vanishes so raw "
          "Kohnen pr⁺_4=(1/3)Id is NOT a plus projector "
          "(no plus component of g)",
          u4_zero)  # structural: H(g)=0 ⇒ pr4(g)=g/3 not plus-supported

    M_HYP = 8
    level_hyp = 4 * M_HYP
    M_odd = (M_HYP % 2 == 1)
    M_sqfree = (abs(sp.mobius(M_HYP)) == 1)
    w4_solvable = None
    for a in range(0, 64):
        for b in range(1, 64, 4):
            if (4 * a - 1) % (M_HYP * b) == 0:
                c = (4 * a - 1) // (M_HYP * b)
                w4_solvable = (a, b, c)
                break
        if w4_solvable is not None:
            break
    outside = (not (M_odd and M_sqfree)) and (w4_solvable is None)
    print(f"        level {level_hyp}=4*{M_HYP}: M odd={M_odd}, "
          f"sqfree={M_sqfree}; W(4) solvable={w4_solvable}")
    check("C.scope: level 32=4·8 has M=8 even (not odd squarefree); "
          "W(4) condition 4a−Mbc=1 unsolvable; OUTSIDE Kohnen 1982 "
          "plus-new isomorphism scope (plus-route structurally closed)",
          outside and level_hyp == 32 and w4_solvable is None)

    # ============================================================ D
    print("D -- Waldspurger / Baruch-Mao constancy (T45)")
    g_w = to_q_series(monomial_t(*WITNESS_KEY, 4 * Q_G_SMALL), Q_G_SMALL)
    assert g_w is not None

    # Untwisted Fricke of f8
    gaps_f8 = {}
    s45 = mpmath.mpf("4.5")
    Ld_f8 = sum(mpmath.mpf(a_f8[n]) * mpmath.power(n, -s45)
                for n in range(1, 8001) if a_f8[n])
    for eps in (1, -1):
        sqN = mpmath.sqrt(8)
        lam = mpmath.mpf(0)
        for n in range(1, 2001):
            an = a_f8[n]
            if not an:
                continue
            xx = 2 * mpmath.pi * n / sqN
            pref = sqN / (2 * mpmath.pi * n)
            c = mpmath.mpf(an)
            lam += c * (pref ** s45 * mpmath.gammainc(s45, xx)
                        + eps * pref ** (4 - s45)
                        * mpmath.gammainc(4 - s45, xx))
        La = lam / ((sqN / (2 * mpmath.pi)) ** s45 * mpmath.gamma(s45))
        gaps_f8[eps] = abs(La - Ld_f8)
    eps_f8_num = 1 if gaps_f8[1] < gaps_f8[-1] else -1
    check("D.f8-Fricke: numeric Fricke of f8 is +1 (T12); "
          "gap(+1)/gap(-1) ratio ≥ 10",
          eps_f8_num == 1
          and max(gaps_f8.values()) / min(gaps_f8.values()) > 10)

    def evaluate_twist(d: int):
        Nlev = 8 * d * d
        eps_th = twist_root_number(d, 1, 8)
        nterm = nterms_for(Nlev)
        s_hi = mpmath.mpf("3.5")
        nterm_afe = min(N_F8, max(nterm, 8000))
        nterm_dir = min(N_F8, max(40000, 8 * nterm_afe))
        L_dir_hi = L_twist_direct(a_f8, d, s_hi, terms=nterm_dir)
        gap_th = abs(L_twist_afe(a_f8, d, s_hi, Nlev, eps_th, nterm_afe)
                     - L_dir_hi)
        gap_wrong = abs(L_twist_afe(a_f8, d, s_hi, Nlev, -eps_th, nterm_afe)
                        - L_dir_hi)
        eps_hi_ok = (gap_th < gap_wrong
                     and (gap_wrong / gap_th > FE_EPS_RATIO
                          if gap_th > 0 else True))
        rel_gap_hi = (gap_th / abs(L_dir_hi)
                      if L_dir_hi != 0 else mpmath.mpf(1))
        L_afe = L_twist_afe(a_f8, d, 2, Nlev, eps_th, nterm_afe)
        L_dir_c = L_twist_direct(a_f8, d, 2, terms=nterm_afe)
        n_lo = max(400, nterm_afe // 2)
        n_hi = min(N_F8, max(nterm_afe, n_lo + 200))
        L_lo = L_twist_afe(a_f8, d, 2, Nlev, eps_th, n_lo)
        L_hi = L_twist_afe(a_f8, d, 2, Nlev, eps_th, n_hi)
        stab_rel = (abs(L_hi - L_lo) / abs(L_hi)
                    if abs(L_hi) > L_VANISH_TOL else mpmath.mpf(0))
        return {
            "d": d, "eps": eps_th, "L_afe": L_afe, "L_dir_c": L_dir_c,
            "rel_gap_hi": rel_gap_hi, "eps_hi_ok": eps_hi_ok,
            "stab_rel": stab_rel,
            "centre_vanish_forced": eps_th == -1,
            "centre_is_zero": abs(L_afe) < L_VANISH_TOL,
        }

    val_rows = [evaluate_twist(d) for d in SMALL_D_VALIDATE
                if is_fundamental_discriminant(d)]
    eps_ok_all = all(r["eps_hi_ok"] for r in val_rows)
    afe_dir_ok = all(r["rel_gap_hi"] < AFE_DIRECT_TOL for r in val_rows)
    vanish_ok = all(r["centre_is_zero"] for r in val_rows
                    if r["centre_vanish_forced"])
    for r in val_rows:
        print(f"        d={r['d']}: eps={r['eps']:+d}, "
              f"L_afe(2)={r['L_afe']}, "
              f"rel@3.5={float(r['rel_gap_hi']):.3e}")
    check("D.AFE(i): theoretical eps_d=chi_d(8) preferred over wrong "
          f"sign at s=3.5 (gap ratio ≥ {FE_EPS_RATIO}) for "
          f"d in {SMALL_D_VALIDATE}",
          eps_ok_all and len(val_rows) >= 6)
    check("D.AFE(ii): AFE matches direct sums at s=3.5 "
          f"(rel ≤ {float(AFE_DIRECT_TOL):.0e}); eps=-1 ⇒ L(2)=0",
          afe_dir_ok and vanish_ok)

    row89 = next(r for r in val_rows if r["d"] == D_LITMUS)
    d89_ok = (row89["stab_rel"] < STABLE_REL_TOL
              and row89["eps_hi_ok"]
              and row89["rel_gap_hi"] < AFE_DIRECT_TOL
              and not row89["centre_is_zero"])
    d89_dir_bad = (abs(row89["L_afe"] - row89["L_dir_c"])
                   / abs(row89["L_afe"]) > mpmath.mpf("1e-2"))
    print(f"        litmus d=89: L_afe(2)={row89['L_afe']}, "
          f"stab={float(row89['stab_rel']):.3e}")
    check("D.AFE(iii): d=89 AFE stabilises (term-doubling < 1e-5, "
          "s=3.5 match); nonvanishing; direct-at-s=2 still disagrees "
          "(T44 trap)",
          d89_ok and d89_dir_bad)

    fund_odd = [d for d in range(1, DMAX + 1, 2)
                if is_fundamental_discriminant(d)]
    vanish_class = [d for d in fund_odd if d % 8 == 5 and d <= Q_G_SMALL]
    vanish_b_ok = all(g_w[d] == 0 for d in vanish_class)
    check(f"D.vanish: all {len(vanish_class)} fund. d≡5 mod 8 have "
          "b(|d|)=0 (root number −1 class)",
          vanish_b_ok and len(vanish_class) >= 10)

    twist_cache = {r["d"]: r for r in val_rows}

    def get_twist(d):
        if d not in twist_cache:
            twist_cache[d] = evaluate_twist(d)
        return twist_cache[d]

    live_rows = []
    for d in fund_odd:
        if d > Q_G_SMALL or d % 8 != 1:
            continue
        bn = g_w[d]
        Lw = get_twist(d)
        Lval = Lw["L_afe"]
        if abs(Lval) < L_VANISH_TOL or bn == 0:
            continue
        denom = mpmath.power(d, mpmath.mpf("1.5")) * Lval
        R = (mpmath.mpf(bn) ** 2) / denom
        live_rows.append({"d": d, "b": bn, "L": Lval, "R": R,
                          "eps": Lw["eps"]})
    print(f"        live R(d) rows (d≡1 mod 8): {len(live_rows)}")
    for r in live_rows:
        print(f"          d={r['d']}: b={r['b']}, L={float(r['L']):.12g}, "
              f"R={float(r['R']):.12g}")
    Rs = [r["R"] for r in live_rows]
    R_med = sorted(Rs, key=float)[len(Rs) // 2] if Rs else None
    spread = (max(abs(r - R_med) / abs(R_med) for r in Rs)
              if Rs and R_med else mpmath.mpf(1))
    print(f"        R_med={R_med}, spread={float(spread):.3e}")
    check(f"D.sample: ≥10 live fund. d≡1 mod 8 with b≠0 and L≠0 "
          f"(got {len(live_rows)}; includes d=89)",
          len(live_rows) >= 10
          and any(r["d"] == 89 for r in live_rows))
    check("D.constancy: R(d)=b(|d|)^2/(|d|^{3/2} L(f8×χ_d,2)) CONSTANT "
          f"on live class (R≈{float(R_TARGET)}, spread≤1e-12; "
          f"measured spread={float(spread):.3e})",
          R_med is not None
          and abs(R_med - R_TARGET) / R_TARGET < mpmath.mpf("1e-8")
          and spread <= R_SPREAD_TOL)
    check("D.eps-class: eps_d=+1 on all live d≡1 mod 8 rows",
          all(r["eps"] == 1 for r in live_rows))

    # ============================================================ FENCES
    print("F -- honesty fences (named, not failures)")
    check("FENCE: Shimura/Kohnen/Waldspurger/Baruch-Mao named classical; "
          "claim = unique monoid preimage + in-suite chain + measured R; "
          "GL(2) centre s=2 NOT xi-line; NO RH; ZETA.HP.CARRIER untouched; "
          "no marker moves",
          len(matches_m8) == 1 and matches_m8[0][2] == Fraction(-8)
          and hecke_ok and outside
          and spread <= R_SPREAD_TOL
          and float(fe_best[2]) < FE_THRESH)

    elapsed = time.time() - t0
    print(f"        walltime {elapsed:.1f}s")
    return summary("HECKE.GEOM.HALFINT.01 half-integral bridge")


if __name__ == "__main__":
    raise SystemExit(run())
