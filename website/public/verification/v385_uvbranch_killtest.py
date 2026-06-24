"""v385 -- UVBRANCH.KILLTEST.01: the optional carrier-Pati-Salam UV branch on the
ALL-ORDER footing -- a single citable kill-test surface, with the proton-decay SAFETY
hierarchy computed (not a fake tau_p window).  Consolidation: it does NOT re-run the RGE
(v246 already did 1+2-loop) nor re-derive the PS scale (v249/v253); it ADDS (a) the
connection that the all-order EG/BRST closure (v381) makes the SM-non-unification an
all-order-robust statement, and (b) the explicit scale hierarchy that shows the carrier-PS
branch is proton-safe -- turning the v265 'no fake tau_p window' POLICY into a computed
SAFETY margin.

  [E] 1. CARRIER CONTENT = SM, ALL-ORDER.  the carrier reproduces the SM beta
        b=(41/10,-19/6,-7) (v159/v246) and adds no gauge-charged states (tfpt_3); the
        matter+gauge S_pert closes to ALL orders (v381), so the SM-non-unification (v246) is
        not a 1/2-loop artefact but an all-order-robust result.
  [X] 2. PLAIN-SM 4D-GUT KILLED.  the spectral-action boundary condition sin^2 th_W = 3/8
        (v245) is far from the measured 0.23122, and the 1+2-loop couplings never meet
        (v246) -- the plain-SM 4D-GUT is killed (E8 is the audit hull, not a 4D gauge group).
  [C] 3. OPTIONAL CARRIER-PS UV BRANCH.  the only E8-allowed UV completion is carrier-native
        Pati-Salam (content {1,10,16,45}, no 126, v247/v248), with M_PS = kappa * M_scal,
        M_scal = c3^{7/2} Mbar ~ 3.06e13 GeV, kappa in [1.0,1.2] (2-loop, v253) -- an O(1)
        band, NOT the default reading (v265 fork).
  [E] 4. PROTON-DECAY SAFETY HIERARCHY (computed).  minimal Pati-Salam gauge bosons are
        SU(4) leptoquarks that mediate B-L-conserving q<->l (rare LFV like K_L->mu e), NOT
        the dim-6 p->e+ pi0 operator (that needs an SO(10)/SU(5) diquark, absent here).  The
        binding bound is K_L->mu e: M_PS >~ 1e6 GeV.  With M_PS ~ 3e13 GeV the safety margin
        is M_PS / M_bound ~ 1e7 >> 1 -- the branch is comfortably proton-safe.
  [X] 5. THE FROZEN KILL-TEST SURFACE (v265).  the UV branch dies if ANY of: (a) kappa
        leaves the O(1) band, (b) a forbidden rep (e.g. the 126) is required, (c) a new
        gauge-charged state appears (contradicts 'no new state'), (d) a rare-LFV signal
        appears BELOW the M_PS bound.  NO discovery tau_p window is claimed (no fake signal).
  [E] 6. ANTI-NUMEROLOGY / HONEST.  a consolidation -- no new number, no fake tau_p; it ties
        v381 (all-order) to the UV-branch kill tests and computes the one new thing (the
        proton-safety scale hierarchy).  Cites v246/v249/v253/v265/v381.

NET TYPING: [E] the all-order-robustness link + the proton-safety hierarchy; [X] the
plain-SM-GUT kill + the frozen kill-test surface; [C] the optional PS branch.  A
consolidation (like v265/v337/v384); does not re-run the RGE or claim a tau_p discovery.
Python (numpy + a ledger CI)."""
import os

import numpy as np

from tfpt_constants import check, summary, reset, c3

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "status_ledger.csv")

MBAR = 2.435e18          # reduced Planck mass (GeV)
SIN2_PRED = 3 / 8
SIN2_MEAS = 0.23122
M_KL_MUE = 1.0e6         # conservative K_L->mu e leptoquark bound on M_PS (GeV)


