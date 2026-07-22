"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { Math } from "./Math";
import { FTransferDynamics } from "./FTransferDynamics";

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
    body: "Quark ratios are closed (Readout Rigidity, c_u/c_d = 55/117); only the absolute scale v_geo remains. The No-Unit theorem (v153) makes it an irreducible metrology primitive — the same unit as gravity's 1/G, over-determined to 0.11% by gravity vs dark energy (v274). A unit, not a gap.",
    formula: "\\det R = 8,\\ \\operatorname{Spec}(Q_+)=\\{1,2,3\\};\\ U_{\\mathrm{point}} \\to v_{\\mathrm{geo}}",
    tone: "border-amber-400/30 bg-amber-500/5",
  },
  {
    tag: "Interface 2",
    marker: "[E] target · [C] seam",
    title: "G_net — the metric-sector inclusion",
    body: "The (E₈)₁ target is closed [E] (v154/v175). The seam coupling SEAM.EQUIV.01 is closed modulo cited theorems: the lattice model (v367/v368) + the S3 stack pin it at every computable level (c = 8, the (E₈)₁ character, torus GSD = 1, RP; v376–v379, ground-state witnesses v489/v490), Lean-pinned (FORM.SEAM.MMST.01). Residual [O] = the cited MMST continuum-existence only (v336; extension leg on the peer-reviewed crossed-product package, realisation at invariant level, v469; stays [O]).",
    formula: "[\\,(E_8)_1 : (D_5)_1\\times(A_3)_1\\,] = 4 = |\\mu_4| \\Rightarrow \\text{holomorphic } c = 8",
    tone: "border-amber-400/30 bg-amber-500/5",
  },
  {
    tag: "Interface 3",
    marker: "[C]",
    title: "F_transfer — one typed runnable solver suite",
    body: "One typed, runnable solver suite — Koide (v371), η_B (v372), axion relic (v373), m_p/m_e (v374) — each with a kill test, folded into a prediction-observatory CI (v375). A guard (v187) keeps them [C] bridges, never compiler outputs.",
    tone: "border-slate-500/30 bg-slate-500/5",
  },
];

const RESIDUAL: { label: string; marker: string; blurb: string; tone: string }[] = [
  {
    label: "v_geo",
    marker: "[O]",
    blurb: "One dimensionful scale — irreducible by the No-Unit theorem and over-determined (gravity = dark energy = M̄_Pl to 0.11%, v274); the same primitive as gravity's 1/G.",
    tone: "from-amber-500/15 to-amber-500/[0.03] border-amber-400/30",
  },
  {
    label: "G_net",
    marker: "[E] target · [C] seam",
    blurb: "Metric inclusion: the (E₈)₁ target is closed and pinned at every computable level (lattice v367/v368 + S3 stack v376–v379, ground-state witnesses v489/v490); the seam coupling SEAM.EQUIV.01 now carries two named routes (route split 2026-07-22, no status change in substance): the MMST route SEAM.EQUIV.MMST.01 is closed modulo cited theorems (Lean FORM.SEAM.MMST.01), residual [O] = the cited MMST continuum existence only (v336; extension leg crossed-product certified, v469); the twistor route SEAM.EQUIV.TWISTOR.01 (Costello–Li construction, prepared by CELEST.SEAM.01) is [O]; the parent closes if either route closes and stays [O] as an unconditional claim.",
    tone: "from-amber-500/15 to-amber-500/[0.03] border-amber-400/30",
  },
  {
    label: "F_transfer",
    marker: "[C]",
    blurb: "One typed runnable solver suite (v371–v374) + a prediction-observatory CI (v375), each with a kill test — bridges, never primitive outputs.",
    tone: "from-slate-500/15 to-slate-500/[0.03] border-slate-500/30",
  },
];

/** The three provably-equivalent faces of the single structural condition (v234). */
const FACES: { face: string; statement: string }[] = [
  { face: "AQFT", statement: "boundary net holomorphic (μ-index 1)" },
  { face: "Geometry", statement: "seam link a homology 3-sphere (Γ perfect ⟺ 2I)" },
  { face: "Rep theory", statement: "exactly one 1-dim irrep (no abelian charge)" },
];

