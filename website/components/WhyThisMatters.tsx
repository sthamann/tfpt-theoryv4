"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { cn } from "@/lib/utils";

const MARKER_TONE: Record<string, string> = {
  "[E]": "text-emerald-200 bg-emerald-500/15 ring-emerald-400/30",
  "[C]": "text-amber-200 bg-amber-500/15 ring-amber-400/30",
  "[O]": "text-rose-200 bg-rose-500/15 ring-rose-400/30",
};

function markerTone(marker: string) {
  return MARKER_TONE[marker.split("/")[0].trim()] ?? MARKER_TONE["[E]"];
}

interface Row {
  q: string;
  plain: string;
  sm: string;
  smKind: "input" | "fitted" | "unexplained";
  tfpt: string;
  marker: string;
}

const ROWS: Row[] = [
  {
    q: "Fine-structure constant α⁻¹",
    plain: "Why light couples at ~1/137",
    sm: "measured input",
    smKind: "input",
    tfpt: "unique root of F_U(1)(α) = 0",
    marker: "[E]",
  },
  {
    q: "Number of fermion families",
    plain: "Why matter comes in threes",
    sm: "input (= 3, observed)",
    smKind: "input",
    tfpt: "N_fam = 3 from ℙ¹∖μ₄ = A₃",
    marker: "[E]",
  },
  {
    q: "Hypercharge assignments",
    plain: "Why electric charges take their values",
    sm: "input (anomaly-chosen)",
    smKind: "input",
    tfpt: "roots of x² − x − 6 = 0 on the 3+2 carrier",
    marker: "[E]",
  },
  {
    q: "Higgs doublet count",
    plain: "Why there is one Higgs doublet",
    sm: "input (= 1)",
    smKind: "input",
    tfpt: "N_Φ = g_car − |μ₄| = 1",
    marker: "[E]",
  },
  {
    q: "Flavor / CKM / PMNS structure",
    plain: "Why mixing angles are not free dials",
    sm: "fitted by hand",
    smKind: "fitted",
    tfpt: "one φ₀-ladder + residue matrix R (det 8)",
    marker: "[E]",
  },
  {
    q: "Solar mixing angle θ₁₂",
    plain: "A frozen number for JUNO to hit or miss",
    sm: "fitted",
    smKind: "fitted",
    tfpt: "1/3 − φ₀/2 = 0.3067 (conditional)",
    marker: "[E]/[C]",
  },
  {
    q: "Strong-CP phase θ̄",
    plain: "Why the neutron electric dipole is tiny",
    sm: "unexplained (tuned ≈ 0)",
    smKind: "unexplained",
    tfpt: "structural null θ_eff = 0",
    marker: "[E]",
  },
  {
    q: "Inflation / scalaron scale",
    plain: "Why the early-universe scale is fixed",
    sm: "free parameter",
    smKind: "fitted",
    tfpt: "seam-fixed M = c₃^(7/2) M̄",
    marker: "[E]",
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
  { level: "Level 2", time: "30 min", label: "The four core documents", href: "/papers" },
  { level: "Level 3", time: "full", label: "Papers + run the verification", href: "/verification" },
];

/**
 * "Why this matters" — SM vs TFPT contrast with a plain-English reading per row.
 */
export function WhyThisMatters() {
  return (
    <section
      id="why"
      className="relative scroll-mt-20 py-16 sm:py-20"
      aria-labelledby="why-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="Derived vs. fitted"
          title="The Standard Model takes ~20 numbers as input; TFPT derives the structure"
          description="The Standard Model takes roughly twenty parameters as input and fits the flavor sector by hand. It does not say why there are three families, why the hypercharges take the values they do, or why the strong-CP phase is essentially zero. TFPT asks whether these share one boundary origin — and answers with a status-graded derivation, not a fit."
        />

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.05 }}
          transition={{ duration: 0.6 }}
          className="mt-10 overflow-hidden border border-slate-700/40 bg-slate-950/40"
        >
          {/* Desktop header */}
          <div className="hidden grid-cols-[1.1fr_1.1fr_0.9fr_1.5fr] gap-px border-b border-slate-800/60 bg-slate-800/40 px-4 py-3 text-[10px] font-semibold uppercase tracking-widest text-slate-300 sm:grid sm:px-5">
            <span>Quantity</span>
            <span>In plain English</span>
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
                className="grid gap-2 px-4 py-3 transition-colors hover:bg-slate-900/40 sm:grid-cols-[1.1fr_1.1fr_0.9fr_1.5fr] sm:items-start sm:gap-3 sm:px-5"
              >
                <span className="text-sm font-medium text-slate-100">{r.q}</span>
                <span className="text-xs leading-snug text-slate-400">{r.plain}</span>
                <span className={cn("text-xs leading-snug", SM_KIND_TONE[r.smKind])}>
                  <span className="mr-1 font-mono text-[10px] uppercase tracking-wider text-slate-600 sm:hidden">
                    SM ·
                  </span>
                  {r.sm}
                </span>
                <span className="flex flex-wrap items-start gap-2">
                  <span
                    className={cn(
                      "mt-0.5 flex-none rounded-sm px-1.5 py-0.5 font-mono text-[10px] font-semibold ring-1",
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
            Status grades: <span className="font-mono text-emerald-300">[E]</span> exact /
            machine-proven · <span className="font-mono text-amber-300">[C]</span> conditional
            (named hypotheses) · <span className="font-mono text-rose-300">[O]</span> open / axiom.
            Nothing in the TFPT column is fitted to the Standard-Model value — each is
            re-derived from the two axioms and machine-checked.
          </div>
        </motion.div>

        <div className="mt-8">
          <div className="mb-3 text-[11px] font-semibold uppercase tracking-widest text-slate-400">
            Start at your depth
          </div>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {LEVELS.map((l) => (
              <Link
                key={l.level}
                href={l.href}
                className="group flex flex-col border border-slate-700/40 bg-slate-950/40 p-4 transition-colors hover:border-blue-400/40 hover:bg-blue-500/5"
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-semibold text-blue-300">
                    {l.level}
                  </span>
                  <span className="border border-slate-700/50 bg-slate-900/60 px-2 py-0.5 font-mono text-[10px] text-slate-400">
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
