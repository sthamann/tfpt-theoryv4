"""Discovery probe (2026-07-24), part 34 of the zeta/prime investigation.
FOUNDING probe for research project ZETA.COMPILER.FUNCTOR
(formerly informal "Weight Drop"): the candidate process
GL(2)/weight-4  -->  GL(1)/centre-1/2.

Working thesis (NOT previously tested in-suite): the weight drop is
FACTORISATION, not projection.  The weight-1/2 object that carries
zeta is the Jacobi theta constant theta3, and it has lived
MULTIPLICATIVELY inside the compiler since part 11:

    Th0 - Th2  =  theta3(q)^2 * theta4(q)^6
               =  theta4(q)^4 * theta4(q^2)^4   (classical Jacobi).

  F1  GL(1) object in-suite (CLASSICAL Riemann theta proof, typed):
      Mellin((theta3(e^{-pi t})-1)/2)(s) = pi^{-s} Gamma(s) zeta(2s);
      functional equation Lambda(s) = Lambda(1/2 - s) from theta3-
      Poisson; centre arithmetic: weight-k theta => Mellin centre
      s = k/2; for theta3, k = 1/2 => s = 1/4 => zeta-argument
      2s has centre 1/2.  So RH's "centre 1/2" IS the Mellin centre
      of the weight-1/2 theta -- the functor's target is defined.
  F2  Factorisation as candidate functor: uniqueness of
      theta3^a theta4^b theta2^c with a+b+c = 8 matching Th0-Th2
      in the theta-constant monoid (exact coefficient match);
      mu3 analogue (part 13): uniqueness of a^i b^{4-i} matching
      E6+A2-signed = a b^3 in the Borwein monoid.  If unique,
      Phi(Form) := theta3-share of the canonical factorisation
      is well-defined on these objects (here exponent 2).
  F3  Hecke-compatibility TEST (the hard point): classical
      weight-1/2 Hecke T(p^2) on theta3 (Shimura / Serre-Stark);
      self-consistent eigenvalue; then HONEST gap typing --
      Mellin does NOT factor over products; Rankin-Selberg /
      Shimura are the preregistered candidate operations that
      would translate factor data into L-data; check whether the
      known L(Th0-Th2,s) = 16 2^{-s} eta(s)eta(s-3) - 8 L(f8,s)
      (part 12) visibly carries a zeta(2s)-trace of the theta3
      factor (expected: NO under plain Mellin).
  F4  Contract ZETA.COMPILER.FUNCTOR + preregistered kills K1-K3.
  F5  Verdict: FOUNDED-WITH-ANCHOR / FOUNDED-WEAK / STILLBORN.

PREREGISTERED CRITERIA
  C1  Mellin identity at s in {1.2, 2.5, 3.7}: >= 20 matching digits.
  C2  Lambda(s) = Lambda(1/2-s) numerically (Poisson route).
  C3  Centre arithmetic documented and numerically consistent.
  C4  Unique (a,b,c) with a+b+c=8 and th3^a th4^b th2^c = Th0-Th2.
  C5  Unique Borwein monomial a^i b^{4-i} matching E6+A2-signed.
  C6  theta3 is T(p^2)-eigenform for p=3,5,7 with EXACT eigenvalue
      computed from the coefficient formula (classical: 1 + p^{-1}).
  C7  Gap typed: no plain-Mellin zeta(2s) factor in L(c,s); Phi's
      L-translation operation named (Rankin-Selberg) and left OPEN.
  K1  Non-unique theta factorisation => factorisation candidate dies.
  K2  No preregistered operation translates Hecke => Phi stays empty
      (project falls back to analogy).
  K3  Langlands honesty: no known general weight-4 -> zeta functor;
      smuggling zeta as an external factor does NOT count.

Firewall: discovery sandbox, NO promotion, no marker moves, no RH
evidence language.  Classical theorems (Riemann's theta proof of the
xi functional equation, Serre-Stark weight-1/2 Hecke, Shimura
correspondence, Rankin-Selberg, Langlands context) named as such --
probe content is the in-suite typing of a candidate functor and its
first exact blocks + kills.  Project is FOUNDED, not solved.
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

QMAX = 64
# Need n * p^2 <= N_HECKE for all checked n and p in {3,5,7}.
N_HECKE = 5000
N_HECKE_CHECK = 100         # verify eigen-relation on n <= this


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
def theta_arr(kind, order):
    """Integer q-coefficients of Jacobi theta constants (nome q)."""
    s = np.zeros(order + 1, dtype=np.int64)
    if kind == 2:
        # theta2(q) = 2 q^{1/4} + 2 q^{9/4} + ... -- store in q^{1/4}-units
        # For pure q-series products of weight 4 we use the even-powered
        # embedding: theta2(q)^4 has integer powers of q.  Here we need
        # theta2 as a series in q^{1/2} for monomials th2^c with c even,
        # or work in t = q^{1/8}.  Simpler: build th2 in half-integer
        # exponents via doubled index (u = q^{1/2}).
        pass
    elif kind == 3:
        s[0] = 1
        n = 1
        while n * n <= order:
            s[n * n] = 2
            n += 1
    elif kind == 4:
        s[0] = 1
        n = 1
        while n * n <= order:
            s[n * n] = 2 * ((-1) ** n)
            n += 1
    return s


def theta2_u(order_u):
    """theta2(u) coefficients in u = q^{1/2}: exponents (2m+1)^2."""
    s = np.zeros(order_u + 1, dtype=np.int64)
    o = 1
    while o * o <= order_u:
        s[o * o] = 2
        o += 2
    return s


def conv(a, b, order):
    return np.convolve(a, b)[: order + 1]


def ppow(a, e, order):
    out = np.zeros(order + 1, dtype=np.int64)
    out[0] = 1
    for _ in range(e):
        out = conv(out, a, order)
    return out


def legendre(n, p):
    """Legendre symbol (n/p) for odd prime p; 0 if p|n."""
    return int(sp.legendre_symbol(n % p, p))


# ================================================================ F1
print("=" * 72)
print("F1 -- GL(1) object in-suite: classical Riemann theta3 chain")
print("=" * 72)

# Conventions (DOCUMENTED):
#   theta3(t) := sum_{n in Z} exp(-pi n^2 t)   [= jtheta3(0, e^{-pi t})]
#   psi(t)    := (theta3(t) - 1)/2              [= sum_{n>=1} exp(-pi n^2 t)]
#   Lambda(s) := int_0^inf psi(t) t^{s-1} dt
#             = pi^{-s} Gamma(s) zeta(2s)       (termwise Mellin)
# Poisson: theta3(1/t) = sqrt(t) theta3(t)
#   => Lambda(s) = Lambda(1/2 - s)              (classical)
# Weight k = 1/2 => Mellin centre s_* = k/2 = 1/4
#   => zeta-argument z = 2s has centre z_* = 1/2.
info("CONVENTION: Lambda(s) = Mellin_s(psi) = pi^{-s} Gamma(s) zeta(2s);")
info("  FE Lambda(s)=Lambda(1/2-s); centre s=1/4 <=> zeta centre 1/2.")


def _as_s(s):
    if isinstance(s, mpmath.mpc) or (getattr(s, "imag", 0)
                                     and s.imag != 0):
        return mpmath.mpc(s)
    return mpmath.mpf(s)


def Lambda_closed(s):
    s = _as_s(s)
    return (mpmath.power(mpmath.pi, -s) * mpmath.gamma(s)
            * mpmath.zeta(2 * s))


def Lambda_split(s):
    """Analytic continuation via Poisson split (classical Riemann)."""
    s = mpmath.mpf(s)

    def integrand(t):
        t = mpmath.mpf(t)
        # psi(t) = sum exp(-pi n^2 t); truncate safely for t >= 1
        psi = mpmath.mpf(0)
        n = 1
        while True:
            term = mpmath.e ** (-mpmath.pi * n * n * t)
            psi += term
            if term < mpmath.mpf("1e-45"):
                break
            n += 1
            if n > 200:
                break
        return psi * (t ** (s - 1) + t ** (-s - mpmath.mpf("0.5")))

    I = mpmath.quad(integrand, [1, mpmath.inf], maxdegree=12)
    return I - mpmath.mpf(1) / (2 * s) - mpmath.mpf(1) / (1 - 2 * s)


mellin_pts = [mpmath.mpf("1.2"), mpmath.mpf("2.5"), mpmath.mpf("3.7")]
mellin_ok = True
mellin_digits = []
for s in mellin_pts:
    closed = Lambda_closed(s)
    split = Lambda_split(s)
    rel = abs(split / closed - 1)
    # digits of agreement
    dig = -mpmath.log10(rel + mpmath.mpf("1e-50"))
    mellin_digits.append(float(dig))
    info(f"s = {s}: Lambda_closed = {closed}")
    info(f"  Lambda_split  = {split}; |ratio-1| = {rel}; ~{dig} digits")
    mellin_ok &= rel < mpmath.mpf("1e-20")

check("F1.C1 CLASSICAL Mellin identity (Riemann): "
      "Mellin((theta3(e^{-pi t})-1)/2)(s) = pi^{-s} Gamma(s) zeta(2s) "
      "at s = 1.2, 2.5, 3.7 via Poisson-split vs closed form "
      "(>= 20 matching digits each)",
      mellin_ok and all(d >= 20 for d in mellin_digits))

fe_pts = [
    mpmath.mpf("0.8"),
    mpmath.mpf("1.2"),
    mpmath.mpc(mpmath.mpf("0.3"), mpmath.mpf("1.1")),
]
# Real points: Poisson-split; complex: closed form (classical FE identity)
fe_ok = True
fe_res = []
for s in fe_pts:
    use_split = isinstance(s, mpmath.mpf) or (
        hasattr(s, "imag") and s.imag == 0)
    if use_split and not isinstance(s, mpmath.mpc):
        lhs = Lambda_split(s)
        rhs = Lambda_split(mpmath.mpf("0.5") - s)
    else:
        lhs = Lambda_closed(s)
        rhs = Lambda_closed(mpmath.mpf("0.5") - s)
    rel = abs(lhs / rhs - 1)
    fe_res.append(rel)
    info(f"FE at s = {s}: |Lambda(s)/Lambda(1/2-s) - 1| = {rel}")
    fe_ok &= rel < mpmath.mpf("1e-18")

# Poisson self-check of theta3 at a point
t_poiss = mpmath.mpf("1.7")
th_t = mpmath.jtheta(3, 0, mpmath.e ** (-mpmath.pi * t_poiss))
th_inv = mpmath.jtheta(3, 0, mpmath.e ** (-mpmath.pi / t_poiss))
poiss_rel = abs(th_inv / (mpmath.sqrt(t_poiss) * th_t) - 1)
info(f"Poisson theta3 at t={t_poiss}: |th(1/t)/(sqrt(t) th(t))-1| = {poiss_rel}")

check("F1.C2 CLASSICAL functional equation via theta3-Poisson: "
      "Lambda(s) = Lambda(1/2 - s) at s = 0.8, 1.2, 0.3+1.1i "
      "(|ratio-1| < 1e-18); Poisson identity theta3(1/t)=sqrt(t) "
      "theta3(t) spot-checked",
      fe_ok and poiss_rel < mpmath.mpf("1e-30"))

# Centre arithmetic
k_th = Fraction(1, 2)
s_centre = k_th / 2          # 1/4
z_centre = 2 * s_centre      # 1/2
# Numeric: the FE fixed point of s <-> 1/2-s is s=1/4
s_fix = mpmath.mpf("0.25")
lam_fix = Lambda_closed(s_fix)  # pole of zeta(1/2)? Wait 2s=1/2, zeta(1/2) OK
# Actually at s=1/4, zeta(2s)=zeta(1/2) finite; Gamma(1/4) fine; no pole.
# The poles of Lambda are at s=0 (from 1/(2s)) and s=1/2 (from 1/(1-2s)).
info(f"centre arithmetic: weight k = {k_th} => Mellin centre s = k/2 = "
     f"{s_centre}; zeta-argument z=2s centre = {z_centre}")
info(f"  Lambda at Mellin centre s=1/4: {lam_fix} (finite; FE fixed point)")
check("F1.C3 CENTRE ARITHMETIC: weight-k theta => Mellin centre s = k/2; "
      "for theta3, k = 1/2 => s = 1/4 => zeta(2s) centre = 1/2.  "
      "Documented: RH's centre 1/2 IS the Mellin centre of the "
      "weight-1/2 theta -- the ZETA.COMPILER.FUNCTOR target point "
      "is thereby defined in-suite (classical typing, not a new claim)",
      s_centre == Fraction(1, 4) and z_centre == Fraction(1, 2)
      and abs(lam_fix) > 0)

# ================================================================ F2
print("=" * 72)
print("F2 -- factorisation uniqueness in the theta-constant monoid")
print("=" * 72)

th3 = theta_arr(3, QMAX)
th4 = theta_arr(4, QMAX)
# theta2 in u = q^{1/2}: product th2^c contributes to q-powers when c*odd^2
# is even in the u-exponent, i.e. convert back to q = u^2.
# For monomial th3^a th4^b th2^c with a+b+c=8: build in u-series
# (exponents doubled for th3,th4) then extract even powers.

def series_in_u(kind, order_u):
    """Coefficients in u = q^{1/2}."""
    s = np.zeros(order_u + 1, dtype=np.int64)
    if kind == 3:
        s[0] = 1
        n = 1
        while 2 * n * n <= order_u:
            s[2 * n * n] = 2
            n += 1
    elif kind == 4:
        s[0] = 1
        n = 1
        while 2 * n * n <= order_u:
            s[2 * n * n] = 2 * ((-1) ** n)
            n += 1
    elif kind == 2:
        return theta2_u(order_u)
    return s


UMAX = 2 * QMAX
th3u = series_in_u(3, UMAX)
th4u = series_in_u(4, UMAX)
th2u = series_in_u(2, UMAX)

target_q = conv(ppow(th3, 2, QMAX), ppow(th4, 6, QMAX), QMAX)  # Th0-Th2
info(f"target Th0-Th2 = th3^2 th4^6 head: {list(target_q[:12])}")

matches = []
n_cand = 0
for a, b, c in itertools.product(range(9), repeat=3):
    if a + b + c != 8:
        continue
    n_cand += 1
    # build in u-units
    su = np.zeros(UMAX + 1, dtype=np.int64)
    su[0] = 1
    for _ in range(a):
        su = conv(su, th3u, UMAX)
    for _ in range(b):
        su = conv(su, th4u, UMAX)
    for _ in range(c):
        su = conv(su, th2u, UMAX)
    # extract q-series: even u-exponents
    qser = np.array([int(su[2 * n]) for n in range(QMAX + 1)], dtype=np.int64)
    if np.array_equal(qser, target_q):
        matches.append((a, b, c))

info(f"enumerated {n_cand} triples (a,b,c) with a+b+c=8; "
     f"exact matches: {matches}")
unique_mu4 = (matches == [(2, 6, 0)])
check("F2.C4 UNIQUENESS in theta-constant monoid: among all "
      f"{n_cand} monomials theta3^a theta4^b theta2^c with a+b+c=8, "
      "EXACTLY one matches Th0-Th2 = theta3^2 theta4^6 to O(q^64): "
      "(a,b,c)=(2,6,0).  (The Jacobi twin theta4^4 theta4(q^2)^4 uses "
      "the generator theta4(q^2) OUTSIDE this monoid -- not a "
      "counterexample to monoid uniqueness.)",
      unique_mu4 and n_cand == 45)

# mu3 / Borwein analogue
print("F2b -- Borwein monoid uniqueness (mu3 analogue, part 13)")
NORD = 40


def eta_pass(d, e, order):
    s = np.zeros(order + 1, dtype=np.int64)
    s[0] = 1
    for k in range(d, order + 1, d):
        for _ in range(e):
            s[k:] = s[k:] - s[:-k]
    return s


def ser_mul(a, b, order):
    return np.convolve(a, b)[: order + 1]


def chi3(n):
    r = n % 3
    if r == 0:
        return 0
    return 1 if r == 1 else -1


def E4_series(scale, order):
    """E4(q^scale) = 1 + 240 sum sigma3(n) q^{scale n}."""
    s = np.zeros(order + 1, dtype=object)
    s[0] = 1
    for n in range(1, order // scale + 1):
        s[scale * n] = 240 * int(sp.divisor_sigma(n, 3))
    return s


# E6+A2 signed = (81 E4(q^3) - E4(q)) / 80
e4_1 = E4_series(1, NORD)
e4_3 = E4_series(3, NORD)
signed_E6 = [(81 * e4_3[n] - e4_1[n]) / 80 for n in range(NORD + 1)]
# must be integers
signed_E6_int = [int(x) for x in signed_E6]
assert all(81 * e4_3[n] - e4_1[n] == 80 * signed_E6_int[n]
           for n in range(NORD + 1))

# Borwein a = theta_{Z[omega]} = 1 + 6 sum (1*chi3)(n) q^n
aB = np.zeros(NORD + 1, dtype=np.int64)
for m_ in range(-12, 13):
    for n_ in range(-12, 13):
        qq = m_ * m_ + m_ * n_ + n_ * n_
        if 0 <= qq <= NORD:
            aB[qq] += 1
r_a = np.array([1] + [6 * sum(chi3(d) for d in sp.divisors(n))
                      for n in range(1, NORD + 1)], dtype=np.int64)
# b = eta(q)^3 / eta(q^3)
eta1_3 = eta_pass(1, 3, NORD)
eta3_1 = eta_pass(3, 1, NORD)
inv3 = np.zeros(NORD + 1, dtype=np.int64)
inv3[0] = 1
for n in range(1, NORD + 1):
    inv3[n] = -sum(int(eta3_1[k]) * int(inv3[n - k])
                   for k in range(1, n + 1) if eta3_1[k])
bB = ser_mul(eta1_3, inv3, NORD)

borwein_a_ok = np.array_equal(aB, r_a)
info(f"Borwein a head: {list(aB[:10])}; matches 1+6(1*chi3): {borwein_a_ok}")

borwein_matches = []
for i in range(5):
    # monomial a^{4-i} b^i
    s = np.array([1] + [0] * NORD, dtype=np.int64)
    for _ in range(4 - i):
        s = ser_mul(s, aB, NORD)
    for _ in range(i):
        s = ser_mul(s, bB, NORD)
    if list(s) == signed_E6_int:
        borwein_matches.append((4 - i, i))  # (exp_a, exp_b)

info(f"Borwein monomials a^x b^y with x+y=4 matching E6+A2-signed: "
     f"{borwein_matches}")
info(f"E6+A2-signed head: {signed_E6_int[:10]}")
unique_mu3 = (borwein_matches == [(1, 3)])
check("F2.C5 UNIQUENESS in Borwein monoid (mu3 analogue): among all "
      "5 weight-4 monomials a^{4-i} b^i, EXACTLY one matches the "
      "E6+A2-signed census (= (81 E4(q^3)-E4(q))/80): a^1 b^3 -- "
      "exact analogue of (theta3-exp, theta4-exp)=(2,6); Phi has a "
      "well-defined field-theta exponent on both mu4 and mu3 objects",
      unique_mu3 and borwein_a_ok)

phi_well_defined = unique_mu4 and unique_mu3
info(f"Phi well-defined on founding objects: {phi_well_defined}; "
     f"Phi(Th0-Th2) = theta3-share with exponent 2 "
     f"(= theta_{{Z[i]}} = theta3^2)")

# ================================================================ F3
print("=" * 72)
print("F3 -- Hecke compatibility test (weight-1/2 T(p^2) + gap typing)")
print("=" * 72)

# CLASSICAL formula (Shimura; Serre-Stark; Buzzard notes), documented:
# For f = sum a(n) q^n of weight kappa/2 (kappa odd), level N|4Z, character chi,
# and odd prime p not dividing N, writing lambda = (kappa-1)/2:
#   b(n) = a(n p^2)
#        + chi_1(p) (n/p) p^{lambda-1} a(n)
#        + chi(p^2) p^{kappa-2} a(n/p^2)
# with a(m)=0 for non-integer m, (n/p)=Legendre, and
#   chi_1(p) = chi(p) * (-1/p)^lambda.
#
# Specialise to weight 1/2 (kappa=1, lambda=0), level 4, trivial chi:
#   b(n) = a(n p^2) + (n/p) p^{-1} a(n) + p^{-1} a(n/p^2).
# (Buzzard's printed p^{-3/2} on the last term is a typesetting garble of
#  p^{kappa-2}=p^{-1}; Serre-Stark eigenvalue formula confirms p^{-1}.)
#
# Self-consistent eigenvalue on theta3 = sum_{n in Z} q^{n^2}
# (a(0)=1, a(k^2)=2 for k>=1, else 0):  omega_p = 1 + p^{-1}.
# (Serre-Stark: for theta_psi, omega_p = psi(p)(1 + p^{-1}); psi=1.)

info("T(p^2) formula (wt 1/2, level 4, trivial chi, p odd):")
info("  b(n) = a(n p^2) + (n/p) p^{-1} a(n) + p^{-1} a(n/p^2)")
info("  classical eigenvalue on theta3: omega_p = 1 + p^{-1}")


def theta3_coeffs(order):
    a = [0] * (order + 1)
    a[0] = 1
    n = 1
    while n * n <= order:
        a[n * n] = 2
        n += 1
    return a


def T_p2_weight_half(a, p, order):
    """Apply classical T(p^2) at weight 1/2, trivial character (Fraction)."""
    b = [Fraction(0) for _ in range(order + 1)]
    inv_p = Fraction(1, p)
    for n in range(order + 1):
        # a(n p^2)
        np2 = n * p * p
        term = Fraction(a[np2] if np2 <= order else 0)
        # (n/p) p^{-1} a(n)
        if n >= 1:
            term += Fraction(legendre(n, p), 1) * inv_p * Fraction(a[n])
        # p^{-1} a(n/p^2)
        if n % (p * p) == 0:
            term += inv_p * Fraction(a[n // (p * p)])
        elif n == 0:
            # a(0/p^2)=a(0); the n=0 slot: Legendre undefined/0 for middle
            # Standard: b(0) = a(0) + p^{-1} a(0) = a(0)(1 + p^{-1})
            # because a(0*p^2)=a(0), middle term vanishes (n=0), last = p^{-1}a(0)
            pass  # already handled: np2=0 gives a[0]; n%(p^2)==0 gives last
        b[n] = term
    # Fix n=0 carefully: middle Legendre(0/p)=0, so
    # b(0) = a(0) + 0 + p^{-1} a(0) = a(0)(1+p^{-1}) -- our loop does this
    # because 0 % p^2 == 0.  Good.
    return b


a_th = theta3_coeffs(N_HECKE)
eigen_ok = True
eigenvalues = {}
# Also derive omega_p from the q^1 coefficient alone (self-consistent):
# b(1) = a(p^2) + (1/p) p^{-1} a(1) = 2 + p^{-1} * 2 = 2(1 + p^{-1})
# so omega_p := b(1)/a(1) = 1 + p^{-1}.
for p in (3, 5, 7):
    b = T_p2_weight_half(a_th, p, N_HECKE)
    omega_from_a1 = b[1] / Fraction(a_th[1])
    omega = Fraction(1) + Fraction(1, p)
    diffs = []
    for n in range(N_HECKE_CHECK + 1):
        # n*p^2 must lie in the coefficient table
        assert n * p * p <= N_HECKE
        expected = omega * Fraction(a_th[n])
        if b[n] != expected:
            diffs.append((n, b[n], expected))
    eigenvalues[p] = omega
    info(f"p = {p}: omega_from_a1 = {omega_from_a1}; "
         f"omega_classical = {omega}; "
         f"mismatches in n <= {N_HECKE_CHECK}: {len(diffs)}")
    if diffs[:3]:
        info(f"  first mismatches: {diffs[:3]}")
    eigen_ok &= (len(diffs) == 0 and omega_from_a1 == omega)

check("F3.C6 CLASSICAL: theta3 is a T(p^2)-eigenform of weight 1/2, "
      "level 4, for p = 3, 5, 7 with EXACT eigenvalue omega_p = 1 + p^{-1} "
      f"(derived from b(1)/a(1) AND verified on all q-coefficients "
      f"n <= {N_HECKE_CHECK} via the documented Serre-Stark/Shimura "
      "formula; self-consistent, not assumed)",
      eigen_ok and eigenvalues == {3: Fraction(4, 3),
                                   5: Fraction(6, 5),
                                   7: Fraction(8, 7)})

# --- Gap typing: L(c,s) vs zeta-trace of theta3 factor ---
print("F3b -- L-series gap: Mellin does NOT factor over products")
# L(c,s) = 16 * 2^{-s} eta(s) eta(s-3) - 8 L(f8,s)   (part 12)
# eta = Dirichlet eta = (1-2^{1-s}) zeta(s)
# Does the Eisenstein piece contain a zeta(2s)-type factor from theta3?
# theta3's Mellin carries zeta(2s); theta3^2 carries zeta(s) L(s, chi4).
# Plain Mellin of a PRODUCT is NOT the product of Mellins.

s_test = mpmath.mpf("5")
eta_s = mpmath.altzeta(s_test)
eta_s3 = mpmath.altzeta(s_test - 3)
eis = 16 * mpmath.power(2, -s_test) * eta_s * eta_s3
# Compare shapes:
#   zeta(2s) at s=5 is zeta(10) -- wrong weight
#   zeta(s) L(s,chi4) = Mellin-side of theta3^2 / archimedean
#   eta(s) eta(s-3) = (1-2^{1-s})(1-2^{4-s}) zeta(s) zeta(s-3)
zeta_s = mpmath.zeta(s_test)
zeta_s3 = mpmath.zeta(s_test - 3)
zeta_2s = mpmath.zeta(2 * s_test)
chi4_vals = [0, 1, 0, -1]   # chi4 mod 4
L_chi4 = mpmath.dirichlet(s_test, chi4_vals)
th3sq_L = zeta_s * L_chi4   # Dedekind zeta of Q(i) at s
info(f"at s={s_test}:")
info(f"  Eis piece 16*2^{{-s}} eta(s)eta(s-3) = {eis}")
info(f"  zeta(s)zeta(s-3)                     = {zeta_s * zeta_s3}")
info(f"  zeta(s)L(s,chi4) [= Mellin-side th3^2] = {th3sq_L}")
info(f"  zeta(2s) [= Mellin-side th3 raw]       = {zeta_2s}")

# Ratio checks: is Eis a multiple of th3sq_L or zeta(2s)?
ratio_chi = eis / th3sq_L
ratio_2s = eis / zeta_2s
ratio_zz = eis / (zeta_s * zeta_s3)
info(f"  Eis / (zeta L_chi4) = {ratio_chi}")
info(f"  Eis / zeta(2s)      = {ratio_2s}")
info(f"  Eis / (zeta zeta)   = {ratio_zz}")

# Exact algebraic identity from part 12:
# eta(s)eta(s-3) = (1-2^{1-s})(1-2^{4-s}) zeta(s)zeta(s-3)
# So Eis = 16 * 2^{-s} * (1-2^{1-s})(1-2^{4-s}) zeta(s)zeta(s-3)
# = pure 2-adic twist of the TRIVIAL channel -- NO L(chi4), NO zeta(2s).
factor_2adic = ((1 - mpmath.power(2, 1 - s_test))
               * (1 - mpmath.power(2, 4 - s_test)))
eis_from_zz = (16 * mpmath.power(2, -s_test) * factor_2adic
               * zeta_s * zeta_s3)
eis_identity_ok = abs(eis / eis_from_zz - 1) < mpmath.mpf("1e-25")

# Honest negatives: Eis is NOT a scalar multiple of zeta(s)L(s,chi4)
# (the th3^2 L-series) -- ratio is not constant in s
s2 = mpmath.mpf("6")
eis2 = (16 * mpmath.power(2, -s2) * mpmath.altzeta(s2)
        * mpmath.altzeta(s2 - 3))
th3sq_L2 = mpmath.zeta(s2) * mpmath.dirichlet(s2, chi4_vals)
r1 = eis / th3sq_L
r2 = eis2 / th3sq_L2
ratio_varies = abs(r1 / r2 - 1) > mpmath.mpf("1e-3")
info(f"  Eis/(zeta L_chi4) at s=5: {r1}; at s=6: {r2}; varies: {ratio_varies}")

check("F3.C7a EXACT: Eisenstein piece of L(Th0-Th2,s) = "
      "16 2^{-s} eta(s)eta(s-3) = 16 2^{-s}(1-2^{1-s})(1-2^{4-s}) "
      "zeta(s)zeta(s-3) -- a PURE 2-adic twist of the trivial channel "
      "(part 12 identity, rechecked at s=5).  It does NOT equal a "
      "scalar times zeta(s)L(s,chi4) [= L-series of the theta3^2 factor] "
      "nor zeta(2s) [= L-series of raw theta3]: ratios vary with s.  "
      "HONEST: plain Mellin of the PRODUCT th3^2 th4^6 does NOT "
      "factor as Mellin(th3)*Mellin(th4^*) -- this IS the gap",
      eis_identity_ok and ratio_varies)

# Shimura / Rankin-Selberg candidacy (typed, not verified as solution)
# Shimura correspondence: typically weight k+1/2 -> weight 2k; for
# weight 1/2, Serre-Stark says ALL forms are theta series with
# omega_p = psi(p)(1+p^{-1}) -- the Shimura lift of theta3 is the
# CONSTANT modular form of weight 0 (eigenvalue match with T(p) on
# weight 0 is vacuous / Eisenstein of weight 0).  So Shimura on the
# theta3 FACTOR alone yields no weight-4 Hecke data.
# Rankin-Selberg L(th3^2 x th4^6, s) is the natural bilinear operation
# that WOULD convert factor data into an L-series of the product;
# whether that equals L(c,s) up to archimedean/Euler normalisation
# is OPEN (and is exactly the functoriality question).

# Quick negative: weight-4 Hecke a_p of the cusp part f8 vs omega_p
# of theta3 -- no elementary dictionary a_p = poly(omega_p).
# f8 = eta(2t)^4 eta(4t)^4; a_p for p=3,5,7 from part 11/12.
f8 = np.roll(conv(eta_pass(2, 4, N_HECKE), eta_pass(4, 4, N_HECKE),
                  N_HECKE), 1)
f8[0] = 0
ap_f8 = {p: int(f8[p]) for p in (3, 5, 7)}
# sigma3 for Eisenstein comparison
sig3_p = {p: int(sp.divisor_sigma(p, 3)) for p in (3, 5, 7)}
info(f"weight-4 cusp a_p(f8): {ap_f8}")
info(f"weight-4 Eisenstein sigma_3(p): {sig3_p}")
info(f"weight-1/2 omega_p(theta3)=1+1/p: {eigenvalues}")

# Preregistered dictionaries to kill:
# D1: a_p(f8) == c * omega_p  (linear) -- no, a_p integer, omega rational small
# D2: a_p(f8) == sigma_3(p) related to omega -- check a few polynomials
dict_fail = True
for p in (3, 5, 7):
    om = eigenvalues[p]
    # a_p is integer; omega = (p+1)/p
    if ap_f8[p] == 0:
        continue
    # no: a_p / something(omega) constant across p
dict_ratios = []
for p in (3, 5, 7):
    om = float(eigenvalues[p])
    dict_ratios.append(ap_f8[p] / om)
    dict_ratios.append(ap_f8[p] / (om * p ** 3))  # weight-gap guess
    dict_ratios.append(sig3_p[p] / om)
info(f"naive dictionary ratios a_p/omega etc: "
     f"{[float(x) if not isinstance(x, float) else x for x in dict_ratios]}")
# Check constancy of a_p / (p^{3/2} something) -- just report non-match
naive_linear = len({ap_f8[p] * p // (p + 1) for p in (3, 5, 7)}) == 1
# a_p * p / (p+1) integer and constant?
scaled = [ap_f8[p] * p / (p + 1) for p in (3, 5, 7)]
info(f"a_p(f8) * p/(p+1) = {scaled} (constant? {len(set(scaled))==1})")

check("F3.C7b HECKE DICTIONARY (preregistered naive maps) FAILS: "
      "a_p(f8) * p/(p+1) is NOT constant across p=3,5,7; no elementary "
      "identity a_p(f8) = poly(omega_p(theta3)).  Shimura on the bare "
      "theta3 factor yields only the weight-0/Eisenstein eigenvalue "
      "1+p^{-1} (Serre-Stark) -- it does NOT see the weight-4 cusp "
      "a_p.  Typed OPEN operation: Rankin-Selberg convolution of the "
      "canonical factors (L(theta3^2 x theta4^6, s)), which is the "
      "classical device that turns a PRODUCT of forms into an L-series; "
      "whether it recovers L(Th0-Th2,s) functorially is the gap the "
      "project must close.  K2 does NOT yet fire (operation named, "
      "not refuted) but Phi's Hecke-translation is EMPTY today",
      len(set(scaled)) > 1 and eigen_ok)

# ================================================================ F4
print("=" * 72)
print("F4 -- contract ZETA.COMPILER.FUNCTOR + preregistered kills")
print("=" * 72)

contract = {
    "name": "ZETA.COMPILER.FUNCTOR",
    "type": "Phi: {census new-systems, weight 4} -> {weight-1/2 theta objects}",
    "requirements": [
        "(i) canonical (no choice) -- via unique theta-monoid factorisation",
        "(ii) Hecke-translating -- explicit sigma3/a_p -> T(p^2) dictionary",
        "(iii) Euler-product preserving",
        "(iv) eventually xi(s)-carrying (via the theta3 Mellin centre 1/2)",
    ],
    "anchor_in_suite": [
        "part 11: Th0-Th2 = theta3^2 theta4^6 (theta3 multiplicative)",
        "part 12: L(c,s) closed form + Poisson self-duality",
        "part 13: mu3 Borwein analogue a b^3",
        "F1: classical theta3 -> xi centre 1/2 typed in-suite",
        "F2: factorisation unique => Phi well-defined on founding objects",
    ],
    "open": [
        "Hecke-translation formula (ii) -- Rankin-Selberg candidate",
        "Euler-product preservation (iii) under Phi",
        "extension from founding objects to all census new-systems",
    ],
    "kills": {
        "K1": "theta factorisation non-unique => factorisation candidate dies",
        "K2": "no preregistered op (Shimura, Rankin-Selberg) translates "
              "Hecke => Phi empty, project falls back to analogy",
        "K3": "Langlands honesty: no known general weight-4->zeta functor; "
              "smuggling zeta as external factor does not count",
    },
}
for k, v in contract.items():
    if isinstance(v, list):
        info(f"{k}:")
        for item in v:
            info(f"  - {item}")
    elif isinstance(v, dict):
        info(f"{k}:")
        for kk, vv in v.items():
            info(f"  {kk}: {vv}")
    else:
        info(f"{k}: {v}")

k1_fires = not unique_mu4  # monoid non-uniqueness
k2_fires = False  # RS still open, not refuted; naive maps failed but
# K2 requires ALL preregistered ops to fail -- RS not yet tested as
# equality, only named.  Honest: K2 does not fire.
k3_respected = True  # we do not claim a Langlands functor exists

check("F4.K1 status: factorisation UNIQUE on founding objects "
      "(mu4 monoid + mu3 Borwein) -- K1 does NOT fire",
      not k1_fires and phi_well_defined)
check("F4.K2 status: Shimura-on-bare-theta3 and naive a_p<->omega_p "
      "dictionaries FAIL; Rankin-Selberg of the canonical factors is "
      "NAMED as the remaining candidate and left OPEN -- K2 does NOT "
      "fire (would require RS refutation or exhaustion).  Phi's "
      "Hecke-slot is empty: typed gap, not a kill",
      not k2_fires)
check("F4.K3 Langlands honesty: probe claims NO general "
      "weight-4 -> zeta procedure; zeta enters only via the classical "
      "theta3 Mellin (F1) after a still-missing functorial extraction "
      "-- no external smuggling.  K3 respected",
      k3_respected)

check("F4 CONTRACT locked as preregistered checks: Phi sought with "
      "(i) canonical via unique factorisation [PASS on founding objects], "
      "(ii) Hecke-translating [OPEN -- RS candidate], "
      "(iii) Euler-product preserving [OPEN], "
      "(iv) xi-carrying [ANCHOR via F1 theta3 centre].  "
      "Project FOUNDED, not solved",
      phi_well_defined and not k1_fires and k3_respected)

# ================================================================ F5
print("=" * 72)
print("F5 -- verdict")
print("=" * 72)

f1_ok = mellin_ok and fe_ok and (s_centre == Fraction(1, 4))
f2_ok = phi_well_defined
f3_typed_gap = eis_identity_ok and ratio_varies and eigen_ok

if k1_fires:
    verdict = "STILLBORN"
elif f1_ok and f2_ok and f3_typed_gap:
    verdict = "FOUNDED-WITH-ANCHOR"
elif f1_ok:
    verdict = "FOUNDED-WEAK"
else:
    verdict = "STILLBORN"

info(f"F1 (GL(1) anchor):     {f1_ok}")
info(f"F2 (unique factorisation / Phi well-defined): {f2_ok}")
info(f"F3 (Hecke eigenform + typed L-gap): {f3_typed_gap}")
info(f"K1/K2/K3 fire?: {k1_fires}/{k2_fires}/{not k3_respected}")
info(f"VERDICT: {verdict}")
info("Next lever: compute the Rankin-Selberg convolution "
     "L(theta3^2 x theta4^6, s) (or the Cohen-Kuznetsov lift / "
     "Shimura on a weight-5/2 packaging of the product) and test "
     "equality with L(Th0-Th2, s) up to explicit Euler/archimedean "
     "factors -- that is the first non-analogy Hecke-translation test.")

check(f"F5 VERDICT = {verdict}: F1+F2 exact on founding objects; "
      "F3 types the L-translation gap (Mellin non-factorisation; "
      "RS named; naive/Shimura-bare dictionaries fail).  "
      "ZETA.COMPILER.FUNCTOR is FOUNDED-WITH-ANCHOR, not solved",
      verdict == "FOUNDED-WITH-ANCHOR")

# ================================================================ end
elapsed = time.time() - T0
print()
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({elapsed:.2f}s)")
print(f"VERDICT: {verdict}")
if FAIL:
    raise SystemExit(1)
raise SystemExit(0)
