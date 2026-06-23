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
- **Icosahedral bedrock** (`v219`): *why* the atoms are `{2,3,5}` — `E₈` is the exceptional top of
  the McKay tower of finite `SU(2)` subgroups (`2I`, order `120 = |R⁺(E₈)|`, has irrep degrees equal
  to the affine-`E₈` Kac marks, `Σ = 30 = h(E₈)`), so choosing `E₈` is choosing the icosahedron. A
  backward certificate, not a P2 proof; the same geometry reads `41` (EM index) as a Gaussian norm and
  `7` (scalaron) as an Eisenstein norm of the one carrier split (`v222`).
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
- **The boundary QFT as one relative object** (`v238`–`v261`, *Modular Spectral Closure*): the
  emergent-QFT round assembles the seam into `TFPT_QFT = (A_Σ, ω_Σ, Δ_Σ, ρ, A_F, H_F, D_F, J, γ, S_rel)`
  and collapses it to a single object. The 96-dim finite spectral triple (`A_F = ℍ_L⊕ℍ_R⊕M₄(ℂ)`, KO-6,
  order-zero, the first-order condition violated *exactly* by the Majorana = the CCvS σ mechanism, `v252`)
  is closed by three moves: the finite Dirac is the **modular/covariance induction** of the seam KMS state
  (`[D_F] = [D_Σ]⊗[K_car]`, the Yukawas a readout of `C_Σ`, `v258`); the spectral-action **cutoff is that
  KMS weight** so `f₂/f₀ = 1` exactly and `κ` becomes a finite-triple trace ratio (`v259`); and the seam
  (pillowcase), the carrier-16 (Kummer nodes) and `E₈` (`H²(K3) = U³⊕E₈(−1)²`) are facets of **one
  Kummer/K3 surface** (`v260`). The assembly certificate (`v261`) pins the cross-consistency — one number
  `4 = [B:A] = |μ₄| = 2χ = |(ℤ/2)²|`, one carrier-16, one gap `6log(3/2)` — so the layer is *QFT-complete
  modulo a single named theorem*, the **Seam Equivalence Theorem** `SEAM.EQUIV.01` (*the raw RP seam IS the
  holomorphic `(E8)₁` net at `τ=i`*; `v286`–`v288`). After the closing arc (`v300`–`v302`) that theorem's
  residual carries **no undischarged TFPT-internal assumption** — it is a composition of standard cited theorems
  (Steklov rigidity, the free-fermion classification, the AQFT stack) over established facts (the carrier-16, the
  derived gap `6log(3/2)>0`) — though it stays `[O]` (not machine-proved end-to-end). Ambient QG kept separate.

### Honest scope — the four layers

TFPT does **not** claim a certified strict Theory of Everything. It is honestly typed in four
layers (this separation is the discipline of the whole package):

| Layer | Content | Status |
|---|---|---|
| **1. Closed compiler** | `E8` glue, carrier, `α⁻¹`, `(R,K,Q,L)`, lepton/quark *ratios* | `[I]/[L]/[N]` |
| **2. Protected IR physics** | `R+R²`, admissible gapped transfer sector (OS-reconstructed *under RP/gap hypotheses*); the boundary QFT as one relative object (Modular Spectral Closure: Dirac = covariance induction, cutoff = KMS weight, seam/carrier/E₈ on one K3) | `[I]/[P]` |
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
| `v1_*.py … v324_*.py` | 322 numbered claim checks (one file per claim cluster; highest ID `v324`). |
| `run_all.py` | Runs the whole suite; ends `ALL CHECKS PASSED`. |
| `tfpt_constants.py` | Shared constants + `check()` harness. |
| `predictions_frozen.json` | **Blind-prediction registry** (frozen 2026-06-09): every dimensionless prediction of record at 25 digits, locked to its formula by `v84_frozen_registry.py` on every run; exactly one `θ12` prediction of record (seed `0.306747`), `r`/`n_s` only as `N_star` bands. |
| `status_ledger.csv` | **Single source of truth.** Every claim with id, status, location, dependency, script — *versioned* (`active`, `canonical_status`, `supersedes`). |
| `script_registry.csv` + `script_clusters.csv` | **Single source for the script index** — generates both the master TeX index table and the website `ScriptIndex` via `make_script_index.py`. |
| `make_docs_map.py` | Generates `docs_map.csv` (paper → section → scripts cited → last changed) and `website_map.csv` (website file → scripts/docs mentioned) — the machine-readable sync surfaces. |
| `audit_sync.py` | **The sync audit** (papers ↔ suite ↔ ledger ↔ changelog ↔ website, both directions); must end `AUDIT OK`. |
| `make_figures.py` | Regenerates the figures (status heatmap, attractor, Coxeter circle, …). |
| `make_manifest.py` | Writes `manifest.sha256` + `lean_manifest.sha256` (content digests). |
| `wolfram/tfpt_readouts.wl` | Independent second path on Wolfram Engine (`116/116` checks); `wolfram/tfpt_readouts_extension.wl` mirrors the exact algebraic/identity/lattice results (`285/285`, verified on Wolfram Engine 14.3). |
| `redteam/run_redteam.py` | **Adversarial layer.** Tries to *break* the five reductions (Targets A–E); verdicts in `REDTEAM.*` ledger rows + `tfpt_5_redteam.tex`. |

