"""Tests for the rotation-measure fit and the residual extraction."""

from __future__ import annotations

import numpy as np
import pytest

from tfpt_eht.residual import (
    PolarimetricImage,
    compute_residual_intercept,
    deproject_radial,
    rotation_measure_fit,
)


def _make_synthetic_cube(
    chi_0_truth: float,
    rm_truth: float,
    *,
    n_channels: int = 6,
    n_pixels: int = 16,
    noise_sigma: float = 1.0e-7,
    seed: int = 7,
) -> PolarimetricImage:
    """Build a small uniform-truth cube to validate the LSQ fitter."""
    rng = np.random.default_rng(seed)
    lam2 = np.linspace(1.5e-7, 1.0e-6, n_channels)
    x = np.linspace(-10.0, 10.0, n_pixels)
    y = np.linspace(-10.0, 10.0, n_pixels)
    X, Y = np.meshgrid(x, y, indexing="xy")
    chi = (
        chi_0_truth
        + rm_truth * lam2.reshape(-1, 1, 1)
        + rng.normal(0.0, noise_sigma, size=(n_channels, n_pixels, n_pixels))
    )
    sigma = np.full_like(chi, noise_sigma, dtype=np.float64)
    return PolarimetricImage(x=X, y=Y, lambda_sq=lam2, chi=chi, sigma_chi=sigma)


def test_rotation_measure_fit_recovers_truth():
    img = _make_synthetic_cube(chi_0_truth=0.5, rm_truth=1.0e5, noise_sigma=1.0e-6)
    chi_0, rm, sigma = rotation_measure_fit(img)
    assert chi_0.mean() == pytest.approx(0.5, abs=2.0e-3)
    assert rm.mean() == pytest.approx(1.0e5, rel=2.0e-3)
    assert sigma.mean() > 0.0
    # Per-pixel uncertainty should be a reasonable fraction of noise/sqrt(F).
    assert sigma.mean() < 1.0e-5


def test_rotation_measure_fit_rejects_shape_mismatch():
    img = _make_synthetic_cube(0.0, 0.0)
    bad_sigma = img.sigma_chi[:, :-1, :]
    bad = PolarimetricImage(
        x=img.x, y=img.y, lambda_sq=img.lambda_sq,
        chi=img.chi, sigma_chi=bad_sigma,
    )
    with pytest.raises(ValueError):
        rotation_measure_fit(bad)


def test_compute_residual_intercept_simple():
    obs = np.array([[1.0, 2.0], [3.0, 4.0]])
    grmhd = np.array([[0.5, 1.0], [1.5, 2.0]])
    res = compute_residual_intercept(obs, grmhd)
    assert res.tolist() == [[0.5, 1.0], [1.5, 2.0]]


def test_compute_residual_intercept_shape_mismatch():
    with pytest.raises(ValueError):
        compute_residual_intercept(np.zeros((4, 4)), np.zeros((4, 5)))


def test_deproject_radial_basic_uniform():
    side = np.linspace(-20.0, 20.0, 64)
    x, y = np.meshgrid(side, side, indexing="xy")
    field = np.full_like(x, 0.42)
    profile = deproject_radial(field, x, y, r_inner=2.0, r_outer=15.0, n_bins=10)
    finite = np.isfinite(profile.values)
    assert finite.any()
    # The profile of a constant field is the constant.
    assert np.allclose(profile.values[finite], 0.42, atol=1e-12)


def test_deproject_radial_inverse_square():
    side = np.linspace(-25.0, 25.0, 200)
    x, y = np.meshgrid(side, side, indexing="xy")
    r = np.hypot(x, y)
    with np.errstate(divide="ignore"):
        field = np.where(r > 0.0, 1.0 / r**2, np.nan)
    profile = deproject_radial(field, x, y, r_inner=3.0, r_outer=20.0, n_bins=12)
    # Recover the slope -2 from a log-log fit.
    valid = np.isfinite(profile.values) & (profile.values > 0)
    coef = np.polyfit(np.log(profile.radii[valid]), np.log(profile.values[valid]), 1)
    assert coef[0] == pytest.approx(-2.0, abs=0.1)
