"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { Download, Clock, FileText } from "lucide-react";
import {
  Prediction,
  predictions,
  STATUS_BADGE,
  LINK_STATUS_META,
} from "@/lib/predictions";
import { cn } from "@/lib/utils";
import { trackPdfInteraction } from "@/lib/track";

type StatusAxis =
  | "Theorem-level null"
  | "Physical observable"
  | "Comparison quantity"
  | "Cosmology comparison"
  | "Scheme projection"
  | "Kill test"
  | "Out-of-sample check";

type TestabilityAxis =
  | "currently testable"
  | "near-term"
  | "long-term"
  | "structural";

const TESTABILITY_LABEL: Record<TestabilityAxis, string> = {
  "currently testable": "Currently testable",
  "near-term": "Near-term",
  "long-term": "Long-term",
  structural: "Structural / kill test",
};

/**
 * Manual testability classification per prediction id. Living theory + living
 * experiment landscape; this map is the place to update when a new run
 * publishes or a new technique becomes available.
 */
const TESTABILITY_BY_ID: Record<string, TestabilityAxis> = {
  "alpha-em": "currently testable",
  "alpha-mz": "currently testable",
  "lambda-c": "currently testable",
  "ckm-phase": "currently testable",
  "rare-kaons": "currently testable",
  theta13: "currently testable",
  pmns: "near-term",
  "neutrino-sum": "near-term",
  "0vbb": "long-term",
  "strong-cp": "structural",
  birefringence: "currently testable",
  "eht-achromatic": "near-term",
  axion: "near-term",
  "eta-b": "long-term",
  "omega-b": "currently testable",
  "no-second-higgs": "structural",
  pi0: "currently testable",
};

const STATUS_AXIS: StatusAxis[] = [
  "Theorem-level null",
  "Physical observable",
  "Comparison quantity",
  "Cosmology comparison",
  "Scheme projection",
  "Out-of-sample check",
  "Kill test",
];

const TESTABILITY_AXIS: TestabilityAxis[] = [
  "currently testable",
  "near-term",
  "long-term",
  "structural",
];

interface MatrixCell {
  status: StatusAxis;
  testability: TestabilityAxis;
  items: Prediction[];
}

function buildMatrix(): MatrixCell[] {
  const map = new Map<string, MatrixCell>();
  for (const s of STATUS_AXIS) {
    for (const t of TESTABILITY_AXIS) {
      map.set(`${s}|${t}`, { status: s, testability: t, items: [] });
    }
  }
  for (const p of predictions) {
    const t = TESTABILITY_BY_ID[p.id] ?? "long-term";
    const cell = map.get(`${p.status}|${t}`);
    if (cell) cell.items.push(p);
  }
  return Array.from(map.values());
}

export function PredictionMatrix() {
  const cells = buildMatrix();
  const usedStatuses = STATUS_AXIS.filter((s) =>
    cells.some((c) => c.status === s && c.items.length > 0),
  );

  return (
    <div className="glass mt-10 overflow-hidden rounded-2xl ring-1 ring-slate-700/40">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          Prediction matrix — proof status × testability
        </span>
        <span className="rounded-full bg-slate-800/60 px-2.5 py-0.5 text-[10px] font-mono uppercase tracking-widest text-slate-300 ring-1 ring-slate-700/40">
          {predictions.length} entries
        </span>
      </div>

      <div className="overflow-x-auto formula-scroll">
        <table className="w-full min-w-[760px] border-separate border-spacing-0 text-left">
          <thead>
            <tr>
              <th
                scope="col"
                className="sticky left-0 z-10 min-w-[160px] border-b border-r border-slate-800/60 bg-slate-950/80 px-3 py-3 text-[10px] font-semibold uppercase tracking-widest text-slate-300"
              >
                Status ↓ / Testability →
              </th>
              {TESTABILITY_AXIS.map((t) => (
                <th
                  key={t}
                  scope="col"
                  className="border-b border-slate-800/60 px-3 py-3 text-left text-[10px] font-semibold uppercase tracking-widest text-slate-300"
                >
                  {TESTABILITY_LABEL[t]}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {usedStatuses.map((s) => {
              const badge = STATUS_BADGE[s];
              return (
                <tr key={s}>
                  <th
                    scope="row"
                    className={cn(
                      "sticky left-0 z-10 border-b border-r border-slate-800/60 bg-slate-950/80 px-3 py-3 align-top text-xs font-semibold",
                      badge.color,
                    )}
                  >
                    <span
                      className={cn(
                        "inline-block rounded-full px-2 py-0.5 ring-1",
                        badge.bg,
                      )}
                    >
                      {s}
                    </span>
                  </th>
                  {TESTABILITY_AXIS.map((t) => {
                    const cell = cells.find(
                      (c) => c.status === s && c.testability === t,
                    );
                    const items = cell?.items ?? [];
                    return (
                      <td
                        key={t}
                        className="border-b border-slate-800/60 align-top px-2 py-2"
                      >
                        <div className="flex flex-col gap-1.5">
                          {items.length === 0 && (
                            <span
                              aria-hidden
                              className="text-[10px] text-slate-700"
                            >
                              ·
                            </span>
                          )}
                          {items.map((p, i) => (
                            <MatrixChip key={p.id} prediction={p} index={i} />
                          ))}
                        </div>
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="border-t border-slate-800/60 px-5 py-3 text-[11px] leading-relaxed text-slate-400">
        Rows mirror the proof-status layer; columns mirror the experimental
        timeline. The same prediction never appears twice. Long-term and
        structural cells are kill criteria, not promises of imminent
        confirmation.
      </div>
    </div>
  );
}

function MatrixChip({
  prediction,
  index,
}: {
  prediction: Prediction;
  index: number;
}) {
  const linkState = prediction.linkStatus ?? "available";
  const linkMeta = LINK_STATUS_META[linkState];
  const Icon =
    linkState === "available"
      ? Download
      : linkState === "note"
        ? FileText
        : Clock;
  const inner = (
    <div className="flex items-start gap-1.5">
      <Icon size={11} className="mt-0.5 flex-none opacity-80" aria-hidden />
      <div className="min-w-0">
        <div className="font-mono text-[11px] font-semibold leading-tight text-slate-100">
          {prediction.shortTitle}
        </div>
        <div className="truncate text-[10px] leading-snug text-slate-400">
          {prediction.title}
        </div>
      </div>
    </div>
  );

  if (linkMeta.disabled) {
    return (
      <span
        aria-disabled="true"
        title={linkMeta.label}
        className="block rounded-md border border-slate-700/40 bg-slate-950/40 px-2 py-1.5 text-slate-300/80"
      >
        {inner}
      </span>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 4 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.05 }}
      transition={{ duration: 0.3, delay: index * 0.03 }}
    >
      <Link
        href={prediction.pdf}
        target="_blank"
        rel="noopener"
        onClick={() =>
          trackPdfInteraction({
            file: prediction.pdf,
            source: "predictions-card",
            kind: "prediction",
            interaction: "download",
            title: prediction.title,
          })
        }
        className="block rounded-md border border-slate-700/40 bg-slate-950/40 px-2 py-1.5 transition-colors hover:border-blue-400/40 hover:bg-blue-500/5"
      >
        {inner}
      </Link>
    </motion.div>
  );
}
