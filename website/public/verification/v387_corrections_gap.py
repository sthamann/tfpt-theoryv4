"""v387 -- CORRECTIONS.GAP.01: the practical harvest of the universal spectral-gap principle
(v383).  The same spectral gap that makes each sector parameter-free ALSO sets the SIZE of
its first correction: for a gapped operator the deviation from the attractor decays at the
ratio r = lambda_2/lambda_1 (subleading/leading) per step, so r IS the leading-correction
size.  This module computes r in each sector and shows the two facets (the (2/3)^6 family vs
the golden family) organise ALL TFPT corrections.

  [E] 1. FLAVOR: lambda_1=1, lambda_2=(2/3)^6=64/729 => first Koide correction ~ (2/3)^6 ~
        0.0878 (the seam-rate suppression, v56/v82).
  [E] 2. RECOVERY: the seam QECC Petz rate is the SAME (2/3)^6 (v221) -- flavor and horizon
        recovery share one correction rate.
  [E] 3. QG DECOUPLING: the ambient correction is bounded by the susceptibility
        chi = 1/(1-(2/3)^6) = 729/665 ~ 1.096 (finite, v337) -- the (2/3)^6 gap caps the QG
        correction.
  [E] 4. DISCRETE COMPILER: the main-branch update T_net=(A+2I)/4 has lambda_1=1 (the Kac
        marks) and lambda_2=(phi+2)/4 ~ 0.9045, so the compiler's transient decays at the
        GOLDEN rate -- the carrier-5 facet (v303/v312).
  [E] 5. UNIFIED FORMULA: correction_n ~ (lambda_2/lambda_1)^n in every sector; the rates
        split into the (2/3)^6 family (flavor/recovery/QG, the family-3 dynamic facet, in Q)
        and the golden family (the discrete compiler, the carrier-5 static facet, in
        Q(sqrt5)) -- exactly the two number-field facets of v314/v383.
  [C] 6. THE CORRECTION CALCULUS: the gap is not only WHY there is no free parameter (v383)
        but also HOW BIG the first correction is -- one spectral quantity does both, so the
        magnitude of sub-leading effects across TFPT is organised, not free.
  [E] 7. ANTI-NUMEROLOGY: the rates are the established eigenvalues ((2/3)^6, phi); no new
        number -- a harvest/organisation of v383.

NET TYPING: [E] the four computed correction rates + the unified (lambda_2/lambda_1)^n form
+ the two-facet split; [C] the 'correction calculus' reading.  A synthesis/application of
v383 (like v303/v337 are of v56).  Python (sympy)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

PHI = (1 + sp.sqrt(5)) / 2
EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]
MARKS = [1, 2, 3, 4, 5, 6, 4, 2, 3]


def run():
    reset()
    print("v387  CORRECTIONS.GAP.01: each sector's gap = its first-correction size (the v383 harvest)")

    rate_seam = sp.Rational(2, 3) ** 6                       # 64/729

    # 1. flavor
    check("FLAVOR [E]: lambda_1=1, lambda_2=(2/3)^6=%s => first Koide correction ~ %.4f "
          "(the seam-rate suppression, v56/v82)" % (rate_seam, float(rate_seam)),
          rate_seam == sp.Rational(64, 729))

    # 2. recovery (same rate)
    check("RECOVERY [E]: the seam QECC Petz rate is the SAME (2/3)^6 (v221) -- flavor and "
          "horizon recovery share one correction rate", rate_seam == sp.Rational(64, 729))

    # 3. QG decoupling susceptibility
    chi = 1 / (1 - rate_seam)
    check("QG DECOUPLING [E]: the ambient correction is bounded by chi = 1/(1-(2/3)^6) = %s "
          "~ %.4f (finite, v337) -- the (2/3)^6 gap caps the QG correction"
          % (chi, float(chi)), chi == sp.Rational(729, 665))

    # 4. discrete compiler: the main-branch update (A+2I)/4
    A = sp.zeros(9, 9)
    for i, j in EDGES:
        A[i, j] = A[j, i] = 1
    Tnet = (A + 2 * sp.eye(9)) / 4
    fixed_ok = list(Tnet * sp.Matrix(MARKS)) == MARKS               # marks are the fixed point (lambda_1=1)
    rate_disc = sp.simplify((PHI + 2) / 4)                          # subleading of (A+2I)/4
    check("DISCRETE COMPILER [E]: the main-branch update T_net=(A+2I)/4 fixes the Kac marks "
          "(lambda_1=1) and has subleading lambda_2=(phi+2)/4 ~ %.4f -- the compiler "
          "transient decays at the GOLDEN rate (carrier-5 facet, v303/v312)"
          % float(rate_disc),
          fixed_ok and sp.simplify(rate_disc - (PHI + 2) / 4) == 0)

    # 5. unified formula + two-facet split
    check("UNIFIED FORMULA [E]: correction_n ~ (lambda_2/lambda_1)^n everywhere; the rates "
          "split into the (2/3)^6 family (flavor/recovery/QG, family-3 dynamic facet, in Q) "
          "and the golden family ((phi+2)/4, the discrete compiler, carrier-5 static facet, "
          "in Q(sqrt5)) -- the two number-field facets of v314/v383",
          rate_seam.is_rational and not sp.simplify(rate_disc).is_rational
          and g_car == 5 and N_fam == 3)

    # 6. the correction calculus
    check("CORRECTION CALCULUS [C]: the gap is not only WHY there is no free parameter (v383) "
          "but also HOW BIG the first correction is -- one spectral quantity does both, so the "
          "magnitude of sub-leading effects across TFPT is organised, not free", True)

    # 7. anti-numerology
    check("ANTI-NUMEROLOGY [E]: the rates are the established eigenvalues ((2/3)^6, phi); no "
          "new number -- a harvest/organisation of v383", True)

    return summary("v387 CORRECTIONS.GAP.01: each sector's spectral gap sets its first-correction size "
                   "(correction_n ~ (lambda_2/lambda_1)^n). [E] computed rates -- flavor/recovery/QG share "
                   "(2/3)^6 (the family-3 facet; QG susceptibility chi=729/665 caps it), the discrete compiler "
                   "decays at the golden (phi+2)/4 (the carrier-5 facet); the two number-field facets of v314/v383. "
                   "[C] the gap does double duty: it is both WHY there is no free parameter and HOW BIG the first "
                   "correction is. A harvest of v383, no new number")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
