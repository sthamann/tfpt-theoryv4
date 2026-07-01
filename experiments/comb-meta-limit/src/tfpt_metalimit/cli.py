"""`python -m tfpt_metalimit.cli analyze` -- the meta-analytic recovery-comb upper limit.

FIREWALL: search-surface meta-analysis, nothing load-bearing. Reports TWO explicitly separated
limits: the boundary/horizon-scoped one (TFPT-relevant) and the all-channel one (universal-DSI
only). See README.md.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from .channels import HORIZON, all_channels
from .kernel import EPS_PREDICTED, LAMBDA, MIN_COMB_PERIODS, OMEGA
from .metalimit import group_limit
from .selfcheck import run_selfcheck

RESULTS = Path(__file__).resolve().parents[2] / "results" / "results.json"


def _fmt(x: float | None) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "  --  "
    return f"{x:.4f}"


def _usable(records) -> list[dict]:
    return [{"key": r.key, "eps2": r.eps2, "se_power": r.se_power}
            for r in records if r.usable_abs]


def analyze(seed: int = 0, rho: float = 0.3, quick: bool = False) -> dict:
    records = all_channels(seed=seed)
    by_key = {r.key: r for r in records}

    horizon_keys = [r.key for r in records if r.group == HORIZON]
    all_keys = [r.key for r in records]

    usable_all = _usable(records)
    usable_horizon = [u for u in usable_all if by_key[u["key"]].group == HORIZON]

    limit_boundary = group_limit(
        "boundary_horizon_scoped", usable_horizon, horizon_keys, rho=rho,
        note="TFPT-relevant limit: channels where TFPT predicts a universal eps "
             "(GW ringdown + FRB horizon-residual tails). None yields an absolute eps "
             "(single-event bend degeneracy; raw FRB waterfalls absent; linear-intensity "
             "observable) -> data_limited.")
    limit_all = group_limit(
        "all_channel_universal_dsi", usable_all, all_keys, rho=rho,
        note="Universal-DSI bound ONLY (surface+horizon), explicitly NOT a TFPT constraint. "
             "Driven by the surface log-flux channels (A1/A4/A5) that expose an absolute "
             "fractional comb amplitude; the other channels are enumerated but data-limited.")

    selfcheck = run_selfcheck(seed=seed, n_trials=40 if quick else 150)

    result = {
        "experiment": "comb-meta-limit",
        "firewall": ("SEARCH-surface meta-analysis, NOT a claim; nothing [E]. The all-channel "
                     "limit is a universal-DSI statement, NOT TFPT. The boundary/horizon-scoped "
                     "limit is the TFPT-relevant one."),
        "kernel": {
            "lambda": LAMBDA, "omega": OMEGA, "eps_predicted": EPS_PREDICTED,
            "eps_predicted_pct": round(100 * EPS_PREDICTED, 2), "min_comb_periods": MIN_COMB_PERIODS,
        },
        "method": ("Per gated recovery curve, fit y = poly2(ln t) + A cos(omega ln t) + "
                   "B sin(omega ln t); a_hat = sqrt(A^2+B^2). For ln(flux) channels a_hat IS the "
                   "fractional eps. Debias the comb POWER by the mean off-kernel power (red-noise "
                   "aware) -> eps^2 +/- se per source; DerSimonian-Laird random-effects combine "
                   "sources->channel->group with a Hartung-Knapp-Sidik-Jonkman robust SE; 95% "
                   "one-sided UL eps95 = sqrt(max(0, eps^2 + t_{k-1} * se_HKSJ)). Shared-detector "
                   "correlation folded via an SE inflation sqrt(1+(k-1)rho)."),
        "limits": {
            "boundary_horizon_scoped": limit_boundary.as_dict(),
            "all_channel_universal_dsi": limit_all.as_dict(),
        },
        "channels": [r.as_dict() for r in records],
        "self_consistency": selfcheck,
        "seed": seed,
        "rho_shared_detector": rho,
    }
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(result, indent=2), encoding="utf-8")
    _print_summary(result, records)
    return result


def _print_summary(result: dict, records) -> None:
    eps_pred = result["kernel"]["eps_predicted"]
    print("=" * 92)
    print("TFPT comb-meta-limit -- hierarchical 95% UPPER LIMIT on the recovery-comb amplitude eps")
    print("=" * 92)
    print(f"frozen kernel: lambda=(3/2)^6={LAMBDA:.4f}  omega={OMEGA:.4f}  "
          f"eps_predicted=exp(-pi^2/ln lambda)={eps_pred:.5f} (~{100*eps_pred:.1f}%)")
    print("\nPER-CHANNEL comb amplitude at omega=2.583 (Tier A = absolute eps; Tier B = normalised):")
    print(f"  {'ch':5s} {'grp':8s} {'firewall':16s} {'ns/gated':9s} {'eps_hat':>8s} "
          f"{'sigma':>8s} {'eps95':>8s} {'norm_amp':>9s} {'p':>6s}  usable")
    for r in records:
        d = r.as_dict()
        ns = f"{d['n_sources']}/{d['n_gated']}"
        p = d["p_value"]
        print(f"  {d['key']:5s} {d['group']:8s} {d['firewall']:16.16s} {ns:9s} "
              f"{_fmt(d['eps_hat']):>8s} {_fmt(d['sigma_amp']):>8s} {_fmt(d['eps95']):>8s} "
              f"{_fmt(d['norm_amp']):>9s} {(f'{p:.3f}' if p is not None else '  --'):>6s}  "
              f"{'YES' if r.usable_abs else 'no'}")

    for name, lim in result["limits"].items():
        print(f"\n{'-' * 92}\nLIMIT: {name}")
        if lim["k_channels"] == 0:
            print(f"  channels used: NONE (enumerated: {', '.join(lim['channels_enumerated'])})")
            print(f"  -> {lim['verdict'].upper()}: {lim['note']}")
            continue
        print(f"  channels used ({lim['k_channels']}): {', '.join(lim['channels_used'])}")
        print(f"  enumerated:            {', '.join(lim['channels_enumerated'])}")
        print(f"  eps_hat = {lim['eps_hat']:.4f}   sigma = {lim['sigma_amp']:.4f}   "
              f"tau^2 = {lim['tau2']:.2e}   I^2 = {lim['i2']:.2f}   t_crit = {lim['t_crit']:.2f}")
        print(f"  95% UL (HKSJ) = {lim['eps95']:.4f} ({100*lim['eps95']:.2f}%)   "
              f"[rho={lim['rho']} inflated: {lim['eps95_rho']:.4f}]")
        rel = lim["eps95"] / eps_pred
        print(f"  vs eps_predicted {eps_pred:.4f}: UL is {rel:.2f}x the prediction  ->  "
              f"{lim['verdict'].upper()}")

    sc = result["self_consistency"]
    print(f"\n{'-' * 92}\nINJECTION SELF-CONSISTENCY:")
    for k, v in sc["recovery"].items():
        print(f"  inject eps={v['eps_true']:.2f} -> recovered eps_hat={v['eps_hat']:.4f}, "
              f"95% UL={v['eps95']:.4f}  (bracketed: {v['recovered_within_UL']})")
    print(f"  coverage @ eps={sc['coverage_eps']} over {sc['coverage_n_trials']} trials: "
          f"{sc['coverage_95UL']:.3f} (target ~0.95; ok={sc['coverage_ok']})")
    print(f"\nwrote {RESULTS}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tfpt-metalimit", description=__doc__)
    sub = ap.add_subparsers(dest="cmd")
    a = sub.add_parser("analyze", help="run the meta-analytic upper limit")
    a.add_argument("--seed", type=int, default=0)
    a.add_argument("--rho", type=float, default=0.3,
                   help="assumed shared-detector cross-channel correlation for the SE inflation")
    a.add_argument("--quick", action="store_true", help="fewer coverage trials (fast smoke run)")
    ns = ap.parse_args(argv)
    if ns.cmd == "analyze":
        analyze(seed=ns.seed, rho=ns.rho, quick=ns.quick)
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
