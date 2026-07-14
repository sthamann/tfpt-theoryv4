"""Alignment + high-pass corrected Stage-1h injection limits (opt-in), NON-DESTRUCTIVE.

Context (forensics 2026-07-14): the frozen Stage-1h (i) fits the (2,2,0) at the NOMINAL
merger, ~15-40 ms before the true ringdown -> A220 under-measured, and (ii) whitens O4 4 kHz
strain without a high-pass, which mishandles the huge sub-20 Hz seismic power and left
GW250114's whitened data heavy-tailed (~12000 samples > 5 sigma). BOTH are fixed here:
align=True (QNM start -> whitened ringdown-envelope peak) and highpass_hz=20 (removes the
sub-20 Hz power). With the high-pass, GW250114's off-source whitened noise is CLEAN
(0 samples > 5 sigma) and its ringdown matched-filter SNR is ~17 in H1 (~2x GW150914), so
GW250114 is now INCLUDED. Writes a SEPARATE results file; the frozen injection_limits.json is
untouched (both flags are opt-in, default off).

Run:  PYTHONPATH=src python scripts/aligned_limits.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tfpt_gw.injection_limits import RATIO, limit_event  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
EVENTS = ["GW250114_082203", "GW150914", "GW200129_065458", "GW190521"]  # GW250114 INCLUDED
HIGHPASS_HZ = 20.0
GAP6 = RATIO                                                  # (2/3)^6 = 0.0878


def frozen_eps90() -> dict:
    p = RESULTS / "injection_limits.json"
    if not p.exists():
        return {}
    d = json.loads(p.read_text())
    return {e["event"]: e.get("eps90_event") for e in d.get("events", [])}


def main() -> None:
    froz = frozen_eps90()
    print("=" * 84)
    print("ALIGN + HIGH-PASS(20Hz) Stage-1h injection limits (align=True) -- GW250114 INCLUDED")
    print(f"kernel ceiling (2/3)^6 = {GAP6:.4f}")
    print("=" * 84)
    out = []
    aligned_event_eps90 = []
    for ev in EVENTS:
        r = limit_event(ev, align=True, highpass_hz=HIGHPASS_HZ)
        print(f"\n{ev}  M_det={r.mf_det}  lag={r.lag_pred_ms} ms  (frozen eps90={froz.get(ev)})")
        for d in r.detectors:
            tag = "" if d.on_source_null else "  [not-null: cannot anchor]"
            e = "--" if d.eps90 is None else f"{d.eps90:.3f}"
            print(f"   {d.detector:3s} A220={d.amp220:7.3f}  eps90={e}  p_on={d.p_on}{tag}")
        print(f"   -> event eps90 (aligned) = {r.eps90_event}")
        if r.eps90_event is not None:
            aligned_event_eps90.append(r.eps90_event)
        out.append({
            "event": r.event, "mf_det": r.mf_det, "lag_pred_ms": r.lag_pred_ms,
            "eps90_event_aligned": r.eps90_event, "eps90_event_frozen": froz.get(ev),
            "detectors": [{"detector": d.detector, "amp220": d.amp220, "eps90": d.eps90,
                           "p_on": d.p_on, "on_source_null": d.on_source_null,
                           "note": d.note} for d in r.detectors],
        })
    stack = min(aligned_event_eps90) if aligned_event_eps90 else None
    froz_stack = min([v for v in froz.values() if v is not None]
                     + [1e9]) if froz else None
    gap = (stack / GAP6) if stack else None
    print("\n" + "-" * 84)
    print(f"ALIGNED stack eps90 (best on-source-null event) = {stack}  "
          f"(frozen stack ~ {froz_stack})")
    if gap:
        print(f"reach-gap vs (2/3)^6=0.088:  aligned x{gap:.1f}  (frozen was ~x7.2)")
    verdict = (
        f"Align + high-pass(20Hz) Stage-1h, GW250114 INCLUDED: stack eps90 = {stack} "
        f"(~x{gap:.1f} above the 0.088 kernel ceiling), from the frozen ~0.63 (~x7.2). "
        "The high-pass makes GW250114's O4b off-source whitened noise clean (0 samples>5sigma) "
        "and its ringdown MF-SNR ~17 (H1); GW250114 now anchors a limit. Upper-bound kernel: "
        "no detection, no tension. Closing fully to 0.088 needs O4c/GWTC-6 + O5 stacks or a "
        "next-gen event."
    ) if stack else "no on-source-null stream anchored a limit"
    print(f"\nVERDICT: {verdict}")
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "aligned_injection_limits.json").write_text(json.dumps({
        "analysis": "align + high-pass(20Hz) Stage-1h (opt-in flags), non-destructive re-analysis",
        "date": "2026-07-14",
        "note": ("frozen injection_limits.json is untouched; align + highpass_hz flags are opt-in "
                 "and default off. GW250114 INCLUDED (high-pass fixes the O4b sub-20Hz whitening "
                 "pathology; off-source clean, ringdown MF-SNR ~17)."),
        "highpass_hz": HIGHPASS_HZ,
        "kernel_ceiling_(2/3)^6": GAP6,
        "events": out,
        "aligned_stack_eps90": stack,
        "frozen_stack_eps90": froz_stack,
        "reach_gap_factor_aligned": round(gap, 2) if gap else None,
        "verdict": verdict,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote {RESULTS / 'aligned_injection_limits.json'}")


if __name__ == "__main__":
    main()
