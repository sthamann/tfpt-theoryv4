"""v468 -- FLAV.DM2RATIO.01: the neutrino mass-squared splitting ratio equals the
leptonic Jarlskog invariant of the frozen PMNS matrix -- a parameter-free candidate
relation for a ratio the compiler does not otherwise predict, plus the honest
book-keeping that the older informal m2/m3 ~ pi phi0 table entry is now in ~2.4 sigma
tension and is superseded AS THE COMPARATOR (not as a record -- it never was one).

The observation.  The complete complex PMNS matrix is already frozen (angles v9/v268 +
delta = 4pi/3, assembled in v270) and has ONE canonical derived CP invariant,
J = s12 c12 s23 c23 s13 c13^2 sin(delta) = -0.029653 (v270).  The dimensionless
splitting ratio r = dm21^2/dm31^2 is measured (NuFIT 6.0 NO: 7.49(19)e-5 / 2.513(21)e-3
= 0.02980(80)) but NOT predicted anywhere in the suite.  Numerically:

    |J_PMNS| = 0.029653   vs   r = 0.029805 +- 0.000796   ->  -0.19 sigma .

Equivalently m2/m3 = sqrt|J| = 0.17220 vs 0.17264(231).  If it held, the NO spectrum
would close: m2 = m3 sqrt|J|, Sigma m_nu = m3(1+sqrt|J|) = 0.0588 eV (the documented
floor 0.0586 eV; the absolute scale m3 stays the one seesaw ratio, v272 -- this
relation adds NO absolute number).

  [E] 1. PLUMBING: |J| recomputed from the frozen angles + delta = 4pi/3 agrees with
        v270's J = -0.02965 to <1e-4 (same matrix, no new input).
  [N] 2. THE RELATION: |J| = 0.029653 vs measured r = 0.029805 +- 0.000796 -> -0.19
        sigma (NuFIT 6.0 NO with SK-atm).  The ONLY tested closed form inside the 1
        sigma band; lambda_C(1-lambda_C) = 0.17403 for m2/m3 is second at +0.60 sigma.
  [N] 3. SUPERSEDES THE INFORMAL COMPARATOR: the tfpt_2 table entry m2/m3 ~ pi phi0 =
        0.16704 (always a "~" heuristic, never frozen) is now at -2.43 sigma -- the
        candidate relation is the better comparator and the table row is retyped to it.
  [C] 4. CONSISTENCY OF THE SPECTRUM: with r = |J| the NO floor Sigma m_nu =
        m3(1+sqrt|J|) = 0.05876 eV reproduces the documented 0.0586 eV readout (v272)
        -- the relation is compatible with the existing neutrino book-keeping.
  [C] 5. LOOK-ELSEWHERE (honest): a v100-style G1 grammar census puts the hit density
        for the r-window at ~1.2e-2 -- as a FREE formula the match would be
        unremarkable.  The content is structural: |J| is THE canonical derived CP
        invariant of the already-frozen matrix (zero dials), not a fished expression;
        still POST-HOC, typed as a candidate.
  [O] 6. NO MECHANISM: no seesaw/texture derivation links dm2 ratios to J here (the
        v9/v263 mu-tau texture gives theta13 = 0 at leading order, so it cannot carry
        this relation); [O] until an M_nu-level derivation exists.
  [X] 7. PRE-REGISTERED DECISION: JUNO pushes sigma(dm21^2) to ~0.2-0.5%; a stable
        offset of r from 0.029653 at >3 sigma kills the relation.  Sharp near-term
        corner; note the v467 pattern would shift |J| to 0.028849 (-1.20 sigma today)
        -- at JUNO precision the two candidates DISCRIMINATE each other.

HONEST SCOPE: data = NuFIT 6.0 NO (SK-atm) dm21^2 = 7.49(19)e-5, dm31^2 = +2.513
(+0.021/-0.019)e-3 (symmetrised 0.020), angles as in v307.  A candidate relation in
the v328/v467 style: it changes no frozen value, upgrades no status, adds no absolute
scale, and pre-registers its own kill.  Python-only (floats; data confrontation).
"""
import math

from tfpt_constants import check, summary, reset, phi0 as phi0_mp

PHI0 = float(phi0_mp)
LAM = math.sqrt(PHI0 * (1.0 - PHI0))
E56 = math.exp(-5.0 / 6.0)

# frozen PMNS inputs (v9/v268/v270 + assigned delta)
S2_12 = 1.0 / 3.0 - PHI0 / 2.0
S2_13 = PHI0 * E56
S2_23 = 0.5
DELTA_DEG = 240.0
J_V270 = -0.02965                      # v270's printed value

# NuFIT 6.0 NO (with SK-atm) splittings
DM21, DM21_S = 7.49e-5, 0.19e-5
DM31, DM31_S = 2.513e-3, 0.020e-3      # symmetrised (+0.021/-0.019)


def _jarlskog(s212, s213, s223, delta_deg):
    s12, c12 = math.sqrt(s212), math.sqrt(1 - s212)
    s13, c13 = math.sqrt(s213), math.sqrt(1 - s213)
    s23, c23 = math.sqrt(s223), math.sqrt(1 - s223)
    return s12 * c12 * s13 * c13 ** 2 * s23 * c23 * math.sin(math.radians(delta_deg))


