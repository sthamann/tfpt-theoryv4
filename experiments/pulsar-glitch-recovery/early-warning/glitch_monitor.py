#!/usr/bin/env python3
"""Vela glitch early-warning monitor (Jodrell Bank glitch table vs. local state).

Checks the live Jodrell Bank Glitch Catalogue
(https://www.jb.man.ac.uk/pulsar/glitches/gTable.html) for NEW Vela entries
(PSR B0833-45 / J0835-4510) against a local state file and reports glitch epoch
+ age in days.

Why: the whole value of this chain is the < 3-day window. PG.06b-FULL (the
complete 665-obs NICER Vela reduction, ``results/pg06b_full_vela.json``) showed
the archival early window is MISSING -- first usable observation 3.4 d (2019) /
7 d (2021) post-glitch, so the achieved ln(tau) reach is 2.17 / 1.38 comb
periods, below the 2.8-period localisation gate. A trigger inside < 3 days
(ideally < 1 d) followed by daily-cadence timing is the only route to a sharp
comb search. On a NEW-glitch alert: submit the prepared NICER ToO
(``too_request_draft.txt``) immediately.

Robustness: the JBO table is HTML without a machine API. Parsing reuses the
injection-tested ``tfpt_pulsar.catalog.parse_jbo_html`` (the one module of this
experiment that talks to the raw HTML). If the download fails or the format
breaks (no records / no Vela rows / non-monotone MJDs), the monitor REPORTS the
failure cleanly and exits 2 WITHOUT touching the state file -- it never crashes
with a traceback and never fabricates a state.

Usage:
  python glitch_monitor.py                # live check against the state file
  python glitch_monitor.py --dry-run      # live check, state file untouched
  python glitch_monitor.py --html FILE    # parse a local gTable.html (offline test)

Exit codes: 0 = no new Vela glitch, 1 = NEW VELA GLITCH (alert!), 2 = fetch/parse failure.

FIREWALL: pure monitor -- no scorecard/ledger/paper mutation; an alert only
starts the human ToO process.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENT_ROOT = HERE.parent
sys.path.insert(0, str(EXPERIMENT_ROOT / "src"))

from tfpt_pulsar.catalog import parse_jbo_html  # noqa: E402

URL = "https://www.jb.man.ac.uk/pulsar/glitches/gTable.html"
UA = "Mozilla/5.0 (compatible; tfpt-pulsar/0.1; research)"
STATE = HERE / "vela_state.json"

# Vela = PSR B0833-45 = PSR J0835-4510; the JBO table lists pulsar='B0833-45',
# jname='0835-4510' (no J prefix). Match generously on either column.
VELA_NAMES = {"B0833-45", "J0835-4510", "0835-4510"}

EARLY_WINDOW_DAYS = 3.0  # PG.06b-FULL: only a < 3 d trigger closes the reach gap
MJD_UNIX_EPOCH = 40587.0  # MJD of 1970-01-01


def mjd_now() -> float:
    return dt.datetime.now(dt.timezone.utc).timestamp() / 86400.0 + MJD_UNIX_EPOCH


def mjd_to_date(mjd: float) -> str:
    d = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc) + dt.timedelta(days=mjd - MJD_UNIX_EPOCH)
    return d.strftime("%Y-%m-%d %H:%M UTC")


def fetch_html(timeout: float = 60.0) -> str | None:
    req = urllib.request.Request(URL, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310
            return r.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"FETCH FAILED: {URL}\n  {exc}", file=sys.stderr)
        return None


def vela_glitches(html: str) -> list[dict] | None:
    """Parse and extract the Vela rows; None = the table format broke."""
    try:
        records = parse_jbo_html(html)
    except Exception as exc:  # the parser is tolerant; anything raised = format break
        print(f"PARSE FAILED: gTable.html no longer parses ({exc})", file=sys.stderr)
        return None
    if not records:
        print("PARSE FAILED: 0 glitch records parsed -- the JBO table format has "
              "changed; fix tfpt_pulsar.catalog.parse_jbo_html first.", file=sys.stderr)
        return None
    vela = [r for r in records if r.pulsar in VELA_NAMES or r.jname in VELA_NAMES]
    if not vela:
        print(f"PARSE SUSPECT: {len(records)} records parsed but NO Vela rows "
              "(B0833-45 / 0835-4510). Either the naming changed or the parse is "
              "silently wrong -- refusing to update state.", file=sys.stderr)
        return None
    out = [
        {"glitch_no": r.glitch_no, "mjd": r.mjd, "df_f_1e9": r.df_f, "reference": r.reference}
        for r in sorted(vela, key=lambda r: (r.mjd if r.mjd is not None else 0.0))
        if r.mjd is not None
    ]
    if not out:
        print("PARSE SUSPECT: Vela rows found but none carries an MJD epoch -- "
              "refusing to update state.", file=sys.stderr)
        return None
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="do not update the state file")
    ap.add_argument("--html", type=Path, default=None,
                    help="parse a local gTable.html instead of fetching (offline test)")
    args = ap.parse_args(argv)

    now = mjd_now()
    print("VELA GLITCH EARLY-WARNING MONITOR (PSR B0833-45 / J0835-4510)")
    print(f"run: {mjd_to_date(now)} (MJD {now:.4f})   source: "
          f"{args.html if args.html else URL}")

    if args.html is not None:
        try:
            html = args.html.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"READ FAILED: {exc}", file=sys.stderr)
            return 2
    else:
        html = fetch_html()
        if html is None:
            return 2

    vela = vela_glitches(html)
    if vela is None:
        return 2

    latest = vela[-1]
    print(f"catalogue: {len(vela)} Vela glitches with epochs; latest #{latest['glitch_no']} "
          f"at MJD {latest['mjd']:.4f} ({mjd_to_date(latest['mjd'])}), "
          f"dF/F = {latest['df_f_1e9']}e-9  [{latest['reference']}]")

    state = None
    if STATE.exists():
        try:
            state = json.loads(STATE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"STATE FILE CORRUPT ({exc}) -- delete {STATE.name} and re-run to "
                  "re-freeze.", file=sys.stderr)
            return 2

    new_glitches: list[dict] = []
    if state is None:
        print(f"first run: freezing current catalogue state ({len(vela)} Vela glitches) "
              "-- no alert by construction.")
    else:
        known = {round(float(m), 2) for m in state["known_epochs_mjd"]}
        new_glitches = [g for g in vela if round(float(g["mjd"]), 2) not in known]

    exit_code = 0
    if new_glitches:
        exit_code = 1
        for g in new_glitches:
            age = now - float(g["mjd"])
            in_window = age <= EARLY_WINDOW_DAYS
            print("=" * 78)
            print(f"*** NEW VELA GLITCH *** #{g['glitch_no']} at MJD {g['mjd']:.4f} "
                  f"({mjd_to_date(g['mjd'])})")
            print(f"    age: {age:.2f} days   dF/F = {g['df_f_1e9']}e-9   [{g['reference']}]")
            if in_window:
                print(f"    WITHIN the {EARLY_WINDOW_DAYS:.0f}-day early window "
                      f"({EARLY_WINDOW_DAYS - age:.2f} d left) -> submit the NICER ToO NOW "
                      "(too_request_draft.txt); daily cadence for ~14 d closes the "
                      "2.8-period reach gap (PG.06b-FULL).")
            else:
                print(f"    OUTSIDE the {EARLY_WINDOW_DAYS:.0f}-day early window -- the sharp "
                      "early-comb leg is already lost for this glitch (PG.06b-FULL: "
                      "archival reach 2.17 < 2.8 periods); long-baseline monitoring "
                      "still adds the late-recovery leg.")
            print("=" * 78)
    elif state is not None:
        age_latest = now - float(latest["mjd"])
        print(f"no new Vela glitch (state: {len(state['known_epochs_mjd'])} known epochs, "
              f"last check {state['last_check_utc']}).")
        print(f"latest known glitch is {age_latest:.1f} days old "
              f"(early window long closed; next Vela glitch expected on the ~3 yr "
              "recurrence -- keep the weekly cron alive).")

    if not args.dry_run:
        STATE.write_text(
            json.dumps(
                {
                    "pulsar": "PSR B0833-45 / J0835-4510 (Vela)",
                    "source": URL,
                    "n_vela_glitches": len(vela),
                    "known_epochs_mjd": [g["mjd"] for g in vela],
                    "latest": latest,
                    "last_check_utc": mjd_to_date(now),
                    "last_check_mjd": round(now, 4),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"state written: {STATE.name}")
    else:
        print("dry run: state file NOT updated")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
