# F_pole — Koide source → pole

**source inputs** — the lepton φ₀-ladder source quotient `Q_src = 0.66446…` (0.33 % below 2/3);
the exact operator factor `u_pole/u_src = aᵀ(R+Q)𝟙/(2·𝟙ᵀRa) = 53/54` (the missing Sheet-Diamond
corner `F=R+Q`, `det B_F = 52 = dim F₄`; suite `v183`, `[E]`).

**scheme** — on-shell (pole) masses vs the TFPT source scale `μ_K`; QED + electroweak threshold
corrections between them.

**transfer** — `F_pole : Q_src ↦ Q_pole = F_QED/EW(Q_src)`. Compute the running of the three charged-lepton
masses from `μ_K` to their poles (QED self-energy + EW thresholds) and re-evaluate the Koide quotient.
This is the only missing step; the `53/54` factor is already exact.

**observables** — `Q_pole` (target `2/3 = |ℤ₂|/N_fam`).

**kill condition** — if a correct on-shell transfer moves `Q_pole` *away* from `2/3` (beyond the measured
`m_τ` precision, σ(m_τ)~0.01 MeV), the source→pole reading fails — the Koide *interpretation* falls, not the
compiler.

**status** — `[E]` for the `53/54` operator factor; `[C]` for the pole-transfer interpretation. Never quote
"Koide exact at the pole" as a compiler output.

**computed (`fpole_solver.py`, 2026-06-15)** — a clean negative that SHARPENS the interpretation: standard
QED/EW running is *excluded* as the transfer. Leptons all have `|charge|=1`, so the QED mass anomalous
dimension is flavour-universal and the high-scale ratios freeze to `m_i/m_j = (M_i/M_j)^{1+ε}` with
`ε=(3/2)(α/π) ≈ +0.0035`. That drives the hierarchy *wider*, pushing `Q` *above* `2/3` (`Q(ε_QED) ≈ 0.6678`),
whereas the φ₀-ladder source sits *below* (`Q_src = 0.66446`, needing `ε ≈ −0.0067`, the wrong sign). So
`F_pole(Koide)` is NOT perturbative running — it confirms `v93`'s honest negative (a continuous non-QED
generator: the `v82` Möbius flow with multiplier `(2/3)^6`, flow time ≈ 2.84), with `53/54` (`v183`, `[E]`)
its structural signature. The missing object is the operator/Möbius transfer generator, not a threshold
computation.
