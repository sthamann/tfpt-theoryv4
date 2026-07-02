"""``tfpt-w analyze`` -- the dark-energy w = -1 kill watchdog.

TFPT predicts a true cosmological constant: ``w = -1`` exactly (the Lambda/H0 engine,
``S_dS * rho_Lambda = 32 pi^4``).  DESI DR2 (2025) reports a preference for *dynamical*
dark energy in the CPL ``w0-wa`` plane, at 2.8-4.2 sigma depending on which supernova
compilation is combined with DESI BAO + CMB.

This watchdog confronts the TFPT point ``(w0, wa) = (-1, 0)`` with each published DESI DR2
combination using the 2-D Gaussian (Mahalanobis) distance, and -- critically -- is
**overlap-aware**: the three SN compilations (Pantheon+, Union3, DES-SN5YR) share low-z
supernovae, so they are ALTERNATIVE datasets, not independent.  The watchdog therefore
takes the *strongest single* overlap-aware combination as the headline and explicitly
shows the spurious significance a naive product would invent.

Frozen kill rule (pre-registered):

    w != -1 at >= 5 sigma in a single, systematics-controlled, overlap-aware combination
    -> the TFPT Lambda/H0 cosmology branch falls (not the compiler core).

A naive sqrt(sum sigma^2) over the three overlapping SN families does NOT count.

In addition to the frozen 2025 baseline, the watchdog carries a DATED STATUS TIMELINE
(data/measurements.json -> "status_timeline"): TFPT predicts the evolving-DE preference
dissolves, so the direction of each update matters and is recorded before the next data
release (2026 entry: DES-Dovekie recalibration 4.2->3.2 sigma; Bayesian reanalysis
eliminates the DESI+CMB-only preference, ln B = -0.57).
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
RESULTS = Path(__file__).resolve().parents[2] / "results"
KILL_SIGMA = 5.0


def _mahalanobis(c: dict, w0_pred: float, wa_pred: float) -> float:
    """2-D Gaussian distance of the prediction from a CPL best fit (with w0-wa corr)."""
    dx = w0_pred - c["w0"]
    dy = wa_pred - c["wa"]
    sx, sy, rho = c["sigma_w0"], c["sigma_wa"], c["rho_w0_wa"]
    denom = 1.0 - rho**2
    m2 = (dx**2 / sx**2 + dy**2 / sy**2 - 2 * rho * dx * dy / (sx * sy)) / denom
    return math.sqrt(max(m2, 0.0))


def analyze(m: dict) -> dict:
    pred = m["tfpt_prediction"]
    rows = []
    for c in m["combinations"]:
        d = _mahalanobis(c, pred["w0"], pred["wa"])
        rows.append({"name": c["name"], "sn_family": c["sn_family"],
                     "tension_2d_sigma": round(d, 2),
                     "published_sigma_vs_LCDM": c["published_sigma_vs_LCDM"]})
    headline = max(rows, key=lambda r: r["tension_2d_sigma"])
    naive = math.sqrt(sum(r["tension_2d_sigma"] ** 2 for r in rows))  # WRONG on purpose
    triggered = headline["tension_2d_sigma"] >= KILL_SIGMA
    return {"prediction": pred, "combinations": rows,
            "headline_overlap_aware_sigma": headline["tension_2d_sigma"],
            "headline_combination": headline["name"],
            "naive_product_sigma_DO_NOT_USE": round(naive, 2),
            "kill_sigma": KILL_SIGMA, "kill_triggered": triggered,
            "status": "tension" if triggered else "data_limited",
            "status_timeline": m.get("status_timeline", [])}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT dark-energy w=-1 watchdog (overlap-aware)")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)
    m = json.loads(DATA.read_text(encoding="utf-8"))

    print("=" * 74)
    print("TFPT dark-energy watchdog  (TFPT: w = -1 exactly; DESI DR2 CPL confrontation)")
    print("=" * 74)
    if args.command == "audit":
        return 0

    res = analyze(m)
    print(f"  TFPT point: (w0, wa) = ({res['prediction']['w0']}, {res['prediction']['wa']})\n")
    print(f"  {'combination':22s} {'SN family':10s}  2D dist   published")
    for r in res["combinations"]:
        print(f"  {r['name']:22s} {r['sn_family']:10s}  {r['tension_2d_sigma']:4.2f}s    "
              f"{r['published_sigma_vs_LCDM']:.1f}s")
    print(f"\n  headline (strongest single, overlap-aware): "
          f"{res['headline_overlap_aware_sigma']:.2f} sigma  [{res['headline_combination']}]")
    print(f"  naive product over 3 overlapping SN families: "
          f"{res['naive_product_sigma_DO_NOT_USE']:.2f} sigma  <-- SPURIOUS, do not use "
          f"(SN samples overlap)")
    print(f"\n  kill rule: w != -1 at >= {KILL_SIGMA} sigma (single overlap-aware combo)")

    if res["status_timeline"]:
        print("\n  STATUS TIMELINE (TFPT predicts the evolving-DE preference dissolves;")
        print("  each dated entry records the direction BEFORE the next data release):")
        for t in res["status_timeline"]:
            print(f"    [{t['date']}] {t['entry']}")
            dv = t.get("des_dovekie_recalibration")
            if dv:
                print(f"        DES-Dovekie ({dv['reference'].split(' -- ')[0]}): "
                      f"w0={dv['w0']}+-{dv['sigma_w0']}, wa={dv['wa']}+-{dv['sigma_wa']}; "
                      f"{dv['significance_vs_LCDM_sigma']} sigma vs LCDM "
                      f"(down from 4.2; ~20% underestimated photometric syst. corrected)")
            by = t.get("bayesian_reanalysis")
            if by:
                print(f"        Bayesian (arXiv:2603.05472): DESI DR2+CMB-only preference "
                      f"ELIMINATED, ln B = {by['desi_dr2_cmb_only_lnB']}+-"
                      f"{by['desi_dr2_cmb_only_lnB_sigma']}; +Dovekie ln B = "
                      f"{by['desi_dr2_cmb_dovekie_lnB']}; Union3 frequentist ~3.8 sigma "
                      f"persists (2.23 sigma Bayesian)")
            if t.get("surviving_pulls"):
                print(f"        surviving: {t['surviving_pulls']}")

    if res["kill_triggered"]:
        verdict = (f"KILL TRIGGERED: {res['headline_combination']} excludes w=-1 at "
                   f"{res['headline_overlap_aware_sigma']:.1f} sigma -> Lambda/H0 cosmology branch falls.")
    else:
        verdict = (f"WATCHDOG ARMED (data_limited): strongest overlap-aware exclusion of w=-1 is "
                   f"{res['headline_overlap_aware_sigma']:.1f} sigma (< {KILL_SIGMA}) on the frozen "
                   f"2025 baseline. 2026 status: that headline is known to be calibration-inflated "
                   f"(DES-Dovekie: 4.2 -> 3.2 sigma; Bayesian DESI+CMB-only ln B = -0.57) -- the "
                   f"preference is dissolving, as TFPT's w=-1 fixed point requires; Union3-driven "
                   f"frequentist pulls (~3.8 sigma) remain. Not a TFPT kill.")
    print(f"\n-> {verdict}")
    res["verdict"] = verdict

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
