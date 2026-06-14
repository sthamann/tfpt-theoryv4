# TFPT — Topological Fixed-Point Theory

> A closed **discrete compiler** for the dimensionless skeleton of the Standard Model and
> cosmology, built from **two inputs** plus typed physical anchors for the absolute scales.
> Every load-bearing claim is machine-checked by an independent verification suite.

TFPT models physics as a small deterministic *compiler*: two boundary inputs are fed in, an
`E8` "audit hull" is built as an intermediate object, and the Standard-Model + cosmology
read-outs fall out as **projections** — through a chain of exact identities and lattice/Lie
theorems, not fits. This repository contains the theory documents, a full Python + Wolfram +
Lean verification stack, and a versioned status ledger that types every claim.

---

## 1. The theory in one page

### The two inputs

| Input | Symbol | Value | Role |
|---|---|---|---|
| Seam normalisation (P1) | `c₃` | `1/(8π)` | boundary/horizon constant |
| Carrier rank (P2) | `g_car` | `5` | the `3+2` carrier interface |

These two collapse further: both are the elementary-symmetric data of the **parabolic anchor**
`a = (1,1,2)`, so the genuine input layer is `a` plus the single transcendental `π`
(`c₃ = 1/(2·e₁(a)·π) = 1/(8π)`). The carrier choice `g_car = 5` is itself an *over-determined
bootstrap fixed point* (forced three independent ways via the `E8` closure), so the theory has
**no free load-bearing number** on the dimensionless axis — only `π` is primitive.

### The compiler pipeline

```
  c₃ = 1/(8π)  ┐
               ├─►  anchor a=(1,1,2)  ──►  powers pₙ=2+2ⁿ ─► |R(E8)|=240, dim E8=248, rank 8
  g_car = 5    ┘                                            (E8 = audit/compiler hull, NOT a gauge group)
        │
        ├─►  carrier D5 ⊕ A3 + μ4  ──►  gauge group, hypercharge, N_fam = 3
        │
        ├─►  φ₀ = 1/(6π) + 48·c₃⁴  ──►  α⁻¹ = 137.0359992  (unique root of the boundary Ward identity)
        │
        ├─►  lattice operators (Q,K,R,L) on H₁(P¹∖μ4)=ℤ³,  det = (3,4,8,20),  ∏ = 1920 = |W(D5)|
        │         └─►  masses (φ₀-ladder), lepton c = (16/7, 4/3, 7/6), quark ratios (integer Plücker)
        │
        └─►  c₃ = Einstein/Jacobson 8π coefficient ─► R+R² scalaron M = c₃^(7/2)·M̄_Pl ≈ 3.06×10¹³ GeV,
                                                       Λ ~ e^(−2α⁻¹), Ω_b = (1−1/4π)φ₀ ≈ 0.04894
```

### What it produces (selected, all machine-checked)

- **`α⁻¹ = 137.0359992`** as the *unique* root of a boundary `U(1)` Ward identity (existence +
  uniqueness, interval-arithmetic verified).
- **Three fermion generations** `N_fam = 3 = rank A3 = dim H₁(P¹∖μ4)`.
- **Flavor**: an integer operator ladder with `det(Q,K,R,L) = (3,4,8,20)`, product
  `1920 = |W(D5)|`; charged-lepton coefficients `(16/7, 4/3, 7/6)` exactly; quark mass *ratios*
  as integer Plücker readouts (`c_u/c_d = 55/117`, …).
- **Solar angle** `sin²θ₁₂ = 1/3 − φ₀/2 = 0.306747` (frozen prediction of record, machine-enforced
  via `predictions_frozen.json`/`v84`; conditional on the seam-misalignment lemma).
- **Cosmology**: `Ω_b`, the Starobinsky scalaron mass, `Λ ~ e^(−2α⁻¹)`, cosmic birefringence
  `β = φ₀/(4π) ≈ 0.2424°`; the former external band `N_star ∈ [50,60]` is sharpened to a
  *conditional* point `N_star(k=0.05/Mpc) = 51.4` `[P]` via the scalaron-reheating chain (`v86`;
  `n_s = 0.9611`, `r = 0.0045`) — honestly recorded: the slow Higgs-channel point is
  `A_s`-disfavoured (−11.4σ; the measured `A_s` requires near-instantaneous reheating), so the
  frozen band stays the surface of record.
