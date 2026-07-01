---
name: promote-to-verification
description: >-
  Promote a TFPT finding from exploration to load-bearing verification/vN_*.py with
  full paper, ledger, changelog, and website sync. Use when a numeric result should
  enter verification/, get a veri citation, close or narrow a gate, or graduate from
  experiments/ to the compiler output.
---

# Promote to verification

A finding **does not exist in TFPT** until it is a `verification/vN_*.py` module cited in a **paper body** with `\veri{vN_<name>.py}`.

## Gate: summary before any edit

After running the script (or confirming the identity), **stop and report**:

- Exact numbers / identities printed
- Pass/fail counts, scope, honest caveats
- What changed vs expectation

**No summary ⇒ no paper/ledger/changelog/website edits.**

## Decision: promote or stay in experiments?

| Stay in `experiments/` | Promote to `verification/vN_*.py` |
|------------------------|-----------------------------------|
| Search target, null, data_limited | Exact identity or audited numeric claim for a paper section |
| Empirical scorecard row only | Needs `\veri{}` in TeX body + ledger row |
| Firewall-limited (FRB/GW search) | Closes/narrows a gate or upgrades a status marker |
| Theory contract (pure math) | Becomes machine-checked suite claim (often still `[C]`) |

When unsure: keep experiment honest; promotion can wait.

## Workflow (follow in order)

### 1. Confirm computationally

```bash
. experiments/tfpt-discovery/.venv/bin/activate
cd verification
python vN_<name>.py          # after writing
python run_all.py            # must end ALL CHECKS PASSED
```

Prefer `sympy` exact where possible; import from `tfpt_constants`; use `check()/summary()/reset()`.

### 2. Write `verification/vN_<name>.py`

- Docstring: honest scope, status markers per check, dependencies
- Never fabricate a pass
- Derive from `{c3, g_car}` primitives

### 3. Register

- Add to `verification/run_all.py` → `MODULES`
- Add row to `verification/script_registry.csv` (cluster, `what_tex`, `what_web`)
- Add/update `verification/status_ledger.csv` (7 cols; quote commas)

### 4. Deep-sync before editing papers

Load skill **`tfpt-deep-sync`**: launch parallel subagents, merge checklists.

```bash
bash build.sh gen   # fresh docs_map.csv + website_map.csv first
```

### 5. Paper integration (mandatory)

- `\veri{vN_<name>.py}` in the **exact section/box** where the content lives — not index alone
- Correct `\mE/\mC/\mO/\mX` marker; ledger keeps fine type
- Status move → sync `introduction.tex` status card **and** `tfpt_4_frontier.tex`
- Multiple sections OK if the script feeds several narratives

### 6. Wolfram (exact results only)

Exact algebraic / identity / lattice / Pascal:

```bash
wolframscript -file verification/wolfram/tfpt_readouts.wl
```

Update `verification/wolfram/README.md` count + `GATE.WOLFRAM.01` ledger row.

Numerical-only (scipy ODE/PDE): Python-only — flag in `.wl` comment + README.

### 7. Changelog

Add dated entry to `changelog.tex` (newest first, plain LaTeX, **mention `vN_<name>.py`**).

### 8. Website (if user-visible)

- `bash build.sh gen` → regenerates `ScriptIndex.tsx`, `changelog.ts`, maps
- `bash build.sh website` → mirrors PDFs + scripts + hashes
- Update `website/lib/papers.ts` sections if narrative changed
- DAG node: add script to `VerificationDag.tsx` if it backs a node
- Status change: `StatusPyramid.tsx`, `orientation/StatusMatrix.tsx`, `predictions.ts`

### 9. Release pipeline

```bash
bash build.sh release    # gen → compile → website → audit → npm build
```

Must end **`AUDIT OK`**. Browser-check touched pages.

### 10. Manifests (last)

```bash
python verification/make_manifest.py
```

## Generated files — never hand-edit

`tex-artefacts/verification.tex` · `website/components/ScriptIndex.tsx` · `website/lib/changelog.ts` · `website/lib/version.ts` · `verification/docs_map.csv` · `verification/website_map.csv`

## Also update when user-visible

- Root `README.md` (highlights, open gates, reproduce commands)
- `experiments/next.txt` (research notes — German OK)
- `zenodo_description.html` if deposit scope/status/repro counts changed

## Full checklist

See [checklist.md](checklist.md)
