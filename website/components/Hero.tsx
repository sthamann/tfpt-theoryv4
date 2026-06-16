"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowRight, BookOpen, Download, Github, ShieldAlert, Sigma } from "lucide-react";
import { trackPdfInteraction } from "@/lib/track";
import { cn, REPO_URL } from "@/lib/utils";
import { ThreeDecoderMap } from "./ThreeDecoderMap";
import { TheoryUnpacking } from "./TheoryUnpacking";
import { GlossTerm } from "./GlossTerm";
import { SITE_VERSION } from "@/lib/version";
import { predictions } from "@/lib/predictions";

const READING_GUIDE = "/papers/introduction.pdf";

// Single source for the headline count: the prediction surface itself, so the
// hero can never drift out of sync with the prediction table again.
const TEST_SURFACES = predictions.length;

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
            <span className="uppercase">TFPT {SITE_VERSION} · the compiler closure · 2026</span>
          </span>

          <h1
            aria-label="Two axioms. One compiler. A testable Standard-Model skeleton."
            className="mt-6 max-w-4xl font-serif text-4xl font-semibold leading-[1.05] text-slate-50 sm:text-5xl md:text-6xl lg:text-7xl"
          >
            <span className="block">Two axioms. One compiler.</span>{" "}
            <span className="block">
              A testable <span className="text-gradient-blue">Standard-Model skeleton</span>.
            </span>
          </h1>

          <ScopeGuard />
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-slate-300">
            The gauge group, three families, hypercharge and the flavor matrix
            follow from two numbers.{" "}
            <span className="font-semibold text-blue-300">α⁻¹ = 137.0359992</span>,
            1.9σ from CODATA-2022.{" "}
            <span className="font-semibold text-slate-100">{TEST_SURFACES} status-graded test surfaces</span>;
            zero fitted constants in the closed branch. Every claim is ledger-typed,
            reproducible, or explicitly open.
          </p>

          <p className="mt-6 max-w-2xl text-base leading-relaxed text-slate-300 sm:text-lg md:text-xl">
            <span className="font-semibold text-slate-100">
              Topological Fixed-Point Theory
            </span>{" "}
            reads the Standard Model, the constants and the scale grammar off a
            single{" "}
            <GlossTerm term="E8 compiler">discrete compiler</GlossTerm> built
            from the{" "}
            <GlossTerm term="seam constant">seam constant c₃ = 1/(8π)</GlossTerm>{" "}
            and the <GlossTerm term="carrier">carrier g_car = 5</GlossTerm>. The
            exceptional lattice E₈ is the compiler&rsquo;s internal bookkeeping,
            not a gauge group. The{" "}
            <GlossTerm term="bootstrap loop">bootstrap loop</GlossTerm> even
            re-derives its own inputs, so the core is{" "}
            <span className="font-semibold text-blue-300">overdetermined, not fitted</span>.
          </p>

          <div className="mt-10 flex flex-col items-center gap-3 sm:flex-row sm:flex-wrap sm:justify-center">
            <Link
              href="/orientation"
              className="group inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-500/30 ring-1 ring-blue-400/40 transition-transform hover:scale-105 focus:scale-105"
            >
              <BookOpen size={16} />
              Read the reading guide
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
              className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-6 py-3 text-sm font-semibold text-slate-100 backdrop-blur transition-colors hover:bg-slate-800/80"
            >
              <Download size={16} />
              Reading guide (PDF)
            </Link>
            <Link
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-6 py-3 text-sm font-semibold text-slate-100 backdrop-blur transition-colors hover:bg-slate-800/80"
            >
              <Github size={16} />
              Code &amp; verification
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

/**
 * The scope guard: the [E]/[C]/[O] discipline made visible in the first
 * viewport, so a skeptical reader sees the separation before reading any
 * single claim. Status is encoded as text + marker (not colour alone) for
 * accessibility; colours mirror the /verification marker legend.
 */
const SCOPE_GUARD: { marker: string; label: string; meaning: string; tone: string }[] = [
  {
    marker: "[E]",
    label: "Exact",
    meaning: "Identities, Lie/lattice theorems, Lean-formalised carrier, numerical fixed points",
    tone: "border-emerald-400/30 bg-emerald-500/10 text-emerald-200",
  },
  {
    marker: "[C]",
    label: "Conditional",
    meaning: "Physical bridges and readouts that hold under named hypotheses",
    tone: "border-amber-400/30 bg-amber-500/10 text-amber-200",
  },
  {
    marker: "[O]",
    label: "Open",
    meaning: "Declared inputs (c₃, g_car), the scale anchor v_geo, and one geometric premise",
    tone: "border-rose-400/30 bg-rose-500/10 text-rose-200",
  },
];

function ScopeGuard() {
  return (
    <div
      aria-label="Claim scope: exact, conditional, open — separated by a machine-checked ledger"
      className="mt-6 flex w-full max-w-3xl flex-col gap-2 sm:flex-row sm:flex-wrap sm:justify-center"
    >
      {SCOPE_GUARD.map((s) => (
        <div
          key={s.label}
          className={cn(
            "flex items-start gap-2 rounded-xl border px-3 py-2 text-left sm:flex-1 sm:basis-56",
            s.tone,
          )}
        >
          <span className="mt-px font-mono text-xs font-semibold">{s.marker}</span>
          <span className="leading-tight">
            <span className="block text-xs font-semibold uppercase tracking-wider">
              {s.label}
            </span>
            <span className="block text-[11px] leading-snug text-slate-300/90">
              {s.meaning}
            </span>
          </span>
        </div>
      ))}
    </div>
  );
}

const STATS: Array<{
  label: string;
  value: string;
  note: string;
  isMath?: boolean;
}> = [
  {
    label: "Axioms",
    value: "2",
    note: "c₃ = 1/(8π) and g_car = 5; everything else is a consequence",
  },
  {
    label: "Test surfaces",
    value: String(TEST_SURFACES),
    note: "Status-graded readouts and kill criteria, each with a marker",
  },
  {
    label: "Fitted constants",
    value: "0",
    note: "In the closed branch; only π stays irreducible after the bootstrap",
  },
  {
    label: "Open interfaces",
    value: "3",
    note: "v_geo scale anchor + G_net metric inclusion + F_transfer — explicitly open",
  },
];
