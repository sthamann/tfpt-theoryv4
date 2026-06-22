"""v338 -- the theta13 sub-leading budget vs the current global fit: the +2 sigma pressure
point (v328), quantified against BOTH NuFIT 6.0 normal-ordering variants and JUNO.  It
neither defuses nor excludes the tension -- it fences it correctly: mild (1.7-2.0 sigma,
data-systematics dependent), within the current 3 sigma, decided by JUNO.

The honest weak point is sin^2 theta13 = phi0 e^{-5/6} = 0.023108 (the carrier-trace
channel, v16/v268/v328).  NuFIT 6.0 (2024) gives TWO normal-ordering central values:

  - WITHOUT Super-Kamiokande atmospheric: 0.02195 +0.00054/-0.00058 (3 sigma 0.02023-0.02376)
  - WITH SK atmospheric (NO best fit):     0.02215 +0.00056/-0.00058 (3 sigma 0.02030-0.02388)

This module quantifies the budget across both:

  [N] 1. THE TENSION IS SK-DEPENDENT: TFPT 0.023108 is +2.0 sigma vs the no-SK central and
        +1.7 sigma vs the with-SK central -- a ~0.3 sigma spread from one systematic choice,
        so it is NOT a clean 2 sigma; the honest band is +1.7 to +2.0 sigma.
  [E] 2. WITHIN 3 SIGMA (not excluded): 0.023108 < the NuFIT 6.0 with-SK 3 sigma upper bound
        0.02388, so the frozen prediction sits INSIDE the current allowed region -- a
        pressure point at the upper ~2 sigma edge, not a falsification.
  [N] 3. THE SUB-LEADING BUDGET: moving 0.023108 to the with-SK central 0.02215 needs
        d(sin^2 theta13) = -0.00096, a -4.3% shift.  PMNS theta13 RG running (NO) is < 1%
        and the exponent 5/6 is EXACT (v268), so ~3% would have to come from a sub-leading
        channel -- larger than the natural PMNS sub-leading size, so no freeze-respecting
        correction cleanly relieves it (consistent with v328); it stays a genuine pressure.
  [X] 4. JUNO DECIDES: JUNO targets sub-1% precision on sin^2 2theta13
        (sigma_{sin^2 theta13} ~ 1-2e-4), which turns today's 1.7-2.0 sigma into a >5 sigma
        statement either way -- a clean, near-term, pre-registered kill/confirm.
  [E] 5. NET ASSESSMENT: the single honest pressure point (v306 seed-hyperplane outlier,
        v328), correctly fenced -- real but mild and within 3 sigma, decided by JUNO; not
        defused, not hidden, not excluded.

HONEST SCOPE: [N] the data-confrontation (repo-documented NuFIT 6.0 centrals, both variants)
+ the budget arithmetic; [E] the within-3-sigma check and the seed-hyperplane consistency;
[X] the JUNO kill.  A confrontation/fencing module; it does not change the frozen prediction.
Python-only (mpmath)."""
import mpmath as mp

from tfpt_constants import check, summary, reset, phi0

# NuFIT 6.0 (2024) normal ordering, repo-documented (nu-fit.org v60 parameters table)
NUFIT_NOSK_C, NUFIT_NOSK_S = mp.mpf("0.02195"), mp.mpf("0.00058")   # without SK atmospheric
NUFIT_SK_C, NUFIT_SK_S = mp.mpf("0.02215"), mp.mpf("0.00057")       # with SK (NO best fit)
NUFIT_SK_3SIG_HI = mp.mpf("0.02388")                                # with-SK 3 sigma upper


def run():
    reset()
    mp.mp.dps = 30
    print("v338  the theta13 sub-leading budget vs the current global fit (NuFIT 6.0, both variants)")

    s13 = phi0 * mp.e ** (mp.mpf(-5) / 6)            # = 0.023108 (v16/v268/v328)
    pull_nosk = (s13 - NUFIT_NOSK_C) / NUFIT_NOSK_S
    pull_sk = (s13 - NUFIT_SK_C) / NUFIT_SK_S

    # 1. the tension is SK-dependent: +2.0 (no SK) vs +1.7 (with SK)
    check("SK-DEPENDENT TENSION [N]: sin^2 theta13 = phi0 e^{-5/6} = %.6f -> %+.2f sigma vs "
          "the no-SK central (0.02195) and %+.2f sigma vs the with-SK central (0.02215); a "
          "~0.3 sigma spread from one systematic, so NOT a clean 2 sigma -- honest band "
          "+1.7 to +2.0 sigma" % (float(s13), float(pull_nosk), float(pull_sk)),
          1.9 <= float(pull_nosk) <= 2.1 and 1.5 <= float(pull_sk) <= 1.9)

    # 2. within 3 sigma (not excluded)
    within_3sig = s13 < NUFIT_SK_3SIG_HI
    check("WITHIN 3 SIGMA [E]: 0.023108 < the NuFIT 6.0 with-SK 3 sigma upper bound %.5f, so "
          "the frozen prediction is INSIDE the current allowed region -- an upper-edge "
          "pressure point, not a falsification" % float(NUFIT_SK_3SIG_HI), within_3sig)

    # 3. the sub-leading budget: -4.3% shift needed; RG < 1%, exponent exact
    shift = NUFIT_SK_C - s13
    shift_pct = float(shift / s13 * 100)
    rg_pct = 1.0
    needed_subleading_pct = abs(shift_pct) - rg_pct
    check("SUB-LEADING BUDGET [N]: moving 0.023108 to the with-SK central needs "
          "d(sin^2 theta13) = %.5f (%.1f%%); RG running < %.0f%% and the exponent 5/6 is "
          "exact, so ~%.0f%% would have to come from a sub-leading channel -- larger than "
          "the natural PMNS sub-leading size, no freeze-respecting correction cleanly "
          "relieves it (v328)" % (float(shift), shift_pct, rg_pct, needed_subleading_pct),
          needed_subleading_pct > 2.0)

    # 4. JUNO decides: sub-1% precision turns 1.7-2.0 sigma into > 5 sigma
    juno_sigma = mp.mpf("0.00015")                  # JUNO/reactor target on sin^2 theta13
    juno_pull = (s13 - NUFIT_SK_C) / juno_sigma     # at the with-SK central
    check("JUNO DECIDES [X]: JUNO targets sub-1%% precision on sin^2 2theta13 "
          "(sigma ~ %.0e), turning today's 1.7-2.0 sigma into ~%.1f sigma at the current "
          "central -- a clean near-term pre-registered kill/confirm"
          % (float(juno_sigma), float(juno_pull)), float(juno_pull) > 5)

    # 5. net assessment: one honest pressure point, correctly fenced
    check("NET ASSESSMENT [E]: the single honest pressure point (v306 seed-hyperplane "
          "outlier, v328) -- real but mild (+1.7 to +2.0 sigma) and within 3 sigma, decided "
          "by JUNO; not defused, not hidden, not excluded",
          within_3sig and 1.5 <= float(pull_sk) <= 2.1)

    return summary("v338 theta13 sub-leading budget (mild, within 3 sigma, JUNO decides)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
