"""Discovery probe (2026-07-24), part 35 of the zeta/prime investigation.
FIRST HECKE-TRANSLATION TEST of the contract ZETA.COMPILER.FUNCTOR
(part 34 founding): Rankin–Selberg convolution of the compiler factors.

Part 34 typed Phi(Th0-Th2) := theta3-share of the unique factorisation
    Th0 - Th2 = theta3^2 * theta4^6
and named Rankin–Selberg as the first candidate operation translating
factor data into L-data (gap F3: plain Mellin does not factor over
products; bare Shimura on theta3 does not see a_p).

  S1  Factor coefficients (classical):
        g := theta3^2  (weight 1): a_g(n) = r_2(n) = 4 sum_{d|n} chi_4(d);
            L-data {1, chi_4}  (essentially zeta_{Q(i)}).
        h := theta4^6  (weight 3): a_h(n) = (-1)^n r_6(n), with the
            classical Jacobi formula (verified on coefficients)
            r_6(n) = 16 sigma_2^sharp(n) - 4 sigma_2^flat(n),
            sigma_2^flat(n)  = sum_{d|n} chi_4(d) d^2,
            sigma_2^sharp(n) = sum_{d|n} chi_4(n/d) d^2
            (= Eis_{chi_4,1} and Eis_{1,chi_4} of weight 3).
  S2  R1 Euler product: a_g a_h suitably normalised is multiplicative;
      local factors at p <= 50 are rational of denominator degree <= 4
      (exact sympy reconstruction from coefficient power series).
  S3  R2 GL(1) factorisation: closed form of
      D(s) := sum_{n>=1} a_g(n) a_h(n) n^{-s}
      as an explicit 2-Euler numerator times
      zeta(s) L(s,chi_4) zeta(s-2) L(s-2,chi_4) / zeta(2s-2),
      derived from the degree-4 local factors (classical RS: the
      numerator 1-p^2 X^2 is the zeta(2s-2) normalisation).
      High-precision numerical check (mpmath, 30 dps).
  S4  R3 xi-honesty: shift table of the four GL(1) components under
      the weight normalisation s |-> s+(k_g+k_h-2)/2 = s+1; whether
      any lands on the centre-1/2 line.  No bending.
  S5  R4 relation to L(F,s) = 16*2^{-s} eta(s)eta(s-3) - 8 L(f8,s)
      (part 12): is a_p(f8) visible in the degree-4 locals of D?
      Expectation: NO — D is the Eisenstein RS shadow; cusp needs
      another bridge.
  S6  Verdict: RS-TRANSLATES-EISENSTEIN / PARTIAL / DEAD, and the
      precise consequence for ZETA.COMPILER.FUNCTOR.

PREREGISTERED CRITERIA
  R1  Multiplicativity of a_g*a_h on coprime pairs n,m <= 300
      (weak form c(nm)*c(1)=c(n)*c(m)); local Euler factors at
      p <= 50 have denom degree <= 4 (exact rational reconstruction).
  R2  Closed GL(1) product form identified from local factors and
      verified numerically at >= 3 points with >= 20 matching digits.
  R3  Shift table documented; honest yes/no on unshifted xi-centre
      after weight normalisation.
  R4  a_p(f8) visibility in D-locals typed (expected: invisible);
      D vs L(F,s) relationship typed (Eisenstein shadow vs cusp).
  K1  No Euler product / denom degree > 4 => RS candidate dead.
  K2  No identifiable GL(1) factorisation => translation empty.

Firewall: discovery sandbox, NO promotion, no marker moves, no RH
evidence language.  Classical theorems (Jacobi r_2/r_6, Rankin–
Selberg of Eisenstein series, Dirichlet L-functions of chi_4) named
as such — probe content is the in-suite translation test of the
functor contract founded in part 34.
"""
from __future__ import annotations

import time
from fractions import Fraction

import mpmath
import numpy as np
import sympy as sp

PASS = 0
FAIL = 0
T0 = time.time()
mpmath.mp.dps = 30

N_COEFF = 10000
N_MULT = 300
P_LOCAL_MAX = 50


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
    s = np.zeros(order + 1, dtype=object)
    s[0] = 1
    n = 1
    while n * n <= order:
        if kind == 3:
            s[n * n] = 2
        else:
            s[n * n] = 2 * ((-1) ** n)
        n += 1
    return s


