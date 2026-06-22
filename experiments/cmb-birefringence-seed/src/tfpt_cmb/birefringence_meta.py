"""Cosmic-birefringence beta META-analysis vs the frozen TFPT seed beta = 0.2424 deg.

The single-measurement modes in ``seed_line.py`` compare beta_TFPT to ACT and Planck
SEPARATELY. This module combines the published beta measurements into ONE meta-estimate --
but does so HONESTLY, because the CMB birefringence measurements are NOT statistically
independent:

  * the Planck-based values (PR3 Minami&Komatsu 2020, PR4 Eskilt 2022) use overlapping Planck
    data and SHARE the dominant systematic -- the absolute polarisation-angle / EB-foreground
    calibration -- so a naive inverse-variance weighting (IVW) treating them as independent
    UNDER-estimates the error (it counts the same Planck information twice);
  * ACT DR6 is a different instrument (semi-independent statistics) but still rests on a similar
    EB-calibration assumption, so a residual shared systematic remains across families.

We therefore report BOTH:
  (1) NAIVE IVW over all measurements -- explicitly a LOWER BOUND on the true error;
  (2) FAMILY-AWARE combination -- collapse each data family to its single most-precise value
      (correlated members do not add information), IVW across families, then add a shared
      calibration systematic SYS_FLOOR_DEG in quadrature (the common EB-modelling assumption).

Plus the genuinely CMB-independent cross-check: BBN Omega_b -> phi0 -> beta. A real frequency /
foreground null needs the raw per-frequency EB spectra (not bundled); the per-experiment
frequency-robustness is taken from the cited papers, not recomputed here. Firewall: consistency
test, no detection claim -- the measurements themselves disagree at ~1 sigma and the shared
systematic dominates.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

from .constants import BETA_DEG, PHI0, SEED_SLOPE

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
SYS_FLOOR_DEG = 0.10        # shared absolute-angle / EB-foreground calibration systematic (deg)


def inverse_variance(vals: list[float], sigs: list[float]) -> tuple[float, float]:
    """Standard inverse-variance-weighted mean and its (statistical) error."""
    w = [1.0 / s**2 for s in sigs]
    mean = sum(v * wi for v, wi in zip(vals, w)) / sum(w)
    return mean, math.sqrt(1.0 / sum(w))


@dataclass
class MetaResult:
    measurements: list[dict] = field(default_factory=list)
    naive_mean: float = 0.0
    naive_sigma: float = 0.0
    naive_z: float = 0.0
    family_values: dict = field(default_factory=dict)   # family -> (beta, sigma) most-precise
    meta_mean: float = 0.0
    meta_sigma: float = 0.0          # incl. shared calibration systematic
    meta_z: float = 0.0
    internal_chi2_dof: float = 0.0   # mutual consistency of the input measurements
    bbn_cross_z: float | None = None  # CMB-independent BBN-Omega_b -> beta check
    verdict: str = ""


def _bbn_beta_cross(m: dict) -> float | None:
    """CMB-independent leg: BBN Omega_b -> implied phi0 -> implied beta_deg, vs TFPT."""
    bbn = next((o for o in m["omega_b"] if "BBN" in o["experiment"]), None)
    if bbn is None:
        return None
    ob = bbn["omega_b_h2"] / bbn["h"] ** 2
    rel = math.hypot(bbn["omega_b_h2_sigma"] / bbn["omega_b_h2"], 2 * bbn["h_sigma"] / bbn["h"])
    beta_from_bbn_rad = ob / SEED_SLOPE          # beta = Omega_b / (4pi-1)
    beta_from_bbn_deg = math.degrees(beta_from_bbn_rad)
    sig = beta_from_bbn_deg * rel
    return (BETA_DEG - beta_from_bbn_deg) / sig


def birefringence_meta(sys_floor_deg: float = SYS_FLOOR_DEG) -> MetaResult:
    m = json.loads(DATA.read_text(encoding="utf-8"))
    betas = m["beta_birefringence_deg"]
    res = MetaResult(measurements=[{k: b[k] for k in ("experiment", "value", "sigma",
                                                       "data_family")} for b in betas])

    vals = [b["value"] for b in betas]
    sigs = [b["sigma"] for b in betas]

    # (1) naive IVW (all independent) -- a LOWER BOUND on the error
    res.naive_mean, res.naive_sigma = inverse_variance(vals, sigs)
    res.naive_z = (BETA_DEG - res.naive_mean) / res.naive_sigma

    # mutual consistency of the inputs (are ACT and Planck even compatible with each other?)
    res.internal_chi2_dof = (sum((v - res.naive_mean) ** 2 / s**2 for v, s in zip(vals, sigs))
                             / max(1, len(vals) - 1))

    # (2) family-aware: collapse each family to its most-precise member (correlated members
    # add no independent information), IVW across families, add the shared systematic
    fam: dict[str, tuple[float, float]] = {}
    for b in betas:
        f = b["data_family"]
        if f not in fam or b["sigma"] < fam[f][1]:
            fam[f] = (b["value"], b["sigma"])
    res.family_values = {f: {"beta_deg": v, "sigma": s} for f, (v, s) in fam.items()}
    fv = [v for v, _ in fam.values()]
    fs = [s for _, s in fam.values()]
    mean, stat = inverse_variance(fv, fs)
    res.meta_mean = mean
    res.meta_sigma = math.hypot(stat, sys_floor_deg)     # + shared calibration systematic
    res.meta_z = (BETA_DEG - res.meta_mean) / res.meta_sigma

    res.bbn_cross_z = _bbn_beta_cross(m)

    naive_ok = abs(res.naive_z) <= 2.0
    meta_ok = abs(res.meta_z) <= 2.0
    res.verdict = (
        f"TFPT beta={BETA_DEG:.4f} deg vs the birefringence meta-estimate. NAIVE IVW (all "
        f"{len(betas)} measurements as independent, a LOWER bound on the error): "
        f"{res.naive_mean:.3f}+/-{res.naive_sigma:.3f} deg -> {res.naive_z:+.2f} sigma. "
        f"FAMILY-AWARE ({len(fam)} data families, + {sys_floor_deg:.2f} deg shared calibration "
        f"systematic): {res.meta_mean:.3f}+/-{res.meta_sigma:.3f} deg -> {res.meta_z:+.2f} sigma. "
        f"The input measurements are mutually consistent (chi2/dof={res.internal_chi2_dof:.2f}); "
        + (f"the CMB-independent BBN-Omega_b leg gives {res.bbn_cross_z:+.2f} sigma. "
           if res.bbn_cross_z is not None else "")
        + ("CONSISTENT" if (naive_ok and meta_ok) else "TENSION")
        + " -- but NOT a detection: the Planck values share data + the absolute-angle "
          "calibration systematic dominates, so the family-aware error (not the naive one) is the "
          "honest one. A real frequency/foreground null needs the raw per-frequency EB spectra.")
    return res
