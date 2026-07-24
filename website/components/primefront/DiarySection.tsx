import type { ReactNode } from "react";
import type { PrimeFrontBadge } from "@/lib/primeFront";
import { StatusBadge } from "./StatusBadge";

export function DiarySection({
  id,
  eyebrow,
  title,
  badge,
  children,
  visual,
}: {
  id: string;
  eyebrow: string;
  title: string;
  badge: PrimeFrontBadge;
  children: ReactNode;
  visual?: ReactNode;
}) {
  return (
    <section
      id={id}
      aria-labelledby={`${id}-heading`}
      className="scroll-mt-24 border-t border-slate-800/60 py-12 sm:py-16"
    >
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-wrap items-center gap-2">
          <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-slate-500">
            {eyebrow}
          </span>
          <StatusBadge badge={badge} />
        </div>
        <h2
          id={`${id}-heading`}
          className="mt-3 font-serif text-2xl font-semibold leading-tight text-slate-50 sm:text-3xl md:text-4xl"
        >
          {title}
        </h2>
        <div className="mt-6 grid gap-8 lg:grid-cols-2 lg:items-start">
          <div className="space-y-4 text-base leading-relaxed text-slate-300">
            {children}
          </div>
          {visual && <div className="lg:sticky lg:top-24">{visual}</div>}
        </div>
      </div>
    </section>
  );
}
