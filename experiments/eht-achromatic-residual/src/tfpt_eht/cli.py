"""Command-line entry point for the TFPT EHT pipeline.

Run a synthetic detection / non-detection / systematic-rejection demo:

    tfpt-eht demo --case signal
    tfpt-eht demo --case null
    tfpt-eht demo --case systematic
    tfpt-eht audit

The ``demo`` command builds a synthetic cube of the chosen class and
prints the three-null report. The ``audit`` command verifies that all
four equivalent expressions of the TFPT coupling agree to machine
precision (catches accidental drift between the constants).
"""

from __future__ import annotations

import argparse
import math
import sys
from collections.abc import Sequence

import numpy as np

from tfpt_eht.constants import (
    BETA_DEG,
    BETA_RAD,
    C3,
    DELTA_TOP,
    PHI0,
    TFPT_COUPLING,
    audit_self_consistency,
)
from tfpt_eht.model import expected_amplitude_at
from tfpt_eht.null_tests import run_all_nulls
from tfpt_eht.residual import (
    compute_residual_intercept,
    deproject_radial,
    rotation_measure_fit,
)
from tfpt_eht.synthetic import SyntheticConfig, generate_observed_mock


def _print_header() -> None:
    print("TFPT achromatic residual pipeline")
    print("=" * 60)
    print(f"  phi0          = {PHI0:.12e}")
    print(f"  c3            = {C3:.12e}")
    print(f"  beta_rad      = {BETA_RAD:.6e}  rad")
    print(f"  beta          = {BETA_DEG:.6f}  deg")
    print(f"  delta_top     = {DELTA_TOP:.6e}")
    print(f"  TFPT coupling = {TFPT_COUPLING:.6e}   (= 16 c3^4 = delta_top/3)")
    print()


def _cmd_audit(_args: argparse.Namespace) -> int:
    _print_header()
    print("Self-consistency audit of the TFPT coupling")
    print("-" * 60)
    audit = audit_self_consistency()
    base = audit["TFPT_COUPLING"]
    failed = 0
    for name, value in audit.items():
        diff = abs(value - base)
        rel = diff / base if base != 0.0 else math.inf
        flag = "OK" if rel < 1.0e-14 else "FAIL"
        print(f"  {name:18s} = {value:.16e}    rel.diff = {rel:.2e}   [{flag}]")
        if flag == "FAIL":
            failed += 1
    print()
    if failed:
        print(f"{failed} expression(s) failed the self-consistency check.")
        return 1
    print("All four expressions agree to machine precision.")
    print()
    print("Predicted residual amplitude at r = 10 r_g, Q_e Q_m = 1:")
    print(f"  {expected_amplitude_at(10.0)}")
    return 0


def _cmd_demo(args: argparse.Namespace) -> int:
    _print_header()
    cfg = SyntheticConfig(
        image_size=args.image_size,
        q_e_eff=args.qe,
        q_m_eff=args.qm,
    )

    if args.case == "signal":
        print("CASE = signal  (GRMHD + TFPT)")
        observed, grmhd = generate_observed_mock(cfg, tfpt_signal=True)
        observed_flip, _ = generate_observed_mock(
            SyntheticConfig(
                image_size=cfg.image_size,
                q_e_eff=cfg.q_e_eff,
                q_m_eff=cfg.q_m_eff,
                geometry=cfg.geometry.__class__(
                    center_x=cfg.geometry.center_x,
                    center_y=cfg.geometry.center_y,
                    r_inner=cfg.geometry.r_inner,
                    r_outer=cfg.geometry.r_outer,
                    sign_orientation=-cfg.geometry.sign_orientation,
                ),
            ),
            tfpt_signal=True,
        )
    elif args.case == "null":
        print("CASE = null  (GRMHD only, no TFPT signal)")
        observed, grmhd = generate_observed_mock(cfg, tfpt_signal=False)
        observed_flip, _ = generate_observed_mock(cfg, tfpt_signal=False)
    elif args.case == "systematic":
        print("CASE = systematic  (GRMHD + constant offset, no TFPT)")
        sys_offset = args.systematic_offset
        observed, grmhd = generate_observed_mock(
            cfg, tfpt_signal=False, systematic_offset=sys_offset
        )
        observed_flip, _ = generate_observed_mock(
            cfg, tfpt_signal=False, systematic_offset=sys_offset
        )
    else:
        raise ValueError(f"unknown case: {args.case}")

    chi0_obs, _rm, _sigma = rotation_measure_fit(observed)
    chi0_obs_flip, _, _ = rotation_measure_fit(observed_flip)

    residual = compute_residual_intercept(chi0_obs, grmhd.chi_0)
    residual_flip = compute_residual_intercept(chi0_obs_flip, grmhd.chi_0)

    profile_plus = deproject_radial(
        residual, observed.x, observed.y,
        r_inner=cfg.geometry.r_inner, r_outer=cfg.geometry.r_outer,
    )
    profile_minus = deproject_radial(
        residual_flip, observed.x, observed.y,
        r_inner=cfg.geometry.r_inner, r_outer=cfg.geometry.r_outer,
    )

    residual_cube = observed.chi - grmhd.cube
    chi_res_per_chan = np.nanmean(residual_cube, axis=(1, 2))
    sigma_per_chan = np.full(
        chi_res_per_chan.shape,
        cfg.angle_noise_sigma / np.sqrt(cfg.image_size**2),
        dtype=np.float64,
    )

    report = run_all_nulls(
        chi_residual_per_channel=chi_res_per_chan,
        lambda_sq=observed.lambda_sq,
        sigma_per_channel=sigma_per_chan,
        profile_plus=profile_plus,
        profile_minus=profile_minus,
        q_e_eff=cfg.q_e_eff,
        q_m_eff=cfg.q_m_eff,
    )

    print()
    print("Null test report")
    print("-" * 60)
    for r in (report.frequency, report.profile, report.sign_flip):
        flag = "PASS" if r.passed else "FAIL"
        print(f"  {r.name:18s} [{flag}]   statistic = {r.statistic:+.4e}  p = {r.p_value:.3e}")
        for k, v in r.detail.items():
            print(f"      {k:30s} = {v:.4e}")
    print()
    flag = "DETECTION" if report.detection else "NO DETECTION"
    print(f"  Combined verdict: {flag}")
    return 0 if report.detection == (args.case == "signal") else 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tfpt-eht",
        description="TFPT achromatic dyonic residual pipeline (Paper 3 §3 remark).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_demo = sub.add_parser("demo", help="run a synthetic end-to-end demo")
    p_demo.add_argument("--case", choices=["signal", "null", "systematic"], default="signal")
    p_demo.add_argument("--image-size", type=int, default=96)
    p_demo.add_argument("--qe", type=float, default=1.0, help="Q_e_eff (default 1)")
    p_demo.add_argument("--qm", type=float, default=1.0, help="Q_m_eff (default 1)")
    p_demo.add_argument(
        "--systematic-offset",
        type=float,
        default=2.0e-6,
        help="constant offset (rad) added in --case systematic",
    )
    p_demo.set_defaults(func=_cmd_demo)

    p_audit = sub.add_parser(
        "audit", help="check that the four expressions of the TFPT coupling agree"
    )
    p_audit.set_defaults(func=_cmd_audit)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
