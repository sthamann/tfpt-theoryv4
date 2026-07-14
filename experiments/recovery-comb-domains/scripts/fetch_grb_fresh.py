#!/usr/bin/env python3
"""Fetch the PREREGISTERED fresh GRB confirmation sample (grb_fresh_restone_v1).

Implements EXACTLY the frozen selection rule of
hypotheses/grb_fresh_restone_v1.yaml:
  * catalog https://www.swift.ac.uk/xrt_curves/grb.list (name <TAB> targetID)
  * exclude the 24 discovery target ids + any GRB name already in data/grb/
  * deterministic order: numpy.random.default_rng(20260713).permutation
  * fetch until 60 curves with >= 30 positive-flux points, max 220 attempts
  * store to data/grb_fresh/<name>.csv (t_s,flux,flux_err)

Run:  cd experiments/recovery-comb-domains && \
      ../tfpt-discovery/.venv/bin/python scripts/fetch_grb_fresh.py
"""
from __future__ import annotations

import csv
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "src"))

from tfpt_combdomains.grb import GRB_TARGETS, UKSSDC, _parse_qdp  # noqa: E402

CATALOG_URL = "https://www.swift.ac.uk/xrt_curves/grb.list"
UA = {"User-Agent": "tfpt-combdomains/0.1 (research; preregistered fresh GRB sample)"}
DATA_FRESH = ROOT / "data" / "grb_fresh"
DATA_DISCOVERY = ROOT / "data" / "grb"

RNG_SEED = 20260713
N_TARGET = 60
MIN_POINTS = 30
MAX_ATTEMPTS = 220

DISCOVERY_IDS = {tid for _, tid in GRB_TARGETS}


def fetch_catalog() -> list[tuple[str, int]]:
    req = urllib.request.Request(CATALOG_URL, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:  # noqa: S310
        text = r.read().decode("utf-8", "replace")
    out = []
    for line in text.splitlines():
        parts = line.strip().split("\t")
        if len(parts) != 2:
            continue
        name, tid_s = parts[0].strip(), parts[1].strip()
        try:
            tid = int(tid_s)
        except ValueError:
            continue
        if name:
            out.append((name, tid))
    return out


def main() -> int:
    print("=" * 84)
    print("PREREGISTERED fresh GRB sample fetch (grb_fresh_restone_v1, frozen 2026-07-13)")
    print("=" * 84)
    catalog = fetch_catalog()
    print(f"catalog: {len(catalog)} GRBs listed")

    discovery_names = {p.stem.replace("_", " ") for p in DATA_DISCOVERY.glob("*.csv")}
    pool = [(n, t) for n, t in catalog
            if t not in DISCOVERY_IDS and n not in discovery_names]
    print(f"after exclusion of {len(DISCOVERY_IDS)} discovery ids "
          f"(+{len(discovery_names)} existing names): {len(pool)} candidates")

    order = np.random.default_rng(RNG_SEED).permutation(len(pool))
    DATA_FRESH.mkdir(parents=True, exist_ok=True)

    got, attempts = 0, 0
    for idx in order:
        if got >= N_TARGET or attempts >= MAX_ATTEMPTS:
            break
        name, tid = pool[int(idx)]
        attempts += 1
        url = UKSSDC.format(tid=tid)
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
                text = resp.read().decode("utf-8", "replace")
        except OSError:
            print(f"  MISS {name:16s} ({tid:08d}) fetch error")
            time.sleep(1.0)
            continue
        rows, real_name = _parse_qdp(text)
        if len(rows) < MIN_POINTS:
            print(f"  SKIP {name:16s} ({tid:08d}) only {len(rows)} points")
            time.sleep(1.0)
            continue
        real_name = real_name or name
        out = DATA_FRESH / f"{real_name.replace(' ', '_')}.csv"
        with out.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["t_s", "flux", "flux_err"])
            for t, f, e in rows:
                w.writerow([f"{t:.6g}", f"{f:.6g}", f"{e:.6g}"])
        got += 1
        print(f"  OK   {real_name:16s} ({tid:08d}): {len(rows)} points  [{got}/{N_TARGET}]")
        time.sleep(1.0)

    print(f"\nfetched {got} fresh curves in {attempts} attempts -> {DATA_FRESH}")
    if got < N_TARGET:
        print("NOTE: target of 60 not reached within the frozen attempt budget -- "
              "the analysis runs on what the frozen rule produced (documented).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
