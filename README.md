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
- **Solar angle** `sin²θ₁₂ = 1/3 − φ₀/2 = 0.306747` (frozen prediction; conditional on the
  seam-misalignment lemma).
- **Cosmology**: `Ω_b`, the Starobinsky scalaron mass, `Λ ~ e^(−2α⁻¹)`, cosmic birefringence
  `β = φ₀/(4π) ≈ 0.2424°`.
- **Self-consistency**: "parameter-free" is a *theorem* — the gapped boundary transport
  (`Δ = 6·log(3/2) > 0`) has, by Perron–Frobenius, a **unique attractor** at rate `(2/3)⁶`; the
  hull carries a literal order-`30 = 2·3·5` Coxeter cycle.

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
is closed (Fursaev–Solodukhin ⟹ `c₃ = 1/(8π)` is the unique value giving `S = A/4`), and the
residual is identified as the one irreducible dimensionful anchor (`1/G` is UV-sensitive,
Sakharov-type induced gravity) — not a diffuse gap.

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
| `v1_*.py … v71_*.py` | 71 numbered claim checks (one file per claim cluster). |
| `run_all.py` | Runs the whole suite; ends `ALL CHECKS PASSED`. |
| `tfpt_constants.py` | Shared constants + `check()` harness. |
| `status_ledger.csv` | **Single source of truth.** Every claim with id, status, location, dependency, script — *versioned* (`active`, `canonical_status`, `supersedes`). |
| `make_figures.py` | Regenerates the figures (status heatmap, attractor, Coxeter circle, …). |
| `make_manifest.py` | Writes `manifest.sha256` + `lean_manifest.sha256` (content digests). |
| `wolfram/tfpt_readouts.wl` | Independent second path on Wolfram Engine (`101/101` checks). |
| `redteam/run_redteam.py` | **Adversarial layer.** Tries to *break* the five reductions (Targets A–E); verdicts in `REDTEAM.*` ledger rows + `tfpt_5_redteam.tex`. |

### Other directories

- `experiments/lean4-carrier-rigidity/` — Lean 4 proof of the carrier algebra (P2: hypercharge,
  anomaly-freedom, integer rigidity), machine-formalised `[F]`.
- `experiments/` — research-level explorations (e.g. `eht-achromatic-residual`, discovery scripts).
- `figures/` — generated PDFs used by the documents.
- `manifest.sha256`, `lean_manifest.sha256` — reproducibility digests.
- `build.sh` — compiles all documents.

---

## 3. Reproduce / verify

Dependencies: a LaTeX distribution (`pdflatex`), Python 3 with `sympy`, `mpmath`, `numpy`,
`matplotlib`; optionally Wolfram Engine and Lean 4 (`elan`/`lake`).

```bash
# 1. Compile the 9 active documents  ->  "9 ok, 0 failed"
bash build.sh notes

# 2. Run the Python verification suite  ->  "ALL CHECKS PASSED"
cd verification && python run_all.py

# 3. Independent Wolfram path  ->  "101/101 passed"  (optional, needs Wolfram Engine)
wolframscript -file verification/wolfram/tfpt_readouts.wl

# 4. Lean carrier-rigidity proof  ->  "AUDIT: PASS"  (optional)
cd experiments/lean4-carrier-rigidity && lake exe cache get && bash scripts/audit.sh

# 5. Red Team / Stress Test layer (adversarial; prints a status per target A-E)
cd verification/redteam && python run_redteam.py

# 6. Regenerate reproducibility manifests (run last)
python verification/make_manifest.py
```

Every script cited in `run_all.py` is also cited inline in the documents via `\veri{vN_*.py}`,
and the status heatmap is generated directly from `status_ledger.csv`, so the papers, the suite,
and the ledger stay in lock-step.

---

## 4. Status markers

Used consistently across all documents and the ledger:

| Marker | Meaning |
|---|---|
| `[I]` | exact identity |
| `[L]` | Lie-/lattice-theorem |
| `[F]` | formalised (Lean) |
| `[N]` | numerical fixed point |
| `[P]` | physical / conditional |
| `[A]` | axiom / anchor / open |

The ledger is *append-only and versioned*: superseded rows are marked `active=false` with a
`canonical_status` pointer, so the current authoritative status of any claim is unambiguous.

---

## 5. What is genuinely open

- **The central theorem**: `1/(8π)` from the seam-determinant replica — structure closed,
  residual reduced to the one dimensionful induced-gravity anchor.
- **Full covariant metric-sector / ambient QG measure** (`G_metric`) — kept open by design;
  gap-decoupled from the admissible IR sector (`Δ_eff = 1.648 > 0`).
- **Absolute amplitude normalisation** (`U_point`) — an anchor; the quark *ratios* are closed.
- **Frontier interfaces** (`m_p/m_e`, `η_B`, Koide, axion relic) — deliberately typed as
  interfaces, never quoted as compiler outputs.

The remaining distance is therefore not a list but **one central physical theorem plus a single
irreducible dimensionful anchor**.

---

*Claim discipline: nothing in this repository is marked closed that is not machine-verified, and
no dimensionful quantity is claimed as a derivation from pure numbers. See `status_ledger.csv`
for the authoritative, per-claim status.*
