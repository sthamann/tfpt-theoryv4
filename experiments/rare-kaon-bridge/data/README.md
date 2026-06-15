# Data — rare-kaon flavour bridge

`data/` is **gitignored** (`data/*`); only this `README.md` and the hand-authored
`measurements.json` are tracked. Published summary values only.

## `measurements.json`

| quantity | value | source |
|---|---|---|
| BR(K⁺→π⁺νν) | (9.6 ⁺¹·⁹₋₁.₈)×10⁻¹¹ | NA62 2016–2024, arXiv:2604.12649 |
| BR(KL→π⁰νν) | < 2.2×10⁻⁹ (90% CL) | KOTO 2024/2025, PRL 134 081802 |
| BR(K⁺)ˢᴹ | (8.4 ± 1.0)×10⁻¹¹ | Buras et al. SM |
| BR(KL)ˢᴹ | (3.4 ± 0.6)×10⁻¹¹ | Buras et al. SM |
| γ (CKM angle) | 64.6° ± 2.8° | LHCb 2024 γ combination |
| Jarlskog J | (3.08 ± 0.13)×10⁻⁵ | PDG 2024 CKM fit |
| \|Vcb\|, \|Vub\| | 0.0409, 0.00369 | PDG 2024 (**external nuisances**) |
| Grossman-Nir | BR(KL) ≤ 4.3·BR(K⁺) | isospin bound |

Only `λ` (Cabibbo) and `δ_CKM` are TFPT-predicted; `|Vcb|`, `|Vub|` and the SM
short-distance functions are external nuisances — this is why the channel is a *downstream
bridge*, not a primitive compiler output. Confirmed 2026-06-15.
