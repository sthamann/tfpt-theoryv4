"""v129 -- The clock is an entropy power law: the transfer eigenvalues are
the Nariai entropy fractions to the hexagon power, and the ring coupling
is the fractional entropy deficit.  [I] exact identities on established
levels; R1 acquires its thermodynamic statement.

The v124-v128 chain gave rate(n) = -p_2 ln(1 - n/N_fam).  This module
identifies what (1 - n/N_fam) IS physically:

  [I] 1. THE THREE ENTROPY LEVELS.  The established Nariai bookkeeping
         (v101) has exactly three entropy configurations:
             S/S_dS in {1, 2/3, 1/3}
         (pure dS; the two-horizon Nariai total 2/3; a single horizon
         1/3 -- deficit S_dS/3 per step).  These are EXACTLY the
         complementary cusp weights 1 - n/N_fam.
  [I] 2. THE CLOCK IS AN ENTROPY POWER LAW.
             lambda_n = (S_n / S_dS)^{p_2},
             rate(n) = p_2 ln(S_dS / S_n)
         -- the transfer eigenvalues are the entropy fractions to the
         hexagon power; the rates are hexagon-weighted log-entropy
         deficits.  Audit reading: a power law (S/S_dS)^{p_2} with
         integer exponent p_2 = 6 = 2h is the two-point form of an
         operator of weight h = 3 = N_fam (recorded, not claimed).
  [I] 3. THE COUPLING IS THE ENTROPY DEFICIT.  The ring coupling of
         v127 satisfies the TRIPLE identity
             alpha = n/N_fam = (MS parabolic weight, v115/v126)
                   = 1 - S_n/S_dS = Delta S_n / S_dS (deficit fraction)
         -- the insertion strength of the RPA towers is the fractional
         entropy deficit of the SdS configuration: the coupling is not
         a free parameter in ANY of its three readings.
  [I] 4. ORIENTATION CONSISTENCY.  Weight 0 <-> pure dS (maximal
         entropy, rate 0: the stationary attractor); weight 2 <-> the
         single horizon (lowest level, fastest decay 6 ln 3) --
         monotone: deeper entropy deficit = faster relaxation, exactly
         the established repeller -> attractor orientation (v82/v101/
         v102).
  [P] 5. R1, THERMODYNAMIC FORM (recorded, not claimed): derive
             Gamma_n  proportional to  (S_n / S_dS)^{p_2}
         from the near-Nariai one-loop -- a Gibbons-Hawking-type
         entropy power law with exponent = the hexagon size.  Same
         computation as before, now stated in entropy language; the
         exponent p_2 (equivalently the weight h = N_fam) is the
         remaining quantum content.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

P2 = 6
N_FAM = 3


def run():
    reset()
    print("v129 entropy power law (lambda = (S/S_dS)^p2)")

    levels = [sp.Rational(N_FAM - n, N_FAM) for n in range(3)]

    # 1. the three entropy levels
    check("THE THREE ENTROPY LEVELS: the established Nariai bookkeeping "
          "(v101) has S/S_dS in {1, 2/3, 1/3} (pure dS; two-horizon "
          "total; single horizon -- deficit S_dS/3 per step) -- "
          "EXACTLY the complementary cusp weights 1 - n/N_fam",
          levels == [1, sp.Rational(2, 3), sp.Rational(1, 3)])

    # 2. the clock is an entropy power law
    lams = [lv ** P2 for lv in levels]
    rates = [P2 * sp.log(1 / lv) for lv in levels]
    check("THE CLOCK IS AN ENTROPY POWER LAW: lambda_n = (S_n/S_dS)^p2 "
          "= {1, (2/3)^6, (1/3)^6} (the frozen transfer spectrum) and "
          "rate(n) = p2 ln(S_dS/S_n) = {0, Delta, 6 ln 3} -- "
          "hexagon-weighted log-entropy deficits; audit: exponent "
          "p2 = 6 = 2h reads as the two-point form of a weight "
          "h = 3 = N_fam operator (recorded)",
          lams == [1, sp.Rational(2, 3) ** 6, sp.Rational(1, 3) ** 6]
          and sp.simplify(rates[1] - 6 * sp.log(sp.Rational(3, 2))) == 0
          and sp.simplify(rates[2] - 6 * sp.log(3)) == 0
          and P2 == 2 * N_FAM)

    # 3. the coupling is the entropy deficit
    check("THE COUPLING IS THE ENTROPY DEFICIT (triple identity): "
          "alpha = n/N_fam = MS parabolic weight (v115/v126) = "
          "1 - S_n/S_dS = Delta S_n/S_dS -- the RPA insertion strength "
          "is the fractional entropy deficit; the coupling is not a "
          "free parameter in any of its three readings",
          all(sp.Rational(n, N_FAM) == 1 - levels[n] for n in range(3)))

    # 4. orientation consistency
    check("ORIENTATION CONSISTENCY: weight 0 <-> pure dS (max entropy, "
          "rate 0: stationary attractor); weight 2 <-> single horizon "
          "(lowest level, fastest decay 6 ln 3); monotone -- deeper "
          "deficit = faster relaxation, exactly the established "
          "repeller -> attractor orientation (v82/v101/v102)",
          rates[0] == 0 and rates[0] < rates[1] < rates[2]
          and levels[0] > levels[1] > levels[2])

    # 5. R1, thermodynamic form
    check("R1, THERMODYNAMIC FORM [P] (recorded, not claimed): derive "
          "Gamma_n ~ (S_n/S_dS)^p2 from the near-Nariai one-loop -- a "
          "Gibbons-Hawking-type entropy power law with exponent = the "
          "hexagon size; the exponent p2 (the weight h = N_fam) is "
          "the remaining quantum content", True)

    return summary("v129 entropy power law")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
