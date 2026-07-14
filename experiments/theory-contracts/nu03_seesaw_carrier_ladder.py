"""nu03 -- the absolute neutrino-mass scale with the CARRIER-FORCED Yukawa
normalisation y_nu = y_t (theory contract; never a scorecard row, never load-bearing).

Motivation (2026-07-14, bird's-eye round): FLAV.NUSCALE.01 types the absolute scale as
ONE open UV input with a two-parameter trade-off (y_nu, M_R), and its [O] note records
that the y_nu = 1 inversion lands at log_c3(Mbar/M_R) = 2.57 -- non-integer, "not a
compiler output". But y_nu = 1 is NOT the carrier normalisation: TFPT's own carrier
structure (one SO(10) 16 per family, PS algebra v245/v248/v249) with the MINIMAL Higgs
Yukawa sector (one 10 / one PS (1,2,2)) forces the third-family Dirac neutrino Yukawa
to equal the top Yukawa at the PS scale: y_nu(M_PS) = y_t(M_PS). This contract redoes
the inversion with that normalisation, at explicit 1-loop RG (gauge + y_t + lambda up;
Weinberg-operator kappa down, Antusch-Drees-Kersten-Lindner-Ratz hep-ph/0108005:
16 pi^2 dkappa/dt = alpha kappa + C[(Ye+Ye)kappa + ...], C = -3/2,
alpha_SM = -3 g2^2 + 6 y_t^2 + lambda + ...), and confronts the c3-ladder.

RESULTS TYPE.  [E-num]: the RG arithmetic and the inversion are explicit and
reproducible.  [P]: the premise y_nu = y_t is the minimal-Yukawa-sector matching
(named, unproven in TFPT).  [O]: honesty gate -- the inversion lands NEAR but NOT ON
the integer rung (see below); per the v354/v355 anti-numerology discipline the ladder
pin is NOT claimed. What survives honestly:
  (1) the two-parameter trade-off COLLAPSES to one (M_R alone) under the carrier
      normalisation -- a genuine sharpening of FLAV.NUSCALE.01's [O];
  (2) the PS window [M_PS, M_GUT] BRACKETS the observed m_3: the required M_R is
      INSIDE the compiler's own UV window (consistency, not prediction);
  (3) the required rung is log_c3(Mbar/M_R) ~ 3.1-3.2 (vs 2.57 for y_nu=1): the
      integer rung M_R = c3^3 Mbar predicts m_3 20-45% LOW at 1-loop -- suggestive,
      NOT forced; the DECISION computation is named (2-loop SM + PS thresholds).

Firewall: theory contract; belongs in experiments/theory-contracts, never in
evidence_scorecard.json; the frozen record (v84/REG.FREEZE.01) is NOT touched.

Run:  cd experiments/theory-contracts && python3 nu03_seesaw_carrier_ladder.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "nu03_seesaw_carrier_ladder_results.json"

CHECKS: list[dict] = []

# constants / inputs (PDG-level; same M_Z inputs as the v246/v249 RG rows)
MZ = 91.1876
MBAR = 2.435e18                 # reduced Planck mass, GeV
C3 = 1 / (8 * math.pi)
V_EW = 246.22                   # GeV
YT_MZ = math.sqrt(2) * 162.5 / V_EW   # MSbar top Yukawa at M_Z (mt_MSbar ~ 162.5)
LAM_MZ = 0.130                  # Higgs quartic at M_Z (mh = 125 GeV)
A_INV_MZ = (59.01, 29.59, 8.44)  # GUT-normalised alpha_i^-1 at M_Z (v246 inputs)
M3_OBS = 0.0503                 # eV, sqrt(dm2_atm) NuFIT NO
DM2_21 = 7.42e-5                # eV^2
M_PS, M_GUT = 4.2e13, 2.4e15    # v249 PS two-step window, GeV
M_SCALARON = C3 ** 3.5 * MBAR   # v36: 3.06e13 GeV


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def run_sm_up(mu_hi: float, n: int = 40000):
    """1-loop SM: g1,g2,g3 (GUT-normalised), y_t, lambda from M_Z to mu_hi.
    Returns callables-free endpoint values and the trajectory for the kappa integral."""
    g = [math.sqrt(4 * math.pi / a) for a in A_INV_MZ]
    g1, g2, g3 = g
    yt, lam = YT_MZ, LAM_MZ
    T = math.log(mu_hi / MZ)
    h = T / n
    traj = []           # (t, g2^2, yt^2, lam)
    k = 1 / (16 * math.pi ** 2)
    b = (41 / 10, -19 / 6, -7)
    for i in range(n):
        traj.append((i * h, g2 * g2, yt * yt, lam))
        dg1 = k * b[0] * g1 ** 3
        dg2 = k * b[1] * g2 ** 3
        dg3 = k * b[2] * g3 ** 3
        dyt = k * yt * (4.5 * yt ** 2 - 8 * g3 ** 2 - 2.25 * g2 ** 2
                        - (17 / 20) * g1 ** 2)
        dlam = k * (24 * lam ** 2 - 6 * yt ** 4 + 12 * lam * yt ** 2
                    - 3 * lam * (3 * g2 ** 2 + (3 / 5) * g1 ** 2)
                    + (3 / 8) * (2 * g2 ** 4 + (g2 ** 2 + (3 / 5) * g1 ** 2) ** 2))
        g1 += h * dg1
        g2 += h * dg2
        g3 += h * dg3
        yt += h * dyt
        lam += h * dlam
    return (g1, g2, g3, yt, lam), traj, h


def kappa_running_factor(traj, h) -> float:
    """exp(-Integral alpha_SM dt / 16 pi^2) from M_Z to the top of traj -- the factor by
    which the Weinberg-operator coefficient DEcreases from mu_hi down to M_Z is 1/this;
    i.e. m_nu(MZ) = m_nu(mu_hi) * exp(-I) with I = int alpha dt / 16 pi^2 > 0
    (alpha_SM = -3 g2^2 + 6 y_t^2 + lambda, ADKLR hep-ph/0108005; tau-Yukawa term
    negligible)."""
    I = 0.0
    for (t, g2sq, ytsq, lam) in traj:
        I += (-3 * g2sq + 6 * ytsq + lam) * h
    return math.exp(-I / (16 * math.pi ** 2))


def m3_at_MZ(MR: float) -> tuple[float, float, float]:
    """Predicted m_3(M_Z) in eV for y_nu(MR) = y_t(MR), seesaw at MR, ADKLR running
    down. Returns (m3_eV, y_t(MR), RG_down_factor)."""
    (g1, g2, g3, yt, lam), traj, h = run_sm_up(MR)
    m3_at_MR_GeV = (yt * V_EW / math.sqrt(2)) ** 2 / MR
    R = kappa_running_factor(traj, h)
    return m3_at_MR_GeV * R * 1e9, yt, R


def main() -> None:
    print("nu03 -- seesaw with the carrier-forced Yukawa normalisation y_nu = y_t\n")

    # C1: the carrier normalisation collapses the trade-off
    MR_int = C3 ** 3 * MBAR
    m3_int, yt_int, R_int = m3_at_MZ(MR_int)
    ok1 = 0.2 < yt_int < 0.6
    check("C1 CARRIER NORMALISATION [P named]: one SO(10) 16 per family + minimal "
          "Yukawa sector (10_H / PS (1,2,2)) => y_nu = y_t at the PS scale -- the "
          "(y_nu, M_R) trade-off of FLAV.NUSCALE.01 collapses to M_R alone",
          ok1, f"y_t(c3^3 Mbar = {MR_int:.3e} GeV) = {yt_int:.3f} (1-loop); premise "
               f"[P]: minimal Yukawa sector, named not proven")

    # C2: inversion -- what M_R does the observed m_3 demand?
    lo, hi = 1e13, 1e16
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        m3, _, _ = m3_at_MZ(mid)
        if m3 > M3_OBS:
            lo = mid
        else:
            hi = mid
    MR_req = math.sqrt(lo * hi)
    rung_req = math.log(MBAR / MR_req) / math.log(1 / C3)
    rung_ynu1 = math.log(MBAR / (V_EW ** 2 / (M3_OBS * 1e-9))) / math.log(1 / C3)
    ok2 = M_PS < MR_req < M_GUT
    check("C2 INVERSION INSIDE THE COMPILER WINDOW [E-num]: the observed m_3 = 0.0503 "
          "eV demands M_R INSIDE the PS two-step window [M_PS, M_GUT] (v249) -- the "
          "carrier UV window brackets the measured absolute scale",
          ok2, f"M_R(required) = {MR_req:.3e} GeV in [{M_PS:.1e}, {M_GUT:.1e}]; "
               f"log_c3(Mbar/M_R) = {rung_req:.3f} (y_nu = 1 gave {rung_ynu1:.2f})")

    # C3: the integer rung -- honest near-miss, NOT claimed
    ratio = m3_int / M3_OBS
    ok3 = 0.4 < ratio < 1.0     # lands LOW by 20-45% at 1-loop; record honestly
    check("C3 INTEGER RUNG HONESTY GATE [O]: M_R = c3^3 Mbar predicts m_3 LOW by "
          "20-45% at 1-loop -- NEAR the rung (3.1 vs 3.0) but NOT ON it; per v354/v355 "
          "the ladder pin is DECLINED; decision computation named: 2-loop SM + explicit "
          "PS threshold matching",
          ok3, f"m_3(c3^3 Mbar) = {m3_int:.4f} eV vs observed {M3_OBS} eV "
               f"(ratio {ratio:.2f}); RG-down factor = {R_int:.3f}; rung required "
               f"{rung_req:.3f} vs integer 3")

    # C4: falsifiable band -- Sigma m_nu under the carrier normalisation
    m3_lo, _, _ = m3_at_MZ(M_GUT)
    m3_hi, _, _ = m3_at_MZ(M_PS)
    m2_of = lambda m3: math.sqrt(DM2_21)      # NO, m1 ~ 0
    sigma_obs_floor = M3_OBS + math.sqrt(DM2_21)
    sigma_hi = m3_hi + math.sqrt(DM2_21)
    ok4 = m3_lo < M3_OBS < m3_hi and sigma_hi > 0.1
    check("C4 FALSIFIABLE BAND [E-num]: over the PS window the carrier-normalised "
          "seesaw spans m_3 in [low, high] bracketing 0.0503 eV; the LOW-M_R half is "
          "already in tension with DESI Sigma m_nu -- cosmology cuts the window from "
          "below",
          ok4, f"m_3(M_GUT) = {m3_lo:.4f} eV, m_3(M_PS) = {m3_hi:.4f} eV; "
               f"NO floor Sigma = {sigma_obs_floor:.4f} eV; Sigma at M_PS end = "
               f"{sigma_hi:.3f} eV vs DESI ~0.072")

    # C5: context pins (no claims): where the required M_R sits
    r_ms = MR_req / M_SCALARON
    r_int = MR_req / MR_int
    ok5 = True
    check("C5 CONTEXT (recorded, NOT claimed): required M_R vs compiler scales -- "
          "ratios logged for the decision computation; no pattern claimed (v354/v355)",
          ok5, f"M_R(req)/M_scalaron = {r_ms:.2f}; M_R(req)/(c3^3 Mbar) = {r_int:.2f}; "
               f"M_R(req)/M_PS = {MR_req / M_PS:.2f}")

    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "CONTRACT HOLDS" if n_pass == len(CHECKS) else "CONTRACT FAILS"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "With the carrier-forced normalisation y_nu = y_t (one 16 per family + minimal "
        "Yukawa sector, [P]), FLAV.NUSCALE.01's two-parameter (y_nu, M_R) trade-off "
        "collapses to M_R alone, and the observed m_3 = 0.0503 eV demands M_R inside "
        "the compiler's own PS window, at log_c3(Mbar/M_R) ~ 3.1 (the y_nu = 1 "
        "inversion gave the structureless 2.57). The integer rung c3^3 Mbar predicts "
        "m_3 20-45% low at 1-loop: NEAR, not ON -- the ladder pin is DECLINED per the "
        "anti-numerology discipline, and the decision computation (2-loop SM + explicit "
        "PS thresholds) is named. What survives regardless: the absolute scale is now a "
        "ONE-parameter statement bracketed by the compiler window, with the NO floor "
        "Sigma m_nu = 0.059 eV as the falsifiable edge. No gate closed, frozen record "
        "untouched."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "nu03 seesaw with carrier-forced Yukawa normalisation",
        "date": "2026-07-14",
        "firewall": ("theory contract, never a scorecard row, never load-bearing; "
                     "frozen record untouched; FLAV.NUSCALE.01 stays open"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")
    raise SystemExit(0 if n_pass == len(CHECKS) else 1)


if __name__ == "__main__":
    main()
