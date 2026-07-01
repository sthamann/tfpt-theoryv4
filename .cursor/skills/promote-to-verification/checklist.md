# Promotion checklist

Copy and track when promoting a finding to verification.

```
Module: vN_<name>.py
Verified result: <concrete numbers from script run>
Affected docs: <e.g. tfpt_2, tfpt_5_redteam>
```

## Script & suite

- [ ] `verification/vN_<name>.py` written with honest docstring
- [ ] Standalone run passes
- [ ] Added to `run_all.py` → `run_all.py` ends ALL CHECKS PASSED
- [ ] Row in `script_registry.csv`
- [ ] Row in `status_ledger.csv`

## Deep-sync (skill: tfpt-deep-sync)

- [ ] `bash build.sh gen` before enumeration
- [ ] Parallel subagents: paper surfaces · website mirrors · stale wording
- [ ] (+ status move) fourth subagent: intro, frontier, contracts, origin_theory
- [ ] Merged checklist applied in one coherent edit

## Papers

- [ ] `\veri{vN_<name>.py}` in paper **body** (correct section)
- [ ] Status marker matches ledger
- [ ] Status move → intro status card + tfpt_4_frontier agree
- [ ] Stale "stays open" / "one missing" prose rewritten

## Wolfram (if exact)

- [ ] Check added to `tfpt_readouts.wl`
- [ ] `wolframscript -file ...` passes
- [ ] README count + GATE.WOLFRAM.01 updated

## Changelog & generated

- [ ] Dated entry in `changelog.tex` mentions vN id
- [ ] `bash build.sh gen` after edits
- [ ] No hand-edits to generated files

## Website

- [ ] `bash build.sh website` if PDFs/scripts changed
- [ ] `papers.ts` / `predictions.ts` if narrative changed
- [ ] VerificationDag / StatusPyramid / StatusMatrix if applicable
- [ ] Browser-check touched pages

## Exit gate

- [ ] `bash build.sh audit` → AUDIT OK
- [ ] `npm run build` in website/ passes
- [ ] `python verification/make_manifest.py` (last)
- [ ] README.md + next.txt updated if user-visible
