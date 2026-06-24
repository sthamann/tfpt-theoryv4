"""Extended seed line: xi = c3/phi0, BBN shadow legs, joint GLS with firewall."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .constants import C3, PHI0, SEED_SLOPE, XI

SEED_DATA = Path(__file__).resolve().parents[3] / "seed-consistency" / "data" / "measurements.json"

# BBN shadow legs (not in core four-leg fit -- different systematics)
BBN_SHADOW = {
    "Y_p": {"value": 0.2453, "sigma": 0.0017, "reference": "PDG 2024 / Cooke+2018 BBN"},
    "D_H": {"value": 2.547e-5, "sigma": 0.025e-5, "reference": "PDG 2024 BBN"},
    "N_eff": {"value": 3.044, "sigma": 0.016, "reference": "Planck 2018 + BBN"},
}


@dataclass
class SeedLeg:
    name: str
    phi0_implied: float | None
    sigma: float | None
    z_frozen: float | None
    in_core_fit: bool
    note: str


@dataclass
class SeedExtendedResult:
    xi: float
    legs: list[SeedLeg] = field(default_factory=list)
    core_chi2_dof: float | None = None
    verdict: str = ""


def _gls(legs: list[dict]) -> tuple[float, float, float]:
    phi = np.array([lg["phi0"] for lg in legs])
    sig = np.array([lg["sigma"] for lg in legs])
    w = 1.0 / sig**2
    phat = float(np.sum(w * phi) / np.sum(w))
    resid = phi - phat
    chi2 = float(np.sum((resid / sig) ** 2))
    dof = len(legs) - 1
    return phat, chi2 / dof if dof else chi2, chi2


def run_seed_extended() -> SeedExtendedResult:
    res = SeedExtendedResult(xi=XI)
    if not SEED_DATA.exists():
        res.verdict = "data_limited: seed-consistency measurements.json missing"
        return res

    m = json.loads(SEED_DATA.read_text(encoding="utf-8"))
    deg2rad = math.pi / 180.0

    def beta_leg():
        b = m["beta_deg"]
        p = b["value"] * deg2rad * 4 * math.pi
        s = b["sigma"] * deg2rad * 4 * math.pi
        return {"name": "beta", "phi0": p, "sigma": s}

    def omega_leg():
        o = m["omega_b_h2"]
        ob = o["value"] / o["h"] ** 2
        p = ob * 4 * math.pi / SEED_SLOPE
        s = (o["sigma"] / o["h"] ** 2) * 4 * math.pi / SEED_SLOPE
        return {"name": "Omega_b", "phi0": p, "sigma": s}

    def t13_leg():
        exps = m["sin2_theta13_reactor_experiments"]
        used = [e for e in exps if e.get("value")]
        w = [1.0 / e["sigma"] ** 2 for e in used]
        val = sum(wi * e["value"] for wi, e in zip(w, used)) / sum(w)
        sig = 1.0 / math.sqrt(sum(w))
        return {"name": "theta13", "phi0": val * math.exp(5 / 6), "sigma": sig * math.exp(5 / 6)}

    def cab_leg():
        c = m["cabibbo_Vus"]
        v, s = c["value"], c["sigma"]
        disc = 1 - 4 * v**2
        phi = (1 - math.sqrt(disc)) / 2
        sp = (2 * v / math.sqrt(disc)) * s
        return {"name": "Cabibbo", "phi0": phi, "sigma": sp}

    core = [beta_leg(), omega_leg(), t13_leg(), cab_leg()]
    phat, chi2dof, _ = _gls(core)
    res.core_chi2_dof = chi2dof

    for lg in core:
        z = (lg["phi0"] - PHI0) / lg["sigma"]
        res.legs.append(SeedLeg(lg["name"], lg["phi0"], lg["sigma"], z, True, "core four-leg GLS"))

    # xi leg: metrology ratio (not an independent phi0 measurement -- shadow)
    res.legs.append(SeedLeg(
        "xi = c3/phi0", XI, None, None, False,
        f"structural ratio {XI:.4f}; not an extra DOF",
    ))

    # BBN shadows: map to phi0 only through Omega_b (already in core) -- report as consistency
    ob_implied = m["omega_b_h2"]["value"] / m["omega_b_h2"]["h"] ** 2
    phi_bbn = ob_implied * 4 * math.pi / SEED_SLOPE
    z_bbn = (phi_bbn - PHI0) / ((m["omega_b_h2"]["sigma"] / m["omega_b_h2"]["h"] ** 2)
                                 * 4 * math.pi / SEED_SLOPE)
    res.legs.append(SeedLeg(
        "BBN Omega_b (shadow)", phi_bbn, None, z_bbn, False,
        "same information as Omega_b leg; D/H and Y_p do not map to phi0 without [C] bridge",
    ))
    for name, leg in BBN_SHADOW.items():
        res.legs.append(SeedLeg(
            name, None, None, None, False,
            f"BBN {name}={leg['value']}: no primitive phi0 map ([O]); consistency via standard BBN",
        ))

    res.verdict = (
        f"extended seed line: core chi2/dof={chi2dof:.2f} (unchanged); xi=c3/phi0={XI:.4f}; "
        f"BBN Y_p/D/H/N_eff recorded as shadow legs (no extra phi0 DOF). "
        f"Kill unchanged: two families >3 sigma off common phi0."
    )
    return res
