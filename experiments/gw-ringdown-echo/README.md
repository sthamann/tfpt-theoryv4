# TFPT GW ringdown echoes — `(2/3)⁶` ratio (Stage 0/1) + dynamic walled-clock recovery (Stage 2)

`search.txt` §5: if post-merger boundary recovery imprints echoes on the black-hole
ringdown, their amplitude ratio is bounded by the **same** recovery eigenvalue that
governs FRBs and flavour:

```
A_{n+1} / A_n  ≤  λ₂ = (2/3)⁶ = 64/729 ≈ 0.0878        (lag free, ratio frozen)
```

It is an **upper bound**, so this is a consistency / upper-limit channel.

## Stage = `catalog_feasibility` (NOT a strain-level echo test)

This experiment is a **GWTC-5.0 catalogue-based feasibility and sensitivity census**;
**strain-level matched filtering is still pending**. It makes **no** echo detection or
non-detection claim. It only forecasts whether a future stacked strain search *could*
detect or bound a `(2/3)⁶` echo, to decide if that search is worth running.

The real test (Stage 1) is separate: high-ringdown-SNR events → Kerr ringdown
subtraction → matched filter on residuals (free lag, free phase, **fixed** ratio) →
injection campaign with `q=(2/3)⁶` → free-`q` control template → time-slide nulls.
Only after that may "null", "hint" or "bound" be written.

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
at the frozen amplitude ratio `(2/3)⁶` (free lag, free-`q` control). Real strain (GW150914,
GW190521) → **no faint kernel-ratio echo coincident in ≥2 detectors**; low-`p` excesses have
`q̂ ~ 1` (residual ringdown power, free-ratio-rejected). Consistent with the upper bound; no claim.

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
background `p`-value. **Result on real strain (GW150914, GW190521): `NO_KERNEL_RECOVERY`** —
where the envelope decays it is leftover single-mode ringdown (profiled `q̂≈1`, not the bend
2.7095).

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
python scripts/fetch_strain.py GW150914 GW190521   # real 32 s strain -> data/strain/
tfpt-gw realdata                      # Stage 1 static (2/3)^6 echo on real strain
tfpt-gw dynamic                       # Stage 2 dynamic walled-clock recovery on real strain
```

## Layout

```
scripts/fetch_catalog.py    # download GWTC event list from GWOSC -> data/gwtc_events.csv
scripts/fetch_strain.py     # download 32 s, 4 kHz HDF5 strain per event -> data/strain/
src/tfpt_gw/constants.py    # frozen ratio (2/3)^6; STAGE
src/tfpt_gw/echo_forecast.py# Stage 0 per-event + stacked echo-SNR sensitivity census
src/tfpt_gw/echo_search.py  # Stage 1 synthetic echo-train injection-recovery (validated 3/3)
src/tfpt_gw/strain_data.py  # real GWOSC HDF5 I/O + whitening + Kerr QNM (Berti+ 2006)
src/tfpt_gw/real_echo_search.py # Stage 1 static (2/3)^6 echo train on real strain
src/tfpt_gw/dynamic_recovery.py # Stage 2 dynamic walled-clock (bend 2.7095) on real strain
src/tfpt_gw/cli.py          # `tfpt-gw analyze | search | realdata | dynamic`
data/gwtc_events.csv        # real LVK GWTC-5.0 catalogue (390 canonical; 391 raw rows)
data/strain/                # real 32 s HDF5 strain (gitignored) + <event>_meta.json
event_count_audit.md        # 390 vs 391 reconciliation + selection accounting
results/dynamic_recovery.json,.png  # Stage 2 output + figure
```
