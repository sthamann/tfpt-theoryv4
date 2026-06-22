"use client";

import { motion } from "motion/react";
import { Math } from "@/components/Math";

type Severity = "theorem" | "bridge" | "structural" | "downstream";

const SEVERITY_META: Record<
  Severity,
  { label: string; chip: string; tone: string }
> = {
  theorem: {
    label: "Identity / theorem kill",
    chip: "bg-blue-500/15 text-blue-200 ring-blue-400/30",
    tone: "from-blue-500 to-violet-500",
  },
  bridge: {
    label: "Numerical kill",
    chip: "bg-emerald-500/15 text-emerald-200 ring-emerald-400/30",
    tone: "from-emerald-500 to-teal-500",
  },
  structural: {
    label: "Structural kill",
    chip: "bg-orange-500/15 text-orange-200 ring-orange-400/30",
    tone: "from-orange-500 to-red-500",
  },
  downstream: {
    label: "Cosmology kill",
    chip: "bg-fuchsia-500/15 text-fuchsia-200 ring-fuchsia-400/30",
    tone: "from-fuchsia-500 to-pink-500",
  },
};

interface KillRow {
  area: string;
  paper: string;
  criterion: string;
  formal: string;
  severity: Severity;
}

const ROWS: KillRow[] = [
  {
    area: "Solar angle θ₁₂",
    paper: "Doc 2 · JUNO (live)",
    criterion:
      "A JUNO central value clearly away from sin²θ₁₂ ≈ 0.307 at high significance kills the seam-misalignment mechanism. JUNO has been taking data since August 2025 — this is the sharpest live test.",
    formal: "\\sin^2\\theta_{12} \\neq \\tfrac{1}{3} - \\tfrac{\\varphi_0}{2} \\approx 0.3067",
    severity: "bridge",
  },
  {
    area: "Tensor ratio r",
    paper: "Doc 1 · CMB-S4",
    criterion:
      "Any robust r ≳ 0.01 is incompatible with the R² branch on which M_Pl and A_s rest. The scalaron predicts r = 12/N★² ≈ 0.004, already below the BK18 bound r < 0.036.",
    formal: "r \\gtrsim 0.01 \\;\\Rightarrow\\; R^2\\text{ branch killed}",
    severity: "bridge",
  },
  {
    area: "Neutrino ordering / m_ββ",
    paper: "Doc 2 · LEGEND, nEXO",
    criterion:
      "Inverted ordering, or a large effective Majorana mass m_ββ, kills the Majorana branch. TFPT prefers normal ordering with a small m_ββ.",
    formal: "\\text{inverted ordering, or } m_{\\beta\\beta} \\gtrsim 10^{-2}\\,\\text{eV}",
    severity: "bridge",
  },
  {
    area: "Leptonic CP phase δ_PMNS",
    paper: "Origin Theory · DUNE / Hyper-K (v320)",
    criterion:
      "The two CP phases are Galois-locked: both are powers of one hexagonal unit ρ = ζ₆ of the family factor, so δ_PMNS = arg(ρ⁴) = δ_CKM,lead + π = 240° (the previously assigned value is now a forced relation to the measured quark phase). A measured δ_PMNS robustly away from 240° (beyond the sub-leading budget, >3σ at DUNE/Hyper-K/JUNO) falsifies the whole Galois-CP organisation.",
    formal: "\\delta_{\\mathrm{PMNS}} \\neq \\delta_{\\mathrm{CKM}}^{\\mathrm{lead}} + \\pi = 240^\\circ",
    severity: "structural",
  },
  {
    area: "Strong CP θ_eff",
    paper: "Doc 2 · PSI nEDM",
    criterion:
      "A solid neutron-EDM signal above the SM background falsifies the structural cancellation. θ_eff = 0 follows from γ₅-Hermiticity, polar structure and the sheet involution plus reflection positivity.",
    formal: "\\theta_{\\mathrm{eff}} \\neq 0 \\;\\Rightarrow\\; \\text{construction killed}",
    severity: "theorem",
  },
  {
    area: "Dark-energy w",
    paper: "Doc 1 · DESI",
    criterion:
      "A robust w ≠ −1 kills the single-engine dark-energy readout, where Λ ∼ e⁻²ᵅ⁻¹ and H₀ ∼ √Λ come from the same exponential scale grammar.",
    formal: "w \\neq -1",
    severity: "downstream",
  },
  {
    area: "EM fixed point α⁻¹",
    paper: "Doc 1 · CODATA",
    criterion:
      "F_U(1)(α) = 0 fails to admit a unique positive root, or the root drifts outside the declared interface uncertainty (currently ≈ 4 × 10⁻⁸ in α⁻¹, about 1.9σ of CODATA-2022).",
    formal: "F_{U(1)}(\\alpha_\\star) = 0 \\text{ has no/second root, or } |\\Delta\\alpha^{-1}| > \\Delta",
    severity: "bridge",
  },
  {
    area: "E₈ glue",
    paper: "Doc 1 (structural)",
    criterion:
      "D₅ and A₃ fail to share the ℤ₄ discriminant, or the glue norms do not sum to the E₈ root norm 2. The whole compiler closure rests on this lattice fact.",
    formal: "\\operatorname{disc}(D_5) \\neq \\operatorname{disc}(A_3) \\text{ or } q(D_5)+q(A_3) \\neq 2",
    severity: "theorem",
  },
  {
    area: "Flavor invariants",
    paper: "Doc 2 (structural)",
    criterion:
      "A future global CKM/PMNS fit that cannot be carried by a residue matrix with det R = 8, principal 2-minors (2,3,5) and χ_R = t³ − 9t² + 10t − 8. Every load-bearing flavor number must live in an E₈ projection.",
    formal: "\\det R \\neq 8 \\text{ or } \\mathrm{minors} \\neq (2,3,5)",
    severity: "structural",
  },
  {
    area: "No second Higgs",
    paper: "Doc 1 (structural)",
    criterion:
      "Robust discovery of a second light seam-even Higgs doublet. The carrier index forces N_Φ = g_car − |μ₄| = 1; an additional doublet kills it.",
    formal: "N_\\Phi = 1 \\Rightarrow \\text{no second light doublet}",
    severity: "structural",
  },
  {
    area: "m_p/m_e — not claimed",
    paper: "Doc 4 (honesty)",
    criterion:
      "The proton/electron ratio is explicitly NOT claimed as a compiler power. It is a cross-sector QCD/EW ratio, deliberately not forced onto the ladder — it only fails if mis-asserted as a compiler power.",
    formal: "m_p/m_e \\text{ is } [\\mathrm{A}],\\ \\text{not a compiler power}",
    severity: "structural",
  },
  {
    area: "Status discipline",
    paper: "Cross-cutting",
    criterion:
      "A claim is promoted past the grade its document carries, an empirical input enters undeclared, or the text disagrees with the machine-checked ledger. The ledger always wins.",
    formal: "\\text{text} \\neq \\text{status ledger}",
    severity: "structural",
  },
];

