"""Residual-intercept extraction from polarimetric image cubes.

Given a polarimetric image cube
``chi(x, lambda^2) = chi_0(x) + RM(x) * lambda^2 + epsilon``,
the residual intercept ``chi_0^res(x)`` is the part of the
zero-wavelength intercept left after subtracting the GRMHD/synchrotron
forward model:

    chi_0^res(x) = chi_0^obs(x) - chi_0^GRMHD(x).

This module provides:

* a per-pixel weighted-least-squares fit of ``chi(lambda^2)`` to obtain
  ``chi_0^obs(x)`` and ``RM(x)``;
* the subtraction step producing ``chi_0^res(x)``;
* a deprojection helper that bins ``chi_0^res(x)`` into a radial
  profile around the photon-ring barycentre.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray


@dataclasses.dataclass(frozen=True)
class PolarimetricImage:
    """Container for a multi-frequency polarimetric image cube.

    Attributes
    ----------
    x, y :
        2-D coordinate arrays in units of r_g (shape ``(H, W)``).
    lambda_sq :
        1-D array of wavelength-squared values for each frequency channel
        (shape ``(F,)``, units m^2).
    chi :
        3-D array of measured polarization angles in radians, shape
        ``(F, H, W)``.
    sigma_chi :
        3-D array of per-pixel angle uncertainties (same shape as
        ``chi``).
    """

    x: NDArray[np.floating]
    y: NDArray[np.floating]
    lambda_sq: NDArray[np.floating]
    chi: NDArray[np.floating]
    sigma_chi: NDArray[np.floating]

    @property
    def shape(self) -> tuple[int, int, int]:
        return self.chi.shape


def rotation_measure_fit(
    image: PolarimetricImage,
) -> tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """Fit ``chi = chi_0 + RM * lambda^2`` per pixel with weighted LSQ.

    Returns
    -------
    chi_0_obs :
        Zero-wavelength intercept per pixel (radians), shape ``(H, W)``.
    rotation_measure :
        Faraday rotation measure per pixel (rad / m^2), shape ``(H, W)``.
    sigma_chi_0 :
        1-sigma uncertainty on ``chi_0_obs`` per pixel, shape ``(H, W)``.
    """
    lam = np.asarray(image.lambda_sq, dtype=np.float64).reshape(-1, 1, 1)
    chi = np.asarray(image.chi, dtype=np.float64)
    sigma = np.asarray(image.sigma_chi, dtype=np.float64)

    if chi.shape != sigma.shape:
        raise ValueError("chi and sigma_chi must have identical shape")
    if chi.shape[0] != lam.shape[0]:
        raise ValueError("first axis of chi must match length of lambda_sq")

    weights = 1.0 / np.square(sigma)
    sum_w = np.sum(weights, axis=0)
    sum_wx = np.sum(weights * lam, axis=0)
    sum_wxx = np.sum(weights * lam**2, axis=0)
    sum_wy = np.sum(weights * chi, axis=0)
    sum_wxy = np.sum(weights * lam * chi, axis=0)

    determinant = sum_w * sum_wxx - sum_wx**2
    determinant = np.where(determinant == 0.0, np.nan, determinant)

    chi_0_obs = (sum_wxx * sum_wy - sum_wx * sum_wxy) / determinant
    rotation_measure = (sum_w * sum_wxy - sum_wx * sum_wy) / determinant
    sigma_chi_0_sq = sum_wxx / determinant
    sigma_chi_0 = np.sqrt(np.abs(sigma_chi_0_sq))
    return chi_0_obs, rotation_measure, sigma_chi_0


def compute_residual_intercept(
    chi_0_obs: NDArray[np.floating],
    chi_0_grmhd: NDArray[np.floating],
) -> NDArray[np.floating]:
    """Compute the residual intercept ``chi_0^res = chi_0^obs - chi_0^GRMHD``.

    The subtraction is point-wise; both maps must have identical shape
    and identical pixel coordinates. Out-of-mask pixels should be set
    to NaN in either input.
    """
    chi_0_obs = np.asarray(chi_0_obs, dtype=np.float64)
    chi_0_grmhd = np.asarray(chi_0_grmhd, dtype=np.float64)
    if chi_0_obs.shape != chi_0_grmhd.shape:
        raise ValueError("residual inputs must have identical shape")
    return chi_0_obs - chi_0_grmhd


@dataclasses.dataclass(frozen=True)
class RadialProfile:
    """Azimuthally averaged radial profile of a per-pixel field.

    Attributes
    ----------
    radii :
        Bin centres in units of r_g.
    values :
        Mean (or median) of the field within each radial bin.
    sigma :
        Standard error of the mean within each bin.
    counts :
        Number of pixels per bin.
    """

    radii: NDArray[np.floating]
    values: NDArray[np.floating]
    sigma: NDArray[np.floating]
    counts: NDArray[np.integer]


def deproject_radial(
    field: NDArray[np.floating],
    x: NDArray[np.floating],
    y: NDArray[np.floating],
    *,
    center: tuple[float, float] = (0.0, 0.0),
    bin_edges: Sequence[float] | NDArray[np.floating] | None = None,
    r_inner: float = 4.0,
    r_outer: float = 30.0,
    n_bins: int = 20,
    statistic: str = "mean",
) -> RadialProfile:
    """Azimuthally bin ``field`` into radial bins around ``center``.

    Pixels with ``NaN`` in ``field`` are excluded. The default radial
    range ``[r_inner, r_outer]`` covers the relevant annulus for
    M87*-class images (r_inner > photon ring, r_outer < jet emission).
    """
    field = np.asarray(field, dtype=np.float64)
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)

    radii = np.hypot(x - center[0], y - center[1])

    if bin_edges is None:
        bin_edges = np.linspace(r_inner, r_outer, n_bins + 1)
    bin_edges = np.asarray(bin_edges, dtype=np.float64)
    n = len(bin_edges) - 1

    centres = np.empty(n, dtype=np.float64)
    values = np.empty(n, dtype=np.float64)
    sigma = np.empty(n, dtype=np.float64)
    counts = np.empty(n, dtype=np.int64)

    flat_r = radii.ravel()
    flat_v = field.ravel()
    valid = np.isfinite(flat_v)

    for i in range(n):
        in_bin = (flat_r >= bin_edges[i]) & (flat_r < bin_edges[i + 1]) & valid
        centres[i] = 0.5 * (bin_edges[i] + bin_edges[i + 1])
        if not np.any(in_bin):
            values[i] = np.nan
            sigma[i] = np.nan
            counts[i] = 0
            continue
        sample = flat_v[in_bin]
        counts[i] = sample.size
        if statistic == "mean":
            values[i] = float(np.mean(sample))
        elif statistic == "median":
            values[i] = float(np.median(sample))
        else:
            raise ValueError(f"unknown statistic: {statistic}")
        if sample.size > 1:
            sigma[i] = float(np.std(sample, ddof=1) / np.sqrt(sample.size))
        else:
            sigma[i] = np.nan

    return RadialProfile(radii=centres, values=values, sigma=sigma, counts=counts)
