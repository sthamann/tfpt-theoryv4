export type PaperStatus = "core" | "bridge" | "conditional" | "downstream";

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
  { label: string; color: string; bg: string; ring: string }
> = {
  core: {
    label: "Core Theorem",
    color: "text-blue-300",
    bg: "bg-blue-500/10",
    ring: "ring-blue-500/30",
  },
  bridge: {
    label: "Bridge Readout",
    color: "text-emerald-300",
    bg: "bg-emerald-500/10",
    ring: "ring-emerald-500/30",
  },
  conditional: {
    label: "Conditional Closure",
    color: "text-orange-300",
    bg: "bg-orange-500/10",
    ring: "ring-orange-500/30",
  },
  downstream: {
    label: "Downstream Interface",
    color: "text-fuchsia-300",
    bg: "bg-fuchsia-500/10",
    ring: "ring-fuchsia-500/30",
  },
};

export const papers: Paper[] = [
  {
    id: "00",
    number: 0,
    slug: "orientation",
    title: "TFPT in One Map",
    subtitle: "Boundary Polarization, Carrier Rigidity, and Observable Closure",
    abstract:
      "The thin entry document for the TFPT 4.5 series. It does not attempt to prove the full theory. Its purpose is to state what TFPT claims, what it does not claim, how the closed branch is organized, and where each load-bearing argument is isolated in the paper sequence.",
    status: "core",
    statusLabel: "Orientation",
    pdf: "/papers/00_orientation_note.pdf",
    inputs: ["None — public orientation layer for the series"],
    contribution: [
      "Organization, status discipline, and a dependency map for the closed-branch argument.",
    ],
    notClaimed: [
      "No carrier proof, no exact electromagnetic calculation, no CMB fit, no mass ledger, no E8 stage atlas, and no nonperturbative QFT proof.",
    ],
    falsification: [
      "The note can fail if it misstates the dependency order, overstates the status of a downstream module, or hides where an assumption first enters.",
    ],
    sections: [
      {
        title: "What TFPT Claims",
        body: "TFPT is organized as a boundary-polarized spectral theory whose primitive input is a one-sided boundary datum. The main theorem chain is not a collection of unrelated numerological readouts — it is a staged reconstruction.",
        formulas: [
          "\\mathfrak{S}_{\\min}\\Rightarrow\\mathcal{B}_{\\min}\\Rightarrow\\mathfrak{T}_\\partial \\Rightarrow (\\tau_{\\mathrm{dbl}},\\iota_C,P_{\\mathrm{prim}},[u_\\Sigma],c_3) \\Rightarrow d^\\star_{\\mathrm{disc}}\\Rightarrow P_{\\mathrm{adm}}\\Rightarrow \\mathfrak{T}_\\star",
        ],
      },
      {
        title: "The Three Decoders",
        body: "The closed branch is read through three decoders that separate structure, counting, and bridge observables.",
        formulas: [
          "Y \\text{ generates structure}",
          "[u_\\Sigma]=1 \\text{ generates counting}",
          "u := \\varphi_0 \\text{ generates bridge observables}",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Staged reconstruction",
        latex:
          "\\mathfrak{S}_{\\min}\\Rightarrow\\mathcal{B}_{\\min}\\Rightarrow\\mathfrak{T}_\\partial \\Rightarrow \\mathfrak{T}_\\star",
        description: "The full burden-of-proof chain from minimal seed to closed branch.",
      },
    ],
    highlights: [
      {
        label: "Layers",
        value: "7",
        description: "Stratified derivation chain, from boundary primitive to cosmology",
      },
      {
        label: "Decoders",
        value: "3",
        description: "Y for structure, [u_Σ]=1 for counting, φ₀ for observables",
      },
      {
        label: "Status discipline",
        value: "4",
        description: "Theorem core, bridge, conditional closure, downstream",
      },
    ],
  },
  {
    id: "01",
    number: 1,
    slug: "boundary-kernel",
    title: "Boundary Polarization and the Primitive Kernel",
    subtitle: "The boundary primitive kernel of TFPT",
    abstract:
      "This paper isolates the primitive boundary kernel. Starting from the minimal operational seed and the one-sided boundary datum, it reconstructs the exact double, the deck involution, the Calderón polarization, the primitive admissibility complex, the primitive seam generator, the winding normalization, and the c₃ normalization. No Standard-Model, phenomenological, gravitational, cosmological, or E8 claim is made in this paper.",
    status: "core",
    statusLabel: "Theorem-level core",
    pdf: "/papers/01_boundary_kernel.pdf",
    inputs: ["Only the orientation map of Paper 0, if read first."],
    contribution: [
      "The primitive kernel 𝓣ᵏᵉʳ_∂ = (𝒜, ℋ, D, J, Γ, τ_dbl, ι_C, P_prim, [u_Σ], c₃) is reconstructed from the one-sided boundary datum rather than inserted later.",
    ],
    notClaimed: [
      "No carrier 3+2 theorem.",
      "No Standard-Model gauge group.",
      "No α, no flavor, no gravity, no cosmology, no E8 grammar.",
    ],
    falsification: [
      "Fails if the one-sided datum does not determine the doubled datum, the Calderón polarization, the primitive Hodge selector, or the normalization of the primitive seam class.",
      "Fails if minimality is read as a preference order over desired physics rather than as a presentation-invariant defect filtration on essentialized bordisms.",
    ],
    sections: [
      {
        title: "One-Sided Boundary Datum",
        body:
          "The starting object is a one-sided boundary datum from which all primitive structure is reconstructed by canonical procedure, not by hand.",
        formulas: [
          "\\mathfrak{T}_\\partial = (\\mathcal{A}_+, \\mathcal{H}_+, D_+, J, \\Gamma, B_\\Sigma)",
        ],
      },
      {
        title: "Exact Double and Deck Involution",
        body:
          "The exact double reconstructs the closed minimal datum carrying the Calderón polarization-induced involution. This section carries the analytic interface to Calderón projectors.",
        formulas: [
          "\\mathfrak{T}_{\\min}^{\\mathrm{cl}} = (\\mathcal{A}, \\mathcal{H}, D, J, \\Gamma, \\tau_{\\mathrm{dbl}}, \\iota_C)",
        ],
      },
      {
        title: "Primitive Admissibility Complex",
        body:
          "The primitive selector is introduced before any color, determinant, family, or QFT sector. A later full selector can factor through P_prim.",
        formulas: ["P_{\\mathrm{prim}} = \\Pi_{\\ker \\Delta_{\\mathrm{prim}}}"],
      },
      {
        title: "Primitive Seam Generator",
        body:
          "The primitive seam generator records the two normalizations that survive at this level. The winding class is a primitive boundary output, not yet a family-counting input.",
        formulas: ["[u_\\Sigma] = 1, \\qquad c_3 = \\frac{1}{8\\pi}"],
      },
      {
        title: "Defect Filtration on Essentialized Bordisms",
        body:
          "Minimality is not a wishlist over preferred physics. It is a canonical defect filtration 𝔇(B^ess) on essentialized admissible bordisms, ordered lexicographically. Each later coordinate is only defined on the stratum where all earlier obstructions are minimal — it is an order of definitions, not an order of weights.",
        formulas: [
          "\\mathfrak{D}(B) = \\big(d_0(B),\\, d_1(B),\\, d_2(B),\\, d_3(B)\\big)",
          "d_0 = |SF(U_\\Sigma)|, \\;\\; d_1 = \\operatorname{rank}_{\\mathrm{ess}}(H^{\\mathrm{fin}}_{\\mathrm{prim}}), \\;\\; d_2 = \\deg^+_{\\mathrm{det}}, \\;\\; d_3 = h^{\\mathrm{red}}_\\Sigma",
        ],
      },
      {
        title: "Essentialization (Stability against Trivial Stabilization)",
        body:
          "For every admissible bordism B, define B^ess = B / B^triv where B^triv is the maximal direct summand on which all primitive load-bearing data vanish. The defect filtration is then read on the essentialized bordism. Adding an empty internal factor cannot change the lexicographic order — rank minimality is not vulnerable under trivial stabilization.",
        formulas: [
          "B^{\\mathrm{ess}} := B / B^{\\mathrm{triv}}",
          "B^{\\mathrm{triv}}: \\quad SF = 0,\\; \\iota_C \\text{ trivial},\\; \\deg_{\\mathrm{det}} = 0,\\; Y_{\\mathrm{prim}}^{\\mathrm{type}} = 0",
          "\\mathfrak{D}(B) := \\mathfrak{D}(B^{\\mathrm{ess}})",
        ],
      },
      {
        title: "Invariance Theorem for Equivalent Presentations",
        body:
          "The lexicographic minimizer is presentation-independent. If F is an equivalence of admissible presentations and ψ_i are strictly increasing per-coordinate maps, then B is a minimizer of 𝔇 if and only if F(B) is a minimizer of 𝔇'. Strictly increasing coordinate maps preserve and reflect the first coordinate at which two vectors differ.",
        formulas: [
          "F: \\mathcal{C} \\to \\mathcal{C}', \\quad d'_i(F(B)) = \\psi_i(d_i(B)), \\quad \\psi_i \\text{ strictly increasing}",
          "\\mathfrak{D}(B) <_{\\mathrm{lex}} \\mathfrak{D}(C) \\iff \\mathfrak{D}'(F(B)) <_{\\mathrm{lex}} \\mathfrak{D}'(F(C))",
        ],
      },
      {
        title: "Minimal Values on the Canonical Branch",
        body:
          "After the repair the minimal chain reads: d_0 = 1 from the minimal nontrivial seam winding; d_1 = dim E_- + dim E_+ = 5 from compact Higgs and primitive Yukawa (downstream of Paper 2); d_2 = 1 from the minimal nonnegative determinant class; d_3 from reduced boundary nullity. The corner count and the 3+2 carrier ranks are not free minimization coordinates here — they are read off downstream.",
        formulas: [
          "(d_0, d_1, d_2) = (1, 5, 1)",
          "|SF(U_\\Sigma)| = 1 \\Rightarrow N_{\\mathrm{corner}} = 4 \\;\\;\\text{(derived, not minimized)}",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Boundary primitive kernel",
        latex:
          "\\mathfrak{T}_\\partial^{\\mathrm{ker}} = (\\mathcal{A}, \\mathcal{H}, D, J, \\Gamma, \\tau_{\\mathrm{dbl}}, \\iota_C, P_{\\mathrm{prim}}, [u_\\Sigma], c_3)",
        description: "The full primitive kernel reconstructed from the one-sided datum.",
      },
      {
        label: "Winding normalization",
        latex: "[u_\\Sigma] = 1",
        description: "Primitive seam class, the source of family counting downstream.",
      },
      {
        label: "Coupling normalization",
        latex: "c_3 = \\dfrac{1}{8\\pi}",
        description: "Derived without empirical input, fixed before any phenomenology.",
      },
    ],
    highlights: [
      {
        label: "Datum",
        value: "1-sided",
        description: "Single boundary datum reconstructs all primitive structure",
      },
      {
        label: "c₃",
        value: "1/8π",
        description: "Primitive coupling normalization, no empirical tuning",
      },
      {
        label: "[u_Σ]",
        value: "1",
        description: "Winding class normalization, fixed at the primitive level",
      },
    ],
  },
  {
    id: "02",
    number: 2,
    slug: "carrier-rigidity",
    title: "Carrier Rigidity and the Standard-Model Packet",
    subtitle: "Hypercharge, Spinor Packet, and the SM gauge quotient from boundary polarization",
    abstract:
      "The carrier polynomial is no longer taken as an entry assumption. Boundary polarization first gives a finite essential two-point carrier E = E_- ⊕ E_+. The compact determinant / Higgs index fixes dim E_+ = 2, while primitive indecomposable Yukawa type fixes the complementary essential rank dim E_- = 3. The determinant-normalized generator is then forced to be Y = −1/3 P_- + 1/2 P_+, and the former carrier equation 6Y² − Y − 1 = 0 with tr_E Y = 0 appears only as its algebraic shadow. From this derived carrier follow the hypercharge vector, the even exterior packet S⁺ = Λ^even E, one chiral Standard-Model family including ν^c, the physical gauge quotient, family counting, admissible occupancy, and the abelian index coefficient.",
    status: "core",
    statusLabel: "Theorem-level core",
    pdf: "/papers/02_carrier_rigidity.pdf",
    inputs: [
      "The primitive boundary kernel (τ_dbl, ι_C, P_prim, [u_Σ], c₃) from Paper 1.",
      "Essential carrier block — no contractible spectator summand.",
      "Compact determinant / Higgs index on the positive polarization block.",
      "Primitive indecomposable Yukawa type — local trilinear with two fermionic legs and one seam-even bosonic leg.",
    ],
    contribution: [
      "Boundary polarization → finite carrier involution ε_car = ι_C|_E with E = E_- ⊕ E_+ (no rank yet).",
      "Compact Higgs index on S² with L_+ ≃ 𝒪(1) → dim E_+ = 2.",
      "Primitive Yukawa type forces Λ³E_- = det E_- → dim E_- = 3.",
      "Determinant-normalized generator Y = −1/3 P_- + 1/2 P_+ as a corollary, with 6Y² − Y − 1 = 0 as its minimal polynomial.",
      "Even exterior packet S⁺ = Λ^even E, gauge quotient G_phys = (SU(3) × SU(2) × U(1)_Y)/ℤ₆, and discrete counting outputs N_fam = 3, Ω_adm = 48, N_Φ = 1, b₁ = 41/10.",
    ],
    notClaimed: [
      "The carrier polynomial is not assumed — only used as the algebraic shadow of the derived eigenvalues.",
      "No exact α value, no CKM / PMNS closure, no value-level transport Yukawa matrices.",
      "No pole-mass ledger, no OS reconstruction, no cosmology, no E8 grammar.",
    ],
    falsification: [
      "Fails if the carrier polynomial 6Y² − Y − 1 = 0 is invoked before the rank discharge (compact Higgs and primitive Yukawa) is complete.",
      "Fails if the determinant-normalized two-point generator is not forced before any phenomenological matching.",
      "Fails if Standard-Model representation data is imported by hand at any earlier step.",
    ],
    sections: [
      {
        title: "1. Boundary Carrier Involution",
        body:
          "The paper does not begin with the carrier polynomial. It begins with the involution induced by the Calderón polarization. At this stage there is only a two-point algebra ℂ[ε_car] = {a·1 + b·ε_car} — no 3+2 split, no hypercharge vector, no Standard-Model packet has been used.",
        formulas: [
          "\\varepsilon_{\\mathrm{car}} := \\iota_C\\big|_E, \\qquad \\varepsilon_{\\mathrm{car}}^2 = \\mathbf{1}",
          "E = E_- \\oplus E_+, \\qquad P_\\pm = \\tfrac{\\mathbf{1} \\pm \\varepsilon_{\\mathrm{car}}}{2}",
        ],
      },
      {
        title: "2. Essential Carrier Block",
        body:
          "All contractible spectator summands on which seam winding, determinant clutching, and the primitive local interaction type vanish are quotiented out. The defect filtration is read on the essentialized bordism B^ess. This prevents any artificial reduction by a trivial direct factor.",
        formulas: [
          "B^{\\mathrm{ess}} = B / B^{\\mathrm{triv}}",
          "B^{\\mathrm{triv}}: \\quad SF=0,\\; \\iota_C \\text{ trivial},\\; \\deg_{\\mathrm{det}} = 0,\\; Y_{\\mathrm{prim}}^{\\mathrm{type}} = 0",
        ],
      },
      {
        title: "3. Compact Higgs Index → dim E_+ = 2",
        body:
          "The unit seam winding selects the minimal nonnegative determinant class on the compactified normal sphere. The seam-even positive polarization block carries c₁(L_+) = 1, the determinant-neutral negative block c₁(L_-) = 0. Riemann–Roch on 𝒪(1) over S² gives a 2-dimensional space of holomorphic sections — this fixes the positive rank, with no Standard-Model name yet attached.",
        formulas: [
          "L_+ \\simeq \\mathcal{O}(1), \\quad L_- \\simeq \\mathcal{O} \\;\\;\\text{on}\\;\\; S^2",
          "H^0(S^2,\\mathcal{O}(1)) \\simeq \\mathbb{C}^2, \\qquad H^1(S^2,\\mathcal{O}(1)) = 0",
          "\\Rightarrow \\;\\; \\dim E_+ = 2",
        ],
      },
      {
        title: "4. Primitive Yukawa Type → dim E_- = 3",
        body:
          "The retained branch contains a nonzero primitive indecomposable local trilinear with two fermionic legs and one seam-even bosonic leg. With dim E_+ = 2, the seam-even bosonic leg contributes the line Λ²E_+. Closure of the negative factor without a spectator forces Λ³E_- = det E_-, hence dim E_- = 3. This is a local type statement, not the value-level transport Yukawa matrices, which belong downstream to Paper 3.",
        formulas: [
          "Y_{\\mathrm{prim}}^{\\mathrm{type}}:\\;\\; (E_- \\otimes E_+) \\otimes \\Lambda^2 E_- \\otimes E_+ \\longrightarrow \\Lambda^3 E_- \\otimes \\Lambda^2 E_+ \\simeq \\mathbb{C}",
          "\\Rightarrow \\;\\; \\Lambda^3 E_- = \\det E_- \\;\\Rightarrow\\; \\dim E_- = 3",
        ],
      },
      {
        title: "5. Determinant-Normalized Generator Y",
        body:
          "Once (dim E_-, dim E_+) = (3, 2) is fixed by the boundary and index arguments, the primitive integer determinant-preserving generator has a unique solution. One unit of determinant winding per block normalizes the eigenvalues to −1/3 and 1/2.",
        formulas: [
          "X = q_- P_- + q_+ P_+, \\quad 3 q_- + 2 q_+ = 0, \\quad q_- < 0 < q_+, \\quad \\gcd(|q_-|, q_+) = 1",
          "\\Rightarrow \\;\\; (q_-, q_+) = (-2, 3) \\;\\Rightarrow\\; X = -2 P_- + 3 P_+",
          "Y = X / 6 = -\\tfrac{1}{3} P_- + \\tfrac{1}{2} P_+",
        ],
      },
      {
        title: "6. Carrier Polynomial as Corollary",
        body:
          "Now the former carrier equation appears only as the minimal polynomial of the two derived roots. The trace vanishes automatically because 3·(−1/3) + 2·(1/2) = 0. The coefficient 6 = 3·2 is not guessed — it is the determinant-periodized block normalization of the rigid 3+2 carrier.",
        formulas: [
          "\\left(Y + \\tfrac{1}{3}\\right)\\left(Y - \\tfrac{1}{2}\\right) = 0 \\;\\;\\Longleftrightarrow\\;\\; 6 Y^2 - Y - \\mathbf{1} = 0",
          "\\operatorname{tr}_E Y = 3 \\cdot \\left(-\\tfrac{1}{3}\\right) + 2 \\cdot \\left(\\tfrac{1}{2}\\right) = 0",
          "\\text{General split: } b s\\, Y^2 + (s - b) Y - \\mathbf{1} = 0, \\;\\; (b, s) = (3, 2)",
        ],
      },
      {
        title: "7. Hypercharge, Exterior Packet & Stabilizer",
        body:
          "Renaming E_3 := E_- and E_2 := E_+ recovers the diagonal hypercharge vector. The even exterior packet S⁺ = Λ^even E has dimension 16 and carries one chiral Standard-Model family including the right-handed neutrino. The internal stabilizer of the carrier datum yields the physical gauge quotient — read as a stabilizer theorem, not as a reconstruction of a known gauge group.",
        formulas: [
          "Y = \\operatorname{diag}\\!\\left(-\\tfrac{1}{3},-\\tfrac{1}{3},-\\tfrac{1}{3},\\tfrac{1}{2},\\tfrac{1}{2}\\right)",
          "S^+ = \\Lambda^{\\mathrm{even}} E, \\qquad \\dim S^+ = 16",
          "G_{\\mathrm{phys}} = \\frac{SU(3) \\times SU(2) \\times U(1)_Y}{\\mathbb{Z}_6}",
        ],
      },
      {
        title: "8. Counting Outputs",
        body:
          "Family count, admissible occupancy, the compact bosonic index, and the abelian index coefficient follow as structural consequences of the carrier, winding, occupancy, and Higgs-index closure — not as precision-observable readouts.",
        formulas: [
          "N_{\\mathrm{fam}} = 3, \\qquad \\Omega_{\\mathrm{adm}} = 48, \\qquad N_\\Phi = 1, \\qquad b_1 = \\tfrac{41}{10}",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Boundary involution (start)",
        latex:
          "\\varepsilon_{\\mathrm{car}} = \\iota_C|_E,\\;\\; E = E_- \\oplus E_+",
        description: "From Calderón polarization — no rank yet.",
      },
      {
        label: "Compact Higgs index → dim E_+",
        latex: "H^0(S^2, \\mathcal{O}(1)) \\simeq \\mathbb{C}^2",
        description: "Riemann–Roch on the seam-even line bundle gives dim E_+ = 2.",
      },
      {
        label: "Primitive Yukawa → dim E_-",
        latex: "\\Lambda^3 E_- = \\det E_- \\Rightarrow \\dim E_- = 3",
        description: "Type-level statement — not value-level transport matrix.",
      },
      {
        label: "Determinant-normalized Y",
        latex: "Y = -\\tfrac{1}{3} P_- + \\tfrac{1}{2} P_+",
        description: "Forced — not chosen — by the discharged ranks (3, 2).",
      },
      {
        label: "Carrier polynomial (corollary)",
        latex: "6 Y^2 - Y - \\mathbf{1} = 0",
        description:
          "Minimal polynomial of the derived roots, not an entry assumption.",
      },
    ],
    highlights: [
      {
        label: "Carrier polynomial",
        value: "Corollary",
        description: "Derived from boundary + compact Higgs + primitive Yukawa",
      },
      {
        label: "dim E_+",
        value: "2",
        description: "Riemann–Roch on the compact Higgs index",
      },
      {
        label: "dim E_-",
        value: "3",
        description: "Primitive Yukawa type forces Λ³E_- = det E_-",
      },
      {
        label: "Coefficient 6",
        value: "= 3·2",
        description: "Determinant-periodized block normalization",
      },
    ],
  },
  {
    id: "03",
    number: 3,
    slug: "em-flavor-transport",
    title: "Electromagnetic Closure and Flavor Transport",
    subtitle: "α, the cusp cubic, and the rigid flavor branch",
    abstract:
      "After the primitive kernel and carrier packet are fixed, the precision-readout layer of TFPT addresses the electromagnetic fixed point, the transport pole of the cusp cubic, the retained seed decoder, and the flavor transport grammar yielding α, δ_ph, λ_C, β_rad, Ω_b, θ₁₃, CKM, and PMNS readouts.",
    status: "bridge",
    statusLabel: "Bridge / precision readout",
    pdf: "/papers/03_em_closure.pdf",
    inputs: [
      "Paper 1 supplies the primitive kernel and [u_Σ] = 1.",
      "Paper 2 supplies the rigid carrier, family count, admissible occupancy, compact Higgs index, and abelian index coefficient.",
    ],
    contribution: [
      "Electromagnetic fixed point α⁻¹(0) = 137.035 999 216 8…",
      "Transport pole of the cusp cubic determines δ_ph.",
      "Retained seed decoder λ_C = √(φ₀(1 − φ₀)) and downstream flavor readouts.",
    ],
    notClaimed: [
      "No full QFT closure.",
      "No gravity / metrology proof, no CMB.",
      "No E8 grammar, no large pole-mass tables.",
    ],
    falsification: [
      "Fails if any numerical constant enters after the fact, if α is used to tune later readouts, or if alternative discrete worlds are not visibly ruled out by the same branch constraints.",
    ],
    sections: [
      {
        title: "Electromagnetic Closure",
        body: "The fine-structure constant emerges as the unique positive root of a self-consistent closure equation built only from primitive normalizations and the carrier packet.",
        formulas: [
          "\\alpha^{-1}(0) = 137.035\\,999\\,216\\,8\\ldots",
          "F_{U(1)}(\\alpha)=\\alpha^3 - 2c_3^3\\alpha^2 - \\frac{4}{5}c_3^6\\!\\left(\\sum_{f,j} L_{f,j}^{\\mathrm{diag}} + N_\\Phi\\right)\\log(\\varphi_{\\mathrm{seam}}(\\alpha)^{-1})",
        ],
      },
      {
        title: "Transport Pole — the Cusp Cubic",
        body: "The transport phase is governed by a cubic with three explicit roots. The lower critical point determines δ_ph on the retained branch.",
        formulas: [
          "P(z) = (z-1)\\!\\left(z-\\tfrac{64}{729}\\right)\\!\\left(z-\\tfrac{1}{729}\\right)",
          "P'(z) = 0",
        ],
      },
      {
        title: "Retained Seed Decoder",
        body: "The retained seed projects to bridge observables.",
        formulas: [
          "u := \\varphi_0",
          "\\lambda_C = \\sqrt{\\varphi_0(1-\\varphi_0)}",
          "\\beta_{\\mathrm{rad}} = \\frac{\\varphi_0}{4\\pi}",
          "\\sin^2\\theta_{13} = \\varphi_0 e^{-\\gamma}",
        ],
      },
      {
        title: "Flavor Transport — CKM and PMNS",
        body: "CKM and PMNS closure follow from holonomy transport on the rigid branch, including hard readouts such as |V_ub| = |V_us|³/3.",
        formulas: ["|V_{ub}| = \\frac{|V_{us}|^3}{3}"],
      },
    ],
    keyFormulas: [
      {
        label: "α inverse",
        latex: "\\alpha^{-1}(0) = 137.035\\,999\\,216\\,8\\ldots",
        description: "Closed-branch root, no fit parameters.",
      },
      {
        label: "Cabibbo seed",
        latex: "\\lambda_C = \\sqrt{\\varphi_0 (1-\\varphi_0)}",
        description: "From φ₀ = 1/(6π) + 3/(256π⁴).",
      },
      {
        label: "Cusp cubic",
        latex:
          "P(z) = (z-1)(z-\\tfrac{64}{729})(z-\\tfrac{1}{729})",
        description: "Transport phase polynomial, source of δ_ph.",
      },
    ],
    highlights: [
      {
        label: "α⁻¹(0)",
        value: "137.0360",
        description: "Computed root vs CODATA 137.035 999 084(21)",
      },
      {
        label: "λ_C",
        value: "0.22438",
        description: "Cabibbo angle from retained seed",
      },
      {
        label: "sin²θ₁₃",
        value: "0.02311",
        description: "Reactor angle from neutrino closure",
      },
      {
        label: "Free knobs",
        value: "0",
        description: "No-knobs audit: every constant traced upstream",
      },
    ],
  },
  {
    id: "04",
    number: 4,
    slug: "admissibility-qft",
    title: "Admissibility, Strong CP, and Nonperturbative QFT Closure",
    subtitle: "Selector vs. dynamics on the TFPT branch",
    abstract:
      "The analytic closure layer of TFPT. The selector P_adm is treated as a physical admissible-sector construction, while the dynamics is carried by Z_rel, admissible Schwinger distributions, Osterwalder–Schrader reconstruction, the local Minkowski net, stable massive scattering, and the exact admissible RG flow.",
    status: "conditional",
    statusLabel: "Conditional closure",
    pdf: "/papers/04_admissibility_qft.pdf",
    inputs: [
      "Paper 1 supplies P_prim.",
      "Paper 2 supplies the carrier and discrete determinant data.",
      "Paper 3 is not logically required except for cross-references.",
    ],
    contribution: [
      "Conditional nonperturbative closure: P_adm = P_prim · P_sing · P_Θ, with θ_eff = 0 and arg det M_u = arg det M_d = 0.",
      "Reflection positivity, OS reconstruction, local Minkowski net, stable massive scattering, exact admissible RG flow.",
    ],
    notClaimed: [
      "No α detail calculation.",
      "No CMB, no E8.",
      "No full empirical tables.",
    ],
    falsification: [
      "Fails if selector and dynamics are conflated, if positivity/gap hypotheses are hidden, or if strong-CP closure uses an inadmissible phase convention.",
    ],
    sections: [
      {
        title: "Selector vs. Dynamics",
        body: "The central distinction: P_adm selects the physical sector, while dynamics is carried by Z_rel, then S^T_n, then OS reconstruction, then the local net, the flow Γ_k, and the renormalized observable layer. This separation is the main defence against overclaiming.",
        formulas: [
          "P_{\\mathrm{adm}} \\quad \\text{selects the physical sector}",
          "Z_{\\mathrm{rel}}\\Rightarrow\\{S_n^T\\}\\Rightarrow(\\mathcal{H}_{\\mathrm{adm}},\\mathfrak{A}_{\\mathrm{adm}})\\Rightarrow \\Gamma_k \\Rightarrow \\mathfrak{G}^{\\mathrm{ren}}_{\\mathrm{TFPT}}",
        ],
      },
      {
        title: "Full Admissibility Complex",
        body: "After carrier and determinant data are fixed, the full selector is composed of three admissibility projectors.",
        formulas: ["P_{\\mathrm{adm}} = P_{\\mathrm{prim}} \\, P_{\\mathrm{sing}} \\, P_\\Theta"],
      },
      {
        title: "Strong CP Closure",
        body: "The strong-CP sector is stated as an admissibility result. The argument connects hadronic singlet selection, determinant structure, γ₅-Hermiticity, and the sheet involution without importing phenomenological tuning.",
        formulas: [
          "\\theta_{\\mathrm{eff}} = 0",
          "\\arg\\det M_u = \\arg\\det M_d = 0",
        ],
      },
      {
        title: "Exact Admissible RG Flow",
        body: "The exact admissible flow is the analytic continuation of the same sector, with the admissible projection included in the flow definition.",
        formulas: [
          "\\partial_k \\Gamma_k = \\tfrac{1}{2}\\operatorname{STr}\\!\\left[(\\Gamma_k^{(2)} + R_k)^{-1}\\partial_k R_k\\right]_{\\mathrm{adm}}",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Admissibility selector",
        latex: "P_{\\mathrm{adm}} = P_{\\mathrm{prim}} \\, P_{\\mathrm{sing}} \\, P_\\Theta",
        description: "Composition of three admissibility projectors.",
      },
      {
        label: "Strong-CP null",
        latex: "\\theta_{\\mathrm{eff}} = 0",
        description: "Theorem-level null on the admissible branch.",
      },
    ],
    highlights: [
      {
        label: "θ_eff",
        value: "0",
        description: "Theorem-level null, not a tuned parameter",
      },
      {
        label: "OS",
        value: "✓",
        description: "Osterwalder–Schrader reconstruction inside the admissible sector",
      },
      {
        label: "Selector",
        value: "P_adm",
        description: "Three projectors: primitive, singlet, theta",
      },
    ],
  },
  {
    id: "05",
    number: 5,
    slug: "metrology",
    title: "Geometric Hodge Closure and Dimensionless Metrology",
    subtitle: "Boundary-normalized observables from λ_Σ",
    abstract:
      "The geometric and metrological branch of TFPT. The theory is not presented as predicting isolated SI numbers. Instead it constructs an internal dimensionless metrology from the boundary spectral unit λ_Σ, with gravity, Planck normalization, electroweak matching, and pole readouts expressed as boundary-normalized observables.",
    status: "bridge",
    statusLabel: "Bridge / metrology",
    pdf: "/papers/05_metrology.pdf",
    inputs: [
      "Paper 1 supplies the boundary branch and primitive spectral unit.",
      "Paper 2 supplies the carrier/Higgs structure.",
      "Paper 4 may supply the renormalized observable layer when the analytic QFT closure is referenced.",
    ],
    contribution: [
      "Boundary-normalized metrology: λ_Σ = λ₁⁺(|B_Σ|), ρ★ = χ_geo,0² / λ_Σ², M_Pl² / λ_Σ² = ρ★/(2π²), G_N λ_Σ² = π/(4ρ★).",
    ],
    notClaimed: [
      "No late-time H₀, no CMB.",
      "No black holes, no horizons, no E8 stage atlas, no astrophysical bursts.",
    ],
    falsification: [
      "Fails if SI units enter as hidden inputs, if λ_Σ is not fixed by the boundary branch, or if electroweak matching is mixed with cosmological comparison rows.",
    ],
    sections: [
      {
        title: "Boundary Spectral Unit",
        body: "The internal unit comes from the first eigenvalue of the boundary operator. All dimensionful-looking statements are rewritten as dimensionless quotients by powers of λ_Σ.",
        formulas: ["\\lambda_\\Sigma = \\lambda_1^+\\!\\left(|B_\\Sigma|\\right)"],
      },
      {
        title: "Planck Normalization",
        body: "The Planck readout is internal — the question is not which SI value of G_N is inserted, but which dimensionless branch quotient is fixed.",
        formulas: [
          "\\rho_\\star = \\frac{\\chi_{\\mathrm{geo},0}^2}{\\lambda_\\Sigma^2}",
          "\\frac{\\bar M_{\\mathrm{Pl}}^2}{\\lambda_\\Sigma^2} = \\frac{\\rho_\\star}{2\\pi^2}",
          "G_N \\lambda_\\Sigma^2 = \\frac{\\pi}{4\\rho_\\star}",
        ],
      },
      {
        title: "Electroweak Matching",
        body: "The electroweak matching layer is included only as boundary-normalized metrology. Pole matching enters in compact form when expressed as a quotient by λ_Σ.",
        formulas: [
          "v_{\\mathrm{phys}} = v_{\\mathrm{geo}}\\sqrt{Z_{\\mathrm{EW}}^{\\mathrm{TFPT}}}",
          "G_N v_{\\mathrm{phys}}^2",
        ],
      },
      {
        title: "Observable Functor Chain",
        body: "Outputs are organized as a chain: closed branch, renormalized observables, physical observables, and finally scheme-projected observables.",
        formulas: [
          "\\mathfrak{T}_\\star \\xrightarrow{\\mathcal{R}_{\\mathrm{ren}}} \\mathfrak{G}^{\\mathrm{ren}}_{\\mathrm{TFPT}} \\xrightarrow{\\mathcal{M}_{\\mathrm{phys}}} \\mathfrak{O}^{\\mathrm{phys}}_{\\mathrm{TFPT}} \\xrightarrow{\\mathcal{M}_{\\mathrm{scheme}}} \\mathfrak{O}^{\\mathrm{scheme}}_{\\mathrm{TFPT}}/\\mathrm{SchGrp}",
        ],
      },
    ],
    keyFormulas: [
      {
        label: "Planck normalization",
        latex: "\\dfrac{\\bar M_{\\mathrm{Pl}}^2}{\\lambda_\\Sigma^2} = \\dfrac{\\rho_\\star}{2\\pi^2}",
      },
      {
        label: "Newton constant",
        latex: "G_N \\lambda_\\Sigma^2 = \\dfrac{\\pi}{4\\rho_\\star}",
      },
    ],
    highlights: [
      {
        label: "Spectral unit",
        value: "λ_Σ",
        description: "First eigenvalue of |B_Σ| — internal length scale",
      },
      {
        label: "Metrology",
        value: "Dimensionless",
        description: "All ratios are scheme-independent quotients",
      },
      {
        label: "Functor chain",
        value: "4 steps",
        description: "T★ → ren → phys → scheme",
      },
    ],
  },
  {
    id: "06",
    number: 6,
    slug: "cosmology",
    title: "Cosmology Interfaces of the TFPT Closed Branch",
    subtitle: "Seam transfer, axion sector, reheating, and CMB targets",
    abstract:
      "Cosmology is not used as a primitive selector of the theory. It is read from the closed branch through seam transfer, determinant-line phase, scalaron sector, axion interface, reheating input, leptogenesis input, neutrino sector, CMB spectra, and conjectural sky-map realization targets.",
    status: "downstream",
    statusLabel: "Downstream interface",
    pdf: "/papers/06_cosmology.pdf",
    inputs: [
      "Papers 1–5 supply the closed branch T★, the carrier packet, the precision branch, the admissible QFT sector, and the boundary-normalized metrology.",
    ],
    contribution: [
      "Downstream cosmology interfaces: Λ_IR, S_Σ, N_DW, axion / reheating / leptogenesis / CMB targets at their proper status levels.",
    ],
    notClaimed: [
      "No carrier proofs, no full α derivation, no QFT closure proof, no SM packet proof.",
    ],
    falsification: [
      "Fails if CMB Stage 2 is sold as a theorem, if a good CMB world is conflated with this observed sky realization, or if cosmology is allowed to tune the primitive branch.",
    ],
    sections: [
      {
        title: "Cosmology as Downstream Interface",
        body: "The closed branch is fixed before cosmology enters. CMB and E8 must never be written as hard theorem claims in this paper. Stage 1 is spectra; Stage 2 is sky realization as a conjectural or programmatic target.",
        formulas: [
          "\\mathfrak{T}_\\star \\Rightarrow (U_\\Sigma, \\det_{\\mathrm{adm}}, \\text{scalaron}, \\text{neutrino sector})\\Rightarrow \\text{cosmology interfaces}",
        ],
      },
      {
        title: "Seam Transfer and Infrared Determinant",
        body: "The seam-transfer expression connects the admissible determinant line to the cosmological constant scale.",
        formulas: [
          "\\Lambda_{\\mathrm{IR}} = \\bar M_{\\mathrm{Pl}}^4 \\!\\left[-\\log\\det_{\\mathrm{adm}}(1 - U_\\Sigma)\\right]",
        ],
      },
      {
        title: "Axion Interface",
        body: "The axion sector depends on seam transfer and determinant-line phase, not on the primitive carrier proof.",
        formulas: [
          "S_\\Sigma = \\log \\mu_\\Sigma(\\alpha_\\star)",
          "N_{\\mathrm{DW}} = 1",
          "\\theta_i = \\pi(1 - \\varphi_{\\mathrm{seam}}(\\alpha_\\star))",
        ],
      },
      {
        title: "CMB — Stage 1 vs. Stage 2",
        body: "Stage 1 is the spectral target: transfer functions, angular spectra, comparison rows. Stage 2 is a conjectural realization target: a good CMB world is not automatically this CMB world.",
      },
    ],
    keyFormulas: [
      {
        label: "Λ_IR (seam transfer)",
        latex:
          "\\Lambda_{\\mathrm{IR}} = \\bar M_{\\mathrm{Pl}}^4 \\!\\left[-\\log\\det_{\\mathrm{adm}}(1 - U_\\Sigma)\\right]",
      },
      {
        label: "Axion interface",
        latex: "N_{\\mathrm{DW}} = 1, \\quad \\theta_i = \\pi(1 - \\varphi_{\\mathrm{seam}}(\\alpha_\\star))",
      },
    ],
    highlights: [
      { label: "N_DW", value: "1", description: "Domain-wall number from the determinant line" },
      {
        label: "Axion ν",
        value: "≈ 15.764 GHz",
        description: "Haloscope window prediction",
      },
      {
        label: "Σ m_ν",
        value: "0.0588 eV",
        description: "Intrinsic neutrino mass sum",
      },
      {
        label: "η_B",
        value: "5.97 × 10⁻¹⁰",
        description: "Baryon asymmetry, leptogenesis interface",
      },
    ],
  },
];
