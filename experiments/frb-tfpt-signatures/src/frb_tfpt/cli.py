"""Command-line driver: ``frb-tfpt audit`` and ``frb-tfpt analyze``.

``analyze`` runs the preregistered, multi-dataset, surrogate-calibrated TFPT
boundary-recovery search, aggregates the axes into an overall verdict that can
only become 'confirmed' on replicated + discriminating support, writes
``results/results.json`` and the diagnostic plots, and prints a scoreboard.

Firewall: search targets, not claims. FRBs are not new gravity, not a Hawking
signature; at most a repeater echoes the dimensionless recovery kernel after
plasma (DM, RM, scattering) removal.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path

import numpy as np

from . import cosmology as cosmo
from . import recovery_kernel as kernel
from . import tfpt_ladder
from .activity_windows import activity_window_test
from .data_io import (
    load_chime_catalog1,
    load_dmz_sharma,
    load_dmz_table4,
    load_fast_20240114A_pol,
    load_fast_121102_1652,
    load_frb20240619D,
    load_frb121102_aggarwal,
    repeater_subsets,
)
from .dmz_baryon import baryon_test
from .drift_freq import drift_score
from .echo_ratio import evaluate_echo_semantic
from .energy_clusters import energy_cluster_score, fit_spacing_ladder, periodogram_curve
from .fingerprint import EvidenceAxis, aggregate_axes
from .markov_spectrum import markov_spectrum_test
from .no_native_dispersion import no_native_dispersion_test
from .periodic_population import evaluate_periodic_windows
from .recovery_observable_model import shared_kernel_search, var1_spectrum
from .rm_relaxation_step import rm_step_relaxation_test
from .timing import folded_rayleigh, waiting_time_structure
from .window_extraction import extract_windows

RESULTS = Path(__file__).resolve().parents[2] / "results"


def _jsonable(obj):
    if is_dataclass(obj):
        return {k: _jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    return obj


# --------------------------------------------------------------------------- #
def cmd_audit(_: argparse.Namespace) -> int:
    print("TFPT FRB prediction layer (derived from c3=1/(8pi), g_car=5)\n")
    print("  Frozen boundary-recovery kernel (exact rationals):")
    for k, v in kernel.kernel_fractions().items():
        print(f"    {k:10s} = {str(v):8s} = {float(v):.6f}")
    print("\n  seed-block cosmology:")
    print(f"    beta_rad   = {kernel.BETA_DEG:.6f} deg")
    print(f"    Omega_b    = {kernel.OMEGA_B_TFPT:.6f}")
    print("\n  recovery ratios (search targets; no fitted exponents):")
    for t in kernel.kernel_ratios():
        print(f"    {t.name:20s} {t.value:9.5f}  [{t.channel}] ({t.provenance})")
    return 0


# --------------------------------------------------------------------------- #
def _plot(fn):
    try:
        fn()
    except Exception as exc:  # noqa: BLE001
        print(f"  [plot skipped] {exc}")


def cmd_analyze(args: argparse.Namespace) -> int:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    RESULTS.mkdir(exist_ok=True)
    out: dict = {"firewall": "search targets, not claims", "kernel_frozen": True,
                 "search_targets": {}, "generic": {}}
    axes: list[EvidenceAxis] = []
    print("=" * 72)
    print("TFPT FRB boundary-recovery search (preregistered; firewall in force)")
    print("=" * 72)

    # ---- FRB.05: DM-z baryon (consistency only) ----------------------------
    print("\n[FRB.05] DM(z) baryon test (consistency only)")
    b4 = baryon_test(load_dmz_table4(), seed=args.seed)
    bs = baryon_test(load_dmz_sharma(), seed=args.seed)
    out["search_targets"]["FRB05_baryon"] = {"adb84d": _jsonable(b4), "sharma2024": _jsonable(bs)}
    for b in (b4, bs):
        print(f"  {b.source}: {b.note}")
    axes.append(EvidenceAxis("FRB05_baryon", b4.c_baryon, "consistency",
                             discriminating=False, replicated=True,
                             note="Omega_b consistent; cannot discriminate TFPT vs Planck"))
    _plot(lambda: _plot_macquart(plt, load_dmz_table4(), b4, RESULTS / "frb05_macquart.png"))

    # ---- FRB.03: activity-window population test ----------------------------
    print("\n[FRB.03] activity-window eigenwidths (population)")
    aw = activity_window_test()
    pop = evaluate_periodic_windows(seed=args.seed)
    out["search_targets"]["FRB03_activity_windows"] = {
        "per_source": _jsonable(aw), "population": _jsonable(pop)}
    for m in aw.matches:
        core = (f"{m.w_core_over_p:.4f} vs 1/27 ({100*m.core_rel_err:.0f}%)"
                if np.isfinite(m.w_core_over_p) else "n/a")
        print(f"  {m.name:16s} W_broad/P={m.w_broad_over_p:.4f} vs 8/27 "
              f"({100*m.broad_rel_err:.0f}%) | W_core/P={core}")
    print(f"  population: {pop.verdict} (null p={pop.null_p:.3f}, LOO stable={pop.leave_one_out_stable})")
    # Package E: data-derived windows for FRB 20180916B (folded CHIME phases) --
    chime_w = load_chime_catalog1()
    m916w = [i for i, x in enumerate(chime_w.repeater) if x == "FRB20180916B"]
    if len(m916w) >= 10:
        ew = extract_windows("FRB 20180916B (CHIME folded)", chime_w.mjd[m916w], 16.33)
        out["search_targets"]["FRB03_activity_windows"]["data_derived_FRB20180916B"] = _jsonable(ew)
        print(f"  data-derived (folded {ew.n_bursts} CHIME bursts): "
              f"W_broad/P={ew.w_broad_over_p:.3f} vs 8/27 ({100*ew.broad_rel_err:.0f}%), "
              f"W_core/P={ew.w_core_over_p:.3f} vs 1/27 ({100*ew.core_rel_err:.0f}%)")
    axes.append(EvidenceAxis("FRB03_activity_window", aw.c_window, "candidate",
                             p_value=pop.null_p, q_value=pop.null_p,
                             discriminating=True, replicated=pop.enough_sources,
                             note=pop.verdict))
    _plot(lambda: _plot_pop_windows(plt, aw, RESULTS / "frb03_population_windows.png"))

    # ---- FRB.02: semantics-correct echo ratios on the FAST 1652 sample ------
    print("\n[FRB.02] recovery echo ratios (observable-semantics split, FAST 1652)")
    fast = load_fast_121102_1652()
    echo = evaluate_echo_semantic(fast, seed=args.seed)
    out["search_targets"]["FRB02_echo_ratio"] = _jsonable(echo)
    print(f"  {echo.source}: {echo.n_bursts} bursts, {echo.n_pairs} within-session pairs, "
          f"{echo.n_sessions} sessions; raw column = {echo.raw_column}; nulls={echo.nulls_used}")
    for cname, ch in echo.channels.items():
        flag = " [AUDIT, not theory]" if ch["audit"] else ""
        tag = "energy ratio" if ch["transform"] == "identity" else "sqrt(energy) [amplitude]"
        print(f"    channel {cname}{flag}: {tag}; best q={ch['best_q']:.3f}; "
              f"significant={ch['significant']}")
    if echo.audit_anomaly:
        print(f"    AUDIT ANOMALY: {echo.audit_anomaly}")
        for tgt, sd in echo.session_diagnostics.items():
            print(f"      session-diag[{tgt}]: top-session frac="
                  f"{sd['max_single_session_fraction']}, contributing={sd['n_sessions_contributing']}, "
                  f"robust(no single storm)={sd['robust_no_single_storm']}")
    # theory channels (energy + amplitude) drive the axis; the audit channel never does.
    # The 8/27 excess lives ONLY in the audit channel under correct semantics.
    theory_significant = any(not ch["audit"] and ch["significant"] for ch in echo.channels.values())
    echo_status = "candidate" if theory_significant else "null"
    theory_min_q = min((ch["best_q"] for ch in echo.channels.values() if not ch["audit"]),
                       default=1.0)
    axes.append(EvidenceAxis("FRB02_echo_ratio", echo.c_echo_theory, echo_status,
                             q_value=theory_min_q, discriminating=True, replicated=False,
                             observable_semantics_valid=True, note=echo.verdict))
    _plot(lambda: _plot_fast_echo(plt, fast, RESULTS / "frb02_fast_echo_ratio.png"))

    # ---- generic: structure vs kernel (kept strictly separate) -------------
    print("\n[generic] energy structure vs TFPT kernel (FAST 1652 energies)")
    ladder = fit_spacing_ladder(fast.energy, seed=args.seed)
    ec = energy_cluster_score("FRB20121102A FAST", fast.energy, seed=args.seed)
    # structure_score: is the distribution non-smooth / multimodal? (NOT TFPT-specific)
    # kernel_score:    do the cluster spacings match a single frozen kernel ratio?
    structure_score = float(ec.c_e)
    kernel_score = float(ladder.c_ladder)
    out["generic"]["fast_spacing_ladder"] = _jsonable(ladder)
    out["generic"]["fast_energy_cluster"] = _jsonable(ec)
    out["generic"]["score_split"] = {
        "structure_score": structure_score, "kernel_score": kernel_score,
        "note": "structure_score (real but NOT TFPT-specific) is kept out of the kernel "
                "verdict; only kernel_score reflects a frozen-ratio match."}
    print(f"  structure_score={structure_score:.2f} (multimodal/non-smooth, not TFPT-specific)")
    print(f"  kernel_score={kernel_score:.2f}  -> {ladder.verdict}")
    print(f"  (energy cluster: {ec.verdict})")
    _plot(lambda: _plot_energy(plt, fast.energy, ec, "FRB 20121102A (FAST 1652)",
                               RESULTS / "frb121102_energy.png"))
    _plot(lambda: _plot_periodogram(plt, fast.energy, "FRB 20121102A (FAST 1652)", args.seed,
                                    RESULTS / "frb121102_logperiodogram.png"))

    # ---- shared recovery-eigenvalue search (multi-observable) --------------
    print("\n[shared] recovery-eigenvalue search across observables (FAST 1652)")
    shared = shared_kernel_search(fast, seed=args.seed)
    out["generic"]["shared_kernel"] = _jsonable(shared)
    for c in shared.channels:
        print(f"    {c.name:12s} a={c.a:.3f} a_ci=[{c.a_ci_lo:.3f},{c.a_ci_hi:.3f}] "
              f"nearest={c.nearest_kernel} kernel_in_a_ci={c.kernel_in_a_ci}")
    print(f"  {shared.verdict}")
    # Package G: full VAR(1) over available observables (per source) -----------
    for label, ser in (("FAST 1652", fast), ("FRB 20240114A pol", load_fast_20240114A_pol())):
        var = var1_spectrum(ser, seed=args.seed)
        out["generic"].setdefault("var1", {})[label] = _jsonable(var)
        print(f"  VAR(1) [{label}]: {var.note if var.available else var.note or 'data-limited'}")

    # ---- FRB.04: polarisation Markov spectrum (v1 strong test) -------------
    print("\n[FRB.04] polarisation PA/RM Markov spectrum (v1 strong test, energy kernel)")
    pol_series = load_fast_20240114A_pol()
    mk_pa = markov_spectrum_test(pol_series, channel="pa", seed=args.seed)
    mk_rm = markov_spectrum_test(pol_series, channel="rm", seed=args.seed)
    # N accounting: one source of truth (n_raw vs n_used per channel)
    n_raw = len(pol_series)
    n_with_pa = int(np.isfinite(pol_series.pa_deg).sum())
    n_with_rm = int(np.isfinite(pol_series.rm).sum())
    out["search_targets"]["FRB04_markov_spectrum"] = {
        "n_accounting": {"n_raw": n_raw, "n_used_pa": n_with_pa, "n_used_rm": n_with_rm,
                         "note": "n_raw = rows in the v5 CSV (S/N>20 catalogue)"},
        "pa": _jsonable(mk_pa), "rm": _jsonable(mk_rm)}
    print(f"  n_raw={n_raw}, n_used_pa={n_with_pa}, n_used_rm={n_with_rm}")
    print(f"  PA: {mk_pa.note}")
    if mk_pa.null_pvals:
        print(f"      per-null p: { {k: round(v, 3) for k, v in mk_pa.null_pvals.items()} }")
    print(f"  RM: {mk_rm.note}")
    if mk_rm.null_pvals:
        print(f"      per-null p: { {k: round(v, 3) for k, v in mk_rm.null_pvals.items()} }")
    mk_best = max((mk_pa, mk_rm), key=lambda r: r.c_markov)
    axes.append(EvidenceAxis("FRB04_polarisation", mk_best.c_markov,
                             "support" if mk_best.c_markov > 0 else
                             ("data_limited" if not mk_best.available else "null"),
                             p_value=mk_best.null_p, q_value=mk_best.null_p,
                             discriminating=True, replicated=False, note=mk_best.note))
    _plot(lambda: _plot_markov(plt, mk_pa, mk_rm, RESULTS / "frb04_markov_spectrum.png"))
    _plot(lambda: _plot_rm_staircase(plt, pol_series, RESULTS / "frb04_rm_staircase.png"))

    # ---- FRB.04b: v2 EXPLORATORY RM step-relaxation (kernel {2/3,1/3}) ------
    rm_step = rm_step_relaxation_test(pol_series, seed=args.seed)
    out["search_targets"]["FRB04b_rm_step_relaxation_v2_exploratory"] = {
        "status": "exploratory_not_preregistered_no_promotion_without_external_replication",
        "result": _jsonable(rm_step)}
    print(f"  [v2 exploratory] RM vs step kernel {{2/3,1/3}}: {rm_step.note}")
    if rm_step.null_pvals:
        print(f"      per-null p: { {k: round(v, 3) for k, v in rm_step.null_pvals.items()} }")
        if rm_step.null_pvals.get("ar1_drift", 0) > 0.05:
            print("      -> the AR(1)-drift null reproduces the proximity: consistent with a "
                  "SMOOTH magneto-ionic drift, not a discrete step spectrum")

    # ---- FRB.01: no native dispersion (kill test, raw data required) -------
    disp = no_native_dispersion_test()
    out["search_targets"]["FRB01_dispersion"] = _jsonable(disp)
    print(f"\n[FRB.01] {disp.note}")
    axes.append(EvidenceAxis("FRB01_dispersion", 0.0, "data_limited", note=disp.note))

    # ---- extra stress dataset (drop-in) ------------------------------------
    d619 = load_frb20240619D()
    if d619.available:
        e619 = evaluate_echo_ratios_by_session(d619, seed=args.seed)
        out["search_targets"]["FRB20240619D_echo"] = _jsonable(e619)
        print(f"\n[stress] FRB 20240619D: {e619.verdict}")

    # ---- CHIME breadth (sanity) -------------------------------------------
    chime = load_chime_catalog1()
    drift = drift_score(chime, seed=args.seed)
    out["generic"]["chime_drift"] = _jsonable(drift)
    m916 = [i for i, x in enumerate(chime.repeater) if x == "FRB20180916B"]
    if len(m916) >= 6:
        fold = folded_rayleigh(chime.mjd[m916], 16.33)
        out["generic"]["frb20180916B_fold"] = _jsonable(fold)
    wt = waiting_time_structure(load_frb121102_aggarwal().mjd, seed=args.seed)
    out["generic"]["aggarwal_waiting"] = _jsonable(wt)
    _plot(lambda: _plot_waiting(plt, wt, RESULTS / "frb121102_waiting.png"))

    # ---- aggregate ---------------------------------------------------------
    overall = aggregate_axes(axes)
    out["axes"] = [_jsonable(a) for a in axes]
    out["overall"] = overall
    print("\n" + "=" * 72)
    print("OVERALL:", overall["verdict"])
    for bucket in ("support_axes", "candidate_axes", "null_axes",
                   "consistency_axes", "data_limited_axes"):
        print(f"  {bucket:20s} {overall[bucket]}")
    print("=" * 72)
    _plot(lambda: _plot_fingerprint(plt, axes, overall, RESULTS / "frb_fingerprint_summary.png"))

    (RESULTS / "results.json").write_text(json.dumps(_jsonable(out), indent=2))
    print(f"\nWrote {RESULTS / 'results.json'} and plots to {RESULTS}/")
    return 0


# --------------------------------------------------------------------------- #
def _plot_macquart(plt, tbl, res, path):
    ok = np.isfinite(tbl.z) & np.isfinite(tbl.dm_cosmic) & (tbl.dm_cosmic > 0)
    z, dmc = tbl.z[ok], tbl.dm_cosmic[ok]
    zs = np.linspace(0.01, max(z) * 1.05, 100)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.scatter(z, dmc, s=22, color="#357", alpha=0.7, label=f"localized FRBs (n={len(z)})")
    ax.plot(zs, cosmo.dm_cosmic(zs, kernel.OMEGA_B_TFPT), "g-",
            label=f"TFPT $\\Omega_b$={kernel.OMEGA_B_TFPT:.4f}")
    ax.plot(zs, cosmo.dm_cosmic(zs, res.omega_b_fit), "r--",
            label=f"FRB fit $\\Omega_b$={res.omega_b_fit:.4f}$\\pm${res.omega_b_err:.4f}")
    ax.set_xlabel("redshift z"); ax.set_ylabel(r"DM$_{\rm cosmic}$  [pc cm$^{-3}$]")
    ax.set_title(f"FRB.05 Macquart relation (TFPT at {res.tension_tfpt_sigma:.1f}$\\sigma$, "
                 f"non-discriminating)")
    ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _plot_pop_windows(plt, aw, path):
    fig, ax = plt.subplots(figsize=(7, 4))
    names = [m.name for m in aw.matches]
    x = np.arange(len(names))
    ax.bar(x, [m.w_broad_over_p for m in aw.matches], width=0.5, color="#9bd",
           edgecolor="#247", label="W_broad/P")
    ax.axhline(kernel.SQRT_LAMBDA2, color="g", label="8/27 ($\\sqrt{\\lambda_2}$)")
    ax.axhline(kernel.SQRT_LAMBDA3, color="c", ls=":", label="1/27 ($\\sqrt{\\lambda_3}$)")
    for m, xx in zip(aw.matches, x):
        if np.isfinite(m.w_core_over_p):
            ax.scatter([xx], [m.w_core_over_p], color="#c33", zorder=5,
                       label="W_core/P" if xx == x[0] else None)
    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=8)
    ax.set_ylabel("window / period")
    ax.set_title(f"FRB.03 activity windows (n={len(names)}; population test needs >=5)")
    ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _plot_fast_echo(plt, series, path):
    sess = series.session_id
    val = series.energy
    lr = []
    for s in np.unique(sess):
        mm = sess == s
        v = val[mm]
        v = v[np.isfinite(v) & (v > 0)]
        if len(v) >= 2:
            lr.append(np.log10(v[1:] / v[:-1]))
    lr = np.concatenate(lr) if lr else np.array([0.0])
    fig, ax = plt.subplots(figsize=(7.4, 4))
    ax.hist(lr, bins=40, color="#cdb", edgecolor="#363")
    # legitimate ENERGY targets on an energy-ratio axis (green) ...
    for v, lab in ((kernel.LAMBDA2, "64/729"), (kernel.LAMBDA3, "1/729")):
        for s in (+1, -1):
            ax.axvline(s * np.log10(v), color="#2a7", lw=1.6)
        ax.text(np.log10(v), ax.get_ylim()[1] * 0.95, f"{lab}\n(energy✓)", color="#175",
                fontsize=7, ha="center", va="top")
    # ... vs the amplitude NUMBERS misapplied to an energy ratio (orange, audit)
    for v, lab in ((kernel.SQRT_LAMBDA2, "8/27"), (kernel.SQRT_LAMBDA3, "1/27")):
        for s in (+1, -1):
            ax.axvline(s * np.log10(v), color="#e80", ls="--", lw=1.4)
        ax.text(np.log10(v), ax.get_ylim()[1] * 0.62, f"{lab}\n(amp #, audit)", color="#a50",
                fontsize=7, ha="center", va="top")
    ax.set_xlabel(r"$\log_{10}(E_{n+1}/E_n)$ within session")
    ax.set_ylabel("count")
    ax.set_title(f"FRB.02 echo ratios FAST 1652 ({len(lr)} pairs): the excess sits at the "
                 f"8/27 amplitude #, not the 64/729 energy target", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _plot_markov(plt, mk_pa, mk_rm, path):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axhline(kernel.LAMBDA2, color="g", label="64/729")
    ax.axhline(kernel.LAMBDA3, color="c", ls=":", label="1/729")
    any_data = False
    for i, (mk, lbl) in enumerate([(mk_pa, "PA"), (mk_rm, "RM")]):
        if mk.available and mk.eigs:
            any_data = True
            ax.scatter([i] * len(mk.eigs), mk.eigs, s=60, label=f"{lbl} eigs")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["PA channel", "RM channel"])
    ax.set_ylabel("non-trivial |eigenvalue|")
    ax.set_yscale("symlog", linthresh=1e-3)
    title = ("FRB.04 PA/RM Markov spectrum vs kernel" if any_data
             else "FRB.04 Markov spectrum: DATA-LIMITED (drop in FRB 20240114A pol catalog)")
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _plot_rm_staircase(plt, series, path):
    fig, ax = plt.subplots(figsize=(7, 4))
    if series.available and np.isfinite(series.rm).sum() > 5:
        ax.scatter(series.mjd, series.rm, s=10, color="#357")
        ax.set_xlabel("MJD"); ax.set_ylabel(r"RM [rad m$^{-2}$]")
        ax.set_title("FRB.04 RM(t) staircase test")
    else:
        ax.text(0.5, 0.5, "DATA-LIMITED\nrm_staircase activates when a repeater\n"
                "RM time series is loaded (e.g. FRB 20240114A)",
                ha="center", va="center", fontsize=11)
        ax.axis("off")
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _plot_fingerprint(plt, axes, overall, path):
    colors = {"support": "#2a2", "candidate": "#e90", "null": "#888",
              "consistency": "#48c", "data_limited": "#ccc"}
    fig, ax = plt.subplots(figsize=(7, 4.2))
    names = [a.name for a in axes]
    y = np.arange(len(names))
    ax.barh(y, [a.score for a in axes],
            color=[colors.get(a.status, "#ccc") for a in axes], edgecolor="#333")
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=8)
    ax.set_xlim(0, 1); ax.set_xlabel("axis score")
    ax.set_title(f"TFPT FRB fingerprint -> {overall['verdict']}", fontsize=11)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in colors.values()]
    ax.legend(handles, colors.keys(), fontsize=7, loc="lower right")
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _plot_energy(plt, energy, ec, title, path):
    x = np.log10(energy[np.isfinite(energy) & (energy > 0)])
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(x, bins=30, density=True, color="#bcd", edgecolor="#346", alpha=0.8, label="bursts")
    xs = np.linspace(x.min(), x.max(), 300)
    ax.plot(xs, _norm_pdf(xs, ec.lognormal.mu, ec.lognormal.sigma), "k--",
            label=f"log-normal null (KS p={ec.lognormal.ks_pvalue:.2f})")
    for mlog in ec.gmm.means_log10:
        ax.axvline(mlog, color="#c33", lw=1, alpha=0.7)
    ax.set_xlabel("log10 energy [erg]"); ax.set_ylabel("density")
    ax.set_title(f"{title}: energy distribution (best_k={ec.gmm.best_k}, C_E={ec.c_e:.2f})")
    ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _plot_periodogram(plt, energy, title, seed, path):
    ratios, z, z95 = periodogram_curve(energy, seed=seed)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ratios, z, color="#225")
    ax.axhline(z95, color="#c33", ls="--", label="surrogate 95% bar")
    ax.set_xlabel("energy spacing ratio  E_k / E_{k+1}")
    ax.set_ylabel("Rayleigh log-periodic power")
    ax.set_title(f"{title}: log-periodogram (cascade test)")
    ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _plot_waiting(plt, wt, path):
    if not wt.log10_seconds:
        return
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(wt.log10_seconds, bins=24, color="#cdb", edgecolor="#363")
    ax.set_xlabel("log10 waiting time [s]"); ax.set_ylabel("count")
    ax.set_title(f"FRB 20121102A waiting times (best_k={wt.best_k}, bimodal={wt.bimodal})")
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _norm_pdf(x, mu, sigma):
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))


# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="frb-tfpt",
                                description="TFPT-signature search in real FRB data")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("audit", help="print the TFPT prediction layer").set_defaults(func=cmd_audit)
    a = sub.add_parser("analyze", help="run the preregistered search on the bundled real data")
    a.add_argument("--seed", type=int, default=0)
    a.set_defaults(func=cmd_analyze)
    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
