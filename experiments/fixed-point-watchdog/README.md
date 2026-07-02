# fixed-point-watchdog — TFPT exact fixed points: zero-drift kill tests

**Status: armed, not triggered — A `tension`, B `consistent`, C `consistent` (2026-07-02).**

TFPT predicts several observables as **exact fixed points**. They are not fit parameters:
any confirmed deviation kills the corresponding branch (or, for the compiler outputs, the
theory). The five fixed points under watch:

1. `w = −1` exactly — dark energy is a true cosmological constant (Λ/H₀ engine).
2. `Σm_ν = 0.0588 eV` — the normal-ordering floor `m₃(1+√|J|)`, `m₁ ≈ 0` (ledger v272/v468).
3. `α⁻¹ = 137.0359992168`, **constant in time** (`α̇/α = 0`; v3).
4. Koide `Q = 2/3` exactly, from the charged-lepton pole masses.
5. The **α–Λ lock**: `ρ_Λ/M̄_Pl⁴ = (3/4π²)·e^(−2α⁻¹)` (v60/v274), which locks the drifts:
   `d ln ρ_Λ/dt = 2α⁻¹·(α̇/α)` — a fractional α drift is amplified by `2α⁻¹ ≈ 274.07` in Λ.

## Three test axes (all from public published values)

### A. Σm_ν × w pincer — verdict `tension`

DESI DR2 + CMB squeeze the joint TFPT point `(w=−1, Σm_ν=0.0588 eV)` from both sides,
and the squeeze is **model-dependent** — so both readings are computed:

- **ΛCDM reading** (`w=−1` held, as TFPT demands): the effective-mass posterior
  `Σm_ν,eff = −0.101 +0.047/−0.056 eV` puts the TFPT floor at **+3.1σ** (the paper's own
  number vs the 0.059 eV oscillation floor: 3.0σ). The floor still sits *inside* the
  standard 95% bound (0.0588 < 0.0642 eV) but *outside* the boundary-corrected
  Feldman–Cousins bound (0.053 eV).
- **w0waCDM reading**: the ν bound relaxes to 0.163 eV and the effective-mass posterior
  peaks at 0 — the TFPT floor is fully compatible (**+0.65σ**). But then `(w0,wa)=(−1,0)`
  itself is disfavoured at **3.1–4.4σ** (2-D Gaussian distance 3.07/3.87/4.37σ; published
  2.8/3.8/4.2σ per SN sample — validates the inputs). Joint (3 dof) ≈ **3.7σ** equivalent.

The pincer: **no published model reading lets both fixed points sit below ~3σ at once.**
Honest caveats: Gaussian approximations of published posteriors; Σm_ν bounds are
model-dependent; the three SN compilations overlap and are never stacked (same rule as
`dark-energy-w-watchdog`).

### B. α–Λ lock — verdict `consistent` (and a built-in mutual exclusion)

- PTB Yb⁺ E3/E2 optical clocks: `α̇/α = 1.8(2.5)×10⁻¹⁹/yr` (Filzinger et al., PRL 130,
  253001 (2023) — still the strictest published limit). Consistent with zero, exactly as
  TFPT demands.
- Through the lock, this bounds `|d ln ρ_Λ/dt| < ~1.4×10⁻¹⁶/yr` (2σ).
- If the DESI DR2 `(w0,wa)` preference were **real** dark-energy dynamics, the implied
  drift today is `|d ln ρ_DE/dt| = 3|1+w0|·H₀ ≈ 3.4–6.9×10⁻¹¹/yr` — via the lock that
  would require `α̇/α ≈ 1.2–2.5×10⁻¹³/yr`, violating the clock bound by a factor
  **~2.4–5.0×10⁵ (~5.7 orders of magnitude)**.

So the lock makes "TFPT + real w(z) evolution" **internally impossible**: TFPT stands or
falls with the joint point (`w=−1` *and* `α` static). If the DESI evolution is ever
confirmed as real DE dynamics, axis B kills the lock immediately — no new experiment
needed beyond the clocks we already have.

### C. Koide-τ kill window — verdict `consistent`

- `Q = 0.666664463 ± 5.08×10⁻⁶` from CODATA-2022 `m_e`, `m_μ` + PDG 2024/2025
  `m_τ = 1776.93 ± 0.09 MeV` → pull **−0.43σ** vs 2/3 (σ_Q is entirely τ-dominated).
- `Q = 2/3` predicts `m_τ = 1776.9690 MeV` (±0.00004 from `m_e`, `m_μ`).
- PDG 2024/2025 central: −0.43σ; Belle II 2023 (1777.09 ± 0.14): +0.86σ. Both consistent.
- **Kill window**: a 5σ kill needs `|m_τ − 1776.9690| ≥ 5σ(m_τ)`. At the current PDG
  central (gap 0.039 MeV) that means `σ(m_τ) < 0.008 MeV`; at the Belle II central
  (gap 0.121 MeV), `σ(m_τ) < 0.024 MeV`. Belle II's full dataset targets
  O(0.01–0.05) MeV — the window is live this decade.

## Run

```bash
. experiments/tfpt-discovery/.venv/bin/activate
cd experiments/fixed-point-watchdog && PYTHONPATH=src python -m tfpt_fixedpoint.cli analyze
```

Deterministic; writes `results/results.json`.

## Data sources (`data/measurements.json`, retrieved 2026-07-02)

- **DESI DR2 neutrino constraints**: Elbers et al., arXiv:2503.14744 (2025) — ΛCDM
  `Σm_ν < 0.0642 eV` (95%), Feldman–Cousins `< 0.053 eV`, effective-mass posterior
  `−0.101 +0.047/−0.056 eV`; w0waCDM `< 0.163 eV`, eff. posterior `0.000 +0.10/−0.081 eV`.
- **DESI DR2 CPL fits**: DESI DR2 Results II, arXiv:2503.14738 (2025) — same `(w0,wa)`
  values as `experiments/dark-energy-w-watchdog` (2.8/3.8/4.2σ per SN sample).
- **α-drift clock limit**: Filzinger et al., PRL 130, 253001 (2023), arXiv:2301.03433.
- **Lepton masses**: CODATA 2022 (`m_e`, `m_μ`); PDG 2024 + 2025 update
  (`m_τ = 1776.93 ± 0.09 MeV`, S. Navas et al., PRD 110, 030001); Belle II
  arXiv:2305.19116 (`1777.09 ± 0.08 ± 0.11 MeV`).

## Verdict enums and kill rules

Per axis: `consistent | tension | data_limited`. Frozen kill rules:

```
A: joint (w=-1, Sigma m_nu=0.0588 eV) excluded at >= 5 sigma under BOTH model readings
   (LCDM-nu AND w0waCDM) in a single systematics-controlled combination.
B: any confirmed alpha_dot/alpha != 0, or a confirmed Lambda drift violating
   d ln rho_Lambda/dt = 2 alpha^-1 d ln alpha/dt.
C: |m_tau - m_tau(Q=2/3)| >= 5 sigma(m_tau), systematics-controlled.
```

## Firewall

Standalone watchdog — a search surface, **not** a load-bearing claim. Not in the
verification suite, ledger, or website. The fixed points under test are TFPT compiler
outputs / branch readouts (`w=−1` and the lock are the cosmology branch; `Σm_ν` is the
seesaw NO floor; Koide `Q=2/3` is an `F_transfer` frontier bridge — never a primitive
compiler output). A `tension` verdict here upgrades nothing; a triggered kill would be
reported honestly and routed to the ledger by the parent, not by this experiment.
