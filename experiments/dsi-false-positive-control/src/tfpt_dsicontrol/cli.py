"""``tfpt-dsicontrol`` — calibrate the frozen TFPT comb detector on NON-TFPT cascades.

The TFPT comb channels (recovery-comb-domains, pulsar-glitch-recovery, crust-cooling-comb) report
NULLS at the frozen kernel omega = 2 pi / ln((3/2)^6) = 2.583. The sceptic's question: "would the
detector fire on ANY discrete-scale-invariant or generic relaxation cascade?" This CONTROL bed
answers with real data: earthquake aftershocks (Omori decay; Sornette-documented log-periodicity)
and solar-flare sequences after large X-flares. FIREWALL: these systems have NO TFPT boundary/
horizon-recovery mapping by construction — that is the point. A quiet detector strengthens the
specificity of every existing null; a detector firing at 2.583 here would QUANTIFY the
universal-DSI coincidence rate the firewall names. Nothing here is [E]; no TFPT claim either way.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from . import efimov, fetch, mct, sequences
from .comb import EPS_PREDICTED, LAMBDA, MIN_COMB_PERIODS, OMEGA, P_THRESHOLD, validate_detector

RESULTS = Path(__file__).resolve().parents[2] / "results"


def _print_efimov(ef: dict) -> None:
    """Report CONTROL 1 (Efimov ladder) — numbers before any verdict language."""
    rt = ef["ladder_ratios"]
    rs = ef["resolvability"]
    print(f"      exactly-derived ladder: lambda=e^(pi/{ef['s0']})={ef['lambda_efimov']} "
          f"(omega={ef['omega_efimov']}) vs kernel omega={ef['omega_kernel']} "
          f"-> {100 * ef['frequency_separation_frac']:.1f}% apart (resolvable)")
    for r in rt["per_system"]:
        print(f"      {r['system']:6s} measured ratio {r['ratio']:5.1f} +- {r['ratio_err']:.2f}"
              f"  | z(lambda=22.69) = {r['z_efimov']:+.2f}  z(lambda=11.39) = {r['z_tfpt']:+.2f}")
    print(f"      combined (inv-var): {rt['combined_ratio']} +- {rt['combined_err']} | "
          f"Efimov {rt['combined_z_efimov']:+.2f} sigma, TFPT {rt['combined_z_tfpt']:+.2f} sigma"
          f" | chi2 scan best lambda={rt['best_fit_lambda']}: Efimov "
          f"{rt['sigma_equiv_efimov']} sigma-equiv, TFPT {rt['sigma_equiv_tfpt']} sigma-equiv")
    w_loc = rs["scan"]["best_localisable_omega"]
    print(f"      EF.02 frozen detector on the Efimov comb ({rs['periods_kernel']} kernel / "
          f"{rs['periods_efimov']} Efimov periods, eps={rs['eps']}, {rs['n_seeds']} seeds): "
          f"kernel fired {rs['kernel_fired']}/{rs['n_seeds']} "
          f"(median p={rs['p_kernel_median']}); detection AT omega_Efimov "
          f"{100 * rs['efimov_detect_rate']:.0f}%; scan localises omega={w_loc} "
          f"(lambda={rs['scan']['best_localisable_lambda']})")
    tail = ("kernel and Efimov DSI are cleanly distinct scales" if ef["passed"]
            else "see record for the failing criterion")
    print(f"      -> control {'PASSED' if ef['passed'] else 'FAILED'}: {tail}")


def _print_mct(mc: dict) -> None:
    """Report CONTROL 2 (MCT exponent spread) — a structural control, no comb run."""
    sp = mc["spread"]
    for r in mc["systems"]:
        src = "quoted" if r["lambda_quoted"] else "derived"
        print(f"      {r['system']:22s} gamma={r['gamma']:.4f}+-{r['gamma_err']:.2f} "
              f"(lambda_MCT={r['lambda_mct']:.3f} {src}, a={r['a']:.3f}, b={r['b']:.3f}) "
              f"| pull from bend 2.7095: {r['pull_from_tfpt_bend']:+.1f} sigma")
    ut, lt = sp["universality_test"], sp["locked_bend_test"]
    print(f"      spread over {sp['n_systems']} systems: mean={sp['gamma_mean']} "
          f"std={sp['gamma_std_sample']} range={sp['gamma_range']} "
          f"(width {sp['gamma_range_width']} = {sp['spread_over_error_range']}x the median "
          f"per-system error {sp['median_per_system_err']})")
    print(f"      one-universal-gamma test: chi2={ut['chi2']}/{ut['dof']} dof "
          f"(~{ut['sigma_equiv_wh']} sigma, WH approx) | LOCKED-BEND gamma==2.7095 test: "
          f"chi2={lt['chi2']}/{lt['dof']} dof (~{lt['sigma_equiv_wh']} sigma, WH approx)")
    nb = sp["nearest_system_to_bend"]
    print(f"      bend 2.7095 sits INSIDE the spread; nearest system {nb['system']} "
          f"(gamma={nb['gamma']}, distance {nb['distance']}) — proximity coincidence, "
          "gamma is system-dependent by construction")
    print(f"      -> control {'PASSED' if mc['passed'] else 'FAILED'}: boundary-less "
          "two-step relaxation shows NO frozen universal bend")


def _analyze(seed: int = 0, refresh: bool = False) -> int:
    print("=" * 92)
    print("FALSE-POSITIVE CONTROL: the frozen TFPT comb detector on KNOWN NON-TFPT cascades")
    print(f"  kernel: lambda=(3/2)^6={LAMBDA:.3f}  omega=2pi/ln(lambda)={OMEGA:.4f}  "
          f"eps_pred={EPS_PREDICTED:.3f}  gate>={MIN_COMB_PERIODS} comb periods  "
          f"threshold p<{P_THRESHOLD}")
    print("  FIREWALL: aftershocks + flare cascades have NO TFPT boundary-recovery mapping (by")
    print("  construction). This bed measures the kernel's coincidence rate on generic/DSI")
    print("  relaxations; it can never confirm TFPT, only calibrate the existing nulls.")
    print("=" * 92)

    # (0) the vendored detector must behave exactly like the original (injection validation)
    v = validate_detector()
    print(f"\n  [0] vendored-detector injection validation ({v.n_seeds} seeds): comb+range "
          f"{100*v.sufficient_comb_rate:.0f}% | smooth-decay FP {100*v.sufficient_null_rate:.0f}% "
          f"| short-range {100*v.short_comb_rate:.0f}% (range-blind) -> validated={v.passed}")
    if not v.passed:
        print("  ABORT: vendored detector failed validation."); return 1

    # (1) real control data
    if refresh or not any(sequences.SEQ.glob("*.csv")):
        print("\n  [1] fetching control sequences (USGS ComCat + NGDC GOES XRS)...")
        fetch.fetch_all(refresh=refresh)
    seqs = sequences.load_sequences()
    if not seqs:
        print("  NO data. Run: python scripts/fetch_aftershocks.py && python scripts/fetch_flares.py")
        return 1
    print(f"\n  [1] {len(seqs)} control sequences "
          f"({sum(s.kind == 'aftershock' for s in seqs)} aftershock, "
          f"{sum(s.kind == 'flare' for s in seqs)} flare):")

    # (2) per-sequence: frozen detector + rate-preserving shuffle + omega scan
    records = []
    for s in seqs:
        r = sequences.analyze_sequence(s, seed=seed)
        records.append(r)
        gate = "" if r["range_sufficient"] else "  <range-blind, excluded from FP denominator>"
        fire = "  <-- FIRED AT KERNEL" if r["fired_at_kernel_frozen"] else ""
        w_loc = r["scan"]["best_localisable_omega"]
        lam_loc = r["scan"]["best_localisable_lambda"]
        loc = (f"best loc. omega={w_loc:.2f} (lambda={lam_loc:.2f}, "
               f"p_shuf={r['p_best_localisable_shuffle_uncorrected']:.3f} uncorr)"
               if w_loc is not None else "no localisable omega in scan band")
        print(f"      {r['name']:16s} [{r['kind']:10s}] {r['n_events']:5d} events "
              f"{r['comb_periods']:.2f} periods | p_kern(periodogram)={r['p_kernel_periodogram']:.3f} "
              f"p_kern(shuffle)={r['p_kernel_shuffle']:.3f} | kernel rank "
              f"{r['scan']['kernel_rank']}/{r['scan']['n_scanned']} | {loc} | "
              f"eps_fit={r['eps_fit_at_kernel']:.3f}{fire}{gate}")

    # (3) the headline: aggregate kernel false-positive rate
    agg = sequences.aggregate(records)
    ff, fs = agg["kernel_fp_frozen"], agg["kernel_fp_strict"]
    print(f"\n  [2] AGGREGATE kernel false-positive rate over {agg['n_gated']}/{agg['n_sequences']}"
          f" gated sequences:")
    print(f"      frozen criterion (periodogram p<{P_THRESHOLD} + range gate): "
          f"{ff['fired']}/{agg['n_gated']} = {ff['rate']}  (Wilson95 {ff['wilson95']})")
    print(f"      strict (frozen AND rate-preserving shuffle p<{P_THRESHOLD}): "
          f"{fs['fired']}/{agg['n_gated']} = {fs['rate']}  (Wilson95 {fs['wilson95']})")
    print(f"      nominal rate at the p<{P_THRESHOLD} threshold under a calibrated null: "
          f"~{P_THRESHOLD}")

    # (4) where do the controls' OWN DSI scales sit? (context for outcome (ii))
    best = [r["scan"]["best_localisable_omega"] for r in records
            if r["range_sufficient"] and r["scan"]["best_localisable_omega"] is not None]
    print(f"\n  [3] controls' own best LOCALISABLE free omegas (gated sequences): "
          f"{[round(w, 2) for w in sorted(best)]} (kernel = {OMEGA:.3f}); Sornette-type "
          f"seismic DSI is typically lambda~2-3.5 (omega~5-9), i.e. away from the kernel.")

    # (5) CONTROL 1 — the Efimov ladder (exactly-derived non-TFPT DSI, gated)
    print("\n  [4] CONTROL 1 — Efimov ladder (nature's exactly-derived non-TFPT DSI):")
    ef = efimov.run_efimov_control(seed=seed)
    _print_efimov(ef)

    # (6) CONTROL 2 — glass/MCT exponent spread (structural, no comb run)
    print("\n  [5] CONTROL 2 — glass/MCT exponent spread vs the frozen bend 2.7095 "
          "(structural control, no comb run):")
    mc = mct.run_mct_control()
    _print_mct(mc)

    # (7) combined aggregate over ALL gated DSI controls (cascades + Efimov ladder)
    comb_agg = sequences.combined_dsi_aggregate(agg, efimov_kernel_fired=ef["kernel_fired"])
    print(f"\n  [6] COMBINED kernel false-positive rate over "
          f"{comb_agg['n_gated_dsi_controls']} gated DSI controls "
          f"({comb_agg['members']}): {comb_agg['kernel_fired']}/"
          f"{comb_agg['n_gated_dsi_controls']} = {comb_agg['rate']} "
          f"(Wilson95 {comb_agg['wilson95']})")

    verdict = _verdict(records, agg, ef, mc, comb_agg)
    print(f"\n==> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {
        "kernel": {"lambda": LAMBDA, "omega": OMEGA, "eps_predicted": EPS_PREDICTED,
                   "min_comb_periods": MIN_COMB_PERIODS, "p_threshold": P_THRESHOLD,
                   "one_period_ln_t": float(np.log(LAMBDA))},
        "detector_validation": asdict(v),
        "scan_band_omega": [sequences.OMEGA_SCAN_LO, sequences.OMEGA_SCAN_HI],
        "n_shuffles": sequences.N_SHUFFLE,
        "sequences": records,
        "aggregate": agg,
        "efimov_control": ef,
        "mct_control": mc,
        "dsi_controls_aggregate": comb_agg,
        "verdict": verdict,
    }
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


def _verdict(records: list[dict], agg: dict, ef: dict, mc: dict, comb_agg: dict) -> str:
    gated = [r for r in records if r["range_sufficient"]]
    ff, fs = agg["kernel_fp_frozen"], agg["kernel_fp_strict"]
    n_asc = sum(r["kind"] == "aftershock" for r in records)
    n_fl = len(records) - n_asc
    fired = [r["name"] for r in gated if r["fired_at_kernel_frozen"]]
    if not fired:
        outcome = (f"the detector is QUIET at the kernel on every gated control "
                   f"(FP {ff['fired']}/{len(gated)}, Wilson95 upper {ff['wilson95'][1]}), "
                   "consistent with the nominal ~5% threshold rate -> the existing TFPT-channel "
                   "nulls are SPECIFIC: the kernel frequency does not fire on generic "
                   "Omori/DSI-type cascades")
    elif fs["fired"] == 0:
        outcome = (f"the frozen criterion fired on {fired} but NO sequence survives the "
                   "rate-preserving shuffle double-check (strict FP 0) -> periodogram-rank "
                   "fluctuations, not a kernel-frequency comb; kernel stays specific")
    else:
        outcome = (f"the kernel frequency FIRED on {fired} (strict FP {fs['fired']}/{len(gated)}"
                   f" = {fs['rate']}) -> IMPORTANT WARNING: this quantifies the universal-DSI "
                   "coincidence rate the firewall names; every TFPT-channel comb p-value must be "
                   "read against THIS base rate, not the nominal 5%")
    rt, rs = ef["ladder_ratios"], ef["resolvability"]
    ef_txt = (f"CONTROL 1 (Efimov ladder, exactly-derived non-TFPT DSI lambda=e^(pi/s0)=22.69): "
              f"measured cold-atom ratios (Cs/7Li/39K) combine to "
              f"{rt['combined_ratio']}+-{rt['combined_err']} — Efimov-consistent "
              f"({rt['combined_z_efimov']} sigma) and {rt['sigma_equiv_tfpt']} sigma from the "
              f"TFPT lambda=11.39 (Cs alone {rt['per_system'][0]['z_tfpt']} sigma); the frozen "
              f"detector on the gated Efimov comb fired at the kernel "
              f"{rs['kernel_fired']}/{rs['n_seeds']} seeds while detecting omega_Efimov=2.01 "
              f"at {100 * rs['efimov_detect_rate']:.0f}% -> "
              f"{'PASSED' if ef['passed'] else 'FAILED'}")
    sp = mc["spread"]
    lt = sp["locked_bend_test"]
    mc_txt = (f"CONTROL 2 (glass/MCT exponent spread, structural): gamma across "
              f"{sp['n_systems']} systems spans {sp['gamma_range']} "
              f"(std {sp['gamma_std_sample']}, {sp['spread_over_error_range']}x the median "
              f"per-system error) — the TFPT bend 2.7095 sits inside the spread but a LOCKED "
              f"universal bend is rejected at chi2={lt['chi2']}/{lt['dof']} dof "
              f"(~{lt['sigma_equiv_wh']} sigma): boundary-less two-step relaxation shows no "
              f"frozen bend -> {'PASSED' if mc['passed'] else 'FAILED'}")
    return (f"{len(records)} real control sequences ({n_asc} aftershock cascades from USGS ComCat"
            f" incl. Landers/Tohoku/Ridgecrest; {n_fl} solar-flare sequences after large X-flares,"
            f" NGDC GOES XRS), {len(gated)} clear the >= {MIN_COMB_PERIODS}-period gate. "
            f"Kernel omega=2.583 false-positive rate: frozen {ff['fired']}/{len(gated)}"
            f" (Wilson95 {ff['wilson95']}), strict {fs['fired']}/{len(gated)}. {outcome}. "
            f"{ef_txt}. {mc_txt}. COMBINED over all {comb_agg['n_gated_dsi_controls']} gated DSI "
            f"controls ({comb_agg['members']}): kernel fired "
            f"{comb_agg['kernel_fired']}/{comb_agg['n_gated_dsi_controls']} "
            f"(Wilson95 {comb_agg['wilson95']}). "
            "FIREWALL: controls have no TFPT mapping by construction; this calibrates detector "
            "specificity only and is NOT evidence for TFPT. No claim; nothing [E].")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="False-positive control: frozen TFPT comb detector on non-TFPT cascades")
    ap.add_argument("command", nargs="?", default="analyze",
                    choices=["analyze", "fetch", "fetch-quakes", "fetch-flares",
                             "validate", "audit", "efimov", "mct"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--refresh", action="store_true", help="re-download raw data")
    args = ap.parse_args(argv)
    if args.command == "audit":
        print(f"kernel omega=2pi/ln((3/2)^6)={OMEGA:.4f}; eps_pred={EPS_PREDICTED:.4f}; "
              f"gate>={MIN_COMB_PERIODS} periods; p<{P_THRESHOLD}; scan band "
              f"[{sequences.OMEGA_SCAN_LO},{sequences.OMEGA_SCAN_HI}]; controls: "
              f"Efimov lambda={efimov.LAMBDA_EFIMOV:.4f} (omega={efimov.OMEGA_EFIMOV:.4f}), "
              f"MCT bend reference={mct.BEND_TFPT:.4f}")
        return 0
    if args.command == "validate":
        v = validate_detector()
        print(asdict(v))
        return 0 if v.passed else 1
    if args.command == "efimov":
        ef = efimov.run_efimov_control(seed=args.seed)
        _print_efimov(ef)
        return 0 if ef["passed"] else 1
    if args.command == "mct":
        mc = mct.run_mct_control()
        _print_mct(mc)
        return 0 if mc["passed"] else 1
    if args.command in ("fetch", "fetch-quakes", "fetch-flares"):
        if args.command in ("fetch", "fetch-quakes"):
            for ms in fetch.MAINSHOCKS:
                print(f"  {ms.name}: -> {fetch.fetch_quake(ms, refresh=args.refresh)}")
        if args.command in ("fetch", "fetch-flares"):
            for tr in fetch.FLARE_TRIGGERS:
                print(f"  {tr.name}: -> {fetch.fetch_flares(tr, refresh=args.refresh)}")
        return 0
    return _analyze(seed=args.seed, refresh=args.refresh)


if __name__ == "__main__":
    raise SystemExit(main())
