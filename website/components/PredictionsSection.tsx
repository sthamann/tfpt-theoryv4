"use client";

import { useState } from "react";
import { motion } from "motion/react";
import Link from "next/link";
import { Download, LayoutGrid, Table2, FlaskConical, Github, FileText } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { PredictionCard } from "./PredictionCard";
import { PredictionMatrix } from "./PredictionMatrix";
import {
  predictions,
  Prediction,
  CATEGORY_META,
  TEST_SURFACE_GROUPS,
  EXPERIMENTS_AUDIT,
} from "@/lib/predictions";
import { cn, REPO_URL } from "@/lib/utils";
import { trackPdfInteraction } from "@/lib/track";

const AUDIT_COUNTS: { label: string; value: number; tone: string }[] = [
  { label: "typed rows", value: EXPERIMENTS_AUDIT.rows, tone: "text-slate-100" },
  { label: "consistent", value: EXPERIMENTS_AUDIT.consistent, tone: "text-emerald-300" },
  { label: "tension", value: EXPERIMENTS_AUDIT.tension, tone: "text-amber-300" },
  { label: "null", value: EXPERIMENTS_AUDIT.null, tone: "text-slate-300" },
  { label: "data-limited", value: EXPERIMENTS_AUDIT.dataLimited, tone: "text-sky-300" },
  { label: "parked", value: EXPERIMENTS_AUDIT.parked, tone: "text-slate-400" },
];

const READING_GUIDE = "/papers/introduction.pdf";

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

type View = "cards" | "matrix";

