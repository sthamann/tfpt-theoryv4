"""Frozen TFPT seed constants for the cross-domain birefringence/baryon test.

Everything here flows from the single seam constant ``c3 = 1/(8 pi)`` (P1); no SI
value and no measured cosmology is imported into the prediction layer. The seed is

    phi0   = (4/3) c3 + 48 c3^4                       (origin_theory, v60)
    beta   = phi0 / (4 pi)         [radians]          (cosmic birefringence)
    Omega_b = (4 pi - 1) * beta                       (baryon fraction)

so a SINGLE seed ``phi0`` predicts BOTH the CMB rotation angle and the baryon
fraction, on the frozen line

    Omega_b / beta_rad = 4 pi - 1 .

The cross-domain test (``seed_line.py``) confronts that one line with two
independent measurements (ACT DR6 beta; Planck/BBN Omega_b).
"""

from __future__ import annotations

import math

C3: float = 1.0 / (8.0 * math.pi)                     # seam constant, P1
PHI0: float = (4.0 / 3.0) * C3 + 48.0 * C3**4         # retarded seed phi0
BETA_RAD: float = PHI0 / (4.0 * math.pi)              # birefringence angle [rad]
BETA_DEG: float = math.degrees(BETA_RAD)              # ~0.2424 deg
SEED_SLOPE: float = 4.0 * math.pi - 1.0              # the frozen Omega_b/beta_rad line
OMEGA_B: float = SEED_SLOPE * BETA_RAD                # ~0.04894


def summary() -> dict[str, float]:
    return {
        "c3": C3,
        "phi0": PHI0,
        "beta_rad": BETA_RAD,
        "beta_deg": BETA_DEG,
        "seed_slope_4pi_minus_1": SEED_SLOPE,
        "Omega_b": OMEGA_B,
    }
