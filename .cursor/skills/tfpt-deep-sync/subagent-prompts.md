# Deep-sync subagent prompts

Replace placeholders before launching.

## 1 — Paper surfaces

```
TFPT deep-sync subagent. Readonly.

Module: vN_<name>.py
Verified result: <concrete summary from script run — exact numbers, not expectations>
Affected docs (if known): <e.g. tfpt_2, origin_theory>

1. Assume maps may be stale — note if parent should re-run `bash build.sh gen`.
2. Use verification/docs_map.csv as primary index: grep the module id.
3. Open each (doc, section, line range) from the map.
4. Return markdown checklist: file | location | required change | priority.
5. List every \veri{}, status marker, keybox that must cite or reflect the result.
6. Flag sections with related narrative but no citation yet.
7. Flag ambiguous placements (which paper section owns the narrative).
8. Do NOT edit files.
```

## 2 — Website mirrors

```
TFPT deep-sync subagent. Readonly.

Module: vN_<name>.py
Verified result: <concrete summary>
Affected doc slugs: <e.g. tfpt-5-redteam>

1. grep vN_* in verification/website_map.csv
2. grep affected doc names in website_map.csv
3. Enumerate exact edits needed in:
   - website/lib/papers.ts (sections, highlights, keyFormulas)
   - website/components/VerificationDag.tsx
   - website/components/StatusPyramid.tsx
   - website/components/orientation/StatusMatrix.tsx
   - website/lib/predictions.ts
   - README.md, experiments/next.txt
4. Return checklist: file | location | required change | priority.
5. Do NOT edit files or generated ScriptIndex.tsx / changelog.ts.
```

## 3 — Stale wording hunt

```
TFPT deep-sync subagent. Readonly.

Module: vN_<name>.py
Verified result: <what changed — e.g. closes gate X, narrows residual Y>

Grep active *.tex, website/, README.md, experiments/next.txt for superseded
open-gate / residual phrases tied to this finding:
- "remaining input", "stays open", "one missing", "genuine remaining"
- old GATE.* ids superseded by this result
- framing that contradicts the new verified numbers

Return every hit with: file | line | current text | suggested rewrite | priority.
Do NOT edit files.
```

## 4 — Status-move scope (optional fourth subagent)

```
TFPT deep-sync subagent. Readonly. Status-marker move.

Module: vN_<name>.py
Verified result: <status change summary>

Scope ONLY:
- introduction.tex (status card, Rest = keybox, sharper aliases)
- tfpt_4_frontier.tex (frontier/QG status source)
- tfpt_research_contracts.tex (residual gates if moved)
- origin_theory.tex (gap list if moved)
- website mirrors: papers.ts entries, StatusPyramid, StatusMatrix, VerificationDag

Return checklist ensuring [E]/[C]/[O]/[X] markers agree everywhere.
Do NOT edit files.
```

## Audit-fix shell subagent

```
TFPT audit-fix subagent.

Run from repo root:
  bash build.sh audit

Parse every failure. Return:
- failure message
- root cause
- exact file + fix needed

Re-run audit after parent applies fixes. Repeat until AUDIT OK.
```
