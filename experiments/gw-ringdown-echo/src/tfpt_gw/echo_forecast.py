"""Catalog-level forecast for the TFPT ringdown-echo amplitude-ratio test.

The full test is a strain-residual search (free lag, fixed ratio (2/3)^6, Bayes
factors stacked over events, with time-slide / inverted-template / free-ratio nulls).
That needs GWOSC strain (~GB/event) and is out of scope here. What we CAN do from the
public GWTC catalogue is the **sensitivity forecast**: given each event's network
SNR, how loud would a maximal (2/3)^6 echo be, and can a stacked search detect or
only bound it? That decides whether the strain-level test is even worth running.

Per event the echo SNR is bounded by
    rho_echo  <=  f_rd * rho_net * (echo power factor) ,
with f_rd the ringdown SNR fraction; the conservative bound takes f_rd = 1.
Stacking N events adds in quadrature.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path

from . import constants

DATA = Path(__file__).resolve().parents[2] / "data" / "gwtc_events.csv"
MIN_MFINAL = 5.0        # exclude BNS / NSBH-light remnants; keep BH ringdowns


@dataclass
class EchoForecast:
    n_events: int = 0
    n_bbh: int = 0
    top: list[dict] = field(default_factory=list)
    stacked_echo_snr_max: float = 0.0       # conservative (f_rd = 1)
    stacked_echo_snr_real: float = 0.0      # f_rd = RINGDOWN_FRACTION
    detectable_max: bool = False
    detectable_real: bool = False
    verdict: str = ""


def _rows():
    out = []
    with open(DATA, newline="") as fh:
        for r in csv.DictReader(fh):
            try:
                snr = float(r["snr"])
            except (TypeError, ValueError):
                continue
            try:
                mfinal = float(r["mfinal"])
            except (TypeError, ValueError):
                mfinal = float("nan")
            out.append({"name": r["name"], "snr": snr, "mfinal": mfinal,
                        "catalog": r["catalog"]})
    return out


def forecast() -> EchoForecast:
    rows = _rows()
    bbh = [r for r in rows if math.isfinite(r["mfinal"]) and r["mfinal"] >= MIN_MFINAL]
    res = EchoForecast(n_events=len(rows), n_bbh=len(bbh))
    if not bbh:
        res.verdict = "no ringdown-capable events in catalogue"
        return res
    f = constants.ECHO_POWER_FACTOR
    for r in bbh:
        r["echo_snr_max"] = r["snr"] * f
        r["echo_snr_real"] = r["snr"] * constants.RINGDOWN_FRACTION * f
    bbh.sort(key=lambda r: r["snr"], reverse=True)
    res.top = [{"name": r["name"], "snr": round(r["snr"], 1),
                "mfinal": round(r["mfinal"], 1),
                "echo_snr_max": round(r["echo_snr_max"], 2),
                "echo_snr_real": round(r["echo_snr_real"], 2)} for r in bbh[:8]]
    res.stacked_echo_snr_max = math.sqrt(sum(r["echo_snr_max"] ** 2 for r in bbh))
    res.stacked_echo_snr_real = math.sqrt(sum(r["echo_snr_real"] ** 2 for r in bbh))
    res.detectable_max = res.stacked_echo_snr_max >= constants.DET_THRESHOLD
    res.detectable_real = res.stacked_echo_snr_real >= constants.DET_THRESHOLD

    # NOTE: stage = catalog_feasibility. These are SENSITIVITY-CENSUS statements about
    # whether a future strain-level matched-filter search could detect/bound a (2/3)^6
    # echo. They are NOT echo detection or non-detection claims.
    if res.detectable_real:
        res.verdict = (f"catalog-feasibility: a maximal (2/3)^6 echo would be reachable by a "
                       f"stacked strain search (stacked rho_echo ~ {res.stacked_echo_snr_real:.1f} "
                       f">= {constants.DET_THRESHOLD:.0f}) -> the strain-level test is worth running; "
                       f"no echo claim is made at catalog level")
    elif res.detectable_max:
        res.verdict = (f"catalog-feasibility: a maximal (2/3)^6 echo is near the threshold of "
                       f"stacked reach (conservative {res.stacked_echo_snr_max:.1f}, realistic "
                       f"{res.stacked_echo_snr_real:.1f}); a strain-level search could BOUND it "
                       f"-> data-limited until strain matched-filtering is run")
    else:
        res.verdict = (f"catalog-feasibility: even stacked, a (2/3)^6 echo is below reach "
                       f"(~{res.stacked_echo_snr_real:.1f}) -> current GWTC cannot test it; "
                       f"data-limited")
    return res
