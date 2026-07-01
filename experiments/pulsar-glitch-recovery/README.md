# Pulsar-glitch recovery — the missing cross-domain leg

> **Firewall:** a **search target / consistency check**, never a load-bearing claim.
> Pulsar glitches are tested as a *residual boundary-recovery pattern*; nothing here
> is upgraded to `[E]`, and the recovery-`Q` channel that needs data not in the size
> catalogue is typed `data_limited`, not assumed.

`problem_1.txt` ("Pulsar Glitches" + the cross-domain "Goldkante") asks for the
**same** frozen boundary-recovery kernel `{1, (2/3)⁶, (1/3)⁶}` (step `3/2`) that is
tested in the FRB sub-burst echoes (`frb-tfpt-signatures` FRB.02/09) and the GW
ringdown echo (`gw-ringdown-echo`) to *also* show up in pulsar-glitch recovery.
The repo already had the FRB and GW legs; **this experiment adds the pulsar leg**,
so the three-way cross-domain test (the strongest possible TFPT signature per
`problem_1.txt`) is finally closeable.

Tested against the **real** Jodrell Bank Glitch Catalogue (Basu et al. 2022):
726 glitches across 222 pulsars (723 with `Δν/ν`).

## What it checks (`src/tfpt_pulsar/`)

| Channel | Signature (`problem_1.txt`) | Method + null | Result |
|---|---|---|---|
| **PG.01** | glitch sizes `Δν/ν` show **log-periodic** discreteness at a TFPT ratio (kernel `(3/2)^k`, or §C `{1+φ₀, 4, 8, 8π}`) | Rayleigh log-periodogram (scan-max p) + targeted single-ratio tests, calibrated against **three** nulls: log-normal, shape-preserving KDE, and the decisive **population-controlled GMM bootstrap** (reproduces the known two-population bimodality); look-elsewhere (Bonferroni) over the candidate family | **null** — the only structure is the known bimodality |
| **PG.02** | consecutive glitch **sizes** step by kernel factors (`\|Δlog s\|` on `{log 3/2, log(3/2)³, log(3/2)⁶}`) | per-pulsar comb fraction vs **within-pulsar shuffle** of the raw sizes — reorder each pulsar's own size set, *then recompute* the consecutive log-ratios (immune to the global bimodality) | **null** (frac 0.20 vs 0.19 chance, p≈0.27) |
| **PG.03** | inter-glitch **waiting-time** ratios on the same comb | per-pulsar comb fraction vs within-pulsar shuffle of the raw waiting intervals (reorder, then recompute ratios) | **null** (frac 0.22 vs 0.25 chance, p≈0.93) |
| **PG.04a** | recovery/healing fraction `Q ∈ {φ₀, 2φ₀, 4φ₀, 8φ₀, 1−φ₀}` | KDE + uniform null on the Yu+2013 `Q` set | **null** (frac 0.10 vs 0.22 chance, p≈1.0) |
| **PG.04b** | multi-component decay timescales `τ_d` form a `(3/2)^k` ladder | per-glitch `τ_{i+1}/τ_i` vs `τ_d`-shuffle | **null** (13 glitches, p≈0.69) |
| **PG.04c** | the *exact* clock (v124): 2-mode **bend** `τ_long/τ_short = ln3/ln(3/2) = 2.7095`; **wall** ≤2 decay modes | bend vs shuffle + component-count census | bend **null** (0/12, p≈1.0); **wall consistent** (45/46 ≤2 modes) |

### Reconsidered: the signature is *dynamical* — an exact *walled two-mode clock*, not a static ratio

Every channel above tests the frozen kernel as a **static ratio** in a histogram, and all come
back null. The verification suite's exact discrete→dynamic reconstruction (`v124`/`v126`/`v147`)
points at a richer reading (`src/tfpt_pulsar/dsi.py`, and `quantum-testbed` QT.04): the recovery
**clock** is the resummed logarithm `rate(n) = −6 ln(1−n/3)` with a **pole (wall) at `n=N_fam=3`**,
so a single recovery is a **two-mode + protected-floor** curve

