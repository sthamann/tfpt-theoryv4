# Scorecard schema reference

## Core fields

| Field | Purpose |
|-------|---------|
| `domain` | Experiment domain (FRB, CMB, GW, Pulsar, …) |
| `observable` | Test id + short label (e.g. `echo ratios (FRB.02)`) |
| `tfpt_value` | Frozen TFPT prediction or search target |
| `data_value` | What data showed (with source scope) |
| `pull_sigma` | Numeric tension if applicable; `None` for null/search |
| `claim_type` | e.g. `search_target`, `prediction`, `downstream_bridge` |
| `bridge_type` | Physical bridge class (honest scope) |
| `stage` | Enum — see below |
| `source` | Data provenance |
| `kill_condition` | Explicit falsification trigger |
| `status` | Enum — see below |

## Metadata fields

| Field | Values / notes |
|-------|----------------|
| `independence_group` | `phi0_seed` · `alpha_em` · `N_star_reheating` · `c3_topform_horizon` · `independent` |
| `alternative_group` | `Nstar_branch` · `HVP_baseline` · `axion_branch` · `w_de_eos` |
| `evidence_class` | `external_data` · `internal_consistency` · `downstream_bridge` · `search_target` · `parked` |
| `discriminative_power` | `internal` · `weak` · `medium` |
| `decision_horizon` | `near_term` · `mid_term` · `long_term` |
| `hint_flag` | `true` when too cold for `status=hint` → use `data_limited` |
| `watch_flag` | Sharpest non-red channel (e.g. dark energy `w`) |
| `validation_tier` | Evidence-ladder rung for analog/lab rows: `instrument_validated` (readout chain proven on real hardware, e.g. EIT S_off, QC kernel) · `analog_positive_control` (engineered positive measured, e.g. a future EIT H3 pass). Nature rows carry no tier — keeps analog validation out of the nature-evidence count. |
| `signature_code` | Optional SIGNATURES.md family tag (`S1`…`S15`, composites such as `S2b/S11`, or `detector-control`) |
| `leakage_class` | New 2026-07-06 typing: `core_operator` · `architecture_core` · `internal_kernel` · `surface_leakage` · `search_target` · `downstream_bridge` · `external_data` · `detector_control` · `parked` |
| `clock_map` | Whether a log-time/phase clock is justified (`operator_clock_read_off_from_boundary_map`, `engineered_transfer_steps`, `observer_time_or_surface_clock_unjustified`, etc.) |
| `transduction_B` | Observable eligibility gate: named readout/coupling `B`, or `missing_or_unproven` for surface-leakage probes |
| `projection_nonzero` | Observable eligibility gate: why the relevant character/mode is visible, or `not_established` |

## stage semantics

| stage | Use |
|-------|-----|
| `prediction_of_record` | Frozen compiler prediction vs data |
| `downstream_bridge` | F_transfer / RGE / lab bridge |
| `search_target` | Preregistered search (FRB, GW echo, …) |
| `catalog_feasibility` | Feasibility / census only |
| `strain_level_test` | GW strain-level null |
| `parked_analog` | No physical dataset |
| `not_applicable` | Internal consistency (Recovery-Channel, Page, S_dS identity) |

## leakage_class semantics

| leakage_class | Use |
|----------------|-----|
| `core_operator` | Direct operator/character-invariance readout (e.g. QGEO S_off / EIT instrument validation) |
| `architecture_core` | Cross-pipeline architecture/seed or phase-family test, not an emission bridge |
| `internal_kernel` | Internal or engineered kernel check; no external nature evidence |
| `surface_leakage` | Astrophysical/lab observable that probes `O = B·T·A` without a proven nonzero `B·P_r` |
| `search_target` | Search row without a stronger core/surface typing |
| `downstream_bridge` | F_transfer/RGE/lab bridge row |
| `external_data` | Direct prediction-of-record vs external measurement |
| `detector_control` | Negative/false-positive control of the detector, not TFPT evidence |
| `parked` | No active dataset |

## status semantics

| status | Use |
|--------|-----|
| `consistent` | Not contradicted; may be non-discriminating |
| `null` | Well-powered absence of search pattern |
| `tension` | Data pulls against TFPT |
| `data_limited` | Correct test, insufficient power/reach |
| `hint` | Rare; needs strong evidence (prefer `data_limited` + `hint_flag`) |
| `kill_channel` | Explicit kill test triggered |
| `parked` | Not active |

## Editing pattern in build_evidence_scorecard.py

```python
["FRB", "echo ratios (FRB.02)", "E_{n+1}/E_n=64/729; amp 8/27",
 "no theory-channel excess (4 sources)", None, "search_target", "boundary recovery kernel",
 "search_target", "FAST 1652 + Blinkverse", "free quotient wins away from kernel", "null"],
```

Optional metadata passed as dict merge after tuple — follow existing rows in the file for the pattern used by the generator.
