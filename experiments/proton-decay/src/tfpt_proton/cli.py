"""``tfpt-proton analyze`` -- confront the TFPT proton lifetime (v266/v249, branch B) with
Super-Kamiokande + the Hyper-K / DUNE / JUNO reach.

Commands:
  analyze   run the confrontation, print the table, write results/results.json
  audit     kernel-freeze guard: assert the frozen axioms / betas / E8 content have not drifted
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from tfpt_proton import proton, unification
from tfpt_proton.confront import analyze

RESULTS = Path(__file__).resolve().parents[2] / "results"

_VERDICT_TAG = {"consistent": "consistent", "tension": "TENSION",
                "kill": "KILL", "data_limited": "data_limited"}


def _print_table(res: dict) -> None:
    print("scalaron scale M_s = c3^{7/2} * Mbar = %.3e GeV  (c3 = 1/(8 pi), axiom P1)\n"
          % res["meta"]["axioms"]["M_scalaron_GeV"])

    hdr = "%-14s %-6s %-10s %-8s %-8s %-11s %-11s %s"
    print("Two-step scales (E8-allowed content x loop order):")
    print(hdr % ("content", "loop", "M_GUT/GeV", "aG^-1", "M_PS/Ms", "", "", ""))
    for content, loops in res["scales"].items():
        for loop, s in loops.items():
            print(hdr % (content, loop.replace("loop", "L"), "%.2e" % s["M_GUT_GeV"],
                         "%.2f" % s["alpha_gut_inv"], "x%.2f" % s["ratio_to_scalaron"],
                         "", "", ""))

    print("\nConfrontation (tau_p band vs current 90% CL limit; verdict per channel):")
    row = "  [%-12s] %-13s %-3s %-14s tau=%-9s band[%.1e,%.1e] pull=%+.1f dex  vs %s"
    for r in res["confrontation"]:
        print(row % (_VERDICT_TAG[r["verdict"]], r["branch"], r["loop"].replace("loop", "L"),
                     r["channel"], "%.2e" % r["tau_central_yr"], r["tau_lo_yr"], r["tau_hi_yr"],
                     r["pull_dex"], "%s>%.1e" % (r["current_experiment"].split()[0],
                                                 r["current_limit_yr"])))

    print("\nPer-branch summary (golden p->e+pi0 channel):")
    for branch, b in res["branch_summary"].items():
        print("  %-14s 1-loop=%-11s 2-loop=%-11s -> %s"
              % (branch, b["e+pi0_verdict_1loop"], b["e+pi0_verdict_2loop"], b["headline"]))

    print("\n==> VERDICT: " + res["verdict"])


def _audit() -> int:
    """Kernel-freeze guard: the axioms, SM betas and E8-allowed content are frozen."""
    checks: list[tuple[str, bool]] = [
        ("axiom c3 = 1/(8 pi)", math.isclose(unification.C3, 1.0 / (8 * math.pi))),
        ("scalaron M_s = c3^{7/2} Mbar in [2.5e13, 3.5e13] GeV",
         2.5e13 < unification.M_SCALARON < 3.5e13),
        ("E8-allowed content = {minimal_16H, +(15,1,1)_45} (v247: one 45, no 126)",
         set(unification.E8_CONTENTS) == {"minimal_16H", "+(15,1,1)_45"}),
        ("minimal PS betas (b4,b2L,b2R) = (-31/3,-3,-7/3)",
         unification.E8_CONTENTS["minimal_16H"] == (-31 / 3, -3.0, -7 / 3)),
        ("+(15,1,1) PS betas = (-9,-3,-7/3)",
         unification.E8_CONTENTS["+(15,1,1)_45"] == (-9.0, -3.0, -7 / 3)),
        ("hadronic band = O(3)", proton.HAD_BAND == 3.0),
        ("tau benchmark TAU16 = 1e36 yr", proton.TAU16 == 1.0e36),
        ("verdict enum = {consistent, tension, kill, data_limited}",
         set(proton.VERDICTS) == {"consistent", "tension", "kill", "data_limited"}),
    ]
    ok = all(passed for _, passed in checks)
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    print("KERNEL FREEZE: " + ("OK" if ok else "DRIFT DETECTED"))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT proton-decay confrontation (branch B)")
    ap.add_argument("command", choices=["analyze", "audit"], nargs="?", default="analyze")
    args = ap.parse_args(argv)

    print("=" * 78)
    print("TFPT proton decay: carrier-native Pati-Salam -> SO(10) (OPTIONAL UV branch B)")
    print("  firewall: tau_p is a downstream/branch prediction, NEVER a primitive [E]/\\veri{}")
    print("=" * 78)

    if args.command == "audit":
        return _audit()

    res = analyze()
    _print_table(res)

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
