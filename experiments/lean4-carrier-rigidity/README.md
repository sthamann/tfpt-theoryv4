# TFPT Carrier Rigidity — Formal Verification in Lean 4

This directory contains a **machine-checked proof in Lean 4** of the
load-bearing algebraic content of Paper 2 of the TFPT 4.5 series
(*Carrier Rigidity, Hypercharge, and the Standard Model Packet from
Boundary Polarization*).

## What is proved

> **Theorem (Carrier polynomial — corollary of boundary polarization).**
> Let `A` be a ring and let `P₋, P₊ ∈ A` be two orthogonal
> idempotents summing to `1`. Define the integer-scaled generator
>
> ```
> sixY := -2 · P₋ + 3 · P₊      (= 6 · Y)
> ```
>
> Then
>
> ```
> sixY² − sixY − 6 = 0,
> ```
>
> which, after dividing by `6` in a `ℚ`-algebra, is the determinant-
> normalised carrier polynomial `6 Y² − Y − 1 = 0` with
> `Y = -P₋/3 + P₊/2`.
>
> Formally verified: `TFPT.Carrier.Polarization.sixY_carrier_polynomial`.

> **Theorem (Discrete rigidity).** The integer pair `(q₋, q₊)` satisfying
>
> * `3 q₋ + 2 q₊ = 0`
> * `q₋ < 0 < q₊`
> * `Int.gcd q₋ q₊ = 1`
>
> is unique: `(q₋, q₊) = (-2, 3)`.
> After determinant normalisation `Y := (q₋ P₋ + q₊ P₊)/6` this fixes
> the rational eigenvalues `-1/3` and `1/2`.
>
> Formally verified: `TFPT.Carrier.Rigidity.unique_carrier_pair`.

> **Corollary (Hypercharge spectrum).** In the canonical 5×5
> diagonal model with `dim E₋ = 3, dim E₊ = 2`,
>
> ```
> Y = diag(-1/3, -1/3, -1/3, 1/2, 1/2),    tr Y = 0,
> 6 Y² − Y − 1 = 0.
> ```
>
> This is the Standard-Model hypercharge vector of the first chiral
> family in the carrier basis.
>
> Formally verified: `TFPT.Carrier.Hypercharge.trace_Y` and
> `TFPT.Carrier.Hypercharge.Y_carrier_polynomial`.

> **Theorem (Glue uniqueness + carrier index, v89/v92 cores; added
> 2026-06-10).** On the carrier discriminant form `A = ℤ₄ × ℤ₄` with
> `qZ(x,y) = (5x² + 3y²) mod 8`:
>
> * the isotropic elements are exactly
>   `{(0,0), (1,1), (1,3), (2,2), (3,1), (3,3)}`;
> * the order-4 isotropic elements generate exactly **two** cyclic
>   subgroups `H₁ = ⟨(1,1)⟩`, `H₂ = ⟨(1,3)⟩`, the unique Klein
>   four-subgroup is **not** isotropic, and the spinor swap
>   `(x,y) ↦ (x,−y)` provably exchanges `H₁ ↔ H₂` — the Lagrangian
>   (`μ₄`) glue is **unique up to the sheet**;
> * the unique isotropic order-2 element is `(2,2)` (the `SO(16)₁`
>   halfway stage of the extension tower);
> * carrier index arithmetic: `μ(D₅)·μ(A₃) = 16`, `[B:A]² = 16 ⇒`
>   Jones index `4 = |μ₄| = |ℤ₂|²`, and `16/4² = 1` (μ-additivity:
>   holomorphy follows from index 4); glue sectors are `h = 1`
>   currents and `248 = 45+15+64+64+60`.
>
> All by kernel `decide` (no `native_decide`).
> Formally verified: `TFPT.Carrier.GlueUniqueness.*` (ten theorems,
> wired into `AxiomCheck`/`AuditCheck`; mirrors
> `verification/v89_carrier_index_lemma.py` and
> `verification/v92_glue_uniqueness.py`, ledger `FORM.GLUE.01`).

