"""TFPT mixing-angle predictions of record, all from c3 / phi0.

    sin^2 theta12 = 1/3 - phi0/2       (TBM + seam misalignment)   = 0.306747
    sin^2 theta13 = phi0 * e^(-5/6)    (seed x carrier-trace)       = 0.0231
    sin^2 theta23 = 1/2                (mu-tau symmetric; octant not selected)
    delta_CKM     = pi/3 + 3 lambda^2  (frozen of record)           = 68.65 deg

theta12/theta13/theta23 are PMNS (neutrino) predictions of record [E/C]; delta_CKM is
the CKM CP phase (different sector, confronted with the LHCb/Belle gamma combination).
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


def summary() -> dict[str, float]:
    return {
        "phi0": PHI0,
        "sin2_theta12": SIN2_THETA12,
        "sin2_theta13": SIN2_THETA13,
        "sin2_theta23": SIN2_THETA23,
        "delta_CKM_deg": DELTA_CKM_DEG,
    }
