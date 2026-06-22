"""``tfpt-gw analyze`` -- ringdown echo-ratio forecast on the LVK GWTC catalogue."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import constants
from .echo_forecast import forecast
from .echo_search import injection_suite

RESULTS = Path(__file__).resolve().parents[2] / "results"
STRAIN_DIR = Path(__file__).resolve().parents[2] / "data" / "strain"


def _run_realdata(events: list[str]) -> int:
    """Stage-1 echo search on REAL GWOSC strain (run scripts/fetch_strain.py first)."""
    from .real_echo_search import search_event      # local import: needs downloaded strain

    print("=" * 80)
    print("TFPT GW echo Stage-1 on REAL GWOSC strain (PSD-whitened MF + Kerr subtraction)")
    print("=" * 80)
    have = [e for e in events if (STRAIN_DIR / f"{e}_meta.json").exists()]
    missing = [e for e in events if e not in have]
    if missing:
        print(f"  (no strain for {missing}; run: python scripts/fetch_strain.py {' '.join(missing)})")
    if not have:
        print("  no strain downloaded -> nothing to do.")
        return 1

    out_events = []
    for ev in have:
        r = search_event(ev)
        print(f"\n  {ev}: M_f={r.mf_msun} Msun, f0={r.f0_hz} Hz, tau={r.tau_ms} ms "
              f"(echo kernel q=(2/3)^6={constants.RATIO:.4f})")
        print(f"    {'det':4s} {'rho_max':>8} {'lag(ms)':>8} {'q_hat':>9} {'p_value':>8} {'kernel?':>8}")
        for d in r.detectors:
            print(f"    {d.detector:4s} {d.rho_max:8.2f} {d.best_lag_ms:8.1f} {d.q_hat:9.4f} "
                  f"{d.p_value:8.4f} {str(d.kernel_consistent):>8}")
        print(f"    -> network rho={r.rho_net}, kernel-consistent detectors="
              f"{r.n_kernel_consistent}/{len(r.detectors)}  =>  {r.label}")
        if r.note:
            print(f"       note: {r.note}")
        out_events.append(vars(r) | {"detectors": [vars(d) for d in r.detectors]})

    any_candidate = any(e["label"] == "KERNEL_ECHO_CANDIDATE" for e in out_events)
    verdict = (
        "NO faint, kernel-ratio ((2/3)^6) ringdown echo found COINCIDENT in >=2 detectors for "
        + ", ".join(have) + ". Single-detector low-p excesses are residual ringdown power "
        "(q_hat ~ 1, not the faint kernel ratio) flagged by the free-ratio control, not echoes. "
        "Consistent with the TFPT UPPER bound (echoes may be absent/smaller). First pass: "
        "dominant-QNM subtraction + off-source background; full multi-mode subtraction + coherent "
        "stacking is the next step. No detection claim."
        if not any_candidate else
        "A faint kernel-ratio echo is coincident in >=2 detectors -- escalate to coherent "
        "stacking + time-slide coincident background + injections before any claim."
    )
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "echo_realdata.json").write_text(
        json.dumps({"stage": "strain_level_test (real GWOSC strain, first pass)",
                    "ratio_(2/3)^6": constants.RATIO, "events": out_events,
                    "verdict": verdict}, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'echo_realdata.json'}")
    return 0


def _run_dynamic(events: list[str]) -> int:
    """Stage-2 DYNAMIC walled-clock recovery matched filter on REAL GWOSC strain.

    Closes the experiments/README §1.1 gap: the static (2/3)^6 ratio searches are null;
    the kernel's dynamic signature is the walled two-mode clock (bend 2.7095 + floor + wall,
    QT.04). Here that template is fit to the post-merger residual power envelope on real
    strain, validated by injection into real off-source noise.
    """
    # local imports (same pattern as _run_realdata): these pull in h5py via strain_data,
    # which the base `analyze`/`audit` commands must not require.
    from .dynamic_recovery import (
        BEND,
        injection_suite_dynamic,
        search_event_dynamic,
    )
    from .strain_data import read_hdf5

    print("=" * 84)
    print("TFPT GW Stage-2: DYNAMIC walled-clock recovery matched filter on REAL GWOSC strain")
    print(f"  frozen bend rate(2)/rate(1) = ln3/ln(3/2) = {BEND:.4f} (one-parameter template)")
    print("=" * 84)

    have = [e for e in events if (STRAIN_DIR / f"{e}_meta.json").exists()]
    missing = [e for e in events if e not in have]
    if missing:
        print(f"  (no strain for {missing}; run: python scripts/fetch_strain.py {' '.join(missing)})")
    if not have:
        print("  no strain downloaded -> nothing to do.")
        return 1

    meta0 = json.loads((STRAIN_DIR / f"{have[0]}_meta.json").read_text(encoding="utf-8"))
    noise = read_hdf5(str(STRAIN_DIR / Path(next(iter(meta0["files"].values()))).name))
    suite = injection_suite_dynamic(noise.data, noise.dt)
    print("\n  injection validation (synthetic recovery -> REAL off-source noise):")
    print(f"    {'injection':14s} {'r2_template':>11} {'q_hat':>8}  {'label':22s} {'expected':22s} ok")
    for r in suite.results:
        print(f"    {r.case:14s} {r.r2_template:11.4f} {r.q_hat:8.4f}  {r.label:22s} "
              f"{r.expected:22s} {r.correct}")
    print(f"    -> {suite.n_correct}/{suite.n_total} correctly classified")

    out_events = []
    for ev in have:
        r = search_event_dynamic(ev, STRAIN_DIR)
        print(f"\n  {ev}: M_f={r.mf_msun} Msun, tau={r.tau_ms} ms")
        print(f"    {'det':4s} {'r2_template':>11} {'q_hat(bend)':>11} {'p_value':>8} {'kernel?':>8}")
        for d in r.detectors:
            print(f"    {d.detector:4s} {d.r2_template:11.4f} {d.q_hat:11.4f} "
                  f"{d.p_value:8.4f} {str(d.kernel_consistent):>8}")
        print(f"    -> kernel-consistent detectors = {r.n_kernel_consistent}/{len(r.detectors)}"
              f"  =>  {r.label}")
        if r.note:
            print(f"       note: {r.note}")
        out_events.append(vars(r) | {"detectors": [vars(d) for d in r.detectors]})

    any_candidate = any(e["label"] == "WALLED_CLOCK_RECOVERY_CANDIDATE" for e in out_events)
    verdict = (
        f"NO locked-ratio (bend {BEND:.4f}) walled-clock recovery found COINCIDENT in >=2 "
        "detectors for " + ", ".join(have) + ". Decaying post-merger envelopes are leftover "
        "single-mode ringdown power (q_hat far from the bend), rejected by the free-ratio "
        "control -- not a TFPT walled-clock recovery. Consistent with the kernel being an "
        "UPPER bound (a recovery imprint may be absent or below sensitivity). First pass: "
        "dominant-QNM subtraction + RMS envelope + off-source background; multi-mode "
        "subtraction + coherent stacking is the next step. No recovery claim made."
        if not any_candidate else
        "A locked-ratio walled-clock recovery is coincident in >=2 detectors -- escalate to "
        "coherent multi-mode subtraction + time-slide background + injections before any claim."
    )
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "dynamic_recovery.json").write_text(
        json.dumps({"stage": "strain_level_test (dynamic walled-clock, real GWOSC strain, first pass)",
                    "bend_ln3_over_ln1.5": BEND,
                    "injection_validation": {"n_correct": suite.n_correct,
                                             "n_total": suite.n_total,
                                             "results": [vars(r) for r in suite.results],
                                             "verdict": suite.verdict},
                    "events": out_events, "verdict": verdict}, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'dynamic_recovery.json'}")
    return 0


def _run_search() -> int:
    """Stage-1 echo matched-filter + injection-recovery (validated on synthetic strain)."""
    print("=" * 78)
    print("TFPT GW echo Stage-1: matched-filter + injection-recovery (synthetic strain)")
    print("=" * 78)
    suite = injection_suite()
    print(f"  frozen ratio (2/3)^6 = {constants.RATIO:.5f};  TFPT C=3/8 ECO template lag "
          f"~ {suite.template_lag_ms:.2f} ms (gravastar-compactness); lag free (scanned)\n")
    print(f"  {'injection':12s} {'echo SNR':>9} {'lag(ms)':>8} {'q_hat':>8}  "
          f"{'label':16s} {'expected':16s} ok")
    for r in suite.results:
        print(f"  {r.case:12s} {r.echo_snr:9.2f} {r.best_lag_ms:8.2f} {r.q_hat:8.4f}  "
              f"{r.label:16s} {r.expected:16s} {r.correct}")
    print(f"\n  -> {suite.n_correct}/{suite.n_total} correctly classified")
    print(f"\n-> {suite.verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {"stage": "strain_level_test (synthetic injection-recovery)",
           "ratio_(2/3)^6": constants.RATIO, "template_lag_ms": suite.template_lag_ms,
           "n_correct": suite.n_correct, "n_total": suite.n_total,
           "results": [vars(r) for r in suite.results], "verdict": suite.verdict}
    (RESULTS / "echo_search.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'echo_search.json'}")
    return 0 if suite.n_correct == suite.n_total else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT GW ringdown echo-ratio forecast + Stage-1 search")
    ap.add_argument("command", choices=["audit", "analyze", "search", "realdata", "dynamic"],
                    nargs="?", default="analyze")
    ap.add_argument("--events", nargs="*", default=["GW150914", "GW190521"],
                    help="events for the realdata/dynamic search (need scripts/fetch_strain.py first)")
    args = ap.parse_args(argv)

    if args.command == "search":
        return _run_search()
    if args.command == "realdata":
        return _run_realdata(args.events)
    if args.command == "dynamic":
        return _run_dynamic(args.events)

    print("=" * 72)
    print(f"TFPT ringdown echo-ratio CENSUS (stage={constants.STAGE}; ratio (2/3)^6, lag free)")
    print("=" * 72)
    for k, v in constants.summary().items():
        print(f"  {k} = {v:.5g}")
    if args.command == "audit":
        return 0

    r = forecast()
    print(f"\nGWTC-5.0: 390 canonical confident events (161 new in O4b); "
          f"local raw rows = {r.n_events} (GW170817 BNS reconciled in event_count_audit.md)")
    print(f"ringdown-capable BBH (Mf>=5 Msun): {r.n_bbh}")
    print("\nloudest ringdown events (echo SNR bounds at the frozen ratio):")
    print(f"  {'event':22s} {'SNR':>6} {'Mf':>6} {'echo_max':>9} {'echo_real':>10}")
    for e in r.top:
        print(f"  {e['name']:22s} {e['snr']:6.1f} {e['mfinal']:6.1f} "
              f"{e['echo_snr_max']:9.2f} {e['echo_snr_real']:10.2f}")
    print(f"\nstacked echo SNR upper bound (conservative f_rd=1):   {r.stacked_echo_snr_max:.1f}")
    print(f"stacked echo SNR upper bound (realistic f_rd=0.3):    {r.stacked_echo_snr_real:.1f}")
    print(f"detection threshold: {constants.DET_THRESHOLD:.0f}")
    print(f"\n-> {r.verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {"constants": constants.summary(), "stage": constants.STAGE,
           "n_canonical": 390, "n_raw_rows": r.n_events, "n_bbh": r.n_bbh, "top": r.top,
           "stacked_echo_snr_max": r.stacked_echo_snr_max,
           "stacked_echo_snr_real": r.stacked_echo_snr_real,
           "detectable_max": r.detectable_max, "detectable_real": r.detectable_real,
           "verdict": r.verdict}
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
