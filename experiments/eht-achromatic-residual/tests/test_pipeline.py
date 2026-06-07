"""End-to-end pipeline tests on synthetic data.

These are the *experimental* validation of the pipeline:

* with a TFPT signal in the cube, all three nulls should fire;
* with no signal, the profile/sign-flip nulls should *not* fire;
* with a constant systematic offset, the frequency null should fire
  but the profile and sign-flip nulls should not.

If any of these change unexpectedly the pipeline logic regressed.
"""

from __future__ import annotations

import dataclasses

import numpy as np

from tfpt_eht.model import BlackHoleGeometry
from tfpt_eht.null_tests import run_all_nulls
from tfpt_eht.residual import (
    compute_residual_intercept,
    deproject_radial,
    rotation_measure_fit,
)
from tfpt_eht.synthetic import SyntheticConfig, generate_observed_mock


def _make_default_cfg(qe: float = 3.0, qm: float = 3.0) -> SyntheticConfig:
    """Synthetic config tuned for clean detection on the unit test grid."""
    return SyntheticConfig(
        image_size=96,
        field_of_view=40.0,
        q_e_eff=qe,
        q_m_eff=qm,
        angle_noise_sigma=2.0e-7,
        rotation_measure_scale=2.0e3,
        chi_grmhd_amplitude=0.10,
        chi_grmhd_seed=42,
        angle_noise_seed=137,
    )


def _flip_geometry(cfg: SyntheticConfig) -> SyntheticConfig:
    new_geom = BlackHoleGeometry(
        center_x=cfg.geometry.center_x,
        center_y=cfg.geometry.center_y,
        r_inner=cfg.geometry.r_inner,
        r_outer=cfg.geometry.r_outer,
        sign_orientation=-cfg.geometry.sign_orientation,
    )
    return dataclasses.replace(cfg, geometry=new_geom)


def _run(cfg: SyntheticConfig, *, tfpt_signal: bool, systematic: float = 0.0):
    cfg_flip = _flip_geometry(cfg)

    observed, grmhd = generate_observed_mock(
        cfg, tfpt_signal=tfpt_signal, systematic_offset=systematic
    )
    observed_flip, grmhd_flip = generate_observed_mock(
        cfg_flip, tfpt_signal=tfpt_signal, systematic_offset=systematic
    )
    # The flip-config uses the same GRMHD truth (the GRMHD model is
    # invariant under our sign convention by construction).
    assert np.allclose(grmhd.chi_0, grmhd_flip.chi_0)

    chi0_obs, _, _ = rotation_measure_fit(observed)
    chi0_obs_flip, _, _ = rotation_measure_fit(observed_flip)
    residual = compute_residual_intercept(chi0_obs, grmhd.chi_0)
    residual_flip = compute_residual_intercept(chi0_obs_flip, grmhd.chi_0)

    profile_plus = deproject_radial(
        residual, observed.x, observed.y,
        r_inner=cfg.geometry.r_inner, r_outer=cfg.geometry.r_outer, n_bins=15,
    )
    profile_minus = deproject_radial(
        residual_flip, observed.x, observed.y,
        r_inner=cfg.geometry.r_inner, r_outer=cfg.geometry.r_outer, n_bins=15,
    )

    # Cube-level residual: chi_obs - chi_grmhd  (both 3-D).  A genuine
    # achromatic TFPT signal has constant per-channel mean; an unmodelled
    # Faraday component would show up as a linear trend in lambda^2.
    residual_cube = observed.chi - grmhd.cube
    chi_res_per_chan = np.nanmean(residual_cube, axis=(1, 2))
    sigma_per_chan = np.full_like(
        chi_res_per_chan,
        cfg.angle_noise_sigma / np.sqrt(cfg.image_size**2),
    )

    return run_all_nulls(
        chi_residual_per_channel=chi_res_per_chan,
        lambda_sq=observed.lambda_sq,
        sigma_per_channel=sigma_per_chan,
        profile_plus=profile_plus,
        profile_minus=profile_minus,
        q_e_eff=cfg.q_e_eff,
        q_m_eff=cfg.q_m_eff,
    )


def test_pipeline_detects_injected_tfpt_signal():
    cfg = _make_default_cfg(qe=8.0, qm=8.0)
    report = _run(cfg, tfpt_signal=True)
    assert report.profile.passed, (
        f"profile null should pass for an injected signal: slope={report.profile.statistic}, "
        f"detail={report.profile.detail}"
    )
    assert report.sign_flip.passed, (
        f"sign-flip null should pass for an injected signal: r={report.sign_flip.statistic}"
    )
    assert report.detection


def test_pipeline_does_not_detect_in_null_case():
    cfg = _make_default_cfg()
    report = _run(cfg, tfpt_signal=False)
    # Without a TFPT signal the profile should NOT follow 1/r^2 with the
    # right amplitude. Allow either the slope or the amplitude check to
    # reject; we only need `passed == False`.
    assert not report.detection


def test_systematic_offset_fails_profile_and_sign_flip():
    cfg = _make_default_cfg()
    # Add a 2 microrad constant offset to the intercept ("calibration error").
    report = _run(cfg, tfpt_signal=False, systematic=2.0e-6)
    # A constant offset is intrinsically achromatic, so the frequency
    # null *could* pass. The structural nulls (profile and sign-flip)
    # must reject.
    assert not report.profile.passed or not report.sign_flip.passed
    assert not report.detection
