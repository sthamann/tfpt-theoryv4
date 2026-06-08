"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { Math } from "./Math";

interface Gate {
  tag: string;
  marker: string;
  title: string;
  body: string;
  formula?: string;
  tone: string;
}

const GATES: Gate[] = [
  {
    tag: "Research gate 1",
    marker: "[A]",
    title: "(U_wall) — the flavor amplitude scale",
    body: "The quark mass ratios are closed (Readout Rigidity, c_u/c_d = 55/117 on the discrete selector stratum). Only the absolute amplitude normalisation U_point stays open — finite, algebraic and falsifiable.",
    formula: "\\det R = 8, \\ \\operatorname{Spec}(Q_+)=\\{1,2,3\\} \\ \\text{fixed};\\ U_{\\mathrm{point}}\\ \\text{open}",
    tone: "border-amber-400/30 bg-amber-500/5",
  },
  {
    tag: "Research gate 2",
    marker: "[A]",
    title: "(G_metric) — the quantum-gravity measure",
    body: "R + R² is heat-kernel grounded (G2) and the admissible IR sector is gap-decoupled (G5, Δ_eff = 1.648 > 0). The ambient projective limit G6 remains open — so a strict physical TOE is not certified.",
    formula: "2\\|V\\| = 0.785 < \\Delta = 6\\log\\tfrac{3}{2};\\ \\ G_6\\ \\text{open}",
    tone: "border-amber-400/30 bg-amber-500/5",
  },
  {
    tag: "Not a gate",
    marker: "[P]/[A]",
    title: "Frontier interfaces — explicitly not compiler powers",
    body: "Koide (near-miss), η_B (downstream readout), the axion relic scale, and m_p/m_e are honestly typed interfaces. They are deliberately not claimed as forced compiler outputs.",
    tone: "border-slate-500/30 bg-slate-500/5",
  },
];

/**
 * Trust section: what is still open. The research contracts name exactly two
 * genuine gates plus a set of typed frontier interfaces — surfacing this near
 * the top is a credibility signal, not a footnote.
 */
export function OpenGates() {
  return (
    <section
      id="open-gates"
      className="relative scroll-mt-20 py-20 sm:py-24"
      aria-labelledby="open-gates-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="Honest boundaries"
          title="What is still open?"
          description="After the compiler closure the entire residual is Rest = (U_wall) ⊕ (G_metric) ⊕ (F_frontier): one flavor wall-selection, one quantum-gravity measure, and a set of deliberately typed frontier interfaces. None of these is hidden, and none is overclaimed."
        />

        <div className="mt-10 grid gap-5 lg:grid-cols-3">
          {GATES.map((g, i) => (
            <motion.article
              key={g.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.05 }}
              transition={{ duration: 0.55, delay: i * 0.08 }}
              className={`flex flex-col rounded-2xl border p-6 ${g.tone}`}
            >
              <div className="flex items-center gap-2">
                <span className="rounded-full border border-slate-600/40 bg-slate-900/50 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-slate-300">
                  {g.tag}
                </span>
                <span className="rounded-full bg-rose-500/15 px-2 py-0.5 font-mono text-[10px] font-semibold text-rose-200 ring-1 ring-rose-400/30">
                  {g.marker}
                </span>
              </div>
              <h3 className="mt-3 font-serif text-base font-semibold text-slate-50">
                {g.title}
              </h3>
              <p className="mt-2 flex-1 text-sm leading-relaxed text-slate-300">
                {g.body}
              </p>
              {g.formula && (
                <div className="mt-3 overflow-x-auto rounded-lg border border-slate-700/40 bg-slate-950/40 p-2.5">
                  <Math block>{g.formula}</Math>
                </div>
              )}
            </motion.article>
          ))}
        </div>

        <div className="mt-6 flex flex-wrap items-center gap-3 text-sm text-slate-400">
          <span>The gates are written up as numbered research contracts.</span>
          <Link
            href="/papers/research-contracts"
            className="inline-flex items-center gap-1.5 font-semibold text-blue-300 transition-colors hover:text-blue-200"
          >
            Read the contracts
            <ArrowRight size={14} aria-hidden />
          </Link>
        </div>
      </div>
    </section>
  );
}
