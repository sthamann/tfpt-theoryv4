"""Fetch the public NICER event files for ObsID 3020560101 (SGR 1935+2154,
2020-04-28 burst storm) from the HEASARC archive into data/nicer/
(gitignored; documented in hypotheses/parity_comb_v1.2_nicer.yaml)."""
import urllib.request
from pathlib import Path

BASE = ("https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/2020_04/"
        "3020560101/xti/event_cl/")
FILES = ["ni3020560101_0mpu7_cl.evt.gz", "ni3020560101_0mpu7_ufa.evt.gz"]
DEST = Path(__file__).resolve().parents[1] / "data" / "nicer"

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
