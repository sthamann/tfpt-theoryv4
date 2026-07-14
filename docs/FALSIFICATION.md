# How to falsify TFPT

> A theory that cannot be killed is not a theory. TFPT freezes its dimensionless predictions
> **before** the data ([`verification/predictions_frozen.json`](../verification/predictions_frozen.json),
> frozen 2026-06-09) and locks each one to its formula on every run
> ([`v84_frozen_registry.py`](../verification/v84_frozen_registry.py)). A live
> scorecard against JUNO / NuFIT / ACT / BK18 is on the
> [website](https://www.fixpoint-theory.com/falsification).

## The sharp kill tests

These are single numbers with no adjustable dial behind them. A confirmed measurement outside the
stated window falsifies the corresponding claim.

| Observable | TFPT frozen value | Falsified if… | Decided by |
|---|---|---|---|
| Leptonic CP phase | `δ_PMNS = δ_CKM,lead + π = 240°` (Galois-locked, `v320`) | measured `δ_CP` far from `240°` | DUNE, Hyper-Kamiokande |
| Cosmic birefringence | `β = φ₀/(4π) ≈ 0.2424°` | isotropic `β` inconsistent with `0.2424°` | CMB polarimetry (ACT, SO, LiteBIRD) |
| Reactor mixing angle | `sin²θ₁₃ = 0.02311` | precise `θ₁₃` off the band | JUNO |
| Solar mixing angle | `sin²θ₁₂ = 1/3 − φ₀/2 = 0.306747` | precise `θ₁₂` off the seed value | JUNO |
| Scalar tilt / tensor ratio | `n_s ∈ [0.960, 0.967]`, `r ∈ [0.0033, 0.0048]` | outside the `N_star` band | CMB-S4, LiteBIRD |
| Fine-structure constant | `α⁻¹ = 137.0359992` (1.9σ from CODATA-2022) | a shift of the CODATA value away from it | atom-interferometry / QED |
| Entropic `R²` coefficient | Bianconi entropic action misses TFPT Starobinsky by exactly `3(8π)⁹` (`v473`) | that gap fails to hold | pre-registered theory kill test |

Additional frozen numbers of record (all in the registry): `Ω_b ≈ 0.04894`, the Cabibbo angle
`λ_C ≈ 0.22438`, the CKM entries `s₁₃ ≈ 0.003765`, `s₂₃ ≈ 0.04343`, `δ_CKM ≈ 68.66°`, the charged
mass ratios (`m_μ/m_τ ≈ 0.06077`, `m_e/m_μ ≈ 0.004847`), quark ratios (`m_u/m_d ≈ 0.4701`,
`m_c/m_s ≈ 13.60`, `m_t/m_b ≈ 40.81`), the Starobinsky scalaron mass `M_scal ≈ 3.06×10¹³ GeV`, and
the dark-energy density `ρ_Λ/M̄⁴ ≈ 7.1×10⁻¹²¹`.

**Currently in tension (honestly recorded):** `sin²θ₁₃` sits at ~2.0σ on the live scorecard. Two
named post-hoc `[O]` candidates sit next to it in the ledger — `FLAV.THIRDGEN.PATTERN.01` (`v467`,
the three ~2σ mixing tensions as one `−φ₀` third-generation pattern) and `FLAV.DM2RATIO.01`
(`v468`, the splitting ratio `= |J_PMNS|` at −0.19σ). The record is unchanged; JUNO / Belle II
decide.

## Not numerology — the null model

<p align="center">
  <img src="../assets/readme/05_nullmodel.png" alt="Frozen predictions vs a null model of 200,000 random look-alikes" width="820"><br>
  <sub><em>13 predictions were frozen <b>before</b> the data; 200,000 random look-alikes score at most 5/13, while TFPT hits 13/13 — a look-elsewhere-corrected chance below 1 in 10³⁰.</em></sub>
</p>

The Monte-Carlo null model (`v100_numerology_null_mc.py`) quantifies the retrospective
look-elsewhere burden; the frozen registry (`v84`) prevents future look-elsewhere drift. Together
they answer the "you just fit numbers" objection with a number.

## What a successful attack looks like

The most valuable contributions, in order of impact:

1. **Reproduce or falsify a frozen prediction** — a measurement outside a stated window.
2. **Find a circular dependency** — a "derived" quantity that secretly used its own target.
3. **Identify an unstated physical assumption** doing load-bearing work.
4. **Challenge a claimed uniqueness result** (e.g. the `E8` glue, the `α⁻¹` root).
5. **Close or kill one of the three open interfaces** (`v_geo`, `SEAM.EQUIV.01`, `F_transfer`).

Open a [claim challenge, reproduction failure, or counterexample issue](../README.md#try-to-break-tfpt).
Every kill test also lives, per-observable, on the website
[falsification page](https://www.fixpoint-theory.com/falsification).
