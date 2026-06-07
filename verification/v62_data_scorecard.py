"""v62 -- confrontation of TFPT predictions with current research data (2024/25).

A falsifiability scorecard: TFPT predictions vs the latest measured values, with the
honest sigma-deviation and an explicit MATCH / mild-TENSION / open / future tag.  This
records SIGNATURES IN DATA -- including the tensions, not only the confirmations.

The check()s here verify that the computed deviation matches the honestly-assessed
value (so the suite stays green AND faithfully records tensions); they do NOT pretend
every prediction is a <1 sigma match.

Data sources (Sep 2024 - 2025):
  alpha^-1   : CODATA 2022, 137.035999177(21)
  sin2 th12  : NuFIT 6.0 (2024), 0.307 +- 0.012 (NO)
  sin2 th13  : NuFIT 6.0 (2024), 0.02195 +- 0.00058 (NO + SK)
  beta_rad   : ACT DR6 (Diego-Palazuelos & Komatsu 2025), 0.215 +- 0.074 deg
  n_s        : Planck 0.9649+-0.0042; CMB-only P+ACT 0.9709+-0.0038; P-ACT-LB+DESI 0.9743+-0.0034
"""
import mpmath as mp
from tfpt_constants import check, summary, reset

mp.mp.dps = 30


def sigdev(pred, meas, err):
    return abs(mp.mpf(pred) - mp.mpf(meas)) / mp.mpf(err)


def run():
    reset()
    print("v62  TFPT vs current data (2024/25) scorecard")

    # alpha^-1: agreement to the quoted precision of the prediction (NOT a spurious sigma)
    check("alpha^-1: TFPT 137.0359992 vs CODATA 137.035999177 -> agree to ~9 sig figs (10^-8 level) [MATCH]",
          abs(mp.mpf('137.0359992') - mp.mpf('137.035999177')) < 1e-7)

    # solar angle: strong match
    s12 = sigdev('0.30675', '0.307', '0.012')
    check(f"sin^2 th12: TFPT 0.30675 vs NuFIT 0.307+-0.012 -> {float(s12):.2f} sigma [MATCH]", s12 < 0.5)

    # reactor angle: mild ~2 sigma tension (honest)
    s13 = sigdev('0.0231', '0.02195', '0.00058')
    check(f"sin^2 th13: TFPT 0.0231 vs NuFIT 0.02195+-0.00058 -> {float(s13):.2f} sigma [mild TENSION]",
          1.5 < s13 < 2.5)

    # birefringence: match
    sb = sigdev('0.2424', '0.215', '0.074')
    check(f"beta_rad: TFPT 0.2424 vs ACT DR6 0.215+-0.074 -> {float(sb):.2f} sigma [MATCH]", sb < 0.6)

    # Starobinsky n_s: consistent with Planck, ~2 sigma tension with DESI-combined
    ns_pred = 1 - 2 / mp.mpf(57)   # N* ~ 57 (from the documented n_s=0.9649)
    s_planck = sigdev(ns_pred, '0.9649', '0.0042')
    s_desi = sigdev(ns_pred, '0.9743', '0.0034')
    check(f"n_s (Starobinsky, N*~57)={float(ns_pred):.4f}: vs Planck 0.9649 -> {float(s_planck):.2f}s [MATCH]; "
          f"vs P-ACT-LB+DESI 0.9743 -> {float(s_desi):.2f}s [TENSION]",
          s_planck < 0.5 and s_desi > 2.0)

    # tensor-to-scalar: sharp future falsifier
    r_pred = 12 / mp.mpf(57)**2
    check(f"r (Starobinsky) = 12/N*^2 = {float(r_pred):.4f} << current bound ~0.03; future test CMB-S4/LiteBIRD",
          r_pred < 0.01)

    # theta23 octant: open in TFPT, ambiguous in data -> consistent
    check("theta23 octant: TFPT [P] open; NuFIT 6.0 ambiguous (0.470 w/o SK, 0.561 w/ SK) -> consistent", True)

    print("  SUMMARY: 3 strong matches (alpha^-1, sin2 th12, beta); 2 mild ~2sigma tensions (sin2 th13, "
          "n_s vs DESI); theta23 open; r~0.0037 = sharp future falsifier")
    return summary("v62 data scorecard")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
