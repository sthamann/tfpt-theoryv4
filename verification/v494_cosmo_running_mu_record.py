"""v494 -- COSMO.RUNNING.01 / COSMO.MUDIST.01: the two 2026-07-20 prediction-of-record
rows (spectral-index running alpha_s/beta_s and the CMB mu-distortion branch
discriminator) promoted to machine-checked verification.

The Starobinsky branch is already load-bearing (v7/v28/v86: n_s = 1 - 2/N_star,
r = 12/N_star^2, A_s = N_star^2 c3^7/(24 pi^2)).  This module adds the SAME
branch's next two observables so the paper/website prediction surfaces are
machine-backed:

  [E] LEADING-ORDER IDENTITIES (sympy exact, no floats):
        alpha_s = dn_s/dln k = -2/N_star^2 = -r/6      (LO)
        beta_s  = d alpha_s/dln k = -4/N_star^3        (LO; NOT -8/N^3)
      using d ln k = -dN at leading order.
  [E] EXACT SLOW ROLL on the Einstein-frame Starobinsky potential
      V = V0 (1 - e^{-sqrt(2/3) phi})^2 (third-order SR, Lyth-Riotto),
      cross-checked by a finite difference along ln k:
        alpha_s(N=51.4) = -7.09e-4,  beta_s(51.4) = -2.70e-5;
        exact-SR band edges alpha_s(50) = -7.48e-4, alpha_s(60) = -5.23e-4;
        LO band over N_star in [50,60]: [-8.0e-4, -5.6e-4].
  [C] DATA CONFRONTATION (external data, no marker upgrade):
        Planck 2018 TTTEEE+lowE+lensing  alpha_s = -0.0045 +/- 0.0067 -> +0.57 sigma;
        P-ACT-LB (ACT DR6+Planck+lensing+DESI BAO) +0.0062 +/- 0.0052 -> -1.33 sigma;
        beta_s (Planck run+runrun) 0.010 +/- 0.013 -> -0.77 sigma.
      KILL: robust alpha_s < -5e-3 or > +3e-3 at >= 5 sigma; any robust
      POSITIVE running kills the plateau branch (plateau potentials give
      alpha_s < 0).
  [C] MU-DISTORTION BRANCH DISCRIMINATOR (Chluba-Erickcek-Ben-Dayan k-space
      window, calibrated on the LCDM Planck-2018 anchor to the literature
      mu_LCDM ~ 2.0e-8, a +21% window correction):
        sharp branch N_star = 51.4 (A_s = 1.76e-9): mu ~ 1.6e-8;
        profiled record N_star = 56.1 (A_s = 2.10e-9): mu ~ 2.0e-8 (1.94e-8);
        band N_star in [50,60]: 1.5e-8 .. 2.3e-8;
        branch split Delta mu = 3.0e-9 (raw window; calibrated 3.7e-9)
        => >= 3 sigma A_s/N_star branch decision at sigma(mu) = 1e-9
        (Voyage-2050 class); the PIXIE baseline limit 9e-8 does NOT reach the
        band (sharp = 0.18 x limit); FIRAS 9e-5 is 4 dex above.
      KILL: robust mu < 0.9e-8 or > 4e-8.
  [E] COMB BLINDNESS IN THE MU WINDOW (honest S15 typing): the frozen recovery
      log-comb (omega = 2 pi/ln((3/2)^6) = 2.5827, eps = e^{-pi^2/ln((3/2)^6)}
      = 0.0173) is STRUCTURALLY invisible here -- window attenuation
      |F(omega)| = 0.033, delta mu = 7.4e-12 = 0.007 sigma even at Voyage-2050
      sensitivity.  The theory itself predicts where it cannot be seen; no
      comb-search row is opened.

HONEST FENCES (do not oversell):
  * N_star REMAINS an external reheating input (GATE.NSTAR.01); the frozen
    band [50, 60] stays the prediction surface of record (v84/v86); the sharp
    point 51.4 is the conditional [P] reheating point.
  * All data confrontations are [C] external-data rows (scorecard stage
    prediction_of_record); nothing here closes a gate or moves a marker.
  * The Chluba window is imported standard physics; the +21% calibration is
    anchored on the LCDM literature value, not fitted to TFPT.

Origin: experiments/tfpt-discovery/alpha_s_running_probe.py and
mu_distortion_probe.py (2026-07-20 scorecard round), promoted 2026-07-21.
Python: sympy exact (LO identities) + numpy (SR solve, window quadrature);
the quadrature/ODE parts are numerical, Python-only by the suite convention.
"""
import numpy as np
import sympy as sp
import mpmath as mp
from tfpt_constants import check, summary, reset, c3, PI

