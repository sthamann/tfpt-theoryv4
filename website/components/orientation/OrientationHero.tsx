"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowLeft, Download, FileText, Sigma } from "lucide-react";
import { Math } from "@/components/Math";

export function OrientationHero() {
  return (
    <section className="relative isolate overflow-hidden pt-12 pb-16 sm:pt-16 sm:pb-20">
      <div aria-hidden className="absolute inset-0 grid-bg pointer-events-none" />
      <div
        aria-hidden
        className="absolute -top-40 left-1/2 -z-10 h-[500px] w-[1000px] -translate-x-1/2 rounded-full opacity-30 blur-3xl"
        style={{
          background:
            "radial-gradient(closest-side, rgba(99,102,241,0.45), rgba(168,85,247,0.25), transparent)",
        }}
      />

      <div className="relative mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <motion.nav
          aria-label="Breadcrumb"
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="mb-8"
        >
          <Link
            href="/"
            className="inline-flex items-center gap-1.5 text-sm text-slate-400 transition-colors hover:text-slate-200"
          >
            <ArrowLeft size={14} />
            Back to overview
          </Link>
        </motion.nav>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
        >
          <span className="inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-500/10 px-4 py-1.5 text-xs font-medium tracking-wider text-blue-200">
            <Sigma size={14} className="opacity-80" />
            <span className="uppercase">Paper 0 · Orientation note</span>
          </span>

          <h1 className="mt-6 font-serif text-4xl font-semibold leading-[1.05] text-slate-50 sm:text-5xl md:text-6xl">
            TFPT in <span className="text-gradient-blue">one map</span>.
          </h1>

          <p className="mt-2 font-serif text-xl text-slate-400 sm:text-2xl">
            Boundary polarization, carrier rigidity, and observable closure.
          </p>

          <p className="mt-6 max-w-3xl text-base leading-relaxed text-slate-300 sm:text-lg">
            The thin entry document for the TFPT 4.5 series. It does not attempt to
            prove the full theory. Its purpose is to state{" "}
            <span className="font-semibold text-slate-100">what TFPT claims</span>,{" "}
            <span className="font-semibold text-slate-100">what it does not claim</span>,
            how the closed branch is organized, and where each load-bearing argument
            is isolated in the paper sequence.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Link
              href="/papers/00_orientation_note.pdf"
              target="_blank"
              rel="noopener"
              className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/30 ring-1 ring-blue-400/40 transition-transform hover:scale-105 focus:scale-105"
            >
              <Download size={16} />
              Download Paper 0 (PDF)
            </Link>
            <Link
              href="/papers/00_orientation_note.pdf"
              target="_blank"
              rel="noopener"
              className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-5 py-2.5 text-sm font-semibold text-slate-100 backdrop-blur transition-colors hover:bg-slate-800/80"
            >
              <FileText size={16} />
              View in browser
            </Link>
            <span className="ml-1 inline-flex items-center gap-2 text-xs text-slate-500">
              by Stefan Hamann &amp; Alessandro Rizzo
            </span>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.9, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
          className="mt-12"
        >
          <div className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40">
            <div className="flex items-center gap-2 border-b border-slate-800/60 px-5 py-3">
              <div className="flex gap-1.5">
                <span className="h-2.5 w-2.5 rounded-full bg-rose-400/60" />
                <span className="h-2.5 w-2.5 rounded-full bg-amber-400/60" />
                <span className="h-2.5 w-2.5 rounded-full bg-emerald-400/60" />
              </div>
              <span className="ml-2 text-xs font-mono uppercase tracking-widest text-slate-400">
                The staged reconstruction (one-line claim)
              </span>
            </div>
            <div className="px-6 py-7 sm:px-10 sm:py-9">
              <div className="overflow-x-auto">
                <Math block>
                  {String.raw`\mathfrak{S}_{\min}\Rightarrow\mathcal{B}_{\min}\Rightarrow\mathfrak{T}_\partial \Rightarrow (\tau_{\mathrm{dbl}},\iota_C,P_{\mathrm{prim}},[u_\Sigma],c_3) \Rightarrow d^\star_{\mathrm{disc}}\Rightarrow P_{\mathrm{adm}}\Rightarrow \mathcal{M}_{d^\star_{\mathrm{disc}}} \Rightarrow \mathcal{Z}_{\mathrm{cl}} \Rightarrow \mathfrak{T}_\star`}
                </Math>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
