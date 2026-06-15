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
              "catalog_feasibility", "strain_level_test", "parked_analog",
              "not_applicable"}      # not_applicable = internal-consistency checks (no empirical stage)
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
     "1/2 broad match, n=2<5 repeaters (LOO-unstable)", None, "search_target", "boundary recovery kernel",
     "search_target", "CHIME + literature repeaters", "no match across >=5 periodic repeaters", "data_limited"],
    ["FRB", "DM(z) baryon fraction (FRB.05)", "Omega_b = 0.04894",
     "Omega_b = 0.0483 +/- 0.0072", 0.1, "search_target", "Macquart relation / baryon census",
     "search_target", "localized FRB DM(z), ApJ adb84d Table 4 + Sharma 2024",
     "localized FRB DM(z) slope excludes 0.04894 at >=3 sigma after host/IGM systematics", "consistent"],
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
     "REAL M87 2017 polarimetry ingested (4 days x 2 bands, RM~5e5); residual nulls need GRMHD imaging",
     None, "search_target", "GRMHD/MHD weights",
     "search_target", "EHT 2023-D01-01 (CyVerse 10.25739/q46m-m857), real uvfits",
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
    # (DM.AXION.SPINE.01 has a single canonical row in the P2 block below -- no duplicate)
    # ---- recovery channel (Test C; theory-internal, data-independent) ----
    ["channel", "recovery kernel as CPTP map", "Gamma(t), spec {1,(2/3)^6,(1/3)^6}",
     "CPTP + data-processing + protected QEC code verified", None, "search_target",
     "quasi-free Bogoliubov channel (v155/160/161)", "search_target",
     "recovery-channel (numerical)", "channel axiom fails (not CP / DPI violated)", "consistent"],
    ["channel", "Page curve turnover", "t_Page = (1-1/(2 sqrt2)) tau = 0.6464 tau",
     "island min-prescription turnover = 0.6466 tau", None, "prediction", "Hawking law P_H=c3/1920M^2",
     "prediction_of_record", "recovery-channel (numerical)",
     "unitary Page turnover not at t_Page", "consistent"],
    # ---- shared seed (one phi0 -> four observables) ----
    ["seed", "shared seed phi0", "phi0 = 1/(6pi)+3/(256pi^4) = 0.05317",
     "4 observables imply same phi0, chi2/dof=1.23 (dominant leg theta13, -1.80 sigma)",
     None, "prediction", "one retarded seed", "prediction_of_record",
     "seed-consistency + cmb-birefringence-seed (shared_seed)",
     "two independent seed legs >3 sigma, or one leg >5 sigma; theta13 alone >3 sigma flags "
     "PMNS theta13 as transfer-corrected", "consistent"],
    # ---- inflation (cmb-inflation-scalaron) ----
    ["CMB", "inflation n_s (Starobinsky/scalaron)", "1-2/N_star = 0.9611 (N=51.4)",
     "Planck 0.9649+/-0.0042", -0.91, "prediction", "N_star reheating input",
     "prediction_of_record", "Planck 2018 / DESI", "n_s >= 0.967 robustly", "consistent"],
    ["CMB", "inflation r (tensor ratio)", "12/N_star^2 = 0.0045",
     "BICEP/Keck < 0.036; CMB-S4 sigma 5e-4", None, "prediction", "N_star reheating input",
     "prediction_of_record", "BICEP/Keck BK18; CMB-S4", "r excluded at CMB-S4 (>5 sigma)", "consistent"],
    ["CMB", "inflation A_s (fixed N_star=51.4 point)", "1.76e-9 at N_star=51.4",
     "Planck 2.10e-9 (branch stress; record is the band, NOT the fixed point)", -11.3, "bridge",
     "N_star reheating branch", "downstream_bridge", "Planck 2018 + branch_resolver (lnB=+62)",
     "A_s incompatible at all admissible N_star in [50,60]", "tension"],
    ["CMB", "inflation A_s (profiled N_star)", "matched at N_star~56.1 (n_s=0.9644, r=0.0038)",
     "Planck 2.10e-9 (consistent when profiled; this is the record reading)", -0.1, "bridge",
     "N_star reheating bridge", "downstream_bridge", "Planck 2018 + branch_resolver",
     "A_s incompatible across the whole [50,60] band", "consistent"],
    # ---- neutrino mixing (neutrino-mixing) ----
    ["neutrino", "sin^2 theta12", "1/3 - phi0/2 = 0.306747", "NuFIT 6.0 0.307+/-0.012", -0.02,
     "prediction", "PMNS (TBM+seam)", "prediction_of_record", "NuFIT 6.0 / JUNO",
     "theta12 off 0.3067 at >3 sigma", "consistent"],
    ["neutrino", "sin^2 theta13", "phi0 e^(-5/6) = 0.0231", "NuFIT 6.0 0.02195+/-0.00058", 2.0,
     "prediction", "PMNS (seed x carrier-trace)", "prediction_of_record", "NuFIT 6.0 / Daya Bay",
     "theta13 off 0.0231 at >3 sigma (currently ~2 sigma)", "tension"],
    ["neutrino", "sin^2 theta23", "1/2 (octant open)", "NuFIT 6.0 0.470+/-0.017", 1.76,
     "prediction", "PMNS (mu-tau)", "prediction_of_record", "NuFIT 6.0",
     "theta23 far from maximal in both octants", "consistent"],
    ["CKM", "delta_CKM", "pi/3 + 3 lambda^2 = 68.65 deg", "LHCb gamma 64.6+/-2.8 deg", 1.45,
     "prediction", "CKM CP phase", "prediction_of_record", "LHCb gamma combination (canonical v88)",
     "gamma incompatible with 68.65 deg", "consistent"],
    # ---- GW v_GW=c (gw-speed-multimessenger) ----
    ["GW", "v_GW = c", "(v_GW-c)/c = 0 (single Lorentz cone)",
     "GW170817 bound [-3e-15, +7e-16]", None, "prediction", "shared causal cone",
     "prediction_of_record", "GW170817 + GRB170817A (Abbott+ 2017)",
     "measured v_GW != c", "consistent"],
    # ---- QNM ringdown ln3 (gw-ringdown-spectroscopy) ----
    ["GW", "QNM family count omega_R/T_H -> ln3", "ln 3 = ln N_fam; area quantum 4 ln3 = ln 81",
     "asymptotic regime not measured (n=0 fundamental only)", None, "search_target",
     "horizon ringdown (Hod, [C]/[P])", "search_target", "GW150914/GW250114 ringdown",
     "high-overtone omega_R/T_H != ln3", "data_limited"],
    # ---- Lambda/H0 engine (lambda-h0-engine) ----
    ["cosmo", "Lambda hierarchy rho_Lambda/M_pl^4", "(3/256pi^4) e^-2ainv = 122.948 orders",
     "measured 122.943 orders (dev 0.004 orders, NOT a pull_sigma)", None, "prediction",
     "EM fixed point alpha^-1", "prediction_of_record", "Planck Omega_Lambda + H0",
     "measured Lambda orders differ from 122.95 by >1 order", "consistent"],
    ["cosmo", "S_dS rho_Lambda = 32 pi^4", "1/(128 c3^4) = 32 pi^4 (exact)",
     "dimensionless identity", None, "prediction", "de Sitter entropy x Lambda",
     "prediction_of_record", "internal identity", "identity fails", "consistent"],
    # ---- dark-energy watchdog (P2) ----
    ["cosmo", "dark-energy equation of state w", "w = -1 (cosmological constant)",
     "DESI DR2 overlap-aware: strongest single combo 4.4 sigma (naive product 6.6 sigma is spurious)",
     None, "prediction", "Lambda = constant vacuum", "prediction_of_record",
     "dark-energy-w-watchdog (DESI DR2, overlap-aware)",
     "w != -1 at >=5 sigma in a single systematics-controlled overlap-aware combination",
     "data_limited"],
    # ---- neutrino absolute sector (P2) ----
    ["neutrino", "sum m_nu", "Sigma m_nu = 5.88e-2 eV (normal ordering)",
     "DESI+CMB upper limit ~0.07 eV", None, "prediction", "PMNS / mass scale",
     "prediction_of_record", "DESI+CMB; KATRIN", "Sigma m_nu excluded or inverted ordering", "consistent"],
    ["neutrino", "m_betabeta (0vbb)", "m_bb = 1.52e-3 eV (normal ordering)",
     "LEGEND/nEXO sensitivity ~10-20 meV (not yet reached)", None, "prediction", "Majorana mass",
     "prediction_of_record", "LEGEND-1000 / nEXO", "a 0vbb signal incompatible with 1.5 meV NO", "data_limited"],
    ["neutrino", "delta_nu_CP", "240 deg (4 pi/3)", "NuFIT 6.0 ~177-270 deg (weak)", None,
     "prediction", "PMNS CP phase", "prediction_of_record", "T2K/NOvA/DUNE/HyperK",
     "delta_nu_CP excludes 240 deg at >=3 sigma", "data_limited"],
    # ---- kaon flavor-bridge ratio (P2) ----
    ["CKM", "rare kaon ratio R_K = KL/K+", "3.33/9.45 = 0.35238",
     "geometry consistent (delta_CKM +1.45s, Jarlskog -0.07s, K+ -0.08s); KOTO KL not at SM reach",
     None, "bridge", "short-distance QCD",
     "downstream_bridge", "rare-kaon-bridge (NA62 + LHCb + PDG; KOTO future)",
     "measured R_K incompatible with 0.3524", "data_limited"],
    # ---- EDM null suite (P2) ----
    ["lab", "neutron EDM (theta_eff=0)", "d_n ~ 0 (RP + sheet involution)",
     "PSI nEDM |d_n| < 1.8e-26 e.cm", None, "prediction", "strong-CP / structure",
     "prediction_of_record", "PSI nEDM / SNS", "a robust EDM incompatible with theta_eff=0", "consistent"],
    ["lab", "electron EDM (theta_eff=0)", "d_e ~ 0",
     "JILA/ACME |d_e| < 4.1e-30 e.cm", None, "prediction", "strong-CP / structure",
     "prediction_of_record", "JILA HfF+ / ACME", "a robust e-EDM incompatible with theta_eff=0", "consistent"],
    # ---- heavy F_transfer solvers (P2; run in ftransfer/) ----
    ["lab", "axion relic DM.AXION.SPINE.01 (theta_i=3pi/5)", "Omega_a h^2 in [0.08,0.16] (frozen band)",
     "finite-T solve: Omega_a h^2 = 0.125 (robust [0.090,0.151] over chi(T) n=7..9, g_* +/-10%)",
     None, "frontier", "relic density / misalignment",
     "downstream_bridge", "ftransfer/axion_relic/spine_finiteT_solve.py",
     "finite-T Omega_a h^2 outside 0.08-0.16 at theta_i=3pi/5", "consistent"],
    ["lab", "leptogenesis eta_B (scalaron-decuple)", "M1=M_scal phi0^2/A_Lambda, A_Lambda=10",
     "Boltzmann solve pending in ftransfer/leptogenesis_boltzmann", None, "bridge", "leptogenesis interface",
     "downstream_bridge", "ftransfer/leptogenesis_boltzmann", "flavored Boltzmann misses eta_B=6.1e-10 by >3x",
     "data_limited"],
    ["EW", "Higgs near-criticality", "lambda(M_Pl)~0, beta_lambda(M_Pl)~0 (double-critical)",
     "Buttazzo2013 fit: lambda(M_Pl)=-0.0143+/-0.0057, beta_lambda=+1.9e-4 (metastable 2.5 sigma)",
     None, "bridge", "seam free-field boundary",
     "downstream_bridge", "higgs-criticality (Buttazzo 2013 NNLO fit)",
     "RGE pull off the double-critical surface at >5 sigma", "consistent"],
    # ---- internal-consistency checks (recovery channel / Page curve) ----
    # ---- parked ----
    ["quantum", "boundary recovery I_n ~ (64/729)^n", "64/729 per step",
     "no direct physical dataset", None, "parked", "analog only",
     "parked_analog", "quantum-recovery-analog (parked)",
     "engineered per-step recovery not at 64/729 (free-ratio control)", "parked"],
]

