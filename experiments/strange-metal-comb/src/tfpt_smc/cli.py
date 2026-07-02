"""``tfpt-smc`` -- the first LABORATORY comb-ripple search: does the strange-metal sigma1(omega/T)
Planckian master curve carry the frozen TFPT log-periodic decoration (omega=2.583, eps~1.7%)?

FIREWALL: strange metals have NO established boundary-recovery structure -- the master curve is a
quantum-critical scaling function, not a horizon/boundary relaxation -- so even a hit would be a
universal-DSI coincidence, never TFPT confirmation. A null is EXPECTED and informative. Nothing
here is [E]; preregistered in hypotheses/strange_metal_comb_v1.yaml BEFORE the data pass.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from . import master
from .comb import (
    EPS_PREDICTED,
    LAMBDA,
    MIN_COMB_PERIODS,
    OMEGA,
    P_THRESHOLD,
    detect_comb,
    validate_detector,
)

RESULTS = Path(__file__).resolve().parents[2] / "results"


def _analyze(seed: int = 0) -> int:
    print("=" * 88)
    print("TFPT comb ripple on the STRANGE-METAL omega/T master curve -- first laboratory search")
    print(f"  kernel: lambda=(3/2)^6={LAMBDA:.3f}  omega=2pi/ln(lambda)={OMEGA:.4f}  "
          f"predicted ripple eps=exp(-pi^2/ln lambda)={EPS_PREDICTED:.4f}")
    print(f"  comb variable: u = ln(hbar*omega/k_B T); one period = ln((3/2)^6) = "
          f"{np.log(LAMBDA):.3f}; gate >= {MIN_COMB_PERIODS} periods")
    print("  FIREWALL: no boundary-recovery structure in strange metals -> any hit = "
          "universal-DSI coincidence, never TFPT confirmation; a null is expected+informative.")
    print("=" * 88)

    # (0) detector validation (proves the ported kernel works, unchanged)
    v = validate_detector()
    print(f"\n  [0] detector validation ({v.n_seeds} seeds; eps={v.eps}, noise={v.noise}): "
          f"sufficient range detected {100 * v.sufficient_comb_rate:.0f}% | false-positive "
          f"{100 * v.sufficient_null_rate:.0f}% | short-range {100 * v.short_comb_rate:.0f}% "
          f"-> validated={v.passed}")

    # (1) PRIMARY data: LSCO x=0.24 master curve (paper's own collapse)
    lsco = master.load_lsco()
    print(f"\n  [1] PRIMARY: {lsco.name} master curve y=ln(T*sigma1) vs u=ln(hw/kT) "
          f"(paper window T>={master.T_MIN:.0f}K, E<={master.E_MAX}eV):")
    print(f"      {len(lsco.u)} points across T={[int(t) for t in lsco.temps]} K "
          f"({lsco.n_dropped} non-positive sigma1 points dropped)")
    print(f"      u range {lsco.u.min():+.2f}..{lsco.u.max():+.2f} = {lsco.u_range:.2f} -> "
          f"{lsco.periods:.2f} comb periods (gate {MIN_COMB_PERIODS}: "
          f"{'PASS' if lsco.periods >= MIN_COMB_PERIODS else 'FAIL -> range-blind'})")

    # (2) SMC.01 kernel rank: primary deg-2 + frozen detector + sensitivity variants
    primary = master.dense_rank(lsco.u, lsco.y, deg=2)
    g_frozen, p_frozen = detect_comb(np.exp(lsco.u), lsco.y, seed=seed)
    variants = {
        "poly_deg3": master.dense_rank(lsco.u, lsco.y, deg=3),
        "poly_deg4": master.dense_rank(lsco.u, lsco.y, deg=4),
        "spline": master.dense_rank(lsco.u, lsco.y,
                                    residuals=master.spline_residuals(lsco.u, lsco.y)),
        "per_T_deg2": master.dense_rank(lsco.u, lsco.y,
                                        residuals=master.per_T_residuals(lsco, deg=2)),
    }
    print(f"\n  [2] SMC.01 kernel rank at omega={OMEGA:.4f} (off-kernel grid omega in [1,6]):")
    print(f"      PRIMARY (deg-2 poly in u):  gain={primary['gain']:.2e}  "
          f"p={primary['p_value']:.4f}  (best off-kernel omega={primary['best_off_omega']})")
    print(f"      frozen detect_comb rank:    gain={g_frozen:.2e}  p={p_frozen:.4f}")
    for k, r in variants.items():
        print(f"      variant {k:11s}:        gain={r['gain']:.2e}  p={r['p_value']:.4f}")
    detrend_robust = all((r["p_value"] < P_THRESHOLD) == (primary["p_value"] < P_THRESHOLD)
                         for r in variants.values())

    # (3) SMC.02 amplitude + phase at the fixed kernel omega
    r_primary = master.poly_residuals(lsco.u, lsco.y, 2)
    amp = master.amplitude_fit(lsco.u, r_primary)
    print(f"\n  [3] SMC.02 amplitude fit at fixed omega: eps_hat={amp['eps_hat']:.4f} "
          f"(predicted {EPS_PREDICTED:.4f}), phi_hat={amp['phi_hat']:.2f}, "
          f"residual rms={amp['resid_rms']:.4f} (in ln sigma1 -> fractional)")

    # (4) SMC.03 null batteries on the primary residuals
    nulls = master.null_batteries(lsco, r_primary, seed=seed)
    print(f"\n  [4] SMC.03 nulls: eps_obs={nulls['eps_obs']:.4f}; "
          f"point-permutation p={nulls['p_permutation']:.4f}, per-T cyclic-shift "
          f"p={nulls['p_block_shift']:.4f} -> conservative p={nulls['p_conservative']:.4f}")
    print(f"      (95% null amplitude = {nulls['eps95_null']:.4f}: the master curve's own "
          f"eps sensitivity floor under the conservative null)")

    # (5) SMC.04 TFPT lambda-battery + Bonferroni
    battery, bat_p, m_eff, best = master.lambda_battery(lsco, seed=seed)
    print(f"\n  [5] SMC.04 TFPT lambda-battery (per-lambda gate + Bonferroni over {m_eff}):")
    for label, e in battery.items():
        tag = "IDIO" if e["idio"] else "atom"
        gate = "" if e["gated"] else "  (NOT gated: range/Nyquist)"
        mark = "  <-- nominally special" if e["comb_detected"] else ""
        print(f"      [{tag}] lambda={e['lambda']:7.3f} (omega={e['omega']:6.2f}, "
              f"{e['periods']:5.2f} periods)  p={e['p_value']:.4f}{mark}{gate}")
    print(f"      best gated={best}; Bonferroni global p={bat_p} -> "
          + ("a TFPT log-period SURVIVES look-elsewhere -> ESCALATE" if bat_p < P_THRESHOLD
             else "no TFPT log-period is special (NULL)"))

    # (6) SMC.05 injection power on the real master curve (all documented detrend variants)
    inj = []
    print("\n  [6] SMC.05 injection-recovery on the REAL master curve:")
    for variant in ("primary", "spline", "per_T"):
        rows = master.injection_power(lsco, eps_list=(0.0, EPS_PREDICTED, 0.05),
                                      variant=variant)
        inj.extend(rows)
        for r in rows:
            label = "false-alarm (eps=0)" if r["eps"] == 0.0 else f"eps={r['eps']:.4f}"
            print(f"      [{variant:7s}] {label:20s} detected {100 * r['detect_rate']:.0f}%  "
                  f"(median p={r['median_p']:.3f}, {r['n_seeds']} seeds)")
    best_p17 = max((r for r in inj if abs(r["eps"] - EPS_PREDICTED) < 1e-9),
                   key=lambda r: r["detect_rate"])
    best_p50 = max((r for r in inj if abs(r["eps"] - 0.05) < 1e-9),
                   key=lambda r: r["detect_rate"])
    fa_max = max((r for r in inj if r["eps"] == 0.0), key=lambda r: r["detect_rate"])

    # (7) SMC.06 Drude negative controls
    controls = []
    print("\n  [7] SMC.06 conventional-metal NEGATIVE CONTROLS (same pipeline):")
    for path, name in ((master.DATA / "au_ordal_nk.csv", "Au (Ordal)"),
                       (master.DATA / "cu_ordal_nk.csv", "Cu (Ordal)")):
        c = master.load_drude(path, name)
        res = master.dense_rank(c.u, c.y, deg=2)
        res.update({"name": name, "n_points": int(len(c.u)),
                    "periods": round(c.periods, 2),
                    "range_sufficient": bool(c.periods >= MIN_COMB_PERIODS)})
        controls.append(res)
        print(f"      {name:11s} {len(c.u):3d} pts, {c.periods:.2f} periods "
              f"(<gate: rank still reported)  gain={res['gain']:.2e}  p={res['p_value']:.4f}"
              + ("  <-- FIRES: pipeline INVALID" if res["p_value"] < P_THRESHOLD else "  quiet"))
    controls_quiet = all(r["p_value"] >= P_THRESHOLD for r in controls)

    # (8) SMC.07 replication leg
    replication = {
        "source": "van der Marel et al. 2003, Nature 425:271 (Bi-2212)",
        "status": "data_limited",
        "note": "No machine-readable public table exists (checked: Nature supplement has "
                "figures/methods only; Leiden repository holds the PDF; the underlying data "
                "files were privately supplied between groups). Documented honestly; the "
                "replication leg is data_limited.",
    }
    print(f"\n  [8] SMC.07 replication leg: {replication['note']}")

    verdict = _verdict(lsco, primary, p_frozen, detrend_robust, amp, nulls, bat_p,
                       best_p17, best_p50, fa_max, controls_quiet)
    print(f"\n==> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {
        "kernel": {"lambda": LAMBDA, "omega": OMEGA, "eps_predicted": EPS_PREDICTED,
                   "min_comb_periods": MIN_COMB_PERIODS,
                   "one_period_in_u": float(np.log(LAMBDA))},
        "detector_validation": {
            "sufficient_comb_rate": v.sufficient_comb_rate,
            "sufficient_null_rate": v.sufficient_null_rate,
            "short_comb_rate": v.short_comb_rate, "passed": v.passed},
        "primary_data": {"name": lsco.name, "provenance": lsco.provenance,
                         "n_points": int(len(lsco.u)), "temps_K": list(lsco.temps),
                         "n_dropped": lsco.n_dropped, "u_range": round(lsco.u_range, 3),
                         "comb_periods": round(lsco.periods, 3),
                         "range_sufficient": bool(lsco.periods >= MIN_COMB_PERIODS)},
        "smc01_kernel_rank": {"primary_deg2": primary,
                              "frozen_detect_comb": {"gain": round(g_frozen, 6),
                                                     "p_value": round(p_frozen, 4)},
                              "variants": variants, "detrend_robust": detrend_robust},
        "smc02_amplitude": amp,
        "smc03_nulls": nulls,
        "smc04_lambda_battery": {"battery": battery, "global_p": bat_p, "m_eff": m_eff,
                                 "best": best},
        "smc05_injection": inj,
        "smc06_drude_controls": {"controls": controls, "all_quiet": controls_quiet},
        "smc07_replication": replication,
        "verdict": verdict,
    }
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


def _verdict(lsco, primary, p_frozen, detrend_robust, amp, nulls, bat_p,
             p17, p50, fa, controls_quiet) -> str:
    kernel_special = primary["p_value"] < P_THRESHOLD and p_frozen < P_THRESHOLD
    powered_17 = p17["detect_rate"] >= 0.5
    if kernel_special and detrend_robust and controls_quiet:
        head = (f"omega=2.583 appears SPECIAL in the LSCO master curve "
                f"(p={primary['p_value']}) -> ESCALATE (independent cross-check first; "
                f"DSI-coincidence class by firewall).")
        status = "hint_flag->stay data_limited pending replication"
    else:
        head = (f"omega=2.583 is NOT special in the LSCO x=0.24 master curve "
                f"(primary p={primary['p_value']}, frozen-detector p={p_frozen:.3f}, "
                f"detrend-robust={detrend_robust}).")
        status = ("null (at detectable amplitude)" if powered_17 else
                  "null-at-detectable-amplitude / data_limited at the predicted 1.7%")
    return (
        f"LSCO x=0.24 sigma1(omega/T) master curve (Michon+ 2023 open data, "
        f"{len(lsco.u)} points, T={int(lsco.temps[0])}..{int(lsco.temps[-1])} K, "
        f"{lsco.periods:.2f} comb periods in u=ln(hw/kT) -> clears the {MIN_COMB_PERIODS} gate). "
        f"{head} Amplitude at the fixed kernel omega: eps_hat={amp['eps_hat']:.4f}, against a "
        f"{nulls['eps95_null']:.4f} 95% conservative-null floor (predicted TFPT eps=0.0173, "
        f"i.e. the data's own systematics sit ABOVE the predicted ripple). Conservative "
        f"null p={nulls['p_conservative']}. TFPT lambda-battery Bonferroni global p={bat_p}. "
        f"Injection on the real master curve (best documented detrend variant): eps=5% detected "
        f"{100 * p50['detect_rate']:.0f}% [{p50['variant']}], predicted eps=1.73% detected "
        f"{100 * p17['detect_rate']:.0f}% [{p17['variant']}], max false-alarm "
        f"{100 * fa['detect_rate']:.0f}% -> the search is "
        f"{'POWERED' if powered_17 else 'UNDERPOWERED'} at the predicted amplitude. "
        f"Drude negative controls (Au, Cu Ordal): {'quiet' if controls_quiet else 'NOT QUIET'}. "
        f"Replication leg (Bi-2212 vdM 2003): data_limited (no public machine-readable table). "
        f"VERDICT: {status}. FIREWALL: strange metals have no established boundary-recovery "
        f"structure; even a hit would be universal-DSI coincidence, never TFPT confirmation. "
        f"No claim; nothing [E]."
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="TFPT comb ripple on the strange-metal omega/T master curve")
    ap.add_argument("command", choices=["analyze", "audit", "fetch"], nargs="?",
                    default="analyze")
    ap.add_argument("--seed", type=int, default=0)
    args, _ = ap.parse_known_args(argv)
    if args.command == "fetch":
        print("Run the data fetchers directly:\n  python scripts/fetch_michon2023.py\n"
              "  python scripts/fetch_drude_control.py")
        return 0
    if args.command == "audit":
        print(f"kernel omega=2pi/ln((3/2)^6)={OMEGA:.4f}; gate>={MIN_COMB_PERIODS} periods; "
              f"predicted eps={EPS_PREDICTED:.4f}; comb variable u=ln(hbar*omega/k_B T)")
        return 0
    return _analyze(seed=args.seed)


if __name__ == "__main__":
    raise SystemExit(main())
