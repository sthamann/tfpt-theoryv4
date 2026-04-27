"use client";

import { motion } from "motion/react";
import { ArrowRight } from "lucide-react";
import { SectionHeader } from "@/components/SectionHeader";

const PUBLIC_ORDER = [
  { n: 0, label: "Orientation", note: "Public entry document" },
  { n: 2, label: "Carrier rigidity", note: "First visible core result" },
  { n: 1, label: "Boundary kernel", note: "Formal foundation backbone" },
  { n: 3, label: "EM closure", note: "Precision prediction layer" },
  { n: 4, label: "QFT closure", note: "Analytic stabilization" },
  { n: 5, label: "Metrology", note: "Dimensionless metrology" },
  { n: 6, label: "Cosmology", note: "Downstream expansion" },
];

const MATH_ORDER = [
  { n: 1, label: "Boundary primitive kernel" },
  { n: 2, label: "Carrier rigidity & SM packet" },
  { n: 3, label: "EM and flavor readouts" },
  { n: 4, label: "Admissibility, strong CP, OS / scattering" },
  { n: 5, label: "Geometric branch & metrology" },
  { n: 6, label: "Downstream cosmology interfaces" },
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
          title="Two paths through the same theory"
          description="The mathematical dependency order is rigid. The recommended public order uses Paper 2 as the visible hook and Paper 0 as the discipline document — without breaking the dependency chain."
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
                      Paper {p.n} — {p.label}
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
                      Paper {p.n} — {p.label}
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
