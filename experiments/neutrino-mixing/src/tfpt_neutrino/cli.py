"""``tfpt-neutrino analyze`` -- PMNS angles + CKM delta vs global fits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import constants
from .mixing_test import run_mixing

RESULTS = Path(__file__).resolve().parents[2] / "results"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT neutrino/CKM mixing vs NuFIT/JUNO/LHCb")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)

    print("=" * 72)
    print("TFPT mixing angles of record (from c3/phi0)")
    print("=" * 72)
    for k, v in constants.summary().items():
        print(f"  {k} = {v:.6g}")
    if args.command == "audit":
        return 0

    r = run_mixing()
    print()
    for c in r.checks:
        print(f"  {c['observable']:14s} TFPT={c['tfpt']:.5g} vs {c['measured']:.5g}"
              f"+/-{c['sigma']:.3g} -> {c['z']:+.2f} sigma "
              f"({'ok' if c['consistent'] else 'TENSION'})  {c['experiment']}")
    print("\n  structural CP relation (v231/v233; not a data pull):")
    for s in r.structural:
        print(f"    {s['relation']}  [{'holds' if s['holds'] else 'FAILS'}]  {s['type']}")
    print(f"\n-> {r.verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(
        json.dumps({"constants": constants.summary(), "checks": r.checks,
                    "structural": r.structural, "verdict": r.verdict}, indent=2),
        encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
