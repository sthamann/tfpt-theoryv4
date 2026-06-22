/**
 * Hostile-referee FAQ data. Kept in a plain (non-"use client") module so both
 * the client UI component and the server page (for FAQPage JSON-LD) can import
 * the actual array rather than a client reference.
 */
export interface FaqItem {
  q: string;
  /** Plain-text answer (also used to build FAQPage JSON-LD). */
  a: string;
}

export const FAQ_ITEMS: FaqItem[] = [
  {
    q: "Is this just E₈ unification again?",
    a: "No. In TFPT, E₈ is the unimodular audit / compiler hull that classifies the admissible discrete charge and residue structures — not an unbroken physical gauge group. The Standard Model is a readout after projection, not an E₈ gauge theory. This is exactly why the no-go results against literal E₈ world-formulas (Distler–Garibaldi; Coleman–Mandula) do not apply: they constrain E₈ as a spacetime gauge symmetry, which TFPT does not claim.",
  },
  {
    q: "Where does experimental input enter?",
    a: "Into the comparison rows, not the construction. CODATA-2022, NuFIT 6.0, ACT DR6, Planck and the running/upcoming experiments are how the closed-branch readouts are checked — they are never used as inputs. The closed branch is built only from the two axioms c₃ = 1/(8π) and g_car = 5.",
  },
  {
    q: "What is actually fitted?",
    a: "In the closed branch: nothing. There are zero fitted constants on the dimensionless axis, and parameter-freeness is a theorem under the named gapped-transport hypotheses (Δ = 6 log(3/2) > 0 gives, by Perron–Frobenius, a unique attractor; the physical identification of the transport operator stays [C]). The only continuous primitive left is π. The conditional layer has declared inputs — the e-fold count N★ for inflation (kept as the frozen band [50,60]; the scalaron-reheating chain computes a conditional point N★ = 51.4 [C], recorded with its A_s tension) and one dimensionful induced-gravity scale — which are typed [C]/[O], never smuggled in.",
  },
  {
    q: "Couldn't all the integer coincidences be numerology?",
    a: "The discipline rule is: every load-bearing number must appear in at least one E₈ branching projection, which turns the number stock into a falsifiable raster. Beyond that, every [E] identity, [E] lattice theorem and [E] numerical fixed point is re-derived from the two axioms by an independent Python suite, mirrored on an independent Wolfram path, and recorded in a versioned status ledger. Since v100 the charge is also quantified by an explicit null model: exhaustively enumerating a declared formula grammar (which provably contains every scored TFPT formula) against conservative data windows gives a joint look-elsewhere-corrected probability ≤ 10⁻³⁰·⁷ that a random theory of equal formula complexity reproduces the scorecard — including the α⁻¹ equation, where exactly one of 94 500 complexity-matched variants hits CODATA. Honestly stated: that is a null-model rejection conditional on the declared grammar, not a certificate — and the test has demonstrated power (perturbing φ₀ by 1% collapses the scorecard).",
  },
  {
    q: "What would kill the theory fastest?",
    a: "Any one of: the α fixed-point equation F_U(1)(α) = 0 failing or admitting a second admissible root; a robust neutron-EDM signal (θ_eff = 0 is structural); the discovery of a second light seam-even Higgs doublet (N_Φ = 1); a robust tensor ratio r ≳ 0.01 (the R² branch carries M_Pl and A_s); a robust w ≠ −1 (the single-engine dark-energy readout); a JUNO solar angle clearly away from 0.307; or any verification script failing to reproduce its claim.",
  },
  {
    q: "What is still open?",
    a: "The live residual is three named interfaces — Rest = v_geo ⊕ G_net ⊕ F_transfer. (1) v_geo: the single dimensionful scale anchor — the quark ratios are closed, only the absolute amplitude remains, and the No-Unit theorem makes it an irreducible metrology primitive (the same unit as gravity's 1/G), over-determined to 0.11% by gravity vs dark energy. (2) G_net: the metric-sector inclusion. Its target (E₈)₁ net is closed — net existence and full-cone reflection positivity are discharged to [E] — so the only open part is one named theorem, the Seam Equivalence Theorem SEAM.EQUIV.01: 'the raw reflection-positive seam state is the holomorphic (E₈)₁ net at τ=i'. The conformal-deck premise QGEO.SYM.01 (the carrier μ₄ clock is the seam's deck) is now its corollary — a conformal net's vacuum is rotation-invariant by axiom, so it follows from SEAM.EQUIV.01 with no extra premise (v335, Lean-pinned). SEAM.EQUIV.01 stays [O] (not machine-proved end-to-end), but its entire residual is now a composition of standard cited theorems (Osterwalder–Schrader/quasi-free clustering, the Kitaev free-fermion classification, an AQFT stack) over established TFPT facts — Lean-pinned (FORM.SEAMEQUIV.01) to exactly those named steps plus the derived Recovery gap Δ = 6·ln(3/2) > 0 — with no undischarged TFPT-internal assumption left. It is by design TFPT's one irreducible structural postulate, the role 'c = const' plays in relativity. (3) F_transfer: the source→pole/relic/cosmology transport (Koide, η_B, the axion relic scale, m_p/m_e are four instances of one typed functor, explicitly not claimed as compiler powers). Structurally these collapse to a single condition — 'the seam carries no nontrivial abelian sector' — with three provably-equivalent faces (holomorphy, a homology-sphere seam link ⟺ 2I, one 1-dim irrep) that all force E₈; in Chern–Simons language it is the single integer step det K = 1, and the whole boundary QFT is one relative object (the Modular Spectral Closure) closed modulo SEAM.EQUIV.01. Separately, the nonperturbative ambient/metric-sector measure QG.AMB.01 (full quantum gravity; its R²/Weyl² sector carries the non-unitary Stelle ghost) is NOT a second TFPT structural item: it is the general Euclidean-QG conformal-factor problem (Gibbons–Hawking–Perry 1978), from which TFPT is rigorously gap-decoupled (Δ_eff = 1.648 > 0) — an inherited, decoupled problem and a strict-TOE completion target, not a TFPT hole (v335). The full sprint-by-sprint reduction that pinned SEAM.EQUIV.01 lives on the /changelog page, not here. The historical labels U_wall / G_metric / F_frontier are kept only for ledger continuity.",
  },
  {
    q: "Why call α⁻¹ a prediction at 1.9σ from CODATA?",
    a: "α⁻¹ = 137.0359992168 is the unique positive root of a parameter-free cubic with proven existence and uniqueness — it is a fixed point, not a fit. The deviation from the CODATA-2022 recommended value is 3.98×10⁻⁸ in α⁻¹, about 1.9σ of that adjustment's uncertainty. It is presented as a numerical fixed point [E], with its kill criterion stated.",
  },
];
