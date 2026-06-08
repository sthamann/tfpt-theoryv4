"use client";

import { motion } from "motion/react";
import { Math } from "@/components/Math";
import { SectionHeader } from "@/components/SectionHeader";

const DECODERS = [
  {
    symbol: "g_{\\mathrm{car}} = 5",
    role: "Engine 1 — discrete closure",
    body: "From the five-slot carrier: the D₅ half-spinor, the family geometry A₃ = ℙ¹∖μ₄, the μ₄ glue to E₈, and the Standard-Model packet — N_fam = 3, Ω_adm = 48, b₁ = 41/10, and the residue matrix R with det 8.",
    formula: "g_{\\mathrm{car}} = 5 \\to E_8 \\to (N_{\\mathrm{fam}}, b_1, R)",
    accent: "from-blue-500 to-violet-500",
    border: "border-blue-400/30 bg-blue-500/5",
  },
  {
    symbol: "c_3 = \\tfrac{1}{8\\pi}",
    role: "Engine 2 — boundary dressing",
    body: "From the seam constant: the seed u = φ₀, the electromagnetic fixed point α⁻¹, the Einstein normaliser ξ, and the exponential scale grammar 1 : 5 : 10 that gives v_EW, H₀ and Λ. Gravity is this engine's geometry channel.",
    formula: "c_3 \\to (u{=}\\varphi_0,\\ \\alpha^{-1},\\ \\xi,\\ \\Lambda,\\ H_0)",
    accent: "from-emerald-500 to-teal-500",
    border: "border-emerald-400/30 bg-emerald-500/5",
  },
  {
    symbol: "E_8\\text{ closure}",
    role: "The bootstrap loop",
    body: "The E₈ closure feeds back and fixes the inputs: g_car = 5 is forced three ways (rank-fill, Coxeter-match, integer-glue), and the 8 in c₃ equals rank E₈ = h(D₅) = φ(30). Inputs and output prove each other — only π stays irreducible.",
    formula: "E_8 \\Rightarrow g_{\\mathrm{car}}{=}5,\\ 8 = \\operatorname{rank}E_8",
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
          eyebrow="The two engines"
          title="Discrete closure, boundary dressing, bootstrap"
          description="Read from the two axioms, the theory factorises into exactly two engines — a discrete closure from g_car and a boundary dressing from c₃ — and the bootstrap loop that feeds the E₈ closure back to fix the inputs."
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
