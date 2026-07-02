"""Fetch the PRIMARY dataset: Michon et al. 2023 open data (LSCO x=0.24 optical spectra).

Source: Michon, B. et al., "Open data to 'Reconciling scaling of the optical conductivity of
cuprate superconductors with Planckian resistivity and specific heat', Nature Communications 14,
3033 (2023)", Yareta (University of Geneva), DOI 10.26037/yareta:zvtvqwmbl5emvd3bxr6sluurqi.
License: CC-BY-4.0 (per the archive's DataCite record).

The archive (a 1.4 MB BagIt zip, 81 files) contains the measured complex dielectric function of
La(2-x)Sr(x)CuO4 at x=0.24 -- ``experimental-data/Epsilon_LSCO-0p24.txt``: energy 2.5 meV..5 eV
(1465 rows) x 13 temperatures T=[9,15,20,30,40,50,60,75,100,150,200,250,300] K, columns
(E, eps1_T, eps2_T, ...). The real optical conductivity is sigma1 = eps0*omega*eps2, i.e.
sigma1[kS/cm] = 0.134518794412 * E[eV] * eps2 (the conversion used by the paper's own fig02 code).
Also copied: the representative error-bar table and the dc resistivity (provenance/context).

Download protocol (Yareta DLCM access API):
  1. POST  {API}/access/metadata/{ID}/prepare-download   (202; server assembles the package)
  2. GET   {API}/access/metadata/{ID}/download           (200; BagIt zip)

Usage:  python scripts/fetch_michon2023.py
"""

from __future__ import annotations

import io
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

ARCHIVE_ID = "36702b55-5945-4bf9-8298-b06506ef89fb"   # resolves from the Yareta DOI
API = "https://access.yareta.unige.ch/access/metadata/" + ARCHIVE_ID
DOI = "10.26037/yareta:zvtvqwmbl5emvd3bxr6sluurqi"
PAPER = "Michon et al., Nat. Commun. 14, 3033 (2023), doi:10.1038/s41467-023-38762-5"
DATA = Path(__file__).resolve().parents[1] / "data"

WANTED = {
    "researchdata/for-yareta/experimental-data/Epsilon_LSCO-0p24.txt":
        "lsco_x0p24_epsilon.txt",
    "researchdata/for-yareta/experimental-data/error_bars.txt":
        "lsco_x0p24_error_bars.txt",
    "researchdata/for-yareta/experimental-data/Rho_LSCO-0p24_H0T.txt":
        "lsco_x0p24_rho_H0T.txt",
}


def _request(url: str, method: str = "GET") -> bytes:
    req = urllib.request.Request(url, method=method,
                                 headers={"User-Agent": "tfpt-smc-fetch/0.1"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def main() -> int:
    DATA.mkdir(exist_ok=True)
    print(f"POST prepare-download ({DOI}) ...")
    _request(API + "/prepare-download", method="POST")
    blob = b""
    for attempt in range(6):
        time.sleep(3 + 2 * attempt)
        try:
            blob = _request(API + "/download")
            if blob[:2] == b"PK":
                break
        except OSError as exc:
            print(f"  attempt {attempt + 1}: {exc}")
    if blob[:2] != b"PK":
        print("FAILED: could not retrieve the Yareta zip.")
        return 1
    print(f"downloaded {len(blob)} bytes")
    zf = zipfile.ZipFile(io.BytesIO(blob))
    header = (f"# Source: {PAPER}\n"
              f"# Open data: Yareta (University of Geneva), DOI {DOI} (CC-BY-4.0)\n"
              f"# Archive member: {{member}}\n"
              f"# Fetched by scripts/fetch_michon2023.py; content below is verbatim.\n")
    for member, out_name in WANTED.items():
        raw = zf.read(member).decode("utf-8")
        out = DATA / out_name
        out.write_text(header.format(member=member) + raw, encoding="utf-8")
        print(f"  wrote {out}  ({len(raw.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
