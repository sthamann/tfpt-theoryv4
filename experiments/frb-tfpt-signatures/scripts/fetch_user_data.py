#!/usr/bin/env python3
"""Fetch user-supplied FRB tables (Blinkverse + ScienceDB pol catalog).

Run from repo:  python scripts/fetch_user_data.py

Blinkverse: public REST export (no login).
ScienceDB FRB 20240114A pol: login-walled — drop FAST_FRB20240114A_pol_catalog_v5.csv
into data/ after a free ScienceDB account download (DOI 10.57760/sciencedb.Fastro.00040).
Optional: set SCIENCEDB_COOKIE env var (browser session cookie) to attempt API download.
"""

from __future__ import annotations

import csv
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
UA = "Mozilla/5.0 (compatible; tfpt-frb/0.3; research)"

BLINKVERSE_SOURCES = (
    "FRB20121102A",
    "FRB20201124A",
    "FRB20220912A",
    "FRB20230607A",
    "FRB20240114A",
)
BLINKVERSE_DL = (
    "https://blinkverse.zero2x.org/api/app/adcp-blinkverse/type/FRB_ANALYSIS_SINGLE/download"
)
BLINKVERSE_API = (
    "https://blinkverse.zero2x.org/api/app/adcp-blinkverse/type/FRB_ANALYSIS_SINGLE"
)
BV_COLMAP = {
    "Source": "source",
    "MJD_topo": "mjd",
    "MJD": "mjd",
    "Energy": "energy",
    "Fluence": "fluence",
    "RM_QUfit": "rm_qufit",
    "RM_syn": "rm_syn",
    "Polar_l": "polar_l",
    "Polar_c": "polar_c",
    "Width": "width",
    "DM_SNR": "dm_snr",
    "DM_alig": "dm_alig",
}
BV_FIELDS = list(BV_COLMAP.values())

SCIENCE_DB_ID = "3fe21485a0b84f328f63a5ca8807b3e5"
SCIENCE_DB_FILE = "a65b9e11b533f53b657838a1a4d253c1"
POL_OUT_NAMES = (
    "FAST_FRB20240114A_pol_catalog_v5.csv",
    "FAST_FRB20240114A_pol_catalog.csv",
    "frb20240114A_fast_pol_catalog.tsv",
)


def _get(url: str, headers: dict | None = None, binary: bool = False, timeout: int = 300):
    h = {"User-Agent": UA, **(headers or {})}
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if binary else r.read().decode("utf-8", errors="replace")


def _norm_bv_row(row: dict, src: str) -> dict:
    out = {f: "" for f in BV_FIELDS}
    for k, v in row.items():
        key = BV_COLMAP.get((k or "").strip())
        if key and v not in (None, "", "null", "NULL"):
            out[key] = v
    if not out["source"]:
        out["source"] = src
    return out


def fetch_blinkverse_csv(source: str) -> list[dict]:
    q = urllib.parse.urlencode(
        {
            "data_name": source,
            "telescopes": "",
            "start_date": "",
            "end_date": "",
            "gl": "",
            "gb": "",
            "radius": "",
            "data_sub_types": "",
        }
    )
    text = _get(f"{BLINKVERSE_DL}?{q}", timeout=300)
    rows = []
    for row in csv.DictReader(io.StringIO(text)):
        r = _norm_bv_row(row, source)
        if r["mjd"] or r["fluence"] or r["energy"]:
            rows.append(r)
    return rows


