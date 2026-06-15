#!/usr/bin/env python3
"""Extract per-burst sub-band arrival times from the raw PSRFITS archives.

Reads the bright single-burst archives in ``new-data/`` (PSRCHIVE .calibP /
PSRFITS .fits) and writes a tiny CSV ``data/frb01_subband_toas.csv`` that the
FRB.01 no-native-dispersion test consumes -- so the kill test is reproducible
without keeping the ~134 MB archives. Run: ``python scripts/extract_subband_toas.py``
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

import numpy as np  # noqa: E402

from frb_tfpt.dispersion import subband_toas  # noqa: E402
from frb_tfpt.psrfits import read_archive  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW_DIRS = [ROOT / "new-data", ROOT / "data" / "raw_bursts"]
OUT = ROOT / "data" / "frb01_subband_toas.csv"

# candidate single-burst archives (band -> likely source)
CANDIDATES = [
    "burst1.calibP", "burst2", "20191003_1032.calibP", "315-pulse.calibP",
    "529-pulse.calibP", "pulse1.calibP", "117pulse.calibP", "149pulse.calibP",
    "burst1 (1).calibP",
]


def _find(name: str) -> Path | None:
    for d in RAW_DIRS:
        p = d / name
        if p.exists():
            return p
    return None


def _source_label(src_name: str, fmin: float, fmax: float) -> str:
    if "190520" in src_name:
        return "FRB20190520B"
    if "20201124" in src_name:
        return "FRB20201124A"
    # placeholder PSRCHIVE name + FAST L-band 1-1.5 GHz + 2019 campaign => 121102A
    if 950 < fmin < 1100 and 1400 < fmax < 1550:
        return "FRB20121102A?"
    return src_name or "unknown"


def main() -> int:
    rows = []
    for name in CANDIDATES:
        p = _find(name)
        if p is None:
            continue
        try:
            arc = read_archive(p)
        except Exception as exc:  # noqa: BLE001
            print(f"  skip {name}: {exc}")
            continue
        f, t, e, snr = subband_toas(arc.I, arc.freqs, float(arc.tbin), n_sub=14, snr_min=6.0)
        if len(f) < 5:
            print(f"  {name}: only {len(f)} sub-bands above SNR 6 -> skip")
            continue
        label = _source_label(arc.source, float(arc.freqs.min()), float(arc.freqs.max()))
        for fi, ti, ei, si in zip(f, t, e, snr):
            rows.append([name, label, round(fi, 3), f"{ti:.6e}", f"{ei:.6e}", round(si, 1)])
        print(f"  {name:22s} [{label}] {len(f)} sub-bands "
              f"({arc.freqs.min():.0f}-{arc.freqs.max():.0f} MHz)")
    if not rows:
        print("no usable bursts found (place archives in new-data/ or data/raw_bursts/)")
        return 1
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["burst_id", "source", "freq_mhz", "toa_s", "toa_err_s", "snr"])
        w.writerows(rows)
    print(f"wrote {OUT} ({len(rows)} sub-band ToAs from "
          f"{len(set(r[0] for r in rows))} bursts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
