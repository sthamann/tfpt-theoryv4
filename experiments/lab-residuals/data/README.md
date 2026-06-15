# Data — lab Ftransfer residuals

Published summary values transcribed from the cited sources (confirmed against the
live FNAL / NA62 / Theory-Initiative pages on 2026-06-15). `measurements.json` is the
single source.

## Muon g−2 (units of 1e-11)
| quantity | value ± σ | reference |
|---|---|---|
| aµ(exp), world avg | 116592071.5 ± 14.5 | Fermilab final, PRL 135 101802 (2025), 124 ppb |
| aµ(SM), data-driven HVP | 116591810 ± 43 | Theory Initiative White Paper 2020 |
| aµ(SM), lattice HVP | 116592033 ± 63 | Theory Initiative update 2025, arXiv:2505.21476 |

The two SM rows differ because the hadronic-vacuum-polarisation (HVP) is contested
(data-driven e⁺e⁻ vs lattice). The TFPT seam-vertex value `Δaµ = 45/(2¹⁹π⁹)` is
confronted with `aµ(exp) − aµ(SM)` under **both** choices.

## Rare kaons
| decay | value | reference |
|---|---|---|
| BR(K⁺→π⁺νν) | (9.6 ⁺¹·⁹₋₁.₈)×10⁻¹¹ | NA62 2016–2024, arXiv:2604.12649 (La Thuile 2026) |
| BR(K⁺→π⁺νν) | (13.0 ⁺³·³₋₃.₀)×10⁻¹¹ | NA62 2016–2022, JHEP 02 (2025) 191 |
| BR(KL→π⁰νν) | < 2.2×10⁻⁹ (90% CL) | KOTO 2024 upper limit |

## Axion haloscope coverage
Marker `m_a = 23.8 µeV ≈ 5.76 GHz` (determinant-line branch, `f_a = M_scal/128`).
ADMX (DFSZ, ≤4.2 µeV), HAYSTAC (~16–23 µeV, ~2× KSVZ), CAPP (10–30 µeV patches). The
marker is inside the HAYSTAC/CAPP band but **not yet excluded at DFSZ** and no excess
is reported there → data-limited.
