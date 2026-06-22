"""``tfpt-cmb analyze`` -- the cross-domain birefringence/baryon seed-line test."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import constants
from .birefringence_meta import SYS_FLOOR_DEG, birefringence_meta
from .seed_line import run_seed_line
from .shared_seed import run_shared_seed

RESULTS = Path(__file__).resolve().parents[2] / "results"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT CMB birefringence + Omega_b seed-line test")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)

    print("=" * 72)
    print("TFPT seed-line: one phi0 -> cosmic birefringence beta AND baryon Omega_b")
    print("=" * 72)
    c = constants.summary()
    print(f"  c3 = 1/(8pi) = {c['c3']:.9f}  ->  phi0 = {c['phi0']:.9f}")
    print(f"  beta = phi0/(4pi) = {c['beta_deg']:.6f} deg ;  "
          f"Omega_b = (4pi-1) beta_rad = {c['Omega_b']:.5f}")
    print(f"  frozen line: Omega_b / beta_rad = 4pi - 1 = {c['seed_slope_4pi_minus_1']:.5f}")
    if args.command == "audit":
        return 0

    r = run_seed_line()
    print("\n[beta_only]")
    for ch in r.beta_checks:
        print(f"    beta  {ch.measured:.3f}+/-{ch.sigma:.3f} deg vs TFPT {ch.predicted:.4f}  "
              f"-> {ch.z:+.2f} sigma  ({ch.name})")
    print(f"    status: {r.modes['beta_only']['status']}")

    print("\n[omega_b_only]  (Omega_b derived unit-safely as Omega_b_h2 / h^2)")
    for ch in r.omega_checks:
        print(f"    Om_b  {ch.measured:.5f}+/-{ch.sigma:.5f} vs TFPT {ch.predicted:.5f}  "
              f"-> {ch.z:+.2f} sigma  ({ch.name})")
    print(f"    status: {r.modes['omega_b_only']['status']}")

    ji = r.modes["joint_independent"]
    print("\n[joint_independent]  (assumes cov(beta,Omega_b)=0)")
    print(f"    line ratio Omega_b/beta_rad = {ji['line_ratio']:.3f} +/- {ji['line_ratio_err']:.3f}"
          f"  vs 4pi-1 = {constants.SEED_SLOPE:.3f}  -> {ji['line_z']:+.2f} sigma")
    print(f"    single-seed coherence: phi0(beta)={ji['phi0_from_beta']:.5f} vs "
          f"phi0(Omega_b)={ji['phi0_from_omega']:.5f} (frozen {constants.PHI0:.5f})  "
          f"-> z={ji['seed_coherence_z']:+.2f} sigma")
    print(f"    status: {ji['status']}")

    jc = r.modes["joint_covariance_placeholder"]
    print("\n[joint_covariance_placeholder]")
    print(f"    status: {jc['status']}")
    print(f"    {jc['note']}")

    print(f"\n-> {r.verdict}")

    # ---- shared-seed meta-test: one phi0 -> four independent observables -----
    s = run_shared_seed()
    print("\n[shared_seed]  one phi0 -> beta + Omega_b + sin^2(theta13) + Cabibbo")
    print(f"    frozen phi0 = {s.phi0_frozen:.5f}")
    for leg in s.legs:
        print(f"    {leg.observable:14s} {leg.measured:.5g} -> phi0={leg.phi0_implied:.5f}"
              f"+/-{leg.phi0_implied_err:.5f}  ({leg.z_vs_frozen:+.2f} sigma)  [{leg.source}]")
    print(f"    combined chi2/dof = {s.combined_chi2:.2f}/{s.dof} ; max|z| = {s.spread_max_z:.2f}")
    print(f"    -> {s.verdict}")

    # ---- beta meta-analysis: combine the birefringence measurements, correlation-aware ----
    mt = birefringence_meta()
    print("\n[beta_meta]  combine the birefringence measurements (shared-systematic aware)")
    for mm in mt.measurements:
        print(f"    {mm['experiment']:38s} {mm['value']:.3f}+/-{mm['sigma']:.3f} deg "
              f"[family {mm['data_family']}]")
    print(f"    NAIVE IVW (independent, lower-bound error): {mt.naive_mean:.3f}+/-{mt.naive_sigma:.3f}"
          f" -> {mt.naive_z:+.2f} sigma   (inputs mutually consistent, chi2/dof={mt.internal_chi2_dof:.2f})")
    print(f"    FAMILY-AWARE (+{SYS_FLOOR_DEG:.2f} deg shared calib syst): "
          f"{mt.meta_mean:.3f}+/-{mt.meta_sigma:.3f} -> {mt.meta_z:+.2f} sigma  (the honest error)")
    if mt.bbn_cross_z is not None:
        print(f"    CMB-INDEPENDENT cross-check (BBN Omega_b -> beta): {mt.bbn_cross_z:+.2f} sigma")
    print(f"    -> {mt.verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {"constants": c, "modes": r.modes, "verdict": r.verdict,
           "shared_seed": {"phi0_frozen": s.phi0_frozen, "combined_chi2": s.combined_chi2,
                           "dof": s.dof, "max_z": s.spread_max_z,
                           "consistent": s.combined_consistent, "verdict": s.verdict,
                           "legs": [vars(leg) for leg in s.legs]},
           "beta_meta": {"naive_mean": mt.naive_mean, "naive_sigma": mt.naive_sigma,
                         "naive_z": mt.naive_z, "meta_mean": mt.meta_mean,
                         "meta_sigma": mt.meta_sigma, "meta_z": mt.meta_z,
                         "internal_chi2_dof": mt.internal_chi2_dof,
                         "bbn_cross_z": mt.bbn_cross_z, "family_values": mt.family_values,
                         "verdict": mt.verdict}}
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