```
R(t) = w0 + w1*exp(-6ln(3/2)*t/tau) + w2*exp(-6ln3*t/tau)
```

with the **det-clean bend** locking the two decay rates at `ln3/ln(3/2) = 2.7095` (PG.04c), a
**protected floor** (incomplete recovery, the `λ=1` "law"), and a **hard wall** (no 3rd decay mode).
PG.04b/c test the data-side proxies on the summary `Q`/`τ_d` (bend null; wall consistent — 45/46
glitches ≤2 modes). The genuine, more-sensitive test needs **time-resolved** recovery *waveforms*
(`ν(t)` after a glitch). Because a single monotone recovery's two-mode **bend is degenerate** with a
single exponential (machine-checked in the GW Stage-2 analysis: a two-mode R² gain of ~1e-3 even
noise-free), the *discriminating* dynamic signature is the **log-periodic comb** across a recovery
spanning a wide range in `ln(time)`, at `ω = 2π/ln((3/2)⁶) = 2.583`. **PG.05 runs exactly that test
on the real Crab `ν(t)` ephemeris** (below). (Sustained log-periodic DSI returns only across a
*cascade* of modes/events, never within one walled recovery.)

All TFPT numbers are *derived* from the two axioms (`c₃ = 1/(8π)`, `g_car = 5`) in
`constants.py` — identical to the `recovery-channel`/FRB kernel — and frozen as
*targets to test against*, never fitted.

## Result (real catalogue, deterministic seed)

- **PG.01.** Glitch sizes are **not** a single log-normal (KS p≈0) and are
  multimodal (GMM `best_k=3`, ΔBIC≈157). A log-periodogram *does* find significant
  log-periodicity at ratio **≈9.96** against the smooth nulls (p≈0.002) — **but this
  is the well-known two-population glitch-size bimodality** (large Vela-type vs small
  Crab-type, ~1 dex apart): it **vanishes under the population-controlled GMM null**
  (p≈0.075), and the best ratio is **not** a preregistered TFPT value (13% off
  `(3/2)⁶`). The coarse candidates `8`, `8π` light up only because they ride on that
  ~1-dex spacing (`p_smooth<0.01` but `p_gmm>0.28`); `(3/2)⁶` has a raw `p_gmm=0.032`
  but **fails the look-elsewhere correction** (×7 candidates).
- **PG.02 / PG.03.** The decisive, bimodality-immune per-pulsar ladders are **null**
  (size frac 0.20 vs 0.19 chance, p≈0.27; waiting frac 0.22 vs 0.25 chance, p≈0.93;
  68/50 pulsars, 467/383 steps): consecutive glitch sizes and waiting times do **not**
  step by kernel factors. The within-pulsar null reorders each pulsar's raw size/interval
  set and *recomputes* the consecutive log-ratios, so the shuffle produces genuinely
  different ratios (the comb fraction is order-invariant, so permuting the already-computed
  ratios would be a tautology that always returns p=1.0).
- **PG.04 (recovery, Yu+2013).** The healing fraction `Q` is **not** clustered at
  `φ₀`-multiples (frac 0.10 vs ~0.22 chance, p≈1.0), the multi-component `τ_d` do **not**
  form the `(3/2)^k` ladder (p≈0.69), and — testing the *correct* v124 candidate — the
  2-mode **bend** `τ_long/τ_short = 2.7095` is also **null** (0/12, p≈1.0). The one
  positive note: the **wall** holds — 45/46 glitches are resolved into **≤2** decay modes,
  consistent with the `n=N_fam=3` pole (weak: most glitches are under-resolved). Real data,
  not `data_limited` any more.
- **Verdict: a clean cross-domain NULL / consistency.** The pulsar leg behaves
  exactly like the FRB energy-cascade result — real *generic* discreteness (here, the
  astrophysical bimodality), but **not** the TFPT recovery kernel. That is itself the
  useful cross-domain statement: the frozen kernel is **not** masquerading in a third,
  physically unrelated dataset.

The machinery is **injection-validated** (`tfpt-pulsar validate`): it recovers an
injected `(3/2)³` comb (p≈0.003, ratio 3.37) and rejects a synthetic *bimodal*
smooth distribution (p≈0.93) — so the PG.01 null is a real null, not a dead pipeline.

