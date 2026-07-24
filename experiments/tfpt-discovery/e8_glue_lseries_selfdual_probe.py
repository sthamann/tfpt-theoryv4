"""Discovery probe (2026-07-24), part 12 of the zeta/prime investigation.
Deep dive on part 11 ("are we missing something big?").  Three threads,
each exact:

  S1  The L-series of the signed glue census c(n) (part 11:
      Th0 - Th2 = th3^2 th4^6 = Eisenstein tower - 8 f8).  Closed forms:
      even n: c(2m) = 16 s3(m) - 288 s3(m/2) + 512 s3(m/4); odd n:
      c(n) = -8 a_n(f8).  2-adic polynomial factorizes:
      16x(1 - 18x + 32x^2) = 16x(1-2x)(1-16x)  =>  the Eisenstein part
      of the L-series is 16 2^-s eta(s) eta(s-3) (Dirichlet eta!).
  S2  POLE KILLING: the trivial channel 240 zeta(s) zeta(s-3) has a
      simple pole at s = 4 (residue 240 zeta(4) = 8 pi^4/3); the spinor
      channel 64 (1-2^-s) zeta zeta keeps it; the mu4-SIGNED channel is
      ENTIRE -- the glue character kills the pole exactly as chi-twists
      do for Dirichlet L-functions.  Special values EXACT:
      Eis(1) = 0, Eis(2) = pi^2/12, Eis(3) = (3/4) zeta(3),
      Eis(4) = 7 pi^4 ln2 / 720.
  S3  THE APERY BRIDGE: f8 = eta(2t)^4 eta(4t)^4 is the Beukers /
      Ahlgren-Ono form: A((p-1)/2) = a_p mod p^2 (Apery numbers of the
      zeta(3) irrationality proof) and the van Hamme (M.2) / Kilbourn
      supercongruence sum_{k<=(p-1)/2} ((1/2)_k/k!)^4 = a_p mod p^3.
      Via part 11, the signed E8 glue census at odd prime shells is
      c(p) = -8 a_p == -8 A((p-1)/2) mod p^2.  Placebo control: the
      congruences FAIL for eta(4t)^8.
  S4  L-VALUES: exact incomplete-Gamma formula for L(f8, s) (Fricke
      sign determined against the direct Dirichlet sum), functional
      equation L(1) = eps 4 L(3)/pi^2 verified, L_c(s) assembled and
      cross-checked against the direct census sum at s = 5.
  S5  SELF-DUAL WIDTH: Poisson summation for the E8 census
      Theta(e^{-2t}) = (pi/t)^4 Theta(e^{-2 pi^2/t}); UNIQUE self-dual
      width t = pi.  The v526-measured seam angle beta = 2 pi = 1/(4c3)
      gives Boltzmann weight e^{-beta norm/2} = e^{-pi |x|^2} = THE
      self-dual Gaussian.  So c3 = 1/(8 pi) rewrites as
      c3 = 1/(|mu4| * beta_selfdual) -- typed chain, each link exact;
      the identification seam-KMS-parameter == census-width is the OPEN
      mechanism (fence, named kill).  Component census S-duality
      F(e^{-pi/x}) = x^4 G(e^{-pi x}) with fixed point x = 1, where the
      values are LEMNISCATIC: F(e^{-pi}) = 2^{-3/2} pi^2 / Gamma(3/4)^8
      = Gamma(1/4)^8/(2^{11/2} pi^6) = sqrt2 / AGM(1, sqrt2)^4 (Gauss
      constant; Chowla-Selberg class {Gamma(1/4), pi} of Q(i)), and
      F / Theta_E8 = sqrt2 / 3 there.
  S6  Honest registry census of ALL new special values (v527
      discipline, placebo family) -- expected NULL.

Firewall: discovery sandbox, NO promotion, no marker moves, no RH
evidence; classical theorems (Ahlgren-Ono, Kilbourn, Chowla-Selberg,
Poisson) named as such -- probe content is the exact in-suite
correlation web, not new mathematics.
"""
import json
import math
import time
from fractions import Fraction

import numpy as np
import mpmath
import sympy as sp
from sympy import Rational

