"use client";

import { useEffect, useRef, useState } from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";

/**
 * Expandable — clamps long prose to a fixed height with a fade-out and a
 * "Show more / Show less" toggle. If the content fits, it renders untouched
 * (no button, no fade). Used to keep the dense mirror texts (paper sections,
 * front boxes, DAG node summaries, prediction descriptions) scannable without
 * deleting any content.
 */
export function Expandable({
  children,
  collapsedHeight = 160,
  className,
}: {
  children: React.ReactNode;
  /** Max height in px while collapsed. */
  collapsedHeight?: number;
  className?: string;
}) {
  const [open, setOpen] = useState(false);
  const [overflows, setOverflows] = useState(false);
  const inner = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = inner.current;
    if (!el) return;
    const check = () => setOverflows(el.scrollHeight > collapsedHeight + 24);
    check();
    // re-check when fonts/layout settle
    const ro = new ResizeObserver(check);
    ro.observe(el);
    return () => ro.disconnect();
  }, [collapsedHeight]);

  const clamped = overflows && !open;

  return (
    <div className={className}>
      <div
        className="relative overflow-hidden transition-[max-height] duration-300"
        style={{ maxHeight: clamped ? collapsedHeight : undefined }}
      >
        <div ref={inner}>{children}</div>
        {clamped && (
          <div
            aria-hidden
            className="pointer-events-none absolute inset-x-0 bottom-0 h-14 bg-gradient-to-t from-slate-950/95 to-transparent"
          />
        )}
      </div>
      {overflows && (
        <button
          type="button"
          onClick={() => setOpen((o) => !o)}
          aria-expanded={open}
          className="mt-1.5 inline-flex items-center gap-1 text-[11px] font-semibold uppercase tracking-widest text-blue-300/80 transition-colors hover:text-blue-200"
        >
          {open ? "Show less" : "Show more"}
          <ChevronDown
            size={12}
            aria-hidden
            className={cn("transition-transform", open && "rotate-180")}
          />
        </button>
      )}
    </div>
  );
}