## PG.05 — the DYNAMIC recovery comb on real Crab ν(t) (NEW, `tfpt-pulsar dynamic`)

PG.01–04 test **static ratios**; PG.05 tests the **dynamical** signature on a real,
time-resolved recovery *waveform* — the one piece the size/`Q`/`τ_d` summaries lack. It uses
the **Jodrell Bank Crab monthly ephemeris** (`crab2.txt`, 479 monthly `ν`/`ν̇` points over
**1988–2026**, `scripts/fetch_crab_ephemeris.py`), the only public dataset with the wide
`ln(time)` reach the comb needs.

Pipeline (`src/tfpt_pulsar/nu_recovery.py`): detect glitches from the `ν̇` steps (10 found,
matching the known Crab glitches incl. the 2017 giant); for each clean inter-glitch segment build
the post-glitch `ν̇` recovery (secular braking removed); test whether a log-periodic comb at the
**kernel** `ω=2.583` is *special* vs a periodogram of off-kernel log-frequencies (a degree-2
polynomial-in-`ln τ` baseline absorbs the smooth recovery trend, so a pure power law is **not**
flagged).

**Result (real Crab `ν(t)`): `data_limited` — NO kernel comb, but the detector is validated.**

- **Injection validation on the real monthly sampling:** an injected geometric-ladder cascade comb
  is detected at `ω` (p≈0.002); a smooth power-law recovery is correctly **rejected** (p≈0.15).
  The detector works on exactly this cadence.
- **Real data:** across **7** clean inter-glitch segments (of 10 glitches over 38 yr) the kernel
  `ω` is **not** a special frequency in any (p≈0.12–0.44) — a clean null above the surrogate +
  look-elsewhere bar.
- **Honest scope:** monthly cadence undersamples the fast (days) transient, so PG.05 probes only the
  slow inter-glitch relaxation; with the comb amplitude predicted at `ε ~ exp(-π²/ln λ) ≈ 2%`, this
  is consistent with the signal being below monthly reach. **No claim.** The sharper test is
  **daily-cadence** timing of a giant glitch (Crab 2017) or Vela, resolving >2 decades in `ln(time)`.

## PG.06 — the dense J0537-6910 stacked recovery comb (HEAVY / optional, `tfpt-pulsar nicer`)

PG.05 was `data_limited` because the Crab *monthly* cadence under-samples the recovery. The
decisive dataset is **PSR J0537-6910, the "Big Glitcher"** — glitches every ~100 d, monitored
densely in X-rays (NICER 2017–, RXTE 1999–2011). `scripts/fetch_nicer_j0537.py` confirms the data
exist: **1165 NICER observations** of J0537 (MJD 57925–60833, ~8 yr, ~2948 ks; committed list
`data/nicer_j0537/j0537_observations.csv`). This stage scaffolds the full reduction **honestly**:

