#!/usr/bin/env python3
"""Download real EHT M87 2017 polarimetric uvfits (data product 2023-D01-01).

Source: https://github.com/eventhorizontelescope/2023-D01-01 (CyVerse DOI
10.25739/q46m-m857). We pull the D-term-calibrated, self-calibrated HOPS sets
(`*_hops_zbl-dtcal+selfcal.uvfits`) for two observing days, both frequency bands
(hi ~229.1 GHz, lo ~227.1 GHz) -- the two bands let us measure the band-to-band EVPA
rotation (the Faraday / achromaticity diagnostic) on REAL data.

Each file is ~0.5 MB. Run: ``python scripts/fetch_eht_data.py``.
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

BASE = "https://raw.githubusercontent.com/eventhorizontelescope/2023-D01-01/master/hops_data"
OUT = Path(__file__).resolve().parents[1] / "data" / "eht_m87_2017"
# (day, day-of-year)
DAYS = [("April05", "095"), ("April06", "096"), ("April10", "100"), ("April11", "101")]
BANDS = ("hi", "lo")
STAGE = "hops_zbl-dtcal+selfcal"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for day, doy in DAYS:
        for band in BANDS:
            fname = f"SR2_M87_2017_{doy}_{band}_{STAGE}.uvfits"
            url = f"{BASE}/{day}/{fname}"
            dest = OUT / f"{day}_{band}.uvfits"
            try:
                urllib.request.urlretrieve(url, dest)  # noqa: S310 (trusted host)
                n += 1
                print(f"  {day}_{band}: {dest.stat().st_size} bytes")
            except Exception as exc:  # noqa: BLE001
                print(f"  {day}_{band}: FAILED ({exc})")
    print(f"downloaded {n} real EHT polarimetric uvfits to {OUT}")
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main())
