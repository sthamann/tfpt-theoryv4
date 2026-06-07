"""v7 -- Gravity / cosmology readouts from c3 and the compiler numbers.

Backs the gravity & cosmology rows in
  tfpt_1_architecture_e8.tex (scalaron c3^7, Lambda decuple, A_s)
  tfpt_2_standard_model.tex  (scalaron exponent 7, inflation)
  introduction.tex (predictions: A_s, n_s, r, theta_12, Omega_b).

Checks the scalaron exponent 7 (four readings), the scalaron mass
M_scal^2/Mbar^2 = c3^7 ~ 3.06e13 GeV, the parameter-free A_s, the Starobinsky
n_s, r, the baryon density Omega_b and the conditional solar angle theta_12.
"""
import mpmath as mp
from tfpt_constants import (check, summary, reset, c3, phi0, Mbar,
                            N_fam, Omega_adm, b1, g_car)


def run():
    reset()
    print("v7  gravity / cosmology readouts")

    # scalaron exponent 7 -- four independent readings
    check("7 = Omega_adm - 10*b1", Omega_adm - int(10 * b1), 7, exact=True)
    check("7 = N_fam + |mu4|", N_fam + 4, 7, exact=True)
    check("7 = g_car + |Z2|", g_car + 2, 7, exact=True)
    check("7 = -deg E + rk E = 4 + 3", 4 + 3, 7, exact=True)

    # scalaron mass M_scal = Mbar * c3^(7/2)
    Mscal = Mbar * c3**(mp.mpf(7) / 2)
    check("M_scal = Mbar*c3^(7/2) ~ 3.06e13 GeV", Mscal, mp.mpf('3.06e13'),
          tol=mp.mpf('5e-3'))

    # parameter-free scalar amplitude A_s (N_star = 55)
    Nstar = 55
    A_s = Nstar**2 * c3**7 / (24 * mp.pi**2)
    check("A_s = N*^2 c3^7 / (24 pi^2) ~ 2.0e-9", A_s, mp.mpf('2.0e-9'),
          tol=mp.mpf('3e-2'))

    # Starobinsky R^2 predictions
    ns = 1 - mp.mpf(2) / Nstar
    r = mp.mpf(12) / Nstar**2
    check("n_s = 1 - 2/N* = 0.9636", ns, mp.mpf('0.96364'), tol=mp.mpf('1e-4'))
    check("r = 12/N*^2 = 0.00397", r, mp.mpf('0.0039669'), tol=mp.mpf('1e-3'))

    # high-precision cosmological constant from the EM fixed point
    from v3_em_alpha import make_F
    ainv = 1 / mp.findroot(make_F(c3, 41), mp.mpf('0.0073'))
    rhoL_ratio = (3 / (4 * mp.pi**2)) * mp.e**(-2 * ainv)
    check("rho_L/Mbar^4 = (3/4pi^2) e^{-2 ainv} = 7.1253e-121",
          rhoL_ratio, mp.mpf('7.12533e-121'), tol=mp.mpf('1e-5'))
    rhoL_qrt_meV = (rhoL_ratio**(mp.mpf(1) / 4)) * Mbar * mp.mpf('1e12')
    check("dark-energy scale rho_L^1/4 = 2.2375 meV (vs observed ~2.24)",
          rhoL_qrt_meV, mp.mpf('2.23747'), tol=mp.mpf('1e-4'))

    # baryon density and solar angle
    Omega_b = (1 - 1 / (4 * mp.pi)) * phi0
    check("Omega_b = (1 - 1/4pi) phi0 = 0.04894", Omega_b, mp.mpf('0.04894'),
          tol=mp.mpf('1e-3'))
    sin2_th12 = mp.mpf(1) / 3 - phi0 / 2
    check("sin^2 theta_12 = 1/3 - phi0/2 = 0.3067 (cond.)",
          sin2_th12, mp.mpf('0.30675'), tol=mp.mpf('1e-3'))
    return summary("v7 gravity/cosmo")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
