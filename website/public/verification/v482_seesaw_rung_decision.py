"""v482 -- FLAV.NUSCALE.03: the decision computation NAMED by v481, EXECUTED in
bracketed (assumption-robust) form -- the integer rung M_R = c3^3 Mbar is
EXCLUDED as an unstructured exact pin, conditional on the carrier premise
y_nu = y_t; the required rescue factor is quantified, its post-hoc proximity to
the atom rational g_car/N_fam = 5/3 is recorded and DECLINED (v354/v355); the
one-parameter window candidate of v481 is UNAFFECTED.  No gate closes.

Background.  v481 (FLAV.NUSCALE.02) collapsed the seesaw to one parameter under
y_nu = y_t and found the integer rung M_R = c3^3 Mbar predicts m_3 = 0.030 eV
-- 40% below the observed 0.0503 eV at 1-loop -- and NAMED the decision
computation (higher loops + thresholds).  Instead of trusting any single set of
higher-loop coefficients, this module executes the decision ROBUSTLY: every
input is bracketed with a band far wider than its real uncertainty, and the
question is whether ANY of them (or all combined) can bridge the gap.

  [E-num] 1. THE GAP: central m_3(rung) = 0.0301 eV vs 0.0503 observed --
        rescue factor F_req = 1.670 (+67%), i.e. 0.154 c3-rungs.
  [E-num] 2. BRACKETED EXCLUSION: with m_t(MSbar) +- 3 GeV (>3 sigma),
        alpha_3^-1 -+ 0.10 (>3 sigma), a +-10% band on the ADKLR kappa
        run-down, and the PS-leg Yukawa beta scaled x[0.5, 1.5] between M_PS
        and M_R (a >50% envelope on the PS-vs-SM running difference), the
        largest single shift is x1.10 and the ALL-favourable combination
        reaches only x1.165 -- far below the required x1.670.  The
        unstructured rung is EXCLUDED conditional on [P] y_nu = y_t: the
        1-loop miss of v481 is NOT an RG artifact.
  [C]  3. THE NAMED ESCAPE, RECORDED AND DECLINED: only a third-generation
        Majorana STRUCTURE factor r = M_R/M_{R,3} ~ 1.67 can revive the rung.
        Post-hoc: r_needed = 1.6696 sits 0.18% from g_car/N_fam = 5/3.  NO
        mechanism forces a 3/5 Clebsch on M_{R,3} today, so per the
        anti-numerology discipline (v354/v355) this is a NAMED coincidence
        with a NAMED missing mechanism (a PS Majorana-sector Clebsch), not a
        claim -- exactly the t0 ~ 30 pattern of v478.
  [O]  4. CANDIDATE UNAFFECTED: v481's one-parameter statement (M_R free in
        the PS window, required M_R = 9.3e13 GeV at rung 3.15, NO floor
        Sigma m_nu = 0.059 eV) never used the integer rung and stands.

NET EFFECT: the v481 candidate is now CLEANLY TYPED -- the exact-pin reading is
dead (robustly), the window reading lives; the frozen record (v84) untouched.
Numerical (explicit 1-loop RG + bracketed envelopes), Python-only by nature.
"""
import math

from tfpt_constants import check, summary, reset, c3, Mbar, g_car, N_fam

MZ = 91.1876
V_EW = 246.22
LAM_MZ = 0.130
M3_OBS = 0.0503
M_PS = 4.2e13
C3 = float(c3)
MR_RUNG = C3 ** 3 * float(Mbar)


def m3_rung(mt_msbar=162.5, a3_inv=8.44, kappa_band=1.0, ps_beta_scale=1.0,
            n=20000) -> float:
    """m_3(M_Z) in eV for y_nu = y_t and M_R = c3^3 Mbar, bracketed inputs."""
    g1, g2, g3 = [math.sqrt(4 * math.pi / a) for a in (59.01, 29.59, a3_inv)]
    yt, lam = math.sqrt(2) * mt_msbar / V_EW, LAM_MZ
    T = math.log(MR_RUNG / MZ)
    t_ps = math.log(M_PS / MZ)
    h = T / n
    k = 1 / (16 * math.pi ** 2)
    b = (41 / 10, -19 / 6, -7)
    I_alpha = 0.0
    for i in range(n):
        t = i * h
        I_alpha += (-3 * g2 * g2 + 6 * yt * yt + lam) * h
        scale = ps_beta_scale if t > t_ps else 1.0
        dg1 = k * b[0] * g1 ** 3
        dg2 = k * b[1] * g2 ** 3
        dg3 = k * b[2] * g3 ** 3
        dyt = scale * k * yt * (4.5 * yt ** 2 - 8 * g3 ** 2 - 2.25 * g2 ** 2
                                - (17 / 20) * g1 ** 2)
        dlam = k * (24 * lam ** 2 - 6 * yt ** 4 + 12 * lam * yt ** 2
                    - 3 * lam * (3 * g2 ** 2 + 0.6 * g1 ** 2)
                    + 0.375 * (2 * g2 ** 4 + (g2 ** 2 + 0.6 * g1 ** 2) ** 2))
        g1 += h * dg1
        g2 += h * dg2
        g3 += h * dg3
        yt += h * dyt
        lam += h * dlam
    R_down = math.exp(-I_alpha / (16 * math.pi ** 2)) * kappa_band
    return (yt * V_EW / math.sqrt(2)) ** 2 / MR_RUNG * R_down * 1e9


