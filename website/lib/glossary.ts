/**
 * Inline glossary used by the GlossTerm component to surface short, one-line
 * definitions for the technical TFPT vocabulary on hover/focus/tap. Keep
 * each definition under ~280 characters so the tooltip stays scannable.
 */
export interface GlossaryEntry {
  term: string;
  alias?: string[];
  short: string;
}

export const GLOSSARY: GlossaryEntry[] = [
  {
    term: "seam",
    alias: ["the seam", "Σ", "boundary seam", "seam sphere"],
    short:
      "The abstract one-sided boundary sphere whose Gauss–Bonnet normaliser fixes c₃ = 1/(8π). Its local gravitational realisation is a horizon, but seam ≠ event horizon — that identification stays [C].",
  },
  {
    term: "seam constant",
    alias: ["c₃", "c3", "boundary number", "c_3"],
    short:
      "The first axiom P1: c₃ = 1/(8π). The boundary/seam normaliser, Gauss–Bonnet-hardenable as 1/(|ℤ₂|·∮ K). Drives the seed, α⁻¹ and the scale grammar.",
  },
  {
    term: "readout",
    alias: ["readouts", "read off", "reads off", "compiler output"],
    short:
      "An observable the compiler reads off E₈ after projection — a gauge charge, a mass-ladder rung, a mixing angle — rather than a separately-postulated quantity. Each readout carries a status grade ([E]/[C]/[O]).",
  },
  {
    term: "carrier",
    alias: ["g_car", "carrier rank", "g_{car}", "five-slot carrier", "3+2"],
    short:
      "The second axiom P2: a five-slot carrier g_car = 5 (3 colour + 2 weak). Its even-Hamming code is the D₅ half-spinor; the Pascal sum 1+5+10 = 16 forces g_car = 5.",
  },
  {
    term: "E8 compiler",
    alias: ["compiler", "audit hull", "E₈ compiler", "E8", "E₈"],
    short:
      "E₈ is the unimodular audit/compiler hull — not a physical gauge group. The Standard Model is a readout after projection; the no-go theorems against literal E₈ do not bite.",
  },
  {
    term: "μ₄ glue",
    alias: ["mu4 glue", "glue theorem", "mu_4 glue", "glue"],
    short:
      "D₅ and A₃ share the discriminant group ℤ₄; their glue norms q(D₅)+q(A₃) = 5/4+3/4 = 2 add to the E₈ root norm. Hence E₈ = (D₅ ⊕ A₃) + μ₄ closes as a lattice theorem.",
  },
  {
    term: "Coxeter compiler",
    alias: ["Z30", "Z₃₀", "Coxeter number", "30 = 2·3·5"],
    short:
      "The Coxeter number h(E₈) = 30 = 2·3·5 factorises into the three discrete atoms: sheet ℤ₂, families ℤ₃, and the carrier g_car = 5. rank E₈ = 8 = φ(30) is the live-phase count.",
  },
  {
    term: "seed",
    alias: ["φ₀", "phi_0", "phi0", "u = φ₀", "retained seed", "varphi_0"],
    short:
      "The bridge seed φ₀ = 1/(6π) + 3/(256π⁴). The carrier base λ_Y = √(φ₀(1−φ₀)) of the mass ladder; also gives sin²θ₁₃ = φ₀ e⁻⁵ᐟ⁶ and β_rad = φ₀/(4π).",
  },
  {
    term: "residue matrix",
    alias: ["R", "flavor residue matrix", "residue matrix R"],
    short:
      "The 3×3 compiler residue matrix R with det R = 8 = h(D₅), principal 2-minors (2,3,5), ‖R‖_F² = 78 = dim E₆, and χ_R = t³ − 9t² + 10t − 8. The flavor signature.",
  },
  {
    term: "word-length",
    alias: ["L matrix", "word-length matrix", "word lengths"],
    short:
      "The integer matrix L = R + 6·(winding) of transport word-lengths in the φ₀-ladder. Σ L = 40, and Σ L + N_Φ = 41 = 10 b₁ fixes the abelian coefficient.",
  },
  {
    term: "bootstrap loop",
    alias: ["bootstrap", "Möbius bootstrap", "self-consistency loop"],
    short:
      "The E₈ closure feeds back as an internal consistency check: g_car = 5 is forced three ways and the 8 in c₃ = rank E₈ = h(D₅) = φ(30) are recovered independently. The bootstrap overdetermines the discrete core; only π stays free.",
  },
  {
    term: "gapped attractor",
    alias: ["unique attractor", "Perron–Frobenius", "attractor"],
    short:
      "The boundary transport has spectral gap Δ = 6 log(3/2) > 0, so by Perron–Frobenius it has a unique attracting fixed point. The constants are selected, not tuned.",
  },
  {
    term: "anchor",
    alias: ["a = (1,1,2)", "parabolic anchor", "(1,1,2)"],
    short:
      "The single parabolic anchor a = (1,1,2). Its elementary symmetric polynomials are (4,5,2) = (|μ₄|, g_car, |ℤ₂|); its power sums generate 240 and 248. Inputs collapse to a plus π.",
  },
  {
    term: "scale grammar",
    alias: ["action ladder", "1:5:10", "exponential engine"],
    short:
      "The large scale ratios are exponential actions of α⁻¹ with rungs 1 : 5 : 10 = C(5,0):C(5,1):C(5,2). v_EW ∼ e^(−α⁻¹/5), Λ ∼ e^(−2α⁻¹), H₀ ∼ √Λ — one engine.",
  },
  {
    term: "status markers",
    alias: ["[E]", "[C]", "[O]", "[X]", "marker key", "fine types"],
    short:
      "The four public display classes: [E] exact/machine-proven, [C] conditional (named hypotheses), [O] open/axiom, [X] falsifiable kill test. The ledger keeps the fine per-claim types (Identity, Lattice, Formal, Numerical, Physical, Axiom) — it is the source of truth.",
  },
  {
    term: "two engines",
    alias: ["discrete closure", "boundary dressing"],
    short:
      "The theory factorises into two engines: Engine 1 (discrete closure from g_car = 5) builds E₈ and the SM packet; Engine 2 (boundary dressing from c₃) gives the seed, α⁻¹ and the scale grammar. Gravity is Engine 2's geometry channel.",
  },
  {
    term: "v_geo",
    alias: ["v_geo", "scale anchor", "U_point", "(U_wall)", "U_wall"],
    short:
      "The flavor/scale interface (historically labelled U_wall): the quark ratios are closed (Readout Rigidity, 55/117) and the selector triangle pins R columnwise; the only remainder is the single dimensionful amplitude scale v_geo — the same nature as gravity's 1/G [O].",
  },
  {
    term: "G_net",
    alias: ["G_net", "(G_metric)", "G_metric", "seam-net inclusion", "continuum realisation"],
    short:
      "The metric-sector interface (historically labelled G_metric): R + R² is heat-kernel grounded (G2) and gap-decoupled (G5); the closing statement is the index-4 μ₄ seam-net inclusion ⇒ holomorphic (E₈)₁, with net existence and full-cone reflection positivity discharged to [E] (v175). Status [C] — closed modulo cited theorems (not solved): the target (E₈)₁ net is now pinned at every computable level by an explicit gapped lattice model (v367/v368) and the S3 closure stack — central charge c = 8 from the lattice (v376), the (E₈)₁ character 248/1 (v377), genus-1 torus GSD = 1 (v378) and reflection positivity (v379), plus the ground-state witnesses c₋ = 8 via the modular commutator (v489) and μ_pre = 4 via the parity census (v490). With the Modular Spectral Closure (v258–v261), the boundary QFT is therefore one relative object closed modulo cited theorems via the Seam Equivalence Theorem SEAM.EQUIV.01 (the raw RP seam IS the holomorphic (E₈)₁ net at τ=i), Lean-pinned (FORM.SEAM.MMST.01, SeamScalingLimit.lean) to the published MMST/Adamo scaling-limit theorems. The one residual is [O] = the abstract continuum scaling-limit existence only (v336; extension leg on the peer-reviewed crossed-product package, realisation at invariant level, v469; stays [O]). The local field equation is separately parameter-free (v358/v359); QG closure is a certification layer, not a prerequisite for testing the readouts [C]/[O].",
  },
  {
    term: "F_transfer",
    alias: ["F_transfer", "(F_frontier)", "F_frontier", "transfer functor"],
    short:
      "The downstream interface: the continuous transport from compiler source data to measured observables, now a typed RUNNABLE solver suite F_transfer = F_pole ⊕ F_Boltzmann ⊕ F_relic ⊕ F_QCD — Koide source→pole (v371), η_B via the Boltzmann washout (v372), the axion relic abundance (v373) and m_p/m_e via QCD/EW matching (v374), each with a kill test and folded into a prediction-observatory CI (v375). The functor contract CONTRACT.F.01 (v213) pins four axioms (μ₄-deck equivariant, Plücker-preserving, positive/stochastic, external-module-explicit); a machine guard (v187) keeps every output a typed [C] bridge, never promoted to a primitive [E] compiler prediction. The third research interface alongside v_geo and G_net.",
  },
  {
    term: "SEAM.EQUIV.01",
    alias: ["SEAM.EQUIV.01", "Seam Equivalence Theorem", "S3", "the keystone", "seam equivalence", "the single keystone"],
    short:
      "The keystone of the metric sector: the raw reflection-positive seam state IS the holomorphic (E₈)₁ boundary net at τ=i. Status [C] — closed modulo cited theorems, NOT solved: the target net is pinned at every computable level by an explicit gapped lattice model (v367/v368) and the S3 closure stack (c = 8 from the lattice v376, the (E₈)₁ character 248/1 v377, genus-1 torus GSD = 1 v378, reflection positivity v379; ground-state witnesses c₋ = 8 via the modular commutator v489 and μ_pre = 4 via the parity census v490), and the chain is Lean-pinned (FORM.SEAM.MMST.01, SeamScalingLimit.lean) to the published MMST/Adamo scaling-limit theorems. The only residual is [O] = the abstract continuum scaling-limit existence (v336), a cited published theorem outside the computational suite; its 128-spinor extension leg is certified at net level by the peer-reviewed crossed-product package (v469, Longo–Rehren/Böckenhauer/KLM; AGT/AMT second witness), realisation at invariant level; stays [O]. Its conformal-deck face QGEO.SYM.01 is a corollary (v335). TFPT's one irreducible structural postulate — the role 'c = const' plays in relativity.",
  },
  {
    term: "Crossed-product route (v469)",
    alias: ["crossed-product route", "crossed product route", "v469", "SEAM.EQUIV.CROSSEDPRODUCT.01"],
    short:
      "The net-level certification of the 128-spinor extension SO(16)₁ → (E₈)₁: the spinor weight h_s = 16/16 = 1 ∈ ℤ fulfils the Longo–Rehren locality criterion, so the ℤ₂ simple-current crossed product is a local index-2 extension (1995–2001 peer-reviewed subfactor theory; KLM μ = 1 ⇒ holomorphic). AGT/AMT preprints are the independent second witness. SEAM.EQUIV.01 stays [O].",
  },
  {
    term: "QG.AMB.01",
    alias: ["QG.AMB.01", "QG.AMB", "C7", "G6", "ambient measure", "quantum-gravity measure", "ambient QG measure"],
    short:
      "The ambient, non-perturbative quantum-gravity measure (historically C7 / G6). Status [C] — discharged as a redundancy, NOT an open frontier: the ambient-redundancy theorem (v369) plus the S3 reflection-positivity closure (v379) show it is a certification object, not missing dynamics — every readout factors through the gapped admissible spectrum (Decoupling Theorem v337, Δ_eff = 1.648 > 0), so TFPT provably does not need it. Conditional on SEAM.EQUIV.01 + Bisognano–Wichmann intrinsicality (the residual [O]). The R²/Weyl² Stelle ghost is a Seeley–DeWitt truncation artefact, so perturbative spin-2 graviton unitarity is established [C] (v304/v370/v380) — not a non-unitarity hole.",
  },
  {
    term: "ALPHA.QUILLEN.EXACT.01",
    alias: ["ALPHA.QUILLEN", "alpha Quillen target", "Quillen determinant target"],
    short:
      "The tracked [O] target: prove F_U(1) is the exact Quillen determinant functional of the seam U(1). v470 sharpens it: the α³ level = the computed bulk Chern invariant |C| = 1 (inflow), the F-normalisation = the embedding index k_Y = 5/3. v472 exhibits the bridge lemma at the finite level: the determinant line over the U(1)-twist moduli of the collar carries curvature = 1 = the inflow level; what stays [O] is the continuum ζ-det identification. The α⁻¹ value itself stays [E].",
  },
  {
    term: "celestial route",
    alias: ["CELEST.SEAM.01", "celestial sphere", "celestial-holographic route"],
    short:
      "The fourth research contract: the seam's boundary 2-sphere IS the celestial sphere of null directions (Möb ≅ PSL(2,ℂ)), and the E₈ μ₄-glue is a flat ℤ₄ monodromy on the A₃ ALE space ℂ²/ℤ₄. WP1–WP5d (both WP5d stages) plus the WP5e α and β stages executed exactly (v492–v505: clock² = deck, null ideal derived, deleting operator explicit, GNS limit state constructed, two-interval index measured, split + strong additivity witnessed, prefactor + level k = 1 pinned on the CFT side, and the equivariant anomaly ledger exact on the twistor side with the honest a₀ refutation); WP5e proper (the global BCOV quantisation) open [O]. A second, quantitative approach to SEAM.EQUIV.01 — which stays [O].",
  },
  {
    term: "ALE space",
    alias: ["A₃ ALE", "A3 ALE space", "ℂ²/ℤ₄"],
    short:
      "An asymptotically locally Euclidean hyperkähler 4-space resolving ℂ²/Γ. TFPT's case is Γ = ℤ₄: ℂ²/ℤ₄ is the A₃ singularity XY = Z⁴, whose deck group induces the sheet flip on the celestial sphere while the μ₄ clock is the Kähler U(2) phase diag(i,1) with clock² = deck (v492).",
  },
  {
    term: "null ideal",
    alias: ["level-2 null ideal", "the 27000"],
    short:
      "The maximal submodule the (E₈)₁ vacuum character deletes at level 2: exactly 27000 = 30³ = (h∨)³ out of Sym²(248) = 27000+3875+1, derived from root data (v497); its generator is the explicit singular vector |s⟩ = (E^θ_{−1})²|0⟩ with J^a_1|s⟩ = 0 on all 248 generators (v498). Quotient 4124 = the μ₄ sector sum.",
  },
];

const NORMALISE = (s: string) => s.toLowerCase().trim();

export function findEntry(needle: string): GlossaryEntry | undefined {
  const norm = NORMALISE(needle);
  return GLOSSARY.find((entry) => {
    if (NORMALISE(entry.term) === norm) return true;
    return entry.alias?.some((a) => NORMALISE(a) === norm);
  });
}
