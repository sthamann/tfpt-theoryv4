"use client";

import { motion } from "motion/react";
import { Math } from "./Math";

const DECODERS = [
  {
    id: "Y",
    title: "Y",
    role: "Structure",
    bullets: [
      "3+2 carrier split",
      "Hypercharge generator",
      "SM packet, gauge quotient",
    ],
    accent: "from-blue-500 to-violet-500",
    chip: "bg-blue-500/15 text-blue-200 ring-blue-400/30",
  },
  {
    id: "uSigma",
    title: "[u_Σ] = 1",
    role: "Counting",
    bullets: [
      "N_fam = 3",
      "Ω_adm = 48",
      "N_Φ = 1, b₁ = 41/10",
    ],
    accent: "from-violet-500 to-fuchsia-500",
    chip: "bg-violet-500/15 text-violet-200 ring-violet-400/30",
  },
  {
    id: "phi0",
    title: "u = φ₀",
    role: "Bridge observables",
    bullets: [
      "λ_C, sin²θ_13, β_rad",
      "α via φ_seam(α)",
      "Cabibbo / PMNS / cosmic β",
    ],
    accent: "from-emerald-500 to-teal-500",
    chip: "bg-emerald-500/15 text-emerald-200 ring-emerald-400/30",
  },
];

export function ThreeDecoderMap() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
      className="glass mx-auto mt-12 max-w-5xl overflow-hidden rounded-2xl ring-1 ring-slate-700/40"
      aria-label="The three-decoder map: structure, counting, observables"
    >
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          One datum · Three decoders · One closed branch
        </span>
        <span className="rounded-full bg-slate-800/60 px-2.5 py-0.5 text-[10px] font-mono uppercase tracking-widest text-slate-300 ring-1 ring-slate-700/40">
          15-second overview
        </span>
      </div>

      <div className="grid gap-0 lg:grid-cols-[1fr_auto_2fr]">
        {/* Left: trunk to joint solve */}
        <div className="border-b border-slate-800/60 p-6 lg:border-b-0 lg:border-r">
          <ol className="space-y-3 text-sm">
            <TrunkStep
              n="1"
              label="One-sided boundary datum"
              tex="\mathfrak{T}_\partial"
              accent="from-slate-400 to-slate-500"
            />
            <Arrow />
            <TrunkStep
              n="2"
              label="Primitive kernel"
              tex="(\tau_{\mathrm{dbl}},\iota_C,P_{\mathrm{prim}},[u_\Sigma],c_3)"
              accent="from-blue-500 to-violet-500"
            />
            <Arrow />
            <TrunkStep
              n="3"
              label="Joint discrete admissibility solve"
              tex="d^\star_{\mathrm{disc}}"
              accent="from-blue-500 to-violet-500"
              highlight
            />
          </ol>
        </div>

        {/* Center: three-way fan */}
        <div className="hidden items-center justify-center px-2 lg:flex">
          <div
            aria-hidden="true"
            className="h-full w-px bg-gradient-to-b from-transparent via-violet-400/40 to-transparent"
          />
        </div>

        {/* Right: three decoders + closed branch */}
        <div className="p-6">
          <div className="grid gap-3 sm:grid-cols-3">
            {DECODERS.map((d, i) => (
              <motion.div
                key={d.id}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.05 }}
                transition={{ duration: 0.5, delay: 0.2 + i * 0.08 }}
                className="relative overflow-hidden rounded-xl border border-slate-700/40 bg-slate-950/40 p-3"
              >
                <div
                  aria-hidden="true"
                  className={`absolute inset-x-0 top-0 h-px bg-gradient-to-r ${d.accent}`}
                />
                <div
                  className={`inline-block rounded-full px-2 py-0.5 text-[9px] font-semibold uppercase tracking-widest ring-1 ${d.chip}`}
                >
                  {d.role}
                </div>
                <div className="mt-2 text-base font-mono font-semibold text-slate-50">
                  <Math>{texOf(d.title)}</Math>
                </div>
                <ul className="mt-2 space-y-0.5 text-[11px] leading-snug text-slate-300">
                  {d.bullets.map((b) => (
                    <li key={b} className="flex gap-1.5">
                      <span aria-hidden="true" className="text-slate-500">
                        ›
                      </span>
                      <span>{b}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>

          <div className="mt-4 rounded-xl border border-emerald-400/25 bg-emerald-500/5 px-4 py-3">
            <div className="flex flex-wrap items-center gap-2">
              <span className="rounded-full bg-emerald-500/15 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-emerald-200 ring-1 ring-emerald-400/30">
                Closed branch T★
              </span>
              <span className="text-[11px] text-emerald-100/85">
                SM packet · α · flavor · θ_eff = 0 · cosmology interfaces
              </span>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

function TrunkStep({
  n,
  label,
  tex,
  accent,
  highlight,
}: {
  n: string;
  label: string;
  tex: string;
  accent: string;
  highlight?: boolean;
}) {
  return (
    <li
      className={`flex items-start gap-3 rounded-xl border p-3 ${
        highlight
          ? "border-blue-400/30 bg-blue-500/5"
          : "border-slate-700/40 bg-slate-950/40"
      }`}
    >
      <span
        className={`flex h-7 w-7 flex-none items-center justify-center rounded-full bg-gradient-to-br ${accent} font-mono text-xs font-semibold text-white shadow`}
      >
        {n}
      </span>
      <div className="min-w-0 flex-1">
        <div className="text-[11px] font-semibold uppercase tracking-widest text-slate-300">
          {label}
        </div>
        <div className="mt-1 overflow-x-auto formula-scroll">
          <Math block>{tex}</Math>
        </div>
      </div>
    </li>
  );
}

function Arrow() {
  return (
    <li
      aria-hidden="true"
      className="flex h-5 items-center justify-center pl-3.5 text-slate-500"
    >
      <span className="block h-3 w-px bg-gradient-to-b from-slate-600/40 via-slate-500/30 to-slate-600/40" />
    </li>
  );
}

/** Map plain decoder titles to their KaTeX form for crisp glyphs. */
function texOf(title: string): string {
  switch (title) {
    case "Y":
      return "Y";
    case "[u_Σ] = 1":
      return "[u_\\Sigma] = 1";
    case "u = φ₀":
      return "u = \\varphi_0";
    default:
      return title;
  }
}
