"""FRB.01 -- no native (non-plasma) dispersion: a consistency / kill test.

TFPT adds no native photon dispersion (a common Lorentz cone). After the plasma
terms are removed, the per-burst arrival time must be

    t(nu) = t0 + K_DM * DM * nu^-2 + A_scat * nu^-4 + drift(nu) + eps,

with NO additional universal frequency-dependent term. This module fits the
plasma model and then tests whether an extra universal term ``A_TFPT * f(nu)`` is
required; ``A_TFPT`` must be consistent with zero. A significant non-plasma
residual would be BAD for TFPT's shared Lorentz cone (hence a kill test, not a
"hit" test).

This requires per-burst time-vs-frequency sub-band arrival data (raw/baseband),
which catalogue-level data do not provide, so with the bundled data it reports
``raw_data_required``. Supply arrays (nu, t, t_err) per burst to activate.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class DispersionResult:
    available: bool
    a_tfpt: float                 # amplitude of the extra universal term
    a_tfpt_err: float
    consistent_with_zero: bool
    note: str


def no_native_dispersion_test(nu_mhz: np.ndarray | None = None,
                              t_s: np.ndarray | None = None,
                              t_err_s: np.ndarray | None = None,
                              extra_index: float = -3.0) -> DispersionResult:
    """Fit t(nu) = t0 + K nu^-2 + A_scat nu^-4 + A_TFPT nu^index and test A_TFPT=0.

    With no sub-band timing supplied, returns ``raw_data_required``.
    """
    if nu_mhz is None or t_s is None:
        return DispersionResult(False, float("nan"), float("nan"), True,
                                "raw_data_required: per-burst sub-band (nu, t) timing "
                                "not available in catalogue data")
    nu = np.asarray(nu_mhz, float)
    t = np.asarray(t_s, float)
    ok = np.isfinite(nu) & np.isfinite(t) & (nu > 0)
    nu, t = nu[ok], t[ok]
    if len(nu) < 6:
        return DispersionResult(False, float("nan"), float("nan"), True, "too few sub-bands")
    w = (1.0 / np.asarray(t_err_s, float)[ok] ** 2) if t_err_s is not None else np.ones_like(t)
    # design: [1, nu^-2, nu^-4, nu^index]
    A = np.vstack([np.ones_like(nu), nu**-2, nu**-4, nu**extra_index]).T
    W = np.diag(w)
    cov = np.linalg.pinv(A.T @ W @ A)
    coef = cov @ (A.T @ (w * t))
    a_tfpt = float(coef[3])
    a_err = float(np.sqrt(max(cov[3, 3], 0.0)))
    consistent = abs(a_tfpt) <= 2 * a_err if a_err > 0 else True
    note = (f"A_TFPT = {a_tfpt:.3e} +/- {a_err:.3e} (nu^{extra_index}); "
            f"{'consistent with 0 (good for shared Lorentz cone)' if consistent else 'NONZERO -> tension'}")
    return DispersionResult(True, a_tfpt, a_err, consistent, note)