### Other directories

- `experiments/lean4-carrier-rigidity/` — Lean 4 proofs, machine-formalised `[F]` (`AUDIT: PASS`,
  no `sorry`/`admit`, only the three standard kernel axioms): the carrier algebra (P2: hypercharge,
  anomaly-freedom, integer rigidity, Pascal/glue uniqueness) **and** the geometric/conditional cores of
  the open `QGEO.SYM.01` premise — the Möbius uniformisation normal form `z↦iz` / `σρσ=ρ⁻¹` / orbit→`μ₄`
  (`FORM.QGEO.02`, mirrors `v177`) and the conditional theorem *mark-local DtN ⇒ `ω∘ρ=ω`*
  (`FORM.QGEO.01`, mirrors `v201`/`v210`). The *implication* is `[F]`; the seam-realisation *premise*
  (`QGEO.SYM.01`) stays `[O]`, a typed target — not closed.
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
#    (the v84+ extension mirrors the exact results, 285/285)
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

- **One condition, not many** (`v234`/`v235`): the whole *structural* residual — the metric inclusion
  `G_net`, the carrier `P2` and red-team Target A — is a single condition, *"the seam carries no
  nontrivial abelian sector"*, with three provably-equivalent faces that all force `E8`: holomorphy
  (`μ`-index 1), a homology-sphere seam link (`Γ` perfect `⟺ 2I`, `v232`), and exactly one 1-dim irrep
  (`v219`) — all equal `#(mark-1) = |H₁| = 1`, true only for `E8`. In abelian Chern–Simons language it is
  the single integer step `holomorphic ⟺ det K = 1`; the extension tower `D₅⊕A₃ (16) → D₈ (4) → E₈ (1)`
  is anyon condensation, i.e. the Kitaev `E8` quantum-Hall state. So the one open analytic step is
  *"the free RP seam condenses the order-`|μ₄|` Lagrangian glue (det → 1)"* = `QGEO.SYM.01`. Plus the two
  irreducibles: the scale `v_geo` (No-Unit theorem) and the transfer functor `F_transfer` (external physics).
  The discrete→dynamic lens (`v303`) shows `F_transfer` is the *readout end of the one principle*, not a
  bolt-on: all four interfaces are gapped relaxations to a unique attractor (Perron–Frobenius / H-theorem / RG
  fixed point), with only `F_pole` (Koide) at the seam rate `(2/3)⁶` and the other three (η_B washout, axion
  freeze, QCD RG) sharing the shape with external rates — honestly fenced by `v187`.
  **The whole emergent-QFT layer collapses onto the *same* premise** (`v261`, Modular Spectral Closure):
  the finite Dirac (covariance induction, `v258`), the spectral-action cutoff (the seam KMS weight, `v259`),
  the gauging (inner fluctuations), the glue and orientability are all readouts of the one seam state, so
  the boundary QFT is closed *as a relative object* modulo the single keystone `SEAM.EQUIV.01` — it adds
  **no new open item** (`QGEO.SYM.01` is its corollary, `v335`).
  The ambient quantum-gravity measure (`QG.AMB.01`) is **not** a second TFPT structural item: it is the
  *general* Euclidean-QG conformal-factor problem (GHP 1978), gap-decoupled (`Δ_eff = 1.648 > 0`) — an
  inherited, decoupled problem, no readout depends on it.
