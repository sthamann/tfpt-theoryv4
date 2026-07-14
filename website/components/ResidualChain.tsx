"use client";

import { motion } from "motion/react";
import { ArrowDown, FileCode2, Play } from "lucide-react";
import { cn } from "@/lib/utils";
import { useReproducer } from "./Reproducer";

/**
 * ResidualChain — the structural-residual reduction chain as live HTML
 * (replaces the static residual_chain.png figure).
 *
 * The step data mirrors verification/make_figures.py::fig_residual_chain
 * (the source of the PDF figure in the research-contracts paper), extended by
 * the certification round (v458–v480). Each step links its key scripts to the
 * in-browser Pyodide reproducer.
 */

type StepTone = "gray" | "green" | "gold";

const TONE: Record<StepTone, { tag: string; ring: string }> = {
  gray: { tag: "text-slate-400", ring: "border-slate-600/40 bg-slate-800/20" },
  green: { tag: "text-emerald-300", ring: "border-emerald-400/25 bg-emerald-500/[0.05]" },
  gold: { tag: "text-amber-300", ring: "border-amber-400/40 bg-amber-500/[0.10]" },
};

interface Step {
  tag: string;
  head: string;
  sub: string;
  tone: StepTone;
  scripts?: string[];
}

const STEPS: Step[] = [
  {
    tag: "start",
    head: "Naive residual",
    sub: "\u201cbuild a quantum-gravity measure\u201d",
    tone: "gray",
  },
  {
    tag: "v175",
    head: "Net existence + full-cone RP",
    sub: "discharged to [E] (the CAR functor)",
    tone: "green",
    scripts: ["v175_net_existence_full_cone.py"],
  },
  {
    tag: "v176–v181",
    head: "One geometric premise",
    sub: "QGEO.SYM.01: the carrier μ₄ clock = the seam's conformal deck",
    tone: "green",
    scripts: ["v176_seam_collar_realisation.py", "v181_clock_is_conformal_symmetry.py"],
  },
  {
    tag: "v194–v201",
    head: "Non-circular form",
    sub: "state-invariance ω∘ρ = ω; the DtN map mark-local (ℤ₄)",
    tone: "green",
    scripts: ["v199_seam_state_invariance.py", "v201_seam_subprincipal_marks.py"],
  },
  {
    tag: "v234–v235",
    head: "ONE condition: holomorphy",
    sub: "no abelian sector ⇔ det K = 1 (the Kitaev E₈ tower)",
    tone: "green",
    scripts: ["v234_seam_holomorphy_selection.py", "v235_seam_chern_simons.py"],
  },
  {
    tag: "v276",
    head: "Flat all-orders closure (Lean)",
    sub: "flat τ=i ⇒ [ρ,H] = 0 to ALL orders (FORM.QGEO.03)",
    tone: "green",
    scripts: ["v276_qgeo_flat_closes_commutator.py"],
  },
  {
    tag: "v282",
    head: "Two faces, ONE object",
    sub: "χ_E8(i) = 12: the flat τ=i geometry = (E₈)₁ holomorphy",
    tone: "green",
    scripts: ["v282_e8_tau_i_unification.py"],
  },
  {
    tag: "v284–v285",
    head: "Two routes, one open lemma",
    sub: "RP-uniqueness 5/6 + condensation 3/4; the open lemmas coincide",
    tone: "green",
    scripts: ["v284_route_i_rp_uniqueness.py", "v285_route_ii_seam_condensation.py"],
  },
  {
    tag: "v286–v288",
    head: "SEAM.EQUIV.01 named + attacked",
    sub: "import firewall (v286); Route A 4/5 (v287); Route B proves the full-L² ℤ₄ lift (v288)",
    tone: "green",
    scripts: ["v286_seam_equivalence_contract.py", "v288_full_l2_subprincipal_z4.py"],
  },
  {
    tag: "v289–v297",
    head: "Flat-Away: 3 routes reduced",
    sub: "heat a₂ closed + Lean (v292/v295/v296), spectral Hessian PD (v293), Troyanov (v294); Route A citable stack (v297)",
    tone: "green",
    scripts: ["v295_flataway_a2_exact.py", "v297_route_a_literature_stack.py"],
  },
  {
    tag: "v300–v302",
    head: "Closing arc: shared fact pinned",
    sub: "Flat-Away hard-pinned from the (E₈)₁ Steklov data (v300); Route A invertible via free fermions (v301); the gap = derived 6 ln(3/2) > 0 (v302)",
    tone: "green",
    scripts: ["v300_flataway_rigid.py", "v301_route_a_invertible.py", "v302_seam_gap.py"],
  },
  {
    tag: "v335–v379",
    head: "Closed modulo cited theorems",
    sub: "QGEO.SYM.01 = a corollary of SEAM.EQUIV.01 (v335); the gapped lattice model (v367/v368) + the S3 stack (v376–v379), Lean-pinned MMST",
    tone: "green",
    scripts: ["v335_seam_equiv_unify.py", "v367_seam_s3_lattice.py", "v379_seam_s3_rp.py"],
  },
  {
    tag: "v458–v480",
    head: "Certification round",
    sub: "the 128-spinor extension leg certified by the peer-reviewed crossed-product package, realisation at invariant level (v469); the R3 graph→geometry bridge discharged to Kronheimer 1989 (v479); the four-interval μ₄ mechanism exhibited, ω∘ρ = ω manifest (v480)",
    tone: "green",
    scripts: [
      "v469_seam_crossedproduct_route.py",
      "v479_kronheimer_quiver_bridge.py",
      "v480_multilocal_four_interval.py",
    ],
  },
  {
    tag: "BEDROCK",
    head: "No TFPT-internal assumption left",
    sub: "the SEAM.EQUIV.01 residual = the cited continuum scaling-limit existence (v336) over established facts; stays [O] (not machine-proved end-to-end)",
    tone: "gold",
    scripts: ["v336_continuum_limit.py"],
  },
];

