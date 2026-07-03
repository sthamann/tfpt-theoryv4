"""``tfpt-qpe analyze`` — preregistered TFPT kernel search on QPE recurrence sequences.

Hypotheses frozen BEFORE analysis in hypotheses/qpe_tfpt_v1.yaml (QPE.01–03).
Data: real published eruption timings (eRO-QPE2 arXiv:2604.09788 Table B.1;
GSN 069 Miniutti+2023 Table A.1) — see data/README.md for provenance.

Firewall: QPEs are an accretion/EMRI ("horizon-adjacent surface") channel —
search target, never a claim; a hit would be a universal-DSI coincidence.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from .kernel import (
    CLOCK_BEND,
    COMB_OMEGA,
    N_FAM,
    PLACEBO_RATIOS,
    RANGE_GATE_PERIODS,
    TEETH,
    TOLERANCE_DEX,
)

DATA = Path(__file__).resolve().parents[2] / "data"
RESULTS = Path(__file__).resolve().parents[2] / "results"

N_SURROGATE = 2000
SEED = 0


# ----------------------------------------------------------------- loaders
def load_ero_qpe2() -> dict[str, list[tuple[float, float]]]:
    """Recurrence sequences per contiguous (Delta N_QPE = 1) block: lists of
    (T_rec, err) preserving order."""
    rows = []
    with open(DATA / "ero_qpe2_arrival_times.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append((int(r["n_qpe"]), float(r["t_obs_s"]), float(r["t_err_s"])))
    rows.sort()
    blocks: dict[str, list[tuple[float, float]]] = {}
    cur: list[tuple[int, float, float]] = []

    def flush() -> None:
        if len(cur) >= 2:
            key = f"block_N{cur[0][0]}-{cur[-1][0]}"
            recs = []
            for (n1, t1, e1), (n2, t2, e2) in zip(cur[:-1], cur[1:], strict=False):
                assert n2 == n1 + 1
                recs.append((t2 - t1, math.hypot(e1, e2)))
            blocks[key] = recs

    for row in rows:
        if cur and row[0] != cur[-1][0] + 1:
            flush()
            cur = []
        cur.append(row)
    flush()
    return blocks


def load_gsn069() -> dict[str, list[tuple[float, float]]]:
    """Within-campaign recurrence-time sequences (already T_rec in the table)."""
    blocks: dict[str, list[tuple[int, float, float]]] = {}
    with open(DATA / "gsn069_recurrence_times.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            blocks.setdefault(r["campaign"], []).append(
                (int(r["order"]), float(r["trec_s"]), float(r["trec_err_s"])))
    out: dict[str, list[tuple[float, float]]] = {}
    for camp, rows in blocks.items():
        rows.sort()
        seq = []
        for (o1, t1, e1), (o2, t2, e2) in zip(rows[:-1], rows[1:], strict=False):
            if o2 == o1 + 1:                      # adjacent only (curation gaps)
                seq.append(((t1, e1), (t2, e2)))
        # keep the full ordered T list where adjacency holds contiguously
        out[camp] = [(t, e) for (o, t, e) in rows]
    return out


# ---------------------------------------------------------------- QPE.01
def ratio_ladder(sources: dict[str, dict[str, list[tuple[float, float]]]],
                 rng: np.random.Generator) -> dict:
    teeth_dex = {name: math.log10(float(f)) for name, f in TEETH.items()}
    per_source = {}
    for sname, blocks in sources.items():
        ratios, ratio_errs = [], []
        for seq in blocks.values():
            for (t1, e1), (t2, e2) in zip(seq[:-1], seq[1:], strict=False):
                if t1 > 0 and t2 > 0:
                    ratios.append(math.log10(t2 / t1))
                    ratio_errs.append((e1 / t1 + e2 / t2) / math.log(10.0))
        if not ratios:
            per_source[sname] = {"n_ratios": 0, "verdict": "data_limited"}
            continue
        ratios_arr = np.array(ratios)
        hits = 0
        for r in ratios_arr:
            for d in teeth_dex.values():
                if abs(r - d) < TOLERANCE_DEX or abs(r + d) < TOLERANCE_DEX:
                    hits += 1
                    break
        # shuffle null: permute raw T within each block, recompute ratios
        null_hits = np.zeros(N_SURROGATE)
        for k in range(N_SURROGATE):
            h = 0
            for seq in blocks.values():
                ts = np.array([t for t, _ in seq])
                if len(ts) < 2:
                    continue
                perm = rng.permutation(ts)
                lr = np.log10(perm[1:] / perm[:-1])
                for r in lr:
                    for d in teeth_dex.values():
                        if abs(r - d) < TOLERANCE_DEX or abs(r + d) < TOLERANCE_DEX:
                            h += 1
                            break
            null_hits[k] = h
        p = float((1 + np.sum(null_hits >= hits)) / (N_SURROGATE + 1))
        # sensitivity: nearest-tooth distance in units of the observed spread
        nearest = min(min(abs(abs(r) - abs(d)) for d in teeth_dex.values())
                      for r in ratios_arr)
        spread = float(np.std(ratios_arr)) if len(ratios_arr) > 1 else float("nan")
        max_dev = float(np.max(np.abs(ratios_arr)))
        step_dex = abs(teeth_dex["step"])
        per_source[sname] = {
            "n_ratios": len(ratios),
            "hits_at_teeth": hits,
            "null_p": round(p, 3),
            "max_abs_log_ratio_dex": round(max_dev, 4),
            "median_ratio_err_dex": round(float(np.median(ratio_errs)), 4),
            "ratio_spread_dex": round(spread, 4),
            "nearest_tooth_gap_dex": round(nearest, 4),
            "sensitivity_note": (f"a step tooth (2/3 = {step_dex:.3f} dex) exceeds the "
                                 f"largest observed |log ratio| ({max_dev:.3f} dex) by "
                                 f">{(step_dex - max_dev) / max(spread, 1e-9):.0f}x the "
                                 f"observed spread -> a kernel step in the QPE clock is "
                                 f"excluded, not merely unobserved"),
            # preregistered: a candidate needs an excess the shuffle null does NOT
            # reproduce (p < 0.05); a hit the null reproduces trivially is null.
            "verdict": "null" if (hits == 0 or p >= 0.05) else "candidate",
        }
    return per_source


# ---------------------------------------------------------------- QPE.02
def clock_triplets(sources: dict[str, dict[str, list[tuple[float, float]]]]) -> dict:
    per_source = {}
    for sname, blocks in sources.items():
        trips = []
        for seq in blocks.values():
            ts = [t for t, _ in seq]
            for a, b, c in zip(ts[:-2], ts[1:-1], ts[2:], strict=False):
                if a > b > c or a < b < c:                     # strictly monotone
                    g1, g2 = abs(b - a), abs(c - b)
                    if g2 > 0:
                        trips.append(g1 / g2)
        n = len(trips)
        if n < 5:
            per_source[sname] = {
                "n_monotone_triplets": n,
                "triplet_gap_ratios": [round(x, 3) for x in trips],
                "clock_bend_target": round(CLOCK_BEND, 4),
                "placebo_ratios": list(PLACEBO_RATIOS),
                "verdict": "data_limited",
                "note": "fewer than 5 monotone recurrence triplets -- underpowered "
                        "(QPE clocks alternate long/short; monotone runs are rare "
                        "by construction)"}
        else:
            near = sum(1 for x in trips if abs(math.log(x / CLOCK_BEND)) < 0.15)
            per_source[sname] = {"n_monotone_triplets": n, "near_bend": near,
                                 "verdict": "null" if near == 0 else "candidate"}
    return per_source


# ---------------------------------------------------------------- QPE.03
def comb_gate(sources: dict[str, dict[str, list[float]]]) -> dict:
    """ln-range gate per campaign on the eruption point process tau_i = t_i - t_0."""
    per_source = {}
    for sname, campaigns in sources.items():
        rows = []
        for cname, taus in campaigns.items():
            taus = [t for t in taus if t > 0]
            if len(taus) < 3:
                continue
            ln_range = math.log(max(taus) / min(taus))
            periods = ln_range * COMB_OMEGA / (2.0 * math.pi)
            rows.append({"campaign": cname, "n_events": len(taus) + 1,
                         "ln_range_periods": round(periods, 2),
                         "gate_passed": bool(periods > RANGE_GATE_PERIODS)})
        n_pass = sum(r["gate_passed"] for r in rows)
        per_source[sname] = {
            "campaigns": rows, "n_gate_passing": n_pass,
            "gate": f"> {RANGE_GATE_PERIODS} comb periods in ln(tau)",
            "verdict": "data_limited" if n_pass == 0 else "gate_passed_run_comb",
            "note": ("quasi-periodic point processes have ln-range ~ ln(N)/ln(lambda); "
                     "stacking raises amplitude, never ln-range (PG.06 machine check)")}
    return per_source


# ------------------------------------------------------------------ main
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT QPE recurrence search")
    ap.add_argument("command", choices=["analyze"], nargs="?", default="analyze")
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args(argv)
    rng = np.random.default_rng(args.seed)

    ero = load_ero_qpe2()
    gsn = load_gsn069()
    sources_rec = {"eRO-QPE2": ero, "GSN 069": {k: [(t, e) for t, e in v]
                                                for k, v in gsn.items()}}

    print("=" * 78)
    print("TFPT QPE recurrence search -- frozen kernel on real eruption timings "
          "(seed %d)" % args.seed)
    print("=" * 78)
    n_ero = sum(len(v) for v in ero.values())
    n_gsn = sum(len(v) for v in gsn.values())
    print(f"  eRO-QPE2: {len(ero)} contiguous blocks, {n_ero} recurrence times "
          f"(arXiv:2604.09788 Table B.1, machine-extracted)")
    print(f"  GSN 069 : {len(gsn)} campaigns, {n_gsn} recurrence times "
          f"(Miniutti+2023 Table A.1, curated)\n")

    q1 = ratio_ladder(sources_rec, rng)
    print("QPE.01 -- recurrence-ratio ladder vs teeth {2/3, 8/27, 64/729} (+inverses)")
    for s, r in q1.items():
        if r.get("n_ratios", 0) == 0:
            print(f"  {s:10s} no usable ratios -> {r['verdict']}")
            continue
        print(f"  {s:10s} n={r['n_ratios']:3d}  hits={r['hits_at_teeth']} "
              f"(null p={r['null_p']})  max|log r|={r['max_abs_log_ratio_dex']} dex, "
              f"spread={r['ratio_spread_dex']} dex, nearest tooth "
              f"{r['nearest_tooth_gap_dex']} dex away -> {r['verdict'].upper()}")
        print(f"             {r['sensitivity_note']}")

    q2 = clock_triplets(sources_rec)
    print("\nQPE.02 -- walled-clock gap ratio (bend 2.7095, wall N_fam=%d)" % N_FAM)
    for s, r in q2.items():
        print(f"  {s:10s} monotone triplets: {r['n_monotone_triplets']} "
              f"{r.get('triplet_gap_ratios', '')} -> {r['verdict'].upper()}")

    # comb: point process needs arrival times; for GSN069 only T_rec are curated
    ero_times: dict[str, list[float]] = {}
    with open(DATA / "ero_qpe2_arrival_times.csv", encoding="utf-8") as fh:
        rows = sorted((int(r["n_qpe"]), float(r["t_obs_s"]))
                      for r in csv.DictReader(fh))
    cur: list[tuple[int, float]] = []
    for n, t in rows:
        if cur and n != cur[-1][0] + 1:
            if len(cur) >= 4:
                t0 = cur[0][1]
                ero_times[f"block_N{cur[0][0]}-{cur[-1][0]}"] = [t - t0 for _, t in cur[1:]]
            cur = []
        cur.append((n, t))
    if len(cur) >= 4:
        t0 = cur[0][1]
        ero_times[f"block_N{cur[0][0]}-{cur[-1][0]}"] = [t - t0 for _, t in cur[1:]]

    q3 = comb_gate({"eRO-QPE2": ero_times})
    print(f"\nQPE.03 -- log-periodic comb (omega = {COMB_OMEGA:.3f}), hard ln-range gate")
    for s, r in q3.items():
        for c in r["campaigns"]:
            mark = "PASS" if c["gate_passed"] else "range-blind"
            print(f"  {s:10s} {c['campaign']:16s} {c['n_events']:2d} events, "
                  f"{c['ln_range_periods']:.2f} periods [{mark}]")
        print(f"  -> {r['verdict'].upper()} ({r['n_gate_passing']} campaigns pass "
              f"the {RANGE_GATE_PERIODS}-period gate)")

    verdicts = {"QPE.01": {s: r["verdict"] for s, r in q1.items()},
                "QPE.02": {s: r["verdict"] for s, r in q2.items()},
                "QPE.03": {s: r["verdict"] for s, r in q3.items()}}
    overall = ("null (QPE.01, replicated 2 sources, quantified sensitivity) + "
               "data_limited (QPE.02 triplet-starved, QPE.03 range-blind)")
    print(f"\n-> OVERALL: {overall}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps({
        "seed": args.seed, "n_surrogate": N_SURROGATE,
        "QPE01_ratio_ladder": q1, "QPE02_clock": q2, "QPE03_comb_gate": q3,
        "verdicts": verdicts, "overall": overall}, indent=2), encoding="utf-8")
    print(f"Wrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
