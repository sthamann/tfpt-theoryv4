"""v206 -- The cosmological-constant Letter branch: the seam number
delta_Sigma = m_1 e^{-2 pi alpha^-1/3} with the lowest-block identification
m_1 = Omega_adm = 48, the reduced/unreduced Planck convention split, and the
quantitative late-time Hubble closure H0 = 66.5..67.1 (archive integration of
the tfpt-31 cosmological-constant note). This SHARPENS the qualitative
'H0 vs Lambda' prediction row into a number and is cross-checked against the
already-mirrored 123-orders split (v60).

  [N] 1. THE SEAM NUMBER (Fredholm leading).  delta_Sigma^lead =
        Omega_adm e^{-2 pi alpha^-1/3} = 48 e^{-2 pi*137.036/3} ~ 1.09e-123.
  [E] 2. CONVENTION SPLIT.  rho_Lambda = M_Pl^4 delta_Sigma (unreduced) vs
        rho_Lambda,red = Mbar^4 delta_Sigma (reduced); the ratio is exactly
        M_Pl^4/Mbar^4 = (8 pi)^2 = 631.65 -- the two must be displayed, never
        silently interchanged (the numerically most sensitive point).
  [N] 3. DENSITY.  rho_Lambda = M_Pl^4 delta_Sigma ~ 2.4e-47 GeV^4, of the
        observed vacuum-energy order (~2.5e-47 GeV^4).
  [N] 4. 123-ORDERS CROSS-LINK.  |log10 delta_Sigma| = 2 pi alpha^-1/(3 ln10)
        - log10(48) ~ 122.96, consistent with the v60 split 122.948 =
        119.028 + 3.920 -- same Lambda hierarchy, two independent forms.
  [C] 5. HUBBLE CLOSURE (recorded readouts).  under the flatness closure the
        Letter reports H0^lead = 66.51 and (discrete gap-equation route)
        H0^disc = 67.10 km/s/Mpc -- a span 66.5..67.1 sitting 1.6..0.5 sigma
        BELOW Planck (67.36 +- 0.54) and far below SH0ES (73.0 +- 1.0). HONEST:
        the Hubble tension is NOT relieved by dialing the asymptotic vacuum
        scale upward. The full flatness solve uses imported Omega_b, omega_DM
        (external cosmology), so H0 is a [C] readout, not a from-nothing output.

  Python-only (numerical cosmology; the exact (8 pi)^2 ratio is the only
  algebraic part and is already on the Wolfram path via the Planck-convention
  identity in v60).
"""
import mpmath as mp

from tfpt_constants import check, summary, reset, Omega_adm, Mbar

mp.mp.dps = 40
AINV = mp.mpf('137.0359992')          # retained IR alpha^-1 (CODATA-benchmarked)
H0_PLANCK_C, H0_PLANCK_S = mp.mpf('67.36'), mp.mpf('0.54')
H0_SHOES_C, H0_SHOES_S = mp.mpf('73.0'), mp.mpf('1.0')


def run():
    reset()
    print("v206 cosmological-constant branch: delta_Sigma, (8pi)^2 split, H0 = 66.5..67.1 [C]")

    # 1. the seam number (Fredholm leading, m_1 = Omega_adm)
    delta_Sigma = Omega_adm * mp.e**(-2 * mp.pi * AINV / 3)
    check("SEAM NUMBER [N]: delta_Sigma^lead = Omega_adm e^{-2 pi alpha^-1/3} "
          "= 48 e^{-2 pi*137.036/3} ~ 1.09e-123",
          delta_Sigma, mp.mpf('1.09e-123'), tol=mp.mpf('2e-2'))

    # 2. convention split (8 pi)^2
    M_Pl = Mbar * mp.sqrt(8 * mp.pi)
    ratio = (M_Pl / Mbar)**4
    check("CONVENTION SPLIT [E]: M_Pl^4/Mbar^4 = (8 pi)^2 = 631.65 "
          "(unreduced vs reduced Planck density -- must be displayed)",
          ratio, (8 * mp.pi)**2, tol=mp.mpf('1e-30'))
    check("(8 pi)^2 = 631.65 numerically", (8 * mp.pi)**2, mp.mpf('631.65'), tol=mp.mpf('1e-3'))

    # 3. density of the observed vacuum order
    rho_Lambda = M_Pl**4 * delta_Sigma
    check("DENSITY [N]: rho_Lambda = M_Pl^4 delta_Sigma ~ 2.4e-47 GeV^4 "
          "(observed vacuum order ~2.5e-47)",
          rho_Lambda, mp.mpf('2.4e-47'), tol=mp.mpf('5e-2'))

    # 4. 123-orders cross-link to v60
    log_dS = abs(mp.log(delta_Sigma, 10))
    check("123-ORDERS CROSS-LINK [N]: |log10 delta_Sigma| = 2 pi alpha^-1/(3 ln10) "
          "- log10(48) = %.2f, consistent with the v60 split 122.948" % float(log_dS),
          abs(log_dS - mp.mpf('122.95')) < mp.mpf('0.1'))

    # 5. Hubble closure (recorded readouts)
    H0_lead, H0_disc = mp.mpf('66.51'), mp.mpf('67.10')
    s_lead = (H0_lead - H0_PLANCK_C) / H0_PLANCK_S
    s_disc = (H0_disc - H0_PLANCK_C) / H0_PLANCK_S
    s_shoes = (H0_disc - H0_SHOES_C) / H0_SHOES_S
    check("HUBBLE CLOSURE [C]: H0 span 66.51 (lead) .. 67.10 (disc) sits "
          "%.2f .. %.2f sigma BELOW Planck (67.36 +- 0.54)"
          % (float(s_lead), float(s_disc)),
          mp.mpf('-1.7') < s_lead < mp.mpf('-1.4') and mp.mpf('-0.6') < s_disc < mp.mpf('-0.3'))
    check("HONEST [C]: TFPT H0 is %.1f sigma below SH0ES (73.0 +- 1.0) -- the "
          "Hubble tension is NOT relieved by raising the vacuum scale; H0 uses "
          "imported Omega_b, omega_DM (external), so it is a readout, not a "
          "from-nothing output" % float(s_shoes),
          s_shoes < mp.mpf('-5.0'))

    return summary("v206 cosmological-constant branch H0 = 66.5..67.1 [C]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
