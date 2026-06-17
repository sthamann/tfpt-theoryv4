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
(`ν(t)` after a glitch): a **matched filter** with the fixed-ratio (2.7095) two-exponential template,
built and validated in `quantum-testbed` QT.04. (Sustained log-periodic DSI returns only across a
*cascade* of events, never within one walled recovery.)

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

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .   # numpy/scipy/matplotlib
python scripts/fetch_glitches.py        # (optional) re-fetch JBO sizes; derived CSV is committed
python scripts/fetch_recovery.py        # (optional) re-fetch Yu+2013 Q/tau_d; derived CSV is committed
tfpt-pulsar audit                       # frozen constants / candidate ratios
tfpt-pulsar validate                    # injection-recovery self-check of the machinery
tfpt-pulsar analyze                     # PG.01/02/03/04 on the real catalogues -> results/
# or without install:  PYTHONPATH=src python -m tfpt_pulsar.cli analyze
```

## Layout

```
scripts/fetch_glitches.py        # download + parse Jodrell Bank gTable.html -> data/jbo_glitches.csv
scripts/fetch_recovery.py        # download + parse Yu+2013 expTab.tex   -> data/yu2013_recovery.csv
data/jbo_glitches.csv            # committed derived size catalogue (726 glitches)
data/yu2013_recovery.csv         # committed derived recovery table (60 Q/tau_d components, 46 glitches)
src/tfpt_pulsar/constants.py     # frozen TFPT kernel + phi0 + preregistered candidate ratios
src/tfpt_pulsar/catalog.py       # HTML/TeX parsers + CSV loaders + per-pulsar/per-glitch grouping
src/tfpt_pulsar/discreteness.py  # PG.01: log-periodicity + GMM + 3 nulls (lognormal/KDE/population)
src/tfpt_pulsar/ratios.py        # PG.02/03: per-pulsar size + waiting-time kernel ladders (shuffle null)
src/tfpt_pulsar/recovery.py      # PG.04: Q-cluster (phi0 multiples) + tau_d multi-timescale ladder
src/tfpt_pulsar/dsi.py           # discrete-scale-invariance predictor (omega=2pi/ln lambda) -- the dynamical signature
src/tfpt_pulsar/validation.py    # injection-recovery self-check
src/tfpt_pulsar/cli.py           # `tfpt-pulsar audit|validate|analyze`
results/results.json             # committed summary (+ pg01_periodogram.png, gitignored)
```
