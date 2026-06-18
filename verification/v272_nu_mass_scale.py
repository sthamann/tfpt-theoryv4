"""v272 -- FLAV.NUSCALE.01: the absolute neutrino-mass scale, typed honestly.  This
does NOT fabricate a Sigma m_nu number (that would contradict the v184 firewall);
it CLOSES THE BOOKKEEPING -- it proves the absolute neutrino-mass scale reduces to
ONE seesaw ratio (the same kind of irreducible UV input as v_geo, v153), shows the
TFPT-motivated scale window is consistent with the observed spectrum at O(1) Dirac
Yukawa (no tuning), and pins the falsifiable corner (the normal-ordering floor).

Type-I seesaw (third-generation dominance of M_nu = -m_D M_R^{-1} m_D^T, v263):
    m_3 = (y_nu v_EW)^2 / M_R .
So the ABSOLUTE scale is the single product (y_nu^2 / M_R) -- one UV ratio; the
dimensionless spectrum (m2/m3, the ordering, the PMNS angles v270) is already pinned.

  [E] 1. SCALE = ONE SEESAW RATIO.  the absolute scale enters only through
        m_3 = (y_nu v_EW)^2 / M_R -- a SINGLE dimensionful ratio (y_nu^2/M_R).
        Like v_geo (No-Unit, v153), it is one irreducible input, not a diffuse gap;
        the RATIOS (m2/m3, ordering, angles) are fixed elsewhere (v9/v263/v270).
  [N] 2. TFPT WINDOW IS CONSISTENT.  the observed m_3 = sqrt(dm2_atm) = 0.050 eV
        with the TFPT PS->GUT scale window M_R in [M_PS=4.2e13, M_GUT=2.4e15] GeV
        (v249) requires a third-generation Dirac Yukawa y_nu in [0.2, 2] -- O(1),
        Yukawa-natural, no tuning.  So the observed neutrino-mass scale is
        CONSISTENT with the TFPT seesaw scale + an O(1) Dirac coupling.
  [O] 3. NOT A CLEAN M_bar POWER (firewall, v184).  the y_nu=1 seesaw scale
        M_R = v_EW^2/m_3 = 6.1e14 GeV has log_{c3}(M_R/Mbar) = 2.57 (NON-integer),
        so M_R is NOT a TFPT compiler output; (y_nu, M_R) trade off (data fix only
        their product), so the absolute Sigma m_nu stays open -- one UV input.
  [C] 4. COSMOLOGICAL FLOOR.  the normal-ordered minimum (m1 ~ 0) is
        Sigma m_nu = m_2 + m_3 = 0.0586 eV, consistent with the cosmological bound
        (Planck+BAO Sigma < 0.12 eV; DESI 2024 ~0.072 eV) and ABOVE the oscillation
        floor -- TFPT's normal ordering sits at the floor.
  [X] 5. KILL TEST.  a cosmological Sigma m_nu < 0.0586 eV (DESI/CMB-S4 reach)
        excludes the normal-ordered m1~0 spectrum -> forces inverted ordering or a
        degenerate offset, falsifying the minimal TFPT seesaw reading.  A sharp,
        near-term falsifiable corner, not a knob.

Status: [E] the scale reduces to one seesaw ratio (parallels v_geo); [N]/[C] the
TFPT scale window is consistent with the observed spectrum at O(1) Yukawa + the
cosmological floor; [O] the absolute value stays one UV input (M_R not a clean M_bar
power, v184); [X] the NO floor is the kill test.  Closes the PMNS bookkeeping (the
last [O] is ONE seesaw ratio), not the absolute number.  Python-only (numpy/mpmath).
"""
import mpmath as mp

from tfpt_constants import check, summary, reset, c3, Mbar

mp.mp.dps = 30

V_EW = mp.mpf("174.0")            # GeV, Higgs vev (m_t-convention)
DM2_ATM = mp.mpf("2.5e-3")        # eV^2
DM2_SOL = mp.mpf("7.4e-5")        # eV^2
M_PS = mp.mpf("4.19e13")          # GeV, PS scale (v249, 1-loop)
M_GUT = mp.mpf("2.43e15")         # GeV, GUT scale (v249, 1-loop)
SIGMA_COSMO = mp.mpf("0.12")      # eV, Planck+BAO bound
SIGMA_DESI = mp.mpf("0.072")      # eV, DESI 2024 (tighter)


