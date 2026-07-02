"use client";

import { motion } from "motion/react";
import { SectionHeader } from "@/components/SectionHeader";

interface Row {
  layer: string;
  status: string;
  paper: string;
  tone: "core" | "bridge" | "conditional" | "downstream";
}

const ROWS: Row[] = [
  {
    layer: "Two axioms {c₃, g_car}",
    status: "Declared inputs — c₃ Gauss–Bonnet-hardenable, P2 algebra Lean-formalised",
    paper: "Doc 1",
    tone: "downstream",
  },
  {
    layer: "E₈ glue D₅ ⊕ A₃ + μ₄",
    status: "Lattice theorem — common discriminant ℤ₄, glue norms 5/4 + 3/4 = 2",
    paper: "Doc 1",
    tone: "core",
  },
  {
    layer: "Carrier traces 240, 248, b₁, det R",
    status: "Exact identities read off the carrier and the residue matrix",
    paper: "Docs 1–2",
    tone: "core",
  },
  {
    layer: "EM fixed point & flavor angles",
    status: "Numerical fixed points — α⁻¹ = 137.0359992, sin²θ₁₂, sin²θ₁₃",
    paper: "Docs 1–2",
    tone: "bridge",
  },
  {
    layer: "Masses, inflation, baryons",
    status: "Conditional — the φ₀-ladder, the R² scalaron, Ω_b and η_B",
    paper: "Docs 2, 4",
    tone: "conditional",
  },
  {
    layer: "Frontier items",
    status: "Honest handles — Koide, m_p/m_e, dark matter, now runnable typed solvers (v371–v375); the local Einstein equation Gₐᵦ+Λgₐᵦ=c₃⁻¹Tₐᵦ is parameter-free [E]; the ambient nonperturbative QG measure QG.AMB.01 is discharged as a redundancy [C] (v369+v379) and perturbative graviton unitarity is established [C] (v304/v370/v380)",
    paper: "Doc 4",
    tone: "conditional",
  },
  {
    layer: "Residual interfaces v_geo [O], G_net [C], F_transfer [C]",
    status: "Numbered research contracts — the scale anchor (open), the metric inclusion and the transfer functor (closed modulo cited theorems; extension leg on peer-reviewed crossed-product theorems, v469)",
    paper: "Doc 8",
    tone: "downstream",
  },
];

const TONE: Record<
  Row["tone"],
  { label: string; bg: string; text: string; ring: string; bar: string }
> = {
  core: {
    label: "[E]",
    bg: "bg-blue-500/15",
    text: "text-blue-200",
    ring: "ring-blue-400/30",
    bar: "from-blue-500 to-violet-500",
  },
  bridge: {
    label: "[E]",
    bg: "bg-emerald-500/15",
    text: "text-emerald-200",
    ring: "ring-emerald-400/30",
    bar: "from-emerald-500 to-teal-500",
  },
  conditional: {
    label: "[C]",
    bg: "bg-orange-500/15",
    text: "text-orange-200",
    ring: "ring-orange-400/30",
    bar: "from-orange-500 to-red-500",
  },
  downstream: {
    label: "[O]",
    bg: "bg-fuchsia-500/15",
    text: "text-fuchsia-200",
    ring: "ring-fuchsia-400/30",
    bar: "from-fuchsia-500 to-pink-500",
  },
};

export function StatusMatrix() {
  return (
    <section
      id="status-matrix"
      className="relative scroll-mt-24 py-20 sm:py-24"
      aria-labelledby="status-matrix-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="Status discipline"
          title="The status matrix"
          description="Every layer of the dependency DAG carries its own grade — exact identity, lattice theorem, numerical fixed point, conditional, or open. The single source of truth is the machine-checked status ledger; if the text and the ledger ever disagree, the ledger wins."
        />

        <div className="mt-10 overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/40">
          <div className="hidden grid-cols-[1.5fr_2fr_1fr_1.4fr] gap-px border-b border-slate-800/60 bg-slate-800/40 px-5 py-3 text-[10px] font-semibold uppercase tracking-widest text-slate-300 md:grid">
            <span>Layer</span>
            <span>Status language</span>
            <span>Tone</span>
            <span>Where handled</span>
          </div>

          <ul className="divide-y divide-slate-800/60">
            {ROWS.map((r, i) => {
              const t = TONE[r.tone];
              return (
                <motion.li
                  key={r.layer}
                  initial={{ opacity: 0, y: 8 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.05 }}
                  transition={{ duration: 0.45, delay: i * 0.04 }}
                  className="relative grid gap-3 px-5 py-5 transition-colors hover:bg-slate-900/40 md:grid-cols-[1.5fr_2fr_1fr_1.4fr] md:items-center md:gap-6 md:py-4"
                >
                  <div
                    className={`absolute left-0 top-0 h-full w-1 bg-gradient-to-b ${t.bar} opacity-80 md:opacity-100`}
                    aria-hidden
                  />
                  <div className="font-serif text-base font-semibold text-slate-50">
                    {r.layer}
                  </div>
                  <div className="text-sm text-slate-300">{r.status}</div>
                  <div>
                    <span
                      className={`inline-flex rounded-full px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest ring-1 ${t.bg} ${t.text} ${t.ring}`}
                    >
                      {t.label}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 md:text-sm">{r.paper}</div>
                </motion.li>
              );
            })}
          </ul>
        </div>
      </div>
    </section>
  );
}
