# TFPT GW ringdown echoes — `(2/3)⁶` ratio (Stage 0/1) + dynamic walled-clock recovery (Stage 2)

`search.txt` §5: if post-merger boundary recovery imprints echoes on the black-hole
ringdown, their amplitude ratio is bounded by the **same** recovery eigenvalue that
governs FRBs and flavour:

```
A_{n+1} / A_n  ≤  λ₂ = (2/3)⁶ = 64/729 ≈ 0.0878        (lag free, ratio frozen)
```

It is an **upper bound**, so this is a consistency / upper-limit channel.

## Stages

Stage 0 is a **GWTC-5.0 catalogue-based feasibility and sensitivity census** (no echo
claim; it only decided the strain search was worth running). Stages 1/1b/2 below are the
actual strain-level tests: Kerr ringdown subtraction → matched filter on residuals (free
lag, free phase, **fixed** ratio) → free-`q` control template → off-source backgrounds →
a stacked statistic over the loudest events. The stacked search that Stage 0 forecast has
now been **run** (Stage 1b); coherent time-slide backgrounds remain the escalation path
if a candidate ever appears.

## Data

Real LVK catalogue from the GWOSC event API (`scripts/fetch_catalog.py`):
**GWTC-5.0, 390 canonical confident events (161 new in O4b)**. The local download is
**391 version-deduplicated rows**; the one-event difference (the legacy BNS GW170817)
is reconciled in [`event_count_audit.md`](event_count_audit.md) and is excluded from
the BBH selection regardless.

## Forecast (real catalogue, `data/gwtc_events.csv`)

- 391 raw rows → **278 ringdown-capable BBH** (`M_f ≥ 5 M☉`); loudest `GW250114` at
  network SNR 78.6 (full selection accounting in `event_count_audit.md`).
- stacked echo-SNR upper bound: 21.1 (conservative `f_rd=1`), **6.3** (realistic
  `f_rd=0.3`) vs detection threshold 5.

→ **catalog-feasibility**: a maximal `(2/3)⁶` echo would be reachable by a stacked
strain search, so the Stage-1 strain test is worth running. **No echo claim is made
at catalog level.**

## Stage 1 — static `(2/3)⁶` echo train on real strain (`tfpt-gw search` / `realdata`)

The Stage-1 matched filter (`echo_search.py` synthetic injection-recovery, validated
**3/3**; `real_echo_search.py` on real GWOSC strain) whitens the strain, subtracts the
dominant Kerr (l=m=2,n=0) ringdown, and matched-filters the residual with an **echo train**
at the frozen amplitude ratio `(2/3)⁶` (free lag, free-`q` control). Real strain now spans
the **10 loudest ringdown events** — including **GW250114 (network SNR 78.6, O4b, the
loudest ringdown on record)**, GW230814, GW240920, GW231226, GW241127, GW200129,
GW190521_074359, GW240621, GW150914, GW190521 — → **no faint kernel-ratio echo coincident
in ≥2 detectors in any event**; low-`p` excesses have `q̂ ~ 1` (residual ringdown power,
free-ratio-rejected). Consistent with the upper bound; no claim.

O4/GWTC-4+ events have no 32 s files on GWOSC; `scripts/fetch_strain_4096.py` downloads the
4096 s 4 kHz archive segment and crops a 32 s window in the same HDF5 layout.

**Redshift correction (signature revision, 2026-07-02):** the GWTC catalogue reports
**source-frame** masses, but the observed ringdown is at `f₀/(1+z)`. All searches now use
the detector-frame mass `M_det = M_src (1+z)` (`strain_data.detector_frame_mass`). Before
this fix GW190521 (z = 0.56) was filtered at 116 Hz instead of the correct ~75 Hz — a
~1.6× template-frequency error on the highest-z event. All stages were re-run corrected.

## Stage 1b — STACKED search over the loudest ringdowns (`tfpt-gw stack`) — NEW

The Stage-0 forecast said only a **stack** reaches the detection threshold (realistic
stacked echo-SNR 6.3 vs threshold 5). `stacked_search.py` combines the per-event
matched-filter maxima into one on-source statistic `Z = Σ ρ²_max` over all detector
streams and draws the background stack from each stream's off-source distribution
(20 000 realisations), plus a Fisher combination as a secondary view.

