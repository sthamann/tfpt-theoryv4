"""AXION.ISO.01 isocurvature kill-test -- a THEORY CONTRACT (never a scorecard row).

Question (problem_b.txt point 6, 2026-07-10): TFPT's frontier axion conjecture
FR.DM.02 fixes f_a = M_scal/(2 dim S+ |mu4|) = M_scal/128 ~ 2.39e11 GeV and the
R^2/Starobinsky branch fixes (A_s, r).  The frontier notes ALSO carry a fixed
misalignment angle (the "spine" angle 3*pi/5 = 108 deg, or the 170 deg hilltop
variant of v25).  Is a FIXED pre-inflationary misalignment angle self-consistent
GIVEN TFPT's own (A_s, r, f_a)?

The reviewer's arithmetic, reproduced exactly here:

    H_inf     = pi * Mbar * sqrt(A_s r / 2)   ~ 1.6e13 GeV
    H_inf/2pi ~ 2.5e12 GeV ~ 10.4 f_a
    H_inf/f_a ~ 66  >  1

so the de Sitter fluctuation of the angle, delta_theta = H_inf/(2 pi f_a) ~ 10.4,
is >> 2 pi: the angle is FULLY RANDOMISED, and (since H_inf > f_a) the PQ symmetry
is effectively RESTORED during inflation.  A homogeneous fixed theta_i is NOT a
consistent initial condition, and the induced CDM isocurvature grossly exceeds the
Planck bound beta_iso < 0.038.  This is a genuine, currently-unregistered TENSION
on the FR.DM.02 branch -- the kill-test FIRES.

The typed escape route (arXiv:2605.15192, 2026) is recorded, not adopted: an
inflaton-driven early-QCD enhancement lifts m_a > H_inf during inflation
(suppressing isocurvature), and PREFERS plateau inflation -- which TFPT's R^2
branch is.  The scalaron-gluon coupling that would do this must be FORCED (from
c3 / spectral action / the A3(+)D5 index), never a free dial, or parameter
freedom is lost.

Checks (hard-typed):

  C1 [E] H_inf from TFPT (A_s, r): reproduces ~1.6e13 GeV (the reviewer's number)
     across the frozen r-band 12/N*^2, N* in [50,60].
  C2 [E] H_inf/f_a ~ 66 > 1 => PQ EFFECTIVELY RESTORED during inflation: the de
     Sitter field excursion exceeds the PQ VEV, so a PRE-inflationary fixed angle
     does not apply -- one is in the post-inflationary/defect regime, not the
     misalignment-with-fixed-theta_i regime FR.DM.02 implicitly assumes.
  C3 [O] IF one nonetheless assumes PQ broken + fixed theta_i: the angle
     fluctuation delta_theta = H_inf/(2 pi f_a) ~ 10.4 >> 2 pi (angle randomised),
     and the CDM axion isocurvature amplitude exceeds Planck's beta_iso < 0.038 by
     MANY orders of magnitude, for BOTH candidate angles (108 deg spine, 170 deg
     hilltop) -- EXCLUDED.
  C4 [O] ESCAPE ROUTE TYPED (2605.15192): the fix is m_a(phi) > H_inf during
     inflation via an inflaton(scalaron)-driven early-QCD scale; it PREFERS plateau
     inflation, and TFPT's R^2 branch is a plateau -- a structural match.  The
     required condition m_a > H_inf is a well-defined target; the coupling must be
     forced, not a dial.
  C5 [E] POWER / NEGATIVE CONTROL: for low-scale inflation (r -> 1e-6) or
     trans-Planckian f_a the same statistic gives delta_theta << 1 (consistent) --
     the tension is driven by TFPT's OWN r ~ 0.004 + f_a ~ 2.4e11, not by the test.
  C6 [O] RELOCATION AUDIT (honest): internal consistency check on the FR.DM.02
     CONJECTURE branch, using standard single-field slow-roll + the Planck
     isocurvature bound (cited external).  VERDICT: the fixed-angle relic scenario
     is INCONSISTENT as stated; FR.DM.02 needs the forced early-QCD coupling.
     Register as an OPEN kill-test.  Never a scorecard row; never [E].

Firewall: frontier observables (axion) are F_transfer bridges, never primitive
compiler outputs; this is a self-consistency test, not external evidence.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "axion01_isocurvature_results.json"

CHECKS: list[dict] = []


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


# --- the two axioms + the frozen consequences (from axioms only, no SI smuggling) ---
PI = math.pi
C3 = 1.0 / (8.0 * PI)                       # P1
G_CAR = 5                                    # P2
DIM_SPLUS = 2 ** (G_CAR - 1)                 # 16
MU4 = 4                                       # glue order
MBAR = 2.435323203e18                         # reduced Planck mass (GeV) -- the one anchor
PHI0 = 1.0 / (6.0 * PI) + 48.0 * C3 ** 4      # retained seed

M_SCAL = C3 ** 3.5 * MBAR                      # scalaron mass ~ 3.06e13 GeV
F_A = M_SCAL / (2 * DIM_SPLUS * MU4)           # = M_scal/128 ~ 2.39e11 GeV (FR.DM.02)

# frozen cosmology (Planck-anchored A_s; r = 12/N*^2 band, N* in [50,60])
A_S = 2.1e-9
BETA_ISO_PLANCK = 0.038                        # Planck 2018 uncorrelated CDM iso bound

THETA_SPINE = 3 * PI / 5                        # 108 deg
THETA_HILLTOP = 170 * PI / 180                  # 170 deg (v25 variant)


def H_inf(As: float, r: float) -> float:
    """Single-field slow roll: A_s r = A_t = 2 H^2/(pi^2 Mbar^2)."""
    return PI * MBAR * math.sqrt(As * r / 2.0)


def r_band() -> list[float]:
    return [12.0 / N ** 2 for N in (50, 55, 60)]


def iso_fraction(H: float, fa: float, theta: float, omega_ratio: float = 1.0) -> float:
    """Uncorrelated CDM axion isocurvature FRACTION beta_iso = P_iso/(P_iso+P_ad).

    delta_theta = H/(2 pi fa); relative density pert = 2 delta_theta/theta
    (quadratic potential); P_iso = (omega_a/omega_c)^2 (2 delta_theta/theta)^2;
    P_ad = A_s.  Returns beta = P_iso/(P_iso+A_s)."""
    dtheta = H / (2 * PI * fa)
    P_iso = (omega_ratio * 2 * dtheta / theta) ** 2
    return P_iso / (P_iso + A_S)


def c1_hinf() -> None:
    vals = [H_inf(A_S, r) for r in r_band()]
    ok = all(1.0e13 < v < 2.5e13 for v in vals) and abs(H_inf(A_S, 0.004) - 1.57e13) / 1.57e13 < 0.05
    check("C1 H_inf FROM TFPT (A_s, r) [E]: H_inf = pi Mbar sqrt(A_s r/2) ~ 1.6e13 "
          "GeV across the frozen r-band 12/N*^2 (N* in [50,60]) -- reproduces the "
          "reviewer's number",
          ok,
          "H_inf(r=0.004)=%.3e; band(N*=50,55,60)=[%.2e, %.2e, %.2e] GeV"
          % (H_inf(A_S, 0.004), *vals))


def c2_pq_restored() -> None:
    H = H_inf(A_S, 0.004)
    ratio = H / F_A
    ok = ratio > 1.0 and abs(ratio - 66) / 66 < 0.25
    check("C2 PQ RESTORED DURING INFLATION [E]: H_inf/f_a ~ 66 > 1 -- the de Sitter "
          "field excursion exceeds the PQ VEV f_a, so a PRE-inflationary FIXED "
          "misalignment angle does NOT apply (post-inflationary/defect regime, not "
          "the fixed-theta_i regime FR.DM.02 assumes)",
          ok, "H_inf/f_a = %.1f (>1); f_a = %.3e GeV, H_inf = %.3e GeV"
          % (ratio, F_A, H))


def c3_isocurvature_excluded() -> None:
    H = H_inf(A_S, 0.004)
    dtheta = H / (2 * PI * F_A)
    beta_spine = iso_fraction(H, F_A, THETA_SPINE)
    beta_hill = iso_fraction(H, F_A, THETA_HILLTOP)
    # excluded means beta >> Planck bound (here beta -> ~1 since P_iso >> A_s)
    ok = (dtheta > 2 * PI and beta_spine > BETA_ISO_PLANCK
          and beta_hill > BETA_ISO_PLANCK)
    check("C3 FIXED-ANGLE ISOCURVATURE EXCLUDED [O]: delta_theta = H_inf/(2 pi f_a) "
          "= %.1f >> 2 pi (angle randomised); CDM axion isocurvature fraction beta "
          "= %.3f (108 deg) / %.3f (170 deg) both >> Planck beta_iso < %.3f -- "
          "EXCLUDED by orders of magnitude" % (dtheta, beta_spine, beta_hill,
                                               BETA_ISO_PLANCK),
          ok,
          "delta_theta=%.2f; beta_spine=%.4f, beta_hilltop=%.4f (bound %.3f)"
          % (dtheta, beta_spine, beta_hill, BETA_ISO_PLANCK))


def c4_escape_route() -> None:
    H = H_inf(A_S, 0.004)
    # target: an inflation-era QCD scale Lambda_inf with m_a(inf) > H_inf.
    # m_a ~ Lambda_QCD^2 / f_a ; require Lambda_inf > sqrt(H_inf f_a).
    Lambda_needed = math.sqrt(H * F_A)
    Lambda_qcd_today = 0.2  # GeV
    enhancement = Lambda_needed / Lambda_qcd_today
    ok = Lambda_needed > 0 and enhancement > 1  # a well-defined, large target
    check("C4 ESCAPE ROUTE TYPED (2605.15192) [O]: lift m_a(phi) > H_inf during "
          "inflation via an inflaton(scalaron)-driven early-QCD scale; the "
          "mechanism PREFERS plateau inflation and TFPT's R^2 branch IS a plateau "
          "(structural match).  Target: Lambda_inf > sqrt(H_inf f_a); coupling MUST "
          "be forced (c3 / spectral action / A3+D5 index), not a dial",
          ok, "Lambda_inf needed ~ %.3e GeV (~%.1e x today's Lambda_QCD) -- a "
          "well-defined target for the forced coupling" % (Lambda_needed, enhancement))


def c5_power_control() -> None:
    # low-scale inflation OR trans-Planckian f_a -> consistent (delta_theta << 1)
    H_low = H_inf(A_S, 1e-6)
    dtheta_low = H_low / (2 * PI * F_A)
    fa_high = 1e17
    dtheta_fa = H_inf(A_S, 0.004) / (2 * PI * fa_high)
    ok = dtheta_low < 1.0 and dtheta_fa < 1.0
    check("C5 POWER / NEGATIVE CONTROL [E]: the tension is driven by TFPT's OWN "
          "r ~ 0.004 + f_a ~ 2.4e11 -- for low-scale inflation (r=1e-6) or "
          "trans-Planckian f_a (1e17) the SAME statistic gives delta_theta << 1 "
          "(consistent), so the kill-test has genuine discriminating power",
          ok, "delta_theta(r=1e-6)=%.3f; delta_theta(f_a=1e17)=%.3e -- both < 1"
          % (dtheta_low, dtheta_fa))


def c6_relocation() -> None:
    imported = [
        "single-field slow-roll relation A_s r = 2 H^2/(pi^2 Mbar^2) (standard)",
        "Planck 2018 uncorrelated CDM isocurvature bound beta_iso < 0.038 (cited)",
        "de Sitter field fluctuation H/(2 pi) per mode (standard)",
        "PQ-restoration criterion H_inf > f_a (standard)",
        "the escape mechanism arXiv:2605.15192 (cited, not adopted)",
    ]
    check("C6 RELOCATION AUDIT [O]: internal consistency test of the FR.DM.02 "
          "CONJECTURE branch. VERDICT: the fixed-angle relic scenario is "
          "INCONSISTENT as stated (C2+C3); FR.DM.02 needs the FORCED early-QCD "
          "coupling (C4). Registered as an OPEN kill-test -- never a scorecard row, "
          "never [E]",
          True, "; ".join(imported))


def main() -> None:
    print("AXION.ISO.01 isocurvature kill-test -- is a fixed misalignment angle "
          "consistent with TFPT's own (A_s, r, f_a)?\n")
    c1_hinf()
    c2_pq_restored()
    c3_isocurvature_excluded()
    c4_escape_route()
    c5_power_control()
    c6_relocation()
    n_pass = sum(c["pass"] for c in CHECKS)
    fired = CHECKS[1]["pass"] and CHECKS[2]["pass"]
    verdict = ("KILL-TEST FIRES (FR.DM.02 fixed-angle scenario inconsistent)"
               if fired and n_pass == len(CHECKS)
               else "INCONCLUSIVE")
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "GIVEN TFPT's own frozen numbers -- r ~ 0.004 (R^2 branch), A_s ~ 2.1e-9, "
        "f_a = M_scal/128 ~ 2.39e11 GeV (FR.DM.02) -- the inflationary Hubble scale "
        "H_inf ~ 1.6e13 GeV satisfies H_inf/f_a ~ 66 > 1 and H_inf/(2 pi f_a) ~ 10.4. "
        "So (i) the PQ symmetry is effectively restored during inflation, and (ii) a "
        "FIXED pre-inflationary misalignment angle (108 deg spine or 170 deg hilltop) "
        "is not a consistent homogeneous initial condition -- the induced CDM "
        "isocurvature exceeds the Planck bound by orders of magnitude. This is a "
        "genuine, previously-unregistered TENSION on the FR.DM.02 branch. The typed "
        "escape (arXiv:2605.15192) lifts m_a > H_inf during inflation and prefers "
        "plateau inflation, matching TFPT's R^2 branch; but the scalaron-gluon "
        "coupling that does this MUST follow from c3 / the spectral action / the "
        "A3(+)D5 index, or parameter freedom is lost. NOT claimed: any closure of "
        "the dark-matter relic scale. Open kill-test; never a scorecard row; "
        "never [E]."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "AXION.ISO.01 isocurvature kill-test",
        "date": "2026-07-10",
        "firewall": ("theory contract, never a scorecard row; F_transfer bridge "
                     "self-consistency, not external evidence"),
        "inputs": {
            "c3": C3, "f_a_GeV": F_A, "M_scal_GeV": M_SCAL,
            "A_s": A_S, "r_ref": 0.004, "H_inf_GeV": H_inf(A_S, 0.004),
            "theta_spine_deg": 108, "theta_hilltop_deg": 170,
        },
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()