- **Upstream (gated, heavy):** fetch the cleaned **L2** events + orbit per ObsID from HEASARC
  (~GB; **not** auto-run), then **PINT** (`get_NICER_TOAs` + a satellite observatory from the
  `.orb`) barycentres + epoch-folds them to `nu(t)` — **no HEASoft/`nicerl2` needed** for the L2
  path. PINT is pip-installed; HEASoft is not (and isn't required). The bulk download + fold is a
  real project, so it is left to the operator; `nu_series_from_nicer` raises rather than fabricate.
- **Downstream (runs now, injection-validated):** `nu(t)` → per-glitch `nudot` recovery →
  superposed-epoch **stack** → the kernel-`omega` comb detector. The detector is validated over
  noisy realisations: in a **sufficient ln(tau) range** the comb is detected **96%** of the time
  with **0%** false positives.

**The key, machine-checked finding (it reframes the whole search):** the comb periodogram needs
**>~2.8 comb periods in ln(tau)** (≈3 decades in `tau`) to localise `omega`. A J0537 ~100 d
inter-glitch interval spans only **~1.9 periods**, where the same comb is detected **0%** of the
time — and **stacking many glitches buys amplitude SNR, NOT ln(tau) range**. So J0537, despite its
dense sampling, is **range-blind**; the decisive target is a **long-interval, densely-monitored**
pulsar — **Vela** (glitch every ~3 yr, daily timing → ~3 decades in `tau`, ~2.8 periods). Output:
`results/pg06_nicer_j0537.json` + `results/pg06_range_finding.png`. **Firewall:** search target,
no claim; the synthetic run validates machinery only.

## PG.06b — REAL NICER Vela-pulsar data: pipeline proven on real photons (`tfpt-pulsar vela`)

PG.06 pointed at a long-interval, densely-monitored pulsar → **Vela** (PSR B0833-45 / J0835-4510).
`scripts/fetch_nicer_vela.py` confirms the HEASARC NICER archive holds **665 Vela observations**
(MJD 57941–60817, ~7.9 yr, ~762 ks; ~6.5 GB of L2 events). `tfpt-pulsar vela --download` pulls one
real observation (~10 MB) and **`src/tfpt_pulsar/vela.py`** runs the reduction end-to-end:

> download cleaned **L2** events + orbit → **PINT** barycentres (`get_NICER_TOAs` + satellite
> observatory from the `.orb`, **no HEASoft**) → H-test fold.

**Real-data result (obsid 0020180102):** 430,739 photons barycentred; the **Vela pulsation is
DETECTED at F0 = 11.19275 Hz (period 89.34 ms, H = 18.4)** — exactly the Vela spin. **The
download → barycentre → fold pipeline is proven on REAL data**, with PINT alone (HEASoft not
installed and not needed).

**Honest wall (no claim).** A comb-*quality* `nu(t)` lives at the ~µHz level (the recovery
structure), so it needs a **phase-connected timing solution** across all 665 observations
(per-obs H-test gives only ~mHz). That is ~6.5 GB of events + a multi-hour PINT/`tempo2` timing
analysis + glitch handling — a real reduction project, **not** a sandbox fold. So PG.06b proves the
real-data pipeline and quantifies the remaining job; it does **not** fabricate a `nu(t)` or claim a
comb. Output: `results/pg06b_vela.json`.

**Offline reduction driver (`scripts/reduce_vela_nu_t.py`).** The full project wired end-to-end,
runnable on a workstation: STAGE 1 (automated) downloads + barycentres + coarse-folds every Vela
obs (resumable; `--max-obs 0` = all ~6.5 GB / hours) → `data/nicer_vela/vela_nu_perobs.csv`
(secular spin-down + big glitches at ~mHz); STAGE 2 (documented research step) = phase-connect the
TOAs with tempo2/PINT (+ glitch model) → `vela_nu_t.csv` at µHz; STAGE 3 hook = `detect_comb` at
ω=2.58 on that `nu(t)`. Tested here on one obs (F0=11.19275 Hz); the full run is offline by design.

## PG.07 — the recovery comb on the REAL 2024 Vela GIANT glitch (NEW, `tfpt-pulsar pg07`)

PG.06b proved the *pipeline* on real Vela photons but stopped at the honest wall: a comb-quality
`ν(t)` needs a **phase-connected** timing solution. PG.07 clears that wall using the one that is
already public. The **2024 April 29 Vela giant glitch** (PSR J0835−4510, MJD 60429.87) was caught
**live** (IAR/PuMA, first-reported; Mount Pleasant precise timing) and the LVK "Constraints on
gravitational waves from the 2024 Vela pulsar glitch" data release
(**Zenodo [10.5281/zenodo.17735648](https://doi.org/10.5281/zenodo.17735648) → record 17735649,
CC-BY-4.0**; A&A 698 A72 (2025) / arXiv:2512.17990) publishes the **phase-connected** TEMPO2 solution
`J0835-4510_long_F3.par`. `scripts/fetch_vela_2024.py` downloads it (~2 KB, committed as provenance)
and derives the small `nudot(τ)` recovery CSV. Real physics read off the `.par`:
**Δν/ν = 2.38×10⁻⁶** (a classic giant Vela glitch), a permanent {Δν, Δν̇} jump, and **three transient
recovery timescales τ_d = {0.39, 2.45, 15.1 d}** (matching A&A 698 A72's ~2.8 d + ~17 d + a fast
term), over a public post-glitch window of **122.7 d**.

`src/tfpt_pulsar/vela2024.py` reconstructs the post-glitch `nudot(τ)` recovery from that model and
runs the **PG.05 detector unchanged** (`nu_recovery.detect_comb`) plus the PG.06 range-power
machinery (`nicer_j0537`).

**Result (real 2024 Vela `ν̇(t)`): `data_limited` — the widest real recovery yet, detector validated,
no kernel comb, and the wall has MOVED off ln(τ)-range.**

- **Reach.** The 2024 window gives **2.55 comb periods** in ln(τ) — the **widest real recovery** the
  search has reached (vs J0537's ~1.9), a genuine step past PG.05/PG.06b.
- **Detector injection-validated on the real Vela cadence:** an injected geometric-cascade comb is
  detected at ω (p≈0.002); a smooth power-law recovery is rejected (p≈0.18).
- **ω=2.583 is NOT special** in the recovery: off-kernel periodogram **p≈0.23**, within-segment
  shuffle p≈0.60, and ω is **not the smallest-p member** of the off-kernel λ-battery (Bonferroni).
- **Range is no longer the wall.** Reusing PG.06's injection-validated range-power curve (reference
  amplitude ε=0.30), a strong comb at Vela-2024's 2.55 periods is localised **95%** of the time
  (vs **0%** at J0537's ~1.9); the smooth null false-positive rate is 0%. The **stacked**
  2016/2019/2021/2024 recoveries reach **3.41 periods** (2021's ~1012 d baseline + 535 d term) and
  are equally flat (p≈0.53) — stacking buys amplitude, **not** range (PG.06).
- **Honest scope (why it is `data_limited`, not a kill).** Two limits, neither of them ln(τ)-range:
  **(1)** the public product is the *smooth parametric glitch MODEL* (permanent jump + a few
  exponentials), **not the residual `ν(t)`** — a predicted **ε ~ exp(−π²/ln λ) ≈ 2%** comb, if it
  exists, lives in the **residuals to that fit**, which the small release does not contain, so any
  null here is null-by-construction; **(2)** at ~2% amplitude a single recovery is amplitude-limited,
  and only **~4** Vela giant glitches exist (stacking √N ≈ 2×, not enough). **Decisive next step:**
  the phase-connected IAR/MPRO ToA **residuals** over a full inter-glitch baseline (2021→2024 ~1012 d
  ≈ 2.8 periods), glitch model removed, superposed-epoch stacked. **No claim; firewall intact** — a
  hit would be a universal-DSI coincidence in the neutron-star interior, not a horizon signature and
  not TFPT confirmation. Output: `results/pg07_vela2024.json` + `results/pg07_vela2024.png`;
  preregistered in `hypotheses/pulsar_pg07_v1.yaml`.

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .   # numpy/scipy/matplotlib
pip install pint-pulsar                                            # for the PG.06/06b PINT fold
python scripts/fetch_glitches.py        # (optional) re-fetch JBO sizes; derived CSV is committed
python scripts/fetch_recovery.py        # (optional) re-fetch Yu+2013 Q/tau_d; derived CSV is committed
python scripts/fetch_crab_ephemeris.py  # (optional) re-fetch Crab nu(t); derived CSV is committed
tfpt-pulsar audit                       # frozen constants / candidate ratios
tfpt-pulsar validate                    # injection-recovery self-check of the machinery
tfpt-pulsar analyze                     # PG.01/02/03/04 (static) on the real catalogues -> results/
tfpt-pulsar dynamic                     # PG.05 dynamic recovery comb (omega=2.58) on real Crab nu(t)
python scripts/fetch_nicer_j0537.py     # PG.06: confirm + list the 1165 NICER J0537 observations
tfpt-pulsar nicer                       # PG.06 scaffold: env + plan + downstream comb (injection-validated)
python scripts/fetch_nicer_vela.py      # PG.06b: confirm + list the 665 NICER Vela-pulsar observations
tfpt-pulsar vela --download             # PG.06b: download one real Vela obs + PINT-fold -> detect the pulsation
python scripts/fetch_vela_2024.py       # PG.07: download the 2024 Vela glitch phase-connected .par (Zenodo)
tfpt-pulsar pg07                        # PG.07: recovery comb (omega=2.58) on the REAL 2024 Vela giant glitch
# or without install:  PYTHONPATH=src python -m tfpt_pulsar.cli analyze
```

## Layout

```
scripts/fetch_glitches.py        # download + parse Jodrell Bank gTable.html -> data/jbo_glitches.csv
scripts/fetch_recovery.py        # download + parse Yu+2013 expTab.tex   -> data/yu2013_recovery.csv
scripts/fetch_crab_ephemeris.py  # download + parse Crab crab2.txt       -> data/crab_ephemeris.csv (PG.05)
scripts/fetch_nicer_j0537.py     # HEASARC nicermastr -> data/nicer_j0537/j0537_observations.csv (PG.06)
scripts/fetch_nicer_vela.py      # HEASARC nicermastr -> data/nicer_vela/vela_observations.csv (PG.06b)
scripts/reduce_vela_nu_t.py      # OFFLINE heavy driver: download+barycentre+fold all Vela obs -> nu(t) (PG.06b)
scripts/fetch_vela_2024.py       # PG.07: download 2024 Vela glitch .par (Zenodo 17735649) -> data/vela_2024/
data/jbo_glitches.csv            # committed derived size catalogue (726 glitches)
data/yu2013_recovery.csv         # committed derived recovery table (60 Q/tau_d components, 46 glitches)
data/crab_ephemeris.csv          # committed derived Crab nu/nudot(t) monthly series (479 points, PG.05)
data/nicer_j0537/j0537_observations.csv  # committed list of 1165 NICER J0537 observations (PG.06)
src/tfpt_pulsar/constants.py     # frozen TFPT kernel + phi0 + preregistered candidate ratios
src/tfpt_pulsar/catalog.py       # HTML/TeX/ephemeris parsers + CSV loaders + grouping
src/tfpt_pulsar/discreteness.py  # PG.01: log-periodicity + GMM + 3 nulls (lognormal/KDE/population)
src/tfpt_pulsar/ratios.py        # PG.02/03: per-pulsar size + waiting-time kernel ladders (shuffle null)
src/tfpt_pulsar/recovery.py      # PG.04: Q-cluster (phi0 multiples) + tau_d multi-timescale ladder
src/tfpt_pulsar/dsi.py           # discrete-scale-invariance predictor (omega=2pi/ln lambda)
src/tfpt_pulsar/nu_recovery.py   # PG.05: dynamic recovery comb (omega=2.58) on real Crab nu(t) + injection
src/tfpt_pulsar/nicer_j0537.py   # PG.06: J0537 stacked-recovery scaffold (PINT upstream + comb downstream)
src/tfpt_pulsar/vela.py          # PG.06b: REAL NICER Vela download + PINT barycentre + H-test fold
src/tfpt_pulsar/vela2024.py      # PG.07: recovery comb on the REAL 2024 Vela giant glitch (.par model)
src/tfpt_pulsar/validation.py    # injection-recovery self-check
src/tfpt_pulsar/cli.py           # `tfpt-pulsar audit|validate|analyze|dynamic|nicer|vela|pg07`
data/nicer_vela/vela_observations.csv  # committed list of 665 NICER Vela-pulsar observations (PG.06b)
data/vela_2024/J0835-4510_long_F3.par  # committed phase-connected 2024 Vela glitch ephemeris (PG.07)
data/vela_2024/vela2024_nudot.csv      # committed derived post-glitch nudot(tau) recovery (PG.07)
data/vela_2024/vela_glitch_recoveries.csv  # committed Vela giant-glitch recovery params 2016-2024 (PG.07)
hypotheses/pulsar_pg07_v1.yaml   # preregistered PG.07 hypothesis (frozen kernel, nulls, kill/data-limited)
results/results.json             # committed summary (+ pg01/pg05/pg06 png, gitignored)
results/pg05_recovery_comb.json, pg06_nicer_j0537.json, pg06b_vela.json, pg07_vela2024.json  # committed summaries
```
