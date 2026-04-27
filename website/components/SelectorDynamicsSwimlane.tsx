"use client";

import { motion } from "motion/react";
import { Math } from "./Math";

interface LaneNode {
  id: string;
  label: string;
  formula: string;
  note?: string;
}

const SELECTOR_LANE: LaneNode[] = [
  {
    id: "Pprim",
    label: "Primitive selector",
    formula: "P_{\\mathrm{prim}}",
    note: "Paper 1 — selects the primitive admissible sector",
  },
  {
    id: "Psing",
    label: "Singlet selector",
    formula: "P_{\\mathrm{sing}}",
    note: "Hadronic singlet projection",
  },
  {
    id: "PTheta",
    label: "Theta selector",
    formula: "P_\\Theta",
    note: "Determinant-line θ-projection ⇒ θ_eff = 0",
  },
  {
    id: "Padm",
    label: "Composite selector",
    formula: "P_{\\mathrm{adm}} = P_{\\mathrm{prim}}\\,P_{\\mathrm{sing}}\\,P_\\Theta",
    note: "Selects the physical admissible sector",
  },
];

const DYNAMICS_LANE: LaneNode[] = [
  {
    id: "Zrel",
    label: "Relative partition",
    formula: "Z_{\\mathrm{rel}}",
    note: "Reflection-positive starting point",
  },
  {
    id: "Sn",
    label: "Schwinger distributions",
    formula: "\\{S_n^T\\}",
    note: "Truncated correlators on the admissible sector",
  },
  {
    id: "OS",
    label: "OS reconstruction",
    formula: "(\\mathcal{H}_{\\mathrm{adm}},\\mathfrak{A}_{\\mathrm{adm}})",
    note: "Hilbert space and local algebras from positivity",
  },
  {
    id: "Net",
    label: "Local net",
    formula: "\\mathfrak{A}_{\\mathrm{adm}}(\\mathcal{O})",
    note: "Stable massive scattering",
  },
  {
    id: "Flow",
    label: "Admissible RG flow",
    formula: "\\partial_k \\Gamma_k = \\tfrac{1}{2}\\operatorname{STr}\\!\\left[(\\Gamma_k^{(2)} + R_k)^{-1}\\partial_k R_k\\right]_{\\mathrm{adm}}",
    note: "Wetterich flow restricted to the admissible sector",
  },
  {
    id: "Gren",
    label: "Renormalised observables",
    formula: "\\Gamma_{\\mathrm{TFPT}}^{\\mathrm{ren}}",
    note: "Output of the dynamics, fed into the observable functor",
  },
];

export function SelectorDynamicsSwimlane() {
  return (
    <div className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          Selector vs. dynamics — two parallel lanes
        </span>
        <span className="rounded-full bg-amber-500/15 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-amber-200 ring-1 ring-amber-400/30">
          Paper 4 · admissibility / QFT closure
        </span>
      </div>

      <div className="grid gap-6 p-6 md:p-8 lg:grid-cols-2">
        <Lane
          title="Selector lane"
          subtitle="Projects out the physical admissible sector"
          accent="from-blue-500 to-violet-500"
          chip="bg-blue-500/15 text-blue-200 ring-blue-400/30"
          nodes={SELECTOR_LANE}
        />
        <Lane
          title="Dynamics lane"
          subtitle="Evolves the admissible sector — does not select it"
          accent="from-emerald-500 to-teal-500"
          chip="bg-emerald-500/15 text-emerald-200 ring-emerald-400/30"
          nodes={DYNAMICS_LANE}
        />
      </div>

      <div className="border-t border-slate-800/60 px-6 py-4 sm:px-8">
        <p className="text-xs leading-relaxed text-slate-400">
          <strong className="text-slate-200">Why this is two lanes, not one chain.</strong>{" "}
          The selector{" "}
          <Math>{"P_{\\mathrm{adm}}"}</Math>{" "}
          decides <em>which sector</em> the theory is about. The dynamics
          carries{" "}
          <em>what the sector does</em>: positivity, OS reconstruction, local
          net, scattering, exact admissible flow. Conflating the two is the
          easiest way to read more physics into a projector than it actually
          carries.
        </p>
      </div>
    </div>
  );
}

function Lane({
  title,
  subtitle,
  accent,
  chip,
  nodes,
}: {
  title: string;
  subtitle: string;
  accent: string;
  chip: string;
  nodes: LaneNode[];
}) {
  return (
    <div className="rounded-2xl border border-slate-800/60 bg-slate-950/40">
      <div className="flex items-center justify-between border-b border-slate-800/60 px-4 py-3">
        <div>
          <div className={`inline-block rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest ring-1 ${chip}`}>
            {title}
          </div>
          <p className="mt-1 text-xs text-slate-400">{subtitle}</p>
        </div>
      </div>
      <ol className="space-y-2 p-4">
        {nodes.map((n, i) => (
          <motion.li
            key={n.id}
            initial={{ opacity: 0, x: -10 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, amount: 0.05 }}
            transition={{ duration: 0.4, delay: i * 0.06 }}
            className="relative rounded-xl border border-slate-700/40 bg-slate-950/60 p-3"
          >
            <div
              aria-hidden="true"
              className={`absolute inset-x-0 top-0 h-px bg-gradient-to-r ${accent} opacity-70`}
            />
            <div className="text-[10px] font-semibold uppercase tracking-widest text-slate-300">
              {n.label}
            </div>
            <div className="mt-1 overflow-x-auto formula-scroll">
              <Math block>{n.formula}</Math>
            </div>
            {n.note && (
              <p className="mt-1 text-[11px] leading-snug text-slate-400">
                {n.note}
              </p>
            )}
            {i < nodes.length - 1 && (
              <div
                aria-hidden
                className="mx-auto mt-2 h-3 w-px bg-gradient-to-b from-slate-600/40 via-slate-500/30 to-slate-600/40"
              />
            )}
          </motion.li>
        ))}
      </ol>
    </div>
  );
}