FIELDS = ["domain", "observable", "tfpt_value", "data_value", "pull_sigma",
          "claim_type", "bridge_type", "stage", "source", "kill_condition", "status"]

EVIDENCE_CLASS_ENUM = {"external_data", "internal_consistency", "downstream_bridge",
                       "search_target", "parked"}
README = Path(__file__).resolve().parent / "README.md"

# --- metadata enrichment (so correlated seed legs / internal checks are not counted
#     as independent external hits) ----------------------------------------------------
_PHI0 = ("beta", "omega_b", "seed", "theta12", "theta13", "cabibbo", "baryon fraction")
_ALPHA = ("lambda hierarchy", "s_ds", "rho_lambda")
_WEAK = ("omega_b", "lambda hierarchy", "s_ds", "v_gw", "rho_lambda", "dark-energy", "baryon")
_NEAR = ("beta", "theta12", "theta13", "inflation n_s", "inflation r", "eht", "kaon",
         "g-2", "dark-energy", "sum m_nu", "shared seed")
_LONG = ("qnm", "m_betabeta", "page curve", "recovery kernel")


# Per-row overrides (keyed by an observable substring): set independence_group / stage /
# alternative_group / watch flags / add composite-row fields the default rules cannot infer.
#
# alternative_group: rows that are NOT independent evidence but alternative interpretation
# bases of the SAME underlying question (so "consistent" and "tension" from one theme are
# never silently double-counted).
OVERRIDES: dict[str, dict] = {
    "achromatic dyonic intercept": {"independence_group": "c3_topform_horizon"},
    "recovery kernel as CPTP map": {"stage": "not_applicable"},
    "Page curve turnover": {"stage": "not_applicable"},
    "S_dS rho_Lambda": {"stage": "not_applicable"},          # algebraic identity, not a measurement
    "shared seed phi0": {"chi2_dof": 1.23, "max_leg_pull_sigma": 2.0,
                         "dominant_leg": "theta13", "dominant_chi2_fraction": 0.88},
    "Lambda hierarchy": {"log_order_deviation": 0.004},
    # --- alternative interpretation bases (one theme, several readings) ---
    "inflation A_s (fixed N_star=51.4 point)": {"alternative_group": "Nstar_branch"},
    "inflation A_s (profiled N_star)": {"alternative_group": "Nstar_branch"},
    "muon g-2 Delta a_mu (WP2020 dispersive)": {"alternative_group": "HVP_baseline"},
    "muon g-2 Delta a_mu (WP2025 lattice)": {"alternative_group": "HVP_baseline"},
    "axion haloscope marker": {"alternative_group": "axion_branch"},
    "AXION.HILLTOP": {"alternative_group": "axion_branch"},
    "AXION.SPINE": {"alternative_group": "axion_branch"},
    # --- dark energy: sharpest non-red channel -> explicit watchdog flag ---
    "dark-energy equation of state w": {"watch_flag": True, "watch_level": "high"},
    # --- Higgs near-criticality: show the two-axis pull, not just a green label ---
    "Higgs near-criticality": {"lambda_pull_sigma": 2.5, "beta_lambda_pull_sigma": "near_zero",
                               "status_note": "near critical; exact double-critical surface "
                                              "mildly stressed (M_t-dominated)"},
}