- **Self-consistency**: under the named gapped-transport hypotheses, "parameter-free" is a
  *theorem* — the gapped boundary transport (`Δ = 6·log(3/2) > 0`) has, by Perron–Frobenius, a
  **unique attractor** at rate `(2/3)⁶` (the physical identification of the transport operator
  stays `[P]`); the hull carries a literal order-`30 = 2·3·5` Coxeter cycle.
- **Master cover** (`v85`): all anchor-block pencil covers are *one* double cover up to GL(2)
  Möbius reparametrisation (`disc = N_fam⁴·det(G)²`); Koide and the carrier are its two branch
  points, the scalaron exponent its trace; `μ₄` is *not* a 4:1 cover of the line (honest negative).
- **Spine tetrahedron** (`v91`): the spine `{2,3,4,5} = {e₃(a), p₀(a), e₁(a), e₂(a)}` is *one*
  finite object — edges `{6,8,10,12,15,20}`, faces `{24,30,40,60}`, volume `120 = |R⁺(E8)|`;
  `240 = |μ₄|·|E(K₄)|·|E(K₅)|` (breaks at `K₆` — specific, not generic). Dual cuts are typed as
  tautological presentation; `7, 16, 41, 48, 240, 248` lie *outside* the sub-grammar (honest).
  The tetrahedron is the *presentation raster of the anchor microcode* — the engine stays
  `a = (1,1,2)` (plus `p₀(a) = 3`).
- **Centered flavor diamond** (`v95`): the four flavor operators are *one* center plus *two*
  axes — `Q = U+V`, `R/L = C∓U` (winding), `K/F = C∓V` (sheet, `Spec V = {0,1,2}` = the cusp
  class); the center has `det C = 14`, `ΣC = 31 = 2^g−1` (the IR gap-bound numerator),
  `Pl_R(C) = 7·(2,3,1)` — the `G₂` reading stays audit-typed.

### Honest scope — the four layers

TFPT does **not** claim a certified strict Theory of Everything. It is honestly typed in four
layers (this separation is the discipline of the whole package):

| Layer | Content | Status |
|---|---|---|
| **1. Closed compiler** | `E8` glue, carrier, `α⁻¹`, `(R,K,Q,L)`, lepton/quark *ratios* | `[I]/[L]/[N]` |
| **2. Protected IR physics** | `R+R²`, admissible gapped transfer sector (OS-reconstructed *under RP/gap hypotheses*) | `[I]/[P]` |
| **3. Anchors** | `π`, one dimensionful induced-gravity scale, `U_point` absolute amplitude norm | `[A]` (declared, not "missing") |
| **4. Interfaces** | `m_p/m_e`, `η_B` (leptogenesis), Koide, axion relic, full ambient QG measure | `[P]/[A]` |

The single remaining **central theorem target** is to derive the
`1/(8π)` area-law coefficient from the replica variation of the seam determinant. Its *structure*
is closed (Fursaev–Solodukhin ⟹ `c₃ = 1/(8π)` is the unique value giving `S = A/4`), its
*mechanism* is now exhibited at the gapped-model level (replica variation of a gapped 2d
determinant **is** of EH form with a cutoff-independent coefficient; target equation
`ln m = 3/4 = q(A₃)`, `v150`), and the residual is identified as the one irreducible dimensionful
anchor (`1/G` is UV-sensitive, Sakharov-type induced gravity) — not a diffuse gap.

---

## 2. Repository structure

### Theory documents (9 active LaTeX "notes", compiled from repo root)

