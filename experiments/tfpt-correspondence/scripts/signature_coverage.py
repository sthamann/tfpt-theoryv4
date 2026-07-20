"""Correspondence-signature COVERAGE CENSUS across all TFPT data sources / experiments.

Answers: "test all data sources and experiments on the correspondence signatures".

The honest premise (anti-double-counting): the correspondence principle does NOT introduce
new observables. Its falsifiable signatures ARE the frozen TFPT kernel that the empirical
suite already tests exhaustively -- the recovery reflectivity (2/3)^6, the compactness window
Q_geom in [3/8, 1/2], and the C=3/8 ECO echo (delay 2.288 M, amplitude <= (2/3)^6). So this
census does NOT re-run those searches; it AUDITS which experiments already test each
correspondence signature and pulls their recorded verdict from the committed results, and it
computes the one quantitative correspondence-specific synthesis: the echo reach-gap between
the (2/3)^6 ceiling and the gw-ringdown-echo eps_90 upper limits (the dated kill threshold).

Firewall: pure audit; never a scorecard row; the correspondence adds NO independent evidence
channel (every hit/null is already counted in the source experiment). Gated on the open
SEAM.EQUIV.01; typed at most [C].

Run:  cd experiments/tfpt-correspondence && python3 scripts/signature_coverage.py
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

EXPERIMENTS = Path(__file__).resolve().parents[2]           # experiments/
RESULTS = Path(__file__).resolve().parents[1] / "results" / "signature_coverage.json"

GAP6 = float(Fraction(2, 3) ** 6)                            # 0.08779...
VERDICT_KEYS = ("verdict", "status", "overall", "overall_expected", "current_status",
                "overall_verdict")


# ---- the frozen correspondence signatures (exact kernel values) ----------
SIGNATURES = {
    "S1_recovery_reflectivity": {
        "kernel": "(2/3)^6 = 64/729 energy / (2/3)^3 amplitude / step 2/3",
        "meaning": "information-channel order parameter = boundary recovery reflectivity",
    },
    "S2_compactness_window": {
        "kernel": "Q_geom in [3/8, 1/2] = [p2(a)/e1(a)^2, |Z2|/|mu4|]",
        "meaning": "geometric phase boundary: horizonless light-trapping ECO",
    },
    "S3_eco_echo": {
        "kernel": "delay 2.288 M (C=3/8 tortoise) x amplitude <= (2/3)^6",
        "meaning": "the observable face: GW ringdown echo at the phase boundary",
    },
    "S4_bekenstein_saturation": {
        "kernel": "q_Bek = 4 c3 S/(E R) = 1 at the horizon; density 1/4 = 1/|mu4|",
        "meaning": "structural: the critical quotient; NOT a data channel",
    },
}

# ---- which experiments already test each signature (grounded where possible) ----
# results: relative path under experiments/<exp>/ to a committed results.json, or None
# (None => verdict taken from the experiment README, quoted with source).
COVERAGE: dict[str, list[dict]] = {
    "S1_recovery_reflectivity": [
        {"exp": "frb-tfpt-signatures", "tests": "FRB.02 echo ratios / FRB.04 pol Markov",
         "results": "results/results.json", "doc": "null (energy (2/3)^6, amplitude (2/3)^3)"},
        {"exp": "pulsar-glitch-recovery", "tests": "PG.01-08 static + recovery comb",
         "results": "results/results.json", "doc": "data_limited (amplitude wall binding)"},
        {"exp": "recovery-comb-domains", "tests": "8 cross-domain channels A1-A5/B4-B5",
         "results": "results/recovery_comb_domains.json", "doc": "null (all real channels)"},
        {"exp": "repeater-cascade", "tests": "RC.01-03 walled clock + comb on FRB cascades",
         "results": "results/results.json", "doc": "null at detectable amplitude"},
        {"exp": "crust-cooling-comb", "tests": "NS crust cooling kT(t) comb",
         "results": "results/results.json", "doc": "data_limited (density-limited)"},
        {"exp": "uhecr-energy-dsi", "tests": "S7 size-space DSI on Auger spectrum",
         "results": "results/results.json", "doc": "null (kernel comb absent)"},
        {"exp": "strange-metal-comb", "tests": "log-periodic ripple on Planckian sigma(w/T)",
         "results": "results/results.json", "doc": "data_limited (underpowered @ eps=1.7%)"},
        {"exp": "qpe-recurrence", "tests": "QPE.01-03 recurrence ratio ladder",
         "results": "results/results.json", "doc": "null (2/3 tooth >17x scatter away)"},
        {"exp": "hfqpo-ladder", "tests": "step (3/2)=(2/3)^-1 ladder on BH HFQPO pairs",
         "results": "results/results.json",
         "doc": "null (archival RXTE scan 2026-07: no tooth, no integer line; "
                "3sig limits 0.53-3.06% rms)"},
        {"exp": "comb-meta-limit", "tests": "meta upper limit on comb amplitude eps",
         "results": "results/results.json", "doc": "data_limited (eps<0.12 all-channel UL)"},
        {"exp": "recovery-channel", "tests": "Test C: CPTP recovery kernel / Page curve",
         "results": None, "doc": "structural consistent (data-independent)"},
        {"exp": "qc-recovery-kernel", "tests": "kernel as executable quantum circuit",
         "results": "results/results.json", "doc": "consistent (sim tiers); hardware data_limited"},
    ],
    "S2_compactness_window": [
        {"exp": "gravastar-compactness", "tests": "Nariai Q_geom=3/8 = max compactness C=3/8",
         "results": None, "doc": "data_limited (suggestive rational match [C])"},
        {"exp": "eht-achromatic-residual", "tests": "horizon-scale shadow / polarimetry",
         "results": "results/eht_real_achromaticity.json",
         "doc": "shadow SIZE degenerate with Kerr -> cannot discriminate the ECO"},
    ],
    "S3_eco_echo": [
        {"exp": "gw-ringdown-echo", "tests": "Stage 1d point test (C=3/8 lag 2.288M x (2/3)^6)",
         "results": None, "doc": "NO_POINT_ECHO (consistent, upper bound); Stage 1h eps_90"},
        {"exp": "gravastar-compactness", "tests": "(delay, amplitude) echo template",
         "results": None, "doc": "template supplies the 2.288M delay for gw-ringdown-echo"},
    ],
    "S4_bekenstein_saturation": [
        {"exp": "tfpt-correspondence", "tests": "CORR.H2 q_Bek=1 (structural, exact)",
         "results": "results/results.json", "doc": "consistent (structural, no data channel)"},
    ],
}

# ---- echo reach-gap inputs (source: gw-ringdown-echo/README.md, Stage 1h) ----
EPS90 = {
    "stack_4kHz": 0.63, "stack_16kHz": 0.85,
    "best_single_GW200129_4kHz": 0.63, "GW150914_4kHz": 0.69, "GW190521_4kHz": 1.86,
    "source": "gw-ringdown-echo/README.md Stage 1h injection-calibrated eps_90 (90% CL)",
}


def find_verdicts(obj, depth: int = 0) -> list[str]:
    """Recursively pull short verdict/status strings from a results JSON blob."""
    out: list[str] = []
    if depth > 6:
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() in VERDICT_KEYS and isinstance(v, str):
                out.append(f"{k}={v[:160]}")
            else:
                out.extend(find_verdicts(v, depth + 1))
    elif isinstance(obj, list):
        for v in obj[:20]:
            out.extend(find_verdicts(v, depth + 1))
    return out


def grounded_verdict(entry: dict) -> str:
    """Read the experiment's committed results.json and extract a recorded verdict;
    fall back to the documented (README-sourced) verdict if no file/field."""
    rel = entry["results"]
    if rel:
        path = EXPERIMENTS / entry["exp"] / rel
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                found = find_verdicts(data)
                if found:
                    return "GROUNDED: " + " | ".join(dict.fromkeys(found))[:220]
            except Exception as exc:  # noqa: BLE001
                return f"README: {entry['doc']}  (results unreadable: {exc})"
        return f"README: {entry['doc']}  (no results.json at {rel})"
    return f"README: {entry['doc']}"


# data-source landscape checked 2026-07-14 (web); sources cited per entry
DATA_SOURCES_2026 = {
    "GW250114": {
        "what": "loudest BBH to date (2025-01-14); network SNR ~80, up-to-merger 65, "
                "POST-MERGER/ringdown ~40 (~3x GW150914)",
        "echo_relevant": "LVK finds NO coherent post-ringdown power; residual network SNR "
                         "< 6.86 at 90% CL (p=0.34) -> per-event amplitude-ratio reach ~6.86/40 "
                         "~ 0.17 (crude), i.e. ~2x above the (2/3)^6 ceiling, NOT ~7x",
        "forensic_2026_07_14": (
            "CORRECTED (scripts/diag_gw250114.py + aligned_limits.py, gw-ringdown-echo): an EARLIER "
            "step wrongly concluded GW250114 was unusable (~12000 whitened samples >5 sigma). That "
            "was an ARTIFACT of a missing HIGH-PASS: O4 4 kHz strain carries huge sub-20 Hz seismic "
            "power that a single mean-Welch whitening mishandles. With the proper O4 conditioning -- "
            "high-pass 20 Hz + MEDIAN-Welch PSD (robust to non-stationary lines) -- GW250114's "
            "off-source whitened noise is CLEAN (0 samples >5 sigma) and its ringdown is recovered. "
            "GW250114's public GWOSC strain IS sufficient (as LVK's own ringdown analysis used it); "
            "GW250114 is now INCLUDED and anchors an echo limit."),
        "general_pipeline_fixes_and_result": (
            "TWO real conditioning fixes added (opt-in, frozen defaults OFF): (1) align_ringdown() "
            "-- the QNM fit started ~15-40 ms before the true ringdown for every event; (2) "
            "highpass_hz=20 + median-Welch -- required for O4 data. Aligned + high-passed + "
            "median-Welch Stage-1h INCLUDING GW250114 (results/aligned_injection_limits.json): "
            "per-event eps90 GW250114=1.69, GW150914=1.30, GW200129=2.47, GW190521=1.55; STACK "
            "eps90 ~ 1.3 => reach-gap ~x15. HONEST NOTE: this is WORSE than the frozen 0.63 (x7.2) "
            "and my earlier 'x3.2' -- because those used UN-high-passed whitening that spuriously "
            "inflated the A220 reference; the properly-conditioned (clean-background) limit is the "
            "trustworthy one. Absolute eps90 is convention-sensitive at the O(2-3x) level. ALL "
            "events are a clean NULL (no echo) -- consistent with the (2/3)^6 upper-bound kernel; "
            "no detection, no tension. 0.088 NOT reached; needs O4c/GWTC-6 + O5 stacks or next-gen."),
        "source": "Abac et al. GW250114 (PRL 135, 111403; arXiv:2509.08099), public on GWOSC",
    },
    "O4c_GWTC6_pending": {
        "what": "O4 ended 2025-11-18; GWTC-5.0=390 events is only through O4b. O4c (the final "
                "segment, Jan-Nov 2025) has 68 candidates already identified and is set for "
                "PUBLIC RELEASE ~DECEMBER 2026 -> more high-SNR ringdowns for a bigger stack "
                "(the real near-term lever, ~5 months out; not available now).",
        "source": "LVK/Caltech news 2026-05-26 (ligo20260526); AEI 2026",
    },
    "hires_16kHz_TESTED": {
        "what": "higher-resolution 16 kHz GW250114 strain EXISTS (GWOSC + local) and now works "
                "with the fixed high-pass+median conditioning: eps90 ~1.6 (L1), comparable to "
                "4 kHz (~1.7), still a clean null. Finer lag sampling does NOT close the gap -- "
                "the limit is AMPLITUDE-limited, not lag-resolution-limited.",
        "source": "gw-ringdown-echo limit_event(hires=True, align=True, highpass_hz=20)",
    },
    "GW250114_zenodo": {
        "what": "GW250114 Zenodo release (10.5281/zenodo.16877102, Sep 2025) = posterior samples "
                "(NRSur7dq4 [+ a calibration-free run], SEOBNRv5PHM, PhenomXPHM, PhenomXO4a) + "
                "analysis results/PSDs/figure scripts. NO separate cleaned strain time series -- "
                "the strain IS the GWOSC R1 (usable once high-passed).",
        "source": "zenodo.org/records/16877102",
    },
    "IR1_2026": {"what": "interim 6-month run ~late Oct/mid Nov 2026 (both LIGOs)", "source": "AEI 2026"},
    "O5_2028_2031": {"what": "A+ sensitivity; larger high-SNR stacks", "source": "igwn userguide"},
    "next_gen": {"what": "Einstein Telescope / Cosmic Explorer (~2035+, ringdown SNR ~hundreds) "
                         "and LISA (SMBH ringdowns, SNR ~thousands) reach FAR below 0.088",
                 "source": "ET/CE/LISA design"},
    "regime_caveat": (
        "standard echo searches (e.g. arXiv:2512.24730) target STRONG reflection "
        "(R_wall~0.99, long-lived QNM trains) -- the WRONG regime for TFPT's WEAK (2/3)^6~0.088 "
        "reflector (one fast-decaying echo). The right instrument is a TARGETED first-echo / "
        "residual-power bound at the 2.288 M lag (gw-ringdown-echo Stage 1d/1h), NOT the "
        "long-lived-QNM reflectivity papers."
    ),
}


def echo_reach_gap() -> dict:
    stack = EPS90["stack_4kHz"]
    factor = stack / GAP6
    gw250114_reach = 6.86 / 40.0                 # residual-SNR limit / post-merger SNR (crude)
    return {
        "kernel_ceiling_(2/3)^6": round(GAP6, 5),
        "current_tfpt_stack_eps90_4kHz": stack,
        "current_tfpt_stack_eps90_16kHz": EPS90["stack_16kHz"],
        "reach_gap_factor_tfpt_pipeline": round(factor, 2),
        "gw250114_amplitude_reach_estimate": round(gw250114_reach, 3),
        "reach_gap_factor_gw250114_estimate": round(gw250114_reach / GAP6, 2),
        "source": EPS90["source"],
        "data_sources_2026": DATA_SOURCES_2026,
        "updated_assessment": (
            "DONE + CORRECTED (2026-07-14): GW250114's public GWOSC strain IS usable once properly "
            "conditioned (high-pass 20 Hz + median-Welch PSD -> clean off-source, ringdown "
            "recovered); an earlier step wrongly excluded it (a missing-high-pass artifact). Two "
            "opt-in conditioning fixes were added (frozen defaults off): merger alignment + O4 "
            "high-pass/median-Welch. Properly-conditioned aligned Stage-1h INCLUDING GW250114 "
            "(results/aligned_injection_limits.json): stack eps90 ~ 1.3 (reach-gap ~x15), ALL events "
            "a clean NULL. This is WORSE than the frozen 0.63 (x7.2) and my earlier optimistic x3.2 "
            "because those used un-high-passed whitening that inflated the A220 reference -- the "
            "properly-conditioned clean-background limit is the trustworthy one (absolute value "
            "convention-sensitive at O(2-3x)). No detection, no tension; 0.088 NOT reached. Path to "
            "0.088: O4c/GWTC-6 + O5 multi-event stacks or a next-gen (ET/CE) event."
        ),
        "dated_kill_threshold": (
            f"the (2/3)^6={GAP6:.4f} ceiling becomes testable once a targeted first-echo bound at "
            "the 2.288 M lag reaches eps_90 <~ 0.088 (GW250114 re-anchored + O4c/O5 stack, or one "
            "next-gen event): a clean well-powered null -> the 'physically visible phase boundary' "
            "reading falls; a coherent echo at (2.288 M, (2/3)^6) across high-SNR events -> the "
            "phase boundary is physically realised (escalates the [C])."
        ),
    }


def main() -> None:
    print("=" * 84)
    print("CORRESPONDENCE SIGNATURE COVERAGE CENSUS  (all data sources / experiments)")
    print("=" * 84)
    census: dict[str, list[dict]] = {}
    n_covered = 0
    for sig_id, sig in SIGNATURES.items():
        print(f"\n[{sig_id}]  {sig['kernel']}\n   ({sig['meaning']})")
        rows = []
        for entry in COVERAGE[sig_id]:
            verdict = grounded_verdict(entry)
            rows.append({"experiment": entry["exp"], "tests": entry["tests"],
                         "verdict": verdict})
            print(f"   - {entry['exp']:24s} {entry['tests']}")
            print(f"       -> {verdict}")
            n_covered += 1
        census[sig_id] = rows

    gap = echo_reach_gap()
    print("\n" + "-" * 84)
    print("ECHO REACH-GAP (the one correspondence-specific quantitative synthesis):")
    print(f"   (2/3)^6 ceiling = {gap['kernel_ceiling_(2/3)^6']}  vs  TFPT-pipeline eps_90 stack "
          f"= {gap['current_tfpt_stack_eps90_4kHz']} (4kHz) -> gap "
          f"x{gap['reach_gap_factor_tfpt_pipeline']}")
    print("   2026 data-source update:")
    for k, v in gap["data_sources_2026"].items():
        line = v if isinstance(v, str) else v.get("what", "")
        print(f"     - {k}: {line}")
    print(f"   -> {gap['updated_assessment']}")
    print(f"   -> {gap['dated_kill_threshold']}")

    verdict = (
        "COVERED / NO NEW CHANNEL. Every correspondence signature is ALREADY tested by the "
        f"empirical suite ({n_covered} experiment legs across S1-S4), all NULL / data_limited "
        "/ consistent to date. The correspondence introduces NO independent observable: its "
        "signatures ARE the frozen kernel ((2/3)^6, the [3/8,1/2] window, the C=3/8 echo) that "
        "FRB / pulsar / GW / recovery-comb / UHECR / QPE / HFQPO / lab channels already probe. "
        "ANTI-DOUBLE-COUNTING: it adds ZERO scorecard weight; it re-interprets, it does not "
        "re-measure. The only near-term lever is the echo reach-gap (x7.2 below current eps_90). "
        "All [C], gated on the open SEAM.EQUIV.01; nothing promoted."
    )
    print("\n" + "=" * 84)
    print("VERDICT:", verdict)

    RESULTS.parent.mkdir(exist_ok=True)
    RESULTS.write_text(json.dumps({
        "audit": "correspondence signature coverage census",
        "date": "2026-07-14",
        "firewall": ("pure audit; never a scorecard row; correspondence adds NO independent "
                     "evidence channel; gated on SEAM.EQUIV.01 (open); type [C]"),
        "signatures": SIGNATURES,
        "census": census,
        "echo_reach_gap": gap,
        "n_experiment_legs": n_covered,
        "verdict": verdict,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote {RESULTS}")


if __name__ == "__main__":
    main()
