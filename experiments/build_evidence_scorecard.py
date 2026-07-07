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
     "Stage-1 matched-filter validated (3/3); real GWOSC strain spans the 10 loudest ringdowns incl. "
     "GW250114 (SNR 78.6, O4b), all templates redshift-corrected to detector-frame f0 -> no kernel-"
     "ratio echo in any event; Stage-1b STACK over 23 detector streams: stacked p=0.262, kernel-"
     "consistent streams 0/23; Stage-1c SIGNATURE BATTERY (energy-reading (2/3)^3, step 2/3, mu4 "
     "per-bounce phases {0,pi/2,pi,3pi/2} = boundary-birefringence analogue, lags 0.5-350 ms incl. "
     "Planckian window, joint 220+221 subtraction, OFF-SOURCE event-gated PSD, Bonferroni x12): "
     "NO_VARIANT_ECHO; Stage-1d POINT TEST v2 (lag FIXED by C=3/8: dt=2.288 M_det +-25%, kernel "
     "ratios, spin scan af={0.60,0.69,0.80}, skip-first-echo, morphology-robust incoherent statistic, "
     "JOINT QNM+train fit repairing the short-lag subtract-then-search self-absorption, Bonferroni "
     "x39): NO_POINT_ECHO (best p_bonf=0.052, single stream GW150914/L1); Stage-1f OFFSET TRAIN "
     "(first echo at the scrambling time t_scr=4M lnS ~0.25s, spacing 2.288M, no QNM subtraction "
     "needed): NO_OFFSET_TRAIN (best p_bonf=0.035); Stage-1g DRIFT+PRECESSION scan (per-bounce "
     "spacing drift +-5/10%, position-only free-phase statistic): NO_DRIFT_OR_PRECESSION_ECHO "
     "(best p_bonf=0.046); broadband-excess mystery RESOLVED by the subtraction ladder: greedy "
     "matching-pursuit residual modelling absorbs the GW200129/GW190521 excesses entirely (quasi-"
     "QNM transient power, higher overtones/mode mixing), GW150914 strongly reduced (one stream "
     "left, older detector state) -- no echo-train candidate at any subtraction depth; the null "
     "is robust against every tested signature reading and systematic; Stage-1d re-run on 16 kHz "
     "strain (lag now 12-13 samples): NO_POINT_ECHO unchanged (best p_bonf 0.053) -> null not a "
     "lag-resolution artefact; Stage-1h INJECTION CAMPAIGN: calibrated ABSOLUTE limits eps_90 "
     "(first-echo/A220, 90% CL): GW200129 0.63, GW150914 0.69, GW190521 1.86, GW250114 15.9 "
     "(weak A220 fit); stack conservative 0.63 (4k)/0.85 (16k); kernel ceiling (2/3)^6=0.088 "
     "~7x below current single-event reach",
     None, "search_target", "boundary recovery kernel",
     "strain_level_test", "LVK GWTC-5.0 + real 32s strain (10 loudest ringdowns incl. GW250114, O4b)",
     "strain-level echo with ratio >>(2/3)^6 across events", "null"],
    ["GW", "area-quantum spectral comb (BM lines)", "Delta A = 4 ln3 => f_n = n ln3/(16 pi^2 M_det)",
     "Stage-1e first run: post-merger residual spectrum comb (~14-23 Hz spacing, ~10-25 harmonics "
     "in band) with spacing battery {0.8,0.9,1.1,1.25}xf_BM as specificity control, off-source PSD, "
     "spin scan: NO_BM_COMB on all 10 loudest events (best p_bonf=0.032, not spacing-specific, no "
     "2nd detector); line widths/exterior coupling model-dependent -> power-limited null",
     None, "search_target", "horizon area quantum (Hod ln3, v57)",
     "strain_level_test", "real 32s GWOSC strain (10 loudest ringdowns incl. GW250114, O4b)",
     "a spacing-specific BM comb coincident in >=2 detectors surviving injections", "data_limited"],
    ["GW", "dynamic walled-clock recovery bend (Stage 2)",
     "bend rate(2)/rate(1)=ln3/ln(3/2)=2.7095 + protected floor + hard wall (v124/v147, QT.04)",
     "NO_KERNEL_RECOVERY on real strain incl. GW250114 (loudest ringdown, O4b): q_hat~1, not the bend; "
     "identifiability: within ONE recovery the bend is degenerate with single-exp (two-mode R^2 gain "
     "~1.3e-3, even noise-free) -> a single ringdown cannot carry the bend; discriminating signature "
     "is the cascade comb (omega=2.58, eps~2%)",
     None, "search_target", "boundary recovery kernel (dynamic)",
     "strain_level_test", "real 32s GWOSC strain (GW250114/GW150914/GW190521); QT.04 walled-clock template",
     "a locked-bend (2.7095) two-timescale recovery coincident in >=2 detectors", "data_limited"],
    # ---- pulsar glitches (experiments/pulsar-glitch-recovery) ----
    # the missing cross-domain leg: same frozen kernel as FRB.02/09 + GW echo
    ["pulsar", "glitch-size log-periodicity (PG.01)", "comb at (3/2)^k or {1+phi0,4,8,8pi}",
     "real comb is the known 2-population bimodality (vanishes under population-controlled null; "
     "(3/2)^6 raw p_gmm=0.03 fails LEE x7)", None, "search_target", "boundary recovery kernel",
     "search_target", "Jodrell Bank Glitch Catalogue (Basu+2022; 726 glitches/222 pulsars)",
     "a preregistered TFPT ratio comb survives the population-controlled null + look-elsewhere", "null"],
    ["pulsar", "per-pulsar size/waiting kernel ladder (PG.02/03)",
     "|dlog s|, dt-ratios on {log 3/2, (3/2)^3, (3/2)^6}",
     "null (frac 0.20/0.22 vs within-pulsar shuffle, p=0.27/0.93; 68/50 pulsars)", None,
     "search_target", "boundary recovery kernel",
     "search_target", "Jodrell Bank Glitch Catalogue (within-pulsar shuffle null)",
     "consecutive glitches step by kernel factors above the within-pulsar shuffle", "null"],
    ["pulsar", "recovery Q / tau_d kernel structure (PG.04)",
     "Q in {phi0..8phi0,1-phi0}; multi-comp tau_d ladder (3/2)^k",
     "null (Q frac 0.10 vs 0.22 chance, p~1.0; tau_d ratios p=0.69; 60 comp/46 glitches)", None,
     "search_target", "boundary recovery kernel (Q/tau_d)",
     "search_target", "Yu+2013 (MNRAS 429,688) expTab recovery table",
     "Q clusters at phi0 multiples OR tau_d components form the kernel ladder", "null"],
    ["pulsar", "dynamic recovery comb on real nu(t) (PG.05)",
     "log-periodic comb at omega=2pi/ln((3/2)^6)=2.583 in the post-glitch recovery waveform",
     "data_limited: detector injection-validated on the real monthly sampling (cascade comb found "
     "p=0.002, smooth power law rejected p=0.15); NO kernel comb in 7 Crab inter-glitch segments "
     "(p=0.12-0.44); monthly cadence < the ~2% (eps~exp(-pi^2/ln lambda)) comb amplitude", None,
     "search_target", "boundary recovery kernel (dynamic)",
     "strain_level_test", "Jodrell Bank Crab monthly ephemeris (479 nu/nudot points, 1988-2026)",
     "a log-periodic comb at omega=2.58 is special vs the off-kernel periodogram in a clean segment",
     "data_limited"],
    ["pulsar", "real NICER Vela reduction pipeline (PG.06b)",
     "download L2 events + PINT barycentre + H-test fold of the long-interval target (Vela)",
     "PIPELINE PROVEN ON REAL DATA: 665 NICER Vela obs confirmed (HEASARC, ~7.9 yr); one obs "
     "downloaded + PINT-barycentred (no HEASoft) -> Vela pulsation DETECTED at F0=11.193 Hz "
     "(89.34 ms, H=18.4). Comb-quality nu(t) still needs phase-connected timing (~6.5 GB, multi-hour)", None,
     "search_target", "boundary recovery kernel (dynamic, real-data pipeline)",
     "strain_level_test", "HEASARC NICER Vela pulsar PSR B0833-45 (665 obs) + PINT",
     "a phase-connected nu(t) over a >~2.8-period Vela inter-glitch recovery shows the omega=2.58 comb",
     "data_limited"],
    ["pulsar", "dense J0537 stacked recovery comb + range finding (PG.06)",
     "same omega=2.583 comb, stacked over many J0537 glitches (NICER/RXTE, dense)",
     "data_limited/scaffold: 1165 NICER J0537 observations confirmed (HEASARC, ~8 yr); upstream "
     "(L2 events + PINT fold -> nu(t)) gated on ~GB downloads (no HEASoft needed); downstream "
     "injection-validated (comb detected 96%, 0% false-positive in sufficient range). KEY: the comb "
     "needs >~2.8 ln(tau) periods; J0537 ~100 d intervals give ~1.9 (range-blind) -- stacking buys "
     "amplitude not range -> the decisive target is a long-interval pulsar (Vela), not J0537", None,
     "search_target", "boundary recovery kernel (dynamic, stacked)",
     "strain_level_test", "HEASARC NICER J0537-6910 (Ho+2020 MNRAS 498,4605; 1165 obs) + PINT",
     "a stacked log-periodic comb at omega=2.58 over a >~2.8-period (long-interval) recovery",
     "data_limited"],
    # PG.07: FIRST real phase-connected wide-ln(tau) Vela recovery (2024 giant glitch)
    ["pulsar", "dynamic recovery comb on the 2024 Vela giant glitch (PG.07)",
     "log-periodic comb at omega=2pi/ln((3/2)^6)=2.583 in the phase-connected post-glitch nudot(t) recovery",
     "data_limited: FIRST real phase-connected wide-ln(tau) Vela recovery (Delta nu/nu=2.4e-6, tau_d={0.39,2.45,15.1} d, 123 d window -> reach 2.55 comb periods, widest yet vs J0537's ~1.9). Detector injection-validated on the real cadence (cascade p=0.002, smooth rejected p=0.18); omega=2.583 NOT special (p=0.23, shuffle 0.60, off-kernel lambda-battery Bonferroni ~1.0); stacked 2016/2019/2021/2024 (reach 3.41) flat p=0.53. RANGE no longer the wall (95% detect at 2.55p); limited by product=smooth glitch MODEL not residual nu(t) + ~2% (eps~exp(-pi^2/ln lambda)) amplitude",
     None, "search_target", "boundary recovery kernel (dynamic)",
     "strain_level_test", "2024 Vela giant glitch phase-connected .par (Zenodo 10.5281/zenodo.17735648; A&A 698 A72 2025)",
     "a log-periodic comb at omega=2.58 is special vs the off-kernel periodogram over a >=2.8-period residual nu(t) Vela recovery",
     "data_limited"],
    # PG.08: the comb on REAL PuMA/IAR daily-cadence phase-connected ToA RESIDUALS
    ["pulsar", "recovery comb on PuMA/IAR daily ToA residuals (PG.08)",
     "log-periodic comb at omega=2.583 in the post-glitch ToA residuals (the product PG.07 "
     "named as decisive: residuals to the fit, refit-absorption basis projected out)",
     "REAL PuMA/IAR daily-cadence release (3 giant glitches, 969 post-glitch TOAs, PINT "
     "pulse-number tracking): J1740-3015 reaches 2.81 periods = FIRST real residual recovery "
     "past the 2.8-period gate; omega=2.583 NOT special in any leg (p 0.28/0.89/0.48; shuffle "
     "+ lambda battery agree); end-to-end injection at real sampling+noise: gate-passing leg "
     "~50% power at eps=0.30, 0% at predicted eps~1.7% -> bounded null, amplitude wall now "
     "binding (public Vela .tim starts at tau=10 d -> 1.83 periods); GLTD ladders 0/2 near "
     "bend 2.7095, Vela-2021 resolves 3 transient modes (wall exception, on record)", None,
     "search_target", "boundary recovery kernel (dynamic, ToA residuals)",
     "strain_level_test", "PuMA/IAR Timing_irregularities release (Zubieta+2024 A&A 689; "
     "GitHub PuMA-Coll) + PINT",
     "the omega=2.583 comb is special vs shuffle + off-kernel battery in a >=2.8-period "
     "residual recovery", "data_limited"],
    # ---- cross-domain recovery-comb search (experiments/recovery-comb-domains) ----
    ["FRB", "recovery comb in FRB burst tail (omega=2.58, stacked)",
     "log-periodic comb at omega=2pi/ln((3/2)^6) in the post-peak burst-tail recovery",
     "REAL data, now STACKED: 8 bright bursts across 3 repeaters (FRB 20121102A x5 FAST, "
     "FRB 20190520B x2 GBT, FRB 20201124A x1 GBT); 7 clear the >=2.8-period ln-range gate; "
     "phase-incoherent stack of the kernel comb gain -> omega=2.58 NOT special (p=0.34) -> clean "
     "NULL (single-burst weak null p=0.25 sharpened to a 7-burst/3-repeater stack). Still WEAK: "
     "FRB tails are scattering/noise-dominated and the comb is an intrinsic ~2% effect", None,
     "search_target", "boundary recovery kernel (dynamic)",
     "search_target", "real FRB waterfalls (FAST/GBT .calibP, 3 repeaters) + shared stacked comb detector",
     "the omega=2.58 comb is special vs the off-kernel periodogram in a clean stacked burst tail",
     "null"],
    ["FRB", "recovery comb in CHIME baseband FRB tail (omega=2.58, stacked)",
     "log-periodic comb at omega=2pi/ln((3/2)^6) in the post-peak burst-tail recovery",
     "REAL CHIME/FRB Baseband Catalog 1 (CANFAR DOI 10.11570/23.0029): 8 distinct FRBs at 2.56us, "
     "coherently dedispersed, full-Stokes; incoherent cross-channel dedispersion -> true profile + "
     "genuine scattering tail; all 8 clear the >=2.8-period gate; STACKED kernel omega=2.58 NOT "
     "special (p=0.67) -> clean NULL on cleaner data than FAST. Still WEAK: a ms burst has no "
     "3-decade recovery and the comb is an intrinsic ~2% effect", None,
     "search_target", "boundary recovery kernel (dynamic)",
     "search_target", "CHIME/FRB baseband catalog (DOI 10.11570/23.0029) + shared stacked comb detector",
     "the omega=2.58 comb is special vs the off-kernel periodogram in a clean stacked CHIME burst tail",
     "null"],
    ["FRB", "microshot cascade kernel (FRB 20220912A B1/B2)",
     "resummed recovery clock: gap ratio ln3/ln(3/2)=2.71 + hard wall at N_fam=3 + log-periodic "
     "time-comb omega=2.58 (v124, dynamic kernel)",
     "REAL vetted microshot catalog (Hewitt+2023 MNRAS 526 2039; Zenodo 10552561): B1 27 + B2 18 "
     "manually-identified microshots (intra-burst point process) + real NRT peak fluxes. Gap ratio "
     "NOT piled at 2.71 above a gap-shuffle null + placebo (B1 enr 1.47 p=0.16 vs placebo 1.26; B2 "
     "below chance); no protected wall (B1 longest decreasing-gap run=5>3); time-DSI comb range-limited "
     "(1.5-1.6 periods <2.8); amplitude echo ratio NOT enriched at 64/729 or 8/27 (B1 energy enr 0.80 "
     "p=0.75, a free quotient hits 9x vs ~0 at the kernel) -> clean NULL across all channels", None,
     "search_target", "boundary recovery kernel (dynamic, intra-burst point process)",
     "search_target", "Nan\u00e7ay ECLAT FRB 20220912A microshots (Hewitt+2023; Zenodo 10552561)",
     "a microshot gap-clock at 2.71 OR a protected wall<=3 OR a time-DSI comb survives the null in >=2 bright bursts",
     "null"],
    # frb-kernel-couplings (2026-07-06): axes the bird's-eye geometry/topology
    # scan found structurally untested -- the 2D ladder COUPLING (all prior tests were
    # marginals), the deck-VISIBLE polarization observable (signed V; PA is mod pi and
    # |V|/I is even, so FRB.04/06/08 were deck-blind by construction), size-space DSI,
    # plus the new non-tooth operator proxies (S8-like block leakage and S2a spectrum).
    ["FRB", "kernel couplings: joint energy-time tooth + V-handedness + size-space DSI "
     "+ phase-time helix + operator proxies (KC.01-06)",
     "KC.01 (forced UNDER THE EMISSION-READOUT BRIDGE E_obs ~ internal population, "
     "t ~ inverse rate -- an assumption NOT derived from TFPT; downgraded 2026-07-06): "
     "pairs on a time tooth (3/2)^k sit on the "
     "partner energy tooth (2/3)^k (E*t=const along the ladder); KC.02 (exploratory Z2 "
     "deck reading): consecutive kernel steps flip the SIGN of circular polarization "
     "(the only deck-visible pol observable); KC.03: log-periodic decoration of the "
     "burst-energy distribution at frozen TFPT ratios (PG.01 analog); KC.04 "
     "(exploratory mu4 deck reading): coupled phase Phi = omega ln(tau ratio) + "
     "q*2*dPA ~ const at frozen omega=2.583, q in {1,2}; KC.05 (exploratory S8 proxy): "
     "PA-derived C4 transition operator should suppress off-character leakage; KC.06 "
     "(exploratory S2a proxy): multivariate lag-1 operator on (cos2PA,sin2PA,L/I,signV) "
     "should approach spectrum {1,64/729,1/729}",
     "REAL committed catalogs (prereg kernel_couplings_v1.yaml + dated KC.04 addendum, "
     "each before its run): KC.01 clean NULL in both sources (20121102A Li+2021 1652 "
     "bursts: 14 joint hits vs 19.5 under the exact energy-shuffle null, enr 0.72 "
     "p=0.94; 20220912A Zhang+2023: p=0.84; free-quotient: >55% of arbitrary bases "
     "beat 2/3); KC.02 NULL (20240114A pol v5, 3540 signed-DOC bursts, 3454 pairs: "
     "alternation 0.480 vs shuffle 0.497, p=0.98 -- handedness mildly persists, "
     "magnetospheric memory; net handedness balanced +0.06); KC.03 NULL in both "
     "sources after the lognormal/KDE/GMM 3-null battery + Bonferroni (global p=0.185 "
     "/ 0.68; the famous energy bimodality is absorbed by the population null -- PG.01 "
     "replicated in the FRB energy domain); KC.04 NULL (83 sessions / 5934 pairs: the "
     "naive permutation null fires at q=1 p=0.0005 but the DRIFT-ROBUST circular-shift "
     "null gives p=0.12 and omega=2.583 is not special vs the off-kernel rank p=0.37 "
     "-- slow PA drift coupled to burst clustering, not a kernel helix; PA mod pi + "
     "RM-uncorrected documented); KC.05 NULL (6037 PA-class pairs: C4 off=0.4268, "
     "shuffle median 0.4629, p_low=0.0045, but Z3 off=0.3677 and random 4-mark controls "
     "can be lower -> not C4-specific block protection); KC.06 NULL (3447 multivariate "
     "polarization pairs: normalized eigs [1.0,0.5066,0.38444,0.04781], distance 0.5676 "
     "to {1,64/729,1/729}, shuffle p_close=0.1799). Audit note on record: a first-pass lambda=8 "
     "'candidate' in KC.03 was a null-generator artefact (sklearn GMM.sample re-seeds "
     "per call -> identical draws), caught by the split-half + free-lambda probes and "
     "fixed; the candidate dissolved", None,
     "search_target", "boundary recovery kernel (2D coupling + Z2/mu4 deck polarization "
     "+ size-space DSI + S8/S2a operator proxies)",
     "search_target", "Li+2021 (VizieR) + Zhang+2023 (VizieR) + FAST 20240114A pol "
     "catalog v5 (frb-kernel-couplings KC.01-06)",
     "a joint tooth, handedness alternation, size-space comb, phase helix, C4 block-leakage "
     "suppression, or S2a lag spectrum survives "
     "its preregistered null battery + controls in >=2 independent sources", "null"],
    # repeater-cascade (experiments/repeater-cascade): first search past the 2.8-period range wall
    ["FRB", "repeater burst-time cascade comb + walled clock (RC.01-04)",
     "frozen comb omega=2.583 in ln(t-t_onset) + walled two-mode clock (bend 2.7095) + "
     "waiting-time tooth ladder {log 3/2, log(3/2)^3, log(3/2)^6} on repeater burst-time "
     "cascades + RC.04 per-source PHASE coherence (persistent boundary-clock reading)",
     "9,916 real bursts / 4 sources (FRB 20220912A Zhang+2023, 20201124A Xu+2022/Zhang+2022, "
     "20240114A FAST pol v5, 15 CHIME Cat2 repeaters): FIRST search past the 2.8-period range "
     "wall -- 9 gate-passing sessions / 2 sources (max reach 4.80 periods), omega=2.583 NOT "
     "special (Fisher p=0.72/0.38, BH q=0.72); RC.01 bend degenerate on real cascades (0/37, "
     "Stage-2 degeneracy reproduced); RC.03 ladders null after Bonferroni (p=0.10); injection: "
     "94% at eps=0.30, 0% at predicted eps=0.0173 -> null at detectable amplitude, amplitude "
     "wall (~1e5 bursts/session) at the predicted 1.7%. RC.04 (2026-07-06): the per-source "
     "comb PHASE at the frozen omega is NOT more concentrated across sessions than the "
     "rate-preserving surrogate null (FRB20240114A R=0.21 over 7 sessions p=0.15; 20201124A "
     "R=0.24 over 2 p=0.49) -> bounds the PERSISTENT per-source clock reading; the transient "
     "per-event reading is untouched (t0-aligned coherent stacks elsewhere agree: PG.07 Vela "
     "p=0.53, crust superposed p=0.45)", None,
     "search_target", "boundary recovery kernel (dynamic, burst-time cascade)",
     "search_target", "FAST (VizieR J/ApJ/955/142; Blinkverse; pol catalog v5) + CHIME/FRB Cat2 "
     "(CANFAR DOI 10.11570/25.0066); repeater-cascade RC.01-03",
     "the omega=2.583 comb survives surrogates + off-kernel rank + lambda battery in >=2 "
     "gate-passing sessions", "null"],
    # frb-ontology (2026-07-07): the FO ontology round (next.txt 2026-07-07 (I)) --
    # what FRBs could BE in TFPT. FO.01 (transduction-invisibility contract, 5/5 PASS)
    # lives in theory-contracts and NEVER enters this scorecard. FO.02/FO.03 are the
    # two categorically new probes (named transduction B / named clock); FO.04/FO.06
    # are prime-2 parity diagnostics; FO.05 closes the episode aggregation level.
    ["FRB", "medium-state common two-rate operator (FO.02, named-B line integrals)",
     "if the relaxing magneto-ionic medium (probed by bursts as delta pulses; DM/RM "
     "are KNOWN linear line integrals -- the first FRB axis passing the S15 "
     "eligibility gate) relaxes under the transfer operator, ALL coupled observables "
     "share ONE two-rate set with frozen ratio r2/r1 = ln3/ln(3/2) = 2.7095 (unlike "
     "an AR(1)/OU drift with observable-specific memories, the FRB.04b killer)",
     "REAL FAST 20240114A pol v5 (6134 bursts, 89 nightly sessions): ACF single "
     "rates RM 0.019/d, DM 0.016/d, log10Weff 0.087/d, DOL 0.077/d; the joint "
     "shared two-rate fit lands at ratio 4.20 but AIC prefers per-observable single "
     "rates (8.07 vs 12.54) -> the nightly medium state does not REQUIRE a second "
     "rate; kernel not the closest ratio (placebo 4.5 closer), OU-null p=0.55. "
     "FO.02b (v1.2 addendum, INTRA-session cadence, 2 sources): the strong "
     "intra-session RM variance (constant-RM rejected at chi2red 77-337 in all 35 "
     "v5 sessions; Xu+2022 20201124A via Blinkverse, 1131 per-burst RM, spans "
     "50-240 rad/m2 over 2-3.5 h) carries NO temporal memory -- 33/35 (v5) and "
     "12/12 (20201124A) sessions fail the injection-validated memory gate (OU at "
     "tau=2-30 min detected 31-34/35 and 8-10/12; white-noise FP 3/35, 0/12) -> "
     "the burst-sampled variance is per-burst/magnetospheric, NOT a relaxing "
     "medium state; the ratio test has nothing to act on at burst cadence. The "
     "medium-measurement reading survives only in the untested hours-to-days band "
     "or via a tracked RM-injection event (20190520B-class table login-walled)", None,
     "search_target", "medium-state transfer operator (named linear transduction: "
     "DM/RM line integrals; S2a-class)",
     "search_target", "FAST 20240114A pol catalog v5 (frb-ontology FO.02, prereg "
     "frb_ontology_v1.yaml)",
     "a common two-rate set at 2.7095 beats the OU null + placebo ratios in the "
     "medium state of >=2 sources", "data_limited"],
    ["FRB", "state-clock comb in tau_mod = cumulative |dRM| (FO.03, S14 named clock)",
     "S14 clock-map reading: the session cascade ticks in the medium's own state "
     "path tau_mod = cumsum|dRM| (total-variation clock), not observer time; comb at "
     "frozen omega=2.583 in ln tau_mod. First FRB comb test with a NAMED clock (all "
     "prior S2b nulls ran on t_observer and are retro-typed bridge nulls)",
     "REAL FAST 20240114A pol v5: 3 sessions pass the 2.8-period reach gate in "
     "ln tau_mod (2.82/2.85/3.16 periods; 32 below gate); survive-all session p "
     "(max of increment-permutation and off-kernel-rank p) 0.84/0.45/0.59; Fisher "
     "p=0.81 -> NULL at detectable amplitude; the predicted eps=1.7% comb stays "
     "behind the amplitude wall (that leg data_limited, as in RC.02)", None,
     "search_target", "boundary recovery kernel (dynamic, S14 medium-state clock "
     "reading of the same comb question as RC.02)",
     "search_target", "FAST 20240114A pol catalog v5 (frb-ontology FO.03, prereg "
     "frb_ontology_v1.yaml)",
     "the omega=2.583 comb is special in ln tau_mod vs increment-permutation + "
     "off-kernel rank in >=2 gate-passing sessions", "null"],
    ["FRB", "parity-without-rate diagnostic: no mu4 PA refinement + rate-free "
     "switches + persistent classes (FO.04)",
     "the m=2 PA fundamental (FRB.08) and handedness persistence (KC.02) ARE the "
     "only Z2 signature the double cover may leave (parity/projection, never a rate; "
     "mu4 is a Galois gear without a pointer): (a) NO m=4 refinement ever; (b) "
     "class-switch times rate-free (no teeth, no comb); (c) class membership "
     "persistent across sessions",
     "REAL FAST 20240114A pol v5 (6133 PA bursts, L/I>=10%): (a) vm2-only first run "
     "fired nominally at m=4 (A4=0.0424 vs null 0.0127, p=0.0005) -- the dated v1.1 "
     "specificity battery resolves it: odd/even harmonic placebos fire equally "
     "(z3=3.6, z4=4.4, z6=4.2 -- generic misfit, the two PA modes sit 60.2 deg "
     "apart, not 90) and a 3-component smooth null absorbs m=4 (p=0.64) -> "
     "PA-distribution misfit, NOT a mu4 pointer, prediction (a) holds; (b) 376 "
     "switch waiting-time ratios: tooth enrichment 0.74, p=1.0, no comb-gated "
     "session -> rate-free; (c) 45/45 sessions share the global dominant PA mode "
     "(binomial p=2.8e-14) -> persistent. All three predictions hold; the same "
     "phenomenology is standard magnetospheric physics (orthogonal modes + "
     "propagation memory) -> consistency typing, never support", None,
     "search_target", "Z2 parity/projection diagnostic (prime 2 carries no rate; "
     "mu4 Galois-gear reading)",
     "search_target", "FAST 20240114A pol catalog v5 (frb-ontology FO.04, prereg "
     "frb_ontology_v1.yaml + dated v1.1 specificity addendum)",
     "a SPECIFIC m=4 refinement (beats odd-harmonic placebos + smooth-null battery) "
     "OR structured switch times OR non-persistent classes kills the "
     "parity-without-rate reading", "consistent"],
    ["FRB", "episode-level transfer ladder: quiescence gaps + episode-integrated "
     "energies on the teeth (FO.05)",
     "if the transfer unit is the ACTIVITY EPISODE (excitation writes marks, one "
     "episode = one step, quiescence = recovery), consecutive quiescence-gap ratios "
     "sit on the time teeth {3/2,(3/2)^3,(3/2)^6} and episode-integrated energies "
     "on the partner teeth (2/3)^k -- the last untested aggregation level (all "
     "prior ladders ran burst-to-burst). Exploratory surface leakage (no named B)",
     "REAL committed catalogs (Blinkverse multi-source deduplicated + FAST 20240114A "
     "v5 times + CHIME Cat2; anti double-counting enforced): 8 sources clear the "
     "5-d episode gates; quiescence-gap Bonferroni p=1.0 (7 sources), episode-energy "
     "Bonferroni p=0.44 (7 sources); the flagged 10-d secondary agrees; largest "
     "single-source excursion FRB20190520B energy enrichment 3.0 at p=0.063 (not "
     "significant, single source) -> clean NULL. Known dominant systematic on "
     "record: observing-schedule selection", None,
     "search_target", "boundary recovery kernel (episode aggregation reading)",
     "search_target", "Blinkverse export + FAST 20240114A pol v5 + CHIME Cat2 "
     "(frb-ontology FO.05, prereg frb_ontology_v1.yaml; episode gap 5 d frozen)",
     "a tooth enrichment in quiescence gaps or episode energies survives the "
     "permutation null + placebo teeth in >=2 sources", "null"],
    ["FRB", "repeater/one-off leaf classes: exact two-mode morphology (FO.06)",
     "if the repeater/one-off dichotomy is a Z2 leaf classification (double cover), "
     "the only uniform-survey catalog shows EXACTLY two morphological modes in "
     "(log width, log bandwidth), membership is persistent, and first-detection "
     "morphology predicts repetition. Prime-2 diagnostic; a hit is DEFAULT astro "
     "(selection/exposure; Pleunis+2021)",
     "REAL CHIME Cat1 (474 clean first sub-bursts, 59 repeater bursts): morphology "
     "DOES predict repetition (CV-AUC 0.833 vs permutation null 0.493, p=0.001; "
     "repeater fraction per GMM mode 0.6% vs 19.9%, odds ratio 44.9 -- replicates "
     "Pleunis+2021, default reading astro/selection), BUT the TFPT-specific 'exactly "
     "two classes' prediction FAILS: BIC prefers k=3 (-1218.6) over k=2 (-1182.3) "
     "-> null for the leaf-class reading. Caveats on record: 400-800 MHz bandwidth "
     "censoring, exposure/beam selection uncorrected", None,
     "search_target", "Z2 leaf-class diagnostic (population morphology, prime-2 "
     "classification without a rate)",
     "search_target", "CHIME/FRB Catalog 1 (VizieR J/ApJS/257/59; frb-ontology "
     "FO.06, prereg frb_ontology_v1.yaml)",
     "BIC selects exactly k=2 AND morphology predicts repetition above the "
     "permutation null after selection correction", "null"],
    ["FRB", "operator-structure probes: covariance blocks + polarimetric null "
     "space + rank drop + time arrow (FO.07-10)",
     "the v1.3 strategy shift ('where is an operator forced NOT to mix states' "
     "instead of visible numbers): FO.07 character classes as BLOCK structure of "
     "the burst-observable correlation matrix (S8 on data); FO.08 FORBIDDEN "
     "region in (DOL, DOC) instead of peaks (S15 hole search); FO.09 delay-"
     "embedded dynamics on <= 3 modes ('rank 3, not 2, not 5'); FO.10 time "
     "arrow in within-session energy sequences (retarded/recovery direction; "
     "preregistered caveat: irreversibility is generic -- a hit is never support)",
     "REAL committed catalogs (prereg frb_ontology_v1.yaml v1.3 + dated v1.3.1 "
     "escalation gate): FO.07 block structure REAL on 5694 complete 10-observable "
     "v5 bursts (k=2 S_off=0.052 vs spectrum-preserving null 0.273, Bonferroni "
     "p=0.006) BUT the partition is exactly the standard Faraday/geometry-vs-"
     "emission sector split (Rand agreement 1.0) -> consistent/default astro, "
     "first-run hint on record; FO.08 NULL (6107 S/N>=20 bursts: largest empty "
     "disk r=0.302 vs marginal-preserving joint-permutation null median 0.551, "
     "p=1.0 -- visible voids are marginal-driven); FO.09 NULL (median Hankel "
     "effective rank 0 in Li+2021 and Zhang+2023 energy sessions -- memoryless, "
     "no 3-mode manifold; multivariate v5 leg flagged descriptive); FO.10 NULL "
     "-- a NEW bound: increment skewness 0.048/0.002 + Pomeau asymmetry "
     "-0.051/-0.006 over 1582/1032 increments, reversal-null Bonferroni p=1.0 -> "
     "within-session energy sequences are TIME-REVERSIBLE at catalog statistics; "
     "an arrow-free cascade bounds every directed-recovery reading of burst "
     "trains (and matches the FO.01 amplifier prediction); quake control open "
     "(USGS data gitignored)", None,
     "search_target", "operator-structure probes (S8-on-data blocks, S15 hole "
     "search, rank manifold, time arrow)",
     "search_target", "FAST 20240114A pol v5 + Li+2021 + Zhang+2023 "
     "(frb-ontology FO.07-10, prereg v1.3 + v1.3.1)",
     "a non-standard-sector covariance block, a joint forbidden Stokes region, "
     "a replicated rank-3 manifold, or a robust time arrow surviving its "
     "reversal null in >= 2 sources", "null"],
    # uhecr-energy-dsi (2026-07-07): the largest ln-E range in nature
    ["cosmic-ray", "UHECR energy-spectrum size-space DSI (Auger Open Data)",
     "log-periodic decoration of the cosmic-ray energy spectrum at the frozen "
     "kernel scale factor (omega = 2.5827 in ln E) -- the S7 size-space reading "
     "on the largest ln-E range in nature (0.1-144 EeV = 2.99 comb periods, "
     "combined SD750+SD1500 above their full-efficiency thresholds where the "
     "aperture is purely geometrical). Transduction B unproven -> exploratory "
     "surface probe; smooth null = piecewise-linear log-density with knots "
     "FROZEN at the published spectral features (second knee/ankle/instep/"
     "suppression), so the population-feature trap is closed by construction",
     "REAL Auger Open Data release 3 (Zenodo 10.5281/zenodo.10488964; 10% of "
     "published events): 21,571 SD1500 vertical + 54,434 SD750 events (deduped): "
     "kernel comb ABSENT -- Lambda = 0.15 (fitted eps 0.0018), MC p = 0.49, "
     "off-kernel rank p = 0.77; Z2 battery null after per-omega MC calibration "
     "((3/2)^3 p = 0.13, (3/2)^4 p = 0.78, Bonferroni 0.26; (3/2)^12 range-blind "
     "at 1.49 periods); audit note on record: the (3/2)^3 leg nominally fired at "
     "p = 0.0025 under the wrong (kernel-omega) null -- per-omega calibration "
     "dissolves it. Injection: 97% power at eps = 0.05, 23% at the predicted "
     "0.0173 -> the null constrains but does not kill the predicted amplitude "
     "(full-statistics Auger / TA+Auger is the dated decider)", None,
     "search_target", "size-space DSI (S7 reading; no clock map needed)",
     "search_target", "Pierre Auger Observatory Open Data release 3 "
     "(uhecr-energy-dsi, prereg uhecr_dsi_v1.yaml)",
     "a shared multiplicative comb at the frozen omega survives the MC + "
     "off-kernel rank on the combined spectrum AND replicates in the "
     "full-statistics Auger or TA spectrum", "null"],
    # cmb-primordial-logcomb (2026-07-07): the one natural bed with a MOTIVATED
    # S14 clock (inflation e-folds are a log-clock); typing against the published
    # Planck log-oscillation search (identical template in ln k).
    ["CMB", "primordial log-comb at the frozen omega (Planck feature search)",
     "if the seed epoch carried the seam recovery, its log-comb is imprinted in "
     "ln k: P(k) = P0(k)[1 + A cos(omega ln(k/k*) + phi)] with FROZEN omega = "
     "2.5827 (log10 = 0.412) and the QT.02 amplitude eps = 0.0173. The clock map "
     "is MOTIVATED here (e-folds; the only such natural bed, S14); the transfer "
     "of the comb into P(k) is an ASSUMED bridge (S15, flagged)",
     "PUBLISHED Planck 2018 X log-oscillation search (identical template): the "
     "frozen omega sits INSIDE the search prior (log10 omega in [0, 2.1]); no "
     "significant feature anywhere (best-fit Delta chi2 ~ 10 typed as noise/"
     "217-GHz artefact); 95% amplitude bound ~0.03 (Planck alone), ~0.029 "
     "combined Planck+SPT-3G+ACT -- a factor 1.7 ABOVE the predicted 0.0173. "
     "Reach: 3.12 comb periods over the full likelihood window (gate passed; "
     "the conservative 0.005-0.2 Mpc^-1 window alone is sub-gate at 1.52). "
     "Zero-parameter target: the frequency has no tunable freedom", None,
     "search_target", "boundary recovery kernel (dynamic, primordial ln k "
     "reading; motivated clock, assumed transfer bridge)",
     "search_target", "Planck 2018 X (A&A 641, A10) Sect. 7-8 + combined "
     "Planck/SPT-3G/ACT feature constraints (cmb-primordial-logcomb typing)",
     "a future 95% bound A_log(omega = 2.583) < 0.017 with no detection kills "
     "the primordial-DSI bridge; a phase-coherent detection AT the frozen omega "
     "escalates (CMB-S4-class combinations decide)", "data_limited"],
    ["X-ray", "recovery comb in magnetar outburst relaxation (omega=2.58)",
     "log-periodic comb at omega=2.58 in the post-outburst X-ray flux decay (wide ln t, stackable)",
     "REAL Swift-XRT/LSXPS data: 6 transient-magnetar outburst light curves; 2 clear the "
     ">=2.8-period ln-range gate (1E 1547.0-5408 at 3.54, SGR 1745-2900 at 2.93 periods); "
     "STACKED kernel omega=2.58 NOT special (p=0.99) -> clean NULL (magnetospheric/surface "
     "relaxation -> firewall caveat, not a horizon recovery; a 2-curve stack at the predicted "
     "~2% amplitude is a weak constraint)", None,
     "search_target", "boundary recovery kernel (dynamic, surface caveat)",
     "search_target", "Swift-XRT/LSXPS long-term light curves (6 curated transient magnetars)",
     "the omega=2.58 comb is special in a wide-ln-t magnetar flux-decay recovery", "null"],
    # Z2/Moebius double-cover readings of the SAME kernel (2026-07-06): an antiperiodic
    # (sheet-parity) comb has ZERO Fourier power at the kernel omega -> every kernel NULL
    # above is silent about it. Exploratory/unforced readings; same curves/detector as the
    # kernel rows -> an alternative READING, never an independent null/hit.
    ["cross-domain", "Z2/Moebius double-cover readings of the recovery comb "
     "((3/2)^3, (3/2)^4, (3/2)^12)",
     "if the comb carries the Z2 sheet parity per kernel period (antiperiodic, periodic only on "
     "the double cover), its power at omega=2.583 is exactly zero: fundamental at omega/2=1.291 "
     "(lambda=(3/2)^12), first odd harmonic at 3omega/2=3.874 ((3/2)^4); a half-period "
     "(sqrt-lambda per rung) clock sits at 2omega=5.165 ((3/2)^3). UNFORCED readings (no theory "
     "contract selects one) that close the antiperiodic blind spot of the kernel NULLs",
     "REAL data, ALL in-hand dynamic channels (2026-07-06): quake battery (6 USGS sequences, "
     "thousands of events) (3/2)^3 p=0.62 / (3/2)^4 p=0.45, Bonferroni global p=0.94 over 11 "
     "gated lambdas; A1 magnetar (3/2)^3 p=0.36 / (3/2)^4 p=0.27; A3 FAST/GBT FRB tails p=0.81 / "
     "p=0.60; A3b CHIME baseband p=0.21 / p=0.40; A4 GRB 22 afterglows p=0.42 / p=0.28; A5 ENT "
     "battery global p=0.095; PULSAR legs: PG.07 Vela-2024 p=0.27/0.23, PG.08 residuals null in "
     "all 3 glitches ((3/2)^3 p=1.0/0.10/0.17); repeater-cascade 9 gate-passing FRB sessions "
     "Fisher p=0.25/(3/2)^3, 0.14/(3/2)^4; crust cooling (3/2)^3 p=0.99 (n=6 gated); FRB "
     "microshots: (3/2)^3 is the FIRST reading to pass the per-lambda gate on the forest (3.22 "
     "periods) -> p=0.40 null; GW echoes cover the antiperiodic reading natively as the "
     "dphi=pi per-bounce phase x (2/3)^3 semantics in the Stage-1c battery (NO_VARIANT_ECHO, "
     "10 events) -> clean NULL everywhere testable (well-powered in quake + GRB + PG.08-J1740 + "
     "RC sessions). Two nominal excesses placebo-typed as artefacts, on record: PG.08 "
     "J1740-3015 (3/2)^4 raw p=0.0018 is a broad non-specific omega=3.6-4.0 bump (periodogram "
     "peak 3.73; placebos 3.6/3.73 equally significant); RC (3/2)^12 Fisher p=4e-4 is sub-gate "
     "(1.5-2.4 < 2.8 periods; placebo lambdas 60-300 equally extreme -> anti-conservative below "
     "the range gate). The antiperiodic FUNDAMENTAL (3/2)^12 (omega=1.29) is range-blind in ALL "
     "current data (needs 13.6 e-folds; widest curve Landers1992 has 13.1) -> data_limited on "
     "that leg", None,
     "search_target", "boundary recovery kernel (dynamic, Z2/Moebius sheet-parity reading)",
     "search_target", "recovery-comb-domains (quake/magnetar/GRB/FRB tails/ENT/microshots) + "
     "pulsar-glitch-recovery PG.07/PG.08 + repeater-cascade RC.02 + crust-cooling-comb + "
     "gw-ringdown-echo Stage-1c dphi=pi (shared stacked detector, per-omega gate)",
     "a Z2 reading ((3/2)^3, (3/2)^4 or (3/2)^12) is special vs its matched off-kernel pool AND "
     "its placebo controls in >=2 independent channels after look-elsewhere", "null"],
    ["pulsar", "recovery-waveform clock template (PG.04/QT.04)",
     "walled 2-mode clock: bend tau ratio 2.7095 + protected floor + wall (<=2 modes)",
     "GW single-event ringdown DONE (gw Stage 2): the bend is degenerate within one monotone recovery "
     "(two-mode R^2 gain ~1e-3); the discriminating signature is the CASCADE comb (omega=2.58), so the "
     "open lever is FRB-repeater tails / pulsar nu(t) post-glitch SEQUENCES, not summary Q/tau_d", None,
     "search_target", "exact discrete->dynamic clock rate(n)=-6ln(1-n/3) (v124/v126/v147)",
     "search_target", "FRB tails / pulsar nu(t) sequences (future); QT.04 template validated; GW Stage 2 done",
     "recovery-waveform SEQUENCE shows the cascade comb at omega=2.58 (or a single recovery fits >=3 modes)",
     "data_limited"],
    # crust-cooling comb (experiments/crust-cooling-comb): the floor-terminated 2nd data world
    ["X-ray", "recovery comb in neutron-star crust cooling (omega=2.583, superposed-epoch)",
     "log-periodic comb at omega=2pi/ln((3/2)^6)=2.583 + protected floor w0>0 in the kT_eff(t) crust-cooling relaxation (the floor-terminated 2nd data world)",
     "data_limited: 8 cooling episodes / 6 quasi-persistent transients (KS 1731-260, MXB 1659-29 x2, XTE J1701-462, EXO 0748-676, MAXI J0556-332 x2, Aql X-1; 67 kT_eff epochs transcribed from published tables). Every curve range-blind for the (3/2)^6 comb (best 2.46<2.8 periods) -> phase-incoherent kernel stack n_used=0; superposed-epoch pooled stack (3.08 periods) -> omega=2.583 NOT special (p=0.45, clean NULL, phase-aligned assumption); TFPT lambda-battery NULL after Bonferroni (global p=1.0); 7/8 episodes show a nonzero core-equilibrium floor. Injection on the real sampling: strong comb (eps=15%) recovered 100%, null FA 5%, but predicted eps~2% detected only 2% -> underpowered (density-poor)",
     None, "search_target", "boundary recovery kernel (dynamic, surface/non-horizon caveat)",
     "search_target", "published crust-cooling tables: Merritt+2016 (KS1731), Parikh+2019 (MXB1659), Fridriksson+2011 (XTEJ1701), Degenaar+2014 (EXO0748), Parikh+2017 (MAXIJ0556), Li/Ootes+2019 (AqlX-1)",
     "the omega=2.583 comb is special vs the off-kernel periodogram in the superposed-epoch stacked cooling ensemble",
     "data_limited"],
    # QPE recurrence search (experiments/qpe-recurrence, 2026-07-03): the frozen kernel
    # on quasi-periodic eruption timings -- the horizon-ADJACENT repeating transient
    # class (surface firewall, same legitimacy as recovery-comb A5).
    ["X-ray", "QPE recurrence kernel search (QPE.01-03)",
     "recurrence-ratio teeth {2/3, 8/27, 64/729}; walled-clock bend 2.7095 (wall N=3); "
     "comb omega=2.583 behind the >2.8-period ln-range gate (preregistered "
     "hypotheses/qpe_tfpt_v1.yaml before analysis)",
     "eRO-QPE2 (32 arrival times, arXiv:2604.09788 Table B.1) + GSN 069 (Miniutti+2023): "
     "QPE.01 NULL in both sources with quantified sensitivity (eRO-QPE2: 12 ratios, "
     "max|log r| = 0.022 dex, the 2/3 tooth is >17x the observed spread away -- a kernel "
     "step in the QPE clock is EXCLUDED, not merely unobserved); QPE.02 data_limited "
     "(3 monotone triplets; QPE clocks alternate by construction); QPE.03 range-blind "
     "(best 0.80 < 2.8 periods)",
     None, "search_target", "boundary-recovery residual (horizon-adjacent SURFACE channel; "
     "accretion/EMRI-mediated -- a hit would be universal-DSI coincidence, never TFPT "
     "confirmation)", "search_target",
     "qpe-recurrence (eRO-QPE2 arXiv:2604.09788; GSN 069 A&A 670 A93)",
     "a replicated tooth/clock excess in >= 2 QPE sources at q < 0.01, or a gate-passing "
     "secular-decay campaign with omega = 2.583 special", "null"],
    # HFQPO ladder (experiments/hfqpo-ladder): BH 3:2 pairs as the geometric relaxation ladder
    ["X-ray", "BH HFQPO 3:2 pairs + geometric-ladder discriminator (hfqpo-ladder H1-H3)",
     "ladder step 3/2 exact (N_fam=3); third tooth nu_3=(3/2)nu_u (661.5/414/252/363 Hz); "
     "NO integer harmonics",
     "4 pairs consistent with exact 3/2 (chi2 p=0.78) BUT J1859+226 breaks universality at "
     "9.2 sigma AND anchored selection null (Boutelier/Torok equal-rms window at the 3/2 "
     "crossing) manufactures the 4-of-5 cluster in 18.5% of trials -> cluster cheap; NO "
     "published x1.5 tooth search (teeth inside the searched RXTE band); only published "
     "third-frequency structures are integer lines (92=184/2, 34/68) favouring the "
     "GR-harmonic alternative; archival RXTE PCA reanalysis designed (prereg YAML), not run",
     None, "search_target", "relaxation-ladder step (non-canonical HFQPO mapping; coincidence-risk)",
     "search_target", "published RXTE tables: RM06, Motta+2014a/2022, Belloni+2012 (hfqpo-ladder)",
     "a >=4sigma third QPO at 1.5*nu_u with no integer line (ladder hit, [C]-tier) OR an "
     "integer line with no tooth (kernel reading dead)", "data_limited"],
    # strange-metal comb (experiments/strange-metal-comb): first laboratory bound on the comb
    ["condensed matter", "comb ripple on the strange-metal omega/T master curve (LSCO x=0.24)",
     "log-periodic ripple at omega=2.583, eps=0.0173 decorating the Planckian sigma1(omega/T) "
     "master curve (seam T=4c3 kappa = KMS/Planckian bound)",
     "data_limited: Michon+2023 open data (11227 pts, 2.92 comb periods, clears gate); "
     "omega=2.583 NOT special (primary p=0.30, detrend-robust; conservative per-T shift null "
     "p=0.68, 95% amplitude floor eps~0.19); lambda-battery Bonferroni p=0.063 null; "
     "injections: predicted eps=1.73% detected 0-25% -> underpowered at predicted amplitude; "
     "Drude controls (Au p=0.33, Cu p=0.14) quiet; Bi-2212 replication leg not publicly "
     "retrievable",
     None, "search_target", "boundary recovery kernel (dynamic, laboratory/non-horizon caveat)",
     "search_target", "Michon+2023 Nat.Commun. 14:3033 open data (Yareta DOI, CC-BY-4.0) + "
     "Ordal Au/Cu controls (strange-metal-comb)",
     "omega=2.583 special vs off-kernel periodogram in >=2 independent compounds",
     "data_limited"],
    # DSI false-positive control (experiments/dsi-false-positive-control): detector specificity
    # (extended 2026-07-02: Efimov ladder + glass/MCT textbook negative controls)
    ["cross-domain", "DSI false-positive control: frozen comb + textbook negative controls "
     "(Efimov, glass/MCT)",
     "kernel omega=2.583 must NOT fire on generic Omori/DSI relaxations; frozen bend 2.7095 "
     "must NOT be universal in boundary-less two-step relaxation",
     "4 aftershock cascades (17654 events) + 4 GOES flare sequences (1076 flares), 4/8 gated; "
     "PLUS Efimov ladder (Cs/7Li/39K, lambda=e^(pi/s0)=22.69) gated: kernel FP 0/5 over all "
     "gated DSI controls (Wilson95 [0,0.43]); Efimov measured 21.3+-1.1 is 8.9 sigma from "
     "TFPT lambda=11.39, detector 0/25 on the Efimov comb while localising omega=2.01; "
     "glass/MCT (7 systems): gamma spans [2.2,2.8] (4x meas. error), locked universal bend "
     "rejected ~4.9 sigma -> bend system-dependent, not generic; flares show own non-kernel "
     "DSI (lambda~2.9-3.9) -> detector specific, nulls informative",
     None, "search_target", "detector specificity control (universal-DSI base rate)",
     "search_target", "USGS ComCat + NGDC GOES XRS + Efimov cold-atom lit. + MCT lit. "
     "(dsi-false-positive-control)",
     "kernel fires on generic cascades well above 5%, OR Efimov inseparable from kernel, OR "
     "glassy gamma clusters on 2.7095", "consistent"],
    # comb-meta-limit (experiments/comb-meta-limit): first quantitative UL on the comb amplitude eps
    ["cross-domain", "meta-analytic UL on recovery-comb amplitude eps (omega=2.583)",
     "eps = exp(-pi^2/ln((3/2)^6)) = 0.0173 (~2%)",
     "boundary/horizon-scoped: data_limited (NO horizon channel yields an absolute eps -- GW single-event bend degenerate, FRB raw tails absent/linear-intensity, A2 sub-SNR); all-channel universal-DSI 95% UL eps<0.120 (HKSJ over surface log-flux A1/A4/A5, ~6.9x the 2% prediction); injection self-consistent (inject 5% -> recover 4.8%, UL 5.5%; coverage 0.92)",
     None, "search_target", "boundary recovery kernel (meta-analytic UL)",
     "search_target", "recovery-comb-domains A1/A4/A5 + pulsar PG.05 + GW/FRB (read-only); DL+Hartung-Knapp random-effects UL",
     "the boundary/horizon-scoped joint 95% UL on eps falls below 2% (soft constraint on the dynamic kernel)",
     "data_limited"],
    # ---- lab (experiments/lab-residuals) ----
    ["lab", "muon g-2 Delta a_mu (WP2020 dispersive)", "2.879e-9",
     "residual 2.62e-9+/-0.45", 0.58, "bridge", "HVP (dispersive)",
     "downstream_bridge", "Fermilab 2025 + WP2020", "residual incompatible with 2.879e-9", "consistent"],
    ["lab", "muon g-2 Delta a_mu (WP2025 lattice)", "2.879e-9",
     "residual 0.39e-9+/-0.64 (WP2025 sigma corrected to 62)", 3.92, "bridge", "HVP (lattice)",
     "downstream_bridge", "Fermilab 2025 + arXiv:2505.21476",
     "lattice HVP consolidates and residual stays ~0; dated 2026-07-02: a data-driven HVP "
     "consensus consistent with lattice/WP25 (CMD-3-side) kills the bridge (+3.9 sigma "
     "today); a KLOE-side dispersive consensus restores <1 sigma. Watch: MUonE (Phase-1 2025 "
     "analysed), BaBar 2026 pipi (stays KLOE-side), TI WP-3 ~2027-28", "tension"],
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
    ["channel", "Petz recovery + rank-one baby universe", "||T^n-P_inf||=(2/3)^{6n}; explicit Petz map recovers the protected code",
     "rank-one limit exact + Petz CPTP + KL on protected; free-ratio/degenerate neg controls pass", None,
     "search_target", "gapped transport / Petz map (companion to v221)", "search_target",
     "recovery-channel (numerical)",
     "a free ratio reaches the (2/3)^6 rate OR a degenerate spectrum keeps the rank-one limit", "consistent"],
    # ---- quantum testbed (experiments/quantum-testbed; internal-consistency, no data) ----
    ["quantum", "entanglement spectrum carries the kernel (QT.01)",
     "surprisals {6ln(3/2)=Delta, 6ln3}; protected DFS mode; I_n=(2/3)^{6n}",
     "exact: modular gap + ratio ln3/ln(3/2) + Schmidt recovery reproduced", None,
     "search_target", "Gaussian Gamma(t) entanglement (v161)", "search_target",
     "quantum-testbed (numerical)",
     "the entanglement spectrum does not carry the kernel", "consistent"],
    ["quantum", "quench discrete-scale-invariance (QT.02)",
     "log-periodic recovery at omega=2pi/ln lambda; eps~e^{-pi^2/ln lambda}",
     "DSI detected for energy gap (3/2)^6 (p~0.002), invisible for 3/2; control null", None,
     "search_target", "complex critical exponent (dynamical kernel)", "search_target",
     "quantum-testbed (numerical)",
     "a non-geometric ladder fakes the DSI at the kernel log-frequency", "consistent"],
    ["quantum", "walled clock + matched-filter discriminator (QT.04)",
     "exact rate(n)=-6ln(1-n/3): bend 2.7095, protected floor, wall at n=3",
     "exact identities hold; matched filter separates kernel (2.71) from non-kernel recovery", None,
     "search_target", "exact discrete->dynamic clock (v124/v126/v147)", "search_target",
     "quantum-testbed (numerical)",
     "the fixed-ratio template fails to separate kernel from non-kernel recoveries", "consistent"],
    ["quantum", "anyon MTC statistical phases (QT.05)",
     "16 sectors: 6 bosons/2 fermions(theta=-1)/8 anyons; spin quantum pi/4, braid pi/2; c=8",
     "exact MTC: phase quanta pi/4 (spin, 8th roots) + pi/2 (braiding), c=8 Gauss-Milgram, integrable S",
     None, "search_target", "carrier anyon MTC (v241/v242/v243)", "search_target",
     "quantum-testbed (numerical)",
     "the modular (S,T) data fails Verlinde/Gauss-Milgram or the phase quanta are not pi/4, pi/2", "consistent"],
    # qc-recovery-kernel: the recovery channel as an executable quantum circuit (analog tier)
    ["quantum", "recovery kernel as a quantum circuit (Kraus dilation)",
     "spec {1,(2/3)^6,(1/3)^6} + walled-clock bend ln3/ln(3/2)=2.7095 as a 5-qubit "
     "amplitude-damping dilation circuit (Perron mode gate-protected; energy + amplitude readings)",
     "Aer exact tier: per-step survivals exact to <=2.4e-15, free-ratio fit recovers the bend "
     "2.709511 (bias -3.8e-14); noisy tier (FakeBrisbane 127-qubit Eagle model, ISA depth 158): "
     "bend identifiable by circuit-native per-mode decode (min_shots_per_mode=256; mean bends "
     "2.46/2.69/2.68/2.65 over 256/1024/4096/16384 shots); the blind QT.04 combined free-ratio "
     "fit is weaker in the fresh run (detection 0%/0%/33%/67%; strict min_shots_identifiable=None), "
     "but first-seed one-step/two-step fits at 16384 are on-bend (2.787/2.806); protected floor "
     "retention 0.993; IBM hardware "
     "EXECUTED 2026-07-03 (ibm_marrakesh Heron R2, 13 circuits x 16384 shots, job "
     "d93ppd6vtlqs73ftdu5g): one-step survivals reproduced (2/3 at -4.2%, 1/3 at +8.9%), "
     "protected-floor retention 0.860, but the blind 12-block bend decode is floor/T1-biased "
     "(1.96 vs 2.71, -28%) -> hardware tier data_limited (needs DD/mitigation beyond the "
     "open plan); real Heron noise exceeds the Eagle fake-backend model", None,
     "search_target", "engineered seam-transfer channel (quantum-circuit analog of QT.04)",
     "not_applicable", "qc-recovery-kernel (Qiskit Aer + FakeBrisbane + ibm_marrakesh)",
     "the bend is not identifiable under the device noise model at any tested shot count",
     "consistent"],
    # qgeo-eit-soff (2026-07-06): the QGEO S_off observable on a REAL measured boundary
    # operator -- EIT measures the electrode ND map, the lab realisation of Lambda_Sigma.
    # Analog/instrument validation, same basket as qc-recovery-kernel (never TFPT evidence).
    ["quantum", "QGEO S_off on a real measured boundary operator (EIT analog channel)",
     "mu4 character block-diagonality of the boundary energy form (QGEO.SYM.01 operator "
     "form, v198/v201/v210): S_off = sum_{r!=s}||P_r R P_s||^2/||R||^2 at the instrument "
     "floor for mu4-marked geometry; generic anisotropy leaks isotropically over the "
     "harmonic lags (forbidden fraction ~12/15); simulation contract "
     "qgeo_soff_reconstruction.py sets the requirement ~1e-3 relative spectral precision",
     "REAL KIT4 open EIT archive (Zenodo 10.5281/zenodo.1203914; 38 tank measurements, 16 "
     "electrodes, 79 injections each): H1 PASS -- the homogeneous tank realises a mu4-block-"
     "diagonal measured ND map at the instrument floor (S_off = 7.6e-5, clock commutator "
     "1.5e-2, reciprocity 5.3e-3 = the sigma~1e-3 dial met on real hardware); H2 PASS -- all "
     "28 anisotropic targets leak with the generic isotropic signature (forbidden fraction "
     "0.87-1.00 vs expected 0.8), none fakes a mu4 positive; 9 centered/annular targets are "
     "rotation-invariant-like and sit near the floor (photo-verified v1.1 anisotropy gate, "
     "dated addendum). v1.2 (same day, frozen acceptance protocol for the lab run): all "
     "metrics moved to the DIFFERENCE operator Delta = R_case - R_hom with the absolute-"
     "leakage dial leak(m)=sqrt(A_off_m/floor_m) (split-half noise floor), C2/C4/C8/C16 "
     "group fingerprint (H3 class = C4 holds AND C8 broken, so a centered ring can never "
     "fake it), clock recovery over all 15 rotations, D4 reflection score, NtD/DtN-proxy "
     "robustness (commutant transfer verified 1e-15), delta^2 break-scaling verified "
     "(exponent 1.998), blind protocol + 9-step break ladder preregistered. Archive re-run: "
     "0 C4-positives (as required, no mu4 target exists), geometry-blind classifier 34/37 "
     "vs documented geometry (3 mismatches physically real: 6.1 foam joints/clamps); "
     "between-session floor identified as the H3-relevant systematic (repeat-homogeneous "
     "requirement frozen). H3 (the decisive mu4-POSITIVE 4-inclusion configuration at "
     "j*pi/2) is NOT in the archive -> data_limited, preregistered as the future "
     "measurement any KIT4-class lab can run", None,
     "search_target", "analog boundary-operator realisation of the QGEO seam premise",
     "not_applicable", "qgeo-eit-soff (KIT4 open 2D EIT, Hauptmann+ arXiv:1704.01178)",
     "H1 or H2 fail at KIT4-class precision (observable not realisable), or the future "
     "mu4-positive H3 leaks at demonstrated instrument precision (analog path closes)",
     "consistent"],
    # ---- shared seed (one phi0 -> four observables) ----
    ["seed", "shared seed phi0", "phi0 = 1/(6pi)+3/(256pi^4) = 0.05317",
     "4 observables imply same phi0, chi2/dof=1.23 (dominant leg theta13, -1.80 sigma). "
     "v4 (2026-07-06) DECODER test on the raw channels: ONE latent u = 0.05292 fits "
     "beta/Omega_b/theta13(reactor)/Cabibbo simultaneously (chi2 = 4.10, dof 3, p = 0.25; "
     "frozen phi0: chi2 = 4.51, dof 4, p = 0.34); AIC prefers the 1-parameter shared decoder "
     "over the saturated per-channel model (6.1 < 8.0); 0/14 single-swap neighbour link "
     "decoders (4pi -> pi..16pi, slope, exponent 5/6 -> 1/2..7/6, Cabibbo link) beat it, and "
     "it sits at the 0.0th percentile of 2000 equal-complexity random placebo decoders "
     "(median placebo chi2 ~ 1200) -- the cross-channel RATIOS are TFPT-specific, an "
     "architecture consistency, not proof. v5 (same day) LOO FORWARD TEST: every "
     "channel predicted by the other three within 2.0 sigma (worst leg theta13 at "
     "-1.99, the known crack candidate); FLAGSHIP dated band: Cabibbo + theta13 + "
     "Omega_b predict beta = 0.2413 +/- 0.0018 deg (~40x narrower than ACT's current "
     "error; ACT DR6 sits at z=-0.36) -- LiteBIRD/Simons Observatory (sigma~0.02 deg) "
     "test this band BLIND, beta never entered the fit. v6 (same day) RETARDED-TAIL "
     "ABLATION: u_tree = 1/(6pi) vs u_ret = 1/(6pi) + 3/(256pi^4) (the specific "
     "topological +0.23% correction) is UNDECIDABLE today (|Delta chi2| = 0.30, tail "
     "< 0.3 sigma in every channel); dated prequential deciders: sigma(V_us) ~ 8e-5 "
     "(kaon/lattice, the realistic one), sigma(sin2th13) ~ 1.8e-5, sigma(omega_b h2) "
     "~ 1.7e-5; beta can NEVER see the tail (needs 1.8e-4 deg). Frozen crack: >= 2 "
     "channels preferring the tree seed at >= 3 sigma kills the retarded reading",
     None, "prediction", "one retarded seed", "prediction_of_record",
     "seed-consistency (v1-v6) + cmb-birefringence-seed (shared_seed)",
     "two independent seed legs >3 sigma, or one leg >5 sigma; theta13 alone >3 sigma flags "
     "PMNS theta13 as transfer-corrected; v4: >2 neighbour decoders beating the TFPT links "
     "or placebo percentile >10% would void the architecture reading", "consistent"],
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
    # ---- EM fixed point alpha^-1 (the headline compiler prediction; v3_em_alpha) ----
    ["EM", "fine-structure constant alpha^-1",
     "137.0359992168 (unique positive root of the boundary U(1) Ward identity F_U(1)=0; M=41 index, v3)",
     "CODATA 2022 137.035999177(21)", 1.9, "prediction", "EM fixed point (compiler primitive)",
     "prediction_of_record", "CODATA 2022 (also scored live in verification/v307_data_watchdog)",
     "alpha^-1 outside the CODATA window at >3 sigma", "consistent"],
    # ---- Lambda/H0 engine (lambda-h0-engine) ----
    ["cosmo", "Lambda hierarchy rho_Lambda/M_pl^4", "(3/256pi^4) e^-2ainv = 122.948 orders",
     "measured 122.943 orders (dev 0.004 orders, NOT a pull_sigma)", None, "prediction",
     "EM fixed point alpha^-1", "prediction_of_record", "Planck Omega_Lambda + H0",
     "measured Lambda orders differ from 122.95 by >1 order", "consistent"],
    ["cosmo", "S_dS rho_Lambda = 32 pi^4", "1/(128 c3^4) = 32 pi^4 (exact)",
     "dimensionless identity", None, "prediction", "de Sitter entropy x Lambda",
     "prediction_of_record", "internal identity", "identity fails", "consistent"],
    # flat-budget closure (2026-07-03): zero-dial composite; the Omega_c leg is the
    # 2026-07-02 NUMEROLOGY-FLAGGED Nebenbefund (post-hoc, single p/q<=12 census hit,
    # ALTERNATIVE reading to the axion-spine DM branch -- see OVERRIDES, never both).
    ["cosmo", "flat LambdaCDM budget closure (H0, Omega_m, t0)",
     "zero-dial closure {Omega_b=phi0(1-1/4pi) [frozen], Omega_c=(2/7)(1-1/4pi) [flagged "
     "candidate], rho_L/Mbar^4=(3/4pi^2)e^-2ainv [frozen], Sigma m_nu=0.0588 eV [v468 "
     "route]} + flatness -> H0=67.15 km/s/Mpc, Omega_m=0.3133, Omega_L=0.6866, t0=13.86 Gyr",
     "H0: Planck18 -0.39 sigma, SH0ES22 -5.67 sigma (the parameter-free PLANCK side of the "
     "Hubble tension), DESI DR2 BAO+CMB -2.16 sigma; Omega_m -0.27, Omega_L +0.26, "
     "Omega_c/Omega_b +0.14; honest stress: omega_b -2.02 (BBN-only D/H -0.73 -- the "
     "stress is CMB-side), omega_c -1.19, derived t0 +2.9 -- one correlated low-h "
     "direction, not additive", None, "pattern_candidate",
     "flat FLRW budget closure (phi0 seed + alpha Lambda engine + nu floor + flagged "
     "Omega_c leg)", "downstream_bridge",
     "experiments/tfpt-discovery/flat_budget_closure.py (Planck 2018 TT,TE,EE+lowE+lensing; "
     "SH0ES 2022; DESI DR2; BBN D/H LUNA)",
     "systematics-converged local H0 >= 71 with broken CMB/BAO concordance, or omega_c "
     "hardened >= 3 sigma away from 0.1186 -- kills the closure pattern only (frozen "
     "Omega_b/Lambda records untouched)", "consistent"],
    # S8 forecast from the same closure (2026-07-03): the budget's first STRUCTURE
    # observable -- takes the KiDS/CMB side of the 2026 S8 bifurcation. Shares every
    # leg with the flat-budget row (phi0_seed + flagged Omega_c leg) -- never a new hit.
    ["cosmo", "S8 forecast from the flat budget (structure side)",
     "budget geometry (H0=67.15, omega_b=0.02207, omega_c=0.11857, Sigma m_nu=0.0588 eV) "
     "+ CAMB -> sigma8 = 0.807, S8 = 0.824 (geometry-only, Planck A_s/n_s imported; "
     "profiled-N_star branch identical 0.824; frozen N_star=51.4 branch 0.754 = the known "
     "A_s branch stress in structure form)",
     "2026 S8 bifurcation: Combined CMB 0.836(13) -0.89 sigma, Planck18 0.832(13) -0.59, "
     "KiDS-Legacy 0.815(19) +0.49, HSC Y3 (DESI-recal) 0.805(18) +1.08, DES Y6 3x2pt "
     "0.789(12) +2.95 -- TFPT sits on the CMB/KiDS side and predicts the DES-vs-KiDS "
     "split resolves as DES-side systematics (mirror of the Hubble-side positioning)",
     None, "pattern_candidate",
     "flat-budget closure + inflation A_s branch (CAMB transfer)",
     "downstream_bridge",
     "experiments/tfpt-discovery/s8_budget_forecast.py (CAMB 1.6.6; KiDS-Legacy 2025, "
     "DES Y6 2026, arXiv:2602.12238 review)",
     "a systematics-converged lensing S8 <= 0.79 replicated across KiDS/DES/HSC/LSST at "
     ">= 5 sigma from the budget value -- kills the closure pattern only", "consistent"],
    # ---- dark-energy watchdog (P2) ----
    ["cosmo", "dark-energy equation of state w", "w = -1 (cosmological constant)",
     "DESI DR2 overlap-aware: strongest single combo 4.4 sigma (naive product 6.6 sigma is "
     "spurious); 2026 timeline (before DR3): DES-Dovekie recalibration (arXiv:2511.07517) "
     "cuts 4.2->3.2 sigma (calibration error in DES-SN5YR); Bayesian reanalysis "
     "(arXiv:2603.05472) eliminates the DESI+CMB-only preference (ln B=-0.57) -- the "
     "preference is dissolving as w=-1 requires; Union3 frequentist 3.8 sigma (2.23 Bayesian) "
     "remains",
     None, "prediction", "Lambda = constant vacuum", "prediction_of_record",
     "dark-energy-w-watchdog (DESI DR2, overlap-aware)",
     "w != -1 at >=5 sigma in a single systematics-controlled overlap-aware combination",
     "data_limited"],
    # ---- exact-fixed-point watchdog (experiments/fixed-point-watchdog) ----
    # pincer overlaps the w row (alternative_group w_de_eos) AND the sum-m_nu row
    # (independence_group nu_mass_floor) -- never an independent hit; see OVERRIDES.
    ["cosmo", "joint fixed point (w, Sigma m_nu) pincer",
     "(w0, wa, Sigma m_nu) = (-1, 0, 0.0588 eV) jointly",
     "DESI DR2 2025 model-dependent squeeze: LCDM eff-mass posterior puts the 0.0588 eV floor "
     "at +3.1 sigma; w0waCDM relaxes nu (+0.65 sigma) but puts (w0,wa)=(-1,0) at 3.1-4.4 sigma; "
     "joint ~3.7 sigma (below 5-sigma kill)", None, "prediction",
     "Lambda constant + NO mass floor (joint point; fixed-point-watchdog)",
     "prediction_of_record", "fixed-point-watchdog (DESI DR2 arXiv:2503.14744 + 2503.14738)",
     "joint (w=-1, 0.0588 eV) excluded at >=5 sigma under BOTH model readings", "tension"],
    ["lab", "alpha-Lambda drift lock (alpha_dot/alpha = 0)",
     "d ln rho_Lambda/dt = 2 alpha^-1 (alpha_dot/alpha), amplifier 274.07; both drifts exactly zero",
     "PTB Yb+ alpha_dot/alpha = 1.8(2.5)e-19/yr -> |d ln Lambda/dt| < 1.4e-16/yr; DESI w0wa "
     "face value needs 3-7e-11/yr -> the lock excludes 'TFPT + real w(z)' by ~10^5.7", None,
     "prediction", "alpha-Lambda lock (v60/v274)",
     "prediction_of_record", "fixed-point-watchdog (Filzinger+ PRL 130 253001)",
     "confirmed alpha drift != 0 or confirmed Lambda drift violating the lock", "consistent"],
    # ---- neutrino absolute sector (P2) ----
    ["neutrino", "sum m_nu", "Sigma m_nu = 5.88e-2 eV (normal ordering)",
     "DESI DR2 2025: LCDM 95% UL 0.0642 eV (floor still inside), but the effective-mass "
     "posterior -0.101 +0.047/-0.056 eV puts the 0.0588 eV floor at +3.1 sigma "
     "(model-dependent squeeze; w0waCDM relaxes to 0.163 eV / +0.65 sigma)", None,
     "prediction", "PMNS / mass scale",
     "prediction_of_record", "DESI DR2 (arXiv:2503.14744) + CMB; KATRIN",
     "Sigma m_nu excluded or inverted ordering", "tension"],
    ["neutrino", "m_betabeta (0vbb)", "m_bb = 1.52e-3 eV (normal ordering)",
     "LEGEND/nEXO sensitivity ~10-20 meV (not yet reached)", None, "prediction", "Majorana mass",
     "prediction_of_record", "LEGEND-1000 / nEXO", "a 0vbb signal incompatible with 1.5 meV NO", "data_limited"],
    ["neutrino", "delta_nu_CP", "240 deg (4 pi/3) = delta_CKM_lead + pi (v231/v233 sheet relation)",
     "NuFIT 6.0 NO best fit 212 +26/-41 deg (CP-violating; CP conservation only within 1 sigma)", 1.08,
     "prediction", "PMNS CP phase (hexagonal mu6 unit, sheet-split)", "prediction_of_record",
     "neutrino-mixing (NuFIT 6.0); sharpens with DUNE/HyperK",
     "delta_nu_CP excludes 240 deg at >=3 sigma", "consistent"],
    # sterile-neutrino dissolution watchdog (fixed-point-watchdog axis D): N_fam=3 leaves
    # no slot for a 4th light state -- the short-baseline anomalies must dissolve.
    ["lab", "sterile-neutrino dissolution watchdog (N_fam=3)",
     "N_fam = 3 exactly (no 4th light state)",
     "MicroBooNE two-beam (Nature 648, 64-69 (2025)) excludes single-sterile LSND/MiniBooNE "
     "at 95% CL and cuts into gallium/BEST space; gallium deficit persists unexplained (no "
     "oscillation signature); JSNS2 running (no excess); SBND+ICARUS decide this decade",
     None, "prediction", "E8 family counting (D5+A3+mu4; no spare slot)",
     "prediction_of_record",
     "fixed-point-watchdog axis D (Nature 648 (2025); arXiv:2512.07159, 2602.06274; SBN 2026)",
     "any confirmed sterile oscillation signal at >= 5 sigma (systematics-controlled; "
     "e.g. joint SBND+ICARUS or JSNS2-II)", "consistent"],
    # ---- fixed-point-watchdog axis E (2026-07-03): Cabibbo dissolution + the NEW
    # parameter-free neutron lifetime. Both legs read the SAME frozen lambda_C
    # (phi0-derived) -> independence_group phi0_seed, never independent hits.
    ["CKM", "Cabibbo first-row dissolution watchdog (axis E)",
     "lambda_C = sqrt(phi0(1-phi0)) = 0.2243762 exact + exact unitarity => V_ud = 0.97450; "
     "first-row deficit must dissolve on the V_ud/nuclear side",
     "PDG26 first row 0.9983(7) (+2.4 sigma deficit); lambda_C dead-on the kaon average "
     "(+0.08 sigma, S=2.5), BETWEEN Kl3 (+2.03) and Kmu2 (-1.63) -> routes must converge on "
     "0.22438; V_ud: superallowed is the outlier (+2.58) while neutron (PDG +0.10, best "
     "+0.87) and pion beta (+0.22) agree with unitarity",
     None, "prediction", "frozen v84 CKM assembly (exact unitarity)",
     "prediction_of_record",
     "fixed-point-watchdog axis E (PDG 2026 Vud/Vus review; PIONEER/lattice f+(0) decide)",
     "converged all-route V_us (S~1) with |V_us-0.224376| >= 5 sigma, or a "
     "systematics-converged first-row deficit >= 5 sigma", "consistent"],
    ["lab", "neutron lifetime tau_n (parameter-free, beam-bottle side)",
     "tau_n = 4906.4(1.7) s / (V_ud^2 (1+3 gA^2)) = 877.53 +- 0.71 s (V_ud exact from "
     "unitarity; gA = 1.27641(56) PERKEO III) -- TFPT takes the BOTTLE side and forbids "
     "the n->chi dark-decay exit (no E8 slot, same counting as the sterile axis)",
     "UCNtau final (bottle) 877.82(30) -0.38 sigma; magnetic/grav storage avg 878.15(20) "
     "-0.85 sigma; beam average (proton counting) 888.1(2.0) -4.98 sigma; J-PARC "
     "ELECTRON-counting beam 877.2(4.0) +0.08 sigma -- the ~4-sigma beam-bottle puzzle "
     "resolves as a proton-counting-beam systematic",
     -0.38, "prediction", "CMS master formula (arXiv:1907.06737) + frozen lambda_C",
     "prediction_of_record",
     "fixed-point-watchdog axis E (UCNtau arXiv:2409.05560; J-PARC arXiv:2412.19519; "
     "NIST BL2/BL3 + tauSPECT decide)",
     "bottle tau_n drifting >= 5 sigma from 877.5 s at fixed gA, or a confirmed "
     "beam-bottle split established as real new physics (dark decay) at >= 5 sigma",
     "consistent"],
    # ---- fixed-point-watchdog axis F (2026-07-03): X17 dissolution ----
    ["lab", "X17 dissolution watchdog (no E8 slot)",
     "no compiler slot for a ~17 MeV boson -> the ATOMKI anomaly family (MX = 16.85(4) "
     "MeV in 8Be/4He/12C) must dissolve",
     "MEG II (EPJ C 85 (2025) 763): NO signal in the same 7Li(p,e+e-)8Be reaction "
     "(R_17.6 < 1.8e-6 at 90% CL; still ~1.5 sigma compatible with ATOMKI per Barducci+ "
     "JHEP 04 (2025) 035); PADME Run III (JHEP 11 (2025) 007): background-consistent "
     "except a 1.8-2.0 sigma GLOBAL excess at 16.90 MeV; PADME Run IV (2025/26) decisive",
     None, "prediction", "E8 carrier counting (no light-boson slot)",
     "prediction_of_record",
     "fixed-point-watchdog axis F (MEG II 2025; PADME Run III 2025)",
     "a confirmed >= 5 sigma X17 resonance, systematics-controlled and replicated "
     "outside ATOMKI", "consistent"],
    # ---- fixed-point-watchdog axis G (2026-07-03): R_D(*) dissolution ----
    ["CKM", "R_D(*) lepton-universality dissolution watchdog",
     "exact unitary CKM assembly + no light charged mediator slot => b->c tau nu "
     "universality must return to SM (R_D = 0.296, R_D* = 0.254)",
     "HFLAV CKM 2025: R_D = 0.358(24) (+2.5 sigma), R_D* = 0.281(11) (+2.2 sigma), "
     "COMBINED 3.8 sigma (3.5 with FLAG24 lattice SM) -- the most significant standing "
     "dissolution target; Belle II full dataset + LHCb Run 3 decide",
     3.8, "prediction", "frozen CKM assembly + compiler content (no leptoquark/W' slot)",
     "prediction_of_record",
     "fixed-point-watchdog axis G (HFLAV CKM25; LHCb PRL 134 061801; Belle II PRD 112 032010)",
     "R_D(*) excess confirmed at >= 5 sigma with independent tagging and consolidated "
     "SM form factors", "tension"],
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
    ["lab", "leptogenesis eta_B (scalaron-decuple)", "M1=M_scal phi0^2/A_Lambda=8.6e9 GeV, A_Lambda=10, delta_CP=4pi/3",
     "full BDP ODE solve: eta_B=6.5e-10 at the frozen M1 (ratio 1.07; kappa_f=0.092)", None, "bridge",
     "leptogenesis interface (Boltzmann)", "downstream_bridge", "ftransfer/leptogenesis_boltzmann/fboltzmann_solve.py",
     "flavored Boltzmann misses eta_B=6.1e-10 by >3x", "consistent"],
    ["lab", "charged-lepton Koide ratio Q (F_pole)",
     "Q* = 2/3 = 0.666667 (democratic |Z2|/N_fam; realised by the source->pole transfer)",
     "PDG pole masses Q = 0.6666645 (= 2/3 to 3e-6, the famous coincidence)", None, "bridge",
     "F_pole source->pole [C] (multiplier (2/3)^6; v93/v183) -- transfer conditional, not closed",
     "downstream_bridge", "PDG charged-lepton pole masses; ftransfer/koide_source_to_pole",
     "Q_pole drifts off 2/3 at >3 sigma", "consistent"],
    # kill-window sharpening of the row above (independence_group koide_q_pole; see OVERRIDES)
    ["lab", "Koide Q=2/3 tau-mass kill window", "m_tau(Q=2/3) = 1776.9690 MeV",
     "PDG 2024/25 Q=0.6666645(51) -> -0.43 sigma; Belle II 2023 +0.86 sigma; 5-sigma kill "
     "needs sigma(m_tau) 0.008-0.024 MeV", None, "bridge",
     "F_pole transfer [C] (kill window sharpening of the existing Koide row)",
     "downstream_bridge", "fixed-point-watchdog (PDG + Belle II arXiv:2305.19116)",
     "|m_tau - 1776.9690| >= 5 sigma(m_tau)", "consistent"],
    ["lab", "proton/electron mass ratio m_p/m_e (F_QCD)",
     "~1836.15 (QCD/EW cross-sector, carrier b3=-7 run, v262); exact 1920-84+0.151=1836.151 [O] numerology-flagged",
     "PDG 1836.15267", None, "bridge",
     "F_QCD cross-sector matching [O] -- frontier keeps it OPEN (the exact combination would invite "
     "the numerology charge); only the b3=-7 QCD-run structure is [I]",
     "downstream_bridge", "PDG; ftransfer/qcd_matching_mp_me",
     "a closed first-principles m_p/m_e disagrees with 1836.15", "data_limited"],
    ["EW", "Higgs near-criticality", "lambda(M_Pl)~0, beta_lambda(M_Pl)~0 (double-critical)",
     "Buttazzo2013 fit: lambda(M_Pl)=-0.0143+/-0.0057, beta_lambda=+1.9e-4 (metastable 2.5 sigma)",
     None, "bridge", "seam free-field boundary",
     "downstream_bridge", "higgs-criticality (Buttazzo 2013 NNLO fit)",
     "RGE pull off the double-critical surface at >5 sigma", "consistent"],
    # ---- problem_b black-hole-cosmology signatures (new; experiments/ standalone) ----
    ["cosmo", "CCBH cosmological coupling k=3 (w=-1)", "k = -3 w_in = 3 (de Sitter seam interior)",
     "Farrah+2023 k=3.11+/-0.79 (k consistent; CCBH-as-DE interpretation contested)", -0.14, "bridge",
     "BH interior EoS -> coupling (Croker-Weiner)", "downstream_bridge",
     "Farrah+2023 ApJL 944 L31 (disputed: Lacy/Amendola/Andrae&El-Badry/Mistele)",
     "robust k != 3 at >=3 sigma in a controlled SMBH-growth sample", "data_limited"],
    ["GW", "ECO compactness C=3/8 (gravastar echo)",
     "C=3/8=Q_geom(Nariai); OBSERVED echo delay ~0.76 ms (62 Msun x (1+z), z=0.09), ratio <= (2/3)^6",
     "no ECO echo detected; ringdown consistent with Kerr (rational 3/8 match is [C])", None, "bridge",
     "Nariai horizon-root quotient / ECO reflectivity", "search_target",
     "Jampolski-Rezzolla 2026 (arXiv:2509.15302) + LVK ringdown",
     "a C=3/8 horizonless echo (predicted delay + (2/3)^6 damping) excluded across high-SNR ringdowns",
     "data_limited"],
    ["cosmo", "cosmic spin handedness (parity)", "approximate parity (tiny mu4/PSL(2,C) remnant)",
     "Shamir JADES 158:105 ~3.3 sigma monopole (likely MW-aberration dipole; Galaxy Zoo isotropic)",
     None, "frontier", "global boundary orientation", "search_target",
     "Shamir 2025 MNRAS 538 76 (JWST JADES); Land+2008 Galaxy Zoo",
     "a parity-odd global spin monopole surviving MW-aberration + selection systematics across surveys",
     "data_limited"],
    # cosmic number-count dipole (experiments/cosmic-dipole-watchdog, 2026-07-03): the
    # Ellis-Baldwin excess vs the FLRW foundation of the cosmology branch. Same isotropy
    # watchdog family as handedness (different observable, independent data).
    ["cosmo", "cosmic number-count dipole (Ellis-Baldwin) watchdog",
     "FLRW isotropy + tiny mu4/PSL(2,C) remnant: NO intrinsic super-Hubble matter dipole "
     "-> the excess must dissolve into clustering/mask/selection systematics",
     "CatWISE2020: D = 15.54e-3 vs kinematic 7.4e-3 (x2.1, CMB-aligned within ~27 deg); "
     "claimed 4.4-5.7 sigma (Secrest+21/22, Dam+23, Wagenveld+25 residual 5.4 sigma; RMP "
     "97 041001 (2025): '>5 sigma'); clustering/mask-aware FLASK reassessment "
     "(arXiv:2511.00822): 3.27-3.63 sigma -- the ERROR BUDGET is the open question",
     None, "frontier", "FLRW foundation of the flat budget / Lambda-H0 engine",
     "search_target",
     "cosmic-dipole-watchdog (CatWISE2020, NVSS/MALS; LSST/Euclid/SKA decide)",
     "a clustering-marginalized, mask-controlled non-kinematic dipole at >= 5 sigma "
     "replicated in >= 2 independent selections -> strikes the FLRW-based cosmology "
     "branch (not the compiler core)", "data_limited"],
    # frozen-eta BBN lithium watchdog (experiments/bbn-lithium-watchdog, 2026-07-03):
    # the 20-year lithium problem under the parameter-free eta. UNIVERSAL to all
    # LCDM-eta cosmologies (weak discriminative power); D/H + Yp legs share phi0_seed.
    ["cosmo", "primordial 7Li at the frozen eta (lithium watchdog)",
     "eta10 = 6.04 frozen (Omega_b = phi0(1-1/4pi), budget h) -> 7Li/H = 5.31(21)e-10 "
     "(PRIMAT rescaled); NO eta dial and NO exotic-BBN slot => the lithium problem must "
     "resolve astrophysically (stellar depletion), never by shifting eta or new BBN physics",
     "Spite plateau 1.58(31)e-10 -> overpredicted x3.36 (+9.9 sigma) = the UNIVERSAL "
     "cosmological lithium problem (shared by Planck-LCDM, NOT TFPT-specific); the anchors "
     "hold at the frozen eta: D/H (Cooke+2018) -0.3 sigma, Yp (Aver+2021) +0.5 sigma",
     9.9, "prediction", "frozen Omega_b record (v84) + flat-budget h + PRIMAT BBN",
     "prediction_of_record",
     "bbn-lithium-watchdog (Pitrou+2018 PRIMAT; Sbordone+2010; Cooke+2018; Aver+2021)",
     "an established Li resolution requiring eta >= 5 sigma off the TFPT omega_b, or "
     "confirmed new BBN-era physics at >= 5 sigma, or D/H pulling >= 5 sigma", "tension"],
    # ---- spectral action / NCG matter content (v244/v245); RGE-confronted in gauge-unification ----
    ["EW", "Weinberg angle sin^2 th_W (spectral scale)", "3/8 (NCG/SU(5) tree, v245)",
     "3/8 is the standard SU(5)/SO(10) GUT value; SM 1-loop run gives alpha1=alpha2 @ ~1e13 GeV "
     "but alpha3 misses 13%, and 3/8->sin^2_W(M_Z)=0.2076 vs 0.23122 (universal ~10% GQW gap, "
     "needs SUSY/thresholds; NOT TFPT-specific)", None,
     "bridge", "spectral-action unification g3=g2=sqrt(5/3)g1",
     "downstream_bridge", "gauge-unification (1/2-loop RGE) vs PDG; Chamseddine-Connes-Marcolli (v245)",
     "couplings unify with a DIFFERENT normalisation than 3/8 (sqrt(5/3))", "data_limited"],
    ["EW", "carrier matter = one anomaly-free generation", "SO(10) 16 = SM gen, sum Y=sum Y^3=0",
     "exact: 16 = one generation, all four anomalies cancel, Higgs=(1,2)_{1/2}", None,
     "bridge", "carrier half-spinor (v244/v245)",
     "not_applicable", "spectral-action matter content (v245, internal identity)",
     "the carrier 16 fails to be an anomaly-free SM generation", "consistent"],
    # ---- proton decay (experiments/proton-decay): optional gauged carrier-PS->SO(10) UV branch B ----
    ["proton decay",
     "proton lifetime tau_p (p->e+pi0), carrier-PS->SO(10) branch B",
     "+(15,1,1) [E8's single 45]: tau_p(e+pi0)=1.46e35 yr (1-loop)/7.7e33 (2-loop); minimal 16H=4.2e33 (excluded); M_PS=scalaron scale",
     "minimal 16H KILLED by Super-K (>2.4e34); +(15,1,1) clears at 1-loop but 2-loop 7.7e33<Super-K = latent tension; Hyper-K ~1e35 (e+pi0) decisive this decade; p->nubar K+ subdominant (data_limited)",
     None, "bridge",
     "carrier-PS->SO(10) dim-6 X,Y gauge exchange at M_GUT (optional UV branch B; v266/v249)",
     "downstream_bridge",
     "proton-decay (2-step RGE) vs Super-K PRD102 112011 (e+pi0)/PRD90 072005 (nuK+); Hyper-K arXiv:1805.04163, DUNE arXiv:2503.23291, JUNO CPC47 113002",
     "Hyper-K reaches ~1e35 yr (p->e+pi0) with no signal, or the 2-loop-low M_GUT holds -> +(15,1,1) excluded (last E8-allowed content; minimal dead, 126 E8-forbidden -> PS branch B killed)",
     "tension"],
    # ---- extended signatures (experiments/extended-signatures) ----
    ["FRB", "joint echo x polarisation (EXT.1)", "echo 64/729 AND mu4/PA in same source",
     "data_limited without FAST/Blinkverse on disk; Fisher stack when data present", None,
     "search_target", "boundary recovery + mu4 clock (cross-correlation)",
     "search_target", "extended-signatures/frb_joint",
     ">=2 sources with simultaneous echo+PA p<0.05 replicated", "data_limited"],
    ["FRB", "anyon pi/4 EVPA comb (EXT.2)", "m=4 spacing 45 deg (QT.05 spin quantum pi/4)",
     "injection validated; real PA null or m=2 dominance (FRB.08 reinterpretation)", None,
     "search_target", "carrier anyon MTC (v241-v243)",
     "search_target", "extended-signatures/frb_anyon",
     "replicated pi/4 comb in >=2 polarised repeaters", "data_limited"],
    ["GW", "gravastar joint lag+ratio (EXT.3)", "lag=0.7 ms AND q<=(2/3)^6 simultaneously",
     "injection pipeline OK; real strain no joint hit (Stage-1 null)", None,
     "search_target", "gravastar C=3/8 + recovery kernel",
     "strain_level_test", "extended-signatures/gw_joint + gw-ringdown-echo",
     "joint lag+ratio echo in >=2 detectors", "data_limited"],
    ["horizon", "compiler fingerprint catalog (EXT.4)", "t_scr~4M logS; P_H~c3/(1920M^2); DeltaA=4ln3",
     "structural identities OK; no direct measurement", None, "search_target",
     "horizon readouts (scrambling/Hawking/area)",
     "search_target", "extended-signatures/horizon",
     "high-overtone QNM != ln3 OR scrambling coeff != 4", "data_limited"],
    ["neutrino", "J_PMNS derived CP strength (EXT.5)", "J=-0.0297, J_max=0.0342",
     "J_max vs NuFIT ~0.033 (~3%); sign negative (CP-violating)", 1.5, "bridge",
     "PMNS assembly (v270)", "downstream_bridge", "extended-signatures/galois_cp + neutrino-mixing",
     "J_PMNS sign flip or |J| incompatible at sharpened delta_CP", "consistent"],
    ["seed", "extended seed xi + BBN shadows (EXT.6)", "xi=c3/phi0; BBN Y_p/D/H/N_eff shadow only",
     "core chi2/dof unchanged; BBN legs no extra phi0 DOF", None, "prediction",
     "one retarded seed + metrology ratio", "prediction_of_record",
     "extended-signatures/seed_extended",
     "two independent phi0 families >3 sigma", "consistent"],
    ["pulsar", "dynamic Crab MF + FRB gap clock (EXT.7)", "bend 2.7095 two-mode + repeater gap ratios",
     "Crab: monthly nu(t) if ephemeris present; FRB gaps null when FAST absent", None,
     "search_target", "walled clock + cascade comb", "search_target",
     "extended-signatures/dynamic_probes",
     "Vela daily nu(t) shows omega=2.58 comb OR locked bend 2.7095", "data_limited"],
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
LEAKAGE_CLASS_ENUM = {"external_data", "downstream_bridge", "search_target",
                      "surface_leakage", "core_operator", "architecture_core",
                      "internal_kernel", "detector_control", "parked"}
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
    # frb-ontology diagnostics: standard magnetospheric physics (orthogonal modes +
    # propagation memory) / survey selection (Pleunis+2021 morphology split) predict
    # the same phenomenology -> weakly discriminating consistency typings, never hits.
    "parity-without-rate diagnostic": {"discriminative_power": "weak",
                                       "signature_code": "S4/S5",
                                       "transduction_B": "missing_or_unproven",
                                       "projection_nonzero": "not_established"},
    "repeater/one-off leaf classes": {"discriminative_power": "weak",
                                      "signature_code": "S4",
                                      "transduction_B": "missing_or_unproven",
                                      "projection_nonzero": "not_established"},
    "UHECR energy-spectrum size-space DSI": {"signature_code": "S7",
                                             "clock_map": "not_required_size_space"},
    "primordial log-comb at the frozen omega": {
        "signature_code": "S2b/S14",
        "clock_map": "motivated_inflation_efolds",
        "transduction_B": "assumed_bridge_flagged",
        "projection_nonzero": "assumed_bridge_flagged",
        "decision_horizon": "mid_term"},
    "operator-structure probes: covariance blocks": {
        "signature_code": "S8-data/S15",
        "discriminative_power": "weak",
        "transduction_B": "missing_or_unproven",
        "projection_nonzero": "not_established"},
    # FO.02 carries the first NAMED FRB transduction (DM/RM line integrals; S15 gate
    # passed); FO.03 carries the first NAMED clock (S14) -- same comb question as
    # RC.02, an alternative READING, never an independent null.
    "medium-state common two-rate operator": {"signature_code": "S2a",
                                              "leakage_class": "core_operator",
                                              "transduction_B": "named_linear_line_integral",
                                              "projection_nonzero": "generic_nonorthogonality",
                                              "clock_map": "not_required_for_rate_test"},
    "state-clock comb in tau_mod": {"signature_code": "S2b/S14",
                                    "clock_map": "named_medium_state_clock"},
    # flat-budget closure: a COMPOSITE of already-counted legs (Omega_b/theta12-class
    # phi0_seed + the alpha_em Lambda engine + the v468 nu floor) plus the flagged
    # Omega_c candidate -- it shares phi0_seed and is an ALTERNATIVE DM reading to the
    # axion-spine branch (one DM question, two readings, never two hits).
    "flat LambdaCDM budget closure": {"independence_group": "phi0_seed",
                                      "alternative_group": "axion_branch",
                                      "discriminative_power": "medium",
                                      "dominant_leg": "omega_b (CMB-side)",
                                      "max_leg_pull_sigma": 2.02},
    # alpha^-1 is the PRIMARY alpha_em member: the Lambda hierarchy + S_dS DERIVE from it,
    # so all three are ONE cluster, not three independent hits. +1.9 sigma at CODATA precision
    # (a watch item, also tracked live in v307_data_watchdog) -- not a clean win.
    "fine-structure constant": {"independence_group": "alpha_em", "watch_flag": True,
                                "watch_level": "medium"},
    # F_transfer bridges to known constants: real handles, but weakly discriminating / [C]/[O].
    # Both Koide rows read the SAME PDG/Belle-II tau mass -> one cluster, never two hits.
    "Koide ratio Q": {"discriminative_power": "weak", "independence_group": "koide_q_pole"},
    "Koide Q=2/3 tau-mass kill window": {"discriminative_power": "weak",
                                         "decision_horizon": "near_term",
                                         "independence_group": "koide_q_pole"},
    "proton/electron mass ratio": {"discriminative_power": "weak"},
    # both CP phases are ONE hexagonal mu6 CM unit rho=e^{i pi/3} split by the Z2 sheet
    # (v231/v233): delta_PMNS = delta_CKM,lead + pi. They are correlated, NOT two
    # independent hits; the leptonic phase has weak discriminative power (large delta_CP error).
    "delta_CKM": {"independence_group": "cp_mu6_phase",
                  "signature_code": "S13",
                  "leakage_class": "architecture_core"},
    "delta_nu_CP": {"independence_group": "cp_mu6_phase", "discriminative_power": "weak",
                    "signature_code": "S13",
                    "leakage_class": "architecture_core"},
    # validation_tier (optional metadata, 2026-07-06): separates the evidence LADDER --
    # math_closed < internal_consistency < instrument_validated < analog_positive_control
    # < nature_* -- so analog/instrument rows never inflate the nature-evidence count.
    "QGEO S_off on a real measured boundary operator":
        {"validation_tier": "instrument_validated",
         "signature_code": "S8",
         "leakage_class": "core_operator",
         "clock_map": "operator_clock_read_off_from_boundary_map",
         "transduction_B": "EIT directly reconstructs the boundary ND operator",
         "projection_nonzero": "direct_operator_projection"},
    "recovery kernel as a quantum circuit":
        {"validation_tier": "instrument_validated",
         "signature_code": "S12",
         "leakage_class": "internal_kernel",
         "clock_map": "engineered_transfer_steps",
         "transduction_B": "quantum circuit and readout implement the channel",
         "projection_nonzero": "direct_circuit_readout"},
    "recovery kernel as CPTP map": {"stage": "not_applicable"},
    "Page curve turnover": {"stage": "not_applicable"},
    "Petz recovery + rank-one baby universe": {"stage": "not_applicable"},
    "entanglement spectrum carries the kernel (QT.01)": {"stage": "not_applicable"},
    "quench discrete-scale-invariance (QT.02)": {"stage": "not_applicable"},
    "walled clock + matched-filter discriminator (QT.04)": {"stage": "not_applicable"},
    "anyon MTC statistical phases (QT.05)": {"stage": "not_applicable"},
    "S_dS rho_Lambda": {"stage": "not_applicable"},          # algebraic identity, not a measurement
    "shared seed phi0": {"chi2_dof": 1.23, "max_leg_pull_sigma": 2.0,
                         "dominant_leg": "theta13", "dominant_chi2_fraction": 0.88,
                         "signature_code": "S9",
                         "leakage_class": "architecture_core",
                         "clock_map": "not_required",
                         "transduction_B": "shared_seed_decoder",
                         "projection_nonzero": "cross_channel_ratios"},
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
    # w(z) from DESI and CCBH-coupling k both probe "is dark energy a constant Lambda?" ->
    # ALTERNATIVE readings of one question, never two independent hits.
    "dark-energy equation of state w": {"watch_flag": True, "watch_level": "high",
                                        "alternative_group": "w_de_eos"},
    "CCBH cosmological coupling": {"alternative_group": "w_de_eos", "discriminative_power": "weak"},
    # the joint (w, Sigma m_nu) pincer is an ALTERNATIVE reading of the w question
    # (w_de_eos) AND shares its nu leg with the sum-m_nu row (nu_mass_floor) -- it is
    # never an independent hit on either axis.
    "joint fixed point (w, Sigma m_nu) pincer": {"alternative_group": "w_de_eos",
                                                 "independence_group": "nu_mass_floor"},
    "sum m_nu": {"independence_group": "nu_mass_floor"},
    # the drift lock DERIVES from the alpha^-1 <-> Lambda-hierarchy relation (v60/v274):
    # same alpha_em cluster as the fine-structure and Lambda rows, not a new hit.
    "alpha-Lambda drift lock": {"independence_group": "alpha_em"},
    "cosmic spin handedness": {"discriminative_power": "weak", "decision_horizon": "long_term"},
    # --- 2026-07-03 watchdog round (axes E-G + dipole + Li + S8) ---
    # both axis-E legs read the SAME frozen lambda_C (phi0-derived): one cluster.
    "Cabibbo first-row dissolution watchdog": {"independence_group": "phi0_seed",
                                               "decision_horizon": "near_term"},
    "neutron lifetime tau_n": {"independence_group": "phi0_seed",
                               "decision_horizon": "near_term"},
    "X17 dissolution watchdog": {"decision_horizon": "near_term"},
    "R_D(*) lepton-universality dissolution watchdog": {"watch_flag": True,
                                                        "watch_level": "medium",
                                                        "decision_horizon": "near_term"},
    "cosmic number-count dipole": {"watch_flag": True, "watch_level": "medium",
                                   "decision_horizon": "long_term"},
    # the lithium problem is UNIVERSAL to every LCDM-eta cosmology -> weak discrimination;
    # its D/H + Yp anchors share the phi0_seed Omega_b record.
    "primordial 7Li at the frozen eta": {"discriminative_power": "weak",
                                         "independence_group": "phi0_seed"},
    # S8 forecast = the SAME closure pattern as the flat-budget row (all legs shared).
    "S8 forecast from the flat budget": {"independence_group": "phi0_seed",
                                         "alternative_group": "axion_branch",
                                         "discriminative_power": "medium",
                                         "dominant_leg": "A_s branch (N_star)"},
    # 3/8 is shared by every SU(5)/SO(10) GUT -> not TFPT-discriminating; the M_Z gap is the
    # universal SM non-unification, not a TFPT-specific tension. Grouped with proton decay:
    # sin^2_W(3/8) and tau_p(branch B) are both downstream of the SAME carrier-PS->SO(10)
    # unification story -> ONE independence_group, never two independent hits.
    "Weinberg angle sin^2 th_W": {"discriminative_power": "weak",
                                  "independence_group": "carrier_ps_so10_uv_branch"},
    # proton lifetime: OPTIONAL gauged UV branch B (not the default boundary-only reading);
    # weakly discriminating (generic GUT signature), near-term decisive (Hyper-K this decade).
    "proton lifetime tau_p": {"discriminative_power": "weak", "decision_horizon": "near_term",
                              "independence_group": "carrier_ps_so10_uv_branch"},
    # --- Higgs near-criticality: show the two-axis pull, not just a green label ---
    "Higgs near-criticality": {"lambda_pull_sigma": 2.5, "beta_lambda_pull_sigma": "near_zero",
                               "status_note": "near critical; exact double-critical surface "
                                              "mildly stressed (M_t-dominated)"},
}


