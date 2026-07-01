"""Standard-Model gauge RGE machinery (PDG boundary conditions).

The measured SM couplings at M_Z are the ONLY external theory inputs on the TFPT side:
they are boundary conditions for the running, exactly as in the load-bearing modules
verification/v249 (PS.RGTEST.01) and v266 (PS.PROTON.02) and the gauge-unification
reproducer. The high-scale content (the Pati-Salam beta coefficients) and the scalaron
scale flow from the TFPT axioms; see ``unification.py``.

Conventions: alpha_i^-1 GUT-normalised (alpha_1 = 5/3 alpha_Y), b_1 GUT-normalised.
"""

from __future__ import annotations

import math

import numpy as np

# --- PDG 2024 inputs at M_Z (MSbar) -- external measured boundary conditions ----------
M_Z = 91.1876
ALPHA_EM_INV = 127.951        # alpha_em^-1(M_Z)
SIN2_W_MEAS = 0.23122         # sin^2 theta_W^MSbar(M_Z)
ALPHA_S = 0.1179              # alpha_s(M_Z)

# 1-loop SM beta coefficients b=(b1,b2,b3), b1 GUT-normalised (v159/v246)
B1L = (41.0 / 10.0, -19.0 / 6.0, -7.0)

# 2-loop SM gauge beta matrix b_ij (gauge sector; Yukawa neglected -- small for this test)
B2L = np.array([
    [199.0 / 50.0, 27.0 / 10.0, 44.0 / 5.0],
    [9.0 / 10.0, 35.0 / 6.0, 12.0],
    [11.0 / 10.0, 9.0 / 2.0, -26.0],
])


def alpha_inv_at_MZ() -> tuple[float, float, float]:
    """(alpha1, alpha2, alpha3)^-1 at M_Z from the measured (alpha_em, sin^2, alpha_s).

    Reproduces the AINV ~ (59.0, 29.6, 8.5) used (hard-coded, rounded) in v249/v266.
    """
    cos2 = 1.0 - SIN2_W_MEAS
    a1 = (3.0 / 5.0) * cos2 * ALPHA_EM_INV    # GUT-normalised U(1)
    a2 = SIN2_W_MEAS * ALPHA_EM_INV
    a3 = 1.0 / ALPHA_S
    return a1, a2, a3


def run_2loop(a0: tuple[float, float, float], t: float, n: int = 3000) -> tuple[float, ...]:
    """Integrate the 2-loop SM gauge RGE for alpha_i^-1(mu), t = ln(mu/M_Z):

        d(alpha_i^-1)/dt = -b_i/(2 pi) - sum_j b_ij/(8 pi^2) * alpha_j .
    """
    ainv = np.array(a0, dtype=float)
    dt = t / n
    for _ in range(n):
        alpha = 1.0 / ainv
        d = np.array([-B1L[i] / (2 * math.pi)
                      - sum(B2L[i, j] / (8 * math.pi**2) * alpha[j] for j in range(3))
                      for i in range(3)])
        ainv = ainv + d * dt
    return tuple(ainv)
