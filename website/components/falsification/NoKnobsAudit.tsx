"use client";

import { motion } from "motion/react";

interface AuditRow {
  output: string;
  inputsAllowed: string;
  inputsForbidden: string;
  freeKnobs: string;
}

const ROWS: AuditRow[] = [
  {
    output: "α⁻¹(0)",
    inputsAllowed:
      "Primitive kernel (Paper 1), carrier packet (Paper 2), exact seam opening φ_seam(α)",
    inputsForbidden:
      "Fitting against CODATA / atom-recoil values; freezing φ_seam at φ₀ inside the root equation",
    freeKnobs: "0",
  },
  {
    output: "λ_C  (Cabibbo angle)",
    inputsAllowed: "Retained seed φ₀ from the joint discrete solve",
    inputsForbidden: "Global CKM-fit residual absorbed into λ_C",
    freeKnobs: "0",
  },
  {
    output: "sin²θ₁₃  (reactor angle)",
    inputsAllowed: "Retained seed φ₀ + γ = 5/6",
    inputsForbidden: "Oscillation-fit central value pre-loaded as input",
    freeKnobs: "0",
  },
  {
    output: "δ_CKM  (CP phase)",
    inputsAllowed:
      "Holonomy transport on the rigid branch; lower critical point of the cusp cubic",
    inputsForbidden: "Adjustable CP dial in the transport sector",
    freeKnobs: "0",
  },
  {
    output: "N_Φ = 1  (Higgs index)",
    inputsAllowed: "Compact bosonic index on the seam-even line bundle",
    inputsForbidden: "Observed Higgs count used as primitive input",
    freeKnobs: "0",
  },
  {
    output: "θ_eff = 0  (strong-CP null)",
    inputsAllowed:
      "Admissibility selector P_adm = P_prim · P_sing · P_Θ, determinant-line phase",
    inputsForbidden: "Tuned θ-phase, hidden flavor-side cancellation",
    freeKnobs: "0",
  },
  {
    output: "β = 0.2424°  (cosmic birefringence)",
    inputsAllowed: "Determinant-line / Chern–Simons response, retained seed φ₀",
    inputsForbidden: "Calibration absorbed into the predicted angle",
    freeKnobs: "0",
  },
  {
    output: "β_BH(r)  (achromatic dyonic intercept)",
    inputsAllowed:
      "Coupling 1/(256π⁴) = 16 c₃⁴ from the same admissibility data as α; geometric weights from the GRMHD source model",
    inputsForbidden:
      "Free coupling rescaling; spatial profile fitted to the residual map",
    freeKnobs: "0 (coupling) · model-dependent (geometry, emission radius)",
  },
  {
    output: "ξ = c₃ / φ₀  (Einstein-limit normalizer)",
    inputsAllowed: "c₃ = 1/(8π) (Paper 1), φ₀ from the retained seed",
    inputsForbidden: "Deriving SI G_N from two dimensionless numbers",
    freeKnobs: "0",
  },
  {
    output: "ν_a ≈ 15.764 GHz  (axion haloscope)",
    inputsAllowed:
      "Seam transfer, determinant-line phase, downstream cosmology budget",
    inputsForbidden: "Coupling rescaling to fit a haloscope window",
    freeKnobs: "0 (coupling) · model-dependent (cosmology)",
  },
];

export function NoKnobsAudit() {
  // Rendered inside an already-labelled <section> (see app/falsification/page.tsx),
  // so this wrapper is a plain <div>: a nested <section> with the same
  // aria-labelledby would create a duplicate landmark with the same accessible
  // name. The id is preserved for in-page anchor links.
  return (
    <div id="no-knobs" className="relative py-12">
      <div className="mx-auto max-w-6xl">
        <div className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 px-5 py-3">
            <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
              No-knobs audit — what is allowed, what is forbidden
            </span>
            <span className="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-emerald-200 ring-1 ring-emerald-400/30">
              Free knobs: 0
            </span>
          </div>

          <div className="overflow-x-auto formula-scroll">
            <table className="w-full min-w-[900px] border-separate border-spacing-0 text-left text-sm">
              <thead>
                <tr>
                  <th
                    scope="col"
                    className="border-b border-slate-800/60 bg-slate-950/60 px-4 py-3 text-[10px] font-semibold uppercase tracking-widest text-slate-300"
                  >
                    Output
                  </th>
                  <th
                    scope="col"
                    className="border-b border-slate-800/60 bg-slate-950/60 px-4 py-3 text-[10px] font-semibold uppercase tracking-widest text-slate-300"
                  >
                    Inputs allowed
                  </th>
                  <th
                    scope="col"
                    className="border-b border-slate-800/60 bg-slate-950/60 px-4 py-3 text-[10px] font-semibold uppercase tracking-widest text-slate-300"
                  >
                    Inputs forbidden
                  </th>
                  <th
                    scope="col"
                    className="border-b border-slate-800/60 bg-slate-950/60 px-4 py-3 text-[10px] font-semibold uppercase tracking-widest text-slate-300"
                  >
                    Free knobs
                  </th>
                </tr>
              </thead>
              <tbody>
                {ROWS.map((row, i) => (
                  <motion.tr
                    key={row.output}
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true, amount: 0.05 }}
                    transition={{ duration: 0.3, delay: i * 0.03 }}
                    className="hover:bg-slate-900/30"
                  >
                    <td className="border-b border-slate-800/60 px-4 py-3 align-top font-mono text-xs font-semibold text-slate-100">
                      {row.output}
                    </td>
                    <td className="border-b border-slate-800/60 px-4 py-3 align-top text-xs leading-relaxed text-slate-300">
                      {row.inputsAllowed}
                    </td>
                    <td className="border-b border-slate-800/60 px-4 py-3 align-top text-xs leading-relaxed text-rose-200/80">
                      {row.inputsForbidden}
                    </td>
                    <td className="border-b border-slate-800/60 px-4 py-3 align-top text-xs font-semibold text-emerald-200">
                      {row.freeKnobs}
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="border-t border-slate-800/60 px-5 py-3 text-[11px] leading-relaxed text-slate-400">
            <strong className="text-slate-200">Reading rule.</strong> For every
            row, the output value must be reproducible from the &ldquo;allowed
            inputs&rdquo; alone — without touching the &ldquo;forbidden
            inputs&rdquo;. The free-knob count is the number of parameters the
            theory may adjust to land on the listed value. Any row where this
            count exceeds zero is treated as a fit, not a prediction.
          </div>
        </div>
      </div>
    </div>
  );
}