export function ResidualChain() {
  const { open } = useReproducer();

  return (
    <div className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40">
      <div className="border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          The structural-residual reduction chain — live
        </span>
        <p className="mt-1 break-words text-xs leading-relaxed text-slate-400">
          The whole &ldquo;quantum gravity&rdquo; question collapses, one machine-checked step
          at a time, to one falsifiable physical statement: is the raw seam (E₈)₁ at τ=i?
        </p>
      </div>

      <ol className="m-0 list-none space-y-0 p-5 sm:p-6">
        {STEPS.map((s, i) => {
          const tone = TONE[s.tone];
          return (
            <motion.li
              key={s.tag}
              initial={{ opacity: 0, y: 8 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 0.3, delay: Math.min(i, 6) * 0.02 }}
            >
              <div className={cn("rounded-xl border p-3.5 sm:p-4", tone.ring)}>
                <div className="flex flex-wrap items-baseline gap-x-2.5 gap-y-1">
                  <span className={cn("font-mono text-[11px] font-semibold", tone.tag)}>
                    {s.tag}
                  </span>
                  <span className="text-sm font-semibold text-slate-100">{s.head}</span>
                </div>
                <p className="mt-1 break-words text-xs leading-relaxed text-slate-400">
                  {s.sub}
                </p>
                {s.scripts && (
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {s.scripts.map((f) => (
                      <button
                        key={f}
                        type="button"
                        onClick={() => open(f)}
                        className="group inline-flex max-w-full items-center gap-1.5 rounded-md border border-slate-700/50 bg-slate-950/60 px-2 py-0.5 font-mono text-[10px] text-slate-300 transition-colors hover:border-blue-400/50 hover:bg-blue-500/10 hover:text-blue-100"
                      >
                        <FileCode2 size={11} className="flex-none group-hover:hidden" aria-hidden />
                        <Play size={11} className="hidden flex-none group-hover:inline" aria-hidden />
                        <span className="min-w-0 break-all text-left">{f}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
              {i < STEPS.length - 1 && (
                <div className="flex justify-center py-1" aria-hidden>
                  <ArrowDown size={14} className="text-slate-600" />
                </div>
              )}
            </motion.li>
          );
        })}
      </ol>

      <p className="border-t border-slate-800/60 px-5 py-4 text-xs italic leading-relaxed text-slate-500">
        Everything above the bedrock is a theorem, a Lean proof or an established citation; the
        bedrock, once a definition (QGEO.SYM.01), is now one falsifiable physical question — and
        the emergent-QFT layer (v258–v261, the Modular Spectral Closure) collapses onto this same
        bedrock, so the boundary QFT adds no new open item. The full step-by-step reduction lives
        on the <span className="not-italic text-slate-300">/changelog</span> page.
      </p>
    </div>
  );
}
