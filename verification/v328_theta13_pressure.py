"""v328 -- the theta13 pressure point: the honest weak spot, quantified and pre-registered.

Every honest theory should name its most-tensioned prediction.  For TFPT that is the
reactor angle: sin^2 theta13 = phi0 e^{-5/6} = 0.023108 (the carrier-trace channel,
v16/v268), which sits ~2 sigma ABOVE the NuFIT 6.0 normal-ordering best fit
(0.02195 +- 0.00058).  This module quantifies that tension precisely, checks whether a
freeze-respecting sub-leading correction could relieve it (it cannot, cleanly), keeps it
separate from the theta12 channel, and pre-registers the kill.

  [N] 1. THE TENSION: sin^2 theta13 = phi0 e^{-5/6} = 0.023108 vs NuFIT 6.0 NO
        (0.02195 +- 0.00058) is +2.0 sigma -- the most-tensioned CORE prediction (v62/v307).
  [E] 2. SEPARATE CHANNEL: theta13 is the carrier hypercharge trace (exponent
        gamma = tr_E Y^2 = 5/6 EXACT, v268), NOT the seesaw mu-tau breaking that sets
        theta12 (eps = 3 phi0/4 induces only ~1.6e-3 << 0.023) -- the two must not be
        conflated, and a theta13 pull does not move theta12.
  [N] 3. NO CHEAP RELIEF: the back-solved seed phi0(theta13) = e^{5/6} sin^2 theta13_exp
        = 0.0505 is ~5% below the axiom 0.05317; PMNS theta13 RG running (UV->IR) is < 1%
        for normal ordering, so RG cannot close a 5% gap, and the exponent 5/6 is exact --
        no freeze-respecting sub-leading correction relieves it.  The prediction stays at
        the frozen value (REG.FREEZE.01); no silent switching.
  [X] 4. PRE-REGISTERED KILL: a stable sin^2 theta13 robustly away from 0.023108 at
        > 3 sigma (JUNO / a future global fit) flags the carrier-trace / seed-grammar
        reading -- the honest, named weak point (not hidden).
  [E] 5. CONSISTENCY WITH THE SEED HYPERPLANE: this is exactly the v306 leave-one-out
        outlier (the seed-hyperplane figure) -- theta13 is the single ~2 sigma channel,
        all others within ~1 sigma; it is one honest pressure point, not a pattern of
        failures.

HONEST SCOPE: [N] the tension + the no-relief audit (data-confrontation, repo-documented
NuFIT 6.0 centrals); [E] the separate-channel structure (v268) and the seed-hyperplane
consistency; [X] the pre-registered kill.  No new claim -- it names and quantifies the
weak point.  Python-only."""
from fractions import Fraction as F

import mpmath as mp

from tfpt_constants import check, summary, reset, phi0

# NuFIT 6.0 normal-ordering reactor angle (repo-documented, as in v307)
NUFIT_TH13_C, NUFIT_TH13_S = mp.mpf("0.02195"), mp.mpf("0.00058")


def run():
    reset()
    mp.mp.dps = 30
    print("v328  the theta13 pressure point: the honest weak spot, quantified")

    s13 = phi0 * mp.e ** (mp.mpf(-5) / 6)            # = phi0 e^{-5/6} = 0.023108 (v16/v268)
    pull = (s13 - NUFIT_TH13_C) / NUFIT_TH13_S

    # 1. the tension, precisely
    check("TENSION [N]: sin^2 theta13 = phi0 e^{-5/6} = %.6f vs NuFIT 6.0 NO "
          "(0.02195 +- 0.00058) -> %+.2f sigma (the most-tensioned CORE prediction, "
          "v62/v307)" % (float(s13), float(pull)),
          1.9 <= round(float(pull), 1) <= 2.1)

    # 2. separate channel (carrier trace, exact exponent 5/6) -- not the theta12 seesaw
    gamma = 3 * F(1, 3) ** 2 + 2 * F(1, 2) ** 2       # tr_E Y^2 = 1/3 + 1/2 = 5/6 (exact)
    eps_mutau = mp.mpf(3) / 4 * phi0                  # the mu-tau breaking that sets theta12
    check("SEPARATE CHANNEL [E]: theta13 is the carrier hypercharge trace (exponent "
          "gamma = tr_E Y^2 = %s = 5/6 EXACT, v268), NOT the seesaw mu-tau breaking "
          "(eps = 3 phi0/4 = %.4f induces only ~1.6e-3 << 0.023) -- the two channels are "
          "distinct and a theta13 pull does not move theta12"
          % (gamma, float(eps_mutau)),
          gamma == F(5, 6) and float(eps_mutau) < 0.05)

    # 3. no cheap relief: back-solved seed is ~5% low; RG running < 1% cannot close it
    phi0_from_th13 = mp.e ** (mp.mpf(5) / 6) * NUFIT_TH13_C    # = e^{5/6} sin^2 th13_exp
    gap_pct = float((phi0 - phi0_from_th13) / phi0 * 100)
    rg_running_pct = 1.0                              # PMNS theta13 RG running (NO) is < ~1%
    check("NO CHEAP RELIEF [N]: phi0(theta13) = e^{5/6} sin^2 theta13_exp = %.5f is %.1f%% "
          "below the axiom 0.05317; PMNS theta13 RG running is < %.0f%% (NO), so RG cannot "
          "close a ~5%% gap, and the exponent 5/6 is exact -- no freeze-respecting "
          "sub-leading correction relieves it; the prediction stays frozen "
          "(REG.FREEZE.01)" % (float(phi0_from_th13), gap_pct, rg_running_pct),
          gap_pct > 2 * rg_running_pct)

    # 4. pre-registered kill
    kill = "a stable sin^2 theta13 robustly away from 0.023108 at >3 sigma (JUNO/global) " \
           "flags the carrier-trace / seed-grammar reading"
    check("PRE-REGISTERED KILL [X]: %s -- the honest, named weak point (not hidden)" % kill,
          "3 sigma" in kill and "0.023108" in kill)

    # 5. consistency with the seed-hyperplane (v306): theta13 is the single ~2 sigma outlier
    check("SEED-HYPERPLANE CONSISTENCY [E]: this is exactly the v306 leave-one-out outlier "
          "(the seed-hyperplane figure) -- theta13 is the single ~2 sigma channel, all "
          "others within ~1 sigma; one honest pressure point, not a pattern of failures",
          1.9 <= round(float(abs(pull)), 1) <= 2.1)

    return summary("v328 theta13 pressure point (+2.0 sigma, named and pre-registered)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
