"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import {
  predictions,
  STATUS_MARKER,
  STATUS_BADGE,
  type Prediction,
} from "@/lib/predictions";
import { REPO_URL } from "@/lib/utils";
import { cn } from "@/lib/utils";

/**
 * The Kill Board — every status-graded readout as a scannable card with its
 * committed kill condition and, where one exists, the live experimental
 * status. It is generated directly from lib/predictions.ts (the single
 * prediction source), so it can never drift from the prediction table; the
 * curated structural kills with their formal conditions live below in
 * KillCriteria.
 */
type Finding = NonNullable<Prediction["experiment"]>["finding"];

const FINDING_META: Record<Finding, { label: string; tone: string }> = {
  consistent: { label: "Live · consistent", tone: "bg-emerald-500/15 text-emerald-200 ring-emerald-400/30" },
  robust: { label: "Live · robust", tone: "bg-emerald-500/15 text-emerald-200 ring-emerald-400/30" },
  tension: { label: "Live · tension", tone: "bg-amber-500/15 text-amber-200 ring-amber-400/30" },
  null: { label: "Live · null", tone: "bg-slate-500/15 text-slate-200 ring-slate-400/30" },
  data_limited: { label: "Data-limited", tone: "bg-sky-500/15 text-sky-200 ring-sky-400/30" },
};

const STRUCTURAL_META = {
  label: "Structural / committed",
  tone: "bg-blue-500/15 text-blue-200 ring-blue-400/30",
};

export function KillBoard() {
  return (
    // Rendered inside an already-labelled <section>, so this is a plain <div>.
    <div id="kill-board" className="relative py-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-5 flex flex-wrap items-center gap-2 text-[11px] text-slate-400">
          <span className="font-semibold uppercase tracking-widest text-slate-300">
            Status legend
          </span>
          {(["consistent", "tension", "null", "data_limited"] as Finding[]).map((f) => (
            <span
              key={f}
              className={cn(
                "rounded-full px-2 py-0.5 font-semibold ring-1",
                FINDING_META[f].tone,
              )}
            >
              {FINDING_META[f].label}
            </span>
          ))}
          <span className={cn("rounded-full px-2 py-0.5 font-semibold ring-1", STRUCTURAL_META.tone)}>
            {STRUCTURAL_META.label}
          </span>
        </div>

        <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {predictions.map((p, i) => {
            const finding = p.experiment?.finding;
            const statusMeta = finding ? FINDING_META[finding] : STRUCTURAL_META;
            return (
              <li key={p.id}>
                <motion.article
                  initial={{ opacity: 0, y: 12 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.05 }}
                  transition={{ duration: 0.35, delay: (i % 6) * 0.04 }}
                  className="flex h-full flex-col rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4"
                >
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="font-mono text-sm font-semibold text-slate-50">
                      {p.shortTitle}
                    </h3>
                    <span
                      className={cn(
                        "flex-none rounded-full px-2 py-0.5 font-mono text-[10px] font-semibold ring-1",
                        STATUS_BADGE[p.status].bg,
                        STATUS_BADGE[p.status].color,
                      )}
                    >
                      {STATUS_MARKER[p.status]}
                    </span>
                  </div>

                  <div className="mt-1 text-xs font-medium text-slate-300">{p.target}</div>

                  <div className="mt-3">
                    <div className="text-[10px] font-semibold uppercase tracking-widest text-rose-300/80">
                      Kill condition
                    </div>
                    <p className="mt-1 text-xs leading-relaxed text-slate-300">{p.killTest}</p>
                  </div>

                  <div className="mt-auto flex flex-wrap items-center justify-between gap-2 pt-3">
                    <span
                      className={cn(
                        "rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider ring-1",
                        statusMeta.tone,
                      )}
                    >
                      {statusMeta.label}
                    </span>
                    {p.experiment?.repoPath ? (
                      <Link
                        href={`${REPO_URL}/tree/main/${p.experiment.repoPath}`}
                        target="_blank"
                        rel="noopener"
                        className="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-300 transition-colors hover:text-blue-200"
                      >
                        Empirical audit
                        <ArrowUpRight size={12} aria-hidden />
                      </Link>
                    ) : (
                      <Link
                        href={p.pdf}
                        target="_blank"
                        rel="noopener"
                        className="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-300 transition-colors hover:text-blue-200"
                      >
                        Source document
                        <ArrowUpRight size={12} aria-hidden />
                      </Link>
                    )}
                  </div>
                </motion.article>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
