"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { Download, ArrowRight } from "lucide-react";
import { SectionHeader } from "@/components/SectionHeader";
import { papers, STATUS_META } from "@/lib/papers";
import { cn } from "@/lib/utils";
import { trackPdfInteraction } from "@/lib/track";

export function SeriesMap() {
  return (
    <section
      id="series-map"
      className="relative scroll-mt-24 py-20 sm:py-24"
      aria-labelledby="series-map-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="Document map"
          title="Five core papers plus four companions"
          description="The reviewer path is the architecture, the two axioms, the E₈ glue and the α fixed point (Doc 1), the Standard Model (Doc 2), the E₈ audit and bootstrap (Doc 3), the honest frontier (Doc 4), and the adversarial Red Team audit (Doc 5). Appendix H (horizon), the Origin Theory synthesis, the research contracts, and the safeguards discipline sit alongside."
        />

        <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {papers
            .filter((p) => p.number > 0)
            .map((p, i) => {
              const meta = STATUS_META[p.status];
              return (
                <motion.article
                  key={p.id}
                  initial={{ opacity: 0, y: 12 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.05 }}
                  transition={{ duration: 0.5, delay: i * 0.06 }}
                  className="group glass relative flex flex-col overflow-hidden rounded-2xl ring-1 ring-slate-700/40 transition-all hover:ring-slate-500/60"
                >
                  <div
                    className={cn(
                      "absolute inset-x-0 top-0 h-px bg-gradient-to-r",
                      meta.gradient,
                    )}
                  />
                  <div className="flex flex-1 flex-col p-6">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="rounded-full border border-slate-600/40 bg-slate-900/50 px-2.5 py-0.5 font-mono text-[10px] font-semibold uppercase tracking-widest text-slate-300">
                        Doc {p.number}
                      </span>
                      <span
                        className={cn(
                          "rounded-full px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest ring-1",
                          meta.bg,
                          meta.color,
                          meta.ring,
                        )}
                      >
                        {meta.label}
                      </span>
                    </div>
                    <h3 className="mt-4 font-serif text-lg font-semibold leading-snug text-slate-50">
                      {p.title}
                    </h3>
                    <p className="mt-2 text-sm leading-relaxed text-slate-400">
                      {p.subtitle}
                    </p>
                    <div className="mt-auto flex flex-wrap items-center gap-3 pt-5">
                      <Link
                        href={p.pdf}
                        target="_blank"
                        rel="noopener"
                        onClick={() =>
                          trackPdfInteraction({
                            file: p.pdf,
                            source: "series-map",
                            kind: "paper",
                            interaction: "download",
                            title: p.title,
                          })
                        }
                        className="inline-flex items-center gap-1.5 rounded-full bg-blue-500/15 px-3 py-1.5 text-xs font-semibold text-blue-200 ring-1 ring-blue-400/30 transition-colors hover:bg-blue-500/25"
                      >
                        <Download size={13} />
                        Download
                      </Link>
                      <Link
                        href={`/papers/${p.slug}`}
                        className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-300 transition-colors hover:text-white"
                      >
                        Open in detail
                        <ArrowRight size={13} />
                      </Link>
                    </div>
                  </div>
                </motion.article>
              );
            })}
        </div>
      </div>
    </section>
  );
}