**Result (10 events, 23 detector streams, redshift-corrected): `Z_on = 149.5` vs
background median `93.8` → stacked `p = 0.262`; kernel-consistent streams 0/23.** The
Fisher secondary is dominated by `q̂ ~ 1` residual-ringdown streams that the free-ratio
control rejects as non-kernel — it is not evidence for a `(2/3)⁶` train. **Verdict:
STACKED NULL — a maximal kernel-ratio echo train is disfavoured in the loudest available
stack; since `(2/3)⁶` is an upper bound, this is `consistent` (the bound tightens). No
detection, no tension claim.**

## Stage 1c — SIGNATURE BATTERY (`tfpt-gw battery`) — "could the signature be different?"

A post-hoc robustness sweep over the alternative signature readings the kernel and the
physics allow (Bonferroni ×12), on the same 10 events:

- **Ratio semantics (the FRB lesson):** amplitude `(2/3)⁶`, **energy reading `(2/3)³`**
  (GW energy ∝ amplitude², so an energy-ratio kernel gives a 3.4× louder strain train),
  and step `2/3`.
- **Per-bounce phase — the boundary-birefringence analogue:** `Δφ ∈ {0, π/2, π, 3π/2}`
  (the μ₄ characters; TFPT's natural value is the quarter turn π/2). Propagation-path GW
  birefringence (parity, `c₋ = 8 ≠ 0`) is common to all echoes of one event and **cancels
  in the inter-echo ratio**; only a per-reflection phase does not cancel — scanned here.
- **Extended lags 0.5–350 ms** (ECO/gravastar ~0.7 ms through Planckian ~0.23 s @63 M☉).
- **Joint (2,2,0)+(2,2,1) subtraction** (Berti+ 2006 fits for both modes) — the `q̂ ~ 1`
  excesses of the primary search are overtone/residual power.
- **Off-source (event-gated) PSD** (v3 re-run): the whitening filter is estimated
  excluding `[merger−1 s, merger+3 s]`, so it cannot adapt to — and ring after — the loud
  event. Diagnostic outcome: the GW150914/GW200129/GW190521 broadband excesses **persist**
  under the off-source PSD, i.e. they are genuine post-merger residual power (plausibly
  unsubtracted higher-mode/nonlinear-QNM content), **not** filter artefacts.
- **Template-agnosticism control:** streams where *all 12* variants fire together are
  broadband residual power (an echo train prefers ONE reading) — rejected as non-echo.

**Result: `NO_VARIANT_ECHO` on all 10 events.** Best Bonferroni `p = 0.0157` (single
stream, not ratio-consistent, no second detector). The primary null is **robust against
the alternative signature readings**. Not covered (documented limits): frequency-dependent
barrier filtering of successive echoes (see Stage 1d's incoherent statistic), inter-echo
lag drift, precessing remnants. Output: `results/signature_battery.json`.

## Stage 1d — TFPT POINT TEST (`tfpt-gw point`) — theory-fixed lag × kernel-fixed ratio

The battery scans the lag freely; TFPT actually **predicts** it: the gravastar-compactness
Nariai rational `C = 3/8` gives the tortoise round trip **`Δt = 2.288 M_det`** (0.77 ms for
GW250114; 2.59 ms for GW190521 at the detector-frame mass). Combining the predicted delay
(±25 % tolerance) with the kernel-fixed ratios `{(2/3)⁶, (2/3)³}` and the μ₄ phases gives a
**point hypothesis** with a minimal look-elsewhere budget (Bonferroni ×10) — the sharpest
TFPT-specific echo test. A second, **morphology-robust incoherent statistic** (free phase
per echo, only positions and ratio weights fixed) covers barrier low-pass filtering that
degrades the coherent template.

**Result (v2, systematic-hardened): `NO_POINT_ECHO` on all 10 events.** The v2 run adds the
full systematics battery from the signature review: **off-source (event-gated) PSD** (the
whitening filter cannot ring after a merger it never saw), a **remnant-spin scan**
`af ∈ {0.60, 0.69, 0.80}` (Kerr template systematic), a **skip-first-echo** variant (the
first reflection samples the nonlinear regime and may break the geometric progression), and
a **joint QNM+train fit** that repairs the short-lag flaw of subtract-then-search: at the
predicted ECO lag (~0.8 ms < τ ≈ 4 ms) echoes *overlap* the primary ringdown, so the QNM
subtraction partially absorbs any train — the joint fit tests both together (F-statistic,
off-source calibrated). GW150914 remains the one event with mild coincident raw excesses
(p ~ 0.001–0.03 across statistics) that persist under the off-source PSD — but nothing
survives Bonferroni in ≥2 detectors (best `p_bonf = 0.05`), and the battery's
template-agnosticism control classifies the excess as broadband residual power (most
plausibly unsubtracted higher-mode / nonlinear-QNM content; an NR-informed subtraction is
the escalation path). Upper bound, no tension. Output: `results/point_test.json`.

## Stage 1f — OFFSET-TRAIN point test (`tfpt-gw offset`) — scrambling delay × cavity spacing

The last untested train geometry: the TFPT scrambling time **t_scr = 4M·ln S ≈ 0.25 s**
(ln S = 2 ln(M/l_P) + ln 4π) can delay the *first* re-emission globally while the cavity
keeps the Nariai spacing **2.288 M ≈ 0.8 ms** — an offset ≠ spacing train that no earlier
stage probed (all anchored the train at the merger). Two theory-fixed numbers ⇒ minimal
trials (Bonferroni ×28: ratio × phase × spacing grid). Bonus: at t_scr the ringdown has
decayed by ~60 e-folds, so **no QNM subtraction is needed** — that systematic vanishes.
Caveat: at 4 kHz the ~0.8 ms spacing is only ~3 samples, so the spacing grid is coarse for
the lightest remnants (documented in the module).

**Result: `NO_OFFSET_TRAIN` on all 10 events** (best `p_bonf = 0.035`, GW200129/V1, single
stream, no coincidence). The offset≠spacing geometry is null. Output:
`results/offset_train.json`.

**Multimode-subtraction diagnostic (`tfpt-gw battery --multimode`):** subtracting
(3,3,0), (2,1,0) and the quadratic 220×220 mode (f = 2f₂₂₀, τ = τ₂₂₀/2) *in addition to*
220+221 does **not** remove the GW150914/GW200129/GW190521 template-agnostic broadband
excesses — they persist and stay template-agnostic.
Output: `results/signature_battery_multimode.json`.

**Agnostic residual-modelling diagnostic (`tfpt-gw battery --aggressive`)** — the honest
stand-in for NR-informed subtraction: greedy matching pursuit fits up to 6 *free* damped
sinusoids (peak-frequency + τ-grid, 30–600 Hz) in the post-merger window and subtracts
them. **Outcome: the broadband-excess mystery is resolved** — GW200129, GW190521 and
GW190521_074359 lose their excesses entirely (H1 p goes 0.001 → 0.2–0.6), i.e. their
"excess" was quasi-QNM transient power (higher overtones n ≥ 2 / mode mixing) that free
damped sinusoids absorb; GW150914 is strongly reduced but retains one low-p
template-agnostic stream (older detector state; residual non-stationarity or deeper mode
content — the only place where a true NR waveform subtraction would still add
information). No echo-train candidate appears at any stage of the subtraction ladder
(220+221 → +330/210/quadratic → +matching pursuit).
Output: `results/signature_battery_aggressive.json`.

## Stage 1g — DRIFT + PRECESSION robustness scan (`tfpt-gw robust`)

The last two signature-distortion axes: **per-bounce lag drift** (a relaxing cavity —
spacing drifts by δ ∈ {−10 %, −5 %, +5 %, +10 %} per bounce, coherent templates at the
C = 3/8 lag grid) and a **precession proxy** (a precessing remnant modulates per-echo
amplitudes while keeping positions — position-only statistic: free phase per echo,
*uniform* weights, testing the train positions without amplitude ordering).

**Result: `NO_DRIFT_OR_PRECESSION_ECHO` on all 10 events** (best `p_bonf = 0.046`,
GW150914/L1, single stream). Output: `results/robustness_scan.json`.

## Stage 1e — AREA-QUANTUM spectral comb (`tfpt-gw bmcomb`) — Bekenstein–Mukhanov lines

BH-specific theory input never tested before: TFPT's area quantum **ΔA = 4 ln3** (v57,
horizon readouts) plus Bekenstein–Mukhanov quantisation makes the horizon a discrete-line
system with transition frequency `ω_BM = T_H ln3` (exactly the Hod frequency, read as a
**line spectrum**): harmonics `f_n = n·ln3/(16π² M_det)` — ~20.5 Hz spacing at 68 M☉, i.e.
**~20 comb lines across the LVK band** in the post-merger residual spectrum. The statistic
compares residual power on comb bins vs interleaved off-comb bins (off-source PSD, joint
220+221 subtraction, off-source backgrounds) with a **spacing battery**
`{0.8, 0.9, 1.0, 1.1, 1.25}×f_BM` as template-specificity control and the spin scan in the
Bonferroni budget.

**Result: `NO_BM_COMB` on all 10 events.** Honest power note: line widths, exterior
coupling and the residual-power fraction carrying the lines are model-dependent — this is
a well-defined search-target null, not a kill test of the area quantum.
Output: `results/bm_comb.json`.

## Stage 2 — DYNAMIC walled-clock recovery matched filter (`tfpt-gw dynamic`) — NEW

Closes the [`experiments/README.md`](../README.md) **§1.1 "Reconsideration"** for the GW
channel: the static ratio is a *number*, but the kernel's discrete→dynamic transition
(`v124`/`v126`/`v147`, mirrored in `quantum-testbed/clock.py` QT.04) is a **walled two-mode
clock** `R(t)=w₀+w₁e^{-(6 ln 3/2)t/τ}+w₂e^{-(6 ln 3)t/τ}` with the **det'-clean bend**
`rate(2)/rate(1)=ln3/ln(3/2)=2.7095`, a protected floor and a hard wall (no 3rd mode).

`dynamic_recovery.py` whitens once, subtracts the dominant QNM, builds the **post-merger
residual power envelope** (binned RMS) and fits the **fixed-bend** template, profiling the
rate ratio over a grid (each ratio = one nonlinear rate → well-conditioned, unlike a free
2-exp fit) with a single-exponential (leftover-ringdown) null model and an off-source
background `p`-value. **Result on real strain (GW250114, GW150914, GW190521):
`NO_KERNEL_RECOVERY`** — where the envelope decays it is leftover single-mode ringdown
(profiled `q̂≈1`, not the bend 2.7095); this now includes the loudest ringdown on record.

**The honest, machine-checked finding (the reason this channel is structurally limited):**

1. **Within ONE monotone recovery the bend is degenerate.** The exact walled-clock curve is
   fit by *floor + a single exponential* to a two-mode R² gain of only **≈1.3×10⁻³** (even
   noise-free) — two summed exponentials look like one + floor. So a single BH ringdown
   residual **cannot carry the rate ratio 2.7095**.
2. **The discriminating dynamic signature is the log-periodic comb across a CASCADE** at
   `ω = 2π/ln((3/2)⁶) = 2.583`, with amplitude `ε ~ exp(-π²/ln λ) ≈ 0.017` (~2%, the QT.02
   suppression law). A single ringdown **is not a cascade** ⇒ the sensitive lever is the
   **time-resolved recovery SEQUENCE of a repeating source** (FRB repeater / pulsar-glitch
   train), not a one-shot ringdown.

**Status: `data_limited`. No recovery claim.** Output: `results/dynamic_recovery.json` +
`results/dynamic_recovery.png` (the degeneracy, the real on-source envelope, the cascade comb).

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .
python scripts/fetch_catalog.py      # re-download GWTC from GWOSC (catalog census)
tfpt-gw analyze                       # Stage 0 census   (or: PYTHONPATH=src python -m tfpt_gw.cli analyze)
tfpt-gw search                        # Stage 1 synthetic injection-recovery (3/3)
python scripts/fetch_strain.py GW150914 GW190521          # O1-O3: 32 s files
python scripts/fetch_strain_4096.py GW250114_082203 ...   # O4+: crop from 4096 s segments
tfpt-gw realdata --events GW250114_082203 GW150914 GW190521   # Stage 1 static echo
tfpt-gw dynamic  --events GW250114_082203 GW150914 GW190521   # Stage 2 walled clock
tfpt-gw stack    --events GW250114_082203 GW230814_230901 GW240920_124024 \
  GW231226_101520 GW241127_061008 GW200129_065458 GW190521_074359 \
  GW240621_195059 GW150914 GW190521                            # Stage 1b stacked search
tfpt-gw battery  --events ...same 10 events...                 # Stage 1c signature battery
tfpt-gw point    --events ...same 10 events...                 # Stage 1d TFPT point test v2
tfpt-gw bmcomb   --events ...same 10 events...                 # Stage 1e area-quantum comb
tfpt-gw offset   --events ...same 10 events...                 # Stage 1f offset-train test
tfpt-gw robust   --events ...same 10 events...                 # Stage 1g drift+precession
tfpt-gw battery --multimode --events GW150914 ...              # 330/210/quadratic diagnostic
tfpt-gw battery --aggressive --events GW150914 ...             # matching-pursuit diagnostic
```

## Layout

```
scripts/fetch_catalog.py    # download GWTC event list from GWOSC -> data/gwtc_events.csv
scripts/fetch_strain.py     # download 32 s, 4 kHz HDF5 strain per event -> data/strain/
scripts/fetch_strain_4096.py# O4+: download 4096 s segment, crop 32 s (same HDF5 layout)
src/tfpt_gw/constants.py    # frozen ratio (2/3)^6; STAGE
src/tfpt_gw/echo_forecast.py# Stage 0 per-event + stacked echo-SNR sensitivity census
src/tfpt_gw/echo_search.py  # Stage 1 synthetic echo-train injection-recovery (validated 3/3)
src/tfpt_gw/strain_data.py  # real GWOSC HDF5 I/O + whitening + Kerr QNM (Berti+ 2006)
src/tfpt_gw/real_echo_search.py # Stage 1 static (2/3)^6 echo train on real strain
src/tfpt_gw/dynamic_recovery.py # Stage 2 dynamic walled-clock (bend 2.7095) on real strain
src/tfpt_gw/stacked_search.py   # Stage 1b stacked search over the loudest ringdowns
src/tfpt_gw/signature_battery.py# Stage 1c signature battery (semantics x mu4 phases x lags)
src/tfpt_gw/point_test.py   # Stage 1d point test v2 (C=3/8 lag, spin scan, skip-first, joint fit)
src/tfpt_gw/bm_comb.py      # Stage 1e area-quantum (Bekenstein-Mukhanov) spectral comb
src/tfpt_gw/offset_train.py # Stage 1f offset-train (scrambling delay x cavity spacing)
src/tfpt_gw/robustness_scan.py # Stage 1g drift + precession (position-only) scan
src/tfpt_gw/cli.py          # `tfpt-gw ...|point|bmcomb|offset|robust` (+ --multimode/--aggressive)
data/gwtc_events.csv        # real LVK GWTC-5.0 catalogue (390 canonical; 391 raw rows)
data/strain/                # real 32 s HDF5 strain (gitignored) + <event>_meta.json
event_count_audit.md        # 390 vs 391 reconciliation + selection accounting
results/dynamic_recovery.json,.png  # Stage 2 output + figure
results/echo_stack.json     # Stage 1b stacked-search output
results/signature_battery.json     # Stage 1c battery output
results/point_test.json     # Stage 1d point-test output
results/bm_comb.json        # Stage 1e area-quantum comb output
results/offset_train.json   # Stage 1f offset-train output
results/robustness_scan.json# Stage 1g drift+precession output
results/signature_battery_multimode.json   # multimode-subtraction diagnostic
results/signature_battery_aggressive.json  # matching-pursuit diagnostic
```
