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
                              extra_index: float = -3.0,
                              include_drift: bool = False) -> DispersionResult:
    """Fit t(nu) = t0 + K nu^-2 + A_scat nu^-4 [+ D nu] + A_TFPT nu^index, test A_TFPT=0.

    ``include_drift`` adds a linear (nu^+1) intrinsic emission-drift term (the FRB
    "sad trombone"), which is *source/burst-intrinsic* and otherwise leaks into
    A_TFPT. With no sub-band timing supplied, returns ``raw_data_required``.
    """
    if nu_mhz is None or t_s is None:
        return DispersionResult(False, float("nan"), float("nan"), True,
                                "raw_data_required: per-burst sub-band (nu, t) timing "
                                "not available in catalogue data")
    nu = np.asarray(nu_mhz, float)
    t = np.asarray(t_s, float)
    ok = np.isfinite(nu) & np.isfinite(t) & (nu > 0)
    nu, t = nu[ok], t[ok]
    min_n = 6 if include_drift else 5      # n_params (5 or 4) + 1 dof
    if len(nu) < min_n:
        return DispersionResult(False, float("nan"), float("nan"), True, "too few sub-bands")
    if t_err_s is not None:
        te = np.asarray(t_err_s, float)[ok]
        good = te[np.isfinite(te) & (te > 0)]
        floor = float(np.median(good)) if good.size else 1.0      # replace 0/NaN errors
        te = np.where(np.isfinite(te) & (te > 0), te, floor)
        te = np.maximum(te, 1e-6 * floor)                          # guard against inf weights
        w = 1.0 / te ** 2
    else:
        w = np.ones_like(t)
    cols = [np.ones_like(nu), nu**-2, nu**-4]
    if include_drift:
        cols.append(nu)                       # linear intrinsic drift
    cols.append(nu**extra_index)              # the TFPT term (last column)
    A = np.vstack(cols).T
    cov = np.linalg.pinv(A.T @ (w[:, None] * A))
    coef = cov @ (A.T @ (w * t))
    a_tfpt = float(coef[-1])
    a_err = float(np.sqrt(max(cov[-1, -1], 0.0)))
    consistent = abs(a_tfpt) <= 2 * a_err if a_err > 0 else True
    note = (f"A_TFPT = {a_tfpt:.3e} +/- {a_err:.3e} (nu^{extra_index}"
            f"{', +drift' if include_drift else ''}); "
            f"{'consistent with 0' if consistent else 'NONZERO -> burst-specific (intrinsic)'}")
    return DispersionResult(True, a_tfpt, a_err, consistent, note)
