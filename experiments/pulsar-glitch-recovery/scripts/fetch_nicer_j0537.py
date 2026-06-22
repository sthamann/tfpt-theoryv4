#!/usr/bin/env python3
"""Resolve NICER ObsIDs for PSR J0537-6910 and print the (heavy) L2-event fetch recipe.

PG.06 needs the DENSE X-ray nu(t) of the "Big Glitcher". This script does the small, free part:
it queries the HEASARC `nicermastr` master table (VO TAP, cone search around J0537-6910) and
writes a committable ObsID list. The actual L2 event/orbit downloads are ~GB and are NOT run
automatically -- the per-ObsID `wget` recipe is printed (and gated behind --download).

HEASoft is NOT required: the archived `*_0mpu7_cl.evt` are cleaned L2 products, and PINT
barycentres + folds them (see src/tfpt_pulsar/nicer_j0537.py). Run:

    python scripts/fetch_nicer_j0537.py            # resolve ObsIDs (small) + print recipe
    python scripts/fetch_nicer_j0537.py --download # ALSO fetch L2 events (~GB!) -- opt-in
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
DATA = ROOT / "data" / "nicer_j0537"
OBS_CSV = DATA / "j0537_observations.csv"

TAP = "https://heasarc.gsfc.nasa.gov/xamin/vo/tap/sync"
XAMIN = "https://heasarc.gsfc.nasa.gov/xamin/"
ARCHIVE = "https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs"
UA = "tfpt-pulsar/0.1 (research)"


def resolve_observations() -> list[dict]:
    """Query the HEASARC NICER master table for all PSR J0537-6910 observations (name match).

    HEASARC's TAP returns BINARY-serialised VOTable, so we parse with astropy (installed in the
    experiments venv). Returns a list of {name, time, end_time, exposure} dicts."""
    from astropy.io.votable import parse_single_table

    adql = ("SELECT name, time, end_time, exposure FROM nicermastr "
            "WHERE name LIKE '%0537%' ORDER BY time")
    url = TAP + "?" + urllib.parse.urlencode(
        {"query": adql, "request": "doQuery", "lang": "ADQL"})   # default = VOTable
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:  # noqa: S310
        raw = r.read()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        tb = parse_single_table(io.BytesIO(raw)).to_table()
    return [{c: row[c] for c in tb.colnames} for row in tb]


def main(argv: list[str]) -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    print("Resolving NICER observations of PSR J0537-6910 (HEASARC nicermastr, name match)...")
    try:
        rows = resolve_observations()
    except Exception as exc:  # noqa: BLE001
        print(f"  TAP query failed ({exc!r}); use the manual recipe below.")
        rows = []

    if rows:
        def fnum(r: dict, k: str) -> float:
            try:
                return float(r.get(k) or 0.0)
            except ValueError:
                return 0.0

        rows = [r for r in rows if fnum(r, "time") > 0]
        with OBS_CSV.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["name", "mjd_start", "mjd_end", "exposure_s"])
            for r in rows:
                w.writerow([r.get("name", ""), r.get("time", ""), r.get("end_time", ""),
                            r.get("exposure", "")])
        mjds = sorted(fnum(r, "time") for r in rows)
        total_ks = sum(fnum(r, "exposure") for r in rows) / 1e3
        print(f"  -> {len(rows)} observations, MJD {mjds[0]:.0f}..{mjds[-1]:.0f} "
              f"({(mjds[-1]-mjds[0])/365.25:.1f} yr), total exposure ~{total_ks:.0f} ks")
        print(f"     wrote {OBS_CSV}  (confirms the dense X-ray nu(t) the comb test needs EXISTS)")
    else:
        print("  No observation list written. Manual: HEASARC Xamin -> table 'nicermastr' -> "
              "object 'PSR J0537-6910'.")

    print("\nPer-observation L2 fetch recipe (cleaned events + orbit; ~GB total, NOT auto-run):")
    print(f"  nicermastr exposes no clean ObsID column here -> use Xamin 'Download products'")
    print(f"  ({XAMIN}) to get the per-ObsID wget script, or browse the archive tree:")
    print(f"    {ARCHIVE}/<YYYY_MM>/<ObsID>/xti/event_cl/ni<ObsID>_0mpu7_cl.evt.gz")
    print(f"    {ARCHIVE}/<YYYY_MM>/<ObsID>/auxil/ni<ObsID>.orb.gz")
    print("  Then: PINT get_NICER_TOAs + satellite observatory from .orb + per-block folding")
    print("        -> data/nicer_j0537/j0537_nu_t.csv  (mjd, nu, nudot); HEASoft NOT needed.")

    if "--download" in argv:
        print("\n--download given, but the bulk GB fetch is intentionally left to the operator "
              "(use the Xamin wget script). This script will not pull GB unattended.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
