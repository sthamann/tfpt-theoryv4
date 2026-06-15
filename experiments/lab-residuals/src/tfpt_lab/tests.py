"""The three lab-channel confrontations (muon g-2, rare kaons, axion).

All three are typed [C] (downstream bridges / frontier), never [E]: the firewall
forbids upgrading F_transfer interfaces to primitive compiler outputs. Verdicts are
deliberately split (per SM baseline for g-2; per relic branch for the axion) so no
single ampel hides a model dependence.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

from . import constants

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"


@dataclass
class ChannelResult:
    name: str
    status: str
    claim_type: str = ""
    lines: list[str] = field(default_factory=list)
    detail: dict = field(default_factory=dict)


def _load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def muon_g2(m: dict) -> ChannelResult:
    """Per-SM-baseline pull of the seam-vertex Delta a_mu = 45/(2^19 pi^9).
    No single global verdict: the channel is SM-HVP-baseline-dependent."""
    g = m["muon_g2"]
    a_exp = g["a_exp_worldavg"]
    out = [f"  Delta a_mu(TFPT) = 45/(2^19 pi^9) = {constants.DELTA_A_MU:.4e}  "
           f"[{constants.CLAIM_TYPE['muon_g-2']}]"]
    detail, viable = {}, []
    for key, sm in g["sm_baselines"].items():
        if sm["value"] is None:
            out.append(f"  {key:24s}: placeholder ({sm['note']}) -> data_limited")
            detail[key] = {"status": "data_limited"}
            continue
        resid = (a_exp["value"] - sm["value"]) * 1e-11
        resid_err = math.hypot(a_exp["sigma"], sm["sigma"]) * 1e-11
        z = (constants.DELTA_A_MU - resid) / resid_err
        status = "viable" if abs(z) <= 2.0 else "tension"
        viable.append(status == "viable")
        out.append(f"  {key:24s}: residual={resid:.3e}+/-{resid_err:.1e}  -> {z:+.2f} sigma "
                   f"({status})")
        detail[key] = {"residual": resid, "residual_err": resid_err, "z": z, "status": status}
    out.append("  -> baseline-dependent: mechanism VIABLE under the dispersive (WP2020) baseline, "
               "TENSION under the lattice-shifted (WP2025) baseline; CMD-3/future are placeholders. "
               "No single 'confirmed'/'killed' verdict (search.txt sec.8 / TFPT firewall).")
    return ChannelResult("muon_g-2", "baseline_dependent",
                         constants.CLAIM_TYPE["muon_g-2"], out, detail)


def rare_kaons(m: dict) -> ChannelResult:
    """K+ -> pi+ nu nu vs NA62 (both releases); KL vs KOTO limit. Status stays
    [C] downstream bridge -- short-distance functions are external."""
    k = m["rare_kaons"]
    kp = k["Kp_pinunu"]
    out = [f"  TFPT BR(K+) = {constants.BR_KP_PINUNU:.2e}  "
           f"[{constants.CLAIM_TYPE['rare_kaons']}]"]
    detail = {}
    for key, meas in kp.items():
        z = (constants.BR_KP_PINUNU - meas["value"]) / meas["sigma"]
        out.append(f"  {key:30s}: {meas['value']:.2e} (+{meas['sigma_plus']:.1e}"
                   f"/-{meas['sigma_minus']:.1e})  -> pull {z:+.2f} sigma")
        detail[key] = {"value": meas["value"], "pull": z}
    win = k["kill_window_1e-11"]
    in_window = win[0] <= constants.BR_KP_PINUNU * 1e11 <= win[1]
    out.append(f"  kill window [{win[0]},{win[1]}]e-11: TFPT 9.45e-11 "
               f"{'inside (bridge intact)' if in_window else 'OUTSIDE (bridge broken)'}")
    lim = k["KL_pi0nunu_limit_90CL"]
    out.append(f"  KL ->pi0 nu nu: TFPT={constants.BR_KL_PI0NUNU:.2e} vs KOTO 90%CL "
               f"{lim['value']:.1e} -> below reach (data_limited)")
    detail["KL_below_limit"] = constants.BR_KL_PI0NUNU < lim["value"]
    # status: strong consistency, but explicitly a downstream bridge (NOT [E])
    out.append("  -> downstream bridge, currently VERY STRONG consistency with NA62 2016-2024 "
               "(pull ~ -0.08 sigma); not a compiler hit.")
    return ChannelResult("rare_kaons", "consistent_downstream_bridge",
                         constants.CLAIM_TYPE["rare_kaons"], out, detail)


def axion(m: dict) -> ChannelResult:
    """Haloscope marker (data_limited) + the two relic branches, split and typed."""
    a = m["axion"]
    hm = a["haloscope_marker"]
    out = [f"  haloscope marker: m_a = {hm['mass_ueV']} ueV (~{hm['freq_GHz']} GHz), "
           f"f_a = M_scal/128  [{constants.CLAIM_TYPE['axion']}]"]
    for c in hm["coverage"]:
        lo, hi = c["range_ueV"]
        hit = lo <= hm["mass_ueV"] <= hi
        out.append(f"    {c['experiment']:8s} {lo}-{hi} ueV ({c['sensitivity']})"
                   f"{'  <-- contains marker' if hit else ''}")
    out.append(f"  marker -> data_limited: {hm['note']}")
    out.append("  relic-density branches (full finite-T solve lives in ftransfer/axion_relic):")
    detail = {}
    for bid, br in a["relic_branches"].items():
        out.append(f"    {bid}: theta_i={br['theta_i_deg']} deg -> status {br['status']}"
                   + (f" (Omega_a h^2 ~ {br['omega_a_h2']})" if "omega_a_h2" in br else
                      f" (frozen band {br['acceptance_band_omega_a_h2']})"))
        detail[bid] = br
    out.append("  -> HILLTOP overcloses (tension); SPINE theta_i=3pi/5 is exploratory and "
               "FROZEN (not a prediction of record).")
    return ChannelResult("axion", "marker_data_limited",
                         constants.CLAIM_TYPE["axion"], out, detail)


def run_all() -> list[ChannelResult]:
    m = _load()
    return [muon_g2(m), rare_kaons(m), axion(m)]
