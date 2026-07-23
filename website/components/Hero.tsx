"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowRight, BookOpen, Download, Github, Play, ShieldAlert, Terminal } from "lucide-react";
import { trackPdfInteraction } from "@/lib/track";
import { REPO_URL } from "@/lib/utils";
import { SITE_VERSION } from "@/lib/version";
import { SCRIPT_TOTAL } from "@/lib/suite";
import { ProofStrip } from "./ProofStrip";
import { SuiteBadge } from "./SuiteBadge";

const READING_GUIDE = "/papers/introduction.pdf";

export function Hero() {
  return (
    <section className="relative isolate overflow-hidden pt-8 pb-8 sm:pt-12 sm:pb-12">
      <div
        aria-hidden="true"
        className="absolute inset-0 grid-bg pointer-events-none"
      />
      {/* Subtle technical rule — no purple glow blob */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-slate-500/40 to-transparent"
      />

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          className="flex flex-col items-center text-center"
        >
          <div className="flex flex-wrap items-center justify-center gap-2">
            <span className="inline-flex items-center gap-2 border border-slate-600/50 bg-slate-950/70 px-3 py-1 font-mono text-[11px] tracking-wide text-slate-300">
              v{SITE_VERSION} · ledger-synced · {SCRIPT_TOTAL} checks green
            </span>
            <SuiteBadge />
          </div>

          <h1
            aria-label="Two axioms. One compiler. A testable Standard-Model skeleton."
            className="mt-4 max-w-4xl font-serif text-[1.85rem] font-semibold leading-[1.08] text-slate-50 sm:mt-5 sm:text-5xl md:text-6xl"
          >
            <span className="block">Two axioms. One compiler.</span>{" "}
            <span className="block">
              A testable{" "}
              <span className="text-blue-300">Standard-Model skeleton</span>.
            </span>
          </h1>

          <p className="mt-4 max-w-2xl text-sm leading-relaxed text-slate-300 sm:text-base">
            A discrete programme that builds the Standard-Model skeleton from
            two fixed inputs — and ships every load-bearing step as
            machine-checked code you can run yourself.
          </p>

          <ProofStrip className="mt-5 sm:mt-6" />

          <div className="mt-5 flex flex-col items-stretch gap-2 sm:mt-7 sm:flex-row sm:flex-wrap sm:items-center sm:justify-center sm:gap-2.5">
            <Link
              href="#intro-video"
              className="group inline-flex items-center justify-center gap-2 border border-blue-400/40 bg-blue-500/15 px-5 py-2.5 text-sm font-semibold text-blue-100 transition-colors hover:bg-blue-500/25"
            >
              <Play size={15} aria-hidden />
              Watch the film (5½ min)
              <ArrowRight
                size={15}
                className="transition-transform group-hover:translate-x-0.5"
                aria-hidden
              />
            </Link>
            <Link
              href="/verification#dag"
              className="group inline-flex items-center justify-center gap-2 border border-slate-600/60 bg-slate-900/60 px-5 py-2.5 text-sm font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
            >
              <Terminal size={15} aria-hidden />
              Run one check in your browser
            </Link>
            <Link
              href="/falsification"
              className="group inline-flex items-center justify-center gap-2 border border-rose-400/35 bg-rose-500/10 px-5 py-2.5 text-sm font-semibold text-rose-100 transition-colors hover:bg-rose-500/20"
            >
              <ShieldAlert size={15} aria-hidden />
              How it can fail
            </Link>
          </div>

          <div className="mt-4 flex flex-wrap items-center justify-center gap-x-4 gap-y-1.5 text-xs text-slate-500">
            <Link
              href="/orientation"
              className="inline-flex items-center gap-1 hover:text-slate-300"
            >
              <BookOpen size={12} aria-hidden />
              Reading guide
            </Link>
            <Link
              href={READING_GUIDE}
              target="_blank"
              rel="noopener"
              onClick={() =>
                trackPdfInteraction({
                  file: READING_GUIDE,
                  source: "hero",
                  kind: "summary",
                  interaction: "download",
                  title: "Reading guide (introduction)",
                })
              }
              className="inline-flex items-center gap-1 hover:text-slate-300"
            >
              <Download size={12} aria-hidden />
              PDF
            </Link>
            <Link
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 hover:text-slate-300"
            >
              <Github size={12} aria-hidden />
              GitHub
            </Link>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
