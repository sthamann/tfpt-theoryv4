import { SITE_VERSION } from "@/lib/version";

export type PaperStatus =
  | "orientation"
  | "core"
  | "synthesis"
  | "audit"
  | "frontier"
  | "redteam"
  | "horizon"
  | "contracts"
  | "safeguards";

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
  safeguards: {
    label: "Verification discipline",
    color: "text-emerald-300",
    bg: "bg-emerald-500/10",
    ring: "ring-emerald-500/30",
    gradient: "from-emerald-500 to-teal-500",
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
        body: `TFPT ${SITE_VERSION} closes the discrete compiler, the algebraic SM readout, the EM fixed point, the admissible gapped IR sector and the R + R² spectral-action shadow. It does not yet certify a strict physical TOE end-to-end (the seam keystone is closed only modulo a cited published theorem). The live residual is three named interfaces: one dimensionful scale anchor v_geo [O], the metric-sector inclusion G_net (route split 2026-07-22: MMST route SEAM.EQUIV.MMST.01 [C] closed modulo cited theorems, twistor route SEAM.EQUIV.TWISTOR.01 [O], parent SEAM.EQUIV.01 [O] as an unconditional claim), and the typed runnable transfer suite F_transfer (v371–v375). The keystone's 128-spinor extension leg is now re-founded on the peer-reviewed crossed-product package (v469, Longo–Rehren/Böckenhauer/KLM), with the realisation input reduced to invariant level — SEAM.EQUIV.01 stays [O]. The historical labels (U_wall)/(G_metric)/(F_frontier) are kept only for ledger continuity.`,
        formulas: [
          "\\underbrace{\\text{compiler}}_{\\text{closed}}\\ \\Big|\\ \\underbrace{\\text{admissible IR physics}}_{\\text{conditional (RP, gap)}}\\ \\Big|\\ \\underbrace{\\text{strict physical TOE}}_{\\text{open}}",
          "\\text{Rest} = v_{\\mathrm{geo}} \\oplus G_{\\mathrm{net}} \\oplus F_{\\mathrm{transfer}}",
        ],
      },
      {
        title: "The anchor: one number a = (1,1,2)",
        body: "The two axioms are not even independent: they are the elementary symmetric polynomials of the single parabolic anchor a = (1,1,2), and its power sums generate the big Lie data directly. The inputs collapse to the anchor plus the lone continuous primitive π. And a is itself half-forced: three positive integers summing to 4 admit exactly one partition, {1,1,2}, so g_car = e₂ = 5 and |Z₂| = e₃ = 2 are arithmetic corollaries of the four marks given the weight typing — machine-checked with all negative controls (v491, sharpening v53); the residual is the weight-typing postulate, and P2 stays the declared axiom. The typing itself is now hardened (v499): given the four marks, rank 3, the cusp class and unitarity (U), the Deligne canonical extension of the flavor connection has deg E = −4 (residue traces) and Mehta–Seshadri stability forces h⁰(E) = 0, so integrality (Birkhoff–Grothendieck), positivity and the sum 4 are theorems — the residual shrinks to the module identification plus (U), both [C]; and that module-identification rest is now ONE residual with the QGEO modulus rest (the order-4 clock = the Coxeter/cusp-class carrier datum; v503, QGEO.EMERGE.LIGHT.01, no marker moves). That common residual is itself reduced to ONE alignment bit — the collar deck central in the mark-D₄; the clock's ORDER is fermionically forced, U² = (−1)^F exactly (v506, SEAM.CLOCK.RIGIDITY.01, markers unchanged) — and the bit is no tautology: the deck's CLASS is derived (every mark-free collar deck is a half-period translation of the seam double), only its POSITION stays the [C] input (v507, SEAM.BIT.ORIGIN.01, markers unchanged). The freedom theorems (v510, SEAM.BIT.FREEDOM.01) type that position half as TOPOLOGY — the covering deck is free on the seam circle, the edge class is excluded — so the bit reduces to the square-modulus datum τ = i alone; and the flag-transitivity web (v512, SEAM.TAU.FLAG.01) gives that datum its sharp DISCRETE form: bare mark-transitivity is automatic for every free-circle configuration (the pair-exchanging V₄; no local jet sees the side bit), while FLAG transitivity (marks AND their two sides indistinguishable, V₄ → D₄) ⟺ τ = i — a 13-fold exact equivalence web whose negation is concretely measurable (odd-doublet split (2/π)ln cot(δ/2) ≠ 0); free OS positivity is since documented as the EIGHTH side-blind test (v521): the bit is not derivable from free RP/Θ existence and remains genuine discrete input. The bit has since survived TEN side-blind derivation attacks on that scoreboard — free RP/Θ (the eighth, v521), the exhausted Wick-computable free-plus-twist state class (the ninth, v525) and the first genuinely interacting seam toy (the tenth, v529) — and is now physically DEFINED as the twist-class choice: facets #14/#15 extend the web to 15 exact equivalences (both directions each), the flip-axis fraction is a gauge-robust order parameter (O = 1/2 at m = 4, 0 elsewhere), and its η holonomy is in principle interferometrically readable (v528, SEAM.BIT.TWISTCLASS.01; the bit remains formal input — a definition replaces no derivation, no marker moves). The consolidated reduction state (2026-07-23): the compiler's dimensionless inputs reduce to four marks (derived from P1-side topology), one discrete symmetry-lift bit — the twist-class choice (flag transitivity ⟺ τ = i; equivalently the clock / the CM-fixed half-period / the non-split extension class on the free seam circle) — and π — a reduction state, not an abolition of the axiom.",
        formulas: [
          "e_1(a)=4=|\\mu_4|,\\quad e_2(a)=5=g_{\\mathrm{car}},\\quad e_3(a)=2=|\\mathbb{Z}_2|",
          "c_3 = \\frac{1}{2\\,e_1(a)\\,\\pi} = \\frac{1}{8\\pi}, \\qquad |R(E_8)| = p_1 p_2 p_3 = 240",
        ],
      },
      {
        title: "TFPT in the light of algorithmic physics",
        body: `The compiler framing sits in the Zuse–Schmidhuber–Wolfram lineage — physics as the output of a short computation. TFPT shares three instincts with it: minimal description length as the selection principle (no load-bearing free number, only π), deterministic resource-bounded generation (a chain of exact identities in about a second, not a search over models — the spirit of Schmidhuber's Speed Prior), and compressibility as the aesthetic (choosing E₈ is choosing the icosahedron, the shortest-to-describe object). It diverges on three points: TFPT forces one program instead of a measure over all universes, its description language is algebraic (Lie/lattice/VOA) rather than Turing bit-strings, and — the load-bearing difference — it is falsifiable, freezing dated kill-tested predictions where the algorithmic-TOE lineage stays metaphysics. This is positioning, not a new claim: it moves no status marker.`,
        formulas: [
          "\\text{shortest program} \\Rightarrow \\text{Kolmogorov / Solomonoff prior};\\quad \\text{TFPT} = \\text{one forced fixed point}",
          "T(2,3,r):\\ \\det\\mathrm{Cartan} = 3,2,1,0,-1\\ \\ (E_6, E_7, E_8, \\hat{E}_8, E_{10})",
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
        value: "9",
        description: "Introduction + 5 core papers + Appendix H + Origin Theory + contracts",
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
        body: "The even-Hamming code on five slots is the D₅ half-spinor: its dimension is the Pascal sum 1 + 5 + 10 = 16, which forces g_car = 5 uniquely. The E₈ root count is then a pure carrier trace. The current reduction state of P2 (2026-07-22, markers unchanged): the compiler's dimensionless inputs reduce to four marks (derived from P1-side topology, v216), one discrete symmetry-lift bit (flag transitivity of the four marks, V₄ → D₄, ⟺ τ = i — bare mark-transitivity is automatic on the free circle and no local jet sees the side bit, v491/v499/v506/v507/v510/v512) and π; AX.P2.01 stays the declared axiom.",
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
        body: "The fine-structure constant is the unique positive root of a parameter-free cubic built only from c₃, the abelian coefficient (Σ L + N_Φ = 41 = 10 b₁) and the exact seam generating function. Existence and uniqueness are proved; the value lands 1.9σ from CODATA-2022. The abelian coefficient is pinned three independent ways — carrier algebra 10 b₁ = g_car·2^(g_car−2)+1 = 41, the U(1) hypercharge index, and the external RGE generator PyR@TE 3, which reproduces β_g₁ = (41/10)g₁³ verbatim (v159) — so the EM input is not a free knob. The three terms reassemble as the stationarity of a U(1) determinant line (Maxwell α³ + Calderón −2c₃³α² + transport), every coefficient a named index/heat-kernel/discriminant atom (v341/v342). The one residual — the from-first-principles proof that this IS the exact ζ-regularised Quillen functional — is the tracked external target ALPHA.QUILLEN.EXACT.01 (v382), never the value. Four honest steps narrow it without closing it: a solvable 4D model reaches the a₄ heat-kernel order (v433); the matter factor b₁ is the U(1)_Y a₄ coefficient via the β = a₄ theorem, collapsing the three residuals to one [C] (the seam F-normalisation) + one [O] (v434); and a π-power test isolates the cubic α³ as the unique metric-independent (π⁰) topological rung, whose coefficient is a conditional integer Chern-Simons level (v435). A fifth step (v470) upgrades both leftovers: the α³ level equals the computed bulk Chern invariant |C| = 1 of the same collar model that realises S3 (TKNN/Avron–Seiler–Simon quantisation + Callan–Harvey inflow + the APS/Witten η=CS reading of δ log det), replacing v435's minimality assumption; and the seam F-normalisation is the affine embedding index k_Y = tr(Y²)/tr(T₃²) = 5/3 (Ginsparg 1987; (3/5)·(41/6) = 41/10 = b₁ exactly) — zero independent content, a face of SEAM.EQUIV.01. One invertible phase, two quantised responses (c₋ = 8 gravitational, C = 1 U(1)). A sixth step (v472) exhibits the bridge lemma at the finite level: the determinant line of the occupied frame over the U(1)-twist moduli of the same collar — the moduli space of flat U(1) connections, the Quillen-shaped object the target names — carries FHS curvature = 1 = the inflow level, exactly and size-independently, with clean controls and the twist-moduli integer equal to the Bloch-BZ integer (Niu–Thouless–Wu); what stays [O] is the continuum ζ-det identification on the abstract seam (= the SEAM.EQUIV.01 face). A seventh step (v484, SEAM.CONTACT.UNIT.01) unifies this target with the φ₀-puncture target: the shared 'c₃ per boundary insertion' rule (the {0,3,6} ladder here, the per-mark weight there) IS the KMS seam unit 2π = 1/(4c₃) with 1/4 = 1/|μ₄| — one bare boundary propagator orbit-averaged over the four marks — derived on the seam circle for the finite cycle sector (the bare Green function takes integer multiples of c₃·ln2 at the μ₄ separations; the log-det contact expansion is exactly graded in c₃ per insertion; the Λ prefactor 3/(4π²) = 48c₃² carries the same Ω_adm = 48 at two insertions). The two [O] targets merge into one remaining analytic step (diagonal ζ-renormalisation + multiplicity matching) — and an eighth step (v485, SEAM.CONTACT.UNIT.02) settles that step at the computable level: the renormalised diagonal vanishes EXACTLY at the KMS seam circumference (G_reg(0;ℓ) = (1/π)ln(ℓ/2π), zero iff ℓ = 2π = 1/(4c₃)), the mark determinant resums in closed form (det(I−uC) = (1−4u)(1+2u)², BFK route v151; linear term absent because Tr C = 0), and the 48/41 multiplicities are ONE state set under two response weights (flat = Ω_adm vs Y²/Ginsparg = 10b₁ = 40+1, Tr₁₆Y² = 10/3 exact). Every finite piece of the merged target is proven; the single remaining [O] is the abstract-seam ζ-det identification — a face of SEAM.EQUIV.01, the v382 typing now substantiated computationally. ALPHA.QUILLEN.EXACT.01 stays [O]; α⁻¹ stays [E].",
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
        body: "The quark mass ratios are pure integer Plücker readouts on the derived selector stratum — no transcendental solve. The absolute amplitude reduces to one overall scale v_geo (ratios + Grand Mass Volume), the same dimensionful anchor as gravity's 1/G. The remaining ℤ₃ deck choice is since derived: the integer deck pairs the Q₊=1 line with the self-conjugate character 2, so the geometric boundary deck is the sheet-twisted class and the cusp exponential is excluded (v141) — GATE.QGEO keeps only its realisation premise, with no discrete freedom left — and that premise sits at its floor: the full Möbius D₄ of the seam curve matches the integer model parity by parity (ι = T_A exactly, δι = Σ; v146). The finite rigidity is now proven exactly [E]: μ₄ has cross-ratio 2 and a faithful Möbius D₄ stabiliser, H¹(ℙ¹∖μ₄) has rank N_fam = 3, and the eigenforms ω_k carry the μ₄ characters of weights (1,2,3) = the A₃ exponents = Spec(Q₊) — so only the seam-collar realisation stays open (v168). The Sheet Diamond carrying these operators is a discrete geometry with two axes (v218): the determinant is linear along the winding axis (A₃-driven, slope 6 = |R⁺(A₃)|) and quadratic along the sheet axis with curvatures (8, 6) = (rank E₈, |R⁺(A₃)|); the anchor-Plücker coordinates lift K→C→F in two exact steps (1,8,10) then (1,8,16) — the decuple A_Λ then the full spinor generation dim S⁺; and the characteristic-polynomial discriminants of Q,K,C,F factor as q(r)²·Disc(q) with squares (1,3,4,6) = (N_Φ,N_fam,|μ₄|,|R⁺(A₃)|) and kernels (13,48,65,105). No new numbers — it organises the existing operators more strictly. Sharper still (v410): the sheet axis V = Q·diag(0,1,1) is a binary internal compiler — its powers print the carrier spine Vⁿ·1 = (2ⁿ⁻¹, 2ⁿ, 2ⁿ⁺¹−1) = (1,2,3),(2,4,7),(4,8,15),(8,16,31), and four exact bilinear families collapse the recurring integers (6,7,9,11; 13 = Δ_Q, 27 = 1ᵀRa, 55, 56 = dim 56_E₇) into one operator's iteration. The quark ratio is then a pure V-power readout c_u/c_d = (1ᵀV⁴1)/((aᵀV1)(1ᵀV²1)) = 55/117 (v411, an exact re-encoding); the unnamed Z₂-wall corner J = M(1,−2) carries χ_J = (6,3,2), aᵀJa = 30 = h(E₈), det(I+J) = 12, det(2I+J) = 40 (v412); the sheet axis encodes the atoms as difference orders Δe₁ = 3, Δ²e₂ = 4, Δ²e₃ = 8 with anchor energy 52+11t (v413); and the center C is a resolvent portal det C = 14 = dim G₂, det(I+C) = 52 = dim F₄, det(2I+C) = 120 = |R⁺(E₈)| (v414). All [E] algebra; the binary spine is forced by Spec(V) = {0,1,2}, so the Lie-dimension readings stay [C], audit-typed.",
        formulas: [
          "\\frac{c_u}{c_d} = \\frac{g_{\\mathrm{car}}\\cdot 11}{N_{\\mathrm{fam}}^2\\,\\Delta_Q} = \\frac{55}{117}, \\quad \\frac{c_c}{c_s} = \\frac{34}{47}, \\quad \\frac{c_t}{c_b} = \\frac{3}{26}",
          "\\hat m_t/\\hat m_b = \\tfrac{3}{26}(\\varphi_0)^{-2} = 40.81",
        ],
      },
      {
        title: "The absolute neutrino scale: one parameter under the carrier normalisation",
        body: "The absolute ν-mass scale is one seesaw ratio m₃ = (y_ν v)²/(2M_R) — honestly typed as one open UV input (v272), with the NO floor Σm_ν = 0.0586 eV as the cosmological kill test. New (v481, FLAV.NUSCALE.02, CANDIDATE class like v467/v468): the y_ν = 1 probe was not the carrier normalisation — one SO(10) 16 per family with the minimal Yukawa sector (10_H / PS (1,2,2)) forces y_ν = y_t at the matching scale, collapsing the (y_ν, M_R) trade-off to M_R alone. With explicit 1-loop RG (gauge/y_t/λ up, ADKLR Weinberg-operator running down) the observed m₃ = 0.0503 eV demands M_R = 9.3×10¹³ GeV — inside the compiler's own PS window [4.2×10¹³, 2.4×10¹⁵] GeV (v249) at log_c₃(M̄/M_R) = 3.15 (y_ν = 1 gives the structureless 2.58). Honesty gate: the integer rung M_R = c₃³M̄ predicts m₃ = 0.030 eV, 40% low at 1-loop, so the ladder pin is DECLINED per the anti-numerology rule — and the named decision computation is meanwhile EXECUTED in bracketed form (v482, FLAV.NUSCALE.03): the rung needs a rescue factor ×1.670 while >3σ-generous input envelopes (m_t ±3 GeV, α_s, κ-run ±10%, PS-leg β ×[0.5,1.5]) reach at most ×1.165 combined, so the unstructured rung is EXCLUDED (not an RG artifact); the only escape, a third-generation Majorana structure factor r ≈ 1.67 sitting 0.18% from g_car/N_fam = 5/3, is recorded post-hoc and declined (no forcing mechanism). That escape is now DECIDED dead (v488, FLAV.NUSCALE.04): since the 126bar is not in the E₈ hull (v247), M_R can only come from the d=5 operator (16·16bar_H)²/Λ with singlet/45 insertion channels; every ν^c channel weight {1, 1/4, 1, −1/2, 3/8} is a {2,3}-smooth rational, so no channel combination can produce 5/3 — and the unique natural 5 of the embedding, k_Y = 5/3 (Ginsparg), is a full-multiplet trace whose direction has Y(ν^c) = 0 exactly, structurally decoupled from the Majorana operator; Clebsches are generation-blind (family-space scalars), so diag(1,1,3/5) cannot arise from group theory at all. A clean negative: the rung+5/3 rescue is a numerical coincidence without mechanism, and the one-parameter window candidate stands as the honest endpoint. The candidate band m₃ ∈ [0.002, 0.115] eV brackets the observation and DESI cuts the window from below; nothing closes and the frozen record is untouched.",
        formulas: [
          "y_\\nu = y_t \\;(\\mathbf{16}\\cdot\\mathbf{16}\\cdot\\mathbf{10}) \\;\\Rightarrow\\; M_R = 9.3\\times10^{13}\\,\\mathrm{GeV} \\in [M_{\\mathrm{PS}}, M_{\\mathrm{GUT}}]",
          "\\log_{c_3}(\\bar M_{\\mathrm{Pl}}/M_R) = 3.15 \\;(\\text{integer rung } c_3^3\\bar M_{\\mathrm{Pl}} \\text{ declined at 1-loop})",
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
    subtitle: "The seven E₈ slices as an audit raster, the cascade spine, the Möbius loop — and the thirty-step celestial/twistor route with the measure chain derived",
    abstract:
      "E₈ as an audit container, not a mystery: the seven maximal slices of 248 as a falsification raster (every load-bearing number must appear in at least one projection), the bridge showing the old E₈ orbit cascade D = 60 − 2n is the same even-integer spine as the compiler, and the Möbius bootstrap in which g_car = 5 and the '8' in c₃ are overdetermined E₈-closure fixed points — only π irreducible. Since the celestial/twistor round the note also carries the THIRTY-STEP continuum story — from the μ₄ clock to the (E₈)₁ boundary shadow — in which the measure chain of the celestial route is DERIVED, not declared: single-valuedness from F-independence + the Quillen pairing (v520), the 1/det_j normalisation the Atiyah–Bott fixed-point factor computed from three independent sources with ψ = 64 reproduced (v523), the residual [O] narrowed to the global BCOV integral beyond the fibre zero-mode factor; plus the Woit OS-bridge stages α/β₁/β₂ (v519/v522/v524), the thermal seam (v526), the ten-test side-blind scoreboard with the twist-class definition of the bit (v528) and the first firing interacting kill test under its typed fence (v529). SEAM.EQUIV.01 and WOIT.OS.TWISTOR.01 stay [O]; no marker moves.",
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
        body: "The carrier rank is an overdetermined E₈-closure fixed point: rank-fill (g + 3 = 8), Coxeter-match (h(D_g) = 2g − 2 = 8), and the integer-glue/norm closure whose reverse-glue quadratic has nontrivial root μ = 4. A fourth, arithmetic face (v491): given the four marks, the unique partition of 4 into three positive parts is {1,1,2}, so g_car = e₂ = 5 is a corollary of the weight typing — the residual is the typing postulate, P2 stays the declared axiom. The typing is itself hardened (v499): Deligne + Birkhoff–Grothendieck + Mehta–Seshadri stability derive integrality, positivity (h⁰ = 0) and the sum 4 from the four marks, rank 3, the cusp class and (U) — leaving the module identification plus (U) as the [C] residuals; the module-identification rest is now ONE residual with the QGEO modulus rest — both reduce to the same order-4 clock = Coxeter of W(A₃) = the cusp-class carrier datum (v503, QGEO.EMERGE.LIGHT.01: the free field alone does NOT select the square — the global det′ winner is hexagonal — the square is pinned by the clock's rigidity; markers unchanged); the clock-rigidity theorems then reduce that common residual to one alignment bit with the clock's order fermionically forced, U² = (−1)^F exactly (v506, SEAM.CLOCK.RIGIDITY.01), and the bit-origin theorems derive the deck's CLASS (a half-period translation of the seam double) — only its position stays the [C] carrier input (v507, SEAM.BIT.ORIGIN.01); the freedom theorems (v510, SEAM.BIT.FREEDOM.01) then type that position half as topology (the covering deck is free on the seam circle; the edge class is excluded), so the residual is the square-modulus datum τ = i alone; and the flag-transitivity web (v512, SEAM.TAU.FLAG.01) restates that residual as ONE discrete symmetry-lift bit — flag transitivity of the four marks (V₄ → D₄) ⟺ τ = i, with bare mark-transitivity automatic for every configuration — the current reduction state of P2: four marks (derived from P1-side topology) + one discrete symmetry-lift bit (flag transitivity ⟺ τ = i) + π, with AX.P2.01 still the declared axiom.",
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
      {
        title: "The celestial and twistor continuum route",
        body: "The seam's boundary 2-sphere is the celestial sphere of null directions (Möb ≅ PSL(2,ℂ), the clock the order-4 Möbius map, v180). Reading the seam through the celestial-holography lens (Bittleston–Homans–Sharma's chiral algebra on ALE spaces; Costello's twistorial SDYM) yields a coherent thirty-step story — the narrative arc from the μ₄ clock to the (E₈)₁ boundary shadow — the executed work packages WP1–WP5d (both WP5d stages) plus the WP5e α, β, γ, δ₁, δ₂, ε₂ and ε₁ stages, the three back-reaction milestones M1–M3, the measure decision (Step 21) and the constructive w_m derivation (Step 24) of the research contract CELEST.SEAM.01, plus the RP-blindness decision on the alignment bit (Step 22) with its twist-state completion (Step 26), the thermal-seam third leg of c₃ (Step 27), the silver demystification (Step 28), the twist-class definition of the bit (Step 29), the interacting FK-toy Kill-Test-2 shadow (Step 30; scoreboard 10), and the α, β₁ and β₂ stages of the OS twistor bridge WOIT.OS.TWISTOR.01 (Steps 20, 23 and 25; full technical reference: the Research Contracts companion). Step 1, setup [E] (v492): the E₈ μ₄-glue grading 240 = 52+64+60+64 is INNER — a flat ℤ₄ monodromy on the A₃ ALE space ℂ²/ℤ₄ (= the A₃ singularity XY = Z⁴); the glue-equivariant sector closes (possible only because dim g_j = (60,64,60,64)) and reproduces the (E₈)₁ character as the sum of the four glue sectors; critical correction: clock² = deck (spin bridge ℤ₈, 8 = 2|μ₄| — the c₃ = 1/(8π) winding integer); that spin bookkeeping is now FORCED on the seam fermions (v506): the NS implementer of the deck satisfies U² = (−1)^F exactly (nonsplit ℤ₄, no phase choice escapes it), the quarter-shift lifts to a canonical ℤ₈ tower (V² ∝ U, V⁴ ∝ (−1)^F), and the R-sector control splits (U_R² = +1) — the forcing rests exactly on the established bounding spin structure. Step 2, deformation [E] (v493): the clock-invariant family XY = Z⁴ + a₀ carries no shape modulus (I = 12a₀, J = 0 identically ⇒ j = 1728, τ = i frozen for all a₀); the clock IS the Picard–Lefschetz/Coxeter monodromy. The residual behind that clock is now ONE alignment bit (v506: a marks-preserving root exists iff the deck is the central involution of the mark-D₄), and the bit has survived its tautology attack (v507, SEAM.BIT.ORIGIN.01): the marks are the four half-periods of the seam double and every mark-free collar deck IS a half-period translation — the deck's CLASS is derived — yet the origin does not force the alignment (core solve λ ∈ {−1, 2, 1/2}, one value per half-period; the aligned one is the CM-fixed c* = (1+τ)/2; the silver counterexample sits in-family); the bit is an equivalence tetrad (clock ⟺ τ = i with the CM-fixed half-period ⟺ deck central ⟺ harmonic deck pairs ⟺ nonsplit NS Fock lift) with a physical face — the Fidkowski–Kitaev-type extension class (central U² = (−1)^F vs edge U² = +1, split; 2 vs 0 roots) — distinguished but not derived: only the POSITION (which half-period) stays the [C] carrier input; no marker moves. And that position half is now TOPOLOGY (v510, SEAM.BIT.FREEDOM.01): the collar deck is a COVERING deck (the ℤ₂ seam of the Möbius double), hence free on the seam circle — the unique free involution is the antipode (Aut(C₁₆) = D₁₆, complete census; every reflection has two circle fixed points and its quotient is an interval, breaking the closed-circle 6π budget), NONSPLIT ⟺ FREE over all 17 involutions in exact Cl(16), and the edge/silver arrangement (whose mark circle passes through the deck poles — the restriction of the BRANCHED pillowcase involution) is excluded; harmonic + free solves exactly to b = ±i, so the alignment bit reduces from 'harmonic AND central' to the square-modulus datum τ = i alone — and the flag-transitivity web (v512, SEAM.TAU.FLAG.01) gives the modulus half its sharp discrete face: on the free circle bare mark-transitivity is automatic for every deck-invariant configuration M(δ) = {±1, ±e^(iδ)} (the pair-exchanging V₄; no local jet sees the side bit), and what selects δ = π/2 ⟺ τ = i is exactly FLAG transitivity (V₄ → D₄ symmetry lift), welded into a 13-fold exact equivalence web (odd-doublet split (2/π)ln cot(δ/2), arc-Laplacian degeneracy, the K3 indicator in closed form, ρ-twist existence, cusp-4-cycle implementability, harmonicity, j = 1728, and — since Step 22 — the D₄ closure of the OS-reflection group) — the carrier input reduces from a continuous modulus to ONE discrete symmetry-lift bit, its negation concretely measurable. Step 3, consistency honestly demoted [E]/[C] (v495): E₈ is on Costello's axionic list and (κ/c₃)² = 12 exactly — but the alignment format passes 8/8 across the whole list: alignment survives, selectivity does not (compatibility, not evidence). Step 4, type mismatch + boundary limit [E] (v496): the (E₈)₁ character is NOT a conformal block in the jet grading (growth n^(2/3) vs n^(1/2)), but one full μ₄ period of loop energies sums exactly to 248 — the character is a boundary-limit SHADOW, the same scaling-limit shape as SEAM.EQUIV.01/MMST. Step 5, the null ideal quantitative [E] (v497): stabilisation theorem w = n+1; 27000 = 30³ = h∨³ DERIVED (Freudenthal/Weyl/peeling); quotient 31124−27000 = 4124 = the independent μ₄ sector sum (two routes, one number); SO(16)₁ negative control (four blocks, 5304 ≠ 14³). Step 6, the deleting object as an operator [E] (v498): |s⟩ = (E^θ_{−1})²|0⟩ explicit, J^a_1|s⟩ = 0 for all 248 generators (case tally 190/57/1), level dial 2(1−k) (only k = 1 deletes), clock phase −1; D₈ contrast: the singular-vector mechanism is level-1 generic, the one-block closure is the E₈/μ₄-specific part. Step 7, the limit state [E]/[C] (v500): the quasi-free family ω_w stabilises exactly at the WP5a threshold and its limit carries the null ideal in its GNS kernel — the complete 9361-block exact level-2 Gram has rank 4124 with kernel 27000 = V(2θ) weight by weight, |s⟩ IS the GNS zero vector, and a CCR obstruction shows the family is NECESSARY. Step 8, the two-interval index [E]/[C] (v501): the fermionic two-interval MI is extensive (μ = 1 reference) while the orbifold prescription pays exactly one classical bit (the ln 2 plateau at machine precision), so μ_gauged = 4 = the v490 parity census, and the condensation arithmetic 16 → 4 → 1 (KLM/Longo–Rehren, θ_v = 1 at ν = 16) closes with μ = 1 — the preregistered kill does not fire. Step 9, the prefactor and the level pinned on the CFT side [E]/[C] (v502): the q^(−1/3) prefactor of E₄/η⁸ is exact μ₄ vacuum-energy bookkeeping — the clock is INNER, so the twist is θ = 0⁸ in every sector (a SHIFT orbifold, not a rotation orbifold) and each sector carries −c/24 = −1/3 at c = 8; the sector weights (0,1,1,1) ARE Casimir energies (spectral flow, and exactly via the 16-Majorana seam carrier: 5/8, 3/8, 1); k = 1 is forced three independent ways (current condition h(J) = k; conformal embedding 47(k−1)(k+266/47) = 0; central charge 240(k−1) = 0) plus the Step-6 singular-vector dial (31124 − 27000 = 4124 at k = 1 only); honest sharpening: glue-h integrality holds at EVERY level and fixes nothing — the naive route is retired; the deck rotation reading fails (3/16 ≠ 3/8). Step 10, the KLM completion on the lattice [E]/[C] (v504): complete rationality (Kawahigashi–Longo–Müger) = split + strong additivity + finite μ-index, and with Step 8 supplying the index the two remaining legs are witnessed for the same orbifold prescription — strong additivity is algebraically EXACT with the shared boundary Majorana (Even(A) ∨ Even(B) = Even(A∪B), GF2 spans full, rank 32/32; disjoint exactly index 2 = the Step-8 ln 2 bit, localised at the split point); entropically the touching defect stays BOUNDED < ln 2 with the Ising ¼-exponent approach (p = 0.2444) while the preregistered U(1)/Dirac control DIVERGES (Klich–Levitov pinned): bounded-vs-divergent is the lattice discriminator (bounded ⟺ finite index, Longo–Xu); the split property is quantitative (coupling σ_k at the elliptic-nome rate πK(1−x)/K(x) to 1.3–2.0%) and the orbifold INHERITS the same ladder exactly (C → −C; the Λ²C compound — Longo heredity); Pimsner–Popa E(a) − a/2 = PaP/2 holds identically (λ = 1/2 = 1/[F:F_even] with exact integer attainment, λ_E4 = 1/4 = 1/μ, exp(Δ∞) = 2 = 1/λ_PP — two independent index routes). All three KLM ingredients now carry lattice witnesses; the continuum uplift is honestly fenced — 'finite-group orbifolds of completely rational nets are completely rational' is Xu's theorem, cited, not claimed. Step 11, the equivariant anomaly ledger on twistor space [E]/[C] (v505): the twistor side of the uplift pushed as far as exact arithmetic reaches — the Atiyah–Bott/Lefschetz fixed-point skeleton of the one-loop box anomaly on ℂ²/ℤ₄ is exact (denominators (2,4,2) with Dedekind sum 5/4 = (|ℤ₄|²−1)/12, equivariant characters (248,0,−8,0) by two routes, invariant average 60 = the carrier); the honest sharpening: only the INVARIANT sector is Okubo-quadratic (36⟨x,x⟩², 36 = λ̃²_e8), the twisted sectors are not, and the AB-weighted sum cancels the D₅ quartic exactly while leaving the RIGID residual 32·T₃ — twisted-sector closed strings must carry the rest; the index bridge is the centrepiece: f(m) = ch₂(T_m) exactly (fixed-point ledger = McKay/Kronheimer intersection ledger), glue defect −78 by both routes; the level dials say k = 1 GEOMETRICALLY (lattice current count 240/0/0/0, embedding residual (0,360,814,1362), one scale ⇒ one level); and an honest refutation: a₀ fills the BSS GRAVITON slot O(2), NOT the axion slot O(−2) (weight mismatch 4 = |μ₄|) — 'the theory brings its own GS axion as a₀' is false; instead the three H²(ALE) classes carry exactly the three twisted-sector Coxeter characters {i,−1,−i}, and the bulk axion must come from the O(−2) tower field itself; the preregistered kill ('inflow demands a level ≠ 1') does NOT fire on the equivariant skeleton. Step 12, the exchange no-go and the contact-term criterion [E]/[C] (v508): could the three sphere axions of Step 11 cancel the rigid 32·T₃ residual by Green–Schwarz-type EXCHANGE with sector-compatible quadratic vertices? No — and the refusal is a theorem, not a fit: the W(D₅)×W(A₃)-invariant vertex space on the glue Cartan is computed exactly (quadratics = span{s₅, s₃}, dim 2; quartics = span{P₁,P₂,P₃,T₅,T₃}, dim 5 — complete by Weyl nullspace arithmetic), and the PRODUCT THEOREM kills the mechanism wholesale (any two invariant quadratics multiply into span{P₁,P₂,P₃} — zero T₅/T₃ content, so every exchange image is annihilated by Φ_T3 while Φ_T3(A_fix) = 32 ≠ 0); the strict two-index ℤ₄ rule collapses the sphere couplings entirely (only m = 0 survives), the twist-insertion channels give a rank-2 exchange matrix with rank([M | A_fix]) = 3 and the annihilator certificate (Φ_T5, Φ_T3, Φ_P)(A_fix) = (0, 32, 72) — two independent obstructions, the second driven by the side discovery K⁽⁰⁾ = −15·K⁽²⁾ (the even-sector quadratics are parallel); naturalness DISSOLVES (ch₂-natural and Atiyah–Bott-weight couplings both certify (0,0) against the required (32,72) — scale- and coupling-independent); controls: SO(16) has NO sphere partners and uncancelled T₅ (E₈ doubly special), D₈ has no T₃ structure at all; the slot bijection of Step 11 is untouched and the preregistered level-kill still does not fire — what dies is the exchange REALISATION of the pairing; the 32·T₃ burden moves to the twisted BCOV contact terms with a BINARY criterion: the one-loop coefficient on ℂ²/ℤ₄ must come out exactly (9,−30,−15,0,32), computed, not fitted. Step 13, one level is a theorem and the sector counter pins k = 1 [E]/[C] (v509): the Costello–Paquette–Sharma level-from-flux mechanism (Burns holography: 'level = flux quantum × Dynkin index') executed on the lockstep spheres — the CPS skeleton is replicated exactly (S³ period (2πi)²N, exceptional-sphere Kähler flux 2πN, boundary level magnitude 2N with T(vector) = 1), and the geometric side is PINNED, not postulated: the Step-11 ch₂ ledger + integrality + unimodularity + effectivity force the pairing matrix c₁(T_m).[Σ_i] = δ_mi by complete enumeration (48 unimodular solutions, exactly 2 effective: identity + diagram flip), so the glue fluxes are F_i = (64,60,64) = dim g_i with exactly ONE quantum per charged root current; 'level = total open-string flux' is KILLED by the lockstep test itself (three unequal numbers — F_i is the flavour multiplicity), while 'level = flux per adjoint current' gives (1,1,1), anchored by the lattice current count (240,0,0,0) and the embedding index 1; the ord-4-vs-level-1 tension resolves (the clock order counts FRACTIONAL flux sectors: μ = 16 = ord², Lagrangian μ₄ glue, KLM 16 → 1) and a new dial pins the value: #primaries((E₈)_k) = (1,3,5,10,15,27) for k = 1..6 — exactly ONE sector iff k = 1; the centrepiece is the LOCKSTEP THEOREM, lifting Step 11's 'one scale ⇒ one level' from heuristic to theorem (clock invariance forces one μ₄ orbit of branch points, |Π_j| = √2·t equal on all three spheres, det(A−1) = −4: no invariant flux vector — k₁ = k₂ = k₃ IS a theorem of clock invariance), with a new falsifier (the clock-forbidden family Z⁴ − Z: zero lockstep chains over all 24 orderings) and an honest limit (uniform doubling keeps the lockstep — equality, not the value); controls: k = 2 dies on the closure dials while the lockstep dial honestly does not fire, SO(16) leaves two spheres flux-dark, A₂ admits no Lagrangian glue at all (μ = 12 not a square); the CPS dictionary on PT/ℤ₄ itself stays [C] (their geometry is the ℂ² blow-up, not the A₃ ALE), the type-I B-model back-reaction stays [O]. Step 14, the full-tensor ledger: the collapse is real, and one cubic door opens [E]/[C] (v511): Step 12's collapse was a CARTAN-restricted statement — the named escape route (δ₂) recomputes the ledger on the full adjoint tensor structure of e₈, with two exact halves. The collapse is CONFIRMED: g₀ = d₅ ⊕ a₃ is semisimple with no u(1) factor (class-0 roots 40+12, root span rank 8), the sectors factorise into minuscule Weyl orbits g₁ = (16_s, 4), g₂ = (10, 6), g₃ = (g₁)*, and the INNERNESS THEOREM decides everything wholesale (the grading element h lies in the Cartan OF g₀, so every g₀-invariant tensor carries total charge 0 mod 4): bilinear invariants exist only at j′ = −j (dims 2/1/1/1) and ALL 15 non-neutral trilinear sector triples have Hom = 0 — the sphere axions have no invariant partner operator at any arity ≤ 3, full-tensorially. AND one cubic door opens: the unique totally symmetric trilinear on all of e₈ — the su(4) d-symbol (so(10) has no cubic Casimir, T₅ stays protected) — carries an exchange quartic Q_dd = (1/60)(T₃ − P₃/4) (two independent routes, Killing propagator 2h∨ = 60 from the roots) with Φ_T3(Q_dd) = 1/60 ≠ 0: Step 12's master kill covers quadratic vertices only. The pairing remains obstructed in the charge reading (M = [E₁₃, E₂₂, E₀₀, Q_dd] rank 3 vs augmented 4) but with the genuinely WEAKER certificate {Φ_T5, ψ = Φ_P − Φ_T3/4}, ψ(A_fix) = 72 − 8 = 64; relaxed, it becomes exactly solvable: A_fix = −u + 8v + 2w + 1920·Q_dd. Number fences typed [C] only: 64 = dim g₁ = 2⁶, 1920 = |W(D₅)| = 8·240 — and the 1920 fence has since been stress-tested and FAILS as a derivation claim (v513, CELEST.DTERM.NONDERIV.01): the |W(D₅)| reading is look-elsewhere-loaded (11/924 catalog expressions hit 1920, vs 8/924 for the control target 1800) and convention-contingent (only 1 of 5 normalisations produces 1920; the charge-legal flux pairings give 2048/1800 and miss; the twisted cubic index 32i clashes in class provenance with the true quartic 32) — the convention-stable [E] core is the factorisation c_d = Φ_T3(A_fix)×2h∨(E₈) = 32×60, the fence stays [C], the physical generation of the 32 stays [O]. Controls: SO(16)/D₈ has no symmetric cubic, no odd sectors and no A₃ block (E₈/μ₄ doubly special); false g₀/sector assignments inflate or kill the tables. The burden on the δ₁ contact terms is thereby SHARPENED (they must supply either the ψ = 64 slice or the selection-rule relaxation — a burden since DISCHARGED by Step 17: the declared KS measure supplies the ψ = 64 slice exactly, so the cubic d-channel is not needed) — and the δ₁ exploration run itself stands UNDECIDED: the strict holomorphic reading is refuted at the ℤ₂/Eguchi–Hanson anchor (a method boundary, not a kill); the contact term is the MODULAR COMPLETION of the Atiyah–Bott data, a Harvey–Moore-type τ-integral with the forced leading (T₅,T₃) ratio 4:3. Step 15, the bulk axion is a construction and λ̃ = 6 is pinned three ways [E]/[C] (v514): Step 11 refuted 'a₀ is the GS axion' and left the bulk axion to the O(−2) tower field as a slot — the ε₁ stage now BUILDS it. On PT′ = Tot(O(1)⊕O(1) → P¹) the pushforward ledger π₊O(−2) closes the Penrose accounting exactly ((d+1)² classes per degree = the exact wave-operator nullspaces, d ≤ 6) and EQUIVARIANTLY: the clock acts on the fibre coordinates as (μ₁,μ₂) ↦ (iμ₁,i⁻¹μ₂), the incidence relation forces the column weights (+1,+1,−1,−1), and the bookkeeping closes block by block for all four characters; the character series are P₀ = 1 + 3t² + 15t⁴ + 21t⁶ + 45t⁸ + …, P₁ = P₃ = 2t + 8t³ + 18t⁵ + …, P₂ = 6t² + 10t⁴ + 28t⁶ + …, the d = 0 slot has multiplicity (1,0,0,0) — THE BULK AXION SURVIVES THE PROJECTION — and the invariant fibre ring is the hypersurface (1−t⁸)/((1−t⁴)²(1−t²)): Z ∈ O(2), X, Y ∈ O(4), one relation in degree 8 = the a₀ weight (the Step-1/Step-2 geometry re-emerging from the slot); the Step-11 bijection sharpens per character (twisted minimal content (2t, 6t², 2t) = the Coxeter eigenvalues, no degree-0 mode, det(A−1) = −4) and the graviton control separates a₀ cohomologically (the O(+2) slot starts invariant only at fibre degree 4 with multiplicity 3 = {X, Z², Y}). The Green–Schwarz residue is pinned THREE independent ways: Okubo (Tr_adj X⁴ = (6⟨x,x⟩)² exactly on the 240 glue roots, 36 = h∨ + 6, λ̃ = 6 = |ℤ₂|·N_fam), the measure chain on PT/ℤ₄ (the quotient factor μ = 1/4 enters vertex²/propagator/anomaly and cancels EXACTLY; wrong bookings quantified and excluded: anomaly-only ⇒ λ̃ = 3, missing propagator renormalisation ⇒ λ̃ = 12), and the flux side (minimal CPS quantum N = 1, a single exchange channel exactly at k = 1, (κ/c₃)² = 12). The first honest back-reaction step follows in Gibbons–Hawking form: clock-invariant four-centre configurations form exactly two branches (four axis points = pure resolution, one free μ₄ orbit = pure deformation), the free orbit re-derives the Step-2 family (Π_p(Z − iᵖz₀) = Z⁴ − z₀⁴, a₀ = −z₀⁴, monodromy = one clock step), the charge-4 GH point is exactly the S³/ℤ₄ seam boundary, the periods Π_j = 4πt₀(i−1)(1, i, i²) confirm the Step-13 lockstep FROM GEOMETRY (Π·A = iΠ), the source ledger carries charge 4 = |μ₄|, and the honest sharpening: the Ricci-flat ALE has asymptotic log coefficient EXACTLY ZERO (the CPS log is an exceptional-locus statement; Burns contrast det g ≠ 1), with the multipole selection rule m ≡ 0 mod 4 storing −a₀ in the first symmetry-breaking (4,±4) harmonic. Controls: so₈ (λ̃² = 12 irrational — perfect squares in the Deligne series only {9, 36} = {sl₃, e₈}), diag(i,i) (Veronese cone, no hypersurface), k = 2 (three exchange channels). Honest fences: conditional on Costello's flat-PT matching [C]; the QUANTISED BCOV coefficient on PT/ℤ₄ and the twisted channels (32·T₃) stay [O] — preregistered as the M1–M3 back-reaction milestones (the A₃ Ω_N, the twisted KS measure, the a₀ uplift), each with success and kill criteria; all three are executed in Steps 16–18. Step 16, the back-reacted Ω_N: closed form, integral periods, forced charge 4 [E]/[C] (v515): the M1 milestone preregistered in Step 15 is now EXECUTED, with the preregistered SUCCESS criterion met and neither KILL fired. The residue 2-form is DERIVED, not assumed (on F = XY − P(Z) all three ambient representatives satisfy dF∧ω₂ = −dX∧dY∧dZ and pull back to ω₂ = dX∧dZ/X; at a₀ = 0 the orbifold-cover pullback is ω₂ = 4·dz₁∧dz₂ = |μ₄| × flat form — the residue normalisation itself CARRIES the source charge 4 — and the clock multiplies ω₂ by i, the Step-1 det = i replicated); the four O(2) centre sections q_p(λ) = iᵖt₀ − i⁻ᵖt₀λ² close the twistor family in one line, XY = Z⁴ + 4t₀²λ²Z² − t₀⁴(1−λ⁴)² (e₁ = e₃ = 0 identically; the seam fibre λ = 0 is exactly the Step-2 family, the a₂ ∈ O(4) slot opens only off-seam), with the CY-compatible clock lift γ: (Z,λ) ↦ (iZ,−iλ), γ⁴ = 1, Ω → +Ω; the periods reduce generically (∫ω₂ = 2πi(q_{j+1} − q_j) for arbitrary profile and path), giving the seam-fibre lockstep vector 2πi·t₀(i−1)(1, i, i²) with the exact covariance Π_{j+1}(−iλ) = iΠ_j(λ) for ALL λ, and the 12 collision nodes — honest conifold points (Hessian det 512t₀⁶, quadric rank 4) — sit exactly on the 8 eighth roots of unity (8 = 2|μ₄|, the ℤ₈ bridge), in clock orbits 4+4+4; the back-reacted 3-form is CLOSED FORM, Ω_N = Ω₀ + Σ N_p K_p with the CPS/Bochner–Martinelli kernel on the four centre twistor lines (∫_{S³}K = (2πi)² exactly, dK = 0 off-source, scale degree 0); the undeformed Ω₀ carries ZERO quantised 3-flux (all flux is sourced), every 3-cycle period is (2πi)²-integral, the flux vector N(1,1,1,1) is forced uniform TWICE OVER (clock orbit + the K₄ connectivity of the four lines), and the lens fundamental domain FORCES N ∈ 4ℤ — the source charge 4 = |μ₄| from quotient large-gauge quantisation, minimal invariant charge ↔ the CPS quantum N = 1 ↔ k = 1 (Step 13). The honest fence has teeth: on the clock-forbidden family Z⁴ − Z the (2πi)² quantisation ALSO holds — integrality alone is NOT the discriminator; the discriminator is the lockstep phase/modulus structure (0/24 orderings vs 8/24, node support on twelfth roots instead of ℤ₈) together with the clock forcing of equal fluxes. Anchors and controls: EH/ℤ₂ forces charge 2 = |ℤ₂| from the same machinery, the CPS flat patch allows every integer N, diag(i,i) collapses at step zero (Ω₀ → −Ω₀), fractional charges N = 1, 2, 3 excluded. Global kernel patching, the Hitchin small resolution and the CPS brane dictionary stay [C]; M2–M3 are executed in Steps 17–18, and the quantised BCOV coefficient stays [O] only in its measure question (the δ₁ chain itself is decided in Step 19). Step 17, the twisted KS measure: every sector the same Okubo square [E]/[C] (v516): the M2 milestone preregistered in Step 15 is now EXECUTED, with the preregistered SUCCESS wording met ON THE DECLARED COMPLETION MEASURE and the KILL (a leftover independent quartic in ANY sector) not fired. The measure ansatz is declared before computing: M2 declares the completion contact term contact_j = (Q⁽⁰⁾ − Q⁽ʲ⁾)/det_j — in the channel with the gʲ zero-mode normalisation 1/det_j the twisted-sector LOOP contributes the UNPHASED sector trace, of which the Atiyah–Bott skeleton kept only the phase-weighted insertion part. Everything downstream is exact arithmetic with no dial to turn: the completion-weight identity w_m = Σ_j(1 − i^{jm})/det_j = (0, 3/2, 2, 3/2) = 4h_m = |μ₄|h_m = −4·ch₂(T_m) — the three sphere axions pair through their OWN McKay ch₂ charges, no free scale, no fit; the locks are parameter-free (T₅ = 0 for ANY scale, ratio 4:3 = the δ₁-forced leading ratio REPRODUCED, the T₃ budget forces c = 4 = |μ₄| uniquely); every twisted channel becomes the SAME perfect Okubo square 36⟨x,x⟩²/det_j (T₅ = T₃ = 0 in every sector), the total 45⟨x,x⟩² = (5/4)×36 = Dedekind × Okubo is exactly the unique quartic-free weighting of the Step-11 rigidity theorem; both Step-12 certificates are killed (Φ_T3: 32 → 0, Φ_P: 72 → 0) and the Step-14 slice ψ = 64 is SUPPLIED EXACTLY — the cubic d-channel is not needed (c_d free = 0); controls: wrong scale leaves T₃ = 32 − 8c, the shuffle breaks T₅ and T₃, SO(16) keeps T₅ = 20/T₃ = −40 (the KILL FIRES there: E₈ doubly special), diag(i,i) degenerates to the ℤ₂ target, the ℤ₂/EH anchor passes at scale 2 = |ℤ₂|. The mandatory fence: the completion reading (loop = unphased sector trace with the same zero-mode normalisation) is DECLARED within this step, supported by the δ₁ modular-completion finding, NOT derived from the BCOV integral here — the δ₁ chain has since been decided in Step 19 (the DERIVED chiral measure fails all three testers), the declared-vs-derived measure question has since been decided in Step 21 (the completion reading is now DERIVED at probe level from two independent constructive sources under the typed premises TP-1..TP-4), and the w_m normalisation itself is since derived constructively in Step 24 — the residual [O] narrows to the global BCOV integral beyond the fibre zero-mode factor. Step 18, the a₀ uplift: four coupled centre-count scales [E]/[C] (v517): the M3 milestone preregistered in Step 15 is now EXECUTED, with the preregistered SUCCESS wording ('a log-type correction whose coefficient is tied to the source charge 4 = |μ₄|') met and the KILL (decoupling from the centre count) not fired. The uplift object is the generalized-Legendre-transform kernel χ = log P₄ — the log of the Step-16 family polynomial (the GLT dictionary of Lindström–Roček / Ivanov–Roček, typed [C]); the bridge is exact: the O(2) section is a NULL coordinate (any kernel is harmonic) and the residue identity ∂_x[transform(log η_p)] = 1/r_p matches the V-ledger exactly (flux −4π per centre, source charge 4 = |μ₄|). The correction arrives on FOUR COUPLED CENTRE-COUNT SCALES: (i) the asymptotic kernel log χ = 4·log η + a₂/η² + (a₀ − a₂²/2)/η⁴ + … with coefficient 4 = |μ₄|, the seam-fibre first correction EXACTLY a₀/η⁴ = the (4,±4) multipole (exact m-grading, no log×power terms); (ii) the GLT tower p_{4k} = 4(−a₀)^k with the n ≡ 0 mod 4 selection rule; (iii) the exceptional-locus log χ(0) = log a₀ = 4·log t₀ + i(4φ₀ + π) (response 1 at the locus vs power law at infinity); (iv) the period response d log Π_j/d log a₀ = 1/4 = 1/|μ₄| uniformly, integrating to the monodromy i = ONE Coxeter clock step (the Step-2 monodromy reproduced from perturbation theory), with a₀-rigid ℤ₈ node support and topological (2πi)² fluxes. Controls: the (4,0) multipole is clock-invariant and breaks nothing; the ℤ₂/EH analogue reads 2 = |ℤ₂| on EVERY dial; k = 3, 5 orbits move the coefficient with the centre count (O(6)/O(10) slots); the forbidden family fails both dials (p₃ = 3, e₄ = 0). What stays [O]: the full nonlinear Kähler potential of the resolved A₃ ALE.  Step 19, the derived measure decides — and disagrees with the declared one [E]/[C] (v518): the δ₁ question that Step 17 left open (DERIVE the completion reading from the Harvey–Moore/BCOV τ-integral) is executed as the consolidated δ₁b/δ₁c/δ₁d chain: instead of declaring or scanning a measure, the measure is SOLVED FOR from blockwise SL(2,ℤ) covariance of the dressed 16-component Weil system. Four exact results: (i) the completion closes — the discriminant module of D₅⊕A₃ is ℤ₄×ℤ₄ with q = (5x²+3y²)/8, Gauss sums 2ζ₈⁵×2ζ₈³ = 4 = √16 (signature 0 mod 8 = rank E₈), the Weil relations hold exactly, the diagonal and anti-diagonal Lagrangians are the two E₈ gluings, and the 16-vector theta S-covariance drops the naive 4-character-rule residual from 2.91 = O(1) to ~10⁻³⁹; (ii) the obstruction is a finite μ₄ CHARACTER, identified — the SL(2,ℤ) relation defects are (1,1,1) exactly on all 15 sector pairs (a character of the orbit stabilisers Γ₁(4)/Γ₀(2)±, not a genuine 2-cocycle), on Γ₁(4) explicitly λ(γ) = i^(2B+C/4); (iii) the cancellation exists and is the TWISTED FIBRE BLOCK — G[a,b] = f₁f₃ is an exact identity, the T-fix mechanism is one line of exact phase arithmetic ((−1)·e(−1/6) = e(1/3) = χ₄(T)), and the exact cancellation table reads: bare → order 4, the three sphere axions f₁f₂f₃ → 4, f₂ → 6, f₁f₃ → 1 — only the twistor-fibre content cancels the μ₄ system, with the strict solutions exactly χ₄ (dims (3,3)) and χ₁₀ (dims (1,1)), certified on the dressed functions; (iv) ALL THREE preregistered testers fail — under both derived solutions the integral misses T₅ = 0 (fractions 0.5/0.83), misses the forced 4:3 leading ratio (W₁₃ = 0) and misses −A_fix/the ψ = −64N slice (spreads 1.05/1.47), and the honest (N₁,N₂) orbit rebalance rescues nothing in the positive cone — a genuine KILL on the derived surface. Controls: the ℤ₂/Eguchi–Hanson anchor (residual order 2, cancelled to 1 by the same mechanism), SO(16) (the order-4 supply structurally absent), wrong form/wrong signature (break exactly). Fences [C]: the f₁f₃ = KS-weight identification (the deck weights (1,3) are the twistor fibre weights forced by the Step-15 incidence ledger — an exact match, NOT a complete BCOV derivation) and the kernel-family convention. TENSION, stated honestly: the DECLARED completion reading (Step 17) delivers the ψ = 64 slice and cancels the 32·T₃; the DERIVED chiral measure (this step) fails all three testers — both are exact; the sharp open question was which of the two is the true BCOV measure. Neither result is hidden behind the other — and Step 21 has since decided the question at probe level in favour of the declared reading, sharpening this kill. What remains (WP5e proper [O]): the GLOBAL BCOV/Kodaira–Spencer quantisation on PT/ℤ₄ (the partition function derived from the twistor side — the CFT-side dials and the equivariant skeleton are now both pinned; the exchange sub-branch is closed by Step 12, the full-tensor ledger executed by Step 14, the level-from-flux dial executed by Step 13, the bulk-axion slot built by Step 15, all three back-reaction milestones it preregistered are executed by Steps 16–18 — the Step-15 fence M1–M3 is FULLY WORKED OFF — the δ₁ chain is DECIDED by Step 19 (kill under the derived measure), the measure question is DECIDED at probe level by Step 21 (the declared completion reading wins: single-valuedness derived from F-independence + the Quillen pairing under the typed premises TP-1..TP-4), and the constructive BCOV derivation of the w_m normalisation itself is EXECUTED by Step 24 (1/det_j computed from three independent sources; nothing in w_m is declared any more at that level); the named remaining target narrows to the GLOBAL BCOV INTEGRAL beyond the fibre zero-mode factor; the cubic d-channel stays not needed and its physical-justification question (c_d = 32×60; the 1920 = |W(D₅)| reading look-elsewhere-loaded and convention-contingent, v513) stays dissolved (Steps 19 and 21 do not revive it)), together with the continuum uplift of the Step-10 lattice witnesses (Xu's theorem for the abstract statement; the concrete seam quotient net and the condensed (E₈)₁ net are Costello–Li territory). The route does NOT close SEAM.EQUIV.01 — it IS the keystone's second, quantitative route, named in its own right as SEAM.EQUIV.TWISTOR.01 ([O]; the conditional MMST route is SEAM.EQUIV.MMST.01, closed modulo cited theorems; the parent closes if either route closes and stays [O] as an unconditional claim) — with the ideal fixed, the operator explicit, the limit state constructed, the index chain measured, the KLM triple witnessed, both faces of the inflow anchored, the collapse confirmed full-tensorially with one cubic door open, one level a theorem with its value pinned by the sector counter, the bulk-axion slot a construction with λ̃ = 6 triply pinned, the back-reacted Ω_N closed-form with (2πi)²-integral lockstep periods and the source charge 4 = |μ₄| forced, the twisted KS measure (on the declared completion reading) landing on the unique quartic-free weighting, the a₀ uplift coupled to the centre count on four scales, the δ₁ chain decided — kill under the derived measure — the measure question decided at probe level for the declared reading (Step 21) and the w_m normalisation itself derived constructively (Step 24); the global quantisation (narrowed to the global BCOV integral beyond the fibre zero-mode factor) stays open. Step 20, the real structure exists — and free reflection positivity picks the same family [E]/[O] (v519): the α stage of the OS twistor bridge WOIT.OS.TWISTOR.01 is executed (WOIT.THETA.FREE.01). The classification is complete: exactly TWO families of anti-linear structures on ℂ² normalise the clock ρ = diag(i,1) — family D (z ↦ μz̄, |μ| = 1) satisfies ΘρΘ = ρ⁻¹ EXACTLY with Θ² = +1 (−1 is IMPOSSIBLE: M·M̄ = diag(|μ|², 1) — the clock-inverting family is Kramers-free), inverts the deck and reflects the seam circle with two cut points; family A (z ↦ μ/z̄) centralises the clock projectively and NEVER inverts it, Θ² = ±1 per μ. The role separation is sharp: family A DEFINES the euclidean section — Woit's ρ_tw (ρ_tw² = −1, no real points) is replicated exactly on ℂ⁴ and is family A globally — while family D REFLECTS it (the OS conjugation; σ_std with real points ℝP³). Mark compatibility pins μ ∈ μ₄ (a 4-element torsor, ρΘ_μρ⁻¹ = Θ_{−μ}: two clock orbits); the ℤ₈ spin plane has no phase leaks; in exact Cl(16) the Fock implementer Θ_Fock = U_r∘K has Θ_Fock² = 2⁷ > 0 (normalised +1), inverts the Fock clock tower (V ↦ 4096·V⁻¹, exact scalar) and normalises the deck — while the DECK-induced candidate has Θ_t² = 256·γ₁⋯γ₁₆ = (−1)^F: the v510 split/nonsplit dichotomy IS the Θ² = +1 vs (−1)^F dichotomy, so the deck does NOT furnish the OS Θ — the seam-circle REFLECTION does. Free reflection positivity then holds for exactly that pinned Θ: on the bond cut (marks at the bond midpoints of the 16-Majorana circle) the one-particle Gram is positive definite ((8,0,0), min eigenvalue 1.888e-3 at 40 digits), the even deg ≤ 2 sector is (29,0,0), and at N = 8 the COMPLETE half-sided algebra is RP with no degree truncation; the twist η = +i is forced (η = 1 non-Hermitian); the cut THROUGH sites fails exactly (det = 0, inertia (3,3,1) — a lattice-placement artifact, the continuum Cauchy–Stieltjes control is strictly positive), and the clock-centralising family-A structure fails RP STRUCTURALLY ((4,4,0)): RP and ΘρΘ = ρ⁻¹ select the SAME family. Bonus: the anti-chiral state flips the odd sector to negative definite — an exact free-level shadow of kill test 3. Kill test 1 of the contract does NOT fire at the free/equivariant level and stays live on the interacting algebra; the interacting algebra, gauge-fixed RP, OS reconstruction, chirality and μ₄ incidence remain open contract work (the β/γ milestones named in the contract). No marker moves. Step 21, the measure decision: single-valuedness is derived, the completion reading wins [E]/[C] (v520, CELEST.WP5E.MEASURE.01, ERFOLG-A on the preregistered decision layer — the δ₁e/δ₁f consolidation): the exact invariant subspace of the dressed 16-component Weil system is dim_Q = 8 = 4×2 with EVERY kernel vector in the Q(ζ₈)-span of the two Lagrangian gluings {e_H, e_H'} — both theta = E₄ = the UNPHASED sector trace; single-valuedness of the physical one-loop lattice factor is DERIVED from two independent constructive sources rather than postulated: (source 1, the F-lemma) every strict chiral closure at physical weight carries a nontrivial character (χ₄(T) = e(1/3), χ₁₀(T) = e(5/6), exact; zero strict trivial-character solutions across all eleven dressings), the canonical column-matched member obeys G(γτ) = χ₄(γ)G(τ) pointwise (certificate 3.9e−16, |G| ≥ 59.6), and an exact change of variables turns fundamental-domain independence into ∫ = 0 for EVERY chiral integrand — the Step-19 route was never a well-defined nonvanishing moduli integral (the kill is SHARPENED); (source 2, the Quillen pairing) the doubled hol×antihol transports satisfy |t·conj(t) − 1| < 8.3e−40 on all 15 pairs (|χ₄|² = 1 exactly vs the one-sided χ₄² = e(2/3) ≠ 1), the doubled 256-dim system closes STRICTLY at trivial character and physical weight (nullspaces (28,17) ≥ 11) containing the unphased diagonal AND the physical columns w_b⊗conj(w_b), while hol⊗hol is EMPTY (0,0); the forced unphased numerator reproduces the Step-17 Okubo squares LEVELWISE inside the Step-19 scaffold (exact 4-design on every level n ≤ 8, J-weighted spreads ~5e−41, zero negative cells) with ψ(skeleton) = +0.2302 = −ψ(contact) — the J-weighted mirror of ±64; the declared reading also wins the column canonicalisation (the physical AB column contained EXACTLY in the χ₄ family, canonicalising (N₁,N₂), yet the canonical member fails every tester) and the ℤ₂/EH anchor (all three derived instantiations fail; only the declared reading hits 9⟨x,x⟩² = (1/4)×36 with the scale tooth c = 1/2 = |ℤ₂|h^A1). Typed premises [C]: TP-1 (F-independent moduli integral), TP-2 (nonvanishing — it must source ψ = 64), TP-3 (the Step-19 kernel convention), TP-4 (the Quillen structure of BCOV F₁); the residual [O] — the constructive BCOV derivation of the w_m normalisation itself — is since executed in Step 24, narrowing the [O] to the global BCOV integral beyond the fibre zero-mode factor. No marker moves. Step 22, free OS positivity does not see the bit: the eighth side-blind test [E]/[C] (v521, SEAM.BIT.RPBLIND.01, KILL exactly as preregistered): could the Step-20 machinery DERIVE the Step-2 alignment bit? No — for EVERY δ the two mark-swapping reflections exist (all 20 cut/mark incidence solvesets empty), mark-FIXING reflections exist iff δ = π/2 (solveset cos δ = 0); free RP is δ-blind in the strongest sense (bond-cut Gram inertias (8,0,0) PD with the full sorted spectra IDENTICAL to 40 digits, deviation 0.0; the N = 16 odd-m failure is a placement artifact resolved at N = 32 where all m = 1..7 have bond axes (16,0,0); the continuum OS kernel is exactly 1/sin((s+t)/2) — the axis position drops out identically; the v510/v512 counterwitness passes); Θ existence is δ-blind too (Θ² = +1, deck normalisation, Fock implementability U² = +2⁷/2⁸ > 0 for every δ), and the ONLY δ-sensitive clause (ΘρΘ = ρ⁻¹) is for δ ≠ π/2 not violated but NOT FORMULABLE — it presupposes the bit; the battery has teeth at every δ (family A fails RP structurally (4,4,0); the chirality–η pinning persists (0,8,0)): RP separates the FAMILIES, never the SIDES; structure gained [C]: the OS-reflection group closes to D₄ exactly at the clock point — face #13 of the Step-2 web (12 → 13); the free RP/Θ battery is the EIGHTH side-blind test on the v512 scoreboard (7 → 8); the honest [O] gap is the mark-decorated/interacting state class — the mark-decorated half is since decided side-blind in Step 26 (the NINTH test, 8 → 9; the free-plus-twist class is exhausted, the residual gap narrows to the genuinely interacting A_hol) — the alignment bit remains genuine discrete input. No marker moves. Step 23, the clock is time-like, GSO is the gauge datum [E]/[C]/[O] (v522, WOIT.BETA1.GSO.01, typed UNDECIDED per the frozen preregistration): the β₁ stage of the OS twistor bridge is executed — the one-step clock insertion T₁ = ⟨θ(e_a), α_S(e_b)⟩ violates Hermiticity EXACTLY (witness entry −i/(8·sin(5π/16)) against +i/(8·sin(5π/16)); the pairing is complex-symmetric: 745 matching, 96 anti-matching, 0 violations — 'OS-symmetric' is strictly weaker than Hermitian), so 'positivity after gauge fixing' is not well-posed for the clock reading; the typing is a census: ALL 16 dihedral reflection axes of the NS seam circle invert the clock lift, none commutes — the μ₄ clock IS Woit's euclidean rotation, and the gaugeable part of its ℤ₈ Fock tower is exactly the 2-torsion {1, (−1)^F} = the GSO/fermion-parity ℤ₂ (the free-fermion shadow of the E₈ glue); under that corrected typing gauge-fixed RP HOLDS exactly ((29,0,0) PD at N = 16 deg ≤ 2, min eigenvalue 1.78e−6; (8,0,0) PD on the complete N = 8 half algebra), the site-cut defect survives gauge fixing ((7,9,6) — the bond placement is gauge-invariant information), family A stays indefinite ((17,12,0)), and the Ramond control forces the NS/ℤ₈ tower; kill test (2)'s free shadow does NOT fire, kill test (1) stays discharged also gauge-invariantly; both stay live on A_hol, and the clock-equivariant statement is re-routed through β₂ (OS quotient first, then the clock as reconstructed transfer operator — contract precision (iii)); transparency: the first frozen run scored 6/13 and the preregistered invariant dimension 30 was a combinatorial error (correct census 28+4 = 32), documented in full. No marker moves. Step 24, the w_m normalisation derived: the fixed-point factor is computed, not declared [E]/[C] (v523, CELEST.WP5E.WM.01, verdict ERFOLG per the frozen preregistration): the named remaining target of Steps 17–21 is executed from three independent sources — (route i, Atiyah–Bott) the equivariant mode ledger of the twistor fibre ℂ² equals the closed form 1/((1−q·i^j)(1−q·i^(−j))) exactly in ℚ(i) at every order n ≤ 120, is REGULAR at q = 1 with Abel value (1/2, 1/4, 1/2) = 1/det_j (det_j = det(1−g^j) = (2,4,2)), converges in exact (C,2) Cesàro arithmetic, and the fixed-point factor splits off EXACTLY at every truncation level d ∈ {7,12,25} for the phased (skeleton) AND the Step-21-forced unphased (completion) trace — the Abel-limit contact_j = (Q⁽⁰⁾−Q⁽ʲ⁾)/det_j is the Step-17 contact vector COMPUTED, not declared; (route ii, zeta/Quillen) the spectral determinant of the g^j-twisted circle Laplacian is 4·sin²(πj/4) = det_j exactly (Lerch + reflection formula symbolically, Hurwitz certificates ~1e−41), the Quillen split gives det Δ = det_j² with the real POSITIVE holomorphic section unique via the SU(2) conjugation pairing, and the δ₁f modular block f₁f₃ carries the exact constant term 1/det_b (≤ 5.2e−28); (route iii, the consistency chain) the derived weight reproduces the Step-17 chain number by number (w = (0, 3/2, 2, 3/2) = 4h = −4·ch₂, T₅ = 0 at every scale, 4:3, c = 4 = |μ₄|, squares (18,9,18), total 45⟨x,x⟩², ψ ±64). Negative controls: 1/det² leaves (T₅,T₃) = (2,12) and contradicts Quillen; 1/|1−i^j| leaves ℚ (w″₁ = 1+√2); the ℤ₂/EH anchor PASSES with the same derivation (c = 2 = |ℤ₂|); the SO(16)/D₈ kill fires; diag(i,i) breaks the zeta = AB identity itself; k = 3, 5 weights wander correctly (w_m = m(k−m)/2 = k·h_m) — only k = 4 carries the E₈ chain. Typed premises [C]: TP-REG/TP-Q/TP-NUM/TP-CH. Nothing in w_m is declared any more at this level; what stays [O] is the GLOBAL BCOV integral beyond the fibre zero-mode factor. No marker moves. Step 25, the OS quotient made explicit: the clock gets its spectral calculus [E]/[C] (v524, WOIT.BETA2.OS.01, verdict SUCCESS per the frozen preregistration, [C]-typed per contract precision (iii)): H_phys is explicit and nondegenerate — N = 16 (deg ≤ 2): the 37×37 bond-cut OS Gram exactly Hermitian, parity-block-diagonal, inertia (37,0,0) PD (min eigenvalue 1.7801e−6 at 40 digits), null space {0}, dim 37 = 29⊕8; N = 8 (complete half algebra): (16,0,0) PD, dim 16 = 8⊕8 = 4² — compact euclidean time reconstructs a THERMAL (KMS) representation (exact certificate sin²(3π/8) − sin(π/8)·sin(5π/8) = 1/2); the euclidean rotation becomes a Klein–Landau local symmetric semigroup (τ_k exactly Hermitian on every shrinking domain, chain identities exact, vacuum fixed; positivity pattern = the Step-20 site/bond dichotomy: even steps PSD via T(2j) = A*A, odd steps indefinite with exactly zero one-particle diagonal — the one-step transfer is NOT positive, the chirality datum); the clock is the quarter turn T^(N/4), positive self-adjoint with certified spectral projections (~1e−40) — exactly the calculus the non-Hermitian pre-quotient average of Step 23 could not have — and at N = 8 the compressed clock spectrum is EXACTLY {1, √2−1} = {1, 1/δ_Silver} in both parity sectors (the silver axes of the Step-20 μ₄ torsor return as the clock eigenvalue); the reconstructed rotation group U(s) = exp(isH) is unitary with the group law — per precision (iii) the [C]-operationalisation of 'the clock acting unitarily'; the Step-23 non-Hermiticity is RESOLVED (census (745,96,0) reproduced; every anti-matching entry is a wrap overlap — the pre-quotient failure was exactly the domain/wrap artifact); the pre-declared KMS deviation carries exactly the declared witnesses (no contraction on the compact circle: C(1)/C(3) = 1+√2 = δ_S exactly, det(G−τ₄) < 0); GSO/Θ: the grading survives, the perpendicular torsor mirror descends anti-unitarily with Θ_phys² = +1 on every sector (Kramers-free), θ_cut∘θ_perp = α_(N/2) exactly; controls: site cut indefinite (the contract kill branch fires there), family A no quotient, anti-chiral (8,8,0) — quotient existence itself selects the chiral orientation; kill tests (1)/(2) strengthened, (3) shadow sharpened, none fires; β₃ is next; transparency: run 1 scored 18/20 (a sympy simplify failure on a TRUE π/16 product formula, fixed by a Laurent-polynomial certificate; no criterion changed). No marker moves; WOIT.OS.TWISTOR.01 stays [O]. Step 26, the twist-state kill: the tenth side-blind test, and the free-plus-twist class is exhausted [E]/[O] (v525, SEAM.BIT.TWISTBLIND.01, KILL exactly as preregistered): Step 22's named door — marks decorating the STATE — is decided negative: the NINTH side-blind test on the v512 scoreboard (9 → 10); the σ-gauge arc decoration satisfies σ∘r = σ on the swap axes, so the twisted Gram is a diagonal unitary congruence (spectra identical to 40 digits); the Kadanoff–Ceva 4-twist insertion ω(D·)/ω(D) is well-defined on the N = 32 ladder (ω(D) real nonzero; the N = 16 odd-m degeneration is the checkerboard artifact) and its RP spectra are the FIRST free-class data of the programme that depend on δ at all (pairwise up to 1.05) — yet the INERTIA stays (16,0,0) PD with the same η = +i for every member: the decoration sees δ, the positivity does not; the μ₄ defect at β = π/2 is pure plane gauge, and the genuine Bogoliubov defect at β = π/4 — where Θ-compatibility selects exactly 2 of 16 sign patterns (NS-wrap forced) and the winner is genuinely non-monomial — is still PD with spectra again identical; STRUCTURE THEOREM (mechanism exact): the defect planes never straddle a cut bond, so every Θ-compatible quasi-free mark decoration is RP-spectrally INVISIBLE; sub-results: the defect energy E_def = 1.2752872 is exactly δ-independent (spread 4e−40), the 4-twist Casimir ln|ω(D)| measures δ but is exactly mirror-symmetric under m ↔ 8−m (a family gauge, never a side selector), the twisted parity ⟨Γ⟩_tw = +1 for every member; the harvest: two bit-presupposing π/2 structures (the η flip +i → −i on the mark-fixing axes; the twist frustration of the mark-fixing mirror, (4,4,0) indefinite — the lattice shadow of the Ising twist field's mirror-oddness) — both formulable only on the fixing axes existing iff δ = π/2 (the v512 facet class); controls: the twist-free limit reproduces Steps 20/22 exactly, the site cut keeps failing, the v512 counterwitness is arc-equivalent at N = 16 to the blind member π/4 (no state-level selector can exclude it), a single twist has ω(D) = 0 identically; the free-plus-twist class — everything Wick-computable — is hereby EXHAUSTED: what could still see the bit is only a genuinely INTERACTING A_hol whose OS data are not Pfaffian-reducible to the chiral vacuum; the alignment bit remains genuine discrete input. No marker moves. THE WOIT BRIDGE (chiral Wick rotation and the real structure, [O]): one EXTERNAL programme is close enough in shape to deserve a named paragraph — named precisely so that proximity is not mistaken for confirmation. Woit's Euclidean Twistor Unification (arXiv:2104.05099) observes that the usual Wick rotation is problematic for purely chiral theories and proposes the counter-move: formulate the theory Euclidean-holomorphically on projective twistor space PT and reconstruct the Lorentzian theory from a conjugation structure / boundary values. TFPT's route has, independently, assembled the ingredients such a reconstruction needs — reflection positivity of the seam collar (v379), the OS reconstruction step (the cited AMT/OS selector in FORM.SEAM.MMST.01), the order-4 clock ρ = diag(i,1) (v492), and the seam reflection (Step 20 makes the referent precise: the seam-circle REFLECTION, not the deck/covering involution — the deck, whose freeness is topology v510, carries the (−1)^F Kramers class instead). What is MISSING is stated exactly: a global anti-linear map Θ: A(PT/Γ) → A(PT/Γ) with Θ² = 1 and ΘρΘ = ρ⁻¹ on the interacting open+closed twistorial algebra, together with reflection positivity of the interacting BCOV+SDYM functional — the two inputs of the new central contract WOIT.OS.TWISTOR.01 in the Research Contracts companion. The α-stage status (Step 20, v519): the missing global object now exists at the FREE level — Θ with Θ² = +1 and ΘρΘ = ρ⁻¹ on all four levels (sphere, ℂ⁴, ℤ₈ spin, Cl(16) Fock), with free RP on the seam system selecting the same family; Woit's two inequivalent real structures (ρ_tw and σ_std) are exactly the two families of that classification, in DIFFERENT contract slots. The β₁-stage status (Step 23, v522) sharpens the dictionary once more: the μ₄ clock is Woit's euclidean rotation ITSELF (time-like), the only gaugeable part of its tower is the GSO/fermion-parity ℤ₂, and gauge-fixed RP holds under that typing. The β₂-stage status (Step 25, v524) delivers the first RECONSTRUCTED objects: the OS quotient of the free system is explicit — (H_phys, Ω) positive definite at both levels, the euclidean rotation a positive transfer step with spectral calculus and a reconstructed unitary rotation group (exact clock spectrum {1, √2−1} at N = 8), the compact-circle reconstruction thermal (KMS) with exactly the pre-declared silver witnesses. The interacting statement stays [O] — kill tests 1 and 2 are discharged only at the free level, and until Θ + RP exist on A_hol, the Woit connection remains a strong analogy, not a mathematical integration; nothing in this paragraph is evidence for either programme. No marker moves.",
        formulas: [
          "(\\text{spin clock})^2 = \\text{deck}, \\qquad 8 = 2|\\mu_4| \\ (\\text{the } c_3 \\text{ winding integer})",
          "\\operatorname{Sym}^2(248) = 27000 + 3875 + 1, \\qquad 27000 = 30^3 = (h^\\vee)^3",
          "|s\\rangle = (E^\\theta_{-1})^2|0\\rangle, \\qquad J^a_1|s\\rangle = 0 \\ \\forall\\, 248, \\qquad \\text{dial } 2(1-k)",
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
      {
        label: "Celestial route",
        value: "30 steps, WP5d complete + WP5e-α/β/γ/δ₁/δ₂/ε₂/ε₁ + M1–M3 + the measure decision + the w_m derivation + WOIT α/β₁/β₂ + thermal third leg of c3 + silver demystified + twist-class bit + FK-toy Kill-Test-2 shadow (scoreboard 10)",
        description: "Dedicated section: μ₄ glue = flat ℤ₄ monodromy on the A₃ ALE, clock² = deck, null ideal 27000 = h∨³ derived, deleting operator explicit, GNS limit state constructed, two-interval index μ-chain 16→4→1 measured, split + strong additivity witnessed (all three KLM ingredients on the lattice, Xu's continuum theorem cited not claimed), the q^(−1/3) prefactor + level k = 1 pinned on the CFT side, the equivariant anomaly ledger exact on the twistor side (index bridge f(m) = ch₂, glue defect −78, rigid 32·T₃ residual, a₀ refuted as GS axion), the exchange sub-branch closed with certificate, the full-tensor ledger executed (one cubic d-symbol door open; its c_d = 1920 = |W(D₅)| fingerprint typed look-elsewhere-loaded by v513), 'one level' a theorem with the sector counter pinning k = 1, the O(−2) bulk-axion slot built with λ̃ = 6 triply pinned, the back-reacted Ω_N closed-form with (2πi)²-integral lockstep periods and the lens-forced source charge 4 = |μ₄|, the twisted KS measure (declared completion reading, ch₂-weighted) cancelling the 32·T₃ residual and supplying the ψ = 64 slice without the cubic d-channel, the a₀ uplift coupled to the centre count on four scales, and the δ₁ chain DECIDED — the derived chiral measure (blockwise covariance solved for, the μ₄ obstruction a character cancelled by the twisted fibre block f₁f₃) fails all three preregistered testers, a genuine kill on the derived surface with the v516 tension stated — and the measure question since DECIDED at probe level (v520: single-valuedness derived from F-independence + the Quillen pairing under TP-1..TP-4, the completion reading wins, the kill sharpened), the w_m normalisation since DERIVED constructively (v523: 1/det_j = the Atiyah–Bott/zeta-determinant fixed-point factor, three independent sources, the v516 chain reproduced number by number under TP-REG/TP-Q/TP-NUM/TP-CH), the OS quotient of the free system made EXPLICIT (v524: H_phys PD at both levels, the clock a positive transfer step with spectral calculus — exact N = 8 spectrum {1, √2−1} — and a reconstructed unitary rotation group; the pre-declared KMS deviation with exactly the silver witnesses), and the twist-state door decided side-blind (v525: the tenth side-blind test, 8 → 9; the free-plus-twist class is exhausted) (v492–v525; the v514 fence M1–M3 fully worked off); WP5e proper (the global BCOV quantisation, narrowed to the global BCOV integral beyond the fibre zero-mode factor) stays the single remaining milestone, SEAM.EQUIV.01 stays [O]",
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
        body: "From the closed baryon fraction Ω_b = (4π − 1)β_rad, the asymmetry follows as a cosmological readout. Leptogenesis is operationalised as a falsifiable interface (v169): fed by TFPT's normal-ordered neutrino spectrum and δ_CP = 240°, the thermal estimate η_B ~ 0.96×10⁻²·ε₁·κ_f brackets the observed 6.1×10⁻¹⁰ over M₁ ∈ [3×10⁹, 3×10¹⁰] GeV (a canonical M₁ = 10¹⁰ GeV gives 6.0×10⁻¹⁰, untuned). But M₁ and the washout are scenario inputs, so η_B stays [C]: if a precise Boltzmann solve excluded the window the route falls, not the theory. The cleanest scenario (v212) shares the decuple A_Λ = 10 = |E(K₅)| across both Boltzmann inputs (M₁ ≈ 8.65×10⁹ GeV, m̃₁ = m₃/A_Λ ≈ 5 meV) with no hidden seesaw scale — a sharper [C] route that cuts the free inputs from two to one, not to zero. The full BDP Boltzmann ODE solve confirms the route at the frozen M₁ (integrated κ_f = 0.092 ⇒ η_B = 6.5×10⁻¹⁰ = 1.07× observed, no free M_R dial), so η_B is a consistent [C] downstream readout, not a derivation (the flavored density-matrix solve is the next refinement).",
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
        body: "The candidate is the determinant-line axion of the strong-CP sector; WIMPs are ruled out (no spare E₈ singlet). The misalignment angle is closed; the decay constant is a conjecture. A misalignment estimate (v185) and a converged FULL finite-T solve (experiments/ftransfer/axion_relic/full_finiteT_solve.py: exact nonlinear misalignment, lattice χ(T)∝T⁻⁸·¹⁶, realistic g_*(T), normalised so θ_i=1 gives the standard Ω_a h² ≈ 0.03) now decide the abundance: at the predicted θ_i ≈ 170° hilltop the relic is Ω_a h² ≈ 0.66 — ~5.5× above Ω_DM h² = 0.12 (the observed value is reached only at θ_i ≈ 106°). So as the dominant dark matter the determinant-line axion at (f_a = M_scal/128 ≈ 2.39×10¹¹ GeV, θ_i ≈ 170°) OVER-closes the universe unless there is extra dilution or a lower f_a — a confirmed tension, not the optimistic all-DM. A more robust angle is the spine branch θ_i = π·N_fam/g_car = 3π/5 = 108° (v211): the same solver reaches Ω_DM at θ ≈ 106°, and 108° (the central spine quotient 3/5, no fit) sits there in the MILD-anharmonic regime — 62° below the hilltop, so NOT exponentially sensitive. It is an alternative ansatz to θ_i = π(1−φ_seam) ≈ 170° (mutually exclusive, the full solver decides, DM.AXION.SPINE.01) — a sharper [C] scenario, not a derivation; a converged Ω_a h² outside ~[0.08, 0.16] demotes the branch. That spine angle is exactly the regular pentagon interior angle: since N_fam = g_car − 2, θ_i = (g_car−2)π/g_car, so cos θ_i = (1−√5)/4 = −1/(2φ), and the golden character is unique to g_car = 5 (v429) — the otherwise-unmapped golden/icosahedral E₈ signature (v354/v313) is the geometry of this one external input, a [C] bridge that does not upgrade DM.AXION.SPINE.01. The haloscope coupling is tied to c₃: in the determinant-line normalization the axion–photon anomaly coefficient is g_aγγ = −4c₃ = −1/(2π), y² = 16c₃² = 1/(4π²) ≈ 0.0253 — the same c₃ that fixes α and the birefringence, with no flow freedom (v207); a [C] structural relation (the coefficient, not a parameter-free g_aγγ in GeV⁻¹, which still carries f_a).",
        formulas: [
          "\\theta_i = \\pi(1 - \\varphi_{\\mathrm{seam}}(\\alpha_\\star)) = 170.4^\\circ",
          "\\theta_i = (g_{\\mathrm{car}}-2)\\pi/g_{\\mathrm{car}} = 3\\pi/5 = 108^\\circ \\ (\\text{pentagon}),\\quad \\cos\\theta_i = -1/(2\\varphi)",
          "f_a = \\frac{M_{\\mathrm{scal}}}{2\\dim S^+ |\\mu_4|} = \\frac{M_{\\mathrm{scal}}}{128} \\approx 2.39\\times 10^{11}\\,\\text{GeV}, \\quad m_a \\approx 23.8\\,\\mu\\text{eV}",
          "g_{a\\gamma\\gamma} = -4c_3 = -\\tfrac{1}{2\\pi}, \\qquad y^2 = 16c_3^2 = \\tfrac{1}{4\\pi^2} \\approx 0.0253",
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
        body: "c₃ = 1/(8π) is the gravitational seam constant; the spectral action gives R + R² structurally (G2), and the closed admissible sector is gap-decoupled from the un-built ambient (G5, Decoupling Theorem). Beyond the action, the field equation is now supplied directly by the entanglement first law δS = δ⟨K⟩ (Jacobson; Faulkner et al.), run with TFPT's atoms: v358 gives the linearised G_ab = c₃⁻¹ T_ab with c₃⁻¹ = 8π fixed, and v359 upgrades it to the FULL covariant G_ab + Λ g_ab = c₃⁻¹ T_ab by demanding stationarity at fixed volume (Lovelock's unique divergence-free tensor), so matter conservation ∇ᵃT_ab = 0 is an output. Both coefficients are TFPT-fixed: 8π = 1/c₃ (no free Newton dial; c₃ is triply over-determined — anchor v23, geometry v58, thermodynamics v358) and Λ from α (ρ_Λ = (3/4π²)e^{−2α⁻¹}, v60). So the full covariant field equation is parameter-free at the local level; what remains is the equation-of-state status and the absolute scale v_geo. An external candidate for that missing action level is now quantified (v473–v478): Bianconi's entropic action S_B = −Tr ln(G̃g̃⁻¹) (PRD 111, 066001 (2025)) matches the TFPT Einstein normalisation only at β′_B = c₃/6 = 1/(48π) (pinned exactly), her emergent Λ_G is quadratic-nonnegative and reproduces the v60 branch with the exact target Tr Q² = 32c₃⁴. The R² kill test was then EXECUTED (v475): the raw entropic scalaron is trans-Planckian (m² = 4608π²/17 M̄²), so the light-trace-mode shortcut is dead — and v477 resolved the 13-order gap as a scale-measure datum (one moment condition, satisfied by TFPT's own KMS moment, zero new dials). The compression conjecture is well-posed (v476) with continuum evidence that the state-side modular data flows to the CHM/BW form (v478); it stays [C]/[O] and the equation-of-state typing stays [O]. The global ambient measure (QG.AMB.01) is discharged as a [C] redundancy (v369/v379) — a certification object, not missing dynamics — and the R²/Weyl² Stelle ghost is a Seeley–DeWitt truncation artefact, so perturbative spin-2 graviton unitarity is established [C] (v304/v370/v380). Archive readouts: an independent gravitational ξ = c₃/φ_tree = 3/4 (v152), a Hubble value H₀ = 66.5–67.1 km/s/Mpc from the Λ branch (the tension is NOT relieved, [C]), and a [P] FRG cross-check.",
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
    subtitle: "Targets A–E, the QFT round (F) and the seam round (G): attacking the load-bearing reductions at their weakest transitions",
    abstract:
      "The deliberately adversarial layer: instead of confirming TFPT, this document attacks the load-bearing reductions (Targets A–G) at their weakest logical transitions. Each target runs through one fixed protocol — minimal statement, assumptions, logical chain, counterexample search, limiting cases, alternative structures, verdict. A red-team check asserts an adversarial fact (a counterexample really exists, a hidden assumption is really needed, a firewall really holds); the honest outcome lives in the status of each target, never in a green pass. Verdicts: A reduced (one residual), B/D/E/F survive narrowed, C survives; none broken on the load-bearing surface. Target F audits the perturbative-QFT + scale round (v269–v275): the two attacks that landed are now resolved — the R²/Weyl² gravity Stelle ghost is a Seeley–DeWitt truncation artefact (the untruncated KMS spectral-action Hessian is entire and zero-free, so resummation decouples it ⇒ perturbative spin-2 graviton unitarity established [C], v304/v370/v380), and the anchor over-determination is conditional on the Λ-branch — both folded back into v269/v274. The ambient QG.AMB.01 measure is itself discharged as a redundancy [C] (v369+v379), a certification object rather than a nonperturbative frontier. The new seam round (Target G) banks the ten-test side-blind scoreboard on the alignment bit (v512 web, v521 eighth, v525 ninth, v529 tenth — the bit is not derivable from any tested class and is now physically defined as the twist-class choice, v528) and reports the layer's first toy-level firing: Kill-Test 2 of the OS twistor contract fires on the interacting Fidkowski–Kitaev seam toy — reflection positivity breaks for every g > 0 following the straddle law (RP fails exactly on quartet-straddled cuts, 24/24) — a fenced honest threat that doubles as the first hard selection principle for the interacting algebra A_hol. WOIT.OS.TWISTOR.01 stays [O]; no marker moves.",
    status: "redteam",
    statusLabel: "Adversarial audit",
    pdf: "/papers/tfpt_5_redteam.pdf",
    inputs: [
      "The five load-bearing reductions of the document set, treated as hostile witnesses.",
      "The red-team scripts redteam/rt_A_e8net.py … rt_F_qft4d.py + run_redteam.py.",
    ],
    contribution: [
      "Target A (seam–Calderón = (E8)₁ net): reduced to ONE residual — boundary-net holomorphy + c = 8 (⇔ the index-4 inclusion); E₈ and bulk uniqueness then follow (v83/v87/v89). The free-bulk premise is a fixed-point theorem (quasi-free ⇒ κ₂ₙ=0) and the infinite Schwinger cone is eliminated (cone gap = one-particle gap (2/3)⁶), so the reduction adds no new open content. Net existence and full-cone reflection positivity are discharged to [E] (the CAR second-quantisation functor reduces full-cone RP for every mode to the one-particle contraction, verified on the complete 2¹⁶-dim Fock space; v175), and A2 is an assembled, verified (E₈)₁ certificate. The seam realisation is the keystone SEAM.EQUIV.01 — the raw RP seam IS the holomorphic (E₈)₁ net at τ=i — whose MMST route SEAM.EQUIV.MMST.01 is now closed modulo cited theorems: an explicit gapped lattice model (v367/v368) and the S3 closure stack (v376–v379, ground-state witnesses v489/v490) pin the target at every computable level, Lean-pinned (FORM.SEAM.MMST.01) to the published MMST/Adamo theorems, leaving [O] = the cited continuum scaling-limit existence only (v336) — its 128-spinor extension leg now certified at net level by the peer-reviewed crossed-product package (v469: locality integer h_s = 16/16 = 1 ∈ ℤ, Longo–Rehren 1995 / Böckenhauer 1996 / Böckenhauer–Evans 1998 / KLM μ = 4/2² = 1 ⇒ holomorphic; the AGT/AMT lattice-VOA route demoted to an independent second witness), with the realisation input reduced from model fiat to invariant level R1′ (quasi-free + gap + class D + c₋ = 8 from P1; computed FHS Chern |C| = 1, ν = 16); SEAM.EQUIV.01 stays [O]. Its conformal-deck face QGEO.SYM.01 is a corollary (v335). The full sprint-by-sprint reduction (v176 → v302) is recorded on the /changelog page and in the research contracts.",
      "Target B (g_car = 5 Pascal selection): survives narrowed — residual = the degree-2 truncation (Quadratic Boundary Locality), since tied to the boundary-net premise (v108–v113).",
      "Target C (k = c₃/2, S = A/4): survives narrowed — the replica/EH chain is now exercised numerically at the collar level with the seam's own kernel (v471); the residual is the cited continuum scaling limit (v336) plus the UV-sensitive absolute 1/G anchor; SEAM.THEOREM.01 stays [O].",
      "Targets D/E (one scale v_geo): survive narrowed — CP phases and the EW/reheating/leptogenesis scales are explicitly outside v_geo.",
      "Target F (perturbative 4D-QFT + scale round, v269–v275): survives narrowed — the two attacks that landed are resolved: the R²/Weyl² Stelle ghost is a Seeley–DeWitt truncation artefact (perturbative spin-2 graviton unitarity established [C], v304/v370/v380) and the ambient QG.AMB.01 measure is discharged as a [C] redundancy (v369+v379).",
      "Target G (the alignment bit + the interacting seam): the bit survives ten side-blind derivation attacks (v512/v521/v525/v529) and is physically defined as the twist-class choice with a gauge-robust order parameter (v528, stays formal input); the OS/RP structure survives free and gauge-fixed (v522/v524) while the interacting straddle law (v529) is the named residual risk of the Woit route — Kill-Test 2 fires at toy level under a typed fence, and every candidate A_hol must pass the straddle filter.",
    ],
    notClaimed: [
      "No target is closed by this layer; 'survives' means the statement stands as worded, not that its residual is gone.",
      "A fourth verdict, 'broken', is reserved for an actual failure — none occurred on the load-bearing surface; the first toy-level firing (the straddle law, v529) is reported visibly and fenced, not hidden.",
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
        body: "Level-1 primary counting (det Cartan: D₈ has 4, E₈ has 1) makes holomorphy necessary AND sufficient — a holomorphic c = 8 chiral CFT is the lattice theory of the unique even unimodular rank-8 lattice. Bulk uniqueness is not independent: for a holomorphic net Rep(A) = Vect, so the bulk pairing is unique (machine contrast: SO(16)₁ admits six modular invariants). Target A therefore collapses to one residual that carries no new open content: the free-bulk premise is a fixed-point theorem (v160), the infinite Schwinger cone is eliminated since the cone gap equals the one-particle gap (2/3)⁶ (v161/v162), and the irreducible core {π, v_geo} is a theorem (v165). Net existence and full-cone reflection positivity are discharged to [E] on the complete 2¹⁶-dim Fock space (the CAR second-quantisation functor reduces full-cone RP for every mode to the one-particle contraction; v175), and A2 is an assembled, verified (E₈)₁ certificate (E₈ Cartan even unimodular, det 1). The seam realisation is the keystone SEAM.EQUIV.01 (the raw RP seam IS the holomorphic (E₈)₁ net at τ=i), whose MMST route SEAM.EQUIV.MMST.01 is now closed modulo cited theorems: an explicit gapped lattice model (v367/v368) and the S3 closure stack (v376–v379, ground-state witnesses v489/v490) pin the target at every computable level, Lean-pinned (FORM.SEAM.MMST.01) to the published MMST/Adamo theorems, leaving [O] = the cited continuum scaling-limit existence only (v336) — its 128-spinor extension leg certified at net level by the peer-reviewed crossed-product package (v469: h_s = 16/16 = 1 ∈ ℤ fulfils the Longo–Rehren locality criterion, KLM μ = 1 ⇒ holomorphic; AGT/AMT demoted to an independent second witness), with the realisation input reduced to invariant level R1′; stays [O]. Its conformal-deck face QGEO.SYM.01 is a corollary (v335). The step-by-step reduction (v160 → v302) lives on the /changelog page, not here.",
        formulas: [
          "c(E_8)_1 = \\tfrac{248}{31} = 8, \\quad c(D_5)_1 = 5, \\quad c(A_3)_1 = 3, \\quad c_{\\mathrm{coset}} = 0",
        ],
      },
      {
        title: "Targets B–E — narrowed, with named residuals",
        body: "B: the Pascal ladder 2^{g−1} = Σ_{k≤2} C(g,k) is exactly equivalent to the degree-2 truncation; the residual is the QBL premise, since merged with the boundary-net gate. C: the replica chain is derived and now exercised numerically on the discretized collar with the seam's own kernel (v471) — the kernel premise is discharged at the finite level; what remains is the continuum leg (MMST class, v336) plus the one dimensionful anchor (v152), gate [O]. D: the frozen CP phase survives at +0.98σ with a decision threshold σ_γ ≤ 0.96°. E: v_geo carries the dimensionless theory; EW/reheating scales are typed interfaces.",
      },
      {
        title: "Target F — the perturbative 4D-QFT + scale round (v269–v275)",
        body: "Target F audits the perturbative-QFT + scale round. The two attacks that landed are now resolved: the R²/Weyl² gravity Stelle ghost is a Seeley–DeWitt truncation artefact (the untruncated KMS spectral-action form factor a(p²)=e^{p²/M²} keeps its only pole at p²=0, the spin-2 sector is ghost-free via the Barnes–Rivers decomposition, and the nearest truncation-zero modulus runs to infinity), so perturbative spin-2 graviton unitarity is established [C] (v304/v370/v380); and the anchor over-determination is conditional on the Λ-branch — both folded back into v269/v274. The ambient QG.AMB.01 measure is itself discharged as a [C] redundancy (v369+v379), a certification object rather than a nonperturbative frontier.",
      },
      {
        title: "Target G — the alignment bit and the interacting seam (the first shot that lands)",
        body: "Two red-team questions: can the bit be derived (a hidden redundancy), and can the OS/RP structure be broken? Attack 1 — ten failures, honestly banked: the v512 equivalence web (no local jet sees the side bit), free RP/Θ existence (the eighth side-blind test, v521), every Wick-computable mark-decorated state (the ninth — the free-plus-twist class is exhausted, v525), and the first genuinely interacting, non-Wick-computable dynamics (the tenth: the interaction sees δ massively yet all side data are mirror-equal, v529). Ten tests, ten kills: the bit is not derivable from any tested class and remains genuine discrete input — now physically DEFINED as the twist-class choice (facets #14/#15 extend the web to 15 exact equivalences, flip-axis fraction a gauge-robust order parameter O = 1/2 at m = 4 else 0, η holonomy in principle interferometrically readable; v528, [C] measurement sketch, no marker moves). Attack 2 — where it fires: on the minimal interacting Fidkowski–Kitaev quartic (16-Majorana NS seam circle, 256-dim, exact) Θ exists exactly (Kill-Test 1 does not fire) but reflection positivity breaks in the interacting ground state for every g > 0 — inertia ladder (37,0,0) → (29,8,0), mechanism interference — and the failure pattern is a law: RP fails exactly on quartet-straddled cuts and stays positive definite on quartet-avoiding ones (the STRADDLE LAW, 24/24). The first live ammunition of the layer, fenced (one toy, one interaction class, [C] flat-band parent) — and simultaneously the first hard selection principle: every candidate A_hol must protect RP against exactly this mechanism, a concrete hurdle for the β₃/γ stages. WOIT.OS.TWISTOR.01 stays [O].",
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
        description: "One statement; E₈ and the unique 2D bulk follow. (A) factors into the A2 net-existence + the keystone SEAM.EQUIV.01, whose MMST route SEAM.EQUIV.MMST.01 is now closed modulo cited theorems (lattice v367/v368 + S3 stack v376–v379, ground-state witnesses v489/v490; parent [O]; residual [O] = cited continuum existence (v336) + crossed-product certified extension leg (v469, LR/Böckenhauer/KLM; AGT/AMT second witness); stays [O]). [C]",
      },
      {
        label: "Same-c rival excluded",
        latex: "(D_8)_1 = SO(16)_1: \\; 4 \\text{ primaries}, \\quad E_8: \\; 1",
        description: "Holomorphy excludes the only same-c competitor. [E]",
      },
    ],
    highlights: [
      { label: "Targets", value: "A–G", description: "The load-bearing reductions plus the seam round, attacked" },
      { label: "Broken", value: "0", description: "No target failed on the load-bearing surface; the one toy-level firing (straddle law, v529) is reported fenced" },
      { label: "Straddle law", value: "24/24", description: "Interacting RP fails exactly on quartet-straddled cuts (v529) — honest threat AND the first hard selection principle for A_hol; ten-test side-blind scoreboard on the bit (v521/v525/v529), twist-class definition (v528)" },
      { label: "Target A", value: "closed mod cited", description: "Factors into the A2 net assembly + the keystone SEAM.EQUIV.01, whose MMST route SEAM.EQUIV.MMST.01 is [C] closed modulo cited theorems (lattice v367/v368 + S3 stack v376–v379, ground-state witnesses v489/v490; parent [O]; residual [O] = cited continuum existence (v336) + crossed-product certified extension leg (v469, LR/Böckenhauer/KLM; AGT/AMT second witness); stays [O])" },
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
      "A change of bookkeeping, not new gravitational physics: if gravity is the geometry-channel readout of the seam, then all horizons read the same boundary constant c₃ = 1/(8π). This note collects the readouts — Hawking, de Sitter and Unruh temperature, black-hole thermodynamics, the Page time, scrambling, the Nariai bound, v_GW = c and cosmic birefringence — in seam units, with two genuine compiler fingerprints (1920 = |W(D₅)|, |μ₄| = 4). The Hawking normalisation itself is since MEASURED on the seam: the reconstructed free OS quotient is KMS with β_angle = 2π exact, T_seam = 4c₃ (v526) — temperature joins geometry and anomaly as the third leg of c₃ ([C]-typed reading; the entropy-fraction bridge honestly does not close).",
    status: "horizon",
    statusLabel: "Appendix H — reframe",
    pdf: "/papers/tfpt_horizon_readouts.pdf",
    inputs: ["The seam constant c₃ = 1/(8π) from P1, read as the horizon normaliser."],
    contribution: [
      "All horizon temperatures share one factor, 1/(2π) = 4c₃; black-hole, de Sitter and Unruh share one thermal grammar.",
      "Two genuine compiler fingerprints: 1920 = |W(D₅)| in the Hawking power, and |μ₄| = 4 in the scrambling time.",
      "The boundary transport sub-leading eigenvalue λ₂ = (2/3)⁶ governs both the SM flavor gap and the horizon Page recovery.",
      "The thermal grammar is since measured on the seam itself: the reconstructed free OS quotient has β = N clock steps by detailed balance, β_angle = 2π exact, T_seam = 4c₃ = the Bisognano–Wichmann/Hawking normalisation (v526) — temperature as the third leg of c₃, beside geometry and anomaly ([C]-typed reading).",
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
        body: "Temperature, entropy, power and lifetime all read off c₃, with the Hawking power denominator carrying the compiler fingerprint 1920 = |W(D₅)| (the Weyl group order of D₅). The temperature is not put in by hand: the stationary exterior modular flow Δ^{it} = e^{−2πtK_H} (Bisognano–Wichmann / Tomita–Takesaki) makes the outside state KMS at inverse temperature 2π, so T_H = κ/(2π) — and that 2π is the seam unit 1/(4c₃), reproducing T_H = c₃/M (the seam = horizon modular identification ties to [ρ,Λ_Σ] = 0). The same normalisation is now MEASURED on the reconstructed free seam OS quotient (SEAM.THERMAL.KMS.01, v526): detailed balance gives β = N clock steps at both levels, hence β_angle = 2π and T_seam = 4c₃ — temperature joins geometry and anomaly as the third leg of c₃ ([C]-typed reading: seam euclidean circle = thermal circle of the reconstructed horizon dynamics; the entropy-fraction bridge to the Nariai ledger honestly does not close). The induced R + R² scalaron then corrects the area law to the Wald entropy S_W = (A/4G)(1 + R_h/3M_s²), an exact consequence of f(R) = R + R²/(6M_s²); the leading A/4G is the c₃ area law (1/4 = 1/|μ₄|). [E] for the identities; the black-hole/modular identification is [C].",
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
      {
        title: "Search targets (not claims) — the [O] ansätze",
        body: "Audit-level search ansätze, explicitly [O]: black-hole echoes / horizonless compactness (any near-horizon echo amplitude ratio ≤ (2/3)⁶ ≈ 0.0878; the gravastar maximum compactness C = 3/8 turns this into an echo template, experiments/gravastar-compactness); the Page-curve recovery kernel I ~ (2/3)^{6n} as a falsifiable shape; FRB repeaters as a preregistered search interface for the frozen kernel ratios (experiments/frb-tfpt-signatures); the BH HFQPO ladder tooth — the four published 3:2 twin pairs are consistent with exactly 3/2 but the cluster is cheap (anchored selection null 18.5%, XTE J1859+226 breaks universality at +9.2σ) and mapping the relaxation-ladder step 3/2 onto a two-oscillator ratio is non-canonical; the one discriminating target, a third tooth at ν₃ = (3/2)ν_u (661.5/414/252/363 Hz, integer harmonics forbidden), was never targeted by any published search, and the preregistered archival RXTE PCA scan (executed 2026-07, 77 ObsIDs, sanity gate 11/12, injection-calibrated) finds neither the tooth nor the integer control line anywhere — a well-powered null with 3σ limits 0.53–3.06% rms; the preregistered NICER extension (MAXI J1820+070, 2026-07-22, single-QPO rule) adds a second-instrument null_with_sensitivity (anchor 55.03 Hz reproduced at 3.8σ, tooth limit 0.75% rms below the anchor strength, the ~110.6 Hz integer line at 3.82σ below the 4σ threshold — a sub-threshold excess, no hit; AstroSat/LAXPC blocked): the ladder reading is unsupported but not killed, GR resonance stays favored, the channel is dormant (experiments/hfqpo-ladder; even a future tooth hit would be [C] until the mapping is derived); cosmological coupling k = 3 (w_in = −1, experiments/ccbh-dark-energy, contested); and cosmic spin parity (approximate parity, a frontier watchdog, experiments/cosmic-handedness). Hunting grounds, not foundations.",
        formulas: [
          "\\frac{\\mathcal A_{n+1}}{\\mathcal A_n} \\lesssim (2/3)^6 \\approx 0.0878, \\qquad \\mathcal C = \\tfrac{3}{8}",
          "\\nu_3 = \\tfrac{3}{2}\\,\\nu_u \\ (661.5/414/252/363\\,\\mathrm{Hz}); \\ \\text{integer lines forbidden on the ladder}",
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
      { label: "Third leg", value: "T_seam = 4c₃", description: "Measured on the reconstructed free seam OS quotient: β = N by detailed balance, β_angle = 2π exact (v526) — temperature beside geometry and anomaly, [C]-typed reading" },
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
      "Why the two TFPT inputs leave no free dimensionless compiler dial beyond the anchor structure and π — the one dimensionful scale v_geo and the continuous transfer physics F_transfer remain explicitly typed, not derived. Two layers, kept strictly apart: a structural [E] core (exact, machine-checked identities) — the (g_car, N_fam) = (5,3) skeleton, the triply-forced 8 (geometry = lattice = gravity, with the seam since measured THERMAL: T_seam = 4c₃ on the reconstructed free OS quotient, temperature the third leg of c₃, v526), the order-30 Coxeter cycle, one boundary transport for both flavor and horizon, and a gapped unique attractor — plus one honestly-typed [C] interpretation: the cyclic self-reproduction reading. A new cyclotomic capstone makes this precise: the entire SM structural sector (the three generations, the two CP phases, the orbit/hierarchy ordering) is the cyclotomic field ℚ(ζ₃₀) with Galois group μ₄ × ℤ₂ (degree 8 = rank E₈), forced by the atoms {2,3,5}; this yields zero dimensionless free parameters ({a, π, v_geo} is the complete input) and one new falsifiable prediction — the two CP phases are Galois-locked, δ_PMNS = δ_CKM,lead + π = 240°. The same arithmetic sharpens three frontier points: the CP lock becomes a quantitative kill test (the selected node is the deck order |μ₄|, the prediction band 240° ± ~9°, currently +1.08σ vs NuFIT 6.0); Bisognano–Wichmann shows the μ₄ deck postulate is downstream of the seam being the (E₈)₁ chiral net, collapsing two open bedrock items toward one; and the minimal hypergraph substrate carrying both the E₈ skeleton and the recovery gap is a fibred product (carrier network × 3-fold family cusp = the 5×6 split).",
    status: "synthesis",
    statusLabel: "Origin synthesis",
    pdf: "/papers/origin_theory.pdf",
    inputs: ["The single boundary pair (g_car, N_fam) = (5, 3)."],
    contribution: [
      "The whole integer skeleton from one pair: rank E₈ = g + N = 8, |ℤ₂| = g − N = 2, |μ₄| = (g+N)/2 = 4, and the Pythagorean mass volume Δ_Y = g² = N² + dim S⁺ = 9 + 16 = 25.",
      "The '8' triply forced — geometry (Gauss–Bonnet seam winding) = lattice (rank E₈) = gravity (Hawking/Einstein 8π); and the seam is thermal: T_seam = 4c₃ measured on the reconstructed free OS quotient (v526), temperature the third leg of c₃ beside geometry and anomaly ([C]-typed reading).",
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
        title: "The '8' is triply forced — and the seam is thermal",
        body: "The seam denominator is fixed three independent ways. If the seam is a horizon, the gravitational 8π forces c₃; it must then coincide with the geometric 2|μ₄| (Gauss–Bonnet) and the lattice rank E₈ — all three give 8. The gravity route no longer rests on arithmetic alignment alone: the temperature normalisation is now MEASURED on the seam itself (v526, SEAM.THERMAL.KMS.01) — the reconstructed free OS quotient admits exactly one detailed-balance thermal representation, β = N clock steps at both levels, β_angle = 2π exact, hence T_seam = 4c₃ = the Bisognano–Wichmann/Hawking normalisation; temperature joins geometry and anomaly as the THIRD LEG of c₃ ([C] reading: seam euclidean circle = thermal circle of the reconstructed horizon dynamics; the entropy-fraction bridge honestly does not close; 'the seam IS a horizon' stays [C]). The Seam–Horizon gate (SEAM.THEOREM.01) stays [O]: v150–v152 closed the mechanism and merged the normalisation into the one anchor, and v471 now exercises the replica chain numerically on the discretized collar with the seam's own kernel (real replica sheets n=2,3; BFK/Calderón conically clean on the kernel; the attractor mode's IR divergence regulated by the recovery gap) — the residual retypes to the cited continuum scaling limit (MMST class, the same single residual as SEAM.EQUIV.01) plus the one dimensionful anchor.",
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
        body: "Collecting the arithmetic arc: the affine-E₈ network spectrum carries the atoms {2,3,5} as the angles 2cos(π/k), with the golden ratio φ = 2cos(π/5) the g_car = 5 signature (v313). The static (carrier) and dynamic (recovery) data split by number field — ℚ(√5) for the 5-fold carrier vs ℚ for the rational family rates (v314) — and the order-30 Coxeter element couples them as the cyclotomic compositum ℚ(ζ₃₀), whose Galois group is exactly μ₄ × ℤ₂ of degree 8 = rank E₈ (v315). The whole SM structural sector lives there: the three generations are the μ₃ cube-root orbit (Galois-refined 1+2, the fixed one the attractor, v317) and the two CP phases the ζ₆ family-factor data (v316). The magnitude seed φ₀ itself reduces to a pure function of π, so there are zero dimensionless free parameters — {a, π, v_geo} is the complete input (v318). [E] arithmetic / [C] the raw-seam realisation closed modulo cited theorems (residual [O] = the cited MMST continuum existence only, v336; extension leg on the peer-reviewed crossed-product package, realisation at invariant level, v469; stays [O]).",
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
        body: "One step links the two open bedrock items. The μ₄ clock is literally a geometric rotation, ρ = diag(iⁿ) = exp(i(π/2)L) with L = diag(n) the seam rotation generator, so μ₄ ⊂ U(1)_rot. For a rotation-covariant seam covariance C = f(L) the modular Hamiltonian K = log((1−C)/C) = g(L) is itself a function of L, so the modular flow commutes with all rotations and the μ₄ clock is a modular symmetry for free — the discriminator: a mere period-4 curvature preserves the clock but its flow is not geometric ([K,L] ≠ 0). This is the Bisognano–Wichmann content: given the seam is the (E₈)₁ chiral net (v308), BW/Hislop–Longo make the vacuum modular flow geometric, so QGEO.SYM.01 (ω∘ρ = ω) is downstream of SEAM.EQUIV.01 + a rotation-invariant vacuum — not an independent axiom (v323). On the exactly solvable four-interval realisation of the four marks the invariance is manifest at the state level (ρCρ⁻¹ = C at machine precision, with the fermionic clock the order-8 double-cover lift ρ⁴ = −1; v480) — the mechanism in the cited multilocal free-fermion class, the raw-collar premise unchanged. And the rotation-invariant vacuum is itself a conformal-NET AXIOM (a chiral net's Möbius-covariant vacuum is the unique invariant positive-energy vector), so QGEO.SYM.01 is in fact a COROLLARY of SEAM.EQUIV.01 with no extra premise (v335, Lean qgeoSymIsCorollary) — the two open bedrock items collapse to ONE, its MMST route SEAM.EQUIV.MMST.01 now closed modulo cited theorems (lattice v367/v368 + S3 stack v376–v379, ground-state witnesses v489/v490). [E] construction / [C] linkage / [O] residual (= the cited MMST continuum scaling-limit existence only, v336; extension leg on the peer-reviewed crossed-product package, realisation at invariant level, v469; stays [O]).",
        formulas: [
          "\\rho = \\operatorname{diag}(i^n) = \\exp\\!\\big(i\\tfrac{\\pi}{2}L\\big), \\quad C = f(L) \\;\\Rightarrow\\; K = g(L), \\quad [K,L] = 0",
        ],
      },
      {
        title: "The minimal hypergraph substrate is a fibred product",
        body: "The rewrite question made concrete. The pure (2,3,5) network gives only the Coxeter skeleton and the golden 5-fold angle; the recovery rate (2/3)⁶ is provably not in its adjacency spectrum (v312). But the smallest substrate that carries everything is a product: the carrier network T_net = (A+2I)/4 (attractor = Kac marks = the E₈ skeleton) fibred by a 3-node family cusp T_cusp = diag((1−w)⁶), w ∈ {0,1/3,2/3} (spectrum {1,(2/3)⁶,(1/3)⁶}). The fibred T_net ⊗ T_cusp carries both at once: top eigenvalue 1 with eigenvector marks ⊗ (w=0) (skeleton × democratic cusp), and (2/3)⁶ as a genuine eigenvalue (network attractor × cusp subleading). This is the cyclotomic split made dynamical — substrate = carrier × family = the 30 = 5×6 of v315, with the recovery gap living entirely in the family factor (v324). [E] construction / [C] reading.",
        formulas: [
          "T = T_{\\mathrm{net}} \\otimes T_{\\mathrm{cusp}}, \\quad \\operatorname{spec} \\ni 1\\ (\\text{marks}\\otimes w{=}0) \\ \\text{and}\\ (2/3)^6\\ (\\text{marks}\\otimes w{=}\\tfrac13)",
        ],
      },
      {
        title: "One coupled local rule unifies carrier × family",
        body: "The three hypergraph modules (v299 carrier growth, v327 branching rule M, v324 fiber product) merge into a single rewrite on a 9×3 labelled grid. One micro-step = network lazy diffusion on each cusp column plus M on each node's family vector (T_micro = T_net ⊗ M, purely local on 27 cells). The joint attractor is marks ⊗ (w=0); one clock hand (2N_fam = 6 family steps) carries recovery (2/3)⁶; v324's T_net ⊗ T_cusp emerges as the cusp-readout basis; v299's growth E₆→E₇→E₈→Ê₈ is unchanged with the fiber attached. The cusp weight 2/3 = |ℤ₂|/N_fam is derived from the rule arity (v327); what remains non-graph-spectral for a full-structure rewrite is the analytic seed φ₀ alone (v312). [E] mechanism unified / [O] seed + φ₀.",
        formulas: [
          "T_{\\mathrm{micro}} = T_{\\mathrm{net}} \\otimes M, \\quad \\text{attractor} = \\mathrm{marks} \\otimes e_0, \\quad \\text{recovery after one hand} = (2/3)^6",
        ],
      },
      {
        title: "The full transfer spectrum from one lazy walk — forced by the clock",
        body: "The uniform rule generates only λ₂ — its zero mode persists under every power, so no iterate reaches the verified third transfer mode (1/3)⁶. The gap closes with a uniqueness statement (v486, HYP.REWRITE.02): for the symmetric rule M(s,h) (one absorbing family channel + ℤ₂ pair) the survival spectrum is {s+h, s−h}, and demanding the physical pair {2/3, 1/3} forces uniquely (stay, hop, leak) = (1/2, 1/6, 1/3) = (1/|ℤ₂|, 1/(|ℤ₂|N_fam), 1/N_fam) — the lazy ℤ₂-pair walk, every rate an atom expression; over the order-6 hand eig(B⁶) = {(2/3)⁶, (1/3)⁶} exactly, so both decay gaps (6ln(3/2) recovery, 6ln3 subdominant) have one recursive generator. And the split selection is not a choice (v487, HYP.REWRITE.03): the lazy rule's one-step spectrum is exactly the complete resummed-clock ladder below the wall (v124: {1−n/3 : n = 0,1,2}), while the uniform rule collapses its odd mode onto the wall (0 = 1−3/3); deck parity IS the rung index ([B,σ] = 0, σ-even → rung 1, σ-odd → rung 2 — the structural home of the parity assignment the FRB comb searches test), and ladder faithfulness + ℤ₂ equivariance + rates ≥ 0 force both the split and the assignment uniquely (the swap needs hop = −1/6 < 0). Corollary: ω₁/ω₂ = rate(2)/rate(1) = log_{3/2}3 — the two comb tones of the empirical program are one bend apart. [E] uniqueness + generation + forcing / [O] the arity {2,3} (anchor input) and the clock's semiclassical derivation (R1).",
        formulas: [
          "\\operatorname{eig}M = \\{1,\\tfrac23,\\tfrac13\\} = \\{1-\\tfrac{n}{N_{\\mathrm{fam}}}\\}_{n=0}^{2}, \\quad \\omega_1/\\omega_2 = \\log_{3/2}3",
        ],
      },
      {
        title: "The φ₀ leading term is icosahedral combinatorics",
        body: "The tree-level retained seed φ₀^tree = 1/(6π) equals F/(4hπ) on the icosahedral hypergraph (F = 20 triangular hyperedges, h = 30, |Aut| = 120): equivalently (F/(g_car·N_fam))·c₃, with F/h = |ℤ₂|/N_fam = 2/3 (the same survival ratio as v327). Gauss–Bonnet consistent with c₃ = 1/(|ℤ₂|·4π). The puncture 48c₃⁴ remains analytic, not a graph fraction (v396). Its geometric side is now EXACT (v483, HYP.PHI0.GEOM.01): every twisted heat trace of the flat τ=i pillowcase is a t-independent rational (σ/ρ traces = 1 = the Atiyah–Bott fixed-point counts; contact term exactly 1/2; clock-equivariant trace exactly 1), so the π⁻⁴ in 48c₃⁴ = 3/(256π⁴) cannot come from flat orbifold geometry at any order — it must sit in the per-mark coupling weight (4 = |μ₄| insertions of weight c₃; the bare 1/(2π) 4-cycle differs by the exact rational 3/16). The puncture target narrows from 'derive the term' to that one rule — and that rule is itself not a new unknown (v484, SEAM.CONTACT.UNIT.01): 'c₃ per insertion' IS the KMS seam unit 2π = 1/(4c₃) with 1/4 = 1/|μ₄| (one bare boundary propagator orbit-averaged over the four marks), derived on the seam circle for the finite cycle sector; the puncture target and ALPHA.QUILLEN.EXACT.01 merge into one remaining analytic step (diagonal ζ-renormalisation + multiplicity matching, 48 = Ω_adm / 41 = 10b₁) — settled at the computable level by v485: the renormalised diagonal vanishes exactly at the KMS seam circumference, the mark determinant resums closed-form (det(I−uC) = (1−4u)(1+2u)², BFK route), and 48/41 are one state set under two response weights; the remaining [O] is the abstract-seam ζ-det identification, a face of SEAM.EQUIV.01 alone. [E] leading term + geometric side + contact unit + diagonal/resummation / [C] reading / [O] the keystone face.",
        formulas: [
          "\\varphi_0^{\\mathrm{tree}} = \\frac{F}{4h\\pi} = \\frac{F}{\\gcar\\Nfam}\\,c_3 = \\frac{1}{6\\pi}",
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
        description: "c₃ is the unique value with the Bekenstein–Hawking 1/4; the replica chain is exercised on the discretized collar (v471), the gate stays [O] (continuum leg + anchor). [I/L]",
      },
    ],
    highlights: [
      { label: "Skeleton", value: "(5,3)", description: "One pair generates the integer alphabet" },
      { label: "McKay bedrock", value: "2I → Ê₈", description: "Why {2,3,5}: E₈ is the icosahedral top (marks = irrep degrees)" },
      { label: "Seam = E₈ singularity", value: "8 P¹'s", description: "du Val resolution of ℂ²/2I; link = Poincaré sphere S³/2I — a model for the seam realisation (SEAM.EQUIV.01, v232); the graph→geometry bridge is now Kronheimer-cited (ALE hyper-Kähler quotient of the marks quiver, v479)" },
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
      "After the compiler closure the live residual is Rest = v_geo ⊕ G_net ⊕ F_transfer (the historical labels U_wall / G_metric / F_frontier are kept only for ledger continuity). This note turns the open interfaces into contracts: a numbered chain of lemmas, the single theorem that closes each, and — for every step — whether it is machine-certifiable today. Priority: the selector-triangle pairings and the v_geo scale anchor first (finite, algebraic, falsifiable), then the G_net inclusion theorem (deep analytic programme); F_transfer is the downstream interface. The emergent-QFT round (v238–v261) then assembles the boundary QFT into one relative object TFPT_QFT = (A_Σ, ω_Σ, Δ_Σ, ρ, A_F, H_F, D_F, J, γ, S_rel): the finite Dirac is a covariance induction of the seam KMS state, the spectral-action cutoff is that KMS weight (f₂/f₀ = 1), and the seam, carrier-16 and E₈ live on one Kummer/K3 surface — the Modular Spectral Closure, complete modulo a single named theorem, the Seam Equivalence Theorem (SEAM.EQUIV.01): the raw RP seam state is the holomorphic (E₈)₁ boundary net at τ=i, with ambient QG kept separate. Since 2026-07-22 the keystone carries two named routes (SEAM.EQUIV.MMST.01, closed modulo cited theorems; SEAM.EQUIV.TWISTOR.01, open — the parent stays [O] as an unconditional claim), the celestial contract CELEST.SEAM.01 is headed 'the celestial and twistor continuum route' with an object diagram, an exact group-extension definition and an A₃ role table, and a new central contract WOIT.OS.TWISTOR.01 states the actual bridge from compiler to physics (the Θ real structure + interacting reflection positivity + OS reconstruction), with seven preregistered kill tests. Both continuum contracts now carry EXECUTED stages: CELEST.SEAM.01 has WP1–WP5d, the WP5e α/β/γ/δ₂/ε₂/ε₁ stages, all three back-reaction milestones M1–M3 (v515–v517), the δ₁ chain DECIDED (kill under the derived measure, v518), the declared-vs-derived measure question DECIDED at probe level for the declared completion reading (v520) and the w_m normalisation DERIVED constructively (1/det_j the Atiyah–Bott/zeta fixed-point factor from three sources, ψ = 64 reproduced, v523) — nothing in the measure chain is declared any more at that level, the residual [O] is the global BCOV integral beyond the fibre zero-mode factor; WOIT.OS.TWISTOR.01 has α executed (Θ exists with Θ² = +1 and ΘρΘ = ρ⁻¹ on all four levels, free RP selects the same family, v519), β₁ executed (the μ₄ clock is the euclidean rotation, the gaugeable datum is the GSO ℤ₂, gauge-fixed RP holds, v522) and β₂ executed (the OS quotient explicit, H_phys positive definite at both levels, the clock a positive transfer operator with spectral calculus, v524) — β₃ next, under the straddle-law constraint of the first interacting seam toy (Kill-Test 2 fires at toy level, v529): an honest threat and the first hard selection principle for A_hol. Both contracts stay [O]; no marker moves.",
    status: "contracts",
    statusLabel: "Open research interfaces",
    pdf: "/papers/tfpt_research_contracts.pdf",
    inputs: [
      "The closed compiler and the three named residual interfaces (v_geo, G_net, F_transfer) from the central status card.",
    ],
    contribution: [
      "Flavor interface (historically U_wall) — reduced to the selector triangle: the dual normal pair (d,n) forces R columnwise (v136/v139), the quark ratios are closed (Readout Rigidity), and the only remainder is the absolute amplitude U_point = the one overall scale v_geo (the same dimensionful anchor as gravity's 1/G).",
      "G_net: IR tier closed under RP + gap (Decoupling Theorem, Δ_eff = 1.648 > 0); the metric sector reduces to the rigorously-constructed (E₈)₁ lattice net (c = 8 = 5 + 3, conformal embedding (D₅)₁×(A₃)₁, coset c = 0), and the ambient measure (QG.AMB.01) is discharged as a redundancy [C] (v369+v379). The closing statement is the index-4 seam-net inclusion via the keystone SEAM.EQUIV.01, whose MMST route SEAM.EQUIV.MMST.01 is now closed modulo cited theorems: an explicit gapped lattice model (v367/v368) and the S3 closure stack (v376–v379, ground-state witnesses v489/v490) pin the target at every computable level, Lean-pinned (FORM.SEAM.MMST.01) to the published MMST/Adamo theorems — the only [O] residual is the cited continuum existence of the scaling limit (v336); its 128-spinor extension leg is certified at net level by the peer-reviewed crossed-product package (v469: locality integer h_s = 16/16 = 1 ∈ ℤ, Longo–Rehren 1995 / Böckenhauer 1996 / Böckenhauer–Evans 1998 / KLM μ = 4/2² = 1 ⇒ holomorphic). Two 2026-07-14 reductions sharpen the same residual without moving it: the R3 'attractor graph IS the du Val singularity' bridge is discharged to Kronheimer's 1989 ALE hyper-Kähler quotient theorems with every finite input a compiler output (v479, SEAM.KRONHEIMER.01 — the premise transforms to 'the raw seam supplies the ALE/orbifold datum'), and the four μ₄ marks are the exactly solvable four-interval multilocal free-fermion modular geometry (v480, QGEO.MULTILOCAL.01: binary clock ρ⁴ = −1, exact sector decoupling, ω∘ρ = ω manifest at the state level; Casini–Huerta/Longo–Xu/Rehren–Tedesco/KLM cited), with the AGT/AMT lattice-VOA route demoted to an independent second witness, and the realisation input reduced from model fiat to invariant level R1′ (quasi-free + gap + class D + c₋ = 8 from P1; computed FHS Chern |C| = 1, ν = 16, the Kitaev 16-fold-way class; Lean parallel route seamResidualClosed'). SEAM.EQUIV.01 stays [O].",
      "The quark ratio c_u/c_d = 55/117 is closed (Readout Rigidity); the '11' is the Pascal sum 16 − g_car.",
      "Modular Spectral Closure (v258–v261): the boundary QFT is one relative object reduced to one premise. The finite Dirac is the modular/covariance induction of the seam KMS state ([D_F] = [D_Σ]⊗[K_car]); the spectral-action cutoff is that same KMS weight (f₂/f₀ = 1); and the seam (pillowcase), carrier-16 (Kummer nodes) and E₈ (H²(K3) = U³⊕E₈(−1)²) are facets of one Kummer/K3 surface. So the whole layer is QFT-complete modulo cited theorems (the MMST route SEAM.EQUIV.MMST.01) via the single keystone SEAM.EQUIV.01 (the raw RP seam IS the holomorphic (E₈)₁ net at τ=i; its conformal-deck face QGEO.SYM.01 is now a corollary, v335), with the ambient measure QG.AMB.01 discharged as a redundancy [C] (v369+v379) — a certification object, not missing dynamics. The perturbative 4D layer is built: the spectral-action S-matrix is Epstein–Glaser-constructible with the SM one-loop β-coefficients (41/10, −19/6, −7) from the carrier content, LSZ-bridged with one-loop unitarity for matter+gauge; the R²/Weyl² gravity sector's Stelle ghost is a Seeley–DeWitt truncation artefact (the untruncated KMS spectral-action Hessian is entire and zero-free, so resummation decouples it ⇒ perturbative spin-2 graviton unitarity established [C], v304/v370/v380). The single mass anchor is over-determined (gravity = dark energy to 0.11%, v274). SEAM.EQUIV.01's MMST route SEAM.EQUIV.MMST.01 is closed modulo cited theorems: an explicit gapped lattice model (v367/v368) and the S3 closure stack (v376–v379, ground-state witnesses v489/v490) pin the target at every computable level — Lean-pinned (FORM.SEAM.MMST.01, SeamScalingLimit.lean) to the published MMST/Adamo theorems — leaving [O] = the abstract continuum scaling-limit existence only (v336), a cited published theorem (closed modulo a cited theorem, not solved; extension leg on the peer-reviewed crossed-product package, realisation at invariant level, v469; stays [O]). The full sprint-by-sprint reduction (v269 → v302) lives on the /changelog page, not here.",
    ],
    notClaimed: [
      "U_point is not a free transcendental input but the single overall scale v_geo (shared with 1/G); the strict claim is only that one dimensionful anchor remains.",
      "G_net's seam keystone (SEAM.EQUIV.01) is closed modulo cited theorems only on its MMST route (SEAM.EQUIV.MMST.01), not solved — the twistor route SEAM.EQUIV.TWISTOR.01 and the unconditional parent stay [O]; the residual is the cited continuum-existence theorem (v336; extension leg on the peer-reviewed crossed-product package, realisation at invariant level, v469; stays [O]); and the ambient measure QG.AMB.01 is discharged as a redundancy [C] (v369+v379), not an open hole. Neither affects the bounded IR claim — full QG closure is a certification layer, not a prerequisite for testing the SM and cosmology readouts.",
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
        body: "The goal is the reflection-positive projective-limit measure over the diffeomorphism-quotiented metric sector. The Seeley–DeWitt R + R² terms (G2) and gap dominance (G5, the Decoupling Theorem) are certified, and the ambient measure is holographically reduced to a finite seam-boundary (Calderón) measure. The closing statement is the Simple-Current Extension Theorem (v154): A = (D₅)₁⊗(A₃)₁ extended by the isotropic glue L = ⟨(1,1)⟩ has index |L| = 4 = |μ₄|, c = 5+3 = 8 and μ(B) = 1 ⇒ holomorphic ⇒ B ≅ (E₈)₁ — exact algebraically, with the explicit target net checked (16 Majoranas, ω_k = |k|, 248 = 120+128, character E₄/η⁸; v156). The free-bulk premise is not postulated but forced by rigidity: a holomorphic c=8 theory has no marginal (1,1) deformation and its lowest interaction is irrelevant (dimension 2), so freeness is a stable isolated fixed point (v157/v158); net existence and full-cone reflection positivity are then discharged to [E] on the 2¹⁶-dim Fock space (v175). The seam realisation is the keystone SEAM.EQUIV.01 (the raw RP seam IS the holomorphic (E₈)₁ net at τ=i), whose MMST route SEAM.EQUIV.MMST.01 is now closed modulo cited theorems: the lattice model (v367/v368) and the S3 stack (v376–v379, ground-state witnesses v489/v490) pin the target at every computable level, Lean-pinned (FORM.SEAM.MMST.01) to the published MMST/Adamo theorems, leaving [O] = the cited continuum scaling-limit existence only (v336). Its conformal-deck face QGEO.SYM.01 is a corollary (v335). The classical field equation supplied by entanglement equilibrium (v358/v359) is honestly typed 'equation of state, not a from-action quantisation' [O]; an external candidate for that missing action level — Bianconi's entropic action S_B = −Tr ln(G̃g̃⁻¹) (Gravity from entropy, PRD 111, 066001 (2025), arXiv:2408.14391) — is quantified in a dedicated keybox (v473): the carrier Hodge count 1+5+10 = 16 = dim S⁺ (the 16 requires the five-slot carrier), her free constant pinned exactly at β′_B = c₃/6 = 1/(48π), her emergent Λ quadratic-nonnegative reproducing the v60 branch with exact target Tr Q² = 32c₃⁴, and the R² kill test (gap exactly 3(8π)⁹ ≈ 10¹³) pre-registered; the compression conjecture P_Σ(G̃g̃⁻¹)P_Σ = Δ_Σ^{1/2} stays [C] and nothing closes. The operator level is executed in v474: the D₅ Clifford/spinor structure is exhibited on the carrier Fock space Λ•ℂ⁵ (ten exact gammas, the 45-dim so(10) preserving the 16-dim even subspace), the Hodge fold is identified as the 5 → 5̄ conjugation (her fiber 1+5+10 becomes the GUT 16 = 1+5̄+10), and the Q-target is decided — integer supports exactly {|ℤ₂|, rank E₈, 2^g_car} with minimal uniform q = c₃², the naive pair-block (10) reading killed. The R² kill test is executed in v475: on the maximally symmetric background the exact vacuum action is 3βR + (17/24)β²R² (tensorial factors now exact), giving a TRANS-PLANCKIAN raw scalaron m² = 4608π²/17 M̄² (≈ 51.7 M̄) — the light-trace-mode reading is dead, a viable mechanism must supply exactly (72/17)(8π)⁹ ≈ 1.7×10¹³ in mass², and KMS-spectral renormalisation is the only surviving R² route; the Lorentzian-positivity caveat now has an explicit timelike witness (1 − αv² ≤ 0). The compression conjecture (AP2) is made well-posed in v476: on a pure bulk the literal operator-side reading P f(C) P is ill-posed (f singular on spec {0,1}), so the state-side reading — build Δ_Σ from the compressed relative metric — is forced (matching Bianconi's own local construction); the mismatch between the readings is exactly second order in the cross-cut correlations and gap-suppressed, converging in the gap-dominated regime where TFPT operates; AP2 itself stays [O]. And the surviving R² route is typed as ONE moment condition in v477: the entropic action is the flat scale-integral of relative heat-kernel actions (Frullani), TFPT's S_rel,χ is the same family at one KMS scale — demanding m² = c₃⁷M̄² forces exactly μ₂/μ₁² = (72/17)(8π)⁹, with the closure identity (4608π²/17)/((72/17)(8π)⁹) = c₃⁷ holding identically: the 13 orders are a scale-measure datum which TFPT's own KMS moment (v36 f₀) fixes correctly — zero new dials, consistency not derivation [C]. First computable steps on the two remaining legs land in v478: the compressed critical state's modular data flows to the CHM/Bisognano–Wichmann geometric form (Calabrese–Cardy c_est → 1 at 2×10⁻⁴, CHM parabola corr → 0.99, even bands exactly zero) — the bridge's modular side meets TFPT's Einstein-derivation input (v323/v358) in the continuum limit; and the measure condition reduces to one exact KMS time t₀ = ln(72/17) + 9ln(8π) = 30.461, with the h(E₈) = 30 near-miss explicitly declined (no-free-pattern rule) — both legs stay [O]. The step-by-step reduction (v160 → v302) is on the changelog.",
        formulas: [
          "a_2 = -\\tfrac{R}{3}, \\qquad a_4\\big|_{R^2} = \\tfrac{R^2}{72}",
          "[\\,(E_8)_1 : (D_5)_1\\times(A_3)_1\\,] = 4 = |\\mu_4|",
        ],
      },
      {
        title: "The Modular Spectral Closure — the boundary QFT as one relative object",
        body: "On top of G_net the boundary QFT is assembled and collapsed to ONE relative object TFPT_QFT. The emergent-QFT skeleton is read off the seam: modular flow σ_t = Δ^{it} is KMS at β=1 (the seam unit 2π = 1/(4c₃), v239); GNS/OS gives a positive H_OS = −log T with gap Δ = 6log(3/2) (v240); particles are the carrier DHR sectors (Gauss–Milgram returns c = 8, v241/v242). The carrier half-spinor 16 is exactly one anomaly-free SM generation (sin²θ_W = 3/8, v245); the plain SM not unifying (v246) is resolved natively by a carrier Pati–Salam UV branch ({1,10,16,45}, no 126, v247–v249), realised as a 96-dim KO-6 spectral triple with one Higgs doublet and no junk (v252/v254). Three closures collapse the layer: D_F is the modular/covariance induction of the seam KMS state (v258), the spectral cutoff IS that KMS weight (f₂/f₀ = 1, v259), and seam, carrier-16 and E₈ live on one Kummer/K3 surface (v260) — certified by one number 4 = [B:A] = |μ₄| = 2χ (v261). So the boundary QFT is closed as one relative object modulo cited theorems via SEAM.EQUIV.01's MMST route SEAM.EQUIV.MMST.01 (Lean FORM.SEAM.MMST.01; pinned at every computable level by the lattice model v367/v368 and the S3 stack v376–v379, ground-state witnesses v489/v490; residual [O] = the cited continuum existence only, v336); the ambient measure QG.AMB.01 is discharged as a [C] redundancy (v369/v379). 4D-GUT is not claimed by default (E₈ is the audit hull); the Pati–Salam branch is a separately-typed, falsifiable UV option with a proton-decay kill test (v265). The full derivation is in the PDF.",
        formulas: [
          "\\mathsf{TFPT}_{\\mathrm{QFT}} = (\\mathcal A_\\Sigma,\\,\\omega_\\Sigma,\\,\\Delta_\\Sigma,\\,\\rho,\\,A_F,\\,H_F,\\,D_F,\\,J,\\,\\gamma,\\,S_{\\mathrm{rel}})",
          "[D_F] = [D_\\Sigma]\\,\\widehat{\\otimes}_{(E_8)_1}\\,[\\mathcal K_{\\mathrm{car}}], \\qquad f = f_\\Sigma \\Rightarrow f_2/f_0 = 1",
          "4 = [B{:}A] = |\\mu_4| = 2\\chi = |(\\mathbb Z/2)^2|, \\qquad H^2(\\mathrm{K3}) = U^3 \\oplus E_8(-1)^2",
        ],
      },
      {
        title: "CELEST.SEAM.01 — the celestial and twistor continuum route (fourth contract)",
        body: "A new research contract (alongside U_wall, G_metric and CONTRACT.F.01), typed as a numbered chain of work packages with pre-registered kill tests — not a claim. THE OBJECT DIAGRAM (read this first; one row per arrow — where mathematics ends and physics begins is visible at a glance): (Σ, μ₄, ρ, Θ) → P¹∖μ₄ [E] (the SEAM.MARKS chain: four marks, clock, cross-ratio 2, τ = i pillowcase; v168/v214/v216/v180, bit reduction v506/v507/v510/v512; kill: a fifth mark, a non-order-4 clock, or a marks-preserving root without flag transitivity) · P¹∖μ₄ → ℂ²/ℤ₄ [E] (CELEST.WP1.01/WP2.01: the glue is the flat ℤ₄ monodromy on the A₃ ALE, clock = Kähler U(2) phase, clock² = deck; v492/v493; kill: equivariant-sector closure failure or a surviving shape modulus) · ℂ²/ℤ₄ → PT/Γ [E]/[C] (CELEST.WP5E.*: equivariant twistor uplift — anomaly ledger, level-from-flux, axion slot, back-reacted Ω_N, twisted KS measure, a₀ uplift, the δ₁ decision; v505/v509/v511/v513/v514/v515/v516/v517/v518; kill: the preregistered level kill; the M1–M3 kills were evaluated by v515/v516/v517 and did not fire; the δ₁ kill FIRED on the derived measure (v518) — the declared/derived measure tension is the named [O]) · PT/Γ → A_hol [O] (the INTERACTING holomorphic algebra: global BCOV+SDYM quantisation, WP5e proper — target of WOIT.OS.TWISTOR.01; kill: anomaly mismatch at the Costello–Li grade) · A_hol →_OS A_Mink [O] (OS reconstruction with the real structure Θ — the WOIT.OS.TWISTOR.01 target; the free-collar RP/OS witnesses v379/FORM.SEAM.MMST.01 are the free anchor only; kill: the seven WOIT.OS.TWISTOR.01 kill tests). THE GROUP EXTENSION, EXACTLY: Γ_ALE = ⟨Deck⟩ ≅ ℤ₄ ⊂ SU(2) — (z₁,z₂) ↦ (iz₁,i⁻¹z₂), triholomorphic, preserves Ω; THIS is the ℤ₄ that is quotiented (ℂ²/Γ_ALE = the A₃ singularity XY = Z⁴, and PT/ℤ₄ throughout means the quotient by Γ_ALE). ρ = Clock = diag(i,1) ∈ U(2) — Kähler, NOT triholomorphic (det ρ = i rotates Ω by the μ₄ generator, v492 S5); it is NOT quotiented — it NORMALISES Γ_ALE and survives as the residual clock symmetry. The global object: since ρ² = Deck exactly (v492/v506), ⟨Γ_ALE, ρ⟩ = ⟨ρ⟩ is cyclic — projectively ℤ₄ with ρ² generating the deck ℤ₂, and on the spin/fermionic level the canonical ℤ₈ tower (V² ∝ U, V⁴ ∝ (−1)^F, nonsplit; 8 = 2|μ₄|; v506/v507). Action table: K_PT — deck trivial, clock weight via det ρ = i [E] (v514); Ω — deck-preserved, clock-rotated by i [E] (v492; the back-reacted Ω_N closed-form with (2πi)²-integral periods and forced charge 4, v515); BCOV fields (O(−2) tower) — orbifold sectors / character series [E] ledger, [O] quantisation (v514); open-string SDYM(E₈) fields — glue-equivariant sector / sector rotation [E] (v492), [O] interacting; boundary states ((E₈)₁ shadow) — μ₄ sector split / clock phase [E] at character/GNS level (v497–v500), [O] as an actual net. THE A₃ ROLE TABLE (no silent identifications): A₃^family = the family factor in the lattice D₅⊕A₃ (su(4)-flavour, three families from its exponents) — related to A₃^ALE by the McKay correspondence OF TYPES only; NOT identical as realisations (one a sublattice of E₈, the other the singularity type of ℂ²/ℤ₄; the connecting bridge is the Kronheimer–Nakajima quiver, v479). A₃^ALE = the ADE type of ℂ²/ℤ₄; its resolution carries the three exceptional spheres. The three exceptional spheres = the Coxeter/Picard–Lefschetz structure (clock = Coxeter element of W(A₃) on H₂, eigenvalues {i,−1,−i}, v493; they carry the three twisted axion slots v505 and the lockstep fluxes v509). D₅^carrier = the carrier factor (g_car = 5), glued to A₃^family by the μ₄ Lagrangian glue into E₈ (v92/v125); no role on the ALE side beyond g₀ = D₅⊕A₃ (v492). Woit's SU(3)_color — external programme reference ONLY (colour as the rank-three quotient bundle on PT): NOT identical — no identification claimed; in particular A₃^family ≇ SU(3)_color. Woit's SU(2)_weak — external programme reference ONLY (the internal spin factor): NOT identical — no identification claimed; whether such an internal SU(2) can be realised on PT/Γ is exactly kill test (6) of WOIT.OS.TWISTOR.01. Hypothesis (as corrected by WP1): the seam is the glue-equivariant ℤ₄-orbifold sector of the celestial chiral algebra on the A₃ ALE space ℂ²/ℤ₄; the μ₄ clock is the Kähler U(2) phase diag(i,1) whose square is the deck group (spin bridge ℤ₈, 8 = 2|μ₄| — the c₃ = 1/(8π) winding integer); the twistorial bulk is the SELF-DUAL sector of TFPT gravity only. The spin bridge is no longer a bookkeeping convention: the NS deck implementation is forced to order 4 (U² = (−1)^F exactly, nonsplit ℤ₄; v506), and the nonsplit class is arrangement-sensitive — the edge (silver) arrangement splits (U² = +1, zero roots), so the seam fermions MEASURE the v506 alignment bit as a Fidkowski–Kitaev-type extension class (v507, SEAM.BIT.ORIGIN.01) — and that class is nonsplit iff the deck acts freely (all 17 seam-circle involutions, v510, SEAM.BIT.FREEDOM.01), which the covering deck does by topology: the edge class is excluded and the bit reduces to the square-modulus datum τ = i alone — restated by the flag-transitivity web (v512, SEAM.TAU.FLAG.01) as one discrete symmetry-lift bit (flag transitivity of the four marks, V₄ → D₄, ⟺ τ = i; since v528 a 15-fold exact equivalence web with the counterwitness passing all 10 established side-blind tests — free RP/Θ is the eighth (v521), the mark-decorated twist-state class the ninth (v525: the free-plus-twist class is exhausted), the interacting FK toy the tenth (v529, with Kill-Test 2 firing at toy level after the straddle law) — and the bit physically defined as the twist-class choice with a gauge-robust order parameter (v528, stays formal input)), narrowing the search space for a future [E] closure to the genuinely interacting algebra under the straddle-law constraint. WP1 is executed and verified (v492, sympy exact, verdict B): the E₈ μ₄-glue grading (v128) is INNER — h = (2,2,2,2,2;0⁴) reads the glue class mod 4 on all 240 roots, so the glue is a flat ℤ₄ monodromy in the Kronheimer–Nakajima sense, with the A₃-side detector reading the same diagonal (1,1) glue of ℤ₄×ℤ₄ (v92/v125); ℂ²/ℤ₄ is verified as the A₃ singularity XY = Z⁴; the glue-equivariant SDYM(E₈) sector closes with graded dimensions 60(d+1)/64(d+1) — possible only because dim g_j = (60,64,60,64) — zero modes = the carrier D₅⊕A₃+Cartan = 60, density 1/4 = 1/|ℤ₄|; the four glue-sector characters sum exactly to the (E₈)₁ character 1+248q+4124q²+34752q³ (v377), with sector weights = the v92/v125 discriminant form (5x²+3y²)/8 and integer glue-diagonal h = (0,1,1,1) (= locality of the (E₈)₁ extension). The critical correction (why verdict B): the A₃ deck acts on the celestial sphere as z → −z (order 2, the sheet flip), NOT as the order-4 clock z → iz; the clock is the U(2) phase diag(i,1) (normalising the deck, det = i rotating the holomorphic symplectic form by the μ₄ generator), with the exact spin bridge (spin clock)² = deck. Clock-invariance selects the 1-parameter A₃ deformation XY = Z⁴ + a₀ whose four branch points are one μ₄ orbit with cross-ratio 2 (the v168/v214 pillowcase marks). Negative controls kill the false spatial action diag(i,i) three ways and the false glue (3112/6720 additivity violations); rigidity = Aut(ℤ₄). Typing/non-circularity: the continuum existence of the (E₈)₁ net on the seam — the SEAM.EQUIV.01 target — is NOT an admissible input. WP2 is now also executed and verified (v493, sympy exact, 47 checks, verdict B): the clock-invariant deformation XY = Z⁴ + a₀ is selected SHARPLY (P(iZ) = P(Z) forces a₃ = a₂ = a₁ = 0, two-sided), is smooth iff a₀ ≠ 0 (disc = 256a₀³), and its binary-quartic invariants are I = 12a₀, J = 0 identically — so j = 1728 and the τ = i pillowcase shape (v168/v214) is FROZEN for every a₀: a₀ is a pure seam SCALE, no shape modulus survives clock-invariance (negative controls: a₁Z gives j = 0, an a₂-instance gives j = 1556068/81 — the test has teeth). The three resolution spheres carry exactly the three nontrivial μ₄ characters {i,−1,−i} under the clock, which acts on H₂ as a Coxeter element of W(A₃) (char x³+x²+x+1, h(A₃) = 4 = |μ₄| = N_fam+1), fixes no cycle, and IS the Picard–Lefschetz monodromy of the family; the surviving direction is the weight-1 χ₁-Fourier diagonal (1,i,i²), all three sphere volumes in lockstep (√2·t). The Bittleston–Homans–Sharma deformed-algebra pattern transfers ℤ₂ → ℤ₄: the fibre bracket −4·Nambu(XY−Z⁴−a₀), anchored at the a₀ = 0 orbifold, closes with corrections exactly linear in a₀ at the ℤ₄ wrap, conserving the μ₄ grade (no sector leak — the WP1 equivariant sector deforms consistently), with a₀ in BHS's weight-0 c² slot; verdict B via three named identifications (−4·Nambu as THE k = 4 CCA bracket; period = root difference; seam-scale reading via clock² = deck). The v216 residual is typed, not moved: given the order-4 clock the square is automatic — a relocation of the same order-4 carrier input, not a new derivation. WP3 is executed and verified (v495, exact Fraction/sympy, 25 checks, verdict B): the Okubo coefficient 5/(2(dim g+2)) is DERIVED as a polynomial identity for all 8 algebras on Costello's list (sl₄ negative control: 5/32 vs 3/32), the closed form λ̃² = 10h∨²/(dim+2) = h∨+6 holds across the Deligne series, and for E₈ the Green–Schwarz coefficient is exactly λ̃ = 6 (unit-trace) resp. λ_fund = 1/10 (adjoint-trace), so (κ/c₃)² = 12 = |μ₄|·N_fam resp. 1/300 — exact anchor rationals, with κ/c₃ itself irrational (2√3; a byproduct: the printed λ²(so₈) = 3/2 in Costello's appendix A is a factor-2 slip, the exact value is 3). The look-elsewhere caveat is part of the result: the same squared-rational alignment holds for ALL eight algebras (8/8 — zero selective power), λ̃-integrality passes 2/8 (shared with sl₃), and the only E₈-selective single test is g_car = 5 | h∨ (1/8); the isolating conjunction is post hoc. Alignment survives; selectivity does not — the c₃-connection is convention-level compatibility plus genuine λ-arithmetic, NOT E₈-selective evidence, and never a derivation of c₃. WP4 is executed and verified too (v496, exact integer/Fraction/sympy, 25 checks, verdict B(ii)): the (E₈)₁ character E₄/η⁸ = (1, 248, 4124, 34752, 213126, …) is NOT a conformal block of the celestial E₈[ℂ²] S-algebra in its own jet grading — the obstruction is localised three ways: (a) the CP grading gives spin 1 − d/2 unbounded below and 248 is never a jet-tower dimension (d ≤ 100); (b) the cumulative generator count is quadratic (31s²+92s+60, 31 = k+h∨), so the jet Fock grows as n^(2/3) against the character's n^(1/2) (f_n/χ_n strictly increasing, n = 1..12); (c) the level-2 null ideal of (E₈)₁ deletes exactly 27000 = 30³ = h∨³ out of Sym²(248) = 1+3875+27000 (the character keeps 4124 = 1+248+3875) — with no jet analogue. But the boundary/period reading holds exactly at the current stratum: the zero-mode slice is the 60 vacuum-sector currents, the jet slice cycles (60,64,60,64), one full μ₄ period of loop energies sums exactly to 248, and the glue-diagonal weights (0,1,1,1) are integers — while the free loop Fock counts 897266 ≫ 248 at level 1, so the rational truncation must be imposed in a limit. That is precisely the MMST scaling-limit shape of SEAM.EQUIV.01 (v336/v449): the character is a boundary/limit SHADOW of the S-algebra, and the constructive limit question passes to WP5. Kill tests evaluated: K1 survived (WP1+WP2), K3 did not fire but is scope-demoted (the alignment format passes 8/8 — compatibility, not evidence), K4 fires only against the exact-block reading (the sector arithmetic holds exactly, so no degradation to 'E₈ admissible'). WP5 is subdivided WP5a–e, and its first milestone WP5a is executed and verified (v497, exact integer/Fraction, 34 checks): the WP4 boundary-limit shadow is made a PRECISE coefficientwise limit — the one-parameter family χ_w of graded Fock characters on the chiral jet generators (E_w = m + w·r in quarter units u = q^(1/4)) contains the chiral jet grading as its w = 2 member (generator counts 64, 120, 128, 180, 192, 240, 256, 300) and its u^n coefficient equals the quarter-moded loop Fock for ALL w ≥ n+1, strictly larger for w ≤ n (n ≤ 8, w ≤ 10) — an explicit stabilisation threshold w = n+1, not a slice; and the null ideal is DERIVED from root data, not cited: Freudenthal + Weyl + character peeling give Sym²(248) = 27000 + 3875 + 1 with residual exactly zero, 27000 = 30³ = h∨³, and the level-2 quotient 31124 − 27000 = 4124 = 1+248+3875 equals the independent μ₄ theta-split sector sum (1036, 1024, 1040, 1024) at q² — two routes, one number. Negative controls: SO(16)₁ through the same pipeline gives FOUR components (5304+1820+135+1), 5304 ≠ 14³ (h∨³ is not generic), quotient 2076 = Θ_D8/η⁸ (the recipe validated on a second algebra), and block weights (0, 1/2, 1, 1) that cannot fuse into one local character; only P = 4 = |μ₄| periodisation reproduces the 248 layer. Honest limit: the limit does NOT generate the truncation (loop Fock 897266 ≫ 248 at level 1) — WP5a fixes the ideal's size and location quantitatively and gives the celestial route the same two-step shape as MMST (limit + maximal ideal). The second WP5 milestone WP5b is executed and verified too (v498, exact integer/Fraction, 53 checks, deterministic — success on the preregistered criterion): the deleting object exists and is explicit — |s⟩ = (E^θ_{−1})²|0⟩ (weight 2θ, level 2 = 8 quarter units = q², an integer level) is constructed in a machine-built Chevalley/Frenkel–Kac basis (cocycle asymmetry on all 57600 pairs, the [e_α,e_{−α}] sign FORCED by Jacobi with SGN = −1, κ derived with κ(θ∨,θ∨) = 2), and J^a_1|s⟩ = 0 is machine-verified for ALL 248 generators with the case classification 190 (first bracket) / 57 (second) / 1 (a = F^θ via the central-term cancellation — the only case that sees the level k); plus J^a_2|s⟩ = 0, E^a_0|s⟩ = 0, exact weight and Shapovalov norm 0; the affine PBW engine is unit-tested on all 61504 basis pairs. Level dial: the F^θ_1 coefficient is 2(1−k) — 2/0/−2 at k = 0/1/2: without the central extension the deletion operator does not exist. μ₄ compatibility: glue class j(θ) = 1 (machine-built h-adapted chamber, ⟨θ,h⟩ = 5, height 29 = h∨−1), clock phase i^(2j) = −1, class(2θ) = 2 sheet-even with the deleting θ-sl₂ crossing the sheet-odd classes (1,3); 8 quarters = q² via the per-period dictionary. The module it generates is THE ideal: weight 2θ has multiplicity 1 in the level-2 Fock, and the direct g₀-orbit BFS reproduces the Freudenthal multiplicities of V(2θ) exactly through depth 4 (27000 = h∨³, quotient 4124; Weyl complete reducibility beyond depth 4 typed [C]). Negative controls separate honestly: the level-1 current state and generic level-2 states are NOT singular; at k = 2 the CUBE is (generic Kac (E^θ)^(k+1) mechanics); SO(16)₁ has the same singular vector but keeps three extra level-1 primaries (h = 1/2 breaks one-block fusion) — the singular-vector mechanism is level-1 generic, the ONE-BLOCK closure is the E₈/μ₄-specific part. Honest handover to WP5c: in the twisted quarter-slot moding two sector-C₁ modes never sum to 8 quarters (minimum 6 = q^(3/2)) — the per-period dictionary (v496), not the per-slot identification, carries |s⟩ to q²; exactly the GNS/limit-state question (kernel ⊇ ideal) that WP5c answers. WP5c is executed and verified (v500, exact integer/Fraction, 35 checks, success on the preregistered criterion): the quasi-free family ω_w exists — loop sector = the affine k = 1 vacuum n-point functions via the machine-determined compact anti-involution θ(e_α) = −e_{−α} (the unique anti-automorphism sign on all 61504 basis pairs), radial sector = oscillator pairings x^(wr) (the exact Gibbs regulator) — is positive for every finite w, and stabilises EXACTLY at the WP5a threshold (ω_w = ω_∞ mod x^(N+1) for w ≥ N+1, sharp at w = N). Its limit carries the null ideal in its GNS kernel: the complete 9361-block exact level-2 Gram has rank 4124 exactly (the preregistered target), kernel 27000 = V(2θ) weight by weight (Freudenthal cross-check on all 9361 weights), every block PSD, rank table per Weyl orbit (0,0,1,8,44), level-1 rank 248 positive definite (the current layer survives); the clock descends to GNS with level-2 rank split (1036,1024,1040,1024) = Θ_Cj/η⁸ at q² — the two-routes identity at the STATE level — and |s⟩ IS the zero vector of GNS(ω_∞), resolving the WP5b twisted-slot tension. A CCR obstruction shows NO w-uniform state can damp the radial modes (the family formulation is NECESSARY, and the family exists — KILL not triggered); controls: k = 2 keeps everything (⟨s|s⟩ = +4), k = 0 has no current layer, D₈ gives one block of four, the wrong family erases the 248 layer (710955 ≠ 248), no damping keeps 897266 ≠ 248. WP5d-α is executed and verified too (v501, Gaussian lattice machinery ED-validated to 1e-15 + exact Fractions, 39 checks): the KLM two-interval index measured entropically on the 16-layer seam carrier — the fermionic two-interval MI is extensive (μ = 1 reference; c fit 0.5000, residual → 0 with N) while the sector-summed orbifold prescription pays exactly one classical bit (the ln 2 plateau at machine precision, |Δ₂ − ln 2| = 1.1e-15 at N = 512), so [F:F_even] = 2 and μ_gauged = 4 = the v490 parity census (two independent lattice witnesses); the orbifold breaks two-interval complementarity S(E) ≠ S(E′) (the direct duality-failure witness) with the complementary-pair budget ≤ ln 4 = ln μ(SO(16)₁) as a double-limit statement; the condensation arithmetic is anchored at both measured ends — det Cartan(D₅)·det Cartan(A₃) = 16, KLM/Longo–Rehren 16/4² = 4/2² = 1, Σd² = (4,4,1), θ_v = 1 exactly at ν = 2c₋ = 16 (rivals ≠ 1) — so μ = 1 after condensation and the preregistered KILL ('μ-offset ≠ 0 after condensation') does NOT fire; controls: the ν = 1 offset is non-removable (θ_v ≠ 1 — the discriminator has teeth), the trivial phase shows nothing, the wrong sector sum loses the full ln 2. WP5d-β is executed and verified as well (v504, Gaussian lattice machinery ED-validated + exact GF2/integer algebra, 37 checks): the two remaining KLM legs of complete rationality witnessed for the same orbifold prescription — strong additivity is algebraically EXACT with the shared boundary Majorana (Even(A) ∨ Even(B) = Even(A∪B): GF2 spans full 64/64, 256/256, 512/512, 1024/1024, matrix rank 32/32; disjoint exactly HALF, index 2 — the missing sector odd⊗odd is the v501 ln 2 bit, localised at the split point; the neutral U(1) algebras do NOT generate the union even with the shared site, gaps 2/10/52 growing); the entropic touching defect is BOUNDED < ln 2 with the Ising ¼-exponent approach ((ln 2 − Δ₂) ~ N^(−p), p = 0.2444 vs 2Δ_μ = 1/4; honest note: 'defect → 0' would be FALSE at the sharp lattice split — bounded ⟺ finite index, Longo–Xu) while the preregistered U(1)/Dirac control bursts ln 2 from L = 128 and grows as (1/2)ln Var Q_A (Klich–Levitov slope 0.10134 vs 1/π² = 0.10132: infinite index — the current-net failure reproduced); the split property is witnessed at the elliptic-nome rate πK(1−x)/K(x) to 1.3–2.0% (σ₁ ~ x^0.5044, trace norm summable) with EXACT orbifold inheritance (P_A flips C → −C, σ_k identical to 8.3e-17; the even-bilinear coupling Gram is the second compound Λ²C — Longo heredity); and Pimsner–Popa E(a) − a/2 = PaP/2 holds identically (λ = 1/2 = 1/[F:F_even] with exact integer attainment: 16384 + 2048 monomial sweeps, 0 violations; λ_E4 = 1/4 = 1/μ; index consistency exp(Δ∞) = 2 = 1/λ_PP over two independent routes; U(1): λ = 1/(m+1) → 0): with v501 ALL THREE KLM ingredients of complete rationality — split, strong additivity, finite μ — are witnessed on the lattice; the continuum uplift is honestly fenced ('finite-group orbifolds of completely rational nets are completely rational' is Xu's theorem — cited, not claimed; the concrete seam quotient net and the interacting condensed (E₈)₁ net stay WP5e/Costello–Li). WP5e is now subdivided, with its α stage executed (v502, exact sympy/Fraction, 33 checks, CELEST.WP5E.ALPHA.01 — the CFT-side prefactor + level pinning): the q^(−1/3) prefactor of E₄/η⁸ IS exact μ₄ vacuum-energy bookkeeping — the clock is INNER ((h,h) = 20, (h′,h′) = 12, sum 32), so the twist on the 8 torus bosons is θ = 0⁸ in all four sectors (a SHIFT orbifold, not a rotation orbifold) and every sector carries the same −c/24 = −1/3 at c = 8; the sector weights (0,1,1,1) ARE Casimir energies (spectral flow j²(h,h)/32 mod 1, and exactly via the 16-Majorana seam carrier, R–NS shift n/16 = 5/8, 3/8, 1); and k = 1 is forced THREE independent ways (current condition h(J) = k = 1; conformal embedding 47(k−1)(k+266/47) = 0 resp. 128k(1−k) = 0; central charge 248k/(k+30) = 8 ⟺ 240(k−1) = 0 — the prefactor itself) plus the WP5b singular-vector dial (31124 − 27000 = 4124 at k = 1 only); honest sharpening: glue-h integrality h(J^j;k) = k(0,1,1,1) holds for ALL k = 1..8 and fixes nothing — the naive integrality route is retired; controls: D₈ has the SAME prefactor but h = (0,1/2,1,1), ℤ₂/μ₄ rotation twists break the common prefactor, wrong k ∈ {2,3,4} fails all five dials. The β stage is executed as well (v505, exact sympy/Fraction, 47 checks, CELEST.WP5E.BETA.01 — the equivariant anomaly ledger on twistor space): the Atiyah–Bott/Lefschetz fixed-point skeleton of the one-loop box anomaly on ℂ²/ℤ₄ is exact — denominators (2,4,2) with Dedekind sum 5/4 = (|ℤ₄|²−1)/12, equivariant characters (248,0,−8,0) by two routes, invariant average 60 = the carrier, Frobenius 61568; only the INVARIANT sector is Okubo-quadratic (36⟨x,x⟩², 36 = λ̃²_e8 — v495 re-derived), the twisted sectors carry irreducible T₅/T₃ content, and the AB-weighted sum cancels the D₅ quartic exactly while leaving the RIGID residual 32·T₃ (no admissible reweighting fixes it; the graded GS exchange is rank-obstructed in sectors 1–3); the index bridge f(m) = (1/4)Σ_j(i^(jm)−1)/det_j = ch₂(T_m) = −(C⁻¹)_mm/2 holds EXACTLY (fixed-point ledger = McKay/Kronheimer intersection ledger) with the integral glue defect −78 by both routes; the level dials say k = 1 geometrically (lattice current count 240 at k = 1 and exactly 0 at k = 2,3,4; embedding residual (0,360,814,1362); one scale ⇒ one level; integrality alone fixes nothing — honest, as on the CFT side); and an honest REFUTATION: the clock-invariant modulus a₀ ∈ O(8) fills the BSS GRAVITON slot O(2), not the axion slot O(−2) (weight mismatch 4 = |μ₄|) — 'the theory brings its own GS axion as a₀' is false; instead the three H²(ALE) classes carry exactly the three twisted-sector Coxeter characters {i,−1,−i} (bijection), and the bulk axion must come from the O(−2) tower field itself; controls: diag(i,i) breaks the ledger four ways, SO(16) glue gives defect −30 ≠ −78 with a failing bulk Okubo, k = 2 dies on the closure dial; the preregistered kill ('inflow demands a level ≠ 1') does NOT fire on the equivariant skeleton. The γ stage is executed as well (v508, exact sympy/Fraction, 27 checks, CELEST.WP5E.GAMMA.01 — the sphere-axion pairing check, an honest rigid NEGATIVE result): the W(D₅)×W(A₃)-invariant vertex space on the glue Cartan is exactly dim 2 (quadratics = span{s₅, s₃}) and dim 5 (quartics = span{P₁,P₂,P₃,T₅,T₃}) by Weyl nullspace arithmetic, and the PRODUCT THEOREM kills every exchange image in the T₃ direction (any two invariant quadratics multiply into span{P₁,P₂,P₃}, while Φ_T3(A_fix) = 32 ≠ 0); the strict two-index rule collapses the sphere couplings entirely, the twist-insertion channels E₁₃ = (16,−96,144,0,0) and E₂₂ = (16,32,16,0,0) give rank([M | A_fix]) = 3 with the annihilator certificate (Φ_T5, Φ_T3, Φ_P)(A_fix) = (0, 32, 72) (side discovery: K⁽⁰⁾ = −15·K⁽²⁾, the even-sector quadratics are parallel); naturalness dissolves (ch₂-natural and AB-weight couplings both certify (0,0) vs required (32,72) — scale-independent); SO(16) has no sphere partners AND uncancelled T₅, D₈ no T₃ structure; the slot bijection is untouched and the level-kill still does not fire. The remaining roadmap is WP5e proper alone (the GLOBAL BCOV/Kodaira–Spencer quantisation on PT/ℤ₄: the partition function E₄/η⁸ including the q^(−1/3) prefactor derived FROM THE TWISTOR SIDE — neither the v502 CFT-side dials, nor the v505 equivariant skeleton, nor the v508 exchange no-go, nor the v509 flux/sector dials trigger the kill branch; the exchange sub-branch is closed by v508, and the ε₂ stage is now executed as well (v509, exact sympy/Fraction, 28 checks, CELEST.WP5E.EPS2.01 — the CPS level-from-flux dial, verdict B): the CPS skeleton exact (S³ period (2πi)²N, exceptional flux 2πN, level magnitude 2N), the pairing matrix pinned by complete enumeration (48 unimodular → 2 effective) with fluxes (64,60,64) and one quantum per current, the naive 'level = total flux' killed by the lockstep test itself, the per-current reading (1,1,1) anchored by the current count (240,0,0,0) and embedding index 1, the ord-4-vs-level-1 tension resolved (16 = ord² fractional sectors condense to 1) with the new sector-counter dial #primaries((E₈)_k) = 1 ⟺ k = 1, and the LOCKSTEP THEOREM lifting 'one scale ⇒ one level' to a theorem of clock invariance (det(A−1) = −4; falsifier Z⁴ − Z: 0/24 orderings lockstep); the CPS dictionary on PT/ℤ₄ stays [C], the type-I B-model back-reaction [O]; and the δ₂ stage is executed too (v511, exact Kostant/Weyl + sympy/Fraction, 41 checks, CELEST.WP5E.DELTA2.01 — the full-tensor ledger, intermediate verdict): the v508 collapse is CONFIRMED full-tensorially and arity-crossing by the innerness theorem (g₀ = d₅ ⊕ a₃ semisimple with no u(1), h in the g₀ Cartan ⇒ every invariant tensor carries total charge 0 mod 4; bilinear Hom table nonzero only at j′ = −j with dims 2/1/1/1, all 15 non-neutral trilinear triples Hom = 0), BUT one cubic door opens: the su(4) d-symbol — the unique symmetric trilinear on all of e₈ (so(10) has no cubic Casimir) — carries the exchange quartic Q_dd = (1/60)(T₃ − P₃/4) with Φ_T3(Q_dd) = 1/60 ≠ 0, so the v508 master kill does not extend to cubic vertices; the pairing stays obstructed in the charge reading with the WEAKER certificate {Φ_T5, ψ = Φ_P − Φ_T3/4}, ψ(A_fix) = 64 (= dim g₁, [C] fence), and becomes exactly solvable relaxed (A_fix = −u + 8v + 2w + 1920·Q_dd, c_d = 1920 = |W(D₅)| = 8·240 [C] — the |W(D₅)| reading since typed look-elsewhere-loaded (11/924 vs 8/924 for the control target 1800) and convention-contingent by the v513 negative certificate, CELEST.DTERM.NONDERIV.01: the convention-stable [E] core is c_d = 32×60); SO(16)/D₈ has no symmetric cubic and false g₀/sector controls separate; and the δ₁ stage is now executed and DECIDED (v518, CELEST.WP5E.DELTA1.01 — kill under the derived measure): the strict holomorphic q⁰ reading is refuted at the ℤ₂/Eguchi–Hanson anchor (a method boundary, not a kill of the contract), the contact term is the MODULAR COMPLETION of the Atiyah–Bott data (a Harvey–Moore-type τ-integral) with the forced leading (T₅,T₃) ratio 4:3, and the τ-integral has been evaluated under a DERIVED measure — the 16-component Weil completion closes exactly (E1.5 residual 2.91 → ~10⁻³⁹), the μ₄ multiplier obstruction is a CHARACTER of the orbit stabilisers (koboundary defects (1,1,1) on all 15 pairs, λ(γ) = i^(2B+C/4) on Γ₁(4)), the cancellation is the twisted fibre block f₁f₃ = G (exact identity; the three sphere axions leave residual order 4), and all three preregistered testers FAIL under both derived solutions (χ₄, χ₁₀) with no (N₁,N₂) rescue in the positive cone — a genuine kill on the derived surface, in stated TENSION with the declared v516 completion reading (which delivers ψ = 64) — a tension since DECIDED at probe level by v520 (CELEST.WP5E.MEASURE.01, ERFOLG-A: single-valuedness derived from F-independence + the Quillen pairing under the typed premises TP-1..TP-4, the completion reading wins, the kill sharpened), and the w_m normalisation since DERIVED constructively by v523 (CELEST.WP5E.WM.01, ERFOLG: 1/det_j = the Atiyah–Bott/zeta-determinant fixed-point factor, computed from three independent sources — the equivariant mode ledger with Abel value (1/2, 1/4, 1/2), the zeta/reflection determinant 4·sin²(πj/4) with the unique real positive Quillen section, the δ₁f block constant term 1/det_b — with the v516 chain reproduced number by number under the typed premises TP-REG/TP-Q/TP-NUM/TP-CH; residual [O] = the global BCOV integral beyond the fibre zero-mode factor); and the ε₁ stage is now executed as well (v514, exact sympy/Fraction, 34 checks, CELEST.WP5E.EPS1.01 — the O(−2) bulk-axion slot, verdict B): the slot is a CONSTRUCTION (the equivariant Penrose ledger closes block by block for all d ≤ 6 and all four characters; character series P₀ = 1 + 3t² + 15t⁴ + …, P₁ = P₃ = 2t + 8t³ + …, P₂ = 6t² + 10t⁴ + …; the d = 0 slot has multiplicity (1,0,0,0) — the bulk axion survives the projection; Molien invariant ring = the v492 hypersurface XY = Z⁴ with relation degree 8 = the a₀ weight; twisted minimal content (2t, 6t², 2t) = the Coxeter eigenvalues; graviton control: O(+2) invariant only from fibre degree 4 with multiplicity 3 = {X, Z², Y}), λ̃ = 6 is pinned by three exact ledgers (Okubo (6⟨x,x⟩)² on the 240 glue roots; the measure chain μ-exact with the wrong bookings 3 and 12 excluded; flux single-channel iff k = 1, (κ/c₃)² = 12), and the GH/A₃ back-reaction step re-derives the v493 family and the Coxeter clock from centre geometry (two branches, period lockstep 4πt₀(i−1)(1, i, i²), source charge 4 = |μ₄|, EH asymptotic log exactly 0 — the CPS log is an exceptional-locus statement, multipole rule m ≡ 0 mod 4 with (4,±4) carrying −a₀); conditional on Costello's flat-PT matching [C]; the quantised BCOV coefficient and the twisted channels (32·T₃) stay [O] with the M1–M3 milestones preregistered (the A₃ Ω_N / the twisted KS measure / the a₀ uplift, each with success + kill); and the M1 milestone is now executed as well (v515, exact sympy, 30 checks, CELEST.WP5E.M1.01 — 'the A₃ Ω_N', SUCCESS on the preregistered criterion): the back-reacted Ω_N is closed-form on the A₃ twistor family (Ω_N = Ω₀ + Σ N_p K_p, CPS/Bochner–Martinelli kernels on the four centre twistor lines; the residue form derived with cover factor 4 = |μ₄| and clock phase i; the family closed as XY = Z⁴ + 4t₀²λ²Z² − t₀⁴(1−λ⁴)² with the CY-compatible clock lift Ω → +Ω), all S³/ℤ₄ periods are (2πi)²-integral with the lockstep flux vector N(1,1,1,1) (forced uniform: clock orbit + K₄ connectivity) and clock covariance Π → iΠ, the 12 conifold nodes sit exactly on the 8 eighth roots of unity, and the lens geometry FORCES the source charge 4 = |μ₄| (only N ≡ 0 mod 4 passes); honest fence: integrality alone does not discriminate — the (2πi)² quantisation holds on the forbidden Z⁴ − Z family too; the discriminator is the lockstep phase structure (0/24 vs 8/24) plus the clock forcing; and the M2 and M3 milestones are now executed as well: M2 (v516, exact sympy/Fraction, 23 checks, CELEST.WP5E.M2.01 — 'the twisted KS measure', SUCCESS on the preregistered v514 S8.2 criterion ON THE DECLARED COMPLETION MEASURE, verdict B): the completion contact term contact_j = (Q⁽⁰⁾ − Q⁽ʲ⁾)/det_j carries the exact completion-weight identity w_m = Σ_j(1 − i^{jm})/det_j = (0, 3/2, 2, 3/2) = 4h_m = |μ₄|h_m = −4·ch₂(T_m) — the three sphere axions pair through their OWN McKay ch₂ charges, no free scale, no fit; parameter-free locks (T₅ = 0 for any scale, ratio 4:3 reproduced, T₃ budget forces c = 4 = |μ₄|); every twisted channel becomes the perfect Okubo square 36⟨x,x⟩²/det_j, total 45⟨x,x⟩² = (5/4)×36 = Dedekind × Okubo (the unique quartic-free weighting of the v505 rigidity theorem); both v508 certificates killed (32 → 0, 72 → 0) and the v511 slice ψ = 64 SUPPLIED EXACTLY — no cubic d-channel needed (c_d free = 0); controls: wrong scale, shuffle, SO(16) (the KILL fires there — E₈ doubly special), diag(i,i), ℤ₂/EH anchor at scale 2 = |ℤ₂|; the completion reading is DECLARED [C] (supported by the δ₁ modular-completion finding, not derived from the BCOV integral — that derivation stays [O], δ1d); and M3 (v517, exact sympy, 23 checks, CELEST.WP5E.M3.01 — 'the a₀ uplift', SUCCESS on the preregistered v514 S8.3 criterion): the (4,±4) multipole uplifted to the GLT kernel χ = log P₄ (the log of the v515 family polynomial; null coordinate ⇒ harmonic for any kernel, residue identity 1/r_p matches the V-ledger, flux −4π per centre), and the log-type correction is coupled to the centre count on FOUR scales (asymptotic kernel log 4 = |μ₄| with first seam-fibre correction exactly a₀/η⁴ and exact m-grading; GLT tower p_{4k} = 4(−a₀)^k with the n ≡ 0 mod 4 selection rule; exceptional-locus log χ(0) = log a₀ = 4·log t₀ + i(4φ₀ + π); period response d log Π/d log a₀ = 1/4 = 1/|μ₄| integrating to the clock monodromy i, v493 reproduced) with a₀-rigid ℤ₈ node support and topological (2πi)² fluxes; controls: (4,0) clock-invariant, ℤ₂/EH reads 2 = |ℤ₂| on every dial, k = 3/5 orbits move the coefficient, the forbidden family fails both dials — the KILL (decoupling) does not fire; the GLT dictionary stays [C], the full nonlinear Kähler potential [O]; the v514 fence M1–M3 is FULLY WORKED OFF, the δ₁ chain is decided by v518, the measure question is decided at probe level by v520 (the declared reading wins), the w_m normalisation is derived constructively by v523, and the named remaining target narrows to the GLOBAL BCOV INTEGRAL beyond the fibre zero-mode factor (the ψ = 64 slice itself is delivered by v516; the cubic-GS-term question stays dissolved — v518/v520 do not revive the d-channel); the continuum uplift of the WP5d lattice witnesses is Xu's theorem, cited not claimed) — WP5a–WP5d (both WP5d stages) plus WP5e-α/β/γ/δ₁/δ₂/ε₂/ε₁ plus M1–M3 are landed. SEAM.EQUIV.01 stays [O]; nothing here moves it. A compact thirty-step synthesis of the executed work packages — the narrative arc from the μ₄ clock to the (E₈)₁ boundary shadow, closing with the WOIT α/β₁/β₂ milestones (v519/v522/v524), the constructive w_m derivation (v523) and the twist-state kill (v525) — is presented as a dedicated section in Paper 3 (E₈ Audit & Bootstrap); this contract remains the full technical reference (typing fence, kill tests, work-package statements).",
        formulas: [
          "240 = 52+64+60+64, \\quad \\dim\\mathfrak g_j = (60,64,60,64), \\quad \\text{glue} = \\operatorname{Ad}(e^{2\\pi i h/4})",
          "(\\text{spin clock})^2 = \\text{deck}, \\qquad |\\mathbb Z_8| = 8 = 2|\\mu_4|",
          "\\Theta_{E_8} = \\textstyle\\sum_j \\Theta_{C_j}, \\qquad \\sum_j \\Theta_{C_j}/\\eta^8 = \\chi_{(E_8)_1}",
        ],
      },
      {
        title: "WOIT.OS.TWISTOR.01 — the Osterwalder–Schrader twistor bridge (new central contract)",
        body: "THIS IS THE ACTUAL BRIDGE FROM COMPILER TO PHYSICS — everything in CELEST.SEAM.01 is preparation for it. A research contract [O] (ledger row WOIT.OS.TWISTOR.01: Open, research contract), not a claim. The external programme it engages — Woit's Euclidean Twistor Unification (arXiv:2104.05099) — is a NAMED reference frame for the shape of the target, never a confirmation in either direction. INPUT: X₊ = (PT/Γ)₊ (Γ = Γ_ALE ≅ ℤ₄, normalised by the clock); A_hol, the INTERACTING open+closed twistorial algebra (SDYM(E₈) + BCOV — the WP5e-proper object whose free/equivariant skeleton is pinned by v492–v518); ρ, the order-4 clock diag(i,1); Θ, the anti-linear real structure induced by the seam reflection — precision (i), from the α stage (v519): 'induced by the seam reflection' means the seam-circle REFLECTION, not the deck/covering involution — the deck (free by topology, v510) furnishes the (−1)^F Kramers class, the seam-circle reflection furnishes Θ_Fock² = +1; precision (ii): on the RP side the μ₄ marks sit at the BOND MIDPOINTS of the 16-Majorana seam circle (the cut through the sites fails RP exactly); μ_BCOV+SDYM, the interacting functional. TARGET THEOREM: Θ² = 1 and ΘρΘ = ρ⁻¹; the gauge-invariant algebra is reflection-positive; and the OS quotient produces (H, Ω, U(P↑₊), A_Mink) with: a positive Hilbert metric, positive energy, local causality, ONE chiral fermion generation WITHOUT mirror doubling, the TFPT charge lattice, an internal SU(3)×SU(2)×U(1) action, and the (E₈)₁ seam net as an ACTUAL boundary net (not only as a character). KILL TESTS (all seven preregistered): (1) Θ incompatible with the clock; (2) RP fails after gauge fixing; (3) the reconstruction produces a vector-like mirror generation; (4) the Penrose transform reaches only free/self-dual states; (5) the reconstructed net has the right character but the wrong OPE / fails net equivalence; (6) the internal SU(2) remains a spacetime factor; (7) the four μ₄ marks are not incidence-compatibly extendable over spacetime. THE α STAGE — EXECUTED (WOIT.THETA.FREE.01, v519): the real structure EXISTS, and free reflection positivity picks the SAME family — exactly two families of anti-linear structures normalise the clock (family D inverts it exactly with Θ² = +1, Kramers-free, and is the OS conjugation σ_std with real points ℝP³; family A centralises it projectively and is Woit's euclidean ρ_tw, replicated exactly on ℂ⁴), the mark-compatible Θ form a μ₄ torsor, the ℤ₈ spin plane has no phase leaks, Θ_Fock = U_r∘K has Θ_Fock² = 2⁷ (normalised +1) with V ↦ 4096·V⁻¹ while the deck-induced candidate has Θ_t² = (−1)^F (the v510 dichotomy), and free RP holds on the bond cut with no degree truncation ((8,0,0)/(29,0,0)/full N = 8 algebra; η = +i forced; the clock-centralising family fails RP structurally; the anti-chiral state flips the odd sector — the free shadow of kill test 3). KILL TEST 1 therefore does NOT fire at the free/equivariant level — and stays formally LIVE on the interacting algebra A_hol; kill tests (2)–(7) are untouched; no marker moves. THE β₁ STAGE IS EXECUTED TOO (v522, WOIT.BETA1.GSO.01, typed UNDECIDED per the frozen preregistration): the μ₄ clock average violates Hermiticity exactly (witness −i/(8·sin(5π/16)); 745 matching / 96 anti / 0 violations — 'OS-symmetric' is strictly weaker than Hermitian), all 16 seam mirror axes invert the clock (it IS Woit's euclidean rotation — time-like), the gaugeable part of the ℤ₈ tower is exactly the GSO/fermion-parity ℤ₂, and under that corrected typing gauge-fixed RP HOLDS ((29,0,0)/(8,0,0) PD; the site-cut defect (7,9,6) survives; family A stays indefinite (17,12,0)); kill test (2)'s free shadow does NOT fire, contract precision (iii) added, and the clock-equivariant statement moves to β₂. THE β₂ STAGE IS EXECUTED TOO (v524, WOIT.BETA2.OS.01, verdict SUCCESS per the frozen preregistration, [C]-typed per contract precision (iii)): the OS quotient of the free system is EXPLICIT — H_phys nondegenerate and PD at both levels (dim 37 = 29⊕8 at N = 16 deg ≤ 2, min eigenvalue 1.7801e−6 at 40 digits; dim 16 = 8⊕8 = 4² at N = 8 complete half algebra — compact euclidean time reconstructs a thermal/KMS representation, exact certificate sin²(3π/8) − sin(π/8)·sin(5π/8) = 1/2), the Klein–Landau local transfer semigroup is exactly Hermitian on all shrinking domains with the site/bond dichotomy as its positivity pattern (even steps PSD via the exact square identity T(2j) = A*A; the one-step transfer NOT positive — the chirality datum, kill-3 shadow sharpened), the μ₄ clock = T^(N/4) is a positive self-adjoint transfer step with spectral calculus (N = 8 spectrum exactly {1, √2−1} = {1, 1/δ_Silver}) and a reconstructed unitary rotation group U(s) = exp(isH) — per precision (iii) the [C]-operationalisation of 'the clock acting unitarily'; the v522 non-Hermiticity is resolved as exactly the domain/wrap artifact (census (745,96,0), every anti-match a wrap overlap); the pre-declared KMS deviation carries exactly the silver witnesses (C(1)/C(3) = 1+√2 = δ_S, det(G−τ₄) < 0 — no contraction on the compact circle); Θ_phys² = +1 on every sector (Kramers-free), θ_cut∘θ_perp = α_(N/2) exactly; controls: site cut indefinite (the contract kill branch fires there), family A no quotient, anti-chiral (8,8,0); kill tests (1)/(2) strengthened, (3) shadow sharpened, none fires — all seven stay live on A_hol. THE β/γ ROADMAP (named milestones with success and kill criteria): (β1) Θ on the gauge-invariant subalgebra + gauge-fixed RP on the equivariant SDYM(E₈) sector (kill: kill test 2 fires) — executed via v522, UNDECIDED, neither kill fires; (β2) the OS quotient of the free system made explicit (kill: the quotient degenerates) — executed via v524, SUCCESS, neither kill fires, β₃ next; (β3) the PT ↔ PT* duality typed against σ_std (kill: the duality forces a clock-centralising structure); (γ) the chirality theorem + the mark incidence (kill: kill tests 3/6/7 fire). SCOPE FENCE (explicit non-claims of the celestial/twistor branch until this closes): both helicities, generic amplitudes, local matter, full Einstein dynamics, EWSB, confinement. SEAM.EQUIV.01 and its route split (MMST/TWISTOR) are stated in their own rows and are not moved by anything here.",
        formulas: [
          "\\Theta^2 = 1, \\qquad \\Theta\\rho\\Theta = \\rho^{-1}",
          "\\mathcal A_{\\mathrm{hol}} \\xrightarrow{\\ \\mathrm{OS}\\ } (\\mathcal H, \\Omega, U(\\mathcal P^{\\uparrow}_+), \\mathcal A_{\\mathrm{Mink}})",
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
        body: "F_transfer = F_observable ∘ F_threshold ∘ F_RG — standard physics fed TFPT source data — with four interfaces, each a typed RUNNABLE solver with a kill test: F_pole (Koide source→pole, v371; the 53/54 factor is an exact [E] readout, the pole interpretation [C]), F_Boltzmann (η_B via the BDP washout, v372), F_relic (the finite-T axion relic — the spine angle θ_i = 3π/5 = π·N_fam/g_car is the sharper branch, the 170° hilltop over-produces, v373/v211), F_QCD (m_p/m_e via carrier-b₃ running, v374) — folded into a status-typed prediction-observatory CI (v375). A machine guard (v187) keeps all four [C]/[O], never promoted to a primitive [E] compiler prediction (exact sub-parts like 53/54 and b₃ = −7 may be [E]). The functor contract CONTRACT.F.01 (v213) pins four structural axioms: μ₄-deck equivariance (λ₂ = (2/3)⁶ is the deck transfer eigenvalue), Plücker preservation (53 = aᵀ(R+Q)1), positivity/stochasticity (spec T = {1,(2/3)⁶,(1/3)⁶}), and explicit external modules. Dynamically (v303) all four share ONE shape — a gapped, positivity-preserving relaxation to a unique attractor (Perron–Frobenius / Boltzmann H-theorem / RG fixed point), the same shape as the main-branch E₈-mark update; F_pole runs it at the seam rate (2/3)⁶ exactly, the others with honestly-fenced external rates. So F_transfer is the downstream readout of the one discrete→dynamic principle — the predictions stay [C], never compiler outputs.",
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
      { label: "One closing theorem", value: "no abelian sector", description: "P2 · G_net · Target A are ONE condition (holomorphy = homology-sphere = one 1-dim irrep, all force E₈), now closed modulo cited theorems: the target net is pinned at every computable level (lattice v367/v368 + S3 stack v376–v379, ground-state witnesses v489/v490), residual [O] = cited continuum existence (v336) + crossed-product certified extension leg (v469, LR/Böckenhauer/KLM; AGT/AMT second witness); stays [O]" },
      { label: "CS realisation", value: "holomorphic ⇔ det K=1", description: "The closing step in abelian Chern-Simons: #anyons=|det K|; the v92 tower D5⊕A3(16)→D8(4)→E8(1) is anyon condensation = the Kitaev E8 state. Residual: condense the |μ₄| Lagrangian glue (v235)" },
      { label: "Closing as physics", value: "seam is SRE", description: "Sharper still: det K=1 ⟺ no topological ground-state degeneracy ⟺ the seam bulk is short-range-entangled (the Kitaev E8 phase) — now verified on the explicit lattice model (det K 4→1, v367/v368) and the genus-1 GSD = 1 closure (v378)" },
      { label: "Seam Equivalence Theorem", value: "closed mod cited (MMST route)", description: "The core is the keystone SEAM.EQUIV.01 (the raw RP seam IS the holomorphic (E8)₁ net at τ=i; route split 2026-07-22: parent [O], twistor route SEAM.EQUIV.TWISTOR.01 [O]), whose MMST route SEAM.EQUIV.MMST.01 is [C] closed modulo cited theorems: pinned at every computable level by an explicit lattice model (v367/v368) and the S3 closure stack (v376–v379, ground-state witnesses v489/v490), Lean-pinned (FORM.SEAM.MMST.01) to the published MMST/Adamo theorems, residual [O] = cited continuum existence (v336) + crossed-product certified extension leg (v469, LR/Böckenhauer/KLM; AGT/AMT second witness); stays [O] — the theory's one irreducible structural postulate, the role the constancy of c plays in relativity" },
      { label: "Flat-Away", value: "one geometric input", description: "Both routes reduce to one shared fact — the raw seam is flat away from the four marks. Heat route: positive-definite a₂ proved (convexity) + closed form + Lean (v292/v295/v296); spectral Hessian PD (v293); Troyanov minimiser (v294); red-team Z₄≠mark-local (v290); Route A = citable stack Kitaev/Freed-Hopkins→Müger/KLM→Conway-Sloane (v297)" },
      { label: "Closing arc (v300–v302)", value: "no TFPT-internal assumption left", description: "Flat-Away hardened to a discrete degeneracy obstruction + its pin derived from the (E8)₁ integer-weight character via 2d Steklov rigidity (v300); Route A's invertibility discharged by the free-fermion classification (gapped 16-Majorana c=8 bulk is invertible, #anyons=|det K_E8|=1; v301); the last input is the derived Recovery gap Δ=6·ln(3/2)≈2.43>0 = a bulk mass gap via OS/quasi-free clustering (v302). SEAM.EQUIV.01's MMST route SEAM.EQUIV.MMST.01 is now [C] closed modulo cited theorems (lattice v367/v368 + S3 stack v376–v379, ground-state witnesses v489/v490, Lean FORM.SEAM.MMST.01), residual [O] = cited continuum existence (v336) + crossed-product certified extension leg (v469, LR/Böckenhauer/KLM; AGT/AMT second witness); stays [O]" },
      { label: "CELEST.SEAM.01 (new)", value: "WP1–WP5d complete + WP5e-α/β/γ/δ₁/δ₂/ε₂/ε₁ + M1–M3 + the measure decision + the w_m derivation", description: "Fourth research contract — the celestial-holographic route: WP1 executed (v492, sympy exact, verdict B): the E₈ μ₄-glue is the flat ℤ₄ monodromy of the equivariant celestial chiral algebra on the A₃ ALE space ℂ²/ℤ₄ (zero modes = carrier, 4-sector (E₈)₁ character, discriminant-form weights), with the exact correction clock² = deck (spin bridge ℤ₈, 8 = 2|μ₄|); WP2 executed (v493, sympy exact, verdict B): the clock-invariant deformation XY = Z⁴ + a₀ is a pure seam scale with the τ = i pillowcase frozen (j = 1728 for all a₀), the clock IS the Picard–Lefschetz/Coxeter monodromy of the family, and the BHS deformed algebra transfers ℤ₂ → ℤ₄ with no sector leak; WP3 executed (v495, exact, verdict B): the Green–Schwarz coefficient is exactly λ̃ = 6 with (κ/c₃)² = 12 = |μ₄|·N_fam — but the look-elsewhere battery shows the alignment format passes 8/8 across Costello's whole list: alignment survives, selectivity does not (compatibility, not E₈-selective evidence; K3 not fired, scope demoted); WP4 executed (v496, exact, verdict B(ii)): the (E₈)₁ character is NOT a conformal block of the S-algebra in its jet grading (spin unbounded, growth n^(2/3) vs n^(1/2), null ideal 27000 = h∨³ localised) but survives exactly as a boundary/limit shadow at the current stratum — the SEAM.EQUIV.01 scaling-limit shape (K4 fires only against the exact reading); WP5a executed (v497, exact, 34 checks): the boundary limit made a precise coefficientwise limit (χ_w family, stabilisation threshold w = n+1, w = 2 = the chiral jet grading) and the null ideal DERIVED from root data (Sym²(248) = 27000+3875+1, 27000 = h∨³; quotient 31124−27000 = 4124 = the independent μ₄ sector sum; SO(16)₁ contrast: four blocks, 5304 ≠ 14³, h = 1/2 breaks fusion); WP5b executed (v498, exact, 53 checks, success on the preregistered criterion): the deleting object is explicit — |s⟩ = (E^θ_{−1})²|0⟩ in a machine-built Chevalley/Frenkel–Kac basis, J^a_1|s⟩ = 0 on all 248 generators (case tally 190/57/1, exactly one case sees k), level dial 2(1−k) (only k = 1 deletes — no deletion object in the centerless loop algebra), μ₄-compatible (j(θ) = 1, clock phase −1, class 2 sheet-even, 8 quarters = q²), U(g)|s⟩ = THE 27000 (orbit BFS = Freudenthal through depth 4, quotient 4124), with the one-block closure typed E₈/μ₄-specific against the SO(16)₁ contrast and the twisted-slot tension flagged as the precise WP5c question; WP5c executed (v500, exact, 35 checks, success on the preregistered criterion): the GNS limit state — the quasi-free family ω_w (machine-determined compact adjoint, x^(wr)-contracted radial oscillators) stabilises exactly at the WP5a threshold and its limit has the null ideal in its GNS kernel (full 9361-block exact Gram, level-2 rank 4124 = χ₂, kernel 27000 = V(2θ) weight by weight, clock split (1036,1024,1040,1024), |s⟩ = the GNS zero vector, CCR obstruction: the family is necessary); WP5d-α executed (v501, ED-validated lattice + exact arithmetic, 39 checks): the KLM two-interval index — fermionic MI extensive (μ = 1), the orbifold pays exactly ln 2 (machine-precision plateau), μ_gauged = 4 = the v490 census, condensation chain 16 → 4 → 1 anchored at both measured ends (θ_v = 1 at ν = 16), KILL not triggered; WP5d-β executed (v504, ED-validated lattice + exact GF2/integer algebra, 37 checks): split + strong additivity — strong additivity algebraically EXACT with the shared boundary Majorana (GF2 spans full, rank 32/32; disjoint exactly index 2 = the v501 ln 2 bit), bounded-vs-divergent entropic discriminator (Z₂ deficit < ln 2 with the Ising ¼-exponent approach vs diverging U(1) control, Klich–Levitov pinned), elliptic-nome split ladder with exact orbifold inheritance (C → −C + Λ²C compound, Longo heredity), Pimsner–Popa λ = 1/2 = 1/[F:F_even] and λ_E4 = 1/4 = 1/μ with integer attainment — all three KLM ingredients witnessed on the lattice, continuum uplift [O] (Xu's theorem cited); WP5e-α executed (v502, exact, 33 checks): the q^(−1/3) prefactor derived as exact μ₄ vacuum-energy bookkeeping (inner clock ⇒ shift orbifold θ = 0⁸, common −c/24 = −1/3; discriminant form = Casimir via spectral flow AND 16-Majorana free fermions; rotation reading fails 3/16 ≠ 3/8) and k = 1 forced three ways (current condition h(J) = k = 1; conformal embedding 47(k−1)(k+266/47) = 0; c = 8 ⟺ 240(k−1) = 0; plus the WP5b singular-vector dial 4124), with the honest sharpening that glue-h integrality holds for ALL k and fixes nothing; WP5e-β executed (v505, exact, 47 checks): the equivariant anomaly ledger on twistor space — AB characters (248,0,−8,0) two routes, per-sector Okubo with the rigid 32·T₃ residual, index bridge f(m) = ch₂(T_m) with glue defect −78 both routes, geometric k = 1 dials (current count 240/0/0/0), a₀ REFUTED as GS axion (graviton slot O(2), mismatch 4 = |μ₄|) with the three sphere classes filling the three twisted axion slots, kill not fired; WP5e-γ executed (v508, exact, 27 checks): the sphere-axion pairing check — an honest rigid NEGATIVE result with certificate: invariant vertex spaces exactly dim 2/5 (Weyl nullspace), product theorem (any two invariant quadratics have zero T₅/T₃ content), rank([M | A_fix]) = 3 with certificate (Φ_T5, Φ_T3, Φ_P) = (0, 32, 72), K⁽⁰⁾ = −15·K⁽²⁾ side discovery, naturalness dissolved scale-independently, SO(16)/D₈ controls — the exchange sub-branch is closed, the slot bijection untouched, the level-kill still not fired; WP5e-δ₂ executed (v511, exact, 41 checks): the full-tensor ledger — the collapse confirmed full-tensorially by the innerness theorem (all 15 non-neutral trilinear triples Hom = 0), the unique symmetric survivor = the su(4) d-symbol opening T₃ with the weaker certificate ψ(A_fix) = 64 and the relaxed solution A_fix = −u + 8v + 2w + 1920·Q_dd; WP5e-ε₂ executed (v509, exact, 28 checks): the CPS level-from-flux dial — 'one level' a theorem of clock invariance, the sector counter #prim((E₈)_k) = 1 ⟺ k = 1; and the c_d negative certificate executed (v513, exact, 24 checks, CELEST.DTERM.NONDERIV.01): the 1920 = |W(D₅)| fence typed look-elsewhere-loaded (11/924 vs 8/924 for control 1800) and convention-contingent — the convention-stable [E] core is c_d = 32×60, the physical generation of the 32 stays [O]; WP5e-ε₁ executed (v514, exact, 34 checks): the O(−2) bulk-axion slot is a CONSTRUCTION (equivariant Penrose ledger block by block, the d = 0 slot survives the projection, Molien = the v492 hypersurface), λ̃ = 6 pinned by three exact ledgers (Okubo / measure cancellation excluding 3 and 12 / flux) and the GH/A₃ back-reaction step re-derives the v493 family and the Coxeter clock from geometry; M1 executed (v515, exact, 30 checks, SUCCESS on the preregistered criterion): the back-reacted Ω_N is closed-form on the A₃ twistor family, all S³/ℤ₄ periods (2πi)²-integral with the lockstep flux vector and clock covariance, the lens geometry FORCES the source charge 4 = |μ₄|, and the honest fence stands — integrality alone does not discriminate (0/24 on the forbidden family); M2 executed (v516, exact, 23 checks, SUCCESS on the preregistered criterion ON THE DECLARED COMPLETION MEASURE): the twisted KS measure — the completion-weight identity w = 4h = −4·ch₂ with no free scale, every twisted channel the same perfect Okubo square 36⟨x,x⟩²/det_j, the 32·T₃ cancelled, both v508 certificates and the v511 ψ = 64 slice supplied exactly (no cubic d-channel needed), the completion reading declared [C], the δ₁ chain since decided by v518 — the declared/derived measure question the named [O]; M3 executed (v517, exact, 23 checks, SUCCESS on the preregistered criterion): the a₀ uplift on the GLT kernel χ = log P₄ — the log coefficient 4 = |μ₄| coupled to the centre count on four scales, period response 1/4 integrating to the Coxeter monodromy i, the GLT dictionary [C], the full nonlinear Kähler potential [O]; δ₁ DECIDED (v518, exact + 30-digit kernels, 30 checks, CELEST.WP5E.DELTA1.01 — an honest decided NEGATIVE result): the derived chiral measure — blockwise SL(2,ℤ) covariance solved for, the μ₄ multiplier obstruction a character (koboundary defects (1,1,1), λ(γ) = i^(2B+C/4)) cancelled exactly by the twisted fibre block f₁f₃ = G, not by the three sphere axions — fails all three preregistered testers under both derived solutions with no (N₁,N₂) rescue: a genuine kill on the derived surface, in stated tension with the declared v516 reading (both exact) — since decided at probe level for the declared reading by v520; the w_m derivation executed (v523, exact, 26 checks, ERFOLG: 1/det_j computed from three independent sources — the mode ledger with Abel value (1/2,1/4,1/2), the zeta/Quillen determinant with the unique real positive section, the δ₁f block constant term — the v516 chain reproduced number by number, typed premises TP-REG/TP-Q/TP-NUM/TP-CH); WP5e proper open (the global BCOV quantisation on PT/ℤ₄ — the single remaining milestone, narrowed to the global BCOV integral beyond the fibre zero-mode factor; the v514 fence M1–M3 is fully worked off); SEAM.EQUIV.01 untouched, stays [O]" },
    ],
  },
  {
    id: "09",
    number: 9,
    label: "Safeguards",
    slug: "safeguards",
    title: "Safeguards against Coincidence and Numerology",
    subtitle: "The verification discipline — every mechanism that defends a load-bearing claim against chance, fitting and over-reading",
    abstract:
      "A two-input theory that reads out many small integers is, a priori, at risk of being elaborate numerology. This companion answers that risk not with rhetoric but with a layered, machine-checked discipline, stated uniformly in one place. The layers: (1) a four-class status calculus with a single-source ledger and a sync audit that makes it structurally impossible for a conditional [C] claim to be rendered as exact [E]; (2) an anti-fitting rule (no free pattern, v305) plus a reverse audit (E8.REVERSE.AUDIT.01) that publishes how much E₈ structure carries NO readout (3/8 primary, 5/8 hull overhead); (3) an over-determination map (v427) whose framework separates multiplicative evidence from compression and which — applied to TFPT's own arithmetic witnesses (v428) — finds the seven (Gauss, Eisenstein, cyclotomy, Galois, lattice, Pascal, Coxeter) to be facets of one (2,3,5)/E₈ object (compression, not seven independent witnesses), locating the genuine multiplication in an input forced four independent ways (the '8' in c₃) plus a foreign readout (α⁻¹≈137) — which gives a conservative unconditional floor (~10⁻¹⁰, v432) hardened to an assumption-minimal counting floor (1/94,500 ≈ 4.40σ, no subjective probability, with a monotone concession ladder, v436); (4) the F_transfer firewall (v187) and the No-Unit theorem (v153) that makes the absence of an absolute scale a theorem, not a gap; (5) a frozen prediction registry (v84) with a Monte-Carlo null model (v100, conditional ≤10⁻³⁰·⁷) and a live data scorecard (v375); (6) two independent reproduction paths — an independent Wolfram engine (116/116 + 540/540 checks) and a Lean 4 kernel proof; and (7) an adversarial red-team layer. The thesis is deliberately narrow: these safeguards make coincidence an expensive explanation of the discrete core, and keep exact compiler closure from ever being mistaken for closed physics.",
    status: "safeguards",
    statusLabel: "Verification discipline",
    pdf: "/papers/tfpt_safeguards.pdf",
    inputs: [
      "The whole TFPT stack as the object of audit: the ledger, the Python/Wolfram/Lean suites, the frozen registry, and the red-team document — read as a single discipline rather than per-result.",
    ],
    contribution: [
      "Status calculus: the four display markers [E]/[C]/[O]/[X] are read from the single-source status_ledger.csv, not retyped per document, and audit_sync.py enforces (both directions) that the suite, runner, registry and ledger agree and that every script is cited in a paper body — so a [C] claim cannot be silently shown as [E].",
      "Anti-fitting: the forward discipline / generator-economy audit (v305) admits an identity as load-bearing only if it is derivationally necessary, kills alternatives, is ablation-relevant, links modules, or is testable; the reverse audit (E8.REVERSE.AUDIT.01) publishes that only 3 of 8 E₈ Casimir degrees feed a primary readout (5/8 are unused hull overhead) — and those five are not diffuse slack but the forced two-family ladder 6·spine{2,3,4,5} ⊔ det-ladder{8,14,20}, the residue classes {0,2} mod 6 forced by h=30 (v431, exact arithmetic; the functorial flavour reading honestly kept [P]).",
      "Over-determination map (v427) + honest self-correction (v428): the framework counts multiplicative evidence only across genuinely disjoint grammars; applying it to TFPT's own seven arithmetic witnesses (Gauss N(3+2i)=13, Eisenstein N(3+2ω)=7, cyclotomy N(3+2ζ₅)=55, Galois |(Z/5)ˣ|=4, |det Cartan E₈|=1, Pascal C(4,≤2)=11, Coxeter φ(30)=8) shows — by the Brieskorn classification (v236) — that they are facets of one (2,3,5)/E₈ object: compression, like the anchor a=(1,1,2), not seven independent multiplications. The genuine multiplication is the input forced four independent ways (rank E₈, h(D₅), φ(30), Milnor all =8) plus the foreign witness α⁻¹≈137. Multiplying only across those disjoint pieces gives a conservative unconditional floor (~10⁻¹⁰, v432) that survives even if a skeptic rejects the declared grammar — ~20 orders above the v100 conditional 10⁻³⁰·⁷; the gap is exactly the payoff of deriving the α form (ALPHA.QUILLEN.EXACT.01) (v470: level = computed |C| = 1, normalisation = k_Y = 5/3; v472: the det-line/moduli bridge lemma exhibited at the finite level; the continuum ζ-det identification stays [O]), so the floor and the α-derivation are one lever. Hardened to an assumption-minimal counting floor (v436): the pure-counting α census alone is 1/94 500 ≈ 4.40σ with no subjective probability, and a monotone concession ladder shows the verdict never rests on the contestable input-‘8’ independence.",
      "Firewall + No-Unit: the four frontier transfers stay typed interfaces, never compiler outputs (v187/v213), and the No-Unit theorem (v153) makes v_geo theorem-forbidden; the residual-certification audit (v384) shows every open item is external-math, theorem-forbidden, or external-physics — zero open internal mechanisms.",
      "Frozen predictions + null model: the registry (v84, REG.FREEZE.01) pre-registers the dimensionless predictions, a Monte-Carlo null model (v100) scores each match against chance, and the live scorecard (v375) records the data — including the pre-registered +2.0σ θ₁₃ tension (FLAV.TH13.PRESSURE.01), the opposite of hiding the worst case.",
      "Two independent paths + red team: an independent Wolfram engine (116/116 + 564/564) and a Lean 4 kernel proof (hypercharge, anomaly, Pascal ladder, seam chain) re-derive the exact core, and the red-team companion attacks the theory and publishes what survives each attack.",
    ],
    notClaimed: [
      "These safeguards do not establish physics: they make coincidence expensive for the discrete core and keep the typing honest, but the seam/anchor/transfer bridges remain the open research problem.",
      "The over-determination map is not a Bayesian proof, and we apply it to ourselves: the seven arithmetic witnesses compress one (2,3,5)/E₈ object (v428), so the honest multiplicative evidence is the multiply-forced input plus the foreign α⁻¹, not seven independent grammars.",
    ],
    falsification: [
      "The discipline fails if any claim marked [E] does not in fact machine-check, if the null model is mis-specified so a chance hit is scored as signal, or if a frozen prediction is quietly retuned after data — each is itself an auditable defect.",
    ],
    sections: [
      {
        title: "Layer 1 — the status calculus (no [C] dressed as [E])",
        body: "Every claim carries [E] exact/proven, [C] conditional, [O] open/axiom, or [X] kill test; the finer per-claim type lives in the single source of truth, status_ledger.csv, and the papers and website only mirror it. The sync audit (audit_sync.py) enforces in both directions that the suite, runner, registry and ledger agree, that every script is cited in a paper body, and that no generated surface is stale — so it is structurally impossible to render a conditional claim as exact.",
      },
      {
        title: "Layer 2 — no free pattern, and the reverse audit",
        body: "The forward discipline (v305) admits an identity as load-bearing only under named anti-fitting conditions; the reverse audit (E8.REVERSE.AUDIT.01) asks the honest opposite — of the eight E₈ Casimir degrees, exactly three feed a primary readout (degree 2 the metric, 8 the rank → c₃, 30 the Coxeter number → g_car), and five carry none. Publishing the 5/8 unused overhead is the anti-cherry-picking signal — and those five are not diffuse slack: they are the forced two-family decomposition deg(E₈) = 6·spine{2,3,4,5} ⊔ ({2}∪det-ladder{8,14,20}), the {0,2} mod 6 classes forced by h=30=2·3·5 (v431). Exact arithmetic; the functorial flavour identification stays [P].",
      },
      {
        title: "Layer 3 — the over-determination map (multiply vs. compress)",
        body: "The framework is the right axis (v427): evidence multiplies only across genuinely disjoint grammars, while many readouts from one generator compress. Applied to TFPT's own seven arithmetic witnesses (v428), it forces a self-correction: by the Brieskorn classification (v236) the (2,3,5) singularity is the one generator behind the order-30 clock (Milnor 8 = rank E₈, 30 = 2·3·5 = h(E₈)), so the seven are facets of that same object — they compress, like the anchor a=(1,1,2). What genuinely multiplies is the input forced four independent ways (rank E₈, h(D₅)=8, φ(30), Milnor) plus the foreign witness α⁻¹≈137. Multiplying only across those disjoint pieces yields a conservative unconditional floor (~10⁻¹⁰, v432) that holds even without the declared grammar — ~20 orders above the v100 conditional 10⁻³⁰·⁷; that gap is the payoff of deriving the α form (ALPHA.QUILLEN.EXACT.01), so the floor and the α-derivation are one lever. Hardened (v436): even stripped of every subjective chance assignment, a pure-counting census — of 94 500 complexity-matched α-equations only the TFPT one hits the CODATA window (v100) — gives 1/94 500 ≈ 4.40σ; a monotone concession ladder (30.7 → 25.8 → 4.98 dex) keeps the “not chance” verdict at the most adversarial rung, so it does not rest on the contestable input-‘8’ independence, and the only honest gap to 5σ is one further independent confirmation (a factor ≤ 0.054).",
        formulas: [
          "N(3+2i)=13,\\ N(3+2\\omega)=7,\\ N(3+2\\zeta_5)=55,\\ |(\\mathbb Z/5)^\\times|=4 \\ \\text{(facets of one } (2,3,5)/E_8)",
          "\\operatorname{rank}E_8=h(D_5)=\\varphi(30)=\\mu(2,3,5)=8 \\ \\text{(forced 4 ways)},\\quad \\alpha^{-1}\\approx137\\ \\text{(foreign)}",
          "10^{-10}\\ \\text{(unconditional floor, v432)}\\ \\gg\\ 10^{-30.7}\\ \\text{(v100, conditional on grammar)}",
          "p_\\alpha\\le 1/94500\\approx 4.40\\sigma\\ \\text{(pure counting, v436; no subjective probability)}",
        ],
      },
      {
        title: "Layer 4 — the firewall and the No-Unit theorem",
        body: "The four frontier transfers (F_pole, F_Boltzmann, F_relic, F_QCD) are typed interfaces, never compiler outputs; a machine guard (v187) enforces it, and the recent single-flow reduction (v425) makes their dynamics the one native seam recovery semigroup, leaving only named anchors external. The No-Unit theorem (v153) makes v_geo forbidden by theorem, and the residual-certification audit (v384) shows zero open internal mechanisms.",
      },
      {
        title: "Layers 5–7 — frozen predictions, independent paths, the red team",
        body: "Predictions are pre-registered (v84, REG.FREEZE.01) and scored against a Monte-Carlo null model (v100) with a live scorecard (v375); the exact core is re-derived twice more independently (an independent Wolfram engine, 116+470 checks, and a Lean 4 kernel proof with no sorry); and the red-team companion attacks the theory and states what survives — including its own honesty that c=8 alone does not select (E₈)₁ (holomorphy, |det K|=1, is the load-bearing extra).",
      },
    ],
    keyFormulas: [
      {
        label: "Seven readouts → one object",
        latex: "N(3{+}2i){=}13,\\ N(3{+}2\\omega){=}7,\\ N(3{+}2\\zeta_5){=}55,\\ |(\\mathbb Z/5)^\\times|{=}4",
        description: "Facets of one (2,3,5)/E₈ object ⇒ compression, not multiplication (v428)",
      },
      {
        label: "What genuinely multiplies",
        latex: "\\operatorname{rank}E_8=h(D_5)=\\varphi(30)=\\mu(2,3,5)=8",
        description: "The '8' in c₃ forced four independent ways, plus the foreign α⁻¹≈137 (v428)",
      },
      {
        label: "Reverse audit",
        latex: "3/8\\ \\text{primary readouts},\\quad 5/8 = 6{\\cdot}\\text{spine} \\sqcup \\text{det-ladder}",
        description: "How much E₈ structure carries NO readout — published, not hidden; the 5/8 is forced two-family structure, not diffuse overhead (v431)",
      },
      {
        label: "No-Unit theorem",
        latex: "\\dim[c_3]=\\dim[g_{\\mathrm{car}}]=0 \\Rightarrow v_{\\mathrm{geo}}\\ \\text{theorem-forbidden}",
        description: "A dimensionless compiler cannot output an absolute scale (v153)",
      },
    ],
    highlights: [
      { label: "Status classes", value: "4", description: "[E]/[C]/[O]/[X], ledger-sourced, audit-enforced — no [C] dressed as [E]" },
      { label: "Witnesses → one object", value: "7→1", description: "Gauss, Eisenstein, cyclotomy, Galois, lattice, Pascal, Coxeter — facets of one (2,3,5)/E₈ object, so they compress (v428)" },
      { label: "Reverse audit", value: "3/8", description: "Only 3 of 8 E₈ degrees feed a primary readout; the 5/8 overhead is forced two-family structure 6·spine ⊔ det-ladder (v431), not diffuse slack" },
      { label: "Firewall", value: "4 typed", description: "F_pole/F_Boltzmann/F_relic/F_QCD never compiler outputs (v187); No-Unit makes v_geo a theorem (v153)" },
      { label: "Unconditional floor", value: "~10⁻¹⁰", description: "Disjoint-pieces-only improbability (v432), grammar-independent; ~20 orders above the v100 conditional 10⁻³⁰·⁷" },
      { label: "Counting floor", value: "≈4.40σ", description: "Assumption-minimal, no subjective probability: 1 of 94,500 complexity-matched α variants hits CODATA (v436); a monotone concession ladder holds the verdict at the most adversarial rung" },
      { label: "Independent paths", value: "2", description: "Wolfram (116+470) + Lean 4 kernel proof re-derive the exact core" },
      { label: "Worst case shown", value: "θ₁₃ +2.0σ", description: "The most-tensioned prediction is pre-registered, not hidden (FLAV.TH13.PRESSURE.01)" },
    ],
  },
];

export function paperLabel(p: Paper): string {
  return p.label ?? `Paper ${p.number}`;
}