export function PredictionsSection() {
  const [filter, setFilter] = useState<Prediction["category"] | "All">("All");
  const [view, setView] = useState<View>("cards");
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
          description="Every row is a single readout with an explicit status marker, dependency class, and a stated kill or pressure criterion. Each links to the source document that derives it — and the freeze file commits the decisive kill criteria in advance. Some rows are closed numerical tests, some are structural kill tests, some are conditional, and a few are honestly-typed non-claims."
        />

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.1 }}
          transition={{ duration: 0.5 }}
          className="mt-8 rounded-2xl border border-emerald-400/20 bg-emerald-500/[0.04] p-5 sm:p-6"
        >
          <div className="flex flex-wrap items-center gap-2">
            <FlaskConical size={16} className="flex-none text-emerald-300" aria-hidden />
            <h3 className="font-serif text-base font-semibold text-slate-50">
              Empirical audit — standalone <code className="font-mono text-sm">experiments/</code> tree
            </h3>
            <span className="ml-auto rounded-full border border-emerald-400/30 bg-emerald-500/10 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-emerald-200">
              search targets · not load-bearing
            </span>
          </div>
          <p className="mt-3 max-w-3xl text-sm leading-relaxed text-slate-300">
            <span className="font-semibold text-slate-100">{EXPERIMENTS_AUDIT.headline}</span>{" "}
            {EXPERIMENTS_AUDIT.finding}
          </p>
          <div className="mt-4 grid grid-cols-3 gap-2 sm:grid-cols-6">
            {AUDIT_COUNTS.map((c) => (
              <div
                key={c.label}
                className="rounded-xl border border-slate-700/40 bg-slate-950/40 px-3 py-2 text-center"
              >
                <div className={cn("font-serif text-xl font-semibold", c.tone)}>{c.value}</div>
                <div className="text-[10px] font-medium uppercase tracking-wider text-slate-400">
                  {c.label}
                </div>
              </div>
            ))}
          </div>
          <p className="mt-4 text-xs leading-relaxed text-slate-400">
            <span className="font-semibold text-slate-300">Firewall:</span> FRB / EHT / GW are
            search fields for residual boundary-recovery patterns, frontier observables (axion,
            η_B, kaons, g−2) are <code className="font-mono">F_transfer</code> downstream bridges —
            never primitive compiler outputs, and no row is upgraded to [E] by data proximity.
          </p>
          <div className="mt-4 flex flex-wrap gap-3">
            <Link
              href={`${REPO_URL}/tree/main/${EXPERIMENTS_AUDIT.repoPath}`}
              target="_blank"
              rel="noopener"
              className="inline-flex items-center gap-1.5 rounded-full border border-emerald-400/30 bg-emerald-500/10 px-3.5 py-1.5 text-xs font-semibold text-emerald-200 transition-colors hover:bg-emerald-500/20"
            >
              <Github size={13} aria-hidden />
              experiments/ on GitHub
            </Link>
            <Link
              href={`${REPO_URL}/blob/main/${EXPERIMENTS_AUDIT.readmePath}`}
              target="_blank"
              rel="noopener"
              className="inline-flex items-center gap-1.5 rounded-full border border-slate-600/40 bg-slate-900/50 px-3.5 py-1.5 text-xs font-semibold text-slate-300 transition-colors hover:text-white"
            >
              <FileText size={13} aria-hidden />
              Audit README
            </Link>
            <Link
              href={`${REPO_URL}/blob/main/${EXPERIMENTS_AUDIT.scorecardPath}`}
              target="_blank"
              rel="noopener"
              className="inline-flex items-center gap-1.5 rounded-full border border-slate-600/40 bg-slate-900/50 px-3.5 py-1.5 text-xs font-semibold text-slate-300 transition-colors hover:text-white"
            >
              <Table2 size={13} aria-hidden />
              evidence_scorecard.json
            </Link>
          </div>
        </motion.div>

        <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {TEST_SURFACE_GROUPS.map((g) => (
            <div
              key={g.label}
              className={cn("rounded-xl border p-4", g.tone.split(" ").slice(0, 2).join(" "))}
            >
              <div
                className={cn(
                  "text-[10px] font-semibold uppercase tracking-widest",
                  g.tone.split(" ").slice(2).join(" "),
                )}
              >
                {g.label}
              </div>
              <ul className="mt-2 flex flex-wrap gap-1.5">
                {g.items.map((it) => (
                  <li
                    key={it}
                    className="rounded-md border border-slate-700/40 bg-slate-950/40 px-2 py-0.5 font-mono text-[10px] text-slate-300"
                  >
                    {it}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-8 grid gap-3 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-4 xl:grid-cols-8">
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

        <div className="mt-8 flex flex-wrap items-center gap-2">
          <div
            role="tablist"
            aria-label="Prediction view"
            className="inline-flex rounded-full bg-slate-900/50 p-0.5 ring-1 ring-slate-700/40"
          >
            <button
              type="button"
              role="tab"
              aria-selected={view === "cards"}
              onClick={() => setView("cards")}
              className={cn(
                "inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-semibold transition-colors",
                view === "cards"
                  ? "bg-blue-500 text-white shadow-md shadow-blue-500/20"
                  : "text-slate-300 hover:text-white",
              )}
            >
              <LayoutGrid size={13} aria-hidden />
              Card view
            </button>
            <button
              type="button"
              role="tab"
              aria-selected={view === "matrix"}
              onClick={() => setView("matrix")}
              className={cn(
                "inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-semibold transition-colors",
                view === "matrix"
                  ? "bg-blue-500 text-white shadow-md shadow-blue-500/20"
                  : "text-slate-300 hover:text-white",
              )}
            >
              <Table2 size={13} aria-hidden />
              Status × testability
            </button>
          </div>

          <span className="mx-2 hidden h-5 w-px bg-slate-800 sm:block" aria-hidden />

          {FILTERS.map((f) => (
            <button
              key={f.id}
              type="button"
              onClick={() => setFilter(f.id)}
              disabled={view === "matrix"}
              className={cn(
                "rounded-full px-4 py-1.5 text-xs font-medium transition-colors ring-1",
                filter === f.id && view === "cards"
                  ? "bg-blue-500 text-white ring-blue-400/40 shadow-md shadow-blue-500/20"
                  : "bg-slate-900/40 text-slate-300 ring-slate-700/40 hover:bg-slate-800/60",
                view === "matrix" && "cursor-not-allowed opacity-40",
              )}
              aria-pressed={filter === f.id}
            >
              {f.label}
            </button>
          ))}
        </div>

        {view === "cards" ? (
          <motion.div
            layout
            className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3"
          >
            {list.map((p, i) => (
              <PredictionCard key={p.id} prediction={p} index={i} />
            ))}
          </motion.div>
        ) : (
          <PredictionMatrix />
        )}

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.05 }}
          transition={{ duration: 0.6 }}
          className="mt-12 flex flex-col items-center gap-4 rounded-2xl border border-slate-700/40 bg-slate-950/40 p-8 text-center"
        >
          <h3 className="font-serif text-xl font-semibold text-slate-50">
            Want the full reading guide?
          </h3>
          <p className="max-w-xl text-sm text-slate-400">
            The introduction states the compiler closure, the dependency DAG,
            the predictions, and the single proof ledger.
          </p>
          <Link
            href={READING_GUIDE}
            target="_blank"
            rel="noopener"
            onClick={() =>
              trackPdfInteraction({
                file: READING_GUIDE,
                source: "predictions-summary-cta",
                kind: "summary",
                interaction: "download",
                title: "Reading guide (introduction)",
              })
            }
            className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
          >
            <Download size={16} />
            Open the reading guide
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
