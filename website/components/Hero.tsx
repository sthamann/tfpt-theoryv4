"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowRight, BookOpen, Download, Sigma } from "lucide-react";
import { Math } from "./Math";

export function Hero() {
  return (
    <section className="relative isolate overflow-hidden pt-12 pb-24 sm:pb-32">
      <div
        aria-hidden="true"
        className="absolute inset-0 grid-bg pointer-events-none"
      />
      <div
        aria-hidden="true"
        className="absolute -top-40 left-1/2 -z-10 h-[600px] w-[1100px] -translate-x-1/2 rounded-full opacity-40 blur-3xl"
        style={{
          background:
            "radial-gradient(closest-side, rgba(99,102,241,0.45), rgba(168,85,247,0.25), transparent)",
        }}
      />

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className="flex flex-col items-center text-center"
        >
          <span className="inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-500/10 px-4 py-1.5 text-xs font-medium tracking-wider text-blue-200">
            <Sigma size={14} className="opacity-80" />
            <span className="uppercase">TFPT 4.5 paper series · 2026</span>
          </span>

          <h1 className="mt-6 max-w-4xl font-serif text-4xl font-semibold leading-[1.05] text-slate-50 sm:text-5xl md:text-6xl lg:text-7xl">
            One <span className="text-gradient-blue">boundary datum</span>.{" "}
            <br className="hidden sm:block" />
            The whole Standard Model.
          </h1>

          <p className="mt-6 max-w-2xl text-base leading-relaxed text-slate-300 sm:text-lg md:text-xl">
            <span className="font-semibold text-slate-100">
              Topological Fixed-Point Theory
            </span>{" "}
            reconstructs the Standard-Model packet, the fine-structure constant,
            the Cabibbo angle, the PMNS matrix, strong-CP closure, and downstream
            cosmology — from a single one-sided boundary datum, with{" "}
            <span className="font-semibold text-blue-300">no fitted constants</span>.
          </p>

          <div className="mt-10 flex flex-col items-center gap-3 sm:flex-row">
            <Link
              href="/orientation"
              className="group inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-500/30 ring-1 ring-blue-400/40 transition-transform hover:scale-105 focus:scale-105"
            >
              <BookOpen size={16} />
              Read the orientation
              <ArrowRight
                size={16}
                className="transition-transform group-hover:translate-x-0.5"
              />
            </Link>
            <Link
              href="/predictions/tfpt_two_page_summary.pdf"
              target="_blank"
              rel="noopener"
              className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-6 py-3 text-sm font-semibold text-slate-100 backdrop-blur transition-colors hover:bg-slate-800/80"
            >
              <Download size={16} />
              Two-page summary
            </Link>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 32 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.9, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
          className="mx-auto mt-20 grid max-w-5xl gap-4 sm:mt-24 sm:grid-cols-2 lg:grid-cols-4"
        >
          {STATS.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 + i * 0.08 }}
              className="glass relative flex flex-col gap-1 rounded-2xl px-5 py-5 ring-1 ring-slate-700/40"
            >
              <div className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
                {s.label}
              </div>
              <div className="font-serif text-2xl font-semibold text-slate-50 sm:text-3xl">
                {s.value}
              </div>
              <div className="text-xs leading-relaxed text-slate-400">
                {s.note}
              </div>
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="relative mx-auto mt-16 max-w-4xl"
        >
          <div className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40">
            <div className="flex items-center gap-2 border-b border-slate-800/60 px-5 py-3">
              <div className="flex gap-1.5">
                <span className="h-2.5 w-2.5 rounded-full bg-rose-400/60" />
                <span className="h-2.5 w-2.5 rounded-full bg-amber-400/60" />
                <span className="h-2.5 w-2.5 rounded-full bg-emerald-400/60" />
              </div>
              <span className="ml-2 text-xs font-mono uppercase tracking-widest text-slate-400">
                The staged reconstruction
              </span>
            </div>
            <div className="px-6 py-8 sm:px-10 sm:py-12">
              <div className="overflow-x-auto">
                <Math block>
                  {String.raw`\mathfrak{S}_{\min}\Rightarrow\mathcal{B}_{\min}\Rightarrow\mathfrak{T}_\partial \Rightarrow (\tau_{\mathrm{dbl}},\iota_C,P_{\mathrm{prim}},[u_\Sigma],c_3) \Rightarrow d^\star_{\mathrm{disc}}\Rightarrow P_{\mathrm{adm}}\Rightarrow \mathfrak{T}_\star`}
                </Math>
              </div>
              <p className="mt-4 text-center text-xs text-slate-400">
                From the minimal seed{" "}
                <Math>{`\\mathfrak{S}_{\\min}`}</Math> to the closed branch{" "}
                <Math>{`\\mathfrak{T}_\\star`}</Math> — the same chain that fixes
                the Standard-Model packet, the gauge group, α, CKM, and PMNS.
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

const STATS = [
  {
    label: "α⁻¹(0)",
    value: "137.0359992",
    note: "Closed-branch root vs CODATA 137.035 999 084(21)",
  },
  {
    label: "Families",
    value: "3",
    note: "From admissible occupancy on the rigid carrier",
  },
  {
    label: "θ_eff",
    value: "0",
    note: "Strong-CP null — theorem-level on the admissible branch",
  },
  {
    label: "Higgs doublets",
    value: "1",
    note: "Compact bosonic index: N_Φ = 1, no extra light doublet",
  },
];
