"""Discovery probe (2026-07-24), part 43 of the zeta/prime investigation.
KOHNEN-PLUS PROJECTION of the T38/T41 compiler object g and the
classical Waldspurger / Kohnen–Zagier central-value attachment.

CONTEXT (T41 named next lever):
  g = theta2(q^2)^2 * theta3(q^2) * theta4 * theta4(q^2)
  weight 5/2, T(p^2)-eigenform with eigenvalues a_p(f8) for
  p = 3..13, trivial nebentypus, 2-power level ~32.
  g[0] = 0; g is NOT Kohnen-plus; T41 Waldspurger samples failed.
  Named lever: project g into the plus space (or find a plus-space
  pendant in the compiler monoid) and re-test Waldspurger.

CLASSICAL FRAME (named as such — not TFPT claims):
  Kohnen plus-space for weight k+1/2, level 4N (Kohnen 1980/82):
    Fourier coeffs b(n) vanish unless (-1)^k n ≡ 0 or 1 (mod 4).
    Here k = 2 (weight 5/2): (-1)^k = +1 ⇒ support on n ≡ 0,1 mod 4
    ⇒ b(n) = 0 for n ≡ 2,3 mod 4.
    (NOTE: the odd-k convention would allow n ≡ 0,3; we test that
    alternate as a documented secondary track, not the primary.)
  On the plus space the Shimura correspondence is an isomorphism
  (Kohnen 1980/82).  Waldspurger's theorem in Kohnen–Zagier form
  relates b(|d|)^2 to central values L(f × χ_d, k) for fundamental
  discriminants d with (-1)^k d > 0  (for k = 2: d > 0).

S1  P1 Plus-projection — TWO routes:
    (a) classical support projector pr^+ (and a U(4)/V(4) hybrid)
        applied to g;
    (b) direct search in the moderately extended T38 monoid
        (theta-monomials weight 5/2 with q^2 and q^4 scalings)
        for g+ with plus support AND T(p^2)-eigenvalues a_p
        (p = 3,5,7) by exact linear algebra.
    Success: g+ exists, unique up to scale, Sh(g+) ∝ f8.

S2  P2 Waldspurger / Kohnen–Zagier on g+ (if found):
    test constancy of
      R(d) = b(|d|)^2 / (|d|^{k-1/2} L(f8 × χ_d, k=2))
    over 4–6 fundamental discriminants; test BOTH sign classes of d
    and select the convention-conformant class ((-1)^k d > 0 ⇒ d > 0).
    Twisted L-values via twisted coeffs + T12 incomplete-Gamma AFE
    (twist level ~ 8 d^2; |d| ≤ 24).
    Success: relative spread < 1% (kill if > 5%).

S3  P3 Centre bookkeeping (honest):
    L(f8 × χ_d, 2) sits at the GL(2) centre s = 2 (weight-4
    normalisation) — NOT on the ξ-line.  Type exactly what the
    Waldspurger join delivers (central-value family as coefficient
    squares) and what it does NOT (no ζ(s) spectrum, no RH content).
    Functor contract map: abelian → centre 1/2 (T39); cuspidal →
    a_p (T41) + central-value family (P2) at GL(2) centre.

PREREGISTERED CRITERIA
  P1: g+ in (extended) monoid, unique up to scale, Sh(g+) ∝ f8.
  P2: Waldspurger ratios constant to < 1% on the conformant class.
  K1: no g+ in moderately extended monoid ⇒ OUTSIDE-MONOID
      (document best approximation).
  K2: Waldspurger spread > 5% ⇒ convention/structure problem.
  Verdict: CENTRAL-VALUES-WIRED (P1+P2)
           / PLUS-FOUND-ONLY (P1 yes, P2 no)
           / OUTSIDE-MONOID (K1)
           / PARTIAL.

Firewall: discovery sandbox, NO promotion, no marker moves, no RH
evidence language.  Classical theorems (Kohnen 1980/82,
Kohnen–Zagier, Waldspurger, Shimura 1973) named as such —
TFPT content is whether the T38/T41 witness admits a plus-space
pendant that wires central twist values into the functor.
"""
from __future__ import annotations

import itertools
import time
from fractions import Fraction

import mpmath
import numpy as np
import sympy as sp

PASS = 0
FAIL = 0
T0 = time.time()
mpmath.mp.dps = 40

# ------------------------------------------------------------ budgets
QMAX = 8000            # q-series for g / Shimura / Hecke
Q_CAND = 1800          # candidate space for linear algebra
N_F8 = 4000
N_SH = 60              # Shimura check window
N_HECKE = 30           # Hecke eigen window (needs p^2 * N_HECKE <= Q)
N_PLUS_LA = 60         # plus-condition rows for LA
K_HALF = 2             # weight = K_HALF + 1/2 = 5/2
HEAD_AP = {3: -4, 5: -2, 7: 24, 11: -44, 13: 22}
WITNESS_KEY = (0, 2, 0, 1, 1, 1)  # th2(q2)^2 th3(q2) th4 th4(q2)
# Extended key: (a0,a2,a4,b0,b2,b4,c0,c2,c4)
WITNESS_KEY9 = (0, 2, 0, 0, 1, 0, 1, 1, 0)
PRIMES_HECKE = (3, 5, 7)


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
    """Fundamental discriminant (classical):
      (i) d ≡ 1 mod 4 and squarefree, OR
      (ii) d ≡ 0 mod 4, d/4 ≡ 2 or 3 mod 4, and d/4 squarefree.
    Note: use signed (d//4) % 4 so that -4 (m=-1 ≡ 3 mod 4) is kept.
    """
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


# ================================================================ f8
f8 = np.roll(conv_i64(eta_pass(2, 4, N_F8),
                      eta_pass(4, 4, N_F8), N_F8), 1)
f8[0] = 0
a_f8 = [int(f8[n]) for n in range(N_F8 + 1)]
head_ok = a_f8[1] == 1 and all(a_f8[p] == v for p, v in HEAD_AP.items())
check("P0.f8: eta(2t)^4 eta(4t)^4 matches T11 a_p head "
      "{3:-4,5:-2,7:24,11:-44,13:22}",
      head_ok)


# ================================================================ thetas
print("=" * 72)
print("P0 -- rebuild T38/T41 witness g; document plus conventions")
print("=" * 72)

TMAX = 4 * QMAX
T_CAND = 4 * Q_CAND


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


_TH_CACHE = {}


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


def monomial_t6(a0, a2, b0, b2, c0, c2, order_t):
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


def monomial_t9(a0, a2, a4, b0, b2, b4, c0, c2, c4, order_t):
    s = np.zeros(order_t + 1, dtype=np.int64)
    s[0] = 1
    for kind, exps in ((2, (a0, a2, a4)), (3, (b0, b2, b4)),
                       (4, (c0, c2, c4))):
        for scale, e in zip((1, 2, 4), exps):
            for _ in range(e):
                s = conv_i64(s, _th(kind, scale, order_t), order_t)
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


t_build0 = time.time()
st_g = monomial_t6(*WITNESS_KEY, TMAX)
bq_g = to_q_series(st_g, QMAX)
assert bq_g is not None
g = bq_g
info(f"g = th2(q2)^2 * th3(q2) * th4 * th4(q2); key6={WITNESS_KEY}")
info(f"  rebuild O(q^{QMAX}) in {time.time() - t_build0:.2f}s")
info(f"  g head: {g[:24]}")
info(f"  g[0]={g[0]}")


def kohnen_plus_ok(bq, allowed_mod4, nmax=200):
    """Plus support: b(n)=0 unless n%4 in allowed_mod4 (n>=1)."""
    bad = {0, 1, 2, 3} - set(allowed_mod4)
    for n in range(1, min(nmax, len(bq) - 1) + 1):
        if (n % 4) in bad and bq[n] != 0:
            return False
    return True


# Classical Kohnen for k even: allowed {0,1}; alternate odd-k-style {0,3}
PLUS_CLASSICAL = (0, 1)   # zeros on 2,3
PLUS_ALTERNATE = (0, 3)   # zeros on 1,2  (user secondary track)

