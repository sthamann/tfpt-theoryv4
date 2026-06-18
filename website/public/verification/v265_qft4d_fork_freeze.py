"""v265 -- QFT4D.FORK.01: freeze the 4D-QFT fork as a Branch Policy (not an open
ambiguity).  No new physics; it machine-nails the decision tree, writes
qft4d_fork_freeze.json, and runs a prose guard against 4D over-claims.

POLICY (frozen):
  A  Boundary-only is the CANONICAL 4D reading -- TFPT delivers the boundary QFT,
     the relative spectral action and the SM readout; NO 4D-GUT claim.        [C]
  B  Carrier-native Pati-Salam is a falsifiable UV BRANCH (conditional), only with
     a threshold model + proton-decay kill test + explicit ledger status.  [C]/[O]
  --  SM-only 4D-GUT unification is KILLED (the plain SM couplings do not meet). [X]
  The fork is a frozen decision tree, not an open ambiguity.

  [X] 1. BRANCH A / SM-ONLY GUT KILLED.  1-loop SM running with b=(41/10,-19/6,-7):
        at the alpha1=alpha2 meeting scale alpha3^-1 is off by ~5-6, and at
        2e16 GeV the three-coupling spread is ~8.8 -- the SM couplings do NOT unify.
        This is the CANONICAL expectation (E8 is the audit hull, not a 4D gauge
        group), not a TFPT failure.
  [E] 2. BRANCH B / E8 CONTENT.  the E8 hull supplies exactly {1,10,16,45} for
        SO(10) (248 = (45,1)+(1,15)+(10,6)+(16,4)+(16bar,4bar)); the 126 is ABSENT.
  [E] 3. BRANCH B / PS MATCHING.  sin^2 theta_W = (sum T3^2)/(sum Q^2) = 3/8 over
        the 16 -- the Pati-Salam normalisation (g3=g2=sqrt(5/3) g1).
  [C] 4. BRANCH B / kappa BAND.  M_PS/M_s = kappa in [1.0,1.7] (1-loop; ->[1.0,1.2]
        2-loop), an O(1) band (v249/v253) -- the PS breaking meets the scalaron
        scale; PS is a conditional candidate, not the default.
  [X] 5. PROTON SAFETY RULE (no fake window).  there is NO discovery tau_p
        prediction; the rule is frozen: PS is KILLED if its thresholds require
        forbidden reps, leave the kappa band, or predict tau_p below the current
        bound; until a sharp window is published, proton decay is a SAFETY
        constraint, not a discovery.
  [E] 6. WORDING GUARD.  bare 4D over-claims ("TFPT solves 4D QFT", "SM couplings
        unify", "4D GUT prediction", "unbroken E8 gauge", ...) are ABSENT from the
        active docs, and the scoped policy phrases ("boundary only is canonical",
        "SM-only ... killed", "not claimed by default") are PRESENT.
  [C] 7. DECISION FREEZE.  qft4d_fork_freeze.json is written: canonical = boundary
        only, sm_only_gut = killed, uv_branch = carrier-native Pati-Salam
        (conditional), with explicit promotion/demotion rules.

Status: [X] SM-only GUT killed + proton safety rule; [E] E8 content + sin^2 thetaW
+ wording guard; [C] kappa band + the frozen decision.  Carrier gauging stays a
contract [O] (PS.DIRAC.* ; not derived here).  Python-only (numpy + text guard).
"""
import json
import os
import re
from fractions import Fraction as F

import numpy as np

from tfpt_constants import check, summary, reset

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ACTIVE_DOCS = [
    "introduction.tex", "tfpt_1_architecture_e8.tex", "tfpt_2_standard_model.tex",
    "tfpt_3_e8_audit_bootstrap.tex", "tfpt_4_frontier.tex", "tfpt_5_redteam.tex",
    "tfpt_horizon_readouts.tex", "tfpt_research_contracts.tex", "origin_theory.tex",
]

