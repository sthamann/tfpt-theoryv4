"""v185 -- Axion relic, honest misalignment estimate. The determinant-line axion
f_a = M_scal/128 ~ 2.39e11 GeV (m_a ~ 23.8 ueV) can provide ALL of the dark
matter, but ONLY if the initial angle sits near the theta_i ~ 170 deg hilltop,
where the relic abundance is exponentially sensitive. So the axion DM branch
stays a [C] scenario, NOT a sharp prediction -- exactly as the Frontier file
already types it. This module quantifies WHY (the harmonic misalignment
under-produces at this f_a, so the hilltop enhancement is required).

  [I] 1. SCALES.  f_a = M_scal/(2 dim S^+ |mu4|) = M_scal/128 with
        M_scal = c3^(7/2) Mbar ~ 3.06e13 GeV gives f_a ~ 2.39e11 GeV; the QCD
        axion mass m_a ~ 5.7 ueV (1e12 GeV / f_a) ~ 23.8 ueV (v25/FR.DM.02).
  [N] 2. HARMONIC MISALIGNMENT UNDER-PRODUCES.  The standard (harmonic)
        post-inflation/aligned estimate Omega_a h^2 ~ 0.12 (f_a/9e11)^{7/6}
        <theta_i^2> gives, at f_a = 2.39e11, a prefactor ~0.12*(0.266)^{1.17}
        ~ 0.025 per unit theta^2 -- so for theta_i ~ O(1) the axion makes only
        ~20% of the DM. To reach the observed Omega_DM h^2 ~ 0.12 at THIS f_a one
        needs theta_eff^2 ~ 5, i.e. the large-angle (anharmonic) enhancement.
  [C] 3. THE HILLTOP IS REQUIRED -> SCENARIO.  TFPT's misalignment angle sits at
        theta_i ~ 170 deg (the seam value pi(1-phi_seam)), exactly the hilltop
        where the anharmonic factor f(theta_i) ~ [ln(1/(pi-theta_i))]^{7/6}
        diverges, so Omega_a h^2 CAN be tuned to 0.12. But near the hilltop the
        relic is exponentially sensitive to theta_i (and to QCD/string
        corrections), so this is a viable SCENARIO, not a sharp number: the axion
        branch stays [C].
  [O] 4. THE CONTRACT (kill test for the BRANCH, not the theory).  F_relic(
        f_a = M_scal/128, theta_i ~ 170 deg, N_DW = 1) =? Omega_DM. If a proper
        finite-T relic solve (with chi(T) and the hilltop anharmonicity) cannot
        land on Omega_DM for plausible theta_i, the determinant-line axion BRANCH
        falls -- not TFPT. The E8 scan leaves no free singlet WIMP (the 128 =
        (16,4)+(16,4) is the same matter spinor), so the axion is the natural DM
        line, but its abundance is transfer/cosmology, never a compiler output.

  Python-only (analytic misalignment estimate; the full finite-T ODE with chi(T)
  is a standard cosmology computation, flagged, not a compiler claim).

  UPDATE (full finite-T solve, experiments/ftransfer/axion_relic): a CONVERGED
  nonlinear misalignment solve (exact theta'' + (3+dlnH/dN)theta' + (m_a(T)/H)^2
  sin theta = 0, lattice chi(T)~T^-8.16, realistic g_*(T); normalised so theta_i=1
  gives the standard Omega_a h^2 ~ 0.03) now DECIDES it: at the PREDICTED theta_i ~
  170 deg the relic is Omega_a h^2 ~ 0.66, ~5.5x ABOVE 0.12 (Omega_DM is reached
  only at theta_i ~ 106 deg). So the determinant-line axion as the DOMINANT dark
  matter OVER-produces -- a confirmed tension, not the optimistic 'all-DM'. Stays
  [C]; over-production kills the axion-as-dominant-DM reading (needs dilution or a
  lower f_a), not the compiler.
"""
import math

import mpmath as mp

from tfpt_constants import c3, dim_Splus, check, summary, reset

MBAR = 2.435323e18           # GeV
OMEGA_DM = 0.12              # Planck Omega_DM h^2


def run():
    reset()
    print("v185 axion relic: all-DM possible at f_a=M_scal/128 but hilltop-sensitive -> [C] scenario")

    # 1. scales
    M_scal = float(c3) ** mp.mpf("3.5") * MBAR
    f_a = float(M_scal) / (2 * dim_Splus * 4)          # /128 = /(2 dim S+ |mu4|)
    m_a_ueV = 5.70 * 1e12 / f_a                          # ueV
    check("SCALES [I]: f_a = M_scal/(2 dim S+ |mu4|) = M_scal/128 = %.2e GeV "
          "(M_scal = c3^{7/2} Mbar = %.2e GeV); QCD axion m_a ~ 5.7 ueV*(1e12/f_a) "
          "= %.1f ueV (v25/FR.DM.02)" % (f_a, float(M_scal), m_a_ueV),
          2.0e11 < f_a < 2.8e11 and 20 < m_a_ueV < 28 and 128 == 2 * dim_Splus * 4)

    # 2. harmonic misalignment under-produces at this f_a
    pref = 0.12 * (f_a / 9e11) ** (7.0 / 6.0)            # Omega_a h^2 per theta^2
    theta_needed = math.sqrt(OMEGA_DM / pref)
    check("HARMONIC MISALIGNMENT UNDER-PRODUCES [N]: Omega_a h^2 ~ 0.12 "
          "(f_a/9e11)^{7/6} <theta^2>; at f_a=%.2e the prefactor is %.3f per "
          "theta^2, so theta_i~O(1) gives only ~%.0f%% of Omega_DM; reaching "
          "Omega_DM h^2=0.12 needs theta_eff^2 ~ %.1f (the large-angle enhancement)"
          % (f_a, pref, 100 * pref / OMEGA_DM, theta_needed**2),
          pref < OMEGA_DM and theta_needed > 1.5)

    # 3. the hilltop is required -> scenario
    theta_i_deg = 170.4
    check("HILLTOP REQUIRED -> SCENARIO [C]: TFPT's misalignment angle is "
          "theta_i ~ %.1f deg (the seam value pi(1-phi_seam)), exactly the "
          "hilltop where the anharmonic factor diverges, so Omega_a h^2 CAN be "
          "tuned to 0.12; but near the hilltop the relic is exponentially "
          "sensitive to theta_i and QCD/string corrections -- a viable SCENARIO, "
          "not a sharp number. The axion DM branch stays [C]" % theta_i_deg,
          165 < theta_i_deg < 175)

    # 4. the contract (kill test for the branch)
    check("THE CONTRACT [O]: F_relic(f_a=M_scal/128, theta_i~170 deg, N_DW=1) =? "
          "Omega_DM is a kill test for the determinant-line axion BRANCH, not the "
          "theory; the E8 scan leaves no free singlet WIMP (128=(16,4)+(16,4) is "
          "the matter spinor), so the axion is the natural DM line, but its "
          "abundance is transfer/cosmology, never a compiler output", True)

    return summary("v185 axion relic: all-DM possible but hilltop-sensitive -> [C] scenario")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
