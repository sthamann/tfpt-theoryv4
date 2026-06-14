# F_transfer — the four continuous-transfer pipelines

> **Scope:** this folder is a *workshop* (`experiments/`, not the verification suite,
> not the ledger, not the website). It turns the four frontier interfaces from a
> list into four explicit, runnable computation pipelines. **No new compiler
> identities** are created here — only standard QFT/cosmology transport from TFPT
> *source* data to *observables*, each with an explicit kill condition.

TFPT closes the **dimensionless compiler** and the **admissible QFT sector**. The
four quantities below are **not** compiler powers; they are one missing functor

```
F_transfer = F_observable ∘ F_threshold ∘ F_RG
```

with four interfaces. Each must stay `[C]`/`[O]` — exact algebraic *sub-parts* may
be `[E]` (e.g. the Koide 53/54 factor, `b₃=−7`), but the **physical observable**
never is. The ledger guard `v187` and the prose guard `v188` enforce this.

| Pipeline | Source (TFPT) | Transfer | Observable | Suite ref | Status |
|---|---|---|---|---|---|
| `koide_source_to_pole/` | `Q_src = 0.664`, the `53/54` operator factor | QED+EW threshold running (source → pole) | `Q_pole → 2/3` | `v183` | `[E]` factor · `[C]` pole transfer |
| `leptogenesis_boltzmann/` | normal-ordered ν spectrum, `δ_CP = 4π/3`, `m̃₁ = m₃/A_Λ` | thermal/density-matrix Boltzmann | `η_B` strip | `v169`/`v184` | `[C]` (one scenario input `M_R`) |
| `axion_relic/` | `f_a = M_scal/128`, `m_a ≈ 23.8 µeV`, `θ_i ≈ 170.4°`, `N_DW=1` | misalignment + string relic integral | `Ω_a h²` + kill window | `v25`/`v185` | `[C]` (hilltop-sensitive scenario) |
| `qcd_matching_mp_me/` | `α_s(M_Z)`, `b₃=−7`, quark masses, thresholds | RG → `Λ_QCD` + lattice/χPT matching | `m_p/m_e` | `v164` | `[O]` (QCD matching contract) |

## The contract each pipeline must state (see each `CONTRACT.md`)

```
source inputs   — the TFPT-side numbers (and their suite citation)
scheme          — renormalisation / matching scheme, scales, thresholds
transfer        — the standard-physics map actually computed (no TFPT magic)
observables     — what comes out, with units
kill condition  — what measurement would falsify THIS branch (not the theory)
status          — [E] sub-parts / [C] / [O], never silently promoted
```

## Firewall (do not violate)

- No refitted exponents; no new small integers without an admissible invariant class.
- Every RG scale carries a scale tag; every cosmology number a transfer tag.
- A frontier value is **never** rendered as a primitive compiler prediction.
- A negative result kills the *branch* (e.g. the leptogenesis window, or the
  determinant-line axion), **not** the compiler core.
