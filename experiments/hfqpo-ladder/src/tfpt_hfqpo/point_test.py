"""HFQPO.H1 — exact-3/2 point test on published pair frequencies.

Per pair: r = nu_u / nu_l, sigma_r by first-order error propagation, pull = (r - 3/2)/sigma_r.
Combined chi^2 over the four preregistered 'consistent' sources (dof = 4). The counterexample
XTE J1859+226 is ALWAYS computed and reported prominently (universality breaker), and Sgr A*
is exploratory only — both are excluded from the combined statistic by preregistration, not
by their values.

A PASS here is explicitly NOT support: the GR 3:2 parametric resonance selects 3:2 on its own
and the H2 selection null clusters ratios near 3/2 without any resonance at all.
"""

from __future__ import annotations

import math
from typing import Any

from tfpt_hfqpo.constants import STEP_F


def ratio_with_sigma(nu_u: float, s_u: float, nu_l: float, s_l: float) -> tuple[float, float]:
    r = nu_u / nu_l
    return r, r * math.sqrt((s_u / nu_u) ** 2 + (s_l / nu_l) ** 2)


def _chi2_sf_dof4(x: float) -> float:
    """Survival function of chi^2 with 4 dof (exact for even dof; no scipy)."""
    return math.exp(-x / 2.0) * (1.0 + x / 2.0)


def run_point_test(sources: list[dict[str, Any]]) -> dict[str, Any]:
    per_source: list[dict[str, Any]] = []
    chi2 = 0.0
    n_combined = 0
    for s in sources:
        r, sig = ratio_with_sigma(s["nu_upper_hz"], s["nu_upper_sigma_hz"],
                                  s["nu_lower_hz"], s["nu_lower_sigma_hz"])
        pull = (r - STEP_F) / sig
        row = {"name": s["name"], "role": s["role"],
               "nu_upper_hz": s["nu_upper_hz"], "nu_lower_hz": s["nu_lower_hz"],
               "ratio": r, "sigma_ratio": sig, "pull_vs_3_2": pull,
               "within_pm_0.05": bool(abs(r - STEP_F) <= 0.05),
               "log_step_exponent": math.log(r) / math.log(STEP_F)}
        per_source.append(row)
        if s["role"] == "consistent":
            chi2 += pull * pull
            n_combined += 1
    assert n_combined == 4, "preregistration fixes the combined statistic to the 4 sources"
    p = _chi2_sf_dof4(chi2)
    breaker = next(r for r in per_source if r["role"] == "counterexample")
    return {
        "id": "HFQPO.H1_exact_3_2_point_test",
        "per_source": per_source,
        "combined": {"sources": n_combined, "chi2": chi2, "dof": 4, "p_value": p,
                     "reading": "3/2 exact NOT rejected across the 4 consistent sources"
                                if p >= 0.01 else "3/2 exact REJECTED (kill condition met)"},
        "counterexample": {
            "name": breaker["name"], "ratio": breaker["ratio"],
            "pull_vs_3_2": breaker["pull_vs_3_2"],
            "note": "genuine published HFQPO pair far from 3:2 AND off the (3/2)^k ladder "
                    f"(log_1.5 ratio = {breaker['log_step_exponent']:.3f}, not an integer): "
                    "3:2 is NOT universal among BH HFQPO pairs",
        },
        "verdict": "consistent" if p >= 0.01 else "tension",
        "honesty": "consistency here is ambiguous BY CONSTRUCTION (coincidence-risk): GR "
                   "parametric resonance also selects exactly 3:2, and H2 shows selection "
                   "alone clusters ratios near 3/2",
    }
