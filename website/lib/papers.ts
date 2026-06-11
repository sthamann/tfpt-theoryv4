export type PaperStatus =
  | "orientation"
  | "core"
  | "synthesis"
  | "audit"
  | "frontier"
  | "horizon"
  | "contracts";

export interface Paper {
  id: string;
  number: number;
  slug: string;
  title: string;
  subtitle: string;
  abstract: string;
  status: PaperStatus;
  statusLabel: string;
  pdf: string;
  pages?: number;
  inputs: string[];
  contribution: string[];
  notClaimed: string[];
  falsification: string[];
  sections: PaperSection[];
  keyFormulas: KeyFormula[];
  highlights: Highlight[];
}

export interface PaperSection {
  title: string;
  body: string;
  formulas?: string[];
}

export interface KeyFormula {
  label: string;
  latex: string;
  description?: string;
}

export interface Highlight {
  label: string;
  value: string;
  description: string;
}

export const STATUS_META: Record<
  PaperStatus,
  { label: string; color: string; bg: string; ring: string; gradient: string }
> = {
  orientation: {
    label: "Reading guide",
    color: "text-slate-200",
    bg: "bg-slate-500/10",
    ring: "ring-slate-400/30",
    gradient: "from-slate-400 to-slate-500",
  },
  core: {
    label: "Compiler core",
    color: "text-blue-300",
    bg: "bg-blue-500/10",
    ring: "ring-blue-500/30",
    gradient: "from-blue-500 to-violet-500",
  },
  synthesis: {
    label: "Origin synthesis",
    color: "text-emerald-300",
    bg: "bg-emerald-500/10",
    ring: "ring-emerald-500/30",
    gradient: "from-emerald-500 to-teal-500",
  },
  audit: {
    label: "E8 audit & bootstrap",
    color: "text-cyan-300",
    bg: "bg-cyan-500/10",
    ring: "ring-cyan-500/30",
    gradient: "from-cyan-500 to-blue-500",
  },
  frontier: {
    label: "Honest frontier",
    color: "text-orange-300",
    bg: "bg-orange-500/10",
    ring: "ring-orange-500/30",
    gradient: "from-orange-500 to-red-500",
  },
  horizon: {
    label: "Appendix H — reframe",
    color: "text-fuchsia-300",
    bg: "bg-fuchsia-500/10",
    ring: "ring-fuchsia-500/30",
    gradient: "from-fuchsia-500 to-pink-500",
  },
  contracts: {
    label: "Open research gates",
    color: "text-amber-300",
    bg: "bg-amber-500/10",
    ring: "ring-amber-500/30",
    gradient: "from-amber-500 to-yellow-500",
  },
};