- **Gravity is parameter-free** (`v358`): the classical metric-sector field equation is no longer only an
  `R+R²` readout. The entanglement first law `δS = δ⟨K⟩` (Jacobson; Faulkner et al.), run with TFPT's atoms,
  gives the *linearised* Einstein equation `G_ab = c₃⁻¹ T_ab` with `c₃⁻¹ = 8π` **fixed** — no free
  dimensionless Newton dial — and the **thermodynamic** origin of `c₃` (the first-law coefficient `2π/η`)
  **coincides** with the **geometric** one (the one-sided Gauss–Bonnet `|Z₂|·2π·χ`) via the atom identity
  `|μ₄| = |Z₂|·χ(S²) = 4`. So `c₃` is **triply over-determined** (anchor, geometry, thermodynamics). The
  matter flux is assembled (the CHM ball modular Hamiltonian, `v323`) and the entropy density is atom-fixed
  (`1/4 = 1/|μ₄|`, central charge `c = g_car+N_fam = 8`). The only residual is the linear→nonlinear extension
  and the one unit `v_geo`.
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
  covariance (removing the Bisognano–Wichmann circularity, `v198`). The bounded residual is then reduced
  once more (`v201`): writing the DtN as `Λ=|k|+M_f` with `M_f` multiplication by the boundary curvature
  `f(θ)`, block-diagonality holds iff `f` is `Z₄`-invariant, and a curvature sourced by the four `μ₄` marks
  `f=Σⱼ g(θ−2πj/4)` *is* automatically `Z₄`-invariant — so the `μ₄`-mark orbit (forced by `v195`) *forces*
  the sub-principal symbol block-diagonal. The entire residual thus collapses to the **mark-locality** of
  the DtN (the seam flat away from the `μ₄` marks `=` the conformal-deck structure) — a foundational
  symmetry postulate in its sharpest, structurally-definitional form (the role `c=const` plays in
  relativity), not a missing theorem.
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
the one item that needs a human constructive-geometry argument (or a proof assistant).

**Latest round (`v269`–`v278`) — the open core is now two sharply-located math obligations.** The
boundary QFT gained a **perturbative 4D layer**: the spectral-action S-matrix `S_pert` is
Epstein–Glaser-constructible (`v269`), with a concrete one-loop quartic (`v271`) and the SM gauge
β-coefficients `(41/10, −19/6, −7)` from the carrier content (`v273`), bridged to the physical asymptotic
S-matrix `S_phys` via LSZ with **one-loop unitarity** verified (the optical theorem: the bubble cut equals
the two-body phase space, `v278`) — for the matter+gauge sector; the `R²/Weyl²` gravity sector is
renormalizable but non-unitary (the Stelle ghost, red-team `rt_F`), which is *exactly* the nonperturbative
frontier. These collapse (`v282`/`v335`) to **one** structural theorem `SEAM.EQUIV.01` — `QGEO.SYM.01` is a
**corollary** of it (a conformal net's vacuum is rotation-invariant by axiom, so the μ₄ deck follows with no extra
premise; `v335`, Lean `qgeoSymIsCorollary`), and `QG.AMB.01` is **not** a second structural item but a *decoupled
general* Euclidean-QG problem (the conformal-factor problem, GHP 1978; gap-decoupled, no readout depends on it).
Concretely the two faces are: **(1)** the geometric postulate *the raw RP seam state is the flat τ=i pillowcase*
(`v276`: granting it, the modular commutator `[ρ,H]=0` closes to all orders, since a flat isometry commutes with
every function of its Laplacian); **(2)** the holomorphy bit — *is the seam-Calderón boundary net holomorphic
(`det K = 1`)?* (`v277`: every other `(E8)₁` invariant — c = 8, det Cartan 1, the 248-current character —
already matches; the `c = 8` counterexample `SO(16)` has `det Cartan = 4`). The single mass anchor is
moreover **over-determined** (`v274`: Newton's G and the dark-energy prediction give the same Planck mass
to 0.11%, conditional on the Λ-branch), and the absolute neutrino scale is **one seesaw ratio** (`v272`).

