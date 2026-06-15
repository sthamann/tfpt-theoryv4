"""The cross-domain seed-line test, in four explicit modes.

TFPT couples ONE seed phi0 to two observables:

    beta_rad = phi0 / (4 pi)        (CMB birefringence)
    Omega_b  = (4 pi - 1) beta_rad  (baryon fraction)

so they lie on the frozen line  Omega_b / beta_rad = 4 pi - 1. Because beta and
Omega_b are NOT guaranteed independent (beta is a polarisation-rotation measurement
with calibration systematics; Omega_b can be CMB-, BBN- or CMB+BAO-bound), the joint
line must NOT be sold as one artificially-sharp detection. We therefore report FOUR
modes:

    beta_only                 -- beta vs ACT/Planck
    omega_b_only              -- Omega_b vs Planck/BBN
    joint_independent         -- the line assuming the two posteriors are independent
    joint_covariance_placeholder -- the same line, flagged that cov(beta, Omega_b)
                                    is NOT modelled, so no combined significance is claimed

A hard UNIT GUARD enforces: beta is always in radians internally; Omega_b is derived
from Omega_b h^2 / h^2 and never confused with Omega_b h^2 (~0.022 vs ~0.049).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

from .constants import BETA_DEG, BETA_RAD, OMEGA_B, PHI0, SEED_SLOPE

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
DEG2RAD = math.pi / 180.0


class UnitError(ValueError):
    """Raised when an Omega_b/Omega_b h^2 or deg/rad confusion is detected."""


def unit_guard(omega_b: float, beta_rad: float) -> None:
    """Fail loudly on the two classic unit slips."""
    if not (0.02 < omega_b < 0.10):
        raise UnitError(f"Omega_b={omega_b:.4f} out of [0.02,0.10] -- likely Omega_b h^2 "
                        f"(~0.022) used as Omega_b (~0.049)")
    if not (1e-4 < abs(beta_rad) < 1e-1):
        raise UnitError(f"beta_rad={beta_rad:.4g} out of range -- likely degrees used as radians")


def _derive_omega_b(entry: dict) -> tuple[float, float]:
    """Omega_b = Omega_b h^2 / h^2 with error propagation (the unit-safe conversion)."""
    obh2, s_obh2 = entry["omega_b_h2"], entry["omega_b_h2_sigma"]
    h, s_h = entry["h"], entry["h_sigma"]
    ob = obh2 / h**2
    rel = math.hypot(s_obh2 / obh2, 2.0 * s_h / h)
    return ob, ob * rel


@dataclass
class Check:
    name: str
    predicted: float
    measured: float
    sigma: float
    z: float
    consistent: bool


@dataclass
class SeedLineResult:
    beta_checks: list[Check] = field(default_factory=list)
    omega_checks: list[Check] = field(default_factory=list)
    modes: dict = field(default_factory=dict)
    verdict: str = ""


def _load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def run_seed_line(beta_primary: str = "ACT", omega_primary: str = "Planck") -> SeedLineResult:
    m = _load()
    res = SeedLineResult()
    unit_guard(OMEGA_B, BETA_RAD)              # guard the prediction itself

    # --- mode: beta_only ---
    for b in m["beta_birefringence_deg"]:
        z = (BETA_DEG - b["value"]) / b["sigma"]
        res.beta_checks.append(Check(b["experiment"], BETA_DEG, b["value"], b["sigma"],
                                     z, abs(z) <= 2.0))
    # --- mode: omega_b_only (derive Omega_b unit-safely) ---
    omega_derived = {}
    for o in m["omega_b"]:
        ob, ob_err = _derive_omega_b(o)
        unit_guard(ob, BETA_RAD)
        omega_derived[o["experiment"]] = (ob, ob_err)
        z = (OMEGA_B - ob) / ob_err
        res.omega_checks.append(Check(o["experiment"], OMEGA_B, ob, ob_err, z, abs(z) <= 2.0))

    res.modes["beta_only"] = {
        "status": "consistent" if all(c.consistent for c in res.beta_checks) else "tension",
        "checks": [vars(c) for c in res.beta_checks]}
    res.modes["omega_b_only"] = {
        "status": "consistent" if all(c.consistent for c in res.omega_checks) else "tension",
        "checks": [vars(c) for c in res.omega_checks]}

    # primary posteriors for the joint line
    bp = next(b for b in m["beta_birefringence_deg"] if beta_primary in b["experiment"])
    beta_meas_rad = bp["value"] * DEG2RAD
    beta_meas_err = bp["sigma"] * DEG2RAD
    unit_guard(OMEGA_B, beta_meas_rad)
    ob, ob_err = omega_derived[next(k for k in omega_derived if omega_primary in k)]

    # --- mode: joint_independent ---
    ratio = ob / beta_meas_rad
    rel = math.hypot(ob_err / ob, beta_meas_err / beta_meas_rad)
    ratio_err = ratio * rel
    line_z = (ratio - SEED_SLOPE) / ratio_err
    # single-seed coherence: invert each posterior to phi0
    phi0_b = beta_meas_rad * (4.0 * math.pi)
    phi0_b_err = beta_meas_err * (4.0 * math.pi)
    phi0_o = ob * (4.0 * math.pi) / SEED_SLOPE
    phi0_o_err = ob_err * (4.0 * math.pi) / SEED_SLOPE
    seed_z = (phi0_b - phi0_o) / math.hypot(phi0_b_err, phi0_o_err)
    res.modes["joint_independent"] = {
        "beta_primary": bp["experiment"], "omega_primary": omega_primary,
        "line_ratio": ratio, "line_ratio_err": ratio_err, "line_z": line_z,
        "phi0_from_beta": phi0_b, "phi0_from_omega": phi0_o, "seed_coherence_z": seed_z,
        "status": "consistent" if abs(line_z) <= 2.0 and abs(seed_z) <= 2.0 else "tension",
        "caveat": "assumes cov(beta, Omega_b) = 0"}

    # --- mode: joint_covariance_placeholder ---
    same_family = ("Planck" in omega_primary)   # ACT beta + Planck Omega_b: both CMB
    res.modes["joint_covariance_placeholder"] = {
        "status": "consistent_no_combined_significance",
        "covariance_modelled": False,
        "note": ("cov(beta, Omega_b) is NOT modelled; "
                 + ("the primary Omega_b is CMB-derived, so a shared-pipeline correlation "
                    "with the ACT beta cannot be excluded -> "
                    if same_family else "")
                 + "no combined significance is claimed. Use BBN Omega_b for a "
                   "genuinely CMB-independent leg.")}

    beta_ok = res.modes["beta_only"]["status"] == "consistent"
    om_ok = res.modes["omega_b_only"]["status"] == "consistent"
    line_ok = res.modes["joint_independent"]["status"] == "consistent"
    if beta_ok and om_ok and line_ok:
        res.verdict = ("consistent with the seed line: one frozen phi0 fits beta and Omega_b "
                       "and the line Omega_b/beta_rad = 4pi-1 holds within errors "
                       "(NOT validated -- beta errors are wide and the joint covariance is "
                       "unmodelled)")
    else:
        res.verdict = "tension in at least one mode -- see per-mode status"
    return res
