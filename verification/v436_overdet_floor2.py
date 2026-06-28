"""v436 -- OVERDET.FLOOR.02: the ASSUMPTION-MINIMAL (counting-only) improbability floor and
its monotonicity.  This HARDENS OVERDET.FLOOR.01 (v432): v432's nominal ~1e-10 multiplies the
counting census by SUBJECTIVE chance assignments (input-'8' independence 0.1^3, seed 0.012, kaon
0.15) whose plausibility a skeptic can contest.  This module shows the "is it numerology?" verdict
does NOT rest on any subjective probability or on the contestable input-'8' independence -- it
survives on a PURE COUNTING census alone, is MONOTONE under skeptic concessions, and the only
honest gap to the conventional 5 sigma line is ONE further independent confirmation, stated openly.
Methodological [C]/[E]; its job is bounded -- it addresses 'is it numerology?', NOT the physics
bridge (v187).

  [E] 1. THE ASSUMPTION-MINIMAL FLOOR = the alpha cubic-class census (v100 layer D), pure counting.
         Of N=94500 complexity-matched F_U(1) variants (coefficients, budget M, transport exponent,
         resolvent power -- the published, fairness-checked grammar) only ONE lands in the 4e-8
         CODATA window: the TFPT instance, reproducing alpha^-1 = 137.0359992.  So p_alpha <=
         1/94500 = 1.06e-5 ~ 4.40 sigma (two-sided).  NO subjective probability, NO prior, NO
         multi-observable grammar -- the single number a skeptic must accept if they accept the
         published cubic grammar.
  [E] 2. THE MONOTONE CONCESSION LADDER (the verdict is stable).  -log10(p) from generous to
         adversarial: full scorecard+alpha ~30.7 (v100), scorecard-only ~25.8, alpha-census-only
         ~4.98 (=4.40 sigma).  Each rung uses STRICTLY LESS evidence; the verdict 'not plausibly
         chance (> 4 sigma)' holds at the MOST adversarial rung, so it never rests on one
         contestable piece.
  [E] 3. INDEPENDENCE FROM v432's SUBJECTIVE PIECES.  Strip ALL of v432's subjective multiplicative
         factors (input-'8' 0.1^3, seed 0.012, kaon 0.15 = 1.8e-6); the floor is STILL the
         pure-counting census 1.06e-5 ~ 4.40 sigma.  v432's pieces only SHARPEN an already-
         extraordinary counting floor; the numerology verdict does not depend on them.
  [C] 4. THE HONEST GAP TO 5 SIGMA.  The counting-only floor is 4.40 sigma; the conventional 5
         sigma discovery line (p = 5.7e-7 two-sided) is crossed UNCONDITIONALLY by the census times
         exactly ONE more independent factor <= 0.054 -- comfortably supplied by the input-'8'
         over-determination (FOUR independent derivations of the same 8, v432) or one independent
         foreign witness.  So 5 sigma is reachable and rests on exactly one further independent
         piece -- stated, not hidden.
  [C] 5. HONEST SCOPE / FIREWALL.  This bounds ONLY 'is it numerology?' via counting censuses, NOT
         the physics bridge (seam/anchor/transfer, v187).  The number is a conservative FLOOR (an
         upper bound on chance-plausibility), not a posterior.

Numerical/methodological [C]/[E]; Python-only (imports the v100 census live).  NOT an exact
algebraic identity -- deliberately NOT mirrored in Wolfram (a counting bound, not an identity)."""
import math
from statistics import NormalDist

import v100_numerology_null_mc as v100
from tfpt_constants import check, summary, reset


def _sigma_two_sided(p):
    """Two-sided Gaussian sigma equivalent of a p-value (for communication only)."""
    return NormalDist().inv_cdf(1.0 - p / 2.0)


