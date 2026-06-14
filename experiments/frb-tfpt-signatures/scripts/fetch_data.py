#!/usr/bin/env python3
"""Re-download the two real FRB datasets from VizieR into ``data/``.

Run from anywhere:  ``python scripts/fetch_data.py``

Both queries hit the CDS VizieR ``asu-tsv`` service, which returns a
tab-separated table with a ``#``-comment header (the loader in ``data_io.py``
parses exactly this format).  See ``data/README.md`` for citations.
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
VIZIER = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv"
UA = "Mozilla/5.0 (compatible; tfpt-frb/0.2; research)"

# VizieR ASU-TSV catalogues
VIZIER_SOURCES = {
    # CHIME/FRB Catalogue 1 (CHIME/FRB Collaboration 2021, ApJS 257, 59), 600 bursts
    "chime_catalog1.tsv": "?-source=J/ApJS/257/59/table2&-out.all&-out.max=unlimited",
    # FRB 20121102A burst components (Aggarwal et al. 2021, ApJ 922, 115), 144 bursts
    "frb20121102_aggarwal2021.tsv": "?-source=J/ApJ/922/115/table5&-out.all&-out.max=unlimited",
}

# IOPscience machine-readable supplements (localized-FRB DM-z + polarimetry)
IOP_SOURCES = {
    # localized FRBs, full DM budget (ApJ 10.3847/1538-4357/adb84d, Table A1)
    "frb_dmz_adb84d_table4.txt":
        "https://iopscience.iop.org/0004-637X/982/2/203/suppdata/apjadb84dt4_ascii.txt"
        "?doi=10.3847%2F1538-4357%2Fadb84d",
    # Sharma et al. 2024 host sample (ApJ 10.3847/1538-4357/adeb72, Table 1)
    "frb_dmz_adeb72_table1.txt":
        "https://iopscience.iop.org/0004-637X/989/1/77/suppdata/apjadeb72t1_ascii.txt"
        "?doi=10.3847%2F1538-4357%2Fadeb72",
    # Pandhi et al. 2024 CHIME non-repeater polarimetry (ApJ 968, 50, Table 1)
    "frb_pol_pandhi2024_table1.txt":
        "https://iopscience.iop.org/0004-637X/968/2/50/suppdata/apjad40aat1_ascii.txt"
        "?doi=10.3847%2F1538-4357%2Fad40aa",
}


def _fetch(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:  # noqa: S310
        data = r.read()
    dest.write_bytes(data)
    print(f"  wrote {dest.name} ({len(data)} bytes)")


def main() -> int:
    DATA.mkdir(exist_ok=True)
    for fname, query in VIZIER_SOURCES.items():
        print(f"fetching {fname} (VizieR) ...")
        _fetch(VIZIER + query, DATA / fname)
    for fname, url in IOP_SOURCES.items():
        print(f"fetching {fname} (IOPscience) ...")
        _fetch(url, DATA / fname)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
