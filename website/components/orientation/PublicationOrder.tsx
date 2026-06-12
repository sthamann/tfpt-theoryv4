"use client";

import { motion } from "motion/react";
import { ArrowRight } from "lucide-react";
import { SectionHeader } from "@/components/SectionHeader";

const PUBLIC_ORDER = [
  { n: 0, label: "Introduction", note: "Reading guide & status assessment" },
  { n: 1, label: "Architecture & E₈", note: "Two axioms, the glue, α⁻¹" },
  { n: 2, label: "Standard Model", note: "The φ₀-ladder & flavor matrix" },
  { n: 3, label: "E₈ audit & bootstrap", note: "Audit raster, the loop" },
  { n: 4, label: "Frontier", note: "Honest open items" },
  { n: 6, label: "Origin Theory", note: "Why no free number remains" },
  { n: 7, label: "Research contracts", note: "The open interfaces v_geo, G_net, F_transfer" },
];

const MATH_ORDER = [
  { n: 1, label: "Architecture: the two axioms, D₅ × A₃ → E₈, α⁻¹" },
  { n: 2, label: "Standard Model: the φ₀-ladder, flavor matrix, θ₁₂" },
  { n: 3, label: "E₈ audit raster, cascade bridge, Möbius bootstrap" },
  { n: 4, label: "Frontier: η_B, m_p/m_e, Koide, dark matter, QG" },
  { n: 5, label: "Appendix H — horizon unit system (reframe)" },
  { n: 6, label: "Origin Theory — the gapped unique attractor" },
];

export function PublicationOrder() {
  return (
    <section
      id="publication-order"
      className="relative scroll-mt-24 py-20 sm:py-24"
      aria-labelledby="publication-order-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="Reading order"
          title="Two paths through the same set"
          description="The dependency order of the four core documents is rigid (1 → 2 → 3 → 4). The recommended reading order starts from the introduction and adds the three companions — Appendix H, the Origin Theory synthesis, and the research contracts — without breaking the chain."
        />

        <div className="mt-12 grid gap-6 lg:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.05 }}
            transition={{ duration: 0.6 }}
            className="glass rounded-2xl ring-1 ring-blue-400/20"
          >
            <div className="flex items-center gap-2 border-b border-slate-800/60 px-5 py-3">
              <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
                Recommended public order
              </span>
            </div>
            <ol className="space-y-3 p-5">
              {PUBLIC_ORDER.map((p, i) => (
                <li
                  key={p.n}
                  className="flex items-center gap-4 rounded-xl border border-slate-800/40 bg-slate-950/40 px-4 py-3 transition-colors hover:bg-slate-900/40"
                >
                  <span className="flex h-8 w-8 flex-none items-center justify-center rounded-lg bg-gradient-to-br from-blue-500/30 to-violet-500/30 font-mono text-xs font-semibold text-blue-100 ring-1 ring-blue-400/30">
                    {p.n}
                  </span>
                  <div className="flex-1">
                    <div className="font-serif text-sm font-semibold text-slate-100">
                      Doc {p.n} — {p.label}
                    </div>
                    <div className="text-xs text-slate-400">{p.note}</div>
                  </div>
                  {i < PUBLIC_ORDER.length - 1 && (
                    <ArrowRight
                      size={14}
                      className="flex-none text-slate-600"
                      aria-hidden
                    />
                  )}
                </li>
              ))}
            </ol>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.05 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="glass rounded-2xl ring-1 ring-emerald-400/20"
          >
            <div className="flex items-center gap-2 border-b border-slate-800/60 px-5 py-3">
              <span className="text-[11px] font-semibold uppercase tracking-widest text-emerald-300/80">
                Mathematical dependency order
              </span>
            </div>
            <ol className="space-y-3 p-5">
              {MATH_ORDER.map((p, i) => (
                <li
                  key={p.n}
                  className="flex items-center gap-4 rounded-xl border border-slate-800/40 bg-slate-950/40 px-4 py-3 transition-colors hover:bg-slate-900/40"
                >
                  <span className="flex h-8 w-8 flex-none items-center justify-center rounded-lg bg-gradient-to-br from-emerald-500/30 to-teal-500/30 font-mono text-xs font-semibold text-emerald-100 ring-1 ring-emerald-400/30">
                    {p.n}
                  </span>
                  <div className="flex-1">
                    <div className="font-serif text-sm font-semibold text-slate-100">
                      Doc {p.n} — {p.label}
                    </div>
                  </div>
                  {i < MATH_ORDER.length - 1 && (
                    <ArrowRight
                      size={14}
                      className="flex-none text-slate-600"
                      aria-hidden
                    />
                  )}
                </li>
              ))}
            </ol>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
