"use client";

import { motion } from "motion/react";
import { Math } from "./Math";
import { AlphaRootPlot } from "./AlphaRootPlot";
import { AlphaSelfConsistencyLoop } from "./AlphaSelfConsistencyLoop";

const COMPARISON: Array<{
  label: React.ReactNode;
  value: string;
  note: string;
  accent: string;
  kind: string;
  /** Whether the label contains math glyphs that must skip uppercase. */
  isMath?: boolean;
}> = [
  {
    label: "TFPT closed-branch root",
    value: "137.035 999 216 8…",
    note: "Unique positive root of F_U(1)(α) = 0; theoretical, no fit",
    accent: "from-blue-500 to-violet-500",
    kind: "theory",
  },
  {
    label: "CODATA 2022 recommended",
    value: "137.035 999 177(21)",
    note: "NIST CODATA 2022 adjustment, recommended value",
    accent: "from-emerald-500 to-teal-500",
    kind: "reference",
  },
  {
    label: (
      <>
        Residual <span className="math-label">α⁻¹</span>(TFPT − CODATA)
      </>
    ),
    value: "≈ 3.98 × 10⁻⁸",
    note: "Difference between theory root and recommended value",
    accent: "from-orange-500 to-amber-500",
    kind: "comparison",
    isMath: true,
  },
];

export function AlphaVisualization() {
  return (
    <div className="glass rounded-2xl ring-1 ring-slate-700/40">
      <div className="border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          Electromagnetic closure —{" "}
          <span className="math-label">α</span> as a self-consistent root
        </span>
      </div>
      <div className="grid gap-8 p-6 md:p-8 lg:grid-cols-2">
        <div className="reviewer-only">
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
          <div className="mt-3 overflow-x-auto formula-scroll rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
            <Math block>
              {String.raw`\begin{aligned}
F_{U(1)}(\alpha) \;&=\; \alpha^3 \;-\; 2 c_3^3\,\alpha^2 \\
                  &\quad -\; \tfrac{4}{5}\, c_3^6\!\left(\textstyle\sum L_{f,j} + N_\Phi\right)\log\!\left(\varphi_{\mathrm{seam}}(\alpha)^{-1}\right)
\end{aligned}`}
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
              key={c.kind}
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

      <div className="grid gap-6 border-t border-slate-800/60 p-6 md:p-8 lg:grid-cols-2">
        <AlphaRootPlot />
        <AlphaInputAudit />
      </div>
      <div className="reviewer-only border-t border-slate-800/60 p-6 md:p-8">
        <AlphaSelfConsistencyLoop />
      </div>
    </div>
  );
}

/**
 * Compact audit table that puts every input the α-closure consumes next to
 * the input it must explicitly NOT consume. The free-knob count is visible
 * at the bottom — the bar that has to read 0 for "not a fit" to mean what
 * it says.
 */
function AlphaInputAudit() {
  const ROWS: Array<{
    element: React.ReactNode;
    from: string;
    forbid: React.ReactNode;
  }> = [
    {
      element: <Math>{"c_3 = 1/(8\\pi)"}</Math>,
      from: "Paper 1 — boundary primitive",
      forbid: "CODATA fitting",
    },
    {
      element: <Math>{"b_1 = 41/10"}</Math>,
      from: "Paper 2 — abelian index coefficient",
      forbid: "Empirical post-tuning",
    },
    {
      element: <Math>{"\\textstyle\\sum L_{f,j} + N_\\Phi"}</Math>,
      from: "Paper 2 — carrier packet, Higgs index",
      forbid: "Free parameter",
    },
    {
      element: <Math>{"\\varphi_{\\mathrm{seam}}(\\alpha)"}</Math>,
      from: "Paper 3 — exact seam opening",
      forbid: <span>Freezing at <Math>{"\\varphi_0"}</Math> inside the root equation</span>,
    },
    {
      element: <span className="font-mono text-slate-200">CODATA 2022</span>,
      from: "External comparison row",
      forbid: "Being used as input",
    },
  ];

  return (
    <div className="rounded-xl border border-slate-700/40 bg-slate-950/40 p-4 sm:p-5">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h4 className="font-serif text-base font-semibold text-slate-50">
          What feeds the closure — and what must not
        </h4>
        <span className="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-emerald-200 ring-1 ring-emerald-400/30">
          Free knobs: 0
        </span>
      </div>

      <div className="mt-3 overflow-x-auto formula-scroll">
        <table className="w-full min-w-full border-separate border-spacing-0 text-left text-xs">
          <thead>
            <tr>
              <th
                scope="col"
                className="border-b border-slate-800/60 px-2 py-2 text-[10px] font-semibold uppercase tracking-widest text-slate-300"
              >
                Element
              </th>
              <th
                scope="col"
                className="border-b border-slate-800/60 px-2 py-2 text-[10px] font-semibold uppercase tracking-widest text-slate-300"
              >
                Comes from
              </th>
              <th
                scope="col"
                className="border-b border-slate-800/60 px-2 py-2 text-[10px] font-semibold uppercase tracking-widest text-slate-300"
              >
                Must not
              </th>
            </tr>
          </thead>
          <tbody>
            {ROWS.map((row, i) => (
              <tr key={i} className="hover:bg-slate-900/30">
                <td className="border-b border-slate-800/60 px-2 py-2 align-top font-mono text-slate-100">
                  {row.element}
                </td>
                <td className="border-b border-slate-800/60 px-2 py-2 align-top leading-snug text-slate-300">
                  {row.from}
                </td>
                <td className="border-b border-slate-800/60 px-2 py-2 align-top leading-snug text-rose-200/85">
                  {row.forbid}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="mt-3 text-[11px] leading-relaxed text-slate-400">
        Every quantity on the left is fixed by an upstream paper before the
        closure equation is touched. Anything in the right column would
        silently turn the α prediction into a fit.
      </p>
    </div>
  );
}
