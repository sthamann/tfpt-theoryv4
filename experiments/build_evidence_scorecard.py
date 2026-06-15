#!/usr/bin/env python3
"""Build the central TFPT empirical evidence scorecard.

One typed row per (domain, observable) across all empirical experiments, with the
firewall typing made explicit (claim_type / bridge_type / stage) so nothing is
silently upgraded. Stage and status are restricted to fixed enums; the script fails
if any row violates them.

The values below match the current deterministic runs of each experiment
(`<experiment>/results/results.json`); keep them in sync when an experiment is re-run.
Run: ``python experiments/build_evidence_scorecard.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "evidence_scorecard.json"

STAGE_ENUM = {"prediction_of_record", "downstream_bridge", "search_target",
              "catalog_feasibility", "strain_level_test", "parked_analog"}
STATUS_ENUM = {"consistent", "hint", "tension", "null", "kill_channel",
               "data_limited", "parked"}

# domain, observable, tfpt_value, data_value, pull_sigma, claim_type, bridge_type,
# stage, source, kill_condition, status
ROWS = [
    # ---- FRB (experiments/frb-tfpt-signatures) ----
    ["FRB", "no native dispersion (FRB.01)", "A_TFPT delay = 0",
     "implied delay <<ToA precision (2 src/119 bursts)", None, "search_target", "horizon Lorentz cone",
     "search_target", "FAST FRB20121102A + FRB20201124A waterfalls",
     "a common above-precision non-plasma delay across sources", "consistent"],
    ["FRB", "echo ratios (FRB.02)", "E_{n+1}/E_n=64/729; amp 8/27",
     "no theory-channel excess (4 sources)", None, "search_target", "boundary recovery kernel",
     "search_target", "FAST 1652 + Blinkverse", "free quotient wins away from kernel", "null"],
    ["FRB", "free-quotient null (FRB.02b)", "q*=8/27 or lose to M0",
     "M0 (best q* non-kernel; LEE p>=0.31)", None, "search_target", "anti-numerology control",
     "search_target", "FAST 1652 + Blinkverse", "free q* significant at a non-kernel value", "null"],
    ["FRB", "activity-window eigenwidths (FRB.03)", "W_broad/P=8/27, W_core/P=1/27",
     "1/2 broad match, n=2<5 repeaters", None, "search_target", "boundary recovery kernel",
     "search_target", "CHIME + literature repeaters", "no match across >=5 periodic repeaters", "hint"],
    ["FRB", "PA/RM Markov spectrum (FRB.04)", "spec(T)={1,64/729,1/729}",
     "null (0/3 sources; AR(1)-drift null)", None, "search_target", "mu4/D4 boundary clock",
     "search_target", "FAST FRB20240114A pol + Blinkverse", "replicated mu4 eigenvalues", "null"],
    ["FRB", "pol-fraction quantisation (FRB.06)", "L/I,|V|/I near kernel fractions",
     "null (placebo-controlled, 0/3)", None, "search_target", "boundary recovery kernel",
     "search_target", "FAST + Blinkverse", "replicated kernel-fraction spike", "null"],
    ["FRB", "width-relaxation echo (FRB.07)", "W_{n+1}/W_n=2/3 or 1/3",
     "null (0/3 sources)", None, "search_target", "sub-burst step kernel",
     "search_target", "Blinkverse", "replicated width-step excess", "null"],
    ["FRB", "static PA mu4 classes (FRB.08)", "4 PA classes 45 deg apart",
     "null (fundamental m=2, not m=4)", None, "search_target", "mu4 angle structure",
     "search_target", "FAST FRB20240114A", "significant fundamental m=4", "null"],
    ["FRB", "recovery-clock dynamics (FRB.09)", "wall<=N_fam=3; g1/g2=2.71",
     "null (wall 0/4, accel 0/4)", None, "search_target", "resummed recovery clock (v124)",
     "search_target", "FAST 1652 + Blinkverse", "cascade wall + accelerating gaps replicated", "null"],
    # ---- CMB (experiments/cmb-birefringence-seed) ----
    ["CMB", "cosmic birefringence beta", "0.2424 deg",
     "ACT DR6 0.215+/-0.074 deg", 0.37, "prediction", "CMB EB/TB calibration",
     "prediction_of_record", "ACT DR6 (arXiv:2509.13654)",
     "systematics-controlled beta excludes 0.2424 deg at >=3 sigma", "consistent"],
    ["CMB", "baryon fraction Omega_b", "0.04894",
     "BBN D/H 0.0489+/-0.0014 (CMB-independent)", 0.04, "prediction", "BBN / CMB Omega_b h2",
     "prediction_of_record", "PDG BBN / Planck 2018", "Omega_b off 0.04894 at >=3 sigma", "consistent"],
    ["CMB", "seed line Omega_b/beta_rad=4pi-1", "11.566",
     "13.1+/-4.5 (joint, cov unmodelled)", 0.35, "prediction", "shared seed phi0",
     "prediction_of_record", "ACT beta + Planck/BBN Omega_b",
     "line broken at >=3 sigma with modelled covariance", "consistent"],
    # ---- EHT (experiments/eht-achromatic-residual) ----
    ["EHT", "achromatic dyonic intercept beta_BH(r)", "achromatic, 1/r^2, sign-flip",
     "synthetic pipeline only; no real EHT residual run yet", None, "search_target", "GRMHD/MHD weights",
     "search_target", "EHT M87*/Sgr A* polarimetry (public)",
     "residual has lambda^2 tail OR not 1/r^2 OR no E.B sign flip", "data_limited"],
    # ---- GW (experiments/gw-ringdown-echo) ----
    ["GW", "ringdown echo amplitude ratio", "A_{n+1}/A_n <= (2/3)^6",
     "catalog feasibility: stacked reach rho_echo~6.3", None, "search_target", "boundary recovery kernel",
     "catalog_feasibility", "LVK GWTC-5.0 (390 canonical; 391 raw rows)",
     "strain-level echo with ratio >>(2/3)^6 across events", "data_limited"],
    # ---- lab (experiments/lab-residuals) ----
    ["lab", "muon g-2 Delta a_mu (WP2020 dispersive)", "2.879e-9",
     "residual 2.62e-9+/-0.45", 0.58, "bridge", "HVP (dispersive)",
     "downstream_bridge", "Fermilab 2025 + WP2020", "residual incompatible with 2.879e-9", "consistent"],
    ["lab", "muon g-2 Delta a_mu (WP2025 lattice)", "2.879e-9",
     "residual 0.39e-9+/-0.65", 3.86, "bridge", "HVP (lattice)",
     "downstream_bridge", "Fermilab 2025 + arXiv:2505.21476",
     "lattice HVP consolidates and residual stays ~0", "tension"],
    ["lab", "rare kaon BR(K+ -> pi+ nu nu)", "9.45e-11",
     "NA62 2016-2024 (9.6 +1.9 -1.8)e-11", -0.08, "bridge", "short-distance QCD",
     "downstream_bridge", "NA62 arXiv:2604.12649", "BR(K+) outside [7,12]e-11", "consistent"],
    ["lab", "rare kaon BR(KL -> pi0 nu nu)", "3.33e-11",
     "KOTO 90%CL < 2.2e-9", None, "bridge", "short-distance QCD",
     "downstream_bridge", "KOTO 2024", "BR(KL) measured incompatible with 3.33e-11", "data_limited"],
    ["lab", "axion haloscope marker", "23.8 ueV (5.76 GHz)",
     "inside HAYSTAC/CAPP band, not DFSZ-excluded", None, "frontier", "dimensionful f_a",
     "search_target", "ADMX/HAYSTAC/CAPP", "DFSZ exclusion at 23.8 ueV with no signal", "data_limited"],
    ["lab", "axion relic DM.AXION.HILLTOP.01", "theta_i=170 deg",
     "Omega_a h^2 ~ 0.66 (overcloses ~5.5x)", None, "bridge", "relic density / misalignment",
     "downstream_bridge", "ftransfer/axion_relic finite-T", "overclosure without dilution", "tension"],
    ["lab", "axion relic DM.AXION.SPINE.01", "theta_i=3pi/5=108 deg (frozen)",
     "exploratory; band 0.08-0.16 frozen pre-run", None, "frontier", "relic density / misalignment",
     "search_target", "ftransfer/axion_relic (pending solve)",
     "finite-T solve outside 0.08<=Omega_a h2<=0.16", "data_limited"],
    # ---- parked ----
    ["quantum", "boundary recovery I_n ~ (64/729)^n", "64/729 per step",
     "no direct physical dataset", None, "parked", "analog only",
     "parked_analog", "quantum-recovery-analog (parked)",
     "engineered per-step recovery not at 64/729 (free-ratio control)", "parked"],
]

FIELDS = ["domain", "observable", "tfpt_value", "data_value", "pull_sigma",
          "claim_type", "bridge_type", "stage", "source", "kill_condition", "status"]


def build() -> dict:
    rows = []
    for r in ROWS:
        row = dict(zip(FIELDS, r, strict=True))
        if row["stage"] not in STAGE_ENUM:
            raise ValueError(f"bad stage {row['stage']!r} in {row['observable']!r}")
        if row["status"] not in STATUS_ENUM:
            raise ValueError(f"bad status {row['status']!r} in {row['observable']!r}")
        rows.append(row)
    by_status: dict[str, int] = {}
    by_stage: dict[str, int] = {}
    for row in rows:
        by_status[row["status"]] = by_status.get(row["status"], 0) + 1
        by_stage[row["stage"]] = by_stage.get(row["stage"], 0) + 1
    return {
        "title": "TFPT empirical evidence scorecard",
        "firewall": "search targets / downstream bridges, NOT load-bearing claims; "
                    "no row is upgraded to [E]",
        "domain_matrix": "9 active empirical domains + 1 parked analog target",
        "stage_enum": sorted(STAGE_ENUM),
        "status_enum": sorted(STATUS_ENUM),
        "n_rows": len(rows),
        "count_by_status": by_status,
        "count_by_stage": by_stage,
        "rows": rows,
    }


def main() -> int:
    card = build()
    OUT.write_text(json.dumps(card, indent=2), encoding="utf-8")
    print(f"wrote {OUT} ({card['n_rows']} rows)")
    print("by status:", card["count_by_status"])
    print("by stage :", card["count_by_stage"])
    sharp = [r for r in card["rows"] if isinstance(r["pull_sigma"], (int, float))
             and abs(r["pull_sigma"]) <= 0.5]
    print("sharpest consistencies (|pull|<=0.5 sigma):")
    for r in sharp:
        print(f"  {r['domain']:4s} {r['observable']:38s} pull={r['pull_sigma']:+.2f} "
              f"[{r['stage']}/{r['status']}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
