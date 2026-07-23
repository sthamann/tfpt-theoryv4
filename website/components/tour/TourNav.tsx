"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";
import type { TourStepMeta } from "./tourData";

interface TourNavProps {
  steps: readonly TourStepMeta[];
  activeIndex: number;
  onGo: (index: number) => void;
  onPrev: () => void;
  onNext: () => void;
}

/**
 * Sticky mobile-first stepper: progress dots + prev/next.
 * Deep links use #step-<id> anchors owned by TourShell.
 */
export function TourNav({
  steps,
  activeIndex,
  onGo,
  onPrev,
  onNext,
}: TourNavProps) {
  const atStart = activeIndex <= 0;
  const atEnd = activeIndex >= steps.length - 1;
  const active = steps[activeIndex];

  return (
    <nav
      aria-label="Tour steps"
      className="sticky top-0 z-30 border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md"
    >
      <div className="mx-auto flex max-w-3xl items-center gap-2 px-3 py-2.5 sm:px-4">
        <button
          type="button"
          onClick={onPrev}
          disabled={atStart}
          aria-label="Previous step"
          className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-slate-700/60 text-slate-200 transition-colors hover:bg-slate-800/80 disabled:cursor-not-allowed disabled:opacity-30"
        >
          <ChevronLeft size={18} aria-hidden />
        </button>

        <div className="min-w-0 flex-1">
          <div className="flex items-center justify-between gap-2">
            <p className="truncate text-[11px] font-semibold uppercase tracking-widest text-blue-300/90">
              Step {active.n} / {steps.length}
            </p>
            <p className="hidden truncate text-xs text-slate-400 sm:block">
              {active.short}
            </p>
          </div>
          <ol className="mt-1.5 flex items-center justify-between gap-1">
            {steps.map((s, i) => {
              const done = i < activeIndex;
              const current = i === activeIndex;
              return (
                <li key={s.id} className="flex-1">
                  <button
                    type="button"
                    onClick={() => onGo(i)}
                    aria-label={`${s.n}. ${s.short}`}
                    aria-current={current ? "step" : undefined}
                    title={s.short}
                    className={cn(
                      "block h-1.5 w-full rounded-full transition-colors",
                      current && "bg-blue-400",
                      done && !current && "bg-emerald-500/70",
                      !done && !current && "bg-slate-700/80 hover:bg-slate-600",
                    )}
                  />
                </li>
              );
            })}
          </ol>
        </div>

        <button
          type="button"
          onClick={onNext}
          disabled={atEnd}
          aria-label="Next step"
          className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-slate-700/60 text-slate-200 transition-colors hover:bg-slate-800/80 disabled:cursor-not-allowed disabled:opacity-30"
        >
          <ChevronRight size={18} aria-hidden />
        </button>
      </div>
      <p className="sr-only">Use left and right arrow keys to move between steps.</p>
    </nav>
  );
}
