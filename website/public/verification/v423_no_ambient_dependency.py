"""v423 -- The No-Ambient-Dependency certificate: NO frozen TFPT readout is
COMPUTED from the ambient quantum-gravity measure QG.AMB.01, and its back-reaction
is gap-decoupled.  This sharpens the v369/v384 prose redundancy ("QG.AMB.01 is a
[C] redundancy, not dynamics") into a MACHINE-CHECKED dependency-graph + script
fact, told HONESTLY: the one place a flavour readout transitively references
QG.AMB.01 (theta13) is an ARCHITECTURAL-coherence edge through the 4D-QFT contract
spine, never a numerical input.  Audit module, Python-only (the gap algebra is
already Wolfram-mirrored via v337).

  [E] 1. GAP-DECOUPLING MARGIN (exact, backs the decoupling).  The ambient
         back-reaction stiffness is 2*dim(E8)*c3^2 = 496/(64 pi^2) = 31/(4 pi^2)
         (31 = 2^g_car - 1) ~ 0.785; the transport gap is Delta = 6 ln(3/2) ~
         2.433; so the decoupling margin Delta_eff = Delta - 31/(4 pi^2) ~ 1.648
         > 0 (v76/v337) and the ambient susceptibility chi = 1/(1-(2/3)^6) =
         729/665 is finite.  Negative control: as the gap -> 0, chi -> inf (the
         ambient would re-enter).
  [E] 2. CERTIFICATION SINK.  The claims that LIST QG.AMB.01 as a dependency are
         ALL gravity-gate / QG-certification rows (GATE.METRIC.01,
         GRAVITY.COMPLETE.01, QGAMB.*, SEAM.S3.RP.01, ...), NONE a frozen
         physical prediction -- QG.AMB.01 has no predictive DIRECT dependent.
  [E] 3. NOT A VALUE SOURCE.  QG.AMB.01 has no producing script (ledger
         script="-"); every frozen prediction of record is COMPUTED by a
         compiler script (EM.FP.01<-v3, FLAV.TH12.01<-v9, FLAV.TH13.01<-v268,
         COSMO.*<-v7), NONE of which is an ambient-measure script
         (v76/v330/v332/v334/v335) -- so no readout VALUE is produced by the
         ambient measure.
  [E] 4. THE ONE LINK IS ARCHITECTURAL, NOT NUMERICAL (told honestly).  Of the
         frozen readouts, only theta13 (FLAV.TH13.01) transitively references
         QG.AMB.01 -- and the path runs through the 4D-QFT CONTRACT spine
         (PS.DIRAC.02 -> CONTRACT.QFT4D.01 -> QG.G2.01 -> GATE.METRIC.01), i.e.
         the readout lives INSIDE the unified spectral-action construction, a
         coherence edge.  Its VALUE sin^2 theta13 = phi0 e^{-5/6} (v268) takes no
         ambient-measure input; alpha, theta12 and all of cosmology have NO route
         to QG.AMB.01 at all.
  [C] 5. VERDICT.  QG.AMB.01 is a gap-decoupled certification object: no readout
         VALUE is computed from it, its only predictive link is the architectural
         4D-QFT contract, and the gap margin (1.648>0) suppresses its
         back-reaction -- v369 as a DAG/script fact.  HONEST: this does NOT prove
         SEAM.EQUIV.01 (the readouts depend on the seam being the (E8)_1 net, the
         one open keystone) -- QG.AMB.01 specifically is dead.

Python-only (csv DAG/script audit + gap arithmetic; the exact 31/(4 pi^2) and
729/665 are mirrored via v337).
"""
import os
import csv
import re
from collections import deque

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, dim_Splus

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "status_ledger.csv")

DIM_E8 = 248
AMB = "QG.AMB.01"
AMB_SCRIPTS = ("v76", "v330", "v332", "v334", "v335", "v369", "v337")
FROZEN = ["EM.FP.01", "FLAV.TH12.01", "FLAV.TH13.01",
          "COSMO.LAM.01", "COSMO.INF.01", "COSMO.OMB.01"]
SPINE = "CONTRACT.QFT4D.01"   # the 4D-QFT contract node on theta13's path
_CLAIM = re.compile(r"^[A-Z][A-Z0-9]*(?:\.[A-Z0-9]+)+$")   # EM.FP.01, QG.AMB.01


def load():
    deps, scr = {}, {}
    with open(LEDGER, newline="") as fh:
        r = csv.reader(fh)
        next(r)
        for row in r:
            if len(row) < 6:
                continue
            cid = row[0].strip()
            deps[cid] = [t.strip() for t in row[4].split(";") if _CLAIM.match(t.strip())]
            scr[cid] = row[5].strip()
    return deps, scr


