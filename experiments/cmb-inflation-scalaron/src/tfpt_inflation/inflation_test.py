"""Confront the TFPT Starobinsky/scalaron read-offs with CMB data."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

from . import constants

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"


@dataclass
class InflationResult:
    n_s_checks: list[dict] = field(default_factory=list)
    r_checks: list[dict] = field(default_factory=list)
    a_s_check: dict = field(default_factory=dict)
    a_s_preferred_n_star: float = float("nan")
    verdict: str = ""


def _load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def run_inflation() -> InflationResult:
    m = _load()
    res = InflationResult()
    ns = constants.n_s(constants.N_STAR_POINT)
    rr = constants.r_tensor(constants.N_STAR_POINT)
    a_s_pt = constants.a_s(constants.N_STAR_POINT)

    for x in m["n_s"]:
        z = (ns - x["value"]) / x["sigma"]
        res.n_s_checks.append({"experiment": x["experiment"], "measured": x["value"],
                               "sigma": x["sigma"], "tfpt": ns, "z": z,
                               "consistent": abs(z) <= 2.0})

    for x in m["r_tensor"]:
        if "limit_95CL" in x:
            res.r_checks.append({"experiment": x["experiment"], "limit_95CL": x["limit_95CL"],
                                 "tfpt": rr, "below_limit": rr < x["limit_95CL"]})
        elif "sigma_forecast" in x:
            res.r_checks.append({"experiment": x["experiment"], "sigma_forecast": x["sigma_forecast"],
                                 "tfpt": rr, "detection_sigma": rr / x["sigma_forecast"]})

    # A_s: point N_star and the A_s-preferred N_star (sqrt scaling)
    ad = m["A_s"][0]
    z_as = (a_s_pt - ad["value"]) / ad["sigma"]
    res.a_s_check = {"experiment": ad["experiment"], "measured": ad["value"], "sigma": ad["sigma"],
                     "tfpt_point": a_s_pt, "z_point": z_as}
    res.a_s_preferred_n_star = math.sqrt(ad["value"] * 24.0 * math.pi**2 / constants.C3**7)

    ns_planck_ok = any(c["consistent"] for c in res.n_s_checks if "Planck" in c["experiment"])
    r_ok = all(c.get("below_limit", True) for c in res.r_checks if "limit_95CL" in c)
    res.verdict = (
        f"n_s point {ns:.4f}: {'consistent with Planck' if ns_planck_ok else 'tension with Planck'}, "
        f"tension with the DESI-combined value; r point {rr:.4f} {'below' if r_ok else 'ABOVE'} "
        f"BK18 (sharp future falsifier at CMB-S4); A_s point is {z_as:+.1f} sigma -> the measured "
        f"A_s requires faster reheating (N_star ~ {res.a_s_preferred_n_star:.1f}). All [C]: N_star is "
        f"an input, M_scal and R+R^2 are [E]."
    )
    return res
