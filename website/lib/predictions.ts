export type DependencyClass =
  | "EM closure"
  | "Flavor readout"
  | "Neutrino closure"
  | "Determinant response"
  | "Determinant response (local)"
  | "Strong-CP closure"
  | "Carrier / Higgs index"
  | "Cosmology readout"
  | "Hadronic readout"
  | "Scheme projection";

export type PredictionStatus =
  | "Theorem-level null"
  | "Physical observable"
  | "Comparison quantity"
  | "Cosmology comparison"
  | "Scheme projection"
  | "Kill test"
  | "Out-of-sample check";

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
  "Theorem-level null": { color: "text-blue-200", bg: "bg-blue-500/15 ring-blue-400/30" },
  "Physical observable": {
    color: "text-emerald-200",
    bg: "bg-emerald-500/15 ring-emerald-400/30",
  },
  "Comparison quantity": {
    color: "text-amber-200",
    bg: "bg-amber-500/15 ring-amber-400/30",
  },
  "Cosmology comparison": {
    color: "text-fuchsia-200",
    bg: "bg-fuchsia-500/15 ring-fuchsia-400/30",
  },
  "Scheme projection": { color: "text-sky-200", bg: "bg-sky-500/15 ring-sky-400/30" },
  "Kill test": { color: "text-rose-200", bg: "bg-rose-500/15 ring-rose-400/30" },
  "Out-of-sample check": {
    color: "text-violet-200",
    bg: "bg-violet-500/15 ring-violet-400/30",
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
  Cosmology: { label: "Cosmology", color: "from-fuchsia-500/20 to-pink-500/20" },
  Higgs: { label: "Higgs sector", color: "from-rose-500/20 to-red-500/20" },
  Astrophysics: {
    label: "Astrophysics / Horizon",
    color: "from-indigo-500/20 to-sky-500/20",
  },
};

