"""HFQPO.H3 — the ladder discriminator (the decisive, preregistered test).

The TFPT-kernel reading of a 3:2 pair is one step of a GEOMETRIC ladder, so it predicts a
third tooth at nu_3 = (3/2) nu_u = (3/2)^2 nu_l and FORBIDS integer harmonic/subharmonic
lines. The GR resonance/harmonic alternative predicts integer lines of nu_0 = nu_u/3 = nu_l/2
(k * nu_0; the marginal 92 Hz = 184/2 in XTE J1550-564 is exactly such a line). Tooth and
4*nu_0 line are >= 26 Hz apart in every source — resolvable at HFQPO widths (Q ~ 5-20).

Stage 1 (THIS version) is a literature census: what do published searches say at the tooth
frequencies? The census below is encoded from the cited papers (verified 2026-07-02); no
event data is touched. Stage 2 is the named archival RXTE PCA reanalysis in
hypotheses/hfqpo_v1.yaml (deliberately not run here).
"""

from __future__ import annotations

from typing import Any

from tfpt_hfqpo.constants import harmonic_fundamental, ladder_tooth

# Literature census at the tooth frequencies (encoded from published searches; the RXTE PCA
# band itself reaches ~kHz — Belloni+2012 searched 100-1000 Hz archive-wide — so the teeth
# are INSIDE the searched band, but no paper publishes a targeted detection OR a per-frequency
# upper limit at nu_3 = 1.5 * nu_u).
_CENSUS: dict[str, dict[str, str | bool]] = {
    "GRO J1655-40": {
        "published_detection_at_tooth": False,
        "published_upper_limit_at_tooth": False,
        "census": "450 Hz is the highest BH QPO frequency ever published (Strohmayer 2001, "
                  "ApJ 552, L49; 4.5% rms, 13-27 keV). Belloni+2012 (MNRAS 426, 1701) "
                  "searched 100-1000 Hz over 7108 archival PCA observations: 4 detections "
                  "for this source, all in the 300-450 Hz dichotomy; nothing near 661.5 Hz "
                  "and no per-frequency upper limit published there.",
    },
    "XTE J1550-564": {
        "published_detection_at_tooth": False,
        "published_upper_limit_at_tooth": True,   # generic in-band limit, not tooth-targeted
        "census": "Belloni+2012: 7 archive-wide detections, clustered near 180/280 Hz; "
                  "nothing at 414 Hz. Varniere & Rodriguez 2018 (ApJ 865, 113) refit the "
                  "stacked ~275 Hz group over 50-1000 Hz: 'no other peak is obvious' with "
                  "3 sigma upper limits ~1-1.8% rms for an additional HFQPO anywhere in the "
                  "considered range — the closest thing to a published tooth limit (the known "
                  "pair sits at 1.2-4.8% rms), but not targeted at 1.5 * nu_u.",
    },
    "GRS 1915+105": {
        "published_detection_at_tooth": False,
        "published_upper_limit_at_tooth": False,
        "census": "Belloni & Altamirano 2013 systematic RXTE search (MNRAS 432, 10): 51 "
                  "detections, 49 between 58-72 Hz, two isolated peaks at ~134/143 Hz; the "
                  "168/113 pair itself only appears in stacked PDS (Remillard & McClintock "
                  "2006). No feature and no published limit at 252 Hz.",
    },
    "H1743-322": {
        "published_detection_at_tooth": False,
        "published_upper_limit_at_tooth": False,
        "census": "Remillard+2006 (ApJ 637, 1002) searched 50-2000 Hz in 111 intervals: one "
                  "single->4sigma detection (239+-4 Hz); stacked detections 166/242 Hz only. "
                  "No feature reported near 363 Hz, no per-frequency upper limit given.",
    },
}

# Published integer-harmonic structures — the resonance/harmonic side of the discriminator.
_ANTI_KERNEL_RECORD = [
    {"source": "XTE J1550-564",
     "feature": "marginal broad 92 Hz = 184/2 (integer subharmonic); Remillard+2002 modelled "
                "92:184:276 as integer harmonics 1:2:3 of 92 Hz",
     "weight": "marginal (one observation group, broad)"},
    {"source": "GRS 1915+105",
     "feature": "simultaneous 34/68 Hz integer 1:2 pair (Belloni & Altamirano 2013); also the "
                "41/69 Hz pair (Strohmayer 2001)",
     "weight": "4.2 sigma (different frequency regime from the 168/113 pair)"},
]


def run_ladder(sources: list[dict[str, Any]]) -> dict[str, Any]:
    per_source: list[dict[str, Any]] = []
    for s in sources:
        if s["role"] != "consistent":
            continue
        nu_u = s["nu_upper_hz"]
        tooth, nu_0 = ladder_tooth(nu_u), harmonic_fundamental(nu_u)
        census = _CENSUS[s["name"]]
        per_source.append({
            "name": s["name"],
            "nu_upper_hz": nu_u,
            "ladder_tooth_hz": tooth,                 # TFPT: expect a peak HERE
            "harmonic_fundamental_hz": nu_0,          # resonance: integer lines k * nu_0
            "harmonic_line_4nu0_hz": 4.0 * nu_0,      # nearest integer line above nu_u
            "tooth_vs_4nu0_separation_hz": tooth - 4.0 * nu_0,   # = nu_u/6, resolvable
            **census,
        })
    return {
        "id": "HFQPO.H3_ladder_discriminator",
        "prediction": {
            "tfpt_ladder": "third QPO at nu_3 = (3/2) nu_u and NO integer harmonics",
            "resonance_alternative": "integer lines of nu_0 = nu_u/3 (e.g. 4 nu_0, nu_l/2)",
        },
        "per_source": per_source,
        "anti_kernel_record": _ANTI_KERNEL_RECORD,
        "stage1_finding": "the teeth lie INSIDE the band RXTE PCA archive searches covered "
                          "(100-1000 Hz), yet no published search targeted nu_3 = 1.5 nu_u and "
                          "no per-frequency upper limits exist at the tooth frequencies; the "
                          "only published third-frequency structures are INTEGER lines "
                          "(92 = 184/2; 34/68), which favour the harmonic alternative",
        "next_stage": "archival RXTE PCA event-data reanalysis specified in "
                      "hypotheses/hfqpo_v1.yaml (targets, ObsID groups, stacking selections, "
                      "detection/upper-limit rules); NOT run in this version",
        "verdict": "data_limited",
        "honesty": "even a future ladder hit would be [C]-tier: the ratio->ladder mapping is "
                   "not canonical TFPT output, and the GR-resonance explanation remains the "
                   "standing favorite",
    }
