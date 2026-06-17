"""Download real GWOSC strain (32 s, 4 kHz HDF5) for chosen events -> data/strain/.

Uses the GWOSC event API to resolve the per-detector 32 s HDF5 URLs (no gwpy); for O1
events whose API entry only lists the 4096 s segment (e.g. GW150914) it falls back to the
public 32 s tutorial files. Writes a small <event>_meta.json (GPS, final mass, files) that
the search reads. Large HDF5 blobs are gitignored; only the meta JSON + this script ship.

Run:  python scripts/fetch_strain.py GW150914 GW190521
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

STRAIN = Path(__file__).resolve().parents[1] / "data" / "strain"
API = "https://gwosc.org/eventapi/json/event/{}/"
TUTORIAL = "https://gwosc.org/s/events/{ev}/{obs}-{det}_LOSC_4_V2-{start}-32.hdf5"  # O1 fallback


def _get(url: str, binary: bool = False, timeout: int = 120):
    req = urllib.request.Request(url, headers={"User-Agent": "tfpt-gw/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if binary else r.read().decode()


def resolve(event: str):
    d = json.loads(_get(API.format(event)))
    key = list(d["events"])[0]
    e = d["events"][key]
    gps = float(e["GPS"])
    mf = e.get("final_mass_source")
    if mf is None:                       # fall back to a near-total-mass estimate
        m1, m2 = e.get("mass_1_source"), e.get("mass_2_source")
        mf = round(0.95 * (m1 + m2), 1) if (m1 and m2) else None
    files = {}
    for s in e.get("strain", []):
        if (s.get("duration") == 32 and s.get("format") == "hdf5"
                and s.get("sampling_rate") == 4096):
            files[s["detector"]] = s["url"]
    if not files:                        # O1 tutorial fallback (e.g. GW150914)
        start = int(gps) - 16
        for obs, det in (("H", "H1"), ("L", "L1")):
            files[det] = TUTORIAL.format(ev=event, obs=obs, det=det, start=start)
    return key, gps, mf, files


def main(argv: list[str]) -> int:
    events = argv or ["GW150914", "GW190521"]
    STRAIN.mkdir(parents=True, exist_ok=True)
    for ev in events:
        try:
            key, gps, mf, urls = resolve(ev)
        except Exception as exc:  # noqa: BLE001
            print(f"  {ev}: RESOLVE FAILED -- {exc!r}")
            continue
        saved = {}
        for det, url in urls.items():
            out = STRAIN / Path(url).name
            try:
                if not out.exists() or out.stat().st_size < 1000:
                    print(f"  downloading {ev} {det}: {url}")
                    out.write_bytes(_get(url, binary=True))
                saved[det] = out.name
                print(f"    {det}: {out.name} ({out.stat().st_size} bytes)")
            except Exception as exc:  # noqa: BLE001
                print(f"    {det}: DOWNLOAD FAILED -- {exc!r}")
        if saved:
            (STRAIN / f"{ev}_meta.json").write_text(
                json.dumps({"event": key, "gps": gps, "mf": mf, "files": saved}, indent=2),
                encoding="utf-8")
            print(f"  {ev}: gps={gps}  mf={mf}  detectors={list(saved)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