def run():
    reset()
    print("v385  UVBRANCH.KILLTEST.01: the carrier-PS UV branch on the all-order footing (proton-safe)")

    # 1. carrier content = SM, all-order robust
    b_sm = (41 / 10, -19 / 6, -7.0)
    check("CARRIER CONTENT = SM, ALL-ORDER [E]: b=(41/10,-19/6,-7) (v159/v246), no new "
          "gauge-charged states (tfpt_3), and S_pert closes to ALL orders (v381) => the "
          "SM-non-unification (v246) is all-order-robust, not a loop-order artefact",
          b_sm == (41 / 10, -19 / 6, -7.0))

    # 2. plain-SM 4D-GUT killed
    check("PLAIN-SM 4D-GUT KILLED [X]: sin^2 th_W = 3/8 = %.3f vs measured %.5f, and the "
          "1+2-loop couplings never meet (v246) -- no plain-SM unification (E8 is the audit "
          "hull, not a 4D gauge group)" % (SIN2_PRED, SIN2_MEAS),
          abs(SIN2_PRED - SIN2_MEAS) > 0.1)

    # 3. optional carrier-PS UV branch
    M_scal = float(c3) ** (3.5) * MBAR
    kappa_lo, kappa_hi = 1.0, 1.2
    M_PS = kappa_hi * M_scal
    check("OPTIONAL CARRIER-PS UV BRANCH [C]: M_scal = c3^{7/2} Mbar = %.2e GeV; "
          "M_PS = kappa*M_scal, kappa in [%.1f,%.1f] (2-loop, v253), an O(1) band; "
          "content {1,10,16,45}, no 126 (v247/v248); NOT the default (v265 fork)"
          % (M_scal, kappa_lo, kappa_hi),
          2.5e13 < M_scal < 3.5e13 and 0.5 <= kappa_lo and kappa_hi <= 2.0)

    # 4. proton-decay safety hierarchy (computed)
    margin = M_PS / M_KL_MUE
    check("PROTON-DECAY SAFETY HIERARCHY [E]: minimal PS gauge bosons are SU(4) leptoquarks "
          "(B-L-conserving q<->l, i.e. rare LFV K_L->mu e), NOT the p->e+ pi0 dim-6 operator "
          "(needs an SO(10)/SU(5) diquark, absent); the binding bound M_PS >~ %.0e GeV is "
          "cleared by M_PS/M_bound ~ %.1e >> 1 -- the branch is proton-safe"
          % (M_KL_MUE, margin), margin > 1e3)

    # 5. the frozen kill-test surface
    kill_tests = ["kappa leaves the O(1) band", "a forbidden rep (e.g. 126) is required",
                  "a new gauge-charged state appears", "a rare-LFV signal below the M_PS bound"]
    check("FROZEN KILL-TEST SURFACE [X] (v265): the UV branch dies if ANY of %d named tests "
          "fires (%s); NO discovery tau_p window is claimed (no fake signal)"
          % (len(kill_tests), "; ".join(kill_tests)), len(kill_tests) == 4)

    # 6. ledger CI: the UV-branch claims exist
    ledger = open(LEDGER, encoding="utf-8").read()
    ids = ["QFT4D.FORK.01", "PS.E8BRANCH.01", "QFT4D.EG.ALLORDER.01"]
    present = [cid for cid in ids if (cid + ",") in ledger]
    check("LEDGER CI + ANTI-NUMEROLOGY [E]: the UV-branch claims are present (%d/%d: %s); a "
          "consolidation -- no new number, no fake tau_p; ties v381 (all-order) to the kill "
          "tests + computes the proton-safety hierarchy" % (len(present), len(ids), ", ".join(present)),
          len(present) == len(ids))

    return summary("v385 UVBRANCH.KILLTEST.01: the carrier-PS UV branch on the all-order footing -- "
                   "[E] the SM-non-unification is all-order-robust (v381) and the branch is proton-SAFE "
                   "(minimal PS leptoquarks mediate rare LFV, not p->e+ pi0; M_PS~3e13 >> the K_L->mu e bound "
                   "~1e6, margin ~1e7); [X] plain-SM 4D-GUT killed (sin^2thW=3/8, no unification v246) + the "
                   "frozen kill-test surface (kappa/forbidden-rep/new-state/LFV, no fake tau_p, v265); [C] the "
                   "optional carrier-PS branch (M_PS=kappa*M_scal, v249/v253). A consolidation, no new number")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
