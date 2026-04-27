"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { Download, FileText } from "lucide-react";
import { papers, STATUS_META } from "@/lib/papers";
import { cn } from "@/lib/utils";
import { SectionHeader } from "./SectionHeader";

const COMPANIONS = [
  {
    label: "Series index",
    desc: "Index of the dedicated TFPT 4.5 split, organized by burden of proof.",
    href: "/papers/series_index.pdf",
  },
  {
    label: "Theory map",
    desc: "Status map of the staged derivation chain — theorem-core, bridge, conditional, downstream.",
    href: "/papers/theory_map.pdf",
  },
  {
    label: "Technical companion",
    desc: "Conventions, positivity, APS interfaces, comparison maps, and downstream continuations.",
    href: "/papers/technical_companion.pdf",
  },
  {
    label: "Coverage audit",
    desc: "Audit of which sections of the source draft are covered, and where.",
    href: "/papers/coverage_audit.pdf",
  },
  {
    label: "Two-page summary",
    desc: "One-page claim, one-page predictions — for fast review.",
    href: "/predictions/tfpt_two_page_summary.pdf",
  },
];

export function DownloadsSection() {
  return (
    <section
      id="downloads"
      className="relative scroll-mt-20 py-24 sm:py-32"
      aria-labelledby="downloads-heading"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="Downloads"
          title="Every PDF, in one place"
          description="The full TFPT 4.5 paper series, the technical companion, the theory status map, and the two-page executive summary — all distributed for academic use."
        />

        <div className="mt-12">
          <h3 className="font-serif text-lg font-semibold text-slate-100">
            Paper series
          </h3>
          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {papers.map((p, i) => {
              const meta = STATUS_META[p.status];
              return (
                <motion.div
                  key={p.id}
                  initial={{ opacity: 0, y: 12 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.05 }}
                  transition={{ duration: 0.5, delay: i * 0.05 }}
                  className="group glass relative flex flex-col overflow-hidden rounded-xl ring-1 ring-slate-700/40 transition-all hover:ring-slate-500/60"
                >
                  <div
                    className={cn(
                      "absolute inset-x-0 top-0 h-px",
                      p.status === "core"
                        ? "bg-gradient-to-r from-blue-500 to-violet-500"
                        : p.status === "bridge"
                          ? "bg-gradient-to-r from-emerald-500 to-teal-500"
                          : p.status === "conditional"
                            ? "bg-gradient-to-r from-orange-500 to-red-500"
                            : "bg-gradient-to-r from-fuchsia-500 to-pink-500",
                    )}
                  />
                  <div className="flex flex-1 flex-col p-5">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="rounded-full border border-slate-600/40 bg-slate-900/50 px-2.5 py-0.5 font-mono text-[10px] font-semibold uppercase tracking-widest text-slate-300">
                        Paper {p.number}
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
                    <h4 className="mt-3 font-serif text-base font-semibold leading-snug text-slate-50">
                      {p.title}
                    </h4>
                    <p className="mt-1 text-xs leading-relaxed text-slate-400">
                      {p.subtitle}
                    </p>
                    <div className="mt-auto flex items-center gap-3 pt-4">
                      <Link
                        href={p.pdf}
                        target="_blank"
                        rel="noopener"
                        className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-300 transition-colors hover:text-blue-200"
                      >
                        <Download size={13} />
                        Download
                      </Link>
                      <Link
                        href={p.pdf}
                        target="_blank"
                        rel="noopener"
                        className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-300 transition-colors hover:text-slate-100"
                      >
                        <FileText size={13} />
                        View
                      </Link>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>

        <div className="mt-14">
          <h3 className="font-serif text-lg font-semibold text-slate-100">
            Companion documents
          </h3>
          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {COMPANIONS.map((c, i) => (
              <motion.div
                key={c.label}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.05 }}
                transition={{ duration: 0.5, delay: i * 0.05 }}
                className="rounded-xl border border-slate-700/40 bg-slate-950/40 p-5 transition-colors hover:bg-slate-900/40"
              >
                <h4 className="font-serif text-base font-semibold text-slate-100">
                  {c.label}
                </h4>
                <p className="mt-2 text-xs leading-relaxed text-slate-400">{c.desc}</p>
                <Link
                  href={c.href}
                  target="_blank"
                  rel="noopener"
                  className="mt-3 inline-flex items-center gap-1.5 text-xs font-semibold text-blue-300 transition-colors hover:text-blue-200"
                >
                  <Download size={13} />
                  Download PDF
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
