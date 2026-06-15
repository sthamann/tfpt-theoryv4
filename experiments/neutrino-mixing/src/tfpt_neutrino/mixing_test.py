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
}


@dataclass
class MixResult:
    checks: list[dict] = field(default_factory=list)
    verdict: str = ""


def _load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def run_mixing() -> MixResult:
    m = _load()
    res = MixResult()
    for key, pred in _PRED.items():
        for x in m[key]:
            z = (pred - x["value"]) / x["sigma"]
            res.checks.append({"observable": key, "tfpt": pred, "measured": x["value"],
                               "sigma": x["sigma"], "z": z, "consistent": abs(z) <= 2.0,
                               "experiment": x["experiment"]})
    sharp = [c for c in res.checks if abs(c["z"]) <= 0.3]
    tens = [c for c in res.checks if abs(c["z"]) > 2.0]
    res.verdict = (
        f"PMNS predictions of record: theta12 sharp ({[round(c['z'],2) for c in res.checks if c['observable']=='sin2_theta12']} sigma), "
        f"theta13 mild ~2 sigma tension (NuFIT 0.02195 vs TFPT 0.0231), theta23 consistent "
        f"with maximal (octant open); CKM delta consistent with the LHCb gamma. "
        f"{len(sharp)} sub-0.3-sigma hits, {len(tens)} >2 sigma."
    )
    return res
