# Data — proton-decay limits

`data/limits.json` holds **published summary values only**, with provenance. These are the
**only** empirical numbers on the data side; the TFPT side flows from the axioms via the RGE.
Anything large/raw would go under `data/raw/` (gitignored). Verified **2026-07-01**.

## `p → e⁺π⁰`

| role | value | experiment | source |
|---|---|---|---|
| current limit | τ > 2.4×10³⁴ yr (90% CL, 450 kton·yr) | Super-Kamiokande I–IV | Phys. Rev. D 102, 112011 (2020); arXiv:2010.16098 |
| future reach | ~6×10³⁴ yr @10 yr → ~1×10³⁵ @20 yr | Hyper-Kamiokande (~2027+) | arXiv:1805.04163; SciPost Phys. Proc. 17, 019; WIN2025 (Wilson) |
| future reach | ~1×10³⁴ yr (400 kton·yr) | DUNE | arXiv:2503.23291 |

## `p → ν̄K⁺`

| role | value | experiment | source |
|---|---|---|---|
| current limit | τ > 5.9×10³³ yr (90% CL, 260 kton·yr) | Super-Kamiokande | Phys. Rev. D 90, 072005 (2014) |
| current (prelim.) | τ > 8.2×10³³ yr (365 kton·yr, **unpublished**) | Super-K preliminary | GUTPC 2024 talk |
| future reach | ~2×10³⁴ yr @10 yr (~3×10³⁴ @20 yr) | Hyper-Kamiokande | arXiv:1805.04163; SciPost Phys. Proc. 17, 019 |
| future reach | ~1.3×10³⁴ yr (400 kton·yr) — **golden LArTPC mode** | DUNE | arXiv:2503.23291; ETH thesis 10.3929/ethz-b-000462924 |
| future reach | ~9.6×10³³ yr (200 kton·yr, ~10 yr) | JUNO | Chin. Phys. C 47, 113002 (2023); arXiv:1507.05613 |

Notes: the published Super-K `ν̄K⁺` limit (5.9×10³³ yr) is used as the current bound; the
365 kton·yr preliminary (8.2×10³³ yr) is recorded but not used. `K⁺` is below the water-Cherenkov
threshold, so Hyper-K tags it via decay products, while DUNE (LArTPC) and JUNO (scintillator)
image/tag it directly — hence `ν̄K⁺` is their golden channel. The hadronic-matrix-element factor
in `τ_p` and the `R_νK = Γ(ν̄K⁺)/Γ(e⁺π⁰)` branching are **external nuisances**, not TFPT inputs.