> **Theorem (Seam-deck closure — the `QGEO.SYM.01` conditional theorem;
> added 2026-06-15).** The last open premise of TFPT, `QGEO.SYM.01`
> ("the carrier μ₄ clock is the conformal deck of the seam"), reduces
> (v201/v210) to: *the raw seam DtN sub-principal symbol is mark-local*
> ⇒ *the carrier clock preserves the quasi-free state* (`ω∘ρ=ω`). This
> module formalises that **implication**:
>
> * `geom_sum_fourth_root`: for `ζ : ℂ` with `ζ⁴ = 1`,
>   `Σ_{j<4} ζ^j = if ζ = 1 then 4 else 0` (4th-root character
>   orthogonality — the kernel that makes a μ₄-mark sum vanish off
>   `mod 4`);
> * `clock_gen_pow_four`, `mark_sum_residue_nonzero`: the clock
>   generator `-i` has order 4 and the three non-trivial residues give a
>   vanishing mark sum, so a μ₄-mark-sourced curvature is supported only
>   on modes `≡ 0 (mod 4)`;
> * `markLocal_blockDiagonal`: a mark-local Toeplitz symbol connects only
>   equal clock-characters (`f_{n-n'} ≠ 0 ⇒ (n ≡ n' mod 4)`), i.e.
>   `[ρ, M_f] = 0`;
> * `SeamDeckPremise` (structure): the **physical premise** that the raw
>   seam DtN is mark-local — a typed target consumed, *not* proved,
>   exactly as `CalderonProjector` encodes the Paper-1 analytic input;
> * `SeamDeckPremise.clock_invariant`: **given** the premise, the clock
>   commutes with the DtN ⇒ the quasi-free state is invariant (`ω∘ρ=ω`).
>
> So the **implication** mark-local ⇒ `ω∘ρ=ω` is `[F]` (machine-proved);
> the **premise** (the physical seam *is* mark-local) stays `[O]` — the
> one fundamental seam-identification postulate, **not** closed here.
> Formally verified: `TFPT.Carrier.SeamDeckClosure.*` (mirrors
> `verification/v201_seam_subprincipal_marks.py` and
> `verification/v210_mark_local_dtn.py`, ledger `FORM.QGEO.01`).

> **Theorem (Möbius uniformisation — the `QGEO.UNIFORM.01` normal form;
> added 2026-06-15).** The constructive `UNIFORM` node of the QGEO proof
> tree (v177): a genus-0 curve with four reduced marks and a faithful
> order-4 clock rotating them is Möbius-equivalent to `(ℙ¹, μ₄)`.
> Machine-proved (`TfptCarrier/MobiusUniformisation.lean`):
>
> * `rho_pow_four`, `rho_order_exactly_four`: the clock `ρ : z ↦ i z`
>   satisfies `ρ⁴ = id` and `ρ² ≠ id` (order exactly 4);
> * `sigma_invol`, `sigma_rho_sigma`: the reflection `σ : z ↦ 1/z` is an
>   involution with `σρσ = ρ⁻¹` — so `⟨ρ, σ⟩` is the dihedral `D₄` of
>   order 8 (the faithful `D₄` of v168);
> * `orbit_scales_to_mu4`: a non-fixed point `a ≠ 0` has orbit
>   `{a, ia, -a, -ia}`, scaling (`z ↦ z/a`) to `μ₄ = {1, i, -1, -i}`;
> * `sigma_perm_mu4`: `σ` permutes `μ₄` (fixes `1, -1`, swaps `i, -i`);
> * `mult_order_four_iff`: a multiplier map `z ↦ ζ z` has order exactly 4
>   iff `ζ = i ∨ ζ = -i` — the canonical representative is `z ↦ i z`.
>
> The geometric half of the seam realisation is thus `[F]`, **given** the
> four marks and the clock; the raw-seam marking obligation
> `QGEO.MARKS.01` stays `[O]`. Bundled as `uniformisation_normal_form`
> and signature-locked in `AuditContract.lean`. Formally verified:
> `TFPT.Carrier.MobiusUniformisation.*` (mirrors
> `verification/v177_seam_marking_kernel.py`, ledger `FORM.QGEO.02`).

