"""PG.08: fetch the PuMA/IAR daily-cadence glitch timing data release (GitHub).

The Pulsar Monitoring in Argentina (PuMA) collaboration publishes the .par/.tim
data release of "Timing irregularities and glitches from the pulsar monitoring
campaign at IAR" (Zubieta et al. 2024, A&A 689, A50441; arXiv:2406.17099) at

    https://github.com/PuMA-Coll/Timing_irregularities

It contains daily-cadence IAR TOAs (sites iar1/iar2, PINT-known observatories)
plus the phase-connected glitch characterisations ("JXXXX-XXXX_glitch.par",
TEMPO2 format with GLF0D/GLTD recovery transients) for the three giant glitches
covered by the campaign:

    J0835-4510 (Vela)  2021-07-22 glitch  (MJD 59417.62, dnu/nu ~ 2.4e-6)
    J0742-2822         2022-09    glitch  (MJD 59839.4,  dnu/nu ~ 4.3e-6)
    J1740-3015         2022-12    glitch  (MJD 59935.2,  dnu/nu ~ 3.2e-7)

Files are small (~50-210 kB) and committed under data/puma_iar/ as provenance.
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

BASE = "https://raw.githubusercontent.com/PuMA-Coll/Timing_irregularities/main"
DATA = Path(__file__).resolve().parents[1] / "data" / "puma_iar"
PULSARS = ["J0835-4510", "J0742-2822", "J1740-3015"]


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    ok = True
    for psr in PULSARS:
        for suffix in (".par", ".tim", "_glitch.par"):
            name = f"{psr}{suffix}"
            url = f"{BASE}/{name}"
            try:
                with urllib.request.urlopen(url, timeout=60) as r:
                    payload = r.read()
                (DATA / name).write_bytes(payload)
                print(f"  {name}: {len(payload)} bytes")
            except Exception as e:  # noqa: BLE001
                print(f"  !! {name}: {type(e).__name__}: {e}")
                ok = False
    print("done" if ok else "INCOMPLETE -- document as data_limited")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
