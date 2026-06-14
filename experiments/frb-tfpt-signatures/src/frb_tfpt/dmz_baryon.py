"""FRB.05 -- the DM(z) baryon test (the cleanest statistical FRB channel).

The TFPT seed fixes the baryon fraction
    Omega_b = (4 pi - 1) * beta_rad,   beta_rad = phi0 / (4 pi)  ->  Omega_b ~ 0.0489.
The Macquart relation makes localized-FRB cosmic DM a direct probe of Omega_b.
We fit Omega_b from real localized FRBs and ask whether the TFPT value is
consistent with the data.

Honest scope: Omega_b(TFPT) = 0.0489 and Omega_b(Planck) = 0.0493 differ by
<1 %, far below the host-DM scatter of an FRB sample, so this test can *confirm
consistency* but cannot single out TFPT over standard LCDM.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import cosmology as cosmo
from .data_io import DMzTable
from .recovery_kernel import OMEGA_B_TFPT

OMEGA_B_PLANCK = 0.0493


@dataclass
class BaryonResult:
    source: str
    n: int
    omega_b_fit: float
    omega_b_err: float
    omega_b_tfpt: float
    omega_b_planck: float
    tension_tfpt_sigma: float       # |fit - TFPT| / err
    c_baryon: float                 # consistency score in [0,1]
    note: str


def baryon_test(tbl: DMzTable, n_boot: int = 2000, seed: int = 0) -> BaryonResult:
    z = tbl.z
    dmc = tbl.dm_cosmic
    ok = np.isfinite(z) & np.isfinite(dmc) & (dmc > 0) & (z > 0)
    z, dmc = z[ok], dmc[ok]
    n = len(z)
    # heuristic per-point sigma: IGM variance grows with DM, plus host floor
    sigma = np.sqrt((0.2 * dmc) ** 2 + 80.0 ** 2)
    ob, ob_err = cosmo.fit_omega_b(z, dmc, sigma=sigma)

    rng = np.random.default_rng(seed)
    boot = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        boot[i], _ = cosmo.fit_omega_b(z[idx], dmc[idx], sigma=sigma[idx])
    err_stat = float(np.std(boot))
    # The error is *systematics-dominated*: f_IGM is known only to ~5% and the
    # host-DM model to ~10-15%; the formal statistical error badly understates
    # the true uncertainty.  Add a 15% systematic floor (this is also roughly
    # the spread seen between independent localized-FRB samples).
    ob_err = float(np.hypot(err_stat, 0.15 * ob))
    tension = abs(ob - OMEGA_B_TFPT) / ob_err if ob_err > 0 else np.inf
    c_baryon = float(np.exp(-0.5 * tension ** 2))   # 1 when TFPT sits at the fit
    note = (f"Omega_b(FRB) = {ob:.4f} +/- {ob_err:.4f} (syst-dominated; stat {err_stat:.4f}); "
            f"TFPT {OMEGA_B_TFPT:.4f} at {tension:.1f} sigma; "
            f"Planck {OMEGA_B_PLANCK:.4f} at {abs(ob - OMEGA_B_PLANCK) / ob_err:.1f} sigma")
    return BaryonResult(tbl.source, n, float(ob), ob_err, OMEGA_B_TFPT,
                        OMEGA_B_PLANCK, float(tension), c_baryon, note)
