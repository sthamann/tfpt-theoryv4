#!/usr/bin/env python3
"""Download + parse the Yu+2013 post-glitch recovery table -> ``data/yu2013_recovery.csv``.

Yu et al. 2013, MNRAS 429, 688 ("Detection of 107 glitches in 36 southern
pulsars", arXiv:1211.2035) compiles, in its ``expTab.tex``, the *exponential
recovery* parameters (healing fraction ``Q`` and decay timescale ``tau_d``, with
the multi-component decays of Vela/Crab) and the originating reference per glitch.
That is exactly the ``Q``/``tau_d`` set the Jodrell Bank size catalogue lacks
(PG.04 in `problem_1.txt`).

Run from anywhere:  ``python scripts/fetch_recovery.py``

The raw e-print tarball (~2.4 MB) is gitignored; only the small derived
``data/yu2013_recovery.csv`` is committed.  Cite Yu et al. 2013 and the per-row
original references (in the CSV) when using these data.
"""

from __future__ import annotations

import io
import sys
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tfpt_pulsar.catalog import (  # noqa: E402
    DATA,
    RECOVERY_CSV,
    parse_yu2013_recovery,
    write_recovery_csv,
)

URL = "https://arxiv.org/e-print/1211.2035"
UA = "Mozilla/5.0 (compatible; tfpt-pulsar/0.1; research)"


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    print(f"fetching {URL} ...")
    req = urllib.request.Request(URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:  # noqa: S310
        blob = r.read()
    print(f"  got e-print tarball ({len(blob)} bytes)")

    tex = None
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tf:
        member = next((m for m in tf.getmembers() if m.name.endswith("expTab.tex")), None)
        if member is None:
            print("  ERROR: expTab.tex not found in the e-print", file=sys.stderr)
            return 1
        tex = tf.extractfile(member).read().decode("utf-8", errors="replace")

    records = parse_yu2013_recovery(tex)
    write_recovery_csv(records)
    n_q = sum(1 for r in records if r.Q is not None)
    n_tau = sum(1 for r in records if r.tau_d is not None)
    n_glitch = len({(r.psr_j, r.epoch_mjd) for r in records})
    print(f"  parsed {len(records)} recovery components across {n_glitch} glitches "
          f"({n_q} with Q, {n_tau} with tau_d)")
    print(f"  wrote {RECOVERY_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
