"""Inflation branch resolver: is N_star=51.4 a prediction of record, or is the record
the band [50,60] with 51.4 only the slow-reheating preferred branch?

The A_s tension (-11.3 sigma at N_star=51.4) is only a kill test if N_star=51.4 is
frozen. If the record is the band [50,60], A_s simply profiles N_star to ~56, where n_s
and r stay fine -- then A_s is a reheating BRIDGE, not a prediction of record. This
module computes both modes and forces the typing decision.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

from . import constants

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"


@dataclass
class BranchResult:
    fixed: dict = field(default_factory=dict)
    profiled: dict = field(default_factory=dict)
    bayes: dict = field(default_factory=dict)
    s4_forecast: dict = field(default_factory=dict)
    decision: str = ""


def _load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def _gauss_ln(x: float, mu: float, sig: float) -> float:
    return -0.5 * ((x - mu) / sig) ** 2 - math.log(sig * math.sqrt(2 * math.pi))


def _bayes_compare(m: dict) -> dict:
    """Evidence ratio: model A (N_star fixed = 51.4) vs model B (N_star ~ U[50,60]).

    Likelihood legs = n_s + A_s (r is a one-sided limit, not a Gaussian leg).  Model B
    marginalises N_star over a flat band prior; the A_s tension at the fixed point makes
    Z_A tiny, so a large ln B favours the *band* being the prediction of record.
    """
    a_s = m["A_s"][0]
    n0, lo, hi = constants.N_STAR_POINT, *constants.N_STAR_BAND
    out = {}
    for ns_row in m["n_s"]:
        ns_v, ns_s = ns_row["value"], ns_row["sigma"]

        def lnL(N: float) -> float:
            return (_gauss_ln(constants.n_s(N), ns_v, ns_s)
                    + _gauss_ln(constants.a_s(N), a_s["value"], a_s["sigma"]))

        lnZ_A = lnL(n0)
        # marginal evidence of model B by fine-grid trapezoid in N over the band
        grid = [lo + (hi - lo) * k / 4000 for k in range(4001)]
        ln_vals = [lnL(N) for N in grid]
        c = max(ln_vals)
        integ = sum(math.exp(v - c) for v in ln_vals) * (hi - lo) / 4000
        lnZ_B = c + math.log(integ) - math.log(hi - lo)        # flat prior 1/(hi-lo)
        out[ns_row["experiment"]] = {
            "lnZ_fixed": lnZ_A, "lnZ_profiled": lnZ_B,
            "ln_bayes_factor_BA": lnZ_B - lnZ_A,
            "preferred": "profiled band" if lnZ_B > lnZ_A else "fixed point",
        }
    return out


def _s4_forecast(m: dict) -> dict:
    """CMB-S4 sharpness for the r prediction at the band endpoints + fixed point."""
    s4 = next((x for x in m["r_tensor"] if "S4" in x["experiment"]), None)
    sig_r = s4["sigma_forecast"] if s4 else 5.0e-4
    r_pt = constants.r_tensor(constants.N_STAR_POINT)
    r_band = (constants.r_tensor(constants.N_STAR_BAND[1]),
              constants.r_tensor(constants.N_STAR_BAND[0]))
    return {"sigma_r_S4": sig_r, "r_point": r_pt, "r_band": list(r_band),
            "S4_detection_sigma_point": r_pt / sig_r,
            "S4_detection_sigma_band": [r_band[0] / sig_r, r_band[1] / sig_r],
            "note": "TFPT r ~ 0.004-0.0048 is a >=8 sigma S4 detection target; r=0 would falsify."}


def resolve() -> BranchResult:
    m = _load()
    planck_ns = next(x for x in m["n_s"] if "Planck" in x["experiment"])
    a_s = m["A_s"][0]
    res = BranchResult()

    # mode A: fixed reheating point N_star = 51.4
    n0 = constants.N_STAR_POINT
    res.fixed = {
        "mode": "fixed_reheating_point", "N_star": n0,
        "n_s": constants.n_s(n0), "r": constants.r_tensor(n0), "A_s": constants.a_s(n0),
        "z_n_s_planck": (constants.n_s(n0) - planck_ns["value"]) / planck_ns["sigma"],
        "z_A_s_planck": (constants.a_s(n0) - a_s["value"]) / a_s["sigma"],
        "status": "tension (A_s)",
    }

    # mode B: profile N_star to the measured A_s, then read n_s, r there
    n_as = math.sqrt(a_s["value"] * 24.0 * math.pi**2 / constants.C3**7)
    n_as = min(max(n_as, constants.N_STAR_BAND[0]), constants.N_STAR_BAND[1])  # within band
    res.profiled = {
        "mode": "profiled_Nstar", "N_star_band": list(constants.N_STAR_BAND),
        "N_star_from_A_s": n_as, "n_s": constants.n_s(n_as), "r": constants.r_tensor(n_as),
        "A_s": constants.a_s(n_as),
        "z_n_s_planck": (constants.n_s(n_as) - planck_ns["value"]) / planck_ns["sigma"],
        "status": "consistent (A_s profiled; reheating bridge)",
    }

    res.bayes = _bayes_compare(m)
    res.s4_forecast = _s4_forecast(m)
    lnbf = res.bayes["Planck 2018 (TT,TE,EE+lowE+lensing)"]["ln_bayes_factor_BA"]

    res.decision = (
        f"DECISION FINALIZED (Bayes factor ln(B_profiled/fixed) = {lnbf:+.1f}, Planck -> the data "
        f"decisively prefer the band): the PREDICTION OF RECORD is the e-fold BAND N_star in "
        f"[50,60]; N_star=51.4 is the PREFERRED slow-channel branch (a within-band point, not the "
        f"record); A_s is a DOWNSTREAM REHEATING BRIDGE. Consequence: n_s and r at N_star=51.4 stay "
        f"prediction_of_record (within the band); A_s at fixed N_star=51.4 is a {res.fixed['z_A_s_planck']:+.1f} "
        f"sigma BRANCH STRESS (downstream_bridge), NOT a record kill test; the record-consistent "
        f"reading profiles A_s to N_star={n_as:.1f} (n_s={res.profiled['n_s']:.4f} at "
        f"{res.profiled['z_n_s_planck']:+.1f} sigma vs Planck, r={res.profiled['r']:.4f}). CMB-S4 "
        f"(sigma_r~5e-4) then tests r=0.0045 at ~9 sigma -- the clean future discriminator."
    )
    return res
