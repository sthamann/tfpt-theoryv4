"use client";

import { motion } from "motion/react";

interface Layer {
  level: number;
  label: string;
  short: string;
  examples: string;
  tone: string;
  ring: string;
  text: string;
  width: string;
  dashed?: boolean;
}

const LAYERS: Layer[] = [
  {
    level: 1,
    label: "[O] Axioms — declared inputs",
    short: "Axiom",
    examples: "c₃ = 1/(8π) (P1) · five-slot carrier g_car = 5 (P2 — since v108–v113 reduced to the boundary-net premise: gate closes ⇒ carrier becomes [E])",
    tone: "from-slate-600 to-slate-500",
    ring: "ring-slate-400/40",
    text: "text-slate-100",
    width: "w-full",
  },
  {
    level: 2,
    label: "[E] Formalised — Lean / exact script",
    short: "Formal",
    examples: "P2 algebra (Lean, 0 sorry) · E₈ glue machine-checked",
    tone: "from-blue-600 to-blue-500",
    ring: "ring-blue-400/40",
    text: "text-blue-50",
    width: "w-[88%]",
  },
  {
    level: 3,
    label: "[E] Lattice / Lie theorem",
    short: "Lattice",
    examples: "E₈ = (D₅ ⊕ A₃) + μ₄ · bootstrap μ² − 5μ + 4 = 0 · order-30 Coxeter",
    tone: "from-cyan-500 to-blue-500",
    ring: "ring-cyan-400/40",
    text: "text-cyan-50",
    width: "w-[76%]",
  },
  {
    level: 4,
    label: "[E] Exact identity",
    short: "Identity",
    examples: "240 = 16·5·3 · 248 = 240+8 · b₁ = 41/10 · det R = 8 · χ_R",
    tone: "from-emerald-500 to-teal-500",
    ring: "ring-emerald-400/40",
    text: "text-emerald-50",
    width: "w-[64%]",
  },
  {
    level: 5,
    label: "[E] Numerical fixed point",
    short: "Numerical",
    examples: "α⁻¹ = 137.0359992 · sin²θ₁₂ = 0.3067 · sin²θ₁₃ = 0.0231 · β_rad",
    tone: "from-violet-500 to-fuchsia-500",
    ring: "ring-violet-400/40",
    text: "text-violet-50",
    width: "w-[52%]",
  },
  {
    level: 6,
    label: "[C]/[O] Conditional & open",
    short: "Conditional / open",
    examples: "masses · A_s, n_s, r · η_B · Koide · (U_wall) flavor · (G_metric) QG",
    tone: "from-amber-500 to-orange-600",
    ring: "ring-amber-400/40",
    text: "text-amber-50",
    width: "w-[40%]",
    dashed: true,
  },
];

export function StatusPyramid() {
  return (
    <div className="glass rounded-2xl ring-1 ring-slate-700/40">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          The claim stack — not all outputs share the same grade
        </span>
        <span className="rounded-full bg-slate-800/60 px-2.5 py-0.5 text-[10px] font-mono uppercase tracking-widest text-slate-300 ring-1 ring-slate-700/40">
          Foundation{" "}
          <span className="math-label">→</span> conditional
        </span>
      </div>

      <div className="space-y-2 p-6 sm:p-8">
        {LAYERS.map((l, i) => (
          <motion.div
            key={l.level}
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.05 }}
            transition={{ duration: 0.5, delay: i * 0.06 }}
            className={`relative mx-auto overflow-hidden rounded-xl bg-gradient-to-r ${l.tone} ${l.ring} ring-1 ${l.width}`}
            style={l.dashed ? { boxShadow: "inset 0 0 0 1px rgba(255,255,255,0.08)" } : undefined}
          >
            {l.dashed && (
              <div
                aria-hidden="true"
                className="pointer-events-none absolute inset-0 rounded-xl"
                style={{
                  backgroundImage:
                    "repeating-linear-gradient(45deg, rgba(255,255,255,0.04) 0 8px, transparent 8px 16px)",
                }}
              />
            )}
            <div className="relative grid gap-2 px-4 py-3 sm:grid-cols-[auto_1fr_auto] sm:items-center sm:gap-4">
              <span
                className={`flex h-7 w-7 flex-none items-center justify-center rounded-full bg-black/30 font-mono text-xs font-semibold ${l.text} ring-1 ring-white/15`}
              >
                {l.level}
              </span>
              <div className="min-w-0">
                <div className={`text-[11px] font-semibold uppercase tracking-widest ${l.text} opacity-90`}>
                  {l.label}
                </div>
                <div className="text-xs leading-snug text-white/85">
                  {l.examples}
                </div>
              </div>
              <span className={`hidden text-[10px] font-mono uppercase tracking-widest text-white/70 sm:inline-block`}>
                {l.short}
              </span>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="border-t border-slate-800/60 px-6 py-4 sm:px-8">
        <p className="text-xs leading-relaxed text-slate-400">
          <strong className="text-slate-200">Reading rule.</strong> The two
          axioms at the top are the foundation; each lower band{" "}
          <em>depends on</em> the bands above. Exact identities and lattice
          theorems fail with a single counterexample; numerical fixed points
          fail against a declared comparison; conditional and open items fail
          only as named hypotheses. The single source of truth for which claim
          sits where is the machine-checked status ledger — if the text and the
          ledger ever disagree, the ledger wins.
        </p>
      </div>
    </div>
  );
}
