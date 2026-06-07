"""Synthetic polarimetric image cubes for end-to-end pipeline testing.

The synthetic generators below produce three classes of mock data, each
intentionally designed to test a different part of the pipeline:

* **observed mock**: GRMHD model + TFPT signal + Gaussian noise. The
  signal should be detected by all three nulls.
* **GRMHD-only mock**: same disc model with TFPT signal *off*. The
  pipeline should *not* claim a detection.
* **systematic mock**: GRMHD + flat (constant) intercept residual to
  emulate a calibration error. The frequency null should pass, but the
  profile and sign-flip nulls should fail.

The synthetic models are physically simplistic (axisymmetric, no
relativistic boosting). They are *not* a substitute for real GRMHD;
their purpose is to validate the pipeline logic and to provide a
falsification baseline.
"""

from __future__ import annotations

import dataclasses
from typing import Final

import numpy as np
from numpy.typing import NDArray

from tfpt_eht.model import BlackHoleGeometry, chi0_tfpt
from tfpt_eht.residual import PolarimetricImage

DEFAULT_LAMBDA_SQ: Final[NDArray[np.float64]] = np.array(
    # Six EHT-like channels in m^2, around 230 GHz and 345 GHz.
    [
        (3.0e8 / 230.0e9) ** 2,
        (3.0e8 / 240.0e9) ** 2,
        (3.0e8 / 270.0e9) ** 2,
        (3.0e8 / 300.0e9) ** 2,
        (3.0e8 / 320.0e9) ** 2,
        (3.0e8 / 345.0e9) ** 2,
    ],
    dtype=np.float64,
)


@dataclasses.dataclass(frozen=True)
class SyntheticConfig:
    """Configuration for synthetic polarimetric image cubes.

    Attributes
    ----------
    image_size :
        Side length of the square image in pixels.
    field_of_view :
        Side length of the image in units of r_g.
    rotation_measure_scale :
        Standard deviation of the per-pixel RM distribution (rad/m^2).
    chi_grmhd_amplitude :
        Amplitude of the GRMHD intercept structure (radians).
    chi_grmhd_seed :
        RNG seed for the GRMHD intercept noise. Deterministic.
    angle_noise_sigma :
        Per-channel per-pixel measurement noise on chi (radians).
    angle_noise_seed :
        RNG seed for the measurement noise. Deterministic.
    q_e_eff, q_m_eff :
        Effective geometric charges (scalar; the TFPT signal scales as
        their product).
    lambda_sq :
        Wavelength-squared values per frequency channel.
    geometry :
        Black-hole image geometry.
    """

    image_size: int = 96
    field_of_view: float = 40.0
    rotation_measure_scale: float = 5.0e3
    chi_grmhd_amplitude: float = 0.30
    chi_grmhd_seed: int = 42
    angle_noise_sigma: float = 5.0e-7
    angle_noise_seed: int = 137
    q_e_eff: float = 1.0
    q_m_eff: float = 1.0
    lambda_sq: NDArray[np.floating] = dataclasses.field(
        default_factory=lambda: DEFAULT_LAMBDA_SQ.copy()
    )
    geometry: BlackHoleGeometry = dataclasses.field(default_factory=BlackHoleGeometry)


def _coordinate_grid(cfg: SyntheticConfig) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    side = np.linspace(
        -cfg.field_of_view / 2.0,
        cfg.field_of_view / 2.0,
        cfg.image_size,
        dtype=np.float64,
    )
    return np.meshgrid(side, side, indexing="xy")