def _evidence_class(row: dict) -> str:
    if row["stage"] == "parked_analog":
        return "parked"
    src = row["source"].lower()
    if "(numerical)" in src or "internal identity" in src:
        return "internal_consistency"
    if row["stage"] == "downstream_bridge":
        return "downstream_bridge"
    if row["stage"] == "search_target":
        return "search_target"
    return "external_data"


def _enrich(row: dict) -> dict:
    o = row["observable"].lower()
    ec = _evidence_class(row)
    if any(k in o for k in _PHI0):
        grp = "phi0_seed"
    elif any(k in o for k in _ALPHA):
        grp = "alpha_em"
    elif "inflation" in o:
        grp = "N_star_reheating"
    else:
        grp = "independent"
    if ec == "internal_consistency":
        disc = "internal"
    elif any(k in o for k in _WEAK):
        disc = "weak"
    else:
        disc = "medium"
    horizon = ("long_term" if any(k in o for k in _LONG)
               else "near_term" if any(k in o for k in _NEAR) else "mid_term")
    # do NOT overwrite anything an OVERRIDE already set (e.g. independence_group)
    row.setdefault("independence_group", grp)
    row.setdefault("discriminative_power", disc)
    row.setdefault("decision_horizon", horizon)
    row.setdefault("evidence_class", ec)
    row.setdefault("hint_flag", "FRB.03" in row["observable"])
    row.setdefault("alternative_group", None)     # not an alternative-interpretation base
    row.setdefault("watch_flag", False)           # high-priority non-red channel?
    return row


