"""CLI audit surface: ``tfpt-qckernel audit | analyze | hardware``.

analyze runs both simulator tiers end-to-end and writes results/results.json.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from . import constants, hardware
from .circuits import relaxation_circuit
from .sim import DEFAULT_N_BLOCKS, FAKE_BACKENDS, run_exact, run_noisy

RESULTS = Path(__file__).resolve().parents[2] / "results" / "results.json"


def cmd_audit(_args: argparse.Namespace) -> int:
    a = constants.audit()
    for k, v in a.items():
        print(f"  {k:32s} {v}")
    print("AUDIT", "OK" if a["ok"] else "FAILED")
    return 0 if a["ok"] else 1


def _circuit_summary() -> dict:
    qc = relaxation_circuit(DEFAULT_N_BLOCKS, semantics="energy")
    return {
        "qubits": 5,
        "layout": "q0 Perron (protected, no gates) | q1/q2 flavor modes | q3/q4 ancillas",
        "damping_block": "CRy(theta_k) sys->anc, CX anc->sys, reset anc; "
                         "sin^2(theta_k/2) = 1 - survival_k",
        "survival_per_block_energy": {"mode2": "2/3", "mode3": "1/3"},
        "survival_per_block_amplitude": {"mode2": "sqrt(2/3)", "mode3": "sqrt(1/3)"},
        "blocks_per_transfer_step": constants.SUBSTEPS_PER_STEP,
        "n_blocks_curve": DEFAULT_N_BLOCKS,
        "logical_depth_final": qc.depth(),
        "logical_ops_final": {k: int(v) for k, v in qc.count_ops().items()},
        "hard_wall": "architectural: exactly two damping channels, no third decay mode",
    }


def cmd_analyze(args: argparse.Namespace) -> int:
    print("== frozen-kernel audit ==")
    a = constants.audit()
    print(f"   ok={a['ok']}  bend={a['bend_ln3_over_ln3half']:.6f}")
    if not a["ok"]:
        return 1

    print("== exact tier (Aer density matrix, both semantics) ==")
    exact = {sem: run_exact(sem) for sem in ("energy", "amplitude")}
    for sem, r in exact.items():
        print(f"   [{sem}] step survivals ok={r.per_step_survival['ok']} "
              f"(mode2 {r.per_step_survival['mode2_after_6_blocks']:.12f} "
              f"vs {r.per_step_survival['mode2_target']:.12f}); "
              f"coherence sqrt-law ok={r.coherence_step_survival['ok']}")
        print(f"   [{sem}] Perron protected={r.perron_protected}  "
              f"max pop err={r.max_population_error:.3e}")
        print(f"   [{sem}] direct bend={r.direct_bend:.10f}  "
              f"free-ratio bend={r.bend_report['free']['ratio']:.10f}  "
              f"(target {constants.BEND:.10f})")

    print(f"== noisy tier (Aer + {args.backend} noise model) ==")
    noisy = run_noisy(args.backend, shots_grid=tuple(args.shots), n_seeds=args.seeds)
    for shots, s in noisy.per_shots_summary.items():
        print(f"   shots={shots:>6}: free ratio {s['mean_free_ratio']:.4f} "
              f"+- {s['std_free_ratio']:.4f} (bias {s['mean_bias']:+.4f}), "
              f"per-mode bend {s['mean_per_mode_bend']:.4f}, "
              f"detection {s['detection_fraction']:.0%}")
    print(f"   min shots identifiable: {noisy.min_shots_identifiable}  "
          f"floor retention after {noisy.n_blocks} blocks: "
          f"{noisy.floor_retention_final:.3f}  verdict: {noisy.verdict}")

    out = {
        "experiment": "qc-recovery-kernel",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "firewall": "internal consistency + hardware feasibility; NOT external evidence",
        "kernel_audit": a,
        "circuit": _circuit_summary(),
        "exact": {sem: asdict(r) for sem, r in exact.items()},
        "noisy": asdict(noisy),
        "verdict": noisy.verdict,
    }
    RESULTS.parent.mkdir(exist_ok=True)
    RESULTS.write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {RESULTS}")
    return 0


def cmd_hardware(args: argparse.Namespace) -> int:
    if args.fetch:
        print(json.dumps(hardware.fetch(args.fetch), indent=2))
    elif args.dry_run:
        print(json.dumps(hardware.dry_run(), indent=2))
    else:
        print(json.dumps(hardware.submit(shots=args.hw_shots), indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="tfpt-qckernel",
                                description="TFPT recovery channel as a quantum circuit")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("audit", help="frozen-kernel identity checks")

    pa = sub.add_parser("analyze", help="exact + noisy simulator tiers -> results.json")
    pa.add_argument("--backend", choices=sorted(FAKE_BACKENDS), default="fake_brisbane")
    pa.add_argument("--shots", type=int, nargs="+", default=[256, 1024, 4096, 16384])
    pa.add_argument("--seeds", type=int, default=3)

    ph = sub.add_parser("hardware", help="IBM runtime submission hook (needs saved token)")
    ph.add_argument("--dry-run", action="store_true",
                    help="validate ISA transpilation only (no token)")
    ph.add_argument("--fetch", metavar="JOB_ID", default=None)
    ph.add_argument("--hw-shots", type=int, default=16384)

    args = p.parse_args(argv)
    if args.cmd == "audit":
        return cmd_audit(args)
    if args.cmd == "analyze":
        return cmd_analyze(args)
    return cmd_hardware(args)


if __name__ == "__main__":
    raise SystemExit(main())
