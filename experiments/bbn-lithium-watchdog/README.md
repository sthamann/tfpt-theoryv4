# bbn-lithium-watchdog — the lithium-7 problem under the frozen TFPT η

**Status: `consistent` (watchdog armed) — D/H −0.3σ and Yp +0.5σ anchor the frozen η;
⁷Li is overpredicted ×3.36 (+9.9σ) = the known cosmological lithium problem, whose
resolution TFPT *requires* to be astrophysical (2026-07-03).**

> **Firewall:** standalone watchdog — a search surface, never a load-bearing claim.
> The `Ω_b` record is frozen elsewhere (v84, `[E]`); this experiment only confronts its
> BBN consequences. Nothing here upgrades any TFPT status.

## The open question (unresolved ~20 years)

Standard BBN at the CMB baryon density overpredicts primordial ⁷Li by a factor ~3
against the Spite plateau in metal-poor halo stars (Sbordone+2010: `Li/H = 1.58±0.31
×10⁻¹⁰`), while D/H (Cooke+2018) and Yp (Aver+2021) agree beautifully at the same η.
No accepted resolution exists: stellar depletion is favoured but not proven; the
nuclear-physics escape is measured away; exotic-BBN escapes (decaying particles,
varying constants) remain on the market.

## The TFPT reading (frozen η, no escape hatch)

TFPT fixes the baryon density with **no dial**: `Ω_b = φ₀(1−1/4π)` (frozen record v84)
+ `h = 0.6715` (flat budget closure) → `ω_b = 0.02207`, `η₁₀ = 6.04`. Rescaling the
PRIMAT reference abundances (Pitrou+2018) to the TFPT η via published local scalings:

| observable | predicted @ frozen η | observed | pull |
|---|---|---|---|
| D/H | `2.512±0.037 ×10⁻⁵` | `2.527±0.030 ×10⁻⁵` (Cooke+2018) | **−0.3σ** |
| Yp | `0.24696±0.00017` | `0.2453±0.0034` (Aver+2021) | **+0.5σ** |
| ⁷Li/H | `5.31±0.21 ×10⁻¹⁰` | `1.58±0.31 ×10⁻¹⁰` (Spite plateau) | **+9.9σ (×3.36)** |

Because η cannot move and the compiler leaves no slot for new BBN-era states (the same
no-slot counting as the sterile/X17/R_D axes), TFPT's **dated dissolution statement** is:

> the lithium problem resolves **astrophysically** (stellar depletion / turbulent
> mixing in halo stars) — never by shifting η, never by new BBN physics.

**Frozen kill rule:** an established resolution requiring η ≥5σ off the TFPT `ω_b`;
OR confirmed new BBN-era physics at ≥5σ; OR a D/H measurement pulling ≥5σ from the
frozen-η value.

## Run

```bash
. experiments/tfpt-discovery/.venv/bin/activate
cd experiments/bbn-lithium-watchdog && PYTHONPATH=src python -m tfpt_li7.cli analyze
```

Deterministic; published values only (`data/measurements.json`); writes
`results/results.json`.

## Method note

PRIMAT reference abundances at Planck `ω_b = 0.02236` are rescaled to the TFPT
`ω_b = 0.02207` (a −1.3% shift) with local power-law scalings (`⁷Li ∝ η^2.12`,
`D/H ∝ η^−1.6`, `Yp ∝ η^0.04`; Fields 2011). Over this range the scaling error is
negligible against the observational errors. The D/H and Yp legs overlap the existing
`cmb-birefringence-seed` BBN cross-check (`independence_group = phi0_seed` — never an
independent hit); the ⁷Li leg is the new confrontation.
