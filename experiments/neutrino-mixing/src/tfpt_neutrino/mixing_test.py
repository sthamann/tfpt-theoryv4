"""Confront the TFPT mixing-angle predictions with global fits."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from . import constants

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"

_PRED = {
    "sin2_theta12": constants.SIN2_THETA12,
    "sin2_theta13": constants.SIN2_THETA13,
    "sin2_theta23": constants.SIN2_THETA23,
    "delta_CKM_deg": constants.DELTA_CKM_DEG,
    "delta_PMNS_deg": constants.DELTA_PMNS_DEG,
}


@dataclass
class MixResult:
    checks: list[dict] = field(default_factory=list)
    structural: list[dict] = field(default_factory=list)
    verdict: str = ""


def _load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def _pull(pred: float, entry: dict) -> tuple[float, float]:
    """Directional pull supporting asymmetric (sigma_plus/sigma_minus) errors.

    Returns (z, sigma_used). For an asymmetric measurement the error on the side
    the prediction lies on is used (the honest one-sided pull)."""
    diff = pred - entry["value"]
    if "sigma" in entry:
        sig = entry["sigma"]
    else:
        sig = entry["sigma_plus"] if diff >= 0.0 else entry["sigma_minus"]
    return diff / sig, sig


def run_mixing() -> MixResult:
    m = _load()
    res = MixResult()
    for key, pred in _PRED.items():
        for x in m[key]:
            z, sig = _pull(pred, x)
            res.checks.append({"observable": key, "tfpt": pred, "measured": x["value"],
                               "sigma": sig, "z": z, "consistent": abs(z) <= 2.0,
                               "experiment": x["experiment"]})

    # structural cross-sector CP relation (v231/v233): both CP phases are ONE hexagonal
    # mu6 CM unit rho=e^{i pi/3}, split by the Z2 sheet (rho^3=-1) -> exact +pi flip.
    # [E] arithmetic / [C] physical bridge; NOT a data pull (the seam deck stays Z/4).
    rel = constants.DELTA_PMNS_DEG - constants.DELTA_CKM_LEAD_DEG
    res.structural.append({
        "relation": "delta_PMNS = delta_CKM,lead + 180 deg  (Z2 sheet flip, rho^4 = -rho)",
        "delta_CKM_lead_deg": constants.DELTA_CKM_LEAD_DEG,
        "delta_PMNS_deg": constants.DELTA_PMNS_DEG,
        "diff_deg": rel, "holds": abs(rel - 180.0) < 1e-9,
        "type": "[E] mu6 arithmetic / [C] physical CP bridge (v220/v225/v231/v233); not a data pull",
    })

    sharp = [c for c in res.checks if abs(c["z"]) <= 0.3]
    tens = [c for c in res.checks if abs(c["z"]) > 2.0]
    z12 = [round(c["z"], 2) for c in res.checks if c["observable"] == "sin2_theta12"]
    zpmns = [round(c["z"], 2) for c in res.checks if c["observable"] == "delta_PMNS_deg"]
    res.verdict = (
        f"PMNS predictions of record: theta12 sharp ({z12} sigma), "
        f"theta13 mild ~2 sigma tension (NuFIT 0.02195 vs TFPT 0.0231), theta23 consistent "
        f"with maximal (octant open); CKM delta consistent with the LHCb gamma. "
        f"delta_PMNS = 240 deg = delta_CKM,lead + 180 (v231/v233 sheet relation) vs "
        f"NuFIT 6.0 {zpmns} sigma -- consistent with the global best fit (CP-violating "
        f"region; weak discriminative power until DUNE/HyperK). "
        f"{len(sharp)} sub-0.3-sigma hits, {len(tens)} >2 sigma."
    )
    return res
