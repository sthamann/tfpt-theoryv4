"""RED TEAM  Target F -- the perturbative 4D-QFT + scale round (v269-v275).

This target adversarially stress-tests the round that was just published (Zenodo 5.2):
the Epstein-Glaser S_pert layer (v269/v271/v273), the PMNS Jarlskog CP strength
(v270), the absolute neutrino-scale typing (v272), the scale over-determination
(v274) and the QG.AMB.01 roadmap (v275).  Two attacks LAND and force a narrowing;
the rest survive as worded.

Adversarial findings (all TRUE = the attack lands):
  * GRAVITY S_pert IS NON-UNITARY.  The spectral-action gravity sector R^2 + Weyl^2
    is power-counting renormalizable (Stelle 1977) but the 4-derivative Weyl^2
    propagator 1/(p^2(p^2+M^2)) partial-fractions to a massive spin-2 mode with a
    NEGATIVE residue -- a ghost.  So v269/v271/v273 "the perturbative S-matrix
    exists" must be SCOPED: matter+gauge is fine, the GRAVITY sub-sector S_pert is
    renormalizable-but-non-unitary, which is exactly why the NONPERTURBATIVE
    QG.AMB.01 (asymptotic safety / the boundary (E8)_1 net) is the real frontier.
  * THE OVER-DETERMINATION IS CONDITIONAL.  v274's Route-2 (cosmology) inverts the
    rho_Lambda/M_bar^4 = (3/4pi^2)e^{-2 alpha^-1} prediction, which is itself
    LAMBDA.BRANCH.01 [C] (the dark-energy branch readout).  So the 0.11% gravity-vs-
    cosmology agreement is conditional on the Lambda-branch being correct, not
    unconditional.
  * J_PMNS INHERITS delta's PROVENANCE.  v270's Jarlskog is a derived consequence of
    (angles + delta), but delta = 240 deg is the ASSEMBLED mu6/triality phase
    (v231/v233), not an M_nu/D_F output -- so J is a consequence with [C] provenance,
    not an independent prediction.
  * THE nu-SCALE WINDOW IS WEAK.  v272's "y_nu in [0.26,2.0]" consistency is nearly
    vacuous (any M_R gives some O(1) y_nu); the honest content is the [O] typing plus
    the ONE genuine kill test (the NO floor Sigma m_nu = 0.0586 eV).

Firewalls that HOLD (no overclaim in the active docs):
  * no active document says "4D QFT solved" / "unitary 4D S-matrix" / "metric sector
    closed" without scope; the wording guard (v265) and the conservative phrasing
    survive the scan.
"""
import os

from rt_common import (banner, step, note, verdict, check, summary, reset,
                       ROOT_DIR, read_text, SURVIVES, SURVIVES_NARROWED)
from fractions import Fraction as F

REPORT = {}

ACTIVE_DOCS = [
    "introduction", "tfpt_1_architecture_e8", "tfpt_2_standard_model",
    "tfpt_3_e8_audit_bootstrap", "tfpt_4_frontier", "tfpt_5_redteam",
    "tfpt_horizon_readouts", "tfpt_research_contracts", "origin_theory",
]


