"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { Download, Target, AlertTriangle } from "lucide-react";
import { Math as Tex } from "./Math";
import { Prediction, STATUS_BADGE, CATEGORY_META } from "@/lib/predictions";
import { cn } from "@/lib/utils";

export function PredictionCard({
  prediction,
  index = 0,
}: {
  prediction: Prediction;
  index?: number;
}) {
  const cat = CATEGORY_META[prediction.category];
  const status = STATUS_BADGE[prediction.status];

  return (
    <motion.article
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.05 }}
      transition={{ duration: 0.5, delay: Math.min(index, 8) * 0.04 }}
      className="group glass relative flex flex-col overflow-hidden rounded-2xl ring-1 ring-slate-700/40 transition-all hover:ring-slate-500/60"
    >
      <div
        aria-hidden="true"
        className={cn(
          "pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r opacity-70",
          cat.color,
        )}
      />

      <div className="flex flex-col gap-2 px-5 pt-5">
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full border border-slate-600/40 bg-slate-900/50 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-slate-300">
            {cat.label}
          </span>
          <span
            className={cn(
              "rounded-full px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest ring-1",
              status.bg,
              status.color,
            )}
          >
            {prediction.status}
          </span>
        </div>

        <h3 className="font-serif text-lg font-semibold leading-snug text-slate-50">
          {prediction.title}
        </h3>
      </div>

      <div className="px-5 pb-3 pt-3">
        <div className="rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
          <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
            Target
          </div>
          <div className="mt-1 overflow-x-auto">
            <Tex block>{prediction.targetLatex}</Tex>
          </div>
        </div>
      </div>

      <p className="px-5 text-sm leading-relaxed text-slate-300">
        {prediction.description}
      </p>

      <div className="mt-4 grid grid-cols-1 gap-px bg-slate-800/60">
        <div className="flex items-start gap-2 bg-slate-950/40 px-5 py-3">
          <Target
            size={14}
            className="mt-0.5 flex-none text-blue-300/70"
            aria-hidden="true"
          />
          <div>
            <div className="text-[10px] font-semibold uppercase tracking-widest text-slate-400">
              Dependency class
            </div>
            <div className="text-xs text-slate-200">
              {prediction.dependencyClass}
            </div>
          </div>
        </div>
        <div className="flex items-start gap-2 bg-slate-950/40 px-5 py-3">
          <AlertTriangle
            size={14}
            className="mt-0.5 flex-none text-orange-300/70"
            aria-hidden="true"
          />
          <div>
            <div className="text-[10px] font-semibold uppercase tracking-widest text-slate-400">
              Kill / pressure test
            </div>
            <div className="text-xs leading-snug text-slate-200">
              {prediction.killTest}
            </div>
          </div>
        </div>
      </div>

      <div className="mt-auto border-t border-slate-800/60 px-5 py-3">
        <Link
          href={prediction.pdf}
          target="_blank"
          rel="noopener"
          className="inline-flex items-center gap-2 text-sm font-semibold text-blue-300 transition-colors hover:text-blue-200"
        >
          <Download size={14} />
          Download dedicated paper
        </Link>
      </div>
    </motion.article>
  );
}