def build() -> dict:
    rows = []
    for r in ROWS:
        row = dict(zip(FIELDS, r, strict=True))
        for key, ov in OVERRIDES.items():       # apply per-row overrides first
            if key in row["observable"]:
                row.update(ov)
        if row["stage"] not in STAGE_ENUM:
            raise ValueError(f"bad stage {row['stage']!r} in {row['observable']!r}")
        if row["status"] not in STATUS_ENUM:
            raise ValueError(f"bad status {row['status']!r} in {row['observable']!r}")
        row = _enrich(row)
        if row["evidence_class"] not in EVIDENCE_CLASS_ENUM:
            raise ValueError(f"bad evidence_class in {row['observable']!r}")
        rows.append(row)

    def _tally(key: str) -> dict[str, int]:
        out: dict[str, int] = {}
        for row in rows:
            if row[key] is None:
                continue
            out[row[key]] = out.get(row[key], 0) + 1
        return out

    return {
        "title": "TFPT empirical evidence scorecard",
        "firewall": "search targets / downstream bridges, NOT load-bearing claims; "
                    "no row is upgraded to [E]",
        "domain_matrix": "9 active empirical search domains + sharp prediction-of-record "
                         "channels + internal-consistency checks + 1 parked analog target",
        "stage_enum": sorted(STAGE_ENUM),
        "status_enum": sorted(STATUS_ENUM),
        "evidence_class_enum": sorted(EVIDENCE_CLASS_ENUM),
        "n_rows": len(rows),
        "count_by_status": _tally("status"),
        "count_by_stage": _tally("stage"),
        "count_by_evidence_class": _tally("evidence_class"),
        "count_by_independence_group": _tally("independence_group"),
        "count_by_alternative_group": _tally("alternative_group"),
        "n_watch_flag": sum(1 for r in rows if r.get("watch_flag")),
        "rows": rows,
    }


