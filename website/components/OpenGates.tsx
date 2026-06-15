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
    body: "Three explicit levels make the status unambiguous. (1) G_net ALGEBRA [E]: (D₅)₁⊗(A₃)₁⋊⟨(1,1)⟩ ≅ (E₈)₁ — Jones index 4 = |μ₄|, holomorphic c = 8, the unique 2D bulk follows (v154). (2) G_net AQFT MACHINERY [E]: net existence and full-cone reflection positivity, via the CAR second-quantisation functor Γ(t)=⊕ₘΛᵐ(t) verified on the complete 2¹⁶-dim Fock space (v175); R + R² is heat-kernel grounded (G2) and the IR sector is gap-decoupled (G5, Δ_eff = 1.648 > 0). (3) G_net SEAM INSTANTIATION [O]: the one remaining premise QGEO.SYM.01 — the carrier μ₄ clock IS the seam's conformal deck. So the mathematics of the target object is closed; the only open item is the physical coupling of the raw seam to that object. That residual was driven to bedrock through the chain v175→v181 (assemble one central theorem → split into the MARKS + KERNEL obligations → close their finite cores → unify into one conformal-realisation premise QGEO.CONF.01 → milder isometry premise QGEO.ISO.01 → conformal-symmetry / deck premise QGEO.SYM.01), each step a theorem or an established citation (uniformisation, Kerékjártó, the order-4 Möbius classification). QGEO.SYM.01 is a definition, left honestly [O], not reducible further without relabeling. Framed honestly it is not a gap but TFPT's one fundamental postulate — the role 'c = const' plays in relativity — from which the rest unfolds by theorem; the achievement is that the whole theory is compressed onto exactly one sharply-located, falsifiable premise. Full QG closure is a certification layer, not a prerequisite for testing the readouts. The sharpest attack on this last premise is now an operator statement: QGEO.ENERGY.02, the energy commutator [ρ, Λ_Σ] = 0 on the rank-8 Calderón polarisation (v192/v193) — with ρ carrier-defined (Coxeter of W(A₃)=S₄), Λ_Σ the raw RP-seam DtN, and the commutator forcing the (1,2,3) grading on H¹. If the raw-seam DtN is RP-definable (the one non-circularity hinge), this turns QGEO.SYM.01 from a definition into an energy-rigidity theorem; an exact rider fixes the direction — the induced EH coefficient selects q(A₃)=¾ (family), not q(D₅)=⁵⁄₄ (carrier), so gravity is family-geometry-induced. That hinge was then tackled (v194): the DtN IS RP-canonical (Osterwalder–Schrader, v54) on a quasi-free seam state (v155), and [ρ, Λ_Σ]=0 closes on the finite cohomology H¹ [E] (distinct μ₄ characters, v177) — so the bedrock reduces one further notch, from a bare definition to ‘intrinsic Bisognano–Wichmann geometric modular covariance of the quasi-free seam state’: sharper and falsifiable, but still [O] (the full-L² modular geometricity must be intrinsic, else it re-presupposes the conformal covariance it should produce). The fog point keeps shrinking; it has not yet closed to [E]. The decisive crack (v198): the DtN principal symbol |k| = diag(|n|) and the clock ρ = diag(i^n) are both diagonal in the Fourier basis, so [ρ, |k|] = 0 EXACTLY on all of L² — the leading-order commutation is free on the whole boundary; and by Tomita–Takesaki [ρ, Λ_Σ]=0 FOLLOWS from the state being μ4-invariant (ω∘ρ=ω), needing only the state + reflection and NO conformal covariance — which removes the Bisognano–Wichmann circularity. So the entire residual is now the single, non-circular state-invariance ‘the raw quasi-free seam state is μ4-invariant’ (the Gaussian bulk measure is deck-invariant) — the maximally-operational form of QGEO.SYM.01. A foundational symmetry postulate cannot be derived from nothing (the role c = const plays in relativity); it is now in its sharpest, falsifiable, non-circular form — still [O], but the diffuse geometry is gone. One further reduction (v201): writing the DtN as Λ = |k| + M_f with M_f = multiplication by the boundary curvature f(θ), block-diagonality holds iff f is Z₄-invariant, and a curvature sourced by the four μ₄ marks f(θ)=Σⱼ g(θ−2πj/4) is automatically Z₄-invariant — so the μ₄-mark orbit (forced by v195) FORCES the sub-principal symbol block-diagonal (3 marks or generic marks break it). The whole residual thus collapses to the mark-locality of the DtN (the seam flat away from the μ₄ marks = the conformal-deck structure) — structurally definitional, the narrowest form yet of QGEO.SYM.01. (Historical label: G_metric.)",
    formula: "[\\,(E_8)_1 : (D_5)_1\\times(A_3)_1\\,] = 4 = |\\mu_4| \\ \\Rightarrow\\ \\text{holomorphic } c = 8",
    tone: "border-amber-400/30 bg-amber-500/5",
  },
  {
    tag: "Interface 3",
    marker: "[C]/[C]",
    title: "F_transfer — one typed functor, four interfaces",
    body: "Not a bag of open topics: F_transfer = F_observable ∘ F_threshold ∘ F_RG, standard physics fed TFPT source data, with exactly four interfaces. F_pole (Koide source→pole): the 53/54 factor is an exact operator readout [E], the pole interpretation [C] (v183). F_Boltzmann (CP source→η_B): the washout anchors (m̃₁ = m_3/A_Λ); the cleanest [C] route is the scalaron-decuple branch where BOTH Boltzmann inputs share A_Λ = 10 = |E(K₅)| and η_B brackets 6.1×10⁻¹⁰ with no hidden seesaw scale (v212), still a sharper scenario. F_relic (axion → Ω_a): all-of-DM is possible only on the θ_i ≈ 170° hilltop, and the spine-angle branch θ_i = 3π/5 = π·N_fam/g_car is the sharper falsifiable [C] alternative (v211). F_QCD (m_p/m_e via Λ_QCD, b₃ = −7, lattice): a QCD matching contract [O], not a compiler number (the rejected 1836 near-formula is the discipline working). A machine guard (v187) enforces that all four stay [C]/[O] and are never promoted to a primitive [E] compiler prediction — exact algebraic sub-parts (53/54, b₃ = −7) may be [E], the physical prediction never is. Beyond the guard, the functor contract CONTRACT.F.01 (v213) pins four structural axioms: (1) μ₄-deck equivariance — the Koide multiplier λ₂ = (2/3)⁶ = 64/729 IS the deck transfer eigenvalue; (2) Plücker preservation — 53 = aᵀ(R+Q)1, ‖Pl(K)‖₁ = 11; (3) positivity/stochasticity — spec(T) = {1,(2/3)⁶,(1/3)⁶} positive, κ_f ∈ (0,1); (4) external modules explicit. It is the third research contract alongside U_wall and G_metric — a typed functor, a consolidation, not a closure.",
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
