import { SITE_VERSION } from "@/lib/version";

export type PaperStatus =
  | "orientation"
  | "core"
  | "synthesis"
  | "audit"
  | "frontier"
  | "redteam"
  | "horizon"
  | "contracts";

export interface Paper {
  id: string;
  number: number;
  /** Display label; companions show this instead of "Paper N". */
  label?: string;
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
  redteam: {
    label: "Adversarial audit",
    color: "text-rose-300",
    bg: "bg-rose-500/10",
    ring: "ring-rose-500/30",
    gradient: "from-rose-500 to-red-600",
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
    title: "Topological Fixed-Point Theory (TFPT) — A Discrete Compiler for the Constants of Physics",
    subtitle: "Reading guide, status assessment, and the dependency DAG",
    abstract:
      "The entry document. From two axioms — the seam constant c₃ = 1/(8π) (P1) and the carrier rank g_car = 5 (P2) — TFPT constructs a discrete compiler for the Standard-Model skeleton (gauge group, three families, hypercharges, the flavor matrix), with E₈ (D₅ ⊕ A₃ + μ₄ ⇒ E₈) as the consistency checksum. The algebraic core is machine-checkable and the dimensionless constants follow as fixed points; physical readouts (scales, masses, inflation, gravity, cosmological transfers) run through explicitly named, status-typed bridges (v_geo, G_net, F_transfer), not as free outputs. This note is the reading guide: the architecture, the predictions, the dependency DAG, and the single proof ledger.",
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
        body: `TFPT ${SITE_VERSION} closes the discrete compiler, the algebraic SM readout, the EM fixed point, the admissible gapped IR sector and the R + R² spectral-action shadow. It does not yet certify a strict physical TOE end-to-end (the seam keystone is closed only modulo a cited published theorem). The live residual is three named interfaces: one dimensionful scale anchor v_geo [O], the metric-sector inclusion G_net (now [C], closed modulo cited theorems via the keystone SEAM.EQUIV.01), and the typed runnable transfer suite F_transfer (v371–v375). The historical labels (U_wall)/(G_metric)/(F_frontier) are kept only for ledger continuity.`,
        formulas: [
          "\\underbrace{\\text{compiler}}_{\\text{closed}}\\ \\Big|\\ \\underbrace{\\text{admissible IR physics}}_{\\text{conditional (RP, gap)}}\\ \\Big|\\ \\underbrace{\\text{strict physical TOE}}_{\\text{open}}",
          "\\text{Rest} = v_{\\mathrm{geo}} \\oplus G_{\\mathrm{net}} \\oplus F_{\\mathrm{transfer}}",
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
        title: "Why this carrier: the QBL theorem chain (v108–v113)",
        body: "The seam owns exactly one measuring device — a single scalar two-point kernel — and four theorems pin what it can do. A scalar kernel exists iff it pairs the two sheets (exactly 2 = |ℤ₂| kernels = the glue ambiguity, v110); the certified channel counts the code by itself — one neutral kernel per code state, graded (1,5,10), so the Pascal closure is two countings of one set, not a condition (v112); pair transport is minimally complete — degree ≤ 1 generates nothing, degree 2 generates every code operation (v111); and the carrier net is 16 free Majorana fermions whose tower carrier → SO(16)₁ → E8₁ never changes the field content — only the certificate grows, and the central charge is the rank of the one kernel: 5 on the carrier block, 8 on the seam hull (v113). The interior is free; the structure is the certificate. Honest residue: the premise 'the seam is the free c=8 net' is the G_net gate itself — one theorem now closes both the metric story and the carrier choice — and that premise is itself no longer free-standing: it is a fixed-point theorem whose only residual factors into the already-open A2 (net existence) and GATE.QGEO, with the irreducible core {π, v_geo} a theorem (v160–v165).",
        formulas: [
          "\\text{scalar kernel exists} \\iff \\varepsilon\\ \\text{sheet-odd}, \\qquad \\#\\,\\text{kernels} = 2 = |\\mathbb{Z}_2|",
          "2^{g-1} = \\sum_{m\\le K}\\binom{g}{m} \\ \\text{(two countings of one set)}, \\qquad c = \\operatorname{rank}(P): \\ 5\\ \\text{carrier}, \\ 8\\ \\text{seam}",
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
        body: "The fine-structure constant is the unique positive root of a parameter-free cubic built only from c₃, the abelian coefficient (Σ L + N_Φ = 41 = 10 b₁) and the exact seam generating function. Existence and uniqueness are proved; the value lands 1.9σ from CODATA-2022. The abelian coefficient is pinned three independent ways — carrier algebra 10 b₁ = g_car·2^(g_car−2)+1 = 41, the U(1) hypercharge index, and the external RGE generator PyR@TE 3, which reproduces β_g₁ = (41/10)g₁³ verbatim (v159) — so the EM input is not a free knob.",
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
        description: "disc = ℤ₄, glue index 4, q(D₅)+q(A₃) = 2. [E]",
      },
      {
        label: "Carrier traces",
        latex: "240 = 16\\cdot 5\\cdot 3, \\qquad 248 = 240 + 8",
        description: "E₈ numbers as traces over the 3+2 carrier, not inputs. [E]",
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
        body: "The quark mass ratios are pure integer Plücker readouts on the derived selector stratum — no transcendental solve. The absolute amplitude reduces to one overall scale v_geo (ratios + Grand Mass Volume), the same dimensionful anchor as gravity's 1/G. The remaining ℤ₃ deck choice is since derived: the integer deck pairs the Q₊=1 line with the self-conjugate character 2, so the geometric boundary deck is the sheet-twisted class and the cusp exponential is excluded (v141) — GATE.QGEO keeps only its realisation premise, with no discrete freedom left — and that premise sits at its floor: the full Möbius D₄ of the seam curve matches the integer model parity by parity (ι = T_A exactly, δι = Σ; v146). The finite rigidity is now proven exactly [E]: μ₄ has cross-ratio 2 and a faithful Möbius D₄ stabiliser, H¹(ℙ¹∖μ₄) has rank N_fam = 3, and the eigenforms ω_k carry the μ₄ characters of weights (1,2,3) = the A₃ exponents = Spec(Q₊) — so only the seam-collar realisation stays open (v168). The Sheet Diamond carrying these operators is a discrete geometry with two axes (v218): the determinant is linear along the winding axis (A₃-driven, slope 6 = |R⁺(A₃)|) and quadratic along the sheet axis with curvatures (8, 6) = (rank E₈, |R⁺(A₃)|); the anchor-Plücker coordinates lift K→C→F in two exact steps (1,8,10) then (1,8,16) — the decuple A_Λ then the full spinor generation dim S⁺; and the characteristic-polynomial discriminants of Q,K,C,F factor as q(r)²·Disc(q) with squares (1,3,4,6) = (N_Φ,N_fam,|μ₄|,|R⁺(A₃)|) and kernels (13,48,65,105). No new numbers — it organises the existing operators more strictly.",
        formulas: [
          "\\frac{c_u}{c_d} = \\frac{g_{\\mathrm{car}}\\cdot 11}{N_{\\mathrm{fam}}^2\\,\\Delta_Q} = \\frac{55}{117}, \\quad \\frac{c_c}{c_s} = \\frac{34}{47}, \\quad \\frac{c_t}{c_b} = \\frac{3}{26}",
          "\\hat m_t/\\hat m_b = \\tfrac{3}{26}(\\varphi_0)^{-2} = 40.81",
        ],
      },
      {
        title: "The solar angle θ₁₂ from the seam",
        body: "Tri-bimaximal gives 1/3; the charged-lepton 1–2 misalignment is the seam ε = q(A₃)φ₀ = (3/4)φ₀, and TBM geometry gives the only previously open SM angle as a conditional derivation — 0.1% from NuFIT 6.0.",
        formulas: [
          "\\varepsilon = q(A_3)\\,\\varphi_0 = \\tfrac{3}{4}\\varphi_0 = c_3 + 36\\,c_3^4, \\qquad q(A_3) = \\frac{N_{\\mathrm{fam}}}{|\\mu_4|}",
          "\\sin^2\\theta_{12}^{\\mathrm{seed}} = \\tfrac{1}{3} - \\tfrac{2}{3}\\varepsilon = \\tfrac{1}{3} - \\tfrac{\\varphi_0}{2} = 0.306747",
        ],
      },
      {
        title: "Branch kernels select the sectors (the sheet question, closed modulo one gate)",
        body: "At the two branch points of the anchor-block double cover the block is rank 1, with integer kernels — at the carrier point the kernel is the democratic vector itself. Rank 1 forces the kernel image onto the antisymmetric direction (−1,1,0): up and down are the deck-odd pair, and the lepton pairing vanishes — the leptons sit on the ramification (Koide is leptonic). The anchor-forced cusp conjugation T_A (with a = e₂+e₃, the conjugation-symmetric vector) realises the same deck action, and the dictionary 'Q₊ grading = A₃ discriminant grading' is now derived (G = T_A·Σ acts integrally as the B₁⊕E decomposition on the cusp basis): the sheet question carries no separate [C] — its residual coincides with the one existing Q-geometry gate.",
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
        description: "Exact compiler signature any future fit must satisfy. [E]",
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
      "The atlas slice readings are audit-level [O] — a program, not a proof of new physics.",
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
        title: "E₈ slice compression: seven slices, two alphabets",
        body: "Sharper than seven separate hits: all seven 248-slices are ONE projection of just two alphabets — the anchor power sums P = (3,4,6,10) (p_n = 2+2ⁿ) and the Sheet-Diamond operator determinants (det Q,…,det F) = (3,4,8,14,20,32), which sum to 81 = N_fam⁴ (the total determinant charge of the flavour space). The K₄ edge products of P are the carrier blocks (12,18,30,24,40,60); one affine map (7,11,13)+s(3,3,3)+t(1,2,3) generates every flavour row budget; and dim E₆ = 78 = p₂(p₀+p₃). The atlas is a closed grammar over admissible invariant classes, not a shelf of trophies — exactly what the No-Free-Pattern discipline demands (v170).",
        formulas: [
          "P = (3,4,6,10),\\quad (\\det Q,\\dots,\\det F) = (3,4,8,14,20,32),\\quad \\textstyle\\sum\\det = 81 = N_{\\mathrm{fam}}^4",
          "248 = p_2\\Delta + \\det R + 81 + 81 = 78 + 8 + 81 + 81 \\quad (E_6\\times A_2)",
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
        description: "‖R‖_F² = 78 = dim E₆, det R = 8 = dim A₂. Audit-level [O].",
      },
      {
        label: "Cascade endpoints",
        latex: "\\tfrac{1}{2}D_{\\mathrm{start}}D_{\\mathrm{end}} = \\tfrac{60\\cdot 8}{2} = 240",
        description: "The old cascade is the same even-integer spine. [E]",
      },
      {
        label: "Reverse glue",
        latex: "\\mu^2 - 5\\mu + 4 = 0",
        description: "Singles out μ = 4 (A₃), g_car = 5. [E]",
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
    subtitle: "η_B, the Higgs quartic, m_p/m_e, Koide, dark matter and quantum gravity — honest status",
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
      "The axion dark-matter candidate fixed (θ_i = 170° closed), with f_a = M_scal/128 a conjecture; the local Einstein equation Gₐᵦ+Λgₐᵦ=c₃⁻¹Tₐᵦ is parameter-free (v358/v359), and the ambient QG measure is discharged as a redundancy [C] (v369+v379).",
    ],
    notClaimed: [
      "η_B as a fundamental compiler power, the absolute axion relic abundance, an exact Koide 2/3, and m_p/m_e as a compiler number are all explicitly not claimed.",
      "Hard rule: Koide, η_B, the axion relic scale and m_p/m_e are not compiler powers unless their missing QFT/cosmology transfer is supplied.",
    ],
    falsification: [
      "Fails if a frontier item is silently asserted as a forced compiler power; m_p/m_e is explicitly left open [O] and only fails if mis-asserted.",
    ],
    sections: [
      {
        title: "Baryon asymmetry η_B — downstream readout + viable transfer route",
        body: "From the closed baryon fraction Ω_b = (4π − 1)β_rad, the asymmetry follows as a cosmological readout. The fundamental leptogenesis route is now operationalised as a falsifiable interface (v169): fed by TFPT's normal-ordered neutrino spectrum and the predicted δ_CP = 240°, the thermal-leptogenesis estimate η_B ~ 0.96×10⁻²·ε₁·κ_f brackets the observed 6.1×10⁻¹⁰ over natural M₁ ∈ [3×10⁹, 3×10¹⁰] GeV and washout (a canonical point M₁ = 10¹⁰ GeV gives 6.0×10⁻¹⁰, untuned) — so the route is viable. But M₁ and the washout are scenario inputs, so η_B stays [C]: if a precise Boltzmann solve excluded the window the route falls, not the theory (the downstream Ω_b readout is independent). An anchored-Boltzmann proposal was tested honestly (v184): the washout anchors plausibly (m̃₁ = m_3/A_Λ ≈ 5 meV, A_Λ = 10 = |E(K₅)|), a cleaner alternative drops the seesaw scale entirely (v212): both Boltzmann inputs share the decuple A_Λ = 10 = |E(K₅)|, M₁ = M_scal·φ₀²/A_Λ ≈ 8.65×10⁹ GeV and m̃₁ = m₃/A_Λ ≈ 5 meV, so M₁ uses only {M_scal, φ₀, A_Λ} (no hidden seesaw scale) and lands in the thermal window where η_B ≈ 1.2×10⁻⁹ brackets the observed 6.1×10⁻¹⁰ — a sharper [C] scenario (the coupling mechanism is posited, not derived; FR.ETAB.04). By contrast the older M₁ = M_R·φ₀⁴ only relocates the free input — M_R is the seesaw scale ~v²/m_3 (the nearest clean TFPT powers of M̄_Pl miss it by ~40–75%), not a compiler power — so the proposal cuts the free inputs from two to one, not to zero. The full BDP Boltzmann ODE solve now confirms the route at the frozen M₁: integrated κ_f = 0.092 gives η_B = 6.5×10⁻¹⁰ = 1.07× the observed value with no free M_R dial (the full flavored density-matrix solve is the next refinement) — so η_B moves from 'solve pending' to a consistent [C] downstream readout, not a derivation.",
        formulas: [
          "\\Omega_b = (4\\pi - 1)\\beta_{\\mathrm{rad}} = 0.04894, \\qquad \\Omega_b h^2 = 0.0222",
          "\\eta_B = 6.09\\times 10^{-10} \\quad (\\text{observed } 6.1\\times 10^{-10})",
          "\\eta_B \\sim 0.96\\times 10^{-2}\\,\\varepsilon_1\\,\\kappa_f, \\qquad \\varepsilon_1 = \\tfrac{3}{16\\pi}\\tfrac{M_1 m_3}{v^2}",
        ],
      },
      {
        title: "Higgs quartic — near-criticality from the free seam",
        body: "The seam UV is the free chiral c=8 fixed point, so the one marginal SM scalar coupling vanishes there: λ(M_seam) = 0 and β_λ(M_seam) = 0 — the Shaposhnikov–Wetterich double criticality, here derived from the free seam, not assumed. Running the PyR@TE-confirmed two-loop SM RGEs from M_Z up with the measured (m_H, m_t) gives λ(M̄_Pl) ≈ 0.002 with β_λ ≈ 0 — the celebrated Standard-Model near-criticality, now explained as a consequence of the free seam. The double condition predicts m_H ≈ 129–134 GeV (measured 125.25 sits a few GeV below, the known slight metastability); the same condition at the scalaron scale gives ≈107 GeV (too low), so the boundary condition lives at the Planck scale — consistent with seam = horizon = Planck (v166).",
        formulas: [
          "\\lambda(M_{\\mathrm{seam}}) = 0, \\qquad \\beta_\\lambda(M_{\\mathrm{seam}}) = 0 \\ \\text{(free seam)}",
          "\\lambda(\\bar M_{\\mathrm{Pl}}) \\approx 0.002, \\qquad m_H \\approx 129\\text{–}134\\ \\mathrm{GeV}",
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
        body: "The candidate is the determinant-line axion of the strong-CP sector; WIMPs are ruled out (no spare E₈ singlet). The misalignment angle is closed; the decay constant is a conjecture. A misalignment estimate (v185) and a converged FULL finite-T solve (experiments/ftransfer/axion_relic/full_finiteT_solve.py: exact nonlinear misalignment, lattice χ(T)∝T⁻⁸·¹⁶, realistic g_*(T), normalised so θ_i=1 gives the standard Ω_a h² ≈ 0.03) now decide the abundance: at the predicted θ_i ≈ 170° hilltop the relic is Ω_a h² ≈ 0.66 — ~5.5× above Ω_DM h² = 0.12 (the observed value is reached only at θ_i ≈ 106°). So as the dominant dark matter the determinant-line axion at (f_a = M_scal/128 ≈ 2.39×10¹¹ GeV, θ_i ≈ 170°) OVER-closes the universe unless there is extra dilution or a lower f_a — a confirmed tension, not the optimistic all-DM. A more robust angle is the spine branch θ_i = π·N_fam/g_car = 3π/5 = 108° (v211): the same solver reaches Ω_DM at θ ≈ 106°, and 108° (the central spine quotient 3/5, no fit) sits there in the MILD-anharmonic regime — 62° below the hilltop, so NOT exponentially sensitive. It is an alternative ansatz to θ_i = π(1−φ_seam) ≈ 170° (mutually exclusive, the full solver decides, DM.AXION.SPINE.01) — a sharper [C] scenario, not a derivation; a converged Ω_a h² outside ~[0.08, 0.16] demotes the branch.",
        formulas: [
          "\\theta_i = \\pi(1 - \\varphi_{\\mathrm{seam}}(\\alpha_\\star)) = 170.4^\\circ",
          "f_a = \\frac{M_{\\mathrm{scal}}}{2\\dim S^+ |\\mu_4|} = \\frac{M_{\\mathrm{scal}}}{128} \\approx 2.39\\times 10^{11}\\,\\text{GeV}, \\quad m_a \\approx 23.8\\,\\mu\\text{eV}",
        ],
      },
      {
        title: "The muon anomalous magnetic moment — a seam vertex readout",
        body: "A [C] downstream readout (archive integration), not a compiler power. The carrier carries a second-order topological defect beyond the one that fixes α: δ₂ = Bγ·δ_top² = (5/4)δ_top² (δ_top = Ω_adm c₃⁴ = 48c₃⁴ = 3/(256π⁴); Bγ = (3/2)(5/6) = 5/4 the carrier compression quotient). Projected through the seam-loop phase 2π (the same 1/(2π) = 4c₃ unit that normalises c₃ itself), it reads as a magnetic vertex correction a_μ^seam = δ₂/(2π) = 45/(524288 π⁹) ≈ 2.879×10⁻⁹. The value is an exact compiler number (trace reading δ₂ = 4!·Tr_{S⁺}(X²)·c₃⁸, Tr = 120 = 5!) — but the identification of δ₂/(2π) as the anomalous moment is a physical bridge, so the prediction is [C]. Data, honestly: 0.81σ vs the dispersive Δa_μ = (2.49±0.48)×10⁻⁹; lattice/CMD-3 HVP shrinks the discrepancy (~1.5×10⁻⁹), where the fixed value then sits ~1.5σ high. A converged Δa_μ outside 2.879×10⁻⁹±0.5×10⁻⁹ excludes the seam-vertex mechanism (compiler core untouched).",
        formulas: [
          "a_\\mu^{\\mathrm{seam}} = \\frac{\\delta_2}{2\\pi} = \\frac{45}{524288\\,\\pi^9} \\approx 2.879\\times 10^{-9}",
          "\\delta_2 = B\\gamma\\,\\delta_{\\mathrm{top}}^2 = \\tfrac54\\,\\delta_{\\mathrm{top}}^2 = 4!\\,\\mathrm{Tr}_{S^+}(X^2)\\,c_3^8",
        ],
      },
      {
        title: "Full quantum gravity — induced from the seam, the field equation parameter-free",
        body: "c₃ = 1/(8π) is the gravitational seam constant; the spectral action gives R + R² structurally (G2), and the closed admissible sector is gap-decoupled from the un-built ambient (G5, Decoupling Theorem). NEW (v358/v359): beyond the R + R² action, the classical field equation is now supplied directly by the entanglement first law δS = δ⟨K⟩ (Jacobson; Faulkner et al.), run with TFPT's atoms. v358 gives the linearised G_ab = c₃⁻¹ T_ab with c₃⁻¹ = 8π FIXED; v359 upgrades this to the FULL covariant G_ab + Λ g_ab = c₃⁻¹ T_ab by demanding stationarity at fixed VOLUME, which brings in the Einstein tensor (not just Ricci; trace g^{ab}G_ab = (1−d/2)R = −R in d=4) — the unique divergence-free tensor (Lovelock), so matter conservation ∇ᵃT_ab = 0 is an output. BOTH coefficients are TFPT-fixed: 8π = 1/c₃ (no free Newton dial; the thermodynamic origin 2π/η equals the geometric |Z₂|·2π·χ iff |μ₄| = |Z₂|·χ = 4, so c₃ is triply over-determined — anchor v23, geometry v58, thermodynamics v358) and Λ from α (ρ_Λ = (3/4π²)e^{−2α⁻¹}, v60). The matter flux is the Casini–Huerta–Myers ball modular Hamiltonian (boost via Bisognano–Wichmann v323) and the entropy density is atom-fixed (1/4 = 1/|μ₄|, central charge c = g_car + N_fam = 8). So B6's full covariant field equation is parameter-free at the local level; the equation-of-state status and the absolute scale v_geo remain, while the global ambient measure (G6 / QG.AMB.01) is now discharged as a redundancy [C] (v369+v379) — a certification object, not missing dynamics, conditional on SEAM.EQUIV.01 + Bisognano–Wichmann — and the R²/Weyl² Stelle ghost is a Seeley–DeWitt truncation artefact, so perturbative spin-2 graviton unitarity is established [C] (v304/v370/v380). Plus three archive readouts: (i) an INDEPENDENT gravitational 3/4 — ξ = c₃/φ_tree = 3/4 = q(A₃) = ln(m/μ) (v152); (ii) a Hubble value from the Λ branch ⇒ H₀ = 66.5–67.1 km/s/Mpc (the Hubble tension is NOT relieved), a [C] readout; (iii) a [P] FRG cross-check with a non-Gaussian UV fixed point.",
        formulas: [
          "G_{ab} = c_3^{-1} T_{ab} = 8\\pi\\, T_{ab}\\quad(\\text{parameter-free}),\\qquad \\tfrac{2\\pi}{\\eta} = |\\mathbb{Z}_2|\\,2\\pi\\,\\chi \\iff |\\mu_4| = |\\mathbb{Z}_2|\\chi = 4",
          "2\\|V_{\\mathrm{metric}}\\| = 0.785 < \\Delta = 6\\log\\tfrac{3}{2} = 2.433, \\qquad \\Delta_{\\mathrm{eff}} = 1.648 > 0",
          "M_{\\mathrm{scal}}^2/\\bar M_{\\mathrm{Pl}}^2 = c_3^7, \\qquad M_{\\mathrm{scal}} = 3.06\\times 10^{13}\\,\\text{GeV}",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "η_B (downstream)",
        latex: "\\eta_B = 6.1\\times 10^{-10}",
        description: "From closed Ω_b h² = 0.0222; not a compiler power. [C]",
      },
      {
        label: "Koide",
        latex: "Q = 0.664 \\to Q_\\star = \\tfrac{2}{3} = \\tfrac{|\\mathbb{Z}_2|}{N_{\\mathrm{fam}}}",
        description: "Near-miss, 0.33% below 2/3; not exact at source. [C]",
      },
      {
        label: "Axion DM",
        latex: "f_a = M_{\\mathrm{scal}}/128, \\quad m_a \\approx 23.8\\,\\mu\\text{eV}",
        description: "Candidate fixed, θ_i = 170° closed; f_a conjectural. [C]/[O]",
      },
      {
        label: "QG gap-decoupling",
        latex: "\\Delta_{\\mathrm{eff}} = \\Delta - 2\\|V\\| = 1.648 > 0",
        description: "Local Einstein eq parameter-free (v358/v359); R + R² grounded (G2); ambient measure (G6/QG.AMB.01) discharged as redundancy (v369+v379). [E]/[C]",
      },
    ],
    highlights: [
      { label: "η_B", value: "6.1×10⁻¹⁰", description: "Downstream readout from Ω_b h² [C]" },
      { label: "Koide Q", value: "0.664", description: "0.33% below 2/3 = |ℤ₂|/N_fam [C]" },
      { label: "m_a", value: "≈ 23.8 µeV", description: "Axion candidate; f_a = M_scal/128 [C]" },
      { label: "muon a_μ", value: "2.879×10⁻⁹", description: "Seam vertex δ₂/(2π); 0.81σ dispersive [C]" },
      { label: "m_p/m_e", value: "open [O]", description: "Cross-sector ratio, not a compiler power" },
    ],
  },
  {
    id: "05",
    number: 5,
    slug: "redteam",
    title: "Red Team — The Adversarial Audit",
    subtitle: "Targets A–E: attacking the five load-bearing reductions at their weakest transitions",
    abstract:
      "The deliberately adversarial layer: instead of confirming TFPT, this document attacks the six load-bearing reductions (Targets A–F) at their weakest logical transitions. Each target runs through one fixed protocol — minimal statement, assumptions, logical chain, counterexample search, limiting cases, alternative structures, verdict. A red-team check asserts an adversarial fact (a counterexample really exists, a hidden assumption is really needed, a firewall really holds); the honest outcome lives in the status of each target, never in a green pass. Verdicts: A reduced (one residual), B/D/E/F survive narrowed, C survives; none broken. Target F audits the perturbative-QFT + scale round (v269–v275): the two attacks that landed are now resolved — the R²/Weyl² gravity Stelle ghost is a Seeley–DeWitt truncation artefact (the untruncated KMS spectral-action Hessian is entire and zero-free, so resummation decouples it ⇒ perturbative spin-2 graviton unitarity established [C], v304/v370/v380), and the anchor over-determination is conditional on the Λ-branch — both folded back into v269/v274. The ambient QG.AMB.01 measure is itself discharged as a redundancy [C] (v369+v379), a certification object rather than a nonperturbative frontier.",
    status: "redteam",
    statusLabel: "Adversarial audit",
    pdf: "/papers/tfpt_5_redteam.pdf",
    inputs: [
      "The five load-bearing reductions of the document set, treated as hostile witnesses.",
      "The red-team scripts redteam/rt_A_e8net.py … rt_F_qft4d.py + run_redteam.py.",
    ],
    contribution: [
      "Target A (seam–Calderón = (E8)₁ net): reduced to ONE residual — boundary-net holomorphy + c = 8 (⇔ the index-4 inclusion); E₈ and bulk uniqueness then follow (v83/v87/v89). The free-bulk premise is a fixed-point theorem (quasi-free ⇒ κ₂ₙ=0) and the infinite Schwinger cone is eliminated (cone gap = one-particle gap (2/3)⁶), so the reduction adds no new open content. Net existence and full-cone reflection positivity are discharged to [E] (the CAR second-quantisation functor reduces full-cone RP for every mode to the one-particle contraction, verified on the complete 2¹⁶-dim Fock space; v175), and A2 is an assembled, verified (E₈)₁ certificate. The seam realisation is the keystone SEAM.EQUIV.01 — the raw RP seam IS the holomorphic (E₈)₁ net at τ=i — now closed modulo cited theorems: an explicit gapped lattice model (v367/v368) and the S3 closure stack (v376–v379) pin the target at every computable level, Lean-pinned (FORM.SEAM.MMST.01) to the published MMST/Adamo theorems, leaving [O] = the cited continuum scaling-limit existence only (v336). Its conformal-deck face QGEO.SYM.01 is a corollary (v335). The full sprint-by-sprint reduction (v176 → v302) is recorded on the /changelog page and in the research contracts.",
      "Target B (g_car = 5 Pascal selection): survives narrowed — residual = the degree-2 truncation (Quadratic Boundary Locality), since tied to the boundary-net premise (v108–v113).",
      "Target C (k = c₃/2, S = A/4): survives — the only anchor is the UV-sensitive absolute 1/G.",
      "Targets D/E (one scale v_geo): survive narrowed — CP phases and the EW/reheating/leptogenesis scales are explicitly outside v_geo.",
    ],
    notClaimed: [
      "No target is closed by this layer; 'survives' means the statement stands as worded, not that its residual is gone.",
      "A fourth verdict, 'broken', is reserved for an actual failure — none occurred, and that is reported as a fact, not a proof.",
    ],
    falsification: [
      "Each target carries explicit kill tests; the layer is built so it MAY downgrade a claim on re-run when data or counterexamples move.",
    ],
    sections: [
      {
        title: "Method — three honest verdicts",
        body: "Each reduction is treated as a hostile witness under one fixed protocol. Allowed outcomes: survives (stands as worded), survives narrowed (stands only after a silent assumption is made explicit), reduced not closed (the conservative wording is correct). A confirmatory script that always passes is worthless here.",
      },
      {
        title: "Target A — the (E8)₁ boundary-net identification",
        body: "Level-1 primary counting (det Cartan: D₈ has 4, E₈ has 1) makes holomorphy necessary AND sufficient — a holomorphic c = 8 chiral CFT is the lattice theory of the unique even unimodular rank-8 lattice. Bulk uniqueness is not independent: for a holomorphic net Rep(A) = Vect, so the bulk pairing is unique (machine contrast: SO(16)₁ admits six modular invariants). Target A therefore collapses to one residual that carries no new open content: the free-bulk premise is a fixed-point theorem (v160), the infinite Schwinger cone is eliminated since the cone gap equals the one-particle gap (2/3)⁶ (v161/v162), and the irreducible core {π, v_geo} is a theorem (v165). Net existence and full-cone reflection positivity are discharged to [E] on the complete 2¹⁶-dim Fock space (the CAR second-quantisation functor reduces full-cone RP for every mode to the one-particle contraction; v175), and A2 is an assembled, verified (E₈)₁ certificate (E₈ Cartan even unimodular, det 1). The seam realisation is the keystone SEAM.EQUIV.01 (the raw RP seam IS the holomorphic (E₈)₁ net at τ=i), now closed modulo cited theorems: an explicit gapped lattice model (v367/v368) and the S3 closure stack (v376–v379) pin the target at every computable level, Lean-pinned (FORM.SEAM.MMST.01) to the published MMST/Adamo theorems, leaving [O] = the cited continuum scaling-limit existence only (v336). Its conformal-deck face QGEO.SYM.01 is a corollary (v335). The step-by-step reduction (v160 → v302) lives on the /changelog page, not here.",
        formulas: [
          "c(E_8)_1 = \\tfrac{248}{31} = 8, \\quad c(D_5)_1 = 5, \\quad c(A_3)_1 = 3, \\quad c_{\\mathrm{coset}} = 0",
        ],
      },
      {
        title: "Targets B–E — narrowed, with named residuals",
        body: "B: the Pascal ladder 2^{g−1} = Σ_{k≤2} C(g,k) is exactly equivalent to the degree-2 truncation; the residual is the QBL premise, since merged with the boundary-net gate. C: the replica chain is derived; the absolute 1/G stays the one anchor. D: the frozen CP phase survives at +0.98σ with a decision threshold σ_γ ≤ 0.96°. E: v_geo carries the dimensionless theory; EW/reheating scales are typed interfaces.",
      },
      {
        title: "Follow-up rounds — the residual count is monotone",
        body: "Machine-checked follow-up rounds moved Target A from three residuals to the single named keystone SEAM.EQUIV.01 and hardened the firewalls (numerology null test: P ≤ 10⁻³⁰·⁷ conditional on the declared grammar). This document states the current reduction; the dated round-by-round development lives on the /changelog page.",
      },
    ],
    keyFormulas: [
      {
        label: "Target A residual",
        latex: "\\text{holomorphy} + c = 8 \\;\\Leftrightarrow\\; [\\mathcal{B} : \\mathcal{A}] = 4 = |\\mu_4|",
        description: "One statement; E₈ and the unique 2D bulk follow. (A) factors into the A2 net-existence + the keystone SEAM.EQUIV.01, now closed modulo cited theorems (lattice v367/v368 + S3 stack v376–v379; residual [O] = the cited continuum existence, v336). [C]",
      },
      {
        label: "Same-c rival excluded",
        latex: "(D_8)_1 = SO(16)_1: \\; 4 \\text{ primaries}, \\quad E_8: \\; 1",
        description: "Holomorphy excludes the only same-c competitor. [E]",
      },
    ],
    highlights: [
      { label: "Targets", value: "A–E", description: "Five load-bearing reductions, attacked" },
      { label: "Broken", value: "0", description: "No target failed; verdicts are typed, not green" },
      { label: "Target A", value: "closed mod cited", description: "Factors into the A2 net assembly + the keystone SEAM.EQUIV.01, now [C] closed modulo cited theorems (lattice v367/v368 + S3 stack v376–v379, residual = cited continuum existence v336)" },
      { label: "Target D CP", value: "triality + sheet", description: "Both CP phases are the universal Z₃ triality phase, split only by the Z₂ sheet (v231/v233) — the power choice is removed" },
    ],
  },
  {
    id: "06",
    number: 6,
    label: "Appendix H",
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
      "Nothing here is new gravitational physics — it is a reframe that exposes shared structure. The search ansätze are explicitly [O], not results.",
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
        body: "Temperature, entropy, power and lifetime all read off c₃, with the Hawking power denominator carrying the compiler fingerprint 1920 = |W(D₅)| (the Weyl group order of D₅). The temperature is not put in by hand: the stationary exterior modular flow Δ^{it} = e^{−2πtK_H} (Bisognano–Wichmann / Tomita–Takesaki) makes the outside state KMS at inverse temperature 2π, so T_H = κ/(2π) — and that 2π is the seam unit 1/(4c₃), reproducing T_H = c₃/M (the seam = horizon modular identification ties to [ρ,Λ_Σ] = 0). The induced R + R² scalaron then corrects the area law to the Wald entropy S_W = (A/4G)(1 + R_h/3M_s²), an exact consequence of f(R) = R + R²/(6M_s²); the leading A/4G is the c₃ area law (1/4 = 1/|μ₄|). [E] for the identities; the black-hole/modular identification is [C].",
        formulas: [
          "T_H = \\frac{c_3}{M}, \\quad S_{BH} = \\frac{M^2}{2c_3}, \\quad P_H = \\frac{c_3}{1920\\,M^2}, \\quad \\tau_{\\mathrm{evap}} = \\frac{640}{c_3}M^3",
          "T_H = \\frac{\\kappa}{2\\pi}, \\quad 2\\pi = \\frac{1}{4c_3}, \\qquad S_W = \\frac{A}{4G}\\Bigl(1 + \\frac{R_h}{3M_s^2}\\Bigr)",
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
        body: "The de Sitter entropy and the cosmic-birefringence angle are the same seam readouts; v_GW = c follows with no measurable dispersion. The defect reading of the black-hole interior: in compiler units it is not a curvature blow-up but the seam attractor — the same gapped transport whose sub-leading eigenvalue is λ₂ = (2/3)⁶ drives φ → φ_⋆ (dφ/dt = 0), so 'ρ → ∞' is replaced by a fixed point; information returns through the same Page-recovery channel; and the end state is a holographic Planck-scale floor (S_BH = A/4, one cell per |μ₄| = 4 Planck areas), not a point. A [C] structural reading — the old RN/torsion-charge metric is not resurrected, it is superseded by the Nariai/seam = horizon anchor.",
        formulas: [
          "S_{dS} = \\frac{e^{2\\alpha^{-1}}}{128\\,c_3^4} = 32\\pi^4 e^{2\\alpha^{-1}} \\approx 3.32\\times 10^{122}",
          "\\beta_{\\mathrm{rad}} = \\frac{\\varphi_0}{4\\pi} \\approx 0.2424^\\circ, \\qquad v_{\\mathrm{GW}} = c",
        ],
      },
      {
        title: "The maximal black hole is the anchor (SdS in seam units)",
        body: "Put a black hole into the de Sitter bulk: at the maximal (Nariai) mass the horizon cubic has roots (1,1,−2) — exactly the traceless projection of the anchor a = (1,1,2) — and the total entropy bound is exactly the Koide branch value 2/3 = |ℤ₂|/N_fam (each horizon carries S_dS/3). The interpolation is (x²+1)/Φ₃(x) with the N_fam cyclotomic; the three-root entropy total |ℤ₂|·S_dS is conserved for every mass; the mass line is itself a split double cover whose deck involution is the horizon swap; and evaporation always flows away from the anchor point — the same repeller/attractor orientation as the flavor relaxation. Six independent landings on already-load-bearing atoms, zero free parameters; the carrier-in-the-bulk reading stays [C].",
        formulas: [
          "t^3 - 3t + 2 = (t-1)^2(t+2), \\qquad \\frac{S_{\\mathrm{Nariai}}}{S_{dS}} = \\frac{2}{3} = \\frac{|\\mathbb{Z}_2|}{N_{\\mathrm{fam}}}",
          "\\frac{S_{\\mathrm{tot}}}{S_{dS}} = \\frac{x^2+1}{x^2+x+1}, \\qquad \\mathrm{disc} \\propto (1-3m)(1+3m)",
        ],
      },
      {
        title: "One orientation: the anchor is the stationary repeller (both sectors)",
        body: "The flavor relaxation is the gradient flow of a cubic potential whose critical points are exactly the two branch points, with stationary curvatures ±Δ (the transfer gap) and a constant Lyapunov rate Δ. The SdS entropy functional has the Nariai/anchor point as its unique stationary point with curvature 2/9 = |ℤ₂|/N_fam², and evaporation ascends the entropy away from it. Both sectors flow away from an anchor-stationary configuration with grammar-constant curvatures; reading this as one variational principle of the seam stays [C], with the disanalogies recorded honestly.",
        formulas: [
          "V''(q{=}2) = +\\Delta, \\quad V''(q{=}5) = -\\Delta, \\qquad \\frac{d(-\\ln\\rho)}{dt} = \\Delta",
          "\\Bigl(\\frac{S_{\\mathrm{tot}}}{S_{dS}}\\Bigr)''(x{=}1) = \\frac{2}{9} = \\frac{|\\mathbb{Z}_2|}{N_{\\mathrm{fam}}^2}",
        ],
      },
      {
        title: "The trisection normal form — the canonical coordinate exists",
        body: "The SdS horizon cubic is uniformized by angle trisection (r = 2cos θ turns it into cos 3θ = −3m; the ℤ₃ trisection deck is the triality of coker Q = ℤ/N_fam). In the centered angle the mass is a pure cosine, m = cos(ψ)/N_fam, and the entropy collapses to ONE cosine of glue atoms with canonical curvature (2/3)³ at the anchor — the Koide constant to the family power. The invariant slope dσ/dm at Nariai is −8/9 = −rank E₈/N_fam². The flavor invariant is a rate, (2/3)^{2N_fam} per transport step; the gravity invariant is a curvature, (2/3)^{N_fam}: same base, exponent ratio |ℤ₂|. The gravity-side clock asked for here has since been constructed (v124–v133, sections below): one clock, two known geometries — the identification reading stays [C].",
        formulas: [
          "\\frac{S_{\\mathrm{tot}}}{S_{dS}} = \\frac{4}{3} - \\frac{2}{3}\\cos\\frac{2\\psi}{3}, \\qquad m = \\frac{\\cos\\psi}{N_{\\mathrm{fam}}}",
          "\\sigma''(0) = \\Bigl(\\frac{2}{3}\\Bigr)^{3}, \\qquad \\frac{d\\sigma}{dm}\\Big|_{N} = -\\frac{8}{9} = -\\frac{\\mathrm{rank}\\,E_8}{N_{\\mathrm{fam}}^2}",
        ],
      },
      {
        title: "The classical clock speaks anchor — and the honest (2/3)-test",
        body: "The classical half of the clock question is pure GR: linearizing around the Nariai geometry dS₂×S², the static mode φ(ρ) = ρ solves the static-patch equation exactly with m² = −2Λ = −|ℤ₂|Λ — the exact SdS family itself pins the modulus mass (Ginsparg–Perry tower: exactly one negative mode). In Hubble units the clock's characteristic polynomial is (λ−1)(λ+2) — the anchor quadratic: its eigenvalues are the distinct anchor roots, and the Nariai cubic factors as (t−1)·χ_clock. The anchor appears a third time: configuration roots, curvature base, clock spectrum. The honest (2/3)-test is negative for the classical clock (integer eigenvalues); the quantum clock — the one-loop conversion of curvature into rate — was the remaining [C] and is resolved by the resummed-clock chain below.",
        formulas: [
          "\\chi_{\\mathrm{clock}}(\\lambda) = \\lambda^2 + \\lambda - 2 = (\\lambda-1)(\\lambda+2)",
          "m^2 = -2\\Lambda = -|\\mathbb{Z}_2|\\Lambda, \\qquad \\frac{d}{dt}\\log(\\sigma - \\tfrac{2}{3}) = 2H = |\\mathbb{Z}_2| H",
        ],
      },
      {
        title: "The resummed quantum clock (v124–v133, v144, v147)",
        body: "The quantum clock now has a closed form: rate(n) = −p₂ ln(1 − n/N_fam) — the three-level spectrum is forced by the pole at N_fam, and the bend log₃∕₂3 is its n = 2 value. Its weights are the Mehta–Seshadri parabolic weights of the exact anchor residue A₀* (v126); the geometric tail is the standard log-determinant/RPA ring resummation, one tower per hexagon site (v127); the rate is an entropy power law Γ ∝ (S/S_dS)^{p₂} in Gibbons–Hawking form (v129); the exponent p₂ = 2h follows from mode counting plus the Born rule, h = N_fam = half the zero-mode count (v130); the per-mode S^{1/2} is the zero-mode area norm ‖Y₁ₘ‖² = A/(4π) exactly (v131); and the scaling anomaly of the non-zero-mode S² determinant is exactly −2/3 = −|ℤ₂|/N_fam — the Koide constant as a spectral anomaly (v132). The ζ(0) budget computed both ways selects the reduced seam reading: per sector −2/3, total −4/3 = minus the seed gain, while the naive 4d route gives −109/45, no atom (v133). The residue of the clock question is one finite budget — the graviton/ghost heat coefficients on S²×S² [C]. The det-ratio step is since derived within the SdS family: e₂-rigidity gives r_b·r_c = 1 − Δ²/3 exactly, so the non-zero-mode determinant ratio is (1 − Δ²/3)^{4/3} with no first-order term in the horizon split (v144); the finite-weight absorption stays [C] with its obstruction stated sharply. The ring sum is now identified as the Born-squared Gaussian zero-mode integral (variance = area ratio, forced by v131), and the quantum bend log_{3/2}3 is determinant-clean — both Nariai weights share one geometry (v147); the residue is the measure identification plus one reference normalisation.",
        formulas: [
          "\\mathrm{rate}(n) = -p_2\\ln\\bigl(1 - \\tfrac{n}{N_{\\mathrm{fam}}}\\bigr), \\qquad \\Gamma_n \\propto \\Bigl(\\frac{S_n}{S_{dS}}\\Bigr)^{p_2}",
          "\\zeta(0)\\big|_{\\det'} = -\\tfrac{2}{3} = -\\tfrac{|\\mathbb{Z}_2|}{N_{\\mathrm{fam}}} \\;\\text{per sector}, \\qquad \\text{total} = -\\tfrac{4}{3}",
        ],
      },
      {
        title: "The dual anchor: the inverse flavor response is the Nariai root (v134)",
        body: "The Nariai pattern is stored inside the flavor compiler as a dual invariant: d := aᵀR⁻¹ = aᵀL⁻¹ = (−1/2, −1/2, 1), with d·1 = 0, d·a = 1 and (1,1,−2) = −2d. The invariance is structural (Sherman–Morrison): a covector is winding-invariant iff it annihilates R⁻¹1 = (1,1,−1)/4 — the anchor does, while 1, e₁ and the torsion normal n do not (the membership is special). Together (d, n) form the dual normal pair of the flavor boundary: d reads the traceless horizon structure, n reads first-generation torsion. A third, purely algebraic leg of the flavor↔horizon bridge, beside the shared clock spectrum (v126) and the entropy power law (v129) [E]; the bridge reading stays [C].",
        formulas: [
          "d := a^{\\top}R^{-1} = a^{\\top}L^{-1} = \\bigl(-\\tfrac12, -\\tfrac12, 1\\bigr), \\qquad (1,1,-2) = -2d",
          "v^{\\top}L^{-1} = v^{\\top}R^{-1} \\iff v\\cdot R^{-1}\\mathbf{1} = 0, \\qquad R^{-1}\\mathbf{1} = \\tfrac14(1,1,-1)",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Universal factor",
        latex: "\\tfrac{1}{2\\pi} = 4c_3, \\qquad T_H = c_3/M",
        description: "One seam constant behind every horizon temperature. [E]",
      },
      {
        label: "Hawking fingerprint",
        latex: "P_H = \\frac{c_3}{1920\\,M^2}, \\quad 1920 = |W(D_5)|",
        description: "Compiler Weyl-group order in the Hawking power. [E]",
      },
      {
        label: "Shared transport",
        latex: "\\lambda_2 = (2/3)^6",
        description: "Same eigenvalue fixes flavor gap and Page recovery. [E]",
      },
    ],
    highlights: [
      { label: "Factor", value: "1/(2π) = 4c₃", description: "Universal horizon temperature factor" },
      { label: "Hawking", value: "1920 = |W(D₅)|", description: "Compiler fingerprint in the power" },
      { label: "S_dS", value: "≈ 3.32×10¹²²", description: "De Sitter entropy from the Λ closure" },
      { label: "Nariai", value: "2/3 · S_dS", description: "Max-BH entropy bound = the Koide branch value; roots = the anchor (1,1,−2) [E]" },
      { label: "β_rad", value: "0.2424°", description: "Cosmic birefringence (ACT DR6: 0.4σ)" },
    ],
  },
  {
    id: "07",
    number: 7,
    label: "Origin Theory",
    slug: "origin-theory",
    title: "Origin Theory",
    subtitle: "The seam as a horizon, the cyclic compiler hull, and the parameter-free attractor",
    abstract:
      "Why the two TFPT inputs leave no free dimensionless compiler dial beyond the anchor structure and π — the one dimensionful scale v_geo and the continuous transfer physics F_transfer remain explicitly typed, not derived. Two layers, kept strictly apart: a structural [E] core (exact, machine-checked identities) — the (g_car, N_fam) = (5,3) skeleton, the triply-forced 8 (geometry = lattice = gravity), the order-30 Coxeter cycle, one boundary transport for both flavor and horizon, and a gapped unique attractor — plus one honestly-typed [C] interpretation: the cyclic self-reproduction reading. A new cyclotomic capstone makes this precise: the entire SM structural sector (the three generations, the two CP phases, the orbit/hierarchy ordering) is the cyclotomic field ℚ(ζ₃₀) with Galois group μ₄ × ℤ₂ (degree 8 = rank E₈), forced by the atoms {2,3,5}; this yields zero dimensionless free parameters ({a, π, v_geo} is the complete input) and one new falsifiable prediction — the two CP phases are Galois-locked, δ_PMNS = δ_CKM,lead + π = 240°. The same arithmetic sharpens three frontier points: the CP lock becomes a quantitative kill test (the selected node is the deck order |μ₄|, the prediction band 240° ± ~9°, currently +1.08σ vs NuFIT 6.0); Bisognano–Wichmann shows the μ₄ deck postulate is downstream of the seam being the (E₈)₁ chiral net, collapsing two open bedrock items toward one; and the minimal hypergraph substrate carrying both the E₈ skeleton and the recovery gap is a fibred product (carrier network × 3-fold family cusp = the 5×6 split).",
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
      "The seam is not identical to an event horizon — it is the abstract normaliser whose local gravitational realisation is a horizon; that identification stays [C].",
      "The cyclic self-reproduction (§6) is a falsifiable interpretation [C], not derived and not machine-checkable.",
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
        title: "The icosahedral bedrock: why the atoms are {2,3,5}",
        body: "E₈ is the exceptional top of the McKay tower of finite SU(2) subgroups (2T→Ê₆, 2O→Ê₇, 2I→Ê₈), so choosing E₈ is choosing the icosahedron. The McKay graph is built from the group: the 120 icosians close to the binary icosahedral group 2I (element orders containing the 2,3,5 axes), and its nine irreducible-representation degrees are exactly the affine-E₈ Kac marks. A backward certificate of the closed E₈, not a P2 proof. The same exceptional geometry has two complex-multiplication readings: the square modulus (j=1728) gives the EM index 41 as a Gaussian norm, the hexagonal partner (j=0) gives the scalaron 7 as an Eisenstein norm.",
        formulas: [
          "2I\\;(|2I|=120):\\;\\; \\{1,2,2,3,3,4,4,5,6\\} = \\text{affine } E_8 \\text{ marks}, \\;\\; \\textstyle\\sum d_i = 30 = h(E_8), \\;\\; \\sum d_i^2 = 120 = |R^+(E_8)|",
          "41 = N_{\\mathbb{Z}[i]}(5+4i) = 10b_1, \\qquad 7 = N_{\\mathbb{Z}[\\omega]}(3+2\\omega) = \\text{scalaron}",
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
      {
        title: "The translation clock: discrete ↔ dynamic is one clock (5 × 6)",
        body: "The bridge between the static (lattice/spectrum) data and the dynamic (recovery) data is a clock — the order-30 Coxeter element — which factorizes into two coprime hands: a static carrier ring ℤ/5 = g_car (golden √5, no rate) and a dynamic family ring ℤ/6 = 2N_fam (the recovery rate (2/3)⁶, exponent 6 = 2N_fam). The dynamic hand runs 0,1,2,3,4,5 with position 0 the conserved law (the attractor, rate 0) and 1..5 the live phases; the static hand runs 1,2,3,4,5. So '0,1,2,3,4,5' is the law-inclusive reading and '1,2,3,4,5' the live-only reading of the same clock. The arithmetic is [E]; 'the bridge is one clock' is [C] (v319).",
        formulas: [
          "\\mathbb{Z}/30 = \\underbrace{\\mathbb{Z}/5}_{\\text{static } g_{\\mathrm{car}}} \\times \\underbrace{\\mathbb{Z}/6}_{\\text{dynamic } 2N_{\\mathrm{fam}}}, \\qquad 30 = h(E_8) = g_{\\mathrm{car}}(2N_{\\mathrm{fam}}) = 5\\times 6",
          "\\mathrm{rate}(n) = -p_2\\log\\!\\big(1-\\tfrac{n}{N_{\\mathrm{fam}}}\\big):\\;\\; \\mathrm{rate}(0)=0\\;(\\text{law}),\\quad (2/3)^6 = (|\\mathbb{Z}_2|/N_{\\mathrm{fam}})^{2N_{\\mathrm{fam}}}",
        ],
      },
      {
        title: "The cyclotomic capstone: the structural sector is ℚ(ζ₃₀) + Galois μ₄ × ℤ₂",
        body: "Collecting the arithmetic arc: the affine-E₈ network spectrum carries the atoms {2,3,5} as the angles 2cos(π/k), with the golden ratio φ = 2cos(π/5) the g_car = 5 signature (v313). The static (carrier) and dynamic (recovery) data split by number field — ℚ(√5) for the 5-fold carrier vs ℚ for the rational family rates (v314) — and the order-30 Coxeter element couples them as the cyclotomic compositum ℚ(ζ₃₀), whose Galois group is exactly μ₄ × ℤ₂ of degree 8 = rank E₈ (v315). The whole SM structural sector lives there: the three generations are the μ₃ cube-root orbit (Galois-refined 1+2, the fixed one the attractor, v317) and the two CP phases the ζ₆ family-factor data (v316). The magnitude seed φ₀ itself reduces to a pure function of π, so there are zero dimensionless free parameters — {a, π, v_geo} is the complete input (v318). [E] arithmetic / [C] the raw-seam realisation closed modulo cited theorems (residual [O] = the cited MMST continuum existence only, v336).",
        formulas: [
          "\\mathbb{Q}(\\zeta_{30}) = \\mathbb{Q}(\\zeta_5)\\cdot\\mathbb{Q}(\\zeta_3), \\quad \\mathrm{Gal} = (\\mathbb{Z}/5)^\\times\\times(\\mathbb{Z}/3)^\\times = \\mu_4\\times\\mathbb{Z}_2, \\quad [\\mathbb{Q}(\\zeta_{30}):\\mathbb{Q}] = 8 = \\operatorname{rank}E_8",
          "\\varphi_0 = \\tfrac{|\\mu_4|}{N_{\\mathrm{fam}}}c_3 + \\Omega_{\\mathrm{adm}}c_3^4 = \\tfrac43 c_3 + 48 c_3^4 \\;\\Rightarrow\\; 0 \\text{ dimensionless free parameters}",
        ],
      },
      {
        title: "The Galois CP lock: a falsifiable prediction",
        body: "The arithmetic is not only descriptive — it makes a testable cross-prediction. Both leading CP phases are powers of the one hexagonal unit ρ = ζ₆ of the family factor: δ_CKM,lead = arg(ρ) = π/3 (60°) and δ_PMNS = arg(ρ⁴) = 4π/3 (240°), and since ρ⁴ = −ρ they are locked, δ_PMNS = δ_CKM,lead + π. This upgrades the previously assigned δ_PMNS = 240° to a Galois-forced relation to the leading (π/3) component of the quark phase: the quark and lepton leading CP phases are not independent. (The lock is to the structural π/3, not the full measured γ = δ_CKM,lead + 3λ² ≈ 68.7° that carries the quark transport correction — so δ_PMNS = 240°, not 248.7°.) Sharpened (v322): the selected node is fixed by the deck order, δ_PMNS = |μ₄|·δ_CKM,lead = 4·(π/3); the sub-leading correction is bounded by the quark analogue 3λ² ≈ 8.7°, so the prediction is the band 240° ± ~9°, currently +1.08σ vs NuFIT 6.0 (NO, δ_CP = 212°⁺²⁶₋₄₁) — and the nearest wrong hexagonal node (180° / 300°) is 60° away, cleanly discriminated at DUNE/Hyper-K (~5–15°). Kill test: a δ_PMNS robustly incompatible with 240° (>3σ at DUNE/Hyper-K/JUNO) falsifies the whole Galois-CP organisation (v320/v322). [E] relation / [C] phase identification / [X] kill test.",
        formulas: [
          "\\rho = \\zeta_6, \\quad \\delta_{\\mathrm{CKM}}^{\\mathrm{lead}} = \\arg\\rho = \\tfrac{\\pi}{3}, \\quad \\delta_{\\mathrm{PMNS}} = \\arg\\rho^4 = \\tfrac{4\\pi}{3}, \\quad \\rho^4 = -\\rho",
          "\\boxed{\\;\\delta_{\\mathrm{PMNS}} = |\\mu_4|\\,\\delta_{\\mathrm{CKM}}^{\\mathrm{lead}} = \\delta_{\\mathrm{CKM}}^{\\mathrm{lead}} + \\pi = 240^\\circ \\pm \\sim 9^\\circ\\;}",
        ],
      },
      {
        title: "Bisognano–Wichmann: the deck postulate is downstream of the chiral net",
        body: "One step links the two open bedrock items. The μ₄ clock is literally a geometric rotation, ρ = diag(iⁿ) = exp(i(π/2)L) with L = diag(n) the seam rotation generator, so μ₄ ⊂ U(1)_rot. For a rotation-covariant seam covariance C = f(L) the modular Hamiltonian K = log((1−C)/C) = g(L) is itself a function of L, so the modular flow commutes with all rotations and the μ₄ clock is a modular symmetry for free — the discriminator: a mere period-4 curvature preserves the clock but its flow is not geometric ([K,L] ≠ 0). This is the Bisognano–Wichmann content: given the seam is the (E₈)₁ chiral net (v308), BW/Hislop–Longo make the vacuum modular flow geometric, so QGEO.SYM.01 (ω∘ρ = ω) is downstream of SEAM.EQUIV.01 + a rotation-invariant vacuum — not an independent axiom (v323). And the rotation-invariant vacuum is itself a conformal-NET AXIOM (a chiral net's Möbius-covariant vacuum is the unique invariant positive-energy vector), so QGEO.SYM.01 is in fact a COROLLARY of SEAM.EQUIV.01 with no extra premise (v335, Lean qgeoSymIsCorollary) — the two open bedrock items collapse to ONE, now closed modulo cited theorems (lattice v367/v368 + S3 stack v376–v379). [E] construction / [C] linkage / [O] residual (= the cited MMST continuum scaling-limit existence only, v336).",
        formulas: [
          "\\rho = \\operatorname{diag}(i^n) = \\exp\\!\\big(i\\tfrac{\\pi}{2}L\\big), \\quad C = f(L) \\;\\Rightarrow\\; K = g(L), \\quad [K,L] = 0",
        ],
      },
      {
        title: "The minimal hypergraph substrate is a fibred product",
        body: "The rewrite question made concrete. The pure (2,3,5) network gives only the Coxeter skeleton and the golden 5-fold angle; the recovery rate (2/3)⁶ is provably not in its adjacency spectrum (v312). But the smallest substrate that carries everything is a product: the carrier network T_net = (A+2I)/4 (attractor = Kac marks = the E₈ skeleton) fibred by a 3-node family cusp T_cusp = diag((1−w)⁶), w ∈ {0,1/3,2/3} (spectrum {1,(2/3)⁶,(1/3)⁶}). The fibred T_net ⊗ T_cusp carries both at once: top eigenvalue 1 with eigenvector marks ⊗ (w=0) (skeleton × democratic cusp), and (2/3)⁶ as a genuine eigenvalue (network attractor × cusp subleading). This is the cyclotomic split made dynamical — substrate = carrier × family = the 30 = 5×6 of v315, with the recovery gap living entirely in the family factor. Honestly (v312) the cusp weight is still injected, not derived from the graph: a consistent realisation of the predicted product structure, not a derivation of 2/3 from a pure rewrite (v324). [E] construction / [C] reading.",
        formulas: [
          "T = T_{\\mathrm{net}} \\otimes T_{\\mathrm{cusp}}, \\quad \\operatorname{spec} \\ni 1\\ (\\text{marks}\\otimes w{=}0) \\ \\text{and}\\ (2/3)^6\\ (\\text{marks}\\otimes w{=}\\tfrac13)",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Pythagorean volume",
        latex: "\\Delta_Y = g^2 = N^2 + |\\mathbb{Z}_2|\\cdot\\operatorname{rank}E_8 = 9 + 16 = 25",
        description: "The whole skeleton from (5,3). [E]",
      },
      {
        label: "Triply-forced 8",
        latex: "8 = 2|\\mu_4| = \\operatorname{rank}E_8 = h(D_5)",
        description: "Geometry = lattice = gravity. [E]",
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
      { label: "McKay bedrock", value: "2I → Ê₈", description: "Why {2,3,5}: E₈ is the icosahedral top (marks = irrep degrees)" },
      { label: "Seam = E₈ singularity", value: "8 P¹'s", description: "du Val resolution of ℂ²/2I; link = Poincaré sphere S³/2I — a model for the seam realisation (SEAM.EQUIV.01, v232)" },
      { label: "Brieskorn capstone", value: "x²+y³+z⁵", description: "One singularity generates the skeleton: Milnor number (2-1)(3-1)(5-1)=8, monodromy = the order-30 Coxeter cycle (eigenvalues = E₈ exponents), both clocks as sub-/Galois structures (v236)" },
      { label: "CM norms", value: "41 · 7", description: "Square (Gauss) gives the EM index, hexagon (Eisenstein) the scalaron" },
      { label: "Gap", value: "6 log(3/2)", description: "Positive ⇒ unique attractor" },
      { label: "Translation clock", value: "5 × 6 = 30", description: "Static carrier hand ℤ/5 × dynamic family hand ℤ/6; 0..5 law-inclusive, 1..5 live-only (v319)" },
      { label: "Cyclotomic capstone", value: "ℚ(ζ₃₀), μ₄×ℤ₂", description: "The SM structural sector is one cyclotomic field, Galois = μ₄×ℤ₂, degree 8 = rank E₈ (v313–v318)" },
      { label: "Galois CP lock", value: "δ_PMNS = δ_CKM + π", description: "A new falsifiable prediction: the two CP phases are Galois-locked, δ_PMNS = 240° (kill test at DUNE/Hyper-K, v320)" },
      { label: "Free numbers", value: "0", description: "Zero dimensionless free parameters: {a, π, v_geo} is the complete input (v318)" },
    ],
  },
  {
    id: "08",
    number: 8,
    label: "Research Contracts",
    slug: "research-contracts",
    title: "Research Contracts for the Remaining Interfaces",
    subtitle: "v_geo · G_net · F_transfer — the live residual as numbered contracts",
    abstract:
      "After the compiler closure the live residual is Rest = v_geo ⊕ G_net ⊕ F_transfer (the historical labels U_wall / G_metric / F_frontier are kept only for ledger continuity). This note turns the open interfaces into contracts: a numbered chain of lemmas, the single theorem that closes each, and — for every step — whether it is machine-certifiable today. Priority: the selector-triangle pairings and the v_geo scale anchor first (finite, algebraic, falsifiable), then the G_net inclusion theorem (deep analytic programme); F_transfer is the downstream interface. The emergent-QFT round (v238–v261) then assembles the boundary QFT into one relative object TFPT_QFT = (A_Σ, ω_Σ, Δ_Σ, ρ, A_F, H_F, D_F, J, γ, S_rel): the finite Dirac is a covariance induction of the seam KMS state, the spectral-action cutoff is that KMS weight (f₂/f₀ = 1), and the seam, carrier-16 and E₈ live on one Kummer/K3 surface — the Modular Spectral Closure, complete modulo a single named theorem, the Seam Equivalence Theorem (SEAM.EQUIV.01): the raw RP seam state is the holomorphic (E₈)₁ boundary net at τ=i, with ambient QG kept separate.",
    status: "contracts",
    statusLabel: "Open research interfaces",
    pdf: "/papers/tfpt_research_contracts.pdf",
    inputs: [
      "The closed compiler and the three named residual interfaces (v_geo, G_net, F_transfer) from the central status card.",
    ],
    contribution: [
      "Flavor interface (historically U_wall) — reduced to the selector triangle: the dual normal pair (d,n) forces R columnwise (v136/v139), the quark ratios are closed (Readout Rigidity), and the only remainder is the absolute amplitude U_point = the one overall scale v_geo (the same dimensionful anchor as gravity's 1/G).",
      "G_net: IR tier closed under RP + gap (Decoupling Theorem, Δ_eff = 1.648 > 0); the metric sector reduces to the rigorously-constructed (E₈)₁ lattice net (c = 8 = 5 + 3, conformal embedding (D₅)₁×(A₃)₁, coset c = 0), and the ambient measure (QG.AMB.01) is discharged as a redundancy [C] (v369+v379). The closing statement is the index-4 seam-net inclusion via the keystone SEAM.EQUIV.01, now closed modulo cited theorems: an explicit gapped lattice model (v367/v368) and the S3 closure stack (v376–v379) pin the target at every computable level, Lean-pinned (FORM.SEAM.MMST.01) to the published MMST/Adamo theorems, leaving [O] = the cited continuum scaling-limit existence only (v336).",
      "The quark ratio c_u/c_d = 55/117 is closed (Readout Rigidity); the '11' is the Pascal sum 16 − g_car.",
      "Modular Spectral Closure (v258–v261): the boundary QFT is one relative object reduced to one premise. The finite Dirac is the modular/covariance induction of the seam KMS state ([D_F] = [D_Σ]⊗[K_car]); the spectral-action cutoff is that same KMS weight (f₂/f₀ = 1); and the seam (pillowcase), carrier-16 (Kummer nodes) and E₈ (H²(K3) = U³⊕E₈(−1)²) are facets of one Kummer/K3 surface. So the whole layer is QFT-complete modulo cited theorems via the single keystone SEAM.EQUIV.01 (the raw RP seam IS the holomorphic (E₈)₁ net at τ=i; its conformal-deck face QGEO.SYM.01 is now a corollary, v335), with the ambient measure QG.AMB.01 discharged as a redundancy [C] (v369+v379) — a certification object, not missing dynamics. The perturbative 4D layer is built: the spectral-action S-matrix is Epstein–Glaser-constructible with the SM one-loop β-coefficients (41/10, −19/6, −7) from the carrier content, LSZ-bridged with one-loop unitarity for matter+gauge; the R²/Weyl² gravity sector's Stelle ghost is a Seeley–DeWitt truncation artefact (the untruncated KMS spectral-action Hessian is entire and zero-free, so resummation decouples it ⇒ perturbative spin-2 graviton unitarity established [C], v304/v370/v380). The single mass anchor is over-determined (gravity = dark energy to 0.11%, v274). SEAM.EQUIV.01 is closed modulo cited theorems: an explicit gapped lattice model (v367/v368) and the S3 closure stack (v376–v379) pin the target at every computable level — Lean-pinned (FORM.SEAM.MMST.01, SeamScalingLimit.lean) to the published MMST/Adamo theorems — leaving [O] = the abstract continuum scaling-limit existence only (v336), a cited published theorem (closed modulo a cited theorem, not solved). The full sprint-by-sprint reduction (v269 → v302) lives on the /changelog page, not here.",
    ],
    notClaimed: [
      "U_point is not a free transcendental input but the single overall scale v_geo (shared with 1/G); the strict claim is only that one dimensionful anchor remains.",
      "G_net's seam keystone (SEAM.EQUIV.01) is closed modulo cited theorems, not solved — the residual is the cited continuum-existence theorem (v336); and the ambient measure QG.AMB.01 is discharged as a redundancy [C] (v369+v379), not an open hole. Neither affects the bounded IR claim — full QG closure is a certification layer, not a prerequisite for testing the SM and cosmology readouts.",
    ],
    falsification: [
      "Each contract names its closing theorem and certifiability; fails if a lemma certified [E] does not in fact machine-check, or if the closing theorem is asserted before its chain completes.",
    ],
    sections: [
      {
        title: "v_geo — the flavor interface and the one scale anchor",
        body: "The flavor interface (historically U_wall) is reduced to the selector triangle: with the dual anchor d = a·R⁻¹ and the torsion normal n, each column of R is the unique lattice point of the address box (v136/v139). The selectors det R = 8 and Spec(Q₊) = {1,2,3} are read off the bundle; the quark ratios are closed by Readout Rigidity, leaving only the absolute amplitude scale = v_geo. And v_geo is not an open gap: by the No-Unit Theorem (v153) a dimensionless compiler provably cannot select an absolute scale, so U_point ~ v_geo, 1/G ~ v_geo² and m/μ = e^{3/4} are one metrology unit in three readings — an irreducible primitive, not a missing derivation.",
        formulas: [
          "\\det R = 8 = n\\cdot a, \\qquad \\operatorname{Spec}(Q_+) = \\{1,2,3\\} = 3\\alpha + 1",
          "\\frac{c_u}{c_d} = \\frac{g_{\\mathrm{car}}\\,\\|\\mathrm{Pl}(K)\\|_1}{N_{\\mathrm{fam}}^2\\,\\Delta_Q} = \\frac{5\\cdot 11}{9\\cdot 13} = \\frac{55}{117}",
        ],
      },
      {
        title: "The selector triangle",
        body: "The dual normal pair (d, n) pins R columnwise; d = (3/2)a − 2·1 is pure anchor data (the first selector is derived), and n is the unique covector with atom pairings (2, 8, 121) on the frame (1, a, σ) of determinant 11. Frame integrality cuts this further: integer covectors form an index-11 sublattice, so the σ-pairing is forced mod 11 — and the pairing values themselves are atom identities — in the cusp frame n pairs to (6,3,5) = (p₂,p₀,e₂)(a), so BOTH dual normals are anchor data (v145/v149); the residue is one discrete assignment; the historical U_wall machinery is over-engineering for the ratios.",
        formulas: [
          "d = a^{\\top}R^{-1} = \\bigl(-\\tfrac12,-\\tfrac12,1\\bigr), \\qquad n = (5,-9,6)",
          "n\\cdot\\mathbf{1} = 2, \\quad n\\cdot a = 8, \\quad n\\cdot\\sigma = 121 = 11^2",
        ],
      },
      {
        title: "G_net — the metric-sector inclusion",
        body: "The goal is the reflection-positive projective-limit measure over the diffeomorphism-quotiented metric sector. G2 (Seeley–DeWitt R + R²) and G5 (gap dominance, Decoupling Theorem) are certified; the ambient measure is holographically reduced to a finite seam-boundary (Calderón) measure. The single closing statement is: the seam-Calderón inclusion has Jones index 4 = |μ₄| (the μ₄ simple-current extension of the carrier net), from which holomorphy and the unique (E₈)₁ bulk follow. The identification now holds at the finite Lie level: the ℤ₄-graded hull carries exact coset duality, the glue average is the carrier projector (index 4), and each sector is a single Weyl orbit — the ℂ[ℤ₄] Q-system realised in 248 dimensions (v143); the residue is scoped to the twisted (Ramond) sector (v148). Assembled, this is the Simple-Current Extension Theorem (v154): A = (D₅)₁⊗(A₃)₁ extended by the isotropic glue L = ⟨(1,1)⟩ has index |L| = 4, c = 5+3 = 8, μ(B) = μ(A)/|L|² = 16/16 = 1 ⇒ holomorphic ⇒ B ≅ (E₈)₁ — the central strict-TOE closing theorem, exact algebraically. That one identification then reduces to a single shared premise (v155): the boundary marginal of a Gaussian bulk is automatically quasi-free, so G_net's analytic core is the same 'seam is a free RP field' premise the area law (v59) and the R3 mechanism (v150/v151) already use — one physical premise, not three. And the target net is explicitly constructed and verified (v156): the Calderón/DtN operator is the free chiral dispersion ω_k = |k|, 16 Majoranas give c = 8 = 5+3, the currents are 248 = 120 + 128, and the holomorphic character E₄/η⁸ = j^{1/3} (248 at level 1) makes B ≅ (E₈)₁ a checked identity. The free-bulk premise itself reframes (v157): freeness is the rigid holomorphic c=8 fixed point — the DtN symbol is universally |k| (Lee–Uhlmann), a holomorphic c=8 theory has no marginal (1,1) deformation (no room for an interaction), and the same |Z₂| that halves 8π in c₃ is the Ramond projection giving μ=1. So premise (A) shrinks from 'prove Gaussianity' to 'the gapped flow reaches the holomorphic fixed point' — freeness forced by rigidity, not postulated. An exact operator-dimension count (v158) shows that destination is a stable, isolated fixed point: the relevant window (0,1) for bosonic deformations is empty, the dimension-1 currents are chiral, and the lowest interaction (a quartic) has dimension 2 — irrelevant. So (A) is now just a basin-of-attraction statement, with a proven stable target. The free-bulk premise (A) is then recast as a fixed-point theorem (quasi-free ⇒ all higher cumulants κ₂ₙ=0; the cone gap = the one-particle gap (2/3)⁶), and net existence and full-cone reflection positivity are discharged to [E] on the complete 2¹⁶-dim Fock space (the CAR second-quantisation functor reduces full-cone RP for every mode to the one-particle contraction; v175). The seam realisation is the keystone SEAM.EQUIV.01 (the raw RP seam IS the holomorphic (E₈)₁ net at τ=i), now closed modulo cited theorems: an explicit gapped lattice model (v367/v368) and the S3 closure stack (v376–v379) pin the target at every computable level, Lean-pinned (FORM.SEAM.MMST.01) to the published MMST/Adamo theorems, leaving [O] = the cited continuum scaling-limit existence only (v336). Its conformal-deck face QGEO.SYM.01 is a corollary (v335). The step-by-step reduction (v160 → v302) is recorded on the /changelog page, not replayed here.",
        formulas: [
          "a_2 = -\\tfrac{R}{3}, \\qquad a_4\\big|_{R^2} = \\tfrac{R^2}{72}",
          "[\\,(E_8)_1 : (D_5)_1\\times(A_3)_1\\,] = 4 = |\\mu_4|",
        ],
      },
      {
        title: "The Modular Spectral Closure — the boundary QFT as one relative object",
        body: "On top of G_net the boundary QFT is assembled and then collapsed to a single relative object. First an emergent-QFT skeleton is read off the seam dynamically: the modular flow σ_t = Δ^{it} is KMS at β=1 (Tomita–Takesaki, with the seam unit 2π = 1/(4c₃) fixing β, v239), GNS/OS reconstruction delivers the Hilbert space and a positive OS Hamiltonian H_OS = −log T with the mass gap Δ = 6log(3/2) (v240), particles are the DHR superselection sectors of the carrier anyon category (Z₄×Z₄, Gauss–Milgram returns c = 8, v241/v242), and the 2-particle S-matrix is the braiding monodromy (Haag–Ruelle, v243). Then the matter content is the carrier half-spinor: the SO(10) 16 is exactly one anomaly-free SM generation with the forced hypercharges and sin²θ_W = 3/8 (v245). The honest 4d data test fires as a kill-test — the plain SM does not unify (v246) — and is resolved natively by gauging the carrier SO(10): the E₈ hull forbids the 126 and supplies {1,10,16,45} (v247), the Pati–Salam algebra A_F = ℍ_L⊕ℍ_R⊕M₄(ℂ) gives the exact charges (v248), and the two-step run meets the scalaron scale M_PS = κM_s (v249). The 96-dim finite spectral triple (A_F, H_F, D_F, J, γ) is then built explicitly and its NCG axioms verified — reality, grading, KO-dimension 6, order-zero, first-order (holding for the SM algebra, violated for Pati–Salam exactly by the Majorana = the CCvS beyond-first-order σ mechanism), mass spectrum + seesaw (v252); the inner fluctuations give exactly one Higgs doublet, no junk, no 126 (v254); orientability/Poincaré are honestly typed (strict fail, weakened hold — a known NCG-Standard-Model feature, v256/v257). Three closures finish the layer. (i) D_F is not posited but the modular/covariance induction of the seam KMS state: with covariance C = (1+e^H)⁻¹ the one-particle modular Hamiltonian log((1−C)C⁻¹) = H exactly, so inducing the carrier covariance C_F = P_F C_Σ P_F returns the v252 operator (same spectrum, chirality-odd, Majorana = off-diagonal covariance, seesaw m_D²/M_R) — D_F is the Kasparov shadow [D_Σ]⊗[K_car], the Yukawas the readout of C_Σ (v258). (ii) The spectral-action cutoff is that same KMS weight: f(u) = e^{−u} is derived (not chosen), giving f₂/f₀ = f₄/f₂ = 1 exactly (a Gaussian control gives √π/2 ≠ 1), so κ = √((f₂/f₀) c_PS/c_grav) = √(c_PS/c_grav) loses its scheme factor and the last open cutoff input becomes a finite trace ratio over the 96-dim H_F (v259). (iii) The seam, the carrier-16 and E₈ live on one Kummer/K3 surface: the pillowcase is the elliptic-involution quotient T²/(z↦−z) (4 marks), the 16 nodes of Km(T²×T²) resolve to 16 exceptional ℙ¹'s = dim S⁺ (the carrier-16 as the square of the seam-4), and H²(K3) = U³ ⊕ E₈(−1)² carries the same E₈ the carrier glues to (v260). The assembly certificate (v261) pins the cross-consistency — one number 4 = [B:A] = |μ₄| = 2χ = |(ℤ/2)²| (index = marks = fixed points = glue order), one carrier-16 (spinor = lattice = triple), one gap 6log(3/2) (OS = recovery = Lindblad) — so the whole layer is the single relative object TFPT_QFT = (A_Σ, ω_Σ, Δ_Σ, ρ, A_F, H_F, D_F, J, γ, S_rel). The Modular Spectral Universality statement: the unique RP holomorphic index-4 KMS seam state minimises the modular clock defect, induces the 96-dim KO-6 triple, whose inner fluctuations generate the gauged Pati–Salam spectral action with the KMS cutoff. The honest sense of completeness: the boundary QFT is closed as one relative object modulo cited theorems via the single keystone SEAM.EQUIV.01 (the raw RP seam = the holomorphic (E₈)₁ net at τ=i; its conformal-deck face QGEO.SYM.01 is a corollary, v335) — pinned at every computable level by an explicit lattice model (v367/v368) and the S3 closure stack (v376–v379), Lean-pinned (FORM.SEAM.MMST.01) to the published MMST/Adamo theorems, residual [O] = the cited continuum existence only (v336) — with the ambient QG measure QG.AMB.01 discharged as a redundancy [C] (v369+v379, gap-decoupled, Δ_eff = 1.648 > 0) — not a diffuse list of open interfaces. 4D-QFT fork policy (frozen as a decision tree, v265): boundary-only is the canonical 4D reading — a 4D-GUT is NOT claimed by default (E₈ is the audit hull, SM-only unification killed, v246); carrier-native Pati-Salam is a separately-typed, falsifiable UV branch (E₈-allowed content {1,10,16,45}, no 126, sin²θ_W = 3/8, the κ band, and a proton-decay kill test — no fake τ_p window). Not an open ambiguity.",
        formulas: [
          "\\mathsf{TFPT}_{\\mathrm{QFT}} = (\\mathcal A_\\Sigma,\\,\\omega_\\Sigma,\\,\\Delta_\\Sigma,\\,\\rho,\\,A_F,\\,H_F,\\,D_F,\\,J,\\,\\gamma,\\,S_{\\mathrm{rel}})",
          "[D_F] = [D_\\Sigma]\\,\\widehat{\\otimes}_{(E_8)_1}\\,[\\mathcal K_{\\mathrm{car}}], \\qquad f = f_\\Sigma \\Rightarrow f_2/f_0 = 1",
          "4 = [B{:}A] = |\\mu_4| = 2\\chi = |(\\mathbb Z/2)^2|, \\qquad H^2(\\mathrm{K3}) = U^3 \\oplus E_8(-1)^2",
        ],
      },
      {
        title: "Certifiability and order",
        body: "The selector-triangle pairings and the v_geo scale anchor are finite, algebraic and falsifiable today; G_net is a deep analytic programme; F_transfer is the downstream interface. The recommended order freezes the frontier status in between.",
        formulas: [
          "\\text{selector pairings} \\rightarrow v_{\\mathrm{geo}} \\rightarrow G_{\\mathrm{net}}",
        ],
      },
      {
        title: "F_transfer is a typed functor, not a bag of open topics",
        body: "F_transfer = F_observable ∘ F_threshold ∘ F_RG — standard physics fed TFPT source data — with exactly four interfaces. F_pole (Koide): the 53/54 factor is an exact operator readout [E], the pole interpretation [C] (v183). F_Boltzmann (η_B): the washout anchors (m̃₁ = m_3/A_Λ); the cleanest [C] route is the scalaron-decuple branch where BOTH Boltzmann inputs share A_Λ = 10 = |E(K₅)| and η_B brackets 6.1×10⁻¹⁰ with no hidden seesaw scale (v212), still a sharper scenario, not a closure. F_relic (axion): a converged full finite-T solve at the predicted θ_i ≈ 170° hilltop OVER-produces, and the spine-angle branch θ_i = 3π/5 = π·N_fam/g_car is the sharper falsifiable [C] alternative (v211). F_QCD (m_p/m_e): a QCD matching contract [O], not a compiler number. A machine guard (v187) enforces that all four stay [C]/[O] and are never promoted to a primitive [E] compiler prediction — exact algebraic sub-parts (53/54, b₃ = −7) may be [E], the physical prediction never is. Beyond the guard, the functor contract CONTRACT.F.01 verifies four structural axioms (v213): (1) μ₄-deck equivariance — the Koide multiplier λ₂ = (2/3)⁶ = 64/729 IS the deck transfer eigenvalue; (2) Plücker preservation — 53 = aᵀ(R+Q)1 is the F-corner reading, Pl(F) = (1,22,30), ‖Pl(K)‖₁ = 11; (3) positivity/stochasticity — spec(T) = {1,(2/3)⁶,(1/3)⁶} positive, washout κ_f ∈ (0,1); (4) external modules explicit — pole transfer, the Boltzmann network, the finite-T χ(T) ODE, the lattice C_N, each named and external, never a compiler number. CONTRACT.F.01 is the third research interface alongside v_geo and G_net: a typed, RUNNABLE solver suite F_transfer = F_pole ⊕ F_Boltzmann ⊕ F_relic ⊕ F_QCD — Koide source→pole (v371), η_B washout (v372), axion relic (v373), m_p/m_e via carrier-b₃ running (v374) — each with a kill test and folded into a status-typed prediction-observatory CI (v375); the predictions stay [C], never compiler outputs. And dynamically (v303, FR.DYNAMICS.01): all four interfaces share ONE shape — a gapped, positivity-preserving relaxation to a UNIQUE attractor (Perron-Frobenius / Boltzmann H-theorem / RG fixed point), the same shape as the main-branch update m←(A+2I)/4·m → the E₈ marks. F_pole (Koide) runs it at the SEAM rate exactly (its Möbius multiplier is (2/3)⁶ = λ₂, the seam-clock eigenvalue); F_Boltzmann (thermal washout), F_relic (cosmological freeze) and F_QCD (the RG flow to the Gaussian UV fixed point, b₃=−7) share the shape with external rates. So F_transfer is the downstream readout end of the one discrete→dynamic principle, not a bolt-on; the theory's simplicity is preserved because the external rates are honestly fenced (v187), not reduced to the seam.",
        formulas: [
          "F_{\\mathrm{transfer}} = F_{\\mathrm{observable}} \\circ F_{\\mathrm{threshold}} \\circ F_{\\mathrm{RG}}",
          "\\{F_{\\mathrm{pole}},\\ F_{\\mathrm{Boltzmann}},\\ F_{\\mathrm{relic}},\\ F_{\\mathrm{QCD}}\\}",
          "\\lambda_2 = (2/3)^6 = 64/729 \\ (\\mu_4\\text{-deck transfer eigenvalue})",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Flavor interface reduced",
        latex: "U_{\\mathrm{point}} \\to v_{\\mathrm{geo}} = \\text{the } 1/G \\text{ anchor}",
        description: "Ratios + Grand Mass Volume ⇒ one overall scale. [E]/[O]",
      },
      {
        label: "Quark ratio closed",
        latex: "\\frac{c_u}{c_d} = \\frac{5\\cdot 11}{9\\cdot 13} = \\frac{55}{117}",
        description: "Readout Rigidity on the discrete stratum. [E]",
      },
      {
        label: "Gate 2 reduction",
        latex: "2\\|V\\| = \\tfrac{31}{4\\pi^2} < \\Delta = 6\\log\\tfrac32 \\Rightarrow \\Delta_{\\mathrm{eff}} = 1.648",
        description: "IR closed (decoupling); G6/QG.AMB.01 discharged as redundancy (v369+v379). [E]/[C]",
      },
    ],
    highlights: [
      { label: "Interfaces", value: "3", description: "v_geo (scale) · G_net (metric) · F_transfer (downstream)" },
      { label: "U_point", value: "→ v_geo", description: "Flavor interface reduced: the single overall scale (= 1/G anchor)" },
      { label: "c_u/c_d", value: "55/117", description: "Closed by Readout Rigidity" },
      { label: "G_net", value: "index 4", description: "Closing statement: the μ₄ index-4 seam-net inclusion ⇒ (E₈)₁; the free-bulk premise (A) factors into A2 + GATE.QGEO, zero new gates (v160–v165)" },
      { label: "v_geo", value: "1 scale", description: "Dimensional-analysis floor: one scale + π; shared by flavor & gravity" },
      { label: "One closing theorem", value: "no abelian sector", description: "P2 · G_net · Target A are ONE condition (holomorphy = homology-sphere = one 1-dim irrep, all force E₈), now closed modulo cited theorems: the target net is pinned at every computable level (lattice v367/v368 + S3 stack v376–v379), residual [O] = the cited continuum existence only (v336)" },
      { label: "CS realisation", value: "holomorphic ⇔ det K=1", description: "The closing step in abelian Chern-Simons: #anyons=|det K|; the v92 tower D5⊕A3(16)→D8(4)→E8(1) is anyon condensation = the Kitaev E8 state. Residual: condense the |μ₄| Lagrangian glue (v235)" },
      { label: "Closing as physics", value: "seam is SRE", description: "Sharper still: det K=1 ⟺ no topological ground-state degeneracy ⟺ the seam bulk is short-range-entangled (the Kitaev E8 phase) — now verified on the explicit lattice model (det K 4→1, v367/v368) and the genus-1 GSD = 1 closure (v378)" },
      { label: "Seam Equivalence Theorem", value: "closed mod cited", description: "The core is the keystone SEAM.EQUIV.01 (the raw RP seam IS the holomorphic (E8)₁ net at τ=i), now [C] closed modulo cited theorems: pinned at every computable level by an explicit lattice model (v367/v368) and the S3 closure stack (v376–v379), Lean-pinned (FORM.SEAM.MMST.01) to the published MMST/Adamo theorems, residual [O] = the cited continuum existence only (v336) — the theory's one irreducible structural postulate, the role the constancy of c plays in relativity" },
      { label: "Flat-Away", value: "one geometric input", description: "Both routes reduce to one shared fact — the raw seam is flat away from the four marks. Heat route: positive-definite a₂ proved (convexity) + closed form + Lean (v292/v295/v296); spectral Hessian PD (v293); Troyanov minimiser (v294); red-team Z₄≠mark-local (v290); Route A = citable stack Kitaev/Freed-Hopkins→Müger/KLM→Conway-Sloane (v297)" },
      { label: "Closing arc (v300–v302)", value: "no TFPT-internal assumption left", description: "Flat-Away hardened to a discrete degeneracy obstruction + its pin derived from the (E8)₁ integer-weight character via 2d Steklov rigidity (v300); Route A's invertibility discharged by the free-fermion classification (gapped 16-Majorana c=8 bulk is invertible, #anyons=|det K_E8|=1; v301); the last input is the derived Recovery gap Δ=6·ln(3/2)≈2.43>0 = a bulk mass gap via OS/quasi-free clustering (v302). SEAM.EQUIV.01 is now [C] closed modulo cited theorems (lattice v367/v368 + S3 stack v376–v379, Lean FORM.SEAM.MMST.01), residual [O] = the cited continuum existence only (v336)" },
    ],
  },
];

export function paperLabel(p: Paper): string {
  return p.label ?? `Paper ${p.number}`;
}
