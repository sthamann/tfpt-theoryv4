"""Fetch O4/GWTC-4+ strain: download the 4096 s 4 kHz GWOSC HDF5 segment, crop a
32 s window around the merger, and write it in the same layout the 32 s files use
(``strain/Strain`` + ``meta``), so the Stage-1/2 searches read it unchanged.

O4a/O4b events have no 32 s files on GWOSC (only 4096 s archive segments), which is
why scripts/fetch_strain.py 404s on them.  The big segment is deleted after cropping;
only the 32 s crop + <event>_meta.json stay (gitignored like all strain).

Run:  python scripts/fetch_strain_4096.py GW250114_082203 GW230814_230901 ...
"""

from __future__ import annotations

import csv
import json
import sys
import tempfile
import urllib.request
from pathlib import Path

import h5py
import numpy as np

HERE = Path(__file__).resolve().parents[1]
STRAIN = HERE / "data" / "strain"
CATALOG = HERE / "data" / "gwtc_events.csv"
API = "https://gwosc.org/eventapi/json/event/{}/"
WINDOW_S = 32


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "tfpt-gw/0.1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def _mfinal(event: str) -> float:
    with open(CATALOG, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["name"] == event and row.get("mfinal"):
                return float(row["mfinal"])
    raise SystemExit(f"{event}: no mfinal in {CATALOG}")


def _crop(big_path: Path, out_path: Path, gps_event: float, detector: str) -> float:
    with h5py.File(big_path, "r") as f:
        st = f["strain/Strain"]
        dt = float(st.attrs["Xspacing"])
        gps_start = float(f["meta"]["GPSstart"][()])
        start_gps = float(int(gps_event - WINDOW_S / 2))
        i0 = int(round((start_gps - gps_start) / dt))
        n = int(round(WINDOW_S / dt))
        if i0 < 0 or i0 + n > st.shape[0]:
            raise ValueError(f"{detector}: event not inside the 4096 s segment")
        data = np.asarray(st[i0:i0 + n], dtype=float)
    if not np.all(np.isfinite(data)):
        raise ValueError(f"{detector}: NaNs in the 32 s window (detector not observing)")
    with h5py.File(out_path, "w") as f:
        ds = f.create_dataset("strain/Strain", data=data)
        ds.attrs["Xspacing"] = dt
        g = f.create_group("meta")
        g.create_dataset("GPSstart", data=start_gps)
        g.create_dataset("Detector", data=np.bytes_(detector))
    return start_gps


def fetch(event: str) -> None:
    d = _get_json(API.format(event))
    ev = list(d["events"].values())[0]
    gps = float(ev["GPS"])
    mf = _mfinal(event)
    # one 4 kHz HDF5 segment per detector
    seen: dict[str, str] = {}
    for s in ev.get("strain", []):
        if (s.get("format") == "hdf5" and int(s.get("sampling_rate", 0)) == 4096
                and s.get("detector") not in seen):
            seen[s["detector"]] = s["url"]
    if not seen:
        raise SystemExit(f"{event}: no 4 kHz hdf5 strain in the event API")

    STRAIN.mkdir(parents=True, exist_ok=True)
    files: dict[str, str] = {}
    for det, url in sorted(seen.items()):
        out_name = f"{det[0]}-{det}_GWOSC_4KHZ_CROP32-{int(gps)}-32.hdf5"
        out_path = STRAIN / out_name
        if not out_path.exists():
            print(f"  {event} {det}: downloading 4096 s segment ...", flush=True)
            with tempfile.NamedTemporaryFile(suffix=".hdf5", delete=False) as tmp:
                tmp_path = Path(tmp.name)
            req = urllib.request.Request(url, headers={"User-Agent": "tfpt-gw/0.1"})
            with urllib.request.urlopen(req, timeout=600) as r, open(tmp_path, "wb") as out:
                while chunk := r.read(1 << 20):
                    out.write(chunk)
            try:
                _crop(tmp_path, out_path, gps, det)
            except ValueError as exc:
                print(f"    {det}: SKIPPED -- {exc}")
                continue
            finally:
                tmp_path.unlink(missing_ok=True)
            print(f"    -> {out_name} ({out_path.stat().st_size} bytes)")
        else:
            print(f"  {event} {det}: {out_name} already present")
        files[det] = out_name

    if not files:
        print(f"  {event}: no usable detector window -- skipped entirely")
        return
    meta = {"gps": gps, "mf": mf, "files": files}
    (STRAIN / f"{event}_meta.json").write_text(json.dumps(meta, indent=2),
                                               encoding="utf-8")
    print(f"  {event}: gps={gps}  mf={mf}  detectors={sorted(files)}")


if __name__ == "__main__":
    events = sys.argv[1:]
    if not events:
        raise SystemExit("usage: python scripts/fetch_strain_4096.py EVENT [EVENT ...]")
    for e in events:
        fetch(e)
