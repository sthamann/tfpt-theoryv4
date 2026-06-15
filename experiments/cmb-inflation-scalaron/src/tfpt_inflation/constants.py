"""TFPT Starobinsky/scalaron inflation predictions, all from c3 = 1/(8 pi).

The low-curvature gravity branch is R + R^2 (spectral action), so inflation is
Starobinsky with the scalaron mass fixed by the compiler:

    M_scal = c3^{7/2} * Mbar  ~ 3.06e13 GeV     (Mbar = reduced Planck mass)

The Starobinsky read-offs depend on the e-fold number N_star (a reheating/observational
input, marker [C], band [50,60]); the reheating computation (v86) pins the slow-channel
point N_star = 51.4:

    n_s = 1 - 2/N_star
    r   = 12/N_star^2
    A_s = N_star^2/(24 pi^2) * c3^7

Typed [C]: N_star is an input, not a compiler output; M_scal and the R+R^2 form are [E].
"""

from __future__ import annotations

import math

C3: float = 1.0 / (8.0 * math.pi)
MBAR_GEV: float = 2.435e18                      # reduced Planck mass
M_SCAL_GEV: float = C3**3.5 * MBAR_GEV          # ~3.06e13 GeV
N_STAR_POINT: float = 51.4                      # slow Higgs-channel reheating (v86)
N_STAR_BAND: tuple[float, float] = (50.0, 60.0)


def n_s(n_star: float) -> float:
    return 1.0 - 2.0 / n_star


def r_tensor(n_star: float) -> float:
    return 12.0 / n_star**2


def a_s(n_star: float) -> float:
    return n_star**2 / (24.0 * math.pi**2) * C3**7


def summary() -> dict[str, float]:
    return {
        "c3": C3, "M_scal_GeV": M_SCAL_GEV, "N_star_point": N_STAR_POINT,
        "n_s_point": n_s(N_STAR_POINT), "r_point": r_tensor(N_STAR_POINT),
        "A_s_point": a_s(N_STAR_POINT),
        "n_s_band": (n_s(N_STAR_BAND[1]), n_s(N_STAR_BAND[0])),
        "r_band": (r_tensor(N_STAR_BAND[1]), r_tensor(N_STAR_BAND[0])),
    }
