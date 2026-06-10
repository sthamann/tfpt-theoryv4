export type DependencyClass =
  | "EM closure"
  | "Flavor / residue matrix"
  | "Neutrino transport"
  | "Scale grammar"
  | "Inflation (R²)"
  | "Strong-CP closure"
  | "Horizon / determinant line"
  | "Carrier / Higgs index"
  | "Frontier interface";

/**
 * Status markers follow the TFPT 5.0 ledger grades:
 *   [I] exact identity · [L] Lie/lattice theorem · [N] numerical fixed point
 *   [P] physical/conditional · [A] axiom/open.
 */
export type PredictionStatus =
  | "Exact identity"
  | "Lattice theorem"
  | "Numerical fixed point"
  | "Conditional"
  | "Open / not forced";

/**
 * Whether the linked PDF behind the card exists. Defaults to "available".
 * Every prediction now links to the source document that derives it.
 */
export type LinkStatus = "available" | "forthcoming" | "note" | "soon";

export const LINK_STATUS_META: Record<
  LinkStatus,
  { label: string; tone: string; disabled: boolean }
> = {
  available: {
    label: "Open the source document",
    tone: "text-blue-300 hover:text-blue-200",
    disabled: false,
  },
  note: {
    label: "View standalone note",
    tone: "text-emerald-300 hover:text-emerald-200",
    disabled: false,
  },
  forthcoming: {
    label: "Paper forthcoming",
    tone: "text-amber-300/80 cursor-not-allowed",
    disabled: true,
  },
  soon: {
    label: "Coming soon",
    tone: "text-slate-400 cursor-not-allowed",
    disabled: true,
  },
};

export interface Prediction {
  id: string;
  slug: string;
  title: string;
  shortTitle: string;
  target: string;
  targetLatex: string;
  numericValue: string;
  unit?: string;
  status: PredictionStatus;
  dependencyClass: DependencyClass;
  killTest: string;
  derivationFormulas: string[];
  pdf: string;
  linkStatus?: LinkStatus;
  description: string;
  category:
    | "Coupling"
    | "Flavor"
    | "Neutrino"
    | "QCD/EDM"
    | "Cosmology"
    | "Higgs"
    | "Astrophysics";
}

export const STATUS_BADGE: Record<PredictionStatus, { color: string; bg: string }> = {
  "Exact identity": { color: "text-blue-200", bg: "bg-blue-500/15 ring-blue-400/30" },
  "Lattice theorem": {
    color: "text-cyan-200",
    bg: "bg-cyan-500/15 ring-cyan-400/30",
  },
  "Numerical fixed point": {
    color: "text-emerald-200",
    bg: "bg-emerald-500/15 ring-emerald-400/30",
  },
  Conditional: {
    color: "text-amber-200",
    bg: "bg-amber-500/15 ring-amber-400/30",
  },
  "Open / not forced": {
    color: "text-rose-200",
    bg: "bg-rose-500/15 ring-rose-400/30",
  },
};

export const CATEGORY_META: Record<
  Prediction["category"],
  { label: string; color: string }
> = {
  Coupling: { label: "Couplings & EM", color: "from-blue-500/20 to-cyan-500/20" },
  Flavor: { label: "Flavor / CKM", color: "from-emerald-500/20 to-teal-500/20" },
  Neutrino: { label: "Neutrino sector", color: "from-violet-500/20 to-purple-500/20" },
  "QCD/EDM": { label: "QCD / EDM", color: "from-orange-500/20 to-amber-500/20" },
  Cosmology: { label: "Cosmology / inflation", color: "from-fuchsia-500/20 to-pink-500/20" },
  Higgs: { label: "Higgs sector", color: "from-rose-500/20 to-red-500/20" },
  Astrophysics: {
    label: "Astrophysics / horizon",
    color: "from-indigo-500/20 to-sky-500/20",
  },
};