export const papers: Paper[] = [
  {
    id: "00",
    number: 0,
    slug: "introduction",
    title: "The Compiler Closure of TFPT",
    subtitle: "Reading guide, status assessment, and the dependency DAG",
    abstract:
      "The entry document. TFPT tips from 'many sectors with surprising hits' to 'one small discrete compiler generates those sectors': from two axioms — the seam constant c₃ = 1/(8π) and the carrier rank g_car = 5 — it builds D₅ ⊕ A₃ + μ₄ ⇒ E₈ and reads off the Standard Model, the constants, and the scale grammar. This note is the reading guide: the architecture, the before/after against the seven original papers, the predictions, the dependency DAG, and the single proof ledger.",
    status: "orientation",
    statusLabel: "Reading guide",
    pdf: "/papers/introduction.pdf",
    inputs: ["The two axioms {c₃, g_car}; everything else is a consequence."],
    contribution: [
      "States the compiler closure, the two-engine picture, the dependency DAG, the proof ledger, and the live experimental tests in one place.",
    ],
    notClaimed: [
      "No new physics is introduced here — the introduction is a map. Load-bearing derivations live in the companion documents.",
    ],
    falsification: [
      "Fails as a guide if the dependency order is misstated, if a status marker disagrees with the ledger, or if a claim is promoted past the grade the companion document carries.",
    ],
    sections: [
      {
        title: "Two inputs, one machine",
        body: "Two numbers go in — a boundary number 1/(8π) and a five-slot carrier — and the discrete Standard-Model core, the dimensionless constants and several scale readouts come out. The dashed loop is the point: the machine reproduces the very two numbers it started from, so the discrete core is overdetermined rather than fitted.",
        formulas: [
          "\\{c_3, g_{\\mathrm{car}}\\} \\;\\Rightarrow\\; D_5 \\oplus A_3 \\xrightarrow{\\;\\mu_4\\;} E_8 \\;\\Rightarrow\\; (\\text{SM},\\ \\text{constants},\\ \\text{scale grammar})",
        ],
      },
      {
        title: "The master story is two engines",
        body: "Read from the two axioms, the theory factorises into exactly two engines: a discrete closure (from g_car = 5) that builds E₈ and the SM packet, and a boundary dressing (from c₃) that produces the seed, α⁻¹ and the scale grammar. Gravity is not a third block — it is the geometry channel of Engine 2.",
        formulas: [
          "\\text{Engine 1: } g_{\\mathrm{car}}{=}5 \\to E_8 \\to (N_{\\mathrm{fam}}, \\Omega_{\\mathrm{adm}}, b_1, R)",
          "\\text{Engine 2: } c_3{=}\\tfrac{1}{8\\pi} \\to (u{=}\\varphi_0, \\alpha^{-1}, \\xi, \\Lambda, H_0)",
        ],
      },
      {
        title: "The compact status formula",
        body: "TFPT 5.0 closes the discrete compiler, the algebraic SM readout, the EM fixed point, the admissible gapped IR sector and the R + R² spectral-action shadow. It does not yet certify a strict physical TOE. The residual is one flavor wall-selection, one quantum-gravity measure, and a set of deliberately typed interfaces.",
        formulas: [
          "\\underbrace{\\text{compiler}}_{\\text{closed}}\\ \\Big|\\ \\underbrace{\\text{admissible IR physics}}_{\\text{conditional (RP, gap)}}\\ \\Big|\\ \\underbrace{\\text{strict physical TOE}}_{\\text{open}}",
          "\\text{Rest} = (U_{\\mathrm{wall}}) \\oplus (G_{\\mathrm{metric}}) \\oplus (F_{\\mathrm{frontier}})",
        ],
      },
      {
        title: "The anchor: one number a = (1,1,2)",
        body: "The two axioms are not even independent: they are the elementary symmetric polynomials of the single parabolic anchor a = (1,1,2), and its power sums generate the big Lie data directly. The inputs collapse to the anchor plus the lone continuous primitive π.",
        formulas: [
          "e_1(a)=4=|\\mu_4|,\\quad e_2(a)=5=g_{\\mathrm{car}},\\quad e_3(a)=2=|\\mathbb{Z}_2|",
          "c_3 = \\frac{1}{2\\,e_1(a)\\,\\pi} = \\frac{1}{8\\pi}, \\qquad |R(E_8)| = p_1 p_2 p_3 = 240",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Compiler closure",
        latex:
          "\\{c_3, g_{\\mathrm{car}}\\} \\Rightarrow D_5 \\oplus A_3 + \\mu_4 \\Rightarrow E_8",
        description: "Two axioms build the E₈ audit hull; the SM is read off by projection.",
      },
      {
        label: "Bootstrap loop",
        latex: "E_8\\text{ closure} \\Rightarrow g_{\\mathrm{car}}{=}5,\\ \\ 8 = \\operatorname{rank}E_8",
        description: "Inputs and output are mutually locked — only π stays irreducible.",
      },
      {
        label: "Reduction in one line",
        latex: "247\\,\\text{pages} \\rightsquigarrow \\text{2 inputs} + \\text{1 machine}",
        description: "The number of independent structural assumptions drops to two.",
      },
    ],
    highlights: [
      {
        label: "Axioms",
        value: "2",
        description: "c₃ = 1/(8π) and g_car = 5 — the rest is a consequence",
      },
      {
        label: "Compiler",
        value: "Z₃₀ = 2·3·5",
        description: "Coxeter–cyclotomic generator behind every sector",
      },
      {
        label: "Free primitive",
        value: "π",
        description: "The one genuinely irreducible continuous number",
      },
      {
        label: "Documents",
        value: "8",
        description: "Introduction + 4 core docs + Appendix H + Origin Theory + contracts",
      },
    ],
  },
  {
    id: "01",
    number: 1,
    slug: "architecture-e8",
    title: "Architecture and the E₈ Compiler",
    subtitle: "The two axioms, the derivation map, and the D₅ × A₃ → E₈ construction",
    abstract:
      "The architecture layer: how the two axioms c₃ = 1/(8π) and g_car = 5 build the Coxeter–cyclotomic compiler — the carrier C⁺ = D₅, the family geometry ℙ¹∖μ₄ = A₃, the μ₄ glue D₅ ⊕ A₃ + μ₄ ⇒ E₈, the electromagnetic fixed point α⁻¹ (with its ablation), and the whole number alphabet 16, 40, 41, 48, 240, 248 as carrier traces.",
    status: "core",
    statusLabel: "Compiler core",
    pdf: "/papers/tfpt_1_architecture_e8.pdf",
    inputs: [
      "P1: the boundary kernel c₃ = 1/(8π) (Gauss–Bonnet hardenable).",
      "P2: the five-slot carrier g_car = 5 (3 colour + 2 weak); P2 algebra is Lean-formalised.",
    ],
    contribution: [
      "The glue theorem E₈ = (D₅ ⊕ A₃) + μ₄: common discriminant ℤ₄, glue index |μ₄| = 4, and q(D₅) + q(A₃) = 5/4 + 3/4 = 2 (the E₈ root norm).",
      "240 = 16·5·3 and 248 = 240 + 8 derived as carrier traces; b₁ = 41/10 and the hypercharge polynomial from the 3+2 split.",
      "The electromagnetic fixed point α⁻¹ = 137.0359992168… as the unique root of F_U(1)(α) = 0.",
    ],
    notClaimed: [
      "E₈ is the unimodular audit/compiler hull, not an unbroken physical gauge group; the SM is a readout after projection.",
      "No dimensionful mass ladder, no full quantum-gravity measure, no cosmology fit.",
    ],
    falsification: [
      "Fails if D₅ and A₃ do not share the ℤ₄ discriminant, if the glue norms do not sum to 2, or if F_U(1)(α) = 0 has no/second admissible root.",
    ],
    sections: [
      {
        title: "The Pascal compiler on five carrier slots",
        body: "The even-Hamming code on five slots is the D₅ half-spinor: its dimension is the Pascal sum 1 + 5 + 10 = 16, which forces g_car = 5 uniquely. The E₈ root count is then a pure carrier trace.",
        formulas: [
          "\\dim S^+ = 2^{g_{\\mathrm{car}}-1} = \\binom{g_{\\mathrm{car}}}{0}+\\binom{g_{\\mathrm{car}}}{1}+\\binom{g_{\\mathrm{car}}}{2} \\iff g_{\\mathrm{car}} = 5",
          "|R(E_8)| = \\dim S^+(\\dim S^+ - 1) = 16 \\cdot 15 = 240",
        ],
      },
      {
        title: "The μ₄ glue: how E₈ is really built",
        body: "D₅ = so(10) (spinor 16) and A₃ = su(4) (the four-puncture family geometry ℙ¹∖μ₄) have the same discriminant group ℤ₄. Their discriminant-form norms are two TFPT constants that add to the E₈ root norm, so the glue closes as a lattice theorem — not a posited 248.",
        formulas: [
          "\\operatorname{disc}(D_5) = \\operatorname{disc}(A_3) = \\mathbb{Z}_4, \\qquad [E_8 : D_5 \\oplus A_3] = |\\mu_4| = 4",
          "q(D_5) + q(A_3) = \\tfrac{5}{4} + \\tfrac{3}{4} = 2 = |\\text{$E_8$ root}|^2",
        ],
      },
      {
        title: "The Z₃₀ = 2·3·5 cyclotomic Coxeter compiler",
        body: "The Coxeter number of E₈ is h = 30 = 2·3·5 — exactly the three discrete atoms (sheet ℤ₂, families ℤ₃, carrier g_car = 5). The rank is the count of live phases of the order-30 cycle.",
        formulas: [
          "h = |\\mathbb{Z}_2|\\cdot N_{\\mathrm{fam}}\\cdot g_{\\mathrm{car}} = 2\\cdot 3\\cdot 5 = 30",
          "|R(E_8)| = r h = 240, \\qquad \\dim E_8 = r(h+1) = 8\\cdot 31 = 248, \\qquad r = \\varphi(30) = 8",
        ],
      },
      {
        title: "The electromagnetic fixed point",
        body: "The fine-structure constant is the unique positive root of a parameter-free cubic built only from c₃, the abelian coefficient (Σ L + N_Φ = 41 = 10 b₁) and the exact seam generating function. Existence and uniqueness are proved; the value lands 1.9σ from CODATA-2022.",
        formulas: [
          "F_{U(1)}(\\alpha) = \\alpha^3 - 2c_3^3\\,\\alpha^2 - \\tfrac{4}{5}c_3^6\\Big(\\textstyle\\sum_{f,j}L_{f,j} + N_\\Phi\\Big)\\log\\tfrac{1}{\\varphi_{\\mathrm{seam}}(\\alpha)} = 0",
          "\\alpha^{-1} = 137.035\\,999\\,216\\,8\\ldots",
        ],
      },
      {
        title: "The scale grammar: one exponential engine",
        body: "The same α⁻¹ ≈ 137 generates the electroweak scale (divided by the carrier 5), the cosmological constant (times 2) and the Hubble scale (via the square root) — the action ladder 1 : 5 : 10 is the Pascal row of the carrier.",
        formulas: [
          "A_{\\mathrm{EW}} : A_H : A_\\Lambda = 1 : 5 : 10 = \\tbinom{5}{0} : \\tbinom{5}{1} : \\tbinom{5}{2}",
          "v_{\\mathrm{EW}} \\sim e^{-\\alpha^{-1}/5}, \\qquad \\Lambda \\sim e^{-2\\alpha^{-1}}, \\qquad H_0 \\sim \\sqrt{\\Lambda}",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Glue theorem",
        latex: "E_8 = (D_5 \\oplus A_3) + \\mu_4",
        description: "disc = ℤ₄, glue index 4, q(D₅)+q(A₃) = 2. [L]",
      },
      {
        label: "Carrier traces",
        latex: "240 = 16\\cdot 5\\cdot 3, \\qquad 248 = 240 + 8",
        description: "E₈ numbers as traces over the 3+2 carrier, not inputs. [I]",
      },
      {
        label: "EM fixed point",
        latex: "F_{U(1)}(\\alpha_\\star) = 0 \\Rightarrow \\alpha^{-1} = 137.0359992168\\ldots",
        description: "Unique root; CODATA-2022 137.035999177(21), dev 2.9×10⁻¹⁰ (1.9σ). [I/N]",
      },
      {
        label: "Abelian coefficient",
        latex: "10\\,b_1 = 41 = \\textstyle\\sum_{f,j} L_{f,j} + N_\\Phi",
        description: "b₁ = 41/10 as a carrier trace.",
      },
    ],
    highlights: [
      {
        label: "E₈ glue",
        value: "D₅ ⊕ A₃ + μ₄",
        description: "Closed lattice construction, not a posited 248",
      },
      {
        label: "α⁻¹",
        value: "137.0359992",
        description: "Unique root of F_U(1)(α) = 0; 1.9σ from CODATA-2022",
      },
      {
        label: "q(D₅)+q(A₃)",
        value: "5/4 + 3/4 = 2",
        description: "The even glue condition — the E₈ root norm",
      },
      {
        label: "rank E₈",
        value: "8 = φ(30)",
        description: "Live phases of the order-30 Coxeter cycle",
      },
    ],
  },
  {
    id: "02",
    number: 2,
    slug: "standard-model",
    title: "The Standard Model from the Compiler",
    subtitle: "The φ₀-ladder, flavor from parabolic transport, and the worked closures",
    abstract:
      "The fermion spectrum — masses, Yukawa structure, CKM, the PMNS skeleton and neutrinos — follows from one master formula with one seed φ₀, the carrier base λ_Y = √(φ₀(1−φ₀)), and the residue matrix of the compiler. Plus the flavor block from parabolic transport on ℙ¹∖μ₄, the five worked closures (θ₁₂, quark c, the explicit mass gap, Starobinsky M, the H2 splitting), and gravity/QG as the seam response.",
    status: "core",
    statusLabel: "Compiler core",
    pdf: "/papers/tfpt_2_standard_model.pdf",
    inputs: [
      "The two axioms and the E₈ compiler of Document 1.",
      "The seed φ₀ = 1/(6π) + 3/(256π⁴) and the carrier base λ_Y = √(φ₀(1−φ₀)).",
    ],
    contribution: [
      "One master mass formula for all nine masses, Yukawa, CKM, PMNS and neutrinos, with the word-lengths read off the compiler residue matrix.",
      "The residue matrix R with det R = 8 = h(D₅), principal 2-minors (2,3,5), and χ_R = t³ − 9t² + 10t − 8.",
      "The solar angle sin²θ₁₂ = 1/3 − φ₀/2 = 0.3067 from the seam misalignment ε = q(A₃)φ₀.",
    ],
    notClaimed: [
      "Charged-lepton masses and quark mass ratios are closed; the absolute quark amplitude scale reduces to one overall scale v_geo (Grand Mass Volume + ratios) — the same dimensionful anchor as gravity's 1/G.",
      "Dimensionful m_W, m_Z, m_H, sin²θ_W, α_s are RG scheme-layer projections, not compiler outputs.",
    ],
    falsification: [
      "Fails if the residue invariants (det 8, minors 2,3,5, χ_R) are not respected by a future global CKM/PMNS fit, or if the lepton φ₀-ladder mismatches the observed hierarchy.",
    ],
    sections: [
      {
        title: "One master formula instead of many Yukawas",
        body: "Every fermion mass is the same ladder: the geometric VEV times the carrier base raised to a compiler word-length, times an O(1) residue. The word-lengths are the fixed residue matrix of the compiler — not free parameters.",
        formulas: [
          "\\hat m_{f,j} = \\frac{v_{\\mathrm{geo}}}{\\sqrt2}\\,\\lambda_Y^{\\,L_{f,j}}\\,\\Lambda_{f,j}, \\qquad \\lambda_Y = \\sqrt{\\varphi_0(1-\\varphi_0)}",
          "\\varphi_0 = \\frac{1}{6\\pi} + \\frac{3}{256\\pi^4} = 0.05317\\ldots",
        ],
      },
      {
        title: "The flavor residue matrix is the compiler signature",
        body: "The word-length matrix L = R + 6·(winding) carries only compiler numbers: its trace is N_fam², its determinant is h(D₅) = 8, its principal 2-minors are (2,3,5) with product 30 = h(E₈), and its Frobenius norm is dim E₆ = 78.",
        formulas: [
          "R = \\begin{pmatrix} 1 & 3 & 0 \\\\ 1 & 5 & 2 \\\\ 2 & 5 & 3 \\end{pmatrix}, \\qquad \\det R = 8, \\quad \\|R\\|_F^2 = 78",
          "\\chi_R(t) = t^3 - \\underbrace{9}_{N_{\\mathrm{fam}}^2}t^2 + \\underbrace{10}_{\\binom{5}{2}}t - \\underbrace{8}_{h(D_5)}",
        ],
      },
      {
        title: "Charged leptons: completely closed in φ₀",
        body: "The lepton amplitudes are the rationals (16/7, 4/3, 7/6) with product 2⁵/N_fam² = 32/9, and the masses are exact φ₀-powers. Applied to the down sector the lepton law provably fails — the quark c's live on the parabolic wall.",
        formulas: [
          "(\\hat m_e, \\hat m_\\mu, \\hat m_\\tau) = \\frac{v_{\\mathrm{geo}}\\pi}{\\sqrt2}\\Big(\\tfrac{16}{7}(\\varphi_0)^5,\\ \\tfrac{4}{3}(\\varphi_0)^3,\\ \\tfrac{7}{6}(\\varphi_0)^2\\Big)",
          "c_e\\,c_\\mu\\,c_\\tau = \\frac{2^{g_{\\mathrm{car}}}}{N_{\\mathrm{fam}}^2} = \\frac{32}{9}",
        ],
      },
      {
        title: "Quark ratios from the same word-lengths",
        body: "The quark mass ratios are pure integer Plücker readouts on the derived selector stratum — no transcendental solve. The absolute amplitude reduces to one overall scale v_geo (ratios + Grand Mass Volume), the same dimensionful anchor as gravity's 1/G.",
        formulas: [
          "\\frac{c_u}{c_d} = \\frac{g_{\\mathrm{car}}\\cdot 11}{N_{\\mathrm{fam}}^2\\,\\Delta_Q} = \\frac{55}{117}, \\quad \\frac{c_c}{c_s} = \\frac{34}{47}, \\quad \\frac{c_t}{c_b} = \\frac{3}{26}",
          "\\hat m_t/\\hat m_b = \\tfrac{3}{26}(\\varphi_0)^{-2} = 40.81",
        ],
      },
      {
        title: "The solar angle θ₁₂ from the seam",
        body: "Tri-bimaximal gives 1/3; the charged-lepton 1–2 misalignment is the seam ε = q(A₃)φ₀ = (3/4)φ₀, and TBM geometry gives the only previously open SM angle as a conditional derivation — 0.1% from NuFIT 6.0.",
        formulas: [
          "\\varepsilon = q(A_3)\\,\\varphi_0 = \\tfrac{3}{4}\\varphi_0, \\qquad q(A_3) = \\frac{N_{\\mathrm{fam}}}{|\\mu_4|}",
          "\\sin^2\\theta_{12} = \\tfrac{1}{3} - \\tfrac{2}{3}\\varepsilon = \\tfrac{1}{3} - \\tfrac{\\varphi_0}{2} = 0.3067",
        ],
      },
      {
        title: "Branch kernels select the sectors (the sheet question, closed modulo one gate)",
        body: "At the two branch points of the anchor-block double cover the block is rank 1, with integer kernels — at the carrier point the kernel is the democratic vector itself. Rank 1 forces the kernel image onto the antisymmetric direction (−1,1,0): up and down are the deck-odd pair, and the lepton pairing vanishes — the leptons sit on the ramification (Koide is leptonic). The anchor-forced cusp conjugation T_A (with a = e₂+e₃, the conjugation-symmetric vector) realises the same deck action, and the dictionary 'Q₊ grading = A₃ discriminant grading' is now derived (G = T_A·Σ acts integrally as the B₁⊕E decomposition on the cusp basis): the sheet question carries no separate [P] — its residual coincides with the one existing Q-geometry gate.",
        formulas: [
          "P(-\\tfrac23)\\,w = \\tfrac{20}{3}(1,-1,0), \\qquad P(-\\tfrac53)\\,w = \\tfrac{2}{3}(-1,1,0)",
          "T_A = \\begin{pmatrix} 0 & 1 & 0 \\\\ 1 & 0 & 0 \\\\ 2 & -2 & 1 \\end{pmatrix}, \\qquad a = e_2 + e_3, \\qquad \\det T_A = -1",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Master mass formula",
        latex: "\\hat m_{f,j} = \\frac{v_{\\mathrm{geo}}}{\\sqrt2}\\,\\lambda_Y^{\\,L_{f,j}}\\,\\Lambda_{f,j}",
        description: "One seed φ₀, one carrier base, the compiler residue matrix.",
      },
      {
        label: "Flavor invariants",
        latex: "\\det R = 8,\\quad \\mathrm{minors}=(2,3,5),\\quad \\chi_R = t^3 - 9t^2 + 10t - 8",
        description: "Exact compiler signature any future fit must satisfy. [I]",
      },
      {
        label: "Solar angle",
        latex: "\\sin^2\\theta_{12} = \\tfrac{1}{3} - \\tfrac{\\varphi_0}{2} = 0.3067",
        description: "Previously open; now conditionally derived (seam ε = (3/4)φ₀). [N/P]",
      },
      {
        label: "Lepton product",
        latex: "c_e c_\\mu c_\\tau = \\frac{2^{g_{\\mathrm{car}}}}{N_{\\mathrm{fam}}^2} = \\frac{32}{9}",
        description: "Charged-lepton amplitudes closed in φ₀.",
      },
    ],
    highlights: [
      {
        label: "Masses",
        value: "1 formula",
        description: "All nine masses + mixings from one φ₀-ladder",
      },
      {
        label: "det R",
        value: "8 = h(D₅)",
        description: "Flavor matrix determinant is a compiler number",
      },
      {
        label: "sin²θ₁₂",
        value: "0.3067",
        description: "1/3 − φ₀/2; 0.1% from NuFIT 6.0",
      },
      {
        label: "Quark ratios",
        value: "55/117, 34/47, 3/26",
        description: "Integer Plücker readouts on the selector stratum",
      },
      {
        label: "Anchor plane",
        value: "(3x+2)(3x+5)",
        description: "det B(K+xQ): 2/3 (Koide/gap) & 5/3 (D₅/A₃) are its singular points [I/L]",
      },
      {
        label: "Double cover",
        value: "Koide = branch pt",
        description: "y² = det B(K+xQ): Koide −2/3 & carrier −5/3 are the two branch points (deck 2 = |ℤ₂|, disc = N_fam⁴) [I/L]",
      },
    ],
  },
  {
    id: "03",
    number: 3,
    slug: "e8-audit-bootstrap",
    title: "E₈ Audit, Cascade Bridge and Bootstrap",
    subtitle: "The seven E₈ slices as an audit raster, the cascade spine, and the Möbius loop",
    abstract:
      "E₈ as an audit container, not a mystery: the seven maximal slices of 248 as a falsification raster (every load-bearing number must appear in at least one projection), the bridge showing the old E₈ orbit cascade D = 60 − 2n is the same even-integer spine as the compiler, and the Möbius bootstrap in which g_car = 5 and the '8' in c₃ are overdetermined E₈-closure fixed points — only π irreducible.",
    status: "audit",
    statusLabel: "E8 audit & bootstrap",
    pdf: "/papers/tfpt_3_e8_audit_bootstrap.pdf",
    inputs: [
      "The compiler core {c₃, g_car} ⇒ E₈ and the residue matrix R from Documents 1–2.",
    ],
    contribution: [
      "The discipline rule: every load-bearing TFPT number must appear in at least one E₈ branching projection — turning the number stock into a falsifiable raster, not numerology.",
      "The numerology null test (v100): an exact census of a fully declared formula grammar plus Monte-Carlo pseudo-theories quantifies the look-elsewhere burden — joint null probability ≤ 10⁻³⁰·⁷ that a random theory of equal formula complexity reproduces the data scorecard (conditional on the declared grammar; with demonstrated power via seed-perturbation and shuffle controls).",
      "E₆ × A₂ reads the flavor matrix: 248 = 78 + 8 + 2·27·3 with ‖R‖_F² = 78 = dim E₆ and det R = 8 = dim A₂.",
      "The Möbius bootstrap: g_car = 5 forced three ways and the '8' in c₃ = rank E₈ = h(D₅) = φ(30) = det R.",
    ],
    notClaimed: [
      "The atlas slice readings are audit-level [A] — a program, not a proof of new physics.",
      "The bootstrap is not creation from nothing: two inputs remain, and π is not produced by the loop.",
    ],
    falsification: [
      "Fails if a load-bearing number cannot be placed in any E₈ projection, or if the reverse glue μ² − 5μ + 4 = 0 does not single out the (D₅, A₃) branch.",
    ],
    sections: [
      {
        title: "The seven E₈ slices as an audit raster",
        body: "Each maximal subalgebra of E₈ projects a TFPT module. The strongest new hit: E₆ × A₂ reads the flavor residue matrix, with E₆ reading its Frobenius norm and A₂ the three-family symmetry.",
        formulas: [
          "248 = \\|R\\|_F^2 + \\det R + 2(\\mathbf{1}^\\top R\\,a)\\,N_{\\mathrm{fam}} = 78 + 8 + 2\\cdot 27\\cdot 3",
          "\\|R\\|_F^2 = 78 = \\dim E_6, \\qquad \\det R = 8 = \\dim A_2 = h(D_5)",
        ],
      },
      {
        title: "The numerology null test (look-elsewhere quantified)",
        body: "An explicit, fully declared null model: the entire complexity-matched formula grammar (provably containing every scored TFPT formula) is enumerated exactly against conservative data windows over the 13 scored frozen-registry observables; Monte-Carlo pseudo-theories and negative controls (seed perturbation, data shuffle) demonstrate the test's power; all 94 500 variants of the F_U(1) equation are root-solved with exactly one CODATA hit. The result is a null-model rejection conditional on the declared grammar — never 'certainty'.",
        formulas: [
          "\\prod_i p_i = 10^{-25.8} \\;(13\\ \\text{observables}), \\qquad p_\\alpha \\le 1.1\\cdot 10^{-5}",
          "P(\\text{null reproduces the scorecard incl.\\ }\\alpha) \\le 10^{-30.7} \\;(\\approx 102\\ \\text{bits})",
        ],
      },
      {
        title: "The cascade bridge: D = 60 − 2n",
        body: "The old E₈ orbit cascade is the same even-integer spine: it starts at 60 = 2·3·10, ends at 8 = h(D₅) (the flavor selector), passes the Coxeter rung 30 = h(E₈), and the product of endpoints recovers the root count.",
        formulas: [
          "D_n = 60 - 2n, \\qquad \\frac{D_{\\mathrm{start}}\\,D_{\\mathrm{end}}}{2} = \\frac{60\\cdot 8}{2} = 240 = |R(E_8)|",
          "240 + D_{\\mathrm{end}} = 248 = \\dim E_8",
        ],
      },
      {
        title: "g_car = 5 forced three ways",
        body: "The carrier rank is an overdetermined E₈-closure fixed point: rank-fill (g + 3 = 8), Coxeter-match (h(D_g) = 2g − 2 = 8), and the integer-glue/norm closure whose reverse-glue quadratic has nontrivial root μ = 4.",
        formulas: [
          "g_{\\mathrm{car}} + 3 = 8, \\qquad h(D_{g}) = 2g - 2 = 8 \\Rightarrow g_{\\mathrm{car}} = 5",
          "q(D_g) + q(A_{\\mu-1}) = 2 \\;\\Longrightarrow\\; \\mu^2 - 5\\mu + 4 = 0",
        ],
      },
      {
        title: "The '8' in c₃ and the irreducible π",
        body: "The seam denominator is fixed five concordant ways. The two axioms collapse to one continuous primitive (π, from Möbius/Gauss–Bonnet) plus one discrete fixed point (the E₈ closure).",
        formulas: [
          "8 = 2|\\mu_4| = \\operatorname{rank}E_8 = h(D_5) = \\varphi(30) = \\det R",
          "\\{c_3, g_{\\mathrm{car}}\\} \\longrightarrow \\underbrace{\\pi}_{\\text{continuous}} + \\underbrace{E_8\\text{ closure}}_{\\text{discrete}}",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "E₆ × A₂ flavor read",
        latex: "248 = 78 + 8 + 2\\cdot 27\\cdot 3",
        description: "‖R‖_F² = 78 = dim E₆, det R = 8 = dim A₂. Audit-level [A].",
      },
      {
        label: "Cascade endpoints",
        latex: "\\tfrac{1}{2}D_{\\mathrm{start}}D_{\\mathrm{end}} = \\tfrac{60\\cdot 8}{2} = 240",
        description: "The old cascade is the same even-integer spine. [I]",
      },
      {
        label: "Reverse glue",
        latex: "\\mu^2 - 5\\mu + 4 = 0",
        description: "Singles out μ = 4 (A₃), g_car = 5. [L]",
      },
      {
        label: "Five readings of 8",
        latex: "8 = \\operatorname{rank}E_8 = h(D_5) = \\varphi(30) = \\det R = 2|\\mu_4|",
        description: "The c₃ denominator is overdetermined.",
      },
    ],
    highlights: [
      {
        label: "Audit rule",
        value: "7 slices",
        description: "Every load-bearing number lives in an E₈ projection",
      },
      {
        label: "Flavor read",
        value: "E₆ × A₂",
        description: "‖R‖² = 78 = dim E₆, det R = 8 = dim A₂",
      },
      {
        label: "g_car = 5",
        value: "forced 3×",
        description: "Rank-fill, Coxeter-match, integer-glue",
      },
      {
        label: "Irreducible",
        value: "π only",
        description: "Bootstrap leaves no free discrete number",
      },
      {
        label: "Null test",
        value: "≤ 10⁻³⁰·⁷",
        description: "Look-elsewhere-corrected probability that a random equal-complexity theory reproduces the scorecard (v100, conditional on the declared grammar)",
      },
    ],
  },
  {
    id: "04",
    number: 4,
    slug: "frontier",
    title: "Frontier Items",
    subtitle: "η_B, m_p/m_e, Koide, dark matter and quantum gravity — honest status",
    abstract:
      "The honest frontier: which physics has a genuine TFPT handle and which does not. For each of η_B, m_p/m_e, the Koide relation, dark matter and full quantum gravity, this note states the genuine structural handle, the precision it currently lands at, and — crucially — what is not a clean compiler power and is deliberately not forced onto the ladder. This document is the status authority for the frontier items.",
    status: "frontier",
    statusLabel: "Honest frontier",
    pdf: "/papers/tfpt_4_frontier.pdf",
    inputs: [
      "The closed branch of Documents 1–3 (compiler, SM packet, scale grammar).",
    ],
    contribution: [
      "η_B = 6.1×10⁻¹⁰ as a downstream readout from the closed Ω_b h² (not a fundamental compiler power).",
      "The Koide relation computed exactly: Q = 0.664, 0.33% below the democratic target 2/3 = |ℤ₂|/N_fam.",
      "The axion dark-matter candidate fixed (θ_i = 170° closed), with f_a = M_scal/128 a conjecture; full QG R + R² heat-kernel grounded, ambient measure open.",
    ],
    notClaimed: [
      "η_B as a fundamental compiler power, the absolute axion relic abundance, an exact Koide 2/3, and m_p/m_e as a compiler number are all explicitly not claimed.",
      "Hard rule: Koide, η_B, the axion relic scale and m_p/m_e are not compiler powers unless their missing QFT/cosmology transfer is supplied.",
    ],
    falsification: [
      "Fails if a frontier item is silently asserted as a forced compiler power; m_p/m_e is explicitly left open [A] and only fails if mis-asserted.",
    ],
    sections: [
      {
        title: "Baryon asymmetry η_B — downstream readout",
        body: "From the closed baryon fraction Ω_b = (4π − 1)β_rad, the asymmetry follows as a cosmological readout. As a fundamental compiler power it is not closed — the leptogenesis Boltzmann solve is not carried out.",
        formulas: [
          "\\Omega_b = (4\\pi - 1)\\beta_{\\mathrm{rad}} = 0.04894, \\qquad \\Omega_b h^2 = 0.0222",
          "\\eta_B = 6.09\\times 10^{-10} \\quad (\\text{observed } 6.1\\times 10^{-10})",
        ],
      },
      {
        title: "The Koide relation — near 2/3, computed exactly",
        body: "The source-level Koide quotient from the lepton φ₀-ladder is 0.664, 0.33% below the democratic compiler target 2/3 = |ℤ₂|/N_fam. A source→pole transfer conjecture brings it onto 2/3, but is not a derivation. The relaxation now has a canonical generator — dq/dt = (Δ/N_fam)·det B(q), the gap times the anchor-block quadric, whose time-1 map is the forced Möbius attractor — and the discrete-vs-continuous question is experimental: n = 3 = N_fam transfer steps corresponds to m_τ = 1776.9427 MeV (+0.14σ; n = 2 excluded at −2.9σ), decidable at σ(m_τ) ~ 0.01 MeV.",
        formulas: [
          "Q_{\\mathrm{TFPT}} = \\frac{\\sum_\\ell \\hat m_\\ell}{(\\sum_\\ell \\sqrt{\\hat m_\\ell})^2} = 0.66446\\ldots, \\qquad Q_\\star = \\frac{|\\mathbb{Z}_2|}{N_{\\mathrm{fam}}} = \\frac{2}{3}",
          "\\frac{dq}{dt} = \\frac{\\Delta}{N_{\\mathrm{fam}}}(q-2)(q-5), \\qquad \\Delta = 6\\log\\tfrac{3}{2}, \\qquad e^{-\\Delta} = \\left(\\tfrac{2}{3}\\right)^6",
        ],
      },
      {
        title: "Dark matter — candidate fixed, scale pending",
        body: "The candidate is the determinant-line axion of the strong-CP sector; WIMPs are ruled out (no spare E₈ singlet). The misalignment angle is closed; the decay constant is a conjecture.",
        formulas: [
          "\\theta_i = \\pi(1 - \\varphi_{\\mathrm{seam}}(\\alpha_\\star)) = 170.4^\\circ",
          "f_a = \\frac{M_{\\mathrm{scal}}}{2\\dim S^+ |\\mu_4|} = \\frac{M_{\\mathrm{scal}}}{128} \\approx 2.39\\times 10^{11}\\,\\text{GeV}, \\quad m_a \\approx 23.8\\,\\mu\\text{eV}",
        ],
      },
      {
        title: "Full quantum gravity — induced from the seam",
        body: "c₃ = 1/(8π) is the gravitational seam constant; the spectral action gives R + R² structurally (G2), and the closed admissible sector is gap-decoupled from the un-built ambient (G5, Decoupling Theorem). The ambient measure (G6) is holographically reduced to a finite seam-boundary measure — the strict-TOE completion target, no longer a bulk problem.",
        formulas: [
          "2\\|V_{\\mathrm{metric}}\\| = 0.785 < \\Delta = 6\\log\\tfrac{3}{2} = 2.433, \\qquad \\Delta_{\\mathrm{eff}} = 1.648 > 0",
          "M_{\\mathrm{scal}}^2/\\bar M_{\\mathrm{Pl}}^2 = c_3^7, \\qquad M_{\\mathrm{scal}} = 3.06\\times 10^{13}\\,\\text{GeV}",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "η_B (downstream)",
        latex: "\\eta_B = 6.1\\times 10^{-10}",
        description: "From closed Ω_b h² = 0.0222; not a compiler power. [P]",
      },
      {
        label: "Koide",
        latex: "Q = 0.664 \\to Q_\\star = \\tfrac{2}{3} = \\tfrac{|\\mathbb{Z}_2|}{N_{\\mathrm{fam}}}",
        description: "Near-miss, 0.33% below 2/3; not exact at source. [P]",
      },
      {
        label: "Axion DM",
        latex: "f_a = M_{\\mathrm{scal}}/128, \\quad m_a \\approx 23.8\\,\\mu\\text{eV}",
        description: "Candidate fixed, θ_i = 170° closed; f_a conjectural. [P/A]",
      },
      {
        label: "QG gap-decoupling",
        latex: "\\Delta_{\\mathrm{eff}} = \\Delta - 2\\|V\\| = 1.648 > 0",
        description: "R + R² grounded (G2); ambient measure (G6) open. [F/A]",
      },
    ],
    highlights: [
      { label: "η_B", value: "6.1×10⁻¹⁰", description: "Downstream readout from Ω_b h² [P]" },
      { label: "Koide Q", value: "0.664", description: "0.33% below 2/3 = |ℤ₂|/N_fam [P]" },
      { label: "m_a", value: "≈ 23.8 µeV", description: "Axion candidate; f_a = M_scal/128 [P]" },
      { label: "m_p/m_e", value: "open [A]", description: "Cross-sector ratio, not a compiler power" },
    ],
  },
  {
    id: "05",
    number: 5,
    slug: "horizon-readouts",
    title: "Appendix H — The Horizon Unit System",
    subtitle: "One seam constant c₃ = 1/(8π) as the universal horizon thermal code",
    abstract:
      "A change of bookkeeping, not new gravitational physics: if gravity is the geometry-channel readout of the seam, then all horizons read the same boundary constant c₃ = 1/(8π). This note collects the readouts — Hawking, de Sitter and Unruh temperature, black-hole thermodynamics, the Page time, scrambling, the Nariai bound, v_GW = c and cosmic birefringence — in seam units, with two genuine compiler fingerprints (1920 = |W(D₅)|, |μ₄| = 4).",
    status: "horizon",
    statusLabel: "Appendix H — reframe",
    pdf: "/papers/tfpt_horizon_readouts.pdf",
    inputs: ["The seam constant c₃ = 1/(8π) from P1, read as the horizon normaliser."],
    contribution: [
      "All horizon temperatures share one factor, 1/(2π) = 4c₃; black-hole, de Sitter and Unruh share one thermal grammar.",
      "Two genuine compiler fingerprints: 1920 = |W(D₅)| in the Hawking power, and |μ₄| = 4 in the scrambling time.",
      "The boundary transport sub-leading eigenvalue λ₂ = (2/3)⁶ governs both the SM flavor gap and the horizon Page recovery.",
    ],
    notClaimed: [
      "Nothing here is new gravitational physics — it is a reframe that exposes shared structure. The search ansätze are explicitly [A], not results.",
    ],
    falsification: [
      "As a reframe it cannot be falsified by new gravity; the compiler fingerprints (1920, |μ₄|) and the shared λ₂ fail only if the underlying lattice numbers are wrong.",
    ],
    sections: [
      {
        title: "The universal horizon temperature factor",
        body: "The factor that appears in every horizon temperature is the seam constant itself. Black holes, de Sitter and Unruh therefore share one thermal grammar.",
        formulas: [
          "\\frac{1}{2\\pi} = 4c_3, \\qquad \\frac{1}{8\\pi} = c_3",
          "T_{\\mathrm{hor}} = 4c_3\\,\\frac{\\hbar\\kappa}{c\\,k_B}",
        ],
      },
      {
        title: "Schwarzschild thermodynamics in four c₃-lines",
        body: "Temperature, entropy, power and lifetime all read off c₃, with the Hawking power denominator carrying the compiler fingerprint 1920 = |W(D₅)| (the Weyl group order of D₅).",
        formulas: [
          "T_H = \\frac{c_3}{M}, \\quad S_{BH} = \\frac{M^2}{2c_3}, \\quad P_H = \\frac{c_3}{1920\\,M^2}, \\quad \\tau_{\\mathrm{evap}} = \\frac{640}{c_3}M^3",
          "1920 = |W(D_5)|",
        ],
      },
      {
        title: "Page time and scrambling",
        body: "The Page time is a fixed fraction of the evaporation time, and the scrambling time carries the second fingerprint |μ₄| = 4. The Page-recovery kernel decays at the same λ₂ = (2/3)⁶ that sets the SM flavor gap.",
        formulas: [
          "t_{\\mathrm{scr}} \\sim |\\mu_4|\\,M\\log S, \\qquad |\\mu_4| = 4",
          "I_n \\sim \\lambda_2^{\\,n} = (2/3)^{6n}, \\qquad \\Delta_{\\mathrm{gap}} = -\\log(2/3)^6 = 6\\log\\tfrac{3}{2}",
        ],
      },
      {
        title: "De Sitter, Nariai and cosmic birefringence",
        body: "The de Sitter entropy and the cosmic-birefringence angle are the same seam readouts; v_GW = c follows with no measurable dispersion.",
        formulas: [
          "S_{dS} = \\frac{e^{2\\alpha^{-1}}}{128\\,c_3^4} = 32\\pi^4 e^{2\\alpha^{-1}} \\approx 3.32\\times 10^{122}",
          "\\beta_{\\mathrm{rad}} = \\frac{\\varphi_0}{4\\pi} \\approx 0.2424^\\circ, \\qquad v_{\\mathrm{GW}} = c",
        ],
      },
      {
        title: "The maximal black hole is the anchor (SdS in seam units)",
        body: "Put a black hole into the de Sitter bulk: at the maximal (Nariai) mass the horizon cubic has roots (1,1,−2) — exactly the traceless projection of the anchor a = (1,1,2) — and the total entropy bound is exactly the Koide branch value 2/3 = |ℤ₂|/N_fam (each horizon carries S_dS/3). The interpolation is (x²+1)/Φ₃(x) with the N_fam cyclotomic; the three-root entropy total |ℤ₂|·S_dS is conserved for every mass; the mass line is itself a split double cover whose deck involution is the horizon swap; and evaporation always flows away from the anchor point — the same repeller/attractor orientation as the flavor relaxation. Six independent landings on already-load-bearing atoms, zero free parameters; the carrier-in-the-bulk reading stays [P].",
        formulas: [
          "t^3 - 3t + 2 = (t-1)^2(t+2), \\qquad \\frac{S_{\\mathrm{Nariai}}}{S_{dS}} = \\frac{2}{3} = \\frac{|\\mathbb{Z}_2|}{N_{\\mathrm{fam}}}",
          "\\frac{S_{\\mathrm{tot}}}{S_{dS}} = \\frac{x^2+1}{x^2+x+1}, \\qquad \\mathrm{disc} \\propto (1-3m)(1+3m)",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Universal factor",
        latex: "\\tfrac{1}{2\\pi} = 4c_3, \\qquad T_H = c_3/M",
        description: "One seam constant behind every horizon temperature. [I]",
      },
      {
        label: "Hawking fingerprint",
        latex: "P_H = \\frac{c_3}{1920\\,M^2}, \\quad 1920 = |W(D_5)|",
        description: "Compiler Weyl-group order in the Hawking power. [I]",
      },
      {
        label: "Shared transport",
        latex: "\\lambda_2 = (2/3)^6",
        description: "Same eigenvalue fixes flavor gap and Page recovery. [I]",
      },
    ],
    highlights: [
      { label: "Factor", value: "1/(2π) = 4c₃", description: "Universal horizon temperature factor" },
      { label: "Hawking", value: "1920 = |W(D₅)|", description: "Compiler fingerprint in the power" },
      { label: "S_dS", value: "≈ 3.32×10¹²²", description: "De Sitter entropy from the Λ closure" },
      { label: "Nariai", value: "2/3 · S_dS", description: "Max-BH entropy bound = the Koide branch value; roots = the anchor (1,1,−2) [I]" },
      { label: "β_rad", value: "0.2424°", description: "Cosmic birefringence (ACT DR6: 0.4σ)" },
    ],
  },
  {
    id: "06",
    number: 6,
    slug: "origin-theory",
    title: "Origin Theory",
    subtitle: "The seam as a horizon, the cyclic compiler hull, and the parameter-free attractor",
    abstract:
      "Why the two TFPT inputs leave no free fundamental number. Two layers, kept strictly apart: a structural [I]/[L] core (exact, machine-checked identities) — the (g_car, N_fam) = (5,3) skeleton, the triply-forced 8 (geometry = lattice = gravity), the order-30 Coxeter cycle, one boundary transport for both flavor and horizon, and a gapped unique attractor — plus one honestly-typed [P] interpretation: the cyclic self-reproduction reading.",
    status: "synthesis",
    statusLabel: "Origin synthesis",
    pdf: "/papers/origin_theory.pdf",
    inputs: ["The single boundary pair (g_car, N_fam) = (5, 3)."],
    contribution: [
      "The whole integer skeleton from one pair: rank E₈ = g + N = 8, |ℤ₂| = g − N = 2, |μ₄| = (g+N)/2 = 4, and the Pythagorean mass volume Δ_Y = g² = N² + dim S⁺ = 9 + 16 = 25.",
      "The '8' triply forced — geometry (Gauss–Bonnet seam winding) = lattice (rank E₈) = gravity (Hawking/Einstein 8π).",
      "A gapped boundary transport (gap 6 log(3/2) > 0) ⇒ a unique Perron–Frobenius attractor: the constants are selected, not tuned.",
    ],
    notClaimed: [
      "The seam is not identical to an event horizon — it is the abstract normaliser whose local gravitational realisation is a horizon; that identification stays [P].",
      "The cyclic self-reproduction (§6) is a falsifiable interpretation [P], not derived and not machine-checkable.",
    ],
    falsification: [
      "The exact core fails if (5,3) does not generate the skeleton or the transport gap is not positive; the cyclic interpretation is falsified by a robust β = 0 or w ≠ −1.",
    ],
    sections: [
      {
        title: "The whole skeleton from one pair (5,3)",
        body: "The integer alphabet of the theory falls out of (g_car, N_fam) = (5,3): the E₈ rank, the sheet and glue counts, and the Pythagorean mass volume as a difference of squares.",
        formulas: [
          "\\operatorname{rank}E_8 = g_{\\mathrm{car}} + N_{\\mathrm{fam}} = 8, \\quad |\\mathbb{Z}_2| = g_{\\mathrm{car}} - N_{\\mathrm{fam}} = 2, \\quad |\\mu_4| = \\tfrac{g+N}{2} = 4",
          "\\Delta_Y = g_{\\mathrm{car}}^2 = N_{\\mathrm{fam}}^2 + |\\mathbb{Z}_2|\\cdot\\operatorname{rank}E_8 = 9 + 16 = 25",
        ],
      },
      {
        title: "The '8' is triply forced",
        body: "The seam denominator is fixed three independent ways. If the seam is a horizon, the gravitational 8π forces c₃; it must then coincide with the geometric 2|μ₄| (Gauss–Bonnet) and the lattice rank E₈ — all three give 8.",
        formulas: [
          "c_3 = \\frac{1}{|\\mathbb{Z}_2|\\oint_{S^2}K\\,dA} = \\frac{1}{2\\cdot 4\\pi} = \\frac{1}{8\\pi}, \\qquad 8\\pi = |\\mathbb{Z}_2|\\cdot 2\\pi\\chi(S^2)",
          "S = 4\\pi k\\,A = 2\\pi c_3\\,A = \\tfrac{1}{4}A \\iff 2\\pi c_3 = \\tfrac{1}{4}",
        ],
      },
      {
        title: "One transport for flavor and horizon",
        body: "The boundary transport spectrum {1, (2/3)⁶, (1/3)⁶} has a sub-leading eigenvalue that appears in both sectors: the SM flavor gap and the horizon Page recovery are the same number.",
        formulas: [
          "\\lambda_2 = (2/3)^6: \\quad \\Delta_{\\mathrm{gap}} = 6\\log\\tfrac{3}{2} \\;\\Longleftrightarrow\\; I_n \\sim (2/3)^{6n}",
        ],
      },
      {
        title: "The gapped unique attractor",
        body: "The transport gap is positive, so by Perron–Frobenius the operator has a unique dominant eigenvector and iterating from any start converges to the same fixed direction. Parameter-freeness is an attractor, not a tuning.",
        formulas: [
          "\\Delta = -\\log(2/3)^6 = 6\\log\\tfrac{3}{2} = 2.4328 > 0",
          "S_{dS}\\,\\rho_\\Lambda = \\frac{1}{128\\,c_3^4} = 32\\pi^4",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Pythagorean volume",
        latex: "\\Delta_Y = g^2 = N^2 + |\\mathbb{Z}_2|\\cdot\\operatorname{rank}E_8 = 9 + 16 = 25",
        description: "The whole skeleton from (5,3). [I]",
      },
      {
        label: "Triply-forced 8",
        latex: "8 = 2|\\mu_4| = \\operatorname{rank}E_8 = h(D_5)",
        description: "Geometry = lattice = gravity. [I]",
      },
      {
        label: "Gapped attractor",
        latex: "\\Delta = 6\\log\\tfrac{3}{2} > 0 \\Rightarrow \\text{unique fixed point}",
        description: "Constants selected by Perron–Frobenius, not tuned. [I/L]",
      },
      {
        label: "Area law",
        latex: "S = 2\\pi c_3\\,A = \\tfrac{1}{4}A \\iff c_3 = \\tfrac{1}{8\\pi}",
        description: "c₃ is the unique value with the Bekenstein–Hawking 1/4. [I/L]",
      },
    ],
    highlights: [
      { label: "Skeleton", value: "(5,3)", description: "One pair generates the integer alphabet" },
      { label: "Δ_Y", value: "25 = 9 + 16", description: "Pythagorean mass volume" },
      { label: "Gap", value: "6 log(3/2)", description: "Positive ⇒ unique attractor" },
      { label: "Free numbers", value: "0", description: "Only π is primitive" },
    ],
  },
  {
    id: "07",
    number: 7,
    slug: "research-contracts",
    title: "Research Contracts for the Two Open Gates",
    subtitle: "(U_wall) the parabolic flavor wall-selection · (G_metric) the full QG measure",
    abstract:
      "After the compiler closure the entire residual is Rest = (U_wall) ⊕ (G_metric) ⊕ (F_frontier). This note turns the two genuine research gates into contracts: a numbered chain of lemmas, the single theorem that closes each gate, and — for every step — whether it is machine-certifiable today. F_frontier is not a gate. Priority: (U_wall) first (finite, algebraic, falsifiable), then (G_metric) (deep analytic programme).",
    status: "contracts",
    statusLabel: "Open research gates",
    pdf: "/papers/tfpt_research_contracts.pdf",
    inputs: [
      "The closed compiler and the two named residual gates from the introduction's status card.",
    ],
    contribution: [
      "Contract 1 (U_wall) — now complete: the quark ratios are closed (Readout Rigidity) and the absolute amplitude U_point reduces to one overall scale v_geo (ratios + Grand Mass Volume) — the same dimensionful anchor as gravity's 1/G. The two [A] anchors collapse to one.",
      "Contract 2 (G_metric): IR tier closed under RP + gap (Decoupling Theorem, Δ_eff = 1.648 > 0); the ambient measure G6 is holographically reduced to a finite seam-boundary measure that is the rigorously-constructed (E₈)₁ lattice net (c = 8 = 5 + 3, conformal embedding (D₅)₁×(A₃)₁, coset c = 0) — so G6 is imported into existing RCFT/conformal-net rigor, not built anew.",
      "The quark ratio c_u/c_d = 55/117 is closed (Readout Rigidity); the '11' is the Pascal sum 16 − g_car.",
    ],
    notClaimed: [
      "U_point is not a free transcendental input but the single overall scale v_geo (shared with 1/G); the strict claim is only that one dimensionful anchor remains.",
      "The ambient boundary projective measure (G6) is reduced but not closed; it blocks certification as a strict physical TOE, but its absence does not affect the bounded IR claim.",
    ],
    falsification: [
      "Each contract names its closing theorem and certifiability; fails if a lemma certified [F] does not in fact machine-check, or if the closing theorem is asserted before its chain completes.",
    ],
    sections: [
      {
        title: "Contract 1 — (U_wall), the flavor wall",
        body: "The goal is to select the one D₄-symmetric realisation on the family curve. The selectors det R = 8 and Spec(Q₊) = {1,2,3} are read off the bundle; the quark ratio is closed by Readout Rigidity, leaving only the absolute amplitude scale.",
        formulas: [
          "\\det R = 8 = n\\cdot a, \\qquad \\operatorname{Spec}(Q_+) = \\{1,2,3\\} = 3\\alpha + 1",
          "\\frac{c_u}{c_d} = \\frac{g_{\\mathrm{car}}\\,\\|\\mathrm{Pl}(K)\\|_1}{N_{\\mathrm{fam}}^2\\,\\Delta_Q} = \\frac{5\\cdot 11}{9\\cdot 13} = \\frac{55}{117}",
        ],
      },
      {
        title: "Theorem U — the four-way split",
        body: "The remaining flavor bridge splits into four pieces: unitarity (polystable ⇒ unitary, finite linear algebra), the H2 readoff, the Λ² readout rigidity, and U_point (the full amplitude normalisation) — which now reduces to the single overall scale v_geo (the same anchor as 1/G). Gate 1 is complete.",
        formulas: [
          "(U_{\\mathrm{wall}}) = U_{\\mathrm{unitary}} + U_{\\mathrm{H2}} + U_{\\Lambda^2} + U_{\\mathrm{point}}",
          "\\|\\mathrm{Pl}(K)\\|_1 = \\textstyle\\sum_{k=0}^{2}\\binom{4}{k} = 11 = 16 - g_{\\mathrm{car}}",
        ],
      },
      {
        title: "Contract 2 — (G_metric), the QG measure",
        body: "The goal is the reflection-positive projective-limit measure over the diffeomorphism-quotiented metric sector. G2 (Seeley–DeWitt R + R²) and G5 (gap dominance, Decoupling Theorem) are certified; the projective limit G6 is now holographically reduced — because the seam is a finite causal boundary, the bulk measure is reconstructed from a finite seam-boundary (Calderón) measure, so G6 is a boundary projective limit (conditional on RP + tightness), not a diffuse bulk problem.",
        formulas: [
          "a_2 = -\\tfrac{R}{3}, \\qquad a_4\\big|_{R^2} = \\tfrac{R^2}{72}",
          "2\\|V_{\\mathrm{metric}}\\| = 0.785 < \\Delta = 6\\log\\tfrac{3}{2} = 2.433, \\qquad \\Delta_{\\mathrm{eff}} = 1.648 > 0",
        ],
      },
      {
        title: "Certifiability and order",
        body: "(U_wall) is finite, algebraic and falsifiable today; (G_metric) is a deep analytic programme. The recommended order freezes the frontier status in between.",
        formulas: [
          "(U_{\\mathrm{wall}}) \\rightarrow \\text{freeze frontier status} \\rightarrow (G_{\\mathrm{metric}})",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Gate 1 closed",
        latex: "U_{\\mathrm{point}} \\to v_{\\mathrm{geo}} = \\text{the } 1/G \\text{ anchor}",
        description: "Ratios + Grand Mass Volume ⇒ one overall scale. [I]/[A]",
      },
      {
        label: "Quark ratio closed",
        latex: "\\frac{c_u}{c_d} = \\frac{5\\cdot 11}{9\\cdot 13} = \\frac{55}{117}",
        description: "Readout Rigidity on the discrete stratum. [I]",
      },
      {
        label: "Gate 2 reduction",
        latex: "2\\|V\\| = \\tfrac{31}{4\\pi^2} < \\Delta = 6\\log\\tfrac32 \\Rightarrow \\Delta_{\\mathrm{eff}} = 1.648",
        description: "IR closed (decoupling); G6 reduced to a seam-boundary measure. [I]/[P]",
      },
    ],
    highlights: [
      { label: "Gates", value: "2", description: "(U_wall) flavor + (G_metric) quantum gravity" },
      { label: "U_point", value: "→ v_geo", description: "Gate 1 closed: the single overall scale (= 1/G anchor)" },
      { label: "c_u/c_d", value: "55/117", description: "Closed by Readout Rigidity" },
      { label: "G6", value: "→ (E₈)₁ net", description: "Reduced to the rigorously-constructed E₈ level-1 lattice net (c = 8 = 5 + 3)" },
      { label: "v_geo", value: "1 scale", description: "Dimensional-analysis floor: one scale + π; shared by flavor & gravity" },
    ],
  },
];
