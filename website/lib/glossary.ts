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
    term: "seam constant",
    alias: ["c₃", "c3", "boundary number", "c_3"],
    short:
      "The first axiom P1: c₃ = 1/(8π). The boundary/seam normaliser, Gauss–Bonnet-hardenable as 1/(|ℤ₂|·∮ K). Drives the seed, α⁻¹ and the scale grammar.",
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
    alias: ["G_net", "(G_metric)", "G_metric", "ambient measure", "quantum-gravity measure", "seam-net inclusion"],
    short:
      "The metric-sector interface (historically labelled G_metric): R + R² is heat-kernel grounded (G2) and gap-decoupled (G5); the closing statement is the index-4 μ₄ seam-net inclusion ⇒ holomorphic (E₈)₁. Net existence and full-cone reflection positivity are discharged to [E] (v175); the residual is then reduced (v176–v181) to a single definitional premise QGEO.SYM.01 — the carrier μ₄ clock is the conformal deck of the seam — which is bedrock, not reducible further without relabeling. The deduction below the premise is now machine-checked: the geometric normal form (UNIFORM: z↦iz, σρσ=ρ⁻¹, orbit→μ₄, multiplier order-4 ⇔ ζ=±i; FORM.QGEO.02) and the conditional implication mark-local ⇒ ω∘ρ=ω (FORM.QGEO.01) are Lean-formalised (AUDIT: PASS, only the three standard kernel axioms), so QGEO.SYM.01 itself stays the one [O] postulate. Full QG closure is a certification layer, not a prerequisite for testing the readouts [C]/[O].",
  },
  {
    term: "F_transfer",
    alias: ["F_transfer", "(F_frontier)", "F_frontier", "transfer functor"],
    short:
      "The downstream interface: the continuous transport from compiler source data to measured observables. Koide source→pole, η_B source→Boltzmann relic, axion scale→abundance and m_p/m_e→QCD/EW matching are four instances of this one missing functor — not primitive compiler predictions [C]. The functor contract CONTRACT.F.01 (v213) pins it with four axioms (μ₄-deck equivariant, Plücker-preserving, positive/stochastic, external-module-explicit); the third research contract alongside U_wall and G_metric.",
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
