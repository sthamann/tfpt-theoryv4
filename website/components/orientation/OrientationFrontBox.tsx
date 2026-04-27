"use client";

import { motion } from "motion/react";
import { Compass, ShieldCheck, XOctagon, Crosshair } from "lucide-react";
import type { LucideIcon } from "lucide-react";

const ITEMS: {
  icon: LucideIcon;
  title: string;
  body: string;
  tone: string;
}[] = [
  {
    icon: Compass,
    title: "Inputs from previous papers",
    body: "None. This is the public orientation layer for the series.",
    tone: "from-blue-500/15 to-cyan-500/10 ring-blue-400/25",
  },
  {
    icon: ShieldCheck,
    title: "New theorem contribution",
    body: "None. The note contributes only organization, status discipline, and a dependency map.",
    tone: "from-emerald-500/15 to-teal-500/10 ring-emerald-400/25",
  },
  {
    icon: XOctagon,
    title: "Not claimed here",
    body: "No carrier proof, no exact electromagnetic calculation, no CMB fit, no mass ledger, no E8 stage atlas, and no nonperturbative QFT proof.",
    tone: "from-slate-500/15 to-slate-500/5 ring-slate-400/25",
  },
  {
    icon: Crosshair,
    title: "Falsification or audit surface",
    body: "The note can fail if it misstates the dependency order, overstates the status of a downstream module, or hides where an assumption first enters.",
    tone: "from-orange-500/15 to-amber-500/10 ring-orange-400/25",
  },
];

export function OrientationFrontBox() {
  return (
    <section
      id="frontbox"
      aria-labelledby="frontbox-heading"
      className="relative scroll-mt-24 py-16"
    >
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <h2 id="frontbox-heading" className="sr-only">
          Front-box: inputs, contribution, exclusions, falsification surface
        </h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {ITEMS.map((it, i) => {
            const Icon = it.icon;
            return (
              <motion.div
                key={it.title}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.05 }}
                transition={{ duration: 0.6, delay: i * 0.08 }}
                className={`relative overflow-hidden rounded-2xl bg-gradient-to-br p-5 ring-1 ${it.tone}`}
              >
                <div className="flex items-center gap-2.5">
                  <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-950/40 ring-1 ring-white/10">
                    <Icon size={16} className="text-slate-100" />
                  </span>
                  <h3 className="font-serif text-base font-semibold text-slate-50">
                    {it.title}
                  </h3>
                </div>
                <p className="mt-3 text-sm leading-relaxed text-slate-300">
                  {it.body}
                </p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