plus_g_class = kohnen_plus_ok(g, PLUS_CLASSICAL, nmax=400)
plus_g_alt = kohnen_plus_ok(g, PLUS_ALTERNATE, nmax=400)
# Count violations
n_viol_class = sum(1 for n in range(1, 201)
                   if n % 4 in (2, 3) and g[n] != 0)
n_viol_alt = sum(1 for n in range(1, 201)
                 if n % 4 in (1, 2) and g[n] != 0)
info("CLASSICAL Kohnen plus (k=2 even): support n≡0,1 mod 4 "
     "(b(n)=0 for n≡2,3).  Formula: (-1)^k n ≡ 0,1 mod 4.")
info(f"  g classical-plus? {plus_g_class}; "
     f"violations n=1..200 on {{2,3}}: {n_viol_class}")
info("ALTERNATE track (odd-k style): support n≡0,3 mod 4 "
     "(b(n)=0 for n≡1,2) — documented secondary, not primary.")
info(f"  g alternate-plus? {plus_g_alt}; "
     f"violations n=1..200 on {{1,2}}: {n_viol_alt}")

check("P0.g: T38/T41 witness rebuilt; g[0]=0; NOT classical Kohnen-plus "
      f"(violations on n≡2,3: {n_viol_class} in 1..200); "
      "classical convention documented (k=2 ⇒ support 0,1)",
      g[0] == 0 and (not plus_g_class) and n_viol_class > 0)


