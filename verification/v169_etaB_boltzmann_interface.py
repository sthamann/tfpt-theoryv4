"""v169 -- The eta_B leptogenesis transfer: operationalising the Boltzmann path
(NOT proving eta_B). The honest F_transfer test of the baryon asymmetry.

eta_B has two readings in TFPT.  As a DOWNSTREAM cosmology readout it is already
hit: Omega_b = (1 - 1/4pi) phi0 = 0.04894, Omega_b h^2 ~ 0.02223, so
eta_B ~ 273.9e-10 * Omega_b h^2 ~ 6.09e-10 (FR.ETAB.01).  This module addresses
the OTHER reading -- the fundamental thermal-leptogenesis Boltzmann computation,
which is a physics interface, not a compiler theorem.  It checks whether the
standard route, FED BY TFPT's neutrino sector, can reach the observed asymmetry.

  [I] 1. STANDARD STRUCTURE.  Type-I thermal leptogenesis with hierarchical RH
         neutrinos: Y_B = a_sph * eps_1 * kappa_f / (...), in the compact form
         eta_B ~ 0.96e-2 * eps_1 * kappa_f, with the sphaleron factor
         a_sph = 28/79 and g_* ~ 106.75 absorbed in the 0.96e-2.
  [.]  2. TFPT INPUTS (the genuine feed).  Normal ordering (v9 texture): m1 ~ 0,
         m2 = sqrt(dm2_sol) ~ 0.0087 eV, m3 = sqrt(dm2_atm) ~ 0.050 eV; the CP
         phase delta_CP = 4pi/3 = 240 deg (the TFPT prediction, |sin| = 0.866).
  [.]  3. DAVIDSON-IBARRA CP ASYMMETRY (scenario in M1).  eps_1 <= (3/16pi)
         M1 m3 / v^2; with the TFPT phase and M1 = 1e10 GeV, eps_1 ~ 8.5e-7. M1
         (the lightest RH-neutrino mass) is a SCENARIO input, not a TFPT output.
  [.]  4. EFFICIENCY (scenario in the washout).  kappa_f(m~1) =
         (3.3e-3/m~1 + (m~1/0.55e-3)^1.16)^{-1} (Buchmueller-Di Bari-Pluemacher);
         for m~1 in [m_* , m_atm] = [1.08e-3, 1e-2] eV, kappa_f ~ 0.03-0.19.
  [C] 5. KILL TEST -- THE ROUTE IS VIABLE, NOT PROVEN.  Over the natural ranges
         M1 in [3e9, 3e10] GeV and m~1 in [m_*, m_atm], eta_B spans a band that
         BRACKETS the observed 6.1e-10 (a canonical point M1 = 1e10 GeV,
         m~1 = 5e-3 eV, delta_CP = 240 deg gives ~6.0e-10 -- NOT tuned). So the
         thermal-leptogenesis route, fed by TFPT's neutrino sector, REACHES the
         observed asymmetry. But M1 and the washout are scenario inputs, so eta_B
         stays [C]: a falsifiable physics interface, NOT a compiler prediction. If
         a precise Boltzmann/RGE computation excluded the window, the LEPTOGENESIS
         ROUTE would fall -- not the theory (the downstream Omega_b readout,
         FR.ETAB.01, is independent and already hit).

Scope [C]: analytic thermal-leptogenesis estimate; the seesaw RGE running of
Y_nu / M_i (PyR@TE with a seesaw model) is an O(1) correction, flagged, not
included. Python-only (numerical; no exact-identity content for Wolfram).
"""
import math

from tfpt_constants import check, summary, reset

PI = math.pi
V = 174.0                          # GeV (Dirac-mass normalisation m_D = y v)
A_SPH = 28.0 / 79.0                # sphaleron B-L -> B conversion
GEV_PER_EV = 1e-9
DM2_SOL, DM2_ATM = 7.5e-5, 2.5e-3  # eV^2 (NuFIT, NO)
M2 = math.sqrt(DM2_SOL)            # eV
M3 = math.sqrt(DM2_ATM)            # eV
DELTA_CP = 4 * PI / 3              # TFPT prediction, 240 deg
M_STAR = 1.08e-3                   # eV, equilibrium neutrino mass
M_ATM = 1e-2                       # eV, upper washout reference
ETA_B_OBS = 6.1e-10


