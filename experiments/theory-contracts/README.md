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

## Open next contract — raw RP seam → Z4 mark-local source

`qgeo_dtn_mark_locality.py` proves the mark-local structure **given** the Z4 marking. The
deeper, still-open theory contract is the *origin* of the marking:

> **Why does the raw RP (reflection-positive) seam produce exactly a `Z4` (`jπ/2`)
> mark-local source — and not `Z3`, not generic marks?**

This is not an empirical test; it is the foundational step that would turn the mark-locality
contract from "consistent if Z4" into "Z4 is forced". It belongs in `tfpt_research_contracts`
(theory contracts), never in `evidence_scorecard.json`. Parked here as the next contract to
formalise.