export const predictions: Prediction[] = [
  {
    id: "alpha-em",
    slug: "alpha-em-closure",
    title: "Fine-Structure Constant — Electromagnetic Fixed Point",
    shortTitle: "α⁻¹(0)",
    target: "α⁻¹(0) = 137.035 999 216 8…",
    targetLatex: "\\alpha^{-1}(0) = 137.035\\,999\\,216\\,8\\ldots",
    numericValue: "137.035999216",
    status: "Numerical fixed point",
    dependencyClass: "EM closure",
    killTest:
      "Failure of the unique-root equation F_U(1)(α) = 0, a second admissible root, or a stable mismatch outside the stated interface uncertainty.",
    derivationFormulas: [
      "F_{U(1)}(\\alpha) = \\alpha^3 - 2c_3^3\\alpha^2 - \\tfrac{4}{5}c_3^6\\Big(\\textstyle\\sum_{f,j}L_{f,j} + N_\\Phi\\Big)\\log\\tfrac{1}{\\varphi_{\\mathrm{seam}}(\\alpha)} = 0",
      "\\textstyle\\sum_{f,j}L_{f,j} + N_\\Phi = 41 = 10\\,b_1",
      "\\alpha^{-1} = 137.035\\,999\\,216\\,8\\ldots",
    ],
    pdf: "/papers/tfpt_1_architecture_e8.pdf",
    description:
      "The fine-structure constant is the unique positive root of the cubic closure built from c₃ and the abelian coefficient 41 = 10 b₁. Existence and uniqueness are proved; the value lands 2.9×10⁻¹⁰ (1.9σ) from CODATA-2022. Typed [N]: the coefficients are exact identities, the Ward-origin reading of the equation is conditional [P] (ledger EM.FP.01).",
    category: "Coupling",
  },
  {
    id: "lambda-c",
    slug: "cabibbo-angle",
    title: "Cabibbo Angle — Retained Seed",
    shortTitle: "λ_C",
    target: "λ_C = 0.22438",
    targetLatex: "\\lambda_C = \\sqrt{\\varphi_0(1-\\varphi_0)} = 0.22438",
    numericValue: "0.22438",
    status: "Exact identity",
    dependencyClass: "Flavor / residue matrix",
    killTest: "Stable CKM global-fit mismatch after the declared comparison map.",
    derivationFormulas: [
      "\\varphi_0 = \\frac{1}{6\\pi} + \\frac{3}{256\\pi^4}",
      "\\lambda_C = \\sqrt{\\varphi_0(1-\\varphi_0)} = 0.22438",
    ],
    pdf: "/papers/tfpt_2_standard_model.pdf",
    description:
      "The Cabibbo angle is the carrier base of the φ₀-ladder — the same seed that fixes the reactor angle and the birefringence amplitude.",
    category: "Flavor",
  },
  {
    id: "flavor-invariants",
    slug: "flavor-invariants",
    title: "Flavor Residue Invariants",
    shortTitle: "det R, χ_R",
    target: "det R = 8, minors (2,3,5), χ_R = t³ − 9t² + 10t − 8",
    targetLatex: "\\det R = 8,\\ \\ \\mathrm{minors}=(2,3,5),\\ \\ \\chi_R = t^3 - 9t^2 + 10t - 8",
    numericValue: "8",
    status: "Exact identity",
    dependencyClass: "Flavor / residue matrix",
    killTest:
      "A future CKM/PMNS global fit that cannot be carried by a residue matrix with det 8, principal minors (2,3,5) and this characteristic polynomial.",
    derivationFormulas: [
      "R = \\begin{pmatrix} 1 & 3 & 0 \\\\ 1 & 5 & 2 \\\\ 2 & 5 & 3 \\end{pmatrix}",
      "\\det R = 8 = h(D_5), \\quad \\|R\\|_F^2 = 78 = \\dim E_6",
      "\\chi_R(t) = t^3 - 9t^2 + 10t - 8",
    ],
    pdf: "/papers/tfpt_2_standard_model.pdf",
    description:
      "The flavor matrix carries only compiler numbers: determinant h(D₅) = 8, principal 2-minors (2,3,5) with product h(E₈) = 30, trace N_fam². Any future global fit must satisfy these.",
    category: "Flavor",
  },
  {
    id: "koide",
    slug: "koide-relation",
    title: "Koide Relation — Near 2/3",
    shortTitle: "Q_Koide",
    target: "Q = 0.664 (target 2/3 = |ℤ₂|/N_fam)",
    targetLatex: "Q = 0.664 \\;\\to\\; Q_\\star = \\tfrac{2}{3} = \\tfrac{|\\mathbb{Z}_2|}{N_{\\mathrm{fam}}}",
    numericValue: "0.664",
    status: "Conditional",
    dependencyClass: "Frontier interface",
    killTest:
      "A source→pole transfer that lands far from 2/3, or a demonstration that the lepton φ₀-ladder is incompatible with the measured charged-lepton masses.",
    derivationFormulas: [
      "Q_{\\mathrm{TFPT}} = \\frac{\\sum_\\ell \\hat m_\\ell}{(\\sum_\\ell \\sqrt{\\hat m_\\ell})^2} = 0.66446\\ldots",
      "Q_\\star = \\frac{|\\mathbb{Z}_2|}{N_{\\mathrm{fam}}} = \\frac{2}{3}",
    ],
    pdf: "/papers/tfpt_4_frontier.pdf",
    description:
      "The source-level Koide quotient is 0.664, 0.33% below the democratic compiler target 2/3. Near-miss, not an exact derivation — the source→pole transfer is a conjecture.",
    category: "Flavor",
  },
  {
    id: "theta12",
    slug: "solar-angle",
    title: "Solar Angle — Seam Misalignment",
    shortTitle: "sin²θ₁₂",
    target: "sin²θ₁₂ = 1/3 − φ₀/2 = 0.3067",
    targetLatex: "\\sin^2\\theta_{12} = \\tfrac{1}{3} - \\tfrac{\\varphi_0}{2} = 0.3067",
    numericValue: "0.3067",
    status: "Numerical fixed point",
    dependencyClass: "Neutrino transport",
    killTest:
      "A JUNO central value clearly away from 0.307 at high significance kills the seam-misalignment mechanism.",
    derivationFormulas: [
      "\\varepsilon = q(A_3)\\,\\varphi_0 = \\tfrac{3}{4}\\varphi_0",
      "\\sin^2\\theta_{12} = \\tfrac{1}{3} - \\tfrac{2}{3}\\varepsilon = \\tfrac{1}{3} - \\tfrac{\\varphi_0}{2} = 0.3067",
    ],
    pdf: "/papers/tfpt_2_standard_model.pdf",
    description:
      "Previously the only open SM angle. Tri-bimaximal 1/3 plus the seam misalignment ε = (3/4)φ₀ gives 0.306747 — 0.1% from NuFIT 6.0. The value is the frozen prediction of record (blind registry predictions_frozen.json, 2026-06-09, machine-enforced by v84): exactly one θ₁₂ number is committed before JUNO, the seam/non-linear variants are typed as derived variants, never as alternatives.",
    category: "Neutrino",
  },
  {
    id: "theta13",
    slug: "reactor-angle",
    title: "Reactor Angle — Seed × Carrier Trace",
    shortTitle: "sin²θ₁₃",
    target: "sin²θ₁₃ = φ₀ e^(−5/6) = 0.0231",
    targetLatex: "\\sin^2\\theta_{13} = \\varphi_0\\,e^{-5/6} = 0.0231",
    numericValue: "0.0231",
    status: "Exact identity",
    dependencyClass: "Neutrino transport",
    killTest: "Robust normal-ordering global-fit exclusion at the stated confidence level.",
    derivationFormulas: [
      "\\sin^2\\theta_{13} = \\varphi_0\\,e^{-5/6}",
      "\\varphi_0 = \\frac{1}{6\\pi} + \\frac{3}{256\\pi^4}",
      "\\sin^2\\theta_{13} = 0.0231",
    ],
    pdf: "/papers/tfpt_2_standard_model.pdf",
    description:
      "The reactor angle is the seed times the carrier-trace factor e⁻⁵ᐟ⁶ (γ = 5/6). Daya Bay / RENO / JUNO compare; PDG 0.0220.",
    category: "Neutrino",
  },
  {
    id: "theta23",
    slug: "atmospheric-octant",
    title: "Atmospheric Angle — μτ-Symmetric Limit",
    shortTitle: "sin²θ₂₃",
    target: "sin²θ₂₃ ≈ 1/2 (octant not selected)",
    targetLatex: "\\sin^2\\theta_{23} \\approx \\tfrac{1}{2}",
    numericValue: "0.5",
    status: "Conditional",
    dependencyClass: "Neutrino transport",
    killTest: "A robust off-maximal octant determination by NOvA / T2K / DUNE.",
    derivationFormulas: [
      "\\theta_{23} = 45^\\circ \\quad (\\mu\\tau\\text{-symmetric limit})",
      "\\delta_{\\mathrm{CP}} = \\tfrac{4\\pi}{3} = 240^\\circ",
    ],
    pdf: "/papers/tfpt_2_standard_model.pdf",
    description:
      "The atmospheric angle is near-maximal in the μτ-symmetric limit; the octant is not selected by the present transport. DUNE addresses the ambiguity.",
    category: "Neutrino",
  },
  {
    id: "neutrino-ordering",
    slug: "neutrino-ordering",
    title: "Mass Ordering & Majorana Branch",
    shortTitle: "NO, m_ββ",
    target: "Normal ordering, small m_ββ",
    targetLatex: "\\text{normal ordering}, \\quad m_{\\beta\\beta}\\ \\text{small}",
    numericValue: "0",
    status: "Conditional",
    dependencyClass: "Neutrino transport",
    killTest:
      "Inverted ordering, or a large m_ββ detection, kills the Majorana branch.",
    derivationFormulas: [
      "\\text{normal ordering preferred}",
      "\\delta_{\\mathrm{CP}} = 240^\\circ",
    ],
    pdf: "/papers/tfpt_2_standard_model.pdf",
    description:
      "The Majorana neutrino sector prefers normal ordering with a small effective mass. LEGEND / nEXO / DUNE / KATRIN are the comparison surface.",
    category: "Neutrino",
  },
  {
    id: "strong-cp",
    slug: "strong-cp-edm-null",
    title: "Strong CP — Neutron-EDM Null",
    shortTitle: "θ_eff = 0",
    target: "θ_eff = 0 (structural null)",
    targetLatex: "\\theta_{\\mathrm{eff}} = 0",
    numericValue: "0",
    status: "Exact identity",
    dependencyClass: "Strong-CP closure",
    killTest: "A solid neutron-EDM signal above the SM background falsifies the structural cancellation.",
    derivationFormulas: [
      "\\arg\\det M_u = \\arg\\det M_d = 0",
      "\\theta_{\\mathrm{eff}} = 0",
    ],
    pdf: "/papers/tfpt_2_standard_model.pdf",
    description:
      "θ_eff = 0 follows from three structural facts (γ₅-Hermiticity, polar structure, sheet involution) plus reflection positivity — without a mass gap. PSI nEDM / SNS test it.",
    category: "QCD/EDM",
  },
  {
    id: "mpme",
    slug: "proton-electron-ratio",
    title: "Proton/Electron Ratio — Not a Compiler Power",
    shortTitle: "m_p/m_e",
    target: "m_p/m_e = 1836.15 (explicitly not claimed)",
    targetLatex: "\\frac{m_p}{m_e} = 1836.15",
    numericValue: "1836.15",
    status: "Open / not forced",
    dependencyClass: "Frontier interface",
    killTest:
      "Only fails if mis-asserted as a compiler power; there is no clean φ₀ power for the QCD-confinement / EW-Yukawa ratio.",
    derivationFormulas: [
      "\\frac{m_p}{m_e} = \\frac{\\text{QCD confinement scale}}{\\text{EW electron Yukawa}}",
      "1/(\\varphi_0)^2 = 353.7, \\quad 1/(\\varphi_0)^3 = 6651 \\;\\text{bracket}\\; 1836",
    ],
    pdf: "/papers/tfpt_4_frontier.pdf",
    description:
      "Listed for honesty: m_p/m_e is a cross-sector ratio, computable at scheme level but genuinely not a compiler power. It is deliberately not forced onto the ladder.",
    category: "QCD/EDM",
  },
  {
    id: "ns",
    slug: "spectral-tilt",
    title: "Scalar Tilt — R² Attractor",
    shortTitle: "n_s",
    target: "n_s = 1 − 2/N★ ∈ [0.960, 0.967] (frozen band)",
    targetLatex: "n_s = 1 - \\tfrac{2}{N_\\star} \\in [0.960,\\,0.967]",
    numericValue: "0.965",
    status: "Conditional",
    dependencyClass: "Inflation (R²)",
    killTest: "A robust n_s far from the Starobinsky line on the same R² attractor (n_s ≥ 0.967 also kills the scalaron-reheating chain).",
    derivationFormulas: [
      "n_s = 1 - \\tfrac{2}{N_\\star}, \\qquad N_\\star \\in [50, 60]\\ \\text{(frozen band)}",
      "N_\\star^{\\mathrm{reheating}} = 51.4 \\ \\Rightarrow\\ n_s = 0.9611 \\ \\text{[P, conditional]}",
    ],
    pdf: "/papers/tfpt_1_architecture_e8.pdf",
    description:
      "The scalar tilt comes from the same R² (Starobinsky) attractor that fixes the scalaron mass. The frozen registry keeps n_s as a band over N★ ∈ [50,60]; the scalaron-reheating chain (v86, Higgs channel) sharpens it conditionally to N★ = 51.4 ⇒ n_s = 0.9611 — recorded with its tensions (+0.9σ below Planck; the same chain underpredicts A_s, so the point is conditional on the decay channel).",
    category: "Cosmology",
  },
  {
    id: "r-tensor",
    slug: "tensor-ratio",
    title: "Tensor-to-Scalar Ratio — R² Branch",
    shortTitle: "r",
    target: "r = 12/N★² ∈ [0.0033, 0.0048] (frozen band)",
    targetLatex: "r = \\tfrac{12}{N_\\star^2} \\in [0.0033,\\,0.0048]",
    numericValue: "0.0040",
    status: "Conditional",
    dependencyClass: "Inflation (R²)",
    killTest: "Any robust r ≳ 0.01 kills the R² branch carrying M_Pl and A_s.",
    derivationFormulas: [
      "r = \\tfrac{12}{N_\\star^2} \\in [0.0033,\\,0.0048], \\qquad N_\\star \\in [50, 60]",
      "N_\\star^{\\mathrm{reheating}} = 51.4 \\ \\Rightarrow\\ r = 0.0045 \\ \\text{[P, conditional]}",
      "\\text{current bound } r < 0.036\\ (\\text{BICEP/Keck BK18})",
    ],
    pdf: "/papers/tfpt_1_architecture_e8.pdf",
    description:
      "The tensor ratio of the R² scalaron is already below the current bound and within reach of CMB-S4 (σ_r ≤ 5×10⁻⁴, ~2033). The frozen registry keeps r as a band; the scalaron-reheating chain (v86) sharpens it conditionally to r = 0.0045.",
    category: "Cosmology",
  },
  {
    id: "as-amplitude",
    slug: "scalar-amplitude",
    title: "Scalar Amplitude — Parameter-Free",
    shortTitle: "A_s",
    target: "A_s = N★² c₃⁷/(24π²) ≈ 2.0×10⁻⁹",
    targetLatex: "A_s = \\frac{N_\\star^2}{24\\pi^2}\\,c_3^7 \\approx 2.0\\times 10^{-9}",
    numericValue: "2.0e-9",
    status: "Conditional",
    dependencyClass: "Inflation (R²)",
    killTest: "A_s incompatible with the seam-fixed scalaron mass on the R² branch.",
    derivationFormulas: [
      "A_s = \\frac{N_\\star^2}{24\\pi^2}\\,c_3^7 \\approx 2.0\\times 10^{-9}",
      "\\text{Planck } \\simeq 2.1\\times 10^{-9}",
    ],
    pdf: "/papers/tfpt_1_architecture_e8.pdf",
    description:
      "Generic Starobinsky fits the scalaron mass to A_s; TFPT fixes it by the seam, (M/M̄)² = c₃⁷, so A_s becomes a prediction — the measured A_s prefers N★ = 56.2. Honest record (v86): the slow Higgs-channel reheating point N★ = 51.4 underpredicts A_s by 11σ, so the measured A_s requires near-instantaneous reheating; A_s arbitrates the reheating speed.",
    category: "Cosmology",
  },
  {
    id: "scalaron",
    slug: "scalaron-mass",
    title: "Scalaron Mass — Seam Power",
    shortTitle: "M_scal",
    target: "M = c₃^(7/2) M̄ = 3.06×10¹³ GeV",
    targetLatex: "M_{\\mathrm{scal}} = c_3^{7/2}\\,\\bar M_{\\mathrm{Pl}} = 3.06\\times 10^{13}\\,\\text{GeV}",
    numericValue: "3.06e13",
    unit: "GeV",
    status: "Numerical fixed point",
    dependencyClass: "Inflation (R²)",
    killTest: "A scalaron mass incompatible with the seam power c₃⁷ = c₃^(Ω_adm − 10 b₁).",
    derivationFormulas: [
      "\\frac{M_{\\mathrm{scal}}^2}{\\bar M_{\\mathrm{Pl}}^2} = c_3^{\\,\\Omega_{\\mathrm{adm}} - 10 b_1} = c_3^7",
      "M_{\\mathrm{scal}} = 3.06\\times 10^{13}\\,\\text{GeV}",
    ],
    pdf: "/papers/tfpt_1_architecture_e8.pdf",
    description:
      "The scalaron mass comes out exactly at the canonical Starobinsky value, with the exponent 7 = 48 − 41 = Ω_adm − 10 b₁ fixed by the seam. A former input is now an output.",
    category: "Cosmology",
  },
  {
    id: "omega-b",
    slug: "baryon-density",
    title: "Baryon Density — One-Engine Readout",
    shortTitle: "Ω_b",
    target: "Ω_b = (4π − 1)β_rad = 0.04894",
    targetLatex: "\\Omega_b = (4\\pi - 1)\\beta_{\\mathrm{rad}} = 0.04894",
    numericValue: "0.04894",
    status: "Conditional",
    dependencyClass: "Scale grammar",
    killTest: "Robust inconsistency under the declared Planck comparison convention.",
    derivationFormulas: [
      "\\Omega_b = (4\\pi - 1)\\,\\beta_{\\mathrm{rad}} = 0.04894",
      "\\Omega_b h^2 = 0.0222",
    ],
    pdf: "/papers/tfpt_4_frontier.pdf",
    description:
      "The baryon fraction reads off the determinant-line angle β_rad. Planck comparison row 0.04930.",
    category: "Cosmology",
  },
  {
    id: "eta-b",
    slug: "baryon-asymmetry",
    title: "Baryon Asymmetry — Downstream Readout",
    shortTitle: "η_B",
    target: "η_B = 6.1×10⁻¹⁰",
    targetLatex: "\\eta_B = 6.1\\times 10^{-10}",
    numericValue: "6.1e-10",
    status: "Conditional",
    dependencyClass: "Frontier interface",
    killTest:
      "Robust exclusion of the quoted value under the declared cosmological pipeline (as a compiler power it is explicitly not closed).",
    derivationFormulas: [
      "\\Omega_b h^2 = 0.0222",
      "\\eta_B = 273.9\\times 10^{-10}\\,\\Omega_b h^2 = 6.09\\times 10^{-10}",
    ],
    pdf: "/papers/tfpt_4_frontier.pdf",
    description:
      "A downstream cosmological readout from the closed Ω_b h² (observed 6.1×10⁻¹⁰). As a fundamental compiler power it is not closed — the leptogenesis Boltzmann solve is an interface.",
    category: "Cosmology",
  },
  {
    id: "hubble",
    slug: "hubble-lambda",
    title: "H₀ vs Λ — One Exponential Engine",
    shortTitle: "H₀ ∼ √Λ",
    target: "v_EW ∼ e^(−α⁻¹/5), Λ ∼ e^(−2α⁻¹), H₀ ∼ √Λ",
    targetLatex: "v_{\\mathrm{EW}} \\sim e^{-\\alpha^{-1}/5},\\ \\ \\Lambda \\sim e^{-2\\alpha^{-1}},\\ \\ H_0 \\sim \\sqrt{\\Lambda}",
    numericValue: "0",
    status: "Conditional",
    dependencyClass: "Scale grammar",
    killTest: "A robust w ≠ −1 kills the single-engine dark-energy readout.",
    derivationFormulas: [
      "A_{\\mathrm{EW}} : A_H : A_\\Lambda = 1 : 5 : 10",
      "\\frac{\\rho_\\Lambda}{\\bar M_{\\mathrm{Pl}}^4} = \\frac{3}{4\\pi^2}\\,e^{-2\\alpha^{-1}}",
    ],
    pdf: "/papers/tfpt_1_architecture_e8.pdf",
    description:
      "The electroweak scale, the cosmological constant and the Hubble scale are all powers of one exponential engine on the carrier — the same α⁻¹ ≈ 137. SH0ES / DESI / Planck (Hubble tension) test it.",
    category: "Cosmology",
  },
  {
    id: "no-second-higgs",
    slug: "no-second-higgs",
    title: "No Second Light Higgs Doublet",
    shortTitle: "N_Φ = 1",
    target: "exactly one seam-even light doublet",
    targetLatex: "N_\\Phi = 1",
    numericValue: "1",
    status: "Exact identity",
    dependencyClass: "Carrier / Higgs index",
    killTest: "Robust discovery of a second light seam-even Higgs doublet.",
    derivationFormulas: [
      "10\\,b_1 = 41 = \\textstyle\\sum_{f,j}L_{f,j} + N_\\Phi",
      "N_\\Phi = g_{\\mathrm{car}} - |\\mu_4| = 1",
    ],
    pdf: "/papers/tfpt_1_architecture_e8.pdf",
    description:
      "The carrier index fixes exactly one weak doublet (N_Φ = g_car − |μ₄| = 1). A structural prohibition, not a fit.",
    category: "Higgs",
  },
  {
    id: "birefringence",
    slug: "cosmic-birefringence",
    title: "Cosmic Birefringence — Determinant Line",
    shortTitle: "β_rad",
    target: "β_rad = φ₀/(4π) = 0.2424°",
    targetLatex: "\\beta_{\\mathrm{rad}} = \\frac{\\varphi_0}{4\\pi} = 0.2424^\\circ",
    numericValue: "0.2424",
    unit: "°",
    status: "Numerical fixed point",
    dependencyClass: "Horizon / determinant line",
    killTest: "An externally calibrated β = 0 within tight error.",
    derivationFormulas: [
      "\\beta_{\\mathrm{rad}} = \\frac{\\varphi_0}{4\\pi} = 0.2424^\\circ",
      "\\text{ACT DR6: } 0.215^\\circ \\pm 0.074^\\circ\\ (0.4\\sigma)",
    ],
    pdf: "/papers/tfpt_horizon_readouts.pdf",
    description:
      "The determinant-line / Chern–Simons response of the seam. ACT DR6 measures 0.215° ± 0.074° — within 0.4σ of the TFPT value.",
    category: "Astrophysics",
  },
  {
    id: "axion",
    slug: "axion-dark-matter",
    title: "Axion Dark Matter — Candidate Fixed",
    shortTitle: "m_a",
    target: "m_a ≈ 23.8 µeV, f_a = M_scal/128",
    targetLatex: "m_a \\approx 23.8\\,\\mu\\text{eV}, \\quad f_a = \\frac{M_{\\mathrm{scal}}}{128} \\approx 2.39\\times 10^{11}\\,\\text{GeV}",
    numericValue: "23.8",
    unit: "µeV",
    status: "Conditional",
    dependencyClass: "Frontier interface",
    killTest:
      "Exclusion of the determinant-line axion window at the coupled sensitivity (relic abundance is scenario-sensitive, not closed).",
    derivationFormulas: [
      "\\theta_i = \\pi(1 - \\varphi_{\\mathrm{seam}}(\\alpha_\\star)) = 170.4^\\circ",
      "f_a = \\frac{M_{\\mathrm{scal}}}{2\\dim S^+|\\mu_4|} = \\frac{M_{\\mathrm{scal}}}{128}, \\quad m_a \\approx 23.8\\,\\mu\\text{eV}",
    ],
    pdf: "/papers/tfpt_4_frontier.pdf",
    description:
      "The candidate is the determinant-line axion of the strong-CP sector (WIMPs ruled out — no spare E₈ singlet). The misalignment angle is closed; f_a = M_scal/128 is a conjecture.",
    category: "Astrophysics",
  },
];

