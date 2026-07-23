"use client";

import Link from "next/link";
import { ArrowRight, FileText } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { trackPdfInteraction } from "@/lib/track";

const CORE: { href: string; label: string; note: string }[] = [
  {
    href: "/papers/introduction.pdf",
    label: "Reading guide",
    note: "introduction.pdf — start here",
  },
  {
    href: "/papers/tfpt_1_architecture_e8.pdf",
    label: "Architecture & E₈",
    note: "Paper 1 — the compiler",
  },
  {
    href: "/papers/tfpt_5_redteam.pdf",
    label: "Red Team",
    note: "Paper 5 — how it can fail",
  },
];

/** Compact home teaser: three core PDFs + link to the full document set. */
export function DownloadsTeaser() {
  return (
    <section
      id="downloads"
      className="relative scroll-mt-20 border-t border-slate-800/60 py-14 sm:py-16"
      aria-labelledby="downloads-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          id="downloads-heading"
          eyebrow="Downloads"
          title="Three papers to start"
          description="The reading guide, the architecture paper, and the adversarial Red Team — then the full set."
        />
        <div className="mt-8 grid gap-3 sm:grid-cols-3">
          {CORE.map((c) => (
            <a
              key={c.href}
              href={c.href}
              target="_blank"
              rel="noopener"
              onClick={() =>
                trackPdfInteraction({
                  file: c.href,
                  source: "downloads-teaser",
                  kind: "paper",
                  interaction: "download",
                  title: c.label,
                })
              }
              className="group flex items-start gap-3 border border-slate-700/50 bg-slate-950/50 px-4 py-4 transition-colors hover:border-slate-500/60"
            >
              <FileText
                size={18}
                className="mt-0.5 flex-none text-slate-500 group-hover:text-blue-300"
                aria-hidden
              />
              <span>
                <span className="block text-sm font-semibold text-slate-100">
                  {c.label}
                </span>
                <span className="mt-0.5 block font-mono text-[11px] text-slate-500">
                  {c.note}
                </span>
              </span>
            </a>
          ))}
        </div>
        <div className="mt-5">
          <Link
            href="/papers"
            className="inline-flex items-center gap-1.5 text-sm font-semibold text-blue-300 hover:text-blue-200"
          >
            All papers →
            <ArrowRight size={14} aria-hidden />
          </Link>
        </div>
      </div>
    </section>
  );
}
