# Evidence scorecard schema (summary)

Source of truth: `experiments/evidence_scorecard.json`  
Generator: `experiments/build_evidence_scorecard.py` (breaks on invalid enums)

## Row identity

One typed row per `(domain, observable)`.

Core fields: `domain`, `observable`, `tfpt_value`, `data_value`, `pull_sigma`, `claim_type`, `bridge_type`, `stage`, `source`, `kill_condition`, `status`

Metadata (anti double-counting): `independence_group`, `discriminative_power`, `decision_horizon`, `evidence_class`, `hint_flag`, `alternative_group`, `watch_flag`

## Fixed enums

**stage:** `prediction_of_record` · `downstream_bridge` · `search_target` · `catalog_feasibility` · `strain_level_test` · `parked_analog` · `not_applicable`

**status:** `consistent` · `hint` · `tension` · `null` · `kill_channel` · `data_limited` · `parked`

**evidence_class:** `external_data` · `internal_consistency` · `downstream_bridge` · `search_target` · `parked`

## independence_group (correlated legs ≠ independent hits)

| Group | Examples |
|-------|----------|
| `phi0_seed` | β, Ω_b, θ12, θ13, Cabibbo, seed line, FRB.05 |
| `alpha_em` | Λ hierarchy, S_dS |
| `N_star_reheating` | Inflation A_s branch |
| `c3_topform_horizon` | EHT from 16c₃⁴ |
| `independent` | default for unrelated legs |

## alternative_group (one question, multiple readings — don't double-count)

`Nstar_branch` · `HVP_baseline` · `axion_branch` · `w_de_eos`

## What never goes in the scorecard

- `experiments/theory-contracts/` rows (pure math)
- Internal CPTP/QEC/Page checks → `evidence_class=internal_consistency`, often `stage=not_applicable`
- Load-bearing verification checks that belong in `status_ledger.csv` instead

## Empirical search quality bar (FRB-style)

- Preregistered hypotheses before looking
- Surrogate null batteries (shuffle, AR(1), block, placebo)
- Observable semantics locked (energy vs amplitude channels)
- Multi-source replication for any "support" claim
- Explicit kill conditions per row