def _grmhd_intercept(
    cfg: SyntheticConfig,
    x: NDArray[np.float64],
    y: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Smooth, axisymmetric GRMHD-mock intercept map (radians).

    Deliberately *not* a physical GRMHD code; just a smooth, large-scale
    pattern centred on the photon-ring barycentre. Used only to test
    the subtraction step.
    """
    rng = np.random.default_rng(cfg.chi_grmhd_seed)
    r = np.hypot(x - cfg.geometry.center_x, y - cfg.geometry.center_y)
    phi = np.arctan2(y - cfg.geometry.center_y, x - cfg.geometry.center_x)
    # Twisted spiral pattern -- coherent over the image scale.
    pattern = np.cos(2.0 * phi + r / 8.0) * np.exp(-r / 20.0)
    blob = rng.normal(0.0, 0.05, size=x.shape)
    return cfg.chi_grmhd_amplitude * pattern + cfg.chi_grmhd_amplitude * 0.05 * blob


def _rotation_measure_field(
    cfg: SyntheticConfig,
    x: NDArray[np.float64],
    y: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Per-pixel RM field. Coherent + small-scale Gaussian fluctuations."""
    rng = np.random.default_rng(cfg.chi_grmhd_seed + 1)
    r = np.hypot(x - cfg.geometry.center_x, y - cfg.geometry.center_y)
    phi = np.arctan2(y - cfg.geometry.center_y, x - cfg.geometry.center_x)
    coherent = cfg.rotation_measure_scale * np.cos(phi)
    noise = rng.normal(0.0, 0.2 * cfg.rotation_measure_scale, size=x.shape)
    envelope = np.exp(-r / 25.0)
    return envelope * (coherent + noise)


def _build_cube(
    cfg: SyntheticConfig,
    chi_0_map: NDArray[np.float64],
    rm_map: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Assemble ``chi(F, H, W) = chi_0 + RM * lambda^2 + noise`` and its sigma."""
    rng = np.random.default_rng(cfg.angle_noise_seed)
    lam = cfg.lambda_sq.reshape(-1, 1, 1)
    chi = chi_0_map[None, :, :] + rm_map[None, :, :] * lam
    noise = rng.normal(0.0, cfg.angle_noise_sigma, size=chi.shape)
    chi = chi + noise
    sigma = np.full_like(chi, cfg.angle_noise_sigma, dtype=np.float64)
    return chi, sigma


@dataclasses.dataclass(frozen=True)
class GRMHDModel:
    """Forward-model output for the residual pipeline.

    Attributes
    ----------
    chi_0 :
        2-D intercept map ``chi_0_grmhd(x)``.
    cube :
        Optional 3-D model ``chi_grmhd(f, x)`` evaluated at the same
        wavelengths as the observations. Used for cube-level residuals
        (needed by the frequency null).
    rotation_measure :
        Optional 2-D RM map ``RM_grmhd(x)``. Reconstructed from
        ``chi_0`` and ``cube`` if not supplied.
    """

    chi_0: NDArray[np.float64]
    cube: NDArray[np.float64]
    rotation_measure: NDArray[np.float64]


def generate_grmhd_mock(cfg: SyntheticConfig | None = None) -> tuple[PolarimetricImage, GRMHDModel]:
    """Build a mock with *no* TFPT signal -- GRMHD intercept only.

    Returns
    -------
    image :
        Synthetic ``PolarimetricImage`` (chi cube + sigma cube).
    grmhd :
        The truth GRMHD model: intercept, cube, and RM map.
    """
    cfg = cfg or SyntheticConfig()
    x, y = _coordinate_grid(cfg)
    chi_0_map = _grmhd_intercept(cfg, x, y)
    rm_map = _rotation_measure_field(cfg, x, y)
    chi, sigma = _build_cube(cfg, chi_0_map, rm_map)
    grmhd_cube = chi_0_map[None, :, :] + rm_map[None, :, :] * cfg.lambda_sq.reshape(-1, 1, 1)
    return (
        PolarimetricImage(x=x, y=y, lambda_sq=cfg.lambda_sq, chi=chi, sigma_chi=sigma),
        GRMHDModel(chi_0=chi_0_map, cube=grmhd_cube, rotation_measure=rm_map),
    )


def generate_observed_mock(
    cfg: SyntheticConfig | None = None,
    *,
    tfpt_signal: bool = True,
    systematic_offset: float = 0.0,
) -> tuple[PolarimetricImage, GRMHDModel]:
    """Build a mock with optional TFPT signal and optional systematic.

    Parameters
    ----------
    cfg :
        Synthetic configuration (defaults to ``SyntheticConfig()``).
    tfpt_signal :
        If ``True``, add the TFPT structured-residual amplitude
        ``chi0_tfpt(coords, geometry)`` to the intercept map.
    systematic_offset :
        Constant value added to the intercept map to emulate a
        calibration error. Used to test that the profile null and
        sign-flip null reject systematics that pass the frequency null.

    Returns
    -------
    image :
        The synthetic ``PolarimetricImage``.
    grmhd :
        The GRMHD-truth model (intercept, cube, RM map). It contains
        the *clean* GRMHD-only prediction -- the TFPT signal lives only
        in ``image.chi`` -- so the residual cube ``image.chi -
        grmhd.cube`` recovers the TFPT contribution plus measurement
        noise.
    """
    cfg = cfg or SyntheticConfig()
    x, y = _coordinate_grid(cfg)
    chi_0_grmhd = _grmhd_intercept(cfg, x, y)
    chi_0_total = chi_0_grmhd.copy()
    if tfpt_signal:
        chi_0_total = chi_0_total + chi0_tfpt(
            coords=(x, y),
            geometry=cfg.geometry,
            q_e_eff=cfg.q_e_eff,
            q_m_eff=cfg.q_m_eff,
        )
    if systematic_offset != 0.0:
        chi_0_total = chi_0_total + systematic_offset
    rm_map = _rotation_measure_field(cfg, x, y)
    chi, sigma = _build_cube(cfg, chi_0_total, rm_map)
    grmhd_cube = chi_0_grmhd[None, :, :] + rm_map[None, :, :] * cfg.lambda_sq.reshape(-1, 1, 1)
    return (
        PolarimetricImage(x=x, y=y, lambda_sq=cfg.lambda_sq, chi=chi, sigma_chi=sigma),
        GRMHDModel(chi_0=chi_0_grmhd, cube=grmhd_cube, rotation_measure=rm_map),
    )
