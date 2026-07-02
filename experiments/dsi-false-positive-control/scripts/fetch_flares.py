#!/usr/bin/env python3
"""Download the 4 solar-flare control sequences from the NOAA NGDC GOES XRS flare reports.

Source: https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/
x-rays/goes/xrs/goes-xrs-report_<year>.txt (public yearly files, no auth). For each trigger
X-flare (Halloween 2003 X17.2, Sep 2005 X17.0, Aug 2011 X6.9, Oct 2014 X3.1) the sequence is all
sun-wide >=C1 flare START times within 60 days of the trigger's start (t0 located in the data:
the largest flare on the trigger date). Parameters in ``tfpt_dsicontrol.fetch.FLARE_TRIGGERS``.
Raw yearly files cached to data/raw/ (gitignored); normalised (t_days,size=peak flux W/m^2)
sequences written to data/sequences/ (committed).

Run:  . ../tfpt-discovery/.venv/bin/activate && python scripts/fetch_flares.py [--refresh]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tfpt_dsicontrol import fetch  # noqa: E402

if __name__ == "__main__":
    refresh = "--refresh" in sys.argv
    for tr in fetch.FLARE_TRIGGERS:
        path = fetch.fetch_flares(tr, refresh=refresh)
        n = sum(1 for _ in path.open()) - 1
        print(f"{tr.name} ({tr.label}): {n} flares -> {path}")