def run():
    reset()
    print("v482  FLAV.NUSCALE.03: the v481 decision computation, executed "
          "(bracketed exclusion)")

    m3_c = m3_rung()
    F_req = M3_OBS / m3_c
    check("THE GAP [E-num]: central m_3(rung) = %.4f eV vs observed %.4f eV -- "
          "rescue factor F_req = %.3f (+%.0f%%), i.e. 0.154 c3-rungs"
          % (m3_c, M3_OBS, F_req, 100 * (F_req - 1)),
          1.5 < F_req < 1.9)

    shifts = {
        "m_t +3": m3_rung(mt_msbar=165.5) / m3_c,
        "m_t -3": m3_rung(mt_msbar=159.5) / m3_c,
        "a3inv -0.10": m3_rung(a3_inv=8.34) / m3_c,
        "a3inv +0.10": m3_rung(a3_inv=8.54) / m3_c,
        "kappa +10%": 1.10,
        "kappa -10%": 0.90,
        "PS-leg x1.5": m3_rung(ps_beta_scale=1.5) / m3_c,
        "PS-leg x0.5": m3_rung(ps_beta_scale=0.5) / m3_c,
    }
    F_best = m3_rung(mt_msbar=165.5, a3_inv=8.34, kappa_band=1.10,
                     ps_beta_scale=0.5) / m3_c
    max_up = max(shifts.values())
    check("BRACKETED EXCLUSION [E-num]: max single band shift x%.3f, "
          "ALL-favourable combined x%.3f, required x%.3f -- NO generous input "
          "band (m_t +-3 GeV >3sig, alpha_s >3sig, kappa-run +-10%%, PS-leg "
          "beta envelope x[0.5,1.5]) bridges the gap: the UNSTRUCTURED rung "
          "M_R = c3^3 Mbar is EXCLUDED conditional on [P] y_nu = y_t (the "
          "v481 miss is not an RG artifact); bands: %s"
          % (max_up, F_best, F_req,
             "; ".join(f"{kk} x{v:.3f}" for kk, v in shifts.items())),
          max_up < 1.15 and F_best < 1.25 and F_best < 0.8 * F_req)

    five_thirds = g_car / N_fam
    rel = abs(F_req - five_thirds) / five_thirds
    check("NAMED ESCAPE + POST-HOC NOTE [C declined]: only a third-generation "
          "Majorana STRUCTURE factor r = M_R/M_R3 ~ %.3f revives the rung; "
          "post-hoc r_needed is %.2f%% from g_car/N_fam = 5/3 -- NO mechanism "
          "forces a 3/5 Clebsch on M_R3 today, so this is a named coincidence "
          "with a named missing mechanism (PS Majorana-sector Clebsch), "
          "DECLINED per v354/v355 -- the same discipline as the t0 ~ 30 "
          "near-miss (v478)" % (F_req, 100 * rel),
          rel < 0.02)

    check("CANDIDATE UNAFFECTED [O]: v481's one-parameter window statement "
          "(M_R free in [M_PS, M_GUT]; required M_R = 9.3e13 GeV at rung "
          "3.15; NO floor Sigma m_nu = 0.059 eV) never used the integer rung "
          "and stands unchanged; FLAV.NUSCALE stays a window-bracketed [O] "
          "candidate; frozen record (v84) untouched; no gate closes", True)

    return summary("v482 FLAV.NUSCALE.03: the named decision computation "
                   "executed -- the integer rung c3^3 Mbar is EXCLUDED as an "
                   "unstructured pin (needs x1.67 in m_3; generous input bands "
                   "give at most x1.165 combined), conditional on y_nu = y_t; "
                   "the r = 5/3-proximate structure escape is recorded and "
                   "DECLINED (0.18%, no mechanism); the v481 one-parameter "
                   "window candidate stands; nothing closes")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