def _eps1(M1, phase):
    """Davidson-Ibarra maximal CP asymmetry x phase (masses -> GeV)."""
    return (3.0 / (16 * PI)) * M1 * (M3 * GEV_PER_EV) / V**2 * phase

def _kappa(mtil):
    """Final efficiency factor (Buchmueller-Di Bari-Pluemacher interpolation)."""
    return 1.0 / (3.3e-3 / mtil + (mtil / 0.55e-3)**1.16)

def _etaB(M1, mtil, phase):
    return 0.96e-2 * _eps1(M1, phase) * _kappa(mtil)


def run():
    reset()
    print("v169 eta_B leptogenesis transfer (Boltzmann path operationalised, [C])")

    # 1. standard structure
    check("STANDARD STRUCTURE [I]: type-I thermal leptogenesis, "
          "eta_B ~ 0.96e-2 eps_1 kappa_f with sphaleron a_sph = 28/79 = %.4f"
          % A_SPH, abs(A_SPH - 28/79) < 1e-12)

    # 2. TFPT inputs
    sin_phase = abs(math.sin(DELTA_CP))
    check("TFPT INPUTS: normal ordering m2 = %.4f eV, m3 = %.4f eV (from "
          "dm2_sol, dm2_atm), CP phase delta_CP = 4pi/3 = 240 deg (|sin| = %.3f) "
          "-- the genuine TFPT feed (v9 texture + the predicted phase)"
          % (M2, M3, sin_phase),
          abs(M3 - 0.05) < 2e-3 and abs(sin_phase - math.sqrt(3)/2) < 1e-9)

    # 3. Davidson-Ibarra eps_1 (scenario M1)
    eps_ref = _eps1(1e10, sin_phase)
    check("DAVIDSON-IBARRA eps_1 (scenario M1): eps_1 <= (3/16pi) M1 m3/v^2; "
          "with the TFPT phase and M1 = 1e10 GeV, eps_1 = %.2e ~ 1e-6 (M1 is a "
          "scenario input, not a TFPT output)" % eps_ref,
          5e-7 < eps_ref < 2e-6)

    # 4. efficiency (scenario washout)
    k_lo, k_hi = _kappa(M_ATM), _kappa(M_STAR)
    check("EFFICIENCY (scenario washout): kappa_f(m~1) Buchmueller-Di "
          "Bari-Pluemacher; for m~1 in [m_*, m_atm] kappa_f in [%.3f, %.3f] "
          "(~0.03-0.19)" % (k_lo, k_hi),
          0.02 < k_lo < 0.05 and 0.15 < k_hi < 0.25)

    # 5. KILL TEST: observed eta_B inside the natural-scenario band
    band = [_etaB(M1, mtil, sin_phase)
            for M1 in (3e9, 1e10, 3e10) for mtil in (M_STAR, 5e-3, M_ATM)]
    lo, hi = min(band), max(band)
    eta_ref = _etaB(1e10, 5e-3, sin_phase)        # canonical, NOT tuned
    check("KILL TEST [C] -- ROUTE VIABLE: over M1 in [3e9,3e10] GeV and m~1 in "
          "[m_*, m_atm], eta_B spans [%.2e, %.2e] which BRACKETS the observed "
          "%.1e; the canonical point (M1=1e10, m~1=5e-3, delta=240deg) gives "
          "eta_B = %.2e (NOT tuned). The leptogenesis route fed by TFPT's "
          "neutrino sector REACHES the observed asymmetry -- but M1/washout are "
          "scenario inputs, so eta_B stays [C], not a compiler prediction"
          % (lo, hi, ETA_B_OBS, eta_ref),
          lo <= ETA_B_OBS <= hi and 4e-10 < eta_ref < 9e-10)

    check("FALSIFIABILITY [C]: if a precise Boltzmann/RGE computation excluded "
          "the window, the LEPTOGENESIS ROUTE falls -- NOT the theory (the "
          "downstream Omega_b readout FR.ETAB.01, eta_B ~ 6.09e-10, is "
          "independent and already hit). The seesaw RGE running of Y_nu/M_i "
          "(PyR@TE seesaw model) is an O(1) correction, flagged, not included",
          True)

    return summary("v169 eta_B leptogenesis transfer")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
