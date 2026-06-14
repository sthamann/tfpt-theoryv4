"""C_RM -- rotation-measure staircase test.

``problem_b.txt`` section 3: a topological transition should make the RM jump in
**discrete steps** (a staircase) rather than drift smoothly.  Test: does a
piecewise-constant (few-level) model of RM(t) beat a smooth polynomial by BIC,
and are the level steps near-constant in ratio?

CHIME/FRB Catalogue 1 and the Aggarwal FRB 20121102A table carry no RM, so with
the bundled data this returns ``None``.  Supply an RM time series (e.g. from a
repeater polarisation paper) to activate the test.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.mixture import GaussianMixture


def _gauss_bic(rss: float, n: int, n_params: int) -> float:
    """BIC of a single Gaussian model (shared variance) with residual sum of
    squares ``rss``, in sklearn's ``GaussianMixture.bic`` convention
    (``-2 logL + n_params log n``) so it is directly comparable to a GMM BIC.
    Lower is better.  ``n_params`` counts the mean/coefficient parameters; the
    variance parameter is added here."""
    rss = max(rss, 1e-30)
    sigma2 = rss / n
    neg2ll = n * (np.log(2 * np.pi) + np.log(sigma2) + 1.0)
    return float(neg2ll + (n_params + 1) * np.log(n))   # +1 for the variance


@dataclass
class RMStepResult:
    n: int
    n_levels: int
    delta_bic_step_vs_smooth: float   # >0 favours the discrete staircase
    level_values: list[float]
    step_ratio_cv: float              # coeff. of variation of successive steps (low => regular)
    c_rm: float
    note: str


def rm_staircase(mjd: np.ndarray, rm: np.ndarray, max_levels: int = 6,
                 seed: int = 0) -> RMStepResult | None:
    t = np.asarray(mjd, dtype=float)
    y = np.asarray(rm, dtype=float)
    ok = np.isfinite(t) & np.isfinite(y)
    t, y = t[ok], y[ok]
    n = len(y)
    if n < 12:
        return None

    yc = y.reshape(-1, 1)
    max_levels = min(max_levels, max(2, n // 4))
    # step model: discrete RM levels via a Gaussian mixture (per-component
    # variance, so it does NOT over-segment a single Gaussian), BIC-selected.
    best_k, best_bic_step, levels = 1, np.inf, np.array([float(np.mean(y))])
    for k in range(1, max_levels + 1):
        gm = GaussianMixture(n_components=k, covariance_type="full",
                             n_init=4, random_state=seed).fit(yc)
        bic_k = gm.bic(yc)
        if bic_k < best_bic_step:
            best_k, best_bic_step, levels = k, float(bic_k), np.sort(gm.means_.ravel())

    # smooth alternative: low-order polynomial in time, SAME BIC convention
    deg = min(3, n - 2)
    resid = y - np.polyval(np.polyfit(t, y, deg), t)
    bic_smooth = _gauss_bic(float(np.sum(resid**2)), n, deg + 1)
    delta = float(bic_smooth - best_bic_step)

    steps = np.diff(levels)
    step_cv = float(np.std(steps) / np.mean(steps)) if len(steps) >= 2 and np.mean(steps) else float("nan")

    s_step = 1.0 / (1.0 + np.exp(-(delta - 6.0) / 3.0)) if best_k > 1 else 0.0
    s_reg = float(np.exp(-(step_cv / 0.3) ** 2)) if np.isfinite(step_cv) else 0.0
    c_rm = float(np.clip(0.6 * s_step + 0.4 * s_step * s_reg, 0, 1))
    return RMStepResult(n, best_k, delta, [float(v) for v in levels],
                        step_cv, c_rm,
                        f"{best_k} RM levels, dBIC(step-smooth)={delta:.1f}")