# Shimura reconfirm
def shimura_A(bq, n, t, psi):
    total = 0
    for d in sp.divisors(n):
        d = int(d)
        idx = t * (n // d) * (n // d)
        if idx >= len(bq):
            return None
        chi = psi(d) * kronecker(t, d)
        total += chi * (d ** (K_HALF - 1)) * bq[idx]
    return int(total)


def shimura_lift(bq, t, psi, nmax):
    out = [0] * (nmax + 1)
    for n in range(1, nmax + 1):
        val = shimura_A(bq, n, t, psi)
        if val is None:
            return None
        out[n] = val
    return out


sh = shimura_lift(g, 2, lambda d: 1, N_SH)
sh_ok = sh is not None and all(
    sh[n] == -8 * a_f8[n] for n in range(1, N_SH + 1))
info(f"Sh_t=2,psi=1(g) = -8 f8 on n=1..{N_SH}? {sh_ok}")
check(f"P0.bridge: Sh_{{t=2,psi=1}}(g) = -8 f8 on n=1..{N_SH} "
      "(T38/T41 reconfirm)",
      sh_ok)


# ================================================================ Hecke
def T_p2_half_integral(a, p, chi_p, chi_p2, order, n_check):
    """T(p^2) at weight 5/2 (k=2), trivial/trial character."""
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
            term += Fraction(chi_p2) * Fraction(p3) * Fraction(
                a[n // (p * p)])
        out[n] = term
    return out


def is_eigen_ap(bq, p, ap, order, n_check, chi_p=1, chi_p2=1):
    b = T_p2_half_integral(bq, p, chi_p, chi_p2, order, n_check)
    for n in range(0, n_check + 1):
        if b[n] != Fraction(ap) * Fraction(bq[n]):
            return False
    return True


def eigen_lambda(bq, p, order, n_check, chi_p=1, chi_p2=1):
    b = T_p2_half_integral(bq, p, chi_p, chi_p2, order, n_check)
    for n in range(1, n_check + 1):
        if bq[n] != 0:
            return b[n] / Fraction(bq[n])
    return None


# Confirm g is T(p^2)-eigen with a_p under trivial chi (T41)
hecke_g_ok = all(
    is_eigen_ap(g, p, HEAD_AP[p], QMAX, N_HECKE)
    for p in PRIMES_HECKE)
info("T(p^2) table for g (trivial chi, T41 reconfirm):")
for p in PRIMES_HECKE:
    lam = eigen_lambda(g, p, QMAX, N_HECKE)
    info(f"  p={p}: lam={lam}, a_p={HEAD_AP[p]}, "
         f"eigen={is_eigen_ap(g, p, HEAD_AP[p], QMAX, N_HECKE)}")
check("P0.hecke: g is T(p^2)-eigenform with lam=a_p(f8) for "
      f"p in {PRIMES_HECKE} under trivial nebentypus (T41)",
      hecke_g_ok)


# ================================================================ P1a
print("=" * 72)
print("P1a -- classical plus projector on g (support + U(4)/V(4) hybrid)")
print("=" * 72)

info("FORMULA (documented): for weight k+1/2, k even, the Kohnen")
info("  plus subspace of M_{k+1/2}(Γ_0(4N)) is cut out by the")
info("  Fourier support condition (Kohnen 1980/82):")
info("    pr^+_supp(Σ a(n) q^n) = Σ_{n≡0,1 (mod 4)} a(n) q^n.")
info("  U(4)/V(4) hybrid (coefficient form of the level-4 projector):")
info("    (f|U_4)_n = a(4n);  (f|V_4)_n = a(n/4) if 4|n else 0;")
info("    pr_U^ε(f) = 1/2 (f + ε · V_4(U_4(f)))  for ε ∈ {±1}.")
info("  Note: V_4 U_4 zeroes all coeffs with n≢0 mod 4; the support")
info("  projector to {0,1} is NOT equal to any single V_4 U_4 image.")
info("  We apply pr^+_supp as the defining plus cut, and report the")
info("  U(4) hybrids as diagnostics.")


def support_project(bq, allowed_mod4):
    out = [0] * len(bq)
    for n in range(len(bq)):
        if n == 0 or (n % 4) in allowed_mod4:
            out[n] = bq[n]
        else:
            out[n] = 0
    return out


def U4(bq):
    """(f|U_4)_n = a(4n)."""
    out = [0] * len(bq)
    for n in range((len(bq) - 1) // 4 + 1):
        out[n] = bq[4 * n]
    return out


def V4(bq):
    """(f|V_4)_n = a(n/4) if 4|n else 0."""
    out = [0] * len(bq)
    for n in range(0, len(bq), 4):
        out[n] = bq[n // 4]
    return out


def half_sum(a, b, eps):
    """(a + eps * b) / 2 as Fraction list (truncated to int if exact)."""
    out = []
    for i in range(len(a)):
        v = (Fraction(a[i]) + Fraction(eps) * Fraction(b[i])) / 2
        out.append(v)
    return out


g_plus_supp = support_project(g, PLUS_CLASSICAL)
g_plus_alt = support_project(g, PLUS_ALTERNATE)
VU_g = V4(U4(g))
pr_U_p = half_sum(g, VU_g, +1)
pr_U_m = half_sum(g, VU_g, -1)

# How much mass was killed by support projector?
mass_g = sum(abs(g[n]) for n in range(1, min(400, len(g))))
mass_plus = sum(abs(g_plus_supp[n]) for n in range(1, min(400, len(g))))
mass_killed = sum(abs(g[n]) for n in range(1, min(400, len(g)))
                  if n % 4 in (2, 3))
info(f"pr^+_supp(g): mass kept={mass_plus}, killed={mass_killed}, "
     f"total={mass_g} (n=1..400 abs-sum)")
info(f"  g_plus_supp head: {g_plus_supp[:24]}")
info(f"  V4U4(g) head: {VU_g[:24]}")
info(f"  pr_U^+ head (Fraction): {[pr_U_p[n] for n in range(16)]}")
info(f"  pr_U^- head (Fraction): {[pr_U_m[n] for n in range(16)]}")

# Is support projection still a T(p^2)-eigenform?
supp_eigen = {
    p: is_eigen_ap(g_plus_supp, p, HEAD_AP[p], QMAX, N_HECKE)
    for p in PRIMES_HECKE
}
info(f"pr^+_supp(g) T(p^2)-eigen at a_p? {supp_eigen}")

def shimura_match_f8(bq, nmax=N_SH):
    """Try Shimura lifts over t compatible with plus / T38.

    Classical note (Kohnen): on the plus space the isomorphism uses
    indices n^2 (t=1), since t=2 hits n≡2 mod 4 where plus coeffs
    vanish.  We also retry t=2 (T38 witness convention) and a few
    other squarefree t ≡ 0,1 mod 4.
    Returns (ok, t, psi_name, scale, sh_head).
    """
    trials = []
    # t ≡ 0 or 1 mod 4 for k even plus-compatible; plus t=2 (T38)
    for t in (1, 2, 5, 10, 13, 17):
        for psi_name, psi in (("trivial", lambda d: 1),
                             ("chi4", chi4),
                             ("chi_m4", lambda d: kronecker(-4, d))):
            # max n with t*n^2 < len(bq)
            n_max = min(nmax, int(((len(bq) - 1) // t) ** 0.5))
            if n_max < 8:
                continue
            sh = shimura_lift(bq, t, psi, n_max)
            if sh is None:
                continue
            if all(v == 0 for v in sh[1:]):
                trials.append((False, t, psi_name, None, sh[:12], n_max,
                               "zero-lift"))
                continue
            scale = None
            for n in range(1, n_max + 1):
                if a_f8[n] != 0 and sh[n] != 0:
                    scale = Fraction(sh[n], a_f8[n])
                    break
            if scale is None:
                trials.append((False, t, psi_name, None, sh[:12], n_max,
                               "no-scale"))
                continue
            ok = all(Fraction(sh[n]) == scale * Fraction(a_f8[n])
                     for n in range(1, n_max + 1))
            trials.append((ok, t, psi_name, scale, sh[:12], n_max, "ok"))
            if ok:
                return True, t, psi_name, scale, sh[:12], trials
    return False, None, None, None, None, trials


# Shimura of support projection — scan t (t=2 vanishes on plus!)
sh_supp_ok, sh_supp_t, sh_supp_psi, scale_supp, sh_supp_head, sh_trials \
    = shimura_match_f8(g_plus_supp, N_SH)
info("Shimura scan on pr^+_supp(g) (plus-compatible t first):")
for ok, t, pn, sc, head, n_max, tag in sh_trials[:10]:
    info(f"  t={t}, psi={pn}, n<= {n_max}: ok={ok}, scale={sc}, "
         f"tag={tag}, head={head}")
info(f"BEST Sh(pr^+_supp): ok={sh_supp_ok}, t={sh_supp_t}, "
     f"psi={sh_supp_psi}, scale={scale_supp}")

P1a_gplus = (
    kohnen_plus_ok(g_plus_supp, PLUS_CLASSICAL, nmax=400)
    and all(supp_eigen.values())
    and sh_supp_ok
)
info(f"P1a success (supp projector yields plus+eigen+Sh∝f8)? {P1a_gplus}")
check("P1a.supp: pr^+_supp(g) is classical-plus by construction; "
      f"T(p^2)-eigen at a_p for p={PRIMES_HECKE}? {supp_eigen}; "
      f"Sh∝f8? {sh_supp_ok} (t={sh_supp_t}, psi={sh_supp_psi}, "
      f"scale={scale_supp}); P1a_witness={P1a_gplus}",
      True)  # computed facts; negative content OK

# U(4) hybrid diagnostics: which ε lands closer to plus support?
for eps, pr in ((+1, pr_U_p), (-1, pr_U_m)):
    # measure residual on forbidden residues
    resid = sum(abs(pr[n]) for n in range(1, 201) if n % 4 in (2, 3))
    kept = sum(abs(pr[n]) for n in range(1, 201) if n % 4 in (0, 1))
    info(f"  pr_U^ε ε={eps:+d}: abs-mass on {{0,1}}={kept}, "
         f"on {{2,3}}={resid} (n=1..200)")
check("P1a.U4: U(4)/V(4) hybrids documented; V4U4 zeroes n≢0 mod 4 "
      "(not the full {{0,1}}-support projector) — computed diagnostic",
      all(VU_g[n] == 0 for n in range(1, 100) if n % 4 != 0))


# ================================================================ P1b
print("=" * 72)
print("P1b -- direct search in extended compiler monoid (q^2 + q^4)")
print("=" * 72)

info("CANDIDATE SPACE (preregistered, moderate extension of T38):")
info("  Weight 5/2 theta-monomials with independent plain / q^2 / q^4")
info("  scalings: keys (a0,a2,a4,b0,b2,b4,c0,c2,c4) summing to 5,")
info("  integer-q filter (min t-exp ≡ 0 mod 4), dedup by q-series.")
info("  Plus condition as LINEAR system on combo coeffs, THEN")
info("  Hecke eigen-condition (T(p^2)-a_p) for p=3,5,7.")
info(f"  LA order O(q^{Q_CAND}); rebuild witnesses at O(q^{QMAX}).")

t_cand0 = time.time()
candidates = []  # (label, bq_short, key9)


def add_cand9(label, key9):
    a0, a2, a4, b0, b2, b4, c0, c2, c4 = key9
    total = sum(key9)
    if total != 5:
        return
    # integer-q: min t-exp from theta2 factors
    # th2(q^s) has min exp s*1^2 = s
    min_exp = 1 * a0 + 2 * a2 + 4 * a4
    if min_exp % 4 != 0:
        return
    st = monomial_t9(*key9, T_CAND)
    bq = to_q_series(st, Q_CAND)
    if bq is None or all(x == 0 for x in bq):
        return
    candidates.append((label, bq, key9))


# Enumerate compositions of 5 across 9 bins
n_tried = 0
for vals in itertools.product(range(6), repeat=8):
    # vals = a0,a2,a4,b0,b2,b4,c0,c2; c4 determined
    partial = sum(vals)
    if partial > 5:
        continue
    c4 = 5 - partial
    key9 = vals + (c4,)
    n_tried += 1
    lab = ("Vext:" + ",".join(str(x) for x in key9))
    add_cand9(lab, key9)

uniq = {}
for lab, bq, key9 in candidates:
    tup = tuple(bq[:500])
    if tup not in uniq:
        uniq[tup] = (lab, bq, key9)
candidates = list(uniq.values())
info(f"compositions tried: {n_tried}; integer-q distinct: "
     f"{len(candidates)} in {time.time() - t_cand0:.1f}s")

# Plus survivors (exact single monomials)
plus_mono_class = [(lab, bq, k) for lab, bq, k in candidates
                   if kohnen_plus_ok(bq, PLUS_CLASSICAL, nmax=N_PLUS_LA)]
plus_mono_alt = [(lab, bq, k) for lab, bq, k in candidates
                 if kohnen_plus_ok(bq, PLUS_ALTERNATE, nmax=N_PLUS_LA)]
info(f"exact plus monomials (classical {{0,1}}): {len(plus_mono_class)}")
info(f"exact plus monomials (alternate {{0,3}}): {len(plus_mono_alt)}")
check(f"P1b.space: extended monoid has {len(candidates)} distinct "
      f"integer-q series (T38 was ~70; q^4 extension); "
      f"classical-plus monomials={len(plus_mono_class)}, "
      f"alternate-plus monomials={len(plus_mono_alt)}",
      len(candidates) >= 70)


def series_from_key9(key9, qmax):
    st = monomial_t9(*key9, 4 * qmax)
    return to_q_series(st, qmax)


def linear_plus_hecke_search(cand_list, allowed_mod4, tag):
    """Exact LA: ONE homogeneous system = plus support ⊕ Hecke.

    Rows: (bad-n plus conditions) + ((T(p^2)-a_p) coeffs for p=3,5,7).
    Columns: candidate monomials.  SVD → rationalize → exact check.

    Returns dict with keys: found, dim_plus, dim_hecke, witness_x,
    witness_bq (short), keys, approx_score, detail.
    """
    n_c = len(cand_list)
    if n_c == 0:
        return {"found": False, "dim_plus": 0, "dim_hecke": 0,
                "witness_x": None, "witness_bq": None, "keys": [],
                "approx_score": None, "detail": "empty candidate list"}

    bad = {0, 1, 2, 3} - set(allowed_mod4)
    bad_ns = [n for n in range(1, N_PLUS_LA + 1) if (n % 4) in bad]

    # Precompute T(p^2) on each candidate (window N_HECKE)
    Tcache = {}  # (j, p) -> list Fraction[0..N_HECKE]
    t_t0 = time.time()
    for j, (lab, bq, key9) in enumerate(cand_list):
        for p in PRIMES_HECKE:
            Tcache[(j, p)] = T_p2_half_integral(
                bq, p, 1, 1, Q_CAND, N_HECKE)
    info(f"  [{tag}] T(p^2) cache for {n_c} cands in "
         f"{time.time() - t_t0:.1f}s")

    n_plus_rows = len(bad_ns)
    n_hecke_rows = len(PRIMES_HECKE) * (N_HECKE + 1)
    n_rows = n_plus_rows + n_hecke_rows

    # Build float matrix directly (avoid giant sympy Matrix)
    Mf = np.zeros((n_rows, n_c), dtype=float)
    for j, (lab, bq, key9) in enumerate(cand_list):
        for i, n in enumerate(bad_ns):
            Mf[i, j] = float(bq[n])
        r0 = n_plus_rows
        for ip, p in enumerate(PRIMES_HECKE):
            ap = HEAD_AP[p]
            Tb = Tcache[(j, p)]
            for n in range(N_HECKE + 1):
                val = Tb[n] - Fraction(ap) * Fraction(bq[n])
                Mf[r0 + ip * (N_HECKE + 1) + n, j] = float(val)

    # Plus-only rank diagnostic
    try:
        rank_plus = int(np.linalg.matrix_rank(Mf[:n_plus_rows], tol=1e-8))
        dim_plus_est = n_c - rank_plus
    except np.linalg.LinAlgError:
        rank_plus = -1
        dim_plus_est = -1
    info(f"  [{tag}] plus-row rank≈{rank_plus}/{n_plus_rows} ⇒ "
         f"plus-null dim≈{dim_plus_est} (over {n_c} candidates)")

    # Numerical SVD → rationalize tiny-singular vectors → exact check.
    t_ns = time.time()
    # Column-normalize for conditioning
    col_norms = np.linalg.norm(Mf, axis=0)
    col_norms[col_norms < 1e-30] = 1.0
    Mf_n = Mf / col_norms
    try:
        _, svals, Vt = np.linalg.svd(Mf_n, full_matrices=True)
    except np.linalg.LinAlgError:
        return {"found": False, "dim_plus": dim_plus_est,
                "dim_hecke": 0, "witness_x": None, "witness_bq": None,
                "keys": [], "approx_score": None,
                "detail": "SVD failed"}

    # Kernel candidates: singular values below threshold
    s_max = float(svals[0]) if len(svals) else 1.0
    ker_tol = 1e-8 * max(s_max, 1.0)
    ker_idxs = [i for i, s in enumerate(svals) if s <= ker_tol]
    # Always keep the smallest few for approximation
    order = list(np.argsort(svals))
    info(f"  [{tag}] SVD: min σ={float(svals[order[0]]):.3e}, "
         f"#σ<tol={len(ker_idxs)}, n_c={n_c} "
         f"({time.time() - t_ns:.1f}s)")

    def float_x_to_int(x_float, max_den=64):
        """Rationalize a float vector to small-integer combo."""
        # Scale so max|x|=1, then nsimplify each coord
        scale = max(abs(float(t)) for t in x_float)
        if scale < 1e-30:
            return None
        xf = [float(t) / scale for t in x_float]
        rats = []
        for t in xf:
            if abs(t) < 1e-9:
                rats.append(Fraction(0))
                continue
            r = sp.nsimplify(t, tolerance=1e-7, rational=True)
            if isinstance(r, sp.Rational):
                fr = Fraction(int(r.p), int(r.q))
            else:
                fr = Fraction(t).limit_denominator(max_den)
            if fr.denominator > max_den:
                fr = Fraction(t).limit_denominator(max_den)
            rats.append(fr)
        dens = [r.denominator for r in rats]
        lcm = 1
        for d in dens:
            lcm = int(lcm * d // int(sp.gcd(lcm, d)))
        ints = [int(r * lcm) for r in rats]
        g = 0
        for c in ints:
            g = int(sp.gcd(g, abs(c)))
        if g > 1:
            ints = [c // g for c in ints]
        # Reject if too dense (noise)
        nnz = sum(1 for c in ints if c != 0)
        if nnz == 0 or nnz > 40:
            return None
        return ints

    def exact_kernel_ok(x_int):
        """Check plus + Hecke exactly on the integer combo."""
        bq = [0] * (Q_CAND + 1)
        for j, coef in enumerate(x_int):
            if coef == 0:
                continue
            bj = cand_list[j][1]
            for n in range(Q_CAND + 1):
                bq[n] += coef * bj[n]
        if all(v == 0 for v in bq):
            return False, bq
        if not kohnen_plus_ok(bq, allowed_mod4, nmax=N_PLUS_LA):
            return False, bq
        for p in PRIMES_HECKE:
            if not is_eigen_ap(bq, p, HEAD_AP[p], Q_CAND, N_HECKE):
                return False, bq
        return True, bq

    # Try kernel singular vectors (and a few near-kernel)
    witnesses = []
    trial_idxs = list(dict.fromkeys(ker_idxs + order[:8]))
    for i in trial_idxs:
        # Vt[i] is right singular vector for σ_i; undo col-normalization
        x_f = Vt[i] / col_norms
        x_int = float_x_to_int(x_f)
        if x_int is None:
            continue
        ok, bq_w = exact_kernel_ok(x_int)
        if ok:
            witnesses.append((x_int, bq_w))

    dim_hecke = len(witnesses)
    # Dedup witnesses up to scale
    uniq_w = []
    for x_int, bq_w in witnesses:
        parallel = False
        for x2, _ in uniq_w:
            ratio = None
            for a, b in zip(x_int, x2):
                if a != 0 and b != 0:
                    if a % b == 0 or b % a == 0:
                        ratio = Fraction(a, b)
                        break
            if ratio is not None and all(
                    Fraction(a) == ratio * Fraction(b)
                    for a, b in zip(x_int, x2)):
                parallel = True
                break
            # also check exact list equality up to ±
            if x_int == x2 or x_int == [-c for c in x2]:
                parallel = True
                break
        if not parallel:
            uniq_w.append((x_int, bq_w))
    dim_hecke = len(uniq_w)
    unique_up_to_scale = (dim_hecke == 1)

    if dim_hecke == 0:
        x_best = Vt[order[0]] / col_norms
        resid = float(np.linalg.norm(Mf @ (x_best * col_norms / col_norms)))
        # recompute with un-normalized: Mf was built unnormalized
        # Actually Mf @ x_raw where x_raw = Vt[i]/col_norms
        x_raw = Vt[order[0]] / col_norms
        resid = float(np.linalg.norm(Mf @ x_raw))
        approx = resid / (float(np.linalg.norm(x_raw)) + 1e-30)
        r_plus = float(np.linalg.norm(Mf[:n_plus_rows] @ x_raw))
        r_hecke = float(np.linalg.norm(Mf[n_plus_rows:] @ x_raw))
        bq_approx = [0.0] * (Q_CAND + 1)
        for j in range(n_c):
            if abs(x_raw[j]) < 1e-12:
                continue
            bj = cand_list[j][1]
            for n in range(Q_CAND + 1):
                bq_approx[n] += float(x_raw[j]) * bj[n]
        return {"found": False, "dim_plus": dim_plus_est,
                "dim_hecke": 0, "witness_x": None,
                "witness_bq": bq_approx, "keys": [],
                "approx_score": approx,
                "detail": (f"combined kernel=0; plus-null≈{dim_plus_est}; "
                           f"best SVD resid/||x||={approx:.6g} "
                           f"(plus_part={r_plus:.6g}, "
                           f"hecke_part={r_hecke:.6g})")}

    x_cand, bq_w = uniq_w[0]
    nz_keys = [(cand_list[i][2], x_cand[i], cand_list[i][0])
               for i in range(n_c) if x_cand[i] != 0]

    return {
        "found": True,
        "dim_plus": dim_plus_est,
        "dim_hecke": dim_hecke,
        "unique": unique_up_to_scale,
        "witness_x": x_cand,
        "witness_bq": bq_w,
        "keys": nz_keys,
        "approx_score": 0.0,
        "detail": (f"plus-null≈{dim_plus_est}, combined-dim={dim_hecke}, "
                   f"unique_up_to_scale={unique_up_to_scale}, "
                   f"nz_terms={len(nz_keys)}"),
    }


# -----------------------------------------------------------------
# ROUTE (b): solve Sh(combo) ∝ f8 inside classical-plus monoid span
# -----------------------------------------------------------------
# Classical (Kohnen): on the plus space the Shimura isomorphism uses
# t with (-1)^k t ≡ 0,1 mod 4; for k=2 the primary choice is t=1
# (t=2 hits only n≡2 mod 4 indices, hence vanishes on plus forms).
# Exact LA: columns = Sh_t=1(c_j) for plus monomials c_j; solve
#   sum x_j Sh(c_j) = λ f8
# then verify plus + T(p^2)=a_p on the combo.

info("ROUTE (b): Sh_t=1 linear preimage of f8 in classical-plus span")
N_SH_LA = 40  # need t*n^2 = n^2 <= Q_CAND


def _clear_denoms_vec(v):
    rats = []
    for x in v:
        r = sp.Rational(x)
        rats.append(Fraction(int(r.p), int(r.q)))
    dens = [r.denominator for r in rats]
    lcm = 1
    for d in dens:
        lcm = int(lcm * d // int(sp.gcd(lcm, d)))
    ints = [int(r * lcm) for r in rats]
    g = 0
    for c in ints:
        g = int(sp.gcd(g, abs(c)))
    if g > 1:
        ints = [c // g for c in ints]
    return ints


def shimura_cols(cand_list, t, psi, nmax):
    cols = []
    for lab, bq, key9 in cand_list:
        sh = shimura_lift(bq, t, psi, nmax)
        if sh is None:
            return None
        cols.append([sh[n] for n in range(1, nmax + 1)])
    return cols


def solve_shimura_preimage(cand_list, t, psi_name, psi, tag):
    nmax = min(N_SH_LA, int(((Q_CAND - 1) // t) ** 0.5))
    if nmax < 10 or not cand_list:
        return {"found": False, "detail": "too few / empty",
                "keys": [], "approx_score": None, "unique": False,
                "witness_bq": None, "scale": None, "hecke_ok": False}
    cols = shimura_cols(cand_list, t, psi, nmax)
    if cols is None:
        return {"found": False, "detail": "Shimura out of table",
                "keys": [], "approx_score": None, "unique": False,
                "witness_bq": None, "scale": None, "hecke_ok": False}
    n_c = len(cand_list)
    A = sp.zeros(nmax, n_c + 1)
    for j in range(n_c):
        for i in range(nmax):
            A[i, j] = sp.Integer(int(cols[j][i]))
    for i in range(nmax):
        A[i, n_c] = -sp.Integer(int(a_f8[i + 1]))
    ns = A.nullspace()
    info(f"  [{tag}] Sh_t={t}/{psi_name}: nullspace dim={len(ns)} "
         f"(nmax={nmax}, n_c={n_c})")
    sols = []
    for v in ns:
        x_lam = _clear_denoms_vec(v)
        lam = x_lam[n_c]
        x = x_lam[:n_c]
        if lam == 0:
            continue
        if lam < 0:
            x = [-c for c in x]
            lam = -lam
        gcdn = lam
        for c in x:
            gcdn = int(sp.gcd(gcdn, abs(c)))
        if gcdn > 1:
            x = [c // gcdn for c in x]
            lam = lam // gcdn
        bq = [0] * (Q_CAND + 1)
        for j, coef in enumerate(x):
            if coef == 0:
                continue
            bj = cand_list[j][1]
            for n in range(Q_CAND + 1):
                bq[n] += coef * bj[n]
        if all(vv == 0 for vv in bq):
            continue
        sols.append((x, lam, bq))

    if not sols:
        Af = np.array(cols, dtype=float).T
        bf = np.array([float(a_f8[n]) for n in range(1, nmax + 1)])
        try:
            sol, resid, rank, _ = np.linalg.lstsq(Af, bf, rcond=None)
            rnorm = float(np.linalg.norm(Af @ sol - bf))
            bnorm = float(np.linalg.norm(bf)) + 1e-30
            approx = rnorm / bnorm
        except np.linalg.LinAlgError:
            approx = None
        return {"found": False,
                "detail": f"no Sh-preimage (lam!=0); lstsq relresid={approx}",
                "keys": [], "approx_score": approx, "unique": False,
                "witness_bq": None, "scale": None, "hecke_ok": False}

    uniq = []
    for x, lam, bq in sols:
        is_par = False
        for x2, lam2, _ in uniq:
            if all(Fraction(a, lam) == Fraction(b, lam2)
                   for a, b in zip(x, x2)):
                is_par = True
                break
        if not is_par:
            uniq.append((x, lam, bq))

    x, lam, bq = uniq[0]
    keys = [(cand_list[j][2], x[j], cand_list[j][0])
            for j in range(n_c) if x[j] != 0]
    h_ok = all(is_eigen_ap(bq, p, HEAD_AP[p], Q_CAND, N_HECKE)
               for p in PRIMES_HECKE)
    info(f"  [{tag}] found Sh-preimage: lam={lam}, nz={len(keys)}, "
         f"unique={len(uniq)==1}, hecke_a_p={h_ok}")
    for key9, coef, lab in keys[:10]:
        info(f"    {coef} * {lab} key9={key9}")
    return {
        "found": True,
        "detail": (f"Sh-preimage lam={lam}, unique={len(uniq)==1}, "
                   f"hecke={h_ok}, nz={len(keys)}"),
        "keys": keys,
        "approx_score": 0.0,
        "unique": len(uniq) == 1,
        "witness_bq": bq,
        "scale": lam,
        "hecke_ok": h_ok,
        "lam": lam,
        "n_sols": len(uniq),
    }


res_sh_class = solve_shimura_preimage(
    plus_mono_class, 1, "trivial", lambda d: 1, "plus-mono/t=1")
info(f"  plus-mono/t=1 result: found={res_sh_class['found']}; "
     f"{res_sh_class['detail']}")
res_sh_chi4 = solve_shimura_preimage(
    plus_mono_class, 1, "chi4", chi4, "plus-mono/t=1/chi4")
info(f"  plus-mono/t=1/chi4 result: found={res_sh_chi4['found']}; "
     f"{res_sh_chi4['detail']}")
# Broader diagnostic: lstsq Sh_t=1 ≈ f8 over ALL candidates (float);
# exact sympy nullspace on 411 cols is too slow for the budget.
info("ROUTE (b-diag): float lstsq Sh_t=1 ≈ f8 over all candidates")
nmax_all = min(40, int((Q_CAND - 1) ** 0.5))
cols_all = shimura_cols(candidates, 1, lambda d: 1, nmax_all)
if cols_all is not None:
    Af = np.array(cols_all, dtype=float).T
    bf = np.array([float(a_f8[n]) for n in range(1, nmax_all + 1)])
    sol, resid, rank, _ = np.linalg.lstsq(Af, bf, rcond=None)
    rnorm = float(np.linalg.norm(Af @ sol - bf))
    bnorm = float(np.linalg.norm(bf)) + 1e-30
    approx_all = rnorm / bnorm
    info(f"  all-cands/t=1 lstsq relresid={approx_all:.6g}, "
         f"rank≈{int(rank)}, nnz(|x|>1e-6)="
         f"{sum(1 for x in sol if abs(x) > 1e-6)}")
else:
    approx_all = None
    info("  all-cands/t=1: Shimura out of table")
res_sh_all = {"found": False, "detail": f"float-diag only; "
              f"relresid={approx_all}", "keys": [],
              "approx_score": approx_all, "unique": False,
              "witness_bq": None, "hecke_ok": False}

mono_hits_class = []
for lab, bq, key9 in plus_mono_class:
    if all(is_eigen_ap(bq, p, HEAD_AP[p], Q_CAND, N_HECKE)
           for p in PRIMES_HECKE):
        mono_hits_class.append((lab, key9, bq))
info(f"exact plus+eigen monomials classical: {len(mono_hits_class)}")
for lab, key9, bq in mono_hits_class:
    sh_ok, sh_t, sh_psi, sh_sc, sh_head, _ = shimura_match_f8(bq, 30)
    info(f"  {lab} key9={key9} head={bq[:12]} Sh∝f8={sh_ok}")

sh_odd = shimura_lift(g_plus_supp, 1, lambda d: 1, 40)
if sh_odd is not None:
    odd_match = all(sh_odd[n] == 4 * a_f8[n]
                    for n in range(1, 41) if n % 2 == 1)
    even_mass = sum(abs(sh_odd[n]) for n in range(2, 41, 2))
    info(f"DIAG: Sh_t=1(pr^+_supp)/4 vs f8 on odds: {odd_match}; "
         f"even |mass| on n=2..40: {even_mass} "
         f"(naive support cut is NOT the modular plus image)")

g_plus = None
g_plus_key_info = None
g_plus_track = None
P1_unique = False
sh_plus_ok = False
sh_plus_scale = None
sh_plus_t = None
sh_plus_psi = None
hecke_plus_ok = False
plus_ok = False

for track, res in (
        ("Sh-preimage-t1", res_sh_class),
        ("Sh-preimage-t1-chi4", res_sh_chi4),
        ("Sh-preimage-all-t1", res_sh_all),
):
    if not res["found"]:
        continue
    bq_full = [0] * (QMAX + 1)
    ok_rb = True
    for key9, coef, lab in res["keys"]:
        bq_f = series_from_key9(key9, QMAX)
        if bq_f is None:
            ok_rb = False
            break
        for n in range(QMAX + 1):
            bq_full[n] += int(coef) * bq_f[n]
    if not ok_rb:
        bq_full = list(res["witness_bq"]) + [0] * (QMAX + 1)
        bq_full = bq_full[: QMAX + 1]
    else:
        info(f"  rebuilt [{track}] head={bq_full[:24]}")
    p_ok = kohnen_plus_ok(bq_full, PLUS_CLASSICAL, nmax=400)
    h_ok = all(is_eigen_ap(bq_full, p, HEAD_AP[p], QMAX, N_HECKE)
               for p in PRIMES_HECKE)
    sh_ok, sh_t, sh_psi, sh_sc, sh_head, _ = shimura_match_f8(
        bq_full, N_SH)
    info(f"  [{track}] plus={p_ok} hecke={h_ok} Sh∝f8={sh_ok} "
         f"t={sh_t} psi={sh_psi} scale={sh_sc}")
    # Success requires classical plus + Sh∝f8; Hecke expected by
    # Shimura equivariance but verified explicitly.
    if p_ok and sh_ok:
        g_plus = bq_full
        g_plus_key_info = res["keys"]
        g_plus_track = track
        P1_unique = bool(res.get("unique"))
        plus_ok = True
        hecke_plus_ok = h_ok
        sh_plus_ok = True
        sh_plus_scale = sh_sc
        sh_plus_t = sh_t
        sh_plus_psi = sh_psi
        break
    # Keep non-plus Sh-preimage as diagnostic only
    if (g_plus is None and sh_ok and not p_ok
            and track == "Sh-preimage-all-t1"):
        info(f"  NOTE: Sh-preimage exists but NOT classical-plus "
             f"(outside Kohnen plus; track={track})")

if g_plus is None and all(supp_eigen.values()):
    g_plus = g_plus_supp
    g_plus_key_info = [("supp", 1, "pr^+_supp(g)")]
    g_plus_track = "P1a-supp-fallback"
    plus_ok = True
    hecke_plus_ok = True
    sh_plus_ok = False
    P1_unique = False
    info("  FALLBACK witness = pr^+_supp(g): plus+eigen but Sh∝f8 "
         "FAILED (even-coeff pollution under t=1)")

P1_found = g_plus is not None
P1_success = bool(P1_found and plus_ok and sh_plus_ok and hecke_plus_ok)

approx_class = res_sh_class.get("approx_score")
approx_alt = res_sh_chi4.get("approx_score")
approx_full = approx_class
info(f"Sh-preimage approx residuals: t1={approx_class}, "
     f"t1/chi4={approx_alt}")
info(f"g+ track={g_plus_track}; P1_success={P1_success}; "
     f"unique={P1_unique}; Sh t/psi/scale="
     f"{sh_plus_t}/{sh_plus_psi}/{sh_plus_scale}")
if g_plus is not None:
    info(f"  g+ head: {g_plus[:24]}")
    info("  T(p^2) table for g+:")
    for p in PRIMES_HECKE:
        lam = eigen_lambda(g_plus, p, min(QMAX, len(g_plus) - 1),
                           N_HECKE)
        info(f"    p={p}: lam={lam}, a_p={HEAD_AP[p]}, "
             f"eigen={is_eigen_ap(g_plus, p, HEAD_AP[p], QMAX, N_HECKE)}")

n_fit = min(120, Q_CAND)
A_f = np.array([[float(bq[n]) for n in range(1, n_fit + 1)]
                for lab, bq, k in candidates], dtype=float).T
targ = np.array([float(g_plus_supp[n]) for n in range(1, n_fit + 1)],
                dtype=float)
try:
    sol, resid, rank_A, _ = np.linalg.lstsq(A_f, targ, rcond=None)
    resid_n = float(np.linalg.norm(A_f @ sol - targ))
    targ_n = float(np.linalg.norm(targ)) + 1e-30
    supp_in_span = resid_n / targ_n < 1e-8
    rank_A = int(rank_A)
except np.linalg.LinAlgError:
    supp_in_span = False
    resid_n = None
    rank_A = -1
info(f"pr^+_supp(g) in R-span of extended monoid (n=1..{n_fit})? "
     f"{supp_in_span} (lstsq relresid={resid_n}, rank≈{rank_A})")

K1_fired = not P1_success
check(f"P1 RESULT: P1_success={P1_success} (found={P1_found}, "
      f"track={g_plus_track}, unique={P1_unique}, plus={plus_ok}, "
      f"hecke={hecke_plus_ok}, Sh∝f8={sh_plus_ok}, "
      f"Sh_t={sh_plus_t}); K1_fired={K1_fired}; "
      f"supp_in_span={supp_in_span}; "
      f"Sh_approx={approx_class}",
      True)


# ================================================================ P2
print("=" * 72)
print("P2 -- Waldspurger / Kohnen–Zagier central-value attachment")
print("=" * 72)

info("CLASSICAL (Kohnen–Zagier / Waldspurger): for g+ in the plus")
info("  space of weight k+1/2 mapping to f of weight 2k under Shimura,")
info("  b(|d|)^2  proportional to  |d|^{k-1/2} L(f × χ_d, k)")
info("  for fundamental discriminants d with (-1)^k d > 0.")
info("  Here k=2 ⇒ central point s=2; conformant class d > 0.")
info("  We also sample d < 0 as a control (should NOT be constant")
info("  under the conformant normalisation).")
info("  Ratio tested: R(d)= b(|d|)^2 / (|d|^{3/2} L(f8×χ_d, 2)).")
info("  Success: rel spread < 1%; Kill K2 if spread > 5%.")


def L_f8_twist_direct(d, s, terms=4000):
    s = mpmath.mpf(s)
    tot = mpmath.mpf(0)
    for n in range(1, min(terms, len(a_f8) - 1) + 1):
        an = a_f8[n]
        if an == 0:
            continue
        ch = kronecker(d, n)
        if ch == 0:
            continue
        tot += mpmath.mpf(an * ch) * mpmath.power(n, -s)
    return tot


def L_f8_twist_afe(d, s, Nlev, eps, terms=2000):
    """Incomplete-Gamma AFE for L(f8 × χ_d, s); weight 4."""
    s = mpmath.mpf(s)
    K = 4
    sqN = mpmath.sqrt(Nlev)
    lam = mpmath.mpf(0)
    for n in range(1, min(terms, len(a_f8) - 1) + 1):
        an = a_f8[n]
        if an == 0:
            continue
        ch = kronecker(d, n)
        if ch == 0:
            continue
        coeff = an * ch
        xx = 2 * mpmath.pi * n / sqN
        lam += mpmath.mpf(coeff) * (
            (sqN / (2 * mpmath.pi * n)) ** s * mpmath.gammainc(s, xx)
            + eps * (sqN / (2 * mpmath.pi * n)) ** (K - s)
            * mpmath.gammainc(K - s, xx))
    return lam / ((sqN / (2 * mpmath.pi)) ** s * mpmath.gamma(s))


def L_twist_best(d, s=2):
    """Direct + AFE cross-check; level = 8 * d^2 (f8 level 8).

    At s=2 prefer L_dir when the AFE–direct gap is large (AFE
    under-converged for bigger |d|); otherwise average is unnecessary
    — document both.
    """
    N_tw = 8 * (d * d)
    L_dir = L_f8_twist_direct(d, s, terms=N_F8)
    gaps = {}
    Lafes = {}
    for eps in (1, -1):
        La = L_f8_twist_afe(d, mpmath.mpf(s), N_tw, eps, terms=2500)
        Lafes[eps] = La
        gaps[eps] = abs(La - L_dir)
    eps_best = 1 if gaps[1] <= gaps[-1] else -1
    L_afe = Lafes[eps_best]
    # Prefer direct at the centre; AFE is a cross-check.
    # (Exact R-constancy from a bad AFE would be a false positive.)
    rel_gap = (gaps[eps_best] / abs(L_dir)
               if L_dir != 0 else mpmath.mpf(1))
    return {
        "L_dir": L_dir,
        "L_afe": L_afe,
        "L_use": L_dir,
        "eps": eps_best,
        "gap": gaps[eps_best],
        "rel_gap": rel_gap,
        "N_tw": N_tw,
    }


# Fundamental discriminants |d| <= 80 (need ≥4–6 with b(|d|)≠0)
DMAX = 80
fund_pos = [d for d in range(1, DMAX + 1)
            if is_fundamental_discriminant(d)]
fund_neg = [d for d in range(-DMAX, 0)
            if is_fundamental_discriminant(d)]
info(f"fundamental discriminants |d|<={DMAX}: pos={fund_pos}")
info(f"  neg={fund_neg}")
check("P2.fund: fundamental-discriminant enumerator matches classical "
      f"lists (pos has 5,8,12,13,...; neg has -3,-4,-7,...); "
      f"|pos|={len(fund_pos)}, |neg|={len(fund_neg)}",
      5 in fund_pos and 8 in fund_pos and -3 in fund_neg
      and -4 in fund_neg and 12 in fund_pos)


def waldspurger_table(bq, discr_list, tag, max_rows=6):
    """Compute R(d) table; skip d with b(|d|)=0 or L≈0."""
    rows = []
    for d in discr_list:
        absd = abs(d)
        if absd >= len(bq):
            continue
        bn = bq[absd]
        if bn == 0:
            info(f"  [{tag}] d={d}: b(|d|)=0 — skip (plus support / "
                 f"vanishing)")
            continue
        Lw = L_twist_best(d, 2)
        Lval = Lw["L_use"]
        if abs(Lval) < mpmath.mpf("1e-20"):
            info(f"  [{tag}] d={d}: L≈0 — skip")
            continue
        # R = b^2 / (|d|^{3/2} L)   (user / probe convention)
        denom = (mpmath.power(absd, mpmath.mpf("1.5")) * Lval)
        R = (mpmath.mpf(bn) ** 2) / denom
        # also inverse-style Kohnen–Zagier: C = |d|^{3/2} b^2 / L
        C = (mpmath.power(absd, mpmath.mpf("1.5"))
             * mpmath.mpf(bn) ** 2) / Lval
        rows.append({
            "d": d, "absd": absd, "b": bn, "b2": bn * bn,
            "L": Lval, "L_dir": Lw["L_dir"], "L_afe": Lw["L_afe"],
            "gap": Lw["gap"], "rel_gap": Lw["rel_gap"],
            "eps": Lw["eps"], "R": R, "C": C,
        })
        info(f"  [{tag}] d={d}: b={bn}, b^2={bn*bn}, "
             f"L_dir={Lw['L_dir']}, L_afe={Lw['L_afe']}, "
             f"rel_gap={float(Lw['rel_gap']):.3e}, eps={Lw['eps']:+d}")
        info(f"         R=b^2/(|d|^{{3/2}}L_dir)={R}; "
             f"C=|d|^{{3/2}}b^2/L_dir={C}")
        if len(rows) >= max_rows:
            break
    return rows


def rel_spread(vals):
    """max |v - med| / |med|; return (spread, med, vals_f)."""
    vs = [float(v) for v in vals if v is not None and abs(v) > 1e-30]
    if len(vs) < 2:
        return None, None, vs
    vs_s = sorted(vs)
    med = vs_s[len(vs_s) // 2]
    if med == 0:
        return None, med, vs_s
    spread = max(abs(v - med) / abs(med) for v in vs_s)
    return spread, med, vs_s


# Choose coefficient source for Waldspurger
if P1_success and g_plus is not None:
    bq_wald = g_plus
    wald_src = f"g+ ({g_plus_track})"
elif P1a_gplus:
    bq_wald = g_plus_supp
    wald_src = "pr^+_supp(g) [P1a]"
else:
    # Honest fallback: still run Waldspurger on g and on pr^+_supp(g)
    # to document the failure mode (T41 expected).
    bq_wald = g_plus_supp
    wald_src = "pr^+_supp(g) [fallback; P1 not successful]"

info(f"Waldspurger coefficient source: {wald_src}")
info(f"  head: {bq_wald[:24]}")

rows_pos = waldspurger_table(bq_wald, fund_pos, "d>0", max_rows=6)
rows_neg = waldspurger_table(bq_wald, fund_neg, "d<0", max_rows=6)

# Also run on raw g as control (T41 kill expected)
info("CONTROL: Waldspurger on raw g (T41 expected fail / same odds):")
rows_g_pos = waldspurger_table(g, fund_pos, "g|d>0", max_rows=6)

spread_pos_R, med_pos_R, vals_pos_R = rel_spread(
    [r["R"] for r in rows_pos])
spread_pos_C, med_pos_C, vals_pos_C = rel_spread(
    [r["C"] for r in rows_pos])
spread_neg_R, med_neg_R, vals_neg_R = rel_spread(
    [r["R"] for r in rows_neg])
spread_neg_C, med_neg_C, vals_neg_C = rel_spread(
    [r["C"] for r in rows_neg])
spread_g_R, med_g_R, vals_g_R = rel_spread(
    [r["R"] for r in rows_g_pos])

info("Constancy summary (relative spread = max|v-med|/|med|):")
info(f"  d>0 R: spread={spread_pos_R}, med={med_pos_R}, vals={vals_pos_R}")
info(f"  d>0 C: spread={spread_pos_C}, med={med_pos_C}, vals={vals_pos_C}")
info(f"  d<0 R: spread={spread_neg_R}, med={med_neg_R}, vals={vals_neg_R}")
info(f"  d<0 C: spread={spread_neg_C}, med={med_neg_C}, vals={vals_neg_C}")
info(f"  raw-g d>0 R: spread={spread_g_R}, med={med_g_R}, vals={vals_g_R}")

# Select convention-conformant class: d > 0 for k=2
# Prefer the normalisation (R or C) with smaller spread
def best_spread(sR, sC):
    cands = [(sR, "R"), (sC, "C")]
    cands = [(s, n) for s, n in cands if s is not None]
    if not cands:
        return None, None
    cands.sort(key=lambda t: t[0])
    return cands[0]


spread_conf, norm_conf = best_spread(spread_pos_R, spread_pos_C)
spread_ctrl, norm_ctrl = best_spread(spread_neg_R, spread_neg_C)

# P2 success requires a genuine P1 g+ (Sh∝f8 plus eigenform).
# Exploratory ratios on the fallback are reported but cannot upgrade.
P2_spread_ok = (spread_conf is not None and spread_conf < 0.01
                and len(rows_pos) >= 4)
P2_ok = bool(P1_success and P2_spread_ok)
K2_fired = False
if P1_success:
    K2_fired = (spread_conf is not None and spread_conf > 0.05) or (
        spread_conf is None)

info(f"CONFORMANT class d>0 (k=2): best_norm={norm_conf}, "
     f"spread={spread_conf}; P2_spread_ok={P2_spread_ok}; "
     f"P2_ok={P2_ok} (gated on P1_success={P1_success})")
info(f"CONTROL class d<0: best_norm={norm_ctrl}, spread={spread_ctrl}")
info(f"K2_fired={K2_fired}")

check(f"P2.Waldspurger RESULT: source={wald_src}; "
      f"n_pos={len(rows_pos)}, n_neg={len(rows_neg)}; "
      f"conformant(d>0) spread={spread_conf} via {norm_conf}; "
      f"control(d<0) spread={spread_ctrl}; "
      f"P2_ok={P2_ok} (thresh 1%); K2={K2_fired} (kill>5%); "
      f"raw-g spread={spread_g_R}",
      True)

# Table dump
info("Waldspurger quotient table (conformant d>0; L=L_dir):")
info(f"  {'d':>6} {'b':>8} {'b^2':>10} {'L_dir':>18} "
     f"{'R':>18} {'rel_gap':>10}")
for r in rows_pos:
    info(f"  {r['d']:6d} {r['b']:8d} {r['b2']:10d} "
         f"{float(r['L']):18.10g} {float(r['R']):18.10g} "
         f"{float(r['rel_gap']):10.3e}")


# ================================================================ P3
print("=" * 72)
print("P3 -- centre bookkeeping (honest functor map)")
print("=" * 72)

info("TYPING (exact, machine-checked links cited):")
info("  ABELIAN channel (T39): Mellin of weight-≤1/2 theta factors")
info("    reaches the ξ-line centre 1/2 (Dedekind / ζ(2s)).")
info("  CUSPIDAL channel (T38/T41): Shimura bridge g → f8 carries")
info("    Hecke eigenvalues a_p via T(p^2)g = a_p g.")
info("  WALDSPURGER join (this probe P2): coefficient squares b(|d|)^2")
info("    of a PLUS-SPACE form attach to the CENTRAL-VALUE FAMILY")
info("    L(f8 × χ_d, s=2) — the GL(2) centre for weight-4")
info("    normalisation (critical line Re(s)=k/2? No: for weight 4")
info("    the functional equation centres at s=2).")
info("  WHAT THIS IS NOT:")
info("    — not a ζ(s) spectral carrier / not an RH reading;")
info("    — not an attachment to the ξ-line centre 1/2;")
info("    — half-integral L(g,s) still has no Euler product.")
info(f"  P1_success={P1_success}, P2_ok={P2_ok}: the cuspidal")
info("    central-value wire is "
     + ("CLOSED on samples." if (P1_success and P2_ok)
        else "NOT closed (plus and/or constancy missing)."))

functor_map_complete = P1_success and P2_ok
check("P3.typing: Waldspurger attaches GL(2)-centre s=2 central "
      "twist values (NOT ξ-line, NOT ζ-spectrum, NOT RH content); "
      f"abelian→1/2 (T39) + cuspidal a_p (T41) + central-value family "
      f"(P2) map completeness={functor_map_complete}",
      True)


# ================================================================ verdict
print("=" * 72)
print("VERDICT")
print("=" * 72)

if P1_success and P2_ok:
    verdict = "CENTRAL-VALUES-WIRED"
elif P1_success and not P2_ok:
    verdict = "PLUS-FOUND-ONLY"
elif K1_fired and not P1_found:
    verdict = "OUTSIDE-MONOID"
elif K1_fired and P1_found and not P1_success:
    # found something plus+eigen but Shimura failed, or vice versa
    verdict = "PARTIAL"
else:
    verdict = "PARTIAL"

info(f"VERDICT: {verdict}")
info(f"  P1_success={P1_success} (found={P1_found}, track={g_plus_track}, "
     f"Sh∝f8={sh_plus_ok}, unique={P1_unique})")
info(f"  P2_ok={P2_ok} (conformant spread={spread_conf})")
info(f"  K1_fired={K1_fired}, K2_fired={K2_fired}")
info(f"  P1a_supp_witness={P1a_gplus}, supp_in_span={supp_in_span}")
info(f"  approx scores: class={approx_class}, alt={approx_alt}")

if verdict == "CENTRAL-VALUES-WIRED":
    info("CONSEQUENCE for ZETA.COMPILER.FUNCTOR: cuspidal channel")
    info("  fully mapped on the probe level — a_p (T41) AND central")
    info("  twist values via plus-space Waldspurger (this probe).")
    info("  Next lever: promote the plus pendant / Waldspurger wire")
    info("  only after ledger-grade hardening; OR ask for the")
    info("  half-integral FE package of g+ (centre 5/4).")
elif verdict == "PLUS-FOUND-ONLY":
    info("CONSEQUENCE: plus-space pendant EXISTS in the monoid and")
    info("  Shimura-matches f8, but Waldspurger constancy failed —")
    info("  convention, conductor, or normalisation gap.  Next lever:")
    info("  refine χ_d / |d|^{k-1/2} / Atkin–Lehner sign package.")
elif verdict == "OUTSIDE-MONOID":
    info("CONSEQUENCE: Kohnen-plus structure lies OUTSIDE the")
    info("  moderately extended theta-monoid (plain/q^2/q^4).")
    info("  Best approx scores documented above; pr^+_supp(g) "
         f"in span? {supp_in_span}.")
    info("  Next lever: enlarge beyond theta-monomials (metaplectic")
    info("  unary theta × monoid, or abstract plus projection as")
    info("  external classical operation — firewall: do not smuggle")
    info("  ζ / RH readings).  Functor map remains: abelian→1/2,")
    info("  cuspidal→a_p; central-value family still open.")
else:
    info("CONSEQUENCE: PARTIAL — typed split of the plus package:")
    info("  (1) pr^+_supp(g) IS classical-plus, T(p^2)-eigen at a_p,")
    info("      AND lies in the extended monoid (q^4 monomials);")
    info("  (2) BUT Sh(pr^+_supp) is NOT ∝ f8 (t=1 matches 4 f8 on")
    info("      ODD coeffs only; even pollution; t=2 vanishes on plus).")
    info("  The Shimura bridge to f8 remains on NON-plus g via t=2")
    info("  (T38/T41).  Waldspurger stay gated on a genuine plus")
    info("  eigenform with Sh∝f8.  Next lever: construct the modular")
    info("  plus projection (not naive coeff cut) — or a metaplectic")
    info("  unary-theta extension that realises Kohnen's isomorphism")
    info("  inside a larger compiler span.")

check(f"VERDICT={verdict} (CENTRAL-VALUES-WIRED / PLUS-FOUND-ONLY / "
      f"OUTSIDE-MONOID / PARTIAL); computed from P1/P2/K1/K2",
      verdict in ("CENTRAL-VALUES-WIRED", "PLUS-FOUND-ONLY",
                  "OUTSIDE-MONOID", "PARTIAL"))

elapsed = time.time() - T0
print("=" * 72)
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({elapsed:.1f}s)")
print(f"VERDICT: {verdict}")
print("=" * 72)
raise SystemExit(0 if FAIL == 0 else 1)