/** Ledger claim IDs per prediction (mirror of the status-ledger row keys). */
export const CLAIM_ID: Record<string, string> = {
  "alpha-em": "EM.FP.01",
  "lambda-c": "FLAV.CKM.01",
  "flavor-invariants": "FLAV.R.01",
  koide: "FR.KOIDE.01",
  theta12: "FLAV.TH12.01",
  theta13: "REG.FREEZE.01",
  theta23: "REG.FREEZE.01",
  "neutrino-ordering": "PRED.LAYER.01",
  "strong-cp": "PRED.LAYER.01",
  mpme: "FR.MPME.01",
  ns: "COSMO.INF.01",
  "r-tensor": "COSMO.INF.01",
  "as-amplitude": "COSMO.INF.01",
  scalaron: "GRAV.SCAL.01",
  "omega-b": "COSMO.OMB.01",
  "eta-b": "FR.ETAB.01",
  hubble: "COSMO.LAM.01",
  "no-second-higgs": "EM.BUDGET.01",
  birefringence: "HOR.01",
  axion: "FR.DM.01",
};

/** Compact status marker per prediction status grade. */
export const STATUS_MARKER: Record<PredictionStatus, string> = {
  "Exact identity": "[I]",
  "Lattice theorem": "[L]",
  "Numerical fixed point": "[N]",
  Conditional: "[P]",
  "Open / not forced": "[A]",
};

/** Status × testability reading guide shown at the top of the surface. */
export const TEST_SURFACE_GROUPS: {
  label: string;
  tone: string;
  items: string[];
}[] = [
  {
    label: "Closed numerical tests",
    tone: "border-emerald-400/25 bg-emerald-500/5 text-emerald-200",
    items: ["α⁻¹", "sin²θ₁₂", "sin²θ₁₃", "λ_C", "β_rad", "det R / minors"],
  },
  {
    label: "Structural kill tests",
    tone: "border-blue-400/25 bg-blue-500/5 text-blue-200",
    items: ["no 2nd Higgs (N_Φ=1)", "neutron EDM (θ_eff=0)", "no 4th generation"],
  },
  {
    label: "Conditional cosmology tests",
    tone: "border-amber-400/25 bg-amber-500/5 text-amber-200",
    items: ["r", "n_s", "A_s", "Ω_b", "η_B", "w ≠ −1"],
  },
  {
    label: "Honest non-claims",
    tone: "border-rose-400/25 bg-rose-500/5 text-rose-200",
    items: ["m_p/m_e", "exact Koide", "axion relic abundance"],
  },
];
