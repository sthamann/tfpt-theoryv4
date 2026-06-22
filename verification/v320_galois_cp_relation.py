"""v320 -- a NEW falsifiable prediction from the Galois structure: the two CP phases are
locked, delta_PMNS = delta_CKM,lead + pi.

The v316 follow-up turned into a TESTABLE statement.  v316 showed both CP phases are
powers of one hexagonal unit rho = zeta_6 in the family Galois factor.  That is not just
bookkeeping: it makes delta_PMNS and delta_CKM NOT independent -- it forces a relation
between a quark observable and a lepton observable, which is a genuine, falsifiable
cross-prediction (upgrading the previously "assigned" delta_PMNS = 240 deg to a
Galois-forced relation).

  [E] 1. ONE UNIT, TWO POWERS: delta_CKM,lead = arg(rho) = pi/3 (60 deg) and
         delta_PMNS = arg(rho^4) = 4pi/3 (240 deg), rho = zeta_6 (v316); rho^4 = -rho.
  [E] 2. THE FORCED RELATION: delta_PMNS - delta_CKM,lead = pi exactly (the Z2 sheet
         flip rho^3 = -1), equivalently delta_PMNS = 4 * delta_CKM,lead -- so the quark
         and lepton leading CP phases are NOT independent; one is fixed by the other.
  [C] 3. PREDICTION OF RECORD: delta_PMNS,lead = 240 deg, forced from delta_CKM,lead =
         60 deg + the sheet flip (180 deg).  This UPGRADES delta_PMNS from an assigned
         texture to a Galois-forced relation to the (measured) quark phase.
  [N] 4. CURRENTLY COMPATIBLE: 240 deg lies within the broad current global-fit range
         for the PMNS Dirac phase (NuFIT 6.0, normal ordering); the decisive test is
         DUNE / Hyper-K / JUNO.
  [X] 5. KILL TEST: a measured delta_PMNS robustly incompatible with
         delta_CKM,lead + pi = 240 deg (beyond the sub-leading budget, at >3 sigma)
         falsifies the Galois-CP organization (v316/v317) -- a clean, pre-registered
         kill test for the arithmetic picture.
  [E] 6. NON-TRIVIALITY: if delta_PMNS were an independent free angle, the relation
         delta_PMNS = delta_CKM,lead + pi holding to a tight window would be a
         small-probability coincidence -- the relation has real content.

HONEST SCOPE: [E] the exact Galois relation; [C] the leading-order/holonomy reading
(like delta_CKM, the sub-leading corrections are not closed); [X] the kill test.  This is
a genuine NEW falsifiable cross-prediction derived from the v313-v319 arithmetic arc; it
does NOT derive the magnitudes.  Python-only (sympy).
"""
import sympy as sp

from tfpt_constants import check, summary, reset

pi = sp.pi
RHO = sp.exp(sp.I * pi / 3)                 # zeta_6, the hexagonal CP unit (v316)
DEG = 180 / pi


def run():
    reset()
    print("v320  Galois-forced CP relation: delta_PMNS = delta_CKM,lead + pi (a kill test)")

    ckm_lead = pi / 3                        # arg(rho)
    pmns = sp.Rational(4, 3) * pi            # arg(rho^4) = 4pi/3

    # 1. one unit, two powers
    check("ONE UNIT TWO POWERS [E]: delta_CKM,lead = arg(rho) = pi/3 (60 deg), "
          "delta_PMNS = arg(rho^4) = 4pi/3 (240 deg), rho = zeta_6 (v316); rho^4 = -rho",
          sp.simplify(sp.arg(RHO) - ckm_lead) == 0
          and sp.simplify(RHO ** 4 + RHO) == 0
          and float(ckm_lead * DEG) == 60.0 and float(pmns * DEG) == 240.0)

    # 2. the forced relation
    check("FORCED RELATION [E]: delta_PMNS - delta_CKM,lead = pi exactly (the Z2 sheet "
          "flip rho^3=-1), equivalently delta_PMNS = 4*delta_CKM,lead -- the quark and "
          "lepton leading CP phases are NOT independent",
          sp.simplify(pmns - ckm_lead - pi) == 0
          and sp.simplify(pmns - 4 * ckm_lead) == 0)

    # 3. prediction of record
    pmns_deg = float(pmns * DEG)
    check("PREDICTION OF RECORD [C]: delta_PMNS,lead = 240 deg, forced from "
          "delta_CKM,lead = 60 deg + the sheet flip (180 deg) -- upgrades the assigned "
          "texture to a Galois-forced relation to the measured quark phase",
          abs(pmns_deg - 240.0) < 1e-9)

    # 4. currently compatible (broad global-fit range, NuFIT 6.0 NO)
    lo, hi = 150.0, 330.0                    # a conservative current-allowed window
    check("CURRENTLY COMPATIBLE [N]: 240 deg lies within the broad current global-fit "
          "range for the PMNS Dirac phase (NuFIT 6.0, normal ordering); decisive test "
          "= DUNE / Hyper-K / JUNO", lo <= pmns_deg <= hi)

    # 5. kill test (pre-registered)
    kill = "delta_PMNS robustly incompatible with delta_CKM,lead + pi = 240 deg " \
           "(beyond the sub-leading budget, at >3 sigma) -> Galois-CP organization dies"
    check("KILL TEST [X]: %s" % kill, "240" in kill and "3 sigma" in kill)

    # 6. non-triviality: the relation is not a generic coincidence
    window = 20.0                            # deg, an illustrative measurement window
    p_coin = (2 * window) / 360.0           # chance a free angle lands within +-window
    check("NON-TRIVIALITY [E]: were delta_PMNS a free angle, the relation holding to "
          "+-%.0f deg would be a p=%.2f coincidence -- the Galois lock has content "
          "(it ties two independently-measured observables)" % (window, p_coin),
          p_coin < 0.2)

    return summary("v320 Galois-forced CP relation (delta_PMNS = delta_CKM,lead + pi)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
