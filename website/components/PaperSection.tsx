"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { Download, FileText } from "lucide-react";
import { Math } from "./Math";
import { Paper, STATUS_META } from "@/lib/papers";
import { cn } from "@/lib/utils";
import { trackPdfInteraction } from "@/lib/track";

/**
 * Detects whether a label contains math/Greek symbols that should not be
 * uppercased. CSS `text-transform: uppercase` rewrites lowercase Greek
 * letters to uppercase Greek (α → Α, θ → Θ), which is wrong for symbols.
 */
const MATH_LABEL_RE =
  /[\u0370-\u03FF\u00B9\u00B2\u00B3⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉ξφθαβγδεζηικλμνπρστυχψωΣΞΦΘΛΠΩΓΔ\[\]√⁻⁺×⋅·]/;
const isMathLabel = (s: string) => MATH_LABEL_RE.test(s);

export function PaperSection({ paper }: { paper: Paper }) {
  const meta = STATUS_META[paper.status];
  const isEven = paper.number % 2 === 0;

  return (
    <article
      id={`paper-${paper.id}`}
      className="relative scroll-mt-20 border-b border-slate-800/40 py-24 first:pt-0 sm:py-32"
      aria-labelledby={`paper-${paper.id}-title`}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div
          className={cn(
            "grid gap-12 lg:grid-cols-12 lg:gap-16",
            isEven ? "" : "lg:[&>div:first-child]:order-2",
          )}
        >
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.05 }}
            transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
            className="lg:col-span-7"
          >
            <div className="flex flex-wrap items-center gap-3">
              <span
                className={cn(
                  "rounded-full px-3 py-1 text-xs font-semibold ring-1",
                  meta.bg,
                  meta.color,
                  meta.ring,
                )}
              >
                Paper {paper.number}
              </span>
              <span
                className={cn(
                  "rounded-full px-3 py-1 text-xs font-medium ring-1",
                  meta.bg,
                  meta.color,
                  meta.ring,
                )}
              >
                {meta.label}
              </span>
            </div>

            <h2
              id={`paper-${paper.id}-title`}
              className="mt-5 font-serif text-3xl font-semibold leading-tight text-slate-50 sm:text-4xl md:text-5xl"
            >
              {paper.title}
            </h2>
            <p className="mt-2 text-lg text-slate-400">{paper.subtitle}</p>

            <p className="mt-6 max-w-3xl text-base leading-relaxed text-slate-300">
              {paper.abstract}
            </p>

            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              <FrontBox
                title="Inputs"
                tone="ring-blue-400/20 bg-blue-500/5"
                items={paper.inputs}
              />
              <FrontBox
                title="Contribution"
                tone="ring-emerald-400/20 bg-emerald-500/5"
                items={paper.contribution}
              />
              <FrontBox
                title="Not claimed here"
                tone="ring-slate-500/20 bg-slate-500/5"
                items={paper.notClaimed}
              />
              <FrontBox
                title="Falsification surface"
                tone="ring-orange-400/20 bg-orange-500/5"
                items={paper.falsification}
              />
            </div>

            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                href={paper.pdf}
                target="_blank"
                rel="noopener"
                onClick={() =>
                  trackPdfInteraction({
                    file: paper.pdf,
                    source: "papers-detail",
                    kind: "paper",
                    interaction: "download",
                    title: paper.title,
                  })
                }
                className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
              >
                <Download size={16} />
                Download Paper {paper.number}
              </Link>
              <Link
                href={paper.pdf}
                target="_blank"
                rel="noopener"
                onClick={() =>
                  trackPdfInteraction({
                    file: paper.pdf,
                    source: "papers-detail",
                    kind: "paper",
                    interaction: "view",
                    title: paper.title,
                  })
                }
                className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/40 px-5 py-2.5 text-sm font-semibold text-slate-100 backdrop-blur transition-colors hover:bg-slate-800/60"
              >
                <FileText size={16} />
                View PDF
              </Link>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.05 }}
            transition={{ duration: 0.8, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
            className="lg:col-span-5"
          >
            <div className="glass sticky top-24 rounded-2xl ring-1 ring-slate-700/40">
              <div className="flex items-center gap-2 border-b border-slate-800/60 px-5 py-3">
                <span className="text-[11px] font-semibold uppercase tracking-widest text-slate-300">
                  Highlights
                </span>
              </div>
              <div className="grid grid-cols-2 gap-px bg-slate-800/60">
                {paper.highlights.map((h) => (
                  <div
                    key={h.label}
                    className="flex flex-col gap-1 bg-slate-950/40 px-4 py-4 transition-colors hover:bg-slate-900/60"
                  >
                    <span
                      className={cn(
                        "text-[10px] font-semibold tracking-widest text-blue-300/80",
                        isMathLabel(h.label) ? "math-label" : "uppercase",
                      )}
                    >
                      {h.label}
                    </span>
                    <span className="font-serif text-xl font-semibold text-slate-50 sm:text-2xl">
                      {h.value}
                    </span>
                    <span className="text-[11px] leading-snug text-slate-400">
                      {h.description}
                    </span>
                  </div>
                ))}
              </div>

              <div className="border-t border-slate-800/60 p-5">
                <h3 className="text-[11px] font-semibold uppercase tracking-widest text-slate-300">
                  Key formulas
                </h3>
                <ul className="mt-3 space-y-3">
                  {paper.keyFormulas.map((f) => (
                    <li
                      key={f.label}
                      className="rounded-lg border border-slate-800/60 bg-slate-950/40 p-3"
                    >
                      <div
                        className={cn(
                          "text-[11px] font-semibold tracking-widest text-blue-300/80",
                          isMathLabel(f.label) ? "math-label" : "uppercase",
                        )}
                      >
                        {f.label}
                      </div>
                      <div className="mt-1 overflow-x-auto">
                        <Math block>{f.latex}</Math>
                      </div>
                      {f.description && (
                        <div className="mt-1 text-[11px] leading-snug text-slate-400">
                          {f.description}
                        </div>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.05 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="mt-12 grid gap-6 lg:grid-cols-2"
        >
          {paper.sections.map((s) => (
            <div
              key={s.title}
              className="group glass relative overflow-hidden rounded-2xl ring-1 ring-slate-800/60 transition-shadow hover:ring-slate-600/50"
            >
              <div className="px-6 py-6">
                <h3 className="font-serif text-lg font-semibold text-slate-50">
                  {s.title}
                </h3>
                <p className="mt-3 text-sm leading-relaxed text-slate-300">{s.body}</p>
                {s.formulas && s.formulas.length > 0 && (
                  <div className="mt-4 space-y-2 border-t border-slate-800/60 pt-4">
                    {s.formulas.map((f, i) => (
                      <div key={i} className="overflow-x-auto">
                        <Math block>{f}</Math>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </article>
  );
}

function FrontBox({
  title,
  tone,
  items,
}: {
  title: string;
  tone: string;
  items: string[];
}) {
  return (
    <div className={cn("rounded-xl border-0 px-4 py-4 ring-1", tone)}>
      <div className="text-[10px] font-semibold uppercase tracking-widest text-slate-300/90">
        {title}
      </div>
      <ul className="mt-2 space-y-1.5 text-xs leading-relaxed text-slate-300">
        {items.map((it, i) => (
          <li key={i} className="flex gap-2">
            <span className="mt-0.5 text-slate-500">›</span>
            <span>{it}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