| File | Contents |
|---|---|
| `introduction.tex` | Entry point & reading guide; the two axioms, the two-engine picture, the status heatmap. |
| `tfpt_1_architecture_e8.tex` | **Core.** Axioms `{c₃, g_car}`, derivation map, EM fixed point, the `D5⊕A3+μ4 ⇒ E8` construction. |
| `tfpt_2_standard_model.tex` | **Standard Model.** The `φ₀`-ladder mass formula, flavor block from parabolic transport, neutrinos, CKM/PMNS, the worked closures. |
| `tfpt_3_e8_audit_bootstrap.tex` | **`E8` audit & bootstrap.** The seven `E8` slices, the cascade bridge, and the Möbius self-consistency loop. |
| `tfpt_4_frontier.tex` | **Frontier.** Honest status of `η_B`, `m_p/m_e`, Koide, dark matter, quantum gravity — what is *not* forced. |
| `tfpt_5_redteam.tex` | **Red Team.** Adversarial stress test of the five load-bearing reductions (Targets A–E): where each would fail and which assumptions are truly necessary. |
| `tfpt_horizon_readouts.tex` | **Appendix H.** `c₃ = 1/(8π)` as the universal horizon thermal code (reframe, not new physics). |
| `tfpt_research_contracts.tex` | The open gates as numbered lemma-chain *contracts* (`U_wall`, `G_metric`). |
| `origin_theory.tex` | Synthesis: the seam-as-horizon formulation, the attractor, and one honestly-typed `[P]` cyclic interpretation. |

### Verification (`verification/`)

| Item | What it is |
|---|---|
| `v1_*.py … v198_*.py` | 197 numbered claim checks (one file per claim cluster; highest ID `v198`, `v186` skipped as redundant). |
| `run_all.py` | Runs the whole suite; ends `ALL CHECKS PASSED`. |
| `tfpt_constants.py` | Shared constants + `check()` harness. |
| `predictions_frozen.json` | **Blind-prediction registry** (frozen 2026-06-09): every dimensionless prediction of record at 25 digits, locked to its formula by `v84_frozen_registry.py` on every run; exactly one `θ12` prediction of record (seed `0.306747`), `r`/`n_s` only as `N_star` bands. |
| `status_ledger.csv` | **Single source of truth.** Every claim with id, status, location, dependency, script — *versioned* (`active`, `canonical_status`, `supersedes`). |
| `script_registry.csv` + `script_clusters.csv` | **Single source for the script index** — generates both the master TeX index table and the website `ScriptIndex` via `make_script_index.py`. |
| `make_docs_map.py` | Generates `docs_map.csv` (paper → section → scripts cited → last changed) and `website_map.csv` (website file → scripts/docs mentioned) — the machine-readable sync surfaces. |
| `audit_sync.py` | **The sync audit** (papers ↔ suite ↔ ledger ↔ changelog ↔ website, both directions); must end `AUDIT OK`. |
| `make_figures.py` | Regenerates the figures (status heatmap, attractor, Coxeter circle, …). |
| `make_manifest.py` | Writes `manifest.sha256` + `lean_manifest.sha256` (content digests). |
| `wolfram/tfpt_readouts.wl` | Independent second path on Wolfram Engine (`116/116` checks); `wolfram/tfpt_readouts_extension.wl` mirrors the exact algebraic/identity/lattice results v84–v198 (`240/240`, verified on Wolfram Engine 14.3). |
| `redteam/run_redteam.py` | **Adversarial layer.** Tries to *break* the five reductions (Targets A–E); verdicts in `REDTEAM.*` ledger rows + `tfpt_5_redteam.tex`. |

### Other directories

- `experiments/lean4-carrier-rigidity/` — Lean 4 proof of the carrier algebra (P2: hypercharge,
  anomaly-freedom, integer rigidity), machine-formalised `[F]`.
- `experiments/` — research-level explorations (e.g. `eht-achromatic-residual`, discovery scripts).
- `figures/` — generated PDFs used by the documents.
- `website/` — the public Next.js mirror (papers, interactive verification DAG, in-browser
  script reproducer); kept byte-identical to the repo by `bash build.sh website` + the audit.
- `manifest.sha256`, `lean_manifest.sha256` — reproducibility digests.
- `build.sh` — the build + sync pipeline: `notes` (compile), `gen` (regenerate the
  single-source surfaces), `website` (mirror sync + version stamp), `audit` (sync audit),
  `release` (all of the above + `npm run build`).

---

## 3. Reproduce / verify

Dependencies: a LaTeX distribution (`pdflatex`), Python 3 with `sympy`, `mpmath`, `numpy`,
`matplotlib`; optionally Wolfram Engine and Lean 4 (`elan`/`lake`).

