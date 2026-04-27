"use client";

import { ReactNode, useId, useState } from "react";
import { findEntry } from "@/lib/glossary";
import { cn } from "@/lib/utils";

interface GlossTermProps {
  /** The term to look up in the glossary. Falls back to children if omitted. */
  term?: string;
  /** Inline content. If `term` is omitted, this string is used as the lookup. */
  children: ReactNode;
  /** Force a specific definition without going through the glossary lookup. */
  override?: string;
  className?: string;
}

/**
 * Inline glossary tooltip. Wraps a technical term with a subtle dotted
 * underline; on hover, focus, or tap a small popover shows a one-sentence
 * definition pulled from `lib/glossary.ts`. Falls back to the native `title`
 * attribute so screen readers and printouts also surface the definition.
 */
export function GlossTerm({
  term,
  children,
  override,
  className,
}: GlossTermProps) {
  const lookupKey =
    term ?? (typeof children === "string" ? children : undefined);
  const entry = lookupKey ? findEntry(lookupKey) : undefined;
  const definition = override ?? entry?.short;
  const [open, setOpen] = useState(false);
  const id = useId();

  if (!definition) {
    // No matching glossary entry → render plain children, no extra DOM.
    return <>{children}</>;
  }

  return (
    <span className="relative inline-block">
      <button
        type="button"
        aria-describedby={id}
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
        onMouseEnter={() => setOpen(true)}
        onMouseLeave={() => setOpen(false)}
        onFocus={() => setOpen(true)}
        onBlur={() => setOpen(false)}
        title={definition}
        className={cn(
          "cursor-help border-b border-dotted border-blue-400/50 align-baseline text-left text-inherit transition-colors hover:text-blue-200 focus:outline-none focus-visible:rounded-sm focus-visible:ring-2 focus-visible:ring-blue-400/40",
          className,
        )}
      >
        {children}
      </button>
      <span
        id={id}
        role="tooltip"
        aria-hidden={!open}
        className={cn(
          "pointer-events-none absolute left-1/2 top-full z-30 mt-2 w-72 max-w-[80vw] -translate-x-1/2 rounded-xl border border-slate-700/60 bg-slate-950/95 p-3 text-xs leading-relaxed text-slate-200 opacity-0 shadow-2xl ring-1 ring-blue-400/20 backdrop-blur-md transition-opacity duration-150",
          open && "pointer-events-auto opacity-100",
        )}
      >
        {entry && (
          <span className="block text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
            {entry.term}
          </span>
        )}
        <span className="mt-1 block text-slate-200">{definition}</span>
      </span>
    </span>
  );
}
