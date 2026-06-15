#!/usr/bin/env python3
"""Download the LVK GWTC event catalogue from GWOSC and write a small CSV.

Source: https://gwosc.org/eventapi/json/GWTC/  (the cumulative GWTC event API).
We keep only the fields the echo forecast needs (name, catalog, network SNR, source
masses, final mass, redshift) so the test is reproducible from a ~40 kB CSV without
re-hitting the API. Run: ``python scripts/fetch_catalog.py``.
"""

from __future__ import annotations

import csv
import json
import sys
import urllib.request
from pathlib import Path

URL = "https://gwosc.org/eventapi/json/GWTC/"
OUT = Path(__file__).resolve().parents[1] / "data" / "gwtc_events.csv"
FIELDS = ["commonName", "catalog.shortName", "network_matched_filter_snr",
          "mass_1_source", "mass_2_source", "total_mass_source",
          "final_mass_source", "redshift"]


def main() -> int:
    try:
        with urllib.request.urlopen(URL, timeout=90) as r:   # noqa: S310 (trusted host)
            data = json.loads(r.read().decode())
    except Exception as exc:  # noqa: BLE001
        print(f"download failed ({exc}); place a cached GWTC json and retry")
        return 1
    events = data.get("events", {})
    rows = []
    for ev in events.values():
        rows.append([ev.get(k) for k in FIELDS])
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["name", "catalog", "snr", "m1", "m2", "mtot", "mfinal", "z"])
        w.writerows(rows)
    print(f"wrote {OUT} ({len(rows)} GWTC events)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
