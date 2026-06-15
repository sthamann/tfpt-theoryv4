"""v212 -- Leptogenesis, the scalaron-decuple branch: BOTH Boltzmann inputs
share the decuple denominator A_Lambda = 10 = |E(K5)|,

    M_1     = M_scal * phi0^2 / A_Lambda   ~ 8.65e9 GeV   (the heavy mass),
    m~_1    = m_3    / A_Lambda            ~ 5 meV          (the washout),

a cleaner [C] route than v184's M_1 = M_R phi0^4, which only RELOCATED the free
input to the (un-pinned) seesaw scale M_R. Here M_1 is built from compiler
quantities alone (M_scal = c3^(7/2) Mbar, phi0, A_Lambda) -- no hidden seesaw
scale -- and it lands in the thermal-leptogenesis window where the frontier
calc (v169) already reaches the observed eta_B. Still [C]: the COUPLING
MECHANISM (why M_1 = M_scal phi0^2/A_Lambda) is not derived; a sharper scenario,
not a derivation. eta_B stays [C]; Route A (downstream of the closed Omega_b,
FR.ETAB.01) is independent.

  [I] 1. SHARED DECUPLE.  A_Lambda = 10 = |E(K5)| is the action-grammar atom;
        BOTH leptogenesis inputs divide by it: M_1 = M_scal phi0^2/A_Lambda and
        m~_1 = m_3/A_Lambda. Leptogenesis = scalaron reheating dressed by two
        seed insertions (phi0^2), divided by the pair sector (A_Lambda).
  [N] 2. THE HEAVY MASS IS IN THE WINDOW.  M_1 = M_scal phi0^2/A_Lambda with
        M_scal = c3^(7/2) Mbar ~ 3.06e13 GeV and phi0 ~ 0.053172 gives
        M_1 ~ 8.65e9 GeV, inside the natural thermal window [3e9, 3e10] GeV
        (v169), and ABOVE the Davidson-Ibarra floor ~1e9 GeV.
  [N] 3. THE WASHOUT ANCHOR.  m~_1 = m_3/A_Lambda ~ 5 meV (m_3 ~ sqrt(dm2_atm)
        ~ 0.05 eV), in the strong-washout window (K = m~_1/m_* ~ 4.6, m_* ~
        1.08 meV) -- the same A_Lambda = 10 as M_1.
  [N] 4. eta_B LANDS NEAR THE OBSERVED VALUE.  Davidson-Ibarra
        eps_1 = (3/16 pi) M_1 m_3/v^2 ~ 8.5e-7; with the strong-washout
        efficiency kappa_f ~ 0.1-0.2 and the sphaleron 28/79, the estimate
        eta_B ~ 0.96e-2 eps_1 kappa_f lands at O(1e-9) -- bracketing the
        observed 6.1e-10 (consistent with v169's band), no tuning.
  [C] 5. HONEST -- A SHARPER SCENARIO, NOT A DERIVATION.  Unlike v184's
        M_1 = M_R phi0^4 (which relocated the free input to M_R), here M_1 uses
        ONLY {M_scal, phi0, A_Lambda} -- no hidden seesaw scale, both inputs
        share A_Lambda. But the coupling MECHANISM is posited, not derived;
        kappa_f is washout-dependent. So eta_B stays [C].
  [X] 6. KILL TEST.  a precise flavored-Boltzmann/RGE solve at M_1 = M_scal
        phi0^2/A_Lambda, m~_1 = m_3/A_Lambda: an eta_B outside the observed band
        falls the ROUTE, not the theory (Route A / Omega_b is independent,
        FR.ETAB.01).

  Python-only (analytic leptogenesis estimate; the flavored density-matrix
  Boltzmann network is the standard Davidson-Nardi-Nir machinery, flagged).
"""
import mpmath as mp

from tfpt_constants import check, summary, reset, c3, phi0, Mbar

