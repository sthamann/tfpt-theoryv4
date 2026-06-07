"""Tests for the TFPT prediction model itself."""

from __future__ import annotations

import math

import numpy as np
import pytest

from tfpt_eht.constants import TFPT_COUPLING
from tfpt_eht.model import (
    BlackHoleGeometry,
    beta_bh_profile,
    chi0_tfpt,
    expected_amplitude_at,
)


def test_beta_bh_scales_as_inverse_r_squared():
    r = np.array([5.0, 10.0, 20.0, 40.0])
    beta = beta_bh_profile(r)
    # beta(2r) / beta(r) should equal 1/4 exactly.
    assert np.allclose(beta[1] / beta[0], 0.25, rtol=1e-12)
    assert np.allclose(beta[2] / beta[0], 1.0 / 16.0, rtol=1e-12)
    assert np.allclose(beta[3] / beta[0], 1.0 / 64.0, rtol=1e-12)


def test_beta_bh_amplitude_at_10_rg():
    """Prediction at r=10 r_g with unit weights matches the coupling."""
    expected = TFPT_COUPLING / 100.0
    assert beta_bh_profile(np.array([10.0]))[0] == pytest.approx(expected, rel=1e-15)


def test_beta_bh_zero_at_zero_radius():
    beta = beta_bh_profile(np.array([0.0, 1.0, 10.0]))
    assert beta[0] == 0.0  # no divergence


def test_beta_bh_geometric_weights():
    base = beta_bh_profile(np.array([10.0]))[0]
    doubled = beta_bh_profile(np.array([10.0]), q_e_eff=2.0, q_m_eff=1.0)[0]
    quadrupled = beta_bh_profile(np.array([10.0]), q_e_eff=2.0, q_m_eff=2.0)[0]
    assert doubled == pytest.approx(2.0 * base, rel=1e-15)
    assert quadrupled == pytest.approx(4.0 * base, rel=1e-15)


def test_beta_bh_sign_flips_with_negative_weights():
    pos = beta_bh_profile(np.array([10.0]), q_e_eff=1.0, q_m_eff=1.0)[0]
    neg = beta_bh_profile(np.array([10.0]), q_e_eff=1.0, q_m_eff=-1.0)[0]
    assert pos == pytest.approx(-neg, rel=1e-15)


def test_chi0_tfpt_respects_geometry_mask():
    side = np.linspace(-30.0, 30.0, 64)
    x, y = np.meshgrid(side, side, indexing="xy")
    geom = BlackHoleGeometry(r_inner=4.0, r_outer=20.0)
    chi = chi0_tfpt((x, y), geom)
    r = np.hypot(x, y)
    inside = r < geom.r_inner
    outside = r > geom.r_outer
    assert np.all(chi[inside] == 0.0)
    assert np.all(chi[outside] == 0.0)
    annulus = (r >= geom.r_inner) & (r <= geom.r_outer)
    assert np.any(chi[annulus] > 0.0)


def test_chi0_tfpt_flips_under_sign_orientation():
    side = np.linspace(-30.0, 30.0, 64)
    x, y = np.meshgrid(side, side, indexing="xy")
    g_plus = BlackHoleGeometry(sign_orientation=+1)
    g_minus = BlackHoleGeometry(sign_orientation=-1)
    chi_plus = chi0_tfpt((x, y), g_plus)
    chi_minus = chi0_tfpt((x, y), g_minus)
    finite = np.isfinite(chi_plus)
    assert np.allclose(chi_plus[finite], -chi_minus[finite], atol=1e-20)


def test_expected_amplitude_at_summary():
    out = expected_amplitude_at(10.0)
    assert out["radius_rg"] == 10.0
    assert out["beta_bh_rad"] > 0.0
    assert out["beta_bh_microdeg"] > 0.0
    # cross-check: deg = rad * 180/pi
    assert out["beta_bh_deg"] == pytest.approx(math.degrees(out["beta_bh_rad"]), rel=1e-15)
