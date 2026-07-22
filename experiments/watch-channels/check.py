#!/usr/bin/env python3
"""TFPT watch-channels checker: live measurements vs. the frozen TFPT bands.

Compares ``measurements.json`` (hand-maintained live side, provenance + date per
entry) against ``frozen_bands.json`` (TFPT targets + kill windows, extracted
verbatim from ``verification/predictions_frozen.json`` and the evidence
scorecard). Computes per-channel pulls, distance to the preregistered kill
criterion, and flags status changes against the previous run (``state.json``).

Pull convention (same as the scorecard): ``pull = (TFPT - measured) / sigma``.
For asymmetric errors the error bar on the side of the TFPT value is used.

Status per channel:
  PASS   |pull| < 2 sigma (and central value inside any kill window)
  WATCH  2 sigma <= |pull| < kill threshold, or central value outside a kill
         window at low significance, or an exclusion-type channel at
         >= watch_sigma but below kill
  ALERT  the preregistered kill criterion is met at face value -> escalate to
         a human; the scorecard/ledger is NEVER mutated from here

FIREWALL: pure monitor. Read-only on everything except its own ``state.json``.
No scorecard, ledger, paper or website mutation; an ALERT is a prompt for a
human to re-run the relevant experiment pipeline, nothing more.

Usage:  python check.py [--dry-run]      (exit 0 = no ALERT, 1 = ALERT, 2 = config error)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FROZEN = HERE / "frozen_bands.json"
MEASURED = HERE / "measurements.json"
STATE = HERE / "state.json"

PASS, WATCH, ALERT = "PASS", "WATCH", "ALERT"
PULL_WATCH_SIGMA = 2.0  # generic watch threshold below the per-channel kill


def _fmt(x: float) -> str:
    return f"{x:.6g}"


def _sided_sigma(entry: dict, tfpt: float) -> float:
    """Symmetric sigma, or the asymmetric error bar on the TFPT side."""
    if "sigma" in entry:
        return float(entry["sigma"])
    if tfpt >= float(entry["value"]):
        return float(entry.get("sigma_plus") or entry["sigma_minus"])
    return float(entry.get("sigma_minus") or entry["sigma_plus"])


def _entry_label(entry: dict) -> str:
    return f"{entry['experiment']} ({entry.get('date', '?')})"


def _record_entry(entries: list[dict]) -> dict:
    for e in entries:
        if e.get("record"):
            return e
    return entries[0]


def _pull(ch: dict, entry: dict) -> float:
    sigma = _sided_sigma(entry, ch["tfpt_value"])
    return (ch["tfpt_value"] - float(entry["value"])) / sigma


def eval_gaussian(ch: dict, entries: list[dict]) -> dict:
    rec = _record_entry(entries)
    pull = _pull(ch, rec)
    kill_sigma = float(ch.get("kill_sigma", 3.0))
    watch_sigma = float(ch.get("watch_sigma", PULL_WATCH_SIGMA))
    status = PASS
    if abs(pull) >= kill_sigma:
        status = ALERT
    elif abs(pull) >= watch_sigma:
        status = WATCH
    kill_margin = f"{kill_sigma - abs(pull):.2f} sigma to kill (|pull| vs {kill_sigma:g})"

    notes = []
    window = ch.get("kill_window")
    if window is not None:
        lo, hi = float(window[0]), float(window[1])
        val = float(rec["value"])
        if val < lo or val > hi:
            edge = lo if val < lo else hi
            sigma = float(rec.get("sigma") or (rec["sigma_plus"] if val > hi else rec["sigma_minus"]))
            exceed = abs(val - edge) / sigma
            if exceed >= kill_sigma:
                status = ALERT
            elif status == PASS:
                status = WATCH
            notes.append(
                f"central value {_fmt(val)} OUTSIDE kill window [{_fmt(lo)}, {_fmt(hi)}] "
                f"at {exceed:.2f} sigma (kill needs >= {kill_sigma:g} sigma robust)"
            )
            kill_margin = f"{kill_sigma - exceed:.2f} sigma to kill (window exceedance)"
        else:
            dist = min(
                (val - lo) / float(rec.get("sigma") or rec.get("sigma_minus")),
                (hi - val) / float(rec.get("sigma") or rec.get("sigma_plus")),
            )
            notes.append(f"central value inside kill window [{_fmt(lo)}, {_fmt(hi)}]; nearest edge {dist:.2f} sigma away")

    for e in entries:
        if e is not rec:
            notes.append(f"also: {_entry_label(e)} -> pull {_pull(ch, e):+.2f} sigma")
    return {
        "status": status,
        "pull": round(pull, 3),
        "measured": f"{_entry_label(rec)}: {_fmt(float(rec['value']))}",
        "kill_margin": kill_margin,
        "notes": notes,
    }


def eval_band(ch: dict, entries: list[dict]) -> dict:
    rec = _record_entry(entries)
    lo, hi = (float(x) for x in ch["band"])
    val, sigma = float(rec["value"]), float(rec["sigma"])
    kill_sigma = float(ch.get("kill_sigma", 3.0))
    if lo <= val <= hi:
        status, pull = PASS, 0.0
        kill_margin = f"inside band [{_fmt(lo)}, {_fmt(hi)}]"
    else:
        edge = lo if val < lo else hi
        pull = (edge - val) / sigma
        status = ALERT if abs(pull) >= kill_sigma else (WATCH if abs(pull) >= PULL_WATCH_SIGMA else PASS)
        kill_margin = f"{kill_sigma - abs(pull):.2f} sigma to kill (band-edge pull vs {kill_sigma:g})"
    notes = []
    if "branch_value" in ch:
        bp = (float(ch["branch_value"]) - val) / sigma
        notes.append(f"slow-reheating branch {_fmt(float(ch['branch_value']))} -> pull {bp:+.2f} sigma (band verdict above)")
    for e in entries:
        if e is not rec:
            notes.append(f"also: {_entry_label(e)}: {_fmt(float(e['value']))}")
    return {
        "status": status,
        "pull": round(pull, 3),
        "measured": f"{_entry_label(rec)}: {_fmt(val)}",
        "kill_margin": kill_margin,
        "notes": notes,
    }


def eval_upper_limit(ch: dict, entries: list[dict]) -> dict:
    rec = _record_entry(entries)
    limit = float(rec["upper_limit"])
    lo, hi = (float(x) for x in ch["band"])
    if hi < limit:
        status = PASS
        kill_margin = f"band max {_fmt(hi)} is {limit / hi:.1f}x below the limit {_fmt(limit)}"
    elif lo < limit:
        status = WATCH
        kill_margin = f"limit {_fmt(limit)} cuts INTO the band [{_fmt(lo)}, {_fmt(hi)}]"
    else:
        status = ALERT
        kill_margin = f"whole band [{_fmt(lo)}, {_fmt(hi)}] above the limit {_fmt(limit)}"
    return {
        "status": status,
        "pull": None,
        "measured": f"{_entry_label(rec)}: < {_fmt(limit)} (95% CL)",
        "kill_margin": kill_margin,
        "notes": [f"also: {_entry_label(e)}" for e in entries if e is not rec],
    }


def eval_exclusion(ch: dict, entries: list[dict]) -> dict:
    rec = _record_entry(entries)
    excl = float(rec["exclusion_sigma"])
    watch_sigma = float(ch.get("watch_sigma", 3.0))
    kill_sigma = float(ch.get("kill_sigma", 5.0))
    if excl >= kill_sigma:
        status = ALERT
    elif excl >= watch_sigma:
        status = WATCH
    else:
        status = PASS
    notes = [
        f"also: {_entry_label(e)} -> {float(e['exclusion_sigma']):.2f} sigma exclusion"
        for e in entries
        if e is not rec
    ]
    return {
        "status": status,
        "pull": round(excl, 3),
        "measured": f"{_entry_label(rec)}: excludes TFPT value at {excl:.1f} sigma",
        "kill_margin": f"{kill_sigma - excl:.2f} sigma to kill (exclusion vs {kill_sigma:g})",
        "notes": notes,
    }


EVALUATORS = {
    "gaussian": eval_gaussian,
    "band": eval_band,
    "upper_limit": eval_upper_limit,
    "exclusion": eval_exclusion,
}


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="do not update state.json")
    args = ap.parse_args(argv)

    try:
        frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
        measured = json.loads(MEASURED.read_text(encoding="utf-8"))["channels"]
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"CONFIG ERROR: cannot load inputs: {exc}", file=sys.stderr)
        return 2

    prev = load_state()
    prev_channels = prev.get("channels", {})
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    results: dict[str, dict] = {}
    print("TFPT WATCH-CHANNELS -- live measurements vs frozen bands")
    print(f"run: {now}   previous run: {prev.get('last_run', '(none -- first run)')}")
    print("pull convention: (TFPT - measured)/sigma, TFPT-side error bar for asymmetric errors")
    print("=" * 100)

    changes: list[str] = []
    n_alert = 0
    for ch in frozen["channels"]:
        cid = ch["id"]
        entries = measured.get(cid)
        if not entries:
            print(f"[{cid}] CONFIG ERROR: no measurement entries -- update measurements.json")
            return 2
        try:
            res = EVALUATORS[ch["type"]](ch, entries)
        except (KeyError, TypeError, ValueError) as exc:
            print(f"[{cid}] CONFIG ERROR: {exc}")
            return 2
        results[cid] = res
        n_alert += res["status"] == ALERT

        old = prev_channels.get(cid, {}).get("status")
        marker = ""
        if old is None:
            marker = "  [NEW]"
        elif old != res["status"]:
            marker = f"  [CHANGED {old} -> {res['status']}]"
            changes.append(f"{cid}: {old} -> {res['status']}")

        tfpt_str = _fmt(ch["tfpt_value"]) if "tfpt_value" in ch else f"band [{_fmt(float(ch['band'][0]))}, {_fmt(float(ch['band'][1]))}]"
        pull_str = f"{res['pull']:+.2f}" if isinstance(res["pull"], float) and ch["type"] != "exclusion" else (
            f"{res['pull']:.2f}" if isinstance(res["pull"], float) else "  --")
        print(f"{res['status']:<6} {cid:<24} ({ch['rank']}){marker}")
        print(f"       TFPT: {tfpt_str}   [{ch['formula']}]")
        print(f"       data: {res['measured']}   pull: {pull_str} sigma")
        print(f"       kill: {ch['kill_criterion']}")
        print(f"       margin: {res['kill_margin']}")
        for note in res["notes"]:
            print(f"       note: {note}")
        print("-" * 100)

    counts = {s: sum(r["status"] == s for r in results.values()) for s in (PASS, WATCH, ALERT)}
    print(f"SUMMARY: {counts[PASS]} PASS / {counts[WATCH]} WATCH / {counts[ALERT]} ALERT   ({len(results)} channels)")
    if changes:
        print("STATUS CHANGES since last run:")
        for c in changes:
            print(f"  * {c}")
    elif prev_channels:
        print("STATUS CHANGES since last run: none")

    if not args.dry_run:
        STATE.write_text(
            json.dumps(
                {
                    "last_run": now,
                    "channels": {cid: {"status": r["status"], "pull": r["pull"]} for cid, r in results.items()},
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"state written: {STATE.name}")
    else:
        print("dry run: state.json NOT updated")

    return 1 if n_alert else 0


if __name__ == "__main__":
    raise SystemExit(main())
