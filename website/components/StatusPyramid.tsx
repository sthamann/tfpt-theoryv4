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
    label: "Theorem core",
    short: "Theorem core",
    examples: "Boundary primitive kernel · carrier rigidity · joint discrete solve",
    tone: "from-blue-600 to-blue-500",
    ring: "ring-blue-400/40",
    text: "text-blue-100",
    width: "w-full",
  },
  {
    level: 2,
    label: "Derived structural output",
    short: "Derived structure",
    examples: "SM packet · 3 families · gauge quotient · N_Φ = 1 · b₁ = 41/10",
    tone: "from-blue-500 to-cyan-500",
    ring: "ring-cyan-400/40",
    text: "text-blue-50",
    width: "w-[88%]",
  },
  {
    level: 3,
    label: "Bridge readout",
    short: "Bridge readout",
    examples: "α⁻¹(0) · λ_C · sin²θ_13 · CKM · PMNS · β_rad",
    tone: "from-emerald-500 to-teal-500",
    ring: "ring-emerald-400/40",
    text: "text-emerald-50",
    width: "w-[76%]",
  },
  {
    level: 4,
    label: "Conditional closure",
    short: "Conditional closure",
    examples:
      "P_adm · OS reconstruction · local Minkowski net · admissible RG flow",
    tone: "from-orange-500 to-red-500",
    ring: "ring-orange-400/40",
    text: "text-orange-50",
    width: "w-[64%]",
  },
  {
    level: 5,
    label: "Downstream interface",
    short: "Downstream",
    examples: "Λ_IR · seam transfer · axion 15.764 GHz · η_B · Σ m_ν · m_ββ",
    tone: "from-fuchsia-500 to-pink-500",
    ring: "ring-fuchsia-400/40",
    text: "text-fuchsia-50",
    width: "w-[52%]",
  },
  {
    level: 6,
    label: "Conjectural / programmatic",
    short: "Conjectural target",
    examples: "CMB Stage 2 · sky realization · transient channels · E8 atlas",
    tone: "from-slate-600 to-slate-700",
    ring: "ring-slate-400/30",
    text: "text-slate-200",
    width: "w-[40%]",
    dashed: true,
  },
];

export function StatusPyramid() {
  return (
    <div className="glass rounded-2xl ring-1 ring-slate-700/40">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          Proof-status pyramid — not all outputs share the same status
        </span>
        <span className="rounded-full bg-slate-800/60 px-2.5 py-0.5 text-[10px] font-mono uppercase tracking-widest text-slate-300 ring-1 ring-slate-700/40">
          Burden of proof, top{" "}
          <span className="math-label">→</span> bottom
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
          <strong className="text-slate-200">Reading rule.</strong> Higher
          layers are the foundation. Each lower layer{" "}
          <em>depends on</em> the layers above and inherits stricter
          falsification surface, but the <em>proof status weakens</em>:
          theorem-core claims fail with a single counterexample; downstream
          interfaces fail only against a declared comparison convention;
          conjectural targets fail only as programmatic predictions.
        </p>
      </div>
    </div>
  );
}
