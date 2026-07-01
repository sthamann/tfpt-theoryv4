# TFPT project skills

Project-local Cursor Agent Skills (`.cursor/skills/`). Loaded on demand when the task matches the skill description.

| Skill | Use when |
|-------|----------|
| [tfpt-experiment](tfpt-experiment/SKILL.md) | Work in `experiments/` — firewall, scorecard, standalone layout |
| [tfpt-empirical-search](tfpt-empirical-search/SKILL.md) | FRB/GW/pulsar/recovery preregistered searches |
| [tfpt-evidence-scorecard](tfpt-evidence-scorecard/SKILL.md) | Update `evidence_scorecard.json` rows and enums |
| [promote-to-verification](promote-to-verification/SKILL.md) | Graduate a finding to `verification/vN_*.py` + papers + ledger |
| [tfpt-deep-sync](tfpt-deep-sync/SKILL.md) | Parallel surface enumeration before/after vN integration |

## Rules (Cursor)

| Rule | Scope |
|------|-------|
| `tfpt-core.mdc` | **Always on** — invariants + skill routing |
| `tfpt-workflow.mdc` | Glob: verification, TeX, changelog, README |
| `sync-maps.mdc` | Glob: verification, TeX, website, README, next.txt |
| `subagent-deep-sync.mdc` | Glob: verification, TeX, website |
| `website-sync.mdc` | Glob: website, verification, TeX |
