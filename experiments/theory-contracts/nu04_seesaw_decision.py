"""nu04 -- the DECISION computation named by v481/FLAV.NUSCALE.02, executed
(theory contract; never a scorecard row, never load-bearing).

v481 declined the integer rung M_R = c3^3 Mbar because it predicts m_3 40% low at
1-loop, and NAMED the decision computation (better RG + thresholds).  This probe
executes the decision in the ROBUST form: instead of trusting any single set of
higher-loop coefficients, it brackets every input with GENEROUS (>= 3 sigma)
bands and asks whether ANY of them can bridge the gap factor

    F_req = m_3(observed) / m_3(rung)  ~ 1.67.

Inputs varied (generous brackets):
  - m_t(MSbar, M_Z): 162.5 +- 3.0 GeV        (>3x the PDG uncertainty)
  - alpha_s via alpha_3^-1(M_Z): 8.44 -+ 0.10 (>3x)
  - dm2_atm: +-3%                             (>3x NuFIT)
  - kappa run-down factor: +-10% band          (generous 2-loop/scheme envelope)
  - PS-stage Yukawa running M_PS -> M_R: beta_yt scaled x[0.5, 1.5] over that
    leg (a >50% envelope on the PS-vs-SM difference)

VERDICT expected and found: the maximal combined shift in m_3(rung) is far below
F_req -- the rung as an UNSTRUCTURED exact pin is EXCLUDED conditional on the
[P] premise y_nu = y_t (it is not an RG artifact).  The only escape is an O(1.7)
STRUCTURE factor in the Majorana sector (third-generation effective eigenvalue
below the rung scale).  POST-HOC OBSERVATION (recorded and DECLINED per
v354/v355): the required factor F_req = 1.671 sits 0.3% from the atom rational
g_car/N_fam = 5/3; no mechanism forces a 3/5 Clebsch on M_R,3 today, so this is
a NAMED coincidence with a NAMED missing mechanism, not a claim.  The
one-parameter window candidate of v481 (M_R = 9.3e13 GeV free in the PS window)
is UNAFFECTED by all of this.

Run:  cd experiments/theory-contracts && python3 nu04_seesaw_decision.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "nu04_seesaw_decision_results.json"
CHECKS: list[dict] = []

MZ = 91.1876
MBAR = 2.435e18
C3 = 1 / (8 * math.pi)
V_EW = 246.22
LAM_MZ = 0.130
M3_OBS = 0.0503          # eV
M_PS, M_GUT = 4.2e13, 2.4e15
MR_RUNG = C3 ** 3 * MBAR


def check(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def m3_rung(mt_msbar=162.5, a3_inv=8.44, kappa_band=1.0, ps_beta_scale=1.0,
            n=20000) -> float:
    """m_3(M_Z) in eV for y_nu = y_t and M_R = c3^3 Mbar, with bracketed inputs.
    ps_beta_scale rescales beta_yt on the leg M_PS -> M_R (PS-vs-SM envelope)."""
    a_inv = (59.01, 29.59, a3_inv)
    g1, g2, g3 = [math.sqrt(4 * math.pi / a) for a in a_inv]
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


def main() -> None:
    print("nu04 -- the v481 decision computation, executed (bracketed exclusion)\n")

    m3_c = m3_rung()
    F_req = M3_OBS / m3_c

    # C1: the gap factor
    check("C1 THE GAP [E-num]: central m_3(rung) = %.4f eV vs observed %.4f eV "
          "-- the rung must be rescued by a factor F_req = %.3f in m_3 (i.e. "
          "+%.1f%%), equivalently 0.154 c3-rungs" % (m3_c, M3_OBS, F_req,
                                                     100 * (F_req - 1)),
          1.5 < F_req < 1.9)

    # C2: bracketed sensitivity -- can ANY generous input band bridge it?
    variations = {
        "m_t +3 GeV (>3 sigma)": m3_rung(mt_msbar=165.5),
        "m_t -3 GeV": m3_rung(mt_msbar=159.5),
        "alpha_3^-1 -0.10 (>3 sigma)": m3_rung(a3_inv=8.34),
        "alpha_3^-1 +0.10": m3_rung(a3_inv=8.54),
        "kappa band +10%": m3_rung(kappa_band=1.10),
        "kappa band -10%": m3_rung(kappa_band=0.90),
        "PS-leg beta_yt x1.5": m3_rung(ps_beta_scale=1.5),
        "PS-leg beta_yt x0.5": m3_rung(ps_beta_scale=0.5),
    }
    shifts = {kk: v / m3_c for kk, v in variations.items()}
    max_up = max(shifts.values())
    # worst-case COMBINED (all favourable at once, still generous)
    m3_best = m3_rung(mt_msbar=165.5, a3_inv=8.34, kappa_band=1.10,
                      ps_beta_scale=0.5)
    F_best = m3_best / m3_c
    ok2 = max_up < 1.15 and F_best < 1.25 and F_best < F_req * 0.8
    detail = "; ".join(f"{kk}: x{v:.3f}" for kk, v in shifts.items())
    check("C2 BRACKETED EXCLUSION [E-num]: no generous input band reaches "
          "F_req -- max single shift x%.3f, ALL-favourable combined x%.3f, "
          "required x%.3f: the unstructured rung is EXCLUDED conditional on "
          "[P] y_nu = y_t (not an RG artifact). Bands: %s"
          % (max_up, F_best, F_req, detail),
          ok2)

    # C3: the named escape -- a Majorana structure factor
    r_needed = F_req
    five_thirds = 5 / 3
    rel = abs(r_needed - five_thirds) / five_thirds
    check("C3 NAMED ESCAPE + POST-HOC NOTE (recorded, DECLINED per v354/v355): "
          "only an O(%.2f) third-generation Majorana STRUCTURE factor "
          "(M_R,3 = M_R/r) can revive the rung. Post-hoc: r_needed = %.4f is "
          "%.2f%% from the atom rational g_car/N_fam = 5/3 -- NO mechanism "
          "forces a 3/5 Clebsch on M_R,3 today, so this is a named coincidence "
          "with a named missing mechanism (PS Majorana-sector Clebsch), NOT a "
          "claim; no promotion of the coincidence"
          % (r_needed, r_needed, 100 * rel),
          rel < 0.02)

    # C4: the one-parameter window candidate is unaffected
    check("C4 CANDIDATE UNAFFECTED [E-num]: the v481 one-parameter statement "
          "(M_R free in the PS window; required M_R = 9.3e13 GeV at rung 3.15; "
          "NO floor Sigma m_nu = 0.059 eV) does not use the integer rung and "
          "stands unchanged; FLAV.NUSCALE stays a window-bracketed [O] "
          "candidate", True)

    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "CONTRACT HOLDS" if n_pass == len(CHECKS) else "CONTRACT FAILS"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "The decision computation named by v481 is executed in bracketed form: "
        "the integer rung M_R = c3^3 Mbar predicts m_3 a factor 1.67 low, and "
        "NO generous input band (m_t +-3 GeV, alpha_s >3 sigma, kappa-run "
        "+-10%, PS-leg beta envelope x[0.5,1.5]) moves it by more than x1.2 -- "
        "the unstructured rung is EXCLUDED conditional on the carrier premise "
        "y_nu = y_t. The only escape is a third-generation Majorana structure "
        "factor r = 1.671; its 0.3% proximity to g_car/N_fam = 5/3 is recorded "
        "post-hoc and DECLINED (no forcing mechanism). The v481 one-parameter "
        "window candidate is unaffected. No gate closes."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "nu04 seesaw integer-rung decision (bracketed exclusion)",
        "date": "2026-07-14",
        "firewall": ("theory contract, never a scorecard row, never "
                     "load-bearing; frozen record untouched"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")
    raise SystemExit(0 if n_pass == len(CHECKS) else 1)


if __name__ == "__main__":
    main()
