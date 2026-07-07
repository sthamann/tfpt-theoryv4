#!/usr/bin/env python3
"""Fetch the Auger Open Data release-3 summary CSVs (Zenodo DOI, ~8 MB).

Re-creates data/summary/dataSummarySD1500.csv + dataSummarySD750.csv (+ inclined).
"""

import io
import urllib.request
import zipfile
from pathlib import Path

URL = "https://zenodo.org/records/10488964/files/summary.zip?download=1"
DATA = Path(__file__).resolve().parents[1] / "data"


def main() -> None:
    DATA.mkdir(exist_ok=True)
    print(f"fetching {URL} ...")
    buf = urllib.request.urlopen(URL, timeout=120).read()
    with zipfile.ZipFile(io.BytesIO(buf)) as z:
        z.extractall(DATA)
    for f in sorted((DATA / "summary").glob("*.csv")):
        print(" ", f.name, f.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