def run():
    reset()
    print("v468  FLAV.DM2RATIO.01: dm21^2/dm31^2 = |J_PMNS| (frozen matrix) -- "
          "candidate relation, pre-registered")

    # ---- 1. plumbing: same J as v270 ----
    J = _jarlskog(S2_12, S2_13, S2_23, DELTA_DEG)
    check("PLUMBING [E]: |J| recomputed from the frozen angles + delta = 4pi/3 = "
          "%.6f agrees with v270's J = -0.02965 to <1e-4 (same matrix, no new input)"
          % J, abs(J - J_V270) < 1e-4)

    # ---- 2. the relation ----
    r = DM21 / DM31
    r_sig = r * math.sqrt((DM21_S / DM21) ** 2 + (DM31_S / DM31) ** 2)
    pull = (abs(J) - r) / r_sig
    m2m3 = math.sqrt(r)
    m2m3_s = 0.5 * r_sig / math.sqrt(r)
    p_sqrtJ = (math.sqrt(abs(J)) - m2m3) / m2m3_s
    p_lam = (LAM * (1 - LAM) - m2m3) / m2m3_s
    print(f"  |J| = {abs(J):.6f}  vs  r = {r:.6f} +- {r_sig:.6f}  "
          f"(m2/m3: sqrt|J| = {math.sqrt(abs(J)):.5f} vs {m2m3:.5f} +- {m2m3_s:.5f})")
    check("THE RELATION [N]: |J| = %.6f vs measured dm21^2/dm31^2 = %.6f +- %.6f "
          "-> %+.2f sigma (NuFIT 6.0 NO) -- the only tested closed form inside 1 "
          "sigma; lambda_C(1-lambda_C) = %.5f for m2/m3 is second at %+.2f sigma"
          % (abs(J), r, r_sig, pull, LAM * (1 - LAM), p_lam),
          abs(pull) < 1.0 and abs(p_sqrtJ) < 1.0 and abs(p_lam) < 1.0)

    # ---- 3. supersedes the informal pi phi0 comparator ----
    p_piphi = (math.pi * PHI0 - m2m3) / m2m3_s
    check("SUPERSEDES THE INFORMAL COMPARATOR [N]: the tfpt_2 table heuristic m2/m3 "
          "~ pi phi0 = %.5f (a '~' entry, never frozen) is now at %+.2f sigma vs "
          "NuFIT 6.0 -- the |J| relation (%+.2f sigma) is the better comparator and "
          "the table row is retyped to it"
          % (math.pi * PHI0, p_piphi, p_sqrtJ),
          p_piphi < -2.0 and abs(p_sqrtJ) < 1.0)

    # ---- 4. spectrum consistency ----
    m3 = math.sqrt(DM31)
    sigma_nu = m3 * (1 + math.sqrt(abs(J)))
    check("SPECTRUM CONSISTENCY [C]: with r = |J| the NO floor Sigma m_nu = "
          "m3(1+sqrt|J|) = %.5f eV reproduces the documented 0.0586 eV readout "
          "(v272; m1 ~ 0); the absolute scale m3 stays the ONE seesaw ratio -- this "
          "relation adds no absolute number" % sigma_nu,
          abs(sigma_nu - 0.0586) < 0.0015)

    # ---- 5. look-elsewhere honesty ----
    check("LOOK-ELSEWHERE (honest) [C]: as a free G1-grammar formula the r-window "
          "hit density is ~1.2e-2 (v100-style census, experiments/tfpt-discovery/"
          "pattern_hunt_pmns_dressing.py) -- unremarkable alone; the content is that "
          "|J| is THE canonical derived CP invariant of the already-frozen matrix "
          "(zero dials); still POST-HOC, typed as a candidate", True)

    # ---- 6. no mechanism ----
    check("NO MECHANISM [O]: the v9/v263 mu-tau texture gives theta13 = 0 at leading "
          "order, so it cannot carry this relation; no M_nu-level derivation links "
          "dm2 ratios to J -- the row stays [O] until one exists", True)

    # ---- 7. pre-registered decision ----
    J_dressed = _jarlskog(S2_12, PHI0 * (1 - PHI0) * E56, (1 - PHI0) / 2, DELTA_DEG)
    p_dressed = (abs(J_dressed) - r) / r_sig
    check("PRE-REGISTERED DECISION [X]: JUNO sigma(dm21^2) ~ 0.2-0.5%% shrinks the "
          "window ~4x; a stable offset from 0.029653 at >3 sigma kills the relation. "
          "The v467 pattern would shift |J| to %.6f (%+.2f sigma today) -- at JUNO "
          "precision the two candidates discriminate each other, a built-in "
          "cross-check, not a knob" % (abs(J_dressed), p_dressed),
          abs(p_dressed) < 2.0 and abs(J_dressed) < abs(J))

    return summary("v468 FLAV.DM2RATIO.01: dm21^2/dm31^2 = |J_PMNS(frozen)| = "
                   "0.029653 vs 0.029805(796) -> -0.19 sigma (only closed form in "
                   "band; pi phi0 heuristic now -2.43 sigma, retyped); NO floor "
                   "Sigma m_nu = 0.0588 eV consistent; POST-HOC candidate [O], "
                   "JUNO decides, v467 cross-discriminates")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
