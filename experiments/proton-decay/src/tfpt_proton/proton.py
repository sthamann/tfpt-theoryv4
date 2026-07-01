"""Proton-decay lifetimes and the preregistered confrontation verdict.

Mechanism: dim-6 gauge-boson-mediated decay by the superheavy SO(10)/SU(5) X,Y bosons at
M_GUT (the standard grand-unified operator). The golden channel is

    tau(p -> e+ pi0) ~ TAU16 * (M_GUT/1e16)^4 * (alpha_GUT^-1/40)^2   yr ,

with TAU16 = 1e36 the SU(5)/SO(10) benchmark at M_X=1e16, alpha_GUT=1/40. Lattice hadronic
matrix elements carry an O(3) band (HAD_BAND). Same formula as v266/v249/pati_salam.

FIREWALL (critical):
  * This dim-6 operator needs the FULL SO(10) completion (the M_GUT X,Y *diquark* bosons).
    If only the minimal Pati-Salam stage is gauged, its SU(4) leptoquarks mediate
    B-L-conserving q<->l (rare LFV, e.g. K_L -> mu e), NOT p -> e+ pi0 (v385). So tau_p is
    a DOWNSTREAM prediction of the OPTIONAL gauged-SO(10) UV branch B -- never a primitive
    compiler output, never [E] / \\veri{}. The default reading A is boundary-only.
  * Generic proton decay is a generic-GUT signature. The TFPT-specific sharpening is:
    (i) M_PS = scalaron scale coincidence; (ii) 126 forbidden + only ONE 45 (v247) =>
    structurally marginal proton-safety; (iii) the minimal 16-content is already excluded.

The second channel p -> nubar K+ (the DUNE / JUNO / SUSY-favoured mode) is SUBDOMINANT in
non-SUSY dim-6 gauge mediation. Its partial width is Gamma(nuK+) = R_nuK * Gamma(e+pi0),
where R_nuK is an O(1) hadronic/flavour factor that is an EXTERNAL nuisance (NOT a TFPT
primitive -- exactly as |Vcb|,|Vub| are nuisances in the rare-kaon bridge). We use the
generic gauge-mediation range R_nuK in [0.1, 1.0] -> tau(nuK+) in [1, 10] x tau(e+pi0).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

TAU16 = 1.0e36          # SU(5)/SO(10) benchmark tau at M_X=1e16, alpha_GUT=1/40 (yr)
HAD_BAND = 3.0          # O(3) hadronic matrix-element band (v266)
# "O(3)" is itself only order-of-magnitude, and GUT thresholds add headroom: an optimistic
# band edge landing within BAND_SOFTNESS of a limit is a TENSION, not a clean kill.
BAND_SOFTNESS = 1.3
R_NUK_BAND = (0.1, 1.0)  # Gamma(nuK+)/Gamma(e+pi0) external band (non-SUSY gauge mediation)

VERDICTS = ("consistent", "tension", "kill", "data_limited")


def tau_epi0(M_GUT: float, alpha_gut_inv: float) -> float:
    """tau(p -> e+ pi0) central value (yr)."""
    return TAU16 * (M_GUT / 1e16) ** 4 * (alpha_gut_inv / 40.0) ** 2


def epi0_band(M_GUT: float, alpha_gut_inv: float) -> tuple[float, float, float]:
    """(central, lo, hi) for p -> e+ pi0 with the O(3) hadronic band."""
    tau = tau_epi0(M_GUT, alpha_gut_inv)
    return tau, tau / HAD_BAND, tau * HAD_BAND


def nubarK_band(M_GUT: float, alpha_gut_inv: float) -> tuple[float, float, float]:
    """(central, lo, hi) for p -> nubar K+ = e+pi0 band folded with the R_nuK nuisance band.

    tau(nuK+) = tau(e+pi0) / R_nuK. Shortest lifetime uses (pessimistic e+pi0) / (largest R);
    longest uses (optimistic e+pi0) / (smallest R). Central uses the geometric means.
    """
    tau, lo, hi = epi0_band(M_GUT, alpha_gut_inv)
    r_lo, r_hi = R_NUK_BAND
    r_c = (r_lo * r_hi) ** 0.5
    return tau / r_c, lo / r_hi, hi / r_lo


@dataclass
class ChannelVerdict:
    channel: str
    tau_central_yr: float
    tau_lo_yr: float
    tau_hi_yr: float
    current_experiment: str
    current_limit_yr: float
    pull_dex: float               # log10(tau_central / current_limit); <0 => below limit
    verdict: str
    within_current_bound: bool    # central above the current 90% CL limit
    best_future_experiment: str = ""
    best_future_reach_yr: float = 0.0
    decisively_testable: bool = False
    note: str = ""
    provenance: dict = field(default_factory=dict)


def _core_verdict(tau_lo: float, tau_hi: float, limit_yr: float) -> str:
    """kill / tension / consistent vs a current 90% CL lower limit, using the band."""
    if tau_lo >= limit_yr:
        return "consistent"                      # even pessimistic ME clears the bound
    if tau_hi < limit_yr / BAND_SOFTNESS:
        return "kill"                            # even optimistic ME comfortably below -> excluded
    return "tension"                             # band brackets / edge within softness of the bound


def confront_channel(channel: str, tau_c: float, tau_lo: float, tau_hi: float,
                     current: dict, futures: list[dict]) -> ChannelVerdict:
    limit = current["tau_limit_yr"]
    core = _core_verdict(tau_lo, tau_hi, limit)
    best = max(futures, key=lambda f: f["tau_reach_yr"]) if futures else None

    verdict = core
    decisively = False
    note = ""
    if core == "consistent" and best is not None:
        # decisively testable if the band reaches down into the best future reach
        if tau_lo <= best["tau_reach_yr"]:
            decisively = True
            note = (f"clears the current bound; decisively probed by "
                    f"{best['experiment']} (reach {best['tau_reach_yr']:.1e} yr)")
        else:
            verdict = "data_limited"
            note = (f"clears the current bound AND lies above the best next-gen reach "
                    f"({best['experiment']} {best['tau_reach_yr']:.1e} yr) -> not testable soon")
    elif core == "tension":
        note = ("central lifetime is below the current limit; only the optimistic edge of the "
                "O(3) hadronic band (or GUT-threshold headroom) keeps it from a clean kill")
    elif core == "kill":
        note = "excluded: even the optimistic edge of the O(3) hadronic band is below the current limit"

    return ChannelVerdict(
        channel=channel,
        tau_central_yr=tau_c, tau_lo_yr=tau_lo, tau_hi_yr=tau_hi,
        current_experiment=current["experiment"], current_limit_yr=limit,
        pull_dex=math.log10(tau_c / limit),
        verdict=verdict,
        within_current_bound=tau_c >= limit,
        best_future_experiment=best["experiment"] if best else "",
        best_future_reach_yr=best["tau_reach_yr"] if best else 0.0,
        decisively_testable=decisively,
        note=note,
        provenance={"current": current.get("source", ""),
                    "future": [f.get("source", "") for f in futures]},
    )
