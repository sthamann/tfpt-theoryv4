# GWTC event-count audit

Reconciles the local download with the canonical LVK headline so the difference is
transparent (a reviewer who sees "391" vs "390" gets the answer here).

## Numbers

| symbol | value | meaning |
|---|---|---|
| `N_canonical` | **390** | LVK headline: cumulative confident events in GWTC-5.0 (161 new in O4b) — LSC O4b catalog page |
| `N_raw_rows` | **391** | rows in `data/gwtc_events.csv` from the GWOSC `eventapi/json/GWTC/` aggregate (version-deduplicated; 391 unique `commonName`, no duplicates) |
| `N_selected_BBH` | **278** | rows used by the echo forecast (`mfinal ≥ 5 M☉`, finite network SNR) |

## Composition of the 391 raw rows (by source sub-catalogue)

| sub-catalogue | rows |
|---|---|
| GWTC-5.0 (O4b, new) | 161 |
| GWTC-4.1 | 140 |
| GWTC-3-confident | 35 |
| GWTC-2.1-confident | 54 |
| GWTC-1-confident | 1 (GW170817, BNS) |
| **total** | **391** |

## The 391 vs 390 difference

The GWOSC aggregate returns the latest version of every confident event across all
sub-catalogues (391 unique names, no duplicates). The LVK headline "390" is a
cumulative-confident bookkeeping count whose exact definition differs by **one**
event from the GWOSC aggregate. The single most plausible difference is the lone
legacy `GWTC-1-confident` row, **GW170817** (a binary neutron star), which is folded
differently in the cumulative count.

This is a bookkeeping reconciliation, not a physics issue: **GW170817 is a BNS with
`M_final ≈ 2.8 M☉` and is excluded from the BBH ringdown selection regardless**, so it
does not enter the 278-event census or any echo forecast number.

## Selection classes (391 → 278)

| step | removed | remaining | reason |
|---|---|---|---|
| raw rows | — | 391 | GWOSC aggregate |
| no published source-frame final mass | 112 | 279 | recent O4b events without a published `final_mass_source` (no ringdown remnant mass ⇒ cannot enter the forecast) |
| `M_final < 5 M☉` | 1 (GW170817) | 278 | BNS / light remnant, not a BH ringdown |
| **selected BBH** | — | **278** | finite SNR + BH ringdown remnant |

## Stage

This experiment is **`catalog_feasibility`**, not a strain-level echo test. The
278-event census forecasts whether a stacked strain search *could* detect or bound a
`(2/3)⁶` echo; it makes **no** echo detection/non-detection claim. The strain-level
matched-filter test (Kerr ringdown subtraction, free lag/phase, fixed ratio, injection
campaign, free-`q` control) is pending and is a separate stage.
