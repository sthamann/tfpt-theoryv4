#!/usr/bin/env python3
"""Download the 4 earthquake aftershock control sequences from the USGS ComCat FDSN service.

Source: https://earthquake.usgs.gov/fdsnws/event/1/query (public, no auth).
Sequences: Landers 1992 M7.3, Hector Mine 1999 M7.1, Tohoku 2011 M9.1, Ridgecrest 2019 M7.1 —
event times + magnitudes in a radius/time window around each mainshock (parameters in
``tfpt_dsicontrol.fetch.MAINSHOCKS``). Raw CSVs cached to data/raw/ (gitignored); normalised
(t_days,size) sequences written to data/sequences/ (committed).

Run:  . ../tfpt-discovery/.venv/bin/activate && python scripts/fetch_aftershocks.py [--refresh]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tfpt_dsicontrol import fetch  # noqa: E402

if __name__ == "__main__":
    refresh = "--refresh" in sys.argv
    for ms in fetch.MAINSHOCKS:
        path = fetch.fetch_quake(ms, refresh=refresh)
        n = sum(1 for _ in path.open()) - 1
        print(f"{ms.name} ({ms.mag}): {n} aftershocks -> {path}")
