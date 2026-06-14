"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { Math } from "./Math";

interface Gate {
  tag: string;
  marker: string;
  title: string;
  body: string;
  formula?: string;
  tone: string;
}

const GATES: Gate[] = [
  {
    tag: "Interface 1",
    marker: "[O]",
    title: "v_geo — the one scale anchor",
    body: "The quark mass ratios are closed (Readout Rigidity, c_u/c_d = 55/117 on the discrete selector stratum) and the selector triangle pins R columnwise (the dual pair (d,n), v136/v139). Only the absolute amplitude scale v_geo remains — the same dimensionful anchor as gravity's 1/G; finite, algebraic and falsifiable. (Historical label: U_wall.)",
    formula: "\\det R = 8, \\ \\operatorname{Spec}(Q_+)=\\{1,2,3\\} \\ \\text{fixed};\\ U_{\\mathrm{point}} \\to v_{\\mathrm{geo}}",
    tone: "border-amber-400/30 bg-amber-500/5",
  },
  {
    tag: "Interface 2",
    marker: "[E] target · [O] seam",
    title: "G_net — the metric-sector inclusion",
    body: "Three explicit levels make the status unambiguous. (1) G_net ALGEBRA [E]: (D₅)₁⊗(A₃)₁⋊⟨(1,1)⟩ ≅ (E₈)₁ — Jones index 4 = |μ₄|, holomorphic c = 8, the unique 2D bulk follows (v154). (2) G_net AQFT MACHINERY [E]: net existence and full-cone reflection positivity, via the CAR second-quantisation functor Γ(t)=⊕ₘΛᵐ(t) verified on the complete 2¹⁶-dim Fock space (v175); R + R² is heat-kernel grounded (G2) and the IR sector is gap-decoupled (G5, Δ_eff = 1.648 > 0). (3) G_net SEAM INSTANTIATION [O]: the one remaining premise QGEO.SYM.01 — the carrier μ₄ clock IS the seam's conformal deck. So the mathematics of the target object is closed; the only open item is the physical coupling of the raw seam to that object. That residual was driven to bedrock through the chain v175→v181 (assemble one central theorem → split into the MARKS + KERNEL obligations → close their finite cores → unify into one conformal-realisation premise QGEO.CONF.01 → milder isometry premise QGEO.ISO.01 → conformal-symmetry / deck premise QGEO.SYM.01), each step a theorem or an established citation (uniformisation, Kerékjártó, the order-4 Möbius classification). QGEO.SYM.01 is a definition, left honestly [O], not reducible further without relabeling. Full QG closure is a certification layer, not a prerequisite for testing the readouts. (Historical label: G_metric.)",
    formula: "[\\,(E_8)_1 : (D_5)_1\\times(A_3)_1\\,] = 4 = |\\mu_4| \\ \\Rightarrow\\ \\text{holomorphic } c = 8",
    tone: "border-amber-400/30 bg-amber-500/5",
  },
  {
    tag: "Interface 3",
    marker: "[C]/[C]",
    title: "F_transfer — source→pole / relic / cosmology",
    body: "Koide, η_B, the axion relic scale and m_p/m_e are four instances of one missing functor F_transfer — the continuous transport from compiler source data to measured observables (Koide source→pole; η_B source→Boltzmann relic; axion scale→abundance; m_p/m_e→QCD/EW matching). Each has a genuine handle but is a transfer target, deliberately not claimed as a primitive compiler output.",
    tone: "border-slate-500/30 bg-slate-500/5",
  },
];

/**
 * Trust section: what is still open. The research contracts name exactly two
 * genuine gates plus a set of typed frontier interfaces — surfacing this near
 * the top is a credibility signal, not a footnote.
 */
export function OpenGates() {
  return (
    <section
      id="open-gates"
      className="relative scroll-mt-20 py-20 sm:py-24"
      aria-labelledby="open-gates-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="Honest boundaries"
          title="What is still open?"
          description="After the compiler closure the live residual is Rest = v_geo ⊕ G_net ⊕ F_transfer: one dimensionful scale anchor, one metric-sector inclusion theorem, and one downstream transfer functor. None of these is hidden, and none is overclaimed. (The historical labels U_wall / G_metric / F_frontier are kept only for ledger continuity.)"
        />

        <div className="mt-10 grid gap-5 lg:grid-cols-3">
          {GATES.map((g, i) => (
            <motion.article
              key={g.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.05 }}
              transition={{ duration: 0.55, delay: i * 0.08 }}
              className={`flex flex-col rounded-2xl border p-6 ${g.tone}`}
            >
              <div className="flex items-center gap-2">
                <span className="rounded-full border border-slate-600/40 bg-slate-900/50 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-slate-300">
                  {g.tag}
                </span>
                <span className="rounded-full bg-rose-500/15 px-2 py-0.5 font-mono text-[10px] font-semibold text-rose-200 ring-1 ring-rose-400/30">
                  {g.marker}
                </span>
              </div>
              <h3 className="mt-3 font-serif text-base font-semibold text-slate-50">
                {g.title}
              </h3>
              <p className="mt-2 flex-1 text-sm leading-relaxed text-slate-300">
                {g.body}
              </p>
              {g.formula && (
                <div className="mt-3 overflow-x-auto rounded-lg border border-slate-700/40 bg-slate-950/40 p-2.5">
                  <Math block>{g.formula}</Math>
                </div>
              )}
            </motion.article>
          ))}
        </div>

        <div className="mt-6 flex flex-wrap items-center gap-3 text-sm text-slate-400">
          <span>The gates are written up as numbered research contracts.</span>
          <Link
            href="/papers/research-contracts"
            className="inline-flex items-center gap-1.5 font-semibold text-blue-300 transition-colors hover:text-blue-200"
          >
            Read the contracts
            <ArrowRight size={14} aria-hidden />
          </Link>
        </div>
      </div>
    </section>
  );
}
