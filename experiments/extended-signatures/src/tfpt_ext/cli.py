"""CLI: run all extended TFPT signature searches."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path

from . import constants
from .dynamic_probes import run_dynamic
from .frb_anyon import run_frb_anyon
from .frb_joint import run_frb_joint
from .galois_cp import run_galois
from .gw_joint import run_gw_joint
from .horizon import run_horizon
from .seed_extended import run_seed_extended

RESULTS = Path(__file__).resolve().parents[2] / "results"


def _jsonable(obj):
    if is_dataclass(obj):
        return {k: _jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if hasattr(obj, "item"):
        return obj.item()
    return obj


def cmd_audit(_: argparse.Namespace) -> int:
    print("TFPT extended signatures -- frozen compiler anchors\n")
    print(f"  phi0     = {constants.PHI0:.8f}")
    print(f"  c3       = {constants.C3:.8f}")
    print(f"  xi       = c3/phi0 = {constants.XI:.6f}")
    print(f"  lambda6  = (2/3)^6 = {constants.LAMBDA6:.8f}")
    print(f"  clock    = ln3/ln(3/2) = {constants.CLOCK_BEND:.6f}")
    print(f"  omega    = 2pi/ln((3/2)^6) = {constants.OMEGA_COMB:.4f}")
    print(f"  gravastar lag = {constants.GRAVASTAR_LAG_MS} ms, C = {constants.GRAVASTAR_C}")
    print(f"  |W(D5)|  = {constants.W_D5}, area 4ln3 = {constants.AREA_LN3:.6f}")
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    seed = args.seed
    print("=" * 72)
    print("EXT.1  FRB joint (intensity x polarisation per source)")
    frb_j = run_frb_joint(seed)
    print(f"  -> {frb_j.verdict}\n")

    print("EXT.2  FRB anyon pi/4 comb (QT.05 polarisation)")
    frb_a = run_frb_anyon(seed)
    print(f"  injection_validated={frb_a.injection_validated}")
    print(f"  -> {frb_a.verdict}\n")

    print("EXT.3  GW gravastar joint (lag + amplitude)")
    gw = run_gw_joint(seed)
    print(f"  -> {gw.verdict}\n")

    print("EXT.4  Horizon compiler fingerprints")
    hor = run_horizon()
    print(f"  identities_ok={hor.identities_ok}")
    print(f"  -> {hor.verdict}\n")

    print("EXT.5  Galois-CP extended (J_PMNS + joint delta)")
    gal = run_galois()
    print(f"  J_PMNS={gal.j_pmns:.5f}, J_max={gal.j_max:.5f}")
    print(f"  -> {gal.verdict}\n")

    print("EXT.6  Extended seed line (xi + BBN shadows)")
    seed_r = run_seed_extended()
    print(f"  xi={seed_r.xi:.6f}, core chi2/dof={seed_r.core_chi2_dof}")
    print(f"  -> {seed_r.verdict}\n")

    print("EXT.7  Dynamic probes (Crab MF + FRB gap clock)")
    dyn = run_dynamic(seed)
    print(f"  -> {dyn.verdict}\n")

    payload = {
        "frb_joint": _jsonable(frb_j),
        "frb_anyon": _jsonable(frb_a),
        "gw_joint": _jsonable(gw),
        "horizon": _jsonable(hor),
        "galois_cp": _jsonable(gal),
        "seed_extended": _jsonable(seed_r),
        "dynamic": _jsonable(dyn),
        "headline": (
            "Extended signature round: joint FRB/GW templates, horizon catalog, "
            "Galois-CP+J_PMNS, seed shadows, dynamic Crab/FRB probes. Search targets only."
        ),
    }
    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / "results.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT extended signature searches")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)
    if args.command == "audit":
        return cmd_audit(args)
    return cmd_analyze(args)


if __name__ == "__main__":
    raise SystemExit(main())
