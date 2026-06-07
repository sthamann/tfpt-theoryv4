"""The three TFPT null tests for the achromatic residual intercept.

Implements the falsification protocol of TFPT Paper 3 §3 (remark on the
dyonic intercept):

* **Null 1: frequency null.** The residual intercept ``chi_0^res(x)``
  must be achromatic — independent of wavelength after Faraday rotation
  is removed. A real TFPT signal does not depend on lambda^2; a spurious
  miscalibration of the lambda^2 fit usually does.

* **Null 2: profile null.** The residual must follow a ``1/r^2`` radial
  law around the photon-ring barycentre. Any other power-law slope (in
  particular flat residuals from systematics) falsifies the
  determinant-line origin of the amplitude.

* **Null 3: sign-flip null.** Reversing the assumed effective E.B sign
  in the GRMHD forward model must flip the sign of the residual. A
  systematic that does *not* respect this parity will not satisfy the
  third null.

All three must pass simultaneously for a positive TFPT detection. The
test thresholds are exposed as parameters so that the user can vary
them under their declared comparison convention.
"""

from __future__ import annotations

import dataclasses
import math

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from tfpt_eht.constants import TFPT_COUPLING
from tfpt_eht.residual import RadialProfile


@dataclasses.dataclass(frozen=True)
class NullTestResult:
    """Result of a single null test.

    Attributes
    ----------
    name :
        Human-readable name of the test.
    passed :
        Whether the null was rejected at the requested confidence
        (``True`` ⇒ TFPT-compatible; ``False`` ⇒ TFPT-incompatible).
    statistic :
        Test statistic value.
    p_value :
        Two-sided p-value.
    detail :
        Free-form dictionary of secondary diagnostics.
    """

    name: str
    passed: bool
    statistic: float
    p_value: float
    detail: dict[str, float]


@dataclasses.dataclass(frozen=True)
class NullTestReport:
    """Bundle of all three null tests.

    A positive TFPT detection requires ``frequency.passed and
    profile.passed and sign_flip.passed`` simultaneously.
    """

    frequency: NullTestResult
    profile: NullTestResult
    sign_flip: NullTestResult

    @property
    def detection(self) -> bool:
        return (
            self.frequency.passed
            and self.profile.passed
            and self.sign_flip.passed
        )


def frequency_null(
    chi_residual_per_channel: NDArray[np.floating],
    lambda_sq: NDArray[np.floating],
    sigma_per_channel: NDArray[np.floating] | None = None,
    *,
    significance_threshold: float = 3.0,
) -> NullTestResult:
    """Test that the residual intercept is independent of wavelength.

    Fits a linear model ``chi^res = a + b * lambda^2`` to the
    channel-stacked residuals. The TFPT prediction is ``b = 0``; the
    test passes when ``|b| / sigma_b < significance_threshold``.

    Parameters
    ----------
    chi_residual_per_channel :
        Residual intercept per frequency channel (radians), shape ``(F,)``.
        This is the per-channel mean of ``chi_0^res(x)`` after removing
        any residual RM-pollution structure.
    lambda_sq :
        Wavelength-squared per channel (m^2), shape ``(F,)``.
    sigma_per_channel :
        Optional uncertainty per channel. If ``None``, an unweighted fit
        is used and the formal F-statistic against a constant model is
        reported.
    """
    y = np.asarray(chi_residual_per_channel, dtype=np.float64)
    x = np.asarray(lambda_sq, dtype=np.float64)
    if y.shape != x.shape:
        raise ValueError("residuals and lambda_sq must have identical shape")
    if y.size < 3:
        raise ValueError("frequency_null requires at least three channels")

    if sigma_per_channel is None:
        slope, intercept, r_value, p_value, sigma_slope = stats.linregress(x, y)
    else:
        sigma = np.asarray(sigma_per_channel, dtype=np.float64)
        if sigma.shape != y.shape:
            raise ValueError("sigma_per_channel must match residuals shape")
        weights = 1.0 / np.square(sigma)
        sw = np.sum(weights)
        sx = np.sum(weights * x)
        sy = np.sum(weights * y)
        sxx = np.sum(weights * x * x)
        sxy = np.sum(weights * x * y)
        det = sw * sxx - sx**2
        if det == 0.0:
            raise ValueError("singular design matrix in frequency_null")
        slope = (sw * sxy - sx * sy) / det
        intercept = (sxx * sy - sx * sxy) / det
        sigma_slope = math.sqrt(sw / det)
        chi2 = np.sum(weights * (y - intercept - slope * x) ** 2)
        dof = max(y.size - 2, 1)
        p_value = float(1.0 - stats.chi2.cdf(chi2, dof))
        r_value = math.nan

    significance = abs(slope) / sigma_slope if sigma_slope > 0 else math.inf
    passed = significance < significance_threshold

    return NullTestResult(
        name="frequency_null",
        passed=passed,
        statistic=float(slope),
        p_value=float(p_value),
        detail={
            "intercept": float(intercept),
            "slope_significance_sigma": float(significance),
            "threshold_sigma": float(significance_threshold),
            "r_squared": float(r_value**2) if not math.isnan(r_value) else math.nan,
        },
    )


