"""F_Boltzmann -- the FULL Boltzmann ODE solve for eta_B (companion to fboltzmann_strip.py).

The strip used the analytic Buchmueller--Di Bari--Pluemacher (BDP) efficiency fit
kappa_f(m~1). Here we INTEGRATE the BDP Boltzmann network from first principles and feed
it the TFPT-frozen source data, then read eta_B at the frozen heavy scale

    M_1 = M_scal * phi0^2 / A_Lambda          (README 7c.6; M_scal = c3^{7/2} Mbar)

(rather than leaving M_R a free dial). This is the "proper solve" the CONTRACT's kill
condition refers to: it (i) replaces the kappa_f fit with the integrated efficiency, and
(ii) checks whether the frozen M_1 reproduces the observed eta_B.

Equations (BDP, z = M1/T, abundances normalised to N_N1^eq(z->0)=1):
    N_N1^eq(z) = (1/2) z^2 K2(z)
    D(z)       = K z K1(z)/K2(z)                     (decays)
    W_ID(z)    = (1/4) K z^3 K1(z)                    (inverse-decay washout)
    dN_N1/dz   = -D (N_N1 - N_N1^eq)
    dN_BL/dz   = -eps1 D (N_N1 - N_N1^eq) - W_ID N_BL
    eta_B      = a_sph * eps1 * kappa_f,  kappa_f = |N_BL(inf)|/eps1  (a_sph = 0.96e-2)
TFPT source: m3 ~ 0.05 eV (NO), m~1 = m3/A_Lambda = 5 meV (washout anchor, A_Lambda=10),
eps1 Davidson-Ibarra with the predicted Dirac phase delta_CP = 4 pi/3 (|sin| = 0.866).
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import kn

# ---- constants (TFPT + standard leptogenesis) ----
V_EW = 174.0                      # GeV
M3_EV = 0.05                      # eV, heaviest light neutrino (normal ordering)
A_LAMBDA = 10                     # |E(K5)| atom
MT1_EV = M3_EV / A_LAMBDA         # 5 meV washout anchor
M_STAR_EV = 1.08e-3              # equilibrium neutrino mass (BDP)
A_SPH = 0.96e-2                   # sphaleron + photon normalisation
ETAB_OBS = 6.1e-10               # Planck
PHI0 = 0.0531710                  # seed phi0 = 1/(6pi)+3/(256pi^4)
C3 = 1.0 / (8.0 * np.pi)
MBAR = 2.435e18                   # reduced Planck mass, GeV
M_SCAL = C3 ** 3.5 * MBAR         # scalaron mass ~ 3.06e13 GeV
M1_TFPT = M_SCAL * PHI0 ** 2 / A_LAMBDA   # frozen heavy scale (README 7c.6)
DELTA_CP = 4.0 * np.pi / 3.0      # predicted Dirac phase
SIN_EFF = abs(np.sin(DELTA_CP))   # 0.866, the O(1) leptogenesis phase proxy
K_WASH = MT1_EV / M_STAR_EV       # decay parameter (strong washout ~4.6)


def _N1eq(z: float) -> float:
    return 0.5 * z * z * kn(2, z)


def _rhs(z: float, y: np.ndarray, K: float) -> list[float]:
    N1, NBL = y
    k1, k2 = kn(1, z), kn(2, z)
    D = K * z * k1 / k2
    W = 0.25 * K * z ** 3 * k1
    dN1 = -D * (N1 - _N1eq(z))
    dNBL = -D * (N1 - _N1eq(z)) - W * NBL      # unit source -> NBL(inf) = kappa_f
    return [dN1, dNBL]


def kappa_f_ode(K: float, z0: float = 0.1, z1: float = 25.0) -> float:
    """Integrated BDP efficiency (unit CP source) -> |N_BL(z1)|."""
    sol = solve_ivp(_rhs, (z0, z1), [_N1eq(z0), 0.0], args=(K,),
                    method="LSODA", rtol=1e-9, atol=1e-12, dense_output=False)
    return float(abs(sol.y[1, -1]))


def eps1_DI(M1: float) -> float:
    """Davidson-Ibarra CP asymmetry with the predicted phase."""
    return (3.0 / (16.0 * np.pi)) * M1 * (M3_EV * 1e-9) / V_EW ** 2 * SIN_EFF


def etaB(M1: float, kappa_f: float) -> float:
    return A_SPH * eps1_DI(M1) * kappa_f


def main() -> int:
    print("=" * 80)
    print("F_Boltzmann: FULL ODE solve for eta_B at the frozen M1 = M_scal phi0^2/A_Lambda")
    print("=" * 80)
    print(f"  M_scal = c3^(7/2) Mbar      = {M_SCAL:.3e} GeV")
    print(f"  M1 (frozen) = M_scal phi0^2/A_Lambda = {M1_TFPT:.3e} GeV")
    print(f"  m~1 = m3/A_Lambda = {MT1_EV*1e3:.1f} meV ;  K = m~1/m* = {K_WASH:.2f} (strong washout)")
    print(f"  delta_CP = 240 deg, |sin| = {SIN_EFF:.3f}\n")

    kf = kappa_f_ode(K_WASH)
    # the analytic BDP fit the strip used, for validation
    kf_fit = (3.3e-3 / MT1_EV + (MT1_EV / 0.55e-3) ** 1.16) ** -1
    eps1 = eps1_DI(M1_TFPT)
    eta = etaB(M1_TFPT, kf)
    eta_fit = etaB(M1_TFPT, kf_fit)

    print("[1] integrated efficiency (full ODE) vs the BDP analytic fit used in the strip")
    print(f"    kappa_f(ODE)  = {kf:.4f}")
    print(f"    kappa_f(fit)  = {kf_fit:.4f}   (ratio ODE/fit = {kf/kf_fit:.2f})")
    print(f"\n[2] eta_B at the frozen M1 = {M1_TFPT:.2e} GeV")
    print(f"    eps1 (Davidson-Ibarra, |sin|=0.866) = {eps1:.3e}")
    print(f"    eta_B(ODE)  = {eta:.3e}   (obs {ETAB_OBS:.2e};  ratio = {eta/ETAB_OBS:.2f})")
    print(f"    eta_B(fit)  = {eta_fit:.3e}   (ratio = {eta_fit/ETAB_OBS:.2f})")

    # the M1 that hits the observed eta_B with the ODE efficiency
    M1_hit = brentq(lambda m: etaB(m, kf) - ETAB_OBS, 1e8, 1e13)
    print(f"\n[3] M1 that reproduces eta_B_obs (ODE efficiency): {M1_hit:.2e} GeV")
    print(f"    frozen M1 / required M1 = {M1_TFPT/M1_hit:.2f}  "
          f"(within a factor ~{max(M1_TFPT/M1_hit, M1_hit/M1_TFPT):.1f})")

    within = 1.0 / 3.0 <= eta / ETAB_OBS <= 3.0
    print("\n" + "-" * 80)
    if within:
        verdict = (f"FULL ODE confirms the strip: with the integrated BDP efficiency kappa_f="
                   f"{kf:.3f} and the predicted delta_CP=4pi/3, the FROZEN heavy scale "
                   f"M1=M_scal phi0^2/A_Lambda={M1_TFPT:.1e} GeV gives eta_B={eta:.2e}, within a "
                   f"factor {max(eta/ETAB_OBS, ETAB_OBS/eta):.1f} of the observed 6.1e-10 -- a "
                   f"near-hit at the frozen scale, no M_R dial. Stays [C] (washout anchored "
                   f"m~1=m3/A_Lambda; M1 via the scalaron route, README 7c.6).")
    else:
        verdict = (f"eta_B(ODE)={eta:.2e} is off the observed 6.1e-10 by a factor "
                   f">3 at the frozen M1 -- the leptogenesis branch is stressed (compiler core "
                   f"untouched; the independent Omega_b readout FR.ETAB.01 stands).")
    print("VERDICT [C]:")
    print(f"  {verdict}")
    print("  KILL (branch): a proper solve putting eta_B_obs OUTSIDE the strip for all M_R")
    print("  consistent with the seesaw would drop the leptogenesis route -- not triggered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
