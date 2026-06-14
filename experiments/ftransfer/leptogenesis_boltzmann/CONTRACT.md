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