def profile_null(
    profile: RadialProfile,
    *,
    expected_slope: float = -2.0,
    tolerance: float = 0.3,
    coupling: float = TFPT_COUPLING,
    q_e_eff: float = 1.0,
    q_m_eff: float = 1.0,
) -> NullTestResult:
    """Test that the radial residual follows a 1/r^2 profile.

    Fits ``log|residual| = a + b * log(r)`` over the radial bins with
    finite values. The TFPT prediction is ``b = -2`` and the intercept
    ``exp(a) = coupling * Q_e_eff * Q_m_eff`` up to sign. The test
    passes when ``|b - (-2)| < tolerance`` and the fitted amplitude is
    consistent with the TFPT coupling at better than a factor of 3.

    Parameters
    ----------
    profile :
        Radial profile of the residual intercept.
    expected_slope :
        TFPT prediction for the log-log slope. Defaults to ``-2``.
    tolerance :
        Allowed deviation in the fitted slope.
    coupling, q_e_eff, q_m_eff :
        Theoretical amplitude prefactor for the diagnostic ratio.
    """
    r = profile.radii
    v = profile.values
    s = profile.sigma

    valid = np.isfinite(v) & (np.abs(v) > 0.0)
    if valid.sum() < 4:
        return NullTestResult(
            name="profile_null",
            passed=False,
            statistic=math.nan,
            p_value=math.nan,
            detail={"reason": float("nan"), "valid_bins": float(valid.sum())},
        )

    log_r = np.log(r[valid])
    log_abs_v = np.log(np.abs(v[valid]))
    log_sigma = np.where(np.isfinite(s[valid]) & (s[valid] > 0), s[valid] / np.abs(v[valid]), 1.0)

    weights = 1.0 / np.square(log_sigma)
    sw = float(np.sum(weights))
    sx = float(np.sum(weights * log_r))
    sy = float(np.sum(weights * log_abs_v))
    sxx = float(np.sum(weights * log_r * log_r))
    sxy = float(np.sum(weights * log_r * log_abs_v))
    det = sw * sxx - sx**2
    if det == 0.0:
        return NullTestResult(
            name="profile_null",
            passed=False,
            statistic=math.nan,
            p_value=math.nan,
            detail={"reason": float("nan")},
        )
    slope = (sw * sxy - sx * sy) / det
    intercept = (sxx * sy - sx * sxy) / det
    sigma_slope = math.sqrt(sw / det)

    slope_ok = abs(slope - expected_slope) < tolerance
    amplitude_fit = math.exp(intercept)
    amplitude_expected = abs(coupling * q_e_eff * q_m_eff)
    if amplitude_expected > 0:
        amplitude_ratio = amplitude_fit / amplitude_expected
    else:
        amplitude_ratio = math.inf
    amplitude_ok = (1.0 / 3.0) <= amplitude_ratio <= 3.0

    significance = abs(slope - expected_slope) / sigma_slope if sigma_slope > 0 else math.inf
    p_value = float(2.0 * (1.0 - stats.norm.cdf(significance)))

    passed = bool(slope_ok and amplitude_ok)

    return NullTestResult(
        name="profile_null",
        passed=passed,
        statistic=float(slope),
        p_value=p_value,
        detail={
            "intercept_log": float(intercept),
            "amplitude_fit": float(amplitude_fit),
            "amplitude_expected": float(amplitude_expected),
            "amplitude_ratio": float(amplitude_ratio),
            "slope_significance_sigma": float(significance),
            "tolerance": float(tolerance),
            "valid_bins": float(valid.sum()),
        },
    )


def sign_flip_null(
    profile_plus: RadialProfile,
    profile_minus: RadialProfile,
    *,
    threshold_anticorrelation: float = -0.5,
) -> NullTestResult:
    """Test that reversing the effective E.B orientation flips the sign.

    The TFPT prediction is

        chi_0^res(x; E.B reversed) = - chi_0^res(x; E.B nominal).

    Equivalently, the two radial profiles must be strongly
    anti-correlated.  A spurious systematic typically produces the
    *same* profile under E.B reversal and gives a positive correlation.

    Parameters
    ----------
    profile_plus, profile_minus :
        Radial profiles computed under the two opposite sign conventions
        for the effective E.B orientation.
    threshold_anticorrelation :
        Maximum Pearson correlation coefficient compatible with TFPT
        (default ``-0.5``: requires meaningful anti-correlation).
    """
    a = profile_plus.values
    b = profile_minus.values
    if a.shape != b.shape:
        raise ValueError("profiles must have identical radial binning")

    mask = np.isfinite(a) & np.isfinite(b)
    if mask.sum() < 4:
        return NullTestResult(
            name="sign_flip_null",
            passed=False,
            statistic=math.nan,
            p_value=math.nan,
            detail={"valid_bins": float(mask.sum())},
        )

    r, p = stats.pearsonr(a[mask], b[mask])
    passed = bool(r <= threshold_anticorrelation)

    return NullTestResult(
        name="sign_flip_null",
        passed=passed,
        statistic=float(r),
        p_value=float(p),
        detail={
            "threshold": float(threshold_anticorrelation),
            "valid_bins": float(mask.sum()),
        },
    )


def run_all_nulls(
    *,
    chi_residual_per_channel: NDArray[np.floating],
    lambda_sq: NDArray[np.floating],
    sigma_per_channel: NDArray[np.floating] | None,
    profile_plus: RadialProfile,
    profile_minus: RadialProfile,
    significance_threshold: float = 3.0,
    profile_tolerance: float = 0.3,
    q_e_eff: float = 1.0,
    q_m_eff: float = 1.0,
) -> NullTestReport:
    """Run all three null tests and return a combined report."""
    freq = frequency_null(
        chi_residual_per_channel=chi_residual_per_channel,
        lambda_sq=lambda_sq,
        sigma_per_channel=sigma_per_channel,
        significance_threshold=significance_threshold,
    )
    prof = profile_null(
        profile=profile_plus,
        tolerance=profile_tolerance,
        q_e_eff=q_e_eff,
        q_m_eff=q_m_eff,
    )
    sign = sign_flip_null(profile_plus=profile_plus, profile_minus=profile_minus)
    return NullTestReport(frequency=freq, profile=prof, sign_flip=sign)
