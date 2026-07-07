# UHECR energy-spectrum DSI — the largest ln-E range in nature

> **Firewall:** a **search target / consistency check**, never a load-bearing claim.
> The transduction `B` (why the cosmic-ray source population should carry seam
> modes) is unproven → exploratory **surface probe** (S7 size-space class); a hit
> would be escalate-only (universal DSI / source-population coincidence stays the
> default reading). Preregistered in `hypotheses/uhecr_dsi_v1.yaml` **before** any
> comb/likelihood statistic ran; the data audit (counts/ranges/columns only) is on
> record in the YAML header.

## Why this bed

The ultra-high-energy cosmic-ray spectrum offers the **largest ln-E range in
nature**: the Auger Open Data (release 3, Zenodo DOI `10.5281/zenodo.10488964` —
10 % of published events) span **0.1 → 144 EeV = 7.27 e-folds = 2.99 comb
periods** above the full-efficiency thresholds, where the aperture is purely
geometrical (flat in energy) — the ln E event distribution is spectrum shape ×
constant. Each array alone is *below* the 2.8-period gate (SD1500: 1.67; SD750:
2.56); the gate is only cleared by the **combined** fit (per-array smooth models
+ ONE shared comb).

## Data (fetched by `scripts/fetch_data.py`, committed under `data/summary/`)

| leg | selection (frozen) | n |
|---|---|---|
| SD1500 vertical | `sd_energy ≥ 2.5 EeV`, `θ ≤ 60°` | 21,571 |
| SD750 | `sd_energy ≥ 0.1 EeV`, `θ ≤ 55°` | 54,434 |
| inclined | excluded (separate 4-EeV aperture, 2.4k events) | — |

46 duplicate `gpstime` events between arrays deduped (SD1500 preferred). Energy
resolution σ(ln E) ≈ 0.07–0.17 attenuates a kernel comb by ≤ 3 % — negligible.

## Method (prereg)

Binned Poisson (200 bins in ln E per array); smooth null = piecewise-linear
log-density with knots **frozen at the published spectral features** (second
knee 0.16 EeV, ankle 5.0, instep 12.6, suppression 45.7 EeV — Auger PRD 102
(2020) 062005 / EPJ C 81 (2021) 966), slopes free — so the smooth model cannot
absorb or fake a comb (the PG.01/KC.03 population-feature lesson, by
construction). Comb alternative = one multiplicative decoration
`1 + a cos(ωx) + b sin(ωx)` **shared** by both arrays at the frozen
`ω = 2π/ln((3/2)⁶) = 2.5827`. Statistic Λ = 2ΔlnL, two-stage fit applied
identically to data and Monte-Carlo draws. Nulls: 400 MC draws from the fitted
smooth model (p_MC); off-kernel rank over 60 log-spaced ω ∈ [0.6, 8]; Z₂/Möbius
λ battery with per-λ reach gate and **per-ω MC calibration**;
injection-recovery at ε = 0.05 and at the predicted ε = 0.0173.

## Result (seed 0; seed 1 agrees) — **null**

- **Kernel comb absent:** Λ_obs = 0.153 (fitted ε̂ = 0.0018), **p_MC = 0.49**;
  off-kernel rank **p = 0.77** — the frozen ω is not special anywhere in the band.
- **Z₂ battery null:** (3/2)³ p_raw = 0.13, (3/2)⁴ p_raw = 0.78 (per-ω
  calibrated; Bonferroni **0.26**); (3/2)¹² range-blind (1.49 periods < 2.8) —
  the same antiperiodic-fundamental blindness as every other bed.
  *Audit note:* under the (wrong) kernel-ω null the (3/2)³ leg had nominally
  fired at p = 0.0025 — the per-ω calibration (the null Λ distribution grows
  with ω because the smooth model absorbs less comb power there) dissolves it;
  kept on record as a method lesson.
- **Power:** injection at ε = 0.05 detected **97 %**; at the predicted
  ε = 0.0173 only **23 %** → the null *constrains but does not kill* the
  predicted amplitude (partially covered; the full-statistics Auger dataset —
  10× the open release — would reach it).

**Verdict: `null`** for a size-space comb at the kernel scale factor on the
largest ln-E range in nature; the predicted-amplitude leg is partially covered
(power 23 %). A future full-statistics spectrum (or TA + Auger jointly) is the
dated decider for the 1.7 % level.

## Reproduce

```bash
python scripts/fetch_data.py                     # Zenodo summary.zip -> data/summary/
python tests/test_frozen_kernel.py               # 8/8 guard
PYTHONPATH=src python -m tfpt_uhecr.analysis --seed 0   # -> results/results.json
```

## Layout

```
hypotheses/uhecr_dsi_v1.yaml   # preregistered selection, knots, nulls, kill conditions
scripts/fetch_data.py          # Zenodo release-3 summary fetch
src/tfpt_uhecr/analysis.py     # two-stage Poisson fit + MC + rank + battery + injections
tests/test_frozen_kernel.py    # kernel/selection/knot freeze guard (8 checks)
data/summary/*.csv             # committed Auger Open Data summary tables (~8 MB)
results/results.json           # committed run (seed 0)
```
