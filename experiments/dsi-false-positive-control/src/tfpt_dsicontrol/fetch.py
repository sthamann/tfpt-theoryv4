"""Fetch the two public control-data worlds: earthquake aftershocks + solar-flare sequences.

(1) EARTHQUAKE AFTERSHOCKS — USGS ComCat FDSN event service (no auth):
    https://earthquake.usgs.gov/fdsnws/event/1/query
    Event times + magnitudes in a radius/time window around 4 large mainshocks. Aftershock
    cascades follow Omori t^-p decay, and the literature (Sornette et al.) reports log-periodic
    (discrete-scale-invariance) structure in some sequences — the canonical NON-TFPT DSI system.
    The window/radius/minmag choices mirror ``recovery-comb-domains``'s quake channel so the two
    experiments see comparable sequences.

(2) SOLAR FLARES — NOAA NGDC GOES XRS flare reports (public yearly text files):
    https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/
    Sun-wide >=C1 flare start times in a 60-day window after 4 large X-flares. Flare occurrence
    after big events follows an Omori-like decaying rate (de Arcangelis et al. 2006) — a second,
    physically independent generic relaxation cascade.

Raw downloads are cached in data/raw/ (gitignored); the small normalised per-sequence event-time
CSVs (t_days,size) are written to data/sequences/ and committed.
"""

from __future__ import annotations

import csv
import io
import math
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data"
RAW = DATA / "raw"
SEQ = DATA / "sequences"
UA = {"User-Agent": "tfpt-research/0.1 (dsi-false-positive-control; mailto:test@example.com)"}
USGS = "https://earthquake.usgs.gov/fdsnws/event/1/query?"
NGDC = ("https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/"
        "solar-flares/x-rays/goes/xrs/goes-xrs-report_{year}.txt")

CLASS_W = {"A": 1e-8, "B": 1e-7, "C": 1e-6, "M": 1e-5, "X": 1e-4}  # W/m^2 per GOES class letter


@dataclass(frozen=True)
class Mainshock:
    name: str
    mag: str          # documentation only
    start: str        # mainshock date (window start)
    end: str          # window end (~3 yr, the recovery-comb-domains convention)
    lat: float
    lon: float
    radius_km: float
    minmag: float


MAINSHOCKS: tuple[Mainshock, ...] = (
    Mainshock("Landers1992", "M7.3", "1992-06-28", "1995-06-28", 34.200, -116.437, 80, 2.5),
    Mainshock("HectorMine1999", "M7.1", "1999-10-16", "2002-10-16", 34.594, -116.271, 80, 2.5),
    Mainshock("Tohoku2011", "M9.1", "2011-03-11", "2014-03-11", 38.297, 142.373, 500, 4.5),
    Mainshock("Ridgecrest2019", "M7.1", "2019-07-06", "2022-07-06", 35.770, -117.599, 80, 2.0),
)


@dataclass(frozen=True)
class FlareTrigger:
    name: str
    date: str         # YYYY-MM-DD of the trigger X-flare (t0 = its start time, read from the file)
    label: str        # documentation only
    window_days: int = 60
    min_class_wm2: float = 1e-6   # >= C1.0


FLARE_TRIGGERS: tuple[FlareTrigger, ...] = (
    FlareTrigger("Halloween2003", "2003-10-28", "X17.2 (AR 10486)"),
    FlareTrigger("Sep2005", "2005-09-07", "X17.0 (AR 10808)"),
    FlareTrigger("Aug2011", "2011-08-09", "X6.9 (AR 11263)"),
    FlareTrigger("Oct2014", "2014-10-24", "X3.1 (AR 12192)"),
)


def _get(url: str, cache: Path, *, refresh: bool = False) -> str:
    cache.parent.mkdir(parents=True, exist_ok=True)
    if cache.exists() and not refresh:
        return cache.read_text(encoding="utf-8")
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:  # noqa: S310
        txt = r.read().decode("utf-8", "replace")
    cache.write_text(txt, encoding="utf-8")
    return txt


def _write_sequence(name: str, rows: list[tuple[float, float]]) -> Path:
    SEQ.mkdir(parents=True, exist_ok=True)
    out = SEQ / f"{name}.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_days", "size"])
        w.writerows((f"{t:.6f}", f"{s:g}") for t, s in rows)
    return out


