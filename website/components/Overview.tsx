"use client";

import { ReactNode } from "react";
import { motion } from "motion/react";
import { Compass, Layers, Target, Shield } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { Math } from "./Math";
import { GlossTerm } from "./GlossTerm";
import { StatusPyramid } from "./StatusPyramid";
import { TheoryUnpacking } from "./TheoryUnpacking";
import { ThreeDecoderMap } from "./ThreeDecoderMap";

interface Pillar {
  icon: typeof Compass;
  title: string;
  body: ReactNode;
  accent: string;
}

const PILLARS: Pillar[] = [
  {
    icon: Compass,
    title: "Two axioms",
    body: (
      <>
        Everything starts from the{" "}
        <GlossTerm term="seam constant">seam constant</GlossTerm> c₃ = 1/(8π) (P1)
        and the five-slot{" "}
        <GlossTerm term="carrier">carrier</GlossTerm> g_car = 5 (P2). No SM gauge
        group, no families, no α is inserted by hand — they are consequences.
      </>
    ),
    accent: "from-blue-500 to-cyan-500",
  },
  {
    icon: Layers,
    title: "The E₈ compiler",
    body: (
      <>
        The carrier gives the D₅ half-spinor, the family geometry ℙ¹∖μ₄ gives A₃,
        and the <GlossTerm term="μ₄ glue">μ₄ glue</GlossTerm> closes E₈ = (D₅ ⊕ A₃)
        + μ₄ as a lattice theorem. E₈ is the{" "}
        <GlossTerm term="E8 compiler">audit hull</GlossTerm>; the SM is a{" "}
        <GlossTerm term="readout">readout</GlossTerm> after projection.
      </>
    ),
    accent: "from-slate-500 to-slate-400",
  },
  {
    icon: Target,
    title: "The bootstrap loop",
    body: (
      <>
        The E₈ closure feeds back and fixes the inputs: g_car = 5 is forced three
        ways and the 8 in c₃ equals rank E₈ = h(D₅) = φ(30). The discrete core is{" "}
        <GlossTerm term="bootstrap loop">overdetermined</GlossTerm> — only π stays
        irreducible.
      </>
    ),
    accent: "from-emerald-500 to-teal-500",
  },
  {
    icon: Shield,
    title: "Status discipline",
    body: (
      <>
        Every claim carries a{" "}
        <GlossTerm term="status markers">grade</GlossTerm> — [E] identity, [E]
        lattice theorem, [E] formalised, [E] numerical fixed point, [C] conditional,
        [O] open — and resolves to a single machine-checked ledger. The ledger wins
        on any disagreement.
      </>
    ),
    accent: "from-orange-500 to-amber-500",
  },
];

