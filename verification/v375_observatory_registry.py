"""v375 -- OBSERVATORY.REGISTRY.01 (Track 4): the prediction OBSERVATORY -- a status-typed CI over
the frozen prediction registry (verification/freeze_file.csv) that makes the falsifiability
surface machine-checkable.  It does NOT re-derive the physics; it verifies (a) the registry is
COMPLETE (every frozen signal has a kill criterion), (b) the headline numerical predictions
re-derive from the atoms {c3, phi0}, and (c) the live scorecard -- each headline prediction's
sigma-distance to the CURRENT measurement -- is internally consistent and correctly typed.

This is the "make the closed pieces usable and the open pieces honestly fenced" infrastructure:
one runnable artifact that turns the registry into a verified scorecard, with the most-tensioned
prediction (theta13) flagged and the recently-updated data (JUNO first run, ACT DR6) recorded.

  [E] 1. FALSIFIABILITY COMPLETE.  every row of freeze_file.csv carries a non-empty
        kill_criterion -- the prediction surface is fully killable, no orphan claims.
  [E] 2. HEADLINE VALUES FROM ATOMS.  sin^2 theta12 = 1/3 - phi0/2, sin^2 theta13 = phi0 e^{-5/6},
        beta_rad = phi0/(4 pi) (rad) re-derive from {phi0} to the registry signals.
  [N] 3. LIVE SCORECARD (current data).  theta12 vs JUNO first run (0.3092 +- 0.0087): COMPATIBLE
        (~0.3 sigma); theta13 vs NuFIT 6.0 NO (0.02195 +- 0.00058): the MOST-TENSIONED core
        prediction (~+2 sigma, the honest pressure point); beta_rad vs ACT DR6 (0.215 +- 0.074
        deg): COMPATIBLE (a hint, systematics pending); r = 12/N*^2 ~ 0.004 < BK18 0.036:
        COMPATIBLE.  All recorded with sigma-distance and status -- no cherry-picking.
  [E] 4. REGISTRY INTEGRITY.  the registry is the single machine-readable falsifiability surface
        (N predictions, each typed signal + kill); this module is its CI.

Status: [E] the completeness + atom re-derivation + integrity; [N] the live data scorecard (the
sigma-distances are data, updated as experiments report).  Tooling that verifies the prediction
surface; introduces no new physics claim.  Python (stdlib csv + mpmath atoms)."""
import csv
import math
import os

from tfpt_constants import check, summary, reset, phi0, PI


def _registry():
    path = os.path.join(os.path.dirname(__file__), "freeze_file.csv")
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run():
    reset()
    print("v375  OBSERVATORY.REGISTRY.01: a status-typed CI over the frozen prediction registry")

    rows = _registry()

    # 1. falsifiability complete: every row has a kill criterion
    missing = [r["claim"] for r in rows if not r.get("kill_criterion", "").strip()]
    check("FALSIFIABILITY COMPLETE [E]: all %d registry rows carry a non-empty kill_criterion "
          "(no orphan claims); missing = %s" % (len(rows), missing or "none"),
          len(rows) >= 18 and missing == [])

    # 2. headline values re-derive from the atoms
    s12 = 1.0 / 3 - float(phi0) / 2
    s13 = float(phi0) * math.exp(-5.0 / 6)
    beta_rad_deg = float(phi0) / (4 * float(PI)) * 180 / float(PI)
    check("HEADLINE VALUES FROM ATOMS [E]: sin^2 theta12 = 1/3 - phi0/2 = %.5f (registry ~0.3067), "
          "sin^2 theta13 = phi0 e^{-5/6} = %.5f (registry 0.023108), beta_rad = phi0/(4pi) = "
          "%.4f deg (registry 0.2424) -- all re-derive from {phi0}"
          % (s12, s13, beta_rad_deg),
          abs(s12 - 0.30675) < 1e-3 and abs(s13 - 0.023108) < 1e-3
          and abs(beta_rad_deg - 0.2424) < 1e-3)

    # 3. live scorecard: sigma-distances to the current measurements
    def sigdist(pred, mean, sig):
        return abs(pred - mean) / sig

    d12 = sigdist(s12, 0.3092, 0.0087)            # JUNO first 59.1-day run
    d13 = sigdist(s13, 0.02195, 0.00058)          # NuFIT 6.0 NO (no-SK)
    dbeta = sigdist(beta_rad_deg, 0.215, 0.074)   # ACT DR6
    r_pred = 12 / 55.0 ** 2                        # r = 12/N*^2, N* ~ 55
    check("LIVE SCORECARD [N]: theta12 vs JUNO first run (0.3092+-0.0087) = %.2f sigma (COMPATIBLE); "
          "theta13 vs NuFIT 6.0 NO (0.02195+-0.00058) = %.2f sigma (MOST-TENSIONED core prediction); "
          "beta_rad vs ACT DR6 (0.215+-0.074) = %.2f sigma (hint, systematics pending); r = 12/N*^2 "
          "= %.4f < BK18 0.036 (COMPATIBLE)" % (d12, d13, dbeta, r_pred),
          d12 < 1.0 and 1.5 < d13 < 2.6 and dbeta < 1.0 and r_pred < 0.036)

    # 4. theta13 is correctly flagged as the most-tensioned in the registry text
    theta13_row = next((r for r in rows if r["claim"] == "reactor_angle"), {})
    flagged = "most-tensioned" in theta13_row.get("tfpt_signal", "").lower()
    check("REGISTRY INTEGRITY [E]: the registry is the single machine-readable falsifiability "
          "surface (%d typed signal+kill predictions); the most-tensioned prediction (theta13, "
          "%.1f sigma) is flagged in its own row (%s) -- the observatory tells the truth about "
          "its weakest point" % (len(rows), d13, "yes" if flagged else "no"),
          len(rows) >= 18 and flagged)

    return summary("v375 OBSERVATORY.REGISTRY.01: a status-typed CI over freeze_file.csv -- all %d predictions "
                   "are killable (falsifiability complete), the headline values re-derive from {phi0}, and the "
                   "live scorecard records theta12 (~%.1f sigma vs JUNO, compatible), theta13 (~%.1f sigma vs "
                   "NuFIT, the flagged pressure point), beta_rad (~%.1f sigma vs ACT, a hint) and r<0.036 "
                   "(compatible). Tooling; no new physics" % (len(rows), d12, d13, dbeta))


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
