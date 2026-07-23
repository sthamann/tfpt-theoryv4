"use client";

import type { TourStepMeta } from "./tourData";
import { ForPhysicists } from "./ForPhysicists";

interface TourStepCardProps {
  step: TourStepMeta;
  children?: React.ReactNode;
  depth?: React.ReactNode;
  visual?: React.ReactNode;
}

/**
 * One tour beat: large plain-English claim, optional mini-visual,
 * optional "For physicists" disclosure.
 */
export function TourStepCard({
  step,
  children,
  depth,
  visual,
}: TourStepCardProps) {
  return (
    <section
      id={`step-${step.id}`}
      aria-labelledby={`tour-heading-${step.id}`}
      className="scroll-mt-24 border-t border-slate-800/60 py-12 sm:py-16"
    >
      <div className="mx-auto max-w-3xl px-4 sm:px-6">
        <p className="text-xs font-semibold uppercase tracking-widest text-blue-300/90">
          {step.n.toString().padStart(2, "0")} · {step.short}
        </p>
        <h2
          id={`tour-heading-${step.id}`}
          className="mt-3 font-serif text-3xl font-semibold leading-tight text-slate-50 sm:text-4xl"
        >
          {step.title}
        </h2>
        <p className="mt-4 text-lg leading-relaxed text-slate-300 sm:text-xl">
          {step.plain}
        </p>

        {visual}
        {children}

        {depth && <ForPhysicists>{depth}</ForPhysicists>}
      </div>
    </section>
  );
}