def _readme_stats_block(card: dict) -> str:
    """The auto-generated stats paragraph (single source = the scorecard JSON)."""
    st = card["count_by_status"]
    ec = card["count_by_evidence_class"]
    ig = card["count_by_independence_group"]
    ag = card["count_by_alternative_group"]
    order = ["consistent", "hint", "tension", "null", "data_limited", "kill_channel", "parked"]
    status_str = ", ".join(f"{st[k]} {k}" for k in order if k in st)
    ec_str = ", ".join(f"{ec[k]} {k}" for k in sorted(ec))
    ig_str = ", ".join(f"{ig[k]} {k}" for k in sorted(ig))
    ag_str = ", ".join(f"{ag[k]} {k}" for k in sorted(ag))
    return (f"<!-- SCORECARD_STATS:START (generated by build_evidence_scorecard.py; do not edit) -->\n"
            f"**Scorecard (auto-generated from `evidence_scorecard.json`): {card['n_rows']} "
            f"Zeilen — {status_str}.**\n\n"
            f"- nach `evidence_class`: {ec_str}\n"
            f"- nach `independence_group`: {ig_str}\n"
            f"- `alternative_group` (eine Frage, mehrere Lesarten — *nicht* doppelt zählen): {ag_str}\n"
            f"- `watch_flag`: {card['n_watch_flag']} (schärfster nicht-roter Kanal: dunkle Energie `w`)\n"
            f"- _Korrelierte `phi0_seed`-Beine, `alternative_group`-Lesarten und "
            f"`internal_consistency`-Checks zählen NICHT als unabhängige externe Treffer._\n"
            f"<!-- SCORECARD_STATS:END -->")


def _update_readme(card: dict) -> bool:
    if not README.exists():
        return False
    text = README.read_text(encoding="utf-8")
    start = "<!-- SCORECARD_STATS:START"
    end = "<!-- SCORECARD_STATS:END -->"
    block = _readme_stats_block(card)
    if start in text and end in text:
        pre = text[:text.index(start)]
        post = text[text.index(end) + len(end):]
        README.write_text(pre + block + post, encoding="utf-8")
        return True
    return False


def main() -> int:
    card = build()
    OUT.write_text(json.dumps(card, indent=2), encoding="utf-8")
    print(f"wrote {OUT} ({card['n_rows']} rows)")
    print("by status:", card["count_by_status"])
    print("by stage :", card["count_by_stage"])
    print("by evidence_class:", card["count_by_evidence_class"])
    print("by independence_group:", card["count_by_independence_group"])
    print("README stats block updated:" , _update_readme(card))
    sharp = [r for r in card["rows"] if isinstance(r["pull_sigma"], (int, float))
             and abs(r["pull_sigma"]) <= 0.5]
    print("sharpest consistencies (|pull|<=0.5 sigma):")
    for r in sharp:
        print(f"  {r['domain']:4s} {r['observable']:38s} pull={r['pull_sigma']:+.2f} "
              f"[{r['stage']}/{r['status']}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