**Self-investigation round (`v280`–`v283`) — the two obligations are one object.** A direct numerical
experiment on the actual flat τ=i pillowcase orbifold realises the whole chain
(`[ρ,Δ]=0 ⇒ [ρ,H]=0 ⇒ [ρ,C]=0 ⇒ ω∘ρ=ω`, route-(i) evidence, `v280`); the Tier-B holomorphy bit is the anyon
count (`#anyons = |det K|`, the condensation tower `16→4→1`, Gauss–Milgram `c=8`, `v281`); and — the candidate
**simplification** — `χ_E8 = j^{1/3}` gives `χ_E8(i) = 1728^{1/3} = 12`, so `τ=i` is **both** the order-4 CM
point (the `QGEO.SYM.01` flat geometry) **and** the `(E8)₁` partition-function modulus (the `QG.AMB.01`
holomorphy): the two obligations are **two faces of one object**, *"the raw seam is `(E8)₁` at `τ=i`"* —
dropping the open count from two to **one** (`v282`). That single open lemma is now attacked from **two
decomposed routes**: RP-state uniqueness (a 6-lemma chain, 5/6 discharged — Troyanov reduces the rest to
*"the raw seam is the constant-curvature state"*, `v284`) and seam-net condensation (a 4-lemma chain, 3/4
discharged — the open bit is `det K=1` = `QGEO.SYM.01`, `v285`); the two routes' open lemmas **coincide**, so
the one statement that closes both is a **canonical equivalence between the raw seam KMS/DtN state and the
holomorphic `(E8)₁` net at `τ=i`**. The recent round's computable predictions are all
consistent at `<2σ`, with two sharp near-term kill tests (Σm_ν floor, proton decay; `v283`).

**Closing sprint (`v286`–`v288`) — the one open core is now a single *named* theorem.** Instead of more
readouts, the open structure is concentrated on one arrow: the **Seam Equivalence Theorem** `SEAM.EQUIV.01`
(`v286`) — *the raw RP seam state IS the holomorphic `(E8)₁` boundary net at `τ=i`*. The contract types four
objects and six arrows and enforces an **import firewall** proving the two proof routes never import each
other (killing the *"`E8` smuggled into the geometry and pulled back out"* circularity). Both routes are then
attacked directly: **Route A** (AQFT, `v287`) reduces the theorem to **one** standard import — *"invertible
Gaussian bulk ⇒ single-sector boundary"* (4/5 lemmas discharged); and **Route B** (DtN, `v288`) **proves** the
full-`L²` lift of the subprincipal `ℤ₄` block-diagonality (a mark-sourced curvature has Fourier support only on
modes `≡ 0 mod 4`, so `[ρ,Λ]=0` on all of `L²`; lifts `v201`/`v284`), shrinking the residual to the single
sharper question *"why is the raw seam subprincipal term mark-local?"*. The honest positioning: **TFPT is
structurally complete modulo one named Seam Equivalence Theorem**, plus an absolute unit (`v_geo`), a transfer
functor (`F_transfer`) and an optional full-QG summit (`QG.AMB.01`).