def conv(a, b, order):
    out = np.zeros(order + 1, dtype=object)
    for i, ai in enumerate(a):
        if not ai:
            continue
        for j in range(min(len(b) - 1, order - i) + 1):
            if b[j]:
                out[i + j] += ai * b[j]
    return out


def ppow(a, e, order):
    out = np.zeros(order + 1, dtype=object)
    out[0] = 1
    for _ in range(e):
        out = conv(out, a, order)
    return out


def eta_pass(d, e, order):
    s = np.zeros(order + 1, dtype=np.int64)
    s[0] = 1
    for k in range(d, order + 1, d):
        for _ in range(e):
            s[k:] = s[k:] - s[:-k]
    return s


def chi4(n: int) -> int:
    r = n % 4
    if r == 1:
        return 1
    if r == 3:
        return -1
    return 0


def sigma2_flat(n: int) -> int:
    """sum_{d|n} chi_4(d) d^2  (= Eis_{1, chi_4} weight-3 coeff)."""
    return sum(chi4(d) * d * d for d in sp.divisors(n))


def sigma2_sharp(n: int) -> int:
    """sum_{d|n} chi_4(n/d) d^2  (= Eis_{chi_4, 1} weight-3 coeff)."""
    return sum(chi4(n // d) * d * d for d in sp.divisors(n))


def r6_classical(n: int) -> int:
    """Classical Jacobi: r_6(n) = 16 sigma_2^sharp(n) - 4 sigma_2^flat(n)."""
    return 16 * sigma2_sharp(n) - 4 * sigma2_flat(n)


def r2_classical(n: int) -> int:
    return 4 * sum(chi4(d) for d in sp.divisors(n))


# ================================================================ data
print("=" * 72)
print("S1 -- factor coefficients g = theta3^2, h = theta4^6")
print("=" * 72)

th3 = theta_arr(3, N_COEFF)
th4 = theta_arr(4, N_COEFF)
ag = ppow(th3, 2, N_COEFF)          # a_g = r_2
ah = ppow(th4, 6, N_COEFF)          # a_h = (-1)^n r_6
th3_6 = ppow(th3, 6, N_COEFF)       # r_6 via theta3^6

r2_ok = all(int(ag[n]) == r2_classical(n) for n in range(1, N_COEFF + 1))
r6_theta_ok = all(int(th3_6[n]) == r6_classical(n) for n in range(1, N_COEFF + 1))
ah_sign_ok = all(int(ah[n]) == ((-1) ** n) * int(th3_6[n])
                 for n in range(0, N_COEFF + 1))

info(f"a_g head: {[int(ag[i]) for i in range(12)]}")
info(f"a_h head: {[int(ah[i]) for i in range(12)]}")
info(f"r_6 head: {[int(th3_6[i]) for i in range(12)]}")
info("CLASSICAL Jacobi formula (verified):")
info("  r_2(n) = 4 sum_{d|n} chi_4(d)")
info("  r_6(n) = 16 sigma_2^sharp(n) - 4 sigma_2^flat(n)")
info("    sigma_2^flat(n)  = sum_{d|n} chi_4(d) d^2")
info("    sigma_2^sharp(n) = sum_{d|n} chi_4(n/d) d^2")
info("  a_h(n) = (-1)^n r_6(n)  (theta4^6 vs theta3^6)")

check(f"S1.r2: a_g(n)=r_2(n)=4 sum chi_4(d) for all n <= {N_COEFF}",
      r2_ok)
check(f"S1.r6: r_6(n)=16 sigma_2^sharp - 4 sigma_2^flat for all n <= {N_COEFF} "
      "(classical Jacobi; chi_4-weighted sigma_2 combination)",
      r6_theta_ok)
check(f"S1.h: a_h(n)=(-1)^n r_6(n) for all n <= {N_COEFF} "
      "(theta4^6 coefficient identity)",
      ah_sign_ok)

# L-data of g (classical): sum a_g(n) n^{-s} = 4 zeta(s) L(s, chi_4)
s_ld = mpmath.mpf("4.0")
Lg_partial = sum(int(ag[n]) * mpmath.power(n, -s_ld)
                 for n in range(1, min(N_COEFF, 6000) + 1))
Lg_closed = 4 * mpmath.zeta(s_ld) * mpmath.dirichlet(s_ld, [0, 1, 0, -1])
Lg_digits = -mpmath.log10(abs(Lg_partial / Lg_closed - 1) + mpmath.mpf("1e-40"))
info(f"L(g,s)=4 zeta(s)L(s,chi_4) at s=4: partial/closed digits ~ {float(Lg_digits):.1f}")
check("S1.Ldata: g carries L-data {1, chi_4}: sum a_g n^{-s} = 4 zeta L(chi_4) "
      "(>= 10 digits at s=4 vs partial sum)",
      Lg_digits >= 10)


# ================================================================ R1
print("=" * 72)
print("R1 -- Euler product: multiplicativity + degree-4 locals")
print("=" * 72)

c = [0] + [int(ag[n]) * int(ah[n]) for n in range(1, N_COEFF + 1)]
c1 = c[1]
info(f"c(n)=a_g(n)a_h(n); c(1)={c1} (= 4*(-12))")

# Weak multiplicativity: c(nm)*c(1) = c(n)*c(m) for gcd(n,m)=1
mult_bad = []
for n in range(1, N_MULT + 1):
    for m in range(1, N_MULT + 1):
        if sp.gcd(n, m) != 1:
            continue
        if n * m > N_COEFF:
            continue
        if c[n * m] * c1 != c[n] * c[m]:
            mult_bad.append((n, m, c[n * m], c[n] * c[m] // c1 if c1 else None))
            if len(mult_bad) >= 5:
                break
    if len(mult_bad) >= 5:
        break

# Normalised bn = c/c(1) is strictly multiplicative
bn = [0] + [Fraction(c[n], c1) for n in range(1, N_COEFF + 1)]
bn_bad = []
for n in range(1, N_MULT + 1):
    for m in range(1, N_MULT + 1):
        if sp.gcd(n, m) != 1:
            continue
        if n * m > N_COEFF:
            continue
        if bn[n * m] != bn[n] * bn[m]:
            bn_bad.append((n, m))
            if len(bn_bad) >= 5:
                break
    if len(bn_bad) >= 5:
        break

info(f"weak-mult failures (n,m <= {N_MULT}): {len(mult_bad)}")
info(f"normalised-mult failures: {len(bn_bad)}")
check(f"R1.mult: a_g*a_h weakly multiplicative on coprime pairs "
      f"n,m <= {N_MULT} (c(nm)*c(1)=c(n)*c(m); normalised bn(1)=1 Eulerian)",
      len(mult_bad) == 0 and len(bn_bad) == 0 and bn[1] == 1)


def ag_ah_at(n: int):
    """Exact a_g(n), a_h(n) from classical formulas (no q-series bound)."""
    return r2_classical(n), ((-1) ** n) * r6_classical(n)


def bn_prime_power_series(p, K):
    """Normalised local series coeffs bn(p^k) for k=0..K via classical formulas."""
    out = []
    for k in range(K + 1):
        if k == 0:
            out.append(sp.Integer(1))
            continue
        n = p ** k
        ag_n, ah_n = ag_ah_at(n)
        out.append(sp.Rational(ag_n * ah_n, c1))
    return out


def reconstruct_local_factor(p, K=10):
    """Exact rational reconstruction of sum_k bn(p^k) X^k via Padé/solve.

    Returns (rational_function, denom_degree, num, den) or None.
    Prefer denser Padé (higher deg_num+deg_den) among series-exact fits.
    Coefficients from classical r_2/r_6 (unbounded prime powers).
    """
    X = sp.symbols("X")
    coeffs = bn_prime_power_series(p, K)

    best = None
    for deg_num in range(0, 5):
        for deg_den in range(1, 5):
            m, n = deg_num, deg_den
            if m + n > K:
                continue
            unk_a = sp.symbols(f"a0:{m + 1}")
            unk_b = sp.symbols(f"b1:{n + 1}")
            num = sum(unk_a[i] * X ** i for i in range(m + 1))
            den = 1 + sum(unk_b[j] * X ** (j + 1) for j in range(n))
            ser_trunc = sum(coeffs[k] * X ** k for k in range(m + n + 1))
            diff = sp.expand(num - den * ser_trunc)
            eqs = [diff.coeff(X, k) for k in range(m + n + 1)]
            vars_all = list(unk_a) + list(unk_b)
            sol = sp.solve(eqs, vars_all, dict=True)
            if not sol:
                continue
            sol = sol[0]
            # skip underdetermined solutions (free parameters left)
            if any(v not in sol for v in vars_all):
                continue
            if any(sol[v].free_symbols for v in vars_all):
                continue
            num_v = sum(sol[unk_a[i]] * X ** i for i in range(m + 1))
            den_v = 1 + sum(sol[unk_b[j]] * X ** (j + 1) for j in range(n))
            if den_v == 0:
                continue
            rat = sp.cancel(num_v / den_v)
            expanded = rat.series(X, 0, K + 1).removeO()
            ok = all(expanded.coeff(X, k) == coeffs[k] for k in range(K + 1))
            if not ok:
                continue
            den_poly = sp.Poly(sp.fraction(sp.together(rat))[1], X)
            ddeg = int(den_poly.degree())
            score = (m + n, m, n)
            cand = (rat, ddeg, num_v, den_v, score)
            if best is None or score > best[4]:
                best = cand
    if best is None:
        return None
    return best[0], best[1], best[2], best[3]


X = sp.symbols("X")


def theor_local_odd(p):
    """Classical RS Dirichlet local: (1-p^2 X^2)/prod_{i,j}(1-a_i b_j X)."""
    ch = chi4(p)
    num = 1 - (p ** 2) * X ** 2
    den = ((1 - X) * (1 - ch * X)
           * (1 - (p ** 2) * X) * (1 - ch * (p ** 2) * X))
    return sp.cancel(num / den)


def theor_local_2():
    """Exact 2-Euler factor of bn from coefficient fit (closed form)."""
    # (8 X^2 - 10 X + 1) / ((1-X)(1-4X))
    return sp.cancel((8 * X ** 2 - 10 * X + 1) / ((1 - X) * (1 - 4 * X)))


# Sanity: classical prime-power formulas match q-series bn where both defined
pp_match = True
for p in sp.primerange(2, 30):
    p = int(p)
    k = 0
    while p ** k <= N_COEFF:
        if sp.Rational(bn[p ** k]) != bn_prime_power_series(p, k)[k]:
            pp_match = False
            break
        k += 1
    if not pp_match:
        break
info(f"classical prime-power bn matches q-series bn: {pp_match}")

local_ok = True
max_den_deg = 0
local_summary = {}
K_REC = 10
for p in sp.primerange(2, P_LOCAL_MAX + 1):
    p = int(p)
    rec = reconstruct_local_factor(p, K=K_REC)
    if rec is None:
        local_ok = False
        info(f"p={p}: RECONSTRUCTION FAILED")
        continue
    rat, ddeg, num_v, den_v = rec
    max_den_deg = max(max_den_deg, ddeg)
    theor = theor_local_2() if p == 2 else theor_local_odd(p)
    match = sp.simplify(sp.cancel(rat - theor)) == 0
    if not match:
        ser_r = rat.series(X, 0, K_REC + 1).removeO()
        ser_t = theor.series(X, 0, K_REC + 1).removeO()
        match = all(ser_r.coeff(X, k) == ser_t.coeff(X, k)
                    for k in range(K_REC + 1))
    local_ok &= match and ddeg <= 4 and pp_match
    local_summary[p] = (ddeg, match, sp.factor(sp.fraction(
        sp.together(theor))[1]))
    if p <= 13 or not match:
        info(f"p={p}: den_deg={ddeg}, matches_closed={match}, "
             f"den={sp.factor(sp.fraction(sp.together(theor))[1])}")

info(f"max denom degree over p <= {P_LOCAL_MAX}: {max_den_deg}")
info("odd-p local (classical RS): "
     "(1-p^2 X^2)/[(1-X)(1-chi_4(p) X)(1-p^2 X)(1-chi_4(p) p^2 X)]")
info("p=2 local: (1 - 10*2^{-s} + 8*4^{-s}) / "
     "[(1-2^{-s})(1-2^{2-s})]")

check(f"R1.local: Euler factors at all p <= {P_LOCAL_MAX} reconstruct as "
      f"rationals with denom degree <= 4 (max={max_den_deg}); match the "
      "classical RS closed locals (degree-4 = 2x2 Rankin–Selberg)",
      local_ok and max_den_deg <= 4)

K1_fires = not (len(mult_bad) == 0 and local_ok and max_den_deg <= 4)
info(f"K1 (no Euler / deg>4): {'FIRES' if K1_fires else 'silent'}")


# ================================================================ R2
print("=" * 72)
print("R2 -- GL(1) factorisation of D(s)")
print("=" * 72)

info("DERIVATION from R1 locals (odd p):")
info("  Satake of a_g/4 = 1*chi_4  : roots {1, chi_4(p)}")
info("  Satake of weight-3 Eis     : roots {1, chi_4(p) p^2}")
info("    (both Eis pieces of r_6 share the same four pairwise products)")
info("  Classical RS Dirichlet series local =")
info("    (1 - (prod Satake) X^2) / prod_{i,j} (1 - a_i b_j X)")
info("    with prod Satake = p^2  =>  numerator 1 - p^2 X^2")
info("  => odd Euler product =")
info("    zeta_odd(s) L(s,chi_4) zeta_odd(s-2) L(s-2,chi_4) / zeta_odd(2s-2)")
info("CLOSED FORM (with exact 2-Euler):")
info("  D(s) = sum a_g(n) a_h(n) n^{-s}")
info("       = -48 * (1 - 10*2^{-s} + 8*4^{-s})")
info("         * zeta(s) L(s,chi_4) zeta(s-2) L(s-2,chi_4)")
info("         / ( zeta(2s-2) * (1 - 2^{2-2s}) )")
info("  (classical RS zeta(2s-...)-normalisation named as such)")


def L_chi4(s):
    return mpmath.dirichlet(s, [0, 1, 0, -1])


def D_closed(s):
    s = mpmath.mpf(s)
    e2num = (1 - 10 * mpmath.power(2, -s)
             + 8 * mpmath.power(4, -s))
    return ((-48) * e2num
            * mpmath.zeta(s) * L_chi4(s)
            * mpmath.zeta(s - 2) * L_chi4(s - 2)
            / (mpmath.zeta(2 * s - 2)
               * (1 - mpmath.power(2, 2 - 2 * s))))


def c_at(n: int) -> int:
    """c(n)=a_g(n)a_h(n) via classical formulas (unbounded)."""
    ag_n, ah_n = ag_ah_at(n)
    return ag_n * ah_n


def D_partial(s, M=None):
    if M is None:
        M = N_COEFF
    s = mpmath.mpf(s)
    # Use q-series table when in range; classical formulas beyond.
    tot = mpmath.mpf(0)
    for n in range(1, M + 1):
        cn = c[n] if n <= N_COEFF else c_at(n)
        tot += cn * mpmath.power(n, -s)
    return tot


def D_euler(s, Pmax=200):
    """Euler-product evaluation of D via locals (fast at large Re s)."""
    s = mpmath.mpf(s)
    # start from c(1) * prod locals of bn
    prod = mpmath.mpf(c1)
    # p=2
    x2 = mpmath.power(2, -s)
    prod *= ((1 - 10 * x2 + 8 * x2 * x2)
             / ((1 - x2) * (1 - 4 * x2)))
    for p in sp.primerange(3, Pmax + 1):
        ch = chi4(int(p))
        x = mpmath.power(p, -s)
        p2 = mpmath.power(p, 2)
        loc = ((1 - p2 * x * x)
               / ((1 - x) * (1 - ch * x)
                  * (1 - p2 * x) * (1 - ch * p2 * x)))
        prod *= loc
    return prod


# Numeric check at large Re(s): partial sums converge fast (|c(n)|~n^3);
# Euler product cross-check with large Pmax + analytic zeta-tail bound.
# Independent numeric check: large-M partial sums (classical c(n))
# vs closed form at large Re(s).  Also wiring check: c1*E2*odd_GL1 = D.
N_PARTIAL = 80000
s_points = [mpmath.mpf(v) for v in ("7.0", "7.5", "8.0", "8.5")]
r2_ok_all = True
digit_list = []

# Wiring identity (exact in the mpmath model): D = c1 * e2 * odd_GL1
wiring_ok = True
for s in s_points:
    closed = D_closed(s)
    x2 = mpmath.power(2, -s)
    e2 = (1 - 10 * x2 + 8 * x2 * x2) / ((1 - x2) * (1 - 4 * x2))
    odd_gl1 = (mpmath.zeta(s) * (1 - mpmath.power(2, -s)) * L_chi4(s)
               * mpmath.zeta(s - 2) * (1 - mpmath.power(2, 2 - s))
               * L_chi4(s - 2)
               / (mpmath.zeta(2 * s - 2)
                  * (1 - mpmath.power(2, 2 - 2 * s))))
    wired = c1 * e2 * odd_gl1
    d_wire = -mpmath.log10(abs(wired / closed - 1) + mpmath.mpf("1e-45"))
    wiring_ok &= d_wire >= 25
    partial = D_partial(s, M=N_PARTIAL)
    d_pa = -mpmath.log10(abs(partial / closed - 1) + mpmath.mpf("1e-45"))
    digit_list.append(float(d_pa))
    ok_pt = float(d_pa) >= 20
    r2_ok_all &= ok_pt
    info(f"s={s}: D_closed={closed}")
    info(f"  wiring digits={float(d_wire):.1f}; "
         f"partial(M={N_PARTIAL})/closed digits={float(d_pa):.1f}")

check("R2.closed: D(s) = -48*(1-10*2^{-s}+8*4^{-s}) "
      "* zeta(s) L(s,chi_4) zeta(s-2) L(s-2,chi_4) "
      "/ (zeta(2s-2)*(1-2^{2-2s})) "
      "(derived from degree-4 locals; classical RS normalisation; "
      "wiring c1*E_2*odd_GL1 identity holds to >= 25 digits)",
      wiring_ok)

check("R2.numeric: closed form matches independent partial sums "
      f"(classical c(n), M={N_PARTIAL}) at s in {{7.0, 7.5, 8.0, 8.5}} "
      f"with >= 20 digits each (got {[round(d, 1) for d in digit_list]})",
      r2_ok_all and all(d >= 20 for d in digit_list))

# Partial-sum tail control at one point
s_tail = mpmath.mpf("7.5")
pA = D_partial(s_tail, M=20000)
pB = D_partial(s_tail, M=N_PARTIAL)
cl = D_closed(s_tail)
tail_shrink = abs(pB - cl) < abs(pA - cl)
info(f"tail control at s=7.5: |partial(20k)-closed|={float(abs(pA - cl)):.3e}; "
     f"|partial({N_PARTIAL})-closed|={float(abs(pB - cl)):.3e}; "
     f"shrinks={tail_shrink}")
check("R2.tail: partial sums approach closed form (tail shrinks "
      f"20k -> {N_PARTIAL} at s=7.5)",
      tail_shrink and abs(pB / cl - 1) < mpmath.mpf("1e-20"))

K2_fires = not r2_ok_all
info(f"K2 (no GL(1) factorisation): {'FIRES' if K2_fires else 'silent'}")


# ================================================================ R3
print("=" * 72)
print("R3 -- xi-honesty: shift table under weight normalisation")
print("=" * 72)

k_g, k_h = 1, 3
wshift = (k_g + k_h - 2) // 2   # = 1
info(f"weights (k_g, k_h)=({k_g},{k_h}); "
     f"weight shift (k_g+k_h-2)/2 = {wshift}")
info("RAW GL(1) factors in D(s) (numerator; ignoring 2-Euler and 1/zeta):")
raw_factors = [
    ("zeta(s)", 0, "centre of Lambda at s=1/2"),
    ("L(s, chi_4)", 0, "centre of Lambda at s=1/2"),
    ("zeta(s-2)", 2, "centre when s-2=1/2 i.e. s=5/2"),
    ("L(s-2, chi_4)", 2, "centre when s-2=1/2 i.e. s=5/2"),
]
for name, sh, note in raw_factors:
    info(f"  {name}: shift={sh}; {note}")
info("Denominator (classical RS normalisation): zeta(2s-2) "
     "(argument centre 1/2 => s=5/4)")

info(f"WEIGHT-NORMALISED variable s_norm = s - {wshift}")
info(f"  (equivalently evaluate D_raw at s_norm+{wshift})")
norm_factors = [
    ("zeta(s_norm+1)", 1, "Lambda-centre at s_norm=-1/2  (NOT 1/2)"),
    ("L(s_norm+1, chi_4)", 1, "Lambda-centre at s_norm=-1/2  (NOT 1/2)"),
    ("zeta(s_norm-1)", -1, "Lambda-centre at s_norm=3/2   (NOT 1/2)"),
    ("L(s_norm-1, chi_4)", -1, "Lambda-centre at s_norm=3/2   (NOT 1/2)"),
]
any_unshifted_norm = False
for name, sh, note in norm_factors:
    info(f"  {name}: weight-shift residue={sh}; {note}")
    if sh == 0:
        any_unshifted_norm = True

info("HONEST R3: raw D(s) DOES contain unshifted zeta(s) and L(s,chi_4)")
info("  (so Phi via RS reaches GL(1) products including zeta).")
info("  After weight normalisation s -> s+(k_g+k_h-2)/2, ALL four")
info("  GL(1) components are shifted off the xi-centre 1/2.")
info("  => xi itself is NOT yet reached by this RS translation.")

check("R3.shifts: shift table documented — raw factors at shifts "
      "{0,0,2,2}; weight-normalised at {+1,+1,-1,-1}; "
      "NO component on centre 1/2 after weight normalisation "
      "(honest negative for xi-carrying)",
      (not any_unshifted_norm)
      and [sh for _, sh, _ in raw_factors] == [0, 0, 2, 2])


# ================================================================ R4
print("=" * 72)
print("R4 -- relation to L(F,s); a_p(f8) visibility")
print("=" * 72)

# f8 from eta product (part 12)
def conv_i64(a, b, order):
    return np.convolve(a, b)[: order + 1]


f8 = np.roll(conv_i64(eta_pass(2, 4, N_COEFF),
                      eta_pass(4, 4, N_COEFF), N_COEFF), 1)
f8[0] = 0

info("L(F,s) = 16*2^{-s} eta(s)eta(s-3) - 8 L(f8,s)  (part 12)")
info("  Eis channel: trivial × trivial at shifts {0, 3}")
info("  D(s) channel: {1, chi_4} × {1, chi_4} at shifts {0, 2}")
info("  (plus 1/zeta(2s-2) RS normalisation and 2-Euler)")
info("=> D is NOT a scalar multiple of the Eis piece of L(F): "
     "different shifts (2 vs 3) and D carries chi_4.")

# Visibility: D-local at odd p depends only on p and chi_4(p), not a_p(f8)
# Two primes with same chi_4 but different a_p(f8) must share the same
# local-factor SHAPE (the polynomial in terms of p, chi), while a_p differs.
ap_f8 = {int(p): int(f8[int(p)]) for p in sp.primerange(3, 50)}
info(f"a_p(f8) for p<=47: {ap_f8}")

# Compare: local factor is determined by (p, chi4(p)); a_p(f8) is not a
# coefficient of that local polynomial.
# Explicit: the Dirichlet series coefficient bn(p) = a_g(p)a_h(p)/c(1)
# For p odd: bn(p) = (ag[p]/4) * (ah[p]/(-12)) *? wait bn(p)=c(p)/c(1)
# Closed: from local series, coeff of X is:
#   for ch=1: 2*(1+p^2) = 2+2p^2?  From (k+1)*e1 at k=1: 2*(1+p^2)=2+2p^2
#   Actually bn(p) for ch=1: 2*(1+p^2)? p=5: 2(1+25)=52 ✓
#   for ch=-1: bn(p)=0
# while a_p(f8) is nonzero for p=3 (a_3=-4) but bn(3)=0.
visibility_kill = True
reasons = []
for p in (3, 7, 11):
    # chi4=-1, bn(p)=0, but a_p(f8) != 0
    if chi4(p) == -1 and bn[p] == 0 and ap_f8[p] != 0:
        reasons.append(f"p={p}: bn(p)=0 but a_p(f8)={ap_f8[p]}")
    else:
        visibility_kill = False
for p in (5, 13, 17):
    # chi4=+1: bn(p)=2(1+p^2) depends only on p, not a_p
    predicted = 2 * (1 + p * p)
    if bn[p] == predicted:
        reasons.append(f"p={p}: bn(p)={bn[p]}=2(1+p^2) "
                       f"independent of a_p(f8)={ap_f8[p]}")
    else:
        visibility_kill = False

info("a_p(f8) visibility evidence:")
for r in reasons:
    info(f"  {r}")

# Also: local Euler factor polynomial has coefficients in Z[p, chi4(p)],
# never involving a_p(f8).  Pair p=5 (a_p=-2) and the formula.
f8_invisible = (bn[3] == 0 and ap_f8[3] != 0
                and bn[5] == 2 * (1 + 25)
                and all(theor_local_odd(int(p)).free_symbols <= {X}
                        for p in sp.primerange(3, 30)))

check("R4.invisible: a_p(f8) is NOT visible in the degree-4 local data "
      "of D (e.g. bn(3)=0 while a_3(f8)=-4; bn(p)=2(1+p^2) for "
      "p=1 mod 4, pure in p; locals are classical Eisenstein RS)",
      f8_invisible and visibility_kill)

# Type the relationship
info("TYPED RELATION:")
info("  D(s) = RS-convolution of the FACTORS (g,h) "
     "= Eisenstein GL(1)-product shadow.")
info("  L(F,s) = additive L-series of the PRODUCT F=g*h "
     "= Eis(trivial; shifts 0,3) - 8 L(f8,s).")
info("  Consequence: RS translates the Eisenstein factor-data; "
     "the cusp form f8 needs a DIFFERENT bridge "
     "(next narrowing of ZETA.COMPILER.FUNCTOR).")

check("R4.typed: D = Eisenstein RS-shadow of the factors; "
      "L(F) mixes trivial-channel Eis (shifts 0,3) with cusp f8; "
      "RS does not see the cusp — typed as the next functor gap",
      f8_invisible)


# ================================================================ S6 verdict
print("=" * 72)
print("S6 -- verdict for ZETA.COMPILER.FUNCTOR")
print("=" * 72)

r1_pass = len(mult_bad) == 0 and local_ok and max_den_deg <= 4
r2_pass = r2_ok_all
r3_honest = not any_unshifted_norm   # xi not reached after weight norm
r4_typed = f8_invisible

if r1_pass and r2_pass and r3_honest and r4_typed and not K1_fires and not K2_fires:
    verdict = "RS-TRANSLATES-EISENSTEIN"
elif r1_pass and r2_pass:
    verdict = "PARTIAL"
else:
    verdict = "DEAD"

info(f"R1={r1_pass} R2={r2_pass} R3_honest_xi_miss={r3_honest} "
     f"R4_typed={r4_typed}")
info(f"K1={'fire' if K1_fires else 'silent'} "
     f"K2={'fire' if K2_fires else 'silent'}")
info(f"VERDICT: {verdict}")
info("CONSEQUENCE for ZETA.COMPILER.FUNCTOR:")
info("  The named first translation test SUCCEEDS on the Eisenstein")
info("  content of the factorisation: Phi's factor data {1,chi_4} x")
info("  {chi_4-pair, shift 2} maps under Rankin–Selberg to the GL(1)")
info("  product zeta(s) L(s,chi_4) zeta(s-2) L(s-2,chi_4) / zeta(2s-2).")
info("  Honest limits: (i) weight-normalised RS does NOT place any")
info("  factor on the xi-centre 1/2; (ii) the cusp a_p(f8) is invisible")
info("  — RS translates the Eisenstein shadow, not the full L(F,s).")
info("NEXT LEVER: a cusp-compatible translation "
     "(Shimura lift / Rankin–Selberg against a cusp form / "
     "other Hecke-bridge) that sees a_p(f8), or a mechanism that")
info("  recentres one GL(1) factor onto the xi-line without "
     "smuggling zeta externally (K3 of part 34).")

check(f"S6.verdict: {verdict} (R1+R2 exact; R3/R4 honestly typed; "
      "K1/K2 silent)",
      verdict == "RS-TRANSLATES-EISENSTEIN")


# ================================================================ summary
print("=" * 72)
elapsed = time.time() - T0
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({elapsed:.1f}s)")
print(f"VERDICT: {verdict}")
if FAIL:
    raise SystemExit(1)
raise SystemExit(0)
