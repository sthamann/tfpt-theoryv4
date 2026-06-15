#!/usr/bin/env python3
"""Stream PSRCHIVE ``.ar`` waterfalls out of the big repeater archives and extend
the FRB.01 sub-band ToA table to many bursts and several sources.

The two large archives in ``new-data/`` hold thousands of single-burst dynamic
spectra:

  * ``FRB20240114A_Morphology_Public_Dataset_*.zip`` -- 2729 ``.ar`` (FRB 20240114A,
    FAST 1000-1500 MHz, 4096 ch);
  * ``FRB20201124A.tar.gz``                          -- 1863 ``.ar`` (FRB 20201124A,
    FAST 1000-1500 MHz, 512 ch).

We never unpack them to disk: each member is read in-memory (BytesIO), the burst's
sub-band arrival times are measured, and only bursts with enough high-SNR sub-bands
are kept. The result is appended to ``data/frb01_subband_toas.csv`` (the .calibP
FRB 20121102A rows written by ``extract_subband_toas.py`` are preserved), so the
cross-burst FRB.01 universality test runs on three sources without the ~14 GB raw.

Run: ``python scripts/extract_ar_toas.py``  (idempotent; rewrites the .ar rows).
"""

from __future__ import annotations

import csv
import io
import sys
import tarfile
import zipfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

import numpy as np  # noqa: E402

from frb_tfpt.dispersion import subband_toas  # noqa: E402
from frb_tfpt.psrfits import read_archive  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
NEW = ROOT / "new-data"
OUT = ROOT / "data" / "frb01_subband_toas.csv"

N_SUB = 12          # sub-bands attempted per burst
SNR_MIN = 5.5       # keep a sub-band ToA above this peak SNR
MIN_SUB = 5         # keep a burst only if it yields >= this many sub-band ToAs
MAX_KEEP = 150      # cap bursts kept per source (keeps the CSV small + balanced)


def _rows_from_archive(data: bytes, member: str, source: str):
    """Read one .ar from raw bytes, return CSV rows or None."""
    try:
        arc = read_archive(io.BytesIO(data), name=member)
    except Exception:  # noqa: BLE001  -- corrupt/odd member: skip silently
        return None
    f, t, e, snr = subband_toas(arc.I, arc.freqs, float(arc.tbin),
                                n_sub=N_SUB, snr_min=SNR_MIN)
    if len(f) < MIN_SUB:
        return None
    bid = Path(member).stem
    return [[bid, source, round(float(fi), 3), f"{ti:.6e}", f"{ei:.6e}", round(float(si), 1)]
            for fi, ti, ei, si in zip(f, t, e, snr)]


def _scan_zip(path: Path, source: str):
    rows, kept, seen = [], 0, 0
    with zipfile.ZipFile(path) as zf:
        members = sorted(n for n in zf.namelist() if n.endswith(".ar"))
        if not members:
            return rows, 0
        stride = max(1, len(members) // (MAX_KEEP * 4))   # spread across the dataset
        for m in members[::stride]:
            seen += 1
            r = _rows_from_archive(zf.read(m), m, source)
            if r:
                rows.extend(r)
                kept += 1
                if kept >= MAX_KEEP:
                    break
    print(f"  {path.name}: scanned {seen}, kept {kept} bursts ({len(rows)} sub-band ToAs)")
    return rows, kept


def _scan_tar(path: Path, source: str):
    rows, kept, seen = [], 0, 0
    with tarfile.open(path, "r:gz") as tf:
        idx = 0
        for m in tf:
            if not m.name.endswith(".ar"):
                continue
            idx += 1
            if idx % 3:                      # stride: every 3rd burst across the campaign
                continue
            seen += 1
            fh = tf.extractfile(m)
            if fh is None:
                continue
            r = _rows_from_archive(fh.read(), m.name, source)
            if r:
                rows.extend(r)
                kept += 1
                if kept >= MAX_KEEP:
                    break
    print(f"  {path.name}: scanned {seen}, kept {kept} bursts ({len(rows)} sub-band ToAs)")
    return rows, kept


def _existing_calibp_rows():
    """Keep already-written rows that did NOT come from the two .ar sources."""
    if not OUT.exists():
        return []
    keep = []
    with open(OUT, newline="") as fh:
        rd = csv.reader(fh)
        header = next(rd, None)
        for row in rd:
            if len(row) >= 2 and row[1] not in ("FRB20240114A", "FRB20201124A"):
                keep.append(row)
    return keep


def main() -> int:
    ar_rows = []
    zip114 = next(NEW.glob("FRB20240114A_Morphology_Public_Dataset_*.zip"), None)
    tar124 = NEW / "FRB20201124A.tar.gz"
    if zip114 and zip114.exists():
        r, _ = _scan_zip(zip114, "FRB20240114A")
        ar_rows += r
    else:
        print("  (FRB20240114A morphology zip not found in new-data/)")
    if tar124.exists():
        r, _ = _scan_tar(tar124, "FRB20201124A")
        ar_rows += r
    else:
        print("  (FRB20201124A.tar.gz not found in new-data/)")
    if not ar_rows:
        print("no .ar bursts extracted")
        return 1
    rows = _existing_calibp_rows() + ar_rows
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["burst_id", "source", "freq_mhz", "toa_s", "toa_err_s", "snr"])
        w.writerows(rows)
    nb = len({(r[0], r[1]) for r in rows})
    ns = len({r[1] for r in rows})
    print(f"wrote {OUT} ({len(rows)} sub-band ToAs from {nb} bursts across {ns} sources)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
