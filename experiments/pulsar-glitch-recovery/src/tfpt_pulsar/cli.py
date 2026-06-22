"""``tfpt-pulsar`` -- cross-domain TFPT recovery-kernel search in pulsar glitches.

Commands:
    audit     print the frozen TFPT constants / candidate ratios
    validate  injection-recovery self-check of the discreteness machinery
    analyze   run PG.01 (size discreteness) + PG.02/03 (kernel ladders) on the
              real Jodrell Bank catalogue; write results/results.json (+ plot)
    dynamic   PG.05: the dynamic recovery-comb test (omega=2.58) on the real Crab
              nu(t) ephemeris; injection-validated; write results/pg05_*.json (+ plot)
    nicer     PG.06 (heavy): scaffold the dense J0537-6910 stacked recovery-comb test
              (HEASARC L2 events + PINT -> nu(t) -> stack); downstream injection-validated
    vela      PG.06b: REAL NICER Vela-pulsar data -- download one obs (--download) + PINT-fold to
              detect the pulsation; proves the reduction pipeline on real data (no HEASoft)
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from . import constants
from .catalog import glitch_sizes, load_catalog, load_recovery
from .discreteness import discreteness_report, periodogram_curve
from .dsi import log_frequency
from .ratios import prolific_glitchers, size_ratio_ladder, waiting_ratio_ladder
from .recovery import bend_wall_test, q_cluster_test, tau_component_ladder
from .validation import injection_recovery

RESULTS = Path(__file__).resolve().parents[2] / "results"


def _audit() -> int:
    print("=" * 74)
    print("TFPT frozen constants / candidate ratios (pulsar-glitch leg)")
    print("=" * 74)
    for k, v in constants.summary().items():
        print(f"  {k:24s} = {v:.6g}")
    print("\n  preregistered size ratios (PG.01/02):")
    for t in constants.candidate_size_ratios():
        print(f"    {t.name:16s} = {t.value:8.4f}  [{t.kind}]  {t.provenance}")
    print("\n  recovery-Q targets (PG.04, data-limited):")
    for k, v in constants.candidate_Q_clusters().items():
        print(f"    {k:8s} = {v:.5f}")
    return 0


def _validate() -> int:
    print("=" * 74)
    print("Injection-recovery self-check (discreteness machinery)")
    print("=" * 74)
    r = injection_recovery()
    print(f"  smooth bimodal null : p={r.smooth_p:.3f}  rejected(no false comb)={r.smooth_rejected}")
    print(f"  injected (3/2)^3 comb: p={r.comb_p:.3f}  detected={r.comb_detected}  "
          f"ratio={r.comb_ratio_recovered:.3f} (ok={r.comb_ratio_ok})")
    print(f"\n-> machinery {'VALID' if r.passed else 'FAILED'}: detects a real comb, "
          "rejects a smooth bimodal distribution")
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "validation.json").write_text(json.dumps(vars(r), indent=2), encoding="utf-8")
    return 0 if r.passed else 1


def _plot(sizes, seed: int) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:  # noqa: BLE001
        return
    ratios, z, z95 = periodogram_curve(sizes, seed=seed)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(ratios, z, lw=1.0, color="#1f77b4", label="Rayleigh power")
    ax.axhline(z95, ls="--", color="0.4", label="95% smooth-null (KDE)")
    for t in constants.candidate_size_ratios():
        if ratios.min() <= t.value <= ratios.max():
            ax.axvline(t.value, ls=":", lw=0.9,
                       color="#d62728" if t.kind == "kernel" else "#2ca02c")
            ax.text(t.value, ax.get_ylim()[1] * 0.92, t.name, rotation=90,
                    va="top", ha="right", fontsize=7)
    ax.set_xlabel("glitch-size spacing ratio r  (Delta nu/nu families)")
    ax.set_ylabel("Rayleigh power z")
    ax.set_title("PG.01 log-periodicity of pulsar glitch sizes (Jodrell Bank)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(RESULTS / "pg01_periodogram.png", dpi=130)
    plt.close(fig)


def _dynamic(seed: int) -> int:
    """PG.05 -- the DYNAMIC recovery-comb test on the real Crab nu(t) waveform.

    The static ratio searches (PG.01-04) are null; the discriminating dynamic signature is the
    log-periodic comb at omega=2pi/ln((3/2)^6)=2.58 across a recovery spanning a wide ln(time)
    range. The Crab monthly ephemeris is the one public dataset with that reach.
    """
    from .nu_recovery import OMEGA, make_plot, pg05_recovery_comb

    r = pg05_recovery_comb(seed=seed)
    print("=" * 78)
    print("PG.05 -- dynamic recovery comb on the real Crab nu(t) (Jodrell Bank ephemeris)")
    print(f"  kernel cascade log-frequency omega = 2pi/ln((3/2)^6) = {OMEGA:.3f}")
    print("=" * 78)
    print(f"  data: {r.n_points} monthly points over {r.span_years:.0f} yr; "
          f"{r.n_glitches} glitches detected")
    inj = r.injection
    print("\n  detector injection-validation (on the REAL monthly sampling):")
    print(f"    injected geometric cascade comb -> detected={inj.comb_detected} (p={inj.comb_p:.3f})")
    print(f"    smooth power-law recovery       -> rejected={inj.smooth_rejected} (p={inj.smooth_p:.3f})")
    print(f"    -> detector valid: {inj.passed}")
    print(f"\n  inter-glitch recovery segments ({len(r.segments)} clean, comb at omega):")
    print(f"    {'glitch MJD':>11} {'n':>4} {'span(d)':>8} {'gain':>7} {'p':>7} {'comb?':>7}")
    for s in r.segments:
        print(f"    {s.glitch_mjd:11.0f} {s.n_points:4d} {s.span_days:8.0f} {s.amplitude:7.3f} "
              f"{s.p_value:7.3f} {str(s.detected):>7}")
    print(f"    -> comb detected in {r.n_detected}/{len(r.segments)} segments")
    print(f"\n==> VERDICT: {r.verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {
        "kernel_omega": r.omega, "n_points": r.n_points, "span_years": r.span_years,
        "n_glitches": r.n_glitches,
        "injection": vars(r.injection), "segments": [vars(s) for s in r.segments],
        "n_detected": r.n_detected, "verdict": r.verdict,
    }
    (RESULTS / "pg05_recovery_comb.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'pg05_recovery_comb.json'}")
    plot_path = make_plot(RESULTS / "pg05_recovery_comb.png", seed=seed)
    print(f"Wrote {plot_path}")
    return 0


def _nicer(seed: int) -> int:
    """PG.06 (heavy/optional) -- the dense, stacked recovery-comb test on PSR J0537-6910.

    Upstream (NICER L2 events + PINT folding -> nu(t)) is gated on ~GB downloads; downstream
    (nu(t) -> superposed-epoch stack -> kernel-omega comb) is injection-validated now on a
    synthetic J0537-like series and runs unchanged on real data when present.
    """
    from .nicer_j0537 import OMEGA, make_plot, run

    r = run(seed=seed)
    print("=" * 80)
    print("PG.06 (heavy) -- dense stacked recovery comb on PSR J0537-6910 (the 'Big Glitcher')")
    print(f"  kernel cascade log-frequency omega = {OMEGA:.3f}")
    print("=" * 80)
    e = r.env
    print(f"  environment: PINT={e.pint} astropy={e.astropy} scipy={e.scipy} "
          f"HEASoft={e.heasoft}")
    print(f"    {e.note}")
    print("\n  fetch/reduce plan (data/nicer_j0537/):")
    for line in r.plan:
        print(f"    {line}")
    if r.real_available and r.real is not None:
        print(f"\n  REAL nu(t): stacked comb gain={r.real.gain:.3f} p={r.real.p_value:.3f} "
              f"({r.real.n_segments} segments, {r.real.tau_points} tau-bins) -> "
              f"detected={r.real.detected}")
    elif r.validation is not None:
        v = r.validation
        print(f"\n  detector validation (comb detection rate over {v.n_seeds} noisy seeds; "
              f"eps={v.eps}, noise={v.noise}):")
        print(f"    SUFFICIENT range (~{v.long_periods:.1f} comb periods, Vela-like long interval):")
        print(f"      comb detected {100*v.long_comb_rate:.0f}%  |  false-positive (null) "
              f"{100*v.long_null_rate:.0f}%  -> validated={v.passed}")
        print(f"    J0537 range (~{v.j0537_periods:.1f} comb periods, ~100 d interval):")
        print(f"      same comb detected {100*v.j0537_comb_rate:.0f}%  -> range-blind "
              "(stacking buys amplitude, NOT ln(tau) range)")
    print(f"\n==> {r.verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {
        "kernel_omega": OMEGA,
        "environment": vars(r.env),
        "fetch_plan": r.plan,
        "real_available": r.real_available,
        "real": vars(r.real) if r.real else None,
        "synthetic_validation": vars(r.validation) if r.validation else None,
        "verdict": r.verdict,
    }
    (RESULTS / "pg06_nicer_j0537.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'pg06_nicer_j0537.json'}")
    if not r.real_available:
        print(f"Wrote {make_plot(RESULTS / 'pg06_range_finding.png')}")
    return 0


def _vela(seed: int, download: bool) -> int:
    """PG.06b -- REAL NICER Vela-pulsar data: prove the reduction pipeline on real photons.

    Vela is the long-interval target PG.06 pointed at. This downloads one real NICER observation
    (if asked / absent) and folds it with PINT to detect the Vela pulsation -- proving the
    download->barycentre->fold pipeline on REAL data (no HEASoft). A comb-quality nu(t) still needs
    a full phase-connected timing solution (documented, heavy).
    """
    from .vela import OBS_CSV, download_one, run

    if download and OBS_CSV.exists():
        with OBS_CSV.open(encoding="utf-8") as fh:
            first = next(csv.DictReader(fh), None)
        if first:
            print(f"  downloading one real NICER Vela obs {first['obsid']} (~10 MB)...")
            download_one(first["obsid"], float(first["mjd_start"]))

    r = run(seed=seed)
    print("=" * 80)
    print("PG.06b -- REAL NICER Vela-pulsar (PSR B0833-45) reduction pipeline")
    print("=" * 80)
    print(f"  archive: {r.n_observations} observations, {r.span_years:.1f} yr, "
          f"~{r.total_exposure_ks:.0f} ks (full L2 download ~{r.full_reduction_gb} GB)"
          if r.n_observations else "  (run scripts/fetch_nicer_vela.py first for the obs list)")
    if r.detection is not None:
        d = r.detection
        print(f"\n  REAL-DATA fold (obsid {d.obsid}):")
        print(f"    {d.n_photons} photons barycentred (PINT, no HEASoft); fold on {d.n_used} subsample")
        print(f"    Vela pulsation: F0={d.best_f0_hz} Hz (period {1000.0/d.best_f0_hz:.2f} ms), "
              f"H={d.h_stat} -> detected={d.detected}")
    else:
        print("\n  no observation downloaded yet -> rerun with --download")
    print(f"\n  full comb-quality nu(t): {r.full_reduction_note}")
    print(f"\n==> {r.verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {"n_observations": r.n_observations, "span_years": r.span_years,
           "total_exposure_ks": r.total_exposure_ks, "full_reduction_gb": r.full_reduction_gb,
           "detection": vars(r.detection) if r.detection else None,
           "full_reduction_note": r.full_reduction_note, "verdict": r.verdict}
    (RESULTS / "pg06b_vela.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'pg06b_vela.json'}")
    return 0


def _analyze(seed: int) -> int:
    records = load_catalog()
    sizes = glitch_sizes(records)
    n_pulsars = len({r.jname for r in records})

    print("=" * 74)
    print("PG -- TFPT recovery-kernel search in pulsar glitches (Jodrell Bank)")
    print("=" * 74)
    print(f"  catalogue: {len(records)} glitches, {n_pulsars} pulsars, "
          f"{len(sizes)} with dF/F")
    print("  most-glitching pulsars: " +
          ", ".join(f"{k}({n})" for k, n in prolific_glitchers(records, top=6)))

    rep = discreteness_report(sizes, seed=seed)
    print("\n[PG.01] glitch-size discreteness / log-periodicity")
    print(f"    log-normal KS p = {rep.lognormal.ks_pvalue:.3f} "
          f"(low => not a single log-normal); GMM best_k={rep.gmm.best_k} "
          f"(dBIC={rep.gmm.delta_bic:.1f})")
    lp = rep.logperiodic
    print(f"    best ratio = {lp.best_ratio:.3f}  z={lp.z_max:.1f}  p(cons)={lp.p_value:.3f}")
    print(f"      nulls: lognormal {lp.p_lognormal:.3f} | kde {lp.p_kde:.3f} | "
          f"GMM-population {lp.p_gmm:.3f} (decisive)")
    print(f"    nearest preregistered ratio: {lp.nearest.name} "
          f"({100*lp.nearest_rel_err:.0f}% away)")
    n_cand = sum(1 for t in rep.targeted if t.kind != "audit")
    print(f"    targeted preregistered ratios (p_gmm population-controlled; "
          f"LEE = Bonferroni x{n_cand}):")
    for t in rep.targeted:
        if min(1.0, t.p_gmm * n_cand) < 0.05:
            flag = " * survives LEE"
        elif t.p_gmm < 0.05:
            flag = "  (raw-only, fails LEE)"
        elif min(t.p_lognormal, t.p_kde) < 0.05:
            flag = "  (bimodality only)"
        else:
            flag = ""
        print(f"      {t.name:16s} [{t.kind:8s}] z={t.z:6.1f}  "
              f"p_smooth={min(t.p_lognormal, t.p_kde):.3f}  p_gmm={t.p_gmm:.3f}{flag}")
    print(f"    -> {rep.verdict}")

    pg02 = size_ratio_ladder(records, seed=seed)
    pg03 = waiting_ratio_ladder(records, seed=seed)
    print(f"\n[PG.02] size-ratio kernel ladder ({pg02.n_pulsars} pulsars, "
          f"{pg02.n_ratios} steps)")
    print(f"    -> {pg02.verdict}")
    print(f"\n[PG.03] waiting-time kernel ladder ({pg03.n_pulsars} pulsars, "
          f"{pg03.n_ratios} steps)")
    print(f"    -> {pg03.verdict}")

    # PG.04 -- the recovery channel (Yu+2013 Q / tau_d), incl. the multi-timescale
    # DSI reading of the kernel
    recs = load_recovery()
    pg04q = q_cluster_test(recs, seed=seed)
    pg04t = tau_component_ladder(recs, seed=seed)
    pg04b = bend_wall_test(recs, seed=seed)
    print(f"\n[PG.04] post-glitch recovery (Yu+2013; {pg04q.n} Q values)")
    print(f"    a) Q clustering at phi0-multiples {{{', '.join(f'{v:.3f}' for v in pg04q.targets.values())}}}")
    print(f"       -> {pg04q.verdict}")
    print(f"    b) tau_d multi-component (3/2)^k ladder ({pg04t.n_glitches} glitches, "
          f"{pg04t.n_ratios} ratios; DSI omega(3/2)={log_frequency(1.5):.2f})")
    print(f"       -> {pg04t.verdict}")
    print("    c) EXACT clock (v124): 2-mode bend ratio 2.7095 + wall (<=2 decay modes)")
    print(f"       component counts {pg04b.comp_counts}; -> {pg04b.verdict}")

    # a kernel claim must (a) be a preregistered ratio surviving the
    # population-controlled null, or (b) appear in a per-pulsar ladder (which is
    # immune to the global bimodality by construction). Single targeted ratios
    # face a look-elsewhere (Bonferroni) correction over the candidate family.
    n_cand = sum(1 for t in rep.targeted if t.kind != "audit")
    pg01_kernel = lp.p_gmm < 0.05 and lp.nearest_rel_err < 0.05
    targeted_kernel = any(t.kind != "audit" and min(1.0, t.p_gmm * n_cand) < 0.05
                          for t in rep.targeted)
    ladder_kernel = pg02.p_value < 0.05 or pg03.p_value < 0.05
    recovery_kernel = pg04q.p_value < 0.05 or pg04t.p_value < 0.05 or pg04b.p_value < 0.05
    n_glitches_wall = sum(pg04b.comp_counts.values())
    n_wall_ok = n_glitches_wall - pg04b.n_wall_exceed
    if pg01_kernel or targeted_kernel or ladder_kernel or recovery_kernel:
        verdict = ("cross-domain kernel signature found in pulsar glitches "
                   "(survives the population-controlled null / shows in a ladder) "
                   "-- inspect channel verdicts")
    else:
        verdict = ("no TFPT recovery-kernel signature in pulsar glitches across all "
                   "channels. (PG.01) glitch sizes show real log-periodic structure, "
                   "but it is the known two-population BIMODALITY (vanishes under the "
                   "population-controlled null) -- NOT a kernel comb; (PG.02/03) the "
                   "decisive per-pulsar kernel ladders are null; (PG.04) the recovery "
                   "fraction Q is not at phi0-multiples, and the multi-component tau_d "
                   "ratios match neither the (3/2)^k ladder nor the det'-clean 2-mode "
                   "bend 2.7095 (the correct v124 candidate) -- though the WALL holds "
                   f"({n_wall_ok}/{n_glitches_wall} glitches need <=2 decay modes, "
                   "consistent with the n=N_fam=3 "
                   "pole). This mirrors the FRB energy-cascade result (generic "
                   "discreteness, not kernel-specific) -- a clean cross-domain NULL. "
                   "The exact clock is WALLED (2 modes + floor, not an infinite ladder), "
                   "so sustained DSI needs a cascade; the open, more-sensitive probe is "
                   "the fixed-ratio (2.7095) two-exponential recovery WAVEFORM template "
                   "(matched filter), not summary Q/tau_d (see quantum-testbed QT.04).")
    print(f"\n==> VERDICT: {verdict}")

    RESULTS.mkdir(exist_ok=True)
    _plot(sizes, seed)
    out = {
        "constants": constants.summary(),
        "catalogue": {"n_glitches": len(records), "n_pulsars": n_pulsars,
                      "n_with_size": len(sizes),
                      "prolific": prolific_glitchers(records, top=6)},
        "pg01_discreteness": {
            "lognormal_ks_p": rep.lognormal.ks_pvalue,
            "gmm_best_k": rep.gmm.best_k, "gmm_delta_bic": rep.gmm.delta_bic,
            "best_ratio": lp.best_ratio, "z_max": lp.z_max,
            "p_value": lp.p_value, "p_lognormal": lp.p_lognormal,
            "p_kde": lp.p_kde, "p_gmm": lp.p_gmm,
            "nearest_ratio": lp.nearest.name, "nearest_rel_err": lp.nearest_rel_err,
            "targeted": [vars(t) for t in rep.targeted], "verdict": rep.verdict,
        },
        "pg02_size_ladder": vars(pg02),
        "pg03_waiting_ladder": vars(pg03),
        "pg04_recovery": {"q_cluster": vars(pg04q), "tau_ladder": vars(pg04t),
                          "bend_wall": vars(pg04b)},
        "verdict": verdict,
    }
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="TFPT recovery-kernel search in pulsar glitches (Jodrell Bank)")
    ap.add_argument("command",
                    choices=["audit", "validate", "analyze", "dynamic", "nicer", "vela"],
                    nargs="?", default="analyze")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--download", action="store_true",
                    help="vela: download one real NICER Vela obs before folding")
    args = ap.parse_args(argv)
    if args.command == "audit":
        return _audit()
    if args.command == "validate":
        return _validate()
    if args.command == "dynamic":
        return _dynamic(args.seed)
    if args.command == "nicer":
        return _nicer(args.seed)
    if args.command == "vela":
        return _vela(args.seed, args.download)
    return _analyze(args.seed)


if __name__ == "__main__":
    raise SystemExit(main())