def _evidence_class(row: dict) -> str:
    if row["stage"] == "parked_analog":
        return "parked"
    if row.get("validation_tier") in {"instrument_validated", "analog_positive_control"}:
        return "internal_consistency"
    if row["stage"] == "not_applicable":
        return "internal_consistency"
    src = row["source"].lower()
    if "(numerical)" in src or "internal identity" in src:
        return "internal_consistency"
    if row["stage"] == "downstream_bridge":
        return "downstream_bridge"
    if row["stage"] in {"search_target", "strain_level_test", "catalog_feasibility"}:
        return "search_target"
    return "external_data"


def _infer_signature_metadata(row: dict) -> None:
    """Attach the 2026-07-06 signature reclassification without changing row meaning."""
    o = row["observable"].lower()
    b = row["bridge_type"].lower()

    if row["stage"] == "parked_analog":
        row.setdefault("leakage_class", "parked")
        return

    if row["evidence_class"] == "downstream_bridge":
        row.setdefault("leakage_class", "downstream_bridge")
        row.setdefault("transduction_B", "downstream_bridge_model")
        row.setdefault("projection_nonzero", "model_dependent")
        return

    if row["evidence_class"] == "external_data":
        row.setdefault("leakage_class", "external_data")
        row.setdefault("clock_map", "not_required")
        row.setdefault("transduction_B", "prediction_decoder_or_standard_observable")
        row.setdefault("projection_nonzero", "prediction_of_record")
        return

    if row["evidence_class"] == "internal_consistency":
        row.setdefault("leakage_class", "internal_kernel")
        row.setdefault("clock_map", "internal_or_engineered")
        row.setdefault("transduction_B", "known_by_construction")
        row.setdefault("projection_nonzero", "direct_internal_observable")

    if "false-positive control" in o:
        row.setdefault("signature_code", "detector-control")
        row.setdefault("leakage_class", "detector_control")
        row.setdefault("clock_map", "matched_to_control_system")
        row.setdefault("transduction_B", "control_dataset_detector")
        row.setdefault("projection_nonzero", "not_a_tfpt_projection")
        return

    # Old visible-number searches are now surface-leakage probes unless a direct operator
    # readout or seed decoder was set by OVERRIDES.
    surface_terms = (
        "boundary recovery kernel", "sub-burst step kernel", "resummed recovery clock",
        "mu4", "z2", "moebius", "walled clock", "recovery comb", "kernel couplings",
        "size-space", "qpe recurrence", "hfqpo", "gravastar", "frb gap clock",
    )
    if row["evidence_class"] == "search_target" and any(t in b or t in o for t in surface_terms):
        row.setdefault("leakage_class", "surface_leakage")
        row.setdefault("transduction_B", "missing_or_unproven")
        row.setdefault("projection_nonzero", "not_established")
        if any(t in o for t in ("comb", "omega", "cascade", "dynamic", "recovery")):
            row.setdefault("clock_map", "observer_time_or_surface_clock_unjustified")
        else:
            row.setdefault("clock_map", "not_required_for_static_probe")

    signature_patterns = (
        ("echo ratios", "S1"),
        ("ringdown echo amplitude ratio", "S1/S10"),
        ("activity-window eigenwidths", "S1"),
        ("pol-fraction quantisation", "S5"),
        ("width-relaxation echo", "S1"),
        ("static PA mu4 classes", "S5"),
        ("PA/RM Markov spectrum", "S2a/S5"),
        ("recovery-clock dynamics", "S3"),
        ("glitch-size log-periodicity", "S7"),
        ("per-pulsar size/waiting kernel ladder", "S1/S7"),
        ("recovery Q / tau_d", "S3"),
        ("dynamic recovery comb", "S2b"),
        ("recovery comb on", "S2b"),
        ("recovery comb in", "S2b"),
        ("microshot cascade", "S1/S2b/S3"),
        ("kernel couplings", "S2a/S4/S5/S6/S7/S8-proxy"),
        ("repeater burst-time cascade", "S2b/S11"),
        ("Z2/Moebius double-cover", "S4"),
        ("recovery-waveform clock template", "S3/S2b"),
        ("QPE recurrence", "S1/S2b/S3"),
        ("BH HFQPO", "S1e"),
        ("comb ripple", "S2b"),
        ("meta-analytic UL", "S2b"),
        ("area-quantum spectral comb", "S10"),
        ("compiler fingerprint catalog", "S10"),
        ("achromatic dyonic intercept", "S10e"),
        ("anyon pi/4", "S12/S5"),
        ("dynamic Crab", "S2b/S3"),
    )
    for needle, code in signature_patterns:
        if needle.lower() in o:
            row.setdefault("signature_code", code)
            break

    if row["evidence_class"] == "search_target":
        row.setdefault("leakage_class", "search_target")
        row.setdefault("clock_map", "not_required_or_unspecified")
        row.setdefault("transduction_B", "experiment_specific")
        row.setdefault("projection_nonzero", "experiment_specific")


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
    _infer_signature_metadata(row)
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
        if row.get("leakage_class") not in LEAKAGE_CLASS_ENUM:
            raise ValueError(f"bad leakage_class in {row['observable']!r}")
        rows.append(row)

    def _tally(key: str) -> dict[str, int]:
        out: dict[str, int] = {}
        for row in rows:
            value = row.get(key)
            if value is None:
                continue
            out[value] = out.get(value, 0) + 1
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
        "leakage_class_enum": sorted(LEAKAGE_CLASS_ENUM),
        "n_rows": len(rows),
        "count_by_status": _tally("status"),
        "count_by_stage": _tally("stage"),
        "count_by_evidence_class": _tally("evidence_class"),
        "count_by_leakage_class": _tally("leakage_class"),
        "count_by_signature_code": _tally("signature_code"),
        "count_by_independence_group": _tally("independence_group"),
        "count_by_alternative_group": _tally("alternative_group"),
        "n_watch_flag": sum(1 for r in rows if r.get("watch_flag")),
        "rows": rows,
    }


