#!/usr/bin/env python3
"""Fetch the 2024 Vela giant-glitch phase-connected ephemeris (PG.07) -> data/vela_2024/.

The 2024 April 29 Vela giant glitch (PSR J0835-4510, MJD 60429.87) was caught live by IAR/PuMA
and precisely timed by Mount Pleasant (MPRO). The LVK "Constraints on gravitational waves from the
2024 Vela pulsar glitch" data release publishes a PHASE-CONNECTED TEMPO2 timing solution with the
full glitch model (permanent {Delta nu, Delta nudot} jump + three transient exponential recovery
terms, tau_d = 0.39, 2.45, 15.1 d):

    Zenodo concept DOI 10.5281/zenodo.17735648  ->  record 17735649 (v1), license CC-BY-4.0
    file: J0835-4510_long_F3.par   (paper: A&A 698, A72 (2025); LVK arXiv:2512.17990)

This downloads the tiny (~2 KB) .par (committed as provenance) and writes two small derived,
committed CSVs:
  * vela2024_nudot.csv          -- the reconstructed post-glitch nudot(tau) recovery waveform
  * vela_glitch_recoveries.csv  -- the Vela giant-glitch recovery-parameter table (2016/2019/2021/
                                   2024) used by the PG.07 stack, WITH per-glitch provenance.

Any large raw tarballs from the same record are NOT fetched (they are gitignored). Cite the data
release (Zenodo 10.5281/zenodo.17735648) and A&A 698 A72 (2025) when using these data.

Run:  python scripts/fetch_vela_2024.py
"""

from __future__ import annotations

import csv
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tfpt_pulsar.vela2024 import (  # noqa: E402
    DATA,
    NUDOT_CSV,
    PAR_FILE,
    RECOVERIES_CSV,
    parse_par,
    published_prior_glitches,
    recovery_grid,
    vela_2024_from_par,
)

PAR_URL = ("https://zenodo.org/api/records/17735649/files/"
           "J0835-4510_long_F3.par/content")
UA = "tfpt-pulsar/0.1 (research)"


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    print(f"fetching {PAR_URL} ...")
    req = urllib.request.Request(PAR_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:  # noqa: S310
        text = r.read().decode("utf-8", errors="replace")
    PAR_FILE.write_text(text, encoding="utf-8")
    print(f"  wrote {PAR_FILE} ({len(text)} bytes)")

    par = parse_par(text)
    print(f"  glitch epoch MJD {par.glep:.5f}; Delta nu/nu = {par.dnu_over_nu:.3e}; "
          f"tau_d = {[round(t, 3) for _, t in par.transients]} d; "
          f"post-glitch window {par.post_glitch_days:.1f} d")

    # derived nudot(tau) recovery waveform (committed, small)
    g24 = vela_2024_from_par(par)
    tau, rec = recovery_grid(g24)
    with NUDOT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["tau_days", "nudot_rec_s2"])
        for t, y in zip(tau, rec, strict=True):
            w.writerow([f"{t:.6g}", f"{y:.6e}"])
    print(f"  wrote {NUDOT_CSV} ({len(tau)} samples, reach "
          f"{__import__('math').log(tau.max() / tau.min()) / __import__('math').log(1.5**6):.2f} "
          "comb periods)")

    # Vela glitch recovery-parameter table for the stack (committed, small)
    glitches = [g24, *published_prior_glitches(par.f0, par.transients)]
    with RECOVERIES_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["glitch", "epoch_mjd", "dnu_over_nu", "tau_d_days",
                    "baseline_days_to_next", "template", "params_source"])
        for g in sorted(glitches, key=lambda g: g.epoch_mjd):
            w.writerow([g.name, f"{g.epoch_mjd:.4f}", f"{g.dnu_over_nu:.2e}",
                        ";".join(f"{t:.3g}" for _, t in g.transients),
                        f"{g.baseline_days:.0f}", int(g.template), g.params_source])
    print(f"  wrote {RECOVERIES_CSV} ({len(glitches)} Vela giant glitches)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
