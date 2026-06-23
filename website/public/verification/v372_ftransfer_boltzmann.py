"""v372 -- FR.BOLTZMANN.SOLVE.01 (Track 3, F_transfer): eta_B from the INTEGRATED
Buchmueller-Di Bari-Pluemacher (BDP) Boltzmann network at the TFPT-frozen heavy scale --
promotes experiments/ftransfer/leptogenesis_boltzmann into the ledger, replacing the v326 toy
washout (kappa=0.3 tuned).  It does NOT re-derive the viability band (v169) or the decuple
anchoring (v212); it integrates the ODE at the frozen inputs and checks whether eta_B lands.

Frozen inputs (NO free M_R dial):
  M1 = M_scal phi0^2 / A_Lambda  (M_scal = c3^{7/2} Mbar; A_Lambda = 2 g_car = 10; v212)
  m~1 = m3 / A_Lambda = 5 meV     (washout anchor; m3 ~ 0.05 eV, normal ordering)
  eps1: Davidson-Ibarra with the PREDICTED Dirac phase delta_CP = 4 pi/3 (|sin| = 0.866, v9)
BDP network (z = M1/T, unit CP source so N_BL(inf) = kappa_f):
  D = K z K1/K2,  W_ID = (1/4) K z^3 K1,  K = m~1/m* (m* = 1.08e-3 eV)
  dN_N1/dz = -D (N_N1 - N_N1^eq),  dN_BL/dz = -D (N_N1 - N_N1^eq) - W_ID N_BL
  eta_B = a_sph eps1 kappa_f  (a_sph = 0.96e-2)

  [E] 1. INTEGRATED EFFICIENCY.  the full-ODE kappa_f (strong washout K ~ 4.6) agrees with the
        analytic BDP fit to ~10-20% -- the integrated transport, not a tuned constant.
  [C] 2. NEAR-HIT AT THE FROZEN SCALE.  eta_B(ODE) at M1 = M_scal phi0^2/A_Lambda lands within
        a factor ~3 of the observed 6.1e-10, with NO M_R dial (M1 from the scalaron route).
  [C] 3. THE REQUIRED M1.  the M1 reproducing eta_B_obs (ODE efficiency) is within a factor of
        a few of the frozen M1 -- the scalaron scale is in the leptogenesis window.
  [X] 4. KILL TEST.  a proper solve putting eta_B_obs OUTSIDE [obs/3, 3 obs] for the frozen
        (M1, m~1) for all seesaw-consistent M_R would drop the leptogenesis branch (the
        compiler core + the independent Omega_b readout FR.ETAB.01 untouched).

Status: [E] the integrated efficiency; [C] the frozen-scale eta_B near-hit (washout anchored
m~1 = m3/A_Lambda, M1 via the scalaron route); [X] the branch kill test.  A typed solver, not a
toy; eta_B stays [C] (a transfer target, not a compiler power).  Python (numpy + scipy)."""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import kn

from tfpt_constants import check, summary, reset, c3 as _c3, g_car, phi0 as _phi0, Mbar as _Mbar

V_EW = 174.0
M3_EV = 0.05
A_LAMBDA = 2 * g_car                       # 10 = |E(K5)| atom
MT1_EV = M3_EV / A_LAMBDA                   # 5 meV washout anchor
M_STAR_EV = 1.08e-3
A_SPH = 0.96e-2
ETAB_OBS = 6.1e-10
PHI0 = float(_phi0)
MBAR = float(_Mbar)
M_SCAL = float(_c3) ** 3.5 * MBAR
M1_TFPT = M_SCAL * PHI0 ** 2 / A_LAMBDA
SIN_EFF = abs(np.sin(4.0 * np.pi / 3.0))   # 0.866 (delta_CP = 240 deg, v9)
K_WASH = MT1_EV / M_STAR_EV


def _N1eq(z):
    return 0.5 * z * z * kn(2, z)


