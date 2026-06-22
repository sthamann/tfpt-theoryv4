#!/usr/bin/env python3
"""OFFLINE (heavy) Vela nu(t) reduction driver -- the full PG.06b project, runnable end-to-end
outside this sandbox.

PG.06b proved the per-observation pipeline on real NICER data (download -> PINT barycentre ->
H-test fold -> Vela pulsation at 11.19 Hz). This script wires that into the FULL reduction so that,
given time + disk, it produces the inputs for the dynamic recovery-comb test:

  STAGE 1 (automated here): for every NICER Vela observation -- download the cleaned L2 events +
    orbit (resumable; ~10 MB each, ~6.5 GB total over 665 obs), barycentre with PINT and measure a
    coarse per-obs spin frequency (H-test peak). Writes data/nicer_vela/vela_nu_perobs.csv
    (mjd, f0_hz, H, n_photons). This already shows the secular spin-down + the big glitches.

  STAGE 2 (the research step, NOT automated -- documented recipe): the per-obs frequency is only
    ~mHz precise (1/T_obs), while the post-glitch RECOVERY (and the omega=2.58 comb) live at ~uHz.
    Reaching that needs a PHASE-CONNECTED timing solution: fold each obs to a pulse TOA (~us) with
    a profile template, then tempo2/PINT fit a model (nu, nudot, nuddot, glitch steps + decays)
    that tracks every rotation across the 7.9-yr span. The output nu(t) / residuals THEN feed the
    comb test (src/tfpt_pulsar/nu_recovery.detect_comb at the kernel omega).

  STAGE 3 (hook): once a phase-connected nu(t) CSV (mjd, nu, nudot) exists at
    data/nicer_vela/vela_nu_t.csv, run `tfpt-pulsar nicer`-style stacking + detect_comb on it.

WARNINGS: Stage 1 is ~6.5 GB of downloads and many hours of folding (~10-90 s/obs). Run this
OUTSIDE the sandbox (a workstation), e.g. `python scripts/reduce_vela_nu_t.py --max-obs 0` (0 = all).
It is resumable: already-measured obs are skipped. No claim is produced; this is the data-reduction
driver the comb test is gated on.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tfpt_pulsar.vela import (  # noqa: E402
    OBS_CSV,
    RAW,
    detect_pulsation,
    download_one,
)

PEROBS_CSV = RAW.parent / "vela_nu_perobs.csv"
PHASE_CONNECTED_CSV = RAW.parent / "vela_nu_t.csv"   # the Stage-2 product the comb test consumes


def _load_obs() -> list[dict]:
    if not OBS_CSV.exists():
        print(f"  {OBS_CSV} missing -- run scripts/fetch_nicer_vela.py first.")
        return []
    with OBS_CSV.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _already_done() -> set[str]:
    if not PEROBS_CSV.exists():
        return set()
    with PEROBS_CSV.open(encoding="utf-8") as fh:
        return {row["obsid"] for row in csv.DictReader(fh)}


def stage1(max_obs: int, keep_events: bool) -> int:
    """Download + per-obs barycentre + coarse-frequency measure for every Vela obs (resumable)."""
    obs = _load_obs()
    if not obs:
        return 1
    done = _already_done()
    todo = [o for o in obs if o["obsid"] not in done]
    if max_obs > 0:
        todo = todo[:max_obs]
    gb = len(todo) * 10.0 / 1024.0
    print(f"STAGE 1: {len(obs)} Vela obs total, {len(done)} already measured, {len(todo)} to do "
          f"(~{gb:.2f} GB download). Resumable; Ctrl-C is safe.")
    new = not PEROBS_CSV.exists()
    with PEROBS_CSV.open("a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["obsid", "mjd", "f0_hz", "H", "n_photons"])
        for i, o in enumerate(todo):
            obsid, mjd = o["obsid"], float(o["mjd_start"])
            t0 = time.time()
            pair = download_one(obsid, mjd)
            if pair is None:
                print(f"  [{i+1}/{len(todo)}] {obsid}: download failed -- skipping")
                continue
            try:
                d = detect_pulsation(pair[0], pair[1])
            except Exception as exc:  # noqa: BLE001
                print(f"  [{i+1}/{len(todo)}] {obsid}: fold failed -- {exc!r}")
                continue
            w.writerow([obsid, f"{mjd:.6f}", f"{d.best_f0_hz:.8f}", f"{d.h_stat:.1f}", d.n_photons])
            fh.flush()
            print(f"  [{i+1}/{len(todo)}] {obsid} mjd={mjd:.1f}: F0={d.best_f0_hz:.6f} Hz "
                  f"H={d.h_stat:.1f} ({time.time()-t0:.0f}s)")
            if not keep_events:                       # save disk: drop the ~17 MB events after folding
                for f in pair:
                    Path(f).unlink(missing_ok=True)
    print(f"\nSTAGE 1 done -> {PEROBS_CSV}")
    print("STAGE 2 (research step, NOT automated): phase-connect the per-obs TOAs with tempo2/PINT")
    print("  (nu, nudot, nuddot + glitch steps/decays) -> data/nicer_vela/vela_nu_t.csv (mjd,nu,nudot).")
    print("STAGE 3 hook: then run the comb test on that nu(t):")
    print("  PYTHONPATH=src python -c \"from tfpt_pulsar.nu_recovery import detect_comb, OMEGA; ...\"")
    print("  (or wire vela_nu_t.csv into tfpt_pulsar.nicer_j0537.stacked_recovery + detect_comb).")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="OFFLINE heavy Vela nu(t) reduction driver (PG.06b)")
    ap.add_argument("--max-obs", type=int, default=5,
                    help="how many NEW obs to process (0 = ALL 665 ~ 6.5 GB / hours; default 5 = demo)")
    ap.add_argument("--keep-events", action="store_true",
                    help="keep the downloaded ~17 MB event files (default: delete after folding)")
    args = ap.parse_args(argv)
    print("=" * 84)
    print("Vela nu(t) reduction driver (PG.06b, HEAVY/OFFLINE). Default --max-obs 5 is a demo;")
    print("use --max-obs 0 on a workstation for the full 665-obs / ~6.5 GB / multi-hour reduction.")
    print("=" * 84)
    return stage1(args.max_obs, args.keep_events)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