# ------------------------------------------------------------------ (1) USGS aftershock sequences
def fetch_quake(ms: Mainshock, *, refresh: bool = False) -> Path:
    """Aftershock (t_days since first catalogued event, magnitude) rows -> data/sequences/."""
    url = USGS + urllib.parse.urlencode({
        "format": "csv", "starttime": ms.start, "endtime": ms.end,
        "latitude": ms.lat, "longitude": ms.lon, "maxradiuskm": ms.radius_km,
        "minmagnitude": ms.minmag, "orderby": "time-asc", "limit": 20000})
    txt = _get(url, RAW / f"usgs_{ms.name}.csv", refresh=refresh)
    events = []
    for row in csv.DictReader(io.StringIO(txt)):
        try:
            when = datetime.fromisoformat(row["time"].replace("Z", "+00:00"))
            events.append((when, float(row["mag"] or "nan")))
        except (KeyError, ValueError):
            continue
    if len(events) < 20:
        raise RuntimeError(f"{ms.name}: only {len(events)} events from USGS")
    t0 = min(when for when, _ in events)   # the mainshock (first catalogued event of the window)
    rows = sorted((((when - t0).total_seconds() / 86400.0), mag) for when, mag in events)
    rows = [(t, mag) for t, mag in rows if t > 0 and math.isfinite(mag)]
    return _write_sequence(ms.name, rows)


# ------------------------------------------------------------- (2) GOES XRS flare-list sequences
_LINE = re.compile(r"^31777(\d{2})(\d{2})(\d{2}).{2}(\d{4})")
_CLASS = re.compile(r"\s([ABCMX])\s?(\d{2,3})\s")


def _parse_goes(txt: str) -> list[tuple[datetime, float]]:
    """(start time UTC, peak flux W/m^2) per flare from a goes-xrs-report yearly file.
    Format (NGDC xrsreadme): cols 6-11 YYMMDD, 14-17 start HHMM; class letter + peak value
    ('C 53' = C5.3, 'X172' = X17.2) further right."""
    out = []
    for line in txt.splitlines():
        m = _LINE.match(line)
        c = _CLASS.search(line[28:])
        if not m or not c:
            continue
        yy, mo, dd, hhmm = m.groups()
        year = 1900 + int(yy) if int(yy) > 70 else 2000 + int(yy)
        try:
            when = datetime(year, int(mo), int(dd), int(hhmm[:2]) % 24, int(hhmm[2:]) % 60,
                            tzinfo=timezone.utc)
        except ValueError:
            continue
        flux = CLASS_W[c.group(1)] * (int(c.group(2)) / 10.0)
        out.append((when, flux))
    return sorted(out)


def fetch_flares(tr: FlareTrigger, *, refresh: bool = False) -> Path:
    """Sun-wide >=C1 flare (t_days since the trigger X-flare start, peak flux) rows.
    t0 = start time of the LARGEST flare on the trigger date (located in the data itself)."""
    year = int(tr.date[:4])
    flares = _parse_goes(_get(NGDC.format(year=year), RAW / f"goes-xrs-report_{year}.txt",
                              refresh=refresh))
    day = datetime.fromisoformat(tr.date).replace(tzinfo=timezone.utc)
    on_day = [(when, flux) for when, flux in flares if when.date() == day.date()]
    if not on_day:
        raise RuntimeError(f"{tr.name}: no flares on trigger date {tr.date}")
    t0, peak = max(on_day, key=lambda wf: wf[1])
    if peak < 1e-4:
        raise RuntimeError(f"{tr.name}: largest flare on {tr.date} is not X-class ({peak:g})")
    horizon = t0 + timedelta(days=tr.window_days)
    rows = [((when - t0).total_seconds() / 86400.0, flux) for when, flux in flares
            if t0 < when <= horizon and flux >= tr.min_class_wm2]
    if len(rows) < 20:
        raise RuntimeError(f"{tr.name}: only {len(rows)} flares in window")
    return _write_sequence(tr.name, rows)


def fetch_all(*, refresh: bool = False) -> dict[str, str]:
    written = {}
    for ms in MAINSHOCKS:
        p = fetch_quake(ms, refresh=refresh)
        n = sum(1 for _ in p.open()) - 1
        written[ms.name] = f"{n} aftershocks ({ms.mag}, USGS ComCat) -> {p}"
        print(f"  {ms.name}: {written[ms.name]}")
    for tr in FLARE_TRIGGERS:
        p = fetch_flares(tr, refresh=refresh)
        n = sum(1 for _ in p.open()) - 1
        written[tr.name] = f"{n} flares >=C1 within {tr.window_days} d of {tr.label} -> {p}"
        print(f"  {tr.name}: {written[tr.name]}")
    return written
