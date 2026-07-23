"use client";

import { useState } from "react";
import Link from "next/link";
import { Check, Copy } from "lucide-react";
import { SCRIPT_TOTAL } from "@/lib/suite";
import { cn } from "@/lib/utils";

const REPRO_LINE = "python run_all.py → ALL CHECKS PASSED";
const REPRO_COPY = "python run_all.py";

/**
 * The anti-slop strip: machine-checked counts + copyable repro one-liner.
 * Intended as the hero visual — lab-notebook, not marketing glow.
 */
export function ProofStrip({ className }: { className?: string }) {
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(REPRO_COPY);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      /* clipboard may be denied; the line remains selectable */
    }
  };

  return (
    <div
      className={cn(
        "w-full max-w-3xl border border-slate-600/50 bg-slate-950/80 text-left",
        className,
      )}
    >
      <div className="border-b border-slate-700/60 px-3 py-2 font-mono text-[11px] leading-relaxed tracking-wide text-slate-300 sm:px-4 sm:text-xs">
        <span className="text-emerald-300/90">{SCRIPT_TOTAL}</span>
        {" machine-checked modules · Wolfram mirror · Lean carrier · "}
        <span className="text-amber-200/90">0 external replications yet</span>
      </div>
      <div className="flex flex-col gap-2 px-3 py-2.5 sm:flex-row sm:items-center sm:justify-between sm:px-4">
        <button
          type="button"
          onClick={copy}
          title="Copy: python run_all.py"
          className="group flex min-w-0 items-center gap-2 text-left font-mono text-[11px] text-slate-200 transition-colors hover:text-white sm:text-xs"
        >
          <span className="truncate">{REPRO_LINE}</span>
          {copied ? (
            <Check size={13} className="flex-none text-emerald-400" aria-hidden />
          ) : (
            <Copy
              size={13}
              className="flex-none text-slate-500 group-hover:text-slate-300"
              aria-hidden
            />
          )}
          <span className="sr-only">
            {copied ? "Copied" : "Copy run command"}
          </span>
        </button>
        <Link
          href="/replication"
          className="flex-none font-mono text-[10px] uppercase tracking-widest text-slate-400 underline decoration-slate-700 underline-offset-2 hover:text-slate-200"
        >
          Replication status →
        </Link>
      </div>
    </div>
  );
}
