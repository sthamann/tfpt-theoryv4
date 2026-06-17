# Data — CCBH dark-energy leg

`data/` is **gitignored** (`data/*`); only this `README.md` and the hand-authored
`measurements.json` are tracked. No downloaded blobs — reproducible from `measurements.json`.

## `measurements.json`

- **Coupling index `k`** — Farrah et al. 2023, ApJL 944 L31, "Observational Evidence for
  Cosmological Coupling of Black Holes and its Implications for an Astrophysical Source of
  Dark Energy": combined `k = 3.11 +0.80/−0.79` from the redshift growth of SMBH mass at
  fixed stellar mass in five samples of passively-evolving elliptical galaxies.
- **Density closure** — the local SMBH realization mass density, grown via `k=3` from
  `z≈7`, can source `Ω_de ≈ 0.68` (Farrah+2023). Confronted with Planck 2018
  `Ω_Λ = 0.6889 ± 0.0056`. **Model-dependent and contested** — reported as an order-level
  consistency leg only.

## Contestation (baked into the verdict)

The CCBH-as-dark-energy claim is **not settled**: Lacy+2024, Amendola+2023,
Andrae & El-Badry 2023 and Mistele 2023 dispute the required mass growth, the
background-cosmology viability of `k=3` as *all* of dark energy, and the coupling
derivation. The runner therefore types this as a **downstream bridge / `data_limited`**,
never a confirmation.
