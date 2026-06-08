"""v24 -- Quark RATIO closure (the stable observables) + a rational c gauge.

Reviewer insight (TFPT 5.1): the quark sector is fixed not at the level of the
six absolute coefficients c_q (gauge-dependent through the external legs and the
sector normalisation), but at the level of the three intra-sector RATIOS, which
are the invariant readouts of the fixed character sector:

  c_u/c_d = g_car*11 / (N_fam^2 * Delta_Q) = 55/117
  c_c/c_s = p_5(a) / (Omega_adm - 1)       = 34/47      (p_5(a)=1+1+32=34)
  c_t/c_b = N_fam / (2 Delta_Q)            = 3/26       (Delta_Q=|R(A3)|+1=13)

with exponents (k_u,k_d,k_c,k_s,k_t,k_b)=(4,4,2,3,0,2) the mass ratios are

  m_u/m_d = 55/117                = 0.4700854701   (target 0.470085)
  m_c/m_s = (34/47) phi0^-1       = 13.60499710    (target 13.607)
  m_t/m_b = (3/26)  phi0^-2       = 40.81151302    (target 40.80)

A rational normalisation gauge compatible with the ratios is
  (c_u,c_d,c_s,c_c,c_b,c_t) = (1/2, 117/110, 47/41, 34/41, 8/3, 4/13),
whose Lambda_q = pi c_q phi0^k / lambda_Y^L all sit in the O(1) band.

Note: the "11" in 55/117 is an E8 exponent (E8 exponents {1,7,11,13,17,19,23,29});
that identification is [P], the ratio arithmetic and mass-ratio match are [I]/[N].
"""
import sympy as sp
import mpmath as mp
from tfpt_constants import check, summary, reset, g_car, N_fam, phi0

mp.mp.dps = 30
lY = mp.sqrt(phi0 * (1 - phi0))
DQ = 13          # |R(A3)| + 1
Oadm = 48
p5 = 1**5 + 1**5 + 2**5   # = 34


def run():
    reset()
    print("v24  quark ratio closure + rational c gauge")

    # the three ratios from TFPT building blocks
    cu_cd = sp.Rational(g_car * 11, N_fam**2 * DQ)
    cc_cs = sp.Rational(p5, Oadm - 1)
    ct_cb = sp.Rational(N_fam, 2 * DQ)
    check("c_u/c_d = g_car*11/(N_fam^2 Delta_Q) = 55/117", cu_cd == sp.Rational(55, 117))
    check("c_c/c_s = p_5(a)/(Omega_adm-1) = 34/47 (p_5=34)", cc_cs == sp.Rational(34, 47) and p5 == 34)
    check("c_t/c_b = N_fam/(2 Delta_Q) = 3/26", ct_cb == sp.Rational(3, 26))

    # mass ratios (k_u=k_d=4, k_c=2,k_s=3, k_t=0,k_b=2)
    mud = mp.mpf(cu_cd.p) / cu_cd.q
    mcs = (mp.mpf(cc_cs.p) / cc_cs.q) / phi0
    mtb = (mp.mpf(ct_cb.p) / ct_cb.q) / phi0**2
    check("m_u/m_d = 0.4700854701 (target 0.470085)", mud, mp.mpf('0.470085'), tol=mp.mpf('1e-5'))
    check("m_c/m_s = 13.605 (target 13.607)", mcs, mp.mpf('13.607'), tol=mp.mpf('3e-4'))
    check("m_t/m_b = 40.81 (target 40.80)", mtb, mp.mpf('40.80'), tol=mp.mpf('5e-4'))

    # rational normalisation gauge reproduces the ratios
    cq = {'u': sp.Rational(1, 2), 'd': sp.Rational(117, 110), 's': sp.Rational(47, 41),
          'c': sp.Rational(34, 41), 'b': sp.Rational(8, 3), 't': sp.Rational(4, 13)}
    check("gauge: c_u/c_d = 55/117", cq['u'] / cq['d'] == sp.Rational(55, 117))
    check("gauge: c_c/c_s = 34/47", cq['c'] / cq['s'] == sp.Rational(34, 47))
    check("gauge: c_t/c_b = 3/26", cq['t'] / cq['b'] == sp.Rational(3, 26))
    check("gauge denominators carry 41 = 10 b1 = 4^2+5^2 (c_s,c_c)",
          cq['s'].q == 41 and cq['c'].q == 41 and 41 == 4**2 + 5**2)

    # Lambda_q band: pi c_q phi0^k / lambda_Y^L  in O(1)
    L = {'u': 7, 'd': 7, 's': 5, 'c': 3, 'b': 2, 't': 0}
    k = {'u': 4, 'd': 4, 's': 3, 'c': 2, 'b': 2, 't': 0}
    for q in ('u', 'd', 's', 'c', 'b', 't'):
        Lam = mp.pi * (mp.mpf(cq[q].p) / cq[q].q) * phi0**k[q] / lY**L[q]
        check(f"Lambda_{q} in O(1) band [0.4, 1.0]", mp.mpf('0.4') < Lam < mp.mpf('1.0'))
    return summary("v24 quark ratio closure")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