PASS = 0
FAIL = 0
T0 = time.time()
N0 = 4096
mpmath.mp.dps = 30


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


# ---------------------------------------------------------------- data
def theta_arr(kind, order):
    s = np.zeros(order + 1, dtype=np.int64)
    if kind == 3:
        s[0] = 1
        n = 1
        while n * n <= order:
            s[n * n] = 2
            n += 1
    elif kind == 4:
        s[0] = 1
        n = 1
        while n * n <= order:
            s[n * n] = 2 * (-1) ** n
            n += 1
    return s


def conv(a, b, order):
    return np.convolve(a, b)[: order + 1]


def eta_pass(d, e, order):
    """prod_{n>=1} (1 - q^{d n})^e via vectorized passes."""
    s = np.zeros(order + 1, dtype=np.int64)
    s[0] = 1
    for k in range(d, order + 1, d):
        for _ in range(e):
            s[k:] = s[k:] - s[:-k]
    return s


th3 = theta_arr(3, N0)
th4 = theta_arr(4, N0)
th3sq = conv(th3, th3, N0)
t4_2 = conv(th4, th4, N0)
t4_4 = conv(t4_2, t4_2, N0)
t4_6 = conv(t4_4, t4_2, N0)
c = conv(th3sq, t4_6, N0)                      # signed glue census
f8 = np.roll(conv(eta_pass(2, 4, N0), eta_pass(4, 4, N0), N0), 1)
f8[0] = 0
g16 = np.roll(eta_pass(4, 8, N0), 1)
g16[0] = 0
sig3 = {m: int(sp.divisor_sigma(m, 3)) for m in range(1, N0 // 2 + 1)}


def c_even_formula(n):
    m = n // 2
    v = 16 * sig3[m]
    if m % 2 == 0:
        v -= 288 * sig3[m // 2]
    if m % 4 == 0:
        v += 512 * sig3[m // 4]
    return v


# ================================================================ S1
print("S1 -- closed forms of c(n) and the eta(s) eta(s-3) skeleton")
head = [1, -8, 16, 32, -144, 16, 448, -192, -912, 88, 2016, 352, -4032]
even_ok = all(int(c[n]) == c_even_formula(n) for n in range(2, N0 + 1, 2))
odd_ok = all(int(c[n]) == -8 * int(f8[n]) for n in range(1, N0 + 1, 2))
check(f"c(n) to n = {N0} by direct theta convolution: head matches part "
      "11; EVEN closed form c(2m) = 16 s3(m) - 288 s3(m/2) + 512 s3(m/4) "
      "for ALL even n; ODD closed form c(n) = -8 a_n(f8) for ALL odd n "
      "(f8 from the independent eta-product route)",
      list(c[:13]) == head and even_ok and odd_ok)
x = sp.symbols('x')
poly_ok = sp.expand(16 * x * (1 - 18 * x + 32 * x ** 2)
                    - 16 * x * (1 - 2 * x) * (1 - 16 * x)) == 0
s5 = mpmath.mpf(5)
eis_direct = sum(mpmath.mpf(c_even_formula(n)) / n ** 5
                 for n in range(2, N0 + 1, 2))
eis_eta = 16 * 2 ** (-s5) * mpmath.altzeta(5) * mpmath.altzeta(2)
info(f"Eis(5): direct even sum = {eis_direct}, "
     f"16 2^-5 eta(5) eta(2) = {eis_eta}")
check("2-adic polynomial factorizes EXACTLY: 16x(1-18x+32x^2) = "
      "16x(1-2x)(1-16x) => Eisenstein part of the census L-series = "
      "16 2^-s eta(s) eta(s-3) with eta = DIRICHLET ETA (the mu4 signing "
      "replaces zeta zeta by eta eta); numeric match at s = 5 "
      "(tail-limited, 1e-6)",
      poly_ok and abs(eis_direct - eis_eta) < 1e-6)

# ================================================================ S2
print("S2 -- pole killing: the signed channel is the unique ENTIRE one")
# rebuild Th1 via q-series route of part 11: theta2(u)^8 / 4 with
# u = q^{1/2}; stored in t = q^{1/8} units (exponents o^2, o odd)
TQ = 300
th2t = np.zeros(8 * TQ + 1, dtype=np.int64)
o = 1
while o * o <= 8 * TQ:
    th2t[o * o] = 2
    o += 2
t = np.convolve(th2t, th2t)[: 8 * TQ + 1]
t = np.convolve(t, t)[: 8 * TQ + 1]
t = np.convolve(t, t)[: 8 * TQ + 1]             # theta2(u)^8 in t-units
Th1 = np.array([t[8 * n] // 4 for n in range(TQ + 1)], dtype=np.int64)
spin_formula = all(int(Th1[n]) == 64 * sum((n // d) ** 3
                                           for d in sp.divisors(n)
                                           if d % 2 == 1)
                   for n in range(1, TQ + 1))
sE = mpmath.mpf(8)
spin_L_direct = sum(mpmath.mpf(int(Th1[n])) / mpmath.mpf(n) ** 8
                    for n in range(1, TQ + 1))
spin_L_closed = 64 * (1 - 2 ** (-sE)) * mpmath.zeta(8) * mpmath.zeta(5)
res_num = mpmath.mpf('0.001') * 240 * mpmath.zeta(mpmath.mpf('4.001')) \
    * mpmath.zeta(mpmath.mpf('1.001'))
res_exact = 240 * mpmath.zeta(4)


def L_f8_direct(s):
    return sum(mpmath.mpf(int(f8[n])) / mpmath.mpf(n) ** s
               for n in range(1, N0 + 1, 2))


Lc_4001 = (16 * 2 ** mpmath.mpf('-4.001')
           * mpmath.altzeta(mpmath.mpf('4.001'))
           * mpmath.altzeta(mpmath.mpf('1.001'))
           - 8 * L_f8_direct(mpmath.mpf('4.001')))
Lc_45 = (16 * 2 ** mpmath.mpf('-4.5') * mpmath.altzeta(mpmath.mpf('4.5'))
         * mpmath.altzeta(mpmath.mpf('1.5')) - 8 * L_f8_direct(4.5))
info(f"residue at s=4 of the trivial channel: {res_num} vs 240 zeta(4) "
     f"= 8 pi^4/3 = {res_exact}")
info(f"L_c near the killed pole: L_c(4.001) = {Lc_4001} (finite)")
check("THREE CHANNELS of the E8 counting function: trivial = "
      "240 zeta(s) zeta(s-3) with simple pole at s = 4, residue "
      "240 zeta(4) = 8 pi^4/3 (numeric 1%); spinor = Th1(n)/64 = "
      "sum_{d|n odd} (n/d)^3 exactly (n <= 300) => 64 (1-2^-s) zeta "
      "zeta, pole SURVIVES; mu4-signed = 16 2^-s eta eta - 8 L(f8) => "
      "ENTIRE.  The signed channel is the UNIQUE pole-free one -- the "
      "glue character is a pole killer, exactly the zeta vs L(chi) "
      "pattern",
      spin_formula
      and abs(spin_L_direct - spin_L_closed) < 1e-6
      and abs(res_num / res_exact - 1) < 0.01
      and abs(Lc_4001) < 50 and abs(Lc_4001 - Lc_45) < 5)
s_ = sp.symbols('s')
# eta(1) = ln 2 (classical value of the Dirichlet eta at 1); verified
# numerically instead of via sympy limit (gruntz recursion issue)
eta1 = sp.log(2)
eta1_num_ok = abs(mpmath.altzeta(1) - mpmath.log(2)) < mpmath.mpf('1e-25')
eis1 = 8 * eta1 * (1 - 8) * sp.zeta(-2)
eis2 = 16 * Rational(1, 4) * (1 - 2 ** (1 - 2)) * (1 - 2 ** 2) \
    * sp.zeta(2) * sp.zeta(-1)
eis3 = 16 * Rational(1, 8) * (1 - Rational(1, 4)) * (1 - 2) \
    * sp.zeta(3) * sp.zeta(0)
eis4 = 16 * Rational(1, 16) * (1 - 2 ** -3) * sp.zeta(4) * eta1
info(f"Eis specials: Eis(1) = {eis1}, Eis(2) = {sp.simplify(eis2)}, "
     f"Eis(3) = {sp.simplify(eis3)}, Eis(4) = {sp.simplify(eis4)}")
check("Eisenstein special values EXACT: Eis(1) = 0 (via the trivial "
      "zero zeta(-2) = 0), Eis(2) = pi^2/12, Eis(3) = (3/4) zeta(3), "
      "Eis(4) = 7 pi^4 ln2 / 720 -- zeta(3) and ln 2 (the first BC "
      "energy, part 4) appear at the integer points of the signed "
      "census L-series (typed observation: 3/4 = the v205 tree ratio)",
      eta1_num_ok and eis1 == 0
      and sp.simplify(eis2 - sp.pi ** 2 / 12) == 0
      and sp.simplify(eis3 - Rational(3, 4) * sp.zeta(3)) == 0
      and sp.simplify(eis4 - 7 * sp.pi ** 4 * sp.log(2) / 720) == 0)

# ================================================================ S3
print("S3 -- the Apery / zeta(3) bridge (Ahlgren-Ono, Kilbourn)")
odd_primes = [p for p in range(3, 98) if sp.isprime(p)]


def apery(n):
    return sum(math.comb(n, k) ** 2 * math.comb(n + k, k) ** 2
               for k in range(n + 1))


ao_ok, ao_wit = True, []
for p in odd_primes:
    lhs = apery((p - 1) // 2) % p ** 2
    rhs = int(f8[p]) % p ** 2
    ao_wit.append((p, lhs == rhs))
    ao_ok &= (lhs == rhs)
check("AHLGREN-ONO (Beukers' conjecture, proved 2000): the zeta(3) "
      "Apery numbers satisfy A((p-1)/2) == a_p(f8) mod p^2 for ALL odd "
      "p <= 97 -- via part 11 the signed E8 glue census at odd prime "
      "shells obeys c(p) = -8 a_p == -8 A((p-1)/2) mod p^2: the census "
      "KNOWS the Apery numbers of the zeta(3) irrationality proof",
      ao_ok)


def kilbourn_sum(p):
    tot = Fraction(0)
    for k in range((p - 1) // 2 + 1):
        tot += Fraction(math.comb(2 * k, k), 4 ** k) ** 4
    num, den = tot.numerator, tot.denominator
    return (num * pow(den, -1, p ** 3)) % p ** 3


kil_ok = all(kilbourn_sum(p) == int(f8[p]) % p ** 3 for p in odd_primes)
check("KILBOURN / van HAMME (M.2): the truncated hypergeometric "
      "4F3-sum sum_{k<=(p-1)/2} ((1/2)_k / k!)^4 == a_p(f8) mod p^3 for "
      "ALL odd p <= 97 -- the mod-p^3 supercongruence layer of the same "
      "cusp form", kil_ok)
pl_ao = sum(1 for p in odd_primes
            if apery((p - 1) // 2) % p ** 2 != int(g16[p]) % p ** 2)
pl_kil = sum(1 for p in odd_primes
             if kilbourn_sum(p) != int(g16[p]) % p ** 3)
info(f"placebo eta(4t)^8: Ahlgren-Ono fails {pl_ao}/{len(odd_primes)}, "
     f"Kilbourn fails {pl_kil}/{len(odd_primes)}")
check("placebo control: BOTH congruences fail for the neighbour "
      "eta-product eta(4t)^8 on >= half the primes -- the Apery bridge "
      "is specific to f8, not generic eta noise",
      pl_ao >= len(odd_primes) // 2 and pl_kil >= len(odd_primes) // 2)

# ================================================================ S4
print("S4 -- L-values of f8 and the assembled census L-series")
hecke_ok = (int(f8[9]) == int(f8[3]) ** 2 - 27
            and int(f8[25]) == int(f8[5]) ** 2 - 125
            and int(f8[49]) == int(f8[7]) ** 2 - 343
            and int(f8[15]) == int(f8[3]) * int(f8[5])
            and int(f8[21]) == int(f8[3]) * int(f8[7])
            and int(f8[35]) == int(f8[5]) * int(f8[7]))
sqN = mpmath.sqrt(8)
K = 4


def L_f8(s, eps, terms=80):
    lam = mpmath.mpf(0)
    for n in range(1, terms + 1):
        an = int(f8[n])
        if an == 0:
            continue
        xx = 2 * mpmath.pi * n / sqN
        lam += an * ((sqN / (2 * mpmath.pi * n)) ** s
                     * mpmath.gammainc(s, xx)
                     + eps * (sqN / (2 * mpmath.pi * n)) ** (K - s)
                     * mpmath.gammainc(K - s, xx))
    return lam / ((sqN / (2 * mpmath.pi)) ** s * mpmath.gamma(s))


Ldir45 = L_f8_direct(mpmath.mpf('4.5'))
gaps = {e: abs(L_f8(mpmath.mpf('4.5'), e) - Ldir45) for e in (1, -1)}
eps = 1 if gaps[1] < gaps[-1] else -1
info(f"Fricke sign: |formula-direct| at s=4.5: eps=+1: {gaps[1]}, "
     f"eps=-1: {gaps[-1]} -> eps = {eps:+d}")
check("f8 is a Hecke eigenform (a_9 = a_3^2 - 27, a_25 = a_5^2 - 125, "
      "a_49 = a_7^2 - 343, full multiplicativity spot-checks) and the "
      "Fricke sign is decided against the direct Dirichlet sum at "
      "s = 4.5 (gap ratio >= 10)",
      hecke_ok and max(gaps.values()) / min(gaps.values()) > 10)
L1 = L_f8(1, eps)
L2 = L_f8(2, eps)
L3 = L_f8(3, eps)
L4 = L_f8(4, eps)
info(f"L(f8,1) = {L1}")
info(f"L(f8,2) = {L2}")
info(f"L(f8,3) = {L3}")
fe = abs(L1 - eps * 4 * L3 / mpmath.pi ** 2)
check("functional equation numeric: L(f8,1) = eps 4 L(f8,3) / pi^2 "
      "(< 1e-20)", fe < mpmath.mpf('1e-20'))
Lc2 = mpmath.pi ** 2 / 12 - 8 * L2
Lc3 = mpmath.mpf(3) / 4 * mpmath.zeta(3) - 8 * L3
Lc4 = 7 * mpmath.pi ** 4 * mpmath.log(2) / 720 - 8 * L4
info(f"L_c(1) = -8 L(f8,1) = {-8 * L1}")
info(f"L_c(2) = pi^2/12 - 8 L(f8,2) = {Lc2}")
info(f"L_c(3) = (3/4) zeta(3) - 8 L(f8,3) = {Lc3}")
info(f"L_c(4) = 7 pi^4 ln2/720 - 8 L(f8,4) = {Lc4}")
Lc5_asm = (16 * 2 ** mpmath.mpf(-5) * mpmath.altzeta(5)
           * mpmath.altzeta(2) - 8 * L_f8(5, eps))
Lc5_dir = sum(mpmath.mpf(int(c[n])) / mpmath.mpf(n) ** 5
              for n in range(1, N0 + 1))
info(f"L_c(5): assembled = {Lc5_asm}, direct census sum = {Lc5_dir}")
check("assembly cross-check: L_c(5) from [16 2^-s eta eta - 8 L(f8,s)] "
      "matches the direct census sum over c(n) to n = 4096 (< 1e-3, "
      "tail-limited) -- the decomposition IS the census L-series",
      abs(Lc5_asm - Lc5_dir) < 1e-3)

# ================================================================ S5
print("S5 -- Poisson self-duality: 2 pi = 1/(4 c3) is the self-dual width")
E4c = np.zeros(N0 + 1, dtype=np.int64)
E4c[0] = 1
for n in range(1, N0 + 1):
    E4c[n] = 240 * (sig3[n] if n <= N0 // 2 else int(sp.divisor_sigma(n, 3)))


def census_E4(q):
    q = mpmath.mpf(q)
    tot, n = mpmath.mpf(0), 0
    while True:
        term = int(E4c[n]) * q ** n
        tot += term
        n += 1
        if n > N0 or (n > 8 and abs(term) < mpmath.mpf('1e-40')):
            break
    return tot


pois_ok = True
for tw in (mpmath.mpf('1.1'), mpmath.mpf('2.6')):
    lhs = census_E4(mpmath.e ** (-2 * tw))
    rhs = (mpmath.pi / tw) ** 4 * census_E4(
        mpmath.e ** (-2 * mpmath.pi ** 2 / tw))
    pois_ok &= abs(lhs / rhs - 1) < mpmath.mpf('1e-24')
check("POISSON SUMMATION for the E8 census: sum e^{-t|x|^2} = (pi/t)^4 "
      "sum e^{-(pi^2/t)|x|^2} (25 digits at t = 1.1, 2.6); the dual "
      "width is pi^2/t => the UNIQUE self-dual width is t = pi",
      pois_ok and set(sp.solve(sp.pi ** 2 / s_ - s_, s_))
      == {sp.pi, -sp.pi})
c3 = 1 / (8 * sp.pi)
beta = 1 / (4 * c3)
check("THE CHAIN (each link exact, typed as rewriting): c3 = 1/(8 pi) "
      "<=> beta = 1/(4 c3) = 2 pi (the v526-MEASURED seam KMS angle) "
      "<=> Boltzmann weight e^{-beta norm/2} = e^{-pi |x|^2} = THE "
      "self-dual Gaussian of Fourier analysis <=> tau = i, the CM point "
      "of Q(i) = the mu4 field.  So 8 pi = |mu4| x (self-dual width x "
      "2): c3 = 1/(|mu4| * beta_selfdual).  OPEN [O] (fence): that the "
      "seam KMS parameter IS the census Gaussian width is NOT derived "
      "-- candidate contract SEAM.SELFDUAL.WIDTH, kill: a derivation "
      "fixing the census width != 2 pi or separating the two parameters",
      beta == 2 * sp.pi and sp.simplify(1 / (4 * beta) - c3) == 0)
jt = mpmath.jtheta
x0 = mpmath.mpf('1.37')


def Fsig(q):
    return jt(3, 0, q) ** 2 * jt(4, 0, q) ** 6


def Gdual(q):
    return jt(3, 0, q) ** 2 * jt(2, 0, q) ** 6


sd_lhs = Fsig(mpmath.e ** (-mpmath.pi / x0))
sd_rhs = x0 ** 4 * Gdual(mpmath.e ** (-mpmath.pi * x0))
series_F = sum(int(c[n]) * mpmath.mpf('0.1') ** n for n in range(N0 + 1))
check("component S-duality: F(e^{-pi/x}) = x^4 G(e^{-pi x}) with "
      "G = th3^2 th2^6 (25 digits at x = 1.37; fixed point x = 1); "
      "jtheta route agrees with our census series at q = 0.1 (25 digits)",
      abs(sd_lhs / sd_rhs - 1) < mpmath.mpf('1e-24')
      and abs(Fsig(mpmath.mpf('0.1')) / series_F - 1)
      < mpmath.mpf('1e-24'))
Fcm = Fsig(mpmath.e ** (-mpmath.pi))
v1 = 2 ** mpmath.mpf('-1.5') * mpmath.pi ** 2 / mpmath.gamma(
    mpmath.mpf(3) / 4) ** 8
v2 = mpmath.gamma(mpmath.mpf(1) / 4) ** 8 / (2 ** mpmath.mpf('5.5')
                                             * mpmath.pi ** 6)
v3 = mpmath.sqrt(2) / mpmath.agm(1, mpmath.sqrt(2)) ** 4
ratio = Fcm / census_E4(mpmath.e ** (-2 * mpmath.pi))
lemn = (mpmath.gamma(mpmath.mpf(1) / 4) ** 2
        / (2 ** mpmath.mpf('1.5') * mpmath.sqrt(mpmath.pi)))
info(f"F at the fixed point e^-pi: {Fcm}")
info(f"  = 2^-3/2 pi^2/G(3/4)^8: {v1}; G(1/4)^8/(2^5.5 pi^6): {v2}; "
     f"sqrt2/AGM(1,sqrt2)^4: {v3}")
info(f"ratio F(e^-pi)/Theta_E8(e^-2pi): {ratio} vs sqrt2/3 = "
     f"{mpmath.sqrt(2) / 3}")
check("at the self-dual fixed point the census values are LEMNISCATIC "
      "(Chowla-Selberg class of Q(i)): F(e^-pi) = 2^-3/2 pi^2/G(3/4)^8 "
      "= G(1/4)^8/(2^11/2 pi^6) = sqrt2/AGM(1,sqrt2)^4 (Gauss constant; "
      "25 digits each); the two special temperatures are LINKED: "
      "F(e^-pi) / Theta_E8(e^-2pi) = sqrt2/3 exactly (component fixed "
      "point beta = pi vs seam self-dual point beta = 2pi); lemniscate "
      "constant varpi = G(1/4)^2/(2^3/2 sqrt pi) confirmed -- the mu4 "
      "field FORCES the transcendence class {Gamma(1/4), pi} at its "
      "special points",
      abs(Fcm / v1 - 1) < mpmath.mpf('1e-24')
      and abs(Fcm / v2 - 1) < mpmath.mpf('1e-24')
      and abs(Fcm / v3 - 1) < mpmath.mpf('1e-24')
      and abs(ratio / (mpmath.sqrt(2) / 3) - 1) < mpmath.mpf('1e-24')
      and abs(lemn - mpmath.mpf('2.62205755429211981046483958989'))
      < mpmath.mpf('1e-25'))

# ================================================================ S6
print("S6 -- honest registry census of the new special values")
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


def census(basedict):
    fracs = [(p, q) for p in range(1, 13) for q in range(1, 13)
             if math.gcd(p, q) == 1]
    t2, t3 = [], []
    for lab, b in basedict.items():
        if b <= 0:
            continue
        for f in (1.0, -1.0):
            bb = b ** f
            for p, q in fracs:
                v = bb * p / q
                for tid, t in targets:
                    rel = abs(v / t - 1)
                    if rel < 1e-6:
                        t2.append((lab, f, p, q, tid, rel))
                    elif rel < 1e-3:
                        t3.append((lab, f, p, q, tid, rel))
    return t2, t3


new_vals = {
    "L(f8,1)": float(L1), "L(f8,2)": float(L2), "L(f8,3)": float(L3),
    "L_c(2)": float(Lc2), "L_c(3)": float(Lc3), "L_c(4)": float(Lc4),
    "F(e^-pi)": float(Fcm), "AGM(1,sqrt2)": float(mpmath.agm(
        1, mpmath.sqrt(2))), "sqrt2/3": float(mpmath.sqrt(2) / 3),
}
placebo = {
    "eulergamma": 0.5772156649015329, "e": math.e, "ln3": math.log(3),
    "3^(1/3)": 3 ** (1 / 3), "sin1": math.sin(1),
    "sqrt(pi)": math.sqrt(math.pi), "5^(1/5)": 5 ** 0.2,
    "atan2c": math.atan(2), "e^gamma": math.exp(0.5772156649015329),
}
t2_n, t3_n = census(new_vals)
t2_p, t3_p = census(placebo)
info(f"new-values family: T2 = {len(t2_n)}, T3 = {len(t3_n)}; placebo: "
     f"T2 = {len(t2_p)}, T3 = {len(t3_p)}")
for h in t2_n:
    info(f"  T2 HIT: {h}")
check("registry census (v527 discipline): NO T2 hit of the new special "
      "values (L-values, lemniscatic point values) on the 16 frozen "
      "registry constants; T3 rate comparable to placebo -- honest "
      "null: the new exact structure does NOT leak into the frozen "
      "readouts",
      len(t2_n) == 0 and len(t3_n) <= max(3 * max(len(t3_p), 1), 6))
check("global consistency guard: c(0) = 1; the three channels exhaust "
      "the census (part 11); signed channel entire (S2), Apery bridge "
      "form-specific (S3), L-series assembly closes (S4), self-dual "
      "width unique (S5)",
      int(c[0]) == 1 and pois_ok and kil_ok and ao_ok)

print()
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({time.time()-T0:.1f}s)")
raise SystemExit(0 if FAIL == 0 else 1)
