"""C_P -- polarisation-angle class test.

``problem_b.txt`` section 4: a Moebius / seam boundary should pin the
polarisation angle to **discrete classes** (e.g. theta0 + k*pi/4) instead of a
continuously rotating field.  Test: PA is defined mod 180 deg; for a candidate
class count ``m`` (spacing 180/m), the quantity ``m*PA`` should be
phase-concentrated (Rayleigh) if the classes are real.

No bundled dataset carries PA, so this returns ``None`` unless a PA array
(degrees) is supplied from a polarisation study.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class PAClassResult:
    n: int
    best_m: int                 # number of angle classes (spacing 180/m deg)
    rayleigh_z: float
    p_value: float
    theta0_deg: float
    c_p: float
    note: str


def pa_angle_classes(pa_deg: np.ndarray, m_values=(2, 4, 6, 8),
                     n_surrogate: int = 2000, seed: int = 0) -> PAClassResult | None:
    pa = np.asarray(pa_deg, dtype=float)
    pa = pa[np.isfinite(pa)]
    n = len(pa)
    if n < 10:
        return None

    rng = np.random.default_rng(seed)
    results = []
    for m in sorted(m_values):
        # PA has period 180 deg, so m classes of spacing 180/m collapse onto one
        # cycle via phase = 2*pi*m*PA/180 = deg2rad(2*m*PA).
        theta = np.deg2rad(2.0 * m * (pa % 180.0))
        c, s = np.cos(theta).mean(), np.sin(theta).mean()
        z = n * (c * c + s * s)
        # surrogate calibration: uniform PA on [0,180)
        null = np.empty(n_surrogate)
        for i in range(n_surrogate):
            th = np.deg2rad(2.0 * m * (rng.uniform(0, 180, n) % 180.0))
            null[i] = n * (np.cos(th).mean() ** 2 + np.sin(th).mean() ** 2)
        p = float((1 + np.sum(null >= z)) / (n_surrogate + 1))
        theta0 = float((np.rad2deg(np.arctan2(s, c)) / (2.0 * m)) % (180.0 / m))
        results.append((m, z, p, theta0))
    # harmonics of the true spacing also concentrate, so the *fundamental* is the
    # smallest significant m; fall back to the max-z m if none is significant.
    significant = [r for r in results if r[2] < 0.05]
    m, z, p, theta0 = (min(significant, key=lambda r: r[0]) if significant
                       else max(results, key=lambda r: r[1]))
    c_p = float(np.clip(1.0 - p / 0.05, 0, 1))
    return PAClassResult(n, m, float(z), p, theta0, c_p,
                         f"{m} PA classes spaced {180 / m:.0f} deg, p={p:.3f}")
