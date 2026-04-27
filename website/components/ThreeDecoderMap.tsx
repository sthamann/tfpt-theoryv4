"use client";

import { motion } from "motion/react";
import { Math } from "./Math";

interface DecoderEntry {
  id: string;
  title: string;
  tex: string;
  role: string;
  bullets: string[];
  accent: string;
  chip: string;
}

const DECODERS: DecoderEntry[] = [
  {
    id: "Y",
    title: "Y",
    tex: "Y",
    role: "Structure",
    bullets: [
      "3 + 2 carrier split",
      "Hypercharge generator",
      "SM packet, gauge quotient",
    ],
    accent: "from-blue-500 to-violet-500",
    chip: "bg-blue-500/15 text-blue-200 ring-blue-400/30",
  },
  {
    id: "uSigma",
    title: "[u_Σ] = 1",
    tex: "[u_\\Sigma] = 1",
    role: "Counting",
    bullets: ["N_fam = 3", "Ω_adm = 48", "N_Φ = 1, b₁ = 41/10"],
    accent: "from-violet-500 to-fuchsia-500",
    chip: "bg-violet-500/15 text-violet-200 ring-violet-400/30",
  },
  {
    id: "phi0",
    title: "u = φ₀",
    tex: "u = \\varphi_0",
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
      aria-label="The three-decoder map: structure, counting, and bridge observables."
    >
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          One datum · One joint solve · Three decoders
        </span>
        <span className="rounded-full bg-slate-800/60 px-2.5 py-0.5 text-[10px] font-mono uppercase tracking-widest text-slate-300 ring-1 ring-slate-700/40">
          15-second overview
        </span>
      </div>

      <div className="px-5 py-7 sm:px-8 sm:py-9">
        <ol className="mx-auto flex max-w-3xl flex-col items-stretch gap-3">
          <TrunkStep
            n="1"
            label="One-sided boundary datum"
            tex="\mathfrak{T}_\partial"
            accent="from-slate-400 to-slate-500"
          />
          <TrunkConnector />
          <TrunkStep
            n="2"
            label="Primitive kernel"
            tex="(\tau_{\mathrm{dbl}},\iota_C,P_{\mathrm{prim}},[u_\Sigma],c_3)"
            accent="from-blue-500 to-violet-500"
          />
          <TrunkConnector />
          <TrunkStep
            n="3"
            label="Joint discrete admissibility solve"
            sublabel="Single discrete solution; structure, counting, bridge seed are joint outputs"
            tex="d^\star_{\mathrm{disc}}"
            accent="from-blue-500 to-violet-500"
            highlight
          />
        </ol>

        <ThreeWayFork />

        <div className="grid gap-3 sm:grid-cols-3" role="list">
          {DECODERS.map((d, i) => (
            <motion.div
              key={d.id}
              role="listitem"
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
                <Math>{d.tex}</Math>
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

        <ConvergenceFork />

        <div className="mx-auto max-w-3xl">
          <ClosedBranchPill />
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
  sublabel,
  highlight,
}: {
  n: string;
  label: string;
  tex: string;
  accent: string;
  sublabel?: string;
  highlight?: boolean;
}) {
  return (
    <li
      className={`flex items-start gap-3 rounded-xl border p-3 ${
        highlight
          ? "border-blue-400/40 bg-blue-500/10 ring-1 ring-blue-400/30"
          : "border-slate-700/40 bg-slate-950/40"
      }`}
    >
      <span
        className={`flex h-7 w-7 flex-none items-center justify-center rounded-full bg-gradient-to-br ${accent} font-mono text-xs font-semibold text-white shadow`}
      >
        {n}
      </span>
      <div className="min-w-0 flex-1">
        <div className="text-[11px] font-semibold uppercase tracking-widest text-slate-200">
          {label}
        </div>
        <div className="mt-1 overflow-x-auto formula-scroll">
          <Math block>{tex}</Math>
        </div>
        {sublabel && (
          <p className="mt-1 text-[11px] leading-snug text-slate-400">
            {sublabel}
          </p>
        )}
      </div>
    </li>
  );
}

function TrunkConnector() {
  return (
    <li
      aria-hidden="true"
      className="flex h-5 items-center justify-center pl-3.5 text-slate-500"
    >
      <span className="block h-3 w-px bg-gradient-to-b from-slate-600/40 via-slate-500/30 to-slate-600/40" />
    </li>
  );
}

/**
 * Visual three-way fork from the joint discrete solve to the three decoders.
 * Drawn as an SVG with a center stem and three branches so the geometry
 * stays the same on any width and prints cleanly to PDF.
 */
function ThreeWayFork() {
  return (
    <div
      className="relative mx-auto my-3 hidden h-12 max-w-3xl sm:block"
      aria-hidden="true"
    >
      <svg
        viewBox="0 0 600 48"
        preserveAspectRatio="none"
        className="h-full w-full"
      >
        <defs>
          <linearGradient id="forkStroke" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#a78bfa" stopOpacity="0.55" />
            <stop offset="1" stopColor="#34d399" stopOpacity="0.55" />
          </linearGradient>
        </defs>
        {/* Trunk */}
        <line x1="300" y1="0" x2="300" y2="20" stroke="url(#forkStroke)" strokeWidth="1.5" />
        {/* Horizontal split line */}
        <line x1="100" y1="20" x2="500" y2="20" stroke="url(#forkStroke)" strokeWidth="1.5" />
        {/* Three branches down */}
        <line x1="100" y1="20" x2="100" y2="44" stroke="url(#forkStroke)" strokeWidth="1.5" />
        <line x1="300" y1="20" x2="300" y2="44" stroke="url(#forkStroke)" strokeWidth="1.5" />
        <line x1="500" y1="20" x2="500" y2="44" stroke="url(#forkStroke)" strokeWidth="1.5" />
      </svg>
      <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full bg-slate-900/85 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-violet-200 ring-1 ring-violet-400/30">
        Three parallel decoders
      </span>
    </div>
  );
}

/**
 * Mobile fallback for the fork — a single vertical connector with a label,
 * since a three-way SVG fan would be unreadable on a narrow screen.
 */
// (Mobile already gets a stacked layout via grid-cols-1 default; the SVG
// fork is hidden below sm:.)

function ConvergenceFork() {
  return (
    <div
      className="relative mx-auto my-3 hidden h-12 max-w-3xl sm:block"
      aria-hidden="true"
    >
      <svg
        viewBox="0 0 600 48"
        preserveAspectRatio="none"
        className="h-full w-full"
      >
        <defs>
          <linearGradient id="mergeStroke" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#34d399" stopOpacity="0.55" />
            <stop offset="1" stopColor="#a78bfa" stopOpacity="0.55" />
          </linearGradient>
        </defs>
        {/* Three top stems */}
        <line x1="100" y1="0" x2="100" y2="24" stroke="url(#mergeStroke)" strokeWidth="1.5" />
        <line x1="300" y1="0" x2="300" y2="24" stroke="url(#mergeStroke)" strokeWidth="1.5" />
        <line x1="500" y1="0" x2="500" y2="24" stroke="url(#mergeStroke)" strokeWidth="1.5" />
        {/* Horizontal merge line */}
        <line x1="100" y1="24" x2="500" y2="24" stroke="url(#mergeStroke)" strokeWidth="1.5" />
        {/* Trunk into closed branch */}
        <line x1="300" y1="24" x2="300" y2="48" stroke="url(#mergeStroke)" strokeWidth="1.5" />
      </svg>
    </div>
  );
}

function ClosedBranchPill() {
  return (
    <div className="rounded-xl border border-emerald-400/30 bg-emerald-500/10 px-4 py-3">
      <div className="flex flex-wrap items-center gap-2">
        <span className="rounded-full bg-emerald-500/20 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-emerald-200 ring-1 ring-emerald-400/30">
          Closed branch <span className="math-label">T★</span>
        </span>
        <span className="text-[11px] text-emerald-50/90">
          SM packet · α · flavor · θ_eff = 0 · cosmology interfaces
        </span>
      </div>
    </div>
  );
}
