"""``tfpt-gw analyze`` -- ringdown echo-ratio forecast on the LVK GWTC catalogue."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import constants
from .echo_forecast import forecast
from .echo_search import injection_suite

RESULTS = Path(__file__).resolve().parents[2] / "results"


def _run_search() -> int:
    """Stage-1 echo matched-filter + injection-recovery (validated on synthetic strain)."""
    print("=" * 78)
    print("TFPT GW echo Stage-1: matched-filter + injection-recovery (synthetic strain)")
    print("=" * 78)
    suite = injection_suite()
    print(f"  frozen ratio (2/3)^6 = {constants.RATIO:.5f};  TFPT C=3/8 ECO template lag "
          f"~ {suite.template_lag_ms:.2f} ms (gravastar-compactness); lag free (scanned)\n")
    print(f"  {'injection':12s} {'echo SNR':>9} {'lag(ms)':>8} {'q_hat':>8}  "
          f"{'label':16s} {'expected':16s} ok")
    for r in suite.results:
        print(f"  {r.case:12s} {r.echo_snr:9.2f} {r.best_lag_ms:8.2f} {r.q_hat:8.4f}  "
              f"{r.label:16s} {r.expected:16s} {r.correct}")
    print(f"\n  -> {suite.n_correct}/{suite.n_total} correctly classified")
    print(f"\n-> {suite.verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {"stage": "strain_level_test (synthetic injection-recovery)",
           "ratio_(2/3)^6": constants.RATIO, "template_lag_ms": suite.template_lag_ms,
           "n_correct": suite.n_correct, "n_total": suite.n_total,
           "results": [vars(r) for r in suite.results], "verdict": suite.verdict}
    (RESULTS / "echo_search.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'echo_search.json'}")
    return 0 if suite.n_correct == suite.n_total else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT GW ringdown echo-ratio forecast + Stage-1 search")
    ap.add_argument("command", choices=["audit", "analyze", "search"], nargs="?", default="analyze")
    args = ap.parse_args(argv)

    if args.command == "search":
        return _run_search()

    print("=" * 72)
    print(f"TFPT ringdown echo-ratio CENSUS (stage={constants.STAGE}; ratio (2/3)^6, lag free)")
    print("=" * 72)
    for k, v in constants.summary().items():
        print(f"  {k} = {v:.5g}")
    if args.command == "audit":
        return 0

    r = forecast()
    print(f"\nGWTC-5.0: 390 canonical confident events (161 new in O4b); "
          f"local raw rows = {r.n_events} (GW170817 BNS reconciled in event_count_audit.md)")
    print(f"ringdown-capable BBH (Mf>=5 Msun): {r.n_bbh}")
    print("\nloudest ringdown events (echo SNR bounds at the frozen ratio):")
    print(f"  {'event':22s} {'SNR':>6} {'Mf':>6} {'echo_max':>9} {'echo_real':>10}")
    for e in r.top:
        print(f"  {e['name']:22s} {e['snr']:6.1f} {e['mfinal']:6.1f} "
              f"{e['echo_snr_max']:9.2f} {e['echo_snr_real']:10.2f}")
    print(f"\nstacked echo SNR upper bound (conservative f_rd=1):   {r.stacked_echo_snr_max:.1f}")
    print(f"stacked echo SNR upper bound (realistic f_rd=0.3):    {r.stacked_echo_snr_real:.1f}")
    print(f"detection threshold: {constants.DET_THRESHOLD:.0f}")
    print(f"\n-> {r.verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {"constants": constants.summary(), "stage": constants.STAGE,
           "n_canonical": 390, "n_raw_rows": r.n_events, "n_bbh": r.n_bbh, "top": r.top,
           "stacked_echo_snr_max": r.stacked_echo_snr_max,
           "stacked_echo_snr_real": r.stacked_echo_snr_real,
           "detectable_max": r.detectable_max, "detectable_real": r.detectable_real,
           "verdict": r.verdict}
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
