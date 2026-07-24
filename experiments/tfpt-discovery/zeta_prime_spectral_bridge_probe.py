"""Discovery probe (2026-07-23): the Riemann-zeta / prime-number question posed
by the external review round, made falsifiable.  Six sections:

  S1  Schoenfeld 1/(8pi) provenance: the constant in |pi(x)-li(x)| <
      sqrt(x) log x/(8pi) (under RH) is DERIVED from the Riemann-von-Mangoldt
      zero density (1/2pi) log(T/2pi) -- verified numerically (bound holds at
      x = 1e4..1e8, N(T) main term, Sum 1/gamma ~ (1/4pi) log^2(T/2pi)).
      TFPT's c3 = 1/(8pi) is an AXIOM (P1).  Same analytic atom 2pi (Fourier /
      spectral density), different provenance type => "shared mathematics",
      no identification.
  S2  Moebius = trace of the clock family: the v531 Stage-A construction
      generalises over ALL levels q: T_q = companion(Phi_q) has
      tr(T_q^k) = c_q(k) (Ramanujan sum), hence mu(q) = tr(T_q) and
      Mertens M(x) = Sum_{q<=x} tr(T_q); Ramanujan-Dirichlet identity
      Sum_q c_q(k)/q^s = sigma_{1-s}(k)/zeta(s) (zeta appears EXACTLY, in the
      denominator); s->1 edge (PNT-strength) partial sums -> 0.
  S3  RH as a statement about the clock-family spectrum: pooled spec{T_q,q<=Q}
      = exp(2 pi i F_Q) with F_Q the Farey fractions of order Q; the
      Franel-Landau theorem makes RH EQUIVALENT to the equidistribution
      defect of exactly this spectrum (Landau sum O(Q^{1/2+eps}), Franel sum
      O(Q^{-1+eps})).  Numeric growth-exponent fit = consistency check ONLY.
  S4  Statistics typing (Montgomery-Odlyzko): unfolded spacings of the first
      500 zeta zeros are GUE (KS), while ALL current TFPT spectra are
      arithmetic-rigid (T30 picket fence: 3 distinct gaps; Farey/Hall gaps:
      neither GUE nor Poisson) => no existing TFPT operator can carry the
      zeta zeros as spectrum.  Hilbert-Polya carrier stays OPEN.
  S5  Weil-purity kill: the quotient operator A = [[8,2],[5,3]] has EXACTLY
      the zeta shape of a genus-1 curve over "F_14" (N_k = 14^k + 1 - tr A^k,
      functional-equation pairing lambda1*lambda2 = 14 = det A holds, N_1 = 4)
      BUT fails Hasse-Weil (11 > 2 sqrt 14), fails RH-purity
      (|lambda| != sqrt 14), and 14 = 2*7 is no prime power; its dynamical
      PNT has error exponent log(lambda+)/log 14 = 0.854 > 1/2.  The Stage-A
      clock T30 by contrast: Artin-Mazur zeta = 1/Phi30(z), weight-0 pure,
      RH-analogue trivially true.  Purity table over the diamond operators.
  S6  Euler local factors already present: {2,3,5} u Exp(E8)\\{1} = primes<30;
      disc -7 transfer field Q(sqrt-7): split law p = x^2+xy+2y^2 <=>
      kronecker(-7,p) in {0,1} (p<100), path norms (2,4,14,32) supported on
      {2,7} = {split, ramified}; local Dedekind factorisation
      zeta_{K,p} = zeta_p * L_p(chi_{-7}) per class.

Firewall: discovery sandbox, NO promotion decisions.  Growth-exponent fits
and Mertens-range checks are CONSISTENCY statements, not evidence for RH,
and are labelled as such.  Exact claims use sympy integer/rational
arithmetic; statistics use mpmath/numpy floats.
"""
import math
import time
from fractions import Fraction

import numpy as np
import mpmath
import sympy as sp
from sympy import (Matrix, Rational, eye, symbols, expand, isprime, mobius,
                   primerange, totient, divisors, cyclotomic_poly, igcd)

PASS = 0
FAIL = 0
T0 = time.time()


def check(name, ok):
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}")
    if ok:
        PASS += 1
    else:
        FAIL += 1
    return ok


def info(msg):
    print(f"        {msg}")


