"""CMB primordial log-comb typing (prereg cmb_logcomb_v1.yaml).

Confronts the frozen kernel frequency omega = 2pi/ln((3/2)^6) with the
published Planck log-oscillation search (identical template in ln k) and
machine-checks the typing: reach, band membership, amplitude margin, verdict.
The only natural-data bed where the S14 log-clock is MOTIVATED (inflation
e-folds); the transfer of the comb into P(k) stays a flagged assumption.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
RESULTS = HERE / "results" / "results.json"

LN_LAMBDA = math.log((3.0 / 2.0) ** 6)
OMEGA = 2.0 * math.pi / LN_LAMBDA
EPS_PRED = math.exp(-math.pi ** 2 / LN_LAMBDA)

# published search band and bounds (on record; hypotheses YAML has citations)
PLANCK_LOG10_OMEGA_PRIOR = (0.0, 2.1)          # Planck 2018 X Table 11 (log model)
BOUND_95 = {"planck2018_x": 0.03, "combined_2024plus": 0.029}

K_FULL = (1e-4, 0.2)      # Mpc^-1, l = 2..2500 likelihood window
K_CONSERVATIVE = (0.005, 0.2)  # non-parametric power-law window
REACH_GATE = 2.8


def analyze() -> dict:
    log10_omega = math.log10(OMEGA)
    in_band = PLANCK_LOG10_OMEGA_PRIOR[0] <= log10_omega <= PLANCK_LOG10_OMEGA_PRIOR[1]

    reach_full = math.log(K_FULL[1] / K_FULL[0]) / LN_LAMBDA
    reach_cons = math.log(K_CONSERVATIVE[1] / K_CONSERVATIVE[0]) / LN_LAMBDA

    tightest = min(BOUND_95.values())
    margin = tightest / EPS_PRED

    checks = {
        "omega_inside_planck_prior": in_band,
        "reach_full_periods": round(reach_full, 2),
        "reach_conservative_periods": round(reach_cons, 2),
        "gate_passes_full_window": reach_full >= REACH_GATE,
        "gate_fails_conservative_window": reach_cons < REACH_GATE,
        "predicted_below_bound": EPS_PRED < tightest,
    }

    verdict = "data_limited" if (in_band and EPS_PRED < tightest) else "tension"
    out = {
        "experiment": "cmb-primordial-logcomb",
        "prereg": "hypotheses/cmb_logcomb_v1.yaml",
        "frozen": {"omega": round(OMEGA, 6), "log10_omega": round(log10_omega, 5),
                   "epsilon_pred": round(EPS_PRED, 6)},
        "published_bounds_95": BOUND_95,
        "amplitude_margin_bound_over_pred": round(margin, 2),
        "checks": checks,
        "clock_map": "MOTIVATED (inflation e-folds are a log-clock; the only such natural bed)",
        "transduction_B": "assumed, not derived (comb transfer into P(k) is a flagged bridge)",
        "verdict": verdict,
        "note": ("the frozen omega sits inside the published Planck search band with "
                 "no reported feature; the predicted amplitude 0.0173 lies a factor "
                 f"{margin:.1f} below today's 95% bound -> data_limited with a dated "
                 "decider (CMB-S4-class combined bounds reach it; a future bound "
                 "< 0.017 at omega = 2.583 with no detection kills the bridge reading)"),
    }
    RESULTS.parent.mkdir(exist_ok=True)
    RESULTS.write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2))
