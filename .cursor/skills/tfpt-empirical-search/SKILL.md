---
name: tfpt-empirical-search
description: >-
  Build or extend preregistered TFPT empirical searches (FRB, GW echo, pulsar glitch,
  recovery-comb, EHT). Covers frozen kernel, null batteries, surrogate calibration,
  verdict enums, and firewall. Use for experiments/frb-*, gw-ringdown-*, pulsar-*,
  recovery-comb-domains, eht-*, preregistered hypothesis YAML, or search_target rows.
---

# TFPT empirical search

Template projects: `frb-tfpt-signatures`, `gw-ringdown-echo`, `pulsar-glitch-recovery`, `recovery-comb-domains`, `eht-achromatic-residual`.

Goal: **find a replicated discriminating signature OR kill it cleanly** — not "find more numbers".

## Before coding

1. Read experiment README firewall paragraph
2. Preregister hypotheses in `hypotheses/*.yaml` **before** looking at data
3. Lock observable semantics (energy vs amplitude, pole vs source, etc.)
4. Define kill conditions per axis

## Frozen kernel

- Ratios are **exact rationals from axioms** — no fitted exponents
- Guard with `tests/` (e.g. `test_recovery_kernel_constants.py`, language rules)
- Common static ratios: `(2/3)^6 = 64/729`, `(2/3)^3 = 8/27`, step `2/3`
- Dynamic signature: recovery comb `ω ≈ 2.58` (= `2π/ln((3/2)^6)`), wall at `N_fam=3`, bend `g1/g2 = ln3/ln(3/2) ≈ 2.7095`

**Observable semantics (FRB lesson):** energy ratio → `64/729`; amplitude ratio → `8/27`. Wrong pairing = flagged audit anomaly, not a candidate.

## Project structure

```
hypotheses/<name>.yaml    # preregistered tests + kill conditions
src/<pkg>/                # analysis modules per axis (FRB.01, PG.05, …)
tests/                    # kernel freeze, semantics guards
data/                     # public data, document fetch scripts
results/results.json      # deterministic CLI output (scorecard source)
scripts/fetch_*.py        # data ingestion
```

CLI pattern: `PYTHONPATH=src python -m <pkg>.cli analyze --seed 0`

## Null batteries (mandatory for search axes)

Run multiple conservative nulls per test; report max-p or Bonferroni where stated:

| Null type | Catches |
|-----------|---------|
| Within-session shuffle | Random pile-up in one burst/session |
| Block / time shuffle | Structured drift masquerading as pattern |
| AR(1) energy / drift | Smooth autocorrelated false positives |
| Placebo controls | Arbitrary control breaks (FRB.06) |
| Free-quotient (FRB.02b) | Best-fit non-kernel ratio with LEE correction |
| Injection-recovery | Detector validates before real data |

**Support** requires ≥2 independent sources, BH-q < 0.01, semantically valid observable — not a single-source pile-up.

## Verdict language (honest)

| Verdict | Meaning |
|---------|---------|
| `null` | Well-powered; pattern absent (good outcome) |
| `consistent` | TFPT not contradicted; often standard physics agrees |
| `data_limited` | Right test, insufficient data/reach (document why) |
| `tension` | Data pulls against TFPT (rare; needs pull_sigma) |
| `not_confirmed_not_refuted` | Mixed; no replicated discriminating support |
| `hint_flag` | Too weak for `hint` status → stay `data_limited` |

Never upgrade to load-bearing `[E]` or paper `\veri{}` from a search null/consistency alone.

## Firewall reminders

- FRB/GW/pulsar/recovery-comb: **boundary-recovery search**, not direct Hawking / new gravity
- Horizon-direct (Hod QNM `ln3`, Hawking power): **outside** FRB firewall unless explicitly scoped
- Surface channels (AGN disk TDE, accretion): same legitimacy as magnetar/GRB — a hit would be universal-DSI coincidence, not TFPT confirmation
- AGN-scheiben-TDE at high-z: time dilation shifts phase in `ln(t)`, does not add ln-range

## Scorecard integration

After CLI run updates `results/results.json`:

1. Sync row values in `experiments/build_evidence_scorecard.py` → `ROWS`
2. `python experiments/build_evidence_scorecard.py`
3. Use skill **`tfpt-evidence-scorecard`** for enum typing

Typical row: `stage=search_target`, `evidence_class=search_target` or `external_data`.

## Completion checklist

- [ ] Hypotheses preregistered before data pass
- [ ] Kernel frozen + tests green
- [ ] Observable semantics documented in README
- [ ] Null batteries run; verdict enum stated
- [ ] `results.json` committed; scorecard row synced
- [ ] README verdict section updated (current version, multi-source counts)
- [ ] No touch of verification/ledger unless promoting (skill: `promote-to-verification`)

## Reference

FRB prereg example: `experiments/frb-tfpt-signatures/hypotheses/frb_tfpt_v1.yaml`  
Catalog: `experiments/README.md` §1, §9
