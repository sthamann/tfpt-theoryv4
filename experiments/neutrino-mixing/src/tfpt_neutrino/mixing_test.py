"""Confront the TFPT mixing-angle predictions with global fits."""

from __future__ import annotations

import json
import math
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


def _j_pmns() -> tuple[float, float]:
    """Leptonic Jarlskog J_PMNS and J_max from the four TFPT channels (v270)."""
    s12sq, s23sq, s13sq = constants.SIN2_THETA12, constants.SIN2_THETA23, constants.SIN2_THETA13
    s12, s23, s13 = math.sqrt(s12sq), math.sqrt(s23sq), math.sqrt(s13sq)
    c12, c23, c13 = math.sqrt(1 - s12sq), math.sqrt(1 - s23sq), math.sqrt(1 - s13sq)
    delta = math.radians(constants.DELTA_PMNS_DEG)
    j = s12 * c12 * s23 * c23 * s13 * c13**2 * math.sin(delta)
    jmax = s12 * c12 * s23 * c23 * s13 * c13**2
    return j, jmax


@dataclass
class MixResult:
    checks: list[dict] = field(default_factory=list)
    structural: list[dict] = field(default_factory=list)
    j_pmns: float = 0.0
    j_max: float = 0.0
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

    res.j_pmns, res.j_max = _j_pmns()
    j_data_max = 0.0332
    res.structural.append({
        "relation": "J_PMNS derived CP strength (v270)",
        "J_PMNS": round(res.j_pmns, 5),
        "J_max": round(res.j_max, 5),
        "J_max_data": j_data_max,
        "z_J_max": round((res.j_max - j_data_max) / 0.002, 2),
        "holds": res.j_pmns < 0 and abs(res.j_max - j_data_max) < 0.006,
        "type": "[C] derived from angles+delta; falsifiable by sharper delta_CP at DUNE",
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
        f"J_PMNS={res.j_pmns:.5f}, J_max={res.j_max:.5f} vs data ~0.033. "
        f"{len(sharp)} sub-0.3-sigma hits, {len(tens)} >2 sigma."
    )
    return res
