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
     "strain-level echo with ratio >>(2/3)^6 across events", "consistent"],
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
    # repeater-cascade (experiments/repeater-cascade): first search past the 2.8-period range wall
    ["FRB", "repeater burst-time cascade comb + walled clock (RC.01-03)",
     "frozen comb omega=2.583 in ln(t-t_onset) + walled two-mode clock (bend 2.7095) + "
     "waiting-time tooth ladder {log 3/2, log(3/2)^3, log(3/2)^6} on repeater burst-time cascades",
     "9,916 real bursts / 4 sources (FRB 20220912A Zhang+2023, 20201124A Xu+2022/Zhang+2022, "
     "20240114A FAST pol v5, 15 CHIME Cat2 repeaters): FIRST search past the 2.8-period range "
     "wall -- 9 gate-passing sessions / 2 sources (max reach 4.80 periods), omega=2.583 NOT "
     "special (Fisher p=0.72/0.38, BH q=0.72); RC.01 bend degenerate on real cascades (0/37, "
     "Stage-2 degeneracy reproduced); RC.03 ladders null after Bonferroni (p=0.10); injection: "
     "94% at eps=0.30, 0% at predicted eps=0.0173 -> null at detectable amplitude, amplitude "
     "wall (~1e5 bursts/session) at the predicted 1.7%", None,
     "search_target", "boundary recovery kernel (dynamic, burst-time cascade)",
     "search_target", "FAST (VizieR J/ApJ/955/142; Blinkverse; pol catalog v5) + CHIME/FRB Cat2 "
     "(CANFAR DOI 10.11570/25.0066); repeater-cascade RC.01-03",
     "the omega=2.583 comb survives surrogates + off-kernel rank + lambda battery in >=2 "
     "gate-passing sessions", "null"],
    ["X-ray", "recovery comb in magnetar outburst relaxation (omega=2.58)",
     "log-periodic comb at omega=2.58 in the post-outburst X-ray flux decay (wide ln t, stackable)",
     "data_limited: needs Swift/XRT or Coti Zelati+2018 flux(t); ~3 decades in ln t = best new "
     "candidate, but magnetospheric (surface) relaxation -> search target with firewall caveat, "
     "not a horizon recovery; detector injection-validated", None,
     "search_target", "boundary recovery kernel (dynamic, surface caveat)",
     "search_target", "Swift/XRT light curves / Coti Zelati+2018 magnetar-outburst sample",
     "the omega=2.58 comb is special in a wide-ln-t magnetar flux-decay recovery", "data_limited"],
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
     "bend identifiable -- per-mode decode 2.65-2.69 at 256 shots, blind QT.04 free-ratio "
     "2.89+/-0.12 at 16384 shots (3/3 seeds), protected floor retention 0.993; IBM hardware "
     "hook prepared (open plan), not executed (needs token)", None,
     "search_target", "engineered seam-transfer channel (quantum-circuit analog of QT.04)",
     "not_applicable", "qc-recovery-kernel (Qiskit Aer + FakeBrisbane; numerical)",
     "the bend is not identifiable under the device noise model at any tested shot count",
     "consistent"],
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
    "delta_CKM": {"independence_group": "cp_mu6_phase"},
    "delta_nu_CP": {"independence_group": "cp_mu6_phase", "discriminative_power": "weak"},
    "recovery kernel as CPTP map": {"stage": "not_applicable"},
    "Page curve turnover": {"stage": "not_applicable"},
    "Petz recovery + rank-one baby universe": {"stage": "not_applicable"},
    "entanglement spectrum carries the kernel (QT.01)": {"stage": "not_applicable"},
    "quench discrete-scale-invariance (QT.02)": {"stage": "not_applicable"},
    "walled clock + matched-filter discriminator (QT.04)": {"stage": "not_applicable"},
    "anyon MTC statistical phases (QT.05)": {"stage": "not_applicable"},
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
