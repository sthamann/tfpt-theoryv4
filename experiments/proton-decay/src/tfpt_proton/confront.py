"""Build the preregistered proton-decay confrontation.

For each E8-allowed Higgs content x {1-loop, 2-loop}, compute the two-step M_PS/M_GUT, then
tau_p(p->e+pi0) and tau_p(p->nubar K+) with their uncertainty bands, and confront each
channel against the current Super-K limit + the Hyper-K / DUNE / JUNO future reach. Emit a
verdict enum per channel/branch in {consistent, tension, kill, data_limited}.

Preregistration (frozen BEFORE looking at the limits): see README "Preregistration". The
verdict thresholds (HAD_BAND=3, BAND_SOFTNESS=1.3, R_nuK in [0.1,1.0]) and the kill rule
live in ``proton.py`` as module constants and are not tuned to the data.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from tfpt_proton import proton, unification

DATA = Path(__file__).resolve().parents[2] / "data" / "limits.json"

# Human-readable branch labels + the frozen E8 story for each content.
_BRANCH_NOTE = {
    "minimal_16H": "minimal renormalisable 16-Higgs (bidoublet + (4,1,2)); the minimal E8 10+16",
    "+(15,1,1)_45": "+ the single SU(4)-adjoint (15,1,1) = the one E8-allowed 45 (v247)",
}
_CHANNEL_BAND = {"e+pi0": proton.epi0_band, "nubarK+": proton.nubarK_band}


def _load_limits() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))["channels"]


def analyze() -> dict:
    limits = _load_limits()
    points = unification.scan()

    scales: dict[str, dict] = {}
    confrontation: list[dict] = []
    for p in points:
        scales.setdefault(p.content, {})[p.loop] = {
            "M_PS_GeV": p.M_PS_GeV, "M_GUT_GeV": p.M_GUT_GeV,
            "alpha_gut_inv": p.alpha_gut_inv, "ratio_to_scalaron": p.ratio_to_scalaron,
            "valid": p.valid, "b_ps": list(p.b_ps),
        }
        for ch_key, band_fn in _CHANNEL_BAND.items():
            tau_c, tau_lo, tau_hi = band_fn(p.M_GUT_GeV, p.alpha_gut_inv)
            cv = proton.confront_channel(
                limits[ch_key]["label"], tau_c, tau_lo, tau_hi,
                limits[ch_key]["current"], limits[ch_key]["future"])
            row = asdict(cv)
            row.update(branch=p.content, loop=p.loop)
            confrontation.append(row)

    branch_summary = _branch_summary(confrontation)
    return {
        "meta": _meta(),
        "scales": scales,
        "confrontation": confrontation,
        "branch_summary": branch_summary,
        "verdict": _verdict_text(scales, branch_summary, confrontation),
    }


def _lookup(rows: list[dict], branch: str, loop: str, channel_label: str) -> dict:
    return next(r for r in rows if r["branch"] == branch and r["loop"] == loop
               and r["channel"] == channel_label)


def _branch_summary(rows: list[dict]) -> dict:
    epi0 = "p -> e+ pi0"
    out: dict[str, dict] = {}
    for branch in unification.E8_CONTENTS:
        v1 = _lookup(rows, branch, "1loop", epi0)["verdict"]
        v2 = _lookup(rows, branch, "2loop", epi0)["verdict"]
        if v1 == "kill" and v2 == "kill":
            overall = "kill"
            headline = "EXCLUDED at both loop orders (Super-K, golden e+pi0 channel)"
        elif "kill" in (v1, v2) or "tension" in (v1, v2):
            overall = "tension"
            headline = (f"survives at 1-loop ({v1}) but is a {v2} at 2-loop -- "
                        "structurally marginal proton-safety (only one E8 45)")
        else:
            overall = v1
            headline = f"1-loop {v1}, 2-loop {v2}"
        out[branch] = {
            "note": _BRANCH_NOTE[branch],
            "e+pi0_verdict_1loop": v1, "e+pi0_verdict_2loop": v2,
            "overall_golden_channel": overall, "headline": headline,
        }
    return out


def _meta() -> dict:
    return {
        "title": "TFPT proton-decay confrontation (carrier-native Pati-Salam -> SO(10), branch B)",
        "axioms": {"c3": unification.C3, "c3_expr": "1/(8 pi)",
                   "Mbar_GeV": unification.MBAR, "M_scalaron_GeV": unification.M_SCALARON,
                   "M_scalaron_expr": "c3^{7/2} * Mbar"},
        "mechanism": "dim-6 SO(10)/SU(5) X,Y gauge-boson exchange at M_GUT; "
                     "tau ~ 1e36 (M_GUT/1e16)^4 (alpha_GUT^-1/40)^2 yr",
        "hadronic_band_O": proton.HAD_BAND,
        "band_softness": proton.BAND_SOFTNESS,
        "R_nuK_band": list(proton.R_NUK_BAND),
        "verdict_enum": list(proton.VERDICTS),
        "reproduces": "verification/v266 (PS.PROTON.02), v249 (PS.RGTEST.01); "
                      "experiments/gauge-unification/results/pati_salam.json",
        "firewall": (
            "tau_p is a DOWNSTREAM/BRANCH prediction of the OPTIONAL gauged carrier-PS -> "
            "SO(10) UV branch B (v249/v266/v385), NOT a primitive compiler output. Never [E], "
            "never \\veri{}. The default reading A is boundary-only (no gauged intermediate "
            "group -> no M_GUT X,Y bosons -> no dim-6 proton decay; v385). Generic proton "
            "decay is a generic-GUT signature; the TFPT-specific sharpening is (i) M_PS = "
            "scalaron-scale coincidence, (ii) 126 forbidden + only one 45 => structurally "
            "marginal proton-safety, (iii) minimal 16-content already excluded."
        ),
    }


def _verdict_text(scales: dict, summary: dict, rows: list[dict]) -> str:
    epi0 = "p -> e+ pi0"
    m1 = scales["minimal_16H"]["1loop"]
    s1 = scales["+(15,1,1)_45"]["1loop"]
    s2 = scales["+(15,1,1)_45"]["2loop"]
    t_min = _lookup(rows, "minimal_16H", "1loop", epi0)
    t_s1 = _lookup(rows, "+(15,1,1)_45", "1loop", epi0)
    t_s2 = _lookup(rows, "+(15,1,1)_45", "2loop", epi0)
    nuk_s1 = _lookup(rows, "+(15,1,1)_45", "1loop", "p -> nubar K+")
    return (
        f"Carrier-native Pati-Salam -> SO(10) proton decay (OPTIONAL gauged UV branch B; NOT "
        f"the default boundary-only reading A). M_PS lands on the TFPT scalaron scale "
        f"M_s={unification.M_SCALARON:.2e} GeV (x{m1['ratio_to_scalaron']:.2f}-"
        f"{s1['ratio_to_scalaron']:.2f}), independent of the gauge running -- the TFPT-specific "
        f"coincidence. GOLDEN CHANNEL p->e+pi0: (1) minimal 16-content M_GUT={m1['M_GUT_GeV']:.2e} "
        f"-> tau_p={t_min['tau_central_yr']:.2e} yr is EXCLUDED by Super-K "
        f"({t_min['current_limit_yr']:.1e} yr) even at the optimistic band edge -> KILL. "
        f"(2) The single E8-allowed 45 +(15,1,1) raises M_GUT to {s1['M_GUT_GeV']:.2e} -> "
        f"tau_p={t_s1['tau_central_yr']:.2e} yr at 1-loop -> CONSISTENT and decisively probed by "
        f"{t_s1['best_future_experiment']}. (3) But at 2-loop M_GUT drops to {s2['M_GUT_GeV']:.2e} "
        f"-> tau_p={t_s2['tau_central_yr']:.2e} yr < Super-K -> a latent TENSION (only the "
        f"optimistic O({proton.HAD_BAND:.0f}) hadronic edge / GUT-threshold headroom saves it). "
        f"So the whole PS branch is proton-safe ONLY with +(15,1,1) and ONLY marginally -- the E8 "
        f"hull supplies just one 45 (v247), so this is a sharp, dated kill-test, not a knob. "
        f"Second channel p->nubar K+ (DUNE/JUNO-optimised) is SUBDOMINANT in non-SUSY dim-6 gauge "
        f"mediation: tau_p~{nuk_s1['tau_central_yr']:.1e} yr for +(15,1,1) sits above even the "
        f"next-gen reach -> data_limited (R_nuK is an external nuisance, not a TFPT primitive). "
        f"FIREWALL: tau_p is a downstream branch prediction, never [E]/\\veri{{}}; if only the "
        f"minimal PS stage is gauged its leptoquarks mediate rare LFV, not p->e+pi0 (v385)."
    )