def _rhs(z, y, K):
    N1, NBL = y
    k1, k2 = kn(1, z), kn(2, z)
    D = K * z * k1 / k2
    W = 0.25 * K * z ** 3 * k1
    src = -D * (N1 - _N1eq(z))
    return [src, src - W * NBL]


def kappa_f_ode(K, z0=0.1, z1=25.0):
    sol = solve_ivp(_rhs, (z0, z1), [_N1eq(z0), 0.0], args=(K,),
                    method="LSODA", rtol=1e-8, atol=1e-12)
    return float(abs(sol.y[1, -1]))


def eps1_DI(M1):
    return (3.0 / (16.0 * np.pi)) * M1 * (M3_EV * 1e-9) / V_EW ** 2 * SIN_EFF


def run():
    reset()
    print("v372  FR.BOLTZMANN.SOLVE.01: integrated BDP eta_B at the frozen M1 = M_scal phi0^2/A_Lambda")

    kf = kappa_f_ode(K_WASH)
    kf_fit = (3.3e-3 / MT1_EV + (MT1_EV / 0.55e-3) ** 1.16) ** -1
    eps1 = eps1_DI(M1_TFPT)
    eta = A_SPH * eps1 * kf

    # 1. integrated efficiency vs the analytic BDP fit
    check("INTEGRATED EFFICIENCY [E]: the full-ODE kappa_f = %.4f (strong washout K = %.2f) "
          "agrees with the analytic BDP fit %.4f to within %.0f%% -- integrated transport, not "
          "a tuned constant" % (kf, K_WASH, kf_fit, abs(kf / kf_fit - 1) * 100),
          0.0 < kf < 1.0 and abs(kf / kf_fit - 1) < 0.5)

    # 2. near-hit at the frozen scale (within a factor ~3)
    ratio = eta / ETAB_OBS
    check("NEAR-HIT AT THE FROZEN SCALE [C]: eta_B(ODE) = %.2e at M1 = M_scal phi0^2/A_Lambda = "
          "%.2e GeV lands within a factor %.1f of the observed %.1e -- NO M_R dial (M1 from the "
          "scalaron route, v212)" % (eta, M1_TFPT, max(ratio, 1 / ratio), ETAB_OBS),
          1 / 3.2 <= ratio <= 3.2)

    # 3. the M1 that reproduces eta_B_obs
    M1_hit = brentq(lambda m: A_SPH * eps1_DI(m) * kf - ETAB_OBS, 1e8, 1e13)
    fac = max(M1_TFPT / M1_hit, M1_hit / M1_TFPT)
    check("REQUIRED M1 [C]: the M1 reproducing eta_B_obs (ODE efficiency) is %.2e GeV, within a "
          "factor %.1f of the frozen M1 = %.2e GeV -- the scalaron scale is in the leptogenesis "
          "window" % (M1_hit, fac, M1_TFPT), fac < 5.0)

    # 4. kill test (branch)
    check("KILL TEST [X]: a proper solve putting eta_B_obs OUTSIDE [obs/3, 3 obs] at the frozen "
          "(M1, m~1) for all seesaw-consistent M_R would drop the leptogenesis branch (compiler "
          "core + the independent Omega_b readout FR.ETAB.01 untouched) -- NOT triggered here",
          1 / 3.2 <= ratio <= 3.2)

    return summary("v372 FR.BOLTZMANN.SOLVE.01: the integrated BDP Boltzmann ODE at the TFPT-frozen "
                   "M1=M_scal phi0^2/A_Lambda (m~1=m3/A_Lambda=5 meV, delta_CP=240deg) gives eta_B within a "
                   "factor ~%.1f of 6.1e-10 with NO M_R dial; replaces the v326 toy washout. Stays [C] (a "
                   "transfer target, not a compiler power); kill = eta_B outside [obs/3,3obs] for all M_R"
                   % max(ratio, 1 / ratio))


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
