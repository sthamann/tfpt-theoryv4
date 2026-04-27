"use client";

import { motion } from "motion/react";
import { Compass, Layers, Target, Shield } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { Math } from "./Math";
import { StatusPyramid } from "./StatusPyramid";
import { GlossTerm } from "./GlossTerm";

const PILLARS = [
  {
    icon: Compass,
    title: "One-sided boundary datum",
    body: "Everything reconstructs from a single one-sided boundary datum 𝓣_∂ = (𝒜₊, ℋ₊, D₊, J, Γ, B_Σ). No carrier, no SM group, no α is inserted by hand.",
    accent: "from-blue-500 to-cyan-500",
  },
  {
    icon: Layers,
    title: "Three decoders",
    body: "Y generates structure (the SM packet). [u_Σ] = 1 generates counting (3 families, 1 Higgs). u = φ₀ generates bridge observables (α, λ_C, sin²θ₁₃).",
    accent: "from-violet-500 to-purple-500",
  },
  {
    icon: Target,
    title: "Falsifiable predictions",
    body: "Each readout has a stated dependency class and a kill criterion. θ_eff = 0 is theorem-level. α⁻¹(0) is a closed-branch root. The axion window scans 15.764 GHz ± 50 MHz.",
    accent: "from-emerald-500 to-teal-500",
  },
  {
    icon: Shield,
    title: "Status discipline",
    body: "Theorem-core, bridge, conditional closure, downstream — every paper opens with what it proves, what it doesn't, and exactly how it can fail.",
    accent: "from-orange-500 to-amber-500",
  },
];

export function Overview() {
  return (
    <section
      id="overview"
      className="relative scroll-mt-20 py-24 sm:py-32"
      aria-labelledby="overview-heading"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="What TFPT claims"
          title="A boundary-polarized spectral framework"
          description="TFPT is not a list of unrelated numerological readouts. It is a staged reconstruction in which the Standard Model, the fine-structure constant, the flavor sector, the strong-CP null, and the cosmology interface are forced by the same primitive boundary datum."
        />

        <div className="mt-14 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
          {PILLARS.map((p, i) => {
            const Icon = p.icon;
            return (
              <motion.div
                key={p.title}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.05 }}
                transition={{ duration: 0.6, delay: i * 0.08 }}
                className="group relative overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/40 p-6 transition-all hover:bg-slate-900/50 hover:ring-1 hover:ring-slate-500/40"
              >
                <div
                  className={`absolute inset-x-0 top-0 h-px bg-gradient-to-r ${p.accent} opacity-60`}
                />
                <div
                  className={`mb-4 inline-flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br ${p.accent} shadow-lg`}
                >
                  <Icon size={20} className="text-white" />
                </div>
                <h3 className="font-serif text-lg font-semibold text-slate-50">
                  {p.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-300">{p.body}</p>
              </motion.div>
            );
          })}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="mt-14 grid gap-6 lg:grid-cols-2"
        >
          <div className="glass rounded-2xl ring-1 ring-blue-400/20">
            <div className="border-b border-slate-800/60 px-5 py-3">
              <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
                Carrier theorem — polynomial as corollary
              </span>
            </div>
            <div className="p-6">
              <p className="text-sm leading-relaxed text-slate-300">
                The carrier polynomial is{" "}
                <span className="font-semibold text-slate-100">not</span> assumed.
                Boundary polarization gives a finite involution, the compact
                Higgs index fixes one rank, and primitive Yukawa type fixes the
                other:
              </p>
              <div className="mt-3 grid gap-2 text-xs">
                <div className="rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
                  <span className="font-mono text-blue-300">1.</span>{" "}
                  <Math>{"\\varepsilon_{\\mathrm{car}} = \\iota_C|_E"}</Math>
                  <span className="text-slate-400">
                    {" "}
                    → <Math>{"E = E_- \\oplus E_+"}</Math>
                  </span>
                </div>
                <div className="rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
                  <span className="font-mono text-blue-300">2.</span> Compact
                  Higgs index{" "}
                  <Math>{"H^0(S^2,\\mathcal{O}(1)) \\simeq \\mathbb{C}^2"}</Math>
                  <span className="text-slate-400">
                    {" "}
                    → <Math>{"\\dim E_+ = 2"}</Math>
                  </span>
                </div>
                <div className="rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
                  <span className="font-mono text-blue-300">3.</span> Primitive
                  Yukawa type{" "}
                  <Math>{"\\Lambda^3 E_- = \\det E_-"}</Math>
                  <span className="text-slate-400">
                    {" "}
                    → <Math>{"\\dim E_- = 3"}</Math>
                  </span>
                </div>
              </div>
              <div className="mt-3 overflow-x-auto rounded-lg border border-blue-400/30 bg-blue-500/5 p-3">
                <Math block>
                  {"Y = -\\tfrac{1}{3} P_- + \\tfrac{1}{2} P_+ \\;\\Rightarrow\\; 6Y^2 - Y - \\mathbf{1} = 0"}
                </Math>
              </div>
              <p className="mt-2 text-xs text-slate-400">
                The polynomial is the minimal polynomial of the derived
                eigenvalues — its algebraic shadow.
              </p>
            </div>
          </div>

          <div className="glass rounded-2xl ring-1 ring-emerald-400/20">
            <div className="border-b border-slate-800/60 px-5 py-3">
              <span className="text-[11px] font-semibold uppercase tracking-widest text-emerald-300/80">
                Closure equation for α
              </span>
            </div>
            <div className="p-6">
              <p className="text-sm leading-relaxed text-slate-300">
                With the seam opening{" "}
                <Math>{"\\varphi_{\\mathrm{seam}}(\\alpha)"}</Math>, the
                fine-structure constant is the unique positive root of the
                self-consistent equation:
              </p>
              <div className="mt-3 overflow-x-auto rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
                <Math block>
                  {"F_{U(1)}(\\alpha_\\star) = 0"}
                </Math>
              </div>
              <div className="mt-2 overflow-x-auto rounded-lg border border-emerald-400/30 bg-emerald-500/5 p-3">
                <Math block>
                  {"\\Rightarrow \\alpha_\\star^{-1} = 137.035\\,999\\,216\\,8\\ldots"}
                </Math>
              </div>
              <p className="mt-3 text-xs text-slate-400">
                CODATA 2022 recommends{" "}
                <span className="font-mono text-slate-200">
                  137.035 999 177(21)
                </span>
                ; the residual{" "}
                <span className="font-mono text-slate-200">
                  α⁻¹(TFPT − CODATA) ≈ 3.98 × 10⁻⁸
                </span>{" "}
                is the difference between the closed-branch root and the
                recommended adjustment.
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="mt-14"
        >
          <StatusPyramid />
        </motion.div>
      </div>
    </section>
  );
}
