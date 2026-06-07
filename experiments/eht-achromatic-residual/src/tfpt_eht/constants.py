"""TFPT theory constants — computed, never assumed.

All constants are derived from the single retained seed

    phi0 = 1/(6*pi) + 3/(256*pi**4)

and the seam constant c3 = 1/(8*pi). No SI value is hard-coded. The
no-knobs audit of TFPT Paper 3 requires that every constant entering
the EHT prediction can be traced back to phi0 and c3.
"""

from __future__ import annotations

import math
from typing import Final

#: Seam normalization. Paper 1, eq. for c3, derived from boundary
#: kernel: c3 = 1/(8 pi).
C3: Final[float] = 1.0 / (8.0 * math.pi)

#: Retained seed of the TFPT closed branch. Paper 3:
#: phi0 = 1/(6 pi) + 3/(256 pi**4).
PHI0: Final[float] = 1.0 / (6.0 * math.pi) + 3.0 / (256.0 * math.pi**4)

#: Global cosmic-birefringence amplitude (radians). Paper 3:
#: beta_rad = phi0 / (4 pi).
BETA_RAD: Final[float] = PHI0 / (4.0 * math.pi)

#: Same amplitude in degrees. Should evaluate to ~0.2424°.
BETA_DEG: Final[float] = math.degrees(BETA_RAD)

#: Topological coefficient delta_top = 48 c3**4 controlling the
#: precision-zone correction of the alpha-kernel and the structured
#: local EHT amplitude.
DELTA_TOP: Final[float] = 48.0 * C3**4

#: TFPT achromatic dyonic coupling. Paper 3, eq. (3):
#: 1/(256 pi**4) = 16 c3**4 = delta_top / 3.
#:
#: This is the *fixed* coupling that multiplies the geometric weights
#: Q_e_eff * Q_m_eff / r**2. The three equivalent expressions must agree
#: to machine precision — see tests.
TFPT_COUPLING: Final[float] = 1.0 / (256.0 * math.pi**4)

#: Internal precision tag for audit consistency checks.
_AUDIT_EPS: Final[float] = 1.0e-15


def audit_self_consistency() -> dict[str, float]:
    """Return the four equivalent expressions of the TFPT EHT coupling.

    All four must agree to machine precision. Used by the test suite to
    guard against accidental drift between the boundary kernel, the
    topological coefficient, and the per-radius response coefficient.
    """
    return {
        "1/(256*pi**4)": 1.0 / (256.0 * math.pi**4),
        "16*c3**4": 16.0 * C3**4,
        "delta_top/3": DELTA_TOP / 3.0,
        "TFPT_COUPLING": TFPT_COUPLING,
    }