```bash
# 1. Compile the 9 active documents + the changelog  ->  "10 ok, 0 failed"
bash build.sh notes

# 2. Run the Python verification suite  ->  "ALL CHECKS PASSED"
cd verification && python run_all.py

# 3. Independent Wolfram path  ->  "116/116 passed"  (optional, needs Wolfram Engine)
#    (the v84+ extension mirrors the exact results, 240/240)
wolframscript -file verification/wolfram/tfpt_readouts.wl
wolframscript -file verification/wolfram/tfpt_readouts_extension.wl

# 4. Lean carrier-rigidity proof  ->  "AUDIT: PASS"  (optional)
cd experiments/lean4-carrier-rigidity && lake exe cache get && bash scripts/audit.sh

# 5. Red Team / Stress Test layer (adversarial; prints a status per target A-E)
cd verification/redteam && python run_redteam.py

# 6. The sync audit: papers <-> suite <-> ledger <-> changelog <-> website  ->  "AUDIT OK"
bash build.sh audit

# 7. Regenerate reproducibility manifests (ALWAYS the last step before export)
python verification/make_manifest.py

# 8. Verify the shipped manifests against the tree (must pass on any export;
#    guards against the stale-row class of error found in the v83 review)
python verification/make_manifest.py --check
```

Every script cited in `run_all.py` is also cited inline in the documents via `\veri{vN_*.py}`
(enforced in both directions by `verification/audit_sync.py`), and the status heatmap is
generated directly from `status_ledger.csv`, so the papers, the suite, the ledger and the
website stay in lock-step. `bash build.sh release` runs the whole pipeline in one command.

---

## 4. Status markers

Used consistently across all documents and the ledger:

The **documents** show a simplified four-class display marker; the **ledger** keeps the fine-grained
per-claim type (Axiom / Formal / Lattice / Numerical / Identity / Physical), so no fidelity is lost.

| Display marker | Meaning | Ledger fine types it covers |
|---|---|---|
| `[E]` | exact / machine-proven | Identity, Lattice (Lie/lattice), Formal (Lean), Numerical |
| `[C]` | conditional (holds under named hypotheses) | Physical, bridge, readout |
| `[O]` | open / axiom (declared input or genuine gap) | Axiom |
| `[X]` | falsifiable kill test | — |

The ledger is *append-only and versioned*: superseded rows are marked `active=false` with a
`canonical_status` pointer, so the current authoritative status of any claim is unambiguous.

---

## 5. What is genuinely open

- **The central theorem**: `1/(8π)` from the seam-determinant replica — structure closed, the
  Fursaev–Solodukhin factor machine-derived (`v90`), and the mechanism now exhibited at the
  gapped-model level (gap ⇒ cutoff-independent EH coefficient under replica, `v150`), with the
  Calderón transfer answered (the DtN kernel is conically clean; the seam-reduced action inherits
  the EH form via the BFK split, `v151`); the `q(A₃)`
  normalisation is itself the one dimensionful anchor in disguise (the EH coefficient is a log-ratio
  `k = ln(m/μ)/12π`, and `m/μ` is `1/G`, `v152`), so the isolated residual is just the
  kernel-identification premise plus that single declared anchor.