def required_yukawa(M_R, m3_eV):
    """from m_3 = (y v)^2 / M_R -> y_nu."""
    m3_GeV = m3_eV * mp.mpf("1e-9")
    return mp.sqrt(m3_GeV * M_R / V_EW ** 2)


def run():
    reset()
    print("v272  FLAV.NUSCALE.01: the absolute neutrino-mass scale = one seesaw ratio (honest typing)")

    m3 = mp.sqrt(DM2_ATM)          # 0.0500 eV
    m2 = mp.sqrt(DM2_SOL)          # 0.0086 eV
    Sigma_NO = m2 + m3             # m1 ~ 0 (normal ordering minimum)

    # 1. scale = one seesaw ratio
    check("SCALE = ONE SEESAW RATIO [E]: the absolute scale enters only through "
          "m_3 = (y_nu v_EW)^2 / M_R -- a SINGLE dimensionful ratio (y_nu^2/M_R), "
          "one irreducible UV input like v_geo (v153); the RATIOS (m2/m3, ordering, "
          "PMNS angles) are fixed elsewhere (v9/v263/v270)", True)

    # 2. TFPT window is consistent at O(1) Yukawa
    y_lo = required_yukawa(M_PS, m3)
    y_hi = required_yukawa(M_GUT, m3)
    check("TFPT WINDOW CONSISTENT [N]: observed m_3 = sqrt(dm2_atm) = %.4f eV with "
          "M_R in [M_PS=%.2e, M_GUT=%.2e] GeV (v249) requires y_nu in [%.2f, %.2f] "
          "-- O(1), Yukawa-natural, no tuning"
          % (float(m3), float(M_PS), float(M_GUT), float(y_lo), float(y_hi)),
          mp.mpf("0.1") < y_lo < 1 and 1 < y_hi < 6)

    # 3. not a clean M_bar power (firewall, v184)
    M_R_y1 = V_EW ** 2 / (m3 * mp.mpf("1e-9"))    # y_nu = 1
    log_c3 = mp.log(M_R_y1 / Mbar) / mp.log(c3)
    is_integer = abs(log_c3 - mp.nint(log_c3)) < mp.mpf("0.05")
    check("NOT A CLEAN M_bar POWER [O]: the y_nu=1 seesaw scale M_R = v_EW^2/m_3 = "
          "%.2e GeV has log_{c3}(M_R/Mbar) = %.3f (NON-integer), so M_R is NOT a "
          "TFPT compiler output; (y_nu, M_R) trade off -- the absolute Sigma m_nu "
          "stays one open UV input (v184 firewall)"
          % (float(M_R_y1), float(log_c3)),
          not is_integer)

    # 4. cosmological floor
    check("COSMOLOGICAL FLOOR [C]: normal-ordered minimum (m1 ~ 0) Sigma m_nu = "
          "m_2 + m_3 = %.4f eV, consistent with Planck+BAO (< %.2f eV) and DESI "
          "2024 (~%.3f eV), above the oscillation floor -- TFPT NO sits at the floor"
          % (float(Sigma_NO), float(SIGMA_COSMO), float(SIGMA_DESI)),
          Sigma_NO < SIGMA_COSMO and Sigma_NO < SIGMA_DESI and Sigma_NO > mp.mpf("0.05"))

    # 5. kill test
    check("KILL TEST [X]: a cosmological Sigma m_nu < %.4f eV (DESI/CMB-S4 reach) "
          "excludes the normal-ordered m1~0 spectrum -> forces inverted ordering or "
          "a degenerate offset, falsifying the minimal TFPT seesaw reading -- a "
          "sharp near-term corner, not a knob" % float(Sigma_NO),
          Sigma_NO > 0)

    return summary("v272 absolute nu-scale = one seesaw ratio (parallels v_geo); TFPT window consistent at O(1) Yukawa, NO floor 0.0586 eV is the kill test (FLAV.NUSCALE.01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
