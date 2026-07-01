---
name: tfpt-evidence-scorecard
description: >-
  Add or update rows in experiments/evidence_scorecard.json via build_evidence_scorecard.py,
  with correct stage/status/evidence_class enums and anti double-counting metadata. Use when
  experiment results change, scorecard stats update, or website predictions.ts needs sync.
---

# TFPT evidence scorecard

Central typed index of all **empirical** confrontations across `experiments/`.

- **Source:** `experiments/evidence_scorecard.json` (generated)
- **Editor:** `experiments/build_evidence_scorecard.py` — edit `ROWS` list, then regenerate
- **NOT for:** theory-contracts, load-bearing verification ledger rows, internal CPTP checks without external data

```bash
python experiments/build_evidence_scorecard.py
```

Regenerates JSON + `<!-- SCORECARD_STATS -->` block in `experiments/README.md`.

## Workflow

1. Run experiment CLI → update `results/results.json`
2. Edit matching row(s) in `build_evidence_scorecard.py` `ROWS`
3. Set metadata fields (see [schema.md](schema.md))
4. Run generator — **fails on invalid enums**
5. If user-visible on website: check `website/lib/predictions.ts` mirror

## Row shape (ROWS tuple order)

```
domain, observable, tfpt_value, data_value, pull_sigma,
claim_type, bridge_type, stage, source, kill_condition, status
```

Plus optional dict keys appended per row in generator: `independence_group`, `evidence_class`, `discriminative_power`, `decision_horizon`, `hint_flag`, `alternative_group`, `watch_flag`, composite fields.

## Fixed enums (generator enforces)

**stage:** `prediction_of_record` · `downstream_bridge` · `search_target` · `catalog_feasibility` · `strain_level_test` · `parked_analog` · `not_applicable`

**status:** `consistent` · `hint` · `tension` · `null` · `kill_channel` · `data_limited` · `parked`

**evidence_class:** `external_data` · `internal_consistency` · `downstream_bridge` · `search_target` · `parked`

## Anti double-counting (mandatory)

| Field | Rule |
|-------|------|
| `independence_group` | Correlated legs share a group — **not independent hits**. `phi0_seed`: β, Ω_b, θ12, θ13, Cabibbo, seed line. `alpha_em`, `N_star_reheating`, `c3_topform_horizon`, `independent`. |
| `alternative_group` | One question, multiple readings — never double-count. `Nstar_branch`, `HVP_baseline`, `axion_branch`, `w_de_eos`. |
| `evidence_class=internal_consistency` | No external measurement — separate from `external_data` basket |
| `discriminative_power=weak` | Standard physics predicts same value (Ω_b, v_GW=c, Λ order) |

README stats are **auto-generated only** — never hand-edit counts in `experiments/README.md`.

## Website mirror

`website/lib/predictions.ts` references `experiments/evidence_scorecard.json` for the audit surface. Update prose there only when prediction **presentation** changes — numbers come from scorecard/regenerator.

Experiment-only work: **no** `bash build.sh audit` required unless verification/papers touched.

## What never goes in the scorecard

- `experiments/theory-contracts/` (pure math → `tfpt_research_contracts` if promoted)
- Load-bearing checks that belong in `verification/status_ledger.csv`
- Silent status upgrades to `[E]` in papers

## Checklist

- [ ] Values match latest `results/results.json` / experiment README
- [ ] Enums valid; generator passes
- [ ] `independence_group` / `alternative_group` set where correlated
- [ ] Kill condition explicit per row
- [ ] README stats block refreshed by generator
- [ ] `predictions.ts` updated if user-visible prediction surface changed

Full schema: [schema.md](schema.md)
