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
    a: "The discipline rule is: every load-bearing number must appear in at least one E₈ branching projection, which turns the number stock into a falsifiable raster. Beyond that, every [E] identity, [E] lattice theorem and [E] numerical fixed point is re-derived from the two axioms by an independent Python suite, mirrored on an independent Wolfram path, and recorded in a versioned status ledger. Since v100 the charge is also quantified by an explicit null model: exhaustively enumerating a declared formula grammar (which provably contains every scored TFPT formula) against conservative data windows gives a joint look-elsewhere-corrected probability ≤ 10⁻³⁰·⁷ that a random theory of equal formula complexity reproduces the scorecard — including the α⁻¹ equation, where exactly one of 94 500 complexity-matched variants hits CODATA. Honestly stated: that is a null-model rejection conditional on the declared grammar, not a certificate — and the test has demonstrated power (perturbing φ₀ by 1% collapses the scorecard). Stripped of that grammar an assumption-minimal floor still remains: the same 94 500-variant α⁻¹ census is pure counting, so p ≤ 1/94 500 ≈ 4.40σ with no subjective probability at all (v436), and a monotone concession ladder (30.7 → 25.8 → 4.98 dex) keeps the 'not chance' verdict even at the most adversarial rung — the only honest gap to 5σ is one further independent confirmation.",
  },
  {
    q: "What would kill the theory fastest?",
    a: "Any one of: the α fixed-point equation F_U(1)(α) = 0 failing or admitting a second admissible root; a robust neutron-EDM signal (θ_eff = 0 is structural); the discovery of a second light seam-even Higgs doublet (N_Φ = 1); a robust tensor ratio r ≳ 0.01 (the R² branch carries M_Pl and A_s); a robust w ≠ −1 (the single-engine dark-energy readout); a JUNO solar angle clearly away from 0.307; or any verification script failing to reproduce its claim.",
  },
  {
    q: "What is still open?",
    a: "The live residual is three named interfaces — Rest = v_geo ⊕ G_net ⊕ F_transfer. (1) v_geo: the single dimensionful scale anchor — the quark ratios are closed, only the absolute amplitude remains, and the No-Unit theorem makes it an irreducible metrology primitive (the same unit as gravity's 1/G), over-determined to 0.11% by gravity vs dark energy. It stays the one genuine [O] unit. (2) G_net: the metric-sector inclusion. Its target (E₈)₁ net is closed — net existence and full-cone reflection positivity are discharged to [E] — and the keystone Seam Equivalence Theorem SEAM.EQUIV.01 ('the raw reflection-positive seam state is the holomorphic (E₈)₁ net at τ=i') is now [C] closed modulo cited theorems, not solved: an explicit gapped lattice model (v367/v368) and the S3 closure stack pin the target at every computable level — central charge c = 8 from the lattice (v376), the (E₈)₁ character 248/1 (v377), genus-1 torus GSD = 1 (v378) and reflection positivity (v379) — and the chain is Lean-pinned (FORM.SEAM.MMST.01, SeamScalingLimit.lean) to the published MMST/Adamo scaling-limit theorems. The only residual is [O] = the abstract continuum scaling-limit existence (v336), a cited published theorem outside the computational suite; its 128-spinor extension leg is certified at net level by the peer-reviewed crossed-product package (v469, Longo–Rehren/Böckenhauer/KLM; AGT/AMT an independent second witness), with the realisation input reduced to invariant level — stays [O]. Its conformal-deck face QGEO.SYM.01 is a corollary (v335). (3) F_transfer: the source→pole/relic/cosmology transport, now a typed RUNNABLE solver suite — Koide source→pole (v371), η_B via the Boltzmann washout (v372), the axion relic (v373) and m_p/m_e via QCD/EW matching (v374), each with a kill test and folded into a status-typed prediction-observatory CI (v375); they stay typed [C] bridges, never compiler powers. Separately, the nonperturbative ambient measure QG.AMB.01 (full quantum gravity) is NOT a second TFPT structural item: the ambient-redundancy theorem (v369) plus the S3 reflection-positivity closure (v379) discharge it as a redundancy — a certification object, not missing dynamics, conditional on SEAM.EQUIV.01 + Bisognano–Wichmann; every readout factors through the gapped admissible spectrum (Δ_eff = 1.648 > 0), so TFPT provably does not need it. Its R²/Weyl² Stelle ghost is a Seeley–DeWitt truncation artefact — perturbative spin-2 graviton unitarity is established [C] (v304/v370/v380), so it is not a non-unitarity hole either. The full sprint-by-sprint reduction that pinned SEAM.EQUIV.01 lives on the /changelog page, not here. The historical labels U_wall / G_metric / F_frontier are kept only for ledger continuity.",
  },
  {
    q: "Why call α⁻¹ a prediction at 1.9σ from CODATA?",
    a: "α⁻¹ = 137.0359992168 is the unique positive root of a parameter-free cubic with proven existence and uniqueness — it is a fixed point, not a fit. The deviation from the CODATA-2022 recommended value is 3.98×10⁻⁸ in α⁻¹, about 1.9σ of that adjustment's uncertainty. It is presented as a numerical fixed point [E], with its kill criterion stated.",
  },
];
