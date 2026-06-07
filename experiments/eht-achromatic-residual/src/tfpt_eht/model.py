"""TFPT structured-residual prediction model.

Implements the prediction of TFPT Paper 3 §3 for the structured local
astrophysical birefringence amplitude near a magnetised compact object:

    beta_BH(r) = TFPT_COUPLING * Q_e_eff(x) * Q_m_eff(x) / r**2

evaluated in image-plane coordinates with `r` measured from the
photon-ring barycentre in units of the gravitational radius
``r_g = G M / c**2``. The amplitude is added to the GRMHD-predicted
linear-polarization angle at zero wavelength (the intercept of the
λ²-fit).
"""

from __future__ import annotations

import dataclasses
import math
from typing import Literal

import numpy as np
from numpy.typing import NDArray

from tfpt_eht.constants import TFPT_COUPLING


@dataclasses.dataclass(frozen=True)
class BlackHoleGeometry:
    """Image-plane geometry of a compact object in the EHT field.

    Coordinates are in units of the gravitational radius ``r_g``. The
    photon-ring barycentre is at ``(center_x, center_y)``.

    Parameters
    ----------
    center_x, center_y :
        Image-plane coordinates of the photon-ring barycentre.
    r_inner :
        Inner cutoff for the radial profile evaluation. Pixels below
        this radius are masked (they sit inside the photon ring and are
        not used for the achromatic-residual test). Default 4 r_g
        excludes the photon ring (M87: ring at ~5 r_g).
    r_outer :
        Outer cutoff for the radial profile evaluation. Default 30 r_g
        excludes the large-scale jet emission.
    sign_orientation :
        Sign convention for the effective E.B orientation. Reversing this
        is the **third null test**: a real TFPT signal flips sign under
        ``sign_orientation -> -sign_orientation``. A spurious systematic
        does not.
    """

    center_x: float = 0.0
    center_y: float = 0.0
    r_inner: float = 4.0
    r_outer: float = 30.0
    sign_orientation: Literal[+1, -1] = +1


def beta_bh_profile(
    radii: NDArray[np.floating],
    q_e_eff: float | NDArray[np.floating] = 1.0,
    q_m_eff: float | NDArray[np.floating] = 1.0,
    coupling: float = TFPT_COUPLING,
) -> NDArray[np.floating]:
    """Evaluate the TFPT structured residual amplitude.

    Parameters
    ----------
    radii :
        Image-plane radii in units of r_g (gravitational radii).
    q_e_eff, q_m_eff :
        Geometric weights of the effective electric and magnetic charges
        in the emission region. May be scalar (global) or per-pixel.
        Their product enters multiplicatively; only the product is
        physically meaningful.
    coupling :
        TFPT prefactor. Defaults to ``1/(256*pi**4) = 16*c3**4``.
        Exposed only so that null-hypothesis fits (coupling = 0) can be
        evaluated against the data using the same function.

    Returns
    -------
    beta_bh :
        The predicted residual intercept ``chi_0^res(r)`` in radians,
        with the conventional sign. Multiply by ``180/pi`` for degrees.
    """
    radii = np.asarray(radii, dtype=np.float64)
    with np.errstate(divide="ignore", invalid="ignore"):
        amplitude = coupling * np.asarray(q_e_eff) * np.asarray(q_m_eff) / radii**2
    amplitude = np.where(radii > 0.0, amplitude, 0.0)
    return amplitude


def chi0_tfpt(
    coords: tuple[NDArray[np.floating], NDArray[np.floating]],
    geometry: BlackHoleGeometry,
    q_e_eff: float | NDArray[np.floating] = 1.0,
    q_m_eff: float | NDArray[np.floating] = 1.0,
) -> NDArray[np.floating]:
    """Per-pixel TFPT contribution to the polarization-angle intercept.

    Parameters
    ----------
    coords :
        ``(x, y)`` image-plane coordinate arrays in units of r_g.
    geometry :
        Image geometry (centre, masking radii, sign convention).
    q_e_eff, q_m_eff :
        Geometric charge weights (scalar or per-pixel array).

    Returns
    -------
    chi0_tfpt :
        The signed TFPT contribution ``s * beta_BH(r)`` to the
        polarization-angle intercept ``chi_0(x)``, evaluated per pixel.
        Pixels outside ``[r_inner, r_outer]`` are set to 0.
    """
    x, y = coords
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    radii = np.hypot(x - geometry.center_x, y - geometry.center_y)
    amplitude = beta_bh_profile(radii, q_e_eff=q_e_eff, q_m_eff=q_m_eff)
    mask = (radii >= geometry.r_inner) & (radii <= geometry.r_outer)
    return np.where(mask, geometry.sign_orientation * amplitude, 0.0)


def expected_amplitude_at(
    radius: float,
    q_e_eff: float = 1.0,
    q_m_eff: float = 1.0,
) -> dict[str, float]:
    """Compact summary of the TFPT prediction at a chosen radius.

    Useful for sanity checks against the prediction note in the
    TFPT paper series. For ``radius=10`` r_g and unit geometric
    weights one finds ``beta_BH ≈ 4.1e-6 rad ≈ 2.3e-4 deg``.
    """
    amplitude = TFPT_COUPLING * q_e_eff * q_m_eff / radius**2
    return {
        "radius_rg": radius,
        "q_e_eff": q_e_eff,
        "q_m_eff": q_m_eff,
        "beta_bh_rad": amplitude,
        "beta_bh_deg": math.degrees(amplitude),
        "beta_bh_microdeg": math.degrees(amplitude) * 1.0e6,
    }
