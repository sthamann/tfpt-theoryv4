#!/usr/bin/env python3
"""PG.06b FULL: bulk-download the complete NICER Vela L2 archive (manifest-frozen).

Reads data/nicer_vela/manifest_full_reduction.json (frozen BEFORE this download),
pulls every observation's cleaned L2 event file + orbit file from the HEASARC
archive with retry/backoff, and writes a resumable download log. Raw files land in
data/nicer_vela/raw/ (gitignored via the data/nicer_vela/* rule -- only the small
derived CSV/JSON products are whitelisted).

Usage:  python scripts/download_vela_all.py [--threads 8] [--retries 3]
Resumable: existing files are skipped; rerun after interruption.
Abort gate: stops if the cumulative download exceeds the manifest's abort_gate_gb.
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "nicer_vela"
RAW = DATA / "raw"
MANIFEST = DATA / "manifest_full_reduction.json"
LOG = DATA / "download_log_full.json"
UA = "tfpt-pulsar/0.1 (research)"

_lock = Lock()
_bytes_total = 0


def _fetch(url: str, out: Path, retries: int) -> tuple[bool, int, str]:
    """Download one gz file, decompress to `out`. Returns (ok, bytes, error)."""
    global _bytes_total
    if out.exists() and out.stat().st_size > 0:
        return True, 0, "cached"
    last = ""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=300) as r:  # noqa: S310
                blob = r.read()
            data = gzip.decompress(blob)
            tmp = out.with_suffix(out.suffix + ".part")
            tmp.write_bytes(data)
            tmp.rename(out)
            with _lock:
                _bytes_total += len(blob)
            return True, len(blob), ""
        except Exception as exc:  # noqa: BLE001
            last = repr(exc)
            time.sleep(2.0 * (attempt + 1))
    return False, 0, last


def _one_obs(o: dict, retries: int) -> dict:
    evt = RAW / f"ni{o['obsid']}_cl.evt"
    orb = RAW / f"ni{o['obsid']}.orb"
    ok_e, b_e, err_e = _fetch(o["evt_url"], evt, retries)
    ok_o, b_o, err_o = _fetch(o["orb_url"], orb, retries)
    return {"obsid": o["obsid"], "evt_ok": ok_e, "orb_ok": ok_o,
            "bytes": b_e + b_o, "err": (err_e or err_o)}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--retries", type=int, default=3)
    args = ap.parse_args(argv)

    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    gate_gb = float(man["abort_gate_gb"])
    obs = man["observations"]
    RAW.mkdir(parents=True, exist_ok=True)
    print(f"manifest: {len(obs)} obs, est {man['estimated_download_gb']} GB "
          f"(abort gate {gate_gb} GB); {args.threads} threads, {args.retries} retries")

    results, t0 = [], time.time()
    with ThreadPoolExecutor(max_workers=args.threads) as ex:
        futs = {ex.submit(_one_obs, o, args.retries): o["obsid"] for o in obs}
        for i, fut in enumerate(as_completed(futs)):
            r = fut.result()
            results.append(r)
            gb = _bytes_total / 1e9
            if gb > gate_gb:
                print(f"ABORT GATE: {gb:.1f} GB > {gate_gb} GB -- stopping")
                for f in futs:
                    f.cancel()
                break
            if (i + 1) % 25 == 0 or not (r["evt_ok"] and r["orb_ok"]):
                rate = _bytes_total / max(1.0, time.time() - t0) / 1e6
                status = "ok" if (r["evt_ok"] and r["orb_ok"]) else f"FAIL {r['err']}"
                print(f"  [{i+1}/{len(obs)}] {r['obsid']}: {status}  "
                      f"(cum {gb:.2f} GB, {rate:.1f} MB/s)", flush=True)

    n_ok = sum(1 for r in results if r["evt_ok"] and r["orb_ok"])
    n_fail = [r["obsid"] for r in results if not (r["evt_ok"] and r["orb_ok"])]
    log = {"finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "n_requested": len(obs), "n_ok": n_ok, "failed_obsids": n_fail,
           "bytes_downloaded": _bytes_total, "elapsed_s": round(time.time() - t0, 1)}
    LOG.write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"\nDONE: {n_ok}/{len(obs)} ok, {len(n_fail)} failed, "
          f"{_bytes_total/1e9:.2f} GB in {log['elapsed_s']:.0f}s -> {LOG}")
    return 0 if not n_fail else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
