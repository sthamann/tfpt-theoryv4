# theory-contracts — pure-math contracts (NOT empirical scorecard rows)

These are **theory contracts**: computational verifications of internal mathematical claims.
They are deliberately kept **out of `evidence_scorecard.json`** (which is for empirical
confrontations only) — passing a theory contract is not external evidence, it is internal
consistency.

## `qgeo_dtn_mark_locality.py`

QGEO Dirichlet-to-Neumann **mark-locality**: with the Z4 marks at `θ = j·π/2` and
`Λ = |D_θ| + M_f`, `f(θ) = Σ_{j=0}^{3} g(θ − jπ/2)`:

1. the four π/2-translates cancel every Fourier mode except `n ≡ 0 (mod 4)`;
2. therefore `[ρ, Λ] = 0` (ρ = rotation by π/2, the Z4 generator);
3. therefore `ω ∘ ρ = ω` for the Λ-canonical (Gibbs/spectral) state.

Verified numerically on the circle (N=64) to ~1e-16, **with the negative controls the
contract must fail on**: Z3 marks (support mod 3) and 4 generic unequal marks both break the
commutator (`[ρ,Λ]/|Λ| ≈ 0.4–0.5`) and the state invariance — exactly as required.

```bash
cd experiments/theory-contracts && python3 qgeo_dtn_mark_locality.py
```

Result (2026-06-15): **CONTRACT HOLDS** (Z4 commutes to 2e-16; Z3 + generic controls break it).
This mirrors the verification-suite QGEO contracts (v168/v192/v193) but as a standalone,
data-independent check; it is intentionally not load-bearing here.

## `qgeo_soff_reconstruction.py` — the reconstruction (tomography) version (2026-07-06)

`qgeo_dtn_mark_locality.py` verifies the exact statement. This contract adds the
**reconstruction/tomography version** — the honest bridge toward a *controlled system*
(BEC analog horizon, superconducting waveguide, optical cavity, numerical Steklov
geometry), where the boundary energy form is never known exactly but must be
reconstructed from finitely many noisy spectral measurements:

1. **S_off leakage statistic** on the μ₄ character classes `{n ≡ r mod 4}`:
   `S_off(Λ) = Σ_{r≠s} ‖P_r Λ P_s‖²_F / ‖Λ‖²_F`, reported for the full operator and for
   the sub-principal part alone (the discriminating piece; `|D|` commutes for free, v198).
2. **Reconstruction pipeline**: only the K=40 lowest eigenpairs "measured" with relative
   noise σ (eigenvalues *and* eigenvector mixing); `Λ̂` reassembled and tested.
3. **Clock-angle scan** `L(θ) = ‖[R(θ), Λ̂]‖²/‖Λ̂‖²`: the zero set is the discriminator.
4. **Detection power**: smallest single-mark shift ε detectable through the noise —
   the *instrument requirement* an analog realisation must beat.

Result (2026-07-06): **CONTRACT HOLDS** (`qgeo_soff_results.json`) —

- exact: μ₄ marks give `S_off^sub < 3e-31`; Z₃ and generic marks leak **O(1)** (1.00 / 0.97);
- reconstructed: μ₄ noise floor scales as `O(σ²)` (1.5e-6 at σ=1e-4 → 1.4e-2 at σ=1e-2),
  controls stay at ~0.9 at every noise level — the discrimination survives realistic
  reconstruction noise by 2–6 orders of magnitude;
- clock-angle zero set: μ₄ marks `{π/2, π, 3π/2, 2π}` exactly; Z₃ marks flip it to
  `{2π/3, 4π/3, 2π}`; generic marks keep only the trivial 2π — the clock is *read off*
  the operator, not assumed (θ=π/2 as the smallest faithful clock, cf. the v200 scan);
- power: a mark shift of **ε = 0.001 rad** is 100%-detectable at σ ≤ 1e-3;
  at σ = 1e-2 the requirement is ε ≥ 0.01 rad.

```bash
cd experiments/theory-contracts && python3 qgeo_soff_reconstruction.py
```

Firewall: pure simulation/mathematics; a "hit" in a real analog system would be
escalate-only, never TFPT confirmation. The still-open foundational piece is unchanged
(see "Open next contract" below): *why* the raw RP seam produces the Z4 marking.

## `fo01_transduction_invisibility.py` — the S15 invisibility contract (2026-07-07)

