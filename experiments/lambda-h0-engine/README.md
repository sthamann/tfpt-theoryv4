# TFPT Λ/H₀ engine — one `α⁻¹` for dark energy and the Hubble scale

Origin-story claim ("Λ dissolves"): the smallness of the cosmological constant is the
**same EM fixed point** `α⁻¹` that fixes `α`, not a fine-tuning:

```
ρ_Λ / M_pl⁴  = (3/256π⁴) e^(−2α⁻¹)   → 122.95 orders (unreduced)
ρ_Λ / M̄_pl⁴  = (3/4π²)   e^(−2α⁻¹)   → 120.15 orders (reduced)
S_dS · ρ_Λ   = 1/(128 c₃⁴) = 32π⁴     (exact dimensionless identity)
H₀ / M̄_pl   ~ e^(−α⁻¹)/(2π)          (H₀ ~ √Λ — one engine)
```

## Result (measured cosmology: Planck Ω_Λ, H₀)

| quantity | TFPT | measured | dev |
|---|---|---|---|
| ρ_Λ/M_pl⁴ (orders) | 122.95 | ~122.9 | ~0.0 |
| ρ_Λ/M̄_pl⁴ (orders) | 120.15 | ~120.1 | ~0.0 |
| `S_dS·ρ_Λ` | 32π⁴ (exact) | — | identity |
| H₀/M̄_pl (log₁₀) | −60.3 | −60.2 | ~0.1 dex |

→ **consistency**: the EM fixed point reproduces the measured Λ hierarchy to ~0.01
orders and `H₀/M̄_pl` to ~0.1 dex; `S_dS·ρ_Λ = 32π⁴` is an exact dimensionless identity.
One engine for Λ, S_dS and H₀ — a **consistency**, not a parameter-free derivation of the
absolute scale (that is the one irreducible anchor).

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .
tfpt-lambda analyze    # or: PYTHONPATH=src python -m tfpt_lambda.cli analyze
```