- **Full covariant metric-sector / ambient QG measure** (`G_metric`) — kept open by design;
  gap-decoupled from the admissible IR sector (`Δ_eff = 1.648 > 0`). After `v83`/`v87` the whole
  Target-A gate is **one** theorem: *the seam–Calderón boundary net is holomorphic with `c = 8`*
  — then `(E8)₁` and the unique 2D bulk both follow. Equivalent index form (`v89`): *the seam net
  contains the carrier net with Jones index `4 = |μ₄|` as its `μ₄` simple-current extension* —
  holomorphy then follows from μ-additivity instead of being assumed. And *which* extension carries
  no freedom (`v92`): the carrier extension tower is completely rigid — carrier `(μ=16)` →
  `SO(16)₁` `(μ=4`, the unique intermediate`)` → `(E8)₁` `(μ=1`, two chiralities = sheet`)` —
  so Gate A is the *bare* index statement. The two structural residuals are now **discharged to a
  theorem** (`v175`): the CAR second-quantisation functor `Γ(t)=⊕ₘΛᵐ(t)` makes full-cone reflection
  positivity reduce *for every `m`* to the one-particle contraction (verified on the complete
  `2¹⁶=65536`-dim Fock space), and net existence is an assembled, verified `(E8)₁` certificate
  (character `1+248q+4124q²+…`, embedding `248=120+128`, `E8` Cartan even unimodular) — so net
  existence and full-cone RP are `[E]`, and the single open structural premise is the seam-collar
  realisation (its finite half — cross-ratio 2, faithful Möbius `D4`, `b₁=N_fam=3`,
  characters = `A3` exponents — is proven exactly, `v168`). That residual is then driven to **bedrock**
  (`v176`–`v181`): assembled as one central theorem (`v176`), split into the marks + kernel
  obligations whose finite cores close (`v177`/`v178`), unified into one conformal-realisation premise
  (`v179`), and reduced — via uniformisation, Kerékjártó and the order-4 Möbius classification — to a
  seam-*isometry* premise (`v180`) and finally to the strictly weaker conformal-*symmetry* / deck
  premise `QGEO.SYM.01` (`v181`): *the carrier `μ₄` clock is the conformal deck of the seam*. Below
  that the residual is **definitional** (the seam's conformal structure *is* the `μ₄`-deck structure of
  the carrier), not a missing theorem — the single irreducible structural residual of the whole theory.
  It is then driven to its sharpest, **non-circular** form (`v194`–`v198`): the raw seam DtN is
  RP-canonical (Osterwalder–Schrader on the quasi-free state, `v194`), the marks are *forced* by a
  Lefschetz/character argument rather than posited (`v195`), and the bedrock is cracked to a clean
  **state-invariance** — the DtN principal symbol `|k|=diag(|n|)` commutes *exactly* with the clock
  `diag(iⁿ)` on all of `L²`, and by Tomita–Takesaki `[ρ,Λ_Σ]=0` *follows from* `ω∘ρ=ω` with no conformal
  covariance (removing the Bisognano–Wichmann circularity, `v198`). So the entire residual is now the
  single, checkable, non-circular statement *“the raw quasi-free seam state is `μ₄`-invariant”* — a
  foundational symmetry postulate in its sharpest falsifiable form (the role `c=const` plays in relativity),
  not a missing theorem.
- **Absolute amplitude normalisation** (`U_point`) — an anchor; the quark *ratios* are closed.
- **Frontier interfaces** (`m_p/m_e`, `η_B`, Koide, axion relic) — deliberately typed as
  interfaces, never quoted as compiler outputs.

The remaining distance is therefore not a list but **one definitional geometric premise**
(`QGEO.SYM.01`, `v181`: *the carrier `μ₄` clock is the conformal deck of the seam* — net existence and
full-cone RP are `[E]`, `v175`, and the conformal/isometry layers reduce to it via uniformisation +
Kerékjártó) plus **one declared metrology unit**. The central theorem reads as a clean simple-current
extension, `(D₅)₁⊗(A₃)₁ ⋊ ⟨(1,1)⟩ ≅ (E₈)₁` (index 4, c = 8, μ = 1 ⇒ holomorphic ⇒ E₈, `v154`), and
`v_geo` is an *irreducible metrology primitive* by the No-Unit Theorem (`v153`): a dimensionless
boundary compiler provably cannot produce an absolute scale, so `U_point ~ v_geo`, `1/G ~ v_geo²` and
`m/μ = e^{3/4}` are one unit in three readings — the only irreducibles are `v_geo` and `π`. Likewise the
two axioms `{c₃, g_car}` are not free knobs: they reduce to the single parabolic anchor `a = (1,1,2)`
plus `π` (`v23`), with `g_car = 5` an over-determined bootstrap fixed point (forced three ways `v6`,
Pascal-unique and Lean-formalised). The bedrock premise is not closeable by a finite computation; it is
the one item that needs a human constructive-geometry argument (or a proof assistant). A development
timeline of all `181` scripts is in `introduction.tex` (and on the website verification page).

---

*Claim discipline: nothing in this repository is marked closed that is not machine-verified, and
no dimensionful quantity is claimed as a derivation from pure numbers. See `status_ledger.csv`
for the authoritative, per-claim status.*
