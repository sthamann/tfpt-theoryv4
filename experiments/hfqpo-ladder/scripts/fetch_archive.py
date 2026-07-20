#!/usr/bin/env python3
"""Download the PCA high-time-resolution files for every ObsID in the frozen
manifest (data/archive/obsid_manifest.json) from the public HEASARC archive.

- Only science files usable for HFQPO work are fetched: FS3*/FS4f (event,
  binned, single-bit) and processed SE*.evt.gz event files. Standard1/2
  (FS46/FS4a) and housekeeping (FH*) are skipped.
- Abort gate: if the running total exceeds MAX_GB the script stops and
  records the fact (prereg rescope rule).
- Idempotent: files already on disk with the right size are not re-fetched.
"""
import json
import os
import re
import subprocess
import sys
import time
from html.parser import HTMLParser
from urllib.request import urlopen

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ARCH = os.path.join(ROOT, "data", "archive")
RAW = os.path.join(ARCH, "raw")
MANIFEST = os.path.join(ARCH, "obsid_manifest.json")
LOG = os.path.join(ARCH, "download_log.json")
BASE = "https://heasarc.gsfc.nasa.gov/FTP/rxte/data/archive"
MAX_GB = 30.0

AO_BY_PREFIX = {"1": "AO1", "2": "AO2", "3": "AO3", "4": "AO4",
                "5": "AO5", "6": "AO6", "7": "AO7", "8": "AO8", "9": "AO9"}

WANT = re.compile(r"^(FS3[0-9a-f]|FS4f|SE[0-9a-f]?)_.*\.(gz|evt\.gz)$", re.I)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v and not v.startswith("?") and not v.startswith("/"):
                    self.links.append(v)


def list_dir(url, retries=4):
    for i in range(retries):
        try:
            with urlopen(url, timeout=40) as r:
                html = r.read().decode("utf-8", "replace")
            p = LinkParser()
            p.feed(html)
            return p.links
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(3 * (i + 1))


def fetch(url, dest, retries=4):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for i in range(retries):
        rc = subprocess.run(
            ["curl", "-s", "-f", "--retry", "3", "--max-time", "600",
             "-o", dest + ".part", url]).returncode
        if rc == 0 and os.path.getsize(dest + ".part") > 0:
            os.replace(dest + ".part", dest)
            return True
        time.sleep(3 * (i + 1))
    if os.path.exists(dest + ".part"):
        os.remove(dest + ".part")
    return False


def main():
    shard_k, shard_n = 0, 1
    if len(sys.argv) == 3:
        shard_k, shard_n = int(sys.argv[1]), int(sys.argv[2])
    log_path = LOG if shard_n == 1 else LOG.replace(".json", f".shard{shard_k}.json")
    with open(MANIFEST) as f:
        manifest = json.load(f)
    log = {"files": {}, "errors": [], "total_bytes": 0, "aborted_over_gate": False}
    if os.path.exists(log_path):
        with open(log_path) as f:
            log = json.load(f)

    obs_jobs = []
    for sname, s in manifest["sources"].items():
        for gname, g in s["groups"].items():
            for obsid in g.get("obsids", []):
                obs_jobs.append((sname, gname, obsid))
    # de-duplicate obsids (an obsid may appear in one group only, but be safe)
    seen = set()
    jobs = []
    for j in obs_jobs:
        if j[2] not in seen:
            seen.add(j[2])
            jobs.append(j)
    jobs = [j for i, j in enumerate(jobs) if i % shard_n == shard_k]

    total = log.get("total_bytes", 0)
    for k, (sname, gname, obsid) in enumerate(jobs):
        prop = "P" + obsid.split("-")[0]
        ao = AO_BY_PREFIX[obsid[0]]
        files = None
        for od in (obsid, obsid + "G"):
            url = f"{BASE}/{ao}/{prop}/{od}/pca/"
            try:
                files = [l for l in list_dir(url) if WANT.match(l)]
                break
            except Exception as e:
                err = str(e)
        if files is None:
            log["errors"].append({"obsid": obsid, "stage": "list", "err": err})
            print(f"[{k+1}/{len(jobs)}] {obsid}: LIST FAILED {err}", flush=True)
            continue
        got = 0
        for fn in files:
            dest = os.path.join(RAW, obsid, fn)
            key = f"{obsid}/{fn}"
            if key in log["files"] and os.path.exists(dest):
                got += 1
                continue
            if total / 1e9 > MAX_GB:
                log["aborted_over_gate"] = True
                break
            ok = fetch(url + fn, dest)
            if ok:
                sz = os.path.getsize(dest)
                total += sz
                log["files"][key] = {"bytes": sz, "source": sname, "group": gname}
                got += 1
            else:
                log["errors"].append({"obsid": obsid, "stage": "fetch", "file": fn})
        log["total_bytes"] = total
        with open(log_path, "w") as f:
            json.dump(log, f, indent=1)
        print(f"[{k+1}/{len(jobs)}] {obsid} ({sname}/{gname}): {got}/{len(files)} files, "
              f"cum {total/1e9:.2f} GB", flush=True)
        if log["aborted_over_gate"]:
            print("ABORT GATE: exceeded MAX_GB - rescope per prereg", flush=True)
            break
    print(f"DONE total={total/1e9:.2f} GB errors={len(log['errors'])}", flush=True)


if __name__ == "__main__":
    main()
