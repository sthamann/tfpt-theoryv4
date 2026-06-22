"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";

interface AuditRow {
  output: string;
  inputsAllowed: string;
  inputsForbidden: string;
  freeKnobs: string;
  /** The single condition that would falsify this row (mirror of the kill board / KillCriteria). */
  kill: string;
}

const ROWS: AuditRow[] = [
  {
    output: "α⁻¹(0)",
    inputsAllowed:
      "c₃ = 1/(8π), b₁ = 41/10, the word-lengths Σ L + N_Φ = 41, the exact seam opening φ_seam(α)",
    inputsForbidden:
      "Fitting against CODATA / atom-recoil values; freezing φ_seam at φ₀ inside the root equation",
    freeKnobs: "0",
    kill: "No unique positive root of F_U(1)=0, or the root drifts outside the declared interface uncertainty (~1.9σ).",
  },
  {
    output: "sin²θ₁₂  (solar angle)",
    inputsAllowed: "The seed φ₀ and the glue norm q(A₃) = 3/4 (seam misalignment ε = (3/4)φ₀)",
    inputsForbidden: "NuFIT central value pre-loaded as input",
    freeKnobs: "0",
    kill: "A JUNO central value clearly away from 0.307 at high significance.",
  },
  {
    output: "sin²θ₁₃  (reactor angle)",
    inputsAllowed: "The seed φ₀ and the carrier trace e⁻⁵ᐟ⁶ (γ = 5/6)",
    inputsForbidden: "Oscillation-fit central value pre-loaded as input",
    freeKnobs: "0",
    kill: "A robust normal-ordering global-fit exclusion at the stated confidence level.",
  },
  {
    output: "δ_PMNS = 240°  (leptonic CP phase)",
    inputsAllowed:
      "The hexagonal unit ρ = ζ₆ of the family Galois factor; δ_PMNS = arg(ρ⁴) = δ_CKM,lead + π, locked by ρ⁴ = −ρ (v320)",
    inputsForbidden: "A free leptonic CP phase fit to NuFIT",
    freeKnobs: "0",
    kill: "A measured δ_PMNS robustly away from δ_CKM,lead + π = 240° (>3σ at DUNE/Hyper-K).",
  },
  {
    output: "det R = 8, minors (2,3,5)",
    inputsAllowed: "The compiler residue matrix R = R(g_car, μ₄)",
    inputsForbidden: "Fitting R to a CKM/PMNS global fit",
    freeKnobs: "0",
    kill: "A CKM/PMNS global fit no residue matrix with det 8, minors (2,3,5) can carry.",
  },
  {
    output: "N_Φ = 1  (Higgs index)",
    inputsAllowed: "The carrier index, N_Φ = g_car − |μ₄| = 1",
    inputsForbidden: "Observed Higgs count used as primitive input",
    freeKnobs: "0",
    kill: "Robust discovery of a second light seam-even Higgs doublet.",
  },
  {
    output: "θ_eff = 0  (strong-CP null)",
    inputsAllowed:
      "γ₅-Hermiticity, polar structure, sheet involution + reflection positivity",
    inputsForbidden: "Tuned θ-phase, hidden flavor-side cancellation",
    freeKnobs: "0",
    kill: "A solid neutron-EDM signal above the Standard-Model background.",
  },
  {
    output: "M_scal = c₃^(7/2) M̄  (scalaron)",
    inputsAllowed: "The seam power c₃⁷ = c₃^(Ω_adm − 10 b₁), exponent 7 = 48 − 41",
    inputsForbidden: "Fitting the scalaron mass to A_s",
    freeKnobs: "0",
    kill: "A scalaron mass incompatible with the seam power c₃⁷.",
  },
  {
    output: "n_s, r, A_s  (inflation)",
    inputsAllowed: "The R² attractor + the seam-fixed scalaron mass + the e-fold count N★",
    inputsForbidden: "A free inflationary amplitude",
    freeKnobs: "0 (amplitude) · N★ input (50–60)",
    kill: "A robust r ≳ 0.01 kills the R² branch carrying M_Pl and A_s.",
  },
  {
    output: "β_rad = 0.2424°  (birefringence)",
    inputsAllowed: "The determinant-line response, β_rad = φ₀/(4π)",
    inputsForbidden: "Calibration absorbed into the predicted angle",
    freeKnobs: "0",
    kill: "An externally calibrated β = 0 within tight error.",
  },
  {
    output: "Ω_b = 0.04894  (baryon density)",
    inputsAllowed: "β_rad via Ω_b = (4π − 1)β_rad",
    inputsForbidden: "Planck value used as primitive input",
    freeKnobs: "0",
    kill: "Robust inconsistency under the declared Planck comparison convention.",
  },
  {
    output: "m_a ≈ 23.8 µeV  (axion DM)",
    inputsAllowed: "f_a = M_scal/128 and the closed misalignment θ_i = 170°",
    inputsForbidden: "Coupling rescaling to fit a haloscope window",
    freeKnobs: "0 (decay-constant conjecture) · scenario-dependent (relic)",
    kill: "Exclusion of the determinant-line axion window at the coupled sensitivity.",
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
            <table className="w-full min-w-[1180px] border-separate border-spacing-0 text-left text-sm">
              <thead>
                <tr>
                  {[
                    "Output",
                    "Inputs allowed",
                    "Inputs forbidden",
                    "Free knobs",
                    "Kill condition",
                    "Verify",
                  ].map((h) => (
                    <th
                      key={h}
                      scope="col"
                      className="border-b border-slate-800/60 bg-slate-950/60 px-4 py-3 text-[10px] font-semibold uppercase tracking-widest text-slate-300"
                    >
                      {h}
                    </th>
                  ))}
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
                    <td className="border-b border-slate-800/60 px-4 py-3 align-top text-xs leading-relaxed text-amber-200/90">
                      {row.kill}
                    </td>
                    <td className="border-b border-slate-800/60 px-4 py-3 align-top text-xs">
                      <Link
                        href="/verification#dag"
                        className="inline-flex items-center gap-1 font-semibold text-blue-300 transition-colors hover:text-blue-200"
                      >
                        Run it
                        <ArrowUpRight size={12} aria-hidden />
                      </Link>
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
