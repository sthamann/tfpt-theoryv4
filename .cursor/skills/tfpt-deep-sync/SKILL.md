---
name: tfpt-deep-sync
description: >-
  Enumerate and sync every TFPT surface when integrating a new verification/vN module,
  status marker change, or superseded open-gate prose. Launches parallel subagents using
  docs_map.csv and website_map.csv. Use with promote-to-verification or any vN, ledger,
  veri citation, or status move that touches papers and website.
---

# TFPT deep-sync

Integrating a finding touches dozens of surfaces. **Do not rely on memory or a single grep.**

Parent agent: run script → summarise result → **`bash build.sh gen`** → launch subagents → merge → edit → audit.

## When mandatory

Launch parallel subagents when **any** of:

- New or renamed `verification/vN_*.py`
- Status marker upgrade/downgrade
- Result closes/narrows/supersedes open/residual prose
- New or moved `\veri{}` citation
- Prediction or falsification surface changed on website

**Skip** only for zero theory impact (CI, tooling, typo) with no `\veri{}`, ledger, status, or mirror touch.

## Order of operations

1. **Run script** — summarise concrete output first (numbers, pass/fail, scope)
2. **`bash build.sh gen`** — refresh `docs_map.csv`, `website_map.csv`
3. **Launch subagents in one message** (parallel)
4. **Merge checklists** — apply all edits coherently
5. **`bash build.sh gen`** again → compile/sync
6. **Exit:** `bash build.sh audit` → `AUDIT OK`
7. Optional: post-edit readonly subagent for missed stale wording

## Parallel launch pattern

| # | Role | subagent_type | readonly | Task |
|---|------|---------------|----------|------|
| 1 | Paper surfaces | `explore` | `true` | `grep vN_* verification/docs_map.csv`; list every `\veri{}`, status marker, keybox, related prose; flag sections with narrative but no citation |
| 2 | Website mirrors | `explore` | `true` | `grep vN_* verification/website_map.csv`; enumerate `papers.ts`, `VerificationDag.tsx`, `StatusPyramid.tsx`, `StatusMatrix.tsx`, `predictions.ts`, `README.md`, `next.txt` |
| 3 | Stale wording | `explore` | `true` | Grep `*.tex`, `website/`, `README.md`, `next.txt` for superseded phrases: "remaining input", "stays open", "one missing", old gate ids |

**Status moves** affecting intro/frontier/contracts/origin: add fourth `explore` subagent scoped to `introduction.tex`, `tfpt_4_frontier.tex`, `tfpt_research_contracts.tex`, `origin_theory.tex` + website mirrors.

After failed audit: launch **`shell`** subagent to run audit, parse failures, iterate until green.

## Subagent prompt template

Copy from [subagent-prompts.md](subagent-prompts.md); fill in module id and verified result summary.

## Content maps (primary index)

| Map | Path | Use |
|-----|------|-----|
| Paper sections | `verification/docs_map.csv` | doc, section, line range, scripts cited |
| Mirror surfaces | `verification/website_map.csv` | website files + README + next.txt |

Both **generated** — never hand-edit. Re-run `bash build.sh gen` after paper/website edits.

## Prose mirrors (check even without grep hit)

- Root `README.md` — highlights, open gates, reproduce commands
- `experiments/next.txt` — running research notes (German allowed)

## Subagents must NOT

- Fabricate script results or upgrade markers without ledger backing
- Hand-edit generated files (`verification.tex`, `ScriptIndex.tsx`, `changelog.ts`, maps, `version.ts`)
- Mark complete without `bash build.sh audit` → AUDIT OK
- Skip README, next.txt, changelog when user-visible

## Parent completion criteria

- [ ] Every merged checklist row addressed or N/A
- [ ] Script in run_all, registry, ledger, changelog (if new vN)
- [ ] `\veri{}` in paper body; Wolfram if exact
- [ ] Status markers agree: intro, frontier, website status components
- [ ] `bash build.sh audit` → AUDIT OK; `npm run build` passes
- [ ] Browser-check touched website pages