function ResidualTreemap() {
  return (
    <figure
      className="mt-8 rounded-2xl border border-slate-700/40 bg-slate-950/30 p-4 sm:p-5"
      aria-label="The complete open residual: v_geo, G_net and F_transfer"
    >
      <figcaption className="mb-3 text-center font-mono text-sm text-slate-300">
        Rest = <span className="text-amber-200">v_geo</span> ⊕{" "}
        <span className="text-amber-200">G_net</span> ⊕{" "}
        <span className="text-slate-200">F_transfer</span>
      </figcaption>
      <div className="grid gap-3 sm:grid-cols-3">
        {RESIDUAL.map((r) => (
          <div
            key={r.label}
            className={`flex flex-col gap-2 rounded-xl border bg-gradient-to-br p-4 ${r.tone}`}
          >
            <div className="flex items-center justify-between gap-2">
              <span className="font-mono text-base font-semibold text-slate-50">
                {r.label}
              </span>
              <span className="rounded-full bg-slate-900/60 px-2 py-0.5 font-mono text-[10px] font-semibold text-slate-300 ring-1 ring-slate-600/40">
                {r.marker}
              </span>
            </div>
            <p className="text-xs leading-relaxed text-slate-300">{r.blurb}</p>
          </div>
        ))}
      </div>
    </figure>
  );
}

/**
 * The single closing condition (v234/v235): the whole structural residual is one
 * condition with three provably-equivalent faces, all forcing E₈. This states the
 * current end-point only — the sprint-by-sprint reduction history lives on /changelog
 * and in the research contracts, not in this reader-facing block.
 */
