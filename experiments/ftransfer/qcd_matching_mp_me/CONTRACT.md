# F_QCD — QCD matching → m_p/m_e

**source inputs** — `α_s(M_Z)`, the carrier-output one-loop QCD coefficient `b₃ = 11 − ⅔N_f = 7`
(`b₃ = −7` for the β-function sign convention; suite `v159`/`v164`/`v172`), the quark masses and EW
thresholds, and the closed electron mass on the φ₀-ladder.

**scheme** — `MS̄` running of `α_s` from `M_Z` down through the flavour thresholds to the confinement scale;
non-perturbative proton mass from lattice QCD / chiral perturbation theory (the O(1) factor is *not*
algebraic).

**transfer** — `F_QCD : (α_s(M_Z), b₃, m_q, thresholds) ↦ m_p`, then
`m_p/m_e = F_QCD(...) / [ (π/√2)(16/7)(φ₀)⁵ v_geo ]`, with `Λ_QCD/v_geo = F_RG(α_s, b₃, thresholds)`.

**observables** — `m_p/m_e` (= 1836.15, **explicitly not claimed** as a compiler power).

**kill condition** — none at the compiler level: `m_p/m_e` is a QCD matching contract, falsifiable only
through the standard-physics transfer (lattice `C_p`), never as a TFPT integer formula. The rejected
near-`1836` formula (SU(9) absent from the `D₅⊕A₃` carrier) is the firewall working.

**status** — `[O]` QCD matching contract. `b₃ = −7` is a clean carrier output (`[E]`); `m_p` is QCD binding
energy (`[O]`). Romance with a 1836 formula is a warning sign, not a result.
