"""``tfpt-gravastar analyze`` -- the Nariai 3/8 <-> gravastar-compactness ECO leg.

Two independent constructions land on the SAME rational and the SAME de Sitter endpoint:

  * TFPT (horizon_readouts/v57): the Nariai geometric quotient ``Q_geom = 3/8`` (Koide-form
    quotient of the three horizon roots at the maximal de Sitter--black-hole state), with the
    pure de Sitter limit ``= 1/2``.
  * Jampolski & Rezzolla (2026, arXiv:2509.15302): the MAXIMUM initial compactness
    ``C = 3/8`` above which collapse to a black hole is unavoidable (a de Sitter core
    nucleates -> gravastar), with the Schwarzschild horizon at ``C = 1/2``.

This runner (a) checks the normal-form match honestly (exact rational + shared endpoint, but
NOT a proven C<->Q_geom map -> typed [C], suggestive), (b) places ``C=3/8`` in the
compactness ladder ``1/3 < 3/8 < 4/9 < 1/2`` (above the photon-sphere/light-trapping
threshold, below Buchdahl and the horizon -> a horizonless echo candidate), and (c) turns it
into a concrete GW echo template: a tortoise-coordinate round-trip echo DELAY plus the TFPT
recovery-reflectivity amplitude bound ``(2/3)^6``.  It sharpens ``gw-ringdown-echo`` (which
fixes the amplitude ratio) with the missing time scale, and is explicit that the EHT shadow
SIZE is degenerate with a Kerr black hole.

Compactness convention: C = M/R (geometric, G=c=1); horizon at C=1/2, photon sphere at R=3M.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
RESULTS = Path(__file__).resolve().parents[2] / "results"


def tortoise(r: float, mass: float = 1.0) -> float:
    """Schwarzschild tortoise coordinate r* = r + 2M ln(r/2M - 1) (horizonless r>2M)."""
    return r + 2.0 * mass * math.log(r / (2.0 * mass) - 1.0)


def echo_delay_geometric(compactness: float) -> dict:
    """Round-trip echo delay (surface <-> photon sphere) in units of M, for an ECO of
    compactness C=M/R.  Closed form via tortoise r* and a numerical cross-check."""
    radius = 1.0 / compactness          # R/M  (M=1 geometric)
    r_ph = 3.0                          # photon sphere at 3M
    if radius <= 2.0:
        raise ValueError(f"C={compactness} is horizon/inside it (R={radius}M <= 2M)")
    light_trapping = radius < r_ph      # surface inside the photon sphere?
    dt_closed = 2.0 * (tortoise(r_ph) - tortoise(radius))
    # numerical cross-check: 2 * integral_R^{r_ph} dr / (1 - 2/r)
    rs = np.linspace(radius, r_ph, 20001)
    dt_numeric = 2.0 * float(np.trapezoid(1.0 / (1.0 - 2.0 / rs), rs))
    return {"radius_over_M": radius, "light_trapping": light_trapping,
            "delay_over_M_closed": dt_closed, "delay_over_M_numeric": dt_numeric}


def analyze(m: dict) -> dict:
    pred, ext = m["tfpt_prediction"], m["external_result"]
    lm = m["compactness_landmarks"]
    C = ext["max_compactness"]

    # (a) normal-form / rational match
    rational_match = math.isclose(pred["Q_geom_nariai"], ext["max_compactness"], abs_tol=1e-12)
    endpoint_match = math.isclose(pred["Q_geom_de_sitter"], ext["de_sitter_endpoint"], abs_tol=1e-12)

    # (b) compactness ladder
    ladder_ok = lm["photon_sphere"] < C < lm["buchdahl"] < lm["black_hole"]

    # (c) echo template -- OBSERVED delays scale with the DETECTOR-frame mass
    # M(1+z) (redshift correction, 2026-07-02; same fix as gw-ringdown-echo)
    echo = echo_delay_geometric(C)
    unit = m["constants"]["GMsun_over_c3_seconds"]
    redshifts = m.get("redshifts", {})
    delays_ms = {}
    for label in ("GW150914_remnant", "GW190521_remnant", "stellar_30"):
        mass_det = m["masses_solar"][label] * (1.0 + float(redshifts.get(label, 0.0)))
        delays_ms[label] = echo["delay_over_M_closed"] * mass_det * unit * 1e3  # ms

    # EHT shadow: critical impact parameter b_c = 3 sqrt(3) M (photon sphere) -> Kerr-degenerate
    b_c_over_M = 3.0 * math.sqrt(3.0)

    verdict = (
        f"SUGGESTIVE NORMAL-FORM MATCH ([C], data_limited): Nariai Q_geom and the "
        f"Jampolski-Rezzolla max compactness are the SAME rational 3/8 with the SAME de Sitter "
        f"endpoint 1/2 -- but no explicit C<->Q_geom map is proven, so it is a structural echo, "
        f"not an identity. C=3/8 sits in 1/3<3/8<4/9<1/2: a HORIZONLESS light-trapping ECO. As a "
        f"GW echo template it predicts an OBSERVED round-trip delay ~{delays_ms['GW150914_remnant']:.2f} ms "
        f"(GW150914: 62 Msun source frame x (1+z), z=0.09) with amplitude ratio <= "
        f"(2/3)^6={pred['echo_amplitude_ratio_bound']:.4f}; "
        f"this is the (delay, amplitude) pair gw-ringdown-echo was missing. EHT shadow size "
        f"(b_c=3 sqrt3 M) is DEGENERATE with Kerr -> echoes, not the shadow, are the discriminator."
    ) if (rational_match and endpoint_match and ladder_ok and echo["light_trapping"]) else \
        "STRUCTURE BROKEN: rational/endpoint/ladder/light-trapping check failed (see fields)."

    return {
        "rational_match_3_8": rational_match,
        "de_sitter_endpoint_match_1_2": endpoint_match,
        "compactness_ladder_ok": ladder_ok,
        "ladder": f"photon 1/3={lm['photon_sphere']:.4f} < C={C} < Buchdahl 4/9="
                  f"{lm['buchdahl']:.4f} < horizon 1/2={lm['black_hole']:.4f}",
        "echo": echo,
        "echo_delay_ms": {k: round(v, 4) for k, v in delays_ms.items()},
        "echo_amplitude_ratio_bound": pred["echo_amplitude_ratio_bound"],
        "eht_shadow_b_c_over_M": round(b_c_over_M, 4),
        "eht_shadow_degenerate_with_kerr": True,
        "status": "data_limited",
        "verdict": verdict,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT Nariai 3/8 <-> gravastar ECO echo template")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)
    m = json.loads(DATA.read_text(encoding="utf-8"))

    print("=" * 78)
    print("TFPT gravastar/ECO compactness  (Nariai Q_geom=3/8  <->  max compactness C=3/8)")
    print("=" * 78)
    if args.command == "audit":
        return 0

    res = analyze(m)
    print(f"  [a] rational match 3/8:        Q_geom(Nariai)=0.375 == C_max=0.375  -> "
          f"{res['rational_match_3_8']}")
    print(f"      de Sitter endpoint 1/2:    Q_geom(dS)=0.5      == C_dS=0.5       -> "
          f"{res['de_sitter_endpoint_match_1_2']}")
    print(f"  [b] compactness ladder:        {res['ladder']}  -> ok={res['compactness_ladder_ok']}")
    e = res["echo"]
    print(f"      C=3/8 surface at R={e['radius_over_M']:.4f} M (2M<R<3M) -> "
          f"light-trapping horizonless ECO = {e['light_trapping']}")
    print(f"  [c] echo round-trip delay:     {e['delay_over_M_closed']:.4f} M "
          f"(numeric {e['delay_over_M_numeric']:.4f} M)")
    for k, v in res["echo_delay_ms"].items():
        print(f"        {k:20s} -> {v:.3f} ms")
    print(f"      echo amplitude ratio bound: <= (2/3)^6 = {res['echo_amplitude_ratio_bound']:.4f}")
    print(f"  [EHT] shadow b_c = 3 sqrt3 M = {res['eht_shadow_b_c_over_M']:.4f} M  "
          f"(degenerate with Kerr: {res['eht_shadow_degenerate_with_kerr']})")
    print(f"\n-> {res['verdict']}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