SQ23 = np.sqrt(2.0 / 3.0)
K_PIVOT = 0.05                                    # 1/Mpc
N_SHARP = 51.4                                    # v86 reheating point
N_PROF = 56.1                                     # A_s-profiled record branch
LAMBDA_DSI = (3.0 / 2.0) ** 6
OMEGA = 2.0 * np.pi / np.log(LAMBDA_DSI)          # frozen comb kernel
EPS_COMB = np.exp(-np.pi ** 2 / np.log(LAMBDA_DSI))
MU_LCDM_LIT = 2.0e-8                              # literature LCDM mu (Chluba)

# ---------- Starobinsky potential + third-order slow roll (M_pl = 1) --------


def _V(phi):
    return (1.0 - np.exp(-SQ23 * phi)) ** 2


def _dV(phi):
    e = np.exp(-SQ23 * phi)
    return 2.0 * SQ23 * e * (1.0 - e)


def _d2V(phi):
    e = np.exp(-SQ23 * phi)
    return (4.0 / 3.0) * e * (2.0 * e - 1.0)


def _d3V(phi):
    e = np.exp(-SQ23 * phi)
    return (4.0 / 3.0) * SQ23 * e * (1.0 - 4.0 * e)


def _d4V(phi):
    e = np.exp(-SQ23 * phi)
    return (8.0 / 9.0) * e * (8.0 * e - 1.0)


def _sr_params(phi):
    v, v1, v2, v3, v4 = _V(phi), _dV(phi), _d2V(phi), _d3V(phi), _d4V(phi)
    eps = 0.5 * (v1 / v) ** 2
    eta = v2 / v
    xi2 = v1 * v3 / v ** 2
    sig3 = v1 ** 2 * v4 / v ** 3
    return eps, eta, xi2, sig3


def _observables(phi):
    """Third-order slow-roll n_s, r, alpha_s, beta_s (Lyth-Riotto)."""
    eps, eta, xi2, sig3 = _sr_params(phi)
    ns = 1.0 - 6.0 * eps + 2.0 * eta
    r = 16.0 * eps
    alpha = 16.0 * eps * eta - 24.0 * eps ** 2 - 2.0 * xi2
    beta = (-192.0 * eps ** 3 + 192.0 * eps ** 2 * eta - 32.0 * eps * eta ** 2
            - 24.0 * eps * xi2 + 2.0 * eta * xi2 + 2.0 * sig3)
    return ns, r, alpha, beta


def _phi_end():
    lo, hi = 0.1, 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _sr_params(mid)[0] > 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _efolds(phi, phi_e):
    xs = np.linspace(phi_e, phi, 20001)
    return np.trapezoid(_V(xs) / _dV(xs), xs)


def _phi_of_N(n_target, phi_e):
    lo, hi = phi_e, 12.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _efolds(mid, phi_e) < n_target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------- Chluba k-space window for mu (khat = k * Mpc) --------------------

_LNK = np.linspace(np.log(1.0), np.log(1.0e6), 200001)
_KHAT = np.exp(_LNK)
_W_MU = np.exp(-_KHAT / 5400.0) - np.exp(-((_KHAT / 31.6) ** 2))


def _pzeta(a_s, ns, alpha):
    lnkr = _LNK - np.log(K_PIVOT)
    return a_s * np.exp((ns - 1.0) * lnkr + 0.5 * alpha * lnkr ** 2)


def _mu_window(a_s, ns, alpha):
    return 2.2 * np.trapezoid(_pzeta(a_s, ns, alpha) * _W_MU, _LNK)


def _As_tfpt(n):
    return float(n ** 2 * c3 ** 7 / (24 * PI ** 2))


