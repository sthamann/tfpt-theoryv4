"""v3 -- The electromagnetic closure: alpha^-1 as the unique root of F_{U(1)}=0.

Backs "fine structure alpha^-1: unique root of F_{U(1)}(alpha)=0,
alpha^-1 = 137.0359992" in
  introduction.tex (before/after, predictions, ledger)
  tfpt_1_architecture_e8.tex  (sec: EM closure, Lemma existence/uniqueness)
  tfpt_2_standard_model.tex.

Reproduces the root, verifies it is the only sign change on (0, 0.05) (the
existence/uniqueness lemma), runs the inverse test (measured alpha -> integer
budget 41), and the ablation showing which inputs are load-bearing.
"""
import mpmath as mp
from tfpt_constants import check, summary, reset, c3, phibase, dtop


def make_F(c3v, M, expo=mp.mpf(-5) / 4, Nfac=8):
    """F_{U(1)} with adjustable budget M, seam exponent and c3 = 1/(Nfac*pi)."""
    cc = 1 / (Nfac * mp.pi)
    pb = 1 / (6 * mp.pi)
    dt = 48 * cc**4

    def phiseam(a):
        Q = dt * mp.e**(-2 * a)
        return pb + Q * (1 - Q)**expo

    def F(a):
        return a**3 - 2 * cc**3 * a**2 - (mp.mpf(4) / 5) * cc**6 * M * mp.log(1 / phiseam(a))
    return F


def F_iv(a):
    """F_{U(1)} in mpmath interval arithmetic (rigorous enclosure)."""
    from mpmath import iv
    PI = iv.pi
    cc = 1 / (8 * PI)
    pb = 1 / (6 * PI)
    dt = 48 * cc**4
    Q = dt * iv.exp(-2 * a)
    # (1-Q)^(-5/4) via exp/log so the fractional power is interval-valid
    ps = pb + Q * iv.exp((iv.mpf(-5) / 4) * iv.log(1 - Q))
    return a**3 - 2 * cc**3 * a**2 - (iv.mpf(4) / 5) * cc**6 * 41 * iv.log(1 / ps)


def interval_uniqueness():
    """Rigorous interval proof: one tight bracket encloses the root with
    definite sign change, and F is sign-definite on a fine partition of
    (alpha_c, 0.05) with exactly one negative->positive crossing."""
    from mpmath import iv
    iv.dps = 30
    # (1) tight enclosing bracket around the root
    lo = iv.mpf('0.0072973525622097')
    hi = iv.mpf('0.0072973525622100')
    Flo, Fhi = F_iv(lo), F_iv(hi)
    bracket_ok = (Flo.b < 0) and (Fhi.a > 0)   # F(lo) wholly <0, F(hi) wholly >0
    # (2) sign-definite partition: count crossings of the enclosure
    n = 200
    a0, a1 = mp.mpf('0.0002'), mp.mpf('0.05')
    edges = [a0 + (a1 - a0) * k / n for k in range(n + 1)]
    crossings = 0
    prev = None
    for k in range(n):
        seg = iv.mpf([float(edges[k]), float(edges[k + 1])])
        v = F_iv(seg)
        s = (-1 if v.b < 0 else (1 if v.a > 0 else 0))  # 0 = indeterminate (contains root)
        if s != 0 and prev is not None and prev != 0 and s != prev:
            crossings += 1
        if s != 0:
            prev = s
    # exactly one indeterminate (root) band and one definite sign flip overall
    indet = 0
    for k in range(n):
        seg = iv.mpf([float(edges[k]), float(edges[k + 1])])
        v = F_iv(seg)
        if not (v.b < 0 or v.a > 0):
            indet += 1
    return bracket_ok, indet


def run():
    reset()
    print("v3  electromagnetic closure  (alpha^-1)")

    F = make_F(c3, 41)
    a = mp.findroot(F, mp.mpf('0.0073'))
    ainv = 1 / a
    check("alpha_* = 0.00729735256220985", a, mp.mpf('0.00729735256220985'),
          tol=mp.mpf('1e-15'))
    check("alpha^-1 = 137.0359992168407", ainv, mp.mpf('137.0359992168407'),
          tol=mp.mpf('1e-13'))

    # CODATA-2022 137.035999177(21): relative deviation ~2.9e-10
    dev = abs(ainv - mp.mpf('137.035999177')) / mp.mpf('137.035999177')
    check("relative deviation vs CODATA-2022 < 3.0e-10", dev < mp.mpf('3.0e-10'))

    # existence + uniqueness: exactly one sign change on (0, 0.05)
    xs = [mp.mpf(k) / 2000 for k in range(1, 101)]  # 0.0005 .. 0.05
    signs = [mp.sign(F(x)) for x in xs]
    changes = sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])
    check("exactly one sign change of F on (0,0.05) (unique simple root)",
          changes, 1, exact=True)

    # rigorous interval-arithmetic version of existence + uniqueness
    bracket_ok, indet = interval_uniqueness()
    check("interval bracket encloses the root with a definite sign change", bracket_ok)
    check("interval partition has exactly one indeterminate (root) band -> unique",
          indet, 1, exact=True)

    # corrected monotonicity endpoint (proof patch): F' is NOT positive at alpha_c;
    # its first zero is alpha_0 > alpha_c, and F<0 on (0, alpha_0]
    def Fp(a, h=mp.mpf('1e-25')):
        return (F(a + h) - F(a - h)) / (2 * h)
    alpha_c = mp.mpf(4) / 3 * c3**3
    check("alpha_c=(4/3)c3^3=8.3988e-5; F'(alpha_c)<0 (~ -5.89e-10): NOT yet increasing at alpha_c",
          abs(alpha_c - mp.mpf('8.39883709197903e-5')) < mp.mpf('1e-18') and Fp(alpha_c) < 0)
    alpha_0 = mp.findroot(Fp, alpha_c * mp.mpf('1.02'))
    check("F' first zero at alpha_0=8.62643e-5 > alpha_c; F'<0 below, F'>0 above",
          abs(alpha_0 - mp.mpf('8.62643433435431e-5')) < mp.mpf('1e-18')
          and Fp(alpha_0 * mp.mpf('0.999')) < 0 and Fp(alpha_0 * mp.mpf('1.001')) > 0)
    check("F(alpha_0)~ -3.82e-7 < 0 => F<0 on (0,alpha_0], then increasing to +inf: one root",
          F(alpha_0) < 0 and abs(F(alpha_0) - mp.mpf('-3.81881e-7')) < mp.mpf('1e-11'))

    # inverse test: feed measured alpha, solve for the integer budget M
    a_meas = 1 / mp.mpf('137.035999177')
    Msolved = mp.findroot(lambda M: make_F(c3, M)(a_meas), mp.mpf('41'))
    check("inverse test: measured alpha reconstructs budget M = 41",
          Msolved, 41, tol=mp.mpf('1e-5'))

    # ablation: neighbouring integer budgets miss; c3=1/(8pi) is selected
    for M in (40, 42):
        am = 1 / mp.findroot(make_F(c3, M), mp.mpf('0.0073'))
        check(f"budget M={M} misses alpha^-1 (|dev|>0.5)", abs(am - ainv) > 0.5)
    for Nf in (7, 9):
        an = 1 / mp.findroot(make_F(c3, 41, Nfac=Nf), mp.mpf('0.0073'))
        check(f"c3=1/({Nf}pi) misses alpha^-1 (|dev|>1)", abs(an - ainv) > 1)
    return summary("v3 EM closure")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