export const predictions: Prediction[] = [
  {
    id: "alpha-em",
    slug: "alpha-em-closure",
    title: "Exact Electromagnetic Closure — Fine-Structure Constant",
    shortTitle: "α⁻¹(0)",
    target: "α⁻¹(0) = 137.035 999 216 8…",
    targetLatex: "\\alpha^{-1}(0) = 137.035\\,999\\,216\\,8\\ldots",
    numericValue: "137.035999216",
    status: "Physical observable",
    dependencyClass: "EM closure",
    killTest:
      "Failure of the self-consistent root equation or a stable precision mismatch outside the stated interface uncertainty.",
    derivationFormulas: [
      "\\varphi_{\\mathrm{seam}}(\\alpha) = \\frac{1}{6\\pi} + \\frac{3 e^{-2\\alpha}}{256\\pi^4}\\!\\left(1-\\frac{3 e^{-2\\alpha}}{256\\pi^4}\\right)^{-5/4}",
      "F_{U(1)}(\\alpha) = \\alpha^3 - 2 c_3^3 \\alpha^2 - \\tfrac{4}{5} c_3^6 \\!\\left(\\textstyle\\sum_{f,j} L_{f,j}^{\\mathrm{diag}} + N_\\Phi\\right) \\log \\!\\left(\\varphi_{\\mathrm{seam}}(\\alpha)^{-1}\\right)",
      "F_{U(1)}(\\alpha_\\star) = 0 \\Rightarrow \\alpha_\\star^{-1} = 137.035\\,999\\,216\\,8\\ldots",
    ],
    pdf: "/predictions/tfpt_prediction_alpha_em_closure.pdf",
    description:
      "The fine-structure constant emerges as the unique positive root of the carrier-form electromagnetic closure equation with the exact seam generating function — not as a fit.",
    category: "Coupling",
  },
  {
    id: "alpha-mz",
    slug: "alpha-mz-scheme",
    title: "Running α at the Z-Pole",
    shortTitle: "α̅⁽⁵⁾(M_Z)⁻¹",
    target: "α̅⁽⁵⁾(M_Z)⁻¹ = 127.9405",
    targetLatex: "\\bar\\alpha^{(5)}(M_Z)^{-1} = 127.9405",
    numericValue: "127.9405",
    status: "Scheme projection",
    dependencyClass: "Scheme projection",
    killTest:
      "Persistent mismatch after declared Standard-Model threshold map.",
    derivationFormulas: [
      "\\alpha^{-1}(0) = 137.035\\,999\\,216\\,8\\ldots",
      "\\bar\\alpha^{(5)}(M_Z)^{-1} = \\mathcal{R}_{\\mathrm{SM}}[\\alpha(0)] = 127.9405",
    ],
    pdf: "/predictions/tfpt_prediction_alpha_mz_scheme.pdf",
    description:
      "Scheme projection of α(0) through the declared Standard-Model threshold map. Not an independently fitted observable.",
    category: "Coupling",
  },
  {
    id: "lambda-c",
    slug: "lambda-c-cabibbo",
    title: "Cabibbo Angle — Retained Flavor Branch",
    shortTitle: "λ_C",
    target: "λ_C = 0.22438",
    targetLatex: "\\lambda_C = 0.22438",
    numericValue: "0.22438",
    status: "Physical observable",
    dependencyClass: "Flavor readout",
    killTest: "Stable CKM global-fit mismatch after the declared comparison map.",
    derivationFormulas: [
      "\\varphi_0 = \\frac{1}{6\\pi} + \\frac{3}{256\\pi^4}",
      "\\lambda_C = \\sqrt{\\varphi_0(1-\\varphi_0)} = 0.22438",
      "\\varphi_0 = \\frac{1 - \\sqrt{1 - 4\\lambda_C^2}}{2}",
    ],
    pdf: "/predictions/tfpt_prediction_lambda_c_cabibbo.pdf",
    description:
      "Physical observable from the hard holonomy closure on the rigid flavor branch, with the retained UV identity as a compact shadow.",
    category: "Flavor",
  },
  {
    id: "ckm-phase",
    slug: "ckm-phase",
    title: "CKM Phase — Holonomy Transport",
    shortTitle: "δ_CKM",
    target: "δ_CKM = 1.198 rad",
    targetLatex: "\\delta_{\\mathrm{CKM}} = 1.198\\,\\text{rad}",
    numericValue: "1.198",
    unit: "rad",
    status: "Comparison quantity",
    dependencyClass: "Flavor readout",
    killTest: "Stable global-flavor-fit exclusion at ≥ 3σ.",
    derivationFormulas: [
      "V_{\\mathrm{CKM}} = U_{u,L}^\\dagger U_{d,L}",
      "\\delta_{\\mathrm{CKM}} = 1.198\\,\\text{rad}",
    ],
    pdf: "/predictions/tfpt_prediction_ckm_phase.pdf",
    description:
      "CKM phase from exact holonomy transport on the rigid branch, not from an adjustable CP dial.",
    category: "Flavor",
  },
  {
    id: "rare-kaons",
    slug: "rare-kaons",
    title: "Rare-Kaon Corridor",
    shortTitle: "K → π ν ν̄",
    target: "BR(K⁺) = 9.40·10⁻¹¹, BR(K_L) = 3.47·10⁻¹¹",
    targetLatex:
      "\\mathrm{BR}(K^+\\!\\to\\pi^+\\nu\\bar\\nu) = 9.40\\!\\times\\!10^{-11}",
    numericValue: "9.40e-11 / 3.47e-11",
    status: "Comparison quantity",
    dependencyClass: "Flavor readout",
    killTest:
      "K⁺ outside [7,12]·10⁻¹¹ or incompatible Grossman–Nir-plane correlation.",
    derivationFormulas: [
      "\\mathrm{BR}(K^+\\!\\to\\pi^+\\nu\\bar\\nu) = 9.40\\!\\times\\!10^{-11}",
      "\\mathrm{BR}(K_L\\!\\to\\pi^0\\nu\\bar\\nu) = 3.47\\!\\times\\!10^{-11}",
    ],
    pdf: "/predictions/tfpt_prediction_rare_kaons.pdf",
    description:
      "The closed CKM point feeds into rare-kaon short-distance amplitudes, with NA62/KOTO as the comparison surface.",
    category: "Flavor",
  },
  {
    id: "theta13",
    slug: "theta13-neutrino",
    title: "Reactor Angle — Neutrino Closure",
    shortTitle: "sin²θ₁₃",
    target: "sin²θ₁₃ = 0.02311",
    targetLatex: "\\sin^2\\theta_{13} = 0.02311",
    numericValue: "0.02311",
    status: "Physical observable",
    dependencyClass: "Neutrino closure",
    killTest: "Robust normal-ordering global-fit exclusion at the stated confidence level.",
    derivationFormulas: [
      "\\sin^2\\theta_{13} = \\varphi_0 e^{-\\gamma}",
      "\\varphi_0 = \\frac{1}{6\\pi} + \\frac{3}{256\\pi^4}, \\quad \\gamma = \\tfrac{5}{6}",
      "\\sin^2\\theta_{13} = 0.02311",
    ],
    pdf: "/predictions/tfpt_prediction_theta13_neutrino.pdf",
    description:
      "PMNS reactor angle from neutrino closure on the closed branch, with the seed expression as a compact UV shadow.",
    category: "Neutrino",
  },
  {
    id: "pmns",
    slug: "pmns-phase-octant",
    title: "PMNS Phase and Atmospheric Octant",
    shortTitle: "δ_CP, sin²θ₂₃",
    target: "δ_CP = 240°, sin²θ₂₃ = 0.4557",
    targetLatex: "\\delta_{\\mathrm{CP}} = 240^\\circ, \\quad \\sin^2\\theta_{23} = 0.4557",
    numericValue: "240° / 0.4557",
    status: "Comparison quantity",
    dependencyClass: "Neutrino closure",
    killTest: "Exclusion of 240° or lower octant at ≥ 3σ.",
    derivationFormulas: [
      "U_{\\mathrm{PMNS}} = U_{e,L}^\\dagger U_{\\nu,L}",
      "\\delta_{\\mathrm{CP}} = 240^\\circ, \\quad \\sin^2\\theta_{23} = 0.4557",
    ],
    pdf: "/predictions/tfpt_prediction_pmns_phase_octant.pdf",
    description:
      "The Majorana neutrino sector is generated by the same admissible transport grammar that fixes the PMNS matrix and mass sum.",
    category: "Neutrino",
  },
  {
    id: "neutrino-sum",
    slug: "neutrino-sum",
    title: "Neutrino Mass Sum — Closed Branch",
    shortTitle: "Σ m_ν",
    target: "Σ m_ν = 5.876·10⁻² eV",
    targetLatex: "\\Sigma m_\\nu = 5.876\\!\\times\\!10^{-2}\\,\\text{eV}",
    numericValue: "0.05876",
    unit: "eV",
    status: "Physical observable",
    dependencyClass: "Neutrino closure",
    killTest: "Robust cosmological upper bound below the branch value.",
    derivationFormulas: [
      "m_{\\nu_1} = 0",
      "m_{\\nu_2} = 8.614\\!\\times\\!10^{-3}\\,\\text{eV}",
      "m_{\\nu_3} = 5.015\\!\\times\\!10^{-2}\\,\\text{eV}",
      "\\Sigma m_\\nu = 5.876\\!\\times\\!10^{-2}\\,\\text{eV}",
    ],
    pdf: "/predictions/tfpt_prediction_neutrino_sum.pdf",
    description:
      "Intrinsic normal-ordering mass-sum output of the closed neutrino branch — no external oscillation inversion is used as primitive input.",
    category: "Neutrino",
  },
  {
    id: "0vbb",
    slug: "neutrinoless-double-beta",
    title: "Neutrinoless Double-Beta — Majorana Branch",
    shortTitle: "m_ββ",
    target: "m_ββ = 1.516·10⁻³ eV",
    targetLatex: "m_{\\beta\\beta} = 1.516\\!\\times\\!10^{-3}\\,\\text{eV}",
    numericValue: "0.001516",
    unit: "eV",
    status: "Comparison quantity",
    dependencyClass: "Neutrino closure",
    killTest:
      "Light-Majorana detection implying m_ββ ≳ 10⁻² eV.",
    derivationFormulas: [
      "m_{\\beta\\beta} = 1.516\\!\\times\\!10^{-3}\\,\\text{eV}",
    ],
    pdf: "/predictions/tfpt_prediction_neutrinoless_double_beta.pdf",
    description:
      "Low-amplitude Majorana target generated by the same neutrino-closure package that fixes PMNS and the mass sum.",
    category: "Neutrino",
  },
  {
    id: "strong-cp",
    slug: "strong-cp-edm-null",
    title: "Strong CP — Neutron-EDM Null",
    shortTitle: "θ_eff = 0",
    target: "θ_eff = 0 (theorem-level null)",
    targetLatex: "\\theta_{\\mathrm{eff}} = 0",
    numericValue: "0",
    status: "Theorem-level null",
    dependencyClass: "Strong-CP closure",
    killTest: "Stable nonzero hadronic EDM signal.",
    derivationFormulas: [
      "\\arg\\det M_u = \\arg\\det M_d = 0",
      "\\theta_{\\mathrm{eff}} = 0",
      "\\bar\\theta = 0, \\quad F(\\theta) > F(0) \\text{ for } \\theta \\not\\equiv 0",
    ],
    pdf: "/predictions/tfpt_prediction_strong_cp_edm_null.pdf",
    description:
      "Consequence of determinant-line closure and admissibility, not a tunable flavor-sector phase.",
    category: "QCD/EDM",
  },
  {
    id: "birefringence",
    slug: "birefringence-beta",
    title: "Cosmic Birefringence — Determinant-Line Response",
    shortTitle: "β",
    target: "β = 0.2424°",
    targetLatex: "\\beta = 0.2424^\\circ",
    numericValue: "0.2424",
    unit: "°",
    status: "Physical observable",
    dependencyClass: "Determinant response",
    killTest:
      "Externally calibrated β = 0 within ±0.05°.",
    derivationFormulas: [
      "\\beta_{\\mathrm{rad}} = \\frac{\\varphi_0}{4\\pi}",
      "\\varphi_0 = \\frac{1}{6\\pi} + \\frac{3}{256\\pi^4}",
      "\\beta = 0.2424^\\circ",
    ],
    pdf: "/predictions/tfpt_prediction_birefringence_beta.pdf",
    description:
      "Determinant-line / Chern–Simons response — sectorized away from the old seed quartet.",
    category: "QCD/EDM",
  },
  {
    id: "eht-achromatic",
    slug: "eht-achromatic-intercept",
    title:
      "Achromatic Residual Polarization Intercept — EHT/ngEHT Test",
    shortTitle: "β_BH(r)",
    target:
      "β_BH(r) ∼ Q_e^eff Q_m^eff / (256π⁴ r²)  — structured, achromatic",
    targetLatex:
      "\\beta_{\\mathrm{BH}}(r) \\sim \\frac{Q_e^{\\mathrm{eff}}\\,Q_m^{\\mathrm{eff}}}{256\\pi^4\\,r^2} = 16 c_3^4 \\frac{Q_e^{\\mathrm{eff}}\\,Q_m^{\\mathrm{eff}}}{r^2}",
    numericValue: "16 c_3^4",
    status: "Physical observable",
    dependencyClass: "Determinant response (local)",
    killTest:
      "Calibrated achromatic residual intercept χ₀^res(x) statistically consistent with zero across the horizon-scale image after honest GRMHD subtraction, or no 1/r² profile, or no sign flip under E·B reversal, or measurable λ² dependence.",
    derivationFormulas: [
      "\\chi(x,\\lambda^2) = \\chi_0(x) + \\mathrm{RM}(x)\\,\\lambda^2 + \\epsilon",
      "\\chi_0^{\\mathrm{res}}(x) = \\chi_0^{\\mathrm{obs}}(x) - \\chi_0^{\\mathrm{GRMHD}}(x)",
      "\\beta_{\\mathrm{BH}}(r) = \\frac{Q_e^{\\mathrm{eff}}\\,Q_m^{\\mathrm{eff}}}{256\\pi^4\\,r^2} = \\frac{\\delta_{\\mathrm{top}}}{3}\\frac{Q_e^{\\mathrm{eff}}\\,Q_m^{\\mathrm{eff}}}{r^2}",
    ],
    pdf: "/predictions/tfpt_prediction_eht_achromatic_intercept.pdf",
    description:
      "Local dyonic projection of the determinant-line response. The TFPT coupling 1/(256π⁴) = 16c₃⁴ is fixed by the same branch data that fixes α and β_rad; only the geometric weights and emission radius are model-dependent. Three independent nulls (frequency, 1/r² profile, E·B sign flip) must be passed simultaneously.",
    category: "Astrophysics",
  },
  {
    id: "axion",
    slug: "axion-haloscope-window",
    title: "Axion Haloscope Window",
    shortTitle: "m_a, ν_a",
    target: "m_a ≈ 65.19 µeV, ν_a ≈ 15.764 GHz",
    targetLatex:
      "m_a \\simeq 65.19\\,\\mu\\text{eV}, \\quad \\nu_a \\simeq 15.764\\,\\text{GHz}",
    numericValue: "15.764",
    unit: "GHz",
    status: "Comparison quantity",
    dependencyClass: "Cosmology readout",
    killTest:
      "Exclusion in 15.764 GHz ± 50 MHz at the coupled sensitivity.",
    derivationFormulas: [
      "f_a \\approx 8.86\\!\\times\\!10^{10}\\,\\text{GeV}",
      "m_a \\approx 65.19\\,\\mu\\text{eV}, \\quad \\nu_a \\approx 15.764\\,\\text{GHz}",
      "|g_{a\\gamma\\gamma}^{(\\mathrm{phys})}| \\approx 1.80\\!\\times\\!10^{-12}\\,\\text{GeV}^{-1}",
    ],
    pdf: "/predictions/tfpt_prediction_axion_haloscope_window.pdf",
    description:
      "Downstream of seam transfer and determinant-line phase. The practical scan window is 15.764 GHz ± 50 MHz.",
    category: "Cosmology",
  },
  {
    id: "eta-b",
    slug: "eta-b-leptogenesis",
    title: "Baryon Asymmetry — Leptogenesis Interface",
    shortTitle: "η_B",
    target: "η_B = 5.97·10⁻¹⁰",
    targetLatex: "\\eta_B = 5.97\\!\\times\\!10^{-10}",
    numericValue: "5.97e-10",
    status: "Cosmology comparison",
    dependencyClass: "Cosmology readout",
    killTest:
      "Robust exclusion of the quoted branch value under the declared Boltzmann solver.",
    derivationFormulas: [
      "\\eta_B = 5.97\\!\\times\\!10^{-10}",
      "\\frac{dY_{\\Delta_\\alpha}}{dz}=\\sum_i \\epsilon_{i\\alpha} D_i (Y_{N_i}-Y_{N_i}^{\\mathrm{eq}}) - W_{i\\alpha} Y_{\\Delta_\\alpha}",
    ],
    pdf: "/predictions/tfpt_prediction_eta_b_leptogenesis.pdf",
    description:
      "Downstream of reheating and heavy-neutrino input data, evaluated through the flavored Boltzmann system.",
    category: "Cosmology",
  },
  {
    id: "omega-b",
    slug: "omega-b-cosmology",
    title: "Baryon Density — Cosmology Comparison",
    shortTitle: "Ω_b",
    target: "Ω_b = 0.04894",
    targetLatex: "\\Omega_b = 0.04894",
    numericValue: "0.04894",
    status: "Cosmology comparison",
    dependencyClass: "Cosmology readout",
    killTest:
      "Robust inconsistency under the declared Planck comparison convention.",
    derivationFormulas: [
      "\\Omega_b = \\frac{\\Omega_b h^2}{h^2}, \\quad h = \\tfrac{H_0}{100}",
      "\\Omega_b = (4\\pi - 1)\\beta_{\\mathrm{rad}} = 0.04894",
    ],
    pdf: "/predictions/tfpt_prediction_omega_b_cosmology.pdf",
    description:
      "Present-epoch reconstruction, Planck 2018 comparison row 0.04930 (residual −0.421σ).",
    category: "Cosmology",
  },
  {
    id: "no-second-higgs",
    slug: "no-second-higgs",
    title: "No Second Light Higgs Doublet",
    shortTitle: "N_Φ = 1",
    target: "no additional seam-even light doublet",
    targetLatex: "N_\\Phi = 1",
    numericValue: "1",
    status: "Kill test",
    dependencyClass: "Carrier / Higgs index",
    killTest: "Robust discovery of a second light seam-even Higgs doublet.",
    derivationFormulas: [
      "(c_1(L_2), c_1(L_3)) = (1, 0)",
      "N_\\Phi = 1",
    ],
    pdf: "/predictions/tfpt_prediction_no_second_higgs.pdf",
    description:
      "Compact bosonic index fixes the determinant class with exactly one weak doublet — a structural prohibition, not a fit.",
    category: "Higgs",
  },
  {
    id: "pi0",
    slug: "pi0-hadronic",
    title: "Neutral Pion — Hadronic Check",
    shortTitle: "m_π⁰",
    target: "m_π⁰ = 134.979 MeV",
    targetLatex: "m_{\\pi^0} = 134.979\\,\\text{MeV}",
    numericValue: "134.979",
    unit: "MeV",
    status: "Out-of-sample check",
    dependencyClass: "Hadronic readout",
    killTest:
      "Robust mismatch outside the stated hadronic uncertainty budget.",
    derivationFormulas: [
      "m_{\\pi^0}\\,\\text{from GMOR with}\\,(m_u + m_d)\\,\\text{and}\\,\\langle\\bar q q\\rangle",
      "m_{\\pi^0} = 134.979\\,\\text{MeV}",
    ],
    pdf: "/predictions/tfpt_prediction_pi0_hadronic.pdf",
    description:
      "Out-of-sample hadronic consistency check derived from the closed branch — not used to tune the carrier or flavor branch.",
    category: "QCD/EDM",
  },
];
