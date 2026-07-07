"""``tfpt-kc`` -- the three FRB kernel-COUPLING axes (KC.01/02/03) on committed catalogs.

KC.01 joint energy-time tooth (the 2D ladder coupling; forced by the frozen kernel)
KC.02 circular-polarization handedness alternation (Z2 deck reading; exploratory)
KC.03 log-periodic decoration of the burst-energy distribution (size-space DSI)
KC.05/KC.06 operator-proxy tests (mu4 block leakage + multivariate S2a spectrum)

Preregistered in hypotheses/kernel_couplings_v1.yaml BEFORE any statistic ran.
Firewall: search targets, never load-bearing; hits are escalate-only.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from . import energy_dsi, helix, joint_tooth, operator_proxy, vsign
from .data import load_li2021, load_pol_v5, load_zhang2023

RESULTS = Path(__file__).resolve().parents[2] / "results"


def main(argv: list[str] | None = None) -> int:
    print("=" * 88)
    print("FRB kernel couplings KC.01-03 (prereg kernel_couplings_v1.yaml, seed 0)")
    print("=" * 88)

    li = load_li2021()
    zh = load_zhang2023()
    pol = load_pol_v5()

    out: dict = {"prereg": "hypotheses/kernel_couplings_v1.yaml", "axes": {}}

    print("\n[KC.01] joint energy-time tooth (2D ladder coupling)")
    kc01 = []
    for b in (li, zh):
        r = joint_tooth.run(b)
        kc01.append(asdict(r))
        print(f"  {r.source}: pairs={r.n_pairs} time-tooth={r.n_time_tooth} "
              f"joint={r.joint_hits} (null {r.null_mean:.1f}, enr {r.enrichment}, "
              f"p={r.p_value}); placebo={r.placebo_max_hits}, "
              f"free-q beats {r.free_q_beat_frac:.0%}")
        print(f"    -> {r.verdict}")
    out["axes"]["KC.01_joint_tooth"] = kc01

    print("\n[KC.02] V-handedness alternation (signed DOC; deck-visible observable)")
    r2 = vsign.run(pol)
    out["axes"]["KC.02_vsign"] = asdict(r2)
    print(f"  {r2.source}: significant={r2.n_significant} pairs={r2.n_pairs} "
          f"alternation={r2.alternation} (null {r2.null_mean}, p={r2.p_value}); "
          f"net handedness={r2.net_handedness}; tooth pairs={r2.n_tooth_pairs} "
          f"(alt={r2.tooth_alternation}, p={r2.tooth_p})")
    print(f"    -> {r2.verdict}")

    print("\n[KC.04] mu4 phase-time helix (frozen omega, q in {1,2}; drift-robust nulls)")
    r4 = helix.run(pol, pol.pa_deg, pol.li_pct)
    out["axes"]["KC.04_phase_helix"] = asdict(r4)
    print(f"  {r4.source}: sessions={r4.n_sessions} pairs={r4.n_pairs}")
    for qk, d in r4.per_q.items():
        print(f"    {qk}: R={d['R']} p_perm={d['p_perm']} p_shift={d['p_shift']} "
              f"p_rank={d['p_offkernel_rank']} detected={d['detected']}")
    print(f"    -> {r4.verdict}")

    print("\n[KC.05/KC.06] non-tooth operator proxies (mu4 block leakage + S2a spectrum)")
    r5 = operator_proxy.run(pol)
    out["axes"]["KC.05_mu4_block_proxy"] = asdict(r5.mu4_block)
    out["axes"]["KC.06_multivariate_spectrum"] = asdict(r5.multivariate_spectrum)
    print(f"  KC.05 {r5.mu4_block.source}: pairs={r5.mu4_block.n_pairs} "
          f"C4 off={r5.mu4_block.c4_off_fraction} "
          f"(shuffle med {r5.mu4_block.shuffle_median}, p_low={r5.mu4_block.p_low}); "
          f"Z3 off={r5.mu4_block.z3_off_fraction}, generic4 med={r5.mu4_block.generic4_median}")
    print(f"    -> {r5.mu4_block.verdict}")
    print(f"  KC.06 {r5.multivariate_spectrum.source}: pairs={r5.multivariate_spectrum.n_pairs} "
          f"eig={r5.multivariate_spectrum.eig_abs_norm} "
          f"dist={r5.multivariate_spectrum.distance_to_target} "
          f"(shuffle med {r5.multivariate_spectrum.shuffle_median_distance}, "
          f"p_close={r5.multivariate_spectrum.p_close})")
    print(f"    -> {r5.multivariate_spectrum.verdict}")

    print("\n[KC.03] energy-distribution DSI (size-space comb, 3-null battery)")
    kc03 = []
    for b in (li, zh):
        r = energy_dsi.run(b)
        kc03.append(asdict(r))
        print(f"  {r.source}: n={r.n_bursts} lnE-range={r.ln_e_range} "
              f"gated={r.n_gated}/12 GMM k={r.gmm_components} -> best {r.best_label} "
              f"p={r.best_p}, Bonferroni global p={r.bonferroni_global_p}")
        print(f"    -> {r.verdict}")
    out["axes"]["KC.03_energy_dsi"] = kc03

    verdicts = ([r["verdict"] for r in kc01] + [r2.verdict, r4.verdict,
                r5.mu4_block.verdict, r5.multivariate_spectrum.verdict]
                + [r["verdict"] for r in kc03])
    n_null = sum(v.startswith("NULL") for v in verdicts)
    out["verdict"] = (
        f"{n_null}/{len(verdicts)} axis-runs NULL. KC.01 tests the FORCED 2D ladder "
        f"coupling (energy x time) that all previous marginal tests skipped; KC.02 the "
        f"only deck-VISIBLE polarization observable (signed V) after FRB.04/06/08 were "
        f"deck-blind by construction; KC.03 the size-space DSI with the PG.01 "
        f"population-null discipline; KC.04 the mu4 phase-time helix at the frozen "
        f"omega (drift-robust circular-shift null); KC.05/KC.06 the new non-tooth "
        f"operator proxies (mu4 block leakage and S2a multivariate spectrum). Firewall: search targets, "
        f"escalate-only, never TFPT confirmation.")
    print(f"\n==> {out['verdict']}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
