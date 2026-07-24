"use client";

import { motion } from "motion/react";
import { Check, CircleDashed, TriangleAlert } from "lucide-react";

/**
 * WoitBridgeProgress -- compact stage bar for WOIT.OS.TWISTOR.01 (the
 * Osterwalder-Schrader twistor bridge): alpha / beta1 / beta2 executed,
 * beta3 open under the straddle-law constraint (v529), the straddle filter
 * since executed as a selector with a unique survivor (v534). Contract
 * stays [O].
 */

type StageState = "done" | "open";

interface Stage {
  id: string;
  label: string;
  sub: string;
  src: string;
  state: StageState;
}

const STAGES: Stage[] = [
  {
    id: "alpha",
    label: "α",
    sub: "Θ exists at the free level; free RP selects the same family",
    src: "v519",
    state: "done",
  },
  {
    id: "beta1",
    label: "β₁",
    sub: "the μ₄ clock is the euclidean rotation; gaugeable datum = the GSO ℤ₂; gauge-fixed RP holds",
    src: "v522",
    state: "done",
  },
  {
    id: "beta2",
    label: "β₂",
    sub: "OS quotient explicit: H_phys positive definite, the clock a positive transfer operator with spectral calculus",
    src: "v524",
    state: "done",
  },
  {
    id: "beta3",
    label: "β₃",
    sub: "next — under the straddle-law constraint",
    src: "open",
    state: "open",
  },
];

export function WoitBridgeProgress() {
  return (
    <div className="mt-8 overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4 sm:p-6">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h4 className="font-serif text-base font-semibold text-slate-50">
          The OS twistor bridge — <span className="font-mono">WOIT.OS.TWISTOR.01</span>
        </h4>
        <span className="rounded-full bg-fuchsia-500/15 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-fuchsia-200 ring-1 ring-fuchsia-400/30">
          research contract · [O]
        </span>
      </div>

      <p className="mt-2 text-xs leading-relaxed text-slate-400">
        The actual bridge from compiler to physics: a global real structure Θ plus interacting
        reflection positivity plus OS reconstruction on the twistorial algebra. Three of its
        preregistered stages are executed; the contract itself stays open.
      </p>

      <div className="mt-4 grid gap-2 sm:grid-cols-4">
        {STAGES.map((s, i) => (
          <motion.div
            key={s.id}
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.35, delay: i * 0.08 }}
            className={`rounded-xl border p-3 ${
              s.state === "done"
                ? "border-emerald-400/25 bg-emerald-500/[0.05]"
                : "border-slate-600/40 bg-slate-800/20"
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5 font-mono text-sm font-semibold text-slate-100">
                {s.state === "done" ? (
                  <Check size={13} className="text-emerald-300" aria-hidden />
                ) : (
                  <CircleDashed size={13} className="text-slate-400" aria-hidden />
                )}
                {s.label}
              </span>
              <span
                className={`rounded px-1.5 py-0.5 font-mono text-[9px] font-semibold ${
                  s.state === "done"
                    ? "bg-emerald-500/15 text-emerald-200"
                    : "bg-slate-700/40 text-slate-300"
                }`}
              >
                {s.src}
              </span>
            </div>
            <p className="mt-1.5 text-[11px] leading-snug text-slate-400">{s.sub}</p>
          </motion.div>
        ))}
      </div>

      <div className="mt-3 flex items-start gap-2 rounded-md border border-amber-400/30 bg-amber-500/[0.06] p-3 text-[11px] leading-relaxed text-amber-100/90">
        <TriangleAlert size={14} className="mt-0.5 flex-none text-amber-300" aria-hidden />
        <span>
          <strong className="text-amber-100">Toy-level kill, honestly banked (v529).</strong>{" "}
          On the first genuinely interacting seam toy, Kill-Test 2 fires: reflection positivity
          breaks for every <span className="font-mono">g &gt; 0</span> following the{" "}
          <em>straddle law</em> (RP fails exactly on quartet-straddled cuts, 24/24). Fenced — one
          toy, one interaction class — this is a named threat <em>and</em> the first hard selection
          principle: every candidate <span className="font-mono">A_hol</span> must pass the
          straddle filter. Executed as a selector (v534), the filter keeps exactly{" "}
          <em>one</em> member alive: reflection positivity dynamically selects the alignment bit{" "}
          <span className="font-mono">δ = π/2</span> with positive coupling — the symmetric
          straddling of the self-mirror member protects RP where every asymmetric member dies.
          No marker moves; the contract stays [O].
        </span>
      </div>
    </div>
  );
}
