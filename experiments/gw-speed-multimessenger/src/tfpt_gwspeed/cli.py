"""``tfpt-gwspeed analyze`` -- TFPT v_GW = c null test from GW170817 + GRB170817A.

TFPT predicts a single Lorentz cone shared by EM, gravity and massless modes, so
(v_GW - c)/c = 0 exactly (horizon_readouts; a named falsifier). The GW170817 + GRB
multimessenger bound brackets zero, so this is a CONSISTENCY (kill-test passed), not a
detection -- a measured v_GW != c would break the gravity closure.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

MPC_M = 3.0856775815e22
C_M_S = 2.99792458e8
DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
RESULTS = Path(__file__).resolve().parents[2] / "results"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT v_GW=c null test (GW170817)")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)

    m = json.loads(DATA.read_text(encoding="utf-8"))["GW170817"]
    print("=" * 72)
    print("TFPT v_GW = c null test (single Lorentz cone) -- GW170817 + GRB170817A")
    print("=" * 72)
    print("  TFPT prediction: (v_GW - c)/c = 0 exactly")
    if args.command == "audit":
        return 0

    # transparent back-of-envelope central value: GW arrived dt before the GRB over D
    D = m["distance_Mpc"] * MPC_M
    light_travel_s = D / C_M_S
    central = m["delta_t_grb_s"] / light_travel_s        # ~ +4e-16 (GW faster by 1.74 s)
    lo, hi = m["published_bound_dv_over_c"]
    tfpt = 0.0
    inside = lo <= tfpt <= hi

    print(f"\n  distance D = {m['distance_Mpc']} Mpc -> light-travel time {light_travel_s:.3e} s")
    print(f"  GRB arrived {m['delta_t_grb_s']} s after merger -> naive central "
          f"(v_GW-c)/c ~ {central:+.1e}")
    print(f"  published bound (emission window {m['emission_window_s']} s): "
          f"[{lo:.1e}, {hi:.1e}]")
    print(f"  TFPT 0 inside bound: {inside}")
    verdict = ("consistency (kill-test passed): the single-Lorentz-cone prediction "
               "(v_GW - c)/c = 0 sits inside the GW170817 bound; a measured v_GW != c "
               "would falsify the gravity closure. Not a detection (standard physics "
               "predicts the same).") if inside else \
              "TENSION: 0 is outside the measured bound -- would falsify the shared cone"
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(
        {"tfpt_dv_over_c": tfpt, "naive_central": central, "bound": [lo, hi],
         "inside": inside, "light_travel_s": light_travel_s, "verdict": verdict,
         "reference": m["reference"]}, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
