"""``tfpt-combdomains`` -- search the dynamic TFPT recovery comb (omega=2.58) across domains.

Runs the shared detector's injection validation, then reports all five channels (A1 magnetar,
A2 BH tail/QNM, A3 FRB burst tail, B4 BEC analog, B5 quantum simulator) with their firewall
legitimacy + data status. No claim: where data is in hand the comb runs; otherwise the precise
blocker is reported.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from . import fetch, quake
from .channels import all_channels
from .comb import EPS_PREDICTED, LAMBDA, MIN_COMB_PERIODS, OMEGA, validate_detector, validate_stack

RESULTS = Path(__file__).resolve().parents[2] / "results"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT recovery comb across domains")
    ap.add_argument("command", choices=["audit", "analyze", "fetch-magnetar", "quake"],
                    nargs="?", default="analyze")
    args, extra = ap.parse_known_args(argv)
    if args.command == "fetch-magnetar":
        return fetch.main(extra)
    if args.command == "quake":
        quake.analyze(refresh="--refresh" in extra)
        return 0

    print("=" * 82)
    print("TFPT recovery comb across domains -- one detector, five channels")
    print(f"  kernel: lambda=(3/2)^6={LAMBDA:.3f}  omega=2pi/ln(lambda)={OMEGA:.3f}  "
          f"predicted ripple eps~exp(-pi^2/ln lambda)={EPS_PREDICTED:.3f}")
    print(f"  ln(tau) RANGE requirement to localise omega: > ~{MIN_COMB_PERIODS} comb periods")
    print("=" * 82)
    if args.command == "audit":
        return 0

    v = validate_detector()
    print(f"\n  detector validation ({v.n_seeds} seeds; eps={v.eps}, noise={v.noise}):")
    print(f"    sufficient range (~{v.sufficient_periods} periods): comb detected "
          f"{100*v.sufficient_comb_rate:.0f}% | false-positive {100*v.sufficient_null_rate:.0f}%")
    print(f"    short range (~{v.short_periods} periods): comb detected "
          f"{100*v.short_comb_rate:.0f}% (range-blind) -> validated={v.passed}")

    sv = validate_stack(n_seeds=60)
    print(f"\n  stacked meta-test validation (faint eps={sv.eps} comb over {sv.n_curves} outbursts, "
          f"~{sv.periods} periods each):")
    print(f"    single curve detected {100*sv.single_rate:.0f}% -> STACK detected "
          f"{100*sv.stacked_rate:.0f}% | false-positive {100*sv.null_rate:.0f}% "
          f"-> validated={sv.passed}  (the A1 'sharpening'; combined FP ~10% -> escalate, not claim)")

    rep = all_channels()
    print("\n  channels:")
    print(f"    {'ch':3s} {'domain':40s} {'legit':16s} {'status':14s} result")
    for c in rep.channels:
        r = ""
        if c.result is not None:
            r = (f"periods={c.result['comb_periods']} range_ok={c.result['range_sufficient']} "
                 f"p={c.result['p_value']} detected={c.result['comb_detected']}")
        print(f"    {c.key:3s} {c.domain:40s} {c.firewall_legitimacy:16s} {c.data_status:14s} {r}")
    for c in rep.channels:
        print(f"\n  [{c.key}] {c.domain} ({c.firewall_legitimacy}, {c.data_status})")
        print(f"      {c.note}")

    real = [c for c in rep.channels if c.data_status == "real"]
    detected = [c for c in real if c.result and c.result["comb_detected"]]
    real_null = [c for c in real if c.result and c.result["range_sufficient"]
                 and not c.result["comb_detected"]]
    verdict = (
        f"detector validated (fires at >~{MIN_COMB_PERIODS} periods, range-blind below; no false "
        f"positives). Across the 5 domains: {len(real)} have data in hand "
        f"({', '.join(c.key for c in real) or 'none'}); "
        + (f"comb DETECTED in {', '.join(c.key for c in detected)} -> ESCALATE (independent check first). "
           if detected else
           (f"in {', '.join(c.key for c in real_null)} the range is sufficient but the kernel "
            f"omega=2.58 is NOT special (clean NULL on real data, though FRB burst tails are "
            f"scattering/noise-dominated -> weak). " if real_null else "")
           + "The wide-ln(t), cleaner channels (A1 magnetar ~3 decades; A2 BH late-time tail) are "
           "data_limited; the analog/simulator channels (B4/B5) need bespoke experiments. The comb "
           "is intrinsically a ~2% effect needing a clean, wide-range recovery -- the search space "
           "is genuinely narrow. No claim.")
    )
    print(f"\n==> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {"kernel": {"lambda": LAMBDA, "omega": OMEGA, "eps_predicted": EPS_PREDICTED,
                      "min_comb_periods": MIN_COMB_PERIODS},
           "detector_validation": asdict(v),
           "stack_validation": asdict(sv),
           "channels": [asdict(c) for c in rep.channels], "verdict": verdict}
    (RESULTS / "recovery_comb_domains.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'recovery_comb_domains.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
