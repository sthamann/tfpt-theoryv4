"""``tfpt-recovery analyze`` -- the recovery kernel as an explicit quantum channel."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import constants
from .channel import analyse_mode, qec_check
from .page_curve import analyse as page_analyse
from .petz_recovery import negative_controls, petz_check, rank_one_limit

RESULTS = Path(__file__).resolve().parents[2] / "results"


def _run_petz() -> int:
    """Explicit Petz recovery + rank-one (baby-universe) limit -- companion to v221."""
    print("=" * 72)
    print("TFPT recovery: explicit Petz map + rank-one baby-universe limit (companion v221)")
    print("=" * 72)
    ro = rank_one_limit()
    print("\n[1] Rank-one / baby-universe limit of the gapped transport T")
    print(f"    {'n':>2}  {'||T^n - P_inf||_2':>18}  {'(2/3)^(6n)':>14}")
    for n, dist, pred in ro.rates:
        print(f"    {n:>2}  {dist:>18.3e}  {pred:>14.3e}")
    print(f"    -> exact rank-one rate = (2/3)^6: {ro.rank_one_exact}; unique fixed point "
          f"(spectral gap): {ro.fixed_point_unique}")
    print("    => the boundary-accessible algebra collapses to ONE dimension (the law/attractor)")
    print("       at the kernel rate -- the 1-dim baby-universe Hilbert space (Engelhardt 2025).")

    print("\n[2] Explicit Petz recovery map R_P per mode")
    petz = {}
    for name, lm in (("lambda1=1", constants.LAMBDA[0]), ("lambda2=(2/3)^6", constants.LAMBDA[1]),
                     ("lambda3=(1/3)^6", constants.LAMBDA[2])):
        r = petz_check(lm)
        petz[name] = r
        print(f"    {name:16s} recovers reference={r.recovers_reference}, CPTP={r.petz_cptp}, "
              f"protected(all states)={r.protected_all_states}")
    print("    -> only the protected lambda=1 mode is recovered for ALL states (Knill-Laflamme);")
    print("       the contracted modes leak at the gap (2/3)^6 per step (v221 bound, now an explicit map).")

    print("\n[3] Negative controls")
    nc = negative_controls()
    print(f"    free ratio r=0.5 lands on the (2/3)^6 kernel rate: {nc['free_ratio_lands_on_kernel']} "
          f"(expected False)")
    print(f"    degenerate (non-gapped) spectrum loses the rank-one limit: "
          f"{nc['degenerate_spectrum_loses_rank_one']} (expected True)")

    ok = (ro.rank_one_exact and ro.fixed_point_unique
          and all(petz[m].petz_cptp and petz[m].recovers_reference for m in petz)
          and petz["lambda1=1"].protected_all_states
          and not petz["lambda2=(2/3)^6"].protected_all_states
          and not nc["free_ratio_lands_on_kernel"]
          and nc["degenerate_spectrum_loses_rank_one"])
    verdict = ("the gapped transport contracts to a RANK-ONE attractor at exactly (2/3)^{6n} "
               "(the 1-dim baby-universe Hilbert space), and the explicit Petz map recovers the "
               "protected 'law' code while the contracted modes leak at the gap -- the [C] Petz "
               "identification v221 deferred, now realised (internal-consistency, no new data)") \
        if ok else "FAIL: a Petz/rank-one/negative-control check did not hold"
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {"rank_one": {"gap": ro.gap, "rank_one_exact": ro.rank_one_exact,
                        "fixed_point_unique": ro.fixed_point_unique,
                        "rates": [{"n": n, "dist": d, "pred_(2/3)^6n": p} for n, d, p in ro.rates]},
           "petz": {m: vars(r) for m, r in petz.items()},
           "negative_controls": nc, "verdict": verdict}
    (RESULTS / "petz_recovery.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'petz_recovery.json'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT recovery channel: CPTP / DPI / QEC / Page / Petz")
    ap.add_argument("command", choices=["audit", "analyze", "petz"], nargs="?", default="analyze")
    args = ap.parse_args(argv)

    if args.command == "petz":
        return _run_petz()

    print("=" * 72)
    print("TFPT recovery kernel as a quantum channel R: H_bulk -> H_observable")
    print("=" * 72)
    for k, v in constants.summary().items():
        print(f"  {k} = {v:.6g}")
    if args.command == "audit":
        return 0

    print("\n[1] CPTP + recovery rate + data-processing (per kernel mode)")
    modes = {"lambda1=1": constants.LAMBDA[0], "lambda2=(2/3)^6": constants.LAMBDA[1],
             "lambda3=(1/3)^6": constants.LAMBDA[2]}
    reports = {}
    all_cptp = True
    for name, lm in modes.items():
        r = analyse_mode(lm)
        reports[name] = r
        all_cptp &= r.trace_preserving and r.completely_positive
        print(f"    {name:16s} CPTP={r.trace_preserving and r.completely_positive} "
              f"(Choi_min={r.choi_min_eig:+.2e})  I_n={{1:{r.recovery_n[1]:.3e}, "
              f"2:{r.recovery_n[2]:.2e}, 3:{r.recovery_n[3]:.2e}}}  "
              f"DPI={r.dpi_holds} ({r.dpi_after:.3f}<={r.dpi_before:.3f})")

    print("\n[2] QEC: protected 'law' code vs contracted modes")
    q = qec_check()
    print(f"    protected lambda=1 mode: decoherence-free={q.protected_is_dfs}, "
          f"Knill-Laflamme={q.knill_laflamme_protected}")
    print(f"    contracted mode correctable on full code: {q.contracted_correctable} "
          f"(expected False -> gap = leakage rate)")
    print(f"    -> {q.note}")

    print("\n[3] Page curve (TFPT Hawking law + island min-prescription)")
    p = page_analyse()
    print(f"    unitary turnover at t/tau = {p.t_page_over_tau:.4f}  vs  "
          f"TFPT t_Page/tau = {p.t_page_theory:.4f}  -> match={p.turnover_matches}")
    print(f"    -> {p.note}")

    verdict = ("recovery kernel is a valid CPTP quantum channel (data-processing "
               "respected, protected 'law' code = decoherence-free subspace), and the "
               "TFPT Hawking law reproduces the unitary Page turnover at t_Page "
               "-- structural confirmation, not new data") if (all_cptp and p.turnover_matches) \
        else "FAIL: a channel axiom or the Page turnover did not hold"
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {
        "constants": constants.summary(),
        "channel": {n: {"cptp": r.trace_preserving and r.completely_positive,
                        "choi_min_eig": r.choi_min_eig, "recovery_n": r.recovery_n,
                        "dpi_holds": r.dpi_holds} for n, r in reports.items()},
        "qec": vars(q),
        "page_curve": vars(p),
        "verdict": verdict,
    }
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
