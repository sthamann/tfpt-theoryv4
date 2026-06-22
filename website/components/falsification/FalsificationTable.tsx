"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { Math } from "@/components/Math";
import {
  predictions,
  STATUS_MARKER,
  STATUS_BADGE,
  type Prediction,
} from "@/lib/predictions";
import { REPO_URL, cn } from "@/lib/utils";

/**
 * The confrontation table — every one of the prediction-surface readouts on a
 * single scannable row: how it is derived, the TFPT value, the current measured
 * value, the deviation, the dated source, and the experiment + timeline that
 * makes it a definitive hit or kill. It is generated directly from
 * lib/predictions.ts (the single prediction source), so it can never drift from
 * the kill board above it; every number is repo-documented (v307 data watchdog,
 * v321 forward kill-test board, freeze_file.csv, and the experiments/ tree).
 */
type Finding = NonNullable<Prediction["experiment"]>["finding"];

const DEVIATION_TONE: Record<Finding | "structural", string> = {
  consistent: "text-emerald-200",
  robust: "text-emerald-200",
  tension: "text-amber-200",
  null: "text-slate-200",
  data_limited: "text-sky-200",
  structural: "text-blue-200",
};

const COLUMNS = [
  "Readout",
  "Derivation",
  "TFPT value",
  "Measured / experimental",
  "Deviation",
  "Source & date",
  "Decisive — hit or kill",
] as const;

export function FalsificationTable() {
  return (
    // Rendered inside an already-labelled <section>, so this is a plain <div>.
    <div id="confrontation-table" className="relative py-8">
      <div className="mx-auto max-w-6xl">
        <div className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 px-5 py-3">
            <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
              Confrontation table — value · derivation · TFPT · measured · deviation · source · decisive year
            </span>
            <span className="rounded-full bg-slate-800/60 px-2.5 py-0.5 text-[10px] font-mono uppercase tracking-widest text-slate-300 ring-1 ring-slate-700/40">
              {predictions.length} readouts
            </span>
          </div>

          <div className="overflow-x-auto formula-scroll">
            <table className="w-full min-w-[1280px] border-separate border-spacing-0 text-left text-sm">
              <caption className="sr-only">
                Every TFPT prediction-surface readout with its derivation, the
                predicted value, the current measured value, the deviation, the
                dated experimental source, and the experiment and approximate
                year that will make it a definitive hit or kill.
              </caption>
              <thead>
                <tr>
                  {COLUMNS.map((h) => (
                    <th
                      key={h}
                      scope="col"
                      className={cn(
                        "border-b border-slate-800/60 px-4 py-3 text-[10px] font-semibold uppercase tracking-widest text-slate-300",
                        h === "Readout"
                          ? "sticky left-0 z-10 min-w-[150px] bg-slate-950"
                          : "bg-slate-950/60",
                      )}
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {predictions.map((p, i) => {
                  const c = p.confrontation;
                  const tone =
                    DEVIATION_TONE[p.experiment?.finding ?? "structural"];
                  const link = p.experiment
                    ? {
                        href: `${REPO_URL}/tree/main/${p.experiment.repoPath}`,
                        label: "Empirical audit",
                        external: true,
                      }
                    : { href: p.pdf, label: "Source document", external: true };
                  return (
                    <motion.tr
                      key={p.id}
                      initial={{ opacity: 0 }}
                      whileInView={{ opacity: 1 }}
                      viewport={{ once: true, amount: 0.02 }}
                      transition={{ duration: 0.3, delay: (i % 8) * 0.02 }}
                      className="group hover:bg-slate-900/30"
                    >
                      <th
                        scope="row"
                        className="sticky left-0 z-10 border-b border-slate-800/60 bg-slate-950 px-4 py-3 align-top group-hover:bg-slate-900"
                      >
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-semibold text-slate-50">
                            {p.shortTitle}
                          </span>
                          <span
                            className={cn(
                              "flex-none rounded-full px-1.5 py-0.5 font-mono text-[9px] font-semibold ring-1",
                              STATUS_BADGE[p.status].bg,
                              STATUS_BADGE[p.status].color,
                            )}
                          >
                            {STATUS_MARKER[p.status]}
                          </span>
                        </div>
                        <Link
                          href={link.href}
                          target="_blank"
                          rel="noopener"
                          className="mt-1 inline-flex items-center gap-1 text-[10px] font-medium text-blue-300/80 transition-colors hover:text-blue-200"
                        >
                          {link.label}
                          <ArrowUpRight size={10} aria-hidden />
                        </Link>
                      </th>
                      <td className="border-b border-slate-800/60 px-4 py-3 align-top">
                        <div className="overflow-x-auto formula-scroll text-xs text-slate-200">
                          <Math>{c.derivation}</Math>
                        </div>
                      </td>
                      <td className="border-b border-slate-800/60 px-4 py-3 align-top font-mono text-xs font-semibold text-slate-100">
                        {c.tfptValue}
                      </td>
                      <td className="border-b border-slate-800/60 px-4 py-3 align-top text-xs leading-relaxed text-slate-300">
                        {c.measured}
                      </td>
                      <td
                        className={cn(
                          "border-b border-slate-800/60 px-4 py-3 align-top text-xs font-semibold leading-relaxed",
                          tone,
                        )}
                      >
                        {c.deviation}
                      </td>
                      <td className="border-b border-slate-800/60 px-4 py-3 align-top text-xs leading-relaxed text-slate-400">
                        {c.source}
                      </td>
                      <td className="border-b border-slate-800/60 px-4 py-3 align-top text-xs leading-relaxed text-amber-200/90">
                        {c.decisive}
                      </td>
                    </motion.tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          <div className="border-t border-slate-800/60 px-5 py-3 text-[11px] leading-relaxed text-slate-400">
            <strong className="text-slate-200">Reading rule.</strong> Every value
            is repo-documented — the measured central values and deviations come
            from the v307 data watchdog and the standalone{" "}
            <code className="font-mono">experiments/</code> tree (current bests:
            CODATA 2022, NuFIT 6.0, ACT DR6, Planck 2018, PDG 2024, BK18, DESI
            DR2, NA62 2026); the &ldquo;decisive&rdquo; column is the forward
            kill-test board (v321), whose timelines are the publicly stated
            experimental targets, not TFPT outputs. Deviations are colour-graded
            by the live empirical finding; no readout is upgraded by data
            proximity.
          </div>
        </div>
      </div>
    </div>
  );
}
