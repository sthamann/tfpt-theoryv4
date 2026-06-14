"""Macquart relation utilities for the FRB.05 baryon (Omega_b) test.

The mean cosmic dispersion measure of the diffuse ionised IGM is (Macquart et
al. 2020; Deng & Zhang 2014)

    <DM_cosmic(z)> = (3 c H0 Omega_b f_IGM chi) / (8 pi G m_p) * I(z),
    I(z) = int_0^z (1+z') / E(z') dz',   E(z) = sqrt(Om (1+z)^3 + OL).

chi ~ 7/8 is the free electrons per baryon (ionised H+He), f_IGM ~ 0.84 the
baryon fraction in the diffuse IGM.  DM_cosmic is linear in the amplitude
``Omega_b * f_IGM``, so fitting localized-FRB DM_cosmic against I(z) recovers
``Omega_b`` once ``f_IGM`` is fixed.
"""

from __future__ import annotations

import numpy as np
from scipy import integrate

# --- fixed cosmology (Planck-2018 flat LCDM) used only for the geometry E(z) -
OMEGA_M: float = 0.315
OMEGA_L: float = 1.0 - OMEGA_M
H0_LITTLE_H: float = 0.674

# --- physical constants (SI) ----------------------------------------------
_C = 2.99792458e8          # m/s
_G = 6.674e-11             # m^3 kg^-1 s^-2
_MP = 1.6726219e-27        # kg
_H0_PER_H = 3.2407793e-18  # s^-1 for h = 1  (100 km/s/Mpc)
_PC_CM3_PER_M2 = 3.0856776e22  # 1 pc cm^-3 = this many m^-2

CHI_E: float = 7.0 / 8.0   # free electrons per baryon (ionised H+He)
F_IGM: float = 0.84        # diffuse-IGM baryon fraction (Macquart 2020)


def E(z: float) -> float:
    return np.sqrt(OMEGA_M * (1.0 + z) ** 3 + OMEGA_L)


def macquart_integral(z: float) -> float:
    """I(z) = int_0^z (1+z')/E(z') dz'."""
    val, _ = integrate.quad(lambda zp: (1.0 + zp) / E(zp), 0.0, z)
    return val


def dm_cosmic(z, omega_b: float, h: float = H0_LITTLE_H,
              f_igm: float = F_IGM, chi: float = CHI_E) -> np.ndarray:
    """Mean cosmic DM (pc cm^-3) at redshift(s) ``z``."""
    z = np.atleast_1d(np.asarray(z, dtype=float))
    iz = np.array([macquart_integral(float(zz)) for zz in z])
    pref = 3.0 * _C * (h * _H0_PER_H) / (8.0 * np.pi * _G * _MP)  # m^-2
    return pref * omega_b * f_igm * chi * iz / _PC_CM3_PER_M2


def fit_omega_b(z: np.ndarray, dm_cosmic_obs: np.ndarray, sigma: np.ndarray | None = None,
                h: float = H0_LITTLE_H, f_igm: float = F_IGM, chi: float = CHI_E):
    """Weighted least-squares fit of Omega_b from DM_cosmic vs I(z).

    Returns (omega_b, omega_b_err).  DM_cosmic = K * Omega_b * I(z) with K the
    fixed prefactor, so this is a one-parameter linear fit through the origin.
    """
    z = np.asarray(z, dtype=float)
    y = np.asarray(dm_cosmic_obs, dtype=float)
    iz = np.array([macquart_integral(float(zz)) for zz in z])
    pref = 3.0 * _C * (h * _H0_PER_H) / (8.0 * np.pi * _G * _MP) / _PC_CM3_PER_M2
    design = pref * f_igm * chi * iz                      # y = omega_b * design
    w = 1.0 / np.asarray(sigma, float) ** 2 if sigma is not None else np.ones_like(y)
    num = np.sum(w * design * y)
    den = np.sum(w * design * design)
    omega_b = num / den
    resid = y - omega_b * design
    dof = max(1, len(y) - 1)
    var = np.sum(w * resid * resid) / dof / den
    return float(omega_b), float(np.sqrt(var))
