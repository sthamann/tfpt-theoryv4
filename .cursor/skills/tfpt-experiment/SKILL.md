---
name: tfpt-experiment
description: >-
  Work in TFPT experiments/ without touching the load-bearing verification suite.
  Covers firewall rules, experiment layout, scorecard vs theory-contracts, and when
  to stay standalone. Use when editing experiments/, adding empirical searches,
  updating evidence_scorecard.json, or when the user says exploration, search target,
  or experiment-only.
---

# TFPT Experiments

`experiments/` holds **search surfaces and consistency checks** — not load-bearing claims.
The verification suite (`verification/vN_*.py`) + papers + ledger are the compiler output.

## Three buckets (never mix)

| Bucket | Location | Goes into papers? | Scorecard? |
|--------|----------|-------------------|------------|
| **Empirical confrontation** | `experiments/<name>/` | No (unless promoted) | Yes → `evidence_scorecard.json` |
| **Theory contract** | `experiments/theory-contracts/` | Maybe later in `tfpt_research_contracts` | **Never** |
| **Load-bearing check** | `verification/vN_*.py` | **Yes** (`\veri{}` in body) | Separate ledger row |

Promotion from experiment → verification: use skill **`promote-to-verification`**.

## Firewall (mandatory)

- Experiments are **search targets, not claims** — verdicts like `null`, `consistent`, `data_limited`, `not_confirmed_not_refuted`.
- **Never silently upgrade** to `[E]` or load-bearing language in papers/README/website.
- FRB / GW echo / pulsar / recovery-comb: **residual boundary-recovery patterns**, not direct Hawking emission or new gravity.
- Horizon-direct structures (Hod QNM `ln3`, Hawking power) belong **outside** FRB/GW firewall tests unless explicitly scoped.
- Frontier observables (Koide, η_B, axion, g−2, kaons) are **`F_transfer` bridges** — never primitive compiler outputs.
- A null result is a **valid, well-powered outcome** — document it honestly.

## Standard project layout

```
experiments/<name>/
├── README.md          # setup, run, verdict, firewall paragraph
├── pyproject.toml     # self-contained deps
├── src/<pkg>/         # importable package
│   └── cli.py         # audit surface: analyze, fetch-*, validate
├── data/              # committed or fetched (document source)
├── results/           # generated outputs (often gitignored)
├── hypotheses/        # preregistered YAML (search projects)
├── scripts/           # one-off fetchers
└── tests/             # guard frozen kernel / semantics
```

Conventions:
- CLI entry: `PYTHONPATH=src python -m <pkg>.cli analyze`
- Shared venv: `. experiments/tfpt-discovery/.venv/bin/activate`
- Constants from axioms only — no hidden SI inputs
- Catalog in `experiments/README.md` (German overview OK here only)

## Scorecard workflow

When an experiment row changes:

```bash
# edit the experiment's result source, then:
python experiments/build_evidence_scorecard.py
```

Regenerates `experiments/evidence_scorecard.json` and the `<!-- SCORECARD_STATS -->` block in `experiments/README.md`.

**Do not** hand-edit scorecard stats in README. Website mirror: `website/lib/predictions.ts` references the scorecard — update if user-visible prediction surface changed.

Schema details: [reference.md](reference.md)

Empirical searches (FRB/GW/pulsar): skill **`tfpt-empirical-search`**.  
Scorecard edits: skill **`tfpt-evidence-scorecard`**.

## Theory contracts

Pure-math checks (e.g. QGEO mark-locality) live in `experiments/theory-contracts/`.
- Run standalone: `cd experiments/theory-contracts && python3 qgeo_dtn_mark_locality.py`
- **Out of scorecard** — internal consistency, not external evidence
- Narrative home if promoted: `tfpt_research_contracts.tex`, not verification ledger as empirical row

## What NOT to touch (experiment-only work)

Unless user explicitly requests promotion:

- `verification/run_all.py`, `verification/vN_*.py`, `status_ledger.csv`
- `\veri{}` citations, `script_registry.csv`, `changelog.tex`
- Generated: `verification.tex`, `ScriptIndex.tsx`, `docs_map.csv`, `website_map.csv`
- `bash build.sh audit` is **not** required for pure experiment README/results updates

**Do** update: experiment README, `results/`, scorecard row if applicable, `experiments/next.txt` for research notes (German allowed).

## Discovery sandbox

Throwaway probes before a vN module:

```
experiments/tfpt-discovery/   # symbolic search, raw scripts
```

Confirm numbers here first; promote via **`promote-to-verification`** when load-bearing.

## Completion checklist (experiment-only)

- [ ] README states firewall, data source, verdict enum, honest scope
- [ ] Frozen kernel guarded by tests (search projects)
- [ ] Scorecard row typed correctly (if empirical)
- [ ] `build_evidence_scorecard.py` run if scorecard changed
- [ ] No accidental edits to verification/ledger/papers
- [ ] `experiments/next.txt` entry if user-visible research note
