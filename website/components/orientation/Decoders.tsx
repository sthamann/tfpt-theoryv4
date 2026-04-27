"use client";

import { motion } from "motion/react";
import { Math } from "@/components/Math";
import { SectionHeader } from "@/components/SectionHeader";

const DECODERS = [
  {
    symbol: "Y",
    role: "Generates structure",
    body: "The carrier decoder Y is the determinant-normalized two-point generator on the derived split E = E_- ⊕ E_+. The ranks are forced by the compact Higgs index (dim E_+ = 2) and primitive Yukawa type (dim E_- = 3). The carrier polynomial 6Y² − Y − 1 = 0 is then the minimal polynomial of the two derived roots — a corollary, not an entry assumption.",
    formula: "Y = -\\tfrac{1}{3} P_- + \\tfrac{1}{2} P_+",
    accent: "from-blue-500 to-violet-500",
    border: "border-blue-400/30 bg-blue-500/5",
  },
  {
    symbol: "[u_\\Sigma] = 1",
    role: "Generates counting",
    body: "The primitive seam class normalization controls family counting (3), admissible occupancy (Ω_adm = 48), and the compact Higgs index (N_Φ = 1).",
    formula: "[u_\\Sigma] = 1",
    accent: "from-violet-500 to-fuchsia-500",
    border: "border-violet-400/30 bg-violet-500/5",
  },
  {
    symbol: "u := \\varphi_0",
    role: "Generates bridge observables",
    body: "After sectorization, the retained UV seed projects to the bridge observables — the Cabibbo angle, the radiative β coefficient, and the reactor angle of the PMNS matrix.",
    formula: "u := \\varphi_0",
    accent: "from-fuchsia-500 to-pink-500",
    border: "border-fuchsia-400/30 bg-fuchsia-500/5",
  },
];

export function Decoders() {
  return (
    <section
      id="decoders"
      className="relative scroll-mt-24 py-20 sm:py-24"
      aria-labelledby="decoders-heading"
    >
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="The three decoders"
          title="Structure, counting, observables"
          description="The closed branch is condensed through three decoders. Each one isolates a different burden of proof, which is why the paper series separates kernel, carrier, precision readouts, QFT closure, metrology, and cosmology."
        />

        <div className="mt-12 grid gap-5 lg:grid-cols-3">
          {DECODERS.map((d, i) => (
            <motion.article
              key={d.symbol}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.05 }}
              transition={{ duration: 0.6, delay: i * 0.1 }}
              className={`relative flex flex-col overflow-hidden rounded-2xl border p-6 ${d.border}`}
            >
              <div
                className={`absolute inset-x-0 top-0 h-px bg-gradient-to-r ${d.accent} opacity-70`}
                aria-hidden
              />
              <div className="flex h-10 items-center justify-center overflow-x-auto rounded-lg bg-slate-950/50 px-3">
                <Math>{d.symbol}</Math>
              </div>
              <p className="mt-4 text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
                {d.role}
              </p>
              <p className="mt-2 text-sm leading-relaxed text-slate-300">
                {d.body}
              </p>
              <div className="mt-4 rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
                <Math block>{d.formula}</Math>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
