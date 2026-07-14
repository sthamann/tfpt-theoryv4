"""v481 -- FLAV.NUSCALE.02: the absolute neutrino-mass scale under the CARRIER
Yukawa normalisation y_nu = y_t -- FLAV.NUSCALE.01's two-parameter (y_nu, M_R)
trade-off collapses to ONE parameter, the required M_R lands INSIDE the compiler's
own PS window, and the nearby integer c3-rung is explicitly DECLINED at 1-loop
(anti-numerology, v354/v355).  A CANDIDATE-class sharpening (genre v467/v468); the
frozen record (v84/REG.FREEZE.01) is untouched and NO gate closes.

Background.  FLAV.NUSCALE.01 (v272) typed the absolute scale as ONE open UV input
with the trade-off m_3 = (y_nu v)^2 / (2 M_R), and recorded that the y_nu = 1
inversion gives log_c3(Mbar/M_R) ~ 2.6 -- non-integer, "not a compiler output".
But y_nu = 1 is not the carrier normalisation: TFPT's own carrier structure (one
SO(10) 16 per family, PS algebra v245/v248/v249) with the MINIMAL Yukawa sector
(one 10_H / PS (1,2,2)) forces the third-family Dirac neutrino Yukawa to equal
the top Yukawa at the matching scale: y_nu = y_t.  This module redoes the
inversion with that normalisation at explicit 1-loop RG:

  up:   g1, g2, g3 (GUT-normalised, b = (41/10, -19/6, -7), the v273 EG
        coefficients), y_t, lambda from M_Z to M_R;
  down: the Weinberg operator kappa with the ADKLR coefficient
        16 pi^2 dkappa/dt = (-3 g2^2 + 6 y_t^2 + lambda) kappa + flavor terms
        (Antusch-Drees-Kersten-Lindner-Ratz, Phys. Lett. B519 (2001) 238,
        hep-ph/0108005; tau-Yukawa flavor term negligible here).

  [P] 1. CARRIER NORMALISATION (named premise): y_nu = y_t at M_R from the
        minimal 16.16.10 Yukawa sector -- the trade-off collapses to M_R alone.
  [N] 2. INVERSION INSIDE THE COMPILER WINDOW: the observed m_3 = sqrt(dm2_atm)
        = 0.0503 eV demands M_R ~ 9.3e13 GeV -- INSIDE the PS two-step window
        [M_PS, M_GUT] = [4.2e13, 2.4e15] (v249), at log_c3(Mbar/M_R) = 3.15.
  [X] 3. INTEGER-RUNG HONESTY GATE: the rung M_R = c3^3 Mbar = 1.53e14 GeV
        predicts m_3 = 0.030 eV -- 40% LOW at 1-loop.  NEAR (3.15 vs 3), NOT ON:
        the ladder pin is DECLINED per v354/v355; the named decision computation
        is 2-loop SM running + explicit PS threshold matching.
  [N] 4. FALSIFIABLE BAND: over the PS window the carrier-normalised seesaw
        spans m_3(M_GUT) = 0.002 .. m_3(M_PS) = 0.115 eV, bracketing the
        observation; the low-M_R half is already in tension with DESI
        Sigma m_nu ~ 0.072 eV -- cosmology cuts the window from below; the NO
        floor Sigma = m_2 + m_3 = 0.059 eV stays the falsifiable edge (v272).
  [C]/[O] 5. Scope: candidate-class; the premise is the minimal Yukawa sector
        [P]; the absolute scale stays formally open until the decision
        computation lands; the frozen registry is untouched.

NET EFFECT: the absolute neutrino scale is now a ONE-parameter statement
bracketed by the compiler's own UV window instead of a two-parameter trade-off.
Numerical (explicit 1-loop RG integration), Python-only by nature.
"""
import math

from tfpt_constants import check, summary, reset, c3, Mbar

MZ = 91.1876
V_EW = 246.22
YT_MZ = math.sqrt(2) * 162.5 / V_EW      # MSbar m_t(M_Z) ~ 162.5 GeV
LAM_MZ = 0.130                            # m_h = 125 GeV quartic at M_Z
A_INV_MZ = (59.01, 29.59, 8.44)           # v246 GUT-normalised inputs
M3_OBS = 0.0503                           # eV (NuFIT NO, sqrt dm2_atm)
DM2_21 = 7.42e-5                          # eV^2
M_PS, M_GUT = 4.2e13, 2.4e15              # v249 PS window
C3 = float(c3)
MBARF = float(Mbar)


def run_sm_up(mu_hi, n=20000):
    g1, g2, g3 = [math.sqrt(4 * math.pi / a) for a in A_INV_MZ]
    yt, lam = YT_MZ, LAM_MZ
    T = math.log(mu_hi / MZ)
    h = T / n
    k = 1 / (16 * math.pi ** 2)
    b = (41 / 10, -19 / 6, -7)
    I_alpha = 0.0                          # integral of alpha_SM dt
    for _ in range(n):
        I_alpha += (-3 * g2 * g2 + 6 * yt * yt + lam) * h
        dg1 = k * b[0] * g1 ** 3
        dg2 = k * b[1] * g2 ** 3
        dg3 = k * b[2] * g3 ** 3
        dyt = k * yt * (4.5 * yt ** 2 - 8 * g3 ** 2 - 2.25 * g2 ** 2
                        - (17 / 20) * g1 ** 2)
        dlam = k * (24 * lam ** 2 - 6 * yt ** 4 + 12 * lam * yt ** 2
                    - 3 * lam * (3 * g2 ** 2 + 0.6 * g1 ** 2)
                    + 0.375 * (2 * g2 ** 4 + (g2 ** 2 + 0.6 * g1 ** 2) ** 2))
        g1 += h * dg1
        g2 += h * dg2
        g3 += h * dg3
        yt += h * dyt
        lam += h * dlam
    R_down = math.exp(-I_alpha / (16 * math.pi ** 2))
    return yt, R_down


