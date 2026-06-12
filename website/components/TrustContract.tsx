"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ListChecks, Play, ShieldAlert, Unlock } from "lucide-react";

const MARKERS: { m: string; label: string; tone: string }[] = [
  { m: "[E]", label: "Formalised", tone: "text-blue-200 ring-blue-400/30 bg-blue-500/10" },
  { m: "[E]", label: "Lattice", tone: "text-cyan-200 ring-cyan-400/30 bg-cyan-500/10" },
  { m: "[E]", label: "Identity", tone: "text-emerald-200 ring-emerald-400/30 bg-emerald-500/10" },
  { m: "[E]", label: "Numerical", tone: "text-violet-200 ring-violet-400/30 bg-violet-500/10" },
  { m: "[C]", label: "Conditional", tone: "text-amber-200 ring-amber-400/30 bg-amber-500/10" },
  { m: "[O]", label: "Open", tone: "text-rose-200 ring-rose-400/30 bg-rose-500/10" },
];

const ACTIONS: {
  href: string;
  label: string;
  icon: typeof ListChecks;
}[] = [
  { href: "/verification", label: "Claim ledger & scripts", icon: ListChecks },
  { href: "/verification#dag", label: "Run a check live", icon: Play },
  { href: "/falsification", label: "How to kill TFPT", icon: ShieldAlert },
  { href: "/#open-gates", label: "What's still open", icon: Unlock },
];

/**
 * The "trust contract" strip: it sits directly under the hero so a sceptical
 * reader sees the status discipline before the big claims — every claim is
 * graded and resolves to a single machine-checked ledger.
 */
export function TrustContract() {
  return (
    <section
      aria-labelledby="trust-contract-heading"
      className="relative -mt-8 pb-4"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.1 }}
          transition={{ duration: 0.6 }}
          className="glass rounded-2xl ring-1 ring-slate-700/40"
        >
          <div className="flex flex-col gap-4 p-5 sm:p-6 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <h2
                id="trust-contract-heading"
                className="font-serif text-lg font-semibold text-slate-50"
              >
                Every claim has a grade. The ledger wins.
              </h2>
              <p className="mt-1 max-w-xl text-sm leading-relaxed text-slate-400">
                Read this as a checkable research artifact, not a landing page.
                Each result is typed, machine-verified, or explicitly open — and
                a single versioned ledger is the source of truth.
              </p>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {MARKERS.map((x) => (
                  <span
                    key={x.m}
                    className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-medium ring-1 ${x.tone}`}
                  >
                    <span className="font-mono font-semibold">{x.m}</span>
                    {x.label}
                  </span>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2 sm:flex sm:flex-wrap lg:flex-col lg:items-stretch">
              {ACTIONS.map((a) => {
                const Icon = a.icon;
                return (
                  <Link
                    key={a.href}
                    href={a.href}
                    className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-4 py-2 text-xs font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
                  >
                    <Icon size={14} className="flex-none text-blue-300" aria-hidden />
                    {a.label}
                  </Link>
                );
              })}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
