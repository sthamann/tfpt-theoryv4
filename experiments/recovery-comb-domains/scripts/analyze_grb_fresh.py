#!/usr/bin/env python3
"""SINGLE preregistered analysis pass for grb_fresh_restone_v1.

Runs the FROZEN test of hypotheses/grb_fresh_restone_v1.yaml on the fresh
sample in data/grb_fresh/ (fetched by scripts/fetch_grb_fresh.py under the
frozen selection rule) and writes results/grb_fresh_restone.json.

Endpoints (frozen): stacked permutation comb p at the two complex-dimension
tones T1 = 2.749026, T2 = 4.911247; Bonferroni over the 2 endpoints.
Decision: p_global < 0.05 AND both median robustness p < 0.10 -> escalate;
else -> null (candidate killed). Firewall: surface channel; a replication
would still NEVER be a TFPT confirmation.

Run:  cd experiments/recovery-comb-domains && \
      ../tfpt-discovery/.venv/bin/python scripts/analyze_grb_fresh.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "src"))

from tfpt_combdomains.comb import _comb_gain  # noqa: E402
from tfpt_combdomains.grb import read_grb_csv  # noqa: E402
from tfpt_combdomains.quake import _stacked_at  # noqa: E402

DATA_FRESH = ROOT / "data" / "grb_fresh"
RESULTS = ROOT / "results" / "grb_fresh_restone.json"

# frozen endpoints (must match hypotheses/grb_fresh_restone_v1.yaml)
T1, T2 = 2.749026, 4.911247
OMEGA1_REF = 2.582707
PRIMARY_SEED = 20260713
ROBUST_SEEDS = (1, 7, 41, 99, 123)
A = 6 * math.log(1.5)
B = 6 * math.log(3.0)


def _assert_frozen_tones() -> None:
    """Re-derive the two roots from a,b (axioms-only) and guard the YAML values."""
    for target in (T1, T2):
        s = complex(0.1, target)
        for _ in range(80):
            f = 1 - np.exp(-A * s) - np.exp(-B * s)
            fp = A * np.exp(-A * s) + B * np.exp(-B * s)
            step = f / fp
            s -= step
            if abs(step) < 1e-14:
                break
        assert abs(s.imag - target) < 1e-4, \
            f"frozen tone {target} does not match re-derived root {s.imag:.6f}"


def main() -> int:
    print("=" * 84)
    print("PREREGISTERED analysis: grb_fresh_restone_v1 (single pass, frozen 2026-07-13)")
    print("=" * 84)
    _assert_frozen_tones()

    files = sorted(DATA_FRESH.glob("*.csv"))
    curves = []
    for f in files:
        rd = read_grb_csv(f)
        if rd is not None:
            curves.append((rd[0], np.log(rd[1])))
    if not curves:
        print("NO fresh curves in data/grb_fresh/ -- run scripts/fetch_grb_fresh.py first.")
        return 1
    spans = [float(np.log(t.max() / t.min())) for t, _ in curves]
    print(f"fresh sample: {len(curves)} curves, ln-range {min(spans):.1f}..{max(spans):.1f} "
          f"(discovery sample EXCLUDED by construction)")

    out: dict = {"n_curves": len(curves), "endpoints": {}}
    ps = {}
    for name, om in (("T1_res2.749", T1), ("T2_res4.911", T2)):
        r = _stacked_at(curves, om, seed=PRIMARY_SEED)
        rob = [_stacked_at(curves, om, seed=s)["p_value"] for s in ROBUST_SEEDS]
        med = float(np.median(rob))
        ps[name] = r["p_value"]
        out["endpoints"][name] = {"omega": om, **r, "robustness_ps": rob,
                                  "median_robust_p": med}
        print(f"  {name}: n_used={r['n_used']}  primary p={r['p_value']:.4f}  "
              f"robustness p={rob} (median {med:.4f})")

    p_global = min(1.0, 2 * min(ps.values()))
    both_med_ok = all(v["median_robust_p"] < 0.10 for v in out["endpoints"].values())
    replicated = p_global < 0.05 and both_med_ok
    verdict = "escalate_replicated" if replicated else "null"

    # secondary (reported, not endpoints)
    ref = _stacked_at(curves, OMEGA1_REF, seed=PRIMARY_SEED)
    lts = [np.log(t) for t, _ in curves]
    ys = [y for _, y in curves]
    grid = np.linspace(1.6, 6.0, 441)
    spec = np.array([sum(_comb_gain(lt, y, w) for lt, y in zip(lts, ys)) for w in grid])
    g_best = float(grid[int(np.argmax(spec))])
    out.update({
        "p_global_bonferroni2": round(p_global, 4),
        "verdict": verdict,
        "omega1_reference": {"omega": OMEGA1_REF, **ref},
        "free_periodogram_best_omega": round(g_best, 3),
        "free_periodogram_gain_best": round(float(spec.max()), 3),
        "prereg": "hypotheses/grb_fresh_restone_v1.yaml",
    })
    print(f"\n  omega_1 reference: p={ref['p_value']:.4f} (not an endpoint)")
    print(f"  free periodogram global best omega = {g_best:.2f} (control)")
    print(f"\n==> p_global (Bonferroni x2) = {p_global:.4f}; both-median<0.10: {both_med_ok}")
    print(f"==> VERDICT: {verdict.upper()}"
          + (" -- post-hoc candidate NOT replicated on the fresh sample; candidate KILLED."
             if verdict == "null" else
             " -- needs a THIRD independent sample + methods review; surface firewall, "
             "never a TFPT confirmation."))

    RESULTS.parent.mkdir(exist_ok=True)
    RESULTS.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {RESULTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