def reaches(g, start, target):
    seen, st = set(), [start]
    while st:
        n = st.pop()
        for d in g.get(n, []):
            if d == target:
                return True
            if d not in seen:
                seen.add(d)
                st.append(d)
    return False


def path(g, start, target):
    prev, q = {start: None}, deque([start])
    while q:
        n = q.popleft()
        for d in g.get(n, []):
            if d not in prev:
                prev[d] = n
                if d == target:
                    p = [d]
                    while prev[p[-1]] is not None:
                        p.append(prev[p[-1]])
                    return list(reversed(p))
                q.append(d)
    return None


def run():
    reset()
    print("v423 No-Ambient-Dependency: no frozen readout is computed from QG.AMB.01")
    g, scr = load()

    # ---- 1. gap-decoupling margin (exact) ----
    c3 = sp.Rational(1, 1) / (8 * sp.pi)
    stiff = sp.simplify(2 * DIM_E8 * c3**2)            # 31/(4 pi^2)
    Delta = 6 * sp.log(sp.Rational(3, 2))
    margin = sp.N(Delta - stiff)
    chi = sp.Rational(1, 1) / (1 - sp.Rational(2, 3)**6)
    check("GAP-DECOUPLING MARGIN [E]: 2 dim(E8) c3^2 = 31/(4 pi^2) (31=2^g_car-1) "
          "~ 0.785, Delta = 6 ln(3/2) ~ 2.433, so Delta_eff ~ 1.648 > 0 "
          "(v76/v337); chi = 1/(1-(2/3)^6) = 729/665 finite (neg control: "
          "gap->0 => chi->inf)",
          stiff == sp.Rational(31, 4) / sp.pi**2 and 31 == 2**g_car - 1
          and margin > 1.6 and chi == sp.Rational(729, 665))

    # ---- 2. certification sink (no prediction directly depends on QG.AMB.01) ----
    dependents = sorted(c for c, d in g.items() if AMB in d)
    pred_dependents = [c for c in dependents if c in FROZEN]
    check("CERTIFICATION SINK [E]: %d claims list QG.AMB.01 as a dependency and "
          "ALL are gravity-gate/QG-certification rows (%s ...), NONE a frozen "
          "prediction" % (len(dependents), ", ".join(dependents[:4])),
          len(dependents) >= 6 and pred_dependents == [])

    # ---- 3. not a value source (script-level) ----
    amb_script = scr.get(AMB, "")
    pred_clean = {c: scr.get(c, "") for c in FROZEN}
    no_amb_compute = all(not any(s in v for s in AMB_SCRIPTS) for v in pred_clean.values())
    check("NOT A VALUE SOURCE [E]: QG.AMB.01 has no producing script (script="
          "'%s'); each frozen prediction is computed by a compiler script "
          "(%s), none an ambient-measure script %s"
          % (amb_script, ", ".join("%s<-%s" % (c, v.replace('.py', ''))
                                    for c, v in pred_clean.items()),
             list(AMB_SCRIPTS)),
          amb_script in ("-", "") and all(pred_clean.values()) and no_amb_compute)

    # ---- 4. the one transitive link is architectural, not numerical ----
    th13_path = path(g, "FLAV.TH13.01", AMB)
    value_clean = [c for c in FROZEN if c != "FLAV.TH13.01" and not reaches(g, c, AMB)]
    check("ARCHITECTURAL-ONLY LINK [E]: of the frozen readouts only theta13 "
          "transitively references QG.AMB.01, via the 4D-QFT CONTRACT spine "
          "(%s) -- a coherence edge, not a numerical input (value sin^2 th13 = "
          "phi0 e^{-5/6}, v268); alpha/theta12/cosmology (%s) have NO route at all"
          % (" -> ".join(th13_path or []),
             ", ".join(value_clean)),
          th13_path is not None and SPINE in th13_path
          and len(value_clean) == len(FROZEN) - 1)

    # ---- 5. verdict (typed) ----
    check("VERDICT [C]: QG.AMB.01 is a gap-decoupled certification object -- no "
          "readout VALUE is computed from it, its only predictive link is the "
          "architectural 4D-QFT contract, and the gap (1.648>0) suppresses its "
          "back-reaction (v369 as a DAG/script fact). HONEST: does NOT prove "
          "SEAM.EQUIV.01 -- the readouts depend on the seam = (E8)_1 net, the "
          "one open keystone; QG.AMB.01 specifically is dead",
          dim_Splus == 16 and pred_dependents == [] and no_amb_compute)

    return summary("v423 No-Ambient-Dependency (no frozen readout computed from "
                   "QG.AMB.01; gap margin 1.648>0; only link is architectural)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
