"""Fetch the public IXPE Level-2 event lists for ObsID 03250499 (1E 1841-045
post-outburst ToO) from the HEASARC archive into data/ixpe/ (gitignored --
~23 MB total; documented in hypotheses/parity_comb_v1.1_ixpe.yaml)."""
import urllib.request
from pathlib import Path

BASE = ("https://heasarc.gsfc.nasa.gov/FTP/ixpe/data/obs/03/03250499/event_l2/")
FILES = [f"ixpe03250499_det{d}_evt2_v01.fits.gz" for d in (1, 2, 3)]
DEST = Path(__file__).resolve().parents[1] / "data" / "ixpe"

if __name__ == "__main__":
    DEST.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        out = DEST / f
        if out.exists():
            print("have", f)
            continue
        print("fetching", f, "...")
        urllib.request.urlretrieve(BASE + f, out)
        print("  ->", out.stat().st_size, "bytes")
