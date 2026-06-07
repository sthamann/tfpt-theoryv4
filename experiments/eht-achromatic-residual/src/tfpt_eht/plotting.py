"""Matplotlib plot helpers for the EHT achromatic-residual pipeline.

Used by the notebooks. Kept deliberately minimal: no styling beyond
matplotlib defaults, no seaborn dependency.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

from tfpt_eht.constants import TFPT_COUPLING

if TYPE_CHECKING:
    from matplotlib.axes import Axes

    from tfpt_eht.residual import RadialProfile


def plot_residual_image(
    residual: NDArray[np.floating],
    x: NDArray[np.floating],
    y: NDArray[np.floating],
    ax: Axes | None = None,
    *,
    vlim: float | None = None,
    title: str = "Residual intercept chi_0^res(x)",
) -> Axes:
    """Render the per-pixel residual intercept map."""
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(5.5, 5.0))
    if vlim is None:
        finite = np.isfinite(residual)
        if finite.any():
            vlim = float(np.nanpercentile(np.abs(residual[finite]), 99))
        else:
            vlim = 1.0
    extent = (
        float(np.min(x)),
        float(np.max(x)),
        float(np.min(y)),
        float(np.max(y)),
    )
    image = ax.imshow(
        residual,
        origin="lower",
        extent=extent,
        cmap="RdBu_r",
        vmin=-vlim,
        vmax=+vlim,
        interpolation="nearest",
    )
    ax.set_xlabel("x  [r_g]")
    ax.set_ylabel("y  [r_g]")
    ax.set_title(title)
    ax.get_figure().colorbar(image, ax=ax, shrink=0.85, label="chi_0^res  [rad]")
    return ax


def plot_radial_profile(
    profile: RadialProfile,
    ax: Axes | None = None,
    *,
    label: str = "TFPT residual",
    show_tfpt_prediction: bool = True,
    q_e_eff: float = 1.0,
    q_m_eff: float = 1.0,
) -> Axes:
    """Plot the radial profile with optional TFPT 1/r^2 overlay."""
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(6.0, 4.5))
    valid = np.isfinite(profile.values)
    ax.errorbar(
        profile.radii[valid],
        profile.values[valid],
        yerr=np.where(np.isfinite(profile.sigma[valid]), profile.sigma[valid], 0.0),
        fmt="o-",
        capsize=2,
        label=label,
    )
    if show_tfpt_prediction:
        r = profile.radii[valid]
        prediction = TFPT_COUPLING * q_e_eff * q_m_eff / r**2
        ax.plot(r, prediction, "k--", alpha=0.6, label="TFPT  ~ 1/r^2")
    ax.set_xlabel("r  [r_g]")
    ax.set_ylabel("chi_0^res(r)  [rad]")
    ax.set_xscale("log")
    ax.set_yscale("symlog", linthresh=1.0e-9)
    ax.axhline(0.0, color="grey", lw=0.5)
    ax.legend()
    ax.set_title("Azimuthally averaged residual intercept")
    return ax


def plot_null_summary(
    report,
    ax: Axes | None = None,
) -> Axes:
    """Bar chart summary of the three nulls."""
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(5.0, 3.0))
    names = ["frequency_null", "profile_null", "sign_flip_null"]
    results = [report.frequency, report.profile, report.sign_flip]
    colors = ["#2ecc71" if r.passed else "#e74c3c" for r in results]
    significances = []
    for r in results:
        s = r.detail.get("slope_significance_sigma", float("nan"))
        if np.isnan(s):
            s = abs(r.statistic)
        significances.append(s)
    ax.barh(names, significances, color=colors)
    ax.set_xlabel("test statistic (sigma or |r|)")
    ax.axvline(3.0, color="grey", linestyle=":", label="3 sigma")
    ax.legend(loc="lower right")
    ax.set_title("TFPT achromatic null tests")
    return ax
