"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { cn } from "@/lib/utils";

const MARKER_TONE: Record<string, string> = {
  "[I]": "text-emerald-200 bg-emerald-500/15 ring-emerald-400/30",
  "[N]": "text-violet-200 bg-violet-500/15 ring-violet-400/30",
  "[P]": "text-amber-200 bg-amber-500/15 ring-amber-400/30",
};

function markerTone(marker: string) {
  return MARKER_TONE[marker.split("/")[0].trim()] ?? MARKER_TONE["[I]"];
}

interface Row {
  q: string;
  sm: string;
  smKind: "input" | "fitted" | "unexplained";
  tfpt: string;
  marker: string;
}

const ROWS: Row[] = [
  {
    q: "Fine-structure constant α⁻¹",
    sm: "measured input",
    smKind: "input",
    tfpt: "unique root of F_U(1)(α) = 0",
    marker: "[N]",
  },
  {
    q: "Number of fermion families",
    sm: "input (= 3, observed)",
    smKind: "input",
    tfpt: "N_fam = 3 from ℙ¹∖μ₄ = A₃",
    marker: "[I]",
  },
  {
    q: "Hypercharge assignments",
    sm: "input (anomaly-chosen)",
    smKind: "input",
    tfpt: "roots of x² − x − 6 = 0 on the 3+2 carrier",
    marker: "[I]",
  },
  {
    q: "Higgs doublet count",
    sm: "input (= 1)",
    smKind: "input",
    tfpt: "N_Φ = g_car − |μ₄| = 1",
    marker: "[I]",
  },
  {
    q: "Flavor / CKM / PMNS structure",
    sm: "fitted by hand",
    smKind: "fitted",
    tfpt: "one φ₀-ladder + residue matrix R (det 8)",
    marker: "[I]/[N]",
  },
  {
    q: "Solar mixing angle θ₁₂",
    sm: "fitted",
    smKind: "fitted",
    tfpt: "1/3 − φ₀/2 = 0.3067 (conditional)",
    marker: "[N]/[P]",
  },
  {
    q: "Strong-CP phase θ̄",
    sm: "unexplained (tuned ≈ 0)",
    smKind: "unexplained",
    tfpt: "structural null θ_eff = 0",
    marker: "[I]",
  },
  {
    q: "Inflation / scalaron scale",
    sm: "free parameter",
    smKind: "fitted",
    tfpt: "seam-fixed M = c₃^(7/2) M̄",
    marker: "[I]",
  },
];

const SM_KIND_TONE: Record<Row["smKind"], string> = {
  input: "text-slate-400",
  fitted: "text-rose-300/80",
  unexplained: "text-amber-300/80",
};

const LEVELS: { level: string; time: string; label: string; href: string }[] = [
  { level: "Level 0", time: "30 sec", label: "Two axioms → E₈ → the SM (this page)", href: "/#overview" },
  { level: "Level 1", time: "5 min", label: "The reading guide", href: "/orientation" },
  { level: "Level 2", time: "30 min", label: "The four core documents", href: "/#papers" },
  { level: "Level 3", time: "full", label: "Papers + run the verification", href: "/verification" },
];

/**
 * "Why this matters" — the motivation the site was missing. It states the
 * physics problem (the Standard Model leaves ~20 numbers as inputs/fits) and
 * contrasts it with what TFPT derives, each with its honest status grade. The
 * TFPT column doubles as a per-topic status dashboard.
 */
export function WhyThisMatters() {
  return (
    <section
      id="why"
      className="relative scroll-mt-20 py-20 sm:py-24"
      aria-labelledby="why-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="Why this matters"
          title="The Standard Model works — but mostly by being told the answers"
          description="It takes roughly twenty numbers as input and fits the flavor sector by hand. It does not say why there are three families, why the hypercharges are what they are, or why the strong-CP phase is essentially zero. TFPT asks whether these share one boundary origin — and answers with a status-graded derivation, not a fit."
        />

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.05 }}
          transition={{ duration: 0.6 }}
          className="mt-10 overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/40"
        >
          <div className="grid grid-cols-[1.3fr_1fr_1.6fr] gap-px border-b border-slate-800/60 bg-slate-800/40 px-4 py-3 text-[10px] font-semibold uppercase tracking-widest text-slate-300 sm:px-5">
            <span>Quantity</span>
            <span>Standard Model</span>
            <span>TFPT</span>
          </div>
          <ul className="divide-y divide-slate-800/60">
            {ROWS.map((r, i) => (
              <motion.li
                key={r.q}
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true, amount: 0.05 }}
                transition={{ duration: 0.4, delay: i * 0.03 }}
                className="grid grid-cols-[1.3fr_1fr_1.6fr] items-start gap-3 px-4 py-3 transition-colors hover:bg-slate-900/40 sm:px-5"
              >
                <span className="text-sm font-medium text-slate-100">{r.q}</span>
                <span className={cn("text-xs leading-snug", SM_KIND_TONE[r.smKind])}>
                  {r.sm}
                </span>
                <span className="flex flex-wrap items-start gap-2">
                  <span
                    className={cn(
                      "mt-0.5 flex-none rounded-full px-1.5 py-0.5 font-mono text-[10px] font-semibold ring-1",
                      markerTone(r.marker),
                    )}
                  >
                    {r.marker}
                  </span>
                  <span className="text-xs leading-snug text-slate-200">{r.tfpt}</span>
                </span>
              </motion.li>
            ))}
          </ul>
          <div className="border-t border-slate-800/60 px-4 py-3 text-[11px] leading-relaxed text-slate-400 sm:px-5">
            Status grades: <span className="font-mono text-emerald-300">[I]</span> exact
            identity · <span className="font-mono text-violet-300">[N]</span> numerical
            fixed point · <span className="font-mono text-amber-300">[P]</span> conditional.
            Nothing in the TFPT column is fitted to the Standard-Model value — each is
            re-derived from the two axioms and machine-checked.
          </div>
        </motion.div>

        {/* Reading levels — start at your depth */}
        <div className="mt-8">
          <div className="mb-3 text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
            Start at your depth
          </div>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {LEVELS.map((l) => (
              <Link
                key={l.level}
                href={l.href}
                className="group flex flex-col rounded-xl border border-slate-700/40 bg-slate-950/40 p-4 transition-colors hover:border-blue-400/40 hover:bg-blue-500/5"
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-semibold text-blue-300">
                    {l.level}
                  </span>
                  <span className="rounded-full bg-slate-800/60 px-2 py-0.5 text-[10px] font-mono text-slate-400">
                    {l.time}
                  </span>
                </div>
                <span className="mt-2 flex items-center gap-1.5 text-sm text-slate-200">
                  {l.label}
                  <ArrowRight
                    size={13}
                    className="flex-none text-slate-600 transition-transform group-hover:translate-x-0.5 group-hover:text-blue-300"
                    aria-hidden
                  />
                </span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