export function Overview() {
  return (
    <section
      id="overview"
      className="relative scroll-mt-20 py-14 sm:py-16"
      aria-labelledby="overview-heading"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="What the compiler derives"
          title="One compiler reads off the Standard Model, the constants and the scales"
          description="The same small integers (2, 3, 5, 16, 240, 248) recur across every sector because they come from one source: a single machine, fed by two inputs, builds E₈ and reads off the Standard-Model skeleton, the constants, and the scale grammar — dozens of real numbers, none fitted in the closed branch."
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
                The μ₄ glue — E₈ as a closure, not an input
              </span>
            </div>
            <div className="p-6">
              <p className="text-sm leading-relaxed text-slate-300">
                D₅ = so(10) (spinor 16) and A₃ = su(4) (the four-puncture family
                geometry) share the{" "}
                <span className="font-semibold text-slate-100">same</span>{" "}
                discriminant group ℤ₄. Their glue norms add to the E₈ root norm:
              </p>
              <div className="mt-3 grid gap-2 text-xs">
                <div className="rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
                  <span className="font-mono text-blue-300">1.</span>{" "}
                  <Math>{"\\operatorname{disc}(D_5) = \\operatorname{disc}(A_3) = \\mathbb{Z}_4"}</Math>
                </div>
                <div className="rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
                  <span className="font-mono text-blue-300">2.</span>{" "}
                  <Math>{"q(D_5) + q(A_3) = \\tfrac{5}{4} + \\tfrac{3}{4} = 2"}</Math>
                  <span className="text-slate-400">
                    {" "}
                    = the E₈ root norm
                  </span>
                </div>
                <div className="rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
                  <span className="font-mono text-blue-300">3.</span>{" "}
                  <Math>{"|R(E_8)| = 16\\cdot 5\\cdot 3 = 240"}</Math>
                  <span className="text-slate-400">
                    {" "}
                    , <Math>{"\\dim E_8 = 240 + 8 = 248"}</Math>
                  </span>
                </div>
              </div>
              <div className="mt-3 overflow-x-auto rounded-lg border border-blue-400/30 bg-blue-500/5 p-3">
                <Math
                  block
                  plain="E₈ is the lattice D₅ together with A₃, glued by the μ₄ simple current."
                >
                  {"E_8 = (D_5 \\oplus A_3) + \\mu_4"}
                </Math>
              </div>
              <p className="mt-2 text-xs text-slate-400">
                A closed lattice-theoretic construction — not a blind positing
                of 248. The E₈ numbers are carrier traces, not inputs.
              </p>
            </div>
          </div>

          <div className="glass rounded-2xl ring-1 ring-emerald-400/20">
            <div className="border-b border-slate-800/60 px-5 py-3">
              <span className="text-[11px] font-semibold uppercase tracking-widest text-emerald-300/80">
                The electromagnetic fixed point{" "}
                <span className="math-label">α</span>
              </span>
            </div>
            <div className="p-6">
              <p className="text-sm leading-relaxed text-slate-300">
                The fine-structure constant is the unique positive root of a
                parameter-free cubic built only from c₃ and the abelian
                coefficient 41 = 10 b₁ — existence and uniqueness are proved:
              </p>
              <div className="mt-3 overflow-x-auto rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
                <Math
                  block
                  plain="A parameter-free cubic in α, built only from c₃ and the abelian coefficient 41, set to zero."
                >
                  {"F_{U(1)}(\\alpha) = \\alpha^3 - 2c_3^3\\alpha^2 - \\tfrac{4}{5}c_3^6\\cdot 41 \\log\\tfrac{1}{\\varphi_{\\mathrm{seam}}(\\alpha)} = 0"}
                </Math>
              </div>
              <div className="mt-2 overflow-x-auto rounded-lg border border-emerald-400/30 bg-emerald-500/5 p-3">
                <Math
                  block
                  plain="Its unique positive root gives the inverse fine-structure constant, about 137.0359992168."
                >
                  {"\\Rightarrow \\alpha^{-1} = 137.035\\,999\\,216\\,8\\ldots"}
                </Math>
              </div>
              <p className="mt-3 text-xs text-slate-400">
                CODATA-2022 recommends{" "}
                <span className="font-mono text-slate-200">
                  137.035 999 177(21)
                </span>
                ; the deviation is{" "}
                <span className="font-mono text-slate-200">2.9 × 10⁻¹⁰</span>,
                about <span className="font-mono text-slate-200">1.9σ</span> of
                its uncertainty — a fixed point, not a fit.
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

        {/* Progressive disclosure: the deep mechanism visuals live here, not in the hero */}
        <details className="group mt-14 border border-slate-700/50 bg-slate-950/40 open:bg-slate-950/60">
          <summary className="cursor-pointer list-none px-5 py-4 marker:content-none [&::-webkit-details-marker]:hidden">
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="font-mono text-[11px] font-semibold uppercase tracking-widest text-slate-500">
                  How it works — detail
                </div>
                <div className="mt-1 font-serif text-lg font-semibold text-slate-100">
                  Unpack the compiler &amp; the three decoders
                </div>
              </div>
              <span className="font-mono text-xs text-slate-500 transition-transform group-open:rotate-90">
                →
              </span>
            </div>
          </summary>
          <div className="border-t border-slate-800/60 px-2 pb-6 sm:px-4">
            <TheoryUnpacking />
            <ThreeDecoderMap />
          </div>
        </details>
      </div>
    </section>
  );
}
