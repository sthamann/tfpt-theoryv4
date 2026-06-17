#!/usr/bin/env python3
"""Download + parse the Jodrell Bank Glitch Catalogue into ``data/jbo_glitches.csv``.

Run from anywhere:  ``python scripts/fetch_glitches.py``

The raw ``gTable.html`` (~1.8 MB) is gitignored; only the small derived CSV
(``data/jbo_glitches.csv``) is committed so the analysis reproduces without the
download.  See ``data/README.md`` for the citation.
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tfpt_pulsar.catalog import DATA, DERIVED_CSV, parse_jbo_html, write_csv  # noqa: E402

URL = "https://www.jb.man.ac.uk/pulsar/glitches/gTable.html"
RAW = DATA / "gTable.html"
UA = "Mozilla/5.0 (compatible; tfpt-pulsar/0.1; research)"


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    print(f"fetching {URL} ...")
    req = urllib.request.Request(URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:  # noqa: S310
        html = r.read().decode("utf-8", errors="replace")
    RAW.write_text(html, encoding="utf-8")
    print(f"  wrote {RAW.name} ({len(html)} bytes)")

    records = parse_jbo_html(html)
    write_csv(records)
    n_pulsars = len({r.jname for r in records})
    n_sizes = sum(1 for r in records if r.df_f is not None)
    print(f"  parsed {len(records)} glitches across {n_pulsars} pulsars "
          f"({n_sizes} with dF/F)")
    print(f"  wrote {DERIVED_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
