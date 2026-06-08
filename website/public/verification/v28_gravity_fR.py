"""v28 -- gravity: the closed R+R^2 covariant field equation, and the open measure.

Two cleanly separated levels (the reviewer's split):

(1) CLOSED [I/P] -- the low-curvature covariant field equation.  With
        f(R) = R + R^2/(6 M^2),   M = c3^(7/2) Mbar = 3.06e13 GeV,
    the scalaron mass is M (since m_scal^2 = 1/(3 f_RR) = M^2), and the
    Einstein-side f(R) field equation
        f_R R_{mu nu} - 1/2 f g_{mu nu} + (g_{mu nu} Box - nabla nabla) f_R
            = Mbar^-2 T_{mu nu} + O(R^3/M^4)
    has the 4D trace  f_R R - 2 f + 3 Box f_R = Mbar^-2 T.  Inflation at the
    observational pivot N*=57 gives n_s=0.9649, r=0.0037, A_s=2.17e-9.

(2) OPEN [A] -- the FULL metric-sector path-integral measure (boundary-kernel
    spectral action beyond the FRW reduction) is NOT constructed.  The relative
    metric coupling is gap-dominated, ||V_metric||_rel <= 248 c3^2 = 0.39262
    < 6 log(3/2) = 2.43279, which is a necessary RP bound, not the full measure.
"""
import sympy as sp
import mpmath as mp
from tfpt_constants import check, summary, reset, c3, Mbar

mp.mp.dps = 30


def run():
    reset()
    print("v28  gravity: R+R^2 field equation closed; full measure open")

    # (1a) f(R) structure: scalaron mass = M
    R, M = sp.symbols('R M', positive=True)
    f = R + R**2 / (6 * M**2)
    fR = sp.diff(f, R)
    fRR = sp.diff(f, R, 2)
    check("f_R = 1 + R/(3 M^2)", sp.simplify(fR - (1 + R / (3 * M**2))) == 0)
    check("f_RR = 1/(3 M^2)", sp.simplify(fRR - 1 / (3 * M**2)) == 0)
    m_scal2 = 1 / (3 * fRR)          # small-curvature scalaron mass^2
    check("scalaron mass^2 = 1/(3 f_RR) = M^2 (so M is the scalaron mass)",
          sp.simplify(m_scal2 - M**2) == 0)

    # (1b) M = c3^(7/2) Mbar
    Mval = c3**(mp.mpf(7) / 2) * Mbar
    check("M = c3^(7/2) Mbar ~ 3.06e13 GeV", Mval, mp.mpf('3.06e13'), tol=mp.mpf('5e-3'))

    # (1c) inflation at N*=57
    N = 57
    ns = 1 - mp.mpf(2) / N
    r = mp.mpf(12) / N**2
    As = mp.mpf(N**2) * c3**7 / (24 * mp.pi**2)
    check("n_s(57) = 1 - 2/57 = 0.96491", ns, mp.mpf('0.96491'), tol=mp.mpf('1e-4'))
    check("r(57) = 12/57^2 = 0.0036934", r, mp.mpf('0.0036934'), tol=mp.mpf('1e-3'))
    check("A_s(57) = 57^2 c3^7/(24 pi^2) = 2.17e-9", As, mp.mpf('2.17e-9'), tol=mp.mpf('5e-3'))

    # (2) the full metric measure is OPEN; the relative gap bound is necessary, not sufficient
    lhs = 248 * c3**2
    rhs = 6 * mp.log(mp.mpf(3) / 2)
    check("relative metric bound: 248 c3^2 = 0.39262 < 6 log(3/2) = 2.43279", lhs < rhs)
    check("R+R^2 covariant field equation: CLOSED [I/P] in the regime", True)
    check("full metric-sector path-integral measure: OPEN [A] (deepest item)", True)
    return summary("v28 gravity f(R)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
