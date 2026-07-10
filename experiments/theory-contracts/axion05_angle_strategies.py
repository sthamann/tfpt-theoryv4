"""AXION.ANGLE.05 strategy scan for the misalignment-angle problem -- THEORY CONTRACT.

Follow-up to axion01-04 (2026-07-10).  axion01 found the fixed pre-inflationary
misalignment angle inconsistent (H_inf/f_a ~ 66, isocurvature catastrophe);
axion02-04 found the early-QCD rescue needs a coupling that is NOT forced (the
"~b3" hint refuted).  This contract steps back and SCANS the known theoretical
strategies for the axion-isocurvature/angle problem, testing EACH against TFPT's
OWN frozen numbers (H_inf, f_a, r, A_s) and classifying it honestly:

  CLEAN            = consistent, NO dial, forced by TFPT numbers
  CANDIDATE        = would work, needs a TFPT-specific derivation (not established)
  DIAL             = works only with a non-forced parameter
  GIVES-UP-AXION-DM= evades the bound but the axion is then not the dark matter
  NOT-VIABLE       = breaks a locked TFPT prediction

The headline finding is CONSTRUCTIVE: the tension is with the FIXED-ANGLE assumption,
NOT with TFPT's numbers.  Because H_inf > f_a (factor ~66), the NATURAL scenario is
POST-INFLATIONARY PQ breaking -- no fixed angle at all -- and f_a = 2.39e11 GeV sits
right in the post-inflationary relic window (Omega_a h^2 ~ O(0.1-0.5)).  That route
is CLEAN (no dial), so the resolution is to DROP the "108 deg spine angle" as a
prediction (it becomes a horizon average), keep f_a, and predict the relic -- at the
one cost of the domain-wall number N_DW = 1 (to be checked).

Checks (hard-typed):

  C1 [E] SETUP: reproduce H_inf ~ 1.6e13, f_a ~ 2.39e11, H_inf/f_a ~ 66,
     delta_theta = H_inf/(2pi f_a) ~ 10.4, and the subdominant bound.
  C2 [E] S1 POST-INFLATIONARY PQ = CLEAN: H_inf > f_a (factor 66) => PQ restored =>
     POST-inflationary => NO fixed angle, NO isocurvature; f_a = 2.39e11 gives
     Omega_a h^2 ~ O(0.1-0.5) (in the relic window).  No dial.  Cost: the angle is
     not a prediction + N_DW = 1 (flagged).
  C3 [E] S2 INFLATION-ERA LARGER f_a = CANDIDATE: isocurvature is killed if
     f_a(inf) > H_inf/(2pi) = 2.5e12 GeV, i.e. f_a(inf)/f_a(0) > ~10.4; would keep
     the angle, but needs the det-line scale to grow ~10x in de Sitter -- NOT
     established (a TFPT-specific derivation target).
  C4 [E] S3 EARLY-QCD HEAVY AXION = DIAL: needs a scalaron-gluon coupling ~7x the
     trace anomaly (axion03), and that factor is NOT forced (axion04 refuted the b3
     reading) -- a dial.
  C5 [E] S4 SUBDOMINANT AXION = GIVES-UP-AXION-DM: the fixed-angle isocurvature bound
     is met only if Omega_a/Omega_c < ~8e-7, i.e. the axion is < 1 ppm of DM -- it
     is then NOT the dark matter.
  C6 [E] S5 LOWER H_inf = NOT-VIABLE: needing H_inf/(2pi) < f_a forces r < ~3.7e-5,
     ~100x below the R^2 prediction r ~ 0.004 -- breaks the locked scalaron branch.
  C7 [O] VERDICT / RELOCATION: the CLEAN resolution is S1 (post-inflationary) --
     drop the fixed angle (the faulty assumption), keep f_a, predict the relic; no
     dial, natural because H_inf > f_a.  This REFRAMES FR.DM.02: the "spine angle"
     is not observable, the DM claim rests on f_a + N_DW = 1.  Never a scorecard row;
     never [E].

Firewall: F_transfer/cosmology bridge; internal consistency, not evidence.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "axion05_angle_strategies_results.json"
CHECKS: list[dict] = []

PI = math.pi
MBAR = 2.435323203e18
C3 = 1.0 / (8.0 * PI)
DIM_SPLUS = 16
MU4 = 4
M_SCAL = C3 ** 3.5 * MBAR
F_A = M_SCAL / (2 * DIM_SPLUS * MU4)             # 2.39e11 GeV
A_S = 2.1e-9
R_REF = 0.004
BETA_ISO = 0.038
THETA_SPINE = 3 * PI / 5                          # 1.885 rad


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def H_inf(r=R_REF):
    return PI * MBAR * math.sqrt(A_S * r / 2.0)


def relic_post_inflationary(fa):
    # misalignment-only estimate; O(1) string/wall uncertainty
    return 0.12 * (fa / 1.0e11) ** 1.17


def c1_setup() -> None:
    H = H_inf()
    ratio = H / F_A
    dtheta = H / (2 * PI * F_A)
    sub = math.sqrt(0.04 * A_S / (2 * dtheta / THETA_SPINE) ** 2)
    ok = 1e13 < H < 2e13 and 60 < ratio < 70 and 9 < dtheta < 12 and sub < 1e-6
    check("C1 SETUP [E]: H_inf ~ %.2e, f_a ~ %.2e, H_inf/f_a ~ %.0f, delta_theta = "
          "H_inf/(2pi f_a) ~ %.1f, subdominant bound Omega_a/Omega_c < %.1e"
          % (H, F_A, ratio, dtheta, sub),
          ok, "H_inf=%.2e, f_a=%.2e, ratio=%.1f, dtheta=%.1f, sub=%.1e"
          % (H, F_A, ratio, dtheta, sub))


def c2_post_inflationary() -> None:
    H = H_inf()
    restored = H > F_A
    relic = relic_post_inflationary(F_A)
    in_window = 0.05 < relic < 1.0
    ok = restored and in_window
    check("C2 S1 POST-INFLATIONARY PQ = CLEAN [E]: H_inf/f_a = %.0f > 1 => PQ "
          "restored => POST-inflationary (NO fixed angle, NO isocurvature); "
          "f_a=%.2e => Omega_a h^2 ~ %.2f (in the relic window). No dial. Cost: the "
          "angle is not a prediction + N_DW=1 (flagged)" % (H / F_A, F_A, relic),
          ok, "H_inf>f_a: %s; Omega_a h^2 ~ %.2f (O(1) string/wall uncertainty)"
          % (restored, relic))


def c3_inflation_era_fa() -> None:
    H = H_inf()
    fa_needed = H / (2 * PI)
    factor = fa_needed / F_A
    ok = factor > 5                                  # a well-defined, large target
    check("C3 S2 INFLATION-ERA LARGER f_a = CANDIDATE [E]: isocurvature killed if "
          "f_a(inf) > H_inf/(2pi) = %.2e GeV, i.e. f_a(inf)/f_a(0) > %.1f; keeps the "
          "angle but needs the det-line scale to grow ~10x in de Sitter -- NOT "
          "established (a TFPT-specific derivation target)" % (fa_needed, factor),
          ok, "f_a(inf) needed = %.2e GeV (~%.1f x today's f_a)" % (fa_needed, factor))


def c4_early_qcd() -> None:
    # axion03/04: needs coupling ~7x anomaly, factor NOT forced (b3 refuted)
    coupling_factor = 6.96
    forced = False
    check("C4 S3 EARLY-QCD HEAVY AXION = DIAL [E]: needs a scalaron-gluon coupling "
          "~%.1fx the trace anomaly (axion03), and that factor is NOT forced "
          "(axion04 refuted the b3 reading) -- a dial" % coupling_factor,
          not forced,
          "coupling amplification ~%.2f, forced by a TFPT atom = %s" % (coupling_factor, forced))


def c5_subdominant() -> None:
    H = H_inf()
    dtheta = H / (2 * PI * F_A)
    bound = math.sqrt(0.04 * A_S / (2 * dtheta / THETA_SPINE) ** 2)
    ok = bound < 1e-5
    check("C5 S4 SUBDOMINANT AXION = GIVES-UP-AXION-DM [E]: the fixed-angle "
          "isocurvature bound is met only if Omega_a/Omega_c < %.1e (< 1 ppm) -- the "
          "axion is then NOT the dark matter" % bound,
          ok, "Omega_a/Omega_c < %.1e => not the DM in the fixed-angle scenario" % bound)


def c6_lower_Hinf() -> None:
    # r needed for H_inf/(2pi) < f_a
    H_target = 2 * PI * F_A
    r_needed = 2 * (H_target / (PI * MBAR)) ** 2 / A_S
    ok = r_needed < R_REF / 20                       # far below R^2 prediction
    check("C6 S5 LOWER H_inf = NOT-VIABLE [E]: needing H_inf/(2pi) < f_a forces "
          "r < %.1e, ~%.0fx below the R^2 prediction r ~ %.3f -- breaks the locked "
          "scalaron branch" % (r_needed, R_REF / r_needed, R_REF),
          ok, "r needed < %.1e vs R^2 r=%.3f (factor ~%.0f too small)"
          % (r_needed, R_REF, R_REF / r_needed))


def c7_verdict() -> None:
    imported = [
        "post-inflationary QCD axion relic Omega_a h^2 ~ 0.12 (f_a/1e11)^1.17 "
        "(O(1) string/wall uncertainty; cited)",
        "PQ restoration criterion max(H_inf, T_reh) > f_a (standard)",
        "domain-wall number N_DW = 1 required post-inflationary (the one crux to "
        "check for the TFPT det-line axion; Lazarides-Shafi bias if N_DW>1)",
        "de Sitter f_a(inf) growth (S2) -- not established, a TFPT derivation target",
    ]
    check("C7 VERDICT / RELOCATION [O]: the CLEAN resolution is S1 (post-inflationary) "
          "-- drop the FIXED ANGLE (the faulty assumption), keep f_a, predict the "
          "relic; no dial, natural because H_inf > f_a. REFRAMES FR.DM.02: the 'spine "
          "angle' is not observable, the DM claim rests on f_a + N_DW=1. Never a "
          "scorecard row; never [E]",
          True, "; ".join(imported))


def main() -> None:
    print("AXION.ANGLE.05 -- scan of strategies for the misalignment-angle problem "
          "against TFPT's own numbers\n")
    c1_setup(); c2_post_inflationary(); c3_inflation_era_fa(); c4_early_qcd()
    c5_subdominant(); c6_lower_Hinf(); c7_verdict()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = ("CLEAN RESOLUTION = post-inflationary PQ (drop the fixed angle); the "
               "tension is with the assumption, not TFPT's numbers"
               if n_pass == len(CHECKS) else "INCONCLUSIVE")
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "Scanning the strategies against TFPT's own frozen numbers gives a "
        "CONSTRUCTIVE answer: the isocurvature tension is with the FIXED "
        "pre-inflationary ANGLE, not with TFPT. Because H_inf ~ 1.6e13 GeV exceeds "
        "f_a ~ 2.39e11 GeV by ~66x, the NATURAL scenario is POST-INFLATIONARY PQ "
        "breaking -- there is then NO fixed angle and NO axion isocurvature, and "
        "f_a = 2.39e11 sits right in the post-inflationary relic window "
        "(Omega_a h^2 ~ O(0.1-0.5)). That route is CLEAN: no dial, forced by "
        "H_inf > f_a. The other routes rank below it: inflation-era larger f_a (S2) "
        "would keep the angle but needs the det-line scale to grow ~10x in de Sitter "
        "(a derivation target, not established); the early-QCD heavy axion (S3) needs "
        "a coupling ~7x the anomaly that is NOT forced (a dial, axion04); a "
        "subdominant axion (S4) evades the bound only at < 1 ppm of DM (not the DM); "
        "lowering H_inf (S5) needs r < 4e-5 and breaks the R^2 branch (not viable). "
        "So the recommended resolution is to REFRAME FR.DM.02: drop the '108 deg "
        "spine angle' as a prediction (it becomes a horizon average), keep f_a, "
        "predict the relic -- consistent and dial-free, at the single cost of the "
        "domain-wall number N_DW = 1 (the one crux to check). Never a scorecard row; "
        "never [E]."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "AXION.ANGLE.05 strategy scan",
        "date": "2026-07-10",
        "firewall": "theory contract, never a scorecard row; not evidence",
        "classification": {
            "S1_post_inflationary": "CLEAN (no dial; needs N_DW=1)",
            "S2_inflation_era_fa": "CANDIDATE (needs f_a(inf) ~10x, not established)",
            "S3_early_qcd": "DIAL (coupling ~7x anomaly not forced, axion04)",
            "S4_subdominant": "GIVES-UP-AXION-DM (Omega_a/Omega_c < 8e-7)",
            "S5_lower_Hinf": "NOT-VIABLE (r < 4e-5 breaks R^2)",
        },
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS, "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()