def fetch_blinkverse_page(source: str, page: int, page_size: int = 100) -> tuple[list[dict], int]:
    q = urllib.parse.urlencode(
        {"page": page, "page_size": page_size, "data_sub_types": "", "data_name": source}
    )
    for attempt in range(6):
        try:
            payload = json.loads(_get(f"{BLINKVERSE_API}?{q}", timeout=120))
            break
        except urllib.error.HTTPError as e:
            if e.code >= 500 and attempt < 5:
                time.sleep(2 * (attempt + 1))
                continue
            raise
    data = payload["data"]
    total = int(data["total_info"]["total_count"])
    rows = []
    for item in data["list"]:
        c = item.get("content") or {}
        mjd = c.get("mjd_topo") or c.get("mjd") or c.get("mjd_inf")
        rows.append(
            {
                "source": c.get("source") or item.get("name") or source,
                "mjd": "" if mjd is None else mjd,
                "energy": "" if c.get("energy") is None else c.get("energy"),
                "fluence": "" if c.get("fluence") is None else c.get("fluence"),
                "rm_qufit": "" if c.get("rm_qufit") is None else c.get("rm_qufit"),
                "rm_syn": "" if c.get("rm_syn") is None else c.get("rm_syn"),
                "polar_l": "" if c.get("polar_l") is None else c.get("polar_l"),
                "polar_c": "" if c.get("polar_c") is None else c.get("polar_c"),
                "width": "" if c.get("width") is None else c.get("width"),
                "dm_snr": "" if c.get("dm_snr") is None else c.get("dm_snr"),
                "dm_alig": "" if c.get("dm_alig") is None else c.get("dm_alig"),
            }
        )
    return rows, total


def fetch_blinkverse_source(source: str) -> list[dict]:
    try:
        rows = fetch_blinkverse_csv(source)
        print(f"  {source}: {len(rows)} rows (CSV export)")
        return rows
    except urllib.error.HTTPError as e:
        if e.code < 500:
            raise
    rows: list[dict] = []
    page = 1
    total = None
    while True:
        chunk, total = fetch_blinkverse_page(source, page)
        if not chunk:
            break
        rows.extend(chunk)
        print(f"  {source}: page {page} -> {len(rows)}/{total}")
        if len(rows) >= total or len(chunk) < 100:
            break
        page += 1
        time.sleep(0.7)
    return rows


def fetch_blinkverse() -> Path:
    out = DATA / "blinkverse_bursts.csv"
    DATA.mkdir(exist_ok=True)
    all_rows: list[dict] = []
    for src in BLINKVERSE_SOURCES:
        print(f"fetching Blinkverse {src} ...")
        all_rows.extend(fetch_blinkverse_source(src))
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=BV_FIELDS)
        w.writeheader()
        w.writerows(all_rows)
    print(f"  wrote {out.name} ({len(all_rows)} rows, {out.stat().st_size} bytes)")
    return out


def fetch_sciencedb_pol() -> Path | None:
    for name in POL_OUT_NAMES:
        if (DATA / name).exists() and (DATA / name).stat().st_size > 1000:
            print(f"  ScienceDB pol catalog already present: {name}")
            return DATA / name

    cookie = os.environ.get("SCIENCEDB_COOKIE", "").strip()
    if not cookie:
        print(
            "  ScienceDB pol catalog: not on disk; anonymous download blocked.\n"
            "  Manual: free login at https://www.scidb.cn/detail?dataSetId="
            f"{SCIENCE_DB_ID}\n"
            "  Save as data/FAST_FRB20240114A_pol_catalog_v5.csv\n"
            "  Or set SCIENCEDB_COOKIE from browser DevTools and re-run."
        )
        return None

    urls = [
        f"https://www.scidb.cn/api/gin-sdb-portal/public/dataset/downloadFile?"
        f"dataSetId={SCIENCE_DB_ID}&fileId={SCIENCE_DB_FILE}&version=V4",
        f"https://www.scidb.cn/api/gin-sdb-file/public/download?fileId={SCIENCE_DB_FILE}&version=V4",
    ]
    headers = {
        "Referer": f"https://www.scidb.cn/detail?dataSetId={SCIENCE_DB_ID}",
        "Origin": "https://www.scidb.cn",
        "Cookie": cookie,
    }
    dest = DATA / POL_OUT_NAMES[0]
    for url in urls:
        try:
            data = _get(url, headers=headers, binary=True, timeout=120)
            if len(data) > 1000:
                dest.write_bytes(data)
                print(f"  wrote {dest.name} ({len(data)} bytes) via ScienceDB API")
                return dest
        except Exception as exc:  # noqa: BLE001
            print(f"  ScienceDB attempt failed: {exc!r}")
    print("  ScienceDB download failed even with cookie — use manual drop-in.")
    return None


def main() -> int:
    DATA.mkdir(exist_ok=True)
    print("TFPT FRB user-data fetch\n")
    fetch_blinkverse()
    print()
    fetch_sciencedb_pol()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
