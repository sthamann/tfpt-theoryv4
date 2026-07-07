#!/usr/bin/env python3
"""Fetch the KIT4 open 2D EIT archive (Zenodo record 1203914, CC BY 4.0).

Downloads data_mat_files.zip (~24 MB: 38 MATLAB files datamat_X_Y.mat with Uel 16x79,
CurrentPattern 16x79, MeasPattern 16x16) and unpacks it into data/mat/.  Photos
(target_photos.zip) are NOT fetched by default (not needed for the analysis; the case
geometry is documented in arXiv:1704.01178).

Provenance: Hauptmann, Kolehmainen, Mach, Savolainen, Seppanen, Siltanen,
"Open 2D Electrical Impedance Tomography data archive", arXiv:1704.01178;
data DOI 10.5281/zenodo.1203914.
"""
from __future__ import annotations

import io
import sys
import urllib.request
import zipfile
from pathlib import Path

BASE = "https://zenodo.org/records/1203914/files"
DATA = Path(__file__).resolve().parents[1] / "data"
UA = {"User-Agent": "tfpt-qgeo-eit-soff/1.0 (open-data fetch)"}


def fetch(name: str) -> bytes:
    url = f"{BASE}/{name}?download=1"
    print(f"  fetching {url}")
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=300) as r:  # noqa: S310
        return r.read()


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    mat_dir = DATA / "mat"
    if mat_dir.exists() and any(mat_dir.glob("*.mat")):
        print(f"already present: {len(list(mat_dir.glob('*.mat')))} .mat files in {mat_dir}")
        return 0
    blob = fetch("data_mat_files.zip")
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        mat_dir.mkdir(exist_ok=True)
        for info in z.infolist():
            name = Path(info.filename).name
            # skip macOS resource forks (__MACOSX/._*.mat) shipped inside the archive
            if name.endswith(".mat") and not name.startswith("._"):
                (mat_dir / name).write_bytes(z.read(info))
    n = len(list(mat_dir.glob("*.mat")))
    print(f"unpacked {n} .mat files -> {mat_dir}")
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main())
