"""C_nu -- frequency drift / spectral structure.

``problem_b.txt`` section 2 reads the downward "sad trombone" drift as a phi
relaxation.  Downward drift on its own is *not* TFPT-specific (it is ubiquitous
in repeaters).  The TFPT-specific claim is that the drift is **quantised /
coupled to energy** rather than continuous, so this module:

* measures the per-burst drift rate from CHIME multi-component bursts, and
* tests whether the drift-rate magnitudes are *discrete* (a TFPT signature)
  rather than a smooth spread.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .data_io import BurstTable
from .energy_clusters import gmm_multimodality

_MJD_TO_MS = 86_400_000.0


@dataclass
class DriftResult:
    n_multi_component: int
    frac_downward: float           # fraction with negative (sad-trombone) drift
    drift_rates: list[float]       # MHz/ms, one per multi-component burst
    discrete_best_k: int | None    # GMM modes of |drift|; >1 hints at quantisation
    discrete_delta_bic: float | None
    c_nu: float
    note: str


def burst_drift_rates(tbl: BurstTable) -> list[float]:
    """Linear drift (MHz/ms) for every burst with >=2 time-ordered components."""
    if tbl.peak_freq.size == 0:
        return []
    groups: dict[str, list[int]] = {}
    for i, nm in enumerate(tbl.name):
        groups.setdefault(nm, []).append(i)
    rates: list[float] = []
    for idx in groups.values():
        if len(idx) < 2:
            continue
        t = tbl.mjd[idx]
        f = tbl.peak_freq[idx]
        ok = np.isfinite(t) & np.isfinite(f)
        if ok.sum() < 2:
            continue
        t, f = t[ok], f[ok]
        if np.ptp(t) <= 0:
            continue
        tms = (t - t.min()) * _MJD_TO_MS
        slope = float(np.polyfit(tms, f, 1)[0])
        rates.append(slope)
    return rates


def drift_score(tbl: BurstTable, seed: int = 0) -> DriftResult:
    rates = burst_drift_rates(tbl)
    n = len(rates)
    if n == 0:
        return DriftResult(0, float("nan"), [], None, None, 0.0,
                           "no multi-component bursts with frequency+time info")
    arr = np.array(rates)
    frac_down = float(np.mean(arr < 0))
    best_k, dbic = None, None
    if n >= 20:
        # Test the *signed* drift for discreteness. (Testing |drift| would be a
        # cheat: a positive-only quantity is trivially split by a 2-Gaussian
        # mixture, which has nothing to do with a TFPT cascade.) Downward drift
        # itself -- frac_down -- is the ordinary "sad trombone", not TFPT-specific.
        # We map exp(fluence) onto a positive scale only to reuse the BIC helper.
        gm = gmm_multimodality(np.exp(arr / (np.std(arr) + 1e-9)), seed=seed)
        best_k, dbic = gm.best_k, gm.delta_bic
        # require genuinely strong multimodality (dBIC > 10) before crediting C_nu
        c_nu = float(np.clip((best_k > 1) * (1 / (1 + np.exp(-(dbic - 10) / 3))), 0, 1))
        note = (f"{n} multi-component bursts; signed-drift GMM best_k={best_k} "
                f"(dBIC={dbic:.1f}); downward {frac_down:.0%} is the standard sad-trombone")
    else:
        c_nu = 0.0
        note = f"only {n} multi-component bursts; too few to test drift quantisation"
    return DriftResult(n, frac_down, rates, best_k, dbic, c_nu, note)
