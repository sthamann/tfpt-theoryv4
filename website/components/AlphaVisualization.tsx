"use client";

import { motion } from "motion/react";
import { Math } from "./Math";

const COMPARISON = [
  {
    label: "TFPT closed root",
    value: "137.035 999 216 8…",
    note: "Unique positive root of F_U(1)(α) = 0",
    accent: "from-blue-500 to-violet-500",
  },
  {
    label: "CODATA 2022",
    value: "137.035 999 084(21)",
    note: "Recommended value, atomic-physics input",
    accent: "from-emerald-500 to-teal-500",
  },
  {
    label: "Residual",
    value: "≈ 1.3 × 10⁻⁷",
    note: "Inside the stated interface uncertainty",
    accent: "from-orange-500 to-amber-500",
  },
];

export function AlphaVisualization() {
  return (
    <div className="glass rounded-2xl ring-1 ring-slate-700/40">
      <div className="border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          Electromagnetic closure — α as a self-consistent root
        </span>
      </div>
      <div className="grid gap-8 p-6 md:p-8 lg:grid-cols-2">
        <div>
          <h3 className="font-serif text-lg font-semibold text-slate-50">
            The closure equation
          </h3>
          <p className="mt-2 text-sm leading-relaxed text-slate-300">
            With <Math>{"c_3 = \\tfrac{1}{8\\pi}"}</Math>,{" "}
            <Math>{"b_1 = \\tfrac{41}{10}"}</Math>, and{" "}
            <Math>{"\\sum L_{f,j} + N_\\Phi = 41"}</Math> from the carrier
            packet, the seam opening
          </p>
          <div className="mt-3 overflow-x-auto rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
            <Math block>
              {"\\varphi_{\\mathrm{seam}}(\\alpha) = \\frac{1}{6\\pi} + \\frac{3 e^{-2\\alpha}}{256\\pi^4}\\!\\left(1-\\frac{3 e^{-2\\alpha}}{256\\pi^4}\\right)^{-5/4}"}
            </Math>
          </div>
          <p className="mt-3 text-sm text-slate-300">enters the closure function</p>
          <div className="mt-3 overflow-x-auto rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
            <Math block>
              {"F_{U(1)}(\\alpha) = \\alpha^3 - 2c_3^3\\alpha^2 - \\tfrac{4}{5}c_3^6\\!\\left(\\textstyle\\sum L_{f,j} + N_\\Phi\\right)\\log\\!\\left(\\varphi_{\\mathrm{seam}}(\\alpha)^{-1}\\right)"}
            </Math>
          </div>
          <p className="mt-3 text-sm text-slate-300">
            and the prediction is the unique positive root.
          </p>
          <div className="mt-3 overflow-x-auto rounded-lg border border-blue-400/30 bg-blue-500/5 p-3">
            <Math block>
              {"F_{U(1)}(\\alpha_\\star) = 0 \\;\\Rightarrow\\; \\alpha_\\star^{-1} = 137.035\\,999\\,216\\,8\\ldots"}
            </Math>
          </div>
        </div>

        <div className="space-y-3">
          {COMPARISON.map((c, i) => (
            <motion.div
              key={c.label}
              initial={{ opacity: 0, x: 12 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: i * 0.1 }}
              className="relative overflow-hidden rounded-xl border border-slate-700/40 bg-slate-950/40 px-5 py-4"
            >
              <div
                className={`absolute left-0 top-0 h-full w-1 bg-gradient-to-b ${c.accent}`}
                aria-hidden="true"
              />
              <div className="text-[10px] font-semibold uppercase tracking-widest text-slate-400">
                {c.label}
              </div>
              <div className="mt-1 font-mono text-xl font-semibold text-slate-50 sm:text-2xl">
                {c.value}
              </div>
              <div className="mt-1 text-xs leading-snug text-slate-400">
                {c.note}
              </div>
            </motion.div>
          ))}

          <div className="mt-6 rounded-lg border border-amber-400/20 bg-amber-500/5 p-4 text-xs leading-relaxed text-amber-100/90">
            <strong className="text-amber-200">No-knobs audit.</strong>{" "}
            The exact opening{" "}
            <Math>{"\\varphi_{\\mathrm{seam}}(\\alpha)"}</Math> must remain inside
            the root equation. Freezing it at <Math>{"\\varphi_0"}</Math> shifts
            the result by ~ 5.02 × 10⁻⁴ in α⁻¹ and is not the benchmark
            definition.
          </div>
        </div>
      </div>
    </div>
  );
}
