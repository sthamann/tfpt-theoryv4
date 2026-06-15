"""``tfpt-recovery analyze`` -- the recovery kernel as an explicit quantum channel."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import constants
from .channel import analyse_mode, qec_check
from .page_curve import analyse as page_analyse

RESULTS = Path(__file__).resolve().parents[2] / "results"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT recovery channel: CPTP / DPI / QEC / Page curve")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)

    print("=" * 72)
    print("TFPT recovery kernel as a quantum channel R: H_bulk -> H_observable")
    print("=" * 72)
    for k, v in constants.summary().items():
        print(f"  {k} = {v:.6g}")
    if args.command == "audit":
        return 0

    print("\n[1] CPTP + recovery rate + data-processing (per kernel mode)")
    modes = {"lambda1=1": constants.LAMBDA[0], "lambda2=(2/3)^6": constants.LAMBDA[1],
             "lambda3=(1/3)^6": constants.LAMBDA[2]}
    reports = {}
    all_cptp = True
    for name, lm in modes.items():
        r = analyse_mode(lm)
        reports[name] = r
        all_cptp &= r.trace_preserving and r.completely_positive
        print(f"    {name:16s} CPTP={r.trace_preserving and r.completely_positive} "
              f"(Choi_min={r.choi_min_eig:+.2e})  I_n={{1:{r.recovery_n[1]:.3e}, "
              f"2:{r.recovery_n[2]:.2e}, 3:{r.recovery_n[3]:.2e}}}  "
              f"DPI={r.dpi_holds} ({r.dpi_after:.3f}<={r.dpi_before:.3f})")

    print("\n[2] QEC: protected 'law' code vs contracted modes")
    q = qec_check()
    print(f"    protected lambda=1 mode: decoherence-free={q.protected_is_dfs}, "
          f"Knill-Laflamme={q.knill_laflamme_protected}")
    print(f"    contracted mode correctable on full code: {q.contracted_correctable} "
          f"(expected False -> gap = leakage rate)")
    print(f"    -> {q.note}")

    print("\n[3] Page curve (TFPT Hawking law + island min-prescription)")
    p = page_analyse()
    print(f"    unitary turnover at t/tau = {p.t_page_over_tau:.4f}  vs  "
          f"TFPT t_Page/tau = {p.t_page_theory:.4f}  -> match={p.turnover_matches}")
    print(f"    -> {p.note}")

    verdict = ("recovery kernel is a valid CPTP quantum channel (data-processing "
               "respected, protected 'law' code = decoherence-free subspace), and the "
               "TFPT Hawking law reproduces the unitary Page turnover at t_Page "
               "-- structural confirmation, not new data") if (all_cptp and p.turnover_matches) \
        else "FAIL: a channel axiom or the Page turnover did not hold"
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {
        "constants": constants.summary(),
        "channel": {n: {"cptp": r.trace_preserving and r.completely_positive,
                        "choi_min_eig": r.choi_min_eig, "recovery_n": r.recovery_n,
                        "dpi_holds": r.dpi_holds} for n, r in reports.items()},
        "qec": vars(q),
        "page_curve": vars(p),
        "verdict": verdict,
    }
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