Machine-checks the FO.01 ontology reading (next.txt 2026-07-07 (I)): every observable
is `O = B·T·A`; a **coherent, threshold-triggered amplifier with uniform character
coupling** is a trivial-character readout, so a null on it is *predicted*, not
informative about the core (SIGNATURES.md 0b.1 / S15). Minimal model: 3 character
classes, doubly-stochastic transfer with the frozen spectrum `{1, (2/3)⁶, (1/3)⁶}`,
scrambled control with the same stationary state and a non-kernel spectrum.

Result (2026-07-07): **CONTRACT HOLDS, 5/5 PASS** (`fo01_transduction_results.json`) —

- C1 the uniform functional is *exactly* blind: `max |1·Tⁿp − 1| = 9.8e-15` (the
  trivial character is a left eigenvector of any stochastic transfer);
- C2 the threshold-intensity readout is *statistically* blind: first-step intensity
  ratios KS D = 0.0085 (p = 0.47), threshold burst trains D = 0.006 / counts D = 0.0
  over 20k realisations — **the 20+ FRB intensity/timing nulls are what this
  ontology predicts**;
- C3 a character-resolved readout recovers 64/729 to 1e-12 (visibility once
  `B·P_r ≠ 0`);
- C4 an unequal-weight intensity coupling makes the *same* functional discriminating
  (KS D = 0.061, p = 5e-33) — invisibility is a property of `B`, not of the channel.

```bash
cd experiments/theory-contracts && python3 fo01_transduction_invisibility.py
```

Open formal piece (noted, not claimed): for which *standard emission processes* is
`B·P_r = 0` provable? That is the S15 theory-contract candidate proper.

## `seam_horizon_replica.py`

Seam–Horizon **replica contract** — the kernel-identification premise of `SEAM.THEOREM.01`
(the residual left by v150/v151/v152) exercised **numerically on a discretized seam
collar**, instead of only symbolically on the abstract 2d scalar:

1. **Replica ⇒ EH form on a real operator**: the matched conical deficit
   `G(γ,m) = log det L(γ) − (γ/2π) log det L(2π)` of the gapped lattice cone operator is
   linear in `ln m` with slope `2C(γ)`, on deficit cones (`γ/2π = 1/4, 1/2, 3/4`; error
   0.01–0.05 %) **and on real replica sheets** (`n = 2`: 0.75 %, `n = 3`: 1.5 %).
2. **Coefficient forced, scale = anchor**: the EH slope is stable under IR/size change
   (0.5 % drift), while the intercept (the ζ-scale `μ_lat`) drifts with the
   discretization — v152's "coefficient forced, absolute scale = anchor" exhibited on
   data. **No canonical `3/4` emerges** (recorded honestly; the anchor stays declared).
3. **BFK split for the discretized Calderón kernel**: the Schur identity
   `log det L = log det(halves_D) + log det S` holds to machine precision (~1e-16);
   across three cone angles the Calderón/Schur factor follows a **pure cut-edge law**
   `E(1−γ/2π)` with tip term ≈ 0 (power check: the same model fails on the full
   determinant) — v151's "conically clean", measured on the kernel itself.
4. **The seam's own spectrum**: the two gapped transfer masses `6 ln(3/2), 6 ln 3`
   (spec T = {1, (2/3)⁶, (1/3)⁶}, v302) sit exactly on the calibrated EH line (≤0.05 %),
   and the Perron/attractor mode (`m = 0`) is demonstrably **IR-divergent**, running
   exactly as `−2C ln(IR ratio)` — the recovery gap `Δ = 6 ln(3/2)` is what makes the
   induced-gravity coefficient finite. *The same gap that makes the attractor unique
   makes Newton's constant finite.*

```bash
cd experiments/theory-contracts && python3 seam_horizon_replica.py
```

