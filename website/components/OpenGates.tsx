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
    marker: "[C]/[O]",
    title: "G_net — the metric-sector inclusion",
    body: "R + R² is heat-kernel grounded (G2) and the admissible IR sector is gap-decoupled (G5, Δ_eff = 1.648 > 0). The closing statement is exactly ONE theorem: the seam–Calderón inclusion has Jones index 4 = |μ₄| (the μ₄ simple-current extension of the carrier net), from which holomorphy and the unique (E₈)₁ bulk follow (LR/KLM/BKLR). The free-bulk premise (A) behind it is itself no longer free-standing: it is a fixed-point theorem with the infinite Schwinger cone eliminated (cone gap = one-particle gap (2/3)⁶ by Bogoliubov second quantisation), factoring into the already-open A2 net-existence + GATE.QGEO with the irreducible core {π, v_geo} a theorem — zero new open content (v160–v165). The terminal inventory (v167) confirms this is the single structural hinge, and the FINITE half of GATE.QGEO is now proven exactly [E] (v168): μ₄ has cross-ratio 2 and a faithful Möbius D₄ stabiliser, H¹(ℙ¹∖μ₄) has rank N_fam = 3, and the eigenforms carry the μ₄ characters of weights (1,2,3) = the A₃ exponents = Spec(Q₊). The two structural residuals are then discharged to a theorem (v175): the CAR second-quantisation functor Γ(t)=⊕ₘΛᵐ(t) makes full-cone reflection positivity reduce for every m to the one-particle contraction (verified on the complete 2¹⁶=65536-dim Fock space), and A2 net existence is an assembled, verified (E₈)₁ certificate (character 1+248q+4124q²+…, embedding 248=120+128, E₈ Cartan even unimodular) — so net existence and full-cone RP become [E] and only the seam-collar realisation (QGEO.REALIZE.01, [O]) stays open. This is now formulated as ONE central statement — the Seam Collar Realisation Theorem (v176): given the RP one-sided seam collar with sheet-odd Calderón involution, faithful D₄ marks and admissible c=8 data, its boundary is ℙ¹∖μ₄ with H¹ grading (1,2,3), the Calderón contraction is the rank-8 K_Σ polarisation and the index-4 extension is (E₈)₁. The proof tree (v177) then sharpens this: four nodes are closed constructively — uniformisation (an order-4 Möbius map + the reflection z↦1/z give a faithful D4, so a genus-0 four-marked D4 boundary IS (ℙ¹,μ₄)), the H¹ character grading (1,2,3), the unique μ₄-equivariant module identification (residue-normalised), and the index-4 net (E₈)₁ — so the whole structural residual is exactly TWO named obligations, neither a finite computation: QGEO.MARKS.01 (the raw RP seam collar canonically produces the genus-0 four-marked D4 boundary) and QGEO.KERNEL.01 (the raw seam Calderón operator IS the μ₄-equivariant free gapped contraction, as an operator). An honest attempt (v178) pushes both as far as computation allows: each finite core is closed [E] — for MARKS the marks are forced to be a generic clock-orbit (μ₄, not the fixed points), distinct iff b₁=3=N_fam, with faithful D4; for KERNEL, on the multiplicity-free H¹ block a μ₄-equivariant operator is forced diagonal (Schur), so the spectrum IS the operator there — leaving each as a single milder premise. Investigating those (v179) shows the two are in fact ONE: genus-0 IS P1 (the χ=2 that gives the 8 in c₃=1/(8π)), the order-4 clock IS the carrier (Coxeter element of W(A₃)=S₄, h(A₃)=4), marks=one orbit is forced, and KERNEL then follows from that same geometry — so the entire structural residual of the theory is a single geometric premise QGEO.CONF.01: that the raw RP seam double is conformally (ℙ¹,μ₄) with the carrier clock as the order-4 Möbius map. And even that reduces one level further (v180): by uniformisation the genus-0 double IS ℙ¹ (the target is produced, not assumed), and an orientation-preserving isometry of a surface is holomorphic hence Möbius, with an order-4 Möbius map being z↦iz — so QGEO.CONF.01 is implied by the milder, non-circular premise QGEO.ISO.01: that the carrier clock is an order-4 orientation-preserving isometry of the RP seam metric (a metric-compatible holonomy). That milder premise is the single remaining structural residual; not closeable by arithmetic. Full QG closure is a certification layer, not a prerequisite for testing the readouts. (Historical label: G_metric.)",
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
