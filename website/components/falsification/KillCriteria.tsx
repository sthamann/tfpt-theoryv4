"use client";

import { motion } from "motion/react";
import { Math } from "@/components/Math";

type Severity = "theorem" | "bridge" | "structural" | "downstream";

const SEVERITY_META: Record<
  Severity,
  { label: string; chip: string; tone: string }
> = {
  theorem: {
    label: "Theorem-level kill",
    chip: "bg-blue-500/15 text-blue-200 ring-blue-400/30",
    tone: "from-blue-500 to-violet-500",
  },
  bridge: {
    label: "Bridge readout kill",
    chip: "bg-emerald-500/15 text-emerald-200 ring-emerald-400/30",
    tone: "from-emerald-500 to-teal-500",
  },
  structural: {
    label: "Structural kill",
    chip: "bg-orange-500/15 text-orange-200 ring-orange-400/30",
    tone: "from-orange-500 to-red-500",
  },
  downstream: {
    label: "Downstream kill",
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
    area: "Carrier theorem",
    paper: "Paper 2",
    criterion:
      "The 3+2 carrier split is not derivable without importing Standard-Model representation data — i.e. dim E_+ = 2 or dim E_- = 3 turn out to require an SM-side input rather than the compact Higgs index and the primitive Yukawa type.",
    formal: "(\\dim E_-,\\dim E_+) = (3,2) \\text{ requires an SM-side import}",
    severity: "theorem",
  },
  {
    area: "Joint discrete solve",
    paper: "Papers 1, 2",
    criterion:
      "An alternative admissible discrete solution survives all primitive constraints (boundary kernel, Higgs index, primitive Yukawa, seam normalisation). The closed branch would no longer be unique.",
    formal: "\\#\\,d^\\star_{\\mathrm{disc}} > 1",
    severity: "theorem",
  },
  {
    area: "Electromagnetic closure",
    paper: "Paper 3",
    criterion:
      "The carrier-form closure equation F_U(1)(α) = 0 fails to admit a unique positive root, or the root differs from CODATA 2022 by more than the declared interface uncertainty (currently ≈ 4 × 10⁻⁸ in α⁻¹).",
    formal: "F_{U(1)}(\\alpha_\\star)=0 \\text{ has no positive root, or }|\\alpha_\\star^{-1} - \\alpha^{-1}_{\\mathrm{CODATA}}| > \\Delta",
    severity: "bridge",
  },
  {
    area: "Strong CP",
    paper: "Paper 4",
    criterion:
      "A stable nonzero hadronic EDM signal under the declared comparison convention. The admissibility/determinant-line argument forces θ_eff = 0 at theorem level, so any robust EDM detection kills the construction.",
    formal: "\\theta_{\\mathrm{eff}} \\neq 0 \\;\\Rightarrow\\; \\text{construction killed}",
    severity: "theorem",
  },
  {
    area: "Higgs sector",
    paper: "Paper 2 → 3",
    criterion:
      "Robust discovery of a second light seam-even Higgs doublet. The compact bosonic index forces N_Φ = 1; an additional doublet kills the determinant class.",
    formal: "N_\\Phi = 1 \\text{ (forced by index) } \\Rightarrow \\text{no second light doublet}",
    severity: "structural",
  },
  {
    area: "Axion haloscope",
    paper: "Paper 6",
    criterion:
      "Calibrated haloscope exclusion of the 15.764 GHz ± 50 MHz window at the coupled sensitivity. A clean exclusion of the predicted band kills the cosmology readout chain.",
    formal: "\\nu_a \\notin [15.714, 15.814]\\,\\mathrm{GHz}",
    severity: "downstream",
  },
  {
    area: "Cosmic birefringence β",
    paper: "Paper 3 (response)",
    criterion:
      "Externally calibrated cosmic-rotation analysis statistically consistent with β = 0 within ±0.05° (without EB self-nulling). Determinant-line response would not be in the data.",
    formal: "\\beta = 0 \\pm 0.05^\\circ \\text{ at declared confidence}",
    severity: "bridge",
  },
  {
    area: "EHT achromatic intercept",
    paper: "Paper 3 → standalone",
    criterion:
      "Calibrated achromatic residual χ₀^res(x) = χ₀^obs − χ₀^GRMHD statistically consistent with zero across the horizon-scale image, or no 1/r² profile, or no E·B sign flip, or measurable λ² dependence.",
    formal: "\\chi_0^{\\mathrm{res}} \\equiv 0 \\text{ after honest GRMHD subtraction}",
    severity: "downstream",
  },
  {
    area: "Cosmology comparison",
    paper: "Paper 6",
    criterion:
      "Robust inconsistency between the closed-branch readouts (Λ_IR, η_B, Σ m_ν, Ω_b) and the comparison data under the declared convention, beyond stated interface uncertainty.",
    formal: "\\text{Closed-branch row} \\notin \\text{declared comparison interval}",
    severity: "downstream",
  },
  {
    area: "Status discipline",
    paper: "Cross-cutting",
    criterion:
      "An assumption first becomes invisible — i.e. an empirical input enters the proof chain without being declared as such, or a downstream comparison feeds back into the primitive branch.",
    formal: "\\text{Hidden empirical input upstream of }\\mathfrak{T}_\\star",
    severity: "structural",
  },
];

export function KillCriteria() {
  return (
    <section
      id="kill-criteria"
      className="relative scroll-mt-20 py-12"
      aria-labelledby="kill-criteria-heading"
    >
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
    </section>
  );
}
