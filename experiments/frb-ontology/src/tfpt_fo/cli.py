"""CLI: PYTHONPATH=src python -m tfpt_fo.cli [analyze|audit] [--seed 0]"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from . import constants as c
from . import fo02_common_rate, fo02b_intra_session, fo03_state_clock, \
    fo04_parity, fo05_episodes, fo06_leaf_classes, fo07_covariance, \
    fo08_nullspace, fo09_rank, fo10_arrow
from .data import load_blinkverse, load_blinkverse_20201124a, load_cat1, \
    load_cat2, load_li2021, load_pol_v5, load_zhang2023, pol_v5_series, \
    SourceBursts

RESULTS = Path(__file__).resolve().parents[2] / "results" / "results.json"


def audit() -> None:
    print("frozen kernel (from c3 = 1/(8*pi), g_car = 5):")
    print(f"  lambda_T   = 64/729   = {float(c.LAMBDA_T):.7f}")
    print(f"  Lambda_DSI = 729/64   = {float(c.LAMBDA_DSI):.5f}")
    print(f"  omega      = 2pi/lnL  = {c.OMEGA:.6f}")
    print(f"  epsilon    = e^-pi2/L = {c.EPSILON_PRED:.6f}")
    print(f"  bend       = ln3/ln1.5= {c.BEND:.6f}")
    print(f"  teeth      = {[round(v, 4) for v in c.TIME_TEETH.values()]}")


def analyze(seed: int) -> None:
    t0 = time.time()
    out = {"experiment": "frb-ontology", "prereg": "hypotheses/frb_ontology_v1.yaml",
           "seed": seed, "axes": {}}

    pol = load_pol_v5()
    print(f"[data] FRB 20240114A v5: {len(pol.mjd)} bursts")

    print("[FO.02] common-rate medium operator ...")
    out["axes"]["FO.02"] = fo02_common_rate.run(pol, seed)
    print(f"        verdict={out['axes']['FO.02']['verdict']}")

    print("[FO.02b] intra-session common-rate (v1.2 addendum) ...")
    out["axes"]["FO.02b"] = fo02b_intra_session.run(
        [pol_v5_series(pol), load_blinkverse_20201124a()], seed)
    print(f"        verdict={out['axes']['FO.02b']['verdict']} "
          f"({out['axes']['FO.02b']['verdicts']})")

    print("[FO.03] state-clock comb ...")
    out["axes"]["FO.03"] = fo03_state_clock.run(pol, seed)
    print(f"        verdict={out['axes']['FO.03']['verdict']}")

    print("[FO.04] parity without rate ...")
    out["axes"]["FO.04"] = fo04_parity.run(pol, seed)
    print(f"        verdict={out['axes']['FO.04']['verdict']}")

    print("[FO.05] episode transfer ...")
    v5_source = SourceBursts("FRB20240114A(v5)", pol.mjd, None)
    sources = load_blinkverse() + [v5_source] + load_cat2()
    print(f"        sources considered: {[s.source for s in sources]}")
    out["axes"]["FO.05"] = fo05_episodes.run(sources, seed)
    print(f"        verdict={out['axes']['FO.05']['verdict']}")

    print("[FO.06] leaf classes (CHIME Cat1) ...")
    out["axes"]["FO.06"] = fo06_leaf_classes.run(load_cat1(), seed)
    print(f"        verdict={out['axes']['FO.06']['verdict']}")

    # v1.3 operator-structure probes
    print("[FO.07] covariance character blocks ...")
    out["axes"]["FO.07"] = fo07_covariance.run(pol, seed)
    print(f"        verdict={out['axes']['FO.07']['verdict']}")

    print("[FO.08] polarimetric null space ...")
    out["axes"]["FO.08"] = fo08_nullspace.run(pol, seed)
    print(f"        verdict={out['axes']['FO.08']['verdict']}")

    energy_sources = [load_li2021(), load_zhang2023()]

    print("[FO.09] rank drop ...")
    out["axes"]["FO.09"] = fo09_rank.run_energy(energy_sources, seed)
    v5s = pol_v5_series(pol)
    out["axes"]["FO.09"]["v5_medium_leg"] = fo09_rank.run_medium(
        seed, v5s.mjd, v5s.obs)
    print(f"        verdict={out['axes']['FO.09']['verdict']}")

    print("[FO.10] causal asymmetry ...")
    out["axes"]["FO.10"] = fo10_arrow.run(energy_sources, seed)
    print(f"        verdict={out['axes']['FO.10']['verdict']}")

    out["runtime_s"] = round(time.time() - t0, 1)
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(out, indent=2))
    print(f"\nwrote {RESULTS} ({out['runtime_s']} s)")
    for k, v in out["axes"].items():
        print(f"  {k}: {v['verdict']}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["analyze", "audit"])
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    if a.cmd == "audit":
        audit()
    else:
        analyze(a.seed)


if __name__ == "__main__":
    main()
