#!/usr/bin/env python3
"""Download + parse the Jodrell Bank Crab Pulsar Monthly Ephemeris -> ``data/crab_ephemeris.csv``.

The Crab monthly radio-timing ephemeris (Lyne, Pritchard, Graham-Smith / Jodrell Bank,
``https://www.jb.man.ac.uk/pulsar/crab/crab2.txt``) tabulates, per month since 1988, the spin
frequency ``nu`` (Hz) and spin-down rate ``nudot`` (1e-15 s^-2) with errors. This is a *real,
time-resolved* nu(t) / nudot(t) series spanning ~38 yr -- the long-baseline post-glitch recovery
*waveform* the static glitch-size catalogue (PG.01-04) lacks, and the only public dataset with the
wide ln(time) range a log-periodic recovery comb (PG.05) needs.

Run from anywhere:  ``python scripts/fetch_crab_ephemeris.py``

The fetched text is ~43 KB; the small derived ``data/crab_ephemeris.csv`` (~580 rows) is committed.
Cite the Jodrell Bank Crab Pulsar Monthly Ephemeris (Lyne, Pritchard & Graham-Smith 1993, MNRAS
265, 1003; updated monthly) when using these data.
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tfpt_pulsar.catalog import (  # noqa: E402
    CRAB_CSV,
    DATA,
    parse_crab_ephemeris,
    write_crab_csv,
)

URL = "https://www.jb.man.ac.uk/pulsar/crab/crab2.txt"
UA = "Mozilla/5.0 (compatible; tfpt-pulsar/0.1; research)"


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    print(f"fetching {URL} ...")
    req = urllib.request.Request(URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:  # noqa: S310
        text = r.read().decode("utf-8", errors="replace")
    print(f"  got {len(text)} bytes")

    rows = parse_crab_ephemeris(text)
    write_crab_csv(rows)
    if rows:
        print(f"  parsed {len(rows)} monthly points, MJD {rows[0].mjd:.0f}..{rows[-1].mjd:.0f} "
              f"({(rows[-1].mjd - rows[0].mjd) / 365.25:.1f} yr)")
    print(f"  wrote {CRAB_CSV}")
    return 0 if rows else 1


if __name__ == "__main__":
    raise SystemExit(main())
