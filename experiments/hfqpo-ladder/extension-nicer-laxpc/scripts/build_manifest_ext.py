#!/usr/bin/env python3
"""Freeze the ObsID manifest for the NICER extension of the hfqpo-ladder H3 scan.

Run BEFORE any photon data is downloaded (metadata only: HTTP HEAD sizes).
Applies the triage rule frozen in hypotheses/hfqpo_ext_v1.yaml:
  - discovery ObsID 1200120107 is mandatory (sanity anchor),
  - remaining pool ObsIDs added in ascending file size until the next file would
    push the running total over BUDGET_GB.

Output: data/manifest_ext.json
"""
import json
import os
import subprocess
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "manifest_ext.json")

BASE = "https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs"
MONTHS = ["2018_03", "2018_04"]
BUDGET_GB = 15.0
MANDATORY = "1200120107"          # ATel #11951 discovery obsid (sanity anchor)
POOL = ["1200120107", "1200120108", "1200120109", "1200120110", "1200120111",
        "1200120112", "1200120113", "1200120114", "1200120115", "1200120116",
        "1200120117", "1200120118", "1200120119", "1200120120"]


def head_size(url):
    r = subprocess.run(["curl", "-s", "-I", "--max-time", "40", url],
                       capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.lower().startswith("content-length:"):
            return int(line.split(":")[1].strip())
    return None


def main():
    rows = []
    for obsid in POOL:
        for month in MONTHS:
            url = f"{BASE}/{month}/{obsid}/xti/event_cl/ni{obsid}_0mpu7_cl.evt.gz"
            sz = head_size(url)
            if sz:
                rows.append({"obsid": obsid, "month": month, "url": url,
                             "bytes": sz})
                print(f"{obsid} {month} {sz/1e9:6.2f} GB", flush=True)
                break
        else:
            rows.append({"obsid": obsid, "month": None, "url": None,
                         "bytes": None, "error": "not found via HEAD"})
            print(f"{obsid} NOT FOUND", flush=True)

    # triage: mandatory discovery obsid first, then ascending size
    found = [r for r in rows if r["bytes"]]
    mand = [r for r in found if r["obsid"] == MANDATORY]
    rest = sorted([r for r in found if r["obsid"] != MANDATORY],
                  key=lambda r: r["bytes"])
    selected = []
    total = 0
    for r in mand + rest:
        if total + r["bytes"] > BUDGET_GB * 1e9:
            r["triage"] = "skipped_over_budget"
            continue
        total += r["bytes"]
        r["triage"] = "selected"
        selected.append(r["obsid"])

    manifest = {
        "comment": ("Frozen ObsID manifest for the NICER extension scan "
                    "(hypotheses/hfqpo_ext_v1.yaml). Created BEFORE photon "
                    "download; sizes via HTTP HEAD only."),
        "frozen_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "MAXI_J1820+070",
        "anchor_hz": 55.12, "tooth_hz": 82.68, "integer_hz": 110.24,
        "budget_gb": BUDGET_GB,
        "triage_rule": "discovery obsid mandatory, then ascending size, "
                       "hard stop before exceeding budget",
        "files": rows,
        "selected_obsids": selected,
        "selected_bytes_total": total,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nmanifest frozen: {OUT}")
    print(f"selected {len(selected)} obsids, {total/1e9:.2f} GB "
          f"(budget {BUDGET_GB} GB)")


if __name__ == "__main__":
    main()
