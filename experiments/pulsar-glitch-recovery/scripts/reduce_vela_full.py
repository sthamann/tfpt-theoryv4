#!/usr/bin/env python3
"""PG.06b FULL reduction driver -- STAGE 1 (per-obs) and STAGE 2 (segments).

STAGE 1: barycentre + Z^2 frequency measurement for every downloaded NICER Vela obs
  (manifest data/nicer_vela/manifest_full_reduction.json; raw files from
  scripts/download_vela_all.py). Parallel over processes, resumable via the output CSV.
  -> data/nicer_vela/vela_nu_perobs_full.csv

STAGE 2: segment-coherent nu fits (gap <= 1.5 d, span <= 8 d) with cycle-slip check.
  -> data/nicer_vela/vela_nu_t_full.csv

Usage:
  python scripts/reduce_vela_full.py stage1 [--procs 6] [--max-obs 0]
  python scripts/reduce_vela_full.py stage2
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tfpt_pulsar.vela_full import (  # noqa: E402
    NV,
    PEROBS_CSV,
    SEGMENTS_CSV,
    LocalSpinModel,
    SpinPredictor,
    build_segments,
    fit_segment,
    measure_obs,
)

FIELDS = ["obsid", "mjd_mid", "tspan_s", "n_ph", "f0", "sigma_f", "h_stat", "z2_1",
          "detected"]
SEG_FIELDS = ["mjd_mid", "tspan_d", "n_obs", "n_det", "n_ph", "f0", "sigma_f",
              "z2_coh", "z2_incoh_sum", "coherent"]


def _worker(obsid: str) -> dict | None:
    pred = SpinPredictor.load()
    m = measure_obs(obsid, pred)
    if m is None:
        return {"obsid": obsid, "mjd_mid": "", "tspan_s": "", "n_ph": "",
                "f0": "", "sigma_f": "", "h_stat": "", "z2_1": "", "detected": False}
    return {"obsid": m.obsid, "mjd_mid": f"{m.mjd_mid:.8f}",
            "tspan_s": f"{m.tspan_s:.1f}", "n_ph": m.n_ph,
            "f0": (f"{m.f0:.9f}" if m.f0 is not None else ""),
            "sigma_f": (f"{m.sigma_f:.3e}" if m.sigma_f is not None else ""),
            "h_stat": f"{m.h_stat:.1f}", "z2_1": f"{m.z2_1:.1f}", "detected": m.detected}


def stage1(procs: int, max_obs: int) -> int:
    man = json.loads((NV / "manifest_full_reduction.json").read_text(encoding="utf-8"))
    obsids = [o["obsid"] for o in man["observations"]]
    done: set[str] = set()
    if PEROBS_CSV.exists():
        with PEROBS_CSV.open(encoding="utf-8") as fh:
            done = {r["obsid"] for r in csv.DictReader(fh)}
    todo = [o for o in obsids if o not in done]
    if max_obs > 0:
        todo = todo[:max_obs]
    print(f"STAGE 1: {len(obsids)} obs, {len(done)} done, {len(todo)} to do "
          f"({procs} procs)", flush=True)
    if not todo:
        return 0
    new = not PEROBS_CSV.exists()
    t0 = time.time()
    with PEROBS_CSV.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        with ProcessPoolExecutor(max_workers=procs) as ex:
            futs = {ex.submit(_worker, o): o for o in todo}
            for i, fut in enumerate(as_completed(futs)):
                try:
                    row = fut.result()
                except Exception as exc:  # noqa: BLE001
                    print(f"  {futs[fut]}: FAILED {exc!r}", flush=True)
                    continue
                if row is not None:
                    w.writerow(row)
                    fh.flush()
                if (i + 1) % 20 == 0:
                    el = time.time() - t0
                    print(f"  [{i+1}/{len(todo)}] {el:.0f}s "
                          f"({el/(i+1):.1f} s/obs)", flush=True)
    print(f"STAGE 1 done -> {PEROBS_CSV}", flush=True)
    return 0


def _load_rows() -> list[dict]:
    rows = []
    with PEROBS_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append({
                "obsid": r["obsid"],
                "mjd_mid": float(r["mjd_mid"]) if r["mjd_mid"] else None,
                "n_ph": int(r["n_ph"]) if r["n_ph"] else 0,
                "f0": float(r["f0"]) if r["f0"] else None,
                "sigma_f": float(r["sigma_f"]) if r["sigma_f"] else None,
                "h_stat": float(r["h_stat"]) if r["h_stat"] else 0.0,
                "z2_1": float(r["z2_1"]) if r["z2_1"] else 0.0,
                "detected": r["detected"] == "True",
            })
    return rows


_RESCUE_LOCAL: LocalSpinModel | None = None


def _rescue_worker(obsid: str) -> dict | None:
    pred = SpinPredictor.load()
    local = _RESCUE_LOCAL
    meta_pred = None
    # centre the narrow rescue window on the local model where available
    m = measure_obs(obsid, pred)          # ensures bary cache exists (now lower floor)
    if m is None:
        return None
    if local is not None:
        lp = local.predict(m.mjd_mid)
        if lp is not None:
            meta_pred = lp[0]
    if meta_pred is not None:
        m = measure_obs(obsid, pred, f_pred_override=meta_pred, half=2.5e-5, h_min=15.0)
    return None if m is None else {
        "obsid": m.obsid, "mjd_mid": f"{m.mjd_mid:.8f}", "tspan_s": f"{m.tspan_s:.1f}",
        "n_ph": m.n_ph, "f0": (f"{m.f0:.9f}" if m.f0 is not None else ""),
        "sigma_f": (f"{m.sigma_f:.3e}" if m.sigma_f is not None else ""),
        "h_stat": f"{m.h_stat:.1f}", "z2_1": f"{m.z2_1:.1f}", "detected": m.detected}


def rescue(procs: int) -> int:
    """Second pass over unusable/undetected obs: lower photon floor + narrow scan
    window centred on the local spin model built from the first-pass detections."""
    global _RESCUE_LOCAL
    rows = _load_rows()
    det = [r for r in rows if r["detected"]]
    _RESCUE_LOCAL = LocalSpinModel(det)
    todo = [r["obsid"] for r in rows if not r["detected"]]
    print(f"RESCUE: {len(det)} detected, retrying {len(todo)} obs", flush=True)
    by_id = {r["obsid"]: r for r in rows}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=procs, initializer=_set_local,
                             initargs=(det,)) as ex:
        futs = {ex.submit(_rescue_worker, o): o for o in todo}
        for i, fut in enumerate(as_completed(futs)):
            try:
                row = fut.result()
            except Exception as exc:  # noqa: BLE001
                print(f"  {futs[fut]}: FAILED {exc!r}", flush=True)
                continue
            if row is not None:
                old = by_id[row["obsid"]]
                old.update({
                    "mjd_mid": float(row["mjd_mid"]), "n_ph": int(row["n_ph"]),
                    "f0": float(row["f0"]) if row["f0"] else None,
                    "sigma_f": float(row["sigma_f"]) if row["sigma_f"] else None,
                    "h_stat": float(row["h_stat"]), "z2_1": float(row["z2_1"]),
                    "detected": row["detected"], "tspan_s": float(row["tspan_s"])})
            if (i + 1) % 40 == 0:
                print(f"  [{i+1}/{len(todo)}] {time.time()-t0:.0f}s", flush=True)
    with PEROBS_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({
                "obsid": r["obsid"],
                "mjd_mid": f"{r['mjd_mid']:.8f}" if r["mjd_mid"] else "",
                "tspan_s": f"{r.get('tspan_s', 0.0):.1f}" if r["mjd_mid"] else "",
                "n_ph": r["n_ph"] or "",
                "f0": f"{r['f0']:.9f}" if r["f0"] is not None else "",
                "sigma_f": f"{r['sigma_f']:.3e}" if r["sigma_f"] is not None else "",
                "h_stat": f"{r['h_stat']:.1f}" if r["mjd_mid"] else "",
                "z2_1": f"{r['z2_1']:.1f}" if r["mjd_mid"] else "",
                "detected": r["detected"]})
    n_det = sum(1 for r in rows if r["detected"])
    print(f"RESCUE done: {n_det} detected total -> {PEROBS_CSV}", flush=True)
    return 0


def _set_local(det_rows: list[dict]) -> None:
    global _RESCUE_LOCAL
    _RESCUE_LOCAL = LocalSpinModel(det_rows)


def stage2() -> int:
    rows = [r for r in _load_rows() if r["mjd_mid"]]
    det = [r for r in rows if r["detected"]]
    local = LocalSpinModel(det)
    pred = SpinPredictor.load()
    segs = build_segments(rows)
    print(f"STAGE 2: {len(rows)} usable obs ({len(det)} detected) -> "
          f"{len(segs)} segments", flush=True)
    out = []
    t0 = time.time()
    for i, seg in enumerate(segs):
        sf = fit_segment(seg, local, pred)
        if sf is not None:
            out.append(sf)
        if (i + 1) % 20 == 0:
            print(f"  [{i+1}/{len(segs)}] {time.time()-t0:.0f}s", flush=True)
    with SEGMENTS_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(SEG_FIELDS)
        for s in out:
            w.writerow([f"{s.mjd_mid:.8f}", f"{s.tspan_d:.3f}", s.n_obs, s.n_det,
                        s.n_ph, f"{s.f0:.10f}", f"{s.sigma_f:.3e}", f"{s.z2_coh:.1f}",
                        f"{s.z2_incoh_sum:.1f}", s.coherent])
    n_coh = sum(1 for s in out if s.coherent)
    print(f"STAGE 2 done: {len(out)} segments ({n_coh} coherent, "
          f"{len(out)-n_coh} incoherent-fallback) -> {SEGMENTS_CSV}", flush=True)
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("stage", choices=["stage1", "rescue", "stage2"])
    ap.add_argument("--procs", type=int, default=6)
    ap.add_argument("--max-obs", type=int, default=0)
    args = ap.parse_args(argv)
    if args.stage == "stage1":
        return stage1(args.procs, args.max_obs)
    if args.stage == "rescue":
        return rescue(args.procs)
    return stage2()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
