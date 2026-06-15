# F_Boltzmann — CP source → η_B

**source inputs** — TFPT's normal-ordered neutrino spectrum (`m₃ ≈ 0.05 eV`), the predicted
`δ_CP = 4π/3 = 240°`, and the plausible washout anchor `m̃₁ = m₃/A_Λ = m₃/10 ≈ 5 meV`
(A_Λ = 10 = |E(K₅)| atom; suite `v9`, `v169`, `v184`).

**scheme** — thermal flavoured leptogenesis; Davidson–Ibarra `ε₁ = (3/16π) M₁ m₃ / v²`; Buchmüller–Di Bari–
Plümacher efficiency `κ_f(m̃₁)`; sphaleron + photon normalisation `0.96×10⁻²`.

**transfer** — `F_Boltzmann : (m̃₁, δ_CP, M_R, T_RH) ↦ η_B`. Run the density-matrix Boltzmann network with
`m̃₁ = m₃/A_Λ` fixed; the heavy scale `M₁ = M_R φ₀⁴` carries **one** scenario input `M_R` (the seesaw scale
`~v²/m₃`, *not* a compiler power — `v184`).

**observables** — `η_B` (observed `6.1×10⁻¹⁰`), as a **strip** over the allowed `(M_R, T_RH)`, not a point
prediction.

**kill condition** — if the observed `η_B` lies **outside** `F_Boltzmann(TFPT strip)` after a proper solve,
the leptogenesis *branch* falls (the downstream `Ω_b` readout `FR.ETAB.01` is independent and already hit).

**status** — `[C]` with one scenario input (`M_R`). The washout is anchored; `M₁=M_R φ₀⁴` only *relocates*
the free scale. Never quote `η_B` as a compiler power.

**computed (`fboltzmann_strip.py`, 2026-06-15)** — turns `v184`'s single point into the honest strip: with the
anchored washout (`κ_f ≈ 0.073`) and the predicted `δ_CP=240°` (`|sin|=0.866`), `η_B^obs = 6.1×10⁻¹⁰` is
reproduced along an `M₁` strip from `≈8.8×10⁹ GeV` upward, i.e. `M_R ≳ 1.1×10¹⁵ GeV` — the lower edge sits
within a factor `~2` of the *natural* seesaw scale `v²/m₃ ≈ 6×10¹⁴ GeV`, so the required heavy scale is
physically reasonable, not tuned. The strip is bounded below (need `M₁` large enough) and above by
`T_RH > M₁` + perturbativity. Stays `[C]`: the washout is TFPT-anchored, but `M_R` is the one free dial
(`M₁=M_R φ₀⁴` relocates it; `M_R` is not a clean `Mbar` power).
