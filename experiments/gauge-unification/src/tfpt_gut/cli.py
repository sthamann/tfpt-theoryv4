"""``tfpt-gut analyze`` -- confront sin^2 theta_W = 3/8 (v244/v245) with PDG couplings."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .rge import (
    ALPHA_S,
    ALPHA_EM_INV,
    M_Z,
    SIN2_W_GUT,
    SIN2_W_MEAS,
    analyse,
    run_1loop,
    run_2loop,
)

RESULTS = Path(__file__).resolve().parents[2] / "results"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="sin^2 theta_W = 3/8 spectral-unification test")
    ap.add_argument("command", choices=["analyze", "audit"], nargs="?", default="analyze")
    args = ap.parse_args(argv)

    print("=" * 74)
    print("Gauge unification: sin^2 theta_W = 3/8 (spectral action, v244/v245) vs PDG")
    print("=" * 74)
    print(f"  inputs @ M_Z={M_Z} GeV: alpha_em^-1={ALPHA_EM_INV}, sin^2_W={SIN2_W_MEAS}, "
          f"alpha_s={ALPHA_S};  GUT target sin^2_W(Lambda)=3/8={SIN2_W_GUT}")
    if args.command == "audit":
        return 0

    r = analyse()
    print(f"\n  alpha_i^-1(M_Z) (GUT-norm) = ({r.a_MZ[0]:.2f}, {r.a_MZ[1]:.2f}, {r.a_MZ[2]:.2f})")
    print(f"  1-loop: alpha1=alpha2 at Lambda_12 = {r.Lambda_12_GeV:.2e} GeV, "
          f"alpha_GUT^-1 = {r.a_gut_inv:.2f}")
    print(f"          alpha3^-1 there = {r.a3_inv_at_12:.2f}  ->  unification miss "
          f"{100*r.unify_miss_pct:.1f}% (SM does NOT unify exactly)")

    # 2-loop cross-check of the three couplings at Lambda_12
    a2l = run_2loop(r.a_MZ, r.t_12)
    print(f"  2-loop @ Lambda_12: alpha_i^-1 = ({a2l[0]:.2f}, {a2l[1]:.2f}, {a2l[2]:.2f}) "
          "(gauge-only; 2-loop tightens but still misses without SUSY)")

    print(f"\n  3/8 boundary => predicted sin^2 theta_W(M_Z) = {r.sin2_pred_1loop:.4f}  "
          f"vs measured {r.sin2_meas:.5f}  -> pull {r.pull_sigma:+.0f} sigma")
    print(f"\n==> VERDICT: {r.verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {
        "inputs": {"M_Z": M_Z, "alpha_em_inv": ALPHA_EM_INV, "sin2_W_meas": SIN2_W_MEAS,
                   "alpha_s": ALPHA_S, "sin2_W_GUT": SIN2_W_GUT},
        "alpha_inv_MZ": list(r.a_MZ),
        "Lambda_12_GeV": r.Lambda_12_GeV, "alpha_gut_inv": r.a_gut_inv,
        "alpha3_inv_at_12": r.a3_inv_at_12, "unify_miss_pct": 100 * r.unify_miss_pct,
        "alpha_inv_2loop_at_12": list(a2l),
        "sin2_pred_1loop": r.sin2_pred_1loop, "sin2_meas": r.sin2_meas,
        "pull_sigma": r.pull_sigma, "verdict": r.verdict,
    }
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
