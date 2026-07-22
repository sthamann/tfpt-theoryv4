#!/usr/bin/env python3
"""Download the NICER cleaned event files listed in the frozen manifest.

- Only obsids with triage == 'selected' are fetched (data/manifest_ext.json).
- Hard abort gate at BUDGET_GB cumulative downloaded bytes (prereg rule).
- Idempotent: files already on disk with the expected size are skipped.

Output: data/raw/<obsid>/ni<obsid>_0mpu7_cl.evt.gz + data/download_log_ext.json
"""
import json
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MANIFEST = os.path.join(ROOT, "data", "manifest_ext.json")
RAW = os.path.join(ROOT, "data", "raw")
LOG = os.path.join(ROOT, "data", "download_log_ext.json")
BUDGET_GB = 15.0


N_STREAMS = 12    # HEASARC caps ~1 MB/s per stream; ranges are supported


def _fetch_range(url, dest_part, a, b, retries=4):
    for i in range(retries):
        rc = subprocess.run(
            ["curl", "-s", "-f", "--retry", "3", "--max-time", "3600",
             "-H", f"Range: bytes={a}-{b}", "-o", dest_part, url]).returncode
        if rc == 0 and os.path.getsize(dest_part) == b - a + 1:
            return True
        time.sleep(5 * (i + 1))
    return False


def fetch(url, dest, expect_bytes):
    """Parallel range download: N_STREAMS contiguous chunks, then concatenate."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    chunk = expect_bytes // N_STREAMS + 1
    jobs = []
    for k in range(N_STREAMS):
        a = k * chunk
        b = min((k + 1) * chunk - 1, expect_bytes - 1)
        if a > b:
            continue
        part = f"{dest}.part{k}"
        if os.path.exists(part) and os.path.getsize(part) == b - a + 1:
            jobs.append((k, part, None))
            continue
        p = subprocess.Popen(
            ["curl", "-s", "-f", "--retry", "3", "--max-time", "3600",
             "-H", f"Range: bytes={a}-{b}", "-o", part, url])
        jobs.append((k, part, (p, a, b)))
    ok = True
    for k, part, j in jobs:
        if j is None:
            continue
        p, a, b = j
        p.wait()
        if not (os.path.exists(part) and os.path.getsize(part) == b - a + 1):
            ok = _fetch_range(url, part, a, b)
            if not ok:
                break
    if ok:
        with open(dest + ".part", "wb") as out:
            for k, part, _ in sorted(jobs):
                with open(part, "rb") as f:
                    while True:
                        buf = f.read(1 << 24)
                        if not buf:
                            break
                        out.write(buf)
        if os.path.getsize(dest + ".part") == expect_bytes:
            os.replace(dest + ".part", dest)
            for k, part, _ in jobs:
                os.remove(part)
            return True
    if os.path.exists(dest + ".part"):
        os.remove(dest + ".part")
    return False


def main():
    with open(MANIFEST) as f:
        manifest = json.load(f)
    log = {"files": {}, "errors": [], "total_bytes": 0,
           "aborted_over_gate": False}
    if os.path.exists(LOG):
        with open(LOG) as f:
            log = json.load(f)
    total = log.get("total_bytes", 0)
    rows = [r for r in manifest["files"] if r.get("triage") == "selected"]
    for k, r in enumerate(rows):
        obsid, url, expect = r["obsid"], r["url"], r["bytes"]
        dest = os.path.join(RAW, obsid, os.path.basename(url))
        if os.path.exists(dest) and os.path.getsize(dest) == expect:
            log["files"][obsid] = {"bytes": expect, "status": "cached"}
            print(f"[{k+1}/{len(rows)}] {obsid} cached "
                  f"({expect/1e9:.2f} GB)", flush=True)
            continue
        if (total + expect) / 1e9 > BUDGET_GB:
            log["aborted_over_gate"] = True
            print(f"ABORT GATE: {obsid} would exceed {BUDGET_GB} GB", flush=True)
            break
        t0 = time.time()
        ok = fetch(url, dest, expect)
        if ok:
            sz = os.path.getsize(dest)
            total += sz
            log["files"][obsid] = {"bytes": sz, "status": "fetched",
                                   "seconds": round(time.time() - t0, 1)}
            print(f"[{k+1}/{len(rows)}] {obsid} {sz/1e9:.2f} GB in "
                  f"{time.time()-t0:.0f}s, cum {total/1e9:.2f} GB", flush=True)
        else:
            log["errors"].append({"obsid": obsid, "url": url})
            print(f"[{k+1}/{len(rows)}] {obsid} FETCH FAILED", flush=True)
        log["total_bytes"] = total
        with open(LOG, "w") as f:
            json.dump(log, f, indent=1)
    with open(LOG, "w") as f:
        json.dump(log, f, indent=1)
    print(f"DONE total={total/1e9:.2f} GB errors={len(log['errors'])}",
          flush=True)


if __name__ == "__main__":
    main()
