"""TFPT mixing-angle predictions of record, all from c3 / phi0.

    sin^2 theta12 = 1/3 - phi0/2       (TBM + seam misalignment)   = 0.306747
    sin^2 theta13 = phi0 * e^(-5/6)    (seed x carrier-trace)       = 0.0231
    sin^2 theta23 = 1/2                (mu-tau symmetric; octant not selected)
    delta_CKM     = pi/3 + 3 lambda^2  (frozen of record)           = 68.65 deg
    delta_PMNS    = 4 pi/3             (hexagonal mu6 unit, sheet)  = 240 deg

theta12/theta13/theta23 are PMNS (neutrino) predictions of record [E/C]; delta_CKM is
the CKM CP phase (confronted with the LHCb/Belle gamma combination).

delta_PMNS is the leptonic CP phase. Per the v220/v225/v231/v233 reduction, BOTH CP
phases are ONE hexagonal CM unit rho = e^{i pi/3} (the j=0 Eisenstein modulus, the
phase fiber over the square mu4 seam), read on the two sheets (rho^3 = -1):

    delta_CKM,lead = arg(rho^1) = pi/3   = 60 deg    (quark sector)
    delta_PMNS     = arg(rho^4) = 4 pi/3 = 240 deg   (lepton sector)
    => delta_PMNS = delta_CKM,lead + pi   (the exact Z2 sheet flip)

This is a [C] downstream bridge, NOT a primitive compiler output: the seam DECK stays
Z/4 (the v215 kill-test selects the square modulus); CP lives in the hexagonal PHASE
FIBER over it. The leading quark phase carries an extra +3 lambda^2 seam misalignment
(v88), giving the full delta_CKM = 68.65 deg; the lepton phase is the bare 4 pi/3.
"""

from __future__ import annotations

import math

C3: float = 1.0 / (8.0 * math.pi)
PHI0: float = (4.0 / 3.0) * C3 + 48.0 * C3**4

SIN2_THETA12: float = 1.0 / 3.0 - PHI0 / 2.0          # 0.306747
SIN2_THETA13: float = PHI0 * math.exp(-5.0 / 6.0)     # 0.0231
SIN2_THETA23: float = 0.5                             # octant not selected
LAMBDA_CABIBBO: float = math.sqrt(PHI0 * (1.0 - PHI0))                  # |Vus|, seed-derived
# frozen of record: delta = pi/3 + 3 lambda^2 = 68.654 deg (canonical v88/FLAV.CP.01)
DELTA_CKM_DEG: float = math.degrees(math.pi / 3.0 + 3.0 * LAMBDA_CABIBBO**2)
# leading (bare) quark phase = arg(rho^1) = pi/3 = 60 deg (hexagonal CM unit; v220/v231)
DELTA_CKM_LEAD_DEG: float = 60.0
# leptonic CP phase = arg(rho^4) = 4 pi/3 = 240 deg = delta_CKM,lead + 180 (sheet; v231/v233)
DELTA_PMNS_DEG: float = 240.0


def summary() -> dict[str, float]:
    return {
        "phi0": PHI0,
        "sin2_theta12": SIN2_THETA12,
        "sin2_theta13": SIN2_THETA13,
        "sin2_theta23": SIN2_THETA23,
        "delta_CKM_deg": DELTA_CKM_DEG,
        "delta_PMNS_deg": DELTA_PMNS_DEG,
    }
