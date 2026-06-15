"""``tfpt-gw analyze`` -- ringdown echo-ratio forecast on the LVK GWTC catalogue."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import constants
from .echo_forecast import forecast

RESULTS = Path(__file__).resolve().parents[2] / "results"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT GW ringdown echo-ratio forecast")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)

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