export function KillCriteria() {
  // Rendered inside an already-labelled <section> (see app/falsification/page.tsx),
  // so this wrapper is a plain <div>: a nested <section> with the same
  // aria-labelledby would create a duplicate landmark with the same accessible
  // name. The id is preserved for in-page anchor links.
  return (
    <div id="kill-criteria" className="relative py-12">
      <div className="mx-auto max-w-5xl">
        <div className="space-y-3">
          {ROWS.map((row, i) => {
            const meta = SEVERITY_META[row.severity];
            return (
              <motion.article
                key={row.area}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.05 }}
                transition={{ duration: 0.4, delay: i * 0.04 }}
                className="glass relative overflow-hidden rounded-2xl ring-1 ring-slate-700/40"
              >
                <div
                  aria-hidden="true"
                  className={`absolute inset-x-0 top-0 h-px bg-gradient-to-r ${meta.tone}`}
                />
                <div className="grid gap-4 p-5 sm:grid-cols-[1fr_2fr] sm:gap-6">
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="font-serif text-base font-semibold text-slate-50">
                        {row.area}
                      </h3>
                    </div>
                    <div className="mt-1 text-[10px] font-semibold uppercase tracking-widest text-slate-400">
                      {row.paper}
                    </div>
                    <span
                      className={`mt-3 inline-block rounded-full px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest ring-1 ${meta.chip}`}
                    >
                      {meta.label}
                    </span>
                  </div>
                  <div>
                    <p className="text-sm leading-relaxed text-slate-300">
                      {row.criterion}
                    </p>
                    <div className="mt-3 overflow-x-auto formula-scroll rounded-md border border-slate-700/40 bg-slate-950/40 p-3">
                      <Math block>{row.formal}</Math>
                    </div>
                  </div>
                </div>
              </motion.article>
            );
          })}
        </div>
      </div>
    </div>
  );
}
