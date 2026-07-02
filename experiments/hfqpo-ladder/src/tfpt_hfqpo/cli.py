"""CLI for the hfqpo-ladder search target.

Commands:
    analyze   run H1 (exact-3/2 point test), H2 (selection null), H3 (ladder census)
              -> results/results.json (deterministic, seed frozen in the YAML)
    audit     print the frozen kernel constants

Run:  PYTHONPATH=src python -m tfpt_hfqpo.cli analyze
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tfpt_hfqpo import constants
from tfpt_hfqpo.ladder import run_ladder
from tfpt_hfqpo.point_test import run_point_test
from tfpt_hfqpo.selection_null import run_selection_null

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "measurements.json"
OUT = ROOT / "results" / "results.json"


def load_sources() -> list[dict[str, Any]]:
    return json.loads(DATA.read_text())["sources"]


def analyze(seed: int) -> dict[str, Any]:
    sources = load_sources()
    h1 = run_point_test(sources)
    h2 = run_selection_null(seed=seed)
    h3 = run_ladder(sources)
    return {
        "experiment": "hfqpo-ladder",
        "version": "v1",
        "prereg": "hypotheses/hfqpo_v1.yaml (frozen 2026-07-02, before the data pass)",
        "kernel": constants.summary(),
        "firewall": "TFPT 3/2 = relaxation-ladder step, NOT a two-oscillator ratio; mapping "
                    "non-canonical; bare 3:2 match = coincidence-risk (GR parametric resonance "
                    "also selects 3:2); only the ladder test discriminates; even a ladder hit "
                    "would be [C]-tier; nothing here is [E]",
        "tests": {"H1": h1, "H2": h2, "H3": h3},
        "overall_verdict": "data_limited",
        "overall_reading": "H1 consistent-but-ambiguous (chi2 p={:.2f} across 4 sources, but "
                           "J1859+226 breaks universality at {:.1f} sigma); H2: anchored "
                           "selection alone manufactures the 4-of-5 cluster in {:.0f}% of "
                           "trials; H3 data_limited: no published x1.5 tooth search — the "
                           "archival RXTE PCA design in the YAML is the decisive next stage"
                           .format(h1["combined"]["p_value"],
                                   h1["counterexample"]["pull_vs_3_2"],
                                   100 * h2["deflator"]["p_anchored_cluster"]),
    }


def main() -> None:
    ap = argparse.ArgumentParser(prog="tfpt-hfqpo")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_an = sub.add_parser("analyze", help="run H1/H2/H3 -> results/results.json")
    p_an.add_argument("--seed", type=int, default=constants.H2_SEED)
    sub.add_parser("audit", help="print frozen kernel constants")
    args = ap.parse_args()

    if args.cmd == "audit":
        for k, v in constants.summary().items():
            print(f"  {k:>24s} = {v}")
        return

    res = analyze(args.seed)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2) + "\n")

    h1, h2, h3 = res["tests"]["H1"], res["tests"]["H2"], res["tests"]["H3"]
    print("hfqpo-ladder v1  (prereg hypotheses/hfqpo_v1.yaml)")
    print("-" * 78)
    print("H1 exact-3/2 point test")
    for r in h1["per_source"]:
        print(f"  {r['name']:>14s} [{r['role']:>14s}]  r = {r['ratio']:.4f} "
              f"+- {r['sigma_ratio']:.4f}   pull vs 3/2 = {r['pull_vs_3_2']:+6.2f}")
    c = h1["combined"]
    print(f"  combined (4 consistent sources): chi2 = {c['chi2']:.3f} (dof 4), "
          f"p = {c['p_value']:.3f}  -> {h1['verdict']}")
    print(f"  counterexample: {h1['counterexample']['name']} at "
          f"{h1['counterexample']['pull_vs_3_2']:+.1f} sigma from 3/2")
    print("H2 selection null (Boutelier/Barret/Torok deflator)")
    for v in h2["variants"]:
        print(f"  {v['variant']:>13s}: P(source near 3/2) = {v['p_source_near_3_2']:.3f}   "
              f"P(>=4 of 5 cluster) = {v['p_cluster_4_of_5']:.4f}")
    print(f"  -> {h2['deflator']['reading'][:96]}...")
    print("H3 ladder discriminator (literature stage)")
    for r in h3["per_source"]:
        print(f"  {r['name']:>14s}: tooth {r['ladder_tooth_hz']:7.1f} Hz vs integer line "
              f"{r['harmonic_line_4nu0_hz']:6.1f} Hz  (published tooth search: "
              f"{'NO' if not r['published_detection_at_tooth'] else 'YES'})")
    print(f"  -> {h3['verdict']}: {h3['stage1_finding'][:96]}...")
    print("-" * 78)
    print(f"OVERALL: {res['overall_verdict']}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
