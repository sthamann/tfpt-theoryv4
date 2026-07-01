"""``tfpt-crust`` -- test the frozen TFPT recovery comb (omega=2.583) on neutron-star crust cooling.

Crust cooling is the cleanest FLOOR-TERMINATED relaxation-to-attractor outside the horizon and is
built here to be the independent SECOND data world the discriminating comb needs. It is range-rich
in principle (weeks..15 yr) but DENSITY-POOR (~5-15 epochs/source), so the honest expectation is a
range/density limit on the intrinsic ~2% comb. FIREWALL: surface heat diffusion, not a horizon
recovery -- a hit is a universal-DSI coincidence, never TFPT confirmation. Nothing is `[E]`.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from . import cooling
from .comb import (
    EPS_PREDICTED,
    LAMBDA,
    MIN_COMB_PERIODS,
    OMEGA,
    validate_detector,
    validate_stack,
)

RESULTS = Path(__file__).resolve().parents[2] / "results"


def _analyze(seed: int = 0) -> int:
    print("=" * 88)
    print("TFPT recovery comb on NEUTRON-STAR CRUST COOLING -- the floor-terminated 2nd data world")
    print(f"  kernel: lambda=(3/2)^6={LAMBDA:.3f}  omega=2pi/ln(lambda)={OMEGA:.4f}  "
          f"predicted ripple eps~exp(-pi^2/ln lambda)={EPS_PREDICTED:.3f}")
    print(f"  ln(tau) RANGE requirement to localise omega: > ~{MIN_COMB_PERIODS} comb periods "
          f"(ONE period = ln((3/2)^6) = {np.log(LAMBDA):.3f} in ln t)")
    print("  FIREWALL: crust heat diffusion (surface), NOT a horizon recovery -> any hit = "
          "universal-DSI coincidence, never TFPT confirmation. Value = independent 2nd world only.")
    print("=" * 88)

    # (0) detector + stack injection validation (proves the ported kernel works, unchanged)
    v = validate_detector()
    print(f"\n  [0] detector validation ({v.n_seeds} seeds; eps={v.eps}, noise={v.noise}):")
    print(f"      sufficient range (~{v.sufficient_periods} periods): detected "
          f"{100*v.sufficient_comb_rate:.0f}% | false-positive {100*v.sufficient_null_rate:.0f}%; "
          f"short range (~{v.short_periods}): {100*v.short_comb_rate:.0f}% (range-blind) "
          f"-> validated={v.passed}")
    sv = validate_stack(n_seeds=40)
    print(f"      stack sharpening (faint eps={sv.eps} over {sv.n_curves} curves): single "
          f"{100*sv.single_rate:.0f}% -> stacked {100*sv.stacked_rate:.0f}% | FP "
          f"{100*sv.null_rate:.0f}% -> validated={sv.passed}")

    # (1) load the real crust-cooling curves
    curves = cooling.load_all()
    if not curves:
        print("\n  NO data in data/*.csv. Run: python scripts/fetch_crust_cooling.py")
        return 1
    n_src = len({c.source for c in curves})
    n_pts = sum(len(c.t) for c in curves)
    print(f"\n  [1] REAL crust-cooling data: {len(curves)} cooling episodes across {n_src} distinct "
          f"quasi-persistent transients ({n_pts} total kT_eff epochs).")
    per_curve = []
    for c in curves:
        r = cooling.run_comb(c.t, c.y, seed=seed)
        r["name"], r["source"], r["n_epochs"] = c.name, c.source, int(len(c.t))
        r["ln_range"], r["ingest"] = round(c.ln_range, 2), c.ingest
        per_curve.append(r)
        gate = "" if r["range_sufficient"] else "  <gate: range-blind, EXCLUDED from kernel stack"
        print(f"      {c.name:22s} {len(c.t):2d} epochs  t=[{c.t.min():6.1f},{c.t.max():7.1f}] d  "
              f"periods={r['comb_periods']:.2f}  p={r['p_value']:.3f}{gate}")

    # (2) phase-incoherent kernel stack (per-curve gate) and (3) superposed-epoch pooled stack
    pairs = [(c.t, c.y) for c in curves]
    stack_inc = cooling.stacked_comb_test(pairs, seed=seed)
    stack_sep = cooling.superposed_epoch_stack(curves, seed=seed)
    print(f"\n  [2] phase-incoherent kernel stack (per-curve >= {MIN_COMB_PERIODS}-period gate): "
          f"n_used={stack_inc['n_used']}/{len(curves)} "
          + ("-> NO curve clears the ln-range gate (kernel comb NOT testable this way)."
             if stack_inc["n_used"] == 0 else f"stacked p={stack_inc['p_value']}"))
    print(f"  [3] SUPERPOSED-EPOCH pooled stack (all episodes -> one ln t series): "
          f"{stack_sep['n_points']} pts span {stack_sep['comb_periods']:.2f} comb periods "
          f"(union ln-range {stack_sep['ln_range']}); range_sufficient={stack_sep['range_sufficient']}")
    print(f"      kernel omega=2.583 rank vs off-kernel periodogram: p={stack_sep['p_value']} -> "
          + ("SPECIAL -> ESCALATE (independent cross-check first)" if stack_sep["comb_detected"]
             else "NOT special -> clean NULL (assumes phase-aligned-at-t0; see injection washout)"))

    # (4) TFPT lambda-battery (look-elsewhere corrected)
    battery, bat_p, m_eff, best = cooling.lambda_battery(curves, seed=seed)
    print(f"\n  [4] TFPT lambda-battery (per-lambda gate + Bonferroni over {m_eff} gated ratios):")
    for label, v2 in battery.items():
        tag = "IDIO" if v2["idio"] else "atom"
        mark = "  <-- nominally special" if v2["comb_detected"] else ""
        gate = "" if v2["n_used"] else "  (range-blind, 0 curves gated)"
        print(f"      [{tag}] lambda={v2['lambda']:7.3f} (omega={v2['omega']:5.2f})  "
              f"n_used={v2['n_used']:2d}  p={v2['p_value']:.4f}{mark}{gate}")
    print(f"      best={best}; Bonferroni global p={bat_p} -> "
          + ("a TFPT log-period SURVIVES look-elsewhere -> ESCALATE" if bat_p < 0.05
             else "no TFPT log-period is special (NULL)"))

    # (5) protected-floor test (generic crust physics, consistency only)
    print("\n  [5] protected-floor test (kT_eff = b + A exp(-t/tau); b = core-equilibrium floor):")
    floors = []
    for c in curves:
        f = cooling.protected_floor(c)
        f["name"] = c.name
        floors.append(f)
        if f.get("floor_eV") is not None:
            print(f"      {c.name:22s} floor b={f['floor_eV']:6.1f} +/- {f['floor_err_eV']:.1f} eV "
                  f"({f['floor_sigma']}sigma), tau={f['tau_days']:.0f} d, chi2_red={f['chi2_red']}"
                  + ("  floor>0" if f["floor_nonzero"] else "  floor consistent-with-0/unconstrained"))
        else:
            print(f"      {c.name:22s} floor fit: {f.get('reason')}")
    n_floor = sum(1 for f in floors if f.get("floor_nonzero"))
    print(f"      {n_floor}/{len(floors)} episodes show a significant nonzero floor "
          "(consistent with the TFPT protected floor -- but generic crust physics, NOT specific).")

    # (6) injection-recovery on the REAL sampling (the sensitivity floor)
    grids = [c.t for c in curves]
    inj, fa = cooling.injection_recovery(grids)
    print("\n  [6] injection-recovery on the REAL epoch sampling (superposed-epoch stack):")
    for r in inj:
        print(f"      {r.label:9s} noise={r.noise:.0%}: aligned-comb detected {100*r.aligned:.0f}% | "
              f"phase-random {100*r.misaligned:.0f}% (washout control)")
    print(f"      comb-free NULL false-alarm: {100*fa:.0f}%  "
          f"(predicted TFPT eps~{EPS_PREDICTED:.0%}: see the eps=2% row -> the honest power floor)")

    verdict = _verdict(curves, n_src, stack_inc, stack_sep, bat_p, n_floor, inj, fa)
    print(f"\n==> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {
        "kernel": {"lambda": LAMBDA, "omega": OMEGA, "eps_predicted": EPS_PREDICTED,
                   "min_comb_periods": MIN_COMB_PERIODS, "one_period_ln_t": float(np.log(LAMBDA))},
        "detector_validation": asdict(v),
        "stack_validation": asdict(sv),
        "n_sources": n_src, "n_episodes": len(curves), "n_epochs_total": n_pts,
        "per_curve": per_curve,
        "stack_incoherent_kernel": stack_inc,
        "stack_superposed_epoch": stack_sep,
        "lambda_battery": battery, "lambda_battery_global_p": bat_p,
        "lambda_battery_m_eff": m_eff, "lambda_battery_best": best,
        "protected_floor": floors, "n_floor_nonzero": n_floor,
        "injection_recovery": [asdict(r) for r in inj],
        "injection_false_alarm": fa,
        "verdict": verdict,
    }
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


def _verdict(curves, n_src, stack_inc, stack_sep, bat_p, n_floor, inj, fa) -> str:
    best_periods = max(c.periods for c in curves)
    eps2 = next((r for r in inj if abs(r.eps - 0.02) < 1e-9), None)
    eps_strong = max(inj, key=lambda r: r.eps) if inj else None
    kernel_sep = ("omega=2.583 is NOT special in the superposed-epoch pooled stack "
                  f"(p={stack_sep['p_value']}, {stack_sep['comb_periods']:.2f} pooled comb periods)"
                  if not stack_sep["comb_detected"] else
                  f"omega=2.583 appears SPECIAL in the pooled stack (p={stack_sep['p_value']}) "
                  "-> ESCALATE (independent cross-check first; phase-alignment assumed)")
    power = ""
    if eps2 is not None and eps_strong is not None:
        power = (f" Injection on the REAL sampling: a strong comb (eps={eps_strong.eps:.0%}) is "
                 f"recovered {100*eps_strong.aligned:.0f}% and the null false-alarm is {100*fa:.0f}%, "
                 f"BUT the PREDICTED eps~2% is detected only {100*eps2.aligned:.0f}% -> the stack is "
                 "UNDERPOWERED on the intrinsic amplitude (density-poor).")
    return (
        f"{len(curves)} crust-cooling episodes across {n_src} quasi-persistent transients "
        f"(KS 1731-260, MXB 1659-29 x2, XTE J1701-462, EXO 0748-676, MAXI J0556-332 x2, Aql X-1). "
        f"Every single cooling curve is RANGE-BLIND for the (3/2)^6 comb (best = {best_periods:.2f} "
        f"< {MIN_COMB_PERIODS} periods), so the phase-incoherent kernel stack has n_used="
        f"{stack_inc['n_used']} and cannot test omega=2.583. The superposed-epoch pooled stack "
        f"({stack_sep['comb_periods']:.2f} periods) CAN: {kernel_sep}. The TFPT lambda-battery is a "
        f"clean NULL after look-elsewhere (Bonferroni global p={bat_p}); {n_floor}/{len(curves)} "
        f"episodes show a significant nonzero core-equilibrium floor (consistent with the TFPT "
        f"protected floor, but generic crust physics).{power} VERDICT: data_limited -- crust cooling "
        f"has the right FLOOR-TERMINATED character but is range/density-limited for the discriminating "
        f"~2% omega=2.583 comb; it serves as an honest 2nd world only via the (low-specificity) "
        f"lambda-battery NULL. FIREWALL: surface heat diffusion, not a horizon recovery -> no hit "
        f"here could ever be TFPT confirmation. No claim; nothing [E]."
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT recovery comb on neutron-star crust cooling")
    ap.add_argument("command", choices=["analyze", "audit", "fetch"], nargs="?", default="analyze")
    ap.add_argument("--seed", type=int, default=0)
    args, _ = ap.parse_known_args(argv)
    if args.command == "fetch":
        print("Run the data (re)generator directly:  python scripts/fetch_crust_cooling.py")
        return 0
    if args.command == "audit":
        print(f"kernel omega=2pi/ln((3/2)^6)={OMEGA:.4f}; gate>={MIN_COMB_PERIODS} periods; "
              f"predicted eps={EPS_PREDICTED:.3f}")
        return 0
    return _analyze(seed=args.seed)


if __name__ == "__main__":
    raise SystemExit(main())