> **Theorem (Cohomology grading — the `QGEO.COHOM.01` character node +
> MODULE parity; added 2026-06-15).** The constructive `COHOM` node of
> the QGEO proof tree (v177). Machine-proved
> (`TfptCarrier/CohomologyGrading.lean`):
>
> * `omega1/2/3_pullback`: the three `H^1(P^1 \ mu4)` eigenforms
>   `omega_k = z^(k-1)/(z^4-1)` have pullback character
>   `rho^* omega_k = i^k omega_k` under the clock `rho : z ↦ i z`
>   (`i^1 = i`, `i^2 = -1`, `i^3 = -i`) — each an exact rational-function
>   identity (the denominator is clock-invariant, `(iz)^4-1 = z^4-1`);
> * `character_grading`: the eigenvalues `(i, -1, -i)` are the characters
>   of weights `(1,2,3)` = the `A_3` exponents = `Spec(Q_+)`, rank
>   `3 = N_fam`;
> * `omega1/2/3_reflection` (MODULE parity): the reflection
>   `sigma : z ↦ 1/z` satisfies `sigma^* omega_1 = omega_3`,
>   `sigma^* omega_2 = omega_2`, `sigma^* omega_3 = omega_1` — the
>   integer-model parity `w_1 <-> w_3`, `w_2` fixed.
>
> The geometric `COHOM`/`MODULE`-parity nodes are thus `[F]`, given the
> marked curve `(P^1, mu4)` and the clock; the `MARKS`/`KERNEL`
> obligations and the MODULE *uniqueness* (multiplicity-free + residue
> normalisation) stay `[O]`/symbolic. Bundled as `cohom_grading` and
> signature-locked in `AuditContract.lean`. Formally verified:
> `TFPT.Carrier.CohomologyGrading.*` (mirrors
> `verification/v177_seam_marking_kernel.py`, ledger `FORM.QGEO.03`).

> **Theorem (Anchor rank-gap uniqueness — `ANCHOR.RANKGAP.UNIQUENESS`;
> added 2026-07-07).** The anchor ladder module (`AnchorLadder.lean`)
> reads `p₄ − p₃ = 8 = rank E₈` off the anchor `a = (1,1,2)`
> (`rank_step`). The new converse `rankgap_uniqueness` shows the
> equation *selects* the anchor: for any positive integers `x, y, z`
> with `x⁴+y⁴+z⁴ = x³+y³+z³+8`, the triple is `(1,1,2)` up to
> permutation — the per-entry contribution `w³(w−1)` is `0` at `w = 1`,
> `8` at `w = 2` and `≥ 54` for `w ≥ 3` (`cube_step_ge_54`,
> `overshoot_ge_three`), so exactly one entry is `2`. Axiom footprint:
> `[propext, Classical.choice, Quot.sound]` only. Scope (honest): this
> forces the anchor *within* positive integer triples of length 3; that
> the anchor is such a triple, and that the rank gap is the right
> normalisation, remain the axiom-side inputs.
> Formally verified: `TFPT.Carrier.AnchorLadder.rankgap_uniqueness`.

## Why this is interesting

* The carrier polynomial `6 Y² − Y − 1 = 0` is in earlier TFPT drafts
  *assumed*. Paper 2 demoted it to a **corollary** of the orthogonal-
  idempotent axioms + the integer Diophantine rigidity. This repo
  formalises that demotion in a proof assistant — so the SM hypercharge
  multiplet becomes a *theorem in a computer algebra system*, not an
  empirical input.

* The proof uses only four abstract axioms:
  `P₋² = P₋`, `P₊² = P₊`, `P₋ P₊ = 0`, `P₊ P₋ = 0`, `P₋ + P₊ = 1`.
  No analytic content, no SI units, no fitted constants.

* If the proof compiles in Lean 4 with Mathlib, it is — barring bugs in
  Lean's kernel itself — a *formal* certificate that the SM hypercharge
  spectrum follows from the TFPT boundary axioms.

## Repository layout

```
lean4-carrier-rigidity/
├── lean-toolchain                 # pinned: leanprover/lean4:v4.29.1
├── lakefile.lean                  # build config, Mathlib v4.29.1
├── TfptCarrier.lean               # top-level entry, re-exports
└── TfptCarrier/
    ├── Polarization.lean          # Layer 1: sixY² − sixY − 6 = 0
    ├── Rigidity.lean              # Layer 3: (q₋, q₊) = (-2, 3)
    ├── Hypercharge.lean           # Layer 2: 5×5 model + tr Y = 0
    ├── Sanity.lean                # #eval smoke tests
    └── AxiomCheck.lean            # #print axioms for the four headlines
```

## How to build

### 1. Install `elan` (Lean's toolchain manager)

```bash
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain none
export PATH="$HOME/.elan/bin:$PATH"
```

### 2. Build the project

From this directory:

