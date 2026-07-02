"""CONTROL 2 — glass/MCT exponent spread: boundary-less two-step relaxation has no frozen bend.

Mode-coupling theory (MCT) is THE canonical theory of two-step relaxation WITHOUT boundary
structure: a beta plateau followed by alpha decay, in supercooled liquids/colloids. Its whole
exponent structure hangs on one number, the exponent parameter lambda_MCT, through the exact
relations (Goetze):

    lambda = Gamma(1-a)^2 / Gamma(1-2a) = Gamma(1+b)^2 / Gamma(1+2b),
    gamma  = 1/(2a) + 1/(2b)            (alpha-timescale divergence  tau ~ |T-T_c|^-gamma).

Crucially, lambda_MCT is an explicit FUNCTIONAL of the static structure S(q): every glass
former gets its OWN exponents. The measured/derived gamma values across systems span
~2.2-2.9 (data/mct_exponents.json, cited per system).

The TFPT walled-clock bend  ln3/ln(3/2) = 2.7095  sits INSIDE that spread. The sceptic's
question: "is a locked bend ~2.71 just what generic two-step relaxation does?" This control
answers structurally (NO comb run, no detector):

  MCT.01 exponent-relation cross-check: complete every row (lambda <-> a, b, gamma) with the
         exact Gamma-function relations and verify the quoted literature values are
         internally consistent (guards against transcription errors in the data file).
  MCT.02 spread statistic: sample mean/std/range of gamma across systems vs the per-system
         measurement errors; chi^2 of the best single universal value (universality test);
         chi^2 of the specific locked value 2.7095 (frozen-bend test). A frozen universal
         bend would make the inter-system spread ~ measurement error and 2.7095 the shared
         value; system-DEPENDENT exponents reject the locked-bend hypothesis.

The control PASSES if boundary-less two-step relaxation does NOT show a frozen universal
bend: locked-bend hypothesis rejected (>= 3 sigma) and spread >> per-system error. Honest
reporting: any near-coincidence of a single system with 2.7095 is stated (it is a proximity
coincidence, exactly like Landers' lambda ~ 12.1 near (3/2)^6 in the cascade bed).

FIREWALL: glassy relaxation has zero TFPT content; a passing control says only that the
frozen bend is NOT a generic property of two-step relaxation — i.e. the bend hypothesis in
the TFPT channels is falsifiable/informative, not cheap. No TFPT claim; nothing [E].
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parents[2] / "data" / "mct_exponents.json"

BEND_TFPT = math.log(3.0) / math.log(1.5)   # 2.7095, the v124/QT.04 walled-clock bend

_A_MAX = 0.3952                              # a(lambda -> 1/2), upper edge of the a-branch


def lambda_from_a(a: float) -> float:
    """Exponent relation, critical branch: lambda = Gamma(1-a)^2 / Gamma(1-2a)."""
    return math.gamma(1.0 - a) ** 2 / math.gamma(1.0 - 2.0 * a)


def lambda_from_b(b: float) -> float:
    """Exponent relation, von Schweidler branch: lambda = Gamma(1+b)^2 / Gamma(1+2b)."""
    return math.gamma(1.0 + b) ** 2 / math.gamma(1.0 + 2.0 * b)


def _bisect(f, lo: float, hi: float, target: float, *, n: int = 200) -> float:
    """Solve f(x) = target for monotonically decreasing f on [lo, hi]."""
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if f(mid) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def a_from_lambda(lam: float) -> float:
    """Invert the critical branch (monotone decreasing in a on (0, 0.395))."""
    return _bisect(lambda_from_a, 1e-6, _A_MAX, lam)


def b_from_lambda(lam: float) -> float:
    """Invert the von Schweidler branch (monotone decreasing in b on (0, 1))."""
    return _bisect(lambda_from_b, 1e-6, 1.0, lam)


def gamma_from_lambda(lam: float) -> float:
    """gamma = 1/(2a) + 1/(2b) — monotone increasing in lambda, hence invertible."""
    return 0.5 / a_from_lambda(lam) + 0.5 / b_from_lambda(lam)


def lambda_from_gamma(gamma: float) -> float:
    """Invert gamma(lambda) (gamma decreasing as lambda decreases -> bisect on -gamma)."""
    return _bisect(lambda g: -gamma_from_lambda(g), 0.51, 0.999, -gamma)


def load_systems() -> list[dict]:
    """Read the per-system MCT exponent sets (with references)."""
    return json.loads(DATA.read_text(encoding="utf-8"))["systems"]


def complete_row(row: dict) -> dict:
    """MCT.01 — complete one system with the exact exponent relations and cross-check.

    If lambda_MCT is quoted, derive (a, b, gamma) from it and report the deviation of the
    derived gamma from the quoted gamma; if only gamma is quoted, derive lambda (and a, b)
    from gamma. Either way the row ends up fully populated + a consistency delta."""
    lam_q, gam_q = row.get("lambda_mct"), float(row["gamma"])
    lam = float(lam_q) if lam_q is not None else lambda_from_gamma(gam_q)
    a, b = a_from_lambda(lam), b_from_lambda(lam)
    gam_derived = 0.5 / a + 0.5 / b
    return {"system": row["system"], "gamma": gam_q, "gamma_err": float(row["gamma_err"]),
            "lambda_mct": round(lam, 4), "lambda_quoted": lam_q is not None,
            "a": round(a, 4), "b": round(b, 4),
            "gamma_derived_from_lambda": round(gam_derived, 4),
            "consistency_delta_gamma": round(gam_derived - gam_q, 4),
            "pull_from_tfpt_bend": round((gam_q - BEND_TFPT) / float(row["gamma_err"]), 2)}


def _chi2_z(chi2: float, dof: int) -> float:
    """Wilson-Hilferty sigma-equivalent for a chi^2 tail (approximate, labelled as such)."""
    x = (chi2 / dof) ** (1.0 / 3.0)
    return (x - (1.0 - 2.0 / (9.0 * dof))) / math.sqrt(2.0 / (9.0 * dof))


def spread_test(rows: list[dict]) -> dict:
    """MCT.02 — the honest spread statistic across systems.

    Reports: sample mean/std/range of gamma; the median per-system error; the universality
    test (chi^2 of the best single value = inverse-variance weighted mean, dof = n-1); and
    the frozen-bend test (chi^2 of gamma == 2.7095 for all systems, dof = n). Sigma
    equivalents via Wilson-Hilferty (approximate)."""
    g = np.array([r["gamma"] for r in rows])
    e = np.array([r["gamma_err"] for r in rows])
    w = 1.0 / e ** 2
    mean_w = float(np.sum(w * g) / np.sum(w))
    chi2_univ = float(np.sum(w * (g - mean_w) ** 2))
    chi2_bend = float(np.sum(w * (g - BEND_TFPT) ** 2))
    n = len(rows)
    std = float(np.std(g, ddof=1))
    rng = float(g.max() - g.min())
    med_err = float(np.median(e))
    nearest = min(rows, key=lambda r: abs(r["gamma"] - BEND_TFPT))
    return {"n_systems": n,
            "gamma_values": [round(float(x), 4) for x in g],
            "gamma_mean": round(float(np.mean(g)), 4),
            "gamma_std_sample": round(std, 4),
            "gamma_range": [round(float(g.min()), 4), round(float(g.max()), 4)],
            "gamma_range_width": round(rng, 4),
            "median_per_system_err": round(med_err, 4),
            "spread_over_error_std": round(std / med_err, 2),
            "spread_over_error_range": round(rng / med_err, 2),
            "bend_tfpt": round(BEND_TFPT, 4),
            "bend_inside_spread": bool(g.min() <= BEND_TFPT <= g.max()),
            "universality_test": {"weighted_mean": round(mean_w, 4),
                                  "chi2": round(chi2_univ, 2), "dof": n - 1,
                                  "sigma_equiv_wh": round(_chi2_z(chi2_univ, n - 1), 2)},
            "locked_bend_test": {"locked_value": round(BEND_TFPT, 4),
                                 "chi2": round(chi2_bend, 2), "dof": n,
                                 "sigma_equiv_wh": round(_chi2_z(chi2_bend, n), 2)},
            "nearest_system_to_bend": {"system": nearest["system"],
                                       "gamma": nearest["gamma"],
                                       "distance": round(abs(nearest["gamma"] - BEND_TFPT),
                                                         4)}}


def run_mct_control() -> dict:
    """The full CONTROL 2 record: completed rows + spread statistics + pass verdict."""
    rows = [complete_row(r) for r in load_systems()]
    spread = spread_test(rows)
    max_incons = max(abs(r["consistency_delta_gamma"]) for r in rows
                     if r["lambda_quoted"])
    relations_ok = bool(max_incons < 0.35)   # quoted lambda vs quoted gamma per system
    locked_rejected = bool(spread["locked_bend_test"]["sigma_equiv_wh"] >= 3.0)
    spread_exceeds = bool(spread["spread_over_error_range"] >= 3.0)
    return {"kind": "structural_control_no_comb_run",
            "systems": rows,
            "spread": spread,
            "exponent_relations_consistent": relations_ok,
            "max_lambda_vs_gamma_inconsistency": round(max_incons, 4),
            "locked_bend_rejected": locked_rejected,
            "spread_exceeds_error": spread_exceeds,
            "passed": bool(relations_ok and locked_rejected and spread_exceeds)}
