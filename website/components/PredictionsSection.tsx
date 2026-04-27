"use client";

import { useState } from "react";
import { motion } from "motion/react";
import Link from "next/link";
import { Download } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { PredictionCard } from "./PredictionCard";
import { predictions, Prediction, CATEGORY_META } from "@/lib/predictions";
import { cn } from "@/lib/utils";
import { trackPdfDownload } from "@/lib/track";

const TWO_PAGE_SUMMARY = "/predictions/tfpt_two_page_summary.pdf";

const FILTERS: { id: Prediction["category"] | "All"; label: string }[] = [
  { id: "All", label: "All predictions" },
  { id: "Coupling", label: "Couplings" },
  { id: "Flavor", label: "Flavor" },
  { id: "Neutrino", label: "Neutrino" },
  { id: "QCD/EDM", label: "QCD / EDM" },
  { id: "Cosmology", label: "Cosmology" },
  { id: "Higgs", label: "Higgs" },
  { id: "Astrophysics", label: "Astrophysics" },
];

export function PredictionsSection() {
  const [filter, setFilter] = useState<Prediction["category"] | "All">("All");
  const list =
    filter === "All" ? predictions : predictions.filter((p) => p.category === filter);

  const counts = predictions.reduce<Record<string, number>>((acc, p) => {
    acc[p.category] = (acc[p.category] || 0) + 1;
    return acc;
  }, {});

  return (
    <section
      id="predictions"
      className="relative scroll-mt-20 py-24 sm:py-32"
      aria-labelledby="predictions-heading"
    >
      <div
        aria-hidden="true"
        className="absolute inset-0 -z-10"
        style={{
          background:
            "radial-gradient(ellipse 60% 40% at 50% 0%, rgba(99,102,241,0.08), transparent 60%)",
        }}
      />
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="The prediction surface"
          title="Sharp, falsifiable readouts"
          description="Every row below is a single closed-branch readout with an explicit dependency class and a stated kill or pressure criterion. Each entry has its own dedicated standalone paper for review and submission."
        />

        <div className="mt-6 grid gap-3 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-4 xl:grid-cols-8">
          <div className="glass flex flex-col rounded-xl px-4 py-3 ring-1 ring-slate-700/40">
            <span className="text-[10px] font-semibold uppercase tracking-widest text-slate-400">
              Total
            </span>
            <span className="font-serif text-2xl font-semibold text-slate-50">
              {predictions.length}
            </span>
          </div>
          {(Object.keys(CATEGORY_META) as Prediction["category"][]).map((c) => (
            <button
              key={c}
              onClick={() => setFilter(c)}
              type="button"
              className={cn(
                "glass relative flex flex-col rounded-xl px-4 py-3 text-left ring-1 transition-colors",
                filter === c
                  ? "ring-blue-400/50 bg-blue-500/10"
                  : "ring-slate-700/40 hover:ring-slate-500/60",
              )}
            >
              <span className="text-[10px] font-semibold uppercase tracking-widest text-slate-400">
                {CATEGORY_META[c].label}
              </span>
              <span className="font-serif text-xl font-semibold text-slate-50">
                {counts[c] || 0}
              </span>
            </button>
          ))}
        </div>

        <div className="mt-8 flex flex-wrap gap-2">
          {FILTERS.map((f) => (
            <button
              key={f.id}
              type="button"
              onClick={() => setFilter(f.id)}
              className={cn(
                "rounded-full px-4 py-1.5 text-xs font-medium transition-colors ring-1",
                filter === f.id
                  ? "bg-blue-500 text-white ring-blue-400/40 shadow-md shadow-blue-500/20"
                  : "bg-slate-900/40 text-slate-300 ring-slate-700/40 hover:bg-slate-800/60",
              )}
              aria-pressed={filter === f.id}
            >
              {f.label}
            </button>
          ))}
        </div>

        <motion.div
          layout
          className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3"
        >
          {list.map((p, i) => (
            <PredictionCard key={p.id} prediction={p} index={i} />
          ))}
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.05 }}
          transition={{ duration: 0.6 }}
          className="mt-12 flex flex-col items-center gap-4 rounded-2xl border border-slate-700/40 bg-slate-950/40 p-8 text-center"
        >
          <h3 className="font-serif text-xl font-semibold text-slate-50">
            Want everything in two pages?
          </h3>
          <p className="max-w-xl text-sm text-slate-400">
            The two-page summary states the one-sentence claim, the staged
            reconstruction, the carrier theorem, the status discipline, and the
            full prediction surface in compact form.
          </p>
          <Link
            href={TWO_PAGE_SUMMARY}
            target="_blank"
            rel="noopener"
            onClick={() =>
              trackPdfDownload({
                file: TWO_PAGE_SUMMARY,
                source: "predictions-summary-cta",
                kind: "summary",
                title: "Two-page summary",
              })
            }
            className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
          >
            <Download size={16} />
            Download two-page summary
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
