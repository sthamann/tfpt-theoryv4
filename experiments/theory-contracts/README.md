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

## Open next contract — raw RP seam → Z4 mark-local source

`qgeo_dtn_mark_locality.py` proves the mark-local structure **given** the Z4 marking. The
deeper, still-open theory contract is the *origin* of the marking:

> **Why does the raw RP (reflection-positive) seam produce exactly a `Z4` (`jπ/2`)
> mark-local source — and not `Z3`, not generic marks?**

This is not an empirical test; it is the foundational step that would turn the mark-locality
contract from "consistent if Z4" into "Z4 is forced". It belongs in `tfpt_research_contracts`
(theory contracts), never in `evidence_scorecard.json`. Parked here as the next contract to
formalise.
