"""``tfpt-lab analyze`` -- TFPT lab-channel confrontations (g-2, kaons, axion)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import constants
from .tests import run_all

RESULTS = Path(__file__).resolve().parents[2] / "results"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT lab-channel F_transfer residuals")
    ap.add_argument("command", choices=["audit", "analyze", "haloscope"], nargs="?",
                    default="analyze")
    args = ap.parse_args(argv)

    if args.command == "haloscope":
        from .haloscope import run as run_haloscope
        st = run_haloscope()
        print("=" * 72)
        print("TFPT spine axion -- haloscope exclusion overlay")
        print("=" * 72)
        print(f"  m_a = {st['m_a_ueV']:.2f} ueV ({st['freq_GHz']:.2f} GHz), f_a = {st['f_a_GeV']:.3e} GeV")
        print(f"  g_agg(DFSZ) = {st['g_agg_DFSZ']:.3e} GeV^-1 ; g_agg(KSVZ) = {st['g_agg_KSVZ']:.3e} GeV^-1")
        print(f"  covering experiments: {st['covering_experiments']}")
        print(f"  KSVZ excluded: {st['KSVZ_excluded']} ; DFSZ excluded: {st['DFSZ_excluded']}")
        print(f"\n-> {st['verdict']}")
        if st.get("plot"):
            print(f"\nWrote plot {st['plot']}")
        return 0

    print("=" * 72)
    print("TFPT lab-channel confrontations (F_transfer probes; firewall in force)")
    print("=" * 72)
    for k, v in constants.summary().items():
        print(f"  {k} = {v:.6g}")
    if args.command == "audit":
        return 0

    results = run_all()
    for r in results:
        print(f"\n[{r.name}]")
        for ln in r.lines:
            print(ln)

    print("\n" + "=" * 72)
    print("SUMMARY (all [C]; statuses split by baseline/branch, no single ampel)")
    for r in results:
        print(f"  {r.name:16s} -> {r.status}")
    print("=" * 72)

    RESULTS.mkdir(exist_ok=True)
    out = {"constants": constants.summary(),
           "channels": {r.name: {"status": r.status, "claim_type": r.claim_type,
                                 "detail": r.detail} for r in results}}
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