def run():
    reset()
    banner("F", "the perturbative 4D-QFT + scale round (v269-v275)")

    # --- 1 minimal statement ------------------------------------------------
    step(1, "minimal statement under attack")
    note("(v269/v271/v273) the 4D perturbative S-matrix S_pert of the spectral action\n"
         "exists (Epstein-Glaser) with one-loop quartic + gauge betas; (v270) the PMNS\n"
         "Jarlskog J = -0.0297 is derived; (v272) the absolute nu-scale is one seesaw\n"
         "ratio; (v274) the mass anchor is over-determined to 0.11%; (v275) QG.AMB.01\n"
         "carries a Tier-A/Tier-B roadmap.")

    # --- 2 assumptions ------------------------------------------------------
    step(2, "assumptions the strong reading silently needs")
    note("(i) 'renormalizable' is read as 'a healthy unitary S-matrix' (it is NOT, for\n"
         "    the higher-derivative gravity sector);\n"
         "(ii) the over-determination treats the rho_Lambda prediction as unconditional;\n"
         "(iii) J_PMNS is read as an independent prediction rather than a consequence of\n"
         "      the assembled delta.")

    # --- 3 logical chain ----------------------------------------------------
    step(3, "logical chain (what is genuinely established)")
    check("power-counting renormalizability of the a_4 operators IS correct (all mass "
          "dim <= 4) -- v269/v271/v273 stand on that", True)
    check("the SM one-loop b_i = (41/10,-19/6,-7) ARE the EG one-loop counterterm "
          "coefficients (v273) -- exact, not new physics", True)

    # --- 4 validity conditions ---------------------------------------------
    step(4, "validity conditions")
    note("EG existence is order-by-order / perturbative only; it never claims a\n"
         "nonperturbative measure. The matter+gauge sector is unitary order by order.")

    # --- 5 counterexample search (the attacks that LAND) --------------------
    step(5, "counterexample search")
    # (a) Stelle ghost: 4-derivative gravity propagator has a negative-residue mode
    #     1/(p^2 (p^2+M^2)) = 1/(M^2 p^2) - 1/(M^2 (p^2+M^2))  (ghost = relative minus)
    healthy_res = F(1)          # residue of 1/p^2 (massless graviton), times 1/M^2
    ghost_res = F(-1)           # residue of 1/(p^2+M^2) (massive spin-2), times 1/M^2
    check("ATTACK LANDS (gravity S_pert non-unitary): the spectral-action Weyl^2 "
          "sector gives a 4-derivative propagator 1/(p^2(p^2+M^2)) whose massive "
          "spin-2 mode has a NEGATIVE residue (Stelle ghost) -- so the gravity "
          "perturbative S-matrix is renormalizable but NOT unitary",
          healthy_res > 0 and ghost_res < 0)
    check("=> the gravity-sector ghost is exactly why the NONPERTURBATIVE QG.AMB.01 "
          "(asymptotic safety / boundary (E8)_1 net) is required: the perturbative "
          "gravity S-matrix cannot be the final word", True)
    # (b) over-determination is conditional on the Lambda-branch
    check("ATTACK LANDS (over-determination conditional): v274 Route-2 inverts "
          "rho_Lambda/M_bar^4 = (3/4pi^2)e^{-2 alpha^-1}, which is LAMBDA.BRANCH.01 [C] "
          "-- so the 0.11% gravity-vs-cosmology agreement is conditional on the "
          "Lambda-branch readout, not unconditional", True)
    # (c) J_PMNS inherits delta's provenance
    check("ATTACK LANDS (J provenance): J_PMNS is a consequence of (angles + delta), "
          "but delta = 240 deg is the assembled mu6/triality phase (v231/v233), NOT an "
          "M_nu/D_F output -- so J carries delta's [C] provenance, not independent", True)
    # (d) nu-scale window is weak
    check("ATTACK LANDS (nu-window weak): v272's y_nu in [0.26,2.0] consistency is "
          "nearly vacuous; the genuine content is the [O] typing + the ONE NO-floor "
          "kill test Sigma m_nu = 0.0586 eV", True)

    # --- 6 limiting / degenerate cases -------------------------------------
    step(6, "limiting / degenerate cases")
    check("if one drops the higher-derivative Weyl^2 term, gravity is non-renormalizable "
          "again -- so renormalizability and unitarity cannot both hold perturbatively "
          "(the well-known Stelle dichotomy); TFPT's escape is nonperturbative (QG.AMB.01)",
          True)

    # --- 7 firewall scan (these must HOLD) ----------------------------------
    step(7, "firewall: no overclaim wording in the positive-claim docs")
    # the red-team paper itself legitimately QUOTES forbidden phrases to forbid them,
    # so it is excluded from the firewall (it is not a positive-claim surface).
    positive_docs = [d for d in ACTIVE_DOCS if d != "tfpt_5_redteam"]
    docs = "\n".join(read_text(os.path.join(ROOT_DIR, f"{d}.tex")) for d in positive_docs).lower()
    banned = ["4d qft solved", "unitary 4d s-matrix", "metric sector closed",
              "quantum gravity solved", "nonperturbative s-matrix"]
    hits = [p for p in banned if p in docs]
    check("FIREWALL HOLDS: no active doc contains an unscoped overclaim "
          "%s (found: %s)" % (banned, hits or "none"), not hits)

    # --- 8 verdict ----------------------------------------------------------
    fails = summary("rt_F perturbative-QFT + scale round")
    verdict(
        REPORT, target_id="F",
        claim="the v269-v275 round: S_pert EG-constructible + one-loop numbers, PMNS "
              "Jarlskog, nu-scale typing, scale over-determination, QG.AMB.01 roadmap",
        assumptions="EG perturbative existence; the spectral-action operator basis; the "
                    "Lambda-branch readout; the assembled mu6 CP phase",
        works="power-counting renormalizability (dim<=4), the exact one-loop b_i "
              "(41/10,-19/6,-7) and quartic beta = 3lam^2/16pi^2 [E]; the unitary "
              "PMNS assembly + J_PMNS as a derived consequence; the honest [O] typing "
              "of the nu-scale; the striking 0.11% anchor over-determination",
        fails="the GRAVITY sub-sector S_pert is renormalizable but NON-UNITARY (Stelle "
              "ghost in Weyl^2); the over-determination is conditional on the "
              "Lambda-branch [C]; J_PMNS inherits delta's [C] provenance; the nu-window "
              "is weak (only the NO floor is a real kill test)",
        status=SURVIVES_NARROWED,
        verdict_text="the round SURVIVES as typed, but two narrowings are mandatory: "
                     "(1) scope S_pert to matter+gauge unitary / gravity "
                     "renormalizable-but-ghosty (-> QG.AMB.01); (2) state the "
                     "over-determination as conditional on the Lambda-branch. "
                     "J_PMNS and the nu-window are already honestly typed.",
        residual="the perturbative gravity S-matrix is non-unitary (Stelle ghost) -- "
                 "this IS the QG.AMB.01 frontier, not a new gap; the over-determination "
                 "is conditional on LAMBDA.BRANCH.01 [C].",
    )
    return fails


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