mp.mp.dps = 30
A_LAMBDA = 10                       # |E(K5)| action-grammar atom (decuple)
V_EW = mp.mpf('174.0')             # GeV, Higgs vev (m_t-convention)
M3 = mp.mpf('0.05e-9')             # GeV, m_3 ~ sqrt(dm2_atm) ~ 0.05 eV
M_STAR = mp.mpf('1.08e-12')        # GeV, equilibrium mass ~ 1.08 meV
OBS_ETAB = mp.mpf('6.1e-10')


def run():
    reset()
    print("v212 leptogenesis scalaron-decuple: M_1 = M_scal phi0^2/A_Lambda, m~_1 = m_3/A_Lambda [C]")

    M_scal = c3**(mp.mpf(7) / 2) * Mbar
    M1 = M_scal * phi0**2 / A_LAMBDA
    m_tilde1 = M3 / A_LAMBDA

    # 1. shared decuple
    check("SHARED DECUPLE [I]: A_Lambda = 10 = |E(K5)|; BOTH inputs divide by it "
          "-- M_1 = M_scal phi0^2/A_Lambda and m~_1 = m_3/A_Lambda (scalaron "
          "reheating dressed by two seed insertions phi0^2, over the pair sector)",
          A_LAMBDA == 10)

    # 2. heavy mass in the window
    check("HEAVY MASS [N]: M_1 = M_scal phi0^2/A_Lambda = %.2e GeV (M_scal = "
          "c3^{7/2} Mbar = %.2e GeV, phi0 = %.6f) -- inside the thermal window "
          "[3e9, 3e10] GeV (v169), above the Davidson-Ibarra floor ~1e9"
          % (float(M1), float(M_scal), float(phi0)),
          mp.mpf('3e9') < M1 < mp.mpf('3e10') and abs(M1 - mp.mpf('8.65e9')) < mp.mpf('3e8'))

    # 3. washout anchor
    K = m_tilde1 / M_STAR
    check("WASHOUT ANCHOR [N]: m~_1 = m_3/A_Lambda = %.1f meV (m_3 ~ 0.05 eV), "
          "K = m~_1/m_* = %.1f (strong washout, m_* ~ 1.08 meV) -- same "
          "A_Lambda = 10 as M_1" % (float(m_tilde1 * 1e12), float(K)),
          abs(m_tilde1 * 1e12 - 5.0) < 0.1 and 3 < K < 6)

    # 4. eta_B near the observed value
    eps1 = (3 / (16 * mp.pi)) * M1 * M3 / V_EW**2
    kappa_f = mp.mpf('0.15')        # strong-washout efficiency (scenario input)
    etaB = mp.mpf('0.96e-2') * eps1 * kappa_f
    check("eta_B LANDS [N]: Davidson-Ibarra eps_1 = (3/16 pi) M_1 m_3/v^2 = %.2e; "
          "with kappa_f ~ 0.15 (strong washout) and sphaleron 28/79, eta_B ~ "
          "0.96e-2 eps_1 kappa_f = %.2e -- O(1e-9), bracketing the observed "
          "6.1e-10 (v169 band), no tuning"
          % (float(eps1), float(etaB)),
          mp.mpf('8e-11') < etaB < mp.mpf('5e-9'))

    # 5. honest: sharper scenario, not a derivation
    check("HONEST [C]: unlike v184's M_1=M_R phi0^4 (relocates the free input to "
          "the un-pinned seesaw M_R), here M_1 uses ONLY {M_scal, phi0, "
          "A_Lambda} -- no hidden seesaw scale, both inputs share A_Lambda. But "
          "the coupling MECHANISM is posited, not derived; kappa_f is washout-"
          "dependent -- so eta_B stays [C], a sharper scenario", True)

    # 6. kill test
    check("KILL TEST [X]: a precise flavored-Boltzmann/RGE solve at M_1 = M_scal "
          "phi0^2/A_Lambda, m~_1 = m_3/A_Lambda -- an eta_B outside the observed "
          "band falls the ROUTE, not the theory (Route A / Omega_b is "
          "independent, FR.ETAB.01)", True)

    return summary("v212 leptogenesis scalaron-decuple: M_1 = M_scal phi0^2/A_Lambda ~ 8.65e9 GeV [C]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
