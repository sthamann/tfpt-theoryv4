#!/usr/bin/env python3
"""Resolve + list the NICER observations of the Vela pulsar (PSR B0833-45 / J0835-4510).

PG.06b: Vela is the long-interval, densely-monitored target the dynamic recovery comb needs.
This queries the HEASARC `nicermastr` master table (VO TAP, cone search at the Vela-pulsar
position -- NOT Vela X-1, a different object 7 deg away) and writes a committable observation
list. The cleaned L2 events + orbit per ObsID (~10 MB each, ~6.6 GB total) are NOT auto-fetched;
download one with `tfpt-pulsar vela --download` (see src/tfpt_pulsar/vela.py).

Run:  python scripts/fetch_nicer_vela.py
"""

from __future__ import annotations

import csv
import io
import sys
import urllib.parse
import urllib.request
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "nicer_vela"
OBS_CSV = DATA / "vela_observations.csv"

# Vela PULSAR (PSR B0833-45 / J0835-4510), J2000 -- NOT the binary Vela X-1
RA_DEG, DEC_DEG = 128.8359, -45.1764
TAP = "https://heasarc.gsfc.nasa.gov/xamin/vo/tap/sync"
UA = "tfpt-pulsar/0.1 (research)"


def resolve_observations(radius_deg: float = 0.02) -> list[dict]:
    """Cone-search nicermastr at the Vela-pulsar position; return obsid/time/exposure dicts."""
    from astropy.io.votable import parse_single_table

    adql = (f"SELECT obsid, name, time, exposure FROM nicermastr "
            f"WHERE CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',{RA_DEG},{DEC_DEG},{radius_deg}))=1 "
            f"ORDER BY time")
    url = TAP + "?" + urllib.parse.urlencode({"query": adql, "request": "doQuery", "lang": "ADQL"})
    with urllib.request.urlopen(  # noqa: S310
            urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120) as r:
        raw = r.read()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        tb = parse_single_table(io.BytesIO(raw)).to_table()
    idc = "obsid" if "obsid" in tb.colnames else "DataLinkID"
    return [{"obsid": str(row[idc]), "name": str(row["name"]),
             "time": float(row["time"]) if row["time"] is not None else 0.0,
             "exposure": float(row["exposure"] or 0.0)} for row in tb]


def main(argv: list[str]) -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    print("Resolving NICER observations of the Vela pulsar (PSR B0833-45)...")
    try:
        rows = [r for r in resolve_observations() if r["time"] > 0]
    except Exception as exc:  # noqa: BLE001
        print(f"  TAP query failed ({exc!r}).")
        return 1
    rows.sort(key=lambda r: r["time"])
    with OBS_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["obsid", "name", "mjd_start", "exposure_s"])
        for r in rows:
            w.writerow([r["obsid"], r["name"], r["time"], r["exposure"]])
    mjd = [r["time"] for r in rows]
    gb = len(rows) * 10.0 / 1024.0
    print(f"  -> {len(rows)} observations, MJD {min(mjd):.0f}..{max(mjd):.0f} "
          f"({(max(mjd)-min(mjd))/365.25:.1f} yr), total ~{sum(r['exposure'] for r in rows)/1e3:.0f} ks")
    print(f"     wrote {OBS_CSV}  (full L2 event download ~{gb:.1f} GB; not auto-fetched)")
    print(f"  next: tfpt-pulsar vela   (downloads one obs + proves the PINT fold on real data)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