```bash
lake update                # fetch Mathlib v4.29.1 and run cache hooks
lake exe cache get         # download pre-built Mathlib oleans (~3 min)
lake build                 # compiles everything (~30 s after cache get)
```

The first `lake update` clones Mathlib (~500 MB). The cache step
downloads ~8 200 pre-built `.olean` files (~1 GB) so the actual
build of *this* project takes a few seconds.

### 3. Re-check just the proofs

```bash
lake build TfptCarrier
```

A successful build prints:

```
Build completed successfully (1231 jobs).
```

plus the `#eval` outputs from `Sanity.lean` and the axiom listings
from `AxiomCheck.lean`. Any `sorry`, `admit`, kernel error, or
non-standard axiom dependency will be flagged.

## Map to TFPT Paper 2

| Lean theorem | Paper 2 reference |
| --- | --- |
| `Polarization` (structure) | §2 "Carrier polynomial as a corollary", eq. for `P_±` |
| `Polarization.sixY_carrier_polynomial` | Theorem (Carrier polynomial from boundary polarization), proof spine |
| `Rigidity.unique_carrier_pair` | Inline integer argument: `3 q₋ + 2 q₊ = 0`, `q₋ < 0 < q₊`, `gcd = 1` |
| `Hypercharge.Y` and `Y_diag_entries` | `Y = diag(-1/3, -1/3, -1/3, 1/2, 1/2)` |
| `Hypercharge.trace_Y` | `tr_E Y = 0` |
| `Hypercharge.Y_carrier_polynomial` | `6 Y² − Y − 1 = 0` on the concrete model |

## Status

> ✅ **Verified on this machine** with `lake build`
> (Lean 4.29.1 + Mathlib v4.29.1, macOS arm64).
> All four theorems compile, zero `sorry`s, no `admit`s.

```
$ lake build
Build completed successfully (1231 jobs).

#eval Y.trace                          -- 0
#eval ((6 : ℚ) • (Y * Y) - Y - 1)      -- !![0,0,0,0,0; 0,0,0,0,0; ...]
```

`#print axioms` for each of the four headline theorems reports only
the three standard Lean axioms `propext`, `Classical.choice`,
`Quot.sound`. No private hypotheses, no `sorry`-laundering, no
domain-specific axioms. The full chain
`Polarization → Rigidity → Hypercharge` is formally verified.

| Module | Status | Lines | Axioms |
| --- | --- | --- | --- |
| `Polarization.lean` | ✅ compiles | ~150 | propext, Classical.choice, Quot.sound |
| `Rigidity.lean`     | ✅ compiles | ~100 | propext, Classical.choice, Quot.sound |
| `Hypercharge.lean`  | ✅ compiles |  ~95 | propext, Classical.choice, Quot.sound |
| `Sanity.lean`       | ✅ `#eval`s match expected output | 30 | n/a |
| `AxiomCheck.lean`   | ✅ `#print axioms` confirms cleanness | 25 | n/a |

## Caveats and audit surface

* This formalises the *algebraic* corollary of Paper 2. The
  representation-theoretic *premises* (compact Higgs index → `dim E₊ = 2`;
  primitive indecomposable Yukawa type → `dim E₋ = 3`) are imported as
  numerical inputs to the `Hypercharge` model. A future Layer 4 would
  formalise those premises directly from the index-theoretic data, which
  is substantially more work and is out of scope here.

* The trace identity uses `Matrix.trace` on `Fin 5 × Fin 5` rational
  matrices. The corresponding abstract statement — `tr Y = 0` for
  *any* faithful finite-dimensional representation with the prescribed
  ranks — is an immediate corollary but is not separately stated.

* Mathlib version is pinned to `v4.29.1` for reproducibility. Pinning
  forward is straightforward, but bumping silently is discouraged.

## Next steps

1. Add a GitHub Actions workflow that runs `lake build` and reports
   the number of `sorry`s and `axiom`s introduced (should be zero
   outside Lean's core).
2. Add a `Tests/Sanity.lean` file with `#eval` checks that print
   the diagonal of `Y` and the value of `trace Y` so that humans can
   read the certificate without running Lean themselves.
3. Extend the formalisation to the discrete `Z₆` gauge quotient
   `G_phys = (SU(3) × SU(2) × U(1)_Y) / Z₆`. This requires
   group-theoretic machinery beyond the current scope.