def m3_pred_eV(MR):
    """m_3(M_Z) for y_nu(MR) = y_t(MR): seesaw at MR + ADKLR running down."""
    yt, R = run_sm_up(MR)
    return (yt * V_EW / math.sqrt(2)) ** 2 / MR * R * 1e9, yt, R


def run():
    reset()
    print("v481  FLAV.NUSCALE.02: seesaw with the carrier normalisation y_nu = y_t")

    MR_int = C3 ** 3 * MBARF
    m3_int, yt_int, R_int = m3_pred_eV(MR_int)

    # 1. carrier normalisation premise
    check("CARRIER NORMALISATION [P named]: one SO(10) 16 per family + minimal "
          "Yukawa sector (10_H / PS (1,2,2)) => y_nu = y_t at the matching scale "
          "(y_t(1.5e14 GeV) = %.3f at 1-loop) -- FLAV.NUSCALE.01's (y_nu, M_R) "
          "trade-off collapses to M_R alone; premise NAMED, not proven" % yt_int,
          0.2 < yt_int < 0.7)

    # 2. inversion inside the compiler window
    lo, hi = 1e13, 1e16
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        if m3_pred_eV(mid)[0] > M3_OBS:
            lo = mid
        else:
            hi = mid
    MR_req = math.sqrt(lo * hi)
    rung_req = math.log(MBARF / MR_req) / math.log(1 / C3)
    MR_ynu1 = (V_EW / math.sqrt(2)) ** 2 / (M3_OBS * 1e-9)   # ledger convention m_D = v/sqrt2
    rung_ynu1 = math.log(MBARF / MR_ynu1) / math.log(1 / C3)
    check("INVERSION INSIDE THE COMPILER WINDOW [N]: the observed m_3 = 0.0503 eV "
          "demands M_R = %.2e GeV -- INSIDE the PS two-step window [4.2e13, 2.4e15] "
          "(v249) -- at log_c3(Mbar/M_R) = %.3f (the y_nu = 1 inversion gives the "
          "structureless %.2f, the FLAV.NUSCALE.01 number)" % (MR_req, rung_req, rung_ynu1),
          M_PS < MR_req < M_GUT and abs(rung_req - 3.15) < 0.05
          and abs(rung_ynu1 - 2.57) < 0.02)

    # 3. integer-rung honesty gate
    ratio = m3_int / M3_OBS
    check("INTEGER-RUNG HONESTY GATE [X declined]: M_R = c3^3 Mbar = %.2e GeV "
          "predicts m_3 = %.4f eV -- ratio %.2f to observation (40%% low at "
          "1-loop; kappa run-down factor %.3f).  NEAR the rung (%.2f vs 3), NOT "
          "ON: the ladder pin is DECLINED per v354/v355; decision computation "
          "named: 2-loop SM + explicit PS threshold matching"
          % (MR_int, m3_int, ratio, R_int, rung_req),
          0.4 < ratio < 0.8)

    # 4. falsifiable band
    m3_lo = m3_pred_eV(M_GUT)[0]
    m3_hi = m3_pred_eV(M_PS)[0]
    m2 = math.sqrt(DM2_21)
    sigma_floor = M3_OBS + m2
    check("FALSIFIABLE BAND [N]: over the PS window m_3 spans [%.4f, %.4f] eV, "
          "bracketing 0.0503; Sigma at the M_PS end = %.3f eV is already in tension "
          "with DESI ~0.072 -- cosmology cuts the window from below; the NO floor "
          "Sigma = m_2 + m_3 = %.4f eV stays the falsifiable edge (v272)"
          % (m3_lo, m3_hi, m3_hi + m2, sigma_floor),
          m3_lo < M3_OBS < m3_hi and sigma_floor < 0.072)

    # 5. scope
    check("SCOPE [C]/[O]: CANDIDATE class (genre v467/v468) -- the premise is the "
          "minimal Yukawa sector [P]; the absolute scale stays formally open until "
          "the named decision computation lands; frozen record (v84/REG.FREEZE.01) "
          "untouched; no gate closes, no marker moves", True)

    return summary("v481 FLAV.NUSCALE.02: carrier normalisation y_nu = y_t collapses "
                   "the (y_nu, M_R) trade-off to one parameter -- required M_R = "
                   "9.3e13 GeV INSIDE the PS window at log_c3(Mbar/M_R) = 3.15; "
                   "integer rung c3^3 Mbar declined at 1-loop (m_3 40% low; decision "
                   "= 2-loop + PS thresholds); falsifiable band brackets observation, "
                   "NO floor Sigma m_nu = 0.059 eV; candidate class, nothing closes")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