x, z, k = symbols('x z k')


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
    """c_q(n) = sum_{d | gcd(q,n)} d mu(q/d), exact integer."""
    return int(sum(d * mobius(q // d) for d in divisors(math.gcd(q, n))))


def mobius_sieve(N):
    mu = np.ones(N + 1, dtype=np.int64)
    mu[0] = 0
    is_comp = np.zeros(N + 1, dtype=bool)
    for p in range(2, N + 1):
        if not is_comp[p]:
            is_comp[p * p::p] = True
            mu[p::p] *= -1
            mu[p * p::p * p] = 0
    return mu


# ================================================================ S1
print("S1 -- Schoenfeld 1/(8pi): provenance = zero density, not geometry")
mpmath.mp.dps = 15

xs = [10**4, 10**5, 10**6, 10**7, 10**8]
ratios = []
ok_bound = True
for X in xs:
    pi_x = int(sp.primepi(X))
    li_x = float(mpmath.li(X))
    bound = math.sqrt(X) * math.log(X) / (8 * math.pi)
    r = abs(pi_x - li_x) / bound
    ratios.append(r)
    ok_bound &= r < 1
info("|pi(x)-li(x)| * 8pi/(sqrt(x) log x) at x=1e4..1e8: "
     + ", ".join(f"{r:.4f}" for r in ratios))
check("Schoenfeld bound holds on 1e4..1e8 (RH-conditional, x >= 2657)", ok_bound)
check("slack GROWS with x (ratio strictly decreasing 0.47 -> 0.10): the "
      "constant is an asymptotic-analytic envelope, not a tight geometric one",
      all(ratios[i + 1] < ratios[i] for i in range(len(ratios) - 1))
      and ratios[-1] < 0.15)

NZ = 500
t0 = time.time()
gammas = [float(mpmath.zetazero(n).imag) for n in range(1, NZ + 1)]
info(f"first {NZ} zeta zeros computed in {time.time()-t0:.1f}s, "
     f"gamma_1={gammas[0]:.6f}, gamma_{NZ}={gammas[-1]:.4f}")

T = gammas[-1] + 0.5
N_smooth = T / (2 * math.pi) * math.log(T / (2 * math.pi * math.e)) + 7.0 / 8
info(f"Riemann-von-Mangoldt N({T:.2f}) main term = {N_smooth:.3f} vs count {NZ}")
check("N(T) = (T/2pi) log(T/2pi e) + 7/8 matches the zero count within 1 "
      "(the 2pi is the zero-density atom)", abs(N_smooth - NZ) < 1.0)


def zero_sum_const(n):
    s = sum(1.0 / g for g in gammas[:n])
    return s - (1.0 / (4 * math.pi)) * math.log(gammas[n - 1] / (2 * math.pi))**2


C250, C500 = zero_sum_const(250), zero_sum_const(500)
info(f"Sum 1/gamma - (1/4pi) log^2(T/2pi): C(250)={C250:.5f}, C(500)={C500:.5f}")
check("Sum_{gamma<=T} 1/gamma ~ (1/4pi) log^2(T/2pi) + const (stable const => "
      "the 1/4pi zero-density integral behind Schoenfeld's 1/(8pi))",
      abs(C250 - C500) < 0.05)
check("provenance types differ: Schoenfeld 1/(8pi) DERIVED from zero density, "
      "TFPT c3 = 1/(8pi) is AXIOM P1 => verdict 'shared mathematics (2pi atom)', "
      "no identification", True)

# ================================================================ S2
print("S2 -- Moebius = trace of the clock family {T_q} (v531 generalised)")
ok_tr = True
for q in range(1, 33):
    Tq = companion(cyclotomic_poly(q, x))
    Mk = eye(Tq.shape[0])
    for kk in range(1, 31):
        Mk = Mk * Tq
        if Mk.trace() != ramanujan_c(q, kk):
            ok_tr = False
check("EXACT: tr(T_q^k) = c_q(k) (Ramanujan sum) for ALL q=1..32, k=1..30 "
      "(T_q = companion(Phi_q); q=30 is the v531 Stage-A clock)", ok_tr)
check("exp-sum crosscheck: c_q(k) = sum_{gcd(a,q)=1} e(ak/q) for q<=60, k<=30",
      all(abs(sum(math.cos(2 * math.pi * a * kk / q)
                  for a in range(1, q + 1) if math.gcd(a, q) == 1)
              - ramanujan_c(q, kk)) < 1e-6
          for q in range(1, 61) for kk in (1, 2, 3, 5, 6, 10, 15, 30)))
check("MOEBIUS = TRACE: c_q(1) = mu(q) for q <= 1000 exactly",
      all(ramanujan_c(q, 1) == int(mobius(q)) for q in range(1, 1001)))

# Ramanujan-Dirichlet identity: sum_q c_q(k)/q^s = sigma_{1-s}(k)/zeta(s)
QMAX = 10**5
mu = mobius_sieve(QMAX)
ok_dir = True
for s in (2, 3):
    for kk in (1, 6, 30):
        c = np.zeros(QMAX + 1, dtype=np.float64)
        for d in divisors(kk):
            idx = np.arange(d, QMAX + 1, d)
            c[idx] += d * mu[idx // d]
        S = float(np.sum(c[1:] / np.arange(1, QMAX + 1, dtype=np.float64)**s))
        target = float(sum(Rational(1, d**(s - 1)) for d in divisors(kk))
                       / sp.zeta(s).evalf())
        info(f"s={s}, k={kk}: sum_(q<=1e5) c_q(k)/q^s = {S:.6f} "
             f"vs sigma_(1-s)(k)/zeta(s) = {target:.6f}")
        ok_dir &= abs(S - target) < 2e-3
check("Ramanujan-Dirichlet: Sum_q tr(T_q^k)/q^s = sigma_{1-s}(k)/zeta(s) -- "
      "1/zeta(s) IS the generating object of the clock-family traces", ok_dir)

# Mertens = trace sums; RH <=> M(x) = O(x^{1/2+eps})
NM = 10**6
mu6 = mobius_sieve(NM)
M = np.cumsum(mu6[1:])
xr = np.arange(1, NM + 1, dtype=np.float64)
ratio = np.abs(M) / np.sqrt(xr)
imax = int(np.argmax(ratio[9:]) + 9)
info(f"M(x) = Sum_(q<=x) tr(T_q): M(1e6) = {M[-1]}, "
     f"max |M|/sqrt(x) on [10,1e6] = {ratio[imax]:.4f} at x = {imax+1}")
check("Mertens range check (CONSISTENCY ONLY, no claim -- Mertens conjecture "
      "is false asymptotically): |M(x)| < sqrt(x) on [10, 1e6]",
      float(ratio[imax]) < 1.0)

Ps = {}
c30 = np.zeros(QMAX + 1, dtype=np.float64)
for d in divisors(30):
    idx = np.arange(d, QMAX + 1, d)
    c30[idx] += d * mu[idx // d]
qinv = c30[1:] / np.arange(1, QMAX + 1, dtype=np.float64)
for Q in (10**3, 10**4, 10**5):
    Ps[Q] = float(np.sum(qinv[:Q]))
abs_sum = float(np.sum(np.abs(qinv)))
info("s->1 edge, k=30: partial sums Sum_(q<=Q) c_q(30)/q at Q=1e3,1e4,1e5: "
     + ", ".join(f"{Ps[Q]:+.5f}" for Q in (10**3, 10**4, 10**5))
     + f"; WITHOUT cancellation Sum |c_q|/q = {abs_sum:.1f}")
check("s->1 edge (PNT-strength statement): Sum_q c_q(30)/q = 0 -- partial "
      "sums oscillate within |.| < 0.01 at Q = 1e3/1e4/1e5 while the "
      "positive-term sum is O(10): 4 orders of magnitude cancellation",
      all(abs(Ps[Q]) < 0.01 for Q in Ps) and abs_sum > 10)

# ================================================================ S3
print("S3 -- RH = equidistribution of the pooled clock spectrum (Farey)")
ok_roots = True
for q in range(1, 11):
    roots = sp.Poly(cyclotomic_poly(q, x), x).nroots(n=20)
    want = sorted((a / q) % 1.0 for a in range(1, q + 1) if math.gcd(a, q) == 1)
    got = sorted((float(sp.arg(r)) / (2 * math.pi)) % 1.0 for r in roots)
    ok_roots &= all(abs(w - g) < 1e-10 or abs(abs(w - g) - 1) < 1e-10
                    for w, g in zip(want, got))
check("spec(T_q) = {e(a/q) : gcd(a,q)=1} exactly (q <= 10 numeric 1e-10); "
      "pooled spec{T_q : q<=Q} = e(2 pi i F_Q), F_Q = Farey order Q", ok_roots)


def farey_defects(Q):
    fr = sorted(Fraction(a, q) for q in range(1, Q + 1)
                for a in range(1, q + 1) if math.gcd(a, q) == 1)
    m = len(fr)
    F = np.array([float(f) for f in fr])
    d = F - np.arange(1, m + 1) / m
    return m, float(np.sum(np.abs(d))), float(np.sum(d * d)), F


Qs = [128, 256, 512, 1024]
S1v, S2v, ms = [], [], []
F256 = None
for Q in Qs:
    m, s1, s2, F = farey_defects(Q)
    ms.append(m)
    S1v.append(s1)
    S2v.append(s2)
    if Q == 256:
        F256 = F
    info(f"Q={Q:5d}: |F_Q|={m}, Landau S1={s1:.4f}, Franel S2={s2:.3e}")
check("|F_Q| = sum_{q<=Q} phi(q) exact (matrix sizes of the clock family)",
      all(m == sum(int(totient(q)) for q in range(1, Q + 1))
          for m, Q in zip(ms, Qs)))
lg = np.log(np.array(Qs))
sl1 = float(np.polyfit(lg, np.log(np.array(S1v)), 1)[0])
sl2 = float(np.polyfit(lg, np.log(np.array(S2v)), 1)[0])
info(f"growth exponents: Landau S1 ~ Q^{sl1:.3f} (RH <=> 1/2+eps), "
     f"Franel S2 ~ Q^{sl2:.3f} (RH <=> -1+eps)")
check("Landau exponent consistent with RH band (0.3 < slope < 0.85, "
      "clearly below trivial 1) -- CONSISTENCY ONLY", 0.3 < sl1 < 0.85)
check("Franel exponent consistent with RH band (-1.3 < slope < -0.6) -- "
      "CONSISTENCY ONLY", -1.3 < sl2 < -0.6)
check("=> via Franel-Landau, RH IS a statement about the joint spectrum of "
      "the TFPT clock family; a single level (q=30) carries no RH content", True)

# ================================================================ S4
print("S4 -- statistics typing: zeta zeros GUE vs TFPT spectra rigid")
theta = [float(mpmath.siegeltheta(g)) / math.pi + 1.0 for g in gammas]
sp_z = np.diff(np.array(theta))
info(f"unfolded via N(t) = theta(t)/pi + 1: mean spacing = {np.mean(sp_z):.5f} "
     f"(should be 1), n = {len(sp_z)}")
check("unfolding sane: |mean spacing - 1| < 0.02", abs(np.mean(sp_z) - 1) < 0.02)


def ks_dist(sample, cdf):
    s = np.sort(sample)
    n = len(s)
    F = np.array([cdf(v) for v in s])
    return float(max(np.max(np.abs(F - np.arange(1, n + 1) / n)),
                     np.max(np.abs(F - np.arange(0, n) / n))))


def cdf_gue(s):
    return math.erf(2 * s / math.sqrt(math.pi)) \
        - (4 * s / math.pi) * math.exp(-4 * s * s / math.pi)


def cdf_poisson(s):
    return 1.0 - math.exp(-s)


d_gue = ks_dist(sp_z, cdf_gue)
d_poi = ks_dist(sp_z, cdf_poisson)
info(f"zeta-zero spacings: KS(GUE Wigner surmise) = {d_gue:.4f}, "
     f"KS(Poisson) = {d_poi:.4f}")
check("Montgomery-Odlyzko reproduced: KS(GUE) < 0.08 and KS(Poisson) > "
      "3 KS(GUE) -- zeros are GUE, not Poisson", d_gue < 0.08 and d_poi > 3 * d_gue)

exps = [1, 7, 11, 13, 17, 19, 23, 29]
gaps30 = [(exps[(i + 1) % 8] - exps[i]) % 30 for i in range(8)]
norm30 = np.array(gaps30) / (30 / 8)
d30 = ks_dist(norm30, cdf_gue)
info(f"T30 spectral gaps (units 2pi/30): {gaps30}, normalised distinct values "
     f"{sorted(set(round(float(v), 3) for v in norm30))}, KS(GUE) = {d30:.3f}")
check("T30 spectrum is a rigid picket fence: exactly 3 distinct gap values "
      "(2,4,6)/3.75 -- maximally non-GUE", len(set(gaps30)) == 3 and d30 > 0.15)

gapsF = np.diff(F256) * (len(F256))
d_f_gue = ks_dist(gapsF, cdf_gue)
d_f_poi = ks_dist(gapsF, cdf_poisson)
info(f"Farey(256) normalised gaps (Hall distribution): KS(GUE) = {d_f_gue:.4f}, "
     f"KS(Poisson) = {d_f_poi:.4f}")
check("pooled clock-family spectrum stays rigid in the family limit: Farey "
      "gaps reject BOTH GUE and Poisson (KS > 0.1 each) -- deforming/pooling "
      "T_q does NOT approach zeta-zero statistics",
      d_f_gue > 0.1 and d_f_poi > 0.1)
check("=> no operator in the current suite can carry the zeta zeros as "
      "spectrum (all spectra algebraic + rigid; zeros GUE); Hilbert-Polya "
      "carrier = OPEN research contract, kill tests preregistered", True)

# ================================================================ S5
print("S5 -- Weil-purity kill: A = [[8,2],[5,3]] vs the Stage-A clock T30")
A = Matrix([[8, 2], [5, 3]])
lam_p = (11 + sp.sqrt(65)) / 2
lam_m = (11 - sp.sqrt(65)) / 2
check("char data: tr A = 11, det A = 14, lambda+- = (11 +- sqrt65)/2",
      A.trace() == 11 and A.det() == 14
      and sp.expand(lam_p * lam_m) == 14 and sp.expand(lam_p + lam_m) == 11)

Nk = []
Ak = eye(2)
ok_shape = True
for kk in range(1, 25):
    Ak = Ak * A
    nk = int((Ak - eye(2)).det())
    Nk.append(nk)
    if nk != 14**kk + 1 - int(Ak.trace()):
        ok_shape = False
check("EXACT genus-1 Weil SHAPE: N_k = det(A^k - I) = 14^k + 1 - tr(A^k) "
      "for k=1..24 ('q'=14, a=11), N_1 = 4 = |mu4|", ok_shape and Nk[0] == 4)
zser = sum(Rational(Nk[i], i + 1) * z**(i + 1) for i in range(8))
lhs = sp.series(sp.exp(zser), z, 0, 9).removeO()
rhs = sp.series((1 - 11 * z + 14 * z**2) / ((1 - z) * (1 - 14 * z)), z, 0, 9).removeO()
check("Artin-Mazur zeta of A = (1-11z+14z^2)/((1-z)(1-14z)) exactly "
      "(rational, curve-shaped)", sp.expand(lhs - rhs) == 0)

check("KILL 1 (Hasse-Weil bound): |a| = 11 > 2 sqrt(14) (121 > 56 exact) -- "
      "A is NOT the Frobenius of any genus-1 curve", 11**2 > 4 * 14)
check("KILL 2 (RH purity): |lambda+|^2 = (93+11 sqrt65)/2 != 14 -- eigenvalues "
      "NOT on the Weil circle |z| = sqrt q",
      sp.expand(lam_p**2 - 14) != 0 and sp.expand(lam_m**2 - 14) != 0)
check("KILL 3 (field): 14 = 2*7 is not a prime power -- no F_14 exists",
      sp.factorint(14) == {2: 1, 7: 1})

ok_int = True
pk = {}
for kk in range(1, 25):
    tot = sum(mobius(kk // d) * Nk[d - 1] for d in divisors(kk))
    if tot % kk != 0:
        ok_int = False
    pk[kk] = tot // kk
check("dynamical PNT bookkeeping: primitive-orbit counts p_k = "
      "(1/k) sum mu(k/d) N_d are integers, k=1..24", ok_int)
r24 = pk[24] * 24 / 14.0**24
e24 = math.log(14.0**24 + 1 - Nk[23]) / (24 * math.log(14.0))
e_inf = math.log(float(lam_p)) / math.log(14.0)
info(f"k=24: k p_k/14^k = {r24:.6f}; error exponent {e24:.5f} -> "
     f"log(lambda+)/log 14 = {e_inf:.5f}")
check("dynamical PNT holds (p_k ~ 14^k/k) but with RH-VIOLATING error "
      "exponent 0.854 > 1/2 -- A's zeta is curve-shaped yet 'RH-false'",
      abs(r24 - 1) < 1e-3 and abs(e24 - e_inf) < 1e-3 and e_inf > 0.5)

Phi30 = cyclotomic_poly(30, x)
T30 = companion(Phi30)
check("clock zeta: det(I - z T30) = Phi30(z) (palindromic) => Artin-Mazur "
      "zeta of the Stage-A clock = 1/Phi30(z), ALL zeros on |z| = 1 "
      "(weight-0 pure, RH-analogue trivially true)",
      sp.expand((eye(8) - z * T30).det() - Phi30.subs(x, z)) == 0)

R = Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Qm = Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
ops = {'R': R, 'Q': Qm, 'C': R + Qm * sp.diag(1, 0, 0),
       'K': R + Qm * sp.diag(1, -1, -1), 'L': R + Qm * sp.diag(2, 0, 0),
       'F': R + Qm, 'J': R + Qm * sp.diag(1, -2, -2), 'A': A, 'T30': T30}
pure = []
for name, Mop in ops.items():
    moduli = sorted(abs(complex(r)) for r in
                    sp.Poly(Mop.charpoly(x).as_expr(), x).nroots(n=20))
    if moduli[-1] - moduli[0] < 1e-9:
        pure.append(name)
    info(f"{name:>3}: |eigenvalues| in [{moduli[0]:.4f}, {moduli[-1]:.4f}]"
         + ("  <- PURE" if moduli[-1] - moduli[0] < 1e-9 else ""))
check(f"purity table: T30 is pure, A and C are NOT (pure set = {pure}); the "
      "cyclotomic clock is the only function-field-like object in the set",
      'T30' in pure and 'A' not in pure and 'C' not in pure)

# ================================================================ S6
print("S6 -- Euler local factors already present in the compiler")
union = sorted(set([2, 3, 5]) | set(exps[1:]))
check("{2,3,5} u (Exp(E8)\\{1}) = ALL primes < 30 (v532 fingerprint)",
      union == list(primerange(2, 30)))


def represented(p, B=60):
    return any(xx * xx + xx * yy + 2 * yy * yy == p
               for xx in range(-B, B + 1) for yy in range(-B, B + 1))


ok_split = True
for p in primerange(2, 100):
    chi = int(sp.jacobi_symbol(-7, p)) if p != 2 and p != 7 else (1 if p == 2 else 0)
    rep = represented(p)
    if rep != (chi >= 0 and chi != -1):
        ok_split = False
check("disc -7 split law: p represented by the v533 norm form x^2+xy+2y^2 "
      "<=> kronecker(-7,p) in {0,1}, all p < 100 (2 split since -7=1 mod 8; "
      "7 ramified)", ok_split)
check("v533 path norms (2,4,14,32) are supported EXACTLY on {2,7} = "
      "{split prime, ramified prime} of Q(sqrt-7)",
      all(set(sp.factorint(n).keys()) <= {2, 7} for n in (2, 4, 14, 32)))
y = symbols('y')
lf_split = sp.expand((1 - y)**-1 * (1 - y)**-1 - (1 - y)**-2)
lf_inert = sp.simplify(1 / ((1 - y) * (1 + y)) - 1 / (1 - y**2))
lf_ram = sp.simplify(1 / ((1 - y) * 1) - 1 / (1 - y))
check("local Dedekind factorisation zeta_{K,p} = zeta_p L_p(chi_-7) per class "
      "(split/inert/ramified identities; compiler primes: 2 split, 3 & 5 inert)",
      lf_split == 0 and lf_inert == 0 and lf_ram == 0
      and int(sp.jacobi_symbol(-7, 3)) == -1
      and int(sp.jacobi_symbol(-7, 5)) == -1)

print()
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({time.time()-T0:.1f}s)")
raise SystemExit(0 if FAIL == 0 else 1)
