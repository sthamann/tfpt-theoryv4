# Reproduce / verify

> Three levels of depth, from a 30-second headline check to a full release rebuild.

## The one command

```bash
./verify            # ~1s   : re-derive the headline claims from the two axioms
./verify --full     # ~4min : the entire Python suite (verification/run_all.py)
./verify --release  #        : full pipeline — docs + suite + website + sync audit
```

No local toolchain? Run the published image:

```bash
docker run --rm ghcr.io/sthamann/tfpt:latest          # 30-second headline check
docker run --rm ghcr.io/sthamann/tfpt:latest --full   # the whole Python suite
```

…or build it yourself: `docker build -t tfpt . && docker run --rm tfpt`. There is also a
[`.devcontainer`](../.devcontainer/devcontainer.json) for one-click GitHub Codespaces / VS Code.

## The independent engines

TFPT is checked by **three independent engines**. `./verify` exposes each:

```bash
./verify --wolfram   # second path on the Wolfram Engine (116/116 base, 368/368 extension)
./verify --lean      # the Lean 4 carrier-rigidity proofs (no sorry/admit)
./verify --audit     # papers <-> suite <-> ledger <-> changelog <-> website  (AUDIT OK)
```

## Full manual reproduction

Dependencies: Python 3 with `mpmath`, `numpy`, `sympy`, `scipy`, `matplotlib` (see
[`requirements.txt`](../requirements.txt)); optionally a LaTeX distribution (`pdflatex`), the
Wolfram Engine, and Lean 4 (`elan`/`lake`).

```bash
pip install -r requirements.txt

# 1. Compile the 9 active documents + the changelog  ->  "10 ok, 0 failed"
bash build.sh notes

# 2. Run the Python verification suite  ->  "ALL CHECKS PASSED"
cd verification && python run_all.py

# 3. Independent Wolfram path  ->  "116/116 passed"  (needs Wolfram Engine)
#    (the v84+ extension mirrors the exact results, 368/368)
wolframscript -file verification/wolfram/tfpt_readouts.wl
wolframscript -file verification/wolfram/tfpt_readouts_extension.wl

# 4. Lean carrier-rigidity proof  ->  "AUDIT: PASS"
cd experiments/lean4-carrier-rigidity && lake exe cache get && bash scripts/audit.sh

# 5. Red Team / Stress Test layer (adversarial; prints a status per target A-E)
cd verification/redteam && python run_redteam.py

# 6. The sync audit: papers <-> suite <-> ledger <-> changelog <-> website  ->  "AUDIT OK"
bash build.sh audit

# 7. Regenerate reproducibility manifests (ALWAYS the last step before export)
python verification/make_manifest.py

# 8. Verify the shipped manifests against the tree (must pass on any export)
python verification/make_manifest.py --check
```

`bash build.sh release` runs the whole pipeline (documents → suite → website mirror → audit → the
production website build) in one command.

## What lives in `verification/`

| Item | What it is |
|---|---|
| `v1_*.py … v472_*.py` | 472 numbered claim checks (one file per claim cluster). |
| `run_all.py` | Runs the whole suite; ends `ALL CHECKS PASSED`. |
| `verify_quick.py` | The fast headline check behind `./verify` (re-derives the core claims). |
| `tfpt_constants.py` | Shared constants + the `check()` harness. |
| `predictions_frozen.json` | **Blind-prediction registry** (frozen 2026-06-09), locked to formulas by `v84` on every run. |
| `status_ledger.csv` | **Single source of truth.** Every claim with id, status, location, dependency, script — versioned. |
| `script_registry.csv` + `script_clusters.csv` | Single source for the script index (TeX table + website `ScriptIndex`). |
| `make_docs_map.py` | Generates `docs_map.csv` + `website_map.csv` — the machine-readable sync surfaces. |
| `audit_sync.py` | **The sync audit** (papers ↔ suite ↔ ledger ↔ changelog ↔ website); must end `AUDIT OK`. |
| `make_figures.py` | Regenerates the figures (status heatmap, attractor, Coxeter circle, …). |
| `make_manifest.py` | Writes `manifest.sha256` + `lean_manifest.sha256` (content digests). |
| `wolfram/tfpt_readouts.wl` | Independent second path on the Wolfram Engine (`116/116`); the extension mirrors the exact results (`368/368`). |
| `redteam/run_redteam.py` | **Adversarial layer.** Tries to *break* the five reductions (Targets A–E). |

## Other directories

- `experiments/lean4-carrier-rigidity/` — Lean 4 proofs, machine-formalised `[F]` (no
  `sorry`/`admit`; every headline theorem's `#print axioms` returns only the three standard kernel
  axioms): the carrier algebra (P2: hypercharge, anomaly-freedom, integer rigidity, Pascal/glue
  uniqueness), the anchor ladder, the geometric/conditional cores of the open interfaces, and the
  seam equivalence chain (`FORM.SEAMEQUIV.01`).
- `experiments/` — research-level explorations (not claims until promoted; see the experiment
  README and `evidence_scorecard.json`).
- `figures/` — generated PDFs used by the documents.
- `website/` — the public Next.js mirror (papers, interactive verification DAG, in-browser Pyodide
  script reproducer); kept byte-identical to the repo by `bash build.sh website` + the audit.
- `manifest.sha256`, `lean_manifest.sha256` — reproducibility digests.
- `build.sh` — the build + sync pipeline: `notes` (compile), `gen` (regenerate the single-source
  surfaces), `website` (mirror sync + version stamp), `audit` (sync audit), `release` (all of the
  above + `npm run build`).

Everything you run in-browser (no install) is also on the
[website verification page](https://www.fixpoint-theory.com/verification), which fetches the same
scripts and runs them via Pyodide.
