"""TFPT achromatic dyonic residual pipeline.

A reproducible pipeline for the TFPT Paper 3 EHT/ngEHT test of the
structured local astrophysical birefringence amplitude

    beta_BH(r) ~ Q_e_eff(x) * Q_m_eff(x) / (256 * pi**4 * r**2)
              = 16 * c3**4 * Q_e_eff * Q_m_eff / r**2
              = (delta_top / 3) * Q_e_eff * Q_m_eff / r**2

where c3 = 1/(8*pi) and delta_top = 48 * c3**4.

The TFPT coupling 1/(256 * pi**4) is fixed by the same branch data that
fixes the fine-structure constant alpha and the global cosmic-birefringence
amplitude beta_rad. Only the geometric weights Q_e_eff, Q_m_eff and the
emission radius are model dependent.

The pipeline runs three independent null tests on a polarimetric image:

    1. **Frequency null** — the residual intercept must be achromatic
       (no measurable lambda^2 dependence beyond Faraday rotation).
    2. **Profile null** — the residual must follow a 1/r^2 spatial law
       (after GRMHD forward-model subtraction).
    3. **Sign-flip null** — the residual must change sign under reversal
       of the effective E.B orientation.

All three nulls must be passed simultaneously for a positive detection.
"""

from __future__ import annotations

from tfpt_eht.constants import (
    BETA_DEG,
    BETA_RAD,
    C3,
    DELTA_TOP,
    PHI0,
    TFPT_COUPLING,
)
from tfpt_eht.model import (
    BlackHoleGeometry,
    beta_bh_profile,
    chi0_tfpt,
    expected_amplitude_at,
)
from tfpt_eht.null_tests import (
    NullTestReport,
    NullTestResult,
    frequency_null,
    profile_null,
    run_all_nulls,
    sign_flip_null,
)
from tfpt_eht.residual import (
    PolarimetricImage,
    compute_residual_intercept,
    deproject_radial,
    rotation_measure_fit,
)
from tfpt_eht.synthetic import (
    GRMHDModel,
    SyntheticConfig,
    generate_grmhd_mock,
    generate_observed_mock,
)

__all__ = [
    "BETA_DEG",
    "BETA_RAD",
    "BlackHoleGeometry",
    "C3",
    "DELTA_TOP",
    "GRMHDModel",
    "NullTestReport",
    "NullTestResult",
    "PHI0",
    "PolarimetricImage",
    "SyntheticConfig",
    "TFPT_COUPLING",
    "beta_bh_profile",
    "chi0_tfpt",
    "compute_residual_intercept",
    "deproject_radial",
    "expected_amplitude_at",
    "frequency_null",
    "generate_grmhd_mock",
    "generate_observed_mock",
    "profile_null",
    "rotation_measure_fit",
    "run_all_nulls",
    "sign_flip_null",
]

__version__ = "0.1.0"
