# TFPT GW ringdown echoes — `(2/3)⁶` amplitude-ratio (catalog feasibility, Stage 0)

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

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .
python scripts/fetch_catalog.py     # re-download GWTC from GWOSC
tfpt-gw analyze                      # or: PYTHONPATH=src python -m tfpt_gw.cli analyze
```

## Layout

```
scripts/fetch_catalog.py    # download GWTC event list from GWOSC -> data/gwtc_events.csv
src/tfpt_gw/constants.py    # frozen ratio (2/3)^6; STAGE = catalog_feasibility
src/tfpt_gw/echo_forecast.py# per-event + stacked echo-SNR sensitivity census
src/tfpt_gw/cli.py          # `tfpt-gw analyze`
data/gwtc_events.csv        # real LVK GWTC-5.0 catalogue (390 canonical; 391 raw rows)
event_count_audit.md        # 390 vs 391 reconciliation + selection accounting
```
