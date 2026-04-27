"use client";

import { motion, useInView } from "motion/react";
import { useRef } from "react";
import { Math } from "./Math";
import { SectionHeader } from "./SectionHeader";

const NODES = [
  {
    id: "seed",
    layer: 1,
    label: "Operational seed",
    formula: "\\mathfrak{S}_{\\min}",
    note: "Pre-physical primitive",
    tone: "from-blue-500 to-blue-400",
  },
  {
    id: "boundary",
    layer: 1,
    label: "Boundary datum",
    formula: "\\mathcal{B}_{\\min} \\to \\mathfrak{T}_\\partial",
    note: "One-sided datum",
    tone: "from-blue-500 to-cyan-400",
  },
  {
    id: "kernel",
    layer: 2,
    label: "Primitive kernel",
    formula: "(\\tau_{\\mathrm{dbl}},\\iota_C,P_{\\mathrm{prim}},[u_\\Sigma],c_3)",
    note: "Paper 1 — boundary primitive",
    tone: "from-blue-500 to-violet-500",
  },
  {
    id: "carrier",
    layer: 3,
    label: "Carrier rigidity",
    formula:
      "\\begin{aligned}\\varepsilon_{\\mathrm{car}} &\\Rightarrow (\\dim E_-,\\dim E_+)=(3,2) \\\\ &\\Rightarrow 6Y^2 - Y - \\mathbf{1} = 0\\end{aligned}",
    note: "Paper 2 — derived; polynomial is corollary",
    tone: "from-violet-500 to-fuchsia-500",
  },
  {
    id: "alpha",
    layer: 4,
    label: "EM closure",
    formula: "\\alpha^{-1}(0) = 137.0359992",
    note: "Paper 3 — precision readout",
    tone: "from-emerald-500 to-teal-500",
  },
  {
    id: "qft",
    layer: 5,
    label: "Admissibility",
    formula: "P_{\\mathrm{adm}} = P_{\\mathrm{prim}} P_{\\mathrm{sing}} P_\\Theta",
    note: "Paper 4 — conditional QFT closure",
    tone: "from-orange-500 to-red-500",
  },
  {
    id: "metrology",
    layer: 6,
    label: "Metrology",
    formula: "G_N \\lambda_\\Sigma^2 = \\dfrac{\\pi}{4\\rho_\\star}",
    note: "Paper 5 — boundary-normalized observables",
    tone: "from-cyan-500 to-emerald-500",
  },
  {
    id: "cosmo",
    layer: 7,
    label: "Cosmology interfaces",
    formula: "N_{\\mathrm{DW}} = 1 \\;\\;|\\;\\; \\Sigma m_\\nu, \\eta_B, m_a",
    note: "Paper 6 — downstream targets",
    tone: "from-fuchsia-500 to-pink-500",
  },
];

export function ReconstructionChain() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, amount: 0.05 });

  return (
    <section
      id="chain"
      className="relative scroll-mt-20 py-24 sm:py-32"
      aria-labelledby="chain-heading"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="The staged reconstruction"
          title="From boundary to observable closure"
          description="TFPT is organized as a layered derivation chain. Each step is a theorem, a bridge readout, a conditional closure, or a downstream interface — never a fit. The status discipline is part of the proof."
        />

        <div ref={ref} className="relative mx-auto mt-16 max-w-4xl">
          <div
            className="absolute left-1/2 top-0 hidden h-full w-px -translate-x-1/2 bg-gradient-to-b from-transparent via-slate-600/40 to-transparent md:block"
            aria-hidden="true"
          />

          <ol className="space-y-6">
            {NODES.map((n, idx) => {
              const isEven = idx % 2 === 0;
              return (
                <motion.li
                  key={n.id}
                  initial={{ opacity: 0, y: 32 }}
                  animate={inView ? { opacity: 1, y: 0 } : {}}
                  transition={{ duration: 0.7, delay: idx * 0.08, ease: [0.16, 1, 0.3, 1] }}
                  className={`relative flex w-full ${
                    isEven ? "md:justify-start" : "md:justify-end"
                  }`}
                >
                  <span
                    className="absolute left-1/2 top-8 z-10 hidden h-3 w-3 -translate-x-1/2 rounded-full bg-slate-100 ring-4 ring-slate-900 md:block"
                    aria-hidden="true"
                  />

                  <div
                    className={`group glass relative w-full overflow-hidden rounded-2xl ring-1 ring-slate-700/40 transition-shadow hover:ring-slate-500/50 md:w-[calc(50%-2.5rem)] ${
                      isEven ? "md:mr-auto" : "md:ml-auto"
                    }`}
                  >
                    <div
                      aria-hidden="true"
                      className={`absolute inset-x-0 top-0 h-px bg-gradient-to-r ${n.tone} opacity-60`}
                    />

                    <div className="px-5 py-5 sm:px-6 sm:py-6">
                      <div className="flex items-center gap-3">
                        <span
                          className={`flex h-8 w-8 flex-none items-center justify-center rounded-full bg-gradient-to-br ${n.tone} font-mono text-xs font-semibold text-white shadow-md`}
                        >
                          {n.layer}
                        </span>
                        <h3 className="font-serif text-lg font-semibold text-slate-50">
                          {n.label}
                        </h3>
                      </div>
                      <div className="mt-3 overflow-x-auto">
                        <Math block>{n.formula}</Math>
                      </div>
                      <p className="mt-2 text-xs uppercase tracking-widest text-slate-400">
                        {n.note}
                      </p>
                    </div>
                  </div>
                </motion.li>
              );
            })}
          </ol>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.05 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="mx-auto mt-16 max-w-4xl rounded-2xl border border-amber-400/20 bg-amber-500/5 px-6 py-5 text-sm text-amber-100/90"
        >
          <strong className="font-semibold text-amber-200">Status discipline.</strong>
          <span className="ml-2 text-amber-100/85">
            The map separates theorem-core, bridge, conditional closure, and
            downstream/programmatic layers. It is a status map of the derivation
            chain, not a claim that all displayed outputs have the same proof
            status.
          </span>
        </motion.div>
      </div>
    </section>
  );
}
