"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowRight, BookOpen, Download, ShieldAlert, Sigma } from "lucide-react";
import { trackPdfInteraction } from "@/lib/track";
import { cn } from "@/lib/utils";
import { ThreeDecoderMap } from "./ThreeDecoderMap";
import { TheoryUnpacking } from "./TheoryUnpacking";
import { GlossTerm } from "./GlossTerm";

const TWO_PAGE_SUMMARY = "/predictions/tfpt_two_page_summary.pdf";

export function Hero() {
  return (
    <section className="relative isolate overflow-hidden pt-12 pb-24 sm:pb-32">
      <div
        aria-hidden="true"
        className="absolute inset-0 grid-bg pointer-events-none"
      />
      <div
        aria-hidden="true"
        className="absolute -top-40 left-1/2 -z-10 h-[600px] w-[1100px] -translate-x-1/2 rounded-full opacity-40 blur-3xl"
        style={{
          background:
            "radial-gradient(closest-side, rgba(99,102,241,0.45), rgba(168,85,247,0.25), transparent)",
        }}
      />

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className="flex flex-col items-center text-center"
        >
          <span className="inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-500/10 px-4 py-1.5 text-xs font-medium tracking-wider text-blue-200">
            <Sigma size={14} className="opacity-80" />
            <span className="uppercase">TFPT 4.5 paper series · 2026</span>
          </span>

          <h1 className="mt-6 max-w-4xl font-serif text-4xl font-semibold leading-[1.05] text-slate-50 sm:text-5xl md:text-6xl lg:text-7xl">
            <span className="block">
              One{" "}
              <span className="text-gradient-blue">boundary datum</span>.
            </span>
            <span className="block">A staged reconstruction of the</span>
            <span className="block">Standard Model packet.</span>
          </h1>
          <p className="mt-3 max-w-2xl text-sm leading-relaxed text-slate-400">
            <span className="font-semibold text-slate-200">Proof discipline.</span>{" "}
            The page separates theorem core, bridge readouts, conditional QFT
            closure, and downstream targets. Every output has an explicit
            failure mode.
          </p>

          <p className="mt-6 max-w-2xl text-base leading-relaxed text-slate-300 sm:text-lg md:text-xl">
            <span className="font-semibold text-slate-100">
              Topological Fixed-Point Theory
            </span>{" "}
            presents a staged reconstruction of the Standard-Model{" "}
            <GlossTerm term="carrier">carrier packet</GlossTerm>, the
            fine-structure constant, the Cabibbo angle, the PMNS matrix,
            strong-CP closure, and downstream cosmology — from a single{" "}
            <GlossTerm term="boundary datum">one-sided boundary datum</GlossTerm>
            , with{" "}
            <span className="font-semibold text-blue-300">no fitted constants</span>.
          </p>

          <div className="mt-10 flex flex-col items-center gap-3 sm:flex-row sm:flex-wrap sm:justify-center">
            <Link
              href="/orientation"
              className="group inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-500/30 ring-1 ring-blue-400/40 transition-transform hover:scale-105 focus:scale-105"
            >
              <BookOpen size={16} />
              Read the orientation map
              <ArrowRight
                size={16}
                className="transition-transform group-hover:translate-x-0.5"
              />
            </Link>
            <Link
              href="/falsification"
              className="group inline-flex items-center gap-2 rounded-full border border-rose-400/40 bg-rose-500/10 px-6 py-3 text-sm font-semibold text-rose-100 transition-colors hover:bg-rose-500/20 focus:bg-rose-500/20"
            >
              <ShieldAlert size={16} />
              How to kill TFPT
              <ArrowRight
                size={16}
                className="transition-transform group-hover:translate-x-0.5"
              />
            </Link>
            <Link
              href={TWO_PAGE_SUMMARY}
              target="_blank"
              rel="noopener"
              onClick={() =>
                trackPdfInteraction({
                  file: TWO_PAGE_SUMMARY,
                  source: "hero",
                  kind: "summary",
                  interaction: "download",
                  title: "Two-page summary",
                })
              }
              className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-6 py-3 text-sm font-semibold text-slate-100 backdrop-blur transition-colors hover:bg-slate-800/80"
            >
              <Download size={16} />
              Two-page summary
            </Link>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 32 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.9, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
          className="mx-auto mt-20 grid max-w-5xl gap-4 sm:mt-24 sm:grid-cols-2 lg:grid-cols-4"
        >
          {STATS.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 + i * 0.08 }}
              className="glass relative flex flex-col gap-1 rounded-2xl px-5 py-5 ring-1 ring-slate-700/40"
            >
              <div
                className={cn(
                  "text-[11px] font-semibold tracking-widest text-blue-300/80",
                  s.isMath ? "math-label" : "uppercase",
                )}
              >
                {s.label}
              </div>
              <div className="font-serif text-2xl font-semibold text-slate-50 sm:text-3xl">
                {s.value}
              </div>
              <div className="text-xs leading-relaxed text-slate-400">
                {s.note}
              </div>
            </motion.div>
          ))}
        </motion.div>

        <TheoryUnpacking />

        <ThreeDecoderMap />
      </div>
    </section>
  );
}

const STATS: Array<{
  label: string;
  value: string;
  note: string;
  isMath?: boolean;
}> = [
  {
    label: "α⁻¹(0)",
    value: "137.0359992",
    note: "Closed-branch root; CODATA 2022 recommended 137.035 999 177(21)",
    isMath: true,
  },
  {
    label: "Families",
    value: "3",
    note: "From admissible occupancy on the rigid carrier",
  },
  {
    label: "θ_eff",
    value: "0",
    note: "Strong-CP null — theorem-level on the admissible branch",
    isMath: true,
  },
  {
    label: "β_BH(r)",
    value: "16 c₃⁴ / r²",
    note: "Achromatic dyonic residual intercept — EHT/ngEHT prediction",
    isMath: true,
  },
];
