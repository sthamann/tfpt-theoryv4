"use client";

import { motion } from "motion/react";
import Image from "next/image";
import Link from "next/link";
import {
  ShieldCheck,
  Dice5,
  Crosshair,
  Layers,
  GitBranch,
  ArrowRight,
} from "lucide-react";
import { SectionHeader } from "@/components/SectionHeader";

const STATS: {
  big: string;
  small: string;
  icon: typeof ShieldCheck;
  tone: string;
}[] = [
  {
    big: "13 / 13",
    small: "TFPT hits all 13 frozen observables; 200k random pseudo-theories reach ≤ 5/13.",
    icon: Dice5,
    tone: "text-emerald-300",
  },
  {
    big: "≈ 4.40σ",
    small: "Assumption-minimal counting floor: of 94,500 declared F_U(1) variants exactly one α path lands in the CODATA window (1 in 94,500), with no subjective probability (v436).",
    icon: Crosshair,
    tone: "text-blue-300",
  },
  {
    big: "3 / 8",
    small: "Only 3 of 8 E₈ Casimir degrees feed a readout — and the 5/8 overhead is forced two-family structure (6·spine ⊔ det-ladder, v431), not diffuse slack.",
    icon: Layers,
    tone: "text-cyan-300",
  },
  {
    big: "≤ 10⁻³⁰·⁷",
    small: "≈ 102 bits that a random theory of equal complexity reproduces the scorecard — conditional on the declared grammar (v100).",
    icon: ShieldCheck,
    tone: "text-violet-300",
  },
];

const LAYERS: string[] = [
  "Status calculus — no [C] dressed as [E]",
  "No free pattern + reverse audit (3/8)",
  "Over-determination map — 7 readouts compress one object",
  "Firewall + No-Unit theorem",
  "Frozen registry + Monte-Carlo null model",
  "Two independent paths — Wolfram + Lean",
  "Red team — Targets A–F + kill tests",
];

const FIGS: { src: string; w: number; h: number; cap: string }[] = [
  {
    src: "/figures/safeguard_null_model.png",
    w: 1080,
    h: 510,
    cap: "Look-elsewhere null model: pseudo-theories hit ≤ 5/13, TFPT hits 13/13.",
  },
  {
    src: "/figures/safeguard_witness_map.png",
    w: 1290,
    h: 750,
    cap: "The seven arithmetic readouts are facets of one (2,3,5)/E₈ object — they compress, not multiply; what genuinely multiplies is the input forced four ways (the '8' in c₃) plus the foreign α⁻¹≈137.",
  },
  {
    src: "/figures/safeguard_alpha_uniqueness.png",
    w: 1170,
    h: 540,
    cap: "α⁻¹ is a unique fixed point: one variant of 94,500 lands in the CODATA window.",
  },
  {
    src: "/figures/safeguard_reverse_audit.png",
    w: 1170,
    h: 450,
    cap: "Reverse audit: only 3/8 E₈ degrees feed a readout — the 5/8 overhead is forced two-family structure (6·spine ⊔ det-ladder, v431), published not hidden.",
  },
];

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.07 } },
};
const item = {
  hidden: { opacity: 0, y: 18 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

/**
 * The "why this isn't numerology" band: a prominent, visual statement of the
 * layered anti-coincidence discipline (null model, α uniqueness, reverse audit,
 * over-determination) — sits in the trust beat of the narrative arc and links to
 * the Safeguards paper.
 */
export function Safeguards() {
  return (
    <section
      id="safeguards"
      aria-labelledby="safeguards-heading"
      className="relative border-t border-slate-800/60 py-16 sm:py-20"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          id="safeguards-heading"
          eyebrow="Safeguards"
          title="Why this isn't numerology"
          description="A two-input theory with many small integers is, a priori, at numerology risk. TFPT answers with a layered, machine-checked discipline — making coincidence an expensive explanation of the discrete core, and never letting exact compiler closure pass for closed physics."
        />

        {/* headline statistics */}
        <motion.div
          variants={container}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.2 }}
          className="mt-8 grid grid-cols-2 gap-3 lg:grid-cols-4"
        >
          {STATS.map((s) => {
            const Icon = s.icon;
            return (
              <motion.div
                key={s.big}
                variants={item}
                className="glass rounded-2xl p-4 ring-1 ring-slate-700/40"
              >
                <Icon size={18} className={s.tone} aria-hidden />
                <div className={`mt-2 font-serif text-2xl font-semibold ${s.tone}`}>
                  {s.big}
                </div>
                <p className="mt-1 text-xs leading-relaxed text-slate-400">
                  {s.small}
                </p>
              </motion.div>
            );
          })}
        </motion.div>

        {/* the seven layers */}
        <motion.ol
          variants={container}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.15 }}
          className="mt-8 grid gap-2 sm:grid-cols-2 lg:grid-cols-3"
        >
          {LAYERS.map((l, i) => (
            <motion.li
              key={l}
              variants={item}
              className="flex items-center gap-3 rounded-xl border border-slate-700/40 bg-slate-900/50 px-3 py-2.5"
            >
              <span className="flex h-6 w-6 flex-none items-center justify-center rounded-full bg-emerald-500/15 text-xs font-semibold text-emerald-300">
                {i + 1}
              </span>
              <span className="text-xs leading-snug text-slate-300">{l}</span>
            </motion.li>
          ))}
        </motion.ol>

        {/* the figures */}
        <motion.div
          variants={container}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.1 }}
          className="mt-8 grid gap-4 sm:grid-cols-2"
        >
          {FIGS.map((f) => (
            <motion.figure
              key={f.src}
              variants={item}
              className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40"
            >
              <Image
                src={f.src}
                width={f.w}
                height={f.h}
                alt={f.cap}
                sizes="(max-width: 640px) 100vw, 50vw"
                className="w-full bg-white"
                style={{ height: "auto" }}
              />
              <figcaption className="px-4 py-3 text-xs leading-relaxed text-slate-400">
                {f.cap}
              </figcaption>
            </motion.figure>
          ))}
        </motion.div>

        {/* calls to action */}
        <div className="mt-8 flex flex-wrap gap-3">
          <Link
            href="/papers/safeguards"
            className="inline-flex items-center gap-2 rounded-full bg-emerald-500/15 px-5 py-2.5 text-sm font-semibold text-emerald-200 ring-1 ring-emerald-400/30 transition-colors hover:bg-emerald-500/25"
          >
            Read the Safeguards paper <ArrowRight size={15} aria-hidden />
          </Link>
          <Link
            href="/verification"
            className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-5 py-2.5 text-sm font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
          >
            <GitBranch size={15} className="text-blue-300" aria-hidden /> The
            verification suite
          </Link>
        </div>
      </div>
    </section>
  );
}