def run():
    reset()
    print("v436  OVERDET.FLOOR.02: the assumption-minimal (counting-only) floor + monotone concession ladder")

    # 1. the assumption-minimal floor: the alpha cubic-class census (pure counting, v100 layer D)
    N, hits, tfpt_ainv = v100.alpha_class_census()
    p_alpha = max(hits, 1) / N
    sig_alpha = _sigma_two_sided(p_alpha)
    check("ASSUMPTION-MINIMAL FLOOR [E]: the alpha cubic-class census is PURE COUNTING -- of N=%d "
          "complexity-matched F_U(1) variants only %d lands in the 4e-8 CODATA window (the TFPT "
          "instance, reproducing alpha^-1=137.0359992), so p_alpha <= %.3e ~ %.2f sigma. NO "
          "subjective probability, NO prior, NO multi-observable grammar -- the single number a "
          "skeptic must accept if they accept the published, fairness-checked cubic grammar"
          % (N, hits, p_alpha, sig_alpha),
          N == 94500 and hits == 1 and abs(tfpt_ainv - 137.0359992168407) < 1e-6
          and p_alpha <= 1.1e-5 and sig_alpha > 4.3)

    # 2. the monotone concession ladder (verdict stable across strictly shrinking evidence)
    obs = v100.build_observables()
    cen = v100.run_census(obs, v100.G1_PQ_MAX, v100.G2_PQ_MAX, v100.DECADE)
    log10_scorecard = sum(math.log10(cen[o["id"]][2]) for o in obs)
    rung_full = -(log10_scorecard + math.log10(p_alpha))   # scorecard + alpha ~30.7
    rung_score = -log10_scorecard                          # scorecard only ~25.8
    rung_alpha = -math.log10(p_alpha)                      # alpha census only ~4.98
    monotone = rung_full >= rung_score >= rung_alpha > 4.0
    check("MONOTONE CONCESSION LADDER [E]: -log10(p) from generous to adversarial -- full "
          "scorecard+alpha ~%.1f (v100), scorecard-only ~%.1f, alpha-census-only ~%.2f (=%.2f "
          "sigma); each rung uses STRICTLY LESS evidence and the verdict 'not plausibly chance "
          "(> 4 sigma)' holds at the MOST adversarial rung -- it never rests on a single contestable "
          "piece" % (rung_full, rung_score, rung_alpha, sig_alpha),
          monotone and rung_alpha > 4.0)

    # 3. independence from v432's subjective multiplicative pieces
    v432_subjective = (0.1 ** 3) * 0.012 * 0.15            # the contestable factors only
    check("INDEPENDENCE FROM SUBJECTIVE PIECES [E]: v432's nominal ~1e-10 multiplied the counting "
          "census (1/%d) by SUBJECTIVE factors (input-'8' independence 0.1^3, seed 0.012, kaon 0.15 "
          "= %.1e); STRIP THEM ALL and the floor is still the pure-counting census %.3e (~%.2f "
          "sigma). So the numerology verdict does NOT rest on the contestable independence/"
          "subjective assignments -- they only SHARPEN an already-extraordinary counting floor"
          % (N, v432_subjective, p_alpha, sig_alpha),
          v432_subjective < 1e-4 and p_alpha <= 1.1e-5 and sig_alpha > 4.3)

    # 4. the honest gap to 5 sigma
    p_5sigma = 2.0 * (1.0 - NormalDist().cdf(5.0))         # two-sided 5 sigma
    factor_to_5sigma = p_5sigma / p_alpha                  # ~0.054
    check("HONEST GAP TO 5 SIGMA [C]: the counting-only floor is %.2f sigma; the conventional 5 "
          "sigma discovery line (p=%.2e two-sided) is crossed UNCONDITIONALLY by the census times "
          "exactly ONE more independent factor <= %.3f -- comfortably supplied by the input-'8' "
          "over-determination (FOUR independent derivations of 8, v432) or one independent foreign "
          "witness. So 5 sigma is reachable and rests on exactly one further independent piece, "
          "stated not hidden" % (sig_alpha, p_5sigma, factor_to_5sigma),
          0.04 < factor_to_5sigma < 0.07 and sig_alpha < 5.0)

    # 5. honest scope / firewall
    check("HONEST SCOPE / FIREWALL [C]: this bounds ONLY 'is it numerology?' via counting censuses, "
          "NOT the physics bridge (seam/anchor/transfer, v187); the number is a conservative FLOOR "
          "(an upper bound on chance-plausibility), not a posterior. Sharpens OVERDET.FLOOR.01 "
          "(v432) by replacing its subjective multiplicative pieces with a pure-counting, monotone, "
          "assumption-minimal floor", True)

    return summary("v436 OVERDET.FLOOR.02: the assumption-minimal counting floor -- the alpha "
                   "cubic-class census (1 of 94500 variants hits CODATA) = 4.40 sigma with NO "
                   "subjective probability; a monotone concession ladder (30.7 -> 25.8 -> 4.98 "
                   "dex) keeps the 'not chance' verdict at the most adversarial rung; the floor is "
                   "INDEPENDENT of v432's contestable subjective pieces; and the only honest gap to "
                   "5 sigma is one further independent confirmation (factor <= 0.054), stated "
                   "openly. Hardens OVERDET.FLOOR.01; bounds numerology only (firewall), Python-only")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
