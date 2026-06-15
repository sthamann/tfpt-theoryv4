# Data — CMB inflation / scalaron

The `data/` directory is **gitignored** (`data/*`); only this `README.md` and the
hand-authored `measurements.json` are tracked. There are **no downloaded blobs** here —
`measurements.json` holds published *summary values* transcribed from the cited sources,
so the experiment is fully reproducible from this file.

## `measurements.json` — published comparison values

| key | value | source / where to get it |
|---|---|---|
| `n_s` (Planck 2018) | 0.9649 ± 0.0042 | Planck 2018 VI, A&A 641 A6 |
| `n_s` (P-ACT-LB + DESI) | 0.9743 ± 0.0034 | ACT DR6 + DESI BAO combined (2025) |
| `r` (BICEP/Keck BK18) | < 0.036 (95% CL) | BICEP/Keck 2021, PRL 127 151301 |
| `r` (CMB-S4 forecast) | σ_r ≈ 5×10⁻⁴ | CMB-S4 science book (forecast) |
| `A_s` (Planck 2018) | 2.10×10⁻⁹ ± 0.03 | Planck 2018 VI; ln(10¹⁰A_s)=3.044 |

Confirmed against the live sources on 2026-06-15. TFPT predictions (`n_s`, `r`, `A_s`)
are computed in `src/tfpt_inflation/constants.py` from `c₃` (no measured input enters
the prediction layer).
