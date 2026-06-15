"""Injection-recovery harness for the residual pipeline -- the runnable part of the
GRMHD-residual P1 task.

Real M87 imaging (eht-imaging / SMILI + ipole GRMHD library) stays data_limited; what is
runnable *now* is the validation that the residual + three-null machinery CLASSIFIES four
controlled injections correctly:

    injection         expected outcome
    ----------------  --------------------------------------------------------------
    tfpt_1overr2      DETECTION (all 3 nulls pass)               <- the real signal shape
    faraday_lambda2   rejected by the FREQUENCY null (lambda^2 tail)
    dterm_leakage     rejected by the PROFILE + SIGN-FLIP nulls (no 1/r^2, no parity)
    evpa_offset       rejected by the PROFILE + SIGN-FLIP nulls (frequency passes)

A pipeline that mislabels any of these is not trustworthy on real M87 data, so this is the
gate the real reconstruction must pass through once GRMHD images exist.
"""

from __future__ import annotations

import dataclasses

import numpy as np

from tfpt_eht.null_tests import NullTestReport, run_all_nulls
from tfpt_eht.residual import (
    PolarimetricImage,
    compute_residual_intercept,
    deproject_radial,
    rotation_measure_fit,
)
from tfpt_eht.synthetic import SyntheticConfig, generate_observed_mock


def _with_extra(image: PolarimetricImage, extra_chi: np.ndarray) -> PolarimetricImage:
    """Return a copy of ``image`` with ``extra_chi`` (shape (F,H,W) or (H,W)) added."""
    extra = extra_chi if extra_chi.ndim == 3 else extra_chi[None, :, :]
    return PolarimetricImage(x=image.x, y=image.y, lambda_sq=image.lambda_sq,
                             chi=image.chi + extra, sigma_chi=image.sigma_chi)


def _flip_cfg(cfg: SyntheticConfig) -> SyntheticConfig:
    g = cfg.geometry
    return SyntheticConfig(
        image_size=cfg.image_size, q_e_eff=cfg.q_e_eff, q_m_eff=cfg.q_m_eff,
        geometry=g.__class__(center_x=g.center_x, center_y=g.center_y,
                             r_inner=g.r_inner, r_outer=g.r_outer,
                             sign_orientation=-g.sign_orientation))


def _nulls(observed, observed_flip, grmhd, cfg) -> NullTestReport:
    chi0_obs, _, _ = rotation_measure_fit(observed)
    chi0_flip, _, _ = rotation_measure_fit(observed_flip)
    residual = compute_residual_intercept(chi0_obs, grmhd.chi_0)
    residual_flip = compute_residual_intercept(chi0_flip, grmhd.chi_0)
    prof_plus = deproject_radial(residual, observed.x, observed.y,
                                 r_inner=cfg.geometry.r_inner, r_outer=cfg.geometry.r_outer)
    prof_minus = deproject_radial(residual_flip, observed.x, observed.y,
                                  r_inner=cfg.geometry.r_inner, r_outer=cfg.geometry.r_outer)
    residual_cube = observed.chi - grmhd.cube
    chi_res_per_chan = np.nanmean(residual_cube, axis=(1, 2))
    sigma_per_chan = np.full(chi_res_per_chan.shape,
                             cfg.angle_noise_sigma / np.sqrt(cfg.image_size**2), dtype=np.float64)
    return run_all_nulls(chi_residual_per_channel=chi_res_per_chan, lambda_sq=observed.lambda_sq,
                         sigma_per_channel=sigma_per_chan, profile_plus=prof_plus,
                         profile_minus=prof_minus, q_e_eff=cfg.q_e_eff, q_m_eff=cfg.q_m_eff)


def _inject(kind: str, cfg: SyntheticConfig):
    """Build (observed, observed_flip, grmhd) for one injection kind."""
    if kind == "tfpt_1overr2":
        observed, grmhd = generate_observed_mock(cfg, tfpt_signal=True)
        observed_flip, _ = generate_observed_mock(_flip_cfg(cfg), tfpt_signal=True)
        return observed, observed_flip, grmhd

    # all the negative controls start from a GRMHD-only (no TFPT) base
    observed, grmhd = generate_observed_mock(cfg, tfpt_signal=False)
    observed_flip, _ = generate_observed_mock(cfg, tfpt_signal=False)
    x, y = observed.x, observed.y
    r = np.hypot(x - cfg.geometry.center_x, y - cfg.geometry.center_y)
    phi = np.arctan2(y - cfg.geometry.center_y, x - cfg.geometry.center_x)

    if kind == "faraday_lambda2":
        # an extra Faraday screen NOT captured by the GRMHD model -> pure lambda^2 residual.
        # Monopole envelope (nonzero spatial mean) so the per-channel mean carries the slope.
        extra_rm = 6.0e3 * np.exp(-r / 20.0)
        extra = extra_rm[None, :, :] * observed.lambda_sq.reshape(-1, 1, 1)
        observed = _with_extra(observed, extra)
        observed_flip = _with_extra(observed_flip, extra)
    elif kind == "dterm_leakage":
        # D-term leakage: frequency-independent azimuthal dipole, no 1/r^2, no E.B parity
        leak = 3.0e-6 * np.cos(phi) * np.exp(-r / 25.0)
        observed = _with_extra(observed, leak)
        observed_flip = _with_extra(observed_flip, leak)        # same under E.B flip
    elif kind == "evpa_offset":
        # constant EVPA calibration offset: frequency-flat, no profile, no parity
        observed = _with_extra(observed, np.full_like(x, 2.0e-6))
        observed_flip = _with_extra(observed_flip, np.full_like(x, 2.0e-6))
    else:
        raise ValueError(f"unknown injection: {kind}")
    return observed, observed_flip, grmhd


_EXPECT = {
    "tfpt_1overr2": "detection",
    "faraday_lambda2": "reject_frequency",
    "dterm_leakage": "reject_profile_or_sign",
    "evpa_offset": "reject_profile_or_sign",
}


def _classify(rep: NullTestReport) -> str:
    if rep.detection:
        return "detection"
    if not rep.frequency.passed:
        return "reject_frequency"
    return "reject_profile_or_sign"


@dataclasses.dataclass
class InjectionResult:
    kind: str
    expected: str
    observed: str
    correct: bool
    nulls: dict


def run_injection_suite(image_size: int = 96) -> list[InjectionResult]:
    cfg = SyntheticConfig(image_size=image_size)
    out: list[InjectionResult] = []
    for kind, expected in _EXPECT.items():
        observed, observed_flip, grmhd = _inject(kind, cfg)
        rep = _nulls(observed, observed_flip, grmhd, cfg)
        got = _classify(rep)
        out.append(InjectionResult(
            kind=kind, expected=expected, observed=got, correct=bool(got == expected),
            nulls={"frequency": bool(rep.frequency.passed), "profile": bool(rep.profile.passed),
                   "sign_flip": bool(rep.sign_flip.passed)}))
    return out
