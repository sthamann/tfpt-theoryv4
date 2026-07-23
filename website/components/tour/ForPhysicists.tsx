"use client";

import { useId, useState } from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";

/**
 * Progressive disclosure block: plain English stays above; technical depth
 * is one click away under a "For physicists" label.
 */
export function ForPhysicists({
  children,
  className,
  label = "For physicists",
}: {
  children: React.ReactNode;
  className?: string;
  label?: string;
}) {
  const [open, setOpen] = useState(false);
  const panelId = useId();

  return (
    <div
      className={cn(
        "mt-5 rounded-xl border border-slate-700/50 bg-slate-950/50",
        className,
      )}
    >
      <button
        type="button"
        aria-expanded={open}
        aria-controls={panelId}
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center justify-between gap-3 px-4 py-3 text-left transition-colors hover:bg-slate-900/60"
      >
        <span className="text-xs font-semibold uppercase tracking-widest text-blue-300/90">
          {label}
        </span>
        <ChevronDown
          size={16}
          aria-hidden
          className={cn(
            "shrink-0 text-slate-400 transition-transform duration-200",
            open && "rotate-180",
          )}
        />
      </button>
      {open && (
        <div
          id={panelId}
          className="border-t border-slate-800/80 px-4 py-4 text-sm leading-relaxed text-slate-300"
        >
          {children}
        </div>
      )}
    </div>
  );
}