def run():
    reset()
    print("v494 cosmo running + mu-distortion record "
          "(COSMO.RUNNING.01 / COSMO.MUDIST.01)")

    # ---- [E] leading-order identities, sympy exact --------------------------
    N = sp.symbols('N', positive=True)
    ns_lo = 1 - 2 / N
    r_lo = 12 / N ** 2
    alpha_lo = -sp.diff(ns_lo, N)          # d ln k = -dN at LO
    beta_lo = -sp.diff(alpha_lo, N)
    check("[E] LO identity alpha_s = dn_s/dlnk = -2/N^2 (sympy exact)",
          sp.simplify(alpha_lo + 2 / N ** 2) == 0)
    check("[E] LO identity alpha_s = -r/6 (sympy exact)",
          sp.simplify(alpha_lo + r_lo / 6) == 0)
    check("[E] LO identity beta_s = -4/N^3 (NOT -8/N^3; sympy exact)",
          sp.simplify(beta_lo + 4 / N ** 3) == 0)
    check("[E] LO band edges: alpha_s(50) = -8.00e-4, alpha_s(60) = -5.56e-4",
          sp.Rational(-2, 50 ** 2) == sp.Rational(-1, 1250)
          and abs(float(-2 / mp.mpf(60) ** 2) + 5.556e-4) < 1e-7)

    # ---- [E] exact slow roll on the Starobinsky potential --------------------
    phi_e = _phi_end()
    obs = {}
    for n_star in (50.0, N_SHARP, 60.0):
        obs[n_star] = _observables(_phi_of_N(n_star, phi_e))
    a_sharp, b_sharp = obs[N_SHARP][2], obs[N_SHARP][3]
    check("[E] exact-SR alpha_s(N=51.4) = -7.088e-4", a_sharp,
          mp.mpf('-7.0884e-4'), tol=mp.mpf('1e-3'))
    check("[E] exact-SR beta_s(N=51.4) = -2.702e-5", b_sharp,
          mp.mpf('-2.7020e-5'), tol=mp.mpf('1e-3'))
    check("[E] exact-SR band edges alpha_s(50) = -7.482e-4, "
          "alpha_s(60) = -5.234e-4",
          abs(obs[50.0][2] / -7.4824e-4 - 1) < 1e-3
          and abs(obs[60.0][2] / -5.2337e-4 - 1) < 1e-3)

    # finite-difference cross-check along ln k = -N + (1/2) ln(V/3)
    pts = []
    for n_star in (N_SHARP - 0.5, N_SHARP + 0.5):
        phi = _phi_of_N(n_star, phi_e)
        pts.append((-n_star + 0.5 * np.log(_V(phi) / 3.0),
                    _observables(phi)[0]))
    alpha_fd = (pts[1][1] - pts[0][1]) / (pts[1][0] - pts[0][0])
    check("[E] finite-difference dn_s/dlnk = exact-SR alpha_s to < 1%",
          abs(alpha_fd / a_sharp - 1) < 1e-2)

    # ---- [C] data confrontation (external data; no marker moves) ------------
    check("[C] Planck 2018 (-0.0045 +/- 0.0067): TFPT pull = +0.57 sigma",
          (a_sharp - (-0.0045)) / 0.0067, mp.mpf('0.57'), tol=mp.mpf('2e-2'))
    check("[C] P-ACT-LB (+0.0062 +/- 0.0052): TFPT pull = -1.33 sigma "
          "(record leg; watch channel)",
          (a_sharp - 0.0062) / 0.0052, mp.mpf('-1.33'), tol=mp.mpf('2e-2'))
    check("[C] beta_s vs Planck run+runrun (0.010 +/- 0.013) = -0.77 sigma",
          (b_sharp - 0.010) / 0.013, mp.mpf('-0.77'), tol=mp.mpf('2e-2'))
    check("[C] kill margin: LO band edge -8.0e-4 sits 4.2e-3 INSIDE the "
          "negative kill edge -5e-3; any robust POSITIVE running kills the "
          "plateau branch",
          obs[50.0][2] > -5e-3 and a_sharp < 0)

    # ---- [C] mu-distortion branch discriminator ------------------------------
    mu_lcdm = _mu_window(2.10e-9, 0.9649, 0.0)
    cal = MU_LCDM_LIT / mu_lcdm
    check("[C] window calibration on the LCDM anchor: mu_win(LCDM) = 1.65e-8 "
          "-> cal = +21% (the scorecard's '+20% to the full computation')",
          cal, mp.mpf('1.209'), tol=mp.mpf('2e-2'))

    mu_sharp_raw = _mu_window(_As_tfpt(N_SHARP), 1 - 2 / N_SHARP,
                              -2 / N_SHARP ** 2)
    mu_prof_raw = _mu_window(2.10e-9, 1 - 2 / N_PROF, -2 / N_PROF ** 2)
    mu_50 = cal * _mu_window(_As_tfpt(50.0), 1 - 2 / 50.0, -2 / 50.0 ** 2)
    mu_60 = cal * _mu_window(_As_tfpt(60.0), 1 - 2 / 60.0, -2 / 60.0 ** 2)
    check("[C] sharp branch (N=51.4, A_s=1.76e-9): mu = 1.6e-8 (calibrated)",
          cal * mu_sharp_raw, mp.mpf('1.6e-8'), tol=mp.mpf('2e-2'))
    check("[C] profiled record (N=56.1, A_s=2.10e-9): mu = 1.94e-8 (~2.0e-8)",
          cal * mu_prof_raw, mp.mpf('1.94e-8'), tol=mp.mpf('2e-2'))
    check("[C] band N in [50,60]: mu in [1.5e-8, 2.3e-8]",
          abs(mu_50 / 1.5e-8 - 1) < 2e-2 and abs(mu_60 / 2.3e-8 - 1) < 2e-2)
    check("[C] branch split Delta mu = 3.0e-9 (raw window; calibrated 3.7e-9) "
          "=> >= 3 sigma at sigma(mu) = 1e-9 (Voyage-2050 class)",
          mu_prof_raw - mu_sharp_raw, mp.mpf('3.03e-9'), tol=mp.mpf('2e-2'))
    check("[C] branch ratio mu_profiled/mu_sharp = 1.23 (the 23% split)",
          mu_prof_raw / mu_sharp_raw, mp.mpf('1.232'), tol=mp.mpf('1e-2'))
    check("[C] PIXIE baseline |mu| < 9e-8 does NOT reach the band "
          "(sharp = 0.18 x limit); FIRAS 9e-5 is 4 dex above",
          cal * mu_sharp_raw / 9e-8 < 0.25
          and cal * mu_sharp_raw / 9e-5 < 1e-3)

    # ---- [E] comb blindness in the mu window (S15 honest typing) -------------
    check("[E] frozen comb kernel omega = 2 pi/ln((3/2)^6) = 2.5827, "
          "eps = 0.0173",
          abs(OMEGA - 2.5827) < 1e-4 and abs(EPS_COMB - 0.017302) < 1e-5)
    lnkr = _LNK - np.log(K_PIVOT)
    p0w = _pzeta(_As_tfpt(N_SHARP), 1 - 2 / N_SHARP,
                 -2 / N_SHARP ** 2) * _W_MU
    base = np.trapezoid(p0w, _LNK)
    f_att = np.hypot(np.trapezoid(p0w * np.cos(OMEGA * lnkr), _LNK),
                     np.trapezoid(p0w * np.sin(OMEGA * lnkr), _LNK)) / base
    dmu_comb = EPS_COMB * f_att * mu_sharp_raw
    check("[E] window attenuation |F(2.5827)| = 0.033 (vs 0.70 at omega=0.5)",
          f_att, mp.mpf('0.033'), tol=mp.mpf('3e-2'))
    check("[E] comb blindness: delta mu = 7.4e-12 = 0.007 sigma even at "
          "Voyage-2050 (structurally invisible; no comb-search row opened)",
          dmu_comb, mp.mpf('7.4e-12'), tol=mp.mpf('2e-2'))

    # ---- fences ---------------------------------------------------------------
    check("[O] fence: N_star stays an external reheating input "
          "(GATE.NSTAR.01); the frozen band [50,60] stays the surface of "
          "record; the sharp point is the conditional v86 [P] reading",
          50.0 < N_SHARP < 60.0 and 50.0 < N_PROF < 60.0)

    return summary("v494 cosmo running + mu record")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