function ClosingCondition() {
  return (
    <figure className="mt-8 rounded-2xl border border-emerald-400/25 bg-emerald-500/[0.04] p-5 sm:p-6">
      <figcaption className="text-sm font-semibold text-emerald-200">
        The structural residual is{" "}
        <span className="underline decoration-emerald-400/40 underline-offset-4">
          one condition
        </span>{" "}
        — the seam carries no nontrivial abelian sector
      </figcaption>
      <p className="mt-2 text-sm leading-relaxed text-slate-300">
        The metric inclusion (G_net), the carrier P2 and red-team Target A are not
        three gates but three faces of a single condition — and all three force E₈:
      </p>
      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        {FACES.map((f) => (
          <div
            key={f.face}
            className="rounded-xl border border-slate-700/40 bg-slate-950/40 p-3"
          >
            <div className="font-mono text-[11px] font-semibold uppercase tracking-wider text-emerald-300/80">
              {f.face}
            </div>
            <div className="mt-1 text-xs leading-relaxed text-slate-300">
              {f.statement}
            </div>
          </div>
        ))}
      </div>
      <div className="mt-4 overflow-x-auto rounded-lg border border-slate-700/40 bg-slate-950/50 p-2.5">
        <Math
          block
          plain="The seam has exactly one one-dimensional representation (a trivial abelianisation, a homology-sphere link) if and only if it is E₈ — equivalently, the K-matrix has determinant one."
        >
          {"\\#(\\text{1-dim irreps}) = |\\Gamma^{\\mathrm{ab}}| = |H_1(S^3/\\Gamma)| = 1 \\iff E_8 \\iff |\\det K| = 1"}
        </Math>
      </div>
      <p className="mt-4 text-sm leading-relaxed text-slate-300">
        <span className="font-semibold text-emerald-200">In short.</span> The whole boundary QFT collapses
        onto this one premise (the Modular Spectral Closure, v258–v261), so{" "}
        <span className="font-mono text-emerald-200">SEAM.EQUIV.01</span> is{" "}
        <span className="text-emerald-200">closed modulo cited theorems</span>: the explicit lattice model
        (v367/v368) and the S3 stack (v376–v379, ground-state witnesses v489/v490) pin the target at every computable level, Lean-pinned
        (FORM.SEAM.MMST.01) to the published MMST/Adamo theorems — the only residual{" "}
        <span className="text-amber-200">[O]</span> is their abstract continuum-existence (v336; its 128-spinor
        extension leg is certified at net level by the peer-reviewed crossed-product package v469, LR/Böckenhauer/KLM,
        with AGT/AMT an independent second witness; stays [O]). The ambient
        measure QG.AMB.01 is a <span className="text-amber-200">[C] redundancy</span> (v369/v379) — a
        certification object, not missing dynamics — and perturbative spin-2 graviton unitarity is
        established (the Stelle ghost is a truncation artefact, v304/v370/v380).
      </p>
      <details className="group mt-3 rounded-lg border border-slate-700/40 bg-slate-950/40">
        <summary className="cursor-pointer list-none px-3 py-2 text-xs font-semibold text-slate-200 transition-colors hover:text-slate-50 [&::-webkit-details-marker]:hidden">
          <span className="text-blue-300 group-open:hidden">＋ </span>
          <span className="hidden text-blue-300 group-open:inline">－ </span>
          The full argument (Modular Spectral Closure · the QG-decoupling theorem · the 4D-QFT fork)
        </summary>
        <div className="space-y-2 px-3 pb-3 text-xs leading-relaxed text-slate-400">
          <p>
            <span className="font-semibold text-slate-300">Modular Spectral Closure (v258–v261).</span> The
            finite Dirac is a covariance induction of the seam KMS state, the spectral-action cutoff <em>is</em>{" "}
            that KMS weight (f₂/f₀ = 1), and seam, carrier-16 and E₈ live on one Kummer/K3 surface — so Dirac,
            cutoff, gauging, glue and orientability are readouts of one seam state. QGEO.SYM.01 is then a
            corollary (a conformal net&apos;s vacuum is rotation-invariant by axiom, v335).
          </p>
          <p>
            <span className="font-semibold text-slate-300">Seam keystone.</span> The keystone&apos;s residual is
            a composition of standard cited theorems (OS/clustering, the Kitaev free-fermion classification,
            the AQFT stack) over established TFPT facts — Lean-pinned to those named steps plus the derived gap
            Δ = 6·ln(3/2) ≈ 2.43 &gt; 0, no undischarged TFPT-internal assumption. Its two heavy legs are
            literature-anchored (v336): the MMST continuum scaling limit and the Adamo–Moriwaki–Tanimoto OS
            reconstruction, with (E₈)₁ inside their range (c=8, rank 8, 16 Majoranas) — and the 128-spinor
            extension leg is now certified at net level by the peer-reviewed crossed-product package (v469,
            LR/Böckenhauer/KLM), with the AGT/AMT route demoted to an independent second witness; stays [O].
          </p>
          <p>
            <span className="font-semibold text-slate-300">QG decoupling is a theorem (v337).</span> Every
            readout factors through the gapped admissible spectrum (χ = 729/665, margin 1.648 &gt; 0), so TFPT
            provably does not need the ambient measure.
          </p>
          <p>
            <span className="font-semibold text-slate-300">4D-QFT fork (v265).</span> Boundary QFT — closed
            modulo cited theorems; ambient QG — discharged as redundancy [C]; 4D GUT — not claimed (E₈ is the
            audit hull, not a 4D gauge group); optional UV branch — carrier-native Pati–Salam, falsifiable by
            thresholds and proton decay. The sprint-by-sprint reduction (v234 → v302) is on the{" "}
            <Link href="/changelog" className="text-blue-300 underline-offset-2 hover:underline">
              changelog
            </Link>
            .
          </p>
        </div>
      </details>
    </figure>
  );
}

/**
 * Trust section: what is still open. The whole structural residual collapses to one
 * condition (no abelian sector ⟹ E₈), plus the one irreducible scale and the typed
 * transfer functor — surfaced near the top as a credibility signal, not a footnote.
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
          description="After the compiler closure the live residual is just three named items — Rest = v_geo ⊕ G_net ⊕ F_transfer. Sharper still: the structural part (the metric inclusion and the carrier P2) is one condition that forces E₈ three equivalent ways — and the entire boundary-QFT layer (Dirac, cutoff, gauging, glue) now collapses onto that same condition via the Modular Spectral Closure. Nothing is hidden, nothing is overclaimed."
        />

        <ClosingCondition />

        <ResidualTreemap />

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

        <FTransferDynamics />

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