def _readme_stats_block(card: dict) -> str:
    """The auto-generated stats paragraph (single source = the scorecard JSON)."""
    st = card["count_by_status"]
    ec = card["count_by_evidence_class"]
    lc = card["count_by_leakage_class"]
    sc = card["count_by_signature_code"]
    ig = card["count_by_independence_group"]
    ag = card["count_by_alternative_group"]
    order = ["consistent", "hint", "tension", "null", "data_limited", "kill_channel", "parked"]
    status_str = ", ".join(f"{st[k]} {k}" for k in order if k in st)
    ec_str = ", ".join(f"{ec[k]} {k}" for k in sorted(ec))
    lc_str = ", ".join(f"{lc[k]} {k}" for k in sorted(lc))
    sc_str = ", ".join(f"{sc[k]} {k}" for k in sorted(sc))
    ig_str = ", ".join(f"{ig[k]} {k}" for k in sorted(ig))
    ag_str = ", ".join(f"{ag[k]} {k}" for k in sorted(ag))
    return (f"<!-- SCORECARD_STATS:START (generated by build_evidence_scorecard.py; do not edit) -->\n"
            f"**Scorecard (auto-generated from `evidence_scorecard.json`): {card['n_rows']} "
            f"Zeilen — {status_str}.**\n\n"
            f"- nach `evidence_class`: {ec_str}\n"
            f"- nach `leakage_class`: {lc_str}\n"
            f"- nach `signature_code`: {sc_str}\n"
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
    print("by leakage_class:", card["count_by_leakage_class"])
    print("by signature_code:", card["count_by_signature_code"])
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
