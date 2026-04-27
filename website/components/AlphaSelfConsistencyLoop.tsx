"use client";

import { motion } from "motion/react";
import { Math } from "./Math";

const STAGES = [
  {
    id: "carrier",
    label: "Carrier packet",
    body: "Y, b₁ = 41/10, ΣL_{f,j} + N_Φ = 41",
  },
  {
    id: "phi-seam",
    label: "Seam opening",
    body: "φ_seam(α)",
  },
  {
    id: "F",
    label: "Closure function",
    body: "F_U(1)(α)",
  },
  {
    id: "alpha",
    label: "Unique positive root",
    body: "α⋆⁻¹ = 137.035 999 216 8…",
  },
];

export function AlphaSelfConsistencyLoop() {
  return (
    <div className="rounded-xl border border-slate-700/40 bg-slate-950/40 p-4 sm:p-5">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h4 className="font-serif text-base font-semibold text-slate-50">
          Self-consistency feedback loop
        </h4>
        <span className="rounded-full bg-violet-500/15 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-violet-200 ring-1 ring-violet-400/30">
          <span className="math-label">α</span> appears in{" "}
          <span className="math-label">φ_seam(α)</span>
        </span>
      </div>

      <p className="mt-2 text-xs leading-relaxed text-slate-400">
        The seam opening{" "}
        <Math>{"\\varphi_{\\mathrm{seam}}(\\alpha)"}</Math> depends on α
        itself, so α is fixed as the unique positive root of a closure
        equation that contains α inside its own opening — not as a freely
        adjustable parameter.
      </p>

      <ol className="mt-4 space-y-2">
        {STAGES.map((s, i) => (
          <motion.li
            key={s.id}
            initial={{ opacity: 0, x: -10 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, amount: 0.05 }}
            transition={{ duration: 0.4, delay: i * 0.08 }}
            className="relative flex items-center gap-3 rounded-lg border border-slate-700/40 bg-slate-950/60 px-3 py-2"
          >
            <span className="flex h-6 w-6 flex-none items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-violet-500 font-mono text-[10px] font-semibold text-white">
              {i + 1}
            </span>
            <div className="min-w-0 flex-1">
              <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
                {s.label}
              </div>
              <div className="font-mono text-xs text-slate-200">{s.body}</div>
            </div>
            {i < STAGES.length - 1 && (
              <span aria-hidden className="text-slate-500">
                ↓
              </span>
            )}
          </motion.li>
        ))}

        <li
          aria-hidden
          className="relative flex items-center gap-3 rounded-lg border border-violet-400/30 bg-violet-500/5 px-3 py-2"
        >
          <span className="flex h-6 w-6 flex-none items-center justify-center rounded-full bg-violet-500/30 font-mono text-[10px] font-semibold text-violet-100">
            ↺
          </span>
          <div className="min-w-0 flex-1">
            <div className="text-[10px] font-semibold uppercase tracking-widest text-violet-200">
              Feedback
            </div>
            <div className="text-xs leading-snug text-violet-100/85">
              The same α appears inside{" "}
              <Math>{"\\varphi_{\\mathrm{seam}}(\\alpha)"}</Math> — the loop
              closes only at α⋆.
            </div>
          </div>
        </li>
      </ol>

      <div className="mt-4 rounded-md border border-slate-700/40 bg-slate-950/60 p-3 text-[11px] leading-relaxed text-slate-300">
        <strong className="text-slate-100">Why this is not a fit.</strong>{" "}
        The carrier packet, c₃, b₁, and ΣL+N_Φ are fixed by Papers 1 and 2{" "}
        <em>before</em> the closure equation is touched. There is no degree
        of freedom left to absorb the CODATA value.
      </div>
    </div>
  );
}
