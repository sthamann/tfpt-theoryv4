"use client";

import { motion } from "motion/react";

const STAGES = [
  {
    id: "T14",
    title: "Deflate the slogan",
    detail: "“2π is self-dual temperature” overreached — angle vs steps separated.",
    verdict: "DEFLATED",
  },
  {
    id: "T20",
    title: "Mode density",
    detail: "Arch kernel is not in the free seam DOS (falling O(1), not log).",
    verdict: "KILLED-AS-NAIVE",
  },
  {
    id: "T22–24",
    title: "Interval cut → dictionary",
    detail: "Boost/log lives in the half-cut; one-constant arch dictionary fails (2/π).",
    verdict: "PARTIAL → DEAD",
  },
  {
    id: "T25",
    title: "Scattering phase",
    detail: "Last observable dies. Seam keeps a discrete μ₄ clock, not a Gamma.",
    verdict: "DEAD · ROUTE CLOSED",
  },
] as const;

export function KillChainTimeline() {
  return (
    <div className="rounded-2xl border border-slate-700/50 bg-slate-950/60 p-4 sm:p-6">
      <p className="mb-4 font-mono text-[10px] uppercase tracking-widest text-rose-300/90">
        Kill chain as a feature — preregistered, not a failure of nerve
      </p>
      <ol className="relative space-y-0">
        <div
          aria-hidden
          className="absolute bottom-3 left-[1.15rem] top-3 w-px bg-gradient-to-b from-rose-400/60 via-amber-400/40 to-slate-600/40"
        />
        {STAGES.map((s, i) => (
          <motion.li
            key={s.id}
            initial={{ opacity: 0, x: -10 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, amount: 0.4 }}
            transition={{ duration: 0.45, delay: i * 0.12 }}
            className="relative flex gap-4 pb-6 last:pb-0"
          >
            <span className="relative z-10 mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-rose-400/40 bg-slate-950 font-mono text-[10px] text-rose-200">
              {i + 1}
            </span>
            <div className="min-w-0 flex-1 rounded-xl border border-slate-700/40 bg-slate-900/50 px-3 py-2.5">
              <div className="flex flex-wrap items-baseline gap-x-2 gap-y-1">
                <span className="font-mono text-[10px] text-slate-500">
                  {s.id}
                </span>
                <span className="font-serif text-base text-slate-100">
                  {s.title}
                </span>
                <span className="ml-auto font-mono text-[9px] uppercase tracking-wider text-rose-300/80">
                  {s.verdict}
                </span>
              </div>
              <p className="mt-1 text-sm leading-relaxed text-slate-400">
                {s.detail}
              </p>
            </div>
          </motion.li>
        ))}
      </ol>
    </div>
  );
}