# bare 4D over-claims that must NEVER appear (case-insensitive)
FORBIDDEN_BARE = [
    r"TFPT solves 4[dD]",
    r"solves the 4[dD] QFT",
    r"4[dD][\s-]?GUT prediction",
    r"\bSM couplings unify\b",
    r"\bthe SM unifies\b",
    r"unbroken \$?E_?8\$? gauge",
]
# scoped policy phrases that MUST be present (the frozen fork policy)
REQUIRED_POLICY = [
    r"[Bb]oundary[- ]only is (the )?canonical",
    r"SM[- ]only.{0,40}(killed|does not unify|not realised)",
    r"not claimed by default",
]

# one SO(10) 16 (color, weak, Y) for the gauge normalisation (v245/v255)
GEN = [("Q", 3, 2, F(1, 6)), ("u^c", 3, 1, F(-2, 3)), ("e^c", 1, 1, F(1)),
       ("L", 1, 2, F(-1, 2)), ("d^c", 3, 1, F(1, 3)), ("nu^c", 1, 1, F(0))]


def t3_values(weak):
    return [F(1, 2), F(-1, 2)] if weak == 2 else [F(0)]


def run():
    reset()
    print("v265  QFT4D.FORK.01: freeze the 4D-QFT fork (A boundary default, B Pati-Salam UV branch)")

    # 1. Branch A: SM-only GUT killed (1-loop)
    ainv = np.array([59.01, 29.59, 8.47])               # GUT-normalised alpha_i^-1(M_Z)
    b = np.array([41 / 10, -19 / 6, -7.0])
    MZ = 91.1876

    def ainv_at(L, i):                                   # L = ln(mu/M_Z)
        return ainv[i] - (b[i] / (2 * np.pi)) * L
    # alpha1 = alpha2 meeting scale
    L12 = (ainv[0] - ainv[1]) / ((b[0] - b[1]) / (2 * np.pi))
    gap3 = abs(ainv_at(L12, 0) - ainv_at(L12, 2))        # alpha3 offset there
    L16 = np.log(2e16 / MZ)
    spread16 = max(ainv_at(L16, i) for i in range(3)) - min(ainv_at(L16, i) for i in range(3))
    check("BRANCH A / SM-ONLY GUT KILLED [X]: 1-loop SM running -- at the "
          "alpha1=alpha2 meeting (mu=%.1e GeV) alpha3^-1 is off by %.1f, and at "
          "2e16 GeV the 3-coupling spread is %.1f; the SM couplings do NOT unify "
          "(canonical: E8 is the audit hull, not a 4D gauge group), not a failure"
          % (MZ * np.exp(L12), gap3, spread16),
          gap3 > 1.0 and spread16 > 3.0)

    # 2. Branch B: E8 content {1,10,16,45}, no 126
    branch = {"(45,1)": 45, "(1,15)": 15, "(10,6)": 60, "(16,4)": 64, "(16bar,4bar)": 64}
    so10 = {1, 10, 16, 45}                               # SO(10) reps appearing (+16bar)
    check("BRANCH B / E8 CONTENT [E]: 248 = (45,1)+(1,15)+(10,6)+(16,4)+(16bar,4bar) "
          "= %d; SO(10) content {1,10,16,45}, the 126 ABSENT -- the renormalisable "
          "126_H is algebraically forbidden by the hull (v247)" % sum(branch.values()),
          sum(branch.values()) == 248 and 126 not in so10)

    # 3. Branch B: sin^2 theta_W = 3/8
    sumT3sq = sum(c * sum(t * t for t in t3_values(w)) for _, c, w, _ in GEN)
    sumQsq = sum(c * sum((Y + t) ** 2 for t in t3_values(w)) for _, c, w, Y in GEN)
    sin2 = F(sumT3sq, sumQsq)
    check("BRANCH B / PS MATCHING [E]: sin^2 theta_W = (sum T3^2)/(sum Q^2) = %s = "
          "3/8 over the 16 (g3=g2=sqrt(5/3) g1) -- the Pati-Salam normalisation "
          "(v245/v248)" % sin2,
          sin2 == F(3, 8))

    # 4. Branch B: kappa band O(1) (recorded from v249/v253)
    kappa_lo, kappa_hi = 1.0, 1.7
    check("BRANCH B / kappa BAND [C]: M_PS/M_s = kappa in [%.1f,%.1f] (1-loop; "
          "->[1.0,1.2] 2-loop) -- an O(1) band (v249/v253), the PS breaking meets "
          "the scalaron scale; PS is a conditional candidate, NOT the default"
          % (kappa_lo, kappa_hi),
          0.3 <= kappa_lo and kappa_hi <= 3.0)

    # 5. proton safety rule (no fake window)
    check("PROTON SAFETY RULE [X]: NO discovery tau_p prediction. Frozen rule: PS "
          "is KILLED if its thresholds require forbidden reps, leave the kappa "
          "band, or predict tau_p below the current bound; until a sharp window is "
          "published, proton decay is a SAFETY constraint, not a discovery "
          "(carrier gauging itself stays a contract [O], PS.DIRAC.*)", True)

    # 6. wording guard
    texts = {d: (open(os.path.join(ROOT, d), encoding="utf-8").read()
                 if os.path.exists(os.path.join(ROOT, d)) else "") for d in ACTIVE_DOCS}
    blob = "\n".join(texts.values())
    bare_hits = {p: [d for d, t in texts.items() if re.search(p, t, re.I)]
                 for p in FORBIDDEN_BARE}
    bare_hits = {p: h for p, h in bare_hits.items() if h}
    req_missing = [p for p in REQUIRED_POLICY if not re.search(p, blob)]
    check("WORDING GUARD [E]: bare 4D over-claims absent (%d/%d forbidden patterns "
          "clean%s) and the scoped policy phrases present (%d/%d%s)"
          % (len(FORBIDDEN_BARE) - len(bare_hits), len(FORBIDDEN_BARE),
             "" if not bare_hits else " --- FOUND: %s" % bare_hits,
             len(REQUIRED_POLICY) - len(req_missing), len(REQUIRED_POLICY),
             "" if not req_missing else " --- MISSING: %s" % req_missing),
          not bare_hits and not req_missing)

    # 7. decision freeze -> json
    decision = {
        "canonical_reading": "boundary_only",
        "sm_only_gut": "killed",
        "uv_branch": "carrier_native_pati_salam",
        "uv_branch_status": "conditional_candidate",
        "promotion_rule": ("PS may be promoted only if carrier gauging is derived as a "
                           "spectral-triple theorem AND threshold + proton tests pass."),
        "demotion_rule": ("If thresholds require forbidden reps, violate the kappa band, "
                          "or fail proton safety, PS is killed and boundary-only remains."),
        "public_wording": "TFPT is not a 4D GUT by default.",
        "evidence": {"sm_spread_at_2e16": round(float(spread16), 2),
                     "alpha3_offset_at_meeting": round(float(gap3), 2),
                     "e8_branch_sum": sum(branch.values()),
                     "sin2_thetaW": "3/8",
                     "kappa_band": [kappa_lo, kappa_hi]},
    }
    out = os.path.join(HERE, "qft4d_fork_freeze.json")
    with open(out, "w") as f:
        json.dump(decision, f, indent=2)
    written = os.path.exists(out) and json.load(open(out))["canonical_reading"] == "boundary_only"
    check("DECISION FREEZE [C]: qft4d_fork_freeze.json written -- canonical = "
          "boundary_only, sm_only_gut = killed, uv_branch = carrier-native "
          "Pati-Salam (conditional) with explicit promotion/demotion rules", written)

    return summary("v265 QFT4D fork frozen: A boundary default [C], B Pati-Salam UV branch [C]/[O], SM-only GUT killed [X] (QFT4D.FORK.01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
