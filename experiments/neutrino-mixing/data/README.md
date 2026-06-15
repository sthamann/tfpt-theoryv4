# Data — neutrino / CKM mixing

`data/` is **gitignored** (`data/*`); only this `README.md` and the hand-authored
`measurements.json` are tracked. No downloaded blobs — `measurements.json` holds
published global-fit *summary values*, so the experiment is reproducible from this file.

## `measurements.json` — published comparison values

| observable | value | source / where to get it |
|---|---|---|
| `sin²θ12` | 0.307 ± 0.012 | NuFIT 6.0, www.nu-fit.org (Esteban+ 2024) |
| `sin²θ12` | 0.3092 ± 0.0087 | JUNO first run (2025), 59.1 d |
| `sin²θ13` | 0.02195 ± 0.00058 | NuFIT 6.0 (Daya Bay-dominated) |
| `sin²θ23` | 0.470 ± 0.017 | NuFIT 6.0 (NO, lower octant; upper-octant ~0.56) |
| `δ_CKM` (γ) | 64.6° ± 2.8 | LHCb γ combination (2024); δ_CKM = π/3+3λ² = 68.65° (canonical v88) |

Confirmed on 2026-06-15. TFPT values (`1/3−φ₀/2`, `φ₀ e^{−5/6}`, `1/2`, `π/3+3λ²`) are in
`src/tfpt_neutrino/constants.py`.