Result (2026-07-02): **CONTRACT HOLDS, 17/17 checks** (`seam_horizon_replica_results.json`).
Together with v90 (FS derived) + v73 (`k = c₃/2` forced) + v150–v152, the
seam-determinant → replica → EH → `S = A/4` chain is exhibited end-to-end at the
finite/discretized level **with the seam's own kernel**. Open `[O]`, unchanged in type:
the continuum scaling limit (MMST class — the same single residual as `SEAM.EQUIV.01`)
and the one dimensionful anchor. Not claimed: a continuum proof, or a derivation of
`ln(m/μ) = 3/4`. Candidate for promotion via `promote-to-verification` (would sharpen
`SEAM.EHMODEL.03`'s "kernel premise" row, not close `SEAM.THEOREM.01`).

## `born01_deck_envariance.py` — Born-Regel aus Recovery? (2026-07-07)

Answers the dated question "kann TFPT die Born-Regel herleiten?" with a machine-checked
**reduction, not a derivation**. Context: `v130` ("Born square") *uses* `Γ = |A|²` as an
input to explain the clock exponent `p₂ = 2h`; it does not derive `ψ²`. This contract
maps what recovery/deck structure *can* carry and what stays postulated:

- **C1 exponent**: basis-independent normalisation forces `α = 2` within the power family
  (the π/4 basis alone kills every other power; variance over bases 4e-33 at α=2 vs 1e-2 off).
- **C2 sheet pairing**: reality for all phases forces `p = A·σ(A)` — **one amplitude factor
  per Z₂ sheet**, σ the Galois/CP conjugation (v316: Gal Z₂ = CP conj). The imported factor 2
  of v130 acquires a structural origin (typed [C]).
- **C3 deck swap = envariance**: the system swap is undone exactly by the partner-sheet swap;
  ρ_S blind to any partner unitary (5e-16 over 200 random U(2)) — Zurek's envariance with the
  swap implemented by the structural deck instead of an auxiliary environment.
- **C4 kernel sector is counting-decidable**: every frozen kernel weight (2/3, 1/3, (2/3)⁶,
  (1/3)⁶, clock weights `(1−n/3)⁶`) is **3-adic**, so finite fine-graining into 3^k equal
  branches (N_fam-fold branching) decides it by counting — *no continuity axiom on the
  kernel's own probability sector*; exhibited exactly (isometric 3-branch fine-graining).
- **C5 unique invariant pairing**: the matched μ₄ Weyl pair (clock + character-transitive
  shift) on C⁴ admits exactly **one** invariant Hermitian form (the Born pairing); clock
  alone → dim 4, shift alone → dim 4, mismatched N=8 → dim 2.
- **C6 relocation audit (honest negative)**: in dim 2 an explicit non-quadratic frame
  function `u + (1/10)sin(2πu)` satisfies additive normalisation exactly — Born is **not**
  free; the forcing needs C1's power family, C2+C5's deck structure, or dim ≥ 3
  (Gleason 1957 / Busch 2003, cited external theorems).

Result (2026-07-07): **CONTRACT HOLDS, 6/6** (`born01_deck_results.json`). Reading: Born
**reduces** to deck-swap symmetry + matched Weyl pair + finite counting on the 3-adic
sector — the same axiom weight class as envariance, with swap and conjugation structural
instead of postulated. **Stays postulated** (recorded in the JSON): outcomes = character-block
projections, single-outcome selection (the measurement problem — untouched), the two
envariance axioms (locality of p, partner-sheet no-signalling), and continuity/Gleason off
the 3-adic sector. Never a scorecard row; never `[E]`.

```bash
cd experiments/theory-contracts && python3 born01_deck_envariance.py
```

## `nm01_backflow_ep.py` — Non-Markovianität & Exceptional Points (2026-07-07)

Answers the dated user question "sind Information Backflow und Exceptional Points fast
natürliche Konsequenzen von Recovery?" — machine-checked: **NO on both**, and that is the
typed, falsifiable-shaped statement (the S15/FO.01 firewall extended to the
open-quantum-system literature):

- **C1 zero backflow**: the seam channel (fixed CPTP map; classical 3×3 kernel and the
  qubit amplitude-damping realisation with η = (2/3)⁶) contracts trace distance
  monotonically — BLP measure = 0 (max increment −1.5e-15 / −6.1e-8, BLP sum 0.0 over
  100 pairs × 12 steps). A discrete semigroup is CP-divisible; backflow is *impossible*
  in the recovery kernel itself.
- **C2 memory control**: one unrefreshed bath qubit under partial-swap collisions gives
  revivals up to +0.34 — backflow is **bath-memory (bridge) physics**; the data-side face
  of this statement is exactly FO.02b's injection-validated memory gate.
- **C3 no exceptional point**: the transfer is normal (‖[T,Tᵀ]‖ = 5.6e-17) with simple
  spectrum (gaps 665/729, 63/729 exact), eigenvector condition exactly 1; the Jordan
  control has cond ~ 1e16. Typed missing-structure prediction (FO.08 class): seam-eligible
  recovery spectra show **no EP coalescence, no EP hysteresis/chirality**.
- **C4 frozen invariant set**: the requested "dimensionsloser Invariant / festes
  Relaxationsverhältnis / universelle Skalierungsfunktion" already exists parameter-free —
  bend ln3/ln(3/2) = 2.7095, teeth 2/3, 8/27, 64/729, comb pair (ω, ε) = (2.5827, 0.0173)
  with *both* frequency and amplitude fixed; ε < 2 % is the amplitude wall behind every
  well-powered surface null.
- **C5 shape degeneracy**: a wrong-ratio (2.0) two-exponential family fits a single
  noiseless kernel recovery to relative RMS 5.4e-3 (true ratio: 3.3e-16) — single-curve
  *shape* searches are provably weakly discriminating; the power sits in cascades, ratio
  ladders and comb phase (the S3 degeneracy, reproduced standalone).

Result (2026-07-07): **CONTRACT HOLDS, 5/5** (`nm01_backflow_results.json`). Never a
scorecard row; never `[E]`.

```bash
cd experiments/theory-contracts && python3 nm01_backflow_ep.py
```

## `comp01_unique_holomorphic.py` — stärkere Kompression: ein Axiom statt zwei (2026-07-07)

Answers the dated question "gibt es eine noch stärkere Kompression?" — yes, machine-exhibited:
the single axiom **"the seam carries THE unique holomorphic boundary CFT"** replaces (P1, P2):

- **C1**: the c=8 character tower `E4/∏(1−qⁿ)⁸ = {1, 248, 4124, 34752, 213126}` — holomorphy
  pins the theory (dim V₁ = 248 = dim E8; v463 standalone).
- **C2 (the octave control)**: `θ_{E8+E8} ≡ θ_{D16+}` term by term — **two** distinct even
  unimodular lattices share **one** character at c=16: uniqueness fails exactly one octave
  above the seam (the *heterotic-string* octave); at c=24 there are 71 theories
  (count ladder 1 / 2 / 71; Mordell / Witt / Schellekens cited).
- **C3**: holomorphic ⇒ c ≡ 0 mod 8; c=8 is the **smallest AND the only unique** value —
  the seam CFT is the minimal holomorphic CFT.
- **C4 (the compression chain, zero discrete choices)**: 8 = 2|μ₄| ⇒ c₃ = 1/(8π) [P1 = rank
  readout]; x² − 8x + 15 = (x−3)(x−5) ⇒ (N_fam, g_car) = (3, 5) [**P2 becomes a theorem**];
  φ₀ = 0.0531719522, λ_T = 64/729, bend 2.7095, comb (2.5827, 0.0173) all follow exactly.
- **C5 (relocation, honest)**: the axiom itself ("physics has a holomorphic boundary CFT")
  is *not* justified here — that is SEAM.EQUIV.01; lattice uniqueness/counts are cited
  external theorems; the dimensionful anchor + v_geo are untouched.

Result (2026-07-07): **CONTRACT HOLDS, 5/5** (`comp01_unique_holo_results.json`). Never a
scorecard row; never `[E]` as physics — the compression rearranges axioms, it does not
prove them.

```bash
cd experiments/theory-contracts && python3 comp01_unique_holomorphic.py
```

## `flav01_winding_disc2.py` — Diskriminantenklasse 2 auf der Winding-Line (2026-07-07)

Machine-checks the **discriminant-class-2 selector** on the flavor winding line
`R_s = R + s·1e₁ᵀ` (analysis round 2026-07-07). The fingerprint itself is *already
published* (v94_sheet_diamond / ledger `FLAV.DIAMOND.01` / `tfpt_2`):
`Δ(s) = disc χ_{R_s} = 17s⁴−18s³+709s²+588s−7996` and
`Δ(6) = 39200 = 2⁵·5²·7² = 2·(10·14)²` — squarefree class exactly `2 = |Z₂|`.
**New here is the selector reading**: is the physical winding `s = 6` the *unique*
integer with `Δ(s) = 2y²`?

Result (2026-07-07): **CONTRACT HOLDS, 6/6 PASS** (`flav01_winding_disc2_results.json`) —

- C1 the char-poly family `t³−(9+s)t²+(10+5s)t−(8+2s)` and the s=6 triple lock
  (tr 15, det 20, Coxeter-lift 30) recomputed exactly from `R`;
- C2 the published fingerprint reproduced (`Δ(6) = 39200`, class 2);
- C3 **uniqueness scan**: `s = 6` is the *only* `s ∈ [0, 10000]` with `Δ(s) = 2y²`
  (witness `y = 140`); no hit in `[−100, −1]`;
- C4 look-elsewhere control: among squarefree classes `k ≤ 100` only
  `{2: s=6, 23: s=306, 41: s=8, 65: s=3, 89: s=4}` occur — "some small class
  somewhere" is cheap, **class-2 uniqueness** is the discriminating statement;
- C5 sibling control: the spectrally-failing H2 branch `{1,3,4}` (tr 8, det 6) has
  `Δ′(6) = 112224`, class `7014 ≠ 2` — the signature separates the physical branch;
- C6 relocation audit (honest): the fingerprint is old, only the scan + Diophantine
  form `17s⁴−18s³+709s²+588s−7996 = 2y²` (genus-1 quartic, integral points finite
  and effectively computable) are new; the ledger correction "reality does not
  select s=6" stands — this is a *different, post-hoc* criterion, audit-level until
  the global statement is proven **and** "class = 2 = |Z₂|" is derived, not observed.

```bash
cd experiments/theory-contracts && python3 flav01_winding_disc2.py
```

Firewall: pure integer arithmetic; never a scorecard row; never `[E]`-as-physics.
Open Diophantine piece (recorded, not claimed): prove `s = 6` is the only
nonnegative integral point of `Δ(s) = 2y²`.

## `glue01_dynamical_selection.py` — dynamische Glue-Selektion: lokale Gates ⇒ D5⊕A3+μ4 (2026-07-10)

Answers the dated question (Zuse/"Rechnender Raum" round) "kann eine lokale Regel die
**Compiler Closure** `D5 ⊕ A3 + μ4` selektieren — statt nur den E8-Stern zu erreichen?"
The network chain v298→v299→v327→v395 reaches E8 as a *star* T(2,3,5); the closure is a
*decomposition*, whose uniqueness was so far **static** (v15 discriminant classification,
v1 lattice certificate). This contract builds the dynamical layer on the attractor graph
Ê8 (the endpoint of v299's growth, whose Kac marks are the v298 diffusion fixed point):

- **C1 [E]**: Kac marks of Ê6/Ê7/Ê8 satisfy `A·m = 2m` exactly — the deletion menu lives
  on the attractor.
- **C2 [E]**: all single-node deletions of Ê8 = the classical Borel–de Siebenthal list,
  and for *every* deletion (all three diagrams) the glue index `√(∏det/det_amb)` is an
  integer **equal to the deleted Kac mark** — the glue order is attractor data, not input.
- **C3 [E]**: exactly five Ê8 punctures are two-sided (the seam's `|Z₂| = 2` sides):
  A1+E7, A2+E6, A3+D5, A4+A4, A1+A7.
- **C4 [E]**: seam-pairing gate (isomorphic **and cyclic** discriminants) → survivors =
  exactly the v15 candidate list, *recomputed from the menu*; A1+A7 rejected (Z₂ vs Z₈)
  although its glue index is also 4 — the gate is finer than the index.
- **C5 [E]**: spectral octave gate, **measured** by running the same lazy local diffusion
  on each side (max err 4.4e-16 vs `2cos(π/h)`): h-ratios (9, 4, **2**, 1, 4) — ratio
  `|Z₂| = 2` is *unique* at A3+D5.
- **C6 [E]/[C]**: both gates independently select the same unique puncture; deleted mark
  4 ⇒ **μ4 = Z₄ emerges** (= h(A3)), h(D5) = 8 = 2|μ4| = rank(E8) (the P1 rank readout,
  COMP.01), ranks (3,5) = (N_fam, g_car), q(A3)+q(D5) = 2 (even glue, v1).
- **C7 [E] controls**: on Ê7 the octave gate alone fires (A2+A5, both mark-3 deletions)
  but pairing kills it (Z₃ vs Z₆); on Ê6 both gates are empty — the gates are
  independent, their agreement is E8-specific.
- **C8 [O] honest**: imported stay the single-node puncture, the Z₂ atom, and **the
  octave condition itself (post-hoc selector until derived — audit-level, same
  discipline as flav01 C6)**; Borel–de Siebenthal is cited machinery. v15 stays the
  static theorem; **P2 is NOT closed** (Ê8 is v299's seed-dependent growth endpoint).

Result (2026-07-10): **CONTRACT HOLDS, 8/8 PASS** (`glue01_dynamical_results.json`).
Gain over v15: its "familyful" filter *imports* `dim S⁺ = 16` and `N_fam = 3` as
selection criteria — here (3,5), μ4 = Z₄ and the 16 come *out* of two structural gates
that import only the Z₂ atom. Never a scorecard row; never `[E]`-as-physics for the
octave reading. **Follow-up:** the post-hoc octave gate (C8's residual) is *derived*
in `glue02_octave_derivation.py` below.

```bash
cd experiments/theory-contracts && python3 glue01_dynamical_selection.py
```

## `glue02_octave_derivation.py` — die Oktave abgeleitet: μ4-Uhr ersetzt das Gate (2026-07-10)

Closes glue01's own C8 residual ("octave condition post-hoc until derived"): the octave
gate is **eliminated as an input**. The independently load-bearing seam premise "the
clock has order 4 = |μ4|" (in-suite: marks = μ4, v216/v453; transfer inherits the clock
and is forced block-diagonal, v446/v445) replaces it as the selector, and the octave
reappears as a **proved property** of the selected pair:

- **C1 [E]**: clock premise recomputed standalone (v445 mini): commutant of the order-4
  clock = exactly the μ4 block algebra (iff); order-2 commutant strictly larger.
- **C2 [E]**: **clock ⇒ spinorial glue**: `disc(D_n) = Z4 = {0,v,s,s'}` has element
  orders {1,2,4,4} — every order-4 generator is a spinor class, so a μ4-cyclic glue
  necessarily runs through the half-spinor sector (n=5: dim 16 = `dim S⁺`); the vector
  class (order 2) cannot carry the clock.
- **C3 [E]**: on glue01's machine-derived two-sided menu, disc pair ≅ (Z4, Z4) selects
  A3+D5 **uniquely — no octave used**.
- **C4 [E]**: the octave is now a **theorem**: `h = |disc|` characterises the A-family
  exactly (family Coxeter clock = seam clock, h(A3) = 4 = |μ4|); `h = 2|disc|`
  characterises **D5** exactly (h = 8 = 2|μ4| = rank E8). `h₂ = |Z₂|·h₁` derived.
- **C5 [E]**: global ladder (no menu import): clock pairing over all ADE yields pairs
  *only* at total rank ≡ 0 mod 8 (rungs 8/16/24/32 with 1/3/5/7 pairs — the same octave
  structure in which COMP.01's holomorphic uniqueness fails above c=8); minimal rung
  unique = A3⊕D5, whose Z4 glue is **built explicitly**: 240 roots of norm 2 (classes
  52+64+60+64), all integer inner products, index det 1 — **E8 emerges from the seam
  pair**. Honest: ratio 2 recurs on `(D_n, D_{2n−1})`, n ≡ 3 mod 8 (rank 32, 56, …) —
  minimality does the pinning, not the octave alone.
- **C6 [E] controls**: A3+A3 not gluable (3/4+3/4 ≢ 0 mod 2); D7/D9/D11 fail vs A3
  (n ≢ 5 mod 8); odd clocks and A1+A7 excluded.
- **C7 [O] honest**: imported stay the clock's raw-seam origin (the parked open
  contract below), Nikulin glue machinery (cited; verified explicitly at rank 8),
  minimality (COMP.01 principle class), and the ADE scope (inherited from v299's
  ρ ≤ 2 growth universe). **P2 is NOT closed.**

Result (2026-07-10): **CONTRACT HOLDS, 7/7 PASS** (`glue02_octave_results.json`).
Chain now: clock (order 4) ⇒ glue = μ4 ⇒ spinorial ⇒ A3⊕D5 ⇒ octave (theorem) ⇒ E8
(explicit 240 roots). Never a scorecard row; never `[E]`-as-physics.

```bash
cd experiments/theory-contracts && python3 glue02_octave_derivation.py
```

## Open next contract — raw RP seam → Z4 mark-local source

`qgeo_dtn_mark_locality.py` proves the mark-local structure **given** the Z4 marking. The
deeper, still-open theory contract is the *origin* of the marking:

> **Why does the raw RP (reflection-positive) seam produce exactly a `Z4` (`jπ/2`)
> mark-local source — and not `Z3`, not generic marks?**

This is not an empirical test; it is the foundational step that would turn the mark-locality
contract from "consistent if Z4" into "Z4 is forced". It belongs in `tfpt_research_contracts`
(theory contracts), never in `evidence_scorecard.json`. Parked here as the next contract to
formalise.
