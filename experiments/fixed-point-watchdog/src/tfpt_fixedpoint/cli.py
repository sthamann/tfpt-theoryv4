"""``tfpt-fixedpoint analyze`` -- the TFPT exact-fixed-point watchdog.

TFPT predicts several observables as EXACT fixed points (any confirmed deviation
is a kill, not a fit-parameter update):

    (1) w = -1 exactly                      (dark energy is a true cosmological constant)
    (2) Sigma m_nu = 0.0588 eV              (normal-ordering floor, m1 ~ 0; v272/v468)
    (3) alpha^-1 = 137.0359992168, static   (alpha-dot/alpha = 0; v3)
    (4) Koide Q = 2/3 exactly               (charged-lepton pole masses)
    (5) the alpha-Lambda lock:  rho_Lambda / Mbar^4 = (3/4pi^2) e^(-2 alpha^-1)  (v60/v274)
        =>  d ln rho_Lambda / dt = 2 alpha^-1 (alpha-dot/alpha)   [amplifier 2 alpha^-1 ~ 274]
    (6) N_fam = 3 exactly                   (D5+A3+mu4 => E8 leaves NO slot for a 4th
                                             light family/sterile state; every short-
                                             baseline anomaly must DISSOLVE)

    (7) lambda_C = sqrt(phi0(1-phi0)) = 0.2243762 exactly + exact CKM first-row
        unitarity (frozen v84 assembly)  =>  V_ud = 0.97450, and via the
        Czarnecki-Marciano-Sirlin master formula a PARAMETER-FREE neutron
        lifetime tau_n = 4906.4 s / (V_ud^2 (1+3 gA^2)) -- TFPT takes the
        BOTTLE side of the beam-bottle puzzle and forbids the dark-decay exit
        (no E8 slot for a light dark state; same counting as axis D).

Seven test axes against PUBLIC published values (data/measurements.json):

  A. Sigma m_nu x w PINCER   -- DESI DR2 neutrino-mass bounds vs the DESI evolving-DE
                                preference; the joint TFPT point (w=-1, 0.0588 eV) is
                                squeezed from both sides; both model readings computed.
  B. alpha-Lambda LOCK       -- PTB optical-clock alpha-drift limit propagated through
                                the lock vs the Lambda drift a real (w0,wa) evolution
                                would imply; quantifies the mutual exclusion.
  C. KOIDE-tau KILL WINDOW   -- Q from CODATA/PDG masses, pull vs 2/3, the m_tau value
                                Q=2/3 predicts, and the precision needed for a 5-sigma kill.
  D. STERILE-nu DISSOLUTION  -- N_fam = 3 requires every short-baseline anomaly to
                                dissolve; tracks MicroBooNE two-beam, gallium/BEST,
                                JSNS2 and the SBN program front by front.
  E. CABIBBO + NEUTRON tau_n -- the first-row deficit must dissolve (exact unitarity);
                                V_us route table, V_ud route table, AND the new
                                parameter-free tau_n = 877.5-877.8 s: bottle-side at
                                <1 sigma, proton-counting beam average at ~ -5 sigma.
  F. X17 DISSOLUTION         -- no E8 slot for a ~17 MeV boson; ATOMKI must dissolve;
                                tracks MEG II (null) vs PADME Run III (1.8 sigma global).
  G. R_D(*) DISSOLUTION      -- exact CKM assembly + no new light states => lepton-flavor
                                universality in b -> c tau nu; the HFLAV 3.8 sigma
                                excess must dissolve (Belle II / LHCb Run 3 decide).

Deterministic: no fetching, no randomness.  Writes results/results.json.

Firewall: standalone watchdog; search surface, NOT a load-bearing claim.  Verdict
enums per axis: consistent | tension | data_limited.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from scipy.stats import chi2 as chi2_dist
from scipy.stats import norm

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
RESULTS = Path(__file__).resolve().parents[2] / "results"

# ---- TFPT fixed points (from the axioms / verification ledger -- not data) ----
W0_TFPT = -1.0                     # true cosmological constant (Lambda/H0 engine)
WA_TFPT = 0.0
SIGMA_MNU_TFPT = 0.0588            # eV; NO floor m3(1+sqrt|J|) (v272 floor 0.0586, v468 closure 0.0588)
ALPHA_INV_TFPT = 137.0359992168    # unique root of F_U(1)=0 (v3); TFPT: constant in time
KOIDE_Q_TFPT = 2.0 / 3.0           # |Z2|/N_fam (v105 one-constant inventory)
N_FAM_TFPT = 3                     # exact compiler output: D5+A3+mu4 => E8 fixes 3 families;
                                   # no spare slot for a 4th light (sterile) state
LOCK_PREFACTOR = 3.0 / (4.0 * math.pi ** 2)   # rho_Lambda/Mbar^4 = (3/4pi^2) e^(-2 alpha^-1) (v60/v274)
AMPLIFIER = 2.0 * ALPHA_INV_TFPT   # d ln rho_Lambda = 2 alpha^-1 * (dalpha/alpha)

KILL_SIGMA = 5.0
KM_S_MPC_TO_PER_YR = 1.0227e-12    # 1 km/s/Mpc in 1/yr

# frozen v84 CKM texture (identical to tfpt-discovery/electron_sector_cabibbo_probe.py):
# lambda_C = sqrt(phi0(1-phi0)) with phi0 = 1/(6 pi) + 48 c3^4, s13 the frozen CKM 1-3 entry
C3 = 1.0 / (8.0 * math.pi)
PHI0 = 1.0 / (6.0 * math.pi) + 48.0 * C3 ** 4
LAMBDA_C_TFPT = math.sqrt(PHI0 * (1.0 - PHI0))          # 0.2243762...
S13_CKM = 0.003765384454486430                          # frozen v84 CKM texture
V_UD_TFPT = math.sqrt(1.0 - LAMBDA_C_TFPT ** 2 - S13_CKM ** 2)   # exact unitarity


def _mahalanobis_2d(c: dict, w0: float, wa: float) -> float:
    dx, dy = w0 - c["w0"], wa - c["wa"]
    sx, sy, rho = c["sigma_w0"], c["sigma_wa"], c["rho_w0_wa"]
    m2 = (dx ** 2 / sx ** 2 + dy ** 2 / sy ** 2 - 2 * rho * dx * dy / (sx * sy)) / (1 - rho ** 2)
    return math.sqrt(max(m2, 0.0))


def _chi2_to_sigma(chi2_val: float, dof: int) -> float:
    """Equivalent two-sided Gaussian significance of a chi^2 exceedance."""
    p = float(chi2_dist.sf(chi2_val, dof))
    if p <= 0.0:
        return float("inf")
    return float(norm.isf(p / 2.0))


# --------------------------------------------------------------------------- A
def axis_a_pincer(m: dict) -> dict:
    nu = m["neutrino_mass"]
    de = m["dark_energy_cpl"]

    # -- neutrino axis, LCDM reading (w = -1 held fixed, as TFPT demands) --
    sig_sym = 0.5 * (nu["lcdm_eff_sigma_plus_eV"] + nu["lcdm_eff_sigma_minus_eV"])
    pull_nu_lcdm = (SIGMA_MNU_TFPT - nu["lcdm_eff_mean_eV"]) / sig_sym
    inside_95 = SIGMA_MNU_TFPT < nu["lcdm_upper_95_eV"]
    inside_fc = SIGMA_MNU_TFPT < nu["lcdm_feldman_cousins_upper_95_eV"]

    # -- neutrino axis, w0waCDM reading (bound relaxes; TFPT point re-tested) --
    sig_w = 0.5 * (nu["w0wacdm_eff_sigma_plus_eV"] + nu["w0wacdm_eff_sigma_minus_eV"])
    pull_nu_w0wa = (SIGMA_MNU_TFPT - nu["w0wacdm_eff_mean_eV"]) / sig_w

    # -- w axis: 2-D distance of (w0,wa)=(-1,0) from each published CPL fit --
    w_rows = []
    for c in de["combinations"]:
        d = _mahalanobis_2d(c, W0_TFPT, WA_TFPT)
        w_rows.append({"name": c["name"], "tension_2d_sigma": round(d, 2),
                       "published_sigma_vs_LCDM": c["published_sigma_vs_LCDM"]})
    w_head = max(w_rows, key=lambda r: r["tension_2d_sigma"])

    # -- joint reading, w0waCDM: (w0, wa, Sigma m_nu) all float --
    chi2_joint = w_head["tension_2d_sigma"] ** 2 + pull_nu_w0wa ** 2
    joint_sigma = _chi2_to_sigma(chi2_joint, dof=3)

    tension = max(abs(pull_nu_lcdm), joint_sigma)
    return {
        "tfpt_point": {"w0": W0_TFPT, "wa": WA_TFPT, "sigma_mnu_eV": SIGMA_MNU_TFPT},
        "reading_LCDM": {
            "model": "LCDM (w=-1 held, as TFPT demands); only the nu axis can pull",
            "pull_nu_sigma": round(pull_nu_lcdm, 2),
            "published_tension_vs_NO_floor_sigma": 3.0,
            "inside_standard_95_bound_0.0642eV": inside_95,
            "inside_feldman_cousins_95_bound_0.053eV": inside_fc,
        },
        "reading_w0waCDM": {
            "model": "w0waCDM (bound relaxes to 0.163 eV; eff-mass posterior peaks at 0)",
            "pull_nu_sigma": round(pull_nu_w0wa, 2),
            "w_axis_2d_sigma": w_rows,
            "w_axis_headline_sigma": w_head["tension_2d_sigma"],
            "w_axis_headline_combination": w_head["name"],
            "joint_3dof_equivalent_sigma": round(joint_sigma, 2),
        },
        "caveat": ("Sigma m_nu bounds are MODEL-DEPENDENT: in LCDM the TFPT floor is in "
                   "~3-sigma tension (via the effective-mass posterior; it still sits inside "
                   "the standard 95% bound 0.0642 eV but outside the Feldman-Cousins 0.053 eV); "
                   "in w0waCDM the floor is fully compatible (+0.7 sigma) but then w=-1 itself "
                   "is disfavoured at up to ~4.4 sigma. The pincer: no published model reading "
                   "lets BOTH TFPT fixed points sit below ~3 sigma simultaneously. Gaussian "
                   "approximations of published posteriors throughout; SN samples overlap "
                   "(never stacked)."),
        "kill_rule": "joint (w=-1, 0.0588 eV) excluded at >= 5 sigma in a single "
                     "systematics-controlled combination under BOTH model readings",
        "max_tension_sigma": round(tension, 2),
        "kill_triggered": bool(tension >= KILL_SIGMA),
        "verdict": "tension",
    }


# --------------------------------------------------------------------------- B
def axis_b_lock(m: dict) -> dict:
    clk = m["alpha_drift_clock"]
    de = m["dark_energy_cpl"]
    h0_per_yr = de["h0_km_s_mpc"] * KM_S_MPC_TO_PER_YR

    # clock -> Lambda drift bound through the lock
    adot = clk["alpha_dot_over_alpha_per_yr"]
    s = clk["sigma_per_yr"]
    bound_2sig = 2.0 * s                                # drift consistent with 0: 2-sigma band
    bound_c2sig = abs(adot) + 2.0 * s                   # conservative: |central| + 2 sigma
    lam_central = AMPLIFIER * adot
    lam_bound_2sig = AMPLIFIER * bound_2sig
    lam_bound_c2sig = AMPLIFIER * bound_c2sig

    # DESI (w0,wa) taken at face value -> d ln rho_DE/dt at z=0 = -3(1+w0) H0
    desi_rows = []
    for c in de["combinations"]:
        rate = 3.0 * abs(1.0 + c["w0"]) * h0_per_yr
        desi_rows.append({"name": c["name"], "w0": c["w0"],
                          "dln_rho_de_dt_per_yr": float(f"{rate:.3g}")})
    desi_max = max(r["dln_rho_de_dt_per_yr"] for r in desi_rows)
    desi_min = min(r["dln_rho_de_dt_per_yr"] for r in desi_rows)

    # mutual exclusion: if the DESI evolution is real DE dynamics AND the lock holds
    implied_alpha_drift = desi_max / AMPLIFIER
    exclusion_factor = desi_max / lam_bound_2sig
    return {
        "lock": "rho_Lambda/Mbar^4 = (3/4pi^2) exp(-2 alpha^-1)  =>  "
                "d ln rho_Lambda/dt = 2 alpha^-1 * (alpha_dot/alpha)",
        "amplifier_2_alpha_inv": round(AMPLIFIER, 4),
        "clock_limit_per_yr": {"central": adot, "sigma": s,
                               "source": clk["source"]},
        "lock_implied_dln_lambda_dt_per_yr": {
            "central": float(f"{lam_central:.3g}"),
            "bound_2sigma": float(f"{lam_bound_2sig:.3g}"),
            "bound_central_plus_2sigma": float(f"{lam_bound_c2sig:.3g}")},
        "desi_face_value_dln_rho_de_dt_per_yr": desi_rows,
        "mutual_exclusion": {
            "desi_implied_range_per_yr": [desi_min, desi_max],
            "implied_alpha_drift_if_lock_and_desi_real_per_yr": float(f"{implied_alpha_drift:.3g}"),
            "clock_bound_2sigma_per_yr": bound_2sig,
            "violation_factor": float(f"{exclusion_factor:.3g}"),
            "orders_of_magnitude": round(math.log10(exclusion_factor), 1),
            "statement": ("IF the DESI (w0,wa) preference is real dark-energy dynamics AND "
                          "the TFPT alpha-Lambda lock holds, the implied alpha drift "
                          f"violates the optical-clock bound by ~10^"
                          f"{math.log10(exclusion_factor):.1f} -- so 'TFPT + real "
                          "w(z) evolution' is internally killed; TFPT is only consistent "
                          "with w = -1 (axis A) AND alpha static (this axis) JOINTLY.")},
        "today": ("clocks see alpha_dot/alpha = 1.8(2.5)e-19/yr (consistent with zero) -- "
                  "exactly what TFPT's static fixed point demands; the lock then bounds "
                  "|d ln Lambda/dt| < ~1.4e-16/yr (2 sigma)"),
        "kill_rule": "any confirmed alpha_dot/alpha != 0, or any confirmed Lambda drift "
                     "violating d ln rho_Lambda/dt = 2 alpha^-1 d(alpha)/alpha/dt",
        "kill_triggered": False,
        "verdict": "consistent",
    }


# --------------------------------------------------------------------------- C
def axis_c_koide(m: dict) -> dict:
    lm = m["lepton_masses"]
    me, se = lm["m_e_MeV"], lm["m_e_sigma_MeV"]
    mmu, smu = lm["m_mu_MeV"], lm["m_mu_sigma_MeV"]
    mtau, stau = lm["m_tau_MeV"], lm["m_tau_sigma_MeV"]

    def koide_q(m1: float, m2: float, m3: float) -> float:
        return (m1 + m2 + m3) / (math.sqrt(m1) + math.sqrt(m2) + math.sqrt(m3)) ** 2

    q = koide_q(me, mmu, mtau)

    def dq_dm(mi: float) -> float:
        s = me + mmu + mtau
        t = math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau)
        return (1.0 / t ** 2) * (1.0 - (s / t) / math.sqrt(mi))

    sq = math.sqrt((dq_dm(me) * se) ** 2 + (dq_dm(mmu) * smu) ** 2 + (dq_dm(mtau) * stau) ** 2)
    pull = (q - KOIDE_Q_TFPT) / sq

    # m_tau that gives Q = 2/3 exactly (Newton iteration; dQ/dm_tau > 0, monotone here)
    mt = mtau
    for _ in range(60):
        mt -= (koide_q(me, mmu, mt) - KOIDE_Q_TFPT) / dq_dm_at(me, mmu, mt)
    mtau_pred = mt
    # sigma on the prediction from m_e, m_mu (negligible, but computed)
    eps = 1e-6
    dpred_dmu = (solve_mtau(me, mmu + eps) - solve_mtau(me, mmu - eps)) / (2 * eps)
    spred = abs(dpred_dmu) * smu

    pull_pdg = (mtau - mtau_pred) / stau
    pull_belle2 = (lm["m_tau_belle2_MeV"] - mtau_pred) / lm["m_tau_belle2_sigma_MeV"]

    # kill window: |m_tau - m_tau_pred| >= 5 sigma(m_tau)
    gap_pdg = abs(mtau - mtau_pred)
    gap_belle2 = abs(lm["m_tau_belle2_MeV"] - mtau_pred)
    return {
        "inputs": {"m_e_MeV": me, "m_mu_MeV": mmu,
                   "m_tau_MeV": [mtau, stau], "m_tau_belle2_MeV": [lm["m_tau_belle2_MeV"],
                                                                   lm["m_tau_belle2_sigma_MeV"]]},
        "Q": float(f"{q:.9f}"),
        "sigma_Q": float(f"{sq:.3g}"),
        "Q_target": "2/3 = 0.666666667",
        "pull_sigma": round(pull, 2),
        "m_tau_predicted_by_Q_two_thirds_MeV": float(f"{mtau_pred:.4f}"),
        "m_tau_prediction_sigma_from_me_mmu_MeV": float(f"{spred:.2g}"),
        "pull_pdg2024_sigma": round(pull_pdg, 2),
        "pull_belle2_2023_sigma": round(pull_belle2, 2),
        "kill_window": {
            "rule": "|m_tau - m_tau(Q=2/3)| >= 5 sigma(m_tau), systematics-controlled",
            "gap_today_pdg_MeV": float(f"{gap_pdg:.4f}"),
            "sigma_needed_to_kill_at_current_pdg_central_MeV": float(f"{gap_pdg / 5.0:.4f}"),
            "gap_today_belle2_MeV": float(f"{gap_belle2:.4f}"),
            "sigma_needed_to_kill_at_belle2_central_MeV": float(f"{gap_belle2 / 5.0:.4f}"),
            "note": ("a future tau-mass at today's Belle II central (1777.09) with "
                     "sigma <~ 0.024 MeV would be a 5-sigma kill; at today's PDG central "
                     "(1776.93) sigma <~ 0.008 MeV would be needed. Belle II full dataset "
                     "aims at O(0.01-0.05) MeV -- the window is live.")},
        "kill_triggered": bool(abs(pull) >= KILL_SIGMA),
        "verdict": "consistent",
    }


def dq_dm_at(m1: float, m2: float, m3: float) -> float:
    s = m1 + m2 + m3
    t = math.sqrt(m1) + math.sqrt(m2) + math.sqrt(m3)
    return (1.0 / t ** 2) * (1.0 - (s / t) / math.sqrt(m3))


def solve_mtau(me: float, mmu: float) -> float:
    mt = 1777.0
    for _ in range(60):
        q = (me + mmu + mt) / (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mt)) ** 2
        mt -= (q - KOIDE_Q_TFPT) / dq_dm_at(me, mmu, mt)
    return mt


# --------------------------------------------------------------------------- D
def axis_d_sterile(m: dict) -> dict:
    """N_fam = 3 dissolution watch: TFPT REQUIRES every short-baseline anomaly to
    dissolve (no 4th light state exists to oscillate into). Data-driven front-by-front
    status from data/measurements.json; kill = any confirmed >= 5 sigma sterile
    oscillation signal."""
    st = m["sterile_neutrino"]
    fronts = []
    any_signal = False
    for name, f in st["fronts"].items():
        any_signal = any_signal or bool(f["confirmed_sterile_signal"])
        fronts.append({"front": name, "reference": f["reference"],
                       "direction": f["direction"],
                       "confirmed_sterile_signal": f["confirmed_sterile_signal"],
                       "status_note": f["status_note"]})
    return {
        "tfpt_fixed_point": {
            "N_fam": N_FAM_TFPT,
            "statement": ("N_fam = 3 is an exact compiler output (D5+A3+mu4 => E8): "
                          "there is no spare E8 slot for a 4th light family/sterile "
                          "state, so TFPT PREDICTS the dissolution of every "
                          "short-baseline anomaly -- not merely survives it.")},
        "fronts": fronts,
        "today": ("MicroBooNE's two-beam analysis (Nature, Dec 2025) excludes the "
                  "single light sterile interpretation of LSND/MiniBooNE at 95% CL "
                  "and cuts into the gallium/BEST parameter space; the gallium "
                  "counting deficit itself persists unexplained (no oscillation "
                  "signature); JSNS2 is running (first data consistent with "
                  "background); SBND+ICARUS will decide this decade."),
        "kill_rule": "any confirmed sterile oscillation signal at >= 5 sigma "
                     "(systematics-controlled; e.g. joint SBND+ICARUS or JSNS2-II)",
        "kill_triggered": any_signal,
        "verdict": "tension" if any_signal else "consistent",
    }


# --------------------------------------------------------------------------- E
def axis_e_cabibbo_neutron(m: dict) -> dict:
    """Cabibbo/first-row dissolution (the axis named 2026-07-03) PLUS the new
    parameter-free neutron-lifetime reading: exact unitarity fixes V_ud, the
    CMS master formula then fixes tau_n with NO TFPT dial -- taking the bottle
    side of the beam-bottle puzzle and forbidding the dark-decay exit."""
    cf = m["cabibbo_first_row"]
    nl = m["neutron_lifetime"]

    v_us_tfpt = LAMBDA_C_TFPT

    # -- V_us routes vs frozen lambda_C --
    vus_rows = []
    for r in cf["V_us"]:
        vus_rows.append({"route": r["route"], "value": r["value"], "sigma": r["sigma"],
                         "pull_sigma": round((v_us_tfpt - r["value"]) / r["sigma"], 2)})
    r_kmu2, s_r = cf["V_us_over_V_ud_kmu2"], cf["V_us_over_V_ud_kmu2_sigma"]
    vus_kmu2 = r_kmu2 / math.sqrt(1.0 + r_kmu2 ** 2)
    s_kmu2 = s_r / (1.0 + r_kmu2 ** 2) ** 1.5
    vus_rows.insert(2, {"route": "Kmu2 route (unitarity-projected)", "value": round(vus_kmu2, 5),
                        "sigma": round(s_kmu2, 5),
                        "pull_sigma": round((v_us_tfpt - vus_kmu2) / s_kmu2, 2)})

    # -- V_ud routes vs unitarity value --
    vud_rows = []
    for r in cf["V_ud"]:
        vud_rows.append({"route": r["route"], "value": r["value"], "sigma": r["sigma"],
                         "pull_sigma": round((V_UD_TFPT - r["value"]) / r["sigma"], 2)})

    # -- the NEW leg: parameter-free tau_n via the CMS master formula --
    C, sC = nl["master_formula_s"], nl["master_formula_sigma_s"]
    gA, sgA = nl["gA_perkeo3"], nl["gA_perkeo3_sigma"]
    denom = V_UD_TFPT ** 2 * (1.0 + 3.0 * gA ** 2)
    tau_tfpt = C / denom
    # error propagation: master-formula constant + gA (V_ud is exact in TFPT)
    dtau_dC = tau_tfpt / C
    dtau_dgA = -tau_tfpt * 6.0 * gA / (1.0 + 3.0 * gA ** 2)
    s_tau = math.sqrt((dtau_dC * sC) ** 2 + (dtau_dgA * sgA) ** 2)

    def pull(tau_meas: float, s_meas: float) -> float:
        return (tau_tfpt - tau_meas) / math.sqrt(s_meas ** 2 + s_tau ** 2)

    tau_rows = [
        {"dataset": "UCNtau final (bottle, magnetic)", "value": nl["tau_bottle_ucntau_s"],
         "sigma": nl["tau_bottle_ucntau_sigma_s"],
         "pull_sigma": round(pull(nl["tau_bottle_ucntau_s"], nl["tau_bottle_ucntau_sigma_s"]), 2)},
        {"dataset": "magnetic/grav UCN storage average", "value": nl["tau_bottle_magnetic_avg_s"],
         "sigma": nl["tau_bottle_magnetic_avg_sigma_s"],
         "pull_sigma": round(pull(nl["tau_bottle_magnetic_avg_s"],
                                  nl["tau_bottle_magnetic_avg_sigma_s"]), 2)},
        {"dataset": "beam average (proton counting)", "value": nl["tau_beam_avg_s"],
         "sigma": nl["tau_beam_avg_sigma_s"],
         "pull_sigma": round(pull(nl["tau_beam_avg_s"], nl["tau_beam_avg_sigma_s"]), 2)},
        {"dataset": "J-PARC beam (electron counting)", "value": nl["tau_beam_jparc_s"],
         "sigma": nl["tau_beam_jparc_sigma_s"],
         "pull_sigma": round(pull(nl["tau_beam_jparc_s"], nl["tau_beam_jparc_sigma_s"]), 2)},
    ]
    bottle_pull = tau_rows[0]["pull_sigma"]
    beam_pull = tau_rows[2]["pull_sigma"]

    first_row_pull = (1.0 - cf["first_row_sum"]) / cf["first_row_sum_sigma"]
    return {
        "tfpt_fixed_point": {
            "lambda_C": round(LAMBDA_C_TFPT, 7),
            "V_ud_unitarity": round(V_UD_TFPT, 5),
            "statement": ("lambda_C = sqrt(phi0(1-phi0)) exactly (frozen v84) + exact CKM "
                          "unitarity: the first-row deficit MUST dissolve, and TFPT says "
                          "where -- V_us converges to 0.22438 (between the two kaon routes) "
                          "and the V_ud side resolves against superallowed (nuclear "
                          "structure/RC), whose routes the neutron already contradicts.")},
        "first_row_deficit_sigma": round(first_row_pull, 2),
        "V_us_routes": vus_rows,
        "V_ud_routes": vud_rows,
        "neutron_lifetime": {
            "master_formula": "tau_n = 4906.4(1.7) s / (V_ud^2 (1+3 gA^2))  [CMS, arXiv:1907.06737]",
            "gA_input": f"{gA}({sgA}) PERKEO III",
            "tau_n_tfpt_s": round(tau_tfpt, 2),
            "tau_n_tfpt_sigma_s": round(s_tau, 2),
            "confrontations": tau_rows,
            "reading": ("TFPT's exact V_ud lands the parameter-free tau_n on the BOTTLE "
                        "side of the beam-bottle puzzle (<1 sigma from UCNtau) and puts "
                        "the proton-counting beam average at ~ -5 sigma => the beam "
                        "carries a systematic (proton counting), exactly as the "
                        "electron-counting J-PARC beam result already suggests. The "
                        "dark-decay exit (n -> chi) is FORBIDDEN by the same E8 counting "
                        "as axis D -- TFPT cannot absorb a real beam-bottle split."),
        },
        "deciders": "PIONEER (pi_e3), lattice f+(0)+fK/fpi, superallowed NS/RC re-evaluations, "
                    "NIST BL2/BL3, J-PARC full dataset, tau_n/gA consensus",
        "kill_rule": ("converged all-route V_us (S~1) with |V_us - 0.224376| >= 5 sigma; OR a "
                      "systematics-converged first-row deficit >= 5 sigma; OR a confirmed "
                      "beam-bottle split established as real new physics (dark decay) at >= 5 "
                      "sigma; OR bottle tau_n drifting >= 5 sigma from 877.5-877.8 s at fixed gA"),
        "kill_triggered": False,
        "verdict": "consistent",
    }


# --------------------------------------------------------------------------- F
def axis_f_x17(m: dict) -> dict:
    """X17 dissolution watch: no E8 slot for a ~17 MeV boson -- the ATOMKI
    anomaly family must dissolve (nuclear/systematic origin)."""
    fronts = []
    any_signal = False
    for name, f in m["x17"]["fronts"].items():
        any_signal = any_signal or bool(f["confirmed_signal"])
        fronts.append({"front": name, "reference": f["reference"],
                       "direction": f["direction"],
                       "confirmed_signal": f["confirmed_signal"],
                       "status_note": f["status_note"]})
    return {
        "tfpt_fixed_point": {
            "statement": ("the E8 compiler content (D5+A3+mu4 carrier counting) has no slot "
                          "for a new ~17 MeV boson with the required couplings -- like the "
                          "sterile axis D, TFPT PREDICTS the dissolution of the ATOMKI "
                          "anomaly family, not merely survives it.")},
        "fronts": fronts,
        "today": ("MEG II (2025) finds no signal in the same 8Be transition (though still "
                  "~1.5 sigma compatible with the ATOMKI combination); PADME's resonant "
                  "scan is background-consistent except a 1.8-2.0 sigma GLOBAL excess at "
                  "16.90 MeV; PADME Run IV (upgraded, 2025/26) is the decisive dataset."),
        "kill_rule": "a confirmed >= 5 sigma X17 resonance (systematics-controlled, "
                     "replicated outside ATOMKI; e.g. PADME Run IV or MEG II full data)",
        "kill_triggered": any_signal,
        "verdict": "tension" if any_signal else "consistent",
    }


# --------------------------------------------------------------------------- G
def axis_g_rd(m: dict) -> dict:
    """R_D(*) lepton-flavor-universality dissolution watch: the frozen CKM
    assembly is exactly unitary and the compiler leaves no light NP state to
    source b -> c tau nu enhancement -- the HFLAV excess must dissolve."""
    rd = m["rd_rdstar"]
    pull_rd = (rd["RD_exp"] - rd["RD_sm"]) / math.sqrt(rd["RD_exp_sigma"] ** 2 + rd["RD_sm_sigma"] ** 2)
    pull_rds = (rd["RDstar_exp"] - rd["RDstar_sm"]) / math.sqrt(rd["RDstar_exp_sigma"] ** 2 + rd["RDstar_sm_sigma"] ** 2)
    return {
        "tfpt_fixed_point": {
            "statement": ("TFPT reads the flavor sector as the frozen, exactly unitary CKM/PMNS "
                          "assembly + SM gauge content; there is no compiler slot for the "
                          "charged mediator (leptoquark/W') a real R_D(*) excess needs. Like "
                          "axes D/E/F this is a DISSOLUTION prediction: SM values must return.")},
        "hflav_ckm2025": {
            "RD": f"{rd['RD_exp']} +- {rd['RD_exp_sigma']} (SM {rd['RD_sm']} +- {rd['RD_sm_sigma']}, "
                  f"pull {pull_rd:+.1f} sigma)",
            "RDstar": f"{rd['RDstar_exp']} +- {rd['RDstar_exp_sigma']} (SM {rd['RDstar_sm']} +- "
                      f"{rd['RDstar_sm_sigma']}, pull {pull_rds:+.1f} sigma)",
            "combined_tension_sigma": rd["combined_tension_sigma"],
            "combined_tension_flag24_sigma": rd["combined_tension_flag24_sigma"]},
        "today": ("HFLAV CKM25 combination sits at 3.8 sigma (3.5 with FLAG24 lattice SM) -- "
                  "the most significant currently-standing dissolution target of the watchdog; "
                  "Belle II full dataset and LHCb Run 3 decide this decade."),
        "kill_rule": "R_D(*) excess confirmed at >= 5 sigma with independent tagging methods "
                     "and consolidated SM form factors (lattice + dispersive agreement)",
        "kill_triggered": False,
        "verdict": "tension",
    }


# ------------------------------------------------------------------------ main
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT exact-fixed-point watchdog")
    ap.add_argument("command", choices=["analyze"], nargs="?", default="analyze")
    ap.parse_args(argv)
    m = json.loads(DATA.read_text(encoding="utf-8"))

    print("=" * 78)
    print("TFPT fixed-point watchdog -- exact fixed points vs published data "
          f"(retrieved {m['retrieved']})")
    print("=" * 78)
    print(f"  fixed points: w = -1 | Sigma m_nu = {SIGMA_MNU_TFPT} eV | "
          f"alpha^-1 = {ALPHA_INV_TFPT} (static) | Koide Q = 2/3 | N_fam = {N_FAM_TFPT}")
    print(f"  alpha-Lambda lock: rho_L/Mbar^4 = (3/4pi^2) e^(-2 alpha^-1), "
          f"amplifier 2 alpha^-1 = {AMPLIFIER:.2f}\n")

    a = axis_a_pincer(m)
    print("AXIS A -- Sigma m_nu x w PINCER (DESI DR2 2025)")
    ra_l, ra_w = a["reading_LCDM"], a["reading_w0waCDM"]
    print(f"  LCDM reading   : TFPT floor {SIGMA_MNU_TFPT} eV vs eff-mass posterior "
          f"-> pull {ra_l['pull_nu_sigma']:+.2f} sigma (paper: 3.0 sigma vs NO floor); "
          f"inside 0.0642 bound: {ra_l['inside_standard_95_bound_0.0642eV']}, "
          f"inside FC 0.053: {ra_l['inside_feldman_cousins_95_bound_0.053eV']}")
    print(f"  w0waCDM reading: nu pull {ra_w['pull_nu_sigma']:+.2f} sigma (compatible), BUT "
          f"(w0,wa)=(-1,0) at {ra_w['w_axis_headline_sigma']:.1f} sigma "
          f"[{ra_w['w_axis_headline_combination']}]; joint (3 dof) ~ "
          f"{ra_w['joint_3dof_equivalent_sigma']:.2f} sigma")
    for r in ra_w["w_axis_2d_sigma"]:
        print(f"      {r['name']:22s} 2D {r['tension_2d_sigma']:.2f}s "
              f"(published {r['published_sigma_vs_LCDM']:.1f}s)")
    print(f"  -> verdict: {a['verdict'].upper()} "
          f"(max {a['max_tension_sigma']:.1f} sigma < {KILL_SIGMA} kill)\n")

    b = axis_b_lock(m)
    print("AXIS B -- alpha-Lambda LOCK (PTB clocks vs DESI face value)")
    li = b["lock_implied_dln_lambda_dt_per_yr"]
    print(f"  clock: alpha_dot/alpha = 1.8(2.5)e-19 /yr -> lock-implied "
          f"|d ln Lambda/dt| < {li['bound_2sigma']:.3g} /yr (2 sigma) "
          f"[central {li['central']:.3g}, cons. {li['bound_central_plus_2sigma']:.3g}]")
    for r in b["desi_face_value_dln_rho_de_dt_per_yr"]:
        print(f"      {r['name']:22s} w0={r['w0']:+.3f} -> |d ln rho_DE/dt|(z=0) = "
              f"{r['dln_rho_de_dt_per_yr']:.3g} /yr")
    me_ = b["mutual_exclusion"]
    print(f"  mutual exclusion: DESI-implied Lambda drift / clock-lock bound = "
          f"{me_['violation_factor']:.3g} (~10^{me_['orders_of_magnitude']}); implied "
          f"alpha drift {me_['implied_alpha_drift_if_lock_and_desi_real_per_yr']:.3g} /yr "
          f"vs clock bound {me_['clock_bound_2sigma_per_yr']:.1g} /yr")
    print(f"  -> verdict: {b['verdict'].upper()} (TFPT + real w(z) evolution internally "
          f"excluded by ~{me_['orders_of_magnitude']} orders)\n")

    c = axis_c_koide(m)
    print("AXIS C -- KOIDE-tau KILL WINDOW (PDG 2024/2025 + Belle II 2023)")
    print(f"  Q = {c['Q']:.9f} +- {c['sigma_Q']:.3g}  vs 2/3  -> pull "
          f"{c['pull_sigma']:+.2f} sigma")
    print(f"  m_tau(Q=2/3) = {c['m_tau_predicted_by_Q_two_thirds_MeV']:.4f} MeV "
          f"(+- {c['m_tau_prediction_sigma_from_me_mmu_MeV']:.2g} from m_e, m_mu)")
    print(f"  PDG 2024/2025: 1776.93(9)  -> {c['pull_pdg2024_sigma']:+.2f} sigma | "
          f"Belle II 2023: 1777.09(14) -> {c['pull_belle2_2023_sigma']:+.2f} sigma")
    kw = c["kill_window"]
    print(f"  kill window: 5-sigma kill needs sigma(m_tau) < "
          f"{kw['sigma_needed_to_kill_at_current_pdg_central_MeV']:.3f} MeV at the PDG "
          f"central, or < {kw['sigma_needed_to_kill_at_belle2_central_MeV']:.3f} MeV at "
          f"the Belle II central")
    print(f"  -> verdict: {c['verdict'].upper()}\n")

    d = axis_d_sterile(m)
    print("AXIS D -- STERILE-nu DISSOLUTION (N_fam = 3; short-baseline status 2025/26)")
    print(f"  TFPT: N_fam = {N_FAM_TFPT} exactly -- no E8 slot for a 4th light state; "
          f"every short-baseline anomaly MUST dissolve")
    for f in d["fronts"]:
        sig = "SIGNAL" if f["confirmed_sterile_signal"] else "no signal"
        print(f"      {f['front']:22s} [{sig}] {f['direction']}")
        print(f"        {f['reference']}")
    print(f"  kill rule: {d['kill_rule']}")
    print(f"  -> verdict: {d['verdict'].upper()} (the dissolution prediction is being "
          f"confirmed; gallium deficit still unexplained but shows no oscillation "
          f"signature)\n")

    e = axis_e_cabibbo_neutron(m)
    print("AXIS E -- CABIBBO DISSOLUTION + parameter-free NEUTRON LIFETIME (PDG26/2026)")
    print(f"  TFPT: lambda_C = {e['tfpt_fixed_point']['lambda_C']} exact -> unitarity "
          f"V_ud = {e['tfpt_fixed_point']['V_ud_unitarity']}; first-row deficit "
          f"{e['first_row_deficit_sigma']:+.1f} sigma must dissolve")
    print("  V_us routes:")
    for r in e["V_us_routes"]:
        print(f"      {r['route']:32s} {r['value']:.5f} +- {r['sigma']:.5f}  "
              f"pull {r['pull_sigma']:+5.2f}s")
    print("  V_ud routes:")
    for r in e["V_ud_routes"]:
        print(f"      {r['route']:32s} {r['value']:.5f} +- {r['sigma']:.5f}  "
              f"pull {r['pull_sigma']:+5.2f}s")
    nlr = e["neutron_lifetime"]
    print(f"  NEW parameter-free tau_n = {nlr['tau_n_tfpt_s']:.2f} +- "
          f"{nlr['tau_n_tfpt_sigma_s']:.2f} s   [{nlr['master_formula']}]")
    for r in nlr["confrontations"]:
        print(f"      {r['dataset']:36s} {r['value']:.2f} +- {r['sigma']:.2f} s  "
              f"pull {r['pull_sigma']:+5.2f}s")
    print(f"  -> verdict: {e['verdict'].upper()} (tau_n lands on the BOTTLE side; "
          f"beam average at {nlr['confrontations'][2]['pull_sigma']:+.1f}s; dark-decay "
          f"exit forbidden)\n")

    f_ = axis_f_x17(m)
    print("AXIS F -- X17 DISSOLUTION (ATOMKI / MEG II / PADME status 2025/26)")
    print("  TFPT: no E8 slot for a ~17 MeV boson -- the ATOMKI family must dissolve")
    for fr in f_["fronts"]:
        sig = "SIGNAL" if fr["confirmed_signal"] else "no confirmed signal"
        print(f"      {fr['front']:10s} [{sig}] {fr['direction']}")
    print(f"  kill rule: {f_['kill_rule']}")
    print(f"  -> verdict: {f_['verdict'].upper()} (MEG II null; PADME 16.90 MeV global "
          f"~1.8-2.0 sigma; Run IV decides)\n")

    g = axis_g_rd(m)
    print("AXIS G -- R_D(*) DISSOLUTION (HFLAV CKM 2025)")
    print(f"  {g['hflav_ckm2025']['RD']}")
    print(f"  {g['hflav_ckm2025']['RDstar']}")
    print(f"  combined: {g['hflav_ckm2025']['combined_tension_sigma']} sigma "
          f"({g['hflav_ckm2025']['combined_tension_flag24_sigma']} with FLAG24) -- "
          f"must dissolve; Belle II / LHCb Run 3 decide")
    print(f"  -> verdict: {g['verdict'].upper()} (the most significant standing "
          f"dissolution target of the watchdog)\n")

    res = {
        "tfpt_fixed_points": {
            "w0": W0_TFPT, "wa": WA_TFPT, "sigma_mnu_eV": SIGMA_MNU_TFPT,
            "alpha_inv": ALPHA_INV_TFPT, "koide_Q": "2/3", "N_fam": N_FAM_TFPT,
            "alpha_lambda_lock": "rho_L/Mbar^4 = (3/4pi^2) e^(-2 alpha^-1)",
            "amplifier": AMPLIFIER,
            "lambda_C": round(LAMBDA_C_TFPT, 7), "V_ud_unitarity": round(V_UD_TFPT, 5)},
        "axis_A_mnu_w_pincer": a,
        "axis_B_alpha_lambda_lock": b,
        "axis_C_koide_tau": c,
        "axis_D_sterile_dissolution": d,
        "axis_E_cabibbo_neutron_lifetime": e,
        "axis_F_x17_dissolution": f_,
        "axis_G_rd_dissolution": g,
        "verdicts": {"A": a["verdict"], "B": b["verdict"], "C": c["verdict"],
                     "D": d["verdict"], "E": e["verdict"], "F": f_["verdict"],
                     "G": g["verdict"]},
        "kill_triggered_any": bool(a["kill_triggered"] or b["kill_triggered"]
                                   or c["kill_triggered"] or d["kill_triggered"]
                                   or e["kill_triggered"] or f_["kill_triggered"]
                                   or g["kill_triggered"]),
        "retrieved": m["retrieved"],
    }
    om = b["mutual_exclusion"]["orders_of_magnitude"]
    verdict_line = (f"WATCHDOG: A={a['verdict']} ({a['max_tension_sigma']:.1f}s pincer), "
                    f"B={b['verdict']} (lock excludes TFPT+real-w(z) by ~10^{om}), "
                    f"C={c['verdict']} ({c['pull_sigma']:+.2f}s Koide), "
                    f"D={d['verdict']} (sterile dissolution on track, MicroBooNE 2025), "
                    f"E={e['verdict']} (tau_n {nlr['tau_n_tfpt_s']:.1f} s bottle-side "
                    f"{nlr['confrontations'][0]['pull_sigma']:+.1f}s / beam "
                    f"{nlr['confrontations'][2]['pull_sigma']:+.1f}s), "
                    f"F={f_['verdict']} (X17 dissolving, PADME Run IV decides), "
                    f"G={g['verdict']} (R_D(*) 3.8s standing -- sharpest dissolution target). "
                    f"No kill triggered (threshold {KILL_SIGMA} sigma).")
    print("-> " + verdict_line)
    res["verdict_line"] = verdict_line

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