**Flat-Away round (`v289`–`v297`) — the residual reduced to one shared geometric input, with proofs.** The
remaining question is decomposed into a 5-lemma chain whose *only* open link is **Flat-Away** — *RP + gap + the
four marks ⇒ the curvature vanishes away from the marks* (`v289`). An honest red-team shows `ℤ₄`-invariance is
**not** mark-locality (a smooth `ε·cos(4θ)` passes the commutator yet shifts the spectrum, `v290`), so Flat-Away
is named as its own mini-theorem (`v291`) with **three independent routes**, each carried to a precise reduction:
the **heat route** — the heat-trace deviation is a positive-definite quadratic form, *proved analytically* via
convexity (`v295`), with the exact `a₂` divided-difference kernel now in **closed form**
`W_k(t) = t(1−e^{−4kt})/(8k(1−e^{−t}))` + finite middle (`v296`) and **Lean-formalised**
(`FORM.FLATAWAY.01`, axiom-clean); the **spectral route** — the spectral-mismatch Hessian over the full
smooth-`ℤ₄` space is positive-definite, so flat is a strict isolated minimum (`v293`); the **variational route**
— Troyanov uniqueness gives the flat cone metric as the unique curvature-energy minimiser (`v294`). And **Route A**'s
import is now a citable theorem stack (Kitaev/Freed–Hopkins → Müger/Kawahigashi–Longo–Müger →
Conway–Sloane/Dong–Xu, `v297`) modulo the **same** geometric input as Route B. So both routes reduce
`SEAM.EQUIV.01` to one shared external fact — flat away from the marks.

**Closing arc (`v300`–`v302`) — the shared fact pinned; no undischarged TFPT-internal assumption left.** Three
moves finish the reduction. **(`v300`)** Flat-Away is hardened from a *soft* minimum to a **discrete** degeneracy
obstruction (any smooth off-mark mode splits a doubly-degenerate Steklov level, changing the spectral multiset),
and its pin is **derived** from the `(E8)₁` integer-weight character `E₄/η⁸ = q^{−1/3}(1+248q+…)` via 2d Steklov
conformal rigidity — so Route B's residual *coincides with* Route A's rationality. **(`v301`)** Route A's one open
hypothesis (*"the quasi-free bulk is invertible"*) is discharged by the **free-fermion classification**: a gapped
16-Majorana (`c=8`) Gaussian bulk is automatically invertible (`#anyons = |det K_E8| = 1`; the gauged `D8=SO(16)`
contrast has `det=4`), which removes the topological-order obstruction. **(`v302`)** The single spectral input
that remains, *"the quasi-free bulk is gapped"*, is identified with the **derived Recovery gap**
`Δ = 6·ln(3/2) ≈ 2.43 > 0` of the frozen transfer spectrum `{1,(2/3)⁶,(1/3)⁶}` (margin `Δ−31/(4π²) ≈ 1.65 > 0`);
by Osterwalder–Schrader / quasi-free clustering a transfer gap *is* a bulk mass gap. **Net:** `SEAM.EQUIV.01`
stays `[O]` (not machine-proved end-to-end), but its entire residual is now a composition of **standard cited
theorems** (OS/clustering, Kitaev free-fermion, the `v297` AQFT stack) over **established** TFPT facts — *no
undischarged TFPT-internal assumption remains*.

**The arithmetic arc (`v313`–`v321`) + the Lean keystone (`FORM.SEAMEQUIV.01`).** A cyclotomic capstone makes the
SM *structural* sector exact: the three generations, the two CP phases and their orbit/hierarchy are the cyclotomic
field `ℚ(ζ₃₀)` with Galois group `μ₄ × ℤ₂` (degree `8 = rank E₈`), forced by the atoms `{2,3,5}`; the seed `φ₀`
itself reduces to a pure function of `π`, so there are **zero dimensionless free parameters** — `{a, π, v_geo}` is
the complete input (`v318`). This yields a **new falsifiable prediction**: the two CP phases are Galois-locked,
`δ_PMNS = δ_CKM,lead + π = 240°` (`v320`; kill test at DUNE/Hyper-K). And the `SEAM.EQUIV.01` closing chain is now
**Lean-formalised** (`FORM.SEAMEQUIV.01`, `lake build` clean): the composition `gap → invertible → holomorphic c=8
→ (E8)₁` is machine-checked, with `#print axioms` pinning the residual to exactly the named cited theorems + the
one OS input.
A development timeline of all `320+` scripts is in `introduction.tex` (and on the website verification page).

---

*Claim discipline: nothing in this repository is marked closed that is not machine-verified, and
no dimensionful quantity is claimed as a derivation from pure numbers. See `status_ledger.csv`
for the authoritative, per-claim status.*
